import requests
import json

# Test reward endpoint
url = "http://127.0.0.1:8001/admin/reward"
payload = {
    "request_id": "test_request_123",
    "outcome": "success"
}

response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")