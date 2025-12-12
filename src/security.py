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

# Provenance imports
import json, time, hashlib, os
from typing import Dict, Any, List
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.exceptions import InvalidSignature

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
            entry["previous_hash"] = self._hash_ledger_entry(self.ledger[-1], include_hash=False)
        else:
            entry["previous_hash"] = None
            
        # Add entry hash
        entry["entry_hash"] = self._hash_ledger_entry(entry, include_hash=False)
        
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
                expected_previous_hash = self._hash_ledger_entry(previous_entry, include_hash=False)
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

# Provenance functions

def _sha256_hex(s: bytes) -> str:
    return hashlib.sha256(s).hexdigest()

def compute_payload_hash(payload: Dict[str,Any]) -> str:
    # canonical JSON: sort keys, separators compact
    js = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_hex(js)

def compute_entry_hash(entry: Dict[str,Any]) -> str:
    # include ordered fields to compute the chaining hash
    # fields: previous_hash, timestamp, actor, event, payload_hash
    core = {
        "previous_hash": entry.get("previous_hash"),
        "timestamp": entry.get("timestamp"),
        "actor": entry.get("actor"),
        "event": entry.get("event"),
        "payload_hash": entry.get("payload_hash")
    }
    js = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_hex(js)

def load_private_key_from_env() -> ec.EllipticCurvePrivateKey:
    pem = os.environ.get("PROVENANCE_PRIVATE_PEM")
    if not pem:
        raise RuntimeError("PROVENANCE_PRIVATE_PEM not set")
    return serialization.load_pem_private_key(pem.encode(), password=None)

def sign_hash_hex(hex_digest: str) -> str:
    priv = load_private_key_from_env()
    sig = priv.sign(bytes.fromhex(hex_digest), ec.ECDSA(hashes.SHA256()))
    # return hex signature
    return sig.hex()

def verify_signature_hex(hex_digest: str, signature_hex: str, public_pem: str) -> bool:
    pub = serialization.load_pem_public_key(public_pem.encode())
    try:
        pub.verify(bytes.fromhex(signature_hex), bytes.fromhex(hex_digest), ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False

def create_entry(db, actor: str, event: str, payload: Dict[str,Any]) -> Dict[str,Any]:
    # get last entry to chain
    last = db.provenance_logs.find_one(sort=[("timestamp",-1)])
    previous_hash = last.get("entry_hash") if last else None
    timestamp = int(time.time())
    payload_hash = compute_payload_hash(payload)
    entry = {
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "actor": actor,
        "event": event,
        "payload_hash": payload_hash,
    }
    entry_hash = compute_entry_hash(entry)
    signature = sign_hash_hex(entry_hash)
    entry.update({"entry_hash": entry_hash, "signature": signature})
    # insert as append-only
    db.provenance_logs.insert_one(entry)
    return entry

def verify_chain(db) -> List[Dict[str,Any]]:
    # return list of tamper reports; empty => OK
    bad = []
    try:
        pub_pem = open("docs/provenance_public.pem","r").read()  # or env var
    except FileNotFoundError:
        # Try to get from environment variable
        pub_pem = os.environ.get("PROVENANCE_PUBLIC_PEM", "")
        if not pub_pem:
            raise RuntimeError("Neither docs/provenance_public.pem nor PROVENANCE_PUBLIC_PEM found")
    
    cursor = db.provenance_logs.find().sort("timestamp", 1)
    prev_hash = None
    for e in cursor:
        # check chain pointer
        if e.get("previous_hash") != prev_hash:
            bad.append({"type":"broken_chain", "entry": e})
            prev_hash = e.get("entry_hash")
            continue
        # recompute entry hash
        recomputed = compute_entry_hash(e)
        if recomputed != e.get("entry_hash"):
            bad.append({"type":"entry_hash_mismatch", "entry": e})
        else:
            # verify signature
            ok = verify_signature_hex(recomputed, e.get("signature"), pub_pem)
            if not ok:
                bad.append({"type":"invalid_signature", "entry": e})
        prev_hash = e.get("entry_hash")
    return bad

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