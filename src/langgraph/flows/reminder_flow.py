from langgraph.graph import StateGraph
import httpx, logging
from src.database import get_db
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)

async def load_targets(ctx: Dict[str,Any]) -> Dict[str,Any]:
    db = get_db()
    target_type = ctx.get("target", "teams")
    if target_type == "teams":
        ctx["targets"] = list(db.teams.find({"registered": True}))
    else:
        ctx["targets"] = list(db.judges.find({}))
    return ctx

async def send_reminders(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Send reminders (simulate by logging)
    for t in ctx.get("targets", []):
        logger.info(f"Reminder sent to {t}")
    # Log delivery
    db = get_db()
    db.reminder_logs.insert_one({
        "targets": ctx["targets"],
        "message": ctx.get("message", "Deadline reminder"),
        "ts": ctx.get("ts")
    })
    return ctx

def build_reminder_flow():
    g = StateGraph(dict)
    g.add_node("load_targets", load_targets)
    g.add_node("send_reminders", send_reminders)
    g.set_entry_point("load_targets")
    g.add_edge("load_targets", "send_reminders")
    g.set_finish_point("send_reminders")
    return g.compile()