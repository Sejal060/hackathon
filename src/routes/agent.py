# src/routes/agent.py
from fastapi import APIRouter, Depends
from ..models import AgentRequest, AgentResponse
from ..mcp_router import route_mcp
from ..reward import RewardSystem
from ..judging_engine import JudgingEngine
from datetime import datetime
from ..bucket_connector import relay_to_bucket
from ..logger import ksml_logger
from ..auth import get_api_key

router = APIRouter(prefix="/agent", tags=["agent"])

# Initialize the judging engine
judging_engine = JudgingEngine()

@router.post("/", response_model=AgentResponse, summary="Process agent requests", dependencies=[Depends(get_api_key)])
async def agent_endpoint(request: AgentRequest):
    """
    Process agent requests and generate responses.
    
    - **team_id**: ID of the team making the request
    - **prompt**: The prompt or query from the team
    - **metadata**: Additional context data
    """
    try:
        # Log the agent request using KSML
        ksml_logger.log_agent_request(request.team_id, request.prompt, request.metadata)

        result = route_mcp(request.dict())

        # Calculate reward using the reward system
        reward_system = RewardSystem()
        reward_value, feedback = reward_system.calculate_reward(result.get("action", ""), "success")

        # Evaluate the result with the judging engine
        try:
            judge_result = judging_engine.evaluate(result.get("result", ""), request.team_id)

            # Store judge score in MongoDB
            judge_data = {
                "team_id": request.team_id,
                "submission_text": result.get("result", ""),
                "judge_result": judge_result,
                "timestamp": datetime.now().isoformat()
            }
            relay_to_bucket(judge_data)

            # Log the judging result
            ksml_logger.log_event(
                intent="judging_evaluation",
                actor="judging_engine",
                context=f"Judging evaluation completed for team {request.team_id}",
                outcome="success",
                additional_data={"total_score": judge_result["total_score"]}
            )
        except Exception as e:
            ksml_logger.log_event(
                intent="judging_evaluation",
                actor="judging_engine",
                context=f"Judging evaluation failed for team {request.team_id}: {str(e)}",
                outcome="error"
            )

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
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")