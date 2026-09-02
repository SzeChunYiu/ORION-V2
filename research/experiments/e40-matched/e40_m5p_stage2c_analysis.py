#!/usr/bin/env python3
"""E40-m5' Stage-2c seed-replica stability-probe analysis (frozen with design V1).

Registered analysis of the campaign-e40-m5p-stage2c native runs (12 cells x 4
seed-replicas x 4 cycles = 192 runs, plus 12 in-campaign F0 federation chains
x 4 upfront runs = 48) — every arm produced under ONE pinned SERVED model
(design §2.2). The frozen m2 F0 chains, produced under an earlier and now
unrecoverable served model, are reported only as a HISTORICAL cross-model
panel that gates nothing:
  §3  probe statistic: per cell per cycle, consensus J_c = mean pairwise
      Jaccard of the replica output_network.csv edge sets; truth anchor
      T_c = mean_k wasserstein_k(c) (analysis-side only).
  §4  four shipping counterfactuals over the same 192 runs (TERMINAL,
      CONSENSUS-ARGMAX, PURITY-ARGMAX, ORACLE-BEST); contrast
      d = f0_best_primary - mean_k shipped_truth_k per cell (12 primary diffs).
  §5  pooled arithmetic mean of per-cell Spearman(J_c, T_c); within-cell
      cycle-shuffle two-sided permutation (10,000 draws, seed 20260902);
      exhaustive 2^12 sign-flip for contrasts; gates G0-G4.
  §6  pre-registered routing.
  §7  controls: planted / null calibration (400 reps, seed 20260830) /
      leakage assert on every feedback read / Jaccard selftest /
      edge-parse round-trip — executable (`selftest`), exercised through
      main() on synthetic campaign trees before the freeze.
Zero model calls, zero native runs. Read-only over inputs; refuses to run
(exit 3) until every one of the 48 chains is settled (COMPLETE or
CANNOT_CHECK); CANNOT_CHECK chains are excluded, counted and reported.
Writes E40_M5P_STAGE2B_ROLLUP_V1.{json,md}.

Design: research/experiments/e40-matched/E40_M5P_STAGE2C_SEED_REPLICA_PROBE_DESIGN_V1.{md,json}
Conventions mirror the frozen m3/m4/m5' scripts verbatim (primary_score,
perm_paired_p, spearman/_ranks, rng.sample per-cell shuffle, FORBIDDEN_SUBSTRINGS,
chain-key globbing, sha manifest, sig_purity = pooled_sig_tp / max(pooled_tp, 1)).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
from pathlib import Path

BASE = Path(os.environ.get("E40M_BASE", "/projects/hep/fs9/users/scyiu/orion-v2-e45"))
M2_ROOT = Path(os.environ.get("E40M_REF", str(BASE / "campaign-e40-m2")))
S2C_ROOT = Path(os.environ.get("E40M_ROOT", str(BASE / "campaign-e40-m5p-stage2c")))
OUT_DIR = Path(os.environ.get("E40M5P2C_OUT", str(S2C_ROOT / "run/rollup")))
# Frozen SERVED model id (design §2.2): every decision call logged by the runner
# must report this id, else the chain is CANNOT_CHECK here too (custody re-check).
SERVED_MODEL = os.environ.get("E40M_SERVED_MODEL", "glm-5.3")

DATASETS = ["weissmann_k562", "weissmann_rpe1"]
REPS = 6
CYCLES = [1, 2, 3, 4]
REPLICAS = ["f2r0", "f2r1", "f2r2", "f2r3"]
SEED_TABLE = {"f2r0": (11, 13), "f2r1": (29, 31), "f2r2": (47, 53), "f2r3": (71, 79)}
F0_MEMBERS = [f"run{i}" for i in range(4)]
FORBIDDEN_SUBSTRINGS = ["quantitative_test_evaluation", "wasserstein",
                        "false_omission_rate", "negative_mean_wasserstein"]
RULES = ["TERMINAL", "CONSENSUS_ARGMAX", "PURITY_ARGMAX", "ORACLE_BEST"]

RHO_SEED, RHO_DRAWS = 20260902, 10000       # design §5 (new stream)
NULLCAL_SEED, NULLCAL_REPS = 20260830, 400  # design §7 (m2/m3 form)
G0_MIN_F0_WINS = 8
G1_P, G2_D, G2_P = 0.05, -0.001, 0.10
MIN_REPLICAS_PER_CELL = 2                   # Jaccard needs a pair; fewer = cell CANNOT_CHECK

_MANIFEST: list[dict] = []


# ------------------------------------------------------------------ primitives
def _sha(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    _MANIFEST.append({"path": str(path), "sha256": h})
    return h


def mean(xs: list[float]) -> float:
    # math.fsum: correctly-rounded sum, identical on every CPython (plain sum()
    # switched to compensated summation in 3.12, which moved last-bit values and
    # flipped >= ties in the permutation counts between 3.11 and 3.13 — verified
    # on a shared fixture before the freeze). Interpreter-independent by design.
    return math.fsum(xs) / len(xs)


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
    num = math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(math.fsum((x - mx) ** 2 for x in xs) * math.fsum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def spearman(xs: list[float], ys: list[float]) -> float:
    return pearson(_ranks(xs), _ranks(ys))


def perm_paired_p(diffs: list[float]) -> float:
    """Verbatim m-series convention: one-sided P(T_perm >= T_obs), positive = F2 better.
    Exhaustive sign-flip (2^n) for n <= 16; larger n is never fed here.
    Sums via math.fsum (interpreter-independent; see mean())."""
    n = len(diffs)
    if n == 0:
        return 1.0
    assert n <= 16, "exhaustive sign-flip only (design §5); do not feed >16 diffs"
    t_obs = math.fsum(diffs) / n
    total = 2 ** n
    count = 0
    for mask in range(total):
        t = math.fsum(d if (mask >> i) & 1 else -d for i, d in enumerate(diffs)) / n
        if t >= t_obs:
            count += 1
    return count / total


def _is_nan(x: float) -> bool:
    return isinstance(x, float) and x != x


def primary_score(metrics_path: Path) -> dict:
    """Verbatim convention of e40_matched_runner_m3.primary_score (truth opened HERE only)."""
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


def best_by_primary(runs: list[dict]) -> dict | None:
    real = [r for r in runs if not _is_nan(r["primary"])]
    if not real:
        return None
    return min(real, key=lambda r: r["primary"])


# --------------------------------------------------------------- edge parsing
def parse_edges(path: Path) -> set[tuple[str, str]]:
    """output_network.csv (upstream pandas dump): header ',0,1' then 'idx,src,dst'.
    Directed edge = (src, dst); the row index is discarded. Loud on any other shape."""
    edges: set[tuple[str, str]] = set()
    lines = path.read_text().splitlines()
    if not lines:
        raise ValueError(f"{path}: empty edge file")
    header = [c.strip() for c in lines[0].split(",")]
    if len(header) != 3 or header[1:] != ["0", "1"]:
        raise ValueError(f"{path}: unexpected header {lines[0]!r}")
    for ln in lines[1:]:
        if not ln.strip():
            continue
        cols = [c.strip() for c in ln.split(",")]
        if len(cols) != 3 or not cols[1] or not cols[2]:
            raise ValueError(f"{path}: malformed edge row {ln!r}")
        edges.add((cols[1], cols[2]))
    return edges


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    """Fixture writer in the upstream shape (used by the round-trip control and fixtures)."""
    path.write_text(",0,1\n" + "".join(f"{i},{s},{t}\n" for i, (s, t) in enumerate(edges)))


def jaccard(a: set, b: set) -> float:
    union = a | b
    if not union:
        return 1.0  # two empty graphs agree (flagged separately via edge counts)
    return len(a & b) / len(union)


def consensus_j(edge_sets: list[set]) -> float:
    pairs = [(i, j) for i in range(len(edge_sets)) for j in range(i + 1, len(edge_sets))]
    assert pairs, "consensus needs >= 2 replicas"
    return mean([jaccard(edge_sets[i], edge_sets[j]) for i, j in pairs])


def sig_purity(fb: dict) -> float:
    """m5' §2 definition, replica-local: sig-TP / max(total-TP, 1)."""
    s = float(fb["pooled_biological_sigificant_evaluation"]["true_positives"])
    p = float(fb["pooled_biological_evaluation"]["true_positives"])
    return s / max(p, 1.0)


