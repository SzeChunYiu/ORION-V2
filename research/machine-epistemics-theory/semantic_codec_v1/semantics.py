"""Exact finite first-order meanings with de Bruijn variable binding.

Truth vectors range over ALL interpretations of registered predicates on the
registered finite sorts. This is fixed-domain equivalence, not equivalence
over arbitrary structures. No hash is accepted as semantic authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
import re


class CannotCheck(ValueError):
    pass


def identifier(value):
    return type(value) is str and re.fullmatch(r"[a-z][a-z0-9_]*", value) is not None


def positive(value):
    return type(value) is int and value > 0


@dataclass(frozen=True, slots=True)
class Sort:
    name: str
    members: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Predicate:
    name: str
    sorts: tuple[str, ...]
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Registry:
    sorts: tuple[Sort, ...]
    predicates: tuple[Predicate, ...]
    epoch: str
    closed: bool = True


@dataclass(frozen=True, slots=True)
class Term:
    kind: str                         # var or const
    value: int | str


@dataclass(frozen=True, slots=True)
class Formula:
    op: str                           # atom, not, and, all, some
    name: str = ""                    # predicate or quantified sort
    terms: tuple[Term, ...] = ()
    children: tuple[Formula, ...] = ()


def atom(name, *terms):
    return Formula("atom", name, tuple(terms))


def negate(body):
    return Formula("not", children=(body,))


def conjunction(left, right):
    return Formula("and", children=(left, right))


def quantify(kind, sort, body):
    return Formula(kind, sort, children=(body,))


def validate_registry(registry):
    if type(registry) is not Registry or type(registry.closed) is not bool or not registry.closed:
        raise CannotCheck("closed materialized registry required")
    if not identifier(registry.epoch) or type(registry.sorts) is not tuple or type(registry.predicates) is not tuple:
        raise CannotCheck("immutable registry and epoch required")
    reserved = {"every", "some", "is", "it", "false", "that", "and"}
    sort_names, members = set(), set()
    for sort in registry.sorts:
        if type(sort) is not Sort or not identifier(sort.name) or sort.name in sort_names or type(sort.members) is not tuple:
            raise CannotCheck("invalid or duplicate sort")
        sort_names.add(sort.name)
        for member in sort.members:
            if not identifier(member) or member in members or member in reserved:
                raise CannotCheck("entity identities must be globally unique and unreserved")
            members.add(member)
    names = set()
    for pred in registry.predicates:
        if type(pred) is not Predicate or not identifier(pred.name) or pred.name in names or pred.name in reserved:
            raise CannotCheck("invalid or duplicate predicate")
        if type(pred.sorts) is not tuple or len(pred.sorts) not in (1, 2) or any(type(s) is not str or s not in sort_names for s in pred.sorts):
            raise CannotCheck("registered unary/binary signature required")
        if type(pred.aliases) is not tuple or any(not identifier(a) or a in reserved for a in pred.aliases) or len(set(pred.aliases)) != len(pred.aliases):
            raise CannotCheck("invalid surface aliases")
        names.add(pred.name)
    # Canonical predicate names must remain unambiguous encoder spellings.
    if any(a in names for p in registry.predicates for a in p.aliases):
        raise CannotCheck("aliases may not shadow canonical predicate names")


def registry_digest(registry):
    validate_registry(registry)
    data = json.dumps(asdict(registry), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def validate_formula(formula, registry, *, max_nodes=256, max_depth=24):
    validate_registry(registry)
    if not positive(max_nodes) or not positive(max_depth):
        raise CannotCheck("positive exact integer formula budgets required")
    predicates = {p.name: p for p in registry.predicates}
    sorts = {s.name: s for s in registry.sorts}
    constants = {m: s.name for s in registry.sorts for m in s.members}
    remaining = max_nodes

    def walk(f, binders, depth):
        nonlocal remaining
        remaining -= 1
        if remaining < 0 or depth > max_depth:
            raise CannotCheck("formula budget exhausted")
        if type(f) is not Formula or type(f.op) is not str or type(f.name) is not str or type(f.terms) is not tuple or type(f.children) is not tuple:
            raise CannotCheck("immutable typed formula required")
        if f.op == "atom":
            if f.name not in predicates or f.children or len(f.terms) != len(predicates[f.name].sorts):
                raise CannotCheck("predicate signature mismatch")
            actual = []
            for t in f.terms:
                if type(t) is not Term or type(t.kind) is not str:
                    raise CannotCheck("typed term required")
                if t.kind == "var" and type(t.value) is int and 0 <= t.value < len(binders):
                    actual.append(binders[t.value])
                elif t.kind == "const" and type(t.value) is str and t.value in constants:
                    actual.append(constants[t.value])
                else:
                    raise CannotCheck("unbound variable or unknown constant")
            if tuple(actual) != predicates[f.name].sorts:
                raise CannotCheck("term sort mismatch")
        elif f.op in ("not", "and"):
            if f.name or f.terms or len(f.children) != (1 if f.op == "not" else 2):
                raise CannotCheck("connective shape mismatch")
            for child in f.children:
                walk(child, binders, depth + 1)
        elif f.op in ("all", "some"):
            if f.name not in sorts or f.terms or len(f.children) != 1:
                raise CannotCheck("quantifier shape mismatch")
            walk(f.children[0], (f.name,) + binders, depth + 1)
        else:
            raise CannotCheck("unknown formula operator")
    walk(formula, (), 0)


def structural_digest(formula, registry):
    validate_formula(formula, registry)
    payload = [registry_digest(registry), asdict(formula)]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class Meaning:
    registry_digest: str
    ground_atoms: tuple[tuple[str, tuple[str, ...]], ...]
    truth_vector: tuple[bool, ...]

    @property
    def seed(self):
        """Finite semantic quotient key, not the runtime KSO seed distribution."""
        data = [self.registry_digest, self.ground_atoms, self.truth_vector]
        return hashlib.sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()


def meaning(formula, registry, *, max_worlds=4096, max_steps=2_000_000):
    validate_formula(formula, registry)
    if not positive(max_worlds) or not positive(max_steps):
        raise CannotCheck("positive exact integer evaluation budgets required")
    domains = {s.name: s.members for s in registry.sorts}
    grounds = []
    for pred in registry.predicates:
        for args in itertools.product(*(domains[s] for s in pred.sorts)):
            grounds.append((pred.name, args))
            # Avoid constructing an unbounded world count or ground inventory.
            if len(grounds) >= max_worlds.bit_length():
                raise CannotCheck("complete world inventory exceeds budget")
    grounds = tuple(grounds)
    count = 1 << len(grounds)
    if count > max_worlds:
        raise CannotCheck("complete world inventory exceeds budget")
    indices = {g: i for i, g in enumerate(grounds)}
    remaining = max_steps

    def evaluate(f, environment, mask):
        nonlocal remaining
        remaining -= 1
        if remaining < 0:
            raise CannotCheck("truth-table evaluation budget exhausted")
        if f.op == "atom":
            args = tuple(environment[t.value] if t.kind == "var" else t.value for t in f.terms)
            return bool(mask & (1 << indices[(f.name, args)]))
        if f.op == "not":
            return not evaluate(f.children[0], environment, mask)
        if f.op == "and":
            return all(evaluate(c, environment, mask) for c in f.children)
        values = (evaluate(f.children[0], (member,) + environment, mask) for member in domains[f.name])
        return all(values) if f.op == "all" else any(values)

    vector = tuple(evaluate(formula, (), mask) for mask in range(count))
    return Meaning(registry_digest(registry), grounds, vector)
