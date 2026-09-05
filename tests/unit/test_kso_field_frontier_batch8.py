"""KSO_FIELD_FRONTIER_THEOREMS_BATCH8_V1 — every item's checker holds, its planted hostiles are caught and its
no-alarm control passes; counts are pinned.  Items H1 (FDX-01), H2 (FDX-02), H3 (FDX-03), H4 (FDX-05)."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_field_frontier_batch8_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_field_frontier_batch8_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all()


def test_h1_open_system_closure(out):
    r = out["H1_FDX01_open_system_closure"]
    assert (r["graphs"], r["coverages"], r["environments"], r["root_free_conclusions"]) == (128, 27, 8, 9)
    assert r["monitored_current_checks"] == 75712 and r["conditional_checks"] == 78976
    assert r["no_closure_cases"] == r["impossibility_witnesses"] == 1727
    assert r["sound_iff_all_roots_covered"] == r["unconditional_sound_iff_all_roots_monitored"] == 3456
    assert r["frozen_root_flipped_unconditional_wrong"] == 22224
    assert (r["mutant_current_validity_without_interface_cases"], r["mutant_current_validity_without_interface_wrong"]) == (179608, 49200)
    assert r["mutant_direct_only_cases"] == r["mutant_direct_only_caught"] == 271
    assert (r["lag_as_of_sound"], r["lag_read_as_current_wrong"]) == (29100, 13128)
    assert r["smallest_impossibility_witness"]["graph"] == {"a": [], "c": ["x1"]} and r["smallest_impossibility_witness"]["flipped"] == "x1"


def test_h1_certificate_is_typed_and_relative_to_D(mod):
    graph = {"a": frozenset({"x1"}), "c": frozenset({"a", "x2"})}
    assert mod.roots_of(graph, "c") == {"x1", "x2"} and mod.mutant_roots_direct_only(graph, "c") == {"x2"}
    cov = {"x1": "UNCOVERED", "x2": "MONITORED", "x3": "MONITORED"}
    assert mod.closure_certificate(mod.roots_of(graph, "c"), cov) == ("NO_CLOSURE", ("x1",))
    assert mod.closure_certificate(mod.mutant_roots_direct_only(graph, "c"), cov) == ("MONITORED_CURRENT", ())
    cov2 = {"x1": "FROZEN", "x2": "MONITORED", "x3": "UNCOVERED"}
    assert mod.closure_certificate(mod.roots_of(graph, "c"), cov2) == ("CONDITIONAL_ON_ASSUMPTIONS", ("x1",))
    sigma1 = {"x1": 0, "x2": 1, "x3": 1}
    assert mod.registered_view(cov, mod.SIGMA0) == mod.registered_view(cov, sigma1)
    assert mod.actual_validity({"x1", "x2"}, mod.SIGMA0) and not mod.actual_validity({"x1", "x2"}, sigma1)


def test_h2_controlled_viability(out):
    r = out["H2_FDX02_controlled_viability"]
    assert r["states"] == r["closed_form_typed_close_agrees"] == r["closed_form_commit_agrees"] == 10584
    assert (r["typed_close_kernel"], r["commit_attractor"], r["commit_needs_no_information_action"]) == (9010, 312, 312)
    assert r["typed_close_and_commit_by_rho"] == {"0": {"typed_close": 3132, "commit": 144}, "1": {"typed_close": 2986, "commit": 84}, "2": {"typed_close": 2892, "commit": 84}}
    assert r["indefinite_safety_kernel_total"] == 1512
    assert (r["mutant_abstain_always_licensed_kernel"], r["mutant_abstain_always_licensed_caught"]) == (10584, 1574)
    assert r["mutant_self_authorize_forged_commits"] == 100 and r["mutant_ignore_envelope_overclaimed"] == 386
    assert r["mutant_ignore_envelope_witness"]["state"] == ["LIVE", 1, "IN", "HIGH", 0, 2, 0, 1]
    assert r["mutant_ignore_envelope_witness"]["terminal"] == "FAILED_DEADLINE_OR_NO_MOVE"
    assert r["no_alarm_ready_states"] == 252 and r["smallest_losing_unknown_with_one_token"] == ["UNKNOWN", 1, "IN", "LOW", 0, 0, 0, 1]


def test_h2_closed_forms_on_single_states(mod):
    ready = ("LIVE", 1, "IN", "LOW", 1, 1, 6, 2)
    assert mod.closed_form_typed_close(ready) and mod.closed_form_commit(ready)
    unknown = ("UNKNOWN", 1, "IN", "LOW", 1, 2, 4, 1)            # query 1 + one forced re-query 1 + act 1 = 3 > 2
    assert not mod.closed_form_typed_close(unknown) and mod.closed_form_typed_close(unknown[:5] + (3, 4, 1))
    assert not mod.closed_form_commit(("UNKNOWN", 1, "IN", "LOW", 1, 6, 0, 0))
    assert mod.closed_form_typed_close(("DEAD", 1, "IN", "LOW", 1, 0, 6, 2)) and mod.closed_form_typed_close(("LIVE", 0, "IN", "LOW", 1, 0, 6, 2))
    assert mod.closed_form_commit(("LIVE", 1, "IN", "HIGH", 1, 2, 5, 0)) and not mod.closed_form_commit(("LIVE", 1, "IN", "HIGH", 1, 2, 5, 1))
    assert not mod.licensed_abstain(("UNKNOWN", 1, "IN", "LOW", 1, 3, 0, 0)) and mod.licensed_abstain(("UNKNOWN", 1, "OUT_FINAL", "LOW", 1, 3, 0, 0))


def test_h3_information_conservation(out):
    r = out["H3_FDX03_information_conservation"]
    assert (r["hypotheses"], r["channels"], r["channel_subsets"], r["garbling_iff_zero_reduction_checks"]) == (16, 6, 64, 384)
    assert r["memory_replay_zero_reduction_classes"] == r["mutant_memory_is_information_caught"] == 533
    assert r["identification_capable_subsets"] == 12 and len(r["minimal_capable_subsets"]) == 5
    assert ["obs_00", "obs_01", "obs_10", "obs_11"] in r["minimal_capable_subsets"] and ["obs_00", "obs_01", "obs_10", "ver_affine"] in r["minimal_capable_subsets"]
    assert r["join_classes_by_observation_count"] == {"0": 1, "1": 2, "2": 4, "3": 8, "4": 16}
    assert r["depth_all_channels"] == r["depth_observations_only"] == 4 and r["entropy_lower_bound_checks"] == 65535
    assert (r["verifiers_below_entropy_bound"], r["verifiers_strictly_help_on_subsets"], r["subsets_tight_at_entropy_bound_all_channels"]) == (0, 2571, 62234)
    assert r["scope_cases"] == 128 and r["extrapolated_by_class_assumption"] == r["scope_collapses_when_assumption_revoked"] == r["mutant_class_scope_unconditional_caught"] == 32
    assert r["risk_channel_exact_unchanged"] == r["mutant_risk_as_exact_eliminates_truth"] == 16
    assert r["bound_by_declared_set"] == {"none": 4, "three_observations": 1, "four_observations": 0} and r["bound_with_verifiers_only"] == 3
    assert r["observed_success_null_probability"] == {"one": "1/2", "five": "1/32"} and r["mutant_single_success_is_proof_caught"] == 1


def test_h3_verdicts_and_garbling(mod):
    three = ("obs_00", "obs_01", "obs_10")
    assert mod.identification_verdict(three, True) == ("UNDECLARED_INFORMATION_GE_BITS", 1)
    assert mod.identification_verdict(three, False, observed_successes=(6,)) == ("IDENTIFICATION_NOT_ESTABLISHED", Fraction(1, 2))
    assert mod.identification_verdict(mod.OBSERVATIONS, True) == ("CONSISTENT_WITH_DECLARED_CHANNELS", 0)
    assert mod.mutant_single_success_is_proof(three, (6,)) == ("UNDECLARED_INFORMATION_GE_BITS", 1)
    assert mod.coarser_than_join("obs_11", three + ("ver_affine",)) and not mod.coarser_than_join("obs_11", three)
    assert len(mod.join_classes(three + ("ver_affine",))) == 16 and len(mod.join_classes(("ver_affine", "ver_monotone"))) == 4
    assert mod.determined_inputs(mod.version_space(0b0110, {0, 1, 2}, frozenset(h for h in mod.HYPS if mod.is_affine(h)))) == {0, 1, 2, 3}
    assert mod.determined_inputs(mod.version_space(0b0110, {0, 1, 2})) == {0, 1, 2}


def test_h4_reversibility_classes(out):
    r = out["H4_FDX05_reversibility_classes"]
    assert r["singles"] == {"revoke:e1": "ESI", "revoke:e2": "ESI", "revoke:e3": "ESI", "revoke:s0": "ESI", "quarantine:a": "ESI",
                            "admit:b": "BOI_STABLE", "adopt:C": "BOI_STABLE", "adopt:D": "BOI_STABLE",
                            "delete:e3": "BOI_DIVERGENT", "delete:e2": "NI", "act": "NI", "dpo:R>R'": "BOI_DIVERGENT"}
    assert r["single_classes"] == {"ESI": 5, "BOI_STABLE": 3, "BOI_DIVERGENT": 2, "NI": 2}
    assert r["sequences_len2"] == 142 and r["class_histogram_len2"] == {"ESI": 25, "BOI_STABLE": 44, "BOI_DIVERGENT": 34, "NI": 39}
    assert r["sequences_len3"] == 1667 and r["class_histogram_len3"] == {"ESI": 125, "BOI_STABLE": 494, "BOI_DIVERGENT": 465, "NI": 583}
    assert r["all_esi_components_give_esi"] == r["esi_composite_implies_esi_components"] == 150 and r["act_in_sequence_gives_ni"] == 414
    assert r["full_state_never_restored"] == r["mutant_history_rewind_refuted"] == 5
    assert r["relearn_vs_reinstate"] == {"reinstate": "ESI", "relearn": "BOI_DIVERGENT"} and r["relearn_route_class"] == "BOI_DIVERGENT"
    assert r["mutant_relearn_is_reinstate_caught"] == r["mutant_out_of_order_rollback_caught"] == r["mutant_readmit_deleted_caught"] == r["mutant_stamp_transitive_inverse_caught"] == 1
    assert r["mutant_out_of_order_witness"] == {"after_mutant": [["C", "art0", None], ["D", "art0", None]], "after_rollback_D": [["C", "art1", "n0"], ["D", "art0", None]]}
    assert r["lifo_rollback_object_exact"] == 1 and r["lifo_rollback_class"] == "BOI_STABLE" and r["dpo_round_trip_class"] == "BOI_DIVERGENT"
    assert r["readmit_invisible_to_projection_witnessed_by_history"] == 1 and r["no_alarm_esi_pairs"] == 2


def test_h4_single_transitions(mod):
    xi0 = mod.base_state()
    r1 = mod.revoke(xi0, "e2")
    assert mod.behaviour_now(r1)[0] == ("LIVE", "DEAD") and mod.pi_sem(mod.reinstate(r1, "e2")) == mod.pi_sem(xi0)
    rel = mod.admit(r1, mod.fresh_id(r1), "b")
    assert mod.behaviour_now(rel) == mod.behaviour_now(xi0) and mod.pi_sem(rel) != mod.pi_sem(xi0)
    assert mod.behaviour_future(rel, xi0.known) != mod.behaviour_future(xi0, xi0.known)
    two = mod.adopt(mod.adopt(xi0, "C", "art1"), "D", "art2")
    with pytest.raises(mod.CannotCheck):
        mod.rollback(two, "C")
    assert mod.rollback(mod.rollback(two, "D"), "C").components == xi0.components
    with pytest.raises(mod.CannotCheck):
        mod.admit(mod.delete(xi0, "e2"), "e2", "b")
    assert mod.classify(xi0, [("act", mod.act)]) == "NI" and mod.classify(xi0, [("quarantine:a", lambda x: mod.quarantine(x, "a"))]) == "ESI"


def test_run_all_status(out):
    assert out["status"] == "ALL_HOLD" and out["NOVELTY"] == "NOT_ESTABLISHED"
    assert set(out["ITEM_STATUS"]) == {"H1_FDX-01", "H2_FDX-02", "H3_FDX-03", "H4_FDX-05"}
    assert len(out["OPEN"]) == 1 and "FD-07" in out["OPEN"][0] and len(out["EXACTLY_BOUNDED_IMPOSSIBILITIES"]) == 4
