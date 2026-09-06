"""KSO_FIELD_FRONTIER_THEOREMS_BATCH9_V1 — every item's checker holds, its planted hostiles are caught and its
no-alarm control passes; counts are pinned.  Items I1 (FDX-08), I2 (FDX-11), I3 (FDX-13), I4 (FDX-15)."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_field_frontier_batch9_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_field_frontier_batch9_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


def test_i1_stochastic_warrant(out):
    r = out["I1_FDX08_stochastic_warrant"]
    assert (r["horizon"], r["paths"], r["models"], r["iid_members"], r["marginal_recursion_agrees"]) == (6, 64, 9, 3, 54)
    assert r["adversary_max_flips_by_envelope"] == {"0": 0, "1": 2, "2": 4, "3": 6, "4": 6, "5": 6, "6": 6} and r["unbudgeted_max_flips"] == 6
    assert r["impossibility_no_rate_bound_without_model_or_envelope_witnesses"] == 6 and r["receipts_typed"] == 640
    assert r["expected_flips_by_model"]["M(a=1/2,b=1/2)"] == "3" and r["expected_flips_by_model"]["M(a=1/4,b=1/4)"] == "3/2"
    assert r["mutant_frequency_as_warrant_wrong_now_paths"] == 6 and r["honest_now_reads_ledger"] == 64
    assert r["mutant_frequency_as_warrant_wrong_next_prob_by_model"]["M(a=1/2,b=1/2)"] == "11/64"
    assert r["predictive_set_sizes"] == {"3": 64} and r["predictive_spread_every_path"] == "1/2"
    assert (r["mutant_rate_equals_some_registered_prediction_paths"], r["mutant_rate_is_no_registered_prediction_paths"]) == (20, 44)
    assert r["max_likelihood_ratio_between_models_at_T"] == "729"
    assert (r["revocation_pairs"], r["mutant_divide_out_posterior_differs"], r["mutant_divide_out_interior_step_differs"]) == (384, 320, 320)
    assert (r["divide_out_exact_at_last_step"], r["divide_out_exact_on_iid_subclass_checks"]) == (64, 1152)
    assert (r["guarantee_horizon"], r["martingale_checks"], r["alpha"]) == (12, 12, "1/20")
    assert Fraction(r["anytime_false_revocation_prob"]) == Fraction(23633, 2097152) <= Fraction(1, 20) < Fraction(r["mutant_stepwise_false_revocation_prob"]) == Fraction(78277, 1048576)
    assert (r["anytime_power_under_alternative"], r["stepwise_power_under_alternative"]) == ("307/1024", "151/256")
    assert r["individual_output_unknown_under_every_evalue"] == 4096 and r["mutant_evalue_promotes_output_caught"] == 794
    assert r["no_alarm_registered_model_gives_exact_receipts"] == 9


def test_i1_receipts_and_hostiles_on_single_paths(mod):
    F = Fraction
    path = (1, 1, 1, 1, 1, 0)
    assert mod.receipt(path) == ("DEAD", "NO_MODEL_REGISTERED", None)
    assert mod.receipt(path, "M(a=1/4,b=3/4)") == ("DEAD", "CONDITIONAL_ON_MODEL:M(a=1/4,b=3/4)", F(3, 4))
    assert mod.receipt(path, "M(a=1/4,b=1/4)")[2] == F(1, 4)
    assert mod.mutant_frequency_as_warrant(path) and mod.mutant_rate_as_probability(path) == F(5, 6)
    assert {mod.predictive(m, path) for m in mod.MODELS} == {F(1, 4), F(1, 2), F(3, 4)}
    assert mod.flips((0, 1, 0, 1, 0, 1)) == 6 and mod.revocations((0, 1, 0, 1, 0, 1)) == 3      # x0 = LIVE: the alternating path
    assert mod.flips((1, 0, 1, 0, 1, 0)) == 5 and mod.revocations((1, 1, 1, 1, 1, 0)) == 1
    assert mod.marginal_live("M(a=1/2,b=1/2)", 3) == F(1, 2)
    # revocation of the last observation: divide-out is exact; of an interior one under a Markov member it is not
    m = "M(a=1/4,b=1/4)"                                        # a Markov member (a + b ≠ 1)
    assert m not in mod.IID_MEMBERS
    assert mod.mutant_divide_out(m, path, 5) == mod.marginal_likelihood_without(m, path, 5)
    assert mod.mutant_divide_out(m, path, 2) != mod.marginal_likelihood_without(m, path, 2)
    iid = "M(a=1/4,b=3/4)"
    assert iid in mod.IID_MEMBERS and mod.mutant_divide_out(iid, path, 2) == mod.marginal_likelihood_without(iid, path, 2)
    # e-process: martingale factors and the anytime rule
    e = mod.e_process((0, 0, 0, 0))
    assert e[0] == F(2) and e[-1] == F(16) and not mod.anytime_revoke((0, 0, 0, 0)) and mod.anytime_revoke((0,) * 5)
    assert mod.interval_liveness((), (frozenset({"g"}),)) == "UNKNOWN" and mod.mutant_evalue_promotes_output(F(1, 2)) == "LIVE"


def test_i2_bifurcation(out):
    r = out["I2_FDX11_bifurcation"]
    assert (r["states"], r["atoms"], r["state_change_pairs"], r["boundary_characterisation_exact"]) == (512, 6, 3840, 3840)
    assert r["total_flips"] == r["flips_explained_by_cut_completion_nogood_authority"] == 2524
    assert r["jump_size_histogram"] == {"0": 2136, "1": 1116, "2": 396, "3": 160, "4": 24, "5": 8}
    assert r["max_jump_by_change_kind"] == {"add_nogood": 2, "grant": 5, "reinstate": 2, "revoke": 2, "withdraw": 5}
    assert (r["states_on_a_boundary"], r["monotone_in_evidence_checks"]) == (504, 1024)
    assert r["mutant_flip_is_mechanism_failure_alarms"] == 588 and r["mutant_graded_continuity_masked_flips"] == 1688
    assert r["sensitivity_at_full_evidence"] == {"c": 3, "x1": 1, "x2": 0, "x3": 0, "x4": 2, "x5": 1}
    assert r["authority_withdraw_s1_jump_at_full_state"] == 5
    assert (r["grounded_extension_equals_c7_policy"], r["states_with_two_stable_extensions"], r["mutant_pick_a_stable_extension_caught"]) == (512, 32, 32)
    assert r["conflict_resolved_by_one_revocation_states"] == 32
    assert r["certificate_table"]["and@dead=[]"] == "OBSTRUCTION" and r["certificate_table"]["xor@dead=['e1']"] == "REINSTATE_FIRST" and r["certificate_table"]["xor@dead=[]"] == "SUCCESS"
    assert (r["obstruction_iff_evidence_invariant_failure"], r["mutant_certify_on_boundary_caught"], r["obstruction_evidence_neighbours_flipping"]) == (12, 5, 0)
    assert r["obstruction_moved_only_by_representation_change"] == 1


def test_i2_boundary_rules_on_single_states(mod):
    full = (frozenset(), frozenset(), frozenset(mod.AUTH_BITS))
    assert mod.commitment_set(full) == frozenset(mod.ATOMS2)
    assert mod.predicted_flips(full, ("revoke", "e1")) == {"x1", "c"}            # e1 is a cut for x1 and c, not for x2 / x3
    assert mod.predicted_flips(full, ("revoke", "e2")) == {"x4", "c"}
    assert mod.predicted_flips(full, ("withdraw", "s1")) == {"x1", "x2", "x3", "x4", "c"}
    assert mod.predicted_flips(full, ("add_nogood", 1)) == {"x4", "c"}             # nogood {e2, e3} covers x4's only alternative and c's
    dead1 = (frozenset({"e1"}), frozenset(), frozenset(mod.AUTH_BITS))
    assert mod.predicted_flips(dead1, ("reinstate", "e1")) == {"x1", "c"}
    assert mod.commitment_set(dead1) ^ mod.commitment_set(full) == {"x1", "c"}
    assert mod.mutant_flip_is_mechanism_failure({"x1", "c"}) and not mod.mutant_flip_is_mechanism_failure({"x1"})
    assert mod.grounded_extension(frozenset({"x3", "x4", "x1"}), {("x3", "x4"), ("x4", "x3")}) == {"x1"}
    assert len(mod.stable_extensions(frozenset({"x3", "x4", "x1"}), {("x3", "x4"), ("x4", "x3")})) == 2
    assert mod.certificate("and", frozenset()) == "OBSTRUCTION" and mod.certificate("xor", frozenset({"e2"})) == "REINSTATE_FIRST"
    assert mod.mutant_certify_on_boundary("xor", frozenset({"e2"})) == "OBSTRUCTION"
    assert not mod.fails("and", frozenset(), extra=(mod.FAB,))


def test_i3_self_model_calibration(out):
    r = out["I3_FDX13_self_model_calibration"]
    assert (r["fixtures"], r["prediction_grid"], r["closed_form_fixed_points_agree"]) == (75, 9, 75)
    assert r["fixed_point_count_histogram"] == {"0": 9, "1": 59, "2": 7}
    assert (r["orbits_converge"], r["orbits_period_two"]) == (594, 81)
    assert (r["fixtures_without_stable_self_prediction"], r["unregistered_loop_prediction_wrong_under_adoption"]) == (9, 26)
    assert r["bistable_witness"] == {"rA": "0", "rB": "1/2", "theta": "1/4", "fixed_points": ["0", "1/4"]}
    assert (r["prediction_cases"], r["mutant_score_on_caused_outcomes_caught"]) == (675, 42)
    assert (r["self_fulfilling_prediction_cases"], r["counterfactual_calibrated_cases"], r["counterfactual_calibrated_but_performatively_wrong"]) == (215, 219, 46)
    assert (r["adaptive_reuse_tables"], r["mutant_reuse_heldout_expected_reported_score"], r["fresh_heldout_expected_score"], r["adaptive_optimism_bias"]) == (512, "47/64", "1/2", "15/64")
    assert r["prediction_record_authority"] == {"self_model": 1, "world_truth": 0, "commit": 0} and r["mutant_prediction_as_warrant_caught"] == 2
    assert r["no_alarm_registered_loop_fixed_point_computable"] == 66


def test_i3_performative_map_on_single_fixtures(mod):
    F = Fraction
    # converging: rA = 1, rB = 1/4, theta = 1/2 — unique stable prediction 5/8, reached from every start in ≤ 2 steps
    assert mod.fixed_points(F(1), F(1, 4), F(1, 2)) == (F(5, 8),)
    assert mod.orbit(F(0), F(1), F(1, 4), F(1, 2))[:3] == [F(0), F(1), F(5, 8)]
    # period two: rA = 1/2, rB = 0, theta = 1/2 — no stable prediction; the shadow rate 1/4 is defined
    assert mod.fixed_points(F(1, 2), F(0), F(1, 2)) == ()
    seq = mod.orbit(F(0), F(1, 2), F(0), F(1, 2))
    assert seq[1:5] == [F(1, 2), F(1, 4), F(1, 2), F(1, 4)] and mod.counterfactual_rate(F(1, 2), F(0)) == F(1, 4)
    # bistable
    assert mod.fixed_points(F(0), F(1, 2), F(1, 4)) == (F(0), F(1, 4))
    # scored on caused outcomes: prediction 1 with rA = 1, rB = 0, theta > 1 never reached → routes only easy tasks
    assert mod.mutant_score_on_caused_outcomes(F(1), F(1), F(0), F(3, 4)) is False       # 1 ≥ 3/4 routes all: realised 1/2
    assert mod.mutant_score_on_caused_outcomes(F(1, 2), F(1, 2), F(0), F(3, 4)) and not mod.counterfactual_calibrated(F(1, 2), F(1, 2), F(0))
    assert mod.mutant_reuse_heldout_selects_best(((1, 0, 0), (1, 1, 0), (0, 0, 0))) == 2
    assert mod.mutant_prediction_as_warrant(F(7, 8)) == "LIVE" and mod.interval_liveness((), (frozenset({"r"}),)) == "UNKNOWN"


def test_i4_residual_attribution(out):
    r = out["I4_FDX15_residual_attribution"]
    assert (r["tasks"], r["lifetimes"]) == (12, 8)
    assert r["real"] == {"diffs": ["1", "3/4", "3/4", "1/2", "3/4", "1/2", "1/2", "1/4"], "p": "1/256", "verdict": "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE", "ablation_mismatched_units": 0}
    assert r["unmatched"]["verdict"] == "RESIDUAL_CONFOUNDED_BY_UNMATCHED_INFORMATION" and r["unmatched"]["ablation_mismatched_units"] == 16
    assert r["unmatched"]["mutant_verdict"] == "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE" and r["mutant_attribute_any_rejection_caught_unmatched"] == 1
    assert r["undetectable"] == {"diffs": ["0", "0", "0", "0", "0", "1/4", "1/4", "1/4"], "p": "1/8", "verdict": "INCONCLUSIVE_UNDERPOWERED"}
    assert r["power_ge_7_of_8_by_win_probability"]["1/2"] == "9/256" and r["power_ge_7_of_8_by_win_probability"]["9/10"] == "81310473/100000000"
    assert r["minimum_detectable_win_probability_power_0_8"] == "9/10"
    assert r["within_lifetime_d1_on_four_items"] == "INCONCLUSIVE on all 15 tables"
    assert (r["smallest_n_d_all_ocm_wins_for_residual_supported"], r["smallest_n_d_for_parent_sufficient_at_p_half"]) == (6, 76)
    assert r["collapsed"]["verdict"] == "RESIDUAL_ONE_COIN_FLAGGED" and r["collapsed"]["one_coin_size"] == "1/2" and r["mutant_attribute_any_rejection_caught_collapsed"] == 1
    assert r["pseudo_replication"] == {"one_lifetime_3_0_p": "1/8", "pooled_x3_9_0_p": "1/512", "verdict": "REFUSED_PSEUDO_REPLICATION"}
    assert r["reference_inside"] == {"licence_grading_diffs": "1", "truth_grading_diffs": "-1", "verdict": "REFUSED_REFERENCE_ARM_IN_DECISION"}
    assert r["parent_plus_delta_equals_ocm_cases"] == 3 and r["no_alarm_matched_family_ties"] == 1


def test_i4_attribution_rule_on_single_cases(mod):
    F = Fraction
    matched = frozenset({"LESSONS", "MANIFEST"})
    a = mod.compare(matched, matched, "real")
    assert a["test"]["verdict"] == "OCM_RESIDUAL" and a["matched_by_ablation"] and a["parent_plus_delta_equals_ocm"]
    b = mod.compare(matched, frozenset({"LESSONS", "MANIFEST_PARTIAL"}), "real", family="F")
    assert not b["matched_by_ablation"] and mod.attribute_residual(b["test"], b["matched_by_ablation"]) == "RESIDUAL_CONFOUNDED_BY_UNMATCHED_INFORMATION"
    assert mod.mutant_attribute_any_rejection_to_delta(b["test"]) == "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE"
    t = mod.sign_test_one_sided([F(1)] * 8)
    assert t["collapsed"] and t["p"] == F(1, 256) and mod.attribute_residual(t, True) == "RESIDUAL_ONE_COIN_FLAGGED"
    t2 = mod.sign_test_one_sided([F(0)] * 5 + [F(1, 4)] * 3)
    assert t2["p"] == F(1, 8) and t2["verdict"] == "INCONCLUSIVE" and mod.attribute_residual(t2, True) == "INCONCLUSIVE_UNDERPOWERED"
    assert mod.attribute_residual(t, True, reference_inside=True) == "REFUSED_REFERENCE_ARM_IN_DECISION"
    assert mod.attribute_residual(t, True, pseudo_replicated=True) == "REFUSED_PSEUDO_REPLICATION"
    assert mod.decide_discordant(4, 0) == "INCONCLUSIVE" and mod.decide_discordant(6, 0) == "RESIDUAL_SUPPORTED" and mod.decide_discordant(38, 38) == "PARENT_SUFFICIENT"
    assert mod.decide_discordant(37, 37) == "INCONCLUSIVE" and mod.decide_discordant(0, 6) == "PARENT_DOMINATES"
    o = mod.arm_outcomes(matched | {"U"}, False, (0, 0, 0, 0))
    assert all(o[f"O{i}"] == 0 for i in range(1, 5)) and all(mod.arm_outcomes(matched | {"U"}, False, (0, 0, 0, 0), "truth")[f"O{i}"] == 1 for i in range(1, 5))


def test_run_all_status(out):
    assert out["status"] == "ALL_HOLD" and out["NOVELTY"] == "NOT_ESTABLISHED"
    assert set(out["ITEM_STATUS"]) == {"I1_FDX-08", "I2_FDX-11", "I3_FDX-13", "I4_FDX-15"}
    assert out["OPEN"] == [] and len(out["CONJECTURES"]) == 1 and "FDX-15" in out["CONJECTURES"][0]
    assert len(out["EXACTLY_BOUNDED_IMPOSSIBILITIES"]) == 5
