# src/bucket_connector.py
# Production-ready connector for BHIV Bucket (MongoDB)
from pymongo import MongoClient
from typing import Dict, Any
import os
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
BUCKET_DB_NAME = os.getenv("BUCKET_DB_NAME", "bhiv_db")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5 second timeout
    db = client[BUCKET_DB_NAME]
    # Test the connection
    client.server_info()
    logger.info(f"Successfully connected to MongoDB at {MONGO_URI}")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    client = None
    db = None

def relay_to_bucket(log_data: Dict[str, Any]) -> str:
    """
    Relay logs/data to BHIV Bucket (MongoDB insert).
    
    Args:
        log_data: Data to insert into the bucket
        
    Returns:
        Status message indicating success or failure
    """
    # If MongoDB connection failed, log to file as fallback
    if client is None or db is None:
        try:
            # Fallback to file logging
            with open("bucket_fallback.log", "a") as f:
                f.write(f"{datetime.now().isoformat()}: {str(log_data)}\n")
            return "Log relayed to fallback file (MongoDB unavailable)"
        except Exception as e:
            return f"Error relaying log to fallback: {str(e)}"
    
    try:
        # Add timestamp if not present
        if "timestamp" not in log_data:
            log_data["timestamp"] = datetime.now().isoformat()
            
        db.logs.insert_one(log_data)
        logger.info("Successfully relayed log to bucket")
        return "Log relayed successfully"
    except Exception as e:
        logger.error(f"Error relaying log to bucket: {str(e)}")
        return f"Error relaying log: {str(e)}"