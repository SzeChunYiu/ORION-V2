"""Exact finite certificate transport. Risk statements only; no truth/action authority.

See THEORY.md CT-02..CT-06. Public complete finite distributions and failure
masks are model inputs, NOT estimates from a calibration sample. All arithmetic
is rational. Enumerations are deliberately bounded; a cap is CANNOT_CHECK.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
import json
from typing import Iterable, Mapping, Sequence

MAX_ATOMS = 12
MAX_DP_BUDGET = 100_000
MANIFEST_FIELDS = (
    "schema_version", "task_spec", "claim_kind", "output_predicate", "domain",
    "operator_artifact", "operator_config", "checker_artifact", "calibration_data",
    "assumptions", "query_policy", "resource_policy", "environment", "epoch",
)


class CannotCheck(ValueError):
    """A missing premise, unsupported input class, or explicit resource cap."""


def rational(value: object) -> Q:
    """Reject floating point, booleans, and silently rounded probability inputs."""
    if isinstance(value, bool) or not isinstance(value, (str, int, Q)):
        raise ValueError("exact int, rational string, or Fraction required")
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational") from exc


def probability(value: object) -> Q:
    result = rational(value)
    if not 0 <= result <= 1:
        raise ValueError("probability/budget must lie in [0,1]")
    return result


def distribution(values: Sequence[object]) -> tuple[Q, ...]:
    if not 1 <= len(values) <= MAX_ATOMS:
        raise CannotCheck(f"finite enumeration requires 1..{MAX_ATOMS} atoms")
    result = tuple(probability(v) for v in values)
    if sum(result) != 1:
        raise ValueError("distribution must sum exactly to one")
    return result


def mask(value: object, n: int) -> int:
    if type(value) is not int or not 0 <= value < (1 << n):
        raise ValueError("mask outside the registered finite sample space")
    return value


def subsets(bits: int) -> Iterable[int]:
    """All submasks, including zero, in deterministic order; no external oracle."""
    sub = bits
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & bits


def mass(p: Sequence[Q], bits: int) -> Q:
    return sum((v for i, v in enumerate(p) if bits & (1 << i)), Q(0))


def tv(p: Sequence[Q], q: Sequence[Q]) -> Q:
    if len(p) != len(q):
        raise ValueError("different sample spaces")
    return sum((abs(a - b) for a, b in zip(p, q)), Q(0)) / 2


@dataclass(frozen=True)
class Bound:
    risk: Q
    event: int
    attaining_distribution: tuple[Q, ...]

    def as_dict(self) -> dict:
        return {"risk": str(self.risk), "event": self.event,
                "attaining_distribution": list(map(str, self.attaining_distribution))}


def _fixed(p: tuple[Q, ...], bad: int, epsilon: Q) -> Bound:
    """CT-02. Internal caller has validated the finite model."""
    if bad == 0:
        return Bound(Q(0), bad, p)
    value = mass(p, bad)
    transfer = min(epsilon, 1 - value)
    q = list(p)
    receiver = next(i for i in range(len(p)) if bad & (1 << i))
    remaining = transfer
    for i in range(len(p)):
        if not bad & (1 << i):
            take = min(q[i], remaining)
            q[i] -= take
            q[receiver] += take
            remaining -= take
    if remaining != 0:
        raise ArithmeticError("attaining construction failed")
    return Bound(value + transfer, bad, tuple(q))


def fixed_event(p: Sequence[object], bad: int, epsilon: object) -> Bound:
    pp = distribution(p)
    return _fixed(pp, mask(bad, len(pp)), probability(epsilon))


@dataclass(frozen=True)
class Frontier:
    bound: Bound
    change_mass: Q
    candidates: int
    feasible: int

    def as_dict(self) -> dict:
        return {**self.bound.as_dict(), "change_mass": str(self.change_mass),
                "candidates": self.candidates, "feasible": self.feasible}


def joint_frontier(p: Sequence[object], old: int, mutable: int,
                   epsilon: object, eta: object) -> Frontier:
    """CT-03: max Q(G) over distribution drift AND allowed failure-event edits."""
    pp = distribution(p)
    old, mutable = mask(old, len(pp)), mask(mutable, len(pp))
    epsilon, eta = probability(epsilon), probability(eta)
    winner = None
    count = feasible = 0
    for changes in subsets(mutable):
        count += 1
        cost = mass(pp, changes)
        if cost > eta:
            continue
        feasible += 1
        bound = _fixed(pp, old ^ changes, epsilon)
        key = (bound.risk, -cost, -bound.event)
        if winner is None or key > winner[0]:
            winner = (key, bound, cost)
    # The unchanged event is always feasible, including eta=0.
    if winner is None:
        raise ArithmeticError("unchanged event missing")
    return Frontier(winner[1], winner[2], count, feasible)


def audit_bound(p: Sequence[object], old: int, mutable: int,
                audited: int, epsilon: object) -> Bound:
    """CT-04: exact observations say the failure event did not change on audited."""
    pp = distribution(p)
    old, mutable = mask(old, len(pp)), mask(mutable, len(pp))
    audited = mask(audited, len(pp))
    if audited & ~mutable:
        raise ValueError("audited must be a subset of mutable")
    worst_event = old | (mutable & ~audited)
    return _fixed(pp, worst_event, probability(epsilon))


def costs_and_budget(costs: Sequence[int], budget: int, n: int) -> tuple[int, ...]:
    if len(costs) != n or any(type(c) is not int or c <= 0 for c in costs):
        raise ValueError("one strictly positive integer audit cost per atom required")
    if type(budget) is not int or budget < 0:
        raise ValueError("nonnegative integer budget required")
    if budget > MAX_DP_BUDGET:
        raise CannotCheck("registered dynamic-programming budget cap exceeded")
    return tuple(costs)


def audit_cost(costs: Sequence[int], bits: int) -> int:
    return sum(c for i, c in enumerate(costs) if bits & (1 << i))


@dataclass(frozen=True)
class Audit:
    bound: Bound
    audited: int
    cost: int
    work: int
    peak_states: int

    def as_dict(self) -> dict:
        return {**self.bound.as_dict(), "audited": self.audited, "cost": self.cost,
                "work": self.work, "peak_states": self.peak_states}


def audit_exhaustive(p: Sequence[object], old: int, mutable: int,
                     epsilon: object, costs: Sequence[int], budget: int) -> Audit:
    """Reference audit subset optimization; exponential costs explicitly reported."""
    pp = distribution(p)
    old, mutable = mask(old, len(pp)), mask(mutable, len(pp))
    epsilon = probability(epsilon)
    cc = costs_and_budget(costs, budget, len(pp))
    winner = None
    work = 0
    for audited in subsets(mutable):
        work += 1
        cost = audit_cost(cc, audited)
        if cost > budget:
            continue
        bound = _fixed(pp, old | (mutable & ~audited), epsilon)
        key = (bound.risk, cost, audited)
        if winner is None or key < winner[0]:
            winner = (key, bound, audited, cost)
    if winner is None:
        raise ArithmeticError("zero-cost empty audit missing")
    return Audit(winner[1], winner[2], winner[3], work, 1)


def audit_knapsack(p: Sequence[object], old: int, mutable: int,
                   epsilon: object, costs: Sequence[int], budget: int) -> Audit:
    """Faithful CT-05 parent: 0/1 knapsack DP, NOT a weakened baseline.

    For each exact spend retain greatest covered good mass, breaking mass ties
    by greatest audited cardinality. Cardinality protects the zero-mass support
    case: erasing the last possible error can improve epsilon to zero.
    """
    pp = distribution(p)
    old, mutable = mask(old, len(pp)), mask(mutable, len(pp))
    epsilon = probability(epsilon)
    cc = costs_and_budget(costs, budget, len(pp))
    useful = mutable & ~old
    states = {0: 0}  # exact spend -> retained audit mask
    work = 0
    peak = 1

    def quality(bits: int) -> tuple:
        return (mass(pp, bits), bits.bit_count(), -bits)

    for i in range(len(pp)):
        if not useful & (1 << i):
            continue
        for spent, audited in list(states.items()):
            work += 1
            target = spent + cc[i]
            if target > budget:
                continue
            new = audited | (1 << i)
            if target not in states or quality(new) > quality(states[target]):
                states[target] = new
        peak = max(peak, len(states))
    options = []
    for spent, audited in states.items():
        work += 1
        bound = _fixed(pp, old | (mutable & ~audited), epsilon)
        options.append(((bound.risk, spent, audited), bound, audited, spent))
    winner = min(options, key=lambda item: item[0])
    return Audit(winner[1], winner[2], winner[3], work, peak)


def manifest_digest(manifest: Mapping[str, str]) -> str:
    if set(manifest) != set(MANIFEST_FIELDS):
        raise CannotCheck("manifest fields incomplete or unregistered")
    if any(not isinstance(manifest[k], str) or not manifest[k].strip()
           for k in MANIFEST_FIELDS):
        raise CannotCheck("all manifest fields require explicit nonempty identities")
    raw = json.dumps(dict(manifest), sort_keys=True, ensure_ascii=False,
                     separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def binding_status(expected: Mapping[str, str], actual: Mapping[str, str],
                   dependencies: Sequence[str], revoked: Iterable[str] = ()) -> str:
    """Mechanical binding check ONLY. This does not verify premises or issue authority."""
    try:
        a, b = manifest_digest(expected), manifest_digest(actual)
    except CannotCheck:
        return "CANNOT_CHECK"
    if expected["claim_kind"] != "RISK_BOUND" or actual["claim_kind"] != "RISK_BOUND":
        return "WRONG_CLAIM_KIND"
    if not dependencies or any(not isinstance(x, str) or not x.strip() for x in dependencies):
        return "CANNOT_CHECK"
    if set(dependencies) & set(revoked) or a != b:
        return "REVALIDATE"
    return "BINDING_MATCH_ONLY"
