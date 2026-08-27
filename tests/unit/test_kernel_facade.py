from __future__ import annotations

import orion_v2
import orion_v2.kernel as kernel


def test_kernel_facade_is_explicitly_non_authorizing_and_unfrozen() -> None:
    assert kernel.KERNEL_API_VERSION == "wave06-candidate-v2"
    assert kernel.KERNEL_FROZEN is False
    assert kernel.GRANTS_ARCHITECTURE_AUTHORITY is False
    assert kernel.GRANTS_SCIENTIFIC_TRUTH is False
    assert kernel.GRANTS_NOVELTY is False
    assert kernel.GRANTS_PUBLICATION_AUTHORITY is False


def test_kernel_facade_covers_all_seven_interface_families() -> None:
    required = {
        # K0
        "ProblemContract",
        "Obligation",
        # K1
        "SolverState",
        "StepReceipt",
        # K2
        "ContextProbe",
        "StructuralRelationReceipt",
        "CorrespondenceLink",
        # K3
        "EvidenceUnit",
        "ReticulateProvenance",
        "SelectiveReopenReceipt",
        # K4
        "ActionProposal",
        "ResponsibilityHypothesis",
        # K5
        "ResearchOpportunityCandidate",
        "JumpProposal",
        # K6
        "CapabilityParityRecord",
        "SaturationVector",
        "CloseoutStatus",
    }
    assert required <= set(kernel.__all__)


def test_parent_reference_algorithms_and_workflow_are_not_universal_kernel_exports() -> None:
    forbidden = {
        "are_bisimilar",
        "bisimulation_relation",
        "compare_experiments",
        "decision_value",
        "viability_kernel",
        "justified_capture_kernel",
        "assess_process_soundness",
        "performative_optima",
        "retraining_trajectory",
        "compile_decision_envelope",
        "assess_theory_transport",
        "assess_native_recovery",
        "assess_evidence_network",
        "pareto_frontier_portfolios",
        "select_actions",
        "minimum_separating_probe_set",
        "WorkflowSpec",
        "WorkflowTask",
        "WorkflowConformanceReceipt",
    }
    assert forbidden.isdisjoint(kernel.__all__)
    for name in forbidden:
        assert not hasattr(kernel, name)


def test_legacy_comparability_certificate_is_not_a_third_k2_owner() -> None:
    assert "ComparabilityCertificate" not in kernel.__all__
    assert not hasattr(kernel, "ComparabilityCertificate")


def test_package_root_cannot_reexpand_reference_implementations() -> None:
    expected_root = {
        "kernel",
        "KERNEL_API_VERSION",
        "KERNEL_FROZEN",
        "GRANTS_ARCHITECTURE_AUTHORITY",
        "GRANTS_SCIENTIFIC_TRUTH",
        "GRANTS_NOVELTY",
        "GRANTS_PUBLICATION_AUTHORITY",
    }
    assert set(orion_v2.__all__) == expected_root
    for name in (
        "FiniteTheory",
        "ComparabilityCertificate",
        "FrontierPortfolio",
        "WorkflowSpec",
        "FiniteViabilitySystem",
        "TheoryTransport",
    ):
        assert not hasattr(orion_v2, name)


def test_facade_exports_only_declared_symbols() -> None:
    for name in kernel.__all__:
        assert hasattr(kernel, name), name
