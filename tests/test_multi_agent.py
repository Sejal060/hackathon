import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pytest
from agent import AgentFactory

@pytest.fixture
def agents():
    return {
        "planner": AgentFactory.create_planner_agent(),
        "executor": AgentFactory.create_executor_agent()
    }

def test_multi_agent_flow(agents):
    plan = agents["planner"].propose_plan("Organize a hackathon")
    assert "Plan" in plan
    result = agents["executor"].execute_plan(plan)
    assert "Result" in result

def test_invalid_input(agents):
    plan = agents["planner"].propose_plan("")
    assert isinstance(plan, str)  # Should not crash