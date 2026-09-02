#!/usr/bin/env python3
"""H-EXT-2 internal-salience Goodhart replication screen (frozen with design V1).

Registered analysis of the H-EXT-2 fresh-cell campaign (two cohorts of F2 chains
on a native learner DIFFERENT from gies, produced by scripts/h_ext2_salience_runner.py):
for the pre-registered primary `sig_purity` (direction FIXED at -1: higher
purity => WORSE wasserstein, i.e. the m5' Stage-1 frozen-direction observation
is now the registered claim) and the 11 other m5' candidates (original
directions, carried as secondaries), measure whether the within-loop signal
ranks / anti-ranks the quantitative truth (raw wasserstein) across the loop's
own cycles. Two channel-EXTERNAL signals are added for G2 (mechanism
specificity): `replica_J` (edge-set Jaccard between each cycle's network and
its seed-replica; the loop never sees the replica) and `within_J` (mean Jaccard
of a cycle's network with the chain's other cycles; zero-cost fallback).

Mechanics are the m5' Stage-1 script verbatim (per-chain Spearman over cycles
with finite truth, arithmetic pooled rho, within-chain cycle-shuffle two-sided
permutation, 10,000 draws) under a NEW seed 20260903. Zero model calls, zero
native runs; read-only over inputs; writes
H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.{json,md}.

Design: research/experiments/h-ext2/H_EXT2_SALIENCE_GOODHART_REPLICATION_DESIGN_V1.{md,json}
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import random
import sys
from pathlib import Path

BASE = Path(os.environ.get("E40M_BASE", "/projects/hep/fs9/users/scyiu/orion-v2-e45"))
RPRIME_ROOT = Path(os.environ.get("HEXT2_RPRIME_ROOT", str(BASE / "campaign-h-ext2-rprime")))
PPRIME_ROOT = Path(os.environ.get("HEXT2_PPRIME_ROOT", str(BASE / "campaign-h-ext2-pprime")))
OUT_DIR = Path(os.environ.get("HEXT2_OUT", str(BASE / "campaign-h-ext2-rprime/run/rollup")))
MODEL = os.environ.get("HEXT2_MODEL", "DCDFG-LIN")  # registered fresh learner; pin-audited per run
PARENT_MODEL = "gies"  # the learner of the m2..m5' parent cell; a fresh cell must differ

DATASETS = ["weissmann_k562", "weissmann_rpe1"]
REPS = 6
CYCLES = [1, 2, 3, 4]
FORBIDDEN_SUBSTRINGS = ["quantitative_test_evaluation", "wasserstein",
                        "false_omission_rate", "negative_mean_wasserstein"]
TP_FIELDS = ["pooled_biological_evaluation", "corum_evaluation", "string_network_evaluation",
             "string_physical_evaluation", "chipseq_evaluation", "ligand_receptor_evaluation"]
SHUFFLE_SEED, DRAWS = 20260903, 10000  # NEW stream (design S3); m5' used 20260831
P_GATE = 0.05
NULLCAL_SEED, NULLCAL_REPS, NULLCAL_DRAWS = 20260904, 400, 1000
NULLCAL_BAND = (0.02, 0.09)
# G0 validity thresholds (frozen)
MIN_COMPLETE_CHAINS = 10        # of 12 per cohort
MIN_CHAINS_GE3_FINITE = 10      # chains with >=3 finite (score, truth) pairs, per cohort
MAX_NAN_CYCLE_FRACTION = 0.10   # NaN-primary cycles over all cycles, per cohort
MIN_CHAINS_PURITY_DISTINCT3 = 8  # chains whose sig_purity takes >=3 distinct values
MIN_CHAINS_J_NONCONSTANT = 8    # for G2: chains whose replica_J is not constant

PRIMARY = "sig_purity"
EXTERNAL_PRIMARY, EXTERNAL_FALLBACK = "replica_J", "within_J"
# m5' directions verbatim, EXCEPT sig_purity which is now registered NEGATIVE-for-truth.
DIRECTIONS = {"pooled_tp": 1, "pooled_sig_tp": 1, "corum_tp": 1, "string_net_tp": 1,
              "string_phys_tp": 1, "chipseq_tp": 1, "ligand_tp": 1, "fast_runtime": -1,
              "zmean_tp": 1, "rankmean_tp": 1, "sig_purity": -1, "efficiency": 1,
              "replica_J": 1, "within_J": 1}

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
    m = mean(xs)
    s = math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))
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
    og = d["quantitative_test_evaluation"]["output_graph"]
    return {"primary": float(og["wasserstein_distance"]["mean"]),
            "true_positives": int(og["true_positives"])}


def find_chain(chains_root: Path, arm_short: str, ds: str, rep: int) -> Path:
    hits = sorted(chains_root.glob(f"*_{arm_short}_{ds}_{rep}"))
    assert len(hits) == 1, f"chain key not unique: {arm_short} {ds} {rep} -> {hits}"
    return hits[0]


# ------------------------------------------------------------------ edge sets
def parse_edges(csv_path: Path) -> set[tuple[str, str]]:
    """Edge set of an upstream output_network.csv (pandas to_csv of a list of pairs:
    header ',0,1', rows 'idx,src,dst'). An empty network yields an empty set."""
    edges: set[tuple[str, str]] = set()
    with open(csv_path, newline="") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if i == 0 or len(row) < 3:
                continue
            edges.add((row[1], row[2]))
    return edges


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


# ------------------------------------------------------------------ candidates
def candidate_scores(fb: list[dict], edges: list[set], replica_edges: list[set | None]) -> dict[str, list[float]]:
    """Per-cycle scores: the 12 m5' candidates (verbatim) + the two external signals."""
    def col(field: str) -> list[float]:
        return [float(x[field]["true_positives"]) for x in fb]

    rt = [float(x["run_time"]) for x in fb]
    pooled = col("pooled_biological_evaluation")
    pooled_sig = col("pooled_biological_sigificant_evaluation")
    zcols = {f: _z(col(f)) for f in TP_FIELDS}
    n = len(fb)
    out = {
        "pooled_tp": pooled,
        "pooled_sig_tp": pooled_sig,
        "corum_tp": col("corum_evaluation"),
        "string_net_tp": col("string_network_evaluation"),
        "string_phys_tp": col("string_physical_evaluation"),
        "chipseq_tp": col("chipseq_evaluation"),
        "ligand_tp": col("ligand_receptor_evaluation"),
        "fast_runtime": rt,
        "zmean_tp": [mean([zcols[f][i] for f in TP_FIELDS]) for i in range(n)],
        "rankmean_tp": [mean([_ranks(col(f))[i] for f in TP_FIELDS]) for i in range(n)],
        "sig_purity": [s / max(p, 1.0) for s, p in zip(pooled_sig, pooled)],
        "efficiency": [a - b for a, b in zip(_z(pooled), _z(rt))],
        "replica_J": [jaccard(e, r) if r is not None else float("nan")
                      for e, r in zip(edges, replica_edges)],
        "within_J": [mean([jaccard(edges[i], edges[j]) for j in range(n) if j != i]) if n > 1 else float("nan")
                     for i in range(n)],
    }
    assert len(out) == 14 and set(out) == set(DIRECTIONS)
    return out


