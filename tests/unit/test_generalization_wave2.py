from orion_v2.generalization import (
    AssumptionDisposition,
    AssumptionRecord,
    FiniteTheory,
    GeneralizationStatus,
    PreservationMode,
    TheoryTransport,
    assess_theory_transport,
)


def _native() -> FiniteTheory:
    return FiniteTheory(
        theory_id="management:stage-gate",
        domain_id="management",
        states=frozenset({"draft", "reviewed", "approved"}),
        actions=frozenset({"review", "approve"}),
        transitions=frozenset(
            {
                ("draft", "review", "reviewed"),
                ("reviewed", "approve", "approved"),
            }
        ),
        judgments={
            "may-release": {"draft": False, "reviewed": False, "approved": True},
            "audit-ready": {"draft": False, "reviewed": True, "approved": True},
        },
        assumptions=("single-approval-authority",),
        action_cost_upper_bounds={"review": 2.0, "approve": 1.0},
        judgment_authority_ceiling={"may-release": 2, "audit-ready": 1},
    )


def _generalized(cost: float = 2.0, authority: int = 2, decision: bool = True) -> FiniteTheory:
    return FiniteTheory(
        theory_id="orion:obligation-process",
        domain_id="generalized",
        states=frozenset({0, 1, 2}),
        actions=frozenset({"inspect", "authorize"}),
        transitions=frozenset({(0, "inspect", 1), (1, "authorize", 2)}),
        judgments={
            "terminal-admissible": {0: False, 1: False, 2: decision},
            "reviewed": {0: False, 1: True, 2: True},
        },
        assumptions=("authority-gate",),
        action_cost_upper_bounds={"inspect": cost, "authorize": 1.0},
        judgment_authority_ceiling={
            "terminal-admissible": authority,
            "reviewed": 1,
        },
    )


def _transport(**kwargs: object) -> TheoryTransport:
    defaults: dict[str, object] = {
        "transport_id": "transport:stage-gate",
        "native_theory_id": "management:stage-gate",
        "generalized_theory_id": "orion:obligation-process",
        "state_map": {"draft": 0, "reviewed": 1, "approved": 2},
        "action_map": {"review": "inspect", "approve": "authorize"},
        "judgment_map": {
            "may-release": "terminal-admissible",
            "audit-ready": "reviewed",
        },
        "registered_judgment_ids": ("may-release", "audit-ready"),
        "assumption_records": (
            AssumptionRecord(
                "single-approval-authority",
                AssumptionDisposition.CALIBRATED,
                ("calibration:authority-gate",),
            ),
        ),
        "source_ids": ("source:stage-gate-native",),
    }
    defaults.update(kwargs)
    return TheoryTransport(**defaults)


def test_exact_interpretation_when_structure_and_decisions_match() -> None:
    result = assess_theory_transport(_native(), _generalized(), _transport())
    assert result.status is GeneralizationStatus.EXACT_INTERPRETATION
    assert result.preserved_transition_count == 2
    assert result.preserved_judgment_cells == 6


def test_partial_decision_registration_is_decision_relative() -> None:
    result = assess_theory_transport(
        _native(),
        _generalized(),
        _transport(registered_judgment_ids=("may-release",)),
    )
    assert result.status is GeneralizationStatus.DECISION_RELATIVE_ADAPTATION


def test_assumption_erasure_fails_closed() -> None:
    result = assess_theory_transport(
        _native(),
        _generalized(),
        _transport(assumption_records=()),
    )
    assert result.status is GeneralizationStatus.INVALID_ASSUMPTION_ERASURE


def test_resource_understatement_fails_closed() -> None:
    result = assess_theory_transport(_native(), _generalized(cost=1.0), _transport())
    assert result.status is GeneralizationStatus.INVALID_RESOURCE_UNDERSTATEMENT


def test_authority_amplification_fails_closed() -> None:
    result = assess_theory_transport(
        _native(),
        _generalized(authority=3),
        _transport(),
    )
    assert result.status is GeneralizationStatus.INVALID_AUTHORITY_AMPLIFICATION


def test_decision_drift_fails_closed() -> None:
    result = assess_theory_transport(
        _native(),
        _generalized(decision=False),
        _transport(),
    )
    assert result.status is GeneralizationStatus.INVALID_NATIVE_JUDGMENT_DRIFT


