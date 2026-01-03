# src/routes/admin.py
from fastapi import APIRouter, Depends
from ..models import RewardRequest, RewardResponse, LogRequest, TeamRegistration
from ..bucket_connector import relay_to_bucket
from ..reward import RewardSystem
from datetime import datetime
from ..logger import ksml_logger
from ..auth import get_api_key
from ..schemas.response import APIResponse
from ..security import verify_nonce_only

router = APIRouter(prefix="", tags=["admin"])

@router.post("/reward", response_model=RewardResponse, summary="Apply reward to a request", dependencies=[Depends(get_api_key)])
async def reward_endpoint(request: RewardRequest):
    """
    Calculate and apply rewards based on request outcome.
    
    - **request_id**: ID of the request to apply reward to
    - **outcome**: Outcome of the request (success, failure, etc.)
    """
    try:
        # Apply reward logic
        reward_system = RewardSystem()
        reward_value, feedback = reward_system.calculate_reward(f"Request {request.request_id}", request.outcome)

        # Log the reward calculation using KSML
        ksml_logger.log_reward_calculation(request.request_id, request.outcome, reward_value)

        return RewardResponse(reward_value=reward_value, feedback=feedback)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/logs", summary="Relay logs to bucket", dependencies=[Depends(get_api_key)])
async def logs_endpoint(request: LogRequest):
    """
    Relay logs to the BHIV Bucket.
    
    - **timestamp**: Timestamp of the log entry
    - **level**: Log level (INFO, ERROR, etc.)
    - **message**: Log message
    - **additional_data**: Optional additional data
    """
    try:
        # Convert Pydantic model to dict for relay_to_bucket
        log_data = request.dict()
        result = relay_to_bucket(log_data)
        return APIResponse(
            success=True,
            message="Logs relayed successfully",
            data={"status": "logged", "result": result}
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message=f"Error relaying logs: {str(e)}",
            data=None
        )

@router.post("/registration", summary="Register a new team", dependencies=[Depends(get_api_key)])
async def register_endpoint(team: TeamRegistration):
    """
    Register a new team for the hackathon.
    
    - **team_name**: Name of the team
    - **members**: List of team members
    - **project_title**: Title of the team's project
    """
    try:
        # Log the registration using KSML
        ksml_logger.log_registration(team.team_name, team.project_title)

        return APIResponse(
            success=True,
            message="Team registered successfully",
            data={"team_id": f"team_{team.team_name.lower().replace(' ', '_')}"}
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message=f"Error registering team: {str(e)}",
            data=None
        )

@router.post("/webhook/registration", summary="N8N webhook for team registration")
async def webhook_registration(payload: TeamRegistration):
    """
    N8N webhook endpoint for team registration automation (deprecated - use LangGraph flows).
    
    - **team_name**: Name of the team
    - **members**: List of team members
    - **project_title**: Title of the team's project
    """
    # Redirect to LangGraph flow for team registration
    from src.langgraph.runner import run_flow
    
    # Prepare the payload for the LangGraph flow
    flow_payload = {
        "team_name": payload.team_name,
        "members": payload.members,
        "project_title": payload.project_title,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        result = await run_flow("team_registration", flow_payload)
        return APIResponse(
            success=True,
            message="Team registration processed via LangGraph flow",
            data={"status": "registered", "result": result}
        )
    except Exception as e:
        # Fallback to original logic if LangGraph flow fails
        ksml_logger.log_registration(payload.team_name, payload.project_title)
        return APIResponse(
            success=True,
            message="Team registered via fallback",
            data={"status": "registered", "team_id": f"team_{payload.team_name.lower().replace(' ', '_')}"}
        )