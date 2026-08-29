from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EXPECTED_PROTOCOL_SCHEMA = "orion.v2.v1-parity-campaign-protocol.v1"
EXPECTED_BINDING_SCHEMA = "orion.v2.v1-parity-subject-binding.v1"
EXPECTED_CENSUS_SCHEMA = "orion.v2.v1-capability-census.v1"
EXPECTED_CAMPAIGNS = 9
EXPECTED_CAPABILITIES = 59
EXPECTED_AGGREGATION = "PER_CELL_NON_COMPENSATORY__NO_FAMILY_AVERAGE_CAN_HIDE_A_LOST_CELL"
EXPECTED_CI_CHECKS = {
    "reference-tests",
    "unified-reference",
    "stochastic-reference",
    "native-recovery",
}
MANDATORY_COORDINATES = {
    "scientific_validity_or_known_answer",
    "false_completion",
    "authority_and_integrity",
    "semantic_and_provenance_preservation",
    "cannot_check_calibration",
    "replay_identity",
}


@dataclass(frozen=True, slots=True)
class ParityProtocolValidation:
    valid: bool
    campaign_count: int
    capability_count: int
    errors: tuple[str, ...]
    terminal: str


@dataclass(frozen=True, slots=True)
class ParitySubjectBindingValidation:
    valid: bool
    subject_commit: str
    ci_check_count: int
    errors: tuple[str, ...]
    terminal: str
    run_authorized: bool = False

    def __post_init__(self) -> None:
        if self.run_authorized:
            raise ValueError("subject binding validation cannot authorize a parity run")