def read_feedback(fb_path: Path) -> dict:
    text = fb_path.read_text()
    for s in FORBIDDEN_SUBSTRINGS:  # executed leakage assert on every feedback read
        assert s not in text, f"redaction failed at {fb_path}: '{s}' present"
    _sha(fb_path)
    return json.loads(text)


# ------------------------------------------------------------------ loaders
def find_chain(chains_root: Path, arm_short: str, ds: str, rep: int) -> Path | None:
    hits = sorted(chains_root.glob(f"*_{arm_short}_{ds}_{rep}"))
    assert len(hits) <= 1, f"chain key not unique: {arm_short} {ds} {rep} -> {hits}"
    return hits[0] if hits else None


def served_models(chain_dir: Path) -> list[str]:
    """Every model id the runner logged for this chain's decision calls."""
    ids: list[str] = []
    for dec in sorted(chain_dir.glob("*/decision.json")):
        _sha(dec)
        for call in json.loads(dec.read_text()).get("call_log", []):
            if "model_id" in call:
                ids.append(str(call["model_id"]))
    return ids


def served_model_violation(chain_dir: Path) -> str | None:
    """Custody re-check of the served-model pin (design §2.2). A chain whose logged
    call ids are not all SERVED_MODEL is CANNOT_CHECK — the runner asserts the same
    thing live; this catches artifacts produced by any other path."""
    ids = served_models(chain_dir)
    if not ids:
        return (f"no served-model record in {chain_dir.name} decision logs "
                f"(cannot prove the chain ran on {SERVED_MODEL!r})")
    bad = sorted({m for m in ids if m != SERVED_MODEL})
    return f"served model(s) {bad} != frozen {SERVED_MODEL!r}" if bad else None


def load_f0_bests(root: Path, *, required: bool, check_served: bool) -> dict[str, dict]:
    """F0 federation bests per cell. required=True for the in-campaign (primary)
    arm; the historical m2 panel is optional and never gates."""
    out: dict[str, dict] = {}
    for ds in DATASETS:
        for rep in range(REPS):
            key = f"{ds}:{rep}"
            d = find_chain(root / "run/chains", "f0", ds, rep)
            if d is None or not (d / "CHAIN_COMPLETE.json").exists():
                status = ("CANNOT_CHECK" if (d is not None and (d / "CANNOT_CHECK.json").exists())
                          else ("MISSING" if d is None else "IN_PROGRESS"))
                out[key] = {"best": None, "runs": [],
                            "status": status if required else "ABSENT"}
                continue
            if check_served:
                viol = served_model_violation(d)
                if viol:
                    out[key] = {"best": None, "runs": [], "status": "CANNOT_CHECK", "error": viol}
                    continue
            _sha(d / "CHAIN_COMPLETE.json")
            runs = []
            for name in F0_MEMBERS:
                exp_id = (d / name / "exp_id").read_text().strip()
                _sha(d / name / "exp_id")
                mp = root / "run/results" / exp_id / "metrics.json"
                _sha(mp)
                runs.append({"run": name, "exp_id": int(exp_id), **primary_score(mp)})
            out[key] = {"best": best_by_primary(runs), "runs": runs, "status": "COMPLETE"}
    return out


def load_replica(chain_dir: Path | None, replica: str) -> dict:
    if chain_dir is None:
        return {"replica": replica, "status": "MISSING"}
    if (chain_dir / "CANNOT_CHECK.json").exists() and not (chain_dir / "CHAIN_COMPLETE.json").exists():
        _sha(chain_dir / "CANNOT_CHECK.json")
        return {"replica": replica, "status": "CANNOT_CHECK",
                "error": json.loads((chain_dir / "CANNOT_CHECK.json").read_text()).get("error")}
    if not (chain_dir / "CHAIN_COMPLETE.json").exists():
        return {"replica": replica, "status": "IN_PROGRESS"}
    _sha(chain_dir / "CHAIN_COMPLETE.json")
    viol = served_model_violation(chain_dir)
    if viol:
        return {"replica": replica, "status": "CANNOT_CHECK", "error": viol}
    # custody: the cycle-1 config must carry exactly the replica's mandated seeds
    c1 = chain_dir / "cycle1" / "config_1.json"
    _sha(c1)
    cfg1 = json.loads(c1.read_text())
    ms, ps = SEED_TABLE[replica]
    if cfg1.get("model_seed") != ms or cfg1.get("partial_intervention_seed") != ps:
        return {"replica": replica, "status": "CANNOT_CHECK",
                "error": f"cycle-1 config seeds {cfg1.get('model_seed')}/{cfg1.get('partial_intervention_seed')}"
                         f" != mandated {ms}/{ps}"}
    cycles = []
    for c in CYCLES:
        cd = chain_dir / f"cycle{c}"
        fb = read_feedback(cd / "redacted_feedback.json")
        exp_id = (cd / "exp_id").read_text().strip()
        _sha(cd / "exp_id")
        rd = S2C_ROOT / "run/results" / exp_id
        for name in ("arguments.json", "metrics.json", "output_network.csv"):
            _sha(rd / name)
        score = primary_score(rd / "metrics.json")
        edges = parse_edges(rd / "output_network.csv")
        cycles.append({"cycle": c, "exp_id": int(exp_id), "primary": score["primary"],
                       "true_positives": score["true_positives"], "sig_purity": sig_purity(fb),
                       "n_edges": len(edges), "edges": edges})
    return {"replica": replica, "status": "COMPLETE", "cycles": cycles}


def load_cells() -> list[dict]:
    cells = []
    for ds in DATASETS:
        for rep in range(REPS):
            reps = [load_replica(find_chain(S2C_ROOT / "run/chains", r, ds, rep), r) for r in REPLICAS]
            cells.append({"key": f"{ds}:{rep}", "dataset": ds, "rep": rep, "replicas": reps})
    return cells