def build_cohort(tag: str, root: Path) -> dict:
    chains, incomplete, pin_violations = [], [], []
    for ds in DATASETS:
        for rep in range(REPS):
            hits = sorted((root / "run/chains").glob(f"*_f2_{ds}_{rep}"))
            key = f"{ds}:{rep}"
            if len(hits) != 1 or not (hits[0] / "CHAIN_COMPLETE.json").exists():
                status = "CANNOT_CHECK" if hits and (hits[0] / "CANNOT_CHECK.json").exists() else "MISSING"
                incomplete.append({"key": key, "status": status})
                continue
            f2_dir = hits[0]
            fb_dicts, truth, edges, rep_edges, exp_ids, rep_ids = [], [], [], [], [], []
            for c in CYCLES:
                cdir = f2_dir / f"cycle{c}"
                fb_path = cdir / "redacted_feedback.json"
                text = fb_path.read_text()
                for s in FORBIDDEN_SUBSTRINGS:  # C2 leakage re-check (executed, not logged)
                    assert s not in text, f"redaction failed at {fb_path}: '{s}' present"
                _sha(fb_path)
                fb_dicts.append(json.loads(text))
                exp_id = (cdir / "exp_id").read_text().strip()
                _sha(cdir / "exp_id")
                rdir = root / "run/results" / exp_id
                args = json.loads((rdir / "arguments.json").read_text())
                _sha(rdir / "arguments.json")
                if args.get("model_name") != MODEL:
                    pin_violations.append(f"{rdir}: model_name={args.get('model_name')!r} != {MODEL!r}")
                truth.append(primary_score(rdir / "metrics.json")["primary"])
                _sha(rdir / "metrics.json")
                edges.append(parse_edges(rdir / "output_network.csv"))
                _sha(rdir / "output_network.csv")
                exp_ids.append(int(exp_id))
                rep_path = cdir / "replica_exp_id"
                if rep_path.exists():
                    rid = rep_path.read_text().strip()
                    _sha(rep_path)
                    rrdir = root / "run/results" / rid
                    rargs = json.loads((rrdir / "arguments.json").read_text())
                    _sha(rrdir / "arguments.json")
                    if rargs.get("model_name") != MODEL:
                        pin_violations.append(f"{rrdir}: replica model_name={rargs.get('model_name')!r}")
                    for k in ("training_regime", "fraction_partial_intervention", "partial_intervention_seed"):
                        if str(rargs.get(k)).lower() != str(args.get(k)).lower():
                            pin_violations.append(f"{rrdir}: replica differs from original on {k}")
                    rep_edges.append(parse_edges(rrdir / "output_network.csv"))
                    _sha(rrdir / "output_network.csv")
                    rep_ids.append(int(rid))
                else:
                    rep_edges.append(None)
                    rep_ids.append(None)
            chains.append({"key": key, "feedback": fb_dicts, "truth": truth, "exp_ids": exp_ids,
                           "replica_exp_ids": rep_ids, "n_edges": [len(e) for e in edges],
                           "scores": candidate_scores(fb_dicts, edges, rep_edges)})
    return {"tag": tag, "root": str(root), "chains": chains, "incomplete": incomplete,
            "pin_violations": pin_violations}


