#!/usr/bin/env python3
"""ME-X5 cross-domain field residual test: runner (frozen with design V1).

Stages
  selftest   parent fidelity, hand-authored known-answer fixtures, the H-EXT-3
             separation pair, oracle validity and null calibration on a small
             public split.
  dev        DEVELOPMENT split (public seed, <= 40 instances). Never protected
             evidence.
  protected  PROTECTED split. Refuses unless PROTECTED_RUN_AUTHORIZATION.json
             (human-written token, acknowledged design sha256) sits next to this
             script AND the custody seed hashes to the frozen commitment.
  analyze    Score a results file against its custody file: the §6 outcome vector
             per mode, gates G0-G5, the pre-registered route and field-ladder rung.

Design: ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.{md,json}
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

import mex5_native_formal as NF  # noqa: E402
import mex5_native_measurement as NM  # noqa: E402
import mex5_native_synthesis as NS  # noqa: E402
import mex5_vocab as VOCAB  # noqa: E402
from mex5_arms import B5_ARM, LADDER, M_ARM, arm_specs, final_state, run_arm  # noqa: E402
from mex5_generator import (  # noqa: E402
    STRATUM_INVARIANT,
    generate_split,
    known_answer_fixtures,
    separation_pair,
)
from mex5_model import MODES, STRATA, canonical_json, episode_to_json  # noqa: E402
from mex5_oracle import (  # noqa: E402
    MAX_CENSORED_FACTS,
    censored_facts,
    oracle_trajectory,
    permutation_invariant,
    valid_at_v0,
)
from mex5_parents import fidelity_selftests  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x5.cross-domain-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x5.cross-domain-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X5-DEV-20260902"
DEV_PER_CELL = 1              # 36 instances <= 40
PROTECTED_PER_CELL = 40       # 3 modes x 12 strata x 40 = 1440
SHUFFLE_SEED = 20260902
EQUIVALENCE_MARGIN_PER_MODE = 0.02
EQUIVALENCE_MARGIN_POOLED = 0.01
DEFAULT_SEED_FILE = Path(os.environ.get(
    "MEX5_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x5/PROTECTED_SEED_V1.txt")))

NATIVE_REVIEWS = {"FORMAL": NF.NATIVE_REVIEW, "MEASUREMENT": NM.NATIVE_REVIEW, "SYNTHESIS": NS.NATIVE_REVIEW}
NATIVE_REVIEW_REQUIRED_KEYS = (
    "native_objects_and_vocabulary", "strongest_native_methods", "valid_and_invalid_transitions",
    "native_failure_classes", "evaluator_assumptions", "lossy_or_invalid_ME_abstractions",
    "strongest_plausible_parent_composition",
)
# G2 conservative strata: nothing should be withheld or abstained on these.
G2_STRATA = ("FULLY_WARRANTED_CONTROL", "AUTHORITY_MISMATCH", "SINGLE_PARENT_SUFFICIENT")
ABLATION_FOR_LOCUS = {
    "TARGET_IDENTITY": "M_MINUS_IDENTITY", "APPARATUS_VALIDITY": "M_MINUS_APPARATUS",
    "EVALUATOR_COVERAGE": "M_MINUS_EVALUATOR", "DEPENDENCE": "M_MINUS_DEPENDENCE",
    "TRANSPORT": "M_MINUS_TRANSPORT", "SCOPE": "M_MINUS_SCOPE",
    "GLOBAL_OBSTRUCTION": "M_MINUS_GLOBAL", "SUPPORT_DEFEAT": "M_MINUS_FAMILIES", "NONE": "M_MINUS_FAMILIES",
}
ABLATIONS = tuple(f"M_MINUS_{c.upper()}" for c in (
    "identity", "apparatus", "evaluator", "dependence", "transport", "scope", "global", "numeric",
    "families", "authority", "unresolved"))


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- statistics -------------------------------------------------------------------

def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def paired_summary(x: list[bool], y: list[bool]) -> dict:
    n = len(x)
    b = sum(1 for a, bb in zip(x, y) if a and not bb)
    c = sum(1 for a, bb in zip(x, y) if bb and not a)
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {"n": n, "x_only": b, "y_only": c, "discordant": b + c, "diff_x_minus_y": diff,
            "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se], "exact_p_two_sided": exact_binomial_two_sided(b, c)}


def holm(pvals: dict[str, float], alpha: float = 0.05) -> dict[str, bool]:
    order = sorted(pvals, key=lambda k: pvals[k])
    m = len(order)
    out, still = {}, True
    for i, k in enumerate(order):
        thresh = alpha / (m - i)
        still = still and pvals[k] <= thresh
        out[k] = bool(still)
    return out


# ---- running arms ------------------------------------------------------------------

def run_instances(pairs, label: str, split_seed_public: str | None):
    specs = arm_specs()
    results = {"schema_version": SCHEMA_RESULTS, "label": label, "split_seed": split_seed_public,
               "arms": [s.name for s in specs], "modes": list(MODES), "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label, "instances": []}
    timing: dict[str, dict[str, int]] = {}
    for ep, traj in pairs:
        st = final_state(ep)
        rng = random.Random(int(ep.seed, 16))
        rec = {"instance_id": ep.episode_id, "mode": ep.mode, "stratum": ep.stratum, "seed": ep.seed,
               "n_versions": len(traj), "n_units": len(st.units), "n_families": len(st.families),
               "n_censored_facts": len(censored_facts(st)), "features": ep.features or {},
               "changed_vocabulary_class": VOCAB.classify(st),
               "changed_vocabulary_class_scrambled": VOCAB.classify_scrambled(st),
               "arms": {}}
        for spec in specs:
            d, cost = run_arm(spec, st, rng)
            rec["arms"][spec.name] = {"decision": d.as_dict(), "ops": cost["ops"]}
            timing.setdefault(ep.episode_id, {})[spec.name] = cost["wall_ns"]
        results["instances"].append(rec)
        custody["instances"].append({
            "instance_id": ep.episode_id, "mode": ep.mode, "stratum": ep.stratum,
            "expected": [v.as_dict() for v in traj], "episode": episode_to_json(ep),
        })
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring ------------------------------------------------------------------------

OUTCOME_KEYS = ("false_transition", "missed_warranted_transition", "responsibility_error", "invalid_transport_accepted",
                "false_closure_over_unresolved", "unnecessary_abstention", "missed_necessary_abstention",
                "narrowing_error", "authority_violation")


def _blank(strata_keys):
    return {"n": 0, "decision_exact": 0, "action_exact": 0, "locus_exact": 0, "authority_exact": 0,
            **{k: 0 for k in OUTCOME_KEYS}, "ops": 0, "wall_ns": 0,
            "per_stratum": {s: {"n": 0, "exact": 0, "false_transition": 0, "unnecessary_abstention": 0,
                                "missed_warranted_transition": 0, "authority_violation": 0} for s in strata_keys}}


def score(results: dict, custody: dict, *, timing: dict | None = None, shuffle_seed: int = SHUFFLE_SEED) -> dict:
    exp_by_id = {r["instance_id"]: r for r in custody["instances"]}
    timing = timing if timing is not None else results.get("_timing_wall_ns", {})
    arms = results["arms"]
    per: dict[str, dict[str, dict]] = {a: {m: _blank(STRATA) for m in list(MODES) + ["POOLED"]} for a in arms}
    exact_vec: dict[str, dict[str, list[bool]]] = {a: {m: [] for m in list(MODES) + ["POOLED"]} for a in arms}
    order: dict[str, list[str]] = {m: [] for m in list(MODES) + ["POOLED"]}
    vocab: dict[str, dict] = {m: {"n": 0, "recovered": 0, "shuffled": 0, "scrambled_adapter": 0} for m in MODES}
    oracle_loci: dict[str, list[str]] = {m: [] for m in MODES}
    vocab_pred: dict[str, list[str]] = {m: [] for m in MODES}
    m_true: dict[str, list[str]] = {m: [] for m in MODES}
    m_pred: dict[str, list[str]] = {m: [] for m in MODES}
    for rec in results["instances"]:
        mode, st = rec["mode"], rec["stratum"]
        exp = exp_by_id[rec["instance_id"]]["expected"][-1]["decision"]
        order[mode].append(rec["instance_id"]); order["POOLED"].append(rec["instance_id"])
        if exp["action"] != "UNRESOLVED":
            vocab[mode]["n"] += 1
            vocab[mode]["recovered"] += int(rec["changed_vocabulary_class"] == exp["locus"])
            vocab[mode]["scrambled_adapter"] += int(rec["changed_vocabulary_class_scrambled"] == exp["locus"])
            oracle_loci[mode].append(exp["locus"]); vocab_pred[mode].append(rec["changed_vocabulary_class"])
        m_true[mode].append(json.dumps(exp, sort_keys=True))
        m_pred[mode].append(json.dumps(rec["arms"][M_ARM]["decision"], sort_keys=True))
        for a in arms:
            got = rec["arms"][a]["decision"]
            for scope in (mode, "POOLED"):
                p = per[a][scope]
                p["n"] += 1
                ex = got == exp
                p["decision_exact"] += int(ex)
                p["action_exact"] += int(got["action"] == exp["action"])
                p["locus_exact"] += int(got["locus"] == exp["locus"])
                p["authority_exact"] += int(got["authority"] == exp["authority"])
                committed = got["action"] in ("COMMIT", "COMMIT_NARROWED")
                exp_commit = exp["action"] in ("COMMIT", "COMMIT_NARROWED")
                p["false_transition"] += int(committed and exp["action"] == "WITHHOLD")
                p["missed_warranted_transition"] += int(exp_commit and got["action"] in ("WITHHOLD", "UNRESOLVED"))
                p["responsibility_error"] += int(exp["locus"] != "NONE" and got["locus"] != exp["locus"])
                p["invalid_transport_accepted"] += int(committed and exp["locus"] == "TRANSPORT")
                p["false_closure_over_unresolved"] += int(got["action"] != "UNRESOLVED" and exp["action"] == "UNRESOLVED")
                p["unnecessary_abstention"] += int(got["action"] == "UNRESOLVED" and exp["action"] != "UNRESOLVED")
                p["missed_necessary_abstention"] += int(got["action"] != "UNRESOLVED" and exp["action"] == "UNRESOLVED")
                p["narrowing_error"] += int(committed and exp_commit and got["action"] != exp["action"])
                p["authority_violation"] += int(got["authority"] == "BELIEF_AND_ACTION" and exp["authority"] == "BELIEF_ONLY")
                p["ops"] += rec["arms"][a]["ops"]
                p["wall_ns"] += timing.get(rec["instance_id"], {}).get(a, 0)
                ps = p["per_stratum"][st]
                ps["n"] += 1; ps["exact"] += int(ex)
                ps["false_transition"] += int(committed and exp["action"] == "WITHHOLD")
                ps["unnecessary_abstention"] += int(got["action"] == "UNRESOLVED" and exp["action"] != "UNRESOLVED")
                ps["missed_warranted_transition"] += int(exp_commit and got["action"] in ("WITHHOLD", "UNRESOLVED"))
                ps["authority_violation"] += int(got["authority"] == "BELIEF_AND_ACTION" and exp["authority"] == "BELIEF_ONLY")
                exact_vec[a][scope].append(ex)
    # within-mode shuffled-label nulls
    rng = random.Random(shuffle_seed)
    shuffled_M: dict[str, float] = {}
    shuffled_vocab: dict[str, float] = {}
    for m in MODES:
        lab = list(m_true[m]); rng.shuffle(lab)
        shuffled_M[m] = sum(1 for a, b in zip(m_pred[m], lab) if a == b) / len(lab) if lab else 0.0
        lab2 = list(oracle_loci[m]); rng.shuffle(lab2)
        shuffled_vocab[m] = sum(1 for a, b in zip(vocab_pred[m], lab2) if a == b) / len(lab2) if lab2 else 0.0
        vocab[m]["shuffled"] = shuffled_vocab[m]
    summary = {}
    for a in arms:
        summary[a] = {}
        for scope, p in per[a].items():
            n = p["n"] or 1
            summary[a][scope] = {
                "n": p["n"], "decision_exact_rate": p["decision_exact"] / n,
                "action_exact_rate": p["action_exact"] / n, "locus_exact_rate": p["locus_exact"] / n,
                "authority_exact_rate": p["authority_exact"] / n,
                **{k: p[k] for k in OUTCOME_KEYS}, "ops": p["ops"], "wall_ms": p["wall_ns"] / 1e6,
                "per_stratum": {s: dict(v, exact_rate=(v["exact"] / v["n"] if v["n"] else None))
                                for s, v in p["per_stratum"].items()},
            }
    return {"per_arm": summary, "_exact": exact_vec, "order": order,
            "changed_vocabulary": {m: dict(vocab[m],
                                           recovery_rate=(vocab[m]["recovered"] / vocab[m]["n"] if vocab[m]["n"] else None),
                                           scrambled_adapter_rate=(vocab[m]["scrambled_adapter"] / vocab[m]["n"] if vocab[m]["n"] else None),
                                           shuffled_label_rate=shuffled_vocab[m]) for m in MODES},
            "shuffled_label_rate_M": shuffled_M}


# ---- gates --------------------------------------------------------------------------

def gates(sc: dict, results: dict, selftest: dict | None) -> dict:
    ex = sc["_exact"]
    pa = sc["per_arm"]
    g: dict = {}
    st_ok = bool(selftest.get("passed")) if selftest else None
    g["G0a_NATIVE_KNOWN_ANSWER"] = {
        "pass": st_ok,
        "rule": "every parent passes its own native known-answer tests; the nine hand-authored fixtures and the H-EXT-3 separation pair are reproduced; the three native-review records are complete",
        "detail": {k: selftest.get(k) for k in ("parent_fidelity_passed", "known_answer_passed", "separation_passed",
                                                "native_review_complete")} if selftest else None,
    }
    g["G0b_ORACLE_VALIDITY"] = {
        "pass": bool(selftest.get("oracle_validity", {}).get("pass")) if selftest else None,
        "rule": "every instance: valid at v0, stratum invariant reproduced, censored facts within the frozen cap, decision invariant under a full relabelling of every element identifier",
        "detail": (selftest or {}).get("oracle_validity"),
    }
    ctrl = {c: pa[c]["POOLED"]["decision_exact_rate"] for c in
            ("C_ALWAYS_COMMIT", "C_NEVER_COMMIT", "C_ALWAYS_UNRESOLVED", "C_RANDOM_DECISION")}
    m_pooled = pa[M_ARM]["POOLED"]["decision_exact_rate"]
    shuf = sc["shuffled_label_rate_M"]
    g0c_ok = (all(v <= 0.25 for v in ctrl.values()) and ctrl["C_RANDOM_DECISION"] <= 0.05
              and all(shuf[m] <= pa[M_ARM][m]["decision_exact_rate"] - 0.50 for m in MODES))
    g["G0c_NULL_CALIBRATION"] = {
        "pass": bool(g0c_ok), "controls": ctrl, "shuffled_label_rate_M": shuf, "M_pooled": m_pooled,
        "rule": "every truth-agnostic control <= 0.25 decision-exact; C_RANDOM_DECISION <= 0.05; M scored against within-mode shuffled oracle decisions is at least 0.50 below M's own rate in every mode",
    }
    g0 = all(bool(g[k]["pass"]) for k in ("G0a_NATIVE_KNOWN_ANSWER", "G0b_ORACLE_VALIDITY", "G0c_NULL_CALIBRATION"))

    # G1 per mode, Holm across modes
    per_mode = {}
    p_adv, p_b5 = {}, {}
    for m in MODES:
        ps = paired_summary(ex[M_ARM][m], ex[B5_ARM][m])
        identical = sum(1 for i in range(len(ex[M_ARM][m])) if ex[M_ARM][m][i] == ex[B5_ARM][m][i])
        n = len(ex[M_ARM][m]) or 1
        recs = [r for r in results["instances"] if r["mode"] == m]
        decision_identity = sum(1 for r in recs if r["arms"][M_ARM]["decision"] == r["arms"][B5_ARM]["decision"]) / (len(recs) or 1)
        per_mode[m] = {"paired": ps, "decision_identity_rate": decision_identity,
                       "M_exact": pa[M_ARM][m]["decision_exact_rate"], "B5_exact": pa[B5_ARM][m]["decision_exact_rate"],
                       "agreement_on_correctness": identical / n}
        p_adv[m] = ps["exact_p_two_sided"] if ps["diff_x_minus_y"] > 0 else 1.0
        p_b5[m] = ps["exact_p_two_sided"] if ps["diff_x_minus_y"] < 0 else 1.0
    holm_adv, holm_b5 = holm(p_adv), holm(p_b5)
    g["G1a_B5_REPRODUCES_M"] = {
        "pass": bool(all(per_mode[m]["decision_identity_rate"] >= 0.995 for m in MODES)),
        "per_mode": {m: per_mode[m]["decision_identity_rate"] for m in MODES},
        "rule": "M and B5 emit the identical decision on >= 99.5% of instances in every mode",
    }
    g["G1b_M_ADVANTAGE_PER_MODE"] = {
        "pass_modes": [m for m in MODES if holm_adv[m]], "holm": holm_adv,
        "per_mode": per_mode,
        "rule": "paired decision-exact difference M - B5 > 0 with an exact two-sided McNemar p surviving Holm correction across the three modes",
    }
    g["G1c_B5_ADVANTAGE_PER_MODE"] = {
        "pass_modes": [m for m in MODES if holm_b5[m]], "holm": holm_b5,
        "rule": "the symmetric test: B5 strictly better than M in a mode, Holm-corrected",
    }
    adv_modes = g["G1b_M_ADVANTAGE_PER_MODE"]["pass_modes"]

    # G2 anti-conservatism per mode
    g2 = {}
    for m in MODES:
        mm = sum(pa[M_ARM][m]["per_stratum"][s]["false_transition"] + pa[M_ARM][m]["per_stratum"][s]["unnecessary_abstention"]
                 + pa[M_ARM][m]["per_stratum"][s]["missed_warranted_transition"] for s in G2_STRATA)
        bb = sum(pa[B5_ARM][m]["per_stratum"][s]["false_transition"] + pa[B5_ARM][m]["per_stratum"][s]["unnecessary_abstention"]
                 + pa[B5_ARM][m]["per_stratum"][s]["missed_warranted_transition"] for s in G2_STRATA)
        g2[m] = {"M": mm, "B5": bb, "pass": mm <= bb}
    g["G2_ANTI_CONSERVATISM"] = {"pass": bool(all(v["pass"] for v in g2.values())), "per_mode": g2,
                                 "strata": list(G2_STRATA),
                                 "rule": "on the negative-control strata M's manufactured doubt (false withholding, unnecessary abstention, missed warranted transitions) does not exceed B5's, in every mode"}

    # G3 mechanism
    g3a: dict = {"applicable": bool(adv_modes), "checks": {}, "pass": None}
    if adv_modes:
        ok = True
        for m in adv_modes:
            for s in STRATA:
                cell = pa[M_ARM][m]["per_stratum"][s]
                b5cell = pa[B5_ARM][m]["per_stratum"][s]
                if cell["exact"] - b5cell["exact"] >= 5:
                    locus = STRATUM_INVARIANT[s][1] or "SUPPORT_DEFEAT"
                    abl = ABLATION_FOR_LOCUS.get(locus, "M_MINUS_FAMILIES")
                    a_rate = pa[abl][m]["per_stratum"][s]["exact_rate"] or 0.0
                    b_rate = b5cell["exact_rate"] or 0.0
                    g3a["checks"][f"{m}/{s}"] = {"ablation": abl, "ablation_exact_rate": a_rate, "B5_exact_rate": b_rate,
                                                 "advantage_vanishes": a_rate <= b_rate}
                    ok &= a_rate <= b_rate
        g3a["pass"] = ok
    g3b = {}
    for abl in ABLATIONS:
        pv = {m: paired_summary(ex[M_ARM][m], ex[abl][m]) for m in MODES}
        pvals = {m: (pv[m]["exact_p_two_sided"] if pv[m]["diff_x_minus_y"] > 0 else 1.0) for m in MODES}
        hol = holm(pvals)
        modes_hit = [m for m in MODES if hol[m]]
        g3b[abl] = {"modes_load_bearing": modes_hit, "per_mode_diff": {m: pv[m]["diff_x_minus_y"] for m in MODES},
                    "identifiable_across_modes": len(modes_hit) >= 2}
    g["G3a_MECHANISM_ATTRIBUTION"] = dict(g3a, rule="each stratum with a claimed M advantage: the matching omission ablation's exact rate <= B5's on that stratum")
    g["G3b_CROSS_MODE_MECHANISM_IDENTIFIABILITY"] = {
        "pass": bool(any(v["identifiable_across_modes"] for v in g3b.values())),
        "per_ablation": g3b,
        "identifiable": [a for a, v in g3b.items() if v["identifiable_across_modes"]],
        "rule": "protocol §7(1): at least one predeclared mechanism is load-bearing (Holm-corrected paired loss when omitted) in at least two native modes. Reported whether or not any residual over B5 exists.",
    }

    # G4 interface ladder per mode + the positive interface-standard test
    g4 = {}
    for m in MODES:
        rates = [pa[r][m]["decision_exact_rate"] for r in LADDER]
        steps, monotone = [], True
        for k in range(4):
            p = paired_summary(ex[LADDER[k + 1]][m], ex[LADDER[k]][m])
            violated = p["diff_x_minus_y"] < 0 and p["exact_p_two_sided"] <= 0.05
            monotone &= not violated
            steps.append({"from": LADDER[k], "to": LADDER[k + 1], "paired": p, "violation": violated})
        load = paired_summary(ex[B5_ARM][m], ex[LADDER[0]][m])
        gap = paired_summary(ex[M_ARM][m], ex[B5_ARM][m])
        lo, hi = gap["wald_ci95"]
        equivalent = abs(lo) <= EQUIVALENCE_MARGIN_PER_MODE and abs(hi) <= EQUIVALENCE_MARGIN_PER_MODE
        interface_load_bearing = load["diff_x_minus_y"] > 0 and load["exact_p_two_sided"] <= 0.05
        significant = [{"step": f"{LADDER[k]}->{LADDER[k + 1]}", "gain": steps[k]["paired"]["diff_x_minus_y"],
                        "p": steps[k]["paired"]["exact_p_two_sided"]}
                       for k in range(4)
                       if steps[k]["paired"]["diff_x_minus_y"] > 0 and steps[k]["paired"]["exact_p_two_sided"] <= 0.05]
        g4[m] = {"rung_exact_rates": dict(zip(LADDER, rates)), "steps": steps, "monotone": monotone,
                 "significant_steps": significant,
                 "decisive_rung": (max(significant, key=lambda x: x["gain"])["step"] if significant else None),
                 "interface_load_bearing": interface_load_bearing, "rung1_vs_rung5": load,
                 "rung5_gap": gap, "equivalent_within_margin": equivalent,
                 "positive_interface_standard": bool(monotone and interface_load_bearing and equivalent)}
    decisive = {m: g4[m]["decisive_rung"] for m in MODES}
    pooled_gap = paired_summary(ex[M_ARM]["POOLED"], ex[B5_ARM]["POOLED"])
    g["G4_INTERFACE_LADDER"] = {
        "pass": bool(all(v["monotone"] for v in g4.values())),
        "per_mode": g4, "pooled_rung5_gap": pooled_gap,
        "decisive_rung_per_mode": decisive,
        "decisive_rung_varies_across_modes": len({v for v in decisive.values() if v}) > 1,
        "significant_steps_per_mode": {m: [s["step"] for s in g4[m]["significant_steps"]] for m in MODES},
        "pooled_equivalent_within_margin": bool(abs(pooled_gap["wald_ci95"][0]) <= EQUIVALENCE_MARGIN_POOLED
                                                and abs(pooled_gap["wald_ci95"][1]) <= EQUIVALENCE_MARGIN_POOLED),
        "positive_interface_standard_all_modes": bool(all(v["positive_interface_standard"] for v in g4.values())),
        "equivalence_margin_per_mode": EQUIVALENCE_MARGIN_PER_MODE, "equivalence_margin_pooled": EQUIVALENCE_MARGIN_POOLED,
        "rule": "monotonicity: no rung k+1 significantly worse than rung k. The interface-standard terminal is a POSITIVE test, not the negation of the gap gate: it requires (i) monotonicity, (ii) rung 1 significantly worse than rung 5 (the interface information is demonstrably load-bearing) and (iii) a two-sided equivalence of M and B5 at full structure within the pre-registered margin, in every mode.",
    }

    cv = sc["changed_vocabulary"]
    # The shuffled-label null needs n to be estimable at all; below the frozen floor it is
    # reported as NOT_ESTIMABLE rather than failed (the 36-instance development split
    # cannot estimate a null with a 0.35 threshold).
    null_floor_n = 100
    null_ok = all((cv[m]["shuffled_label_rate"] <= 0.35) for m in MODES if cv[m]["n"] >= null_floor_n)
    null_estimable = all(cv[m]["n"] >= null_floor_n for m in MODES)
    g["G5_CHANGED_VOCABULARY"] = {
        "pass": bool(all((cv[m]["recovery_rate"] or 0) >= 0.90 for m in MODES) and null_ok),
        "shuffled_null_estimable": null_estimable, "null_estimability_floor_n": null_floor_n,
        "per_mode": cv,
        "rule": "one mode-blind rule set, written without ORION vocabulary and reading native fields through a per-mode adapter, recovers the responsibility class in >= 90% of decidable instances in every mode, while the same classifier scored against within-mode shuffled oracle labels stays <= 35% (evaluated only where a mode has at least 100 decidable instances; below that the null is reported NOT_ESTIMABLE, never passed). FORMAL SURROGATE ONLY: no independent native reviewer participated, so protocol §11 R2 is not grantable by this study.",
    }

    m_ms = pa[M_ARM]["POOLED"]["wall_ms"]; b_ms = pa[B5_ARM]["POOLED"]["wall_ms"]
    g["COST"] = {"M_wall_ms": m_ms, "B5_wall_ms": b_ms, "M_ops": pa[M_ARM]["POOLED"]["ops"], "B5_ops": pa[B5_ARM]["POOLED"]["ops"],
                 "ratio_B5_over_M_wall": (b_ms / m_ms) if m_ms else None,
                 "flag": ("COST_ADVANTAGE_M" if m_ms and b_ms > 2 * m_ms else "COST_ADVANTAGE_B5" if b_ms and m_ms > 2 * b_ms else "COST_PARITY_WITHIN_2X"),
                 "rule": "wall-clock ratio with a 2x flag; reported, never a route by itself"}

    # route
    n_adv = len(adv_modes)
    if not g0:
        route, reason = "CANNOT_CHECK", "G0 native/oracle/null validity failed: lane defect, repair and re-freeze"
    elif n_adv >= 2:
        if not g["G2_ANTI_CONSERVATISM"]["pass"]:
            route, reason = "CANNOT_CHECK", "M advantage in two or more modes coexists with manufactured doubt on the negative-control strata"
        elif not g3a["pass"]:
            route, reason = "CANNOT_CHECK", "M advantage not attributable to a named mechanism by omission ablation"
        elif not g["G5_CHANGED_VOCABULARY"]["pass"]:
            route, reason = "CANNOT_CHECK", "M advantage without a recoverable common object under changed vocabulary"
        else:
            route, reason = "ME_X5_FIELD_RESIDUAL_CANDIDATE", f"M exceeds B5 in {n_adv} native modes, anti-conservative, mechanism attributed, common object recoverable"
    elif n_adv == 1:
        route, reason = "MODE_SPECIFIC_RESIDUAL", f"M exceeds B5 in exactly one native mode ({adv_modes[0]}); protocol §12 treats a single-domain residual as a contraction, not a field claim"
    elif g["G4_INTERFACE_LADDER"]["positive_interface_standard_all_modes"]:
        route, reason = "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL", "no gap at full structure (equivalence established within the pre-registered margin) while the interface information is demonstrably load-bearing across the ladder in every mode"
    else:
        route, reason = "PARENT_SUFFICIENT", "no M advantage over B5 in any native mode, and the positive interface-standard test does not fire"
    if not g["G5_CHANGED_VOCABULARY"]["pass"] and route in ("PARENT_SUFFICIENT", "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL"):
        ladder_rung = "R0_NO_RESIDUAL"
    elif route in ("ME_X5_FIELD_RESIDUAL_CANDIDATE",):
        ladder_rung = "R2_NOT_GRANTABLE_INDEPENDENT_ADJUDICATION_ABSENT"
    elif route == "CANNOT_CHECK":
        ladder_rung = "NOT_ASSIGNED"
    else:
        ladder_rung = "R1_BENCHMARK_INTEGRATION_VALUE"
    b5_dom = g["G1c_B5_ADVANTAGE_PER_MODE"]["pass_modes"]
    g["ROUTE"] = {"route": route, "reason": reason, "field_support_ladder": ladder_rung,
                  "R3_ESTABLISHED_FIELD_GRANTABLE": False,
                  "B5_dominates_modes": b5_dom, "cost_flag": g["COST"]["flag"],
                  "cross_mode_mechanisms": g["G3b_CROSS_MODE_MECHANISM_IDENTIFIABILITY"]["identifiable"],
                  "decisive_rung_per_mode": g["G4_INTERFACE_LADDER"]["decisive_rung_per_mode"],
                  "decisive_rung_varies_across_modes": g["G4_INTERFACE_LADDER"]["decisive_rung_varies_across_modes"]}
    return g


def render_md(analysis: dict) -> str:
    L = [f"# ME-X5 analysis — {analysis['label']}\n"]
    if analysis["label"] == "DEVELOPMENT":
        L.append("**DEVELOPMENT split: not protected evidence. Nothing below supports a confirmatory claim.**\n")
    L.append(f"Results sha256 `{analysis['results_sha256']}`; custody sha256 `{analysis['custody_sha256']}`; "
             f"instances {analysis['n_instances']}.\n")
    pa = analysis["score"]["per_arm"]
    L.append("## Decision-exact rate per mode (§6: reported per mode; a pooled average may not hide a mode failure)\n")
    L.append("| arm | " + " | ".join(list(MODES) + ["POOLED", "false trans.", "unnec. abst.", "auth. viol.", "wall ms"]) + " |")
    L.append("|---|" + "---|" * (len(MODES) + 5))
    for a in pa:
        row = [f"{pa[a][m]['decision_exact_rate']:.3f}" for m in list(MODES) + ["POOLED"]]
        p = pa[a]["POOLED"]
        row += [str(p["false_transition"]), str(p["unnecessary_abstention"]), str(p["authority_violation"]), f"{p['wall_ms']:.1f}"]
        L.append(f"| {a} | " + " | ".join(row) + " |")
    L.append("\n## Per-stratum decision-exact rate (pooled over modes)\n")
    arms = list(pa)
    L.append("| stratum | " + " | ".join(arms) + " |")
    L.append("|---|" + "---|" * len(arms))
    for s in STRATA:
        cells = []
        for a in arms:
            v = pa[a]["POOLED"]["per_stratum"][s]
            cells.append("–" if v["exact_rate"] is None else f"{v['exact_rate']:.2f}")
        L.append(f"| {s} | " + " | ".join(cells) + " |")
    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        if k == "ROUTE":
            continue
        L.append(f"- **{k}**: pass={v.get('pass', v.get('pass_modes'))} — {v.get('rule', '')}")
    r = analysis["gates"]["ROUTE"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}.\n\nField-support ladder: `{r['field_support_ladder']}`; "
             f"R3 grantable: {r['R3_ESTABLISHED_FIELD_GRANTABLE']}; cross-mode mechanisms: {r['cross_mode_mechanisms']}; "
             f"cost: `{r['cost_flag']}`.\n")
    L.append("\n## Interface ladder, reported per mode (never pooled)\n")
    g4 = analysis["gates"]["G4_INTERFACE_LADDER"]
    L.append("| mode | " + " | ".join(LADDER) + " | significant steps | decisive rung |")
    L.append("|---|" + "---|" * (len(LADDER) + 2))
    for m in MODES:
        v = g4["per_mode"][m]
        L.append(f"| {m} | " + " | ".join(f"{v['rung_exact_rates'][r]:.3f}" for r in LADDER) + " | "
                 + (", ".join(s["step"].split("->")[0][6:9] + "→" + s["step"].split("->")[1][6:9] for s in v["significant_steps"]) or "none")
                 + f" | {v['decisive_rung'] or 'none'} |")
    L.append(f"\nDecisive rung varies across modes: **{g4['decisive_rung_varies_across_modes']}**.\n")
    return "\n".join(L)


# ---- stages ---------------------------------------------------------------------------

def stage_selftest(out_dir: Path) -> int:
    report: dict = {"schema_version": SCHEMA_ANALYSIS + ".selftest"}
    fid = fidelity_selftests()
    report["parent_fidelity"] = fid
    report["parent_fidelity_passed"] = all(r["passed"] for r in fid)
    ok = report["parent_fidelity_passed"]

    ka = []
    for f in known_answer_fixtures():
        got = oracle_trajectory(f["episode"])[-1].decision.as_dict()
        passed = got == f["expected"]
        ka.append({"name": f["name"], "passed": passed, "expected": f["expected"], "oracle": got})
        ok &= passed
    report["known_answer"] = ka
    report["known_answer_passed"] = all(k["passed"] for k in ka)

    sep_cases = separation_pair()
    specs = {s.name: s for s in arm_specs()}
    sep_out = {}
    rng = random.Random(0)
    for c in sep_cases:
        got = oracle_trajectory(c["episode"])[-1].decision.as_dict()
        st = final_state(c["episode"])
        arms = {n: run_arm(specs[n], st, rng)[0].as_dict() for n in (LADDER[0], B5_ARM, M_ARM)}
        sep_out[c["name"]] = {"oracle": got, "expected": c["expected"], "oracle_matches": got == c["expected"], "arms": arms}
        ok &= got == c["expected"]
    v1 = [sep_out[c]["arms"][LADDER[0]] for c in ("SEP-P", "SEP-Q")]
    identical = v1[0] == v1[1]
    fails_one = any(sep_out[c]["arms"][LADDER[0]] != sep_out[c]["expected"] for c in ("SEP-P", "SEP-Q"))
    structure_exact = all(sep_out[c]["arms"][n] == sep_out[c]["expected"] for c in ("SEP-P", "SEP-Q") for n in (B5_ARM, M_ARM))
    report["separation"] = {"cases": sep_out, "verdict_only_identical_on_P_and_Q": identical,
                            "verdict_only_errs_on_at_least_one": fails_one,
                            "witness_level_exact_on_both": structure_exact,
                            "passed": bool(identical and fails_one and structure_exact)}
    report["separation_passed"] = report["separation"]["passed"]
    ok &= report["separation_passed"]

    nr = {m: {k: bool(NATIVE_REVIEWS[m].get(k)) for k in NATIVE_REVIEW_REQUIRED_KEYS} for m in MODES}
    report["native_review"] = {"per_mode": nr, "modes": list(MODES),
                               "independent_reviewer": False,
                               "note": "protocol §3 records are present for all three modes; the reviewer is the study author, which is registered as a limitation and is why §11 R2 is not grantable here"}
    report["native_review_complete"] = all(all(v.values()) for v in nr.values()) and len(MODES) >= 3
    ok &= report["native_review_complete"]

    pairs = generate_split("selftest", "ME-X5-SELFTEST", 1)
    validity = {"n": len(pairs), "valid_at_v0": 0, "invariant": 0, "permutation_invariant": 0, "within_cap": 0}
    from mex5_model import trajectory as _traj
    for ep, traj in pairs:
        validity["valid_at_v0"] += int(valid_at_v0(ep))
        validity["permutation_invariant"] += int(permutation_invariant(ep))
        validity["within_cap"] += int(all(len(censored_facts(s)) <= MAX_CENSORED_FACTS for s in _traj(ep)))
        exp_a, exp_l = STRATUM_INVARIANT[ep.stratum]
        d = traj[-1].decision
        hit = (exp_a is None or d.action == exp_a) and (exp_l is None or d.locus == exp_l)
        validity["invariant"] += int(hit)
    validity["pass"] = all(validity[k] == validity["n"] for k in ("valid_at_v0", "invariant", "permutation_invariant", "within_cap"))
    report["oracle_validity"] = validity
    ok &= validity["pass"]

    res, cus = run_instances(pairs, "SELFTEST", "ME-X5-SELFTEST")
    sc = score(res, cus)
    gt = gates(sc, res, dict(report, passed=True))
    report["null_calibration"] = gt["G0c_NULL_CALIBRATION"]
    report["selftest_arm_exact_pooled"] = {a: v["POOLED"]["decision_exact_rate"] for a, v in sc["per_arm"].items()}
    report["selftest_changed_vocabulary"] = sc["changed_vocabulary"]
    report["passed"] = bool(ok)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X5_SELFTEST_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    print(f"selftest {'PASS' if ok else 'FAIL'}: parents {sum(r['passed'] for r in fid)}/{len(fid)}, "
          f"known-answer {sum(k['passed'] for k in ka)}/{len(ka)}, separation {report['separation_passed']}, "
          f"native review {report['native_review_complete']}, oracle validity {validity['pass']}")
    return 0 if ok else 1


def _run_split(label: str, split: str, split_seed: str, per_cell: int, out_dir: Path, public_seed: str | None) -> int:
    pairs = generate_split(split, split_seed, per_cell)
    res, cus = run_instances(pairs, label, public_seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X5_{label}_RESULTS_V1.json"
    cp = out_dir / f"ME_X5_{label}_EXPECTED_CUSTODY_V1.json"
    tp = out_dir / f"ME_X5_{label}_TIMING_V1.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res)); cp.write_text(canonical_json(cus))
    tp.write_text(canonical_json({"schema_version": SCHEMA_RESULTS + ".timing", "label": label, "wall_ns": timing,
                                  "note": "wall-clock is machine-dependent and is kept out of the deterministic results file"}))
    print(f"{label}: {len(pairs)} instances, results sha256 {sha256_file(rp)[:16]}…, custody sha256 {sha256_file(cp)[:16]}…")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_cell: int) -> int:
    if per_cell * len(MODES) * len(STRATA) > 40:
        print("development split is capped at 40 instances", file=sys.stderr)
        return 2
    return _run_split("DEVELOPMENT", "dev", DEV_SEED, per_cell, out_dir, DEV_SEED)


def stage_protected(out_dir: Path, per_cell: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized", file=sys.stderr)
        return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization file unreadable: {exc}", file=sys.stderr)
        return 3
    token = str(auth.get("human_written_token", "")).strip()
    if auth.get("human_written") is not True or len(token) < 16:
        print("REFUSED: authorization requires human_written=true and a human_written_token (>= 16 chars)", file=sys.stderr)
        return 3
    design_sha = sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else ""
    if auth.get("acknowledged_design_sha256") != design_sha:
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr)
        return 3
    if not seed_file.exists():
        print(f"REFUSED: custody seed file absent ({seed_file})", file=sys.stderr)
        return 4
    seed = seed_file.read_bytes().strip()
    commitment = json.loads(DESIGN_JSON.read_text())["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed).hexdigest() != commitment:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr)
        return 4
    return _run_split("PROTECTED", "protected", seed.decode(), per_cell, out_dir, None)


def stage_analyze(results_path: Path, custody_path: Path, out_dir: Path, label: str | None = None,
                  selftest_report: Path | None = None) -> int:
    res = json.loads(results_path.read_text()); cus = json.loads(custody_path.read_text())
    label = label or res.get("label", "UNKNOWN")
    tp = results_path.with_name(results_path.name.replace("_RESULTS_", "_TIMING_"))
    timing = json.loads(tp.read_text()).get("wall_ns", {}) if tp.exists() else {}
    sp = selftest_report or (out_dir / "ME_X5_SELFTEST_REPORT.json")
    selftest = json.loads(sp.read_text()) if sp.exists() else None
    sc = score(res, cus, timing=timing)
    gt = gates(sc, res, selftest)
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label, "results_sha256": sha256_file(results_path),
                "custody_sha256": sha256_file(custody_path), "n_instances": len(res["instances"]),
                "score": {"per_arm": sc["per_arm"], "changed_vocabulary": sc["changed_vocabulary"],
                          "shuffled_label_rate_M": sc["shuffled_label_rate_M"]},
                "gates": gt}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X5_{label}_ANALYSIS_V1.json").write_text(json.dumps(analysis, indent=2, sort_keys=True))
    (out_dir / f"ME_X5_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    r = gt["ROUTE"]
    print(f"{label} route: {r['route']} ({r['reason']}); ladder {r['field_support_ladder']}; "
          f"M {sc['per_arm'][M_ARM]['POOLED']['decision_exact_rate']:.3f} vs B5 {sc['per_arm'][B5_ARM]['POOLED']['decision_exact_rate']:.3f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-cell", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_cell or DEV_PER_CELL)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_cell or PROTECTED_PER_CELL, a.seed_file)
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr)
            return 2
        return stage_analyze(a.results, a.custody, a.out, selftest_report=a.selftest_report)
    return 2


if __name__ == "__main__":
    sys.exit(main())
