# src/reasoning.py
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class ReasoningModule:
    def plan(self, processed_input: str, context: Optional[Dict] = None) -> str:
        """
        Generate a plan based on the processed input and optional context.
        Args:
            processed_input: Processed input string from InputHandler.
            context: Optional dictionary with additional context (e.g., user preferences).
        Returns:
            A string representing the planned action.
        """
        logger.info(f"Planning action for: {processed_input}, context: {context}")
        
        # Initialize plan based on keywords in input
        if "trip" in processed_input.lower() or "mountain" in processed_input.lower():
            base_plan = "Check weather -> Book transport -> Pack essentials -> Start trip"
        elif "hackathon" in processed_input.lower():
            base_plan = "Decide theme -> Invite participants -> Arrange venue -> Schedule sessions"
        elif "meeting" in processed_input.lower():
            base_plan = "Prepare agenda -> Send invites -> Reserve meeting room -> Conduct meeting"
        else:
            base_plan = f"Process input: {processed_input} -> Take general action"
        
        # Incorporate context if provided (example logic)
        if context:
            # Example: Modify plan based on context (e.g., location or priority)
            location = context.get("location", "unknown")
            priority = context.get("priority", "normal")
            base_plan += f" | Context: location={location}, priority={priority}"
        
        logger.info(f"Generated plan: {base_plan}")
        return base_plan