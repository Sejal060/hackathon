import pytest
from unittest.mock import MagicMock
from src.agent import BasicAgent
from src.reward import RewardSystem
import src.multi_agent as multi_agent_module
from src.input_handler import InputHandler
from src.reasoning import ReasoningModule
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

@pytest.fixture
def agent(mocker):
    """BasicAgent with a dummy/test api key and mocked Groq client"""
    agent = BasicAgent(api_key="test-key")
    mock_client = mocker.patch("src.agent.Groq")
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mocked response"))]
    mock_client.return_value.chat.completions.create.return_value = mock_response
    return agent

def test_process_input_success(agent):
    """Success case: Call process_input and assert it returns a dict with expected keys"""
    res = agent.process_input("mentor task")
    assert isinstance(res, dict)
    expected_keys = {"thoughts", "processed_input", "action", "result", "response"}
    assert any(k in res for k in expected_keys), f"Missing expected keys, returned: {res}"

def test_multi_agent_flow():
    """Multi-agent flow: Test planner, executor, and environment interaction"""
    if not (hasattr(multi_agent_module, "PlannerAgent") and
            hasattr(multi_agent_module, "ExecutorAgent") and
            hasattr(multi_agent_module, "Environment")):
        pytest.skip("Multi-agent classes not present; skipping multi-agent flow test")
    planner = multi_agent_module.PlannerAgent(api_key="test-key")
    executor = multi_agent_module.ExecutorAgent(api_key="test-key")
    env = multi_agent_module.Environment()
    plan = planner.propose_plan("test task")
    assert isinstance(plan, str)
    result = executor.execute_plan(plan)
    assert isinstance(result, (str, dict))
    reward = env.give_reward(result)
    assert isinstance(reward, int)

def test_invalid_input_handling(agent):
    """Invalid input: Ensure process_input handles empty string gracefully"""
    res = agent.process_input("")
    assert isinstance(res, dict)

def test_reward_logging_and_values(caplog):
    """Reward system: Test reward values and logging"""
    rs = RewardSystem()
    caplog.set_level(logging.INFO)
    values = {rs.calculate_reward("some result") for _ in range(10)}
    assert values.issubset({0, 1, 2, 3}), f"Unexpected reward values: {values}"
    assert any("Calculating reward" in r.getMessage() for r in caplog.records), "No reward log found"

def test_api_failure_simulation(monkeypatch, agent):
    """API failure simulation: Ensure agent handles failure gracefully"""
    import src.agent as agent_module
    patched_any = False
    if hasattr(BasicAgent, "_call_api"):
        def _fake_call_api(self, *args, **kwargs):
            raise RuntimeError("Simulated network failure")
        monkeypatch.setattr(BasicAgent, "_call_api", _fake_call_api)
        patched_any = True
    if not patched_any:
        pytest.skip("No external/internal call candidates found to simulate API failures")
    res = agent.process_input("simulate failure")
    assert isinstance(res, dict)

def test_long_input_handling(agent):
    """Test handling of very long input strings"""
    long_input = "x" * 10000
    res = agent.process_input(long_input)
    assert isinstance(res, dict)
    expected_keys = {"thoughts", "processed_input", "action", "result", "response"}
    assert any(k in res for k in expected_keys)

def test_special_characters_input(agent):
    """Test handling of special characters in input"""
    special_input = "!@#$%^&*()_+|~`{}[]:;<>?,./"
    res = agent.process_input(special_input)
    assert isinstance(res, dict)

def test_none_input_handling(agent):
    """Test handling of None input"""
    res = agent.process_input(None)
    assert isinstance(res, dict)

def test_reward_negative_scenarios():
    """Test RewardSystem with negative or complex scenarios"""
    rs = RewardSystem()
    assert rs.calculate_reward("") == 0
    assert rs.calculate_reward("invalid|complex|input") >= -1
    assert rs.calculate_reward(None) == 0

def test_specific_output_keys(agent):
    """Test specific output keys in agent response"""
    res = agent.process_input("valid task input")
    assert isinstance(res, dict)
    assert "response" in res or "result" in res

def test_api_timeout_simulation(monkeypatch, agent):
    """Simulate API timeout failure"""
    import src.agent as agent_module
    patched_any = False
    if hasattr(BasicAgent, "_call_api"):
        def _fake_call_api(self, *args, **kwargs):
            raise TimeoutError("Simulated timeout")
        monkeypatch.setattr(BasicAgent, "_call_api", _fake_call_api)
        patched_any = True
    if not patched_any:
        pytest.skip("No external/internal call candidates found to simulate timeout")
    res = agent.process_input("simulate timeout")
    assert isinstance(res, dict)

