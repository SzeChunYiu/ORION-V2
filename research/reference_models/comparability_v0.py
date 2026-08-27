"""Cross-generation comparability reference model V0.

This exact rule set exists to exercise known scientific distinctions. It is not
a universal linking/equating method and grants no reuse or adoption authority.
"""

from __future__ import annotations

from typing import Any, Mapping


VALID_RELATIONS = {"EQUIVALENT", "REFINES", "CONTEXTUAL", "INCOMPATIBLE", "UNMAPPED"}


def classify_comparability(record: Mapping[str, Any]) -> str:
    relation = str(record.get("semantic_relation", "UNMAPPED")).upper()
    if relation not in VALID_RELATIONS:
        return "CANNOT_CHECK"

    uncertainty = record.get("uncertainty")
    tolerance = record.get("tolerance")
    if not isinstance(uncertainty, (int, float)) or not isinstance(tolerance, (int, float)):
        return "CANNOT_CHECK"
    if uncertainty < 0 or tolerance < 0:
        return "CANNOT_CHECK"

    if relation == "INCOMPATIBLE":
        return "NONCOMPARABLE"
    if relation == "UNMAPPED" or not bool(record.get("mapping_recoverable")):
        return "CANNOT_CHECK"

    if uncertainty > tolerance:
        return "NONCOMPARABLE_UNDER_TOLERANCE"

    anchors_required = bool(record.get("anchors_required"))
    anchors_complete = bool(record.get("anchors_complete"))
    partial_anchor = bool(record.get("partial_anchor_evidence"))
    if anchors_required and not anchors_complete and not partial_anchor:
        return "CANNOT_CHECK"

    invariance_required = bool(record.get("invariance_required"))
    invariance_passed = bool(record.get("invariance_passed"))
    partial_invariance = bool(record.get("partial_invariance_evidence"))
    if invariance_required and not invariance_passed and not partial_invariance:
        return "CANNOT_CHECK"

    content_preserved = bool(record.get("evidence_content_preserved"))
    obligation_preserved = bool(record.get("obligation_meaning_preserved"))
    if content_preserved and not obligation_preserved:
        return "CONTENT_COMPARABLE_CLOSURE_REOPEN"
    if not content_preserved:
        return "NONCOMPARABLE"

    if relation in {"EQUIVALENT", "REFINES"} and (
        not anchors_required or anchors_complete
    ) and (not invariance_required or invariance_passed):
        return "COMPARABLE"

    return "PARTIALLY_COMPARABLE"


__all__ = ["classify_comparability"]
