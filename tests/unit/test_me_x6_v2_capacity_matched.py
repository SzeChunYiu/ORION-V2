"""ME-X6 V2: the load-bearing facts as executable assertions.

V2's result is a TIE, and a tie is the outcome most easily produced by an arm that
could not have lost. Every claim below is therefore paired with a control that must
fail when the fact is removed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "research/experiments/me-x6-v2"
V1 = ROOT / "research/experiments/me-x6"
for p in (str(V2), str(V1)):
    if p not in sys.path:
        sys.path.insert(0, p)

import mex6v2_fitters as F  # noqa: E402
import mex6v2_run as R  # noqa: E402
from mex6_arms import TYPED_SIGNS  # noqa: E402
from mex6_generator import generate_split  # noqa: E402
from mex6_model import CHANNELS  # noqa: E402
from mex6_oracle import oracle  # noqa: E402

DEV_CACHE: dict[int, tuple] = {}


def dev(per_cell: int = 2):
    if per_cell not in DEV_CACHE:
        insts = generate_split("dev", R.DEV_SEED, per_cell)
        deltas = [F.half_difference(i.window, CHANNELS) for i in insts]
        truths = [oracle(i.window).capability for i in insts]
        DEV_CACHE[per_cell] = (insts, deltas, truths)
    return DEV_CACHE[per_cell]


def protected_analysis():
    p = V2 / "results/ME_X6_V2_PROTECTED_ANALYSIS_V1.json"
    if not p.exists():
        pytest.skip("protected analysis absent")
    return json.loads(p.read_text())


# ---- the fitters are heuristics: they CAN miss a member of their own class -------

def test_forward_selection_can_miss_a_rule_its_own_class_contains():
    f = R.greedy_can_fail_fixture()
    assert f["hidden_rule_correct"] == f["n"] == 6
    assert f["exhaustive_best_correct"] == 6
    assert f["greedy_correct"] == 5
    assert f["greedy_is_suboptimal"]


def test_the_l1_path_can_miss_a_rule_its_own_class_contains():
    f = R.l1_can_fail_fixture()
    assert f["hidden_rule_correct"] == f["n"] == 8
    assert f["l1_correct"] < f["hidden_rule_correct"]


def test_no_exhaustive_search_is_registered():
    """The tautology guard: an exhaustive search over a class containing M's vector
    could not fail, and the tie would be an identity rather than a measurement."""
    d = json.loads((V2 / "ME_X6_V2_CAPACITY_MATCHED_COMPARATOR_DESIGN_V1.json").read_text())
    procs = d["comparator"]["fitting_procedures"]
    assert set(procs) == {"B6_GREEDY_SUBSET_UNTYPED", "B7_L1_PATH_UNTYPED"}
    assert all("exhaustive" not in v.lower() for v in procs.values())
    assert "EXHAUSTIVE" in d["reachability_audit_pre_run"][
        "both_fitters_are_heuristics_that_can_miss_a_member_of_their_own_class"]


# ---- the comparator class can fail and can succeed -------------------------------

def test_the_comparator_class_contains_both_a_failing_and_an_exact_member():
    _, deltas, truths = dev()
    n = len(truths)
    all_plus = F.accuracy(deltas, truths, {c: 1 for c in CHANNELS})
    m_loaded = F.accuracy(deltas, truths, {c: TYPED_SIGNS.get(c, 0) for c in CHANNELS})
    assert all_plus == 28 and n == 56          # a member that fails half the split
    assert m_loaded == n                       # and one that is exact


# ---- the fit is frozen, deterministic, and reproduces ----------------------------

def test_the_frozen_weights_still_reproduce_from_the_public_development_split():
    ok, drift = R.refit_reproduces()
    assert ok, drift


def test_the_fit_is_rng_free_and_repeats_byte_for_byte():
    a = R.fit_on_development()
    b = R.fit_on_development()
    assert a["B8_CAPACITY_MATCHED_BEST"]["weights"] == b["B8_CAPACITY_MATCHED_BEST"]["weights"]
    assert a["B7_L1_PATH_UNTYPED"]["weights"] == b["B7_L1_PATH_UNTYPED"]["weights"]


def test_the_unit_sign_control_reproduces_V1s_own_frozen_signs():
    """Cross-study control: V2's capacity control must BE V1's comparator, not a
    lookalike. V1's frozen signs are read from V1's design JSON and compared."""
    v1 = json.loads((V1 / "ME_X6_COLLECTIVE_EPISTEMICS_EXACT_STUDY_DESIGN_V1.json").read_text())
    v1_signs = {k: int(v) for k, v in
                v1["comparator"]["frozen_fitted_signs"]["B4X_FITTED_UNTYPED"].items()}
    v2 = R.fit_on_development()[R.UNIT_SIGN_ARM]["weights"]
    assert {k: int(v) for k, v in v2.items()} == v1_signs


# ---- capacity matching actually bit ----------------------------------------------

def test_the_registered_comparator_zeroes_channels_and_the_control_does_not():
    fit = R.fit_on_development()
    cmp_w = fit[R.CMP_ARM]["weights"]
    ctl_w = fit[R.UNIT_SIGN_ARM]["weights"]
    assert sum(1 for v in cmp_w.values() if not v) >= 1
    six = ("preprints", "journal_papers", "authors", "citations",
           "semantic_novelty", "disruption")
    assert all(cmp_w[c] == 0 for c in six), "the comparator drops all six M-zeroed channels"
    assert all(ctl_w[c] != 0 for c in six), "V1's unit-sign class cannot drop them"


# ---- the protected outcome, and the control that makes it a measurement ----------

def test_protected_M_and_the_capacity_matched_comparator_tie_with_zero_discordant_pairs():
    a = protected_analysis()
    pa = a["score"]["per_arm"]
    assert a["n_instances"] == 1400
    assert pa[R.M_ARM]["capability_correct"] == 1400
    assert pa[R.CMP_ARM]["capability_correct"] == 1400
    g = a["gates"]
    assert g["G1b_TIE_AT_MATCHED_CAPACITY"]["pass"] is True
    assert g["G1b_TIE_AT_MATCHED_CAPACITY"]["discordant_pairs"] == 0
    assert g["G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT"]["pass"] is False
    assert g["ROUTE"]["terminal"] == "TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY"


def test_protected_the_unit_sign_control_fails_exactly_the_seven_decoupled_strata():
    a = protected_analysis()
    decoupled = {"I1_DUPLICATES", "I2_PARAPHRASE", "I3_MASS_LOW_INFORMATION",
                 "I4_RETRACTED_WORK", "I5_CITATION_RING", "I7_FIELD_SIZE_SCALING",
                 "I8_FASHION_CONCENTRATION"}
    failing = {k.split("|")[0] for k, v in a["by_cell"].items()
               if v[R.UNIT_SIGN_ARM] < v["_n"]}
    assert failing == decoupled
    assert a["score"]["per_arm"][R.UNIT_SIGN_ARM]["capability_correct"] == 700
    assert a["gates"]["G2_CAPACITY_IS_THE_SEPARATOR"]["pass"] is True


def test_un_zeroing_the_six_channels_destroys_the_tie():
    """CONTROL. The tie must be a property of the FITTED vector, not of the scoring
    path. Restoring the comparator's six dropped channels to the control's own signs
    must collapse it to the control's score."""
    _, deltas, truths = dev()
    fit = R.fit_on_development()
    w = dict(fit[R.CMP_ARM]["weights"])
    ctl = fit[R.UNIT_SIGN_ARM]["weights"]
    assert F.accuracy(deltas, truths, w) == len(truths)
    for c in ("preprints", "journal_papers", "authors", "citations",
              "semantic_novelty", "disruption"):
        w[c] = ctl[c]
    assert F.accuracy(deltas, truths, w) < len(truths)


