#!/usr/bin/env python3
"""PC-R6 full-regression evaluator lane over the frozen E30-R11 / E60 proposals.

Implements section 3 of PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1 (registered
2026-09-02).  Zero model calls: the only native compute is re-running frozen
proposals through the frozen per-project runtimes and executing the frozen
per-task test suite.

Custody rules honoured here
  * The frozen-lane adapter (`run/e30_r11_arm_eval_frozen_lane.py`, sha256
    829abb41...) is IMPORTED and its `_evaluate_bugsinpy` closure executed
    verbatim for workspace provisioning, patch application, compile and the
    registered failing test.  The full-regression suite is attached through a
    runtime proxy that wraps `execute_test_binding` (registered test first,
    verbatim; then the suite in the same compiled workspace).  Nothing in the
    adapter's decision surface is forked or modified.
  * Read-only over the frozen campaign trees: every write lands under the PC-R6
    campaign directory; scratch workspaces are per evaluation and removed by
    the adapter itself.
  * No imputation: non-applying / non-compiling / timed-out / uncollected
    evaluations carry `critical_new_failure_count = None` with a reason code.
  * Every input file read enters a sha256 manifest (`manifest` stage for the
    frozen input set; per-stage read manifests for everything else).
  * Gold-blind except in the `gr0b` stage, which reads BugsInPy gold patches for
    the registered known-answer control and marks its records
    `gold_or_fixed_solution_accessed = True`.

Stages
  manifest   hash the frozen input set, derive the campaign id
  gr0a       --execute --index N : re-run the registered failing test (adapter
             verbatim, no suite) for one (cell, task); without --execute:
             collect + diff against the frozen native_success vectors
  gr0b       gold-patch known-answer control on the frozen 5-task subset
  gr0        combine gr0a + gr0b receipts into PC_R6_GR0_RECEIPT.json
  suite      --index N : baseline pass + every arm x rep patched pass for one
             (cell, task)
  rollup     collect suite records into PC_R6_FULLREG_RAW_ROLLUP_V1.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

LANE_VERSION = "orion.v2.pc-r6-fullreg-evaluator-lane.v2"
DESIGN_ID = "PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1"
SEED = 20260902
SUITE_TIMEOUT_SECONDS = 900  # frozen, design section 3
FROZEN_LANE_TIMEOUT_SECONDS = 10800  # compile + registered test, as the frozen lane ran
FROZEN_ADAPTER_SHA256 = "829abb411ccf0bd71182eea4c11d2e07fae60f3b743872f7b4fce0a8635aae93"
FROZEN_ADAPTER_VERSION = "orion.v2.e30-r11-frozen-lane-arm-eval-adapter.v3"

CELLS: dict[str, dict[str, Any]] = {
    "e30r11": {
        "campaign": "campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6",
        "arms": ["F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION",
                 "SAME_MODEL_REFLECTION", "SIMPLE_DIRECT"],
        "reps": ["1", "2", "3"],
        "evaluations": 480,
        "truth": "E30_R11_TERMINAL_RAW_ROLLUP.json paired_task_table (in-repo, freeze 4663435c...)",
    },
    "e60": {
        "campaign": "campaign-e60-r1-component-ablation-20260829-38aedc50",
        "arms": ["F2_ORION_METABOLIC_FULL", "F2_MINUS_DECOMPOSITION",
                 "F2_MINUS_NATIVE_RECOVERY", "F2_MINUS_COUNTERPROBE",
                 "F2_MINUS_SELECTIVE_REOPEN"],
        "reps": ["1", "2", "3"],
        "evaluations": 600,
        "truth": ("frozen campaign evaluation records (600) anchored to in-repo "
                  "E60 arm_summaries / component_effects paired tables / supersede.sha256"),
    },
}
CELL_ORDER = ["e30r11", "e60"]

# Baseline pass = the SAME adapter path with a marker patch that only creates one
# untracked dotfile at the workspace root (git apply refuses empty input, so an
# honest no-op patch must create something).  Recorded as amendment A3.
BASELINE_MARKER_PATCH = (
    "diff --git a/.orion-pc-r6-baseline-marker b/.orion-pc-r6-baseline-marker\n"
    "new file mode 100644\n"
    "--- /dev/null\n"
    "+++ b/.orion-pc-r6-baseline-marker\n"
    "@@ -0,0 +1 @@\n"
    "+PC-R6 baseline pass: no proposal patch applied\n"
)
BASELINE_ARM_ID = "PC_R6_BASELINE"
GR0B_ARM_ID = "PC_R6_GOLD_CONTROL"
GR0B_TASK_COUNT = 5
GR0B_SELECTION_RULE = (
    "projects in lexicographic order; within a project tasks in bug_id order; a task "
    "whose gold source patch cannot flip the registered failing test because the "
    "frozen workspace lacks a fixture that only the fixed commit adds is "
    "GOLD_NOT_APPLICABLE_MISSING_FIXTURE and the next bug_id of the same project is "
    "tried; the first five projects with an applicable control (amendments A4, A13)"
)
_MISSING_FILE_RE = re.compile(r"No such file or directory: '([^']+)'")
GOLD_PATCH_TEMPLATE = (
    "{campaign}/baseline_lanes/{task_id}/BugsInPy/projects/{project}/bugs/{bug_id}/bug_patch.txt"
)

NONE_REASONS = {
    "patch": "NONE_PATCH_NOT_APPLIED",
    "compile": "NONE_COMPILE_FAILED",
    "timeout": "NONE_SUITE_TIMEOUT",
    "uncollected": "NONE_SUITE_NOT_COLLECTED",
    "baseline": "NONE_BASELINE_UNAVAILABLE",
    "exception": "NONE_EVALUATOR_EXCEPTION",
    "uncheckable": "NONE_RESPONSE_UNCHECKABLE",
    "checkout": "NONE_WORKSPACE_CHECKOUT_FAILED",
}

# Runs one unittest module under the FROZEN environment python and records every
# test outcome as JSON (the same TestLoader `python -m unittest <module>` uses).
# Must stay Python 3.6 compatible (frozen runtimes 3.6.9 / 3.7.0 / 3.8.3).
UNITTEST_JSON_RUNNER = r'''
import json, os, sys, unittest

class _Recorder(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super(_Recorder, self).__init__(*args, **kwargs)
        self.outcomes = {}
    def _set(self, test, outcome):
        key = test.id()
        prior = self.outcomes.get(key)
        rank = {"passed": 0, "skipped": 1, "failed": 2, "error": 3}
        if prior is None or rank[outcome] > rank[prior]:
            self.outcomes[key] = outcome
    def addSuccess(self, test):
        super(_Recorder, self).addSuccess(test); self._set(test, "passed")
    def addFailure(self, test, err):
        super(_Recorder, self).addFailure(test, err); self._set(test, "failed")
    def addError(self, test, err):
        super(_Recorder, self).addError(test, err); self._set(test, "error")
    def addSkip(self, test, reason):
        super(_Recorder, self).addSkip(test, reason); self._set(test, "skipped")
    def addExpectedFailure(self, test, err):
        super(_Recorder, self).addExpectedFailure(test, err); self._set(test, "passed")
    def addUnexpectedSuccess(self, test):
        super(_Recorder, self).addUnexpectedSuccess(test); self._set(test, "failed")
    def addSubTest(self, test, subtest, err):
        super(_Recorder, self).addSubTest(test, subtest, err)
        if err is not None:
            self._set(test, "error" if issubclass(err[0], Exception) and not issubclass(err[0], test.failureException) else "failed")

def main():
    out, modules = sys.argv[1], sys.argv[2:]
    # `python -m unittest` resolves modules against the current directory; a
    # script invocation puts the script directory first instead -- restore the
    # `-m` semantics so the frozen workspace is importable exactly as registered.
    sys.path.insert(0, os.getcwd())
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(modules)
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=1, resultclass=_Recorder)
    result = runner.run(suite)
    payload = {"tests": result.outcomes, "tests_run": result.testsRun,
               "was_successful": result.wasSuccessful()}
    with open(out, "w") as handle:
        json.dump(payload, handle, sort_keys=True)
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
'''


# --------------------------------------------------------------------------- utils
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Manifest:
    """sha256 ledger of every input file this process reads."""

    def __init__(self) -> None:
        self.entries: dict[str, str] = {}

    def record(self, path: Path, label: str | None = None) -> str:
        digest = sha256_file(path)
        self.entries[label or str(path)] = digest
        return digest

    def read_json(self, path: Path, label: str | None = None) -> Any:
        self.record(path, label)
        return json.loads(path.read_text(encoding="utf-8"))

    def read_text(self, path: Path, label: str | None = None) -> str:
        self.record(path, label)
        return path.read_text(encoding="utf-8")

    def lines(self) -> list[str]:
        return [f"{digest}  {label}" for label, digest in sorted(self.entries.items())]

    def digest(self) -> str:
        return sha256_text("\n".join(self.lines()) + "\n")

    def write(self, path: Path) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.lines()) + "\n", encoding="utf-8")
        return self.digest()


class LaneError(RuntimeError):
    pass


# --------------------------------------------------------------------------- cells
class Cell:
    def __init__(self, name: str, root: Path, manifest: Manifest, *, allow_partial: bool = False):
        spec = CELLS[name]
        self.name = name
        self.root = root.resolve()
        self.spec = spec
        self.manifest = manifest
        if not allow_partial and self.root.name != spec["campaign"]:
            raise LaneError(f"{name}: campaign dir {self.root.name} != frozen {spec['campaign']}")
        self.run = self.root / "run"
        reps = [d.name[len("confirmatory-r"):] for d in sorted(self.run.glob("confirmatory-r*"))]
        if allow_partial:
            self.reps = reps
        else:
            if reps != spec["reps"]:
                raise LaneError(f"{name}: reps {reps} != frozen {spec['reps']}")
            self.reps = list(spec["reps"])
        self.frozen: dict[str, dict[str, Any]] = {}
        self.tasks: dict[str, dict[str, Any]] = {}
        for rep in self.reps:
            frozen = manifest.read_json(self.run / f"confirmatory-r{rep}" / "frozen_tasks.json",
                                        f"{name}/run/confirmatory-r{rep}/frozen_tasks.json")
            self.frozen[rep] = frozen
            table = {item["task_id"]: item for item in frozen.get("tasks", [])}
            if not self.tasks:
                self.tasks = table
            elif set(table) != set(self.tasks):
                raise LaneError(f"{name}: task set differs between reps")
        arms_seen = sorted({p.name for rep in self.reps
                            for p in (self.run / f"confirmatory-r{rep}" / "responses").glob("*")
                            if p.is_dir()})
        if allow_partial:
            self.arms = [arm for arm in spec["arms"] if arm in arms_seen]
        else:
            if arms_seen != sorted(spec["arms"]):
                raise LaneError(f"{name}: arms {arms_seen} != frozen {sorted(spec['arms'])}")
            self.arms = list(spec["arms"])
        self.task_ids = sorted(self.tasks)

    def response_path(self, rep: str, arm: str, task_id: str) -> Path:
        return self.run / f"confirmatory-r{rep}" / "responses" / arm / f"{task_id}.json"

    def evaluation_path(self, rep: str, arm: str, task_id: str) -> Path:
        return self.run / f"confirmatory-r{rep}" / "evaluations" / arm / f"{task_id}.json"

    def workspace(self, task_id: str) -> Path:
        return self.root / "evaluator_private" / task_id

    def expected_evaluations(self) -> int:
        return len(self.reps) * len(self.arms) * len(self.task_ids)


def plan_indices(cells: list[Cell]) -> list[tuple[str, str]]:
    return [(cell.name, task_id) for cell in cells for task_id in cell.task_ids]


# --------------------------------------------------------------------------- suite plan
def resolve_unittest_module(dotted: str, workspace: Path) -> tuple[str, str] | None:
    parts = dotted.split(".")
    for k in range(len(parts), 0, -1):
        rel = Path(*parts[:k])
        if (workspace / rel).with_suffix(".py").is_file():
            return ".".join(parts[:k]), str(rel.with_suffix(".py"))
        if (workspace / rel / "__init__.py").is_file():
            return ".".join(parts[:k]), str(rel / "__init__.py")
    return None


def plan_suite(support_text: str, workspace: Path, bug_info_text: str | None = None) -> dict[str, Any]:
    """Derive the frozen per-task suite from the registered test command lines.

    Suite = every test collected by the frozen runtime in the test file(s) the
    registered command references, using the registered command's own runner
    family (pytest for `pytest`/`python -m pytest`/`tox` lines, unittest for
    `python -m unittest` lines) -- amendment A1.
    """
    families: set[str] = set()
    files: list[str] = []
    modules: list[str] = []
    flags: list[str] = []
    lines: list[str] = []
    for raw in support_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
        tokens = shlex.split(line)
        head = Path(tokens[0]).name if tokens else ""
        if head == "tox":
            family, targets, line_flags = "pytest", tokens[1:], ["-q", "-o", "addopts="]
        elif head == "pytest":
            family, targets, line_flags = "pytest", tokens[1:], []
        elif head in {"python", "python3", "python3.6", "python3.7", "python3.8"} and tokens[1:3] == ["-m", "pytest"]:
            family, targets, line_flags = "pytest", tokens[3:], []
        elif head in {"python", "python3", "python3.6", "python3.7", "python3.8"} and tokens[1:3] == ["-m", "unittest"]:
            family, targets, line_flags = "unittest", tokens[3:], []
        else:
            raise LaneError(f"unsupported registered test command: {line}")
        families.add(family)
        for flag in line_flags:
            if flag not in flags:
                flags.append(flag)
        for target in targets:
            if target.startswith("-"):
                if target not in flags:
                    flags.append(target)
                continue
            if family == "pytest":
                file_part = target.split("::", 1)[0]
                if not (workspace / file_part).is_file():
                    raise LaneError(f"registered test file missing: {file_part}")
                if file_part not in files:
                    files.append(file_part)
            else:
                resolved = resolve_unittest_module(target, workspace)
                if resolved is None:
                    raise LaneError(f"cannot resolve unittest module for {target}")
                module, file_part = resolved
                if module not in modules:
                    modules.append(module)
                if file_part not in files:
                    files.append(file_part)
    if len(families) != 1:
        raise LaneError(f"mixed or empty runner families: {sorted(families)}")
    crosscheck = None
    if bug_info_text:
        declared = []
        for line in bug_info_text.splitlines():
            if line.startswith("test_file="):
                value = line.split("=", 1)[1].strip().strip('"')
                declared = [item for item in value.split(";") if item]
        crosscheck = {"bug_info_test_files": declared,
                      "matches_registered_command_files": sorted(declared) == sorted(files)}
    return {
        "runner_family": families.pop(),
        "test_files": files,
        "unittest_modules": modules,
        "pytest_flags": flags,
        "registered_lines": lines,
        "registered_lines_sha256": sha256_text("\n".join(lines)),
        "bug_info_crosscheck": crosscheck,
        "suite_definition": ("all test cases collected by the frozen runtime in the test "
                             "file(s) referenced by the registered test command; "
                             "parametrized instances count individually"),
    }


# --------------------------------------------------------------------------- suite run
def _run_with_group_kill(command: list[str], *, cwd: Path, env: dict[str, str],
                         timeout: int) -> dict[str, Any]:
    started = time.perf_counter()
    process = subprocess.Popen(command, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            stdout, stderr = process.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
    return {
        "command": command, "returncode": None if timed_out else process.returncode,
        "timed_out": timed_out, "wall_time_seconds": time.perf_counter() - started,
        "stdout_tail": (stdout or "")[-4000:], "stderr_tail": (stderr or "")[-4000:],
    }


def parse_junit(path: Path) -> dict[str, str]:
    tree = ET.parse(path)
    outcomes: dict[str, str] = {}
    for case in tree.getroot().iter("testcase"):
        key = f"{case.get('classname', '')}::{case.get('name', '')}"
        tags = {child.tag for child in case}
        if "error" in tags:
            outcome = "error"
        elif "failure" in tags:
            outcome = "failed"
        elif "skipped" in tags:
            outcome = "skipped"
        else:
            outcome = "passed"
        rank = {"passed": 0, "skipped": 1, "failed": 2, "error": 3}
        if key not in outcomes or rank[outcome] > rank[outcomes[key]]:
            outcomes[key] = outcome
    return outcomes


def run_frozen_suite(workspace: Path, environment_python: Path, plan: dict[str, Any],
                     run_dir: Path, *, timeout: int = SUITE_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Execute the frozen suite in a compiled workspace and record per-test outcomes."""
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(environment_python.parent.parent)
    env["PATH"] = str(environment_python.parent) + os.pathsep + env.get("PATH", "")
    run_dir.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, Any] = {
        "schema_version": "orion.v2.pc-r6-suite-receipt.v1",
        "runner_family": plan["runner_family"], "test_files": plan["test_files"],
        "timeout_seconds": timeout,
    }
    if plan["runner_family"] == "pytest":
        xml = run_dir / "suite_junit.xml"
        if xml.exists():
            xml.unlink()
        command = [str(environment_python), "-m", "pytest", *plan["pytest_flags"],
                   "--junitxml", str(xml), *plan["test_files"]]
        result = _run_with_group_kill(command, cwd=workspace, env=env, timeout=timeout)
        receipt.update(result)
        if result["timed_out"]:
            receipt.update({"status": "SUITE_TIMEOUT", "tests": {}})
            return receipt
        if not xml.is_file():
            receipt.update({"status": "SUITE_NOT_COLLECTED", "tests": {},
                            "reason": "no junit report produced"})
            return receipt
        receipt["junit_sha256"] = sha256_file(xml)
        try:
            tests = parse_junit(xml)
        except ET.ParseError as exc:
            receipt.update({"status": "SUITE_NOT_COLLECTED", "tests": {},
                            "reason": f"junit parse error: {exc}"})
            return receipt
    else:
        runner_path = run_dir / "pc_r6_unittest_runner.py"
        runner_path.write_text(UNITTEST_JSON_RUNNER, encoding="utf-8")
        out = run_dir / "suite_unittest.json"
        if out.exists():
            out.unlink()
        command = [str(environment_python), str(runner_path), str(out), *plan["unittest_modules"]]
        result = _run_with_group_kill(command, cwd=workspace, env=env, timeout=timeout)
        receipt.update(result)
        if result["timed_out"]:
            receipt.update({"status": "SUITE_TIMEOUT", "tests": {}})
            return receipt
        if not out.is_file():
            receipt.update({"status": "SUITE_NOT_COLLECTED", "tests": {},
                            "reason": "unittest runner produced no report"})
            return receipt
        receipt["report_sha256"] = sha256_file(out)
        payload = json.loads(out.read_text(encoding="utf-8"))
        tests = {str(k): str(v) for k, v in payload.get("tests", {}).items()}
        receipt["tests_run"] = payload.get("tests_run")
    if not tests:
        receipt.update({"status": "SUITE_NOT_COLLECTED", "tests": {},
                        "reason": "zero test cases collected"})
        return receipt
    counts = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    for outcome in tests.values():
        counts[outcome] += 1
    receipt.update({"status": "COLLECTED", "tests": tests, "counts": counts,
                    "collected": len(tests)})
    return receipt


