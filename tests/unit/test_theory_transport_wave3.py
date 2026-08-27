from dataclasses import replace
from types import SimpleNamespace

import pytest

from orion_v2.theory_transport import (
    AdaptationStatus,
    AssumptionDisposition,
    AssumptionTreatment,
    CompositionStatus,
    CounterexampleWitness,
    GeneralizationContext,
    InterpretationAssessment,
    InterpretationKind,
    InterpretationStatus,
    ResourceCalibration,
    ResourceInterval,
    ScientificTheory,
    TargetAdaptation,
    TheoryInterpretation,
    TransportCertificate,
    TransportValidityBinding,
    ValidityStatus,
    assess_interpretation,
    assess_target_adaptation,
    assess_transport_validity,
    compose_transport_certificates,
    upgrade_wave2_finite_theory,
)


def _resource(lower: float, upper: float, *, unit: str = "cost") -> tuple[ResourceInterval, ...]:
    return (ResourceInterval("effort", unit, lower, upper),)


def _native_theory(*, domain: str = "management", epoch: str = "v1") -> ScientificTheory:
    return ScientificTheory(
        theory_id=f"{domain}:native",
        domain_id=domain,
        epoch_id=epoch,
        states=frozenset({"draft", "reviewed"}),
        actions=frozenset({"review"}),
        transitions=frozenset({("draft", "review", "reviewed")}),
        judgments={
            "release_allowed": {"draft": False, "reviewed": True},
            "risk_class": {"draft": "high", "reviewed": "low"},
        },
        assumptions=("qualified-reviewer",),
        action_resources={"review": _resource(2, 3)},
        judgment_authority_ceiling={"release_allowed": 1, "risk_class": 1},
    )


def _envelope_theory(*, extension: bool = False, sound: bool = False) -> ScientificTheory:
    states = {"open", "closed"}
    actions = {"validate"}
    transitions = {("open", "validate", "closed")}
    judgments = {
        "admissible": {"open": False, "closed": True},
        "risk": {"open": "high", "closed": "low"},
    }
    resources = {"validate": _resource(2, 3)}
    authority = {"admissible": 1, "risk": 1}
    if extension:
        states.add("archived")
        actions.add("archive")
        transitions.add(("closed", "archive", "archived"))
        judgments["admissible"]["archived"] = True
        judgments["risk"]["archived"] = "low"
        resources["archive"] = _resource(1, 1)
    if sound:
        judgments["admissible"] = {
            "open": frozenset({False}),
            "closed": frozenset({True}),
        }
        judgments["risk"] = {
            "open": frozenset({"high", "medium"}),
            "closed": frozenset({"low", "medium"}),
        }
    return ScientificTheory(
        theory_id="general:obligation",
        domain_id="general",
        epoch_id="g1",
        states=frozenset(states),
        actions=frozenset(actions),
        transitions=frozenset(transitions),
        judgments=judgments,
        assumptions=("qualified-reviewer",),
        action_resources=resources,
        judgment_authority_ceiling=authority,
    )


def _context(
    *,
    judgments=("release_allowed", "risk_class"),
    actions=("review",),
    allowed_loss=(),
    required_counterexamples=("draft-not-releaseable",),
) -> GeneralizationContext:
    return GeneralizationContext(
        context_id="release-decision",
        registered_judgment_ids=judgments,
        registered_action_ids=actions,
        allowed_lost_judgment_ids=allowed_loss,
        required_counterexample_ids=required_counterexamples,
    )


def _interpretation(
    *,
    native: ScientificTheory,
    generalized: ScientificTheory,
    kind: InterpretationKind = InterpretationKind.EXACT,
    context: GeneralizationContext | None = None,
    state_map=None,
    reverse_state_map=None,
    assumption_treatments=None,
    resource_calibrations=(),
) -> TheoryInterpretation:
    state_map = state_map or {"draft": "open", "reviewed": "closed"}
    reverse_state_map = reverse_state_map or {
        "open": frozenset({"draft"}),
        "closed": frozenset({"reviewed"}),
    }
    assumption_treatments = assumption_treatments or (
        AssumptionTreatment("qualified-reviewer", AssumptionDisposition.PRESERVED),
    )
    return TheoryInterpretation(
        interpretation_id=f"{native.domain_id}->obligation",
        native_theory_id=native.theory_id,
        generalized_theory_id=generalized.theory_id,
        source_epoch_id=native.epoch_id,
        generalized_epoch_id=generalized.epoch_id,
        kind=kind,
        context=context or _context(),
        state_map=state_map,
        reverse_state_map=reverse_state_map,
        action_map={"review": "validate"},
        reverse_action_map={"validate": frozenset({"review"})},
        judgment_map={"release_allowed": "admissible", "risk_class": "risk"},
        assumption_treatments=assumption_treatments,
        resource_calibrations=resource_calibrations,
        counterexamples=(
            CounterexampleWitness(
                "draft-not-releaseable",
                "draft",
                "release_allowed",
                False,
                source_ids=("native-case:1",),
            ),
        ),
        source_ids=("source:native-theory", "source:general-envelope"),
    )


