"""
Security utilities for the HackaVerse platform
"""
from fastapi import Header, HTTPException
import os
from datetime import datetime
import time
import json
import hashlib
import hmac
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


def verify_nonce_only(x_nonce: str = Header(None, alias="X-Nonce")):
    """
    Verify only the X-Nonce header for simpler endpoints.
    
    Args:
        x_nonce: The X-Nonce header value
        
    Returns:
        The nonce value if valid
        
    Raises:
        HTTPException: If nonce is missing and not in test mode
    """
    # Allow bypass in test mode
    if os.getenv("SKIP_NONCE") == "true":
        return "bypassed"
    
    if not x_nonce:
        raise HTTPException(status_code=400, detail="Missing X-Nonce header")
    return x_nonce