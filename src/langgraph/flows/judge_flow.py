from langgraph.graph import StateGraph
from typing import Dict, Any
import logging, httpx
from src.database import get_db  # use your db helper
from tenacity import retry, wait_fixed, stop_after_attempt
import os

logger = logging.getLogger(__name__)

async def assign_judge(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # pick judge (simple round-robin placeholder)
    db = get_db()
    judges = list(db.judges.find({"active": True}))
    judge_id = judges[0]["_id"] if judges else "auto_judge"
    ctx["judge_id"] = str(judge_id)
    return ctx

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
async def notify_judge(ctx: Dict[str,Any]) -> Dict[str,Any]:
    notifier_url = ctx.get("NOTIFIER_URL", os.environ.get("NOTIFIER_URL", "http://localhost:8001"))
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{notifier_url}/notify/judge", json={"judge": ctx["judge_id"], "project": ctx["project_id"]})
    return ctx

async def persist_assignment(ctx: Dict[str,Any]) -> Dict[str,Any]:
    db = get_db()
    db.assignments.update_one(
        {"project_id": ctx["project_id"]},
        {"$set": {"judge_id": ctx["judge_id"], "ts": ctx.get("ts")}},
        upsert=True
    )
    return ctx

def build_judge_flow():
    g = StateGraph(dict)
    g.add_node("assign_judge", assign_judge)
    g.add_node("notify_judge", notify_judge)
    g.add_node("persist_assignment", persist_assignment)
    g.set_entry_point("assign_judge")
    g.add_edge("assign_judge", "notify_judge")
    g.add_edge("notify_judge", "persist_assignment")
    g.set_finish_point("persist_assignment")
    return g.compile()