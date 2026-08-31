#!/usr/bin/env python3
"""E40-m5' Stage-1 truth-calibration channel screen (frozen with design V1).

Registered re-analysis of the frozen m2/m3 F2 chain artifacts: for each of the
12 frozen candidate composites of the ALREADY-VISIBLE feedback fields, measure
whether it ranks truth (raw wasserstein). Select on cohort R (frozen m2 F2
chains), confirm on cohort P (frozen m3 F2 chains). Zero model calls, zero
native runs. Read-only over inputs; writes
E40_M5P_CHANNEL_SCREEN_ROLLUP_V1.{json,md}.

Design: research/experiments/e40-matched/E40_M5P_CHANNEL_SCREEN_DESIGN_V1.{md,json}
Conventions mirror the frozen m4 script verbatim (perm/shuffle form, chain-key
globbing, FORBIDDEN_SUBSTRINGS, sha manifest).
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
M4_ROLLUP = BASE / "campaign-e40-m4/run/rollup/E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.json"
M4_ROLLUP_SHA = "b8d2554097b43299a3aff8e200c580476baded8150b057e997a5f9898a732817"
OUT_DIR = Path(os.environ.get("E40M5P_OUT", str(BASE / "campaign-e40-m5p/stage1/rollup")))

DATASETS = ["weissmann_k562", "weissmann_rpe1"]
REPS = 6
CYCLES = [1, 2, 3, 4]
F0_MEMBERS = [f"run{i}" for i in range(4)]
FORBIDDEN_SUBSTRINGS = ["quantitative_test_evaluation", "wasserstein",
                        "false_omission_rate", "negative_mean_wasserstein"]
TP_FIELDS = ["pooled_biological_evaluation", "corum_evaluation", "string_network_evaluation",
             "string_physical_evaluation", "chipseq_evaluation", "ligand_receptor_evaluation"]
SHUFFLE_SEED, DRAWS = 20260831, 10000  # seed matches m4's M1 so GS0 is exact

RHO_GATE, P_GATE = 0.4, 0.05

_MANIFEST: list[dict] = []


def _sha(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    _MANIFEST.append({"path": str(path), "sha256": h})
    return h


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


def _z(xs: list[float]) -> list[float]:
    m, s = mean(xs), math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))
    return [(x - m) / s if s > 0 else 0.0 for x in xs]


def pearson(xs: list[float], ys: list[float]) -> float:
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def spearman(xs: list[float], ys: list[float]) -> float:
    return pearson(_ranks(xs), _ranks(ys))


def primary_score(metrics_path: Path) -> dict:
    with open(metrics_path) as fh:
        d = json.load(fh)
    qte = d["quantitative_test_evaluation"]
    og = qte["output_graph"]
    return {
        "primary": float(og["wasserstein_distance"]["mean"]),
        "true_positives": int(og["true_positives"]),
        "corum_tp": float(d["corum_evaluation"]["true_positives"]),
        "string_tp": float(d["string_network_evaluation"]["true_positives"]),
    }


def find_chain(chains_root: Path, arm_short: str, ds: str, rep: int) -> Path:
    hits = sorted(chains_root.glob(f"*_{arm_short}_{ds}_{rep}"))
    assert len(hits) == 1, f"chain key not unique: {arm_short} {ds} {rep} -> {hits}"
    return hits[0]


def best_by_primary(runs: list[dict]) -> dict:
    real = [r for r in runs if not (isinstance(r["primary"], float) and r["primary"] != r["primary"])]
    assert real, "no real run"
    return min(real, key=lambda r: r["primary"])


def candidate_scores(fb: list[dict]) -> dict[str, list[float]]:
    """Per-cycle scores for all 12 candidates from the chain's 4 feedback dicts."""
    def col(field: str) -> list[float]:
        return [float(x[field]["true_positives"]) for x in fb]

    rt = [float(x["run_time"]) for x in fb]
    pooled = col("pooled_biological_evaluation")
    pooled_sig = col("pooled_biological_sigificant_evaluation")
    zcols = {f: _z(col(f)) for f in TP_FIELDS}
    out = {
        "pooled_tp": pooled,
        "pooled_sig_tp": pooled_sig,
        "corum_tp": col("corum_evaluation"),
        "string_net_tp": col("string_network_evaluation"),
        "string_phys_tp": col("string_physical_evaluation"),
        "chipseq_tp": col("chipseq_evaluation"),
        "ligand_tp": col("ligand_receptor_evaluation"),
        "fast_runtime": rt,
        "zmean_tp": [mean([zcols[f][i] for f in TP_FIELDS]) for i in range(len(fb))],
        "rankmean_tp": [mean([_ranks(col(f))[i] for f in TP_FIELDS]) for i in range(len(fb))],
        "sig_purity": [s / max(p, 1.0) for s, p in zip(pooled_sig, pooled)],
        "efficiency": [a - b for a, b in zip(_z(pooled), _z(rt))],
    }
    assert len(out) == 12
    return out


