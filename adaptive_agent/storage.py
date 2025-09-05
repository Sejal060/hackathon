# adaptive_agent/storage.py
import csv
import datetime
import logging
from pathlib import Path
from typing import Union

import pandas as pd

logger = logging.getLogger(__name__)

# Resolve data directory relative to project root (one level up from this file)
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
WEIGHTS_CSV = DATA_DIR / "weights.csv"
FEEDBACK_CSV = DATA_DIR / "feedback.csv"
IMPROVE_CSV = DATA_DIR / "improvement_log.csv"

DEFAULT_TEMPLATES = [
    ("SUG-1", "Try a 25-minute focused study sprint, then 5-minute break.", 0.0),
    ("SUG-2", "Plan tomorrow’s top 3 tasks tonight.", 0.0),
    ("SUG-3", "If stuck, switch to an easier sub-task for 10 minutes.", 0.0),
    # Add more production templates based on hackathon feedback
    ("SUG-4", "Review your code for bugs and optimize for performance.", 0.0),
    ("SUG-5", "Get feedback from a teammate on your current progress.", 0.0),
]

WEIGHTS_HEADERS = ["suggestion_id", "text", "weight"]
FEEDBACK_HEADERS = ["timestamp", "suggestion_id", "user_text", "suggestion_text", "feedback"]
IMPROVE_HEADERS = ["timestamp", "suggestion_id", "prev_weight", "reward", "new_weight"]


def _ensure_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _timezone_aware_utc_iso() -> str:
    # ISO 8601 with timezone info (Z indicates UTC)
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _sanitize_csv_field(value: Union[str, None]) -> str:
    """Mitigate CSV/Excel formula injection by prefixing risky values.

    If the value starts with one of (=, +, -, @), prefix with a single quote.
    """
    if value is None:
        return ""
    s = str(value)
    if s and s[0] in ("=", "+", "-", "@"):
        return "'" + s
    return s


# Optional cross-process file locking if portalocker is available
try:
    import portalocker  # type: ignore

    _HAVE_PORTALOCKER = True
except Exception:  # pragma: no cover - optional dependency
    portalocker = None
    _HAVE_PORTALOCKER = False


def _append_row_csv(path: Path, row: list) -> None:
    """Append a single CSV row with optional file locking."""
    _ensure_dir()
    try:
        if _HAVE_PORTALOCKER:
            with open(path, "a", newline="", encoding="utf-8") as f:
                portalocker.lock(f, portalocker.LOCK_EX)
                csv.writer(f).writerow(row)
                f.flush()
                portalocker.unlock(f)
        else:
            with open(path, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)
    except Exception:
        # Let caller handle logging so context is preserved
        raise


def _init_csvs() -> None:
    _ensure_dir()

    if not WEIGHTS_CSV.exists():
        try:
            with open(WEIGHTS_CSV, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(WEIGHTS_HEADERS)
                for sid, txt, wt in DEFAULT_TEMPLATES:
                    w.writerow([sid, _sanitize_csv_field(txt), wt])
        except Exception:
            logger.exception("Failed to initialize weights CSV")

    if not FEEDBACK_CSV.exists():
        try:
            with open(FEEDBACK_CSV, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(FEEDBACK_HEADERS)
        except Exception:
            logger.exception("Failed to initialize feedback CSV")

    if not IMPROVE_CSV.exists():
        try:
            with open(IMPROVE_CSV, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(IMPROVE_HEADERS)
        except Exception:
            logger.exception("Failed to initialize improvement CSV")


def load_weights() -> pd.DataFrame:
    try:
        _init_csvs()
        df = pd.read_csv(WEIGHTS_CSV)
        logger.info(f"Loaded {len(df)} weights")
        return df
    except Exception:
        logger.exception("Failed to load weights")
        return pd.DataFrame(columns=WEIGHTS_HEADERS)


def save_weights(df: pd.DataFrame) -> None:
    try:
        _ensure_dir()
        df.to_csv(WEIGHTS_CSV, index=False)
        logger.info("Weights saved")
    except Exception:
        logger.exception("Failed to save weights")


def log_feedback(suggestion_id: str, user_text: str, suggestion_text: str, reward: Union[int, float]) -> None:
    try:
        _init_csvs()
        ts = _timezone_aware_utc_iso()
        row = [
            ts,
            suggestion_id,
            _sanitize_csv_field(user_text),
            _sanitize_csv_field(suggestion_text),
            reward,
        ]
        _append_row_csv(FEEDBACK_CSV, row)
        logger.info(f"Logged feedback for {suggestion_id} with reward {reward}")
    except Exception:
        logger.exception("Failed to log feedback")


def log_improvement(suggestion_id: str, prev_w: float, reward: Union[int, float], new_w: float) -> None:
    try:
        _init_csvs()
        ts = _timezone_aware_utc_iso()
        row = [ts, suggestion_id, prev_w, reward, new_w]
        _append_row_csv(IMPROVE_CSV, row)
        logger.info(f"Logged improvement for {suggestion_id}")
    except Exception:
        logger.exception("Failed to log improvement")


def load_feedback() -> pd.DataFrame:
    try:
        _init_csvs()
        return pd.read_csv(FEEDBACK_CSV)
    except Exception:
        logger.exception("Failed to load feedback")
        return pd.DataFrame(columns=FEEDBACK_HEADERS)


def load_improvements() -> pd.DataFrame:
    try:
        _init_csvs()
        return pd.read_csv(IMPROVE_CSV)
    except Exception:
        logger.exception("Failed to load improvements")
        return pd.DataFrame(columns=IMPROVE_HEADERS)
