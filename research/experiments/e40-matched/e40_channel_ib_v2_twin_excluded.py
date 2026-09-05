#!/usr/bin/env python3
"""E40 channel information bound + ranker shipping, V2: the held-out chain's TWINS leave the fold.

Defect found after the V1 rollups were filed (and recorded rather than patched): the m2/m3
substrate is deterministic, and 15 exact configurations -- same dataset, regime, fraction,
model_seed and partial_intervention_seed -- were executed in MORE THAN ONE chain (F0 chains
re-using seeds; m3's cycle-1 anchor landing on the same interventional@0 config an F0 chain
also ran).  39 of the 144 rows therefore have a byte-identical native run in ANOTHER chain,
with identical truth.  V1's leave-one-chain-out held out one chain while its twin rows sat in
the training fold, so every V1 "out of sample" number saw the sample it was scoring in 27 % of
its rows.  The IB1/IB2 verdicts and the RS recovered fraction are withdrawn to CANNOT_CHECK.

V2 changes ONE thing: the training fold for a held-out chain excludes every row whose exact
configuration equals any configuration in the held-out chain.  Ranker, lambda, feature sets,
statistics, nulls, seeds, controls, gates and routing are inherited unchanged from the V1
modules (imported read-only), and a new must-fire control counts the twins so the defect can
never be silent again.

Exit codes -- "could not check" keeps its own code:
  0  measured (rollup written)
  4  a registered control FAILED (checked; the verdict is refused)
  5  CANNOT_CHECK (an envelope is invalid)
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import e40_channel_information_bound as IB  # noqa: E402  (frozen V1; read-only)
import e40_ranker_shipping as RS  # noqa: E402  (frozen V1; read-only)

DESIGN = "E40_CHANNEL_IB_V2_TWIN_EXCLUDED_DESIGN_V1"
DESIGN_JSON = HERE / f"{DESIGN}.json"
ROLLUP_DIR = HERE / "rollup-e40-channel-ib-v2"
ROLLUP = ROLLUP_DIR / "E40_CHANNEL_IB_V2_ROLLUP_V1.json"
SCHEMA = "orion.v2.e40-channel-ib-v2-twin-excluded.rollup.v1"

EXPECTED_TWIN_ROWS = 39           # measured before the freeze; the control must reproduce it
EXPECTED_TWIN_CONFIGS = 15


class ControlFailed(Exception):
    pass


# ---- twins ----------------------------------------------------------------------------------

def config_key(r: dict[str, Any]) -> tuple:
    return (r["dataset"], r["regime"], float(r["frac"]), int(r["model_seed"]), int(r["pi_seed"]))


def twin_census(chains: dict) -> dict[str, Any]:
    """Rows whose exact configuration was executed in another chain; identical truth asserted."""
    where: dict[tuple, list[tuple]] = {}
    for k, rs in chains.items():
        for r in rs:
            where.setdefault(config_key(r), []).append((k, round(r["truth_wasserstein"], 9)))
    cross = {c: v for c, v in where.items() if len({k for k, _ in v}) > 1}
    rows = sum(len(v) for v in cross.values())
    same_truth = all(len({t for _, t in v}) == 1 for v in cross.values())
    per_chain_v1_leak = {}
    for k, rs in chains.items():
        keys = {config_key(r) for r in rs}
        leaked = sum(1 for k2, rs2 in chains.items() if k2 != k for r in rs2 if config_key(r) in keys)
        per_chain_v1_leak[f"{k[0]}/{k[1]}"] = leaked
    return {"twin_configs_across_chains": len(cross), "rows_with_a_twin_in_another_chain": rows,
            "twins_have_identical_truth": same_truth,
            "v1_training_rows_that_were_twins_of_the_held_out_chain": per_chain_v1_leak,
            "chains_whose_v1_fold_was_contaminated": sum(1 for v in per_chain_v1_leak.values() if v > 0)}


def training_rows(chains: dict, held: tuple, kind: str, truth: dict | None) -> tuple[list, list]:
    """V2 fold: every other chain's rows EXCEPT those whose config equals a held-out config."""
    banned = {config_key(r) for r in chains[held]}
    x, y = [], []
    for k, rs in chains.items():
        if k == held:
            continue
        ys = truth[k] if truth else [r["truth_wasserstein"] for r in rs]
        for r, yy in zip(rs, ys):
            if config_key(r) in banned:
                continue
            x.append(IB.features(r, kind))
            y.append(yy)
    return x, y


