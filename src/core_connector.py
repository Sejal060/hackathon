# src/core_connector.py
# Production-ready connector for BHIV Core
import requests
from typing import Dict, Any
from .bucket_connector import relay_to_bucket
from datetime import datetime
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Get BHIV Core URL from environment variables with fallback
BHIV_CORE_URL = os.getenv("BHIV_CORE_URL", "http://localhost:8002/reason")

def connect_to_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handshake with BHIV Core - POST payload to /process.
    
    Args:
        payload: Data to send to BHIV Core
        
    Returns:
        Response from BHIV Core or mock response if connection fails
    """
    # Log core connection attempt
    connection_log = {
        "timestamp": datetime.now().isoformat(),
        "intent": "core_connection",
        "actor": "core_connector",
        "context": f"Connecting to {BHIV_CORE_URL} with payload: {str(payload)}",
        "outcome": "attempted"
    }
    relay_to_bucket(connection_log)
    
    try:
        # Make request to BHIV Core with timeout and proper headers
        response = requests.post(
            BHIV_CORE_URL, 
            json=payload, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        
        # Log successful connection
        success_log = {
            "timestamp": datetime.now().isoformat(),
            "intent": "core_connection",
            "actor": "core_connector",
            "context": f"Successfully connected to BHIV Core. Response: {str(result)}",
            "outcome": "success"
        }
        relay_to_bucket(success_log)
        
        logger.info(f"Successfully connected to BHIV Core: {BHIV_CORE_URL}")
        return result
    except requests.exceptions.Timeout:
        error_msg = f"Timeout connecting to BHIV Core at {BHIV_CORE_URL}"
        logger.error(error_msg)
        
        # Log timeout failure
        failure_log = {
            "timestamp": datetime.now().isoformat(),
            "intent": "core_connection",
            "actor": "core_connector",
            "context": error_msg,
            "outcome": "timeout"
        }
        relay_to_bucket(failure_log)
        
        # Return a mock response for timeout
        return {"status": "timeout", "message": error_msg, "data": payload}
    except requests.exceptions.ConnectionError:
        error_msg = f"Connection error connecting to BHIV Core at {BHIV_CORE_URL}"
        logger.error(error_msg)
        
        # Log connection error failure
        failure_log = {
            "timestamp": datetime.now().isoformat(),
            "intent": "core_connection",
            "actor": "core_connector",
            "context": error_msg,
            "outcome": "connection_error"
        }
        relay_to_bucket(failure_log)
        
        # Return a mock response for connection error
        return {"status": "connection_error", "message": error_msg, "data": payload}
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error connecting to BHIV Core: {str(e)}"
        logger.error(error_msg)
        
        # Log request exception failure
        failure_log = {
            "timestamp": datetime.now().isoformat(),
            "intent": "core_connection",
            "actor": "core_connector",
            "context": error_msg,
            "outcome": "request_error"
        }
        relay_to_bucket(failure_log)
        
        # Return a mock response for other request errors
        return {"status": "request_error", "message": error_msg, "data": payload}
    except Exception as e:
        error_msg = f"Unexpected error connecting to BHIV Core: {str(e)}"
        logger.error(error_msg)
        
        # Log unexpected error failure
        failure_log = {
            "timestamp": datetime.now().isoformat(),
            "intent": "core_connection",
            "actor": "core_connector",
            "context": error_msg,
            "outcome": "unexpected_error"
        }
        relay_to_bucket(failure_log)
        
        # Return a mock response for unexpected errors
        return {"status": "unexpected_error", "message": error_msg, "data": payload}