DIRECTIONS = {"pooled_tp": 1, "pooled_sig_tp": 1, "corum_tp": 1, "string_net_tp": 1,
              "string_phys_tp": 1, "chipseq_tp": 1, "ligand_tp": 1, "fast_runtime": -1,
              "zmean_tp": 1, "rankmean_tp": 1, "sig_purity": 1, "efficiency": 1}


def build_cohort(tag: str, f2_root: Path) -> dict:
    chains = []
    for ds in DATASETS:
        for rep in range(REPS):
            f2_dir = find_chain(f2_root / "run/chains", "f2", ds, rep)
            fb_dicts, truth = [], []
            for c in CYCLES:
                fb_path = f2_dir / f"cycle{c}" / "redacted_feedback.json"
                text = fb_path.read_text()
                for s in FORBIDDEN_SUBSTRINGS:  # C2 leakage re-check
                    assert s not in text, f"redaction failed at {fb_path}: '{s}' present"
                _sha(fb_path)
                fb_dicts.append(json.loads(text))
                exp_id = (f2_dir / f"cycle{c}" / "exp_id").read_text().strip()
                _sha(f2_dir / f"cycle{c}" / "exp_id")
                truth.append(primary_score(f2_root / "run/results" / exp_id / "metrics.json")["primary"])
            chains.append({"key": f"{ds}:{rep}", "feedback": fb_dicts, "truth": truth,
                           "scores": candidate_scores(fb_dicts)})
    f0_bests = {}
    for ds in DATASETS:
        for rep in range(REPS):
            d = find_chain(M2_ROOT / "run/chains", "f0", ds, rep)
            runs = []
            for name in F0_MEMBERS:
                exp_id = (d / name / "exp_id").read_text().strip()
                _sha(d / name / "exp_id")
                runs.append({"run": name, **primary_score(M2_ROOT / "run/results" / exp_id / "metrics.json")})
            f0_bests[f"{ds}:{rep}"] = best_by_primary(runs)
    return {"tag": tag, "chains": chains, "f0_bests": f0_bests, "status": "OK"}


def eval_candidate(cohort: dict, cand: str) -> dict:
    rhos, excluded = [], []
    usable = []
    for ch in cohort["chains"]:
        pairs = [(s, t) for s, t in zip(ch["scores"][cand], ch["truth"]) if math.isfinite(t) and math.isfinite(s)]
        if len(pairs) < 3:
            excluded.append(ch["key"])
            continue
        ss = [p[0] for p in pairs]
        tt = [p[1] for p in pairs]
        rhos.append(spearman(ss, tt))
        usable.append((ch, ss, tt))
    raw_pooled = mean(rhos)
    rng = random.Random(SHUFFLE_SEED)
    hits = 0
    for _ in range(DRAWS):
        perm = mean([spearman(rng.sample(ss, len(ss)), tt) for _, ss, tt in usable])
        if abs(perm) >= abs(raw_pooled):
            hits += 1
    return {"raw_pooled_rho": raw_pooled,
            "directed_pooled_rho": -DIRECTIONS[cand] * raw_pooled,
            "perm_p_two_sided": hits / DRAWS,
            "chains_used": len(rhos), "chains_excluded_lt3": excluded,
            "per_chain_rho": [f"{ch['key']}:{r:.4f}" for ch, r in zip([u[0] for u in usable], rhos)]}


def argmax_census(cohort: dict, cand: str) -> dict:
    rows = []
    for ch in cohort["chains"]:
        sc = [v * DIRECTIONS[cand] for v in ch["scores"][cand]]
        idx = sc.index(max(sc))  # earliest cycle wins ties (m4 convention)
        tr = _ranks(ch["truth"])
        f0b = cohort["f0_bests"][ch["key"]]
        rows.append({"key": ch["key"], "ship_cycle": CYCLES[idx], "ship_true_rank": tr[idx],
                     "tp_delta_vs_f0best": ch["feedback"][idx]["pooled_biological_evaluation"]["true_positives"]
                                           - f0b["true_positives"]})
    return {"ship_true_rank_mean": mean([r["ship_true_rank"] for r in rows]),
            "ship_cycle_census": {str(c): sum(1 for r in rows if r["ship_cycle"] == c) for c in CYCLES},
            "mean_tp_delta_vs_f0best": mean([r["tp_delta_vs_f0best"] for r in rows]),
            "rows": rows}


