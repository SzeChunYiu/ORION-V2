#!/usr/bin/env python3
"""ME-X6 V4 — the coverage-LIMITED regime: how much is the typed prior worth, as a function of coverage?

Revival backlog #308 row R2a.  V3 terminated `TYPING_IS_A_COVERAGE_PRIOR`: with full role coverage on
the development split an untyped capacity-matched learner ties M 1800/1800, and V2's frozen vector
fails 0/400 on the four roles it never saw exercised.  Attributed stage: **regime** — at full
coverage the prior cannot show.  V4 registers DOMAINS with limited coverage at fit time and measures
the typed-vs-untyped contrast on every stratum, exercised and unexercised, at five coverage levels.

Registered domains D_k, k in (0, 2, 4, 6, 8): the ten non-carrier V1 strata plus the first k of the
eight lone-carrier strata in the registered role order (G.ROLE_LONE_CARRIER_STRATUM).  D_8 is V3's
full coverage and its refit is V3's frozen refit (known answer).  For each domain the untyped
comparators (V2's `select_capacity_matched`, V1's `fit_signs`) are fitted on that domain's PUBLIC
development split only; M is V1's typed rule, unchanged.  The protected population contains every
stratum, so for domain D_k the eight carrier strata split into EXERCISED (in D_k) and UNEXERCISED.

Pre-registered expectation: on exercised strata the untyped refit ties M (0 discordant, both scales)
— live, it can fail either way; on unexercised carrier strata M is ahead — the coverage gap; the
advantage M − B8_Dk is non-increasing in k and zero at k = 8.  Terminal vocabulary:
  TYPING_VALUE_EQUALS_COVERAGE_GAP        (expected; the prior is worth exactly the coverage gap)
  TYPING_SEPARATES_BEYOND_COVERAGE        (M ahead on an EXERCISED stratum: a residual beyond coverage)
  UNTYPED_RECOVERS_UNEXERCISED__CORRECTED (an untyped refit ties M on a stratum it never saw: the
                                           coverage-gap reading of V3 is corrected)
  LANE_DEFECT
Stages: selftest | fit | dev | protected | analyze.  V1/V2/V3 modules imported READ-ONLY.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from collections import Counter
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "me-x6"
V2 = HERE.parent / "me-x6-v2"
V3 = HERE.parent / "me-x6-v3"
for _p in (str(HERE), str(V3), str(V2), str(V1)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import mex6v2_fitters as F  # noqa: E402  (V2, read-only)
import mex6v3_generator as G  # noqa: E402  (V3, read-only)
from mex6_arms import ArmSpec, TYPED_SIGNS, _cap_typed, fit_signs  # noqa: E402  (V1, read-only)
from mex6_model import CHANNELS, FALL, FLAT, RISE, SCALES  # noqa: E402
from mex6_oracle import decidable_from_fit_window, oracle  # noqa: E402

STUDY_ID = "ME-X6-V4"
SCHEMA_RESULTS = "orion.v2.me-x6-v4.coverage-limited-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x6-v4.coverage-limited-analysis.v1"
DESIGN_JSON = HERE / "ME_X6_V4_COVERAGE_LIMITED_REGIME_DESIGN_V1.json"
FIT_JSON = HERE / "ME_X6_V4_DEVELOPMENT_FIT_V1.json"
V3_DESIGN_JSON = V3 / "ME_X6_V3_ROLE_COVERAGE_SHIFT_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
AUTH_USED = HERE / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json"
DEFAULT_SEED_FILE = Path(os.environ.get("MEX6V4_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody" / "me-x6-v4" / "PROTECTED_SEED_V1.txt")))
RESULTS_DIR = HERE / "results"

DEV_SEED = "ME-X6-V3-DEV-20260904"       # V3's public development seed: D_8's fit must reproduce V3's frozen refit
DEV_PER_CELL = 2
PROTECTED_PER_CELL = 50                  # 18 strata x 2 scales x 50 = 1800
COVERAGE_LEVELS = (0, 2, 4, 6, 8)

CARRIER_STRATA: tuple[str, ...] = tuple(G.ROLE_LONE_CARRIER_STRATUM.values())      # registered role order
CARRIER_ROLE: dict[str, str] = {s: r for r, s in G.ROLE_LONE_CARRIER_STRATUM.items()}
NON_CARRIER_STRATA: tuple[str, ...] = tuple(s for s in G.STRATA_V3 if s not in CARRIER_STRATA)
assert len(CARRIER_STRATA) == 8 and len(NON_CARRIER_STRATA) == 10


def domain(k: int) -> tuple[str, ...]:
    return NON_CARRIER_STRATA + CARRIER_STRATA[:k]


M_ARM = "M_TYPED_COLLECTIVE_STATE"
def refit_arm(k: int) -> str: return f"B8_D{k}_REFIT_COVERAGE_{k}_OF_8"
def unit_arm(k: int) -> str: return f"B4X_D{k}_UNIT_SIGN_COVERAGE_{k}_OF_8"
CONTROL_ARMS = ("C_ALWAYS_RISE", "C_ALWAYS_FLAT", "C_ALWAYS_FALL")
TERMINALS = ("TYPING_VALUE_EQUALS_COVERAGE_GAP", "TYPING_SEPARATES_BEYOND_COVERAGE", "UNTYPED_RECOVERS_UNEXERCISED__CORRECTED", "LANE_DEFECT")


def canonical_json(o) -> str:
    return json.dumps(o, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, j) for j in range(k + 1)) / 2 ** n)


# ---- fitting -------------------------------------------------------------------------------

_M_SPEC = ArmSpec(M_ARM, CHANNELS, _cap_typed)
_M_RNG = random.Random(0)


def m_verdict(window) -> str:
    return _cap_typed(window, _M_SPEC, _M_RNG)


def fit_on_development() -> dict:
    """Every learned arm, per registered domain, fitted on the PUBLIC development split restricted
    to that domain's strata.  Deterministic; the protected seed plays no part."""
    out: dict = {"dev_seed": DEV_SEED, "dev_per_cell": DEV_PER_CELL, "domains": {}}
    for k in COVERAGE_LEVELS:
        insts = G.generate_split_v3("dev", DEV_SEED, DEV_PER_CELL, strata=domain(k))
        deltas = [F.half_difference(i.window, CHANNELS) for i in insts]
        truths = [oracle(i.window).capability for i in insts]
        sel = F.select_capacity_matched(deltas, truths, CHANNELS)
        unit = fit_signs(insts, CHANNELS)
        w8 = {c: float(sel["B8_CAPACITY_MATCHED_BEST"]["weights"].get(c, 0.0)) for c in CHANNELS}
        wu = {c: float(unit.get(c, 0)) for c in CHANNELS}
        out["domains"][str(k)] = {
            "strata": list(domain(k)), "n_dev": len(truths),
            "exercised_carriers": list(CARRIER_STRATA[:k]), "unexercised_carriers": list(CARRIER_STRATA[k:]),
            refit_arm(k): {"weights": w8, "selected_fitter": sel["B8_CAPACITY_MATCHED_BEST"]["selected_fitter"],
                           "dev_capability_correct": sel["B8_CAPACITY_MATCHED_BEST"]["dev_capability_correct"],
                           "zeroed_unexercised_roles": [CARRIER_ROLE[s] for s in CARRIER_STRATA[k:] if w8[CARRIER_ROLE[s]] == 0.0],
                           "nonzero_unexercised_roles": [CARRIER_ROLE[s] for s in CARRIER_STRATA[k:] if w8[CARRIER_ROLE[s]] != 0.0]},
            unit_arm(k): {"weights": wu, "dev_capability_correct": F.accuracy(deltas, truths, unit)},
        }
    return out


