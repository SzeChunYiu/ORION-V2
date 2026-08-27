"""Reference objects for the ORION-V2 research programme.

This package is intentionally small and non-authorizing. It provides exact,
replayable objects for known-answer tests while the broader scientific design
remains under donor saturation and protected evaluation.
"""

from .comparability import Anchor, ComparabilityCertificate, ComparabilityStatus
from .contracts import EvidenceRef, Obligation, ObligationStatus, ProblemContract, Terminal
from .donors import (
    DomainProblem,
    DonorDisposition,
    DonorReductionCase,
    DonorReductionReceipt,
    reduce_donors,
)
from .evaluation import CapabilityParityRecord, ParityDisposition, SaturationVector
from .evidence import (
    DependenceEdge,
    DependenceKind,
    EvidenceDependenceAssessment,
    EvidenceUnit,
    assess_evidence_dependence,
)
from .jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, assess_jump
from .performative import EvaluationDeployment, PerformativeAssessment, assess_performative_evaluation
from .policy import ActionProposal, ActionValue, SelectionReceipt, select_actions
from .provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance
from .solver import SolverState, StepReceipt, apply_step, infer_terminal
from .structural import (
    ContextProbe,
    FiniteTransitionSystem,
    RelationType,
    StructuralRelationReceipt,
    are_bisimilar,
    indiscernibility_classes,
    safe_quotient,
)

__all__ = [
    "ActionProposal", "ActionValue", "Anchor", "CapabilityParityRecord",
    "ComparabilityCertificate", "ComparabilityStatus", "ContextProbe",
    "DependenceEdge", "DependenceKind", "DomainProblem", "DonorDisposition",
    "DonorReductionCase", "DonorReductionReceipt", "EvaluationDeployment",
    "EvidenceDependenceAssessment", "EvidenceRef", "EvidenceUnit",
    "FiniteTransitionSystem", "InheritanceRelation", "JumpAssessment",
    "JumpLevel", "JumpProposal", "JumpTrigger", "Obligation",
    "ObligationStatus", "ParityDisposition", "PerformativeAssessment",
    "ProblemContract", "ProvenanceEdge", "ProvenanceNode", "RelationType",
    "ReticulateProvenance", "SaturationVector", "SelectionReceipt",
    "SolverState", "StepReceipt", "StructuralRelationReceipt", "Terminal",
    "apply_step", "are_bisimilar", "assess_evidence_dependence", "assess_jump",
    "assess_performative_evaluation", "indiscernibility_classes",
    "infer_terminal", "reduce_donors", "safe_quotient", "select_actions"
]
