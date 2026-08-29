from __future__ import annotations

from orion_v2.conceptual_development import (
    ConceptState,
    ConceptTransitionEvidence,
    ConceptTransitionKind,
    ConceptTransitionProposal,
    ConceptTransitionStatus,
    DomainStructure,
    TransferDiscoveryStatus,
    TransferEvidence,
    TransferHypothesis,
    assess_concept_transition,
    assess_transfer_hypothesis,
    discover_transfer_candidates,
    induce_relational_abstractions,
)


def _structure(identity: str, domain: str, surface: str) -> DomainStructure:
    return DomainStructure(
        structure_id=identity,
        domain_id=domain,
        source_ids=(f"source-{identity}",),
        relation_ids=("bounded-model-validity",),
        higher_order_relation_ids=("regime-selects-adequate-model",),
        invariant_ids=("retain-valid-local-judgments",),
        failure_topology_ids=("overgeneralization-breaks-hidden-case",),
        surface_tags=(surface,),
    )


def test_relational_abstraction_is_induced_from_cross_domain_structure() -> None:
    abstractions = induce_relational_abstractions(
        (
            _structure("a", "domain-a", "surface-alpha"),
            _structure("b", "domain-b", "surface-beta"),
        )
    )
    assert len(abstractions) == 1
    abstraction = abstractions[0]
    assert set(abstraction.support_domain_ids) == {"domain-a", "domain-b"}
    assert "REL:bounded-model-validity" in abstraction.feature_ids
    assert abstraction.surface_diversity_score == 1.0


def test_surface_similarity_without_relational_overlap_does_not_create_lesson() -> None:
    left = DomainStructure(
        "left",
        "domain-a",
        relation_ids=("relation-a",),
        higher_order_relation_ids=("higher-a",),
        surface_tags=("same-word",),
    )
    right = DomainStructure(
        "right",
        "domain-b",
        relation_ids=("relation-b",),
        higher_order_relation_ids=("higher-b",),
        surface_tags=("same-word",),
    )
    assert induce_relational_abstractions((left, right)) == ()


def test_discovery_retrieves_remote_donors_via_learned_abstraction() -> None:
    donors = (
        _structure("a", "domain-a", "surface-alpha"),
        _structure("b", "domain-b", "surface-beta"),
    )
    abstraction = induce_relational_abstractions(donors)
    target = _structure("target", "domain-c", "surface-gamma")
    candidates = discover_transfer_candidates(target, (*donors, target), abstraction)
    assert len(candidates) == 1
    candidate = candidates[0]
    assert set(candidate.donor_structure_ids) == {"a", "b"}
    assert candidate.structural_coverage == 1.0
    assert candidate.max_surface_similarity == 0.0
    assert candidate.remote_transfer_score == 1.0


def _hypothesis() -> TransferHypothesis:
    return TransferHypothesis(
        hypothesis_id="h1",
        candidate_id="candidate-1",
        mapped_relation_ids=("map-1",),
        predicted_target_consequence_ids=("hidden-decision-1",),
        prohibited_transfer_ids=("do-not-copy-domain-object",),
        falsifier_ids=("counterexample-1",),
    )


def test_transfer_is_rejected_when_decoy_control_exposes_false_analogy() -> None:
    receipt = assess_transfer_hypothesis(
        _hypothesis(),
        TransferEvidence(
            donor_native_recovery_pass=True,
            target_prediction_frozen_pre_outcome=True,
            hidden_target_discrimination_pass=True,
            negative_decoy_rejection_pass=False,
            countertransfer_challenge_pass=True,
            parent_control_executed=True,
            parent_control_sufficient=False,
            resource_accounted=True,
        ),
    )
    assert receipt.status is TransferDiscoveryStatus.FALSE_ANALOGY_REJECTED
    assert not receipt.scientific_truth_authorized


def test_parent_sufficiency_is_a_valid_transfer_terminal() -> None:
    receipt = assess_transfer_hypothesis(
        _hypothesis(),
        TransferEvidence(
            donor_native_recovery_pass=True,
            target_prediction_frozen_pre_outcome=True,
            hidden_target_discrimination_pass=True,
            negative_decoy_rejection_pass=True,
            countertransfer_challenge_pass=True,
            parent_control_executed=True,
            parent_control_sufficient=True,
            resource_accounted=True,
        ),
    )
    assert receipt.status is TransferDiscoveryStatus.PARENT_SUFFICIENT


