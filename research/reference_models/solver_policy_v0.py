"""Fail-closed ORION-V2 solver-policy reference model V0.

This is a tiny deterministic specification aid for known-answer cases. It is
not a V2 solver implementation and does not optimize scientific actions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class SolverDecision:
    action: str
    terminal: str | None = None
    responsibility: str | None = None
    jump_level: int | None = None
    reason: str = ""


def decide(state: Mapping[str, Any]) -> SolverDecision:
    """Apply a deliberately conservative precedence to one synthetic state.

    The order encodes known scientific separations, not a general optimal
    policy. New cases that do not match return CANNOT_CHECK.
    """

    if bool(state.get("contradiction")) or bool(state.get("global_gluing_obstruction")):
        return SolverDecision(
            action="STOP",
            terminal="CONTRADICTION_OR_OBSTRUCTION",
            reason="local commitments cannot currently form one valid global state",
        )

    if bool(state.get("all_mandatory_obligations_discharged")):
        authority = str(state.get("authority_state", "CANNOT_CHECK"))
        if authority == "AUTHORIZED" and bool(state.get("support_bound")):
            return SolverDecision(
                action="STOP",
                terminal="JUSTIFIED_SOLUTION",
                reason="all mandatory obligations, support and authority are bound",
            )
        if authority == "PENDING_EXTERNAL":
            return SolverDecision(
                action="ASK_EXTERNAL",
                terminal="AUTHORITY_REQUIRED",
                reason="candidate content is ready but adoption authority remains external",
            )
        return SolverDecision(
            action="STOP",
            terminal="CANNOT_CHECK",
            reason="obligations appear discharged but support or authority is not established",
        )

    if bool(state.get("coverage_censored")):
        return SolverDecision(
            action="STOP",
            terminal="SEARCH_ROUTE_CENSORED",
            reason="an unobserved material route cannot be treated as evidence of absence",
        )

    if bool(state.get("serial_pipeline")) and bool(state.get("candidate_generation_total_failure")):
        if bool(state.get("local_repair_available")):
            return SolverDecision(
                action="REPAIR",
                responsibility="SERIAL_UPSTREAM",
                jump_level=1,
                reason="ranking cannot explain a total upstream candidate-generation failure",
            )

    if bool(state.get("local_repair_available")) and bool(state.get("local_repair_discriminator_passed")):
        return SolverDecision(
            action="REPAIR",
            responsibility="SINGLE",
            jump_level=1,
            reason="a witnessed lower-level repair defeats higher escalation",
        )

    if bool(state.get("observationally_tied")) and bool(state.get("discriminating_intervention_available")):
        if float(state.get("resource_remaining", 0)) > 0:
            return SolverDecision(
                action="DISCRIMINATE",
                reason="an admissible intervention can separate the live alternatives",
            )

    if (
        bool(state.get("all_registered_probes_observed"))
        and bool(state.get("same_information_family_exhausted"))
        and not bool(state.get("separator_found"))
        and int(state.get("live_hypothesis_count", 0)) > 1
    ):
        return SolverDecision(
            action="STOP",
            terminal="STRUCTURALLY_NONIDENTIFIABLE",
            reason="all registered probes in the current information family fail to separate alternatives",
        )

    if bool(state.get("multiple_justified_alternatives")) and not bool(
        state.get("further_separator_available")
    ):
        return SolverDecision(
            action="STOP",
            terminal="MULTIPLE_JUSTIFIED_ALTERNATIVES",
            reason="several alternatives remain justified and no admissible separator is available",
        )

    if bool(state.get("incumbent_model_inadequacy_witnessed")):
        if bool(state.get("model_expansion_available")) and not bool(
            state.get("model_expansion_tested_and_insufficient")
        ):
            return SolverDecision(
                action="REMODEL_REABSTRACT",
                jump_level=2,
                reason="test model-class expansion before changing the governing representation",
            )
        if (
            bool(state.get("model_expansion_tested_and_insufficient"))
            and bool(state.get("representation_insufficiency_witnessed"))
        ):
            return SolverDecision(
                action="ESCALATE",
                jump_level=3,
                reason="lower model expansion failed and representation insufficiency is witnessed",
            )

    if bool(state.get("admissible_work_remains")) and float(state.get("resource_remaining", 0)) <= 0:
        return SolverDecision(
            action="STOP",
            terminal="RESOURCE_BOUND",
            reason="useful admissible work remains but the declared resource budget is exhausted",
        )

    return SolverDecision(
        action="STOP",
        terminal="CANNOT_CHECK",
        reason="the V0 reference policy has no justified decision for this state",
    )


__all__ = ["SolverDecision", "decide"]
