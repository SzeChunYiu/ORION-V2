"""MACHINE_EPISTEMICS_FOUNDATION_V1 — registry and exact hostile checks."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "research" / "machine-epistemics-theory" / "machine_epistemics_foundation_v1_check.py"
REGISTRY = ROOT / "research" / "machine-epistemics-theory" / "MACHINE_EPISTEMICS_FOUNDATION_V1.json"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("machine_epistemics_foundation_v1_check", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_meg02_truth_and_actionability_are_distinct(mod):
    r = mod.check_meg02_truth_action_split()
    assert r["truth_without_exact_certificate"] == "UNKNOWN"
    assert r["risk_bounded_action"] == "AUTHORIZED_RISK_BOUNDED"
    assert r["mutant_score_to_truth_caught"] == 1
    assert r["strict_policy_refused"] == 1


def test_behavior_identity_drift_is_fail_closed(mod):
    r = mod.check_identity_drift()
    assert r == {"drift_fields_caught": 9, "unbound_fields_cannot_check": 1}


def test_meg16_corrected_nogood_algebra(mod):
    r = mod.check_meg16_nogood_algebra()
    assert r["profiles_n3"] == 20
    assert r["prefilter_only_mutant_caught"] == 1
    assert r["live_live_cross_nogood_terminal"] == "CONTRADICTED"
    assert r["atlas_unconditional_kleene_statement_refuted"] == 1
    assert r["conditional_kleene_checks"] > 0


def test_foundation_registry_is_complete_and_fail_closed(mod):
    data = json.loads(REGISTRY.read_text())
    r = mod.validate_registry(data)
    assert r["atlas_obligations"] == 36
    assert r["primitives"] >= 15
    assert r["pending_pr317_rows"] >= 1
    assert r["absorption_bindings"] >= 5


def test_registry_hostile_mutants_fire(mod):
    data = json.loads(REGISTRY.read_text())
    r = mod.check_registry_mutants(data)
    assert r["registry_mutants_caught"] == 5


def test_cli_exit_codes_are_distinct(mod, monkeypatch):
    assert mod.main(["--registry", str(REGISTRY)]) == 0
    monkeypatch.setattr(mod, "run_all", lambda *a, **k: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda *a, **k: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
