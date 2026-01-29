# src/routes/judge.py
from fastapi import APIRouter, Depends
from ..models import JudgeRequest, JudgeResponse
from ..judging.multi_agent_judge import MultiAgentJudge, evaluate_submission_multi_agent
from ..judging.consensus import aggregate_consensus
from ..logger import ksml_logger
from ..auth import get_api_key
from ..schemas.response import APIResponse
from ..database import get_db
from ..security import create_entry, compute_payload_hash
from typing import Dict, Any
import logging
import hashlib
import time

# Set up logging
logger = logging.getLogger(__name__)

# Define the judge router
router = APIRouter(prefix="/judge", tags=["judge"])

# Initialize the multi-agent judging engine
multi_agent_judge = MultiAgentJudge()

@router.post("/score", response_model=JudgeResponse, summary="Scores a single submission", dependencies=[Depends(get_api_key)])
async def score_submission(request: JudgeRequest):
    """
    Scores a single submission using the Multi-Agent AI Judging Engine.
    
    - **submission_text**: The text to evaluate
    - **team_id**: Optional team ID for tracking
    """
    logger.info(f"Score submission endpoint called for team {request.team_id}")
    
    # Log the judging request using KSML
    ksml_logger.log_event(
        intent="judging_request",
        actor=f"team_{request.team_id}" if request.team_id else "anonymous",
        context=f"Multi-agent judging request received for submission of length {len(request.submission_text)}",
        outcome="received",
        tenant_id=request.tenant_id,
        event_id=request.event_id,
        workspace_id=request.workspace_id
    )
    
    # Evaluate the submission using multi-agent system
    evaluation_result = evaluate_submission_multi_agent({
        "submission_text": request.submission_text,
        "team_id": request.team_id,
        "tenant_id": request.tenant_id,
        "event_id": request.event_id
    })
    
    # Extract consensus scores for the response
    consensus_scores = evaluation_result["criteria_scores"]
    
    # Log the judging response
    ksml_logger.log_event(
        intent="judging_response",
        actor="multi_agent_judging_engine",
        context=f"Multi-agent judging completed for team {request.team_id}",
        outcome="success",
        additional_data={"consensus_score": evaluation_result["consensus_score"]},
        tenant_id=request.tenant_id,
        event_id=request.event_id,
        workspace_id=request.workspace_id
    )
    
    # Return the structured response
    return JudgeResponse(
        clarity=consensus_scores.get("clarity", 0),
        quality=consensus_scores.get("tech_depth", 0),  # tech_depth maps to quality
        innovation=consensus_scores.get("innovation", 0),
        total_score=evaluation_result["consensus_score"],
        confidence=evaluation_result.get("confidence", 0.9),
        trace=evaluation_result["reasoning_chain"],
        team_id=request.team_id,
        fallback=evaluation_result.get("fallback")
    )

