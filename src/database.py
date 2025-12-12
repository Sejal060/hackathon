import os
from pymongo import MongoClient
import time

# MONGO_URI will be read from environment variables when connect_to_db is called

client = None
db = None

def connect_to_db_with_retry(retries=5, delay=2):
    """
    Create a global MongoDB client with retry logic & select the default database.
    Call this on app startup.
    """
    global client, db
    # Read from environment variable
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI is not set in environment variables")

    for i in range(retries):
        try:
            # Create client with connection pooling and timeout settings
            _client = MongoClient(MONGO_URI, maxPoolSize=20, serverSelectionTimeoutMS=5000)
            # Test the connection
            _client.admin.command('ping')
            
            # Choose a database name – you can change 'hackathon' to anything you like
            _db = _client["hackathon"]

            # Assign to globals
            globals()["client"] = _client
            globals()["db"] = _db
            
            print("✅ Connected to MongoDB Atlas")
            return _client
        except Exception as e:
            print(f"DB connection failed (attempt {i+1}/{retries}), retrying...")
            if i < retries - 1:  # Don't sleep on the last attempt
                time.sleep(delay)
    
    raise Exception("Could not connect to MongoDB after retries")

def connect_to_db():
    """
    Create a global MongoDB client & select the default database.
    Call this on app startup.
    """
    return connect_to_db_with_retry()

def get_db():
    """
    Returns the global db object. Use this inside your routes/services.
    """
    if db is None:
        raise RuntimeError("Database is not initialized. Did you call connect_to_db() on startup?")
    return db

def close_db():
    """
    Close the global client on shutdown.
    """
    global client
    if client is not None:
        client.close()
        client = None
        print("🛑 MongoDB connection closed")