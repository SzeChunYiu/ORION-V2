from orion_v2.policy import (
    ActionProposal,
    ActionValue,
    SelectionStatus,
    select_actions,
)


def test_hard_gate_failure_cannot_be_compensated_by_value() -> None:
    unsafe = ActionProposal(
        "unsafe",
        "experiment",
        ActionValue(False, scientific_value=1000),
    )
    safe = ActionProposal(
        "safe",
        "query",
        ActionValue(True, obligation_reduction=1, cost=1),
    )
    receipt = select_actions((unsafe, safe))
    assert receipt.status is SelectionStatus.UNIQUE
    assert receipt.selected_action_ids == ("safe",)
    assert receipt.rejected_gate_action_ids == ("unsafe",)


def test_incomparable_actions_remain_a_pareto_set() -> None:
    informative = ActionProposal(
        "informative",
        "experiment",
        ActionValue(True, distinguishing_power=5, cost=5),
    )
    cheap = ActionProposal(
        "cheap",
        "query",
        ActionValue(True, distinguishing_power=1, cost=1),
    )
    receipt = select_actions((informative, cheap))
    assert receipt.status is SelectionStatus.PARETO_SET
    assert set(receipt.selected_action_ids) == {"informative", "cheap"}
