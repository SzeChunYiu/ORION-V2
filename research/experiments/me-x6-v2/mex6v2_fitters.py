"""ME-X6 V2 — capacity-matched UNTYPED comparators, learned rather than hand-set.

ME-X6 V1's comparator `B4X_FITTED_UNTYPED` learns one weight per channel in
{-1, 0, +1} by univariate marginal screening.  Its `0` arises only from an exact
tie in a per-channel tally, so in practice it cannot *drop* a channel, and V1's
own provenance receipt (section 4) attributed the comparator's failure to exactly
that: restoring M's magnitudes alone recovers one stratum, zeroing the six
channels M weights at zero recovers all seven.

That zeroing was **hand-set**.  V2 asks the question V1 could not: does a
comparator whose weight class *contains zero and non-unit magnitudes* and which
is **fitted** from the public development split recover the conjunction?

Two standard, fully pre-specified procedures are registered.  Neither is an
exhaustive search over the weight class -- an exhaustive search would contain M's
own vector and would therefore be an arm that could not fail (see
`MEX6V2_REACHABILITY_AUDIT`).  Both are deterministic: no RNG, no seed, fixed
tie-breaks, fixed iteration caps.  Pure standard library, exactly as V1.

  B6_GREEDY_SUBSET_UNTYPED   forward selection over (channel, weight) pairs,
                             weight in {-2, -1, +1}; unselected channels are 0.
  B7_L1_PATH_UNTYPED         L1-penalised least squares (lasso) by cyclic
                             coordinate descent over a frozen lambda grid, in two
                             pre-registered feature scalings.

`B8_CAPACITY_MATCHED_BEST` is whichever of the two scores higher on the
development split under a frozen rule.  Selecting the stronger of two
pre-specified fitters on the *development* split only is what makes the
comparator the strongest available in its class; it sees no protected instance.
"""
from __future__ import annotations

from typing import Iterable, Sequence

# --- the shared decision rule, taken from V1 unchanged --------------------------
# `_halves` and the late-minus-early half difference are exactly what V1's
# `_dir_of` sums.  The fitters here operate on that same statistic, so a fitted
# vector is loadable into V1's own `_cap_fitted` code path without translation.

RISE = "RISE"
FLAT = "FLAT"
FALL = "FALL"

GREEDY_WEIGHTS: tuple[int, ...] = (1, -1, -2)   # tie-break order; 0 = unselected
GREEDY_MAX_ROUNDS = 16

LASSO_SCALINGS: tuple[str, ...] = ("RAW", "STANDARDIZED")
LASSO_GRID_POINTS = 25
LASSO_GRID_DECADES = 6.0        # lambda_max * 10**(-j * DECADES / (POINTS - 1))
LASSO_MAX_ITER = 5000
LASSO_TOL = 1e-10
LASSO_ZERO_EPS = 1e-9           # |w| below this is reported and scored as exactly 0


def half_difference(window, channels: Sequence[str]) -> dict[str, int]:
    """Late-half minus early-half channel totals over the fit window.

    Integer arithmetic, no normalisation: the same quantity V1's `_dir_of`
    accumulates, so nothing is lost or rescaled between fitting and scoring.
    """
    h = window.fit_len // 2
    early = window.fit_periods[:h]
    late = window.fit_periods[h:]
    return {k: sum(p.channels[k] for p in late) - sum(p.channels[k] for p in early)
            for k in channels}


def direction_from_weights(delta: dict[str, int], weights: dict[str, float]) -> str:
    s = sum(w * delta[k] for k, w in weights.items() if w)
    return RISE if s > 0 else (FALL if s < 0 else FLAT)


def accuracy(deltas: Sequence[dict[str, int]], truths: Sequence[str],
             weights: dict[str, float]) -> int:
    return sum(1 for d, t in zip(deltas, truths)
               if direction_from_weights(d, weights) == t)


# ---- B6: greedy forward selection ----------------------------------------------

def fit_greedy_subset(deltas: Sequence[dict[str, int]], truths: Sequence[str],
                      channels: Sequence[str]) -> tuple[dict[str, int], list[dict]]:
    """Forward selection over (channel, weight) pairs.

    Start from the all-zero vector -- which predicts FLAT everywhere, a real and
    non-trivial hypothesis on this generator.  At each round, score every
    (unassigned channel, weight in GREEDY_WEIGHTS) addition and take the best;
    accept only on a STRICT improvement.  Ties break by, in order: higher
    accuracy, smaller |weight|, channel order as given, then GREEDY_WEIGHTS order.

    This is a heuristic and is *not* exhaustive: it cannot discover a channel that
    only helps in combination with another not yet selected.  That is the property
    that makes it able to fail, and it is demonstrated on a constructed dataset in
    `tests/unit/test_me_x6_v2_capacity_matched.py`.
    """
    weights: dict[str, int] = {}
    trace: list[dict] = []
    best_acc = accuracy(deltas, truths, weights)
    trace.append({"round": 0, "added": None, "weight": None, "accuracy": best_acc,
                  "n": len(truths)})
    for rnd in range(1, GREEDY_MAX_ROUNDS + 1):
        best: tuple[int, int, int, int] | None = None   # (acc, -|w| rank, chan idx, w idx)
        best_pair: tuple[str, int] | None = None
        for ci, ch in enumerate(channels):
            if ch in weights:
                continue
            for wi, w in enumerate(GREEDY_WEIGHTS):
                trial = dict(weights)
                trial[ch] = w
                acc = accuracy(deltas, truths, trial)
                key = (acc, -abs(w), -ci, -wi)
                if best is None or key > best:
                    best, best_pair = key, (ch, w)
        if best is None or best_pair is None or best[0] <= best_acc:
            break
        ch, w = best_pair
        weights[ch] = w
        best_acc = best[0]
        trace.append({"round": rnd, "added": ch, "weight": w, "accuracy": best_acc,
                      "n": len(truths)})
    return {c: int(weights.get(c, 0)) for c in channels}, trace


