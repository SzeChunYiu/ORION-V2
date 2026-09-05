"""KSO_SELF_MODEL_PREREQUISITE_THEOREMS_BATCH5_V1 — every theorem's checker holds, its planted mutants are
caught and its no-alarm control passes; counts are pinned."""
from __future__ import annotations

import importlib.util
import inspect
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_self_model_prereqs_batch5_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_self_model_prereqs_batch5_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


def test_e1_meg29_self_model_fibre(out):
    r = out["E1_MEG29_self_model_fibre"]
    assert (r["random_spaces"], r["object_liveness_checks"], r["object_activation_checks"], r["edge_rule_checks"]) == (30, 2832, 472, 390)
    assert r["self_seeded_query_inert_on_objects"] == r["mutant_self_edge_refused"] == r["mutant_self_edge_activates_object"] == 30
    assert r["mutant_world_truth_raised_caught"] == r["mutant_self_diagnosis_promotes_object_caught"] == r["object_closure_no_alarm"] == 1
    assert r["proposal_never_live_checks"] == 8 and r["adoption_refusals"] == 2 and r["mutant_adopted_by_own_prediction_caught"] == 1


def test_e1_self_authority_has_no_world_truth_and_no_commit(mod):
    assert mod.SELF_AUTH.get("world_truth", 0) == 0 and mod.SELF_AUTH.get("commit", 0) == 0 and mod.PROPOSAL_AUTH.get("commit", 0) == 0
    iv, auth = mod.proposal_atom(("t0",), "pred")
    assert iv[0] == mod.ZERO and mod.liveness(iv, frozenset()) == mod.UNKNOWN
    assert mod.adopt(iv, {"evidence_id": "pred", "authority": mod.SELF_AUTH, "source": "internal"})[0] == "REFUSED_NOT_EXTERNAL_COMMIT"


def test_e2_m11_diagnostic_layer_soundness(out):
    r = out["E2_M11S3_diagnostic_layer_soundness"]
    assert r["traces"] == r["representation_iff_certificate_checks"] == 128000 and r["representation_verdicts"] == 8
    assert r["method_verdicts_all_without_certificate"] == 1743 and r["insufficient_evidence_verdicts"] == 249 and r["replay_checks"] == 1267
    assert r["restoring_operator_traces"] == r["mutant_repeated_failure_escalates_caught"] == 800 and r["mutant_ignore_certificate_caught"] == 7
    assert r["other_class_no_alarm"] == 126000 and r["s5_missing_dependency_is_gap"] == 1


def test_e2_classifier_is_a_pure_function_of_the_trace(mod):
    assert list(inspect.signature(mod.classify).parameters) == ["trace"]
    f = {k: v[0] for k, v in mod.FIELDS.items()}
    live_fail = {a: (mod.LIVE, False) for a in mod.ALTERNATIVES}
    assert mod.classify((f, live_fail, True)) == "REPRESENTATION"
    assert mod.classify((f, live_fail, False)) == "INSUFFICIENT_EVIDENCE"
    assert mod.classify((dict(f, operator="DEFECT"), {**live_fail, "operator_alt": (mod.LIVE, True)}, True)) == "OPERATOR_WRONG"
    assert mod.classify((dict(f, info="MISSING"), live_fail, True)) == "MISSING_INFORMATION"


def test_e3_meg28_obstruction_certificate(out):
    r = out["E3_MEG28_obstruction_certificate"]
    assert r["target_x_revocation_checks"] == 128 and r["obstructions_found"] == 8 and r["compositions_tried_for_and"] == 8
    assert all(r[k] == 1 for k in ("and_obstruction", "xor_lower_level_sufficient", "post_jump_reachable", "mutant_without_live_clause_caught", "reinstate_makes_reachable", "mutant_partial_enumeration_caught", "in_span_family_no_alarm"))


def test_e4_m11_proposal_prediction_adoption(out):
    r = out["E4_M11S5_proposal_prediction_adoption"]
    assert r["decision_cases"] == r["spec_agreement"] == r["self_score_nondependence"] == r["leak_and_self_adoption_refusals"] == 11250
    assert r["adopted"] == 1746 and r["mutant_dev_tasks_overfit_cases"] == r["mutant_dev_tasks_caught"] == 1080 and r["mutant_dev_tasks_pessimistic_cases"] == 1376
    assert r["memorising_challenger_refused"] == r["seen_tasks_refused"] == r["honest_adopted_no_alarm"] == 1 and r["c6_and_protected_refused"] == 2


