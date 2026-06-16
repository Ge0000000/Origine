import urllib.request
import json
import sys

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "kuma"

def main():
    # Login
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/login", json.dumps({"password": CAPROVER_PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))["data"]["token"]
    
    print("Enabling base domain SSL...")
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/user/apps/appDefinitions/enablebasedomainssl", json.dumps({"appName": APP_NAME}).encode("utf-8"), {"Content-Type": "application/json", "x-captain-auth": token})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        print("Success:", resp.read().decode("utf-8"))
    except Exception as e:
        print("Error:", e)
        if hasattr(e, 'read'):
            print(e.read().decode("utf-8"))

    print("Forcing SSL...")
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/user/apps/appDefinitions/update", json.dumps({
        "appName": APP_NAME,
        "instanceCount": 1,
        "containerHttpPort": 3001,
        "forceSsl": True,
        "websocketSupport": True,
        "notExposeAsWebApp": False
    }).encode("utf-8"), {"Content-Type": "application/json", "x-captain-auth": token})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        print("Success update:", resp.read().decode("utf-8"))
    except Exception as e:
        print("Error update:", e)

if __name__ == "__main__":
    main()
