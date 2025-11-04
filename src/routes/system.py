# src/routes/system.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/system")

@router.get("/health")
def health_endpoint():
    return {"status": "healthy", "version": "v2", "timestamp": datetime.now().isoformat()}