from orion_v2.information_order import (
    DecisionProblem,
    ExperimentComparison,
    FiniteExperiment,
    compare_experiments,
    decision_value,
)


def _problem() -> DecisionProblem:
    return DecisionProblem(
        "guess-state",
        (0, 1),
        (0, 1),
        {0: 0.5, 1: 0.5},
        {
            (state, action): float(state == action)
            for state in (0, 1)
            for action in (0, 1)
        },
    )


def test_perfect_signal_blackwell_dominates_constant_signal() -> None:
    perfect = FiniteExperiment(
        "perfect",
        (0, 1),
        ("zero", "one"),
        {
            0: {"zero": 1.0, "one": 0.0},
            1: {"zero": 0.0, "one": 1.0},
        },
    )
    constant = FiniteExperiment(
        "constant",
        (0, 1),
        ("x",),
        {0: {"x": 1.0}, 1: {"x": 1.0}},
    )
    garbling = {"zero": {"x": 1.0}, "one": {"x": 1.0}}
    assert (
        compare_experiments(
            perfect,
            constant,
            left_to_right_garbling=garbling,
        )
        is ExperimentComparison.LEFT_BLACKWELL_DOMINATES
    )
    assert decision_value(perfect, _problem()) == 1.0
    assert decision_value(constant, _problem()) == 0.5


def test_registered_tasks_do_not_create_universal_equivalence() -> None:
    left = FiniteExperiment(
        "left", (0, 1), ("x",), {0: {"x": 1.0}, 1: {"x": 1.0}}
    )
    right = FiniteExperiment(
        "right", (0, 1), ("y",), {0: {"y": 1.0}, 1: {"y": 1.0}}
    )
    assert (
        compare_experiments(left, right, registered_problems=(_problem(),))
        is ExperimentComparison.DECISION_EQUIVALENT_ON_REGISTERED_TASKS
    )
