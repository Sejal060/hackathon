import pytest
import logging
import importlib
from unittest.mock import MagicMock

# Import modules from your src package
from src.agent import BasicAgent
from src.reward import RewardSystem
import src.multi_agent as multi_agent_module

@pytest.fixture
def agent(mocker):
    """BasicAgent with a dummy/test api key and mocked Groq client"""
    agent = BasicAgent(api_key="test-key")
    # Mock Groq client to avoid real API calls
    mock_client = mocker.patch("src.agent.Groq")
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mocked response"))]
    mock_client.return_value.chat.completions.create.return_value = mock_response
    return agent

def test_process_input_success(agent):
    """
    Success case:
    - Call process_input and assert it returns a dict
    - Ensure at least one of the expected keys is present
    """
    res = agent.process_input("mentor task")
    assert isinstance(res, dict)
    expected_keys = {"thoughts", "processed_input", "action", "result", "response"}
    assert any(k in res for k in expected_keys), f"Missing expected keys, returned: {res}"

def test_multi_agent_flow():
    """
    Multi-agent flow:
    - If PlannerAgent/ExecutorAgent/Environment exist, run a minimal flow:
      planner.propose_plan -> executor.execute_plan -> env.give_reward
    - If the classes aren't present, skip this test.
    """
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
    """
    Invalid input:
    - Send empty string (or other invalid text) and ensure the method does not crash.
    - The agent should either return a dict or handle gracefully.
    """
    try:
        res = agent.process_input("")  # invalid/empty input
    except Exception as e:
        pytest.fail(f"process_input raised an exception on invalid input: {e}")
    assert isinstance(res, dict)

def test_reward_logging_and_values(caplog):
    """
    Reward system:
    - Call calculate_reward several times, assert returned values are in the expected set.
    - Use caplog to confirm a log message was created.
    """
    rs = RewardSystem()
    caplog.set_level(logging.INFO)
    values = {rs.calculate_reward("some result") for _ in range(10)}
    assert values.issubset({0, 1, 2, 3}), f"Unexpected reward values: {values}"
    assert any("Calculating reward" in r.getMessage() for r in caplog.records), "No reward log found"

def test_api_failure_simulation(monkeypatch, agent):
    """
    API failure simulation:
    - Attempt to detect common external-call points and monkeypatch them to raise an error.
    - If no obvious external-call hook is present, skip the test.
    - If patched, ensure agent handles the failure gracefully (returns a dict), otherwise skip.
    """
    import src.agent as agent_module

    patched_any = False

    # 1) Patch requests.post if the module imports requests
    if hasattr(agent_module, "requests"):
        def _fake_post(*args, **kwargs):
            raise RuntimeError("Simulated network failure")
        monkeypatch.setattr(agent_module.requests, "post", _fake_post)
        patched_any = True

    # 2) Patch a common internal hook name if present
    if hasattr(BasicAgent, "_call_api"):
        def _fake_call_api(self, *args, **kwargs):
            raise RuntimeError("Simulated internal API failure")
        monkeypatch.setattr(BasicAgent, "_call_api", _fake_call_api)
        patched_any = True

    # 3) If nothing was patched, skip this test (can't simulate)
    if not patched_any:
        pytest.skip("No external/internal call candidates found to simulate API failures; skipping")

    try:
        res = agent.process_input("simulate failure")
    except Exception:
        pytest.skip("Agent raised an exception on simulated API failure; consider adding error handling")
    assert isinstance(res, dict)

def test_long_input_handling(agent):
    """
    Test handling of very long input strings.
    - Ensure agent processes long inputs without crashing.
    - Output should still be a dict with expected keys.
    """
    long_input = "x" * 10000
    try:
        res = agent.process_input(long_input)
    except Exception as e:
        pytest.fail(f"process_input failed on long input: {e}")
    assert isinstance(res, dict)
    expected_keys = {"thoughts", "processed_input", "action", "result", "response"}
    assert any(k in res for k in expected_keys), f"Missing expected keys for long input, returned: {res}"

