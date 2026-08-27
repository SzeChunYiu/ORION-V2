"""Non-authorizing reference objects for the ORION-V2 research programme."""

from .comparability import Anchor, ComparabilityCertificate, ComparabilityStatus
from .contracts import EvidenceRef, Obligation, ObligationStatus, ProblemContract, Terminal
from .correspondence import (
    CorrespondenceChainAssessment,
    CorrespondenceLink,
    CorrespondenceStatus,
    assess_correspondence_chain,
)
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
from .evidence_network import (
    DependenceCluster,
    EvidenceItem,
    EvidenceNetworkAssessment,
    EvidenceNetworkStatus,
    assess_evidence_network,
)
from .frontier_portfolio import (
    FrontierOpportunity,
    FrontierPortfolio,
    FrontierStatus,
    assess_frontier_portfolio,
    pareto_frontier_portfolios,
)
from .generalization import (
    AssumptionDisposition,
    AssumptionRecord,
    FiniteTheory,
    GeneralizationAssessment,
    GeneralizationStatus,
    PreservationMode,
    SharedEnvelopeAssessment,
    SharedEnvelopeStatus,
    TheoryTransport,
    assess_shared_envelope,
    assess_theory_transport,
)
from .generalization_compiler import (
    AdaptationContract,
    AdaptationStatus,
    DecisionEnvelope,
    EnvelopeStatus,
    assess_adaptation_contract,
    compile_decision_envelope,
    judgment_preserved_by_envelope,
)
from .information_order import (
    DecisionProblem,
    ExperimentComparison,
    FiniteExperiment,
    compare_experiments,
    decision_value,
    validates_garbling,
)
from .inheritance import (
    ComponentInheritanceEdge,
    ComponentNode,
    InheritanceAssessment,
    InheritanceStatus,
    affected_descendants,
    assess_inheritance,
)
from .jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, assess_jump
from .opportunity import OpportunityStatus, ResearchOpportunityCandidate, assess_opportunity
from .parity import (
    CapabilityCensusValidation,
    load_and_validate_capability_census,
    validate_capability_census,
)
from .performative import (
    EvaluationDeployment,
    PerformativeAssessment,
    assess_performative_evaluation,
)
from .performative_dynamics import (
    FinitePerformativeSystem,
    PerformativeDynamicsStatus,
    assess_performative_dynamics,
    performative_optima,
    retraining_trajectory,
    stable_policies,
    static_optima,
)
from .policy import ActionProposal, ActionValue, SelectionReceipt, select_actions
from .probes import (
    Hypothesis,
    Probe,
    ProbeDesignReceipt,
    ProbeDesignStatus,
    minimum_separating_probe_set,
)
from .process_network import (
    ObligationProcessNetwork,
    ProcessMarking,
    ProcessSoundnessAssessment,
    ProcessSoundnessStatus,
    ProcessTask,
    apply_task,
    assess_process_soundness,
)
from .provenance import ProvenanceEdge, ProvenanceNode, ReticulateProvenance
from .reopening import (
    Commitment,
    CommitmentDisposition,
    SelectiveReopenReceipt,
    SupportFamily,
    selective_reopen,
)
from .responsibility import (
    DiagnosisStatus,
    DiagnosticProbe,
    ResponsibilityAssessment,
    ResponsibilityHypothesis,
    ResponsibilityTopology,
    assess_responsibility,
    minimum_diagnostic_probe_set,
)
from .scale_gluing import (
    ContextualModel,
    FiniteScaleModel,
    GluingStatus,
    ScaleMap,
    ScaleStatus,
    assess_gluing,
    assess_scale_map,
    global_sections,
)
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
from .viability import (
    FiniteViabilitySystem,
    ViabilityMode,
    justified_capture_kernel,
    viability_kernel,
)
from .workflow import (
    PrecedenceConstraint,
    WorkflowConformanceReceipt,
    WorkflowConformanceStatus,
    WorkflowSpec,
    WorkflowTask,
)

__all__ = [name for name in globals() if not name.startswith("_")]