def test_e5_m11_shadow_non_interference(out):
    r = out["E5_M11S9_shadow_non_interference"]
    assert r["streams"] == r["object_and_commitments_identical"] == 30 and r["shadow_receipts"] == r["snapshot_replay_checks"] == 125
    assert r["mutant_shadow_writes_object_caught"] == r["mutant_shadow_commits_externally_caught"] == r["mutant_edit_receipt_caught"] == 30 and r["agreeing_stream_no_alarm"] == 1


def test_e6_meg18_reopen_and_exact_rollback(out):
    r = out["E6_MEG18_reopen_and_exact_rollback"]
    assert r["produced_objects"] == ["cached_and_conclusion", "feat_ab", "h_0001", "phi_quad"] and r["interface_and_untouched_preserved"] == 16
    assert r["reopening_set"] == ["archive", "cached_and_conclusion", "feat_ab", "h_0001", "phi_quad", "renderer", "report"]
    assert all(r[k] == 1 for k in ("adoption_applied", "rollback_state_hash_equal", "mutant_rollback_leaves_cache_caught", "mutant_rollback_without_revoke_caught", "unrelated_unchanged"))


def test_e7_meg30_meta_termination(out):
    r = out["E7_MEG30_meta_termination"]
    assert r["budget_x_charge_runs"] == 21 and r["window_bound_checks"] == 4
    assert all(r[k] == 1 for k in ("rising_schedule_terminates_faster", "mutant_charge_zero_refused", "mutant_halving_livelocks_at_cap", "meter_target_detected", "unreached_window_no_alarm"))


def test_e8_improvement_halves_are_conjectures_with_both_fixtures(out):
    r = out["E8_KST12_KST14_conjectures"]
    assert r["ks_t12_status"] == r["ks_t14_status"] == "CONJECTURE"
    assert r["ks_t12_smallest_holding_chain"] == 2 and r["ks_t12_smallest_failing_chain_with_internal_query"] == 1
    assert r["ks_t12_costs_by_k_target_only"] == {1: [2, 2], 2: [3, 2], 3: [4, 2], 4: [5, 2]} and r["ks_t12_costs_by_k_with_internal"] == {1: [3, 5], 2: [4, 5], 3: [5, 5], 4: [6, 5]}
    assert r["ks_t14_holds_on"] == "Q={AND}: 0→1" and r["ks_t14_fails_on"] == "Q={XOR}: 1→1" and r["ks_t14_harmful_lift"] == "R'={1,ab} on Q={XOR}: 1→0" and r["ks_t14_whole_family"] == [8, 16]


def test_residual_halves_r1_r2_r3(out):
    r1, r2, r3 = out["R1_MEG19_deconsolidation"], out["R2_MEG27_regular_inventory"], out["R3_MEG02_graded_witness"]
    assert r1["undo_exact"] == r1["mutant_dangling_summary_caught"] == 1 and r1["answers_preserved_over_gamma"] == 384
    assert r1["direct_cost_chain3"] == 4 and r1["via_macro_cost_by_exceptions"] == {0: 2, 1: 3, 2: 4, 3: 5, 4: 6} and r1["exception_crossover"] == 2 and r1["decision_criterion"].startswith("OPEN_PARENT_OWNED")
    assert (r2["prefixes"], r2["discourse_states"], r2["dfa_states"]) == (13, 16, 4)
    assert r2["bounded_agrees_when_decisive"] == 879 and r2["bounded_cannot_check_cases"] == r2["decided_by_reachability"] == 161 and r2["sat_complete_at_state_bound"] == 208
    assert r2["unsat_unreachable_by_bound_cases"] == 17 and r2["mutant_bound_is_pass_caught"] == 89 and r2["status"].startswith("PROVED_REGULAR_INVENTORY")
    assert r3["status"] == "OPEN" and r3["viterbi_recompute_vs_subtract"] == ["3/5", "0"] and r3["shared_assumption_naive_vs_exact"] == ["1/2", "3/8"]


def test_run_all_carries_no_novelty_claim(out):
    assert out["NOVELTY"] == "NOT_ESTABLISHED" and out["status"] == "ALL_HOLD"
    assert len([k for k in out if k.startswith("E")]) == 8 and len([k for k in out if k.startswith("R")]) == 3


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
    capsys.readouterr()
