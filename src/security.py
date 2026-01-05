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
from collections import defaultdict
import threading
from typing import Tuple


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)  # key -> list of timestamps
        self.lock = threading.Lock()

    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = time.time()
        with self.lock:
            # Clean old requests
            self.requests[key] = [t for t in self.requests[key] if current_time - t < window]
            # Check limit
            if len(self.requests[key]) >= limit:
                return False
            # Add current request
            self.requests[key].append(current_time)
            return True

class SecurityManager:
    def __init__(self):
        self.nonces = {}  # nonce -> expiry_time
        self.api_secret = os.getenv("SECURITY_SECRET_KEY", "default_secret_for_dev")
        self.rate_limiter = RateLimiter()
        self.lock = threading.Lock()

    def verify_nonce(self, nonce: str, timestamp: int) -> bool:
        """
        Verify that the nonce hasn't been used before within TTL

        Args:
            nonce: The nonce to verify
            timestamp: Request timestamp

        Returns:
            True if nonce is valid and unused, False otherwise
        """
        current_time = int(time.time())
        ttl = 300  # 5 minutes

        with self.lock:
            # Clean expired nonces
            expired = [n for n, exp in self.nonces.items() if current_time > exp]
            for n in expired:
                del self.nonces[n]

            # Check if timestamp is too old
            if current_time - timestamp > ttl:
                return False

            # Check if nonce exists and not expired
            if nonce in self.nonces:
                return False

            # Add nonce with expiry
            self.nonces[nonce] = current_time + ttl
            return True

    def verify_signature(self, timestamp: str, request_body: str, signature: str) -> bool:
        """
        Verify the signature using timestamp + request_body

        Args:
            timestamp: Request timestamp as string
            request_body: Raw request body
            signature: Expected signature

        Returns:
            True if signature is valid, False otherwise
        """
        message = f"{timestamp}{request_body}".encode('utf-8')

        # Calculate expected signature
        expected_signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

# Create a global security manager instance
security_manager = SecurityManager()


# API Key roles mapping
API_KEY_ROLES = {
    os.getenv("API_KEY", "default_key"): "admin",  # Default API key is admin
    # Add more mappings as needed, e.g.:
    # "agent_key_123": "agent",
    # "admin_key_456": "admin",
}

def get_api_key_role(api_key: str) -> Optional[str]:
    """Get role for API key"""
    return API_KEY_ROLES.get(api_key)

def validate_request_signing(x_timestamp: Optional[str], request_body: str, x_signature: Optional[str]) -> None:
    """Validate request signing if headers present"""
    if not x_signature:
        return  # Optional, allow request

    if not x_timestamp:
        raise HTTPException(status_code=400, detail="Missing X-Timestamp header when X-Signature provided")

    try:
        ts = int(x_timestamp)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-Timestamp format")

    if not security_manager.verify_signature(x_timestamp, request_body, x_signature):
        raise HTTPException(status_code=401, detail="Invalid X-Signature")

def validate_replay_protection(x_nonce: Optional[str], x_timestamp: Optional[str]) -> None:
    """Validate replay protection if headers present"""
    if not x_nonce:
        return  # Optional, allow request

    if not x_timestamp:
        raise HTTPException(status_code=400, detail="Missing X-Timestamp header when X-Nonce provided")

    try:
        ts = int(x_timestamp)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-Timestamp format")

    if not security_manager.verify_nonce(x_nonce, ts):
        raise HTTPException(status_code=409, detail="Invalid or reused nonce, or timestamp too old")

def check_rate_limit(api_key: str, path: str) -> None:
    """Check rate limiting for API key and path"""
    # 60 requests per minute per API key
    key = f"{api_key}:general"
    if not security_manager.rate_limiter.is_allowed(key, 60, 60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # 10 requests per minute for /admin routes
    if path.startswith("/admin"):
        admin_key = f"{api_key}:admin"
        if not security_manager.rate_limiter.is_allowed(admin_key, 10, 60):
            raise HTTPException(status_code=429, detail="Admin rate limit exceeded")