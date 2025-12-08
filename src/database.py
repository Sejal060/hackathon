# src/database.py
import os
from pymongo import MongoClient

# MONGO_URI will be read from environment variables when connect_to_db is called

client = None
db = None

def connect_to_db():
    """
    Create a global MongoDB client & select the default database.
    Call this on app startup.
    """
    global client, db
    # Read from environment variable
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI is not set in environment variables")

    if client is None:
        # Create client
        _client = MongoClient(MONGO_URI)

        # Choose a database name – you can change 'hackathon' to anything you like
        _db = _client["hackathon"]

        # Assign to globals
        globals()["client"] = _client
        globals()["db"] = _db

        print("✅ Connected to MongoDB Atlas")

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