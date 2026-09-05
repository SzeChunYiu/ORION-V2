"""KSO_COMPARISON_PREREQUISITE_THEOREMS_BATCH4_V1 — every theorem's checker holds, its planted mutants are
caught and its no-alarm control passes; counts are pinned."""
from __future__ import annotations

import importlib.util
import inspect
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_comparison_prereqs_batch4_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_comparison_prereqs_batch4_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


def test_d1_meg32_equivalence_rules(out):
    r = out["D1_MEG32_equivalence_rules"]
    assert r["size_checks"] == 315 and r["tables_checked"] == 24000 and r["table_grids"] == 240 and r["unconditional_grid_checks"] == 128
    assert Fraction(r["worst_false_residual"]) == Fraction(729, 15625) <= Fraction(1, 20)
    assert r["equivalence_size_checks_large_nd"] == 24 and 0 < r["worst_false_equivalence_large_nd"] <= 0.05
    assert r["m2_zero_discordance_margin"] == "7/1000" and r["m2_conditional_verdict"] == "INCONCLUSIVE"
    assert r["first_nd_equivalence_possible"] == 76 and r["equivalence_power_at_half"] == {10: 0.0, 20: 0.0, 30: 0.0, 50: 0.0, 100: 0.2356, 200: 0.7708}
    assert r["power"]["residual@nd=20,p=9/10"] == 0.867 and r["power"]["residual@nd=50,p=3/5"] == 0.028
    assert r["mutant_p_gt_005_false_equivalence"] == 0.8505 and r["mutant_optional_stopping_size"] == 0.1273 and r["mutant_posthoc_exclusion_size"] == 0.1256
    assert r["fixed_rule_size_at_boundary_30"] == 0.0435 and r["cp_interval_20_15"] == ["509/1000", "913/1000"]


def test_d1_rule_is_a_pure_function_of_the_table(mod):
    assert list(inspect.signature(mod.decide_discordant).parameters) == ["n10", "n01", "delta", "alpha"]
    assert mod.decide_discordant(0, 0) == "INCONCLUSIVE" and mod.decide_discordant(20, 0) == "RESIDUAL_SUPPORTED" and mod.decide_discordant(0, 20) == "PARENT_DOMINATES"
    assert mod.decide_discordant(6, 0) == "RESIDUAL_SUPPORTED" and mod.decide_discordant(5, 0) == "INCONCLUSIVE"


def test_d2_meg14_channel_bounds(out):
    r = out["D2_MEG14_channel_bounds"]
    t = r["table"]
    key = ("teaching_dimension", "extended_teaching_dimension", "membership_query_complexity", "demo_expected_pairs_uniform", "demo_n_for_90pct_uniform", "log2M_ceil")
    assert tuple(t["ALL16"][k] for k in key) == (4, 4, 4, "25/3", 13, 4)
    assert tuple(t["AFFINE8"][k] for k in key) == (3, 3, 3, "13/3", 6, 3)
    assert tuple(t["MONOTONE6"][k] for k in key) == (3, 3, 3, "52/9", 11, 3)
    assert tuple(t["SIX_ORDERS"][k] for k in key) == (1, 1, 1, "2", 4, 3)
    assert r["audits_m3"] == {c: "CONSISTENT" for c in ("INSTRUCTION", "DEMONSTRATION", "INTERACTION", "EXPERIMENTATION")} and r["measured_equal_bound_channels"] == 4
    assert r["six_order_expected_pairs_by_distinct_prob"] == {"0": None, "1/4": "4", "1/2": "2", "1": "1"}
    assert r["mutant_below_bound_caught"] == 2 and r["no_alarm_unidentified"] == 1


def test_d3_meg02_graded_operator_warrant(out):
    r = out["D3_MEG02_graded_operator_warrant"]
    assert r["all_unknown_composition_checks"] == 5776 and r["conformal_coverage_n5_delta_1_3"] == "2/3" and r["conformal_k"] == 4 and r["shifted_scope_coverage"] == "0"
    assert r["mutant_score_as_warrant_live_false"] == ["c2", "c5"] and r["honest_live_false"] == []
    assert r["mutant_certificate_transferred_caught"] == 1 and r["revoking_calibration_kills_claim"] == 1 and r["gating_score_independent"] == 1


def test_d4_meg07_surprise_no_drop(out):
    r = out["D4_MEG07_surprise_no_drop"]
    assert r["one_hop_lower_bound_checks"] == 1176 and r["equivalence_checks"] == 1176 and r["matched_cardinality_noop_seed_sets"] == 41 and r["teleport_free_monotone_checks"] == 187
    assert (r["fanout_k"], r["space_size"], r["fanout_heads_dropped_uniform"], r["fanout_heads_kept_propagated"]) == (13, 20, 13, 13)
    assert r["hub_witness_both_backgrounds"] == 2 and r["mutant_scaled_background_breaks_t06"] == 1 and r["mutant_matched_cardinality_is_noop"] == 1


