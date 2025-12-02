import requests
import time

def check_deployment():
    # Use the actual Render URL from your deployment
    url = "https://ai-agent-x2iw.onrender.com"
    print(f"Checking deployment at {url}")
    
    # List of endpoints to check
    endpoints = [
        "/ping",
        "/system/health",
        "/judge/score",
        "/agent/run",
        "/workflows/run"
    ]
    
    results = {}
    
    try:
        for endpoint in endpoints:
            full_url = f"{url}{endpoint}"
            print(f"\nChecking {full_url}...")
            
            try:
                # For endpoints that require authentication or specific methods,
                # we'll do a simple GET request first
                response = requests.get(full_url, timeout=15)
                results[endpoint] = response.status_code
                print(f"Status Code: {response.status_code}")
                
                # For the health endpoint, also print the response
                if endpoint == "/system/health":
                    print(f"Response Content: {response.json()}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Error accessing {full_url}: {e}")
                results[endpoint] = "Error"
        
        print("\n=== SUMMARY ===")
        all_good = True
        for endpoint, status in results.items():
            status_str = "✅ PASS" if status == 200 else f"❌ FAIL ({status})"
            print(f"{endpoint:<20} {status_str}")
            if status != 200:
                all_good = False
                
        if all_good:
            print("\n🎉 All endpoints returned 200! Deployment is working correctly.")
        else:
            print("\n⚠️  Some endpoints failed. Please check the deployment.")
            
        return all_good
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = check_deployment()
    if success:
        print("\n✅ Deployment verification completed successfully!")
    else:
        print("\n❌ Deployment verification failed!")