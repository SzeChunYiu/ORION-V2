from orion_v2.human_epistemics_social import (
    CounterfactualProposal,
    CounterfactualStatus,
    IncubationReceipt,
    IncubationStatus,
    MemoryRevisionReceipt,
    MemoryRevisionStatus,
    ObserverCouplingReceipt,
    ObserverCouplingStatus,
    PanelIndependenceStatus,
    PedagogicalSampleReceipt,
    PedagogicalStatus,
    PolicyHabitReceipt,
    PolicyHabitStatus,
    ReviewerJudgment,
    ReviewStage,
    TeachingScope,
    assess_counterfactual,
    assess_incubation,
    assess_memory_revision,
    assess_observer_coupling,
    assess_panel_independence,
    assess_pedagogical_sample,
    assess_policy_habit,
)


def test_nonexhaustive_teaching_can_preserve_exploration() -> None:
    receipt = PedagogicalSampleReceipt(
        "sample", "teacher", frozenset({"a"}), frozenset({"a", "b"}),
        TeachingScope.NONEXHAUSTIVE,
    )
    result = assess_pedagogical_sample(receipt, frozenset({"a", "b"}))
    assert result.status is PedagogicalStatus.EXPLORATION_PRESERVED
    assert not result.claim_authorized and not result.authority_granted


def test_nonexhaustive_teaching_can_suppress_hidden_valid_alternative() -> None:
    receipt = PedagogicalSampleReceipt(
        "sample", "teacher", frozenset({"a"}), frozenset({"a", "b"}),
        TeachingScope.NONEXHAUSTIVE,
    )
    result = assess_pedagogical_sample(receipt, frozenset({"a"}))
    assert result.status is PedagogicalStatus.INSTRUCTION_INDUCED_SEARCH_SUPPRESSION
    assert result.hidden_valid_items == ("b",)


def test_false_exhaustive_teaching_scope_is_contradicted() -> None:
    receipt = PedagogicalSampleReceipt(
        "sample", "teacher", frozenset({"a"}), frozenset({"a", "b"}),
        TeachingScope.EXHAUSTIVE,
    )
    assert (
        assess_pedagogical_sample(receipt, frozenset({"a"})).status
        is PedagogicalStatus.EXHAUSTIVE_SCOPE_CONTRADICTED
    )


def test_safety_bounded_teaching_restricts_only_unauthorized_exploration() -> None:
    receipt = PedagogicalSampleReceipt(
        "sample", "teacher", frozenset({"safe"}),
        frozenset({"safe", "supervised", "hazard"}), TeachingScope.SAFETY_BOUNDED,
        authorized_exploration_items=frozenset({"supervised"}),
    )
    safe = assess_pedagogical_sample(receipt, frozenset({"safe", "supervised"}))
    unsafe = assess_pedagogical_sample(receipt, frozenset({"safe", "hazard"}))
    assert safe.status is PedagogicalStatus.SAFETY_RESTRICTION_RESPECTED
    assert unsafe.status is PedagogicalStatus.SAFETY_RESTRICTION_VIOLATED


def test_blind_initial_independence_is_assessed_before_communication() -> None:
    result = assess_panel_independence(
        (
            ReviewerJudgment(
                "r1-initial", "r1", ReviewStage.BLIND_INITIAL, "pass",
                frozenset({"model-A", "corpus-A"}),
            ),
            ReviewerJudgment(
                "r2-initial", "r2", ReviewStage.BLIND_INITIAL, "fail",
                frozenset({"model-B", "corpus-B"}),
            ),
            ReviewerJudgment(
                "r2-final", "r2", ReviewStage.AFTER_COMMUNICATION, "pass",
                frozenset({"model-B", "corpus-B"}), frozenset({"r1-initial"}),
            ),
        )
    )
    assert result.status is PanelIndependenceStatus.INDEPENDENT_INITIAL_PANEL
    assert result.independent_support_count == 2
    assert result.excluded_later_judgment_ids == ("r2-final",)


def test_shared_model_makes_initial_panel_dependent() -> None:
    result = assess_panel_independence(
        (
            ReviewerJudgment(
                "r1", "r1", ReviewStage.BLIND_INITIAL, "pass",
                frozenset({"model-A", "corpus-A"}),
            ),
            ReviewerJudgment(
                "r2", "r2", ReviewStage.BLIND_INITIAL, "pass",
                frozenset({"model-A", "corpus-B"}),
            ),
        )
    )
    assert result.status is PanelIndependenceStatus.DEPENDENT_INITIAL_PANEL
    assert result.independent_support_count == 1


def test_message_seen_during_initial_stage_violates_blinding() -> None:
    result = assess_panel_independence(
        (
            ReviewerJudgment(
                "r1", "r1", ReviewStage.BLIND_INITIAL, "pass",
                frozenset({"model-A"}), frozenset({"editor-anchor"}),
            ),
            ReviewerJudgment(
                "r2", "r2", ReviewStage.BLIND_INITIAL, "pass",
                frozenset({"model-B"}),
            ),
        )
    )
    assert result.status is PanelIndependenceStatus.DEPENDENT_INITIAL_PANEL


def test_working_memory_can_change_without_rewriting_archive() -> None:
    result = assess_memory_revision(
        MemoryRevisionReceipt(
            "m", "archive-1", "archive-1", "working-1", "working-2",
            retrieved_item_ids=frozenset({"failure-7"}),
        )
    )
    assert result.status is MemoryRevisionStatus.WORKING_STATE_REVISED_ARCHIVE_PRESERVED
    assert not result.scientific_truth_granted


def test_archive_mutation_is_not_reconsolidation() -> None:
    result = assess_memory_revision(
        MemoryRevisionReceipt("m", "archive-1", "archive-2", "working-1", "working-2")
    )
    assert result.status is MemoryRevisionStatus.ARCHIVE_HISTORY_MUTATED


