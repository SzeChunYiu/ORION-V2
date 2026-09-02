#!/usr/bin/env python3
"""SD80 naturalistic case-matrix intake (PC-R7 / FM80 shared matrix), V1.

Builds hashed case records from lawful public witness sources, applies the
FM80 s3 eligibility ledger item-by-item, separates the tagger/arm-visible
record from the hidden outcome key, and freezes the 20-case tagging
calibration set. It does NOT tag: tagging is done by two independent
fresh-context taggers (see SD80_PC_R7_OBLIGATION_PROVENANCE_TAGGING_RULE_V1.md)
and merged by sd80_case_matrix_finalize.py.

Sources (snapshots under research/experiments/sd80/sources/raw, sha256 in the
output manifest):
  RPP    Reproducibility Project: Psychology, OSF ezcuj/ytpuq rpp_data.csv
  RPCB   Reproducibility Project: Cancer Biology, OSF e5nvr final-analysis csvs
  FORMAL 1000+ theorems project status file (mathlib4 docs/1000.yaml) + Wikidata
  MLRC   MLRC journal-track prose verdicts (SD30 inventory) - recorded, NOT counted
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import sys
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "research/experiments/sd80/sources/raw"
OUT = ROOT / "research/experiments/sd80"
SEED = 20260902
FORMAL_TAG_SAMPLE = 60
CALIBRATION = {"PSYCHOLOGY_RPP": 7, "CANCER_BIOLOGY_RPCB": 7, "FORMAL_MATHEMATICS_1000PLUS": 6}


def sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def fsha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_csv(name: str) -> list[dict]:
    with open(RAW / name, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def clean(d: dict, keys: list[str]) -> dict:
    return {k: (d.get(k) or "").strip() for k in keys}


# ----------------------------------------------------------------- RP:P
RPP_ASSESSMENT = {"1": "ENDORSEMENT", "2": "CONCERNS_INFORMED_JUDGMENT", "3": "CONCERNS_UNPUBLISHED_EVIDENCE",
                  "4": "CONCERNS_PUBLISHED_EVIDENCE", "9": "NO_RESPONSE"}
RPP_VISIBLE = ["Study Num", "Study Title (O)", "Authors (O)", "Journal (O)", "Volume (O)", "Issue (O)", "Pages (O)",
               "Descriptors (O)", "Discipline (O)", "Number of Studies (O)", "Replicated study number (R)",
               "Secondary data (O)", "Feasibility (O)", "Description of effect (O)", "Type of effect (O)",
               "Test statistic (O)", "N (O)", "Reported P-value (O)", "Effect size (O)", "Project URL",
               "Collect materials from authors", "Planned Sample", "Planned Power", "Original Author's Assessment",
               "OSC reviewer (O)"]
RPP_ARM_ONLY = ["Test statistic (R)", "N (R)", "P-value (R)", "# Tails (R)", "Type of analysis (R)", "Power (R)",
                "Effect Size (R)", "Direction (R)"]
RPP_HIDDEN = ["Replicate (R)", "Meta-analysis significant", "O within CI R", "Meta-analytic estimate (Fz)",
              "Findings similarity (R)", "Effect similarity (R)", "Surprise of outcome (R)", "Notes (R)",
              "Differences (R)", "Replication similarity (R)", "T_pval_USE..R.", "T_sign_R", "T_O_larger"]


def build_rpp(regs: dict) -> tuple[list[dict], dict]:
    rows = read_csv("rpp_data.csv")
    cases, hidden = [], {}
    for r in rows:
        title = (r.get("Study Title (O)") or "").strip()
        verdict = (r.get("Replicate (R)") or "").strip().lower()
        if not title or verdict not in ("yes", "no"):
            continue
        cid = f"RPP-{r['Study Num'].strip()}"
        m = re.search(r"osf\.io/(\w{5})", r.get("Project URL", ""))
        pid = m.group(1) if m else None
        reg = regs.get(pid, {}) if pid else {}
        vis = clean(r, RPP_VISIBLE)
        vis["Original Author's Assessment (decoded)"] = RPP_ASSESSMENT.get(vis["Original Author's Assessment"], "OTHER_OR_UNCODED")
        vis["OSC reviewer (O)"] = "PRESENT" if vis["OSC reviewer (O)"] else "ABSENT"
        vis["osf_project_id"] = pid
        vis["osf_registrations_public_api"] = {
            "status": reg.get("status", "NOT_QUERIED"),
            "count": len(reg.get("registrations", [])),
            "registrations": [{k: v for k, v in x.items() if k in ("id", "title", "date_registered", "supplement", "withdrawn")}
                              for x in reg.get("registrations", [])],
        }
        ma = (r.get("Meta-analysis significant") or "").strip()
        composite = ("STRICT_SUCCESS" if verdict == "yes" and ma == "1" else
                     "STRICT_FAILURE" if verdict == "no" and ma == "0" else "MIXED")
        hidden[cid] = {**clean(r, RPP_HIDDEN), "composite_witness_class": composite}
        arm_only = clean(r, RPP_ARM_ONLY)
        cases.append({
            "case_id": cid, "domain": "PSYCHOLOGY_RPP", "domain_class": "EMPIRICAL",
            "witness_class": "REGISTERED_REPLICATION_VERDICT",
            "source": {"project": "Reproducibility Project: Psychology", "osf_node": "ezcuj", "component": "ytpuq",
                       "file": "rpp_data.csv", "row_study_num": r["Study Num"].strip(), "osf_project_url": vis["Project URL"]},
            "registered_decision_contract": {
                "question": "Given the original claim, the registered replication protocol/constraints and the replication's reported summary statistics, does the replication satisfy the a-priori replication criterion for this effect?",
                "dispositions": ["REPLICATION_SATISFIES_CRITERION", "REPLICATION_FAILS_CRITERION", "INCONCLUSIVE_REOPEN"],
                "strongest_native_parent": "replicator a-priori criterion applied to reported statistics; meta-analytic composite (RP:P Science 2015 aac4716)",
            },
            "tagger_visible_record": vis,
            "arm_visible_supplement_pre_verdict": arm_only,
        })
    return cases, hidden


# ---------------------------------------------------------------- RP:CB
RPCB_PAPER_VIS = ["Original paper title", "Year", "Original paper journal", "Number of original authors", "OSF project link",
                  "Draft protocol shared with original authors date", "Registered Report submission date",
                  "Registered Report acceptance date", "Link to Registered Report", "Did original authors respond to any emails?",
                  "Number of lab(s) contracted for the entire paper"]
RPCB_EXP_VIS = ["Experiment #", "Original paper figure", "Was experiment originally identified by RP:CB team",
                "Did the experiment protocol get submitted to eLife", "Did the experiment protocol get accepted and published in eLife",
                "Clarifications asked of original authors", "Quality of response from original authors", "Data shared by original authors",
                "Code shared by original authors", "Key materials asked to be shared", "Key materials offered to be shared",
                "Key materials shared", "Type of experiment", "What types of experimental techniques were utilized?",
                "What category of experimental techniques were utilized?", "Number of lab(s) contracted for the experiment",
                "Registered Report protocol", "Experiment description", "Original sample number (reported)",
                "Replication sample number (power)", "Was the original experiment blinded?", "Was the original experiment randomized?",
                "Was the original experiment sample size determined a priori?", "Was the replication experiment sample size determined a priori?",
                "Was a statistical test reported in the original paper?", "What statistical test(s) was reported?",
                "Was variation of biological repeats reported in the original experiment?"]
RPCB_EXP_HIDDEN = ["Replication experiment completed", "If experiment incomplete, why?", "Changes needed during experimentation?",
                   "If modifications were needed for experiment to proceed, what were they?", "Changes able to be implemented during experimentation?",
                   "If modifications unable to be fully implemented, why?", "Replication study figure", "Was the replication experiment blinded?",
                   "Was the replication experiment randomized?", "Replication sample number (reported)", "Notes"]


def build_rpcb() -> tuple[list[dict], dict]:
    papers = {p["Paper #"].strip(): p for p in read_csv("rpcb_paper_level.csv")}
    exps = read_csv("rpcb_experiment_level.csv")
    effects = read_csv("rpcb_effect_level.csv")
    by_exp: dict[tuple[str, str], list[dict]] = {}
    for e in effects:
        by_exp.setdefault((e["Paper #"].strip(), e["Experiment #"].strip()), []).append(e)
    cases, hidden = [], {}
    for x in exps:
        if (x.get("Replication experiment attempted") or "").strip() != "Yes":
            continue
        key = (x["Paper #"].strip(), x["Experiment #"].strip())
        p = papers.get(key[0], {})
        cid = f"RPCB-P{key[0]}-E{key[1]}"
        effs = by_exp.get(key, [])
        matches = []
        for e in effs:
            exp_dir = e["Expected difference based on the original paper?"].strip()
            obs = e["Observed difference in replication?"].strip()
            if exp_dir == "Positive":
                matches.append(obs == "Positive")
            elif exp_dir == "Null":
                matches.append(obs in ("Null", "Null-positive", "Null-negative"))
        composite = ("NO_WITNESS" if not matches else "STRICT_SUCCESS" if all(matches) else
                     "STRICT_FAILURE" if not any(matches) else "MIXED")
        hidden[cid] = {
            "experiment_execution_record": clean(x, RPCB_EXP_HIDDEN),
            "effects": [{k: (e.get(k) or "").strip() for k in e if k not in ("Paper #", "Experiment #")} for e in effs],
            "n_effects": len(effs), "n_comparable_effects": len(matches), "composite_witness_class": composite,
            "link_to_replication_study": (p.get("Link to Replication study") or "").strip(),
            "replication_study_fully_completed_paper_level": (p.get("Replication study fully completed") or "").strip(),
        }
        vis = {"paper": clean(p, RPCB_PAPER_VIS), "experiment": clean(x, RPCB_EXP_VIS), "paper_num": key[0]}
        cases.append({
            "case_id": cid, "domain": "CANCER_BIOLOGY_RPCB", "domain_class": "EMPIRICAL",
            "witness_class": "REGISTERED_REPORT_REPLICATION_OUTCOME",
            "source": {"project": "Reproducibility Project: Cancer Biology", "osf_node": "e5nvr",
                       "files": ["rpcb_paper_level.csv", "rpcb_experiment_level.csv", "rpcb_effect_level.csv"],
                       "paper_num": key[0], "experiment_num": key[1], "registered_report_url": vis["paper"]["Link to Registered Report"]},
            "registered_decision_contract": {
                "question": "Given the original claim, the eLife Registered Report protocol constraints and the replication's reported effect-level statistics, does the replication of this experiment satisfy the protocol's pre-specified replication criteria?",
                "dispositions": ["REPLICATION_SATISFIES_CRITERION", "REPLICATION_FAILS_CRITERION", "INCONCLUSIVE_REOPEN"],
                "strongest_native_parent": "Registered Report pre-specified analysis plan applied to reported effects; RP:CB composite outcome criteria (Errington et al. 2021 eLife 10:e71601)",
            },
            "tagger_visible_record": vis,
            "arm_visible_supplement_pre_verdict": {"note": "effect-level replication statistics are released to arms at dispatch with direction/verdict columns stripped; frozen in the dispatch PR"},
        })
    return cases, hidden


# --------------------------------------------------------------- FORMAL
def wikidata(qid: str) -> dict:
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "ORION-V2-SD80-intake/1.0 (research; contact via repository)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as f:
                d = json.load(f)
            ent = d["entities"][qid]
            return {
                "status": "OK",
                "label_en": ent.get("labels", {}).get("en", {}).get("value"),
                "description_en": ent.get("descriptions", {}).get("en", {}).get("value"),
                "enwiki_title": ent.get("sitelinks", {}).get("enwiki", {}).get("title"),
                "n_sitelinks": len(ent.get("sitelinks", {})),
                "claims_present": sorted(ent.get("claims", {}).keys())[:40],
            }
        except Exception as exc:  # noqa: BLE001
            err = str(exc)[:200]
            time.sleep(1.5 * (attempt + 1))
    return {"status": "ERR", "error": err}


def build_formal(fetch: bool) -> tuple[list[dict], dict, dict]:
    data = yaml.safe_load((RAW / "mathlib4_docs_1000.yaml").read_text())
    commit = json.loads((RAW / "mathlib4_master_commit.json").read_text())["sha"]
    all_entries = []
    for qid, v in data.items():
        v = v or {}
        has_witness = any(k in v for k in ("decl", "decls", "url", "identifiers"))
        all_entries.append((qid, v, has_witness))
    eligible = [(q, v) for q, v, w in all_entries if w]
    rng = random.Random(SEED)
    sample = sorted(rng.sample([q for q, _ in eligible], FORMAL_TAG_SAMPLE))
    sset = set(sample)
    cases, hidden = [], {}
    wd_cache_path = OUT / "sources/wikidata_cache.json"
    wd_cache = json.loads(wd_cache_path.read_text()) if wd_cache_path.exists() else {}
    for q, v in eligible:
        in_sample = q in sset
        if in_sample and fetch and q not in wd_cache:
            wd_cache[q] = wikidata(q)
            time.sleep(0.5)
        wd = wd_cache.get(q, {"status": "NOT_FETCHED"})
        cid = f"FORMAL-{q}"
        hidden[cid] = {k: v[k] for k in v if k in ("decl", "decls", "url", "identifiers", "authors", "date", "comment")}
        vis = {"wikidata_qid": q, "title_1000plus": v.get("title"), "msc_classification": v.get("msc"),
               "wikidata": {k: wd.get(k) for k in ("status", "label_en", "description_en", "enwiki_title", "n_sitelinks")}}
        cases.append({
            "case_id": cid, "domain": "FORMAL_MATHEMATICS_1000PLUS", "domain_class": "FORMAL",
            "witness_class": "MACHINE_CHECKED_FORMALIZATION_WITNESS",
            "source": {"project": "1000+ theorems formalisation status (mathlib4 docs/1000.yaml)", "mathlib4_master_commit": commit,
                       "wikidata_item": f"https://www.wikidata.org/wiki/{q}"},
            "registered_decision_contract": {
                "question": "Given the theorem's public informal record (name, Wikidata description, encyclopedic statement), produce a precise formal statement (Lean 4 / Mathlib signature) and the registered disposition on whether the statement as publicly given is formalizable without added hypotheses.",
                "dispositions": ["FORMALIZABLE_AS_STATED", "HYPOTHESES_MISSING_REOPEN", "STATEMENT_FALSE_OR_ILLFORMED_BLOCK"],
                "strongest_native_parent": "direct Mathlib-fluent formalization; witness = machine-checked declaration in Mathlib or a listed external formal library",
            },
            "tagger_visible_record": vis,
            "tagging_pool": "TAG_SAMPLE_60" if in_sample else "ELIGIBLE_UNTAGGED_RESERVE",
        })
    if fetch:
        wd_cache_path.write_text(json.dumps(wd_cache, indent=1, sort_keys=True))
    meta = {"entries_total": len(all_entries), "entries_with_formal_witness": len(eligible),
            "tag_sample_size": FORMAL_TAG_SAMPLE, "sample_seed": SEED, "mathlib4_master_commit": commit}
    return cases, hidden, meta


# ----------------------------------------------------------------- MLRC
def build_mlrc() -> tuple[list[dict], dict]:
    inv = json.loads((ROOT / "research/experiments/results/issue50/sd30/mlrc_witness_inventory.json").read_text())
    cases, hidden = [], {}
    for r in inv["rows"]:
        if r.get("verdict_bin") in (None, "NOT_APPLICABLE"):
            continue
        cid = f"MLRC-{r['openreview_forum_id']}"
        hidden[cid] = {k: r.get(k) for k in ("verdict_class_analyst", "verdict_bin", "verdict_prose_extract", "per_claim_summary")}
        vis = {k: r.get(k) for k in ("openreview_forum_id", "cycle", "original_title_as_cited", "original_arxiv_id",
                                      "original_resolved_title", "code_url", "tmlr_online_date")}
        cases.append({
            "case_id": cid, "domain": "MACHINE_LEARNING_MLRC", "domain_class": "EMPIRICAL_COMPUTATIONAL",
            "witness_class": "INDEPENDENT_PROSE_REPRODUCTION_VERDICT",
            "source": {"project": "MLRC Journal Track (TMLR/OpenReview)", "forum": f"https://openreview.net/forum?id={r['openreview_forum_id']}"},
            "registered_decision_contract": {"question": "NOT_DEFINED_PENDING_OUTCOME_FREE_EVIDENCE_LAYER", "dispositions": [],
                                             "strongest_native_parent": "original authors' reported results + released code"},
            "tagger_visible_record": vis,
        })
    return cases, hidden


# ----------------------------------------------------------- eligibility
def eligibility(case: dict, hidden_entry: dict) -> dict:
    dom = case["domain"]
    items = {}
    c = case["registered_decision_contract"]
    items["a_question_and_decision_written_without_answer"] = "PASS" if c["dispositions"] else "FAIL_NO_OUTCOME_FREE_CONTRACT"
    items["b_strongest_native_parent_named"] = "PASS" if c["strongest_native_parent"] else "FAIL"
    for k in ("c_remote_donor_known_or_prospective_criterion", "d_donor_outside_local_retrieval_neighbourhood", "e_transfer_consequence_nontrivial"):
        items[k] = "NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY"
    if dom == "PSYCHOLOGY_RPP":
        items["f_witness_exposes_wrong_decision"] = "PASS" if hidden_entry.get("Replicate (R)") else "FAIL"
    elif dom == "CANCER_BIOLOGY_RPCB":
        items["f_witness_exposes_wrong_decision"] = "PASS" if hidden_entry.get("composite_witness_class") not in (None, "NO_WITNESS") else "FAIL_NO_EFFECT_LEVEL_WITNESS"
    elif dom == "FORMAL_MATHEMATICS_1000PLUS":
        items["f_witness_exposes_wrong_decision"] = "PASS" if hidden_entry else "FAIL"
    else:
        items["f_witness_exposes_wrong_decision"] = "PASS_PROSE_VERDICT_ONLY"
    items["g_visible_materials_free_of_hidden_key"] = ("PASS_BY_CONSTRUCTION" if dom != "MACHINE_LEARNING_MLRC"
                                                       else "FAIL_REPORT_TEXT_CARRIES_VERDICT__NO_STRIPPED_EVIDENCE_LAYER")
    items["s4_operational_remoteness"] = "NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_K_CORPUS_FREEZE"
    pc_r7 = all(items[k].startswith("PASS") for k in ("a_question_and_decision_written_without_answer", "b_strongest_native_parent_named",
                                                       "f_witness_exposes_wrong_decision", "g_visible_materials_free_of_hidden_key"))
    return {"items": items, "pc_r7_eligible": pc_r7,
            "fm80_eligible": "PENDING_DONOR_KEY_AND_REMOTENESS_FREEZE" if pc_r7 else "INELIGIBLE"}


def main() -> int:
    fetch = "--no-fetch" not in sys.argv
    regs_path = RAW / "rpp_osf_registrations.json"
    regs = json.loads(regs_path.read_text()) if regs_path.exists() else {}
    rpp, h_rpp = build_rpp(regs)
    rpcb, h_rpcb = build_rpcb()
    formal, h_formal, formal_meta = build_formal(fetch)
    mlrc, h_mlrc = build_mlrc()
    hidden = {**h_rpp, **h_rpcb, **h_formal, **h_mlrc}
    cases = rpp + rpcb + formal + mlrc
    for case in cases:
        case["eligibility"] = eligibility(case, hidden.get(case["case_id"], {}))
        case["hidden_key_sha256"] = sha(hidden.get(case["case_id"], {}))
        case["record_sha256"] = sha({k: v for k, v in case.items() if k != "record_sha256"})
    # calibration set: seeded, from PC-R7-eligible tagged pools only
    rng = random.Random(SEED + 1)
    calib = []
    for dom, n in CALIBRATION.items():
        pool = [c["case_id"] for c in cases if c["domain"] == dom and c["eligibility"]["pc_r7_eligible"]
                and c.get("tagging_pool", "TAG_ALL") != "ELIGIBLE_UNTAGGED_RESERVE"]
        calib += sorted(rng.sample(pool, n))
    manifest = {f.name: {"sha256": fsha(f), "bytes": f.stat().st_size} for f in sorted(RAW.iterdir()) if f.is_file()}
    counts = {}
    for c in cases:
        d = counts.setdefault(c["domain"], {"records": 0, "pc_r7_eligible": 0, "tagging_pool": 0})
        d["records"] += 1
        d["pc_r7_eligible"] += int(c["eligibility"]["pc_r7_eligible"])
        d["tagging_pool"] += int(c["eligibility"]["pc_r7_eligible"] and c.get("tagging_pool", "TAG_ALL") != "ELIGIBLE_UNTAGGED_RESERVE")
    out = {
        "schema_version": "orion.v2.sd80-case-matrix-cases.v1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seed": SEED, "source_manifest_sha256": manifest, "formal_meta": formal_meta, "domain_counts": counts,
        "calibration_case_ids": calib, "cases": cases,
    }
    (OUT / "SD80_CASE_MATRIX_CASES_V1.json").write_text(json.dumps(out, indent=1, sort_keys=False, ensure_ascii=False, default=str))
    (OUT / "SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json").write_text(json.dumps(
        {"schema_version": "orion.v2.sd80-case-matrix-hidden-keys.v1",
         "custody": "NEVER mount in a model-visible workspace; taggers and arms must not read this file",
         "keys": hidden}, indent=1, sort_keys=True, ensure_ascii=False, default=str))
    # tagger-visible views (no eligibility flags, no hidden keys, no source verdict fields)
    def view(c):
        return {"case_id": c["case_id"], "domain": c["domain"], "domain_class": c["domain_class"],
                "witness_class": c["witness_class"], "registered_decision_contract": c["registered_decision_contract"],
                "public_record": c["tagger_visible_record"]}
    tagged_pool = [c for c in cases if c["eligibility"]["pc_r7_eligible"] and c.get("tagging_pool", "TAG_ALL") != "ELIGIBLE_UNTAGGED_RESERVE"]
    (OUT / "SD80_TAGGER_VISIBLE_RECORDS_V1.json").write_text(json.dumps(
        {"schema_version": "orion.v2.sd80-tagger-visible.v1", "n": len(tagged_pool), "records": [view(c) for c in tagged_pool]},
        indent=1, ensure_ascii=False))
    (OUT / "SD80_TAGGING_CALIBRATION_SET_V1.json").write_text(json.dumps(
        {"schema_version": "orion.v2.sd80-tagging-calibration.v1", "seed": SEED + 1, "case_ids": calib,
         "records": [view(c) for c in tagged_pool if c["case_id"] in set(calib)]}, indent=1, ensure_ascii=False))
    print(json.dumps({"domain_counts": counts, "formal_meta": formal_meta, "calibration": calib, "hidden": len(hidden)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
