import logging

logger = logging.getLogger(__name__)

class RewardSystem:
    def calculate_reward(self, result: str) -> int:
        if result and str(result).strip():
            logger.info(f"Calculated reward for result: {result}")
            return 1
        else:
            logger.info("Invalid result processed")
            return -1