def frozen_fit() -> dict:
    return json.loads(FIT_JSON.read_text())


def v3_known_answer(fit: dict) -> dict:
    """D_8's refit must equal V3's frozen `B8_V3_REFIT_COVERAGE_MATCHED` vector (same public seed, same
    strata, same fitter): the known-answer gate of this lane."""
    v3 = json.loads(V3_DESIGN_JSON.read_text())["comparators"]["frozen_fitted_weights"]["B8_V3_REFIT_COVERAGE_MATCHED"]["weights"]
    mine = fit["domains"]["8"][refit_arm(8)]["weights"]
    drift = {c: (float(v3.get(c, 0.0)), mine[c]) for c in CHANNELS if abs(float(v3.get(c, 0.0)) - mine[c]) > 1e-9}
    return {"pass": not drift, "drift": drift, "v3_design_sha256": sha256_file(V3_DESIGN_JSON)}


# ---- running -------------------------------------------------------------------------------

def arm_table(fit: dict) -> dict:
    arms: dict = {M_ARM: ("window", m_verdict)}
    for k in COVERAGE_LEVELS:
        d = fit["domains"][str(k)]
        arms[refit_arm(k)] = ("delta", (lambda dl, w=d[refit_arm(k)]["weights"]: F.direction_from_weights(dl, w)))
        arms[unit_arm(k)] = ("delta", (lambda dl, w=d[unit_arm(k)]["weights"]: F.direction_from_weights(dl, w)))
    for name, dd in (("C_ALWAYS_RISE", RISE), ("C_ALWAYS_FLAT", FLAT), ("C_ALWAYS_FALL", FALL)):
        arms[name] = ("delta", (lambda _d, x=dd: x))
    return arms


