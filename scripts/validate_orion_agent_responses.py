#!/usr/bin/env python3
"""Validate ORION real-problem agent responses before native evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_AUTHORITY = {"NONE", "PROPOSAL_ONLY", "EXECUTION_TEST_ONLY"}
UNRESOLVED_PREFIXES = ("CANNOT_CHECK", "EXECUTION_FAILED")
FULL_METABOLIC_STAGES = (
    "INGEST",
    "DECOMPOSE",
    "SORT",
    "NATIVE_RECONSTRUCT",
    "REDUCE",
    "ABSORB",
    "RECOMBINE",
    "CHALLENGE",
    "ASSIMILATE_OR_RECYCLE",
)


class ValidationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _non_blank_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def validate_response(
    response: dict[str, Any],
    *,
    expected_task_id: str,
    expected_arm_id: str,
    required_fields: tuple[str, ...],
) -> list[str]:
    errors: list[str] = []
    if response.get("schema_version") != "orion.v2.agent-response.v1":
        errors.append("unexpected schema_version")
    if response.get("task_id") != expected_task_id:
        errors.append("task_id does not match request path")
    if response.get("arm_id") != expected_arm_id:
        errors.append("arm_id does not match request path")
    for field in required_fields:
        if field not in response:
            errors.append(f"missing required field: {field}")

    status = str(response.get("status", ""))
    unresolved = status.upper().startswith(UNRESOLVED_PREFIXES)
    if not status.strip():
        errors.append("status must be non-blank")

    requested_authority = response.get("requested_authority")
    if requested_authority not in ALLOWED_AUTHORITY:
        errors.append("requested_authority is outside the experiment ceiling")

    for field in ("source_ids_used", "assumptions", "discriminator_or_tests"):
        if field in response and not _non_blank_list(response[field]):
            if not (unresolved and response[field] == []):
                errors.append(f"{field} must be a list of non-blank strings")

    if not unresolved:
        artifact = response.get("proposed_patch_or_artifact")
        if artifact is None:
            errors.append("checkable response requires proposed_patch_or_artifact")
        elif isinstance(artifact, dict):
            artifact_type = artifact.get("type")
            if artifact_type not in {"unified_diff", "path", "native_result_request"}:
                errors.append("unsupported proposed artifact type")
            if artifact_type == "unified_diff" and not isinstance(artifact.get("content"), str):
                errors.append("unified_diff requires string content")
        elif not isinstance(artifact, str):
            errors.append("proposed artifact must be a string, object or null")

        falsifier = response.get("falsifier")
        if not isinstance(falsifier, str) or not falsifier.strip():
            errors.append("checkable response requires a falsifier")

    uncertainty = response.get("uncertainty")
    if not isinstance(uncertainty, (str, dict, list, int, float)):
        errors.append("uncertainty must be explicitly representable")

    resource = response.get("resource_receipt")
    if resource is not None and not isinstance(resource, dict):
        errors.append("resource_receipt must be an object when supplied")

    if expected_arm_id == "F2_ORION_METABOLIC_FULL" and not unresolved:
        stages = response.get("metabolic_stages")
        if not isinstance(stages, dict):
            errors.append("full F2 response requires metabolic_stages object")
        else:
            missing = [stage for stage in FULL_METABOLIC_STAGES if stage not in stages]
            if missing:
                errors.append("missing metabolic stages: " + ", ".join(missing))
            for stage, value in stages.items():
                if stage in FULL_METABOLIC_STAGES and value in (None, "", [], {}):
                    errors.append(f"metabolic stage {stage} is empty; use explicit CANNOT_CHECK")

    receipt = response.get("patch_emission_receipt")
    if receipt is not None:
        # Additive, optional field: arms that canonicalize at emission carry an audit
        # trail so the raw header-exact interface-fidelity endpoint stays reportable.
        if not isinstance(receipt, dict):
            errors.append("patch_emission_receipt must be an object when supplied")
        else:
            if receipt.get("schema_version") != "orion.v2.patch-emission.v1":
                errors.append("unexpected patch_emission_receipt schema_version")
            for key in ("emission_status", "raw_sha256", "emitted_sha256", "raw_was_header_exact"):
                if key not in receipt:
                    errors.append(f"patch_emission_receipt missing required key: {key}")
            authority = receipt.get("authority")
            if not isinstance(authority, dict) or authority.get(
                "gold_or_fixed_patch_access"
            ) != "FORBIDDEN_NOT_USED":
                errors.append("patch_emission_receipt must record gold-blind emission")
            if any(authority.get(key) is True for key in (
                "may_change_semantic_edit", "may_guess_paths", "may_relocate_hunks",
                "may_rescore_a_frozen_campaign",
            ) if isinstance(authority, dict)):
                errors.append("patch_emission_receipt claims authority beyond serialization")

    if response.get("scientific_truth_authorized") is True:
        errors.append("agent response cannot authorize scientific truth")
    if response.get("field_status_authorized") is True:
        errors.append("agent response cannot authorize field status")
    if response.get("publication_readiness_authorized") is True:
        errors.append("agent response cannot authorize publication readiness")
    return errors


def validate_directory(
    workdir: Path,
    *,
    manifest_path: Path,
    arms: set[str] | None,
    tasks: set[str] | None,
) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    required_fields = tuple(
        manifest.get("agent_protocol", {}).get("required_response_fields", ())
    )
    receipts: list[dict[str, Any]] = []
    invalid_count = 0
    for path in sorted((workdir / "responses").glob("*/*.json")):
        arm_id = path.parent.name
        task_id = path.stem
        if arms and arm_id not in arms:
            continue
        if tasks and task_id not in tasks:
            continue
        response = read_json(path)
        errors = validate_response(
            response,
            expected_task_id=task_id,
            expected_arm_id=arm_id,
            required_fields=required_fields,
        )
        valid = not errors
        invalid_count += int(not valid)
        receipt = {
            "schema_version": "orion.v2.agent-response-validation.v1",
            "task_id": task_id,
            "arm_id": arm_id,
            "response_path": str(path),
            "valid": valid,
            "errors": errors,
            "scientific_truth_authorized": False,
            "field_status_authorized": False,
            "publication_readiness_authorized": False,
        }
        receipts.append(receipt)
        write_json(workdir / "response_validation" / arm_id / f"{task_id}.json", receipt)
    summary = {
        "schema_version": "orion.v2.agent-response-validation-summary.v1",
        "validated_count": len(receipts),
        "invalid_count": invalid_count,
        "all_valid": invalid_count == 0,
        "receipts": receipts,
        "authority": {
            "scientific_truth": False,
            "field_status": False,
            "publication_readiness": False,
        },
    }
    write_json(workdir / "aggregate" / "response_validation.json", summary)
    return summary


def parse_ids(value: str) -> set[str] | None:
    result = {item.strip() for item in value.split(",") if item.strip()}
    return result or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/experiments/ORION_REAL_PROBLEM_SUITE_V1.json"),
    )
    parser.add_argument("--arms", default="")
    parser.add_argument("--tasks", default="")
    args = parser.parse_args(argv)
    try:
        summary = validate_directory(
            args.workdir,
            manifest_path=args.manifest,
            arms=parse_ids(args.arms),
            tasks=parse_ids(args.tasks),
        )
    except (ValidationError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["all_valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
