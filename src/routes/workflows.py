#!/usr/bin/env python3
"""
API routes for LangGraph workflows
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import langgraph_workflows
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from langgraph_workflows.workflow_manager import workflow_manager, WorkflowType
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    print(f"Warning: LangGraph workflows not available: {e}")
    LANGGRAPH_AVAILABLE = False

# Import auth
from ..auth import get_api_key

router = APIRouter(prefix="/workflows", tags=["workflows"])

# Pydantic models for request/response
class TeamRegistrationRequest(BaseModel):
    team_name: str
    members: List[str]
    project_title: str

class MentorBotRequest(BaseModel):
    team_id: str
    prompt: str
    metadata: Optional[Dict[str, Any]] = {}

class WorkflowRunRequest(BaseModel):
    name: str
    payload: Optional[Dict[str, Any]] = {}

class WorkflowListResponse(BaseModel):
    workflows: List[str]

class WorkflowResponse(BaseModel):
    status: str
    workflow_type: str
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    timestamp: str

class ExecutionLogResponse(BaseModel):
    execution_log: List[Dict[str, Any]]
    count: int

# Helper function to check if LangGraph is available
def check_langgraph_availability():
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="LangGraph workflows are not available. Please install langgraph package."
        )

@router.post("/team-registration", response_model=WorkflowResponse, summary="Run team registration workflow")
def run_team_registration_workflow(
    request: TeamRegistrationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Run the team registration LangGraph workflow.
    
    - **team_name**: Name of the team
    - **members**: List of team members
    - **project_title**: Title of the team's project
    """
    check_langgraph_availability()
    
    try:
        result = workflow_manager.run_team_registration(request.dict())
        return WorkflowResponse(
            status=result["status"],
            workflow_type=result["workflow_type"],
            message=result.get("message"),
            result=result.get("execution_record", {}).get("result"),
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run team registration workflow: {str(e)}"
        )

@router.post("/mentorbot", response_model=WorkflowResponse, summary="Run MentorBot prompt workflow")
def run_mentorbot_workflow(
    request: MentorBotRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Run the MentorBot prompt LangGraph workflow.
    
    - **team_id**: ID of the team making the request
    - **prompt**: The prompt or query from the team
    - **metadata**: Additional context data (optional)
    """
    check_langgraph_availability()
    
    try:
        result = workflow_manager.run_mentorbot_request(request.dict())
        return WorkflowResponse(
            status=result["status"],
            workflow_type=result["workflow_type"],
            message=result.get("message"),
            result=result.get("execution_record", {}).get("result"),
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run MentorBot workflow: {str(e)}"
        )

@router.post("/judging-reminder", response_model=WorkflowResponse, summary="Run judging reminder workflow")
def run_judging_reminder_workflow(
    api_key: str = Depends(get_api_key)
):
    """
    Run the judging reminder LangGraph workflow.
    """
    check_langgraph_availability()
    
    try:
        result = workflow_manager.run_judging_reminder()
        return WorkflowResponse(
            status=result["status"],
            workflow_type=result["workflow_type"],
            message=result.get("message"),
            result=result.get("execution_record", {}).get("result"),
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run judging reminder workflow: {str(e)}"
        )

@router.post("/run", response_model=WorkflowResponse, summary="Run workflow by name")
def run_workflow(
    request: WorkflowRunRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Run a workflow by name.
    
    - **name**: Name of the workflow to run ("judge", "mentor", etc.)
    - **payload**: Data to pass to the workflow (optional)
    """
    check_langgraph_availability()
    
    try:
        result = workflow_manager.run_workflow_by_name(request.name, request.payload)
        return WorkflowResponse(
            status=result["status"],
            workflow_type=result.get("workflow_type", "unknown"),
            message=result.get("message"),
            result=result.get("execution_record", {}).get("result") if "execution_record" in result else result.get("result"),
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run workflow: {str(e)}"
        )

@router.get("/list", response_model=WorkflowListResponse, summary="List available workflows")
def list_workflows(
    api_key: str = Depends(get_api_key)
):
    """
    List all available workflows.
    """
    check_langgraph_availability()
    
    workflows = ["judge", "mentor", "team_registration"]
    return WorkflowListResponse(workflows=workflows)

@router.get("/execution-log", response_model=ExecutionLogResponse, summary="Get workflow execution log")
def get_workflow_execution_log(
    api_key: str = Depends(get_api_key)
):
    """
    Get the execution log of all workflows.
    """
    check_langgraph_availability()
    
    try:
        log = workflow_manager.get_execution_log()
        return ExecutionLogResponse(
            execution_log=log,
            count=len(log)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve execution log: {str(e)}"
        )

@router.delete("/execution-log", response_model=WorkflowResponse, summary="Clear workflow execution log")
def clear_workflow_execution_log(
    api_key: str = Depends(get_api_key)
):
    """
    Clear the workflow execution log.
    """
    check_langgraph_availability()
    
    try:
        result = workflow_manager.clear_execution_log()
        return WorkflowResponse(
            status=result["status"],
            workflow_type="log_management",
            message=result["message"],
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear execution log: {str(e)}"
        )

@router.get("/health", response_model=WorkflowResponse, summary="Check workflow system health")
def workflow_health_check():
    """
    Check the health of the workflow system.
    """
    status = "success" if LANGGRAPH_AVAILABLE else "warning"
    message = "LangGraph workflows are available" if LANGGRAPH_AVAILABLE else "LangGraph workflows are not available"
    
    return WorkflowResponse(
        status=status,
        workflow_type="health_check",
        message=message,
        timestamp=datetime.now().isoformat()
    )