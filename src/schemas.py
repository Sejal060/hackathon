from pydantic import BaseModel
from typing import List, Optional

class AgentRequest(BaseModel):
    task_id: Optional[str] = None
    agent: str
    input: str
    tags: List[str] = []
    retries: int = 3

class RewardRequest(BaseModel):
    team_id: str
    score: float
    feedback: Optional[str] = None

class LogResponse(BaseModel):
    timestamp: str
    message: str
    level: str
