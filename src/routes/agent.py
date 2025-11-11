# src/routes/agent.py
from fastapi import APIRouter
from ..models import AgentRequest, AgentResponse
from ..mcp_router import route_mcp
from ..reward import RewardSystem
from datetime import datetime
from ..bucket_connector import relay_to_bucket
from ..logger import ksml_logger

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/", response_model=AgentResponse, summary="Process agent requests")
def agent_endpoint(request: AgentRequest):
    """
    Process agent requests and generate responses.
    
    - **team_id**: ID of the team making the request
    - **prompt**: The prompt or query from the team
    - **metadata**: Additional context data
    """
    # Log the agent request using KSML
    ksml_logger.log_agent_request(request.team_id, request.prompt, request.metadata)
    
    result = route_mcp(request.dict())
    
    # Calculate reward using the reward system
    reward_system = RewardSystem()
    reward_value, feedback = reward_system.calculate_reward(result.get("action", ""), "success")
    
    # Log the agent response
    ksml_logger.log_agent_response(request.team_id, result)
    
    # Return the response with the calculated reward
    return AgentResponse(
        processed_input=result["processed_input"],
        action=result["action"],
        result=result["result"],
        reward=reward_value,
        core_response=result.get("core_response")
    )