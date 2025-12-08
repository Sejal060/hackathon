import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import database helper
from src.database import connect_to_db, get_db

# Connect to MongoDB
connect_to_db()
db = get_db()

# Check if logs collection exists and has data
try:
    # List collections
    collections = db.list_collection_names()
    print(f"Collections in blackholeinifverse60_db_user: {collections}")
    
    # Check logs collection
    if "logs" in collections:
        log_count = db.logs.count_documents({})
        print(f"Number of log entries: {log_count}")
        
        # Show a few log entries
        if log_count > 0:
            print("\nSample log entries:")
            logs = db.logs.find().limit(3)
            for log in logs:
                print(f"  - {log}")
        else:
            print("No log entries found")
    else:
        print("Logs collection not found")
        
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")