from __future__ import annotations
from dataclasses import dataclass
from typing import Hashable, Mapping
Distribution = Mapping[Hashable, float]

def _validated_distribution(distribution: Distribution) -> dict[Hashable, float]:
    if not distribution: raise ValueError("distribution must be non-empty")
    result = dict(distribution)
    if any(value < 0 for value in result.values()): raise ValueError("distribution weights must be non-negative")
    if abs(sum(result.values()) - 1.0) > 1e-9: raise ValueError("distribution weights must sum to 1")
    return result

def total_variation(left: Distribution, right: Distribution) -> float:
    left_valid = _validated_distribution(left); right_valid = _validated_distribution(right); support = set(left_valid) | set(right_valid)
    return 0.5 * sum(abs(left_valid.get(item, 0.0) - right_valid.get(item, 0.0)) for item in support)

@dataclass(frozen=True, slots=True)
class EvaluationDeployment:
    evaluation_id: str; policy_id: str; pre_distribution: Distribution; post_distribution: Distribution; metric_pre: float; metric_post: float; protected_outcome_pre: float | None = None; protected_outcome_post: float | None = None; intervention_or_natural_control_id: str = ""
    def __post_init__(self) -> None:
        if not self.evaluation_id.strip() or not self.policy_id.strip(): raise ValueError("evaluation and policy identities must be non-blank")
        _validated_distribution(self.pre_distribution); _validated_distribution(self.post_distribution)

@dataclass(frozen=True, slots=True)
class PerformativeAssessment:
    evaluation_id: str; distribution_shift: float; metric_delta: float; protected_outcome_delta: float | None; proxy_improves_protected_worsens: bool; causal_attribution_available: bool; terminal: str; grants_scientific_success: bool = False
    def __post_init__(self) -> None:
        if self.grants_scientific_success: raise ValueError("performative assessment cannot grant scientific success")

def assess_performative_evaluation(deployment: EvaluationDeployment, *, shift_tolerance: float = 0.0) -> PerformativeAssessment:
    if shift_tolerance < 0: raise ValueError("shift_tolerance must be non-negative")
    shift = total_variation(deployment.pre_distribution, deployment.post_distribution); metric_delta = deployment.metric_post - deployment.metric_pre; protected_delta = None; proxy_failure = False
    if deployment.protected_outcome_pre is not None and deployment.protected_outcome_post is not None:
        protected_delta = deployment.protected_outcome_post - deployment.protected_outcome_pre; proxy_failure = metric_delta > 0 and protected_delta < 0
    causal = bool(deployment.intervention_or_natural_control_id.strip())
    terminal = "PROXY_IMPROVES_PROTECTED_OUTCOME_WORSENS" if proxy_failure else "PERFORMATIVE_SHIFT_DETECTED_CAUSE_CANNOT_CHECK" if shift > shift_tolerance and not causal else "PERFORMATIVE_SHIFT_DETECTED_CONTROL_BOUND" if shift > shift_tolerance else "NO_MATERIAL_PERFORMATIVE_SHIFT_UNDER_BOUND"
    return PerformativeAssessment(deployment.evaluation_id, shift, metric_delta, protected_delta, proxy_failure, causal, terminal)
