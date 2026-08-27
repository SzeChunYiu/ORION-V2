import pytest

from orion_v2.contracts import Obligation, ObligationStatus, ProblemContract


def test_problem_contract_rejects_empty_scope() -> None:
    with pytest.raises(ValueError, match="scope"):
        ProblemContract("p", "target", "decision", ())


def test_satisfied_obligation_cannot_keep_blockers() -> None:
    with pytest.raises(ValueError, match="blockers"):
        Obligation(
            "o",
            "must be true",
            status=ObligationStatus.SATISFIED,
            blocker_ids=("b",),
        )


def test_contract_preserves_authority_boundary() -> None:
    contract = ProblemContract(
        problem_id="problem:1",
        target="select a scientifically admissible design",
        decision_class="design",
        scope=("declared system",),
        authority_requirements=("external-adoption",),
        resource_budget=10,
    )
    assert contract.requires_authority() is True
