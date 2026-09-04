#!/usr/bin/env python3
"""E40-RS — the shipping operator re-tested with the out-of-sample ranker the channel bound found.

Lineage, in one line each:
  m3   the drag is the SELECTION operator (both_final / both_best null; only F0_best - F2_final separates)
  m4   shipping by a single proxy field does not eliminate the drag
  IB   a leave-one-chain-out ridge ranker on the eight visible fields (+ the executed config)
       ranks truth out of sample (FB8 rho 0.220 p 0.019; FB8+CFG rho 0.392 p 0.0005);
       feedback does not add to the config prior at n = 36 (IB3 not fired)

This file pulls m4's lever again with the IB ranker as the shipping operator, on the same frozen
tuples, with the ranker never seeing the chain it ships for.  Zero model calls, zero native runs.
Pure Python; every sum is math.fsum; every draw is seeded from the design and consumed in order.

Exit codes -- "could not check" keeps its own code:
  0  measured (whatever the routing says)
  2  usage error
  4  a registered control FAILED (checked; the verdict is refused)
  5  CANNOT_CHECK (an envelope is invalid; a control could not be obtained)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import e40_channel_information_bound as IB  # noqa: E402  (frozen; read-only)

DESIGN = "E40_RANKER_SHIPPING_REANALYSIS_DESIGN_V1"
DESIGN_JSON = HERE / f"{DESIGN}.json"
ROLLUP_DIR = HERE / "rollup-e40-ranker-shipping"
ROLLUP = ROLLUP_DIR / "E40_RANKER_SHIPPING_ROLLUP_V1.json"
SCHEMA = "orion.v2.e40-ranker-shipping.rollup.v1"

KINDS = ("FB8", "CFG", "FB8+CFG")
PRIMARY_KIND = "FB8+CFG"          # the controller's full visible information: feedback + its own config
RIDGE_LAMBDA = IB.RIDGE_LAMBDA    # 1.0 -- inherited, not re-tuned
SIGNFLIP_N = 4000
SIGNFLIP_SEED = 20260904
PLANT_SEED = 20260904
PLANT_NOISE_SD_FRACTION = 0.25
PLANT_MIN_RECOVERED_FRACTION = 0.75
NULLCAL_REPS = 100
NULLCAL_FLIPS = 400
NULLCAL_SEED = 20260903
NULLCAL_BAND = (0.02, 0.09)
ALPHA = 0.05
RS2_MIN_RECOVERED_FRACTION = 0.5
F2_COHORTS = (("campaign-e40-m2", "f2"), ("campaign-e40-m3", "f2"))
F0_COHORT = ("campaign-e40-m2", "f0")


class ControlFailed(Exception):
    pass


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- the leave-one-chain-out ranker, returning predictions ------------------------------

def loco_predictions(chains: dict, kind: str, truth: dict | None = None) -> dict:
    """Per held-out chain: the ridge prediction for each of its 4 rows, fitted on every OTHER chain."""
    keys = list(chains)
    out = {}
    for held in keys:
        xtr, ytr = [], []
        for k in keys:
            if k == held:
                continue
            ys = truth[k] if truth else [r["truth_wasserstein"] for r in chains[k]]
            for r, y in zip(chains[k], ys):
                xtr.append(IB.features(r, kind))
                ytr.append(y)
        w, ym, mu, sd = IB._ridge_fit(xtr, ytr, RIDGE_LAMBDA)
        out[held] = IB._ridge_predict(w, ym, mu, sd, [IB.features(r, kind) for r in chains[held]])
    return out


def ship_index(preds: list[float]) -> int:
    """Argmin of predicted wasserstein; ties broken by the EARLIEST cycle (the loop cannot un-run a cycle)."""
    return min(range(len(preds)), key=lambda i: (preds[i], i))


# ---- pairs --------------------------------------------------------------------------------

def make_pairs(chains: dict, preds: dict[str, dict], truth: dict | None = None) -> list[dict[str, Any]]:
    """One record per F2 chain, paired to the m2 F0 chain of the same (dataset, rep) -- exactly the
    pairing the m2/m3 receipts use (asserted by the reproduction control)."""
    def tw(k, i):
        return truth[k][i] if truth else chains[k][i]["truth_wasserstein"]
    f0 = {(rs[0]["dataset"], rs[0]["rep"]): k for k, rs in chains.items() if (k[0], rs[0]["arm"]) == F0_COHORT}
    pairs = []
    for k, rs in chains.items():
        if (k[0], rs[0]["arm"]) not in F2_COHORTS:
            continue
        k0 = f0[(rs[0]["dataset"], rs[0]["rep"])]
        f2w = [tw(k, i) for i in range(4)]
        f0w = [tw(k0, i) for i in range(4)]
        rec = {"campaign": k[0], "chain": k[1], "f0_chain": k0[1],
               "f2_final": f2w[3], "f2_best": min(f2w), "f0_best": min(f0w)}
        for kind in KINDS:
            i2 = ship_index(preds[kind][k])
            i0 = ship_index(preds[kind][k0])
            rec[f"f2_ship[{kind}]"] = f2w[i2]
            rec[f"f2_ship_cycle[{kind}]"] = rs[i2]["cycle"]
            rec[f"f0_ship[{kind}]"] = f0w[i0]
        pairs.append(rec)
    if len(pairs) != 24:
        raise IB.CannotCheck(f"{len(pairs)} F2 chains paired, expected 24")
    return pairs


def signflip_two_sided_and_directed(diffs: list[float], n: int, seed: int) -> dict[str, float]:
    """p_pos: P(mean >= observed) under sign flips; p_neg: P(mean <= observed)."""
    p_pos = IB.signflip_p(diffs, n, seed)
    p_neg = IB.signflip_p([-d for d in diffs], n, seed)
    return {"p_pos": p_pos, "p_neg": p_neg}


def contrasts(pairs: list[dict[str, Any]], kind: str, seed: int = SIGNFLIP_SEED, n: int = SIGNFLIP_N) -> dict[str, Any]:
    """All contrasts in the m-series convention d = F0_x - F2_y on wasserstein (lower is better):
    negative d => F2 worse.  'improvement' = F2_final - F2_ship (positive => the lever helped)."""
    def block(name: str, diffs: list[float]) -> dict[str, Any]:
        ps = signflip_two_sided_and_directed(diffs, n, seed)
        return {"name": name, "n": len(diffs), "mean_d": IB._mean(diffs),
                "wins_f2": sum(1 for d in diffs if d > 0), "wins_f0": sum(1 for d in diffs if d < 0),
                "ties": sum(1 for d in diffs if d == 0), **ps}
    out: dict[str, Any] = {}
    for camp in ("campaign-e40-m2", "campaign-e40-m3", "pooled"):
        sub = [p for p in pairs if camp == "pooled" or p["campaign"] == camp]
        out[camp] = {
            "P0_f0best_minus_f2final": block("F0_best - F2_final (registered m-series primary)", [p["f0_best"] - p["f2_final"] for p in sub]),
            "P1_f0best_minus_f2ship": block(f"F0_best - F2_ship[{kind}]", [p["f0_best"] - p[f"f2_ship[{kind}]"] for p in sub]),
            "P2_improvement_f2final_minus_f2ship": block(f"F2_final - F2_ship[{kind}] (>0: lever helps)", [p["f2_final"] - p[f"f2_ship[{kind}]"] for p in sub]),
            "P3_fair_f0ship_minus_f2ship": block(f"F0_ship[{kind}] - F2_ship[{kind}] (matched operator)", [p[f"f0_ship[{kind}]"] - p[f"f2_ship[{kind}]"] for p in sub]),
            "P4_ceiling_f0best_minus_f2best": block("F0_best - F2_best (oracle both sides)", [p["f0_best"] - p["f2_best"] for p in sub]),
            "recoverable_f2final_minus_f2best": block("F2_final - F2_best (what any shipping operator could recover)", [p["f2_final"] - p["f2_best"] for p in sub]),
        }
        rec = out[camp]["recoverable_f2final_minus_f2best"]["mean_d"]
        imp = out[camp]["P2_improvement_f2final_minus_f2ship"]["mean_d"]
        out[camp]["recovered_fraction"] = (imp / rec) if rec > 0 else None
        out[camp]["ship_cycle_census"] = {str(c): sum(1 for p in sub if p[f"f2_ship_cycle[{kind}]"] == c) for c in (1, 2, 3, 4)}
    return out


# ---- controls -----------------------------------------------------------------------------

def control_recoverable_positive(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    """Contrast-could-exist: the oracle-recoverable improvement is strictly positive pooled AND at
    least 12 of 24 chains have a non-final best cycle (otherwise no operator can move anything)."""
    rec = [p["f2_final"] - p["f2_best"] for p in pairs]
    movable = sum(1 for r in rec if r > 0)
    ok = IB._mean(rec) > 0 and movable >= 12
    return {"control": "RECOVERABLE_IMPROVEMENT_EXISTS", "pass": ok, "mean_recoverable": IB._mean(rec),
            "chains_with_a_better_earlier_cycle": movable, "n": len(rec), "rule": "mean > 0 and movable >= 12"}


def control_planted(chains: dict) -> dict[str, Any]:
    """run_time := truth + N(0, 0.25 sd) on a COPY; the FB8 ranker-ship must recover >= 75 % of the
    oracle-recoverable improvement pooled.  Proves the pipeline ships on an informative channel."""
    rng = random.Random(PLANT_SEED)
    ys = [r["truth_wasserstein"] for rs in chains.values() for r in rs]
    m = IB._mean(ys)
    sd = math.sqrt(math.fsum((y - m) ** 2 for y in ys) / (len(ys) - 1))
    planted = {}
    for k, rs in chains.items():
        planted[k] = []
        for r in rs:
            r2 = dict(r)
            r2["feedback"] = dict(r["feedback"])
            r2["feedback"]["run_time"] = r["truth_wasserstein"] + rng.gauss(0.0, PLANT_NOISE_SD_FRACTION * sd)
            planted[k].append(r2)
    preds = {kind: loco_predictions(planted, kind) for kind in KINDS}
    pairs = make_pairs(planted, preds)
    c = contrasts(pairs, "FB8", n=400)
    frac = c["pooled"]["recovered_fraction"]
    ok = frac is not None and frac >= PLANT_MIN_RECOVERED_FRACTION
    return {"control": "PLANTED_SIGNAL_SHIPS", "pass": ok, "recovered_fraction_FB8": frac,
            "improvement_mean": c["pooled"]["P2_improvement_f2final_minus_f2ship"]["mean_d"],
            "rule": f"recovered_fraction >= {PLANT_MIN_RECOVERED_FRACTION}"}


def control_nullcal(chains: dict) -> dict[str, Any]:
    """Shuffle truth within chains REPS times; RS1's test on the PRIMARY kind must reject at ~alpha."""
    rng = random.Random(NULLCAL_SEED)
    keys = list(chains)
    rejections = 0
    for rep in range(NULLCAL_REPS):
        truth = {}
        for k in keys:
            ys = [r["truth_wasserstein"] for r in chains[k]]
            rng.shuffle(ys)
            truth[k] = ys
        preds = {PRIMARY_KIND: loco_predictions(chains, PRIMARY_KIND, truth)}
        # the other kinds are not needed for RS1; fill them with the primary so make_pairs is total
        preds = {kind: preds[PRIMARY_KIND] for kind in KINDS}
        pairs = make_pairs(chains, preds, truth)
        diffs = [p["f2_final"] - p[f"f2_ship[{PRIMARY_KIND}]"] for p in pairs]
        p = IB.signflip_p(diffs, NULLCAL_FLIPS, NULLCAL_SEED + 1 + rep)
        if IB._mean(diffs) > 0 and p <= ALPHA:
            rejections += 1
    rate = rejections / NULLCAL_REPS
    ok = NULLCAL_BAND[0] <= rate <= NULLCAL_BAND[1]
    return {"control": "NULL_CALIBRATION", "pass": ok, "rejection_rate": rate,
            "reps": NULLCAL_REPS, "flips": NULLCAL_FLIPS, "band": list(NULLCAL_BAND)}


