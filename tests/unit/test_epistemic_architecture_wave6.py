import pytest

from orion_v2.epistemic_architecture import (
    CapabilityContext,
    EpistemicAction,
    FrontierEpisode,
    FrontierObstruction,
    FrontierRouteStatus,
    MachineConcept,
    MachineConceptRole,
    RegimeTransformScope,
    machine_concept_descriptor,
    route_frontier_action,
)
from orion_v2.jump import JumpLevel


def _context() -> CapabilityContext:
    return CapabilityContext(
        environment_ids=("env:finite-world",),
        task_family_ids=("tasks:frontier-diagnosis",),
        resource_regime_ids=("budget:matched",),
        system_boundary_ids=("boundary:research-system",),
        substrate_or_interface_ids=("substrate:machine",),
        timescale_ids=("timescale:episode",),
        criterion_ids=("criterion:justified-terminal",),
    )


def _episode(*, lower_levels: tuple[str, ...] = ("J0:insufficient", "J1:insufficient")) -> FrontierEpisode:
    obstruction = FrontierObstruction(
        obstruction_id="obstruction:representation",
        problem_id="problem:frontier",
        witness_ids=("witness:collision",),
        responsibility_hypothesis_ids=("responsibility:representation",),
        discriminator_ids=("probe:hidden-case",),
        lower_level_disposition_ids=lower_levels,
    )
    return FrontierEpisode(
        episode_id="episode:1",
        problem_id="problem:frontier",
        capability_context=_context(),
        obstruction=obstruction,
        admissible_actions=(
            EpistemicAction.LEARN,
            EpistemicAction.PROVE,
            EpistemicAction.CHANGE_REPRESENTATION,
            EpistemicAction.TRANSFORM_REGIME,
            EpistemicAction.ABSTAIN,
        ),
    )


def test_machine_x_terms_have_distinct_scientific_roles() -> None:
    assert machine_concept_descriptor(MachineConcept.MACHINE_LEARNING).role is MachineConceptRole.LEARNING_MECHANISM
    assert machine_concept_descriptor(MachineConcept.MACHINE_COGNITION).role is MachineConceptRole.COGNITIVE_ARCHITECTURE
    assert machine_concept_descriptor(MachineConcept.MACHINE_INTELLIGENCE).role is MachineConceptRole.CAPABILITY_PROFILE
    assert machine_concept_descriptor(MachineConcept.MACHINE_NATIVE_INTELLIGENCE).role is MachineConceptRole.DESIGN_ORIENTATION
    assert machine_concept_descriptor(MachineConcept.MACHINE_SCIENTIFIC_INTELLIGENCE).role is MachineConceptRole.SCIENTIFIC_CAPABILITY
    assert machine_concept_descriptor(MachineConcept.MACHINE_EPISTEMICS).role is MachineConceptRole.EPISTEMIC_CONTROL
    assert machine_concept_descriptor(MachineConcept.AI_FOR_SCIENCE).role is MachineConceptRole.APPLICATION_ECOSYSTEM


def test_capability_claim_requires_declared_locality_context() -> None:
    with pytest.raises(ValueError, match="timescale_ids must not be empty"):
        CapabilityContext(
            environment_ids=("env",),
            task_family_ids=("task",),
            resource_regime_ids=("resource",),
            system_boundary_ids=("boundary",),
            substrate_or_interface_ids=("substrate",),
            timescale_ids=(),
            criterion_ids=("criterion",),
        )


def test_learning_is_existing_control_not_automatic_jump() -> None:
    route = route_frontier_action(_episode(), EpistemicAction.LEARN)
    assert route.status is FrontierRouteStatus.EXISTING_CONTROL_ACTION
    assert route.jump_level is None
    assert route.superiority_authorized is False


def test_representation_change_routes_to_existing_jump_machinery() -> None:
    route = route_frontier_action(_episode(), EpistemicAction.CHANGE_REPRESENTATION)
    assert route.status is FrontierRouteStatus.JUMP_ASSESSMENT_REQUIRED
    assert route.jump_level is JumpLevel.REPRESENTATION_REGIME_TRANSITION
    assert route.scientific_truth_authorized is False


def test_transform_regime_requires_scope_and_maps_to_minimum_relevant_level() -> None:
    episode = _episode()
    with pytest.raises(ValueError, match="explicit transform_scope"):
        route_frontier_action(episode, EpistemicAction.TRANSFORM_REGIME)

    route = route_frontier_action(
        episode,
        EpistemicAction.TRANSFORM_REGIME,
        transform_scope=RegimeTransformScope.TOOL_OR_INSTRUMENT,
    )
    assert route.status is FrontierRouteStatus.JUMP_ASSESSMENT_REQUIRED
    assert route.jump_level is JumpLevel.METHOD_TOOL_INSTRUMENT_INVENTION


def test_frontier_transformation_is_blocked_before_lower_level_disposition() -> None:
    route = route_frontier_action(
        _episode(lower_levels=()),
        EpistemicAction.CHANGE_REPRESENTATION,
    )
    assert route.status is FrontierRouteStatus.BLOCKED_LOWER_LEVEL_UNRESOLVED


def test_abstention_is_a_valid_frontier_terminal_action() -> None:
    route = route_frontier_action(_episode(), EpistemicAction.ABSTAIN)
    assert route.status is FrontierRouteStatus.SAFE_ABSTAIN
    assert route.jump_level is None
