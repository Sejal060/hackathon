import pytest
from src.schemas import AgentRequest, RewardRequest, LogResponse

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
        team_id="team_42",
        score=3.5,
        feedback="Good work!"
    )
    
    assert reward_request.team_id == "team_42"
    assert reward_request.score == 3.5
    assert reward_request.feedback == "Good work!"
    
    # Test creation without optional feedback
    reward_request_no_feedback = RewardRequest(
        team_id="team_42",
        score=3.5
    )
    
    assert reward_request_no_feedback.team_id == "team_42"
    assert reward_request_no_feedback.score == 3.5
    assert reward_request_no_feedback.feedback is None
    
    # Test validation with missing required fields
    with pytest.raises(ValueError):
        RewardRequest(score=3.5)  # Missing team_id
    
    with pytest.raises(ValueError):
        RewardRequest(team_id="test")  # Missing score

def test_log_response_creation():
    """Test LogResponse model creation and validation"""
    # Test valid creation
    log_response = LogResponse(
        timestamp="2025-01-01T12:00:00Z",
        message="Test log message",
        level="INFO"
    )
    
    assert log_response.timestamp == "2025-01-01T12:00:00Z"
    assert log_response.message == "Test log message"
    assert log_response.level == "INFO"
    
    # Test validation with missing required fields
    with pytest.raises(ValueError):
        LogResponse(message="test", level="INFO")  # Missing timestamp
    
    with pytest.raises(ValueError):
        LogResponse(timestamp="2025-01-01T12:00:00Z", level="INFO")  # Missing message
        
    with pytest.raises(ValueError):
        LogResponse(timestamp="2025-01-01T12:00:00Z", message="test")  # Missing level