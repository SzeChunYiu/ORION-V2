from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import permutations
from typing import Mapping


class CollectiveDecisionStatus(str, Enum):
    ADOPTED = "ADOPTED"
    SELECTED_EXTERNAL_ADOPTION_REQUIRED = "SELECTED_EXTERNAL_ADOPTION_REQUIRED"
    AGENDA_DEPENDENT_EXTERNAL_DECISION_REQUIRED = (
        "AGENDA_DEPENDENT_EXTERNAL_DECISION_REQUIRED"
    )
    NO_QUORUM = "NO_QUORUM"
    PAIRWISE_TIE = "PAIRWISE_TIE"
    RULE_OR_AGENDA_DRIFT = "RULE_OR_AGENDA_DRIFT"
    SELF_ADOPTION_FORBIDDEN = "SELF_ADOPTION_FORBIDDEN"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CollectiveDecisionConstitution:
    constitution_id: str
    alternative_ids: tuple[str, ...]
    participant_ids: tuple[str, ...]
    frozen_agenda: tuple[str, ...]
    rule_id: str = "SEQUENTIAL_PAIRWISE_MAJORITY"
    quorum: int = 1
    adoption_authority_id: str = ""
    external_adoption_required: bool = True
    disallow_proposer_as_sole_authority: bool = True

    def __post_init__(self) -> None:
        if not self.constitution_id.strip() or not self.rule_id.strip():
            raise ValueError("constitution and rule identities must be non-blank")
        for field_name, values in (
            ("alternative", self.alternative_ids),
            ("participant", self.participant_ids),
            ("agenda", self.frozen_agenda),
        ):
            if not values or any(not value.strip() for value in values):
                raise ValueError(f"{field_name} identities must be non-empty and non-blank")
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} identities must be unique")
        if set(self.frozen_agenda) != set(self.alternative_ids):
            raise ValueError("the agenda must contain every alternative exactly once")
        if self.quorum < 1 or self.quorum > len(self.participant_ids):
            raise ValueError("quorum must be between one and the participant count")
        if not self.external_adoption_required and not self.adoption_authority_id.strip():
            raise ValueError("an adoption authority is required when direct adoption is enabled")


@dataclass(frozen=True, slots=True)
class PreferenceProfile:
    profile_id: str
    rankings: Mapping[str, tuple[str, ...]]

    def __post_init__(self) -> None:
        if not self.profile_id.strip():
            raise ValueError("profile identity must be non-blank")


@dataclass(frozen=True, slots=True)
class ProposalOwnership:
    proposer_by_alternative: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class CollectiveDecisionAssessment:
    constitution_id: str
    status: CollectiveDecisionStatus
    selected_alternative_id: str | None
    agenda_outcomes: tuple[str, ...]
    agenda_dependent: bool
    participating_voter_ids: tuple[str, ...]
    violations: tuple[str, ...]
    adoption_authority_granted: bool = False
    scientific_truth_granted: bool = False

    def __post_init__(self) -> None:
        if self.scientific_truth_granted:
            raise ValueError("collective adoption cannot grant scientific truth")
        if self.status is not CollectiveDecisionStatus.ADOPTED and self.adoption_authority_granted:
            raise ValueError("only an adopted decision may carry adoption authority")


def _validated_rankings(
    constitution: CollectiveDecisionConstitution,
    profile: PreferenceProfile,
) -> dict[str, tuple[str, ...]]:
    alternatives = set(constitution.alternative_ids)
    rankings: dict[str, tuple[str, ...]] = {}
    for participant_id, ranking in profile.rankings.items():
        if participant_id not in constitution.participant_ids:
            raise ValueError(f"unknown participant {participant_id}")
        if len(ranking) != len(alternatives) or set(ranking) != alternatives:
            raise ValueError(
                f"participant {participant_id} must rank every alternative exactly once"
            )
        rankings[participant_id] = tuple(ranking)
    return rankings


def _pairwise_winner(
    left: str,
    right: str,
    rankings: Mapping[str, tuple[str, ...]],
) -> str | None:
    left_votes = 0
    right_votes = 0
    for ranking in rankings.values():
        if ranking.index(left) < ranking.index(right):
            left_votes += 1
        else:
            right_votes += 1
    if left_votes == right_votes:
        return None
    return left if left_votes > right_votes else right


