from langgraph.graph import StateGraph
import httpx, logging
from src.database import get_db
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)

async def fetch_teams(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Fetch teams based on deadline config
    db = get_db()
    deadline_config = ctx.get("deadline_config", {})
    
    # Determine which teams need reminders based on the deadline config
    teams = list(db.teams.find({"registered": True}))
    ctx["teams"] = teams
    return ctx

async def send_reminders(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Send reminders to teams
    teams = ctx.get("teams", [])
    message = ctx.get("message", "Deadline reminder")
    
    # Send reminder to each team (using HTTP client)
    notifier_url = ctx.get("NOTIFIER_URL", os.environ.get("NOTIFIER_URL", "http://localhost:8001"))
    
    for team in teams:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(f"{notifier_url}/notify/reminder", json={
                    "team_id": team.get("_id"),
                    "message": message,
                    "deadline": ctx.get("deadline_config", {}).get("deadline")
                })
            logger.info(f"Reminder sent to team {team.get('team_name', team.get('_id'))}")
        except Exception as e:
            logger.error(f"Failed to send reminder to team: {str(e)}")
    
    return ctx

async def log_delivery(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Log delivery of reminders
    db = get_db()
    
    # Create a log entry for the reminder delivery
    log_entry = {
        "teams_count": len(ctx.get("teams", [])),
        "message": ctx.get("message", "Deadline reminder"),
        "deadline_config": ctx.get("deadline_config"),
        "sent_at": ctx.get("timestamp"),
        "status": "sent"
    }
    
    db.reminder_logs.insert_one(log_entry)
    return ctx

def build_reminder_flow():
    g = StateGraph(dict)
    g.add_node("fetch_teams", fetch_teams)
    g.add_node("send_reminders", send_reminders)
    g.add_node("log_delivery", log_delivery)
    g.set_entry_point("fetch_teams")
    g.add_edge("fetch_teams", "send_reminders")
    g.add_edge("send_reminders", "log_delivery")
    g.set_finish_point("log_delivery")
    return g.compile()