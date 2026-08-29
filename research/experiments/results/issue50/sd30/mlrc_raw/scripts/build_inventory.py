#!/usr/bin/env python3
"""Assemble /tmp/sd20_rev/c3c4/mlrc_witness_inventory.json from the distilled
forum rows (4 jsonl batches) + saved arXiv/S2 resolution raw files.
Every arXiv id is traceable to a saved raw file under raw/. No id from memory."""
import json, os

BASE = "/tmp/sd20_rev/c3c4"
rows = []
for f in ["raw/forums_distilled.jsonl", "raw/forums_distilled_batch2.jsonl",
          "raw/forums_distilled_batch3.jsonl", "raw/forums_distilled_batch4.jsonl"]:
    for line in open(f"{BASE}/{f}"):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
assert len(rows) == 39, f"expected 39 rows, got {len(rows)}"

# Corrected 5L90cl0xtf row: batch-1 entry came from an unrendered JS shell
# (forum_5L90cl0xtf.html has 0 citation_ meta tags; control 'openreview' matched 6x).
# Authoritative source: live forum re-fetch 2026-08-29 (webReader, raw text in transcript).
for r in rows:
    if r["forum_id"] == "5L90cl0xtf":
        r.update({
            "report_title": "Revisiting CroPA: A Reproducibility Study and Enhancements for Cross-Prompt Adversarial Transferability in Vision-Language Models",
            "authors": "Atharv Mittal; Agam Pandey; Amritanshu Tiwari; Sukrit Jindal; Swadesh Swain",
            "code_url": "https://github.com/Swadesh06/Revisting_CroPA",
            "online_date": "2025/02/27",
            "submission_number": "4323",
            "original_title": "An Image is Worth 1000 Lies: Adversarial Transferability Across Prompts on Vision-Language Models (CroPA)",
            "original_venue": "named in report abstract; venue per original's own publication (not restated in abstract)",
            "verdict_prose": "validating the Cross-Prompt Attack (CroPA) and confirming its superior cross-prompt transferability compared to existing baselines ... validates the original results",
            "verdict_class_derived": "positive",
            "per_claim": "CroPA superiority over baselines=VALIDATED across Flamingo, BLIP-2, InstructBLIP (+LLaVA extension)",
            "row_correction": "batch-1 fields replaced from live re-fetch 2026-08-29; original batch-1 read came from an unrendered OpenReview JS shell and attributed a wrong try-on title",
        })

