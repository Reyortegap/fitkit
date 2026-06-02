#!/usr/bin/env python3
"""Genera ilustraciones FITKIT vía nanobananaapi.ai (async + polling)."""
import os, sys, json, time, urllib.request, urllib.error

API = "https://api.nanobananaapi.ai/api/v1/nanobanana"
KEY = os.environ.get("NANO_KEY", "").strip()
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

STYLE = (
    "Flat editorial vector illustration, strict duotone palette: bright neon lime green and "
    "near-black charcoal only. Solid dark charcoal background. High contrast, clean bold geometric "
    "shapes, flat solid shadows, no photographic gradients, no realistic colors. Centered single "
    "subject, athletic premium fitness brand style, minimal negative space. ABSOLUTELY NO text, "
    "no letters, no numbers, no hex codes, no logo, no watermark. Subject: "
)

def post(prompt):
    body = json.dumps({"prompt": prompt, "type": "TEXTTOIAMGE", "numImages": 1}).encode()
    req = urllib.request.Request(API + "/generate", data=body, method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def find_task_id(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == "taskid" and isinstance(v, str):
                return v
            t = find_task_id(v)
            if t:
                return t
    return None

def poll(task_id, tries=60, wait=5):
    url = f"{API}/record-info?taskId={task_id}"
    for _ in range(tries):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        data = d.get("data", d)
        flag = data.get("successFlag", d.get("successFlag"))
        if flag == 1:
            resp = data.get("response", {}) or {}
            url_img = resp.get("resultImageUrl") or (resp.get("resultUrls") or [None])[0]
            return url_img
        if flag in (2, 3):
            raise RuntimeError(f"generation failed flag={flag}: {json.dumps(d)[:300]}")
        time.sleep(wait)
    raise TimeoutError("polling timed out")

def download(url, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())

def generate(subject, out):
    res = post(STYLE + subject)
    tid = find_task_id(res)
    if not tid:
        raise RuntimeError(f"no taskId in response: {json.dumps(res)[:400]}")
    print(f"  task {tid} …", flush=True)
    img = poll(tid)
    if not img:
        raise RuntimeError("no image url after success")
    download(img, out)
    print(f"  saved {out}", flush=True)

if __name__ == "__main__":
    if not KEY:
        sys.exit("NANO_KEY env var missing")
    if len(sys.argv) >= 3:
        generate(sys.argv[1], sys.argv[2])
    else:
        sys.exit("usage: gen.py 'subject' output.png")
