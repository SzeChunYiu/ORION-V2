"""Reference objects for bounded foundation-saturation assessment.

The module records whether a declared knowledge universe has been traversed
through native, changed-vocabulary and hostile-parent routes before a proposed
field foundation is synthesized. It intentionally grants no scientific,
disciplinary or publication authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class RouteDisposition(str, Enum):
    COMPLETE = "COMPLETE"
    CENSORED = "CENSORED"
    OPEN = "OPEN"


class FindingKind(str, Enum):
    COORDINATE = "COORDINATE"
    RELATION = "RELATION"
    OBSTRUCTION = "OBSTRUCTION"
    FAILURE = "FAILURE"
    PARENT_CONTRACTION = "PARENT_CONTRACTION"
    BENCHMARK = "BENCHMARK"
    NONE = "NONE"


class FoundationSaturationStatus(str, Enum):
    OPEN_COVERAGE = "OPEN_COVERAGE"
    REOPENED_MATERIAL_FINDING = "REOPENED_MATERIAL_FINDING"
    READY_FOR_INTERNAL_SYNTHESIS = "READY_FOR_INTERNAL_SYNTHESIS"
    READY_FOR_EXTERNAL_DEMARCATION = "READY_FOR_EXTERNAL_DEMARCATION"
    CANNOT_CHECK = "CANNOT_CHECK"


REQUIRED_CLEAN_PASSES = 3


@dataclass(frozen=True, slots=True)
class SearchRouteReceipt:
    route_id: str
    family_id: str
    disposition: RouteDisposition
    source_ids: tuple[str, ...] = ()
    censor_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.route_id.strip() or not self.family_id.strip():
            raise ValueError("search routes require non-empty route and family identities")
        object.__setattr__(self, "disposition", RouteDisposition(self.disposition))
        if self.disposition is RouteDisposition.COMPLETE and not self.source_ids:
            raise ValueError("complete search routes require at least one source identity")
        if self.disposition is RouteDisposition.CENSORED:
            if not self.censor_reason or not self.censor_reason.strip():
                raise ValueError("censored search routes require an explicit reason")
        elif self.censor_reason is not None:
            raise ValueError("only censored routes may carry a censor reason")


@dataclass(frozen=True, slots=True)
class SaturationPassReceipt:
    pass_id: str
    covered_family_ids: frozenset[str]
    full_declared_universe: bool
    changed_vocabulary: bool
    hostile_parent_search: bool
    material_findings: tuple[FindingKind, ...] = (FindingKind.NONE,)
    open_route_ids: tuple[str, ...] = ()
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if not self.pass_id.strip() or not self.covered_family_ids:
            raise ValueError("saturation passes require identity and covered families")
        findings = tuple(FindingKind(item) for item in self.material_findings)
        if not findings:
            findings = (FindingKind.NONE,)
        if FindingKind.NONE in findings and len(findings) > 1:
            raise ValueError("NONE cannot be combined with material finding kinds")
        object.__setattr__(self, "material_findings", findings)
        if self.authority_granted:
            raise ValueError("a saturation pass cannot grant field authority")

    @property
    def has_material_finding(self) -> bool:
        return any(item is not FindingKind.NONE for item in self.material_findings)


@dataclass(frozen=True, slots=True)
class FoundationSaturationAssessment:
    status: FoundationSaturationStatus
    open_family_ids: tuple[str, ...]
    open_route_ids: tuple[str, ...]
    censored_route_ids: tuple[str, ...]
    consecutive_no_material_passes: int
    required_no_material_passes: int
    latest_material_findings: tuple[FindingKind, ...]
    internal_synthesis_allowed: bool
    external_demarcation_ready: bool
    field_authority_granted: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", FoundationSaturationStatus(self.status))
        if self.consecutive_no_material_passes < 0:
            raise ValueError("pass count must be non-negative")
        if self.required_no_material_passes < 1:
            raise ValueError("at least one clean pass must be required")
        if self.field_authority_granted:
            raise ValueError("foundation assessment cannot grant field authority")
        if self.external_demarcation_ready and not self.internal_synthesis_allowed:
            raise ValueError("external demarcation requires internal synthesis readiness")


def _consecutive_clean_passes(
    passes: tuple[SaturationPassReceipt, ...],
    required_family_ids: frozenset[str],
) -> int:
    count = 0
    for receipt in reversed(passes):
        if (
            receipt.has_material_finding
            or receipt.open_route_ids
            or not receipt.full_declared_universe
            or not receipt.changed_vocabulary
            or not receipt.hostile_parent_search
            or not required_family_ids <= receipt.covered_family_ids
        ):
            break
        count += 1
    return count


def assess_foundation_saturation(
    required_family_ids: Iterable[str],
    routes: Iterable[SearchRouteReceipt],
    passes: Iterable[SaturationPassReceipt],
    *,
    external_review_complete: bool = False,
    required_clean_passes: int = REQUIRED_CLEAN_PASSES,
) -> FoundationSaturationAssessment:
    """Assess bounded foundation saturation without granting field authority.

    The canonical Wave-06 rule requires three consecutive full-universe,
    changed-vocabulary, hostile-parent passes after the latest material
    addition. Open routes or uncovered families block synthesis. Censored
    routes remain visible and are never converted into negative evidence.
    """

    if required_clean_passes < 1:
        raise ValueError("required_clean_passes must be positive")

    required = frozenset(item for item in required_family_ids if item.strip())
    route_tuple = tuple(routes)
    pass_tuple = tuple(passes)

    if not required or not route_tuple or not pass_tuple:
        return FoundationSaturationAssessment(
            FoundationSaturationStatus.CANNOT_CHECK,
            tuple(sorted(required)),
            tuple(
                sorted(
                    route.route_id
                    for route in route_tuple
                    if route.disposition is RouteDisposition.OPEN
                )
            ),
            tuple(
                sorted(
                    route.route_id
                    for route in route_tuple
                    if route.disposition is RouteDisposition.CENSORED
                )
            ),
            0,
            required_clean_passes,
            (),
            False,
            False,
        )

    route_ids = tuple(route.route_id for route in route_tuple)
    if len(route_ids) != len(set(route_ids)):
        raise ValueError("search route identities must be unique")
    pass_ids = tuple(receipt.pass_id for receipt in pass_tuple)
    if len(pass_ids) != len(set(pass_ids)):
        raise ValueError("saturation pass identities must be unique")

    completed_families = frozenset(
        route.family_id
        for route in route_tuple
        if route.disposition is RouteDisposition.COMPLETE
    )
    open_families = tuple(sorted(required - completed_families))
    declared_open_routes = {
        route.route_id
        for route in route_tuple
        if route.disposition is RouteDisposition.OPEN
    }
    declared_open_routes.update(pass_tuple[-1].open_route_ids)
    open_routes = tuple(sorted(declared_open_routes))
    censored_routes = tuple(
        sorted(
            route.route_id
            for route in route_tuple
            if route.disposition is RouteDisposition.CENSORED
        )
    )
    latest = pass_tuple[-1]
    latest_material = tuple(
        item for item in latest.material_findings if item is not FindingKind.NONE
    )
    clean_count = _consecutive_clean_passes(pass_tuple, required)

    if latest.has_material_finding:
        status = FoundationSaturationStatus.REOPENED_MATERIAL_FINDING
        internal_ready = False
        external_ready = False
    elif open_families or open_routes or clean_count < required_clean_passes:
        status = FoundationSaturationStatus.OPEN_COVERAGE
        internal_ready = False
        external_ready = False
    elif external_review_complete:
        status = FoundationSaturationStatus.READY_FOR_EXTERNAL_DEMARCATION
        internal_ready = True
        external_ready = True
    else:
        status = FoundationSaturationStatus.READY_FOR_INTERNAL_SYNTHESIS
        internal_ready = True
        external_ready = False

    return FoundationSaturationAssessment(
        status,
        open_families,
        open_routes,
        censored_routes,
        clean_count,
        required_clean_passes,
        latest_material,
        internal_ready,
        external_ready,
    )
