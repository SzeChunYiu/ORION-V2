#!/usr/bin/env python3
"""H-EXT-1N naturalistic replication of the conditional-activation gate study (design V1).

Same six witness types as H-EXT-1, re-instantiated on naturalistic record fields; same
gate family, selection rule, nulls, gates G0-G4 and no-rescue clause. Gate logic,
accuracy/cost aggregation, null percentile and the planted-suite canary pattern are
IMPORTED from scripts/h_ext1_gate_study.py; only the feature extraction (naturalistic
fields), the split handling (frozen DEV/EVAL study dirs instead of task-id parity),
the within-metadata null and the naturalistic terminal names are new.

Design: research/experiments/h-ext1-naturalistic/H_EXT1N_DESIGN_V1.{md,json}.
Grants nothing; routes to pre-registered terminals.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "research/experiments/h-ext1-naturalistic/H_EXT1N_DESIGN_V1.json"
H1_PATH = ROOT / "scripts/h_ext1_gate_study.py"


def _load_h1():
    spec = importlib.util.spec_from_file_location("h_ext1_gate_study", H1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/h_ext1_gate_study.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


H1 = _load_h1()
ARM_M, ARM_OFF, ARM_PARENT = H1.ARM_M, H1.ARM_OFF, H1.ARM_PARENT
CANDIDATE_GATES = H1.CANDIDATE_GATES
TOKEN_RE = H1.TOKEN_RE  # identical uppercase-token regex to H-EXT-1
gate_fires = H1.gate_fires
accuracy, gated_accuracy = H1.accuracy, H1.gated_accuracy
mean_wall, gated_mean_wall = H1.mean_wall, H1.gated_mean_wall
percentile, scored = H1.percentile, H1.scored
read_json, write_json, sha256_path, sha256_text = H1.read_json, H1.write_json, H1.sha256_path, H1.sha256_text
DesignViolation = H1.DesignViolation

FORBIDDEN_KEYS = set(H1.FORBIDDEN_KEYS) | {"pmid", "doi", "nct", "ncts", "registry_ids", "split"}
ORACLE_ACTIVE_STRATA = {"NS1A", "NS1C"}
DECLARED_RE = re.compile(
    r"\b(secondary|post[- ]?hoc|pre-?specified|exploratory|ancillary|extension|sub-?study|follow-up|"
    r"long-term follow-up|pooled|subgroup)\s+(analysis|analyses|study|studies|report|results)\b",
    re.IGNORECASE,
)
NATURALISTIC_TERMINALS = {
    "G3_FAIL": "ACTIVATION_POLICY_NOT_IDENTIFIABLE_IN_NATURALISTIC_RECORDS",
    "G3S_FAIL": "ACTIVATION_POLICY_IDENTIFIABLE_ONLY_AT_METADATA_GRANULARITY",
    "PASS": "CONDITIONAL_ACTIVATION_IDENTIFIABLE_IN_NATURALISTIC_RECORDS",
}


# ---------------------------------------------------------------------------
# naturalistic witness features (same six witness types as H-EXT-1)
# ---------------------------------------------------------------------------

def strip_forbidden(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: strip_forbidden(v) for k, v in value.items() if k not in FORBIDDEN_KEYS}
    if isinstance(value, list):
        return [strip_forbidden(v) for v in value]
    return value


def evidence_records(task: dict[str, Any]) -> list[dict[str, Any]]:
    recs = task.get("records")
    if not isinstance(recs, list):
        return []
    return [r for r in recs if isinstance(r, dict) and "title" in r and "abstract" in r]


def _norm_author(name: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()


def _components(n: int, links: list[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in links:
        parent[find(a)] = find(b)
    return len({find(i) for i in range(n)})


def witness_features(task: dict[str, Any]) -> dict[str, Any]:
    """Keys deliberately identical to H-EXT-1's so H1.gate_fires applies unchanged.

    w_dup_hash      <- duplicate identifier: two records share a visible grant id
    w_shared_root   <- shared lineage root: two records share the same last (senior) author
    w_declared_overlap <- a record's text declares a secondary/post-hoc/sub-study relation
    w_xref_root     <- text cross-reference: an uppercase token from one record's TITLE
                       (the naturalistic 'root name', typically the trial acronym) occurs in
                       another record's title or abstract
    w_shared_token  <- an uppercase token occurs in >=2 records' full text (title+abstract)
    n_records, n_roots (author-link components), root_ratio = n_records / n_roots
    """
    recs = evidence_records(strip_forbidden(task))
    n = len(recs)
    titles = [str(r.get("title", "")) for r in recs]
    texts = [str(r.get("title", "")) + " " + str(r.get("abstract", "")) for r in recs]
    authors = [[_norm_author(a) for a in (r.get("authors") or []) if _norm_author(a)] for r in recs]
    last_authors = [a[-1] if a else "" for a in authors]
    grants = [{str(g).strip().upper() for g in (r.get("grant_ids") or []) if str(g).strip()} for r in recs]
    w_dup_hash = any(grants[i] & grants[j] for i in range(n) for j in range(i + 1, n))
    w_shared_root = any(last_authors[i] and last_authors[i] == last_authors[j] for i in range(n) for j in range(i + 1, n))
    w_declared_overlap = any(DECLARED_RE.search(t) for t in texts)
    title_tokens = [set(TOKEN_RE.findall(t)) for t in titles]
    w_xref_root = any(tok in texts[j] for i in range(n) for j in range(n) if i != j for tok in title_tokens[i])
    token_records: dict[str, set[int]] = {}
    for i, text in enumerate(texts):
        for tok in set(TOKEN_RE.findall(text)):
            token_records.setdefault(tok, set()).add(i)
    w_shared_token = any(len(idx) >= 2 for idx in token_records.values())
    links = [(i, j) for i in range(n) for j in range(i + 1, n) if set(authors[i]) & set(authors[j])]
    n_roots = _components(n, links) if n else 0
    return {
        "w_dup_hash": bool(w_dup_hash),
        "w_shared_root": bool(w_shared_root),
        "w_declared_overlap": bool(w_declared_overlap),
        "w_xref_root": bool(w_xref_root),
        "w_shared_token": bool(w_shared_token),
        "n_records": n,
        "n_roots": n_roots,
        "root_ratio": (n / n_roots) if n_roots else 0.0,
    }


def canary_check(task: dict[str, Any]) -> None:
    """Injected oracle-shaped keys (stratum, expected, registry ids, pmids) must not change
    any candidate gate's output."""
    base = witness_features(task)
    poisoned = copy.deepcopy(task)
    poisoned["stratum"] = "NS1A"
    poisoned["expected"] = {"decision": "ACCEPT_H"}
    poisoned["oracle"] = {"ncts_by_record": {"r1": "NCT00000001", "r2": "NCT00000001"}}
    poisoned["split"] = "EVAL"
    for rec in evidence_records(poisoned):
        rec["nct"] = "NCT00000001"
        rec["pmid"] = "12345678"
        rec["correct"] = False
    after = witness_features(poisoned)
    for gate in CANDIDATE_GATES:
        if gate_fires(gate, base) != gate_fires(gate, after):
            raise DesignViolation(f"canary failed: gate {gate} changed under injected oracle keys on {task.get('task_id')}")


