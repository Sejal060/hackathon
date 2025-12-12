import asyncio
from typing import Dict, Any
from src.langgraph.manager import get_flow

async def run_flow(name: str, payload: Dict[str, Any]):
    flow = get_flow(name)
    if not flow:
        raise ValueError(f"Unknown flow: {name}")
    # adapt to actual langgraph compiled API — many compile()s return an object with .run(payload)
    result = await flow.ainvoke(payload)  # if API differs, Qoder can adjust
    return result

def run_flow_sync(name: str, payload: Dict[str, Any]):
    return asyncio.run(run_flow(name, payload))