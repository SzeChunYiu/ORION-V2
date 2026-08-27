from orion_v2.constitutional import (
    CollectiveDecisionConstitution,
    CollectiveDecisionStatus,
    PreferenceProfile,
    ProposalOwnership,
    assess_collective_decision,
)


def test_majority_cycle_is_exposed_as_agenda_dependence() -> None:
    constitution = CollectiveDecisionConstitution(
        "political-choice",
        ("A", "B", "C"),
        ("v1", "v2", "v3"),
        ("A", "B", "C"),
        quorum=3,
    )
    profile = PreferenceProfile(
        "cycle",
        {
            "v1": ("A", "B", "C"),
            "v2": ("B", "C", "A"),
            "v3": ("C", "A", "B"),
        },
    )
    result = assess_collective_decision(constitution, profile)
    assert (
        result.status
        is CollectiveDecisionStatus.AGENDA_DEPENDENT_EXTERNAL_DECISION_REQUIRED
    )
    assert set(result.agenda_outcomes) == {"A", "B", "C"}
    assert result.scientific_truth_granted is False


def test_scientific_selection_still_requires_external_adoption() -> None:
    constitution = CollectiveDecisionConstitution(
        "framework-adoption",
        ("v1", "v2"),
        ("reviewer-a", "reviewer-b", "reviewer-c"),
        ("v1", "v2"),
        quorum=2,
        adoption_authority_id="programme-board",
        external_adoption_required=True,
    )
    profile = PreferenceProfile(
        "reviews",
        {
            "reviewer-a": ("v2", "v1"),
            "reviewer-b": ("v2", "v1"),
            "reviewer-c": ("v1", "v2"),
        },
    )
    result = assess_collective_decision(constitution, profile)
    assert result.selected_alternative_id == "v2"
    assert result.status is CollectiveDecisionStatus.SELECTED_EXTERNAL_ADOPTION_REQUIRED
    assert result.adoption_authority_granted is False


def test_rule_or_agenda_changed_after_freeze_invalidates_decision() -> None:
    constitution = CollectiveDecisionConstitution(
        "corporate-board",
        ("hold", "invest"),
        ("a", "b"),
        ("hold", "invest"),
        quorum=2,
    )
    profile = PreferenceProfile(
        "p", {"a": ("invest", "hold"), "b": ("invest", "hold")}
    )
    result = assess_collective_decision(
        constitution,
        profile,
        actual_agenda=("invest", "hold"),
    )
    assert result.status is CollectiveDecisionStatus.RULE_OR_AGENDA_DRIFT


def test_no_quorum_is_not_a_negative_adoption_result() -> None:
    constitution = CollectiveDecisionConstitution(
        "standards-body",
        ("old", "new"),
        ("a", "b", "c"),
        ("old", "new"),
        quorum=3,
    )
    profile = PreferenceProfile(
        "p", {"a": ("new", "old"), "b": ("new", "old")}
    )
    result = assess_collective_decision(constitution, profile)
    assert result.status is CollectiveDecisionStatus.NO_QUORUM
    assert result.selected_alternative_id is None


def test_self_adoption_by_single_proposer_authority_is_forbidden() -> None:
    constitution = CollectiveDecisionConstitution(
        "self-change",
        ("incumbent", "candidate"),
        ("agent",),
        ("incumbent", "candidate"),
        adoption_authority_id="agent",
        external_adoption_required=False,
    )
    profile = PreferenceProfile("self", {"agent": ("candidate", "incumbent")})
    ownership = ProposalOwnership({"candidate": "agent"})
    result = assess_collective_decision(
        constitution,
        profile,
        proposal_ownership=ownership,
        adoption_authority_present=True,
    )
    assert result.status is CollectiveDecisionStatus.SELF_ADOPTION_FORBIDDEN


def test_authorized_nonself_decision_can_be_adopted() -> None:
    constitution = CollectiveDecisionConstitution(
        "external-board",
        ("old", "new"),
        ("reviewer-a", "reviewer-b"),
        ("old", "new"),
        adoption_authority_id="board",
        external_adoption_required=False,
    )
    profile = PreferenceProfile(
        "p", {"reviewer-a": ("new", "old"), "reviewer-b": ("new", "old")}
    )
    result = assess_collective_decision(
        constitution, profile, adoption_authority_present=True
    )
    assert result.status is CollectiveDecisionStatus.ADOPTED
    assert result.adoption_authority_granted is True