def size_class(task: dict[str, Any]) -> str:
    return f"N1-K{len(evidence_records(task))}"


# ---------------------------------------------------------------------------
# extraction: study dir -> per-instance table
# ---------------------------------------------------------------------------

def extract_instances(study_dir: Path, arms: tuple[str, ...] = (ARM_M, ARM_OFF, ARM_PARENT)) -> dict[str, Any]:
    if not (study_dir / "public_tasks.json").exists():
        raise DesignViolation(f"no prepared study under {study_dir}")
    freeze = read_json(study_dir / "FROZEN_SUITE.json")
    tasks = {t["task_id"]: t for t in read_json(study_dir / "public_tasks.json")["tasks"]}
    oracle = read_json(study_dir / "private_oracle.json")
    strata = oracle.get("strata", {})
    eval_rows = read_json(study_dir / "EVALUATION_ROWS.json") if (study_dir / "EVALUATION_ROWS.json").exists() else []
    by_task_arm = {(r["task_id"], r["arm"]): r for r in eval_rows}
    rows = []
    for task_id, task in sorted(tasks.items()):
        canary_check(task)
        feats = witness_features(task)
        arm_block: dict[str, Any] = {}
        for arm in arms:
            row = by_task_arm.get((task_id, arm))
            resp_path = study_dir / "responses" / arm / f"{task_id}.json"
            wall = calls = None
            if resp_path.exists():
                receipt = read_json(resp_path).get("resource_receipt") or {}
                wall = receipt.get("wall_time_seconds")
                calls = receipt.get("model_calls")
            present = row is not None and not row.get("missing")
            arm_block[arm] = {
                "present": present,
                "correct": bool(row["correct"]) if present else None,
                "actual": row.get("actual") if present else None,
                "wall_time_seconds": wall,
                "model_calls": calls,
            }
        rows.append({
            "task_id": task_id,
            "study_id": size_class(task),
            "topic": task.get("topic"),
            "null_stratum": f"{task.get('topic')}|{size_class(task)}",
            "features": feats,
            "arms": arm_block,
            "oracle_stratum_reporting_only": strata.get(task_id),
        })
    return {
        "schema_version": "orion.v2.h-ext1n-instances.v1",
        "study_dir": str(study_dir),
        "split": freeze.get("split"),
        "seed": freeze.get("seed"),
        "corpus_freeze_sha256": freeze.get("corpus_freeze_sha256"),
        "arms": list(arms),
        "n": len(rows),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# development (DEV split only) -> gate freeze
# ---------------------------------------------------------------------------

def develop(dev_instances: dict[str, Any], design_path: Path) -> dict[str, Any]:
    if dev_instances.get("split") != "DEV":
        raise DesignViolation("develop() accepts the DEV split only")
    rows = scored(dev_instances["rows"], (ARM_M, ARM_OFF))
    if not rows:
        raise DesignViolation("development split has no scored rows")
    base = max(accuracy(rows, ARM_M), accuracy(rows, ARM_OFF))
    table = []
    for gate in CANDIDATE_GATES:
        active = [gate_fires(gate, r["features"]) for r in rows]
        acc = gated_accuracy(rows, active)
        table.append({"gate_id": gate, "dev_accuracy": acc, "dev_advantage": acc - base,
                      "activation_rate": sum(active) / len(rows), "activations": sum(active)})
    ranked = sorted(enumerate(table), key=lambda it: (-it[1]["dev_advantage"], it[1]["activation_rate"], it[0]))
    best = ranked[0][1]
    selected = best["gate_id"] if best["dev_advantage"] > 0 else None
    feature_spec = {"gate": selected, "features": sorted(witness_features({"records": []}).keys()),
                    "token_regex": TOKEN_RE.pattern, "declared_regex": DECLARED_RE.pattern,
                    "root": "last-author (shared_root); author-link components (n_roots)",
                    "dup_identifier": "shared grant_id"}
    return {
        "schema_version": "orion.v2.h-ext1n-gate-freeze.v1",
        "design_sha256": sha256_path(design_path),
        "corpus_freeze_sha256": dev_instances.get("corpus_freeze_sha256"),
        "dev_cell": "N1-DEV",
        "dev_n": len(rows),
        "dev_task_ids_sha256": sha256_text(",".join(sorted(r["task_id"] for r in rows))),
        "dev_acc_M": accuracy(rows, ARM_M),
        "dev_acc_OFF": accuracy(rows, ARM_OFF),
        "dev_acc_PARENT": accuracy(scored(dev_instances["rows"], (ARM_PARENT,)), ARM_PARENT),
        "candidates": table,
        "selected_gate": selected,
        "terminal_if_none": None if selected else "NO_CANDIDATE_GATE_ON_DEV",
        "gate_sha256": sha256_text(json.dumps(feature_spec, sort_keys=True)) if selected else None,
        "feature_spec": feature_spec,
        "no_rescue": True,
    }


# ---------------------------------------------------------------------------
# evaluation (EVAL split) with pooled and within-metadata nulls
# ---------------------------------------------------------------------------

def null_distribution(rows: list[dict[str, Any]], active: list[bool], draws: int, seed: int, key: str | None) -> list[float]:
    """Random gates with the selected gate's activation count, pooled (key=None) or matched
    inside each arm-visible metadata cell rows[i][key] (topic x size class)."""
    rng = random.Random(seed)
    base = max(accuracy(rows, ARM_M), accuracy(rows, ARM_OFF))
    groups: dict[str, list[int]] = {}
    counts: dict[str, int] = {}
    for i, (r, on) in enumerate(zip(rows, active)):
        g = str(r[key]) if key else "_all"
        groups.setdefault(g, []).append(i)
        counts[g] = counts.get(g, 0) + (1 if on else 0)
    out = []
    for _ in range(draws):
        rand_active = [False] * len(rows)
        for g, idxs in groups.items():
            for i in rng.sample(idxs, min(counts[g], len(idxs))):
                rand_active[i] = True
        out.append(gated_accuracy(rows, rand_active) - base)
    return out


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p from discordant counts (b: M-only correct, c: OFF-only)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * p)


