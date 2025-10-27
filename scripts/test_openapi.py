import requests
import time
import subprocess
import sys

def test_openapi():
    # Start the server in the background
    print("Starting server...")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", "--port", "8000"
    ])
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test the OpenAPI endpoint
        response = requests.get("http://127.0.0.1:8000/openapi.json")
        if response.status_code == 200:
            openapi_spec = response.json()
            print("OpenAPI spec retrieved successfully!")
            print(f"Title: {openapi_spec['info']['title']}")
            print(f"Version: {openapi_spec['info']['version']}")
            print(f"Description: {openapi_spec['info']['description']}")
            return True
        else:
            print(f"Failed to retrieve OpenAPI spec. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error testing OpenAPI endpoint: {e}")
        return False
    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    test_openapi()