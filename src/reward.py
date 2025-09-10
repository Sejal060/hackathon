# src/reward.py
import logging

logger = logging.getLogger(__name__)

class RewardSystem:
    def calculate_reward(self, result: str) -> int:
        logger.info(f"Calculating reward for result: {result}")
        # Simple scoring logic: +1 per executed step
        steps = result.split("|")
        reward = len(steps)
        return reward