def evaluate(eval_instances: dict[str, Any], freeze: dict[str, Any], design: dict[str, Any],
             dev_ids: set[str], corpus_freeze_sha256: str | None) -> dict[str, Any]:
    gate = freeze["selected_gate"]
    if gate is None:
        raise DesignViolation("no frozen gate; evaluation not permitted")
    rows_all = list(eval_instances["rows"])
    arms = (ARM_M, ARM_OFF, ARM_PARENT)
    missing = [r["task_id"] for r in rows_all if not all(r["arms"].get(a, {}).get("present") for a in arms)]
    result: dict[str, Any] = {
        "schema_version": "orion.v2.h-ext1n-cell-result.v1",
        "cell": "N1-EVAL", "gate_id": gate, "gate_sha256": freeze["gate_sha256"],
        "n_total": len(rows_all), "n_missing": len(missing), "missing_task_ids": missing[:50],
    }
    if missing or not rows_all:
        result["terminal"] = "CANNOT_CHECK_RUN_INVALID"
        result["gates"] = {}
        return result
    rows = scored(rows_all, arms)
    g0_reasons = []
    ids = {r["task_id"] for r in rows}
    if ids & dev_ids:
        g0_reasons.append("dev/eval task-id overlap")
    if eval_instances.get("split") != "EVAL":
        g0_reasons.append("scored cell is not the EVAL split")
    if corpus_freeze_sha256 and eval_instances.get("corpus_freeze_sha256") != corpus_freeze_sha256:
        g0_reasons.append("eval study corpus freeze sha differs from the frozen corpus")
    if freeze.get("corpus_freeze_sha256") and freeze.get("corpus_freeze_sha256") != eval_instances.get("corpus_freeze_sha256"):
        g0_reasons.append("gate freeze and eval study were built from different corpora")
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
    null_pooled = null_distribution(rows, active, draws, null_seed, None)
    null_within = null_distribution(rows, active, draws, null_seed + 1, "null_stratum")
    q95_pooled, q95_within = percentile(null_pooled, 0.95), percentile(null_within, 0.95)
    per_study = {}
    for study in sorted({r["study_id"] for r in rows}):
        sub = [(r, on) for r, on in zip(rows, active) if r["study_id"] == study]
        srows, sact = [r for r, _ in sub], [on for _, on in sub]
        per_study[study] = {"n": len(srows), "activations": sum(sact), "acc_M": accuracy(srows, ARM_M),
                            "acc_OFF": accuracy(srows, ARM_OFF), "acc_PARENT": accuracy(srows, ARM_PARENT),
                            "acc_GATED": gated_accuracy(srows, sact)}
    per_topic = {}
    for topic in sorted({str(r["topic"]) for r in rows}):
        sub = [(r, on) for r, on in zip(rows, active) if str(r["topic"]) == topic]
        srows, sact = [r for r, _ in sub], [on for _, on in sub]
        per_topic[topic] = {"n": len(srows), "activations": sum(sact), "acc_M": accuracy(srows, ARM_M),
                            "acc_OFF": accuracy(srows, ARM_OFF), "acc_GATED": gated_accuracy(srows, sact)}
    oracle_active = [str(r.get("oracle_stratum_reporting_only")) in ORACLE_ACTIVE_STRATA for r in rows]
    per_stratum: dict[str, dict[str, int]] = {}
    for r, on in zip(rows, active):
        s = str(r.get("oracle_stratum_reporting_only"))
        e = per_stratum.setdefault(s, {"n": 0, "activations": 0, "M": 0, "OFF": 0, "PARENT": 0, "GATED": 0})
        e["n"] += 1
        e["activations"] += 1 if on else 0
        e["M"] += 1 if r["arms"][ARM_M]["correct"] else 0
        e["OFF"] += 1 if r["arms"][ARM_OFF]["correct"] else 0
        e["PARENT"] += 1 if r["arms"][ARM_PARENT]["correct"] else 0
        e["GATED"] += 1 if r["arms"][ARM_M if on else ARM_OFF]["correct"] else 0
    tp = sum(1 for on, oa in zip(active, oracle_active) if on and oa)
    fp = sum(1 for on, oa in zip(active, oracle_active) if on and not oa)
    fn = sum(1 for on, oa in zip(active, oracle_active) if not on and oa)
    b = sum(1 for r in rows if r["arms"][ARM_M]["correct"] and not r["arms"][ARM_OFF]["correct"])
    c = sum(1 for r in rows if r["arms"][ARM_OFF]["correct"] and not r["arms"][ARM_M]["correct"])
    gates = {
        "G0_VALIDITY": {"pass": not g0_reasons, "reasons": g0_reasons},
        "G1_DOMINATES_ALWAYS_ON": {
            "pass": acc_g >= acc_m and calls_g <= calls_m and (wall_m is None or wall_g is None or wall_g <= 1.05 * wall_m),
            "acc_GATED": acc_g, "acc_M": acc_m, "calls_GATED": calls_g, "calls_M": calls_m,
            "mean_wall_GATED": wall_g, "mean_wall_M": wall_m,
        },
        "G2_DOMINATES_ALWAYS_OFF_AND_PARENT": {
            "pass_vs_OFF": acc_g > acc_off, "pass_vs_PARENT": acc_g >= acc_parent,
            "pass": acc_g > acc_off and acc_g >= acc_parent, "acc_OFF": acc_off, "acc_PARENT": acc_parent,
        },
        "G3_BEATS_SHUFFLE_NULL": {
            "pass": advantage > q95_pooled, "advantage": advantage, "null_q95": q95_pooled,
            "null_mean": statistics.mean(null_pooled), "null_max": max(null_pooled),
            "null_exceedance_fraction": sum(1 for v in null_pooled if v >= advantage) / len(null_pooled), "draws": draws,
        },
        "G3S_BEATS_WITHIN_STUDY_NULL": {
            "null": "within topic x size-class (arm-visible metadata)",
            "pass": advantage > q95_within, "advantage": advantage, "null_q95": q95_within,
            "null_mean": statistics.mean(null_within), "null_max": max(null_within),
            "null_exceedance_fraction": sum(1 for v in null_within if v >= advantage) / len(null_within), "draws": draws,
        },
        "G4_SIGN_CONSISTENCY": {
            "unit": "size class (arm-visible n_records)",
            "pass": all(v["acc_GATED"] >= max(v["acc_M"], v["acc_OFF"]) for v in per_study.values()),
            "per_study": per_study,
        },
    }
    result.update({
        "n_scored": len(rows), "activations": n_active, "activation_rate": n_active / len(rows), "gates": gates,
        "references_reporting_only": {
            "ORACLE_STRATUM_ceiling_acc": gated_accuracy(rows, oracle_active),
            "per_oracle_stratum": per_stratum,
            "per_topic": per_topic,
            "activation_precision_vs_oracle": tp / (tp + fp) if tp + fp else None,
            "activation_recall_vs_oracle": tp / (tp + fn) if tp + fn else None,
            "M_vs_OFF_paired": {"M_only_correct": b, "OFF_only_correct": c, "mcnemar_exact_p": mcnemar_exact(b, c),
                                "note": "secondary: naturalistic replication of the P-D dependence contrast; not a gate"},
        },
        "terminal": route(gates),
    })
    return result


