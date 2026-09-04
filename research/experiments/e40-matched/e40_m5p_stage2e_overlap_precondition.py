#!/usr/bin/env python3
"""E40-m5' Stage-2e — replica-overlap precondition probe (ZERO model calls).

Stage-2c's seed-replica stability probe rests on a premise it never tested: that
independent seed-replicas of the same cell produce output graphs whose agreement
carries information. Stage-2c measured consensus J = 0.0093..0.0520 (mean 0.0282),
but a config census of its 48 live chains shows the replicas were NOT running the
same config: in 26 of 48 cell-cycles all four replicas held four DIFFERENT non-seed
configs, in 19 three, in 3 two, and in none did all four agree. So the reported J
conflated seed variation with config variation, and the seed-only quantity the
premise is about was never measured.

This probe measures it directly, with no model in the loop at all: the configs are
fixed by the design, so there is no prompt, no mandate, no served-model channel and
no channel drift. It answers one question:

    On the pinned substrate (gies / weissmann, subset 0.05, do_filter), does varying
    ONLY the seed pair produce replicas whose edge-set agreement has any dynamic
    range -- and does that agreement discriminate seed variation from config variation?

Both failure directions are pre-registered, because both void the premise:
  * J_seed_only near 0   -> replicas are near-disjoint; the statistic cannot rank.
  * J_seed_only near 1   -> the seed knob generates no replica independence at all,
                            so "independent seed-replicas" do not exist here and the
                            only thing that ever moved the graphs was the model's own
                            config choices, i.e. the feedback channel the probe was
                            meant to be independent of.

Commands: `selftest`, `plan`, `run --task N`, `analyze`.
Exit codes are DISTINCT: 0 admissible verdict, 3 campaign not settled,
5 could-not-check (a control failed or an envelope is inhomogeneous). "Could not
check" is never reported as "checked and fine".
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

# ------------------------------------------------------------------ identity
SCHEMA = "orion.v2.e40-matched.m5p-stage2e-overlap-precondition.v1"
DESIGN = "E40_M5P_STAGE2E_OVERLAP_PRECONDITION_DESIGN_V1"
BASE = Path(os.environ.get("E40M_BASE", "/projects/hep/fs9/users/scyiu/orion-v2-e45"))
ROOT = Path(os.environ.get("E40M_ROOT", str(BASE / "campaign-e40-m5p-stage2e")))
RESULTS = ROOT / "run/results"
OUT_DIR = ROOT / "run/rollup"
VENV_PY = Path(os.environ.get("E40M_PY", str(BASE / "campaign-e40-r3/run/venv/bin/python")))
CAUSALBENCH_SRC = Path(os.environ.get("E40M_SRC", str(BASE / "campaign-e40-r3/causalbench")))
DATA_DIR = Path(os.environ.get("E40M_DATA", str(BASE / "datasets/causalbench/raw")))
EXP_ID_BASE = 505000

# --------------------------------------------- frozen grid (design §2, pre-run)
DATASETS = ("weissmann_k562", "weissmann_rpe1")
# Seed table inherited VERBATIM from the Stage-2c replica table (design §2.1).
SEEDS = (("s0", 11, 13), ("s1", 29, 31), ("s2", 47, 53), ("s3", 71, 79))
# Non-seed configs fixed by the design (no model chooses them). They span the
# training_regime axis and two interior partial fractions.
CONFIGS = (
    ("c0", "interventional", 0.0),
    ("c1", "partial_interventional", 0.5),
    ("c2", "partial_interventional", 0.8),
    ("c3", "observational", 0.0),
)
SUBSTRATE = {"model_name": "gies", "subset_data": 0.05, "max_path_length": -1,
             "omission_estimation_size": 1000}
# One determinism repeat per dataset: (c0, s0) run again at its own exp_id. If the
# substrate is seed-deterministic these two runs are identical and J == 1.0; this is
# the known-answer control proving the pipeline CAN produce a high J.
DETERMINISM_REPEAT = ("c0", "s0")

# ------------------------------------------------------- frozen gate constants
P1_J_FLOOR = 0.20          # below: replicas near-disjoint, statistic has no resolution
P1_J_CEILING = 0.98        # above: seed knob generates no independence
P2_ALPHA = 0.05            # one-sided, stratified EXHAUSTIVE permutation (no RNG)
JACCARD_SELFTEST_SEED = 20260902   # inherited from Stage-2c controls

_MANIFEST: list[dict[str, str]] = []


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha(p: Path) -> str:
    d = sha256_file(p)
    _MANIFEST.append({"path": str(p), "sha256": d})
    return d


def mean(xs: list[float]) -> float:
    # math.fsum: correctly-rounded, interpreter-independent (Stage-2c convention).
    return math.fsum(xs) / len(xs)


# ------------------------------ edge/Jaccard primitives (Stage-2c, byte-identical)
# A unit test asserts these are character-for-character the Stage-2c definitions, so
# "same statistic as the probe it is a precondition for" is verified, not asserted.
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


# ----------------------------------------------------------------- slot algebra
def slots() -> list[dict[str, Any]]:
    """The frozen run grid: 2 datasets x 4 configs x 4 seeds + 2 determinism repeats."""
    out: list[dict[str, Any]] = []
    for ds in DATASETS:
        for cname, regime, frac in CONFIGS:
            for sname, ms, ps in SEEDS:
                out.append({"dataset": ds, "config": cname, "seed": sname, "repeat": 0,
                            "cfg": {**SUBSTRATE, "dataset_name": ds, "training_regime": regime,
                                    "fraction_partial_intervention": frac,
                                    "model_seed": ms, "partial_intervention_seed": ps}})
    for ds in DATASETS:
        cname, sname = DETERMINISM_REPEAT
        regime, frac = next((r, f) for c, r, f in CONFIGS if c == cname)
        ms, ps = next((m, p) for s, m, p in SEEDS if s == sname)
        out.append({"dataset": ds, "config": cname, "seed": sname, "repeat": 1,
                    "cfg": {**SUBSTRATE, "dataset_name": ds, "training_regime": regime,
                            "fraction_partial_intervention": frac,
                            "model_seed": ms, "partial_intervention_seed": ps}})
    for i, s in enumerate(out):
        s["task"] = i
        s["exp_id"] = EXP_ID_BASE + i
        s["key"] = f"{s['dataset']}|{s['config']}|{s['seed']}|r{s['repeat']}"
    return out


# ---------------------------------------------------------------- native driver
def native_run(cfg: dict[str, Any], exp_id: int, log_path: Path) -> Path:
    """One pinned-native invocation (m2/m3/Stage-2c verbatim command shape)."""
    out_dir = RESULTS / str(exp_id)
    metrics = out_dir / "metrics.json"
    if metrics.exists():
        return metrics
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["/usr/bin/time", "-v", str(VENV_PY), "-m", "causalscbench.apps.main_app",
           "--output_directory", str(RESULTS), "--data_directory", str(DATA_DIR),
           "--model_name", cfg["model_name"], "--dataset_name", cfg["dataset_name"],
           "--training_regime", cfg["training_regime"],
           "--fraction_partial_intervention", str(cfg["fraction_partial_intervention"]),
           "--partial_intervention_seed", str(cfg["partial_intervention_seed"]),
           "--model_seed", str(cfg["model_seed"]),
           "--subset_data", str(cfg["subset_data"]), "--do_filter",
           "--max_path_length", str(cfg["max_path_length"]),
           "--omission_estimation_size", str(cfg["omission_estimation_size"]),
           "--exp_id", str(exp_id)]
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w") as log:
        log.write(" ".join(cmd) + "\n")
        log.flush()
        proc = subprocess.run(cmd, cwd=str(CAUSALBENCH_SRC), stdout=log, stderr=log)
    if proc.returncode != 0 or not metrics.exists():
        raise RuntimeError(f"native run exp_id={exp_id} failed rc={proc.returncode}")
    return metrics


def run_task(task: int) -> int:
    s = next(x for x in slots() if x["task"] == task)
    native_run(s["cfg"], s["exp_id"], ROOT / f"run/logs/native_{s['exp_id']}.log")
    (RESULTS / str(s["exp_id"]) / "slot.json").write_text(json.dumps(s, indent=1, sort_keys=True))
    print(json.dumps({"task": task, "exp_id": s["exp_id"], "key": s["key"], "status": "DONE"}))
    return 0


# ------------------------------------------------- per-envelope homogeneity gate
def envelope_status(s: dict[str, Any]) -> dict[str, Any]:
    """Every run must be settled AND provably the config the design froze for its slot.
    A run whose arguments.json disagrees with its frozen slot is INHOMOGENEOUS -- it is
    excluded, counted and reported, never silently used. (E30-R12 lesson: pinning an id
    does not pin a condition; assert the condition itself, per envelope.)"""
    d = RESULTS / str(s["exp_id"])
    metrics, args, net = d / "metrics.json", d / "arguments.json", d / "output_network.csv"
    if not d.exists():
        return {"status": "MISSING", "detail": "no result dir"}
    for p in (metrics, args, net):
        if not p.exists():
            return {"status": "IN_PROGRESS", "detail": f"missing {p.name}"}
    got = json.loads(args.read_text())
    mismatched = {}
    for k, want in s["cfg"].items():
        have = got.get(k)
        if isinstance(want, float) or isinstance(have, float):
            ok = have is not None and abs(float(have) - float(want)) < 1e-12
        else:
            ok = str(have) == str(want)
        if not ok:
            mismatched[k] = {"frozen": want, "recorded": have}
    if mismatched:
        return {"status": "INHOMOGENEOUS", "detail": mismatched}
    for p in (metrics, args, net):
        _sha(p)
    return {"status": "COMPLETE", "n_edges": len(parse_edges(net))}


# ------------------------------------------------------------------- statistics
def strat_perm_p(seed_only: dict[str, list[float]], config_only: dict[str, list[float]]) -> dict:
    """One-sided stratified EXHAUSTIVE permutation, no RNG at all.
    H0: within each dataset stratum the seed-only and config-only J values are
    exchangeable. T = pooled mean(seed_only) - pooled mean(config_only).
    Enumerates every within-stratum relabelling (C(8,4)^2 = 4900 here)."""
    strata = sorted(set(seed_only) | set(config_only))
    pools, na = [], []
    for st in strata:
        a, b = seed_only.get(st, []), config_only.get(st, [])
        pools.append(a + b)
        na.append(len(a))
    n_a = math.fsum(na)
    if n_a == 0 or math.fsum(len(p) for p in pools) == n_a:
        return {"status": "CANNOT_CHECK", "detail": "a stratum has no contrast"}
    obs_a = math.fsum(math.fsum(seed_only.get(st, [])) for st in strata)
    obs_b = math.fsum(math.fsum(config_only.get(st, [])) for st in strata)
    n_b = math.fsum(len(config_only.get(st, [])) for st in strata)
    t_obs = obs_a / n_a - obs_b / n_b
    combos = [list(itertools.combinations(range(len(p)), k)) for p, k in zip(pools, na)]
    total = ge = 0
    for pick in itertools.product(*combos):
        sa = math.fsum(pools[i][j] for i, idxs in enumerate(pick) for j in idxs)
        sb = math.fsum(math.fsum(pools[i]) for i in range(len(pools))) - sa
        t = sa / n_a - sb / n_b
        total += 1
        if t >= t_obs - 1e-15:
            ge += 1
    return {"status": "OK", "t_obs": t_obs, "draws": total, "exhaustive": True,
            "p_one_sided": ge / total}


# --------------------------------------------------------------------- controls
def control_jaccard_selftest(*, seed: int = JACCARD_SELFTEST_SEED) -> dict:
    rng = random.Random(seed)
    genes = [f"ENSG{i:011d}" for i in range(400)]
    E: set[tuple[str, str]] = set()
    while len(E) < 417:
        s, t = rng.sample(genes, 2)
        E.add((s, t))
    src = [e[0] for e in E]
    dst = [e[1] for e in E]
    rng.shuffle(dst)
    E_shuf = set(zip(src, dst))
    checks = {"J_E_E": jaccard(E, E), "J_E_shuffled": jaccard(E, E_shuf),
              "J_E_empty": jaccard(E, set()),
              "J_half": jaccard(set(list(E)[:200]), set(list(E)[100:300]))}
    ok = (checks["J_E_E"] == 1.0 and checks["J_E_shuffled"] < 0.05
          and checks["J_E_empty"] == 0.0 and abs(checks["J_half"] - 100 / 300) < 1e-12)
    return {"control": "jaccard_selftest", **checks, "verdict": "PASS" if ok else "FAIL"}


def control_edge_roundtrip(tmp: Path, *, seed: int = JACCARD_SELFTEST_SEED) -> dict:
    rng = random.Random(seed)
    genes = [f"ENSG{i:011d}" for i in range(300)]
    edges, seen = [], set()
    while len(edges) < 417:
        s, t = rng.sample(genes, 2)
        if (s, t) not in seen:
            seen.add((s, t))
            edges.append((s, t))
    p = tmp / "output_network.csv"
    write_edges(p, edges)
    parsed = parse_edges(p)
    bad_ok = False
    p4 = tmp / "bad.csv"
    p4.write_text("src,dst\na,b\n")
    try:
        parse_edges(p4)
    except ValueError:
        bad_ok = True
    ok = parsed == seen and len(parsed) == 417 and bad_ok
    return {"control": "edge_roundtrip", "n_parsed": len(parsed), "rejects_bad_shape": bad_ok,
            "verdict": "PASS" if ok else "FAIL"}


def control_permutation_null(*, reps: int = 400, seed: int = 20260903) -> dict:
    """The stratified exhaustive permutation must reject at ~alpha under H0."""
    rng = random.Random(seed)
    rej = 0
    for _ in range(reps):
        so = {ds: [rng.random() for _ in range(4)] for ds in DATASETS}
        co = {ds: [rng.random() for _ in range(4)] for ds in DATASETS}
        if strat_perm_p(so, co)["p_one_sided"] <= P2_ALPHA:
            rej += 1
    rate = rej / reps
    return {"control": "permutation_null_calibration", "reps": reps, "seed": seed,
            "rejection_rate": rate, "accept_band": [0.02, 0.09],
            "verdict": "PASS" if 0.02 <= rate <= 0.09 else "FAIL"}


def control_determinism(cells: dict[str, Any]) -> dict:
    """Known-answer: the (c0,s0) repeat pair. If the substrate is seed-deterministic
    this J is 1.0 -- proof the pipeline CAN produce a high J, so a low seed-only J
    elsewhere is a substrate fact and not a broken parser."""
    per = {}
    for ds in DATASETS:
        a = cells.get(f"{ds}|{DETERMINISM_REPEAT[0]}|{DETERMINISM_REPEAT[1]}|r0")
        b = cells.get(f"{ds}|{DETERMINISM_REPEAT[0]}|{DETERMINISM_REPEAT[1]}|r1")
        per[ds] = jaccard(a, b) if (a is not None and b is not None) else None
    vals = [v for v in per.values() if v is not None]
    ok = len(vals) == len(DATASETS)
    return {"control": "determinism_repeat", "J_per_dataset": per,
            "verdict": "PASS" if ok else "FAIL",
            "note": "records the value; the PASS rule is only that BOTH repeats exist and parse"}


def registered_controls(tmp: Path, cells: dict[str, Any]) -> dict:
    """The registered control battery. There is no reduced variant: a --fast mode that
    can return a different verdict from the same code is the silent-failure pattern this
    programme exists to prevent. 400 reps x 4900 exhaustive permutations costs seconds."""
    return {"jaccard": control_jaccard_selftest(),
            "edge_roundtrip": control_edge_roundtrip(tmp),
            "nullcal": control_permutation_null(reps=400),
            "determinism": control_determinism(cells)}


def controls_gate(controls: dict | None) -> dict:
    """Stage-2c REPAIR R1 pattern: controls are CONSUMED. Absence is its own status."""
    if controls is None:
        return {"status": "CONTROLS_UNAVAILABLE", "per_control": {}}
    per, missing, failed = {}, [], []
    for name in ("jaccard", "edge_roundtrip", "nullcal", "determinism"):
        rec = controls.get(name)
        if not isinstance(rec, dict) or "verdict" not in rec:
            per[name] = "ABSENT"
            missing.append(name)
            continue
        per[name] = rec["verdict"]
        if rec["verdict"] != "PASS":
            failed.append(name)
    if missing:
        return {"status": "CONTROLS_UNAVAILABLE", "per_control": per, "missing": missing}
    if failed:
        return {"status": "CONTROL_FAILED", "per_control": per, "failed": failed}
    return {"status": "VALID", "per_control": per}


# ------------------------------------------------------------------------ gates
def evaluate_gates(stats: dict, controls: dict | None) -> dict:
    cg = controls_gate(controls)
    p0 = cg["status"] == "VALID" and stats.get("envelopes_ok") is True
    j = stats.get("seed_only_mean_J")
    p1 = bool(p0 and j is not None and P1_J_FLOOR <= j <= P1_J_CEILING)
    perm = stats.get("perm", {})
    p2 = bool(p0 and perm.get("status") == "OK" and perm.get("t_obs", 0) > 0
              and perm.get("p_one_sided", 1.0) <= P2_ALPHA)
    if not p0:
        disp = "CANNOT_CHECK"
        route = ("could-not-check: a registered control failed or an envelope is "
                 "inhomogeneous; nothing is filed about the precondition")
    elif not p1:
        if j is not None and j < P1_J_FLOOR:
            disp = "E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT"
            route = ("seed-only replicas are near-disjoint: the consensus statistic has no "
                     "dynamic range on this substrate under ANY prompt, mandate or model, so "
                     "the Stage-2c probe is not testable here. This is a PRECONDITION terminal, "
                     "explicitly NOT the registered E40_TERMINAL (which needs a valid "
                     "G0-pass / G1-G4-fail run).")
        else:
            disp = "E40_PROBE_PRECONDITION_UNMET__REPLICATION_DEGENERATE"
            route = ("the seed knob generates no replica independence: 'independent "
                     "seed-replicas' do not exist on this substrate, so the probe's premise is "
                     "void. PRECONDITION terminal, NOT the registered E40_TERMINAL.")
    elif not p2:
        disp = "AMBIGUOUS__PRECONDITION_MET_STATISTIC_NON_DISCRIMINATING"
        route = ("the precondition holds but seed-only agreement does not exceed config-only "
                 "agreement: reported as ambiguous in exactly those words")
    else:
        disp = "PROBE_PRECONDITION_MET"
        route = ("the precondition holds and the statistic discriminates: closure of the E40 "
                 "line requires a mandate-free re-run of the seed-replica probe under its own "
                 "freeze; that campaign is the single blocking artifact")
    return {"P0_CONTROLS_AND_ENVELOPES_VALID": p0, "P1_SEED_REPLICATION_INFORMATIVE": p1,
            "P2_CONSENSUS_DISCRIMINATES": p2, "gates_admissible": p0,
            "controls_gate": cg, "disposition": disp, "preregistered_route": route}


# ---------------------------------------------------------------------- analyse
def load_cells() -> tuple[dict[str, set], dict[str, dict]]:
    edges, status = {}, {}
    for s in slots():
        st = envelope_status(s)
        status[s["key"]] = st
        if st["status"] == "COMPLETE":
            edges[s["key"]] = parse_edges(RESULTS / str(s["exp_id"]) / "output_network.csv")
    return edges, status


def analyse(edges: dict[str, set], status: dict[str, dict]) -> dict:
    unsettled = {k: v for k, v in status.items() if v["status"] != "COMPLETE"}
    seed_only, config_only, detail = {}, {}, {}
    for ds in DATASETS:
        so, co = [], []
        for cname, _r, _f in CONFIGS:
            es = [edges[f"{ds}|{cname}|{sn}|r0"] for sn, _m, _p in SEEDS
                  if f"{ds}|{cname}|{sn}|r0" in edges]
            if len(es) >= 2:
                v = consensus_j(es)
                so.append(v)
                detail[f"seed_only:{ds}:{cname}"] = {"J": v, "k": len(es),
                                                     "n_edges": [len(e) for e in es]}
        for sn, _m, _p in SEEDS:
            es = [edges[f"{ds}|{cname}|{sn}|r0"] for cname, _r, _f in CONFIGS
                  if f"{ds}|{cname}|{sn}|r0" in edges]
            if len(es) >= 2:
                v = consensus_j(es)
                co.append(v)
                detail[f"config_only:{ds}:{sn}"] = {"J": v, "k": len(es),
                                                    "n_edges": [len(e) for e in es]}
        seed_only[ds], config_only[ds] = so, co
    flat_so = [v for ds in DATASETS for v in seed_only[ds]]
    flat_co = [v for ds in DATASETS for v in config_only[ds]]
    perm = (strat_perm_p(seed_only, config_only) if flat_so and flat_co
            else {"status": "CANNOT_CHECK", "detail": "no contrast available"})
    return {"envelopes_ok": not unsettled, "unsettled": unsettled,
            "n_complete": len(edges), "n_slots": len(status),
            "seed_only_J_by_dataset": seed_only, "config_only_J_by_dataset": config_only,
            "seed_only_mean_J": mean(flat_so) if flat_so else None,
            "config_only_mean_J": mean(flat_co) if flat_co else None,
            "detail": detail, "perm": perm}


def run_analysis(*, write: bool = True) -> tuple[int, dict]:
    import tempfile
    edges, status = load_cells()
    stats = analyse(edges, status)
    with tempfile.TemporaryDirectory() as td:
        controls = registered_controls(Path(td), edges)
    gates = evaluate_gates(stats, controls)
    doc = {"schema_version": SCHEMA, "design": DESIGN, "campaign_root": str(ROOT),
           "model_calls": 0,
           "note": "zero model calls by construction: every config is fixed by the design",
           "grid": {"datasets": list(DATASETS), "configs": [list(c) for c in CONFIGS],
                    "seeds": [list(s) for s in SEEDS], "exp_id_base": EXP_ID_BASE},
           "analysis": stats, "controls": controls, "gates": gates,
           "manifest": {"n_files": len(_MANIFEST), "files": _MANIFEST}}
    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "E40_M5P_STAGE2E_ROLLUP_V1.json").write_text(
            json.dumps(doc, indent=1, sort_keys=True))
    print(json.dumps({"disposition": gates["disposition"],
                      "P0": gates["P0_CONTROLS_AND_ENVELOPES_VALID"],
                      "P1": gates["P1_SEED_REPLICATION_INFORMATIVE"],
                      "P2": gates["P2_CONSENSUS_DISCRIMINATES"],
                      "seed_only_mean_J": stats["seed_only_mean_J"],
                      "config_only_mean_J": stats["config_only_mean_J"],
                      "perm": stats["perm"], "n_complete": stats["n_complete"],
                      "unsettled": list(stats["unsettled"])[:5]}, indent=1))
    if not stats["envelopes_ok"] and all(
            v["status"] in ("MISSING", "IN_PROGRESS") for v in stats["unsettled"].values()):
        return 3, doc
    return (0 if gates["gates_admissible"] else 5), doc


# --------------------------------------------------------------------- selftest
def _fixture(root: Path, *, mode: str) -> None:
    """Synthetic campaign. mode 'high': seed-only replicas nearly identical and
    config-only replicas disjoint (precondition met). 'disjoint': everything ~3%
    overlap (the Stage-2c-like structural failure). 'degenerate': everything J=1."""
    rng = random.Random(11)
    genes = [f"ENSG{i:011d}" for i in range(4000)]

    def draw(n: int) -> list[tuple[str, str]]:
        out, seen = [], set()
        while len(out) < n:
            s, t = rng.sample(genes, 2)
            if (s, t) not in seen:
                seen.add((s, t))
                out.append((s, t))
        return out

    for s in slots():
        d = root / "run/results" / str(s["exp_id"])
        d.mkdir(parents=True, exist_ok=True)
        base_cfg = draw(400)
        if mode == "degenerate":
            edges = draw(0) or []
            rng2 = random.Random(1)
            edges = [(f"ENSG{i:011d}", f"ENSG{i + 1:011d}") for i in range(400)]
        elif mode == "high":
            anchor = random.Random(hash(s["dataset"] + s["config"]) & 0xFFFF)
            pool = [(f"E{s['dataset']}{s['config']}_{i}", f"T{i}") for i in range(420)]
            keep = pool[:400] if s["seed"] in ("s0", "s1") else pool[10:410]
            edges = keep
            del anchor
        else:
            edges = base_cfg
        write_edges(d / "output_network.csv", edges)
        (d / "metrics.json").write_text(json.dumps(
            {"quantitative_test_evaluation": {"output_graph": {
                "wasserstein_distance": {"mean": 0.16}}}}, sort_keys=True))
        (d / "arguments.json").write_text(json.dumps(
            {**s["cfg"], "exp_id": str(s["exp_id"])}, sort_keys=True))


def selftest(*, fast: bool = False) -> int:
    import tempfile
    failures: list[str] = []
    records: dict = {}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for name, fn in (("jaccard", control_jaccard_selftest),
                         ("edge_roundtrip", lambda: control_edge_roundtrip(tmp))):
            records[name] = fn()
            if records[name]["verdict"] != "PASS":
                failures.append(f"{name} control FAIL: {records[name]}")
        records["nullcal"] = control_permutation_null(reps=400)
        if records["nullcal"]["verdict"] != "PASS":
            failures.append(f"nullcal FAIL: {records['nullcal']}")
        # grid shape
        sl = slots()
        if len(sl) != len(DATASETS) * len(CONFIGS) * len(SEEDS) + len(DATASETS):
            failures.append(f"grid size wrong: {len(sl)}")
        if len({s["exp_id"] for s in sl}) != len(sl) or len({s["key"] for s in sl}) != len(sl):
            failures.append("exp_ids / keys must be unique")
        # each routing branch must be reachable from a fixture
        for mode, expect in (("high", "PROBE_PRECONDITION_MET"),
                             ("disjoint", "E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT"),
                             ("degenerate", "E40_PROBE_PRECONDITION_UNMET__REPLICATION_DEGENERATE")):
            root = tmp / mode
            _fixture(root, mode=mode)
            g = globals()
            saved = (g["ROOT"], g["RESULTS"], g["OUT_DIR"])
            g["ROOT"], g["RESULTS"], g["OUT_DIR"] = root, root / "run/results", root / "out"
            try:
                rc, doc = run_analysis(write=False)
            finally:
                g["ROOT"], g["RESULTS"], g["OUT_DIR"] = saved
            disp = doc["gates"]["disposition"]
            records[f"fixture_{mode}"] = {
                "rc": rc, "disposition": disp,
                "seed_only_mean_J": doc["analysis"]["seed_only_mean_J"],
                "config_only_mean_J": doc["analysis"]["config_only_mean_J"]}
            if disp != expect:
                failures.append(f"fixture {mode}: expected {expect}, got {disp} "
                                f"(J_seed={doc['analysis']['seed_only_mean_J']})")
        # inhomogeneous envelope -> CANNOT_CHECK with rc=5, never a verdict
        root = tmp / "inhomog"
        _fixture(root, mode="high")
        victim = sorted((root / "run/results").iterdir())[3] / "arguments.json"
        bad = json.loads(victim.read_text())
        bad["model_seed"] = 999999
        victim.write_text(json.dumps(bad, sort_keys=True))
        g = globals()
        saved = (g["ROOT"], g["RESULTS"], g["OUT_DIR"])
        g["ROOT"], g["RESULTS"], g["OUT_DIR"] = root, root / "run/results", root / "out"
        try:
            rc, doc = run_analysis(write=False)
        finally:
            g["ROOT"], g["RESULTS"], g["OUT_DIR"] = saved
        records["fixture_inhomogeneous"] = {"rc": rc, "disposition": doc["gates"]["disposition"]}
        if rc != 5 or doc["gates"]["disposition"] != "CANNOT_CHECK":
            failures.append(f"inhomogeneous envelope must be could-not-check rc=5: rc={rc}")
        # a failed control must void the verdict even with perfect statistics
        stats_ok = {"envelopes_ok": True, "seed_only_mean_J": 0.9,
                    "perm": {"status": "OK", "t_obs": 0.5, "p_one_sided": 0.0}}
        if evaluate_gates(stats_ok, {"jaccard": {"verdict": "FAIL"},
                                     "edge_roundtrip": {"verdict": "PASS"},
                                     "nullcal": {"verdict": "PASS"},
                                     "determinism": {"verdict": "PASS"}})["disposition"] \
                != "CANNOT_CHECK":
            failures.append("a failed control must void the verdict")
        # NO-ALARM: the clean case must NOT fire
        if evaluate_gates(stats_ok, {"jaccard": {"verdict": "PASS"},
                                     "edge_roundtrip": {"verdict": "PASS"},
                                     "nullcal": {"verdict": "PASS"},
                                     "determinism": {"verdict": "PASS"}})["disposition"] \
                != "PROBE_PRECONDITION_MET":
            failures.append("no-alarm case: clean controls + clean stats must route MET")
        # both P1 boundaries are live
        for j, expect in ((0.19, "E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT"),
                          (0.99, "E40_PROBE_PRECONDITION_UNMET__REPLICATION_DEGENERATE"),
                          (0.20, "PROBE_PRECONDITION_MET"), (0.98, "PROBE_PRECONDITION_MET")):
            got = evaluate_gates({**stats_ok, "seed_only_mean_J": j},
                                 {k: {"verdict": "PASS"} for k in
                                  ("jaccard", "edge_roundtrip", "nullcal", "determinism")})
            if got["disposition"] != expect:
                failures.append(f"P1 boundary J={j}: expected {expect}, got {got['disposition']}")
    print(json.dumps({"selftest": "e40_m5p_stage2e", "fast": fast,
                      "records": records, "failures": failures}, indent=1, sort_keys=True))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("plan")
    r = sub.add_parser("run"); r.add_argument("--task", type=int, required=True)
    sub.add_parser("analyze")
    p = sub.add_parser("selftest"); p.add_argument("--fast", action="store_true")
    args = ap.parse_args(argv)
    if args.cmd == "selftest":
        return selftest(fast=args.fast)
    if args.cmd == "plan":
        print(json.dumps(slots(), indent=1, sort_keys=True))
        return 0
    if args.cmd == "run":
        return run_task(args.task)
    rc, _ = run_analysis()
    return rc


if __name__ == "__main__":
    sys.exit(main())
