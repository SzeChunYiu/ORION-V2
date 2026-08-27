"""Reference objects for the ORION-V2 research programme.

This package is intentionally small and non-authorizing.  It provides exact,
replayable objects for known-answer tests while the broader scientific design
remains under donor saturation and protected evaluation.
"""

from .contracts import (
    EvidenceRef,
    Obligation,
    ObligationStatus,
    ProblemContract,
    Terminal,
)
from .evaluation import CapabilityParityRecord, ParityDisposition, SaturationVector
from .jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, assess_jump
from .policy import ActionProposal, ActionValue, SelectionReceipt, select_actions
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
    "ActionProposal",
    "ActionValue",
    "CapabilityParityRecord",
    "ContextProbe",
    "EvidenceRef",
    "FiniteTransitionSystem",
    "JumpAssessment",
    "JumpLevel",
    "JumpProposal",
    "JumpTrigger",
    "Obligation",
    "ObligationStatus",
    "ParityDisposition",
    "ProblemContract",
    "RelationType",
    "SaturationVector",
    "SelectionReceipt",
    "SolverState",
    "StepReceipt",
    "StructuralRelationReceipt",
    "Terminal",
    "apply_step",
    "are_bisimilar",
    "assess_jump",
    "indiscernibility_classes",
    "infer_terminal",
    "safe_quotient",
    "select_actions",
]
