#!/usr/bin/env python3
"""Parallel resolver: arXiv export API (export.arxiv.org), title search.
Raw Atom XML saved to raw/arxiv_resolution/<slug>.xml BEFORE any parsing.
arXiv ids only ever taken from the saved <id> elements. 1 req / 3.2s courtesy rate."""
import json, os, re, time, urllib.parse, urllib.request

OUT = "/tmp/sd20_rev/c3c4/raw/arxiv_resolution"
os.makedirs(OUT, exist_ok=True)
QUERIES = json.load(open("/tmp/sd20_rev/c3c4/s2_queries.json"))

API = "http://export.arxiv.org/api/query?search_query={q}&max_results=3"

def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

for slug, title in QUERIES.items():
    out = f"{OUT}/{slug}.xml"
    if os.path.exists(out) and os.path.getsize(out) > 500:
        continue
    # exact-title search; colon in title must be handled (arXiv treats it in quotes fine when encoded)
    q = 'ti:"%s"' % title
    url = API.format(q=urllib.parse.quote(q))
    body = None
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mlrc-witness-inventory/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read().decode("utf-8", "replace")
            break
        except Exception as e:
            if i == 3:
                body = f"<error>{e}</error>"
            time.sleep(8)
    open(out, "w").write(body)
    time.sleep(3.2)

# parse ONLY from saved files
entries_re = re.compile(r"<entry>(.*?)</entry>", re.S)
id_re = re.compile(r"<id>http://arxiv.org/abs/([^<v]+?)(v\d+)?</id>")
t_re = re.compile(r"<title>(.*?)</title>", re.S)
pub_re = re.compile(r"<published>(\d{4})")
summary = {}
for slug in QUERIES:
    xml = open(f"{OUT}/{slug}.xml").read()
    hits = []
    for e in entries_re.findall(xml)[:3]:
        m = id_re.search(e)
        tm = t_re.search(e)
        ym = pub_re.search(e)
        if m and tm:
            t = re.sub(r"\s+", " ", tm.group(1)).strip()
            hits.append({"arxiv": m.group(1), "title": t,
                         "year": ym.group(1) if ym else None,
                         "exact_match": norm(t) == norm(QUERIES[slug])})
    summary[slug] = {"query": QUERIES[slug], "hits": hits}
json.dump(summary, open(f"{OUT}/_summary.json", "w"), indent=1, ensure_ascii=False)
n_exact = sum(1 for v in summary.values() if v["hits"] and v["hits"][0]["exact_match"])
n_any = sum(1 for v in summary.values() if v["hits"])
print(f"arXiv API: {n_any}/30 have hits, {n_exact}/30 top-hit exact-title match")
for slug, v in summary.items():
    if v["hits"]:
        h = v["hits"][0]
        print(f"  {slug:<18} {h['arxiv']:<12} exact={h['exact_match']} {h['title'][:66]}")
    else:
        print(f"  {slug:<18} NO-HIT")
