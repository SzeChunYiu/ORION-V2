#!/usr/bin/env python3
"""ME-X7 exact claim-sufficient-external-witness study runner (frozen with design V1).

Stages
  selftest   parent fidelity (native known-answer tests), G0a hand-authored
             known-answer fixtures, the P/Q separation pair, the planted
             positives that must trip each no-alarm assertion, G0b oracle
             self-agreement and cross-implementation agreement on a small
             generated set, and null calibration.
  dev        DEVELOPMENT split (public seed, <= 40 instances).  Labelled
             DEVELOPMENT; never protected evidence.
  protected  PROTECTED split.  Refuses unless PROTECTED_RUN_AUTHORIZATION.json
             (human-written token, acknowledged design sha256) is present next
             to this script AND the custody seed hashes to the frozen commitment.
  analyze    Score a results file against its custody file: §6 outcomes,
             G0-G6 gates, the pre-registered route.

Every violation count in the analysis is reported beside the number of
instances actually evaluated for it (`n_evaluated`); a gate whose
`n_evaluated` is zero reports CANNOT_CHECK, never a pass.

Design: ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V1.{md,json}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from mex7_arms import (  # noqa: E402
    ABLATION_FIELDS,
    ABLATION_FOR_CLASS,
    B5_ARM,
    LADDER_RUNGS,
    DISTINCT_IMPLEMENTATIONS,
    MODULE_CHECK_B5,
    MODULE_CHECK_M,
    M_ARM,
    arm_specs,
    run_arm,
    visible_nodes,
)
from mex7_generator import (  # noqa: E402
    CENSOR_VARIANTS_ALL,
    generate_split,
    known_answer_fixtures,
    planted_positives,
    separation_pair,
)
from mex7_model import (  # noqa: E402
    ACCEPT,
    LOCI,
    CANNOT_CHECK,
    CELLS,
    CHECKS,
    INJECTION_CLASSES,
    LOCUS_UNDECLARED,
    MODES,
    REJECT,
    STRATA,
    canonical_json,
    instance_to_json,
)
from mex7_oracle import CHECK_FN, oracle, planter_agrees  # noqa: E402
from mex7_parents import fidelity_selftests  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x7.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x7.exact-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X7-DEV-20260902"
DEV_PER_CELL = 1            # 25 instances <= 40
PROTECTED_PER_CELL = 50     # 1250 instances
DEFAULT_SEED_FILE = Path(
    os.environ.get(
        "MEX7_PROTECTED_SEED_FILE",
        str(Path.home() / ".orion-custody/me-x7/PROTECTED_SEED_V1.txt"),
    )
)

TRACE_ARM = "S2_FULL_HUMAN_STYLE_TRACE"
LADDER = [name for name, _ in LADDER_RUNGS]
SELF_CONTAINED_ARM = "M_MINUS_REGISTRY_RESOLUTION"
NONINFERIORITY_MARGIN = 0.01
NULL_CEILING = 0.15
G2_STRATUM = "NO_DEFECT_WARRANTED"
S3_STRATA = ("STALE_OR_WRONG_SOURCE", "HIDDEN_DEPENDENCE", "INVALID_CALIBRATION")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ---- statistics ---------------------------------------------------------------

def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def exact_binomial_one_sided(b: int, c: int) -> float:
    """P(at least `b` of `b+c` favour x) under H0 p=1/2 — the one-sided
    McNemar tail used for the non-inferiority conjunct."""
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, sum(math.comb(n, i) for i in range(b, n + 1)) / 2 ** n)


def paired_summary(x: list[bool], y: list[bool]) -> dict:
    n = len(x)
    b = sum(1 for a, bb in zip(x, y) if a and not bb)
    c = sum(1 for a, bb in zip(x, y) if bb and not a)
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {
        "n": n,
        "x_only": b,
        "y_only": c,
        "discordant": b + c,
        "diff_x_minus_y": diff,
        "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se],
        "exact_p_two_sided": exact_binomial_two_sided(b, c),
    }


# ---- running arms over a split -------------------------------------------------

def run_instances(instances, label: str, split_seed_public: str | None) -> tuple[dict, dict]:
    specs = arm_specs()
    results = {
        "schema_version": SCHEMA_RESULTS,
        "label": label,
        "split_seed": split_seed_public,
        "arms": [s.name for s in specs],
        "instances": [],
    }
    custody = {
        "schema_version": SCHEMA_RESULTS + ".expected-custody",
        "label": label,
        "instances": [],
    }
    timing: dict[str, dict[str, int]] = {}
    for inst in instances:
        ep = inst.episode
        exp = oracle(ep)
        planted_ok, planted_why = planter_agrees(ep, inst.stratum)
        vis_full = visible_nodes(ep, full_registry=True)
        cross_ok = all(
            CHECK_FN[c](ep, vis_full) == MODULE_CHECK_M[c](ep, vis_full)
            and CHECK_FN[c](ep, vis_full) == MODULE_CHECK_B5[c](ep, vis_full)
            for c in CHECKS
        )
        rec = {
            "instance_id": inst.instance_id,
            "stratum": inst.stratum,
            "mode": inst.mode,
            "locus": inst.locus,
            "replay_required": ep.contract.replay_required,
            "n_supports": len(ep.supports),
            "n_nodes": len(ep.nodes),
            "n_trace_steps": len(ep.internal_steps),
            "arms": {},
        }
        rng = random.Random(sha256_text(inst.instance_id)[:12])
        for spec in specs:
            t0 = time.perf_counter_ns()
            out = run_arm(spec, ep, rng)
            wall = time.perf_counter_ns() - t0
            entry = {
                "verdict": out.verdict,
                "detected_class": out.detected_class,
                "checks_run": out.checks_run,
                "export_units": out.export_units,
            }
            if spec.name in (M_ARM, B5_ARM) and out.check_statuses is not None:
                entry["check_statuses"] = out.check_statuses
            rec["arms"][spec.name] = entry
            timing.setdefault(inst.instance_id, {})[spec.name] = wall
        results["instances"].append(rec)
        custody["instances"].append(
            {
                "instance_id": inst.instance_id,
                "stratum": inst.stratum,
                "mode": inst.mode,
                "locus": inst.locus,
                "expected": exp.as_dict(),
                "planter_agrees": planted_ok,
                "planter_note": planted_why,
                "cross_implementation_agrees": cross_ok,
                "instance": instance_to_json(inst),
            }
        )
    results["_timing_wall_ns"] = timing
    return results, custody


# ---- scoring -------------------------------------------------------------------

def _exact(arm: dict, exp: dict) -> bool:
    if arm["verdict"] != exp["verdict"]:
        return False
    if exp["verdict"] == REJECT:
        return arm["detected_class"] == exp["defect_class"]
    return True


def score(results: dict, custody: dict, *, shuffle_seed: int = 20260902, timing: dict | None = None) -> dict:
    exp_by_id = {r["instance_id"]: r for r in custody["instances"]}
    timing = timing if timing is not None else results.get("_timing_wall_ns", {})
    arms = results["arms"]

    def blank_arm() -> dict:
        return {
            "exact": [],
            "false_acceptance": 0,
            "false_rejection": 0,
            "misclassified_reject": 0,
            "abstain_on_decidable": 0,
            "missed_censoring": 0,
            "export_units": 0,
            "checks_run": 0,
            "wall_ns": 0,
            "per_cell": defaultdict(lambda: {"n": 0, "exact": 0}),
            "per_locus": defaultdict(lambda: {"n": 0, "exact": 0}),
            "detect": defaultdict(lambda: {"n": 0, "hit": 0}),
            "replay_supported": 0,
            "class_agrees_with_b5": defaultdict(lambda: {"n": 0, "hit": 0}),
        }

    per_arm: dict[str, dict] = {a: blank_arm() for a in arms}
    order: list[str] = []
    cells: list[tuple[str, str]] = []
    oracle_verdicts: list[str] = []
    oracle_classes: list[str | None] = []
    g0b_exhaustive = {"n": 0, "ok": 0}
    g0b_planter = {"n": 0, "ok": 0}
    g0b_cross = {"n": 0, "ok": 0}

    for rec in results["instances"]:
        iid = rec["instance_id"]
        cus = exp_by_id[iid]
        exp = cus["expected"]
        order.append(iid)
        cells.append((rec["stratum"], rec["mode"]))
        oracle_verdicts.append(exp["verdict"])
        oracle_classes.append(exp["defect_class"])
        g0b_exhaustive["n"] += 1
        g0b_exhaustive["ok"] += int(bool(exp["exhaustive_agrees"]))
        g0b_planter["n"] += 1
        g0b_planter["ok"] += int(bool(cus["planter_agrees"]))
        g0b_cross["n"] += 1
        g0b_cross["ok"] += int(bool(cus["cross_implementation_agrees"]))
        b5_class = rec["arms"][B5_ARM]["detected_class"] if B5_ARM in rec["arms"] else None
        for a in arms:
            ar = rec["arms"][a]
            pa = per_arm[a]
            ok = _exact(ar, exp)
            pa["exact"].append(ok)
            key = f"{rec['stratum']}|{rec['mode']}"
            pa["per_cell"][key]["n"] += 1
            pa["per_cell"][key]["exact"] += int(ok)
            lk = f"{rec['stratum']}|{rec['locus']}"
            pa["per_locus"][lk]["n"] += 1
            pa["per_locus"][lk]["exact"] += int(ok)
            if exp["verdict"] == REJECT:
                if ar["verdict"] == ACCEPT:
                    pa["false_acceptance"] += 1
                elif ar["verdict"] == REJECT and ar["detected_class"] != exp["defect_class"]:
                    pa["misclassified_reject"] += 1
                d = pa["detect"][exp["defect_class"]]
                d["n"] += 1
                d["hit"] += int(ar["verdict"] == REJECT and ar["detected_class"] == exp["defect_class"])
                ca = pa["class_agrees_with_b5"][exp["defect_class"]]
                if rec["stratum"] in S3_STRATA:
                    ca["n"] += 1
                    ca["hit"] += int(ar["detected_class"] == b5_class)
            if exp["verdict"] == ACCEPT and ar["verdict"] == REJECT:
                pa["false_rejection"] += 1
            if exp["verdict"] != CANNOT_CHECK and ar["verdict"] == CANNOT_CHECK:
                pa["abstain_on_decidable"] += 1
            if exp["verdict"] == CANNOT_CHECK and ar["verdict"] != CANNOT_CHECK:
                pa["missed_censoring"] += 1
            pa["export_units"] += ar["export_units"]
            pa["checks_run"] += ar["checks_run"]
            pa["wall_ns"] += timing.get(iid, {}).get(a, 0)
            if rec["replay_required"] and ar["checks_run"] >= 1:
                pass

    # replay support: does the arm's runnable set carry both replay checks?
    from mex7_arms import _runnable  # noqa: E402
    specs = {s.name: s for s in arm_specs()}
    replay_n = 0
    replay_support: dict[str, int] = defaultdict(int)
    for rec in results["instances"]:
        if not rec["replay_required"]:
            continue
        replay_n += 1
        for a in arms:
            spec = specs[a]
            if spec.native is not None or a == "C_RANDOM_VERDICT":
                continue
            runnable = set(_runnable(spec.fields))
            if {"C_ARTIFACT_DIGEST", "C_ENV_IDENTITY"} <= runnable:
                replay_support[a] += 1

    # shuffled-label null for M
    rng = random.Random(shuffle_seed)
    idx = list(range(len(order)))
    rng.shuffle(idx)
    shuffled_exact_M: list[bool] = []
    if M_ARM in arms:
        m_out = {r["instance_id"]: r["arms"][M_ARM] for r in results["instances"]}
        for i, j in enumerate(idx):
            if i == j:
                continue
            fake = {"verdict": oracle_verdicts[j], "defect_class": oracle_classes[j]}
            shuffled_exact_M.append(_exact(m_out[order[i]], fake))

    # ---- registered-mechanism coverage ledger: every registered mechanism with
    # the number of instances that actually exercised it, so an undrawn one is
    # visible instead of silently contributing a clean zero.
    coverage: dict[str, dict[str, int]] = {
        "cell": defaultdict(int), "locus": defaultdict(int),
        "censor_variant": defaultdict(int), "mode": defaultdict(int),
    }
    for rec, cus_rec in zip(results["instances"], (exp_by_id[r["instance_id"]] for r in results["instances"])):
        coverage["cell"][f"{rec['stratum']}|{rec['mode']}"] += 1
        coverage["mode"][rec["mode"]] += 1
        if rec["stratum"] in ("STALE_OR_WRONG_SOURCE", "HIDDEN_DEPENDENCE"):
            coverage["locus"][f"{rec['stratum']}|{rec['locus']}"] += 1
        facts = dict(tuple(f) for f in cus_rec["instance"]["facts"])
        if "censor_variant" in facts:
            coverage["censor_variant"][facts["censor_variant"]] += 1

    # ---- S2, instance-sensitive: on replay-required episodes M's two replay
    # checks must reproduce the oracle's statuses, not merely be runnable.
    s2 = {"n": 0, "hit": 0}
    for rec in results["instances"]:
        if not rec["replay_required"]:
            continue
        want = exp_by_id[rec["instance_id"]]["expected"]["statuses"]
        got = rec["arms"].get(M_ARM, {}).get("check_statuses") or {}
        s2["n"] += 1
        s2["hit"] += int(
            all(got.get(c) == want.get(c) for c in ("C_ARTIFACT_DIGEST", "C_ENV_IDENTITY"))
        )

    # ---- per-check agreement between the two independent implementations
    impl_agreement: dict[str, dict[str, int]] = {c: {"n": 0, "agree": 0} for c in CHECKS}
    for rec in results["instances"]:
        a = rec["arms"].get(M_ARM, {}).get("check_statuses") or {}
        b = rec["arms"].get(B5_ARM, {}).get("check_statuses") or {}
        for c in CHECKS:
            if c in a and c in b:
                impl_agreement[c]["n"] += 1
                impl_agreement[c]["agree"] += int(a[c] == b[c])

    n_total = len(order)
    summary: dict[str, dict] = {}
    for a, pa in per_arm.items():
        n = len(pa["exact"])
        summary[a] = {
            "n": n,
            "exact_rate": sum(pa["exact"]) / n if n else None,
            "false_acceptance": pa["false_acceptance"],
            "false_acceptance_n_evaluated": sum(1 for v in oracle_verdicts if v == REJECT),
            "false_rejection": pa["false_rejection"],
            "false_rejection_n_evaluated": sum(1 for v in oracle_verdicts if v == ACCEPT),
            "misclassified_reject": pa["misclassified_reject"],
            "abstain_on_decidable": pa["abstain_on_decidable"],
            "abstain_n_evaluated": sum(1 for v in oracle_verdicts if v != CANNOT_CHECK),
            "missed_censoring": pa["missed_censoring"],
            "missed_censoring_n_evaluated": sum(1 for v in oracle_verdicts if v == CANNOT_CHECK),
            "mean_export_units": pa["export_units"] / n if n else None,
            "mean_checks_run": pa["checks_run"] / n if n else None,
            "wall_ms": pa["wall_ns"] / 1e6,
            "per_cell": {k: dict(v, exact_rate=v["exact"] / v["n"] if v["n"] else None) for k, v in pa["per_cell"].items()},
            "per_locus": {k: dict(v, exact_rate=v["exact"] / v["n"] if v["n"] else None) for k, v in pa["per_locus"].items()},
            "detection_recall": {
                k: {"n_evaluated": v["n"], "hit": v["hit"], "recall": v["hit"] / v["n"] if v["n"] else None}
                for k, v in pa["detect"].items()
            },
            "replay_supported": replay_support.get(a, 0),
            "replay_n_evaluated": replay_n,
        }
    return {
        "per_arm": summary,
        "coverage_ledger": {k: dict(v) for k, v in coverage.items()},
        "s2_replay": s2,
        "implementation_agreement": impl_agreement,
        "_raw": per_arm,
        "order": order,
        "cells": cells,
        "oracle_verdicts": oracle_verdicts,
        "g0b": {
            "exhaustive": g0b_exhaustive,
            "planter": g0b_planter,
            "cross_implementation": g0b_cross,
        },
        "shuffled_exact_M": shuffled_exact_M,
        "n_total": n_total,
    }


# ---- gates ---------------------------------------------------------------------

def gates(sc: dict, results: dict, selftest_ok: bool | None) -> dict:
    raw = sc["_raw"]
    per = sc["per_arm"]
    arms = results["arms"]
    cells = sc["cells"]
    n = sc["n_total"]
    ov = sc["oracle_verdicts"]
    g: dict = {}

    # ---- G0
    b = sc["g0b"]
    g["G0a_KNOWN_ANSWER"] = {
        "pass": selftest_ok,
        "n_evaluated": len(CELLS) + 4 + 2 if selftest_ok is not None else 0,
        "rule": "hand-authored fixture per applicable (stratum, mode) cell, the P/Q separation pair "
                "and the planted positives are reproduced in the selftest report",
    }
    g["G0b_ORACLE_SELF_AGREEMENT"] = {
        "pass": bool(
            b["exhaustive"]["n"] > 0
            and b["exhaustive"]["ok"] == b["exhaustive"]["n"]
            and b["planter"]["ok"] == b["planter"]["n"]
            and b["cross_implementation"]["ok"] == b["cross_implementation"]["n"]
        ),
        "n_evaluated": b["exhaustive"]["n"],
        "exhaustive_agree": b["exhaustive"],
        "planter_agree": b["planter"],
        "cross_implementation_agree": b["cross_implementation"],
        "rule": "direct rule == exhaustive enumeration; the planter's declared defect == the "
                "full-structure recomputation (exactly one INVALID check, no censoring); the arms' "
                "independent module implementation == the oracle's check table at full visibility",
    }
    always_accept = raw["C_ALWAYS_ACCEPT"]["exact"]
    always_cc = raw["C_ALWAYS_CANNOT_CHECK"]["exact"]
    rnd = raw["C_RANDOM_VERDICT"]["exact"]
    aa_n = [x for x, v in zip(always_accept, ov) if v == REJECT]
    cc_n = [x for x, v in zip(always_cc, ov) if v != CANNOT_CHECK]
    shuffled = sc["shuffled_exact_M"]
    shuffle_rate = (sum(shuffled) / len(shuffled)) if shuffled else None
    g["G0c_NULL_CALIBRATION"] = {
        "pass": bool(
            len(aa_n) > 0
            and sum(aa_n) == 0
            and len(cc_n) > 0
            and sum(cc_n) == 0
            and shuffle_rate is not None
            and shuffle_rate <= NULL_CEILING
            and (sum(rnd) / n if n else 1.0) <= NULL_CEILING
        ),
        "always_accept_exact_where_oracle_rejects": {"hit": sum(aa_n), "n_evaluated": len(aa_n)},
        "always_cannot_check_exact_where_decidable": {"hit": sum(cc_n), "n_evaluated": len(cc_n)},
        "random_verdict_exact_rate": sum(rnd) / n if n else None,
        "M_vs_shuffled_labels_exact_rate": shuffle_rate,
        "n_evaluated_shuffled": len(shuffled),
        "ceiling": NULL_CEILING,
        "n_evaluated": min(len(aa_n), len(cc_n), len(shuffled) if shuffled else 0),
        "rule": "the degenerate always-accept and always-abstain controls score 0 where their "
                "answer is wrong; random and shuffled-label nulls stay under the ceiling",
    }

    # ---- G1: M vs B5
    m = raw[M_ARM]["exact"]
    b5 = raw[B5_ARM]["exact"]
    paired = paired_summary(m, b5)
    identity = sum(1 for x, y in zip(m, b5) if x == y) / n if n else None
    per_cell_disc: dict[str, float] = {}
    for cell in sorted({f"{s}|{md}" for s, md in cells}):
        idxs = [i for i, (s, md) in enumerate(cells) if f"{s}|{md}" == cell]
        disc = sum(1 for i in idxs if m[i] != b5[i])
        per_cell_disc[cell] = disc / len(idxs) if idxs else 0.0
    g["G1a_B5_REPRODUCES_M"] = {
        "pass": bool(identity is not None and identity >= 0.995 and max(per_cell_disc.values(), default=0.0) <= 0.05),
        "decision_identity": identity,
        "n_evaluated": n,
        "worst_cell_discordance": max(per_cell_disc.values(), default=0.0),
        "per_cell_discordance": per_cell_disc,
        "rule": "identical exact-match indicator on >= 99.5% of instances and no cell above 5% discordant",
    }
    cell_m_only = {}
    for cell in sorted(per_cell_disc):
        idxs = [i for i, (s, md) in enumerate(cells) if f"{s}|{md}" == cell]
        cell_m_only[cell] = sum(1 for i in idxs if m[i] and not b5[i])
    g["G1b_M_ADVANTAGE"] = {
        "pass": bool(
            paired["diff_x_minus_y"] > 0
            and paired["exact_p_two_sided"] <= 0.05
            and max(cell_m_only.values(), default=0) >= 5
        ),
        "n_evaluated": n,
        "paired": paired,
        "cells_with_5plus_M_only": {k: v for k, v in cell_m_only.items() if v >= 5},
        "rule": "paired exact-match difference M - B5 > 0, exact two-sided p <= 0.05, and at least "
                "one cell with >= 5 M-only-exact instances",
    }
    g["G1c_B5_AHEAD"] = {
        "pass": bool(paired["diff_x_minus_y"] < 0 and paired["exact_p_two_sided"] <= 0.05),
        "n_evaluated": n,
        "paired": paired,
        "rule": "its own positive test, not the negation of G1b: paired difference M - B5 < 0 with "
                "exact two-sided p <= 0.05",
    }

    # ---- G2 anti-conservatism (on the fully warranted stratum)
    idxs = [i for i, (s, _) in enumerate(cells) if s == G2_STRATUM]
    m_bad = sum(
        1
        for i in idxs
        if results["instances"][i]["arms"][M_ARM]["verdict"] != ACCEPT
    )
    b5_bad = sum(
        1
        for i in idxs
        if results["instances"][i]["arms"][B5_ARM]["verdict"] != ACCEPT
    )
    g["G2_ANTI_CONSERVATISM"] = {
        "pass": bool(len(idxs) > 0 and m_bad <= b5_bad),
        "n_evaluated": len(idxs),
        "M_non_accept": m_bad,
        "B5_non_accept": b5_bad,
        "rule": "on fully warranted episodes M must not refuse or abstain more often than B5",
    }

    # ---- G3 mechanism: omission-specific detection loss, class by class
    from mex7_model import CHECK_FOR_CLASS, FIELD_FOR_CLASS, REQUIRED_FIELDS  # noqa: E402

    field_to_ablation = {fld: name for name, fld in ABLATION_FIELDS}
    rows = []
    g3_ok = len(INJECTION_CLASSES) > 0
    for cls in INJECTION_CLASSES:
        check = CHECK_FOR_CLASS[cls]
        # every field the check needs; omitting any of them must blind it, and
        # omitting anything else must not.  `C_ROUTE_COMPLETENESS` needs two
        # (design §9(3)), so two ablations are predicted to break that class.
        expected_blind = {field_to_ablation[f] for f in REQUIRED_FIELDS[check] if f in field_to_ablation}
        m_rec = per[M_ARM]["detection_recall"].get(cls, {"n_evaluated": 0, "recall": None})
        n_eval = m_rec["n_evaluated"]
        observed_blind = set()
        for name, fld in ABLATION_FIELDS:
            r = per[name]["detection_recall"].get(cls, {"recall": None})["recall"]
            if r is None or m_rec["recall"] is None:
                continue
            if r < m_rec["recall"]:
                observed_blind.add(name)
        designated = ABLATION_FOR_CLASS[cls]
        ok = bool(
            n_eval > 0
            and m_rec["recall"] is not None
            and observed_blind == expected_blind
            and designated in expected_blind
        )
        rows.append(
            {
                "class": cls,
                "check": check,
                "n_evaluated": n_eval,
                "M_recall": m_rec["recall"],
                "designated_omission_arm": designated,
                "predicted_blinding_omissions": sorted(expected_blind),
                "observed_blinding_omissions": sorted(observed_blind),
                "pass": ok,
            }
        )
        g3_ok &= ok
    g["G3_MECHANISM_BY_OMISSION"] = {
        "pass": bool(g3_ok),
        "n_evaluated": sum(r["n_evaluated"] for r in rows),
        "per_class": rows,
        "rule": "for every injection class, the set of field omissions that lower its detection recall "
                "equals exactly the set of fields its check requires (FIELD_FOR_CLASS is the designated "
                "member); no other omission blinds it",
    }

    # ---- G4 interface ladder
    steps = []
    ladder_ok = True
    for lo, hi in zip(LADDER, LADDER[1:]):
        s = paired_summary(raw[hi]["exact"], raw[lo]["exact"])
        regress = s["diff_x_minus_y"] < 0 and s["exact_p_two_sided"] <= 0.05
        ladder_ok &= not regress
        steps.append({"from": lo, "to": hi, "paired": s, "regression": bool(regress)})
    rung_rates = {name: per[name]["exact_rate"] for name in LADDER}
    g["G4_INTERFACE_LADDER"] = {
        "pass": bool(ladder_ok),
        "n_evaluated": n,
        "rung_exact_rate": rung_rates,
        "steps": steps,
        "rule": "no rung k+1 significantly worse than rung k (rung k+1's fields contain rung k's, so a "
                "reversal is a lane defect of the surface definitions, not a finding)",
    }

    # ---- G5 sufficiency: protocol §7's five conjuncts, each a positive test
    s1_rows = []
    s1_ok = True
    for cls in INJECTION_CLASSES:
        for mode in MODES:
            idxs2 = [
                i
                for i, (s, md) in enumerate(cells)
                if md == mode and s == cls
            ]
            if not idxs2:
                s1_rows.append({"class": cls, "mode": mode, "n_evaluated": 0, "status": "CANNOT_CHECK_NOT_APPLICABLE"})
                continue
            mr = sum(
                1
                for i in idxs2
                if results["instances"][i]["arms"][M_ARM]["detected_class"] == cls
                and results["instances"][i]["arms"][M_ARM]["verdict"] == REJECT
            ) / len(idxs2)
            br = sum(
                1
                for i in idxs2
                if results["instances"][i]["arms"][B5_ARM]["detected_class"] == cls
                and results["instances"][i]["arms"][B5_ARM]["verdict"] == REJECT
            ) / len(idxs2)
            ok = mr >= br - NONINFERIORITY_MARGIN
            s1_ok &= ok
            s1_rows.append(
                {"class": cls, "mode": mode, "n_evaluated": len(idxs2), "M_recall": mr, "B5_recall": br, "pass": ok}
            )
    s2_n = sc["s2_replay"]["n"]
    s2_hit = sc["s2_replay"]["hit"]
    s3_rows = []
    s3_ok = True
    for cls in S3_STRATA:
        v = raw[M_ARM]["class_agrees_with_b5"].get(cls, {"n": 0, "hit": 0})
        ok = v["n"] > 0 and v["hit"] == v["n"]
        s3_ok &= ok
        s3_rows.append({"class": cls, "n_evaluated": v["n"], "agrees": v["hit"], "pass": bool(ok)})
    fa_pairs = [
        (
            results["instances"][i]["arms"][M_ARM]["verdict"] == ACCEPT,
            results["instances"][i]["arms"][B5_ARM]["verdict"] == ACCEPT,
        )
        for i in range(n)
        if ov[i] == REJECT
    ]
    fa_m = sum(1 for x, _ in fa_pairs if x)
    fa_b = sum(1 for _, y in fa_pairs if y)
    disc_m = sum(1 for x, y in fa_pairs if x and not y)
    disc_b = sum(1 for x, y in fa_pairs if y and not x)
    fa_diff = (fa_m - fa_b) / len(fa_pairs) if fa_pairs else 0.0
    s4_ok = bool(fa_pairs) and fa_diff <= NONINFERIORITY_MARGIN
    trace_units = per[TRACE_ARM]["mean_export_units"]
    m_units = per[M_ARM]["mean_export_units"]
    s5_paired = paired_summary(raw[M_ARM]["exact"], raw[TRACE_ARM]["exact"])
    s5_more_accurate = bool(s5_paired["diff_x_minus_y"] > 0 and s5_paired["exact_p_two_sided"] <= 0.05)
    s5_smaller = bool(trace_units and m_units and m_units <= trace_units)
    s5_ok = bool(s5_more_accurate)  # export size is reported, never decisive (design §9(7))
    conjuncts = {
        "S1_FAILURE_CLASS_PRESERVATION": {
            "pass": bool(s1_ok),
            "n_evaluated": sum(r.get("n_evaluated", 0) for r in s1_rows),
            "per_class_mode": s1_rows,
            "rule": f"per class and mode, M's detection recall >= B5's - {NONINFERIORITY_MARGIN}",
        },
        "S2_REPLAY_SUPPORT": {
            "pass": bool(s2_n > 0 and s2_hit == s2_n),
            "n_evaluated": s2_n,
            "supported": s2_hit,
            "rule": "on every replay-required episode the witness's own artifact-identity and "
                    "environment-identity checks reproduce the full-structure statuses — an "
                    "instance-by-instance test, not a restatement of the arm's field set",
        },
        "S3_SELECTIVE_REOPENING_WITHOUT_HIDDEN_HISTORY": {
            "pass": bool(s3_ok),
            "n_evaluated": sum(r["n_evaluated"] for r in s3_rows),
            "per_class": s3_rows,
            "rule": "on support-defeat episodes the witness identifies the same defect class as the "
                    "full-structure audit, with no reconstruction of hidden history",
        },
        "S4_FALSE_ACCEPTANCE_NONINFERIORITY": {
            "pass": bool(s4_ok),
            "n_evaluated": len(fa_pairs),
            "M_false_acceptance": fa_m,
            "B5_false_acceptance": fa_b,
            "difference": fa_diff,
            "margin": NONINFERIORITY_MARGIN,
            "one_sided_exact_p_M_worse": exact_binomial_one_sided(disc_m, disc_b),
            "discordant_M_only": disc_m,
            "discordant_B5_only": disc_b,
            "rule": f"M's false-acceptance rate exceeds B5's by at most {NONINFERIORITY_MARGIN} "
                    "(a prespecified absolute margin, not a failure to reject)",
        },
        "S5_PREFERABLE_TO_FULL_TRACE": {
            "pass": bool(s5_ok),
            "n_evaluated": n,
            "more_accurate_than_full_trace": s5_more_accurate,
            "paired_M_minus_full_trace": s5_paired,
            "M_mean_export_units": m_units,
            "full_trace_mean_export_units": trace_units,
            "export_units_not_larger": s5_smaller,
            "rule": "protocol §7(5) in its positive form: the witness is *scientifically preferable* to "
                    "the full-trace arm — strictly more accurate under a paired exact test (decisive; "
                    "the trace's accuracy is bounded by what it carries, not by its length) and no "
                    "larger in exported records (reported; export size depends on the generator's "
                    "trace-length range and is not decisive on its own)",
        },
    }
    g["G5_SUFFICIENCY"] = {
        "pass": all(c["pass"] for c in conjuncts.values()),
        "n_evaluated": min(c["n_evaluated"] for c in conjuncts.values()),
        "failed_conjuncts": [k for k, v in conjuncts.items() if not v["pass"]],
        "conjuncts": conjuncts,
    }

    # ---- G6 cross-mode transfer
    mode_rows = {}
    g6_ok = True
    for mode in MODES:
        idxs2 = [i for i, (_, md) in enumerate(cells) if md == mode]
        if not idxs2:
            mode_rows[mode] = {"n_evaluated": 0, "status": "CANNOT_CHECK"}
            g6_ok = False
            continue
        mm = [m[i] for i in idxs2]
        bb = [b5[i] for i in idxs2]
        p = paired_summary(mm, bb)
        rung = {name: sum(raw[name]["exact"][i] for i in idxs2) / len(idxs2) for name in LADDER}
        mono = all(
            rung[hi] >= rung[lo] - 1e-12 for lo, hi in zip(LADDER, LADDER[1:])
        )
        ok = mono and p["diff_x_minus_y"] >= -NONINFERIORITY_MARGIN
        g6_ok &= ok
        mode_rows[mode] = {
            "n_evaluated": len(idxs2),
            "paired_M_minus_B5": p,
            "rung_exact_rate": rung,
            "ladder_monotone": mono,
            "pass": bool(ok),
        }
    g["G6_CROSS_MODE_TRANSFER"] = {
        "pass": bool(g6_ok),
        "n_evaluated": sum(v.get("n_evaluated", 0) for v in mode_rows.values()),
        "per_mode": mode_rows,
        "rule": "the ladder is monotone and M is non-inferior to B5 separately in each epistemic mode "
                "(protocol §10: results that fail to transfer across a second mode are killed)",
    }

    # ---- cost flag
    m_wall = per[M_ARM]["wall_ms"]
    b5_wall = per[B5_ARM]["wall_ms"]
    ratio = (b5_wall / m_wall) if m_wall else None
    cost_flag = "COST_COMPARABLE"
    if ratio is not None and ratio >= 2.0:
        cost_flag = "COST_ADVANTAGE_M"
    elif ratio is not None and ratio <= 0.5:
        cost_flag = "COST_ADVANTAGE_B5"
    g["COST"] = {
        "flag": cost_flag,
        "M_wall_ms": m_wall,
        "B5_wall_ms": b5_wall,
        "wall_ratio_b5_over_m": ratio,
        "M_mean_export_units": m_units,
        "full_trace_mean_export_units": trace_units,
        "rule": "reported; never a route by itself",
    }

    # ---- G7: identity-exporting vs self-contained witness (a positive test,
    # not a cross-cut, because with the M-vs-B5 gates expected to tie this is
    # where the study's separating content lives).
    sc_arm = per[SELF_CONTAINED_ARM]
    undeclared_idx = [
        i for i, r in enumerate(results["instances"]) if r["locus"] == LOCUS_UNDECLARED
    ]
    other_idx = [i for i in range(n) if i not in set(undeclared_idx)]
    m_on_und = (
        sum(raw[M_ARM]["exact"][i] for i in undeclared_idx) / len(undeclared_idx)
        if undeclared_idx else None
    )
    sc_on_und = (
        sum(raw[SELF_CONTAINED_ARM]["exact"][i] for i in undeclared_idx) / len(undeclared_idx)
        if undeclared_idx else None
    )
    agree_elsewhere = (
        all(raw[M_ARM]["exact"][i] == raw[SELF_CONTAINED_ARM]["exact"][i] for i in other_idx)
        if other_idx else None
    )
    sc_fa_und = sum(
        1 for i in undeclared_idx
        if ov[i] == REJECT and results["instances"][i]["arms"][SELF_CONTAINED_ARM]["verdict"] == ACCEPT
    )
    g["G7_WITNESS_SELF_CONTAINMENT"] = {
        "pass": bool(
            undeclared_idx
            and m_on_und is not None
            and sc_on_und is not None
            and m_on_und > sc_on_und
            and agree_elsewhere
        ),
        "status": "EVALUATED" if undeclared_idx else "CANNOT_CHECK_NO_UNDECLARED_INSTANCES",
        "n_evaluated": len(undeclared_idx),
        "n_evaluated_elsewhere": len(other_idx),
        "M_exact_on_undeclared": m_on_und,
        "self_contained_exact_on_undeclared": sc_on_und,
        "self_contained_false_acceptance_on_undeclared": sc_fa_und,
        "identical_everywhere_else": agree_elsewhere,
        "self_contained_exact_overall": sc_arm["exact_rate"],
        "rule": "a positive test with its own denominator: on undeclared-upstream episodes the "
                "identity-exporting witness is strictly more exact than the self-contained one, and "
                "the two are identical on every other episode — so the separation is the mechanism, "
                "not a rate. Zero such episodes reports CANNOT_CHECK, never a pass.",
    }

    # ---- registered-mechanism coverage ledger (design §3): every registered
    # mechanism with the number of instances that exercised it.
    ledger = sc["coverage_ledger"]
    expected_variants = set(CENSOR_VARIANTS_ALL)
    undrawn = {
        "censor_variants": sorted(expected_variants - set(ledger["censor_variant"])),
        "cells": sorted({f"{s2_}|{m2_}" for s2_, m2_ in CELLS} - set(ledger["cell"])),
        "loci": sorted(
            {f"{st}|{lo}" for st in ("STALE_OR_WRONG_SOURCE", "HIDDEN_DEPENDENCE") for lo in LOCI}
            - set(ledger["locus"])
        ),
    }
    g["COVERAGE_LEDGER"] = {
        "n_evaluated": n,
        "drawn": ledger,
        "never_exercised": undrawn,
        "all_registered_mechanisms_exercised": not any(undrawn.values()),
        "rule": "reported, not a gate: any registered mechanism with zero instances is named here so "
                "no violation count computed over it can be read as 'checked and fine'",
    }

    # ---- agreement between the two independent check implementations
    g["IMPLEMENTATION_AGREEMENT"] = {
        "n_evaluated": max((v["n"] for v in sc["implementation_agreement"].values()), default=0),
        "per_check": sc["implementation_agreement"],
        "distinct_implementations": list(DISTINCT_IMPLEMENTATIONS),
        "rule": "M and B5 run different code for source status, dependence, environment identity "
                "(computational mode) and preservation; the remaining seven checks are arithmetic "
                "thin enough that two implementations would coincide, and are reported as shared",
    }

    # ---- route
    g0_ok = bool(g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"] and (selftest_ok is not False))
    if not g0_ok:
        route, reason = "CANNOT_CHECK", "a hard G0 gate failed — lane defect; repair, re-freeze, no arm verdict"
        terminal = "NONE"
    elif g["G1c_B5_AHEAD"]["pass"]:
        route = "PARENT_SUFFICIENT"
        reason = "the parent federation is strictly ahead of the claim-sufficient witness"
        terminal = "WITNESS_INSUFFICIENT_PARENT_AHEAD"
    elif g["G1b_M_ADVANTAGE"]["pass"] and not g["G2_ANTI_CONSERVATISM"]["pass"]:
        route, reason, terminal = "M_OVER_ABSTAINS", "witness advantage bought by refusing warranted transitions", "NONE"
    elif g["G1b_M_ADVANTAGE"]["pass"] and g["G3_MECHANISM_BY_OMISSION"]["pass"]:
        route, reason, terminal = "ME_X7_RESIDUAL_CANDIDATE", "witness advantage over the federation attributable to named fields", "WITNESS_ABOVE_PARENT"
    elif g["G1b_M_ADVANTAGE"]["pass"]:
        route, reason, terminal = "CANNOT_CHECK", "advantage not attributable to a named witness field", "NONE"
    elif not g["G6_CROSS_MODE_TRANSFER"]["pass"]:
        route = "PARENT_SUFFICIENT"
        reason = "no discordance with the federation, but the result does not transfer across both modes"
        terminal = "NO_CROSS_MODE_TRANSFER"
    elif g["G5_SUFFICIENCY"]["pass"]:
        route = "PARENT_SUFFICIENT"
        reason = "the federation is matched, and the compact witness meets every sufficiency conjunct"
        terminal = "WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT"
    else:
        route = "PARENT_SUFFICIENT"
        reason = "the federation is matched but a sufficiency conjunct fails"
        terminal = "WITNESS_NOT_CLAIM_SUFFICIENT:" + ",".join(g["G5_SUFFICIENCY"]["failed_conjuncts"])
    if terminal == "WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT" and not g["G7_WITNESS_SELF_CONTAINMENT"]["pass"]:
        if g["G7_WITNESS_SELF_CONTAINMENT"]["status"].startswith("CANNOT_CHECK"):
            terminal += "__SELF_CONTAINMENT_CANNOT_CHECK"
        else:
            terminal += "__SELF_CONTAINMENT_NOT_SEPARATED"
    elif terminal == "WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT":
        terminal += "__REQUIRES_IDENTITY_EXPORT"
    g["ROUTE"] = {
        "route": route,
        "reason": reason,
        "witness_terminal": terminal,
        "cost_flag": cost_flag,
        "note": "PARENT_SUFFICIENT is a successful terminal of this design; the witness terminal is a "
                "separate positive statement and neither is the negation of the other",
    }
    return g


# ---- rendering ------------------------------------------------------------------

def render_md(analysis: dict) -> str:
    L: list[str] = []
    L.append(f"# ME-X7 analysis — {analysis['label']}\n")
    if analysis["label"] != "PROTECTED":
        L.append(f"**{analysis['label']} split: not protected evidence. Numbers below cannot support any confirmatory claim.**\n")
    L.append(
        f"Results sha256 `{analysis['results_sha256']}`; custody sha256 `{analysis['custody_sha256']}`; "
        f"instances {analysis['n_instances']}.\n"
    )
    per = analysis["score"]["per_arm"]
    L.append("## Per-arm outcomes (§6)\n")
    L.append("| arm | exact | false accept (n) | false reject (n) | misclassified | abstain on decidable (n) | missed censoring (n) | mean export | mean checks | wall ms |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for a, s in per.items():
        L.append(
            f"| {a} | {s['exact_rate']:.3f} | {s['false_acceptance']} ({s['false_acceptance_n_evaluated']}) | "
            f"{s['false_rejection']} ({s['false_rejection_n_evaluated']}) | {s['misclassified_reject']} | "
            f"{s['abstain_on_decidable']} ({s['abstain_n_evaluated']}) | {s['missed_censoring']} ({s['missed_censoring_n_evaluated']}) | "
            f"{s['mean_export_units']:.1f} | {s['mean_checks_run']:.1f} | {s['wall_ms']:.1f} |"
        )
    L.append("\n## Detection recall by failure class (n evaluated in brackets)\n")
    show = [a for a in per if not a.startswith("L") or a == "L6_FULL_WITNESS"]
    L.append("| class | " + " | ".join(show) + " |")
    L.append("|---|" + "---|" * len(show))
    for cls in INJECTION_CLASSES:
        row = []
        for a in show:
            d = per[a]["detection_recall"].get(cls)
            row.append("–" if not d or d["recall"] is None else f"{d['recall']:.2f} ({d['n_evaluated']})")
        L.append(f"| {cls} | " + " | ".join(row) + " |")
    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        if k in ("ROUTE", "COST", "COVERAGE_LEDGER", "IMPLEMENTATION_AGREEMENT"):
            continue
        L.append(f"- **{k}**: pass={v.get('pass')}, n_evaluated={v.get('n_evaluated')} — {v.get('rule', '')}")
    for k, v in analysis["gates"]["G5_SUFFICIENCY"]["conjuncts"].items():
        L.append(f"  - {k}: pass={v['pass']}, n_evaluated={v['n_evaluated']}")
    cl = analysis["gates"]["COVERAGE_LEDGER"]
    L.append("\n## Registered-mechanism coverage\n")
    L.append(f"- all registered mechanisms exercised: **{cl['all_registered_mechanisms_exercised']}**")
    for k, v in cl["never_exercised"].items():
        L.append(f"- never exercised — {k}: {v if v else 'none'}")
    ia = analysis["gates"]["IMPLEMENTATION_AGREEMENT"]
    L.append(
        f"\nM/B5 implementation agreement (distinct code on {', '.join(ia['distinct_implementations'])}): "
        + ", ".join(f"{c} {v['agree']}/{v['n']}" for c, v in ia["per_check"].items() if v["n"])
        + "\n"
    )
    r = analysis["gates"]["ROUTE"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}. Witness terminal: `{r['witness_terminal']}`. Cost: `{r['cost_flag']}`.\n")
    return "\n".join(L)


# ---- stages ---------------------------------------------------------------------

def stage_selftest(out_dir: Path) -> int:
    report: dict = {
        "schema_version": SCHEMA_ANALYSIS + ".selftest",
        "parent_fidelity": fidelity_selftests(),
        "known_answer": [],
        "planted_positives": [],
        "separation": {},
    }
    ok = all(r["passed"] for r in report["parent_fidelity"])

    for f in known_answer_fixtures():
        exp = oracle(f["instance"].episode)
        passed = (
            exp.verdict == f["expected"]["verdict"]
            and exp.defect_class == f["expected"]["defect_class"]
            and exp.exhaustive_agrees
        )
        report["known_answer"].append(
            {
                "name": f["name"],
                "passed": bool(passed),
                "expected": f["expected"],
                "oracle": {"verdict": exp.verdict, "defect_class": exp.defect_class},
            }
        )
        ok &= passed

    for probe in planted_positives():
        agreed, why = planter_agrees(probe["episode"], probe["claimed_stratum"])
        passed = (not agreed) if probe["must_be_rejected"] else agreed
        report["planted_positives"].append(
            {
                "name": probe["name"],
                "passed": bool(passed),
                "must_be_rejected": probe["must_be_rejected"],
                "planter_agreed": bool(agreed),
                "note": why,
            }
        )
        ok &= passed

    p, q = separation_pair()
    specs = {s.name: s for s in arm_specs()}
    sep: dict[str, dict] = {}
    for inst in (p, q):
        exp = oracle(inst.episode)
        sep[inst.instance_id] = {
            "oracle_verdict": exp.verdict,
            "oracle_class": exp.defect_class,
            "arms": {
                name: {
                    "verdict": (o := run_arm(specs[name], inst.episode, random.Random(0))).verdict,
                    "detected_class": o.detected_class,
                }
                for name in (SELF_CONTAINED_ARM, M_ARM, B5_ARM)
            },
        }
    self_identical = (
        sep["SEP-P"]["arms"][SELF_CONTAINED_ARM] == sep["SEP-Q"]["arms"][SELF_CONTAINED_ARM]
    )
    oracle_differs = sep["SEP-P"]["oracle_verdict"] != sep["SEP-Q"]["oracle_verdict"]
    resolved_exact = all(
        sep[k]["arms"][name]["verdict"] == sep[k]["oracle_verdict"]
        for k in ("SEP-P", "SEP-Q")
        for name in (M_ARM, B5_ARM)
    )
    report["separation"] = {
        "cases": sep,
        "self_contained_outputs_identical_on_P_and_Q": bool(self_identical),
        "oracle_verdicts_differ": bool(oracle_differs),
        "identity_exporting_exact_on_both": bool(resolved_exact),
        "passed": bool(self_identical and oracle_differs and resolved_exact),
    }
    ok &= report["separation"]["passed"]

    instances = generate_split("selftest", "ME-X7-SELFTEST", 1)
    res, cus = run_instances(instances, "SELFTEST", "ME-X7-SELFTEST")
    sc = score(res, cus)
    gt = gates(sc, res, True)
    report["oracle_agreement"] = gt["G0b_ORACLE_SELF_AGREEMENT"]
    report["null_calibration"] = gt["G0c_NULL_CALIBRATION"]
    report["selftest_arm_exact"] = {a: v["exact_rate"] for a, v in sc["per_arm"].items()}
    ok &= gt["G0b_ORACLE_SELF_AGREEMENT"]["pass"]
    ok &= gt["G0c_NULL_CALIBRATION"]["pass"]
    report["passed"] = bool(ok)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ME_X7_SELFTEST_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    print(
        f"selftest {'PASS' if ok else 'FAIL'}: parents "
        f"{sum(r['passed'] for r in report['parent_fidelity'])}/{len(report['parent_fidelity'])}, "
        f"known-answer {sum(k['passed'] for k in report['known_answer'])}/{len(report['known_answer'])}, "
        f"planted positives {sum(k['passed'] for k in report['planted_positives'])}/{len(report['planted_positives'])}, "
        f"separation {report['separation']['passed']}, "
        f"G0b {gt['G0b_ORACLE_SELF_AGREEMENT']['pass']}, G0c {gt['G0c_NULL_CALIBRATION']['pass']}"
    )
    return 0 if ok else 1


def _run_split(label: str, split: str, split_seed: str, per_cell: int, out_dir: Path, public_seed: str | None) -> int:
    instances = generate_split(split, split_seed, per_cell)
    res, cus = run_instances(instances, label, public_seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_X7_{label}_RESULTS_V1.json"
    cp = out_dir / f"ME_X7_{label}_EXPECTED_CUSTODY_V1.json"
    tp = out_dir / f"ME_X7_{label}_TIMING_V1.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res))
    cp.write_text(canonical_json(cus))
    tp.write_text(
        canonical_json(
            {
                "schema_version": SCHEMA_RESULTS + ".timing",
                "label": label,
                "wall_ns": timing,
                "note": "wall-clock is machine-dependent and is kept out of the deterministic results file",
            }
        )
    )
    print(f"{label}: {len(instances)} instances, results {rp} sha256 {sha256_file(rp)[:16]}…, custody sha256 {sha256_file(cp)[:16]}…")
    return stage_analyze(rp, cp, out_dir, label)


def stage_dev(out_dir: Path, per_cell: int) -> int:
    if per_cell * len(CELLS) > 40:
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
    if not token or auth.get("human_written") is not True or len(token) < 16:
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


def stage_analyze(results_path: Path, custody_path: Path, out_dir: Path, label: str | None = None, selftest_report: Path | None = None) -> int:
    res = json.loads(results_path.read_text())
    cus = json.loads(custody_path.read_text())
    label = label or res.get("label", "UNKNOWN")
    tp = results_path.with_name(results_path.name.replace("_RESULTS_", "_TIMING_"))
    timing = json.loads(tp.read_text()).get("wall_ns", {}) if tp.exists() else {}
    selftest_ok = None
    sp = selftest_report or (out_dir / "ME_X7_SELFTEST_REPORT.json")
    if sp.exists():
        selftest_ok = bool(json.loads(sp.read_text()).get("passed"))
    sc = score(res, cus, timing=timing)
    gt = gates(sc, res, selftest_ok)
    analysis = {
        "schema_version": SCHEMA_ANALYSIS,
        "label": label,
        "results_sha256": sha256_file(results_path),
        "custody_sha256": sha256_file(custody_path),
        "n_instances": len(res["instances"]),
        "score": {"per_arm": sc["per_arm"]},
        "gates": gt,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"ME_X7_{label}_ANALYSIS_V1.json").write_text(json.dumps(analysis, indent=2, sort_keys=True, default=str))
    (out_dir / f"ME_X7_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    print(
        f"{label} route: {gt['ROUTE']['route']} ({gt['ROUTE']['reason']}); witness terminal: "
        f"{gt['ROUTE']['witness_terminal']}; M exact {sc['per_arm'][M_ARM]['exact_rate']:.3f}, "
        f"B5 exact {sc['per_arm'][B5_ARM]['exact_rate']:.3f}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-cell", type=int, default=None)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--custody", type=Path)
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
