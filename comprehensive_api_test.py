#!/usr/bin/env python3
"""
Comprehensive test script for team registration API endpoint
This script tests multiple scenarios to identify the root cause of the 400 error
"""

import requests
import json
import sys
import time

def test_health_check():
    """Test basic health check"""
    print("=== Testing Health Check ===")
    try:
        response = requests.get("https://ai-agent-x2iw.onrender.com/ping", timeout=10)
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Check Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_workflows_health():
    """Test workflows health endpoint"""
    print("\n=== Testing Workflows Health ===")
    try:
        response = requests.get("https://ai-agent-x2iw.onrender.com/workflows/health", timeout=10)
        print(f"Workflows Health Status: {response.status_code}")
        print(f"Workflows Health Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Workflows Health Failed: {e}")
        return False

def test_list_workflows():
    """Test list workflows endpoint"""
    print("\n=== Testing List Workflows ===")
    try:
        response = requests.get("https://ai-agent-x2iw.onrender.com/workflows/list", timeout=10)
        print(f"List Workflows Status: {response.status_code}")
        print(f"List Workflows Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"List Workflows Failed: {e}")
        return False

def test_team_registration_scenarios():
    """Test team registration with different scenarios"""
    api_url = "https://ai-agent-x2iw.onrender.com/workflows/team-registration"
    api_key = "2b899caf7e3aea924c96761326bdded5162da31a9d1fdba59a2a451d2335c778"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    
    # Test 1: Minimal payload (only required fields)
    print("\n=== Test 1: Minimal Payload ===")
    minimal_payload = {
        "team_name": "Test Team",
        "members": ["Member1"],
        "project_title": "Test Project"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=minimal_payload, timeout=30)
        print(f"Minimal Payload Status: {response.status_code}")
        print(f"Minimal Payload Response: {response.text}")
    except Exception as e:
        print(f"Minimal Payload Failed: {e}")
    
    # Test 2: Full payload (with all fields)
    print("\n=== Test 2: Full Payload ===")
    full_payload = {
        "team_name": "Tenant Test Team",
        "members": ["Alice"],
        "project_title": "MultiTenant Verification",
        "tenant_id": "tenant_123",
        "workspace_id": "workspace_456",
        "event_id": "event_789"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=full_payload, timeout=30)
        print(f"Full Payload Status: {response.status_code}")
        print(f"Full Payload Response: {response.text}")
    except Exception as e:
        print(f"Full Payload Failed: {e}")
    
    # Test 3: No API key
    print("\n=== Test 3: No API Key ===")
    no_key_headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, headers=no_key_headers, json=full_payload, timeout=30)
        print(f"No API Key Status: {response.status_code}")
        print(f"No API Key Response: {response.text}")
    except Exception as e:
        print(f"No API Key Failed: {e}")
    
    # Test 4: Wrong API key
    print("\n=== Test 4: Wrong API Key ===")
    wrong_key_headers = {
        "Content-Type": "application/json",
        "X-API-Key": "wrong_key_123"
    }
    
    try:
        response = requests.post(api_url, headers=wrong_key_headers, json=full_payload, timeout=30)
        print(f"Wrong API Key Status: {response.status_code}")
        print(f"Wrong API Key Response: {response.text}")
    except Exception as e:
        print(f"Wrong API Key Failed: {e}")

def main():
    """Run all tests"""
    print("Starting comprehensive API testing...")
    
    # Test basic connectivity
    health_ok = test_health_check()
    workflows_health_ok = test_workflows_health()
    list_workflows_ok = test_list_workflows()
    
    print(f"\n=== Summary ===")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Workflows Health: {'✅' if workflows_health_ok else '❌'}")
    print(f"List Workflows: {'✅' if list_workflows_ok else '❌'}")
    
    if health_ok and workflows_health_ok and list_workflows_ok:
        print("\n=== All basic tests passed, testing team registration ===")
        test_team_registration_scenarios()
    else:
        print("\n❌ Basic tests failed. The API may not be properly deployed or configured.")
        print("Please check:")
        print("1. The API is deployed and running")
        print("2. The API key is correctly set in the environment")
        print("3. The LangGraph workflows are properly configured")

if __name__ == "__main__":
    main()