from groq import Groq
from typing import Dict
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class BasicAgent:
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "test-key")
        self.client = Groq(api_key=self.api_key)

    def process_input(self, user_input: str) -> Dict[str, str]:
        logger.info(f"Step 1: Received input - {user_input}")
        if user_input is None or user_input.strip() == "":
            logger.info("Step 2: Empty or None input received")
            return {"thoughts": "No input provided", "result": "No action taken"}
        try:
            response = self.client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                messages=[{"role": "user", "content": user_input}]
            )
            output = response.choices[0].message.content
            logger.info("Step 2: Reasoning complete")
            return {"thoughts": "Processed user input", "result": output}
        except Exception as e:
            logger.error(f"Step 3: Error - {str(e)}")
            return {"thoughts": "Error in processing", "result": f"Failed due to: {str(e)}"}