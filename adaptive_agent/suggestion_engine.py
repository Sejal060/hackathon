# adaptive_agent/suggestion_engine.py
import numpy as np
from typing import Dict, Any, Optional
from rl_engine import RLEngine
from .storage import load_weights

rl_engine = RLEngine(agent_name="adaptive_feedback", epsilon=0.1, alpha=0.1)

def initialize_rl():
    """Initialize RL with suggestions as actions."""
    df = load_weights()
    if df.empty:
        return
    actions = df["suggestion_id"].tolist()
    rl_engine.register_actions(actions)

def choose_suggestion(context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    initialize_rl()
    if not rl_engine.actions:
        return None
    state = rl_engine.get_state(context)
    action = rl_engine.choose_action(state)
    df = load_weights()
    row = df[df["suggestion_id"] == action].iloc[0]
    return {"suggestion_id": action, "text": row["text"], "weight": float(row["weight"])}

# Call initialize_rl() on module load
initialize_rl()