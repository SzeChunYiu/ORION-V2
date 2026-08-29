"""Fail-closed recursive abstraction semantics for ORION-V2.

A higher abstraction level is retained only when it has a protected residual over
its strongest lower-level/parent explanation. Recursive stability is a bounded,
reopenable terminal, never a declaration of ultimate truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class RecursiveGeneralizationStatus(StrEnum):
    BLOCKED_CRITICAL_LOSS = "BLOCKED_CRITICAL_LOSS"
    PARENT_SUFFICIENT = "PARENT_SUFFICIENT"
    NO_HIGHER_LEVEL_RESIDUAL = "NO_HIGHER_LEVEL_RESIDUAL"
    HELDOUT_HIGHER_LEVEL_RESIDUAL = "HELDOUT_HIGHER_LEVEL_RESIDUAL"
    PROSPECTIVE_HIGHER_LEVEL_RESIDUAL = "PROSPECTIVE_HIGHER_LEVEL_RESIDUAL"
    RECURSIVE_STABILITY_CANDIDATE = "RECURSIVE_STABILITY_CANDIDATE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class AbstractionLevel:
    level: int
    abstraction_ids: tuple[str, ...]
    parent_level: int | None
    scope_domain_ids: tuple[str, ...]
    scope_epoch_ids: tuple[str, ...]
    omitted_route_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.level < 0:
            raise ValueError("abstraction levels must be non-negative")
        if self.parent_level is not None and self.parent_level >= self.level:
            raise ValueError("parent level must be lower than the current level")
        for name in ("abstraction_ids", "scope_domain_ids", "scope_epoch_ids", "omitted_route_ids"):
            values = getattr(self, name)
            if any(not item.strip() for item in values):
                raise ValueError(f"{name} may not contain blanks")
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must be unique")


@dataclass(frozen=True, slots=True)
class GeneralizationEvidence:
    strongest_parent_executed: bool
    strongest_parent_sufficient: bool | None
    heldout_prediction_gain: float | None
    heldout_transfer_gain: float | None
    compression_gain: float | None
    critical_information_loss: bool
    prospective_decision_gain: float | None
    resource_delta: float | None
    hostile_omission_challenge_pass: bool | None


@dataclass(frozen=True, slots=True)
class RecursiveGeneralizationReceipt:
    candidate_id: str
    from_level: int
    to_level: int
    status: RecursiveGeneralizationStatus
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    ultimate_truth_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", RecursiveGeneralizationStatus(self.status))
        if self.to_level != self.from_level + 1:
            raise ValueError("recursive receipts must connect adjacent abstraction levels")
        if self.scientific_truth_authorized or self.ultimate_truth_authorized:
            raise ValueError("recursive-generalization receipts are non-authorizing")


def assess_higher_abstraction(
    candidate_id: str,
    *,
    from_level: int,
    evidence: GeneralizationEvidence,
    minimum_material_gain: float = 0.0,
) -> RecursiveGeneralizationReceipt:
    if evidence.critical_information_loss:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.BLOCKED_CRITICAL_LOSS, ("higher abstraction loses a registered critical distinction",))
    if not evidence.strongest_parent_executed:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.CANNOT_CHECK, ("strongest lower-level/parent explanation has not executed",))
    if evidence.strongest_parent_sufficient is True:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.PARENT_SUFFICIENT, ("strongest lower-level/parent explanation reproduces the candidate residual",))
    unresolved = [
        name
        for name, value in (
            ("heldout_prediction_gain", evidence.heldout_prediction_gain),
            ("heldout_transfer_gain", evidence.heldout_transfer_gain),
            ("compression_gain", evidence.compression_gain),
            ("resource_delta", evidence.resource_delta),
        )
        if value is None
    ]
    if evidence.strongest_parent_sufficient is None:
        unresolved.append("strongest_parent_sufficient")
    if unresolved:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.CANNOT_CHECK, tuple(f"unresolved {name}" for name in unresolved))
    gains = (evidence.heldout_prediction_gain or 0.0, evidence.heldout_transfer_gain or 0.0, evidence.compression_gain or 0.0)
    material = any(gain > minimum_material_gain for gain in gains)
    if not material:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.NO_HIGHER_LEVEL_RESIDUAL, ("higher abstraction adds no material held-out prediction, transfer or compression residual",))
    if evidence.hostile_omission_challenge_pass is False:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.NO_HIGHER_LEVEL_RESIDUAL, ("higher abstraction failed the hostile omission challenge",))
    if evidence.prospective_decision_gain is None:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.HELDOUT_HIGHER_LEVEL_RESIDUAL, ("candidate has a held-out residual; prospective research-decision value remains untested",))
    if evidence.prospective_decision_gain <= minimum_material_gain:
        return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.HELDOUT_HIGHER_LEVEL_RESIDUAL, ("candidate improves held-out structure but not the prospectively frozen research decision",))
    return RecursiveGeneralizationReceipt(candidate_id, from_level, from_level + 1, RecursiveGeneralizationStatus.PROSPECTIVE_HIGHER_LEVEL_RESIDUAL, ("candidate adds a material held-out and prospective residual beyond the strongest lower-level explanation",))


@dataclass(frozen=True, slots=True)
class RecursiveStabilityEvidence:
    latest_level: int
    attempted_next_level: bool
    material_next_level_residual: bool | None
    new_domain_challenge_pass: bool | None
    new_epoch_challenge_pass: bool | None
    hostile_omission_challenge_pass: bool | None
    unresolved_route_ids: tuple[str, ...] = ()


def assess_recursive_stability(evidence: RecursiveStabilityEvidence) -> RecursiveGeneralizationReceipt:
    candidate_id = f"recursive-stability-L{evidence.latest_level}"
    if evidence.latest_level < 0:
        raise ValueError("latest level must be non-negative")
    if not evidence.attempted_next_level:
        return RecursiveGeneralizationReceipt(candidate_id, evidence.latest_level, evidence.latest_level + 1, RecursiveGeneralizationStatus.CANNOT_CHECK, ("another recursive abstraction pass has not been attempted",))
    unknown = []
    for name, value in (
        ("material_next_level_residual", evidence.material_next_level_residual),
        ("new_domain_challenge_pass", evidence.new_domain_challenge_pass),
        ("new_epoch_challenge_pass", evidence.new_epoch_challenge_pass),
        ("hostile_omission_challenge_pass", evidence.hostile_omission_challenge_pass),
    ):
        if value is None:
            unknown.append(name)
    if unknown:
        return RecursiveGeneralizationReceipt(candidate_id, evidence.latest_level, evidence.latest_level + 1, RecursiveGeneralizationStatus.CANNOT_CHECK, tuple(f"unresolved {name}" for name in unknown))
    if evidence.material_next_level_residual:
        return RecursiveGeneralizationReceipt(candidate_id, evidence.latest_level, evidence.latest_level + 1, RecursiveGeneralizationStatus.HELDOUT_HIGHER_LEVEL_RESIDUAL, ("a further material abstraction exists; recursive search must continue",))
    if not (evidence.new_domain_challenge_pass and evidence.new_epoch_challenge_pass and evidence.hostile_omission_challenge_pass):
        return RecursiveGeneralizationReceipt(candidate_id, evidence.latest_level, evidence.latest_level + 1, RecursiveGeneralizationStatus.CANNOT_CHECK, ("stability challenge failed or remains unsupported",))
    reasons = ["no material next-level residual survived new-domain, new-epoch and hostile-omission challenges"]
    if evidence.unresolved_route_ids:
        reasons.append("stability is bounded by unresolved routes: " + ", ".join(evidence.unresolved_route_ids))
    return RecursiveGeneralizationReceipt(candidate_id, evidence.latest_level, evidence.latest_level + 1, RecursiveGeneralizationStatus.RECURSIVE_STABILITY_CANDIDATE, tuple(reasons))


def accepted_residual_levels(receipts: Iterable[RecursiveGeneralizationReceipt]) -> tuple[int, ...]:
    return tuple(receipt.to_level for receipt in receipts if receipt.status in {RecursiveGeneralizationStatus.HELDOUT_HIGHER_LEVEL_RESIDUAL, RecursiveGeneralizationStatus.PROSPECTIVE_HIGHER_LEVEL_RESIDUAL})
