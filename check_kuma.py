import urllib.request
import json
import sys

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "kuma"

def api_call(path, data=None, token=None, method="POST"):
    url = CAPROVER_URL + path
    headers = {}
    if token:
        headers["x-captain-auth"] = token
    
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, body, headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
        
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"ERREUR: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode())
        sys.exit(1)

def main():
    r = api_call("/api/v2/login", {"password": CAPROVER_PASSWORD})
    token = r["data"]["token"]
    
    print("Fetching app status...")
    # There is no direct API for logs without websocket in CapRover V2, but we can check app definitions.
    r = api_call(f"/api/v2/user/apps/appData/{APP_NAME}", token=token, method="GET")
    
    # Just print the port and the nodes
    data = r.get("data", {})
    print("App definition:")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
