# src/reward.py
import logging
import numpy as np

logger = logging.getLogger(__name__)

class RewardSystem:
    def calculate_reward(self, result: str) -> int:
        reward = np.random.choice([1, -1])
        logger.info(f"Calculated reward: {reward}")
        return reward

