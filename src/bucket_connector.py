# src/bucket_connector.py
# Production-ready connector for BHIV Bucket (MongoDB)
from typing import Dict, Any
import os
import logging
from datetime import datetime
from .database import get_db

# Set up logging
logger = logging.getLogger(__name__)

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
BUCKET_DB_NAME = os.getenv("BUCKET_DB_NAME", "blackholeinifverse60_db_user")

def relay_to_bucket(log_data: Dict[str, Any]) -> str:
    """
    Relay logs/data to BHIV Bucket (MongoDB insert).
    
    Args:
        log_data: Data to insert into the bucket
        
    Returns:
        Status message indicating success or failure
    """
    try:
        # Get database connection
        db = get_db()
        
        # Add timestamp if not present
        if "timestamp" not in log_data:
            log_data["timestamp"] = datetime.now().isoformat()
            
        db.logs.insert_one(log_data)
        logger.info("Successfully relayed log to bucket")
        return "Log relayed successfully"
    except Exception as e:
        logger.error(f"Error relaying log to bucket: {str(e)}")
        # Fallback to file logging
        try:
            # Fallback to file logging
            with open("bucket_fallback.log", "a") as f:
                f.write(f"{datetime.now().isoformat()}: {str(log_data)}\n")
            return "Log relayed to fallback file (MongoDB error)"
        except Exception as file_e:
            return f"Error relaying log: {str(e)}, File fallback error: {str(file_e)}"