def derive_critical(baseline_tests: dict[str, str], patched_tests: dict[str, str]) -> dict[str, Any]:
    """Critical new failures = tests passing at baseline and not passing patched.

    Conservative reading (amendment A2): a baseline-passing test that is
    failed, errored, skipped or MISSING (not collected, e.g. import broken by the
    patch) in the patched run is a new failure.  Baseline-failing tests can never
    become new failures.
    """
    baseline_passing = sorted(k for k, v in baseline_tests.items() if v == "passed")
    breakdown = {"failed": 0, "error": 0, "skipped": 0, "missing": 0}
    new_failures: list[str] = []
    for key in baseline_passing:
        outcome = patched_tests.get(key)
        if outcome == "passed":
            continue
        breakdown["missing" if outcome is None else outcome] += 1
        new_failures.append(key)
    newly_passing = sorted(k for k, v in patched_tests.items()
                           if v == "passed" and baseline_tests.get(k) not in (None, "passed"))
    return {
        "critical_new_failure_count": len(new_failures),
        "critical_new_failure_breakdown": breakdown,
        "critical_new_failure_ids": new_failures[:200],
        "baseline_passing_count": len(baseline_passing),
        "patched_collected_count": len(patched_tests),
        "newly_passing_count": len(newly_passing),
        "newly_passing_ids": newly_passing[:50],
    }