def campaign_status(cells: list[dict], f0_primary: dict[str, dict]) -> dict:
    census: dict[str, int] = {}
    unsettled, cannot = [], []
    for cell in cells:
        for r in cell["replicas"]:
            census[r["status"]] = census.get(r["status"], 0) + 1
            if r["status"] in ("MISSING", "IN_PROGRESS"):
                unsettled.append(f"{cell['key']}:{r['replica']}")
            elif r["status"] == "CANNOT_CHECK":
                cannot.append({"chain": f"{cell['key']}:{r['replica']}", "error": r.get("error")})
    for key, entry in f0_primary.items():
        st = entry.get("status", "MISSING")
        census[st] = census.get(st, 0) + 1
        if st in ("MISSING", "IN_PROGRESS"):
            unsettled.append(f"{key}:f0")
        elif st == "CANNOT_CHECK":
            cannot.append({"chain": f"{key}:f0", "error": entry.get("error")})
    return {"chains_by_status": census, "unsettled": unsettled, "cannot_check": cannot,
            "settled": not unsettled}


# ---------------------------------------------------------------- per-cell
def cell_statistics(cell: dict, f0_best: dict | None) -> dict:
    reps = [r for r in cell["replicas"] if r["status"] == "COMPLETE"]
    out = {"key": cell["key"], "dataset": cell["dataset"], "rep": cell["rep"],
           "replicas_used": [r["replica"] for r in reps],
           "replicas_excluded": [r["replica"] for r in cell["replicas"] if r["status"] != "COMPLETE"]}
    if len(reps) < MIN_REPLICAS_PER_CELL:
        out["status"] = "CANNOT_CHECK__TOO_FEW_REPLICAS"
        return out
    if f0_best is None:
        out["status"] = "CANNOT_CHECK__NO_F0_REFERENCE"
        return out
    # §3 probe statistic and truth anchor
    J = [consensus_j([r["cycles"][i]["edges"] for r in reps]) for i in range(len(CYCLES))]
    T = []
    for i in range(len(CYCLES)):
        w = [r["cycles"][i]["primary"] for r in reps if not _is_nan(r["cycles"][i]["primary"])]
        T.append(mean(w) if w else float("nan"))
    out["J"] = J
    out["T"] = T
    out["n_edges"] = {r["replica"]: [c["n_edges"] for c in r["cycles"]] for r in reps}
    finite = [(j, t) for j, t in zip(J, T) if math.isfinite(t)]
    out["rho_J_T"] = spearman([p[0] for p in finite], [p[1] for p in finite]) if len(finite) >= 3 else None
    # §4 shipping counterfactuals
    idx_cons = J.index(max(J))  # cell-level, earliest tie
    shipped: dict[str, list[float]] = {k: [] for k in RULES}
    ship_cycle: dict[str, list[int]] = {k: [] for k in RULES}
    for r in reps:
        w = [c["primary"] for c in r["cycles"]]
        pur = [c["sig_purity"] for c in r["cycles"]]
        idx_pur = pur.index(max(pur))  # replica-local, earliest tie
        real = [i for i, x in enumerate(w) if not _is_nan(x)]
        idx_orc = min(real, key=lambda i: w[i]) if real else len(CYCLES) - 1
        for rule, idx in (("TERMINAL", len(CYCLES) - 1), ("CONSENSUS_ARGMAX", idx_cons),
                          ("PURITY_ARGMAX", idx_pur), ("ORACLE_BEST", idx_orc)):
            shipped[rule].append(w[idx])
            ship_cycle[rule].append(CYCLES[idx])
    out["ship_cycle"] = ship_cycle
    out["f0_best_primary"] = f0_best["primary"]
    out["shipped_truth"] = shipped
    out["d"] = {}
    out["d_per_replica"] = {}
    for rule in RULES:
        vals = shipped[rule]
        if any(_is_nan(v) for v in vals):
            out["status"] = "CANNOT_CHECK__NAN_PRIMARY"
            return out
        out["d"][rule] = f0_best["primary"] - mean(vals)
        out["d_per_replica"][rule] = [f0_best["primary"] - v for v in vals]
    out["status"] = "COMPLETE"
    return out


# ------------------------------------------------------------------ pooled
def contrast(diffs: list[float]) -> dict:
    return {"n": len(diffs), "mean_d": mean(diffs) if diffs else None,
            "perm_p": perm_paired_p(diffs) if diffs else None,
            "f0_wins": sum(1 for d in diffs if d < 0), "f2_wins": sum(1 for d in diffs if d > 0),
            "ties": sum(1 for d in diffs if d == 0)}


def pooled_rho(cells: list[dict], *, seed: int = RHO_SEED, draws: int = RHO_DRAWS) -> dict:
    usable = [c for c in cells if c.get("status") == "COMPLETE" and c.get("rho_J_T") is not None]
    if not usable:
        return {"status": "CANNOT_CHECK__NO_USABLE_CELLS", "cells_used": 0}
    series = []
    for c in usable:
        finite = [(j, t) for j, t in zip(c["J"], c["T"]) if math.isfinite(t)]
        series.append(([p[0] for p in finite], [p[1] for p in finite]))
    raw = mean([c["rho_J_T"] for c in usable])
    rng = random.Random(seed)
    hits = 0
    for _ in range(draws):
        perm = mean([spearman(rng.sample(jj, len(jj)), tt) for jj, tt in series])
        if abs(perm) >= abs(raw):
            hits += 1
    return {"status": "OK", "raw_pooled_rho": raw, "directed_pooled_rho": -raw,
            "perm_p_two_sided": hits / draws, "draws": draws, "seed": seed,
            "cells_used": len(usable), "cells_excluded": [c["key"] for c in cells if c not in usable],
            "per_cell_rho": {c["key"]: c["rho_J_T"] for c in usable}}


def evaluate_gates(ct: dict, rho: dict, strata: dict) -> dict:
    g0 = bool(ct["TERMINAL"]["n"] and ct["TERMINAL"]["mean_d"] < 0
              and ct["TERMINAL"]["f0_wins"] >= G0_MIN_F0_WINS)
    g1 = bool(rho.get("status") == "OK" and rho["directed_pooled_rho"] > 0
              and rho["perm_p_two_sided"] <= G1_P)
    g2 = bool(ct["CONSENSUS_ARGMAX"]["n"] and ct["CONSENSUS_ARGMAX"]["mean_d"] >= G2_D
              and ct["CONSENSUS_ARGMAX"]["perm_p"] <= G2_P)
    g3 = bool(ct["PURITY_ARGMAX"]["n"] and (ct["PURITY_ARGMAX"]["mean_d"] < G2_D
                                            or ct["PURITY_ARGMAX"]["perm_p"] > G2_P))
    g4 = bool(strata and all(s["CONSENSUS_ARGMAX_mean_d"] is not None and s["TERMINAL_mean_d"] is not None
                             and s["CONSENSUS_ARGMAX_mean_d"] > s["TERMINAL_mean_d"]
                             for s in strata.values()))
    if not g0:
        route = "G0 failed: CANNOT_CHECK disposition; diagnose campaign mechanics under a separate freeze"
        disposition = "CANNOT_CHECK"
    elif g1 and g2 and g3 and g4:
        route = ("authorize m6 prospective confirm campaign under its own freeze "
                 "(no revival claim from Stage-2c alone)")
        disposition = "M6_AUTHORIZED"
    else:
        route = ("E40 line TERMINAL: deficit attributable to the information available to the loop "
                 "by any channel tested; further revival needs a new mechanism class")
        disposition = "E40_TERMINAL"
    return {"G0_DRAG_PRESENT_UNDER_TERMINAL": g0, "G1_CONSENSUS_RANKS_TRUTH": g1,
            "G2_CONSENSUS_SHIPPING_CLOSES_DRAG": g2, "G3_ANTI_CONTROL_DISTINGUISHES": g3,
            "G4_SPLIT_CONSISTENT": g4, "disposition": disposition, "preregistered_route": route}