def route(gates: dict[str, Any]) -> str:
    if not gates["G0_VALIDITY"]["pass"]:
        return "DESIGN_VIOLATION_RUN_VOID"
    if not gates["G1_DOMINATES_ALWAYS_ON"]["pass"]:
        return "GATING_DOES_NOT_DOMINATE_ALWAYS_ON"
    if not gates["G2_DOMINATES_ALWAYS_OFF_AND_PARENT"]["pass_vs_OFF"]:
        return "GATING_DOES_NOT_DOMINATE_ALWAYS_OFF"
    if not gates["G2_DOMINATES_ALWAYS_OFF_AND_PARENT"]["pass_vs_PARENT"]:
        return "STRONGEST_PARENT_SUFFICIENT_UNDER_GATING"
    if not gates["G3_BEATS_SHUFFLE_NULL"]["pass"]:
        return NATURALISTIC_TERMINALS["G3_FAIL"]
    if not gates["G4_SIGN_CONSISTENCY"]["pass"]:
        return "ACTIVATION_ADVANTAGE_NOT_SIGN_CONSISTENT"
    if not gates["G3S_BEATS_WITHIN_STUDY_NULL"]["pass"]:
        return NATURALISTIC_TERMINALS["G3S_FAIL"]
    return NATURALISTIC_TERMINALS["PASS"]


