#!/usr/bin/env python3
"""
LangGraph implementation for team registration workflow
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
class TeamRegistrationState(MessagesState):
    """State for team registration workflow"""
    team_name: str
    members: List[str]
    project_title: str
    registration_data: Dict[str, Any]
    backend_response: Dict[str, Any]
    workflow_status: str

# Define tools for the workflow
@tool
def receive_registration_data(team_name: str, members: List[str], project_title: str) -> Dict[str, Any]:
    """Receive and validate team registration data"""
    return {
        "team_name": team_name,
        "members": members,
        "project_title": project_title,
        "timestamp": datetime.now().isoformat()
    }

@tool
def send_to_backend(registration_data: dict) -> Dict[str, Any]:
    """Simulate sending registration data to the backend API"""
    try:
        # Simulate successful backend response
        return {
            "status": "success",
            "message": "Team registered successfully",
            "team_id": f"team_{int(time.time())}",
            "registration_data": registration_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to register team: {str(e)}"
        }

# Define nodes for the workflow
def receive_registration_node(state: TeamRegistrationState) -> Dict[str, Any]:
    """Node to receive and validate registration data"""
    # Extract data from the last message (assuming it contains the registration data)
    if state["messages"]:
        last_message = state["messages"][-1]
        if hasattr(last_message, 'content'):
            try:
                registration_data = json.loads(last_message.content)
                validated_data = receive_registration_data.invoke(registration_data)
                return {
                    "team_name": validated_data["team_name"],
                    "members": validated_data["members"],
                    "project_title": validated_data["project_title"],
                    "registration_data": validated_data,
                    "workflow_status": "data_received"
                }
            except json.JSONDecodeError:
                return {
                    "workflow_status": "error",
                    "messages": [HumanMessage(content="Invalid JSON data received")]
                }
    
    return {
        "workflow_status": "waiting_for_data",
        "messages": [HumanMessage(content="Waiting for registration data")]
    }

def send_to_backend_node(state: TeamRegistrationState) -> Dict[str, Any]:
    """Node to send data to backend"""
    if state["registration_data"]:
        backend_response = send_to_backend.invoke(state["registration_data"])
        return {
            "backend_response": backend_response,
            "workflow_status": "completed" if backend_response.get("status") != "error" else "error"
        }
    
    return {
        "workflow_status": "error",
        "messages": [HumanMessage(content="No registration data to send")]
    }

def finalize_registration_node(state: TeamRegistrationState) -> Dict[str, Any]:
    """Node to finalize the registration process"""
    if state["backend_response"] and state["backend_response"].get("status") != "error":
        return {
            "messages": [HumanMessage(content=f"Team {state['team_name']} registered successfully")],
            "workflow_status": "finalized"
        }
    else:
        error_msg = state["backend_response"].get("message", "Registration failed")
        return {
            "messages": [HumanMessage(content=f"Registration failed: {error_msg}")],
            "workflow_status": "failed"
        }

# Create the workflow graph
def create_team_registration_workflow():
    """Create the team registration workflow using LangGraph"""
    # Initialize the graph
    workflow = StateGraph(TeamRegistrationState)
    
    # Add nodes
    workflow.add_node("receive_registration", receive_registration_node)
    workflow.add_node("send_to_backend", send_to_backend_node)
    workflow.add_node("finalize_registration", finalize_registration_node)
    
    # Add edges
    workflow.add_edge("receive_registration", "send_to_backend")
    workflow.add_edge("send_to_backend", "finalize_registration")
    
    # Set entry and finish points
    workflow.set_entry_point("receive_registration")
    workflow.set_finish_point("finalize_registration")
    
    # Compile the workflow without checkpointer to avoid configuration issues
    return workflow.compile()

# Main function to run the workflow
def run_team_registration(registration_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the team registration workflow
    
    Args:
        registration_data: Dictionary containing team_name, members, and project_title
        
    Returns:
        Dictionary with workflow result
    """
    # Create the workflow
    app = create_team_registration_workflow()
    
    # Prepare initial state
    initial_state = {
        "messages": [HumanMessage(content=json.dumps(registration_data))],
        "team_name": "",
        "members": [],
        "project_title": "",
        "registration_data": {},
        "backend_response": {},
        "workflow_status": "initialized"
    }
    
    # Run the workflow
    try:
        final_state = app.invoke(initial_state)
        return {
            "status": "success",
            "workflow_status": final_state["workflow_status"],
            "team_name": final_state.get("team_name", ""),
            "backend_response": final_state.get("backend_response", {}),
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
    # Example registration data
    example_data = {
        "team_name": "AI Innovators",
        "members": ["Alice Smith", "Bob Johnson", "Charlie Brown"],
        "project_title": "AI-Powered Hackathon Management System"
    }
    
    # Run the workflow
    result = run_team_registration(example_data)
    print("Workflow Result:")
    print(json.dumps(result, indent=2))