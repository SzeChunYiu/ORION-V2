from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class GeneralizationLayer(str, Enum):
    NATIVE_THEORY = "NATIVE_THEORY"
    MINIMAL_ENVELOPE = "MINIMAL_ENVELOPE"
    INTERPRETATION_LAWS = "INTERPRETATION_LAWS"
    NATIVE_RECOVERY = "NATIVE_RECOVERY"
    APPROXIMATE_TRANSPORT = "APPROXIMATE_TRANSPORT"
    TARGET_REALIZATION = "TARGET_REALIZATION"


class UnifiedGeneralizationStatus(str, Enum):
    READY_FOR_PROTECTED_TARGET_EVALUATION = (
        "READY_FOR_PROTECTED_TARGET_EVALUATION"
    )
    BLOCKED_MINIMAL_ENVELOPE = "BLOCKED_MINIMAL_ENVELOPE"
    BLOCKED_INTERPRETATION_LAWS = "BLOCKED_INTERPRETATION_LAWS"
    BLOCKED_NATIVE_RECOVERY = "BLOCKED_NATIVE_RECOVERY"
    BLOCKED_APPROXIMATE_TRANSPORT = "BLOCKED_APPROXIMATE_TRANSPORT"
    BLOCKED_TARGET_REALIZATION = "BLOCKED_TARGET_REALIZATION"
    CANNOT_CHECK = "CANNOT_CHECK"


_POSITIVE_STATUSES: Mapping[GeneralizationLayer, frozenset[str]] = {
    GeneralizationLayer.NATIVE_THEORY: frozenset({"SOURCE_BOUND"}),
    GeneralizationLayer.MINIMAL_ENVELOPE: frozenset(
        {"COMPILED_EXACT", "COMPILED_DECISION_RELATIVE"}
    ),
    GeneralizationLayer.INTERPRETATION_LAWS: frozenset(
        {
            "EXACT_INTERPRETATION",
            "CONSERVATIVE_EXTENSION",
            "DECISION_RELATIVE_ADAPTATION",
            "SOUND_ABSTRACTION",
        }
    ),
    GeneralizationLayer.NATIVE_RECOVERY: frozenset(
        {"EXACT_NATIVE_RECOVERY", "SOUND_NATIVE_RECOVERY"}
    ),
    GeneralizationLayer.APPROXIMATE_TRANSPORT: frozenset(
        {
            "NOT_REQUIRED_EXACT",
            "EXACT_STOCHASTIC_TRANSPORT",
            "EPSILON_BOUNDED_STOCHASTIC_TRANSPORT",
        }
    ),
    GeneralizationLayer.TARGET_REALIZATION: frozenset(
        {
            "READY_FOR_PROTECTED_TARGET_EVALUATION",
            "READY_FOR_TARGET_NATIVE_VALIDATION",
        }
    ),
}

_CANNOT_CHECK_TOKENS = (
    "CANNOT_CHECK",
    "MISSING_",
    "UNRESOLVED",
    "EXPIRED_",
)

_BLOCKED_STATUS: Mapping[GeneralizationLayer, UnifiedGeneralizationStatus] = {
    GeneralizationLayer.MINIMAL_ENVELOPE: UnifiedGeneralizationStatus.BLOCKED_MINIMAL_ENVELOPE,
    GeneralizationLayer.INTERPRETATION_LAWS: UnifiedGeneralizationStatus.BLOCKED_INTERPRETATION_LAWS,
    GeneralizationLayer.NATIVE_RECOVERY: UnifiedGeneralizationStatus.BLOCKED_NATIVE_RECOVERY,
    GeneralizationLayer.APPROXIMATE_TRANSPORT: UnifiedGeneralizationStatus.BLOCKED_APPROXIMATE_TRANSPORT,
    GeneralizationLayer.TARGET_REALIZATION: UnifiedGeneralizationStatus.BLOCKED_TARGET_REALIZATION,
}


