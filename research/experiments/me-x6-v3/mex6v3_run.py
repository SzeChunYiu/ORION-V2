"""ME-X6 V3 runner: selftest / fit / freeze / dev / protected / digest / analyze.

    selftest    known-answer fixtures, generator validity on the public development
                split, the role-coverage census, the controls that keep every zero
                honest, and the pre-run REACHABILITY audit of every registered clause
    fit         fit the coverage-MATCHED comparators on the PUBLIC V3 development
                split (18 strata x 2 scales x 2 = 72) and write the fit JSON
    freeze      write the design JSON once (refuses if it exists): fitted vectors,
                substrate pins, seed commitment, reachability audit
    dev         score every arm on the development split
    protected   refuses unless PROTECTED_RUN_AUTHORIZATION.json is present, the
                acknowledged design digest matches, and the custody seed hashes to
                the frozen commitment (exit 3 / 3 / 4); archives the authorization
    digest      regenerate a split from a seed and print its sha256 (run in a fresh
                process under another PYTHONHASHSEED: the reproducibility guard)
    analyze     gates and route from an existing results/custody pair

V1's modules and V2's fitters are imported READ-ONLY.  Nothing here writes into
me-x6/ or me-x6-v2/, refits any frozen vector of theirs, or touches a gate, number,
terminal or authorization of either.  New run identity, pure standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "me-x6"
V2 = HERE.parent / "me-x6-v2"
for _p in (str(HERE), str(V2), str(V1)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import mex6v2_fitters as F  # noqa: E402  (V2, read-only)
import mex6v3_generator as G  # noqa: E402
from mex6_arms import ArmSpec, TYPED_SIGNS, _cap_typed, fit_signs  # noqa: E402  (V1, read-only)
from mex6_model import CHANNELS, FALL, FLAT, RISE, SCALES, VALIDATION_CHANNELS  # noqa: E402
from mex6_oracle import decidable_from_fit_window, oracle  # noqa: E402

STUDY_ID = "ME-X6-V3"
SCHEMA_DESIGN = "orion.v2.me-x6-v3.role-coverage-shift-design.v1"
SCHEMA_RESULTS = "orion.v2.me-x6-v3.role-coverage-shift-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x6-v3.role-coverage-shift-analysis.v1"
DESIGN_JSON = HERE / "ME_X6_V3_ROLE_COVERAGE_SHIFT_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
AUTH_USED = HERE / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json"
DEFAULT_SEED_FILE = Path.home() / ".orion-custody" / "me-x6-v3" / "PROTECTED_SEED_V1.txt"
RESULTS_DIR = HERE / "results"

DEV_SEED = "ME-X6-V3-DEV-20260904"
DEV_PER_CELL = 2                      # 36 cells x 2 = 72, the split the comparators are FITTED on
PROTECTED_PER_CELL = 50               # 36 cells x 50 = 1800

# ---- the frozen substrate (V1 generator/arms, V2 fitters and V2's frozen vector) ----
# Pinned so that every stage refuses on drift: a V3 verdict is only about V3's
# question if the thing V2 froze is the thing V3 reads.
V2_DESIGN_JSON = V2 / "ME_X6_V2_CAPACITY_MATCHED_COMPARATOR_DESIGN_V1.json"
V2_FIT_JSON = V2 / "results" / "ME_X6_V2_DEVELOPMENT_FIT_V1.json"
SUBSTRATE_PINS: dict[str, str] = {
    "me-x6/mex6_model.py": "c0a7298265eaf34bd496a32c74ed29fc3d60c415b295ec5cda669eda09d07d9b",
    "me-x6/mex6_generator.py": "9f510b54fe23c0e7c4413859fd981ca8486d16cf615a1273cc73ac38c80eb718",
    "me-x6/mex6_oracle.py": "1d539ed60ff578606b02a0def5b90b4b0896d4e15e40c5b714ae6ff7087f26d7",
    "me-x6/mex6_arms.py": "a72d7de2557495262a2f9999f3372078310c8da8ee792a16ed2fea7f5254ea04",
    "me-x6-v2/mex6v2_fitters.py": "021516be1ea28c3cd2c199e80f876bbc4bcb7f5474f1bbb4a038412ed2a9c359",
    "me-x6-v2/ME_X6_V2_CAPACITY_MATCHED_COMPARATOR_DESIGN_V1.json":
        "ce7942af1d36092dc24c3ab310f80a0b836be4171d5e11a51bffe129772fa3d7",
    "me-x6-v2/results/ME_X6_V2_DEVELOPMENT_FIT_V1.json":
        "d86060a438fc2cf001a8fe0e52839ab730402ea8fe7b3d305452751ec6ae9aef",
}

# ---- arms --------------------------------------------------------------------------
M_ARM = "M_TYPED_COLLECTIVE_STATE"
B8_V2_ARM = "B8_V2_FROZEN_COVERAGE_UNMATCHED"       # V2's exact frozen vector, no refit
REFIT_ARM = "B8_V3_REFIT_COVERAGE_MATCHED"          # V2's select_capacity_matched on the V3 dev split
GREEDY_V3_ARM = "B6_V3_GREEDY_SUBSET_UNTYPED"
L1_V3_ARM = "B7_V3_L1_PATH_UNTYPED"
UNIT_ARM = "B4X_V1_UNIT_SIGN_LEARNED_CONTROL"       # V1's fit_signs on the V3 dev split
B9_ARM = "B9_EXHAUSTIVE_UNTYPED_IDENTITY_CHECK"     # contains M's vector: a vacuity disclosure, not evidence
CONTROL_ARMS = ("C_ALWAYS_RISE", "C_ALWAYS_FLAT", "C_ALWAYS_FALL")
FITTED_ARMS = (REFIT_ARM, GREEDY_V3_ARM, L1_V3_ARM, UNIT_ARM, B9_ARM)
G8_ARMS = (M_ARM, B8_V2_ARM, REFIT_ARM, UNIT_ARM)

B9_WEIGHT_ORDER: tuple[int, ...] = (0, 1, -1, -2)   # class {-2,-1,0,+1}; tie order for B9's selection

HARD_GATES = ("G0a_KNOWN_ANSWER", "G0b_GENERATOR_VALIDITY", "G0c_NULL_CALIBRATION",
              "G0d_M_EXACT_BY_CONSTRUCTION_ON_V1_STRATA", "G0e_COVERAGE_AND_CAPACITY_BITS",
              "G8_VERDICT_CONSTANCY_WITHIN_CELL")
LIVE_GATES = ("G0d2_M_ON_HELD_OUT_ROLES", "G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4",
              "G2_M_VS_B8_V3_REFIT_ON_ALL_18", "G3_B8_V3_REFIT_VS_B8_V2_FROZEN_ON_HELD_OUT_4",
              "G6_CROSS_SCALE_CONSISTENCY")
TERMINALS = ("LANE_DEFECT", "NO_CROSS_SCALE_TRANSFER", "TYPING_IS_A_COVERAGE_PRIOR",
             "TYPING_LOAD_BEARING_BEYOND_COVERAGE", "TYPING_NOT_SEPARATED_UNDER_COVERAGE_SHIFT",
             "M_BEHIND_COMPARATOR", "NONE")

OPERATOR_INSTRUCTION_VERBATIM = (
    "for the negative results we need to find ways to improve our orion v2 framework, so we "
    "can also improve the quality of the paper in order to make sure they are all top tier."
)
OPERATOR_INSTRUCTION_SOURCE = "operator directive 2026-09-04, relayed via the interface-revival lane brief"


# ---- helpers -------------------------------------------------------------------------

def canonical_json(o) -> str:
    return json.dumps(o, indent=2, sort_keys=True, default=str)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def exact_binomial_two_sided(b: int, c: int) -> float:
    """Exact McNemar / discordant-pair sign test, two-sided, in exact integers."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def binom_upper_tail(k: int, n: int, p) -> float:
    """P(X >= k), Binomial(n, p), exact in rationals (the float form overflows at
    this n and would return inf, making a `p > alpha` gate incapable of failing)."""
    if n == 0:
        return 1.0
    k = max(0, min(k, n))
    q = Fraction(p).limit_denominator(10 ** 6)
    one_q = 1 - q
    tail = sum((Fraction(comb(n, i)) * q ** i * one_q ** (n - i) for i in range(k, n + 1)),
               Fraction(0))
    return min(1.0, max(0.0, tail.numerator / tail.denominator))


def substrate_drift() -> dict[str, dict[str, str]]:
    drift = {}
    for rel, want in SUBSTRATE_PINS.items():
        p = HERE.parent / rel
        got = sha256_file(p) if p.exists() else "ABSENT"
        if got != want:
            drift[rel] = {"pinned": want, "observed": got}
    return drift


def refuse_on_substrate_drift() -> None:
    d = substrate_drift()
    if d:
        raise SystemExit(f"REFUSED: the frozen V1/V2 substrate has drifted: {canonical_json(d)}")


def modal_class_rate(strata: dict[str, tuple[str, str]] = G.STRATA_V3) -> dict:
    """The DERIVABLE null bar (V2 receipt section 5b): an arm answering the modal
    capability class of the registered strata scores exactly this on a balanced
    split.  Computed from STRATA_V3, never written down."""
    counts = Counter(v[0] for v in strata.values())
    modal, k = counts.most_common(1)[0]
    return {"modal_class": modal, "modal_count": k, "n_strata": len(strata),
            "rate": k / len(strata), "class_counts": dict(counts)}


# ---- weight vectors ----------------------------------------------------------------

def m_vector() -> dict[str, int]:
    return {c: int(TYPED_SIGNS.get(c, 0)) for c in CHANNELS}


def frozen_b8_v2() -> dict:
    """V2's frozen B8 vector, read from V2's frozen design JSON and corroborated
    against V2's development-fit JSON.  Both files are sha256-pinned above; any
    disagreement between them, or with the pins, is refused."""
    refuse_on_substrate_drift()
    design = json.loads(V2_DESIGN_JSON.read_text())
    fit = json.loads(V2_FIT_JSON.read_text())
    wd = {k: int(v) for k, v in
          design["comparator"]["frozen_fitted_weights"]["B8_CAPACITY_MATCHED_BEST"]["weights"].items()}
    wf = {k: int(v) for k, v in fit["B8_CAPACITY_MATCHED_BEST"]["weights"].items()}
    if wd != wf:
        raise SystemExit("REFUSED: V2's design JSON and fit JSON disagree on B8's vector")
    return {"weights": {c: wd[c] for c in CHANNELS},
            "selected_fitter": design["comparator"]["selected_fitter"],
            "source_design_json": V2_DESIGN_JSON.name,
            "source_design_sha256": sha256_file(V2_DESIGN_JSON),
            "corroborated_by_fit_json": V2_FIT_JSON.name,
            "corroborated_by_fit_sha256": sha256_file(V2_FIT_JSON)}


