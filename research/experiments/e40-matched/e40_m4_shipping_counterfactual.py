#!/usr/bin/env python3
"""E40-m4 shipping-operator counterfactual re-analysis (frozen with design V1).

Registered re-analysis of the frozen m2/m3 chain artifacts: F2 ships the cycle
argmax of the cycle-visible proxy (pooled_biological_evaluation.true_positives)
instead of the terminal cycle. Zero model calls, zero native runs. Read-only
over inputs; writes E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.{json,md}.

Design: research/experiments/e40-matched/E40_M4_SHIPPING_OPERATOR_COUNTERFACTUAL_DESIGN_V1.{md,json}
Conventions mirror the frozen m3 runner verbatim (primary_score, perm_paired_p,
FORBIDDEN_SUBSTRINGS, chain-key globbing).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
from pathlib import Path

BASE = Path(os.environ.get("E40M_BASE", "/projects/hep/fs9/users/scyiu/orion-v2-e45"))
M2_ROOT = BASE / "campaign-e40-m2"
M3_ROOT = BASE / "campaign-e40-m3"
OUT_DIR = Path(os.environ.get("E40M4_OUT", str(BASE / "campaign-e40-m4/run/rollup")))

DATASETS = ["weissmann_k562", "weissmann_rpe1"]
REPS = 6
CYCLES = [1, 2, 3, 4]
F0_MEMBERS = [f"run{i}" for i in range(4)]
FORBIDDEN_SUBSTRINGS = ["quantitative_test_evaluation", "wasserstein",
                        "false_omission_rate", "negative_mean_wasserstein"]
TP_CHANNELS = ["true_positives", "corum_tp", "string_tp"]
M1_SEED, M1_DRAWS = 20260831, 10000

# frozen m3 rollup numbers this script must reproduce (design G0)
FROZEN = {
    "primary_mean_d": -0.007413520834557391,
    "primary_perm_p": 0.986083984375,
    "tp_mean_d": -13.083333333333334,
    "tp_perm_p": 0.995849609375,
    "both_best_mean_d": -0.0012099336519952111,
}

_MANIFEST: list[dict] = []


def _sha(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    _MANIFEST.append({"path": str(path), "sha256": h})
    return h


def primary_score(metrics_path: Path) -> dict:
    """Verbatim convention of e40_matched_runner_m3.primary_score."""
    with open(metrics_path) as fh:
        d = json.load(fh)
    qte = d["quantitative_test_evaluation"]
    og = qte["output_graph"]
    return {
        "primary": float(og["wasserstein_distance"]["mean"]),
        "true_positives": int(og["true_positives"]),
        "false_positives": int(og["false_positives"]),
        "false_omission_rate": float(qte["false_omission_rate"]),
        "corum_tp": float(d["corum_evaluation"]["true_positives"]),
        "string_tp": float(d["string_network_evaluation"]["true_positives"]),
        "run_time": float(d["run_time"]),
    }


def perm_paired_p(diffs: list[float]) -> float:
    """Verbatim convention of e40_matched_runner_m3.perm_paired_p (exhaustive n<=16)."""
    n = len(diffs)
    if n == 0:
        return 1.0
    t_obs = sum(diffs) / n
    total = 2 ** n
    count = 0
    for mask in range(total):
        t = sum(d if (mask >> i) & 1 else -d for i, d in enumerate(diffs)) / n
        if t >= t_obs:
            count += 1
    return count / total


def find_chain(chains_root: Path, arm_short: str, ds: str, rep: int) -> Path:
    hits = sorted(chains_root.glob(f"*_{arm_short}_{ds}_{rep}"))
    assert len(hits) == 1, f"chain key not unique: {arm_short} {ds} {rep} -> {hits}"
    return hits[0]


def load_runs(chain_dir: Path, run_names: list[str], results_root: Path) -> list[dict]:
    runs = []
    for name in run_names:
        exp_id = (chain_dir / name / "exp_id").read_text().strip()
        _sha(chain_dir / name / "exp_id")
        runs.append({"run": name, "exp_id": int(exp_id),
                     **primary_score(results_root / exp_id / "metrics.json")})
    return runs


def best_by_primary(runs: list[dict]) -> dict:
    real = [r for r in runs if not (isinstance(r["primary"], float) and r["primary"] != r["primary"])]
    assert real, "no real run"
    return min(real, key=lambda r: r["primary"])


def load_proxy(chain_dir: Path) -> tuple[list[float], list[str]]:
    """Cycle-visible proxy scalars (pooled_biological_evaluation.true_positives)."""
    vals, blobs = [], []
    for c in CYCLES:
        fb_path = chain_dir / f"cycle{c}" / "redacted_feedback.json"
        text = fb_path.read_text()
        for s in FORBIDDEN_SUBSTRINGS:  # C2 leakage re-check
            assert s not in text, f"redaction failed at {fb_path}: '{s}' present"
        _sha(fb_path)
        fb = json.loads(text)
        vals.append(float(fb["pooled_biological_evaluation"]["true_positives"]))
        blobs.append(text)
    return vals, blobs


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def _ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def pearson(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def spearman(xs: list[float], ys: list[float]) -> float:
    return pearson(_ranks(xs), _ranks(ys))


def build_cohort(tag: str, f2_root: Path, f2_results: Path) -> dict:
    pairs = []
    fallback_chains = 0
    for ds in DATASETS:
        for rep in range(REPS):
            f0_dir = find_chain(M2_ROOT / "run/chains", "f0", ds, rep)
            f2_dir = find_chain(f2_root / "run/chains", "f2", ds, rep)
            f0_runs = load_runs(f0_dir, F0_MEMBERS, M2_ROOT / "run/results")
            f2_runs = load_runs(f2_dir, [f"cycle{c}" for c in CYCLES], f2_results)
            proxy, _ = load_proxy(f2_dir)
            f0_best = best_by_primary(f0_runs)
            f2_final = f2_runs[-1]
            f2_best = best_by_primary(f2_runs)

            finite = [i for i, p in enumerate(proxy) if math.isfinite(p)]
            if len(finite) < len(CYCLES):
                fallback_chains += 1
                ship_idx = len(CYCLES) - 1  # fall back to terminal
                fallback = True
            else:
                best_p = max(proxy)
                ship_idx = proxy.index(best_p)  # earliest cycle wins ties
                fallback = False
            ship = f2_runs[ship_idx]

            # true-rank of the shipped cycle (1 = best of 4, average ranks on ties)
            pr = _ranks([r["primary"] for r in f2_runs])
            pairs.append({
                "key": f"{ds}:{rep}", "dataset": ds, "rep": rep,
                "f0_best": f0_best, "f0_runs": f0_runs,
                "f2_final": f2_final, "f2_best": f2_best, "f2_ship": ship,
                "f2_runs": f2_runs, "proxy": proxy,
                "ship_cycle": CYCLES[ship_idx], "ship_fallback": fallback,
                "ship_true_rank": pr[ship_idx],
                "rho_proxy_truth": spearman(proxy, [r["primary"] for r in f2_runs]),
            })
    return {"tag": tag, "pairs": pairs, "fallback_chains": fallback_chains,
            "status": ("CANNOT_CHECK__PROXY_MISSING"
                       if fallback_chains > 2 else "OK")}


def contrasts(cohort: dict) -> dict:
    ps = cohort["pairs"]
    d_primary = [p["f0_best"]["primary"] - p["f2_ship"]["primary"] for p in ps]   # neg = F0 better
    d_recovery = [p["f2_final"]["primary"] - p["f2_ship"]["primary"] for p in ps]  # neg = ship better
    out = {
        "CT1_primary": {
            "contrast": "f0_best - f2_ship (raw wasserstein, negative = F0 better)",
            "mean_d": mean(d_primary), "perm_p": perm_paired_p(d_primary),
            "f0_wins": sum(1 for d in d_primary if d < 0),
            "f2_wins": sum(1 for d in d_primary if d > 0),
        },
        "CT2_recovery": {
            "contrast": "f2_final - f2_ship (negative = proxy shipping improves)",
            "mean_d": mean(d_recovery), "perm_p": perm_paired_p(d_recovery),
            "recovery_nonneg_chains": sum(1 for d in d_recovery if d <= 0),
        },
        "CT3_tp_family": {},
        "M1_mechanism": {},
        "M2_selection_census": {
            "ship_cycle_census": {str(c): sum(1 for p in ps if p["ship_cycle"] == c) for c in CYCLES},
            "ship_true_ranks": [p["ship_true_rank"] for p in ps],
            "ship_true_rank_mean": mean([p["ship_true_rank"] for p in ps]),
            "cycle1_persistence": sum(1 for p in ps if p["ship_cycle"] == 1),
        },
    }
    for ch in TP_CHANNELS:
        dd = [p["f2_ship"][ch] - p["f0_best"][ch] for p in ps]  # neg = F2 worse
        out["CT3_tp_family"][ch] = {"mean_d": mean(dd), "perm_p": perm_paired_p(dd)}
    rhos = [p["rho_proxy_truth"] for p in ps]
    obs = mean(rhos)
    rng = random.Random(M1_SEED)
    hits = 0
    for _ in range(M1_DRAWS):
        perm_rho = mean([spearman(rng.sample(p["proxy"], len(p["proxy"])),
                                  [r["primary"] for r in p["f2_runs"]]) for p in ps])
        if abs(perm_rho) >= abs(obs):
            hits += 1
    out["M1_mechanism"] = {
        "per_chain_rho": {p["key"]: p["rho_proxy_truth"] for p in ps},
        "pooled_rho_arithmetic": obs,
        "pooled_rho_fisher_z_reference": (math.tanh(mean([math.atanh(max(-0.999999, min(0.999999, r)))
                                                          for r in rhos]))),
        "perm_p_two_sided": hits / M1_DRAWS,
        "gate_eval_note": "G2 evaluates pooled_rho_arithmetic (Fisher-z is ill-defined at |rho|=1 with n=4; documented pre-compute in the design clarification)",
    }
    return out


def reproduce_m3(cohort: dict) -> dict:
    """G0: reproduce the frozen m3 rollup numbers from raw artifacts."""
    ps = cohort["pairs"]
    d_final = [p["f0_best"]["primary"] - p["f2_final"]["primary"] for p in ps]
    d_best = [p["f0_best"]["primary"] - p["f2_best"]["primary"] for p in ps]
    res = {
        "primary_mean_d": mean(d_final),
        "primary_perm_p": perm_paired_p(d_final),
        "both_best_mean_d": mean(d_best),
    }
    tp_orient = {}
    for name, dd in (("f2_minus_f0", [p["f2_final"]["true_positives"] - p["f0_best"]["true_positives"] for p in ps]),
                     ("f0_minus_f2", [p["f0_best"]["true_positives"] - p["f2_final"]["true_positives"] for p in ps])):
        tp_orient[name] = {"mean_d": mean(dd), "perm_p": perm_paired_p(dd)}
    ok_tp = {k: (abs(v["mean_d"] - FROZEN["tp_mean_d"]) <= 1e-9 and v["perm_p"] == FROZEN["tp_perm_p"])
             for k, v in tp_orient.items()}
    resolved = [k for k, ok in ok_tp.items() if ok]
    res["tp_family_by_orientation"] = tp_orient
    res["tp_orientation_resolved"] = resolved[0] if len(resolved) == 1 else None
    res["reproduced"] = (
        abs(res["primary_mean_d"] - FROZEN["primary_mean_d"]) <= 1e-9
        and res["primary_perm_p"] == FROZEN["primary_perm_p"]
        and abs(res["both_best_mean_d"] - FROZEN["both_best_mean_d"]) <= 1e-9
        and len(resolved) == 1
    )
    res["frozen_expected"] = FROZEN
    return res


def evaluate_gates(rep: dict, ct: dict) -> dict:
    g1 = (ct["CT1_primary"]["mean_d"] >= -0.001
          and ct["CT1_primary"]["perm_p"] <= 0.90
          and ct["CT2_recovery"]["recovery_nonneg_chains"] >= 8)
    g2 = (abs(ct["M1_mechanism"]["pooled_rho_arithmetic"]) < 0.2
          or ct["M1_mechanism"]["perm_p_two_sided"] > 0.05)
    if g1:
        route = "draft m5 prospective interventional: shipping rule = proxy-argmax (matched scale, m-series gates)"
    elif g2:
        route = "draft m5-prime feedback-channel design (calibrated extreme-resident probes / proxy-truth calibration)"
    else:
        route = "neither lever authorized; E40 line stays terminal-negative pending a new mechanism class"
    return {"G0_M3_REPRODUCED": rep["reproduced"],
            "G1_DRAG_ELIMINATED_UNDER_PROXY_SHIPPING": g1,
            "G2_PROXY_CHANNEL_UNINFORMATIVE": g2,
            "preregistered_route": route}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cohorts = {
        "P_primary": build_cohort("P_primary", M3_ROOT, M3_ROOT / "run/results"),
        "R_replication": build_cohort("R_replication", M2_ROOT, M2_ROOT / "run/results"),
    }
    repro = reproduce_m3(cohorts["P_primary"])
    analysis = {k: contrasts(c) for k, c in cohorts.items()}
    gates = (evaluate_gates(repro, analysis["P_primary"])
             if repro["reproduced"] else
             {"G0_M3_REPRODUCED": False, "status": "M4_CANNOT_RUN__REPRODUCTION_FAILED"})

    manifest = {"n_files": len(_MANIFEST), "files": _MANIFEST}
    rollup = {
        "schema_version": "orion.v2.e40-matched.m4-rollup.v1",
        "variant": "e40-m4-shipping-operator-counterfactual",
        "design": "E40_M4_SHIPPING_OPERATOR_COUNTERFACTUAL_DESIGN_V1",
        "cohorts": {k: {"status": c["status"], "fallback_chains": c["fallback_chains"],
                        "pairs": [{kk: p[kk] for kk in
                                   ("key", "ship_cycle", "ship_fallback", "ship_true_rank",
                                    "proxy", "rho_proxy_truth")}
                                  | {"f0_best_primary": p["f0_best"]["primary"],
                                     "f2_final_primary": p["f2_final"]["primary"],
                                     "f2_ship_primary": p["f2_ship"]["primary"],
                                     "f2_best_primary": p["f2_best"]["primary"]}
                                  for p in c["pairs"]]} for k, c in cohorts.items()},
        "reproduction": repro,
        "analysis": analysis,
        "gates": gates,
        "manifest": manifest,
    }
    (OUT_DIR / "E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.json").write_text(
        json.dumps(rollup, indent=1, sort_keys=True))

    lines = [f"# E40-m4 shipping-operator counterfactual rollup V1",
             "", f"reproduced m3 frozen numbers: {repro['reproduced']}",
             f"TP orientation resolved: {repro['tp_orientation_resolved']}", ""]
    for k, ct in analysis.items():
        lines += [f"## {k}", json.dumps(ct, indent=1, sort_keys=True), ""]
    lines += ["## gates", json.dumps(gates, indent=1, sort_keys=True)]
    (OUT_DIR / "E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.md").write_text("\n".join(lines) + "\n")

    print(json.dumps({"gates": gates,
                      "P_CT1": analysis["P_primary"]["CT1_primary"],
                      "R_CT1": analysis["R_replication"]["CT1_primary"]}, indent=1))
    return 0 if (repro["reproduced"] and all(c["status"] == "OK" for c in cohorts.values())) else 2


if __name__ == "__main__":
    sys.exit(main())