# --------------------------------------------------------------------------- lane
class RuntimeProxy:
    """Pass-through to the frozen runtime; attaches the suite after the registered test."""

    def __init__(self, runtime, hook: Callable[[Path, Path], dict[str, Any]] | None):
        self._runtime = runtime
        self.compile_workspace = runtime.compile_workspace
        self._hook = hook
        self.last_suite: dict[str, Any] | None = None
        self.last_registered: dict[str, Any] | None = None

    def execute_test_binding(self, workspace, **kwargs):
        receipt = self._runtime.execute_test_binding(workspace, **kwargs)
        self.last_registered = receipt
        self.last_suite = None
        if self._hook is not None:
            try:
                self.last_suite = self._hook(Path(workspace), Path(kwargs["environment_python"]))
            except Exception as exc:  # the adapter closure must never see this
                self.last_suite = {"status": "SUITE_EVALUATOR_EXCEPTION",
                                   "reason": f"{type(exc).__name__}: {exc}", "tests": {}}
        return receipt

    def __getattr__(self, name):
        return getattr(self._runtime, name)


class Lane:
    """One frozen campaign bound to the verbatim adapter closure."""

    def __init__(self, cell: Cell, adapter_path: Path, manifest: Manifest, *, suite: bool):
        self.cell = cell
        self.manifest = manifest
        source = cell.root / "source"
        scripts = source / "scripts"
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        self.adapter_sha256 = manifest.record(adapter_path, "frozen_lane_adapter")
        adapter = load_module(f"pc_r6_frozen_adapter_{cell.name}", adapter_path)
        self.adapter = adapter
        self.evaluator = load_module(
            f"pc_r6_evaluator_{cell.name}",
            scripts / "evaluate_orion_real_problem_responses_v2.py")
        manifest.record(scripts / "evaluate_orion_real_problem_responses_v2.py",
                        f"{cell.name}/source/scripts/evaluate_orion_real_problem_responses_v2.py")
        manifest.record(scripts / "run_orion_real_problem_suite.py",
                        f"{cell.name}/source/scripts/run_orion_real_problem_suite.py")
        self.runtime = load_module(f"pc_r6_runtime_{cell.name}", scripts / "bugsinpy_project_runtime.py")
        manifest.record(scripts / "bugsinpy_project_runtime.py",
                        f"{cell.name}/source/scripts/bugsinpy_project_runtime.py")
        manifest.record(source / "research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json",
                        f"{cell.name}/source/research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json")
        manifest.record(cell.root / "SETUP_RECEIPT.json", f"{cell.name}/SETUP_RECEIPT.json")
        self.plan: dict[str, Any] | None = None
        self.run_dir: Path | None = None
        self.proxy = RuntimeProxy(self.runtime, self._hook if suite else None)
        self.evaluate = adapter.make_frozen_lane_evaluate_bugsinpy(
            self.evaluator.runner, self.proxy, cell.root, source)
        self.adapter_version = getattr(adapter, "LANE_ADAPTER_VERSION", None)

    def _hook(self, workspace: Path, environment_python: Path) -> dict[str, Any]:
        assert self.plan is not None and self.run_dir is not None
        return run_frozen_suite(workspace, environment_python, self.plan, self.run_dir)

    def task_plan(self, task_id: str) -> dict[str, Any]:
        workspace = self.cell.workspace(task_id)
        support = self.manifest.read_text(workspace / "bugsinpy_run_test.sh",
                                          f"{self.cell.name}/evaluator_private/{task_id}/bugsinpy_run_test.sh")
        info_path = workspace / "bugsinpy_bug.info"
        info = (self.manifest.read_text(info_path, f"{self.cell.name}/evaluator_private/{task_id}/bugsinpy_bug.info")
                if info_path.is_file() else None)
        return plan_suite(support, workspace, info)

    def run_one(self, *, rep: str | None, arm_id: str, task_id: str, response: dict[str, Any],
                workdir: Path) -> dict[str, Any]:
        task = self.cell.tasks[task_id]
        frozen = self.cell.frozen[rep] if rep is not None else {"tasks": [task]}
        self.plan = self.task_plan(task_id) if self.proxy._hook is not None else None
        self.run_dir = workdir / "runs" / arm_id / task_id
        workdir.mkdir(parents=True, exist_ok=True)
        self.proxy.last_suite = None
        self.proxy.last_registered = None
        if self.evaluator.response_is_uncheckable(response):
            record = self.evaluator.uncheckable_evaluation(task, response, arm_id)
            record["native_success"] = False
            record["pc_r6_uncheckable"] = True
        else:
            record = self.evaluate(frozen, workdir, task, response, arm_id,
                                   timeout_seconds=FROZEN_LANE_TIMEOUT_SECONDS)
        record["pc_r6"] = {
            "lane_version": LANE_VERSION, "cell": self.cell.name, "rep": rep,
            "arm_id": arm_id, "task_id": task_id, "project": task.get("project"),
            "frozen_lane_adapter_version": self.adapter_version,
            "frozen_lane_adapter_sha256": self.adapter_sha256,
            "suite_plan": self.plan, "suite": self.proxy.last_suite,
            "registered_failing_test_status": (
                self.proxy.last_registered.get("status") if self.proxy.last_registered else None),
        }
        return record


