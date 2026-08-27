"""Reticulate component provenance and alternative-support reference model V0.

This transparent model demonstrates why one declared parent or commit ancestry can
be insufficient for scientific inheritance. It is not a complete provenance or
certificate-transport implementation.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


class ProvenanceInputError(ValueError):
    pass


def artifact_parent_ids(components: Sequence[Mapping[str, Any]]) -> frozenset[str]:
    parents: set[str] = set()
    component_ids: set[str] = set()
    for component in components:
        component_id = str(component.get("component_id", ""))
        parent_id = str(component.get("parent_id", ""))
        contribution_kind = str(component.get("contribution_kind", ""))
        if not component_id or not parent_id or not contribution_kind:
            raise ProvenanceInputError("components require id, parent and contribution kind")
        if component_id in component_ids:
            raise ProvenanceInputError("component identities must be unique")
        component_ids.add(component_id)
        parents.add(parent_id)
    return frozenset(parents)


def declared_single_parent_is_complete(
    components: Sequence[Mapping[str, Any]], declared_parent_id: str
) -> bool:
    if not declared_parent_id:
        raise ProvenanceInputError("declared parent identity is required")
    return artifact_parent_ids(components) == frozenset({declared_parent_id})


def claim_support_status(
    support_families: Sequence[Sequence[str]], revoked_parent_ids: Sequence[str]
) -> str:
    """Classify a claim after parent revocation with alternative support families."""

    if not support_families:
        raise ProvenanceInputError("claim requires at least one support family")
    normalized: list[frozenset[str]] = []
    for family in support_families:
        values = frozenset(str(item) for item in family)
        if not values or any(not item for item in values):
            raise ProvenanceInputError("support families must contain non-empty parent ids")
        normalized.append(values)

    revoked = frozenset(str(item) for item in revoked_parent_ids)
    affected = [family for family in normalized if family & revoked]
    surviving = [family for family in normalized if not family & revoked]
    if not affected:
        return "UNAFFECTED"
    if surviving:
        return "VALID_ALTERNATIVE_SUPPORT"
    return "INVALIDATED"


def classify_claims_after_revocation(
    claims: Sequence[Mapping[str, Any]], revoked_parent_ids: Sequence[str]
) -> dict[str, str]:
    result: dict[str, str] = {}
    for claim in claims:
        claim_id = str(claim.get("claim_id", ""))
        if not claim_id or claim_id in result:
            raise ProvenanceInputError("claim ids must be non-empty and unique")
        result[claim_id] = claim_support_status(
            claim.get("support_families", ()), revoked_parent_ids
        )
    return result


__all__ = [
    "ProvenanceInputError",
    "artifact_parent_ids",
    "claim_support_status",
    "classify_claims_after_revocation",
    "declared_single_parent_is_complete",
]
