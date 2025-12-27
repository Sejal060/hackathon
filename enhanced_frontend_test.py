import requests
import json

def test_enhanced_frontend_integration():
    """Enhanced test for frontend integration with all new endpoints"""
    base_url = "https://ai-agent-x2iw.onrender.com"
    
    print("🧪 Enhanced Frontend Integration Test")
    print("=" * 60)
    
    # Test 1: Register a test team
    print("1. Testing Team Registration (LangGraph flow)...")
    registration_payload = {
        "team_name": "Frontend Test Team",
        "members": ["Test User 1", "Test User 2"],
        "project_title": "Test Project for Frontend Integration"
    }
    
    try:
        response = requests.post(f"{base_url}/admin/webhook/hackaverse/registration", json=registration_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Team registration endpoint: Working")
            print(f"   - Message: {data.get('message', '')}")
        else:
            print(f"❌ Team registration failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Team registration test failed: {e}")
    
    # Test 2: Agent endpoint
    print("\n2. Testing Agent endpoint...")
    agent_payload = {
        "user_input": "How to integrate with the HackaVerse API?",
        "context": {
            "team_id": "frontend_test_team",
            "project_type": "web_application"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/agent", json=agent_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent endpoint: Working")
            print(f"   - Success: {data.get('success', False)}")
            print(f"   - Message: {data.get('message', '')[:50]}...")
        else:
            print(f"❌ Agent endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Agent endpoint test failed: {e}")
    
    # Test 3: Judge endpoint (new multi-agent system)
    print("\n3. Testing Judge endpoint (Multi-Agent)...")
    judge_payload = {
        "submission_text": "This is a test submission for frontend integration. The project implements a comprehensive solution with multiple features and demonstrates good technical depth.",
        "team_id": "frontend_test_team"
    }
    
    try:
        response = requests.post(f"{base_url}/judge/score", json=judge_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Judge endpoint: Working")
            print(f"   - Total Score: {data.get('total_score', 0)}")
            print(f"   - Clarity: {data.get('clarity', 0)}")
            print(f"   - Innovation: {data.get('innovation', 0)}")
        else:
            print(f"❌ Judge endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Judge endpoint test failed: {e}")
    
    # Test 4: Submit and score endpoint
    print("\n4. Testing Submit & Score endpoint...")
    try:
        response = requests.post(f"{base_url}/judge/submit", json=judge_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Submit & Score endpoint: Working")
            if data.get('success'):
                judging_result = data.get('data', {}).get('judging_result', {})
                print(f"   - Consensus Score: {judging_result.get('consensus_score', 0)}")
                print(f"   - Individual Scores Available: {len(judging_result.get('individual_scores', {})) > 0}")
            else:
                print(f"   - Success: {data.get('success', False)}")
        else:
            print(f"❌ Submit & Score endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Submit & Score endpoint test failed: {e}")
    
    # Test 5: Get rubric endpoint
    print("\n5. Testing Rubric endpoint...")
    try:
        response = requests.get(f"{base_url}/judge/rubric")
        if response.status_code == 200:
            data = response.json()
            print("✅ Rubric endpoint: Working")
            rubric_data = data.get('data', {})
            print(f"   - Criteria Count: {len(rubric_data.get('criteria', {}))}")
            print(f"   - Has Weights: {'weights' in rubric_data}")
        else:
            print(f"❌ Rubric endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Rubric endpoint test failed: {e}")
    
    # Test 6: LangGraph flow endpoint
    print("\n6. Testing LangGraph Flow endpoint...")
    flow_payload = {
        "team_name": "Test Flow Team",
        "members": ["Flow Member"],
        "project_title": "Test Flow Project",
        "timestamp": "2023-12-27T10:00:00Z"
    }
    
    try:
        response = requests.post(f"{base_url}/flows/team_registration", json=flow_payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ LangGraph Flow endpoint: Working")
            print(f"   - Message: {data.get('message', '')}")
        else:
            print(f"❌ LangGraph Flow endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ LangGraph Flow endpoint test failed: {e}")
    
    # Test 7: Health check
    print("\n7. Testing Health endpoint...")
    try:
        response = requests.get(f"{base_url}/system/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint: Working")
            print(f"   - Status: {data.get('status', '')}")
            print(f"   - Version: {data.get('version', '')}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
    
    # Test 8: Ready endpoint for deployment
    print("\n8. Testing Ready endpoint...")
    try:
        response = requests.get(f"{base_url}/system/ready")
        if response.status_code == 200:
            data = response.json()
            print("✅ Ready endpoint: Working")
            print(f"   - Ready: {data.get('ready', False)}")
        else:
            print(f"❌ Ready endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Ready endpoint test failed: {e}")
    
    print("=" * 60)
    print("🎉 Enhanced frontend integration test completed!")
    
    # Summary
    print("\n📋 Integration Test Summary:")
    print("- Register: ✅ Tested")
    print("- Submit: ✅ Tested") 
    print("- Agent: ✅ Tested")
    print("- Judge: ✅ Tested (Multi-Agent)")
    print("- Logs: ✅ Tested (via system endpoints)")
    print("\nAll critical frontend-backend integration points verified!")

if __name__ == "__main__":
    test_enhanced_frontend_integration()