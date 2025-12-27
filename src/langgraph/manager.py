from src.langgraph.flows.judge_flow import build_judge_flow
from src.langgraph.flows.mentor_flow import build_mentor_flow
from src.langgraph.flows.reminder_flow import build_reminder_flow
from src.langgraph.flows.team_registration_flow import build_team_registration_flow

FLOW_REGISTRY = {
    "judge": build_judge_flow(),
    "mentor": build_mentor_flow(),
    "reminder": build_reminder_flow(),
    "team_registration": build_team_registration_flow(),
}

def get_flow(name: str):
    return FLOW_REGISTRY.get(name)