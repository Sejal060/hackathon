# src/database.py
# Centralized database connection management for the HackaVerse engine
import os
import time
import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from fastapi import HTTPException

# Configure logging
logger = logging.getLogger(__name__)

# Environment
ENV = os.getenv("ENV", "development")

# Global database connection
db = None

# Degraded mode globals
DB_AVAILABLE = False
DB_ERROR_TYPE = None

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
    global db, DB_AVAILABLE, DB_ERROR_TYPE
    
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

            # Set degraded mode globals
            DB_AVAILABLE = True
            DB_ERROR_TYPE = None

            return client
            
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.warning(f"MongoDB connection attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:  # Don't sleep on the last attempt
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                # Set degraded mode
                DB_AVAILABLE = False
                if "Authentication failed" in str(e):
                    DB_ERROR_TYPE = "auth"
                elif isinstance(e, ServerSelectionTimeoutError):
                    DB_ERROR_TYPE = "dns"
                elif isinstance(e, ConnectionFailure):
                    DB_ERROR_TYPE = "network"
                else:
                    DB_ERROR_TYPE = "unknown"
                logger.error("❌ Failed to connect to MongoDB after all retries")
                break  # Exit the loop
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            DB_AVAILABLE = False
            DB_ERROR_TYPE = "unknown"
            break

    # Handle degraded mode based on environment
    if not DB_AVAILABLE:
        if ENV == "production":
            raise RuntimeError(f"Database connection failed in production mode. Error type: {DB_ERROR_TYPE}")
        else:
            logger.warning(f"Starting in degraded mode (ENV={ENV}). Database unavailable. Error type: {DB_ERROR_TYPE}")
    else:
        logger.info("Database connection successful")

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

        # Index for submissions
        database.submissions.create_index([("submission_hash", 1)], unique=True)
        database.submissions.create_index([("team_id", 1)])

        # Index for judgments
        database.judgments.create_index([("submission_hash", 1)])
        database.judgments.create_index([("team_id", 1)])
        database.judgments.create_index([("version", 1)])
        
        logger.info("✅ Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Failed to create indexes: {e}")

def get_db():
    """
    Returns the global db object. Use this inside your routes/services.
    """
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail=f"Database unavailable in degraded mode. Error type: {DB_ERROR_TYPE}")
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

def get_db_status():
    """
    Returns database status for health checks.
    """
    return {
        "db_connected": DB_AVAILABLE,
        "degraded_mode": not DB_AVAILABLE,
        "env": ENV,
        "db_error_type": DB_ERROR_TYPE
    }