def loo_stability(cohort: dict, cand: str) -> dict:
    rhos = []
    for ch in cohort["chains"]:
        pairs = [(s, t) for s, t in zip(ch["scores"][cand], ch["truth"]) if math.isfinite(t) and math.isfinite(s)]
        if len(pairs) >= 3:
            rhos.append(spearman([p[0] for p in pairs], [p[1] for p in pairs]))
    return {"loo_min": min(mean(rhos[:i] + rhos[i + 1:]) for i in range(len(rhos))),
            "loo_max": max(mean(rhos[:i] + rhos[i + 1:]) for i in range(len(rhos)))}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rollup_sha = _sha(M4_ROLLUP)
    gs0_ok = rollup_sha == M4_ROLLUP_SHA
    m4 = json.loads(M4_ROLLUP.read_text())

    cohorts = {"P_confirm": build_cohort("P_confirm", M3_ROOT),
               "R_select": build_cohort("R_select", M2_ROOT)}
    table = {c: {k: eval_candidate(v, c) for k in v["chains"][0]["scores"]} for c, v in cohorts.items()}

    # GS0: reproduce m4's M1 for pooled_tp on both cohorts (raw rho + perm p)
    gs0_detail = {}
    for coh, m4_key in (("P_confirm", "P_primary"), ("R_select", "R_replication")):
        got = table[coh]["pooled_tp"]
        want = m4["analysis"][m4_key]["M1_mechanism"]
        gs0_detail[coh] = {"got_raw_rho": got["raw_pooled_rho"], "want_raw_rho": want["pooled_rho_arithmetic"],
                           "rho_ok": abs(got["raw_pooled_rho"] - want["pooled_rho_arithmetic"]) <= 1e-9,
                           "got_perm_p": got["perm_p_two_sided"], "want_perm_p": want["perm_p_two_sided"],
                           "perm_ok": abs(got["perm_p_two_sided"] - want["perm_p_two_sided"]) <= 1e-9}
        gs0_ok = gs0_ok and gs0_detail[coh]["rho_ok"] and gs0_detail[coh]["perm_ok"]

    r_rows = {k: v for k, v in table["R_select"].items() if k != "pooled_tp"}
    eligible = [k for k, v in r_rows.items() if v["perm_p_two_sided"] <= P_GATE and v["directed_pooled_rho"] > 0]
    winner = max(eligible, key=lambda k: r_rows[k]["directed_pooled_rho"]) if eligible else None
    gs1 = winner is not None
    gs2 = bool(winner and table["P_confirm"][winner]["directed_pooled_rho"] >= RHO_GATE
               and table["P_confirm"][winner]["perm_p_two_sided"] <= P_GATE)

    if gs2:
        route = ("draft m5-double-prime prospective interventional: fresh 12x4 F2 campaign, "
                 "winner composite surfaced in feedback+prompt, shipping = winner-argmax, m-series gates")
    elif gs1:
        route = "draft Stage-2b seed-replica stability-probe design (needs new native runs)"
    else:
        route = ("no visible composite ranks truth; draft Stage-2b seed-replica stability-probe design; "
                 "strengthens terminal reading if Stage-2b fails")

    gates = {"GS0_M4_REPRODUCED": gs0_ok, "GS0_detail": gs0_detail,
             "GS1_SELECTION_AVAILABLE_ON_R": gs1, "winner": winner,
             "GS2_WINNER_CONFIRMED_ON_P": gs2, "preregistered_route": route}

    extra = {}
    if winner:
        extra = {"winner_census_P": argmax_census(cohorts["P_confirm"], winner),
                 "winner_loo_P": loo_stability(cohorts["P_confirm"], winner),
                 "winner_census_R": argmax_census(cohorts["R_select"], winner)}

    rollup = {"schema_version": "orion.v2.e40-matched.m5p-stage1-rollup.v1",
              "variant": "e40-m5p-channel-screen",
              "design": "E40_M5P_CHANNEL_SCREEN_DESIGN_V1",
              "m4_rollup_sha256": rollup_sha,
              "table": table, "gates": gates, "winner_detail": extra,
              "manifest": {"n_files": len(_MANIFEST), "files": _MANIFEST}}
    (OUT_DIR / "E40_M5P_CHANNEL_SCREEN_ROLLUP_V1.json").write_text(
        json.dumps(rollup, indent=1, sort_keys=True))

    lines = ["# E40-m5' Stage-1 channel screen rollup V1", "",
             f"winner: {winner}", f"route: {route}", ""]
    for coh, cands in table.items():
        lines += [f"## {coh}", "| candidate | raw rho | directed rho | perm p | excl |", "|---|---|---|---|---|"]
        for k, v in sorted(cands.items()):
            lines.append(f"| {k} | {v['raw_pooled_rho']:+.4f} | {v['directed_pooled_rho']:+.4f} "
                         f"| {v['perm_p_two_sided']:.5f} | {len(v['chains_excluded_lt3'])} |")
        lines.append("")
    lines += ["## gates", json.dumps(gates, indent=1, sort_keys=True)]
    (OUT_DIR / "E40_M5P_CHANNEL_SCREEN_ROLLUP_V1.md").write_text("\n".join(lines) + "\n")

    print(json.dumps({"gates": {k: v for k, v in gates.items() if k != "GS0_detail"},
                      "R_top3": sorted(((k, round(v['directed_pooled_rho'], 4), round(v['perm_p_two_sided'], 4))
                                        for k, v in r_rows.items()),
                                       key=lambda t: -t[1])[:3]}, indent=1))
    return 0 if gs0_ok else 2


if __name__ == "__main__":
    sys.exit(main())
