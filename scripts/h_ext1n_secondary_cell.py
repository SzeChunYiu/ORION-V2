#!/usr/bin/env python3
"""H-EXT-1N secondary cell: dependence recovery, preservation and parent sufficiency.

Scores the held-out N1-EVAL split against the endpoints frozen in
research/experiments/h-ext1-naturalistic/H_EXT1N_SECONDARY_CELL_FREEZE_V1.json, which was
committed before the split was dispatched. This is a SEPARATE identity from the H-EXT-1N
gate question: that question terminated on the development split at NO_CANDIDATE_GATE_ON_DEV
and no gate is selected, scored or reported here.

Instance extraction, the witness features and the exact McNemar test are imported from
scripts/h_ext1n_gate_study.py so the arm-visibility canary and the feature definitions are
literally the same code that the gate study used.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATE_STUDY = ROOT / "scripts/h_ext1n_gate_study.py"
DEFAULT_FREEZE = ROOT / "research/experiments/h-ext1-naturalistic/H_EXT1N_SECONDARY_CELL_FREEZE_V1.json"
DEPENDENT_STRATA = ("NS1A", "NS1C")
INDEPENDENT_STRATA = ("NS1B", "NS1D")


def _load_gate_study():
    spec = importlib.util.spec_from_file_location("h_ext1n_gate_study", GATE_STUDY)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/h_ext1n_gate_study.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


G = _load_gate_study()
ARM_M, ARM_OFF, ARM_PARENT = G.ARM_M, G.ARM_OFF, G.ARM_PARENT


def _acc(rows: list[dict[str, Any]], arm: str) -> float:
    return sum(1 for r in rows if r["arms"][arm]["correct"]) / len(rows) if rows else 0.0


def _discordance(rows: list[dict[str, Any]], a: str, b: str) -> tuple[int, int]:
    only_a = sum(1 for r in rows if r["arms"][a]["correct"] and not r["arms"][b]["correct"])
    only_b = sum(1 for r in rows if r["arms"][b]["correct"] and not r["arms"][a]["correct"])
    return only_a, only_b


def _subset(rows: list[dict[str, Any]], strata: tuple[str, ...]) -> list[dict[str, Any]]:
    return [r for r in rows if str(r.get("oracle_stratum_reporting_only")) in strata]


def _family_error(rows: list[dict[str, Any]], arm: str, answers: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows:
        actual = r["arms"][arm].get("actual") or {}
        truth = answers.get(r["task_id"], {}).get("independent_support_family_count")
        got = actual.get("independent_support_family_count")
        if truth is None or not isinstance(got, (int, float)):
            key = "unparsed"
        else:
            key = f"{int(got) - int(truth):+d}"
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items()))


def analyze(instances: dict[str, Any], freeze: dict[str, Any], dev_ids: set[str], answers: dict[str, Any],
            gate_freeze: dict[str, Any] | None) -> dict[str, Any]:
    rows_all = instances["rows"]
    arms = (ARM_M, ARM_OFF, ARM_PARENT)
    missing = [r["task_id"] for r in rows_all if not all(r["arms"].get(a, {}).get("present") for a in arms)]
    reasons = []
    if missing:
        reasons.append(f"{len(missing)} sets missing an arm response")
    if instances.get("split") != "EVAL":
        reasons.append("scored cell is not the EVAL split")
    if {r["task_id"] for r in rows_all} & dev_ids:
        reasons.append("EVAL/DEV task-id overlap")
    if instances.get("corpus_freeze_sha256") != freeze["corpus_freeze_sha256"]:
        reasons.append("EVAL study was built from a different corpus than the frozen one")
    result: dict[str, Any] = {
        "schema_version": "orion.v2.h-ext1n-secondary-cell-result.v1",
        "cell_id": "H-EXT-1N-SECONDARY",
        "cell": "N1-EVAL",
        "n_total": len(rows_all),
        "n_missing": len(missing),
        "gate_identity_note": "the H-EXT-1N gate question terminated at NO_CANDIDATE_GATE_ON_DEV; selected_gate="
                              f"{(gate_freeze or {}).get('selected_gate')!r}; no gate is scored here",
        "validity": {"pass": not reasons, "reasons": reasons},
    }
    if reasons:
        result["terminal"] = "CANNOT_CHECK_RUN_INVALID"
        return result
    rows = rows_all
    dep, ind = _subset(rows, DEPENDENT_STRATA), _subset(rows, INDEPENDENT_STRATA)
    b_dep, c_dep = _discordance(dep, ARM_M, ARM_OFF)
    p_dep = G.mcnemar_exact(b_dep, c_dep)
    acc_dep, acc_ind = _acc(dep, ARM_M), _acc(ind, ARM_M)
    ep = freeze["endpoints"]
    a_pass = acc_dep >= 0.80 and p_dep < 0.01
    b_pass = acc_ind >= 0.90
    b_par, c_par = _discordance(rows, ARM_M, ARM_PARENT)
    p_par = G.mcnemar_exact(b_par, c_par)
    acc_m, acc_par = _acc(rows, ARM_M), _acc(rows, ARM_PARENT)
    if p_par >= 0.05:
        parent_terminal = "STRONGEST_PARENT_SUFFICIENT_ON_NATURALISTIC_RECORDS"
    elif acc_m > acc_par:
        parent_terminal = "DEPENDENCE_AWARE_ARM_BEATS_STRONGEST_PARENT_ON_NATURALISTIC_RECORDS"
    else:
        parent_terminal = "STRONGEST_PARENT_BEATS_DEPENDENCE_AWARE_ARM_ON_NATURALISTIC_RECORDS"
    per_stratum: dict[str, Any] = {}
    for r in rows:
        s = str(r.get("oracle_stratum_reporting_only"))
        e = per_stratum.setdefault(s, {"n": 0, "M": 0, "OFF": 0, "PARENT": 0})
        e["n"] += 1
        for arm, key in ((ARM_M, "M"), (ARM_OFF, "OFF"), (ARM_PARENT, "PARENT")):
            e[key] += 1 if r["arms"][arm]["correct"] else 0
    witness = {}
    for gate in G.CANDIDATE_GATES:
        active = [G.gate_fires(gate, r["features"]) for r in rows]
        oracle_active = [str(r.get("oracle_stratum_reporting_only")) in DEPENDENT_STRATA for r in rows]
        tp = sum(1 for a, o in zip(active, oracle_active) if a and o)
        fp = sum(1 for a, o in zip(active, oracle_active) if a and not o)
        fn = sum(1 for a, o in zip(active, oracle_active) if not a and o)
        witness[gate] = {"activations": sum(active), "precision": tp / (tp + fp) if tp + fp else None,
                         "recall": tp / (tp + fn) if tp + fn else None}
    per_topic: dict[str, Any] = {}
    for r in rows:
        t = str(r.get("topic"))
        e = per_topic.setdefault(t, {"n": 0, "M": 0, "OFF": 0, "PARENT": 0})
        e["n"] += 1
        for arm, key in ((ARM_M, "M"), (ARM_OFF, "OFF"), (ARM_PARENT, "PARENT")):
            e[key] += 1 if r["arms"][arm]["correct"] else 0
    result.update({
        "endpoints": {
            "A_DETECTION": {"definition": ep["A_DETECTION"]["definition"], "acc_M_dependent": acc_dep,
                            "n": len(dep), "M_only_correct": b_dep, "OFF_only_correct": c_dep,
                            "mcnemar_exact_p": p_dep, "threshold": 0.80, "pass": a_pass},
            "B_PRESERVATION": {"definition": ep["B_PRESERVATION"]["definition"], "acc_M_independent": acc_ind,
                               "n": len(ind), "threshold": 0.90, "pass": b_pass},
            "C_PARENT_SUFFICIENCY": {"acc_M": acc_m, "acc_PARENT": acc_par, "M_only_correct": b_par,
                                     "PARENT_only_correct": c_par, "mcnemar_exact_p": p_par,
                                     "terminal": parent_terminal},
        },
        "pooled": {"acc_M": acc_m, "acc_OFF": _acc(rows, ARM_OFF), "acc_PARENT": acc_par, "n": len(rows)},
        "reporting_only": {
            "per_stratum": dict(sorted(per_stratum.items())),
            "per_topic": dict(sorted(per_topic.items())),
            "witness_informativeness_vs_oracle": witness,
            "family_count_error_M": _family_error(rows, ARM_M, answers),
            "family_count_error_OFF": _family_error(rows, ARM_OFF, answers),
        },
        "terminal": ("DEPENDENCE_NOT_DETECTED_IN_NATURALISTIC_RECORDS" if not a_pass else
                     "DEPENDENCE_MODELLING_OVER_TRIGGERS_ON_NATURALISTIC_RECORDS" if not b_pass else
                     "DEPENDENCE_STRUCTURE_RECOVERABLE_FROM_NATURALISTIC_RECORDS"),
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_manuscript_change": False, "grants_general_dependence_detector": False},
    })
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--instances", type=Path, required=True)
    p.add_argument("--dev-instances", type=Path, required=True)
    p.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    p.add_argument("--gate-freeze", type=Path, default=None)
    p.add_argument("--oracle", type=Path, required=True, help="N1-EVAL private_oracle.json (restored after dispatch)")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    freeze = G.read_json(args.freeze)
    if G.sha256_path(args.freeze) != freeze.get("_self_sha256", G.sha256_path(args.freeze)):
        raise RuntimeError("freeze file self-hash mismatch")
    instances = G.read_json(args.instances)
    dev_ids = {r["task_id"] for r in G.read_json(args.dev_instances)["rows"]}
    answers = G.read_json(args.oracle)["answers"]
    gate_freeze = G.read_json(args.gate_freeze) if args.gate_freeze else None
    result = analyze(instances, freeze, dev_ids, answers, gate_freeze)
    result["freeze_sha256"] = G.sha256_path(args.freeze)
    G.write_json(args.out, result)
    print(json.dumps({"terminal": result["terminal"], "parent": result.get("endpoints", {}).get("C_PARENT_SUFFICIENCY", {}).get("terminal")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