def fit_b9_exhaustive(deltas, truths) -> dict:
    """Exhaustive enumeration over {-2,-1,0,+1}^8 on the eight validation channels.

    This class CONTAINS M's own vector, so its tie with M is an IDENTITY CHECK and
    not evidence (registered as such).  It is kept because it answers a different
    question: how many members of the class the development split leaves
    indistinguishable at the maximum -- i.e. whether 72 public instances pin the
    rule.  Deterministic selection among maximal vectors: fewest nonzeros, then
    lexicographically smallest index tuple in B9_WEIGHT_ORDER.
    """
    chans = VALIDATION_CHANNELS
    best_acc = -1
    maximal: list[tuple[int, ...]] = []
    for idx in product(range(len(B9_WEIGHT_ORDER)), repeat=len(chans)):
        w = {c: B9_WEIGHT_ORDER[i] for c, i in zip(chans, idx)}
        acc = F.accuracy(deltas, truths, w)
        if acc > best_acc:
            best_acc, maximal = acc, [idx]
        elif acc == best_acc:
            maximal.append(idx)
    chosen = min(maximal, key=lambda t: (sum(1 for i in t if i != 0), t))
    weights = {c: 0 for c in CHANNELS}
    weights.update({c: B9_WEIGHT_ORDER[i] for c, i in zip(chans, chosen)})
    m_idx = tuple(B9_WEIGHT_ORDER.index(TYPED_SIGNS[c]) for c in chans)
    return {"weights": weights, "dev_capability_correct": best_acc,
            "n_candidates": len(B9_WEIGHT_ORDER) ** len(chans),
            "n_maximal_vectors": len(maximal),
            "m_vector_is_maximal": m_idx in set(maximal),
            "chosen_equals_m_vector": chosen == m_idx,
            "label": "IDENTITY CHECK -- the class contains M's vector; a tie with M is not evidence"}


def dev_split():
    return G.generate_split_v3("dev", DEV_SEED, DEV_PER_CELL)


def deltas_truths(insts):
    return ([F.half_difference(i.window, CHANNELS) for i in insts],
            [oracle(i.window).capability for i in insts])


def fit_on_development(with_b9: bool = True) -> dict:
    """Every learned arm, fitted on the PUBLIC V3 development split.  Deterministic
    and RNG-free; the protected seed plays no part here and could not."""
    insts = dev_split()
    deltas, truths = deltas_truths(insts)
    sel = F.select_capacity_matched(deltas, truths, CHANNELS)
    out = {
        REFIT_ARM: {"weights": sel["B8_CAPACITY_MATCHED_BEST"]["weights"],
                    "selected_fitter": sel["B8_CAPACITY_MATCHED_BEST"]["selected_fitter"],
                    "dev_capability_correct": sel["B8_CAPACITY_MATCHED_BEST"]["dev_capability_correct"]},
        GREEDY_V3_ARM: {"weights": sel["B6_GREEDY_SUBSET_UNTYPED"]["weights"],
                        "dev_capability_correct": sel["B6_GREEDY_SUBSET_UNTYPED"]["dev_capability_correct"],
                        "trace": sel["B6_GREEDY_SUBSET_UNTYPED"]["trace"]},
        L1_V3_ARM: {"weights": sel["B7_L1_PATH_UNTYPED"]["weights"],
                    "dev_capability_correct": sel["B7_L1_PATH_UNTYPED"]["dev_capability_correct"]},
    }
    unit = fit_signs(insts, CHANNELS)
    out[UNIT_ARM] = {"weights": {c: int(unit.get(c, 0)) for c in CHANNELS},
                     "dev_capability_correct": F.accuracy(deltas, truths, unit)}
    if with_b9:
        out[B9_ARM] = fit_b9_exhaustive(deltas, truths)
    for a in out:
        out[a]["n_channels_zeroed"] = sum(1 for v in out[a]["weights"].values() if not v)
        out[a]["n_dev"] = len(truths)
    out["dev_seed"] = DEV_SEED
    out["dev_per_cell"] = DEV_PER_CELL
    out["n_dev"] = len(truths)
    out["selection_rule"] = sel["selection_rule"]
    return out


def frozen_fit() -> dict:
    d = json.loads(DESIGN_JSON.read_text())
    out = {}
    for arm, rec in d["comparators"]["frozen_fitted_weights"].items():
        out[arm] = {"weights": {k: float(v) for k, v in rec["weights"].items()},
                    "dev_capability_correct": rec.get("dev_capability_correct")}
    b8 = d["comparators"]["B8_V2_FROZEN"]
    out[B8_V2_ARM] = {"weights": {k: float(v) for k, v in b8["weights"].items()}}
    return out


def refit_reproduces() -> tuple[bool, dict]:
    committed = frozen_fit()
    live = fit_on_development(with_b9=True)
    live[B8_V2_ARM] = {"weights": frozen_b8_v2()["weights"]}
    drift = {}
    for arm in committed:
        cw = {k: float(v) for k, v in committed[arm]["weights"].items()}
        lw = {k: float(v) for k, v in live[arm]["weights"].items()}
        if any(abs(cw.get(k, 0.0) - lw.get(k, 0.0)) > 1e-9 for k in set(cw) | set(lw)):
            drift[arm] = {"committed": cw, "refit": lw}
    return (not drift), drift


# ---- arms ------------------------------------------------------------------------------

_M_SPEC = ArmSpec(M_ARM, CHANNELS, _cap_typed)
_M_RNG = random.Random(0)   # _cap_typed never draws from it; passed to honour V1's signature


def m_verdict(window) -> str:
    """M exactly as V1 computes it: `_cap_typed` over the FieldWindow (V1's `_dir_of`),
    NOT the untyped `direction_from_weights` path the comparators use.  The two
    paths are asserted to agree on M's vector in the selftest (an identity
    disclosure), and asserted to be different code (a VACUOUS_CONTRAST guard)."""
    return _cap_typed(window, _M_SPEC, _M_RNG)


def arm_table(frozen: dict) -> dict:
    arms = {M_ARM: ("window", m_verdict)}
    for a in (B8_V2_ARM, REFIT_ARM, GREEDY_V3_ARM, L1_V3_ARM, UNIT_ARM, B9_ARM):
        if a in frozen:
            arms[a] = ("delta", (lambda d, w=frozen[a]["weights"]: F.direction_from_weights(d, w)))
    for name, d in (("C_ALWAYS_RISE", RISE), ("C_ALWAYS_FLAT", FLAT), ("C_ALWAYS_FALL", FALL)):
        arms[name] = ("delta", (lambda _d, dd=d: dd))
    return arms


# ---- running ---------------------------------------------------------------------------

def split_digest(insts) -> str:
    """sha256 of the split's full content (channels AND latents), independent of arms."""
    rows = [{"instance_id": i.instance_id, "stratum": i.stratum, "scale": i.scale,
             "periods": [{"index": p.index, "latent": dict(p.latent), "channels": dict(p.channels)}
                         for p in i.window.periods]} for i in insts]
    return sha256_text(canonical_json(rows))


def run_instances(instances, label: str, frozen: dict) -> tuple[dict, dict]:
    arms = arm_table(frozen)
    rows, custody = [], []
    for inst in instances:
        w = inst.window
        delta = F.half_difference(w, CHANNELS)
        truth = oracle(w).capability
        ok, why = G.planter_agrees_v3(w, inst.stratum)
        ok2, why2 = G.channel_signature_agrees(w, inst.stratum)
        custody.append({"instance_id": inst.instance_id, "stratum": inst.stratum,
                        "scale": inst.scale, "planter_agrees": ok, "planter_reason": why,
                        "channel_signature_agrees": ok2, "channel_signature_reason": why2,
                        "decidable_from_fit_window": decidable_from_fit_window(w),
                        "expected_capability": truth})
        verdicts = {}
        for name, (kind, fn) in arms.items():
            verdicts[name] = fn(w) if kind == "window" else fn(delta)
        rows.append({"instance_id": inst.instance_id, "stratum": inst.stratum,
                     "scale": inst.scale, "expected_capability": truth, "arms": verdicts})
    res = {"schema_version": SCHEMA_RESULTS, "label": label, "n_instances": len(rows),
           "arms": sorted(arms), "split_digest": split_digest(instances),
           "frozen_weights": {a: frozen[a]["weights"] for a in frozen if "weights" in frozen[a]},
           "instances": rows}
    cus = {"schema_version": SCHEMA_RESULTS + ".custody", "label": label, "instances": custody}
    return res, cus


# ---- scoring ---------------------------------------------------------------------------

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
            "strata": [r["stratum"] for r in rows], "scales": [r["scale"] for r in rows], "n": n}


def _subset_idx(sc: dict, strata: tuple[str, ...] | None, scale: str | None) -> list[int]:
    return [i for i in range(sc["n"])
            if (strata is None or sc["strata"][i] in strata)
            and (scale is None or sc["scales"][i] == scale)]


def _verdict(cx: int, cy: int, x_wins: int, y_wins: int, discordant: int) -> str:
    if cx == cy and discordant == 0:
        return "TIE"
    if cx > cy and x_wins >= 1 and y_wins == 0:
        return "X_AHEAD"
    if cy > cx and y_wins >= 1 and x_wins == 0:
        return "Y_AHEAD"
    return "MIXED"


