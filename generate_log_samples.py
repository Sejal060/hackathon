#!/usr/bin/env python3
"""
Generate log samples for handover to Vinayak
Demonstrates the KSML logging format
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8001"

def generate_sample_logs():
    """Generate sample logs by making various API calls"""
    print("Generating sample logs...")
    
    # 1. Test registration
    print("1. Testing team registration...")
    registration_payload = {
        "team_name": "Sample Team Alpha",
        "members": ["Alice Developer", "Bob Coder"],
        "project_title": "AI-Powered Log Analysis"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/webhook/hackaverse/registration", 
                               json=registration_payload)
        print(f"   Registration response: {response.status_code}")
    except Exception as e:
        print(f"   Registration error: {str(e)}")
    
    time.sleep(1)
    
    # 2. Test agent request
    print("2. Testing agent request...")
    agent_payload = {
        "team_id": "sample_team_alpha",
        "prompt": "How to implement microservices architecture?",
        "metadata": {
            "project_domain": "web_development",
            "experience_level": "intermediate"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agent/", json=agent_payload)
        print(f"   Agent response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Agent result: {data.get('result', '')[:100]}...")
    except Exception as e:
        print(f"   Agent error: {str(e)}")
    
    time.sleep(1)
    
    # 3. Test reward calculation
    print("3. Testing reward calculation...")
    reward_payload = {
        "request_id": "req_sample_001",
        "outcome": "success"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/reward", json=reward_payload)
        print(f"   Reward response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Reward value: {data.get('reward_value', 'unknown')}")
    except Exception as e:
        print(f"   Reward error: {str(e)}")
    
    time.sleep(1)
    
    # 4. Test health check
    print("4. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/system/health")
        print(f"   Health response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   System status: {data.get('status', 'unknown')}")
    except Exception as e:
        print(f"   Health error: {str(e)}")
    
    print("\nSample logs generated successfully!")
    print("Check MongoDB 'bhiv_db.logs' collection for KSML formatted logs.")

def export_sample_logs():
    """Export sample logs to a JSON file"""
    print("Exporting sample logs to file...")
    
    # Sample KSML log format
    sample_logs = [
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "registration",
            "actor": "registration_system",
            "context": "Team Sample Team Alpha registered with project: AI-Powered Log Analysis",
            "outcome": "success"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "agent_request",
            "actor": "team_sample_team_alpha",
            "context": "Team sample_team_alpha requested: How to implement microservices architecture?",
            "outcome": "received",
            "additional_data": "{\"metadata\": {\"project_domain\": \"web_development\", \"experience_level\": \"intermediate\"}}"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "input_processing",
            "actor": "mcp_router",
            "context": "{'team_id': 'sample_team_alpha', 'prompt': 'How to implement microservices architecture?', 'metadata': {'project_domain': 'web_development', 'experience_level': 'intermediate'}}",
            "outcome": "started"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "reasoning",
            "actor": "mcp_router",
            "context": "Input: How to implement microservices architecture?, Context: {'project_domain': 'web_development', 'experience_level': 'intermediate'}",
            "outcome": "completed"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "execution",
            "actor": "mcp_router",
            "context": "Action: Research microservices architecture patterns",
            "outcome": "completed"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "core_communication",
            "actor": "mcp_router",
            "context": "Communicated with BHIV Core for team sample_team_alpha",
            "outcome": "success",
            "additional_data": "{\"payload_size\": 150, \"response_size\": 200}"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "agent_response",
            "actor": "system",
            "context": "Response generated for team sample_team_alpha",
            "outcome": "success",
            "additional_data": "{\"response_length\": 500}"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "reward_calculation",
            "actor": "reward_system",
            "context": "Calculated reward for request req_sample_001 with outcome: success",
            "outcome": "completed",
            "additional_data": "{\"reward_value\": 1.5}"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "intent": "health_check",
            "actor": "system",
            "context": "System health check performed",
            "outcome": "healthy"
        }
    ]
    
    # Save to file
    with open("sample_logs.json", "w") as f:
        json.dump(sample_logs, f, indent=2)
    
    print("Sample logs exported to sample_logs.json")
    print("Format follows KSML (Karmic System Micro Logging) specification:")
    print("{ \"intent\": \"...\", \"actor\": \"...\", \"context\": \"...\", \"outcome\": \"...\" }")

if __name__ == "__main__":
    print("HackaVerse Log Sample Generator")
    print("=" * 40)
    
    # Generate live logs by making API calls
    generate_sample_logs()
    
    print("\n" + "=" * 40)
    
    # Export sample logs to file
    export_sample_logs()
    
    print("\nHandover complete! Share sample_logs.json with Vinayak.")