def validate_parity_protocol(
    protocol: Mapping[str, Any], census: Mapping[str, Any]
) -> ParityProtocolValidation:
    """Validate the prospective parity design without granting run authority.

    The protocol is intentionally checked against the exact frozen 59-cell census.
    A missing, duplicated or invented capability fails closed. A valid design is
    only ready to bind an exact V2 subject and case/evaluator manifests; it does
    not authorize an outcome-generating parity run by itself.
    """

    errors: list[str] = []

    if protocol.get("schema_version") != EXPECTED_PROTOCOL_SCHEMA:
        errors.append("unexpected parity protocol schema_version")
    if census.get("schema_version") != EXPECTED_CENSUS_SCHEMA:
        errors.append("unexpected capability census schema_version")
    if protocol.get("status") != "DESIGN_FROZEN_V2_SUBJECT_UNBOUND":
        errors.append("parity design must remain frozen with V2 subject unbound")

    census_rows = census.get("capabilities")
    if not isinstance(census_rows, list):
        census_rows = []
        errors.append("capability census must contain a list")
    census_ids = [
        str(row.get("capability_id", ""))
        for row in census_rows
        if isinstance(row, Mapping)
    ]
    if len(census_ids) != EXPECTED_CAPABILITIES:
        errors.append(
            f"expected {EXPECTED_CAPABILITIES} frozen capabilities, observed {len(census_ids)}"
        )
    if len(set(census_ids)) != len(census_ids):
        errors.append("frozen capability census identities are not unique")

    frozen_v1 = protocol.get("frozen_v1")
    if not isinstance(frozen_v1, Mapping):
        frozen_v1 = {}
        errors.append("frozen_v1 binding is missing")
    census_source = census.get("source")
    if not isinstance(census_source, Mapping):
        census_source = {}
    if frozen_v1.get("freeze_commit") != census_source.get("freeze_commit"):
        errors.append("parity protocol and capability census bind different V1 commits")
    if frozen_v1.get("capability_count") != EXPECTED_CAPABILITIES:
        errors.append("parity protocol does not bind the 59-cell denominator")

    campaigns = protocol.get("campaigns")
    if not isinstance(campaigns, list):
        campaigns = []
        errors.append("campaigns must be a list")
    if len(campaigns) != EXPECTED_CAMPAIGNS:
        errors.append(
            f"expected {EXPECTED_CAMPAIGNS} parity campaigns, observed {len(campaigns)}"
        )

    campaign_ids: list[str] = []
    assigned: list[str] = []
    for index, campaign in enumerate(campaigns):
        if not isinstance(campaign, Mapping):
            errors.append(f"campaign[{index}] must be an object")
            continue
        campaign_id = str(campaign.get("campaign_id", ""))
        campaign_ids.append(campaign_id)
        if not campaign_id:
            errors.append(f"campaign[{index}] lacks identity")
        capability_ids = campaign.get("capability_ids")
        if not isinstance(capability_ids, list) or not capability_ids:
            errors.append(f"campaign {campaign_id!r} has no capability denominator")
        else:
            assigned.extend(str(item) for item in capability_ids)
        hostile = campaign.get("hostile_controls")
        if not isinstance(hostile, list) or not hostile:
            errors.append(f"campaign {campaign_id!r} has no hostile controls")

    if len(campaign_ids) != len(set(campaign_ids)):
        errors.append("parity campaign identities must be unique")
    duplicates = sorted({item for item in assigned if assigned.count(item) > 1})
    if duplicates:
        errors.append("capabilities assigned to multiple campaigns: " + ", ".join(duplicates))
    missing = sorted(set(census_ids) - set(assigned))
    unknown = sorted(set(assigned) - set(census_ids))
    if missing:
        errors.append("frozen capabilities missing from parity protocol: " + ", ".join(missing))
    if unknown:
        errors.append("non-census capabilities invented by parity protocol: " + ", ".join(unknown))
    if len(assigned) != EXPECTED_CAPABILITIES:
        errors.append(
            f"parity assignment denominator must be {EXPECTED_CAPABILITIES}, observed {len(assigned)}"
        )

    comparison = protocol.get("comparison_contract")
    if not isinstance(comparison, Mapping):
        comparison = {}
        errors.append("comparison_contract is missing")
    mandatory = comparison.get("mandatory_coordinates")
    if not isinstance(mandatory, list) or not MANDATORY_COORDINATES.issubset(
        {str(item) for item in mandatory}
    ):
        errors.append("mandatory non-compensatory parity coordinates are incomplete")
    if comparison.get("aggregation_rule") != EXPECTED_AGGREGATION:
        errors.append("per-cell non-compensatory aggregation rule was changed")

    run_gate = protocol.get("run_gate")
    if not isinstance(run_gate, Mapping) or run_gate.get("allowed_now") is not False:
        errors.append("design freeze must not self-authorize a parity run")
    v2_subject = protocol.get("v2_subject")
    if not isinstance(v2_subject, Mapping) or v2_subject.get("commit") != (
        "TO_BIND_AFTER_KERNEL_CONTRACTION_BEFORE_OUTCOME_ACCESS"
    ):
        errors.append("V2 subject must remain outcome-blind and unbound in the design freeze")

    authority = protocol.get("authority")
    if not isinstance(authority, Mapping):
        authority = {}
        errors.append("authority block is missing")
    for key in (
        "grants_v2_closeout",
        "grants_scientific_truth",
        "grants_novelty",
        "grants_publication_authority",
    ):
        if authority.get(key) is not False:
            errors.append(f"parity design may not grant {key}")

    terminal = (
        "PARITY_PROTOCOL_READY_TO_BIND_V2_SUBJECT"
        if not errors
        else "PARITY_PROTOCOL_INVALID"
    )
    return ParityProtocolValidation(
        valid=not errors,
        campaign_count=len(campaigns),
        capability_count=len(assigned),
        errors=tuple(errors),
        terminal=terminal,
    )


