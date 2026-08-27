"""Candidate stable ORION-V2 kernel facade.

This module is intentionally much smaller than :mod:`orion_v2`'s research
namespace.  It exposes the scientific *interfaces* that survive Wave-06
contraction while leaving parent-owned algorithms and transparent reference
implementations in their native modules.

The facade is not frozen architecture and grants no scientific or adoption
authority.  It is the candidate subject for protected V1 parity.
"""

from __future__ import annotations

# K0 — identity, problem/authority contract and typed terminal boundary.
from .contracts import EvidenceRef, Obligation, ObligationStatus, ProblemContract, Terminal

# K1 — plural solving state and step receipts.  The current finite/reference
# solver implementation remains behind this state interface.
from .solver import SolverState, StepReceipt

# K2 — relation/transport request and receipt families.  Exact bisimulation,
# Blackwell comparison, probabilistic abstraction and other donor algorithms are
# adapters/reference methods and are intentionally not re-exported here.
from .structural import ContextProbe, RelationType, StructuralRelationReceipt
from .correspondence import (
    CorrespondenceChainAssessment,
    CorrespondenceLink,
    CorrespondenceStatus,
)

# K3 — evidence dependence, component lineage and selective revalidation.
from .evidence import DependenceEdge, DependenceKind, EvidenceDependenceAssessment, EvidenceUnit
from .provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance
from .reopening import (
    Commitment,
    CommitmentDisposition,
    SelectiveReopenReceipt,
    SupportFamily,
)

# K4 — action/diagnosis/workflow interfaces.  Selection, probe-set search,
# process-net analysis and domain-specific diagnosis algorithms remain adapters.
from .policy import ActionProposal, ActionValue, SelectionReceipt, SelectionStatus
from .responsibility import (
    DiagnosisStatus,
    ResponsibilityAssessment,
    ResponsibilityHypothesis,
    ResponsibilityTopology,
)
from .workflow import (
    PrecedenceConstraint,
    WorkflowConformanceReceipt,
    WorkflowConformanceStatus,
    WorkflowSpec,
    WorkflowTask,
)

# K5 — frontier opportunity and escalation proposal states.  Portfolio/R&D
# optimization is a replaceable parent policy rather than a stable primitive.
from .opportunity import OpportunityStatus, ResearchOpportunityCandidate
from .jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, TriggerKind

# K6 — parity, saturation and closeout interfaces.  Local status never grants
# external scientific/publication authority.
from .evaluation import CapabilityParityRecord, ParityDisposition, SaturationVector
from .closure import CloseoutAssessment, CloseoutInputs, CloseoutStatus


KERNEL_API_VERSION = "wave06-candidate-v1"
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
    "PrecedenceConstraint",
    "WorkflowConformanceReceipt",
    "WorkflowConformanceStatus",
    "WorkflowSpec",
    "WorkflowTask",
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
