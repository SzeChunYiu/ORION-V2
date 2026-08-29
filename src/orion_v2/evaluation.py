from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ParityDisposition(str, Enum):
    PRESERVE_NATIVE = "PRESERVE_NATIVE"
    PRESERVE_AS_SPECIAL_CASE = "PRESERVE_AS_SPECIAL_CASE"
    MERGE_INTO_DEEPER_OBJECT = "MERGE_INTO_DEEPER_OBJECT"
    SPLIT_BY_CONTEXT = "SPLIT_BY_CONTEXT"
    REPLACE_WITH_PARENT_METHOD = "REPLACE_WITH_PARENT_METHOD"
    REPLACE_WITH_DONOR_PRODUCT = "REPLACE_WITH_DONOR_PRODUCT"
    GENERALIZE_WITH_NEW_COORDINATE = "GENERALIZE_WITH_NEW_COORDINATE"
    DEPRECATE_AFTER_PROTECTED_NONINFERIORITY = "DEPRECATE_AFTER_PROTECTED_NONINFERIORITY"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CapabilityParityRecord:
    capability_id: str
    disposition: ParityDisposition
    v1_evidence_ids: tuple[str, ...]
    v2_object_ids: tuple[str, ...] = ()
    parent_ids: tuple[str, ...] = ()
    protected_result_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id must be non-blank")
        object.__setattr__(self, "disposition", ParityDisposition(self.disposition))
        if not self.v1_evidence_ids or any(not item.strip() for item in self.v1_evidence_ids):
            raise ValueError("v1_evidence_ids are required")
        if self.disposition is ParityDisposition.DEPRECATE_AFTER_PROTECTED_NONINFERIORITY and not self.protected_result_ids:
            raise ValueError("deprecation requires protected non-inferiority evidence")
        if self.disposition in {
            ParityDisposition.REPLACE_WITH_PARENT_METHOD,
            ParityDisposition.REPLACE_WITH_DONOR_PRODUCT,
        } and not self.parent_ids:
            raise ValueError("replacement dispositions require parent identities")
        if self.disposition not in {ParityDisposition.CANNOT_CHECK} and not self.v2_object_ids:
            raise ValueError("a resolved disposition must bind at least one V2 object")


@dataclass(frozen=True, slots=True)
class SaturationVector:
    coverage_gap: float
    open_routes: int
    new_coordinate_rate: float
    new_relation_rate: float
    new_obstruction_rate: float
    new_failure_rate: float
    parent_contraction_rate: float
    benchmark_family_growth: int
    unresolved_collision_rate: float
    mandatory_routes_completed: bool

    def __post_init__(self) -> None:
        for name in (
            "coverage_gap",
            "new_coordinate_rate",
            "new_relation_rate",
            "new_obstruction_rate",
            "new_failure_rate",
            "parent_contraction_rate",
            "unresolved_collision_rate",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.open_routes < 0 or self.benchmark_family_growth < 0:
            raise ValueError("counts must be non-negative")

    def is_no_material_change(
        self,
        *,
        rate_threshold: float = 0.0,
        allow_censored_open_routes: bool = False,
    ) -> bool:
        if not self.mandatory_routes_completed:
            return False
        if self.coverage_gap > rate_threshold:
            return False
        if self.open_routes and not allow_censored_open_routes:
            return False
        rates = (
            self.new_coordinate_rate,
            self.new_relation_rate,
            self.new_obstruction_rate,
            self.new_failure_rate,
            self.parent_contraction_rate,
            self.unresolved_collision_rate,
        )
        return all(rate <= rate_threshold for rate in rates) and self.benchmark_family_growth == 0
