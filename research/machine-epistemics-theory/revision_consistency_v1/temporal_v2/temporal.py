"""Finite, model-relative temporal validity. No production authority or effects.

A complete upper revision envelope is a premise, not learned from missing edges.
The actual world/transition policy is NOT discovered or authenticated by this code.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Iterable
import json


class Verdict(str, Enum):
    PERSISTENT = "MODEL_PERSISTENT"
    REFUTED = "MODEL_PERSISTENCE_REFUTED"
    CANNOT_CHECK = "CANNOT_CHECK"


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def vertices(n: int, values: frozenset[int]) -> None:
    if type(n) is not int or n < 1:
        raise ValueError("nonempty finite state space required")
    if type(values) is not frozenset or any(type(v) is not int or not 0 <= v < n for v in values):
        raise ValueError("immutable set of in-range integer state ids required")


def graph(n: int, edges: frozenset[tuple[int, int]]) -> None:
    vertices(n, frozenset())
    if type(edges) is not frozenset:
        raise ValueError("immutable edge set required")
    for edge in edges:
        if type(edge) is not tuple or len(edge) != 2 or any(type(v) is not int or not 0 <= v < n for v in edge):
            raise ValueError("edges must be pairs of in-range integer state ids")


@dataclass(frozen=True)
class Envelope:
    n: int
    lower: frozenset[tuple[int, int]]
    upper: frozenset[tuple[int, int]]
    good: frozenset[int]
    scope: str

    def __post_init__(self) -> None:
        graph(self.n, self.lower)
        graph(self.n, self.upper)
        vertices(self.n, self.good)
        if not self.lower <= self.upper:
            raise ValueError("inconsistent lower/upper relation")
        if type(self.scope) is not str or not self.scope:
            raise ValueError("explicit registered scope required")

    def as_dict(self) -> dict:
        return {"schema": "ME_TEMPORAL_ENVELOPE_V2", "n": self.n,
                "lower": sorted(self.lower), "upper": sorted(self.upper),
                "good": sorted(self.good), "scope": self.scope}

    @property
    def fingerprint(self) -> str:
        return digest(self.as_dict())


@dataclass(frozen=True)
class Kernel:
    safe: frozenset[int]
    next_hop: tuple[int | None, ...]
    distance: tuple[int | None, ...]
    edge_reads: int
    reverse_edge_visits: int

    def adverse_path(self, start: int) -> tuple[int, ...] | None:
        if type(start) is not int or not 0 <= start < len(self.distance):
            raise ValueError("invalid start state")
        if self.distance[start] is None:
            return None
        path = [start]
        while self.next_hop[path[-1]] is not None:
            path.append(self.next_hop[path[-1]])
        return tuple(path)


def kernel(n: int, edges: frozenset[tuple[int, int]], good: frozenset[int]) -> Kernel:
    """Reverse BFS: linear graph work; deterministic sorting adds comparison cost.

    One shortest adverse path costs its length to materialize. Do not call the
    full enumeration/hashing/witness output free when citing the graph-work bound.
    """
    graph(n, edges)
    vertices(n, good)
    reverse: list[list[int]] = [[] for _ in range(n)]
    for source, target in sorted(edges):
        reverse[target].append(source)
    distance: list[int | None] = [None] * n
    following: list[int | None] = [None] * n
    queue = deque(sorted(set(range(n)) - good))
    for bad in queue:
        distance[bad] = 0
    visits = 0
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            visits += 1
            if distance[source] is None:
                distance[source] = distance[target] + 1
                following[source] = target
                queue.append(source)
    return Kernel(frozenset(i for i, d in enumerate(distance) if d is None),
                  tuple(following), tuple(distance), len(edges), visits)


def parent_kernel(n: int, edges: frozenset[tuple[int, int]], good: frozenset[int]) -> frozenset[int]:
    """Independent descending greatest fixed point; no kernel/BFS call."""
    graph(n, edges)
    vertices(n, good)
    current = good
    while True:
        rejected = {s for s, t in edges if t not in current}
        following = frozenset(s for s in current if s not in rejected)
        if following == current:
            return current
        current = following


def path_reference(n: int, edges: frozenset[tuple[int, int]], good: frozenset[int], start: int) -> tuple[int, ...] | None:
    """Independent forward enumeration of simple paths, for small calibration only."""
    graph(n, edges)
    vertices(n, good)
    if type(start) is not int or not 0 <= start < n:
        raise ValueError("invalid start")
    paths = [(start,)]
    while paths:
        for path in paths:
            if path[-1] not in good:
                return path
        paths = [p + (t,) for p in paths for s, t in sorted(edges)
                 if s == p[-1] and t not in p]
    return None


@dataclass(frozen=True)
class Witness:
    model: str
    relation: str
    path: tuple[int, ...]


def witness(env: Envelope, start: int, relation: str) -> Witness | None:
    if relation not in ("lower", "upper"):
        raise ValueError("unknown relation")
    path = kernel(env.n, getattr(env, relation), env.good).adverse_path(start)
    return None if path is None else Witness(env.fingerprint, relation, path)


def verify_witness(env: Envelope, item: Witness, start: int) -> bool:
    if type(start) is not int or not 0 <= start < env.n:
        return False
    if type(item) is not Witness or item.model != env.fingerprint or item.relation not in ("lower", "upper"):
        return False
    path = item.path
    if type(path) is not tuple or not path or any(type(v) is not int or not 0 <= v < env.n for v in path):
        return False
    if path[0] != start or path[-1] in env.good or len(path) != len(set(path)):
        return False
    edges = getattr(env, item.relation)
    return all((s, t) in edges for s, t in zip(path, path[1:]))


def classify(env: Envelope | None, belief: frozenset[int]) -> Verdict:
    """Decide UNIVERSAL persistence in every permissible completion, not current truth.

    REFUTED means a permitted adverse path refutes the universal guarantee. It
    does not mean every actual execution fails. Empty belief is not proof.
    """
    if env is None:
        return Verdict.CANNOT_CHECK
    if type(env) is not Envelope:
        raise ValueError("typed envelope required")
    vertices(env.n, belief)
    if not belief:
        return Verdict.CANNOT_CHECK
    if belief <= kernel(env.n, env.upper, env.good).safe:
        return Verdict.PERSISTENT
    if not belief <= kernel(env.n, env.lower, env.good).safe:
        return Verdict.REFUTED
    return Verdict.CANNOT_CHECK


def subsets(items: Iterable) -> Iterable[frozenset]:
    ordered = tuple(items)
    for mask in range(1 << len(ordered)):
        yield frozenset(v for i, v in enumerate(ordered) if mask & (1 << i))


def completion_reference(env: Envelope, belief: frozenset[int]) -> Verdict:
    """Exhaust all relation completions; deliberately expensive independent parent."""
    vertices(env.n, belief)
    if not belief:
        return Verdict.CANNOT_CHECK
    answers = {belief <= parent_kernel(env.n, env.lower | optional, env.good)
               for optional in subsets(sorted(env.upper - env.lower))}
    if answers == {True}:
        return Verdict.PERSISTENT
    if answers == {False}:
        return Verdict.REFUTED
    return Verdict.CANNOT_CHECK
