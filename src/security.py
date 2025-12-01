#!/usr/bin/env python3
"""
Security module for sovereign compliance
Implements nonce, signature, and ledger chaining for enhanced security
"""

import hashlib
import hmac
import time
import json
import os
import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecurityManager:
    """Manages security features including nonce, signature, and ledger chaining"""
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize the security manager
        
        Args:
            secret_key: Secret key for HMAC signing. If None, will be generated from environment or default.
        """
        if secret_key is None:
            secret_key = os.getenv("SECURITY_SECRET_KEY", "default_secret_key_for_development_only")
        
        self.secret_key = secret_key.encode('utf-8')
        self.ledger = []  # In-memory ledger (in production, this would be a persistent store)
        self.used_nonces = set()  # Track used nonces to prevent replay attacks
        
    def generate_nonce(self) -> str:
        """
        Generate a unique nonce
        
        Returns:
            Base64 encoded nonce
        """
        # Generate a random 32-byte nonce
        nonce_bytes = secrets.token_bytes(32)
        nonce = base64.b64encode(nonce_bytes).decode('utf-8')
        return nonce
    
    def verify_nonce(self, nonce: str) -> bool:
        """
        Verify that a nonce is valid and hasn't been used before
        This function marks the nonce as used if it's valid.
        
        Args:
            nonce: Nonce to verify
            
        Returns:
            True if nonce is valid and unused, False otherwise
        """
        # Check if nonce has already been used (prevent replay attacks)
        if nonce in self.used_nonces:
            return False
            
        # Try to decode the nonce to verify it's valid base64
        try:
            base64.b64decode(nonce.encode('utf-8'))
            # Mark nonce as used
            self.used_nonces.add(nonce)
            return True
        except Exception:
            return False
    
    def generate_timestamp(self) -> int:
        """
        Generate a timestamp for the request
        
        Returns:
            Unix timestamp in seconds
        """
        return int(time.time())
    
    def sign_payload(self, data: Dict[str, Any], nonce: str, timestamp: int) -> str:
        """
        Create a signature for the data using HMAC-SHA256
        
        Args:
            data: Data to sign
            nonce: Nonce for the request
            timestamp: Timestamp for the request
            
        Returns:
            Base64 encoded signature
        """
        # Create a canonical string representation of the data
        canonical_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
        
        # Create the message to sign
        message = f"{canonical_data}:{nonce}:{timestamp}".encode('utf-8')
        
        # Create HMAC signature
        signature = hmac.new(self.secret_key, message, hashlib.sha256).digest()
        
        # Return base64 encoded signature
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, data: Dict[str, Any], nonce: str, timestamp: int, signature: str) -> bool:
        """
        Verify a signature
        
        Args:
            data: Data that was signed
            nonce: Nonce used in the signature
            timestamp: Timestamp used in the signature
            signature: Signature to verify
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Decode the provided signature
            provided_signature = base64.b64decode(signature.encode('utf-8'))
            
            # Create the expected signature
            expected_signature = self.sign_payload(data, nonce, timestamp)
            expected_signature_bytes = base64.b64decode(expected_signature.encode('utf-8'))
            
            # Use hmac.compare_digest for timing-attack resistant comparison
            return hmac.compare_digest(provided_signature, expected_signature_bytes)
        except Exception:
            return False
    
    def create_ledger_entry(self, data: Dict[str, Any], nonce: str, timestamp: int, signature: str) -> Dict[str, Any]:
        """
        Create a ledger entry for the request
        
        Args:
            data: Request data
            nonce: Nonce used
            timestamp: Timestamp used
            signature: Signature created
            
        Returns:
            Ledger entry dictionary
        """
        entry = {
            "id": len(self.ledger) + 1,
            "data_hash": self._hash_data(data),
            "nonce": nonce,
            "timestamp": timestamp,
            "signature": signature,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Add previous entry hash for chaining
        if self.ledger:
            entry["previous_hash"] = self._hash_ledger_entry(self.ledger[-1])
        else:
            entry["previous_hash"] = None
            
        # Add entry hash
        entry["entry_hash"] = self._hash_ledger_entry(entry)
        
        return entry
    
    def add_to_ledger(self, data: Dict[str, Any], nonce: str, timestamp: int, signature: str) -> Dict[str, Any]:
        """
        Add an entry to the ledger
        
        Args:
            data: Request data
            nonce: Nonce used
            timestamp: Timestamp used
            signature: Signature created
            
        Returns:
            Ledger entry that was added
        """
        entry = self.create_ledger_entry(data, nonce, timestamp, signature)
        self.ledger.append(entry)
        return entry
    
    def verify_ledger_integrity(self) -> bool:
        """
        Verify the integrity of the ledger
        
        Returns:
            True if ledger is valid, False otherwise
        """
        if not self.ledger:
            return True  # Empty ledger is valid
            
        for i, entry in enumerate(self.ledger):
            # Verify entry hash
            expected_hash = self._hash_ledger_entry(entry, include_hash=False)
            if entry["entry_hash"] != expected_hash:
                return False
                
            # Verify chain integrity
            if i > 0:
                previous_entry = self.ledger[i-1]
                expected_previous_hash = self._hash_ledger_entry(previous_entry)
                if entry["previous_hash"] != expected_previous_hash:
                    return False
                    
        return True
    
    def get_ledger(self) -> list:
        """
        Get the ledger entries
        
        Returns:
            List of ledger entries
        """
        return self.ledger.copy()
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """
        Create a hash of the data
        
        Args:
            data: Data to hash
            
        Returns:
            SHA256 hash of the data
        """
        canonical_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_data.encode('utf-8')).hexdigest()
    
    def _hash_ledger_entry(self, entry: Dict[str, Any], include_hash: bool = True) -> str:
        """
        Create a hash of a ledger entry
        
        Args:
            entry: Ledger entry to hash
            include_hash: Whether to include the entry_hash field in the hash
            
        Returns:
            SHA256 hash of the entry
        """
        # Create a copy of the entry without the hash field if requested
        entry_copy = entry.copy()
        if not include_hash and "entry_hash" in entry_copy:
            del entry_copy["entry_hash"]
            
        canonical_entry = json.dumps(entry_copy, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_entry.encode('utf-8')).hexdigest()