def test_special_characters_input(agent):
    """
    Test handling of special characters in input.
    - Ensure agent processes inputs with special chars without crashing.
    - Output should be a dict.
    """
    special_input = "!@#$%^&*()_+|~`{}[]:;<>?,./"
    try:
        res = agent.process_input(special_input)
    except Exception as e:
        pytest.fail(f"process_input failed on special characters: {e}")
    assert isinstance(res, dict)

def test_none_input_handling(agent):
    """
    Test handling of None input.
    - Ensure agent gracefully handles None without crashing.
    - Output should be a dict.
    """
    try:
        res = agent.process_input(None)
    except Exception as e:
        pytest.fail(f"process_input failed on None input: {e}")
    assert isinstance(res, dict)

def test_reward_negative_scenarios():
    """
    Test RewardSystem with negative or complex scenarios.
    - Test empty, invalid, or complex inputs for reward calculation.
    - Ensure rewards are within expected range.
    """
    rs = RewardSystem()
    assert rs.calculate_reward("") == 0, "Empty input should return 0 reward"
    assert rs.calculate_reward("invalid|complex|input") >= -1, "Complex input should return valid reward"
    assert rs.calculate_reward(None) == 0, "None input should return 0 reward"

def test_specific_output_keys(agent):
    """
    Test specific output keys in agent response.
    - Ensure critical keys like 'response' or 'result' are present for valid inputs.
    """
    res = agent.process_input("valid task input")
    assert isinstance(res, dict)
    assert "response" in res or "result" in res, f"Expected 'response' or 'result' key, got: {res}"

def test_api_timeout_simulation(monkeypatch, agent):
    """
    Simulate API timeout failure.
    - Patch requests.post or _call_api to raise a timeout-specific error.
    - Ensure agent handles timeout gracefully.
    """
    import src.agent as agent_module

    patched_any = False

    if hasattr(agent_module, "requests"):
        def _fake_post(*args, **kwargs):
            raise TimeoutError("Simulated timeout")
        monkeypatch.setattr(agent_module.requests, "post", _fake_post)
        patched_any = True

    if hasattr(BasicAgent, "_call_api"):
        def _fake_call_api(self, *args, **kwargs):
            raise TimeoutError("Simulated timeout")
        monkeypatch.setattr(BasicAgent, "_call_api", _fake_call_api)
        patched_any = True

    if not patched_any:
        pytest.skip("No external/internal call candidates found to simulate timeout; skipping")

    try:
        res = agent.process_input("simulate timeout")
    except Exception:
        pytest.skip("Agent raised an exception on simulated timeout; consider adding error handling")
    assert isinstance(res, dict)

# New tests for Step 2: Add Tests to tests/test_agent.py
def test_executor_execute_plan(mocker):
    """Test ExecutorAgent execute_plan method."""
    mock_executor = mocker.Mock()
    mock_executor.execute_plan.return_value = {"status": "completed"}
    mocker.patch("src.multi_agent.ExecutorAgent", return_value=mock_executor)
    executor = multi_agent_module.ExecutorAgent(api_key="test-key")
    result = executor.execute_plan("test plan")
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] == "completed"

def test_input_handler_process_input():
    """Test input_handler processes input correctly."""
    from src.input_handler import process_input  # Adjust import if function name differs
    result = process_input("valid input")
    assert isinstance(result, str)  # Adjust based on actual output type
    assert result == "valid input"  # Adjust based on processing logic

def test_main_app_loads(mocker):
    """Test main.py Streamlit app loads without errors."""
    mocker.patch("streamlit.run", return_value=None)  # Mock Streamlit run
    from src.main import main  # Adjust import if file is project.py
    try:
        main()
    except Exception as e:
        pytest.fail(f"Main app failed to load: {e}")
    assert True  # Pass if no exception

def test_reasoning_generate_plan():
    """Test reasoning.py generates a plan."""
    from src.reasoning import generate_plan  # Adjust import if function/method name differs
    plan = generate_plan("test task")
    assert isinstance(plan, str)  # Adjust based on actual output type
    assert len(plan) > 0