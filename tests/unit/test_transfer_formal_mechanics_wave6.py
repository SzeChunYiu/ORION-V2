from __future__ import annotations

from orion_v2.transfer_formal_mechanics import (
    FiniteCategory,
    FiniteRelationalStructure,
    FormalContext,
    FormalTransferMap,
    FunctorCandidate,
    TransferValueProfile,
    TransformationCase,
    TypedFact,
    assess_functor,
    assess_invariance,
    assess_partial_homomorphism,
    enumerate_type_respecting_node_maps,
    formal_concept_closure,
    noncompensatory_dominates,
)


def test_partial_homomorphism_supports_cross_domain_relation_renaming() -> None:
    donor = FiniteRelationalStructure(
        "math-poset", "pure-math",
        ("a", "b"), (("a", "state"), ("b", "state")),
        (TypedFact("precedes", "ORDER", ("a", "b")),),
        ("acyclic",),
    )
    target = FiniteRelationalStructure(
        "science-causal", "experimental-science",
        ("x", "y"), (("x", "state"), ("y", "state")),
        (TypedFact("before_intervention", "ORDER", ("x", "y")),),
        ("no-cycle",),
    )
    mapping = FormalTransferMap(
        (("a", "x"), ("b", "y")),
        (("precedes", "before_intervention"),),
        invariant_map=(("acyclic", "no-cycle"),),
    )
    result = assess_partial_homomorphism(donor, target, mapping)
    assert result.critical_valid
    assert result.relation_preservation_rate == 1.0


def test_false_analogy_is_rejected_when_direction_relation_missing() -> None:
    donor = FiniteRelationalStructure(
        "d", "domain-a", ("a", "b"), (("a", "node"), ("b", "node")),
        (TypedFact("causes", "DIRECTED", ("a", "b")),),
    )
    target = FiniteRelationalStructure(
        "t", "domain-b", ("x", "y"), (("x", "node"), ("y", "node")),
        (TypedFact("causes", "DIRECTED", ("y", "x")),),
    )
    result = assess_partial_homomorphism(
        donor, target, FormalTransferMap((("a", "x"), ("b", "y")), ()),
    )
    assert not result.critical_valid
    assert result.relation_violations == 1


def test_exact_type_respecting_oracle_enumerates_bijections() -> None:
    donor = FiniteRelationalStructure(
        "d", "math", ("a", "b"), (("a", "v"), ("b", "v")), ()
    )
    target = FiniteRelationalStructure(
        "t", "chemistry", ("x", "y", "z"),
        (("x", "v"), ("y", "v"), ("z", "other")), ()
    )
    maps = enumerate_type_respecting_node_maps(donor, target)
    assert len(maps) == 2
    assert all({dest for _, dest in mapping} == {"x", "y"} for mapping in maps)


def test_formal_concept_analysis_closure_is_exact() -> None:
    context = FormalContext(
        objects=("g1", "g2", "g3"),
        attributes=("m1", "m2"),
        incidence=frozenset({
            ("g1", "m1"), ("g1", "m2"),
            ("g2", "m1"),
            ("g3", "m2"),
        }),
    )
    extent, intent = formal_concept_closure(context, objects=("g1", "g2"))
    assert extent == frozenset({"g1", "g2"})
    assert intent == frozenset({"m1"})


def _walking_arrow(prefix: str) -> FiniteCategory:
    a, b = f"{prefix}A", f"{prefix}B"
    ida, idb, f = f"id{prefix}A", f"id{prefix}B", f"{prefix}f"
    return FiniteCategory(
        objects=(a, b),
        morphisms=(ida, idb, f),
        source_target=((ida, a, a), (idb, b, b), (f, a, b)),
        identities=((a, ida), (b, idb)),
        composition=(
            (ida, ida, ida), (idb, idb, idb),
            (ida, f, f), (f, idb, f),
        ),
    )


def test_functoriality_checks_identity_and_composition() -> None:
    donor = _walking_arrow("D")
    target = _walking_arrow("T")
    good = FunctorCandidate(
        (("DA", "TA"), ("DB", "TB")),
        (("idDA", "idTA"), ("idDB", "idTB"), ("Df", "Tf")),
    )
    assert assess_functor(donor, target, good).valid

    bad = FunctorCandidate(
        (("DA", "TA"), ("DB", "TB")),
        (("idDA", "idTA"), ("idDB", "idTB"), ("Df", "idTA")),
    )
    result = assess_functor(donor, target, bad)
    assert not result.valid
    assert result.endpoint_violations >= 1


def test_invariance_and_equivariance_use_hidden_transformations() -> None:
    cases = (
        TransformationCase("c1", (1, 2), (2, 1), "swap"),
        TransformationCase("c2", (3, 5), (5, 3), "swap"),
    )
    invariant = assess_invariance(cases, lambda x: sum(x))
    assert invariant.rate == 1.0

    equivariant = assess_invariance(
        cases,
        lambda x: x[0] - x[1],
        output_transform=lambda transform, y: -y if transform == "swap" else y,
    )
    assert equivariant.rate == 1.0


def test_pareto_dominance_cannot_buy_critical_failure() -> None:
    baseline = TransferValueProfile(0.7, 0.6, 0.1, 0.95, 1.0, 0.8, 10.0)
    better = TransferValueProfile(0.8, 0.7, 0.05, 0.96, 1.0, 0.9, 9.0)
    assert noncompensatory_dominates(better, baseline)

    unsafe = TransferValueProfile(1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, critical_failure=True)
    assert not noncompensatory_dominates(unsafe, baseline)
