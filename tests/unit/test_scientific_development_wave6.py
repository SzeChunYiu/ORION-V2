from orion_v2.scientific_development import (
    CorpusBiasAudit,
    DevelopmentOutcomeClass,
    DevelopmentStep,
    MetaPrincipleEvidence,
    ScientificDevelopmentEpisode,
    ScientificDevelopmentStatus,
    assess_meta_principle,
    corpus_summary,
    discover_operator_contrasts,
)


def _episode(ep_id: str, outcome: DevelopmentOutcomeClass, feature: str, *, domain: str, epoch: str):
    return ScientificDevelopmentEpisode(
        episode_id=ep_id,
        domain_id=domain,
        epoch_id=epoch,
        outcome_class=outcome,
        steps=(
            DevelopmentStep(
                step_id=f"{ep_id}-s0",
                ordinal=0,
                state_feature_ids=("state:open",),
                action_feature_ids=(feature,),
                result_feature_ids=("result:recorded",),
                resource_cost=1.0,
            ),
        ),
        source_mode_ids=("paper", "repository"),
    )


def test_operator_discovery_uses_success_and_failure_population():
    episodes = (
        _episode("p1", DevelopmentOutcomeClass.VALIDATED_SUCCESS, "move:X", domain="math", epoch="e1"),
        _episode("p2", DevelopmentOutcomeClass.VALIDATED_SUCCESS, "move:X", domain="biology", epoch="e2"),
        _episode("n1", DevelopmentOutcomeClass.VALIDATED_FAILURE, "move:Y", domain="math", epoch="e1"),
        _episode("n2", DevelopmentOutcomeClass.ABANDONED, "move:Y", domain="chemistry", epoch="e2"),
    )
    found = discover_operator_contrasts(episodes, minimum_positive_support=2, maximum_feature_order=1)
    assert found
    best = found[0]
    assert best.feature_ids == ("ACTION:move:X",)
    assert best.positive_rate == 1.0
    assert best.negative_rate == 0.0
    assert set(best.source_domain_ids) == {"math", "biology"}


def test_population_regularities_do_not_become_causal_laws_automatically():
    receipt = assess_meta_principle(
        "candidate-1",
        MetaPrincipleEvidence(
            corpus_bias_audit_pass=True,
            matched_failure_controls_executed=True,
            strongest_parent_executed=True,
            strongest_parent_sufficient=False,
            heldout_field_pass=True,
            heldout_epoch_pass=True,
            prospective_task_pass=None,
            critical_loss_observed=False,
            resource_accounted=True,
        ),
    )
    assert receipt.status is ScientificDevelopmentStatus.POPULATION_REGULARITY_ONLY
    assert not receipt.causal_law_authorized


def test_prospective_residual_requires_parent_and_bias_controls():
    receipt = assess_meta_principle(
        "candidate-2",
        MetaPrincipleEvidence(
            corpus_bias_audit_pass=True,
            matched_failure_controls_executed=True,
            strongest_parent_executed=True,
            strongest_parent_sufficient=False,
            heldout_field_pass=True,
            heldout_epoch_pass=True,
            prospective_task_pass=True,
            critical_loss_observed=False,
            resource_accounted=True,
            independent_adjudication_complete=True,
        ),
    )
    assert receipt.status is ScientificDevelopmentStatus.PROSPECTIVE_META_POLICY_RESIDUAL


def test_bias_audit_is_fail_closed():
    audit = CorpusBiasAudit(
        survivorship_model_bound=True,
        publication_bias_model_bound=True,
        citation_bias_model_bound=True,
        field_epoch_bias_model_bound=True,
        language_geography_bias_model_bound=True,
        team_institution_bias_model_bound=True,
        missing_failure_censoring_explicit=True,
        multiple_source_modes_present=False,
    )
    assert not audit.passes_for_population_claims


def test_corpus_summary_never_equates_proxy_metrics_with_truth():
    episodes = (
        _episode("p", DevelopmentOutcomeClass.VALIDATED_SUCCESS, "move:X", domain="math", epoch="e1"),
        _episode("u", DevelopmentOutcomeClass.UNKNOWN, "move:X", domain="physics", epoch="e2"),
    )
    summary = corpus_summary(episodes)
    assert summary["validated_success"] == 1
    assert summary["unknown_or_partial"] == 1
    assert "citation" not in summary