# ---- B7: L1-penalised least squares over a frozen lambda path -------------------

def _design(deltas: Sequence[dict[str, int]], channels: Sequence[str],
            scaling: str) -> tuple[list[list[float]], list[float]]:
    x = [[float(d[c]) for c in channels] for d in deltas]
    if scaling == "RAW":
        return x, [1.0] * len(channels)
    n = len(x)
    scales: list[float] = []
    for j in range(len(channels)):
        col = [row[j] for row in x]
        mean = sum(col) / n
        var = sum((v - mean) ** 2 for v in col) / n
        sd = var ** 0.5
        scales.append(sd if sd > 0 else 1.0)
    return [[row[j] / scales[j] for j in range(len(channels))] for row in x], scales


def _soft(z: float, g: float) -> float:
    if z > g:
        return z - g
    if z < -g:
        return z + g
    return 0.0


def _lasso(x: list[list[float]], y: list[float], lam: float) -> list[float]:
    """Cyclic coordinate descent for (1/2n)||y - Xw||^2 + lam*||w||_1, no intercept.

    Deterministic: zero initialisation, fixed cyclic order, fixed cap and
    tolerance.  Standard soft-thresholding update; kept in pure Python because the
    study, like V1, carries no third-party dependency.
    """
    n, p = len(x), len(x[0])
    w = [0.0] * p
    col_sq = [sum(row[j] * row[j] for row in x) for j in range(p)]
    resid = list(y)
    for _ in range(LASSO_MAX_ITER):
        delta_max = 0.0
        for j in range(p):
            if col_sq[j] == 0.0:
                continue
            wj = w[j]
            rho = sum(x[i][j] * (resid[i] + x[i][j] * wj) for i in range(n))
            new = _soft(rho / n, lam) / (col_sq[j] / n)
            if new != wj:
                d = new - wj
                for i in range(n):
                    resid[i] -= x[i][j] * d
                w[j] = new
                delta_max = max(delta_max, abs(d))
        if delta_max < LASSO_TOL:
            break
    return w


def fit_l1_path(deltas: Sequence[dict[str, int]], truths: Sequence[str],
                channels: Sequence[str]) -> tuple[dict[str, float], list[dict]]:
    """Fit both registered scalings across the frozen lambda grid; select on the
    development split by capability accuracy, ties to the LARGER lambda (sparser),
    then RAW before STANDARDIZED.  No RNG anywhere.
    """
    y = [1.0 if t == RISE else (-1.0 if t == FALL else 0.0) for t in truths]
    n = len(y)
    best: tuple[int, float, int] | None = None
    best_w: dict[str, float] | None = None
    trace: list[dict] = []
    for si, scaling in enumerate(LASSO_SCALINGS):
        x, scales = _design(deltas, channels, scaling)
        lam_max = max(abs(sum(x[i][j] * y[i] for i in range(n))) / n
                      for j in range(len(channels)))
        if lam_max <= 0:
            lam_max = 1.0
        for gi in range(LASSO_GRID_POINTS):
            lam = lam_max * 10 ** (-gi * LASSO_GRID_DECADES / (LASSO_GRID_POINTS - 1))
            raw = _lasso(x, y, lam)
            w = {c: (0.0 if abs(raw[j] / scales[j]) < LASSO_ZERO_EPS else raw[j] / scales[j])
                 for j, c in enumerate(channels)}
            acc = accuracy(deltas, truths, w)
            nz = sum(1 for v in w.values() if v)
            trace.append({"scaling": scaling, "lambda": lam, "accuracy": acc,
                          "nonzero": nz, "n": n})
            key = (acc, lam, -si)
            if best is None or key > best:
                best, best_w = key, w
    assert best_w is not None
    return best_w, trace


# ---- B8: the registered capacity-matched comparator -----------------------------

def select_capacity_matched(dev_deltas: Sequence[dict[str, int]],
                            dev_truths: Sequence[str],
                            channels: Sequence[str]) -> dict:
    """Fit both procedures on the development split and register the stronger.

    Frozen selection rule: higher development capability accuracy wins; an exact
    tie goes to B6, the sparser and simpler of the two.  The protected seed plays
    no part here and could not -- this function never sees a protected instance,
    and the whole fit is a deterministic function of the public development split.
    """
    w6, t6 = fit_greedy_subset(dev_deltas, dev_truths, channels)
    w7, t7 = fit_l1_path(dev_deltas, dev_truths, channels)
    a6 = accuracy(dev_deltas, dev_truths, w6)
    a7 = accuracy(dev_deltas, dev_truths, w7)
    chosen = "B6_GREEDY_SUBSET_UNTYPED" if a6 >= a7 else "B7_L1_PATH_UNTYPED"
    return {
        "B6_GREEDY_SUBSET_UNTYPED": {"weights": w6, "dev_capability_correct": a6,
                                     "trace": t6},
        "B7_L1_PATH_UNTYPED": {"weights": w7, "dev_capability_correct": a7,
                               "trace_len": len(t7)},
        "B8_CAPACITY_MATCHED_BEST": {
            "selected_fitter": chosen,
            "weights": (w6 if chosen == "B6_GREEDY_SUBSET_UNTYPED" else w7),
            "dev_capability_correct": max(a6, a7),
        },
        "n_dev": len(dev_truths),
        "selection_rule": "higher development capability accuracy; exact tie to B6",
    }


def zero_count(weights: dict[str, float]) -> int:
    return sum(1 for v in weights.values() if not v)


def channels_of(weights: Iterable[str]) -> tuple[str, ...]:
    return tuple(weights)