def split_digest(insts) -> str:
    rows = [{"instance_id": i.instance_id, "stratum": i.stratum, "scale": i.scale,
             "periods": [{"index": p.index, "latent": dict(p.latent), "channels": dict(p.channels)} for p in i.window.periods]} for i in insts]
    return sha256_text(canonical_json(rows))


def run_instances(instances, label: str, fit: dict) -> tuple[dict, dict]:
    arms = arm_table(fit)
    rows, custody = [], []
    for inst in instances:
        w = inst.window
        delta = F.half_difference(w, CHANNELS)
        truth = oracle(w).capability
        ok, why = G.planter_agrees_v3(w, inst.stratum)
        custody.append({"instance_id": inst.instance_id, "stratum": inst.stratum, "scale": inst.scale, "planter_agrees": ok,
                        "planter_reason": why, "decidable_from_fit_window": decidable_from_fit_window(w), "expected_capability": truth})
        verdicts = {name: (fn(w) if kind == "window" else fn(delta)) for name, (kind, fn) in arms.items()}
        rows.append({"instance_id": inst.instance_id, "stratum": inst.stratum, "scale": inst.scale, "expected_capability": truth, "arms": verdicts})
    res = {"schema_version": SCHEMA_RESULTS, "study_id": STUDY_ID, "label": label, "n_instances": len(rows), "arms": sorted(arms),
           "split_digest": split_digest(instances), "fit_sha256": sha256_file(FIT_JSON) if FIT_JSON.exists() else None, "instances": rows}
    cus = {"schema_version": SCHEMA_RESULTS + ".custody", "label": label, "instances": custody}
    return res, cus


# ---- scoring / gates ---------------------------------------------------------------------

def score(res: dict) -> dict:
    rows = res["instances"]
    vec = {a: [r["arms"][a] == r["expected_capability"] for r in rows] for a in res["arms"]}
    return {"vec": vec, "strata": [r["stratum"] for r in rows], "scales": [r["scale"] for r in rows], "n": len(rows),
            "per_arm": {a: {"capability_correct": sum(v), "n": len(v), "rate": (sum(v) / len(v)) if v else 0.0} for a, v in vec.items()}}


