import os, csv, datetime, pandas as pd

DATA_DIR = "data"
WEIGHTS_CSV = os.path.join(DATA_DIR, "weights.csv")
FEEDBACK_CSV = os.path.join(DATA_DIR, "feedback.csv")
IMPROVE_CSV = os.path.join(DATA_DIR, "improvement_log.csv")

DEFAULT_TEMPLATES = [
    ("SUG-1", "Try a 25-minute focused study sprint, then 5-minute break.", 0.0),
    ("SUG-2", "Plan tomorrow’s top 3 tasks tonight.", 0.0),
    ("SUG-3", "If stuck, switch to an easier sub-task for 10 minutes.", 0.0),
]

def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _init_csvs():
    _ensure_dir()
    if not os.path.exists(WEIGHTS_CSV):
        with open(WEIGHTS_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["suggestion_id","text","weight"])
            for sid, txt, wt in DEFAULT_TEMPLATES: w.writerow([sid, txt, wt])
    if not os.path.exists(FEEDBACK_CSV):
        with open(FEEDBACK_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["timestamp","suggestion_id","user_text","suggestion_text","feedback"])
    if not os.path.exists(IMPROVE_CSV):
        with open(IMPROVE_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["timestamp","suggestion_id","prev_weight","reward","new_weight"])

def load_weights() -> pd.DataFrame:
    _init_csvs()
    return pd.read_csv(WEIGHTS_CSV)

def save_weights(df: pd.DataFrame):
    df.to_csv(WEIGHTS_CSV, index=False)

def log_feedback(suggestion_id, user_text, suggestion_text, reward: int):
    _init_csvs()
    ts = datetime.datetime.utcnow().isoformat()
    with open(FEEDBACK_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, suggestion_id, user_text, suggestion_text, reward])

def log_improvement(suggestion_id, prev_w, reward, new_w):
    _init_csvs()
    ts = datetime.datetime.utcnow().isoformat()
    with open(IMPROVE_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, suggestion_id, prev_w, reward, new_w])

def load_feedback() -> pd.DataFrame:
    _init_csvs()
    return pd.read_csv(FEEDBACK_CSV)

def load_improvements() -> pd.DataFrame:
    _init_csvs()
    return pd.read_csv(IMPROVE_CSV)
