#!/usr/bin/env python3
"""
Test script for HackaVerse backend
Validates all major endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8001"
DEPLOYED_URL = "https://ai-agent-x2iw.onrender.com"

def test_root_endpoint(base_url):
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint: OK")
            return True
        else:
            print(f"❌ Root endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint: Error - {str(e)}")
        return False

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/system/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint: OK - Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint: Error - {str(e)}")
        return False

def test_ping_endpoint(base_url):
    """Test the ping endpoint"""
    print("Testing ping endpoint...")
    try:
        response = requests.get(f"{base_url}/ping")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ping endpoint: OK - Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Ping endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ping endpoint: Error - {str(e)}")
        return False

def test_agent_endpoint(base_url):
    """Test the agent endpoint"""
    print("Testing agent endpoint...")
    payload = {
        "team_id": "test_team",
        "prompt": "What is the meaning of life?",
        "metadata": {"test": True}
    }
    try:
        response = requests.post(f"{base_url}/agent/", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent endpoint: OK - Response: {data.get('result', 'no result')[:50]}...")
            return True
        else:
            print(f"❌ Agent endpoint: Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Agent endpoint: Error - {str(e)}")
        return False

def test_reward_endpoint(base_url):
    """Test the reward endpoint"""
    print("Testing reward endpoint...")
    payload = {
        "request_id": "test_request_123",
        "outcome": "success"
    }
    try:
        response = requests.post(f"{base_url}/admin/reward", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reward endpoint: OK - Reward: {data.get('reward_value', 'unknown')}")
            return True
        else:
            print(f"❌ Reward endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Reward endpoint: Error - {str(e)}")
        return False

def test_registration_endpoint(base_url):
    """Test the registration endpoint"""
    print("Testing registration endpoint...")
    payload = {
        "team_name": "Test Team",
        "members": ["Alice", "Bob"],
        "project_title": "Test Project"
    }
    try:
        response = requests.post(f"{base_url}/admin/register", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registration endpoint: OK - Message: {data.get('message', 'no message')}")
            return True
        else:
            print(f"❌ Registration endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Registration endpoint: Error - {str(e)}")
        return False

def test_webhook_registration_endpoint(base_url):
    """Test the webhook registration endpoint"""
    print("Testing webhook registration endpoint...")
    payload = {
        "team_name": "Webhook Test Team",
        "members": ["Charlie", "Diana"],
        "project_title": "Webhook Test Project"
    }
    try:
        response = requests.post(f"{base_url}/admin/webhook/hackaverse/registration", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook registration endpoint: OK - Status: {data.get('status', 'no status')}")
            return True
        else:
            print(f"❌ Webhook registration endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Webhook registration endpoint: Error - {str(e)}")
        return False

def test_logs_endpoint(base_url):
    """Test the logs endpoint"""
    print("Testing logs endpoint...")
    payload = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": "Test log entry from validation script"
    }
    try:
        response = requests.post(f"{base_url}/admin/logs", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logs endpoint: OK - Status: {data.get('status', 'no status')}")
            return True
        else:
            print(f"❌ Logs endpoint: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logs endpoint: Error - {str(e)}")
        return False

def run_all_tests(base_url):
    """Run all tests and return overall result"""
    print(f"Running tests against {base_url}")
    print("=" * 50)
    
    tests = [
        test_root_endpoint,
        test_health_endpoint,
        test_ping_endpoint,
        test_agent_endpoint,
        test_reward_endpoint,
        test_registration_endpoint,
        test_webhook_registration_endpoint,
        test_logs_endpoint
    ]
    
    results = []
    for test in tests:
        result = test(base_url)
        results.append(result)
        # Small delay between tests
        time.sleep(0.5)
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    # Test local deployment
    print("Testing local deployment...")
    local_result = run_all_tests(BASE_URL)
    
    print("\n" + "=" * 50)
    
    # Test deployed version (if accessible)
    print("Testing deployed version...")
    deployed_result = run_all_tests(DEPLOYED_URL)
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Local: {'✅ PASS' if local_result else '❌ FAIL'}")
    print(f"Deployed: {'✅ PASS' if deployed_result else '❌ FAIL'}")