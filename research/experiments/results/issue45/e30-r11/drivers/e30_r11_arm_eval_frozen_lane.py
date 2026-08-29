#!/usr/bin/env python3
"""Frozen-lane arm evaluation adapter for E30 R11.

Infrastructure defect this adapter records and works around (2026-08-29):
the stock `evaluate_orion_real_problem_responses_v2.py` delegates to
`run_orion_real_problem_suite._evaluate_bugsinpy`, which provisions its own
workspace via stock `bugsinpy-checkout`/`bugsinpy-compile` and stock
`bugsinpy_run_test.sh`. On this campaign that lane cannot reproduce the frozen
baseline environment (evidence: run/confirmatory-r1/evaluations/F2_ORION_METABOLIC_FULL/
bugsinpy-ansible-2.json written 2026-08-29T02:35Z -- test_returncode 4,
ModuleNotFoundError under Python 3.11.5 -- while the same task's frozen lane
baseline receipt is PASS_VALID_BUG_REPRODUCED under Python 3.6.9 with the
registered compatibility interventions).

This adapter keeps EVERY stock decision surface unchanged:
  * response selection, uncheckable precheck, CANNOT_CHECK mapping, atomic
    writes  -> reused verbatim from evaluate_orion_real_problem_responses_v2
  * patch extraction (`_extract_patch`)            -> reused verbatim
  * pass predicate (rc==0 AND no infrastructure-error markers) -> replicated
    verbatim from `_bugsinpy_test_infrastructure_error`
  * record schema `orion.v2.task-evaluation.v1`    -> identical keys
Only the workspace provisioning lane changes: instead of a fresh stock
checkout, each evaluation copies the campaign's baseline-verified frozen
`evaluator_private/<task_id>` workspace, applies the arm patch to the project
directory (same `git apply --whitespace=nowarn -` invocation and cwd as
stock), recompiles with the campaign's frozen
`bugsinpy_project_runtime.compile_workspace` (exact-runtimes python, offline
cache, prospective bindings, registry interventions) and runs the registered
failing-test binding via `execute_test_binding` -- the same two functions the
frozen baseline driver `e30_baseline_driver_r11.py` used. Isolated lane
environment (HOME/TMPDIR/XDG_CACHE_HOME/PIP_CACHE_DIR/PIP_CONFIG_FILE/
GIT_CONFIG_GLOBAL) mirrors the baseline driver per
E30_R11_INFRASTRUCTURE_PREREGISTRATION lane_environment_policy.

No frozen endpoint is modified: requests, frozen_tasks.json, response
artifacts, predicates and output schema are untouched; the adapter adds
provenance fields only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

LANE_ADAPTER_VERSION = "orion.v2.e30-r11-frozen-lane-arm-eval-adapter.v3"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _capture(command: list[str], *, cwd: Path, env: dict[str, str], timeout: int) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command, cwd=str(cwd), env=env, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        return {
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        def _tail(value: Any) -> str:
            if isinstance(value, bytes):
                return value.decode("utf-8", "replace")[-4000:]
            return str(value or "")[-4000:]
        return {
            "returncode": None,
            "stdout_tail": _tail(exc.stdout),
            "stderr_tail": _tail(exc.stderr),
            "timed_out": True,
        }


def make_frozen_lane_evaluate_bugsinpy(runner, runtime, campaign: Path, source: Path):
    setup_receipt = json.loads((campaign / "SETUP_RECEIPT.json").read_text(encoding="utf-8"))
    registry_path = source / "research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json"
    offline_cache = Path(setup_receipt["offline_cache"]["directory"])
    offline_manifest = Path(setup_receipt["offline_cache"]["manifest"])

    def _evaluate_bugsinpy(frozen, workdir, task, response, arm_id, *, timeout_seconds):
        started = time.perf_counter()
        task_id = task["task_id"]
        project = str(task["project"])
        patch = runner._extract_patch(response)
        record: dict[str, Any] = {
            "schema_version": "orion.v2.task-evaluation.v1",
            "task_id": task_id,
            "arm_id": arm_id,
            "benchmark_id": "bugsinpy",
            "agent_status": response.get("status"),
            "evaluation_lane": LANE_ADAPTER_VERSION,
        }
        run_dir = workdir / "runs" / arm_id / task_id
        workspace = run_dir / "workspace"
        try:
            if run_dir.exists():
                shutil.rmtree(run_dir)
            run_dir.mkdir(parents=True, exist_ok=True)

            # ---- isolated lane environment (baseline driver policy) ----
            lane = run_dir / "lane"
            home, temporary, xdg_cache, pip_cache = (
                lane / "home", lane / "tmp", lane / "xdg-cache", lane / "pip-cache")
            for directory in (home, temporary, xdg_cache, pip_cache):
                directory.mkdir(parents=True, exist_ok=True)
            mirror_record = next(
                item for item in setup_receipt["mirrors"] if item["project"] == project)
            gitconfig = lane / "gitconfig"
            mirror_uri = Path(mirror_record["mirror"]).resolve().as_uri()
            gitconfig.write_text(
                f'[url "{mirror_uri}"]\n'
                f'\tinsteadOf = {mirror_record["url"]}\n'
                f'\tinsteadOf = {mirror_record["url"]}.git\n',
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update({
                "HOME": str(home), "TMPDIR": str(temporary),
                "XDG_CACHE_HOME": str(xdg_cache), "PIP_CACHE_DIR": str(pip_cache),
                "PIP_CONFIG_FILE": os.devnull,
                "GIT_CONFIG_GLOBAL": str(gitconfig), "GIT_TERMINAL_PROMPT": "0",
            })
            # keep foreign site-packages (cluster Python 3.11 bundle) and any
            # inherited PYTHONHOME out of the frozen exact-runtime interpreter;
            # removed (not blanked -- a blank PYTHONHOME breaks Py_Initialize)
            for foreign in ("PYTHONPATH", "PYTHONHOME"):
                environment.pop(foreign, None)
                os.environ.pop(foreign, None)
            record["isolated_environment"] = {
                **{key: environment[key] for key in
                   ("HOME", "TMPDIR", "XDG_CACHE_HOME", "PIP_CACHE_DIR",
                    "PIP_CONFIG_FILE", "GIT_CONFIG_GLOBAL")},
                "PYTHONPATH": "removed",
                "PYTHONHOME": "removed",
            }
            os.environ.update(environment)

            # ---- frozen workspace copy (baseline-verified checkout) ----
            private_source = campaign / "evaluator_private" / task_id
            shutil.copytree(
                private_source, workspace,
                # stale bytecode caches carry the ORIGINAL absolute source
                # paths and would shadow freshly-collected test modules
                ignore=shutil.ignore_patterns(
                    ".orion-e30-env", ".orion-e30-support", "env",
                    "__pycache__", "*.pyc"),
                # preserve symlinks AS symlinks: the frozen workspaces contain
                # tracked-but-broken symlinks (e.g. black docs/*.md ->
                # _build/generated/*); copytree's default follow mode raises
                # FileNotFoundError on them
                symlinks=True,
            )
            # restore the tree to the post-checkout state the frozen baseline
            # compiled FROM: the baseline run left in-repo build products
            # behind in evaluator_private, and `python -m pip` resolves the
            # CWD as a site directory -- a stale egg-info there shadows the
            # env's pinned install and breaks dependency verification
            # (observed: bugsinpy-tqdm-1, pip show tqdm -> 4.41.1 with
            # Location=<workspace> instead of the pinned 4.44.1 in the env).
            # Removed = exactly the repo-IGNORED paths (build products by the
            # repo's own .gitignore definition: build/, dist/, *.egg-info/,
            # __pycache__/, generated .c/.so, .pytest_cache, ...) plus a
            # suffix sweep for egg-info objects and compiled artifacts that
            # individual repos forgot to ignore (e.g. ansible-5 untracked
            # lib/ansible_base.egg-info/).  PRESERVED = tracked files with
            # their frozen modifications (the registered failing-test edits,
            # e.g. tqdm tests_contrib.py), the bugsinpy framework files
            # (bugsinpy_requirements.txt / bugsinpy_run_test.sh / setup / info)
            # and untracked new test files (registered failing tests added as
            # new .py files) -- all of these were present at baseline compile
            # start and are required (MISSING_RUNTIME_FILES otherwise).
            removed_stale: list[str] = []
            ignored_list = _capture(
                ["git", "ls-files", "-o", "-i", "--exclude-standard",
                 "--directory"],
                cwd=workspace, env=environment, timeout=600)
            for relative in ignored_list["stdout_tail"].splitlines():
                relative = relative.strip()
                if not relative:
                    continue
                target = workspace / relative
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target, ignore_errors=True)
                elif target.exists() or target.is_symlink():
                    target.unlink()
                else:
                    continue
                removed_stale.append(relative)
            for target in workspace.rglob("*"):
                if ".git" in target.parts:
                    continue
                name = target.name
                if target.is_dir() and not target.is_symlink() and name.endswith(
                        (".egg-info", ".egg-link")):
                    shutil.rmtree(target, ignore_errors=True)
                    removed_stale.append(
                        str(target.relative_to(workspace)))
                elif (target.is_file() or target.is_symlink()) and name.endswith(
                        (".pyc", ".pyo", ".so", ".o", ".egg")):
                    target.unlink()
                    removed_stale.append(
                        str(target.relative_to(workspace)))
            record["workspace_stale_build_artifacts_removed"] = len(removed_stale)
            record["workspace_stale_build_artifacts_sample"] = removed_stale[:40]
            status_probe = _capture(["git", "status", "--porcelain"],
                                    cwd=workspace, env=environment, timeout=300)
            record["workspace_dirty_after_restore"] = (
                status_probe["stdout_tail"].strip()[:2000] or None)
            head = _capture(["git", "rev-parse", "HEAD"], cwd=workspace,
                            env=environment, timeout=120)
            workspace_head = head["stdout_tail"].strip()
            expected_head = str(task.get("expected_buggy_commit", ""))
            head_matches = bool(
                head["returncode"] == 0 and len(workspace_head) == 40
                and 7 <= len(expected_head) <= 40
                and workspace_head.startswith(expected_head))
            record["workspace_source"] = (
                "campaign evaluator_private frozen checkout "
                "(baseline PASS_VALID_BUG_REPRODUCED)")
            record["workspace_head"] = workspace_head
            record["expected_workspace_head"] = expected_head
            record["workspace_head_matches"] = head_matches
            checkout_ok = head["returncode"] == 0 and head_matches
            record["checkout_returncode"] = 0 if checkout_ok else 1

            # ---- patch application (stock `git apply` invocation; frozen-lane
            # workspaces carry the project repo at the workspace ROOT, matching
            # the solver workspace layout the patch paths are relative to) ----
            project_workspace = workspace
            patch_result = None
            if checkout_ok and patch:
                try:
                    completed = subprocess.run(
                        ["git", "apply", "--whitespace=nowarn", "-"],
                        cwd=str(project_workspace), env=environment,
                        input=patch, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                    )
                    patch_result = {
                        "returncode": completed.returncode,
                        "stderr_tail": completed.stderr[-4000:],
                    }
                except subprocess.TimeoutExpired:
                    patch_result = {"returncode": None, "stderr_tail": "timeout"}
            record["patch_present"] = patch is not None
            record["patch_apply_returncode"] = (
                patch_result["returncode"] if patch_result else None)
            record["patch_size_bytes"] = len(patch.encode("utf-8")) if patch else 0

            # ---- frozen compile + registered failing test ----
            compile_receipt = None
            test_receipt = None
            if checkout_ok and patch_result and patch_result["returncode"] == 0:
                prospective = setup_receipt["prospective_bindings"][project]
                project_python = Path(
                    setup_receipt["project_pythons"][str(task["python_version"])])
                compile_receipt = runtime.compile_workspace(
                    workspace, project=project, project_python=project_python,
                    compiler_compat_cflags=str(prospective.get("compiler_compat_cflags", "")),
                    offline_cache=offline_cache,
                    offline_cache_manifest=offline_manifest,
                    prospective_binding_path=Path(prospective["path"]),
                    registry_path=registry_path,
                    receipt_path=run_dir / "compile_receipt.json",
                    timeout_seconds=timeout_seconds,
                )
                record["compile_status"] = compile_receipt.get("status")
                record["compile_returncode"] = (
                    0 if compile_receipt.get("status") == "PASS" else 1)
                if compile_receipt.get("status") == "PASS":
                    prospective_binding = json.loads(
                        Path(prospective["path"]).read_text(encoding="utf-8"))
                    test_prereqs = prospective_binding.get(
                        "legacy_build", {}).get("test_prerequisites", [])
                    test_receipt = runtime.execute_test_binding(
                        workspace, project=project,
                        environment_python=Path(compile_receipt["environment_python"]),
                        stage="registered_failing_test",
                        registry_path=registry_path,
                        offline_cache=offline_cache,
                        test_prerequisites=test_prereqs,
                        timeout_seconds=timeout_seconds,
                    )
                    (run_dir / "test_receipt.json").write_text(
                        json.dumps(test_receipt, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
                    record["test_binding_status"] = test_receipt.get("status")
            elif checkout_ok:
                record["compile_returncode"] = None

            # ---- stock predicate, verbatim ----
            test_returncode = test_receipt.get("returncode") if test_receipt else None
            if test_receipt:
                combined = (
                    str(test_receipt.get("stdout_tail", "")) + "\n"
                    + str(test_receipt.get("stderr_tail", ""))).casefold()
                infrastructure_error = bool(
                    test_returncode in {4, 5}
                    or any(marker in combined for marker in (
                        "modulenotfounderror", "importerror while loading conftest",
                        "unable to import required dependencies", "command not found",
                        "no module named", "could not find a version that satisfies",
                        "error: file not found:", "no tests ran", "collected 0 items",
                    )))
            else:
                infrastructure_error = False
            passed = bool(
                test_receipt and test_returncode == 0 and not infrastructure_error)
            record.update({
                "test_returncode": test_returncode,
                "test_infrastructure_error": infrastructure_error,
                "original_failing_tests_fixed": passed,
                "native_success": passed,
                "full_regression_suite_passed": None,
                "full_regression_suite_status": "CANNOT_CHECK_NOT_RUN",
                "critical_new_failure_count": None,
                "metamorphic_or_mutation_test_pass_rate": "NOT_RUN",
                "gold_patch_text_similarity_diagnostic": "WITHHELD_NOT_COMPUTED",
                "scientific_truth_authorized": False,
                "field_status_authorized": False,
                "stdout_tail": (
                    str(test_receipt.get("stdout_tail", ""))[-4000:] if test_receipt
                    else str(compile_receipt.get("stderr_tail", ""))[-4000:] if compile_receipt
                    else str(patch_result["stderr_tail"])[-4000:] if patch_result
                    else str(head["stderr_tail"])[-4000:]),
                "stderr_tail": (
                    str(test_receipt.get("stderr_tail", ""))[-4000:] if test_receipt
                    else str(compile_receipt.get("stderr_tail", ""))[-4000:] if compile_receipt
                    else str(patch_result["stderr_tail"])[-4000:] if patch_result
                    else str(head["stderr_tail"])[-4000:]),
            })
        except Exception as exc:  # never crash the array item; record honestly
            record.update({
                "status": "CANNOT_CHECK_EVALUATOR_FAILURE",
                "reason": f"{type(exc).__name__}: {exc}",
                "test_returncode": None,
                "test_infrastructure_error": None,
                "native_success": False,
                "original_failing_tests_fixed": False,
                "full_regression_suite_passed": None,
                "critical_new_failure_count": None,
                "scientific_truth_authorized": False,
                "field_status_authorized": False,
            })
        finally:
            record["wall_time_seconds"] = time.perf_counter() - started
            try:
                if workspace.exists():
                    shutil.rmtree(workspace)
                    record["workspace_cleanup"] = "removed_after_evaluation"
            except OSError as exc:
                record["workspace_cleanup"] = f"cleanup_failed: {exc}"
        return record

    return _evaluate_bugsinpy


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--arms", default="")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--timeout-seconds", type=int, default=10800)
    args = parser.parse_args()
    campaign = args.campaign.resolve()
    source = campaign / "source"
    scripts_dir = str(source / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    evaluator = load_module(
        "orion_evaluate_v2_frozen_lane",
        source / "scripts/evaluate_orion_real_problem_responses_v2.py")
    runtime = load_module(
        "orion_bugsinpy_runtime_frozen_lane",
        source / "scripts/bugsinpy_project_runtime.py")
    evaluator.runner._evaluate_bugsinpy = make_frozen_lane_evaluate_bugsinpy(
        evaluator.runner, runtime, campaign, source)
    arms = {item.strip() for item in args.arms.split(",") if item.strip()} or None
    tasks = {item.strip() for item in args.tasks.split(",") if item.strip()} or None
    count = evaluator.evaluate(
        args.workdir.resolve(), arms=arms, tasks=tasks,
        timeout_seconds=args.timeout_seconds)
    print(f"frozen-lane evaluations written: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
