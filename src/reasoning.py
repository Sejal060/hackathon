# src/reasoning.py
class Reasoning:
    def plan(self, processed_input: str) -> str:
        # Simple planner logic (expand as needed)
        if "mentor" in processed_input:
            return "mentor_action"
        elif "reminder" in processed_input:
            return "reminder_action"
        elif "judge" in processed_input:
            return "judging_action"
        else:
            return "default_action"
