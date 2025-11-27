#!/usr/bin/env python3
"""
LangGraph implementation for MentorBot prompt workflow
Replaces the N8N workflow with a more robust and maintainable solution
"""

from typing import Annotated, Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
import requests
import json
import os
from datetime import datetime

# Define the state structure for our workflow
class MentorBotState(MessagesState):
    """State for MentorBot prompt workflow"""
    team_id: str
    prompt: str
    metadata: Dict[str, Any]
    agent_response: Dict[str, Any]
    workflow_status: str

# Define tools for the workflow
@tool
def receive_mentor_request(team_id: str, prompt: str, metadata: Dict[str, Any] = {}) -> Dict[str, Any]:
    """Receive and validate mentor request"""
    return {
        "team_id": team_id,
        "prompt": prompt,
        "metadata": metadata,
        "timestamp": datetime.now().isoformat()
    }

@tool
def send_to_agent(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate sending request to the agent endpoint"""
    try:
        # Simulate successful agent response
        return {
            "status": "success",
            "processed_input": agent_data.get("prompt", ""),
            "action": "provide_guidance",
            "result": f"Here's guidance for your question: {agent_data.get('prompt', '')}",
            "reward": 0.8
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process agent request: {str(e)}"
        }

# Define nodes for the workflow
def receive_mentor_request_node(state: MentorBotState) -> Dict[str, Any]:
    """Node to receive and validate mentor request"""
    # Extract data from the last message (assuming it contains the mentor request)
    if state["messages"]:
        last_message = state["messages"][-1]
        if hasattr(last_message, 'content'):
            try:
                mentor_data = json.loads(last_message.content)
                validated_data = receive_mentor_request.invoke(mentor_data)
                return {
                    "team_id": validated_data["team_id"],
                    "prompt": validated_data["prompt"],
                    "metadata": validated_data["metadata"],
                    "workflow_status": "request_received"
                }
            except json.JSONDecodeError:
                return {
                    "workflow_status": "error",
                    "messages": [HumanMessage(content="Invalid JSON data received")]
                }
    
    return {
        "workflow_status": "waiting_for_data",
        "messages": [HumanMessage(content="Waiting for mentor request data")]
    }

def send_to_agent_node(state: MentorBotState) -> Dict[str, Any]:
    """Node to send request to agent"""
    if state["team_id"] and state["prompt"]:
        agent_data = {
            "team_id": state["team_id"],
            "prompt": state["prompt"],
            "metadata": state["metadata"]
        }
        
        agent_response = send_to_agent.invoke(agent_data)
        return {
            "agent_response": agent_response,
            "workflow_status": "agent_response_received" if agent_response.get("status") != "error" else "error"
        }
    
    return {
        "workflow_status": "error",
        "messages": [HumanMessage(content="Missing team_id or prompt")]
    }

def finalize_mentor_request_node(state: MentorBotState) -> Dict[str, Any]:
    """Node to finalize the mentor request process"""
    if state["agent_response"] and state["agent_response"].get("status") != "error":
        return {
            "messages": [HumanMessage(content=f"Agent response received for team {state['team_id']}")],
            "workflow_status": "completed"
        }
    else:
        error_msg = state["agent_response"].get("message", "Agent request failed")
        return {
            "messages": [HumanMessage(content=f"Agent request failed: {error_msg}")],
            "workflow_status": "failed"
        }

# Create the workflow graph
def create_mentorbot_workflow():
    """Create the MentorBot workflow using LangGraph"""
    # Initialize the graph
    workflow = StateGraph(MentorBotState)
    
    # Add nodes
    workflow.add_node("receive_mentor_request", receive_mentor_request_node)
    workflow.add_node("send_to_agent", send_to_agent_node)
    workflow.add_node("finalize_mentor_request", finalize_mentor_request_node)
    
    # Add edges
    workflow.add_edge("receive_mentor_request", "send_to_agent")
    workflow.add_edge("send_to_agent", "finalize_mentor_request")
    
    # Set entry and finish points
    workflow.set_entry_point("receive_mentor_request")
    workflow.set_finish_point("finalize_mentor_request")
    
    # Compile the workflow without checkpointer to avoid configuration issues
    return workflow.compile()

# Main function to run the workflow
def run_mentorbot_request(mentor_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the MentorBot prompt workflow
    
    Args:
        mentor_data: Dictionary containing team_id, prompt, and optional metadata
        
    Returns:
        Dictionary with workflow result
    """
    # Create the workflow
    app = create_mentorbot_workflow()
    
    # Prepare initial state
    initial_state = {
        "messages": [HumanMessage(content=json.dumps(mentor_data))],
        "team_id": "",
        "prompt": "",
        "metadata": {},
        "agent_response": {},
        "workflow_status": "initialized"
    }
    
    # Run the workflow
    try:
        final_state = app.invoke(initial_state)
        return {
            "status": "success",
            "workflow_status": final_state["workflow_status"],
            "team_id": final_state.get("team_id", ""),
            "agent_response": final_state.get("agent_response", {}),
            "messages": [msg.content for msg in final_state["messages"]]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "workflow_status": "failed"
        }

# Example usage
if __name__ == "__main__":
    # Example mentor request data
    example_data = {
        "team_id": "team_123",
        "prompt": "How do I implement user authentication in my web application?",
        "metadata": {
            "project_type": "web_application",
            "tech_stack": "FastAPI, MongoDB"
        }
    }
    
    # Run the workflow
    result = run_mentorbot_request(example_data)
    print("Workflow Result:")
    print(json.dumps(result, indent=2))