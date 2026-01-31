"""
Replay Protection Module

Provides basic demo-safe replay protection for hackathon APIs.
Uses in-memory storage with TTL (time-to-live) for seen request IDs.
Scoped by tenant_id + event_id to allow same request_id across different tenants/events.
"""

import time
import threading
from typing import Optional, Tuple
from collections import defaultdict


class ReplayProtection:
    """
    Simple in-memory replay protection with TTL.
    
    Features:
    - Scoped by (tenant_id, event_id, request_id)
    - TTL-based cleanup (default: 1 hour)
    - Thread-safe operations
    - Demo-safe (not bank-grade security)
    """
    
    def __init__(self, ttl_seconds: int = 3600, max_entries: int = 10000):
        """
        Initialize replay protection.
        
        Args:
            ttl_seconds: Time-to-live for stored request IDs (default: 1 hour)
            max_entries: Maximum number of entries to store before cleanup (default: 10000)
        """
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        # Store: {(tenant_id, event_id, request_id): timestamp}
        self._seen_requests: dict = {}
        self._lock = threading.Lock()
        self._cleanup_counter = 0
    
    def _cleanup_expired(self):
        """Remove expired entries. Called periodically."""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self._seen_requests.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        for key in expired_keys:
            del self._seen_requests[key]
    
    def _maybe_cleanup(self):
        """Trigger cleanup periodically based on entry count."""
        self._cleanup_counter += 1
        # Cleanup every 100 requests or when max entries reached
        if self._cleanup_counter >= 100 or len(self._seen_requests) > self.max_entries:
            self._cleanup_counter = 0
            self._cleanup_expired()
    
    def check_and_store(
        self,
        request_id: str,
        tenant_id: str = "default",
        event_id: str = "default_event"
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if request_id is a replay and store it if new.
        
        Args:
            request_id: The unique request identifier
            tenant_id: Tenant identifier for scoping
            event_id: Event identifier for scoping
            
        Returns:
            Tuple of (is_new, error_message)
            - is_new: True if this is a new request, False if it's a replay
            - error_message: None if new, descriptive message if replay
        """
        if not request_id:
            return True, None  # Empty request_id is treated as new (backward compatibility)
        
        # Create scoped key
        scoped_key = (tenant_id, event_id, request_id)
        current_time = time.time()
        
        with self._lock:
            self._maybe_cleanup()
            
            if scoped_key in self._seen_requests:
                # Check if expired
                stored_time = self._seen_requests[scoped_key]
                if current_time - stored_time <= self.ttl_seconds:
                    return False, f"Duplicate request detected: request_id '{request_id}' has already been processed for tenant '{tenant_id}' and event '{event_id}'"
                else:
                    # Expired, update timestamp
                    self._seen_requests[scoped_key] = current_time
                    return True, None
            else:
                # New request
                self._seen_requests[scoped_key] = current_time
                return True, None
    
    def is_duplicate(
        self,
        request_id: str,
        tenant_id: str = "default",
        event_id: str = "default_event"
    ) -> bool:
        """
        Check if request_id is a duplicate without storing it.
        
        Args:
            request_id: The unique request identifier
            tenant_id: Tenant identifier for scoping
            event_id: Event identifier for scoping
            
        Returns:
            True if duplicate, False otherwise
        """
        if not request_id:
            return False
        
        scoped_key = (tenant_id, event_id, request_id)
        current_time = time.time()
        
        with self._lock:
            if scoped_key in self._seen_requests:
                stored_time = self._seen_requests[scoped_key]
                return current_time - stored_time <= self.ttl_seconds
            return False
    
    def get_stats(self) -> dict:
        """Get current statistics for monitoring."""
        with self._lock:
            return {
                "total_stored_requests": len(self._seen_requests),
                "ttl_seconds": self.ttl_seconds,
                "max_entries": self.max_entries
            }


# Global instance for use across the application
replay_protection = ReplayProtection()


def check_replay(
    request_id: str,
    tenant_id: str = "default",
    event_id: str = "default_event"
) -> Tuple[bool, Optional[str]]:
    """
    Convenience function to check and store a request ID.
    
    Args:
        request_id: The unique request identifier
        tenant_id: Tenant identifier for scoping
        event_id: Event identifier for scoping
        
    Returns:
        Tuple of (is_new, error_message)
    """
    return replay_protection.check_and_store(request_id, tenant_id, event_id)