# ------------------------------------------------------------------ statistics
def pooled_rho(usable: list[tuple[list[float], list[float]]], *, seed: int, draws: int) -> tuple[float, float]:
    """Arithmetic pooled Spearman + within-chain cycle-shuffle two-sided perm p (m5' form)."""
    rhos = [spearman(ss, tt) for ss, tt in usable]
    raw = mean(rhos)
    rng = random.Random(seed)
    hits = 0
    for _ in range(draws):
        perm = mean([spearman(rng.sample(ss, len(ss)), tt) for ss, tt in usable])
        if abs(perm) >= abs(raw):
            hits += 1
    return raw, hits / draws


def eval_candidate(chains: list[dict], cand: str, *, seed: int = SHUFFLE_SEED, draws: int = DRAWS) -> dict:
    usable, excluded, keys = [], [], []
    for ch in chains:
        pairs = [(s, t) for s, t in zip(ch["scores"][cand], ch["truth"])
                 if math.isfinite(t) and math.isfinite(s)]
        if len(pairs) < 3:
            excluded.append(ch["key"])
            continue
        usable.append(([p[0] for p in pairs], [p[1] for p in pairs]))
        keys.append(ch["key"])
    if not usable:
        return {"raw_pooled_rho": float("nan"), "directed_pooled_rho": float("nan"),
                "perm_p_two_sided": float("nan"), "chains_used": 0, "chains_excluded_lt3": excluded,
                "per_chain_rho": []}
    raw, p = pooled_rho(usable, seed=seed, draws=draws)
    return {"raw_pooled_rho": raw, "directed_pooled_rho": -DIRECTIONS[cand] * raw,
            "perm_p_two_sided": p, "chains_used": len(usable), "chains_excluded_lt3": excluded,
            "per_chain_rho": [f"{k}:{spearman(ss, tt):.4f}" for k, (ss, tt) in zip(keys, usable)]}


def argmax_census(chains: list[dict], cand: str) -> dict:
    rows = []
    for ch in chains:
        if not all(math.isfinite(t) for t in ch["truth"]):
            continue
        sc = [v * DIRECTIONS[cand] for v in ch["scores"][cand]]
        if any(not math.isfinite(v) for v in sc):
            continue
        idx = sc.index(max(sc))  # earliest cycle wins ties (m4 convention)
        rows.append({"key": ch["key"], "ship_cycle": CYCLES[idx], "ship_true_rank": _ranks(ch["truth"])[idx]})
    return {"chains": len(rows),
            "ship_true_rank_mean": mean([r["ship_true_rank"] for r in rows]) if rows else float("nan"),
            "ship_cycle_census": {str(c): sum(1 for r in rows if r["ship_cycle"] == c) for c in CYCLES}}