# ---------------------------------------------------------------------------
# rollup
# ---------------------------------------------------------------------------

def fmt(v: Any) -> str:
    return f"{v:.4f}" if isinstance(v, float) else str(v)


def rollup(freeze: dict[str, Any], cell: dict[str, Any] | None, design_path: Path, corpus_freeze: dict[str, Any] | None) -> dict[str, Any]:
    if cell is None:
        binding = freeze.get("terminal_if_none") or "CANNOT_CHECK_RUN_INVALID"
    else:
        binding = cell["terminal"]
    return {
        "schema_version": "orion.v2.h-ext1n-rollup.v1",
        "hypothesis_id": "H-EXT-1N",
        "design_sha256": sha256_path(design_path),
        "corpus_freeze": {k: corpus_freeze.get(k) for k in ("n_sets", "n_dependent", "n_independent", "by_stratum", "by_split", "host", "public_tasks_sha256")} if corpus_freeze else None,
        "gate_freeze": {k: freeze.get(k) for k in ("selected_gate", "gate_sha256", "dev_n", "dev_task_ids_sha256", "design_sha256", "dev_acc_M", "dev_acc_OFF", "terminal_if_none")},
        "cell": cell,
        "binding_cell": "N1-EVAL",
        "binding_terminal": binding,
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_real_corpus_dependence_detection": False, "grants_manuscript_change": False},
    }


