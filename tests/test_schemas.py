import pytest
from src.schemas import AgentRequest, RewardRequest, LogResponse
from src.models import LogEntry

def test_agent_request_creation():
    """Test AgentRequest model creation and validation"""
    # Test valid creation
    agent_request = AgentRequest(
        team_id="team_42",
        prompt="How to build a REST API?"
    )
    
    assert agent_request.team_id == "team_42"
    assert agent_request.prompt == "How to build a REST API?"
    
    # Test validation with missing required fields
    with pytest.raises(ValueError):
        AgentRequest(prompt="test")  # Missing team_id
    
    with pytest.raises(ValueError):
        AgentRequest(team_id="test")  # Missing prompt

def test_reward_request_creation():
    """Test RewardRequest model creation and validation"""
    # Test valid creation
    reward_request = RewardRequest(
        request_id="req_42",
        outcome="success"
    )

    assert reward_request.request_id == "req_42"
    assert reward_request.outcome == "success"

    # Test validation with missing required fields
    with pytest.raises(ValueError):
        RewardRequest(outcome="success")  # Missing request_id

    with pytest.raises(ValueError):
        RewardRequest(request_id="test")  # Missing outcome

def test_log_response_creation():
    """Test LogResponse model creation and validation"""
    # Test valid creation
    log_entry = LogEntry(
        timestamp="2025-01-01T12:00:00Z",
        message="Test log message",
        level="INFO"
    )
    log_response = LogResponse(
        logs=[log_entry],
        count=1
    )

    assert log_response.logs[0].timestamp == "2025-01-01T12:00:00Z"
    assert log_response.logs[0].message == "Test log message"
    assert log_response.logs[0].level == "INFO"
    assert log_response.count == 1

    # Test validation with missing required fields
    with pytest.raises(ValueError):
        LogResponse(logs=[log_entry])  # Missing count

    with pytest.raises(ValueError):
        LogResponse(count=1)  # Missing logs