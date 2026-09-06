"""KSO_FIELD_FRONTIER_THEOREMS_BATCH11_V1 — every item's checker holds, its planted hostiles are caught and its
no-alarm control passes; counts are pinned.  Items K1 (FDX-09), K2 (FDX-10), K3 (FDX-12)."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_field_frontier_batch11_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_field_frontier_batch11_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


# --- one test per theorem -------------------------------------------------------------------------


def test_k1_infinite_structured_learning(out, mod):
    r = out["K1_FDX09_infinite_structured_learning"]
    assert (r["treebank_rules"], r["saturated_rules"], r["chart_equals_brute_force"]) == (6, 14, 12)
    assert r["saturated_derivations_by_k"] == {"0": 1, "1": 2, "2": 5, "3": 14, "4": 42}
    assert r["treebank_derivations"] == {"N V N P N": 3, "N V N": 2, "N V": 1} and r["treebank_coverage"] == 5
    assert (r["positive_monotonicity_checks"], r["sub_inventories_with_unique_parse_of_N_V_N_P_N"]) == (192, 14)
    assert r["derivations_after_revoking_nmod_and_bare_obl"] == 1 and r["verdict_after_revocation"] == "INTERPRETED"
    assert r["inventories_identified_in_the_limit"] == 255
    assert (r["characteristic_sample_trees"], r["characteristic_sample_lower_bound"]) == (4, 2)
    assert Fraction(r["expected_cover_time_uniform_8"]) == 8 * mod.harmonic(8) == Fraction(761, 35)
    assert Fraction(r["expected_cover_time_zipf_8"]) > Fraction(761, 35) > 8
    assert r["unbounded_arity_conjecture_changes"] == 6
    assert r["honest_verdict_two_attested_attachments"] == "AMBIGUOUS" and r["ranking_scores"] == {"obl": 9, "nmod": 3}
    assert r["completed_packs_by_k"] == {"0": {"span_type": 4, "derivation_identity": 4}, "1": {"span_type": 9, "derivation_identity": 10},
                                         "2": {"span_type": 16, "derivation_identity": 22}, "3": {"span_type": 25, "derivation_identity": 50},
                                         "4": {"span_type": 36, "derivation_identity": 125}}
    # direct: the saturated inventory's count on N V N P N P N is the exact brute-force count
    assert mod.derivations(mod.pp_string(2), mod.saturated_inventory(4)) == 5 == mod.catalan(3)


def test_k2_endogenous_representation_discovery(out, mod):
    r = out["K2_FDX10_endogenous_representation_discovery"]
    assert r["base_terms_up_to_8"] == 9168 and r["base_terms_by_size"] == {"1": 2, "2": 2, "3": 10, "4": 26, "5": 114, "6": 402, "7": 1722, "8": 6890}
    assert (r["minimal_size_base"]["XOR"], r["minimal_size_base"]["EQV"], r["minimal_size_with_xor"]["XOR"], r["minimal_size_with_xor"]["EQV"]) == (8, 8, 3, 4)
    assert r["functions_shortened_by_xor"] == 3 and r["version_space_invariance_checks"] == 81
    assert (r["search_position_base"]["XOR"], r["search_position_with_xor"]["XOR"]) == (2936, 16)
    assert (r["search_position_base"]["EQV"], r["search_position_with_xor"]["EQV"]) == (6990, 38)
    assert (r["positions_raised_by_xor"], r["positions_lowered_by_xor"], r["levin_position_bound_checks"]) == (7, 2, 32)
    assert r["task_sets_adopting_xor"] == 4 and r["mdl_adoption_by_task_set"]["XOR"]["adopted"] == [] and r["mdl_adoption_by_task_set"]["XOR EQV"] == {"adopted": ["EQV", "XOR"], "best_gain": 1}
    assert (r["discovery_selection_bits"], r["given_selection_bits"]) == (4, 0)
    assert r["discovery_evaluation_terms"] == {"candidates": 12, "per_candidate_up_to_8": 26032}
    assert (r["minimal_xor_definitions"], r["unseen_rows_undetermined"]) == (8, 104)
    assert mod.version_space({0: 0, 3: 0}) == frozenset({0, 0b0010, 0b0100, 0b0110})


def test_k3_safe_incremental_commitment(out, mod):
    r = out["K3_FDX12_safe_incremental_commitment"]
    assert r["accepted_strings"] == 6 and r["accepting_states_safe"] == 6
    assert r["unsafe_states"] == [3, 4, 5, 6, 13]
    assert r["garden_path_reason"] == "RETRACTED_BY_COMPLETION:9" and r["late_negation_reason"] == "RETRACTED_BY_COMPLETION:19"
    assert (r["bounded_decisive_agreements"], r["bounded_cannot_check"]) == (147, 33)
    assert r["thresholds_by_state"]["3"] == {"ell_star": 4, "saturation_depth": 5, "first_violation": 5}
    assert r["thresholds_by_state"]["2"] == {"ell_star": 2, "saturation_depth": 6, "first_violation": None}
    assert (r["atomic_channel_pass"], r["streaming_channel_pass"]) == (6, 2)
    assert [s["string"] for s in r["streaming_refusals"]] == ["the horse raced past the barn .", "the horse raced past the barn fell .",
                                                             "the horse did fall .", "the horse did fall not ."]
    assert r["revocation_blocks_emission"] == 1 and r["authorisation_gate_checks"] == 2
    # direct: the exact criterion and the bounded checker at the thresholds
    assert mod.exact_verdict(3)[0] == "UNSAFE" and mod.bounded_verdict(3, 4) == "CANNOT_CHECK" and mod.bounded_verdict(3, 5) == "UNSAFE"
    assert mod.bounded_verdict(2, 1) == "CANNOT_CHECK" and mod.bounded_verdict(2, 2) == "SAFE"          # empty content: ℓ* decides
    assert mod.bounded_verdict(16, 0) == "CANNOT_CHECK" and mod.bounded_verdict(16, 1) == "SAFE"        # content: saturation decides


# --- one test per mutant class ---------------------------------------------------------------------


def test_k1_mutants_caught(out, mod):
    r = out["K1_FDX09_infinite_structured_learning"]
    assert (r["mutant_generalise_family_orders_overshoots"], r["mutant_overshoot_uncorrected_by_positive_text"]) == (254, 254)
    assert r["mutant_rank_licenses_top1_wrong_gold"] == 1
    G = frozenset({mod.rule("V", "nsubj:N", "HEAD", "obj:N")})
    over = mod.mutant_generalise_family_orders(G)
    assert len(over) == 6 and mod.rule("V", "HEAD", "obj:N", "nsubj:N") in over and mod.mutant_generalise_family_orders(over) == over
    assert mod.licensed_commit(2) == "AMBIGUOUS" and mod.mutant_rank_licenses_top1(["obl", "nmod"]) == "INTERPRETED"
    # the packing hostile's shape: derivation-identity keys store one node per derivation (≥ Catalan(k+1) at the top span)
    assert r["completed_packs_by_k"]["4"]["derivation_identity"] >= 42 and r["completed_packs_by_k"]["4"]["derivation_identity"] > r["completed_packs_by_k"]["4"]["span_type"]


def test_k2_mutants_caught(out, mod):
    r = out["K2_FDX10_endogenous_representation_discovery"]
    assert r["mutant_memorising_abstraction_adopted"] == 39 and r["honest_table_priced_abstraction_adopted"] == 0
    assert mod.mutant_memorising_abstraction_gain({0: 1, 1: 0}, 8) == 7 > 0
    assert mod.honest_table_abstraction_cost({0: 1, 1: 0}) == 4
    # honest pricing never adopts on the fixture because every partial table has a consistent function of size ≤ 4
    import itertools
    base_min = mod.minimal_sizes(mod.enumerate_terms(mod.BASE_LIBRARY, 8))
    for pattern in itertools.product((None, 0, 1), repeat=4):
        ev = {i: v for i, v in enumerate(pattern) if v is not None}
        if 0 < len(ev) < 4:
            assert min(base_min[f][0] for f in mod.version_space(ev)) <= 4
    assert len({(f >> 2) & 1 for f in mod.version_space({0: 1, 1: 0})}) == 2       # the unseen row stays undetermined


def test_k3_mutants_caught(out, mod):
    r = out["K3_FDX12_safe_incremental_commitment"]
    assert r["mutant_existential_lookahead_wrong_states"] == 5 and r["mutant_bounded_pass_is_safe_wrong_cases"] == 16
    assert r["mutant_forget_history_emits"] == 1
    assert mod.mutant_existential_lookahead(3) == "SAFE" and mod.exact_verdict(3)[0] == "UNSAFE"
    assert mod.mutant_bounded_pass_is_safe(3, 4) == "SAFE" and mod.bounded_verdict(3, 4) == "CANNOT_CHECK"
    bad = mod.stream(("the", "horse", "slept", "."), revoke_after=3, revoked_ids=frozenset({"e_s"}), forget_history=True)
    good = mod.stream(("the", "horse", "slept", "."), revoke_after=3, revoked_ids=frozenset({"e_s"}))
    assert bad["refused_at"] is None and good["refused_at"] == 3 and good["reason"] == "DEAD:horse_slept" and good["committed"] == ["horse_slept"]


# --- no-alarm control ---------------------------------------------------------------------------------


def test_no_alarm_controls(out, mod):
    k1, k2, k3 = out["K1_FDX09_infinite_structured_learning"], out["K2_FDX10_endogenous_representation_discovery"], out["K3_FDX12_safe_incremental_commitment"]
    # K1: an inventory with one attested attachment gives a unique parse; renaming/ordering the unpack does not change verdicts
    assert k1["derivations_after_revoking_nmod_and_bare_obl"] == 1 and k1["no_alarm_ranking_as_unpack_order"] == 1
    assert mod.derivations(("N", "V"), mod.induce([mod.T_INTR])) == 1
    # K2: the extended library has exactly the 16 behaviours; giving XOR changes no version space
    assert k2["no_alarm_extended_library_same_behaviours"] == 16 and k2["version_space_invariance_checks"] == 81
    # K3: the monotone branch is SAFE at every prefix and the atomic check passes every accepted string
    assert k3["no_alarm_monotone_branch_prefixes_safe"] == 4 and k3["atomic_channel_pass"] == 6
    assert all(mod.exact_verdict(mod.state_of(p))[0] == "SAFE" for p in (("the",), ("the", "horse"), ("the", "horse", "slept"), ("the", "horse", "slept", ".")))


def test_run_all_status_and_cannot_check_exit(out, mod, capsys):
    assert out["status"] == "ALL_HOLD" and out["NOVELTY"] == "NOT_ESTABLISHED"
    assert set(out["ITEM_STATUS"]) == {"K1_FDX-09", "K2_FDX-10", "K3_FDX-12"}
    assert len(out["OPEN"]) == 3 and len(out["CANNOT_CHECK"]) == 3 and len(out["EXACTLY_BOUNDED_IMPOSSIBILITIES"]) == 3
    # CANNOT_CHECK is a distinct exit code, never a pass
    assert mod.main(["--probe-cannot-check"]) == 2
    captured = capsys.readouterr()
    assert '"status": "CANNOT_CHECK"' in captured.out
    with pytest.raises(mod.CannotCheck):
        mod.ceil_log2(0)