def merge_critical(record: dict[str, Any], baseline: dict[str, Any] | None) -> dict[str, Any]:
    """Derive the critical count for one patched record against the task baseline."""
    pc = record["pc_r6"]
    original = {key: record.get(key) for key in (
        "full_regression_suite_passed", "full_regression_suite_status", "critical_new_failure_count")}
    record["frozen_lane_original"] = original
    suite = pc.get("suite")
    reason = None
    derived: dict[str, Any] = {}
    if record.get("pc_r6_uncheckable") or str(record.get("status", "")).startswith("CANNOT_CHECK"):
        reason = NONE_REASONS["exception"] if "EVALUATOR_FAILURE" in str(record.get("status", "")) else NONE_REASONS["uncheckable"]
    elif record.get("checkout_returncode") not in (0,):
        reason = NONE_REASONS["checkout"]
    elif record.get("patch_apply_returncode") != 0:
        reason = NONE_REASONS["patch"]
    elif record.get("compile_status") != "PASS":
        reason = NONE_REASONS["compile"]
    elif baseline is None or baseline.get("status") != "BASELINE_OK":
        reason = NONE_REASONS["baseline"]
    elif suite is None or suite.get("status") == "SUITE_EVALUATOR_EXCEPTION":
        reason = NONE_REASONS["exception"]
    elif suite.get("status") == "SUITE_TIMEOUT":
        reason = NONE_REASONS["timeout"]
    elif suite.get("status") != "COLLECTED":
        reason = NONE_REASONS["uncollected"]
    else:
        derived = derive_critical(baseline["suite"]["tests"], suite["tests"])
    if reason:
        count = None
        status = reason
        passed = None
    else:
        count = derived["critical_new_failure_count"]
        status = "COUNTED"
        passed = bool(record.get("native_success")) and count == 0
    pc.update({
        "critical_new_failure_status": status,
        "critical_new_failure_count": count,
        "full_regression_suite_passed": passed,
        "baseline_ref": (baseline or {}).get("record_sha256"),
        **derived,
    })
    record["critical_new_failure_count"] = count
    record["full_regression_suite_passed"] = passed
    record["full_regression_suite_status"] = (
        "PC_R6_FULL_REGRESSION_SUITE_RUN" if status == "COUNTED" else f"CANNOT_CHECK_{status}")
    return record


def run_baseline(lane: Lane, task_id: str, workdir: Path) -> dict[str, Any]:
    response = {"status": "PC_R6_BASELINE_MARKER", "task_id": task_id, "arm_id": BASELINE_ARM_ID,
                "proposed_patch_or_artifact": {"type": "unified_diff", "content": BASELINE_MARKER_PATCH}}
    record = lane.run_one(rep=None, arm_id=BASELINE_ARM_ID, task_id=task_id,
                          response=response, workdir=workdir)
    suite = record["pc_r6"].get("suite") or {}
    if record.get("patch_apply_returncode") != 0:
        status = "BASELINE_MARKER_PATCH_FAILED"
    elif record.get("compile_status") != "PASS":
        status = "BASELINE_COMPILE_FAILED"
    elif suite.get("status") == "SUITE_TIMEOUT":
        status = "SUITE_TIMEOUT"
    elif suite.get("status") != "COLLECTED":
        status = "BASELINE_SUITE_NOT_COLLECTED"
    elif not any(outcome == "passed" for outcome in suite.get("tests", {}).values()):
        # a suite whose baseline passes nothing (e.g. one import-error pseudo
        # test) would make every patched count vacuously 0 -> unusable baseline
        status = "BASELINE_SUITE_NO_PASSING_TESTS"
    else:
        status = "BASELINE_OK"
    baseline = {
        "schema_version": "orion.v2.pc-r6-baseline.v1", "lane_version": LANE_VERSION,
        "cell": lane.cell.name, "task_id": task_id, "project": lane.cell.tasks[task_id].get("project"),
        "status": status, "baseline_marker_patch_sha256": sha256_text(BASELINE_MARKER_PATCH),
        "registered_failing_test_native_success_at_baseline": record.get("native_success"),
        "bug_reproduced_at_baseline": bool(
            record.get("compile_status") == "PASS" and record.get("native_success") is False),
        "suite": suite, "suite_plan": record["pc_r6"].get("suite_plan"),
        "closure_record": {k: record.get(k) for k in (
            "compile_status", "patch_apply_returncode", "test_returncode",
            "test_infrastructure_error", "workspace_head", "workspace_head_matches",
            "workspace_stale_build_artifacts_removed", "wall_time_seconds", "status", "reason")},
        "generated_utc": utc_now(),
    }
    baseline["record_sha256"] = sha256_text(json.dumps(baseline, sort_keys=True))
    return baseline


def registered_test_suite_outcomes(plan: dict[str, Any] | None, tests: dict[str, str]) -> dict[str, str | None]:
    """Outcome of each registered test id inside the suite run (informational)."""
    result: dict[str, str | None] = {}
    if not plan:
        return result
    for line in plan["registered_lines"]:
        tokens = shlex.split(line)
        targets = [t for t in tokens[1:] if not t.startswith("-") and t not in ("-m", "pytest", "unittest")]
        for target in targets:
            if plan["runner_family"] == "unittest":
                result[target] = tests.get(target)
                continue
            if "::" not in target:
                continue
            file_part, _, node = target.partition("::")
            stem = Path(file_part).with_suffix("").as_posix().replace("/", ".")
            name = node.split("::")[-1]
            matches = [k for k in tests if k.split("::")[0].startswith(stem) and k.split("::", 1)[1].split("[")[0] == name]
            result[target] = tests[matches[0]] if len(matches) == 1 else (
                "AMBIGUOUS" if matches else None)
    return result


