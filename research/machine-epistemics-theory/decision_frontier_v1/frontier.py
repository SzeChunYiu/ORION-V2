"""Exact finite decision-region calibration. Not an OCM runtime or authority source.

Python >=3.11, standard library only. Costs are exact positive Fractions.
Public tables specify possibilities; no planner method takes the actual world.
See THEORY.md for assumptions, proofs, accounting and parent ownership.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from typing import Iterable


class CannotCheck(RuntimeError):
    """Missing closure or reference-instrument capacity, never an impossibility."""


class ContractError(ValueError):
    """Malformed or inconsistent registered model, observation or certificate."""


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def cost_text(value: Fraction | None) -> str:
    return "INFINITY" if value is None else str(value)


@dataclass(frozen=True)
class Query:
    name: str
    outcomes: tuple[str, ...]
    cost: Fraction
    source_id: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or type(self.source_id) is not str or not self.name or not self.source_id:
            raise ContractError("query identity/source required")
        if not isinstance(self.outcomes, tuple) or any(type(x) is not str for x in self.outcomes):
            raise ContractError("immutable string outcome tuple required")
        if type(self.cost) is not Fraction or self.cost <= 0:
            raise ContractError("cost must be an exact positive Fraction")


@dataclass(frozen=True)
class Model:
    allowed: tuple[frozenset[str], ...]
    queries: tuple[Query, ...]
    contract_id: str
    epoch: str
    closure_id: str | None

    def __post_init__(self) -> None:
        if type(self.contract_id) is not str or type(self.epoch) is not str or not self.contract_id or not self.epoch or not self.allowed:
            raise ContractError("nonempty family, contract and epoch required")
        if not isinstance(self.allowed, tuple) or any(type(a) is not frozenset for a in self.allowed):
            raise ContractError("immutable tuple of action sets required")
        if any(any(type(a) is not str or not a for a in row) for row in self.allowed):
            raise ContractError("nonempty action identifiers required")
        if not isinstance(self.queries, tuple) or any(not isinstance(q, Query) for q in self.queries):
            raise ContractError("immutable Query tuple required")
        if self.closure_id is not None and type(self.closure_id) is not str:
            raise ContractError("closure identity must be a string or None")
        if len({q.name for q in self.queries}) != len(self.queries):
            raise ContractError("duplicate query id")
        if any(len(q.outcomes) != len(self.allowed) for q in self.queries):
            raise ContractError("incomplete observation table")

    @property
    def worlds(self) -> frozenset[int]:
        return frozenset(range(len(self.allowed)))

    @property
    def fingerprint(self) -> str:
        return digest({"schema": "ME-DF-1", "allowed": [sorted(a) for a in self.allowed],
                       "queries": [{"id": q.name, "outcomes": q.outcomes,
                                    "cost": str(q.cost), "source": q.source_id}
                                   for q in self.queries],
                       "contract": self.contract_id, "epoch": self.epoch,
                       "closure": self.closure_id})

    def belief(self, items: Iterable[int] | None = None) -> frozenset[int]:
        b = self.worlds if items is None else frozenset(items)
        if not b or any(type(w) is not int or w not in self.worlds for w in b):
            raise ContractError("EMPTY_OR_INVALID_BELIEF")
        if not self.closure_id:
            raise CannotCheck("FAMILY_CLOSURE_NOT_BOUND")
        return b

    def safe(self, belief: Iterable[int] | None = None) -> frozenset[str]:
        b = self.belief(belief)
        return frozenset.intersection(*(self.allowed[w] for w in sorted(b)))

    def query(self, name: str) -> Query:
        for q in self.queries:
            if q.name == name:
                return q
        raise ContractError("UNKNOWN_QUERY")

    def split(self, belief: Iterable[int], query: Query) -> dict[str, frozenset[int]]:
        b = self.belief(belief)
        if query not in self.queries:
            raise ContractError("UNREGISTERED_QUERY")
        return {o: frozenset(w for w in b if query.outcomes[w] == o)
                for o in sorted({query.outcomes[w] for w in b})}

    def observe(self, belief: Iterable[int], query_id: str, outcome: str) -> frozenset[int]:
        branches = self.split(belief, self.query(query_id))
        if outcome not in branches:
            raise ContractError("INCONSISTENT_OBSERVATION")
        return branches[outcome]

    def observation_cells(self, belief: Iterable[int] | None = None) -> tuple[frozenset[int], ...]:
        cells: dict[tuple[str, ...], set[int]] = {}
        for w in sorted(self.belief(belief)):
            cells.setdefault(tuple(q.outcomes[w] for q in self.queries), set()).add(w)
        return tuple(frozenset(c) for c in cells.values())

    def obstruction(self, belief: Iterable[int] | None = None) -> frozenset[int] | None:
        return next((c for c in self.observation_cells(belief) if not self.safe(c)), None)


@dataclass(frozen=True)
class Plan:
    action: str | None = None
    query: str | None = None
    branches: tuple[tuple[str, "Plan"], ...] = ()


def masks(belief: frozenset[int]):
    xs = sorted(belief)
    for n in range(1, len(xs) + 1):
        for c in combinations(xs, n):
            yield frozenset(c)


def key(b: frozenset[int]) -> str:
    return ",".join(map(str, sorted(b)))


class Solver:
    def __init__(self, model: Model, max_worlds: int = 12):
        if len(model.allowed) > max_worlds:
            raise CannotCheck("REFERENCE_STATE_CAP")
        self.model = model
        self.evaluated_states = 0

        @lru_cache(None)
        def solve(b: frozenset[int]) -> tuple[Fraction | None, Plan | None]:
            self.evaluated_states += 1
            safe = model.safe(b)
            if safe:
                return Fraction(0), Plan(action=min(safe))
            best: Fraction | None = None
            plan: Plan | None = None
            for q in model.queries:
                parts = model.split(b, q)
                if len(parts) < 2:
                    continue
                children = [(o, solve(c)) for o, c in parts.items()]
                if any(v is None for _, (v, _) in children):
                    continue
                value = q.cost + max(v for _, (v, _) in children if v is not None)
                if best is None or value < best:
                    best = value
                    plan = Plan(query=q.name, branches=tuple((o, p) for o, (_, p) in children if p is not None))
            return best, plan
        self._solve = solve

    def solve(self, belief: Iterable[int] | None = None) -> tuple[Fraction | None, Plan | None]:
        return self._solve(self.model.belief(belief))

    def certificate(self) -> dict:
        m = self.model
        return {"schema": "ME-DF-1", "fingerprint": m.fingerprint,
                "values": {key(b): cost_text(self.solve(b)[0]) for b in masks(m.worlds)}}

    def decide(self, budget: Fraction, belief: Iterable[int] | None = None) -> dict:
        if type(budget) is not Fraction or budget < 0:
            raise ContractError("nonnegative exact budget required")
        b = self.model.belief(belief)
        value, plan = self.solve(b)
        if value is None:
            witness = self.model.obstruction(b)
            if witness is None:
                raise ContractError("INFINITY_WITHOUT_OBSTRUCTION")
            return {"status": "OBSTRUCTION_WITNESSED", "worlds": sorted(witness), "cost": "INFINITY"}
        if value > budget:
            return {"status": "BUDGET_INSUFFICIENT", "cost": str(value)}
        return {"status": "DECISION_READY" if value == 0 else "QUERY_POLICY_READY",
                "cost": str(value), "plan": plan}


def verify_certificate(model: Model, cert: dict, max_worlds: int = 12) -> int:
    """Separate bottom-up Bellman checker. Does not call Solver or use its cache."""
    model.belief()
    if len(model.allowed) > max_worlds:
        raise CannotCheck("CERTIFICATE_CHECK_CAP")
    if type(cert) is not dict:
        raise ContractError("CERTIFICATE_OBJECT_REQUIRED")
    if cert.get("schema") != "ME-DF-1" or cert.get("fingerprint") != model.fingerprint:
        raise ContractError("CERTIFICATE_IDENTITY_MISMATCH")
    vals = cert.get("values", {})
    subsets = tuple(masks(model.worlds))
    if type(vals) is not dict or set(vals) != {key(b) for b in subsets}:
        raise ContractError("CERTIFICATE_DOMAIN_MISMATCH")
    checked: dict[frozenset[int], Fraction | None] = {}
    for b in subsets:
        common = set(model.allowed[min(b)])
        for w in b:
            common.intersection_update(model.allowed[w])
        candidates: list[Fraction] = [Fraction(0)] if common else []
        if not common:
            for q in model.queries:
                parts: dict[str, set[int]] = {}
                for w in b:
                    parts.setdefault(q.outcomes[w], set()).add(w)
                if len(parts) <= 1:
                    continue
                child = [checked[frozenset(c)] for c in parts.values()]
                if all(v is not None for v in child):
                    candidates.append(q.cost + max(v for v in child if v is not None))
        expected = min(candidates) if candidates else None
        if vals[key(b)] != cost_text(expected):
            raise ContractError("BELLMAN_VALUE_MISMATCH:" + key(b))
        checked[b] = expected
    return len(checked)


def verify_plan(model: Model, plan: Plan, belief: Iterable[int] | None = None) -> Fraction:
    """All-branches proof check, not just replay on a favorable actual world."""
    def check(node: Plan, b: frozenset[int], depth: int) -> Fraction:
        if not isinstance(node, Plan) or type(node.branches) is not tuple:
            raise ContractError("IMMUTABLE_PLAN_REQUIRED")
        if depth >= len(model.allowed):
            raise ContractError("NON_PROGRESSING_PLAN")
        if node.action is not None:
            if node.query is not None or node.branches or node.action not in model.safe(b):
                raise ContractError("UNSAFE_OR_MALFORMED_LEAF")
            return Fraction(0)
        if node.query is None:
            raise ContractError("MISSING_PLAN_CHOICE")
        q = model.query(node.query)
        parts = model.split(b, q)
        children = dict(node.branches)
        if len(parts) < 2 or len(children) != len(node.branches) or set(children) != set(parts):
            raise ContractError("MISSING_DUPLICATE_OR_NONPROGRESS_BRANCH")
        return q.cost + max(check(children[o], c, depth + 1) for o, c in parts.items())
    return check(plan, model.belief(belief), 0)


def replay(model: Model, plan: Plan, actual_world: int) -> tuple[str, Fraction, tuple]:
    """Evaluation harness ONLY. The planner is never given actual_world."""
    if type(actual_world) is not int or actual_world not in model.worlds:
        raise ContractError("INVALID_EVALUATION_WORLD")
    verify_plan(model, plan)
    trace = []
    cost = Fraction(0)
    node = plan
    while node.query is not None:
        q = model.query(node.query)
        outcome = q.outcomes[actual_world]
        trace.append((q.name, outcome, str(q.cost)))
        cost += q.cost
        node = dict(node.branches)[outcome]
    if node.action not in model.allowed[actual_world]:
        raise ContractError("UNSAFE_REPLAY")
    return node.action, cost, tuple(trace)


def partitions(items: frozenset[int]):
    """Canonical set partitions; exponential/Bell-number enumeration, no free preprocessing."""
    xs = tuple(sorted(items))
    def rec(i: int, blocks: tuple[frozenset[int], ...]):
        if i == len(xs):
            yield blocks
            return
        x = xs[i]
        for j in range(len(blocks)):
            yield from rec(i + 1, blocks[:j] + (blocks[j] | {x},) + blocks[j + 1:])
        yield from rec(i + 1, blocks + (frozenset({x}),))
    yield from rec(0, ())


def memory_frontier(model: Model, max_worlds: int = 7) -> dict:
    """Optimal online query cost for k message cells. Encoder construction NOT free."""
    if len(model.allowed) > max_worlds:
        raise CannotCheck("ENCODER_ENUMERATION_CAP")
    solver = Solver(model)
    n = len(model.allowed)
    best: dict[int, Fraction | None] = {k: None for k in range(1, n + 1)}
    witness: dict[int, tuple] = {}
    count = 0
    for p in partitions(model.belief()):
        count += 1
        values = [solver.solve(c)[0] for c in p]
        if any(v is None for v in values):
            continue
        value = max(v for v in values if v is not None)
        for k in range(len(p), n + 1):
            if best[k] is None or value < best[k]:
                best[k], witness[k] = value, p
    return {"cost_by_cells": {str(k): cost_text(v) for k, v in best.items()},
            "witnesses": {str(k): [sorted(c) for c in p] for k, p in witness.items()},
            "partitions_enumerated": count, "beliefs_solved": solver.evaluated_states}


def action_cover(model: Model, max_actions: int = 16) -> tuple[str, ...] | None:
    """Minimum action set hitting every world's allowed set (DF-06)."""
    model.belief()
    actions = sorted(set().union(*model.allowed))
    if len(actions) > max_actions:
        raise CannotCheck("ACTION_COVER_ENUMERATION_CAP")
    for k in range(1, len(actions) + 1):
        for selected in combinations(actions, k):
            if all(set(selected) & allowed for allowed in model.allowed):
                return selected
    return None


