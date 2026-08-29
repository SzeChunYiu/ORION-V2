"""Cross-layer integration semantics for the ORION-V2 research framework.

This module does not contain domain-specific discovery lessons. It supplies the
fail-closed control interface connecting native solving, parent recovery,
transfer discovery, conceptual development, formalism genesis, empirical
expansion and recursive meta-learning.

The central rule is minimum sufficient escalation: a more elaborate research
mode is not admissible while a cheaper registered alternative remains
unevaluated or sufficient.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Iterable


def _ids(values: Iterable[str], *, name: str, allow_empty: bool = True) -> tuple[str, ...]:
    result = tuple(values)
    if not allow_empty and not result:
        raise ValueError(f"{name} must not be empty")
    if any(not value.strip() for value in result):
        raise ValueError(f"{name} may not contain blank identities")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} identities must be unique")
    return result


class FrameworkLayer(StrEnum):
    SCIENTIFIC_EPISODE = "L0_SCIENTIFIC_EPISODE"
    KNOWLEDGE_METABOLISM = "L1_KNOWLEDGE_METABOLISM"
    TRANSFER_DISCOVERY = "L2_TRANSFER_DISCOVERY"
    CONCEPTUAL_DEVELOPMENT = "L3_CONCEPTUAL_DEVELOPMENT"
    FORMAL_MECHANICS = "L4_FORMAL_MECHANICS"
    FORMALISM_GENESIS = "L5_FORMALISM_GENESIS"
    DEVELOPMENT_OPERATOR = "L6_DEVELOPMENT_OPERATOR"
    DEVELOPMENT_META_POLICY = "L7_DEVELOPMENT_META_POLICY"
    RECURSIVE_PRINCIPLE = "L8_PLUS_RECURSIVE_PRINCIPLE"


class DevelopmentMode(StrEnum):
    NATIVE_DIRECT = "NATIVE_DIRECT"
    STRONGEST_PARENT = "STRONGEST_PARENT"
    TRANSFER_DISCOVERY = "TRANSFER_DISCOVERY"
    CONCEPTUAL_DEVELOPMENT = "CONCEPTUAL_DEVELOPMENT"
    FORMALISM_GENESIS = "FORMALISM_GENESIS"
    EMPIRICAL_EXPANSION = "EMPIRICAL_EXPANSION"
    RECURSIVE_META_LEARNING = "RECURSIVE_META_LEARNING"
    ABSTAIN = "ABSTAIN"


MODE_LAYER = {
    DevelopmentMode.NATIVE_DIRECT: FrameworkLayer.SCIENTIFIC_EPISODE,
    DevelopmentMode.STRONGEST_PARENT: FrameworkLayer.FORMAL_MECHANICS,
    DevelopmentMode.TRANSFER_DISCOVERY: FrameworkLayer.TRANSFER_DISCOVERY,
    DevelopmentMode.CONCEPTUAL_DEVELOPMENT: FrameworkLayer.CONCEPTUAL_DEVELOPMENT,
    DevelopmentMode.FORMALISM_GENESIS: FrameworkLayer.FORMALISM_GENESIS,
    DevelopmentMode.EMPIRICAL_EXPANSION: FrameworkLayer.SCIENTIFIC_EPISODE,
    DevelopmentMode.RECURSIVE_META_LEARNING: FrameworkLayer.DEVELOPMENT_META_POLICY,
    DevelopmentMode.ABSTAIN: FrameworkLayer.SCIENTIFIC_EPISODE,
}


class ModeAssessmentStatus(StrEnum):
    ADMISSIBLE = "ADMISSIBLE"
    SIMPLE_OR_PARENT_SUFFICIENT = "SIMPLE_OR_PARENT_SUFFICIENT"
    BLOCKED_UNRESOLVED_CHEAPER_ALTERNATIVE = "BLOCKED_UNRESOLVED_CHEAPER_ALTERNATIVE"
    BLOCKED_MISSING_MODE_WITNESS = "BLOCKED_MISSING_MODE_WITNESS"
    BLOCKED_UNFROZEN_PROSPECTIVE_IDENTITY = "BLOCKED_UNFROZEN_PROSPECTIVE_IDENTITY"
    BLOCKED_AUTHORITY_OR_RESOURCE = "BLOCKED_AUTHORITY_OR_RESOURCE"
    SAFE_ABSTAIN = "SAFE_ABSTAIN"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class RegisteredAlternative:
    alternative_id: str
    mode: DevelopmentMode
    expected_resource_cost: float
    evaluated: bool
    sufficient: bool | None
    critical_failure_observed: bool = False
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.alternative_id.strip():
            raise ValueError("alternatives require an identity")
        object.__setattr__(self, "mode", DevelopmentMode(self.mode))
        if self.expected_resource_cost < 0:
            raise ValueError("expected_resource_cost cannot be negative")
        object.__setattr__(self, "evidence_ids", _ids(self.evidence_ids, name="evidence_ids"))
        if not self.evaluated and self.sufficient is not None:
            raise ValueError("unevaluated alternatives cannot have a sufficiency verdict")


@dataclass(frozen=True, slots=True)
class ModeWitnessBundle:
    native_parent_ids: tuple[str, ...] = ()
    donor_candidate_ids: tuple[str, ...] = ()
    negative_transfer_probe_ids: tuple[str, ...] = ()
    concept_deficit_witness_ids: tuple[str, ...] = ()
    representational_deficit_witness_ids: tuple[str, ...] = ()
    semantic_validation_plan_ids: tuple[str, ...] = ()
    predecessor_recovery_plan_ids: tuple[str, ...] = ()
    missing_observation_ids: tuple[str, ...] = ()
    measurement_plan_ids: tuple[str, ...] = ()
    population_episode_ids: tuple[str, ...] = ()
    lower_level_saturation_receipt_ids: tuple[str, ...] = ()
    heldout_route_ids: tuple[str, ...] = ()
    counterexample_or_obstruction_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            object.__setattr__(self, name, _ids(getattr(self, name), name=name))


@dataclass(frozen=True, slots=True)
class DevelopmentModeProposal:
    proposal_id: str
    episode_id: str
    mode: DevelopmentMode
    target_obligation_ids: tuple[str, ...]
    prospective_identity_frozen: bool
    expected_resource_cost: float
    expected_new_consequence_ids: tuple[str, ...] = ()
    requested_authority_level: int = 0

    def __post_init__(self) -> None:
        for value in (self.proposal_id, self.episode_id):
            if not value.strip():
                raise ValueError("mode proposals require identities")
        object.__setattr__(self, "mode", DevelopmentMode(self.mode))
        object.__setattr__(self, "target_obligation_ids", _ids(self.target_obligation_ids, name="target_obligation_ids", allow_empty=False))
        object.__setattr__(self, "expected_new_consequence_ids", _ids(self.expected_new_consequence_ids, name="expected_new_consequence_ids"))
        if self.expected_resource_cost < 0:
            raise ValueError("expected_resource_cost cannot be negative")
        if self.requested_authority_level < 0:
            raise ValueError("requested authority cannot be negative")


@dataclass(frozen=True, slots=True)
class ModeAssessmentContext:
    alternatives: tuple[RegisteredAlternative, ...]
    witnesses: ModeWitnessBundle
    authority_ceiling: int
    resource_budget: float
    current_mode_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.authority_ceiling < 0 or self.resource_budget < 0:
            raise ValueError("authority ceiling and resource budget must be non-negative")
        object.__setattr__(self, "current_mode_ids", _ids(self.current_mode_ids, name="current_mode_ids"))
        alternative_ids = [item.alternative_id for item in self.alternatives]
        if len(alternative_ids) != len(set(alternative_ids)):
            raise ValueError("alternative identities must be unique")


@dataclass(frozen=True, slots=True)
class DevelopmentModeReceipt:
    proposal_id: str
    mode: DevelopmentMode
    layer: FrameworkLayer
    status: ModeAssessmentStatus
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    theory_revision_authorized: bool = False
    publication_readiness_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "mode", DevelopmentMode(self.mode))
        object.__setattr__(self, "layer", FrameworkLayer(self.layer))
        object.__setattr__(self, "status", ModeAssessmentStatus(self.status))
        if self.scientific_truth_authorized or self.theory_revision_authorized or self.publication_readiness_authorized:
            raise ValueError("mode receipts are non-authorizing")


def _required_mode_witnesses(mode: DevelopmentMode, w: ModeWitnessBundle) -> tuple[str, ...]:
    missing: list[str] = []
    if mode in {DevelopmentMode.NATIVE_DIRECT, DevelopmentMode.STRONGEST_PARENT}:
        if not w.native_parent_ids:
            missing.append("native_parent_ids")
    elif mode is DevelopmentMode.TRANSFER_DISCOVERY:
        if not w.donor_candidate_ids:
            missing.append("donor_candidate_ids")
        if not w.negative_transfer_probe_ids:
            missing.append("negative_transfer_probe_ids")
    elif mode is DevelopmentMode.CONCEPTUAL_DEVELOPMENT:
        if not w.concept_deficit_witness_ids:
            missing.append("concept_deficit_witness_ids")
        if not w.counterexample_or_obstruction_ids:
            missing.append("counterexample_or_obstruction_ids")
    elif mode is DevelopmentMode.FORMALISM_GENESIS:
        if not w.representational_deficit_witness_ids:
            missing.append("representational_deficit_witness_ids")
        if not w.semantic_validation_plan_ids:
            missing.append("semantic_validation_plan_ids")
        if not w.predecessor_recovery_plan_ids:
            missing.append("predecessor_recovery_plan_ids")
        if not w.counterexample_or_obstruction_ids:
            missing.append("counterexample_or_obstruction_ids")
    elif mode is DevelopmentMode.EMPIRICAL_EXPANSION:
        if not w.missing_observation_ids:
            missing.append("missing_observation_ids")
        if not w.measurement_plan_ids:
            missing.append("measurement_plan_ids")
    elif mode is DevelopmentMode.RECURSIVE_META_LEARNING:
        if len(w.population_episode_ids) < 2:
            missing.append("population_episode_ids>=2")
        if not w.lower_level_saturation_receipt_ids:
            missing.append("lower_level_saturation_receipt_ids")
        if not w.heldout_route_ids:
            missing.append("heldout_route_ids")
    return tuple(missing)


def assess_mode_proposal(proposal: DevelopmentModeProposal, context: ModeAssessmentContext) -> DevelopmentModeReceipt:
    """Evaluate minimum-sufficient escalation without prescribing domain content."""

    if proposal.requested_authority_level > context.authority_ceiling:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.BLOCKED_AUTHORITY_OR_RESOURCE, ("requested authority exceeds the episode authority ceiling",))
    if proposal.expected_resource_cost > context.resource_budget:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.BLOCKED_AUTHORITY_OR_RESOURCE, ("proposal exceeds the registered resource budget",))
    if proposal.mode is DevelopmentMode.ABSTAIN:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.SAFE_ABSTAIN, ("abstention preserves unresolved obligations without fabricating completion",))
    if not proposal.prospective_identity_frozen:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.BLOCKED_UNFROZEN_PROSPECTIVE_IDENTITY, ("research-mode identity was not frozen before outcome access",))

    missing = _required_mode_witnesses(proposal.mode, context.witnesses)
    if missing:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.BLOCKED_MISSING_MODE_WITNESS, tuple(f"missing {item}" for item in missing))

    cheaper_or_equal = tuple(a for a in context.alternatives if a.mode is not proposal.mode and a.expected_resource_cost <= proposal.expected_resource_cost and not a.critical_failure_observed)
    sufficient = tuple(a for a in cheaper_or_equal if a.evaluated and a.sufficient is True)
    if sufficient:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.SIMPLE_OR_PARENT_SUFFICIENT, tuple(f"{a.alternative_id} ({a.mode}) is already sufficient at equal/lower registered cost" for a in sufficient))
    unresolved = tuple(a for a in cheaper_or_equal if not a.evaluated or a.sufficient is None)
    if unresolved:
        return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.BLOCKED_UNRESOLVED_CHEAPER_ALTERNATIVE, tuple(f"{a.alternative_id} ({a.mode}) remains an unresolved equal/lower-cost alternative" for a in unresolved))

    if proposal.mode is DevelopmentMode.FORMALISM_GENESIS:
        required = {DevelopmentMode.STRONGEST_PARENT, DevelopmentMode.EMPIRICAL_EXPANSION}
        missing_modes = required - {a.mode for a in context.alternatives}
        if missing_modes:
            return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.CANNOT_CHECK, tuple(f"formalism-genesis comparison is missing {mode.value}" for mode in sorted(missing_modes, key=lambda item: item.value)))

    return DevelopmentModeReceipt(proposal.proposal_id, proposal.mode, MODE_LAYER[proposal.mode], ModeAssessmentStatus.ADMISSIBLE, ("proposal satisfies mode witnesses and no equal/lower-cost registered alternative remains sufficient or unresolved",))


class MemoryKind(StrEnum):
    KNOWLEDGE = "KNOWLEDGE"
    TRANSFER = "TRANSFER"
    CONCEPT = "CONCEPT"
    FORMALISM = "FORMALISM"
    DEVELOPMENT_OPERATOR = "DEVELOPMENT_OPERATOR"
    META_PRINCIPLE = "META_PRINCIPLE"
    FAILURE = "FAILURE"


@dataclass(frozen=True, slots=True)
class FrameworkMemoryEntry:
    entry_id: str
    kind: MemoryKind
    source_ids: tuple[str, ...]
    predecessor_entry_ids: tuple[str, ...]
    scope_ids: tuple[str, ...]
    disposition: str
    payload_digest: str
    reopen_condition_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.entry_id.strip() or not self.disposition.strip():
            raise ValueError("memory entries require identity and disposition")
        object.__setattr__(self, "kind", MemoryKind(self.kind))
        for name in ("source_ids", "predecessor_entry_ids", "scope_ids", "reopen_condition_ids"):
            object.__setattr__(self, name, _ids(getattr(self, name), name=name))
        if len(self.payload_digest) != 64 or any(ch not in "0123456789abcdef" for ch in self.payload_digest):
            raise ValueError("payload_digest must be a lowercase sha256 hex digest")


@dataclass(frozen=True, slots=True)
class FrameworkMemoryLedger:
    entries: tuple[FrameworkMemoryEntry, ...] = ()

    def __post_init__(self) -> None:
        ids = [entry.entry_id for entry in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("memory ledger entry identities must be unique")
        known: set[str] = set()
        for entry in self.entries:
            if not set(entry.predecessor_entry_ids).issubset(known):
                raise ValueError("memory entries may reference only earlier predecessors")
            known.add(entry.entry_id)

    def append(self, *, entry_id: str, kind: MemoryKind, source_ids: Iterable[str], predecessor_entry_ids: Iterable[str], scope_ids: Iterable[str], disposition: str, payload: str, reopen_condition_ids: Iterable[str] = ()) -> "FrameworkMemoryLedger":
        if any(entry.entry_id == entry_id for entry in self.entries):
            raise ValueError("memory entry identity already exists")
        entry = FrameworkMemoryEntry(entry_id=entry_id, kind=kind, source_ids=tuple(source_ids), predecessor_entry_ids=tuple(predecessor_entry_ids), scope_ids=tuple(scope_ids), disposition=disposition, payload_digest=sha256(payload.encode("utf-8")).hexdigest(), reopen_condition_ids=tuple(reopen_condition_ids))
        return FrameworkMemoryLedger(self.entries + (entry,))


def framework_layers() -> tuple[FrameworkLayer, ...]:
    return tuple(FrameworkLayer)
