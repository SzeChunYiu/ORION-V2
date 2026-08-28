from __future__ import annotations

import subprocess

from scripts.materialize_orion_solver_workspaces import test_infrastructure_error as baseline_infra_error
from scripts.run_orion_real_problem_suite import _bugsinpy_test_infrastructure_error


def _result(text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["test"], 1, stdout=text, stderr="")


def test_dependency_import_failure_is_not_a_reproduced_bug() -> None:
    result = _result("ImportError while loading conftest: No module named 'numpy'")
    assert baseline_infra_error(result)
    assert _bugsinpy_test_infrastructure_error(result)


def test_assertion_failure_is_an_eligible_native_bug_failure() -> None:
    result = _result("FAILED test_mod.py::test_value - AssertionError: 1 != 2")
    assert not baseline_infra_error(result)
    assert not _bugsinpy_test_infrastructure_error(result)
