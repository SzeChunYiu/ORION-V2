import pytest

from orion_v2.scientific_development import DevelopmentOutcomeClass
from orion_v2.scientific_development_sources import (
    DevelopmentObservation,
    ObservationKind,
    OutcomeBinding,
    assemble_all,
    assemble_episode,
)


def obs(i, *, traj="t1", source_mode="papers", proxy=()):
    return DevelopmentObservation(
        observation_id=f"o{i}", trajectory_id=traj, domain_id="math", epoch_id="2020s",
        source_mode_id=source_mode, ordinal=i, kind=ObservationKind.METHOD_OR_REPRESENTATION,
        action_feature_ids=(f"a{i}",), result_feature_ids=(f"r{i}",), source_ids=(f"s{i}",),
        proxy_metrics=proxy,
    )


def test_unbound_trajectory_is_unknown_not_success():
    ep = assemble_episode((obs(0), obs(1)))
    assert ep.outcome_class is DevelopmentOutcomeClass.UNKNOWN
    assert ep.outcome_witness_ids == ()


def test_validated_outcome_requires_witness():
    with pytest.raises(ValueError):
        OutcomeBinding("t1", DevelopmentOutcomeClass.VALIDATED_SUCCESS, ())


def test_bound_success_preserves_proxy_without_using_proxy_as_label():
    bind = OutcomeBinding("t1", DevelopmentOutcomeClass.VALIDATED_SUCCESS, ("replication-witness",))
    ep = assemble_episode((obs(0, proxy=(("citations", 9999.0),)), obs(1)), bind)
    assert ep.outcome_class is DevelopmentOutcomeClass.VALIDATED_SUCCESS
    assert ep.outcome_witness_ids == ("replication-witness",)
    assert ("o0:citations", 9999.0) in ep.proxy_metrics


def test_trajectory_domain_epoch_cannot_be_silently_merged():
    other = DevelopmentObservation(
        observation_id="o2", trajectory_id="t1", domain_id="physics", epoch_id="2020s",
        source_mode_id="papers", ordinal=2, kind=ObservationKind.OTHER, action_feature_ids=("x",),
    )
    with pytest.raises(ValueError):
        assemble_episode((obs(0), other))


def test_all_groups_multiple_source_modes_and_explicit_bindings():
    bindings = (OutcomeBinding("t1", DevelopmentOutcomeClass.VALIDATED_FAILURE, ("correction",)),)
    episodes = assemble_all((obs(0), obs(1, source_mode="software"), obs(0, traj="t2")), bindings)
    assert [e.episode_id for e in episodes] == ["t1", "t2"]
    assert episodes[0].outcome_class is DevelopmentOutcomeClass.VALIDATED_FAILURE
    assert episodes[1].outcome_class is DevelopmentOutcomeClass.UNKNOWN
    assert set(episodes[0].source_mode_ids) == {"papers", "software"}
