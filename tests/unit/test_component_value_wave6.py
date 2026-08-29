import pytest

from orion_v2.component_value import (
    ComponentValueStatus,
    ConfigurationCaseResult,
    CostVector,
    CriticalFailure,
    PairInteractionStatus,
    assess_component_value,
    assess_pair_interaction,
    pareto_frontier,
    result_dominates,
)


def result(
    case: str,
    config: str,
    components: set[str],
    success: bool,
    quality: float,
    *,
    failures: set[CriticalFailure] = set(),
    compute: float = 0,
    latency: float = 0,
) -> ConfigurationCaseResult:
    return ConfigurationCaseResult(
        case,
        config,
        frozenset(components),
        success,
        quality,
        frozenset(failures),
        CostVector(compute=compute, latency=latency),
    )


def test_critical_failure_is_noncompensatory_in_dominance() -> None:
    good = result("c", "good", {"k"}, True, 0.7, compute=2)
    fast_wrong = result(
        "c",
        "fast-wrong",
        set(),
        False,
        1.0,
        failures={CriticalFailure.FALSE_COMPLETION},
        compute=1,
    )
    assert result_dominates(good, fast_wrong)
    assert not result_dominates(fast_wrong, good)


def test_pareto_frontier_keeps_quality_cost_tradeoff() -> None:
    accurate = result("c", "accurate", {"a"}, True, 0.95, compute=10)
    efficient = result("c", "efficient", {"b"}, True, 0.85, compute=2)
    dominated = result("c", "dominated", {"d"}, True, 0.8, compute=3)
    assert pareto_frontier((accurate, efficient, dominated)) == (
        "accurate",
        "efficient",
    )


def test_component_is_necessary_when_removal_causes_false_completion() -> None:
    full = [result("c", "full", {"x"}, True, 0.9, compute=2)]
    ablated = [
        result(
            "c",
            "minus-x",
            set(),
            False,
            0.5,
            failures={CriticalFailure.FALSE_COMPLETION},
            compute=1,
        )
    ]
    assessment = assess_component_value("x", full, ablated)
    assert assessment.status is ComponentValueStatus.NECESSARY
    assert assessment.protected_regression_case_ids == ("c",)


def test_parent_replacement_prevents_framework_ownership_claim() -> None:
    full = [result("c", "full", {"x"}, True, 0.9, compute=3)]
    ablated = [result("c", "minus-x", set(), True, 0.6, compute=1)]
    parent = [result("c", "parent", {"parent"}, True, 0.91, compute=2)]
    assessment = assess_component_value(
        "x", full, ablated, parent_replacement_results=parent
    )
    assert assessment.status is ComponentValueStatus.PARENT_REPLACEABLE
    assert assessment.parent_replacement_case_ids == ("c",)


def test_component_that_only_adds_cost_is_redundant_drag() -> None:
    full = [result("c", "full", {"x"}, True, 0.9, compute=3)]
    ablated = [result("c", "minus-x", set(), True, 0.9, compute=1)]
    assessment = assess_component_value("x", full, ablated)
    assert assessment.status is ComponentValueStatus.REDUNDANT_DRAG


def test_component_can_improve_efficiency_without_changing_science() -> None:
    full = [result("c", "full", {"x"}, True, 0.9, compute=1)]
    ablated = [result("c", "minus-x", set(), True, 0.9, compute=3)]
    assessment = assess_component_value("x", full, ablated)
    assert assessment.status is ComponentValueStatus.EFFICIENCY_IMPROVING


def test_component_is_harmful_when_removal_repairs_quality_and_failure() -> None:
    full = [
        result(
            "c",
            "full",
            {"x"},
            False,
            0.4,
            failures={CriticalFailure.CRITERION_DRIFT},
            compute=3,
        )
    ]
    ablated = [result("c", "minus-x", set(), True, 0.8, compute=2)]
    assessment = assess_component_value("x", full, ablated)
    assert assessment.status is ComponentValueStatus.HARMFUL
    assert assessment.protected_improvement_case_ids == ("c",)


def test_component_is_contextual_when_it_helps_one_case_and_hurts_another() -> None:
    full = [
        result("help", "full-help", {"x"}, True, 0.9, compute=2),
        result("hurt", "full-hurt", {"x"}, True, 0.6, compute=2),
    ]
    ablated = [
        result("help", "minus-help", set(), True, 0.5, compute=1),
        result("hurt", "minus-hurt", set(), True, 0.9, compute=1),
    ]
    assessment = assess_component_value("x", full, ablated)
    assert assessment.status is ComponentValueStatus.CONTEXTUAL


