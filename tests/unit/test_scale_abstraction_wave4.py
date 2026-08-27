from orion_v2.scale_abstraction import (
    ScaleAbstractionStatus,
    ScaleContext,
    ScaleIndexedAbstraction,
    assess_scale_abstraction,
)


def _spin_abstraction() -> ScaleIndexedAbstraction:
    micro = frozenset({"++", "+-", "-+", "--"})
    macro = frozenset({2, 0, -2})
    return ScaleIndexedAbstraction(
        "two-spin-magnetization",
        "spin-configuration",
        "magnetization",
        micro,
        macro,
        {"++": 2, "+-": 0, "-+": 0, "--": -2},
        {
            "magnetization": {
                "++": 2.0,
                "+-": 0.0,
                "-+": 0.0,
                "--": -2.0,
            }
        },
        {"magnetization": {2: 2.0, 0: 0.0, -2: -2.0}},
        {"magnetization": 0.0},
        {
            "flip-first": {
                "++": "-+",
                "+-": "--",
                "-+": "++",
                "--": "+-",
            }
        },
        {"flip-first": {2: 0, 0: 2, -2: 0}},
        {
            "first-spin": {
                "++": "+",
                "+-": "+",
                "-+": "-",
                "--": "-",
            },
            "second-spin": {
                "++": "+",
                "+-": "-",
                "-+": "+",
                "--": "-",
            },
        },
    )


def test_statistical_physics_abstraction_is_safe_for_registered_observable() -> None:
    result = assess_scale_abstraction(
        _spin_abstraction(),
        ScaleContext(
            "magnetization-only",
            ("magnetization",),
            allowed_lost_query_ids=("first-spin", "second-spin"),
        ),
    )
    assert result.status is ScaleAbstractionStatus.CONTEXT_SAFE_ABSTRACTION
    assert set(result.collapsed_query_ids) == {"first-spin", "second-spin"}


def test_registered_intervention_exposes_non_lumpable_coarse_state() -> None:
    result = assess_scale_abstraction(
        _spin_abstraction(),
        ScaleContext(
            "intervention",
            ("magnetization",),
            registered_intervention_ids=("flip-first",),
            allowed_lost_query_ids=("first-spin", "second-spin"),
        ),
    )
    assert (
        result.status
        is ScaleAbstractionStatus.OBSERVATION_SAFE_INTERVENTION_UNSAFE
    )
    assert ("flip-first", "+-") in result.intervention_mismatches or (
        "flip-first",
        "-+",
    ) in result.intervention_mismatches


def test_future_query_change_expires_current_safe_abstraction() -> None:
    result = assess_scale_abstraction(
        _spin_abstraction(),
        ScaleContext(
            "future-first-spin",
            ("magnetization",),
            allowed_lost_query_ids=("second-spin",),
            future_query_ids=("first-spin",),
        ),
    )
    assert result.status is ScaleAbstractionStatus.FUTURE_QUERY_UNSAFE


def test_undeclared_information_loss_fails_closed() -> None:
    result = assess_scale_abstraction(
        _spin_abstraction(), ScaleContext("bad", ("magnetization",))
    )
    assert result.status is ScaleAbstractionStatus.UNDECLARED_INFORMATION_LOSS


def test_geographical_total_can_hide_exposure_distribution() -> None:
    abstraction = ScaleIndexedAbstraction(
        "ma-up-example",
        "household-distribution",
        "district-total",
        frozenset({"equal", "concentrated"}),
        frozenset({100}),
        {"equal": 100, "concentrated": 100},
        {"population": {"equal": 100.0, "concentrated": 100.0}},
        {"population": {100: 100.0}},
        {"population": 0.0},
        {},
        {},
        {"exposure-inequality": {"equal": 0.0, "concentrated": 1.0}},
    )
    current = assess_scale_abstraction(
        abstraction,
        ScaleContext(
            "population-only",
            ("population",),
            allowed_lost_query_ids=("exposure-inequality",),
        ),
    )
    future = assess_scale_abstraction(
        abstraction,
        ScaleContext(
            "exposure-policy",
            ("population",),
            future_query_ids=("exposure-inequality",),
        ),
    )
    assert current.status is ScaleAbstractionStatus.CONTEXT_SAFE_ABSTRACTION
    assert future.status is ScaleAbstractionStatus.FUTURE_QUERY_UNSAFE


def test_bijective_scale_change_can_be_exact() -> None:
    abstraction = ScaleIndexedAbstraction(
        "coordinate-rename",
        "celsius-state",
        "kelvin-state",
        frozenset({0, 100}),
        frozenset({273.15, 373.15}),
        {0: 273.15, 100: 373.15},
        {"temperature": {0: 0.0, 100: 100.0}},
        {"temperature": {273.15: 0.0, 373.15: 100.0}},
        {"temperature": 0.0},
        {},
        {},
        {},
    )
    result = assess_scale_abstraction(
        abstraction, ScaleContext("temperature", ("temperature",))
    )
    assert result.status is ScaleAbstractionStatus.EXACT_SCALE_EQUIVALENCE
    assert result.scientific_equivalence_granted is True
