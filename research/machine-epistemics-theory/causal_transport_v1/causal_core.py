"""Finite causal/transport reference semantics. Research calibration, not an authority service.

Every probability is exact. Model tables are explicit and their construction/storage are
not free. No live data, external actions, network, sampling, or hidden solver oracle.
See THEORY.md for quantifiers, parents, proofs and limits.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from typing import Callable, Mapping, Sequence


class CannotCheck(ValueError):
    """Missing or undefined input, distinct from a refuted claim or inconsistent evidence."""


def digest(value: object) -> str:
    """Restricted JSON identity. No floats, callables, repr(), or implicit normalization."""
    def encode(v: object) -> object:
        if isinstance(v, F):
            return {"rational": [v.numerator, v.denominator]}
        if v is None or type(v) in (str, int, bool):
            return v
        if isinstance(v, (tuple, list)):
            return [encode(x) for x in v]
        if isinstance(v, dict) and all(type(k) is str for k in v):
            return {k: encode(v[k]) for k in sorted(v)}
        raise TypeError("identity supports exact JSON data and Fraction only")
    body = json.dumps(encode(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(body.encode("utf-8")).hexdigest()


def distribution(values: Sequence[F | int]) -> tuple[F, ...]:
    if not values or any(type(v) not in (F, int) for v in values):
        raise ValueError("nonempty exact rational distribution required")
    p = tuple(F(v) for v in values)
    if any(v < 0 for v in p) or sum(p) != 1:
        raise ValueError("probabilities must be nonnegative and sum to exactly one")
    return p


@dataclass(frozen=True)
class Equation:
    variable: str
    parents: tuple[str, ...]
    # Ordered first by latent index, then by cartesian product of parent domains.
    table: tuple[int, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "parents", tuple(self.parents))
        object.__setattr__(self, "table", tuple(self.table))


@dataclass(frozen=True)
class SCM:
    """Finite acyclic SCM with a SINGLE joint exogenous variable (no independence assumed)."""
    variables: tuple[str, ...]
    domains: tuple[tuple[int, ...], ...]
    prior: tuple[F, ...]
    equations: tuple[Equation, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "variables", tuple(self.variables))
        object.__setattr__(self, "domains", tuple(tuple(d) for d in self.domains))
        object.__setattr__(self, "equations", tuple(self.equations))
        if not self.variables or len(set(self.variables)) != len(self.variables):
            raise ValueError("variables must be nonempty and unique")
        if not all(type(v) is str and v for v in self.variables):
            raise ValueError("variable names must be nonempty strings")
        if len(self.domains) != len(self.variables) or len(self.equations) != len(self.variables):
            raise ValueError("one domain and one equation required per variable")
        object.__setattr__(self, "prior", distribution(self.prior))
        seen: dict[str, tuple[int, ...]] = {}
        for name, dom, eq in zip(self.variables, self.domains, self.equations):
            if not dom or len(set(dom)) != len(dom) or any(type(v) is not int for v in dom):
                raise ValueError("nonempty distinct integer domains required")
            if eq.variable != name or len(set(eq.parents)) != len(eq.parents):
                raise ValueError("equation order or duplicate parent error")
            if any(p not in seen for p in eq.parents):
                raise ValueError("parents must precede their child; cycles/unknown parents rejected")
            rows = len(self.prior)
            for p in eq.parents:
                rows *= len(seen[p])
            if len(eq.table) != rows or any(type(v) is not int or v not in dom for v in eq.table):
                raise ValueError("incomplete or out-of-domain equation table")
            seen[name] = dom

    @property
    def fingerprint(self) -> str:
        return digest({"schema": "FINITE_SCM_V1", "variables": self.variables,
                       "domains": self.domains, "prior": self.prior,
                       "equations": [{"variable": e.variable, "parents": e.parents,
                                      "table": e.table} for e in self.equations]})

    def validate_assignment(self, assignment: Mapping[str, int]) -> None:
        domains = dict(zip(self.variables, self.domains))
        for key, value in assignment.items():
            if key not in domains or type(value) is not int or value not in domains[key]:
                raise ValueError("unknown variable or invalid value in assignment")

    def solve(self, latent: int, intervene: Mapping[str, int] | None = None) -> dict[str, int]:
        if type(latent) is not int or not 0 <= latent < len(self.prior):
            raise ValueError("invalid latent index")
        do = {} if intervene is None else dict(intervene)
        self.validate_assignment(do)
        domains = dict(zip(self.variables, self.domains))
        state: dict[str, int] = {}
        for eq in self.equations:
            if eq.variable in do:
                state[eq.variable] = do[eq.variable]
            else:
                offset = latent
                for parent in eq.parents:
                    dom = domains[parent]
                    offset = offset * len(dom) + dom.index(state[parent])
                state[eq.variable] = eq.table[offset]
        return state

    def marginal(self, variables: tuple[str, ...], *,
                 intervene: Mapping[str, int] | None = None) -> dict[tuple[int, ...], F]:
        if len(set(variables)) != len(variables) or any(v not in self.variables for v in variables):
            raise ValueError("unknown/duplicate marginal variable")
        domains = dict(zip(self.variables, self.domains))
        out = {row: F(0) for row in product(*(domains[v] for v in variables))}
        for u, p in enumerate(self.prior):
            state = self.solve(u, intervene)
            out[tuple(state[v] for v in variables)] += p
        return out


@dataclass(frozen=True)
class Query:
    """OBS and DO condition within their world; CF conditions in the factual world."""
    kind: str
    event: tuple[tuple[str, int], ...]
    intervention: tuple[tuple[str, int], ...] = ()
    condition: tuple[tuple[str, int], ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ("OBS", "DO", "CF"):
            raise ValueError("unregistered causal query kind")
        if self.kind == "OBS" and self.intervention:
            raise ValueError("observation query cannot carry intervention")
        for name in ("event", "intervention", "condition"):
            items = getattr(self, name)
            if any(len(item) != 2 or type(item[0]) is not str or type(item[1]) is not int
                   for item in items) or len(dict(items)) != len(items):
                raise ValueError("malformed or duplicate query coordinate")
            object.__setattr__(self, name, tuple(sorted(items)))

    @property
    def fingerprint(self) -> str:
        return digest({"schema": "CAUSAL_QUERY_V1", "kind": self.kind, "event": self.event,
                       "intervention": self.intervention, "condition": self.condition})

    def evaluate(self, model: SCM) -> F:
        event, do, cond = map(dict, (self.event, self.intervention, self.condition))
        for assignment in (event, do, cond):
            model.validate_assignment(assignment)
        numerator, denominator = F(0), F(0)
        for u, mass in enumerate(model.prior):
            target = model.solve(u, do)
            conditioning = model.solve(u) if self.kind == "CF" else target
            if all(conditioning[v] == x for v, x in cond.items()):
                denominator += mass
                if all(target[v] == x for v, x in event.items()):
                    numerator += mass
        if denominator == 0:
            raise CannotCheck("ZERO_PROBABILITY_CONDITION")
        return numerator / denominator


@dataclass(frozen=True)
class IntervalResult:
    status: str
    lower: F | None
    upper: F | None
    witnesses: tuple[str, ...]
    evaluated: int


def identified_interval(models: Sequence[SCM], query: Query) -> IntervalResult:
    """Exact over the ENTIRE supplied class only; a grid is not an all-SCM oracle."""
    if not models:
        return IntervalResult("CONFLICT", None, None, (), 0)
    vals: list[tuple[F, str]] = []
    for model in models:
        try:
            value = query.evaluate(model)
        except CannotCheck:
            return IntervalResult("CANNOT_CHECK", None, None, (model.fingerprint,), len(vals))
        vals.append((value, model.fingerprint))
    low, high = min(vals), max(vals)
    return IntervalResult("IDENTIFIED" if low[0] == high[0] else "PARTIAL",
                          low[0], high[0], (low[1], high[1]), len(vals))


def restrict_by_law(models: Sequence[SCM], query: Query, value: F) -> tuple[SCM, ...]:
    """Idealized exact population-law constraint, NOT a finite-sample estimator."""
    if type(value) not in (F, int) or not 0 <= value <= 1:
        raise ValueError("invalid exact-law probability")
    return tuple(m for m in models if query.evaluate(m) == value)


def restrict_by_observed_event(models: Sequence[SCM], query: Query) -> tuple[SCM, ...]:
    """A single observed event rules out only zero likelihood, not small likelihood."""
    return tuple(m for m in models if query.evaluate(m) > 0)


def binary_counterfactual_bounds(p0: F, p1: F) -> tuple[F, F]:
    """Sharp P(Y_1=1 | Y_0=0) interval given exact p_x=P(Y_x=1), unrestricted coupling."""
    if any(type(p) not in (F, int) or not 0 <= p <= 1 for p in (p0, p1)):
        raise ValueError("invalid marginal probability")
    p0, p1 = F(p0), F(p1)
    if p0 == 1:
        raise CannotCheck("ZERO_PROBABILITY_CONDITION")
    return max(F(0), p1 - p0) / (1 - p0), min(p1, 1 - p0) / (1 - p0)


def total_variation(p: Sequence[F], q: Sequence[F]) -> F:
    p, q = distribution(p), distribution(q)
    if len(p) != len(q):
        raise ValueError("distributions require a declared common alphabet")
    return sum((abs(a - b) for a, b in zip(p, q)), F(0)) / 2


def mix(p: Sequence[F], kernel: Sequence[Sequence[F]]) -> tuple[F, ...]:
    p = distribution(p)
    if len(kernel) != len(p):
        raise ValueError("one kernel row required per input state")
    rows = tuple(distribution(row) for row in kernel)
    if len({len(row) for row in rows}) != 1:
        raise ValueError("kernel output alphabet must be common")
    return tuple(sum((p[i] * rows[i][j] for i in range(len(p))), F(0))
                 for j in range(len(rows[0])))


def transport_bound(p: Sequence[F], q: Sequence[F],
                    kernel: Sequence[Sequence[F]], changed: Sequence[Sequence[F]]) -> F:
    """Common-mass coupling bound: eps + sum_u min(p_u,q_u) TV(K_u,L_u).

    This is at most 1-(1-eps)(1-max eta_u), and at most the additive bound.
    Inputs are stipulated exact laws, NOT inferred from finite data by this function.
    """
    p, q = distribution(p), distribution(q)
    mix(p, kernel)
    mix(q, changed)
    if len(kernel) != len(changed):
        raise ValueError("common latent alphabet required")
    eps = total_variation(p, q)
    return eps + sum((min(pu, qu) * total_variation(k, l)
                      for pu, qu, k, l in zip(p, q, kernel, changed)), F(0))


def conditional_distribution(p: Sequence[F], event: Sequence[int]) -> tuple[F, ...]:
    p = distribution(p)
    if len(set(event)) != len(event) or any(type(i) is not int or not 0 <= i < len(p) for i in event):
        raise ValueError("invalid conditioning subset")
    mass = sum((p[i] for i in event), F(0))
    if not mass:
        raise CannotCheck("ZERO_PROBABILITY_CONDITION")
    return tuple(p[i] / mass for i in event)


def conditional_tv_bound(p: Sequence[F], q: Sequence[F], event: Sequence[int]) -> F:
    p, q = distribution(p), distribution(q)
    conditional_distribution(p, event)
    conditional_distribution(q, event)
    return min(F(1), total_variation(p, q) /
               max(sum(p[i] for i in event), sum(q[i] for i in event)))


def transcript_tv_bound(epsilons: Sequence[F]) -> F:
    """Same policy, fixed finite horizon, uniform SAME-HISTORY per-round TV bounds."""
    agreement = F(1)
    for eps in epsilons:
        if type(eps) not in (F, int) or not 0 <= eps <= 1:
            raise ValueError("invalid kernel discrepancy")
        agreement *= 1 - F(eps)
    return 1 - agreement


History = tuple[tuple[int, int], ...]
Policy = Callable[[History], Sequence[F]]
Channel = Callable[[History, int], Sequence[F]]


def transcript_law(policy: Policy, channel: Channel, horizon: int) -> dict[History, F]:
    """Enumerate an adaptive history law; exponential, bounded to 8 steps for calibration.

