#!/usr/bin/env python3
"""Time-boxed S2 retry: re-fetch error-record files only; 3 attempts each,
25/45s backoff; hard stop after 9 minutes. Raw saved before reading."""
import json, glob, os, time, urllib.parse, urllib.request

OUT = "/tmp/sd20_rev/c3c4/raw/s2_resolution"
QUERIES = json.load(open("/tmp/sd20_rev/c3c4/s2_queries.json"))
BASE = "https://api.semanticscholar.org/graph/v1/paper/search?query={q}&fields=title,externalIds,venue,year&limit=5"
DEADLINE = time.time() + 540

def fetch(url):
    for i in range(3):
        if time.time() > DEADLINE:
            return None
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mlrc-witness-inventory/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(25 + 20 * i); continue
            return json.dumps({"http_error": e.code})
        except Exception:
            time.sleep(15)
    return None

todo = []
for f in sorted(glob.glob(f"{OUT}/*.json")):
    slug = os.path.basename(f)[:-5]
    if slug.startswith('_'): continue
    d = json.load(open(f))
    if not d.get('data'):
        todo.append(slug)
print("retry queue:", len(todo), flush=True)
done_ok = 0
for slug in todo:
    if time.time() > DEADLINE:
        print("deadline hit, stopping", flush=True); break
    url = BASE.format(q=urllib.parse.quote(QUERIES[slug]))
    body = fetch(url)
    if body is None:
        print(f"{slug}: skipped (deadline)", flush=True); continue
    open(f"{OUT}/{slug}.json", "w").write(body)
    ok = '"data"' in body
    done_ok += ok
    print(f"{slug}: {'OK' if ok else 'still-429'}", flush=True)
    time.sleep(3)
print(f"retry recovered {done_ok} responses", flush=True)
