"""FM80-§9-EXEC checker discipline: planted positive passes at n=70, registered n=30 is UNDERPOWERED not negative,
null fails 9.1, fidelity regression fails 9.3, A2 reproduction fails 9.5; SD80 preconditions: every donor-dependent
clause is CANNOT_CHECK because the pool carries no donor key (corrected 2026-09-06, #308 R11b — the previous
assertion pinned the mislabel it was meant to catch), with the no-alarm control that a genuine False still fails."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "research" / "experiments" / "fm80-exec" / "fm80_exec_gate.py"
spec = importlib.util.spec_from_file_location("fm80_exec_gate", P); M = importlib.util.module_from_spec(spec); sys.modules["fm80_exec_gate"] = M; spec.loader.exec_module(M)


def test_selftest_plants_and_no_alarm() -> None:
    rep = M.planted_and_no_alarm()
    assert all(v for k, v in rep.items() if isinstance(v, bool)), rep
    assert abs(rep["best_case_p_at_bar_n30"] - 0.25) < 1e-12 and rep["best_case_p_at_bar_n61"] < 0.05 / 3


def test_clause_census_counts() -> None:
    c = {k: sum(1 for v in M.CLAUSES.values() if v["class"] == k) for k in ("EXACT", "MODEL_PROXY", "HUMAN_ONLY")}
    assert c == {"EXACT": 12, "MODEL_PROXY": 3, "HUMAN_ONLY": 4}


SD80 = ROOT / "research" / "experiments" / "sd80" / "SD80_CASE_MATRIX_CASES_V1.json"


def test_sd80_preconditions_3c_is_cannot_check_not_a_rejection() -> None:
    """#308 R11b. This test previously asserted `3c == SOME_FAIL` with 455 checkable, which pinned the very
    defect it existed to catch: the adapter hardcoded `has_donor_key = False`, so the "455/455 fail" was a
    constant. The records say NOT_APPLICABLE...FM80_PENDING_DONOR_KEY on 455/455 — unevaluable, not rejected."""
    rows = M.case_table_from_sd80(SD80)
    assert len(rows) == 455
    pre = M.preconditions(rows)
    assert pre["3c"]["status"] == "CANNOT_CHECK" and pre["3c"]["n_checkable"] == 0 and pre["3c"]["n_pass"] == 0
    for clause in ("3d", "3e", "4.1", "4.2", "4.3"):
        assert pre[clause]["status"] == "CANNOT_CHECK", clause
    # and the adapter must not be reintroducing a constant: no row carries a boolean donor-key value
    assert all(r["has_donor_key"] is None for r in rows)


def test_sd80_preconditions_3g_is_checkable_and_discriminates() -> None:
    """The correction moves clauses in BOTH directions: 3g's input does exist in this pool, and reading it from
    the record recovers a real check (419 pass / 36 fail) that the hardcoded adapter reported as CANNOT_CHECK."""
    pre = M.preconditions(M.case_table_from_sd80(SD80))
    assert pre["3g"]["status"] == "SOME_FAIL" and pre["3g"]["n_checkable"] == 455 and pre["3g"]["n_pass"] == 419


def test_no_alarm_a_genuine_false_still_fails() -> None:
    """The fix must not blind the gate: a case that really carries a checked negative must still report it."""
    base = {"case_id": "X", "domain": "D", "eligible": None, "witness_disposition": None, "dispositions": {},
            "critical_fidelity_failure": {}, "donor_visible_to_baseline_or_prompt": None}
    assert M.preconditions([{**base, "has_donor_key": False}])["3c"]["status"] == "SOME_FAIL"
    assert M.preconditions([{**base, "has_donor_key": True}])["3c"]["status"] == "PASS_ALL"
    mixed = M.preconditions([{**base, "has_donor_key": True}, {**base, "has_donor_key": False}])["3c"]
    assert mixed["status"] == "SOME_FAIL" and mixed["n_checkable"] == 2 and mixed["n_pass"] == 1


def test_sd80_token_mapping() -> None:
    assert M.tri_from_sd80_item("PASS") is True
    assert M.tri_from_sd80_item("PASS_BY_CONSTRUCTION") is True
    assert M.tri_from_sd80_item("FAIL_NO_EFFECT_LEVEL_WITNESS") is False
    assert M.tri_from_sd80_item("NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY") is None
    assert M.tri_from_sd80_item(None) is None


def test_sd80_eligibility_ceiling_rpcb_below_registered_bar() -> None:
    """The pool's arithmetic, asserted so it cannot drift silently: RPCB ceilings below the bar of 61 under every
    Stage A outcome, MLRC at 0, formal and RPP above it."""
    c = M.sd80_eligibility_ceiling(M.case_table_from_sd80(SD80))
    assert c["bar_per_domain"] == 61
    d = c["domains"]
    assert d["CANCER_BIOLOGY_RPCB"]["checkable_ceiling"] == 50
    assert d["MACHINE_LEARNING_MLRC"]["checkable_ceiling"] == 0
    assert d["FORMAL_MATHEMATICS_1000PLUS"]["checkable_ceiling"] == 243
    assert d["PSYCHOLOGY_RPP"]["checkable_ceiling"] == 100
    assert not d["CANCER_BIOLOGY_RPCB"]["bar_reachable_before_stage_a"]
    assert d["FORMAL_MATHEMATICS_1000PLUS"]["bar_reachable_before_stage_a"]
    assert sorted(c["domains_below_bar_before_stage_a"]) == ["CANCER_BIOLOGY_RPCB", "MACHINE_LEARNING_MLRC"]