# ---- gates and routing ---------------------------------------------------------------------

def evaluate_gates(controls: list[dict[str, Any]], primary: dict[str, Any]) -> dict[str, Any]:
    """Controls are CONSUMED here (UNGATED_CONTROL_VERDICT guard)."""
    if not all(c["pass"] for c in controls):
        return {"RS0_CONTROLS_VALID": False, "RS1": None, "RS2": None,
                "terminal": "CANNOT_CHECK__CONTROL_FAILED",
                "failed_controls": [c["control"] for c in controls if not c["pass"]]}
    pooled = primary["pooled"]
    p2 = pooled["P2_improvement_f2final_minus_f2ship"]
    rs1 = p2["mean_d"] > 0 and p2["p_pos"] <= ALPHA
    frac = pooled["recovered_fraction"]
    rs2 = bool(rs1 and frac is not None and frac >= RS2_MIN_RECOVERED_FRACTION)
    if rs1 and rs2:
        terminal = "SHIPPING_OPERATOR_RECOVERS_HALF_OR_MORE_OF_THE_DRAG__PROSPECTIVE_SHIPPING_LINE_WARRANTED"
    elif rs1:
        terminal = "SHIPPING_OPERATOR_HELPS_BUT_THE_DRAG_STANDS__PARTIAL"
    else:
        terminal = "SHIPPING_LEVER_EXHAUSTED__NO_OOS_RANKER_ON_VISIBLE_FIELDS_SHIPS_BETTER_THAN_THE_LOOPS_FINAL"
    p1 = pooled["P1_f0best_minus_f2ship"]
    p3 = pooled["P3_fair_f0ship_minus_f2ship"]
    return {"RS0_CONTROLS_VALID": True, "RS1_SHIPPING_LEVER_HELPS": rs1,
            "RS2_RECOVERS_HALF_OR_MORE": rs2, "recovered_fraction": frac,
            "RS3_drag_under_ranker_shipping": {"mean_d": p1["mean_d"], "p_f2_worse": p1["p_neg"],
                                               "still_significantly_negative": p1["mean_d"] < 0 and p1["p_neg"] <= ALPHA},
            "RS4_fair_matched_operator": {"mean_d": p3["mean_d"], "p_f2_worse": p3["p_neg"], "p_f2_better": p3["p_pos"]},
            "terminal": terminal}


