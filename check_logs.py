from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["bhiv_db"]

# Check if logs collection exists and has data
try:
    # List collections
    collections = db.list_collection_names()
    print(f"Collections in bhiv_db: {collections}")
    
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