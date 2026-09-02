"""Research-only ontic/epistemic boundary semantics.

This module separates the external target/world from the observation channel,
the machine's epistemic/scientific state, and the machine's generative regime.
It does not model the world as a machine and it does not grant privileged access
to an objective world state.

The primary engineering use is discrepancy-locus diagnosis: before a research
system changes a model, representation, problem, evaluator, tool, workflow, or
scientific claim, it should keep distinct hypotheses that the relevant
discrepancy originates in the target, observation/measurement channel, current
epistemic model, representation/generative regime, registered problem/criterion,
evaluator/validation contract, or research process/tool/workflow.

The module is intentionally not re-exported from :mod:`orion_v2.kernel`.
Receipts and action suggestions are non-authorizing: they can make a diagnosis
inspectable and route a candidate action family, but cannot establish scientific
truth, target-world change, novelty, framework adoption, or field status.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from .epistemic_architecture import EpistemicAction


def _ids(values: Iterable[str], *, name: str, allow_empty: bool = False) -> tuple[str, ...]:
    result = tuple(values)
    if not allow_empty and not result:
        raise ValueError(f"{name} must not be empty")
    if any(not value.strip() for value in result):
        raise ValueError(f"{name} may not contain blank identities")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} identities must be unique")
    return result


class DiscrepancyLocus(StrEnum):
    """Candidate locus responsible for a witnessed scientific discrepancy.

    The set is an operational responsibility interface rather than a claim that
    all scientific error admits one universal partition. More than one locus
    may remain live, and domain-native reconstruction can contract or refine a
    locus before protected use.
    """

    TARGET_WORLD = "TARGET_WORLD"
    OBSERVATION_MEASUREMENT = "OBSERVATION_MEASUREMENT"
    EPISTEMIC_MODEL = "EPISTEMIC_MODEL"
    REPRESENTATION_REGIME = "REPRESENTATION_REGIME"
    PROBLEM_CRITERION = "PROBLEM_CRITERION"
    EVALUATOR_VALIDATION = "EVALUATOR_VALIDATION"
    PROCESS_TOOL_WORKFLOW = "PROCESS_TOOL_WORKFLOW"


class LocusDiagnosisStatus(StrEnum):
    NO_DISCREPANCY_WITNESSED = "NO_DISCREPANCY_WITNESSED"
    ACTIONABLE_LOCUS_HYPOTHESIS = "ACTIONABLE_LOCUS_HYPOTHESIS"
    MULTIPLE_LIVE_LOCUS_HYPOTHESES = "MULTIPLE_LIVE_LOCUS_HYPOTHESES"
    CANNOT_IDENTIFY = "CANNOT_IDENTIFY"


@dataclass(frozen=True, slots=True)
class WorldObservationBoundary:
    """Registered interface between a target and the observations available to inquiry.

    ``target_id`` identifies the scientific referent. It is not an assertion
    that the machine has direct access to the target's objective state.
    """

    boundary_id: str
    target_id: str
    observation_channel_ids: tuple[str, ...]
    instrument_or_interface_ids: tuple[str, ...]
    context_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.boundary_id.strip() or not self.target_id.strip():
            raise ValueError("world/observation boundaries require bound identities")
        for name in (
            "observation_channel_ids",
            "instrument_or_interface_ids",
            "context_ids",
        ):
            object.__setattr__(self, name, _ids(getattr(self, name), name=name))


@dataclass(frozen=True, slots=True)
class OnticEpistemicDelta:
    """Registered case-level distinction between different kinds of change.

    This object is intended for known-answer fixtures, adjudicated episodes, or
    explicit scientific records. It is not a hidden oracle available to the
    acting machine. ``target_changed`` may therefore be ``None`` when target
    change is not independently established.
    """

    transition_id: str
    target_changed: bool | None
    observation_channel_changed: bool | None
    epistemic_state_changed: bool
    generative_regime_changed: bool
    process_or_tool_changed: bool

    def __post_init__(self) -> None:
        if not self.transition_id.strip():
            raise ValueError("ontic/epistemic deltas require an identity")


@dataclass(frozen=True, slots=True)
class LocusHypothesis:
    hypothesis_id: str
    locus: DiscrepancyLocus
    witness_ids: tuple[str, ...]
    discriminator_ids: tuple[str, ...]
    falsifier_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip():
            raise ValueError("locus hypotheses require an identity")
        object.__setattr__(self, "locus", DiscrepancyLocus(self.locus))
        for name in ("witness_ids", "discriminator_ids", "falsifier_ids"):
            object.__setattr__(self, name, _ids(getattr(self, name), name=name))


@dataclass(frozen=True, slots=True)
class LocusDiagnosisEvidence:
    """Evidence disposition for responsibility hypotheses.

    ``diagnostic_evaluator_adequate`` refers to the evaluator used to
    discriminate *among locus hypotheses*. It is deliberately distinct from a
    scientific evaluator/oracle that may itself be under diagnosis through the
    ``EVALUATOR_VALIDATION`` locus.
    """

    discrepancy_witness_ids: tuple[str, ...]
    supported_hypothesis_ids: tuple[str, ...] = ()
    defeated_hypothesis_ids: tuple[str, ...] = ()
    unresolved_hypothesis_ids: tuple[str, ...] = ()
    diagnostic_evaluator_adequate: bool | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "discrepancy_witness_ids",
            _ids(self.discrepancy_witness_ids, name="discrepancy_witness_ids", allow_empty=True),
        )
        for name in (
            "supported_hypothesis_ids",
            "defeated_hypothesis_ids",
            "unresolved_hypothesis_ids",
        ):
            object.__setattr__(self, name, _ids(getattr(self, name), name=name, allow_empty=True))
        groups = (
            set(self.supported_hypothesis_ids),
            set(self.defeated_hypothesis_ids),
            set(self.unresolved_hypothesis_ids),
        )
        if any(groups[i] & groups[j] for i in range(3) for j in range(i + 1, 3)):
            raise ValueError("a locus hypothesis cannot have conflicting evidence dispositions")


_LOCUS_CANDIDATE_ACTIONS: dict[DiscrepancyLocus, tuple[EpistemicAction, ...]] = {
    DiscrepancyLocus.TARGET_WORLD: (
        EpistemicAction.MEASURE,
        EpistemicAction.EXPERIMENT,
        EpistemicAction.CHALLENGE,
    ),
    DiscrepancyLocus.OBSERVATION_MEASUREMENT: (
        EpistemicAction.MEASURE,
        EpistemicAction.CHALLENGE,
        EpistemicAction.BUILD_TOOL,
    ),
    DiscrepancyLocus.EPISTEMIC_MODEL: (
        EpistemicAction.CHALLENGE,
        EpistemicAction.EXPERIMENT,
        EpistemicAction.CHANGE_MODEL,
    ),
    DiscrepancyLocus.REPRESENTATION_REGIME: (
        EpistemicAction.CHALLENGE,
        EpistemicAction.CHANGE_REPRESENTATION,
        EpistemicAction.TRANSFORM_REGIME,
    ),
    DiscrepancyLocus.PROBLEM_CRITERION: (
        EpistemicAction.CHALLENGE,
        EpistemicAction.REFORMULATE_PROBLEM,
    ),
    DiscrepancyLocus.EVALUATOR_VALIDATION: (
        EpistemicAction.CHALLENGE,
        EpistemicAction.BUILD_TOOL,
        EpistemicAction.CHANGE_WORKFLOW,
    ),
    DiscrepancyLocus.PROCESS_TOOL_WORKFLOW: (
        EpistemicAction.CHALLENGE,
        EpistemicAction.BUILD_TOOL,
        EpistemicAction.CHANGE_WORKFLOW,
    ),
}


@dataclass(frozen=True, slots=True)
class LocusDiagnosisReceipt:
    status: LocusDiagnosisStatus
    live_hypothesis_ids: tuple[str, ...]
    live_loci: tuple[DiscrepancyLocus, ...]
    candidate_actions: tuple[EpistemicAction, ...]
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    target_change_authorized: bool = False
    action_adoption_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", LocusDiagnosisStatus(self.status))
        object.__setattr__(
            self,
            "live_hypothesis_ids",
            _ids(self.live_hypothesis_ids, name="live_hypothesis_ids", allow_empty=True),
        )
        loci = tuple(DiscrepancyLocus(value) for value in self.live_loci)
        if len(loci) != len(set(loci)):
            raise ValueError("live_loci must be unique")
        object.__setattr__(self, "live_loci", loci)
        actions = tuple(EpistemicAction(value) for value in self.candidate_actions)
        if len(actions) != len(set(actions)):
            raise ValueError("candidate_actions must be unique")
        object.__setattr__(self, "candidate_actions", actions)
        if not self.reasons or any(not reason.strip() for reason in self.reasons):
            raise ValueError("locus diagnosis receipts require reasons")
        if (
            self.scientific_truth_authorized
            or self.target_change_authorized
            or self.action_adoption_authorized
        ):
            raise ValueError("locus diagnosis receipts are non-authorizing")


def _candidate_actions(loci: Iterable[DiscrepancyLocus]) -> tuple[EpistemicAction, ...]:
    ordered: list[EpistemicAction] = []
    for locus in loci:
        for action in _LOCUS_CANDIDATE_ACTIONS[locus]:
            if action not in ordered:
                ordered.append(action)
    return tuple(ordered)


def assess_discrepancy_locus(
    hypotheses: tuple[LocusHypothesis, ...],
    evidence: LocusDiagnosisEvidence,
) -> LocusDiagnosisReceipt:
    """Assess which discrepancy loci remain live without converting diagnosis to truth.

    An actionable locus requires a witnessed discrepancy, an adequate diagnostic
    evaluator, exactly one supported hypothesis, and explicit defeat of every
    registered alternative. Otherwise the result remains plural or
    ``CANNOT_IDENTIFY``. Returned actions are candidate families only;
    higher-level changes must still pass the existing frontier/Jump machinery.
    """

    if not hypotheses:
        raise ValueError("at least one registered locus hypothesis is required")
    ids = tuple(item.hypothesis_id for item in hypotheses)
    if len(ids) != len(set(ids)):
        raise ValueError("locus hypothesis identities must be unique")
    registered = set(ids)
    dispositioned = (
        set(evidence.supported_hypothesis_ids)
        | set(evidence.defeated_hypothesis_ids)
        | set(evidence.unresolved_hypothesis_ids)
    )
    unknown = dispositioned - registered
    if unknown:
        raise ValueError(f"evidence references unregistered locus hypotheses: {sorted(unknown)}")

    if not evidence.discrepancy_witness_ids:
        return LocusDiagnosisReceipt(
            LocusDiagnosisStatus.NO_DISCREPANCY_WITNESSED,
            (),
            (),
            (),
            ("no registered discrepancy witness licenses a responsibility diagnosis",),
        )

    if evidence.diagnostic_evaluator_adequate is not True:
        live = tuple(item for item in hypotheses if item.hypothesis_id not in evidence.defeated_hypothesis_ids)
        loci = tuple(dict.fromkeys(item.locus for item in live))
        return LocusDiagnosisReceipt(
            LocusDiagnosisStatus.CANNOT_IDENTIFY,
            tuple(item.hypothesis_id for item in live),
            loci,
            _candidate_actions(loci),
            ("the registered diagnostic evaluator cannot establish the responsibility distinction",),
        )

    supported = tuple(item for item in hypotheses if item.hypothesis_id in evidence.supported_hypothesis_ids)
    unresolved = tuple(
        item
        for item in hypotheses
        if item.hypothesis_id in evidence.unresolved_hypothesis_ids
        or item.hypothesis_id not in dispositioned
    )

    if len(supported) == 1 and not unresolved and len(evidence.defeated_hypothesis_ids) == len(hypotheses) - 1:
        winner = supported[0]
        return LocusDiagnosisReceipt(
            LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS,
            (winner.hypothesis_id,),
            (winner.locus,),
            _candidate_actions((winner.locus,)),
            ("one registered locus remains supported after explicit discrimination of all alternatives",),
        )

    live = supported + tuple(item for item in unresolved if item not in supported)
    loci = tuple(dict.fromkeys(item.locus for item in live))
    if len(live) > 1:
        return LocusDiagnosisReceipt(
            LocusDiagnosisStatus.MULTIPLE_LIVE_LOCUS_HYPOTHESES,
            tuple(item.hypothesis_id for item in live),
            loci,
            _candidate_actions(loci),
            ("multiple responsibility hypotheses remain live; escalation must not pretend the locus is identified",),
        )

    return LocusDiagnosisReceipt(
        LocusDiagnosisStatus.CANNOT_IDENTIFY,
        tuple(item.hypothesis_id for item in live),
        loci,
        _candidate_actions(loci),
        ("the registered evidence does not identify a unique discrepancy locus",),
    )
