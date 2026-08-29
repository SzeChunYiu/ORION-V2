from __future__ import annotations

from orion_v2.donors import DomainProblem, DonorReductionCase
from orion_v2.knowledge_metabolism import (
    KnowledgeKind,
    MetabolicContract,
    MetabolicStage,
    MetabolicStatus,
    RawKnowledgeUnit,
    RecombinationProposal,
    SourceFragment,
    decompose_and_sort_sources,
    run_knowledge_metabolism,
)
from orion_v2.native_recovery import NativeRecoveryCase


def _problem() -> DomainProblem:
    return DomainProblem(
        problem_id="parent-problem",
        domain_id="parent-domain",
        native_problem="recover a typed scientific decision",
        source_ids=("source-parent",),
        object_types=("claim",),
        state_types=("open", "resolved"),
        operation_types=("test",),
        native_judgment_ids=("judgment-native",),
        assumption_ids=("assumption-a",),
    )


def _fragments(*, permission: bool = True) -> tuple[SourceFragment, ...]:
    permission_id = "permission-a" if permission else ""
    first = SourceFragment(
        fragment_id="fragment-a",
        source_id="source-a",
        source_mode="paper",
        content_digest="digest-a",
        authority_ceiling=2,
        custody_id="custody-a",
        licence_or_permission_id=permission_id,
        units=(
            RawKnowledgeUnit(
                "unit-a-claim",
                KnowledgeKind.CLAIM,
                "The intervention changes the measured state.",
                native_term_ids=("intervention",),
                assumption_ids=("assumption-a",),
                counterexample_ids=("counterexample-a",),
            ),
            RawKnowledgeUnit(
                "unit-a-method",
                KnowledgeKind.METHOD,
                "Use a discriminating intervention.",
                native_term_ids=("intervention",),
                assumption_ids=("assumption-a",),
            ),
        ),
    )
    second = SourceFragment(
        fragment_id="fragment-b",
        source_id="source-b",
        source_mode="incident-record",
        content_digest="digest-b",
        authority_ceiling=1,
        units=(
            RawKnowledgeUnit(
                "unit-b-claim",
                KnowledgeKind.CLAIM,
                "  the intervention CHANGES the measured state. ",
                native_term_ids=("intervention",),
                assumption_ids=("assumption-a",),
                dependence_ids=("shared-instrument",),
            ),
            RawKnowledgeUnit(
                "unit-b-failure",
                KnowledgeKind.FAILURE_LESSON,
                "A shared instrument can create false corroboration.",
                assumption_ids=("assumption-a",),
                counterexample_ids=("counterexample-b",),
            ),
        ),
    )
    return first, second


def _recovery(*, preserve_assumption: bool = True) -> tuple[NativeRecoveryCase, ...]:
    return (
        NativeRecoveryCase(
            case_id="recovery-a",
            domain_id="parent-domain",
            theory_family_id="parent-family",
            native_judgment="native-ok",
            generalized_judgment="general-ok",
            native_to_generalized={"native-ok": "general-ok"},
            native_assumption_ids=("assumption-a",),
            mapped_assumption_ids=("assumption-a",) if preserve_assumption else (),
            native_counterexample_ids=("counterexample-a",),
            reflected_counterexample_ids=("counterexample-a",),
            source_ids=("source-parent",),
        ),
    )


def _donor_case(kind: str) -> DonorReductionCase:
    common = dict(
        case_id=f"donor-{kind}",
        candidate_id="candidate-a",
        donor_problems=(_problem(),),
        reconstruction_receipt_ids=("reconstruction-a",),
        mapping_ids=("mapping-a",),
        preserved_native_judgment_ids=("judgment-native",),
    )
    if kind == "parent":
        return DonorReductionCase(**common)
    if kind == "strict":
        return DonorReductionCase(
            **common,
            added_coordinate_ids=("bridge-coordinate",),
            strict_witness_ids=("strict-witness",),
            strongest_product_test_ids=("parent-product-test",),
            strongest_product_ties=False,
            falsifier_ids=("falsifier-a",),
        )
    if kind == "refuted":
        return DonorReductionCase(
            **common,
            parent_refutation_ids=("parent-refutation",),
        )
    raise ValueError(kind)


