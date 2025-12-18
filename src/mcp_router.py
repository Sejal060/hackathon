# src/mcp_router.py
from typing import Dict, Any
from .input_handler import InputHandler
from .reasoning import ReasoningModule
from .executor import Executor
from .core_connector import connect_to_core
from .bucket_connector import relay_to_bucket
from .logger import ksml_logger
from datetime import datetime
import asyncio

# Import the new MCP routing components
from src.mcp.agent_registry import AGENT_REGISTRY
from src.mcp.load_balancer import RoundRobinBalancer

# Initialize load balancers for each agent type
_balancers = {
    role: RoundRobinBalancer(agents)
    for role, agents in AGENT_REGISTRY.items()
}

async def route_message(agent_type: str, payload: dict):
    """Route message to appropriate agent with load balancing and forwarding support."""
    
    # Log the routing event
    ksml_logger.log_event(
        intent="agent_routing",
        actor="mcp_router",
        context=f"Routing to agent type: {agent_type}",
        outcome="started"
    )
    
    # Get the appropriate balancer or default
    balancer = _balancers.get(agent_type, _balancers["default"])
    agent = balancer.next()

    # Handle the message with the selected agent
    result = await agent.handle(payload)

    # Check if we need to forward to another agent
    next_agent = result.get("forward_to")
    if next_agent:
        # Recursive call to route to the next agent
        forwarded_result = await route_message(next_agent, result)
        # Merge results
        result.update(forwarded_result)

    return result

def route_mcp(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Coordinate MCP agents: input -> reason -> execute."""
    # Initialize modules
    input_handler = InputHandler()
    reasoning = ReasoningModule()
    executor = Executor()
    
    team_id = payload.get("team_id", "unknown")
    
    # Log input processing start using KSML
    ksml_logger.log_event(
        intent="input_processing",
        actor="mcp_router",
        context=str(payload),
        outcome="started"
    )
    
    # Process the input
    input_data = input_handler.process_input(payload.get("prompt", ""))
    
    # Log input processing completion
    ksml_logger.log_event(
        intent="input_processing",
        actor="mcp_router",
        context=f"Processed: {input_data}",
        outcome="completed"
    )
    
    # Log reasoning start
    ksml_logger.log_event(
        intent="reasoning",
        actor="mcp_router",
        context=f"Input: {input_data}, Context: {payload.get('metadata', {})}",
        outcome="started"
    )
    
    # Generate reasoning plan
    context = payload.get("metadata", {})
    reasoning_result = reasoning.plan(input_data, context)
    
    # Log reasoning completion
    ksml_logger.log_event(
        intent="reasoning",
        actor="mcp_router",
        context=f"Plan: {reasoning_result}",
        outcome="completed"
    )
    
    # Log execution start
    ksml_logger.log_event(
        intent="execution",
        actor="mcp_router",
        context=f"Action: {reasoning_result}",
        outcome="started"
    )
    
    # Execute the plan
    result = executor.execute(reasoning_result)
    
    # Log execution completion
    ksml_logger.log_event(
        intent="execution",
        actor="mcp_router",
        context=f"Result: {result}",
        outcome="completed"
    )
    
    # Send to BHIV Core
    core_payload = {
        "input": input_data,
        "action": reasoning_result,
        "result": result,
        "team_id": team_id
    }
    
    # Log core communication start
    ksml_logger.log_event(
        intent="core_communication",
        actor="mcp_router",
        context=str(core_payload),
        outcome="started"
    )
    
    core_response = connect_to_core(core_payload)
    
    # Log core communication completion
    ksml_logger.log_core_communication(team_id, core_payload, core_response)
    
    # Log overall flow completion
    ksml_logger.log_event(
        intent="mcp_flow",
        actor="mcp_router",
        context=f"Team: {team_id}",
        outcome="success"
    )
    
    return {
        "processed_input": input_data,
        "action": reasoning_result,
        "result": result,
        "core_response": core_response
    }