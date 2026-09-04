"""Exact research semantics for ME-FOUNDATION-TYPED-LIFECYCLE-V1.

Standard library only. This is not a production authorization, proof-kernel,
cryptographic attestation or conformal-calibration implementation. The certificate
checker and authority set below are explicit TRUSTED INPUTS to the finite model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from fractions import Fraction as Q
from hashlib import sha256
import json
from typing import Callable, Iterable, Mapping, Sequence

Profile = tuple[int, ...]  # A support is a nonnegative bit set over base evidence.
ZERO: Profile = ()
ONE: Profile = (0,)


class CannotCheck(Exception):
    """A required input, checker or bounded computation is unavailable."""


class Conflict(ValueError):
    """Incompatible evidence bounds or conflicting event identities."""


def exact(x: int | Q) -> Q:
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError("exact rational required; floats are not certificates")
    return Q(x)


def canon(terms: Iterable[int]) -> Profile:
    items = tuple(terms)
    if any(type(w) is not int or w < 0 for w in items):
        raise TypeError("supports must be nonnegative integer bit sets")
    kept: list[int] = []
    for w in sorted(set(items), key=lambda z: (z.bit_count(), z)):
        if not any(v & w == v for v in kept):
            kept.append(w)
    return tuple(sorted(kept))


def alternative(p: Profile, q: Profile) -> Profile:
    return canon((*p, *q))


def conjunct(p: Profile, q: Profile) -> Profile:
    return canon(a | b for a in p for b in q)


def leq(p: Profile, q: Profile) -> bool:
    return all(any(b & a == b for b in q) for a in p)


def holds(p: Profile, available: int) -> bool:
    if type(available) is not int or available < 0:
        raise TypeError("available evidence must be a nonnegative bit set")
    return any(w & available == w for w in p)


def filter_nogoods(p: Profile, nogoods: Profile) -> Profile:
    nogoods = canon(nogoods)
    return canon(w for w in p if not any(n & w == n for n in nogoods))


def joint(p: Profile, q: Profile, nogoods: Profile) -> Profile:
    return filter_nogoods(conjunct(p, q), nogoods)


class Live(str, Enum):
    LIVE = "LIVE"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Interval:
    lower: Profile
    upper: Profile

    def __post_init__(self) -> None:
        if canon(self.lower) != self.lower or canon(self.upper) != self.upper:
            raise ValueError("noncanonical profile")
        if not leq(self.lower, self.upper):
            raise Conflict("lower does not imply upper")

    def verdict(self, available: int, nogoods: Profile = ZERO) -> Live:
        if holds(filter_nogoods(self.lower, nogoods), available):
            return Live.LIVE
        if not holds(filter_nogoods(self.upper, nogoods), available):
            return Live.DEAD
        return Live.UNKNOWN

    def compose(self, other: Interval, nogoods: Profile = ZERO) -> Interval:
        return Interval(joint(self.lower, other.lower, nogoods),
                        joint(self.upper, other.upper, nogoods))

    def refine(self, certificate: Interval) -> Interval:
        # Soundness of the certificate's semantic bounds is an external premise.
        return Interval(alternative(self.lower, certificate.lower),
                        conjunct(self.upper, certificate.upper))


def profiles(n: int) -> tuple[Profile, ...]:
    if type(n) is not int or not 0 <= n <= 3:
        raise CannotCheck("registered enumeration bound is 0 <= n <= 3")
    return tuple(sorted({canon(w for w in range(1 << n) if chosen >> w & 1)
                         for chosen in range(1 << (1 << n))}))


def substitute(p: Profile, images: Mapping[int, Profile]) -> Profile:
    """Acyclic/fully expanded provenance substitution, not an independence rule."""
    result = ZERO
    for w in p:
        term = ONE
        for bit in range(w.bit_length()):
            if w >> bit & 1:
                if bit not in images:
                    raise CannotCheck("unresolved provenance atom")
                term = conjunct(term, images[bit])
        result = alternative(result, term)
    return result


def closure(seed: Iterable[int], edges: Iterable[tuple[int, int]]) -> frozenset[int]:
    reached = set(seed)
    arcs = tuple(edges)
    while True:
        nxt = reached | {v for u, v in arcs if u in reached}
        if nxt == reached:
            return frozenset(reached)
        reached = nxt


Matrix = tuple[tuple[Q, ...], ...]
Vector = tuple[Q, ...]


def validate_operator(p: Sequence[Sequence[Q]], s: Sequence[Q], alpha: Q) -> None:
    n = len(s)
    if not n or len(p) != n or any(len(row) != n for row in p):
        raise ValueError("nonempty square operator and matching seed required")
    if not 0 < exact(alpha) <= 1:
        raise ValueError("restart must be in (0,1]")
    if any(exact(x) < 0 for row in p for x in row) or any(sum(row) > 1 for row in p):
        raise ValueError("operator must be nonnegative and row-substochastic")
    if any(exact(x) < 0 for x in s) or sum(s) > 1:
        raise ValueError("seed must be a nonnegative subprobability vector")


def transpose_apply(p: Matrix, x: Vector) -> Vector:
    return tuple(sum((p[i][j] * x[i] for i in range(len(x))), Q(0))
                 for j in range(len(x)))


def step(p: Matrix, s: Vector, alpha: Q, x: Vector) -> Vector:
    px = transpose_apply(p, x)
    return tuple(alpha * a + (1 - alpha) * b for a, b in zip(s, px))


def fixed_point(p: Matrix, s: Vector, alpha: Q) -> Vector:
    """Exact Gaussian solve; deliberately bounded, not a scalability claim."""
    validate_operator(p, s, alpha)
    n = len(s)
    if n > 32:
        raise CannotCheck("exact reference solve limited to 32 states")
    rows = [[Q(i == j) - (1 - alpha) * p[j][i] for j in range(n)]
            + [alpha * s[i]] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            raise ArithmeticError("singular operator despite contraction premises")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        factor = rows[j][j]
        rows[j] = [x / factor for x in rows[j]]
        for i in range(n):
            if i != j:
                factor = rows[i][j]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[j])]
    return tuple(row[-1] for row in rows)


def iterate(p: Matrix, s: Vector, alpha: Q, k: int) -> tuple[Vector, Q]:
    validate_operator(p, s, alpha)
    if type(k) is not int or k < 0:
        raise ValueError("nonnegative integer iteration index required")
    x = tuple(alpha * a for a in s)
    for _ in range(k):
        x = step(p, s, alpha, x)
    return x, (1 - alpha) ** (k + 1) * sum(s)


def residual_bound(p: Matrix, s: Vector, alpha: Q, x: Vector) -> Q:
    validate_operator(p, s, alpha)
    if len(x) != len(s):
        raise ValueError("candidate vector dimension mismatch")
    for v in x:
        exact(v)
    return sum(abs(a - b) for a, b in zip(x, step(p, s, alpha, x))) / alpha


def perturbation_bound(p: Matrix, s: Vector, r: Matrix, t: Vector, alpha: Q) -> Q:
    validate_operator(p, s, alpha)
    validate_operator(r, t, alpha)
    if len(s) != len(t):
        raise ValueError("transport into common coordinates required")
    dmatrix = max(sum(abs(a - b) for a, b in zip(x, y)) for x, y in zip(p, r))
    return sum(abs(a - b) for a, b in zip(s, t)) + (1 - alpha) / alpha * dmatrix * sum(s)


def selection_bound(marginal_error: Q, selection_mass_lower: Q) -> Q:
    a, pi = exact(marginal_error), exact(selection_mass_lower)
    if not 0 <= a <= 1 or not 0 < pi <= 1:
        raise ValueError("valid error bound and positive selection mass required")
    return min(Q(1), a / pi)


def drift_bound(error: Q, total_variation: Q, event_disagreement: Q = Q(0)) -> Q:
    xs = tuple(exact(x) for x in (error, total_variation, event_disagreement))
    if any(not 0 <= x <= 1 for x in xs):
        raise ValueError("all bounds must lie in [0,1]")
    return min(Q(1), sum(xs))


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Binding:
    implementation: str
    model: str
    configuration: str
    representation: str
    preprocessing: str
    checker: str
    calibration: str
    target: str
    quantifier: str
    selection_policy: str
    resource_contract: str
    assumptions: tuple[str, ...]
    scope: tuple[str, ...]
    epoch_start: int
    epoch_end: int

    def __post_init__(self) -> None:
        for key, value in asdict(self).items():
            if key not in ("assumptions", "scope", "epoch_start", "epoch_end"):
                if not isinstance(value, str) or not value:
                    raise ValueError("empty binding component: " + key)
        for xs in (self.assumptions, self.scope):
            if not isinstance(xs, tuple) or any(not isinstance(x, str) or not x for x in xs):
                raise TypeError("scope and assumptions must be immutable string tuples")
            if len(set(xs)) != len(xs):
                raise ValueError("duplicate scope or assumption")
        if type(self.epoch_start) is not int or type(self.epoch_end) is not int:
            raise TypeError("epochs must be integers")
        if not 0 <= self.epoch_start <= self.epoch_end:
            raise ValueError("invalid validity interval")

    @property
    def fingerprint(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class Certificate:
    binding: Binding
    kind: str  # EXACT_TARGET or RISK_BOUND; distinct propositions.
    support: Interval
    error_bound: Q = Q(0)

    def __post_init__(self) -> None:
        if self.kind not in ("EXACT_TARGET", "RISK_BOUND"):
            raise ValueError("unregistered certificate kind")
        if not 0 <= exact(self.error_bound) <= 1:
            raise ValueError("invalid error bound")
        if self.kind == "EXACT_TARGET" and self.error_bound != 0:
            raise ValueError("exact target and nonzero error are different kinds")

    @property
    def fingerprint(self) -> str:
        return digest({"binding": self.binding.fingerprint, "kind": self.kind,
                       "lower": self.support.lower, "upper": self.support.upper,
                       "error_bound": str(self.error_bound)})


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True)
class Decision:
    status: str
    asserts_target: bool = False
    risk: Q | None = None


def commit_gate(cert: Certificate, current: Binding, *, context: str, epoch: int,
                available: int, nogoods: Profile, request: str, risk_limit: Q,
                external_authority: frozenset[str],
                check_certificate: Callable[[Certificate], Verdict] | None) -> Decision:
    """Pure decision model. Does not perform an external effect or mint evidence.

    Trust in check_certificate and external_authority is an explicit assumption,
    not something this module obtains by checking a hash or a caller's label.
    """
    if cert.binding.fingerprint != current.fingerprint:
        return Decision("REVALIDATE_IDENTITY")
    if type(epoch) is not int or not current.epoch_start <= epoch <= current.epoch_end:
        return Decision("REFUSED_EPOCH")
    if context not in current.scope:
        return Decision("REFUSED_SCOPE")
    if cert.support.verdict(available, nogoods) is not Live.LIVE:
        return Decision("REFUSED_SUPPORT")
    if check_certificate is None:
        return Decision("CANNOT_CHECK")
    checked = check_certificate(cert)
    if checked is Verdict.CANNOT_CHECK:
        return Decision("CANNOT_CHECK")
    if checked is not Verdict.PASS:
        return Decision("REFUSED_CHECK")
    if request not in external_authority:
        return Decision("REFUSED_AUTHORITY")
    if request == "ASSERT_EXACT":
        if cert.kind != "EXACT_TARGET" or current.quantifier != "EXACT_TARGET":
            return Decision("REFUSED_KIND")
        return Decision("ASSERT_EXACT", True, Q(0))
    if request == "ACT_WITH_RISK":
        if cert.kind != "RISK_BOUND" or current.quantifier != "CONDITIONAL_ON_HISTORY":
            return Decision("REFUSED_QUANTIFIER")
        if not 0 <= exact(risk_limit) <= 1 or cert.error_bound > risk_limit:
            return Decision("REFUSED_RISK")
        return Decision("RISK_AUTHORIZED", False, cert.error_bound)
    return Decision("REFUSED_REQUEST")


@dataclass(frozen=True)
class Budget:
    risk_limit: Q
    work_limit: int
    events: tuple[tuple[str, str, Q, int], ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= exact(self.risk_limit) <= 1 or type(self.work_limit) is not int or self.work_limit < 0:
            raise ValueError("invalid budget")
        if not isinstance(self.events, tuple):
            raise TypeError("immutable events required")
        ids: set[str] = set()
        for event in self.events:
            if not isinstance(event, tuple) or len(event) != 4:
                raise TypeError("malformed event")
            key, cert, risk, work = event
            if not isinstance(key, str) or not isinstance(cert, str) or not key or not cert or key in ids or not 0 <= exact(risk) <= 1:
                raise ValueError("invalid or repeated event identity")
            if type(work) is not int or work < 1:
                raise ValueError("every transition needs a positive integer work charge")
            ids.add(key)
        if self.risk_spent > self.risk_limit or self.work_spent > self.work_limit:
            raise ValueError("budget exceeded")

    @property
    def risk_spent(self) -> Q:
        return sum((e[2] for e in self.events), Q(0))

    @property
    def work_spent(self) -> int:
        return sum(e[3] for e in self.events)

    def reserve(self, event: tuple[str, str, Q, int]) -> Budget:
        if not isinstance(event, tuple) or len(event) != 4:
            raise TypeError("malformed event")
        for old in self.events:
            if old[0] == event[0]:
                if old != event:
                    raise Conflict("same event id, changed payload")
                return self  # replay, not a second exposure
        return Budget(self.risk_limit, self.work_limit, (*self.events, event))


def robust_answer(possible_answers: Iterable[str]) -> Decision:
    answers = frozenset(possible_answers)
    if not answers:
        return Decision("CANNOT_CHECK_EMPTY_MODEL")
    if len(answers) != 1:
        return Decision("UNKNOWN_AMBIGUOUS")
    # A consensus over a supplied set is not proof that the true state is in it.
    return Decision("UNANIMOUS_WITHIN_MODEL")


def version_space(hypotheses: tuple[tuple[str, ...], ...],
                  lessons: tuple[tuple[int, str], ...], available: int) -> tuple[tuple[str, ...], ...]:
    """Finite, explicit hypothesis class; no claim that this class contains reality."""
    if type(available) is not int or not 0 <= available < (1 << len(lessons)):
        raise ValueError("lesson mask outside the registered universe")
    width = len(hypotheses[0]) if hypotheses else 0
    if any(len(h) != width for h in hypotheses):
        raise ValueError("hypothesis domains differ")
    if any(type(x) is not int or not 0 <= x < width for x, _ in lessons):
        raise ValueError("lesson outside registered query domain")
    return tuple(h for h in hypotheses
                 if all(not (available >> i & 1) or h[x] == y
                        for i, (x, y) in enumerate(lessons)))


def query_warrants(hypotheses: tuple[tuple[str, ...], ...],
                   lessons: tuple[tuple[int, str], ...], query: int, answer: str) -> Profile:
    """Minimal nonvacuous supports for one query, exact only on this finite class.

    Acquisition is exponential and fully charged by enumeration; the general
    theorem applies only to a nonempty, consistent active version space.
    """
    if len(lessons) > 12 or len(hypotheses) > 256:
        raise CannotCheck("finite compilation bound exceeded")
    if not hypotheses or type(query) is not int or not 0 <= query < len(hypotheses[0]):
        raise ValueError("nonempty registered class and in-domain query required")
    supports = []
    for mask in range(1 << len(lessons)):
        space = version_space(hypotheses, lessons, mask)
        if space and all(h[query] == answer for h in space):
            supports.append(mask)
    return canon(supports)
