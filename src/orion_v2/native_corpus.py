from __future__ import annotations

from .correspondence import (
    CorrespondenceLink,
    assess_correspondence_chain,
)
from .evidence_network import (
    DependenceCluster,
    EvidenceItem,
    assess_evidence_network,
)
from .frontier_portfolio import (
    FrontierOpportunity,
    assess_frontier_portfolio,
)
from .generalization_compiler import AdaptationContract
from .information_order import (
    FiniteExperiment,
    compare_experiments,
)
from .native_recovery import NativeRecoveryCase
from .performative_dynamics import (
    FinitePerformativeSystem,
    assess_performative_dynamics,
)
from .process_network import (
    ObligationProcessNetwork,
    ProcessTask,
    assess_process_soundness,
)
from .responsibility import (
    DiagnosticProbe,
    ResponsibilityHypothesis,
    ResponsibilityTopology,
    assess_responsibility,
)
from .scale_gluing import ContextualModel, assess_gluing
from .viability import (
    FiniteViabilitySystem,
    ViabilityMode,
    justified_capture_kernel,
    viability_kernel,
)


def _recovery_case(
    case_id: str,
    domain_id: str,
    family: str,
    native_judgment: object,
    generalized_judgment: object,
    *,
    assumptions: tuple[str, ...],
    source_ids: tuple[str, ...],
    counterexamples: tuple[str, ...] = (),
) -> NativeRecoveryCase:
    return NativeRecoveryCase(
        case_id=case_id,
        domain_id=domain_id,
        theory_family_id=family,
        native_judgment=native_judgment,
        generalized_judgment=generalized_judgment,
        native_to_generalized={native_judgment: generalized_judgment},
        native_assumption_ids=assumptions,
        mapped_assumption_ids=assumptions,
        native_counterexample_ids=counterexamples,
        reflected_counterexample_ids=counterexamples,
        source_ids=source_ids,
    )


def _manufacturing_network(*, quality_evidence: bool) -> ObligationProcessNetwork:
    return ObligationProcessNetwork(
        network_id=(
            "manufacturing-release"
            if quality_evidence
            else "manufacturing-release-missing-evidence"
        ),
        obligations=frozenset({"design", "verified", "released"}),
        initial_fulfilled=frozenset({"design"}),
        terminal_obligations=frozenset({"released"}),
        tasks=(
            ProcessTask(
                "quality-verification",
                frozenset({"design"}),
                frozenset({"verified"}),
                evidence_required=frozenset({"qa-record"}),
            ),
            ProcessTask(
                "release-approval",
                frozenset({"verified"}),
                frozenset({"released"}),
                authority_required=1,
            ),
        ),
        available_evidence=(
            frozenset({"qa-record"}) if quality_evidence else frozenset()
        ),
        authority_ceiling=1,
    )


def _legal_authority_network() -> ObligationProcessNetwork:
    return ObligationProcessNetwork(
        network_id="administrative-decision",
        obligations=frozenset({"petition", "hearing", "decision"}),
        initial_fulfilled=frozenset({"petition"}),
        terminal_obligations=frozenset({"decision"}),
        tasks=(
            ProcessTask(
                "conduct-hearing",
                frozenset({"petition"}),
                frozenset({"hearing"}),
                authority_required=2,
            ),
            ProcessTask(
                "issue-decision",
                frozenset({"hearing"}),
                frozenset({"decision"}),
                authority_required=2,
            ),
        ),
        authority_ceiling=1,
    )


def _engineering_diagnosis() -> str:
    hypotheses = (
        ResponsibilityHypothesis(
            "pump-fault",
            frozenset({"pump"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"alarm"}),
        ),
        ResponsibilityHypothesis(
            "valve-fault",
            frozenset({"valve"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"alarm"}),
        ),
    )
    probe = DiagnosticProbe(
        "pressure-profile",
        {"pump-fault": "low-inlet", "valve-fault": "high-inlet"},
        cost=1.0,
    )
    return assess_responsibility(
        frozenset({"alarm"}), hypotheses, (probe,)
    ).status.value


def _medical_interaction_diagnosis() -> str:
    hypotheses = (
        ResponsibilityHypothesis(
            "pathogen-a",
            frozenset({"a"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"fever"}),
        ),
        ResponsibilityHypothesis(
            "pathogen-b",
            frozenset({"b"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"cough"}),
        ),
        ResponsibilityHypothesis(
            "interaction",
            frozenset({"a", "b"}),
            ResponsibilityTopology.INTERACTION_ONLY,
            frozenset({"fever", "cough"}),
        ),
    )
    return assess_responsibility(
        frozenset({"fever", "cough"}), hypotheses
    ).status.value


