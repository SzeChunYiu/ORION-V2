from orion_v2.formalism_genesis import (
    DistinctionCase,
    FormalismCandidate,
    FormalismGenesisEvidence,
    FormalismGenesisStatus,
    assess_formalism_candidate,
    minimal_discriminating_feature_sets,
    representation_collisions,
)


def _candidate() -> FormalismCandidate:
    return FormalismCandidate(
        formalism_id="candidate-v1",
        parent_formalism_ids=("parent",),
        primitive_ids=("scope-coordinate",),
        relation_ids=("depends-on",),
        operation_ids=("compose",),
        axiom_ids=("typed-composition",),
        semantic_model_ids=("finite-model-1",),
        recovery_map_ids=("recover-parent",),
        proof_or_derivation_rule_ids=("rule-1",),
        intended_deficit_ids=("collision-1",),
        prospective_consequence_ids=("hidden-decision-1",),
    )


def _good_evidence(**changes) -> FormalismGenesisEvidence:
    values = dict(
        registered_deficit_present=True,
        strongest_parent_executed=True,
        strongest_parent_sufficient=False,
        expressibility_or_collision_reduction_pass=True,
        semantic_model_witness_pass=True,
        consistency_or_model_check_pass=True,
        parent_recovery_pass=True,
        old_valid_case_retention_pass=True,
        prospective_new_consequence_pass=True,
        hidden_problem_success_pass=True,
        minimality_or_simpler_patch_check_pass=True,
        resource_accounted=True,
        independent_formal_check_complete=False,
    )
    values.update(changes)
    return FormalismGenesisEvidence(**values)


def test_representation_collision_exposes_missing_distinction() -> None:
    cases = (
        DistinctionCase("a", ("same-state",), "accept", (("scope", "local"), ("colour", "red"))),
        DistinctionCase("b", ("same-state",), "reject", (("scope", "remote"), ("colour", "red"))),
    )
    collisions = representation_collisions(cases)
    assert len(collisions) == 1
    assert collisions[0].separating_feature_ids == ("scope",)
    assert minimal_discriminating_feature_sets(cases) == (("scope",),)


def test_multiple_collisions_yield_minimum_hitting_set() -> None:
    cases = (
        DistinctionCase("a", ("s",), "d1", (("p", "0"), ("q", "0"))),
        DistinctionCase("b", ("s",), "d2", (("p", "1"), ("q", "0"))),
        DistinctionCase("c", ("s",), "d3", (("p", "0"), ("q", "1"))),
    )
    assert minimal_discriminating_feature_sets(cases) == (("p", "q"),)


def test_unsplittable_collision_is_not_magically_repaired() -> None:
    cases = (
        DistinctionCase("a", ("same",), "yes", (("x", "0"),)),
        DistinctionCase("b", ("same",), "no", (("x", "0"),)),
    )
    assert representation_collisions(cases)
    assert minimal_discriminating_feature_sets(cases) == ()


def test_parent_sufficiency_blocks_new_formalism_credit() -> None:
    receipt = assess_formalism_candidate(_candidate(), _good_evidence(strongest_parent_sufficient=True))
    assert receipt.status is FormalismGenesisStatus.PARENT_SUFFICIENT


def test_new_symbols_without_semantics_fail_closed() -> None:
    candidate = FormalismCandidate(
        formalism_id="symbols-only",
        parent_formalism_ids=("parent",),
        primitive_ids=("new-symbol",),
        relation_ids=(),
        operation_ids=(),
        axiom_ids=(),
        semantic_model_ids=(),
        recovery_map_ids=(),
        proof_or_derivation_rule_ids=(),
        intended_deficit_ids=("d",),
        prospective_consequence_ids=(),
    )
    receipt = assess_formalism_candidate(candidate, _good_evidence())
    assert receipt.status is FormalismGenesisStatus.BLOCKED_NO_SEMANTICS


def test_old_valid_case_loss_blocks_promotion() -> None:
    receipt = assess_formalism_candidate(_candidate(), _good_evidence(old_valid_case_retention_pass=False))
    assert receipt.status is FormalismGenesisStatus.BLOCKED_OLD_CASE_RETENTION


def test_simpler_patch_removes_formalism_residual() -> None:
    receipt = assess_formalism_candidate(
        _candidate(), _good_evidence(minimality_or_simpler_patch_check_pass=False)
    )
    assert receipt.status is FormalismGenesisStatus.NO_GENERATIVE_RESIDUAL


def test_protected_residual_requires_hidden_generativity() -> None:
    receipt = assess_formalism_candidate(_candidate(), _good_evidence())
    assert receipt.status is FormalismGenesisStatus.PROTECTED_FORMALISM_RESIDUAL
    assert receipt.scientific_truth_authorized is False
    assert receipt.foundation_status_authorized is False
    assert receipt.adoption_authorized is False
