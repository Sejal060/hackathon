# src/routes/system.py
from fastapi import APIRouter
from datetime import datetime
import platform
import sys
from ..logger import ksml_logger

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/health", summary="Check system health")
def health_endpoint():
    """
    Check system health and return status information.
    
    Returns:
    - **status**: Current system status
    - **version**: API version
    - **timestamp**: Current timestamp
    - **platform**: Platform information
    """
    # Log the health check using KSML
    ksml_logger.log_system_health("healthy")
    
    return {
        "status": "healthy", 
        "version": "v2.0",
        "timestamp": datetime.now().isoformat(),
        "platform": f"{platform.system()} {platform.release()}",
        "python_version": sys.version
    }