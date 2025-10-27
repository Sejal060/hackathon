import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class ReasoningModule:
    """
    Reasoning engine that can plan locally or query external MCP (BHIV) agents.
    """

    def __init__(self, use_external_agent: bool = True):
        self.use_external_agent = use_external_agent
        self.mcp_endpoint = "http://localhost:8002/handle_task"

    def plan(self, processed_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate or fetch a reasoning plan.
        If use_external_agent=True, the function sends the query to the BHIV MCP bridge.
        Otherwise, it uses local logic.
        """
        logger.info(f"Planning action for: {processed_input}, context: {context}")

        # Step 1: Try external MCP reasoning
        if self.use_external_agent:
            try:
                payload = {
                    "agent": "edumentor_agent",
                    "input": processed_input,
                    "pdf_path": "",
                    "input_type": "text",
                    "retries": 2,
                    "fallback_model": "edumentor_agent",
                    "tags": ["reasoning", "ai", "plan"]
                }
                logger.info(f"Sending reasoning request to MCP bridge: {self.mcp_endpoint}")
                response = requests.post(self.mcp_endpoint, json=payload, timeout=20)
                response.raise_for_status()
                result = response.json()

                if isinstance(result, dict) and "agent_output" in result:
                    logger.info("Received response from MCP bridge.")
                    return str(result["agent_output"])

            except Exception as e:
                logger.error(f"External MCP reasoning failed: {str(e)}. Falling back to local reasoning.")

        # Step 2: Local reasoning fallback
        if "trip" in processed_input.lower() or "mountain" in processed_input.lower():
            base_plan = "Check weather -> Book transport -> Pack essentials -> Start trip"
        elif "hackathon" in processed_input.lower():
            base_plan = "Decide theme -> Invite participants -> Arrange venue -> Schedule sessions"
        elif "meeting" in processed_input.lower():
            base_plan = "Prepare agenda -> Send invites -> Reserve meeting room -> Conduct meeting"
        else:
            base_plan = f"Process input: {processed_input} -> Take general action"

        if context:
            location = context.get("location", "unknown")
            priority = context.get("priority", "normal")
            base_plan += f" | Context: location={location}, priority={priority}"

        logger.info(f"Generated local plan: {base_plan}")
        return base_plan
