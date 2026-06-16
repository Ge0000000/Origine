import urllib.request
import json

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"

def main():
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/login", json.dumps({"password": CAPROVER_PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))["data"]["token"]
    
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/user/apps/appDefinitions", headers={"x-captain-auth": token})
    apps = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))["data"]["appDefinitions"]
    
    for app in apps:
        if app["appName"] == "kuma":
            print(json.dumps(app, indent=2))

if __name__ == "__main__":
    main()
