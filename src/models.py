# src/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class TeamRegistration(BaseModel):
    team_name: str
    members: List[str]
    project_title: str

class AgentRequest(BaseModel):
    team_id: str
    prompt: str
    metadata: Dict = {}

class RewardRequest(BaseModel):
    request_id: str
    outcome: str

class LogRequest(BaseModel):
    timestamp: str
    level: str
    message: str
    additional_data: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    processed_input: str
    action: str
    result: str
    reward: float
    core_response: Optional[Dict[str, Any]] = None

class RewardResponse(BaseModel):
    reward_value: float
    feedback: str

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str

class JudgeRequest(BaseModel):
    submission_text: str
    team_id: Optional[str] = None

class JudgeResponse(BaseModel):
    clarity: int
    quality: int
    innovation: int
    total_score: float
    confidence: float
    trace: str
    team_id: Optional[str] = None

# Add more as needed