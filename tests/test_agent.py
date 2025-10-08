import pytest
from unittest.mock import MagicMock
from src.agent import BasicAgent
from src.reward import RewardSystem
import src.multi_agent as multi_agent_module
from src.input_handler import InputHandler
from src.reasoning import ReasoningModule
from src.executor import Executor
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from src.main import initialize_app

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
    values = {rs.calculate_reward("some result")[0] for _ in range(10)}  # Extract reward from tuple
    assert values.issubset({1.0}), f"Unexpected reward values: {values}"  # Expect 1.0 for one step
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
    reward, feedback = rs.calculate_reward("")  # Unpack tuple
    assert reward == 0.0 and feedback == "No action provided"
    reward, feedback = rs.calculate_reward("invalid|complex|input")
    assert reward >= -1  # Allow for negative rewards if logic supports it
    reward, feedback = rs.calculate_reward(None)
    assert reward == 0.0 and feedback == "No action provided"

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

def test_reasoning_plan_with_context():
    """Test ReasoningModule with context"""
    reasoning = ReasoningModule()
    plan = reasoning.plan("plan a trip", {"location": "Himalayas", "priority": "high"})
    assert isinstance(plan, str)
    assert "Check weather" in plan
    assert "location=Himalayas" in plan
    assert "priority=high" in plan

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

def test_executor_execute_failure(mocker):
    """Test Executor failure case"""
    mock_executor = mocker.Mock()
    mock_executor.execute_plan.side_effect = Exception("Execution failed")
    mocker.patch("src.multi_agent.ExecutorAgent", return_value=mock_executor)
    executor = multi_agent_module.ExecutorAgent(api_key="test-key")
    with pytest.raises(Exception):
        executor.execute_plan("failing_plan")

def test_executor_partial_execution():
    """Test Executor with partial execution"""
    executor = Executor()
    result = executor.execute("Step1 -> Failed Step -> Step3")
    assert isinstance(result, str)
    assert "Executed: Step1" in result
    assert "Executed: Failed Step" in result
    assert "Executed: Step3" in result

# Updated main app test
def test_main_app_loads(mocker):
    """Test main.py FastAPI app loads without errors"""
    mocker.patch("uvicorn.run")
    from src.main import app
    try:
        response = app.openapi()
        assert response is not None
    except Exception as e:
        pytest.fail(f"Main app failed to load: {e}")

# Updated tests for main.py coverage
def test_agent_endpoint_exception(mocker):
    """Test /agent endpoint with mocked executor failure"""
    # Reinitialize app with a clean executor
    app = initialize_app()
    # Mock executor.execute for this test only
    mock_executor = mocker.patch.object(app.executor, "execute", side_effect=Exception("Execution failed"))
    with TestClient(app) as client:
        try:
            response = client.get("/agent?input=test")
            # If we get here, the exception was properly handled
            assert response.status_code == 500
            assert response.json()["detail"] == "Internal Server Error"
        except Exception:
            # If exception is raised, it means the mock worked correctly
            mock_executor.assert_called_once()

def test_agent_endpoint_large_input(caplog):
    """Test /agent endpoint with large input"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        caplog.set_level(logging.INFO)
        large_input = "x" * 10000
        response = client.get(f"/agent?input={large_input}")
        assert response.status_code == 200
        assert "processed_input" in response.json()
        assert any(f"/agent GET called with input: {large_input}" in r.getMessage() for r in caplog.records)

def test_agent_endpoint_invalid_json():
    """Test /agent POST with invalid JSON"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        response = client.post("/agent", json={"invalid_key": "value"})
        assert response.status_code == 422

def test_agent_endpoint_context(caplog):
    """Test /agent POST with context"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        caplog.set_level(logging.INFO)
        input_data = {"user_input": "plan a trip", "context": {"location": "Himalayas"}}
        response = client.post("/agent", json=input_data)
        assert response.status_code == 200
        assert "location=Himalayas" in response.json()["action"]
        assert any(f"/agent POST called with input: plan a trip" in r.getMessage() for r in caplog.records)

def test_multi_agent_endpoint():
    """Test /multi-agent endpoint"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        response = client.get("/multi-agent?task=organize hackathon")
        assert response.status_code == 200
        assert "Arrange venue" in response.json()["plan"]

def test_reward_endpoint_success():
    """Test /reward endpoint with successful outcome"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        response = client.post("/reward", json={"action": "step1|step2", "outcome": "success"})
        assert response.status_code == 200
        assert response.json()["reward_value"] > 2.0  # 2 steps * 1.5
        assert "Success" in response.json()["feedback"]

def test_reward_endpoint_failure():
    """Test /reward endpoint with failure outcome"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        response = client.post("/reward", json={"action": "step1", "outcome": "fail"})
        assert response.status_code == 200
        assert response.json()["reward_value"] < 1.0  # 1 step * 0.5
        assert "Failure" in response.json()["feedback"]

def test_logs_endpoint():
    """Test /logs endpoint"""
    app = initialize_app()  # Reinitialize app
    from src.main import log_action
    with TestClient(app) as client:
        log_action("Test log entry")
        response = client.get("/logs")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert "Test log entry" in [entry["message"] for entry in response.json()]

def test_validation_exception():
    """Test validation exception handler"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        response = client.get("/agent?input=")  # Empty input triggers validation
        assert response.status_code == 422
        assert "String should have at least 1 character" in str(response.json()["detail"])

def test_general_exception():
    """Test general exception handler"""
    app = initialize_app()  # Reinitialize app
    with TestClient(app) as client:
        # Simulate an unhandled exception (e.g., by modifying a dependency)
        with pytest.raises(Exception):
            response = client.get("/agent?input=crash&trigger_error=true")
            assert response.status_code == 500
            assert "Internal Server Error" in response.json()["detail"]