def test_sound_overapproximation_can_preserve_native_outcome() -> None:
    generalized = FiniteTheory(
        theory_id="orion:abstract",
        domain_id="generalized",
        states=frozenset({0, 1}),
        actions=frozenset({"advance"}),
        transitions=frozenset({(0, "advance", 1)}),
        judgments={
            "outcome": {
                0: frozenset({"fail", "pass"}),
                1: frozenset({"pass"}),
            }
        },
        assumptions=("abstract",),
        action_cost_upper_bounds={"advance": 1.0},
        judgment_authority_ceiling={"outcome": 0},
    )
    native = FiniteTheory(
        theory_id="native",
        domain_id="science",
        states=frozenset({"a", "b"}),
        actions=frozenset({"go"}),
        transitions=frozenset({("a", "go", "b")}),
        judgments={"result": {"a": "fail", "b": "pass"}},
        assumptions=("abstract",),
        action_cost_upper_bounds={"go": 1.0},
        judgment_authority_ceiling={"result": 0},
    )
    transport = TheoryTransport(
        "t",
        "native",
        "orion:abstract",
        {"a": 0, "b": 1},
        {"go": "advance"},
        {"result": "outcome"},
        ("result",),
        (AssumptionRecord("abstract", AssumptionDisposition.PRESERVED),),
        PreservationMode.SOUND_OVER_APPROXIMATION,
        source_ids=("source",),
    )
    assert (
        assess_theory_transport(native, generalized, transport).status
        is GeneralizationStatus.SOUND_ABSTRACTION
    )


def test_two_remote_domains_can_share_an_envelope_without_semantic_identity() -> None:
    from orion_v2.generalization import SharedEnvelopeStatus, assess_shared_envelope

    engineering = FiniteTheory(
        theory_id="engineering:v-model",
        domain_id="engineering",
        states=frozenset({"specified", "verified", "released"}),
        actions=frozenset({"verify", "release"}),
        transitions=frozenset(
            {
                ("specified", "verify", "verified"),
                ("verified", "release", "released"),
            }
        ),
        judgments={
            "may-deploy": {
                "specified": False,
                "verified": False,
                "released": True,
            },
            "evidence-ready": {
                "specified": False,
                "verified": True,
                "released": True,
            },
        },
        assumptions=("single-change-authority",),
        action_cost_upper_bounds={"verify": 2.0, "release": 1.0},
        judgment_authority_ceiling={"may-deploy": 2, "evidence-ready": 1},
    )
    engineering_transport = TheoryTransport(
        "transport:v-model",
        "engineering:v-model",
        "orion:obligation-process",
        {"specified": 0, "verified": 1, "released": 2},
        {"verify": "inspect", "release": "authorize"},
        {
            "may-deploy": "terminal-admissible",
            "evidence-ready": "reviewed",
        },
        ("may-deploy", "evidence-ready"),
        (
            AssumptionRecord(
                "single-change-authority",
                AssumptionDisposition.CALIBRATED,
                ("calibration:authority-gate",),
            ),
        ),
        source_ids=("source:v-model",),
    )
    result = assess_shared_envelope(
        _native(),
        engineering,
        _generalized(),
        _transport(),
        engineering_transport,
    )
    assert result.status is SharedEnvelopeStatus.SHARED_EXACT_ENVELOPE
    assert result.shared_generalized_judgment_ids == (
        "reviewed",
        "terminal-admissible",
    )
    assert result.semantic_identity_claimed is False


def test_transition_drift_is_not_generalization() -> None:
    generalized = FiniteTheory(
        theory_id="orion:obligation-process",
        domain_id="generalized",
        states=frozenset({0, 1, 2}),
        actions=frozenset({"inspect", "authorize"}),
        transitions=frozenset({(0, "authorize", 2)}),
        judgments={
            "terminal-admissible": {0: False, 1: False, 2: True},
            "reviewed": {0: False, 1: True, 2: True},
        },
        assumptions=("authority-gate",),
        action_cost_upper_bounds={"inspect": 2.0, "authorize": 1.0},
        judgment_authority_ceiling={"terminal-admissible": 2, "reviewed": 1},
    )
    assert (
        assess_theory_transport(_native(), generalized, _transport()).status
        is GeneralizationStatus.INVALID_TRANSITION_DRIFT
    )
