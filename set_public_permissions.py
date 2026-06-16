import urllib.request
import json

DIRECTUS_URL = "http://directus.37.187.219.15.nip.io"
EMAIL = "admin@origine.dev"
PASSWORD = "Origine@Admin2026!"

def api_call(path, method="GET", data=None, token=None):
    url = f"{DIRECTUS_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code} on {method} {path}: {e.read().decode()}")
        return None

def main():
    login_res = api_call("/auth/login", method="POST", data={"email": EMAIL, "password": PASSWORD})
    token = login_res["data"]["access_token"]

    # In Directus v11, Public permissions are tied to the Public Policy (or public role).
    # Let's find policies
    policies = api_call("/policies", method="GET", token=token)
    public_policy_id = None
    if policies and "data" in policies:
        for p in policies["data"]:
            if "Public" in p.get("name", ""):
                public_policy_id = p["id"]
                break
                
    if public_policy_id:
        print(f"Found Public policy: {public_policy_id}")
        api_call("/permissions", method="POST", data={
            "collection": "produits",
            "action": "read",
            "fields": ["*"],
            "policy": public_policy_id,
            "permissions": {}
        }, token=token)
        print("Permissions attached to Public policy.")
    else:
        print("Public policy not found.")

if __name__ == "__main__":
    main()
