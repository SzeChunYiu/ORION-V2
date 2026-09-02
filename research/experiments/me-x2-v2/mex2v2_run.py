#!/usr/bin/env python3
"""ME-X2 V2 revival study runner (frozen with design V2).

The V1 lane routed `PARENT_SUFFICIENT` with `B5` ahead of `M`, on a uniform
failure signature: `M` takes the cheapest admissible discriminator with no
lookahead and its fail-closed reachability rule then reports that no live
hypothesis is establishable, so `M` declares `CANNOT_IDENTIFY` where an exact
planner picks the right test first and succeeds.  V1 registered both orderings
(design V1 §4.1) as *M's rendering*, not as ORION semantics.  V2 renders them
the other way (``mex2v2_levers``) and re-tests against the same strongest
parent, on a fresh committed seed.

Stages
  selftest   V1 provenance (G0d), parent fidelity, V1's 14 known-answer fixtures
             and separation pair, the V2 lever known-answer fixtures, and
             G0b/G0c on a small generated set (public selftest seed).
  dev        DEVELOPMENT split (public seed, <= 48 instances). Never protected evidence.
  g0scale    Optional protected-scale G0 coverage probe on a PUBLIC seed, run with
             V1-known arms only (M_V1 and both controls) so it reveals nothing about
             the V2 comparison.  Never evidence for any arm claim.
  protected  PROTECTED split.  Refuses unless PROTECTED_RUN_AUTHORIZATION.json
             (human_written=true, token >= 16 chars, acknowledged_design_sha256 = sha256
             of the frozen V2 design JSON) is present next to this script AND the custody
             seed file's sha256 equals the V2 commitment.
  analyze    Score a results file against its custody file: S5 outcomes, gates G0-G5,
             cost, pre-registered route and lever verdict.

Design: ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.{md,json}
V1 lane (imported, never edited): research/experiments/me-x2/
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
for _p in (str(HERE), str(V1_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from mex2_generator import generate_split, known_answer_fixtures, separation_pair  # noqa: E402
from mex2_model import CLASSES, STRATA, TYPICAL_LEVEL, Instance, canonical_json, instance_from_json, instance_to_json  # noqa: E402
from mex2_oracle import Environment, oracle_targets  # noqa: E402
from mex2_parents import fidelity_selftests  # noqa: E402
from mex2_run import exact_binomial_two_sided, paired_summary, score, score_trajectory  # noqa: E402

import mex2v2_provenance as provenance  # noqa: E402
from mex2v2_arms import B5_ARM, EXTRA_SEARCH_ARM, LADDER, M_V1_ARM, arm_specs, make_policy  # noqa: E402
from mex2v2_levers import M2_ARM, M2_L1_ARM, M2_L2_ARM, M2_LOCUS_ABLATIONS  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x2-v2.revival-study-results.v2"
SCHEMA_ANALYSIS = "orion.v2.me-x2-v2.revival-study-analysis.v2"
DESIGN_JSON = HERE / "ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.json"
LEVER_FIXTURES = HERE / "ME_X2_V2_LEVER_KNOWN_ANSWER_FIXTURES_V2.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X2-V2-DEV-20260902"
DEV_PAIRS_PER_STRATUM = 2          # 48 instances
DEV_CAP = 48
PROTECTED_PAIRS_PER_STRATUM = 50   # 1200 instances
DEFAULT_SEED_FILE = Path(os.environ.get("MEX2V2_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x2-v2/PROTECTED_SEED_V2.txt")))

MIN_DECOYS = {"PROTECTED": 5, "DEVELOPMENT": 0, "SELFTEST": 0, "G0SCALE": 5}
RANDOM_MAX = 0.25
# The decoy-coverage and random-control clauses are frequency claims about a 1 200-instance split and
# are n-sensitive; V1 already switched decoy coverage off below the protected split (MIN_DECOYS).  V2
# treats the random-control margin the same way: enforced on the protected split and on the scale
# probe, reported elsewhere.  The never-intervene clause and the within-pair swap null stay hard at
# every label, and no clause concerning an arm under test is relaxed anywhere.
RANDOM_MAX_ENFORCED = {"PROTECTED": True, "G0SCALE": True}
SWAP_MARGIN = 0.30
G0SCALE_ARMS = (M_V1_ARM, "C_RANDOM_POLICY", "C_NEVER_INTERVENE")
MEDIATION_CLASS_MIN = 0.8
MECHANISM_MIN = 0.8


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- running -------------------------------------------------------------------------------------

def _scaled(inst: Instance, mult: float) -> Instance:
    if mult == 1.0:
        return inst
    return Instance(**{**{k: getattr(inst, k) for k in inst.__dataclass_fields__}, "budget": int(round(inst.budget * mult))})


def run_instances(pairs: list[tuple[Instance, dict]], label: str, split_seed_public: str | None, only: tuple[str, ...] | None = None) -> tuple[dict, dict]:
    specs = [s for s in arm_specs() if only is None or s.name in only]
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
            rec["arms"][spec.name] = {"trajectory": traj.as_dict(), "budget_multiplier": spec.budget_multiplier,
                                      "jump_receipts": getattr(pol, "jump_receipts", None), "lever_receipts": getattr(pol, "lever_receipts", None)}
            timing.setdefault(inst.instance_id, {})[spec.name] = wall
        results["instances"].append(rec)
        custody["instances"].append({"instance_id": inst.instance_id, "stratum": orc["oracle_class"], "oracle": orc, "instance": instance_to_json(inst)})
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -------------------------------------------------------------------------------------

def score_v2(results: dict, custody: dict, *, timing: dict | None = None) -> dict:
    """V1's scorer (unchanged, imported) plus the V2 quantities: the within-pair oracle-swap null
    for the arm under test (M2 — never V1's ``swap_null_M``), and the per-instance lever activity."""
    sc = score(results, custody, timing=timing)
    cus = {r["instance_id"]: r for r in custody["instances"]}
    rec_by_id = {r["instance_id"]: r for r in results["instances"]}
    arms = results["arms"]
    swap_m2: list[bool] = []
    if M2_ARM in arms:
        for rec in results["instances"]:
            pid = rec["partner_instance_id"]
            if pid in cus and pid in rec_by_id:
                swap_m2.append(score_trajectory(rec["arms"][M2_ARM]["trajectory"], cus[pid]["oracle"], cus[rec["instance_id"]]["instance"])["decision_correct"])
    lever: list[dict] = []
    for rec in results["instances"]:
        arm = rec["arms"].get(M2_ARM) or {}
        rs = arm.get("lever_receipts") or []
        steps = (arm.get("trajectory") or {}).get("steps") or []
        # V1's inherited act() consults _discriminators before its unique / common-fix branches, so a
        # receipt is written for the top-ranked candidate even on steps where M2 goes on to apply a
        # unique or common fix instead.  Attribution must read only the actions actually EXECUTED.
        executed = [r for r in rs if r["step"] < len(steps) and steps[r["step"]]["kind"] == r["kind"] and steps[r["step"]]["target"] == r["action"]]
        lever.append({"instance_id": rec["instance_id"], "steps": len(rs), "executed_steps": len(executed),
                      "considered_not_executed": len(rs) - len(executed),
                      "l2_only_admissible": any(r.get("l2_only_admissible") for r in executed),
                      "l1_changed_choice": any(r.get("l1_changed_choice") for r in executed),
                      "expected_abstention_positive": any((r.get("expected_abstention") or 0) > 0 for r in executed),
                      "foreclosure_permitted": any((r.get("foreclosed") or 0) > 0 for r in executed)})
    sc["swap_null_M2"] = swap_m2
    sc["lever_activity"] = lever
    sc.pop("swap_null_M", None)     # V2 gates on the arm under test, never on V1's M
    return sc


def _rate(rows: list[dict], key: str = "decision_correct") -> float:
    return sum(bool(r[key]) for r in rows) / len(rows) if rows else 0.0


def gates_v2(sc: dict, results: dict, selftest_ok: bool | None, label: str, prov: dict | None = None) -> dict:
    rows = sc["_rows"]; strata = sc["strata"]; n = len(sc["order"]); arms = results["arms"]
    g: dict = {}
    m2 = [r["decision_correct"] for r in rows[M2_ARM]]
    b5 = [r["decision_correct"] for r in rows[B5_ARM]]
    v1 = [r["decision_correct"] for r in rows[M_V1_ARM]]
    m2_rate = sum(m2) / n if n else 0.0

    # ---- G0 -------------------------------------------------------------------------------------
    min_d = MIN_DECOYS.get(label, 1)
    decoy_ok = all(sc["decoy_counts"].get(c, 0) >= min_d for c in CLASSES if (TYPICAL_LEVEL[c] or 0) >= 1)
    inverse_ok = all(sc["inverse_decoy_counts"].get(c, 0) >= min_d for c in CLASSES if TYPICAL_LEVEL[c] == 0) and sc["ci_apparent_identifiable"] >= min_d
    g["G0a_KNOWN_ANSWER"] = {"pass": selftest_ok, "rule": "V1's 14 hand-authored fixtures and separation pair (M2 and B5 decision-correct) plus the V2 lever known-answer fixtures, reproduced in selftest"}
    g["G0b_ORACLE_SELF_AGREEMENT"] = {"pass": bool(sc["g0b_all_agree"] and sc["variant_invariants_hold"] and decoy_ok and inverse_ok), "exhaustive_agrees_all": sc["g0b_all_agree"], "variant_invariants_hold": sc["variant_invariants_hold"],
                                      "decoy_coverage_ok": decoy_ok, "inverse_decoy_coverage_ok": inverse_ok, "decoy_counts": sc["decoy_counts"], "inverse_decoy_counts": sc["inverse_decoy_counts"], "ci_apparent_identifiable": sc["ci_apparent_identifiable"], "min_per_class": min_d,
                                      "rule": "enumeration == branch-and-bound and a truth-agnostic decision-correct policy exists on every instance; variant invariants hold; >= min decoys per apparent class, inverse decoys per level-0 class and apparent-CANNOT_IDENTIFY identifiable instances"}
    never = [r["decision_correct"] for r, ident in zip(rows["C_NEVER_INTERVENE"], sc["identifiable"]) if ident]
    rnd = _rate(rows["C_RANDOM_POLICY"])
    swap = sc["swap_null_M2"]; swap_rate = sum(swap) / len(swap) if swap else 0.0
    rnd_enforced = RANDOM_MAX_ENFORCED.get(label, False)
    rnd_ok = rnd <= RANDOM_MAX or not rnd_enforced
    g["G0c_NULL_CALIBRATION"] = {"pass": bool(sum(never) == 0 and rnd_ok and swap_rate <= m2_rate - SWAP_MARGIN), "random_clause_enforced": bool(rnd_enforced), "random_clause_met": bool(rnd <= RANDOM_MAX), "never_intervene_correct_on_identifiable": sum(never), "n_identifiable": len(never), "random_decision_rate": rnd,
                                 "M2_within_pair_swap_rate": swap_rate, "M2_decision_rate": m2_rate, "swap_n": len(swap),
                                 "rule": "NEVER_INTERVENE decision-correct = 0 on identifiable instances; RANDOM <= 0.25 (enforced on PROTECTED and G0SCALE, reported below that split size); M2 scored against the partner's oracle <= M2's true rate - 0.30"}
    prov = prov if prov is not None else provenance.check()
    g["G0d_V1_PROVENANCE"] = {"pass": bool(prov["all_match"]), "files": prov["files"],
                              "rule": "every frozen V1 file (generator, oracle, catalogue, parents, arms, runner, design JSON) byte-identical to the hash published in the V1 receipt: V2 changes the arm under test and nothing else"}
    g0 = bool(g["G0a_KNOWN_ANSWER"]["pass"]) and g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"] and g["G0d_V1_PROVENANCE"]["pass"]

    # ---- G1 -------------------------------------------------------------------------------------
    identical = [rows[M2_ARM][i]["decision_seq"] == rows[B5_ARM][i]["decision_seq"] for i in range(n)]
    ps = paired_summary(m2, b5)
    per_st = {}
    for st in STRATA:
        idx = [i for i, s in enumerate(strata) if s == st]
        if idx:
            per_st[st] = {"n": len(idx), "decision_discordant": sum(1 for i in idx if not identical[i]),
                          "M2_only_correct": sum(1 for i in idx if m2[i] and not b5[i]), "B5_only_correct": sum(1 for i in idx if b5[i] and not m2[i])}
    disc = 1 - sum(identical) / n if n else 0.0
    g1a = disc <= 0.005 and all(v["decision_discordant"] / v["n"] <= 0.05 for v in per_st.values())
    g1b = ps["diff_x_minus_y"] > 0 and ps["exact_p_two_sided"] <= 0.05 and any(v["M2_only_correct"] >= 5 for v in per_st.values())
    g1c = ps["diff_x_minus_y"] < 0 and ps["exact_p_two_sided"] <= 0.05
    g["G1a_B5_REPRODUCES_M2"] = {"pass": bool(g1a), "decision_identity_rate": 1 - disc, "per_stratum": per_st, "rule": "intervention/declaration sequences identical on >= 99.5% of instances and no stratum > 5% discordant"}
    g["G1b_M2_ADVANTAGE"] = {"pass": bool(g1b), "paired": ps, "rule": "minimal-level decision-correct diff (M2 - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M2-only-correct"}
    g["G1c_B5_ADVANTAGE"] = {"pass": bool(g1c), "rule": "symmetric: diff < 0 with p <= 0.05 (B5 dominates)"}

    # ---- G2 -------------------------------------------------------------------------------------
    sm = sc["per_arm"][M2_ARM]; sb = sc["per_arm"][B5_ARM]; sv = sc["per_arm"][M_V1_ARM]
    g2a = sm["false_escalation"] <= sb["false_escalation"] and sm["spec_damage"] <= sb["spec_damage"]
    g2b = sm["false_escalation"] <= sv["false_escalation"] and sm["spec_damage"] <= sv["spec_damage"]
    g["G2_ANTI_ESCALATION"] = {"pass": bool(g2a and g2b), "vs_B5_pass": bool(g2a), "vs_M_V1_pass": bool(g2b),
                               "M2_false_escalation": sm["false_escalation"], "B5_false_escalation": sb["false_escalation"], "M_V1_false_escalation": sv["false_escalation"],
                               "M2_spec_damage": sm["spec_damage"], "B5_spec_damage": sb["spec_damage"], "M_V1_spec_damage": sv["spec_damage"],
                               "rule": "M2 false escalations and specification damage <= B5's (V1's clause) AND <= V1's M: a revival may not buy decisions with escalation harm"}

    # ---- G3 mediation (only if G1b) ---------------------------------------------------------------
    g3: dict = {"pass": None, "applicable": bool(g1b), "checks": {}}
    if g1b:
        only = [i for i in range(n) if m2[i] and not b5[i]]
        cls_ok = sum(rows[M2_ARM][i]["class_correct"] for i in only) / len(only) if only else 0.0
        a_ok = cls_ok >= MEDIATION_CLASS_MIN
        b_ok = True; b_checks = {}
        for st, v in per_st.items():
            if v["M2_only_correct"] >= 5:
                b5r = sc["per_arm"][B5_ARM]["per_stratum"][st]["decision_rate"] or 0.0
                abl = {a: (sc["per_arm"][a]["per_stratum"][st]["decision_rate"] or 0.0) for a in M2_LOCUS_ABLATIONS}
                ok = all(r <= b5r + 1e-12 for r in abl.values())
                b_checks[st] = {"B5_rate": b5r, "ablation_rates": abl, "advantage_vanishes": ok}; b_ok &= ok
        pe = paired_summary(m2, [r["decision_correct"] for r in rows[EXTRA_SEARCH_ARM]])
        c_ok = pe["diff_x_minus_y"] > 0 and pe["exact_p_two_sided"] <= 0.05
        g3["checks"] = {"a_class_correct_among_M2_only": cls_ok, "a_pass": a_ok, "b_per_stratum": b_checks, "b_pass": b_ok, "c_vs_extra_search": pe, "c_pass": c_ok}
        g3["pass"] = bool(a_ok and b_ok and c_ok)
    g3["rule"] = "(a) M2's class correct on >= 80% of M2-only-correct instances; (b) on each advantaged stratum both locus ablations <= B5; (c) B3 with 1.5x budget does not reach M2 (paired p <= 0.05)"
    g["G3_MEDIATION"] = g3

    # ---- G4 ladder --------------------------------------------------------------------------------
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
                                "rule": "no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = the G1 paired test"}

    # ---- G5 lever attribution ---------------------------------------------------------------------
    pv = paired_summary(m2, v1)
    l1 = [r["decision_correct"] for r in rows[M2_L1_ARM]]; l2 = [r["decision_correct"] for r in rows[M2_L2_ARM]]
    p_l1 = paired_summary(l1, v1); p_l2 = paired_summary(l2, v1)
    a_ok = pv["diff_x_minus_y"] > 0 and pv["exact_p_two_sided"] <= 0.05
    b_ok = (p_l1["diff_x_minus_y"] <= pv["diff_x_minus_y"]) and (p_l2["diff_x_minus_y"] <= pv["diff_x_minus_y"])
    act = {r["instance_id"]: r for r in sc["lever_activity"]}
    only_m2 = [i for i in range(n) if m2[i] and not v1[i]]
    mech = 0
    for i in only_m2:
        a = act.get(sc["order"][i], {})
        if rows[M_V1_ARM][i]["false_ci"] and (a.get("l2_only_admissible") or a.get("l1_changed_choice")):
            mech += 1
    mech_rate = mech / len(only_m2) if only_m2 else 0.0
    c_ok = bool(only_m2) and mech_rate >= MECHANISM_MIN
    only_v1 = [i for i in range(n) if v1[i] and not m2[i]]
    d_ok = len(only_v1) < len(only_m2)
    g["G5_LEVER_ATTRIBUTION"] = {"pass": bool(a_ok and b_ok and c_ok and d_ok), "applicable": True,
                                 "a_paired_M2_vs_M_V1": pv, "a_pass": bool(a_ok),
                                 "b_single_lever_vs_M_V1": {M2_L1_ARM: p_l1, M2_L2_ARM: p_l2}, "b_pass": bool(b_ok),
                                 "c_mechanism_rate": mech_rate, "c_n_M2_only_correct": len(only_m2), "c_pass": bool(c_ok),
                                 "d_n_M_V1_only_correct": len(only_v1), "d_pass": bool(d_ok),
                                 "rule": "(a) paired M2 - M_V1 > 0 at exact p <= 0.05 [routes the lever verdict]; (b) neither single-lever arm improves on M_V1 by more than the conjunction does [reported diagnostic]; "
                                         "(c) >= 80% of M2-only-correct instances are ones where V1 declared a false CANNOT_IDENTIFY AND M2's EXECUTED lever receipts show an L2-only-admissible action or an L1-changed choice [routes the lever verdict: failing it gives LEVERS_NOT_ATTRIBUTED]; "
                                         "(d) M2 loses fewer instances to V1 than it gains: the revival must not move the failure [routes the lever verdict: failing it gives LEVERS_MOVE_THE_FAILURE]"}

    # ---- cost --------------------------------------------------------------------------------------
    rm = [r["regret"] for r in rows[M2_ARM]]; rb = [r["regret"] for r in rows[B5_ARM]]
    m_less = sum(1 for a, b in zip(rm, rb) if a is not None and b is not None and a < b)
    b_less = sum(1 for a, b in zip(rm, rb) if a is not None and b is not None and b < a)
    pc = exact_binomial_two_sided(m_less, b_less)
    flag = "COST_ADVANTAGE_M2" if (m_less > b_less and pc <= 0.05) else "COST_ADVANTAGE_B5" if (b_less > m_less and pc <= 0.05) else "COST_PARITY"
    g["COST"] = {"M2_mean_regret": sm["mean_regret"], "B5_mean_regret": sb["mean_regret"], "M_V1_mean_regret": sv["mean_regret"], "M2_mean_cost": sm["mean_cost"], "B5_mean_cost": sb["mean_cost"],
                 "instances_M2_lower_regret": m_less, "instances_B5_lower_regret": b_less, "sign_test_p": pc, "M2_wall_ms": sm["wall_ms"], "B5_wall_ms": sb["wall_ms"], "flag": flag,
                 "rule": "paired sign test on per-instance regret (registered cost units) at p <= 0.05; wall-clock reported only"}

    # ---- routes ------------------------------------------------------------------------------------
    if not g0:
        route, reason = "CANNOT_CHECK", "G0 provenance/generator/oracle/null validity failed: lane defect, repair and re-freeze"
    elif g1a:
        route, reason = "PARENT_SUFFICIENT", "B5 reproduces M2's intervention decisions (the improved rendering of ORION's unfixed orderings is reproduced by an exact planner)"
    elif g1b:
        if not g["G2_ANTI_ESCALATION"]["pass"]:
            route, reason = "M2_OVER_ESCALATES", "M2 advantage coexists with more false escalation or specification damage than B5 or than V1's M"
        elif not g3["pass"]:
            route, reason = "CANNOT_CHECK", "M2 advantage not attributable to locus diagnosis (G3 failed)"
        elif flag == "COST_ADVANTAGE_B5":
            route, reason = "QUALITY_COST_TRADEOFF_NO_DOMINANCE", "M2 advantage on minimal-level decisions but B5 significantly lower regret: no frontier dominance"
        else:
            route, reason = "ME_X2_RESIDUAL_CANDIDATE", "M2 advantage, anti-escalation, mediation attributed, not cost-dominated"
    elif g1c:
        route, reason = "PARENT_SUFFICIENT", "B5 dominates M2 on minimal-level decisions (B5_DOMINATES)"
    else:
        route, reason = "PARENT_SUFFICIENT", "no M2 advantage over B5 (discordance without significance)"

    if pv["diff_x_minus_y"] < 0 and pv["exact_p_two_sided"] <= 0.05:
        lever_verdict = "LEVERS_HARM"
    elif not (pv["diff_x_minus_y"] > 0 and pv["exact_p_two_sided"] <= 0.05):
        lever_verdict = "LEVERS_NULL"
    elif not g["G2_ANTI_ESCALATION"]["vs_M_V1_pass"] or len(only_v1) >= len(only_m2):
        lever_verdict = "LEVERS_MOVE_THE_FAILURE"
    elif not c_ok:
        lever_verdict = "LEVERS_NOT_ATTRIBUTED"   # M2 beats V1 for reasons the executed receipts do not attribute to either lever
    elif g1c:
        lever_verdict = "LEVERS_PARTIAL_RECOVERY"
    else:
        lever_verdict = "LEVERS_RECOVER_M"
    g["ROUTE"] = {"route": route, "reason": reason, "ladder_terminal": g["G4_INTERFACE_LADDER"]["terminal"], "cost_flag": flag, "b5_dominates": bool(g1c),
                  "lever_verdict": lever_verdict, "M2_decision_rate": m2_rate, "M_V1_decision_rate": sum(v1) / n if n else 0.0, "B5_decision_rate": sum(b5) / n if n else 0.0}
    return g


