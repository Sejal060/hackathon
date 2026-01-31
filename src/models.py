# src/models.py
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime


def get_current_timestamp():
    """Helper function to get current timestamp as string."""
    return datetime.now().isoformat()


class TeamRegistration(BaseModel):
    """Request model for team registration."""
    team_name: str = Field(..., min_length=1, description="Name of the team (required)")
    members: List[str] = Field(..., min_items=1, description="List of team member names (required, at least 1)")
    project_title: str = Field(..., min_length=1, description="Title of the team's project (required)")
    tenant_id: Optional[str] = Field(default="default", description="Tenant identifier for isolation")
    event_id: Optional[str] = Field(default="default_event", description="Event identifier for isolation")
    workspace_id: Optional[str] = Field(default=None, description="Workspace identifier")

    @validator("members")
    def validate_members_not_empty(cls, v):
        """Ensure all member names are non-empty strings."""
        if not all(isinstance(m, str) and m.strip() for m in v):
            raise ValueError("All member names must be non-empty strings")
        return v


class AgentRequest(BaseModel):
    """Request model for agent processing."""
    team_id: str = Field(..., min_length=1, description="ID of the team making the request (required)")
    prompt: str = Field(..., min_length=1, description="The prompt or query from the team (required)")
    metadata: Dict = Field(default_factory=dict, description="Additional context data")
    tenant_id: Optional[str] = Field(default="default", description="Tenant identifier for isolation")
    event_id: Optional[str] = Field(default="default_event", description="Event identifier for isolation")
    workspace_id: Optional[str] = Field(default=None, description="Workspace identifier")


class RewardRequest(BaseModel):
    """Request model for reward calculation."""
    request_id: str = Field(..., min_length=1, description="ID of the request to apply reward to (required, used for replay protection)")
    outcome: str = Field(..., min_length=1, description="Outcome of the request: success, failure, partial_success, needs_improvement (required)")
    tenant_id: Optional[str] = Field(default="default", description="Tenant identifier for isolation")
    event_id: Optional[str] = Field(default="default_event", description="Event identifier for isolation")
    workspace_id: Optional[str] = Field(default=None, description="Workspace identifier")

    @validator("outcome")
    def validate_outcome(cls, v):
        """Validate outcome is one of the allowed values."""
        allowed = {"success", "failure", "partial_success", "needs_improvement"}
        if v.lower() not in allowed:
            raise ValueError(f"Outcome must be one of: {', '.join(allowed)}")
        return v.lower()


class LogRequest(BaseModel):
    """Request model for log relay."""
    timestamp: str = Field(
        default_factory=get_current_timestamp,
        description="Timestamp of the log entry (ISO format, auto-generated if not provided)"
    )
    level: str = Field(..., min_length=1, description="Log level: INFO, ERROR, WARNING, DEBUG (required)")
    message: str = Field(..., min_length=1, description="Log message (required)")
    additional_data: Optional[Dict[str, Any]] = Field(default=None, description="Optional additional data")
    tenant_id: Optional[str] = Field(default="default", description="Tenant identifier for isolation")
    event_id: Optional[str] = Field(default="default_event", description="Event identifier for isolation")
    workspace_id: Optional[str] = Field(default=None, description="Workspace identifier")

    @validator("level")
    def validate_level(cls, v):
        """Validate level is one of the standard log levels."""
        allowed = {"INFO", "ERROR", "WARNING", "DEBUG", "CRITICAL", "WARN"}
        if v.upper() not in allowed:
            raise ValueError(f"Level must be one of: {', '.join(sorted(allowed))}")
        return v.upper()
    
    @validator("timestamp")
    def validate_timestamp(cls, v):
        """Ensure timestamp is valid, auto-generate if empty."""
        if not v or not str(v).strip():
            return get_current_timestamp()
        return v


class AgentResponse(BaseModel):
    """Response model for agent processing."""
    processed_input: str
    action: str
    result: str
    reward: float
    core_response: Optional[Dict[str, Any]] = None


class RewardResponse(BaseModel):
    """Response model for reward calculation."""
    reward_value: float
    feedback: str


class LogEntry(BaseModel):
    """Single log entry model."""
    timestamp: str
    level: str
    message: str


class LogResponse(BaseModel):
    """Response model for log retrieval."""
    logs: List[LogEntry]
    count: int


class JudgeRequest(BaseModel):
    """Request model for judging submissions."""
    submission_text: str = Field(..., min_length=1, description="The text to evaluate (required)")
    team_id: Optional[str] = Field(default=None, description="Optional team ID for tracking")
    tenant_id: Optional[str] = Field(default="default", description="Tenant identifier for isolation")
    event_id: Optional[str] = Field(default="default_event", description="Event identifier for isolation")
    workspace_id: Optional[str] = Field(default=None, description="Workspace identifier")
    request_id: Optional[str] = Field(default=None, description="Optional request ID for replay protection (if not provided, submission_hash is used)")
    # Internal storage fields
    submission_hash: Optional[str] = Field(default=None, description="Internal: SHA256 hash of submission")

    @validator("submission_text")
    def validate_submission_not_empty(cls, v):
        """Ensure submission text is not just whitespace."""
        if not v.strip():
            raise ValueError("Submission text cannot be empty or whitespace only")
        return v.strip()

class JudgeResponse(BaseModel):
    clarity: int
    quality: int
    innovation: int
    total_score: float
    confidence: float
    trace: str
    team_id: Optional[str] = None
    fallback: Optional[bool] = None
    # Internal storage fields
    version: Optional[int] = None


class BatchSubmissionItem(BaseModel):
    """Single submission item for batch judging."""
    submission_text: str = Field(..., min_length=1, description="The text to evaluate (required)")
    team_id: Optional[str] = Field(default=None, description="Optional team ID for tracking")
    request_id: Optional[str] = Field(default=None, description="Optional request ID for replay protection")

    @validator("submission_text")
    def validate_submission_not_empty(cls, v):
        """Ensure submission text is not just whitespace."""
        if not v.strip():
            raise ValueError("Submission text cannot be empty or whitespace only")
        return v.strip()


class BatchJudgeRequest(BaseModel):
    """Request model for batch judging multiple submissions."""
    submissions: List[BatchSubmissionItem] = Field(..., min_items=1, max_items=100, description="List of submissions to judge (required, 1-100 items)")
    tenant_id: Optional[str] = Field(default="default", description="Tenant identifier for isolation")
    event_id: Optional[str] = Field(default="default_event", description="Event identifier for isolation")
    workspace_id: Optional[str] = Field(default=None, description="Workspace identifier")


class BatchJudgeResult(BaseModel):
    """Result item for batch judging response."""
    team_id: Optional[str] = None
    consensus_score: float
    criteria_scores: Dict[str, int]
    confidence: float
    reasoning_chain: str
    rank: int
    fallback: Optional[bool] = None


class BatchJudgeResponse(BaseModel):
    """Response model for batch judging."""
    results: List[BatchJudgeResult]
    total_count: int
    tenant_id: str
    event_id: str


class RankEntry(BaseModel):
    """Single rank entry for leaderboard."""
    team_id: str
    rank: int
    total_score: float
    clarity: int
    quality: int
    innovation: int
    confidence: float


class RankResponse(BaseModel):
    """Response model for rankings/leaderboard."""
    rankings: List[RankEntry]
    total_count: int
    tenant_id: str
    event_id: str


# Add more as needed