"""Candidate stable ORION-V2 kernel facade.

This module is intentionally much smaller than :mod:`orion_v2`'s research
namespace. It exposes only scientific interface objects that survive Wave-06
contraction. Parent-owned algorithms, compatibility layers and transparent
reference implementations remain importable from their native modules but are
not universal kernel primitives.

The facade is not frozen architecture and grants no scientific, novelty,
publication or adoption authority. It is the candidate subject for protected
V1 parity.
"""

from __future__ import annotations

# K0 — identity, problem/authority contract and typed terminal boundary.
from .contracts import EvidenceRef, Obligation, ObligationStatus, ProblemContract, Terminal

# K1 — plural solving state and step receipts. The current finite/reference
# solver operations remain behind this state interface.
from .solver import SolverState, StepReceipt

# K2 — single-context relation and cross-epoch/chain transport contracts.
# Bisimulation, Blackwell comparison, generalization compilers, stochastic
# abstraction and other donor algorithms remain adapters/reference methods.
from .structural import ContextProbe, RelationType, StructuralRelationReceipt
from .correspondence import (
    CorrespondenceChainAssessment,
    CorrespondenceLink,
    CorrespondenceStatus,
)

# K3 — evidence dependence, lineage and selective revalidation.
from .evidence import DependenceEdge, DependenceKind, EvidenceDependenceAssessment, EvidenceUnit
from .provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance
from .reopening import (
    Commitment,
    CommitmentDisposition,
    SelectiveReopenReceipt,
    SupportFamily,
)

# K4 — action and diagnosis contracts only. Workflow/process-net scheduling,
# separating-probe search and other control algorithms are replaceable parents.
from .policy import ActionProposal, ActionValue, SelectionReceipt, SelectionStatus
from .responsibility import (
    DiagnosisStatus,
    ResponsibilityAssessment,
    ResponsibilityHypothesis,
    ResponsibilityTopology,
)

# K5 — frontier opportunity and escalation proposal states. Portfolio/R&D
# optimization is a replaceable parent policy rather than a stable primitive.
from .opportunity import OpportunityStatus, ResearchOpportunityCandidate
from .jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, TriggerKind

# K6 — parity, saturation and closeout interfaces. Local status never grants
# external scientific/publication authority.
from .evaluation import CapabilityParityRecord, ParityDisposition, SaturationVector
from .closure import CloseoutAssessment, CloseoutInputs, CloseoutStatus


KERNEL_API_VERSION = "wave06-candidate-v2"
KERNEL_FROZEN = False
GRANTS_ARCHITECTURE_AUTHORITY = False
GRANTS_SCIENTIFIC_TRUTH = False
GRANTS_NOVELTY = False
GRANTS_PUBLICATION_AUTHORITY = False


__all__ = (
    # K0
    "EvidenceRef",
    "Obligation",
    "ObligationStatus",
    "ProblemContract",
    "Terminal",
    # K1
    "SolverState",
    "StepReceipt",
    # K2
    "ContextProbe",
    "RelationType",
    "StructuralRelationReceipt",
    "CorrespondenceChainAssessment",
    "CorrespondenceLink",
    "CorrespondenceStatus",
    # K3
    "DependenceEdge",
    "DependenceKind",
    "EvidenceDependenceAssessment",
    "EvidenceUnit",
    "InheritanceRelation",
    "ProvenanceEdge",
    "ProvenanceNode",
    "ReticulateProvenance",
    "Commitment",
    "CommitmentDisposition",
    "SelectiveReopenReceipt",
    "SupportFamily",
    # K4
    "ActionProposal",
    "ActionValue",
    "SelectionReceipt",
    "SelectionStatus",
    "DiagnosisStatus",
    "ResponsibilityAssessment",
    "ResponsibilityHypothesis",
    "ResponsibilityTopology",
    # K5
    "OpportunityStatus",
    "ResearchOpportunityCandidate",
    "JumpAssessment",
    "JumpLevel",
    "JumpProposal",
    "JumpTrigger",
    "TriggerKind",
    # K6
    "CapabilityParityRecord",
    "ParityDisposition",
    "SaturationVector",
    "CloseoutAssessment",
    "CloseoutInputs",
    "CloseoutStatus",
    # boundary metadata
    "KERNEL_API_VERSION",
    "KERNEL_FROZEN",
    "GRANTS_ARCHITECTURE_AUTHORITY",
    "GRANTS_SCIENTIFIC_TRUTH",
    "GRANTS_NOVELTY",
    "GRANTS_PUBLICATION_AUTHORITY",
)
