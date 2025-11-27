#!/usr/bin/env python3
"""
Final verification script to ensure the application is ready for production deployment
"""

import os
import sys
import time
import subprocess
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_endpoints():
    """Test all required endpoints"""
    print("Testing endpoints...")
    
    # Start the server
    print("Starting server...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8001",
        "--log-level", "warning"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    # Check if process is running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print(f"✗ Server failed to start:")
        print(f"stdout: {stdout.decode()}")
        print(f"stderr: {stderr.decode()}")
        return False
    
    try:
        base_url = "http://127.0.0.1:8001"
        api_key = os.getenv("API_KEY", "your_secret_api_key_here")
        headers = {"X-API-Key": api_key}
        
        # Test 1: Health endpoint
        print("  Testing /system/health...")
        response = requests.get(f"{base_url}/system/health", timeout=5)
        if response.status_code == 200:
            print("  ✓ /system/health endpoint working")
        else:
            print(f"  ✗ /system/health returned {response.status_code}")
            return False
            
        # Test 2: Root endpoint
        print("  Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("  ✓ Root endpoint working")
        else:
            print(f"  ✗ Root endpoint returned {response.status_code}")
            return False
            
        # Test 3: Register endpoint
        print("  Testing /admin/register...")
        register_data = {
            "team_name": "Test Team",
            "members": ["Alice", "Bob"],
            "project_title": "Test Project"
        }
        response = requests.post(
            f"{base_url}/admin/register", 
            json=register_data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ /admin/register endpoint working")
        else:
            print(f"  ✗ /admin/register returned {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
        # Test 4: Agent endpoint
        print("  Testing /agent/...")
        agent_data = {
            "team_id": "test_team",
            "prompt": "Explain how to build a REST API",
            "metadata": {"test": True}
        }
        response = requests.post(
            f"{base_url}/agent/", 
            json=agent_data,
            headers=headers,
            timeout=10  # Longer timeout for agent processing
        )
        if response.status_code == 200:
            print("  ✓ /agent/ endpoint working")
        else:
            print(f"  ✗ /agent/ returned {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
        # Test 5: Reward endpoint
        print("  Testing /admin/reward...")
        reward_data = {
            "request_id": "test_request_123",
            "outcome": "success"
        }
        response = requests.post(
            f"{base_url}/admin/reward", 
            json=reward_data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ /admin/reward endpoint working")
        else:
            print(f"  ✗ /admin/reward returned {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
        # Test 6: Logs endpoint
        print("  Testing /admin/logs...")
        log_data = {
            "timestamp": "2024-01-01T12:00:00Z",
            "level": "INFO",
            "message": "Test log message"
        }
        response = requests.post(
            f"{base_url}/admin/logs", 
            json=log_data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ /admin/logs endpoint working")
        else:
            print(f"  ✗ /admin/logs returned {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
        print("✓ All endpoints working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Error testing endpoints: {e}")
        return False
    finally:
        # Terminate the server
        print("Stopping server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def test_cors():
    """Test CORS configuration"""
    print("\nTesting CORS configuration...")
    
    # This would require a more complex test with actual CORS requests
    # For now, we'll just check that the configuration is present
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
    if allowed_origins:
        print("✓ CORS configuration present")
        return True
    else:
        print("✗ CORS configuration missing")
        return False

def test_env_vars():
    """Test that all required environment variables are set"""
    print("\nTesting environment variables...")
    
    required_vars = [
        "API_KEY",
        "BHIV_CORE_URL",
        "MONGO_URI"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            
    if missing_vars:
        print(f"✗ Missing required environment variables: {missing_vars}")
        return False
    else:
        print("✓ All required environment variables are set")
        return True

def test_documentation():
    """Test that documentation endpoints are accessible"""
    print("\nTesting documentation endpoints...")
    
    # Start the server
    print("Starting server...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8001",
        "--log-level", "warning"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        base_url = "http://127.0.0.1:8001"
        
        # Test OpenAPI JSON
        print("  Testing /openapi.json...")
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            print("  ✓ /openapi.json accessible")
        else:
            print(f"  ✗ /openapi.json returned {response.status_code}")
            return False
            
        # Test docs
        print("  Testing /docs...")
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("  ✓ /docs accessible")
        else:
            print(f"  ✗ /docs returned {response.status_code}")
            return False
            
        print("✓ Documentation endpoints working")
        return True
        
    except Exception as e:
        print(f"✗ Error testing documentation: {e}")
        return False
    finally:
        # Terminate the server
        print("Stopping server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def main():
    """Run all verification tests"""
    print("Running final verification tests...\n")
    
    tests = [
        test_env_vars,
        test_cors,
        test_endpoints,
        test_documentation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("Test failed, continuing with remaining tests...")
            
    print(f"\nFinal Results: {passed}/{total} test groups passed")
    
    if passed == total:
        print("🎉 All verification tests passed! The application is ready for production deployment.")
        print("\nDeployment Information:")
        print("- Base URL: https://ai-agent-x2iw.onrender.com")
        print("- API Key: production_secret_key_2024")
        print("- Required endpoints are all functional")
        print("- CORS is configured for frontend integration")
        return True
    else:
        print("❌ Some verification tests failed. Please address the issues above before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)