def _correspondence_results() -> tuple[str, str, str, str]:
    metrology = assess_correspondence_chain(
        (
            CorrespondenceLink(
                "calibration-link",
                "instrument-v1",
                "instrument-v2",
                ("calibration-function",),
                ("reference-standard",),
                ("unit", "measurement-procedure"),
                valid_context_ids=("laboratory",),
                exact=True,
            ),
        ),
        context_id="laboratory",
        required_invariant_ids=("unit", "measurement-procedure"),
        tolerance=0.0,
    ).status.value
    psychometrics = assess_correspondence_chain(
        (
            CorrespondenceLink(
                "form-link",
                "form-a",
                "form-b",
                ("score-link",),
                ("anchor-items",),
                ("construct",),
                uncertainty_upper_bound=0.03,
                valid_context_ids=("population-p",),
                semantic_loss_ids=("dropped-item-content",),
            ),
        ),
        context_id="population-p",
        required_invariant_ids=("construct",),
        tolerance=0.05,
    ).status.value
    politics = assess_correspondence_chain(
        (
            CorrespondenceLink(
                "ideal-point-link",
                "legislature-a",
                "legislature-b",
                ("common-scale-map",),
                ("bridge-legislators",),
                (),
                valid_context_ids=("roll-call",),
                violated_invariant_ids=("latent-policy-space",),
            ),
        ),
        context_id="roll-call",
        required_invariant_ids=("latent-policy-space",),
        tolerance=0.1,
    ).status.value
    linguistics = assess_correspondence_chain(
        (
            CorrespondenceLink(
                "sense-link",
                "corpus-t1",
                "corpus-t2",
                ("embedding-alignment",),
                ("anchor-lexemes",),
                (),
                valid_context_ids=("historical-corpus",),
                unresolved_invariant_ids=("sense-identity",),
            ),
        ),
        context_id="historical-corpus",
        required_invariant_ids=("sense-identity",),
        tolerance=0.2,
    ).status.value
    return metrology, psychometrics, politics, linguistics


def _control_viability() -> tuple[frozenset[str], frozenset[str]]:
    system = FiniteViabilitySystem(
        "robust-control",
        frozenset({"stable", "boundary", "failure"}),
        {
            ("stable", "hold"): frozenset({"stable"}),
            ("boundary", "control"): frozenset({"stable", "failure"}),
        },
        {
            "stable": frozenset({"hold"}),
            "boundary": frozenset({"control"}),
            "failure": frozenset(),
        },
        frozenset({"stable", "boundary"}),
        frozenset({"stable"}),
    )
    return (
        viability_kernel(system, mode=ViabilityMode.ROBUST),
        viability_kernel(system, mode=ViabilityMode.EXISTENTIAL),
    )


def _education_capture() -> frozenset[str]:
    system = FiniteViabilitySystem(
        "learning-space",
        frozenset({"novice", "basics", "mastery"}),
        {
            ("novice", "learn-basics"): frozenset({"basics"}),
            ("basics", "learn-advanced"): frozenset({"mastery"}),
            ("mastery", "practice"): frozenset({"mastery"}),
        },
        {
            "novice": frozenset({"learn-basics"}),
            "basics": frozenset({"learn-advanced"}),
            "mastery": frozenset({"practice"}),
        },
        frozenset({"novice", "basics", "mastery"}),
        frozenset({"mastery"}),
    )
    return justified_capture_kernel(system, mode=ViabilityMode.ROBUST)


def _gluing_result() -> str:
    model = ContextualModel(
        "parity-obstruction",
        ("x", "y", "z"),
        {"x": (0, 1), "y": (0, 1), "z": (0, 1)},
        {
            "xy": ("x", "y"),
            "yz": ("y", "z"),
            "xz": ("x", "z"),
        },
        {
            "xy": frozenset({(0, 0), (1, 1)}),
            "yz": frozenset({(0, 0), (1, 1)}),
            "xz": frozenset({(0, 1), (1, 0)}),
        },
    )
    return assess_gluing(model).value


def _information_result() -> str:
    perfect = FiniteExperiment(
        "perfect",
        (0, 1),
        ("zero", "one"),
        {
            0: {"zero": 1.0, "one": 0.0},
            1: {"zero": 0.0, "one": 1.0},
        },
    )
    constant = FiniteExperiment(
        "constant",
        (0, 1),
        ("x",),
        {0: {"x": 1.0}, 1: {"x": 1.0}},
    )
    garbling = {"zero": {"x": 1.0}, "one": {"x": 1.0}}
    return compare_experiments(
        perfect,
        constant,
        left_to_right_garbling=garbling,
    ).value