def contrast(sc: dict, x: str, y: str, strata: tuple[str, ...]) -> dict:
    """x vs y on the given strata, per scale (never pooled into one claim), with per-stratum cells."""
    out: dict = {"x": x, "y": y, "strata": list(strata), "per_scale": {}}
    for scl in SCALES:
        idx = [i for i in range(sc["n"]) if sc["strata"][i] in strata and sc["scales"][i] == scl]
        if not idx:
            out["per_scale"][scl] = {"status": "CANNOT_CHECK_NO_INSTANCES", "n": 0}
            continue
        vx, vy = sc["vec"][x], sc["vec"][y]
        b = sum(1 for i in idx if vx[i] and not vy[i]); c = sum(1 for i in idx if vy[i] and not vx[i])
        cells = {}
        for st in sorted({sc["strata"][i] for i in idx}):
            sub = [i for i in idx if sc["strata"][i] == st]
            cells[st] = {"n": len(sub), "x_correct": sum(1 for i in sub if vx[i]), "y_correct": sum(1 for i in sub if vy[i]),
                         "x_only": sum(1 for i in sub if vx[i] and not vy[i]), "y_only": sum(1 for i in sub if vy[i] and not vx[i])}
        out["per_scale"][scl] = {"status": "EVALUATED", "n": len(idx), "x_correct": sum(1 for i in idx if vx[i]), "y_correct": sum(1 for i in idx if vy[i]),
                                 "x_only": b, "y_only": c, "discordant": b + c, "exact_p_two_sided": exact_binomial_two_sided(b, c), "cells": cells}
    return out


