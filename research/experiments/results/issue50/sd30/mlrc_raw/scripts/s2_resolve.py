#!/usr/bin/env python3
"""Resolve MLRC reproduced-original titles to arXiv ids via Semantic Scholar Graph API.

Protocol: raw JSON response saved to raw/s2_resolution/<slug>.json BEFORE any reading.
No arXiv id is ever asserted from memory; only externalIds.ArXiv in the saved response.
Rate limit: ~1 req/s unauthenticated -> sleep 1.2s between queries, retry on 429.
"""
import json, os, time, urllib.parse, urllib.request, sys

OUT = "/tmp/sd20_rev/c3c4/raw/s2_resolution"
os.makedirs(OUT, exist_ok=True)

# slug -> exact query string (original paper title as named by the reproducibility report,
# parenthetical analyst suffixes stripped)
QUERIES = {
 "cropa":            "An Image is Worth 1000 Lies: Adversarial Transferability Across Prompts on Vision-Language Models",
 "moderntcn":        "ModernTCN: A Modern Pure Convolution Structure for General Time Series Analysis",
 "mrl_dense":        "Leveraging Multivariate Representations for Dense Retrieval",
 "fvit":             "Improving Interpretation Faithfulness for Vision Transformers",
 "nifa":             "Node Injection-based Fairness Attack on Graph Neural Networks",
 "user_item_fair":   "User-item fairness tradeoffs in recommendations",
 "comp_mechanisms":  "Competition of Mechanisms: Tracing How Language Models Handle Facts and Counterfactuals",
 "llm_negotiation":  "Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation",
 "nonmarkov_fair":   "Remembering to Be Fair: Non-Markovian Fairness in Sequential Decision Making",
 "slice":            "SLICE: Stabilized LIME for Consistent Explanations for Image Classification",
 "gnnboundary":      "GNNBoundary: Towards Explaining Graph Neural Networks Through the Lens of Decision Boundaries",
 "dn_cbm":           "Discover-then-Name: Towards Adapting Concept Bottleneck Models without Human-labeled Data",
 "scoreable_games":  "Benchmarking LLM Capabilities in Negotiation through Scoreable Games",
 "calibrated_dec":   "Decoupling Feature Extraction and Classification Layers for Calibrated Neural Networks",
 "gnninterpreter":   "GNNInterpreter",
 "tgnn_explainer":   "Explaining Temporal Graph Models through an Explorer-Navigator Framework",
 "rl_trajectories":  "Explaining RL Decisions with Trajectories",
 "fairac":           "Fair Attribute Completion on Graph with Missing Attributes",
 "pcbm":             "Post-Hoc Concept Bottleneck Models",
 "extremalmask":     "Learning Perturbations to Explain Time Series Predictions",
 "cs_shapley":       "CS-Shapley: Classwise-Shapley Values for Data Valuation",
 "iti_gen":          "ITI-GEN: Inclusive Text-to-Image Generation",
 "robust_fair_clust":"Robust Fair Clustering: A Novel Fairness Attack and Defense Framework",
 "cuda":             "CUDA: Curriculum of Data Augmentation on Long-Tailed Visual Recognition",
 "lico":             "LICO: Explainable Models with Language-Image Consistency",
 "equal_improv":     "Equal Improvability: A New Fairness Notion Considering the Long-Term Impact",
 "cot_faithful":     "Measuring Faithfulness in Chain-of-Thought Reasoning",
 "concept_ablation": "Ablating Concepts in Text-to-Image Diffusion Models",
 "model_guidance":   "Studying How to Efficiently and Effectively Guide Models with Explanations",
 "graphair":         "Learning Fair Graph Representations Via Automated Data Augmentations",
}

BASE = "https://api.semanticscholar.org/graph/v1/paper/search?query={q}&fields=title,externalIds,venue,year&limit=5"

def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mlrc-witness-inventory/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8"), r.status
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                time.sleep(10 * (i + 1)); continue
            return json.dumps({"http_error": e.code}), e.code
        except Exception as e:
            if i == tries - 1:
                return json.dumps({"transport_error": str(e)}), -1
            time.sleep(5)
    return json.dumps({"transport_error": "exhausted"}), -1

results = {}
for slug, q in QUERIES.items():
    url = BASE.format(q=urllib.parse.quote(q))
    body, status = fetch(url)
    with open(f"{OUT}/{slug}.json", "w") as f:
        f.write(body)
    try:
        j = json.loads(body)
    except Exception:
        j = {"parse_error": True}
    results[slug] = {"query": q, "status": status, "n": j.get("total")}
    time.sleep(1.2)

# Read back ONLY from the saved files (protocol: read after save)
print(f"{'slug':<18} {'status':<7} {'hits':<6} arXiv/year/venue/title-of-top-hit")
summary = {}
for slug in QUERIES:
    with open(f"{OUT}/{slug}.json") as f:
        j = json.load(f)
    top = (j.get("data") or [None])[0]
    if not top:
        summary[slug] = None
        print(f"{slug:<18} {results[slug]['status']:<7} {str(results[slug]['n']):<6} NO-HIT")
        continue
    ax = (top.get("externalIds") or {}).get("ArXiv")
    summary[slug] = {"s2_title": top.get("title"), "arxiv": ax,
                     "venue": top.get("venue"), "year": top.get("year"),
                     "query": QUERIES[slug]}
    print(f"{slug:<18} {results[slug]['status']:<7} {str(results[slug]['n']):<6} {ax or '-'} / {top.get('year')} / {str(top.get('venue'))[:24]} / {str(top.get('title'))[:70]}")

with open(f"{OUT}/_summary.json", "w") as f:
    json.dump(summary, f, indent=1, ensure_ascii=False)
print("\nsaved:", f"{OUT}/_summary.json")
