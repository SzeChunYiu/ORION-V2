"""Fail-closed scientificity gates for ORION-V2 claim promotion.

This module distinguishes inspiration, operational concepts, prospective results,
replication/cross-domain evidence, and foundation-proposition candidates. It
never grants field status, superiority, or journal acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ScientificityLevel(IntEnum):
    S0_INSPIRATION_OR_METAPHOR = 0
    S1_OPERATIONALLY_DEFINED_CONCEPT = 1
    S2_DISCRIMINATING_HYPOTHESIS = 2
    S3_PROSPECTIVELY_TESTED_RESULT = 3
    S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN = 4
    S5_FOUNDATION_PROPOSITION_CANDIDATE = 5


@dataclass(frozen=True, slots=True)
class ScientificityEvidence:
    level: ScientificityLevel
    preregistered_or_frozen: bool = False
    strongest_parent_compared: bool = False
    negative_control_present: bool = False
    independent_evaluation: bool = False
    cross_domain_or_replication: bool = False
    robustness_audit: bool = False
    critical_failure_open: bool = False


@dataclass(frozen=True, slots=True)
class ClaimPromotionDecision:
    allowed: bool
    maximum_level: ScientificityLevel
    reasons: tuple[str, ...]
    field_status_granted: bool = False
    superiority_granted: bool = False
    publication_readiness_granted: bool = False


def assess_claim_promotion(
    evidence: ScientificityEvidence,
    requested_level: ScientificityLevel,
) -> ClaimPromotionDecision:
    """Return the maximum defensible scientificity level for current evidence."""

    reasons: list[str] = []
    maximum = ScientificityLevel(evidence.level)

    if maximum >= ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT:
        if not evidence.preregistered_or_frozen:
            maximum = ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS
            reasons.append("confirmatory promotion requires a frozen/preregistered protocol")
        if not evidence.strongest_parent_compared:
            maximum = min(maximum, ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS)
            reasons.append("headline result requires strongest-parent comparison")
        if not evidence.negative_control_present:
            maximum = min(maximum, ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS)
            reasons.append("headline result requires a negative/simple control")
        if evidence.critical_failure_open:
            maximum = min(maximum, ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS)
            reasons.append("open critical failure blocks empirical promotion")

    if maximum >= ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN:
        if not evidence.independent_evaluation:
            maximum = ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT
            reasons.append("S4 requires independent evaluation")
        if not evidence.cross_domain_or_replication:
            maximum = min(maximum, ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT)
            reasons.append("S4 requires independent replication or material cross-domain evidence")
        if not evidence.robustness_audit:
            maximum = min(maximum, ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT)
            reasons.append("S4 requires robustness to reasonable analysis choices")

    if maximum >= ScientificityLevel.S5_FOUNDATION_PROPOSITION_CANDIDATE:
        if not (
            evidence.independent_evaluation
            and evidence.cross_domain_or_replication
            and evidence.robustness_audit
            and evidence.strongest_parent_compared
        ):
            maximum = ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN
            reasons.append("S5 requires independent cross-domain parent-aware evidence")

    requested = ScientificityLevel(requested_level)
    allowed = requested <= maximum
    if not allowed:
        reasons.append(f"requested {requested.name} exceeds maximum {maximum.name}")

    return ClaimPromotionDecision(
        allowed=allowed,
        maximum_level=maximum,
        reasons=tuple(dict.fromkeys(reasons)),
    )