def compare(sc: dict, x: str, y: str, strata: tuple[str, ...] | None) -> dict:
    """x versus y, reported per scale, per stratum x scale, and pooled.  The pass
    verdict is decided PER SCALE and the two scales are never pooled into one
    claim: `overall` is the common per-scale verdict or SCALE_DISAGREEMENT."""
    vx, vy = sc["vec"][x], sc["vec"][y]
    out: dict = {"x": x, "y": y, "strata": list(strata) if strata else "ALL", "per_scale": {},
                 "per_cell": {}}
    for scl in SCALES:
        idx = _subset_idx(sc, strata, scl)
        if not idx:
            out["per_scale"][scl] = {"status": "CANNOT_CHECK_NO_INSTANCES", "n": 0}
            continue
        b = sum(1 for i in idx if vx[i] and not vy[i])
        c = sum(1 for i in idx if vy[i] and not vx[i])
        cx = sum(1 for i in idx if vx[i])
        cy = sum(1 for i in idx if vy[i])
        xw = yw = tie = 0
        strata_here = sorted({sc["strata"][i] for i in idx})
        for st in strata_here:
            key = f"{st}|{scl}"
            rec = sc["by_cell"][key]
            if rec[x] > rec[y]:
                xw += 1
            elif rec[y] > rec[x]:
                yw += 1
            else:
                tie += 1
            out["per_cell"][key] = {"x_correct": rec[x], "y_correct": rec[y], "n": rec["_n"],
                                    "x_only": sum(1 for i in idx if sc["strata"][i] == st and vx[i] and not vy[i]),
                                    "y_only": sum(1 for i in idx if sc["strata"][i] == st and vy[i] and not vx[i])}
            out["per_cell"][key]["exact_p_two_sided"] = exact_binomial_two_sided(
                out["per_cell"][key]["x_only"], out["per_cell"][key]["y_only"])
        out["per_scale"][scl] = {
            "status": "EVALUATED", "n": len(idx), "x_correct": cx, "y_correct": cy,
            "x_only": b, "y_only": c, "discordant": b + c,
            "exact_p_two_sided": exact_binomial_two_sided(b, c),
            "cells": {"n": len(strata_here), "x_wins": xw, "y_wins": yw, "ties": tie},
            "verdict": _verdict(cx, cy, xw, yw, b + c)}
    idx = _subset_idx(sc, strata, None)
    b = sum(1 for i in idx if vx[i] and not vy[i])
    c = sum(1 for i in idx if vy[i] and not vx[i])
    out["pooled_for_display_only"] = {
        "n": len(idx), "x_correct": sum(1 for i in idx if vx[i]),
        "y_correct": sum(1 for i in idx if vy[i]), "x_only": b, "y_only": c,
        "discordant": b + c, "exact_p_two_sided": exact_binomial_two_sided(b, c),
        "note": "pooled across scales for display; no clause reads this"}
    verdicts = {v.get("verdict") for v in out["per_scale"].values() if v.get("status") == "EVALUATED"}
    if len(out["per_scale"]) < len(SCALES) or any(v.get("status") != "EVALUATED" for v in out["per_scale"].values()):
        out["overall"] = "CANNOT_CHECK"
    elif len(verdicts) == 1:
        out["overall"] = verdicts.pop()
    else:
        out["overall"] = "SCALE_DISAGREEMENT"
    return out


# ---- gates -------------------------------------------------------------------------------
# Every gate is a POSITIVE test carrying its own n_evaluated.  A gate with
# n_evaluated == 0 reports CANNOT_CHECK and never a pass.  No terminal is the
# negation of another gate.

def gates(sc: dict, res: dict, cus: dict, selftest_ok: bool | None, selftest_meta: dict | None,
          registered_gates: tuple[str, ...] | None = None) -> dict:
    g: dict[str, dict] = {}
    n = sc["n"]
    pa = sc["per_arm"]
    vec = sc["vec"]
    meta = selftest_meta or {}
    held = G.HELD_OUT_STRATA
    v1s = G.V1_STRATA

    g["G0a_KNOWN_ANSWER"] = {
        "pass": selftest_ok,
        "n_evaluated": int(meta.get("n_checks", 0)) if selftest_ok is not None else 0,
        "status": "EVALUATED" if selftest_ok is not None else "CANNOT_CHECK_NO_SELFTEST_REPORT",
        "rule": "every selftest fixture reproduces; the denominator is READ from the report"}

    pl = sum(1 for c in cus["instances"] if c["planter_agrees"])
    dec = sum(1 for c in cus["instances"] if c["decidable_from_fit_window"])
    sig = sum(1 for c in cus["instances"] if c["channel_signature_agrees"])
    g["G0b_GENERATOR_VALIDITY"] = {
        "pass": (pl == n and dec == n and sig == n) if n else None, "n_evaluated": n,
        "planter_agree": {"ok": pl, "n": n},
        "decidable_from_fit_window": {"ok": dec, "n": n},
        "declared_channel_signature_on_new_strata": {"ok": sig, "n": n,
                                                     "n_new_stratum_instances": sum(1 for c in cus["instances"] if c["stratum"] in held)},
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "the planter's DECLARED (capability, activity) effect equals the full-structure "
                "recomputation on every instance; every holdout direction is already carried by "
                "its fit window; every new-stratum instance moves exactly its declared channels"}

    bar = modal_class_rate()
    best = max(pa[a]["capability_rate"] for a in CONTROL_ARMS)
    p_ctrl = binom_upper_tail(max(pa[a]["capability_correct"] for a in CONTROL_ARMS), n,
                              Fraction(1, 3)) if n else 1.0
    g["G0c_NULL_CALIBRATION"] = {
        "pass": (best <= bar["rate"] + 1e-12) if n else None, "n_evaluated": n,
        "best_control_rate": best, "derivable_bar_modal_class_rate": bar["rate"],
        "bar_derivation": bar,
        "controls": {a: pa[a]["capability_rate"] for a in CONTROL_ARMS},
        "exact_upper_tail_vs_uniform_third": p_ctrl,
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "no constant arm EXCEEDS the modal-class rate computed from STRATA_V3 (V2 receipt "
                "5b: the derivable bar, not a hand-set constant); a constant arm above it means a "
                "stratum is planted off its declaration"}

    idx_v1 = _subset_idx(sc, v1s, None)
    m_v1 = sum(1 for i in idx_v1 if vec[M_ARM][i])
    g["G0d_M_EXACT_BY_CONSTRUCTION_ON_V1_STRATA"] = {
        "pass": (m_v1 == len(idx_v1)) if idx_v1 else None, "n_evaluated": len(idx_v1),
        "m_correct": m_v1,
        "status": "EVALUATED" if idx_v1 else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "on the 14 V1 strata M reproduces the oracle on every instance, as V1 design 1.3 "
                "declares.  VALIDITY, not contrast: a failure here is generator drift.  The four "
                "NEW strata are deliberately excluded -- M's a-priori sign may be wrong there and "
                "that is a result (G0d2), not a defect"}

    fw = res["frozen_weights"]
    w2 = fw[B8_V2_ARM]
    zeroed_roles = tuple(r for r in G.LONE_CARRIER.values() for _ in [0])  # keep order of held-out strata
    zeroed_roles = tuple(G.LONE_CARRIER[s][0] for s in held)
    b8_zero_set = {c for c, v in w2.items() if not float(v)}
    refit_zeros = sum(1 for v in fw[REFIT_ARM].values() if not float(v))
    g["G0e_COVERAGE_AND_CAPACITY_BITS"] = {
        "pass": (all(r in b8_zero_set for r in zeroed_roles)
                 and all(float(w2[c]) != 0 for c in ("formal_artifacts", "replications_passed",
                                                      "retractions", "independent_rederivations"))
                 and len(b8_zero_set) == 12),
        "n_evaluated": len(w2),
        "b8_v2_frozen_n_channels_zeroed": len(b8_zero_set), "n_channels": len(w2),
        "b8_v2_frozen_zeroes_the_four_held_out_roles": {r: (r in b8_zero_set) for r in zeroed_roles},
        "b8_v3_refit_n_channels_zeroed": refit_zeros,
        "unit_sign_control_n_channels_zeroed": sum(1 for v in fw[UNIT_ARM].values() if not float(v)),
        "rule": "READ from the vector: V2's frozen B8 zeroes exactly the four roles the held-out "
                "strata carry (the coverage-UNMATCHED premise) and 12 of 16 channels in all "
                "(the capacity-matched premise); if either is false the contrast is empty"}

    # G0d2 -- M on the held-out roles.  LIVE, not hard: an a-priori sign error is a
    # genuine M failure and must be allowed to happen (routes M_BEHIND_COMPARATOR via G2).
    per = {}
    for st in held:
        for scl in SCALES:
            rec = sc["by_cell"].get(f"{st}|{scl}")
            if rec:
                per[f"{st}|{scl}"] = {"m_correct": rec[M_ARM], "n": rec["_n"]}
    idx_h = _subset_idx(sc, held, None)
    m_h = sum(1 for i in idx_h if vec[M_ARM][i])
    g["G0d2_M_ON_HELD_OUT_ROLES"] = {
        "pass": (m_h == len(idx_h)) if idx_h else None, "n_evaluated": len(idx_h),
        "m_correct": m_h, "per_cell": per,
        "status": "EVALUATED" if idx_h else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "M's a-priori TYPED_SIGNS return the declared capability on every instance of the "
                "four new strata.  A measurement: the signs were fixed in V1 before these strata "
                "existed and the strata's effects were derived from protocol semantics, not from M"}

    c1 = compare(sc, M_ARM, B8_V2_ARM, held)
    g["G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4"] = {
        "pass": c1["overall"] == "X_AHEAD", "verdict": c1["overall"],
        "n_evaluated": c1["pooled_for_display_only"]["n"], "comparison": c1,
        "status": "EVALUATED" if c1["overall"] != "CANNOT_CHECK" else "CANNOT_CHECK",
        "disclosure": "the comparator half of this contrast is STRUCTURALLY DETERMINED: the held-out "
                      "strata move only channels B8_V2 zeroes, so B8_V2 reads FLAT on every one of "
                      "them BY CONSTRUCTION (that is what coverage-unmatched means operationally). "
                      "What G1 measures is M's side -- whether the a-priori signs carry roles the "
                      "fitter never saw exercised.  Read with G3, which shows what coverage alone buys",
        "rule": "at EACH scale separately: M's held-out accuracy exceeds B8_V2's, M wins >= 1 held-out "
                "cell and loses none; exact discordant-pair test reported per scale and per stratum"}

    c2 = compare(sc, M_ARM, REFIT_ARM, None)
    g["G2_M_VS_B8_V3_REFIT_ON_ALL_18"] = {
        "pass": c2["overall"] in ("X_AHEAD", "TIE"), "verdict": c2["overall"],
        "n_evaluated": c2["pooled_for_display_only"]["n"], "comparison": c2,
        "status": "EVALUATED" if c2["overall"] != "CANNOT_CHECK" else "CANNOT_CHECK",
        "refit_vector_equals_m_vector": _same_vector(fw[REFIT_ARM], fw[M_ARM] if M_ARM in fw else m_vector()),
        "refit_sign_pattern_equals_m": _same_signs(fw[REFIT_ARM], m_vector()),
        "rule": "at EACH scale separately: TIE (equal totals AND zero discordant pairs) means "
                "capacity + coverage suffice; M AHEAD (wins cells, loses none) means the fitter "
                "heuristics cannot learn the full rule; REFIT AHEAD routes M_BEHIND_COMPARATOR"}

    c3 = compare(sc, REFIT_ARM, B8_V2_ARM, held)
    g["G3_B8_V3_REFIT_VS_B8_V2_FROZEN_ON_HELD_OUT_4"] = {
        "pass": c3["overall"] == "X_AHEAD", "verdict": c3["overall"],
        "n_evaluated": c3["pooled_for_display_only"]["n"], "comparison": c3,
        "status": "EVALUATED" if c3["overall"] != "CANNOT_CHECK" else "CANNOT_CHECK",
        "rule": "at EACH scale separately: the coverage-matched refit is ahead of the coverage-"
                "unmatched frozen vector on the held-out strata -- attributes a G1 separation to "
                "COVERAGE (the fitter learns the roles once it sees them) rather than to typing"}

    per_scale_signs = {}
    consistent = True
    for tag, cmp in (("M_minus_B8_V2", c1), ("M_minus_REFIT", c2)):
        s = {}
        for scl in SCALES:
            rec = cmp["per_scale"][scl]
            if rec.get("status") != "EVALUATED":
                s[scl] = None
                continue
            d = rec["x_correct"] - rec["y_correct"]
            s[scl] = (d > 0) - (d < 0)
        per_scale_signs[tag] = s
        vals = set(s.values())
        if None in vals or len(vals) != 1:
            consistent = False
    g["G6_CROSS_SCALE_CONSISTENCY"] = {
        "pass": consistent, "n_evaluated": n, "per_scale_signs": per_scale_signs,
        "status": "EVALUATED" if n else "CANNOT_CHECK_NO_INSTANCES",
        "rule": "the sign of (M - comparator) is the same at both units of analysis, for both "
                "comparators; a result at one scale only is not a result here"}

    flips = 0
    checked = 0
    flip_cells = []
    for key, rec in sc["by_cell"].items():
        checked += 1
        for a in G8_ARMS:
            if 0 < rec[a] < rec["_n"]:
                flips += 1
                flip_cells.append(f"{key}:{a}")
    g["G8_VERDICT_CONSTANCY_WITHIN_CELL"] = {
        "pass": (flips == 0) if checked else None, "n_evaluated": checked, "n_cells": checked,
        "flips": flips, "flip_cells": flip_cells, "arms": list(G8_ARMS),
        "status": "EVALUATED" if checked else "CANNOT_CHECK_NO_CELLS",
        "rule": "for M, both comparators and the unit-sign control, every instance of a cell "
                "receives the same verdict"}

    g["COVERAGE_LEDGER"] = {
        "all_registered_cells_exercised": len(sc["by_cell"]) == len(G.CELLS_V3),
        "n_cells_exercised": len(sc["by_cell"]), "n_cells_registered": len(G.CELLS_V3),
        "never_exercised": sorted(f"{s}|{sc_}" for s, sc_ in G.CELLS_V3
                                  if f"{s}|{sc_}" not in sc["by_cell"])}
    evaluated = tuple(k for k in g if k not in ("COVERAGE_LEDGER",))
    reg = registered_gates if registered_gates is not None else HARD_GATES + LIVE_GATES
    g["SCOPE_BINDING"] = {
        "registered": sorted(reg), "evaluated": sorted(evaluated),
        "equal": sorted(reg) == sorted(evaluated),
        "rule": "REGISTERED_SCOPE_DIVERGENCE guard: the gates evaluated are exactly the gates the "
                "frozen design registers; a narrower or wider evaluation is a lane defect"}
    g["ROUTE"] = route(g)
    return g


