from __future__ import annotations

import subprocess

from scripts.materialize_orion_solver_workspaces import test_infrastructure_error as baseline_infra_error
from scripts.run_orion_real_problem_suite import _bugsinpy_test_infrastructure_error


def _result(text: str, *, returncode: int = 1) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["test"], returncode, stdout=text, stderr="")


def test_dependency_import_failure_is_not_a_reproduced_bug() -> None:
    result = _result("ImportError while loading conftest: No module named 'numpy'")
    assert baseline_infra_error(result)
    assert _bugsinpy_test_infrastructure_error(result)


def test_assertion_failure_is_an_eligible_native_bug_failure() -> None:
    result = _result("FAILED test_mod.py::test_value - AssertionError: 1 != 2")
    assert not baseline_infra_error(result)
    assert not _bugsinpy_test_infrastructure_error(result)


def test_pytest_usage_error_is_infrastructure_not_a_reproduced_bug() -> None:
    result = _result("ERROR: file not found: pandas/tests/test_missing.py", returncode=4)
    assert baseline_infra_error(result)
    assert _bugsinpy_test_infrastructure_error(result)


def test_missing_test_selector_is_infrastructure_even_if_exit_code_is_not_four() -> None:
    result = _result("ERROR: file not found: pandas/tests/test_missing.py")
    assert baseline_infra_error(result)
    assert _bugsinpy_test_infrastructure_error(result)


def test_no_tests_collected_is_infrastructure_not_a_reproduced_bug() -> None:
    result = _result("collected 0 items\nno tests ran", returncode=5)
    assert baseline_infra_error(result)
    assert _bugsinpy_test_infrastructure_error(result)
