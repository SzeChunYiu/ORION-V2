from orion_v2.performative_dynamics import (
    FinitePerformativeSystem,
    PerformativeDynamicsStatus,
    assess_performative_dynamics,
    performative_optima,
    retraining_trajectory,
    static_optima,
)


def test_deployment_response_can_reverse_policy_ranking() -> None:
    system = FinitePerformativeSystem(
        "response",
        ("A", "B"),
        ("good", "bad"),
        {
            "A": {"good": 0.1, "bad": 0.9},
            "B": {"good": 0.9, "bad": 0.1},
        },
        {
            ("A", "good"): 0.0,
            ("A", "bad"): 1.0,
            ("B", "good"): 0.4,
            ("B", "bad"): 0.4,
        },
    )
    baseline = {"good": 0.9, "bad": 0.1}
    assert static_optima(system, baseline) == ("A",)
    assert performative_optima(system) == ("B",)
    assert (
        assess_performative_dynamics(system, baseline)
        is PerformativeDynamicsStatus.POLICY_WINNER_REVERSAL
    )


def test_retraining_can_cycle() -> None:
    system = FinitePerformativeSystem(
        "cycle",
        ("A", "B"),
        (0, 1),
        {"A": {0: 1.0, 1: 0.0}, "B": {0: 0.0, 1: 1.0}},
        {
            ("A", 0): 1.0,
            ("A", 1): 0.0,
            ("B", 0): 0.0,
            ("B", 1): 1.0,
        },
    )
    path, status = retraining_trajectory(system, "A")
    assert status is PerformativeDynamicsStatus.RETRAINING_CYCLE
    assert path[-1] == "A"
