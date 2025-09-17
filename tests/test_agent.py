import sys
import os
sys.path.insert(0, os.path.abspath('src'))  # Add src to Python path for imports

import pytest
import logging
from unittest.mock import patch, Mock

# Now import modules
from agent import BasicAgent  # Relative import after path fix
from reward import RewardSystem
import multi_agent as multi_agent_module
from data_manager import DataManager

@pytest.fixture
def agent():
    """BasicAgent with a dummy/test api key"""
    return BasicAgent(api_key="test-key")

@pytest.fixture
def data_manager():
    """DataManager fixture for testing"""
    return DataManager()

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
    - Test edge case with invalid plan input.
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

    # Edge case: Invalid plan
    invalid_result = executor.execute_plan("")
    assert isinstance(invalid_result, (str, dict))  # Should not crash

def test_invalid_input_handling(agent):
    """
    Invalid input:
    - Send empty string and special characters, ensure no crash.
    - Verify graceful handling with error message or default response.
    """
    try:
        res = agent.process_input("")  # Empty input
        assert isinstance(res, dict)
        assert "error" in res.get("action", "").lower() or "invalid" in res.get("result", "").lower()
    except Exception as e:
        pytest.fail(f"process_input raised an exception on empty input: {e}")

    try:
        res = agent.process_input("!@#$%")  # Special characters
        assert isinstance(res, dict)
        assert "error" in res.get("action", "").lower() or "invalid" in res.get("result", "").lower()
    except Exception as e:
        pytest.fail(f"process_input raised an exception on special input: {e}")

def test_reward_logging_and_values(caplog):
    """
    Reward system:
    - Call calculate_reward several times, assert returned values are in the expected set.
    - Use caplog to confirm a log message was created.
    - Test edge case with invalid result.
    """
    rs = RewardSystem()
    caplog.set_level(logging.INFO)
    values = {rs.calculate_reward("some result") for _ in range(10)}
    assert values.issubset({1, -1}), f"Unexpected reward values: {values}"
    assert any("Calculated reward" in r.getMessage() for r in caplog.records), "No reward log found"

    # Edge case: Invalid result
    with caplog.at_level(logging.INFO):
        invalid_reward = rs.calculate_reward(None)
        assert invalid_reward in [1, -1], "Invalid result should return default reward"
        assert any("Invalid result processed" in r.getMessage() for r in caplog.records), "No invalid result log"

def test_api_failure_simulation(monkeypatch, agent):
    """
    API failure simulation:
    - Patch external call (e.g., requests.post) and internal _call_api to raise errors.
    - Ensure agent handles failures gracefully.
    """
    import src.agent as agent_module

    # Patch requests.post
    if hasattr(agent_module, "requests"):
        def _fake_post(*args, **kwargs):
            raise RuntimeError("Simulated network failure")
        monkeypatch.setattr(agent_module.requests, "post", _fake_post)

    # Patch internal _call_api
    if hasattr(BasicAgent, "_call_api"):
        def _fake_call_api(self, *args, **kwargs):
            raise RuntimeError("Simulated internal API failure")
        monkeypatch.setattr(BasicAgent, "_call_api", _fake_call_api)

    try:
        res = agent.process_input("simulate failure")
        assert isinstance(res, dict)
        assert "error" in res.get("action", "").lower() or "failed" in res.get("result", "").lower()
    except Exception as e:
        pytest.fail(f"Agent crashed on simulated API failure: {e}")

def test_data_manager_team_registration(data_manager):
    """
    DataManager: Test team registration and retrieval.
    - Register a team and verify it’s in the list.
    - Test duplicate team registration (should raise ValueError).
    """
    team_id = data_manager.register_team("TestTeam", ["Member1"], "test@email.com", "TestCollege")
    assert isinstance(team_id, str)
    teams = data_manager.get_teams()
    assert any(t["team_name"] == "TestTeam" for t in teams)

    with pytest.raises(ValueError):
        data_manager.register_team("TestTeam", ["Member1"], "test@email.com", "TestCollege")

def test_data_manager_project_submission(data_manager):
    """
    DataManager: Test project submission and leaderboard.
    - Submit a project and verify it affects the leaderboard.
    """
    data_manager.register_team("TestTeam2", ["Member2"], "test2@email.com", "TestCollege2")
    submission_id = data_manager.submit_project(
        "TestTeam2", "TestProject", "Test desc", "github.com/test", "demo.com/test", ["Python"]
    )
    assert isinstance(submission_id, str)
    leaderboard = data_manager.get_leaderboard()
    assert any(entry["team_name"] == "TestTeam2" for entry in leaderboard)

# Add this if RL engine exists (adjust import if needed)
def test_rl_engine_integration(monkeypatch, agent):
    """
    RL Engine Integration: Mock RL engine interaction.
    - Simulate an RL update and verify state/action handling.
    """
    if not hasattr(agent, "rl_engine"):
        pytest.skip("RL engine not integrated in agent; skipping")

    def mock_update_q_value(self, state, action, reward):
        self.q_table[state][action] = reward
        return True

    monkeypatch.setattr(agent.rl_engine, "update_q_value", mock_update_q_value)
    state = {"input": "test"}
    action = "test_action"
    reward = 1
    result = agent.process_input("test", state=state)
    assert agent.rl_engine.update_q_value(state, action, reward)
    assert action in result.get("action", "")