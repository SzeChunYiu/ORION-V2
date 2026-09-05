"""KSO_DIALOGUE_PREREQUISITE_THEOREMS_BATCH3_V1 — every theorem's checker holds, its planted mutants are
caught and its no-alarm control passes; counts are pinned."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_dialogue_prereqs_batch3_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_dialogue_prereqs_batch3_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_c1_meg33_epistemic_action_value(mod):
    r = mod.check_c1_meg33_epistemic_action_value()
    assert r["hypothesis_sets"] == 2500 and r["irrelevant_ambiguity_zero_value_sets"] == 8
    assert r["refinement_pairs_checked"] == 4040 and r["refinement_strict_cases"] == 3920
    assert r["repeated_question_nonpositive"] == 73300
    assert r["query_never_dead_checks"] == 160 and r["closure_only_dead_side_checks"] == 160
    assert r["mutant_query_closes_upper_mints_dead"] == 80 and r["mutant_value_by_separation_caught"] == 1
    assert r["mutant_never_clarify_regret"] == "1"
    assert all(r[k] == 1 for k in ("case_A_no_question", "case_B_clarify", "case_C_refinement_preferred", "case_D_repeat_penalised"))


def test_c1_refinement_is_the_only_general_order(mod):
    # two incomparable partitions of one hypothesis set need not be value-ordered: the theorem is stated for refinement
    V = [(0, 0, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0)]
    pa = [[V[0]], [V[1], V[2]]]
    pb = [[V[1]], [V[0], V[2]]]
    assert not mod.refines(pa, pb) and not mod.refines(pb, pa)
    assert mod.expected_moved(V, pa) == mod.expected_moved(V, pb) == mod.Fraction(4, 3)


def test_c2_meg25_commitment_gate(mod):
    r = mod.check_c2_meg25_commitment_gate()
    assert r["accept_iff_honest_checks"] == 729 and r["honest_plans"] == 12
    assert r["mutant_inject_caught"] == 12 and r["mutant_protected_leak_caught"] == 12
    assert r["mutant_drop_uncertainty_caught"] == 6 and r["mutant_paraphrase_flip_caught"] == 8
    assert r["mutant_launder_said_caught"] == 1 and r["protected_in_plan_refused"] == 1


def test_c2_renderer_signature_has_no_store(mod):
    import inspect

    assert list(inspect.signature(mod.render).parameters) == ["plan"]


def test_c3_meg27_prefix_commitment(mod):
    r = mod.check_c3_meg27_prefix_commitment()
    assert r["sentences"] == 15 and r["prefixes"] == 60 and r["discourse_states"] == 18
    assert r["committed_prefixes_have_completion"] == 371 and r["refused_prefixes_have_none"] == 709
    assert r["full_bound_exact"] == 1080
    assert r["mutant_greedy_commits_dead_end"] == 709 and r["mutant_bound_is_pass_caught"] == 1713
    assert all(r[k] == 1 for k in ("reopen_missing_referent", "reopen_weakened_comparative", "reopen_missing_premise_stated", "no_alarm_all_live", "repair_at_bounded_cost"))


def test_c4_meg11_pipeline_semantics(mod):
    r = mod.check_c4_meg11_pipeline_semantics()
    assert r["fixtures"] == 40 and r["runs"] == 320 and r["replay_identical"] == 320
    assert r["non_terminal_configs_step"] == 1056 and r["live_marks_preserved"] == 1376
    assert r["terminals"] == {"FOUND": 36, "GAP": 156, "OBSTRUCTION": 92, "CANNOT_CHECK": 36}
    assert r["cannot_check_absorbed_runs"] == 36
    assert r["mutant_fire_on_unknown_caught"] == 44 and r["mutant_launder_cannot_check_caught"] == 4 and r["mutant_stale_cache_caught"] == 244


def test_c4_terminals_are_exactly_four(mod):
    assert set(mod.TERMINALS) == {"FOUND", "GAP", "OBSTRUCTION", "CANNOT_CHECK"} and len(mod.STAGES) == 7


def test_c5_meg10_procedure_algebra_laws(mod):
    r = mod.check_c5_meg10_procedure_algebra_laws()
    assert r["profiles_at_n3"] == 20
    assert r["seq_assoc"] == r["seq_unit_annihilator"] == r["seq_warrant_commutes"] == r["alt_assoc_comm_idem_unit"] == r["distributive"] == 8000
    assert r["if_static_below_trace"] == 6400 and r["live_static_implies_live_trace"] == 51200 and r["if_strict_static_dead_trace_live"] == 2824
    assert r["loop_idempotent"] == 3200 and r["meter_exhaustion_cannot_check"] == 3
    assert r["mutant_unmetered_loop_caught"] == r["mutant_if_as_alternative_caught"] == r["mutant_static_for_trace_caught"] == r["mutant_alt_without_certificate_caught"] == 1
    assert r["random_programs_static_below_trace"] == 217


def test_c6_meg15_discriminating_interaction(mod):
    r = mod.check_c6_meg15_discriminating_interaction()
    assert r["worlds"] == 16 and r["sound_eliminations"] == 48 and r["out_of_scope_cannot_check"] == 16
    assert r["feedback_interval_zero"] == 192 and r["mutant_reward_as_outcome_eliminates_truth"] == 96
    assert r["per_input_reopen_on_o0"] == [0, 3]
    assert r["mutant_feedback_raises_interval_caught"] == 1 and r["procedure_interval_unchanged"] == 1


def test_c7_meg16_contradiction_policy(mod):
    r = mod.check_c7_meg16_contradiction_policy()
    assert r["majority_checks"] == 20 and r["two_bridge_verdict_table"] == 16
    assert r["supersession_reopen"] == ["c_tue", "plan"]
    assert all(r[k] == 1 for k in ("records_live_neither_promoted", "composite_dead_parts_intact", "mutant_majority_resolves_caught", "scoped_bridge_resolves_on_scope", "disjoint_scopes_no_contradiction", "retraction_no_laundering", "hostile_history_rewrite_caught", "hostile_stale_cache_caught", "hostile_unrelated_touched_caught", "hostile_retraction_moves_world_caught"))


def test_c8_meg21_representation_lifts(mod):
    r = mod.check_c8_meg21_representation_lifts()
    assert r["affine_span"] == 8 and r["quadratic_span"] == 16 and r["found_outcomes_preserved"] == 8
    assert r["small_candidates"] == 288 and r["small_admitted"] == 48 and r["small_refused"] == 240
    assert all(r[k] == 1 for k in ("m4_lift_admissible", "m4_rollback_exact", "obstructed_query_improves", "mutant_signature_change_refused", "mutant_content_change_refused", "mutant_degrading_lift_refused", "mutant_quotient_merge_refused", "mutant_edge_interval_change_refused"))


def test_run_all_carries_no_novelty_claim(mod):
    out = mod.run_all()
    assert out["NOVELTY"] == "NOT_ESTABLISHED" and out["status"] == "ALL_HOLD"
    assert len([k for k in out if k.startswith("C")]) == 8


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
    capsys.readouterr()
