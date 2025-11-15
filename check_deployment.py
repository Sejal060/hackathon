import requests
import time

def check_deployment():
    url = "https://ai-agent-x2iw.onrender.com"
    print(f"Checking deployment at {url}")
    
    try:
        # Try to get the root endpoint
        response = requests.get(url, timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text[:500]}")
        return response.status_code
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        return None
    except Exception as e:
        print(f"Other Error: {e}")
        return None

if __name__ == "__main__":
    status = check_deployment()
    if status:
        print(f"Deployment check completed with status: {status}")
    else:
        print("Deployment check failed")