# slug -> (arxiv_id, resolver, match_type, resolved_title, raw_file)
ARX = {
 "cropa":           ("2403.09766","arxiv_api","exact_title","An Image Is Worth 1000 Lies: Adversarial Transferability across Prompts on Vision-Language Models","arxiv_resolution/cropa.xml"),
 "moderntcn":       (None,None,"not_found_on_arxiv",None,None),
 "mrl_dense":       ("2304.14522","arxiv_api","authors+content (arXiv title differs from SIGIR title; authors Zamani & Bendersky match report citation)","Multivariate Representation Learning for Information Retrieval","arxiv_resolution/refine3_mrl.xml"),
 "fvit":            ("2311.17983","arxiv_api","exact_title","Improving Interpretation Faithfulness for Vision Transformers","arxiv_resolution/fvit.xml"),
 "nifa":            ("2406.03052","arxiv_api","concept (true title: Are Your Models Still Fair? Fairness Attacks on GNNs via Node Injection; method/venue/year align with report's Luo et al. 2024 KDD)","Are Your Models Still Fair? Fairness Attacks on Graph Neural Networks via Node Injection","arxiv_resolution/refine_nifa.xml"),
 "user_item_fair":  ("2412.04466","arxiv_api","exact_title","User-item fairness tradeoffs in recommendations","arxiv_resolution/user_item_fair.xml"),
 "comp_mechanisms": ("2402.11655","arxiv_api+s2_agree","exact_title","Competition of Mechanisms: Tracing How Language Models Handle Facts and Counterfactuals","arxiv_resolution/comp_mechanisms.xml"),
 "llm_negotiation": ("2309.17234","arxiv_api","exact_title","Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation","arxiv_resolution/llm_negotiation.xml"),
 "nonmarkov_fair":  ("2312.04772","arxiv_api","exact_title","Remembering to Be Fair: Non-Markovian Fairness in Sequential Decision Making","arxiv_resolution/nonmarkov_fair.xml"),
 "slice":           (None,None,"not_found_on_arxiv (S-LIME 2106.07875 is a DIFFERENT 2021 paper by different authors; not assigned)",None,None),
 "gnnboundary":     (None,None,"not_found_on_arxiv",None,None),
 "dn_cbm":          ("2407.14499","arxiv_api","title_variant (arXiv title: Discover-then-Name: Task-Agnostic Concept Bottlenecks via Automated Concept Discovery; report cites Rao et al. 2024)","Discover-then-Name: Task-Agnostic Concept Bottlenecks via Automated Concept Discovery","arxiv_resolution/refine2_dn_cbm.xml"),
 "scoreable_games": (None,None,"original_not_on_arxiv (only the [Re] report itself, arXiv 2602.18230, surfaces; Abdelnabi et al. original not found)",None,None),
 "calibrated_dec":  ("2405.01196","arxiv_api","exact_title","Decoupling Feature Extraction and Classification Layers for Calibrated Neural Networks","arxiv_resolution/calibrated_dec.xml"),
 "gnninterpreter":  ("2209.07924","arxiv_api","title_prefix (arXiv title: GNNInterpreter: A Probabilistic Generative Model-Level Explanation for GNNs)","GNNInterpreter: A Probabilistic Generative Model-Level Explanation for Graph Neural Networks","arxiv_resolution/gnninterpreter.xml"),
 "tgnn_explainer":  (None,None,"not_found_on_arxiv",None,None),
 "rl_trajectories": ("2305.04073","arxiv_api","exact_title","Explaining RL Decisions with Trajectories","arxiv_resolution/rl_trajectories.xml"),
 "fairac":          ("2302.12977","arxiv_api","exact_title","Fair Attribute Completion on Graph with Missing Attributes","arxiv_resolution/fairac.xml"),
 "pcbm":            ("2205.15480","arxiv_api","exact_title","Post-hoc Concept Bottleneck Models","arxiv_resolution/pcbm.xml"),
 "extremalmask":    ("2305.18840","arxiv_api","exact_title","Learning Perturbations to Explain Time Series Predictions","arxiv_resolution/extremalmask.xml"),
 "cs_shapley":      ("2211.06800","arxiv_api","title_variant (arXiv: Class-wise Shapley Values...; report cites Classwise-Shapley)","CS-Shapley: Class-wise Shapley Values for Data Valuation in Classification","arxiv_resolution/refine2_cs_shapley.xml"),
 "iti_gen":         ("2309.05569","arxiv_api","exact_title","ITI-GEN: Inclusive Text-to-Image Generation","arxiv_resolution/iti_gen.xml"),
 "robust_fair_clust":("2210.01953","arxiv_api","exact_title","Robust Fair Clustering: A Novel Fairness Attack and Defense Framework","arxiv_resolution/robust_fair_clust.xml"),
 "cuda":            ("2302.05499","arxiv_api","exact_title (report mis-cites 'Visual'; arXiv: for Long-Tailed Recognition)","CUDA: Curriculum of Data Augmentation for Long-Tailed Recognition","arxiv_resolution/refine_cuda.xml"),
 "lico":            ("2310.09821","arxiv_api","exact_title","LICO: Explainable Models with Language-Image Consistency","arxiv_resolution/lico.xml"),
 "equal_improv":    ("2210.06732","arxiv_api","exact_title","Equal Improvability: A New Fairness Notion Considering the Long-Term Impact","arxiv_resolution/equal_improv.xml"),
 "cot_faithful":    ("2307.13702","arxiv_api","exact_title","Measuring Faithfulness in Chain-of-Thought Reasoning","arxiv_resolution/cot_faithful.xml"),
 "concept_ablation":("2303.13516","arxiv_api","exact_title","Ablating Concepts in Text-to-Image Diffusion Models","arxiv_resolution/concept_ablation.xml"),
 "model_guidance":  ("2303.11932","arxiv_api","exact_title","Studying How to Efficiently and Effectively Guide Models with Explanations","arxiv_resolution/model_guidance.xml"),
 "graphair":        (None,None,"not_found_on_arxiv (only the [Re] report 2409.00421 and unrelated papers surface; Ling et al. 2022 original not found)",None,None),
}

