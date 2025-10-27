import logging
import time
import json
from src.integrations.bhiv_connectors import send_to_core, save_to_bucket

logger = logging.getLogger(__name__)

class Executor:
    def execute(self, action: str) -> str:
        logger.info(f"Executing action: {action}")
        try:
            # Simulate execution (replace with actual logic)
            if "->" not in action:
                raise ValueError("Invalid action format")
            steps = action.split(" -> ")
            executed = [f"Executed: {step}" for step in steps if step]
            result = " | ".join(executed) if executed else "No steps executed"
            
            # Prepare payload for BHIV integration
            payload = {
                "action": action,
                "result": result,
                "timestamp": time.time(),
                "steps_count": len(executed)
            }
            
            # Send to BHIV Core and save to BHIV Bucket
            try:
                core_resp = send_to_core(payload)
                logger.info(f"Sent to BHIV Core: {core_resp}")
            except Exception as e:
                logger.warning(f"Failed to send to BHIV Core: {str(e)}")
            
            try:
                filename = f"execution_{int(time.time())}.json"
                bucket_path = save_to_bucket(payload, filename)
                logger.info(f"Saved to BHIV Bucket: {bucket_path}")
            except Exception as e:
                logger.warning(f"Failed to save to BHIV Bucket: {str(e)}")
            
            return result
        except ValueError as ve:
            logger.error(f"Execution failed due to invalid format: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected execution failure: {str(e)}")
            raise