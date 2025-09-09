# src/reasoning.py
import logging

logger = logging.getLogger(__name__)

class ReasoningModule:
    def plan_action(self, processed_input: str) -> str:
        """
        Simple reasoning logic:
        - If input mentions 'mentor', return 'mentor_action'
        - Otherwise, return 'default_action'
        """
        logger.info(f"Planning action for: {processed_input}")
        if "mentor" in processed_input.lower():
            return "mentor_action"
        return "default_action"

