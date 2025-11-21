# src/routes/admin.py
from fastapi import APIRouter, Depends
from ..models import RewardRequest, RewardResponse, LogRequest, TeamRegistration
from ..bucket_connector import relay_to_bucket
from ..reward import RewardSystem
from datetime import datetime
from ..logger import ksml_logger
from ..main import get_api_key

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reward", response_model=RewardResponse, summary="Apply reward to a request", dependencies=[Depends(get_api_key)])
def reward_endpoint(request: RewardRequest):
    """
    Calculate and apply rewards based on request outcome.
    
    - **request_id**: ID of the request to apply reward to
    - **outcome**: Outcome of the request (success, failure, etc.)
    """
    # Apply reward logic
    reward_system = RewardSystem()
    reward_value, feedback = reward_system.calculate_reward(f"Request {request.request_id}", request.outcome)
    
    # Log the reward calculation using KSML
    ksml_logger.log_reward_calculation(request.request_id, request.outcome, reward_value)
    
    return RewardResponse(reward_value=reward_value, feedback=feedback)

@router.post("/logs", summary="Relay logs to bucket", dependencies=[Depends(get_api_key)])
def logs_endpoint(request: LogRequest):
    """
    Relay logs to the BHIV Bucket.
    
    - **timestamp**: Timestamp of the log entry
    - **level**: Log level (INFO, ERROR, etc.)
    - **message**: Log message
    - **additional_data**: Optional additional data
    """
    # Convert Pydantic model to dict for relay_to_bucket
    log_data = request.dict()
    result = relay_to_bucket(log_data)
    return {"status": "logged", "result": result}

@router.post("/register", summary="Register a new team", dependencies=[Depends(get_api_key)])
def register_endpoint(team: TeamRegistration):
    """
    Register a new team for the hackathon.
    
    - **team_name**: Name of the team
    - **members**: List of team members
    - **project_title**: Title of the team's project
    """
    # Log the registration using KSML
    ksml_logger.log_registration(team.team_name, team.project_title)
    
    return {"message": "Team registered successfully", "team_id": f"team_{team.team_name.lower().replace(' ', '_')}"}

@router.post("/webhook/hackaverse/registration", summary="N8N webhook for team registration")
def webhook_registration(payload: TeamRegistration):
    """
    N8N webhook endpoint for team registration automation.
    
    - **team_name**: Name of the team
    - **members**: List of team members
    - **project_title**: Title of the team's project
    """
    # Log the registration using KSML
    ksml_logger.log_registration(payload.team_name, payload.project_title)
    
    # Add registration logic if needed
    return {"status": "registered", "team_id": f"team_{payload.team_name.lower().replace(' ', '_')}"}