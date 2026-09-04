#!/usr/bin/env python3
"""ME-F1 R3 -- the controller's development-split loss attributed by organ ablation.

ME-F1 V1 routes CANNOT_CHECK (G0e NO_LAUNDERING_VARIANCE, structural) and nothing here changes
that.  What V1 also recorded, and never attributed, is that at identical resources the bare model
beat the ORION control on the development split (SIMPLE_DIRECT 0.7562 / 0.6625 vs
M_ME_FRONTIER_CONTROL 0.4062 / 0.4500).  M is three organs -- warrant gate, locus diagnosis,
minimum escalation -- and V1 froze an omission ablation for each of them (mef1_arms.py, MODEL_ARMS)
for the protected campaign that must never be dispatched.  This file runs those V1-frozen ablations
on the SAME development split, against the SAME strongest parent on that split, through the SAME
frozen runner (mef1_run.py dev, imported read-only), and attributes M's deficit to ONE organ or to
none.  No arm text is authored here.  Nothing here is a protected-split result.

Exit codes -- "could not check" keeps its own code:
  0  measured / frozen / dispatched
  2  usage error
  4  a registered control FAILED (checked; the verdict is refused)
  5  CANNOT_CHECK (an input is missing or invalid; a run is incomplete)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "me-f1"
if str(V1) not in sys.path:
    sys.path.insert(0, str(V1))

DESIGN = "ME_F1_R3_ORGAN_ABLATION_DESIGN_V1"
DESIGN_JSON = HERE / f"{DESIGN}.json"
RESULTS = HERE / "results"
ROLLUP = RESULTS / "ME_F1_R3_ROLLUP_V1.json"
SCHEMA = "orion.v2.me-f1-r3.rollup.v1"

PARENT = "SIMPLE_DIRECT"
M = "M_ME_FRONTIER_CONTROL"
ABLATIONS = ("M_MINUS_MINIMUM_ESCALATION", "M_MINUS_WARRANT_GATE", "M_MINUS_LOCUS_DIAGNOSIS")
ARMS = (PARENT, M) + ABLATIONS
RUNS = ("r1", "r2")
N_CAMPAIGNS = 8                      # DEV_CAP; the same 8 campaigns as V1 (dev seed is V1's)
MAX_CONCURRENCY = 3
ALPHA = 0.05
SIGNFLIP_N = 4000
SIGNFLIP_SEED = 20260904
#: instrument control: the untouched arms must land inside V1's own observed run-to-run envelope,
#: widened by one envelope width on each side (V1 pre/post: SIMPLE 0.6625-0.7562, M 0.3125-0.4500).
INSTRUMENT_ENVELOPE = {PARENT: (0.5688, 0.8499), M: (0.1750, 0.5875)}
CALIBRATION = V1 / "results" / "ME_F1_CALIBRATION_RECEIPT.json"
CALIBRATION_SHA256 = None  # filled at freeze from the V1 artifact and asserted at run/evaluate


class CannotCheck(Exception):
    pass


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _mean(v: list[float]) -> float:
    return math.fsum(v) / len(v) if v else float("nan")


def signflip_p(diffs: list[float], n: int, seed: int) -> float:
    """One-sided: P(mean >= observed) under random sign flips."""
    rng = random.Random(seed)
    obs = _mean(diffs)
    ge = 0
    for _ in range(n):
        s = _mean([d if rng.random() < 0.5 else -d for d in diffs])
        if s >= obs - 1e-12:
            ge += 1
    return (ge + 1) / (n + 1)


# ---- freeze --------------------------------------------------------------------------------

def freeze() -> dict[str, Any]:
    if not CALIBRATION.exists():
        raise CannotCheck(f"V1 calibration receipt missing: {CALIBRATION}")
    cal = json.loads(CALIBRATION.read_text())
    if cal.get("decision") != "WINDOW_HIT" or not cal.get("selected_level"):
        raise CannotCheck("V1 calibration receipt is not a WINDOW_HIT; the dev geometry would fall back")
    manifest = V1 / "ME_F1_SOURCE_MANIFEST_V1.json"
    fz = {"schema_version": "orion.v2.me-f1-r3.freeze.v2", "design": DESIGN,
          "design_json_sha256": sha256_file(DESIGN_JSON),
          "arms": list(ARMS), "runs": list(RUNS), "n_campaigns": N_CAMPAIGNS, "max_concurrency": MAX_CONCURRENCY,
          "calibration_receipt_sha256": sha256_file(CALIBRATION), "selected_level": cal["selected_level"],
          "v1_source_manifest_sha256": sha256_file(manifest) if manifest.exists() else None,
          # what the run CONSUMES is bound and asserted: each arm text R3 dispatches, by sha256.
          # The whole-file sha and the tree commit are recorded for provenance; a later merge that
          # changes an arm this design never runs (B5, PR #276) must not invalidate the freeze.
          "arm_text_sha256": arm_text_sha256(),
          "v1_arms_py_sha256": sha256_file(V1 / "mef1_arms.py"),
          "v1_tree_commit": _tree_commit(),
          "pre_outcome_correction_r1": {
              "date": "2026-09-04",
              "what": "freeze V1 bound the whole of mef1_arms.py; ORION-V2 #276 (dc27ced) changed the B5 text only, "
                      "invalidating that binding with no R3 outcome in existence; re-frozen against post-#276 main "
                      "with per-arm bindings; design, gates, seed, envelope and routing unchanged",
              "arms_this_design_runs_changed_by_pr276": [],
              "arm_changed_by_pr276_not_run_here": "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION (40e96181... -> 2b9d589c...)",
              "record": "ME_F1_R3_PRE_OUTCOME_CORRECTION_R1.md"},
          "channel": "mef1_channel.call_control (frozen V1: codex-cli 0.129.0-alpha.15, gpt-5.5, medium; served id not exposed)",
          "authority": {"alters_me_f1_terminal": False, "authorizes_protected_dispatch": False,
                        "grants_scientific_truth": False, "grants_field_status": False}}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "ME_F1_R3_FREEZE_V1.json").write_text(json.dumps(fz, indent=2, sort_keys=True) + "\n")
    return fz


def arm_text_sha256() -> dict[str, str]:
    """sha256 of every control text this design dispatches, read from the live V1 table."""
    import mef1_arms as A  # noqa: E402  (frozen V1, read-only)
    return {a: hashlib.sha256(A._ARM_CONTROL[a].encode()).hexdigest() for a in ARMS}


def _tree_commit() -> str | None:
    try:
        cp = subprocess.run(["/usr/bin/git", "rev-parse", "HEAD"], cwd=str(HERE), capture_output=True, text=True, check=False)
        return cp.stdout.strip() or None
    except OSError:
        return None


def _assert_frozen() -> dict[str, Any]:
    fp = RESULTS / "ME_F1_R3_FREEZE_V1.json"
    if not fp.exists():
        raise CannotCheck("not frozen: run `freeze` first")
    fz = json.loads(fp.read_text())
    if fz["design_json_sha256"] != sha256_file(DESIGN_JSON):
        raise CannotCheck("design twin changed after the freeze")
    live = arm_text_sha256()
    drift = sorted(a for a in ARMS if fz.get("arm_text_sha256", {}).get(a) != live[a])
    if drift:
        raise CannotCheck(f"arm text changed after the freeze for {drift} (the freeze binds every arm R3 dispatches)")
    if fz["calibration_receipt_sha256"] != sha256_file(CALIBRATION):
        raise CannotCheck("V1 calibration receipt changed after the freeze")
    return fz


# ---- run -----------------------------------------------------------------------------------

def run(run_id: str) -> int:
    fz = _assert_frozen()
    if run_id not in RUNS:
        raise CannotCheck(f"unknown run id {run_id!r}")
    out = RESULTS / run_id
    if (out / "ME_F1_DEVELOPMENT_RESULTS_V1.json").exists():
        print(f"{run_id}: results already present; not re-dispatching")
        return 0
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CALIBRATION, out / "ME_F1_CALIBRATION_RECEIPT.json")  # geometry L2, sha asserted above
    cmd = [sys.executable, str(V1 / "mef1_run.py"), "dev", "--out", str(out),
           "--campaigns", str(N_CAMPAIGNS), "--arms", ",".join(ARMS), "--max-concurrency", str(fz["max_concurrency"])]
    print("dispatch:", " ".join(cmd))
    cp = subprocess.run(cmd, check=False)
    return cp.returncode


# ---- evaluate ------------------------------------------------------------------------------

def per_campaign_rates(out: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """arm -> campaign_id -> {rate, coverage, unwarranted, inconclusive, local, exact, calls}."""
    import mef1_run as R  # noqa: E402  (frozen V1 runner, read-only)
    from mef1_score import score_campaign  # noqa: E402
    results = json.loads((out / "ME_F1_DEVELOPMENT_RESULTS_V1.json").read_text())
    custody = json.loads((out / "ME_F1_DEVELOPMENT_EXPECTED_CUSTODY_V1.json").read_text())
    cus = {c["campaign_id"]: c for c in custody["campaigns"]}
    table: dict[str, dict[str, dict[str, Any]]] = {}
    for entry in results["campaigns"]:
        if entry["family"] != "F_CRITICAL":
            continue  # the primary is registered over F_CRITICAL only (V1 design S3.3)
        c = cus[entry["campaign_id"]]
        gt = {int(k): v for k, v in c["ground_truth"].items()}
        block_of = {int(k): v for k, v in c["block_of"].items()}
        for arm, obj in entry["arms"].items():
            rec = R._record_from_json(obj)
            cs = score_campaign(rec, gt, entry["family"], entry["n_rungs"], block_of)
            acts = obj.get("actions", [])
            table.setdefault(arm, {})[entry["campaign_id"]] = {
                "rate": cs.rate(), "coverage": cs.coverage(),
                "unwarranted": sum(1 for r in cs.rungs if r.claimed and not r.warranted),
                "claims": sum(1 for r in cs.rungs if r.claimed),
                "inconclusive": sum(1 for a in acts if a["outcome"] == "INCONCLUSIVE"),
                "local_search": sum(1 for a in acts if a["tool"] == "local_search"),
                "exact_solve": sum(1 for a in acts if a["tool"] == "exact_solve"),
                "actions": len(acts), "model_calls": int(obj.get("model_calls", 0)),
                "cannot_check": obj.get("cannot_check", "")}
    return table


def paired(table_runs: list[dict], a: str, b: str) -> dict[str, Any]:
    """Per (run, campaign) paired difference rate(a) - rate(b); one-sided sign-flip p (a > b)."""
    diffs = []
    for t in table_runs:
        for cid in sorted(t.get(a, {})):
            if cid in t.get(b, {}):
                diffs.append(t[a][cid]["rate"] - t[b][cid]["rate"])
    return {"a": a, "b": b, "n": len(diffs), "mean_diff": _mean(diffs),
            "wins_a": sum(1 for d in diffs if d > 0), "wins_b": sum(1 for d in diffs if d < 0),
            "ties": sum(1 for d in diffs if d == 0),
            "p_a_above_b": signflip_p(diffs, SIGNFLIP_N, SIGNFLIP_SEED),
            "p_b_above_a": signflip_p([-d for d in diffs], SIGNFLIP_N, SIGNFLIP_SEED)}


def arm_summary(table_runs: list[dict], arm: str) -> dict[str, Any]:
    cells = [v for t in table_runs for v in t.get(arm, {}).values()]
    n_act = sum(c["actions"] for c in cells) or 1
    return {"n_cells": len(cells), "mean_rate": _mean([c["rate"] for c in cells]),
            "mean_coverage": _mean([c["coverage"] for c in cells]),
            "unwarranted_claims": sum(c["unwarranted"] for c in cells), "claims": sum(c["claims"] for c in cells),
            "inconclusive_rate": sum(c["inconclusive"] for c in cells) / n_act,
            "local_search": sum(c["local_search"] for c in cells), "exact_solve": sum(c["exact_solve"] for c in cells),
            "actions": sum(c["actions"] for c in cells), "model_calls": sum(c["model_calls"] for c in cells),
            "cannot_check_cells": sum(1 for c in cells if c["cannot_check"])}


def controls(table_runs: list[dict]) -> list[dict[str, Any]]:
    out = []
    # C1 every registered cell present and scorable: 5 arms x 8 campaigns x 2 runs, no cannot_check
    expected = len(ARMS) * N_CAMPAIGNS * len(RUNS)
    cells = sum(len(t.get(a, {})) for t in table_runs for a in ARMS)
    cc = sum(1 for t in table_runs for a in ARMS for v in t.get(a, {}).values() if v["cannot_check"])
    out.append({"control": "ALL_CELLS_PRESENT_AND_SCORABLE", "pass": cells == expected and cc == 0,
                "cells": cells, "expected": expected, "cannot_check_cells": cc})
    # C2 budget matched: every cell has the same number of actions and model calls
    acts = sorted({v["actions"] for t in table_runs for a in ARMS for v in t.get(a, {}).values()})
    calls = sorted({v["model_calls"] for t in table_runs for a in ARMS for v in t.get(a, {}).values()})
    out.append({"control": "BUDGET_MATCHED_ACROSS_ARMS", "pass": len(acts) == 1 and len(calls) == 1,
                "distinct_action_counts": acts, "distinct_call_counts": calls})
    # C3 instrument: the two untouched arms reproduce inside V1's envelope
    inst = {}
    ok = True
    for arm, (lo, hi) in INSTRUMENT_ENVELOPE.items():
        m = arm_summary(table_runs, arm)["mean_rate"]
        inst[arm] = {"mean_rate": m, "envelope": [lo, hi], "inside": lo <= m <= hi}
        ok = ok and inst[arm]["inside"]
    out.append({"control": "INSTRUMENT_REPRODUCES_V1_ENVELOPE", "pass": ok, "arms": inst})
    # C4 the world still forecloses laundering (reported; not a pass/fail on the arms, but a
    # measurement that must be populated: zero over zero is not a measurement)
    claims = sum(arm_summary(table_runs, a)["claims"] for a in ARMS)
    out.append({"control": "LAUNDERING_MEASUREMENT_POPULATED", "pass": claims > 0, "total_claims": claims,
                "unwarranted_total": sum(arm_summary(table_runs, a)["unwarranted_claims"] for a in ARMS)})
    return out


def evaluate_gates(ctrls: list[dict[str, Any]], contrasts: dict[str, Any], summaries: dict[str, Any]) -> dict[str, Any]:
    if not all(c["pass"] for c in ctrls):
        return {"A0_CONTROLS_VALID": False, "terminal": "CANNOT_CHECK__CONTROL_FAILED",
                "failed_controls": [c["control"] for c in ctrls if not c["pass"]]}
    esc = contrasts[f"M_MINUS_MINIMUM_ESCALATION_vs_{M}"]
    wg = contrasts[f"M_MINUS_WARRANT_GATE_vs_{M}"]
    ld = contrasts[f"M_MINUS_LOCUS_DIAGNOSIS_vs_{M}"]
    a1 = (esc["mean_diff"] > 0 and esc["p_a_above_b"] <= ALPHA
          and summaries["M_MINUS_MINIMUM_ESCALATION"]["inconclusive_rate"] < summaries[M]["inconclusive_rate"])
    a2 = wg["mean_diff"] > 0 and wg["p_a_above_b"] <= ALPHA
    a3 = ld["mean_diff"] > 0 and ld["p_a_above_b"] <= ALPHA
    if a1 and not a2:
        terminal = "M_HANDICAPPED_BY_ITS_ESCALATION_MANDATE__PROMPT_IMPLICATED_MODEL_EXONERATED"
    elif a2 and not a1:
        terminal = "WARRANT_DISCIPLINE_COSTS_COVERAGE_ON_A_WORLD_THAT_FORECLOSES_LAUNDERING__REGIME_CONDITIONAL"
    elif a1 and a2:
        terminal = "BOTH_MANDATE_AND_DISCIPLINE_IMPLICATED__TWO_ORGANS_EACH_COST_COVERAGE"
    else:
        terminal = "M_DEFICIT_NOT_ATTRIBUTABLE_TO_A_NAMED_ORGAN__ARCHITECTURAL_RESIDUAL"
    best = max(ABLATIONS, key=lambda a: summaries[a]["mean_rate"])
    return {"A0_CONTROLS_VALID": True, "A1_MANDATE_IMPLICATED": a1, "A2_DISCIPLINE_COST": a2,
            "A3_LOCUS_DIAGNOSIS_COST": a3,
            "A4_reported_best_ablation_vs_parent": {"best_ablation": best, **contrasts[f"{best}_vs_{PARENT}"]},
            "terminal": terminal}


def evaluate(out: Path = ROLLUP) -> int:
    fz = _assert_frozen()
    tables = []
    for r in RUNS:
        d = RESULTS / r
        if not (d / "ME_F1_DEVELOPMENT_RESULTS_V1.json").exists():
            raise CannotCheck(f"{r}: no results")
        tables.append(per_campaign_rates(d))
    ctrls = controls(tables)
    contrasts = {}
    for a in ABLATIONS:
        contrasts[f"{a}_vs_{M}"] = paired(tables, a, M)
        contrasts[f"{a}_vs_{PARENT}"] = paired(tables, a, PARENT)
    contrasts[f"{M}_vs_{PARENT}"] = paired(tables, M, PARENT)
    summaries = {a: arm_summary(tables, a) for a in ARMS}
    gates = evaluate_gates(ctrls, contrasts, summaries)
    roll = {"schema_version": SCHEMA, "design": DESIGN, "freeze": fz, "interpreter": sys.version.split()[0],
            "script_sha256": sha256_file(Path(__file__)), "controls": ctrls, "arm_summaries": summaries,
            "contrasts": contrasts, "gates": gates,
            "per_run_per_campaign": {r: t for r, t in zip(RUNS, tables)},
            "authority": {"alters_me_f1_terminal": False, "authorizes_protected_dispatch": False,
                          "grants_scientific_truth": False, "grants_field_status": False}}
    out.write_text(json.dumps(roll, indent=1, sort_keys=True) + "\n")
    for c in ctrls:
        print(f"control {c['control']}: {'PASS' if c['pass'] else 'FAIL'}")
    for a in ARMS:
        s = summaries[a]
        print(f"{a:30s} rate {s['mean_rate']:.4f} cov {s['mean_coverage']:.4f} inconclusive {s['inconclusive_rate']:.3f} "
              f"local {s['local_search']} exact {s['exact_solve']} unwarranted {s['unwarranted_claims']}/{s['claims']}")
    for k, v in contrasts.items():
        print(f"{k:48s} mean {v['mean_diff']:+.4f} ({v['wins_a']}-{v['wins_b']}-{v['ties']}) p {v['p_a_above_b']:.4f}")
    print("terminal", gates["terminal"])
    return 0 if gates.get("A0_CONTROLS_VALID") else 4


# ---- selftest --------------------------------------------------------------------------------

def selftest() -> int:
    fails = []

    def check(name, cond):
        print(f"  {'ok ' if cond else 'FAIL'} {name}")
        if not cond:
            fails.append(name)

    import mef1_arms as A  # noqa: E402
    check("every arm is a V1-registered model arm (no arm text authored here)", all(a in A.MODEL_ARMS for a in ARMS))
    check("the three ablations are V1's omission ablations of M's three organs",
          all(a in A._ARM_CONTROL for a in ABLATIONS) and all("REMOVED" in A._ARM_CONTROL[a] for a in ABLATIONS))
    rng = random.Random(3)
    pos = [abs(rng.gauss(0.1, 0.02)) for _ in range(16)]
    check("sign-flip: all-positive diffs are significant", signflip_p(pos, 2000, 1) <= ALPHA)
    check("sign-flip: negated vector is not", signflip_p([-d for d in pos], 2000, 1) > 0.5)

    def tbl(rates: dict[str, float], inc: dict[str, float], runs=2, n=8):
        out = []
        for r in range(runs):
            t = {}
            for a in ARMS:
                t[a] = {}
                for i in range(n):
                    rate = min(1.0, max(0.0, rates[a] + 0.01 * ((i + r) % 3 - 1)))
                    t[a][f"F_CRITICAL-{i:04d}"] = {"rate": rate, "coverage": rate, "unwarranted": 0, "claims": 10,
                                                    "inconclusive": int(round(56 * inc[a] / 8)), "local_search": 3, "exact_solve": 4,
                                                    "actions": 7, "model_calls": 8, "cannot_check": ""}
            out.append(t)
        return out
    base = {PARENT: 0.72, M: 0.40, "M_MINUS_MINIMUM_ESCALATION": 0.40, "M_MINUS_WARRANT_GATE": 0.40, "M_MINUS_LOCUS_DIAGNOSIS": 0.40}
    inc = {a: 0.45 for a in ARMS}
    inc[PARENT] = 0.05

    def run_gates(rates, incs):
        t = tbl(rates, incs)
        c = controls(t)
        con = {}
        for a in ABLATIONS:
            con[f"{a}_vs_{M}"] = paired(t, a, M)
            con[f"{a}_vs_{PARENT}"] = paired(t, a, PARENT)
        con[f"{M}_vs_{PARENT}"] = paired(t, M, PARENT)
        return c, evaluate_gates(c, con, {a: arm_summary(t, a) for a in ARMS})
    c, g = run_gates(base, inc)
    check("controls pass on a well-formed synthetic table", all(x["pass"] for x in c))
    check("route: no organ moves -> architectural residual", g["terminal"].startswith("M_DEFICIT_NOT_ATTRIBUTABLE"))
    r = dict(base, M_MINUS_MINIMUM_ESCALATION=0.62)
    i = dict(inc, M_MINUS_MINIMUM_ESCALATION=0.10)
    check("route: escalation ablation up with INCONCLUSIVE down -> mandate implicated", run_gates(r, i)[1]["terminal"].startswith("M_HANDICAPPED_BY_ITS_ESCALATION"))
    i2 = dict(inc, M_MINUS_MINIMUM_ESCALATION=0.45)
    check("route: escalation ablation up but INCONCLUSIVE NOT down -> A1 does not fire", not run_gates(r, i2)[1]["A1_MANDATE_IMPLICATED"])
    r2 = dict(base, M_MINUS_WARRANT_GATE=0.62)
    check("route: warrant-gate ablation up -> discipline cost (regime-conditional)", run_gates(r2, inc)[1]["terminal"].startswith("WARRANT_DISCIPLINE_COSTS"))
    r3 = dict(base, M_MINUS_WARRANT_GATE=0.62, M_MINUS_MINIMUM_ESCALATION=0.62)
    check("route: both -> two organs", run_gates(r3, i)[1]["terminal"].startswith("BOTH_MANDATE_AND_DISCIPLINE"))
    bad = dict(base, SIMPLE_DIRECT=0.30)
    cb, gb = run_gates(bad, inc)
    check("instrument control fails when the parent falls outside V1's envelope, and the verdict is refused",
          not all(x["pass"] for x in cb) and gb["terminal"].startswith("CANNOT_CHECK"))
    live = arm_text_sha256()
    check("binding: every dispatched arm text has a sha256 and they are distinct", len(set(live.values())) == len(ARMS))
    fp = RESULTS / "ME_F1_R3_FREEZE_V1.json"
    if fp.exists():
        fz = json.loads(fp.read_text())
        check("binding: the committed freeze names every dispatched arm text, and they match the live table",
              all(fz.get("arm_text_sha256", {}).get(a) == live[a] for a in ARMS))
        check("binding: B5 is not among the arms this freeze binds (the #276 change is out of scope by construction)",
              "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION" not in fz.get("arm_text_sha256", {}))
    if DESIGN_JSON.exists():
        dc = json.loads(DESIGN_JSON.read_text())["constants"]
        check("design twin: constants agree with the script",
              tuple(dc["arms"]) == ARMS and dc["parent"] == PARENT and dc["m"] == M and tuple(dc["ablations"]) == ABLATIONS
              and tuple(dc["runs"]) == RUNS and dc["n_campaigns"] == N_CAMPAIGNS and dc["max_concurrency"] == MAX_CONCURRENCY
              and dc["alpha"] == ALPHA and dc["signflip_n"] == SIGNFLIP_N and dc["signflip_seed"] == SIGNFLIP_SEED
              and {k: tuple(v) for k, v in dc["instrument_envelope"].items()} == INSTRUMENT_ENVELOPE)
    else:
        check("design twin present", False)
    print(f"selftest: {len(fails)} failures")
    return 0 if not fails else 5


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("freeze")
    sub.add_parser("run").add_argument("--run-id", required=True, choices=RUNS)
    sub.add_parser("evaluate").add_argument("--out", type=Path, default=ROLLUP)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "selftest":
            return selftest()
        if a.cmd == "freeze":
            print(json.dumps(freeze(), indent=1))
            return 0
        if a.cmd == "run":
            return run(a.run_id)
        if a.cmd == "evaluate":
            return evaluate(a.out)
    except CannotCheck as exc:
        print(f"CANNOT_CHECK: {exc}", file=sys.stderr)
        return 5
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
