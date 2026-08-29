#!/usr/bin/env python3
"""Final arXiv attempts for stubborn slugs + S2 pass-2 retry integration is separate.
Raw saved to raw/arxiv_resolution/refine3_<slug>.xml BEFORE parsing."""
import json, os, re, time, urllib.parse, urllib.request

OUT = "/tmp/sd20_rev/c3c4/raw/arxiv_resolution"
API = "http://export.arxiv.org/api/query?search_query={q}&max_results=5"

R3 = {
 "moderntcn":    'all:"pure convolution structure"',
 "tgnn":         'all:"T-GNNExplainer"',
 "mrl":          'all:"multivariate representations" AND all:"dense retrieval"',
 "slice":        'all:"Stabilized LIME for Consistent"',
 "graphair":     'all:"Learning Fair Graph Representations"',
 "moderntcn_b":  'all:"general time series analysis" AND all:"pure convolution"',
}

for slug, q in R3.items():
    out = f"{OUT}/refine3_{slug}.xml"
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
for slug in R3:
    xml = open(f"{OUT}/refine3_{slug}.xml").read()
    print(f"== {slug}")
    n = 0
    for e in entries_re.findall(xml)[:5]:
        m, tm, ym = id_re.search(e), t_re.search(e), pub_re.search(e)
        if m and tm:
            t = re.sub(r"\s+", " ", tm.group(1)).strip()
            print(f"   {m.group(1):<12} {ym.group(1) if ym else '?'}  {t[:82]}")
            n += 1
    if not n:
        print("   NO-HIT")