# ---- run -------------------------------------------------------------------------------------

def run(out: Path = ROLLUP) -> int:
    rows = IB.load_rows()
    chains = IB.chains_of(rows)
    controls = [IB.control_m2_m3_reproduced(chains)]
    preds = {kind: loco_predictions(chains, kind) for kind in KINDS}
    pairs = make_pairs(chains, preds)
    controls.append(control_recoverable_positive(pairs))
    controls.append(control_planted(chains))
    controls.append(control_nullcal(chains))
    by_kind = {kind: contrasts(pairs, kind) for kind in KINDS}
    gates = evaluate_gates(controls, by_kind[PRIMARY_KIND])
    roll = {
        "schema_version": SCHEMA, "design": DESIGN,
        "design_json_sha256": sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else None,
        "script_sha256": sha256_file(Path(__file__)), "tuples_sha256": sha256_file(IB.TUPLES),
        "interpreter": sys.version.split()[0],
        "constants": {"kinds": list(KINDS), "primary_kind": PRIMARY_KIND, "ridge_lambda": RIDGE_LAMBDA,
                      "signflip_n": SIGNFLIP_N, "signflip_seed": SIGNFLIP_SEED, "plant_seed": PLANT_SEED,
                      "plant_noise_sd_fraction": PLANT_NOISE_SD_FRACTION,
                      "plant_min_recovered_fraction": PLANT_MIN_RECOVERED_FRACTION,
                      "nullcal": {"reps": NULLCAL_REPS, "flips": NULLCAL_FLIPS, "seed": NULLCAL_SEED, "band": list(NULLCAL_BAND)},
                      "alpha": ALPHA, "rs2_min_recovered_fraction": RS2_MIN_RECOVERED_FRACTION},
        "n_pairs": len(pairs), "controls": controls, "contrasts_by_kind": by_kind, "gates": gates,
        "pairs": pairs,
        "authority": {"revives_e40": False, "authorizes_m6": False, "alters_e40_closure": False,
                      "grants_field_status": False, "grants_scientific_truth": False},
    }
    ROLLUP_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(roll, indent=1, sort_keys=True) + "\n")
    for c in controls:
        print(f"control {c['control']}: {'PASS' if c['pass'] else 'FAIL'}")
    for kind in KINDS:
        pl = by_kind[kind]["pooled"]
        print(f"{kind:8s} pooled  P0 {pl['P0_f0best_minus_f2final']['mean_d']:+.6f}  "
              f"P1 {pl['P1_f0best_minus_f2ship']['mean_d']:+.6f} (p_f2_worse {pl['P1_f0best_minus_f2ship']['p_neg']:.4f})  "
              f"P2 {pl['P2_improvement_f2final_minus_f2ship']['mean_d']:+.6f} (p {pl['P2_improvement_f2final_minus_f2ship']['p_pos']:.4f})  "
              f"recovered {pl['recovered_fraction']}")
    print("gates", json.dumps({k: v for k, v in gates.items() if not isinstance(v, dict)}))
    print(f"interpreter {sys.version.split()[0]}; written {out}")
    if not gates["RS0_CONTROLS_VALID"]:
        return 4
    return 0


