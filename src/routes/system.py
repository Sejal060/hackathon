# src/routes/system.py
from fastapi import APIRouter
from datetime import datetime
import platform
import sys
import time
from ..logger import ksml_logger

router = APIRouter(prefix="/system", tags=["system"])

# Track application start time for uptime calculation
START_TIME = time.time()

@router.get("/health", summary="Check system health")
def health_endpoint():
    """
    Check system health and return status information.
    
    Returns:
    - **status**: Current system status
    - **uptime**: Application uptime in seconds
    - **version**: API version
    """
    # Calculate uptime
    uptime = time.time() - START_TIME
    
    # Log the health check using KSML
    ksml_logger.log_system_health("ok")
    
    return {
        "status": "ok",
        "uptime": f"{uptime:.2f} seconds",
        "version": "v3"
    }