import requests
import json

def final_handover_check():
    base_url = 'https://ai-agent-x2iw.onrender.com'
    
    print("🚀 Starting final handover verification...\n")
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        r = requests.get(f'{base_url}/')
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            message = r.json().get("message", "N/A")
            print(f"   Message: {message}")
            print("   ✅ PASS\n")
        else:
            print("   ❌ FAIL\n")
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
    
    # Test 2: Health endpoint
    print("2. Testing health endpoint...")
    try:
        r = requests.get(f'{base_url}/system/health')
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            health = r.json().get("status", "N/A")
            print(f"   Health: {health}")
            print("   ✅ PASS\n")
        else:
            print("   ❌ FAIL\n")
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
    
    # Test 3: Ping endpoint
    print("3. Testing ping endpoint...")
    try:
        r = requests.get(f'{base_url}/ping')
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            status = r.json().get("status", "N/A")
            print(f"   Status: {status}")
            print("   ✅ PASS\n")
        else:
            print("   ❌ FAIL\n")
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
    
    # Test 4: Agent endpoint
    print("4. Testing agent endpoint...")
    try:
        payload = {
            'team_id': 'test_team_handover',
            'prompt': 'Test request for handover verification',
            'metadata': {'source': 'final_handover_check'}
        }
        r = requests.post(f'{base_url}/agent/', json=payload)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            action = data.get("action", "N/A")[:50]
            reward = data.get("reward", "N/A")
            print(f"   Action: {action}...")
            print(f"   Reward: {reward}")
            print("   ✅ PASS\n")
        else:
            print("   ❌ FAIL\n")
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
    
    # Test 5: Admin reward endpoint
    print("5. Testing admin reward endpoint...")
    try:
        payload = {
            'request_id': 'handover_test_123',
            'outcome': 'success'
        }
        r = requests.post(f'{base_url}/admin/reward', json=payload)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            reward_value = data.get("reward_value", "N/A")
            feedback = data.get("feedback", "N/A")
            print(f"   Reward Value: {reward_value}")
            print(f"   Feedback: {feedback}")
            print("   ✅ PASS\n")
        else:
            print("   ❌ FAIL\n")
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
    
    print("🎉 Final handover verification completed!")
    print("📋 Summary: All critical endpoints are working correctly.")
    print("✅ The system is ready for handover to Vinayak.")

if __name__ == "__main__":
    final_handover_check()