def test_exact_interpretation_satisfies_round_trip_and_counterexample_reflection() -> None:
    native = _native_theory()
    generalized = _envelope_theory()
    assessment = assess_interpretation(
        native, generalized, _interpretation(native=native, generalized=generalized)
    )
    assert assessment.status is InterpretationStatus.EXACT_INTERPRETATION
    assert assessment.round_trip_state_count == 2
    assert assessment.reflected_counterexample_ids == ("draft-not-releaseable",)
    assert assessment.authority_granted is False


def test_conservative_extension_allows_new_generalized_states_but_reflects_old_behavior() -> None:
    native = _native_theory()
    generalized = _envelope_theory(extension=True)
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            kind=InterpretationKind.CONSERVATIVE_EXTENSION,
        ),
    )
    assert assessment.status is InterpretationStatus.CONSERVATIVE_EXTENSION


def test_conservative_extension_rejects_extra_behavior_inside_native_image() -> None:
    native = _native_theory()
    generalized = replace(
        _envelope_theory(extension=True),
        transitions=frozenset(
            {
                ("open", "validate", "closed"),
                ("closed", "validate", "open"),
                ("closed", "archive", "archived"),
            }
        ),
    )
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            kind=InterpretationKind.CONSERVATIVE_EXTENSION,
        ),
    )
    assert assessment.status is InterpretationStatus.INVALID_BACKWARD_REFLECTION


def test_decision_relative_quotient_may_drop_only_declared_unregistered_judgments() -> None:
    native = ScientificTheory(
        theory_id="politics:native",
        domain_id="politics",
        epoch_id="2026",
        states=frozenset({"a", "b", "c"}),
        actions=frozenset({"compare"}),
        transitions=frozenset({("a", "compare", "c"), ("b", "compare", "c")}),
        judgments={
            "eligible": {"a": True, "b": True, "c": False},
            "party": {"a": "x", "b": "y", "c": "z"},
        },
        assumptions=("common-scale",),
        action_resources={"compare": _resource(1, 1)},
        judgment_authority_ceiling={"eligible": 1, "party": 1},
    )
    generalized = ScientificTheory(
        theory_id="general:eligibility",
        domain_id="general",
        epoch_id="g1",
        states=frozenset({"in", "out"}),
        actions=frozenset({"test"}),
        transitions=frozenset({("in", "test", "out")}),
        judgments={"admissible": {"in": True, "out": False}},
        assumptions=("common-scale",),
        action_resources={"test": _resource(1, 1)},
        judgment_authority_ceiling={"admissible": 1},
    )
    interpretation = TheoryInterpretation(
        interpretation_id="politics->eligibility",
        native_theory_id=native.theory_id,
        generalized_theory_id=generalized.theory_id,
        source_epoch_id=native.epoch_id,
        generalized_epoch_id=generalized.epoch_id,
        kind=InterpretationKind.DECISION_RELATIVE,
        context=GeneralizationContext(
            "eligibility-only",
            registered_judgment_ids=("eligible",),
            registered_action_ids=("compare",),
            allowed_lost_judgment_ids=("party",),
        ),
        state_map={"a": "in", "b": "in", "c": "out"},
        reverse_state_map={"in": frozenset({"a", "b"}), "out": frozenset({"c"})},
        action_map={"compare": "test"},
        reverse_action_map={"test": frozenset({"compare"})},
        judgment_map={"eligible": "admissible"},
        assumption_treatments=(
            AssumptionTreatment("common-scale", AssumptionDisposition.PRESERVED),
        ),
        source_ids=("source:politics",),
    )
    assessment = assess_interpretation(native, generalized, interpretation)
    assert assessment.status is InterpretationStatus.DECISION_RELATIVE_ADAPTATION
    assert assessment.collapsed_judgment_ids == ("party",)
    assert assessment.warnings