def historical_panel(cells: list[dict], f0_hist: dict[str, dict]) -> dict:
    """Same probe, contrasted against the frozen m2 F0 chains. Those chains were
    produced under an earlier, unrecoverable served model, so this panel is a
    CROSS-MODEL comparison: reported for continuity with m2/m3/m4/m5' and
    explicitly NON-GATING (design §2.2, §4.1)."""
    usable = {k: v for k, v in f0_hist.items() if v.get("best") is not None}
    stats = [cell_statistics(c, usable.get(c["key"], {}).get("best")) for c in cells]
    complete = [s for s in stats if s["status"] == "COMPLETE"]
    ct = {rule: contrast([s["d"][rule] for s in complete]) for rule in RULES}
    strata = {}
    for ds in DATASETS:
        sub = [s for s in complete if s["dataset"] == ds]
        strata[ds] = {"n": len(sub)}
        for rule in RULES:
            strata[ds][f"{rule}_mean_d"] = mean([s["d"][rule] for s in sub]) if sub else None
    return {"gating": False,
            "caveat": "cross-model contrast (m2 F0 served model unrecoverable); reported, never gated",
            "cells_complete": len(complete), "contrasts": ct, "strata": strata,
            "cells_absent": [k for k, v in f0_hist.items() if v.get("best") is None]}


def analyse(cells: list[dict], f0: dict[str, dict]) -> dict:
    stats = [cell_statistics(c, f0[c["key"]]["best"]) for c in cells]
    complete = [s for s in stats if s["status"] == "COMPLETE"]
    ct = {rule: contrast([s["d"][rule] for s in complete]) for rule in RULES}
    per_rep = {rule: [d for s in complete for d in s["d_per_replica"][rule]] for rule in RULES}
    secondary = {rule: {"n": len(per_rep[rule]), "mean_d": mean(per_rep[rule]) if per_rep[rule] else None,
                        "f0_wins": sum(1 for d in per_rep[rule] if d < 0),
                        "f2_wins": sum(1 for d in per_rep[rule] if d > 0),
                        "note": "per-replica diffs are within-cell correlated; descriptive only (no p)"}
                 for rule in RULES}
    strata = {}
    for ds in DATASETS:
        sub = [s for s in complete if s["dataset"] == ds]
        strata[ds] = {"n": len(sub)}
        for rule in RULES:
            strata[ds][f"{rule}_mean_d"] = mean([s["d"][rule] for s in sub]) if sub else None
    rho = pooled_rho(stats)
    gates = evaluate_gates(ct, rho, strata)
    census = {rule: {str(c): sum(1 for s in complete for x in s["ship_cycle"][rule] if x == c)
                     for c in CYCLES} for rule in RULES}
    return {"cells": [{k: v for k, v in s.items()} for s in stats],
            "cells_complete": len(complete),
            "cells_cannot_check": [{"key": s["key"], "status": s["status"]} for s in stats
                                   if s["status"] != "COMPLETE"],
            "contrasts_primary_12cell": ct, "contrasts_secondary_per_replica": secondary,
            "strata": strata, "rho": rho, "ship_cycle_census": census, "gates": gates}


def controls_from_runner() -> dict:
    out = {}
    for name, rel in (("planted", "run/controls/planted/planted.json"), ("nullcal", "run/controls/nullcal.json")):
        p = S2C_ROOT / rel
        if p.exists():
            _sha(p)
            out[name] = json.loads(p.read_text())
        else:
            out[name] = None
    return out


# ------------------------------------------------------------------ controls
def control_nullcal_perm(*, reps: int = NULLCAL_REPS, seed: int = NULLCAL_SEED) -> dict:
    """m2/m3 form: the exhaustive sign-flip null rejects at ~alpha under H0 (band [0.02, 0.09])."""
    rng = random.Random(seed)
    rejections = sum(1 for _ in range(reps)
                     if perm_paired_p([rng.gauss(0, 1) for _ in range(12)]) < 0.05)
    rate = rejections / reps
    return {"control": "permutation_null_calibration", "reps": reps, "seed": seed, "n_pairs": 12,
            "alpha": 0.05, "rejection_rate": rate, "accept_band": [0.02, 0.09],
            "verdict": "PASS" if 0.02 <= rate <= 0.09 else "FAIL"}


def control_nullcal_gate_chain(*, reps: int = NULLCAL_REPS, seed: int = NULLCAL_SEED,
                               draws: int = 400) -> dict:
    """Random-config pass rate of the decision chain G1^G2^G3^G4 under a null campaign
    (J and T independent per cell; every contrast diff ~ N(0, 0.005)) must be < 1%.
    The rho permutation uses a reduced draw count here (documented) — calibration only."""
    rng = random.Random(seed)
    passes = 0
    for _ in range(reps):
        stats = []
        for ds in DATASETS:
            for rep in range(REPS):
                J = [rng.random() for _ in CYCLES]
                T = [rng.random() for _ in CYCLES]
                stats.append({"key": f"{ds}:{rep}", "dataset": ds, "status": "COMPLETE", "J": J, "T": T,
                              "rho_J_T": spearman(J, T),
                              "d": {rule: rng.gauss(0, 0.005) for rule in RULES}})
        ct = {rule: contrast([s["d"][rule] for s in stats]) for rule in RULES}
        strata = {ds: {f"{rule}_mean_d": mean([s["d"][rule] for s in stats if s["dataset"] == ds])
                       for rule in RULES} for ds in DATASETS}
        rho = pooled_rho(stats, seed=rng.randrange(2 ** 31), draws=draws)
        g = evaluate_gates(ct, rho, strata)
        if g["G1_CONSENSUS_RANKS_TRUTH"] and g["G2_CONSENSUS_SHIPPING_CLOSES_DRAG"] \
                and g["G3_ANTI_CONTROL_DISTINGUISHES"] and g["G4_SPLIT_CONSISTENT"]:
            passes += 1
    rate = passes / reps
    return {"control": "null_gate_chain_pass_rate", "reps": reps, "seed": seed, "rho_draws": draws,
            "pass_rate": rate, "threshold": 0.01, "verdict": "PASS" if rate < 0.01 else "FAIL"}


