# src/routes/system.py
from fastapi import APIRouter
from datetime import datetime
import platform
import sys
import time
from ..logger import ksml_logger
from ..database import get_db
from ..schemas.response import APIResponse

router = APIRouter(prefix="/system", tags=["system"])

# Track application start time for uptime calculation
START_TIME = time.time()

def get_uptime():
    """Calculate and return application uptime"""
    return time.time() - START_TIME

@router.get("/health", summary="Check system health")
async def health():
    """
    Check system health and return status information.
    
    Returns:
    - **success**: Boolean indicating success
    - **message**: Status message
    - **data**: Contains uptime and version
    """
    # Calculate uptime
    uptime = get_uptime()
    version = "v3"
    
    # Log the health check using KSML
    ksml_logger.log_system_health("ok")
    
    return APIResponse(
        success=True,
        message="System is healthy",
        data={
            "uptime": f"{uptime:.2f} seconds",
            "version": version
        }
    )

@router.get("/test-db", summary="Test database connection")
async def test_db():
    """
    Test database connection and list collections.
    
    Returns:
    - **success**: Boolean indicating success
    - **message**: Status message
    - **data**: Contains list of collections
    """
    db = get_db()
    # Example: list collections
    collections = db.list_collection_names()
    return APIResponse(
        success=True,
        message="Database connection successful",
        data={"collections": collections}
    )

@router.get("/ready")
async def readiness():
    return APIResponse(
        success=True,
        message="Service is ready",
        data=None
    )