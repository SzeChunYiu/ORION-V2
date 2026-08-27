from orion_v2.identifiability import (
    DiagnosticProbe,
    IdentifiabilityAndProbeSystem,
    IdentifiabilityStatus,
    ProbeKind,
    assess_identifiability,
    equivalence_classes,
    structural_information_gain_of_repetition,
)


def _medical_system() -> IdentifiabilityAndProbeSystem:
    return IdentifiabilityAndProbeSystem(
        "differential-diagnosis",
        frozenset({"viral", "bacterial", "autoimmune"}),
        (
            DiagnosticProbe("fever", ProbeKind.OBSERVATION, 0),
            DiagnosticProbe("culture", ProbeKind.INTERVENTION, 4, "clinical-consent"),
            DiagnosticProbe("autoantibody", ProbeKind.OBSERVATION, 2),
        ),
        {
            "fever": {
                "viral": "yes",
                "bacterial": "yes",
                "autoimmune": "yes",
            },
            "culture": {
                "viral": "negative",
                "bacterial": "positive",
                "autoimmune": "negative",
            },
            "autoantibody": {
                "viral": "negative",
                "bacterial": "negative",
                "autoimmune": "positive",
            },
        },
    )


def test_medical_differential_is_discriminable_by_two_costed_probes() -> None:
    result = assess_identifiability(
        _medical_system(),
        selected_probe_ids=("fever",),
        available_authority_ids=("clinical-consent",),
        resource_budget=6,
    )
    assert result.status is IdentifiabilityStatus.DISCRIMINABLE
    assert set(result.minimum_additional_probe_ids) == {"culture", "autoantibody"}
    assert result.minimum_additional_cost == 6


def test_required_clinical_authority_is_not_laundered_as_resource_failure() -> None:
    result = assess_identifiability(
        _medical_system(),
        selected_probe_ids=("fever",),
        resource_budget=100,
    )
    assert result.status is IdentifiabilityStatus.AUTHORITY_REQUIRED
    assert result.blocking_authority_ids == ("clinical-consent",)


def test_causal_models_observationally_equivalent_but_intervention_separates() -> None:
    system = IdentifiabilityAndProbeSystem(
        "causal-direction",
        frozenset({"x-causes-y", "y-causes-x"}),
        (
            DiagnosticProbe("observe-correlation", ProbeKind.OBSERVATION, 1),
            DiagnosticProbe("do-x", ProbeKind.INTERVENTION, 5),
        ),
        {
            "observe-correlation": {
                "x-causes-y": "correlated",
                "y-causes-x": "correlated",
            },
            "do-x": {
                "x-causes-y": "y-changes",
                "y-causes-x": "y-stable",
            },
        },
    )
    observed = assess_identifiability(
        system, selected_probe_ids=("observe-correlation",)
    )
    assert observed.status is IdentifiabilityStatus.DISCRIMINABLE
    assert observed.minimum_additional_probe_ids == ("do-x",)


def test_age_period_cohort_like_structural_alias_is_nonidentifiable() -> None:
    system = IdentifiabilityAndProbeSystem(
        "apc-alias",
        frozenset({"age-effect", "period-effect", "cohort-effect"}),
        (
            DiagnosticProbe("same-cross-section", ProbeKind.OBSERVATION, 1),
            DiagnosticProbe("more-same-cross-section", ProbeKind.OBSERVATION, 10),
        ),
        {
            "same-cross-section": {
                "age-effect": "same-linear-trend",
                "period-effect": "same-linear-trend",
                "cohort-effect": "same-linear-trend",
            },
            "more-same-cross-section": {
                "age-effect": "same-linear-trend",
                "period-effect": "same-linear-trend",
                "cohort-effect": "same-linear-trend",
            },
        },
    )
    result = assess_identifiability(system)
    assert result.status is IdentifiabilityStatus.STRUCTURALLY_NONIDENTIFIABLE
    assert result.minimum_additional_probe_ids == ()


def test_repeated_deterministic_probe_does_not_create_structural_identification() -> None:
    system = _medical_system()
    assert (
        structural_information_gain_of_repetition(
            system,
            selected_probe_ids=("fever",),
            repeated_probe_id="fever",
        )
        == 0
    )


def test_resource_bound_is_distinct_from_nonidentifiability() -> None:
    result = assess_identifiability(
        _medical_system(),
        selected_probe_ids=("fever",),
        available_authority_ids=("clinical-consent",),
        resource_budget=5,
    )
    assert result.status is IdentifiabilityStatus.RESOURCE_BOUND
    assert result.minimum_additional_cost == 6


def test_existing_probe_partition_is_explicit() -> None:
    classes = equivalence_classes(_medical_system(), ("culture",))
    assert ("autoimmune", "viral") in classes
    assert ("bacterial",) in classes
