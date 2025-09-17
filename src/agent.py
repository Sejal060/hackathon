from groq import Groq
from typing import Dict
import logging
import os

logger = logging.getLogger(__name__)

class BasicAgent:
    def __init__(self, api_key: str = None, role: str = "generic"):
        """
        api_key: Groq API key (optional, can also come from environment variable)
        role: a simple label for this agent (e.g., 'planner', 'executor')
        """
        self.role = role
        try:
            self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        except Exception:
            self.client = None  # allow tests to run without API key

    def process_input(self, user_input: str) -> Dict[str, str]:
        logger.info(f"Step 1: Received input - {user_input}")
        try:
            if not self.client:
                # fallback for testing without Groq API
                return {"thoughts": f"Simulated processing of: {user_input}", "action": "test-output"}

            response = self.client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                messages=[{"role": "user", "content": user_input}]
            )
            output = response.choices[0].message.content
            logger.info("Step 2: Reasoning complete")
            return {"thoughts": "Processed user input", "action": output}
        except Exception as e:
            logger.error(f"Step 3: Error - {str(e)}")
            return {"thoughts": "Error in processing", "action": str(e)}

    # 🟢 New methods
    def propose_plan(self, user_input: str) -> str:
        """Planner role generates a plan."""
        if not user_input:
            return "Invalid input. No plan generated."
        return f"[Plan by {self.role}] Steps to handle: {user_input}"

    def execute_plan(self, plan: str) -> str:
        """Executor role executes a plan."""
        if not plan:
            return "Invalid plan. Nothing executed."
        return f"[Execution by {self.role}] Result: Completed {plan}"


class AgentFactory:
    @staticmethod
    def create_planner_agent(api_key: str = None) -> BasicAgent:
        return BasicAgent(api_key=api_key, role="planner")

    @staticmethod
    def create_executor_agent(api_key: str = None) -> BasicAgent:
        return BasicAgent(api_key=api_key, role="executor")



