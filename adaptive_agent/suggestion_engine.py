import numpy as np
from .storage import load_weights

def choose_suggestion(epsilon: float = 0.1):
    df = load_weights()
    if df.empty:
        return None
    if np.random.rand() < epsilon:
        row = df.sample(1).iloc[0]             # explore
    else:
        row = df.sort_values("weight", ascending=False).iloc[0]  # exploit
    return dict(suggestion_id=row["suggestion_id"], text=row["text"], weight=float(row["weight"]))
