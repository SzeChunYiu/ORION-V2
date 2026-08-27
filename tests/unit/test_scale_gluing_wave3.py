from orion_v2.scale_gluing import (
    ContextualModel,
    FiniteScaleModel,
    GluingStatus,
    ScaleMap,
    ScaleStatus,
    assess_gluing,
    assess_scale_map,
)


def test_locally_nonempty_parity_constraints_can_have_global_obstruction() -> None:
    model = ContextualModel(
        "parity",
        ("x", "y", "z"),
        {"x": (0, 1), "y": (0, 1), "z": (0, 1)},
        {
            "xy": ("x", "y"),
            "yz": ("y", "z"),
            "xz": ("x", "z"),
        },
        {
            "xy": frozenset({(0, 0), (1, 1)}),
            "yz": frozenset({(0, 0), (1, 1)}),
            "xz": frozenset({(0, 1), (1, 0)}),
        },
    )
    assert assess_gluing(model) is GluingStatus.GLOBAL_OBSTRUCTION


def test_scale_map_can_be_safe_now_and_unsafe_for_future_query() -> None:
    micro = FiniteScaleModel(
        "micro",
        frozenset({"a", "b"}),
        frozenset({"stay"}),
        frozenset({("a", "stay", "a"), ("b", "stay", "b")}),
        {"current": {"a": 0, "b": 0}, "future": {"a": 1, "b": 2}},
    )
    macro = FiniteScaleModel(
        "macro",
        frozenset({"m"}),
        frozenset({"stay"}),
        frozenset({("m", "stay", "m")}),
        {"current": {"m": 0}, "future": {"m": 1}},
    )
    mapping = ScaleMap(
        "map",
        {"a": "m", "b": "m"},
        {"stay": "stay"},
        ("current",),
        ("future",),
    )
    assert (
        assess_scale_map(micro, macro, mapping)
        is ScaleStatus.SAFE_CURRENT_FUTURE_UNSAFE
    )
