from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class ParityExecutionStatus(str, Enum):
    INVALID_PROTOCOL = "INVALID_PROTOCOL"
    BLOCKED_SUBJECT_BINDING = "BLOCKED_SUBJECT_BINDING"
    BLOCKED_CASE_SOURCE_AUDIT = "BLOCKED_CASE_SOURCE_AUDIT"
    BLOCKED_PROTECTED_CASE_SELECTION = "BLOCKED_PROTECTED_CASE_SELECTION"
    BLOCKED_EVALUATOR_CUSTODY = "BLOCKED_EVALUATOR_CUSTODY"
    BLOCKED_PARENT_BASELINE_BINDING = "BLOCKED_PARENT_BASELINE_BINDING"
    BLOCKED_RESOURCE_BUDGET_BINDING = "BLOCKED_RESOURCE_BUDGET_BINDING"
    READY_FOR_PROTECTED_PARITY_RUN = "READY_FOR_PROTECTED_PARITY_RUN"


@dataclass(frozen=True, slots=True)
class ParityExecutionAssessment:
    status: ParityExecutionStatus
    blockers: tuple[str, ...]
    run_authorized: bool = False
    grants_v1_parity: bool = False
    grants_v2_closeout: bool = False
    grants_scientific_truth: bool = False
    grants_novelty: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", ParityExecutionStatus(self.status))
        if (
            self.grants_v1_parity
            or self.grants_v2_closeout
            or self.grants_scientific_truth
            or self.grants_novelty
        ):
            raise ValueError("parity execution gate is non-authorizing")
        if self.status is not ParityExecutionStatus.READY_FOR_PROTECTED_PARITY_RUN and self.run_authorized:
            raise ValueError("blocked parity gate cannot authorize execution")


def assess_parity_execution_readiness(
    *,
    protocol: Mapping[str, Any],
    subject_binding: Mapping[str, Any],
    case_source_audit: Mapping[str, Any],
    resource_protocol: Mapping[str, Any],
    custody_protocol: Mapping[str, Any],
    baseline_registry: Mapping[str, Any],
) -> ParityExecutionAssessment:
    """Return the first ordered execution-preflight blocker.

    This gate is deliberately distinct from a parity outcome assessor. Even the
    READY terminal only means the paired protected run may begin; it grants no
    parity result, architecture authority, scientific truth or novelty.
    """

    if (
        protocol.get("schema_version") != "orion.v2.v1-parity-campaign-protocol.v1"
        or protocol.get("status") != "DESIGN_FROZEN_V2_SUBJECT_UNBOUND"
        or not isinstance(protocol.get("run_gate"), Mapping)
        or protocol["run_gate"].get("allowed_now") is not False
    ):
        return ParityExecutionAssessment(
            ParityExecutionStatus.INVALID_PROTOCOL,
            ("prospective parity design is invalid or self-authorizing",),
        )

    if (
        subject_binding.get("schema_version") != "orion.v2.v1-parity-subject-binding.v1"
        or subject_binding.get("terminal") != "PARITY_SUBJECT_BOUND_RUN_NOT_AUTHORIZED"
        or not isinstance(subject_binding.get("v2_subject"), Mapping)
        or len(str(subject_binding["v2_subject"].get("commit", ""))) != 40
    ):
        return ParityExecutionAssessment(
            ParityExecutionStatus.BLOCKED_SUBJECT_BINDING,
            ("exact contracted V2 subject binding is missing or invalid",),
        )

    if (
        case_source_audit.get("schema_version") != "orion.v2.v1-parity-case-source-audit.v1"
        or case_source_audit.get("status") != "V1_NATIVE_SOURCES_BOUND_PROTECTED_CASE_SELECTION_OPEN"
    ):
        return ParityExecutionAssessment(
            ParityExecutionStatus.BLOCKED_CASE_SOURCE_AUDIT,
            ("frozen V1-native case-source provenance is missing or invalid",),
        )

    protected_registry = custody_protocol.get("protected_case_registry")
    if not isinstance(protected_registry, Mapping) or protected_registry.get("bound") is not True:
        return ParityExecutionAssessment(
            ParityExecutionStatus.BLOCKED_PROTECTED_CASE_SELECTION,
            ("protected held-out case identities/selection receipt are not bound",),
        )

    evaluator_registry = custody_protocol.get("evaluator_registry")
    if not isinstance(evaluator_registry, Mapping) or evaluator_registry.get("bound") is not True:
        return ParityExecutionAssessment(
            ParityExecutionStatus.BLOCKED_EVALUATOR_CUSTODY,
            ("protected evaluator/custody identities are not bound",),
        )

    implementation_bindings = baseline_registry.get("implementation_bindings")
    if not isinstance(implementation_bindings, Mapping) or implementation_bindings.get("bound") is not True:
        return ParityExecutionAssessment(
            ParityExecutionStatus.BLOCKED_PARENT_BASELINE_BINDING,
            ("strongest parent-composed comparator implementations are not bound",),
        )

    case_budget = resource_protocol.get("case_budget_manifest")
    if not isinstance(case_budget, Mapping) or case_budget.get("bound") is not True:
        return ParityExecutionAssessment(
            ParityExecutionStatus.BLOCKED_RESOURCE_BUDGET_BINDING,
            ("matched per-case provider/tool/time/compute budgets are not bound",),
        )

    for artifact_name, artifact in (
        ("resource protocol", resource_protocol),
        ("custody protocol", custody_protocol),
        ("baseline registry", baseline_registry),
    ):
        gate = artifact.get("run_gate")
        if not isinstance(gate, Mapping):
            return ParityExecutionAssessment(
                ParityExecutionStatus.INVALID_PROTOCOL,
                (f"{artifact_name} lacks a run gate",),
            )

    return ParityExecutionAssessment(
        ParityExecutionStatus.READY_FOR_PROTECTED_PARITY_RUN,
        (),
        run_authorized=True,
    )