def gates(sc: dict, res: dict, cus: dict, fit: dict, selftest_ok: bool | None) -> dict:
    g: dict = {}
    n = sc["n"]
    g["G0a_KNOWN_ANSWER_D8_REPRODUCES_V3_REFIT"] = v3_known_answer(fit)
    g["G0a2_SELFTEST"] = {"pass": selftest_ok, "n_evaluated": 1 if selftest_ok is not None else 0}
    bad = [c["instance_id"] for c in cus["instances"] if not c["planter_agrees"] or not c["decidable_from_fit_window"]]
    g["G0b_GENERATOR_VALIDITY"] = {"pass": (n > 0 and not bad), "n_evaluated": n, "invalid": bad[:10]}
    counts = Counter(v[0] for v in G.STRATA_V3.values()); modal, kmod = counts.most_common(1)[0]
    best_const = max(sc["per_arm"][a]["rate"] for a in CONTROL_ARMS)
    strata_present = sorted(set(sc["strata"]))
    balanced = len(strata_present) == len(G.STRATA_V3)
    g["G0c_NULL_CALIBRATION"] = {"pass": (bool(balanced and abs(best_const - kmod / len(G.STRATA_V3)) < 1e-9) if balanced else None),
                                 "best_constant_rate": best_const, "derived_bar": kmod / len(G.STRATA_V3), "modal_class": modal, "balanced_split": balanced}
    g["G0d_M_EXACT_ON_ALL_STRATA"] = {"pass": sc["per_arm"][M_ARM]["capability_correct"] == n, "M_correct": sc["per_arm"][M_ARM]["capability_correct"], "n": n}
    tie_ok, adv_ok, recovers, curve = True, True, [], {}
    per_domain = {}
    for k in COVERAGE_LEVELS:
        ex = tuple(NON_CARRIER_STRATA + CARRIER_STRATA[:k]); un = tuple(CARRIER_STRATA[k:])
        c_ex = contrast(sc, M_ARM, refit_arm(k), ex)
        c_un = contrast(sc, M_ARM, refit_arm(k), un) if un else None
        tie_here = all(v.get("discordant") == 0 for v in c_ex["per_scale"].values() if v.get("status") == "EVALUATED")
        tie_ok &= tie_here
        adv_here, rec_here = True, []
        if c_un is not None:
            for scl, v in c_un["per_scale"].items():
                if v.get("status") != "EVALUATED":
                    continue
                for st, cell in v["cells"].items():
                    if cell["x_correct"] > cell["y_correct"] and cell["y_only"] == 0:
                        continue
                    adv_here = False
                    if cell["y_correct"] == cell["x_correct"]:
                        rec_here.append(f"{st}|{scl}")
        adv_ok &= adv_here; recovers += rec_here
        curve[str(k)] = {}
        for scl in SCALES:
            idx = [i for i in range(n) if sc["scales"][i] == scl]
            curve[str(k)][scl] = sum(1 for i in idx if sc["vec"][M_ARM][i]) - sum(1 for i in idx if sc["vec"][refit_arm(k)][i])
        per_domain[str(k)] = {"exercised": c_ex, "unexercised": c_un, "tie_on_exercised": tie_here, "advantage_on_every_unexercised_cell": adv_here,
                              "untyped_ties_on_unexercised_cells": rec_here, "refit_zeroed_unexercised_roles": fit["domains"][str(k)][refit_arm(k)]["zeroed_unexercised_roles"]}
    g["G1_TIE_ON_EXERCISED_STRATA"] = {"pass": tie_ok, "n_evaluated": n, "note": "live: M ahead OR behind on an exercised stratum fails this gate"}
    g["G2_ADVANTAGE_ON_UNEXERCISED_CARRIERS"] = {"pass": adv_ok, "untyped_ties_on_unexercised_cells": recovers}
    mono = all(all(curve[str(a)][s] >= curve[str(b)][s] for s in SCALES) for a, b in zip(COVERAGE_LEVELS, COVERAGE_LEVELS[1:]))
    zero8 = all(curve["8"][s] == 0 for s in SCALES)
    g["G3_COVERAGE_CURVE"] = {"pass": mono and zero8, "monotone_non_increasing": mono, "zero_at_full_coverage": zero8, "advantage_M_minus_refit_by_coverage": curve}
    g["per_domain"] = per_domain
    hard = all(bool(g[k]["pass"]) for k in ("G0a_KNOWN_ANSWER_D8_REPRODUCES_V3_REFIT", "G0b_GENERATOR_VALIDITY", "G0d_M_EXACT_ON_ALL_STRATA")) and g["G0c_NULL_CALIBRATION"]["pass"] is not False
    if not hard:
        route = "LANE_DEFECT"
    elif not tie_ok:
        route = "TYPING_SEPARATES_BEYOND_COVERAGE" if any(v["per_scale"][s].get("x_only", 0) > 0 for v in (per_domain[str(k)]["exercised"] for k in COVERAGE_LEVELS) for s in SCALES if v["per_scale"][s].get("status") == "EVALUATED") else "LANE_DEFECT"
    elif recovers:
        route = "UNTYPED_RECOVERS_UNEXERCISED__CORRECTED"
    elif adv_ok and g["G3_COVERAGE_CURVE"]["pass"]:
        route = "TYPING_VALUE_EQUALS_COVERAGE_GAP"
    else:
        route = "LANE_DEFECT"
    g["ROUTE"] = {"route": route, "terminals": TERMINALS}
    return g


def render_md(a: dict) -> str:
    L = [f"# {STUDY_ID} — {a['label']} analysis", "", f"Route: **{a['gates']['ROUTE']['route']}** (n = {a['n_instances']})", "",
         "| arm | correct | rate |", "|---|---:|---:|"]
    for arm, s in sorted(a["per_arm"].items()):
        L.append(f"| {arm} | {s['capability_correct']}/{s['n']} | {s['rate']:.4f} |")
    L += ["", "| coverage k | M − refit (scale " + ") | M − refit (scale ".join(SCALES) + ") | tie on exercised | advantage on every unexercised cell | refit zeroed unexercised roles |", "|---|---:|---:|---|---|---|"]
    for k in COVERAGE_LEVELS:
        d = a["gates"]["per_domain"][str(k)]; cv = a["gates"]["G3_COVERAGE_CURVE"]["advantage_M_minus_refit_by_coverage"][str(k)]
        L.append(f"| {k}/8 | " + " | ".join(str(cv[s]) for s in SCALES) + f" | {d['tie_on_exercised']} | {d['advantage_on_every_unexercised_cell']} | {d['refit_zeroed_unexercised_roles']} |")
    L += ["", "| gate | pass |", "|---|---|"]
    for k, v in a["gates"].items():
        if k in ("ROUTE", "per_domain"):
            continue
        L.append(f"| {k} | {v.get('pass')} |")
    L += ["", "Authority: grants nothing. `NO NOVELTY OR BREAKTHROUGH CLAIM`."]
    return "\n".join(L) + "\n"