def render_md(analysis: dict) -> str:
    L = [f"# ME-X2 V2 revival analysis — {analysis['label']}\n"]
    if analysis["label"] != "PROTECTED":
        L.append(f"**{analysis['label']} split: not protected evidence. Numbers below cannot support any confirmatory claim.**\n")
    L.append(f"Results sha256 `{analysis['results_sha256']}`; custody sha256 `{analysis['custody_sha256']}`; instances {analysis['n_instances']}.\n")
    L.append("## Per-arm outcomes (S5)\n")
    L.append("| arm | decision (min-level) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | mean regret | mean cost | Brier | ECE5 | wall ms |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    f = lambda v: "n/a" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
    for a, s in analysis["score"]["per_arm"].items():
        L.append(f"| {a} | {f(s['decision_rate'])} | {f(s['class_rate'])} | {f(s['locus_rate'])} | {f(s['success_rate'])} | {s['false_escalation']} | {s['missed_escalation']} | {s['false_ci']} | {s['correct_ci']}/{s['n_ci_instances']} | {s['recurrence']} | {s['spec_damage']} | {f(s['mean_regret'])} | {f(s['mean_cost'])} | {f(s['brier'])} | {f(s['ece5'])} | {s['wall_ms']:.1f} |")
    arms = list(analysis["score"]["per_arm"])
    L.append("\n## Per-stratum decision-correct rate (stratum = oracle class)\n")
    L.append("| stratum | n | " + " | ".join(arms) + " |"); L.append("|---|---|" + "---|" * len(arms))
    for st in STRATA:
        v0 = analysis["score"]["per_arm"][arms[0]]["per_stratum"][st]
        L.append(f"| {st} | {v0['n']} | " + " | ".join("–" if analysis["score"]["per_arm"][a]["per_stratum"][st]["decision_rate"] is None else f"{analysis['score']['per_arm'][a]['per_stratum'][st]['decision_rate']:.2f}" for a in arms) + " |")
    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        if k not in ("ROUTE", "COST"):
            L.append(f"- **{k}**: pass={v.get('pass')} — {v.get('rule', '')}")
    r = analysis["gates"]["ROUTE"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}.\n")
    L.append(f"Lever verdict: `{r['lever_verdict']}` (M2 {r['M2_decision_rate']:.3f}, V1's M {r['M_V1_decision_rate']:.3f}, B5 {r['B5_decision_rate']:.3f}). "
             f"Ladder terminal: `{r['ladder_terminal']}`. Cost: `{r['cost_flag']}`.\n")
    return "\n".join(L)


# ---- stages ---------------------------------------------------------------------------------------

def _run_fixture_arms(inst: Instance, names: list[str]) -> dict:
    specs = {s.name: s for s in arm_specs()}
    return {nme: Environment(inst).run(make_policy(specs[nme], "selftest")).as_dict() for nme in names}


def lever_fixtures() -> dict:
    return json.loads(LEVER_FIXTURES.read_text())


def stage_selftest(out_dir: Path) -> int:
    prov = provenance.check()
    report: dict = {"schema_version": SCHEMA_ANALYSIS + ".selftest", "v1_provenance": prov, "parent_fidelity": fidelity_selftests(),
                    "known_answer": [], "separation": {}, "lever_known_answer": [], "oracle_agreement": None, "null_calibration": None}
    ok = bool(prov["all_match"]) and all(r["passed"] for r in report["parent_fidelity"])

    for fx in known_answer_fixtures():
        inst = fx["instance"]; orc = oracle_targets(inst)
        got = {k: orc[k] for k in fx["expected"]}
        passed = got == fx["expected"] and orc["exhaustive_agrees"]
        arms = _run_fixture_arms(inst, [M2_ARM, B5_ARM, M_V1_ARM])
        dec = {a: score_trajectory(t, orc, instance_to_json(inst))["decision_correct"] for a, t in arms.items()}
        passed &= dec[M2_ARM] and dec[B5_ARM]
        report["known_answer"].append({"name": fx["name"], "passed": bool(passed), "expected": fx["expected"], "oracle": got, "decision_correct": dec})
        ok &= passed

    sep_out = {}
    for case in separation_pair():
        inst = case["instance"]; orc = oracle_targets(inst)
        oracle_ok = {k: orc[k] for k in case["expected"]} == case["expected"]
        arms = _run_fixture_arms(inst, [LADDER[0], B5_ARM, M2_ARM])
        sep_out[case["name"]] = {"oracle_matches_hand_answer": oracle_ok, "arms": {a: score_trajectory(t, orc, instance_to_json(inst)) for a, t in arms.items()}}
        ok &= oracle_ok
    v1seq = [sep_out[c]["arms"][LADDER[0]]["decision_seq"] for c in ("SEP-P", "SEP-Q")]
    report["separation"] = {"verdict_only_outputs_identical_on_P_and_Q": v1seq[0] == v1seq[1],
                            "verdict_only_fails_at_least_one": not all(sep_out[c]["arms"][LADDER[0]]["decision_correct"] for c in ("SEP-P", "SEP-Q")),
                            "structure_exchange_exact_on_both": all(sep_out[c]["arms"][a]["decision_correct"] for c in ("SEP-P", "SEP-Q") for a in (B5_ARM, M2_ARM)),
                            "cases": {k: {"oracle_matches_hand_answer": v["oracle_matches_hand_answer"], "decision_correct": {a: s["decision_correct"] for a, s in v["arms"].items()}} for k, v in sep_out.items()}}
    report["separation"]["passed"] = bool(report["separation"]["verdict_only_outputs_identical_on_P_and_Q"] and report["separation"]["verdict_only_fails_at_least_one"] and report["separation"]["structure_exchange_exact_on_both"])
    ok &= report["separation"]["passed"]

    # V2 lever known-answer fixtures: the diagnosed failure shape, and the registered limits
    doc = lever_fixtures()
    for fx in doc["fixtures"]:
        inst = instance_from_json(fx["instance"]); orc = oracle_targets(inst)
        oracle_ok = {k: orc[k] for k in fx["expected_oracle"]} == fx["expected_oracle"] and orc["exhaustive_agrees"]
        got = {}
        for arm, exp in fx["expected_arms"].items():
            s = score_trajectory(_run_fixture_arms(inst, [arm])[arm], orc, instance_to_json(inst))
            got[arm] = {k: s[k] for k in exp}
        arms_ok = all(got[a] == exp for a, exp in fx["expected_arms"].items())
        passed = bool(oracle_ok and arms_ok)
        report["lever_known_answer"].append({"name": fx["name"], "registered_limit": fx["registered_limit"], "passed": passed, "oracle_matches": bool(oracle_ok), "arms": got})
        ok &= passed

    pairs = generate_split("selftest", "ME-X2-V2-SELFTEST", {s: 1 for s in STRATA})
    res, cus = run_instances(pairs, "SELFTEST", "ME-X2-V2-SELFTEST")
    sc = score_v2(res, cus)
    gt = gates_v2(sc, res, True, "SELFTEST", prov=prov)
    report["oracle_agreement"] = sc["g0b_all_agree"]; ok &= sc["g0b_all_agree"] and sc["variant_invariants_hold"]
    report["null_calibration"] = gt["G0c_NULL_CALIBRATION"]; ok &= gt["G0c_NULL_CALIBRATION"]["pass"]
    report["selftest_arm_decision_rates"] = {a: v["decision_rate"] for a, v in sc["per_arm"].items()}
    report["passed"] = bool(ok)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X2_V2_SELFTEST_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    print(f"selftest {'PASS' if ok else 'FAIL'}: V1 provenance {prov['all_match']}, parent tests {sum(r['passed'] for r in report['parent_fidelity'])}/{len(report['parent_fidelity'])}, "
          f"known-answer {sum(k['passed'] for k in report['known_answer'])}/{len(report['known_answer'])}, lever known-answer {sum(k['passed'] for k in report['lever_known_answer'])}/{len(report['lever_known_answer'])}, "
          f"separation {report['separation']['passed']}, oracle agreement {sc['g0b_all_agree']}, null calibration {gt['G0c_NULL_CALIBRATION']['pass']}")
    return 0 if ok else 1


def _run_split(label: str, split: str, split_seed: str, pairs_per_stratum: int, out_dir: Path, public_seed: str | None, only: tuple[str, ...] | None = None) -> int:
    pairs = generate_split(split, split_seed, {s: pairs_per_stratum for s in STRATA})
    res, cus = run_instances(pairs, label, public_seed, only=only)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X2_V2_{label}_RESULTS_V2.json"; cp = out_dir / f"ME_X2_V2_{label}_EXPECTED_CUSTODY_V2.json"; tp = out_dir / f"ME_X2_V2_{label}_TIMING_V2.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus))
    tp.write_text(canonical_json({"schema_version": SCHEMA_RESULTS + ".timing", "label": label, "wall_ns": timing, "note": "wall-clock is machine-dependent and is kept out of the deterministic results file"}))
    print(f"{label}: {len(pairs)} instances, results {rp} sha256 {sha256_file(rp)[:16]}…, custody {cp} sha256 {sha256_file(cp)[:16]}…")
    if only is not None:
        return 0
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, pairs_per_stratum: int) -> int:
    if pairs_per_stratum * len(STRATA) * 2 > DEV_CAP:
        print(f"development split is capped at {DEV_CAP} instances", file=sys.stderr); return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, pairs_per_stratum, out_dir, DEV_SEED)