def sequential_agenda_winner(
    agenda: tuple[str, ...],
    rankings: Mapping[str, tuple[str, ...]],
) -> str | None:
    if not agenda:
        raise ValueError("agenda must be non-empty")
    incumbent = agenda[0]
    for challenger in agenda[1:]:
        winner = _pairwise_winner(incumbent, challenger, rankings)
        if winner is None:
            return None
        incumbent = winner
    return incumbent


def assess_collective_decision(
    constitution: CollectiveDecisionConstitution,
    profile: PreferenceProfile,
    *,
    proposal_ownership: ProposalOwnership | None = None,
    actual_agenda: tuple[str, ...] | None = None,
    actual_rule_id: str | None = None,
    adoption_authority_present: bool = False,
    enumerate_agenda_dependence: bool = True,
) -> CollectiveDecisionAssessment:
    rankings = _validated_rankings(constitution, profile)
    participating = tuple(sorted(rankings))
    if len(rankings) < constitution.quorum:
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.NO_QUORUM,
            None,
            (),
            False,
            participating,
            (f"quorum requires {constitution.quorum}; observed {len(rankings)}",),
        )

    agenda = actual_agenda or constitution.frozen_agenda
    rule_id = actual_rule_id or constitution.rule_id
    if rule_id != constitution.rule_id or agenda != constitution.frozen_agenda:
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.RULE_OR_AGENDA_DRIFT,
            None,
            (),
            False,
            participating,
            ("rule or agenda differs from the frozen constitution",),
        )
    if rule_id != "SEQUENTIAL_PAIRWISE_MAJORITY":
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.CANNOT_CHECK,
            None,
            (),
            False,
            participating,
            (f"unsupported finite reference rule: {rule_id}",),
        )

    selected = sequential_agenda_winner(agenda, rankings)
    if selected is None:
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.PAIRWISE_TIE,
            None,
            (),
            False,
            participating,
            ("a pairwise contest tied",),
        )

    outcomes: tuple[str, ...]
    if enumerate_agenda_dependence:
        if len(constitution.alternative_ids) > 8:
            return CollectiveDecisionAssessment(
                constitution.constitution_id,
                CollectiveDecisionStatus.CANNOT_CHECK,
                selected,
                (),
                False,
                participating,
                ("agenda-dependence enumeration is capped at eight alternatives",),
            )
        outcome_set: set[str] = set()
        for ordering in permutations(constitution.alternative_ids):
            outcome = sequential_agenda_winner(tuple(ordering), rankings)
            if outcome is not None:
                outcome_set.add(outcome)
        outcomes = tuple(sorted(outcome_set))
    else:
        outcomes = (selected,)
    agenda_dependent = len(outcomes) > 1

    if (
        proposal_ownership is not None
        and constitution.disallow_proposer_as_sole_authority
        and constitution.adoption_authority_id.strip()
        and proposal_ownership.proposer_by_alternative.get(selected)
        == constitution.adoption_authority_id
        and len(constitution.participant_ids) == 1
    ):
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.SELF_ADOPTION_FORBIDDEN,
            selected,
            outcomes,
            agenda_dependent,
            participating,
            ("the sole adoption authority proposed the selected alternative",),
        )

    if agenda_dependent:
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.AGENDA_DEPENDENT_EXTERNAL_DECISION_REQUIRED,
            selected,
            outcomes,
            True,
            participating,
            ("the selected alternative depends on agenda order",),
        )

    if constitution.external_adoption_required or not adoption_authority_present:
        return CollectiveDecisionAssessment(
            constitution.constitution_id,
            CollectiveDecisionStatus.SELECTED_EXTERNAL_ADOPTION_REQUIRED,
            selected,
            outcomes,
            False,
            participating,
            (),
        )

    return CollectiveDecisionAssessment(
        constitution.constitution_id,
        CollectiveDecisionStatus.ADOPTED,
        selected,
        outcomes,
        False,
        participating,
        (),
        adoption_authority_granted=True,
    )
