from pydantic import BaseModel, Field
from typing import List, Optional

class AgentRequest(BaseModel):
    team_id: str = Field(..., examples=["team_42"])
    submission_url: str = Field(..., examples=["https://.../project.zip"])

class RewardRequest(BaseModel):
    team_id: str
    score: float
    feedback: Optional[str] = None

class LogResponse(BaseModel):
    timestamp: str
    message: str
    level: str