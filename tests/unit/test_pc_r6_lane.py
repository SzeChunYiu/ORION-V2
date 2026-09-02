"""PC-R6 full-regression lane: unit + end-to-end tests on a synthetic frozen campaign tree.

The end-to-end test drives `main()` through every stage (manifest, gr0a execute +
collect with the checker negative control, gr0b, gr0, suite, rollup) and then the
analysis script, on a synthetic two-cell campaign whose evaluator_private
workspace is a real git repository compiled by the REAL frozen runtime
(`bugsinpy_project_runtime.compile_workspace`) through the REAL frozen-lane
adapter closure.  The m5p precedent showed smoke tests that skip `main()` miss
runtime defects, so nothing here mocks the adapter.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PCR6 = ROOT / "research/experiments/pc-r6"
ADAPTER = ROOT / "research/experiments/results/issue45/e30-r11/drivers/e30_r11_arm_eval_frozen_lane.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lane = load("pc_r6_fullreg_eval", PCR6 / "pc_r6_fullreg_eval.py")
analysis = load("pc_r6_fullreg_analysis", PCR6 / "pc_r6_fullreg_analysis.py")

TASK = "bugsinpy-tqdm-1"
PROJECT = "tqdm"

BUGGY_INIT = "def add(a, b):\n    return a - b\n\n\ndef mul(a, b):\n    return a * b\n"
TEST_FILE = (
    "import unittest\n\nimport tqdm\n\n\nclass T(unittest.TestCase):\n"
    "    def test_add(self):\n        self.assertEqual(tqdm.add(2, 3), 5)\n\n"
    "    def test_mul(self):\n        self.assertEqual(tqdm.mul(2, 3), 6)\n\n"
    "    def test_other(self):\n        self.assertTrue(True)\n"
)


def diff(path: str, old: str, new: str) -> str:
    """Minimal unified diff for whole-file replacement (git apply compatible)."""
    old_lines, new_lines = old.splitlines(), new.splitlines()
    body = "".join(f"-{line}\n" for line in old_lines) + "".join(f"+{line}\n" for line in new_lines)
    return (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n"
            f"@@ -1,{len(old_lines)} +1,{len(new_lines)} @@\n{body}")


GOOD_INIT = BUGGY_INIT.replace("return a - b", "return a + b")
BREAK_MUL_INIT = GOOD_INIT.replace("return a * b", "return a * b + 1")
SYNTAX_ERROR_INIT = GOOD_INIT + "def broken(:\n"
BROKEN_TEST_FILE = "import nonexistent_module_pc_r6_xyz\n" + TEST_FILE

PATCHES = {
    "good": diff("tqdm/__init__.py", BUGGY_INIT, GOOD_INIT),
    "break_mul": diff("tqdm/__init__.py", BUGGY_INIT, BREAK_MUL_INIT),
    "garbage": "this is not a patch\n",
    "syntax_error": diff("tqdm/__init__.py", BUGGY_INIT, SYNTAX_ERROR_INIT),
    "break_test_import": diff("tests/test_tqdm.py", TEST_FILE, BROKEN_TEST_FILE),
}

E30_ARMS = {
    "F2_ORION_METABOLIC_FULL": ("good", True, 0),
    "F0_PARENT_FEDERATION": ("break_mul", True, 1),
    "SAME_MODEL_REFLECTION": ("garbage", False, None),
    "SIMPLE_DIRECT": ("syntax_error", False, None),
}
E60_ARMS = {
    "F2_ORION_METABOLIC_FULL": ("good", True, 0),
    "F2_MINUS_DECOMPOSITION": ("break_mul", True, 1),
    "F2_MINUS_NATIVE_RECOVERY": ("good", True, 0),
    "F2_MINUS_COUNTERPROBE": ("uncheckable", False, None),
    "F2_MINUS_SELECTIVE_REOPEN": ("break_test_import", False, 2),
}


def git(cwd: Path, *argv: str) -> str:
    completed = subprocess.run(["git", *argv], cwd=str(cwd), text=True, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
    return completed.stdout


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_workspace(root: Path) -> str:
    ws = root / "evaluator_private" / TASK
    (ws / "tqdm").mkdir(parents=True)
    (ws / "tests").mkdir()
    (ws / "tqdm/__init__.py").write_text(BUGGY_INIT)
    (ws / "tests/__init__.py").write_text("")
    (ws / "tests/test_tqdm.py").write_text(TEST_FILE)
    (ws / ".gitignore").write_text("__pycache__/\n*.pyc\n.orion-e30-env/\n")
    git(ws, "init", "-q", ".")
    git(ws, "add", ".")
    git(ws, "commit", "-q", "-m", "buggy")
    head = git(ws, "rev-parse", "HEAD").strip()
    (ws / "bugsinpy_run_test.sh").write_text("python -m unittest -q tests.test_tqdm.T.test_add\n")
    (ws / "bugsinpy_requirements.txt").write_text("")
    (ws / "bugsinpy_bug.info").write_text('python_version="3.8.3"\ntest_file="tests/test_tqdm.py"\n')
    return head


def build_campaign(root: Path, name: str, arms: dict, head: str | None = None) -> str:
    root.mkdir(parents=True)
    if head is None:
        head = build_workspace(root)
    source = root / "source"
    (source / "scripts").mkdir(parents=True)
    for script in ("evaluate_orion_real_problem_responses_v2.py", "run_orion_real_problem_suite.py",
                   "bugsinpy_project_runtime.py"):
        shutil.copy(ROOT / "scripts" / script, source / "scripts" / script)
    (source / "research/experiments").mkdir(parents=True)
    shutil.copy(ROOT / "research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json",
                source / "research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json")
    cache = root / "offline-cache"
    cache.mkdir()
    (cache / "manifest.json").write_text(json.dumps({
        "schema_version": "orion.v2.bugsinpy-offline-distribution-cache.v1", "artifacts": []}))
    binding = root / f"{PROJECT}-prospective-binding.json"
    binding.write_text(json.dumps({
        "schema_version": "orion.v2.bugsinpy-prospective-runtime-binding.v2", "project": PROJECT,
        "dependency_pins": {}, "requirement_dispositions": {}, "marker_decisions": {},
        "legacy_build": {}, "distribution_overrides": {}, "distribution_override_prerequisites": {}}))
    mirror = root / "mirror"
    mirror.mkdir()
    (root / "SETUP_RECEIPT.json").write_text(json.dumps({
        "mirrors": [{"project": PROJECT, "mirror": str(mirror), "url": "https://example.invalid/tqdm"}],
        "prospective_bindings": {PROJECT: {"path": str(binding), "compiler_compat_cflags": ""}},
        "project_pythons": {"3.8.3": sys.executable},
        "offline_cache": {"directory": str(cache), "manifest": str(cache / "manifest.json")},
    }))
    rep = root / "run/confirmatory-r1"
    (rep / "responses").mkdir(parents=True)
    (rep / "evaluations").mkdir(parents=True)
    task = {"task_id": TASK, "project": PROJECT, "bug_id": 1, "python_version": "3.8.3",
            "expected_buggy_commit": head, "adapter": "bugsinpy", "benchmark_id": "bugsinpy"}
    (rep / "frozen_tasks.json").write_text(json.dumps({"tasks": [task]}))
    for arm, (kind, native, _count) in arms.items():
        (rep / "responses" / arm).mkdir()
        (rep / "evaluations" / arm).mkdir()
        if kind == "uncheckable":
            response = {"task_id": TASK, "arm_id": arm, "status": "COMPLETED_PROPOSAL_ONLY",
                        "proposed_patch_or_artifact": None}
        else:
            response = {"task_id": TASK, "arm_id": arm, "status": "COMPLETED_PROPOSAL_ONLY",
                        "proposed_patch_or_artifact": {"type": "unified_diff", "content": PATCHES[kind]}}
        (rep / "responses" / arm / f"{TASK}.json").write_text(json.dumps(response))
        (rep / "evaluations" / arm / f"{TASK}.json").write_text(json.dumps({
            "task_id": TASK, "arm_id": arm, "native_success": native, "agent_status": "COMPLETED_PROPOSAL_ONLY",
            "full_regression_suite_passed": None, "critical_new_failure_count": None,
            "evaluation_lane": "orion.v2.e30-r11-frozen-lane-arm-eval-adapter.v3"}))
    return head


def build_truth(truth: Path, e60_root: Path) -> None:
    (truth / "e30-r11").mkdir(parents=True)
    table = {f"{arm}/{TASK}": {"r1": {"native_success": native, "status": None,
                                      "agent_status": "COMPLETED_PROPOSAL_ONLY",
                                      "full_regression_suite_passed": None}}
             for arm, (_k, native, _c) in E30_ARMS.items()}
    (truth / "e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json").write_text(json.dumps({
        "paired_task_table": table, "freeze_sha256": "synthetic",
        "per_arm_totals": {arm: {"native_success": int(native)} for arm, (_k, native, _c) in E30_ARMS.items()}}))
    e60 = truth / "e60-r1-component-ablation"
    e60.mkdir()
    arm_summaries = {arm: {"success_count": int(native), "project_strata": {PROJECT: {"success_count": int(native)}}}
                     for arm, (_k, native, _c) in E60_ARMS.items()}
    (e60 / "E60_R1_COMPONENT_ABLATION_ANALYSIS.json").write_text(json.dumps({"arm_summaries": arm_summaries}))
    effects = {}
    full = E60_ARMS["F2_ORION_METABOLIC_FULL"][1]
    for arm, (_k, native, _c) in E60_ARMS.items():
        if arm == "F2_ORION_METABOLIC_FULL":
            continue
        table = {"both_true": int(full and native), "left_only": int(full and not native),
                 "right_only": int(native and not full), "both_false": int(not full and not native)}
        effects[arm] = {"left_arm": "F2_ORION_METABOLIC_FULL", "right_arm": arm,
                        "success": {"paired_table": table}}
    (e60 / "component_effects.json").write_text(json.dumps(effects))
    record = e60_root / "run/confirmatory-r1/evaluations/F2_MINUS_DECOMPOSITION" / f"{TASK}.json"
    (e60 / "supersede.sha256").write_text(f"{sha(record)}  {record}\n")


@pytest.fixture(scope="module")
def campaign(tmp_path_factory) -> dict:
    base = tmp_path_factory.mktemp("pc_r6")
    e30 = base / lane.CELLS["e30r11"]["campaign"]
    e60 = base / lane.CELLS["e60"]["campaign"]
    head = build_campaign(e30, "e30", E30_ARMS)
    build_campaign(e60, "e60", E60_ARMS, head=None)
    gold = e30 / f"baseline_lanes/{TASK}/BugsInPy/projects/{PROJECT}/bugs/1/bug_patch.txt"
    gold.parent.mkdir(parents=True)
    gold.write_text(PATCHES["good"])
    truth = base / "truth"
    build_truth(truth, e60)
    out = base / "pc-r6-out"
    common = ["--e30-campaign", str(e30), "--e60-campaign", str(e60), "--adapter", str(ADAPTER),
              "--out", str(out), "--truth-dir", str(truth), "--allow-partial-cells", "--date", "20260902"]
    return {"base": base, "e30": e30, "e60": e60, "out": out, "truth": truth, "common": common}


# --------------------------------------------------------------------------- pure functions
def test_plan_suite_pytest_and_tox(tmp_path: Path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests/test_a.py").write_text("")
    (tmp_path / "tests/test_b.py").write_text("")
    plan = lane.plan_suite("pytest tests/test_a.py::test_x\npytest tests/test_a.py::C::test_y\n"
                           "python3 -m pytest tests/test_b.py::test_z\n", tmp_path,
                           'test_file="tests/test_a.py;tests/test_b.py"\n')
    assert plan["runner_family"] == "pytest"
    assert plan["test_files"] == ["tests/test_a.py", "tests/test_b.py"]
    assert plan["pytest_flags"] == []
    assert plan["bug_info_crosscheck"]["matches_registered_command_files"] is True
    tox = lane.plan_suite("tox tests/test_a.py::test_x\n", tmp_path)
    assert tox["pytest_flags"] == ["-q", "-o", "addopts="]
    assert tox["test_files"] == ["tests/test_a.py"]


def test_plan_suite_unittest_and_mixed(tmp_path: Path):
    (tmp_path / "tornado/test").mkdir(parents=True)
    (tmp_path / "tornado/__init__.py").write_text("")
    (tmp_path / "tornado/test/__init__.py").write_text("")
    (tmp_path / "tornado/test/web_test.py").write_text("")
    plan = lane.plan_suite("python -m unittest -q tornado.test.web_test.StaticFileTest.test_a\n"
                           "python -m unittest -q tornado.test.web_test.StaticFileTest.test_b\n", tmp_path)
    assert plan["runner_family"] == "unittest"
    assert plan["unittest_modules"] == ["tornado.test.web_test"]
    assert plan["test_files"] == ["tornado/test/web_test.py"]
    with pytest.raises(lane.LaneError):
        lane.plan_suite("pytest tornado/test/web_test.py::t\npython -m unittest -q tornado.test.web_test\n", tmp_path)
    with pytest.raises(lane.LaneError):
        lane.plan_suite("pytest tests/missing.py::t\n", tmp_path)
    with pytest.raises(lane.LaneError):
        lane.plan_suite("make test\n", tmp_path)


def test_parse_junit_outcomes(tmp_path: Path):
    xml = tmp_path / "j.xml"
    xml.write_text(
        '<testsuites><testsuite name="pytest">'
        '<testcase classname="tests.test_a" name="test_ok"/>'
        '<testcase classname="tests.test_a" name="test_param[1-2]"><failure message="x"/></testcase>'
        '<testcase classname="tests.test_a.C" name="test_err"><error message="y"/></testcase>'
        '<testcase classname="tests.test_a" name="test_skip"><skipped message="z"/></testcase>'
        '</testsuite></testsuites>')
    assert lane.parse_junit(xml) == {
        "tests.test_a::test_ok": "passed", "tests.test_a::test_param[1-2]": "failed",
        "tests.test_a.C::test_err": "error", "tests.test_a::test_skip": "skipped"}


def test_derive_critical_counts_missing_skipped_error_conservatively():
    baseline = {"a": "passed", "b": "passed", "c": "passed", "d": "passed", "e": "failed", "f": "skipped"}
    patched = {"a": "passed", "b": "failed", "c": "error", "d": "skipped", "e": "passed"}
    derived = lane.derive_critical(baseline, patched)
    assert derived["critical_new_failure_count"] == 3
    assert derived["critical_new_failure_breakdown"] == {"failed": 1, "error": 1, "skipped": 1, "missing": 0}
    assert derived["newly_passing_count"] == 1
    missing = lane.derive_critical(baseline, {})
    assert missing["critical_new_failure_count"] == 4
    assert missing["critical_new_failure_breakdown"]["missing"] == 4
    assert lane.derive_critical(baseline, dict(baseline))["critical_new_failure_count"] == 0


def test_checker_negative_control_and_compare():
    frozen = {("1", "A", "t1"): True, ("1", "A", "t2"): False, ("1", "B", "t1"): None}
    control = lane.checker_negative_control(frozen)
    assert control["pass"] is True and control["flipped_detected"] == 1 and control["dropped_detected"] == 1
    assert lane.compare_vectors(frozen, dict(frozen))["bit_exact"]
    bad = dict(frozen)
    bad[("1", "B", "t1")] = False  # None -> False is a mismatch, never silently equal
    assert lane.compare_vectors(frozen, bad)["mismatched"] == 1
    assert lane.checker_negative_control({})["pass"] is False


def test_baseline_marker_patch_applies_cleanly(tmp_path: Path):
    git(tmp_path, "init", "-q", ".")
    (tmp_path / "f").write_text("x\n")
    git(tmp_path, "add", "f")
    git(tmp_path, "commit", "-q", "-m", "i")
    completed = subprocess.run(["git", "apply", "--whitespace=nowarn", "-"], cwd=str(tmp_path),
                               input=lane.BASELINE_MARKER_PATCH, text=True, check=False)
    assert completed.returncode == 0
    assert (tmp_path / ".orion-pc-r6-baseline-marker").is_file()


def test_frozen_constants_match_design():
    design = json.loads((PCR6 / "PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1.json").read_text())
    assert lane.SUITE_TIMEOUT_SECONDS == design["stage_spec"]["suite_timeout_s"] == 900
    assert lane.CELLS["e30r11"]["campaign"] == design["cells"]["primary_e30r11"]["campaign"]
    assert lane.CELLS["e30r11"]["arms"] == design["cells"]["primary_e30r11"]["arms"]
    assert lane.CELLS["e60"]["campaign"] == design["cells"]["component_e60"]["campaign"]
    assert lane.CELLS["e60"]["arms"] == design["cells"]["component_e60"]["arms"]
    assert lane.CELLS["e30r11"]["evaluations"] == 480 and lane.CELLS["e60"]["evaluations"] == 600
    assert analysis.SEED == lane.SEED == 20260902
    assert analysis.BOOTSTRAP_DRAWS == 10000
    assert analysis.NON_INFERIORITY_MARGIN == 0.02 and analysis.NECESSITY_MARGIN == 0.02
    assert analysis.CELL_FAMILIES["e30r11"]["family_size"] == design["statistics"]["families"]["cell1"] == 3
    assert analysis.CELL_FAMILIES["e60"]["family_size"] == design["statistics"]["families"]["cell2"] == 4
    assert lane.FROZEN_ADAPTER_SHA256 == sha(ADAPTER)


# --------------------------------------------------------------------------- end-to-end via main()
def test_main_manifest_stage(campaign):
    rc = lane.main(["--stage", "manifest", *campaign["common"]])
    assert rc == 0
    payload = json.loads((campaign["out"] / "PC_R6_INPUT_MANIFEST.json").read_text())
    assert payload["campaign_id"].startswith("campaign-pc-r6-fullreg-e30r11-e60-20260902-")
    assert len(payload["manifest8"]) == 8
    lines = (campaign["out"] / "PC_R6_INPUT_MANIFEST.sha256").read_text().splitlines()
    labels = [line.split("  ", 1)[1] for line in lines]
    assert labels == sorted(labels) and len(lines) == payload["entry_count"]
    assert any(line.endswith(f"gold/{TASK}/bug_patch.txt") for line in lines)
    assert any("responses/F2_ORION_METABOLIC_FULL" in line for line in lines)
    assert any(line.endswith("@HEAD") for line in lines)
    assert payload["frozen_lane_adapter_sha256"] == lane.FROZEN_ADAPTER_SHA256


def test_main_list_indices(campaign, capsys):
    assert lane.main(["--stage", "list-indices", *campaign["common"]]) == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert out == [f"0\te30r11\t{TASK}", f"1\te60\t{TASK}"]


def test_main_gr0a_execute_collect_and_negative_control(campaign):
    for index in (0, 1):
        assert lane.main(["--stage", "gr0a", "--execute", "--index", str(index), *campaign["common"]]) == 0
    out = campaign["out"]
    for arm, (_kind, native, _count) in E30_ARMS.items():
        record = json.loads((out / "records_gr0a/e30r11/r1" / arm / f"{TASK}.json").read_text())
        assert record["native_success"] is native, arm
        assert record["pc_r6"]["suite"] is None  # gr0a never runs the suite
        assert record["evaluation_lane"] == "orion.v2.e30-r11-frozen-lane-arm-eval-adapter.v3" or record.get("pc_r6_uncheckable")
    for arm, (_kind, native, _count) in E60_ARMS.items():
        record = json.loads((out / "records_gr0a/e60/r1" / arm / f"{TASK}.json").read_text())
        assert record["native_success"] is native, arm
    assert lane.main(["--stage", "gr0a", *campaign["common"]]) == 0
    receipt = json.loads((out / "PC_R6_GR0A_RECEIPT.json").read_text())
    assert receipt["status"] == "PASS"
    assert receipt["cells"]["e30r11"]["reproduction"] == "4/4"
    assert receipt["cells"]["e60"]["reproduction"] == "5/5"
    assert receipt["checker_validation"]["e30r11"]["pass"] and receipt["checker_validation"]["e60"]["pass"]
    assert receipt["cells"]["e30r11"]["anchors"]["campaign_evaluation_records_cross_check"]["bit_exact"]
    assert receipt["cells"]["e60"]["anchors"]["pass"]
    # negative control at the record level: corrupt one new-lane record -> collect must FAIL
    target = out / "records_gr0a/e30r11/r1/F2_ORION_METABOLIC_FULL" / f"{TASK}.json"
    original = target.read_text()
    corrupted = json.loads(original)
    corrupted["native_success"] = False
    target.write_text(json.dumps(corrupted))
    try:
        assert lane.main(["--stage", "gr0a", *campaign["common"]]) == 1
        bad = json.loads((out / "PC_R6_GR0A_RECEIPT.json").read_text())
        assert bad["status"] == "FAIL"
        assert bad["cells"]["e30r11"]["comparison"]["mismatched"] == 1
        assert bad["cells"]["e30r11"]["comparison"]["mismatch_list"][0]["key"] == ["1", "F2_ORION_METABOLIC_FULL", TASK]
    finally:
        target.write_text(original)
    assert lane.main(["--stage", "gr0a", *campaign["common"]]) == 0
    # a drifted in-repo truth anchor must also fail the cell
    truth_rollup = campaign["truth"] / "e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json"
    saved = truth_rollup.read_text()
    drifted = json.loads(saved)
    drifted["paired_task_table"][f"SIMPLE_DIRECT/{TASK}"]["r1"]["native_success"] = True
    truth_rollup.write_text(json.dumps(drifted))
    try:
        assert lane.main(["--stage", "gr0a", *campaign["common"]]) == 1
    finally:
        truth_rollup.write_text(saved)
    assert lane.main(["--stage", "gr0a", *campaign["common"]]) == 0


def test_main_gr0b_gold_control_and_combine(campaign):
    out = campaign["out"]
    assert lane.main(["--stage", "gr0b", *campaign["common"]]) == 0
    receipt = json.loads((out / "PC_R6_GR0B_RECEIPT.json").read_text())
    assert receipt["status"] == "PASS"
    item = receipt["tasks"][0]
    assert item["task_id"] == TASK and item["bug_reproduced_at_baseline"] is True
    assert item["gold_native_success"] is True and item["critical_new_failure_count"] == 0
    assert item["baseline_passing_count"] == 2 and item["newly_passing_count"] == 1
    record = json.loads((out / "records_gr0b/e30r11/gold" / f"{TASK}.json").read_text())
    assert record["gold_or_fixed_solution_accessed"] is True
    assert lane.main(["--stage", "gr0", "--out", str(out)]) == 0
    combined = json.loads((out / "PC_R6_GR0_RECEIPT.json").read_text())
    assert combined["gr0_status"] == "PASS"


def test_main_suite_rollup_and_analysis(campaign, tmp_path: Path):
    out = campaign["out"]
    for index in (0, 1):
        assert lane.main(["--stage", "suite", "--index", str(index), *campaign["common"]]) == 0
    baseline = json.loads((out / "records/e30r11/baseline" / f"{TASK}.json").read_text())
    assert baseline["status"] == "BASELINE_OK" and baseline["bug_reproduced_at_baseline"] is True
    assert baseline["suite"]["tests"] == {"tests.test_tqdm.T.test_add": "failed",
                                          "tests.test_tqdm.T.test_mul": "passed",
                                          "tests.test_tqdm.T.test_other": "passed"}
    expected_status = {
        "F2_ORION_METABOLIC_FULL": "COUNTED", "F0_PARENT_FEDERATION": "COUNTED",
        "SAME_MODEL_REFLECTION": "NONE_PATCH_NOT_APPLIED", "SIMPLE_DIRECT": "NONE_COMPILE_FAILED",
    }
    for arm, (_kind, native, count) in E30_ARMS.items():
        record = json.loads((out / "records/e30r11/r1" / arm / f"{TASK}.json").read_text())
        assert record["native_success"] is native, arm
        assert record["critical_new_failure_count"] == count, arm
        assert record["pc_r6"]["critical_new_failure_status"] == expected_status[arm], arm
        assert record["frozen_lane_original"]["critical_new_failure_count"] is None
        if count == 0:
            assert record["full_regression_suite_passed"] is True
        elif count is None:
            assert record["full_regression_suite_passed"] is None
            assert record["full_regression_suite_status"].startswith("CANNOT_CHECK_NONE_")
        else:
            assert record["full_regression_suite_passed"] is False
    e60_status = {"F2_MINUS_COUNTERPROBE": "NONE_RESPONSE_UNCHECKABLE", "F2_MINUS_SELECTIVE_REOPEN": "COUNTED"}
    for arm, (_kind, native, count) in E60_ARMS.items():
        record = json.loads((out / "records/e60/r1" / arm / f"{TASK}.json").read_text())
        assert record["native_success"] is native, arm
        assert record["critical_new_failure_count"] == count, arm
        if arm in e60_status:
            assert record["pc_r6"]["critical_new_failure_status"] == e60_status[arm]
    broken = json.loads((out / "records/e60/r1/F2_MINUS_SELECTIVE_REOPEN" / f"{TASK}.json").read_text())
    assert broken["pc_r6"]["critical_new_failure_breakdown"]["missing"] == 2
    # resumable: second run skips existing records
    assert lane.main(["--stage", "suite", "--index", "0", *campaign["common"]]) == 0
    log = json.loads((out / "logs/records" / f"e30r11-{TASK}.json").read_text())
    assert all(item.get("skipped") == "exists" for item in log["evaluations"])
    assert lane.main(["--stage", "rollup", *campaign["common"]]) == 0
    rollup = json.loads((out / "PC_R6_FULLREG_RAW_ROLLUP_V1.json").read_text())
    assert rollup["complete"] is True
    totals = rollup["cells"]["e30r11"]["arm_totals"]
    assert totals["F2_ORION_METABOLIC_FULL"]["counted"] == 1
    assert totals["SAME_MODEL_REFLECTION"]["none_reasons"] == {"NONE_PATCH_NOT_APPLIED": 1}
    assert totals["SIMPLE_DIRECT"]["compile_failure_rate"] == 1.0
    assert (out / "PC_R6_READ_MANIFEST.sha256").is_file()
    # analysis refuses without a GR0 PASS receipt, then runs
    analysis_out = tmp_path / "analysis"
    common = ["--rollup", str(out / "PC_R6_FULLREG_RAW_ROLLUP_V1.json"),
              "--analyzer", str(ROOT / "scripts/analyze_orion_real_problem_results.py"), "--out", str(analysis_out)]
    assert analysis.main([*common, "--gr0-receipt", str(tmp_path / "missing.json")]) == 2
    failing = tmp_path / "gr0-fail.json"
    failing.write_text(json.dumps({"gr0_status": "FAIL", "components": {}}))
    assert analysis.main([*common, "--gr0-receipt", str(failing)]) == 2
    assert not (analysis_out / "PC_R6_FULLREG_ROLLUP_V1.json").exists()
    assert analysis.main([*common, "--gr0-receipt", str(out / "PC_R6_GR0_RECEIPT.json")]) == 0
    result = json.loads((analysis_out / "PC_R6_FULLREG_ROLLUP_V1.json").read_text())
    cell1 = result["cells"]["e30r11"]
    f2_f0 = next(c for c in cell1["contrasts"] if c["right_arm"] == "F0_PARENT_FEDERATION")
    assert f2_f0["checkable_task_count"] == 1 and f2_f0["paired_table"]["right_only"] == 1
    assert f2_f0["risk_difference"]["estimate"] == -1.0
    assert f2_f0["risk_difference"]["seed"] == 20260902 and f2_f0["risk_difference"]["bootstrap_repetitions"] == 10000
    assert result["gates"]["GR1"]["status"] == "PASS"
    assert result["gates"]["GR2"]["status"] in {"NULL", "FIRED"}
    assert (analysis_out / "PC_R6_OUTCOME_RECEIPT.md").is_file()
    assert "mean-success" in (analysis_out / "PC_R6_OUTCOME_RECEIPT.md").read_text()


# --------------------------------------------------------------------------- analysis statistics
def synthetic_rollup(seed: int = 7) -> dict:
    import random
    rng = random.Random(seed)
    projects = ["ansible", "black", "cookiecutter", "fastapi", "pandas", "scrapy", "tornado", "tqdm"]
    task_ids = [f"bugsinpy-{p}-{i}" for p in projects for i in range(1, 6)]
    cells = {}
    for cell_name, arms in (("e30r11", lane.CELLS["e30r11"]["arms"]), ("e60", lane.CELLS["e60"]["arms"])):
        evaluations = {}
        arm_totals = {}
        for arm in arms:
            rate = 0.05 if arm == "F2_ORION_METABOLIC_FULL" else 0.25
            for task_id in task_ids:
                reps = {}
                for rep in ("r1", "r2", "r3"):
                    roll = rng.random()
                    if roll < 0.15:
                        reps[rep] = {"critical_new_failure_count": None,
                                     "critical_new_failure_status": "NONE_PATCH_NOT_APPLIED"}
                    else:
                        reps[rep] = {"critical_new_failure_count": int(rng.random() < rate) * rng.randint(1, 3),
                                     "critical_new_failure_status": "COUNTED"}
                evaluations[f"{arm}/{task_id}"] = reps
            arm_totals[arm] = {"evaluations": 120, "patch_apply_failure_rate": 0.15,
                               "compile_failure_rate": 0.0, "checkable_rate": 0.85}
        cells[cell_name] = {"campaign": cell_name, "arms": arms, "reps": ["1", "2", "3"], "task_ids": task_ids,
                            "task_projects": {t: t.split("-")[1] for t in task_ids},
                            "baselines": {t: {"status": "BASELINE_OK"} for t in task_ids},
                            "evaluations": evaluations, "arm_totals": arm_totals}
    return {"complete": True, "cells": cells}


@pytest.fixture(scope="module")
def analyzer():
    return load("frozen_analyzer_for_pc_r6", ROOT / "scripts/analyze_orion_real_problem_results.py")


def test_analysis_statistics_deterministic_and_gated(analyzer, tmp_path: Path):
    import functools
    analyzer.paired_bootstrap_difference = functools.partial(
        analyzer.paired_bootstrap_difference, repetitions=analysis.BOOTSTRAP_DRAWS, seed=analysis.SEED)
    rollup = synthetic_rollup()
    first = {name: analysis.analyze_cell(name, cell, analyzer) for name, cell in rollup["cells"].items()}
    second = {name: analysis.analyze_cell(name, cell, analyzer) for name, cell in rollup["cells"].items()}
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    cell1 = first["e30r11"]
    assert cell1["multiplicity"]["registered_family_size"] == 3
    assert first["e60"]["multiplicity"]["registered_family_size"] == 4
    for item in cell1["contrasts"]:
        rd = item["risk_difference"]
        assert rd["bootstrap_stratification"] == "PROJECT" and rd["seed"] == 20260902
        assert rd["ci95"][0] <= rd["estimate"] <= rd["ci95"][1]
        assert item["one_sided_97_5_upper_bound"] == rd["ci95"][1]
        assert item["swapped_orientation"]["negation_consistent"] is True
        assert item["checkable_task_count"] + len(item["missing_task_ids"]) == 40
        assert item["multiplicity_status"] == "HOLM_ADJUSTED"
    gates = analysis.evaluate_gates(first)
    assert gates["GR1"]["status"] in {"PASS", "FAIL"}
    assert gates["GR1"]["one_sided_97_5_upper_bound"] == next(
        c for c in cell1["contrasts"] if c["right_arm"] == "F0_PARENT_FEDERATION")["one_sided_97_5_upper_bound"]
    assert len(gates["GR2"]["considered"]) == 7
    assert len(gates["GR3"]["considered"]) == 4
    for entry in gates["GR3"]["considered"]:
        assert entry["contrast"].startswith("F2_MINUS_") and entry["contrast"].endswith("- F2_ORION_METABOLIC_FULL")
    assert gates["routing"]


def test_majority_keeps_none_in_denominator(analyzer):
    assert analyzer.frozen_majority([True, None, None]) is None
    assert analyzer.frozen_majority([True, True, None]) is True
    assert analyzer.frozen_majority([False, False, True]) is False
    assert analysis.any_true_aggregate([False, None, None]) is None
    assert analysis.any_true_aggregate([False, True, None]) is True


def test_gates_all_cannot_check_when_nothing_checkable(analyzer):
    import functools
    analyzer.paired_bootstrap_difference = functools.partial(
        analyzer.paired_bootstrap_difference, repetitions=100, seed=analysis.SEED)
    rollup = synthetic_rollup()
    for cell in rollup["cells"].values():
        for reps in cell["evaluations"].values():
            for rep in reps.values():
                rep["critical_new_failure_count"] = None
                rep["critical_new_failure_status"] = "NONE_SUITE_TIMEOUT"
    cells = {name: analysis.analyze_cell(name, cell, analyzer) for name, cell in rollup["cells"].items()}
    gates = analysis.evaluate_gates(cells)
    assert gates["GR1"]["status"] == "CANNOT_CHECK"
    assert gates["GR2"]["status"] == "CANNOT_CHECK" and gates["GR3"]["status"] == "CANNOT_CHECK"
    assert gates["routing"].startswith("CANNOT_CHECK")
    for item in cells["e30r11"]["contrasts"]:
        assert item["checkable_task_count"] == 0 and item.get("holm_adjusted_p") is None