@router.post("/submit", response_model=Dict[str, Any], summary="Saves and scores a submission", dependencies=[Depends(get_api_key)])
async def submit_and_score(request: JudgeRequest):
    """
    Saves and scores a submission using the Multi-Agent AI Judging Engine.

    - **submission_text**: The text to evaluate
    - **team_id**: Optional team ID for tracking
    """
    logger.info(f"Submit and score endpoint called for team {request.team_id}")

    # Compute submission hash
    submission_hash = hashlib.sha256(request.submission_text.encode('utf-8')).hexdigest()
    request.submission_hash = submission_hash

    # Get database connection
    db = get_db()

    # Check if submission already exists
    existing_submission = db.submissions.find_one({"submission_hash": submission_hash})
    if existing_submission:
        logger.info(f"Submission already exists with hash {submission_hash}")
    else:
        # Save submission to database
        submission_doc = {
            "submission_text": request.submission_text,
            "team_id": request.team_id,
            "submission_hash": submission_hash,
            "tenant_id": request.tenant_id,
            "event_id": request.event_id,
            "workspace_id": request.workspace_id,
            "timestamp": int(time.time())
        }
        db.submissions.insert_one(submission_doc)
        logger.info(f"Submission saved for team {request.team_id} with hash {submission_hash}")

    # Log the submission using KSML and create provenance
    ksml_logger.log_event(
        intent="submission_save",
        actor=f"team_{request.team_id}" if request.team_id else "anonymous",
        context=f"Submission saved with hash {submission_hash}",
        outcome="success",
        tenant_id=request.tenant_id,
        event_id=request.event_id,
        workspace_id=request.workspace_id
    )

    # Create provenance entry for submission
    create_entry(
        db,
        actor=f"team_{request.team_id}" if request.team_id else "anonymous",
        event="submission_save",
        payload={
            "submission_hash": submission_hash,
            "team_id": request.team_id,
            "tenant_id": request.tenant_id,
            "event_id": request.event_id,
            "workspace_id": request.workspace_id
        },
        event_id=request.event_id,
        outcome="success"
    )

    # Evaluate the submission using multi-agent system
    evaluation_result = evaluate_submission_multi_agent({
        "submission_text": request.submission_text,
        "team_id": request.team_id,
        "tenant_id": request.tenant_id,
        "event_id": request.event_id
    })

    # Extract consensus scores for the response
    consensus_scores = evaluation_result["criteria_scores"]

    # Determine version for judgment
    existing_judgment = db.judgments.find_one(
        {"submission_hash": submission_hash},
        sort=[("version", -1)]
    )
    version = (existing_judgment["version"] + 1) if existing_judgment else 1

    # Save judgment to database
    judgment_doc = {
        "submission_hash": submission_hash,
        "team_id": request.team_id,
        "clarity": consensus_scores.get("clarity", 0),
        "quality": consensus_scores.get("tech_depth", 0),
        "innovation": consensus_scores.get("innovation", 0),
        "total_score": evaluation_result["consensus_score"],
        "confidence": evaluation_result.get("confidence", 0.9),
        "trace": evaluation_result["reasoning_chain"],
        "version": version,
        "tenant_id": request.tenant_id,
        "event_id": request.event_id,
        "workspace_id": request.workspace_id,
        "timestamp": int(time.time())
    }
    if evaluation_result.get("fallback"):
        judgment_doc["fallback"] = True
    db.judgments.insert_one(judgment_doc)
    logger.info(f"Judgment saved for submission {submission_hash}, version {version}")

    # Log the judging response
    ksml_logger.log_event(
        intent="judgment_save",
        actor="multi_agent_judging_engine",
        context=f"Judgment saved for submission {submission_hash}, version {version}",
        outcome="success",
        additional_data={"consensus_score": evaluation_result["consensus_score"], "version": version},
        tenant_id=request.tenant_id,
        event_id=request.event_id,
        workspace_id=request.workspace_id
    )

    # Create provenance entry for judgment
    create_entry(
        db,
        actor="multi_agent_judging_engine",
        event="judgment_save",
        payload={
            "submission_hash": submission_hash,
            "version": version,
            "total_score": evaluation_result["consensus_score"],
            "team_id": request.team_id,
            "tenant_id": request.tenant_id,
            "event_id": request.event_id,
            "workspace_id": request.workspace_id
        },
        event_id=request.event_id,
        outcome="success"
    )

    # Return the structured response with both submission and judging results
    return APIResponse(
        success=True,
        message="Submission saved and multi-agent scored successfully",
        data={
            "submission": {
                "text": request.submission_text,
                "team_id": request.team_id,
                "submission_hash": submission_hash
            },
            "judging_result": {
                "individual_scores": evaluation_result["individual_scores"],
                "consensus_score": evaluation_result["consensus_score"],
                "criteria_scores": consensus_scores,
                "reasoning_chain": evaluation_result["reasoning_chain"],
                "confidence": evaluation_result.get("confidence", 0.9),
                "version": version,
                **({"fallback": True} if evaluation_result.get("fallback") else {})
            }
        }
    )

@router.get("/rubric", response_model=Dict[str, Any], summary="Returns judging criteria", dependencies=[Depends(get_api_key)])
async def get_rubric():
    """
    Returns the judging criteria used by the Multi-Agent AI Judging Engine.
    """
    logger.info("Rubric endpoint called")
    
    # Import the rubric from the new rubric module
    from ..judging.rubric import CRITERIA, WEIGHTS, TOTAL_POSSIBLE_SCORE
    
    # Return the rubric
    rubric_data = {
        "criteria": CRITERIA,
        "weights": WEIGHTS,
        "total_possible_score": TOTAL_POSSIBLE_SCORE
    }
    
    return APIResponse(
        success=True,
        message="Multi-agent judging criteria retrieved successfully",
        data=rubric_data
    )