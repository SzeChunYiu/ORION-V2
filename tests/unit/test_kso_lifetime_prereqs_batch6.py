"""KSO_LIFETIME_PREREQUISITE_THEOREMS_BATCH6_V1 — every item's checker holds, its planted hostiles are caught and its
no-alarm control passes; counts are pinned."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_lifetime_prereqs_batch6_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_lifetime_prereqs_batch6_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


def test_f1_capability_level_revocation(out):
    r = out["F1_P1_capability_revocation"]
    assert (r["profiles"], r["cases"], r["refused_unauthorized"]) == (85, 21760, 10880)
    assert r["cut_iff_checks"] == r["hitting_set_iff_checks"] == r["monotone_checks"] == 10880 and r["reply_never_claims_removal_while_live"] == 32640
    assert r["mutant_silent_cases"] == r["mutant_silent_caught"] == 10584 and r["clarify_cases"] == 7488 and r["single_warrant_no_alarm"] == 1
    assert r["m12_two_sense_word"] == {"unspecified": "CLARIFY_REMAINDER", "capability": "CAPABILITY_REMOVED", "capability_without_authority": "CAPABILITY_PERSISTS_UNAUTHORIZED_REMAINDER", "mutant": "REVOKED"}


def test_f1_readings_are_policies_over_the_lattice(mod):
    word = mod.capability_profile([{"L_early"}, {"L_late"}])
    r_named, rep = mod.revoke_named(word, frozenset(), "L_late", {"L_early", "L_late"})
    assert rep["capability"] == mod.LIVE and rep["remainder"] == [frozenset({"L_early"})]
    r_all, rep_all = mod.revoke_all(word, frozenset(), "L_late", {"L_early", "L_late"})
    assert rep_all["capability"] == mod.DEAD and r_named < r_all
    assert mod.revoke_all(word, frozenset(), "L_late", {"L_early"})[1]["status"] == "REFUSED_UNAUTHORIZED"


def test_f2_unit_of_inference(out):
    r = out["F2_P2_unit_of_inference"]
    assert r["m12_revoked_stops_p_single"] == "1/4" and r["pooled_p_by_k"] == ["1/4", "1/16", "1/64"] and r["between_ordering_variance"] == "0" and r["n_eff_kish_rho1"] == "2"
    assert r["pooling_monotone_checks"] == 54 and r["pooling_crosses_alpha_tables"] == 16 and r["honest_units_for_three_orderings"] == 1 and r["mutant_pool_orderings_caught"] == 1
    assert r["size_n54_by_block"]["54"] == "1/2" and r["size_n54_by_block"]["27"] == "1/4" and r["size_n54_by_block"]["6"] == "65/256" and Fraction(r["size_n54_by_block"]["1"]) <= Fraction(1, 20)
    assert r["min_lifetimes_for_rejection"] == 5 and r["sign_test_size_ok_m5_30"] == 26 and r["order_permutation_p_identical"] == "1"
    assert r["power_by_m_and_p"]["8"]["9/10"] == "81310473/100000000" and r["power_by_m_and_p"]["5"]["9/10"] == "59049/100000"


def test_f2_exact_sizes_are_fractions(mod):
    assert mod.critical_value(4) is None and mod.critical_value(5) == 5 and mod.sign_test_p(6, 6) == Fraction(1, 64)
    assert mod.size_under_block_dependence(54, 54) == Fraction(1, 2) and mod.paired_lifetime_power(8, Fraction(9, 10)) > Fraction(4, 5)


def test_f3_observational_limits(out):
    r = out["F3_P3_observational_limits"]
    assert (r["observations"], r["identified_by_observation"], r["ambiguous_nominal"], r["verdict_set_size_on_nominal"]) == (512, 504, 8, 2)
    assert r["representation_completions_per_nominal"] == 1 and r["completions_per_observation"] == 250
    assert r["honest_posterior_constant_over_repeats"] == ["1/250"] * 6 and r["mutant_posterior_over_repeats"][-1] == "32/281"
    assert r["fully_tried_traces"] == r["adaptive_exact"] == 65536 and r["adaptive_worst_case_runs"] == 3 and r["adaptive_expected_runs_uniform"] == "7/4"
    assert r["mutant_two_run_cases"] == r["mutant_two_run_caught"] == 16 and r["proper_subsets_nonidentifying"] == 7 and r["zero_runs_on_identified_observations"] == 64512


def test_f4_false_structural_alarm(out):
    r = out["F4_P4_false_structural_alarm"]
    assert (r["fixtures"], r["failed_runs"]) == (26208, 24498)
    assert r["explained_by_dead_warrant"] == r["lemma_checks"] == r["mutant_dead_is_structural_caught"] == r["reinstate_then_fresh_obstruction"] == 4842
    assert r["certificate_never_obstruction_when_dead"] == 19368 and r["converse_dead_but_not_explained"] == 14526 and r["converse_local_without_dead"] == 3420 and r["no_dead_no_alarm"] == 5130


def test_f4_lemma_on_a_single_fixture(mod):
    path = ((frozenset({"e1"}),),)
    assert not mod.run_path(path, (0,), {"e1"}, False, False) and mod.dead_on_path(path, (0,), {"e1"}) == [0]
    assert mod.minimum_sufficient(path, (0,), {"e1"}, False, False) == "D2" and mod.certificate_status(path, (0,), {"e1"}, True) == "REINSTATE_FIRST"
    assert mod.mutant_dead_is_structural(path, (0,), {"e1"}, False, False) == "D3"


def test_f5_epistemic_identity(out):
    r = out["F5_P5_epistemic_identity"]
    assert r["machines"] == r["honest_restart_same_machine"] == r["commitments_attributable_after_honest_restart"] == 20 and r["atom_liveness_preserved_checks"] == 92
    assert r["s31_split_stale_handle_passes"] == r["s31_split_caught"] == r["commitments_not_attributable_after_split"] == 20
    assert r["truncated_log_path_check_passes"] == r["truncated_log_caught"] == r["out_of_band_component_swap_caught"] == r["lineage_rewrite_caught"] == r["in_memory_lineage_lost_after_restart"] == 20
    assert r["honest_extension_no_alarm"] == 1 and r["reasons"] == {"ROOT_OR_PREFIX_BROKEN": 20}


def test_f6_graded_semiring_half(out):
    r = out["F6_MEG02_graded_half"]
    assert (r["families"], r["gradings"], r["cases"]) == (469, 8, 60032) and r["absorption_exact"] == r["graded_retraction_exact"] == r["positive_iff_live"] == 60032
    assert r["grade_above_one_breaks_absorption"] == r["mutant_scalar_subtract_caught"] == r["single_derivation_no_alarm"] == 1 and r["scalar_witnesses_found"] == 2
    assert r["smallest_scalar_witness"] == ([["a"]], [["a"], ["b"]], "a", "9/10", "0", "3/5")
    assert r["plus_times_sum_exact_cases"] == 840 and r["plus_times_sum_strictly_over"] == 1974 and r["measure_retraction_exact"] == 2814 and r["r3_witness_as_measure"] == "3/8"
    assert r["status"].startswith("PROVED (max,×)")


def test_f7_j2_j3_ceilings(out):
    r = out["F7_MEG28_j2_j3_ceilings"]
    assert r["targets"] == r["minimum_level_equals_anf_degree"] == r["mutant_poor_score_refused"] == 256 and r["level_sizes"] == {"1": 16, "2": 128, "3": 256}
    assert r["witness_checks"] == 368 and r["jump_admissible_iff_minimum_level"] == 768 and r["s6_skip_to_top_refused"] == 112 and r["proposed_level_insufficient_refused"] == 128
    assert r["mutant_partial_level2_caught"] == 64 and r["cannot_check_when_level2_oracle_missing"] == 240 and r["affine_no_jump_no_alarm"] == 32
    assert r["e3_and_embedding"] == {"level1": "CEILING", "minimum_level": 2, "witness": [[0, 1]]} and r["meg07_per_source_normalisation"].startswith("OPEN")


def test_f8_reference_arm_binding(out):
    r = out["F8_P6_reference_arm_binding"]
    assert r["target_x_example_sets"] == r["version_space_exact"] == r["identified_iff_four_examples"] == r["outside_bits_checks"] == 256 and r["label_checks"] == 10
    assert r["m12_shape"] == {"paired": "RESIDUAL_SUPPORTED", "mutant_reference_as_matched": "PARENT_DOMINATES"}
    assert r["mutant_reference_as_matched_caught"] == r["mutant_prompt_matching_caught"] == r["matched_parent_no_alarm"] == 1 and r["undeclared_bits_on_k2"] == 2 and r["certified_matched_possible"] is False


def test_hostiles_are_applied_and_caught(mod):
    # F1 silent revoke-named on a two-sense word
    word = mod.capability_profile([{"L_early"}, {"L_late"}])
    r2, reply, rem = mod.mutant_revoke_named_silent("CAPABILITY", word, frozenset(), "L_late", {"L_early", "L_late"})
    assert reply == "REVOKED" and mod.live(word, r2) and mod.notice_semantics("CAPABILITY", word, frozenset(), "L_late", {"L_early", "L_late"})[1] == "CAPABILITY_REMOVED"
    # F2 pooling three identical re-orderings
    assert mod.mutant_pool_orderings([(2, 0)] * 3) == "RESIDUAL_SUPPORTED" and mod.lifetime_design([(2, 0)] * 3, distinct_streams=False) == (1, "DESCRIPTIVE")
    # F3 repetition updates the mutant, never the honest posterior
    f0 = {k: v[0] for k, v in mod.FIELDS.items()}
    assert mod.posterior_rep(Fraction(1, 250), f0, 5) == Fraction(1, 250) < mod.mutant_posterior_from_repetition(Fraction(1, 250), f0, 5)
    # F5 stale handle passes the split; honest check catches it
    import random
    m = mod.build_machine(random.Random(1), "t")
    before = mod.identity_of(m["active"], m["components"])
    s = mod.restart_split(m)
    assert mod.stale_handle_check(s) and mod.same_machine(before, s["active"], s["components"]) == (False, "ROOT_OR_PREFIX_BROKEN")
    # F6 scalar subtraction on the witness
    g = {"a": Fraction(9, 10), "b": Fraction(3, 5)}
    D = {frozenset({"a"}), frozenset({"b"})}
    assert mod.mutant_scalar_subtract(mod.graded_value_recompute(D, g, frozenset()), g["a"]) == 0 != mod.graded_value_recompute(D, g, {"a"})
    # F7 POOR_SCORE trigger refused
    and3 = tuple(x[0] & x[1] for x in mod.INPUTS3)
    assert mod.assess_jump(and3, 1, 2, mod.mutant_poor_score_trigger()) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
    # F8 reference arm entered as the matched parent flips the verdict; the honest report refuses
    assert mod.mutant_reference_as_matched((9, 1), (0, 10)) == "PARENT_DOMINATES"
    with pytest.raises(mod.CannotCheck):
        mod.comparison_report((9, 1), (0, 10), "MATCHED")


def test_run_all_status_and_no_novelty_claim(out):
    assert out["NOVELTY"] == "NOT_ESTABLISHED" and out["status"] == "ALL_HOLD"
    assert len([k for k in out if k.startswith("F")]) == 8 and set(out["ITEM_STATUS"]) == {f"F{i}" for i in range(1, 9)} and len(out["OPEN"]) == 3


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
    capsys.readouterr()
