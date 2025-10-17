import json
from datetime import datetime
import time

def reflect(module_name, trace_id, input_data, output_data, duration_ms=None, metrics=None):
    """
    Write a structured log entry to console and storage.

    Args:
        module_name (str): Name of the module generating the log
        trace_id (str): Unique ID for tracing this request
        input_data (dict): Input to the module
        output_data (dict): Output from the module
        duration_ms (float, optional): Duration of execution in milliseconds
        metrics (dict, optional): Any additional metrics
    """
    log_entry = {
        "module": module_name,
        "trace_id": trace_id,
        "input": input_data,
        "output": output_data,
        "duration_ms": duration_ms,
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Print to console
    print(json.dumps(log_entry, indent=2))

    # Persist to bucket (if storage_service is available)
    try:
        from storage_service import save_log  # adjust import to your service
        save_log(kind="reflection", payload=log_entry)
    except ImportError:
        # If storage_service not configured, skip saving
        pass