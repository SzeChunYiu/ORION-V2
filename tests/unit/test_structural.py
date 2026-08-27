from orion_v2.structural import (
    FiniteTransitionSystem,
    RelationType,
    are_bisimilar,
    indiscernibility_classes,
    safe_quotient,
)


def _coffee_machine() -> FiniteTransitionSystem:
    return FiniteTransitionSystem(
        system_id="engineering:coffee",
        states=frozenset({"idle", "paid", "served"}),
        initial_state="idle",
        transitions={
            ("idle", "commit"): frozenset({"paid"}),
            ("paid", "execute"): frozenset({"served"}),
            ("served", "reset"): frozenset({"idle"}),
        },
        observations={"idle": "ready", "paid": "authorized", "served": "complete"},
    )


def _review_process() -> FiniteTransitionSystem:
    return FiniteTransitionSystem(
        system_id="management:review",
        states=frozenset({1, 2, 3}),
        initial_state=1,
        transitions={
            (1, "commit"): frozenset({2}),
            (2, "execute"): frozenset({3}),
            (3, "reset"): frozenset({1}),
        },
        observations={1: "ready", 2: "authorized", 3: "complete"},
    )


def test_remote_domain_systems_can_be_behaviorally_equivalent() -> None:
    assert are_bisimilar(_coffee_machine(), _review_process()) is True


def test_same_topic_different_behavior_is_not_bisimilar() -> None:
    broken = FiniteTransitionSystem(
        system_id="management:broken-review",
        states=frozenset({1, 2}),
        initial_state=1,
        transitions={(1, "commit"): frozenset({2})},
        observations={1: "ready", 2: "complete"},
    )
    assert are_bisimilar(_review_process(), broken) is False


def test_indiscernibility_is_attribute_relative() -> None:
    table = {
        "a": {"surface": "same", "effect": "allow"},
        "b": {"surface": "same", "effect": "deny"},
        "c": {"surface": "different", "effect": "allow"},
    }
    surface_classes = indiscernibility_classes(table, ("surface",))
    effect_classes = indiscernibility_classes(table, ("effect",))
    assert frozenset({"a", "b"}) in surface_classes
    assert frozenset({"a", "c"}) in effect_classes


def test_safe_quotient_is_target_relative() -> None:
    safe = safe_quotient(
        (("a", "b"), ("c",)),
        {"a": 1, "b": 1, "c": 0},
        context_id="current-target",
        left_id="fine",
        right_id="coarse",
    )
    unsafe = safe_quotient(
        (("a", "b"), ("c",)),
        {"a": 1, "b": 0, "c": 0},
        context_id="future-query",
        left_id="fine",
        right_id="coarse",
    )
    assert safe.relation is RelationType.SAFE_QUOTIENT
    assert unsafe.relation is RelationType.DISTINGUISHED_BY