def stage_g0scale(out_dir: Path, pairs_per_stratum: int, public_seed: str) -> int:
    """Protected-scale G0 coverage probe on a PUBLIC seed, with V1-known arms only.

    Decoy coverage and the null margins are properties of the generator, which G0d freezes
    byte-identical to V1's.  Running the probe with M_V1 and the two controls reproduces numbers
    that the V1 receipt already published, so it reveals nothing about the V2 comparison; the V2
    arms are deliberately excluded.  Never evidence for any arm claim.
    """
    if not public_seed or public_seed.startswith("ME-X2-V2-PROTECTED"):
        print("g0scale requires an explicitly public seed", file=sys.stderr); return 2
    pairs = generate_split("g0scale", public_seed, {s: pairs_per_stratum for s in STRATA})
    res, cus = run_instances(pairs, "G0SCALE", public_seed, only=G0SCALE_ARMS)
    res.pop("_timing_wall_ns", None)
    sc = score(res, cus)
    min_d = MIN_DECOYS["G0SCALE"]
    decoy_ok = all(sc["decoy_counts"].get(c, 0) >= min_d for c in CLASSES if (TYPICAL_LEVEL[c] or 0) >= 1)
    inverse_ok = all(sc["inverse_decoy_counts"].get(c, 0) >= min_d for c in CLASSES if TYPICAL_LEVEL[c] == 0) and sc["ci_apparent_identifiable"] >= min_d
    never = [r["decision_correct"] for r, ident in zip(sc["_rows"]["C_NEVER_INTERVENE"], sc["identifiable"]) if ident]
    rnd = _rate(sc["_rows"]["C_RANDOM_POLICY"])
    v1_rate = _rate(sc["_rows"][M_V1_ARM]); swap = sc["swap_null_M"]; swap_rate = sum(swap) / len(swap) if swap else 0.0
    rep = {"schema_version": SCHEMA_ANALYSIS + ".g0scale", "public_seed": public_seed, "n_instances": len(pairs), "arms": list(res["arms"]),
           "g0b": {"exhaustive_agrees_all": sc["g0b_all_agree"], "variant_invariants_hold": sc["variant_invariants_hold"], "decoy_coverage_ok": decoy_ok, "inverse_decoy_coverage_ok": inverse_ok,
                   "decoy_counts": sc["decoy_counts"], "inverse_decoy_counts": sc["inverse_decoy_counts"], "ci_apparent_identifiable": sc["ci_apparent_identifiable"]},
           "g0c_v1_arms_only": {"never_intervene_correct_on_identifiable": sum(never), "n_identifiable": len(never), "random_decision_rate": rnd,
                                "M_V1_decision_rate": v1_rate, "M_V1_within_pair_swap_rate": swap_rate, "margin_ok": bool(swap_rate <= v1_rate - SWAP_MARGIN)},
           "per_stratum_n": {st: sum(1 for s in sc["strata"] if s == st) for st in STRATA},
           "note": "coverage probe only; V2 arms excluded by construction; not evidence for any arm claim"}
    passed = bool(sc["g0b_all_agree"] and sc["variant_invariants_hold"] and decoy_ok and inverse_ok and sum(never) == 0 and rnd <= RANDOM_MAX and rep["g0c_v1_arms_only"]["margin_ok"])
    rep["passed"] = passed
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X2_V2_G0SCALE_PROBE_V2.json").write_text(json.dumps(rep, indent=2, sort_keys=True))
    print(f"g0scale {'PASS' if passed else 'FAIL'} on {len(pairs)} instances (public seed {public_seed}); decoys {rep['g0b']['decoy_coverage_ok']}, inverse {rep['g0b']['inverse_decoy_coverage_ok']}, random {rnd:.3f}")
    return 0 if passed else 1


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
        print("REFUSED: acknowledged_design_sha256 does not match the frozen V2 design JSON", file=sys.stderr); return 3
    if not provenance.check()["all_match"]:
        print("REFUSED: the frozen V1 lane has moved (G0d): V2 must compare against V1's world", file=sys.stderr); return 5
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
    sp = selftest_report if selftest_report else out_dir / "ME_X2_V2_SELFTEST_REPORT.json"
    selftest_ok = bool(json.loads(sp.read_text()).get("passed")) if sp.exists() else None
    sc = score_v2(res, cus, timing=timing)
    gt = gates_v2(sc, res, selftest_ok, label)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label, "results_sha256": sha256_file(results_path), "custody_sha256": sha256_file(custody_path), "n_instances": len(res["instances"]),
                "score": {"per_arm": sc["per_arm"], "decoy_counts": sc["decoy_counts"], "inverse_decoy_counts": sc["inverse_decoy_counts"],
                          "lever_activity": {"instances_with_l2_only_admissible_action": sum(1 for r in sc["lever_activity"] if r["l2_only_admissible"]),
                                             "instances_with_l1_changed_choice": sum(1 for r in sc["lever_activity"] if r["l1_changed_choice"]),
                                             "instances_with_permitted_foreclosure": sum(1 for r in sc["lever_activity"] if r["foreclosure_permitted"]),
                                             "instances_with_positive_expected_abstention": sum(1 for r in sc["lever_activity"] if r["expected_abstention_positive"]),
                                             "receipts_considered_not_executed": sum(r["considered_not_executed"] for r in sc["lever_activity"]),
                                             "receipts_executed": sum(r["executed_steps"] for r in sc["lever_activity"])}},
                "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X2_V2_{label}_ANALYSIS_V2.json").write_text(json.dumps(analysis, indent=2, sort_keys=True))
    (out_dir / f"ME_X2_V2_{label}_ANALYSIS_V2.md").write_text(render_md(analysis))
    r = gt["ROUTE"]
    print(f"{label} route: {r['route']} ({r['reason']}); lever verdict: {r['lever_verdict']}; ladder: {r['ladder_terminal']}; cost: {r['cost_flag']}; "
          f"M2 {r['M2_decision_rate']:.3f}, M_V1 {r['M_V1_decision_rate']:.3f}, B5 {r['B5_decision_rate']:.3f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "g0scale", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--pairs-per-stratum", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--public-seed", type=str, default=None)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.pairs_per_stratum or DEV_PAIRS_PER_STRATUM)
    if a.stage == "g0scale":
        if not a.public_seed:
            print("g0scale requires --public-seed", file=sys.stderr); return 2
        return stage_g0scale(a.out, a.pairs_per_stratum or PROTECTED_PAIRS_PER_STRATUM, a.public_seed)
    if a.stage == "protected":
        return stage_protected(a.out, a.pairs_per_stratum or PROTECTED_PAIRS_PER_STRATUM, a.seed_file)
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr); return 2
        return stage_analyze(a.results, a.custody, a.out, selftest_report=a.selftest_report)
    return 2


if __name__ == "__main__":
    sys.exit(main())
