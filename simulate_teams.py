import requests
import random
import time

BASE_URL = "http://localhost:8001"

def register_team(team_id):
    payload = {
        "team_name": f"Team_{team_id}",
        "members": [f"Member_{i}" for i in range(1, 4)],
        "project_title": f"AI Project {random.randint(10, 99)}"
    }
    r = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"✅ Registered: {payload['team_name']} | Status: {r.status_code}")

def query_agent(team_id):
    question = f"What are the improvements for AI Project {random.randint(10, 99)}?"
    payload = {"query": question, "context": {"team_id": team_id}}
    r = requests.post(f"{BASE_URL}/agent", json=payload)
    print(f"🤖 Agent Response ({team_id}): {r.json()}")

if __name__ == "__main__":
    for i in range(1, 8):
        register_team(i)
        query_agent(i)
        time.sleep(1)
