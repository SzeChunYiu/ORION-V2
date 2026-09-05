"""Scope witnesses from review of PR359 head564b6a9; no protected outcomes."""
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_field_frontier_batch8_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("batch8_review_boundaries", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_optimized_cli_cannot_report_a_verified_terminal():
    result = subprocess.run([sys.executable, "-O", str(PATH)], capture_output=True, text=True, timeout=10)
    assert result.returncode == 2
    report = json.loads(result.stdout)
    assert report["status"] == "CANNOT_CHECK" and "ASSERTIONS_DISABLED" in report["reason"]
    assert "ITEM_STATUS" not in report and "ALL_HOLD" not in result.stdout


def test_optimized_direct_checkers_refuse_before_mutant_execution():
    # The original verifier returned ALL_HOLD with this false validity oracle under -O.
    script = """
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location('batch8_optimized_review', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.actual_validity = lambda roots, sigma: True
refused = []
for name, check in [('run_all', module.run_all), *module.CHECKS.items()]:
    try:
        check()
    except module.CannotCheck as exc:
        if 'ASSERTIONS_DISABLED' not in str(exc):
            raise SystemExit('wrong refusal')
        refused.append(name)
    else:
        raise SystemExit('optimized checker accepted: ' + name)
print(json.dumps(refused))
"""
    result = subprocess.run([sys.executable, "-O", "-c", script, str(PATH)],
                            capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert len(json.loads(result.stdout)) == 5


def test_uncovered_root_does_not_exclude_sound_partial_decisions(mod):
    roots = frozenset({"x1", "x2"})
    coverage = {"x1": "UNCOVERED", "x2": "MONITORED", "x3": "UNCOVERED"}
    assert mod.closure_certificate(roots, coverage)[0] == "NO_CLOSURE"
    decided = 0
    for bits in itertools.product((0, 1), repeat=3):
        sigma = dict(zip(mod.ROOTS, bits))
        view = mod.registered_view(coverage, sigma)
        partial = "INVALID" if view == (0,) else "UNKNOWN"
        if partial == "INVALID":
            assert not mod.actual_validity(roots, sigma)
            decided += 1
    assert decided == 4
    all_true, hidden_false = dict(mod.SIGMA0), dict(mod.SIGMA0, x1=0)
    assert mod.registered_view(coverage, all_true) == mod.registered_view(coverage, hidden_false)
    assert mod.actual_validity(roots, all_true) != mod.actual_validity(roots, hidden_false)


def test_three_risk_repetitions_can_reduce_exact_space_under_one_total_error(mod):
    # A boundary witness, not a replacement general stochastic-channel theorem.
    checked = 0
    for truth in mod.HYPS:
        for errors in ((), (0,), (1,), (2,)):
            transcript = tuple(mod.hval(truth, 3) ^ (i in errors) for i in range(3))
            remaining = frozenset(h for h in mod.HYPS
                                  if sum(mod.hval(h, 3) != answer for answer in transcript) <= 1)
            assert truth in remaining and len(remaining) == 8
            assert mod.determined_inputs(remaining) == {3}
            checked += 1
    assert checked == 64


def test_fresh_identity_deletion_is_outside_registered_composition_claim(mod):
    original = mod.base_state()
    fresh = mod.fresh_id(original)
    admit = lambda state: mod.admit(state, fresh, "b")
    delete = lambda state: mod.delete(state, fresh)
    admitted = admit(original)
    assert not any(label == "delete:" + fresh for label, _ in mod.menu(admitted))
    assert mod.classify(original, [("admit:b", admit)]) == "BOI_STABLE"
    assert mod.pi_sem(delete(admitted)) == mod.pi_sem(original)
    assert mod.classify(original, [("admit:b", admit), ("delete:" + fresh, delete)]) == "ESI"
