#!/usr/bin/env python3
"""SD80 case-matrix finalize: GN0 calibration agreement, full-tag merge,
tag populations, PC-R7 sufficiency verdict, and the intake receipt
SD80_CASE_MATRIX_INTAKE_V1.{json,md}.

Stages:
  calibration  -> compares tagging/calibration_tagger_{A,B}.json, writes
                  tagging/SD80_GN0_CALIBRATION_AGREEMENT_V1.json (+ disagreement list)
  split        -> writes per-domain tagger-visible files for the full round
  full         -> merges tagging/full_tagger_{A,B}_<domain>.json, applies the
                  frozen adjudication (tagger disagreement -> adjudicated tag from
                  tagging/full_adjudication.json, else INTERNAL by rule s3 note),
                  computes populations and writes the intake receipt
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/experiments/sd80"
TAG = OUT / "tagging"
DOMAINS = ["PSYCHOLOGY_RPP", "CANCER_BIOLOGY_RPCB", "FORMAL_MATHEMATICS_1000PLUS"]
MIN_PER_TAG = 15
MIN_ELIGIBLE = 30
GN0_MIN = 0.90


def load(p: Path):
    return json.loads(p.read_text())


def fsha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tags_by_id(p: Path) -> dict:
    d = load(p)
    return {t["case_id"]: t for t in d["tags"]}


def calibration() -> dict:
    cal = load(OUT / "SD80_TAGGING_CALIBRATION_SET_V1.json")
    a = tags_by_id(TAG / "calibration_tagger_A.json")
    b = tags_by_id(TAG / "calibration_tagger_B.json")
    ids = cal["case_ids"]
    missing = [i for i in ids if i not in a or i not in b]
    agree = [i for i in ids if i in a and i in b and a[i]["tag"] == b[i]["tag"]]
    disagree = [{"case_id": i, "A": a[i], "B": b[i]} for i in ids if i in a and i in b and a[i]["tag"] != b[i]["tag"]]
    rate = len(agree) / len(ids)
    res = {
        "schema_version": "orion.v2.sd80-gn0-calibration.v1", "n_cases": len(ids), "n_agree": len(agree),
        "agreement_rate": rate, "gn0_threshold": GN0_MIN, "gn0_pass": rate >= GN0_MIN and not missing,
        "missing": missing, "disagreements": disagree,
        "tag_counts": {"A": {t: sum(1 for i in ids if a.get(i, {}).get("tag") == t) for t in ("EXTERNAL_VERIFIABLE", "INTERNAL")},
                       "B": {t: sum(1 for i in ids if b.get(i, {}).get("tag") == t) for t in ("EXTERNAL_VERIFIABLE", "INTERNAL")}},
        "per_domain": {},
        "inputs_sha256": {"A": fsha(TAG / "calibration_tagger_A.json"), "B": fsha(TAG / "calibration_tagger_B.json")},
        "computed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    for dom in DOMAINS:
        dids = [i for i in ids if any(r["case_id"] == i and r["domain"] == dom for r in cal["records"])]
        res["per_domain"][dom] = {"n": len(dids), "agree": sum(1 for i in dids if i in agree)}
    (TAG / "SD80_GN0_CALIBRATION_AGREEMENT_V1.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("n_cases", "n_agree", "agreement_rate", "gn0_pass", "missing", "tag_counts", "per_domain")}, indent=1))
    for d in disagree:
        print("DISAGREE", d["case_id"], "A=", d["A"]["tag"], "|", d["A"]["rationale"][:160], "\n   B=", d["B"]["tag"], "|", d["B"]["rationale"][:160])
    return res


def split() -> None:
    vis = load(OUT / "SD80_TAGGER_VISIBLE_RECORDS_V1.json")
    for dom in DOMAINS:
        recs = [r for r in vis["records"] if r["domain"] == dom]
        (TAG / f"records_{dom}.json").write_text(json.dumps({"domain": dom, "n": len(recs), "records": recs}, indent=1, ensure_ascii=False))
        print(dom, len(recs))


def full() -> dict:
    cases = load(OUT / "SD80_CASE_MATRIX_CASES_V1.json")
    gn0 = load(TAG / "SD80_GN0_CALIBRATION_AGREEMENT_V1.json")
    adj_path = TAG / "full_adjudication.json"
    adjud = load(adj_path)["adjudications"] if adj_path.exists() else {}
    rule_sha = fsha(OUT / "SD80_PC_R7_OBLIGATION_PROVENANCE_TAGGING_RULE_V1.md")
    per_domain, tag_records, disagreements, missing_all = {}, [], [], []
    for dom in DOMAINS:
        a = tags_by_id(TAG / f"full_tagger_A_{dom}.json")
        b = tags_by_id(TAG / f"full_tagger_B_{dom}.json")
        pool = [c for c in cases["cases"] if c["domain"] == dom and c["eligibility"]["pc_r7_eligible"]
                and c.get("tagging_pool", "TAG_ALL") != "ELIGIBLE_UNTAGGED_RESERVE"]
        eligible_total = sum(1 for c in cases["cases"] if c["domain"] == dom and c["eligibility"]["pc_r7_eligible"])
        counts = {"EXTERNAL_VERIFIABLE": 0, "INTERNAL": 0}
        n_agree = 0
        missing = []
        for c in pool:
            i = c["case_id"]
            if i not in a or i not in b:
                missing.append(i)
                continue
            if a[i]["tag"] == b[i]["tag"]:
                final, how = a[i]["tag"], "AGREED"
                n_agree += 1
            elif i in adjud:
                final, how = adjud[i]["tag"], "ADJUDICATED"
                disagreements.append({"case_id": i, "A": a[i]["tag"], "B": b[i]["tag"], "final": final, "adjudication": adjud[i]})
            else:
                final, how = "INTERNAL", "DISAGREEMENT_UNADJUDICATED_DEFAULT_INTERNAL"
                disagreements.append({"case_id": i, "A": a[i]["tag"], "B": b[i]["tag"], "final": final, "adjudication": None})
            counts[final] += 1
            tag_records.append({"case_id": i, "domain": dom, "tag_A": a[i]["tag"], "tag_B": b[i]["tag"], "final_tag": final, "resolution": how})
        missing_all += missing
        n_tagged = len(pool) - len(missing)
        per_domain[dom] = {
            "pc_r7_eligible_cases": eligible_total, "tagging_pool": len(pool), "tagged": n_tagged, "missing": missing,
            "full_round_agreement_rate": (n_agree / n_tagged) if n_tagged else None,
            "tag_counts": counts,
            "both_tags_ge_15": counts["EXTERNAL_VERIFIABLE"] >= MIN_PER_TAG and counts["INTERNAL"] >= MIN_PER_TAG,
            "eligible_ge_30": eligible_total >= MIN_ELIGIBLE,
        }
    structure_ok = (sum(1 for d in DOMAINS if cases["cases"] and any(c["domain"] == d and c["domain_class"] == "FORMAL" for c in cases["cases"])) >= 1
                    and sum(1 for d in DOMAINS if any(c["domain"] == d and c["domain_class"].startswith("EMPIRICAL") for c in cases["cases"])) >= 2)
    all_eligible_ok = all(per_domain[d]["eligible_ge_30"] for d in DOMAINS)
    tags_ok = all(per_domain[d]["both_tags_ge_15"] for d in DOMAINS)
    gn0_pass = bool(gn0["gn0_pass"])
    if gn0_pass and structure_ok and all_eligible_ok and tags_ok and not missing_all:
        verdict = "MATRIX_SUFFICIENT_FOR_PC_R7"
    else:
        verdict = "INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES"
    reasons = []
    if not gn0_pass:
        reasons.append("GN0_FAIL")
    if not structure_ok:
        reasons.append("FM80_S2_DOMAIN_STRUCTURE_NOT_MET")
    if not all_eligible_ok:
        reasons.append("FEWER_THAN_30_ELIGIBLE_IN_SOME_DOMAIN")
    if not tags_ok:
        reasons.append("TAG_POPULATION_BELOW_15_IN_SOME_DOMAIN: " + ", ".join(
            f"{d}:{per_domain[d]['tag_counts']}" for d in DOMAINS if not per_domain[d]["both_tags_ge_15"]))
    if missing_all:
        reasons.append(f"UNTAGGED_CASES:{len(missing_all)}")
    receipt = {
        "schema_version": "orion.v2.sd80-case-matrix-intake.v1",
        "title": "SD80 naturalistic case-matrix intake V1 + PC-R7 obligation-provenance tagging calibration",
        "class": "CASE_MATRIX_INTAKE__NO_ARM_RUN__NO_OUTCOME_ACCESS_BY_TAGGERS_OR_ARMS",
        "computed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": "Mac (intake, hashing, tagging orchestration); LUNARC unreachable during intake (expired 2FA socket); billy-old reserved for any arm compute",
        "frozen_inputs": {
            "pc_r7_design": "research/experiments/pc-r7/PC_R7_NATURALISTIC_OBLIGATION_CELL_DESIGN_V1.{md,json}",
            "fm80_protocol": "research/experiments/FM80_NATURALISTIC_TRANSFER_DECISIVE_PROTOCOL_V1.{md,json}",
            "tagging_rule_sha256": rule_sha,
            "cases_file": "research/experiments/sd80/SD80_CASE_MATRIX_CASES_V1.json",
            "cases_file_sha256": fsha(OUT / "SD80_CASE_MATRIX_CASES_V1.json"),
            "hidden_keys_file_sha256": fsha(OUT / "SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json"),
            "source_manifest_sha256": cases["source_manifest_sha256"],
        },
        "sources": {
            "PSYCHOLOGY_RPP": {"lawful_source": "OSF public API + published dataset (ezcuj/ytpuq rpp_data.csv; registrations via api.osf.io per project)", "witness_class": "REGISTERED_REPLICATION_VERDICT"},
            "CANCER_BIOLOGY_RPCB": {"lawful_source": "OSF public API + published final-analysis dataset (e5nvr); eLife Registered Reports", "witness_class": "REGISTERED_REPORT_REPLICATION_OUTCOME"},
            "FORMAL_MATHEMATICS_1000PLUS": {"lawful_source": "mathlib4 docs/1000.yaml at master commit " + cases["formal_meta"]["mathlib4_master_commit"] + " + Wikidata EntityData", "witness_class": "MACHINE_CHECKED_FORMALIZATION_WITNESS"},
            "MACHINE_LEARNING_MLRC": {"lawful_source": "SD30 MLRC journal-track inventory (OpenReview/TMLR)", "witness_class": "INDEPENDENT_PROSE_REPRODUCTION_VERDICT",
                                       "status": "RECORDED_NOT_COUNTED: no outcome-free evidence layer (report text carries the verdict; OpenReview API challenge-gated 2026-09-02)"},
        },
        "domain_counts_raw": cases["domain_counts"],
        "fm80_eligibility_note": "FM80 s3 items c-e and s4 remoteness are donor-specific; recorded NOT_APPLICABLE for PC-R7 (no donor arm) and PENDING for FM80 (no donor key / K / corpus freeze exists yet). FM80 eligibility is therefore PENDING for every case; PC-R7 eligibility uses items a, b, f, g.",
        "gn0_calibration": {k: gn0[k] for k in ("n_cases", "n_agree", "agreement_rate", "gn0_threshold", "gn0_pass", "tag_counts", "per_domain", "disagreements")},
        "full_tagging": {"per_domain": per_domain, "disagreements": disagreements, "n_untagged": len(missing_all)},
        "sufficiency": {"verdict": verdict, "reasons": reasons,
                        "rule": "PC-R7 s1: both tags >= 15 cases/domain in every domain, >= 30 eligible/domain, FM80 s2 structure, GN0 >= 0.90"},
        "authority": {"grants_claim": False, "arm_run_performed": False, "scientific_truth_authorized": False},
    }
    (OUT / "SD80_CASE_MATRIX_INTAKE_V1.json").write_text(json.dumps(receipt, indent=1))
    (TAG / "SD80_FINAL_TAGS_V1.json").write_text(json.dumps({"schema_version": "orion.v2.sd80-final-tags.v1", "tags": tag_records}, indent=1))
    print(json.dumps({"per_domain": per_domain, "verdict": verdict, "reasons": reasons, "n_disagreements": len(disagreements)}, indent=1))
    return receipt


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "calibration"
    {"calibration": calibration, "split": split, "full": full}[stage]()
