import urllib.request
import json

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "kuma"

def main():
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/login", json.dumps({"password": CAPROVER_PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))["data"]["token"]
    
    print("Updating kuma to remove volume...")
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/user/apps/appDefinitions/update", json.dumps({
        "appName": APP_NAME,
        "instanceCount": 1,
        "containerHttpPort": 3001,
        "forceSsl": False,
        "websocketSupport": True,
        "notExposeAsWebApp": False,
        "volumes": [] # REMOVE VOLUMES
    }).encode("utf-8"), {"Content-Type": "application/json", "x-captain-auth": token})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        print("Success update:", resp.read().decode("utf-8"))
    except Exception as e:
        print("Error update:", e)

if __name__ == "__main__":
    main()
