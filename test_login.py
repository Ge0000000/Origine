import urllib.request
import json

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"

def main():
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/login", json.dumps({"password": CAPROVER_PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req).read().decode("utf-8")
    print("Login response:", resp)

if __name__ == "__main__":
    main()
