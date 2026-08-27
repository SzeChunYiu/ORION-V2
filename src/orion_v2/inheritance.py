from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class InheritanceRelation(str, Enum):
    COPY = "COPY"
    TRANSFORM = "TRANSFORM"
    CALIBRATE = "CALIBRATE"
    MERGE = "MERGE"
    COMPOSE = "COMPOSE"


class InheritanceStatus(str, Enum):
    EXACT_SINGLE_PARENT = "EXACT_SINGLE_PARENT"
    VALIDATED_RETICULATE = "VALIDATED_RETICULATE"
    INVALID_CYCLE = "INVALID_CYCLE"
    INVALID_UNVALIDATED_TRANSPORT = "INVALID_UNVALIDATED_TRANSPORT"
    INVALID_AUTHORITY_AMPLIFICATION = "INVALID_AUTHORITY_AMPLIFICATION"
    MISSING_COMPONENT_LINEAGE = "MISSING_COMPONENT_LINEAGE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ComponentNode:
    component_id: str
    artifact_id: str
    role: str
    epoch: str
    authority_ceiling: int

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.component_id,
                self.artifact_id,
                self.role,
                self.epoch,
            )
        ):
            raise ValueError(
                "component identities, role and epoch must be non-blank"
            )
        if self.authority_ceiling < 0:
            raise ValueError("authority ceiling must be non-negative")


@dataclass(frozen=True, slots=True)
class ComponentInheritanceEdge:
    parent_component_id: str
    child_component_id: str
    relation: InheritanceRelation
    transport_validated: bool
    source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "relation", InheritanceRelation(self.relation))
        if (
            not self.parent_component_id.strip()
            or not self.child_component_id.strip()
        ):
            raise ValueError("inheritance endpoints must be non-blank")
        if self.transport_validated and not self.source_ids:
            raise ValueError("validated transport requires source identities")


@dataclass(frozen=True, slots=True)
class InheritanceAssessment:
    status: InheritanceStatus
    affected_component_ids: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    grants_authority: bool = False

    def __post_init__(self) -> None:
        if self.grants_authority:
            raise ValueError("inheritance assessment cannot grant authority")


def _has_cycle(
    nodes: set[str], edges: tuple[ComponentInheritanceEdge, ...]
) -> bool:
    children: dict[str, set[str]] = {node: set() for node in nodes}
    for edge in edges:
        children.setdefault(edge.parent_component_id, set()).add(
            edge.child_component_id
        )
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(child) for child in children.get(node, ())):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)


def affected_descendants(
    changed_component_ids: tuple[str, ...],
    edges: tuple[ComponentInheritanceEdge, ...],
) -> tuple[str, ...]:
    children: dict[str, set[str]] = {}
    for edge in edges:
        children.setdefault(edge.parent_component_id, set()).add(
            edge.child_component_id
        )
    affected = set(changed_component_ids)
    frontier = list(changed_component_ids)
    while frontier:
        current = frontier.pop()
        for child in children.get(current, ()):
            if child not in affected:
                affected.add(child)
                frontier.append(child)
    return tuple(sorted(affected))


def assess_inheritance(
    nodes: tuple[ComponentNode, ...],
    edges: tuple[ComponentInheritanceEdge, ...],
    *,
    required_child_component_ids: tuple[str, ...] = (),
) -> InheritanceAssessment:
    node_by_id: Mapping[str, ComponentNode] = {
        node.component_id: node for node in nodes
    }
    if len(node_by_id) != len(nodes):
        raise ValueError("component identities must be unique")
    if any(
        edge.parent_component_id not in node_by_id
        or edge.child_component_id not in node_by_id
        for edge in edges
    ):
        return InheritanceAssessment(InheritanceStatus.CANNOT_CHECK, ())
    if _has_cycle(set(node_by_id), edges):
        return InheritanceAssessment(InheritanceStatus.INVALID_CYCLE, ())
    incoming: dict[str, list[ComponentInheritanceEdge]] = {}
    for edge in edges:
        incoming.setdefault(edge.child_component_id, []).append(edge)
        parent = node_by_id[edge.parent_component_id]
        child = node_by_id[edge.child_component_id]
        if child.authority_ceiling > parent.authority_ceiling:
            return InheritanceAssessment(
                InheritanceStatus.INVALID_AUTHORITY_AMPLIFICATION,
                affected_descendants((child.component_id,), edges),
            )
        if (
            edge.relation is not InheritanceRelation.COPY
            and not edge.transport_validated
        ):
            return InheritanceAssessment(
                InheritanceStatus.INVALID_UNVALIDATED_TRANSPORT,
                affected_descendants((child.component_id,), edges),
            )
    missing = set(required_child_component_ids) - set(incoming)
    if missing:
        return InheritanceAssessment(
            InheritanceStatus.MISSING_COMPONENT_LINEAGE,
            tuple(sorted(missing)),
        )
    reticulate = any(
        len(incoming_edges) > 1 for incoming_edges in incoming.values()
    )
    return InheritanceAssessment(
        InheritanceStatus.VALIDATED_RETICULATE
        if reticulate
        else InheritanceStatus.EXACT_SINGLE_PARENT,
        (),
    )