def _same_vector(a: dict, b: dict) -> bool:
    return all(abs(float(a.get(c, 0)) - float(b.get(c, 0))) < 1e-9 for c in CHANNELS)


def _same_signs(a: dict, b: dict) -> bool:
    sg = lambda v: (float(v) > 0) - (float(v) < 0)  # noqa: E731
    return all(sg(a.get(c, 0)) == sg(b.get(c, 0)) for c in CHANNELS)


def route(g: dict) -> dict:
    """Registered precedence.  LANE_DEFECT (any hard gate, coverage or scope) ->
    NO_CROSS_SCALE_TRANSFER (G6) -> TYPING_IS_A_COVERAGE_PRIOR -> TYPING_LOAD_BEARING_
    BEYOND_COVERAGE -> TYPING_NOT_SEPARATED_UNDER_COVERAGE_SHIFT -> M_BEHIND_COMPARATOR
    -> NONE.  The G1-tie terminal additionally requires that no comparator is
    strictly ahead of M, so a tie on the held-out strata produced by M being WRONG
    there cannot be reported as 'not separated' while the refit is ahead (that
    would be TERMINAL_OVERSTATES_ITS_PROCEDURE); it then routes M_BEHIND_COMPARATOR."""
    for h in HARD_GATES:
        if g[h].get("pass") is not True:
            return {"route": "CANNOT_CHECK", "terminal": "LANE_DEFECT",
                    "reason": f"hard gate {h} did not pass -- repair, re-freeze, no arm verdict"}
    if not g["COVERAGE_LEDGER"]["all_registered_cells_exercised"]:
        return {"route": "CANNOT_CHECK", "terminal": "LANE_DEFECT",
                "reason": "not every registered cell was exercised"}
    if not g.get("SCOPE_BINDING", {}).get("equal", True):
        return {"route": "CANNOT_CHECK", "terminal": "LANE_DEFECT",
                "reason": "REGISTERED_SCOPE_DIVERGENCE: evaluated gates != registered gates"}
    g1 = g["G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4"]["verdict"]
    g2 = g["G2_M_VS_B8_V3_REFIT_ON_ALL_18"]["verdict"]
    g3 = g["G3_B8_V3_REFIT_VS_B8_V2_FROZEN_ON_HELD_OUT_4"]["verdict"]
    if g["G6_CROSS_SCALE_CONSISTENCY"].get("pass") is not True:
        return {"route": "CANNOT_CHECK", "terminal": "NO_CROSS_SCALE_TRANSFER",
                "reason": "the sign of (M - comparator) differs between the two units of analysis"}
    comparator_ahead = (g2 == "Y_AHEAD") or (g1 == "Y_AHEAD")
    if g1 == "X_AHEAD" and g2 == "TIE" and g3 == "X_AHEAD":
        return {"route": "PARENT_SUFFICIENT_AT_FULL_COVERAGE",
                "terminal": "TYPING_IS_A_COVERAGE_PRIOR",
                "reason": "M is ahead of the coverage-unmatched frozen comparator on the held-out "
                          "roles; the coverage-matched refit ties M everywhere and is itself ahead "
                          "of the frozen vector on the held-out roles.  The a-priori typed "
                          "assignment buys exactly what development coverage would have bought: "
                          "robustness to roles the fitter never saw exercised, and nothing at full "
                          "coverage"}
    if g1 == "X_AHEAD" and g2 == "X_AHEAD":
        return {"route": "TYPED_STATE_SEPARATES_AT_MATCHED_CAPACITY_AND_COVERAGE",
                "terminal": "TYPING_LOAD_BEARING_BEYOND_COVERAGE",
                "reason": "M is ahead of the frozen comparator on the held-out roles AND ahead of "
                          "the coverage-matched refit at both scales: the registered fitting "
                          "heuristics cannot learn the full rule even when every role is exercised"}
    if g1 == "TIE" and not comparator_ahead:
        return {"route": "PARENT_SUFFICIENT",
                "terminal": "TYPING_NOT_SEPARATED_UNDER_COVERAGE_SHIFT",
                "reason": "M and the coverage-unmatched frozen comparator agree on every held-out "
                          "instance at both scales; typing did not carry the unexercised roles"}
    if comparator_ahead:
        return {"route": "COMPARATOR_AHEAD", "terminal": "M_BEHIND_COMPARATOR",
                "reason": "a comparator is strictly ahead of M at both scales (wins cells, loses "
                          "none): M's a-priori sign is wrong somewhere the comparator is right"}
    return {"route": "CANNOT_CHECK", "terminal": "NONE",
            "reason": f"no registered clause holds as registered (G1={g1}, G2={g2}, G3={g3}): "
                      "arms differ in total but not consistently by cell, so no representational "
                      "reading is supported"}


# ---- the role-coverage census and the controls ---------------------------------------------

def role_coverage_census(insts) -> dict:
    """From GENERATED V1-stratum instances: which validation channels move in which
    strata, and which have a lone-carrier stratum.  This is the premise of the
    study, recomputed rather than quoted."""
    movers: dict[str, set] = {c: set() for c in VALIDATION_CHANNELS}
    alone: dict[str, set] = {c: set() for c in VALIDATION_CHANNELS}
    for i in insts:
        if i.stratum not in G.V1_STRATA:
            continue
        mv = G.validation_movers(i.window)
        for c in mv:
            movers[c].add(i.stratum)
        if len(mv) == 1:
            alone[mv[0]].add(i.stratum)
    no_lone = tuple(c for c in VALIDATION_CHANNELS if not alone[c])
    b8 = frozen_b8_v2()["weights"]
    b8_zeroed_validation = tuple(c for c in VALIDATION_CHANNELS if not b8[c])
    m_roles = tuple(c for c in VALIDATION_CHANNELS if TYPED_SIGNS.get(c, 0))
    return {"moves_in": {c: sorted(movers[c]) for c in VALIDATION_CHANNELS},
            "lone_carrier_in": {c: sorted(alone[c]) for c in VALIDATION_CHANNELS},
            "channels_with_no_lone_carrier_v1_stratum": list(no_lone),
            "b8_v2_zeroed_validation_channels": list(b8_zeroed_validation),
            "m_declared_roles": list(m_roles),
            # The premise, stated exactly: every channel B8_V2 zeroed is a channel no V1
            # stratum exercises alone; the four held-out strata are those channels; and
            # the ONLY channel without a lone V1 carrier that B8_V2 did NOT zero is
            # `retractions` (kept because I4 is decided by it -- see the note below).
            "premise_holds": set(b8_zeroed_validation) <= set(no_lone)
            and set(b8_zeroed_validation) == set(G.LONE_CARRIER[s][0] for s in G.HELD_OUT_STRATA)
            and set(no_lone) - set(b8_zeroed_validation) == {"retractions"},
            "retractions_note": "retractions has no strictly-lone V1 stratum either (corrections "
                                "co-moves x1 against its x3 inside I4), but B8_V2 kept it because "
                                "I4 is decided by it; it is counted as covered, as the brief records"}


