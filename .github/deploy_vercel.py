import json
import os
import sys
import time
import hashlib
import requests

TOKEN = os.environ["VERCEL_TOKEN"]
PROJECT = os.environ["VERCEL_PROJECT"]
OUT = "vercel-prebuilt/output"
API = "https://api.vercel.com"
HEAD = {"Authorization": f"Bearer {TOKEN}"}

files = []
for root, _dirs, names in os.walk(OUT):
    for name in names:
        path = os.path.join(root, name)
        rel = os.path.relpath(path, "vercel-prebuilt")
        data = open(path, "rb").read()
        files.append((rel, len(data), hashlib.sha1(data).hexdigest(), data))

print(f"files={len(files)} bytes={sum(f[1] for f in files)}", flush=True)
for rel, size, sha, data in files:
    r = requests.post(
        API + "/v2/files",
        headers={**HEAD, "Content-Type": "application/octet-stream",
                 "x-now-digest": sha, "x-now-size": str(size)},
        data=data, timeout=300,
    )
    if r.status_code not in (200, 409):
        print("upload failed", rel, r.status_code, r.text[:300], flush=True)
        sys.exit(1)
print("upload complete", flush=True)

payload = {
    "name": "universal-system-v2",
    "project": PROJECT,
    "prebuilt": True,
    "version": 2,
    "files": [{"file": rel, "size": size, "mode": 0o100644, "sha": sha}
              for rel, size, sha, _ in files],
}
r = requests.post(API + "/v13/deployments", headers={**HEAD, "Content-Type": "application/json"},
                  json=payload, timeout=300)
print("create", r.status_code, flush=True)
d = r.json()
if r.status_code >= 400 or d.get("error"):
    print(json.dumps(d.get("error") or d)[:1000], flush=True)
    sys.exit(1)
print("id=" + d.get("id", ""), flush=True)

deadline = time.time() + 600
while time.time() < deadline:
    time.sleep(10)
    s = requests.get(API + "/v13/deployments/" + d["id"], headers=HEAD, timeout=60).json()
    state = s.get("readyState") or s.get("status")
    print("state=" + str(state), flush=True)
    if state in ("READY", "ERROR", "CANCELED"):
        break
else:
    print("timeout", flush=True)
    sys.exit(1)

if state != "READY":
    print(json.dumps(s)[:1000], flush=True)
    sys.exit(1)
url = "https://" + s["url"]
print("URL=" + url, flush=True)
print("ALIAS=" + str(s.get("alias")), flush=True)
