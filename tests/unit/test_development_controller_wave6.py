from orion_v2.development_controller import (
    DevelopmentMode,
    DevelopmentModeProposal,
    FrameworkLayer,
    FrameworkMemoryLedger,
    MemoryKind,
    ModeAssessmentContext,
    ModeAssessmentStatus,
    ModeWitnessBundle,
    RegisteredAlternative,
    assess_mode_proposal,
    framework_layers,
)


def proposal(mode, *, cost=5.0, frozen=True):
    return DevelopmentModeProposal(
        proposal_id=f"p-{mode}",
        episode_id="episode-1",
        mode=mode,
        target_obligation_ids=("ob-1",),
        prospective_identity_frozen=frozen,
        expected_resource_cost=cost,
    )


def test_framework_layers_cover_recursive_hierarchy():
    layers = framework_layers()
    assert layers[0] is FrameworkLayer.SCIENTIFIC_EPISODE
    assert layers[-1] is FrameworkLayer.RECURSIVE_PRINCIPLE
    assert len(layers) == 9


def test_transfer_blocked_while_cheaper_parent_unresolved():
    context = ModeAssessmentContext(
        alternatives=(RegisteredAlternative("parent", DevelopmentMode.STRONGEST_PARENT, 1.0, False, None),),
        witnesses=ModeWitnessBundle(donor_candidate_ids=("d",), negative_transfer_probe_ids=("n",)),
        authority_ceiling=1,
        resource_budget=10,
    )
    assert assess_mode_proposal(proposal(DevelopmentMode.TRANSFER_DISCOVERY), context).status is ModeAssessmentStatus.BLOCKED_UNRESOLVED_CHEAPER_ALTERNATIVE


def test_parent_sufficiency_blocks_formalism_invention():
    context = ModeAssessmentContext(
        alternatives=(
            RegisteredAlternative("parent", DevelopmentMode.STRONGEST_PARENT, 1.0, True, True),
            RegisteredAlternative("data", DevelopmentMode.EMPIRICAL_EXPANSION, 2.0, True, False),
        ),
        witnesses=ModeWitnessBundle(
            representational_deficit_witness_ids=("collision",),
            semantic_validation_plan_ids=("model",),
            predecessor_recovery_plan_ids=("recover",),
            counterexample_or_obstruction_ids=("counter",),
        ),
        authority_ceiling=1,
        resource_budget=10,
    )
    assert assess_mode_proposal(proposal(DevelopmentMode.FORMALISM_GENESIS), context).status is ModeAssessmentStatus.SIMPLE_OR_PARENT_SUFFICIENT


def test_formalism_genesis_requires_parent_and_data_controls():
    context = ModeAssessmentContext(
        alternatives=(),
        witnesses=ModeWitnessBundle(
            representational_deficit_witness_ids=("collision",),
            semantic_validation_plan_ids=("model",),
            predecessor_recovery_plan_ids=("recover",),
            counterexample_or_obstruction_ids=("counter",),
        ),
        authority_ceiling=1,
        resource_budget=10,
    )
    assert assess_mode_proposal(proposal(DevelopmentMode.FORMALISM_GENESIS), context).status is ModeAssessmentStatus.CANNOT_CHECK


def test_formalism_genesis_admissible_after_lower_cost_alternatives_fail():
    context = ModeAssessmentContext(
        alternatives=(
            RegisteredAlternative("parent", DevelopmentMode.STRONGEST_PARENT, 1.0, True, False),
            RegisteredAlternative("data", DevelopmentMode.EMPIRICAL_EXPANSION, 2.0, True, False),
        ),
        witnesses=ModeWitnessBundle(
            representational_deficit_witness_ids=("collision",),
            semantic_validation_plan_ids=("model",),
            predecessor_recovery_plan_ids=("recover",),
            counterexample_or_obstruction_ids=("counter",),
        ),
        authority_ceiling=1,
        resource_budget=10,
    )
    assert assess_mode_proposal(proposal(DevelopmentMode.FORMALISM_GENESIS), context).status is ModeAssessmentStatus.ADMISSIBLE


def test_recursive_meta_requires_population_and_saturation():
    context = ModeAssessmentContext(
        alternatives=(),
        witnesses=ModeWitnessBundle(population_episode_ids=("e1", "e2"), heldout_route_ids=("field",)),
        authority_ceiling=1,
        resource_budget=10,
    )
    assert assess_mode_proposal(proposal(DevelopmentMode.RECURSIVE_META_LEARNING), context).status is ModeAssessmentStatus.BLOCKED_MISSING_MODE_WITNESS


def test_recursive_meta_admissible_with_lower_level_terminal():
    context = ModeAssessmentContext(
        alternatives=(),
        witnesses=ModeWitnessBundle(
            population_episode_ids=("e1", "e2"),
            lower_level_saturation_receipt_ids=("sat-1",),
            heldout_route_ids=("field", "epoch"),
        ),
        authority_ceiling=1,
        resource_budget=10,
    )
    assert assess_mode_proposal(proposal(DevelopmentMode.RECURSIVE_META_LEARNING), context).status is ModeAssessmentStatus.ADMISSIBLE


def test_unfrozen_constructive_mode_is_rejected():
    context = ModeAssessmentContext(alternatives=(), witnesses=ModeWitnessBundle(native_parent_ids=("p",)), authority_ceiling=1, resource_budget=10)
    assert assess_mode_proposal(proposal(DevelopmentMode.NATIVE_DIRECT, frozen=False), context).status is ModeAssessmentStatus.BLOCKED_UNFROZEN_PROSPECTIVE_IDENTITY


def test_safe_abstain_does_not_require_prospective_identity():
    context = ModeAssessmentContext(alternatives=(), witnesses=ModeWitnessBundle(), authority_ceiling=0, resource_budget=0)
    assert assess_mode_proposal(proposal(DevelopmentMode.ABSTAIN, cost=0, frozen=False), context).status is ModeAssessmentStatus.SAFE_ABSTAIN


def test_memory_ledger_is_append_only_and_source_bound():
    ledger = FrameworkMemoryLedger().append(
        entry_id="k1", kind=MemoryKind.KNOWLEDGE, source_ids=("source-1",), predecessor_entry_ids=(), scope_ids=("domain-a",), disposition="RETAIN", payload="alpha"
    )
    ledger = ledger.append(
        entry_id="f1", kind=MemoryKind.FAILURE, source_ids=("source-2",), predecessor_entry_ids=("k1",), scope_ids=("domain-a",), disposition="NEGATIVE_TRANSFER", payload="beta", reopen_condition_ids=("new-evidence",)
    )
    assert len(ledger.entries) == 2
    assert ledger.entries[1].predecessor_entry_ids == ("k1",)
    assert ledger.entries[1].payload_digest != ledger.entries[0].payload_digest