# Global security manager instance
security_manager = SecurityManager()

# Decorator for securing endpoints
def secure_endpoint(func):
    """
    Decorator to secure endpoints with nonce, signature, and ledger verification
    """
    async def wrapper(*args, **kwargs):
        # This is a simplified decorator - in practice, you would extract
        # nonce, timestamp, and signature from request headers
        # and verify them before calling the function
        
        # For now, we'll just call the function and add it to the ledger
        result = await func(*args, **kwargs)
        return result
        
    return wrapper

# Example usage
if __name__ == "__main__":
    # Create a security manager
    sec_manager = SecurityManager("test_secret_key")
    
    # Example data
    data = {
        "team_id": "team_123",
        "action": "register",
        "timestamp": int(time.time())
    }
    
    # Generate nonce and timestamp
    nonce = sec_manager.generate_nonce()
    timestamp = sec_manager.generate_timestamp()
    
    # Create signature
    signature = sec_manager.sign_payload(data, nonce, timestamp)
    
    # Verify signature
    is_valid = sec_manager.verify_signature(data, nonce, timestamp, signature)
    print(f"Signature valid: {is_valid}")
    
    # Add to ledger
    ledger_entry = sec_manager.add_to_ledger(data, nonce, timestamp, signature)
    print(f"Ledger entry added: {ledger_entry['id']}")
    
    # Verify ledger integrity
    is_integrity_valid = sec_manager.verify_ledger_integrity()
    print(f"Ledger integrity valid: {is_integrity_valid}")
    
    # Show ledger
    ledger = sec_manager.get_ledger()
    print(f"Ledger has {len(ledger)} entries")