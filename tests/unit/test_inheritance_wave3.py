from orion_v2.inheritance import (
    ComponentInheritanceEdge,
    ComponentInheritanceRelation,
    ComponentNode,
    InheritanceStatus,
    affected_descendants,
    assess_inheritance,
)


def test_multi_parent_component_inheritance_can_be_validated() -> None:
    nodes = (
        ComponentNode("p1", "parent-a", "representation", "e1", 2),
        ComponentNode("p2", "parent-b", "method", "e1", 2),
        ComponentNode("c", "child", "composite", "e2", 2),
    )
    edges = (
        ComponentInheritanceEdge(
            "p1",
            "c",
            ComponentInheritanceRelation.MERGE,
            True,
            ("receipt:a",),
        ),
        ComponentInheritanceEdge(
            "p2",
            "c",
            ComponentInheritanceRelation.MERGE,
            True,
            ("receipt:b",),
        ),
    )
    result = assess_inheritance(
        nodes, edges, required_child_component_ids=("c",)
    )
    assert result.status is InheritanceStatus.VALIDATED_RETICULATE


def test_authority_cannot_amplify_through_lineage() -> None:
    nodes = (
        ComponentNode("p", "parent", "evidence", "e1", 1),
        ComponentNode("c", "child", "claim", "e2", 3),
    )
    edges = (
        ComponentInheritanceEdge(
            "p",
            "c",
            ComponentInheritanceRelation.COPY,
            True,
            ("receipt",),
        ),
    )
    assert (
        assess_inheritance(nodes, edges).status
        is InheritanceStatus.INVALID_AUTHORITY_AMPLIFICATION
    )


def test_component_change_reopens_only_descendants() -> None:
    edges = (
        ComponentInheritanceEdge(
            "a",
            "b",
            ComponentInheritanceRelation.COPY,
            True,
            ("r",),
        ),
        ComponentInheritanceEdge(
            "b",
            "c",
            ComponentInheritanceRelation.COPY,
            True,
            ("r",),
        ),
        ComponentInheritanceEdge(
            "x",
            "y",
            ComponentInheritanceRelation.COPY,
            True,
            ("r",),
        ),
    )
    assert affected_descendants(("a",), edges) == ("a", "b", "c")


def test_component_inheritance_cycle_is_rejected() -> None:
    nodes = (
        ComponentNode("a", "artifact-a", "method", "e1", 1),
        ComponentNode("b", "artifact-b", "method", "e1", 1),
    )
    edges = (
        ComponentInheritanceEdge(
            "a",
            "b",
            ComponentInheritanceRelation.COPY,
            True,
            ("r1",),
        ),
        ComponentInheritanceEdge(
            "b",
            "a",
            ComponentInheritanceRelation.COPY,
            True,
            ("r2",),
        ),
    )
    assert assess_inheritance(nodes, edges).status is InheritanceStatus.INVALID_CYCLE
