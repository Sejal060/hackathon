# src/mcp_router.py
from typing import Dict, Any
from .input_handler import InputHandler
from .reasoning import ReasoningModule
from .executor import Executor
from .core_connector import connect_to_core
from .bucket_connector import relay_to_bucket
from datetime import datetime

def route_mcp(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Coordinate MCP agents: input -> reason -> execute."""
    # Initialize modules
    input_handler = InputHandler()
    reasoning = ReasoningModule()
    executor = Executor()
    
    # Log input processing start
    input_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "input_processing",
        "actor": "mcp_router",
        "context": str(payload),
        "outcome": "started"
    }
    relay_to_bucket(input_log)
    
    # Process the input
    input_data = input_handler.process_input(payload.get("prompt", ""))
    
    # Log input processing completion
    input_complete_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "input_processing",
        "actor": "mcp_router",
        "context": f"Processed: {input_data}",
        "outcome": "completed"
    }
    relay_to_bucket(input_complete_log)
    
    # Log reasoning start
    reasoning_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "reasoning",
        "actor": "mcp_router",
        "context": f"Input: {input_data}, Context: {payload.get('metadata', {})}",
        "outcome": "started"
    }
    relay_to_bucket(reasoning_log)
    
    # Generate reasoning plan
    context = payload.get("metadata", {})
    reasoning_result = reasoning.plan(input_data, context)
    
    # Log reasoning completion
    reasoning_complete_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "reasoning",
        "actor": "mcp_router",
        "context": f"Plan: {reasoning_result}",
        "outcome": "completed"
    }
    relay_to_bucket(reasoning_complete_log)
    
    # Log execution start
    execution_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "execution",
        "actor": "mcp_router",
        "context": f"Action: {reasoning_result}",
        "outcome": "started"
    }
    relay_to_bucket(execution_log)
    
    # Execute the plan
    result = executor.execute(reasoning_result)
    
    # Log execution completion
    execution_complete_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "execution",
        "actor": "mcp_router",
        "context": f"Result: {result}",
        "outcome": "completed"
    }
    relay_to_bucket(execution_complete_log)
    
    # Send to BHIV Core
    core_payload = {
        "input": input_data,
        "action": reasoning_result,
        "result": result,
        "team_id": payload.get("team_id", "unknown")
    }
    
    # Log core communication start
    core_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "core_communication",
        "actor": "mcp_router",
        "context": str(core_payload),
        "outcome": "started"
    }
    relay_to_bucket(core_log)
    
    core_response = connect_to_core(core_payload)
    
    # Log core communication completion
    core_complete_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "core_communication",
        "actor": "mcp_router",
        "context": str(core_response),
        "outcome": "completed"
    }
    relay_to_bucket(core_complete_log)
    
    # Log overall flow completion
    flow_complete_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "mcp_flow",
        "actor": "mcp_router",
        "context": f"Team: {payload.get('team_id', 'unknown')}",
        "outcome": "success"
    }
    relay_to_bucket(flow_complete_log)
    
    return {
        "processed_input": input_data,
        "action": reasoning_result,
        "result": result,
        "core_response": core_response
    }