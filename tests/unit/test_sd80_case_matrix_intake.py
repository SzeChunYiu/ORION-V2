"""Custody checks for the SD80 naturalistic case-matrix intake (PC-R7/FM80)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SD80 = ROOT / "research/experiments/sd80"
CASES = SD80 / "SD80_CASE_MATRIX_CASES_V1.json"
HIDDEN = SD80 / "SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json"
VISIBLE = SD80 / "SD80_TAGGER_VISIBLE_RECORDS_V1.json"
CALIB = SD80 / "SD80_TAGGING_CALIBRATION_SET_V1.json"

LEAK_FIELDS = {
    "Replicate (R)", "Meta-analysis significant", "O within CI R", "composite_witness_class",
    "Observed difference in replication?", "Replication p value", "Replication experiment completed",
    "verdict_bin", "verdict_class_analyst", "decl", "decls",
}

pytestmark = pytest.mark.skipif(not CASES.exists(), reason="SD80 intake artifacts absent")


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def _walk_keys(obj, out: set[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.add(k)
            _walk_keys(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk_keys(v, out)


def test_every_case_record_hash_matches_content():
    data = json.loads(CASES.read_text())
    hidden = json.loads(HIDDEN.read_text())["keys"]
    assert data["cases"], "no cases"
    for case in data["cases"]:
        body = {k: v for k, v in case.items() if k != "record_sha256"}
        assert case["record_sha256"] == _sha(body), case["case_id"]
        assert case["hidden_key_sha256"] == _sha(hidden.get(case["case_id"], {})), case["case_id"]


def test_tagger_visible_records_carry_no_hidden_key_fields():
    for path in (VISIBLE, CALIB):
        keys: set[str] = set()
        _walk_keys(json.loads(path.read_text())["records"], keys)
        assert not (keys & LEAK_FIELDS), f"{path.name} leaks {sorted(keys & LEAK_FIELDS)}"


def test_calibration_set_is_twenty_eligible_cases_across_three_domains():
    calib = json.loads(CALIB.read_text())
    data = json.loads(CASES.read_text())
    by_id = {c["case_id"]: c for c in data["cases"]}
    assert len(calib["case_ids"]) == 20 and len(set(calib["case_ids"])) == 20
    domains = {by_id[i]["domain"] for i in calib["case_ids"]}
    assert domains == {"PSYCHOLOGY_RPP", "CANCER_BIOLOGY_RPCB", "FORMAL_MATHEMATICS_1000PLUS"}
    assert all(by_id[i]["eligibility"]["pc_r7_eligible"] for i in calib["case_ids"])


def test_domain_structure_meets_fm80_s2_minimum():
    data = json.loads(CASES.read_text())
    counts = data["domain_counts"]
    formal = [d for d in counts if any(c["domain"] == d and c["domain_class"] == "FORMAL" for c in data["cases"])]
    empirical = [d for d in counts if counts[d]["pc_r7_eligible"] >= 30
                 and any(c["domain"] == d and c["domain_class"].startswith("EMPIRICAL") for c in data["cases"])]
    assert len(formal) >= 1 and all(counts[d]["pc_r7_eligible"] >= 30 for d in formal)
    assert len(empirical) >= 2


def test_mlrc_recorded_but_not_counted():
    data = json.loads(CASES.read_text())
    mlrc = [c for c in data["cases"] if c["domain"] == "MACHINE_LEARNING_MLRC"]
    assert mlrc and not any(c["eligibility"]["pc_r7_eligible"] for c in mlrc)


def test_source_manifest_hashes_match_raw_files():
    data = json.loads(CASES.read_text())
    raw = SD80 / "sources/raw"
    for name, rec in data["source_manifest_sha256"].items():
        p = raw / name
        assert p.exists(), name
        assert hashlib.sha256(p.read_bytes()).hexdigest() == rec["sha256"], name