def control_jaccard_selftest(*, seed: int = 20260902) -> dict:
    rng = random.Random(seed)
    genes = [f"ENSG{i:011d}" for i in range(400)]
    E = set()
    while len(E) < 417:
        s, t = rng.sample(genes, 2)
        E.add((s, t))
    src = [e[0] for e in E]
    dst = [e[1] for e in E]
    rng.shuffle(dst)  # rewired: same endpoints, shuffled pairing
    E_shuf = set(zip(src, dst))
    checks = {"J_E_E": jaccard(E, E), "J_E_shuffled": jaccard(E, E_shuf),
              "J_E_empty": jaccard(E, set()), "J_empty_empty": jaccard(set(), set()),
              "J_half": jaccard(set(list(E)[:200]), set(list(E)[100:300]))}
    ok = (checks["J_E_E"] == 1.0 and checks["J_E_shuffled"] < 0.05 and checks["J_E_empty"] == 0.0
          and abs(checks["J_half"] - 100 / 300) < 1e-12
          and abs(consensus_j([E, E, E_shuf]) - (1.0 + 2 * checks["J_E_shuffled"]) / 3) < 1e-12)
    return {"control": "jaccard_selftest", **checks, "verdict": "PASS" if ok else "FAIL"}


def control_edge_roundtrip(tmp: Path, *, seed: int = 20260902) -> dict:
    rng = random.Random(seed)
    genes = [f"ENSG{i:011d}" for i in range(300)]
    edges = []
    seen = set()
    while len(edges) < 417:
        s, t = rng.sample(genes, 2)
        if (s, t) not in seen:
            seen.add((s, t))
            edges.append((s, t))
    p = tmp / "output_network.csv"
    write_edges(p, edges)
    parsed = parse_edges(p)
    p2 = tmp / "roundtrip.csv"
    write_edges(p2, sorted(parsed))
    again = parse_edges(p2)
    header_ok = p.read_text().splitlines()[0] == ",0,1"
    # a real upstream fixture line shape (from campaign-e40-m3 results 501000)
    p3 = tmp / "upstream_shape.csv"
    p3.write_text(",0,1\n0,ENSG00000174748,ENSG00000125691\n1,ENSG00000254772,ENSG00000177600\n")
    up = parse_edges(p3)
    bad_ok = False
    p4 = tmp / "bad.csv"
    p4.write_text("src,dst\na,b\n")
    try:
        parse_edges(p4)
    except ValueError:
        bad_ok = True
    ok = (parsed == seen and again == seen and len(parsed) == 417 and header_ok
          and up == {("ENSG00000174748", "ENSG00000125691"), ("ENSG00000254772", "ENSG00000177600")}
          and bad_ok)
    return {"control": "edge_parse_roundtrip", "n_edges": len(parsed), "header_ok": header_ok,
            "upstream_shape_ok": up is not None, "rejects_foreign_header": bad_ok,
            "verdict": "PASS" if ok else "FAIL"}


