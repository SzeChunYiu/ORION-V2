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
from .jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, assess_jump
from .meta_formalization import (
    ConservativeExtensionAssessment,
    ConservativeExtensionStatus,
    FiniteConsequenceTheory,
    FiniteGaloisConnection,
    FiniteLens,
    FiniteLogic,
    FinitePoset,
    LawAssessment,
    LawStatus,
    SignatureMorphism,
    assess_abstract_transformer_soundness,
    assess_conservative_extension,
    assess_galois_connection,
    assess_lens_laws,
    assess_satisfaction_condition,
)
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
from .provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance
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
from .theory_transport import (
    AdaptationStatus,
    AssumptionDisposition as TransportAssumptionDisposition,
    AssumptionTreatment,
    CompositionAssessment,
    CompositionStatus,
    CounterexampleWitness,
    GeneralizationContext,
    InterpretationAssessment,
    InterpretationKind,
    InterpretationStatus,
    ResourceCalibration,
    ResourceInterval,
    ScientificTheory,
    TargetAdaptation,
    TargetAdaptationAssessment,
    TheoryInterpretation,
    TransportCertificate,
    TransportValidityBinding,
    ValidityAssessment,
    ValidityStatus,
    assess_interpretation,
    assess_target_adaptation,
    assess_transport_validity,
    compose_transport_certificates,
    upgrade_wave2_finite_theory,
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
