from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
MOD = HERE / "research" / "machine-epistemics-theory" / "meg_foundation_batch2_exact.py"
spec = importlib.util.spec_from_file_location("meg_foundation_batch2_exact", MOD)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_meg02_truth_vs_actionability_and_drift():
    r = m.check_meg02()
    assert r["truth_status"] == m.UNKNOWN
    assert r["risk_gate"] == "ALLOW"
    assert r["marginal_coverage"] == "9/10"
    assert r["conditional_coverage_at_b"] == 0
    assert r["identity_drift_caught"] == 1


def test_meg03_epoch_and_supersession():
    r = m.check_meg03()
    assert r["scope_associativity_checks"] == 125
    assert r["cross_epoch_partition_rejected"] == 1
    assert r["supersession_impact"] == ["old", "plan"]


def test_meg16_nogood_corrected_law():
    r = m.check_meg16()
    assert r["profiles"] == 20
    assert r["atlas_meet_homomorphism_refuted"] == 1
    assert r["strict_meet_counterexamples"] > 0
    assert r["constraint_kills_joint_composite"] == 1


def test_meg17_relearn_is_lifecycle_distinct_and_local():
    r = m.check_meg17()
    assert r["reinstate_exact"] == 1
    assert r["relearn_current_behavior_equal"] == 1
    assert r["relearn_lifecycle_profile_differs"] == 1
    assert r["local_work"] < r["global_rederive_mutant_work"]


def test_meg20_sufficiency_certificate_hostiles():
    r = m.check_meg20()
    assert r == {
        "valid_certificate": "CERTIFIED",
        "pushforward_fixed_point_equal": 1,
        "nonlumpable_mutant_refused": 1,
        "nonmeasurable_warrant_refused": 1,
        "answer_not_factoring_refused": 1,
    }


def test_cli_passes_and_reports_non_novelty():
    p = subprocess.run([sys.executable, str(MOD)], text=True, capture_output=True, check=False)
    assert p.returncode == 0, p.stderr + p.stdout
    data = json.loads(p.stdout)
    assert data["status"] == "PASS"
    assert data["result"]["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"


def test_cannot_check_is_distinct_exit_2(monkeypatch):
    monkeypatch.setattr(m, "run_all", lambda: (_ for _ in ()).throw(m.CannotCheck("fixture")))
    assert m.main() == 2
