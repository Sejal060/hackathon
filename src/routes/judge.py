# src/routes/judge.py
from fastapi import APIRouter, Depends
from ..models import JudgeRequest, JudgeResponse
from ..judging.multi_agent_judge import MultiAgentJudge, evaluate_submission_multi_agent
from ..judging.consensus import aggregate_consensus
from ..logger import ksml_logger
from ..auth import get_api_key
from ..schemas.response import APIResponse
from typing import Dict, Any
import logging
from ..security import verify_nonce_only

# Set up logging
logger = logging.getLogger(__name__)

# Define the judge router
router = APIRouter(prefix="/judge", tags=["judge"])

# Initialize the multi-agent judging engine
multi_agent_judge = MultiAgentJudge()

@router.post("/score", response_model=JudgeResponse, summary="Scores a single submission")
async def score_submission(request: JudgeRequest, nonce=Depends(verify_nonce_only)):
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
        outcome="received"
    )
    
    # Evaluate the submission using multi-agent system
    evaluation_result = evaluate_submission_multi_agent({
        "submission_text": request.submission_text,
        "team_id": request.team_id
    })
    
    # Extract consensus scores for the response
    consensus_scores = evaluation_result["criteria_scores"]
    
    # Log the judging response
    ksml_logger.log_event(
        intent="judging_response",
        actor="multi_agent_judging_engine",
        context=f"Multi-agent judging completed for team {request.team_id}",
        outcome="success",
        additional_data={"consensus_score": evaluation_result["consensus_score"]}
    )
    
    # Return the structured response
    return JudgeResponse(
        clarity=consensus_scores.get("clarity", 0),
        quality=consensus_scores.get("tech_depth", 0),  # tech_depth maps to quality
        innovation=consensus_scores.get("innovation", 0),
        total_score=evaluation_result["consensus_score"],
        confidence=0.9,  # Placeholder - would be from actual result
        trace=evaluation_result["reasoning_chain"],
        team_id=request.team_id
    )

@router.post("/submit", response_model=Dict[str, Any], summary="Saves and scores a submission")
async def submit_and_score(request: JudgeRequest, nonce=Depends(verify_nonce_only)):
    """
    Saves and scores a submission using the Multi-Agent AI Judging Engine.
    
    - **submission_text**: The text to evaluate
    - **team_id**: Optional team ID for tracking
    """
    logger.info(f"Submit and score endpoint called for team {request.team_id}")
    
    # In a production environment, you would save the submission to a database here
    # For now, we'll just log that the submission was received
    logger.info(f"Submission saved for team {request.team_id}")
    
    # Log the judging request using KSML
    ksml_logger.log_event(
        intent="submission_save_and_judge",
        actor=f"team_{request.team_id}" if request.team_id else "anonymous",
        context=f"Submission saved and multi-agent judging request received for submission of length {len(request.submission_text)}",
        outcome="received"
    )
    
    # Evaluate the submission using multi-agent system
    evaluation_result = evaluate_submission_multi_agent({
        "submission_text": request.submission_text,
        "team_id": request.team_id
    })
    
    # Extract consensus scores for the response
    consensus_scores = evaluation_result["criteria_scores"]
    
    # Log the judging response
    ksml_logger.log_event(
        intent="submission_judged",
        actor="multi_agent_judging_engine",
        context=f"Submission multi-agent judged for team {request.team_id}",
        outcome="success",
        additional_data={"consensus_score": evaluation_result["consensus_score"]}
    )
    
    # Return the structured response with both submission and judging results
    return APIResponse(
        success=True,
        message="Submission saved and multi-agent scored successfully",
        data={
            "submission": {
                "text": request.submission_text,
                "team_id": request.team_id
            },
            "judging_result": {
                "individual_scores": evaluation_result["individual_scores"],
                "consensus_score": evaluation_result["consensus_score"],
                "criteria_scores": consensus_scores,
                "reasoning_chain": evaluation_result["reasoning_chain"],
                "confidence": 0.9  # Placeholder - would be from actual result
            }
        }
    )

@router.get("/rubric", response_model=Dict[str, Any], summary="Returns judging criteria")
async def get_rubric(nonce=Depends(verify_nonce_only)):
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