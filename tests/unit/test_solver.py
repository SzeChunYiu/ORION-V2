from orion_v2.contracts import Obligation, ObligationStatus, ProblemContract, Terminal
from orion_v2.solver import SolverState, StepReceipt, apply_step, infer_terminal


def _contract(authority: bool = False) -> ProblemContract:
    return ProblemContract(
        "problem",
        "answer",
        "scientific-claim",
        ("declared scope",),
        authority_requirements=("external-review",) if authority else (),
        resource_budget=10,
    )


def test_solution_requires_hard_obligations_and_authority() -> None:
    state = SolverState(
        state_id="s0",
        contract=_contract(authority=True),
        obligations=(Obligation("o", "verify", ObligationStatus.SATISFIED),),
        remaining_resource=10,
    )
    assert infer_terminal(state) is Terminal.AUTHORITY_REQUIRED


def test_structural_nonidentifiability_is_not_resource_failure() -> None:
    state = SolverState(
        state_id="s0",
        contract=_contract(),
        obligations=(
            Obligation("o", "identify target", ObligationStatus.NONIDENTIFIABLE),
        ),
        remaining_resource=0,
    )
    assert infer_terminal(state) is Terminal.STRUCTURALLY_NONIDENTIFIABLE


def test_step_receipt_updates_state_and_resource() -> None:
    open_obligation = Obligation("o", "verify")
    state = SolverState(
        state_id="s0",
        contract=_contract(),
        obligations=(open_obligation,),
        remaining_resource=5,
    )
    satisfied = Obligation("o", "verify", ObligationStatus.SATISFIED)
    receipt = StepReceipt("step", "check", "s0", "s1", cost=2)
    updated = apply_step(state, receipt, obligations=(satisfied,))
    assert updated.remaining_resource == 3
    assert updated.terminal is Terminal.JUSTIFIED_SOLUTION
