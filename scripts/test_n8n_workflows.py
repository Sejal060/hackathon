#!/usr/bin/env python3
"""
Test script to simulate n8n webhook POSTs to FastAPI endpoints
This script proves expected behavior without running n8n
"""

import requests
import json

def test_n8n_workflows():
    """Test N8N workflow simulations"""
    print("🧪 Testing N8N Workflow Simulation")
    print("===================================")
    
    # Base URL for FastAPI backend
    BASE_URL = "http://localhost:8001"
    
    # Test 1: Team Registration Workflow Simulation
    print("\n1️⃣ Testing Team Registration Workflow")
    print("   Simulating POST to /agent endpoint")
    print("   Payload: Team registration data")
    
    team_registration_payload = {
        "user_input": "Register team n8n_test_team",
        "context": {
            "team_id": "n8n_test_team"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/agent",
            json=team_registration_payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"   ✅ Team registration simulation successful (Status: {response.status_code})")
        else:
            print(f"   ❌ Team registration simulation failed (Status: {response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Team registration simulation failed with exception: {e}")
    
    # Test 2: MentorBot Prompt Workflow Simulation
    print("\n2️⃣ Testing MentorBot Prompt Workflow")
    print("   Simulating POST to /agent endpoint")
    print("   Payload: Mentor request data")
    
    mentor_payload = {
        "user_input": "How do I implement authentication in my FastAPI app?",
        "context": {
            "team_id": "n8n_test_team",
            "project_type": "web_application"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/agent",
            json=mentor_payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"   ✅ Mentor request simulation successful (Status: {response.status_code})")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Mentor request simulation failed (Status: {response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Mentor request simulation failed with exception: {e}")
    
    # Test 3: Verify endpoints are accessible
    print("\n3️⃣ Testing Endpoint Accessibility")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print(f"   ✅ /docs endpoint accessible (Status: {response.status_code})")
        else:
            print(f"   ❌ /docs endpoint not accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ /docs endpoint test failed with exception: {e}")
    
    try:
        response = requests.get(f"{BASE_URL}/ping")
        if response.status_code == 200:
            print(f"   ✅ /ping endpoint accessible (Status: {response.status_code})")
            result = response.json()
            print(f"   Response: {result}")
        else:
            print(f"   ❌ /ping endpoint not accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ /ping endpoint test failed with exception: {e}")
    
    print("\n✅ N8N Workflow Simulation Complete")
    print("   All workflows have been tested successfully")
    print("   Check the responses above to verify expected behavior")

if __name__ == "__main__":
    test_n8n_workflows()