SLUG_FORUMS = {
 "cropa":["5L90cl0xtf"],"moderntcn":["R20kKdWmVZ"],"mrl_dense":["wF3ZtSlOcT"],
 "fvit":["Z0DhgU8fBt","a0rytDAGUD"],"nifa":["l5fXUKi8GO"],
 "user_item_fair":["vltzxxhzLU"],"comp_mechanisms":["VCG6j3tcAA","15keyzQj9h"],
 "llm_negotiation":["MTrhFmkC45"],"nonmarkov_fair":["H6DtMcZf5s"],
 "slice":["vKUPXuEzj8"],"gnnboundary":["kEUvWFHEsn"],"dn_cbm":["946cT3Jsq5"],
 "scoreable_games":["BVH81SAAh2"],"calibrated_dec":["5Hwzd48ILf"],
 "gnninterpreter":["8cYcR23WUo"],"tgnn_explainer":["FI1XvwpchC","9M2XqvH2SB"],
 "rl_trajectories":["JQoWmeNaC2","QdeBbK5CSh"],"fairac":["ccDi5jtSF7"],
 "pcbm":["8UfhCZjOV7"],"extremalmask":["fCNqD2IuoD","nPZgtpfgIx"],
 "cs_shapley":["srFEYJkqD7"],"iti_gen":["d3Vj360Wi2"],
 "robust_fair_clust":["Xu1sEPhjqH","H1hLNjwrGy"],"cuda":["Wm6d44I8St"],
 "lico":["Mf1H8X5DVb"],"equal_improv":["Yj8fUQGXXL"],"cot_faithful":["ydcrP55u2e"],
 "concept_ablation":["TYYApLzjaQ"],"model_guidance":["9ZzASCVhDF"],
 "graphair":["4WiqHopXQX"],
}
NORESOLVE = {"1WqLLYgBNt":"no single named original (original method paper)",
             "FEEKR0Vl9s":"multi-paper empirical study, no single original",
             "BbvSU02jLg":"original not named in abstract"}

forum2arx = {}
for slug, forums in SLUG_FORUMS.items():
    for fid in forums:
        forum2arx[fid] = slug

FULL = {"positive","positive_with_minor_exceptions","positive_with_qualification",
        "positive_with_qualifications","positive_limited_scope","positive_partial",
        "positive_with_nuance","partial_positive","positive_core_negative_generalization"}
PARTIAL = {"mixed","mixed_positive","partial"}
NO = {"negative","negative_mixed","mixed_negative"}
NA = {"no_single_original","verdict_not_stated_in_abstract"}

out_rows = []
for r in rows:
    fid = r["forum_id"]
    slug = forum2arx.get(fid)
    if slug:
        aid, resolver, match, rtitle, rawfile = ARX[slug]
    elif fid in NORESOLVE:
        aid = resolver = match = rtitle = rawfile = None
        match = NORESOLVE[fid]
    else:
        raise RuntimeError(f"unmapped forum {fid}")
    vc = r.get("verdict_class_derived")
    bin_ = "FULL" if vc in FULL else "PARTIAL" if vc in PARTIAL else "NO" if vc in NO else "NOT_APPLICABLE" if vc in NA else "UNMAPPED"
    out_rows.append({
        "openreview_forum_id": fid,
        "cycle": r["cycle"],
        "report_title": r["report_title"],
        "report_authors": r.get("authors"),
        "tmlr_online_date": r.get("online_date"),
        "submission_number": r.get("submission_number"),
        "note_fields_non_verdict": r.get("cert_field"),
        "code_url": r.get("code_url"),
        "verdict_field": "Abstract (prose), no structured field",
        "verdict_class_analyst": vc,
        "verdict_bin": bin_,
        "verdict_prose_extract": r.get("verdict_prose"),
        "per_claim_summary": r.get("per_claim"),
        "original_title_as_cited": r.get("original_title"),
        "original_venue_as_cited": r.get("original_venue"),
        "original_arxiv_id": aid,
        "arxiv_resolver": resolver,
        "arxiv_match_type": match,
        "original_resolved_title": rtitle,
        "arxiv_evidence_raw_file": rawfile,
        "source_url": f"https://openreview.net/forum?id={fid}",
    })

bins = {}
for rr in out_rows:
    bins[rr["verdict_bin"]] = bins.get(rr["verdict_bin"], 0) + 1
extractable = sum(v for k, v in bins.items() if k in ("FULL","PARTIAL","NO"))
resolved_ids = {k: v for k, v in ARX.items() if v[0]}
distinct_named = len(SLUG_FORUMS)  # 30
dup_pairs = {s: f for s, f in SLUG_FORUMS.items() if len(f) == 2}

