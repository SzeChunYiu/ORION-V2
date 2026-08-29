"""Reference semantics for comparing a candidate higher-order theory with its
strongest parent federation.

The objects in this module are research/evaluation fixtures. They deliberately
do not grant scientific truth, field status, architecture authority, novelty or
publication readiness.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Mapping


class TheoryDisposition(str, Enum):
    ABSORPTIVE_SUPERTHEORY_CANDIDATE = "ABSORPTIVE_SUPERTHEORY_CANDIDATE"
    INTEGRATIVE_THEORY_ADVANCE = "INTEGRATIVE_THEORY_ADVANCE"
    ENGINEERING_EFFICIENCY_ADVANCE = "ENGINEERING_EFFICIENCY_ADVANCE"
    FEDERATED_PARENT_EQUIVALENT = "FEDERATED_PARENT_EQUIVALENT"
    PARENT_COMPOSITION_SUFFICIENT = "PARENT_COMPOSITION_SUFFICIENT"
    OVERGENERALIZED_THEORY = "OVERGENERALIZED_THEORY"
    REDUNDANT_DRAG = "REDUNDANT_DRAG"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class TheoryProfile:
    """Frozen profile for one candidate under one evaluation contract.

    Quality coordinates are oriented so that larger values are better. Cost
    coordinates are non-negative and smaller is better. The values may be
    normalized scores, rates, or bounded utilities, but the two profiles being
    compared must use exactly the same coordinate identities and semantics.
    """

    theory_id: str
    native_fidelity: float
    quality: Mapping[str, float]
    costs: Mapping[str, float]
    generativity: float = 0.0
    integration: float = 0.0
    cross_domain_count: int = 0
    independent_evaluation: bool = False
    local_parent_deference: bool = False
    critical_failures: frozenset[str] = frozenset()
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if not self.theory_id.strip():
            raise ValueError("theory profiles require a non-empty identity")
        if not 0.0 <= self.native_fidelity <= 1.0:
            raise ValueError("native fidelity must lie in [0, 1]")
        if not self.quality or not self.costs:
            raise ValueError("theory profiles require quality and cost coordinates")
        for key, value in self.quality.items():
            if not str(key).strip() or not isfinite(float(value)):
                raise ValueError("quality coordinates require identities and finite values")
        for key, value in self.costs.items():
            if not str(key).strip() or not isfinite(float(value)) or float(value) < 0:
                raise ValueError("cost coordinates require identities and non-negative finite values")
        if not isfinite(self.generativity) or self.generativity < 0:
            raise ValueError("generativity must be a non-negative finite value")
        if not isfinite(self.integration) or self.integration < 0:
            raise ValueError("integration must be a non-negative finite value")
        if self.cross_domain_count < 0:
            raise ValueError("cross-domain count must be non-negative")
        if self.authority_granted:
            raise ValueError("a theory profile cannot grant field or scientific authority")


@dataclass(frozen=True, slots=True)
class TheoryDominanceAssessment:
    disposition: TheoryDisposition
    quality_gains: tuple[str, ...]
    quality_regressions: tuple[str, ...]
    cost_gains: tuple[str, ...]
    cost_regressions: tuple[str, ...]
    hard_failure_ids: tuple[str, ...]
    candidate_dominates: bool
    strict_scientific_gain: bool
    authority_granted: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "disposition", TheoryDisposition(self.disposition))
        if self.authority_granted:
            raise ValueError("a dominance assessment cannot grant authority")
        if self.candidate_dominates and (
            self.quality_regressions or self.cost_regressions or self.hard_failure_ids
        ):
            raise ValueError("a dominating candidate cannot carry registered regressions")


def assess_theory_dominance(
    candidate: TheoryProfile,
    parent_federation: TheoryProfile,
    *,
    tolerance: float = 1e-9,
    minimum_cross_domains: int = 2,
) -> TheoryDominanceAssessment:
    """Compare a candidate theory with its strongest parent federation.

    The assessment is deliberately conservative:

    * critical failures and parent-native fidelity regressions are
      non-compensatory;
    * quality and cost coordinate sets must match exactly;
    * an absorptive-supertheory candidate must be no worse on every declared
      quality and cost coordinate, show a strict scientific/integrative gain,
      have independent evaluation, cover multiple domains, and defer locally
      to a sufficient parent;
    * no result grants field, truth, novelty or publication authority.
    """

    if tolerance < 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be a non-negative finite value")
    if minimum_cross_domains < 1:
        raise ValueError("minimum_cross_domains must be positive")

    candidate_quality = set(candidate.quality)
    parent_quality = set(parent_federation.quality)
    candidate_costs = set(candidate.costs)
    parent_costs = set(parent_federation.costs)

    if candidate_quality != parent_quality or candidate_costs != parent_costs:
        return TheoryDominanceAssessment(
            TheoryDisposition.CANNOT_CHECK,
            (),
            (),
            (),
            (),
            (),
            False,
            False,
        )

    quality_gains = tuple(
        sorted(
            key
            for key in candidate_quality
            if float(candidate.quality[key])
            > float(parent_federation.quality[key]) + tolerance
        )
    )
    quality_regressions = tuple(
        sorted(
            key
            for key in candidate_quality
            if float(candidate.quality[key]) + tolerance
            < float(parent_federation.quality[key])
        )
    )
    cost_gains = tuple(
        sorted(
            key
            for key in candidate_costs
            if float(candidate.costs[key]) + tolerance
            < float(parent_federation.costs[key])
        )
    )
    cost_regressions = tuple(
        sorted(
            key
            for key in candidate_costs
            if float(candidate.costs[key])
            > float(parent_federation.costs[key]) + tolerance
        )
    )
    hard_failures = tuple(sorted(candidate.critical_failures))

    fidelity_regression = (
        candidate.native_fidelity + tolerance < parent_federation.native_fidelity
    )
    if hard_failures or fidelity_regression:
        failures = hard_failures + (("NATIVE_FIDELITY_REGRESSION",) if fidelity_regression else ())
        return TheoryDominanceAssessment(
            TheoryDisposition.OVERGENERALIZED_THEORY,
            quality_gains,
            quality_regressions,
            cost_gains,
            cost_regressions,
            failures,
            False,
            bool(quality_gains),
        )

    if quality_regressions:
        return TheoryDominanceAssessment(
            TheoryDisposition.PARENT_COMPOSITION_SUFFICIENT,
            quality_gains,
            quality_regressions,
            cost_gains,
            cost_regressions,
            (),
            False,
            bool(quality_gains),
        )

    generative_gain = (
        candidate.generativity > parent_federation.generativity + tolerance
    )
    integrative_gain = candidate.integration > parent_federation.integration + tolerance
    strict_scientific_gain = bool(quality_gains) or generative_gain or integrative_gain

    if not strict_scientific_gain:
        if cost_regressions:
            return TheoryDominanceAssessment(
                TheoryDisposition.REDUNDANT_DRAG,
                quality_gains,
                quality_regressions,
                cost_gains,
                cost_regressions,
                (),
                False,
                False,
            )
        if cost_gains:
            return TheoryDominanceAssessment(
                TheoryDisposition.ENGINEERING_EFFICIENCY_ADVANCE,
                quality_gains,
                quality_regressions,
                cost_gains,
                cost_regressions,
                (),
                True,
                False,
            )
        return TheoryDominanceAssessment(
            TheoryDisposition.FEDERATED_PARENT_EQUIVALENT,
            (),
            (),
            (),
            (),
            (),
            True,
            False,
        )

    no_registered_regression = not cost_regressions
    candidate_dominates = no_registered_regression
    earns_absorptive_candidate = all(
        (
            candidate_dominates,
            generative_gain or integrative_gain,
            candidate.cross_domain_count >= minimum_cross_domains,
            candidate.independent_evaluation,
            candidate.local_parent_deference,
        )
    )

    disposition = (
        TheoryDisposition.ABSORPTIVE_SUPERTHEORY_CANDIDATE
        if earns_absorptive_candidate
        else TheoryDisposition.INTEGRATIVE_THEORY_ADVANCE
    )
    return TheoryDominanceAssessment(
        disposition,
        quality_gains,
        (),
        cost_gains,
        cost_regressions,
        (),
        candidate_dominates,
        True,
    )
