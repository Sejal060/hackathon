import requests
import json

# Test agent endpoint
url = "http://127.0.0.1:8001/agent/"
payload = {
    "team_id": "test_team",
    "prompt": "Hello, world!",
    "metadata": {}
}

response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")