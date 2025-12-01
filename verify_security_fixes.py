#!/usr/bin/env python3
"""
Script to verify the security fixes for CORS and Authentication issues.
"""

import os
import sys
import importlib
from dotenv import load_dotenv

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def verify_env_vars():
    """Verify that the new environment variables are documented"""
    print("Checking .env.example for security configurations...")
    
    with open('.env.example', 'r') as f:
        content = f.read()
        
    # Check for CORS configuration
    if 'ALLOWED_ORIGINS' in content:
        print("✅ ALLOWED_ORIGINS found in .env.example")
    else:
        print("❌ ALLOWED_ORIGINS missing from .env.example")
        
    # Check for API key configuration
    if 'API_KEY' in content:
        print("✅ API_KEY found in .env.example")
    else:
        print("❌ API_KEY missing from .env.example")
        
    # Check for security secret key configuration
    if 'SECURITY_SECRET_KEY' in content:
        print("✅ SECURITY_SECRET_KEY found in .env.example")
    else:
        print("❌ SECURITY_SECRET_KEY missing from .env.example")

def verify_cors_implementation():
    """Verify CORS implementation in main.py"""
    print("\nChecking CORS implementation...")
    
    with open('src/main.py', 'r') as f:
        content = f.read()
        
    # Check for CORS middleware with environment variable support
    if 'allowed_origins = os.getenv("ALLOWED_ORIGINS"' in content:
        print("✅ Dynamic CORS configuration found")
    else:
        print("❌ Dynamic CORS configuration missing")
        
    # Check for conditional CORS setup
    if 'if "*" in allowed_origins:' in content:
        print("✅ Conditional CORS setup found")
    else:
        print("❌ Conditional CORS setup missing")

def verify_auth_implementation():
    """Verify authentication implementation"""
    print("\nChecking authentication implementation...")
    
    # Check auth.py for auth functions
    with open('src/auth.py', 'r') as f:
        content = f.read()
        
    if 'get_api_key' in content:
        print("✅ API key authentication function found in auth.py")
    else:
        print("❌ API key authentication function missing from auth.py")
        
    if 'APIKeyHeader' in content:
        print("✅ APIKeyHeader import found in auth.py")
    else:
        print("❌ APIKeyHeader import missing from auth.py")
        
    # Check admin routes for auth dependencies
    with open('src/routes/admin.py', 'r') as f:
        content = f.read()
        
    if 'Depends(get_api_key)' in content:
        print("✅ Authentication dependencies found in admin routes")
    else:
        print("❌ Authentication dependencies missing from admin routes")
        
    # Check agent routes for auth dependencies
    with open('src/routes/agent.py', 'r') as f:
        content = f.read()
        
    if 'Depends(get_api_key)' in content:
        print("✅ Authentication dependencies found in agent routes")
    else:
        print("❌ Authentication dependencies missing from agent routes")

def verify_security_layer_implementation():
    """Verify security layer implementation"""
    print("\nChecking security layer implementation...")
    
    # Check security.py for required functions
    with open('src/security.py', 'r') as f:
        content = f.read()
        
    required_functions = [
        'generate_nonce',
        'verify_nonce',
        'sign_payload',
        'verify_signature'
    ]
    
    for func in required_functions:
        if f'def {func}' in content:
            print(f"✅ {func} function found in security.py")
        else:
            print(f"❌ {func} function missing from security.py")
            
    # Check middleware.py for security header validation
    with open('src/middleware.py', 'r') as f:
        content = f.read()
        
    required_headers = [
        'X-Nonce',
        'X-Signature',
        'X-Timestamp'
    ]
    
    for header in required_headers:
        if header in content:
            print(f"✅ {header} header validation found in middleware.py")
        else:
            print(f"❌ {header} header validation missing from middleware.py")
            
    # Check for nonce verification in middleware
    if 'verify_nonce' in content:
        print("✅ Nonce verification found in middleware.py")
    else:
        print("❌ Nonce verification missing from middleware.py")

def verify_ledger_implementation():
    """Verify ledger chaining implementation"""
    print("\nChecking ledger chaining implementation...")
    
    # Check storage_service.py for ledger implementation
    with open('src/storage_service.py', 'r') as f:
        content = f.read()
        
    required_ledger_features = [
        'previous_hash',
        'hash',
        'transaction_ledger'
    ]
    
    for feature in required_ledger_features:
        if feature in content:
            print(f"✅ {feature} found in storage_service.py")
        else:
            print(f"❌ {feature} missing from storage_service.py")

def verify_docs_updated():
    """Verify that API documentation was updated"""
    print("\nChecking API documentation updates...")
    
    with open('API_REFERENCE.md', 'r') as f:
        content = f.read()
        
    if 'Authentication' in content and 'X-API-Key' in content:
        print("✅ Authentication section updated in API_REFERENCE.md")
    else:
        print("❌ Authentication section not properly updated in API_REFERENCE.md")
        
    if 'CORS Configuration' in content:
        print("✅ CORS Configuration section found in API_REFERENCE.md")
    else:
        print("❌ CORS Configuration section missing from API_REFERENCE.md")
        
    # Check for security headers documentation
    security_headers = ['X-Nonce', 'X-Signature', 'X-Timestamp']
    for header in security_headers:
        if header in content:
            print(f"✅ {header} documented in API_REFERENCE.md")
        else:
            print(f"❌ {header} not documented in API_REFERENCE.md")

def main():
    """Main verification function"""
    print("Verifying security fixes implementation...\n")
    
    verify_env_vars()
    verify_cors_implementation()
    verify_auth_implementation()
    verify_security_layer_implementation()
    verify_ledger_implementation()
    verify_docs_updated()
    
    print("\nVerification complete!")

if __name__ == "__main__":
    main()