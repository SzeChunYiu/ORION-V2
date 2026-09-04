from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "research" / "machine-epistemics-theory" / "meg_frontier_f1_extraction_exact.py"
spec = importlib.util.spec_from_file_location("meg_frontier_f1_extraction_exact", MOD)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_every_deterministic_capacity_limited_selector_has_a_relevance_relabeling_miss():
    r = m.deterministic_impossibility(4, 2)
    assert r["selectors"] == 11
    assert r["selector_task_pairs"] == 44
    assert r["miss_pairs"] > 0


def test_randomization_cannot_give_zero_error_under_singleton_symmetry():
    p = m.randomized_uniform_k_subset(4, 2)
    assert set(p.values()) == {m.Fraction(1, 2)}


def test_certificate_is_exact_sufficient_condition_and_fails_closed():
    possible = (frozenset({"a"}), frozenset({"b"}), frozenset({"a", "b"}))
    ok, union = m.union_condition(possible, 2)
    assert ok and union == {"a", "b"}
    cert = m.ExtractionCoverageCertificate(union, 2, "F", "z", "checker", "S", "e")
    assert cert.validate(possible) == "CERTIFIED"
    bad = m.ExtractionCoverageCertificate(frozenset({"a"}), 2, "F", "z", "checker", "S", "e")
    assert bad.validate(possible) == "COVERAGE_NOT_PROVED"


def test_cli_terminal_and_non_novelty():
    p = subprocess.run([sys.executable, str(MOD)], capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stdout + p.stderr
    d = json.loads(p.stdout)
    assert d["status"] == "PASS"
    assert d["result"]["terminal"] == "NO_UNIVERSAL_NO_DROP_WITHOUT_DISCRIMINATING_STRUCTURE"
    assert d["result"]["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"