def _contract() -> MetabolicContract:
    return MetabolicContract(
        contract_id="contract-a",
        problem_id="problem-a",
        comparison_identity="comparison-a",
        registered_decision_ids=("decision-a",),
        required_source_modes=("paper", "incident-record"),
        required_knowledge_kinds=(KnowledgeKind.CLAIM, KnowledgeKind.METHOD),
        maximum_authority_level=1,
    )


def _proposal(fragments: tuple[SourceFragment, ...], **overrides: object) -> RecombinationProposal:
    atoms = decompose_and_sort_sources(fragments)
    claim_atom = next(atom.atom_id for atom in atoms if atom.kind is KnowledgeKind.CLAIM)
    method_atom = next(atom.atom_id for atom in atoms if atom.kind is KnowledgeKind.METHOD)
    values: dict[str, object] = {
        "proposal_id": "proposal-a",
        "statement": "Combine a source-bound claim with a discriminating method.",
        "atom_ids": (claim_atom, method_atom),
        "bridge_relation_ids": ("bridge-a",),
        "intended_decision_ids": ("decision-a",),
        "discriminator_ids": ("discriminator-a",),
        "falsifier_ids": ("falsifier-a",),
        "requested_authority_level": 1,
    }
    values.update(overrides)
    return RecombinationProposal(**values)


def test_decomposition_merges_equivalent_content_without_erasing_provenance() -> None:
    atoms = decompose_and_sort_sources(_fragments())
    claim = next(atom for atom in atoms if atom.kind is KnowledgeKind.CLAIM)
    assert claim.source_ids == ("source-a", "source-b")
    assert claim.fragment_ids == ("fragment-a", "fragment-b")
    assert claim.authority_ceiling == 1
    assert claim.counterexample_ids == ("counterexample-a",)
    assert claim.dependence_ids == ("shared-instrument",)


def test_parent_owned_solution_is_absorbed_without_false_novelty() -> None:
    fragments = _fragments()
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("parent"),
        _recovery(),
        _proposal(fragments),
    )
    assert result.status is MetabolicStatus.PARENT_ASSIMILATION_READY
    assert MetabolicStage.ASSIMILATE in result.completed_stages
    assert not result.scientific_truth_authorized
    assert not result.novelty_authorized
    assert not result.adoption_authorized


def test_strict_residual_requires_protected_evaluation() -> None:
    fragments = _fragments()
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("strict"),
        _recovery(),
        _proposal(fragments),
    )
    assert result.status is MetabolicStatus.STRICT_RESIDUAL_READY_FOR_PROTECTED_EVALUATION
    assert result.assimilated_atom_ids
    assert result.recycled_atom_ids
    assert not result.adoption_authorized


def test_parent_refutation_is_recycled_as_negative_knowledge() -> None:
    fragments = _fragments()
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("refuted"),
        _recovery(),
        _proposal(fragments),
    )
    assert result.status is MetabolicStatus.PARENT_REFUTATION_RECYCLED
    assert result.recycled_atom_ids == result.atom_ids
    assert MetabolicStage.RECYCLE in result.completed_stages


def test_native_assumption_erasure_blocks_absorption() -> None:
    fragments = _fragments()
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("strict"),
        _recovery(preserve_assumption=False),
        _proposal(fragments),
    )
    assert result.status is MetabolicStatus.BLOCKED_NATIVE_RECOVERY


def test_missing_discriminator_or_falsifier_blocks_recombination_claim() -> None:
    fragments = _fragments()
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("strict"),
        _recovery(),
        _proposal(fragments, discriminator_ids=(), falsifier_ids=()),
    )
    assert result.status is MetabolicStatus.BLOCKED_CHALLENGE


def test_authority_cannot_exceed_weakest_absorbed_source() -> None:
    fragments = _fragments()
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("strict"),
        _recovery(),
        _proposal(fragments, requested_authority_level=2),
    )
    assert result.status is MetabolicStatus.BLOCKED_AUTHORITY


def test_unresolved_custody_blocks_ingestion() -> None:
    fragments = _fragments(permission=False)
    result = run_knowledge_metabolism(
        _contract(),
        fragments,
        _donor_case("strict"),
        _recovery(),
        _proposal(fragments),
    )
    assert result.status is MetabolicStatus.BLOCKED_SOURCE_CUSTODY
