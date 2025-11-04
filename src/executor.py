import logging
import time
import json
from src.integrations.bhiv_connectors import send_to_core, save_to_bucket
from src.bucket_connector import relay_to_bucket
from datetime import datetime

logger = logging.getLogger(__name__)

class Executor:
    def execute(self, action: str) -> str:
        logger.info(f"Executing action: {action}")
        
        # Log execution start
        execution_start_log = {
            "timestamp": datetime.now().isoformat(),
            "intent": "execution_detail",
            "actor": "executor",
            "context": f"Action: {action}",
            "outcome": "started"
        }
        relay_to_bucket(execution_start_log)
        
        try:
            # Simulate execution (replace with actual logic)
            if "->" not in action:
                raise ValueError("Invalid action format")
            steps = action.split(" -> ")
            
            # Log step processing
            step_processing_log = {
                "timestamp": datetime.now().isoformat(),
                "intent": "execution_detail",
                "actor": "executor",
                "context": f"Steps to execute: {steps}",
                "outcome": "processing"
            }
            relay_to_bucket(step_processing_log)
            
            executed = [f"Executed: {step}" for step in steps if step]
            result = " | ".join(executed) if executed else "No steps executed"
            
            # Log execution completion
            execution_complete_log = {
                "timestamp": datetime.now().isoformat(),
                "intent": "execution_detail",
                "actor": "executor",
                "context": f"Result: {result}",
                "outcome": "completed"
            }
            relay_to_bucket(execution_complete_log)
            
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
                
                # Log core communication success
                core_success_log = {
                    "timestamp": datetime.now().isoformat(),
                    "intent": "core_communication",
                    "actor": "executor",
                    "context": "Successfully sent to BHIV Core",
                    "outcome": "success"
                }
                relay_to_bucket(core_success_log)
            except Exception as e:
                logger.warning(f"Failed to send to BHIV Core: {str(e)}")
                
                # Log core communication failure
                core_failure_log = {
                    "timestamp": datetime.now().isoformat(),
                    "intent": "core_communication",
                    "actor": "executor",
                    "context": f"Failed to send to BHIV Core: {str(e)}",
                    "outcome": "failure"
                }
                relay_to_bucket(core_failure_log)
            
            try:
                filename = f"execution_{int(time.time())}.json"
                bucket_path = save_to_bucket(payload, filename)
                logger.info(f"Saved to BHIV Bucket: {bucket_path}")
                
                # Log bucket save success
                bucket_success_log = {
                    "timestamp": datetime.now().isoformat(),
                    "intent": "bucket_save",
                    "actor": "executor",
                    "context": f"Saved to BHIV Bucket: {bucket_path}",
                    "outcome": "success"
                }
                relay_to_bucket(bucket_success_log)
            except Exception as e:
                logger.warning(f"Failed to save to BHIV Bucket: {str(e)}")
                
                # Log bucket save failure
                bucket_failure_log = {
                    "timestamp": datetime.now().isoformat(),
                    "intent": "bucket_save",
                    "actor": "executor",
                    "context": f"Failed to save to BHIV Bucket: {str(e)}",
                    "outcome": "failure"
                }
                relay_to_bucket(bucket_failure_log)
            
            return result
        except ValueError as ve:
            logger.error(f"Execution failed due to invalid format: {str(ve)}")
            
            # Log execution error
            execution_error_log = {
                "timestamp": datetime.now().isoformat(),
                "intent": "execution_detail",
                "actor": "executor",
                "context": f"Execution failed: {str(ve)}",
                "outcome": "error"
            }
            relay_to_bucket(execution_error_log)
            
            raise
        except Exception as e:
            logger.error(f"Unexpected execution failure: {str(e)}")
            
            # Log unexpected error
            unexpected_error_log = {
                "timestamp": datetime.now().isoformat(),
                "intent": "execution_detail",
                "actor": "executor",
                "context": f"Unexpected execution failure: {str(e)}",
                "outcome": "error"
            }
            relay_to_bucket(unexpected_error_log)
            
            raise