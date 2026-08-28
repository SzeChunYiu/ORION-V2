import pytest

from orion_v2.theory_dominance import (
    TheoryDisposition,
    TheoryProfile,
    assess_theory_dominance,
)


def _parent() -> TheoryProfile:
    return TheoryProfile(
        "F0",
        native_fidelity=1.0,
        quality={
            "justified_terminal": 0.80,
            "safe_transport": 0.90,
        },
        costs={
            "compute": 10.0,
            "expert_time": 5.0,
        },
        generativity=0.20,
        integration=0.10,
        cross_domain_count=2,
        independent_evaluation=True,
        local_parent_deference=True,
    )


def _candidate(**overrides: object) -> TheoryProfile:
    values: dict[str, object] = {
        "theory_id": "F2",
        "native_fidelity": 1.0,
        "quality": {
            "justified_terminal": 0.80,
            "safe_transport": 0.90,
        },
        "costs": {
            "compute": 10.0,
            "expert_time": 5.0,
        },
        "generativity": 0.20,
        "integration": 0.10,
        "cross_domain_count": 2,
        "independent_evaluation": True,
        "local_parent_deference": True,
    }
    values.update(overrides)
    return TheoryProfile(**values)  # type: ignore[arg-type]


def test_theory_profile_cannot_grant_authority() -> None:
    with pytest.raises(ValueError):
        _candidate(authority_granted=True)


def test_mismatched_coordinates_return_cannot_check() -> None:
    result = assess_theory_dominance(
        _candidate(quality={"different": 1.0}),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.CANNOT_CHECK
    assert not result.candidate_dominates


def test_critical_failure_is_non_compensatory() -> None:
    result = assess_theory_dominance(
        _candidate(
            quality={
                "justified_terminal": 0.99,
                "safe_transport": 0.99,
            },
            critical_failures=frozenset({"AUTHORITY_VIOLATION"}),
        ),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.OVERGENERALIZED_THEORY
    assert result.hard_failure_ids == ("AUTHORITY_VIOLATION",)
    assert not result.candidate_dominates


def test_native_fidelity_regression_is_non_compensatory() -> None:
    result = assess_theory_dominance(
        _candidate(native_fidelity=0.95),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.OVERGENERALIZED_THEORY
    assert "NATIVE_FIDELITY_REGRESSION" in result.hard_failure_ids


def test_quality_regression_returns_parent_sufficient() -> None:
    result = assess_theory_dominance(
        _candidate(
            quality={
                "justified_terminal": 0.81,
                "safe_transport": 0.85,
            }
        ),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.PARENT_COMPOSITION_SUFFICIENT
    assert result.quality_regressions == ("safe_transport",)


def test_equal_profile_is_federated_parent_equivalent() -> None:
    result = assess_theory_dominance(_candidate(), _parent())
    assert result.disposition is TheoryDisposition.FEDERATED_PARENT_EQUIVALENT
    assert result.candidate_dominates
    assert not result.strict_scientific_gain
    assert not result.authority_granted


def test_cost_only_gain_is_engineering_efficiency_advance() -> None:
    result = assess_theory_dominance(
        _candidate(costs={"compute": 8.0, "expert_time": 5.0}),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.ENGINEERING_EFFICIENCY_ADVANCE
    assert result.cost_gains == ("compute",)
    assert not result.strict_scientific_gain


def test_cost_drag_without_scientific_gain_is_redundant_drag() -> None:
    result = assess_theory_dominance(
        _candidate(costs={"compute": 12.0, "expert_time": 5.0}),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.REDUNDANT_DRAG
    assert result.cost_regressions == ("compute",)


def test_integration_gain_without_cross_domain_evidence_is_integrative_advance() -> None:
    result = assess_theory_dominance(
        _candidate(integration=0.30, cross_domain_count=1),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.INTEGRATIVE_THEORY_ADVANCE
    assert result.strict_scientific_gain
    assert result.candidate_dominates


def test_scientific_gain_with_cost_regression_is_not_dominance() -> None:
    result = assess_theory_dominance(
        _candidate(
            quality={
                "justified_terminal": 0.90,
                "safe_transport": 0.90,
            },
            costs={"compute": 20.0, "expert_time": 5.0},
            generativity=0.40,
        ),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.INTEGRATIVE_THEORY_ADVANCE
    assert not result.candidate_dominates
    assert result.cost_regressions == ("compute",)


def test_absorptive_candidate_requires_generativity_independence_and_deference() -> None:
    result = assess_theory_dominance(
        _candidate(
            quality={
                "justified_terminal": 0.90,
                "safe_transport": 0.92,
            },
            costs={"compute": 9.0, "expert_time": 5.0},
            generativity=0.50,
            integration=0.40,
            cross_domain_count=3,
            independent_evaluation=True,
            local_parent_deference=True,
        ),
        _parent(),
    )
    assert result.disposition is TheoryDisposition.ABSORPTIVE_SUPERTHEORY_CANDIDATE
    assert result.candidate_dominates
    assert result.strict_scientific_gain
    assert result.quality_gains == ("justified_terminal", "safe_transport")
    assert result.cost_gains == ("compute",)
    assert not result.authority_granted
