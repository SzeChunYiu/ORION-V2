from dataclasses import dataclass

from orion_v2.generalization_compiler import (
    AdaptationContract,
    AdaptationStatus,
    EnvelopeStatus,
    assess_adaptation_contract,
    compile_decision_envelope,
    judgment_preserved_by_envelope,
)


@dataclass(frozen=True)
class Theory:
    states: frozenset[str]
    actions: frozenset[str]
    transitions: frozenset[tuple[str, str, str]]
    judgments: dict[str, dict[str, object]]
    assumptions: tuple[str, ...] = ()


def test_compiler_builds_coarsest_decision_and_transition_preserving_envelope() -> None:
    theory = Theory(
        frozenset({"a", "b", "c"}),
        frozenset({"step"}),
        frozenset(
            {
                ("a", "step", "c"),
                ("b", "step", "c"),
                ("c", "step", "c"),
            }
        ),
        {"decision": {"a": "open", "b": "open", "c": "closed"}},
    )
    envelope = compile_decision_envelope(theory, ("decision",))
    assert envelope.status is EnvelopeStatus.COMPILED_DECISION_RELATIVE
    assert frozenset({"a", "b"}) in envelope.blocks
    assert frozenset({"c"}) in envelope.blocks


def test_future_query_exposes_loss_hidden_by_current_decision() -> None:
    theory = Theory(
        frozenset({"a", "b"}),
        frozenset({"stay"}),
        frozenset({("a", "stay", "a"), ("b", "stay", "b")}),
        {"current": {"a": 0, "b": 0}},
    )
    envelope = compile_decision_envelope(theory, ("current",))
    assert (
        judgment_preserved_by_envelope(envelope, {"a": 1, "b": 2})
        is False
    )


def test_adaptation_requires_roles_calibration_tests_authority_and_epochs() -> None:
    blocked = AdaptationContract(
        "contract",
        ("measurement", "decision"),
        {"measurement": "assay"},
        ("scale",),
        (),
        (),
        "",
        "source-v1",
        "target-v1",
    )
    assert assess_adaptation_contract(blocked) is AdaptationStatus.BLOCKED_ROLE_MAP
    ready = AdaptationContract(
        "contract",
        ("measurement", "decision"),
        {"measurement": "assay", "decision": "clinical-call"},
        ("scale",),
        ("scale",),
        ("target-known-answer",),
        "external-authority",
        "source-v1",
        "target-v1",
    )
    assert (
        assess_adaptation_contract(ready)
        is AdaptationStatus.READY_FOR_TARGET_NATIVE_VALIDATION
    )
