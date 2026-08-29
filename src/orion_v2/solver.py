from __future__ import annotations

from dataclasses import dataclass, replace

from .contracts import Obligation, ObligationStatus, ProblemContract, Terminal
from .policy import ActionProposal


@dataclass(frozen=True, slots=True)
class StepReceipt:
    step_id: str
    action_id: str
    input_state_id: str
    output_state_id: str
    evidence_ids: tuple[str, ...] = ()
    cost: float = 0.0
    execution_succeeded: bool = True
    scientific_terminal_authorized: bool = False

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (self.step_id, self.action_id, self.input_state_id, self.output_state_id)
        ):
            raise ValueError("step receipt identities must be non-blank")
        if self.cost < 0:
            raise ValueError("cost must be non-negative")
        if self.scientific_terminal_authorized:
            raise ValueError("a step receipt cannot self-authorize a scientific terminal")


@dataclass(frozen=True, slots=True)
class SolverState:
    state_id: str
    contract: ProblemContract
    obligations: tuple[Obligation, ...]
    hypotheses: tuple[str, ...] = ()
    admissible_actions: tuple[ActionProposal, ...] = ()
    history: tuple[StepReceipt, ...] = ()
    remaining_resource: float = 0.0
    authority_satisfied: bool = False
    contradiction: bool = False
    representation_insufficient: bool = False
    method_family_insufficient: bool = False
    terminal: Terminal | None = None

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-blank")
        if self.remaining_resource < 0:
            raise ValueError("remaining_resource must be non-negative")
        ids = [obligation.obligation_id for obligation in self.obligations]
        if len(ids) != len(set(ids)):
            raise ValueError("obligation identities must be unique")
        action_ids = [action.action_id for action in self.admissible_actions]
        if len(action_ids) != len(set(action_ids)):
            raise ValueError("action identities must be unique")


def infer_terminal(state: SolverState) -> Terminal | None:
    if state.contradiction:
        return Terminal.CONTRADICTION_OR_OBSTRUCTION
    if state.representation_insufficient:
        return Terminal.REPRESENTATION_INSUFFICIENT
    if state.method_family_insufficient:
        return Terminal.METHOD_FAMILY_INSUFFICIENT

    statuses = {obligation.status for obligation in state.obligations if obligation.hard}
    if ObligationStatus.NONIDENTIFIABLE in statuses:
        return Terminal.STRUCTURALLY_NONIDENTIFIABLE
    if ObligationStatus.CENSORED in statuses:
        return Terminal.SEARCH_ROUTE_CENSORED
    if ObligationStatus.AUTHORITY_BLOCKED in statuses:
        return Terminal.AUTHORITY_REQUIRED
    if ObligationStatus.CANNOT_CHECK in statuses:
        return Terminal.CANNOT_CHECK
    if ObligationStatus.DEFEATED in statuses:
        return Terminal.REFUTED

    all_hard_satisfied = all(
        obligation.status is ObligationStatus.SATISFIED
        for obligation in state.obligations
        if obligation.hard
    )
    any_soft_open = any(
        obligation.status is ObligationStatus.OPEN
        for obligation in state.obligations
        if not obligation.hard
    )
    if all_hard_satisfied:
        if state.contract.requires_authority() and not state.authority_satisfied:
            return Terminal.AUTHORITY_REQUIRED
        return Terminal.JUSTIFIED_PARTIAL_RESULT if any_soft_open else Terminal.JUSTIFIED_SOLUTION

    if state.remaining_resource == 0 and any(
        obligation.status is ObligationStatus.OPEN for obligation in state.obligations
    ):
        return Terminal.RESOURCE_BOUND
    return None


def apply_step(
    state: SolverState,
    receipt: StepReceipt,
    *,
    obligations: tuple[Obligation, ...] | None = None,
    remaining_resource: float | None = None,
) -> SolverState:
    if receipt.input_state_id != state.state_id:
        raise ValueError("step receipt does not bind the input solver state")
    if receipt.cost > state.remaining_resource:
        raise ValueError("step cost exceeds remaining resource")
    new_resource = state.remaining_resource - receipt.cost if remaining_resource is None else remaining_resource
    if new_resource < 0:
        raise ValueError("remaining resource cannot be negative")
    updated = replace(
        state,
        state_id=receipt.output_state_id,
        obligations=state.obligations if obligations is None else obligations,
        history=(*state.history, receipt),
        remaining_resource=new_resource,
        terminal=None,
    )
    return replace(updated, terminal=infer_terminal(updated))