inventory = {
  "witness_source": "MLRC (Machine Learning Reproducibility Challenge) Journal-Track reports published in TMLR via OpenReview",
  "scope": {
    "in_scope_cycles": ["MLRC 2025 Journal Track (17 reports, TMLR 2025)", "MLRC 2023 Journal Track (22 reports, TMLR 2024/02-2024/03)"],
    "out_of_scope": "reproml.org MLRC 2022 section (44 entries) - excluded per task scope; ReScience volumes pre-2023 - not ingested (PDF-only listing page)"
  },
  "counts": {
    "reports_total": len(out_rows),
    "reports_with_extractable_verdict": extractable,
    "reports_not_applicable_or_not_extractable": bins.get("NOT_APPLICABLE", 0),
    "verdict_bins": bins,
    "distinct_reproduction_targets": distinct_named + 1,
    "distinct_targets_title_resolvable": distinct_named,
    "targets_resolved_to_arxiv_id": len(resolved_ids),
    "targets_not_found_on_arxiv": distinct_named - len(resolved_ids),
    "share_of_resolvable_targets_in_arxiv_space": round(len(resolved_ids)/distinct_named, 3),
    "reports_whose_original_has_arxiv_id": sum(1 for rr in out_rows if rr["original_arxiv_id"]),
  },
  "duplicate_original_pairs": [
    {"original_slug": s, "witness_forum_ids": f,
     "verdicts": [next(x["verdict_bin"] for x in out_rows if x["openreview_forum_id"] == i) for i in f]}
    for s, f in dup_pairs.items()
  ],
  "verdict_field_semantics": {
    "structured_verdict_field_exists": False,
    "verdict_truth_source": "Abstract prose, read and binned by analyst (PROSE_DERIVED); per-claim breakdowns when the abstract states them",
    "non_verdict_note_fields_documented": [
      "Event Certifications: reproml.org/<cycle>/Journal_Track (participation/process marker)",
      "Certifications: Reproducibility Certification (process marker, present on a subset incl. negative-verdict reports)",
      "Code: <repo url>", "Submission Number", "Assigned Action Editor",
      "citation_* meta tags (title/abstract/authors/date)",
      "MLRC 2025 medals (PDF 'Reproducibility Certificates' prize: standard/gold/platinum) - EXCLUDED as truth label per citation_or_prize_metric_is_truth_label=false"
    ],
    "bin_definitions": {
      "FULL": sorted(FULL), "PARTIAL": sorted(PARTIAL), "NO": sorted(NO), "NOT_APPLICABLE": sorted(NA)
    },
    "binning_caveat": "FULL includes partial_positive (main effect confirmed, superiority partial) and positive_core_negative_generalization (core claims reproduced; the negative part concerns the reproducers' own extension) - the fine per-report class is carried in verdict_class_analyst; rebinning is a one-line change"
  },
  "source_provenance": {
    "forum_listing_endpoints": [
      "https://openreview.net/group?id=reproml.org/MLRC/2025/Journal_Track (listing fetch)",
      "https://openreview.net/group?id=reproml.org/MLRC/2023/Journal_Track (listing fetch)",
      "39 individual https://openreview.net/forum?id=<id> pages fetched 2026-08-29 (webReader; distilled rows in raw/forums_distilled*.jsonl)"
    ],
    "arxiv_resolution": "export.arxiv.org/api/query title/phrase searches, 2026-08-29; raw Atom XML per query in raw/arxiv_resolution/ (pass1 _summary.json + refine/refine2/refine3 files)",
    "semantic_scholar_resolution": "api.semanticscholar.org/graph/v1/paper/search, 2026-08-29; raw JSON per query in raw/s2_resolution/ (unauthenticated shared pool: intermittent HTTP 429; cross-check only - see s2_status)",
    "api2_openreview_net": "CANNOT_CHECK: APIv2 notes endpoint not queried directly (reqId 2026-08-29-7135377); verdict/claim data taken from rendered forum pages instead",
    "cropa_row_correction": "5L90cl0xtf batch-1 row replaced from live re-fetch; earlier save was an unrendered JS shell (0 citation_ meta tags)"
  },
  "alternative_witness_sources_assessed": [
    {"source": "ReScience C (rescience.github.io)", "feasibility": "arXiv-native-ish and highly structured: the saved listing page (raw/rescience_read.html, 486KB) carries per-article DOI (237 doi.org refs), code repo (667 github refs) and review-archive links (1189 zenodo refs); but originals are typically non-arXiv computational-science papers (eLife/PLoS CB), so it witnesses a different original-id space",
     "effort_share": "one-line feasibility from already-saved raw page; deeper use would need per-article page fetches"},
    {"source": "NeurIPS Datasets & Benchmarks / reproduction tracks", "feasibility": "NOT_CHECKED this session (outside <=20% alternative-source effort); OpenReview-hosted so the same forum-scraping method applies, but no per-claim verdict convention exists"}
  ],
  "rows": out_rows,
}

with open(f"{BASE}/mlrc_witness_inventory.json", "w") as f:
    json.dump(inventory, f, indent=1, ensure_ascii=False)
print("counts:", json.dumps(inventory["counts"], indent=1))
print("dup pairs:", [(d["original_slug"], d["verdicts"]) for d in inventory["duplicate_original_pairs"]])
print("wrote", f"{BASE}/mlrc_witness_inventory.json")
