#!/usr/bin/env python3
"""ME-X2 exact locus-diagnosis / minimum-escalation study runner (frozen with design V1).

Stages
  selftest   parent fidelity (native known-answer tests), G0a hand-authored fixtures
             (oracle + M/B5 decisions), H-EXT-3 separation pair, G0b/G0c on a small
             generated set (public selftest seed).
  dev        DEVELOPMENT split (public seed, <= 48 instances). Never protected evidence.
  protected  PROTECTED split. Refuses unless PROTECTED_RUN_AUTHORIZATION.json
             (human_written=true, token >= 16 chars, acknowledged_design_sha256 = sha256 of
             the frozen design JSON) is present next to this script AND the custody seed
             file's sha256 equals the commitment frozen in the design JSON.
  analyze    Score a results file against its custody file: S5 outcomes, gates G0-G4,
             cost, pre-registered route.

Design: ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.{md,json}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from mex2_arms import arm_specs, make_policy  # noqa: E402
from mex2_generator import generate_split, known_answer_fixtures, separation_pair  # noqa: E402
from mex2_model import CLASSES, STRATA, TYPICAL_LEVEL, Instance, canonical_json, instance_from_json, instance_to_json  # noqa: E402
from mex2_oracle import Environment, oracle_targets  # noqa: E402
from mex2_parents import fidelity_selftests  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x2.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x2.exact-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X2-DEV-20260902"
DEV_PAIRS_PER_STRATUM = 2          # 48 instances
DEV_CAP = 48
PROTECTED_PAIRS_PER_STRATUM = 50   # 1200 instances
DEFAULT_SEED_FILE = Path(os.environ.get("MEX2_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x2/PROTECTED_SEED_V1.txt")))

M_ARM = "M_ME_LOCUS_PLUS_MINIMUM_ESCALATION"
B5_ARM = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
LADDER = ["B5_R1_VERDICT_ONLY", "B5_R2_PLUS_CANDIDATE_SET", "B5_R3_PLUS_DISCRIMINATOR_TABLES", "B5_R4_PLUS_DISPOSITION_RECORDS", B5_ARM]
EXTRA_SEARCH_ARM = "B3_EQUAL_EXTRA_SEARCH_1_5X"
LOCUS_ABLATIONS = ("M_MINUS_LOCUS_DIAGNOSIS", "M_LOCUS_LABELS_SHUFFLED")
MIN_DECOYS = {"PROTECTED": 5, "DEVELOPMENT": 0, "SELFTEST": 0}
RANDOM_MAX = 0.25


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- running --------------------------------------------------------------------------------------------

def _scaled(inst: Instance, mult: float) -> Instance:
    if mult == 1.0:
        return inst
    return Instance(**{**{k: getattr(inst, k) for k in inst.__dataclass_fields__}, "budget": int(round(inst.budget * mult))})


def run_instances(pairs: list[tuple[Instance, dict]], label: str, split_seed_public: str | None) -> tuple[dict, dict]:
    specs = arm_specs()
    results = {"schema_version": SCHEMA_RESULTS, "label": label, "split_seed": split_seed_public, "arms": [s.name for s in specs], "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label, "instances": []}
    timing: dict[str, dict[str, int]] = {}
    for inst, orc in pairs:
        rec = {"instance_id": inst.instance_id, "pair_id": inst.pair_id, "partner_instance_id": inst.partner_instance_id, "stratum": orc["oracle_class"], "variant": inst.variant,
               "template": inst.template, "apparent_class": inst.apparent_class, "budget": inst.budget, "features": inst.features,
               "public": instance_to_json(inst, include_truth=False), "arms": {}}
        for spec in specs:
            pol = make_policy(spec, inst.seed)
            t0 = time.perf_counter_ns()
            traj = Environment(_scaled(inst, spec.budget_multiplier)).run(pol)
            wall = time.perf_counter_ns() - t0
            rec["arms"][spec.name] = {"trajectory": traj.as_dict(), "budget_multiplier": spec.budget_multiplier, "jump_receipts": getattr(pol, "jump_receipts", None)}
            timing.setdefault(inst.instance_id, {})[spec.name] = wall
        results["instances"].append(rec)
        custody["instances"].append({"instance_id": inst.instance_id, "stratum": orc["oracle_class"], "oracle": orc, "instance": instance_to_json(inst)})
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -----------------------------------------------------------------------------------------------

def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n)


def paired_summary(x: list[bool], y: list[bool]) -> dict:
    n = len(x)
    b = sum(1 for a, bb in zip(x, y) if a and not bb); c = sum(1 for a, bb in zip(x, y) if bb and not a)
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {"n": n, "x_only": b, "y_only": c, "discordant": b + c, "diff_x_minus_y": diff, "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se], "exact_p_two_sided": exact_binomial_two_sided(b, c)}


def score_trajectory(traj: dict, orc: dict, inst_json: dict) -> dict:
    lv = {i["intervention_id"]: i["level"] for i in inst_json["interventions"]}
    steps = traj["steps"]
    applied = [lv[s["target"]] for s in steps if s["kind"] == "INTERVENE"]
    recur = sum(1 for s in steps if s["kind"] == "INTERVENE" and s["outcome"] == "RECURRENCE")
    dec = next((s for s in reversed(steps) if s["kind"] in ("INTERVENE", "DECLARE_CANNOT_IDENTIFY")), None)
    d_cls = dec["declared_class"] if dec else None; d_loc = dec["declared_locus"] if dec else None; conf = dec["confidence"] if dec else None
    ol = orc["oracle_level"]; success = traj["success"]
    max_lv = max(applied) if applied else None
    if ol is None:
        decision = traj["terminal"] == "CANNOT_IDENTIFY_DECLARED" and (max_lv is None or max_lv < 2)
        false_esc = max_lv is not None and max_lv >= 2
        missed = False
    else:
        decision = success and applied[-1] == ol and max_lv <= ol
        false_esc = max_lv is not None and max_lv > ol
        missed = not success
    cost = traj["total_cost"]
    return {
        "class_correct": d_cls == orc["oracle_class"], "locus_correct": d_loc == orc["oracle_locus"], "decision_correct": bool(decision), "success": bool(success),
        "false_escalation": bool(false_esc), "missed_escalation": bool(missed), "false_ci": traj["terminal"] == "CANNOT_IDENTIFY_DECLARED" and ol is not None,
        "correct_ci": traj["terminal"] == "CANNOT_IDENTIFY_DECLARED" and ol is None, "recurrence": recur, "spec_damage": 4 in applied and orc["truth_locus"] != "PROBLEM_CRITERION",
        "false_world_change": d_loc == "TARGET_WORLD" and orc["oracle_locus"] != "TARGET_WORLD", "false_model_attribution": d_cls == "MODEL_FAMILY_INADEQUATE" and orc["oracle_class"] != "MODEL_FAMILY_INADEQUATE",
        "false_representation_attribution": d_cls in ("REPRESENTATION_INSUFFICIENT", "FORMALISM_OR_OPERATOR_INSUFFICIENT") and orc["oracle_class"] not in ("REPRESENTATION_INSUFFICIENT", "FORMALISM_OR_OPERATOR_INSUFFICIENT"),
        "cost": cost, "regret": (cost - orc["oracle_cost"]) if ol is not None else None, "ci_cost": cost if ol is None else None, "confidence": conf,
        "decision_seq": [(s["kind"], s["target"]) for s in steps if s["kind"] != "PROBE"], "max_level": max_lv, "declared_class": d_cls, "declared_locus": d_loc,
    }


def _ece(pairs: list[tuple[float, bool]], bins: int = 5) -> float | None:
    if not pairs:
        return None
    tot = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        grp = [(c, ok) for c, ok in pairs if (lo <= c < hi) or (b == bins - 1 and c == 1.0)]
        if grp:
            tot += len(grp) / len(pairs) * abs(sum(ok for _, ok in grp) / len(grp) - sum(c for c, _ in grp) / len(grp))
    return tot


def score(results: dict, custody: dict, *, timing: dict | None = None) -> dict:
    cus = {r["instance_id"]: r for r in custody["instances"]}
    timing = timing if timing is not None else results.get("_timing_wall_ns", {})
    arms = results["arms"]
    per: dict[str, list[dict]] = {a: [] for a in arms}
    order: list[str] = []; strata: list[str] = []; variants: list[str] = []; identifiable: list[bool] = []
    g0b = True; decoy_counts: dict[str, int] = {}; inverse_counts: dict[str, int] = {}; ci_apparent_identifiable = 0
    variant_ok = True
    for rec in results["instances"]:
        iid = rec["instance_id"]; c = cus[iid]; orc = c["oracle"]; inst_json = c["instance"]
        order.append(iid); strata.append(orc["oracle_class"]); variants.append(rec["variant"]); identifiable.append(orc["oracle_level"] is not None)
        g0b &= bool(orc["exhaustive_agrees"]) and bool(orc.get("uniformly_decidable", False))
        f = rec["features"]
        if f.get("is_decoy"):
            decoy_counts[rec["apparent_class"]] = decoy_counts.get(rec["apparent_class"], 0) + 1
        if f.get("is_inverse_decoy"):
            inverse_counts[rec["apparent_class"]] = inverse_counts.get(rec["apparent_class"], 0) + 1
        if rec["apparent_class"] == "CANNOT_IDENTIFY" and orc["oracle_level"] is not None:
            ci_apparent_identifiable += 1
        v = rec["variant"]
        if v == "PLAIN":
            variant_ok &= bool(orc["probe_identifiable"]) and orc["oracle_class"] == inst_json["causes"][[x["cause_id"] for x in inst_json["causes"]].index(inst_json["truth"])]["obstruction_class"]
        elif v == "PARTIAL":
            variant_ok &= bool(orc["identifiable"]) and not orc["probe_identifiable"]
        elif v == "SAME_FIX":
            variant_ok &= orc["oracle_locus"] == "CANNOT_IDENTIFY" and orc["oracle_level"] is not None
        elif v == "CI":
            variant_ok &= orc["oracle_class"] == "CANNOT_IDENTIFY" and orc["oracle_level"] is None
        for a in arms:
            s = score_trajectory(rec["arms"][a]["trajectory"], orc, inst_json)
            s["wall_ns"] = timing.get(iid, {}).get(a, 0)
            per[a].append(s)
    # within-pair oracle swap null for M
    swap: list[bool] = []
    rec_by_id = {r["instance_id"]: r for r in results["instances"]}
    for rec in results["instances"]:
        pid = rec["partner_instance_id"]
        if pid in cus and pid in rec_by_id and M_ARM in arms:
            oo = cus[pid]["oracle"]
            swap.append(score_trajectory(rec["arms"][M_ARM]["trajectory"], oo, cus[rec["instance_id"]]["instance"])["decision_correct"])
    summary = {}
    for a, rows in per.items():
        n = len(rows)
        def rate(k):
            return sum(bool(r[k]) for r in rows) / n if n else None
        ident_rows = [r for r in rows if r["regret"] is not None]
        ci_rows = [r for r in rows if r["ci_cost"] is not None]
        conf_pairs = [(r["confidence"], r["class_correct"]) for r in rows if r["confidence"] is not None]
        per_stratum = {}
        for st in STRATA:
            idx = [i for i, s in enumerate(strata) if s == st]
            per_stratum[st] = {"n": len(idx), "decision_rate": (sum(rows[i]["decision_correct"] for i in idx) / len(idx)) if idx else None, "class_rate": (sum(rows[i]["class_correct"] for i in idx) / len(idx)) if idx else None,
                               "false_escalation": sum(rows[i]["false_escalation"] for i in idx), "missed_escalation": sum(rows[i]["missed_escalation"] for i in idx)}
        per_variant = {}
        for v in sorted(set(variants)):
            idx = [i for i, x in enumerate(variants) if x == v]
            per_variant[v] = {"n": len(idx), "decision_rate": sum(rows[i]["decision_correct"] for i in idx) / len(idx)}
        summary[a] = {
            "n": n, "decision_rate": rate("decision_correct"), "class_rate": rate("class_correct"), "locus_rate": rate("locus_correct"), "success_rate": rate("success"),
            "false_escalation": sum(r["false_escalation"] for r in rows), "missed_escalation": sum(r["missed_escalation"] for r in rows), "false_ci": sum(r["false_ci"] for r in rows), "correct_ci": sum(r["correct_ci"] for r in rows),
            "n_ci_instances": len(ci_rows), "recurrence": sum(r["recurrence"] for r in rows), "spec_damage": sum(r["spec_damage"] for r in rows),
            "false_world_change": sum(r["false_world_change"] for r in rows), "false_model_attribution": sum(r["false_model_attribution"] for r in rows), "false_representation_attribution": sum(r["false_representation_attribution"] for r in rows),
            "mean_cost": sum(r["cost"] for r in rows) / n if n else None, "mean_regret": (sum(r["regret"] for r in ident_rows) / len(ident_rows)) if ident_rows else None, "mean_ci_cost": (sum(r["ci_cost"] for r in ci_rows) / len(ci_rows)) if ci_rows else None,
            "brier": (sum((c - ok) ** 2 for c, ok in conf_pairs) / len(conf_pairs)) if conf_pairs else None, "ece5": _ece(conf_pairs), "n_confidence": len(conf_pairs),
            "wall_ms": sum(r["wall_ns"] for r in rows) / 1e6, "per_stratum": per_stratum, "per_variant": per_variant,
        }
    return {"per_arm": summary, "_rows": per, "order": order, "strata": strata, "variants": variants, "identifiable": identifiable, "g0b_all_agree": g0b, "variant_invariants_hold": variant_ok,
            "decoy_counts": decoy_counts, "inverse_decoy_counts": inverse_counts, "ci_apparent_identifiable": ci_apparent_identifiable, "swap_null_M": swap}


def gates(sc: dict, results: dict, selftest_ok: bool | None, label: str) -> dict:
    rows = sc["_rows"]; strata = sc["strata"]; n = len(sc["order"]); arms = results["arms"]
    g: dict = {}
    m = [r["decision_correct"] for r in rows[M_ARM]]; b5 = [r["decision_correct"] for r in rows[B5_ARM]]
    m_rate = sum(m) / n if n else 0.0
    # G0
    min_d = MIN_DECOYS.get(label, 1)
    decoy_ok = all(sc["decoy_counts"].get(c, 0) >= min_d for c in CLASSES if (TYPICAL_LEVEL[c] or 0) >= 1)
    inverse_ok = all(sc["inverse_decoy_counts"].get(c, 0) >= min_d for c in CLASSES if TYPICAL_LEVEL[c] == 0) and sc["ci_apparent_identifiable"] >= min_d
    g["G0a_KNOWN_ANSWER"] = {"pass": selftest_ok, "rule": "16 hand-authored fixtures (oracle targets; M and B5 decision-correct) + separation pair reproduced in selftest"}
    g["G0b_ORACLE_SELF_AGREEMENT"] = {"pass": bool(sc["g0b_all_agree"] and sc["variant_invariants_hold"] and decoy_ok and inverse_ok), "exhaustive_agrees_all": sc["g0b_all_agree"], "variant_invariants_hold": sc["variant_invariants_hold"],
                                      "decoy_coverage_ok": decoy_ok, "inverse_decoy_coverage_ok": inverse_ok, "decoy_counts": sc["decoy_counts"], "inverse_decoy_counts": sc["inverse_decoy_counts"], "ci_apparent_identifiable": sc["ci_apparent_identifiable"], "min_per_class": min_d,
                                      "rule": "enumeration == branch-and-bound and a truth-agnostic decision-correct policy exists on every instance; variant invariants hold; >= min decoys per apparent class (typical level >= 1) and >= min inverse decoys per level-0 class and apparent-CANNOT_IDENTIFY"}
    never = [r["decision_correct"] for r, ident in zip(rows["C_NEVER_INTERVENE"], sc["identifiable"]) if ident]
    rnd = sum(r["decision_correct"] for r in rows["C_RANDOM_POLICY"]) / n if n else 0.0
    swap = sc["swap_null_M"]; swap_rate = sum(swap) / len(swap) if swap else 0.0
    g["G0c_NULL_CALIBRATION"] = {"pass": bool(sum(never) == 0 and rnd <= RANDOM_MAX and swap_rate <= m_rate - 0.30), "never_intervene_correct_on_identifiable": sum(never), "n_identifiable": len(never), "random_decision_rate": rnd,
                                 "M_within_pair_swap_rate": swap_rate, "M_decision_rate": m_rate, "swap_n": len(swap),
                                 "rule": "NEVER_INTERVENE decision-correct = 0 on identifiable instances; RANDOM <= 0.25; M scored against the partner's oracle <= M's true rate - 0.30"}
    g0 = bool(g["G0a_KNOWN_ANSWER"]["pass"]) and g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"]
    # G1
    identical = [rows[M_ARM][i]["decision_seq"] == rows[B5_ARM][i]["decision_seq"] for i in range(n)]
    ps = paired_summary(m, b5)
    per_st = {}
    for st in STRATA:
        idx = [i for i, s in enumerate(strata) if s == st]
        if idx:
            per_st[st] = {"n": len(idx), "decision_discordant": sum(1 for i in idx if not identical[i]), "M_only_correct": sum(1 for i in idx if m[i] and not b5[i]), "B5_only_correct": sum(1 for i in idx if b5[i] and not m[i])}
    disc = 1 - sum(identical) / n if n else 0.0
    g1a = disc <= 0.005 and all(v["decision_discordant"] / v["n"] <= 0.05 for v in per_st.values())
    g1b = ps["diff_x_minus_y"] > 0 and ps["exact_p_two_sided"] <= 0.05 and any(v["M_only_correct"] >= 5 for v in per_st.values())
    g1c = ps["diff_x_minus_y"] < 0 and ps["exact_p_two_sided"] <= 0.05
    g["G1a_B5_REPRODUCES_M"] = {"pass": bool(g1a), "decision_identity_rate": 1 - disc, "per_stratum": per_st, "rule": "intervention/declaration sequences identical on >= 99.5% of instances and no stratum > 5% discordant"}
    g["G1b_M_ADVANTAGE"] = {"pass": bool(g1b), "paired": ps, "rule": "minimal-level decision-correct diff (M - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M-only-correct"}
    g["G1c_B5_ADVANTAGE"] = {"pass": bool(g1c), "rule": "symmetric: diff < 0 with p <= 0.05 (B5 dominates)"}
    # G2
    sm = sc["per_arm"][M_ARM]; sb = sc["per_arm"][B5_ARM]
    g["G2_ANTI_ESCALATION"] = {"pass": bool(sm["false_escalation"] <= sb["false_escalation"] and sm["spec_damage"] <= sb["spec_damage"]), "M_false_escalation": sm["false_escalation"], "B5_false_escalation": sb["false_escalation"], "M_spec_damage": sm["spec_damage"], "B5_spec_damage": sb["spec_damage"],
                               "rule": "M false escalations <= B5's and M specification damage <= B5's"}
    # G3 (only if G1b)
    g3: dict = {"pass": None, "applicable": bool(g1b), "checks": {}}
    if g1b:
        only = [i for i in range(n) if m[i] and not b5[i]]
        cls_ok = sum(rows[M_ARM][i]["class_correct"] for i in only) / len(only) if only else 0.0
        a_ok = cls_ok >= 0.8
        b_ok = True; b_checks = {}
        for st, v in per_st.items():
            if v["M_only_correct"] >= 5:
                b5r = sc["per_arm"][B5_ARM]["per_stratum"][st]["decision_rate"] or 0.0
                abl = {a: (sc["per_arm"][a]["per_stratum"][st]["decision_rate"] or 0.0) for a in LOCUS_ABLATIONS}
                ok = all(r <= b5r + 1e-12 for r in abl.values())
                b_checks[st] = {"B5_rate": b5r, "ablation_rates": abl, "advantage_vanishes": ok}; b_ok &= ok
        x = [r["decision_correct"] for r in rows[EXTRA_SEARCH_ARM]]
        pe = paired_summary(m, x)
        c_ok = pe["diff_x_minus_y"] > 0 and pe["exact_p_two_sided"] <= 0.05
        g3["checks"] = {"a_class_correct_among_M_only": cls_ok, "a_pass": a_ok, "b_per_stratum": b_checks, "b_pass": b_ok, "c_vs_extra_search": pe, "c_pass": c_ok}
        g3["pass"] = bool(a_ok and b_ok and c_ok)
    g3["rule"] = "(a) M's class correct on >= 80% of M-only-correct instances; (b) on each advantaged stratum both locus ablations <= B5; (c) B3 with 1.5x budget does not reach M (paired p <= 0.05)"
    g["G3_MEDIATION"] = g3
    # G4 ladder
    rung_rates = {r: sc["per_arm"][r]["decision_rate"] for r in LADDER}
    steps = []; monotone = True
    for k in range(4):
        p = paired_summary([r["decision_correct"] for r in rows[LADDER[k + 1]]], [r["decision_correct"] for r in rows[LADDER[k]]])
        violated = p["diff_x_minus_y"] < 0 and p["exact_p_two_sided"] <= 0.05
        monotone &= not violated
        steps.append({"from": LADDER[k], "to": LADDER[k + 1], "paired": p, "violation": violated})
    gap_null = not g1b
    g["G4_INTERFACE_LADDER"] = {"pass": bool(monotone), "rung_decision_rates": rung_rates, "steps": steps, "rung5_gap": ps, "rung5_gap_null": gap_null,
                                "terminal": ("RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL" if (monotone and gap_null) else "CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE" if (monotone and not gap_null) else "LADDER_NON_MONOTONE"),
                                "rule": "no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = G1 paired test"}
    # cost (registered cost units are commensurable across arms)
    rm = [r["regret"] for r in rows[M_ARM]]; rb = [r["regret"] for r in rows[B5_ARM]]
    m_less = sum(1 for a, b in zip(rm, rb) if a is not None and b is not None and a < b); b_less = sum(1 for a, b in zip(rm, rb) if a is not None and b is not None and b < a)
    pc = exact_binomial_two_sided(m_less, b_less)
    flag = "COST_ADVANTAGE_M" if (m_less > b_less and pc <= 0.05) else "COST_ADVANTAGE_B5" if (b_less > m_less and pc <= 0.05) else "COST_PARITY"
    g["COST"] = {"M_mean_regret": sm["mean_regret"], "B5_mean_regret": sb["mean_regret"], "M_mean_cost": sm["mean_cost"], "B5_mean_cost": sb["mean_cost"], "instances_M_lower_regret": m_less, "instances_B5_lower_regret": b_less, "sign_test_p": pc,
                 "M_wall_ms": sm["wall_ms"], "B5_wall_ms": sb["wall_ms"], "flag": flag, "rule": "paired sign test on per-instance regret (registered cost units) at p <= 0.05; wall-clock reported only"}
    # route
    if not g0:
        route, reason = "CANNOT_CHECK", "G0 generator/oracle/null validity failed: lane defect, repair and re-freeze"
    elif g1a:
        route, reason = "PARENT_SUFFICIENT", "B5 reproduces M's intervention decisions"
    elif g1b:
        if not g["G2_ANTI_ESCALATION"]["pass"]:
            route, reason = "M_OVER_ESCALATES", "M advantage coexists with more false escalation or specification damage than B5"
        elif not g3["pass"]:
            route, reason = "CANNOT_CHECK", "M advantage not attributable to locus diagnosis (G3 failed)"
        elif flag == "COST_ADVANTAGE_B5":
            route, reason = "QUALITY_COST_TRADEOFF_NO_DOMINANCE", "M advantage on minimal-level decisions but B5 significantly lower regret: no frontier dominance"
        else:
            route, reason = "ME_X2_RESIDUAL_CANDIDATE", "M advantage, anti-escalation, mediation attributed, not cost-dominated"
    elif g1c:
        route, reason = "PARENT_SUFFICIENT", "B5 dominates M on minimal-level decisions (B5_DOMINATES)"
    else:
        route, reason = "PARENT_SUFFICIENT", "no M advantage over B5 (discordance without significance)"
    g["ROUTE"] = {"route": route, "reason": reason, "ladder_terminal": g["G4_INTERFACE_LADDER"]["terminal"], "cost_flag": flag, "b5_dominates": bool(g1c)}
    return g


def render_md(analysis: dict) -> str:
    L = [f"# ME-X2 analysis — {analysis['label']}\n"]
    if analysis["label"] == "DEVELOPMENT":
        L.append("**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**\n")
    L.append(f"Results sha256 `{analysis['results_sha256']}`; custody sha256 `{analysis['custody_sha256']}`; instances {analysis['n_instances']}.\n")
    L.append("## Per-arm outcomes (S5)\n")
    L.append("| arm | decision (min-level) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | false world | mean regret | mean cost | Brier | ECE5 | wall ms |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    f = lambda v: "n/a" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
    for a, s in analysis["score"]["per_arm"].items():
        L.append(f"| {a} | {f(s['decision_rate'])} | {f(s['class_rate'])} | {f(s['locus_rate'])} | {f(s['success_rate'])} | {s['false_escalation']} | {s['missed_escalation']} | {s['false_ci']} | {s['correct_ci']}/{s['n_ci_instances']} | {s['recurrence']} | {s['spec_damage']} | {s['false_world_change']} | {f(s['mean_regret'])} | {f(s['mean_cost'])} | {f(s['brier'])} | {f(s['ece5'])} | {s['wall_ms']:.1f} |")
    arms = list(analysis["score"]["per_arm"])
    L.append("\n## Per-stratum decision-correct rate (stratum = oracle class)\n")
    L.append("| stratum | n | " + " | ".join(arms) + " |"); L.append("|---|---|" + "---|" * len(arms))
    for st in STRATA:
        v0 = analysis["score"]["per_arm"][arms[0]]["per_stratum"][st]
        L.append(f"| {st} | {v0['n']} | " + " | ".join("–" if analysis["score"]["per_arm"][a]["per_stratum"][st]["decision_rate"] is None else f"{analysis['score']['per_arm'][a]['per_stratum'][st]['decision_rate']:.2f}" for a in arms) + " |")
    L.append("\n## Per-variant decision-correct rate\n")
    vars_ = sorted(analysis["score"]["per_arm"][arms[0]]["per_variant"])
    L.append("| variant | n | " + " | ".join(arms) + " |"); L.append("|---|---|" + "---|" * len(arms))
    for v in vars_:
        L.append(f"| {v} | {analysis['score']['per_arm'][arms[0]]['per_variant'][v]['n']} | " + " | ".join(f"{analysis['score']['per_arm'][a]['per_variant'][v]['decision_rate']:.2f}" for a in arms) + " |")
    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        if k != "ROUTE":
            L.append(f"- **{k}**: pass={v.get('pass')} — {v.get('rule', '')}")
    r = analysis["gates"]["ROUTE"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}. Ladder terminal: `{r['ladder_terminal']}`. Cost: `{r['cost_flag']}`.\n")
    return "\n".join(L)


# ---- stages -------------------------------------------------------------------------------------------------

def _run_fixture_arms(inst: Instance, names: list[str]) -> dict:
    specs = {s.name: s for s in arm_specs()}
    out = {}
    for nme in names:
        traj = Environment(inst).run(make_policy(specs[nme], "selftest"))
        out[nme] = traj.as_dict()
    return out


def stage_selftest(out_dir: Path) -> int:
    report: dict = {"schema_version": SCHEMA_ANALYSIS + ".selftest", "parent_fidelity": fidelity_selftests(), "known_answer": [], "separation": {}, "oracle_agreement": None, "null_calibration": None}
    ok = all(r["passed"] for r in report["parent_fidelity"])
    for fx in known_answer_fixtures():
        inst = fx["instance"]; orc = oracle_targets(inst)
        got = {k: orc[k] for k in fx["expected"]}
        passed = got == fx["expected"] and orc["exhaustive_agrees"]
        arms = _run_fixture_arms(inst, [M_ARM, B5_ARM])
        dec = {a: score_trajectory(t, orc, instance_to_json(inst))["decision_correct"] for a, t in arms.items()}
        passed &= all(dec.values())
        report["known_answer"].append({"name": fx["name"], "passed": bool(passed), "expected": fx["expected"], "oracle": got, "decision_correct": dec})
        ok &= passed
    sep = separation_pair(); sep_out = {}
    for case in sep:
        inst = case["instance"]; orc = oracle_targets(inst)
        oracle_ok = {k: orc[k] for k in case["expected"]} == case["expected"]
        arms = _run_fixture_arms(inst, [LADDER[0], B5_ARM, M_ARM])
        sep_out[case["name"]] = {"oracle_matches_hand_answer": oracle_ok, "oracle": {k: orc[k] for k in case["expected"]}, "arms": {a: score_trajectory(t, orc, instance_to_json(inst)) for a, t in arms.items()}, "raw": arms}
        ok &= oracle_ok
    v1 = [sep_out[c]["arms"][LADDER[0]]["decision_seq"] for c in ("SEP-P", "SEP-Q")]
    verdict_identical = v1[0] == v1[1]
    verdict_fails_one = not all(sep_out[c]["arms"][LADDER[0]]["decision_correct"] for c in ("SEP-P", "SEP-Q"))
    structure_exact = all(sep_out[c]["arms"][a]["decision_correct"] for c in ("SEP-P", "SEP-Q") for a in (B5_ARM, M_ARM))
    report["separation"] = {"cases": {k: {kk: vv for kk, vv in v.items() if kk != "raw"} for k, v in sep_out.items()}, "verdict_only_outputs_identical_on_P_and_Q": verdict_identical, "verdict_only_fails_at_least_one": verdict_fails_one,
                            "structure_exchange_exact_on_both": structure_exact, "passed": bool(verdict_identical and verdict_fails_one and structure_exact)}
    ok &= report["separation"]["passed"]
    pairs = generate_split("selftest", "ME-X2-SELFTEST", {s: 1 for s in STRATA})
    res, cus = run_instances(pairs, "SELFTEST", "ME-X2-SELFTEST")
    sc = score(res, cus)
    gt = gates(sc, res, True, "SELFTEST")
    report["oracle_agreement"] = sc["g0b_all_agree"]; ok &= sc["g0b_all_agree"] and sc["variant_invariants_hold"]
    report["null_calibration"] = gt["G0c_NULL_CALIBRATION"]; ok &= gt["G0c_NULL_CALIBRATION"]["pass"]
    report["selftest_arm_decision_rates"] = {a: v["decision_rate"] for a, v in sc["per_arm"].items()}
    report["passed"] = bool(ok)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X2_SELFTEST_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    print(f"selftest {'PASS' if ok else 'FAIL'}: parent tests {sum(r['passed'] for r in report['parent_fidelity'])}/{len(report['parent_fidelity'])}, known-answer {sum(k['passed'] for k in report['known_answer'])}/{len(report['known_answer'])}, separation {report['separation']['passed']}, oracle agreement {sc['g0b_all_agree']}, null calibration {gt['G0c_NULL_CALIBRATION']['pass']}")
    return 0 if ok else 1


def _run_split(label: str, split: str, split_seed: str, pairs_per_stratum: int, out_dir: Path, public_seed: str | None) -> int:
    pairs = generate_split(split, split_seed, {s: pairs_per_stratum for s in STRATA})
    res, cus = run_instances(pairs, label, public_seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X2_{label}_RESULTS_V1.json"; cp = out_dir / f"ME_X2_{label}_EXPECTED_CUSTODY_V1.json"; tp = out_dir / f"ME_X2_{label}_TIMING_V1.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus))
    tp.write_text(canonical_json({"schema_version": SCHEMA_RESULTS + ".timing", "label": label, "wall_ns": timing, "note": "wall-clock is machine-dependent and is kept out of the deterministic results file"}))
    print(f"{label}: {len(pairs)} instances, results {rp} sha256 {sha256_file(rp)[:16]}…, custody {cp} sha256 {sha256_file(cp)[:16]}…")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, pairs_per_stratum: int) -> int:
    if pairs_per_stratum * len(STRATA) * 2 > DEV_CAP:
        print(f"development split is capped at {DEV_CAP} instances", file=sys.stderr); return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, pairs_per_stratum, out_dir, DEV_SEED)


def stage_protected(out_dir: Path, pairs_per_stratum: int, seed_file: Path) -> int:
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
    return _run_split("PROTECTED", "protected", seed.decode(), pairs_per_stratum, out_dir, None)


def stage_analyze(results_path: Path, custody_path: Path, out_dir: Path, label: str | None = None, selftest_report: Path | None = None) -> int:
    res = json.loads(results_path.read_text()); cus = json.loads(custody_path.read_text())
    label = label or res.get("label", "UNKNOWN")
    tp = results_path.with_name(results_path.name.replace("_RESULTS_", "_TIMING_"))
    timing = json.loads(tp.read_text()).get("wall_ns", {}) if tp.exists() else {}
    selftest_ok = None
    sp = selftest_report if selftest_report else out_dir / "ME_X2_SELFTEST_REPORT.json"
    if sp.exists():
        selftest_ok = bool(json.loads(sp.read_text()).get("passed"))
    sc = score(res, cus, timing=timing)
    gt = gates(sc, res, selftest_ok, label)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label, "results_sha256": sha256_file(results_path), "custody_sha256": sha256_file(custody_path), "n_instances": len(res["instances"]),
                "score": {"per_arm": sc["per_arm"], "decoy_counts": sc["decoy_counts"], "inverse_decoy_counts": sc["inverse_decoy_counts"]}, "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X2_{label}_ANALYSIS_V1.json").write_text(json.dumps(analysis, indent=2, sort_keys=True))
    (out_dir / f"ME_X2_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    print(f"{label} route: {gt['ROUTE']['route']} ({gt['ROUTE']['reason']}); ladder: {gt['ROUTE']['ladder_terminal']}; cost: {gt['ROUTE']['cost_flag']}; M decision {sc['per_arm'][M_ARM]['decision_rate']:.3f}, B5 decision {sc['per_arm'][B5_ARM]['decision_rate']:.3f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--pairs-per-stratum", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.pairs_per_stratum or DEV_PAIRS_PER_STRATUM)
    if a.stage == "protected":
        return stage_protected(a.out, a.pairs_per_stratum or PROTECTED_PAIRS_PER_STRATUM, a.seed_file)
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr); return 2
        return stage_analyze(a.results, a.custody, a.out, selftest_report=a.selftest_report)
    return 2


if __name__ == "__main__":
    sys.exit(main())