def loco_rho_v2(chains: dict, kind: str, truth: dict | None = None) -> dict:
    out = {}
    for held in chains:
        x, y = training_rows(chains, held, kind, truth)
        w, ym, mu, sd = IB._ridge_fit(x, y, IB.RIDGE_LAMBDA)
        yte = truth[held] if truth else [r["truth_wasserstein"] for r in chains[held]]
        pred = IB._ridge_predict(w, ym, mu, sd, [IB.features(r, kind) for r in chains[held]])
        rho = IB.spearman(pred, yte)
        top1 = min(range(4), key=lambda i: pred[i]) == min(range(4), key=lambda i: yte[i])
        out[held] = (rho, top1)
    return out


def loco_predictions_v2(chains: dict, kind: str, truth: dict | None = None) -> dict:
    out = {}
    for held in chains:
        x, y = training_rows(chains, held, kind, truth)
        w, ym, mu, sd = IB._ridge_fit(x, y, IB.RIDGE_LAMBDA)
        out[held] = IB._ridge_predict(w, ym, mu, sd, [IB.features(r, kind) for r in chains[held]])
    return out


def assert_no_twin_in_any_fold(chains: dict) -> dict[str, Any]:
    """The V2 fold must contain ZERO twins of the held-out chain: recount from the rows
    (not from the filter) that the training fold size equals all-other-rows minus the twins."""
    worst = 0
    for held in chains:
        banned = {config_key(r) for r in chains[held]}
        twins = sum(1 for k2, rs2 in chains.items() if k2 != held for r in rs2 if config_key(r) in banned)
        others = sum(len(rs2) for k2, rs2 in chains.items() if k2 != held)
        x_kept, _ = training_rows(chains, held, "CFG", None)
        if len(x_kept) != others - twins:
            raise ControlFailed(f"fold for {held}: kept {len(x_kept)} rows, expected {others - twins}")
        worst = max(worst, twins)
    return {"max_rows_excluded_from_a_fold": worst}


# ---- V2 permutation null, plant and null calibration (IB) ----------------------------------

def perm_p_v2(chains: dict, kind: str, observed: float, n_perm: int, seed: int) -> tuple[float, list[float]]:
    rng = random.Random(seed)
    null = []
    for _ in range(n_perm):
        truth = {}
        for k in chains:
            ys = [r["truth_wasserstein"] for r in chains[k]]
            rng.shuffle(ys)
            truth[k] = ys
        null.append(IB.pooled(loco_rho_v2(chains, kind, truth))["mean_rho"])
    ge = sum(1 for v in null if v >= observed - 1e-12)
    return (ge + 1) / (n_perm + 1), null


def _planted_copy(chains: dict, seed: int) -> dict:
    rng = random.Random(seed)
    ys = [r["truth_wasserstein"] for rs in chains.values() for r in rs]
    m = IB._mean(ys)
    sd = math.sqrt(math.fsum((y - m) ** 2 for y in ys) / (len(ys) - 1))
    planted = {}
    for k, rs in chains.items():
        planted[k] = []
        for r in rs:
            r2 = dict(r)
            r2["feedback"] = dict(r["feedback"])
            r2["feedback"]["run_time"] = r["truth_wasserstein"] + rng.gauss(0.0, IB.PLANT_NOISE_SD_FRACTION * sd)
            planted[k].append(r2)
    return planted


