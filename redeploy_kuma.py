import urllib.request
import urllib.error
import json
import tarfile
import io

CAPROVER_URL = "http://captain.37.187.219.15.nip.io"
CAPROVER_PASSWORD = "captain42"
APP_NAME = "kuma"
DOCKER_IMAGE = "louislam/uptime-kuma:1"

def main():
    # Login
    req = urllib.request.Request(CAPROVER_URL + "/api/v2/login", json.dumps({"password": CAPROVER_PASSWORD}).encode("utf-8"), {"Content-Type": "application/json"})
    token = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))["data"]["token"]
    
    # Check what is going on by redeploying and seeing if we get an error
    captain_def = json.dumps({"schemaVersion": 2, "imageName": DOCKER_IMAGE}).encode("utf-8")
    tarball_buffer = io.BytesIO()
    with tarfile.open(fileobj=tarball_buffer, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="captain-definition")
        info.size = len(captain_def)
        tar.addfile(info, io.BytesIO(captain_def))
    tarball_data = tarball_buffer.getvalue()

    boundary = "----CapRoverBoundary8888"
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"sourceFile\"; filename=\"deploy.tar.gz\"\r\nContent-Type: application/octet-stream\r\n\r\n".encode()
        + tarball_data
        + f"\r\n--{boundary}--\r\n".encode()
    )

    url = f"{CAPROVER_URL}/api/v2/user/apps/appData/{APP_NAME}"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "x-captain-auth": token,
        "Content-Length": str(len(body)),
    }
    req = urllib.request.Request(url, body, headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            print("Deploy success:", resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Deploy error {e.code}:", e.read().decode("utf-8"))

if __name__ == "__main__":
    main()
