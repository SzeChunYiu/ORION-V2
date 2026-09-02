"""FG series shared model: finite case worlds, term languages, formalisms.

The object of the FG series is a *registered decision family* `J` over a finite
case set `X`, seen through an *active formalism* `F` that induces a quotient
`q_F`.  Issue #50 §L5 fixes the collision diagnostic

    C_F = {(i, j) : q_F(x_i) = q_F(x_j) and J(x_i) != J(x_j)}

A non-empty `C_F` proves only that `F` is too coarse for that registered
decision family; it never proves that a new formalism is needed.  Which repair
is *correct* is fixed by a cost-ordered search, frozen in `REPAIR_TIERS`, that
transcribes §L5's mandated order:

    existing parent formalism
      -> one missing variable/observation
      -> local patch / scope condition
      -> representation change
      -> and only then a candidate new primitive.

Nothing in this module is authorizing.  It carries no oracle: the oracle lives
in `fg_oracle.py` and is never imported by an arm.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_INSTANCE = "orion.v2.fg.instance.v1"

# ---------------------------------------------------------------------------
# Repair tiers (frozen; the cost order IS the registered search order of §L5)
# ---------------------------------------------------------------------------

NO_CHANGE = "NO_CHANGE"
PARENT_FORMALISM_SUFFICIENT = "PARENT_FORMALISM_SUFFICIENT"
ADD_ONE_OBSERVATION = "ADD_ONE_OBSERVATION"
LOCAL_PATCH = "LOCAL_PATCH"
REPRESENTATION_CHANGE = "REPRESENTATION_CHANGE"
NEW_PRIMITIVE = "NEW_PRIMITIVE"

REPAIR_TIERS: tuple[str, ...] = (
    NO_CHANGE,
    PARENT_FORMALISM_SUFFICIENT,
    ADD_ONE_OBSERVATION,
    LOCAL_PATCH,
    REPRESENTATION_CHANGE,
    NEW_PRIMITIVE,
)
TIER_COST: Mapping[str, int] = {name: index for index, name in enumerate(REPAIR_TIERS)}

#: The two terminals whose emission is an act of formalism invention.  Only
#: NEW_PRIMITIVE counts as *false formalism invention* when the truth is
#: cheaper (§L5: a representation change is still inside the old primitives).
INVENTION_TERMINALS: tuple[str, ...] = (NEW_PRIMITIVE,)

# Derived-term grammar over recorded atoms (closed, depth 1, frozen).
DERIVED_OPS: tuple[str, ...] = ("EQ", "SUM3", "DIFF3")
#: Relational primitives available only at the NEW_PRIMITIVE tier.
RELATIONAL_OPS: tuple[str, ...] = ("COMP", "REACH")


# ---------------------------------------------------------------------------
# Structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Observable:
    """An atomic observable with a finite domain."""

    obs_id: str
    domain: tuple[str, ...]
    recorded: bool

    def __post_init__(self) -> None:
        if not self.obs_id.strip():
            raise ValueError("observables require a non-blank identity")
        if len(self.domain) < 2 or len(set(self.domain)) != len(self.domain):
            raise ValueError("observable domains must hold >= 2 distinct values")

    def index_of(self, value: str) -> int:
        return self.domain.index(value)


@dataclass(frozen=True, slots=True)
class Case:
    """One registered case: a total assignment plus its registered decision."""

    case_id: str
    values: tuple[tuple[str, str], ...]
    decision_id: str

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.decision_id.strip():
            raise ValueError("cases require case and decision identities")
        keys = [key for key, _ in self.values]
        if len(keys) != len(set(keys)):
            raise ValueError("case assignments must be functional")

    @property
    def assignment(self) -> dict[str, str]:
        return dict(self.values)


@dataclass(frozen=True, slots=True)
class Relation:
    """A registered binary relation over cases (undirected edge list)."""

    rel_id: str
    edges: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not self.rel_id.strip():
            raise ValueError("relations require an identity")


@dataclass(frozen=True, slots=True)
class Formalism:
    """A language: an identity plus the terms in its signature."""

    formalism_id: str
    term_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.formalism_id.strip():
            raise ValueError("formalisms require an identity")
        if len(self.term_ids) != len(set(self.term_ids)):
            raise ValueError("signature terms must be unique")
        if not self.term_ids:
            raise ValueError("formalisms require at least one term")


# ---------------------------------------------------------------------------
# Terms: encoded as "OP:arg|arg" strings so instances serialise as plain JSON
# ---------------------------------------------------------------------------


def atom(obs_id: str) -> str:
    return f"ATOM:{obs_id}"


def derived(op: str, left: str, right: str) -> str:
    if op not in DERIVED_OPS:
        raise ValueError(f"unknown derived op {op!r}")
    return f"{op}:{left}|{right}"


def relational(op: str, rel_id: str, anchor: str = "") -> str:
    if op not in RELATIONAL_OPS:
        raise ValueError(f"unknown relational op {op!r}")
    return f"{op}:{rel_id}|{anchor}"


def parse_term(term_id: str) -> tuple[str, tuple[str, ...]]:
    op, _, rest = term_id.partition(":")
    args = tuple(part for part in rest.split("|")) if rest else ()
    return op, args


def term_kind(term_id: str) -> str:
    op, _ = parse_term(term_id)
    if op == "ATOM":
        return "ATOM"
    if op in DERIVED_OPS:
        return "DERIVED"
    if op in RELATIONAL_OPS:
        return "RELATIONAL"
    raise ValueError(f"unknown term {term_id!r}")


# ---------------------------------------------------------------------------
# Instance
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Instance:
    """One FG70 task.  `stratum` is the true terminal and is evaluator-only."""

    instance_id: str
    suite: str
    stratum: str
    observables: tuple[Observable, ...]
    cases: tuple[Case, ...]
    active_formalism: Formalism
    parent_formalisms: tuple[Formalism, ...]
    relations: tuple[Relation, ...]
    patch_budget: int
    planted_decoys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.patch_budget < 0:
            raise ValueError("patch budget must be non-negative")
        if len({case.case_id for case in self.cases}) != len(self.cases):
            raise ValueError("case identities must be unique")
        known = {observable.obs_id for observable in self.observables}
        for case in self.cases:
            if set(case.assignment) != known:
                raise ValueError("every case must assign every observable")

    @property
    def observable_map(self) -> dict[str, Observable]:
        return {observable.obs_id: observable for observable in self.observables}

    @property
    def relation_map(self) -> dict[str, Relation]:
        return {relation.rel_id: relation for relation in self.relations}

    def recorded_atoms(self) -> tuple[str, ...]:
        return tuple(atom(o.obs_id) for o in self.observables if o.recorded)

    def all_atoms(self) -> tuple[str, ...]:
        return tuple(atom(o.obs_id) for o in self.observables)


# ---------------------------------------------------------------------------
# Term evaluation (pure; identical for arms and oracle)
# ---------------------------------------------------------------------------


def _components(relation: Relation, case_ids: Sequence[str]) -> dict[str, str]:
    parent = {case_id: case_id for case_id in case_ids}

    def find(node: str) -> str:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for left, right in relation.edges:
        if left not in parent or right not in parent:
            continue
        a, b = find(left), find(right)
        if a != b:
            parent[max(a, b)] = min(a, b)
    return {case_id: find(case_id) for case_id in case_ids}


def evaluate_term(term_id: str, instance: Instance) -> dict[str, str]:
    """Return case_id -> value for `term_id` over every case of `instance`."""

    op, args = parse_term(term_id)
    case_ids = [case.case_id for case in instance.cases]
    if op == "ATOM":
        (obs_id,) = args
        return {case.case_id: case.assignment[obs_id] for case in instance.cases}
    if op in DERIVED_OPS:
        left, right = args
        obs = instance.observable_map
        if left not in obs or right not in obs:
            raise ValueError(f"derived term references unknown observable: {term_id}")
        out: dict[str, str] = {}
        for case in instance.cases:
            li = obs[left].index_of(case.assignment[left])
            ri = obs[right].index_of(case.assignment[right])
            if op == "EQ":
                out[case.case_id] = "T" if case.assignment[left] == case.assignment[right] else "F"
            elif op == "SUM3":
                out[case.case_id] = str((li + ri) % 3)
            else:
                out[case.case_id] = str((li - ri) % 3)
        return out
    if op in RELATIONAL_OPS:
        rel_id, anchor = args
        relation = instance.relation_map.get(rel_id)
        if relation is None:
            raise ValueError(f"relational term references unknown relation: {term_id}")
        roots = _components(relation, case_ids)
        if op == "COMP":
            return dict(roots)
        target = roots.get(anchor)
        return {case_id: ("T" if roots[case_id] == target else "F") for case_id in case_ids}
    raise ValueError(f"unknown term {term_id!r}")


def signatures(term_ids: Sequence[str], instance: Instance) -> dict[str, tuple[str, ...]]:
    columns = [evaluate_term(term_id, instance) for term_id in term_ids]
    return {
        case.case_id: tuple(column[case.case_id] for column in columns)
        for case in instance.cases
    }


def derived_term_space(instance: Instance) -> tuple[str, ...]:
    """Every depth-1 derived term over *recorded* observables (no new data)."""

    recorded = [o.obs_id for o in instance.observables if o.recorded]
    terms: list[str] = []
    for left in recorded:
        for right in recorded:
            if left >= right:
                continue
            for op in DERIVED_OPS:
                terms.append(derived(op, left, right))
                if op == "DIFF3":  # EQ and SUM3 are symmetric; DIFF3 is not
                    terms.append(derived(op, right, left))
    return tuple(sorted(set(terms)))


def relational_term_space(instance: Instance) -> tuple[str, ...]:
    terms: list[str] = []
    for relation in instance.relations:
        terms.append(relational("COMP", relation.rel_id))
        for case in instance.cases:
            terms.append(relational("REACH", relation.rel_id, case.case_id))
    return tuple(sorted(set(terms)))


# ---------------------------------------------------------------------------
# Canonical serialisation
# ---------------------------------------------------------------------------


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def instance_to_json(instance: Instance) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_INSTANCE,
        "instance_id": instance.instance_id,
        "suite": instance.suite,
        "stratum": instance.stratum,
        "observables": [
            {"obs_id": o.obs_id, "domain": list(o.domain), "recorded": o.recorded}
            for o in instance.observables
        ],
        "cases": [
            {
                "case_id": c.case_id,
                "values": [list(pair) for pair in c.values],
                "decision_id": c.decision_id,
            }
            for c in instance.cases
        ],
        "active_formalism": {
            "formalism_id": instance.active_formalism.formalism_id,
            "term_ids": list(instance.active_formalism.term_ids),
        },
        "parent_formalisms": [
            {"formalism_id": f.formalism_id, "term_ids": list(f.term_ids)}
            for f in instance.parent_formalisms
        ],
        "relations": [
            {"rel_id": r.rel_id, "edges": [list(e) for e in r.edges]}
            for r in instance.relations
        ],
        "patch_budget": instance.patch_budget,
        "planted_decoys": list(instance.planted_decoys),
    }


def instance_from_json(payload: Mapping[str, Any]) -> Instance:
    return Instance(
        instance_id=payload["instance_id"],
        suite=payload["suite"],
        stratum=payload["stratum"],
        observables=tuple(
            Observable(o["obs_id"], tuple(o["domain"]), bool(o["recorded"]))
            for o in payload["observables"]
        ),
        cases=tuple(
            Case(c["case_id"], tuple((k, v) for k, v in c["values"]), c["decision_id"])
            for c in payload["cases"]
        ),
        active_formalism=Formalism(
            payload["active_formalism"]["formalism_id"],
            tuple(payload["active_formalism"]["term_ids"]),
        ),
        parent_formalisms=tuple(
            Formalism(f["formalism_id"], tuple(f["term_ids"]))
            for f in payload["parent_formalisms"]
        ),
        relations=tuple(
            Relation(r["rel_id"], tuple((a, b) for a, b in r["edges"]))
            for r in payload["relations"]
        ),
        patch_budget=int(payload["patch_budget"]),
        planted_decoys=tuple(payload.get("planted_decoys", ())),
    )


def arm_view(instance: Instance) -> dict[str, Any]:
    """Registered information handed to every arm.  Never carries the stratum."""

    payload = instance_to_json(instance)
    payload.pop("stratum")
    payload.pop("planted_decoys")
    payload["repair_tiers"] = list(REPAIR_TIERS)
    return payload


def instances_digest(instances: Iterable[Instance]) -> str:
    return sha256_text(canonical_json([instance_to_json(i) for i in instances]))
