import requests
import time

def verify_endpoints():
    """Verify that all required endpoints are working"""
    base_url = "http://127.0.0.1:8001"
    
    print("🔍 Verifying Hackathon Management System Endpoints")
    print("=" * 50)
    
    # Test 1: Ping endpoint
    print("\n1️⃣ Testing /ping endpoint...")
    try:
        response = requests.get(f"{base_url}/ping", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ PASS: {response.json()}")
        else:
            print(f"   ❌ FAIL: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 2: Agent endpoint
    print("\n2️⃣ Testing /agent endpoint...")
    try:
        payload = {"team_id": "verification_team", "prompt": "test prompt"}
        response = requests.post(f"{base_url}/agent", json=payload, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ PASS: Agent response received")
            result = response.json()
            print(f"   📊 Result: {result.get('result', 'N/A')[:50]}...")
        else:
            print(f"   ❌ FAIL: Status {response.status_code}")
            print(f"   📝 Error: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 3: Reward endpoint
    print("\n3️⃣ Testing /admin/reward endpoint...")
    try:
        payload = {"request_id": "verification_request", "outcome": "success"}
        response = requests.post(f"{base_url}/admin/reward", json=payload, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ PASS: {response.json()}")
        else:
            print(f"   ❌ FAIL: Status {response.status_code}")
            print(f"   📝 Error: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 4: Logs endpoint
    print("\n4️⃣ Testing /admin/logs endpoint...")
    try:
        payload = {"timestamp": "2025-01-01T00:00:00", "level": "INFO", "message": "Verification test"}
        response = requests.post(f"{base_url}/admin/logs", json=payload, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ PASS: {response.json()}")
        else:
            print(f"   ❌ FAIL: Status {response.status_code}")
            print(f"   📝 Error: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 5: Health endpoint
    print("\n5️⃣ Testing /system/health endpoint...")
    try:
        response = requests.get(f"{base_url}/system/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ PASS: {response.json()}")
        else:
            print(f"   ❌ FAIL: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Verification complete!")

if __name__ == "__main__":
    verify_endpoints()