"""Executable reference semantics for ORION knowledge decomposition and reuse.

The module turns the protein-digestion/recycling-centre analogy into a typed,
non-authorizing scientific pipeline:

    ingest -> decompose -> sort -> reconstruct -> reduce -> absorb
    -> recombine -> challenge -> assimilate or recycle

The analogy is only a design aid. Scientific value still depends on native
parent recovery, counter-probes, protected evaluation, resource accounting and
external authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Iterable

from .donors import DonorDisposition, DonorReductionCase, DonorReductionReceipt, reduce_donors
from .native_recovery import (
    NativeRecoveryAssessment,
    NativeRecoveryCase,
    NativeRecoveryStatus,
    assess_native_recovery_suite,
)


class KnowledgeKind(str, Enum):
    OBSERVATION = "OBSERVATION"
    CLAIM = "CLAIM"
    ASSUMPTION = "ASSUMPTION"
    METHOD = "METHOD"
    RELATION = "RELATION"
    PROCEDURE = "PROCEDURE"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    FAILURE_LESSON = "FAILURE_LESSON"
    AUTHORITY_CONSTRAINT = "AUTHORITY_CONSTRAINT"


class MetabolicStage(str, Enum):
    INGEST = "INGEST"
    DECOMPOSE = "DECOMPOSE"
    SORT = "SORT"
    NATIVE_RECONSTRUCT = "NATIVE_RECONSTRUCT"
    REDUCE = "REDUCE"
    ABSORB = "ABSORB"
    RECOMBINE = "RECOMBINE"
    CHALLENGE = "CHALLENGE"
    ASSIMILATE = "ASSIMILATE"
    RECYCLE = "RECYCLE"


class MetabolicStatus(str, Enum):
    BLOCKED_SOURCE_CUSTODY = "BLOCKED_SOURCE_CUSTODY"
    BLOCKED_DECOMPOSITION = "BLOCKED_DECOMPOSITION"
    BLOCKED_NATIVE_RECONSTRUCTION = "BLOCKED_NATIVE_RECONSTRUCTION"
    BLOCKED_NATIVE_RECOVERY = "BLOCKED_NATIVE_RECOVERY"
    BLOCKED_RECOMBINATION = "BLOCKED_RECOMBINATION"
    BLOCKED_CHALLENGE = "BLOCKED_CHALLENGE"
    BLOCKED_AUTHORITY = "BLOCKED_AUTHORITY"
    PARENT_REFUTATION_RECYCLED = "PARENT_REFUTATION_RECYCLED"
    PARENT_ASSIMILATION_READY = "PARENT_ASSIMILATION_READY"
    CONSERVATIVE_INTEGRATION_READY = "CONSERVATIVE_INTEGRATION_READY"
    STRICT_RESIDUAL_READY_FOR_PROTECTED_EVALUATION = (
        "STRICT_RESIDUAL_READY_FOR_PROTECTED_EVALUATION"
    )
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class RawKnowledgeUnit:
    unit_id: str
    kind: KnowledgeKind
    content: str
    native_term_ids: tuple[str, ...] = ()
    assumption_ids: tuple[str, ...] = ()
    counterexample_ids: tuple[str, ...] = ()
    dependence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", KnowledgeKind(self.kind))
        if not self.unit_id.strip() or not self.content.strip():
            raise ValueError("knowledge units require non-blank identity and content")
        for values in (
            self.native_term_ids,
            self.assumption_ids,
            self.counterexample_ids,
            self.dependence_ids,
        ):
            if any(not value.strip() for value in values):
                raise ValueError("knowledge-unit identity collections may not contain blanks")
            if len(values) != len(set(values)):
                raise ValueError("knowledge-unit identity collections must be unique")


@dataclass(frozen=True, slots=True)
class SourceFragment:
    fragment_id: str
    source_id: str
    source_mode: str
    content_digest: str
    authority_ceiling: int
    units: tuple[RawKnowledgeUnit, ...]
    custody_id: str = ""
    licence_or_permission_id: str = ""

    def __post_init__(self) -> None:
        for value in (
            self.fragment_id,
            self.source_id,
            self.source_mode,
            self.content_digest,
        ):
            if not value.strip():
                raise ValueError("source fragments require bound identity and digest")
        if self.authority_ceiling < 0:
            raise ValueError("authority ceiling must be non-negative")
        if not self.units:
            raise ValueError("source fragments require at least one structured unit")
        unit_ids = tuple(unit.unit_id for unit in self.units)
        if len(unit_ids) != len(set(unit_ids)):
            raise ValueError("unit identities must be unique inside a fragment")


@dataclass(frozen=True, slots=True)
class KnowledgeAtom:
    atom_id: str
    kind: KnowledgeKind
    canonical_content: str
    source_ids: tuple[str, ...]
    fragment_ids: tuple[str, ...]
    source_modes: tuple[str, ...]
    native_term_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...]
    counterexample_ids: tuple[str, ...]
    dependence_ids: tuple[str, ...]
    authority_ceiling: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", KnowledgeKind(self.kind))
        if not self.atom_id.strip() or not self.canonical_content.strip():
            raise ValueError("knowledge atoms require identity and content")
        if self.authority_ceiling < 0:
            raise ValueError("authority ceiling must be non-negative")
        for values in (
            self.source_ids,
            self.fragment_ids,
            self.source_modes,
            self.native_term_ids,
            self.assumption_ids,
            self.counterexample_ids,
            self.dependence_ids,
        ):
            if any(not value.strip() for value in values):
                raise ValueError("atom identity collections may not contain blanks")
            if len(values) != len(set(values)):
                raise ValueError("atom identity collections must be unique")


@dataclass(frozen=True, slots=True)
class RecombinationProposal:
    proposal_id: str
    statement: str
    atom_ids: tuple[str, ...]
    bridge_relation_ids: tuple[str, ...]
    intended_decision_ids: tuple[str, ...]
    discriminator_ids: tuple[str, ...]
    falsifier_ids: tuple[str, ...]
    requested_authority_level: int = 0

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.statement.strip():
            raise ValueError("recombination proposals require identity and statement")
        if self.requested_authority_level < 0:
            raise ValueError("requested authority must be non-negative")
        for name in (
            "atom_ids",
            "bridge_relation_ids",
            "intended_decision_ids",
            "discriminator_ids",
            "falsifier_ids",
        ):
            values = getattr(self, name)
            if any(not value.strip() for value in values):
                raise ValueError(f"{name} may not contain blanks")
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must be unique")


@dataclass(frozen=True, slots=True)
class MetabolicContract:
    contract_id: str
    problem_id: str
    comparison_identity: str
    registered_decision_ids: tuple[str, ...]
    required_source_modes: tuple[str, ...] = ()
    required_knowledge_kinds: tuple[KnowledgeKind, ...] = ()
    maximum_authority_level: int = 0
    require_native_recovery: bool = True
    require_discriminator: bool = True
    require_falsifier: bool = True

    def __post_init__(self) -> None:
        for value in (self.contract_id, self.problem_id, self.comparison_identity):
            if not value.strip():
                raise ValueError("metabolic contracts require bound identities")
        if not self.registered_decision_ids:
            raise ValueError("at least one registered decision is required")
        if self.maximum_authority_level < 0:
            raise ValueError("maximum authority must be non-negative")
        object.__setattr__(
            self,
            "required_knowledge_kinds",
            tuple(KnowledgeKind(item) for item in self.required_knowledge_kinds),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeMetabolismReceipt:
    contract_id: str
    proposal_id: str
    status: MetabolicStatus
    completed_stages: tuple[MetabolicStage, ...]
    atom_ids: tuple[str, ...]
    assimilated_atom_ids: tuple[str, ...]
    recycled_atom_ids: tuple[str, ...]
    donor_disposition: DonorDisposition | None
    native_recovery_statuses: tuple[NativeRecoveryStatus, ...]
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    novelty_authorized: bool = False
    adoption_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", MetabolicStatus(self.status))
        object.__setattr__(
            self,
            "completed_stages",
            tuple(MetabolicStage(stage) for stage in self.completed_stages),
        )
        if self.scientific_truth_authorized or self.novelty_authorized or self.adoption_authorized:
            raise ValueError("knowledge-metabolism receipts are non-authorizing")


def _canonical_text(value: str) -> str:
    return " ".join(value.casefold().split())


def _atom_key(unit: RawKnowledgeUnit) -> tuple[object, ...]:
    return (
        unit.kind,
        _canonical_text(unit.content),
        tuple(sorted(unit.native_term_ids)),
        tuple(sorted(unit.assumption_ids)),
    )


def decompose_and_sort_sources(
    fragments: Iterable[SourceFragment],
) -> tuple[KnowledgeAtom, ...]:
    """Decompose structured sources and merge equivalent atoms conservatively.

    Equivalent content is merged only when kind, canonical content, native terms
    and assumptions match. Provenance and dependence are unioned; authority is
    capped at the lowest contributing ceiling.
    """

    fragment_tuple = tuple(fragments)
    groups: dict[tuple[object, ...], list[tuple[SourceFragment, RawKnowledgeUnit]]] = {}
    for fragment in fragment_tuple:
        for unit in fragment.units:
            groups.setdefault(_atom_key(unit), []).append((fragment, unit))

    atoms: list[KnowledgeAtom] = []
    for key, entries in sorted(groups.items(), key=lambda item: repr(item[0])):
        kind, canonical_content, native_terms, assumptions = key
        digest_input = repr(key).encode("utf-8")
        atom_id = f"atom-{sha256(digest_input).hexdigest()[:20]}"
        atoms.append(
            KnowledgeAtom(
                atom_id=atom_id,
                kind=kind,
                canonical_content=canonical_content,
                source_ids=tuple(sorted({fragment.source_id for fragment, _ in entries})),
                fragment_ids=tuple(sorted({fragment.fragment_id for fragment, _ in entries})),
                source_modes=tuple(sorted({fragment.source_mode for fragment, _ in entries})),
                native_term_ids=native_terms,
                assumption_ids=assumptions,
                counterexample_ids=tuple(
                    sorted(
                        {
                            item
                            for _, unit in entries
                            for item in unit.counterexample_ids
                        }
                    )
                ),
                dependence_ids=tuple(
                    sorted(
                        {
                            item
                            for _, unit in entries
                            for item in unit.dependence_ids
                        }
                    )
                ),
                authority_ceiling=min(fragment.authority_ceiling for fragment, _ in entries),
            )
        )
    return tuple(atoms)


def _receipt(
    contract: MetabolicContract,
    proposal: RecombinationProposal,
    status: MetabolicStatus,
    stages: tuple[MetabolicStage, ...],
    atoms: tuple[KnowledgeAtom, ...],
    assimilated: tuple[str, ...],
    recycled: tuple[str, ...],
    donor_receipt: DonorReductionReceipt | None,
    recovery_assessments: tuple[NativeRecoveryAssessment, ...],
    *reasons: str,
) -> KnowledgeMetabolismReceipt:
    return KnowledgeMetabolismReceipt(
        contract.contract_id,
        proposal.proposal_id,
        status,
        stages,
        tuple(atom.atom_id for atom in atoms),
        assimilated,
        recycled,
        donor_receipt.disposition if donor_receipt else None,
        tuple(item.status for item in recovery_assessments),
        tuple(reasons),
    )


def run_knowledge_metabolism(
    contract: MetabolicContract,
    fragments: Iterable[SourceFragment],
    donor_case: DonorReductionCase,
    recovery_cases: tuple[NativeRecoveryCase, ...],
    proposal: RecombinationProposal,
) -> KnowledgeMetabolismReceipt:
    """Run the fail-closed ORION decomposition–absorption lifecycle."""

    source_tuple = tuple(fragments)
    stages: list[MetabolicStage] = [MetabolicStage.INGEST]
    available_modes = {fragment.source_mode for fragment in source_tuple}
    missing_modes = tuple(sorted(set(contract.required_source_modes) - available_modes))
    custody_missing = tuple(
        sorted(
            fragment.fragment_id
            for fragment in source_tuple
            if fragment.custody_id and not fragment.licence_or_permission_id
        )
    )
    if missing_modes or custody_missing:
        reasons = []
        if missing_modes:
            reasons.append(f"missing required source modes: {', '.join(missing_modes)}")
        if custody_missing:
            reasons.append(f"custody permission unresolved: {', '.join(custody_missing)}")
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_SOURCE_CUSTODY,
            tuple(stages),
            (),
            (),
            (),
            None,
            (),
            *reasons,
        )

    atoms = decompose_and_sort_sources(source_tuple)
    stages.extend((MetabolicStage.DECOMPOSE, MetabolicStage.SORT))
    available_kinds = {atom.kind for atom in atoms}
    missing_kinds = tuple(
        item.value
        for item in contract.required_knowledge_kinds
        if item not in available_kinds
    )
    if not atoms or missing_kinds:
        reason = "no knowledge atoms were produced"
        if missing_kinds:
            reason = f"missing required knowledge kinds: {', '.join(sorted(missing_kinds))}"
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_DECOMPOSITION,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            None,
            (),
            reason,
        )

    donor_receipt = reduce_donors(donor_case)
    stages.extend((MetabolicStage.NATIVE_RECONSTRUCT, MetabolicStage.REDUCE))
    if donor_receipt.disposition in {
        DonorDisposition.BLOCKED_NATIVE_RECONSTRUCTION,
        DonorDisposition.BLOCKED_MAPPING,
    }:
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_NATIVE_RECONSTRUCTION,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            donor_receipt,
            (),
            *donor_receipt.reasons,
        )
    if donor_receipt.disposition is DonorDisposition.CANNOT_CHECK:
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.CANNOT_CHECK,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            donor_receipt,
            (),
            *donor_receipt.reasons,
        )
    if donor_receipt.disposition is DonorDisposition.REFUTED_BY_PARENT:
        stages.append(MetabolicStage.RECYCLE)
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.PARENT_REFUTATION_RECYCLED,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            donor_receipt,
            (),
            *donor_receipt.reasons,
        )

    recovery_assessments: tuple[NativeRecoveryAssessment, ...] = ()
    if recovery_cases:
        recovery_assessments, recovery_summary = assess_native_recovery_suite(recovery_cases)
        if contract.require_native_recovery and not recovery_summary.all_valid:
            return _receipt(
                contract,
                proposal,
                MetabolicStatus.BLOCKED_NATIVE_RECOVERY,
                tuple(stages),
                atoms,
                (),
                tuple(atom.atom_id for atom in atoms),
                donor_receipt,
                recovery_assessments,
                "one or more native judgments, assumptions or counterexamples were not recovered",
            )
    elif contract.require_native_recovery:
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_NATIVE_RECOVERY,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            donor_receipt,
            (),
            "native recovery is required but no recovery case was supplied",
        )
    stages.append(MetabolicStage.ABSORB)

    atom_by_id = {atom.atom_id: atom for atom in atoms}
    unknown_atoms = tuple(sorted(set(proposal.atom_ids) - set(atom_by_id)))
    if not proposal.atom_ids or unknown_atoms or not proposal.bridge_relation_ids:
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_RECOMBINATION,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            donor_receipt,
            recovery_assessments,
            "proposal must bind known atoms and at least one bridge relation",
            *(f"unknown atom {item}" for item in unknown_atoms),
        )
    stages.append(MetabolicStage.RECOMBINE)

    missing_challenge = (
        (contract.require_discriminator and not proposal.discriminator_ids)
        or (contract.require_falsifier and not proposal.falsifier_ids)
    )
    if missing_challenge:
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_CHALLENGE,
            tuple(stages),
            atoms,
            (),
            tuple(atom.atom_id for atom in atoms),
            donor_receipt,
            recovery_assessments,
            "proposal lacks a required discriminator or falsifier",
        )
    stages.append(MetabolicStage.CHALLENGE)

    used_atoms = tuple(sorted(set(proposal.atom_ids)))
    recycled_atoms = tuple(sorted(set(atom_by_id) - set(used_atoms)))
    weakest_authority = min(atom_by_id[item].authority_ceiling for item in used_atoms)
    authority_ceiling = min(weakest_authority, contract.maximum_authority_level)
    if proposal.requested_authority_level > authority_ceiling:
        return _receipt(
            contract,
            proposal,
            MetabolicStatus.BLOCKED_AUTHORITY,
            tuple(stages),
            atoms,
            (),
            tuple(sorted(set(atom_by_id))),
            donor_receipt,
            recovery_assessments,
            "proposal requests authority above the weakest absorbed source or contract ceiling",
        )

    stages.append(MetabolicStage.ASSIMILATE)
    if recycled_atoms:
        stages.append(MetabolicStage.RECYCLE)

    if donor_receipt.disposition in {
        DonorDisposition.ABSORBED_SPECIAL_CASE,
        DonorDisposition.IDEAL_DONOR_PRODUCT_EQUIVALENCE,
    }:
        status = MetabolicStatus.PARENT_ASSIMILATION_READY
    elif donor_receipt.disposition is DonorDisposition.CONSERVATIVE_ENVELOPE:
        status = MetabolicStatus.CONSERVATIVE_INTEGRATION_READY
    elif donor_receipt.disposition is DonorDisposition.CANDIDATE_STRICT_RESIDUAL:
        status = MetabolicStatus.STRICT_RESIDUAL_READY_FOR_PROTECTED_EVALUATION
    else:
        status = MetabolicStatus.CANNOT_CHECK

    return _receipt(
        contract,
        proposal,
        status,
        tuple(stages),
        atoms,
        used_atoms,
        recycled_atoms,
        donor_receipt,
        recovery_assessments,
        "reference assimilation complete; protected scientific evaluation remains required",
    )
