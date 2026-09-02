#!/usr/bin/env python3
"""H-EXT-1 conditional-activation gate study (design V1).

Extracts per-instance tables from P-D generated-suite campaign roots, selects a gate
on the development split ONLY, freezes it, evaluates GATED_M = M if gate(x) else OFF
on disjoint cells against the frozen gates G0..G4 (clean baselines + shuffle-equal-n
nulls), and writes the rollup. Design: research/experiments/h-ext1/
H_EXT1_CONDITIONAL_ACTIVATION_DESIGN_V1.{md,json}. The gate never sees oracle fields
or arm outputs (canary-asserted). Grants nothing; routes to pre-registered terminals.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import re
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "research/experiments/h-ext1/H_EXT1_CONDITIONAL_ACTIVATION_DESIGN_V1.json"
ARM_M = "P_D_FULL"
ARM_OFF = "P_D_MINUS_DEPENDENCE"
ARM_PARENT = "STRONGEST_ASSURANCE_FEDERATION"
FORBIDDEN_KEYS = {"strata", "stratum", "answers", "expected", "answer", "correct", "actual", "private_oracle", "oracle"}
TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9-]{3,}\b")
CANDIDATE_GATES = (
    "G_A_PROVENANCE_WITNESS",
    "G_B_PLUS_XREF",
    "G_C_PLUS_DECLARED",
    "G_D_PLUS_SHARED_TOKEN",
    "G_E_COUNT_GE4",
    "G_F_ROOT_RATIO_GT1",
)
FROZEN_SEED = 20260903
ORACLE_ACTIVE_STRATA = {"PDS1A", "PDS1C"}


class DesignViolation(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# io helpers
# ---------------------------------------------------------------------------

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# gate input: oracle stripping + witness features
# ---------------------------------------------------------------------------

def strip_forbidden(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: strip_forbidden(v) for k, v in value.items() if k not in FORBIDDEN_KEYS}
    if isinstance(value, list):
        return [strip_forbidden(v) for v in value]
    return value


def evidence_records(task: dict[str, Any]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if "lineage_root" in node and "replay_hash" in node:
                found.append(node)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(task)
    return found


def witness_features(task: dict[str, Any]) -> dict[str, Any]:
    recs = evidence_records(strip_forbidden(task))
    hashes = [str(r.get("replay_hash")) for r in recs]
    roots = [str(r.get("lineage_root")) for r in recs]
    texts = [str(r.get("method_text", "")) for r in recs]
    n = len(recs)
    n_roots = len(set(roots))
    w_dup_hash = len(hashes) != len(set(hashes))
    w_shared_root = len(roots) != len(set(roots))
    w_declared_overlap = any(r.get("declared_overlap") for r in recs)
    w_xref_root = any(roots[j] in texts[i] for i in range(n) for j in range(n) if i != j)
    token_records: dict[str, set[int]] = {}
    for i, text in enumerate(texts):
        for tok in set(TOKEN_RE.findall(text)):
            token_records.setdefault(tok, set()).add(i)
    w_shared_token = any(len(idx) >= 2 for idx in token_records.values())
    return {
        "w_dup_hash": w_dup_hash,
        "w_shared_root": w_shared_root,
        "w_declared_overlap": w_declared_overlap,
        "w_xref_root": w_xref_root,
        "w_shared_token": w_shared_token,
        "n_records": n,
        "n_roots": n_roots,
        "root_ratio": (n / n_roots) if n_roots else 0.0,
    }


def gate_fires(gate_id: str, f: dict[str, Any]) -> bool:
    g_a = bool(f["w_dup_hash"] or f["w_shared_root"])
    g_b = g_a or bool(f["w_xref_root"])
    g_c = g_b or bool(f["w_declared_overlap"])
    if gate_id == "G_A_PROVENANCE_WITNESS":
        return g_a
    if gate_id == "G_B_PLUS_XREF":
        return g_b
    if gate_id == "G_C_PLUS_DECLARED":
        return g_c
    if gate_id == "G_D_PLUS_SHARED_TOKEN":
        return g_c or bool(f["w_shared_token"])
    if gate_id == "G_E_COUNT_GE4":
        return int(f["n_records"]) >= 4
    if gate_id == "G_F_ROOT_RATIO_GT1":
        return float(f["root_ratio"]) > 1.0
    raise DesignViolation(f"unknown gate {gate_id}")


def canary_check(task: dict[str, Any]) -> None:
    """Injected oracle-shaped keys must not change any candidate gate output."""
    base = witness_features(task)
    poisoned = copy.deepcopy(task)
    poisoned["stratum"] = "PDS1A"
    poisoned["expected"] = {"decision": "ACCEPT_H"}
    poisoned["strata"] = {task.get("task_id", "x"): "PDS1C"}
    poisoned["oracle"] = {"answers": {"decision": "REJECT_H"}}
    for rec in evidence_records(poisoned):
        rec["correct"] = False
        rec["actual"] = {"decision": "ACCEPT_H"}
    after = witness_features(poisoned)
    for gate in CANDIDATE_GATES:
        if gate_fires(gate, base) != gate_fires(gate, after):
            raise DesignViolation(f"canary failed: gate {gate} changed under injected oracle keys on {task.get('task_id')}")


# ---------------------------------------------------------------------------
# extraction: campaign root -> per-instance table
# ---------------------------------------------------------------------------

def extract_instances(campaign_root: Path, arms: tuple[str, ...] = (ARM_M, ARM_OFF, ARM_PARENT)) -> dict[str, Any]:
    studies = sorted(p for p in campaign_root.iterdir() if p.is_dir() and (p / "public_tasks.json").exists())
    if not studies:
        raise DesignViolation(f"no prepared studies under {campaign_root}")
    rows: list[dict[str, Any]] = []
    seeds: dict[str, int] = {}
    for study_dir in studies:
        freeze = read_json(study_dir / "FROZEN_SUITE.json")
        seeds[study_dir.name] = int(freeze["seed"])
        tasks = {t["task_id"]: t for t in read_json(study_dir / "public_tasks.json")["tasks"]}
        oracle = read_json(study_dir / "private_oracle.json")
        strata = oracle.get("strata", {})
        eval_rows = read_json(study_dir / "EVALUATION_ROWS.json") if (study_dir / "EVALUATION_ROWS.json").exists() else []
        by_task_arm = {(r["task_id"], r["arm"]): r for r in eval_rows}
        for task_id, task in sorted(tasks.items()):
            canary_check(task)
            feats = witness_features(task)
            arm_block: dict[str, Any] = {}
            for arm in arms:
                row = by_task_arm.get((task_id, arm))
                resp_path = study_dir / "responses" / arm / f"{task_id}.json"
                wall = None
                calls = None
                if resp_path.exists():
                    receipt = read_json(resp_path).get("resource_receipt") or {}
                    wall = receipt.get("wall_time_seconds")
                    calls = receipt.get("model_calls")
                arm_block[arm] = {
                    "present": row is not None and not row.get("missing"),
                    "correct": bool(row["correct"]) if row is not None and not row.get("missing") else None,
                    "wall_time_seconds": wall,
                    "model_calls": calls,
                }
            rows.append({
                "task_id": task_id,
                "study_id": study_dir.name,
                "features": feats,
                "arms": arm_block,
                "oracle_stratum_reporting_only": strata.get(task_id),
            })
    return {
        "schema_version": "orion.v2.h-ext1-instances.v1",
        "campaign_root": str(campaign_root),
        "study_seeds": seeds,
        "arms": list(arms),
        "n": len(rows),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# development split + selection
# ---------------------------------------------------------------------------

def split_parity(task_id: str) -> int:
    return hashlib.sha256(task_id.encode("utf-8")).digest()[0] % 2


def dev_rows(instances: dict[str, Any]) -> list[dict[str, Any]]:
    return [r for r in instances["rows"] if split_parity(r["task_id"]) == 0]


def eval_rows_retro(instances: dict[str, Any]) -> list[dict[str, Any]]:
    return [r for r in instances["rows"] if split_parity(r["task_id"]) == 1]


def scored(rows: list[dict[str, Any]], arms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [r for r in rows if all(r["arms"].get(a, {}).get("present") for a in arms)]


def accuracy(rows: list[dict[str, Any]], arm: str) -> float:
    return sum(1 for r in rows if r["arms"][arm]["correct"]) / len(rows) if rows else 0.0


def gated_accuracy(rows: list[dict[str, Any]], active: list[bool]) -> float:
    hits = 0
    for r, on in zip(rows, active):
        hits += 1 if r["arms"][ARM_M if on else ARM_OFF]["correct"] else 0
    return hits / len(rows) if rows else 0.0


def gated_mean_wall(rows: list[dict[str, Any]], active: list[bool]) -> float | None:
    vals = []
    for r, on in zip(rows, active):
        w = r["arms"][ARM_M if on else ARM_OFF]["wall_time_seconds"]
        if w is not None:
            vals.append(float(w))
    return statistics.mean(vals) if vals else None


def mean_wall(rows: list[dict[str, Any]], arm: str) -> float | None:
    vals = [float(r["arms"][arm]["wall_time_seconds"]) for r in rows if r["arms"][arm]["wall_time_seconds"] is not None]
    return statistics.mean(vals) if vals else None


def develop(instances: dict[str, Any], design_path: Path) -> dict[str, Any]:
    rows = scored(dev_rows(instances), (ARM_M, ARM_OFF))
    if not rows:
        raise DesignViolation("development split has no scored rows")
    base = max(accuracy(rows, ARM_M), accuracy(rows, ARM_OFF))
    table = []
    for gate in CANDIDATE_GATES:
        active = [gate_fires(gate, r["features"]) for r in rows]
        acc = gated_accuracy(rows, active)
        table.append({
            "gate_id": gate,
            "dev_accuracy": acc,
            "dev_advantage": acc - base,
            "activation_rate": sum(active) / len(rows),
            "activations": sum(active),
        })
    ranked = sorted(
        enumerate(table),
        key=lambda it: (-it[1]["dev_advantage"], it[1]["activation_rate"], it[0]),
    )
    best = ranked[0][1]
    selected = best["gate_id"] if best["dev_advantage"] > 0 else None
    return {
        "schema_version": "orion.v2.h-ext1-gate-freeze.v1",
        "design_sha256": sha256_path(design_path),
        "dev_cell": "RETROSPECTIVE_DEV",
        "dev_n": len(rows),
        "dev_task_ids_sha256": sha256_text(",".join(sorted(r["task_id"] for r in rows))),
        "dev_acc_M": accuracy(rows, ARM_M),
        "dev_acc_OFF": accuracy(rows, ARM_OFF),
        "candidates": table,
        "selected_gate": selected,
        "terminal_if_none": None if selected else "NO_CANDIDATE_GATE_ON_DEV",
        "gate_sha256": sha256_text(json.dumps({"gate": selected, "features": sorted(witness_features({}).keys()), "regex": TOKEN_RE.pattern}, sort_keys=True)) if selected else None,
        "no_rescue": True,
    }


# ---------------------------------------------------------------------------
# evaluation
# ---------------------------------------------------------------------------

def null_distribution(rows: list[dict[str, Any]], n_active: int, draws: int, seed: int, within_study: bool,
                      per_study_counts: dict[str, int] | None = None) -> list[float]:
    rng = random.Random(seed)
    base = max(accuracy(rows, ARM_M), accuracy(rows, ARM_OFF))
    idx_by_study: dict[str, list[int]] = {}
    for i, r in enumerate(rows):
        idx_by_study.setdefault(r["study_id"], []).append(i)
    out = []
    for _ in range(draws):
        active = [False] * len(rows)
        if within_study:
            for study, idxs in idx_by_study.items():
                k = min((per_study_counts or {}).get(study, 0), len(idxs))
                for i in rng.sample(idxs, k):
                    active[i] = True
        else:
            for i in rng.sample(range(len(rows)), min(n_active, len(rows))):
                active[i] = True
        out.append(gated_accuracy(rows, active) - base)
    return out


def percentile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(round(q * (len(s) - 1)))))
    return s[k]


def evaluate_cell(instances: dict[str, Any], freeze: dict[str, Any], cell: str, design: dict[str, Any],
                  frozen_dev_ids_sha: str | None = None, dev_ids: set[str] | None = None) -> dict[str, Any]:
    gate = freeze["selected_gate"]
    if gate is None:
        raise DesignViolation("no frozen gate; evaluation not permitted")
    if cell == "RETROSPECTIVE_EVAL":
        rows_all = eval_rows_retro(instances)
    elif cell == "PROSPECTIVE":
        rows_all = list(instances["rows"])
    else:
        raise DesignViolation(f"unknown cell {cell}")
    arms = (ARM_M, ARM_OFF, ARM_PARENT)
    missing = [r["task_id"] for r in rows_all if not all(r["arms"].get(a, {}).get("present") for a in arms)]
    result: dict[str, Any] = {
        "schema_version": "orion.v2.h-ext1-cell-result.v1",
        "cell": cell,
        "gate_id": gate,
        "gate_sha256": freeze["gate_sha256"],
        "n_total": len(rows_all),
        "n_missing": len(missing),
        "missing_task_ids": missing[:50],
    }
    if cell == "PROSPECTIVE" and missing:
        result["terminal"] = "CANNOT_CHECK_PROSPECTIVE_RUN_INVALID"
        result["gates"] = {}
        return result
    rows = scored(rows_all, arms)
    if not rows:
        result["terminal"] = "CANNOT_CHECK_PROSPECTIVE_RUN_INVALID" if cell == "PROSPECTIVE" else "DESIGN_VIOLATION_RUN_VOID"
        result["gates"] = {}
        return result
    # G0 validity
    g0_reasons = []
    ids = {r["task_id"] for r in rows}
    if dev_ids is not None and ids & dev_ids and cell == "RETROSPECTIVE_EVAL":
        g0_reasons.append("dev/eval overlap")
    if cell == "PROSPECTIVE":
        seeds = set(instances.get("study_seeds", {}).values())
        if not seeds:
            g0_reasons.append("no seed recorded")
        # the frozen campaign derived study seeds from base 20260903; a prospective root
        # must not reuse ANY of the frozen study seeds
        frozen_study_seeds = set(design.get("_frozen_study_seeds", []))
        if seeds & frozen_study_seeds:
            g0_reasons.append("prospective root reuses a frozen study seed")
    if missing and cell == "RETROSPECTIVE_EVAL":
        g0_reasons.append(f"{len(missing)} rows missing an arm")
    active = [gate_fires(gate, r["features"]) for r in rows]
    n_active = sum(active)
    acc_m, acc_off, acc_parent = accuracy(rows, ARM_M), accuracy(rows, ARM_OFF), accuracy(rows, ARM_PARENT)
    acc_g = gated_accuracy(rows, active)
    base = max(acc_m, acc_off)
    advantage = acc_g - base
    wall_m, wall_g = mean_wall(rows, ARM_M), gated_mean_wall(rows, active)
    calls_m = sum(int(r["arms"][ARM_M]["model_calls"] or 0) for r in rows)
    calls_g = sum(int(r["arms"][ARM_M if on else ARM_OFF]["model_calls"] or 0) for r, on in zip(rows, active))
    draws = int(design.get("null_draws", 2000))
    null_seed = int(design.get("null_seed", 20260902))
    per_study_counts: dict[str, int] = {}
    for r, on in zip(rows, active):
        per_study_counts[r["study_id"]] = per_study_counts.get(r["study_id"], 0) + (1 if on else 0)
    null_pooled = null_distribution(rows, n_active, draws, null_seed, False)
    null_within = null_distribution(rows, n_active, draws, null_seed + 1, True, per_study_counts)
    q95_pooled, q95_within = percentile(null_pooled, 0.95), percentile(null_within, 0.95)
    per_study = {}
    for study in sorted({r["study_id"] for r in rows}):
        sub = [(r, on) for r, on in zip(rows, active) if r["study_id"] == study]
        srows = [r for r, _ in sub]
        sact = [on for _, on in sub]
        per_study[study] = {
            "n": len(srows),
            "activations": sum(sact),
            "acc_M": accuracy(srows, ARM_M),
            "acc_OFF": accuracy(srows, ARM_OFF),
            "acc_PARENT": accuracy(srows, ARM_PARENT),
            "acc_GATED": gated_accuracy(srows, sact),
        }
    # reporting-only references (oracle stratum ceiling + study-id metadata gate)
    oracle_active = [str(r.get("oracle_stratum_reporting_only")) in ORACLE_ACTIVE_STRATA for r in rows]
    study_active = [r["study_id"].startswith("PD-S1") for r in rows]
    per_stratum = {}
    for r, on in zip(rows, active):
        s = str(r.get("oracle_stratum_reporting_only"))
        e = per_stratum.setdefault(s, {"n": 0, "activations": 0, "M": 0, "OFF": 0, "GATED": 0})
        e["n"] += 1
        e["activations"] += 1 if on else 0
        e["M"] += 1 if r["arms"][ARM_M]["correct"] else 0
        e["OFF"] += 1 if r["arms"][ARM_OFF]["correct"] else 0
        e["GATED"] += 1 if r["arms"][ARM_M if on else ARM_OFF]["correct"] else 0
    gates = {
        "G0_VALIDITY": {"pass": not g0_reasons, "reasons": g0_reasons},
        "G1_DOMINATES_ALWAYS_ON": {
            "pass": acc_g >= acc_m and calls_g <= calls_m and (wall_m is None or wall_g is None or wall_g <= 1.05 * wall_m),
            "acc_GATED": acc_g, "acc_M": acc_m, "calls_GATED": calls_g, "calls_M": calls_m,
            "mean_wall_GATED": wall_g, "mean_wall_M": wall_m,
        },
        "G2_DOMINATES_ALWAYS_OFF_AND_PARENT": {
            "pass_vs_OFF": acc_g > acc_off, "pass_vs_PARENT": acc_g >= acc_parent,
            "pass": acc_g > acc_off and acc_g >= acc_parent,
            "acc_OFF": acc_off, "acc_PARENT": acc_parent,
        },
        "G3_BEATS_SHUFFLE_NULL": {
            "pass": advantage > q95_pooled, "advantage": advantage, "null_q95": q95_pooled,
            "null_mean": statistics.mean(null_pooled), "null_max": max(null_pooled),
            "null_exceedance_fraction": sum(1 for v in null_pooled if v >= advantage) / len(null_pooled),
            "draws": draws,
        },
        "G3S_BEATS_WITHIN_STUDY_NULL": {
            "pass": advantage > q95_within, "advantage": advantage, "null_q95": q95_within,
            "null_mean": statistics.mean(null_within), "null_max": max(null_within),
            "null_exceedance_fraction": sum(1 for v in null_within if v >= advantage) / len(null_within),
            "draws": draws,
        },
        "G4_SIGN_CONSISTENCY": {
            "pass": all(v["acc_GATED"] >= max(v["acc_M"], v["acc_OFF"]) for v in per_study.values()),
            "per_study": per_study,
        },
    }
    result.update({
        "n_scored": len(rows),
        "activations": n_active,
        "activation_rate": n_active / len(rows),
        "gates": gates,
        "references_reporting_only": {
            "ORACLE_STRATUM_ceiling_acc": gated_accuracy(rows, oracle_active),
            "STUDY_ID_IS_PDS1_acc": gated_accuracy(rows, study_active),
            "per_oracle_stratum": per_stratum,
        },
        "terminal": route(gates, cell),
    })
    return result


def route(gates: dict[str, Any], cell: str) -> str:
    if not gates["G0_VALIDITY"]["pass"]:
        return "DESIGN_VIOLATION_RUN_VOID"
    if not gates["G1_DOMINATES_ALWAYS_ON"]["pass"]:
        return "GATING_DOES_NOT_DOMINATE_ALWAYS_ON"
    if not gates["G2_DOMINATES_ALWAYS_OFF_AND_PARENT"]["pass_vs_OFF"]:
        return "GATING_DOES_NOT_DOMINATE_ALWAYS_OFF"
    if not gates["G2_DOMINATES_ALWAYS_OFF_AND_PARENT"]["pass_vs_PARENT"]:
        return "STRONGEST_PARENT_SUFFICIENT_UNDER_GATING"
    if not gates["G3_BEATS_SHUFFLE_NULL"]["pass"]:
        return "ACTIVATION_POLICY_NOT_IDENTIFIABLE_FROM_INPUTS"
    if not gates["G4_SIGN_CONSISTENCY"]["pass"]:
        return "ACTIVATION_ADVANTAGE_NOT_SIGN_CONSISTENT"
    if not gates["G3S_BEATS_WITHIN_STUDY_NULL"]["pass"]:
        return "ACTIVATION_POLICY_IDENTIFIABLE_ONLY_AT_STUDY_GRANULARITY"
    return "CONDITIONAL_ACTIVATION_IDENTIFIABLE_FROM_EVIDENCE_STRUCTURE"


# ---------------------------------------------------------------------------
# rollup
# ---------------------------------------------------------------------------

def rollup(freeze: dict[str, Any], cells: dict[str, dict[str, Any]], design_path: Path) -> dict[str, Any]:
    prospective = cells.get("PROSPECTIVE")
    retro = cells.get("RETROSPECTIVE_EVAL")
    binding = prospective["terminal"] if prospective else "CANNOT_CHECK_PROSPECTIVE_RUN_INVALID"
    return {
        "schema_version": "orion.v2.h-ext1-rollup.v1",
        "hypothesis_id": "H-EXT-1",
        "design_sha256": sha256_path(design_path),
        "gate_freeze": {k: freeze[k] for k in ("selected_gate", "gate_sha256", "dev_n", "dev_task_ids_sha256", "design_sha256")},
        "cells": cells,
        "binding_cell": "PROSPECTIVE",
        "binding_terminal": binding,
        "retrospective_terminal": retro["terminal"] if retro else None,
        "cells_agree": (retro["terminal"] == binding) if (retro and prospective) else None,
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_real_corpus_dependence_detection": False, "grants_manuscript_change": False},
    }


def fmt(v: Any) -> str:
    return f"{v:.4f}" if isinstance(v, float) else str(v)


def rollup_markdown(roll: dict[str, Any]) -> str:
    lines = ["# H-EXT-1 Rollup V1", "",
             f"Design sha256 `{roll['design_sha256'][:16]}`; frozen gate **{roll['gate_freeze']['selected_gate']}** "
             f"(gate sha `{str(roll['gate_freeze']['gate_sha256'])[:16]}`, dev n={roll['gate_freeze']['dev_n']}).", "",
             f"**Binding terminal (PROSPECTIVE): `{roll['binding_terminal']}`**", ""]
    for cell_name, cell in roll["cells"].items():
        lines += [f"## {cell_name}", "", f"Terminal: `{cell['terminal']}` — scored {cell.get('n_scored', 0)}/{cell['n_total']}, "
                  f"activations {cell.get('activations', 0)} ({fmt(cell.get('activation_rate', 0.0))})", ""]
        gates = cell.get("gates", {})
        if not gates:
            lines += [f"Missing arm responses on {cell['n_missing']} tasks; nothing inferred.", ""]
            continue
        g1, g2, g3, g3s, g4 = (gates[k] for k in ("G1_DOMINATES_ALWAYS_ON", "G2_DOMINATES_ALWAYS_OFF_AND_PARENT",
                                                  "G3_BEATS_SHUFFLE_NULL", "G3S_BEATS_WITHIN_STUDY_NULL", "G4_SIGN_CONSISTENCY"))
        lines += ["| Gate | Pass | Detail |", "|---|---|---|",
                  f"| G0 | {gates['G0_VALIDITY']['pass']} | {'; '.join(gates['G0_VALIDITY']['reasons']) or 'clean'} |",
                  f"| G1 | {g1['pass']} | GATED {fmt(g1['acc_GATED'])} vs M {fmt(g1['acc_M'])}; calls {g1['calls_GATED']} vs {g1['calls_M']}; wall {fmt(g1['mean_wall_GATED'])} vs {fmt(g1['mean_wall_M'])} |",
                  f"| G2 | {g2['pass']} | vs OFF {fmt(g2['acc_OFF'])} ({g2['pass_vs_OFF']}); vs PARENT {fmt(g2['acc_PARENT'])} ({g2['pass_vs_PARENT']}) |",
                  f"| G3 | {g3['pass']} | advantage {fmt(g3['advantage'])} vs pooled-null q95 {fmt(g3['null_q95'])} (mean {fmt(g3['null_mean'])}, max {fmt(g3['null_max'])}, exceedance {fmt(g3['null_exceedance_fraction'])}, {g3['draws']} draws) |",
                  f"| G3S | {g3s['pass']} | vs within-study-null q95 {fmt(g3s['null_q95'])} (mean {fmt(g3s['null_mean'])}, max {fmt(g3s['null_max'])}, exceedance {fmt(g3s['null_exceedance_fraction'])}) |",
                  f"| G4 | {g4['pass']} | per-study below |", "",
                  "| Study | n | act | M | OFF | PARENT | GATED |", "|---|---|---|---|---|---|---|"]
        for s, v in g4["per_study"].items():
            lines.append(f"| {s} | {v['n']} | {v['activations']} | {fmt(v['acc_M'])} | {fmt(v['acc_OFF'])} | {fmt(v['acc_PARENT'])} | {fmt(v['acc_GATED'])} |")
        refs = cell.get("references_reporting_only", {})
        lines += ["", f"Reporting-only references: oracle-stratum ceiling {fmt(refs.get('ORACLE_STRATUM_ceiling_acc'))}, "
                  f"study-id metadata gate {fmt(refs.get('STUDY_ID_IS_PDS1_acc'))}.", "",
                  "| Oracle stratum (reporting only) | n | act | M | OFF | GATED |", "|---|---|---|---|---|---|"]
        for s, v in sorted(refs.get("per_oracle_stratum", {}).items()):
            lines.append(f"| {s} | {v['n']} | {v['activations']} | {v['M']} | {v['OFF']} | {v['GATED']} |")
        lines.append("")
    lines += [f"Cells agree: {roll['cells_agree']}. Authority: all grants false.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--campaign-root", type=Path, required=True)
    e.add_argument("--out", type=Path, required=True)
    d = sub.add_parser("develop")
    d.add_argument("--instances", type=Path, required=True)
    d.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    d.add_argument("--out", type=Path, required=True)
    ev = sub.add_parser("evaluate")
    ev.add_argument("--instances", type=Path, required=True)
    ev.add_argument("--freeze", type=Path, required=True)
    ev.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    ev.add_argument("--cell", choices=("RETROSPECTIVE_EVAL", "PROSPECTIVE"), required=True)
    ev.add_argument("--dev-instances", type=Path, default=None)
    ev.add_argument("--out", type=Path, required=True)
    a = sub.add_parser("all")
    a.add_argument("--retro-root", type=Path, required=True)
    a.add_argument("--prospective-root", type=Path, default=None)
    a.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    a.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args(argv)

    if args.command == "extract":
        write_json(args.out, extract_instances(args.campaign_root))
        return 0
    if args.command == "develop":
        freeze = develop(read_json(args.instances), args.design)
        write_json(args.out, freeze)
        print(json.dumps({"selected_gate": freeze["selected_gate"], "terminal_if_none": freeze["terminal_if_none"]}))
        return 0 if freeze["selected_gate"] else 4
    if args.command == "evaluate":
        design = read_json(args.design)
        inst = read_json(args.instances)
        dev_ids = None
        if args.dev_instances is not None:
            dev_ids = {r["task_id"] for r in dev_rows(read_json(args.dev_instances))}
        res = evaluate_cell(inst, read_json(args.freeze), args.cell, design, dev_ids=dev_ids)
        write_json(args.out, res)
        print(json.dumps({"cell": args.cell, "terminal": res["terminal"]}))
        return 0
    # all
    out = args.out_dir
    design = read_json(args.design)
    retro = extract_instances(args.retro_root)
    write_json(out / "data" / "RETROSPECTIVE_instances.json", retro)
    freeze = develop(retro, args.design)
    write_json(out / "H_EXT1_GATE_FREEZE.json", freeze)
    if not freeze["selected_gate"]:
        write_json(out / "H_EXT1_ROLLUP_V1.json", {"binding_terminal": "NO_CANDIDATE_GATE_ON_DEV", "gate_freeze": freeze})
        print("NO_CANDIDATE_GATE_ON_DEV")
        return 4
    design["_frozen_study_seeds"] = sorted(retro["study_seeds"].values())
    dev_ids = {r["task_id"] for r in dev_rows(retro)}
    cells: dict[str, Any] = {}
    cells["RETROSPECTIVE_EVAL"] = evaluate_cell(retro, freeze, "RETROSPECTIVE_EVAL", design, dev_ids=dev_ids)
    write_json(out / "H_EXT1_CELL_RETROSPECTIVE_EVAL.json", cells["RETROSPECTIVE_EVAL"])
    if args.prospective_root is not None:
        pro = extract_instances(args.prospective_root)
        write_json(out / "data" / "PROSPECTIVE_instances.json", pro)
        cells["PROSPECTIVE"] = evaluate_cell(pro, freeze, "PROSPECTIVE", design)
        write_json(out / "H_EXT1_CELL_PROSPECTIVE.json", cells["PROSPECTIVE"])
    roll = rollup(freeze, cells, args.design)
    write_json(out / "H_EXT1_ROLLUP_V1.json", roll)
    (out / "H_EXT1_ROLLUP_V1.md").write_text(rollup_markdown(roll), encoding="utf-8")
    print(json.dumps({"binding_terminal": roll["binding_terminal"], "retrospective_terminal": roll["retrospective_terminal"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
