from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CorrespondenceStatus(str, Enum):
    EXACT = "EXACT"
    COMPARABLE_WITHIN_TOLERANCE = "COMPARABLE_WITHIN_TOLERANCE"
    PARTIALLY_COMPARABLE = "PARTIALLY_COMPARABLE"
    NONCOMPARABLE = "NONCOMPARABLE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CorrespondenceLink:
    link_id: str
    source_epoch: str
    target_epoch: str
    mapping_ids: tuple[str, ...]
    anchor_ids: tuple[str, ...]
    preserved_invariant_ids: tuple[str, ...]
    uncertainty_upper_bound: float = 0.0
    valid_context_ids: tuple[str, ...] = ()
    violated_invariant_ids: tuple[str, ...] = ()
    unresolved_invariant_ids: tuple[str, ...] = ()
    semantic_loss_ids: tuple[str, ...] = ()
    exact: bool = False

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (self.link_id, self.source_epoch, self.target_epoch)
        ):
            raise ValueError("correspondence identities must be non-blank")
        if self.source_epoch == self.target_epoch:
            raise ValueError("correspondence links require distinct epochs")
        if self.uncertainty_upper_bound < 0:
            raise ValueError("uncertainty must be non-negative")
        for values in (
            self.mapping_ids,
            self.anchor_ids,
            self.preserved_invariant_ids,
            self.valid_context_ids,
            self.violated_invariant_ids,
            self.unresolved_invariant_ids,
            self.semantic_loss_ids,
        ):
            if any(not value.strip() for value in values):
                raise ValueError("correspondence identities may not be blank")


@dataclass(frozen=True, slots=True)
class CorrespondenceChainAssessment:
    status: CorrespondenceStatus
    source_epoch: str
    target_epoch: str
    accumulated_uncertainty_upper_bound: float
    preserved_invariant_ids: tuple[str, ...]
    violated_invariant_ids: tuple[str, ...]
    unresolved_invariant_ids: tuple[str, ...]
    semantic_loss_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("correspondence chains do not grant adoption authority")


def assess_correspondence_chain(
    links: tuple[CorrespondenceLink, ...],
    *,
    context_id: str,
    required_invariant_ids: tuple[str, ...],
    tolerance: float,
) -> CorrespondenceChainAssessment:
    if not context_id.strip() or tolerance < 0:
        raise ValueError("context must be non-blank and tolerance non-negative")
    if not links:
        return CorrespondenceChainAssessment(
            CorrespondenceStatus.CANNOT_CHECK,
            "",
            "",
            0.0,
            (),
            (),
            tuple(required_invariant_ids),
            (),
            ("no correspondence links supplied",),
        )
    reasons: list[str] = []
    for left, right in zip(links, links[1:]):
        if left.target_epoch != right.source_epoch:
            return CorrespondenceChainAssessment(
                CorrespondenceStatus.CANNOT_CHECK,
                links[0].source_epoch,
                links[-1].target_epoch,
                sum(link.uncertainty_upper_bound for link in links),
                (),
                (),
                tuple(required_invariant_ids),
                (),
                (f"non-contiguous chain at {left.link_id}->{right.link_id}",),
            )
    if any(
        link.valid_context_ids and context_id not in link.valid_context_ids
        for link in links
    ):
        reasons.append("one or more links are not validated for the target context")
    preserved = (
        set.intersection(*(set(link.preserved_invariant_ids) for link in links))
        if links
        else set()
    )
    violated = set().union(*(set(link.violated_invariant_ids) for link in links))
    unresolved = set().union(*(set(link.unresolved_invariant_ids) for link in links))
    required = set(required_invariant_ids)
    missing = required - preserved - violated - unresolved
    unresolved |= missing
    losses = set().union(*(set(link.semantic_loss_ids) for link in links))
    uncertainty = sum(link.uncertainty_upper_bound for link in links)
    if required & violated:
        status = CorrespondenceStatus.NONCOMPARABLE
        reasons.append("a required invariant is violated")
    elif (
        reasons
        or required & unresolved
        or any(not link.mapping_ids or not link.anchor_ids for link in links)
    ):
        status = CorrespondenceStatus.CANNOT_CHECK
        reasons.append(
            "required mapping, anchor, context or invariant evidence is incomplete"
        )
    elif losses or uncertainty > tolerance:
        status = CorrespondenceStatus.PARTIALLY_COMPARABLE
        if losses:
            reasons.append("semantic information is lost along the chain")
        if uncertainty > tolerance:
            reasons.append("accumulated uncertainty exceeds tolerance")
    elif all(link.exact for link in links) and uncertainty == 0:
        status = CorrespondenceStatus.EXACT
    else:
        status = CorrespondenceStatus.COMPARABLE_WITHIN_TOLERANCE
    return CorrespondenceChainAssessment(
        status,
        links[0].source_epoch,
        links[-1].target_epoch,
        uncertainty,
        tuple(sorted(preserved)),
        tuple(sorted(violated)),
        tuple(sorted(unresolved)),
        tuple(sorted(losses)),
        tuple(reasons),
    )
