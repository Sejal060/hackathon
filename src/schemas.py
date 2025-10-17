# src/schemas.py

from pydantic import BaseModel, HttpUrl
from typing import List, Optional


# 👥 Individual team member information
class TeamMember(BaseModel):
    name: str
    email: Optional[str]


# 📝 Team registration schema
class TeamRegistration(BaseModel):
    team_id: str
    team_name: str
    members: List[TeamMember]
    category: str


# 🚀 Project submission schema
class Submission(BaseModel):
    team_id: str
    project_name: str
    github_link: Optional[HttpUrl]
    description: Optional[str]


# 🧠 Result returned by AI agent
class AgentResult(BaseModel):
    team_id: str
    score: float
    feedback: str
    timestamp: str


# 💰 Reward or reinforcement feedback schema
class RewardResponse(BaseModel):
    team_id: str
    reward: float
    reason: Optional[str]
