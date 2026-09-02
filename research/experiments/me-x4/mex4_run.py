#!/usr/bin/env python3
"""ME-X4 exact selective-reopening study runner (frozen with design V1).

Stages
  selftest   parent fidelity (native known-answer tests), G0a hand-authored
             known-answer fixtures, H-EXT-3 separation pair, G0b oracle
             self-agreement on a small generated set, null calibration.
  dev        DEVELOPMENT split (public seed, <= 40 instances). Results are
             labelled DEVELOPMENT and are never protected evidence.
  protected  PROTECTED split. Refuses to run unless
             PROTECTED_RUN_AUTHORIZATION.json (human-written token) is present
             next to this script AND the custody seed file's sha256 equals the
             commitment frozen in the design JSON.
  analyze    Score a results file against its custody expected-sets file:
             §5 outcomes, G0-G4 gates, pre-registered route.

Design: ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.{md,json}
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from mex4_arms import MODULES, ArmRunner, ArmView, arm_specs  # noqa: E402
from mex4_generator import known_answer_fixtures, generate_split, separation_pair  # noqa: E402
from mex4_model import STRATA, Instance, apply_event, canonical_json, instance_from_json, instance_to_json  # noqa: E402
from mex4_oracle import expected_trajectory  # noqa: E402
from mex4_parents import fidelity_selftests  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x4.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x4.exact-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X4-DEV-20260902"
DEV_PER_STRATUM = 3          # 36 instances <= 40
PROTECTED_PER_STRATUM = 100  # 1200 instances
DEFAULT_SEED_FILE = Path(os.environ.get("MEX4_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x4/PROTECTED_SEED_V1.txt")))

M_ARM = "M_ME_SELECTIVE_REOPENING"
B5_ARM = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
LADDER = ["B5_R1_VERDICT_ONLY", "B5_R2_PROV", "B5_R3_PROV+DEP", "B5_R4_PROV+DEP+TRANS+EVAL", B5_ARM]
G2_STRATA = ("NO_REOPENING_NEEDED", "NEW_INDEPENDENT_SUPPORT")
ABLATION_FOR_STRATUM = {
    "DEPENDENCE_DISCOVERED": "M_MINUS_DEPENDENCE_ANCESTRY",
    "TRANSPORT_RELATION_INVALIDATED": "M_MINUS_TYPED_TRANSPORT",
    "EVALUATOR_BLIND_OR_REPLACED": "M_MINUS_EVALUATOR_CONTRACT",
}
DEFAULT_ABLATION = "M_MINUS_SUPPORT_FAMILIES"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ---- running arms over a split -------------------------------------------------

def run_instances(pairs: list[tuple[Instance, list]], label: str, split_seed_public: str | None) -> tuple[dict, dict]:
    specs = arm_specs()
    results = {"schema_version": SCHEMA_RESULTS, "label": label, "split_seed": split_seed_public, "arms": [s.name for s in specs], "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label, "instances": []}
    timing: dict[str, dict[str, int]] = {}  # wall-clock kept out of the deterministic results file
    for inst, traj in pairs:
        acc = inst.world_v0.accepted_ids()
        rec = {"instance_id": inst.instance_id, "stratum": inst.stratum, "seed": inst.seed, "n_versions": len(inst.events), "accepted": list(acc), "n_claims": len(inst.world_v0.claims), "n_families": len(inst.world_v0.families), "n_evidence": len(inst.world_v0.evidence), "features": inst.features, "arms": {}}
        for spec in specs:
            runner = ArmRunner(spec, inst.seed)
            w = inst.world_v0; hist = []; versions = []; ops = 0; mops = 0; wall = 0
            for ev in inst.events:
                w = apply_event(w, ev); hist.append(ev)
                out, cost = runner.run_version(ArmView(inst.world_v0, w, list(hist), acc))
                versions.append({c: out[c] for c in acc})
                ops += cost.get("ops", 0); mops += cost.get("module_ops", 0); wall += cost.get("wall_ns", 0)
            rec["arms"][spec.name] = {"versions": versions, "cost": {"engine_ops": ops, "module_ops": mops}}
            timing.setdefault(inst.instance_id, {})[spec.name] = wall
        results["instances"].append(rec)
        custody["instances"].append({"instance_id": inst.instance_id, "stratum": inst.stratum, "expected": [t.as_dict() for t in traj], "instance": instance_to_json(inst)})
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -----------------------------------------------------------------------

def _sets(disp: dict[str, str]) -> tuple[set[str], set[str], set[str]]:
    return ({c for c, d in disp.items() if d == "REOPENED"}, {c for c, d in disp.items() if d == "PRESERVED"}, {c for c, d in disp.items() if d == "UNRESOLVED"})


def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def paired_summary(x: list[bool], y: list[bool]) -> dict:
    """x, y: per-instance exact-match indicators for two arms (same order)."""
    n = len(x)
    b = sum(1 for a, bb in zip(x, y) if a and not bb)   # x-only correct
    c = sum(1 for a, bb in zip(x, y) if bb and not a)   # y-only correct
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {"n": n, "x_only": b, "y_only": c, "discordant": b + c, "diff_x_minus_y": diff, "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se], "exact_p_two_sided": exact_binomial_two_sided(b, c)}


def score(results: dict, custody: dict, *, shuffle_seed: int = 20260902, timing: dict | None = None) -> dict:
    exp_by_id = {r["instance_id"]: r for r in custody["instances"]}
    timing = timing if timing is not None else results.get("_timing_wall_ns", {})
    arms = results["arms"]
    per_arm: dict[str, dict] = {a: {"instance_exact": [], "final_exact": [], "over_reopen": 0, "under_reopen": 0, "invalid_preservation": 0, "false_unresolved": 0, "missed_unresolved": 0, "recovery_ok": 0, "recovery_n": 0, "engine_ops": 0, "module_ops": 0, "wall_ns": 0, "per_stratum": {s: {"n": 0, "exact": 0, "over": 0, "under": 0, "invalid_pres": 0, "false_unres": 0, "missed_unres": 0} for s in STRATA}} for a in arms}
    order: list[str] = []
    strata_of: list[str] = []
    oracle_nontrivial: list[bool] = []
    oracle_requires_change: list[bool] = []   # some version has reopened or unresolved non-empty
    oracle_has_mixed: list[bool] = []         # some version has preserved AND (reopened or unresolved) non-empty
    shuffled_exact_M: list[bool] = []
    rng = random.Random(shuffle_seed)
    g0b_all_agree = True
    for rec in results["instances"]:
        iid = rec["instance_id"]; st = rec["stratum"]; order.append(iid); strata_of.append(st)
        exp = exp_by_id[iid]["expected"]
        g0b_all_agree &= all(t["exhaustive_agrees"] for t in exp)
        acc = rec["accepted"]
        final_exp = exp[-1]
        oracle_requires_change.append(any(t["reopened"] or t["unresolved"] for t in exp))
        oracle_has_mixed.append(any(t["preserved"] and (t["reopened"] or t["unresolved"]) for t in exp))
        oracle_nontrivial.append(len({d for k in ("reopened", "preserved", "unresolved") for d in ([k] if final_exp[k] else [])}) >= 2)
        # recovery targets: commitments reopened at some earlier version and preserved at the final version
        recovery_targets = {c for t in exp[:-1] for c in t["reopened"] if c in final_exp["preserved"]}
        for a in arms:
            ar = rec["arms"][a]; pa = per_arm[a]; ps = pa["per_stratum"][st]
            ok_all = True
            for vi, (disp, t) in enumerate(zip(ar["versions"], exp)):
                r, p, u = _sets(disp)
                ok = (r == set(t["reopened"]) and p == set(t["preserved"]) and u == set(t["unresolved"]))
                ok_all &= ok
                over = len(r & set(t["preserved"])); under = len(set(t["reopened"]) - r); inv = len(p - set(t["preserved"]))
                fu = len(u - set(t["unresolved"])); mu = len(set(t["unresolved"]) - u)
                pa["over_reopen"] += over; pa["under_reopen"] += under; pa["invalid_preservation"] += inv; pa["false_unresolved"] += fu; pa["missed_unresolved"] += mu
                ps["over"] += over; ps["under"] += under; ps["invalid_pres"] += inv; ps["false_unres"] += fu; ps["missed_unres"] += mu
            fr, fp, fu_ = _sets(ar["versions"][-1])
            pa["final_exact"].append(fr == set(final_exp["reopened"]) and fp == set(final_exp["preserved"]) and fu_ == set(final_exp["unresolved"]))
            pa["instance_exact"].append(ok_all); ps["n"] += 1; ps["exact"] += int(ok_all)
            for c in recovery_targets:
                pa["recovery_n"] += 1; pa["recovery_ok"] += int(ar["versions"][-1][c] == "PRESERVED")
            pa["engine_ops"] += ar["cost"]["engine_ops"]; pa["module_ops"] += ar["cost"]["module_ops"]; pa["wall_ns"] += timing.get(iid, {}).get(a, 0)
        # assigned-label null for M: shuffle the oracle's final dispositions among commitments
        if oracle_nontrivial[-1] and M_ARM in arms:
            labels = {c: ("REOPENED" if c in final_exp["reopened"] else "PRESERVED" if c in final_exp["preserved"] else "UNRESOLVED") for c in acc}
            vals = list(labels.values()); rng.shuffle(vals); shuffled = dict(zip(acc, vals))
            if shuffled == labels:
                continue
            m_final = rec["arms"][M_ARM]["versions"][-1]
            shuffled_exact_M.append(all(m_final[c] == shuffled[c] for c in acc))
    summary = {}
    for a, pa in per_arm.items():
        n = len(pa["instance_exact"])
        summary[a] = {
            "n": n,
            "instance_exact_rate": sum(pa["instance_exact"]) / n if n else None,
            "final_exact_rate": sum(pa["final_exact"]) / n if n else None,
            "over_reopen": pa["over_reopen"], "under_reopen": pa["under_reopen"], "invalid_preservation": pa["invalid_preservation"],
            "false_unresolved": pa["false_unresolved"], "missed_unresolved": pa["missed_unresolved"],
            "recovery_rate": (pa["recovery_ok"] / pa["recovery_n"]) if pa["recovery_n"] else None, "recovery_n": pa["recovery_n"],
            "engine_ops": pa["engine_ops"], "module_ops": pa["module_ops"], "wall_ms": pa["wall_ns"] / 1e6,
            "per_stratum": {s: dict(v, exact_rate=(v["exact"] / v["n"] if v["n"] else None)) for s, v in pa["per_stratum"].items()},
        }
    return {"per_arm": summary, "_raw": per_arm, "order": order, "strata": strata_of, "g0b_all_agree": g0b_all_agree, "shuffled_exact_M": shuffled_exact_M, "oracle_requires_change": oracle_requires_change, "oracle_has_mixed": oracle_has_mixed}


def gates(sc: dict, results: dict, selftest_ok: bool | None) -> dict:
    raw = sc["_raw"]; strata = sc["strata"]; arms = results["arms"]
    n = len(sc["order"])
    g: dict = {}
    # G0 generator/oracle validity
    shuffled = sc["shuffled_exact_M"]
    shuffle_rate = (sum(shuffled) / len(shuffled)) if shuffled else 0.0
    never = raw["C_NEVER_REOPEN"]["instance_exact"]; reset = raw["M_GLOBAL_RESET_CONTROL"]["instance_exact"]; rnd = raw["C_RANDOM_DISPOSITION"]["instance_exact"]
    never_where_change_required = [x for x, req in zip(never, sc["oracle_requires_change"]) if req]
    reset_where_mixed = [x for x, mixed in zip(reset, sc["oracle_has_mixed"]) if mixed]
    g["G0a_KNOWN_ANSWER"] = {"pass": selftest_ok, "rule": "12 hand-authored fixtures + separation pair reproduced by the oracle (selftest)"}
    g["G0b_ORACLE_SELF_AGREEMENT"] = {"pass": bool(sc["g0b_all_agree"]), "rule": "Kleene == exhaustive enumeration on every version of every instance"}
    g["G0c_NULL_CALIBRATION"] = {
        "pass": bool(sum(never_where_change_required) == 0 and sum(reset_where_mixed) == 0 and shuffle_rate <= 0.10 and (sum(rnd) / n if n else 0) <= 0.10),
        "never_reopen_exact_where_oracle_requires_change": sum(never_where_change_required), "n_requires_change": len(never_where_change_required),
        "global_reset_exact_where_oracle_mixed": sum(reset_where_mixed), "n_mixed": len(reset_where_mixed),
        "random_exact_rate": (sum(rnd) / n) if n else None,
        "assigned_label_shuffle_exact_rate_M": shuffle_rate, "shuffle_n": len(shuffled),
        "rule": "NEVER_REOPEN exact=0 on instances whose oracle reopens/censors something; GLOBAL_RESET exact=0 on instances whose oracle mixes preserved with reopened/unresolved; RANDOM exact <= 10%; M vs within-instance shuffled oracle labels exact <= 10%",
    }
    g0 = bool(g["G0a_KNOWN_ANSWER"]["pass"]) and g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"]
    # G1 M vs B5
    m = raw[M_ARM]["instance_exact"]; b5 = raw[B5_ARM]["instance_exact"]
    ps = paired_summary(m, b5)
    identical = [all(vm == vb for vm, vb in zip(rec["arms"][M_ARM]["versions"], rec["arms"][B5_ARM]["versions"])) for rec in results["instances"]]
    per_stratum_disc = {}
    for s in STRATA:
        idx = [i for i, st in enumerate(strata) if st == s]
        if idx:
            per_stratum_disc[s] = {"n": len(idx), "decision_discordant": sum(1 for i in idx if not identical[i]), "M_only_exact": sum(1 for i in idx if m[i] and not b5[i]), "B5_only_exact": sum(1 for i in idx if b5[i] and not m[i])}
    disc_rate = 1 - sum(identical) / n if n else 0.0
    g1a = disc_rate <= 0.005 and all(v["decision_discordant"] / v["n"] <= 0.05 for v in per_stratum_disc.values())
    g1b = ps["diff_x_minus_y"] > 0 and ps["exact_p_two_sided"] <= 0.05 and any(v["M_only_exact"] >= 5 for v in per_stratum_disc.values())
    g["G1a_B5_REPRODUCES_M"] = {"pass": bool(g1a), "decision_identity_rate": 1 - disc_rate, "per_stratum": per_stratum_disc, "rule": "M and B5 decisions identical on >= 99.5% of instances and no stratum > 5% discordant"}
    g["G1b_M_ADVANTAGE"] = {"pass": bool(g1b), "paired": ps, "rule": "instance-exact diff (M - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M-only-exact instances"}
    # G2 anti-conservatism
    m_over = sum(raw[M_ARM]["per_stratum"][s]["over"] for s in G2_STRATA); b_over = sum(raw[B5_ARM]["per_stratum"][s]["over"] for s in G2_STRATA)
    g["G2_ANTI_CONSERVATISM"] = {"pass": bool(m_over <= b_over), "M_over_reopen": m_over, "B5_over_reopen": b_over, "strata": list(G2_STRATA), "rule": "on NO_REOPENING_NEEDED and NEW_INDEPENDENT_SUPPORT, M over-reopened commitments <= B5's"}
    # G3 mechanism (only if G1b)
    g3: dict = {"pass": None, "applicable": bool(g1b), "checks": {}}
    if g1b:
        ok = True
        for s, v in per_stratum_disc.items():
            if v["M_only_exact"] >= 5:
                abl = ABLATION_FOR_STRATUM.get(s, DEFAULT_ABLATION)
                abl_rate = sc["per_arm"][abl]["per_stratum"][s]["exact_rate"] or 0.0
                b5_rate = sc["per_arm"][B5_ARM]["per_stratum"][s]["exact_rate"] or 0.0
                vanish = abl_rate <= b5_rate
                g3["checks"][s] = {"ablation": abl, "ablation_exact_rate": abl_rate, "B5_exact_rate": b5_rate, "advantage_vanishes": vanish}
                ok &= vanish
        g3["pass"] = ok
    g3["rule"] = "each stratum with a claimed M advantage: the matching omission ablation's exact rate <= B5's on that stratum"
    g["G3_MECHANISM"] = g3
    # G4 interface ladder (H-EXT-3)
    rung_rates = [sc["per_arm"][r]["instance_exact_rate"] for r in LADDER]
    steps = []
    monotone = True
    for k in range(4):
        p = paired_summary(raw[LADDER[k + 1]]["instance_exact"], raw[LADDER[k]]["instance_exact"])
        violated = p["diff_x_minus_y"] < 0 and p["exact_p_two_sided"] <= 0.05
        monotone &= not violated
        steps.append({"from": LADDER[k], "to": LADDER[k + 1], "paired": p, "violation": violated})
    gap = paired_summary(m, b5)
    gap_null = not g1b
    g["G4_INTERFACE_LADDER"] = {"pass": bool(monotone), "rung_exact_rates": dict(zip(LADDER, rung_rates)), "steps": steps, "rung5_gap": gap, "rung5_gap_null": gap_null,
                                "terminal": ("RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL" if (monotone and gap_null) else "CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE" if (monotone and not gap_null) else "LADDER_NON_MONOTONE"),
                                "rule": "no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = G1 paired test"}
    # cost
    m_ops = sc["per_arm"][M_ARM]["engine_ops"] + sc["per_arm"][M_ARM]["module_ops"]; b_ops = sc["per_arm"][B5_ARM]["engine_ops"] + sc["per_arm"][B5_ARM]["module_ops"]
    m_ms = sc["per_arm"][M_ARM]["wall_ms"]; b_ms = sc["per_arm"][B5_ARM]["wall_ms"]
    g["COST"] = {"M_ops": m_ops, "B5_ops": b_ops, "M_wall_ms": m_ms, "B5_wall_ms": b_ms, "ratio_B5_over_M_wall": (b_ms / m_ms) if m_ms else None,
                 "flag": ("COST_ADVANTAGE_M" if m_ms and b_ms > 2 * m_ms else "COST_ADVANTAGE_B5" if b_ms and m_ms > 2 * b_ms else "COST_PARITY_WITHIN_2X"),
                 "rule": "wall-clock flag at 2x (only commensurable scale; engine op counts are engine-native and reported only); no route by itself (a cost-only claim needs the separate scaling cell)"}
    # route
    if not g0:
        route = "CANNOT_CHECK"; reason = "G0 generator/oracle validity failed: lane defect, repair and re-freeze"
    elif g1a:
        route = "PARENT_SUFFICIENT"; reason = "B5 reproduces M's reopening/preservation/unresolved decisions"
    elif g1b:
        if not g["G2_ANTI_CONSERVATISM"]["pass"]:
            route = "M_OVER_REOPENS"; reason = "M advantage coexists with over-reopening on conservative strata"
        elif g3["pass"]:
            route = "ME_X4_RESIDUAL_CANDIDATE"; reason = "M advantage, anti-conservative, mechanism attributed by omission ablation"
        else:
            route = "CANNOT_CHECK"; reason = "M advantage not attributable to a named mechanism (G3 failed)"
    else:
        route = "PARENT_SUFFICIENT"; reason = "no M advantage over B5 (B5 not worse, or discordance without significance)"
    g["ROUTE"] = {"route": route, "reason": reason, "ladder_terminal": g["G4_INTERFACE_LADDER"]["terminal"], "cost_flag": g["COST"]["flag"]}
    return g


def render_md(analysis: dict) -> str:
    L = []
    L.append(f"# ME-X4 analysis — {analysis['label']}\n")
    if analysis["label"] == "DEVELOPMENT":
        L.append("**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**\n")
    L.append(f"Results sha256 `{analysis['results_sha256']}`; custody sha256 `{analysis['custody_sha256']}`; instances {analysis['n_instances']}.\n")
    L.append("## Per-arm outcomes (§5)\n")
    L.append("| arm | instance exact | final exact | over | under | invalid pres. | false unres. | missed unres. | recovery | engine ops | module ops | wall ms |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for a, s in analysis["score"]["per_arm"].items():
        rec = "n/a" if s["recovery_rate"] is None else f"{s['recovery_rate']:.3f} (n={s['recovery_n']})"
        L.append(f"| {a} | {s['instance_exact_rate']:.3f} | {s['final_exact_rate']:.3f} | {s['over_reopen']} | {s['under_reopen']} | {s['invalid_preservation']} | {s['false_unresolved']} | {s['missed_unresolved']} | {rec} | {s['engine_ops']} | {s['module_ops']} | {s['wall_ms']:.1f} |")
    L.append("\n## Per-stratum instance-exact rate\n")
    arms = list(analysis["score"]["per_arm"])
    L.append("| stratum | " + " | ".join(arms) + " |")
    L.append("|---|" + "---|" * len(arms))
    for st in STRATA:
        row = []
        for a in arms:
            v = analysis["score"]["per_arm"][a]["per_stratum"][st]
            row.append("–" if v["exact_rate"] is None else f"{v['exact_rate']:.2f}")
        L.append(f"| {st} | " + " | ".join(row) + " |")
    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        if k in ("ROUTE",):
            continue
        L.append(f"- **{k}**: pass={v.get('pass')} — {v.get('rule', '')}")
    r = analysis["gates"]["ROUTE"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}. Ladder terminal: `{r['ladder_terminal']}`. Cost: `{r['cost_flag']}`.\n")
    return "\n".join(L)


# ---- stages ---------------------------------------------------------------------------

def stage_selftest(out_dir: Path) -> int:
    report: dict = {"schema_version": SCHEMA_ANALYSIS + ".selftest", "parent_fidelity": fidelity_selftests(), "known_answer": [], "separation": {}, "oracle_agreement": None, "null_calibration": None}
    ok = all(r["passed"] for r in report["parent_fidelity"])
    # G0a: hand-authored fixtures
    for f in known_answer_fixtures():
        w = f["world"]; acc = w.accepted_ids(); traj = expected_trajectory(w, f["events"], acc)
        got = traj[-1].as_dict(); exp = f["expected"]
        passed = all(got[k] == exp[k] for k in ("reopened", "preserved", "unresolved")) and all(t.exhaustive_agrees for t in traj)
        if "expected_trajectory" in f:
            passed &= all(all(t.as_dict()[k] == e[k] for k in ("reopened", "preserved", "unresolved")) for t, e in zip(traj, f["expected_trajectory"]))
        report["known_answer"].append({"name": f["name"], "passed": passed, "expected": exp, "oracle": {k: got[k] for k in ("reopened", "preserved", "unresolved")}})
        ok &= passed
    # H-EXT-3 separation pair: verdict-only federation must fail on at least one of P,Q; rung 5 and M must be exact on both
    sep = separation_pair()
    specs = {s.name: s for s in arm_specs()}
    sep_out = {}
    for case in sep:
        w0 = case["world"]; acc = w0.accepted_ids(); traj = expected_trajectory(w0, case["events"], acc)
        exp = traj[-1].as_dict()
        oracle_ok = all(exp[k] == case["expected"][k] for k in ("reopened", "preserved", "unresolved"))
        per_arm = {}
        for name in (LADDER[0], B5_ARM, M_ARM):
            r = ArmRunner(specs[name], 1); w = w0; hist = []
            for ev in case["events"]:
                w = apply_event(w, ev); hist.append(ev)
                out, _ = r.run_version(ArmView(w0, w, list(hist), acc))
            per_arm[name] = out
        sep_out[case["name"]] = {"oracle_matches_hand_answer": oracle_ok, "expected": case["expected"], "arms": per_arm}
        ok &= oracle_ok
    v1 = [sep_out[c]["arms"][LADDER[0]] for c in ("SEP-P", "SEP-Q")]
    verdict_identical_outputs = v1[0] == v1[1]
    verdict_fails_one = any(sep_out[c]["arms"][LADDER[0]]["c"] != ("REOPENED" if c == "SEP-P" else "PRESERVED") for c in ("SEP-P", "SEP-Q"))
    structure_exact = all(sep_out[c]["arms"][n]["c"] == ("REOPENED" if c == "SEP-P" else "PRESERVED") for c in ("SEP-P", "SEP-Q") for n in (B5_ARM, M_ARM))
    report["separation"] = {"cases": sep_out, "verdict_only_outputs_identical_on_P_and_Q": verdict_identical_outputs, "verdict_only_fails_at_least_one": verdict_fails_one, "structure_exchange_exact_on_both": structure_exact, "passed": bool(verdict_identical_outputs and verdict_fails_one and structure_exact)}
    ok &= report["separation"]["passed"]
    # G0b/G0c on a small generated set (public selftest seed)
    pairs = generate_split("selftest", "ME-X4-SELFTEST", {s: 1 for s in STRATA})
    res, cus = run_instances(pairs, "SELFTEST", "ME-X4-SELFTEST")
    sc = score(res, cus)
    report["oracle_agreement"] = sc["g0b_all_agree"]; ok &= sc["g0b_all_agree"]
    gt = gates(sc, res, True)
    report["null_calibration"] = gt["G0c_NULL_CALIBRATION"]; ok &= gt["G0c_NULL_CALIBRATION"]["pass"]
    report["selftest_arm_exact"] = {a: v["instance_exact_rate"] for a, v in sc["per_arm"].items()}
    report["passed"] = bool(ok)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X4_SELFTEST_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    print(f"selftest {'PASS' if ok else 'FAIL'}: parent tests {sum(r['passed'] for r in report['parent_fidelity'])}/{len(report['parent_fidelity'])}, known-answer {sum(k['passed'] for k in report['known_answer'])}/{len(report['known_answer'])}, separation {report['separation']['passed']}, oracle agreement {sc['g0b_all_agree']}, null calibration {gt['G0c_NULL_CALIBRATION']['pass']}")
    return 0 if ok else 1


def _run_split(label: str, split: str, split_seed: str, per_stratum: int, out_dir: Path, public_seed: str | None) -> int:
    pairs = generate_split(split, split_seed, {s: per_stratum for s in STRATA})
    res, cus = run_instances(pairs, label, public_seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X4_{label}_RESULTS_V1.json"; cp = out_dir / f"ME_X4_{label}_EXPECTED_CUSTODY_V1.json"; tp = out_dir / f"ME_X4_{label}_TIMING_V1.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus)); tp.write_text(canonical_json({"schema_version": SCHEMA_RESULTS + ".timing", "label": label, "wall_ns": timing, "note": "wall-clock is machine-dependent and is kept out of the deterministic results file"}))
    print(f"{label}: {len(pairs)} instances, results {rp} sha256 {sha256_file(rp)[:16]}…, custody {cp} sha256 {sha256_file(cp)[:16]}…")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_stratum: int) -> int:
    if per_stratum * len(STRATA) > 40:
        print("development split is capped at 40 instances", file=sys.stderr); return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_stratum, out_dir, DEV_SEED)


def stage_protected(out_dir: Path, per_stratum: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized", file=sys.stderr); return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization file unreadable: {exc}", file=sys.stderr); return 3
    token = str(auth.get("human_written_token", "")).strip()
    if not token or auth.get("human_written") is not True or len(token) < 16:
        print("REFUSED: authorization requires human_written=true and a human_written_token (>= 16 chars)", file=sys.stderr); return 3
    design_sha = sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else ""
    if auth.get("acknowledged_design_sha256") != design_sha:
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr); return 3
    if not seed_file.exists():
        print(f"REFUSED: custody seed file absent ({seed_file})", file=sys.stderr); return 4
    seed = seed_file.read_bytes().strip()
    commitment = json.loads(DESIGN_JSON.read_text())["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed).hexdigest() != commitment:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr); return 4
    return _run_split("PROTECTED", "protected", seed.decode(), per_stratum, out_dir, None)


def stage_analyze(results_path: Path, custody_path: Path, out_dir: Path, label: str | None = None, selftest_report: Path | None = None) -> int:
    res = json.loads(results_path.read_text()); cus = json.loads(custody_path.read_text())
    label = label or res.get("label", "UNKNOWN")
    tp = results_path.with_name(results_path.name.replace("_RESULTS_", "_TIMING_"))
    timing = json.loads(tp.read_text()).get("wall_ns", {}) if tp.exists() else {}
    selftest_ok = None
    if selftest_report and selftest_report.exists():
        selftest_ok = bool(json.loads(selftest_report.read_text()).get("passed"))
    else:
        sp = out_dir / "ME_X4_SELFTEST_REPORT.json"
        if sp.exists():
            selftest_ok = bool(json.loads(sp.read_text()).get("passed"))
    sc = score(res, cus, timing=timing)
    gt = gates(sc, res, selftest_ok)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label, "results_sha256": sha256_file(results_path), "custody_sha256": sha256_file(custody_path), "n_instances": len(res["instances"]), "score": {"per_arm": sc["per_arm"]}, "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X4_{label}_ANALYSIS_V1.json").write_text(json.dumps(analysis, indent=2, sort_keys=True))
    (out_dir / f"ME_X4_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    print(f"{label} route: {gt['ROUTE']['route']} ({gt['ROUTE']['reason']}); ladder: {gt['ROUTE']['ladder_terminal']}; M exact {sc['per_arm'][M_ARM]['instance_exact_rate']:.3f}, B5 exact {sc['per_arm'][B5_ARM]['instance_exact_rate']:.3f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-stratum", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_stratum or DEV_PER_STRATUM)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_stratum or PROTECTED_PER_STRATUM, a.seed_file)
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr); return 2
        return stage_analyze(a.results, a.custody, a.out, selftest_report=a.selftest_report)
    return 2


if __name__ == "__main__":
    sys.exit(main())
