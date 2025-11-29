# src/multi_agent.py
from .agent import BasicAgent
import logging
import numpy as np  # for random rewards

# Import the workflow manager
from langgraph_workflows.workflow_manager import workflow_manager

logger = logging.getLogger(__name__)

class PlannerAgent(BasicAgent):
    def propose_plan(self, task: str) -> str:
        logger.info(f"Planner: Proposing plan for task '{task}'")
        return f"Plan: Step 1 → Work on {task}"

class ExecutorAgent(BasicAgent):
    def execute_plan(self, plan: str) -> str:
        logger.info(f"Executor: Executing plan '{plan}'")
        return f"Result: {plan} executed successfully"

class Environment:
    def give_reward(self, result: str) -> int:
        # RL-style: random +1 or -1 reward (humility → learn from failures too)
        reward = int(np.random.choice([1, -1]))
        logger.info(f"Environment: Reward {reward} (humility: learn from -1)")
        return reward

def route_to_workflow(agent_type: str, payload: dict):
    """Route to the appropriate workflow based on agent type"""
    if agent_type == "judge":
        return workflow_manager.run_judging_reminder()
    elif agent_type == "mentor":
        return workflow_manager.run_mentorbot_request(payload)
    else:
        logger.warning(f"Unknown agent type: {agent_type}")
        return {"status": "error", "message": f"Unknown agent type: {agent_type}"}