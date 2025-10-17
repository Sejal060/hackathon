# src/core_connector.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BHIV_CORE_URL = os.getenv("BHIV_CORE_URL")  # e.g., https://core.example/api

def send_for_reasoning(payload: dict):
    """
    Send data to BHIV Core for reasoning and return response.
    """
    if not BHIV_CORE_URL:
        raise ValueError("BHIV_CORE_URL not set")

    try:
        r = requests.post(f"{BHIV_CORE_URL}/reason", json=payload, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error calling BHIV Core: {e}")
        return None