def controls_on_dev(fit: dict) -> dict:
    """Every zero this study asserts is paired with a control that MOVES the counter
    in the same run."""
    insts = dev_split()
    deltas, truths = deltas_truths(insts)
    held_idx = [k for k, i in enumerate(insts) if i.stratum in G.HELD_OUT_STRATA]
    hd = [deltas[k] for k in held_idx]
    ht = [truths[k] for k in held_idx]
    b8 = frozen_b8_v2()["weights"]
    mv = m_vector()
    # 1. B8_V2 on the held-out strata: FLAT everywhere by construction ... and un-zeroing
    #    the four roles with M's signs restores them (the counter moves).
    b8_held = F.accuracy(hd, ht, b8)
    b8_flat = sum(1 for d in hd if F.direction_from_weights(d, b8) == FLAT)
    unzeroed = dict(b8)
    for s in G.HELD_OUT_STRATA:
        c = G.LONE_CARRIER[s][0]
        unzeroed[c] = mv[c]
    unz_held = F.accuracy(hd, ht, unzeroed)
    # 2. M with ONE a-priori sign flipped loses exactly that role's stratum.
    flips = {}
    for s in G.HELD_OUT_STRATA:
        c = G.LONE_CARRIER[s][0]
        bad = dict(mv)
        bad[c] = -mv[c]
        lost = sorted({insts[k].stratum for k in range(len(insts))
                       if F.direction_from_weights(deltas[k], bad) != truths[k]})
        flips[c] = {"flipped_to": bad[c], "strata_lost": lost, "n_lost": sum(
            1 for k in range(len(insts)) if F.direction_from_weights(deltas[k], bad) != truths[k])}
    # 3. M via V1's typed code path == M via the untyped rule (identity disclosure), and
    #    the comparators' vectors differ from M's (VACUOUS_CONTRAST guard).
    m_typed = [m_verdict(i.window) for i in insts]
    m_untyped = [F.direction_from_weights(d, mv) for d in deltas]
    return {
        "b8_v2_on_held_out_dev": {"correct": b8_held, "n": len(ht), "reads_FLAT": b8_flat,
                                  "note": "FLAT by construction -- disclosed, see G1"},
        "b8_v2_unzeroed_with_m_signs_on_held_out_dev": {"correct": unz_held, "n": len(ht),
                                                        "counter_moved": unz_held > b8_held},
        "m_single_sign_flip_controls": flips,
        "m_typed_path_equals_untyped_rule_on_dev": {"agree": sum(1 for a, b in zip(m_typed, m_untyped) if a == b),
                                                     "n": len(insts)},
        "vectors_differ_from_m": {a: (not _same_vector(fit[a]["weights"], mv))
                                  for a in (REFIT_ARM, GREEDY_V3_ARM, L1_V3_ARM, UNIT_ARM, B9_ARM) if a in fit},
        "b8_v2_differs_from_m": not _same_vector(b8, mv),
        "sign_pattern_equals_m": {a: _same_signs(fit[a]["weights"], mv)
                                  for a in (REFIT_ARM, GREEDY_V3_ARM, L1_V3_ARM, B9_ARM) if a in fit},
    }


def reachability_audit(fit: dict) -> dict:
    """Can every registered clause be satisfied, and can it fail?  Run before the
    protected split exists; anything unreachable is relabelled here as a pre-outcome
    correction."""
    insts = dev_split()
    deltas, truths = deltas_truths(insts)
    ctl = controls_on_dev(fit)
    mv = m_vector()
    fixtures = {
        "LANE_DEFECT": route(_gateset(G0e_COVERAGE_AND_CAPACITY_BITS=False))["terminal"],
        "NO_CROSS_SCALE_TRANSFER": route(_gateset(G6_CROSS_SCALE_CONSISTENCY=False))["terminal"],
        "TYPING_IS_A_COVERAGE_PRIOR": route(_gateset(G1="X_AHEAD", G2="TIE", G3="X_AHEAD"))["terminal"],
        "TYPING_LOAD_BEARING_BEYOND_COVERAGE": route(_gateset(G1="X_AHEAD", G2="X_AHEAD", G3="X_AHEAD"))["terminal"],
        "TYPING_NOT_SEPARATED_UNDER_COVERAGE_SHIFT": route(_gateset(G1="TIE", G2="TIE", G3="TIE"))["terminal"],
        "M_BEHIND_COMPARATOR": route(_gateset(G1="X_AHEAD", G2="Y_AHEAD", G3="X_AHEAD"))["terminal"],
        "M_BEHIND_COMPARATOR_via_G1_tie_with_refit_ahead": route(_gateset(G1="TIE", G2="Y_AHEAD", G3="X_AHEAD"))["terminal"],
        "NONE": route(_gateset(G1="X_AHEAD", G2="MIXED", G3="X_AHEAD"))["terminal"],
    }
    return {
        "G1_comparator_half_is_structurally_determined": {
            "statement": "The held-out strata move only channels B8_V2 zeroes, so B8_V2 reads FLAT "
                         "on every held-out instance BY CONSTRUCTION.  This is disclosed as the "
                         "operational meaning of 'coverage-unmatched', not as a finding.  G1's "
                         "measured content is M's side (G0d2); G3 attributes what coverage buys.",
            "b8_v2_held_out_dev": ctl["b8_v2_on_held_out_dev"],
            "counter_moves_when_unzeroed": ctl["b8_v2_unzeroed_with_m_signs_on_held_out_dev"]},
        "M_can_fail_on_a_new_stratum": {
            "statement": "M's signs were fixed in V1; each new stratum's effect was derived from "
                         "protocol semantics.  A single flipped sign loses exactly that role's "
                         "stratum, so an a-priori error would be visible and would route "
                         "M_BEHIND_COMPARATOR through G2 rather than be hidden by a hard gate.",
            "single_sign_flip_controls": ctl["m_single_sign_flip_controls"],
            "m_on_dev_all_strata": {"correct": F.accuracy(deltas, truths, mv), "n": len(truths)}},
        "the_refit_can_lose_and_can_win": {
            "greedy_v3_dev": fit[GREEDY_V3_ARM]["dev_capability_correct"],
            "l1_v3_dev": fit[L1_V3_ARM]["dev_capability_correct"],
            "refit_dev": fit[REFIT_ARM]["dev_capability_correct"], "n": fit["n_dev"],
            "unit_sign_control_dev": fit[UNIT_ARM]["dev_capability_correct"],
            "statement": "both registered fitters are heuristics (V2 fixtures re-asserted in the "
                         "selftest); whichever B8_V3_REFIT is, it is not M's vector unless the "
                         "analysis flags refit_vector_equals_m_vector, in which case a G2 tie is an "
                         "identity and is reported as one"},
        "refit_vector_equals_m_vector": _same_vector(fit[REFIT_ARM]["weights"], mv),
        "refit_sign_pattern_equals_m": _same_signs(fit[REFIT_ARM]["weights"], mv),
        "B9_is_an_identity_check": {
            "statement": "the exhaustive class contains M's vector; its tie with M is a vacuity "
                         "disclosure, never evidence.  Reported only for what it measures: how "
                         "many class members the development split leaves maximal",
            "n_maximal_vectors": fit[B9_ARM]["n_maximal_vectors"],
            "m_vector_is_maximal": fit[B9_ARM]["m_vector_is_maximal"],
            "chosen_equals_m_vector": fit[B9_ARM]["chosen_equals_m_vector"]},
        "the_activity_half_is_not_reported": {
            "statement": "V1 computes the activity direction from the activity channels by the "
                         "same call for every arm; it is equal by construction and not evidence"},
        "the_protected_seed_governs_instance_generation_only": {
            "statement": "every fit is a deterministic, RNG-free function of the PUBLIC "
                         "development split, frozen before the protected seed is revealed"},
        "null_bar_is_derived_not_hand_set": modal_class_rate(),
        "every_terminal_is_reachable_by_fixture": fixtures,
        "every_terminal_reached": all(v == k.split("_via_")[0] for k, v in fixtures.items()),
        "vacuous_contrast_guard": {"m_typed_path_equals_untyped_rule": ctl["m_typed_path_equals_untyped_rule_on_dev"],
                                   "comparator_vectors_differ_from_m": ctl["vectors_differ_from_m"],
                                   "b8_v2_differs_from_m": ctl["b8_v2_differs_from_m"],
                                   "sign_pattern_equals_m": ctl["sign_pattern_equals_m"]},
    }


def _gateset(G1: str = "X_AHEAD", G2: str = "TIE", G3: str = "X_AHEAD", **over) -> dict:
    g = {k: {"pass": True} for k in HARD_GATES}
    g["G0d2_M_ON_HELD_OUT_ROLES"] = {"pass": True}
    g["G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4"] = {"pass": G1 == "X_AHEAD", "verdict": G1}
    g["G2_M_VS_B8_V3_REFIT_ON_ALL_18"] = {"pass": G2 in ("X_AHEAD", "TIE"), "verdict": G2}
    g["G3_B8_V3_REFIT_VS_B8_V2_FROZEN_ON_HELD_OUT_4"] = {"pass": G3 == "X_AHEAD", "verdict": G3}
    g["G6_CROSS_SCALE_CONSISTENCY"] = {"pass": True}
    g["COVERAGE_LEDGER"] = {"all_registered_cells_exercised": True}
    g["SCOPE_BINDING"] = {"equal": True}
    for k, v in over.items():
        g[k] = {"pass": v}
    return g


# ---- reproducibility guard -------------------------------------------------------------------

