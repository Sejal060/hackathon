import requests
import time
import subprocess
import sys

def verify_routes():
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
            print("OpenAPI spec retrieved successfully!")
            
            # Check if the expected paths are present
            paths = openapi_spec.get('paths', {})
            print(f"Available paths: {list(paths.keys())}")
            
            # Check for our expected routes
            expected_paths = ['/agent/', '/agent', '/reward/', '/reward', '/logs/', '/logs']
            found_paths = [path for path in expected_paths if path in paths]
            print(f"Found expected paths: {found_paths}")
            
            # Check tags
            tags = [tag['name'] for tag in openapi_spec.get('tags', [])]
            print(f"Available tags: {tags}")
            
            return True
        else:
            print(f"Failed to retrieve OpenAPI spec. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error verifying routes: {e}")
        return False
    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    verify_routes()