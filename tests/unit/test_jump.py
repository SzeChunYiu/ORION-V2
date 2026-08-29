from orion_v2.jump import (
    JumpAssessment,
    JumpLevel,
    JumpProposal,
    JumpTrigger,
    TriggerKind,
    assess_jump,
    minimum_level,
)


def _proposal(level: JumpLevel) -> JumpProposal:
    trigger = JumpTrigger(
        trigger_id=f"trigger:{level}",
        kind=TriggerKind.EXPRESSIVE_CEILING,
        incumbent_level=JumpLevel.LOCAL_REPAIR_COMPOSITION,
        witness_ids=("proof:old-closure-ceiling",),
        lower_level_dispositions=("J0-insufficient", "J1-insufficient"),
    )
    return JumpProposal(
        proposal_id=f"proposal:{level}",
        trigger=trigger,
        level=level,
        transformation_family="representation-change",
        parent_ids=("donor:verified-regime-revision",),
        correspondence_ids=("map:old-new",),
        preservation_obligation_ids=("preserve:valid-old-results",),
        predicted_contract_ids=("contract:new-reach",),
        falsifier_ids=("falsifier:no-new-reach",),
    )


def test_poor_score_is_not_a_jump_trigger() -> None:
    trigger = JumpTrigger(
        trigger_id="poor-score",
        kind=TriggerKind.POOR_SCORE,
        incumbent_level=JumpLevel.ACTION_PARAMETER,
        witness_ids=("metric:low",),
        lower_level_dispositions=("not-tested",),
    )
    proposal = JumpProposal(
        proposal_id="invalid",
        trigger=trigger,
        level=JumpLevel.MODEL_HYPOTHESIS_EXPANSION,
        transformation_family="model-expansion",
        parent_ids=("parent",),
        correspondence_ids=("map",),
        preservation_obligation_ids=("preserve",),
        predicted_contract_ids=("contract",),
        falsifier_ids=("falsifier",),
    )
    assert assess_jump(proposal, lower_level_sufficient=False, donor_product_ties=False) is JumpAssessment.INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED


def test_censored_route_cannot_support_jump() -> None:
    trigger = JumpTrigger(
        trigger_id="censored",
        kind=TriggerKind.EXPRESSIVE_CEILING,
        incumbent_level=JumpLevel.ACTION_PARAMETER,
        witness_ids=("search:zero",),
        lower_level_dispositions=("search-failed",),
        route_censored=True,
    )
    assert trigger.is_admissible is False


def test_minimum_responsible_level_wins() -> None:
    lower = _proposal(JumpLevel.REPRESENTATION_REGIME_TRANSITION)
    higher = _proposal(JumpLevel.FRAMEWORK_REVISION)
    assert minimum_level((higher, lower)) == lower


def test_donor_tie_contracts_jump_claim() -> None:
    proposal = _proposal(JumpLevel.REPRESENTATION_REGIME_TRANSITION)
    assert assess_jump(proposal, lower_level_sufficient=False, donor_product_ties=True) is JumpAssessment.DONOR_SUBSUMES_JUMP
