import urllib.request
import urllib.error
import json
import sys
import time
import tarfile
import io

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "kuma"
DOCKER_IMAGE = "louislam/uptime-kuma:1.23.13"

ENV_VARS = []

VOLUMES = [
    {"volumeName": "kuma-data", "containerPath": "/app/data"},
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
    print("  DEPLOIEMENT UPTIME KUMA SUR CAPROVER")
    print("=" * 55)

    print("\n1. Authentification...")
    r = api_call("/api/v2/login", {"password": CAPROVER_PASSWORD})
    token = r["data"]["token"]
    print("   Token OK")

    print("\n2. Création de l'application...")
    try:
        api_call("/api/v2/user/apps/appDefinitions/register", {"appName": APP_NAME, "hasPersistentData": True}, token)
        print("   Application créée avec succès.")
    except Exception as e:
        print("   Application existe probablement déjà.")

    print("\n3. Configuration des volumes et limites RAM...")
    node_override = json.dumps({"TaskTemplate":{"ContainerSpec":{"Resources":{"Limits":{"MemoryBytes":134217728}}}}})
    r = api_call("/api/v2/user/apps/appDefinitions/update", {
        "appName": APP_NAME,
        "instanceCount": 1,
        "envVars": ENV_VARS,
        "volumes": VOLUMES,
        "containerHttpPort": 3001, # Uptime Kuma écoute sur le 3001
        "forceSsl": False,
        "websocketSupport": True, # Kuma utilise des websockets
        "notExposeAsWebApp": False,
        "customNodeUpdateOverride": node_override
    }, token)
    print("   Status update: {}".format(r.get("status")))

    print("\n4. Déploiement de l'image (louislam/uptime-kuma:1.23.13)...")
    r = deploy_tarball(APP_NAME, DOCKER_IMAGE, token)
    if r:
        print("   Status deploy: {}".format(r.get("status")))

    print("\n5. Activation HTTPS...")
    try:
        api_call("/api/v2/user/apps/appDefinitions/enablebasedomainssl", {"appName": APP_NAME}, token)
        r = api_call("/api/v2/user/apps/appDefinitions/update", {
            "appName": APP_NAME,
            "instanceCount": 1,
            "envVars": ENV_VARS,
            "volumes": VOLUMES,
            "containerHttpPort": 3001,
            "forceSsl": True,
            "websocketSupport": True,
            "notExposeAsWebApp": False,
            "customNodeUpdateOverride": node_override
        }, token)
        print("   HTTPS activé.")
    except Exception as e:
        print("   HTTPS non activable ou déjà activé.")

    print("\n=== UPTIME KUMA DEPLOYE ===")
    print("URL: https://kuma.37.187.219.15.nip.io")

if __name__ == "__main__":
    main()
