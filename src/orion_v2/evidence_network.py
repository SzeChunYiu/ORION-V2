from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceNetworkStatus(str, Enum):
    INDEPENDENCE_SUPPORTED = "INDEPENDENCE_SUPPORTED"
    DEPENDENCE_ADJUSTED = "DEPENDENCE_ADJUSTED"
    CONTRADICTORY_EVIDENCE = "CONTRADICTORY_EVIDENCE"
    DEPENDENCE_UNIDENTIFIED = "DEPENDENCE_UNIDENTIFIED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    evidence_id: str
    direction: int
    weight: float
    authority_ceiling: int

    def __post_init__(self) -> None:
        if not self.evidence_id.strip() or self.direction not in {-1, 0, 1}:
            raise ValueError(
                "evidence requires a non-blank id and direction -1/0/1"
            )
        if self.weight < 0 or self.authority_ceiling < 0:
            raise ValueError(
                "weight and authority ceiling must be non-negative"
            )


@dataclass(frozen=True, slots=True)
class DependenceCluster:
    cluster_id: str
    member_ids: tuple[str, ...]
    intracluster_correlation: float | None
    basis_id: str = ""

    def __post_init__(self) -> None:
        if not self.cluster_id.strip() or not self.member_ids:
            raise ValueError(
                "dependence cluster identity and members are required"
            )
        if len(set(self.member_ids)) != len(self.member_ids):
            raise ValueError("cluster members must be unique")
        if (
            self.intracluster_correlation is not None
            and not 0 <= self.intracluster_correlation <= 1
        ):
            raise ValueError(
                "intracluster correlation must lie in [0,1]"
            )


@dataclass(frozen=True, slots=True)
class EvidenceNetworkAssessment:
    status: EvidenceNetworkStatus
    naive_count: int
    effective_count: float | None
    naive_signed_support: float
    adjusted_signed_support: float | None
    authority_ceiling: int
    warnings: tuple[str, ...] = ()
    grants_truth: bool = False

    def __post_init__(self) -> None:
        if self.grants_truth:
            raise ValueError("evidence-network assessment cannot grant truth")


def assess_evidence_network(
    items: tuple[EvidenceItem, ...],
    clusters: tuple[DependenceCluster, ...],
) -> EvidenceNetworkAssessment:
    if not items:
        return EvidenceNetworkAssessment(
            EvidenceNetworkStatus.CANNOT_CHECK, 0, None, 0.0, None, 0
        )
    item_by_id = {item.evidence_id: item for item in items}
    if len(item_by_id) != len(items):
        raise ValueError("evidence identities must be unique")
    seen: set[str] = set()
    for cluster in clusters:
        if not set(cluster.member_ids) <= set(item_by_id):
            return EvidenceNetworkAssessment(
                EvidenceNetworkStatus.CANNOT_CHECK,
                len(items),
                None,
                sum(item.direction * item.weight for item in items),
                None,
                min(item.authority_ceiling for item in items),
                (
                    f"cluster {cluster.cluster_id} references unknown evidence",
                ),
            )
        if seen & set(cluster.member_ids):
            return EvidenceNetworkAssessment(
                EvidenceNetworkStatus.CANNOT_CHECK,
                len(items),
                None,
                sum(item.direction * item.weight for item in items),
                None,
                min(item.authority_ceiling for item in items),
                (
                    "overlapping dependence clusters require a richer covariance model",
                ),
            )
        seen.update(cluster.member_ids)
    if any(
        cluster.intracluster_correlation is None for cluster in clusters
    ):
        return EvidenceNetworkAssessment(
            EvidenceNetworkStatus.DEPENDENCE_UNIDENTIFIED,
            len(items),
            None,
            sum(item.direction * item.weight for item in items),
            None,
            min(item.authority_ceiling for item in items),
        )

    effective_count = float(len(items) - len(seen))
    adjusted_support = sum(
        item.direction * item.weight
        for item in items
        if item.evidence_id not in seen
    )
    for cluster in clusters:
        rho = float(cluster.intracluster_correlation)
        size = len(cluster.member_ids)
        design_effect = 1.0 + (size - 1) * rho
        effective_count += size / design_effect
        adjusted_support += (
            sum(
                item_by_id[item_id].direction
                * item_by_id[item_id].weight
                for item_id in cluster.member_ids
            )
            / design_effect
        )

    directions = {item.direction for item in items if item.direction}
    status = (
        EvidenceNetworkStatus.CONTRADICTORY_EVIDENCE
        if directions == {-1, 1}
        else EvidenceNetworkStatus.DEPENDENCE_ADJUSTED
        if clusters
        else EvidenceNetworkStatus.INDEPENDENCE_SUPPORTED
    )
    return EvidenceNetworkAssessment(
        status,
        len(items),
        effective_count,
        sum(item.direction * item.weight for item in items),
        adjusted_support,
        min(item.authority_ceiling for item in items),
    )
