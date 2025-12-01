#!/usr/bin/env python3
"""
Security middleware for FastAPI
Integrates nonce, signature, and ledger chaining for enhanced security
"""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Optional, Dict, Any
import json
import base64
import time

from .security import security_manager

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware to handle security features"""
    
    async def dispatch(self, request: Request, call_next):
        """
        Process incoming requests with security checks
        """
        # Skip security checks for certain endpoints (health checks, docs, etc.)
        skip_paths = ["/system/health", "/ping", "/docs", "/redoc", "/openapi.json"]
        if request.url.path in skip_paths:
            return await call_next(request)
        
        # Check if this is an administrative endpoint that requires additional security
        if self._requires_advanced_security(request):
            try:
                # Perform security checks
                await self._perform_security_checks(request)
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={"detail": f"Security validation failed: {str(e)}"}
                )
        
        # Continue with the request
        response = await call_next(request)
        return response
    
    def _requires_advanced_security(self, request: Request) -> bool:
        """
        Determine if a request requires advanced security checks
        
        Args:
            request: Incoming request
            
        Returns:
            True if advanced security is required, False otherwise
        """
        # Require advanced security for administrative endpoints
        admin_paths = ["/admin/", "/agent/", "/judge/"]
        for path in admin_paths:
            if request.url.path.startswith(path):
                return True
        return False
    
    async def _perform_security_checks(self, request: Request):
        """
        Perform security checks on the request
        
        Args:
            request: Incoming request
        """
        # Extract security headers
        nonce = request.headers.get("X-Nonce")
        timestamp = request.headers.get("X-Timestamp")
        signature = request.headers.get("X-Signature")
        
        # Validate required headers
        if not nonce:
            raise HTTPException(status_code=400, detail="Missing X-Nonce header")
        
        if not timestamp:
            raise HTTPException(status_code=400, detail="Missing X-Timestamp header")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing X-Signature header")
        
        # Validate timestamp (should be within 5 minutes)
        try:
            request_time = int(timestamp)
            current_time = int(time.time())
            time_diff = abs(current_time - request_time)
            
            if time_diff > 300:  # 5 minutes
                raise HTTPException(status_code=400, detail="Request timestamp is too old or in the future")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid timestamp format")
        
        # Verify nonce
        if not security_manager.verify_nonce(nonce):
            raise HTTPException(status_code=400, detail="Invalid or reused nonce")
        
        # Get request body for signature verification
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            try:
                data = json.loads(body.decode('utf-8')) if body else {}
            except json.JSONDecodeError:
                data = {}
        else:
            # For GET requests, use query parameters
            data = dict(request.query_params)
        
        # Verify signature
        is_valid = security_manager.verify_signature(data, nonce, request_time, signature)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Add to ledger
        ledger_entry = security_manager.add_to_ledger(data, nonce, request_time, signature)
        
        # Store security info in request state for use in endpoints
        request.state.security_info = {
            "nonce": nonce,
            "timestamp": request_time,
            "signature": signature,
            "ledger_entry_id": ledger_entry["id"]
        }

# Security header dependencies for specific endpoints
async def get_security_headers(
    nonce: Optional[str] = None,
    timestamp: Optional[str] = None,
    signature: Optional[str] = None
) -> Dict[str, Any]:
    """
    Dependency to extract security headers
    
    Args:
        nonce: Nonce header
        timestamp: Timestamp header
        signature: Signature header
        
    Returns:
        Dictionary with security headers
    """
    return {
        "nonce": nonce,
        "timestamp": timestamp,
        "signature": signature
    }

# Example of how to use security in an endpoint
def secure_endpoint_dependency():
    """
    Dependency for securing endpoints that require advanced security
    """
    def dependency(
        request: Request,
        security_headers: dict = Depends(get_security_headers)
    ):
        # This would be where you perform additional security checks
        # For now, we'll just pass through
        return security_headers
    
    return dependency