def digest_in_subprocess(seed: str, per_cell: int, hashseed: str, prefix: str) -> str:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = hashseed
    out = subprocess.run([sys.executable, str(Path(__file__).resolve()), "digest",
                          "--seed-literal", seed, "--per-cell", str(per_cell), "--prefix", prefix],
                         env=env, capture_output=True, text=True, check=True)
    return out.stdout.strip().split()[-1]


# ---- selftest ----------------------------------------------------------------------------------

def stage_selftest(out_dir: Path) -> int:
    import mex6v2_run as R2  # V2's own can-fail fixtures, read-only
    refuse_on_substrate_drift()
    checks: list[dict] = []

    checks.append({"check": "direction_rule",
                   "pass": (F.direction_from_weights({"a": 3}, {"a": 1}) == RISE
                            and F.direction_from_weights({"a": 3}, {"a": -1}) == FALL
                            and F.direction_from_weights({"a": 3}, {"a": 0}) == FLAT)})
    gf = R2.greedy_can_fail_fixture()
    checks.append({"check": "greedy_forward_selection_can_fail", "pass": gf["greedy_is_suboptimal"],
                   "detail": {k: gf[k] for k in ("greedy_correct", "exhaustive_best_correct", "n")}})
    lf = R2.l1_can_fail_fixture()
    checks.append({"check": "l1_path_can_fail", "pass": lf["l1_is_suboptimal"],
                   "detail": {k: lf[k] for k in ("l1_correct", "hidden_rule_correct", "n")}})

    insts = dev_split()
    checks.append({"check": "planter_agrees_on_every_dev_instance",
                   "pass": all(G.planter_agrees_v3(i.window, i.stratum)[0] for i in insts), "n": len(insts)})
    checks.append({"check": "decidable_from_fit_window_on_every_dev_instance",
                   "pass": all(decidable_from_fit_window(i.window) for i in insts), "n": len(insts)})
    checks.append({"check": "declared_channel_signature_on_every_new_stratum_dev_instance",
                   "pass": all(G.channel_signature_agrees(i.window, i.stratum)[0] for i in insts),
                   "n": sum(1 for i in insts if i.stratum in G.HELD_OUT_STRATA)})
    checks.append({"check": "all_registered_cells_generated",
                   "pass": len({(i.stratum, i.scale) for i in insts}) == len(G.CELLS_V3), "n": len(G.CELLS_V3)})

    # the planter REJECTS a mis-declared effect (the check can fail)
    rejected = 0
    for i in insts:
        other = next(s for s in G.STRATA_V3 if G.STRATA_V3[s] != G.STRATA_V3[i.stratum])
        rejected += 0 if G.planter_agrees_v3(i.window, other)[0] else 1
    checks.append({"check": "planter_rejects_a_different_declared_effect", "pass": rejected == len(insts),
                   "n": len(insts), "rejected": rejected})
    bad_sig = sum(1 for i in insts if i.stratum in G.HELD_OUT_STRATA
                  and not G.channel_signature_agrees(i.window, next(
                      s for s in G.HELD_OUT_STRATA if s != i.stratum))[0])
    checks.append({"check": "channel_signature_check_rejects_another_new_stratum_signature",
                   "pass": bad_sig == sum(1 for i in insts if i.stratum in G.HELD_OUT_STRATA), "rejected": bad_sig})

    # V3 delegates V1 strata to V1's generator byte-for-byte
    from mex6_generator import generate_split as v1_generate_split
    v1 = v1_generate_split("dev", DEV_SEED, DEV_PER_CELL)
    v3v1 = [i for i in insts if i.stratum in G.V1_STRATA]
    checks.append({"check": "v3_generator_reproduces_v1_generator_on_v1_strata",
                   "pass": len(v1) == len(v3v1) and all(a.window == b.window and a.instance_id == b.instance_id
                                                        for a, b in zip(v1, v3v1)), "n": len(v1)})

    census = role_coverage_census(insts)
    checks.append({"check": "role_coverage_census_premise_holds", "pass": census["premise_holds"],
                   "detail": {k: census[k] for k in ("channels_with_no_lone_carrier_v1_stratum",
                                                     "b8_v2_zeroed_validation_channels")}})

    fit = fit_on_development(with_b9=True)
    ctl = controls_on_dev(fit)
    n_held = ctl["b8_v2_on_held_out_dev"]["n"]
    checks.append({"check": "b8_v2_reads_FLAT_on_every_held_out_dev_instance_BY_CONSTRUCTION_disclosed",
                   "pass": ctl["b8_v2_on_held_out_dev"]["reads_FLAT"] == n_held, "n": n_held})
    checks.append({"check": "unzeroing_the_four_roles_moves_the_counter",
                   "pass": ctl["b8_v2_unzeroed_with_m_signs_on_held_out_dev"]["counter_moved"],
                   "detail": ctl["b8_v2_unzeroed_with_m_signs_on_held_out_dev"]})
    checks.append({"check": "each_single_sign_flip_of_M_loses_exactly_its_role_stratum",
                   "pass": all(v["strata_lost"] == [s] for s, v in
                               ((s, ctl["m_single_sign_flip_controls"][G.LONE_CARRIER[s][0]]) for s in G.HELD_OUT_STRATA)),
                   "detail": ctl["m_single_sign_flip_controls"]})
    checks.append({"check": "m_typed_code_path_equals_untyped_rule_on_M_vector_identity_disclosure",
                   "pass": ctl["m_typed_path_equals_untyped_rule_on_dev"]["agree"] == len(insts), "n": len(insts)})
    checks.append({"check": "vacuous_contrast_guard_comparator_vectors_differ_from_M",
                   "pass": ctl["b8_v2_differs_from_m"] and all(ctl["vectors_differ_from_m"][a] for a in (REFIT_ARM, UNIT_ARM)),
                   "detail": ctl["vectors_differ_from_m"]})
    checks.append({"check": "m_verdict_and_direction_from_weights_are_different_code",
                   "pass": m_verdict.__code__ is not F.direction_from_weights.__code__
                   and _cap_typed.__module__ == "mex6_arms" and F.direction_from_weights.__module__ == "mex6v2_fitters"})

    bar = modal_class_rate()
    checks.append({"check": "null_bar_is_the_modal_class_rate_of_STRATA_V3", "pass": abs(bar["rate"] - 8 / 18) < 1e-12,
                   "detail": bar})
    src = Path(__file__).read_text()
    # The literal is assembled so this line cannot match itself; the check reads the
    # runner's source for V2's hand-set constant (V2 receipt section 5b).
    hand_set_literal = "0." + "60"
    checks.append({"check": "no_hand_set_null_constant_in_runner", "pass": hand_set_literal not in src,
                   "literal_searched": hand_set_literal})
    # G0c can fail: a synthetic per-arm table with a constant arm above the bar
    fake_sc = {"n": 18, "per_arm": {a: {"capability_rate": 0.0, "capability_correct": 0} for a in CONTROL_ARMS}}
    fake_sc["per_arm"]["C_ALWAYS_FLAT"] = {"capability_rate": 0.5, "capability_correct": 9}
    best = max(fake_sc["per_arm"][a]["capability_rate"] for a in CONTROL_ARMS)
    checks.append({"check": "G0c_fails_when_a_constant_arm_exceeds_the_derivable_bar",
                   "pass": not (best <= bar["rate"] + 1e-12)})

    tail = binom_upper_tail(1200, PROTECTED_PER_CELL * len(G.CELLS_V3), Fraction(1, 3))
    checks.append({"check": "exact_tail_finite_at_protected_scale", "pass": 0.0 <= tail <= 1.0, "value": tail})

    audit = reachability_audit(fit)
    checks.append({"check": "every_terminal_reachable_by_fixture", "pass": audit["every_terminal_reached"],
                   "detail": audit["every_terminal_is_reachable_by_fixture"]})
    # the fitter can fail in fact on THIS split: at least one registered fitter is below ceiling
    checks.append({"check": "at_least_one_registered_fitter_is_below_ceiling_on_the_v3_dev_split",
                   "pass": min(fit[GREEDY_V3_ARM]["dev_capability_correct"], fit[L1_V3_ARM]["dev_capability_correct"]) < fit["n_dev"],
                   "detail": {"greedy": fit[GREEDY_V3_ARM]["dev_capability_correct"],
                              "l1": fit[L1_V3_ARM]["dev_capability_correct"], "n": fit["n_dev"]}})
    checks.append({"check": "B9_class_contains_M_vector_identity_disclosure",
                   "pass": fit[B9_ARM]["m_vector_is_maximal"], "detail": {k: fit[B9_ARM][k] for k in
                                                                          ("n_maximal_vectors", "chosen_equals_m_vector", "n_candidates")}})

    # NONREPRODUCIBLE_FROZEN_ARTIFACT guard on the dev split: two fresh processes under two
    # hash seeds that both differ from this process's and from each other.
    d1 = digest_in_subprocess(DEV_SEED, DEV_PER_CELL, "1", "dev")
    d2 = digest_in_subprocess(DEV_SEED, DEV_PER_CELL, "12345", "dev")
    d0 = split_digest(insts)
    checks.append({"check": "dev_split_digest_identical_across_PYTHONHASHSEED_1_and_12345_and_parent",
                   "pass": d0 == d1 == d2, "digests": {"parent": d0, "hashseed_1": d1, "hashseed_12345": d2}})

    passed = all(c["pass"] for c in checks)
    rep = {"schema_version": SCHEMA_RESULTS + ".selftest", "passed": passed, "n_checks": len(checks),
           "checks": checks, "role_coverage_census": census, "controls_on_dev": ctl,
           "reachability_audit": audit, "substrate_pins": SUBSTRATE_PINS, "python": sys.version}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X6_V3_SELFTEST_REPORT.json").write_text(canonical_json(rep))
    print(f"selftest: {sum(1 for c in checks if c['pass'])}/{len(checks)} checks pass")
    for c in checks:
        if not c["pass"]:
            print(f"  FAIL {c['check']}")
    return 0 if passed else 1


# ---- stages -------------------------------------------------------------------------------------