def test_undeclared_information_loss_fails_closed() -> None:
    native = ScientificTheory(
        "n", "d", "e", frozenset({1, 2}), frozenset({"a"}), frozenset(),
        {"registered": {1: True, 2: True}, "future": {1: "x", 2: "y"}},
        ("a",), {"a": _resource(0, 0)}, {"registered": 0, "future": 0},
    )
    generalized = ScientificTheory(
        "g", "g", "e2", frozenset({"q"}), frozenset({"b"}), frozenset(),
        {"r": {"q": True}}, ("a",), {"b": _resource(0, 0)}, {"r": 0},
    )
    interpretation = TheoryInterpretation(
        "i", "n", "g", "e", "e2", InterpretationKind.DECISION_RELATIVE,
        GeneralizationContext("c", ("registered",), ("a",)),
        {1: "q", 2: "q"}, {"q": frozenset({1, 2})},
        {"a": "b"}, {"b": frozenset({"a"})}, {"registered": "r"},
        (AssumptionTreatment("a", AssumptionDisposition.PRESERVED),),
        source_ids=("s",),
    )
    assert (
        assess_interpretation(native, generalized, interpretation).status
        is InterpretationStatus.INVALID_UNDECLARED_INFORMATION_LOSS
    )


def test_sound_abstraction_uses_set_inclusion_for_scalar_and_set_native_values() -> None:
    native = _native_theory()
    generalized = _envelope_theory(sound=True)
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            kind=InterpretationKind.SOUND_ABSTRACTION,
        ),
    )
    assert assessment.status is InterpretationStatus.SOUND_ABSTRACTION


def test_sound_abstraction_can_preserve_set_valued_native_result() -> None:
    native = replace(
        _native_theory(),
        judgments={
            "release_allowed": {
                "draft": frozenset({False}),
                "reviewed": frozenset({True}),
            },
            "risk_class": {
                "draft": frozenset({"high"}),
                "reviewed": frozenset({"low"}),
            },
        },
    )
    generalized = _envelope_theory(sound=True)
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            kind=InterpretationKind.SOUND_ABSTRACTION,
        ),
    )
    assert assessment.status is InterpretationStatus.SOUND_ABSTRACTION


def test_exact_interpretation_rejects_relaxed_assumption() -> None:
    native = _native_theory()
    generalized = _envelope_theory()
    relaxed = (
        AssumptionTreatment(
            "qualified-reviewer",
            AssumptionDisposition.RELAXED,
            evidence_ids=("evidence:relax",),
            revalidation_obligation_ids=("revalidate:target",),
        ),
    )
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            assumption_treatments=relaxed,
        ),
    )
    assert assessment.status is InterpretationStatus.INVALID_ASSUMPTION_TREATMENT


def test_decision_relative_adaptation_allows_calibrated_assumption_with_revalidation() -> None:
    native = _native_theory()
    generalized = _envelope_theory()
    calibrated = (
        AssumptionTreatment(
            "qualified-reviewer",
            AssumptionDisposition.CALIBRATED,
            evidence_ids=("calibration:reviewer-equivalence",),
            revalidation_obligation_ids=("target:known-answer",),
        ),
    )
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            kind=InterpretationKind.DECISION_RELATIVE,
            context=_context(judgments=("release_allowed",)),
            assumption_treatments=calibrated,
        ),
    )
    assert assessment.status is InterpretationStatus.DECISION_RELATIVE_ADAPTATION
    assert any("revalidation" in warning for warning in assessment.warnings)


def test_resource_understatement_is_rejected() -> None:
    native = _native_theory()
    generalized = replace(_envelope_theory(), action_resources={"validate": _resource(1, 1)})
    assert (
        assess_interpretation(
            native, generalized, _interpretation(native=native, generalized=generalized)
        ).status
        is InterpretationStatus.INVALID_RESOURCE_CALIBRATION
    )


