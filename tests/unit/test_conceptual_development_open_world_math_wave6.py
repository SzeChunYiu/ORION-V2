from __future__ import annotations

from orion_v2.conceptual_development import (
    DomainStructure,
    discover_transfer_candidates,
    induce_relational_abstractions,
)


def structure(structure_id: str, domain_id: str, surface: str) -> DomainStructure:
    return DomainStructure(
        structure_id=structure_id,
        domain_id=domain_id,
        source_ids=(f"source:{structure_id}",),
        native_parent_ids=(f"parent:{domain_id}",),
        relation_ids=("structure_preserving_map",),
        invariant_ids=("decision_relevant_invariant",),
        transformation_ids=("allowed_representation_change",),
        surface_tags=(surface,),
    )


def test_mathematics_and_arbitrary_sciences_share_same_open_world_interface() -> None:
    donors = (
        structure("algebra-case", "pure_mathematics_algebra", "group"),
        structure("topology-case", "pure_mathematics_topology", "homotopy"),
        structure("chemistry-case", "chemistry", "molecule"),
        structure("biology-case", "evolutionary_biology", "population"),
    )
    abstractions = induce_relational_abstractions(
        donors,
        minimum_support_domains=3,
        minimum_feature_count=3,
        maximum_pairwise_surface_similarity=0.0,
    )
    assert abstractions
    assert {"pure_mathematics_algebra", "pure_mathematics_topology"}.issubset(
        set(abstractions[0].support_domain_ids)
    )
    assert {"chemistry", "evolutionary_biology"}.issubset(
        set(abstractions[0].support_domain_ids)
    )


def test_remote_target_can_be_new_domain_not_named_by_framework() -> None:
    donors = (
        structure("number-theory-case", "pure_mathematics_number_theory", "prime"),
        structure("control-case", "control_engineering", "controller"),
        structure("climate-case", "climate_science", "circulation"),
    )
    abstractions = induce_relational_abstractions(
        donors,
        minimum_support_domains=3,
        minimum_feature_count=3,
        maximum_pairwise_surface_similarity=0.0,
    )
    target = structure("new-domain-case", "future_science_not_in_any_allowlist", "novel-object")
    candidates = discover_transfer_candidates(target, donors, abstractions)
    assert candidates
    assert candidates[0].structural_coverage == 1.0
    assert candidates[0].max_surface_similarity == 0.0
    assert set(candidates[0].donor_structure_ids) == {
        "number-theory-case",
        "control-case",
        "climate-case",
    }


def test_surface_vocabulary_does_not_create_structure_by_itself() -> None:
    left = DomainStructure(
        structure_id="math-surface",
        domain_id="mathematics",
        relation_ids=("formal_relation",),
        surface_tags=("network",),
    )
    right = DomainStructure(
        structure_id="biology-surface",
        domain_id="biology",
        relation_ids=("different_relation",),
        surface_tags=("network",),
    )
    abstractions = induce_relational_abstractions(
        (left, right),
        minimum_support_domains=2,
        minimum_feature_count=2,
    )
    assert abstractions == ()