# ---- stages --------------------------------------------------------------------------------

def stage_fit(out: Path) -> int:
    fit = fit_on_development()
    FIT_JSON.write_text(canonical_json(fit))
    ka = v3_known_answer(fit)
    print(f"fit written {FIT_JSON.name} sha256 {sha256_file(FIT_JSON)[:16]}…; D_8 reproduces V3 refit: {ka['pass']}")
    for k in COVERAGE_LEVELS:
        d = fit["domains"][str(k)]
        print(f"  D_{k}: n_dev={d['n_dev']} refit={d[refit_arm(k)]['selected_fitter']} dev_correct={d[refit_arm(k)]['dev_capability_correct']} zeroed_unexercised={d[refit_arm(k)]['zeroed_unexercised_roles']} nonzero_unexercised={d[refit_arm(k)]['nonzero_unexercised_roles']}")
    return 0 if ka["pass"] else 1


def stage_selftest(out: Path) -> int:
    fit = frozen_fit() if FIT_JSON.exists() else fit_on_development()
    ok_refit, _ = (True, None) if not FIT_JSON.exists() else (canonical_json(fit_on_development()) == canonical_json(fit), None)
    ka = v3_known_answer(fit)
    # planted failure: a results table where M is ahead of the D_8 refit on an EXERCISED stratum must NOT route to the expected terminal
    insts = G.generate_split_v3("selftest", "ME-X6-V4-SELFTEST", 1)
    res, cus = run_instances(insts, "SELFTEST", fit)
    sc = score(res); g = gates(sc, res, cus, fit, True)
    planted = json.loads(json.dumps(res))
    for r in planted["instances"]:
        if r["stratum"] == NON_CARRIER_STRATA[0]:
            r["arms"][refit_arm(8)] = "MUTANT_WRONG"
    gp = gates(score(planted), planted, cus, fit, True)
    planted_fires = gp["G1_TIE_ON_EXERCISED_STRATA"]["pass"] is False and gp["ROUTE"]["route"] != "TYPING_VALUE_EQUALS_COVERAGE_GAP"
    # planted: an untyped refit tying M on an unexercised cell must route CORRECTED
    planted2 = json.loads(json.dumps(res))
    for r in planted2["instances"]:
        if r["stratum"] == CARRIER_STRATA[7]:
            r["arms"][refit_arm(0)] = r["expected_capability"]
    gp2 = gates(score(planted2), planted2, cus, fit, True)
    planted2_fires = gp2["ROUTE"]["route"] in ("UNTYPED_RECOVERS_UNEXERCISED__CORRECTED", "LANE_DEFECT") and bool(gp2["G2_ADVANTAGE_ON_UNEXERCISED_CARRIERS"]["untyped_ties_on_unexercised_cells"])
    ok = bool(ok_refit and ka["pass"] and g["G0b_GENERATOR_VALIDITY"]["pass"] and g["G0d_M_EXACT_ON_ALL_STRATA"]["pass"] and planted_fires and planted2_fires)
    out.mkdir(parents=True, exist_ok=True)
    rep = {"passed": ok, "fit_reproduces": ok_refit, "known_answer": ka, "selftest_gates": {k: v for k, v in g.items() if k != "per_domain"},
           "planted_tie_violation_fires": planted_fires, "planted_untyped_recovery_fires": planted2_fires, "n_selftest": len(insts)}
    (out / "ME_X6_V4_SELFTEST_REPORT_V1.json").write_text(canonical_json(rep))
    print(f"selftest {'PASS' if ok else 'FAIL'}: fit reproduces {ok_refit}, known answer {ka['pass']}, planted tie violation fires {planted_fires}, planted untyped recovery fires {planted2_fires}; selftest route {g['ROUTE']['route']}")
    return 0 if ok else 1


