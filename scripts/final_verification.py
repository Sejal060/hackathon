import requests
import time
import subprocess
import sys
import json

def final_verification():
    # Start the server in the background
    print("Starting server...")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", "--port", "8000"
    ])
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Get the OpenAPI spec
        response = requests.get("http://127.0.0.1:8000/openapi.json")
        if response.status_code == 200:
            openapi_spec = response.json()
            print("✅ OpenAPI spec retrieved successfully!")
            
            # Check API info
            info = openapi_spec.get('info', {})
            print(f"✅ Title: {info.get('title')}")
            print(f"✅ Version: {info.get('version')}")
            print(f"✅ Description: {info.get('description')}")
            
            # Check contact info
            contact = info.get('contact', {})
            print(f"✅ Contact: {contact.get('name')} <{contact.get('email')}>")
            
            # Check tags
            tags = [tag['name'] for tag in openapi_spec.get('tags', [])]
            expected_tags = ['agent', 'admin', 'system']
            if all(tag in tags for tag in expected_tags):
                print(f"✅ All expected tags present: {tags}")
            else:
                print(f"❌ Missing tags. Expected: {expected_tags}, Found: {tags}")
                return False
            
            # Check paths
            paths = openapi_spec.get('paths', {})
            print(f"✅ Available paths: {list(paths.keys())}")
            
            # Check schemas for examples
            schemas = openapi_spec.get('components', {}).get('schemas', {})
            agent_request_schema = schemas.get('AgentRequest', {})
            
            # Check if AgentRequest has examples
            if 'properties' in agent_request_schema:
                team_id_prop = agent_request_schema['properties'].get('team_id', {})
                submission_url_prop = agent_request_schema['properties'].get('prompt', {})
                
                # Check for examples in properties
                team_id_examples = team_id_prop.get('examples', [])
                submission_url_examples = submission_url_prop.get('examples', [])
                
                if team_id_examples and submission_url_examples:
                    print(f"✅ AgentRequest schema has examples:")
                    print(f"   - team_id: {team_id_examples}")
                    print(f"   - prompt: {submission_url_examples}")
                else:
                    print("⚠️  AgentRequest schema missing examples in properties")
            
            # Check for examples in schema level
            agent_request_examples = agent_request_schema.get('examples', {})
            if agent_request_examples:
                print(f"✅ AgentRequest schema has examples at schema level: {list(agent_request_examples.keys())}")
            else:
                print("⚠️  AgentRequest schema missing examples at schema level")
            
            print("\n🎉 All verifications completed successfully!")
            return True
        else:
            print(f"❌ Failed to retrieve OpenAPI spec. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()
        print("⏹️  Server stopped.")

if __name__ == "__main__":
    success = final_verification()
    sys.exit(0 if success else 1)