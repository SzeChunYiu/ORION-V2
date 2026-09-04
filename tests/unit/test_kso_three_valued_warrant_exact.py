"""KSO_THREE_VALUED_WARRANT_AND_REOPENING_V1 — the checker's statements hold and its mutants fire."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory" / "kso_three_valued_warrant_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_three_valued_warrant_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_ks_t21_exhaustive_denominators(mod):
    r = mod.check_ks_t21(3)
    assert r == {"profiles": 20, "intervals": 168, "reduction_checks": 160, "homomorphism_checks": 168 * 168 * 8, "refinement_checks": 27920}


def test_completeness_bit_counterexample_fires(mod):
    r = mod.check_completeness_bit_counterexample()
    assert r["bit_reads"] == "UNKNOWN" and r["interval_reads"] == "DEAD" == r["kleene"]


def test_ks_t04c_head_share_clause(mod):
    r = mod.check_ks_t04c_head_share()
    assert r["head_renormalising_mutant_differs"] == 1 and r["witness_unrelated_unchanged"] == 1


def test_ks_t22_reopening_partition(mod):
    r = mod.check_ks_t22()
    assert r["reopen"] == ["a"] and r["recheck"] == ["b", "c", "d", "e"] and r["unaffected"] == ["x", "y", "z"]


def test_cli_exit_codes_are_three_and_distinct(mod, monkeypatch, capsys):
    assert mod.main([]) == 0
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(AssertionError("planted")))
    assert mod.main([]) == 1
    monkeypatch.setattr(mod, "run_all", lambda: (_ for _ in ()).throw(mod.CannotCheck("planted")))
    assert mod.main([]) == 2
