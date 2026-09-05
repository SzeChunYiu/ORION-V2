"""KSO_OPEN_LIST_CLOSURE_THEOREMS_BATCH7_V1 — every item's checker holds, its planted hostiles are caught and its
no-alarm control passes; counts are pinned; the open list is empty and every remaining impossibility is exactly bounded."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_open_list_closure_batch7_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_open_list_closure_batch7_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


def test_g1_depth4_tower_and_j4_j5(out):
    r = out["G1_MEG28_ceilings_beyond_three_inputs"]
    assert r["depth4_targets"] == r["minimum_level_equals_anf_degree"] == 65536
    assert r["level_sizes"] == {"1": 32, "2": 2048, "3": 32768, "4": 65536}
    assert r["witness_checks_independent"] == 65504 and r["jump_admissible_iff_minimum_level"] == 393216
    assert (r["skip_to_higher_level_refused"], r["proposed_level_insufficient_refused"]) == (65472, 129024)
    assert r["mutant_poor_score_refused"] == 256 and r["mutant_partial_level3_caught"] == 16384 and r["cannot_check_when_level3_oracle_missing"] == 63488
    assert r["affine_no_jump_no_alarm"] == 96
    assert (r["j4_affine_maps"], r["j4_degree_invariant_checks"], r["j4_gain_under_affine_registry"]) == (1344, 344064, {1: 0, 2: 0})
    assert r["j4_gain_under_registry_with_transposition"] == 8 and r["mutant_uniform_reformulation_ceiling_caught"] == 1
    assert (r["j5_unrestricted_tool_class_ceilings"], r["j5_one_tool_level_size"], r["j5_registered_ceilings"], r["mutant_unregistered_tool_caught"]) == (0, 80, 176, 1)


def test_g1_functions_on_single_targets(mod):
    and4 = sum(1 << p for p in range(16) if p & 1 and p & 2)                     # x·y on four inputs
    assert mod.degree_int(and4, 4) == 2 and mod.minimum_level_int(and4, 4) == 2
    assert mod.assess_jump_int(and4, 1, 2, mod.trigger_from_chain_int(and4, 1, 4), 4) == "CANDIDATE_FOR_PROTECTED_EVALUATION"
    assert mod.assess_jump_int(and4, 1, 3, mod.trigger_from_chain_int(and4, 1, 4), 4) == "NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT"
    xyzw = 1 << 15
    assert mod.degree_int(xyzw, 4) == 4 and mod.minimum_level_int(xyzw, 4, oracles={3: "CANNOT_CHECK"}) == "CANNOT_CHECK"
    assert mod.assess_jump_int(and4, 1, 2, mod.mutant_poor_score_trigger(), 4) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"


def test_g2_per_source_normalisation(out):
    r = out["G2_MEG07_per_source_normalisation"]
    assert (r["fixture_atoms"], r["fan_out"], r["popular_sources"], r["misses_reproduced"]) == (34, 13, 5, 13)
    assert (r["request_activation"], r["child_activation"], r["child_background"]) == ("1/15", "4/975", "89/11050")
    assert r["monotone_functional_exclusions"] == 39 and r["placebo_seed_sets"] == 127
    assert r["clause_admits_children"] == r["clause_extra_bound"] == r["grandchildren_excluded"] == 13
    assert r["mutant_seed_conditioned_caught"] == r["mutant_rescaled_caught"] == r["mutant_attribution_ratio_caught"] == 1 and r["mutant_rescaled_extra_atoms"] == 13
    assert r["t06_uniform_seed_zero_surprise"] == r["t06b_specific_first_hub_popular"] == r["t06b_hub_only"] == r["sigma_one_no_alarm"] == 1


def test_g2_walk_is_exact_and_the_miss_is_real(mod):
    atoms, out_ = mod.m21_fixture()
    a = mod.activation(atoms, out_, {"r": Fraction(1, 3), "s2": Fraction(1, 3), "s3": Fraction(1, 3)}, Fraction(1, 5))
    pi = mod.activation(atoms, out_, mod.uniform_seed(atoms), Fraction(1, 5))
    assert a["c0"] == Fraction(4, 975) < pi["c0"] == Fraction(89, 11050)
    assert mod.surprise_positive(a, pi)["r"] and not mod.surprise_positive(a, pi)["c0"]


def test_g3_context_free_inventory(out):
    r = out["G3_MEG27_context_free_inventory"]
    assert (r["prefixes"], r["states"], r["cases"]) == (61, 192, 11712)
    assert r["bounded_agrees_with_exact"] == 64356 and r["bounded_cannot_check"] == 5916 and r["fixed_point_agrees_with_min_length_table"] == 11712
    assert (r["sat_cases"], r["unsat_cases"], r["unsat_never_reached_by_any_bound"]) == (2643, 9069, 213)
    assert r["sat_complete_exactly_at_lstar"] == 2643 and r["sat_beyond_every_tried_bound"] == 0
    assert r["lstar_histogram"] == {"0": 432, "1": 972, "2": 567, "3": 252, "4": 420}
    assert r["depth_to_lstar"] == {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5}
    assert (r["mutant_bound_is_pass_caught"], r["mutant_fixed_bound_is_unsat_caught"], r["mutant_regular_approximation_caught"]) == (1374, 4542, 1)


def test_g3_single_prefixes(mod):
    full = {"refs": {"cat", "dog", "bird"}, "live": {"c1": mod.LIVE, "c2": mod.LIVE, "c3": mod.LIVE}, "budget": 3}
    assert mod.cf_exact(("cat", "that", "dog"), full) == "SAT" and mod.cf_bounded(("cat", "that", "dog"), full, 1) == "CANNOT_CHECK"
    assert mod.cf_bounded(("cat", "that", "dog"), full, 2) == "SAT"
    assert mod.cf_exact(("cat", "chased", "ran"), full) == "UNSAT" and mod.mutant_regular_approximation(("cat", "chased", "ran"), full) == "SAT"
    assert mod.mutant_bound_is_pass("CANNOT_CHECK") == "SAT" and mod.mutant_fixed_bound_is_unsat("CANNOT_CHECK") == "UNSAT"


def test_g4_deconsolidation_decision(out, mod):
    r = out["G4_MEG19_deconsolidation_decision"]
    assert r["mdl_cases"] == r["closed_form_checks"] == 315
    assert r["crossover_uses_by_k_and_exceptions"]["1"] == {"0": None, "1": None, "2": None, "3": None}
    assert r["crossover_uses_by_k_and_exceptions"]["3"] == {"0": 2, "1": 4, "2": 6, "3": 8}
    assert (r["exception_liveness_gating_checks"], r["mutant_dead_exception_cases"], r["mutant_premature_split_caught"]) == (8, 7, 7)
    assert r["mdl_keep_without_navigation_gain_witness"] == {"k": 2, "uses": 8, "Q": ["t", "x1"], "before": 4, "after": 5}
    assert mod.mdl_decision(3, 6, 2)[0] == "KEEP" and mod.mdl_decision(3, 6, 3)[0] == "SPLIT"


def test_g5_improvement_halves(out, mod):
    r = out["G5_KST12_KST14_improvement_halves"]
    assert r["t12_chain_cases"] == r["t12_clause_checks"] == 246 and r["t12_never_worse_when_Q_in_exports"] == 6
    assert r["t12_unconditional_refutation"] == {"k": 1, "Q": ["x1"], "before": 1, "after": 3}
    assert r["t12_smallest_holding"] == {"k": 2, "Q": ["t"], "before": 3, "after": 2}
    assert (r["t14_pairs_x_Q"], r["t14_monotone_when_nested"], r["t14_improve_iff_Q_meets_difference"], r["t14_lowered_when_not_nested"]) == (1024, 324, 324, 281)
    assert r["t14_unconditional_refutation"]["after"] == 0 < r["t14_unconditional_refutation"]["before"]
    assert mod.ceiling_on([(0, 1, 1, 0)], ["feat_1", "feat_ab"]) == 0 and mod.ceiling_on([mod.FAB], list(mod.FEATURES)) == 1


def test_g6_measure_reading(out, mod):
    r = out["G6_MEG02_measure_reading"]
    assert (r["antichains"], r["gradings"], r["valuation_identity_checks"], r["monotone_checks"]) == (20, 2, 800, 336)
    assert (r["disjoint_product_rule_checks"], r["shared_product_rule_fails"], r["sum_equals_measure_iff_single_checks"]) == (188, 612, 40)
    assert r["sum_exceeds_one_witness"] == {"D": [["a"], ["c"]], "sum": "7/6", "measure": "5/6"}
    assert r["retraction_by_forcing_equals_survivors"] == 320 and r["batches"] == r["expectation_linearity_checks"] == 1540
    assert (r["mutant_independent_coverage_wrong"], r["independent_coverage_right_when_disjoint"], r["mutant_measure_promotes_liveness_caught"]) == (1404, 77, 1)
    g = {"a": Fraction(1, 2), "b": Fraction(1, 2), "c": Fraction(1, 2)}
    D = mod.canon([frozenset({"a", "b"}), frozenset({"a", "c"})])
    assert mod.plus_times_sum(D, g) == Fraction(1, 2) and mod.measure(D, g) == Fraction(3, 8) and mod.measure(D, g, {"a"}) == 0


def test_g7_reference_arm_grading(out, mod):
    r = out["G7_reference_arm_grading"]
    assert (r["verified_facts"], r["closure_size"], r["in_scope_items"], r["out_of_scope_items"]) == (24, 28, 26, 20)
    assert r["licence_with_registered_negative_rule"] == {"NO": 4, "UNKNOWN": 16}
    assert r["rows"]["unbound_reference"] == {"honest_unknown_licensed": 0, "unlicensed_true": 20, "unlicensed_false": 0, "in_scope_licensed": 26, "truth_grader_out_of_scope": 20}
    assert r["rows"]["default_no"]["truth_grader_out_of_scope"] == 20 and r["rows"]["honest"]["honest_unknown_licensed"] == 20
    assert r["balanced_suite_truth_grades"] == {"honest": 0, "unbound_reference": 20, "default_no": 10}
    assert r["balanced_suite_licensed_grades"] == {"honest": 20, "unbound_reference": 0, "default_no": 0}
    assert r["channel_detector_tail_18_of_20"] == "211/1048576"
    assert mod.grade(("paris", "LOCATED_IN", "spain"), "NO", "UNKNOWN", False) == "UNLICENSED_TRUE"
    assert mod.grade(("paris", "LOCATED_IN", "spain"), "UNKNOWN", "UNKNOWN", False) == "LICENSED_CORRECT"
    assert mod.mutant_truth_grader(("paris", "LOCATED_IN", "spain"), "NO", "UNKNOWN", False) == "CORRECT"


def test_g8_paired_lifetimes(out, mod):
    r = out["G8_paired_lifetimes_design"]
    assert r["critical_wins_by_m"] == {"4": None, "5": 5, "6": 6, "7": 7, "8": 7} and r["size_8_at_7"] == "9/256" and r["two_sided_critical"] == 8
    assert r["bonferroni_critical_by_families"] == {"1": 7, "2": 8, "5": 8, "10": 8, "12": 8, "13": None}
    assert r["size_collapsed_one_coin"] == "1/2" and r["size_iid_binomial"] == "9/256"
    assert (r["unanimous_two_sided_size"], r["unanimous_power_at_0_9"], r["max_families_with_fwer_within_alpha"]) == ("1/128", "43046721/100000000", 6)
    assert (r["valid_substitutions"], r["same_variation_distinct_differences"], r["iid_variation_distinct_differences"]) == (24, 1, 2)
    assert r["mutant_collision_caught"] == r["mutant_echo_leak_caught"] == r["pooling_refused"] == 1
    assert mod.sign_test_power(8, 7, Fraction(9, 10)) == Fraction(81310473, 100000000)
    assert mod.registered_substitution(["blick"], {"paris"}, {"blick": "paris"}) == "REFUSED_COLLISION_WITH_REGISTERED"
    assert mod.echo_leak((("is", "blick", "Yes."), ("Yes.",))) and not mod.echo_leak((("is", "blick", "a", "florp"), ("Yes.",)))


def test_g9_positive_only_identification(out, mod):
    r = out["G9_MEG34_positive_only_identification"]
    assert r["positive_text_never_separates"] == r["mutant_positive_only_locks_on_finite"] == r["one_registered_query_separates"] == 6
    assert r["smallest_non_separating_sample"] == [["NP", "VP"]]
    text = frozenset({("NP", "VP"), ("NP", "CONJ", "NP", "VP")})
    assert mod.consistent(text, [1, 2, 3, None], 8) == [2, 3, None] and mod.mutant_positive_only_identifies(text, [1, 2, 3, None], 8) == 2


def test_run_all_status_open_list_empty_and_no_novelty_claim(out):
    assert out["NOVELTY"] == "NOT_ESTABLISHED" and out["status"] == "ALL_HOLD"
    assert len([k for k in out if k.startswith("G")]) == 9 and set(out["ITEM_STATUS"]) == {f"G{i}" for i in range(1, 10)}
    assert out["OPEN"] == [] and len(out["EXACTLY_BOUNDED_IMPOSSIBILITIES"]) == 7
