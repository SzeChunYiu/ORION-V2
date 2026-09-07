"""The recall-signature scan is a programme-level precondition, so it must fire on planted
contamination, stay silent on planted clean reasoning, and reproduce the FM80 §9 V2 finding on the
real probe record rather than only on fixtures."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load(rel: str, name: str):
    s = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


M = _load("scripts/recall_signature_scan.py", "recall_signature_scan")
C = _load("research/experiments/fm80-exec/fm80_formal_source_census.py", "fm80_formal_source_census")


def test_scan_selftest() -> None:
    assert M._self_test() == 0


def test_census_selftest() -> None:
    assert C._self_test() == 0


def test_empty_input_is_cannot_check_not_clean() -> None:
    assert M.scan([], ["k"])["status"] == M.CANNOT_CHECK


def test_no_alarm_reasoning_without_recall_is_clean() -> None:
    clean = [{"id": str(i), "answer": 1, "truth": 1,
              "text": "The original N is 24 and power is marginal, so I expect it to hold."}
             for i in range(30)]
    assert M.scan(clean, ["Replicate (R)"])["status"] == M.CLEAN


def test_citing_the_parent_report_alone_is_not_a_recall_marker() -> None:
    """The defect that inflated the first published figure: 28/30 replies cite the parent report,
    which is legitimate literature use. It must not count."""
    r = M.scan([{"id": "x", "text": "Open Science Collaboration (2015) defines the criterion."}],
               ["Replicate (R)"])
    assert r["status"] == M.CLEAN and r["n_citing_a_recalled_outcome"] == 0


def test_reproduces_the_fm80_finding_on_the_real_probe_record() -> None:
    rec = ROOT / "research/experiments/fm80-exec/results/FM80_S9_V2_RANGE_PROBE_V1.json"
    keys = json.loads((ROOT / "research/experiments/sd80/SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json")
                      .read_text())["keys"]
    raw = json.loads(rec.read_text())["raw"]

    def rows(arm: str) -> list[dict]:
        return [{"id": r["case_id"], "text": r["raw_tail"], "answer": r["disposition"],
                 "truth": {"yes": "REPLICATION_SATISFIES_CRITERION",
                           "no": "REPLICATION_FAILS_CRITERION"}.get(
                     str(keys[r["case_id"]].get("Replicate (R)", "")).strip().lower())}
                for r in raw if r["arm"] == arm]

    a1 = M.scan(rows("A1"), ["Replicate (R)"])
    a0 = M.scan(rows("A0"), ["Replicate (R)"])
    assert a1["status"] == M.DETECTED
    assert a1["n_naming_a_key_field_verbatim"] == 16
    # The control arm anchors the number: without 0/30 here, 16/30 there means nothing.
    assert a0["status"] == M.CLEAN
    assert a0["n_naming_a_key_field_verbatim"] == 0


def test_census_on_the_pinned_source_matches_the_receipt() -> None:
    src = ROOT / "research/experiments/sd80/sources/raw/mathlib4_docs_1000.yaml"
    out = C.census(src.read_text())
    assert out["n_entries"] == 1199
    assert out["n_formalised"] == 243
    assert out["n_unformalised"] == 956
    assert out["n_unformalised_title_only"] == 945
    assert out["adverse_seam_upper_bound"] == 29
    assert out["seam_clears_bar"] is False and out["bar_per_domain"] == 61
    keys = json.loads((ROOT / "research/experiments/sd80/SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json")
                      .read_text())["keys"]
    sd80 = {q.removeprefix("FORMAL-") for q in keys if q.startswith("FORMAL-")}
    assert not (sd80 ^ set(out["formalised_ids"])), "SD80 must be exactly the formalised side"
