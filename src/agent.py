# src/agent.py
from groq import Groq
from typing import Dict
import logging
import os

logger = logging.getLogger(__name__)

class BasicAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def process_input(self, user_input: str) -> Dict[str, str]:
        logger.info(f"Step 1: Received input - {user_input}")
        try:
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