def test_claim_change_requires_new_evidence_and_revalidation() -> None:
    no_evidence = assess_memory_revision(
        MemoryRevisionReceipt(
            "m1", "a", "a", "w1", "w2", changed_claim_ids=frozenset({"claim"}),
        )
    )
    not_revalidated = assess_memory_revision(
        MemoryRevisionReceipt(
            "m2", "a", "a", "w1", "w2",
            new_evidence_ids=frozenset({"evidence"}),
            changed_claim_ids=frozenset({"claim"}),
        )
    )
    assert no_evidence.status is MemoryRevisionStatus.CLAIM_CHANGED_WITHOUT_NEW_EVIDENCE
    assert not_revalidated.status is MemoryRevisionStatus.CLAIM_CHANGED_WITHOUT_REVALIDATION


def test_incubation_candidate_remains_proposal_without_external_test() -> None:
    result = assess_incubation(
        IncubationReceipt(
            "i", "input", frozenset({"claim"}), frozenset({"claim"}),
            candidate_ids=frozenset({"candidate"}),
        )
    )
    assert result.status is IncubationStatus.PROPOSAL_ONLY
    assert not result.candidate_authorized_as_evidence


def test_incubation_cannot_change_protected_claims_by_itself() -> None:
    result = assess_incubation(
        IncubationReceipt(
            "i", "input", frozenset({"old"}), frozenset({"new"}),
            candidate_ids=frozenset({"candidate"}),
        )
    )
    assert result.status is IncubationStatus.PROTECTED_STATE_CHANGED_WITHOUT_EVIDENCE


def test_external_evidence_during_interval_is_not_pure_incubation() -> None:
    result = assess_incubation(
        IncubationReceipt(
            "i", "input", frozenset({"claim"}), frozenset({"claim"}),
            candidate_ids=frozenset({"candidate"}),
            external_evidence_during_interval=frozenset({"new-paper"}),
        )
    )
    assert result.status is IncubationStatus.EXTERNAL_EVIDENCE_CONTAMINATED


def test_policy_revaluation_detects_habit_outliving_context() -> None:
    result = assess_policy_habit(
        PolicyHabitReceipt(
            "h", "workflow", "epoch-1", "epoch-2", 100,
            outcome_devalued=True, revaluation_test_run=True,
            policy_response_changed=False,
        )
    )
    assert result.status is PolicyHabitStatus.POLICY_HABIT_OUTLIVED_CONTEXT
    assert not result.authority_granted


def test_changed_context_without_revaluation_requires_check() -> None:
    result = assess_policy_habit(
        PolicyHabitReceipt(
            "h", "workflow", "epoch-1", "epoch-2", 10,
            outcome_devalued=False, revaluation_test_run=False,
            policy_response_changed=False,
        )
    )
    assert result.status is PolicyHabitStatus.REVALIDATION_REQUIRED


def test_revaluated_policy_can_adapt() -> None:
    result = assess_policy_habit(
        PolicyHabitReceipt(
            "h", "workflow", "epoch-1", "epoch-2", 10,
            outcome_devalued=True, revaluation_test_run=True,
            policy_response_changed=True,
        )
    )
    assert result.status is PolicyHabitStatus.REVALUATED_AND_ADAPTED


def test_counterfactual_is_proposal_not_observation() -> None:
    result = assess_counterfactual(
        CounterfactualProposal(
            "c", "causal-model", "do(x=1)", "y increases",
            frozenset({"no-unmeasured-confounding"}),
        )
    )
    assert result.status is CounterfactualStatus.PROPOSAL_ONLY
    assert not result.scientific_truth_granted


def test_simulation_laundered_as_observation_fails() -> None:
    result = assess_counterfactual(
        CounterfactualProposal(
            "c", "model", "intervention", "outcome", frozenset({"assumption"}),
            represented_as_observation=True,
        )
    )
    assert result.status is CounterfactualStatus.SIMULATION_OBSERVATION_LAUNDERING


def test_external_observation_links_counterfactual_to_test_not_truth() -> None:
    result = assess_counterfactual(
        CounterfactualProposal(
            "c", "model", "intervention", "outcome", frozenset({"assumption"}),
            external_observation_ids=frozenset({"experiment-1"}),
        )
    )
    assert result.status is CounterfactualStatus.EXTERNALLY_TESTED
    assert not result.scientific_truth_granted


def test_observer_coupling_requires_target_specific_change_and_stable_control() -> None:
    result = assess_observer_coupling(
        ObserverCouplingReceipt(
            "o", "publish-benchmark", "publication changes training selection",
            target_before=0.1, target_after=0.8,
            stable_control_before=0.1, stable_control_after=0.15,
            minimum_material_change=0.5,
        )
    )
    assert result.status is ObserverCouplingStatus.COUPLING_CANDIDATE
    assert not result.authority_granted


def test_stable_target_and_control_do_not_support_performativity() -> None:
    result = assess_observer_coupling(
        ObserverCouplingReceipt(
            "o", "measure", "measurement could change the process",
            target_before=1.0, target_after=1.05,
            stable_control_before=1.0, stable_control_after=1.03,
            minimum_material_change=0.2,
        )
    )
    assert result.status is ObserverCouplingStatus.STABLE_CONTROL


def test_target_and_control_change_is_confounding_not_coupling_proof() -> None:
    result = assess_observer_coupling(
        ObserverCouplingReceipt(
            "o", "publish", "publication may change behavior",
            target_before=0, target_after=1,
            stable_control_before=0, stable_control_after=1,
            minimum_material_change=0.5,
        )
    )
    assert result.status is ObserverCouplingStatus.CONFOUNDED_CHANGE