# ------------------------------------------------------------------ fixtures
def write_fixture(m2_root: Path, s2c_root: Path, *, mode: str, seed: int = 7,
                  drop: dict[str, str] | None = None, served: str | None = None) -> None:
    """Synthetic campaign tree: historical m2 F0 layout (12_f0..23_f0, run0-3) + the
    Stage-2c layout (48 replica chains x 4 cycles + 12 in-campaign F0 chains x 4 runs,
    exp_ids 504000+, results with arguments/metrics/output_network, decision logs
    carrying the served-model id).
    mode 'planted': consensus tracks truth, consensus shipping beats F0 slightly, terminal
    and purity anti-select. mode 'null': truth independent of consensus, F0 = cell oracle.
    drop: {chain_key: 'CANNOT_CHECK'|'MISSING'|'IN_PROGRESS'} to exercise exclusion paths."""
    rng = random.Random(seed)
    drop = drop or {}
    genes = [f"ENSG{i:011d}" for i in range(500)]

    def metrics(w: float, tp: int = 150) -> dict:
        return {"quantitative_test_evaluation": {"output_graph": {
                    "wasserstein_distance": {"mean": w}, "true_positives": tp, "false_positives": 200},
                    "false_omission_rate": 0.15},
                "corum_evaluation": {"true_positives": 80.0}, "string_network_evaluation": {"true_positives": 200.0},
                "string_physical_evaluation": {"true_positives": 100.0},
                "ligand_receptor_evaluation": {"true_positives": 0.0}, "chipseq_evaluation": {"true_positives": 2},
                "pooled_biological_evaluation": {"true_positives": 230.0},
                "pooled_biological_sigificant_evaluation": {"true_positives": 100},
                "run_time": 140.0}

    def redacted(m: dict, purity: float) -> dict:
        d = {k: v for k, v in m.items() if k != "quantitative_test_evaluation"}
        d["pooled_biological_sigificant_evaluation"] = {"true_positives": round(purity * 230.0, 3)}
        return d

    served = served or SERVED_MODEL

    def call_log(n: int = 1) -> list[dict]:
        return [{"attempt": i, "model_id": served, "input_tokens": 500, "output_tokens": 100}
                for i in range(n)]

    m2_chains, m2_results = m2_root / "run/chains", m2_root / "run/results"
    s_chains, s_results = s2c_root / "run/chains", s2c_root / "run/results"
    task = 0
    for di, ds in enumerate(DATASETS):
        for rep in range(REPS):
            cell = di * REPS + rep
            # consensus level per cycle: cycle 4 lowest (terminal anti-selects); best among 1-3 rotates
            s_levels = [0.9, 0.6, 0.75]
            rot = cell % 3
            s_levels = s_levels[rot:] + s_levels[:rot] + [0.3]
            base = 0.17 + 0.01 * rng.random()
            truth = [[0.0] * len(CYCLES) for _ in REPLICAS]
            for ci, s in enumerate(s_levels):
                for k in range(len(REPLICAS)):
                    if mode == "planted":
                        truth[k][ci] = base - 0.04 * s + 0.0005 * rng.random()
                    else:
                        truth[k][ci] = base + 0.02 * rng.random()
            cell_mean = [mean([truth[k][ci] for k in range(len(REPLICAS))]) for ci in range(len(CYCLES))]
            if mode == "planted":
                f0_best = cell_mean[s_levels.index(max(s_levels))] + 0.0005  # consensus ship beats F0 slightly
            else:
                f0_best = min(cell_mean) - 0.0002  # F0 just under the cell oracle: drag under every rule
            f0_dir = m2_chains / f"{12 + cell:02d}_f0_{ds}_{rep}"
            f0_dir.mkdir(parents=True, exist_ok=True)
            (f0_dir / "CHAIN_COMPLETE.json").write_text("{}")
            for i, name in enumerate(F0_MEMBERS):
                exp = 500048 + cell * 4 + i
                (f0_dir / name).mkdir(exist_ok=True)
                (f0_dir / name / "exp_id").write_text(str(exp))
                (m2_results / str(exp)).mkdir(parents=True, exist_ok=True)
                (m2_results / str(exp) / "metrics.json").write_text(
                    json.dumps(metrics(f0_best if i == 1 else f0_best + 0.01 * (i + 1))))
            for k, replica in enumerate(REPLICAS):
                key = f"{ds}:{rep}:{replica}"
                cdir = s_chains / f"{task:02d}_{replica}_{ds}_{rep}"
                ms, ps = SEED_TABLE[replica]
                if drop.get(key) == "MISSING":
                    task += 1
                    continue
                cdir.mkdir(parents=True, exist_ok=True)
                if drop.get(key) == "CANNOT_CHECK":
                    (cdir / "CANNOT_CHECK.json").write_text(json.dumps({"error": "fixture: mandate exhausted"}))
                    task += 1
                    continue
                for ci, c in enumerate(CYCLES):
                    cyd = cdir / f"cycle{c}"
                    cyd.mkdir(exist_ok=True)
                    exp = 503000 + task * 4 + ci
                    (cyd / "exp_id").write_text(str(exp))
                    cfg = {"model_name": "gies", "subset_data": 0.05, "max_path_length": -1, "do_filter": True,
                           "dataset_name": ds, "training_regime": "interventional",
                           "fraction_partial_intervention": 0.0, "omission_estimation_size": 1000,
                           "model_seed": ms if c == 1 else rng.randrange(100),
                           "partial_intervention_seed": ps if c == 1 else rng.randrange(100)}
                    (cyd / "config_1.json").write_text(json.dumps(cfg, sort_keys=True))
                    (cyd / "decision.json").write_text(json.dumps(
                        {"cycle": c, "replica": replica, "configs": [cfg], "call_log": call_log()}))
                    m = metrics(truth[k][ci])
                    purity = 0.3 + 0.1 * ci  # purity peaks at cycle 4 -> anti-selects with terminal
                    (cyd / "redacted_feedback.json").write_text(json.dumps(redacted(m, purity), sort_keys=True))
                    rd = s_results / str(exp)
                    rd.mkdir(parents=True, exist_ok=True)
                    (rd / "metrics.json").write_text(json.dumps(m))
                    (rd / "arguments.json").write_text(json.dumps({**cfg, "exp_id": str(exp)}))
                    # replica edge set: shared core (size 417*s) + private edges to 417
                    s = s_levels[ci]
                    rng_e = random.Random(seed * 1000 + cell * 10 + ci)  # same core across replicas
                    core = set()
                    while len(core) < int(417 * s):
                        core.add(tuple(rng_e.sample(genes, 2)))
                    edges = set(core)
                    while len(edges) < 417:
                        edges.add(tuple(rng.sample(genes, 2)))
                    write_edges(rd / "output_network.csv", sorted(edges))
                if drop.get(key) == "IN_PROGRESS":
                    task += 1
                    continue
                (cdir / "CHAIN_COMPLETE.json").write_text(json.dumps({"task": task}))
                task += 1
            # in-campaign F0 federation chain for this cell (Stage-2c primary reference)
            fkey = f"{ds}:{rep}:f0"
            fdir = s_chains / f"{48 + cell:02d}_f0_{ds}_{rep}"
            if drop.get(fkey) == "MISSING":
                continue
            fdir.mkdir(parents=True, exist_ok=True)
            if drop.get(fkey) == "CANNOT_CHECK":
                (fdir / "CANNOT_CHECK.json").write_text(json.dumps({"error": "fixture: F0 chain failed"}))
                continue
            (fdir / "upfront").mkdir(exist_ok=True)
            (fdir / "upfront" / "decision.json").write_text(json.dumps(
                {"cycle": 0, "replica": "f0", "configs": [], "call_log": call_log()}))
            for i, name in enumerate(F0_MEMBERS):
                exp = 504192 + cell * 4 + i
                (fdir / name).mkdir(exist_ok=True)
                (fdir / name / "exp_id").write_text(str(exp))
                rd = s_results / str(exp)
                rd.mkdir(parents=True, exist_ok=True)
                (rd / "metrics.json").write_text(json.dumps(
                    metrics(f0_best if i == 1 else f0_best + 0.01 * (i + 1))))
            if drop.get(fkey) == "IN_PROGRESS":
                continue
            (fdir / "CHAIN_COMPLETE.json").write_text(json.dumps({"cell": cell, "arm": "f0"}))


# --------------------------------------------------------------------- main
def run(*, write: bool = True) -> tuple[int, dict]:
    _MANIFEST.clear()
    cells = load_cells()
    f0_primary = load_f0_bests(S2C_ROOT, required=True, check_served=True)
    st = campaign_status(cells, f0_primary)
    if not st["settled"]:
        doc = {"schema_version": "orion.v2.e40-matched.m5p-stage2c-rollup.v1",
               "variant": "e40-m5p-stage2c-seed-replica-stability-probe",
               "status": "REFUSED__CAMPAIGN_NOT_SETTLED", "campaign": st}
        if write:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            (OUT_DIR / "E40_M5P_STAGE2C_STATUS.json").write_text(json.dumps(doc, indent=1, sort_keys=True))
        print(json.dumps({"status": doc["status"], "chains_by_status": st["chains_by_status"],
                          "unsettled_n": len(st["unsettled"])}, indent=1))
        return 3, doc
    an = analyse(cells, f0_primary)
    f0_hist = load_f0_bests(M2_ROOT, required=False, check_served=False)
    hist = historical_panel(cells, f0_hist)
    for c in an["cells"]:  # edge sets are not serializable / not needed in the rollup
        c.pop("edges", None)
    rollup = {"schema_version": "orion.v2.e40-matched.m5p-stage2c-rollup.v1",
              "variant": "e40-m5p-stage2c-seed-replica-stability-probe",
              "design": "E40_M5P_STAGE2C_SEED_REPLICA_PROBE_DESIGN_V1",
              "status": "OK",
              "f0_arm": "in-campaign (Stage-2c), same served model as F2",
              "served_model_pinned": SERVED_MODEL,
              "historical_reference_root": str(M2_ROOT), "campaign_root": str(S2C_ROOT),
              "campaign": st,
              "primary": "mean wasserstein_distance.mean of quantitative_test_evaluation.output_graph (lower better)",
              "contrast_convention": "d = f0_best_primary - mean_k shipped_truth_k; negative = F0 better; "
                                     "perm_p = one-sided exhaustive sign-flip P(T_perm >= T_obs) (m-series)",
              "rho_convention": "pooled arithmetic mean of per-cell Spearman(J_c, T_c); directed = -raw; "
                                "within-cell cycle shuffle two-sided, 10000 draws, seed 20260902",
              "analysis": an,
              "historical_m2_f0_panel_nongating": hist,
              "controls_runner": controls_from_runner(),
              "manifest": {"n_files": len(_MANIFEST), "files": _MANIFEST}}
    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "E40_M5P_STAGE2C_ROLLUP_V1.json").write_text(json.dumps(rollup, indent=1, sort_keys=True))
        g = an["gates"]
        lines = ["# E40-m5' Stage-2c seed-replica stability-probe rollup V1", "",
                 f"disposition: {g['disposition']}", f"route: {g['preregistered_route']}", "",
                 f"cells complete: {an['cells_complete']}/12; cannot_check: {an['cells_cannot_check']}",
                 f"chains: {st['chains_by_status']}; CANNOT_CHECK chains: {st['cannot_check']}", "",
                 "## contrasts (12-cell primary)", "| rule | n | mean_d | perm_p | f0 wins | f2 wins |",
                 "|---|---|---|---|---|---|"]
        for rule in RULES:
            c = an["contrasts_primary_12cell"][rule]
            md = "n/a" if c["mean_d"] is None else f"{c['mean_d']:+.6f}"
            pp = "n/a" if c["perm_p"] is None else f"{c['perm_p']:.6f}"
            lines.append(f"| {rule} | {c['n']} | {md} | {pp} | {c['f0_wins']} | {c['f2_wins']} |")
        r = an["rho"]
        lines += ["", "## consensus-truth rho",
                  json.dumps({k: v for k, v in r.items() if k != "per_cell_rho"}, indent=1, sort_keys=True),
                  "", "## strata", json.dumps(an["strata"], indent=1, sort_keys=True),
                  "", "## historical m2-F0 panel (cross-model, NON-GATING)",
                  json.dumps({"cells_complete": hist["cells_complete"],
                              "contrasts": {k: {kk: v[kk] for kk in ("n", "mean_d", "perm_p", "f0_wins")}
                                            for k, v in hist["contrasts"].items()}},
                             indent=1, sort_keys=True),
                  "", "## gates", json.dumps(g, indent=1, sort_keys=True)]
        (OUT_DIR / "E40_M5P_STAGE2C_ROLLUP_V1.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"status": "OK", "gates": an["gates"],
                      "contrasts": {k: {kk: v[kk] for kk in ("n", "mean_d", "perm_p", "f0_wins")}
                                    for k, v in an["contrasts_primary_12cell"].items()},
                      "rho": {k: an["rho"].get(k) for k in ("raw_pooled_rho", "directed_pooled_rho",
                                                            "perm_p_two_sided", "cells_used")}}, indent=1))
    return 0, rollup


