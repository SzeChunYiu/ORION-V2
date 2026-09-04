"""ME-X6 V2 runner: selftest / fit / dev / protected / analyze.

    selftest    fitter known-answer fixtures, generator validity, null calibration,
                and the pre-run REACHABILITY audit of every registered clause
    fit         fit the capacity-matched comparators on the PUBLIC development split
                and print the vector to be frozen into the design JSON
    dev         score every arm on the development split
    protected   refuses unless PROTECTED_RUN_AUTHORIZATION.json is present, the
                acknowledged design digest matches, and the custody seed hashes to
                the frozen commitment
    analyze     gates and route from an existing results/custody pair

V1's modules are imported READ-ONLY from ../me-x6.  Nothing in this study writes to
me-x6/, refits B4X_FITTED_UNTYPED's frozen signs, or touches a V1 gate, number or
authorization.  V1's result is immutable; this is a new run identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "me-x6"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(V1))

import mex6v2_fitters as F  # noqa: E402
from mex6_arms import TYPED_SIGNS, fit_signs  # noqa: E402
from mex6_generator import CELLS, generate_split  # noqa: E402
from mex6_model import CHANNELS, FALL, FLAT, RISE, SCALES  # noqa: E402
from mex6_oracle import decidable_from_fit_window, oracle, planter_agrees  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x6-v2.capacity-matched-comparator-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x6-v2.capacity-matched-comparator-analysis.v1"
DESIGN_JSON = HERE / "ME_X6_V2_CAPACITY_MATCHED_COMPARATOR_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEFAULT_SEED_FILE = Path.home() / ".orion-custody" / "me-x6-v2" / "PROTECTED_SEED_V1.txt"

DEV_SEED = "ME-X6-V2-DEV-20260904"
DEV_PER_CELL = 2                      # the split the comparator is FITTED on, n = 56
PROTECTED_PER_CELL = 50               # n = 1400, matching V1's protected size

M_ARM = "M_TYPED_COLLECTIVE_STATE"
CMP_ARM = "B8_CAPACITY_MATCHED_BEST"          # V2's registered comparator
GREEDY_ARM = "B6_GREEDY_SUBSET_UNTYPED"
L1_ARM = "B7_L1_PATH_UNTYPED"
UNIT_SIGN_ARM = "B4X_FITTED_UNTYPED_UNIT_SIGN_LEARNED_CONTROL"
EQUAL_ARM = "B4X_INFORMATION_MATCHED_UNTYPED_EQUAL_WEIGHT"
CONTROL_ARMS = ("C_ALWAYS_RISE", "C_ALWAYS_FLAT", "C_ALWAYS_FALL")

# The capability half is the contested question.  The ACTIVITY half is read from the
# activity channels by the same call for every arm in V1, so it is equal BY
# CONSTRUCTION and is not evidence (V1 provenance receipt section 3).  V2 therefore
# does not report an activity half at all rather than publishing a number no arm
# could have lost.  This is a deliberate narrowing and is registered as one.


def canonical_json(o) -> str:
    return json.dumps(o, indent=2, sort_keys=True, default=str)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def binom_upper_tail(k: int, n: int, p) -> float:
    """P(X >= k) for Binomial(n, p), EXACT in rationals.

    The float form overflows at n = 1400 and would return inf, making any
    `p > alpha` hard gate incapable of failing.  V1 hit this and solved it the same
    way; the fix is carried here rather than rediscovered.
    """
    if n == 0:
        return 1.0
    k = max(0, min(k, n))
    q = Fraction(p).limit_denominator(10 ** 6)
    one_q = 1 - q
    tail = sum((Fraction(comb(n, i)) * q ** i * one_q ** (n - i) for i in range(k, n + 1)),
               Fraction(0))
    return min(1.0, max(0.0, tail.numerator / tail.denominator))


# ---- arms ----------------------------------------------------------------------

def _const(direction: str):
    return lambda delta: direction


def arm_table(frozen: dict) -> dict:
    """arm name -> callable(delta dict) -> direction.

    Every non-control arm is the SAME function of the same 16 channel
    half-differences.  Arms differ only in their weight vector, which is the whole
    point: capacity, not information, is the variable under study.
    """
    arms = {
        M_ARM: lambda d, w={c: TYPED_SIGNS.get(c, 0) for c in CHANNELS}:
            F.direction_from_weights(d, w),
        CMP_ARM: lambda d, w=frozen["B8_CAPACITY_MATCHED_BEST"]["weights"]:
            F.direction_from_weights(d, w),
        GREEDY_ARM: lambda d, w=frozen["B6_GREEDY_SUBSET_UNTYPED"]["weights"]:
            F.direction_from_weights(d, w),
        L1_ARM: lambda d, w=frozen["B7_L1_PATH_UNTYPED"]["weights"]:
            F.direction_from_weights(d, w),
        UNIT_SIGN_ARM: lambda d, w=frozen["B4X_FITTED_UNTYPED_UNIT_SIGN_LEARNED_CONTROL"]["weights"]:
            F.direction_from_weights(d, w),
        EQUAL_ARM: lambda d, w={c: 1 for c in CHANNELS}:
            F.direction_from_weights(d, w),
    }
    arms["C_ALWAYS_RISE"] = _const(RISE)
    arms["C_ALWAYS_FLAT"] = _const(FLAT)
    arms["C_ALWAYS_FALL"] = _const(FALL)
    return arms


# ---- fitting -------------------------------------------------------------------

def fit_on_development() -> dict:
    """Fit every learned arm on the public development split.  Deterministic.

    The protected seed governs INSTANCE GENERATION ONLY.  It plays no part here and
    could not: this function reads the public development seed, and every fitter is
    RNG-free.  Stated because a seed that does nothing, unstated, is a defect.
    """
    insts = generate_split("dev", DEV_SEED, DEV_PER_CELL)
    deltas = [F.half_difference(i.window, CHANNELS) for i in insts]
    truths = [oracle(i.window).capability for i in insts]
    sel = F.select_capacity_matched(deltas, truths, CHANNELS)
    unit = fit_signs(insts, CHANNELS)          # V1's own univariate screening fitter
    sel[UNIT_SIGN_ARM] = {
        "weights": {c: int(unit.get(c, 0)) for c in CHANNELS},
        "dev_capability_correct": F.accuracy(deltas, truths, unit),
        "note": ("V1's comparator, refitted here by V1's own fit_signs on V2's "
                 "development split.  Learned and information-matched, but its class "
                 "is {-1,0,+1} with 0 reachable only by an exact per-channel tie, so "
                 "in practice it cannot drop a channel.  This is V2's CAPACITY "
                 "control: it holds 'learned' fixed and varies only capacity."),
    }
    sel["dev_seed"] = DEV_SEED
    sel["dev_per_cell"] = DEV_PER_CELL
    return sel


def frozen_fit() -> dict:
    d = json.loads(DESIGN_JSON.read_text())
    out = {}
    for arm, rec in d["comparator"]["frozen_fitted_weights"].items():
        out[arm] = {"weights": {k: float(v) for k, v in rec["weights"].items()},
                    "dev_capability_correct": rec.get("dev_capability_correct")}
    return out


def refit_reproduces() -> tuple[bool, dict]:
    """The frozen vectors must still be what the fitters produce from the public
    development split.  Drift is refused, never absorbed."""
    committed = frozen_fit()
    live = fit_on_development()
    drift = {}
    for arm in committed:
        cw = {k: float(v) for k, v in committed[arm]["weights"].items()}
        lw = {k: float(v) for k, v in live[arm]["weights"].items()}
        if any(abs(cw.get(k, 0.0) - lw.get(k, 0.0)) > 1e-9 for k in set(cw) | set(lw)):
            drift[arm] = {"committed": cw, "refit": lw}
    return (not drift), drift


# ---- running -------------------------------------------------------------------

def run_instances(instances, label: str, frozen: dict) -> tuple[dict, dict]:
    arms = arm_table(frozen)
    rows, custody = [], []
    for inst in instances:
        w = inst.window
        delta = F.half_difference(w, CHANNELS)
        truth = oracle(w).capability
        ok, why = planter_agrees(w, inst.stratum)
        custody.append({"instance_id": inst.instance_id, "stratum": inst.stratum,
                        "scale": inst.scale, "planter_agrees": ok,
                        "planter_reason": why,
                        "decidable_from_fit_window": decidable_from_fit_window(w),
                        "expected_capability": truth})
        rows.append({"instance_id": inst.instance_id, "stratum": inst.stratum,
                     "scale": inst.scale, "expected_capability": truth,
                     "arms": {name: fn(delta) for name, fn in arms.items()}})
    res = {"schema_version": SCHEMA_RESULTS, "label": label,
           "n_instances": len(rows), "arms": sorted(arms),
           "frozen_weights": {a: frozen[a]["weights"] for a in frozen if "weights" in frozen[a]},
           "instances": rows}
    cus = {"schema_version": SCHEMA_RESULTS + ".custody", "label": label,
           "instances": custody}
    return res, cus


# ---- scoring -------------------------------------------------------------------

def score(res: dict) -> dict:
    rows = res["instances"]
    arms = res["arms"]
    n = len(rows)
    per_arm, vec = {}, {}
    for a in arms:
        v = [r["arms"][a] == r["expected_capability"] for r in rows]
        vec[a] = v
        per_arm[a] = {"capability_correct": sum(v), "n_evaluated": n,
                      "capability_rate": (sum(v) / n) if n else 0.0}
    cells = sorted({(r["stratum"], r["scale"]) for r in rows})
    by_cell = {}
    for st, sc in cells:
        sub = [i for i, r in enumerate(rows) if r["stratum"] == st and r["scale"] == sc]
        by_cell[f"{st}|{sc}"] = {a: sum(1 for i in sub if vec[a][i]) for a in arms}
        by_cell[f"{st}|{sc}"]["_n"] = len(sub)
    return {"per_arm": per_arm, "vec": vec, "cells": cells, "by_cell": by_cell,
            "strata": [r["stratum"] for r in rows], "scales": [r["scale"] for r in rows],
            "n": n}


def paired(x: list[bool], y: list[bool]) -> dict:
    b = sum(1 for i, j in zip(x, y) if i and not j)
    c = sum(1 for i, j in zip(x, y) if j and not i)
    return {"n": len(x), "x_only": b, "y_only": c, "discordant": b + c,
            "exact_p_two_sided": exact_binomial_two_sided(b, c)}


def cell_compare(sc: dict, x: str, y: str) -> dict:
    xw = yw = tie = 0
    for key, rec in sc["by_cell"].items():
        if rec[x] > rec[y]:
            xw += 1
        elif rec[y] > rec[x]:
            yw += 1
        else:
            tie += 1
    return {"n_cells": len(sc["by_cell"]), "x_wins": xw, "y_wins": yw, "ties": tie}


# ---- gates ---------------------------------------------------------------------
# Every gate is a POSITIVE test carrying its own n_evaluated.  No terminal is the
# negation of another gate.  n_evaluated == 0 reports CANNOT_CHECK, never a pass.

def gates(sc: dict, res: dict, cus: dict, selftest_ok: bool | None,
          selftest_meta: dict | None) -> dict:
    g: dict[str, dict] = {}
    n = sc["n"]
    pa = sc["per_arm"]
    vec = sc["vec"]
    meta = selftest_meta or {}

    g["G0a_KNOWN_ANSWER"] = {
        "pass": selftest_ok,
        "n_evaluated": int(meta.get("n_checks", 0)) if selftest_ok is not None else 0,
        "status": "EVALUATED" if selftest_ok is not None else "CANNOT_CHECK_NO_SELFTEST_REPORT",
        "rule": "the fitter and generator known-answer fixtures in the selftest report "
                "all reproduce; the denominator is READ from that report, never recomputed"}

    pl = sum(1 for c in cus["instances"] if c["planter_agrees"])
    dec = sum(1 for c in cus["instances"] if c["decidable_from_fit_window"])
    g["G0b_GENERATOR_VALIDITY"] = {
        "pass": (pl == n and dec == n) if n else None, "n_evaluated": n,
        "planter_agree": {"ok": pl, "n": n},
        "decidable_from_fit_window": {"ok": dec, "n": n},
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "the planter's declared capability effect equals the full-structure "
                "recomputation on every instance, and every holdout direction is "
                "already carried by its fit window"}

    # G0c -- the controls must NOT clear the bar the comparator is judged against.
    worst = max(pa[a]["capability_rate"] for a in CONTROL_ARMS)
    p_ctrl = binom_upper_tail(max(pa[a]["capability_correct"] for a in CONTROL_ARMS),
                              n, Fraction(1, 3)) if n else 1.0
    g["G0c_NULL_CALIBRATION"] = {
        "pass": (worst < 0.60) if n else None, "n_evaluated": n,
        "best_control_rate": worst, "controls": {a: pa[a]["capability_rate"] for a in CONTROL_ARMS},
        "exact_upper_tail_vs_uniform_third": p_ctrl,
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "no constant arm reaches 0.60 capability accuracy; a suite an always-X "
                "arm can win is not measuring a decision rule"}

    # G0d -- M is exact BY CONSTRUCTION on this generator (V1 design 1.3).  This is a
    # VALIDITY check, not a contrast: see the reachability audit.  If M is not exact
    # the generator has drifted and no arm verdict may be read.
    g["G0d_M_EXACT_BY_CONSTRUCTION"] = {
        "pass": (pa[M_ARM]["capability_correct"] == n) if n else None,
        "n_evaluated": n, "m_correct": pa[M_ARM]["capability_correct"],
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "M reproduces the oracle capability direction on every instance, as "
                "V1 design 1.3 declares.  A failure here is generator drift, not a result"}

    # G0e -- capacity matching actually BIT.  A comparator whose class contains zero
    # but whose fitted vector zeroes nothing is not capacity-matched in fact, and the
    # study would be measuring nothing.  Positive test with its denominator.
    w = res["frozen_weights"][CMP_ARM]
    zeros = sum(1 for v in w.values() if not float(v))
    g["G0e_CAPACITY_MATCHING_BIT"] = {
        "pass": zeros > 0, "n_evaluated": len(w), "n_channels_zeroed": zeros,
        "n_channels": len(w),
        "unit_sign_control_zeroed": sum(
            1 for v in res["frozen_weights"][UNIT_SIGN_ARM].values() if not float(v)),
        "rule": "the registered comparator's fitted vector sets at least one channel "
                "weight to exactly zero; otherwise the class containing zero was "
                "never exercised and the contrast with V1 is empty"}

    # G1a -- the live contrast.  POSITIVE test that M is ahead of the capacity-matched
    # learned comparator.
    cc = cell_compare(sc, M_ARM, CMP_ARM)
    pr = paired(vec[M_ARM], vec[CMP_ARM])
    g["G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT"] = {
        "pass": (pa[M_ARM]["capability_rate"] > pa[CMP_ARM]["capability_rate"]
                 and cc["x_wins"] > 0 and cc["y_wins"] == 0) if n else None,
        "n_evaluated": n, "n_cells": cc["n_cells"], "cells": cc, "paired": pr,
        "m_rate": pa[M_ARM]["capability_rate"], "parent_rate": pa[CMP_ARM]["capability_rate"],
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "M's capability accuracy exceeds the LEARNED capacity-matched untyped "
                "comparator's, and M wins cells while losing none"}

    # G1b -- the tie, as its own POSITIVE test rather than the negation of G1a.
    g["G1b_TIE_AT_MATCHED_CAPACITY"] = {
        "pass": (pa[M_ARM]["capability_correct"] == pa[CMP_ARM]["capability_correct"]
                 and pr["discordant"] == 0) if n else None,
        "n_evaluated": n, "discordant_pairs": pr["discordant"],
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "M and the capacity-matched comparator agree on every instance: equal "
                "totals AND zero discordant pairs, so the tie is verdict-level and not "
                "two different arms happening to score the same"}

    # G2 -- V2's own contribution: capacity, holding LEARNEDNESS fixed, is what V1's
    # separation measured.  Both arms here are fitted from the same development split
    # by a published-standard procedure; only the weight class differs.
    cc2 = cell_compare(sc, CMP_ARM, UNIT_SIGN_ARM)
    pr2 = paired(vec[CMP_ARM], vec[UNIT_SIGN_ARM])
    g["G2_CAPACITY_IS_THE_SEPARATOR"] = {
        "pass": (pa[CMP_ARM]["capability_rate"] > pa[UNIT_SIGN_ARM]["capability_rate"]
                 and cc2["y_wins"] == 0) if n else None,
        "n_evaluated": n, "n_cells": cc2["n_cells"], "cells": cc2, "paired": pr2,
        "capacity_matched_rate": pa[CMP_ARM]["capability_rate"],
        "unit_sign_rate": pa[UNIT_SIGN_ARM]["capability_rate"],
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "the capacity-matched LEARNED comparator is ahead of the unit-sign "
                "LEARNED comparator (V1's own) and loses no cell to it; both are "
                "fitted on the same split, so only the weight class differs"}

    # G6 -- the verdict must hold separately at both units of analysis.
    per_scale = {}
    for scl in SCALES:
        idx = [i for i, s in enumerate(sc["scales"]) if s == scl]
        if not idx:
            per_scale[scl] = {"status": "CANNOT_CHECK_NO_INSTANCES"}
            continue
        m = sum(1 for i in idx if vec[M_ARM][i])
        p = sum(1 for i in idx if vec[CMP_ARM][i])
        per_scale[scl] = {"n": len(idx), "m": m, "parent": p, "m_minus_parent": m - p}
    signs = {v["m_minus_parent"] > 0 for v in per_scale.values() if "m_minus_parent" in v}
    g["G6_CROSS_SCALE_CONSISTENCY"] = {
        "pass": (len(signs) == 1) if len(per_scale) == len(SCALES) else None,
        "n_evaluated": n, "per_scale": per_scale,
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "the sign of (M - comparator) is the same at both units of analysis; a "
                "result that holds at only one scale is not a result here"}

    # G8 -- within-cell verdict constancy.  Instances of a cell are structural
    # replicates, so a arm that flips verdict inside a cell is reading instance noise.
    flips = 0
    checked = 0
    for key, rec in sc["by_cell"].items():
        checked += 1
        for a in (M_ARM, CMP_ARM, UNIT_SIGN_ARM):
            if 0 < rec[a] < rec["_n"]:
                flips += 1
    g["G8_VERDICT_CONSTANCY_WITHIN_CELL"] = {
        "pass": (flips == 0) if checked else None, "n_evaluated": checked,
        "n_cells": checked, "flips": flips,
        "status": "EVALUATED" if checked else "CANNOT_CHECK_NO_CELLS",
        "rule": "for M, the comparator and the unit-sign control, every instance of a "
                "cell receives the same verdict"}

    g["COVERAGE_LEDGER"] = {
        "all_registered_cells_exercised": len(sc["by_cell"]) == len(CELLS),
        "n_cells_exercised": len(sc["by_cell"]), "n_cells_registered": len(CELLS),
        "never_exercised": sorted(f"{s}|{sc_}" for s, sc_ in CELLS
                                  if f"{s}|{sc_}" not in sc["by_cell"])}
    g["ROUTE"] = route(g)
    return g


def route(g: dict) -> dict:
    hard = ("G0a_KNOWN_ANSWER", "G0b_GENERATOR_VALIDITY", "G0c_NULL_CALIBRATION",
            "G0d_M_EXACT_BY_CONSTRUCTION", "G0e_CAPACITY_MATCHING_BIT",
            "G8_VERDICT_CONSTANCY_WITHIN_CELL")
    for h in hard:
        if g[h].get("pass") is not True:
            return {"route": "CANNOT_CHECK", "terminal": "NONE",
                    "reason": f"hard gate {h} did not pass -- lane defect; repair, "
                              "re-freeze, no arm verdict"}
    if not g["COVERAGE_LEDGER"]["all_registered_cells_exercised"]:
        return {"route": "CANNOT_CHECK", "terminal": "NONE",
                "reason": "not every registered cell was exercised"}
    if g["G1b_TIE_AT_MATCHED_CAPACITY"]["pass"]:
        return {"route": "PARENT_SUFFICIENT",
                "terminal": "TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY",
                "reason": "a LEARNED untyped comparator whose weight class contains zero "
                          "reproduces M's capability verdict on every instance. The "
                          "separation V1 measured is attributable to the comparator's "
                          "capacity, not to typing. ME-X6 contracts to an interpretive "
                          "framework -- the protocol's own contraction rule, and a "
                          "legitimate result, not a failure"}
    if g["G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT"]["pass"]:
        if not g["G6_CROSS_SCALE_CONSISTENCY"]["pass"]:
            return {"route": "PARENT_SUFFICIENT", "terminal": "NO_CROSS_SCALE_TRANSFER",
                    "reason": "M's lead does not hold at the second unit of analysis"}
        return {"route": "TYPED_STATE_SEPARATES_FROM_A_LEARNED_CAPACITY_MATCHED_PARENT",
                "terminal": "LEARNED_CAPACITY_MATCHED_UNTYPED_AGGREGATE_DOES_NOT_RECOVER_"
                            "THE_CAPABILITY_DIRECTION",
                "reason": "M is ahead of an untyped comparator that was allowed to drop "
                          "channels and learned its own vector from the development "
                          "split, at matched information and matched capacity"}
    return {"route": "CANNOT_CHECK", "terminal": "NONE",
            "reason": "neither the tie nor the M-ahead clause holds as registered: M and "
                      "the comparator differ in total but not consistently by cell, so "
                      "no representational reading is supported"}


# ---- selftest, including the pre-run reachability audit -------------------------

def reachability_audit() -> dict:
    """Can every registered clause be SATISFIED at all, and can it FAIL at all?

    Run before the protected split exists.  Anything unreachable is repaired or
    relabelled here, as a pre-outcome correction, never after an outcome.
    """
    insts = generate_split("dev", DEV_SEED, DEV_PER_CELL)
    deltas = [F.half_difference(i.window, CHANNELS) for i in insts]
    truths = [oracle(i.window).capability for i in insts]
    n = len(truths)
    mw = {c: TYPED_SIGNS.get(c, 0) for c in CHANNELS}
    hand_zeroed = dict(fit_signs(insts, CHANNELS))
    for c in ("preprints", "journal_papers", "authors", "citations",
              "semantic_novelty", "disruption"):
        hand_zeroed[c] = 0
    findings = {
        "class_contains_a_FAILING_member": {
            "witness": "all-+1 weights",
            "correct": F.accuracy(deltas, truths, {c: 1 for c in CHANNELS}), "n": n},
        "class_contains_an_EXACT_member": {
            "witness": "V1 provenance receipt section 4's hand-set zeroing",
            "correct": F.accuracy(deltas, truths, hand_zeroed), "n": n},
        "M_is_itself_a_member_of_the_untyped_class": {
            "witness": "M's own weight dict loaded into the untyped decision rule",
            "correct": F.accuracy(deltas, truths, mw), "n": n},
        "G0d_is_a_validity_check_not_a_contrast": {
            "statement": "M is exact by construction on this generator (V1 design 1.3), "
                         "so a clause of the form 'the comparator is AHEAD of M' is "
                         "UNREACHABLE here and is deliberately NOT registered. The two "
                         "live outcomes are G1b (tie) and G1a (M ahead); a comparator "
                         "win is impossible against a ceiling and claiming to test for "
                         "it would be a clause that could not fire."},
        "the_activity_half_is_not_reported": {
            "statement": "V1 computes the activity direction from the same channels by "
                         "the same call for every arm, so it is equal BY CONSTRUCTION "
                         "and is not evidence. V2 scores the capability half only "
                         "rather than publishing a 100% agreement no arm could lose."},
        "the_protected_seed_does_nothing_to_the_fit": {
            "statement": "The comparator fit is a deterministic, RNG-free function of "
                         "the PUBLIC development split, frozen before the protected "
                         "seed is revealed. The protected seed governs instance "
                         "generation only. Recorded so that a seed with no effect on a "
                         "parameter is disclosed rather than implied."},
    }
    return findings


def greedy_can_fail_fixture() -> dict:
    """A dataset on which forward selection PROVABLY misses a member of its own class.

    The labels are generated by the hidden rule `{f2: +1, f3: -2}` -- a vector the
    greedy weight class contains exactly.  Greedy's first round takes `f3: -1`,
    which scores 5/6 on its own, and from there no single addition reaches 6/6, so
    it stops one short of a rule it could have represented.  Exhaustive enumeration
    over the same class finds the 6/6 vector.

    This is why the study is not a tautology.  A comparator fitted by exhaustive
    search over a class that contains M's own vector could not fail to recover M's
    rule, and a tie would be an identity rather than a measurement.  Both registered
    fitters are heuristics -- forward selection is greedy and non-backtracking,
    the lasso path is a convex relaxation over a fixed grid -- so `B8` reaching M's
    verdict is a finding and not a definition.
    """
    chans = ("f1", "f2", "f3")
    deltas = [
        {"f1": -1, "f2": -2, "f3": 1},
        {"f1": 3, "f2": -3, "f3": -3},
        {"f1": 2, "f2": -3, "f3": -1},
        {"f1": 2, "f2": -3, "f3": 2},
        {"f1": -2, "f2": -3, "f3": -3},
        {"f1": 1, "f2": 1, "f3": -3},
    ]
    hidden = {"f1": 0, "f2": 1, "f3": -2}
    truths = [F.direction_from_weights(d, hidden) for d in deltas]
    w, trace = F.fit_greedy_subset(deltas, truths, chans)
    got = F.accuracy(deltas, truths, w)
    exhaustive = 0
    best_w = None
    for a in (0, 1, -1, -2):
        for b in (0, 1, -1, -2):
            for c in (0, 1, -1, -2):
                cand = {"f1": a, "f2": b, "f3": c}
                acc = F.accuracy(deltas, truths, cand)
                if acc > exhaustive:
                    exhaustive, best_w = acc, cand
    return {"greedy_weights": w, "greedy_correct": got,
            "hidden_rule": hidden, "hidden_rule_correct": F.accuracy(deltas, truths, hidden),
            "exhaustive_best_correct": exhaustive, "exhaustive_best_weights": best_w,
            "n": len(deltas), "greedy_is_suboptimal": got < exhaustive,
            "rounds": len(trace) - 1}


def l1_can_fail_fixture() -> dict:
    """The same demonstration for the other registered fitter.

    Labels come from the hidden rule `{f2: +1, f3: -2}`, which the lasso's own class
    (real weights) contains.  Across the frozen lambda grid in both registered
    scalings, the best-scoring solution reaches 6/8 while the hidden rule reaches
    8/8 and even the greedy heuristic reaches 7/8.  A convex relaxation over a fixed
    grid is a heuristic too, and this records that plainly.
    """
    chans = ("f1", "f2", "f3")
    deltas = [
        {"f1": 1, "f2": 2, "f3": 1}, {"f1": 1, "f2": 2, "f3": 2},
        {"f1": -2, "f2": -2, "f3": 2}, {"f1": 1, "f2": 3, "f3": 2},
        {"f1": -2, "f2": -3, "f3": 1}, {"f1": -1, "f2": -2, "f3": -3},
        {"f1": 2, "f2": 3, "f3": 3}, {"f1": -3, "f2": 2, "f3": 1},
    ]
    hidden = {"f1": 0, "f2": 1, "f3": -2}
    truths = [F.direction_from_weights(d, hidden) for d in deltas]
    w, _ = F.fit_l1_path(deltas, truths, chans)
    got = F.accuracy(deltas, truths, w)
    return {"l1_weights": {k: round(v, 6) for k, v in w.items()}, "l1_correct": got,
            "hidden_rule": hidden,
            "hidden_rule_correct": F.accuracy(deltas, truths, hidden),
            "n": len(deltas), "l1_is_suboptimal": got < F.accuracy(deltas, truths, hidden)}


def stage_selftest(out_dir: Path) -> int:
    checks: list[dict] = []

    # 1. soft-threshold known answers
    for z, gmm, want in ((0.5, 0.2, 0.3), (-0.5, 0.2, -0.3), (0.1, 0.2, 0.0)):
        checks.append({"check": f"soft({z},{gmm})", "pass": abs(F._soft(z, gmm) - want) < 1e-12})

    # 2. lasso at a huge lambda is exactly the zero vector; at lambda -> 0 it fits
    x = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    y = [1.0, -1.0, 0.0]
    checks.append({"check": "lasso_large_lambda_is_zero",
                   "pass": F._lasso(x, y, 1e6) == [0.0, 0.0]})
    small = F._lasso(x, y, 1e-9)
    checks.append({"check": "lasso_small_lambda_recovers_sign",
                   "pass": small[0] > 0 and small[1] < 0})

    # 3. the direction rule
    checks.append({"check": "direction_rule",
                   "pass": (F.direction_from_weights({"a": 3}, {"a": 1}) == RISE
                            and F.direction_from_weights({"a": 3}, {"a": -1}) == FALL
                            and F.direction_from_weights({"a": 3}, {"a": 0}) == FLAT)})

    # 4. greedy is a heuristic that CAN fail
    gf = greedy_can_fail_fixture()
    checks.append({"check": "greedy_forward_selection_can_fail", "pass": gf["greedy_is_suboptimal"],
                   "detail": gf})
    lf = l1_can_fail_fixture()
    checks.append({"check": "l1_path_can_fail", "pass": lf["l1_is_suboptimal"], "detail": lf})

    # 5. generator validity on the development split
    insts = generate_split("dev", DEV_SEED, DEV_PER_CELL)
    ok = all(planter_agrees(i.window, i.stratum)[0] for i in insts)
    dec = all(decidable_from_fit_window(i.window) for i in insts)
    checks.append({"check": "planter_agrees_on_every_dev_instance", "pass": ok,
                   "n": len(insts)})
    checks.append({"check": "decidable_from_fit_window_on_every_dev_instance", "pass": dec,
                   "n": len(insts)})

    # 6. every registered stratum reaches a cell
    checks.append({"check": "all_registered_cells_generated",
                   "pass": len({(i.stratum, i.scale) for i in insts}) == len(CELLS),
                   "n": len(CELLS)})

    # 7. the exact binomial tail does not overflow at protected scale
    tail = binom_upper_tail(900, PROTECTED_PER_CELL * len(CELLS), Fraction(1, 3))
    checks.append({"check": "exact_tail_finite_at_protected_scale",
                   "pass": 0.0 <= tail <= 1.0, "value": tail})

    passed = all(c["pass"] for c in checks)
    rep = {"schema_version": SCHEMA_RESULTS + ".selftest", "passed": passed,
           "n_checks": len(checks), "checks": checks,
           "reachability_audit": reachability_audit()}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X6_V2_SELFTEST_REPORT.json").write_text(canonical_json(rep))
    print(f"selftest: {sum(1 for c in checks if c['pass'])}/{len(checks)} checks pass")
    return 0 if passed else 1


# ---- stages --------------------------------------------------------------------

def _run_split(label: str, prefix: str, seed: str, per_cell: int, out_dir: Path) -> int:
    if not DESIGN_JSON.exists():
        print(f"REFUSED: frozen design absent ({DESIGN_JSON.name})", file=sys.stderr)
        return 5
    ok, drift = refit_reproduces()
    if not ok:
        print(f"REFUSED: the frozen comparator weights no longer reproduce: {drift}",
              file=sys.stderr)
        return 5
    frozen = frozen_fit()
    insts = generate_split(prefix, seed, per_cell)
    res, cus = run_instances(insts, label, frozen)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X6_V2_{label}_RESULTS_V1.json"
    cp = out_dir / f"ME_X6_V2_{label}_EXPECTED_CUSTODY_V1.json"
    rp.write_text(canonical_json(res))
    cp.write_text(canonical_json(cus))
    print(f"{label}: {len(insts)} instances, results sha256 {sha256_file(rp)[:16]}..., "
          f"custody sha256 {sha256_file(cp)[:16]}...")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_cell: int) -> int:
    if per_cell * len(CELLS) > 56:
        print("the development split is capped at 56 instances", file=sys.stderr)
        return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_cell, out_dir)


def stage_protected(out_dir: Path, per_cell: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent -- protected run not authorized",
              file=sys.stderr)
        return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization file unreadable: {exc}", file=sys.stderr)
        return 3
    token = str(auth.get("human_written_token", "")).strip()
    if auth.get("human_written") is not True or len(token) < 16:
        print("REFUSED: authorization requires human_written=true and a "
              "human_written_token (>= 16 chars)", file=sys.stderr)
        return 3
    if auth.get("acknowledged_design_sha256") != sha256_file(DESIGN_JSON):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON",
              file=sys.stderr)
        return 3
    if not seed_file.exists():
        print(f"REFUSED: custody seed file absent ({seed_file})", file=sys.stderr)
        return 4
    seed = seed_file.read_bytes().strip()
    commit = json.loads(DESIGN_JSON.read_text())["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed).hexdigest() != commit:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr)
        return 4
    return _run_split("PROTECTED", "protected", seed.decode(), per_cell, out_dir)


def stage_analyze(rp: Path, cp: Path, out_dir: Path, label: str | None = None,
                  selftest_report: Path | None = None) -> int:
    res = json.loads(rp.read_text())
    cus = json.loads(cp.read_text())
    label = label or res.get("label", "UNKNOWN")
    sp = selftest_report or (out_dir / "ME_X6_V2_SELFTEST_REPORT.json")
    selftest_ok, meta = None, None
    if sp.exists():
        rep = json.loads(sp.read_text())
        selftest_ok = bool(rep.get("passed"))
        meta = {"n_checks": rep.get("n_checks", 0)}
    sc = score(res)
    gt = gates(sc, res, cus, selftest_ok, meta)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label,
                "results_sha256": sha256_file(rp), "custody_sha256": sha256_file(cp),
                "n_instances": sc["n"], "score": {"per_arm": sc["per_arm"]},
                "by_cell": sc["by_cell"], "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X6_V2_{label}_ANALYSIS_V1.json").write_text(canonical_json(analysis))
    (out_dir / f"ME_X6_V2_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    r = gt["ROUTE"]
    print(f"{label} route: {r['route']}; terminal: {r['terminal']}")
    print(f"  M {sc['per_arm'][M_ARM]['capability_rate']:.4f}  "
          f"capacity-matched {sc['per_arm'][CMP_ARM]['capability_rate']:.4f}  "
          f"unit-sign control {sc['per_arm'][UNIT_SIGN_ARM]['capability_rate']:.4f}")
    return 0


def render_md(a: dict) -> str:
    g = a["gates"]
    pa = a["score"]["per_arm"]
    L = [f"# ME-X6 V2 {a['label']} analysis", "",
         f"- instances: {a['n_instances']}",
         f"- route: `{g['ROUTE']['route']}` — terminal `{g['ROUTE']['terminal']}`",
         f"- reason: {g['ROUTE']['reason']}", "",
         "Only the CAPABILITY half is scored. V1 computes the activity direction from "
         "the same channels by the same call for every arm, so an activity agreement "
         "is equal by construction and is not evidence.", "",
         "## Gates", "", "| gate | pass | n_evaluated |", "|---|---|---|"]
    for k, v in g.items():
        if k in ("ROUTE", "COVERAGE_LEDGER"):
            continue
        L.append(f"| `{k}` | {v.get('pass')} | {v.get('n_evaluated')} |")
    L += ["", "## Arms (capability)", "", "| arm | correct | rate | n |", "|---|---|---|---|"]
    for k, v in sorted(pa.items(), key=lambda x: -x[1]["capability_rate"]):
        L.append(f"| `{k}` | {v['capability_correct']} | {v['capability_rate']:.4f} | "
                 f"{v['n_evaluated']} |")
    cl = g["COVERAGE_LEDGER"]
    L += ["", "## Coverage", "",
          f"- cells exercised: {cl['n_cells_exercised']} / {cl['n_cells_registered']}",
          f"- never exercised: {cl['never_exercised'] or 'none'}", ""]
    return "\n".join(L)


def stage_fit(out_dir: Path) -> int:
    sel = fit_on_development()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X6_V2_DEVELOPMENT_FIT_V1.json").write_text(canonical_json(sel))
    for arm in (GREEDY_ARM, L1_ARM, UNIT_SIGN_ARM):
        w = sel[arm]["weights"]
        print(f"{arm}: dev {sel[arm]['dev_capability_correct']}/{sel['n_dev']}, "
              f"zeros {sum(1 for v in w.values() if not v)}/{len(w)}")
        print(f"   {({k: (round(v, 6) if isinstance(v, float) else v) for k, v in w.items() if v})}")
    print(f"{CMP_ARM}: selected {sel[CMP_ARM]['selected_fitter']}, "
          f"dev {sel[CMP_ARM]['dev_capability_correct']}/{sel['n_dev']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "fit", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-cell", type=int, default=None)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "fit":
        return stage_fit(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_cell or DEV_PER_CELL)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_cell or PROTECTED_PER_CELL, a.seed_file)
    if not a.results or not a.custody:
        print("analyze needs --results and --custody", file=sys.stderr)
        return 2
    return stage_analyze(a.results, a.custody, a.out, None, a.selftest_report)


if __name__ == "__main__":
    sys.exit(main())
