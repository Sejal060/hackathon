# src/storage_service.py
import os
import requests
import json

# Load environment variables if using .env
from dotenv import load_dotenv
load_dotenv()

BHIV_BUCKET_URL = os.getenv("BHIV_BUCKET_URL")  # e.g., https://bucket.example/api/upload
BHIV_API_KEY = os.getenv("BHIV_API_KEY")

def save_log(kind: str, payload: dict):
    """
    Send structured log to BHIV bucket.
    """
    if not BHIV_BUCKET_URL or not BHIV_API_KEY:
        print("BHIV_BUCKET_URL or BHIV_API_KEY not available")
        return None

    body = {"kind": kind, "payload": payload}
    headers = {"Authorization": f"Bearer {BHIV_API_KEY}"}

    try:
        resp = requests.post(BHIV_BUCKET_URL, json=body, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error sending log to BHIV bucket: {e}")
        return None