# src/routes/admin.py
from fastapi import APIRouter
from ..models import RewardRequest, RewardResponse, LogRequest, TeamRegistration
from ..bucket_connector import relay_to_bucket
from datetime import datetime

router = APIRouter(prefix="/admin")

@router.post("/reward", response_model=RewardResponse)
def reward_endpoint(request: RewardRequest):
    # Apply reward logic (stub for now)
    log = {
        "intent": "reward", 
        "outcome": request.outcome,
        "request_id": request.request_id,
        "timestamp": datetime.now().isoformat()
    }
    relay_to_bucket(log)
    return {"reward_value": 1.0, "feedback": "Reward applied successfully"}

@router.post("/logs")
def logs_endpoint(request: LogRequest):
    # Convert Pydantic model to dict for relay_to_bucket
    log_data = request.dict()
    result = relay_to_bucket(log_data)
    return {"status": "logged", "result": result}

@router.post("/register")
def register_endpoint():
    # Placeholder for register endpoint
    return {"message": "Team registered successfully"}

@router.post("/webhook/hackaverse/registration")
def webhook_registration(payload: TeamRegistration):
    log = {
        "intent": "registration", 
        "actor": "webhook", 
        "context": str(payload), 
        "outcome": "success",
        "timestamp": datetime.now().isoformat()
    }
    relay_to_bucket(log)
    # Add registration logic if needed
    return {"status": "registered"}