@dataclass(frozen=True, slots=True)
class GeneralizationLayerReceipt:
    receipt_id: str
    layer: GeneralizationLayer
    subject_id: str
    status: str
    predecessor_receipt_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    authority_granted: bool = False
    novelty_granted: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "layer", GeneralizationLayer(self.layer))
        if any(
            not value.strip()
            for value in (self.receipt_id, self.subject_id, self.status)
        ):
            raise ValueError("layer receipt identity, subject and status are required")
        if any(not value.strip() for value in self.predecessor_receipt_ids):
            raise ValueError("predecessor receipt ids may not be blank")
        if any(not value.strip() for value in self.source_ids):
            raise ValueError("source ids may not be blank")
        if self.authority_granted or self.novelty_granted:
            raise ValueError("generalization layer receipts are non-authorizing")


@dataclass(frozen=True, slots=True)
class UnifiedGeneralizationAssessment:
    status: UnifiedGeneralizationStatus
    ordered_receipt_ids: tuple[str, ...]
    blocked_layer: GeneralizationLayer | None
    reasons: tuple[str, ...]
    authority_granted: bool = False
    novelty_granted: bool = False
    target_adoption_granted: bool = False

    def __post_init__(self) -> None:
        if (
            self.authority_granted
            or self.novelty_granted
            or self.target_adoption_granted
        ):
            raise ValueError("unified generalization assessment is non-authorizing")


_REQUIRED_ORDER = (
    GeneralizationLayer.NATIVE_THEORY,
    GeneralizationLayer.MINIMAL_ENVELOPE,
    GeneralizationLayer.INTERPRETATION_LAWS,
    GeneralizationLayer.NATIVE_RECOVERY,
    GeneralizationLayer.APPROXIMATE_TRANSPORT,
    GeneralizationLayer.TARGET_REALIZATION,
)


def assess_unified_generalization_stack(
    receipts: tuple[GeneralizationLayerReceipt, ...],
) -> UnifiedGeneralizationAssessment:
    if len(receipts) != len(_REQUIRED_ORDER):
        return UnifiedGeneralizationAssessment(
            UnifiedGeneralizationStatus.CANNOT_CHECK,
            tuple(item.receipt_id for item in receipts),
            None,
            ("one receipt per required layer is required",),
        )
    by_layer = {item.layer: item for item in receipts}
    if len(by_layer) != len(receipts) or set(by_layer) != set(_REQUIRED_ORDER):
        return UnifiedGeneralizationAssessment(
            UnifiedGeneralizationStatus.CANNOT_CHECK,
            tuple(item.receipt_id for item in receipts),
            None,
            ("required layers must be unique and complete",),
        )
    ordered = tuple(by_layer[layer] for layer in _REQUIRED_ORDER)
    for index, receipt in enumerate(ordered):
        if index == 0:
            if receipt.predecessor_receipt_ids:
                return UnifiedGeneralizationAssessment(
                    UnifiedGeneralizationStatus.CANNOT_CHECK,
                    tuple(item.receipt_id for item in ordered),
                    receipt.layer,
                    ("native theory receipt may not depend on a later receipt",),
                )
        else:
            predecessor = ordered[index - 1].receipt_id
            if predecessor not in receipt.predecessor_receipt_ids:
                return UnifiedGeneralizationAssessment(
                    UnifiedGeneralizationStatus.CANNOT_CHECK,
                    tuple(item.receipt_id for item in ordered),
                    receipt.layer,
                    (
                        f"layer {receipt.layer.value} does not bind immediate predecessor {predecessor}",
                    ),
                )
        if receipt.status not in _POSITIVE_STATUSES[receipt.layer]:
            if any(token in receipt.status for token in _CANNOT_CHECK_TOKENS):
                return UnifiedGeneralizationAssessment(
                    UnifiedGeneralizationStatus.CANNOT_CHECK,
                    tuple(item.receipt_id for item in ordered),
                    receipt.layer,
                    (f"layer {receipt.layer.value} is unresolved: {receipt.status}",),
                )
            return UnifiedGeneralizationAssessment(
                _BLOCKED_STATUS.get(
                    receipt.layer, UnifiedGeneralizationStatus.CANNOT_CHECK
                ),
                tuple(item.receipt_id for item in ordered),
                receipt.layer,
                (f"layer {receipt.layer.value} failed: {receipt.status}",),
            )
    return UnifiedGeneralizationAssessment(
        UnifiedGeneralizationStatus.READY_FOR_PROTECTED_TARGET_EVALUATION,
        tuple(item.receipt_id for item in ordered),
        None,
        (),
    )
