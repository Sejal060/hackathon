# src/bucket_connector.py
# Placeholder - await Vinayak's endpoints
from pymongo import MongoClient
from typing import Dict, Any
import os

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)  # From .env MONGO_URI
db = client["bhiv_db"]

def relay_to_bucket(log_data: Dict[str, Any]) -> str:
    """Relay logs/data to BHIV Bucket (MongoDB insert)."""
    try:
        db.logs.insert_one(log_data)
        return "Log relayed successfully"
    except Exception as e:
        return f"Error relaying log: {str(e)}"