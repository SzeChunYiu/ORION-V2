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
