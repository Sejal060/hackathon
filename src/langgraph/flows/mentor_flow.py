from langgraph.graph import StateGraph
import logging, httpx
from src.database import get_db
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)

async def validate(ctx: Dict[str,Any]) -> Dict[str,Any]:
    if not ctx.get("question"): raise ValueError("question missing")
    return ctx

async def route_to_mentor(ctx: Dict[str,Any]) -> Dict[str,Any]:
    db = get_db()
    mentor = db.mentors.find_one({"active": True}) or {"_id":"mentor_auto"}
    ctx["mentor_id"] = str(mentor["_id"])
    return ctx

async def send_reply(ctx: Dict[str,Any]) -> Dict[str,Any]:
    notifier_url = ctx.get("NOTIFIER_URL", os.environ.get("NOTIFIER_URL", "http://localhost:8001"))
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{notifier_url}/notify/mentor", json={"mentor": ctx["mentor_id"], "question": ctx["question"], "user": ctx.get("user")})
    db = get_db()
    db.mentor_queries.insert_one({"user": ctx.get("user"), "question": ctx["question"], "mentor": ctx["mentor_id"]})
    return ctx

def build_mentor_flow():
    g = StateGraph(dict)
    g.add_node("validate", validate)
    g.add_node("route", route_to_mentor)
    g.add_node("reply", send_reply)
    g.set_entry_point("validate")
    g.add_edge("validate", "route")
    g.add_edge("route", "reply")
    g.set_finish_point("reply")
    return g.compile()