def stage_fit(out_dir: Path) -> int:
    refuse_on_substrate_drift()
    fit = fit_on_development(with_b9=True)
    fit["B8_V2_FROZEN"] = frozen_b8_v2()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X6_V3_DEVELOPMENT_FIT_V1.json").write_text(canonical_json(fit))
    for arm in FITTED_ARMS:
        w = fit[arm]["weights"]
        print(f"{arm}: dev {fit[arm]['dev_capability_correct']}/{fit['n_dev']}, zeros {fit[arm]['n_channels_zeroed']}/{len(w)}")
        print(f"   {({k: (round(v, 6) if isinstance(v, float) else v) for k, v in w.items() if v})}")
    print(f"{REFIT_ARM}: selected {fit[REFIT_ARM]['selected_fitter']}")
    return 0


def stage_freeze(out_dir: Path, seed_file: Path) -> int:
    """Write the design JSON exactly once.  Requires the custody seed to exist so its
    commitment can be published BEFORE any protected instance is generated."""
    if DESIGN_JSON.exists():
        print(f"REFUSED: {DESIGN_JSON.name} already exists; a frozen design is not rewritten", file=sys.stderr)
        return 6
    refuse_on_substrate_drift()
    if not seed_file.exists():
        print(f"REFUSED: custody seed absent ({seed_file}); the commitment must be published in the design", file=sys.stderr)
        return 4
    seed = seed_file.read_bytes().strip()
    commit = hashlib.sha256(seed).hexdigest()
    fit = fit_on_development(with_b9=True)
    b8v2 = frozen_b8_v2()
    insts = dev_split()
    census = role_coverage_census(insts)
    audit = reachability_audit(fit)
    design = {
        "schema_version": SCHEMA_DESIGN, "study_id": STUDY_ID,
        "title": "Is the a-priori typed assignment load-bearing under ROLE-COVERAGE SHIFT?",
        "question": ("V2 attributed V1's separation to comparator capacity: a learned capacity-matched "
                     "untyped vector ties M 1400/1400.  That vector zeroes exactly the four of M's eight "
                     "declared roles that no V1 stratum exercises as a lone carrier, so the fitter dropped "
                     "roles the development split never exercised in isolation.  On strata that exercise "
                     "those roles alone, does the a-priori typed assignment separate from (a) V2's frozen "
                     "coverage-UNMATCHED vector and (b) the same fitter refitted on a coverage-MATCHED "
                     "development split?"),
        "predecessors": {
            "ME-X6": {"status": "IMMUTABLE -- not edited, not re-run", "role": "generator, oracle, M, fit_signs"},
            "ME-X6-V2": {"status": "IMMUTABLE -- not edited, not re-run", "role": "fitters, B8 frozen vector, custody conventions",
                         "terminal_as_receipted": "TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY"}},
        "substrate_pins_sha256": SUBSTRATE_PINS,
        "strata": {
            "v1_strata": {s: list(G.STRATA[s]) for s in G.V1_STRATA},
            "new_strata": {s: {"capability": G.NEW_STRATA[s][0], "activity": G.NEW_STRATA[s][1],
                               "lone_carrier": G.LONE_CARRIER[s][0], "carrier_direction": G.LONE_CARRIER[s][1],
                               "declared_channel_signature": G.declared_channel_signature(s)} for s in G.HELD_OUT_STRATA},
            "held_out_4": list(G.HELD_OUT_STRATA),
            "role_lone_carrier_stratum": G.ROLE_LONE_CARRIER_STRATUM,
            "n_strata": len(G.STRATA_V3), "n_cells": len(G.CELLS_V3),
            "generator": "mex6v3_generator.py: V1 strata via V1's build_window unchanged; new strata draw in V1's order"},
        "role_coverage_census_from_generated_instances": census,
        "comparators": {
            "M_TYPED_COLLECTIVE_STATE": "V1's _cap_typed over TYPED_SIGNS, imported unchanged; computed on the FieldWindow by V1's own code path",
            "B8_V2_FROZEN": b8v2,
            "B8_V3_REFIT": {"procedure": "V2's select_capacity_matched (B6 greedy, B7 lasso, frozen selection rule) on the V3 development split",
                            "fitted_on": {"split": "PUBLIC DEVELOPMENT", "seed": DEV_SEED, "per_cell": DEV_PER_CELL, "n": fit["n_dev"]},
                            "selected_fitter": fit[REFIT_ARM]["selected_fitter"]},
            "B4X_V1_UNIT_SIGN_LEARNED_CONTROL": "V1's fit_signs on the V3 development split (class {-1,0,+1})",
            "B9_EXHAUSTIVE_UNTYPED_IDENTITY_CHECK": {
                "class": "{-2,-1,0,+1}^8 over the eight validation channels, exhaustive",
                "label": "IDENTITY CHECK, NOT EVIDENCE: the class contains M's vector, so a tie with M is a vacuity disclosure",
                "reported_for": "how many class members the development split leaves maximal (identifiability of the rule from 72 public instances)",
                "n_candidates": fit[B9_ARM]["n_candidates"], "n_maximal_vectors": fit[B9_ARM]["n_maximal_vectors"],
                "m_vector_is_maximal": fit[B9_ARM]["m_vector_is_maximal"], "chosen_equals_m_vector": fit[B9_ARM]["chosen_equals_m_vector"]},
            "C_ALWAYS_RISE/FLAT/FALL": "null controls",
            "frozen_fitted_weights": {a: {"weights": fit[a]["weights"], "dev_capability_correct": fit[a]["dev_capability_correct"],
                                          "n_channels_zeroed": fit[a]["n_channels_zeroed"], "n_dev": fit["n_dev"]}
                                      for a in FITTED_ARMS},
            "provenance": "CONSTRUCTED_FOR_THIS_STUDY; NOT PUBLISHED-METHOD PARENTS (V2 design section 2 applies unchanged)",
            "handicap_disclosure": ("B8_V2_FROZEN is deliberately coverage-UNMATCHED: that is the manipulated variable, "
                                    "not a harness asymmetry.  B8_V3_REFIT is the parity arm that removes the handicap; "
                                    "G3 measures what removing it buys (HANDICAPPED_COMPARATOR guard)")},
        "scored_half": {"capability": "SCORED", "activity": "NOT SCORED AND NOT REPORTED (equal by construction, V1 provenance receipt section 3)"},
        "protected_split": {"cells": len(G.CELLS_V3), "per_cell": PROTECTED_PER_CELL,
                            "n": len(G.CELLS_V3) * PROTECTED_PER_CELL, "prefix": "protected",
                            "reporting": "per stratum, per scale, and the held-out-4 subset separately; the two scales are never pooled into one claim"},
        "gates": {"hard": list(HARD_GATES), "live": list(LIVE_GATES),
                  "null_bar": {"rule": "no constant arm exceeds the modal-class rate computed from STRATA_V3", **modal_class_rate()},
                  "paired_test": "exact two-sided discordant-pair (McNemar) binomial test, per scale and per stratum",
                  "note": ("every gate is a POSITIVE test with its own n_evaluated; G0d2 is LIVE not hard so an a-priori "
                           "sign error of M on a new stratum is a result, not a lane defect")},
        "terminals": {
            "LANE_DEFECT": "any hard gate, coverage or scope binding fails -> route CANNOT_CHECK",
            "NO_CROSS_SCALE_TRANSFER": "G6 fails -> route CANNOT_CHECK",
            "TYPING_IS_A_COVERAGE_PRIOR": "G1 M ahead AND G2 tie AND G3 refit ahead, at both scales -> route PARENT_SUFFICIENT_AT_FULL_COVERAGE",
            "TYPING_LOAD_BEARING_BEYOND_COVERAGE": "G1 M ahead AND G2 M ahead, at both scales",
            "TYPING_NOT_SEPARATED_UNDER_COVERAGE_SHIFT": "G1 tie at both scales AND no comparator strictly ahead of M -> route PARENT_SUFFICIENT",
            "M_BEHIND_COMPARATOR": "any comparator strictly ahead of M at both scales (wins cells, loses none)",
            "NONE": "no clause holds as registered (mixed by cell) -> route CANNOT_CHECK",
            "precedence": "LANE_DEFECT > NO_CROSS_SCALE_TRANSFER > TYPING_IS_A_COVERAGE_PRIOR > TYPING_LOAD_BEARING_BEYOND_COVERAGE > TYPING_NOT_SEPARATED_UNDER_COVERAGE_SHIFT > M_BEHIND_COMPARATOR > NONE",
            "pre_outcome_correction": ("the G1-tie terminal requires that no comparator is strictly ahead of M; a held-out tie "
                                       "produced by M being WRONG on the new strata routes M_BEHIND_COMPARATOR, not 'not separated' "
                                       "(TERMINAL_OVERSTATES_ITS_PROCEDURE guard)")},
        "reachability_audit_pre_run": audit,
        "failure_ledger_audit": {
            "VACUOUS_CONTRAST": "M runs V1's typed code path on the window; comparators run V2's untyped rule on half-differences; vectors asserted to differ; the M-vector identity between the two paths is disclosed",
            "STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE": "G1's comparator half is determined by construction and is disclosed as such; G1's measured content is M's side (G0d2, which can fail) and G3 attributes coverage; G2 is open in both directions (greedy 64/72 vs lasso 72/72 on dev shows the fitter class can lose)",
            "HANDICAPPED_COMPARATOR": "the coverage handicap is the manipulated variable; the parity arm B8_V3_REFIT is registered and G3 reads it",
            "NONREPRODUCIBLE_FROZEN_ARTIFACT": "no RNG draw ordered by an unordered container (CELLS_V3 is a tuple; per-instance seeds are sha256-derived); split digests compared across PYTHONHASHSEED 1 and 12345 in fresh processes, dev at selftest and protected after the run",
            "REGISTERED_SCOPE_DIVERGENCE": "SCOPE_BINDING gate: the gate set evaluated must equal the gate set registered here; every clause is evaluated at BOTH scales separately",
            "TERMINAL_OVERSTATES_ITS_PROCEDURE": "each terminal names the gate verdicts that would have to be otherwise for it to be false; the G1-tie terminal cannot fire while a comparator is ahead",
            "CHECK_THAT_RUNS_AND_CANNOT_FIRE": "every hard gate has a selftest fixture or control on which it fails (planter rejection, signature rejection, G0c above-bar fixture, un-zeroing counter, sign-flip controls)",
            "RENDERED_SURFACE_SUBSTITUTED_FOR_THE_FACT": "every number in the receipt is parsed from a results/analysis JSON; pytest exit status read from $? with no pipe",
            "FORECLOSED_FAILURE_MODE": "M's failure mode (a wrong a-priori sign) has dynamic range: single-sign-flip controls lose exactly one stratum each",
            "AUTHORITY_LAUNDERING": "grants nothing; see authority"},
        "seed_commitment": {"protected_seed_sha256": commit, "revealed": False,
                            "note": f"custody file {seed_file}; the seed value is revealed in the outcome receipt AFTER the run"},
        "protected_run_authorization": {"operator_instruction_verbatim": OPERATOR_INSTRUCTION_VERBATIM,
                                        "source": OPERATOR_INSTRUCTION_SOURCE,
                                        "guard": "PROTECTED_RUN_AUTHORIZATION.json with human_written=true, token >= 16 chars, acknowledged_design_sha256 == this file's digest (else exit 3); custody seed must hash to the commitment (else exit 4); archived after use"},
        "out_of_scope": ["re-running ME-X6 V1 or V2", "re-fitting any V1/V2 frozen vector",
                         "any change to a V1/V2 gate, number, terminal or authorization",
                         "writing anything into research/experiments/me-x6/ or me-x6-v2/"],
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_manuscript_change": False, "flagship_gate": False},
    }
    DESIGN_JSON.write_text(canonical_json(design))
    print(f"frozen design: {DESIGN_JSON.name} sha256 {sha256_file(DESIGN_JSON)}")
    print(f"seed commitment: {commit}")
    return 0