def paired_signflip_p(diffs: list[float]) -> float:
    """Exact one-sided sign-flip p for mean(diffs) > 0 (n <= 16 enumerated)."""
    n = len(diffs)
    if n == 0:
        return 1.0
    t_obs = sum(diffs) / n
    count = 0
    for mask in range(2 ** n):
        t = sum(d if (mask >> i) & 1 else -d for i, d in enumerate(diffs)) / n
        if t >= t_obs:
            count += 1
    return count / 2 ** n


def nullcal(*, reps: int = NULLCAL_REPS, draws: int = NULLCAL_DRAWS, seed: int = NULLCAL_SEED) -> dict:
    """Machinery check for the rho permutation: random 12x4 cohorts must reject at ~alpha."""
    rng = random.Random(seed)
    rejections = 0
    for r in range(reps):
        usable = [([rng.random() for _ in CYCLES], [rng.random() for _ in CYCLES]) for _ in range(12)]
        _, p = pooled_rho(usable, seed=seed + 1 + r, draws=draws)
        if p < P_GATE:
            rejections += 1
    rate = rejections / reps
    return {"control": "rho_permutation_null_calibration", "reps": reps, "draws": draws,
            "rejection_rate": rate, "accept_band": list(NULLCAL_BAND),
            "verdict": "PASS" if NULLCAL_BAND[0] <= rate <= NULLCAL_BAND[1] else "FAIL"}


def selftest_edges() -> dict:
    """Jaccard/edge-parse selftest (Stage-2b precedent): J(E,E)=1, J(E,disjoint)=0, round-trip."""
    a = {("g1", "g2"), ("g2", "g3"), ("g3", "g4")}
    b = {("g1", "g2"), ("g9", "g8")}
    checks = {"J_self": jaccard(a, a) == 1.0, "J_disjoint": jaccard(a, {("x", "y")}) == 0.0,
              "J_partial": abs(jaccard(a, b) - 0.25) < 1e-12, "J_empty_pair": jaccard(set(), set()) == 1.0}
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "output_network.csv"
        p.write_text(",0,1\n0,g1,g2\n1,g2,g3\n2,g3,g4\n")
        checks["parse_roundtrip"] = parse_edges(p) == a
        p.write_text('""\n')
        checks["parse_empty"] = parse_edges(p) == set()
    return {"control": "edge_parse_jaccard_selftest", "checks": checks,
            "verdict": "PASS" if all(checks.values()) else "FAIL"}


# --------------------------------------------------------------------- gates
def controls_from_runner(root: Path) -> dict:
    out = {}
    for name, rel in (("planted", "run/controls/planted/planted.json"), ("nullcal_signflip", "run/controls/nullcal.json")):
        p = root / rel
        if p.exists():
            _sha(p)
            out[name] = json.loads(p.read_text()).get("verdict")
        else:
            out[name] = "ABSENT"
    return out


def g0_validity(cohorts: dict, screen_controls: dict) -> tuple[bool, dict]:
    detail = {}
    ok = all(v["verdict"] == "PASS" for v in screen_controls.values())
    detail["screen_controls_pass"] = ok
    for tag, coh in cohorts.items():
        chains = coh["chains"]
        n_cycles = len(chains) * len(CYCLES)
        nan_cycles = sum(1 for ch in chains for t in ch["truth"] if not math.isfinite(t))
        ge3 = sum(1 for ch in chains if sum(1 for t in ch["truth"] if math.isfinite(t)) >= 3)
        distinct3 = sum(1 for ch in chains if len(set(round(v, 12) for v in ch["scores"][PRIMARY])) >= 3)
        d = {"chains_complete": len(chains), "incomplete": coh["incomplete"],
             "runner_controls": coh["runner_controls"], "pin_violations": coh["pin_violations"],
             "nan_cycle_fraction": (nan_cycles / n_cycles) if n_cycles else 1.0,
             "chains_ge3_finite": ge3, "chains_purity_distinct3": distinct3}
        d["pass"] = (len(chains) >= MIN_COMPLETE_CHAINS and not coh["pin_violations"]
                     and coh["runner_controls"].get("planted") == "PASS"
                     and coh["runner_controls"].get("nullcal_signflip") == "PASS"
                     and d["nan_cycle_fraction"] <= MAX_NAN_CYCLE_FRACTION
                     and ge3 >= MIN_CHAINS_GE3_FINITE and distinct3 >= MIN_CHAINS_PURITY_DISTINCT3)
        detail[tag] = d
        ok = ok and d["pass"]
    return ok, detail