def test_d4_fanout_threshold_is_exact(mod):
    # (1−α)(|V|−1) < k is the exact drop condition for a one-hop head of a single seed under the uniform background
    a = mod.ALPHA_NAV
    atoms, edges = mod.fanout_fixture(12, 6)          # k = 12, |V| = 19: (2/3)·18 = 12 = k → a*_Q(c) = π(c) exactly, ρ = 0 (KS-T06 boundary)
    pi, _ = mod.backgrounds(atoms, edges, frozenset(), a)
    act = mod.solve_activation(atoms, edges, frozenset(), {"r": Fraction(1)}, a)
    assert act["c0"] == pi["c0"] and not mod.surprising(act, pi)["c0"]
    atoms, edges = mod.fanout_fixture(12, 7)          # k = 12, |V| = 20: (2/3)·19 > 12 → kept by π
    pi, _ = mod.backgrounds(atoms, edges, frozenset(), a)
    act = mod.solve_activation(atoms, edges, frozenset(), {"r": Fraction(1)}, a)
    assert mod.surprising(act, pi)["c0"]


def test_d5_meg20_sufficiency_certificate(out):
    r = out["D5_MEG20_sufficiency_certificate"]
    assert r["agreements_over_gamma_x_Q"] == 8 and r["global_lumpability_fails_restricted_certifies"] == 1 and r["uncovered_query_refine_required"] == 1
    assert r["mutant_without_measurability_caught"] == 1 and r["cotail_witness_measurable_not_lumpable_under_R"] == 1
    assert r["answers"] == {"with_certificate": "ANSWERED_FROM_SUMMARY", "without": "REFINE_REQUIRED"}


def test_d6_meg34_inventory_identifiability(out):
    r = out["D6_MEG34_inventory_identifiability"]
    assert r["reopen_inv1"] == {"d1": [0, 1]} and r["reopen_inv2"] == {"d2": [0], "r1": []}
    assert (r["example_sets"], r["lifecycle_classes"], r["behaviour_classes"], r["nonidentifiability_witness_classes"]) == (14, 9, 2, 3)
    assert r["pairs_separated_by_lifecycle_test"] == r["pairs_conflated_by_mutant"] == 51 and r["renamed_ids_equivalent"] == 2
    assert r["identification_by_distinct_prob"]["0"]["expected_pairs"] is None and r["identification_by_distinct_prob"]["1/4"]["expected_pairs"] == "4"


def test_d7_meg09_multiscale_coherence(out):
    r = out["D7_MEG09_multiscale_coherence"]
    assert r["partitions"] == 52 and r["admissible_partitions"] == r["admissible_all_commute"] == r["commuting_partitions"] == 2 and r["nonadmissible_but_commuting"] == 0
    assert r["mutant_coarse_obstruction_final_caught"] == 2 and r["coarse_gap_refine_required"] == 1 and r["pruned_coarse_ceiling_checked_at_fine"] == 1
    assert r["fixture_outcomes"]["b1|['ea2']"] == ["GAP", "FOUND", "DESCEND_WITH_CERTIFICATE"] and r["fixture_commutes_at_empty"] == 0 and r["fixture_breaks_under_inner_revocation"] == 1


def test_d8_meg23_organisation_admissibility(out):
    r = out["D8_MEG23_organisation_admissibility"]
    assert r["moves"] == 17 and r["local_predicate_equals_global"] == 17 and r["unaffected_fibre_certificates_kept"] == 37
    assert r["verdicts"] == {"split": {"ADMISSIBLE": 2, "REFUSED:FIBRE_NOT_ADMISSIBLE": 6}, "merge": {"ADMISSIBLE": 1, "REFUSED:FIBRE_NOT_ADMISSIBLE": 2}, "relink": {"ADMISSIBLE": 6}}
    assert all(r[k] == 1 for k in ("mutant_relink_raises_authority_caught", "mutant_constitution_touched_refused", "mutant_export_join_refused", "dangling_transport_refused", "pareto_incomparable_scalar_orders_flip", "router_reweight_is_feedback"))


def test_run_all_carries_no_novelty_claim(out):
    assert out["NOVELTY"] == "NOT_ESTABLISHED" and out["status"] == "ALL_HOLD"
    assert len([k for k in out if k.startswith("D")]) == 8


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
    capsys.readouterr()
