import urllib.request
import sys

try:
    resp = urllib.request.urlopen("http://kuma.37.187.219.15.nip.io", timeout=10)
    print("STATUS:", resp.status)
    print("BODY:", resp.read(200).decode("utf-8"))
except Exception as e:
    print("ERROR:", e)
