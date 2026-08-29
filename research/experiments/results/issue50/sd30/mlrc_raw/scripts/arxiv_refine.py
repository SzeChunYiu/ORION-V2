#!/usr/bin/env python3
"""Refinement pass for slugs whose exact-title arXiv search failed or hit the [Re]
report instead of the original. Token/fragment queries; raw saved to
raw/arxiv_resolution/refine_<slug>.xml BEFORE parsing."""
import json, os, re, time, urllib.parse, urllib.request

OUT = "/tmp/sd20_rev/c3c4/raw/arxiv_resolution"
API = "http://export.arxiv.org/api/query?search_query={q}&max_results=5"

REFINE = {
 "moderntcn":      'ti:ModernTCN',
 "mrl_dense":      'ti:"multivariate representations" AND ti:"dense retrieval"',
 "nifa":           'ti:"Node Injection" AND ti:fairness',
 "slice":          'ti:"Stabilized LIME"',
 "gnnboundary":    'ti:GNNBoundary',
 "dn_cbm":         'ti:"concept bottleneck" AND ti:"without human"',
 "tgnn_explainer": 'ti:"explorer" AND ti:"navigator" AND ti:"temporal graph"',
 "cs_shapley":     'ti:classwise AND ti:Shapley',
 "cuda":           'all:"Curriculum of Data Augmentation"',
 "graphair":       'ti:"fair graph representations" AND ti:augmentations',
 "scoreable_games":'all:"scoreable games"',
 "gnninterpreter": 'ti:GNNInterpreter',
}

def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

for slug, q in REFINE.items():
    out = f"{OUT}/refine_{slug}.xml"
    if not (os.path.exists(out) and os.path.getsize(out) > 500):
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

entries_re = re.compile(r"<entry>(.*?)</entry>", re.S)
id_re = re.compile(r"<id>http://arxiv.org/abs/([^<v]+?)(v\d+)?</id>")
t_re = re.compile(r"<title>(.*?)</title>", re.S)
pub_re = re.compile(r"<published>(\d{4})")

res = {}
for slug in REFINE:
    xml = open(f"{OUT}/refine_{slug}.xml").read()
    hits = []
    for e in entries_re.findall(xml)[:5]:
        m, tm, ym = id_re.search(e), t_re.search(e), pub_re.search(e)
        if m and tm:
            t = re.sub(r"\s+", " ", tm.group(1)).strip()
            hits.append({"arxiv": m.group(1), "title": t, "year": ym.group(1) if ym else None})
    res[slug] = hits
    print(f"== {slug}")
    for h in hits:
        print(f"   {h['arxiv']:<12} {h['year']}  {h['title'][:80]}")
    if not hits:
        print("   NO-HIT")
json.dump(res, open(f"{OUT}/_refine_summary.json", "w"), indent=1, ensure_ascii=False)
