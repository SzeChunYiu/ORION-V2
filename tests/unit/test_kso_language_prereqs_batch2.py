"""KSO_LANGUAGE_PREREQUISITE_THEOREMS_BATCH2_V1 — every theorem's checker holds, its planted mutant is
caught and its no-alarm control passes."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_language_prereqs_batch2_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_language_prereqs_batch2_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_b1_meg05_discourse_state(mod):
    r = mod.check_b1_meg05_discourse_state()
    assert r["speakers"] == 10 and r["authority_chains_checked"] == 270 and r["meet_and_join_compositions_bottom"] == 2
    assert r["mutant_majority_promote_caught"] == 1 and r["retraction_leaves_machine_unchanged"] == 2 and r["bridge_makes_other_proposition_live"] == 1


def test_b2_meg12_per_input_vsw(mod):
    r = mod.check_b2_meg12_per_input_vsw()
    assert r["liveness_equals_agreement_checks"] == 9720 and r["per_input_reopen_checks"] == 960 and r["family_warrant_is_meet_of_per_input"] == 1440
    assert r["mutant_whole_procedure_overreopens"] == 840 and r["unrelated_evidence_no_alarm"] == 480 and r["affine_alternative_witness"] == 1


def test_b2_vsw_named_witness(mod):
    W = mod.vsw(mod.AFFINE8, {i: (mod.AFFINE8[3][i], f"e{i}") for i in range(4)}, range(4))
    assert W[0] == mod.canon([{"e0"}, {"e1", "e2", "e3"}])
    assert mod.reopen_per_input(W, "e0") == frozenset()


def test_b3_meg13_gap_learning_soundness(mod):
    r = mod.check_b3_meg13_gap_learning_soundness()
    assert all(r["genome_after_admit"].values()) and r["ambiguous_not_admitted"] == 1 and r["admitted_warrant_is_vsw_antichain"] == 1
    assert r["mutant_admit_without_agreement_caught"] == 1 and r["mutant_average_contradiction_caught"] == 1 and r["feedback_admits_zero"] == 1
    assert not any("FEEDBACK" in v for v in mod.GAP_CHANNELS.values())


def test_b4_meg24_canonical_meaning_graph(mod):
    r = mod.check_b4_meg24_canonical_meaning_graph()
    assert r["can_equal_iff_isomorphic_pairs"] == 4096 and r["random_relabel_invariance"] == 40
    assert r["wl1_collision_c6_vs_2c3"] == 1 and r["mutant_wl_hash_as_canonical_caught"] == 1 and r["beyond_bound_cannot_check"] == 1


def test_b4_canonical_form_bound_is_cannot_check_not_pass(mod):
    with pytest.raises(mod.CannotCheck):
        mod.can(("e",) * (mod.CAN_MAX_VERTICES + 1), ())


def test_b5_meg03_scope_epoch_supersession(mod):
    r = mod.check_b5_meg03_scope_epoch_supersession()
    assert r["measurability_checks"] == 1215 and r["epoch_algebra_checks"] == 15625
    assert r["tuesday_wednesday_reopen"] == ["day_tue", "plan"] and r["tuesday_wednesday_unaffected"] == ["day_wed", "note", "unrelated", "venue"]
    assert r["mutant_stale_plan_caught"] == 1 and r["supersession_equals_ks_t22"] == 1 and r["no_alarm_before_supersession"] == 1


def test_b6_meg17_repair_after_reopen(mod):
    r = mod.check_b6_meg17_repair_after_reopen()
    assert r["random_spaces"] == 30
    for key in ("works_before", "fails_after", "unrelated_liveness_intact", "activation_outside_reach_intact", "reinstate_exact", "relearn_live_new_id", "behaviour_equal_lifecycle_differs", "work_exact_leq_cone"):
        assert r[key] == 30, key
    assert r["mutant_global_touches_more"] > 0


def test_b7_meg19_consolidation_locality(mod):
    r = mod.check_b7_meg19_consolidation_locality()
    assert r["intervals_at_n2"] == 20 and r["liveness_change_only_through_exports"] == 50714 and r["unqualified_converse_fails"] > 0
    assert r["fixture_cases"]["deep_non_exported"] == {"lambda_m": ["LIVE", "LIVE"], "reopen": ["x2"], "recheck": ["m", "x4"], "content_recheck": ["p2"]}
    assert r["mutant_recheck_only_on_liveness_caught"] == 1 and r["mutant_summary_majority_caught"] == 1 and r["mutant_equal_by_liveness_caught"] == 1
    assert r["deconsolidation"] == "PARENT_SUFFICIENT_EXPECTED"


def test_b8_meg28_dpo_jump_preservation(mod):
    r = mod.check_b8_meg28_dpo_jump_preservation()
    assert r["affine_span"] == 8 and r["quadratic_span"] == 16 and r["atoms_preserved_interval_and_signature"] == 18 and r["old_repertoire_byte_identical"] == 8
    assert r["reopening_set"] == ["archive", "feat_ab", "h_0001", "phi_affine", "phi_quad", "renderer", "report"]
    assert r["rollback_exact"] == 1 and r["mutant_interface_attribute_change_refused"] == 1 and r["mutant_one_hop_caught"] == 1 and r["dangling_refused"] == 1
    assert r["improvement_half"] == "OPEN"


def test_run_all_carries_no_novelty_claim(mod):
    out = mod.run_all()
    assert out["NOVELTY"] == "NOT_ESTABLISHED" and len([k for k in out if k.startswith("B")]) == 8


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
    capsys.readouterr()
