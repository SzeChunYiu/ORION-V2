"""KSO_ONE_DAY_THEOREMS_BATCH1_V1 — every theorem's checker holds and its planted mutant is caught."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_one_day_theorems_batch1_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_one_day_theorems_batch1_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_t1_meg04_commit_bottom(mod):
    r = mod.check_t1_meg04_commit_bottom()
    assert r["glb_pairs_checked"] == 3**4 * 3**4 and r["mutant_authority_max_caught"] == 1 and r["mutant_drop_operator_factor_caught"] == 1


def test_t2_meg06_budget_bracket(mod):
    r = mod.check_t2_meg06_budget_bracket()
    assert r["partial_sum_identity_checks"] == 10 and r["chain17_mutant_found_unsound"] == 1
    assert r["float_l1_error_max"] <= r["float_bound"]


def test_t3_meg08_feedback_not_warrant(mod):
    r = mod.check_t3_meg08_feedback_not_warrant()
    assert r["signature_checks"] == 240 and r["matrices_changed_by_perturbation"] == 30 and r["mutant_feedback_edits_label_caught"] == 30


def test_t4_meg18_jump_rollback(mod):
    r = mod.check_t4_meg18_jump_rollback()
    assert r["quarantined"] == ["am", "m", "md"] and r["rollback_exact"] == 1 and r["revocation_alone_changes_fixed_point"] == 1


def test_t5_meg22_shared_evidence(mod):
    r = mod.check_t5_meg22_shared_evidence()
    assert r["sigma"] == ["L"] and r["interference_exact"] == ["L", "c1", "c2", "p1", "p2"] and r["mutant_drop_bridge_caught"] == 1


def test_t6_meg26_candidate_warrant(mod):
    r = mod.check_t6_meg26_candidate_warrant()
    assert r["ambiguous_blocks_firing"] == 1 and r["merged_atom_fires_under_ambiguity"] == 1 and r["mutant_forced_collapse_caught"] == 1


def test_t7_meg29_no_self_authority(mod):
    r = mod.check_t7_meg29_no_self_authority()
    assert r["mutant_self_commit_refused"] == 1 and r["dependent_certificate_dies_with_model"] == 1 and r["independent_certificate_survives"] == 1


def test_t8_meg30_no_livelock(mod):
    r = mod.check_t8_meg30_no_livelock()
    assert r["runs"] == r["ended_cannot_check"] + r["ended_done"] and r["ended_done"] > 0
    assert r["mutant_unmetered_livelocks_at_cap"] == 1 and r["mutant_stale_cache_caught"] == 1


def test_t9_meg31_information_unit(mod):
    r = mod.check_t9_meg31_information_unit()
    assert r["telescoping_chains"] == 50 and r["split_source_counts_once"] == 1 and r["mutant_double_count_caught"] == 1


def test_t10_meg35_upper_certificates(mod):
    r = mod.check_t10_meg35_upper_certificates(3)
    assert r["intervals"] == 168 and r["bounded_alternative_checks"] == 16064 and r["mutant_replace_upper_decertifies_dead"] > 0


def test_t11_meg01_evidence_dependence(mod):
    r = mod.check_t11_meg01_evidence_dependence()
    assert r["flat_equals_through_derived"] == 960 and r["mutant_derived_as_assumption_caught"] == 1


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