def test_discovered_transfer_can_reach_protected_residual_without_granting_truth() -> None:
    receipt = assess_transfer_hypothesis(
        _hypothesis(),
        TransferEvidence(
            donor_native_recovery_pass=True,
            target_prediction_frozen_pre_outcome=True,
            hidden_target_discrimination_pass=True,
            negative_decoy_rejection_pass=True,
            countertransfer_challenge_pass=True,
            parent_control_executed=True,
            parent_control_sufficient=False,
            resource_accounted=True,
        ),
    )
    assert receipt.status is TransferDiscoveryStatus.PROTECTED_TRANSFER_RESIDUAL
    assert not receipt.scientific_truth_authorized
    assert not receipt.adoption_authorized


def _concept(version: int = 1) -> ConceptState:
    return ConceptState(
        concept_id="concept-x",
        version=version,
        relation_ids=("relation-1",),
        scope_condition_ids=("scope-1",),
        operational_link_ids=("measurement-1",),
        invariant_ids=("invariant-1",),
        exemplar_ids=("example-1",),
        counterexample_ids=("counterexample-1",),
        parent_concept_ids=("parent-1",),
        authority_ceiling=1,
    )


def _proposal(after: ConceptState) -> ConceptTransitionProposal:
    return ConceptTransitionProposal(
        transition_id="transition-1",
        kind=ConceptTransitionKind.REVISE,
        before_concept_id="concept-x",
        before_version=1,
        after=after,
        trigger_ids=("anomaly-1",),
        predicted_decision_ids=("decision-1",),
        predicted_hidden_case_ids=("hidden-1",),
        falsifier_ids=("falsifier-1",),
        loss_ids=("loss-audit-1",),
        requested_authority_level=1,
    )


def test_conceptual_transition_requires_explicit_loss_audit() -> None:
    receipt = assess_concept_transition(
        _concept(),
        _proposal(_concept(version=2)),
        ConceptTransitionEvidence(
            parent_recovery_pass=True,
            native_fidelity_pass=True,
            old_valid_cases_retained=True,
            scope_explicit=True,
            loss_audited=False,
            measurement_links_valid=True,
            authority_valid=True,
            prediction_or_decision_changed=True,
            formal_necessity=False,
            hidden_case_pass=True,
        ),
    )
    assert receipt.status is ConceptTransitionStatus.BLOCKED_SCOPE_OR_LOSS_AUDIT


def test_vocabulary_only_change_has_no_scientific_residual() -> None:
    receipt = assess_concept_transition(
        _concept(),
        _proposal(_concept(version=2)),
        ConceptTransitionEvidence(
            parent_recovery_pass=True,
            native_fidelity_pass=True,
            old_valid_cases_retained=True,
            scope_explicit=True,
            loss_audited=True,
            measurement_links_valid=True,
            authority_valid=True,
            prediction_or_decision_changed=False,
            formal_necessity=False,
            hidden_case_pass=True,
        ),
    )
    assert receipt.status is ConceptTransitionStatus.NO_SCIENTIFIC_RESIDUAL


def test_operationalized_concept_transition_waits_for_hidden_evidence() -> None:
    receipt = assess_concept_transition(
        _concept(),
        _proposal(_concept(version=2)),
        ConceptTransitionEvidence(
            parent_recovery_pass=True,
            native_fidelity_pass=True,
            old_valid_cases_retained=True,
            scope_explicit=True,
            loss_audited=True,
            measurement_links_valid=True,
            authority_valid=True,
            prediction_or_decision_changed=True,
            formal_necessity=False,
            hidden_case_pass=None,
        ),
    )
    assert receipt.status is ConceptTransitionStatus.READY_FOR_PROTECTED_EVALUATION


def test_hidden_case_success_can_support_bounded_conceptual_residual() -> None:
    receipt = assess_concept_transition(
        _concept(),
        _proposal(_concept(version=2)),
        ConceptTransitionEvidence(
            parent_recovery_pass=True,
            native_fidelity_pass=True,
            old_valid_cases_retained=True,
            scope_explicit=True,
            loss_audited=True,
            measurement_links_valid=True,
            authority_valid=True,
            prediction_or_decision_changed=True,
            formal_necessity=False,
            hidden_case_pass=True,
            independent_adjudication_complete=True,
        ),
    )
    assert (
        receipt.status
        is ConceptTransitionStatus.INDEPENDENTLY_ADJUDICATED_CONCEPTUAL_RESIDUAL
    )
    assert not receipt.foundation_status_authorized
