# src/routes/judge.py
from fastapi import APIRouter, Depends
from ..models import JudgeRequest, JudgeResponse
from ..judging_engine import JudgingEngine
from ..logger import ksml_logger
from ..auth import get_api_key
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define the judge router
router = APIRouter(prefix="/judge", tags=["judge"])

# Initialize the judging engine
judging_engine = JudgingEngine()

@router.post("/", response_model=JudgeResponse, summary="Evaluate a submission with AI judging")
def judge_endpoint(request: JudgeRequest):
    """
    Evaluate a submission using the AI Judging Engine.
    
    - **submission_text**: The text to evaluate
    - **team_id**: Optional team ID for tracking
    """
    logger.info(f"Judge endpoint called for team {request.team_id}")
    
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