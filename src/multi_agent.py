# src/multi_agent.py
from .agent import BasicAgent
import logging
import numpy as np  # for random rewards

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
