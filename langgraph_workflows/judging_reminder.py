#!/usr/bin/env python3
"""
LangGraph implementation for judging reminder workflow
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define the state structure for our workflow
class JudgingReminderState(MessagesState):
    """State for judging reminder workflow"""
    submissions: List[Dict[str, Any]]
    judge_emails: List[str]
    notification_sent: bool
    workflow_status: str
    last_check_time: str

# Define tools for the workflow
@tool
def get_submissions() -> List[Dict[str, Any]]:
    """Simulate getting submissions from the backend"""
    # Simulate some submissions
    return [
        {
            "id": "sub_1",
            "team_name": "Innovators",
            "project_title": "AI Assistant",
            "submitted_at": "2025-11-27T10:00:00Z"
        },
        {
            "id": "sub_2",
            "team_name": "Creators",
            "project_title": "Blockchain Solution",
            "submitted_at": "2025-11-27T11:00:00Z"
        }
    ]

@tool
def send_judge_notification(judge_emails: List[str], submissions_count: int) -> Dict[str, Any]:
    """Simulate sending notification to judges about new submissions"""
    try:
        return {
            "status": "success",
            "message": f"Notification sent to {len(judge_emails)} judges about {submissions_count} submissions",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send notification: {str(e)}"
        }

# Define nodes for the workflow
def check_submissions_node(state: JudgingReminderState) -> Dict[str, Any]:
    """Node to check for new submissions"""
    submissions = get_submissions.invoke({})
    
    return {
        "submissions": submissions,
        "last_check_time": datetime.now().isoformat(),
        "workflow_status": "submissions_checked"
    }

def notify_judges_node(state: JudgingReminderState) -> Dict[str, Any]:
    """Node to notify judges if there are new submissions"""
    if state["submissions"]:
        # Get judge emails from environment or use defaults
        judge_emails = os.getenv("JUDGE_EMAILS", "judges@example.com").split(",")
        judge_emails = [email.strip() for email in judge_emails]
        
        notification_result = send_judge_notification.invoke({
            "judge_emails": judge_emails,
            "submissions_count": len(state["submissions"])
        })
        
        return {
            "judge_emails": judge_emails,
            "notification_sent": notification_result["status"] == "success",
            "workflow_status": "judges_notified" if notification_result["status"] == "success" else "notification_failed",
            "messages": [HumanMessage(content=notification_result["message"])]
        }
    else:
        return {
            "notification_sent": False,
            "workflow_status": "no_submissions",
            "messages": [HumanMessage(content="No new submissions to review")]
        }

def finalize_reminder_node(state: JudgingReminderState) -> Dict[str, Any]:
    """Node to finalize the reminder process"""
    if state["notification_sent"]:
        return {
            "messages": [HumanMessage(content=f"Judges notified about {len(state['submissions'])} submissions")],
            "workflow_status": "completed"
        }
    else:
        return {
            "messages": [HumanMessage(content="No notifications sent")],
            "workflow_status": "completed_no_action"
        }

# Create the workflow graph
def create_judging_reminder_workflow():
    """Create the judging reminder workflow using LangGraph"""
    # Initialize the graph
    workflow = StateGraph(JudgingReminderState)
    
    # Add nodes
    workflow.add_node("check_submissions", check_submissions_node)
    workflow.add_node("notify_judges", notify_judges_node)
    workflow.add_node("finalize_reminder", finalize_reminder_node)
    
    # Add edges
    workflow.add_edge("check_submissions", "notify_judges")
    workflow.add_edge("notify_judges", "finalize_reminder")
    
    # Set entry and finish points
    workflow.set_entry_point("check_submissions")
    workflow.set_finish_point("finalize_reminder")
    
    # Compile the workflow without checkpointer to avoid configuration issues
    return workflow.compile()

# Main function to run the workflow
def run_judging_reminder() -> Dict[str, Any]:
    """
    Run the judging reminder workflow
    
    Returns:
        Dictionary with workflow result
    """
    # Create the workflow
    app = create_judging_reminder_workflow()
    
    # Prepare initial state
    initial_state = {
        "messages": [HumanMessage(content="Starting judging reminder workflow")],
        "submissions": [],
        "judge_emails": [],
        "notification_sent": False,
        "workflow_status": "initialized",
        "last_check_time": ""
    }
    
    # Run the workflow
    try:
        final_state = app.invoke(initial_state)
        return {
            "status": "success",
            "workflow_status": final_state["workflow_status"],
            "submissions_count": len(final_state.get("submissions", [])),
            "notification_sent": final_state.get("notification_sent", False),
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
    # Run the workflow
    result = run_judging_reminder()
    print("Workflow Result:")
    print(json.dumps(result, indent=2))