def _evidence_result() -> float:
    items = tuple(EvidenceItem(f"validator-{i}", 1, 1.0, 2) for i in range(4))
    cluster = DependenceCluster(
        "shared-model",
        tuple(item.evidence_id for item in items),
        0.5,
        "model-lineage",
    )
    result = assess_evidence_network(items, (cluster,))
    if result.effective_count is None:
        raise AssertionError("constructed dependence case must be identified")
    return result.effective_count


def _performative_result() -> str:
    system = FinitePerformativeSystem(
        "benchmark-response",
        ("A", "B"),
        ("good", "bad"),
        {
            "A": {"good": 0.1, "bad": 0.9},
            "B": {"good": 0.9, "bad": 0.1},
        },
        {
            ("A", "good"): 0.0,
            ("A", "bad"): 1.0,
            ("B", "good"): 0.4,
            ("B", "bad"): 0.4,
        },
    )
    return assess_performative_dynamics(
        system, {"good": 0.9, "bad": 0.1}
    ).value


def _frontier_result() -> str:
    opportunities = (
        FrontierOpportunity(
            "importance-heavy",
            5,
            1,
            1,
            1,
            1,
            2,
            0.1,
            frozenset({"biology"}),
            ("decision",),
        ),
        FrontierOpportunity(
            "information-heavy",
            1,
            5,
            1,
            1,
            1,
            2,
            0.1,
            frozenset({"physics"}),
            ("decision",),
        ),
    )
    status, _ = assess_frontier_portfolio(
        opportunities,
        budget=2,
        risk_limit=1,
        agenda_authority_bound=True,
    )
    return status.value


