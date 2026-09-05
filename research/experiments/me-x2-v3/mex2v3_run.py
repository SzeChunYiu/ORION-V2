#!/usr/bin/env python3
"""ME-X2 V3 — identification-threshold calibration under the H-EXT-3 interface standard (#308 R1b).

Stages
  selftest    V1/V2 provenance pins; M3(τ = 1.0) ≡ M2 decision-for-decision on a public split (identity,
              no-alarm); M3(τ = 0.0) differs from M2 somewhere the threshold fired (the lever is live);
              a planted analysis mutation (M3 false escalations above B5's) must fail G2.
  calibrate   PUBLIC calibration split (seed below, 10 pairs/stratum = 240): every τ on the grid; the
              frozen selection rule picks τ*; writes ME_X2_V3_CALIBRATION_V1.json.  Never protected evidence.
  dev         PUBLIC development split (48) with the frozen τ* — a rehearsal, never evidence.
  protected   refuses without PROTECTED_RUN_AUTHORIZATION.json (ME-X shape), on design/calibration drift,
              or a seed not hashing to the commitment.  Runs the frozen arm set on 50 pairs/stratum.
  analyze     S5 outcomes, gates, route, lever verdict, over-escalation counts.
V1 and V2 are imported read-only (their sha256 are pinned in the design JSON).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1_DIR = HERE.parent / "me-x2"
V2_DIR = HERE.parent / "me-x2-v2"
for _p in (str(HERE), str(V2_DIR), str(V1_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from mex2_generator import generate_split  # noqa: E402
from mex2_model import STRATA, Instance, canonical_json, instance_to_json  # noqa: E402
from mex2_oracle import Environment  # noqa: E402
from mex2_run import exact_binomial_two_sided, paired_summary, score  # noqa: E402
from mex2v3_arms import B5_ARM, LADDER, M2_ARM, M_V1_ARM, SELECTORS, TAU_GRID, arm_name, arm_specs, make_policy  # noqa: E402

STUDY_ID = "ME-X2-V3"
SCHEMA_RESULTS = "orion.v2.me-x2-v3.threshold-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x2-v3.threshold-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X2_V3_IDENTIFICATION_THRESHOLD_DESIGN_V1.json"
CALIBRATION_JSON = HERE / "ME_X2_V3_CALIBRATION_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
AUTH_USED = HERE / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json"
DEFAULT_SEED_FILE = Path(os.environ.get("MEX2V3_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x2-v3/PROTECTED_SEED_V3.txt")))
CAL_SEED = "ME-X2-V3-CALIBRATION-20260905"
CAL_PAIRS = 10
DEV_SEED = "ME-X2-V3-DEV-20260905"
DEV_PAIRS = 2
PROTECTED_PAIRS = 50
PINS = {
    "me-x2/mex2_arms.py": V1_DIR / "mex2_arms.py", "me-x2/mex2_generator.py": V1_DIR / "mex2_generator.py", "me-x2/mex2_model.py": V1_DIR / "mex2_model.py",
    "me-x2/mex2_oracle.py": V1_DIR / "mex2_oracle.py", "me-x2/mex2_parents.py": V1_DIR / "mex2_parents.py", "me-x2/mex2_run.py": V1_DIR / "mex2_run.py",
    "me-x2-v2/mex2v2_levers.py": V2_DIR / "mex2v2_levers.py", "me-x2-v3/mex2v3_levers.py": HERE / "mex2v3_levers.py", "me-x2-v3/mex2v3_arms.py": HERE / "mex2v3_arms.py",
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pins() -> dict:
    return {k: sha256_file(v) for k, v in PINS.items()}


def _scaled(inst: Instance, mult: float) -> Instance:
    if mult == 1.0:
        return inst
    return Instance(**{**{k: getattr(inst, k) for k in inst.__dataclass_fields__}, "budget": int(round(inst.budget * mult))})


def run_instances(pairs, label: str, taus: tuple[float, ...], only=None, selectors: tuple[str, ...] = SELECTORS) -> tuple[dict, dict]:
    specs = [s for s in arm_specs(taus, selectors) if only is None or s.name in only]
    results = {"schema_version": SCHEMA_RESULTS, "study_id": STUDY_ID, "label": label, "arms": [s.name for s in specs], "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label, "instances": []}
    timing: dict = {}
    for inst, orc in pairs:
        rec = {"instance_id": inst.instance_id, "pair_id": inst.pair_id, "partner_instance_id": inst.partner_instance_id, "stratum": orc["oracle_class"], "variant": inst.variant,
               "template": inst.template, "apparent_class": inst.apparent_class, "budget": inst.budget, "features": inst.features, "public": instance_to_json(inst, include_truth=False), "arms": {}}
        for spec in specs:
            pol = make_policy(spec, inst.seed)
            t0 = time.perf_counter_ns()
            traj = Environment(_scaled(inst, spec.budget_multiplier)).run(pol)
            timing.setdefault(inst.instance_id, {})[spec.name] = time.perf_counter_ns() - t0
            rec["arms"][spec.name] = {"trajectory": traj.as_dict(), "budget_multiplier": spec.budget_multiplier,
                                      "threshold_receipts": getattr(pol, "threshold_receipts", None)}
        results["instances"].append(rec)
        custody["instances"].append({"instance_id": inst.instance_id, "stratum": orc["oracle_class"], "oracle": orc, "instance": instance_to_json(inst)})
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -----------------------------------------------------------------------------------

def arm_summary(sc: dict, arm: str) -> dict:
    rows = sc["_rows"][arm]
    return {"decision_rate": sum(r["decision_correct"] for r in rows) / len(rows), "false_escalation": sum(r["false_escalation"] for r in rows),
            "missed_escalation": sum(r["missed_escalation"] for r in rows), "spec_damage": sum(r["spec_damage"] for r in rows),
            "false_ci": sum(r["false_ci"] for r in rows), "correct_ci": sum(r["correct_ci"] for r in rows), "n": len(rows)}


def grid_arms() -> list[tuple[float, str]]:
    return [(t, sel) for sel in SELECTORS for t in TAU_GRID if not (t == 1.0 and sel != "MINRANK")]


def calibration_rule(table: dict, b5: dict) -> tuple[float, str, str]:
    """Frozen τ*/selector selection on the PUBLIC calibration split: among grid points whose false
    escalations and specification damage do not exceed B5's, the highest decision-correct rate; ties →
    the LARGEST τ, then MINRANK.  If no grid point satisfies the constraint, τ* = 1.0 (≡ M2)."""
    admissible = [(t, sel) for t, sel in grid_arms() if table[arm_name(t, sel)]["false_escalation"] <= b5["false_escalation"] and table[arm_name(t, sel)]["spec_damage"] <= b5["spec_damage"]]
    if not admissible:
        return 1.0, "MINRANK", "no grid point within B5's escalation harm; τ* = 1.0 (≡ M2)"
    best = max(admissible, key=lambda ts: (round(table[arm_name(*ts)]["decision_rate"], 12), ts[0], ts[1] == "MINRANK"))
    return best[0], best[1], f"highest decision rate among grid points with false_escalation <= B5 ({b5['false_escalation']}) and spec_damage <= B5 ({b5['spec_damage']}); ties -> largest τ, then MINRANK"


def threshold_activity(results: dict, arm: str) -> dict:
    fired = committed = 0
    inst_committed = []
    for rec in results["instances"]:
        rs = (rec["arms"].get(arm) or {}).get("threshold_receipts") or []
        if rs:
            fired += 1
        if any(r.get("committed") for r in rs):
            committed += 1
            inst_committed.append(rec["instance_id"])
    return {"instances_threshold_consulted": fired, "instances_committed": committed, "committed_ids": inst_committed}


def gates_v3(sc: dict, results: dict, m3_arm: str, selftest_ok: bool | None, label: str) -> dict:
    g: dict = {}
    rows = sc["_rows"]
    t = {a: arm_summary(sc, a) for a in results["arms"]}
    b5, m2, m3, mv1 = t[B5_ARM], t[M2_ARM], t[m3_arm], t[M_V1_ARM]
    g["G0a_SELFTEST"] = {"pass": selftest_ok}
    g["G0b_ORACLE_SELF_AGREEMENT"] = {"pass": bool(sc["g0b_all_agree"] and sc["variant_invariants_hold"])}
    never = [r["decision_correct"] for r, ident in zip(rows["C_NEVER_INTERVENE"], sc["identifiable"]) if ident]
    g["G0c_NULL_CALIBRATION"] = {"pass": bool(sum(never) == 0 and t["C_RANDOM_POLICY"]["decision_rate"] <= 0.25), "never_intervene_on_identifiable": sum(never), "random": t["C_RANDOM_POLICY"]["decision_rate"]}
    pm = paired_summary([r["decision_correct"] for r in rows[m3_arm]], [r["decision_correct"] for r in rows[B5_ARM]])
    g["G1b_M3_ADVANTAGE_OVER_B5"] = {"pass": bool(pm["diff_x_minus_y"] > 0 and pm["exact_p_two_sided"] < 0.05), **pm}
    g["G1c_B5_ADVANTAGE_OVER_M3"] = {"pass": bool(pm["diff_x_minus_y"] < 0 and pm["exact_p_two_sided"] < 0.05)}
    g["G2_ANTI_ESCALATION_VS_B5"] = {"pass": bool(m3["false_escalation"] <= b5["false_escalation"] and m3["spec_damage"] <= b5["spec_damage"]),
                                     "M3_false_escalation": m3["false_escalation"], "B5_false_escalation": b5["false_escalation"], "M3_spec_damage": m3["spec_damage"], "B5_spec_damage": b5["spec_damage"]}
    g["G2b_OVER_ESCALATION_COUNT"] = {"M3": m3["false_escalation"], "M2": m2["false_escalation"], "M_V1": mv1["false_escalation"], "B5": b5["false_escalation"],
                                      "M3_missed_escalation": m3["missed_escalation"], "M2_missed_escalation": m2["missed_escalation"], "B5_missed_escalation": b5["missed_escalation"], "note": "co-primary, reported in absolute counts; G2 gates on B5's harm"}
    pl = paired_summary([r["decision_correct"] for r in rows[m3_arm]], [r["decision_correct"] for r in rows[M2_ARM]])
    act = threshold_activity(results, m3_arm)
    m3_only = [i for i, (a, b) in enumerate(zip(rows[m3_arm], rows[M2_ARM])) if a["decision_correct"] and not b["decision_correct"]]
    m2_only = [i for i, (a, b) in enumerate(zip(rows[m3_arm], rows[M2_ARM])) if b["decision_correct"] and not a["decision_correct"]]
    ids = [rec["instance_id"] for rec in results["instances"]]
    mech = sum(1 for i in m3_only if ids[i] in set(act["committed_ids"]) and rows[M2_ARM][i].get("false_ci")) / len(m3_only) if m3_only else None
    g["G5_LEVER_ATTRIBUTION"] = {"pass": bool(pl["diff_x_minus_y"] > 0 and pl["exact_p_two_sided"] < 0.05 and m3["spec_damage"] == 0 and (mech is None or mech >= 0.8)),
                                 "M3_minus_M2": pl, "M3_only_correct": len(m3_only), "M2_only_correct": len(m2_only), "mechanism_rate_on_M3_only": mech, "threshold_activity": {k: v for k, v in act.items() if k != "committed_ids"}}
    ladder = [t[a]["decision_rate"] for a in LADDER]
    g["G4_INTERFACE_LADDER"] = {"rates": dict(zip(LADDER, ladder)), "monotone": all(x <= y for x, y in zip(ladder, ladder[1:]))}
    hard = all(bool(g[k]["pass"]) for k in ("G0b_ORACLE_SELF_AGREEMENT", "G0c_NULL_CALIBRATION")) and g["G0a_SELFTEST"]["pass"] is not False
    if not hard:
        route = "LANE_DEFECT"
    elif g["G1b_M3_ADVANTAGE_OVER_B5"]["pass"] and g["G2_ANTI_ESCALATION_VS_B5"]["pass"]:
        route = "M3_ADVANTAGE__THRESHOLD_COMMITMENT_WITHIN_B5_HARM"
    elif g["G1b_M3_ADVANTAGE_OVER_B5"]["pass"]:
        route = "M3_ADVANTAGE_BOUGHT_WITH_ESCALATION_HARM (not a residual: G2 fails)"
    elif g["G1c_B5_ADVANTAGE_OVER_M3"]["pass"]:
        route = "PARENT_SUFFICIENT (B5_DOMINATES)"
    else:
        route = "PARENT_SUFFICIENT (parity within power)"
    lever = "THRESHOLD_RECOVERS_ABSTENTIONS" if g["G5_LEVER_ATTRIBUTION"]["pass"] else ("THRESHOLD_HARMS" if pl["diff_x_minus_y"] < 0 and pl["exact_p_two_sided"] < 0.05 else "THRESHOLD_NULL")
    g["ROUTE"] = {"route": route, "lever_verdict": lever, "M3_arm": m3_arm, "M3_decision_rate": m3["decision_rate"], "M2_decision_rate": m2["decision_rate"], "M_V1_decision_rate": mv1["decision_rate"], "B5_decision_rate": b5["decision_rate"], "label": label}
    g["per_arm"] = t
    return g


def render_md(a: dict) -> str:
    g = a["gates"]; r = g["ROUTE"]
    L = [f"# {STUDY_ID} — {a['label']} analysis", "", f"Route: **{r['route']}** · lever verdict: **{r['lever_verdict']}** · n = {a['n_instances']}", "",
         "| arm | decision | false esc. | missed esc. | spec dmg | false CI | correct CI |", "|---|---:|---:|---:|---:|---:|---:|"]
    for arm, s in sorted(g["per_arm"].items()):
        L.append(f"| {arm} | {s['decision_rate']:.4f} | {s['false_escalation']} | {s['missed_escalation']} | {s['spec_damage']} | {s['false_ci']} | {s['correct_ci']} |")
    L += ["", "| gate | pass | detail |", "|---|---|---|"]
    for k, v in g.items():
        if k in ("ROUTE", "per_arm"):
            continue
        L.append(f"| {k} | {v.get('pass')} | {json.dumps({kk: vv for kk, vv in v.items() if kk != 'pass'}, default=str)[:260]} |")
    L += ["", "Authority: grants nothing. `NO NOVELTY OR BREAKTHROUGH CLAIM`."]
    return "\n".join(L) + "\n"


# ---- stages ------------------------------------------------------------------------------------

def _pairs(split: str, seed: str, per: int):
    return generate_split(split, seed, {s: per for s in STRATA})


def stage_selftest(out: Path) -> int:
    pairs = _pairs("selftest", "ME-X2-V3-SELFTEST", 1)
    res, cus = run_instances(pairs, "SELFTEST", (0.0, 1.0), only=(M2_ARM, arm_name(1.0), arm_name(0.0), B5_ARM, "C_RANDOM_POLICY", "C_NEVER_INTERVENE", M_V1_ARM) + tuple(LADDER), selectors=("MINRANK",))
    res.pop("_timing_wall_ns", None)
    sc = score(res, cus)
    ident = [a["decision_correct"] == b["decision_correct"] and a["false_ci"] == b["false_ci"] and a["false_escalation"] == b["false_escalation"] for a, b in zip(sc["_rows"][arm_name(1.0)], sc["_rows"][M2_ARM])]
    identity_ok = all(ident)
    traj_identity = all(rec["arms"][arm_name(1.0)]["trajectory"]["steps"] == rec["arms"][M2_ARM]["trajectory"]["steps"] for rec in res["instances"])
    act0 = threshold_activity(res, arm_name(0.0))
    lever_live = act0["instances_committed"] >= 1
    g = gates_v3(sc, res, arm_name(0.0), True, "SELFTEST")
    # planted analysis mutation: inflate M3's false escalations above B5's -> G2 must fail and the route must not be the positive terminal
    for r in sc["_rows"][arm_name(0.0)][:3]:
        r["false_escalation"] = True
    sc["_rows"][arm_name(0.0)][0]["spec_damage"] = True
    gp = gates_v3(sc, res, arm_name(0.0), True, "SELFTEST-PLANTED")
    planted_fires = gp["G2_ANTI_ESCALATION_VS_B5"]["pass"] is False and not gp["ROUTE"]["route"].startswith("M3_ADVANTAGE__THRESHOLD")
    ok = bool(identity_ok and traj_identity and lever_live and planted_fires and g["G0b_ORACLE_SELF_AGREEMENT"]["pass"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "ME_X2_V3_SELFTEST_REPORT_V1.json").write_text(canonical_json({"passed": ok, "tau_1_identity_with_M2": identity_ok, "tau_1_trajectory_identity": traj_identity,
                                                                            "tau_0_threshold_activity": act0, "planted_g2_fires": planted_fires, "n": len(pairs), "pins": pins()}))
    print(f"selftest {'PASS' if ok else 'FAIL'}: τ=1 ≡ M2 {identity_ok}/{traj_identity}; τ=0 committed on {act0['instances_committed']}/{len(pairs)}; planted G2 fires {planted_fires}")
    return 0 if ok else 1


def stage_calibrate(out: Path) -> int:
    pairs = _pairs("calibration", CAL_SEED, CAL_PAIRS)
    res, cus = run_instances(pairs, "CALIBRATION", TAU_GRID)
    res.pop("_timing_wall_ns", None)
    sc = score(res, cus)
    table = {a: arm_summary(sc, a) for a in res["arms"]}
    tau_star, sel_star, rule = calibration_rule(table, table[B5_ARM])
    cal = {"schema_version": SCHEMA_RESULTS + ".calibration", "study_id": STUDY_ID, "public_seed": CAL_SEED, "pairs_per_stratum": CAL_PAIRS, "n_instances": len(pairs),
           "grid": [list(x) for x in grid_arms()], "table": table, "tau_star": tau_star, "selector_star": sel_star, "tau_star_arm": arm_name(tau_star, sel_star), "selection_rule": rule,
           "threshold_activity": {arm_name(t, sel): {k: v for k, v in threshold_activity(res, arm_name(t, sel)).items() if k != "committed_ids"} for t, sel in grid_arms()},
           "pins": pins(), "note": "PUBLIC calibration split; never protected evidence"}
    CALIBRATION_JSON.write_text(canonical_json(cal))
    out.mkdir(parents=True, exist_ok=True)
    (out / "ME_X2_V3_CALIBRATION_RESULTS_V1.json").write_text(canonical_json(res))
    print(f"calibration on {len(pairs)}: τ* = {tau_star} selector {sel_star} ({rule})")
    for t, sel in grid_arms():
        s = table[arm_name(t, sel)]
        print(f"  {sel} τ={t:.2f}: decision {s['decision_rate']:.4f} false_esc {s['false_escalation']} missed {s['missed_escalation']} spec {s['spec_damage']} committed {cal['threshold_activity'][arm_name(t, sel)]['instances_committed']}")
    print(f"  M2 {table[M2_ARM]['decision_rate']:.4f} fe {table[M2_ARM]['false_escalation']}; B5 {table[B5_ARM]['decision_rate']:.4f} fe {table[B5_ARM]['false_escalation']}")
    return 0


def frozen_tau() -> tuple[float, str]:
    d = json.loads(DESIGN_JSON.read_text())
    return float(d["tau_star"]), str(d.get("selector_star", "MINRANK"))


def _run_split(label: str, split: str, seed_public: str | None, seed: str, per: int, out: Path) -> int:
    tau, sel = frozen_tau()
    taus = tuple(sorted({tau, 0.0, 1.0}))
    pairs = _pairs(split, seed, per)
    res, cus = run_instances(pairs, label, taus, selectors=tuple(dict.fromkeys(("MINRANK", sel))))
    timing = res.pop("_timing_wall_ns")
    res["split_seed"] = seed_public
    out.mkdir(parents=True, exist_ok=True)
    rp = out / f"ME_X2_V3_{label}_RESULTS_V1.json"; cp = out / f"ME_X2_V3_{label}_EXPECTED_CUSTODY_V1.json"
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus))
    (out / f"ME_X2_V3_{label}_TIMING_V1.json").write_text(canonical_json({"wall_ns": timing}))
    print(f"{label}: {len(pairs)} instances; results sha256 {sha256_file(rp)[:16]}…")
    return stage_analyze(rp, cp, out, label)


def stage_dev(out: Path) -> int:
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, DEV_SEED, DEV_PAIRS, out)


def stage_protected(out: Path, seed_file: Path, per: int) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized", file=sys.stderr); return 3
    auth = json.loads(AUTH_FILE.read_text())
    if auth.get("human_written") is not True or len(str(auth.get("human_written_token", ""))) < 16:
        print("REFUSED: authorization requires human_written=true and a token >= 16 chars", file=sys.stderr); return 3
    if auth.get("acknowledged_design_sha256") != sha256_file(DESIGN_JSON):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr); return 3
    d = json.loads(DESIGN_JSON.read_text())
    if d["substrate_pins_sha256"] != pins() or d["calibration_sha256"] != sha256_file(CALIBRATION_JSON):
        print("REFUSED: substrate or calibration drift since the freeze", file=sys.stderr); return 5
    if not seed_file.exists():
        print(f"REFUSED: custody seed absent ({seed_file})", file=sys.stderr); return 4
    seed = seed_file.read_bytes().strip()
    if hashlib.sha256(seed).hexdigest() != d["seed_commitment"]["protected_seed_sha256"]:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr); return 4
    rc = _run_split("PROTECTED", "protected", None, seed.decode(), per, out)
    auth["consumed"] = True; auth["revealed_protected_seed"] = seed.decode()
    AUTH_USED.write_text(canonical_json(auth)); AUTH_FILE.unlink()
    return rc


def stage_analyze(rp: Path, cp: Path, out: Path, label: str | None = None) -> int:
    res = json.loads(rp.read_text()); cus = json.loads(cp.read_text())
    label = label or res["label"]
    sp = out / "ME_X2_V3_SELFTEST_REPORT_V1.json"
    selftest_ok = bool(json.loads(sp.read_text()).get("passed")) if sp.exists() else None
    sc = score(res, cus)
    m3_arm = arm_name(*frozen_tau()) if DESIGN_JSON.exists() else arm_name(0.0)
    g = gates_v3(sc, res, m3_arm, selftest_ok, label)
    a = {"schema_version": SCHEMA_ANALYSIS, "study_id": STUDY_ID, "label": label, "n_instances": len(res["instances"]), "results_sha256": sha256_file(rp), "custody_sha256": sha256_file(cp), "gates": g}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"ME_X2_V3_{label}_ANALYSIS_V1.json").write_text(canonical_json(a))
    (out / f"ME_X2_V3_{label}_ANALYSIS_V1.md").write_text(render_md(a))
    r = g["ROUTE"]
    print(f"{label} route: {r['route']}; lever: {r['lever_verdict']}; M3 {r['M3_decision_rate']:.4f} M2 {r['M2_decision_rate']:.4f} B5 {r['B5_decision_rate']:.4f}; false esc M3/M2/B5 = {g['G2b_OVER_ESCALATION_COUNT']['M3']}/{g['G2b_OVER_ESCALATION_COUNT']['M2']}/{g['G2b_OVER_ESCALATION_COUNT']['B5']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "calibrate", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--pairs-per-stratum", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "calibrate":
        return stage_calibrate(a.out)
    if a.stage == "dev":
        return stage_dev(a.out)
    if a.stage == "protected":
        return stage_protected(a.out, a.seed_file, a.pairs_per_stratum or PROTECTED_PAIRS)
    return stage_analyze(a.results, a.custody, a.out)


if __name__ == "__main__":
    sys.exit(main())
