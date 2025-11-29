#!/usr/bin/env python3
"""
Workflow Manager for LangGraph workflows
Centralized management of all automation workflows
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
import time
from enum import Enum

# Import workflow modules
from .team_registration import run_team_registration
from .judging_reminder import run_judging_reminder
from .mentorbot_prompt import run_mentorbot_request

class WorkflowType(Enum):
    """Enumeration of supported workflow types"""
    TEAM_REGISTRATION = "team_registration"
    JUDGING_REMINDER = "judging_reminder"
    MENTORBOT_PROMPT = "mentorbot_prompt"

class WorkflowManager:
    """Centralized manager for all LangGraph workflows"""
    
    def __init__(self):
        """Initialize the workflow manager"""
        self.workflows = {
            WorkflowType.TEAM_REGISTRATION: run_team_registration,
            WorkflowType.JUDGING_REMINDER: run_judging_reminder,
            WorkflowType.MENTORBOT_PROMPT: run_mentorbot_request
        }
        self.execution_log = []
    
    def run_workflow(self, workflow_type: WorkflowType, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run a specific workflow
        
        Args:
            workflow_type: Type of workflow to run
            data: Data to pass to the workflow
            
        Returns:
            Dictionary with workflow result
        """
        if workflow_type not in self.workflows:
            return {
                "status": "error",
                "message": f"Unsupported workflow type: {workflow_type}",
                "workflow_type": workflow_type.value,
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            # Run the workflow
            start_time = time.time()
            
            # Pass data only if it's provided and the workflow expects it
            if data is None:
                result = self.workflows[workflow_type]()
            else:
                result = self.workflows[workflow_type](data)
                
            end_time = time.time()
            
            # Log the execution
            execution_record = {
                "workflow_type": workflow_type.value,
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "end_time": datetime.fromtimestamp(end_time).isoformat(),
                "duration": end_time - start_time,
                "status": result.get("status", "unknown"),
                "result": result
            }
            self.execution_log.append(execution_record)
            
            return {
                "status": "success",
                "workflow_type": workflow_type.value,
                "execution_record": execution_record,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_record = {
                "workflow_type": workflow_type.value,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.execution_log.append(error_record)
            
            return {
                "status": "error",
                "message": str(e),
                "workflow_type": workflow_type.value,
                "error_record": error_record,
                "timestamp": datetime.now().isoformat()
            }
    
    def run_team_registration(self, registration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the team registration workflow
        
        Args:
            registration_data: Dictionary containing team_name, members, and project_title
            
        Returns:
            Dictionary with workflow result
        """
        return self.run_workflow(WorkflowType.TEAM_REGISTRATION, registration_data)
    
    def run_judging_reminder(self) -> Dict[str, Any]:
        """
        Run the judging reminder workflow
        
        Returns:
            Dictionary with workflow result
        """
        return self.run_workflow(WorkflowType.JUDGING_REMINDER)
    
    def run_mentorbot_request(self, mentor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the MentorBot prompt workflow
        
        Args:
            mentor_data: Dictionary containing team_id, prompt, and optional metadata
            
        Returns:
            Dictionary with workflow result
        """
        return self.run_workflow(WorkflowType.MENTORBOT_PROMPT, mentor_data)
    
    def run_workflow_by_name(self, name: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Unified function to run a workflow by name
        
        Args:
            name: Name of the workflow to run ("judge", "mentor", etc.)
            payload: Data to pass to the workflow
            
        Returns:
            Dictionary with workflow result
        """
        workflow_mapping = {
            "judge": WorkflowType.JUDGING_REMINDER,
            "mentor": WorkflowType.MENTORBOT_PROMPT,
            "team_registration": WorkflowType.TEAM_REGISTRATION
        }
        
        if name not in workflow_mapping:
            return {
                "status": "error",
                "message": f"Unsupported workflow name: {name}",
                "timestamp": datetime.now().isoformat()
            }
        
        workflow_type = workflow_mapping[name]
        return self.run_workflow(workflow_type, payload)
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """
        Get the execution log of all workflows
        
        Returns:
            List of execution records
        """
        return self.execution_log.copy()
    
    def clear_execution_log(self) -> Dict[str, Any]:
        """
        Clear the execution log
        
        Returns:
            Dictionary with confirmation
        """
        log_count = len(self.execution_log)
        self.execution_log.clear()
        return {
            "status": "success",
            "message": f"Cleared {log_count} execution records",
            "timestamp": datetime.now().isoformat()
        }

# Global instance for convenience
workflow_manager = WorkflowManager()

# Example usage
if __name__ == "__main__":
    # Create workflow manager
    manager = WorkflowManager()
    
    # Example 1: Team registration
    print("=== Team Registration Workflow ===")
    registration_data = {
        "team_name": "AI Innovators",
        "members": ["Alice Smith", "Bob Johnson", "Charlie Brown"],
        "project_title": "AI-Powered Hackathon Management System"
    }
    
    result = manager.run_team_registration(registration_data)
    print(json.dumps(result, indent=2))
    
    # Example 2: MentorBot request
    print("\n=== MentorBot Prompt Workflow ===")
    mentor_data = {
        "team_id": "team_123",
        "prompt": "How do I implement user authentication in my web application?",
        "metadata": {
            "project_type": "web_application",
            "tech_stack": "FastAPI, MongoDB"
        }
    }
    
    result = manager.run_mentorbot_request(mentor_data)
    print(json.dumps(result, indent=2))
    
    # Example 3: Judging reminder
    print("\n=== Judging Reminder Workflow ===")
    result = manager.run_judging_reminder()
    print(json.dumps(result, indent=2))
    
    # Example 4: Run workflow by name
    print("\n=== Run Workflow by Name (Judge) ===")
    result = manager.run_workflow_by_name("judge")
    print(json.dumps(result, indent=2))
    
    # Show execution log
    print("\n=== Execution Log ===")
    log = manager.get_execution_log()
    print(json.dumps(log, indent=2))