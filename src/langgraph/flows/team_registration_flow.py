from langgraph.graph import StateGraph
from typing import Dict, Any
import logging
from src.database import get_db
from src.logger import KSMLLogger
import os

logger = logging.getLogger(__name__)
ksml_logger = KSMLLogger()

async def validate_registration(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Validate registration data
    team_name = ctx.get("team_name", "")
    members = ctx.get("members", [])
    
    if not team_name:
        raise ValueError("Team name is required")
    
    if not members or len(members) == 0:
        raise ValueError("At least one team member is required")
    
    return ctx

async def register_team(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Register the team in the database
    db = get_db()
    
    team_data = {
        "team_name": ctx.get("team_name", ""),
        "members": ctx.get("members", []),
        "project_title": ctx.get("project_title", ""),
        "registered_at": ctx.get("timestamp"),
        "active": True
    }
    
    result = db.teams.insert_one(team_data)
    ctx["team_id"] = str(result.inserted_id)
    
    return ctx

async def log_registration(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Log the registration event
    ksml_logger.log_registration(
        team_name=ctx.get("team_name", ""),
        project_title=ctx.get("project_title", ""),
        team_id=ctx.get("team_id", "")
    )
    return ctx

def build_team_registration_flow():
    g = StateGraph(dict)
    g.add_node("validate_registration", validate_registration)
    g.add_node("register_team", register_team)
    g.add_node("log_registration", log_registration)
    g.set_entry_point("validate_registration")
    g.add_edge("validate_registration", "register_team")
    g.add_edge("register_team", "log_registration")
    g.set_finish_point("log_registration")
    return g.compile()