def test_resource_unit_conversion_requires_evidence_and_can_be_conservative() -> None:
    native = replace(_native_theory(), action_resources={"review": _resource(2, 3, unit="hours")})
    generalized = replace(
        _envelope_theory(), action_resources={"validate": _resource(120, 180, unit="minutes")}
    )
    calibration = ResourceCalibration(
        "effort", "effort", "hours", "minutes", scale=60,
        evidence_ids=("unit:hours-to-minutes",),
    )
    assessment = assess_interpretation(
        native,
        generalized,
        _interpretation(
            native=native,
            generalized=generalized,
            resource_calibrations=(calibration,),
        ),
    )
    assert assessment.status is InterpretationStatus.EXACT_INTERPRETATION


def test_authority_cannot_be_amplified_by_generalization() -> None:
    native = _native_theory()
    generalized = replace(
        _envelope_theory(), judgment_authority_ceiling={"admissible": 2, "risk": 1}
    )
    assert (
        assess_interpretation(
            native, generalized, _interpretation(native=native, generalized=generalized)
        ).status
        is InterpretationStatus.INVALID_AUTHORITY_AMPLIFICATION
    )


def test_decisive_counterexample_cannot_be_hidden_inside_unknown_set() -> None:
    native = _native_theory()
    generalized = replace(
        _envelope_theory(sound=True),
        judgments={
            "admissible": {
                "open": frozenset({False, True}),
                "closed": frozenset({True}),
            },
            "risk": {
                "open": frozenset({"high", "medium"}),
                "closed": frozenset({"low", "medium"}),
            },
        },
    )
    assert (
        assess_interpretation(
            native,
            generalized,
            _interpretation(
                native=native,
                generalized=generalized,
                kind=InterpretationKind.SOUND_ABSTRACTION,
            ),
        ).status
        is InterpretationStatus.INVALID_COUNTEREXAMPLE_REFLECTION
    )


def test_transport_validity_expires_on_calibration_change() -> None:
    frozen = TransportValidityBinding("i", "s1", "g1", "a", "c1", "e1", "r1", "p1")
    result = assess_transport_validity(frozen, replace(frozen, calibration_digest="c2"))
    assert result.status is ValidityStatus.EXPIRED_CALIBRATION
    assert result.expired_coordinates == ("calibration_digest",)


def test_transport_validity_reports_multiple_expirations() -> None:
    frozen = TransportValidityBinding("i", "s1", "g1", "a", "c1", "e1", "r1", "p1")
    result = assess_transport_validity(
        frozen, replace(frozen, source_epoch_id="s2", evaluator_digest="e2")
    )
    assert result.status is ValidityStatus.MULTIPLE_EXPIRATIONS
    assert set(result.expired_coordinates) == {"source_epoch_id", "evaluator_digest"}


def _certificate(
    certificate_id: str,
    source: str,
    target: str,
    source_epoch: str,
    target_epoch: str,
    status: InterpretationStatus,
    judgment_map,
    authority: int = 2,
) -> TransportCertificate:
    return TransportCertificate(
        certificate_id, source, target, source_epoch, target_epoch, status,
        judgment_map, uncertainty_bound=0.1, semantic_loss_bound=0.2,
        authority_ceiling=authority, source_ids=(f"source:{certificate_id}",),
    )


def test_transport_certificates_compose_with_accumulated_uncertainty_and_min_authority() -> None:
    left = _certificate(
        "a-b", "A", "B", "e1", "e2",
        InterpretationStatus.EXACT_INTERPRETATION, {"j": "k"}, authority=3,
    )
    right = _certificate(
        "b-c", "B", "C", "e2", "e3",
        InterpretationStatus.CONSERVATIVE_EXTENSION, {"k": "m"}, authority=1,
    )
    result = compose_transport_certificates(left, right, certificate_id="a-c")
    assert result.status is CompositionStatus.COMPOSED_CONSERVATIVE
    assert result.certificate is not None
    assert result.certificate.judgment_map == {"j": "m"}
    assert result.certificate.uncertainty_bound == pytest.approx(0.2)
    assert result.certificate.semantic_loss_bound == pytest.approx(0.4)
    assert result.certificate.authority_ceiling == 1


def test_transport_composition_rejects_noncontiguous_epochs() -> None:
    left = _certificate(
        "a-b", "A", "B", "e1", "e2",
        InterpretationStatus.EXACT_INTERPRETATION, {"j": "k"},
    )
    right = _certificate(
        "b-c", "B", "C", "wrong", "e3",
        InterpretationStatus.EXACT_INTERPRETATION, {"k": "m"},
    )
    assert (
        compose_transport_certificates(left, right, certificate_id="a-c").status
        is CompositionStatus.INVALID_NONCONTIGUOUS_CHAIN
    )


