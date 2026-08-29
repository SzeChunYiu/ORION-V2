"""Source-adapter contract for population-scale scientific-development corpora.

Acquisition is deliberately out of scope here. Lawful source-specific adapters emit
source-bound observations; this module assembles them into development episodes only
when trajectory identity and outcome witnesses are explicit. Citation, fame and
other proxy metrics never determine the scientific outcome class.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from .scientific_development import DevelopmentOutcomeClass, DevelopmentStep, ScientificDevelopmentEpisode


def _unique(values: Iterable[str], name: str) -> tuple[str, ...]:
    result = tuple(values)
    if any(not x.strip() for x in result):
        raise ValueError(f"{name} may not contain blanks")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} must be unique")
    return result


class ObservationKind(StrEnum):
    PROBLEM_FRAME = "PROBLEM_FRAME"
    HYPOTHESIS_OR_CONJECTURE = "HYPOTHESIS_OR_CONJECTURE"
    METHOD_OR_REPRESENTATION = "METHOD_OR_REPRESENTATION"
    EXPERIMENT_OR_COMPUTATION = "EXPERIMENT_OR_COMPUTATION"
    FORMAL_RESULT = "FORMAL_RESULT"
    DATA_OR_INSTRUMENT = "DATA_OR_INSTRUMENT"
    VERSION_OR_REVISION = "VERSION_OR_REVISION"
    REPLICATION = "REPLICATION"
    CORRECTION = "CORRECTION"
    RETRACTION = "RETRACTION"
    ABANDONMENT = "ABANDONMENT"
    OTHER = "OTHER"


@dataclass(frozen=True, slots=True)
class DevelopmentObservation:
    observation_id: str
    trajectory_id: str
    domain_id: str
    epoch_id: str
    source_mode_id: str
    ordinal: int
    kind: ObservationKind
    action_feature_ids: tuple[str, ...]
    result_feature_ids: tuple[str, ...] = ()
    failure_feature_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    validation_ids: tuple[str, ...] = ()
    institution_ids: tuple[str, ...] = ()
    team_id: str = ""
    proxy_metrics: tuple[tuple[str, float], ...] = ()
    bias_flag_ids: tuple[str, ...] = ()
    resource_cost: float = 0.0

    def __post_init__(self) -> None:
        for value in (self.observation_id, self.trajectory_id, self.domain_id, self.epoch_id, self.source_mode_id):
            if not value.strip():
                raise ValueError("observation identities may not be blank")
        object.__setattr__(self, "kind", ObservationKind(self.kind))
        if self.ordinal < 0 or self.resource_cost < 0:
            raise ValueError("ordinal/resource cost must be non-negative")
        if not self.action_feature_ids:
            raise ValueError("observations require action features")
        for name in ("action_feature_ids", "result_feature_ids", "failure_feature_ids", "source_ids", "validation_ids", "institution_ids", "bias_flag_ids"):
            object.__setattr__(self, name, _unique(getattr(self, name), name))
        metric_names = [name for name, _ in self.proxy_metrics]
        if len(metric_names) != len(set(metric_names)) or any(not name.strip() for name in metric_names):
            raise ValueError("proxy metric names must be nonblank and unique")


@dataclass(frozen=True, slots=True)
class OutcomeBinding:
    trajectory_id: str
    outcome_class: DevelopmentOutcomeClass
    witness_ids: tuple[str, ...]
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.trajectory_id.strip():
            raise ValueError("trajectory_id required")
        object.__setattr__(self, "outcome_class", DevelopmentOutcomeClass(self.outcome_class))
        object.__setattr__(self, "witness_ids", _unique(self.witness_ids, "witness_ids"))
        object.__setattr__(self, "source_ids", _unique(self.source_ids, "source_ids"))
        if self.outcome_class in {DevelopmentOutcomeClass.VALIDATED_SUCCESS, DevelopmentOutcomeClass.VALIDATED_FAILURE} and not self.witness_ids:
            raise ValueError("validated outcome classes require witnesses")


def assemble_episode(observations: Iterable[DevelopmentObservation], binding: OutcomeBinding | None = None) -> ScientificDevelopmentEpisode:
    values = tuple(sorted(observations, key=lambda x: (x.ordinal, x.observation_id)))
    if not values:
        raise ValueError("episode requires observations")
    trajectories = {x.trajectory_id for x in values}
    domains = {x.domain_id for x in values}
    epochs = {x.epoch_id for x in values}
    if len(trajectories) != 1 or len(domains) != 1 or len(epochs) != 1:
        raise ValueError("one episode cannot silently merge trajectory/domain/epoch identities")
    trajectory_id = next(iter(trajectories))
    if binding is not None and binding.trajectory_id != trajectory_id:
        raise ValueError("outcome binding targets another trajectory")
    outcome = binding.outcome_class if binding else DevelopmentOutcomeClass.UNKNOWN
    witnesses = binding.witness_ids if binding else ()
    steps = tuple(
        DevelopmentStep(
            step_id=x.observation_id,
            ordinal=i,
            state_feature_ids=(f"KIND:{x.kind.value}",),
            action_feature_ids=x.action_feature_ids,
            result_feature_ids=x.result_feature_ids,
            failure_feature_ids=x.failure_feature_ids,
            source_ids=x.source_ids,
            validation_ids=x.validation_ids,
            resource_cost=x.resource_cost,
        )
        for i, x in enumerate(values)
    )
    proxy = {f"{x.observation_id}:{name}": value for x in values for name, value in x.proxy_metrics}
    team_ids = {x.team_id for x in values if x.team_id}
    return ScientificDevelopmentEpisode(
        episode_id=trajectory_id,
        domain_id=next(iter(domains)),
        epoch_id=next(iter(epochs)),
        outcome_class=outcome,
        steps=steps,
        source_mode_ids=tuple(sorted({x.source_mode_id for x in values})),
        team_id=next(iter(team_ids)) if len(team_ids) == 1 else "",
        institution_ids=tuple(sorted({i for x in values for i in x.institution_ids})),
        outcome_witness_ids=witnesses,
        proxy_metrics=tuple(sorted(proxy.items())),
        bias_flag_ids=tuple(sorted({b for x in values for b in x.bias_flag_ids})),
    )


def assemble_all(observations: Iterable[DevelopmentObservation], bindings: Iterable[OutcomeBinding] = ()) -> tuple[ScientificDevelopmentEpisode, ...]:
    groups: dict[str, list[DevelopmentObservation]] = {}
    for item in observations:
        groups.setdefault(item.trajectory_id, []).append(item)
    binding_values = tuple(bindings)
    binding_map = {item.trajectory_id: item for item in binding_values}
    if len(binding_map) != len(binding_values):
        raise ValueError("duplicate outcome binding for trajectory")
    return tuple(assemble_episode(groups[key], binding_map.get(key)) for key in sorted(groups))
