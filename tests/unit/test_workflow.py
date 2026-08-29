import pytest
from orion_v2.workflow import PrecedenceConstraint, WorkflowConformanceStatus, WorkflowSpec, WorkflowTask

def _workflow()->WorkflowSpec:
    return WorkflowSpec("research",(WorkflowTask("orient","orientation"),WorkflowTask("search","acquisition"),WorkflowTask("simulate","computation"),WorkflowTask("validate","validation")),(PrecedenceConstraint("orient","search","scope before search"),PrecedenceConstraint("search","validate","evidence before validation"),PrecedenceConstraint("simulate","validate","result before validation")))

def test_unordered_tasks_can_run_concurrently() -> None: assert _workflow().can_run_concurrently("search","simulate") is True

def test_trace_detects_required_order_violation() -> None:
    receipt=_workflow().check_trace(("validate","search")); assert receipt.status is WorkflowConformanceStatus.ORDER_VIOLATION and ("search","validate") in receipt.violated_constraints

def test_cyclic_workflow_is_rejected() -> None:
    with pytest.raises(ValueError,match="acyclic"):
        WorkflowSpec("cycle",(WorkflowTask("a","x"),WorkflowTask("b","x")),(PrecedenceConstraint("a","b","r"),PrecedenceConstraint("b","a","r")))