# ---- routing and gate reachability ------------------------------------------------

def _gateset(**over):
    base = {k: {"pass": True} for k in
            ("G0a_KNOWN_ANSWER", "G0b_GENERATOR_VALIDITY", "G0c_NULL_CALIBRATION",
             "G0d_M_EXACT_BY_CONSTRUCTION", "G0e_CAPACITY_MATCHING_BIT",
             "G8_VERDICT_CONSTANCY_WITHIN_CELL", "G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT",
             "G1b_TIE_AT_MATCHED_CAPACITY", "G2_CAPACITY_IS_THE_SEPARATOR",
             "G6_CROSS_SCALE_CONSISTENCY")}
    base["COVERAGE_LEDGER"] = {"all_registered_cells_exercised": True}
    for k, v in over.items():
        base[k] = {"pass": v}
    return base


def test_the_separation_terminal_is_reachable():
    r = R.route(_gateset(G1b_TIE_AT_MATCHED_CAPACITY=False))
    assert r["route"] == "TYPED_STATE_SEPARATES_FROM_A_LEARNED_CAPACITY_MATCHED_PARENT"


def test_a_failed_hard_gate_routes_to_cannot_check_not_to_a_verdict():
    r = R.route(_gateset(G0e_CAPACITY_MATCHING_BIT=False))
    assert r["route"] == "CANNOT_CHECK" and r["terminal"] == "NONE"


def test_neither_live_clause_holding_is_cannot_check_not_a_tie():
    r = R.route(_gateset(G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT=False,
                         G1b_TIE_AT_MATCHED_CAPACITY=False))
    assert r["route"] == "CANNOT_CHECK"


def test_an_unexercised_cell_cannot_be_routed_past():
    g = _gateset(G1b_TIE_AT_MATCHED_CAPACITY=False)
    g["COVERAGE_LEDGER"] = {"all_registered_cells_exercised": False}
    assert R.route(g)["route"] == "CANNOT_CHECK"


# ---- the study never writes into V1, and the protected guard is re-armed ----------

def test_no_V1_artifact_was_written_by_V2():
    assert not (V1 / "results/ME_X6_V2_PROTECTED_RESULTS_V1.json").exists()
    assert R.DESIGN_JSON.parent == V2


def test_the_protected_authorization_was_archived_after_use():
    assert not (V2 / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    used = json.loads((V2 / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json").read_text())
    assert used["consumed"] is True
    import hashlib
    assert hashlib.sha256(used["revealed_protected_seed"].encode()).hexdigest() == \
        used["acknowledged_seed_commitment_sha256"]


def test_the_exact_binomial_tail_does_not_overflow_at_protected_scale():
    from fractions import Fraction
    v = R.binom_upper_tail(900, 1400, Fraction(1, 3))
    assert 0.0 <= v <= 1.0
