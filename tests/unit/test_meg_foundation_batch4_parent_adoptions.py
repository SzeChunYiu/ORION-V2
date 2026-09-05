from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "research" / "machine-epistemics-theory" / "meg_foundation_batch4_parent_adoptions_exact.py"
spec = importlib.util.spec_from_file_location("meg_foundation_batch4_parent_adoptions_exact", MOD)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_meg14_teaching_and_membership_query_resources_differ():
    r = m.check_meg14()
    assert r["teaching_dimension"] == 1
    assert r["membership_query_complexity"] == 2
    assert r["td_equals_mq_refuted"] == 1


def test_meg32_nonrejection_is_not_equivalence():
    r = m.check_meg32()
    assert r["ordinary_p_nonrejection_not_equivalence"] == 1
    assert r["missing_margin_or_interval_is_cannot_check"] == 1
    assert r["p_gt_alpha_mutant_caught"] == 1


def test_equivalence_requires_registered_interval_and_margin():
    assert m.equivalence_decision(margin=0.1, ci=(-0.05, 0.05), method_id="paired-exact-v1") == "EQUIVALENT"
    assert m.equivalence_decision(margin=0.1, ci=(-0.2, 0.01), method_id="paired-exact-v1") == "NOT_EQUIVALENT_OR_INCONCLUSIVE"
    assert m.equivalence_decision(margin=0.1, ci=(-0.05, 0.05), method_id=None) == "CANNOT_CHECK"


def test_cli_preserves_non_novelty():
    p = subprocess.run([sys.executable, str(MOD)], capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stdout + p.stderr
    d = json.loads(p.stdout)
    assert d["status"] == "PASS"
    assert d["result"]["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"