def _with_roots(m2: Path, s2c: Path, out: Path):
    """Rebind module roots (fixture runs go through the same main() code path)."""
    g = globals()
    saved = (g["M2_ROOT"], g["S2C_ROOT"], g["OUT_DIR"])
    g["M2_ROOT"], g["S2C_ROOT"], g["OUT_DIR"] = m2, s2c, out
    return saved


def _restore_roots(saved) -> None:
    g = globals()
    g["M2_ROOT"], g["S2C_ROOT"], g["OUT_DIR"] = saved


def selftest(*, fast: bool = False) -> int:
    import tempfile
    failures: list[str] = []
    records: dict = {}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        records["jaccard"] = control_jaccard_selftest()
        records["edge_roundtrip"] = control_edge_roundtrip(tmp)
        reps = 40 if fast else NULLCAL_REPS
        records["nullcal_perm"] = control_nullcal_perm(reps=reps)
        records["nullcal_gate_chain"] = control_nullcal_gate_chain(reps=reps, draws=100 if fast else 400)
        for k, v in records.items():
            if v["verdict"] != "PASS":
                failures.append(f"{k} control FAIL: {v}")
        # planted end-to-end through main(): every gate must PASS, route = m6
        for mode, expect in (("planted", True), ("null", False)):
            root = tmp / mode
            write_fixture(root / "m2", root / "s2c", mode=mode)
            saved = _with_roots(root / "m2", root / "s2c", root / "out")
            try:
                rc, doc = run()
            finally:
                _restore_roots(saved)
            g = doc.get("analysis", {}).get("gates", {})
            records[f"fixture_{mode}"] = {"rc": rc, "gates": g,
                                          "rho": {k: doc["analysis"]["rho"].get(k) for k in
                                                  ("directed_pooled_rho", "perm_p_two_sided")} if rc == 0 else None}
            if rc != 0:
                failures.append(f"{mode} fixture: main() rc={rc}")
                continue
            if not (root / "out/E40_M5P_STAGE2C_ROLLUP_V1.json").exists():
                failures.append(f"{mode} fixture: rollup json not written")
            if g.get("G0_DRAG_PRESENT_UNDER_TERMINAL") is not True:
                failures.append(f"{mode} fixture: G0 must pass (terminal drag planted): {g}")
            if g.get("G1_CONSENSUS_RANKS_TRUTH") is not expect:
                failures.append(f"{mode} fixture: G1 expected {expect}: {g}")
            if mode == "planted" and not all(g.get(k) for k in ("G2_CONSENSUS_SHIPPING_CLOSES_DRAG",
                                                                "G3_ANTI_CONTROL_DISTINGUISHES",
                                                                "G4_SPLIT_CONSISTENT")):
                failures.append(f"planted fixture: G2-G4 must pass: {g}")
            if mode == "planted" and g.get("disposition") != "M6_AUTHORIZED":
                failures.append(f"planted fixture: route must be m6: {g}")
            if mode == "null" and g.get("disposition") != "E40_TERMINAL":
                failures.append(f"null fixture: route must be TERMINAL: {g}")
            if doc["manifest"]["n_files"] < 12 * 4 * (3 * 4 + 4 + 2) + 12 * 8 + 12 * 4:
                failures.append(f"{mode} fixture: manifest too small ({doc['manifest']['n_files']})")
        # refusal: one MISSING chain -> exit 3, nothing analysed; one IN_PROGRESS -> exit 3
        for kind in ("MISSING", "IN_PROGRESS"):
            root = tmp / f"refuse_{kind}"
            write_fixture(root / "m2", root / "s2c", mode="planted",
                          drop={"weissmann_rpe1:2:f2r1": kind})
            saved = _with_roots(root / "m2", root / "s2c", root / "out")
            try:
                rc, doc = run()
            finally:
                _restore_roots(saved)
            if rc != 3 or "analysis" in doc or (root / "out/E40_M5P_STAGE2C_ROLLUP_V1.json").exists():
                failures.append(f"{kind} chain must make main() refuse with rc=3: rc={rc}")
        # exclusion: CANNOT_CHECK chains are counted, the cell is evaluated on the remaining replicas;
        # a cell with <2 replicas is CANNOT_CHECK itself and the contrasts shrink to 11 cells
        root = tmp / "cannot"
        write_fixture(root / "m2", root / "s2c", mode="planted",
                      drop={"weissmann_k562:1:f2r2": "CANNOT_CHECK", "weissmann_rpe1:4:f2r0": "CANNOT_CHECK",
                            "weissmann_rpe1:4:f2r1": "CANNOT_CHECK", "weissmann_rpe1:4:f2r3": "CANNOT_CHECK"})
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            rc, doc = run()
        finally:
            _restore_roots(saved)
        an = doc.get("analysis", {})
        cc = {c["key"]: c for c in an.get("cells", [])}
        if rc != 0 or len(doc["campaign"]["cannot_check"]) != 4:
            failures.append(f"CANNOT_CHECK chains must be counted (4) and analysis still run: rc={rc}")
        if cc.get("weissmann_k562:1", {}).get("replicas_used") != ["f2r0", "f2r1", "f2r3"]:
            failures.append(f"cell with one CANNOT_CHECK replica must use the other three: {cc.get('weissmann_k562:1')}")
        if cc.get("weissmann_rpe1:4", {}).get("status") != "CANNOT_CHECK__TOO_FEW_REPLICAS" \
                or an.get("cells_complete") != 11 or an["contrasts_primary_12cell"]["TERMINAL"]["n"] != 11:
            failures.append("cell with <2 replicas must be CANNOT_CHECK and drop out of the contrasts")
        # leakage assert on read is executed
        root = tmp / "leak"
        write_fixture(root / "m2", root / "s2c", mode="planted")
        fbp = next((root / "s2c/run/chains").glob("05_*/cycle3/redacted_feedback.json"))
        fbp.write_text(fbp.read_text()[:-1] + ', "x": {"wasserstein": 1}}')
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            run(write=False)
            failures.append("leaked feedback must abort the analysis (assert on read)")
        except AssertionError as exc:
            if "redaction failed" not in str(exc):
                failures.append(f"wrong assert fired on leaked feedback: {exc}")
        finally:
            _restore_roots(saved)
        # seed-mandate custody: a COMPLETE chain whose cycle-1 config drifts off its seeds is CANNOT_CHECK
        root = tmp / "seeds"
        write_fixture(root / "m2", root / "s2c", mode="planted")
        c1 = next((root / "s2c/run/chains").glob("07_f2r3_*/cycle1/config_1.json"))
        cfg = json.loads(c1.read_text())
        cfg["model_seed"] = 0
        c1.write_text(json.dumps(cfg, sort_keys=True))
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            rc, doc = run(write=False)
        finally:
            _restore_roots(saved)
        if rc != 0 or len(doc["campaign"]["cannot_check"]) != 1 \
                or "mandated 71/79" not in doc["campaign"]["cannot_check"][0]["error"]:
            failures.append(f"seed-mandate drift must surface as CANNOT_CHECK: {doc.get('campaign')}")
        # Stage-2c: an unsettled IN-CAMPAIGN F0 chain also refuses (rc=3)
        for kind in ("MISSING", "IN_PROGRESS"):
            root = tmp / f"refuse_f0_{kind}"
            write_fixture(root / "m2", root / "s2c", mode="planted",
                          drop={"weissmann_k562:3:f0": kind})
            saved = _with_roots(root / "m2", root / "s2c", root / "out")
            try:
                rc, doc = run(write=False)
            finally:
                _restore_roots(saved)
            if rc != 3 or "analysis" in doc:
                failures.append(f"unsettled in-campaign F0 chain ({kind}) must refuse: rc={rc}")
        # Stage-2c: a CANNOT_CHECK in-campaign F0 chain removes exactly that cell
        root = tmp / "f0_cannot"
        write_fixture(root / "m2", root / "s2c", mode="planted", drop={"weissmann_rpe1:5:f0": "CANNOT_CHECK"})
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            rc, doc = run(write=False)
        finally:
            _restore_roots(saved)
        an = doc.get("analysis", {})
        cc = {c["key"]: c["status"] for c in an.get("cells", [])}
        if rc != 0 or cc.get("weissmann_rpe1:5") != "CANNOT_CHECK__NO_F0_REFERENCE" \
                or an["contrasts_primary_12cell"]["TERMINAL"]["n"] != 11:
            failures.append(f"CANNOT_CHECK in-campaign F0 must drop its cell only: {cc.get('weissmann_rpe1:5')}")
        records["fixture_f0_cannot_check"] = {"rc": rc, "cells_complete": an.get("cells_complete")}
        # Stage-2c: served-model substitution in the artifacts fails closed everywhere
        root = tmp / "served"
        write_fixture(root / "m2", root / "s2c", mode="planted", served="glm-5.2")
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            rc, doc = run(write=False)
        finally:
            _restore_roots(saved)
        an = doc.get("analysis", {})
        gates = an.get("gates", {})
        errs = [c["error"] for c in doc["campaign"]["cannot_check"]]
        if rc != 0 or len(errs) != 60 or not all("glm-5.2" in str(e) for e in errs) \
                or an.get("cells_complete") != 0 or gates.get("disposition") != "CANNOT_CHECK":
            failures.append(f"substituted served model must make every chain CANNOT_CHECK: "
                            f"n={len(errs)} cells={an.get('cells_complete')} {gates.get('disposition')}")
        records["fixture_served_substitution"] = {"rc": rc, "cannot_check_chains": len(errs),
                                                  "disposition": gates.get("disposition")}
        # Stage-2c: a COMPLETE chain with no served-model record at all is CANNOT_CHECK
        root = tmp / "nolog"
        write_fixture(root / "m2", root / "s2c", mode="planted")
        dec = next((root / "s2c/run/chains").glob("03_f2r3_*/cycle2/decision.json"))
        d = json.loads(dec.read_text()); d.pop("call_log"); dec.write_text(json.dumps(d))
        for other in sorted((root / "s2c/run/chains").glob("03_f2r3_*/cycle*/decision.json")):
            dd = json.loads(other.read_text())
            if "call_log" in dd:
                dd.pop("call_log"); other.write_text(json.dumps(dd))
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            rc, doc = run(write=False)
        finally:
            _restore_roots(saved)
        errs = [c for c in doc["campaign"]["cannot_check"] if "no served-model record" in str(c["error"])]
        if rc != 0 or len(errs) != 1:
            failures.append(f"chain without any served-model record must be CANNOT_CHECK: {errs}")
        # Stage-2c: the historical m2-F0 panel is present, populated and explicitly non-gating
        root = tmp / "hist"
        write_fixture(root / "m2", root / "s2c", mode="planted")
        saved = _with_roots(root / "m2", root / "s2c", root / "out")
        try:
            rc, doc = run(write=False)
        finally:
            _restore_roots(saved)
        hp = doc.get("historical_m2_f0_panel_nongating", {})
        if rc != 0 or hp.get("gating") is not False or hp.get("cells_complete") != 12 \
                or "gates" in hp or hp["contrasts"]["TERMINAL"]["n"] != 12:
            failures.append(f"historical m2-F0 panel must be present, 12 cells, non-gating: {hp!r}")
        records["historical_panel"] = {"cells_complete": hp.get("cells_complete"),
                                       "gating": hp.get("gating")}
    print(json.dumps({"selftest": "e40_m5p_stage2c_analysis", "fast": fast,
                      "controls": {k: v.get("verdict") for k, v in records.items() if "verdict" in v},
                      "fixtures": {k: v for k, v in records.items() if k.startswith("fixture")},
                      "failures": failures}, indent=1))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("run")
    p = sub.add_parser("selftest"); p.add_argument("--fast", action="store_true")
    args = ap.parse_args(argv)
    if args.cmd == "selftest":
        return selftest(fast=args.fast)
    rc, _ = run()
    return rc


if __name__ == "__main__":
    sys.exit(main())
