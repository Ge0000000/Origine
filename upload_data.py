import requests
import json
import time

DIRECTUS_URL = "http://directus.37.187.219.15.nip.io"
EMAIL = "admin@origine.dev"
PASSWORD = "Origine@Admin2026!"

print("Logging in to Directus...")
res = requests.post(f"{DIRECTUS_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
token = res.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}

def upload_image(filepath, title):
    print(f"Uploading {title}...")
    with open(filepath, 'rb') as f:
        files = {'file': (title + '.png', f, 'image/png')}
        r = requests.post(f"{DIRECTUS_URL}/files", headers=headers, files=files)
        data = r.json()
        if "data" in data:
            return data["data"]["id"]
        print("Upload error:", data)
        return None

# Upload images
matikos_img = upload_image(r"C:\Users\Utilisateur\.gemini\antigravity\brain\a209cf84-badc-4ca9-877a-fe5fa471faa0\matikos_hero_1781643805637.png", "matikos_hero")
time.sleep(2)
annuaire_img = upload_image(r"C:\Users\Utilisateur\.gemini\antigravity\brain\a209cf84-badc-4ca9-877a-fe5fa471faa0\annuaire_hero_1781643817571.png", "annuaire_hero")
time.sleep(2)
croisetier_img = upload_image(r"C:\Users\Utilisateur\.gemini\antigravity\brain\a209cf84-badc-4ca9-877a-fe5fa471faa0\croisetier_hero_1781643828116.png", "croisetier_hero")
time.sleep(2)

print("Fetching sites...")
sites = requests.get(f"{DIRECTUS_URL}/items/sites", headers=headers).json()["data"]

for site in sites:
    slug = site["slug"]
    site_id = site["id"]
    
    # Try to find existing vitrine
    vitrines_res = requests.get(f"{DIRECTUS_URL}/items/vitrines?filter[site_id][_eq]={site_id}", headers=headers).json()["data"]
    
    vitrine_id = vitrines_res[0]["id"] if len(vitrines_res) > 0 else None
    
    payload = {"site_id": site_id}
    
    if slug == "matikos":
        payload["hero_titre"] = "L'Excellence Artisanale en Menuiserie & Plâtrerie"
        payload["hero_description"] = "Basés à Segré en Anjou Bleu, nous concevons et réalisons des espaces sur-mesure alliant savoir-faire traditionnel et finitions contemporaines pour vos projets de rénovation."
        payload["services"] = ["Menuiserie sur-mesure", "Plâtrerie décorative", "Agencement intérieur", "Isolation thermique"]
        payload["adresse"] = "42 Rue des Artisans, 49500 Segré-en-Anjou Bleu"
        payload["telephone"] = "02 41 92 00 00"
        payload["email"] = "contact@matikos.fr"
        if matikos_img:
            payload["hero_image"] = matikos_img
            payload["realisations"] = [matikos_img] # On utilise l'image du hero comme 1ere réalisation pour l'instant
            
    elif slug == "annuaire-createurs-catholiques":
        payload["hero_titre"] = "L'Annuaire des Créateurs Catholiques"
        payload["hero_description"] = "Soutenez l'économie chrétienne et l'artisanat de talent. Découvrez une sélection rigoureuse d'artistes, sculpteurs, peintres et créateurs inspirés par la foi."
        if annuaire_img:
            payload["hero_image"] = annuaire_img
            
    elif slug == "le-croisetier":
        payload["hero_titre"] = "Atelier Le Croisetier"
        payload["hero_description"] = "Création de croix en bois sculptées à la main. Un artisanat d'art sacré, façonné dans la prière et la noblesse du bois massif."
        payload["services"] = ["Croix murales", "Croix de procession", "Sculpture sur bois", "Restauration d'art"]
        if croisetier_img:
            payload["hero_image"] = croisetier_img
            payload["realisations"] = [croisetier_img]
            
    if payload.get("hero_titre"):
        if vitrine_id:
            requests.patch(f"{DIRECTUS_URL}/items/vitrines/{vitrine_id}", headers=headers, json=payload)
            print(f"Updated vitrine for {slug}")
        else:
            requests.post(f"{DIRECTUS_URL}/items/vitrines", headers=headers, json=payload)
            print(f"Created vitrine for {slug}")

# Ajouter un créateur factice
creators_res = requests.get(f"{DIRECTUS_URL}/items/annuaire_createurs", headers=headers).json()["data"]
if len(creators_res) == 0:
    print("Creating sample creators...")
    creator1 = {
        "nom": "Atelier Saint Joseph",
        "slug": "atelier-saint-joseph",
        "specialite": "Menuiserie d'Art",
        "description": "Menuisier passionné, je fabrique des oratoires, des crèches et des objets de piété en chêne massif de nos forêts.",
        "localisation": "Bretagne",
        "est_sponsorise": True,
        "statut": "published",
        "logo": croisetier_img
    }
    creator2 = {
        "nom": "Lumière du Ciel",
        "slug": "lumiere-du-ciel",
        "specialite": "Ciergerie",
        "description": "Cierges 100% cire d'abeille confectionnés de façon artisanale. Idéal pour vos coins prière.",
        "localisation": "Provence",
        "est_sponsorise": False,
        "statut": "published",
        "logo": annuaire_img
    }
    requests.post(f"{DIRECTUS_URL}/items/annuaire_createurs", headers=headers, json=creator1)
    requests.post(f"{DIRECTUS_URL}/items/annuaire_createurs", headers=headers, json=creator2)
    print("Creators created.")

print("All done!")