The channel may describe changing hidden state through its conditional history kernel.
This function does not learn that kernel or authorize physical experiments.
"""
    if type(horizon) is not int or not 0 <= horizon <= 8:
        raise CannotCheck("HORIZON_OUTSIDE_REFERENCE_BUDGET")
    histories: dict[History, F] = {(): F(1)}
    for _ in range(horizon):
        updated: dict[History, F] = {}
        for history, mass in histories.items():
            for action, pa in enumerate(distribution(policy(history))):
                if not pa:
                    continue
                for observation, po in enumerate(distribution(channel(history, action))):
                    if po:
                        h = history + ((action, observation),)
                        updated[h] = updated.get(h, F(0)) + mass * pa * po
        histories = updated
        if len(histories) > 65536:
            raise CannotCheck("TRANSCRIPT_STATE_BUDGET")
    return histories


def history_distance(p: Mapping[History, F], q: Mapping[History, F]) -> F:
    keys = sorted(set(p) | set(q))
    return total_variation(tuple(p.get(k, F(0)) for k in keys),
                           tuple(q.get(k, F(0)) for k in keys))


def binding_status(bound: Mapping[str, str], current: Mapping[str, str]) -> str:
    """Identity consistency only, never authenticity, truth, equivalence, or adoption."""
    if not bound or any(not k or not v for k, v in bound.items()):
        return "CANNOT_CHECK"
    if any(k not in current or not current[k] for k in bound):
        return "CANNOT_CHECK"
    return "MATCH" if all(current[k] == v for k, v in bound.items()) else "REVALIDATE"


def verify_joint_marginals(domains: Sequence[Sequence[int]],
                           joint: Mapping[tuple[int, ...], F],
                           marginals: Mapping[tuple[int, ...], Mapping[tuple[int, ...], F]]) -> bool:
    """Verify a supplied finite joint-law witness. Does NOT solve the marginal LP.

    A rejected proposed witness is not proof that no other witness exists.
    Empty marginal requirements carry no scientific claim even though normalized joints pass.
    """
    ds = tuple(tuple(d) for d in domains)
    if not ds or any(not d or len(set(d)) != len(d) for d in ds):
        raise ValueError("nonempty finite distinct domains required")
    states = tuple(product(*ds))
    if any(s not in states for s in joint):
        raise ValueError("joint law has undeclared states")
    weights = distribution(tuple(joint.get(s, F(0)) for s in states))
    for axes, expected in marginals.items():
        if not axes or len(set(axes)) != len(axes) or any(type(i) is not int or not 0 <= i < len(ds) for i in axes):
            raise ValueError("invalid marginal coordinates")
        projections = tuple(product(*(ds[i] for i in axes)))
        if any(s not in projections for s in expected):
            raise ValueError("marginal has undeclared states")
        target = distribution(tuple(expected.get(s, F(0)) for s in projections))
        observed = {s: F(0) for s in projections}
        for state, mass in zip(states, weights):
            observed[tuple(state[i] for i in axes)] += mass
        if tuple(observed[s] for s in projections) != target:
            return False
    return True