def built_in_native_recovery_cases() -> tuple[NativeRecoveryCase, ...]:
    manufacturing_sound = assess_process_soundness(
        _manufacturing_network(quality_evidence=True)
    ).status.value
    manufacturing_missing = assess_process_soundness(
        _manufacturing_network(quality_evidence=False)
    ).status.value
    legal_authority = assess_process_soundness(_legal_authority_network()).status.value
    metrology, psychometrics, politics, linguistics = _correspondence_results()
    robust, existential = _control_viability()
    return (
        _recovery_case(
            "NR04-01",
            "manufacturing-quality",
            "G02-1",
            "WORKFLOW_SOUND",
            manufacturing_sound,
            assumptions=("qa-evidence", "release-authority", "finite-task-model"),
            source_ids=("van-der-aalst-workflow",),
        ),
        _recovery_case(
            "NR04-02",
            "manufacturing-quality",
            "G02-1",
            "QUALITY_EVIDENCE_MISSING",
            manufacturing_missing,
            assumptions=("qa-evidence-required",),
            counterexamples=("missing-qa-record",),
            source_ids=("van-der-aalst-workflow",),
        ),
        _recovery_case(
            "NR04-03",
            "administrative-law",
            "G02-1",
            "SIGNATORY_REQUIRED",
            legal_authority,
            assumptions=("jurisdictional-authority-role",),
            counterexamples=("authority-below-required-level",),
            source_ids=("legal-procedure-native-card",),
        ),
        _recovery_case(
            "NR04-04",
            "reliability-engineering",
            "G02-2",
            "ALTERNATIVES_SEPARABLE_BY_MEASUREMENT",
            _engineering_diagnosis(),
            assumptions=("component-model", "sensor-semantics"),
            counterexamples=("alarm-alone-nonidentifying",),
            source_ids=("de-kleer-williams-1987", "reiter-1987"),
        ),
        _recovery_case(
            "NR04-05",
            "medicine",
            "G02-2",
            "INTERACTION_ONLY_SYNDROME",
            _medical_interaction_diagnosis(),
            assumptions=("clinical-observation-model", "interaction-cause"),
            counterexamples=("single-cause-explanations-insufficient",),
            source_ids=("clinical-differential-native-card",),
        ),
        _recovery_case(
            "NR04-06",
            "metrology",
            "G02-3",
            "TRACEABLE_EXACT_LINK",
            metrology,
            assumptions=("reference-standard", "calibration-chain"),
            source_ids=("nist-metrological-traceability",),
        ),
        _recovery_case(
            "NR04-07",
            "psychometrics",
            "G02-3",
            "LINKED_WITH_ITEM_CONTENT_LOSS",
            psychometrics,
            assumptions=("anchor-items", "population-p", "construct-invariance"),
            counterexamples=("item-content-loss",),
            source_ids=("psychometric-equating-native-card",),
        ),
        _recovery_case(
            "NR04-08",
            "political-methodology",
            "G02-3",
            "LATENT_SCALE_INVARIANT_VIOLATED",
            politics,
            assumptions=("bridge-legislators", "common-policy-space"),
            counterexamples=("policy-space-changed",),
            source_ids=("clinton-jackman-rivers-2004",),
        ),
        _recovery_case(
            "NR04-09",
            "diachronic-linguistics",
            "G02-3",
            "SENSE_IDENTITY_UNRESOLVED",
            linguistics,
            assumptions=("corpus-alignment", "sense-inventory"),
            counterexamples=("polysemy-anchor-ambiguity",),
            source_ids=("hamilton-leskovec-jurafsky-2016",),
        ),
        _recovery_case(
            "NR04-10",
            "robust-control",
            "G02-4",
            "ROBUST_SAFE_SET",
            robust,
            assumptions=("adversarial-successor-semantics", "safe-set"),
            source_ids=("aubin-viability",),
        ),
        _recovery_case(
            "NR04-11",
            "control-planning",
            "G02-4",
            "EXISTENTIAL_SAFE_SET",
            existential,
            assumptions=("existential-successor-semantics", "safe-set"),
            source_ids=("aubin-viability",),
        ),
        _recovery_case(
            "NR04-12",
            "education-learning-space",
            "G02-4",
            "MASTERY_REACHABLE_STATES",
            _education_capture(),
            assumptions=("prerequisite-order", "mastery-target"),
            source_ids=("falmagne-doignon-learning-spaces",),
        ),
        _recovery_case(
            "NR04-13",
            "local-global-reasoning",
            "G03-2",
            "LOCALLY_VALID_GLOBALLY_INCONSISTENT",
            _gluing_result(),
            assumptions=("context-cover", "parity-constraints"),
            counterexamples=("no-global-section",),
            source_ids=("abramsky-brandenburger-2011",),
        ),
        _recovery_case(
            "NR04-14",
            "statistical-decision-theory",
            "G03-1",
            "INFORMATIVE_EXPERIMENT_DOMINATES",
            _information_result(),
            assumptions=("shared-state-space", "validated-garbling"),
            source_ids=("blackwell-1953",),
        ),
        _recovery_case(
            "NR04-15",
            "evidence-synthesis",
            "G03-3",
            "EFFECTIVE_INDEPENDENT_COUNT",
            _evidence_result(),
            assumptions=("disjoint-cluster", "rho-0.5"),
            counterexamples=("naive-count-four",),
            source_ids=("kish-design-effect", "hedges-tipton-johnson-2010"),
        ),
        _recovery_case(
            "NR04-16",
            "performative-evaluation",
            "G03-5",
            "DEPLOYMENT_REVERSES_WINNER",
            _performative_result(),
            assumptions=("policy-response-map", "protected-loss"),
            counterexamples=("static-ranking-fails",),
            source_ids=("perdomo-et-al-2020", "lucas-1976"),
        ),
        _recovery_case(
            "NR04-17",
            "research-portfolio-management",
            "G03-6",
            "INCOMPARABLE_PORTFOLIO_CHOICES",
            _frontier_result(),
            assumptions=("budget-two", "agenda-authority-bound"),
            counterexamples=("single-score-collapse",),
            source_ids=("march-1991", "lehman-stanley-2011"),
        ),
    )


def built_in_target_adaptation_contracts() -> tuple[AdaptationContract, ...]:
    return (
        AdaptationContract(
            "manufacturing-to-scientific-review",
            ("evidence-gate", "release-authority"),
            {
                "evidence-gate": "scientific-validity-review",
                "release-authority": "external-adoption-authority",
            },
            ("scientific-validity-calibration",),
            ("scientific-validity-calibration",),
            ("fresh-scientific-known-answer", "authority-hostile-control"),
            "external-scientific-authority",
            "manufacturing-v1",
            "science-v1",
        ),
        AdaptationContract(
            "engineering-diagnosis-to-medicine",
            ("cause-hypothesis", "diagnostic-probe"),
            {
                "cause-hypothesis": "clinical-differential",
                "diagnostic-probe": "clinical-test",
            },
            ("clinical-risk-calibration",),
            (),
            ("clinical-known-answer",),
            "clinical-authority",
            "engineering-v1",
            "clinical-v1",
        ),
        AdaptationContract(
            "political-scale-to-diachronic-semantics",
            ("anchor", "latent-coordinate"),
            {"anchor": "anchor-lexeme", "latent-coordinate": "semantic-axis"},
            ("sense-calibration",),
            ("sense-calibration",),
            (),
            "linguistic-domain-authority",
            "politics-v1",
            "linguistics-v1",
        ),
    )