def rollup_markdown(roll: dict[str, Any]) -> str:
    gf = roll["gate_freeze"]
    lines = ["# H-EXT-1N Rollup V1 (naturalistic replication of H-EXT-1)", "",
             f"Design sha256 `{roll['design_sha256'][:16]}`; frozen gate **{gf['selected_gate']}** "
             f"(gate sha `{str(gf['gate_sha256'])[:16]}`, dev n={gf['dev_n']}, dev M {fmt(gf['dev_acc_M'])} / OFF {fmt(gf['dev_acc_OFF'])}).", ""]
    cf = roll.get("corpus_freeze")
    if cf:
        lines += [f"Corpus: {cf['n_sets']} evidence sets ({cf['n_dependent']} dependent / {cf['n_independent']} independent), "
                  f"strata {cf['by_stratum']}, splits {cf['by_split']}, host `{cf['host']}`.", ""]
    lines += [f"**Binding terminal (N1-EVAL): `{roll['binding_terminal']}`**", ""]
    cell = roll.get("cell")
    if not cell:
        lines += ["No evaluation cell was scored.", ""]
        return "\n".join(lines)
    lines += [f"Terminal: `{cell['terminal']}` — scored {cell.get('n_scored', 0)}/{cell['n_total']}, activations {cell.get('activations', 0)} ({fmt(cell.get('activation_rate', 0.0))})", ""]
    gates = cell.get("gates", {})
    if not gates:
        lines += [f"Missing arm responses on {cell['n_missing']} tasks; nothing inferred.", ""]
        return "\n".join(lines)
    g1, g2, g3, g3s, g4 = (gates[k] for k in ("G1_DOMINATES_ALWAYS_ON", "G2_DOMINATES_ALWAYS_OFF_AND_PARENT",
                                              "G3_BEATS_SHUFFLE_NULL", "G3S_BEATS_WITHIN_STUDY_NULL", "G4_SIGN_CONSISTENCY"))
    lines += ["| Gate | Pass | Detail |", "|---|---|---|",
              f"| G0 | {gates['G0_VALIDITY']['pass']} | {'; '.join(gates['G0_VALIDITY']['reasons']) or 'clean'} |",
              f"| G1 | {g1['pass']} | GATED {fmt(g1['acc_GATED'])} vs M {fmt(g1['acc_M'])}; calls {g1['calls_GATED']} vs {g1['calls_M']}; wall {fmt(g1['mean_wall_GATED'])} vs {fmt(g1['mean_wall_M'])} |",
              f"| G2 | {g2['pass']} | vs OFF {fmt(g2['acc_OFF'])} ({g2['pass_vs_OFF']}); vs PARENT {fmt(g2['acc_PARENT'])} ({g2['pass_vs_PARENT']}) |",
              f"| G3 | {g3['pass']} | advantage {fmt(g3['advantage'])} vs pooled-null q95 {fmt(g3['null_q95'])} (mean {fmt(g3['null_mean'])}, max {fmt(g3['null_max'])}, exceedance {fmt(g3['null_exceedance_fraction'])}, {g3['draws']} draws) |",
              f"| G3S | {g3s['pass']} | vs within-(topic x size) null q95 {fmt(g3s['null_q95'])} (mean {fmt(g3s['null_mean'])}, max {fmt(g3s['null_max'])}, exceedance {fmt(g3s['null_exceedance_fraction'])}) |",
              f"| G4 | {g4['pass']} | per size class below |", "",
              "| Size class | n | act | M | OFF | PARENT | GATED |", "|---|---|---|---|---|---|---|"]
    for s, v in g4["per_study"].items():
        lines.append(f"| {s} | {v['n']} | {v['activations']} | {fmt(v['acc_M'])} | {fmt(v['acc_OFF'])} | {fmt(v['acc_PARENT'])} | {fmt(v['acc_GATED'])} |")
    refs = cell.get("references_reporting_only", {})
    mo = refs.get("M_vs_OFF_paired", {})
    lines += ["", f"Reporting-only references: oracle-stratum ceiling {fmt(refs.get('ORACLE_STRATUM_ceiling_acc'))}; "
              f"activation precision vs oracle-active strata {fmt(refs.get('activation_precision_vs_oracle'))}, recall {fmt(refs.get('activation_recall_vs_oracle'))}; "
              f"M vs OFF paired: M-only {mo.get('M_only_correct')}, OFF-only {mo.get('OFF_only_correct')}, exact McNemar p {fmt(mo.get('mcnemar_exact_p'))}.", "",
              "| Oracle stratum (reporting only) | n | act | M | OFF | PARENT | GATED |", "|---|---|---|---|---|---|---|"]
    for s, v in sorted(refs.get("per_oracle_stratum", {}).items()):
        lines.append(f"| {s} | {v['n']} | {v['activations']} | {v['M']} | {v['OFF']} | {v['PARENT']} | {v['GATED']} |")
    lines += ["", "| Topic | n | act | M | OFF | GATED |", "|---|---|---|---|---|---|"]
    for t, v in refs.get("per_topic", {}).items():
        lines.append(f"| {t} | {v['n']} | {v['activations']} | {fmt(v['acc_M'])} | {fmt(v['acc_OFF'])} | {fmt(v['acc_GATED'])} |")
    lines += ["", "Authority: all grants false.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--study-dir", type=Path, required=True)
    e.add_argument("--out", type=Path, required=True)
    d = sub.add_parser("develop")
    d.add_argument("--instances", type=Path, required=True)
    d.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    d.add_argument("--out", type=Path, required=True)
    ev = sub.add_parser("evaluate")
    ev.add_argument("--instances", type=Path, required=True)
    ev.add_argument("--dev-instances", type=Path, required=True)
    ev.add_argument("--freeze", type=Path, required=True)
    ev.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    ev.add_argument("--corpus-freeze", type=Path, default=None)
    ev.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args(argv)
    if args.command == "extract":
        write_json(args.out, extract_instances(args.study_dir))
        return 0
    if args.command == "develop":
        freeze = develop(read_json(args.instances), args.design)
        write_json(args.out, freeze)
        print(json.dumps({"selected_gate": freeze["selected_gate"], "terminal_if_none": freeze["terminal_if_none"]}))
        return 0 if freeze["selected_gate"] else 4
    design = read_json(args.design)
    freeze = read_json(args.freeze)
    if freeze["design_sha256"] != sha256_path(args.design):
        raise DesignViolation("design file changed after gate freeze (no-rescue clause)")
    dev_ids = {r["task_id"] for r in read_json(args.dev_instances)["rows"]}
    corpus_freeze = read_json(args.corpus_freeze) if args.corpus_freeze else None
    cell = evaluate(read_json(args.instances), freeze, design, dev_ids,
                    sha256_path(args.corpus_freeze) if args.corpus_freeze else None)
    write_json(args.out_dir / "H_EXT1N_CELL_EVAL.json", cell)
    roll = rollup(freeze, cell, args.design, corpus_freeze)
    write_json(args.out_dir / "H_EXT1N_ROLLUP_V1.json", roll)
    (args.out_dir / "H_EXT1N_ROLLUP_V1.md").write_text(rollup_markdown(roll), encoding="utf-8")
    print(json.dumps({"binding_terminal": roll["binding_terminal"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
