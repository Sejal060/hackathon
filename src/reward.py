import logging

logger = logging.getLogger(__name__)

class RewardSystem:
    def calculate_reward(self, result: str) -> int:
        logger.info(f"Calculating reward for result: {result}")
        # Handle None or empty input
        if result is None or result == "":
            return 0
        # Simple scoring logic: +1 per executed step
        steps = result.split("|")
        # Remove empty steps to handle cases like "||"
        steps = [step for step in steps if step]
        reward = len(steps)
        return reward