# src/database.py
# Centralized database connection management for the HackaVerse engine
import os
import time
import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

# Configure logging
logger = logging.getLogger(__name__)

# Global database connection
db = None

def connect_to_db_with_retry(retries=5, delay=2):
    """
    Connect to MongoDB with retry logic and connection pooling.
    
    Args:
        retries (int): Number of retry attempts
        delay (int): Delay between retries in seconds
        
    Returns:
        MongoClient: Connected MongoDB client
        
    Raises:
        RuntimeError: If connection fails after all retries
    """
    global db
    
    # Get MongoDB URI from environment
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise RuntimeError("MONGODB_URI is not set in environment variables")
    
    # Try to connect with retries
    for attempt in range(retries):
        try:
            logger.info(f"Connecting to MongoDB (attempt {attempt + 1}/{retries})...")
            
            # Create client with connection pooling and timeout settings
            client = MongoClient(
                mongodb_uri,
                maxPoolSize=20,  # Increase connection pool size
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            client.admin.command('ping')
            logger.info("✅ Connected to MongoDB Atlas")
            
            # Get the database
            db_name = os.getenv("BUCKET_DB_NAME", "blackholeinifverse60_db_user")
            db = client[db_name]
            
            # Create indexes for better performance
            _create_indexes(db)
            
            return client
            
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.warning(f"MongoDB connection attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:  # Don't sleep on the last attempt
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("❌ Failed to connect to MongoDB after all retries")
                raise RuntimeError(f"Failed to connect to MongoDB after {retries} attempts: {e}")
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise RuntimeError(f"Unexpected error connecting to MongoDB: {e}")

def _create_indexes(database):
    """Create indexes for better performance"""
    try:
        # Index for provenance logs
        database.provenance_logs.create_index([("timestamp", 1)])
        database.provenance_logs.create_index([("entry_hash", 1)], unique=True)
        
        # Index for regular logs
        database.logs.create_index([("timestamp", 1)])
        
        # Index for assignments
        database.assignments.create_index([("project_id", 1)], unique=True)
        
        logger.info("✅ Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Failed to create indexes: {e}")

def get_db():
    """
    Returns the global db object. Use this inside your routes/services.
    """
    if db is None:
        raise RuntimeError("Database is not initialized. Did you call connect_to_db() on startup?")
    return db

def close_db():
    """
    Close the database connection gracefully.
    """
    global db
    if db is not None:
        try:
            db.client.close()
            logger.info("✅ Database connection closed")
        except Exception as e:
            logger.warning(f"Error closing database connection: {e}")
        finally:
            db = None