from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


REQUIRED_CONTROL_PLANE = frozenset(
    {
        "freeze_contract",
        "freeze_manifest",
        "component_graph",
        "component_binding",
        "issue_disposition_ledger",
        "theorem_census",
        "p1_p15_claim_ledger",
        "failure_ledger",
        "research_harness_tree",
    }
)


@dataclass(frozen=True, slots=True)
class HandoffValidation:
    valid: bool
    terminal: str
    errors: tuple[str, ...]


def validate_handoff_receipt(receipt: Mapping[str, Any]) -> HandoffValidation:
    errors: list[str] = []
    if receipt.get("schema_version") != "orion.v2.v1-handoff-receipt.v1":
        errors.append("unexpected schema_version")
    if receipt.get("handoff_terminal") != "V1_FREEZE_HANDOFF_BOUND_AND_NON_RETROACTIVE":
        errors.append("handoff terminal is not bound")
    source = receipt.get("source") or {}
    if source.get("repository") != "SzeChunYiu/ORION":
        errors.append("wrong source repository")
    for name in ("freeze_commit", "freeze_subject_commit", "freeze_base_tree"):
        value = source.get(name)
        if not isinstance(value, str) or len(value) != 40:
            errors.append(f"{name} must be a 40-character Git SHA")
    control_plane = receipt.get("control_plane") or {}
    missing = REQUIRED_CONTROL_PLANE - set(control_plane)
    if missing:
        errors.append("missing control-plane bindings: " + ", ".join(sorted(missing)))
    for name, binding in control_plane.items():
        if name not in REQUIRED_CONTROL_PLANE:
            errors.append(f"unexpected control-plane binding: {name}")
            continue
        if not isinstance(binding, Mapping):
            errors.append(f"control-plane binding {name} must be an object")
            continue
        if not str(binding.get("path", "")).strip():
            errors.append(f"control-plane binding {name} lacks a path")
        identity = str(binding.get("git_identity", ""))
        if len(identity) != 40:
            errors.append(f"control-plane binding {name} lacks a Git identity")
    non_retroactivity = receipt.get("non_retroactivity") or {}
    if non_retroactivity.get("v1_history_immutable") is not True:
        errors.append("V1 history is not declared immutable")
    if non_retroactivity.get("v2_cannot_rewrite_v1_terminals") is not True:
        errors.append("non-retroactivity terminal protection missing")
    permissions = receipt.get("permissions") or {}
    if permissions.get("reference_implementation_authorized") is not True:
        errors.append("reference implementation is not authorized")
    if permissions.get("scientific_claim_promotion_authorized") is not False:
        errors.append("handoff must not grant scientific claim promotion")
    terminal = "V1_HANDOFF_VALID" if not errors else "V1_HANDOFF_INVALID"
    return HandoffValidation(not errors, terminal, tuple(errors))


def load_and_validate(path: str | Path) -> HandoffValidation:
    with Path(path).open("r", encoding="utf-8") as handle:
        receipt = json.load(handle)
    return validate_handoff_receipt(receipt)
