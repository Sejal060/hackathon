import requests
import json
import os
import time
from typing import Dict
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Environment variables with defaults
BHIV_CORE_URL = os.getenv("BHIV_CORE_URL", "http://localhost:9000/bhiv/core")
BUCKET_DIR = os.getenv("BHIV_BUCKET_DIR", "./data/bucket")
FAILED_LOG_PATH = "data/failed_core_sends.log"

# Create directories if they don't exist
os.makedirs(BUCKET_DIR, exist_ok=True)
os.makedirs(os.path.dirname(FAILED_LOG_PATH) if os.path.dirname(FAILED_LOG_PATH) else ".", exist_ok=True)

def send_to_core(payload: Dict, max_retries=3, backoff=1):
    """
    Send payload to BHIV Core with retry logic.
    
    Args:
        payload: Dictionary containing the data to send
        max_retries: Maximum number of retry attempts
        backoff: Backoff multiplier for retry delays
        
    Returns:
        Response from BHIV Core
        
    Raises:
        Exception: If all retry attempts fail
    """
    logger.info(f"Sending payload to BHIV Core: {BHIV_CORE_URL}")
    
    for i in range(max_retries):
        try:
            resp = requests.post(BHIV_CORE_URL, json=payload, timeout=5)
            resp.raise_for_status()
            logger.info("Successfully sent payload to BHIV Core")
            return resp.json()
        except Exception as e:
            logger.warning(f"Attempt {i+1} failed: {str(e)}")
            last_exception = e
            if i < max_retries - 1:  # Don't sleep on the last attempt
                time.sleep(backoff * (i+1))
    
    # After retries, log failure and raise
    logger.error(f"All retry attempts failed. Logging to {FAILED_LOG_PATH}")
    try:
        with open(FAILED_LOG_PATH, "a") as f:
            f.write(json.dumps({
                "timestamp": time.time(),
                "payload": payload, 
                "error": str(last_exception)
            }) + "\n")
    except Exception as log_error:
        logger.error(f"Failed to write to error log: {str(log_error)}")
    
    raise last_exception

def save_to_bucket(payload: Dict, filename: str):
    """
    Save payload to BHIV Bucket (local file storage).
    
    Args:
        payload: Dictionary containing the data to save
        filename: Name of the file to save the data to
        
    Returns:
        Path to the saved file
    """
    path = os.path.join(BUCKET_DIR, filename)
    logger.info(f"Saving payload to BHIV Bucket: {path}")
    
    try:
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)
        logger.info(f"Successfully saved payload to {path}")
        return path
    except Exception as e:
        logger.error(f"Failed to save payload to bucket: {str(e)}")
        raise