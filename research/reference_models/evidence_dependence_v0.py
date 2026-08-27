"""Conservative evidence-dependence reference model V0.

The connected-component count is a structural lower-resolution diagnostic, not
a statistical proof of independence. Shared declared dependence identities join
evidence items into a common component. Unobserved dependence remains outside
this model and must be reported separately in real protocols.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class DependenceInputError(ValueError):
    pass


@dataclass
class _UnionFind:
    parent: dict[str, str]

    @classmethod
    def create(cls, ids: Sequence[str]) -> "_UnionFind":
        return cls(parent={item: item for item in ids})

    def find(self, item: str) -> str:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            next_item = self.parent[item]
            self.parent[item] = root
            item = next_item
        return root

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def declared_dependence_components(
    evidence: Sequence[Mapping[str, Any]],
) -> tuple[frozenset[str], ...]:
    """Partition evidence by transitive overlap of declared dependence ids."""

    ids = [str(item.get("id", "")) for item in evidence]
    if not ids or any(not item for item in ids) or len(set(ids)) != len(ids):
        raise DependenceInputError("evidence ids must be non-empty and unique")

    union_find = _UnionFind.create(ids)
    owners: dict[str, str] = {}
    for item in evidence:
        evidence_id = str(item["id"])
        raw_dependence = item.get("dependence_ids", ())
        if not isinstance(raw_dependence, Sequence) or isinstance(raw_dependence, (str, bytes)):
            raise DependenceInputError("dependence_ids must be a sequence")
        for dependence_id_raw in raw_dependence:
            dependence_id = str(dependence_id_raw)
            if not dependence_id:
                raise DependenceInputError("dependence identities may not be blank")
            previous = owners.get(dependence_id)
            if previous is None:
                owners[dependence_id] = evidence_id
            else:
                union_find.union(previous, evidence_id)

    groups: dict[str, set[str]] = {}
    for evidence_id in ids:
        groups.setdefault(union_find.find(evidence_id), set()).add(evidence_id)
    return tuple(sorted((frozenset(group) for group in groups.values()), key=lambda group: sorted(group)))


def declared_independent_component_count(evidence: Sequence[Mapping[str, Any]]) -> int:
    return len(declared_dependence_components(evidence))


def equicorrelated_effective_n(n: int, rho: float) -> float:
    """Return n / (1 + (n-1)rho) for an equicorrelated illustration."""

    if n <= 0:
        raise DependenceInputError("n must be positive")
    if not -1.0 / max(1, n - 1) <= rho <= 1.0:
        raise DependenceInputError("rho is outside the valid equicorrelation range")
    denominator = 1.0 + (n - 1) * rho
    if denominator <= 0:
        raise DependenceInputError("effective sample size is undefined at this boundary")
    return n / denominator


__all__ = [
    "DependenceInputError",
    "declared_dependence_components",
    "declared_independent_component_count",
    "equicorrelated_effective_n",
]