# ---- selftest --------------------------------------------------------------------------------

def selftest() -> int:
    fails = []

    def check(name, cond):
        print(f"  {'ok ' if cond else 'FAIL'} {name}")
        if not cond:
            fails.append(name)

    check("ship: argmin of predictions", ship_index([0.3, 0.1, 0.2, 0.4]) == 1)
    check("ship: ties break to the earliest cycle", ship_index([0.2, 0.1, 0.1, 0.4]) == 1)
    rng = random.Random(1)
    pos = [abs(rng.gauss(0.01, 0.002)) for _ in range(24)]
    sym = [rng.gauss(0.0, 0.01) for _ in range(24)]
    check("sign-flip: all-positive diffs give p_pos <= alpha", IB.signflip_p(pos, 2000, 1) <= ALPHA)
    check("sign-flip: p_neg of an all-positive vector is ~1", IB.signflip_p([-d for d in pos], 2000, 1) > 0.5)
    check("sign-flip: symmetric noise is not significant", IB.signflip_p(sym, 2000, 1) > ALPHA or IB.signflip_p([-d for d in sym], 2000, 1) > ALPHA)
    ctrl_ok = [{"control": "x", "pass": True}]
    ctrl_bad = [{"control": "x", "pass": False}]

    def prim(mean_p2, p_pos, frac, mean_p1=-0.005, p_neg=0.99):
        return {"pooled": {"P2_improvement_f2final_minus_f2ship": {"mean_d": mean_p2, "p_pos": p_pos},
                           "recovered_fraction": frac,
                           "P1_f0best_minus_f2ship": {"mean_d": mean_p1, "p_neg": p_neg},
                           "P3_fair_f0ship_minus_f2ship": {"mean_d": 0.0, "p_neg": 0.5, "p_pos": 0.5}}}
    check("route: control failed refuses every gate", evaluate_gates(ctrl_bad, prim(0.01, 0.001, 0.9))["terminal"].startswith("CANNOT_CHECK"))
    check("route: RS1 and RS2 -> prospective shipping line", evaluate_gates(ctrl_ok, prim(0.01, 0.001, 0.9))["terminal"].startswith("SHIPPING_OPERATOR_RECOVERS_HALF"))
    check("route: RS1 only -> partial", evaluate_gates(ctrl_ok, prim(0.004, 0.01, 0.3))["terminal"].startswith("SHIPPING_OPERATOR_HELPS_BUT"))
    check("route: RS1 not fired -> lever exhausted", evaluate_gates(ctrl_ok, prim(0.001, 0.4, 0.1))["terminal"].startswith("SHIPPING_LEVER_EXHAUSTED"))
    check("route: RS2 cannot fire without RS1 (unfailable-clause guard)", evaluate_gates(ctrl_ok, prim(-0.001, 0.9, 0.9))["RS2_RECOVERS_HALF_OR_MORE"] is False)
    # a synthetic world: 36 chains x 4 rows, an informative field -> the FB8 ranker must ship the best cycle
    def synth(informative: bool, seed: int = 7):
        r = random.Random(seed)
        chains = {}
        for i in range(36):
            camp = "campaign-e40-m2" if i < 24 else "campaign-e40-m3"
            arm = "f0" if i < 12 else "f2"
            rs = []
            for cyc in range(1, 5):
                y = r.uniform(0.1, 0.3)
                fb = {f: r.uniform(0, 100) for f in IB.FEEDBACK_FIELDS}
                fb["run_time"] = (y * 1000 + r.gauss(0, 1)) if informative else r.uniform(0, 100)
                rs.append({"campaign": camp, "arm": arm, "chain": f"{i}_{arm}_ds_{i % 12}", "cycle": cyc,
                           "dataset": "ds", "rep": i % 12, "regime": IB.REGIMES[cyc % 3], "frac": cyc / 4,
                           "feedback": fb, "truth_wasserstein": y})
            chains[(camp, f"{i}_{arm}_ds_{i % 12}")] = rs
        return chains
    ch = synth(True)
    preds = {k: loco_predictions(ch, k) for k in KINDS}
    pairs = make_pairs(ch, preds)
    c = contrasts(pairs, "FB8", n=200)
    check("synthetic informative field: FB8 ranker recovers >= 75% of the recoverable", (c["pooled"]["recovered_fraction"] or 0) >= 0.75)
    ch0 = synth(False)
    preds0 = {k: loco_predictions(ch0, k) for k in KINDS}
    c0 = contrasts(make_pairs(ch0, preds0), "FB8", n=200)
    check("synthetic uninformative field: FB8 ranker does not recover >= 75% (control can fail)", (c0["pooled"]["recovered_fraction"] or 0) < 0.75)
    if DESIGN_JSON.exists():
        dc = json.loads(DESIGN_JSON.read_text())["constants"]
        check("design twin: constants agree with the script",
              tuple(dc["kinds"]) == KINDS and dc["primary_kind"] == PRIMARY_KIND and dc["ridge_lambda"] == RIDGE_LAMBDA
              and dc["signflip_n"] == SIGNFLIP_N and dc["signflip_seed"] == SIGNFLIP_SEED and dc["plant_seed"] == PLANT_SEED
              and dc["plant_noise_sd_fraction"] == PLANT_NOISE_SD_FRACTION
              and dc["plant_min_recovered_fraction"] == PLANT_MIN_RECOVERED_FRACTION
              and dc["nullcal"] == {"reps": NULLCAL_REPS, "flips": NULLCAL_FLIPS, "seed": NULLCAL_SEED, "band": list(NULLCAL_BAND)}
              and dc["alpha"] == ALPHA and dc["rs2_min_recovered_fraction"] == RS2_MIN_RECOVERED_FRACTION)
    else:
        check("design twin present", False)
    print(f"selftest: {len(fails)} failures")
    return 0 if not fails else 5


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("run").add_argument("--out", type=Path, default=ROLLUP)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "selftest":
            return selftest()
        if a.cmd == "run":
            return run(a.out)
    except IB.CannotCheck as exc:
        print(f"CANNOT_CHECK: {exc}", file=sys.stderr)
        return 5
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