def control_planted_v2(chains: dict) -> dict[str, Any]:
    planted = _planted_copy(chains, IB.PLANT_SEED)
    pool = IB.pooled(loco_rho_v2(planted, "FB8"))
    p, _ = perm_p_v2(planted, "FB8", pool["mean_rho"], 400, IB.PERM_SEED)
    ok = pool["mean_rho"] >= IB.PLANT_MIN_RHO and p <= IB.ALPHA
    return {"control": "PLANTED_SIGNAL_DETECTED", "pass": ok, "mean_rho": pool["mean_rho"],
            "top1_hit_rate": pool["top1_hit_rate"], "perm_p": p, "n_perm": 400}


def control_nullcal_v2(chains: dict) -> dict[str, Any]:
    rng = random.Random(IB.NULLCAL_SEED)
    rejections = 0
    for rep in range(IB.NULLCAL_REPS):
        truth = {}
        for k in chains:
            ys = [r["truth_wasserstein"] for r in chains[k]]
            rng.shuffle(ys)
            truth[k] = ys
        fake = {k: [dict(r, truth_wasserstein=y) for r, y in zip(chains[k], truth[k])] for k in chains}
        obs = IB.pooled(loco_rho_v2(fake, "FB8"))["mean_rho"]
        p, _ = perm_p_v2(fake, "FB8", obs, IB.NULLCAL_PERMS, IB.NULLCAL_SEED + 1 + rep)
        if p <= IB.ALPHA:
            rejections += 1
    rate = rejections / IB.NULLCAL_REPS
    ok = IB.NULLCAL_BAND[0] <= rate <= IB.NULLCAL_BAND[1]
    return {"control": "NULL_CALIBRATION", "pass": ok, "rejection_rate": rate,
            "reps": IB.NULLCAL_REPS, "perms": IB.NULLCAL_PERMS, "band": list(IB.NULLCAL_BAND)}


# ---- RS controls under V2 folds --------------------------------------------------------------

def control_planted_ships_v2(chains: dict) -> dict[str, Any]:
    planted = _planted_copy(chains, RS.PLANT_SEED)
    preds = {kind: loco_predictions_v2(planted, kind) for kind in RS.KINDS}
    pairs = RS.make_pairs(planted, preds)
    c = RS.contrasts(pairs, "FB8", n=400)
    frac = c["pooled"]["recovered_fraction"]
    ok = frac is not None and frac >= RS.PLANT_MIN_RECOVERED_FRACTION
    return {"control": "PLANTED_SIGNAL_SHIPS", "pass": ok, "recovered_fraction_FB8": frac,
            "rule": f"recovered_fraction >= {RS.PLANT_MIN_RECOVERED_FRACTION}"}


def control_rs_nullcal_v2(chains: dict) -> dict[str, Any]:
    rng = random.Random(RS.NULLCAL_SEED)
    rejections = 0
    for rep in range(RS.NULLCAL_REPS):
        truth = {}
        for k in chains:
            ys = [r["truth_wasserstein"] for r in chains[k]]
            rng.shuffle(ys)
            truth[k] = ys
        pk = loco_predictions_v2(chains, RS.PRIMARY_KIND, truth)
        preds = {kind: pk for kind in RS.KINDS}
        pairs = RS.make_pairs(chains, preds, truth)
        diffs = [p["f2_final"] - p[f"f2_ship[{RS.PRIMARY_KIND}]"] for p in pairs]
        p = IB.signflip_p(diffs, RS.NULLCAL_FLIPS, RS.NULLCAL_SEED + 1 + rep)
        if IB._mean(diffs) > 0 and p <= RS.ALPHA:
            rejections += 1
    rate = rejections / RS.NULLCAL_REPS
    ok = RS.NULLCAL_BAND[0] <= rate <= RS.NULLCAL_BAND[1]
    return {"control": "NULL_CALIBRATION", "pass": ok, "rejection_rate": rate,
            "reps": RS.NULLCAL_REPS, "flips": RS.NULLCAL_FLIPS, "band": list(RS.NULLCAL_BAND)}


