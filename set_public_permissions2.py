import urllib.request
import json

DIRECTUS_URL = "http://directus.37.187.219.15.nip.io"
EMAIL = "admin@origine.dev"
PASSWORD = "Origine@Admin2026!"

def main():
    req = urllib.request.Request(DIRECTUS_URL + "/auth/login", json.dumps({"email": EMAIL, "password": PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode())["data"]["access_token"]

    public_policy_id = "abf8a154-5b1c-4a46-ac9c-7300570f4f17"
    
    req = urllib.request.Request(DIRECTUS_URL + "/permissions", json.dumps({
        "collection": "produits",
        "action": "read",
        "fields": ["*"],
        "policy": public_policy_id,
        "permissions": {}
    }).encode("utf-8"), {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    
    try:
        res = urllib.request.urlopen(req).read().decode()
        print("Success:", res)
    except urllib.error.HTTPError as e:
        print("Error:", e.read().decode())

if __name__ == "__main__":
    main()
