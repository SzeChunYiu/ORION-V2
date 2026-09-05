from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "research" / "machine-epistemics-theory" / "field_dynamics_v1" / "field_dynamics_exact.py"
spec = importlib.util.spec_from_file_location("field_dynamics_exact", MOD)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_fd01_authority():
    r = m.check_fd01()
    assert r["authority_pair_checks"] == 6561
    assert r["max_mutant_caught"] == 1


def test_fd02_warrant_source():
    r = m.check_fd02()
    assert r["cross_nogood_blocks_joint"] == 1
    assert r["score_does_not_mint_truth"] == 1


def test_fd03_local_revision():
    r = m.check_fd03()
    assert set(r["impact"]) == {"e", "a", "b", "c"}
    assert r["one_hop_mutant_caught"] == 1


def test_fd04_exact_perturbation_bound():
    r = m.check_fd04()
    assert r["kernel_seed_pair_checks"] == 20736
    assert r["kernels"] == 36
    assert r["seeds"] == 4


def test_fd05_lifecycle_hysteresis():
    r = m.check_fd05()
    assert r["same_identity_semantic_reinstatement"] == 1
    assert r["relearn_behavior_equal_lineage_distinct"] == 1


def test_fd06_parent_safety_kernel():
    r = m.check_fd06()
    assert r["kernel"] == [3]
    assert r["parent_disposition"] == "PARENT_SUFFICIENT"


def test_fd08_projection_gates():
    r = m.check_fd08()
    assert r["nonlumpable_mutant_caught"] == 1
    assert r["warrant_measurability_independent_gate"] == 1


def test_fd09_fd10_nonlaundering_and_self():
    assert m.check_fd09()["ten_speakers_do_not_mint_truth"] == 1
    assert m.check_fd10()["self_cannot_raise_commit"] == 1


def test_fd11_resource_fixture():
    assert m.check_fd11()["no_free_representation_fixture"] == 1


def test_fd12_typed_terminal():
    r = m.check_fd12()
    assert r["status_vectors"] == 4096
    assert r["ignore_cannot_check_mutant_caught"] == 1


def test_cli_and_open_research_preserved():
    p = subprocess.run([sys.executable, str(MOD)], capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stdout + p.stderr
    d = json.loads(p.stdout)
    assert d["status"] == "PASS"
    assert d["result"]["FD-07"]["status"] == "OPEN_RESEARCH"
    assert d["result"]["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"
    assert d["result"]["FIELD_STATUS"] == "NOT_ESTABLISHED"
