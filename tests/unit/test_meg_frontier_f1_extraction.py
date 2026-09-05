from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from dataclasses import replace
import itertools
import pytest

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "research" / "machine-epistemics-theory" / "meg_frontier_f1_extraction_exact.py"
spec = importlib.util.spec_from_file_location("meg_frontier_f1_extraction_exact", MOD)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m
spec.loader.exec_module(m)

UNIVERSE = frozenset({"a", "b", "c"})
CTX = dict(universe=UNIVERSE, capacity=2, task_family="F", state_digest="z", checker_id="checker", scope="S", epoch="e")


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
    cert = m.ExtractionCoverageCertificate(union, 2, "F", "z", "checker", "S", "e", UNIVERSE, m.family_digest(UNIVERSE, possible))
    assert cert.validate(possible, **dict(CTX, registered_family_digest=m.family_digest(UNIVERSE, possible))) == "CERTIFIED"
    bad = m.ExtractionCoverageCertificate(frozenset({"a"}), 2, "F", "z", "checker", "S", "e", UNIVERSE, m.family_digest(UNIVERSE, possible))
    assert bad.validate(possible, **dict(CTX, registered_family_digest=m.family_digest(UNIVERSE, possible))) == "COVERAGE_NOT_PROVED"


def test_certificate_identity_drift_is_cannot_check():
    possible = (frozenset({"a"}),)
    cert = m.ExtractionCoverageCertificate(frozenset({"a"}), 2, "F", "z", "checker", "S", "e", UNIVERSE, m.family_digest(UNIVERSE, possible))
    for key, value in {
        "capacity": 3,
        "task_family": "G",
        "state_digest": "z2",
        "checker_id": "checker2",
        "scope": "T",
        "epoch": "e2",
    }.items():
        ctx = dict(CTX, registered_family_digest=m.family_digest(UNIVERSE, possible)); ctx[key] = value
        assert cert.validate(possible, **ctx) == "CANNOT_CHECK_IDENTITY_DRIFT"


def test_cli_terminal_and_non_novelty():
    p = subprocess.run([sys.executable, str(MOD)], capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stdout + p.stderr
    d = json.loads(p.stdout)
    assert d["status"] == "PASS"
    assert d["result"]["certificate_identity_drift_dimensions_caught"] == 6
    assert d["result"]["terminal"] == "NO_UNIVERSAL_NO_DROP_WITHOUT_DISCRIMINATING_STRUCTURE"
    assert d["result"]["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"


def test_declared_family_cannot_be_silently_truncated_or_candidates_minted():
    possible = (frozenset({"a"}), frozenset({"b"}))
    digest = m.family_digest(UNIVERSE, possible)
    ctx = dict(CTX, registered_family_digest=digest)
    cert = m.ExtractionCoverageCertificate(frozenset({"a", "b"}), 2, "F", "z", "checker", "S", "e", UNIVERSE, digest)
    assert cert.validate(possible[:1], **ctx) == "CANNOT_CHECK_FAMILY_IDENTITY_DRIFT"
    assert replace(cert, candidates=frozenset({"outside"})).validate(possible, **ctx) == "INELIGIBLE_CANDIDATE"
    assert replace(cert, universe=None).validate(possible, **ctx) == "CANNOT_CHECK_UNREGISTERED_FINITE_FAMILY"
    assert cert.validate((frozenset({"outside"}),), **ctx) == "CANNOT_CHECK_MALFORMED_FINITE_FAMILY"


def test_certificate_freezes_nested_candidate_and_universe_sets():
    selected, universe = {"a"}, {"a", "b"}
    possible = (frozenset({"a"}),)
    digest = m.family_digest(universe,possible)
    cert = m.ExtractionCoverageCertificate(selected,2,"F","z","checker","S","e",universe,digest)
    selected.add("outside")
    universe.clear()
    assert cert.candidates == frozenset({"a"})
    assert cert.universe == frozenset({"a","b"})


def test_union_condition_is_iff_by_independent_exhaustive_selectors():
    atoms = ("a", "b", "c")
    subsets = tuple(frozenset(s) for size in range(4) for s in itertools.combinations(atoms, size))
    for mask in range(1 << len(subsets)):
        family = tuple(d for i, d in enumerate(subsets) if mask & (1 << i))
        for k in range(4):
            witness_exists = any(len(s) <= k and all(d <= s for d in family) for s in subsets)
            assert m.union_condition(family, k)[0] == witness_exists


@pytest.mark.parametrize("k", [True, -1, 0.5, float("nan"), "2"])
def test_invalid_capacity_is_rejected(k):
    with pytest.raises(ValueError):
        m.union_condition((frozenset({"a"}),), k)


def test_exhausted_or_unresolved_enumeration_is_not_absence():
    with pytest.raises(m.CannotCheck):
        m.deterministic_impossibility(40, 20)
    with pytest.raises(m.CannotCheck):
        m.union_condition(iter([frozenset({"a"})]), 2)


def test_cli_failure_and_cannot_check_exit_codes(monkeypatch, capsys):
    def fail():
        raise AssertionError("planted theorem failure")
    monkeypatch.setattr(m, "check_meg07", fail)
    assert m.main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FAIL"
    def cannot():
        raise m.CannotCheck("finite family unavailable")
    monkeypatch.setattr(m, "check_meg07", cannot)
    assert m.main() == 2
    assert json.loads(capsys.readouterr().out)["status"] == "CANNOT_CHECK"
    p = subprocess.run([sys.executable, "-O", str(MOD)], capture_output=True, text=True)
    assert p.returncode == 2
    assert json.loads(p.stdout)["status"] == "CANNOT_CHECK"
