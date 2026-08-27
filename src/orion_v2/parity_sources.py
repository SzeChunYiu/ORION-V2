from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EXPECTED_SCHEMA = "orion.v2.v1-parity-case-source-audit.v1"
EXPECTED_V1_COMMIT = "8f250fc3e55d6d6a28fb1fb33d9932ef1a8760b5"
EXPECTED_CAMPAIGNS = {f"PARITY-{letter}" for letter in "ABCDEFGHI"}
_ALLOWED_SOURCE_STATUS = {
    "V1_NATIVE_SOURCE_ANCHORS_BOUND",
    "PARTIAL_V1_NATIVE_SOURCE_ANCHORS",
    "V1_NATIVE_SOURCE_ANCHORS_BOUND_EXTERNAL_CUSTODY_OPEN",
}
_REQUIRED_AUTHORITY_FALSE = {
    "grants_v1_parity",
    "grants_v2_closeout",
    "grants_architecture_authority",
    "grants_scientific_truth",
    "grants_novelty",
    "grants_publication_authority",
}


@dataclass(frozen=True, slots=True)
class ParityCaseSourceAuditValidation:
    valid: bool
    source_count: int
    covered_campaign_count: int
    partial_campaign_ids: tuple[str, ...]
    errors: tuple[str, ...]
    terminal: str
    run_authorized: bool = False

    def __post_init__(self) -> None:
        if self.run_authorized:
            raise ValueError("case-source audit validation cannot authorize a parity run")


def _is_sha(value: object) -> bool:
    text = str(value)
    return len(text) == 40 and all(ch in "0123456789abcdef" for ch in text)


def validate_parity_case_source_audit(audit: Mapping[str, Any]) -> ParityCaseSourceAuditValidation:
    errors: list[str] = []

    if audit.get("schema_version") != EXPECTED_SCHEMA:
        errors.append("unexpected case-source audit schema_version")
    if audit.get("status") != "V1_NATIVE_SOURCES_BOUND_PROTECTED_CASE_SELECTION_OPEN":
        errors.append("case-source audit must keep protected selection open")

    frozen = audit.get("frozen_v1")
    if not isinstance(frozen, Mapping):
        frozen = {}
        errors.append("frozen_v1 block is missing")
    if frozen.get("freeze_commit") != EXPECTED_V1_COMMIT:
        errors.append("case-source audit does not bind the frozen V1 commit")
    if frozen.get("capability_count") != 59:
        errors.append("case-source audit does not preserve the 59-cell denominator")
    for key in ("harness_readme_blob_sha", "harness_tests_tree_sha"):
        if not _is_sha(frozen.get(key)):
            errors.append(f"frozen_v1.{key} must be one exact Git object SHA")

    rows = audit.get("audited_sources")
    if not isinstance(rows, list) or not rows:
        rows = []
        errors.append("audited_sources must be a non-empty list")
    source_ids: list[str] = []
    paths: list[str] = []
    covered: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            errors.append(f"audited_sources[{index}] must be an object")
            continue
        source_id = str(row.get("source_id", ""))
        path = str(row.get("path", ""))
        source_ids.append(source_id)
        paths.append(path)
        if not source_id.strip() or not path.strip():
            errors.append(f"audited source {index} lacks identity or path")
        if not _is_sha(row.get("blob_sha")):
            errors.append(f"audited source {source_id!r} lacks exact blob SHA")
        campaigns = row.get("campaign_ids")
        if not isinstance(campaigns, list) or not campaigns:
            errors.append(f"audited source {source_id!r} has no campaign mapping")
            campaigns = []
        unknown = sorted(set(map(str, campaigns)) - EXPECTED_CAMPAIGNS)
        if unknown:
            errors.append(f"audited source {source_id!r} maps unknown campaigns: {', '.join(unknown)}")
        covered.update(map(str, campaigns))
        falsifiers = row.get("falsifiers")
        if not isinstance(falsifiers, list) or not falsifiers or any(not str(item).strip() for item in falsifiers):
            errors.append(f"audited source {source_id!r} lacks explicit falsifiers")
    if len(source_ids) != len(set(source_ids)):
        errors.append("audited source identities must be unique")
    if len(paths) != len(set(paths)):
        errors.append("audited source paths must be unique")

    statuses = audit.get("campaign_source_status")
    if not isinstance(statuses, list):
        statuses = []
        errors.append("campaign_source_status must be a list")
    status_ids: list[str] = []
    partial: list[str] = []
    for row in statuses:
        if not isinstance(row, Mapping):
            errors.append("campaign source status row must be an object")
            continue
        campaign_id = str(row.get("campaign_id", ""))
        status = str(row.get("status", ""))
        status_ids.append(campaign_id)
        if campaign_id not in EXPECTED_CAMPAIGNS:
            errors.append(f"unknown campaign source status {campaign_id!r}")
        if status not in _ALLOWED_SOURCE_STATUS:
            errors.append(f"invalid source status {status!r} for {campaign_id!r}")
        if status == "PARTIAL_V1_NATIVE_SOURCE_ANCHORS":
            partial.append(campaign_id)
        if not str(row.get("remaining", "")).strip():
            errors.append(f"campaign {campaign_id!r} must disclose remaining source work")
    if set(status_ids) != EXPECTED_CAMPAIGNS or len(status_ids) != len(EXPECTED_CAMPAIGNS):
        errors.append("campaign_source_status must contain exactly PARITY-A through PARITY-I")
    if covered != EXPECTED_CAMPAIGNS:
        missing = sorted(EXPECTED_CAMPAIGNS - covered)
        errors.append("audited sources do not map every parity campaign: " + ", ".join(missing))

    gaps = audit.get("global_gaps")
    if not isinstance(gaps, list) or not gaps:
        errors.append("case-source audit must retain explicit global gaps")

    run_gate = audit.get("run_gate")
    if not isinstance(run_gate, Mapping) or run_gate.get("allowed_now") is not False:
        errors.append("case-source audit cannot authorize a parity run")

    authority = audit.get("authority")
    if not isinstance(authority, Mapping):
        authority = {}
        errors.append("authority block is missing")
    for key in _REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            errors.append(f"case-source audit may not grant {key}")

    return ParityCaseSourceAuditValidation(
        valid=not errors,
        source_count=len(rows),
        covered_campaign_count=len(covered & EXPECTED_CAMPAIGNS),
        partial_campaign_ids=tuple(sorted(partial)),
        errors=tuple(errors),
        terminal=(
            "V1_NATIVE_CASE_SOURCES_VALID_PROTECTED_SELECTION_OPEN"
            if not errors
            else "V1_NATIVE_CASE_SOURCE_AUDIT_INVALID"
        ),
    )