def test_transport_composition_rejects_missing_judgment_chain() -> None:
    left = _certificate(
        "a-b", "A", "B", "e1", "e2",
        InterpretationStatus.EXACT_INTERPRETATION, {"j": "k"},
    )
    right = _certificate(
        "b-c", "B", "C", "e2", "e3",
        InterpretationStatus.EXACT_INTERPRETATION, {"other": "m"},
    )
    assert (
        compose_transport_certificates(left, right, certificate_id="a-c").status
        is CompositionStatus.INVALID_JUDGMENT_CHAIN
    )


def _engineering_target() -> ScientificTheory:
    return ScientificTheory(
        theory_id="engineering:native",
        domain_id="engineering",
        epoch_id="v1",
        states=frozenset({"unverified", "verified"}),
        actions=frozenset({"verify"}),
        transitions=frozenset({("unverified", "verify", "verified")}),
        judgments={
            "release_permitted": {"unverified": False, "verified": True},
            "hazard": {"unverified": "high", "verified": "low"},
        },
        assumptions=("qualified-reviewer",),
        action_resources={"verify": _resource(2, 3)},
        judgment_authority_ceiling={"release_permitted": 1, "hazard": 1},
    )


def _target_interpretation(target: ScientificTheory, envelope: ScientificTheory) -> TheoryInterpretation:
    return TheoryInterpretation(
        interpretation_id="engineering->obligation",
        native_theory_id=target.theory_id,
        generalized_theory_id=envelope.theory_id,
        source_epoch_id=target.epoch_id,
        generalized_epoch_id=envelope.epoch_id,
        kind=InterpretationKind.EXACT,
        context=GeneralizationContext(
            "engineering-release",
            ("release_permitted", "hazard"),
            ("verify",),
            required_counterexample_ids=("unverified-not-releaseable",),
        ),
        state_map={"unverified": "open", "verified": "closed"},
        reverse_state_map={
            "open": frozenset({"unverified"}),
            "closed": frozenset({"verified"}),
        },
        action_map={"verify": "validate"},
        reverse_action_map={"validate": frozenset({"verify"})},
        judgment_map={"release_permitted": "admissible", "hazard": "risk"},
        assumption_treatments=(
            AssumptionTreatment("qualified-reviewer", AssumptionDisposition.PRESERVED),
        ),
        counterexamples=(
            CounterexampleWitness(
                "unverified-not-releaseable", "unverified", "release_permitted", False,
            ),
        ),
        source_ids=("source:engineering",),
    )


def test_remote_domain_adaptation_requires_independent_target_mapping_and_validation() -> None:
    source = _native_theory(domain="management")
    target = _engineering_target()
    envelope = _envelope_theory()
    source_i = _interpretation(native=source, generalized=envelope)
    target_i = _target_interpretation(target, envelope)
    source_a = assess_interpretation(source, envelope, source_i)
    target_a = assess_interpretation(target, envelope, target_i)
    adaptation = TargetAdaptation(
        adaptation_id="management-method-to-engineering",
        source_interpretation_id=source_i.interpretation_id,
        target_interpretation_id=target_i.interpretation_id,
        shared_generalized_theory_id=envelope.theory_id,
        envelope_state_to_target_state={"open": "unverified", "closed": "verified"},
        envelope_action_to_target_action={"validate": "verify"},
        registered_envelope_judgment_ids=("admissible", "risk"),
        calibration_ids=("calibration:engineering-review",),
        validation_case_ids=("engineering:known-answer-1", "engineering:hostile-1"),
        source_ids=("source:management", "source:engineering"),
    )
    result = assess_target_adaptation(source_i, source_a, target_i, target_a, adaptation)
    assert result.status is AdaptationStatus.READY_FOR_PROTECTED_TARGET_EVALUATION
    assert result.ready_for_target_evaluation is True
    assert result.target_success_claimed is False


