"""KSO_FIELD_FRONTIER_THEOREMS_BATCH10_V1 — every item's checker holds, its planted hostiles are caught and its
no-alarm control passes; counts are pinned.  Items J1 (FDX-06), J2 (FDX-07), J3 (FDX-14)."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_field_frontier_batch10_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_field_frontier_batch10_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


# --- one test per theorem -------------------------------------------------------------------------


def test_j1_distributed_epistemics(out):
    r = out["J1_FDX06_distributed_epistemics"]
    assert (r["intervals"], r["antitone_checks"], r["causally_closed_views"]) == (168, 4536, 15)
    assert (r["delivery_orders_checked"], r["order_pairs"]) == (59, 259)
    assert r["view_verdicts"] == {"over_claim": 354, "under_claim": 369, "agree": 1797}
    assert r["stale_view_correct_in_history_without_rv2"] == 168
    assert (r["import_authority_pairs"], r["import_commit_always_zero"], r["relay_paths_bounded"], r["two_path_cases"]) == (162, 162, 1458, 490)
    assert r["imports_dead_under_trust_revocation"] == r["native_atoms_unchanged"] == r["receiver_recomputation_agrees"] == 1336
    assert r["compositions_with_import_die_with_trust"] == 148
    assert r["equivocation_delivery_patterns"] == {"detectable": 37, "undetectable": 27}
    assert r["impact_distributes_over_union_checks"] == 4096
    assert r["batched_cone_subset_of_sequential_union"] == r["final_state_order_independent"] == 36
    assert (r["cone_revoke_e1"], r["cone_revoke_trust_m"], r["cone_revoke_e3"]) == (["x", "y", "z"], ["x", "y", "z"], ["n", "q"])
    assert (r["revoke_then_reinstate_batched_cone"], r["revoke_then_reinstate_sequential_cones"]) == (0, 6)
    assert (r["sources_1_robustness_checks"], r["sources_2_robustness_checks"], r["sources_3_robustness_checks"]) == (2, 4, 8)
    assert r["all_nodes_agree_yet_world_truth_rank"] == 0


def test_j2_epistemic_games(out):
    r = out["J2_FDX07_epistemic_games"]
    assert r["adversary_strategies"] == 81 and r["non_interference_checks"] == 486
    assert r["mixed_claim_commits_via_adversary_free_alternative"] == 81
    assert (r["adversary_only_claims_committed_under_REQ_TRUTH"], r["adversary_only_claims_committed_under_REQ_COMMIT"]) == (0, 0)
    assert r["authority_ceiling_checks"] == r["REQ_COMMIT_never_from_evidence"] == 486
    assert r["REQ_REPORT_commits"] == {"c_report": 36, "c_sybil": 61, "c_composed": 18}
    assert r["strategies_forcing_refusal_under_REQ_REPORT"] == {"c_native": 0, "c_native2": 0, "c_mixed": 0, "c_report": 45, "c_sybil": 20, "c_composed": 63}
    assert r["contradiction_local_to_joint_supports"] == 4
    assert r["sybil_independent_supports"] == {"honest": 1, "mutant_id_disjointness": 3, "no_alarm_two_sensors": 2}
    assert r["retraction_cone"] == ["a1", "commit:c_report"] and r["commit_before_retraction_licensed"] == 1
    assert r["confidence_coordinate_ignored_checks"] == 4374
    assert (r["inspection_equilibria_verified"], r["inspection_no_interior_equilibrium"]) == (63, 45)
    assert r["inspection_example"] == {"g": 1, "f": 1, "c": 1, "d": 2, "p_star": "1/2", "q_star": "1/2"}


def test_j3_whole_system_lower_bounds(out):
    r = out["J3_FDX14_whole_system_lower_bounds"]
    assert r["class_sizes"] == {"ALL16": 16, "AFFINE8": 8, "MONOTONE6": 6}
    assert r["identification_bound_checks"] == 327675 and set(r["identification_cost_full_class_by_mix"].values()) == {4}
    assert r["identification_bits_by_class_observations"] == {"ALL16": 4, "AFFINE8": 3, "MONOTONE6": 3}
    assert r["retention_affine_memory"] == {"retained": 8, "cannot_represent": 8, "mutant_description_without_cannot_represent_wrong": 8, "honest_wrong": 0}
    assert r["three_bit_projections_colliding_targets"] == 32
    assert (r["repair_retention_checks"], r["repair_retention_tight_cases"], r["repair_retention_generalisation_checks"]) == (648, 164, 48)
    assert r["fooling_set_pairs"] == 120 and r["equality_transcript_bits_lower_bound"] == 4
    assert r["verification_probes_by_class"] == {"ALL16": {"oblivious": 4, "adaptive": 4, "entropy_bound": 4},
                                                "AFFINE8": {"oblivious": 3, "adaptive": 3, "entropy_bound": 3},
                                                "MONOTONE6": {"oblivious": 4, "adaptive": 3, "entropy_bound": 3}}
    assert r["whole_system_table"]["ALL16"] == {"identification_bits": 4, "retention_bits": 4, "verification_probes_oblivious": 4,
                                                "communication_bits_equality": 4, "repair_plus_retention_min_at_k1": 5, "cannot_represent_targets": 0}
    assert r["whole_system_table"]["AFFINE8"] == {"identification_bits": 3, "retention_bits": 3, "verification_probes_oblivious": 3,
                                                  "communication_bits_equality": 3, "repair_plus_retention_min_at_k1": 4, "cannot_represent_targets": 8}


# --- one test per mutant class ---------------------------------------------------------------------


def test_j1_mutants_caught(out, mod):
    r = out["J1_FDX06_distributed_epistemics"]
    assert r["mutant_lww_divergent_order_pairs"] == 117
    assert r["mutant_lww_witness"] == {"view": ["ri1", "rv1", "rv1b"], "order_a": ["rv1", "ri1", "rv1b"], "order_b": ["rv1", "rv1b", "ri1"],
                                       "lww_a": ["e1"], "lww_b": [], "honest": ["e1"]}
    assert r["mutant_stale_view_as_current_wrong_in_history_with_rv2"] == 97
    assert r["mutant_commit_travels_caught"] == 81 and r["mutant_authority_join_over_paths_caught"] == 490
    assert r["mutant_import_without_message_assumption_survives"] == 883 and r["mutant_trust_sender_verdict_wrong"] == 875
    assert r["mutant_majority_is_world_truth_caught"] == 1
    # direct: revoke-wins vs last-writer-wins on the concurrent revoke/reinstate view
    V = frozenset({"rv1", "ri1", "rv1b"})
    assert mod.revoked_set(V) == {"e1"}
    assert mod.mutant_lww_revocation_bit(("rv1", "rv1b", "ri1")) == frozenset() and mod.mutant_lww_revocation_bit(("rv1", "ri1", "rv1b")) == {"e1"}
    assert mod.rank(mod.mutant_commit_travels(mod.auth(source=1, commit=1), mod.auth(source=1, commit=1)), "commit") == 1
    assert mod.rank(mod.import_authority(mod.auth(source=1, commit=1), mod.auth(source=1, commit=1)), "commit") == 0


def test_j2_mutants_caught(out, mod):
    r = out["J2_FDX07_epistemic_games"]
    assert r["mutant_report_as_truth_commits_under_REQ_TRUTH"] == 36
    assert r["mutant_confidence_gate_commits_under_REQ_TRUTH"] == 36
    assert r["mutant_nogood_kills_endpoint_caught"] == 1
    assert r["mutant_receipt_without_evidence_ids_misses_commitment"] == 1
    assert r["sybil_independent_supports"]["mutant_id_disjointness"] == 3
    s = mod.Strategy({"a1": "asserted", "a2": "asserted", "a3": "asserted"}, frozenset(), Fraction(1))
    assert mod.gate(mod.CLAIMS["c_report"], s, mod.REQS["REQ_TRUTH"])[0] == "REFUSED:AUTHORITY_INSUFFICIENT"
    assert mod.mutant_report_as_truth(mod.CLAIMS["c_report"], s, mod.REQS["REQ_TRUTH"])[0] == "COMMITTED"
    assert mod.mutant_confidence_gate(mod.CLAIMS["c_report"], s, mod.REQS["REQ_TRUTH"])[0] == "COMMITTED"
    assert mod.mutant_sybil_independent_count(mod.CLAIMS["c_sybil"]) == 3
    assert mod.independent_support_count(mod.CLAIMS["c_sybil"], {"a1": "adv", "a2": "adv", "a3": "adv"}) == 1


def test_j3_mutants_caught(out, mod):
    r = out["J3_FDX14_whole_system_lower_bounds"]
    assert r["mutant_charge_channel_one_bit_below_bound_subsets"] == 258644
    assert r["retention_affine_memory"]["mutant_description_without_cannot_represent_wrong"] == 8
    assert r["mutant_repair_from_memory_replay_violations"] == 324
    assert r["mutant_digest_equality_false_same_pairs"] == {"1": 56, "2": 24, "3": 8, "4": 0}
    assert r["mutant_oblivious_verifier_three_probes_monotone_accepts_forgery"] == 6
    assert r["mutant_oblivious_verifier_witness"] == {"probes": [0, 1, 2], "claimed": 0, "actual": 8}
    table = mod.identification_cost(("table",), mod.mutant_charge_channel_one_bit(("table",)))
    assert table[mod.FULL] == 1 < mod.ceil_log2(16)
    assert mod.identification_cost(("table",))[mod.FULL] == 4
    assert mod.truncation_digest(0b0111, 3) == mod.truncation_digest(0b1111, 3)


# --- no-alarm control ---------------------------------------------------------------------------------


def test_no_alarm_controls(out, mod):
    j1, j2, j3 = out["J1_FDX06_distributed_epistemics"], out["J2_FDX07_epistemic_games"], out["J3_FDX14_whole_system_lower_bounds"]
    # J1: a view holding every event agrees with the full history; a view missing nothing never over-claims
    full = frozenset(e.eid for e in mod.EVENTS)
    assert mod.revoked_set(full) == {"e1"} and j1["stale_view_correct_in_history_without_rv2"] == 168
    # J1: two-sensor alternatives count as two independent supports (no Sybil alarm on genuine independence)
    assert j2["sybil_independent_supports"]["no_alarm_two_sensors"] == 2
    # J2: native claims commit under REQ_TRUTH whatever the adversary does; a mixed claim commits through {o2}
    assert j2["strategies_forcing_refusal_under_REQ_REPORT"]["c_native"] == 0 and j2["mixed_claim_commits_via_adversary_free_alternative"] == 81
    assert mod.gate(mod.CLAIMS["c_native"], mod.Strategy({"a1": "absent", "a2": "absent", "a3": "absent"}, frozenset(), Fraction(0)), mod.REQS["REQ_TRUTH"]) == ("COMMITTED", frozenset({"o1"}))
    # J3: four probes separate every pair; the affine memory retains every affine target; four-bit digests never collide
    assert j3["no_alarm_four_probes_separate_all"] == 120 and j3["retention_affine_memory"]["honest_wrong"] == 0
    assert j3["mutant_digest_equality_false_same_pairs"]["4"] == 0


def test_run_all_status_and_cannot_check_exit(out, mod, capsys):
    assert out["status"] == "ALL_HOLD" and out["NOVELTY"] == "NOT_ESTABLISHED"
    assert set(out["ITEM_STATUS"]) == {"J1_FDX-06", "J2_FDX-07", "J3_FDX-14"}
    assert len(out["OPEN"]) == 3 and len(out["CANNOT_CHECK"]) == 3 and len(out["EXACTLY_BOUNDED_IMPOSSIBILITIES"]) == 3
    # CANNOT_CHECK is a distinct exit code, never a pass
    assert mod.main(["--probe-cannot-check"]) == 2
    captured = capsys.readouterr()
    assert '"status": "CANNOT_CHECK"' in captured.out
    with pytest.raises(mod.CannotCheck):
        mod.ceil_log2(0)