# ---- run --------------------------------------------------------------------------------------

def run(out: Path = ROLLUP) -> int:
    rows = IB.load_rows()
    chains = IB.chains_of(rows)

    # controls first; the twin census must FIRE at the pre-freeze counts, and the V2 fold must be clean
    census = twin_census(chains)
    c_twins = {"control": "TWIN_CENSUS_FIRES", "pass": (census["rows_with_a_twin_in_another_chain"] == EXPECTED_TWIN_ROWS
                                                          and census["twin_configs_across_chains"] == EXPECTED_TWIN_CONFIGS
                                                          and census["twins_have_identical_truth"]),
               **census, "expected": {"rows": EXPECTED_TWIN_ROWS, "configs": EXPECTED_TWIN_CONFIGS}}
    try:
        fold = assert_no_twin_in_any_fold(chains)
        c_fold = {"control": "V2_FOLD_HAS_NO_TWIN", "pass": True, **fold}
    except ControlFailed as exc:
        c_fold = {"control": "V2_FOLD_HAS_NO_TWIN", "pass": False, "reason": str(exc)}
    ib_controls = [c_twins, c_fold, IB.control_m4_reproduced(chains), IB.control_m2_m3_reproduced(chains),
                   control_planted_v2(chains), control_nullcal_v2(chains)]

    # IB under V2 folds
    ib: dict[str, Any] = {}
    res = {}
    for kind in ("FB8", "CFG", "FB8+CFG"):
        res[kind] = loco_rho_v2(chains, kind)
        pool = IB.pooled(res[kind])
        p, null = perm_p_v2(chains, kind, pool["mean_rho"], IB.N_PERM, IB.PERM_SEED)
        by_cohort = {}
        for camp, arm in IB.COHORTS:
            sub = {k: v for k, v in res[kind].items() if k[0] == camp and chains[k][0]["arm"] == arm}
            by_cohort[f"{camp}/{arm}"] = IB.pooled(sub)
        ib[kind] = {**pool, "perm_p": p, "n_perm": IB.N_PERM, "null_mean": IB._mean(null),
                    "null_p95": sorted(null)[int(0.95 * len(null))], "by_cohort": by_cohort,
                    "per_chain_rho": {f"{k[0]}/{k[1]}": v[0] for k, v in res[kind].items()}}
    diffs = [res["FB8+CFG"][k][0] - res["CFG"][k][0] for k in chains
             if res["FB8+CFG"][k][0] is not None and res["CFG"][k][0] is not None]
    ib["FB8+CFG_minus_CFG"] = {"mean_diff": IB._mean(diffs), "n": len(diffs),
                               "signflip_p": IB.signflip_p(diffs, IB.SIGNFLIP_N, IB.SIGNFLIP_SEED)}
    ib_gates = IB.evaluate_gates(ib_controls, ib)

    # RS under V2 folds
    preds = {kind: loco_predictions_v2(chains, kind) for kind in RS.KINDS}
    pairs = RS.make_pairs(chains, preds)
    rs_controls = [c_twins, c_fold, IB.control_m2_m3_reproduced(chains), RS.control_recoverable_positive(pairs),
                   control_planted_ships_v2(chains), control_rs_nullcal_v2(chains)]
    by_kind = {kind: RS.contrasts(pairs, kind) for kind in RS.KINDS}
    rs_gates = RS.evaluate_gates(rs_controls, by_kind[RS.PRIMARY_KIND])

    v1_ib = json.loads((HERE / "rollup-e40-channel-ib" / "E40_CHANNEL_IB_ROLLUP_V1.json").read_text())
    v1_rs = json.loads(RS.ROLLUP.read_text())
    rollup = {
        "schema_version": SCHEMA, "design": DESIGN,
        "design_json_sha256": IB.sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else None,
        "script_sha256": IB.sha256_file(Path(__file__)), "tuples_sha256": IB.sha256_file(IB.TUPLES),
        "v1_ib_rollup_sha256": IB.sha256_file(HERE / "rollup-e40-channel-ib" / "E40_CHANNEL_IB_ROLLUP_V1.json"),
        "v1_rs_rollup_sha256": IB.sha256_file(RS.ROLLUP),
        "interpreter": sys.version.split()[0],
        "fold": "leave-one-chain-out with the held-out chain's exact-config twins removed from the training fold",
        "inherited_unchanged": ["ridge lambda", "feature sets", "statistics", "permutation and sign-flip nulls and seeds",
                                "plant and null-calibration constants", "gates", "routing", "pairing"],
        "twin_census": census,
        "ib": {"controls": ib_controls, "information_bound": ib, "gates": ib_gates,
               "v1_for_comparison_WITHDRAWN": {k: {"mean_rho": v1_ib["information_bound"][k]["mean_rho"],
                                                    "perm_p": v1_ib["information_bound"][k]["perm_p"]}
                                               for k in ("FB8", "CFG", "FB8+CFG")}},
        "rs": {"controls": rs_controls, "contrasts": by_kind, "gates": rs_gates,
               "pairs": pairs,
               "v1_for_comparison_WITHDRAWN": {"recovered_fraction": v1_rs["gates"].get("recovered_fraction"),
                                               "terminal": v1_rs["gates"].get("terminal")}},
        "authority": {"grants_scientific_truth": False, "revives_e40": False, "authorizes_m6": False,
                      "grants_field_status": False},
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rollup, indent=1, sort_keys=True) + "\n")
    print(f"interpreter {sys.version.split()[0]}")
    print(f"twins: {census['twin_configs_across_chains']} configs, {census['rows_with_a_twin_in_another_chain']} rows, "
          f"{census['chains_whose_v1_fold_was_contaminated']}/36 V1 folds contaminated")
    for c in ib_controls:
        print(f"IB control {c['control']}: {'PASS' if c['pass'] else 'FAIL'}")
    for kind in ("FB8", "CFG", "FB8+CFG"):
        x = ib[kind]
        print(f"IB {kind:8s} V2 mean_rho {x['mean_rho']:+.4f} top1 {x['top1_hit_rate']:.3f} perm_p {x['perm_p']:.4f} "
              f"(V1 withdrawn: {v1_ib['information_bound'][kind]['mean_rho']:+.4f}, p {v1_ib['information_bound'][kind]['perm_p']:.4f})")
    d = ib["FB8+CFG_minus_CFG"]
    print(f"IB FB8+CFG - CFG {d['mean_diff']:+.4f} signflip_p {d['signflip_p']:.4f}")
    print("IB gates", json.dumps(ib_gates))
    for c in rs_controls:
        print(f"RS control {c['control']}: {'PASS' if c['pass'] else 'FAIL'}")
    pk = by_kind[RS.PRIMARY_KIND]["pooled"]
    print(f"RS recovered_fraction {pk['recovered_fraction']} (V1 withdrawn {v1_rs['gates'].get('recovered_fraction')}); "
          f"P2 mean {pk['P2_improvement_f2final_minus_f2ship']['mean_d']:+.5f} p_pos {pk['P2_improvement_f2final_minus_f2ship']['p_pos']:.4f}; "
          f"P1 drag {pk['P1_f0best_minus_f2ship']['mean_d']:+.5f} p_neg {pk['P1_f0best_minus_f2ship']['p_neg']:.4f}")
    print("RS gates", json.dumps(rs_gates))
    print(f"rollup {out} sha256 {IB.sha256_file(out)}")
    if not (ib_gates["IB0_CONTROLS_VALID"] and rs_gates["RS0_CONTROLS_VALID"]):
        return 4
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "census"])
    ap.add_argument("--out", type=Path, default=ROLLUP)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "census":
            print(json.dumps(twin_census(IB.chains_of(IB.load_rows())), indent=1))
            return 0
        return run(a.out)
    except IB.CannotCheck as exc:
        print(f"CANNOT_CHECK: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