def validate_parity_subject_binding(
    binding: Mapping[str, Any],
    protocol: Mapping[str, Any],
    *,
    expected_subject_commit: str | None = None,
    expected_protocol_blob_sha: str | None = None,
) -> ParitySubjectBindingValidation:
    """Validate immutable outcome-blind subject binding without run authority."""

    errors: list[str] = []
    if binding.get("schema_version") != EXPECTED_BINDING_SCHEMA:
        errors.append("unexpected parity subject-binding schema_version")

    protocol_block = binding.get("protocol")
    if not isinstance(protocol_block, Mapping):
        protocol_block = {}
        errors.append("protocol binding is missing")
    if protocol_block.get("protocol_id") != protocol.get("protocol_id"):
        errors.append("binding and frozen protocol identities differ")
    if protocol_block.get("design_status") != "DESIGN_FROZEN_V2_SUBJECT_UNBOUND":
        errors.append("binding must point to the unmodified frozen design")
    if expected_protocol_blob_sha is not None and protocol_block.get("blob_sha") != expected_protocol_blob_sha:
        errors.append("binding does not point to the expected frozen protocol blob")

    frozen_v1 = binding.get("frozen_v1")
    protocol_v1 = protocol.get("frozen_v1")
    if not isinstance(frozen_v1, Mapping) or not isinstance(protocol_v1, Mapping):
        errors.append("V1 binding is missing")
        frozen_v1 = {}
        protocol_v1 = {}
    if frozen_v1.get("freeze_commit") != protocol_v1.get("freeze_commit"):
        errors.append("subject binding changed the frozen V1 commit")
    if frozen_v1.get("capability_count") != EXPECTED_CAPABILITIES:
        errors.append("subject binding does not preserve the 59-cell denominator")

    subject = binding.get("v2_subject")
    if not isinstance(subject, Mapping):
        subject = {}
        errors.append("V2 subject block is missing")
    subject_commit = str(subject.get("commit", ""))
    if len(subject_commit) != 40 or any(character not in "0123456789abcdef" for character in subject_commit):
        errors.append("V2 subject must bind one exact lowercase 40-hex commit")
    if expected_subject_commit is not None and subject_commit != expected_subject_commit:
        errors.append("V2 subject commit differs from the expected contracted commit")
    for key in (
        "kernel_api_version",
        "kernel_facade_blob_sha",
        "kernel_disposition_blob_sha",
        "package_root_blob_sha",
    ):
        if not str(subject.get(key, "")).strip():
            errors.append(f"V2 subject lacks {key}")

    ci = binding.get("pre_binding_ci")
    if not isinstance(ci, list):
        ci = []
        errors.append("pre-binding CI list is missing")
    names: list[str] = []
    for row in ci:
        if not isinstance(row, Mapping):
            errors.append("pre-binding CI row must be an object")
            continue
        name = str(row.get("check_name", ""))
        names.append(name)
        if row.get("conclusion") != "success":
            errors.append(f"pre-binding CI check {name!r} is not successful")
        if not isinstance(row.get("check_run_id"), int):
            errors.append(f"pre-binding CI check {name!r} lacks numeric check-run identity")
    if set(names) != EXPECTED_CI_CHECKS or len(names) != len(EXPECTED_CI_CHECKS):
        errors.append("pre-binding CI must bind exactly the four convergence checks")

    custody = binding.get("custody")
    if not isinstance(custody, Mapping):
        custody = {}
        errors.append("custody block is missing")
    for key in ("outcome_access_before_binding", "parity_outcomes_observed", "binding_mutable"):
        if custody.get(key) is not False:
            errors.append(f"subject binding requires {key}=false")

    run_gate = binding.get("run_gate")
    if not isinstance(run_gate, Mapping) or run_gate.get("allowed_now") is not False:
        errors.append("subject binding cannot authorize parity execution")
    if binding.get("terminal") != "PARITY_SUBJECT_BOUND_RUN_NOT_AUTHORIZED":
        errors.append("unexpected subject-binding terminal")

    authority = binding.get("authority")
    if not isinstance(authority, Mapping):
        authority = {}
        errors.append("authority block is missing")
    for key in (
        "grants_v2_closeout",
        "grants_architecture_authority",
        "grants_scientific_truth",
        "grants_novelty",
        "grants_publication_authority",
    ):
        if authority.get(key) is not False:
            errors.append(f"subject binding may not grant {key}")

    return ParitySubjectBindingValidation(
        valid=not errors,
        subject_commit=subject_commit,
        ci_check_count=len(ci),
        errors=tuple(errors),
        terminal=(
            "PARITY_SUBJECT_BINDING_VALID_RUN_NOT_AUTHORIZED"
            if not errors
            else "PARITY_SUBJECT_BINDING_INVALID"
        ),
    )