def _run_split(label: str, prefix: str, seed: str, per_cell: int, out_dir: Path) -> int:
    if not DESIGN_JSON.exists():
        print(f"REFUSED: frozen design absent ({DESIGN_JSON.name})", file=sys.stderr)
        return 5
    refuse_on_substrate_drift()
    ok, drift = refit_reproduces()
    if not ok:
        print(f"REFUSED: the frozen comparator weights no longer reproduce: {canonical_json(drift)}", file=sys.stderr)
        return 5
    frozen = frozen_fit()
    insts = G.generate_split_v3(prefix, seed, per_cell)
    res, cus = run_instances(insts, label, frozen)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X6_V3_{label}_RESULTS_V1.json"
    cp = out_dir / f"ME_X6_V3_{label}_EXPECTED_CUSTODY_V1.json"
    rp.write_text(canonical_json(res))
    cp.write_text(canonical_json(cus))
    print(f"{label}: {len(insts)} instances, split digest {res['split_digest']}, results sha256 "
          f"{sha256_file(rp)}, custody sha256 {sha256_file(cp)}")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_cell: int) -> int:
    if per_cell * len(G.CELLS_V3) > 72:
        print("the development split is capped at 72 instances", file=sys.stderr)
        return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_cell, out_dir)


def stage_protected(out_dir: Path, per_cell: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent -- protected run not authorized", file=sys.stderr)
        return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization file unreadable: {exc}", file=sys.stderr)
        return 3
    token = str(auth.get("human_written_token", "")).strip()
    if auth.get("human_written") is not True or len(token) < 16:
        print("REFUSED: authorization requires human_written=true and a human_written_token (>= 16 chars)", file=sys.stderr)
        return 3
    if auth.get("acknowledged_design_sha256") != sha256_file(DESIGN_JSON):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr)
        return 3
    if auth.get("operator_instruction_verbatim") != OPERATOR_INSTRUCTION_VERBATIM:
        print("REFUSED: the authorization does not quote the operator instruction verbatim", file=sys.stderr)
        return 3
    if not seed_file.exists():
        print(f"REFUSED: custody seed file absent ({seed_file})", file=sys.stderr)
        return 4
    seed = seed_file.read_bytes().strip()
    commit = json.loads(DESIGN_JSON.read_text())["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed).hexdigest() != commit:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr)
        return 4
    rc = _run_split("PROTECTED", "protected", seed.decode(), per_cell, out_dir)
    if rc == 0:
        used = dict(auth)
        used.update({"consumed": True, "archive_after_use": True, "per_cell": per_cell,
                     "revealed_protected_seed": seed.decode(),
                     "revealed_protected_seed_sha256": hashlib.sha256(seed).hexdigest(),
                     "note": ("Consumed by the ME-X6-V3 protected run and archived here so the guard is re-armed: "
                              "PROTECTED_RUN_AUTHORIZATION.json no longer exists, and stage_protected refuses "
                              "with exit 3 until a new one is written.")})
        AUTH_USED.write_text(canonical_json(used))
        AUTH_FILE.unlink()
        print(f"authorization archived to {AUTH_USED.name}; live file deleted")
    return rc


def stage_digest(seed: str, per_cell: int, prefix: str) -> int:
    insts = G.generate_split_v3(prefix, seed, per_cell)
    print(f"digest n={len(insts)} PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED', 'unset')} {split_digest(insts)}")
    return 0


def stage_analyze(rp: Path, cp: Path, out_dir: Path, label: str | None = None,
                  selftest_report: Path | None = None) -> int:
    res = json.loads(rp.read_text())
    cus = json.loads(cp.read_text())
    label = label or res.get("label", "UNKNOWN")
    sp = selftest_report or (out_dir / "ME_X6_V3_SELFTEST_REPORT.json")
    selftest_ok, meta = None, None
    if sp.exists():
        rep = json.loads(sp.read_text())
        selftest_ok = bool(rep.get("passed"))
        meta = {"n_checks": rep.get("n_checks", 0)}
    registered = None
    if DESIGN_JSON.exists():
        d = json.loads(DESIGN_JSON.read_text())
        registered = tuple(d["gates"]["hard"]) + tuple(d["gates"]["live"])
    sc = score(res)
    gt = gates(sc, res, cus, selftest_ok, meta, registered)
    held = G.HELD_OUT_STRATA
    per_scale = {}
    for scl in SCALES:
        idx = _subset_idx(sc, None, scl)
        idx_h = _subset_idx(sc, held, scl)
        per_scale[scl] = {a: {"all_18": {"correct": sum(1 for i in idx if sc["vec"][a][i]), "n": len(idx)},
                              "held_out_4": {"correct": sum(1 for i in idx_h if sc["vec"][a][i]), "n": len(idx_h)}}
                          for a in res["arms"]}
    idx_h = _subset_idx(sc, held, None)
    held_out = {a: {"correct": sum(1 for i in idx_h if sc["vec"][a][i]), "n": len(idx_h)} for a in res["arms"]}
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label,
                "results_sha256": sha256_file(rp), "custody_sha256": sha256_file(cp),
                "split_digest": res.get("split_digest"),
                "design_sha256": sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else None,
                "n_instances": sc["n"], "score": {"per_arm": sc["per_arm"]},
                "per_scale": per_scale, "held_out_4_pooled_for_display": held_out,
                "by_cell": sc["by_cell"], "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X6_V3_{label}_ANALYSIS_V1.json").write_text(canonical_json(analysis))
    (out_dir / f"ME_X6_V3_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    r = gt["ROUTE"]
    print(f"{label} route: {r['route']}; terminal: {r['terminal']}")
    for a in (M_ARM, B8_V2_ARM, REFIT_ARM, UNIT_ARM):
        print(f"  {a}: {sc['per_arm'][a]['capability_correct']}/{sc['n']}  held-out-4 {held_out[a]['correct']}/{held_out[a]['n']}")
    return 0


def render_md(a: dict) -> str:
    g = a["gates"]
    pa = a["score"]["per_arm"]
    L = [f"# ME-X6 V3 {a['label']} analysis", "",
         f"- instances: {a['n_instances']}",
         f"- route: `{g['ROUTE']['route']}` — terminal `{g['ROUTE']['terminal']}`",
         f"- reason: {g['ROUTE']['reason']}", "",
         "Only the CAPABILITY half is scored (the activity half is equal by construction).", "",
         "## Gates", "", "| gate | pass | verdict | n_evaluated |", "|---|---|---|---|"]
    for k, v in g.items():
        if k in ("ROUTE", "COVERAGE_LEDGER", "SCOPE_BINDING"):
            continue
        L.append(f"| `{k}` | {v.get('pass')} | {v.get('verdict', '')} | {v.get('n_evaluated')} |")
    L += ["", "## Arms (capability), per scale", "",
          "| arm | all-18 SUBFIELD | all-18 PROBLEM_FAMILY | held-out-4 SUBFIELD | held-out-4 PROBLEM_FAMILY | pooled |",
          "|---|---|---|---|---|---|"]
    ps = a["per_scale"]
    for k, v in sorted(pa.items(), key=lambda x: -x[1]["capability_rate"]):
        s1, s2 = ps["SCALE_SUBFIELD"][k], ps["SCALE_PROBLEM_FAMILY"][k]
        L.append(f"| `{k}` | {s1['all_18']['correct']}/{s1['all_18']['n']} | {s2['all_18']['correct']}/{s2['all_18']['n']} | "
                 f"{s1['held_out_4']['correct']}/{s1['held_out_4']['n']} | {s2['held_out_4']['correct']}/{s2['held_out_4']['n']} | "
                 f"{v['capability_correct']}/{v['n_evaluated']} |")
    cl = g["COVERAGE_LEDGER"]
    L += ["", "## Coverage", "",
          f"- cells exercised: {cl['n_cells_exercised']} / {cl['n_cells_registered']}",
          f"- never exercised: {cl['never_exercised'] or 'none'}",
          f"- scope binding equal: {g['SCOPE_BINDING']['equal']}", ""]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "fit", "freeze", "dev", "protected", "digest", "analyze"))
    ap.add_argument("--out", type=Path, default=RESULTS_DIR)
    ap.add_argument("--per-cell", type=int, default=None)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--seed-literal", type=str, default=None)
    ap.add_argument("--prefix", type=str, default="protected")
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "fit":
        return stage_fit(a.out)
    if a.stage == "freeze":
        return stage_freeze(a.out, a.seed_file)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_cell or DEV_PER_CELL)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_cell or PROTECTED_PER_CELL, a.seed_file)
    if a.stage == "digest":
        seed = a.seed_literal if a.seed_literal is not None else a.seed_file.read_bytes().strip().decode()
        return stage_digest(seed, a.per_cell or PROTECTED_PER_CELL, a.prefix)
    if not a.results or not a.custody:
        print("analyze needs --results and --custody", file=sys.stderr)
        return 2
    return stage_analyze(a.results, a.custody, a.out, None, a.selftest_report)


if __name__ == "__main__":
    sys.exit(main())
