#!/usr/bin/env python3
"""
Script to verify the security fixes for CORS and Authentication issues.
"""

import os
import sys
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
    
    # Check main.py for auth functions
    with open('src/main.py', 'r') as f:
        content = f.read()
        
    if 'get_api_key' in content:
        print("✅ API key authentication function found in main.py")
    else:
        print("❌ API key authentication function missing from main.py")
        
    if 'APIKeyHeader' in content:
        print("✅ APIKeyHeader import found in main.py")
    else:
        print("❌ APIKeyHeader import missing from main.py")
        
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

def main():
    """Main verification function"""
    print("Verifying security fixes implementation...\n")
    
    verify_env_vars()
    verify_cors_implementation()
    verify_auth_implementation()
    verify_docs_updated()
    
    print("\nVerification complete!")

if __name__ == "__main__":
    main()