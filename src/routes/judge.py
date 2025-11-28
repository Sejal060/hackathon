# src/routes/judge.py
from fastapi import APIRouter, Depends
from ..models import JudgeRequest, JudgeResponse
from ..judging_engine import JudgingEngine, evaluate_submission
from ..logger import ksml_logger
from ..auth import get_api_key
from typing import Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define the judge router
router = APIRouter(prefix="/judge", tags=["judge"])

# Initialize the judging engine
judging_engine = JudgingEngine()

@router.post("/score", response_model=JudgeResponse, summary="Scores a single submission")
def score_submission(request: JudgeRequest):
    """
    Scores a single submission using the AI Judging Engine.
    
    - **submission_text**: The text to evaluate
    - **team_id**: Optional team ID for tracking
    """
    logger.info(f"Score submission endpoint called for team {request.team_id}")
    
    # Log the judging request using KSML
    ksml_logger.log_event(
        intent="judging_request",
        actor=f"team_{request.team_id}" if request.team_id else "anonymous",
        context=f"Judging request received for submission of length {len(request.submission_text)}",
        outcome="received"
    )
    
    # Evaluate the submission
    result = judging_engine.evaluate(request.submission_text, request.team_id)
    
    # Log the judging response
    ksml_logger.log_event(
        intent="judging_response",
        actor="judging_engine",
        context=f"Judging completed for team {request.team_id}",
        outcome="success",
        additional_data={"total_score": result["total_score"]}
    )
    
    # Return the structured response
    return JudgeResponse(
        clarity=result["clarity"],
        quality=result["quality"],
        innovation=result["innovation"],
        total_score=result["total_score"],
        confidence=result["confidence"],
        trace=result["trace"],
        team_id=result["team_id"]
    )

@router.post("/submit", response_model=Dict[str, Any], summary="Saves and scores a submission")
def submit_and_score(request: JudgeRequest):
    """
    Saves and scores a submission using the AI Judging Engine.
    
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
        context=f"Submission saved and judging request received for submission of length {len(request.submission_text)}",
        outcome="received"
    )
    
    # Evaluate the submission
    result = judging_engine.evaluate(request.submission_text, request.team_id)
    
    # Log the judging response
    ksml_logger.log_event(
        intent="submission_judged",
        actor="judging_engine",
        context=f"Submission judged for team {request.team_id}",
        outcome="success",
        additional_data={"total_score": result["total_score"]}
    )
    
    # Return the structured response with both submission and judging results
    return {
        "submission": {
            "text": request.submission_text,
            "team_id": request.team_id
        },
        "judging_result": {
            "clarity": result["clarity"],
            "quality": result["quality"],
            "innovation": result["innovation"],
            "total_score": result["total_score"],
            "confidence": result["confidence"],
            "trace": result["trace"],
            "team_id": result["team_id"]
        }
    }

@router.get("/rubric", response_model=Dict[str, str], summary="Returns judging criteria")
def get_rubric():
    """
    Returns the judging criteria used by the AI Judging Engine.
    """
    logger.info("Rubric endpoint called")
    
    # Return the rubric
    return judging_engine.rubric