def test_source_success_does_not_replace_target_native_validation() -> None:
    source = _native_theory(domain="management")
    target = _engineering_target()
    envelope = _envelope_theory()
    source_i = _interpretation(native=source, generalized=envelope)
    target_i = _target_interpretation(target, envelope)
    result = assess_target_adaptation(
        source_i,
        assess_interpretation(source, envelope, source_i),
        target_i,
        assess_interpretation(target, envelope, target_i),
        TargetAdaptation(
            "a", source_i.interpretation_id, target_i.interpretation_id,
            envelope.theory_id, {"open": "unverified", "closed": "verified"},
            {"validate": "verify"}, ("admissible",), ("calibration:target",), (), ("source",),
        ),
    )
    assert result.status is AdaptationStatus.MISSING_TARGET_VALIDATION


def test_target_realization_must_be_right_inverse_of_target_transport() -> None:
    source = _native_theory(domain="management")
    target = _engineering_target()
    envelope = _envelope_theory()
    source_i = _interpretation(native=source, generalized=envelope)
    target_i = _target_interpretation(target, envelope)
    result = assess_target_adaptation(
        source_i,
        assess_interpretation(source, envelope, source_i),
        target_i,
        assess_interpretation(target, envelope, target_i),
        TargetAdaptation(
            "a", source_i.interpretation_id, target_i.interpretation_id,
            envelope.theory_id, {"open": "verified"}, {"validate": "verify"},
            ("admissible",), ("calibration:target",), ("validation:1",), ("source",),
        ),
    )
    assert result.status is AdaptationStatus.INVALID_TARGET_REALIZATION


def test_interpretation_objects_are_non_authorizing() -> None:
    with pytest.raises(ValueError, match="non-authorizing"):
        InterpretationAssessment(
            "i", InterpretationStatus.EXACT_INTERPRETATION, (), (),
            0, 0, 0, 0, (), (), authority_granted=True,
        )


def test_exact_interpretation_rejects_extra_generalized_old_language_structure() -> None:
    native = _native_theory()
    base = _envelope_theory()
    generalized = replace(
        base,
        judgments={**base.judgments, "extra": {"open": 0, "closed": 1}},
        judgment_authority_ceiling={**base.judgment_authority_ceiling, "extra": 0},
    )
    assert (
        assess_interpretation(
            native, generalized, _interpretation(native=native, generalized=generalized)
        ).status
        is InterpretationStatus.INVALID_ROUND_TRIP
    )


def test_exact_interpretation_rejects_authority_decrease_as_nonidentity() -> None:
    native = replace(
        _native_theory(), judgment_authority_ceiling={"release_allowed": 2, "risk_class": 1}
    )
    generalized = _envelope_theory()
    assert (
        assess_interpretation(
            native, generalized, _interpretation(native=native, generalized=generalized)
        ).status
        is InterpretationStatus.INVALID_ROUND_TRIP
    )


def test_conservative_extension_allows_extra_generalized_judgment() -> None:
    native = _native_theory()
    base = _envelope_theory(extension=True)
    generalized = replace(
        base,
        judgments={
            **base.judgments,
            "audit_trace_available": {"open": False, "closed": True, "archived": True},
        },
        judgment_authority_ceiling={
            **base.judgment_authority_ceiling,
            "audit_trace_available": 0,
        },
    )
    assert (
        assess_interpretation(
            native,
            generalized,
            _interpretation(
                native=native,
                generalized=generalized,
                kind=InterpretationKind.CONSERVATIVE_EXTENSION,
            ),
        ).status
        is InterpretationStatus.CONSERVATIVE_EXTENSION
    )


def test_target_adaptation_requires_registered_decision_and_source_identity() -> None:
    with pytest.raises(ValueError, match="registered decisions"):
        TargetAdaptation("a", "s", "t", "g", {}, {}, (), (), (), ())


def test_wave2_finite_theory_upgrade_does_not_invent_lower_bound_or_epoch() -> None:
    old = SimpleNamespace(
        theory_id="old",
        domain_id="domain",
        states=frozenset({0, 1}),
        actions=frozenset({"step"}),
        transitions=frozenset({(0, "step", 1)}),
        judgments={"done": {0: False, 1: True}},
        assumptions=("a",),
        action_cost_upper_bounds={"step": 5},
        judgment_authority_ceiling={"done": 1},
    )
    upgraded = upgrade_wave2_finite_theory(old, epoch_id="bound-epoch")
    interval = upgraded.action_resources["step"][0]
    assert upgraded.epoch_id == "bound-epoch"
    assert interval.lower == 0
    assert interval.upper == 5
