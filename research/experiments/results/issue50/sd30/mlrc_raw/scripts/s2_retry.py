#!/usr/bin/env python3
"""Second pass: re-fetch ONLY the S2 responses that came back as error records
(http_error / transport_error / empty). Longer backoff. Raw saved before reading."""
import json, os, time, urllib.parse, urllib.request

OUT = "/tmp/sd20_rev/c3c4/raw/s2_resolution"

def needs_retry(path):
    try:
        j = json.loads(open(path).read())
    except Exception:
        return True
    if "http_error" in j or "transport_error" in j or not j.get("data"):
        return True
    return False

def fetch(url, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mlrc-witness-inventory/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 + 10 * i)
                continue
            return json.dumps({"http_error": e.code})
        except Exception as e:
            time.sleep(10)
            if i == tries - 1:
                return json.dumps({"transport_error": str(e)})
    return json.dumps({"transport_error": "exhausted"})

def query_of(slug):
    # rebuild query from the request context file written by pass 1 summary;
    # fall back to slug-stem title from _summary.json
    with open(f"{OUT}/_summary.json") as f:
        s = json.load(f)
    return s.get(slug, {}).get("query") if isinstance(s.get(slug), dict) else None

QUERIES = json.load(open("/tmp/sd20_rev/c3c4/s2_queries.json"))
BASE = "https://api.semanticscholar.org/graph/v1/paper/search?query={q}&fields=title,externalIds,venue,year&limit=5"

todo = [s for s in QUERIES if os.path.exists(f"{OUT}/{s}.json") and needs_retry(f"{OUT}/{s}.json")]
print("retry queue:", todo, flush=True)
for slug in todo:
    url = BASE.format(q=urllib.parse.quote(QUERIES[slug]))
    body = fetch(url)
    open(f"{OUT}/{slug}.json", "w").write(body)
    ok = '"data"' in body
    print(f"{slug}: {'OK' if ok else 'STILL-FAIL'} ({len(body)}B)", flush=True)
    time.sleep(5)
print("PASS2 DONE", flush=True)
