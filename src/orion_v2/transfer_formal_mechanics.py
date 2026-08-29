"""Executable reference mechanics for formal transfer and conceptual development.

The module is deliberately content-neutral.  It implements exact, finite reference
checks for several mature parent formalisms that can be used as baselines or
oracles in ORION-V2 transfer-discovery experiments:

- typed partial relational homomorphisms;
- Formal Concept Analysis closure;
- finite-category functoriality;
- invariance/equivariance checks;
- non-compensatory value profiles.

It does not claim that all mathematical or scientific concepts reduce to these
representations.  A native domain may refuse the projection and remain the
strongest parent.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Iterable, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class TypedFact:
    predicate: str
    relation_type: str
    args: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.predicate.strip() or not self.relation_type.strip() or not self.args:
            raise ValueError("facts require predicate, relation type and arguments")
        if any(not arg.strip() for arg in self.args):
            raise ValueError("fact arguments may not be blank")


@dataclass(frozen=True, slots=True)
class FiniteRelationalStructure:
    structure_id: str
    domain_id: str
    nodes: tuple[str, ...]
    node_types: tuple[tuple[str, str], ...]
    facts: tuple[TypedFact, ...]
    invariant_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.structure_id.strip() or not self.domain_id.strip():
            raise ValueError("structures require identities")
        if not self.nodes or len(self.nodes) != len(set(self.nodes)):
            raise ValueError("nodes must be non-empty and unique")
        if any(not n.strip() for n in self.nodes):
            raise ValueError("node identities may not be blank")
        type_map = dict(self.node_types)
        if set(type_map) != set(self.nodes):
            raise ValueError("node_types must bind every node exactly once")
        if len(self.node_types) != len(type_map):
            raise ValueError("duplicate node type binding")
        if any(not t.strip() for t in type_map.values()):
            raise ValueError("node types may not be blank")
        for fact in self.facts:
            if any(arg not in type_map for arg in fact.args):
                raise ValueError("fact references unknown node")

    @property
    def types(self) -> dict[str, str]:
        return dict(self.node_types)


@dataclass(frozen=True, slots=True)
class FormalTransferMap:
    node_map: tuple[tuple[str, str], ...]
    relation_map: tuple[tuple[str, str], ...]
    relation_type_map: tuple[tuple[str, str], ...] = ()
    invariant_map: tuple[tuple[str, str], ...] = ()

    @property
    def nodes(self) -> dict[str, str]:
        return dict(self.node_map)

    @property
    def relations(self) -> dict[str, str]:
        return dict(self.relation_map)

    @property
    def relation_types(self) -> dict[str, str]:
        return dict(self.relation_type_map)

    @property
    def invariants(self) -> dict[str, str]:
        return dict(self.invariant_map)


@dataclass(frozen=True, slots=True)
class HomomorphismAssessment:
    mapped_node_count: int
    mapped_fact_count: int
    type_violations: int
    relation_violations: int
    relation_type_violations: int
    invariant_violations: int
    relation_preservation_rate: float
    critical_valid: bool



def assess_partial_homomorphism(
    donor: FiniteRelationalStructure,
    target: FiniteRelationalStructure,
    mapping: FormalTransferMap,
) -> HomomorphismAssessment:
    """Check a finite partial typed relational homomorphism exactly."""

    node_map = mapping.nodes
    relation_map = mapping.relations
    relation_type_map = mapping.relation_types
    invariant_map = mapping.invariants

    if not set(node_map).issubset(donor.nodes):
        raise ValueError("node map has unknown donor nodes")
    if not set(node_map.values()).issubset(target.nodes):
        raise ValueError("node map has unknown target nodes")

    type_violations = 0
    for source, dest in node_map.items():
        if donor.types[source] != target.types[dest]:
            type_violations += 1

    target_fact_keys = {
        (fact.predicate, fact.relation_type, fact.args)
        for fact in target.facts
    }
    mapped_fact_count = 0
    relation_violations = 0
    relation_type_violations = 0
    for fact in donor.facts:
        if not all(arg in node_map for arg in fact.args):
            continue
        mapped_fact_count += 1
        target_predicate = relation_map.get(fact.predicate, fact.predicate)
        target_relation_type = relation_type_map.get(fact.relation_type, fact.relation_type)
        target_args = tuple(node_map[arg] for arg in fact.args)
        exact_key = (target_predicate, target_relation_type, target_args)
        if exact_key in target_fact_keys:
            continue
        # Distinguish semantic relation-type mismatch from absent relation.
        if any(
            pred == target_predicate and args == target_args and rtype != target_relation_type
            for pred, rtype, args in target_fact_keys
        ):
            relation_type_violations += 1
        else:
            relation_violations += 1

    invariant_violations = 0
    target_invariants = set(target.invariant_ids)
    for donor_invariant in donor.invariant_ids:
        if donor_invariant not in invariant_map:
            continue
        if invariant_map[donor_invariant] not in target_invariants:
            invariant_violations += 1

    relation_preservation_rate = (
        (mapped_fact_count - relation_violations - relation_type_violations)
        / mapped_fact_count
        if mapped_fact_count
        else 0.0
    )
    critical_valid = (
        type_violations == 0
        and relation_violations == 0
        and relation_type_violations == 0
        and invariant_violations == 0
        and mapped_fact_count > 0
    )
    return HomomorphismAssessment(
        mapped_node_count=len(node_map),
        mapped_fact_count=mapped_fact_count,
        type_violations=type_violations,
        relation_violations=relation_violations,
        relation_type_violations=relation_type_violations,
        invariant_violations=invariant_violations,
        relation_preservation_rate=relation_preservation_rate,
        critical_valid=critical_valid,
    )


@dataclass(frozen=True, slots=True)
class FormalContext:
    objects: tuple[str, ...]
    attributes: tuple[str, ...]
    incidence: frozenset[tuple[str, str]]

    def __post_init__(self) -> None:
        if len(self.objects) != len(set(self.objects)) or len(self.attributes) != len(set(self.attributes)):
            raise ValueError("objects and attributes must be unique")
        if any(g not in self.objects or m not in self.attributes for g, m in self.incidence):
            raise ValueError("incidence references unknown object or attribute")


def derive_attributes(context: FormalContext, objects: Iterable[str]) -> frozenset[str]:
    selected = frozenset(objects)
    if not selected:
        return frozenset(context.attributes)
    if not selected.issubset(context.objects):
        raise ValueError("unknown object")
    return frozenset(
        attribute
        for attribute in context.attributes
        if all((obj, attribute) in context.incidence for obj in selected)
    )


def derive_objects(context: FormalContext, attributes: Iterable[str]) -> frozenset[str]:
    selected = frozenset(attributes)
    if not selected:
        return frozenset(context.objects)
    if not selected.issubset(context.attributes):
        raise ValueError("unknown attribute")
    return frozenset(
        obj
        for obj in context.objects
        if all((obj, attribute) in context.incidence for attribute in selected)
    )


def formal_concept_closure(
    context: FormalContext,
    *,
    objects: Iterable[str] = (),
    attributes: Iterable[str] = (),
) -> tuple[frozenset[str], frozenset[str]]:
    """Return the FCA closure containing a supplied object or attribute seed."""

    object_seed = frozenset(objects)
    attribute_seed = frozenset(attributes)
    if object_seed and attribute_seed:
        raise ValueError("provide objects or attributes, not both")
    if object_seed:
        intent = derive_attributes(context, object_seed)
        extent = derive_objects(context, intent)
        return extent, intent
    intent_seed = attribute_seed
    extent = derive_objects(context, intent_seed)
    intent = derive_attributes(context, extent)
    return extent, intent


@dataclass(frozen=True, slots=True)
class FiniteCategory:
    objects: tuple[str, ...]
    morphisms: tuple[str, ...]
    source_target: tuple[tuple[str, str, str], ...]
    identities: tuple[tuple[str, str], ...]
    composition: tuple[tuple[str, str, str], ...]

    def __post_init__(self) -> None:
        if len(self.objects) != len(set(self.objects)) or len(self.morphisms) != len(set(self.morphisms)):
            raise ValueError("category objects and morphisms must be unique")
        st = {m: (s, t) for m, s, t in self.source_target}
        if set(st) != set(self.morphisms):
            raise ValueError("source_target must bind every morphism")
        if any(s not in self.objects or t not in self.objects for s, t in st.values()):
            raise ValueError("morphism endpoint references unknown object")
        identity_map = dict(self.identities)
        if set(identity_map) != set(self.objects):
            raise ValueError("identity must bind each object")
        if any(m not in self.morphisms for m in identity_map.values()):
            raise ValueError("identity references unknown morphism")
        if any(f not in self.morphisms or g not in self.morphisms or h not in self.morphisms for f, g, h in self.composition):
            raise ValueError("composition references unknown morphism")

    @property
    def endpoints(self) -> dict[str, tuple[str, str]]:
        return {m: (s, t) for m, s, t in self.source_target}

    @property
    def identity_map(self) -> dict[str, str]:
        return dict(self.identities)

    @property
    def compose(self) -> dict[tuple[str, str], str]:
        return {(f, g): h for f, g, h in self.composition}


@dataclass(frozen=True, slots=True)
class FunctorCandidate:
    object_map: tuple[tuple[str, str], ...]
    morphism_map: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class FunctorAssessment:
    endpoint_violations: int
    identity_violations: int
    composition_violations: int

    @property
    def valid(self) -> bool:
        return not (
            self.endpoint_violations
            or self.identity_violations
            or self.composition_violations
        )


def assess_functor(
    donor: FiniteCategory,
    target: FiniteCategory,
    candidate: FunctorCandidate,
) -> FunctorAssessment:
    """Check object/morphism, identity and composition preservation exactly."""

    object_map = dict(candidate.object_map)
    morphism_map = dict(candidate.morphism_map)
    if set(object_map) != set(donor.objects) or set(morphism_map) != set(donor.morphisms):
        raise ValueError("functor candidate must map all donor objects and morphisms")
    if not set(object_map.values()).issubset(target.objects) or not set(morphism_map.values()).issubset(target.morphisms):
        raise ValueError("functor candidate maps outside target category")

    endpoint_violations = 0
    for morphism, (source, dest) in donor.endpoints.items():
        mapped = morphism_map[morphism]
        target_source, target_dest = target.endpoints[mapped]
        if (target_source, target_dest) != (object_map[source], object_map[dest]):
            endpoint_violations += 1

    identity_violations = sum(
        morphism_map[donor.identity_map[obj]] != target.identity_map[object_map[obj]]
        for obj in donor.objects
    )

    composition_violations = 0
    for (f, g), h in donor.compose.items():
        mapped_pair = (morphism_map[f], morphism_map[g])
        if target.compose.get(mapped_pair) != morphism_map[h]:
            composition_violations += 1

    return FunctorAssessment(
        endpoint_violations=endpoint_violations,
        identity_violations=identity_violations,
        composition_violations=composition_violations,
    )


@dataclass(frozen=True, slots=True)
class TransformationCase:
    case_id: str
    original: object
    transformed: object
    transform_id: str


@dataclass(frozen=True, slots=True)
class InvarianceAssessment:
    total: int
    preserved: int
    violated_case_ids: tuple[str, ...]

    @property
    def rate(self) -> float:
        return self.preserved / self.total if self.total else 0.0


def assess_invariance(
    cases: Sequence[TransformationCase],
    judgment: Callable[[object], object],
    output_transform: Callable[[str, object], object] | None = None,
) -> InvarianceAssessment:
    """Check invariance or equivariance on an explicit transformation suite."""

    violations: list[str] = []
    for case in cases:
        expected = judgment(case.original)
        if output_transform is not None:
            expected = output_transform(case.transform_id, expected)
        if judgment(case.transformed) != expected:
            violations.append(case.case_id)
    return InvarianceAssessment(
        total=len(cases),
        preserved=len(cases) - len(violations),
        violated_case_ids=tuple(violations),
    )


@dataclass(frozen=True, slots=True)
class TransferValueProfile:
    hidden_target_quality: float
    remote_donor_recall: float
    false_analogy_rate: float
    native_fidelity: float
    old_case_retention: float
    formal_witness_rate: float
    resource_cost: float
    critical_failure: bool = False

    def __post_init__(self) -> None:
        for value in (
            self.hidden_target_quality,
            self.remote_donor_recall,
            self.false_analogy_rate,
            self.native_fidelity,
            self.old_case_retention,
            self.formal_witness_rate,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("quality coordinates must be in [0, 1]")
        if self.resource_cost < 0:
            raise ValueError("resource cost cannot be negative")

    def benefit_vector(self) -> tuple[float, ...]:
        return (
            self.hidden_target_quality,
            self.remote_donor_recall,
            1.0 - self.false_analogy_rate,
            self.native_fidelity,
            self.old_case_retention,
            self.formal_witness_rate,
            -self.resource_cost,
        )


def noncompensatory_dominates(
    challenger: TransferValueProfile,
    baseline: TransferValueProfile,
    *,
    tolerance: float = 0.0,
) -> bool:
    """Return Pareto dominance while preserving hard critical-failure gates."""

    if challenger.critical_failure and not baseline.critical_failure:
        return False
    left = challenger.benefit_vector()
    right = baseline.benefit_vector()
    no_worse = all(a + tolerance >= b for a, b in zip(left, right, strict=True))
    strictly_better = any(a > b + tolerance for a, b in zip(left, right, strict=True))
    return no_worse and strictly_better


def enumerate_type_respecting_node_maps(
    donor: FiniteRelationalStructure,
    target: FiniteRelationalStructure,
) -> tuple[tuple[tuple[str, str], ...], ...]:
    """Exact small-structure oracle helper used only for finite calibration tasks."""

    choices: list[tuple[str, ...]] = []
    for donor_node in donor.nodes:
        matching = tuple(
            target_node
            for target_node in target.nodes
            if target.types[target_node] == donor.types[donor_node]
        )
        if not matching:
            return ()
        choices.append(matching)
    maps: list[tuple[tuple[str, str], ...]] = []
    for values in product(*choices):
        if len(set(values)) != len(values):
            continue
        maps.append(tuple(zip(donor.nodes, values, strict=True)))
    return tuple(maps)
