from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DonorDisposition(str, Enum):
    BLOCKED_NATIVE_RECONSTRUCTION = "BLOCKED_NATIVE_RECONSTRUCTION"
    BLOCKED_MAPPING = "BLOCKED_MAPPING"
    ABSORBED_SPECIAL_CASE = "ABSORBED_SPECIAL_CASE"
    CONSERVATIVE_ENVELOPE = "CONSERVATIVE_ENVELOPE"
    IDEAL_DONOR_PRODUCT_EQUIVALENCE = "IDEAL_DONOR_PRODUCT_EQUIVALENCE"
    CANDIDATE_STRICT_RESIDUAL = "CANDIDATE_STRICT_RESIDUAL"
    REFUTED_BY_PARENT = "REFUTED_BY_PARENT"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class DomainProblem:
    problem_id: str
    domain_id: str
    native_problem: str
    source_ids: tuple[str, ...]
    object_types: tuple[str, ...]
    state_types: tuple[str, ...]
    operation_types: tuple[str, ...]
    native_judgment_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("problem_id", "domain_id", "native_problem"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-blank")
        for name in ("source_ids", "object_types", "state_types", "operation_types", "native_judgment_ids"):
            values = getattr(self, name)
            if not values or any(not value.strip() for value in values):
                raise ValueError(f"{name} must contain non-blank values")
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must be unique")
        if any(not value.strip() for value in self.assumption_ids):
            raise ValueError("assumption_ids may not contain blanks")


@dataclass(frozen=True, slots=True)
class DonorReductionCase:
    case_id: str
    candidate_id: str
    donor_problems: tuple[DomainProblem, ...]
    reconstruction_receipt_ids: tuple[str, ...]
    mapping_ids: tuple[str, ...]
    preserved_native_judgment_ids: tuple[str, ...]
    added_coordinate_ids: tuple[str, ...] = ()
    strict_witness_ids: tuple[str, ...] = ()
    strongest_product_test_ids: tuple[str, ...] = ()
    strongest_product_ties: bool | None = None
    falsifier_ids: tuple[str, ...] = ()
    open_route_ids: tuple[str, ...] = ()
    parent_refutation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if any(not value.strip() for value in (self.case_id, self.candidate_id)):
            raise ValueError("case and candidate identities must be non-blank")
        if not self.donor_problems:
            raise ValueError("at least one donor problem is required")
        for name in ("reconstruction_receipt_ids", "mapping_ids", "preserved_native_judgment_ids", "added_coordinate_ids", "strict_witness_ids", "strongest_product_test_ids", "falsifier_ids", "open_route_ids", "parent_refutation_ids"):
            values = getattr(self, name)
            if any(not value.strip() for value in values):
                raise ValueError(f"{name} may not contain blanks")
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must be unique")
        if self.strict_witness_ids and not self.added_coordinate_ids:
            raise ValueError("strict witnesses require explicit added coordinates")
        if self.strongest_product_ties is not None and not self.strongest_product_test_ids:
            raise ValueError("a donor-product verdict requires test identities")


@dataclass(frozen=True, slots=True)
class DonorReductionReceipt:
    case_id: str
    disposition: DonorDisposition
    reasons: tuple[str, ...]
    donor_count: int
    preserved_native_judgment_count: int
    scientific_truth_authorized: bool = False
    novelty_authorized: bool = False

    def __post_init__(self) -> None:
        if self.scientific_truth_authorized or self.novelty_authorized:
            raise ValueError("donor reduction receipts are non-authorizing")


def reduce_donors(case: DonorReductionCase) -> DonorReductionReceipt:
    def receipt(disposition: DonorDisposition, *reasons: str) -> DonorReductionReceipt:
        return DonorReductionReceipt(case.case_id, disposition, tuple(reasons), len(case.donor_problems), len(case.preserved_native_judgment_ids))
    if case.parent_refutation_ids:
        return receipt(DonorDisposition.REFUTED_BY_PARENT, "a native parent directly refutes the candidate residual", *case.parent_refutation_ids)
    if not case.reconstruction_receipt_ids or not case.preserved_native_judgment_ids:
        return receipt(DonorDisposition.BLOCKED_NATIVE_RECONSTRUCTION, "native reconstruction and judgment preservation are required")
    if not case.mapping_ids:
        return receipt(DonorDisposition.BLOCKED_MAPPING, "no explicit structural mapping is bound")
    if not case.added_coordinate_ids:
        return receipt(DonorDisposition.ABSORBED_SPECIAL_CASE, "the candidate is a donor special case")
    if not case.strict_witness_ids:
        return receipt(DonorDisposition.CONSERVATIVE_ENVELOPE, "added coordinates exist but no strict witness survives")
    if case.strongest_product_ties is None:
        return receipt(DonorDisposition.CANNOT_CHECK, "strongest donor product has not been tested")
    if case.strongest_product_ties:
        return receipt(DonorDisposition.IDEAL_DONOR_PRODUCT_EQUIVALENCE, "strongest donor product ties the candidate")
    if case.open_route_ids or not case.falsifier_ids:
        return receipt(DonorDisposition.CANNOT_CHECK, "open routes or missing falsifiers block a strict residual", *case.open_route_ids)
    return receipt(DonorDisposition.CANDIDATE_STRICT_RESIDUAL, "a strict witness survives the strongest donor product")
