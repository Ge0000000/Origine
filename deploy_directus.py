#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script de correction Phase 1 :
# 1. Corriger l'email admin (domaine valide)
# 2. Activer le proxy CapRover (sous-domaine directus)
# 3. Vérifier le démarrage de Directus

import urllib.request
import urllib.error
import json
import sys
import time
import tarfile
import io

CAPROVER_URL = "http://localhost:3000"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "directus"
DOCKER_IMAGE = "directus/directus:11.17.4"

# Email corrigé : utiliser .dev ou .io qui sont des vrais TLD
ENV_VARS = [
    {"key": "DB_CLIENT",             "value": "sqlite3"},
    {"key": "DB_FILENAME",           "value": "/directus/database/database.sqlite"},
    {"key": "SECRET",                "value": "origine_jwt_secret_2026_xK9mP3qR"},
    {"key": "ADMIN_EMAIL",           "value": "admin@origine.dev"},
    {"key": "ADMIN_PASSWORD",        "value": "Origine@Admin2026!"},
    {"key": "PUBLIC_URL",            "value": "http://directus.37.187.219.15.nip.io"},
    {"key": "STORAGE_LOCATIONS",     "value": "local"},
    {"key": "STORAGE_LOCAL_ROOT",    "value": "/directus/uploads"},
    {"key": "NODE_OPTIONS",          "value": "--max-old-space-size=256"},
    {"key": "TELEMETRY",             "value": "false"},
]

VOLUMES = [
    {"volumeName": "directus-database", "containerPath": "/directus/database"},
    {"volumeName": "directus-uploads",  "containerPath": "/directus/uploads"},
]


def api_call(path, data, token=None):
    url = CAPROVER_URL + path
    headers = {"Content-Type": "application/json"}
    if token:
        headers["x-captain-auth"] = token
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, body, headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("  ERREUR HTTP {}: {}".format(e.code, e.read().decode()))
        sys.exit(1)


def deploy_tarball(app_name, image_name, token):
    """Déploie via captain-definition tarball."""
    captain_def = json.dumps({"schemaVersion": 2, "imageName": image_name}).encode("utf-8")
    tarball_buffer = io.BytesIO()
    with tarfile.open(fileobj=tarball_buffer, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="captain-definition")
        info.size = len(captain_def)
        tar.addfile(info, io.BytesIO(captain_def))
    tarball_data = tarball_buffer.getvalue()

    boundary = "----CapRoverBoundary8888"
    body = (
        "--{}\r\nContent-Disposition: form-data; name=\"sourceFile\"; filename=\"deploy.tar.gz\"\r\nContent-Type: application/octet-stream\r\n\r\n".format(boundary).encode()
        + tarball_data
        + "\r\n--{}--\r\n".format(boundary).encode()
    )

    url = "{}/api/v2/user/apps/appData/{}".format(CAPROVER_URL, app_name)
    headers = {
        "Content-Type": "multipart/form-data; boundary={}".format(boundary),
        "x-captain-auth": token,
        "Content-Length": str(len(body)),
    }
    req = urllib.request.Request(url, body, headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("  ERREUR: {}".format(e.read().decode()))
        return None


def main():
    print("=" * 55)
    print("  CORRECTION EMAIL + PROXY DIRECTUS")
    print("=" * 55)

    # --- Login ---
    print("\n1. Authentification...")
    r = api_call("/api/v2/login", {"password": CAPROVER_PASSWORD})
    token = r["data"]["token"]
    print("   Token OK")

    # --- Mise à jour des variables + activation proxy ---
    print("\n2. Correction email admin + activation sous-domaine...")
    r = api_call("/api/v2/user/apps/appDefinitions/update", {
        "appName": APP_NAME,
        "instanceCount": 1,
        "envVars": ENV_VARS,
        "volumes": VOLUMES,
        "containerHttpPort": 8055,
        # Activation du proxy CapRover (sous-domaine directus.*)
        "forceSsl": False,
        "websocketSupport": False,
        "notExposeAsWebApp": False,
    }, token)
    print("   Status update: {}".format(r.get("status")))

    # --- Redéploiement avec image correcte ---
    print("\n3. Redéploiement avec email corrigé (admin@origine.dev)...")
    r = deploy_tarball(APP_NAME, DOCKER_IMAGE, token)
    if r:
        print("   Status deploy: {}".format(r.get("status")))
        print("   {}".format(r.get("description", "")))

    # --- Attente démarrage ---
    print("\n4. Attente démarrage (120 secondes)...")
    for i in range(12):
        time.sleep(10)
        print("   {}s...".format((i + 1) * 10))

    # --- Test HTTP ---
    print("\n5. Test HTTP Directus (port 8055)...")
    import subprocess
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8055/server/health"],
        capture_output=True, text=True
    )
    print("   HTTP Status port 8055: {}".format(r.stdout))

    # Test via proxy CapRover
    r2 = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-H", "Host: directus.37.187.219.15.nip.io", "http://localhost"],
        capture_output=True, text=True
    )
    print("   HTTP Status via proxy: {}".format(r2.stdout))

    print("\n=== RÉSUMÉ ===")
    print("URL admin: http://directus.37.187.219.15.nip.io")
    print("Email:     admin@origine.dev")
    print("MDP:       Origine@Admin2026!")


if __name__ == "__main__":
    main()
