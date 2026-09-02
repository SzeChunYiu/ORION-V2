"""Tiny known-answer tests for the H-EXT-4 premium-bound checker.

The full sweep is run via ``--full``; here only the named fixtures and the
smallest exhaustive family are exercised so the test stays well under a minute.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research" / "llm-machine-epistemics" / "h_ext4_premium_bounds.py"
SPEC = importlib.util.spec_from_file_location("h_ext4_premium_bounds", SRC)
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod  # dataclasses need the module registered
SPEC.loader.exec_module(mod)  # type: ignore[union-attr]

TOL = 1e-9


def _pr(m):
    pr = mod.premium(m)
    assert pr["feasible"]
    return pr


def test_witness_formula_all_priors() -> None:
    """Omega_dyn(q) = h_b(q) = h_b(R*), Omega_card = 1, Fano side tight for every prior."""
    for q in (Fraction(1, 2), Fraction(3, 4), Fraction(9, 10)):
        for same in (False, True):
            m = mod.witness(q, same_succ_fibre=same)
            pr = _pr(m)
            cp = mod.cardinality_premium(m, pr)
            assert abs(pr["c_stat"]) <= TOL
            assert abs(pr["omega"] - mod.hb(float(q))) <= TOL
            assert abs(cp["omega_card"] - 1.0) <= TOL
            r = mod.regret_01(pr["stat_opt"][0], m)
            assert abs(r - float(min(q, 1 - q))) <= TOL
            assert abs(mod.upper_bound_fano(m, pr) - pr["omega"]) <= TOL
            merged = pr["stat_opt"][0]
            assert mod.regret_lb(merged, m) <= mod.delta_of(merged, m) + TOL
            assert abs(mod.delta_of(merged, m) - pr["omega"]) <= TOL
    # prior-dependence figure quoted by the clean-room review
    assert abs(_pr(mod.witness(Fraction(9, 10)))["omega"] - 0.4689955935892812) < 1e-9


def test_witness_regret_lower_bound_tight_only_at_uniform() -> None:
    m = mod.witness(Fraction(1, 2))
    pr = _pr(m)
    merged = pr["stat_opt"][0]
    assert abs(mod.regret_lb(merged, m) - 1.0) <= TOL and abs(pr["omega"] - 1.0) <= TOL
    m = mod.witness(Fraction(9, 10))
    pr = _pr(m)
    merged = pr["stat_opt"][0]
    assert mod.regret_lb(merged, m) < mod.delta_of(merged, m) - 1e-3


def test_no_nontrivial_lower_bound_on_premium() -> None:
    """Vanishing-premium family: static-optimum regret stays >= u while Omega -> 0."""
    prev = None
    for u in (Fraction(1, 4), Fraction(3, 10), Fraction(33, 100)):
        m = mod.vanishing_premium(u)
        pr = _pr(m)
        assert min(mod.regret_01(p, m) for p in pr["stat_opt"]) >= float(u) - TOL
        assert prev is None or pr["omega"] < prev
        prev = pr["omega"]
    assert prev < 0.01


def test_phantom_premium_breaks_fano_form_not_label_form() -> None:
    m = mod.phantom_premium()
    pr = _pr(m)
    assert not mod.satisfies_pc(m)
    assert abs(pr["omega"] - 1.0) <= TOL
    assert all(mod.regret_01(p, m) == 0 for p in pr["stat_opt"])
    assert mod.upper_bound_fano(m, pr) < pr["omega"] - 0.5      # Fano form fails
    assert pr["omega"] <= mod.upper_bound_label(m, pr) + TOL     # label form holds


def test_conjecture_c1_refuted_and_label_bound_loose() -> None:
    m = mod.loose_ub_label_example()
    pr = _pr(m)
    assert abs(pr["omega"] - (1.0 - mod.hb(0.25))) <= TOL
    assert mod.conjecture_c1(m, pr) > pr["omega"] + 0.2
    assert mod.upper_bound_delta(m, pr) > pr["omega"] + 0.4
    assert abs(mod.upper_bound_label(m, pr) - mod.upper_bound_delta(m, pr)) <= TOL
    for p in pr["stat_opt"]:
        assert mod.regret_lb(p, m) <= mod.delta_of(p, m) + TOL <= mod.fano_ub(p, m) + 2 * TOL


def test_cardinality_zero_conditions_inequivalent() -> None:
    m = mod.omega_dyn_zero_card_positive()
    pr = _pr(m)
    cp = mod.cardinality_premium(m, pr)
    assert abs(pr["omega"]) <= TOL
    assert cp["k_stat"] == 2 and cp["k_dyn"] == 3
    assert abs(cp["omega_card"] - math.log2(1.5)) <= TOL


def test_dormant_two_step_and_shared_successor() -> None:
    d = mod.dormant_two_step()
    pi = (0, 0, 1, 2, 3, 4)
    assert mod.static_admissible(pi, d) and mod.n1(pi, d) and mod.w_k(pi, d, 1)
    assert not mod.w_k(pi, d, 2) and not mod.right_congruent(pi, d)
    pr = _pr(d)
    assert abs(pr["c_stat"]) <= TOL and abs(pr["c_dyn"] - 1.0) <= TOL
    s = mod.shared_successor()
    assert mod.w_k((0, 0, 1, 1, 2, 3, 4), s, 3)
    assert not any(mod.canon([p[h] for h in range(4)]) == (0, 0, 1, 1) and mod.dynamic_admissible(p, s)
                   for p in mod.rgs_partitions(s.n))


def test_fano_gate_zero_is_a_skip_not_a_pass_on_nonpc_family() -> None:
    """The (ii) counter is PC-gated; without PC the same inequality does fail.

    ``T1_fano_ub_violations == 0`` on the non-PC family must NOT be read as
    "Delta <= sum_x phi_{k_x} held everywhere": the check is only run where (ii)
    is asserted (terminal model AND PC).  Dropping PC must expose violations,
    and the gated and ungated denominators must differ.
    """
    receipt = mod.run(full=False, seed=7)
    row = next(r for r in receipt["A_T1_T2_bounds_by_family"]
               if r["family"] == "random_terminal_nonPC")
    assert row["T1_fano_ub_violations"] == 0                       # gated: no PC machine fails
    assert row["T1_fano_ub_violations_ungated_by_pc"] > 0          # ungated: non-PC machines do
    assert row["T1_machines_with_ungated_fano_ub_violation"] > 0
    assert 0 < row["machines_pc"] < row["machines"]
    assert row["T1_fano_applicable_partitions"] < row["T1_fano_terminal_partitions_ungated_by_pc"]
    # every violation is on a non-PC machine, so the PC-gated pass is a real pass
    assert row["machines_terminal_model"] == row["machines"]
    # a congruent family must have no violation even ungated (control: no false alarm)
    pc_row = next(r for r in receipt["A_T1_T2_bounds_by_family"] if r["family"].startswith("terminal_"))
    assert pc_row["T1_fano_ub_violations_ungated_by_pc"] == 0
    assert pc_row["T1_fano_terminal_partitions_ungated_by_pc"] > 0


def test_card_non_ordering_is_not_a_max_over_classes_artifact() -> None:
    """K maxes over predictive classes, the entropy cost averages; does that matter?

    On every instance behind Remark A.5(d) the current histories occupy a single
    predictive class, so max and total block count coincide and no ordering flips.
    """
    res = mod.check_b_card_definition()
    assert res["instances_checked"] >= 5
    assert res["instances_with_one_predictive_class"] == res["instances_checked"]
    assert res["orderings_that_flip_under_total_count"] == 0
    assert res["verdict"] == "NON_ORDERING_NOT_A_MAX_VS_MEAN_ARTIFACT"
    orders = {r["ordering_max"] for r in res["instances"]}
    assert {"omega_dyn<omega_card", "omega_dyn>omega_card"} <= orders  # both directions present
    assert all(r["definitions_agree"] for r in res["instances"])
    # control: the two definitions ARE different functionals once several
    # predictive classes carry current histories, so the agreement above is a
    # property of these instances and not of the two definitions.
    separated = None
    for m in mod.terminal_family(3, 1, mod.SETS_2, [mod.uniform_prior(3)], None):
        cur = [h for h in range(m.n) if m.probs[h] > 0]
        if len({m.P[h] for h in cur}) < 2:
            continue
        pi = tuple(range(m.n))  # discrete partition: one block per history
        if mod.blocks_total_over_fibres(pi, m) > mod.blocks_per_fibre(pi, m):
            separated = m
            break
    assert separated is not None, "no multi-class machine separates the two K definitions"


def test_small_sweep_passes() -> None:
    receipt = mod.run(full=False, seed=7)
    assert receipt["A_L1_one_step_reduction"]["verdict"] == "PASS"
    assert receipt["A_P1_P2_eps_criterion_and_bayes_regret"]["verdict"] == "PASS"
    assert receipt["A_T1_sandwich_verdict"] == "PASS"
    assert receipt["A_T2_premium_bounds_pc_verdict"] == "PASS"
    assert receipt["A_T2_upper_bound_without_pc"]["verdict"] == "PC_LOAD_BEARING_FOR_FANO_FORM__LABEL_FORM_HOLDS"
    assert receipt["A_C1_no_nontrivial_lower_bound_on_omega"]["verdict"] == "REFUTED"
    assert receipt["B_cardinality"]["verdict"] == "PASS"
    assert receipt["C_multistep"]["verdict"] == "PASS"
    assert receipt["C3_multistep_fano_ub_depth2"]["verdict"] == "PASS"
    assert receipt["scientific_authority"] is False
    assert receipt["empirical_llm_result"] is False
