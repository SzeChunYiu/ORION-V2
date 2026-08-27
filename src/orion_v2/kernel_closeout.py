from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


EXPECTED_SCHEMA = "orion.v2.kernel-component-disposition.v1"
EXPECTED_FAMILIES = tuple(f"K{i}" for i in range(7))


@dataclass(frozen=True, slots=True)
class KernelDispositionValidation:
    valid: bool
    family_count: int
    interface_count: int
    unresolved_duplicate_count: int
    errors: tuple[str, ...]
    terminal: str


def validate_kernel_disposition(
    manifest: Mapping[str, Any], *, source_root: str | Path | None = None
) -> KernelDispositionValidation:
    """Validate the contraction manifest without freezing the architecture.

    A green result means that the candidate boundary is internally coherent and
    ready for duplicate-group disposition.  It does *not* mean the kernel is
    scientifically or architecturally admitted.
    """

    errors: list[str] = []
    if manifest.get("schema_version") != EXPECTED_SCHEMA:
        errors.append("unexpected kernel disposition schema_version")

    families = manifest.get("families")
    if not isinstance(families, list):
        families = []
        errors.append("families must be a list")

    family_ids: list[str] = []
    interfaces: list[str] = []
    supporting: list[str] = []
    for index, family in enumerate(families):
        if not isinstance(family, Mapping):
            errors.append(f"family[{index}] must be an object")
            continue
        family_id = str(family.get("family_id", ""))
        family_ids.append(family_id)
        if not str(family.get("name", "")).strip():
            errors.append(f"family {family_id!r} lacks name")
        if not str(family.get("downstream_role", "")).strip():
            errors.append(f"family {family_id!r} lacks downstream scientific role")
        candidates = family.get("interface_candidates")
        if not isinstance(candidates, list) or not candidates:
            errors.append(f"family {family_id!r} lacks stable interface candidates")
        else:
            interfaces.extend(str(item) for item in candidates)
        support = family.get("supporting_modules")
        if not isinstance(support, list):
            errors.append(f"family {family_id!r} supporting_modules must be a list")
        else:
            supporting.extend(str(item) for item in support)
        v1_families = family.get("v1_capability_families")
        if not isinstance(v1_families, list) or not v1_families:
            errors.append(f"family {family_id!r} lacks V1 capability-family mapping")

    if tuple(sorted(family_ids)) != EXPECTED_FAMILIES:
        errors.append(
            "kernel families must be exactly K0..K6; observed "
            + ", ".join(sorted(family_ids))
        )
    if len(family_ids) != len(set(family_ids)):
        errors.append("kernel family identities must be unique")
    duplicate_interfaces = sorted(
        {item for item in interfaces if interfaces.count(item) > 1}
    )
    if duplicate_interfaces:
        errors.append(
            "stable interface candidates have multiple owners: "
            + ", ".join(duplicate_interfaces)
        )

    parent_rows = manifest.get("parent_or_reference_modules")
    if not isinstance(parent_rows, list):
        parent_rows = []
        errors.append("parent_or_reference_modules must be a list")
    parent_modules: list[str] = []
    for index, row in enumerate(parent_rows):
        if not isinstance(row, Mapping):
            errors.append(f"parent/reference row[{index}] must be an object")
            continue
        module = str(row.get("module", ""))
        parent_modules.append(module)
        if not module or not str(row.get("owner", "")).strip() or not str(
            row.get("role", "")
        ).strip():
            errors.append(f"parent/reference row[{index}] lacks module/owner/role")
    if len(parent_modules) != len(set(parent_modules)):
        errors.append("parent/reference module identities must be unique")
    overlap = sorted(set(interfaces) & set(parent_modules))
    if overlap:
        errors.append(
            "stable interfaces cannot simultaneously be parent/reference implementations: "
            + ", ".join(overlap)
        )

    duplicate_groups = manifest.get("unresolved_duplicate_groups")
    if not isinstance(duplicate_groups, list):
        duplicate_groups = []
        errors.append("unresolved_duplicate_groups must be a list")
    duplicate_group_ids: list[str] = []
    for index, group in enumerate(duplicate_groups):
        if not isinstance(group, Mapping):
            errors.append(f"duplicate group[{index}] must be an object")
            continue
        group_id = str(group.get("group_id", ""))
        duplicate_group_ids.append(group_id)
        members = group.get("modules")
        if not group_id or not isinstance(members, list) or len(members) < 2:
            errors.append(f"duplicate group[{index}] lacks identity or >=2 modules")
        if not str(group.get("required_disposition", "")).strip():
            errors.append(f"duplicate group {group_id!r} lacks required disposition")
    if len(duplicate_group_ids) != len(set(duplicate_group_ids)):
        errors.append("duplicate-group identities must be unique")

    if duplicate_groups and manifest.get("kernel_frozen") is not False:
        errors.append("kernel cannot be frozen while semantic duplicate groups remain open")
    if not duplicate_groups and manifest.get("kernel_frozen") is True:
        # A no-duplicate manifest still needs parity/admission evidence; this schema
        # may record a freeze only after a successor closure artifact explicitly
        # binds those requirements.  This prevents hand-editing the planning file
        # into an authority-bearing architecture terminal.
        errors.append(
            "this planning manifest cannot self-freeze the kernel; use a separate protected freeze receipt"
        )

    requirements = manifest.get("freeze_requirements")
    if not isinstance(requirements, list) or len(requirements) < 6:
        errors.append("kernel freeze requirements are incomplete")

    for key in (
        "grants_architecture_authority",
        "grants_scientific_truth",
        "grants_novelty",
    ):
        if manifest.get(key) is not False:
            errors.append(f"kernel disposition may not grant {key}")

    if source_root is not None:
        root = Path(source_root)
        for module in interfaces:
            if not (root / f"{module}.py").is_file():
                errors.append(f"stable interface candidate has no source module: {module}")

    terminal = (
        "KERNEL_CANDIDATE_VALID_DUPLICATE_REDUCTION_OPEN"
        if not errors and duplicate_groups
        else "KERNEL_CANDIDATE_READY_FOR_PROTECTED_FREEZE_RECEIPT"
        if not errors
        else "KERNEL_DISPOSITION_INVALID"
    )
    return KernelDispositionValidation(
        valid=not errors,
        family_count=len(families),
        interface_count=len(interfaces),
        unresolved_duplicate_count=len(duplicate_groups),
        errors=tuple(errors),
        terminal=terminal,
    )
