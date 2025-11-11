from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["bhiv_db"]

# Check for KSML formatted logs (they should have intent, actor, context, outcome fields)
try:
    # Find logs with KSML format
    ksml_logs = db.logs.find({
        "intent": {"$exists": True},
        "actor": {"$exists": True},
        "context": {"$exists": True},
        "outcome": {"$exists": True}
    }).limit(5)
    
    ksml_logs_list = list(ksml_logs)
    
    if len(ksml_logs_list) > 0:
        print(f"Found {len(ksml_logs_list)} KSML formatted logs:")
        for log in ksml_logs_list:
            print(f"  - Intent: {log.get('intent')}, Actor: {log.get('actor')}, Outcome: {log.get('outcome')}")
    else:
        print("No KSML formatted logs found in MongoDB")
        
    # Check total log count
    total_logs = db.logs.count_documents({})
    print(f"\nTotal logs in database: {total_logs}")
        
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")