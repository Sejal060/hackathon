# adaptive_agent/tuner.py
from typing import Dict, Any, Optional

from rl_engine import RLEngine
from .storage import load_weights, save_weights, log_improvement

rl_engine = RLEngine(agent_name="adaptive_feedback")

def update_weight(suggestion_id: str, reward: int, context: Dict[str, Any], next_context: Optional[Dict[str, Any]] = None):
    df = load_weights()
    idx = df.index[df["suggestion_id"] == suggestion_id]
    if len(idx) == 0:
        return
    i = idx[0]
    prev = float(df.at[i, "weight"])
    state = rl_engine.get_state(context)
    next_state = rl_engine.get_state(next_context) if next_context else None
    rl_engine.update_q_value(state, suggestion_id, reward, next_state)
    new_w = rl_engine.q_table[state][suggestion_id]  # Sync with Q-value
    df.at[i, "weight"] = new_w
    save_weights(df)
    log_improvement(suggestion_id, prev, reward, new_w)