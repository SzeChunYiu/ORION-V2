"""Fail-closed donor reduction assessor V0.

This is a V2 research-control model derived from the established ORION donor-
envelope workflow. It distinguishes useful absorption and composition outcomes
without granting scientific truth, novelty or framework admission.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class DonorReductionResult:
    verdict: str
    reasons: tuple[str, ...]
    grants_scientific_truth: bool = False
    grants_novelty: bool = False
    grants_v2_admission: bool = False


def _ids(case: Mapping[str, Any], field: str) -> tuple[str, ...]:
    raw = case.get(field, ())
    if not isinstance(raw, (list, tuple)):
        return ()
    values = tuple(str(item) for item in raw)
    if any(not item for item in values) or len(values) != len(set(values)):
        return ()
    return values


def assess_donor_reduction(case: Mapping[str, Any]) -> DonorReductionResult:
    """Apply the frozen V0 reduction sequence to one candidate claim."""

    collision = str(case.get("v1_collision_status", "NOT_CHECKED"))
    if collision in {"NOT_CHECKED", "CANNOT_CHECK"}:
        return DonorReductionResult(
            "BLOCKED_V1_COLLISION_AUDIT",
            ("exact V1 ownership/collision audit is incomplete",),
        )
    if collision == "FULLY_V1_OWNED":
        return DonorReductionResult(
            "FULLY_OWNED_BY_V1",
            ("the candidate is already owned by frozen V1 and cannot become a V2 claim",),
        )

    if not _ids(case, "absorption_receipt_ids"):
        return DonorReductionResult(
            "BLOCKED_ABSORPTION_INCOMPLETE",
            ("no admitted native mechanism/structural absorption receipt is bound",),
        )

    if not _ids(case, "donor_claim_ids") or not _ids(
        case, "donor_assumption_ids"
    ) or not _ids(case, "donor_reconstruction_ids"):
        return DonorReductionResult(
            "BLOCKED_DONOR_RECONSTRUCTION",
            ("donor claims, assumptions and native reconstruction are required",),
        )

    if not str(case.get("embedding_map_id", "")) or not _ids(
        case, "preservation_obligation_ids"
    ):
        return DonorReductionResult(
            "BLOCKED_CONSERVATIVE_EMBEDDING",
            ("an explicit embedding and preservation obligations are required",),
        )

    added = _ids(case, "added_coordinate_ids")
    if not added:
        return DonorReductionResult(
            "ABSORBED_SPECIAL_CASE",
            ("the donor is reconstructed and preserved as a special case",),
        )

    strict = _ids(case, "strict_separation_witness_ids")
    if not strict:
        return DonorReductionResult(
            "CONSERVATIVE_ENVELOPE",
            (
                "added coordinates are explicit and donor behavior is preserved",
                "no strict separation witness has survived",
            ),
        )

    product_relation = str(case.get("ideal_donor_product_relation", "UNTESTED"))
    product_evidence = _ids(case, "ideal_donor_product_evidence_ids")
    if product_relation == "UNTESTED" or not product_evidence:
        return DonorReductionResult(
            "BLOCKED_IDEAL_DONOR_PRODUCT",
            ("the strongest compatible donor product has not been tested",),
        )
    if product_relation == "TIES_CANDIDATE":
        return DonorReductionResult(
            "IDEAL_DONOR_PRODUCT_EQUIVALENCE",
            (
                "the candidate separates an isolated donor on a registered witness",
                "the strongest compatible donor product ties the candidate",
                "the supported result is an interface/composition boundary, not distinct superiority",
            ),
        )
    if product_relation != "CANDIDATE_SEPARATES":
        return DonorReductionResult(
            "CANNOT_CHECK",
            ("unrecognized or unresolved ideal donor product relation",),
        )

    open_routes = _ids(case, "open_route_ids")
    if open_routes:
        return DonorReductionResult(
            "BLOCKED_OPEN_ROUTES",
            tuple(f"open donor/formulation route: {route}" for route in open_routes),
        )

    if not _ids(case, "falsifier_ids"):
        return DonorReductionResult(
            "BLOCKED_NO_FALSIFIER",
            ("candidate strict envelope requires registered falsifiers",),
        )
    if not _ids(case, "fresh_evaluation_ids"):
        return DonorReductionResult(
            "BLOCKED_NO_FRESH_EVALUATION",
            ("candidate strict envelope requires protected fresh evaluation",),
        )

    return DonorReductionResult(
        "CANDIDATE_STRICT_ENVELOPE",
        (
            "native donors are reconstructed and conservatively embedded",
            "a strict witness survives the strongest compatible donor product",
            "registered falsifiers and fresh evaluation are bound",
            "the terminal remains non-authorizing",
        ),
    )


__all__ = ["DonorReductionResult", "assess_donor_reduction"]