def gold_not_applicable_reason(record: dict[str, Any], workspace: Path, manifest: Manifest,
                               label: str) -> str | None:
    """Amendment A13: the gold SOURCE patch (BugsInPy bug_patch.txt) omits test-side
    fixture files added by the fixed commit; when the registered failing test fails
    identically after gold with a FileNotFoundError naming a path that (a) is absent
    from the frozen workspace and (b) is added by the fixed commit, the control is not
    applicable to that task (a substrate property shared by every arm), not a lane
    defect.  Every condition is checked; anything else stays a real FAIL."""
    if record.get("patch_apply_returncode") != 0 or record.get("compile_status") != "PASS":
        return None
    if record.get("native_success") is not False:
        return None
    text = str(record.get("stdout_tail", "")) + "\n" + str(record.get("stderr_tail", ""))
    match = _MISSING_FILE_RE.search(text)
    if not match or "FileNotFoundError" not in text:
        return None
    missing = match.group(1)
    if (workspace / missing).exists():
        return None
    info_path = workspace / "bugsinpy_bug.info"
    if not info_path.is_file():
        return None
    fixed = None
    for line in manifest.read_text(info_path, f"{label}/bugsinpy_bug.info").splitlines():
        if line.startswith("fixed_commit_id="):
            fixed = line.split("=", 1)[1].strip().strip('"')
    if not fixed:
        return None
    shown = subprocess.run(["git", "show", "--name-only", "--format=", fixed], cwd=str(workspace),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if shown.returncode != 0 or missing not in shown.stdout.splitlines():
        return None
    return f"GOLD_NOT_APPLICABLE_MISSING_FIXTURE:{missing}"


# --------------------------------------------------------------------------- stages
def stage_manifest(args, cells: list[Cell], manifest: Manifest) -> int:
    e30 = next(cell for cell in cells if cell.name == "e30r11")
    for cell in cells:
        for rep in cell.reps:
            for arm in cell.arms:
                for task_id in cell.task_ids:
                    manifest.record(cell.response_path(rep, arm, task_id),
                                    f"{cell.name}/run/confirmatory-r{rep}/responses/{arm}/{task_id}.json")
                    eval_path = cell.evaluation_path(rep, arm, task_id)
                    if eval_path.is_file():
                        manifest.record(eval_path,
                                        f"{cell.name}/run/confirmatory-r{rep}/evaluations/{arm}/{task_id}.json")
        setup = manifest.read_json(cell.root / "SETUP_RECEIPT.json", f"{cell.name}/SETUP_RECEIPT.json")
        for project, binding in sorted(setup.get("prospective_bindings", {}).items()):
            manifest.record(Path(binding["path"]), f"{cell.name}/prospective_binding/{project}")
        cache_manifest = Path(setup["offline_cache"]["manifest"])
        manifest.record(cache_manifest, f"{cell.name}/offline_cache/manifest.json")
        manifest.record(cell.root / "source/research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json",
                        f"{cell.name}/source/research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json")
        for name in ("evaluate_orion_real_problem_responses_v2.py", "run_orion_real_problem_suite.py",
                     "bugsinpy_project_runtime.py"):
            manifest.record(cell.root / "source/scripts" / name, f"{cell.name}/source/scripts/{name}")
        for task_id in cell.task_ids:
            workspace = cell.workspace(task_id)
            for name in ("bugsinpy_run_test.sh", "bugsinpy_bug.info", "bugsinpy_requirements.txt",
                         "bugsinpy_setup.sh"):
                if (workspace / name).is_file():
                    manifest.record(workspace / name, f"{cell.name}/evaluator_private/{task_id}/{name}")
            identity = workspace_identity(workspace)
            manifest.entries[f"{cell.name}/evaluator_private/{task_id}/@HEAD"] = identity["head"]
            manifest.entries[f"{cell.name}/evaluator_private/{task_id}/@STATUS_PORCELAIN"] = identity["status_sha256"]
            for rel, digest in identity["deviating_files"].items():
                manifest.entries[f"{cell.name}/evaluator_private/{task_id}/{rel}"] = digest
    manifest.record(args.adapter, "frozen_lane_adapter")
    truth = args.truth_dir
    for rel in ("e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json",
                "e60-r1-component-ablation/component_effects.json",
                "e60-r1-component-ablation/supersede.sha256",
                "e60-r1-component-ablation/E60_R1_COMPONENT_ABLATION_ANALYSIS.json"):
        manifest.record(truth / rel, f"truth/{rel}")
    for task_id, gold in select_gr0b_tasks(e30, args):
        manifest.record(gold, f"gold/{task_id}/bug_patch.txt")
    digest = manifest.write(args.out / "PC_R6_INPUT_MANIFEST.sha256")
    campaign_id = f"campaign-pc-r6-fullreg-e30r11-e60-{args.date}-{digest[:8]}"
    payload = {
        "schema_version": "orion.v2.pc-r6-input-manifest.v1", "lane_version": LANE_VERSION,
        "design": DESIGN_ID, "generated_utc": utc_now(), "entry_count": len(manifest.entries),
        "manifest_sha256": digest, "manifest8": digest[:8], "campaign_id": campaign_id,
        "cells": {cell.name: {"root": str(cell.root), "arms": cell.arms, "reps": cell.reps,
                              "tasks": len(cell.task_ids), "expected_evaluations": cell.expected_evaluations()}
                  for cell in cells},
        "frozen_lane_adapter_sha256": manifest.entries["frozen_lane_adapter"],
    }
    write_json(args.out / "PC_R6_INPUT_MANIFEST.json", payload)
    print(json.dumps({"campaign_id": campaign_id, "entries": len(manifest.entries)}))
    return 0


def workspace_identity(workspace: Path) -> dict[str, Any]:
    def git(*argv: str) -> str:
        completed = subprocess.run(["git", *argv], cwd=str(workspace), stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, check=False)
        return completed.stdout
    head = git("rev-parse", "HEAD").strip()
    # deviations from HEAD that actually enter the lane: the adapter's copytree
    # ignores .orion-e30-env / .orion-e30-support / env / __pycache__ / *.pyc,
    # so those trees are excluded from the identity (and from the hashing cost)
    status = git("status", "--porcelain", "--untracked-files=all", "--",
                 ".", ":!.orion-e30-env", ":!.orion-e30-support", ":!env",
                 ":!.orion-e30-pip-tmp", ":(exclude,glob)**/__pycache__/**", ":(exclude,glob)**/*.pyc")
    deviating: dict[str, str] = {}
    for line in status.splitlines():
        if len(line) < 4:
            continue
        code, rel = line[:2], line[3:]
        if rel.startswith("\""):
            continue
        target = workspace / rel
        if "D" in code or not target.is_file() or target.is_symlink():
            continue
        deviating[rel] = sha256_file(target)
    return {"head": head, "status_sha256": sha256_text(status), "deviating_files": deviating}


def gr0b_candidates(e30: Cell, args) -> dict[str, list[tuple[str, Path]]]:
    """Per project (lexicographic), tasks in bug_id order whose gold patch file exists."""
    by_project: dict[str, list[dict[str, Any]]] = {}
    for task in e30.tasks.values():
        by_project.setdefault(str(task["project"]), []).append(task)
    candidates: dict[str, list[tuple[str, Path]]] = {}
    for project in sorted(by_project):
        for task in sorted(by_project[project], key=lambda item: int(item["bug_id"])):
            gold = Path(args.gold_patch_template.format(
                campaign=e30.root, task_id=task["task_id"], project=project, bug_id=task["bug_id"]))
            if gold.is_file():
                candidates.setdefault(project, []).append((task["task_id"], gold))
    return candidates


def select_gr0b_tasks(e30: Cell, args) -> list[tuple[str, Path]]:
    """First candidate of the first five projects (the frozen-input manifest set)."""
    candidates = gr0b_candidates(e30, args)
    return [tasks[0] for _project, tasks in list(candidates.items())[:GR0B_TASK_COUNT]]


def record_path(out: Path, kind: str, cell: str, rep: str | None, arm: str | None, task_id: str) -> Path:
    if rep is None:
        return out / kind / cell / "baseline" / f"{task_id}.json"
    return out / kind / cell / f"r{rep}" / arm / f"{task_id}.json"


def stage_execute(args, cells: list[Cell], manifest: Manifest, *, kind: str) -> int:
    """kind = 'records_gr0a' (registered test only) or 'records' (registered test + suite)."""
    indices = plan_indices(cells)
    if args.index is None or not (0 <= args.index < len(indices)):
        raise LaneError(f"--index must be in [0, {len(indices)})")
    cell_name, task_id = indices[args.index]
    cell = next(c for c in cells if c.name == cell_name)
    lane = Lane(cell, args.adapter, manifest, suite=(kind == "records"))
    workdir = args.out / "scratch" / kind / cell_name
    log = {"index": args.index, "cell": cell_name, "task_id": task_id, "kind": kind,
           "started_utc": utc_now(), "evaluations": []}
    baseline = None
    if kind == "records":
        base_path = record_path(args.out, kind, cell_name, None, None, task_id)
        if base_path.is_file():
            baseline = json.loads(base_path.read_text(encoding="utf-8"))
        if baseline is None or baseline.get("lane_version") != LANE_VERSION:
            baseline = run_baseline(lane, task_id, workdir / "baseline")
            write_json(base_path, baseline)
        log["baseline_status"] = baseline["status"]
    for rep in cell.reps:
        for arm in cell.arms:
            target = record_path(args.out, kind, cell_name, rep, arm, task_id)
            if target.is_file():
                try:
                    existing = json.loads(target.read_text(encoding="utf-8"))
                    if existing.get("pc_r6", {}).get("lane_version") == LANE_VERSION:
                        log["evaluations"].append({"rep": rep, "arm": arm, "skipped": "exists"})
                        continue
                except json.JSONDecodeError:
                    pass
            response = manifest.read_json(cell.response_path(rep, arm, task_id),
                                          f"{cell_name}/run/confirmatory-r{rep}/responses/{arm}/{task_id}.json")
            if kind == "records" and baseline is not None and baseline.get("status") != "BASELINE_OK":
                lane.proxy._hook = None  # suite pointless without a baseline; keep registered test
            record = lane.run_one(rep=rep, arm_id=arm, task_id=task_id, response=response,
                                  workdir=workdir / f"r{rep}")
            if kind == "records":
                merge_critical(record, baseline)
            write_json(target, record)
            log["evaluations"].append({
                "rep": rep, "arm": arm, "native_success": record.get("native_success"),
                "critical_new_failure_count": record.get("critical_new_failure_count"),
                "status": record.get("pc_r6", {}).get("critical_new_failure_status"),
                "wall_time_seconds": record.get("wall_time_seconds")})
    log["finished_utc"] = utc_now()
    write_json(args.out / "logs" / kind / f"{cell_name}-{task_id}.json", log)
    manifest.write(args.out / "manifests" / f"{kind}-{cell_name}-{task_id}.sha256")
    print(json.dumps({k: v for k, v in log.items() if k != "evaluations"}))
    return 0


# --------------------------------------------------------------------------- GR0(a)
def frozen_vector_e30(truth_dir: Path, manifest: Manifest) -> tuple[dict[tuple[str, str, str], bool], dict[str, Any]]:
    path = truth_dir / "e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json"
    rollup = manifest.read_json(path, "truth/e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json")
    vector: dict[tuple[str, str, str], bool] = {}
    for key, reps in rollup["paired_task_table"].items():
        arm, task_id = key.split("/", 1)
        for rep_key, item in reps.items():
            vector[(rep_key[1:], arm, task_id)] = bool(item["native_success"])
    anchors = {"file_sha256": manifest.entries["truth/e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json"],
               "internal_freeze_sha256": rollup.get("freeze_sha256"),
               "per_arm_totals": {arm: item["native_success"] for arm, item in rollup["per_arm_totals"].items()}}
    return vector, anchors


def frozen_vector_from_records(cell: Cell, manifest: Manifest) -> dict[tuple[str, str, str], bool | None]:
    vector: dict[tuple[str, str, str], bool | None] = {}
    for rep in cell.reps:
        for arm in cell.arms:
            for task_id in cell.task_ids:
                path = cell.evaluation_path(rep, arm, task_id)
                if not path.is_file():
                    vector[(rep, arm, task_id)] = None
                    continue
                record = manifest.read_json(path, f"{cell.name}/run/confirmatory-r{rep}/evaluations/{arm}/{task_id}.json")
                vector[(rep, arm, task_id)] = record.get("native_success")
    return vector


def majority(values: list[bool | None]) -> bool | None:
    threshold = len(values) / 2
    if sum(v is True for v in values) > threshold:
        return True
    if sum(v is False for v in values) > threshold:
        return False
    return None


def anchor_e60(cell: Cell, vector: dict[tuple[str, str, str], bool | None], truth_dir: Path,
               manifest: Manifest) -> dict[str, Any]:
    """Bind the E60 per-evaluation vector to the in-repo frozen aggregates."""
    result: dict[str, Any] = {"checks": []}
    # supersede.sha256 lists the sha256 of the SUPERSEDED (old) rep-3 artifacts, preserved
    # under repair/superseded-r3-falsifier/; the live record must differ from it and the
    # preserved copy must match it (E60 receipt section 2.5)
    supersede_path = truth_dir / "e60-r1-component-ablation/supersede.sha256"
    supersede = manifest.read_text(supersede_path, "truth/e60-r1-component-ablation/supersede.sha256")
    repair = cell.root / "repair" / "superseded-r3-falsifier"
    repair_ledgers = sorted(repair.glob("supersede-*.sha256"))
    result["checks"].append({
        "check": "supersede_ledger_preserved_in_campaign_repair_dir",
        "pass": any(sha256_file(p) == sha256_file(supersede_path) for p in repair_ledgers)})
    preserved = {sha256_file(p): str(p.relative_to(cell.root)) for p in repair.glob("evaluations/*/*.json")}
    for line in supersede.splitlines():
        digest, _, path = line.partition("  ")
        if "/evaluations/" not in path:
            continue
        digest = digest.strip()
        rel = path.split("/run/", 1)[1]
        local = cell.run / rel
        live_differs = local.is_file() and sha256_file(local) != digest
        result["checks"].append({"check": "supersede_sha256_superseded_record_preserved_and_live_differs",
                                 "path": rel, "preserved_copy": preserved.get(digest),
                                 "pass": bool(live_differs and digest in preserved)})
    analysis = manifest.read_json(truth_dir / "e60-r1-component-ablation/E60_R1_COMPONENT_ABLATION_ANALYSIS.json",
                                  "truth/e60-r1-component-ablation/E60_R1_COMPONENT_ABLATION_ANALYSIS.json")
    task_level: dict[str, dict[str, bool | None]] = {}
    for arm in cell.arms:
        task_level[arm] = {task_id: majority([vector.get((rep, arm, task_id)) for rep in cell.reps])
                           for task_id in cell.task_ids}
        expected = analysis["arm_summaries"][arm]["success_count"]
        observed = sum(v is True for v in task_level[arm].values())
        result["checks"].append({"check": "arm_summary_success_count", "arm": arm,
                                 "expected": expected, "observed": observed, "pass": expected == observed})
        for project, stratum in analysis["arm_summaries"][arm].get("project_strata", {}).items():
            observed_p = sum(v is True for task_id, v in task_level[arm].items()
                             if cell.tasks[task_id].get("project") == project)
            result["checks"].append({"check": "arm_summary_project_success_count", "arm": arm, "project": project,
                                     "expected": stratum["success_count"], "observed": observed_p,
                                     "pass": stratum["success_count"] == observed_p})
    effects = manifest.read_json(truth_dir / "e60-r1-component-ablation/component_effects.json",
                                 "truth/e60-r1-component-ablation/component_effects.json")
    for contrast, block in effects.items():
        left, right = block["left_arm"], block["right_arm"]
        table = {"both_true": 0, "left_only": 0, "right_only": 0, "both_false": 0}
        for task_id in cell.task_ids:
            a, b = task_level[left][task_id], task_level[right][task_id]
            if a is None or b is None:
                continue
            table["both_true" if a and b else "left_only" if a else "right_only" if b else "both_false"] += 1
        expected = block["success"]["paired_table"]
        result["checks"].append({"check": "component_effects_success_paired_table", "contrast": contrast,
                                 "expected": expected, "observed": table, "pass": expected == table})
    result["pass"] = all(item["pass"] for item in result["checks"])
    return result


def compare_vectors(frozen: dict[tuple[str, str, str], Any], observed: dict[tuple[str, str, str], Any]) -> dict[str, Any]:
    mismatches = []
    missing = []
    matched = 0
    for key in sorted(frozen):
        if key not in observed:
            missing.append(list(key))
        elif observed[key] is frozen[key] or observed[key] == frozen[key]:
            matched += 1
        else:
            mismatches.append({"key": list(key), "frozen": frozen[key], "observed": observed[key]})
    return {"expected": len(frozen), "matched": matched, "mismatched": len(mismatches),
            "missing": len(missing), "mismatch_list": mismatches[:100], "missing_list": missing[:100],
            "bit_exact": matched == len(frozen) and not mismatches and not missing}


def checker_negative_control(frozen: dict[tuple[str, str, str], Any]) -> dict[str, Any]:
    """The comparator must detect one deliberately corrupted entry and pass a self-compare."""
    if not frozen:
        return {"pass": False, "reason": "empty frozen vector"}
    self_compare = compare_vectors(frozen, dict(frozen))
    corrupted = dict(frozen)
    key = sorted(frozen)[0]
    corrupted[key] = not bool(frozen[key])
    flipped = compare_vectors(frozen, corrupted)
    dropped = dict(frozen)
    dropped.pop(key)
    missing = compare_vectors(frozen, dropped)
    ok = (self_compare["bit_exact"] and flipped["mismatched"] == 1 and not flipped["bit_exact"]
          and flipped["mismatch_list"][0]["key"] == list(key)
          and missing["missing"] == 1 and not missing["bit_exact"])
    return {"pass": ok, "self_compare_bit_exact": self_compare["bit_exact"],
            "flipped_key": list(key), "flipped_detected": flipped["mismatched"],
            "dropped_detected": missing["missing"]}


def stage_gr0a_collect(args, cells: list[Cell], manifest: Manifest) -> int:
    receipt: dict[str, Any] = {
        "schema_version": "orion.v2.pc-r6-gr0a-receipt.v1", "lane_version": LANE_VERSION,
        "design": DESIGN_ID, "gate": "GR0(a) LANE_VALID: registered-failing-test vector bit-exact",
        "generated_utc": utc_now(), "cells": {}, "checker_validation": {},
    }
    overall = True
    for cell in cells:
        if cell.name == "e30r11":
            frozen, anchors = frozen_vector_e30(args.truth_dir, manifest)
            campaign_records = frozen_vector_from_records(cell, manifest)
            cross = compare_vectors(frozen, campaign_records)
            anchors["campaign_evaluation_records_cross_check"] = {k: v for k, v in cross.items()
                                                                  if k not in ("mismatch_list", "missing_list")}
            anchors["pass"] = cross["bit_exact"]
        else:
            frozen = frozen_vector_from_records(cell, manifest)
            anchors = anchor_e60(cell, frozen, args.truth_dir, manifest) if not args.skip_e60_anchor else {"pass": True, "skipped": True}
        control = checker_negative_control(frozen)
        receipt["checker_validation"][cell.name] = control
        observed: dict[tuple[str, str, str], Any] = {}
        for rep in cell.reps:
            for arm in cell.arms:
                for task_id in cell.task_ids:
                    path = record_path(args.out, "records_gr0a", cell.name, rep, arm, task_id)
                    if path.is_file():
                        record = manifest.read_json(path, f"records_gr0a/{cell.name}/r{rep}/{arm}/{task_id}.json")
                        observed[(rep, arm, task_id)] = record.get("native_success")
        if len(frozen) != cell.spec["evaluations"] and not args.allow_partial_cells:
            raise LaneError(f"{cell.name}: frozen vector has {len(frozen)} entries, expected {cell.spec['evaluations']}")
        comparison = compare_vectors(frozen, observed)
        cell_pass = bool(control["pass"] and anchors.get("pass") and comparison["bit_exact"])
        overall = overall and cell_pass
        receipt["cells"][cell.name] = {
            "truth": cell.spec["truth"], "anchors": anchors, "comparison": comparison, "pass": cell_pass,
            "reproduction": f"{comparison['matched']}/{comparison['expected']}",
        }
    receipt["status"] = "PASS" if overall else "FAIL"
    write_json(args.out / "PC_R6_GR0A_RECEIPT.json", receipt)
    print(json.dumps({"gr0a": receipt["status"],
                      **{name: item["reproduction"] for name, item in receipt["cells"].items()},
                      "checker_validation": {k: v["pass"] for k, v in receipt["checker_validation"].items()}}))
    return 0 if overall else 1


# --------------------------------------------------------------------------- GR0(b)
def stage_gr0b(args, cells: list[Cell], manifest: Manifest) -> int:
    e30 = next(cell for cell in cells if cell.name == "e30r11")
    lane = Lane(e30, args.adapter, manifest, suite=True)
    if len(gr0b_candidates(e30, args)) < GR0B_TASK_COUNT and not args.allow_partial_cells:
        raise LaneError("gr0b needs gold patches for at least five projects")
    workdir = args.out / "scratch" / "records_gr0b"
    results: list[dict[str, Any]] = []
    not_applicable: list[dict[str, Any]] = []
    overall = True
    candidates = gr0b_candidates(e30, args)
    projects_controlled = 0
    for project, tasks in candidates.items():
        if projects_controlled >= GR0B_TASK_COUNT:
            break
        for task_id, gold_path in tasks:
            base_path = record_path(args.out, "records_gr0b", "e30r11", None, None, task_id)
            if base_path.is_file() and json.loads(base_path.read_text(encoding="utf-8")).get("lane_version") == LANE_VERSION:
                baseline = json.loads(base_path.read_text(encoding="utf-8"))
            else:
                baseline = run_baseline(lane, task_id, workdir / "baseline")
                write_json(base_path, baseline)
            gold = manifest.read_text(gold_path, f"gold/{task_id}/bug_patch.txt")
            response = {"status": "PC_R6_GOLD_PATCH_CONTROL", "task_id": task_id, "arm_id": GR0B_ARM_ID,
                        "proposed_patch_or_artifact": {"type": "unified_diff", "content": gold}}
            record = lane.run_one(rep=None, arm_id=GR0B_ARM_ID, task_id=task_id, response=response,
                                  workdir=workdir / "gold")
            record["gold_or_fixed_solution_accessed"] = True
            record["gold_patch_sha256"] = manifest.entries[f"gold/{task_id}/bug_patch.txt"]
            merge_critical(record, baseline)
            plan = record["pc_r6"].get("suite_plan")
            in_suite = {
                "baseline": registered_test_suite_outcomes(plan, (baseline.get("suite") or {}).get("tests", {})),
                "gold": registered_test_suite_outcomes(plan, (record["pc_r6"].get("suite") or {}).get("tests", {})),
            }
            record["pc_r6"]["registered_test_in_suite"] = in_suite
            not_applicable_reason = gold_not_applicable_reason(
                record, e30.workspace(task_id), manifest, f"e30r11/evaluator_private/{task_id}")
            record["pc_r6"]["gold_control_status"] = not_applicable_reason or "APPLICABLE"
            write_json(args.out / "records_gr0b" / "e30r11" / "gold" / f"{task_id}.json", record)
            item = {
                "task_id": task_id, "project": project,
                "baseline_status": baseline["status"],
                "bug_reproduced_at_baseline": baseline["bug_reproduced_at_baseline"],
                "gold_patch_apply_returncode": record.get("patch_apply_returncode"),
                "gold_compile_status": record.get("compile_status"),
                "gold_native_success": record.get("native_success"),
                "critical_new_failure_count": record.get("critical_new_failure_count"),
                "critical_new_failure_status": record["pc_r6"].get("critical_new_failure_status"),
                "baseline_passing_count": record["pc_r6"].get("baseline_passing_count"),
                "newly_passing_count": record["pc_r6"].get("newly_passing_count"),
                "registered_test_in_suite": in_suite,
                "suite_registered_test_divergence": bool(
                    record.get("native_success") is True
                    and in_suite["gold"] and all(v != "passed" for v in in_suite["gold"].values())),
                "suite_runner_family": (plan or {}).get("runner_family"),
            }
            if not_applicable_reason:
                item.update({"gold_control_status": not_applicable_reason, "pass": None})
                not_applicable.append(item)
                print(json.dumps(item))
                continue
            item["gold_control_status"] = "APPLICABLE"
            item["pass"] = bool(
                baseline["status"] == "BASELINE_OK"
                and baseline["bug_reproduced_at_baseline"]
                and record.get("native_success") is True
                and record.get("critical_new_failure_count") == 0
                # lane-validity precondition (amendment A6, relaxed by A14): the baseline
                # suite must contain passing tests; the registered test's own outcome
                # inside the suite run is recorded, not gated (order-dependent modules)
                and (record["pc_r6"].get("baseline_passing_count") or 0) >= 1)
            overall = overall and item["pass"]
            results.append(item)
            projects_controlled += 1
            print(json.dumps(item))
            break
    if projects_controlled < GR0B_TASK_COUNT and not args.allow_partial_cells:
        overall = False
    receipt = {
        "schema_version": "orion.v2.pc-r6-gr0b-receipt.v1", "lane_version": LANE_VERSION, "design": DESIGN_ID,
        "gate": "GR0(b) LANE_VALID: gold patch flips registered failing test AND critical_new_failure_count == 0",
        "selection_rule": GR0B_SELECTION_RULE, "generated_utc": utc_now(), "tasks": results,
        "not_applicable": not_applicable, "projects_controlled": projects_controlled,
        "status": "PASS" if overall and results else "FAIL",
    }
    write_json(args.out / "PC_R6_GR0B_RECEIPT.json", receipt)
    manifest.write(args.out / "manifests" / "records_gr0b.sha256")
    print(json.dumps({"gr0b": receipt["status"], "tasks": len(results)}))
    return 0 if receipt["status"] == "PASS" else 1


def stage_gr0_combine(args) -> int:
    parts = {}
    for name in ("PC_R6_GR0A_RECEIPT.json", "PC_R6_GR0B_RECEIPT.json"):
        path = args.out / name
        if not path.is_file():
            raise LaneError(f"missing {name}")
        parts[name] = {"sha256": sha256_file(path),
                       "status": json.loads(path.read_text(encoding="utf-8")).get("status")}
    status = "PASS" if all(item["status"] == "PASS" for item in parts.values()) else "FAIL"
    receipt = {"schema_version": "orion.v2.pc-r6-gr0-receipt.v1", "lane_version": LANE_VERSION,
               "design": DESIGN_ID, "gate": "GR0 LANE_VALID (hard)", "components": parts,
               "gr0_status": status, "generated_utc": utc_now()}
    write_json(args.out / "PC_R6_GR0_RECEIPT.json", receipt)
    print(json.dumps({"gr0": status}))
    return 0 if status == "PASS" else 1


# --------------------------------------------------------------------------- rollup
def stage_rollup(args, cells: list[Cell], manifest: Manifest) -> int:
    rollup: dict[str, Any] = {
        "schema_version": "orion.v2.pc-r6-fullreg-raw-rollup.v1", "lane_version": LANE_VERSION,
        "design": DESIGN_ID, "generated_utc": utc_now(), "suite_timeout_seconds": SUITE_TIMEOUT_SECONDS,
        "cells": {},
    }
    complete = True
    for cell in cells:
        baselines: dict[str, Any] = {}
        for task_id in cell.task_ids:
            path = record_path(args.out, "records", cell.name, None, None, task_id)
            if path.is_file():
                item = manifest.read_json(path, f"records/{cell.name}/baseline/{task_id}.json")
                baselines[task_id] = {
                    "status": item["status"], "project": item.get("project"),
                    "bug_reproduced_at_baseline": item.get("bug_reproduced_at_baseline"),
                    "runner_family": (item.get("suite_plan") or {}).get("runner_family"),
                    "collected": (item.get("suite") or {}).get("collected"),
                    "counts": (item.get("suite") or {}).get("counts"),
                    "suite_wall_time_seconds": (item.get("suite") or {}).get("wall_time_seconds"),
                    "record_sha256": item.get("record_sha256"),
                }
            else:
                baselines[task_id] = {"status": "MISSING"}
                complete = False
        evaluations: dict[str, dict[str, dict[str, Any]]] = {}
        arm_totals: dict[str, dict[str, Any]] = {}
        for arm in cell.arms:
            totals = {"evaluations": 0, "missing": 0, "native_success": 0, "patch_applied": 0,
                      "compiled": 0, "counted": 0, "critical_new_failure_any": 0,
                      "none_reasons": {}, "suite_timeouts": 0}
            for rep in cell.reps:
                for task_id in cell.task_ids:
                    path = record_path(args.out, "records", cell.name, rep, arm, task_id)
                    key = f"{arm}/{task_id}"
                    if not path.is_file():
                        evaluations.setdefault(key, {})[f"r{rep}"] = {"status": "MISSING"}
                        totals["missing"] += 1
                        complete = False
                        continue
                    record = manifest.read_json(path, f"records/{cell.name}/r{rep}/{arm}/{task_id}.json")
                    pc = record.get("pc_r6", {})
                    entry = {
                        "native_success": record.get("native_success"),
                        "critical_new_failure_count": record.get("critical_new_failure_count"),
                        "critical_new_failure_status": pc.get("critical_new_failure_status"),
                        "critical_new_failure_breakdown": pc.get("critical_new_failure_breakdown"),
                        "full_regression_suite_passed": record.get("full_regression_suite_passed"),
                        "patch_apply_returncode": record.get("patch_apply_returncode"),
                        "compile_status": record.get("compile_status"),
                        "suite_status": (pc.get("suite") or {}).get("status"),
                        "agent_status": record.get("agent_status"), "status": record.get("status"),
                        "project": pc.get("project"),
                        "wall_time_seconds": record.get("wall_time_seconds"),
                    }
                    evaluations.setdefault(key, {})[f"r{rep}"] = entry
                    totals["evaluations"] += 1
                    totals["native_success"] += entry["native_success"] is True
                    totals["patch_applied"] += entry["patch_apply_returncode"] == 0
                    totals["compiled"] += entry["compile_status"] == "PASS"
                    if entry["critical_new_failure_count"] is None:
                        reason = entry["critical_new_failure_status"] or "NONE_UNKNOWN"
                        totals["none_reasons"][reason] = totals["none_reasons"].get(reason, 0) + 1
                        totals["suite_timeouts"] += reason == NONE_REASONS["timeout"]
                    else:
                        totals["counted"] += 1
                        totals["critical_new_failure_any"] += entry["critical_new_failure_count"] > 0
            expected = len(cell.reps) * len(cell.task_ids)
            totals["expected"] = expected
            totals["patch_apply_failure_rate"] = (
                (totals["evaluations"] - totals["patch_applied"]) / totals["evaluations"] if totals["evaluations"] else None)
            totals["compile_failure_rate"] = (
                (totals["patch_applied"] - totals["compiled"]) / totals["patch_applied"] if totals["patch_applied"] else None)
            totals["checkable_rate"] = totals["counted"] / totals["evaluations"] if totals["evaluations"] else None
            arm_totals[arm] = totals
        rollup["cells"][cell.name] = {
            "campaign": cell.root.name, "arms": cell.arms, "reps": cell.reps, "task_ids": cell.task_ids,
            "task_projects": {task_id: cell.tasks[task_id].get("project") for task_id in cell.task_ids},
            "baselines": baselines, "evaluations": evaluations, "arm_totals": arm_totals,
        }
    rollup["complete"] = complete
    write_json(args.out / "PC_R6_FULLREG_RAW_ROLLUP_V1.json", rollup)
    # union of every per-stage read manifest + this stage
    union = Manifest()
    for path in sorted((args.out / "manifests").glob("*.sha256")):
        for line in path.read_text(encoding="utf-8").splitlines():
            digest, _, label = line.partition("  ")
            if label:
                union.entries[label] = digest
    union.entries.update(manifest.entries)
    read_digest = union.write(args.out / "PC_R6_READ_MANIFEST.sha256")
    rollup["read_manifest_sha256"] = read_digest
    write_json(args.out / "PC_R6_FULLREG_RAW_ROLLUP_V1.json", rollup)
    print(json.dumps({"complete": complete, "cells": {name: {arm: t["counted"] for arm, t in c["arm_totals"].items()}
                                                       for name, c in rollup["cells"].items()}}))
    return 0 if complete else 1


# --------------------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stage", required=True,
                        choices=["manifest", "gr0a", "gr0b", "gr0", "suite", "rollup", "list-indices"])
    parser.add_argument("--e30-campaign", type=Path)
    parser.add_argument("--e60-campaign", type=Path)
    parser.add_argument("--cells", default="e30r11,e60")
    parser.add_argument("--adapter", type=Path, help="frozen-lane adapter path (default: <e30>/run/e30_r11_arm_eval_frozen_lane.py)")
    parser.add_argument("--out", type=Path, required=True, help="PC-R6 campaign directory (all writes land here)")
    parser.add_argument("--truth-dir", type=Path, help="research/experiments/results/issue45 (in-repo truth anchors)")
    parser.add_argument("--gold-patch-template", default=GOLD_PATCH_TEMPLATE)
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y%m%d"))
    parser.add_argument("--index", type=int)
    parser.add_argument("--execute", action="store_true", help="gr0a: execute one index instead of collecting")
    parser.add_argument("--allow-partial-cells", action="store_true", help="tests only: relax arm/rep/campaign-name checks")
    parser.add_argument("--skip-e60-anchor", action="store_true", help="tests only: skip in-repo E60 anchor binding")
    parser.add_argument("--expect-adapter-sha256", default=FROZEN_ADAPTER_SHA256)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.out = args.out.resolve()
    manifest = Manifest()
    cell_names = [name for name in CELL_ORDER if name in {c.strip() for c in args.cells.split(",")}]
    roots = {"e30r11": args.e30_campaign, "e60": args.e60_campaign}
    try:
        if args.stage == "gr0":
            return stage_gr0_combine(args)
        cells = []
        for name in cell_names:
            if roots[name] is None:
                raise LaneError(f"--{'e30' if name == 'e30r11' else 'e60'}-campaign required for cell {name}")
            cells.append(Cell(name, roots[name], manifest, allow_partial=args.allow_partial_cells))
        if args.adapter is None:
            if args.e30_campaign is None:
                raise LaneError("--adapter or --e30-campaign required")
            args.adapter = args.e30_campaign / "run" / "e30_r11_arm_eval_frozen_lane.py"
        args.adapter = args.adapter.resolve()
        if args.expect_adapter_sha256 and sha256_file(args.adapter) != args.expect_adapter_sha256:
            raise LaneError(f"adapter sha256 mismatch at {args.adapter}; expected {args.expect_adapter_sha256}")
        if args.stage == "list-indices":
            for index, (cell, task_id) in enumerate(plan_indices(cells)):
                print(f"{index}\t{cell}\t{task_id}")
            return 0
        if args.stage == "manifest" or (args.stage == "gr0a" and not args.execute):
            if args.truth_dir is None:
                raise LaneError("--truth-dir required")
            args.truth_dir = args.truth_dir.resolve()
        if args.stage == "manifest":
            return stage_manifest(args, cells, manifest)
        if args.stage == "gr0a":
            if args.execute:
                return stage_execute(args, cells, manifest, kind="records_gr0a")
            return stage_gr0a_collect(args, cells, manifest)
        if args.stage == "gr0b":
            return stage_gr0b(args, cells, manifest)
        if args.stage == "suite":
            return stage_execute(args, cells, manifest, kind="records")
        if args.stage == "rollup":
            return stage_rollup(args, cells, manifest)
    except LaneError as exc:
        print(f"LANE_ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
