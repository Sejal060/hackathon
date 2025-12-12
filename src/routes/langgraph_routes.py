from fastapi import APIRouter, Body, HTTPException
import os
from src.langgraph.runner import run_flow
from src.schemas.response import APIResponse

router = APIRouter(prefix="/flows", tags=["langgraph"])

@router.post("/{flow_name}")
async def trigger_flow(flow_name: str, payload: dict = Body(...)):
    try:
        # inject env defaults if needed, e.g. NOTIFIER_URL from settings
        payload.setdefault("NOTIFIER_URL", os.environ.get("NOTIFIER_URL"))
        result = await run_flow(flow_name, payload)
        return APIResponse(success=True, message="Flow executed", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))