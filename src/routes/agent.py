# src/routes/agent.py
from fastapi import APIRouter
from ..models import AgentRequest, AgentResponse
from ..mcp_router import route_mcp

router = APIRouter(prefix="/agent")

@router.post("/", response_model=AgentResponse)
def agent_endpoint(request: AgentRequest):
    result = route_mcp(request.dict())
    # Add reward calculation
    # For now, we'll use a simple reward calculation
    reward = len(result.get("result", "")) * 0.1
    
    # Return the response with the core response included
    return AgentResponse(
        processed_input=result["processed_input"],
        action=result["action"],
        result=result["result"],
        reward=reward,
        core_response=result.get("core_response")
    )