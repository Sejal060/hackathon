from .storage import load_weights, save_weights, log_improvement

def clamp(x, lo=-1.0, hi=1.0):
    return max(lo, min(hi, x))

def update_weight(suggestion_id: str, reward: int, alpha: float = 0.1):
    df = load_weights()
    idx = df.index[df["suggestion_id"] == suggestion_id]
    if len(idx) == 0:
        return
    i = idx[0]
    prev = float(df.at[i, "weight"])
    newv = clamp(prev + alpha * reward)
    df.at[i, "weight"] = newv
    save_weights(df)
    log_improvement(suggestion_id, prev, reward, newv)
