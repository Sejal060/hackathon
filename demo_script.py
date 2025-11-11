#!/usr/bin/env python3
"""
Demo script showing HackaVerse backend in action
This script demonstrates all the key functionality
"""

import requests
import json
import time
from datetime import datetime
import threading
import uvicorn
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_system():
    """Demonstrate the HackaVerse system"""
    print("🚀 HackaVerse Backend Demo")
    print("=" * 40)
    
    # Base URL for the demo
    BASE_URL = "http://127.0.0.1:8001"
    
    print("1️⃣  Team Registration")
    registration_payload = {
        "team_name": "Demo Team",
        "members": ["Sejal", "Yash", "Vinayak"],
        "project_title": "HackaVerse Platform"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/webhook/hackaverse/registration", 
                               json=registration_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Team registered successfully!")
            print(f"   🆔 Team ID: {data.get('team_id')}")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Registration error (backend may not be running): {str(e)}")
    
    time.sleep(1)
    
    print("\n2️⃣  Agent Request")
    agent_payload = {
        "team_id": "demo_team",
        "prompt": "How to build a REST API with FastAPI?",
        "metadata": {
            "project_type": "web_backend",
            "experience_level": "intermediate"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agent/", json=agent_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Agent processed request successfully!")
            print(f"   📝 Response: {data.get('result', '')[:100]}...")
            print(f"   🏆 Reward: {data.get('reward', 0)} points")
        else:
            print(f"   ❌ Agent request failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Agent error (backend may not be running): {str(e)}")
    
    time.sleep(1)
    
    print("\n3️⃣  Reward Calculation")
    reward_payload = {
        "request_id": "req_demo_001",
        "outcome": "success"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/reward", json=reward_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Reward calculated successfully!")
            print(f"   🏆 Reward value: {data.get('reward_value', 0)}")
            print(f"   💬 Feedback: {data.get('feedback', 'No feedback')}")
        else:
            print(f"   ❌ Reward calculation failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Reward error (backend may not be running): {str(e)}")
    
    time.sleep(1)
    
    print("\n4️⃣  System Health Check")
    try:
        response = requests.get(f"{BASE_URL}/system/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ System is healthy!")
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🔢 Version: {data.get('version')}")
            print(f"   🐍 Python: {data.get('python_version', '')[:30]}...")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Health check error (backend may not be running): {str(e)}")
    
    print("\n" + "=" * 40)
    print("🎯 Demo Complete!")
    print("\nTo see the full system in action:")
    print("1. Start the backend: uvicorn src.main:app --reload --port 8001")
    print("2. Run this demo script again")
    print("3. Check MongoDB for KSML formatted logs in bhiv_db.logs")

if __name__ == "__main__":
    demo_system()