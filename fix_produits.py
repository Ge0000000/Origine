import urllib.request
import json
import uuid

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

    # Fix the id field in produits collection
    api_call("/fields/produits/id", method="PATCH", data={
        "schema": {"default_value": "uuid_generate_v4()"}
    }, token=token)

    # Fetch Site ID for Le Croisetier
    sites = api_call("/items/sites", method="GET", token=token)
    site_id = None
    for site in sites["data"]:
        if site.get("slug") == "le-croisetier":
            site_id = site["id"]
            break

    # Get the image ID from directus_files
    files = api_call("/files", method="GET", token=token)
    image_id = None
    for f in files["data"]:
        if f.get("title") == "Crucifix Le Croisetier":
            image_id = f["id"]
            break

    # Create Product Item with explicit UUID
    product_item = {
        "id": str(uuid.uuid4()),
        "status": "published",
        "site_id": site_id,
        "nom": "Crucifix artisanal Le Croisetier",
        "description": "Chaque pièce est unique, façonnée avec soin pour accompagner les grands moments de la vie (Baptême, Communion, Confirmation). Bois peint à la main en Anjou avec un Christ métallique blanc. Hauteur 10 cm avec socle.",
        "prix": 22,
        "lien_stripe": "https://buy.stripe.com/bJe5kwgRGdNgay82bkejK00",
        "image": image_id
    }
    
    api_call("/items/produits", method="POST", data=product_item, token=token)
    print("Product fixed and inserted!")

if __name__ == "__main__":
    main()
