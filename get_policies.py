import urllib.request
import json

DIRECTUS_URL = "http://directus.37.187.219.15.nip.io"
EMAIL = "admin@origine.dev"
PASSWORD = "Origine@Admin2026!"

def main():
    req = urllib.request.Request(DIRECTUS_URL + "/auth/login", json.dumps({"email": EMAIL, "password": PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode())["data"]["access_token"]

    req = urllib.request.Request(DIRECTUS_URL + "/policies", headers={"Authorization": f"Bearer {token}"})
    print(urllib.request.urlopen(req).read().decode())

if __name__ == "__main__":
    main()
