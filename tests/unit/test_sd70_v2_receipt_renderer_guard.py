"""The SD70-V2 receipt renderer must refuse a degenerate rollup, not decorate it.

Two silent-failure modes are in scope, both of which fail toward the appearance
of strength:

*  a counter that never ran, printed as ``0``;
*  a contrast that could not exist, printed as a difference between two
   accuracies nobody measured.

``COULD_NOT_RENDER`` therefore has its own exit code (3), distinct from a usage
or IO error (1) and from a successful render (0).  The healthy fixture is
asserted too: a guard that fires on everything is a guard nobody keeps.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / "research" / "experiments" / "sd70-v2" / "sd70v2_make_receipt.py"

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_COULD_NOT_RENDER = 3

SP = "MAXMARGIN_PARENT"
F2 = "F2_RECURSIVE_META_DISCOVERY_FULL"
F2S = "F2_STATIC_NO_RECURSION"
MODEL_ARMS = (F2, F2S, "F2_FULL_MINUS_FAILURE_EVIDENCE",
              "F2_FULL_MINUS_PARENT_FEDERATION", "TARGET_ONLY_NEGATIVE_CONTROL")
DET_ARMS = (SP, "F0_PARENT_FEDERATION", "FIXED_META_LESSON",
            "STRONGEST_GENERATOR_FAITHFUL_PARENT", "SIMPLE_FREQUENCY_PARENT")


def _cost(model_calls: int, tokens: int | None) -> dict:
    return {
        "model_calls": model_calls,
        "attempts_total": model_calls,
        "retries": 0,
        "input_tokens": 0 if tokens is None else tokens // 2,
        "output_tokens": 0 if tokens is None else tokens - tokens // 2,
        "total_tokens": tokens,
        "tool_calls": 0,
        "wall_seconds_total": 1.0 * model_calls,
    }


def _arm(n: int, acc: float, failures: int, model_calls: int, tokens: int | None) -> dict:
    return {
        "n": n,
        "exact_accuracy": acc,
        "wilson95": [max(0.0, acc - 0.06), min(1.0, acc + 0.06)],
        "critical_false_direction_rate": 0.05,
        "arm_failures": failures,
        "chance_level": 0.262,
        "resource_cost": _cost(model_calls, tokens),
    }


def _contrast(point: float) -> dict:
    return {"point": point, "ci_low": point - 0.05, "ci_high": point + 0.05,
            "b": 20, "c": 18, "midp_one_sided_a_gt_b": 0.4}


def healthy_rollup() -> dict:
    arms: dict[str, dict] = {}
    for a in MODEL_ARMS:
        arms[a] = _arm(240, 0.70, 3, 240, 120_000)
    for a in DET_ARMS:
        arms[a] = _arm(240, 0.72, 0, 0, None)
    for a in (f"{SP}__LP", f"{SP}__QS"):
        arms[a] = _arm(240, 0.26, 0, 0, None)
    return {
        "route": "PARENT_SUFFICIENT",
        "design_sha256": "0" * 64,
        "task_count": 240,
        "strongest_generator_faithful_parent": SP,
        "arms": arms,
        "primary_outcomes": {
            "protected_decision_quality": {
                "F2_FULL_vs_SP": _contrast(-0.02),
                "F2_STATIC_vs_SP": _contrast(-0.03),
            },
            "holm": {
                "F2_FULL_vs_SP": {"holm_threshold": 0.025, "reject": False},
                "F2_STATIC_vs_SP": {"holm_threshold": 0.05, "reject": False},
            },
            "critical_false_direction": {"F2_FULL_vs_SP": _contrast(0.01)},
            "parent_non_regression": {"delta_ci_low": -0.07, "margin": 0.05, "holds": False},
        },
        "negative_controls": {
            f"{SP}__LP": {"accuracy": 0.26, "chance": 0.262,
                          "wilson95": [0.20, 0.32], "behaves": True},
        },
        "ablations": {"F2_FULL_minus_NO_FAILURE_EVIDENCE": _contrast(0.01)},
        "secondary": {"F0_vs_SP": _contrast(-0.01)},
        "missingness": {
            "model_arm_tasks": 1140, "model_arm_failures": 12,
            "global_failure_rate": 0.0105, "per_arm_exceeding_threshold": [],
        },
        "gates": {"delta_at_least_0_10": False},
        "cannot_check_reasons": [],
    }


CAMPAIGN_META = {
    "design_merge_sha": "7e3ad77", "host": "testhost", "partition": "testpart",
    "account": "testacct", "jobid": "0", "workdir": "/tmp/none",
    "code_state": "clean", "started_utc": "2026-09-03T00:00:00Z",
    "finished_utc": "2026-09-03T01:00:00Z", "alpha_family": 0.05,
    "global_failure_threshold": 0.05, "per_arm_failure_threshold": 0.10,
    "integrity_violations": 0, "dispatch_integrity_passed": True,
    "oracle_sha256": "1" * 64, "model": "gpt-5.6-terra", "deviations": "None.",
}


def _run(tmp_path: Path, rollup: dict) -> subprocess.CompletedProcess[str]:
    paths = {}
    for name, obj in (
        ("rollup.json", rollup),
        ("FROZEN_SUITE.json", {"seed_commitment": "2" * 64, "manifest_sha256": "3" * 64}),
        ("REQUEST_SURFACE_MANIFEST.json",
         {"arms": {"TARGET_ONLY_NEGATIVE_CONTROL": {"training_token_leaks_into_target_only": 0}}}),
        ("meta.json", CAMPAIGN_META),
    ):
        p = tmp_path / name
        p.write_text(json.dumps(obj))
        paths[name] = p
    out = tmp_path / "receipt.md"
    return subprocess.run(
        [sys.executable, str(RENDERER), str(paths["rollup.json"]),
         str(paths["FROZEN_SUITE.json"]), str(paths["REQUEST_SURFACE_MANIFEST.json"]),
         str(paths["meta.json"]), str(out)],
        capture_output=True, text=True,
    ), out


def test_healthy_rollup_renders_and_raises_no_alarm(tmp_path: Path) -> None:
    """The no-alarm case: a rollup that can carry the contrasts must render."""
    proc, out = _run(tmp_path, healthy_rollup())
    assert proc.returncode == EXIT_OK, proc.stderr
    text = out.read_text()
    assert "SD70_V2_ROUTE = PARENT_SUFFICIENT" in text
    assert "COULD_NOT_RENDER" not in text


@pytest.mark.parametrize(
    ("mutate", "needle"),
    [
        (lambda r: r["arms"][F2].update(n=0), "scored no task"),
        (lambda r: r["arms"][F2].update(arm_failures=240), "failed on every task"),
        (lambda r: r["arms"][F2]["resource_cost"].update(total_tokens=None),
         "token counter that never ran"),
        (lambda r: r["arms"][F2]["resource_cost"].update(model_calls=0), "records no model call"),
        (lambda r: r["arms"].pop(F2S), "is absent from the rollup"),
        (lambda r: r["primary_outcomes"]["protected_decision_quality"].pop("F2_FULL_vs_SP"),
         "registered primary contrast"),
    ],
)
def test_degenerate_rollup_is_refused_with_its_own_exit_code(
    tmp_path: Path, mutate, needle: str
) -> None:
    rollup = copy.deepcopy(healthy_rollup())
    mutate(rollup)
    proc, out = _run(tmp_path, rollup)
    assert proc.returncode == EXIT_COULD_NOT_RENDER, proc.stdout + proc.stderr
    assert proc.returncode != EXIT_USAGE
    payload = json.loads(proc.stderr)
    assert payload["status"] == "COULD_NOT_RENDER"
    assert any(needle in reason for reason in payload["reasons"]), payload
    assert not out.exists(), "a refused render must not leave a receipt behind"


def test_all_model_arms_failed_is_refused_not_rendered_as_a_contrast(tmp_path: Path) -> None:
    """Taxonomy #2: a contrast that could not exist must never reach the page."""
    rollup = copy.deepcopy(healthy_rollup())
    for arm in MODEL_ARMS:
        rollup["arms"][arm].update(n=240, arm_failures=240, exact_accuracy=0.0)
    proc, out = _run(tmp_path, rollup)
    assert proc.returncode == EXIT_COULD_NOT_RENDER, proc.stdout + proc.stderr
    assert not out.exists()


def test_usage_error_has_a_different_exit_code_than_could_not_render() -> None:
    proc = subprocess.run([sys.executable, str(RENDERER)], capture_output=True, text=True)
    assert proc.returncode == EXIT_USAGE
    assert proc.returncode != EXIT_COULD_NOT_RENDER
