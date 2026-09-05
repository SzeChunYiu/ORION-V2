"""Exact reference for a genuinely infinite class; external oracle authority is a premise.

All thresholds and query coordinates are integers with no fixed global bound.
Resource-bounded calls can return CANNOT_CHECK. No runtime admission is granted.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Callable


class CannotCheck(ValueError):
    """The declared reference contract could not be checked."""


def _integer(value, name):
    if type(value) is not int:
        raise CannotCheck(f"{name} must be an exact integer, not a boolean")
    return value


def _text(value, name):
    if type(value) is not str or not value:
        raise CannotCheck(f"{name} must be a nonempty string")
    return value


@dataclass(frozen=True)
class Context:
    authority: str
    scope: str
    verifier: str
    epoch: str


@dataclass(frozen=True)
class Observation:
    identity: str
    revocation_unit: str
    x: int
    label: int
    context: Context


@dataclass(frozen=True)
class Snapshot:
    context: Context
    records: tuple[Observation, ...] = ()
    revoked: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Interval:
    # None is an infinite endpoint, never a missing finite observation.
    lower: int | None
    upper: int | None
    status: str = "CONSISTENT"

    @property
    def cardinality(self):
        if self.status == "CONTRADICTION":
            return 0
        if self.lower is None or self.upper is None:
            return None
        return self.upper - self.lower + 1


@dataclass(frozen=True)
class Decision:
    status: str
    label: int | None
    witness_units: frozenset[str]
    snapshot_digest: str


@dataclass(frozen=True)
class Identification:
    status: str
    snapshot: Snapshot
    threshold: int | None
    query_points: tuple[int, ...]
    reason: str = ""


def validate(snapshot):
    if type(snapshot) is not Snapshot or type(snapshot.context) is not Context:
        raise CannotCheck("typed snapshot and context required")
    ctx = snapshot.context
    for name in ("authority", "scope", "verifier", "epoch"):
        _text(getattr(ctx, name), name)
    if type(snapshot.records) is not tuple or type(snapshot.revoked) is not frozenset:
        raise CannotCheck("immutable complete ledger and revocation set required")
    identities, units = set(), set()
    for row in snapshot.records:
        if type(row) is not Observation:
            raise CannotCheck("typed observation required")
        _text(row.identity, "identity")
        _text(row.revocation_unit, "revocation unit")
        if row.identity in identities:
            raise CannotCheck("record identities cannot be reused")
        identities.add(row.identity)
        units.add(row.revocation_unit)
        _integer(row.x, "query coordinate")
        if type(row.label) is not int or row.label not in (0, 1):
            raise CannotCheck("exact binary membership label required")
        if type(row.context) is not Context:
            raise CannotCheck("typed observation context required")
        for name in ("authority", "scope", "verifier", "epoch"):
            _text(getattr(row.context, name), f"observation {name}")
        if row.context != ctx:
            raise CannotCheck("authority/scope/verifier/epoch context mismatch")
    for unit in snapshot.revoked:
        _text(unit, "revoked unit")
    if not snapshot.revoked <= units:
        raise CannotCheck("undeclared revocation unit")
    return snapshot


def snapshot_digest(snapshot):
    validate(snapshot)
    payload = {
        "class": "INTEGER_THRESHOLDS_V1",
        "context": vars(snapshot.context),
        "records": [(r.identity, r.revocation_unit, r.x, r.label)
                    for r in snapshot.records],
        "revoked": sorted(snapshot.revoked),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def live_records(snapshot):
    validate(snapshot)
    return tuple(row for row in snapshot.records if row.revocation_unit not in snapshot.revoked)


def version_space(snapshot):
    rows = live_records(snapshot)
    negatives = [r.x + 1 for r in rows if r.label == 0]
    positives = [r.x for r in rows if r.label == 1]
    lower = max(negatives) if negatives else None
    upper = min(positives) if positives else None
    status = "CONTRADICTION" if lower is not None and upper is not None and lower > upper else "CONSISTENT"
    return Interval(lower, upper, status)


def predict(snapshot, x):
    _integer(x, "query coordinate")
    space = version_space(snapshot)
    digest = snapshot_digest(snapshot)
    if space.status == "CONTRADICTION":
        return Decision("CONTRADICTION", None, frozenset(), digest)
    if space.upper is not None and x >= space.upper:
        witnesses = frozenset(r.revocation_unit for r in live_records(snapshot)
                              if r.label == 1 and r.x <= x)
        return Decision("LIVE", 1, witnesses, digest)
    if space.lower is not None and x < space.lower:
        witnesses = frozenset(r.revocation_unit for r in live_records(snapshot)
                              if r.label == 0 and r.x >= x)
        return Decision("LIVE", 0, witnesses, digest)
    return Decision("UNKNOWN", None, frozenset(), digest)


def revoke(snapshot, units):
    validate(snapshot)
    if type(units) is not frozenset:
        raise CannotCheck("revocation must name an immutable complete set of units")
    for unit in units:
        _text(unit, "revoked unit")
    revised = Snapshot(snapshot.context, snapshot.records, snapshot.revoked | units)
    return validate(revised)


def boundary_units(snapshot):
    space = version_space(snapshot)
    if space.cardinality != 1:
        return None
    theta = space.lower
    rows = live_records(snapshot)
    left = frozenset(r.revocation_unit for r in rows if r.x == theta - 1 and r.label == 0)
    right = frozenset(r.revocation_unit for r in rows if r.x == theta and r.label == 1)
    return left, right


def tolerates_revocations(snapshot, r):
    """Exact global identification after ANY <= r source-unit deletions."""
    _integer(r, "revocation budget")
    if r < 0:
        raise CannotCheck("revocation budget must be nonnegative")
    boundary = boundary_units(snapshot)
    return boundary is not None and all(len(units) > r for units in boundary)


def optimal_repair_queries(snapshot):
    """Worst-case exact MQ count, given ONLY the surviving interval."""
    space = version_space(snapshot)
    if space.status == "CONTRADICTION":
        raise CannotCheck("contradictory oracle evidence")
    if space.cardinality is None:
        return None  # No uniform finite bound, not failure of pointwise learnability.
    return (space.cardinality - 1).bit_length()


def identify(snapshot, oracle: Callable[[int], Observation], *, max_queries=256,
             max_integer_bits=1024):
    """Adaptive exact learner retaining all accepted evidence for later revocation.

    External host verification of each oracle observation is a premise. This
    function validates syntax, context, identity and consistency; it cannot
    authenticate a caller's claimed authority or infer independent source units.
    No query is made when a declared budget is exhausted. Calls made to an
    invalid/unavailable oracle still count in query_points.
    """
    validate(snapshot)
    _integer(max_queries, "query budget")
    _integer(max_integer_bits, "integer bit budget")
    if max_queries < 0 or max_integer_bits < 1 or not callable(oracle):
        raise CannotCheck("nonnegative query budget, positive bit budget and oracle required")
    state, points = snapshot, []

    def bits(x):
        return abs(x).bit_length() + 1

    if any(bits(row.x) > max_integer_bits for row in state.records):
        return Identification("CANNOT_CHECK", state, None, (), "initial integer bit budget exceeded")

    while True:
        space = version_space(state)
        if space.status == "CONTRADICTION":
            return Identification("CONTRADICTION", state, None, tuple(points), "inconsistent exact labels")
        if space.cardinality == 1:
            return Identification("IDENTIFIED", state, space.lower, tuple(points))
        if len(points) >= max_queries:
            return Identification("CANNOT_CHECK", state, None, tuple(points), "query budget exhausted")
        if space.lower is not None and space.upper is not None:
            # The two possible interval sizes differ by at most one.
            x = (space.lower + space.upper) // 2
        elif space.lower is not None:
            # Move to the right by exponentially increasing magnitude.
            x = max(space.lower, 2 * abs(space.lower) + 1)
        elif space.upper is not None:
            x = min(space.upper - 1, -2 * abs(space.upper) - 1)
        else:
            x = 0
        if bits(x) > max_integer_bits:
            return Identification("CANNOT_CHECK", state, None, tuple(points), "query integer bit budget exhausted")
        points.append(x)
        try:
            answer = oracle(x)
        except Exception as exc:
            return Identification("CANNOT_CHECK", state, None, tuple(points), f"oracle unavailable: {type(exc).__name__}")
        try:
            if type(answer) is not Observation or type(answer.x) is not int or answer.x != x:
                raise CannotCheck("answer does not bind the requested integer query")
            _text(answer.revocation_unit, "answer revocation unit")
            if answer.revocation_unit in state.revoked:
                raise CannotCheck("revoked authority cannot issue a live answer in this context")
            revised = Snapshot(state.context, state.records + (answer,), state.revoked)
            validate(revised)
        except CannotCheck as exc:
            return Identification("CANNOT_CHECK", state, None, tuple(points), str(exc))
        state = revised
