from langgraph.graph import StateGraph
from typing import Dict, Any
import logging
from src.database import get_db
from src.judging.multi_agent_judge import evaluate_submission_multi_agent
from src.judging.consensus import aggregate_consensus
from src.logger import KSMLLogger
import os

logger = logging.getLogger(__name__)
ksml_logger = KSMLLogger()

async def assign_judge(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # pick judge (simple round-robin placeholder)
    db = get_db()
    judges = list(db.judges.find({"active": True}))
    judge_id = judges[0]["_id"] if judges else "auto_judge"
    ctx["judge_id"] = str(judge_id)
    return ctx

async def score_rubric_criteria(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Score rubric criteria using multi-agent judging system
    submission_text = ctx.get("submission_text", "")
    team_id = ctx.get("team_id", "")
    
    # Use the multi-agent judging engine to evaluate the submission
    evaluation_result = evaluate_submission_multi_agent({
        "submission_text": submission_text,
        "team_id": team_id
    })
    
    ctx["evaluation_result"] = evaluation_result
    return ctx

async def persist_score(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Persist the score to the database
    db = get_db()
    
    # Insert score record with individual and consensus scores
    score_record = {
        "team_id": ctx.get("team_id", ""),
        "project_id": ctx.get("project_id", ""),
        "judge_id": ctx.get("judge_id", ""),
        "individual_scores": ctx.get("evaluation_result", {}).get("individual_scores", {}),
        "consensus_score": ctx.get("evaluation_result", {}).get("consensus_score", 0),
        "criteria_scores": ctx.get("evaluation_result", {}).get("criteria_scores", {}),
        "submitted_at": ctx.get("submitted_at"),
        "evaluated_at": ctx.get("evaluated_at"),
        "reasoning_chain": ctx.get("evaluation_result", {}).get("reasoning_chain", "")
    }
    
    db.scores.insert_one(score_record)
    return ctx

async def log_provenance(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Log provenance of the judging process
    ksml_logger.log_event(
        intent="judging_process",
        actor=f"judge_{ctx.get('judge_id', 'unknown')}",
        context=f"Judging completed for project {ctx.get('project_id', '')} by team {ctx.get('team_id', '')}",
        outcome="completed",
        additional_data={
            "team_id": ctx.get("team_id", ""),
            "project_id": ctx.get("project_id", ""),
            "judge_id": ctx.get("judge_id", ""),
            "score": ctx.get("evaluation_result", {}).get("consensus_score", 0),
            "individual_scores": ctx.get("evaluation_result", {}).get("individual_scores", {}),
            "reasoning_chain": ctx.get("evaluation_result", {}).get("reasoning_chain", "")
        }
    )
    return ctx

def build_judge_flow():
    g = StateGraph(dict)
    g.add_node("assign_judge", assign_judge)
    g.add_node("score_rubric_criteria", score_rubric_criteria)
    g.add_node("persist_score", persist_score)
    g.add_node("log_provenance", log_provenance)
    g.set_entry_point("assign_judge")
    g.add_edge("assign_judge", "score_rubric_criteria")
    g.add_edge("score_rubric_criteria", "persist_score")
    g.add_edge("persist_score", "log_provenance")
    g.set_finish_point("log_provenance")
    return g.compile()