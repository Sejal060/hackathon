import requests
import json

# Test registration webhook
url = "http://127.0.0.1:8001/admin/webhook/hackaverse/registration"
payload = {
    "team_name": "Test Team",
    "members": ["Alice", "Bob"],
    "project_title": "Test Project"
}

response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")