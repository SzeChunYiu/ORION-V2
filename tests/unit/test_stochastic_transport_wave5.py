import pytest

from orion_v2.stochastic_transport import (
    DecisionRobustnessStatus,
    FiniteStochasticTheory,
    StochasticTransport,
    StochasticTransportLink,
    StochasticTransportStatus,
    assess_decision_robustness,
    assess_stochastic_transport,
    compose_stochastic_transport_bounds,
    total_variation,
)


def _exact_pair() -> tuple[FiniteStochasticTheory, FiniteStochasticTheory, StochasticTransport]:
    source = FiniteStochasticTheory(
        "source",
        frozenset({"a", "b"}),
        frozenset({"step"}),
        {
            ("a", "step"): {"a": 0.8, "b": 0.2},
            ("b", "step"): {"a": 0.1, "b": 0.9},
        },
        {"risk": {"a": 0.2, "b": 0.8}},
        "e1",
    )
    target = FiniteStochasticTheory(
        "target",
        frozenset({"A", "B"}),
        frozenset({"advance"}),
        {
            ("A", "advance"): {"A": 0.8, "B": 0.2},
            ("B", "advance"): {"A": 0.1, "B": 0.9},
        },
        {"risk": {"A": 0.2, "B": 0.8}},
        "e2",
    )
    transport = StochasticTransport(
        "exact-map",
        {"a": "A", "b": "B"},
        {"step": "advance"},
        ("risk",),
        0.0,
        0.0,
        "e1",
        "e2",
        2,
    )
    return source, target, transport


def _approximate_pair() -> tuple[FiniteStochasticTheory, FiniteStochasticTheory, StochasticTransport]:
    source = FiniteStochasticTheory(
        "micro",
        frozenset({"a1", "a2", "b"}),
        frozenset({"step"}),
        {
            ("a1", "step"): {"a1": 0.8, "a2": 0.0, "b": 0.2},
            ("a2", "step"): {"a1": 0.0, "a2": 0.7, "b": 0.3},
            ("b", "step"): {"a1": 0.1, "a2": 0.0, "b": 0.9},
        },
        {"risk": {"a1": 0.21, "a2": 0.29, "b": 0.8}},
        "micro-e1",
    )
    target = FiniteStochasticTheory(
        "macro",
        frozenset({"A", "B"}),
        frozenset({"advance"}),
        {
            ("A", "advance"): {"A": 0.75, "B": 0.25},
            ("B", "advance"): {"A": 0.1, "B": 0.9},
        },
        {"risk": {"A": 0.25, "B": 0.8}},
        "macro-e1",
    )
    transport = StochasticTransport(
        "approx-map",
        {"a1": "A", "a2": "A", "b": "B"},
        {"step": "advance"},
        ("risk",),
        0.05,
        0.05,
        "micro-e1",
        "macro-e1",
        1,
    )
    return source, target, transport


def test_total_variation_is_exact_on_finite_support() -> None:
    assert total_variation({"a": 0.8, "b": 0.2}, {"a": 0.75, "b": 0.25}) == pytest.approx(0.05)


def test_exact_stochastic_transport() -> None:
    source, target, transport = _exact_pair()
    result = assess_stochastic_transport(source, target, transport)
    assert result.status is StochasticTransportStatus.EXACT_STOCHASTIC_TRANSPORT
    assert result.observed_transition_error == 0
    assert result.observed_observable_error == 0


def test_epsilon_bounded_stochastic_transport() -> None:
    source, target, transport = _approximate_pair()
    result = assess_stochastic_transport(source, target, transport)
    assert result.status is StochasticTransportStatus.EPSILON_BOUNDED_STOCHASTIC_TRANSPORT
    assert result.observed_transition_error == pytest.approx(0.05)
    assert result.observed_observable_error == pytest.approx(0.04)


def test_declared_transition_bound_cannot_be_exceeded() -> None:
    source, target, transport = _approximate_pair()
    too_strict = StochasticTransport(
        transport.transport_id,
        transport.state_map,
        transport.action_map,
        transport.registered_observable_ids,
        0.04,
        transport.observable_epsilon,
        transport.source_epoch,
        transport.target_epoch,
        transport.authority_ceiling,
    )
    assert (
        assess_stochastic_transport(source, target, too_strict).status
        is StochasticTransportStatus.INVALID_TRANSITION_ERROR
    )


def test_decision_margin_can_certify_or_refuse_preservation() -> None:
    preserved = assess_decision_robustness({"A": 1.0, "B": 0.7}, error_bound=0.1)
    boundary = assess_decision_robustness({"A": 1.0, "B": 0.8}, error_bound=0.1)
    assert preserved.status is DecisionRobustnessStatus.DECISION_PRESERVED_BY_MARGIN
    assert boundary.status is DecisionRobustnessStatus.DECISION_NOT_CERTIFIED_MARGIN_TOO_SMALL


def test_small_error_can_still_change_the_best_action() -> None:
    result = assess_decision_robustness(
        {"A": 1.0, "B": 0.99},
        error_bound=0.02,
        observed_values={"A": 0.98, "B": 1.0},
    )
    assert result.status is DecisionRobustnessStatus.DECISION_CHANGED


def test_chain_bounds_accumulate_and_authority_can_only_decrease() -> None:
    result = compose_stochastic_transport_bounds(
        (
            StochasticTransportLink("l1", 0.1, 0.2, 3, ("a",)),
            StochasticTransportLink("l2", 0.15, 0.1, 1, ("b",)),
        )
    )
    assert result.transition_error_bound == pytest.approx(0.25)
    assert result.observable_error_bound == pytest.approx(0.3)
    assert result.authority_ceiling == 1
    assert result.unresolved_assumption_ids == ("a", "b")
    assert result.exact is False


def test_undeclared_dependence_blocks_chain_composition() -> None:
    result = compose_stochastic_transport_bounds(
        (StochasticTransportLink("l1", 0.1, 0.1, 1, dependence_declared=False),)
    )
    assert result.cannot_check is True
    assert result.transition_error_bound is None


def test_invalid_probability_kernel_fails_closed() -> None:
    with pytest.raises(ValueError, match="sum to one"):
        FiniteStochasticTheory(
            "bad",
            frozenset({"a", "b"}),
            frozenset({"step"}),
            {
                ("a", "step"): {"a": 0.9, "b": 0.9},
                ("b", "step"): {"a": 0.0, "b": 1.0},
            },
            {},
            "e1",
        )
