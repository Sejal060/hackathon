import requests
import json

def test_frontend_integration():
    """Test frontend integration with deployed endpoints"""
    base_url = "https://ai-agent-x2iw.onrender.com"
    
    print("🧪 Frontend Integration Test")
    print("=" * 50)
    
    # Test 1: CORS headers
    print("1. Testing CORS headers...")
    try:
        response = requests.get(f"{base_url}/", headers={"Origin": "https://app.gurukul-ai.in"})
        cors_header = response.headers.get("access-control-allow-origin", "")
        if cors_header == "*":
            print("✅ CORS: All origins allowed (development setting)")
        else:
            print(f"⚠️  CORS: {cors_header} (may need adjustment for production)")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
    
    # Test 2: Content-Type headers
    print("2. Testing Content-Type headers...")
    try:
        response = requests.get(f"{base_url}/")
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            print("✅ Content-Type: application/json")
        else:
            print(f"⚠️  Content-Type: {content_type}")
    except Exception as e:
        print(f"❌ Content-Type test failed: {e}")
    
    # Test 3: Agent endpoint with sample data
    print("3. Testing Agent endpoint...")
    agent_payload = {
        "team_id": "frontend_test_team",
        "prompt": "How to integrate with the HackaVerse API?",
        "metadata": {
            "source": "frontend_integration_test",
            "user_id": "test_user_123"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/agent/", json=agent_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent endpoint: Working")
            print(f"   - Processed input: {data.get('processed_input', '')[:50]}...")
            print(f"   - Action: {data.get('action', '')[:50]}...")
            print(f"   - Result: {data.get('result', '')[:50]}...")
            print(f"   - Reward: {data.get('reward', 0)}")
        else:
            print(f"❌ Agent endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Agent endpoint test failed: {e}")
    
    # Test 4: Registration endpoint
    print("4. Testing Registration endpoint...")
    registration_payload = {
        "team_name": "Frontend Integration Test Team",
        "members": ["Yash", "Nikhil"],
        "project_title": "Frontend Integration Test"
    }
    
    try:
        response = requests.post(f"{base_url}/admin/register", json=registration_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Registration endpoint: Working")
            print(f"   - Message: {data.get('message', '')}")
            print(f"   - Team ID: {data.get('team_id', '')}")
        else:
            print(f"❌ Registration endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Registration endpoint test failed: {e}")
    
    # Test 5: Health endpoint
    print("5. Testing Health endpoint...")
    try:
        response = requests.get(f"{base_url}/system/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint: Working")
            print(f"   - Status: {data.get('status', '')}")
            print(f"   - Version: {data.get('version', '')}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
    
    print("=" * 50)
    print("🎉 Frontend integration test completed!")

if __name__ == "__main__":
    test_frontend_integration()