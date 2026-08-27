from dataclasses import replace

from orion_v2.conversion import (
    ConstrainedConversionSystem,
    ConversionStatus,
    ConversionTransition,
    MonotoneDirection,
    MonotoneSpec,
    assess_conversion_path,
)


def _quantum_system() -> ConstrainedConversionSystem:
    return ConstrainedConversionSystem(
        "quantum-resource",
        "quantum-information",
        frozenset({"entangled", "less-entangled", "separable"}),
        frozenset({"locc-dilute", "locc-discard"}),
        (
            ConversionTransition(
                "entangled", "locc-dilute", "less-entangled", 2, "cert:q1"
            ),
            ConversionTransition(
                "less-entangled", "locc-discard", "separable", 1, "cert:q2"
            ),
        ),
        (MonotoneSpec("entanglement", MonotoneDirection.NONINCREASING),),
        {
            "entanglement": {
                "entangled": 2.0,
                "less-entangled": 1.0,
                "separable": 0.0,
            }
        },
        {"entangled": 0, "less-entangled": 0, "separable": 0},
    )


def _evidence_system() -> ConstrainedConversionSystem:
    return ConstrainedConversionSystem(
        "evidence-conversion",
        "scientific-evidence",
        frozenset(
            {"independent-primary", "correlated-summary", "independent-confirmation"}
        ),
        frozenset({"summarize", "replicate"}),
        (
            ConversionTransition(
                "independent-primary", "summarize", "correlated-summary", 1
            ),
            ConversionTransition(
                "correlated-summary", "replicate", "independent-confirmation", 5
            ),
        ),
        (
            MonotoneSpec("dependence-risk", MonotoneDirection.NONDECREASING),
            MonotoneSpec("fidelity", MonotoneDirection.NONINCREASING),
        ),
        {
            "dependence-risk": {
                "independent-primary": 0.0,
                "correlated-summary": 1.0,
                "independent-confirmation": 1.0,
            },
            "fidelity": {
                "independent-primary": 1.0,
                "correlated-summary": 0.8,
                "independent-confirmation": 0.8,
            },
        },
        {
            "independent-primary": 1,
            "correlated-summary": 1,
            "independent-confirmation": 1,
        },
    )


def test_quantum_resource_conversion_respects_monotone() -> None:
    result = assess_conversion_path(
        _quantum_system(),
        source_state_id="entangled",
        target_state_id="separable",
        operation_ids=("locc-dilute", "locc-discard"),
        resource_budget=3,
    )
    assert result.status is ConversionStatus.CONVERSION_CERTIFIED
    assert result.total_resource_cost == 3


def test_quantum_conversion_rejects_operation_outside_free_set() -> None:
    result = assess_conversion_path(
        _quantum_system(),
        source_state_id="entangled",
        target_state_id="separable",
        operation_ids=("global-unitary",),
    )
    assert result.status is ConversionStatus.UNADMITTED_OPERATION


def test_evidence_summary_does_not_create_independent_authority() -> None:
    result = assess_conversion_path(
        _evidence_system(),
        source_state_id="independent-primary",
        target_state_id="independent-confirmation",
        operation_ids=("summarize",),
    )
    assert result.status is ConversionStatus.TARGET_NOT_REACHED


def test_adding_fake_independent_conversion_violates_dependence_monotone() -> None:
    system = _evidence_system()
    bad = replace(
        system,
        monotone_values={
            **system.monotone_values,
            "dependence-risk": {
                "independent-primary": 0.0,
                "correlated-summary": 1.0,
                "independent-confirmation": 0.0,
            },
        },
    )
    result = assess_conversion_path(
        bad,
        source_state_id="independent-primary",
        target_state_id="independent-confirmation",
        operation_ids=("summarize", "replicate"),
    )
    assert result.status is ConversionStatus.PROTECTED_MONOTONE_VIOLATION


def test_conversion_cannot_amplify_authority() -> None:
    system = _quantum_system()
    bad = replace(
        system,
        authority_ceiling_by_state={
            "entangled": 0,
            "less-entangled": 1,
            "separable": 1,
        },
    )
    result = assess_conversion_path(
        bad,
        source_state_id="entangled",
        target_state_id="less-entangled",
        operation_ids=("locc-dilute",),
    )
    assert result.status is ConversionStatus.AUTHORITY_AMPLIFICATION


def test_resource_budget_is_noncompensatory() -> None:
    result = assess_conversion_path(
        _quantum_system(),
        source_state_id="entangled",
        target_state_id="separable",
        operation_ids=("locc-dilute", "locc-discard"),
        resource_budget=2.9,
    )
    assert result.status is ConversionStatus.RESOURCE_BOUND_EXCEEDED
