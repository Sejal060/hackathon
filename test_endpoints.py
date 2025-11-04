import requests
import json

def test_endpoints():
    """Test the main endpoints to verify they work correctly"""
    base_url = "http://127.0.0.1:8001"
    
    # Test ping endpoint
    print("Testing /ping endpoint...")
    response = requests.get(f"{base_url}/ping")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test agent endpoint
    print("\nTesting /agent endpoint...")
    payload = {"team_id": "test_team", "prompt": "Hello, world!"}
    response = requests.post(f"{base_url}/agent", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    
    # Test reward endpoint
    print("\nTesting /admin/reward endpoint...")
    payload = {"request_id": "test_request", "outcome": "success"}
    response = requests.post(f"{base_url}/admin/reward", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    
    # Test logs endpoint
    print("\nTesting /admin/logs endpoint...")
    payload = {"timestamp": "2025-01-01T00:00:00", "level": "INFO", "message": "test log"}
    response = requests.post(f"{base_url}/admin/logs", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_endpoints()