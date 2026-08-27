from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping, Protocol

State = Hashable
Value = Hashable | frozenset[Hashable]


class TheoryLike(Protocol):
    states: frozenset[State]
    actions: frozenset[str]
    transitions: frozenset[tuple[State, str, State]]
    judgments: Mapping[str, Mapping[State, Value]]
    assumptions: tuple[str, ...]


class EnvelopeStatus(str, Enum):
    COMPILED_EXACT = "COMPILED_EXACT"
    COMPILED_DECISION_RELATIVE = "COMPILED_DECISION_RELATIVE"
    CANNOT_CHECK_MISSING_JUDGMENT = "CANNOT_CHECK_MISSING_JUDGMENT"
    CANNOT_CHECK_EMPTY_REGISTRY = "CANNOT_CHECK_EMPTY_REGISTRY"


class AdaptationStatus(str, Enum):
    READY_FOR_TARGET_NATIVE_VALIDATION = "READY_FOR_TARGET_NATIVE_VALIDATION"
    BLOCKED_ROLE_MAP = "BLOCKED_ROLE_MAP"
    BLOCKED_CALIBRATION = "BLOCKED_CALIBRATION"
    BLOCKED_TARGET_TESTS = "BLOCKED_TARGET_TESTS"
    BLOCKED_AUTHORITY = "BLOCKED_AUTHORITY"
    BLOCKED_EPOCH = "BLOCKED_EPOCH"


@dataclass(frozen=True, slots=True)
class DecisionEnvelope:
    envelope_id: str
    registered_judgment_ids: tuple[str, ...]
    blocks: tuple[frozenset[State], ...]
    state_to_block: Mapping[State, int]
    preserves_transitions: bool
    status: EnvelopeStatus
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", EnvelopeStatus(self.status))
        if not self.envelope_id.strip():
            raise ValueError("envelope identity must be non-blank")


@dataclass(frozen=True, slots=True)
class AdaptationContract:
    contract_id: str
    required_source_roles: tuple[str, ...]
    target_role_map: Mapping[str, str]
    required_calibration_ids: tuple[str, ...]
    bound_calibration_ids: tuple[str, ...]
    target_native_test_ids: tuple[str, ...]
    authority_binding_id: str
    source_epoch: str
    target_epoch: str

    def __post_init__(self) -> None:
        if not self.contract_id.strip():
            raise ValueError("adaptation contract identity must be non-blank")
        values = (
            *self.required_source_roles,
            *self.target_role_map.keys(),
            *self.target_role_map.values(),
            *self.required_calibration_ids,
            *self.bound_calibration_ids,
            *self.target_native_test_ids,
        )
        if any(not value.strip() for value in values):
            raise ValueError("adaptation identities may not be blank")


def _canonical_blocks(
    groups: Mapping[tuple[object, ...], list[State]],
) -> tuple[frozenset[State], ...]:
    return tuple(
        frozenset(values)
        for _, values in sorted(groups.items(), key=lambda item: repr(item[0]))
    )


def compile_decision_envelope(
    theory: TheoryLike,
    registered_judgment_ids: tuple[str, ...],
    *,
    preserve_transitions: bool = True,
    envelope_id: str = "decision-envelope",
) -> DecisionEnvelope:
    if not registered_judgment_ids:
        return DecisionEnvelope(
            envelope_id,
            (),
            (),
            {},
            preserve_transitions,
            EnvelopeStatus.CANNOT_CHECK_EMPTY_REGISTRY,
        )
    missing_tables = [
        item for item in registered_judgment_ids if item not in theory.judgments
    ]
    missing_cells = [
        f"{item}:{state!r}"
        for item in registered_judgment_ids
        if item in theory.judgments
        for state in theory.states
        if state not in theory.judgments[item]
    ]
    if missing_tables or missing_cells:
        warnings = tuple(
            [f"missing judgment table {item}" for item in missing_tables]
            + [f"missing judgment cell {item}" for item in missing_cells]
        )
        return DecisionEnvelope(
            envelope_id,
            registered_judgment_ids,
            (),
            {},
            preserve_transitions,
            EnvelopeStatus.CANNOT_CHECK_MISSING_JUDGMENT,
            warnings,
        )

    groups: dict[tuple[object, ...], list[State]] = {}
    for state in theory.states:
        signature = tuple(
            theory.judgments[item][state] for item in registered_judgment_ids
        )
        groups.setdefault(signature, []).append(state)
    blocks = _canonical_blocks(groups)

    if preserve_transitions:
        changed = True
        while changed:
            changed = False
            state_to_block = {
                state: index for index, block in enumerate(blocks) for state in block
            }
            transition_index: dict[tuple[State, str], set[int]] = {}
            for source, action, target in theory.transitions:
                transition_index.setdefault((source, action), set()).add(
                    state_to_block[target]
                )
            refined: dict[tuple[object, ...], list[State]] = {}
            for state in theory.states:
                judgment_signature = tuple(
                    theory.judgments[item][state]
                    for item in registered_judgment_ids
                )
                transition_signature = tuple(
                    (
                        action,
                        tuple(
                            sorted(transition_index.get((state, action), set()))
                        ),
                    )
                    for action in sorted(theory.actions)
                )
                refined.setdefault(
                    (judgment_signature, transition_signature), []
                ).append(state)
            new_blocks = _canonical_blocks(refined)
            if set(new_blocks) != set(blocks):
                blocks = new_blocks
                changed = True

    state_to_block = {
        state: index for index, block in enumerate(blocks) for state in block
    }
    status = (
        EnvelopeStatus.COMPILED_EXACT
        if all(len(block) == 1 for block in blocks)
        else EnvelopeStatus.COMPILED_DECISION_RELATIVE
    )
    return DecisionEnvelope(
        envelope_id,
        registered_judgment_ids,
        blocks,
        state_to_block,
        preserve_transitions,
        status,
    )


def judgment_preserved_by_envelope(
    envelope: DecisionEnvelope,
    judgment: Mapping[State, Value],
) -> bool:
    if not envelope.blocks or set(judgment) != set(envelope.state_to_block):
        return False
    return all(
        len({judgment[state] for state in block}) == 1 for block in envelope.blocks
    )


def assess_adaptation_contract(contract: AdaptationContract) -> AdaptationStatus:
    missing_roles = set(contract.required_source_roles) - set(
        contract.target_role_map
    )
    if missing_roles:
        return AdaptationStatus.BLOCKED_ROLE_MAP
    missing_calibrations = set(contract.required_calibration_ids) - set(
        contract.bound_calibration_ids
    )
    if missing_calibrations:
        return AdaptationStatus.BLOCKED_CALIBRATION
    if not contract.target_native_test_ids:
        return AdaptationStatus.BLOCKED_TARGET_TESTS
    if not contract.authority_binding_id.strip():
        return AdaptationStatus.BLOCKED_AUTHORITY
    if not contract.source_epoch.strip() or not contract.target_epoch.strip():
        return AdaptationStatus.BLOCKED_EPOCH
    return AdaptationStatus.READY_FOR_TARGET_NATIVE_VALIDATION
