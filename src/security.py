"""
Security utilities for the HackaVerse platform
"""
import time
from fastapi import Header, HTTPException
import os, hmac, hashlib
from datetime import datetime
import json
import base64
from typing import Dict, Any, Optional


class SecurityManager:
    def __init__(self):
        self.nonces = set()  # In production, use Redis or DB
        self.api_secret = os.getenv("API_SECRET", "default_secret_for_dev")
    
    def verify_nonce(self, nonce: str) -> bool:
        """
        Verify that the nonce hasn't been used before
        
        Args:
            nonce: The nonce to verify
            
        Returns:
            True if nonce is valid and unused, False otherwise
        """
        if nonce in self.nonces:
            return False
        self.nonces.add(nonce)
        return True
    
    def verify_signature(self, data: Dict[str, Any], nonce: str, timestamp: int, signature: str) -> bool:
        """
        Verify the signature using the provided data, nonce, and timestamp
        
        Args:
            data: Request data
            nonce: Nonce value
            timestamp: Request timestamp
            signature: Expected signature
            
        Returns:
            True if signature is valid, False otherwise
        """
        # Create signature string
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        message = f"{data_str}{nonce}{timestamp}".encode('utf-8')
        
        # Calculate expected signature
        expected_signature = base64.b64encode(
            hmac.new(
                self.api_secret.encode('utf-8'), 
                message, 
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        return hmac.compare_digest(expected_signature, signature)
    
    def add_to_ledger(self, data: Dict[str, Any], nonce: str, timestamp: int, signature: str) -> Dict[str, Any]:
        """
        Add security information to the ledger for audit purposes
        
        Args:
            data: Request data
            nonce: Nonce value
            timestamp: Request timestamp
            signature: Signature
            
        Returns:
            Ledger entry
        """
        from .database import get_db
        db = get_db()

        entry = {
            "data": data,
            "nonce": nonce,
            "timestamp": timestamp,
            "signature": signature,
            "created_at": datetime.now().isoformat()
        }

        # In production, store this in a security ledger
        result = db.security_ledger.insert_one(entry)

        return {
            "id": str(result.inserted_id),
            "timestamp": timestamp
        }

# Create a global security manager instance
security_manager = SecurityManager()


SECRET = os.getenv("SIGNING_SECRET", "dev-secret")

def current_minutes():
    return int(time.time() // 60)

def verify_nonce_only(
    x_nonce: str = Header(None, alias="X-Nonce"),
    x_timestamp: str = Header(None, alias="X-Timestamp"),
    x_signature: str = Header(None, alias="X-Signature"),
):
    if os.getenv("SKIP_NONCE") == "true":
        return "bypassed"

    if not x_nonce:
        raise HTTPException(status_code=400, detail="Missing X-Nonce header")
    if not x_timestamp:
        raise HTTPException(status_code=400, detail="Missing X-Timestamp header")
    if not x_signature:
        raise HTTPException(status_code=400, detail="Missing X-Signature header")

    try:
        ts = int(x_timestamp)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-Timestamp format")

    now = current_minutes()

    # Allow ±2 minutes skew
    if abs(now - ts) > 2:
        raise HTTPException(status_code=400, detail="Request timestamp is too old or in the future")

    # Validate signature based on minutes
    msg = f"{x_nonce}:{x_timestamp}".encode()
    expected = hmac.new(SECRET.encode(), msg, hashlib.sha256).hexdigest()

    if x_signature != expected:
        raise HTTPException(status_code=401, detail="Invalid X-Signature")

    return {"nonce": x_nonce, "timestamp": x_timestamp, "signature": x_signature}