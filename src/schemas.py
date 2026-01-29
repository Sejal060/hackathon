from pydantic import BaseModel, Field
from typing import List, Optional

class AgentRequest(BaseModel):
    team_id: str = Field(..., examples=["team_42"])
    prompt: str = Field(..., examples=["How to build a REST API?"])  # Changed from submission_url to prompt
    tenant_id: str = "default"
    event_id: str = "default_event"
    workspace_id: Optional[str] = None

class RewardRequest(BaseModel):
    team_id: str
    score: float
    feedback: Optional[str] = None
    tenant_id: str = "default"
    event_id: str = "default_event"
    workspace_id: Optional[str] = None

class LogResponse(BaseModel):
    timestamp: str
    message: str
    level: str