def observed_memory_frontier(model: Model, signal: tuple[str, ...], max_signals: int = 7) -> dict:
    """DF-11: the encoder sees only signal[w], not an unobserved hidden world.

    Acquisition cost/validity of the signal is external and must be accounted for.
    Codebook search and the decoder's later queries are counted separately.
    """
    model.belief()
    if type(signal) is not tuple or len(signal) != len(model.allowed) or any(type(z) is not str for z in signal):
        raise ContractError("COMPLETE_IMMUTABLE_SIGNAL_REQUIRED")
    symbols = tuple(sorted(set(signal)))
    if len(symbols) > max_signals:
        raise CannotCheck("SIGNAL_ENCODER_ENUMERATION_CAP")
    solver = Solver(model)
    fibres = tuple(frozenset(w for w in model.worlds if signal[w] == z) for z in symbols)
    best: dict[int, Fraction | None] = {k: None for k in range(1, len(symbols) + 1)}
    witnesses = {}
    count = 0
    for p in partitions(frozenset(range(len(symbols)))):
        count += 1
        cells = tuple(frozenset().union(*(fibres[i] for i in block)) for block in p)
        values = [solver.solve(c)[0] for c in cells]
        if any(v is None for v in values):
            continue
        value = max(v for v in values if v is not None)
        for k in range(len(p), len(symbols) + 1):
            if best[k] is None or value < best[k]:
                best[k] = value
                witnesses[str(k)] = [[symbols[i] for i in sorted(block)] for block in p]
    common_by_signal = tuple(model.safe(f) for f in fibres)
    cover_model = Model(common_by_signal, (), model.contract_id, model.epoch, model.closure_id)
    cover = action_cover(cover_model)
    return {"cost_by_cells": {str(k): cost_text(v) for k, v in best.items()},
            "signal_symbols": list(symbols), "witnesses": witnesses,
            "zero_query_cover": None if cover is None else list(cover),
            "partitions_enumerated": count, "beliefs_solved": solver.evaluated_states}
