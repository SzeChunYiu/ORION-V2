#!/usr/bin/env python3
"""E40 channel information bound — registered re-analysis over the frozen m2/m3 tuples.

Question (frozen in E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1): does ANY linear function of
the eight cycle-visible feedback fields rank the held-out primary (wasserstein mean, lower
better) OUT OF SAMPLE, i.e. when the ranker is fitted on every other chain and applied to a
chain it never saw?  m5' Stage-1 screened twelve frozen composites in-sample and found no
selector; this is the "any (linear) function" step that saturates the feedback-channel
lever class, and it separates the feedback signal from the prior over configurations.

Zero model calls, zero native runs.  Pure Python (no numpy in the project environment);
every sum is `math.fsum`; every RNG draw is seeded from the design and consumed in a fixed
order, never over an unordered container.

Exit codes -- "could not check" keeps its own code:
  0  measured (rollup written)
  5  CANNOT_CHECK: a registered control failed, or an envelope is invalid; nothing filed
  2  usage / input error
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROLLUP_DIR = HERE / "rollup-e40-channel-ib"
TUPLES = ROLLUP_DIR / "E40_CHANNEL_IB_TUPLES_V1.json"
DESIGN_JSON = HERE / "E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1.json"
M4_ROLLUP = HERE / "rollup-m4" / "E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.json"

SCHEMA = "orion.v2.e40-channel-information-bound.rollup.v1"

FEEDBACK_FIELDS = (
    "chipseq_evaluation", "corum_evaluation", "ligand_receptor_evaluation",
    "pooled_biological_evaluation", "pooled_biological_sigificant_evaluation",
    "run_time", "string_network_evaluation", "string_physical_evaluation",
)
REGIMES = ("observational", "partial_interventional", "interventional")
COHORTS = (("campaign-e40-m2", "f0"), ("campaign-e40-m2", "f2"), ("campaign-e40-m3", "f2"))

# ---- frozen analysis constants (design S4) ------------------------------------------
RIDGE_LAMBDA = 1.0
N_PERM = 2000
PERM_SEED = 20260904
SIGNFLIP_N = 4000
SIGNFLIP_SEED = 20260904
PLANT_SEED = 20260904
PLANT_NOISE_SD_FRACTION = 0.25
PLANT_MIN_RHO = 0.5
NULLCAL_REPS = 100
NULLCAL_PERMS = 200
NULLCAL_SEED = 20260903
NULLCAL_BAND = (0.02, 0.09)
ALPHA = 0.05
REPRO_TOL_RHO = 1e-9
REPRO_TOL_D = 1e-6


class CannotCheck(Exception):
    pass


# ---- small linear algebra, pure python ---------------------------------------------

def _solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting.  a is n x n, SPD by construction."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        if abs(p) < 1e-14:
            raise CannotCheck("singular normal equations")
        for j in range(col, n + 1):
            m[col][j] /= p
        for r in range(n):
            if r != col and m[r][col] != 0.0:
                f = m[r][col]
                for j in range(col, n + 1):
                    m[r][j] -= f * m[col][j]
    return [m[i][n] for i in range(n)]


def _ridge_fit(x: list[list[float]], y: list[float], lam: float) -> tuple[list[float], float, list[float], list[float]]:
    """Standardise columns on the training fold, centre y, solve (X'X + lam I) w = X'y."""
    n, p = len(x), len(x[0])
    mu = [math.fsum(row[j] for row in x) / n for j in range(p)]
    sd = []
    for j in range(p):
        v = math.fsum((row[j] - mu[j]) ** 2 for row in x) / max(1, n - 1)
        sd.append(math.sqrt(v) if v > 0 else 1.0)
    z = [[(row[j] - mu[j]) / sd[j] for j in range(p)] for row in x]
    ym = math.fsum(y) / n
    yc = [v - ym for v in y]
    xtx = [[math.fsum(z[i][a] * z[i][b] for i in range(n)) + (lam if a == b else 0.0)
            for b in range(p)] for a in range(p)]
    xty = [math.fsum(z[i][a] * yc[i] for i in range(n)) for a in range(p)]
    w = _solve(xtx, xty)
    return w, ym, mu, sd


def _ridge_predict(w: list[float], ym: float, mu: list[float], sd: list[float], x: list[list[float]]) -> list[float]:
    return [ym + math.fsum(w[j] * (row[j] - mu[j]) / sd[j] for j in range(len(w))) for row in x]


def _ranks(v: list[float]) -> list[float]:
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(a: list[float], b: list[float]) -> float | None:
    if len(a) < 3:
        return None
    ra, rb = _ranks(a), _ranks(b)
    ma, mb = math.fsum(ra) / len(ra), math.fsum(rb) / len(rb)
    num = math.fsum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = math.sqrt(math.fsum((x - ma) ** 2 for x in ra))
    db = math.sqrt(math.fsum((y - mb) ** 2 for y in rb))
    if da == 0.0 or db == 0.0:
        return None
    return num / (da * db)


# ---- data ---------------------------------------------------------------------------

def load_rows(path: Path = TUPLES) -> list[dict[str, Any]]:
    d = json.loads(path.read_text())
    rows = d["rows"]
    # envelope validity: every row carries every field, cohort sizes are exact
    for r in rows:
        for f in FEEDBACK_FIELDS:
            if f not in r["feedback"]:
                raise CannotCheck(f"{r['chain']} cycle {r['cycle']}: feedback lacks {f}")
        if r["regime"] not in REGIMES:
            raise CannotCheck(f"{r['chain']}: unknown regime {r['regime']!r}")
    counts = Counter((r["campaign"], r["arm"]) for r in rows)
    for c in COHORTS:
        if counts.get(c) != 48:
            raise CannotCheck(f"cohort {c} has {counts.get(c)} rows, expected 48")
    return rows


def chains_of(rows: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for r in rows:
        out.setdefault((r["campaign"], r["chain"]), []).append(r)
    for k, v in out.items():
        v.sort(key=lambda r: r["cycle"])
        if len(v) != 4:
            raise CannotCheck(f"chain {k} has {len(v)} rows, expected 4")
    return dict(sorted(out.items()))


def features(row: dict[str, Any], kind: str) -> list[float]:
    fb = [float(row["feedback"][f]) for f in FEEDBACK_FIELDS]
    cfg = [1.0 if row["regime"] == g else 0.0 for g in REGIMES] + [row["frac"], row["frac"] ** 2]
    if kind == "FB8":
        return fb
    if kind == "CFG":
        return cfg
    if kind == "FB8+CFG":
        return fb + cfg
    raise ValueError(kind)


# ---- the leave-one-chain-out ranker ----------------------------------------------------

def loco_rho(chains: dict[tuple[str, str], list[dict[str, Any]]], kind: str,
             truth: dict[tuple[str, str], list[float]] | None = None,
             lam: float = RIDGE_LAMBDA) -> dict[tuple[str, str], tuple[float | None, bool]]:
    """Per held-out chain: (Spearman(pred, truth), top1_hit).  Positive rho = ranks truth."""
    keys = list(chains)
    out: dict[tuple[str, str], tuple[float | None, bool]] = {}
    for held in keys:
        xtr: list[list[float]] = []
        ytr: list[float] = []
        for k in keys:
            if k == held:
                continue
            ys = truth[k] if truth else [r["truth_wasserstein"] for r in chains[k]]
            for r, y in zip(chains[k], ys):
                xtr.append(features(r, kind))
                ytr.append(y)
        w, ym, mu, sd = _ridge_fit(xtr, ytr, lam)
        xte = [features(r, kind) for r in chains[held]]
        yte = truth[held] if truth else [r["truth_wasserstein"] for r in chains[held]]
        pred = _ridge_predict(w, ym, mu, sd, xte)
        rho = spearman(pred, yte)
        top1 = min(range(4), key=lambda i: pred[i]) == min(range(4), key=lambda i: yte[i])
        out[held] = (rho, top1)
    return out


def _mean(vals: list[float]) -> float:
    return math.fsum(vals) / len(vals) if vals else float("nan")


def pooled(res: dict[tuple[str, str], tuple[float | None, bool]]) -> dict[str, Any]:
    rhos = [v[0] for v in res.values() if v[0] is not None]
    return {"n_chains": len(res), "n_rho_defined": len(rhos), "mean_rho": _mean(rhos),
            "top1_hit_rate": _mean([1.0 if v[1] else 0.0 for v in res.values()])}


def perm_p(chains, kind: str, observed: float, n_perm: int, seed: int) -> tuple[float, list[float]]:
    """Within-chain permutation of truth, full LOCO refit each time.  One-sided (>=)."""
    rng = random.Random(seed)
    keys = list(chains)
    null: list[float] = []
    for _ in range(n_perm):
        truth = {}
        for k in keys:
            ys = [r["truth_wasserstein"] for r in chains[k]]
            rng.shuffle(ys)
            truth[k] = ys
        res = loco_rho(chains, kind, truth)
        null.append(pooled(res)["mean_rho"])
    ge = sum(1 for v in null if v >= observed - 1e-12)
    return (ge + 1) / (n_perm + 1), null


def signflip_p(diffs: list[float], n: int, seed: int) -> float:
    rng = random.Random(seed)
    obs = _mean(diffs)
    ge = 0
    for _ in range(n):
        s = _mean([d if rng.random() < 0.5 else -d for d in diffs])
        if s >= obs - 1e-12:
            ge += 1
    return (ge + 1) / (n + 1)


# ---- controls ---------------------------------------------------------------------------

def control_planted(chains) -> dict[str, Any]:
    """Overwrite run_time with truth + noise on a COPY; the FB8 ranker must then fire."""
    rng = random.Random(PLANT_SEED)
    ys = [r["truth_wasserstein"] for rs in chains.values() for r in rs]
    m = _mean(ys)
    sd = math.sqrt(math.fsum((y - m) ** 2 for y in ys) / (len(ys) - 1))
    planted = {}
    for k, rs in chains.items():
        planted[k] = []
        for r in rs:
            r2 = dict(r)
            r2["feedback"] = dict(r["feedback"])
            r2["feedback"]["run_time"] = r["truth_wasserstein"] + rng.gauss(0.0, PLANT_NOISE_SD_FRACTION * sd)
            planted[k].append(r2)
    res = loco_rho(planted, "FB8")
    pool = pooled(res)
    p, _ = perm_p(planted, "FB8", pool["mean_rho"], 400, PERM_SEED)
    ok = pool["mean_rho"] >= PLANT_MIN_RHO and p <= ALPHA
    return {"control": "PLANTED_SIGNAL_DETECTED", "pass": ok, "mean_rho": pool["mean_rho"],
            "top1_hit_rate": pool["top1_hit_rate"], "perm_p": p, "n_perm": 400,
            "rule": f"mean_rho >= {PLANT_MIN_RHO} and perm_p <= {ALPHA}"}


def control_nullcal(chains) -> dict[str, Any]:
    """Shuffle truth within chains REPS times; the test must reject at ~alpha."""
    rng = random.Random(NULLCAL_SEED)
    keys = list(chains)
    rejections = 0
    for rep in range(NULLCAL_REPS):
        truth = {}
        for k in keys:
            ys = [r["truth_wasserstein"] for r in chains[k]]
            rng.shuffle(ys)
            truth[k] = ys
        fake = {k: [dict(r, truth_wasserstein=y) for r, y in zip(chains[k], truth[k])] for k in keys}
        obs = pooled(loco_rho(fake, "FB8"))["mean_rho"]
        p, _ = perm_p(fake, "FB8", obs, NULLCAL_PERMS, NULLCAL_SEED + 1 + rep)
        if p <= ALPHA:
            rejections += 1
    rate = rejections / NULLCAL_REPS
    ok = NULLCAL_BAND[0] <= rate <= NULLCAL_BAND[1]
    return {"control": "NULL_CALIBRATION", "pass": ok, "rejection_rate": rate,
            "reps": NULLCAL_REPS, "perms": NULLCAL_PERMS, "band": list(NULLCAL_BAND)}


def control_m4_reproduced(chains) -> dict[str, Any]:
    """Per-chain raw Spearman(pooled_tp, wasserstein), arithmetic mean over the 12 F2 chains
    of each cohort, must equal m4's frozen M1 pooled_rho_arithmetic to 1e-9."""
    m4 = json.loads(M4_ROLLUP.read_text())["analysis"]
    expected = {("campaign-e40-m3", "f2"): m4["P_primary"]["M1_mechanism"]["pooled_rho_arithmetic"],
                ("campaign-e40-m2", "f2"): m4["R_replication"]["M1_mechanism"]["pooled_rho_arithmetic"]}
    got = {}
    for (camp, arm), exp in expected.items():
        rhos = []
        for (c, name), rs in chains.items():
            if c != camp or rs[0]["arm"] != arm:
                continue
            rho = spearman([float(r["feedback"]["pooled_biological_evaluation"]) for r in rs],
                           [r["truth_wasserstein"] for r in rs])
            rhos.append(0.0 if rho is None else rho)
        got[f"{camp}/{arm}"] = {"mean_rho": _mean(rhos), "expected": exp, "n_chains": len(rhos),
                                "abs_delta": abs(_mean(rhos) - exp)}
    ok = all(v["abs_delta"] <= REPRO_TOL_RHO and v["n_chains"] == 12 for v in got.values())
    return {"control": "M4_M1_REPRODUCED", "pass": ok, "per_cohort": got, "tol": REPRO_TOL_RHO}


def control_m2_m3_reproduced(chains) -> dict[str, Any]:
    """m2 primary mean_d (F0_best - F2_final) = -0.008979, m3 = -0.007414 (m3 F2 vs m2 F0);
    m2 F0 best-of-4 regime census = interventional 5 / observational 4 / partial 3."""
    f0 = {(rs[0]["dataset"], rs[0]["rep"]): rs for (c, n), rs in chains.items()
          if c == "campaign-e40-m2" and rs[0]["arm"] == "f0"}
    out = {}
    for camp, exp in (("campaign-e40-m2", -0.008979), ("campaign-e40-m3", -0.007414)):
        ds = []
        for (c, n), rs in chains.items():
            if c != camp or rs[0]["arm"] != "f2":
                continue
            best = min(r["truth_wasserstein"] for r in f0[(rs[0]["dataset"], rs[0]["rep"])])
            final = rs[-1]["truth_wasserstein"]
            ds.append(best - final)
        out[camp] = {"mean_d": _mean(ds), "expected_receipt_rounded": exp, "n_pairs": len(ds),
                     "abs_delta": abs(_mean(ds) - exp)}
    census = Counter()
    for rs in f0.values():
        best = min(rs, key=lambda r: r["truth_wasserstein"])
        census[best["regime"]] += 1
    census_ok = (census.get("interventional") == 5 and census.get("observational") == 4
                 and census.get("partial_interventional") == 3)
    ok = all(v["abs_delta"] <= REPRO_TOL_D and v["n_pairs"] == 12 for v in out.values()) and census_ok
    return {"control": "M2_M3_PRIMARY_AND_CENSUS_REPRODUCED", "pass": ok, "primary": out,
            "f0_best_regime_census": dict(census), "expected_census":
            {"interventional": 5, "observational": 4, "partial_interventional": 3}, "tol": REPRO_TOL_D}


# ---- gates and routing -------------------------------------------------------------------

def evaluate_gates(controls: list[dict[str, Any]], ib: dict[str, Any]) -> dict[str, Any]:
    """Controls are CONSUMED here: any failure refuses every gate (UNGATED_CONTROL_VERDICT guard)."""
    controls_ok = all(c["pass"] for c in controls)
    if not controls_ok:
        return {"IB0_CONTROLS_VALID": False, "IB1": None, "IB2": None, "IB3": None,
                "terminal": "CANNOT_CHECK__CONTROL_FAILED",
                "failed_controls": [c["control"] for c in controls if not c["pass"]]}
    ib1 = ib["FB8"]["mean_rho"] > 0 and ib["FB8"]["perm_p"] <= ALPHA
    ib2 = ib["CFG"]["mean_rho"] > 0 and ib["CFG"]["perm_p"] <= ALPHA
    ib3 = ib["FB8+CFG_minus_CFG"]["mean_diff"] > 0 and ib["FB8+CFG_minus_CFG"]["signflip_p"] <= ALPHA
    if ib1:
        terminal = "OOS_RANKER_EXISTS__PROSPECTIVE_M5PP_WARRANTED"
    elif ib2:
        terminal = "CHANNEL_INFORMATION_BOUND__PRIOR_OVER_CONFIGS_IS_THE_ONLY_OOS_SIGNAL"
    else:
        terminal = "CHANNEL_INFORMATION_BOUND__NO_OOS_SIGNAL_IN_FEEDBACK_OR_CONFIG"
    return {"IB0_CONTROLS_VALID": True, "IB1_FEEDBACK_RANKS_TRUTH_OOS": ib1,
            "IB2_CONFIG_RANKS_TRUTH_OOS": ib2, "IB3_FEEDBACK_ADDS_TO_CONFIG": ib3,
            "terminal": terminal}


def descriptive(chains) -> dict[str, Any]:
    """Non-gating: per-field within-chain raw Spearman by cohort, and the extreme-regime census."""
    per_field: dict[str, dict[str, float]] = {}
    for f in FEEDBACK_FIELDS:
        per_field[f] = {}
        for camp, arm in COHORTS:
            rhos = []
            for (c, n), rs in chains.items():
                if c != camp or rs[0]["arm"] != arm:
                    continue
                rho = spearman([float(r["feedback"][f]) for r in rs], [r["truth_wasserstein"] for r in rs])
                rhos.append(0.0 if rho is None else rho)
            per_field[f][f"{camp}/{arm}"] = _mean(rhos)
    extreme = Counter()
    for (c, n), rs in chains.items():
        best = min(rs, key=lambda r: r["truth_wasserstein"])
        extreme[(f"{c}/{rs[0]['arm']}", "extreme" if best["regime"] != "partial_interventional" else "interior")] += 1
    return {"per_field_mean_within_chain_raw_spearman_vs_wasserstein": per_field,
            "true_best_cycle_regime_class_census": {f"{k[0]}|{k[1]}": v for k, v in sorted(extreme.items())},
            "note": "raw Spearman: positive = the field rises with wasserstein (i.e. anti-truth). "
                    "Descriptive only; the gates use the out-of-sample ranker."}


# ---- run ---------------------------------------------------------------------------------

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(out_dir: Path) -> int:
    rows = load_rows()
    chains = chains_of(rows)
    controls = [control_m4_reproduced(chains), control_m2_m3_reproduced(chains),
                control_planted(chains), control_nullcal(chains)]
    ib: dict[str, Any] = {}
    res = {}
    for kind in ("FB8", "CFG", "FB8+CFG"):
        res[kind] = loco_rho(chains, kind)
        pool = pooled(res[kind])
        p, null = perm_p(chains, kind, pool["mean_rho"], N_PERM, PERM_SEED)
        by_cohort = {}
        for camp, arm in COHORTS:
            sub = {k: v for k, v in res[kind].items() if k[0] == camp and chains[k][0]["arm"] == arm}
            by_cohort[f"{camp}/{arm}"] = pooled(sub)
        ib[kind] = {**pool, "perm_p": p, "n_perm": N_PERM, "null_mean": _mean(null),
                    "null_p95": sorted(null)[int(0.95 * len(null))], "by_cohort": by_cohort,
                    "per_chain_rho": {f"{k[0]}/{k[1]}": v[0] for k, v in res[kind].items()}}
    diffs = []
    for k in chains:
        a, b = res["FB8+CFG"][k][0], res["CFG"][k][0]
        if a is not None and b is not None:
            diffs.append(a - b)
    ib["FB8+CFG_minus_CFG"] = {"mean_diff": _mean(diffs), "n": len(diffs),
                               "signflip_p": signflip_p(diffs, SIGNFLIP_N, SIGNFLIP_SEED)}
    gates = evaluate_gates(controls, ib)
    rollup = {
        "schema_version": SCHEMA, "design": "E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1",
        "design_json_sha256": sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else None,
        "tuples_sha256": sha256_file(TUPLES), "script_sha256": sha256_file(Path(__file__)),
        "interpreter": sys.version.split()[0],
        "constants": {"ridge_lambda": RIDGE_LAMBDA, "n_perm": N_PERM, "perm_seed": PERM_SEED,
                      "signflip_n": SIGNFLIP_N, "signflip_seed": SIGNFLIP_SEED, "plant_seed": PLANT_SEED,
                      "plant_noise_sd_fraction": PLANT_NOISE_SD_FRACTION, "plant_min_rho": PLANT_MIN_RHO,
                      "nullcal": {"reps": NULLCAL_REPS, "perms": NULLCAL_PERMS, "seed": NULLCAL_SEED,
                                  "band": list(NULLCAL_BAND)}, "alpha": ALPHA},
        "n_rows": len(rows), "n_chains": len(chains),
        "controls": controls, "information_bound": ib, "gates": gates,
        "descriptive": descriptive(chains),
        "authority": {"grants_scientific_truth": False, "revives_e40": False,
                      "authorizes_m6": False, "grants_field_status": False},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    jp = out_dir / "E40_CHANNEL_IB_ROLLUP_V1.json"
    jp.write_text(json.dumps(rollup, indent=1, sort_keys=True) + "\n")
    print(f"interpreter {sys.version.split()[0]}")
    for c in controls:
        print(f"control {c['control']}: {'PASS' if c['pass'] else 'FAIL'}")
    for kind in ("FB8", "CFG", "FB8+CFG"):
        x = ib[kind]
        print(f"{kind:8s} mean_rho {x['mean_rho']:+.4f} top1 {x['top1_hit_rate']:.3f} perm_p {x['perm_p']:.4f} "
              f"(null mean {x['null_mean']:+.4f}, p95 {x['null_p95']:+.4f})")
    d = ib["FB8+CFG_minus_CFG"]
    print(f"FB8+CFG - CFG mean_diff {d['mean_diff']:+.4f} signflip_p {d['signflip_p']:.4f}")
    print("gates", json.dumps(gates))
    print(f"rollup {jp} sha256 {sha256_file(jp)}")
    if not gates["IB0_CONTROLS_VALID"]:
        return 5
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run"])
    ap.add_argument("--out", type=Path, default=ROLLUP_DIR)
    a = ap.parse_args(argv)
    try:
        return run(a.out)
    except CannotCheck as exc:
        print(f"CANNOT_CHECK: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
