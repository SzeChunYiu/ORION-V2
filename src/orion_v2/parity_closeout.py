from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EXPECTED_PROTOCOL_SCHEMA = "orion.v2.v1-parity-campaign-protocol.v1"
EXPECTED_CENSUS_SCHEMA = "orion.v2.v1-capability-census.v1"
EXPECTED_CAMPAIGNS = 9
EXPECTED_CAPABILITIES = 59
EXPECTED_AGGREGATION = "PER_CELL_NON_COMPENSATORY__NO_FAMILY_AVERAGE_CAN_HIDE_A_LOST_CELL"
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


def validate_parity_protocol(
    protocol: Mapping[str, Any], census: Mapping[str, Any]
) -> ParityProtocolValidation:
    """Validate the prospective parity design without granting run authority.

    The protocol is intentionally checked against the exact frozen 59-cell census.
    A missing, duplicated or invented capability fails closed.  A valid design is
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
