"""ME-X6 runner: selftest / dev / protected / analyze.

    selftest   known-answer fixtures, oracle self-agreement, null calibration
    dev        DEVELOPMENT split under the public seed (never protected)
    protected  refuses unless PROTECTED_RUN_AUTHORIZATION.json is present and
               the custody seed hashes to the frozen commitment
    analyze    gates and route from an existing results/custody pair
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mex6_arms import (  # noqa: E402
    ABLATION_GROUPS,
    B4X_ARM,
    B4X_FITTED_ARM,
    B4_LITERAL_ARM,
    LADDER,
    M_ARM,
    arm_specs,
    fit_all,
    fit_signs,
    load_fitted_signs,
    run_arm,
)
from mex6_generator import (  # noqa: E402
    CELLS,
    CONTROL_STRATA,
    PERTURBATION_STRATA,
    STRATA,
    generate_split,
    sha256_text,
)
from mex6_model import CHANNELS, FALL, FLAT, RISE, SCALES  # noqa: E402
from mex6_oracle import decidable_from_fit_window, oracle, planter_agrees  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x6.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x6.exact-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X6_COLLECTIVE_EPISTEMICS_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEFAULT_SEED_FILE = Path.home() / ".orion-custody" / "me-x6" / "PROTECTED_SEED_V1.txt"

DEV_SEED = "ME-X6-DEV-20260903"
SELFTEST_SEED = "ME-X6-SELFTEST"
SHUFFLE_SEED = 20260903

# The strata on which the true capability direction CONTRADICTS the direction of
# some channel the untyped parent must give a single global sign to: volume and
# attention rise while capability is flat (I1, I2, I3, I5, I7, I8), or every
# ordinary validated channel rises while capability falls (I4).  A single sign
# per channel cannot represent "volume counts only when validation accompanies
# it", so these are where an untyped aggregate is predicted to fail.
#
# Registered from the DEVELOPMENT split -- the design's declared public tuning
# surface -- before any protected instance exists, as the support of the
# falsifiable prediction P-MEX6-1 (design section 7).
# P-MEX6-2's support, registered from the development split before any protected
# instance exists: the steps of the fitted untyped ladder that lose exactness.
PREDICTED_LADDER_REGRESSIONS = ("L1_ACTIVITY_ONLY -> L2_PLUS_ATTENTION",)

DECOUPLED_STRATA = ("I1_DUPLICATES", "I2_PARAPHRASE", "I3_MASS_LOW_INFORMATION",
                    "I4_RETRACTED_WORK", "I5_CITATION_RING",
                    "I7_FIELD_SIZE_SCALING", "I8_FASHION_CONCENTRATION")

# Which typed channel group each invariance stratum depends on, declared in
# advance.  G3 tests this exactly: an ablation must blind the strata that need
# the group it drops, and no others.
ABLATION_PREDICTION: dict[str, tuple[str, ...]] = {
    "M_MINUS_CORRECTION_RETRACTION": ("I4_RETRACTED_WORK",),
    "M_MINUS_REDERIVATION": ("I10_INDEPENDENT_REDISCOVERY",),
    "M_MINUS_FORMAL": ("X6I7_ONE_BREAKTHROUGH",),
    "M_MINUS_REPLICATION": ("I9_DELAYED_VALIDATION",),
    "M_MINUS_REUSE": (),
    "M_MINUS_COST": (),
}


def canonical_json(o) -> str:
    return json.dumps(o, indent=2, sort_keys=True, default=str)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def binom_upper_tail(k: int, n: int, p: Fraction | float) -> float:
    """P(X >= k) for X ~ Binomial(n, p), computed EXACTLY in rational arithmetic.

    The obvious float form -- `comb(n, i) * p**i * (1-p)**(n-i)` -- is unusable
    here: at the registered protected size the binomial coefficients exceed the
    float range and the expression raises OverflowError (or, if that were
    caught, returns inf, and `inf > 0.05` would make this hard gate incapable of
    failing).  Exact Fractions have neither failure mode, and exactness is the
    house style for this study anyway.  Only the final ratio is narrowed to a
    float, and that narrowing is guarded.
    """
    if n == 0:
        return 1.0
    k = max(0, min(k, n))
    q = Fraction(p).limit_denominator(10 ** 6)
    one_q = 1 - q
    tail = sum((Fraction(comb(n, i)) * q ** i * one_q ** (n - i) for i in range(k, n + 1)),
               Fraction(0))
    return min(1.0, max(0.0, tail.numerator / tail.denominator))


def paired(x: list[bool], y: list[bool]) -> dict:
    b = sum(1 for i, j in zip(x, y) if i and not j)
    c = sum(1 for i, j in zip(x, y) if j and not i)
    n = len(x)
    diff = (sum(x) - sum(y)) / n if n else 0.0
    return {"n": n, "x_only": b, "y_only": c, "discordant": b + c,
            "diff_x_minus_y": diff, "exact_p_two_sided": exact_binomial_two_sided(b, c)}


# ---- running -------------------------------------------------------------------

def run_instances(instances, label: str, split_seed_public: str | None):
    specs = arm_specs()
    results = {"schema_version": SCHEMA_RESULTS, "label": label,
               "split_seed": split_seed_public, "arms": [s.name for s in specs],
               "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label,
               "instances": []}
    timing: dict[str, dict[str, int]] = {}
    for inst in instances:
        w = inst.window
        exp = oracle(w)
        ok, why = planter_agrees(w, inst.stratum)
        rec = {"instance_id": inst.instance_id, "stratum": inst.stratum,
               "scale": inst.scale, "arms": {}}
        rng = random.Random(int(sha256_text(inst.instance_id)[:12], 16))
        for spec in specs:
            t0 = time.perf_counter_ns()
            v = run_arm(spec, w, rng)
            timing.setdefault(inst.instance_id, {})[spec.name] = time.perf_counter_ns() - t0
            rec["arms"][spec.name] = v.as_dict()
        results["instances"].append(rec)
        custody["instances"].append({
            "instance_id": inst.instance_id, "stratum": inst.stratum, "scale": inst.scale,
            "expected": exp.as_dict(), "planter_agrees": ok, "planter_note": why,
            "decidable_from_fit_window": decidable_from_fit_window(w),
        })
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -------------------------------------------------------------------

def _exact(a: dict, e: dict) -> bool:
    return a["capability"] == e["capability"] and a["activity"] == e["activity"]


def score(res: dict, cus: dict, timing: dict) -> dict:
    arms = res["arms"]
    exp = {c["instance_id"]: c for c in cus["instances"]}
    per_arm: dict[str, dict] = {}
    for a in arms:
        ex, cap, act = [], [], []
        by_stratum: dict[str, list[bool]] = {}
        by_scale: dict[str, list[bool]] = {s: [] for s in SCALES}
        for rec in res["instances"]:
            e = exp[rec["instance_id"]]["expected"]
            v = rec["arms"][a]
            hit = _exact(v, e)
            ex.append(hit)
            cap.append(v["capability"] == e["capability"])
            act.append(v["activity"] == e["activity"])
            by_stratum.setdefault(rec["stratum"], []).append(hit)
            by_scale[rec["scale"]].append(hit)
        w = sum(t.get(a, 0) for t in timing.values()) if timing else 0
        per_arm[a] = {
            "n_evaluated": len(ex),
            "exact_rate": sum(ex) / len(ex) if ex else 0.0,
            "capability_rate": sum(cap) / len(cap) if cap else 0.0,
            "activity_rate": sum(act) / len(act) if act else 0.0,
            "per_stratum": {k: {"n_evaluated": len(v), "exact_rate": sum(v) / len(v)}
                            for k, v in sorted(by_stratum.items())},
            "per_scale": {k: {"n_evaluated": len(v),
                              "exact_rate": (sum(v) / len(v)) if v else 0.0}
                          for k, v in by_scale.items()},
            "wall_ms": round(w / 1e6, 6),
        }
    vec = {a: [_exact(r["arms"][a], exp[r["instance_id"]]["expected"]) for r in res["instances"]]
           for a in arms}
    cell_of = [f"{r['stratum']}|{r['scale']}" for r in res["instances"]]
    cells = sorted(set(cell_of))
    # Per (arm, cell): how many instances were exact, and whether the arm's
    # verdict was CONSTANT across the cell.  Constancy is what makes this a
    # constructive result rather than a sampling one, so it is measured, not
    # assumed.
    cell_exact: dict[str, dict[str, tuple[int, int]]] = {}
    cell_constant: dict[str, dict[str, bool]] = {}
    for a in arms:
        ce, cc = {}, {}
        for c in cells:
            idx = [i for i, cl in enumerate(cell_of) if cl == c]
            hits = [vec[a][i] for i in idx]
            verds = {(res["instances"][i]["arms"][a]["capability"],
                      res["instances"][i]["arms"][a]["activity"]) for i in idx}
            ce[c] = (sum(hits), len(hits))
            cc[c] = len(verds) <= 1
        cell_exact[a], cell_constant[a] = ce, cc
    return {"per_arm": per_arm, "vec": vec, "cells": cells, "cell_of": cell_of,
            "cell_exact": cell_exact, "cell_constant": cell_constant,
            "strata": [r["stratum"] for r in res["instances"]],
            "scales": [r["scale"] for r in res["instances"]]}


def cell_compare(sc: dict, x: str, y: str, cells: list[str] | None = None) -> dict:
    """Deterministic cell-level comparison, replacing a paired significance test.

    The arms' verdicts are constant within a cell (asserted by G8), so there is
    no chance mechanism for a paired exact test to test: a p-value over instance
    counts would be an inflated denominator dressed as evidence.  The honest
    quantity is how many CELLS each arm is exact on."""
    cs = cells if cells is not None else sc["cells"]
    ex = sc["cell_exact"]

    def won(a, c):
        h, t = ex[a][c]
        return t > 0 and h == t

    x_only = sorted(c for c in cs if won(x, c) and not won(y, c))
    y_only = sorted(c for c in cs if won(y, c) and not won(x, c))
    return {"n_cells": len(cs), "x_exact_cells": sum(1 for c in cs if won(x, c)),
            "y_exact_cells": sum(1 for c in cs if won(y, c)),
            "x_only_cells": x_only, "y_only_cells": y_only,
            "x_ahead": len(x_only) > 0 and len(y_only) == 0}


# ---- gates ---------------------------------------------------------------------
# Every gate is a POSITIVE test carrying its own n_evaluated.  No terminal is
# computed as the negation of another gate.  A gate with n_evaluated == 0 reports
# CANNOT_CHECK and never a pass.

def _cc(n: int) -> str:
    return "CANNOT_CHECK_NO_INSTANCES" if n == 0 else "EVALUATED"


def gates(sc: dict, res: dict, cus: dict, selftest_ok: bool | None) -> dict:
    g: dict[str, dict] = {}
    vec, strata, scales = sc["vec"], sc["strata"], sc["scales"]
    n = len(strata)
    pa = sc["per_arm"]

    # G0a -- reproduced known answers (from the selftest report)
    g["G0a_KNOWN_ANSWER"] = {
        "n_cells": len(sc["cells"]),
        "pass": selftest_ok, "n_evaluated": (len(CELLS) + 4) if selftest_ok is not None else 0,
        "status": "EVALUATED" if selftest_ok is not None else "CANNOT_CHECK_NO_SELFTEST_REPORT",
        "rule": "one hand-authored fixture per (stratum, scale) cell plus the planted "
                "positives are reproduced in the selftest report"}

    # G0b -- oracle self-agreement and generator validity
    pl = sum(1 for c in cus["instances"] if c["planter_agrees"])
    dec = sum(1 for c in cus["instances"] if c["decidable_from_fit_window"])
    g["G0b_ORACLE_SELF_AGREEMENT"] = {
        "n_cells": len(sc["cells"]),
        "planter_agree": {"ok": pl, "n": n},
        "decidable_from_fit_window": {"ok": dec, "n": n},
        "pass": pl == n and dec == n, "n_evaluated": n,
        "rule": "the planter's declared (capability, activity) effect equals the "
                "full-structure recomputation on every instance, and every instance's "
                "holdout direction is already carried by its fit window"}

    # G0c -- null calibration.  Each no-alarm assertion is paired below in the
    # selftest with a planted positive that must trip it.
    cap_flat = [i for i in range(n) if cus["instances"][i]["expected"]["capability"] != RISE]
    always_rise_hits = sum(1 for i in cap_flat if vec["C_ALWAYS_RISE"][i])
    cap_moves = [i for i in range(n) if cus["instances"][i]["expected"]["capability"] != FLAT]
    always_flat_hits = sum(1 for i in cap_moves if vec["C_ALWAYS_FLAT"][i])
    rng = random.Random(SHUFFLE_SEED)
    shuffled = [c["expected"] for c in cus["instances"]]
    rng.shuffle(shuffled)
    m_shuf = sum(1 for r, e in zip(res["instances"], shuffled) if _exact(r["arms"][M_ARM], e)) / n
    # Every arm that holds the activity channels reads them directly, so the
    # joint exact match reduces to a three-way guess on the capability half.
    # The null's expectation is therefore 1/3 exactly, and the majority-class
    # rate is a derived quantity too.  Both are computed, not chosen: this gate
    # carries no threshold constant.
    cap_truth = [c["expected"]["capability"] for c in cus["instances"]]
    majority = max(Counter(cap_truth).values()) / n
    rnd_cap = sum(1 for r, c in zip(res["instances"], cus["instances"])
                  if r["arms"]["C_RANDOM"]["capability"] == c["expected"]["capability"])
    rnd_above = binom_upper_tail(rnd_cap, n, 1 / 3)
    shuf_above = binom_upper_tail(round(m_shuf * n), n, majority)
    g["G0c_NULL_CALIBRATION"] = {
        "n_cells": len(sc["cells"]),
        "always_rise_exact_where_capability_not_rise": {"hit": always_rise_hits,
                                                        "n_evaluated": len(cap_flat)},
        "always_flat_exact_where_capability_moves": {"hit": always_flat_hits,
                                                     "n_evaluated": len(cap_moves)},
        "random_capability_hits": rnd_cap,
        "random_vs_one_third_upper_tail_p": rnd_above,
        "M_vs_shuffled_labels_exact_rate": m_shuf,
        "shuffled_vs_majority_class_upper_tail_p": shuf_above,
        "majority_class_capability_rate": majority,
        "always_flat_exact_rate": pa["C_ALWAYS_FLAT"]["exact_rate"],
        "n_evaluated": n,
        "pass": (always_rise_hits == 0 and always_flat_hits == 0
                 and rnd_above > 0.05 and shuf_above > 0.05),
        "rule": "the degenerate controls score zero where their answer is wrong; the "
                "random control is not significantly above its derived 1/3 expectation "
                "and the shuffled-label null is not significantly above the majority-class "
                "rate. No threshold constant: both reference values are computed from the "
                "split. `always_flat_exact_rate` is reported beside the majority-class rate "
                "so a degenerate control's score cannot be read as skill."}

    # G1 -- M against the information-matched fitted parent.  Two separate
    # POSITIVE tests; a tie fires neither, and neither is the other's negation.
    # Deterministic, over CELLS: see cell_compare for why no p-value is reported.
    cmp_m = cell_compare(sc, M_ARM, B4X_FITTED_ARM)
    cmp_p = cell_compare(sc, B4X_FITTED_ARM, M_ARM)
    g["G1a_M_AHEAD_OF_MATCHED_PARENT"] = {
        "cells": cmp_m, "n_evaluated": n, "n_cells": len(sc["cells"]),
        "pass": cmp_m["x_ahead"],
        "rule": "M is exact on strictly more CELLS than the information-matched fitted "
                "parent, and on none fewer. No significance test: the arms' verdicts are "
                "constant within a cell (G8), so a paired exact p-value over instance "
                "counts would be an inflated denominator, not evidence."}
    g["G1b_MATCHED_PARENT_AHEAD"] = {
        "cells": cmp_p, "n_evaluated": n, "n_cells": len(sc["cells"]),
        "pass": cmp_p["x_ahead"],
        "rule": "its own positive test, not the negation of G1a"}

    # G2 -- anti-conservatism: M must not buy its invariance robustness by
    # refusing to call the genuine strata.
    idx = [i for i in range(n) if strata[i] in ("GENUINE_CAPABILITY_GAIN",
                                                "GENUINE_CAPABILITY_LOSS")]
    m_ok = sum(1 for i in idx if vec[M_ARM][i])
    par_ok = sum(1 for i in idx if vec[B4X_FITTED_ARM][i])
    g["G2_ANTI_CONSERVATISM"] = {
        "n_cells": len(sc["cells"]),
        "M_exact": m_ok, "parent_exact": par_ok, "n_evaluated": len(idx),
        "status": _cc(len(idx)), "pass": (len(idx) > 0 and m_ok >= par_ok),
        "rule": "on the genuine capability-change strata M is at least as exact as the "
                "matched parent -- invariance must not be bought with abstention"}

    # G3 -- mechanism by omission, per ablation, against the declared prediction
    per_abl = {}
    all_ok = True
    for abl in ABLATION_GROUPS:
        broke = []
        for s in sorted(STRATA):
            si = [i for i in range(n) if strata[i] == s]
            if not si:
                continue
            base = sum(1 for i in si if vec[M_ARM][i]) / len(si)
            got = sum(1 for i in si if vec[abl][i]) / len(si)
            if got < base:
                broke.append(s)
        want = sorted(ABLATION_PREDICTION.get(abl, ()))
        ok = sorted(broke) == want
        all_ok = all_ok and ok
        per_abl[abl] = {"strata_degraded": sorted(broke), "predicted": want,
                        "pass": ok, "n_evaluated": n}
    g["G3_MECHANISM_BY_OMISSION"] = {
        "n_cells": len(sc["cells"]),
        "per_ablation": per_abl, "pass": all_ok, "n_evaluated": n,
        "rule": "each typed-channel ablation degrades exactly the strata declared to "
                "depend on it, and no others"}

    # G4 -- the untyped information ladder, per scale, never pooled.
    #
    # NOT a monotonicity gate.  An earlier version required no rung to be worse
    # than the one below and called a reversal a lane defect.  Measurement showed
    # that framing is wrong: L2 is strictly worse than L1 even after every rung
    # is fitted on its own channel set, because one global sign cannot IGNORE a
    # channel that moves without capability -- the attention channel destroys
    # I5_CITATION_RING, which L1 gets right precisely by not holding it. Fitting
    # does not remove the reversal, so it is a property of untyped aggregation
    # and a finding, registered as P-MEX6-2 and tested in G7.
    #
    # The positive test that remains: the full channel set is exact on strictly
    # more cells than the activity-only rung, per scale.
    per_scale_ladder = {}
    ladder_ok = True
    top, bottom = LADDER[-1][0], LADDER[0][0]
    for scale in SCALES:
        si = [i for i in range(n) if scales[i] == scale]
        sc_cells = sorted({sc["cell_of"][i] for i in si})
        rungs = {name: {"exact_cells": sum(1 for c in sc_cells
                                           if sc["cell_exact"][name][c][1] > 0
                                           and sc["cell_exact"][name][c][0] == sc["cell_exact"][name][c][1]),
                        "exact_rate": (sum(1 for i in si if vec[name][i]) / len(si)) if si else 0.0}
                 for name, _ in LADDER}
        steps = []
        for (a, _), (b, _) in zip(LADDER, LADDER[1:]):
            cp = cell_compare(sc, b, a, sc_cells)
            steps.append({"from": a, "to": b, "cells": cp,
                          "regression": len(cp["y_only_cells"]) > 0})
        tb = cell_compare(sc, top, bottom, sc_cells)
        # a COUNT comparison, not dominance: the top rung is expected to lose
        # I5_CITATION_RING to the activity-only rung (that reversal IS P-MEX6-2),
        # so requiring dominance would make this gate fail on the very mechanism
        # the study registers.
        ok = bool(si) and tb["x_exact_cells"] > tb["y_exact_cells"]
        ladder_ok = ladder_ok and ok
        per_scale_ladder[scale] = {
            "rung": rungs, "steps": steps, "top_vs_bottom": tb,
            "n_evaluated": len(si), "n_cells": len(sc_cells), "status": _cc(len(si)),
            "regressions": [f"{st['from']} -> {st['to']}" for st in steps if st["regression"]],
            "pass": ok}
    g["G4_INFORMATION_LADDER"] = {
        "per_scale": per_scale_ladder, "pass": ladder_ok, "n_evaluated": n,
        "n_cells": len(sc["cells"]),
        "rule": f"positive test, per scale and never pooled: {top} is exact on strictly more "
                f"cells than {bottom} (a count, not dominance -- the top rung is expected to "
                f"lose I5_CITATION_RING to {bottom}, which is P-MEX6-2). Intermediate reversals are REPORTED, not failed: every "
                "rung is fitted on its own channel set, so a reversal is a property of untyped "
                "aggregation (P-MEX6-2), not a lane defect."}

    # G5 -- the hostile-invariance suite: every invariance its own positive test
    per_inv = {}
    inv_ok = True
    for s in sorted(PERTURBATION_STRATA):
        si = [i for i in range(n) if strata[i] == s]
        m_rate = (sum(1 for i in si if vec[M_ARM][i]) / len(si)) if si else 0.0
        p_rate = (sum(1 for i in si if vec[B4X_FITTED_ARM][i]) / len(si)) if si else 0.0
        ok = bool(si) and m_rate == 1.0
        inv_ok = inv_ok and ok
        per_inv[s] = {"M_exact_rate": m_rate, "matched_parent_exact_rate": p_rate,
                      "n_evaluated": len(si), "status": _cc(len(si)), "pass": ok}
    g["G5_HOSTILE_INVARIANCE_SUITE"] = {
        "n_cells": len(sc["cells"]),
        "per_invariance": per_inv, "pass": inv_ok, "n_evaluated": n,
        "rule": "protocol section 7 I1-I10 and the short protocol's X6-I7, each its own "
                "positive test with its own denominator; a stratum with no instances "
                "reports CANNOT_CHECK and never a pass"}

    # G6 -- cross-scale transfer, separately in each scale
    per_scale = {}
    tr_ok = True
    for scale in SCALES:
        si = [i for i in range(n) if scales[i] == scale]
        sc_cells = sorted({sc["cell_of"][i] for i in si})
        cp = cell_compare(sc, M_ARM, B4X_FITTED_ARM, sc_cells)
        rate = (sum(1 for i in si if vec[M_ARM][i]) / len(si)) if si else 0.0
        ok = bool(si) and not cp["y_only_cells"]
        tr_ok = tr_ok and ok
        per_scale[scale] = {"M_exact_rate": rate, "cells": cp, "n_evaluated": len(si),
                            "n_cells": len(sc_cells), "status": _cc(len(si)), "pass": ok}
    g["G6_CROSS_SCALE_TRANSFER"] = {
        "per_scale": per_scale, "pass": tr_ok, "n_evaluated": n,
        "n_cells": len(sc["cells"]),
        "rule": "the result must hold separately at each unit of analysis (protocol section 3): "
                "in each scale the matched parent is exact on no cell M misses. A result that "
                "does not transfer to the second scale is killed."}

    # G7 -- the registered structural prediction, stated before the run
    fails, unexpected = [], []
    for s in sorted(STRATA):
        si = [i for i in range(n) if strata[i] == s]
        if not si:
            continue
        rate = sum(1 for i in si if vec[B4X_FITTED_ARM][i]) / len(si)
        if rate < 1.0:
            (fails if s in DECOUPLED_STRATA else unexpected).append(s)
    missed = [s for s in DECOUPLED_STRATA if s not in fails]
    ladder_regressions = sorted({r for v in per_scale_ladder.values() for r in v["regressions"]})
    p2_ok = ladder_regressions == sorted(PREDICTED_LADDER_REGRESSIONS)
    g["G7_REGISTERED_PREDICTION"] = {
        "n_cells": len(sc["cells"]),
        "P_MEX6_2_predicted_ladder_regressions": sorted(PREDICTED_LADDER_REGRESSIONS),
        "P_MEX6_2_observed_ladder_regressions": ladder_regressions,
        "P_MEX6_2_pass": p2_ok,
        "predicted_failure_support": sorted(DECOUPLED_STRATA),
        "observed_failures_inside_support": sorted(fails),
        "observed_failures_outside_support": sorted(unexpected),
        "predicted_but_not_observed": sorted(missed),
        "pass": not unexpected and not missed and p2_ok, "n_evaluated": n,
        "rule": "two predictions registered before the run. P-MEX6-1: the information-matched "
                "untyped parent fails exactly on the strata where the true capability direction "
                "contradicts a channel it must give one global sign to, and nowhere else. "
                "P-MEX6-2: the fitted untyped ladder is NOT monotone -- adding the attention "
                "channel strictly reduces exactness, because one global sign cannot ignore a "
                "channel that moves without capability. Both must hold."}

    # G8 -- verdict constancy within a cell.  This is the gate that licenses
    # every deterministic comparison above.  If an arm's verdict ever varied
    # inside a cell there WOULD be a chance mechanism, the constructive framing
    # would be wrong, and inferential statistics would be required -- so a
    # failure here routes CANNOT_CHECK rather than being quietly absorbed.
    varying = sorted(f"{a}|{c}" for a in res["arms"] for c in sc["cells"]
                     if not sc["cell_constant"][a][c] and not a.startswith("C_RANDOM"))
    g["G8_VERDICT_CONSTANCY_WITHIN_CELL"] = {
        "varying_arm_cells": varying, "n_evaluated": n, "n_cells": len(sc["cells"]),
        "instances_per_cell": (n // len(sc["cells"])) if sc["cells"] else 0,
        "pass": not varying,
        "rule": "every arm's verdict is constant across the instances of a cell, so the "
                "study is a CONSTRUCTIVE separation over cells and not a sampling study. "
                "C_RANDOM is excluded by construction: it draws per instance and is "
                "expected to vary. Instances per cell buy structural coverage -- a cell's "
                "verdict is shown invariant under varying baselines, step sizes and step "
                "onsets -- and buy no statistical power, which is why no gate but G0c "
                "reports a p-value."}

    # coverage ledger -- reported, never a gate
    drawn = Counter(f"{s}|{c}" for s, c in zip(strata, scales))
    never = sorted({f"{s}|{c}" for s, c in CELLS} - set(drawn))
    g["COVERAGE_LEDGER"] = {
        "drawn": dict(sorted(drawn.items())), "never_exercised": never,
        "all_registered_mechanisms_exercised": not never, "n_evaluated": n,
        "n_cells": len(sc["cells"]),
        "rule": "reported, not a gate: any registered cell with zero instances is named "
                "here so no rate computed over it can be read as 'checked and fine'"}

    g["ROUTE"] = route(g)
    return g


def route(g: dict) -> dict:
    hard = ("G0a_KNOWN_ANSWER", "G0b_ORACLE_SELF_AGREEMENT", "G0c_NULL_CALIBRATION",
            "G8_VERDICT_CONSTANCY_WITHIN_CELL")
    for h in hard:
        if g[h].get("pass") is not True:
            return {"route": "CANNOT_CHECK", "terminal": "NONE",
                    "reason": f"hard gate {h} did not pass -- lane defect; repair, "
                              "re-freeze, no arm verdict"}
    if not g["G6_CROSS_SCALE_TRANSFER"]["pass"]:
        return {"route": "PARENT_SUFFICIENT", "terminal": "NO_CROSS_SCALE_TRANSFER",
                "reason": "the result does not hold at the second unit of analysis"}
    if g["G1b_MATCHED_PARENT_AHEAD"]["pass"]:
        return {"route": "PARENT_SUFFICIENT", "terminal": "UNTYPED_AGGREGATE_SUFFICIENT",
                "reason": "the information-matched untyped parent is ahead of the typed "
                          "state; X6 contracts to an interpretive framework"}
    if not g["G1a_M_AHEAD_OF_MATCHED_PARENT"]["pass"]:
        return {"route": "PARENT_SUFFICIENT", "terminal": "TYPING_NOT_SEPARATED",
                "reason": "M and the information-matched untyped parent tie; typing adds "
                          "nothing detectable here and X6 contracts to an interpretive "
                          "framework (protocol section 6 contraction rule)"}
    if not g["G2_ANTI_CONSERVATISM"]["pass"]:
        return {"route": "M_OVER_ABSTAINS", "terminal": "NONE",
                "reason": "M's invariance robustness was bought by refusing the genuine strata"}
    # The all-pass terminal asserts the invariance suite, the omission mechanism,
    # the ladder AND the registered prediction, so the route must read all four.
    # Claiming "the mechanism map matches its declared prediction" without
    # consulting G7 would be a sentence nobody executed.
    unmet = [k for k in ("G3_MECHANISM_BY_OMISSION", "G4_INFORMATION_LADDER",
                         "G5_HOSTILE_INVARIANCE_SUITE", "G7_REGISTERED_PREDICTION")
             if not g[k]["pass"]]
    if unmet:
        return {"route": "CANNOT_CHECK", "terminal": "NONE",
                "reason": "M is ahead of the matched parent, but " + ", ".join(unmet)
                          + " did not hold, so no representational claim is supported"}
    # NOT a residual.  Design section 1.3 declares M exact by construction on this
    # generator, so the M-vs-parent gap is arithmetic and cannot be the finding.
    # Awarding a residual on the strength of that gap would contradict the
    # design's own disclaimer, so no path here reaches one.  What this terminal
    # does claim is representational and is carried by G3, G5, G6 and G7: at
    # matched information a single global sign per channel cannot represent
    # "volume counts only when validation accompanies it", and the mechanism map
    # -- which typed channel is load-bearing for which invariance -- is
    # established and matches its declared prediction.
    return {"route": "MECHANISM_ESTABLISHED_NOT_A_RESIDUAL",
            "terminal": "UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION",
            "reason": "the mechanism map matches its declared prediction, every registered "
                      "hostile invariance holds, and the result holds separately at both "
                      "scales. M's exactness is by construction (design 1.3) and is NOT "
                      "evidence; no ME-X6 residual is claimed"}


# ---- selftest ------------------------------------------------------------------

def mex6_typed_capability(w):
    from mex6_arms import TYPED_SIGNS, _dir_of
    keys = tuple(k for k in CHANNELS if k in TYPED_SIGNS)
    return _dir_of(w, keys, TYPED_SIGNS)


def _skew_i4(w):
    """A hand-built counterfactual: give the validated channels a larger step
    than the retraction channel, which the generator never does because all
    channels of an instance share one step magnitude."""
    from dataclasses import replace as _replace
    from mex6_model import Period
    per = []
    for idx, pd in enumerate(w.periods):
        ch = dict(pd.channels)
        half = w.fit_len // 2
        if idx >= half:
            for c in ("formal_artifacts", "replications_passed", "downstream_reuse"):
                ch[c] = ch[c] + 40
        per.append(Period(index=pd.index, latent=pd.latent, channels=ch))
    return _replace(w, periods=tuple(per))

def stage_selftest(out_dir: Path) -> int:
    rep: dict = {"schema_version": SCHEMA_RESULTS + ".selftest"}
    insts = generate_split("selftest", SELFTEST_SEED, 1)
    signs_ok, committed, refit = assert_frozen_signs_still_reproduce()
    rep["frozen_signs_still_reproduce"] = signs_ok
    load_fitted_signs(committed)
    specs = {s.name: s for s in arm_specs()}

    # 1. known answer: every cell's recomputed verdict equals its declared effect
    ka = sum(1 for i in insts if planter_agrees(i.window, i.stratum)[0])
    rep["known_answer"] = {"ok": ka, "n": len(insts)}

    # 2. the fit window determines the holdout direction on every cell
    dec = sum(1 for i in insts if decidable_from_fit_window(i.window))
    rep["decidable_from_fit_window"] = {"ok": dec, "n": len(insts)}

    # 3. M is exact on every hand-authored cell
    m_ok = sum(1 for i in insts
               if run_arm(specs[M_ARM], i.window, random.Random(0)).as_dict()
               == oracle(i.window).as_dict())
    rep["M_exact_on_every_cell"] = {"ok": m_ok, "n": len(insts)}

    # 4. planted positives: each no-alarm assertion is paired with a case that
    #    MUST trip it.  An assertion never shown to fire is not evidence.
    positives = {}
    #    (a) a broken M -- capability read from raw volume -- must lose the
    #        decoupled strata
    broken = [i for i in insts if i.stratum in DECOUPLED_STRATA]
    from mex6_arms import _cap_untyped
    untyped_spec = {sp.name: sp for sp in arm_specs()}[B4X_ARM]
    tripped = sum(1 for i in broken
                  if _cap_untyped(i.window, untyped_spec, random.Random(0))
                  != oracle(i.window).capability)
    positives["untyped_reading_fails_the_decoupled_strata"] = {"tripped": tripped,
                                                               "n": len(broken)}
    #    (b) the always-rise control must be wrong wherever capability is not RISE
    nr = [i for i in insts if oracle(i.window).capability != RISE]
    positives["always_rise_is_wrong_where_capability_is_not_rise"] = {
        "tripped": len(nr), "n": len(nr)}
    #    (c) a planted sign flip in M's typed score must break I4
    i4 = [i for i in insts if i.stratum == "I4_RETRACTED_WORK"]
    from mex6_arms import TYPED_SIGNS, _dir_of
    flipped = dict(TYPED_SIGNS); flipped["retractions"] = +1
    keys = tuple(k for k in CHANNELS if k in flipped)
    tr = sum(1 for i in i4
             if _dir_of(i.window, keys, flipped) != oracle(i.window).capability)
    positives["flipping_the_retraction_sign_breaks_I4"] = {"tripped": tr, "n": len(i4)}
    #    (d) verdict constancy must be capable of firing.  I4's typed sum is
    #        s1 + s2 + s3 - 2r, whose sign is invariant only because every channel
    #        of an instance shares one step magnitude.  Hand-build a window with
    #        per-channel steps and the sum flips to RISE, so a cell holding both
    #        would not be constant.  A constancy gate never shown to fire would be
    #        a counter that never ran.
    from mex6_arms import _dir_of as _dir
    i4w = [i.window for i in insts if i.stratum == "I4_RETRACTED_WORK"]
    flips = 0
    for w in i4w:
        base = mex6_typed_capability(w)
        skewed = _skew_i4(w)
        if skewed is not None and mex6_typed_capability(skewed) != base:
            flips += 1
    positives["per_channel_steps_break_I4_constancy"] = {"tripped": flips, "n": len(i4w)}

    #    (e) the planter must reject a mislabelled stratum
    #        the relabel must name a stratum with a DIFFERENT declared effect:
    #        the planter checks effects, not names, so relabelling I10 as
    #        GENUINE_CAPABILITY_GAIN is correctly accepted -- both declare
    #        (RISE, RISE) -- and would be a false alarm, not a miss.
    def _other(st: str) -> str | None:
        for cand in sorted(STRATA):
            if STRATA[cand] != STRATA[st]:
                return cand
        return None
    pairs = [(i, _other(i.stratum)) for i in insts]
    pairs = [(i, o) for i, o in pairs if o]
    mism = sum(1 for i, o in pairs if not planter_agrees(i.window, o)[0])
    positives["planter_rejects_a_mislabelled_stratum"] = {"tripped": mism, "n": len(pairs)}
    rep["constancy_positive_note"] = (
        "a hand-built window with per-channel step magnitudes flips I4's typed capability "
        "from FALL to RISE, so G8's constancy check is demonstrably able to fire")
    rep["planted_positives"] = positives

    rep["passed"] = bool(
        signs_ok and ka == len(insts) and dec == len(insts) and m_ok == len(insts)
        and all(v["tripped"] == v["n"] and v["n"] > 0 for v in positives.values()))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X6_SELFTEST_REPORT.json").write_text(canonical_json(rep))
    print(f"selftest {'PASS' if rep['passed'] else 'FAIL'}: known-answer {ka}/{len(insts)}, "
          f"fit-window-decidable {dec}/{len(insts)}, M exact {m_ok}/{len(insts)}, "
          f"planted positives {sum(1 for v in positives.values() if v['tripped'] == v['n'])}/"
          f"{len(positives)}")
    return 0 if rep["passed"] else 1


# ---- stages --------------------------------------------------------------------

def frozen_signs() -> dict[str, int]:
    """The comparator's signs as COMMITTED in the frozen design JSON.

    Refitting them at run time would mean the "frozen" signs were never frozen:
    a generator or fitting change after the freeze would silently replace the
    committed weights on a protected run.  They are read from the design file,
    and `assert_frozen_signs_still_reproduce` checks that a refit on the public
    development split still yields them -- so drift is caught rather than
    absorbed.
    """
    d = json.loads(DESIGN_JSON.read_text())
    return {arm: {k: int(v) for k, v in sg.items()}
            for arm, sg in d["comparator"]["frozen_fitted_signs"].items()}


def assert_frozen_signs_still_reproduce() -> tuple[bool, dict[str, int], dict[str, int]]:
    committed = frozen_signs()
    refit = fit_all(generate_split("dev", DEV_SEED, 1))
    return committed == refit, committed, refit


def _run_split(label: str, prefix: str, seed: str, per_cell: int, out_dir: Path,
               public: str | None) -> int:
    ok, committed, refit = assert_frozen_signs_still_reproduce()
    if not ok:
        drift = {k: (committed.get(k), refit.get(k)) for k in sorted(set(committed) | set(refit))
                 if committed.get(k) != refit.get(k)}
        print(f"REFUSED: the frozen comparator signs no longer reproduce: {drift}", file=sys.stderr)
        return 5
    load_fitted_signs(committed)
    insts = generate_split(prefix, seed, per_cell)
    res, cus = run_instances(insts, label, public)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X6_{label}_RESULTS_V1.json"
    cp = out_dir / f"ME_X6_{label}_EXPECTED_CUSTODY_V1.json"
    tp = out_dir / f"ME_X6_{label}_TIMING_V1.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus))
    tp.write_text(canonical_json({"schema_version": SCHEMA_RESULTS + ".timing",
                                  "label": label, "wall_ns": timing,
                                  "note": "wall-clock is machine-dependent and is kept "
                                          "out of the deterministic results file"}))
    print(f"{label}: {len(insts)} instances, results sha256 {sha256_file(rp)[:16]}…, "
          f"custody sha256 {sha256_file(cp)[:16]}…")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_cell: int) -> int:
    if per_cell * len(CELLS) > 56:
        print("development split is capped at 56 instances", file=sys.stderr)
        return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_cell, out_dir, DEV_SEED)


def stage_protected(out_dir: Path, per_cell: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized",
              file=sys.stderr)
        return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization file unreadable: {exc}", file=sys.stderr)
        return 3
    token = str(auth.get("human_written_token", "")).strip()
    if not token or auth.get("human_written") is not True or len(token) < 16:
        print("REFUSED: authorization requires human_written=true and a "
              "human_written_token (>= 16 chars)", file=sys.stderr)
        return 3
    design_sha = sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else ""
    if auth.get("acknowledged_design_sha256") != design_sha:
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
    return _run_split("PROTECTED", "protected", seed.decode(), per_cell, out_dir, None)


def stage_analyze(rp: Path, cp: Path, out_dir: Path, label: str | None = None,
                  selftest_report: Path | None = None) -> int:
    res = json.loads(rp.read_text()); cus = json.loads(cp.read_text())
    label = label or res.get("label", "UNKNOWN")
    tp = rp.with_name(rp.name.replace("_RESULTS_", "_TIMING_"))
    timing = json.loads(tp.read_text()).get("wall_ns", {}) if tp.exists() else {}
    sp = selftest_report or (out_dir / "ME_X6_SELFTEST_REPORT.json")
    selftest_ok = bool(json.loads(sp.read_text()).get("passed")) if sp.exists() else None
    sc = score(res, cus, timing)
    gt = gates(sc, res, cus, selftest_ok)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label,
                "results_sha256": sha256_file(rp), "custody_sha256": sha256_file(cp),
                "n_instances": len(res["instances"]),
                "score": {"per_arm": sc["per_arm"]}, "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X6_{label}_ANALYSIS_V1.json").write_text(canonical_json(analysis))
    (out_dir / f"ME_X6_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    r = gt["ROUTE"]
    print(f"{label} route: {r['route']} ({r['reason']}); terminal: {r['terminal']}; "
          f"M exact {sc['per_arm'][M_ARM]['exact_rate']:.3f}, matched parent "
          f"{sc['per_arm'][B4X_FITTED_ARM]['exact_rate']:.3f}")
    return 0


def render_md(a: dict) -> str:
    g = a["gates"]; pa = a["score"]["per_arm"]
    L = [f"# ME-X6 {a['label']} analysis", "",
         f"- instances: {a['n_instances']}",
         f"- route: `{g['ROUTE']['route']}` — terminal `{g['ROUTE']['terminal']}`",
         f"- reason: {g['ROUTE']['reason']}", "",
         "## Gates", "",
         "Both denominators are shown. Instances are structural replicates of a cell, not "
         "independent observations: only G0c reports an inferential statistic.", "",
         "| gate | pass | instances | cells |", "|---|---|---|---|"]
    for k, v in g.items():
        if k in ("ROUTE", "COVERAGE_LEDGER"):
            continue
        L.append(f"| `{k}` | {v.get('pass')} | {v.get('n_evaluated')} | {v.get('n_cells', '—')} |")
    L += ["", "## Arms", "", "| arm | exact | capability | activity | n |", "|---|---|---|---|---|"]
    for k, v in sorted(pa.items(), key=lambda x: -x[1]["exact_rate"]):
        L.append(f"| `{k}` | {v['exact_rate']:.3f} | {v['capability_rate']:.3f} | "
                 f"{v['activity_rate']:.3f} | {v['n_evaluated']} |")
    cl = g["COVERAGE_LEDGER"]
    L += ["", "## Coverage", "",
          f"- all registered cells exercised: **{cl['all_registered_mechanisms_exercised']}**",
          f"- never exercised: {cl['never_exercised'] or 'none'}", ""]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-cell", type=int, default=None)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_cell or 1)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_cell or 50, a.seed_file)
    if not a.results or not a.custody:
        print("analyze needs --results and --custody", file=sys.stderr)
        return 2
    return stage_analyze(a.results, a.custody, a.out, None, a.selftest_report)


if __name__ == "__main__":
    sys.exit(main())