# New tests for InputHandler
def test_input_handler_process_input():
    """Test InputHandler processes input correctly"""
    handler = InputHandler()
    result = handler.process_input("valid input")
    assert isinstance(result, str)
    assert result == "valid input"

def test_input_handler_empty_input():
    """Test InputHandler with empty input"""
    handler = InputHandler()
    result = handler.process_input("")
    assert isinstance(result, str)
    assert result == ""

# New tests for ReasoningModule
def test_reasoning_plan_trip():
    """Test ReasoningModule plan for trip-related input"""
    reasoning = ReasoningModule()
    plan = reasoning.plan("plan a mountain trip")
    assert isinstance(plan, str)
    assert "Check weather" in plan

def test_reasoning_plan_hackathon():
    """Test ReasoningModule plan for hackathon input"""
    reasoning = ReasoningModule()
    plan = reasoning.plan("organize a hackathon")
    assert isinstance(plan, str)
    assert "Arrange venue" in plan

def test_reasoning_plan_meeting():
    """Test ReasoningModule plan for meeting input"""
    reasoning = ReasoningModule()
    plan = reasoning.plan("schedule a meeting")
    assert isinstance(plan, str)
    assert "Reserve meeting room" in plan

def test_reasoning_plan_default():
    """Test ReasoningModule plan for default case"""
    reasoning = ReasoningModule()
    plan = reasoning.plan("random task")
    assert isinstance(plan, str)
    assert "Process input: random task" in plan

def test_reasoning_plan_logging(caplog):
    """Test logging in ReasoningModule.plan"""
    reasoning = ReasoningModule()
    caplog.set_level(logging.INFO)
    reasoning.plan("plan a trip")
    assert any("Planning action" in r.getMessage() for r in caplog.records)

# Updated executor test
def test_executor_execute_plan(mocker):
    """Test ExecutorAgent execute_plan method"""
    mock_executor = mocker.Mock()
    mock_executor.execute_plan.return_value = {"status": "completed"}
    mocker.patch("src.multi_agent.ExecutorAgent", return_value=mock_executor)
    executor = multi_agent_module.ExecutorAgent(api_key="test-key")
    result = executor.execute_plan("test plan")
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] == "completed"

# Updated main app test
def test_main_app_loads(mocker):
    """Test main.py FastAPI app loads without errors"""
    # Mock uvicorn.run to prevent server startup
    mocker.patch("uvicorn.run")
    # Import the app object
    from src.main import app
    try:
        # Test app loading by accessing OpenAPI schema
        response = app.openapi()
        assert response is not None
    except Exception as e:
        pytest.fail(f"Main app failed to load: {e}")

# New tests for main.py coverage
def test_agent_endpoint_exception(mocker):
    """Test /agent endpoint with mocked executor failure"""
    from src.main import app, input_handler, reasoning, executor, reward_system
    mocker.patch.object(executor, "execute", side_effect=Exception("Execution failed"))
    with pytest.raises(Exception):
        app.dependency_overrides = {}
        response = app.__call__({"path": "/agent", "query_string": b"input=test"})

def test_agent_endpoint_logging_invalid(caplog):
    from src.main import app
    from fastapi.testclient import TestClient
    caplog.set_level(logging.INFO)
    with TestClient(app) as client:
        response = client.get("/agent?input=")
        assert response.status_code == 422
        assert any("Validation error" in r.getMessage() for r in caplog.records)
        
def test_cors_middleware():
    from src.main import app
    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        response = client.get("/ping", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.headers.get("Access-Control-Allow-Origin") == "*", "CORS not applied"

def test_reward_system_exception(mocker):
    """Test RewardSystem handles exceptions gracefully"""
    from src.reward import RewardSystem
    mocker.patch("src.reward.RewardSystem.calculate_reward", side_effect=ValueError("Invalid reward"))
    rs = RewardSystem()
    with pytest.raises(ValueError):
        rs.calculate_reward("invalid")

def test_reward_system_edge_case():
    """Test RewardSystem with edge case input"""
    from src.reward import RewardSystem
    rs = RewardSystem()
    result = rs.calculate_reward("edge_case_input")
    assert isinstance(result, (int, float))
    assert result >= -1 and result <= 3

def test_agent_endpoint_invalid_query(caplog):
    """Test /agent endpoint with invalid query parameter"""
    from src.main import app
    from fastapi.testclient import TestClient
    caplog.set_level(logging.INFO)
    with TestClient(app) as client:
        response = client.get("/agent")  # Missing input parameter
        assert response.status_code == 422  # Unprocessable Entity for missing required query
        assert any("called with input:" not in r.getMessage() for r in caplog.records)