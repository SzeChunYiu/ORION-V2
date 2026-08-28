#!/usr/bin/env python3
"""Generate, dispatch, evaluate and analyze the E70-GC1 composition suite.

The suite is fully self-contained (Python standard library only) and is secondary
anti-copy/composition evidence. It never replaces the naturalistic E30/E40/E50
studies. Private generation parameters and hidden cases stay outside solver
workspaces. Raw emitted patches are the primary end-to-end outcome; the shared
syntax-only canonicalizer is evaluated only as a secondary sensitivity analysis.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable

from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "research/experiments/ORION_GENERATED_COMPOSITION_COUNTERFACTUAL_SUITE_V1.json"
DEFAULT_WORKDIR = ROOT / ".orion-generated-composition-suite"
DIFF_PATH_RE = re.compile(r"^diff --git a/(?P<a>[^\n]+) b/(?P<b>[^\n]+)$", re.MULTILINE)


class SuiteError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SuiteError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SuiteError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def random_token(rng: random.Random, prefix: str, length: int = 6) -> str:
    alphabet = string.ascii_uppercase
    return prefix + "_" + "".join(rng.choice(alphabet) for _ in range(length))


def oracle(record: dict[str, Any], spec: dict[str, Any]) -> str:
    labels = spec["labels"]
    if record.get("source") not in spec["allowed_sources"]:
        return labels["unknown"]
    unit = record.get("unit")
    if unit not in {spec["unit_primary"], spec["unit_scaled"]}:
        return labels["unknown"]

    x = int(record["x"])
    if unit == spec["unit_scaled"]:
        x *= int(spec["scale_factor"])
    y = int(record["y"])
    score = (
        int(spec["a"]) * x
        + int(spec["b"]) * y
        + int(spec["c"])
    ) % int(spec["modulus"])

    if bool(record.get("counterexample")):
        return labels["review"]
    if score >= int(spec["high"]):
        return labels["accept"]
    if score <= int(spec["low"]):
        return labels["reject"]
    return labels["review"]


def random_record(rng: random.Random, spec: dict[str, Any]) -> dict[str, Any]:
    sources = list(spec["all_sources"]) + [random_token(rng, "OUTSIDE", 4)]
    units = [spec["unit_primary"], spec["unit_scaled"], random_token(rng, "BADUNIT", 4)]
    return {
        "x": rng.randint(-80, 80),
        "y": rng.randint(-40, 40),
        "unit": rng.choice(units),
        "source": rng.choice(sources),
        "counterexample": bool(rng.getrandbits(1)) if rng.random() < 0.25 else False,
    }


def generate_spec(rng: random.Random, index: int) -> dict[str, Any]:
    modulus = rng.choice([17, 19, 23, 29, 31])
    low = rng.randint(3, modulus // 3)
    high = rng.randint(max(low + 3, (2 * modulus) // 3), modulus - 2)
    sources = [random_token(rng, f"SRC{index}", 5) for _ in range(4)]
    allowed = sorted(rng.sample(sources, 2))
    labels = {
        "accept": random_token(rng, "GO", 5),
        "review": random_token(rng, "HOLD", 5),
        "reject": random_token(rng, "STOP", 5),
        "unknown": random_token(rng, "UNK", 5),
    }
    return {
        "task_index": index,
        "a": rng.choice([2, 3, 4, 5, 7]),
        "b": rng.choice([2, 3, 5, 6, 7]),
        "c": rng.randint(1, modulus - 1),
        "modulus": modulus,
        "low": low,
        "high": high,
        "unit_primary": random_token(rng, "UNITA", 5),
        "unit_scaled": random_token(rng, "UNITB", 5),
        "scale_factor": rng.randint(2, 7),
        "all_sources": sources,
        "allowed_sources": allowed,
        "labels": labels,
    }


def find_public_examples(rng: random.Random, spec: dict[str, Any], count: int = 4) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    observed_labels: set[str] = set()
    for _ in range(4000):
        record = random_record(rng, spec)
        expected = oracle(record, spec)
        if expected in observed_labels and len(examples) < 3:
            continue
        examples.append({"record": record, "expected": expected})
        observed_labels.add(expected)
        if len(examples) >= count:
            break
    if len(examples) < count:
        raise SuiteError("failed to generate public examples")
    return examples


def hidden_cases(rng: random.Random, spec: dict[str, Any], count: int = 96) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    # Force authority, unit and counterexample branches before random coverage.
    valid_source = spec["allowed_sources"][0]
    cases.append({"x": 1, "y": 2, "unit": spec["unit_primary"], "source": "UNREGISTERED_PRIVATE_SOURCE", "counterexample": False})
    cases.append({"x": 2, "y": 1, "unit": "UNREGISTERED_PRIVATE_UNIT", "source": valid_source, "counterexample": False})
    cases.append({"x": 5, "y": 3, "unit": spec["unit_primary"], "source": valid_source, "counterexample": True})

    while len(cases) < count:
        cases.append(random_record(rng, spec))
    return cases


def render_public_workspace(path: Path, spec: dict[str, Any], examples: list[dict[str, Any]]) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "sources").mkdir()
    labels = spec["labels"]
    (path / "solver.py").write_text(
        "\"\"\"Implement decide(record) from the source fragments.\"\"\"\n\n"
        "def decide(record):\n"
        f"    return {labels['accept']!r}  # intentionally incomplete baseline\n",
        encoding="utf-8",
    )
    (path / "sources/01_measurement.md").write_text(
        "# Measurement rule\n\n"
        f"The primary unit token is `{spec['unit_primary']}`. The scaled unit token is "
        f"`{spec['unit_scaled']}`; when it is used, multiply x by {spec['scale_factor']} before scoring. "
        "Any other unit is outside the usable measurement contract.\n\n"
        f"For a usable measurement, compute `score = ({spec['a']} * x + {spec['b']} * y + {spec['c']}) % {spec['modulus']}`.\n",
        encoding="utf-8",
    )
    (path / "sources/02_authority.md").write_text(
        "# Source authority rule\n\n"
        "A record can support a scientific decision only when its `source` token is in this exact authorized set:\n\n"
        + "\n".join(f"- `{source}`" for source in spec["allowed_sources"])
        + "\n\nOther source tokens do not authorize a substantive decision.\n",
        encoding="utf-8",
    )
    (path / "sources/03_decision.md").write_text(
        "# Decision codebook and thresholds\n\n"
        f"Unknown/unusable evidence returns `{labels['unknown']}`.\n\n"
        f"A registered counterexample returns `{labels['review']}`.\n\n"
        f"Otherwise score >= {spec['high']} returns `{labels['accept']}`; score <= {spec['low']} returns `{labels['reject']}`; intermediate scores return `{labels['review']}`.\n",
        encoding="utf-8",
    )
    (path / "sources/04_precedence.md").write_text(
        "# Precedence\n\n"
        "Apply the rules in this order: (1) source authority, (2) recognized measurement unit and normalization, "
        "(3) counterexample override, (4) score thresholds. An unauthorized source or unknown unit returns the unknown code before any later rule.\n",
        encoding="utf-8",
    )
    (path / "README.md").write_text(
        "# Fresh generated source-composition repair task\n\n"
        "Implement `solver.decide(record)` using all relevant source fragments. The semantic constants and output tokens were generated after protocol freeze. "
        "The hidden evaluator contains additional records and is not present in this workspace. Do not use network retrieval.\n\n"
        "## Public examples\n\n"
        + "\n".join(
            f"- `{json.dumps(item['record'], sort_keys=True)}` -> `{item['expected']}`"
            for item in examples
        )
        + "\n",
        encoding="utf-8",
    )


def generate(protocol: dict[str, Any], workdir: Path, *, count: int, seed: int, arms: list[str], force: bool) -> None:
    if workdir.exists():
        if not force:
            raise SuiteError(f"workdir exists; pass --force to replace it: {workdir}")
        shutil.rmtree(workdir)
    public_root = workdir / "public"
    private_root = workdir / "private"
    requests_root = workdir / "requests"
    rng = random.Random(seed)
    task_rows: list[dict[str, Any]] = []

    for index in range(count):
        task_id = f"gc1-{index + 1:03d}"
        task_rng = random.Random(rng.getrandbits(64))
        spec = generate_spec(task_rng, index)
        examples = find_public_examples(task_rng, spec)
        cases = hidden_cases(task_rng, spec)
        expected = [oracle(record, spec) for record in cases]
        public_path = public_root / task_id
        render_public_workspace(public_path, spec, examples)
        private_payload = {
            "schema_version": "orion.v2.generated-composition-private.v1",
            "task_id": task_id,
            "spec": spec,
            "records": cases,
            "expected": expected,
        }
        write_json(private_root / f"{task_id}.json", private_payload)
        manifest_rows = []
        for file in sorted(public_path.rglob("*")):
            if file.is_file():
                relative = file.relative_to(public_path).as_posix()
                manifest_rows.append({"path": relative, "sha256": sha256_bytes(file.read_bytes()), "bytes": file.stat().st_size})

        baseline_example = next(
            (item for item in examples if item["expected"] != spec["labels"]["accept"]),
            examples[0],
        )
        task_row = {
            "task_id": task_id,
            "solver_workspace": str(public_path.resolve()),
            "adapter": "generated_composition_counterfactual",
            "benchmark_id": "generated_composition_counterfactual",
            "public_manifest": manifest_rows,
            "baseline_observation": {
                "current_implementation_returns": spec["labels"]["accept"],
                "public_record": baseline_example["record"],
                "expected_from_public_sources": baseline_example["expected"],
                "status": "KNOWN_INCORRECT_IMPLEMENTATION",
            },
        }
        task_rows.append(task_row)
        for arm in arms:
            request = {
                "schema_version": "orion.v2.agent-request.v1",
                "task_id": task_id,
                "arm_id": arm,
                "task": task_row,
                "resource_contract": protocol.get("resource_contract", {
                    "default_cpu_cores": 2,
                    "default_memory_gb": 4,
                }),
                "scientific_truth_authorized": False,
                "field_status_authorized": False,
                "publication_readiness_authorized": False,
            }
            write_json(requests_root / arm / f"{task_id}.json", request)

    freeze = {
        "schema_version": "orion.v2.generated-composition-freeze.v1",
        "suite_id": protocol["suite_id"],
        "protocol_sha256": sha256_bytes(DEFAULT_PROTOCOL.read_bytes()) if DEFAULT_PROTOCOL.exists() else None,
        "seed": seed,
        "task_count": count,
        "arms": arms,
        "tasks": task_rows,
        "private_gold_mounted_to_solver": False,
        "authority": protocol.get("authority", {}),
    }
    write_json(workdir / "FROZEN_TASKS.json", freeze)


def model_command() -> list[str]:
    override = os.environ.get("ORION_GC1_ARM_COMMAND", "").strip()
    if override:
        import shlex
        return shlex.split(override)
    return [sys.executable, str(ROOT / "scripts/orion_codex_arms.py")]


def dispatch(workdir: Path, *, arms: list[str], max_concurrency: int, overwrite: bool) -> dict[str, Any]:
    command_prefix = model_command()
    jobs: list[tuple[str, str, Path, Path]] = []
    for arm in arms:
        for request_path in sorted((workdir / "requests" / arm).glob("*.json")):
            response_path = workdir / "responses" / arm / request_path.name
            if response_path.exists() and not overwrite:
                continue
            jobs.append((arm, request_path.stem, request_path, response_path))

    def run_one(job: tuple[str, str, Path, Path]) -> dict[str, Any]:
        arm, task_id, request_path, response_path = job
        response_path.parent.mkdir(parents=True, exist_ok=True)
        start = time.time()
        completed = subprocess.run(
            command_prefix + ["--request", str(request_path), "--response", str(response_path)],
            cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=int(os.environ.get("ORION_GC1_TIMEOUT", "2700")), check=False,
        )
        return {
            "arm_id": arm,
            "task_id": task_id,
            "returncode": completed.returncode,
            "wall_time_seconds": time.time() - start,
            "response_exists": response_path.exists(),
            "stdout_tail": completed.stdout[-2000:],
        }

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
        futures = [pool.submit(run_one, job) for job in jobs]
        for future in as_completed(futures):
            results.append(future.result())
    summary = {"schema_version": "orion.v2.gc1-dispatch.v1", "jobs": sorted(results, key=lambda x: (x["arm_id"], x["task_id"]))}
    write_json(workdir / "DISPATCH_RECEIPT.json", summary)
    return summary


def extract_patch(response: dict[str, Any]) -> str | None:
    artifact = response.get("proposed_patch_or_artifact")
    if isinstance(artifact, dict) and artifact.get("type") == "unified_diff" and isinstance(artifact.get("content"), str):
        return artifact["content"]
    if isinstance(artifact, str):
        return artifact
    return None


def patch_paths(patch: str) -> tuple[str, ...]:
    paths: list[str] = []
    for match in DIFF_PATH_RE.finditer(patch):
        old = match.group("a")
        new = match.group("b")
        if old != new:
            raise SuiteError("rename patch is outside GC1 scope")
        paths.append(old)
    return tuple(paths)


def apply_patch(workspace: Path, patch: str) -> tuple[bool, str]:
    try:
        paths = patch_paths(patch)
    except SuiteError as exc:
        return False, str(exc)
    if not paths or any(path != "solver.py" for path in paths):
        return False, f"patch paths must be exactly solver.py; observed={paths}"
    check = subprocess.run(
        ["git", "apply", "--check", "--whitespace=nowarn", "-"], cwd=str(workspace), input=patch,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check.returncode != 0:
        return False, check.stderr[-2000:]
    applied = subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"], cwd=str(workspace), input=patch,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return applied.returncode == 0, applied.stderr[-2000:]


RUNNER_CODE = r'''
import contextlib, importlib.util, io, json, sys
payload = json.load(sys.stdin)
module_path = sys.argv[1]
spec = importlib.util.spec_from_file_location("gc1_solver", module_path)
module = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    spec.loader.exec_module(module)
    outputs = [module.decide(record) for record in payload["records"]]
print(json.dumps(outputs))
'''


def score_workspace(workspace: Path, records: list[dict[str, Any]], expected: list[str]) -> dict[str, Any]:
    environment = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
    }
    completed = subprocess.run(
        [sys.executable, "-c", RUNNER_CODE, str(workspace / "solver.py")],
        input=json.dumps({"records": records}), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=20, check=False, cwd=str(workspace), env=environment,
    )
    if completed.returncode != 0:
        return {"runtime_success": False, "hidden_accuracy": 0.0, "stderr_tail": completed.stderr[-2000:]}
    try:
        observed = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"runtime_success": False, "hidden_accuracy": 0.0, "stderr_tail": "non-JSON solver output"}
    if not isinstance(observed, list) or len(observed) != len(expected):
        return {"runtime_success": False, "hidden_accuracy": 0.0, "stderr_tail": "output length mismatch"}
    correct = sum(str(got) == want for got, want in zip(observed, expected, strict=True))
    accuracy = correct / len(expected) if expected else 0.0
    return {"runtime_success": True, "hidden_accuracy": accuracy, "hidden_oracle_success": correct == len(expected), "correct": correct, "total": len(expected), "stderr_tail": ""}


def evaluate_one(workdir: Path, arm: str, task_id: str) -> dict[str, Any]:
    response_path = workdir / "responses" / arm / f"{task_id}.json"
    private = read_json(workdir / "private" / f"{task_id}.json")
    public = workdir / "public" / task_id
    if not response_path.exists():
        return {"task_id": task_id, "arm_id": arm, "status": "CANNOT_CHECK_MISSING_RESPONSE", "raw_hidden_oracle_success": False}
    response = read_json(response_path)
    patch = extract_patch(response)
    if patch is None:
        return {"task_id": task_id, "arm_id": arm, "status": "NO_EXECUTABLE_PATCH", "raw_hidden_oracle_success": False}

    raw_dir = workdir / "evaluation" / "raw" / arm / task_id
    if raw_dir.exists():
        shutil.rmtree(raw_dir)
    shutil.copytree(public, raw_dir)
    raw_apply, raw_error = apply_patch(raw_dir, patch)
    raw_score = {"runtime_success": False, "hidden_accuracy": 0.0, "hidden_oracle_success": False}
    if raw_apply:
        raw_score = score_workspace(raw_dir, private["records"], private["expected"])

    audit = audit_and_canonicalize_unified_diff(patch)
    normalized_apply = False
    normalized_score = {"runtime_success": False, "hidden_accuracy": 0.0, "hidden_oracle_success": False}
    normalized_error = "NOT_APPLICABLE"
    if audit.valid_or_canonicalizable and audit.canonical_diff is not None:
        normalized_dir = workdir / "evaluation" / "syntax_normalized" / arm / task_id
        if normalized_dir.exists():
            shutil.rmtree(normalized_dir)
        shutil.copytree(public, normalized_dir)
        normalized_apply, normalized_error = apply_patch(normalized_dir, audit.canonical_diff)
        if normalized_apply:
            normalized_score = score_workspace(normalized_dir, private["records"], private["expected"])

    resource = response.get("resource_receipt") if isinstance(response.get("resource_receipt"), dict) else {}
    result = {
        "schema_version": "orion.v2.gc1-evaluation.v1",
        "task_id": task_id,
        "arm_id": arm,
        "agent_status": response.get("status"),
        "raw_patch_sha256": sha256_text(patch),
        "raw_patch_apply_success": raw_apply,
        "raw_patch_apply_error": raw_error,
        "raw_hidden_accuracy": raw_score.get("hidden_accuracy", 0.0),
        "raw_hidden_oracle_success": bool(raw_apply and raw_score.get("hidden_oracle_success")),
        "syntax_audit_status": (
            "VALID_UNCHANGED" if audit.valid_or_canonicalizable and not audit.changed
            else "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION" if audit.valid_or_canonicalizable
            else "INVALID_NOT_CANONICALIZABLE"
        ),
        "syntax_audit_reasons": list(audit.reasons),
        "syntax_normalized_patch_apply_success": normalized_apply,
        "syntax_normalized_patch_apply_error": normalized_error,
        "syntax_normalized_hidden_accuracy": normalized_score.get("hidden_accuracy", 0.0),
        "syntax_normalized_hidden_oracle_success": bool(normalized_apply and normalized_score.get("hidden_oracle_success")),
        "model_tokens": resource.get("total_tokens_reported_by_cli"),
        "model_wall_time_seconds": resource.get("wall_time_seconds"),
        "patch_size_bytes": len(patch.encode("utf-8")),
        "gold_or_private_spec_visible_to_solver": False,
        "scientific_truth_authorized": False,
        "publication_readiness_authorized": False,
    }
    return result


def evaluate(workdir: Path, *, arms: list[str]) -> list[dict[str, Any]]:
    frozen = read_json(workdir / "FROZEN_TASKS.json")
    tasks = [str(item["task_id"]) for item in frozen["tasks"]]
    results: list[dict[str, Any]] = []
    for arm in arms:
        for task_id in tasks:
            result = evaluate_one(workdir, arm, task_id)
            write_json(workdir / "evaluations" / arm / f"{task_id}.json", result)
            results.append(result)
    return results


def binomial_two_sided(left_only: int, right_only: int) -> float | None:
    n = left_only + right_only
    if n == 0:
        return None
    tail = min(left_only, right_only)
    probability = sum(math.comb(n, k) for k in range(tail + 1)) / (2 ** n)
    return min(1.0, 2 * probability)


def paired_bootstrap(values: list[float], *, seed: int, reps: int = 10000) -> dict[str, Any]:
    if not values:
        return {"estimate": None, "ci95": [None, None], "pair_count": 0}
    estimate = sum(values) / len(values)
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(reps):
        sampled = [values[rng.randrange(len(values))] for _ in values]
        draws.append(sum(sampled) / len(sampled))
    draws.sort()
    lo = draws[int(0.025 * (len(draws) - 1))]
    hi = draws[int(0.975 * (len(draws) - 1))]
    return {"estimate": estimate, "ci95": [lo, hi], "pair_count": len(values), "bootstrap_repetitions": reps, "seed": seed}


def analyze(workdir: Path, *, arms: list[str], seed: int) -> dict[str, Any]:
    frozen = read_json(workdir / "FROZEN_TASKS.json")
    tasks = [str(item["task_id"]) for item in frozen["tasks"]]
    by_arm: dict[str, dict[str, dict[str, Any]]] = {}
    summaries: dict[str, Any] = {}
    for arm in arms:
        rows: dict[str, dict[str, Any]] = {}
        for task_id in tasks:
            path = workdir / "evaluations" / arm / f"{task_id}.json"
            if path.exists():
                rows[task_id] = read_json(path)
        by_arm[arm] = rows
        count = len(rows)
        raw_success = sum(bool(row.get("raw_hidden_oracle_success")) for row in rows.values())
        normalized_success = sum(bool(row.get("syntax_normalized_hidden_oracle_success")) for row in rows.values())
        summaries[arm] = {
            "task_count": count,
            "raw_success_count": raw_success,
            "raw_success_rate": raw_success / count if count else None,
            "syntax_normalized_success_count": normalized_success,
            "syntax_normalized_success_rate": normalized_success / count if count else None,
            "raw_patch_apply_failures": sum(not bool(row.get("raw_patch_apply_success")) for row in rows.values()),
            "syntax_canonicalization_changed_count": sum(row.get("syntax_audit_status") == "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION" for row in rows.values()),
            "mean_raw_hidden_accuracy": (sum(float(row.get("raw_hidden_accuracy", 0.0)) for row in rows.values()) / count if count else None),
            "model_tokens_total": sum(int(row["model_tokens"]) for row in rows.values() if isinstance(row.get("model_tokens"), int)),
        }

    f2 = "F2_ORION_METABOLIC_FULL"
    comparisons: list[dict[str, Any]] = []
    if f2 in by_arm:
        for control in ("F0_PARENT_FEDERATION", "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"):
            if control not in by_arm:
                continue
            common = sorted(set(by_arm[f2]) & set(by_arm[control]))
            diffs: list[float] = []
            left_only = 0
            right_only = 0
            for task_id in common:
                left = bool(by_arm[f2][task_id].get("raw_hidden_oracle_success"))
                right = bool(by_arm[control][task_id].get("raw_hidden_oracle_success"))
                diffs.append(float(left) - float(right))
                left_only += int(left and not right)
                right_only += int(right and not left)
            comparisons.append({
                "left_arm": f2,
                "right_arm": control,
                "raw_success_risk_difference": paired_bootstrap(diffs, seed=seed),
                "left_only": left_only,
                "right_only": right_only,
                "exact_discordant_p": binomial_two_sided(left_only, right_only),
            })

    result = {
        "schema_version": "orion.v2.gc1-analysis.v1",
        "suite_id": frozen["suite_id"],
        "status": "SECONDARY_ANTI_COPY_COMPOSITION_EVIDENCE_ONLY",
        "arm_summaries": summaries,
        "primary_comparisons": comparisons,
        "authority": {
            "grants_active_solving_proof": False,
            "grants_field_status": False,
            "grants_submission_readiness": False,
        },
    }
    write_json(workdir / "aggregate" / "analysis.json", result)
    lines = [
        "# E70-GC1 Execution Summary",
        "",
        "Secondary generated counterfactual/source-composition evidence only.",
        "",
        "| Arm | Raw hidden success | Syntax-normalized sensitivity | Raw patch-apply failures |",
        "| --- | ---: | ---: | ---: |",
    ]
    for arm in arms:
        row = summaries.get(arm, {})
        lines.append(
            f"| {arm} | {row.get('raw_success_count', 0)}/{row.get('task_count', 0)} | "
            f"{row.get('syntax_normalized_success_count', 0)}/{row.get('task_count', 0)} | "
            f"{row.get('raw_patch_apply_failures', 0)} |"
        )
    lines += ["", "This suite cannot replace E30/E40/E50 and does not prove absence of training-data influence."]
    (workdir / "EXECUTION_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def parse_arms(protocol: dict[str, Any], value: str | None) -> list[str]:
    if not value:
        return list(protocol["core_pilot_arms"])
    allowed = set(protocol["arms"])
    arms = [item.strip() for item in value.split(",") if item.strip()]
    unknown = [item for item in arms if item not in allowed]
    if unknown:
        raise SuiteError(f"unknown arms: {unknown}")
    return arms


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("generate", "dispatch", "evaluate", "analyze", "all"))
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    parser.add_argument("--arms")
    parser.add_argument("--task-count", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--max-concurrency", type=int, default=2)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--overwrite-responses", action="store_true")
    args = parser.parse_args(argv)

    protocol = read_json(args.protocol)
    if protocol.get("status") != "PROSPECTIVE_SECONDARY_ANTI_COPY_PROTOCOL_NO_RESULTS":
        raise SuiteError("protocol is not in prospective no-results state")
    arms = parse_arms(protocol, args.arms)
    count = args.task_count or int(protocol["task_count"])
    seed = args.seed if args.seed is not None else int(protocol["seed"])
    if count <= 0 or args.max_concurrency <= 0:
        raise SuiteError("task-count and max-concurrency must be positive")

    if args.action in {"generate", "all"}:
        generate(protocol, args.workdir, count=count, seed=seed, arms=arms, force=args.force)
    if args.action in {"dispatch", "all"}:
        dispatch(args.workdir, arms=arms, max_concurrency=args.max_concurrency, overwrite=args.overwrite_responses)
    if args.action in {"evaluate", "all"}:
        evaluate(args.workdir, arms=arms)
    if args.action in {"analyze", "all"}:
        analyze(args.workdir, arms=arms, seed=seed)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (SuiteError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
