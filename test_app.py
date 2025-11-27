#!/usr/bin/env python3
"""
Test script to verify the application can start correctly
"""

import os
import sys
import time
import subprocess
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all modules can be imported without errors"""
    print("Testing imports...")
    
    try:
        from src.main import app
        print("✓ Main app imported successfully")
    except Exception as e:
        print(f"✗ Failed to import main app: {e}")
        return False
    
    try:
        from src.routes.agent import router as agent_router
        print("✓ Agent router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import agent router: {e}")
        return False
        
    try:
        from src.routes.admin import router as admin_router
        print("✓ Admin router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import admin router: {e}")
        return False
        
    try:
        from src.routes.system import router as system_router
        print("✓ System router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import system router: {e}")
        return False
        
    try:
        from src.routes.judge import router as judge_router
        print("✓ Judge router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import judge router: {e}")
        return False
        
    return True

def test_env_vars():
    """Test that required environment variables are set"""
    print("\nTesting environment variables...")
    
    required_vars = ["API_KEY"]
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

def test_startup():
    """Test that the application can start"""
    print("\nTesting application startup...")
    
    try:
        # Start the server in the background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8001",
            "--log-level", "warning"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"✗ Application failed to start:")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            return False
            
        # Try to make a request to the health endpoint
        try:
            response = requests.get("http://127.0.0.1:8001/system/health", timeout=5)
            if response.status_code == 200:
                print("✓ Application started successfully and health endpoint responded")
                return True
            else:
                print(f"✗ Health endpoint returned status code {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to reach health endpoint: {e}")
            return False
        finally:
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                
    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        return False

def main():
    """Run all tests"""
    print("Running application tests...\n")
    
    tests = [
        test_imports,
        test_env_vars,
        test_startup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("Test failed, stopping further tests")
            break
            
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)