def evaluate(cohorts: dict, *, draws: int = DRAWS) -> dict:
    table = {tag: {k: eval_candidate(coh["chains"], k, draws=draws) for k in DIRECTIONS}
             for tag, coh in cohorts.items()}
    pooled_chains = cohorts["R_prime"]["chains"] + cohorts["P_prime"]["chains"]
    table["POOLED_24"] = {k: eval_candidate(pooled_chains, k, draws=draws) for k in DIRECTIONS}

    r, p = table["R_prime"][PRIMARY], table["P_prime"][PRIMARY]
    g1_r = bool(r["chains_used"] and r["directed_pooled_rho"] > 0 and r["perm_p_two_sided"] <= P_GATE)
    g1_sign = bool(p["chains_used"] and p["directed_pooled_rho"] > 0)
    g1 = g1_r and g1_sign
    pooled = table["POOLED_24"][PRIMARY]
    g1_plus = bool(pooled["chains_used"] and pooled["directed_pooled_rho"] > 0 and pooled["perm_p_two_sided"] <= P_GATE)

    # G2: the anti-ranking must be ABSENT for a channel-external signal on R'.
    def specificity(cand: str) -> dict:
        chains = cohorts["R_prime"]["chains"]
        nonconst = sum(1 for ch in chains
                       if len(set(round(v, 12) for v in ch["scores"][cand] if math.isfinite(v))) >= 2)
        row = table["R_prime"][cand]
        usable = row["chains_used"] >= MIN_CHAINS_J_NONCONSTANT and nonconst >= MIN_CHAINS_J_NONCONSTANT
        anti = bool(row["chains_used"] and row["raw_pooled_rho"] > 0 and row["perm_p_two_sided"] <= P_GATE)
        # strengthening (non-gating): per-chain raw rho(purity) - raw rho(external) > 0 ?
        diffs = []
        for ch in chains:
            pr = [(s, t) for s, t in zip(ch["scores"][PRIMARY], ch["truth"]) if math.isfinite(s) and math.isfinite(t)]
            ex = [(s, t) for s, t in zip(ch["scores"][cand], ch["truth"]) if math.isfinite(s) and math.isfinite(t)]
            if len(pr) >= 3 and len(ex) >= 3:
                diffs.append(spearman([a for a, _ in pr], [b for _, b in pr])
                             - spearman([a for a, _ in ex], [b for _, b in ex]))
        return {"candidate": cand, "chains_nonconstant": nonconst, "usable": usable,
                "significant_anti_ranking": anti,
                "verdict": ("CANNOT_CHECK" if not usable else ("PASS" if not anti else "FAIL")),
                "paired_purity_minus_external": {"n": len(diffs), "mean_d": mean(diffs) if diffs else float("nan"),
                                                 "signflip_p_one_sided": paired_signflip_p(diffs) if diffs else 1.0}}

    g2_primary = specificity(EXTERNAL_PRIMARY)
    g2_fallback = specificity(EXTERNAL_FALLBACK)
    g2_source = EXTERNAL_PRIMARY if g2_primary["verdict"] != "CANNOT_CHECK" else EXTERNAL_FALLBACK
    g2_verdict = g2_primary["verdict"] if g2_source == EXTERNAL_PRIMARY else g2_fallback["verdict"]

    return {"table": table,
            "G1_ANTI_RANKING_REPLICATES": g1, "G1_detail": {"R_prime_directed_rho_gt0_and_p_le_0.05": g1_r,
                                                            "P_prime_same_sign": g1_sign,
                                                            "POOLED_24_secondary": g1_plus},
            "G2_MECHANISM_SPECIFIC": g2_verdict, "G2_source": g2_source,
            "G2_detail": {EXTERNAL_PRIMARY: g2_primary, EXTERNAL_FALLBACK: g2_fallback},
            "purity_argmax_census": {tag: argmax_census(coh["chains"], PRIMARY) for tag, coh in cohorts.items()}}


