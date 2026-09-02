#!/usr/bin/env python3
"""ME-X1 exact cross-transition coupling study runner (frozen with design V1).

Stages
  selftest   parent fidelity (native known-answer tests), G0a hand-authored
             known-answer fixtures (the 14 public development cases) and the
             H-EXT-3 separation pair, G0b oracle self-agreement on a small
             generated set, null calibration.
  dev        DEVELOPMENT split (public seed, <= 5 instances per family).
             Results are labelled DEVELOPMENT and are never protected evidence.
             Also derives the M_MINIMAL_RECEIPT atom-kind set (frozen into the
             design JSON before the protected run).
  protected  PROTECTED split. Refuses to run unless
             PROTECTED_RUN_AUTHORIZATION.json (human-written token) is present
             next to this script AND the custody seed file's sha256 equals the
             commitment frozen in the design JSON.
  analyze    Score a results file against its custody expected-decisions file:
             S7 outcomes per family, G0-G4 gates, pre-registered route.

Design: ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.{md,json}
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

from mex1_arms import ATOM_KINDS, ArmRunner, ArmView, arm_specs  # noqa: E402
from mex1_generator import generate_split, known_answer_fixtures, separation_pair, variant_for  # noqa: E402
from mex1_model import (  # noqa: E402
    ABSTAIN_AUTHORITY, BLOCK_TRANSPORT, DEFER_CANNOT_CHECK, FAMILIES, PRESERVE, SELECTIVELY_REOPEN, UPDATE, Instance,
    apply_event, canonical_json, instance_to_json,
)
from mex1_oracle import expected_for  # noqa: E402
from mex1_parents import fidelity_selftests  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x1.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x1.exact-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X1-DEV-20260902"
SELFTEST_SEED = "ME-X1-SELFTEST"
DEV_PER_FAMILY = 4            # 40 instances; cap 5 per family
PROTECTED_PER_FAMILY = 100    # 1000 instances
DEFAULT_SEED_FILE = Path(os.environ.get("MEX1_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x1/PROTECTED_SEED_V1.txt")))

M_ARM = "M_ME_TRANSITION_CONTROL"
B5_ARM = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
LADDER = ["B5_R1_VERDICT_ONLY", "B5_R2_PROV", "B5_R3_PROV+DEP", "B5_R4_PROV+DEP+TRANS+EVAL", B5_ARM]
ABLATION_FOR_FAMILY = {
    "X1-A_CLAIM_PROBLEM_IDENTITY": "M_MINUS_PROBLEM_IDENTITY",
    "X1-B_MEASUREMENT_CALIBRATION": "M_MINUS_MEASUREMENT_COMPARABILITY",
    "X1-C_HIDDEN_DEPENDENCE": "M_MINUS_DEPENDENCE",
    "X1-D_INVALID_TRANSPORT": "M_MINUS_TRANSPORT",
    "X1-E_DEFEATED_PREREQUISITE": "M_MINUS_SUPPORT_REOPENING",
    "X1-F_EVALUATOR_BLINDNESS": "M_MINUS_EVALUATOR_CONTRACT",
    "X1-G_AUTHORITY_MISMATCH": "M_MINUS_AUTHORITY",
    "X1-H_PROOF_WRONG_SPECIFICATION": "M_MINUS_PROBLEM_IDENTITY",
    "X1-I_LOCAL_COMPAT_GLOBAL_OBSTRUCTION": "M_MINUS_UNRESOLVED_TERMINAL",
    "X1-J_FULLY_WARRANTED": "M_MINUS_UNRESOLVED_TERMINAL",
}
WARRANTED = (UPDATE, PRESERVE)
CONSERVATIVE = (DEFER_CANNOT_CHECK, ABSTAIN_AUTHORITY)
# reverse precedence order for the minimal-receipt backward elimination
SHUFFLE_PERMUTATIONS = 200
MINIMAL_RECEIPT_ORDER = ("authority", "witness", "overlap", "piece", "evaluator", "evc", "tr", "transport", "ind", "support", "comparability", "cal", "ident", "src", "checker", "spec", "criterion", "identity", "nocontra")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def design() -> dict:
    return json.loads(DESIGN_JSON.read_text()) if DESIGN_JSON.exists() else {}


def minimal_receipt_kinds() -> tuple[str, ...]:
    return tuple(design().get("m_minimal_receipt", {}).get("dropped_atom_kinds", ()))


# ---- running arms over a split -------------------------------------------------

def _view(inst: Instance) -> ArmView:
    w = inst.world_v0
    for ev in inst.events:
        w = apply_event(w, ev)
    return ArmView(inst.world_v0, w, list(inst.events), inst.request, inst.world_v0.accepted_ids())


def run_instances(pairs: list[tuple[Instance, object]], label: str, split_seed_public: str | None, specs=None) -> tuple[dict, dict]:
    specs = specs or arm_specs(minimal_receipt_kinds())
    results = {"schema_version": SCHEMA_RESULTS, "label": label, "split_seed": split_seed_public, "arms": [s.name for s in specs], "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label, "instances": []}
    timing: dict[str, dict[str, int]] = {}
    for inst, exp in pairs:
        v = _view(inst)
        rec = {"instance_id": inst.instance_id, "family": inst.family, "variant": inst.variant, "seed": inst.seed, "request_kind": inst.request.kind, "accepted": list(v.accepted), "n_claims": len(inst.world_v0.claims), "n_events": len(inst.events), "features": inst.features, "arms": {}}
        for spec in specs:
            d, cost = ArmRunner(spec, inst.seed).run(v)
            rec["arms"][spec.name] = {"decision": d.as_dict(), "cost": {"engine_ops": cost.get("ops", 0), "module_ops": cost.get("module_ops", 0)}}
            timing.setdefault(inst.instance_id, {})[spec.name] = cost.get("wall_ns", 0)
        results["instances"].append(rec)
        custody["instances"].append({"instance_id": inst.instance_id, "family": inst.family, "variant": inst.variant, "expected": exp.as_dict(), "instance": instance_to_json(inst)})
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -----------------------------------------------------------------------

def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def paired_summary(x: list[bool], y: list[bool]) -> dict:
    n = len(x)
    b = sum(1 for a, bb in zip(x, y) if a and not bb)
    c = sum(1 for a, bb in zip(x, y) if bb and not a)
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {"n": n, "x_only": b, "y_only": c, "discordant": b + c, "diff_x_minus_y": diff, "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se], "exact_p_two_sided": exact_binomial_two_sided(b, c)}


OUTCOME_KEYS = ("false_update", "missed_warranted_update", "over_reopen", "under_reopen", "invalid_transport", "false_closure", "evaluator_laundering", "problem_spec_laundering", "authority_laundering", "correct_unresolved", "n_oracle_unresolved", "warranted_hit", "n_warranted", "unnecessary_defer", "n_not_conservative")


def _empty_counts() -> dict:
    return {"n": 0, "exact": 0, **{k: 0 for k in OUTCOME_KEYS}}


def score(results: dict, custody: dict, *, shuffle_seed: int = 20260902, timing: dict | None = None) -> dict:
    exp_by_id = {r["instance_id"]: r for r in custody["instances"]}
    timing = timing if timing is not None else results.get("_timing_wall_ns", {})
    arms = results["arms"]
    per_arm: dict[str, dict] = {a: {"instance_exact": [], "engine_ops": 0, "module_ops": 0, "wall_ns": 0, "total": _empty_counts(), "per_family": {f: _empty_counts() for f in FAMILIES}, "per_variant": {v: _empty_counts() for v in ("POSITIVE", "NEGATIVE", "AMBIGUITY")}} for a in arms}
    order: list[str] = []; families: list[str] = []
    oracle_actions: list[str] = []
    g0b_all_agree = True
    for rec in results["instances"]:
        iid = rec["instance_id"]; fam = rec["family"]; var = rec["variant"]; order.append(iid); families.append(fam)
        exp = exp_by_id[iid]["expected"]
        g0b_all_agree &= bool(exp["exhaustive_agrees"])
        oa, orr = exp["action"], set(exp["reopened"]); oracle_actions.append(oa)
        for a in arms:
            ar = rec["arms"][a]; pa = per_arm[a]
            d = ar["decision"]; aa, arr = d["action"], set(d["reopened"])
            ok = (aa == oa and arr == orr)
            pa["instance_exact"].append(ok)
            out = {k: 0 for k in OUTCOME_KEYS}
            out["false_update"] = int(aa == UPDATE and oa != UPDATE)
            out["missed_warranted_update"] = int(oa == UPDATE and aa != UPDATE)
            if oa == SELECTIVELY_REOPEN or aa == SELECTIVELY_REOPEN:
                out["over_reopen"] = len(arr - orr); out["under_reopen"] = len(orr - arr)
            out["invalid_transport"] = int(oa == BLOCK_TRANSPORT and aa == UPDATE)
            out["false_closure"] = int(oa == DEFER_CANNOT_CHECK and aa in WARRANTED)
            out["evaluator_laundering"] = int(exp["decisive_module"] == "EVAL" and aa == UPDATE)
            out["problem_spec_laundering"] = int(exp["decisive_module"] == "IDENT" and aa == UPDATE)
            out["authority_laundering"] = int(oa == ABSTAIN_AUTHORITY and aa == UPDATE)
            out["n_oracle_unresolved"] = int(oa == DEFER_CANNOT_CHECK); out["correct_unresolved"] = int(oa == DEFER_CANNOT_CHECK and aa == DEFER_CANNOT_CHECK)
            out["n_warranted"] = int(oa in WARRANTED); out["warranted_hit"] = int(oa in WARRANTED and ok)
            out["n_not_conservative"] = int(oa not in CONSERVATIVE); out["unnecessary_defer"] = int(oa not in CONSERVATIVE and aa in CONSERVATIVE)
            for bucket in (pa["total"], pa["per_family"][fam], pa["per_variant"][var]):
                bucket["n"] += 1; bucket["exact"] += int(ok)
                for k in OUTCOME_KEYS:
                    bucket[k] += out[k]
            pa["engine_ops"] += ar["cost"]["engine_ops"]; pa["module_ops"] += ar["cost"]["module_ops"]; pa["wall_ns"] += timing.get(iid, {}).get(a, 0)
    # assigned-label null for M: mean exact agreement of M's decisions with the
    # oracle decisions permuted across instances (200 permutations, fixed seed)
    shuffled_exact_M: list[bool] = []
    if M_ARM in arms and len(order) > 1:
        rng = random.Random(shuffle_seed)
        decisions = [(exp_by_id[i]["expected"]["action"], tuple(exp_by_id[i]["expected"]["reopened"])) for i in order]
        m_dec = [(rec["arms"][M_ARM]["decision"]["action"], tuple(rec["arms"][M_ARM]["decision"]["reopened"])) for rec in results["instances"]]
        for _ in range(SHUFFLE_PERMUTATIONS):
            perm = list(range(len(order))); rng.shuffle(perm)
            shuffled_exact_M.extend(m_dec[i] == decisions[j] for i, j in enumerate(perm))
    n = len(order)
    freq = {a: oracle_actions.count(a) / n for a in set(oracle_actions)} if n else {}
    chance = sum(p * p for p in freq.values())

    def rates(b: dict) -> dict:
        return dict(b, exact_rate=(b["exact"] / b["n"] if b["n"] else None), correct_unresolved_rate=(b["correct_unresolved"] / b["n_oracle_unresolved"] if b["n_oracle_unresolved"] else None), warranted_recall=(b["warranted_hit"] / b["n_warranted"] if b["n_warranted"] else None), unnecessary_defer_rate=(b["unnecessary_defer"] / b["n_not_conservative"] if b["n_not_conservative"] else None))
    summary = {}
    for a, pa in per_arm.items():
        summary[a] = {"n": n, "instance_exact_rate": (sum(pa["instance_exact"]) / n) if n else None, **{k: v for k, v in rates(pa["total"]).items() if k not in ("n", "exact")}, "engine_ops": pa["engine_ops"], "module_ops": pa["module_ops"], "wall_ms": pa["wall_ns"] / 1e6, "per_family": {f: rates(b) for f, b in pa["per_family"].items()}, "per_variant": {v: rates(b) for v, b in pa["per_variant"].items()}}
    return {"per_arm": summary, "_raw": per_arm, "order": order, "families": families, "oracle_actions": oracle_actions, "g0b_all_agree": g0b_all_agree, "shuffled_exact_M": shuffled_exact_M, "oracle_action_frequencies": freq, "chance_agreement": chance}


def gates(sc: dict, results: dict, selftest_ok: bool | None) -> dict:
    raw = sc["_raw"]; fams = sc["families"]; oa = sc["oracle_actions"]; n = len(sc["order"])
    g: dict = {}
    shuffled = sc["shuffled_exact_M"]; shuffle_rate = (sum(shuffled) / len(shuffled)) if shuffled else 0.0
    upd = raw["C_ALWAYS_UPDATE"]["instance_exact"]; dfr = raw["C_ALWAYS_DEFER"]["instance_exact"]; rnd = raw["C_RANDOM_ACTION"]["instance_exact"]
    upd_where_change = [x for x, a in zip(upd, oa) if a not in WARRANTED]
    dfr_where_determinate = [x for x, a in zip(dfr, oa) if a != DEFER_CANNOT_CHECK]
    g["G0a_KNOWN_ANSWER"] = {"pass": selftest_ok, "rule": "14 public development fixtures + separation pair reproduced by the oracle; M and B5 exact on all of them (selftest)"}
    g["G0b_ORACLE_SELF_AGREEMENT"] = {"pass": bool(sc["g0b_all_agree"]), "rule": "precedence walk / Kleene support == exhaustive enumeration on every instance; every instance valid at v0; family invariants satisfied at generation"}
    g["G0c_NULL_CALIBRATION"] = {
        "pass": bool(sum(upd_where_change) == 0 and sum(dfr_where_determinate) == 0 and (sum(rnd) / n if n else 0) <= 0.20 and shuffle_rate <= 0.35),
        "always_update_exact_where_oracle_not_warranted": sum(upd_where_change), "n_not_warranted": len(upd_where_change),
        "always_defer_exact_where_oracle_determinate": sum(dfr_where_determinate), "n_determinate": len(dfr_where_determinate),
        "random_exact_rate": (sum(rnd) / n) if n else None, "assigned_label_shuffle_exact_rate_M": shuffle_rate, "shuffle_n": len(shuffled), "chance_agreement": sc["chance_agreement"],
        "rule": "C_ALWAYS_UPDATE exact = 0 where the oracle is not UPDATE/PRESERVE; C_ALWAYS_DEFER exact = 0 where the oracle is determinate; C_RANDOM exact <= 20%; M vs permuted oracle decisions (mean over 200 permutations) exact <= 35% (chance = sum of squared action frequencies, reported)",
    }
    g0 = bool(g["G0a_KNOWN_ANSWER"]["pass"]) and g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"]
    m = raw[M_ARM]["instance_exact"]; b5 = raw[B5_ARM]["instance_exact"]
    ps = paired_summary(m, b5)
    identical = [rec["arms"][M_ARM]["decision"] == rec["arms"][B5_ARM]["decision"] for rec in results["instances"]]
    per_family_disc = {}
    for f in FAMILIES:
        idx = [i for i, ff in enumerate(fams) if ff == f]
        if idx:
            per_family_disc[f] = {"n": len(idx), "decision_discordant": sum(1 for i in idx if not identical[i]), "M_only_exact": sum(1 for i in idx if m[i] and not b5[i]), "B5_only_exact": sum(1 for i in idx if b5[i] and not m[i])}
    disc_rate = 1 - sum(identical) / n if n else 0.0
    g1a = disc_rate <= 0.005 and all(v["decision_discordant"] / v["n"] <= 0.05 for v in per_family_disc.values())
    g1b = ps["diff_x_minus_y"] > 0 and ps["exact_p_two_sided"] <= 0.05 and any(v["M_only_exact"] >= 5 for v in per_family_disc.values())
    g["G1a_B5_REPRODUCES_M"] = {"pass": bool(g1a), "decision_identity_rate": 1 - disc_rate, "per_family": per_family_disc, "rule": "M and B5 transition decisions identical on >= 99.5% of instances and no family > 5% discordant"}
    g["G1b_M_ADVANTAGE"] = {"pass": bool(g1b), "paired": ps, "rule": "paired exact-transition difference (M - B5) > 0, exact two-sided p <= 0.05, >= 1 family with >= 5 M-only-exact instances"}
    mt = sc["per_arm"][M_ARM]; bt = sc["per_arm"][B5_ARM]
    g2 = (mt["unnecessary_defer"] <= bt["unnecessary_defer"]) and ((mt["warranted_recall"] or 0.0) >= (bt["warranted_recall"] or 0.0))
    g["G2_ANTI_CONSERVATISM"] = {"pass": bool(g2), "M_unnecessary_defer": mt["unnecessary_defer"], "B5_unnecessary_defer": bt["unnecessary_defer"], "M_warranted_recall": mt["warranted_recall"], "B5_warranted_recall": bt["warranted_recall"], "n_warranted": mt["n_warranted"], "rule": "M's unnecessary defer/abstain count <= B5's and M's warranted-transition recall >= B5's (warranted = oracle UPDATE/PRESERVE: every NEGATIVE variant and family J)"}
    g3: dict = {"pass": None, "applicable": bool(g1b), "checks": {}}
    if g1b:
        ok = True
        for f, v in per_family_disc.items():
            if v["M_only_exact"] >= 5:
                abl = ABLATION_FOR_FAMILY[f]
                abl_rate = sc["per_arm"][abl]["per_family"][f]["exact_rate"] or 0.0; b5_rate = sc["per_arm"][B5_ARM]["per_family"][f]["exact_rate"] or 0.0
                vanish = abl_rate <= b5_rate
                g3["checks"][f] = {"ablation": abl, "ablation_exact_rate": abl_rate, "B5_exact_rate": b5_rate, "advantage_vanishes": vanish}
                ok &= vanish
        g3["pass"] = ok
    g3["rule"] = "each family with a claimed M advantage: the matching omission ablation's exact rate on that family <= B5's (A,H->PROBLEM_IDENTITY; B->MEASUREMENT_COMPARABILITY; C->DEPENDENCE; D->TRANSPORT; E->SUPPORT_REOPENING; F->EVALUATOR_CONTRACT; G->AUTHORITY; I,J->UNRESOLVED_TERMINAL)"
    g["G3_MECHANISM"] = g3
    rung_rates = [sc["per_arm"][r]["instance_exact_rate"] for r in LADDER]
    steps = []; monotone = True
    for k in range(4):
        p = paired_summary(raw[LADDER[k + 1]]["instance_exact"], raw[LADDER[k]]["instance_exact"])
        violated = p["diff_x_minus_y"] < 0 and p["exact_p_two_sided"] <= 0.05
        monotone &= not violated
        steps.append({"from": LADDER[k], "to": LADDER[k + 1], "paired": p, "violation": violated})
    gap_null = not g1b
    g["G4_INTERFACE_LADDER"] = {"pass": bool(monotone), "rung_exact_rates": dict(zip(LADDER, rung_rates)), "steps": steps, "rung5_gap": ps, "rung5_gap_null": gap_null,
                                "terminal": ("RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL" if (monotone and gap_null) else "CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE" if (monotone and not gap_null) else "LADDER_NON_MONOTONE"),
                                "rule": "H-EXT-3: no rung k+1 significantly worse than rung k (paired exact p <= 0.05 in the wrong direction is a violation); rung-5 gap = the G1 paired test"}
    m_ms = mt["wall_ms"]; b_ms = bt["wall_ms"]
    g["COST"] = {"M_ops": mt["engine_ops"] + mt["module_ops"], "B5_ops": bt["engine_ops"] + bt["module_ops"], "M_wall_ms": m_ms, "B5_wall_ms": b_ms, "ratio_B5_over_M_wall": (b_ms / m_ms) if m_ms else None,
                 "flag": ("COST_ADVANTAGE_M" if m_ms and b_ms > 2 * m_ms else "COST_ADVANTAGE_B5" if b_ms and m_ms > 2 * b_ms else "COST_PARITY_WITHIN_2X"),
                 "rule": "wall-clock flag at 2x; engine op counts engine-native and reported only; never a route by itself"}
    if not g0:
        route, reason = "CANNOT_CHECK", "G0 generator/oracle validity failed: lane defect, repair and re-freeze"
    elif g1a:
        route, reason = "PARENT_SUFFICIENT", "B5 reproduces M's transition decisions"
    elif g1b:
        if not g["G2_ANTI_CONSERVATISM"]["pass"]:
            route, reason = "M_OVER_CONSERVATIVE", "M advantage coexists with unnecessary deferral / lower warranted recall"
        elif g3["pass"]:
            route, reason = "ME_X1_RESIDUAL_CANDIDATE", "M advantage, anti-conservative, mechanism attributed by omission ablation"
        else:
            route, reason = "CANNOT_CHECK", "M advantage not attributable to a named cross-transition condition (G3 failed)"
    else:
        route, reason = "PARENT_SUFFICIENT", "no M advantage over B5 (B5 not worse, or discordance without significance)"
    g["ROUTE"] = {"route": route, "reason": reason, "ladder_terminal": g["G4_INTERFACE_LADDER"]["terminal"], "cost_flag": g["COST"]["flag"]}
    return g


def render_md(analysis: dict) -> str:
    L = [f"# ME-X1 analysis — {analysis['label']}\n"]
    if analysis["label"] == "DEVELOPMENT":
        L.append("**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**\n")
    L.append(f"Results sha256 `{analysis['results_sha256']}`; custody sha256 `{analysis['custody_sha256']}`; instances {analysis['n_instances']}.\n")
    L.append("## Per-arm outcome vector (S7)\n")
    cols = ["exact", "false upd.", "missed warr.", "over-reopen", "under-reopen", "inv. transport", "false closure", "eval. laund.", "prob/spec laund.", "auth. laund.", "correct unres.", "warr. recall", "unnec. defer", "ops", "wall ms"]
    L.append("| arm | " + " | ".join(cols) + " |"); L.append("|---|" + "---|" * len(cols))
    for a, s in analysis["score"]["per_arm"].items():
        cu = "n/a" if s["correct_unresolved_rate"] is None else f"{s['correct_unresolved_rate']:.2f}"
        wr = "n/a" if s["warranted_recall"] is None else f"{s['warranted_recall']:.3f}"
        ud = "n/a" if s["unnecessary_defer_rate"] is None else f"{s['unnecessary_defer_rate']:.3f}"
        L.append(f"| {a} | {s['instance_exact_rate']:.3f} | {s['false_update']} | {s['missed_warranted_update']} | {s['over_reopen']} | {s['under_reopen']} | {s['invalid_transport']} | {s['false_closure']} | {s['evaluator_laundering']} | {s['problem_spec_laundering']} | {s['authority_laundering']} | {cu} | {wr} | {ud} | {s['engine_ops'] + s['module_ops']} | {s['wall_ms']:.1f} |")
    L.append("\n## Per-family exact-transition rate\n")
    arms = list(analysis["score"]["per_arm"])
    L.append("| family | " + " | ".join(arms) + " |"); L.append("|---|" + "---|" * len(arms))
    for f in FAMILIES:
        row = []
        for a in arms:
            v = analysis["score"]["per_arm"][a]["per_family"][f]
            row.append("–" if v["exact_rate"] is None else f"{v['exact_rate']:.2f}")
        L.append(f"| {f} | " + " | ".join(row) + " |")
    L.append("\n## Per-variant exact-transition rate\n")
    L.append("| variant | " + " | ".join(arms) + " |"); L.append("|---|" + "---|" * len(arms))
    for vname in ("POSITIVE", "NEGATIVE", "AMBIGUITY"):
        row = []
        for a in arms:
            v = analysis["score"]["per_arm"][a]["per_variant"][vname]
            row.append("–" if v["exact_rate"] is None else f"{v['exact_rate']:.2f}")
        L.append(f"| {vname} | " + " | ".join(row) + " |")
    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        if k != "ROUTE":
            L.append(f"- **{k}**: pass={v.get('pass')} — {v.get('rule', '')}")
    r = analysis["gates"]["ROUTE"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}. Ladder terminal: `{r['ladder_terminal']}`. Cost: `{r['cost_flag']}`.\n")
    return "\n".join(L)


# ---- stages ---------------------------------------------------------------------------

def _decision_of(arm_name: str, w0, events, request, seed: int = 7):
    spec = {s.name: s for s in arm_specs(minimal_receipt_kinds())}[arm_name]
    w = w0
    for ev in events:
        w = apply_event(w, ev)
    d, _ = ArmRunner(spec, seed).run(ArmView(w0, w, list(events), request, w0.accepted_ids()))
    return d


def stage_selftest(out_dir: Path) -> int:
    report: dict = {"schema_version": SCHEMA_ANALYSIS + ".selftest", "parent_fidelity": fidelity_selftests(), "known_answer": [], "separation": {}, "oracle_agreement": None, "null_calibration": None}
    ok = all(r["passed"] for r in report["parent_fidelity"])
    for f in known_answer_fixtures():
        _w, exp = expected_for(f["world"], f["events"], f["request"])
        want_re = tuple(f.get("expected_reopened", ())) if f["expected"] == SELECTIVELY_REOPEN else ()
        passed = exp.action == f["expected"] and exp.reopened == want_re and exp.exhaustive_agrees and f["expected"] not in f.get("forbidden", [])
        arms_ok = {}
        for arm in (M_ARM, B5_ARM):
            d = _decision_of(arm, f["world"], f["events"], f["request"])
            arms_ok[arm] = (d.action == exp.action and tuple(d.reopened) == exp.reopened)
        passed &= all(arms_ok.values())
        report["known_answer"].append({"case_id": f["case_id"], "family": f["family"], "passed": passed, "expected": f["expected"], "oracle": exp.action, "oracle_reopened": list(exp.reopened), "arms_exact": arms_ok})
        ok &= passed
    sep = separation_pair(); sep_out = {}
    for case in sep:
        _w, exp = expected_for(case["world"], case["events"], case["request"])
        sep_out[case["name"]] = {"expected": case["expected"], "oracle": exp.action, "oracle_reopened": list(exp.reopened), "arms": {a: _decision_of(a, case["world"], case["events"], case["request"]).as_dict() for a in (LADDER[0], B5_ARM, M_ARM)}}
    p, q = sep_out["SEP-P"], sep_out["SEP-Q"]
    verdict_blind = p["arms"][LADDER[0]] == q["arms"][LADDER[0]]
    verdict_errs = (p["arms"][LADDER[0]]["action"] != p["oracle"]) or (q["arms"][LADDER[0]]["action"] != q["oracle"])
    structure_exact = all(sep_out[k]["arms"][a]["action"] == sep_out[k]["oracle"] and sep_out[k]["arms"][a]["reopened"] == sep_out[k]["oracle_reopened"] for k in sep_out for a in (B5_ARM, M_ARM))
    oracle_ok = p["oracle"] == SELECTIVELY_REOPEN and p["oracle_reopened"] == ["c"] and q["oracle"] == PRESERVE
    report["separation"] = {"cases": sep_out, "verdict_only_identical_on_P_and_Q": verdict_blind, "verdict_only_errs": verdict_errs, "structure_exchange_exact": structure_exact, "passed": bool(verdict_blind and verdict_errs and structure_exact and oracle_ok)}
    ok &= report["separation"]["passed"]
    pairs = generate_split("selftest", SELFTEST_SEED, {f: 1 for f in FAMILIES})
    res, cus = run_instances(pairs, "SELFTEST", SELFTEST_SEED)
    sc = score(res, cus)
    report["oracle_agreement"] = {"n": len(pairs), "all_agree": sc["g0b_all_agree"]}
    gt = gates(sc, res, True)
    report["null_calibration"] = gt["G0c_NULL_CALIBRATION"]
    report["m_b5_exact_on_selftest_split"] = {M_ARM: sc["per_arm"][M_ARM]["instance_exact_rate"], B5_ARM: sc["per_arm"][B5_ARM]["instance_exact_rate"]}
    ok &= bool(sc["g0b_all_agree"]) and bool(gt["G0c_NULL_CALIBRATION"]["pass"])
    report["passed"] = bool(ok)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X1_SELFTEST_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    n_par = len(report["parent_fidelity"]); n_par_ok = sum(r["passed"] for r in report["parent_fidelity"])
    print(f"selftest: parents {n_par_ok}/{n_par}; known-answer {sum(k['passed'] for k in report['known_answer'])}/{len(report['known_answer'])}; separation {report['separation']['passed']}; oracle agreement {sc['g0b_all_agree']}; null calibration {gt['G0c_NULL_CALIBRATION']['pass']}; PASSED={ok}")
    return 0 if ok else 1


def derive_minimal_receipt(pairs: list) -> tuple[str, ...]:
    """Frozen rule: backward elimination over atom kinds in reverse precedence
    order; a kind is dropped iff M restricted to the remaining kinds stays exact
    on every development instance. Deterministic; development-only."""
    from mex1_arms import ArmSpec, TYPED
    dropped: list[str] = []
    for kind in MINIMAL_RECEIPT_ORDER:
        trial = tuple(dropped + [kind])
        spec = ArmSpec("M_TRIAL", "M", dict(TYPED), "transition_control", dropped_kinds=trial)
        exact = True
        for inst, exp in pairs:
            d, _ = ArmRunner(spec, inst.seed).run(_view(inst))
            if (d.action, tuple(d.reopened)) != (exp.action, exp.reopened):
                exact = False; break
        if exact:
            dropped.append(kind)
    return tuple(dropped)


def _run_split(label: str, split: str, split_seed: str, per_family: int, out_dir: Path, public_seed: str | None) -> int:
    pairs = generate_split(split, split_seed, {f: per_family for f in FAMILIES})
    res, cus = run_instances(pairs, label, public_seed)
    timing = res.pop("_timing_wall_ns")
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X1_{label}_RESULTS_V1.json"; cp = out_dir / f"ME_X1_{label}_EXPECTED_CUSTODY_V1.json"; tp = out_dir / f"ME_X1_{label}_TIMING_V1.json"
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus)); tp.write_text(canonical_json({"schema_version": SCHEMA_RESULTS + ".timing", "label": label, "wall_ns": timing, "note": "wall-clock is machine-dependent and is kept out of the deterministic results file"}))
    print(f"{label}: {len(pairs)} instances, results {rp} sha256 {sha256_file(rp)[:16]}…, custody {cp} sha256 {sha256_file(cp)[:16]}…")
    if label == "DEVELOPMENT":
        dropped = derive_minimal_receipt(pairs)
        mp = out_dir / "ME_X1_DEVELOPMENT_MINIMAL_RECEIPT_V1.json"
        mp.write_text(json.dumps({"schema_version": SCHEMA_ANALYSIS + ".minimal-receipt", "rule": "backward elimination over atom kinds in reverse precedence order; drop iff M stays exact on every development instance", "order": list(MINIMAL_RECEIPT_ORDER), "dropped_atom_kinds": list(dropped), "kept_atom_kinds": [k for k in ATOM_KINDS if k not in dropped], "frozen_in_design_json": list(minimal_receipt_kinds())}, indent=2, sort_keys=True))
        print(f"DEVELOPMENT minimal receipt: dropped {list(dropped)} (design JSON freezes {list(minimal_receipt_kinds())})")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_family: int) -> int:
    if per_family > 5:
        print("development split is capped at 5 instances per family", file=sys.stderr); return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_family, out_dir, DEV_SEED)


def stage_protected(out_dir: Path, per_family: int, seed_file: Path) -> int:
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
    commitment = design()["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed).hexdigest() != commitment:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr); return 4
    return _run_split("PROTECTED", "protected", seed.decode(), per_family, out_dir, None)


def stage_analyze(results_path: Path, custody_path: Path, out_dir: Path, label: str | None = None, selftest_report: Path | None = None) -> int:
    res = json.loads(results_path.read_text()); cus = json.loads(custody_path.read_text())
    label = label or res.get("label", "UNKNOWN")
    tp = results_path.with_name(results_path.name.replace("_RESULTS_", "_TIMING_"))
    timing = json.loads(tp.read_text()).get("wall_ns", {}) if tp.exists() else {}
    selftest_ok = None
    sp = selftest_report if (selftest_report and selftest_report.exists()) else out_dir / "ME_X1_SELFTEST_REPORT.json"
    if sp.exists():
        selftest_ok = bool(json.loads(sp.read_text()).get("passed"))
    sc = score(res, cus, timing=timing)
    gt = gates(sc, res, selftest_ok)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label, "results_sha256": sha256_file(results_path), "custody_sha256": sha256_file(custody_path), "n_instances": len(res["instances"]), "oracle_action_frequencies": sc["oracle_action_frequencies"], "score": {"per_arm": sc["per_arm"]}, "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X1_{label}_ANALYSIS_V1.json").write_text(json.dumps(analysis, indent=2, sort_keys=True))
    (out_dir / f"ME_X1_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    print(f"{label} route: {gt['ROUTE']['route']} ({gt['ROUTE']['reason']}); ladder: {gt['ROUTE']['ladder_terminal']}; M exact {sc['per_arm'][M_ARM]['instance_exact_rate']:.3f}, B5 exact {sc['per_arm'][B5_ARM]['instance_exact_rate']:.3f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-family", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_family or DEV_PER_FAMILY)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_family or PROTECTED_PER_FAMILY, a.seed_file)
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr); return 2
        return stage_analyze(a.results, a.custody, a.out, selftest_report=a.selftest_report)
    return 2


if __name__ == "__main__":
    sys.exit(main())
