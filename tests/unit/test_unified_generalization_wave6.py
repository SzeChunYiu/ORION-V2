from dataclasses import replace

from orion_v2.unified_generalization import (
    GeneralizationLayer,
    GeneralizationLayerReceipt,
    UnifiedGeneralizationStatus,
    assess_unified_generalization_stack,
)


def _stack() -> tuple[GeneralizationLayerReceipt, ...]:
    native = GeneralizationLayerReceipt(
        "r0", GeneralizationLayer.NATIVE_THEORY, "native:v1", "SOURCE_BOUND", source_ids=("source",)
    )
    envelope = GeneralizationLayerReceipt(
        "r1", GeneralizationLayer.MINIMAL_ENVELOPE, "envelope:v1", "COMPILED_DECISION_RELATIVE", ("r0",)
    )
    interpretation = GeneralizationLayerReceipt(
        "r2", GeneralizationLayer.INTERPRETATION_LAWS, "interpretation:v1", "DECISION_RELATIVE_ADAPTATION", ("r1",)
    )
    recovery = GeneralizationLayerReceipt(
        "r3", GeneralizationLayer.NATIVE_RECOVERY, "recovery:v1", "EXACT_NATIVE_RECOVERY", ("r2",)
    )
    approximate = GeneralizationLayerReceipt(
        "r4", GeneralizationLayer.APPROXIMATE_TRANSPORT, "transport:v1", "NOT_REQUIRED_EXACT", ("r3",)
    )
    target = GeneralizationLayerReceipt(
        "r5", GeneralizationLayer.TARGET_REALIZATION, "target:v1", "READY_FOR_PROTECTED_TARGET_EVALUATION", ("r4",)
    )
    return native, envelope, interpretation, recovery, approximate, target


def test_complete_stack_reaches_protected_evaluation_only() -> None:
    result = assess_unified_generalization_stack(_stack())
    assert result.status is UnifiedGeneralizationStatus.READY_FOR_PROTECTED_TARGET_EVALUATION
    assert result.authority_granted is False
    assert result.novelty_granted is False
    assert result.target_adoption_granted is False


def test_later_success_cannot_compensate_for_native_recovery_failure() -> None:
    stack = list(_stack())
    stack[3] = replace(stack[3], status="INVALID_COUNTEREXAMPLE_LOSS")
    result = assess_unified_generalization_stack(tuple(stack))
    assert result.status is UnifiedGeneralizationStatus.BLOCKED_NATIVE_RECOVERY
    assert result.blocked_layer is GeneralizationLayer.NATIVE_RECOVERY


def test_unresolved_stochastic_transport_is_cannot_check() -> None:
    stack = list(_stack())
    stack[4] = replace(stack[4], status="CANNOT_CHECK_DEPENDENCE")
    result = assess_unified_generalization_stack(tuple(stack))
    assert result.status is UnifiedGeneralizationStatus.CANNOT_CHECK
    assert result.blocked_layer is GeneralizationLayer.APPROXIMATE_TRANSPORT


def test_disconnected_receipts_do_not_form_a_stack() -> None:
    stack = list(_stack())
    stack[2] = replace(stack[2], predecessor_receipt_ids=("unrelated",))
    result = assess_unified_generalization_stack(tuple(stack))
    assert result.status is UnifiedGeneralizationStatus.CANNOT_CHECK
    assert "immediate predecessor" in result.reasons[0]


def test_duplicate_layer_is_rejected() -> None:
    stack = list(_stack())
    stack[-1] = replace(stack[-1], layer=GeneralizationLayer.APPROXIMATE_TRANSPORT)
    assert assess_unified_generalization_stack(tuple(stack)).status is UnifiedGeneralizationStatus.CANNOT_CHECK
