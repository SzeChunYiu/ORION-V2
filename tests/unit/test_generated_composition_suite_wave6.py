from __future__ import annotations

import difflib
import json
import random
import re
from pathlib import Path

from scripts.run_orion_generated_composition_suite import (
    evaluate_one,
    generate,
    generate_spec,
    oracle,
    read_json,
)


PROTOCOL = {
    "suite_id": "E70-GC1-TEST",
    "status": "PROSPECTIVE_SECONDARY_ANTI_COPY_PROTOCOL_NO_RESULTS",
    "authority": {
        "grants_scientific_truth": False,
        "grants_active_solving_proof": False,
        "grants_field_status": False,
        "grants_submission_readiness": False,
    },
}


def test_oracle_enforces_authority_before_later_rules() -> None:
    spec = generate_spec(random.Random(7), 0)
    record = {
        "x": 100,
        "y": 100,
        "unit": spec["unit_primary"],
        "source": "UNAUTHORIZED",
        "counterexample": True,
    }
    assert oracle(record, spec) == spec["labels"]["unknown"]


def test_generation_keeps_private_spec_out_of_public_workspace(tmp_path: Path) -> None:
    workdir = tmp_path / "suite"
    generate(
        PROTOCOL,
        workdir,
        count=2,
        seed=20260828,
        arms=["SIMPLE_DIRECT", "F2_ORION_METABOLIC_FULL"],
        force=False,
    )
    frozen = read_json(workdir / "FROZEN_TASKS.json")
    assert frozen["task_count"] == 2
    assert frozen["private_gold_mounted_to_solver"] is False
    for task in frozen["tasks"]:
        workspace = Path(task["solver_workspace"])
        assert workspace.is_dir()
        assert (workspace / "solver.py").exists()
        assert len(list((workspace / "sources").glob("*.md"))) == 4
        assert not any(path.name.startswith("private") for path in workspace.rglob("*"))
        assert (workdir / "private" / f"{task['task_id']}.json").exists()


def _correct_solver(spec: dict) -> str:
    labels = spec["labels"]
    allowed = repr(set(spec["allowed_sources"]))
    return f'''"""Generated correct test implementation."""

def decide(record):
    if record.get("source") not in {allowed}:
        return {labels["unknown"]!r}
    unit = record.get("unit")
    if unit not in {{{spec["unit_primary"]!r}, {spec["unit_scaled"]!r}}}:
        return {labels["unknown"]!r}
    x = int(record["x"])
    if unit == {spec["unit_scaled"]!r}:
        x *= {spec["scale_factor"]}
    y = int(record["y"])
    score = ({spec["a"]} * x + {spec["b"]} * y + {spec["c"]}) % {spec["modulus"]}
    if bool(record.get("counterexample")):
        return {labels["review"]!r}
    if score >= {spec["high"]}:
        return {labels["accept"]!r}
    if score <= {spec["low"]}:
        return {labels["reject"]!r}
    return {labels["review"]!r}
'''


def _rooted_patch(before: str, after: str) -> str:
    body = "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="a/solver.py",
            tofile="b/solver.py",
        )
    )
    return "diff --git a/solver.py b/solver.py\n" + body


def test_hidden_evaluator_accepts_correct_composed_repair(tmp_path: Path) -> None:
    workdir = tmp_path / "suite"
    arm = "SIMPLE_DIRECT"
    generate(PROTOCOL, workdir, count=1, seed=9, arms=[arm], force=False)
    task_id = "gc1-001"
    private = read_json(workdir / "private" / f"{task_id}.json")
    solver_path = workdir / "public" / task_id / "solver.py"
    before = solver_path.read_text(encoding="utf-8")
    after = _correct_solver(private["spec"])
    patch = _rooted_patch(before, after)
    response = {
        "schema_version": "orion.v2.agent-response.v1",
        "task_id": task_id,
        "arm_id": arm,
        "status": "COMPLETED_PROPOSAL_ONLY",
        "proposed_patch_or_artifact": {"type": "unified_diff", "content": patch},
        "resource_receipt": {"total_tokens_reported_by_cli": 100, "wall_time_seconds": 1.0},
    }
    response_path = workdir / "responses" / arm / f"{task_id}.json"
    response_path.parent.mkdir(parents=True)
    response_path.write_text(json.dumps(response), encoding="utf-8")

    result = evaluate_one(workdir, arm, task_id)
    assert result["raw_patch_apply_success"] is True
    assert result["raw_hidden_oracle_success"] is True
    assert result["raw_hidden_accuracy"] == 1.0
    assert result["gold_or_private_spec_visible_to_solver"] is False


def test_syntax_only_sensitivity_does_not_replace_raw_failure(tmp_path: Path) -> None:
    workdir = tmp_path / "suite"
    arm = "F2_ORION_METABOLIC_FULL"
    generate(PROTOCOL, workdir, count=1, seed=11, arms=[arm], force=False)
    task_id = "gc1-001"
    private = read_json(workdir / "private" / f"{task_id}.json")
    solver_path = workdir / "public" / task_id / "solver.py"
    before = solver_path.read_text(encoding="utf-8")
    after = _correct_solver(private["spec"])
    patch = _rooted_patch(before, after)
    # Damage only the hunk count metadata.  The edit body and paths stay fixed,
    # so the arm-blind canonicalizer may recompute the counts without guessing
    # or changing semantics, while raw git-apply must fail.
    patch, replacements = re.subn(
        r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@",
        lambda match: (
            f"@@ -{match.group(1)},{int(match.group(2)) + 7} "
            f"+{match.group(3)},{int(match.group(4)) + 11} @@"
        ),
        patch,
        count=1,
    )
    assert replacements == 1
    response_path = workdir / "responses" / arm / f"{task_id}.json"
    response_path.parent.mkdir(parents=True)
    response_path.write_text(
        json.dumps({
            "schema_version": "orion.v2.agent-response.v1",
            "task_id": task_id,
            "arm_id": arm,
            "status": "COMPLETED_PROPOSAL_ONLY",
            "proposed_patch_or_artifact": {"type": "unified_diff", "content": patch},
            "resource_receipt": {},
        }),
        encoding="utf-8",
    )
    result = evaluate_one(workdir, arm, task_id)
    assert result["raw_patch_apply_success"] is False
    assert result["raw_hidden_oracle_success"] is False
    assert result["syntax_audit_status"] == "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION"
    assert result["syntax_normalized_hidden_oracle_success"] is True