def _run_split(label: str, prefix: str, seed: str, per_cell: int, out: Path) -> int:
    fit = frozen_fit()
    insts = G.generate_split_v3(prefix, seed, per_cell)
    res, cus = run_instances(insts, label, fit)
    out.mkdir(parents=True, exist_ok=True)
    rp = out / f"ME_X6_V4_{label}_RESULTS_V1.json"; cp = out / f"ME_X6_V4_{label}_EXPECTED_CUSTODY_V1.json"
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus))
    print(f"{label}: {len(insts)} instances; results sha256 {sha256_file(rp)[:16]}…")
    return stage_analyze(rp, cp, out, label)


def stage_dev(out: Path, per_cell: int) -> int:
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_cell, out)


def stage_protected(out: Path, per_cell: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized", file=sys.stderr); return 3
    auth = json.loads(AUTH_FILE.read_text())
    if auth.get("human_written") is not True or len(str(auth.get("human_written_token", ""))) < 16:
        print("REFUSED: authorization requires human_written=true and a token >= 16 chars", file=sys.stderr); return 3
    if auth.get("acknowledged_design_sha256") != sha256_file(DESIGN_JSON):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr); return 3
    design = json.loads(DESIGN_JSON.read_text())
    if design["fit_sha256"] != sha256_file(FIT_JSON):
        print("REFUSED: the development fit has moved since the freeze", file=sys.stderr); return 5
    if not seed_file.exists():
        print(f"REFUSED: custody seed absent ({seed_file})", file=sys.stderr); return 4
    seed = seed_file.read_bytes().strip()
    if hashlib.sha256(seed).hexdigest() != design["seed_commitment"]["protected_seed_sha256"]:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr); return 4
    rc = _run_split("PROTECTED", "protected", seed.decode(), per_cell, out)
    auth["consumed"] = True; auth["revealed_protected_seed"] = seed.decode()
    AUTH_USED.write_text(canonical_json(auth)); AUTH_FILE.unlink()
    return rc


def stage_analyze(rp: Path, cp: Path, out: Path, label: str | None = None) -> int:
    res = json.loads(rp.read_text()); cus = json.loads(cp.read_text()); fit = frozen_fit()
    label = label or res["label"]
    sp = out / "ME_X6_V4_SELFTEST_REPORT_V1.json"
    selftest_ok = bool(json.loads(sp.read_text()).get("passed")) if sp.exists() else None
    sc = score(res)
    a = {"schema_version": SCHEMA_ANALYSIS, "study_id": STUDY_ID, "label": label, "n_instances": sc["n"], "results_sha256": sha256_file(rp),
         "custody_sha256": sha256_file(cp), "per_arm": sc["per_arm"], "gates": gates(sc, res, cus, fit, selftest_ok)}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"ME_X6_V4_{label}_ANALYSIS_V1.json").write_text(canonical_json(a))
    (out / f"ME_X6_V4_{label}_ANALYSIS_V1.md").write_text(render_md(a))
    print(f"{label} route: {a['gates']['ROUTE']['route']}; curve {a['gates']['G3_COVERAGE_CURVE']['advantage_M_minus_refit_by_coverage']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("fit", "selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=RESULTS_DIR)
    ap.add_argument("--per-cell", type=int, default=None)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    a = ap.parse_args(argv)
    if a.stage == "fit":
        return stage_fit(a.out)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_cell or 1)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_cell or PROTECTED_PER_CELL, a.seed_file)
    return stage_analyze(a.results, a.custody, a.out)


if __name__ == "__main__":
    sys.exit(main())