def route(g0: bool, g1: bool, g2: str) -> str:
    if not g0:
        return "CANNOT_CHECK__CAMPAIGN_INVALID: diagnose mechanics under a separate freeze; no science claim"
    if not g1:
        return "SALIENCE_ANTI_RANKING_NOT_REPLICATED: m5' observation filed as a single-learner artefact"
    if g2 == "PASS":
        return ("SALIENCE_ANTI_RANKING_REPLICATED_CROSS_LEARNER: H-EXT-2 advances one rung; authorize a "
                "cross-substrate cell design under its own freeze (no field/novelty claim)")
    if g2 == "FAIL":
        return ("ANTI_RANKING_NOT_CHANNEL_SPECIFIC: anti-ranking also present for a channel-external signal; "
                "locus claim unsupported, phenomenon parent-owned (Goodhart / proxy misalignment)")
    return "G2_CANNOT_CHECK: G1 replicated but no usable external anchor; specificity untested (report as such)"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    screen_controls = {"nullcal_rho": nullcal(reps=int(os.environ.get("HEXT2_NULLCAL_REPS", NULLCAL_REPS)),
                                              draws=int(os.environ.get("HEXT2_NULLCAL_DRAWS", NULLCAL_DRAWS))),
                       "edges": selftest_edges()}
    cohorts = {"R_prime": build_cohort("R_prime", RPRIME_ROOT), "P_prime": build_cohort("P_prime", PPRIME_ROOT)}
    for tag, coh in cohorts.items():
        coh["runner_controls"] = controls_from_runner(Path(coh["root"]))
    if MODEL == PARENT_MODEL:
        screen_controls["fresh_learner"] = {"verdict": "FAIL", "reason": "HEXT2_MODEL equals the parent cell learner"}
    g0, g0_detail = g0_validity(cohorts, screen_controls)
    draws = int(os.environ.get("HEXT2_DRAWS", DRAWS))
    ev = evaluate(cohorts, draws=draws)
    verdict_route = route(g0, ev["G1_ANTI_RANKING_REPLICATES"], ev["G2_MECHANISM_SPECIFIC"])
    gates = {"G0_CAMPAIGN_VALID": g0, "G0_detail": g0_detail,
             "G1_ANTI_RANKING_REPLICATES": ev["G1_ANTI_RANKING_REPLICATES"], "G1_detail": ev["G1_detail"],
             "G2_MECHANISM_SPECIFIC": ev["G2_MECHANISM_SPECIFIC"], "G2_source": ev["G2_source"],
             "preregistered_route": verdict_route}
    rollup = {"schema_version": "orion.v2.h-ext2.salience-goodhart-rollup.v1",
              "variant": "h-ext2-salience-goodhart-replication",
              "design": "H_EXT2_SALIENCE_GOODHART_REPLICATION_DESIGN_V1",
              "model": MODEL, "parent_model": PARENT_MODEL, "primary": PRIMARY,
              "directions": DIRECTIONS, "shuffle_seed": SHUFFLE_SEED, "draws": draws,
              "screen_controls": screen_controls, "cohorts": {t: {"root": c["root"], "chains": len(c["chains"]),
                                                                  "incomplete": c["incomplete"],
                                                                  "runner_controls": c["runner_controls"]}
                                                              for t, c in cohorts.items()},
              "table": ev["table"], "G2_detail": ev["G2_detail"],
              "purity_argmax_census": ev["purity_argmax_census"], "gates": gates,
              "manifest": {"n_files": len(_MANIFEST), "files": _MANIFEST}}
    (OUT_DIR / "H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.json").write_text(json.dumps(rollup, indent=1, sort_keys=True))

    lines = ["# H-EXT-2 salience-Goodhart replication rollup V1", "",
             f"model: {MODEL} (parent cell: {PARENT_MODEL})", f"primary: {PRIMARY} (registered direction -1)",
             f"route: {verdict_route}", ""]
    for coh, cands in ev["table"].items():
        lines += [f"## {coh}", "| candidate | raw rho | directed rho | perm p | used | excl |", "|---|---|---|---|---|---|"]
        for k, v in sorted(cands.items()):
            lines.append(f"| {k} | {v['raw_pooled_rho']:+.4f} | {v['directed_pooled_rho']:+.4f} "
                         f"| {v['perm_p_two_sided']:.5f} | {v['chains_used']} | {len(v['chains_excluded_lt3'])} |")
        lines.append("")
    lines += ["## gates", json.dumps({k: v for k, v in gates.items() if k != "G0_detail"}, indent=1, sort_keys=True)]
    (OUT_DIR / "H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"gates": {k: v for k, v in gates.items() if not k.endswith("detail")}}, indent=1))
    return 0 if g0 else 2


if __name__ == "__main__":
    sys.exit(main())
