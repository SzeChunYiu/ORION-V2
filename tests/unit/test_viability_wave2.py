from orion_v2.viability import (
    FiniteViabilitySystem,
    ViabilityMode,
    justified_capture_kernel,
    viability_kernel,
)


def test_unsafe_high_reward_shortcut_is_outside_justified_kernel() -> None:
    system = FiniteViabilitySystem(
        system_id="frontier-project",
        states=frozenset({"start", "review", "claim", "unsafe"}),
        transitions={
            ("start", "review-first"): frozenset({"review"}),
            ("start", "publish-now"): frozenset({"unsafe"}),
            ("review", "adopt"): frozenset({"claim"}),
            ("claim", "maintain"): frozenset({"claim"}),
        },
        admissible_actions={
            "start": frozenset({"review-first", "publish-now"}),
            "review": frozenset({"adopt"}),
            "claim": frozenset({"maintain"}),
            "unsafe": frozenset(),
        },
        safe_states=frozenset({"start", "review", "claim"}),
        goal_states=frozenset({"claim"}),
    )
    assert justified_capture_kernel(system) == frozenset(
        {"start", "review", "claim"}
    )


def test_robust_and_existential_viability_differ_under_uncertainty() -> None:
    system = FiniteViabilitySystem(
        system_id="uncertain",
        states=frozenset({"s", "safe", "unsafe"}),
        transitions={
            ("s", "try"): frozenset({"safe", "unsafe"}),
            ("safe", "stay"): frozenset({"safe"}),
        },
        admissible_actions={
            "s": frozenset({"try"}),
            "safe": frozenset({"stay"}),
            "unsafe": frozenset(),
        },
        safe_states=frozenset({"s", "safe"}),
    )
    assert "s" in viability_kernel(system, mode=ViabilityMode.EXISTENTIAL)
    assert "s" not in viability_kernel(system, mode=ViabilityMode.ROBUST)