def test_no_matched_cases_returns_cannot_check() -> None:
    assessment = assess_component_value(
        "x",
        [result("a", "full", {"x"}, True, 1.0)],
        [result("b", "minus", set(), True, 1.0)],
    )
    assert assessment.status is ComponentValueStatus.CANNOT_CHECK


def test_synergistic_pair_requires_both_components() -> None:
    full = [result("c", "full", {"a", "b"}, True, 1.0)]
    minus_a = [
        result(
            "c",
            "minus-a",
            {"b"},
            False,
            0.2,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        )
    ]
    minus_b = [
        result(
            "c",
            "minus-b",
            {"a"},
            False,
            0.2,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        )
    ]
    minus_both = [
        result(
            "c",
            "minus-both",
            set(),
            False,
            0.0,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        )
    ]
    assessment = assess_pair_interaction(
        "a", "b", full, minus_a, minus_b, minus_both
    )
    assert assessment.status is PairInteractionStatus.SYNERGISTIC
    assert assessment.interaction_by_case[0][1] == pytest.approx(1.0)


def test_substitutable_pair_only_fails_when_both_removed() -> None:
    full = [result("c", "full", {"a", "b"}, True, 1.0)]
    minus_a = [result("c", "minus-a", {"b"}, True, 1.0)]
    minus_b = [result("c", "minus-b", {"a"}, True, 1.0)]
    minus_both = [
        result(
            "c",
            "minus-both",
            set(),
            False,
            0.0,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        )
    ]
    assessment = assess_pair_interaction(
        "a", "b", full, minus_a, minus_b, minus_both
    )
    assert assessment.status is PairInteractionStatus.SUBSTITUTABLE
    assert assessment.interaction_by_case[0][1] == pytest.approx(-1.0)


def test_additive_pair_has_near_zero_interaction() -> None:
    full = [result("c", "full", {"a", "b"}, True, 1.0)]
    minus_a = [result("c", "minus-a", {"b"}, True, 0.7)]
    minus_b = [result("c", "minus-b", {"a"}, True, 0.8)]
    minus_both = [result("c", "minus-both", set(), True, 0.5)]
    assessment = assess_pair_interaction(
        "a", "b", full, minus_a, minus_b, minus_both
    )
    assert assessment.status is PairInteractionStatus.ADDITIVE
    assert assessment.interaction_by_case[0][1] == pytest.approx(0.0)


def test_invalid_full_reference_is_excluded_from_interaction() -> None:
    full = [
        result(
            "c",
            "full",
            {"a", "b"},
            False,
            0.9,
            failures={CriticalFailure.FALSE_COMPLETION},
        )
    ]
    minus_a = [result("c", "minus-a", {"b"}, True, 0.8)]
    minus_b = [result("c", "minus-b", {"a"}, True, 0.8)]
    minus_both = [result("c", "minus-both", set(), True, 0.7)]
    assessment = assess_pair_interaction(
        "a", "b", full, minus_a, minus_b, minus_both
    )
    assert assessment.status is PairInteractionStatus.CANNOT_CHECK
    assert assessment.excluded_case_ids == ("c",)


def test_pair_interaction_can_be_contextual_across_cases() -> None:
    full = [
        result("synergy", "full-s", {"a", "b"}, True, 1.0),
        result("substitute", "full-r", {"a", "b"}, True, 1.0),
    ]
    minus_a = [
        result(
            "synergy",
            "ma-s",
            {"b"},
            False,
            0.0,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        ),
        result("substitute", "ma-r", {"b"}, True, 1.0),
    ]
    minus_b = [
        result(
            "synergy",
            "mb-s",
            {"a"},
            False,
            0.0,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        ),
        result("substitute", "mb-r", {"a"}, True, 1.0),
    ]
    minus_both = [
        result(
            "synergy",
            "mab-s",
            set(),
            False,
            0.0,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        ),
        result(
            "substitute",
            "mab-r",
            set(),
            False,
            0.0,
            failures={CriticalFailure.PROTECTED_CAPABILITY_LOSS},
        ),
    ]
    assessment = assess_pair_interaction(
        "a", "b", full, minus_a, minus_b, minus_both
    )
    assert assessment.status is PairInteractionStatus.CONTEXTUAL_INTERACTION
