import urllib.request
import urllib.parse
import json
import uuid

DIRECTUS_URL = "http://directus.37.187.219.15.nip.io"
EMAIL = "admin@origine.dev"
PASSWORD = "Origine@Admin2026!"
IMAGE_URL = "https://lecroisetier.fr/uploads/crucifix-rose_le_croisetier-1774283134.webp"

def api_call(path, method="GET", data=None, token=None, content_type="application/json"):
    url = f"{DIRECTUS_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None and content_type == "application/json":
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif data is not None:
        headers["Content-Type"] = content_type
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code} on {method} {path}: {e.read().decode()}")
        return None

def main():
    # 1. Login
    login_res = api_call("/auth/login", method="POST", data={"email": EMAIL, "password": PASSWORD})
    token = login_res["data"]["access_token"]
    print("Logged in.")

    # 2. Create Collection 'produits'
    collection_data = {
        "collection": "produits",
        "meta": {
            "icon": "shopping_cart",
            "note": "Produits e-commerce",
            "display_template": "{{nom}}"
        },
        "schema": {"name": "produits"},
        "fields": [
            {"field": "id", "type": "uuid", "meta": {"hidden": True, "readonly": True}, "schema": {"is_primary_key": True, "has_auto_increment": False}},
            {"field": "status", "type": "string", "meta": {"interface": "select-dropdown", "options": {"choices": [{"text": "Published", "value": "published"}, {"text": "Draft", "value": "draft"}]}}, "schema": {"default_value": "published"}},
            {"field": "site_id", "type": "uuid", "meta": {"interface": "select-dropdown-m2o"}, "schema": {}},
            {"field": "nom", "type": "string", "meta": {"interface": "input"}, "schema": {}},
            {"field": "description", "type": "text", "meta": {"interface": "textarea"}, "schema": {}},
            {"field": "prix", "type": "integer", "meta": {"interface": "input"}, "schema": {}},
            {"field": "lien_stripe", "type": "string", "meta": {"interface": "input"}, "schema": {}},
            {"field": "image", "type": "uuid", "meta": {"interface": "file-image"}, "schema": {}}
        ]
    }
    api_call("/collections", method="POST", data=collection_data, token=token)
    print("Collection 'produits' created.")

    # 3. Create Relations
    api_call("/relations", method="POST", data={
        "collection": "produits", "field": "site_id", "related_collection": "sites"
    }, token=token)
    api_call("/relations", method="POST", data={
        "collection": "produits", "field": "image", "related_collection": "directus_files"
    }, token=token)
    print("Relations created.")

    # 4. Set Permissions
    api_call("/permissions", method="POST", data={
        "collection": "produits",
        "action": "read",
        "fields": ["*"],
        "permissions": {}
    }, token=token)
    print("Permissions set.")

    # 5. Fetch Site ID for Le Croisetier
    sites = api_call("/items/sites", method="GET", token=token)
    site_id = None
    for site in sites["data"]:
        if site.get("slug") == "le-croisetier":
            site_id = site["id"]
            break
    
    if not site_id:
        print("Error: Site 'le-croisetier' not found.")
        return

    # 6. Upload Image
    print("Downloading image...")
    image_data = urllib.request.urlopen(IMAGE_URL).read()
    
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\nCrucifix Le Croisetier\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"crucifix.webp\"\r\nContent-Type: image/webp\r\n\r\n".encode()
        + image_data
        + f"\r\n--{boundary}--\r\n".encode()
    )
    
    upload_res = api_call("/files", method="POST", data=body, token=token, content_type=f"multipart/form-data; boundary={boundary}")
    image_id = upload_res["data"]["id"] if upload_res else None
    print(f"Image uploaded: {image_id}")

    # 7. Create Product Item
    product_item = {
        "status": "published",
        "site_id": site_id,
        "nom": "Crucifix artisanal Le Croisetier",
        "description": "Chaque pièce est unique, façonnée avec soin pour accompagner les grands moments de la vie (Baptême, Communion, Confirmation). Bois peint à la main en Anjou avec un Christ métallique blanc. Hauteur 10 cm avec socle.",
        "prix": 22,
        "lien_stripe": "https://buy.stripe.com/bJe5kwgRGdNgay82bkejK00",
        "image": image_id
    }
    api_call("/items/produits", method="POST", data=product_item, token=token)
    print("Product created for Le Croisetier.")

if __name__ == "__main__":
    main()
