import urllib.request
import json
import time

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "kuma"

def main():
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/login", json.dumps({"password": CAPROVER_PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))["data"]["token"]
    
    print("Setting instance count to 0...")
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/user/apps/appDefinitions/update", json.dumps({
        "appName": APP_NAME,
        "instanceCount": 0,
        "containerHttpPort": 3001,
        "forceSsl": False,
        "websocketSupport": True,
        "notExposeAsWebApp": False,
    }).encode("utf-8"), {"Content-Type": "application/json", "x-captain-auth": token})
    urllib.request.urlopen(req, timeout=30)
    
    time.sleep(3)
    
    print("Setting instance count to 1...")
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/user/apps/appDefinitions/update", json.dumps({
        "appName": APP_NAME,
        "instanceCount": 1,
        "containerHttpPort": 3001,
        "forceSsl": False,
        "websocketSupport": True,
        "notExposeAsWebApp": False,
    }).encode("utf-8"), {"Content-Type": "application/json", "x-captain-auth": token})
    urllib.request.urlopen(req, timeout=30)
    
    print("Done")

if __name__ == "__main__":
    main()
