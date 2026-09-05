"""Independent regression cases for batch-six claims outside its planted fixtures."""
import importlib.util
import random
from fractions import Fraction
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def theory():
    path = Path(__file__).resolve().parents[2] / "research/machine-epistemics-theory/kso_lifetime_prereqs_batch6_exact.py"
    spec = importlib.util.spec_from_file_location("lifetime_revision_boundaries", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_adoption_must_extend_actual_component_predecessor(theory):
    m = theory.build_machine(random.Random(7), "continuity")
    before = theory.identity_of(m["active"], m["components"])
    m["active"].append({"kind": "ADOPT", "component": "operator", "prev": "unrelated", "fp": "v3"})
    assert theory.same_machine(before, m["active"], {**m["components"], "operator": "v3"}) == (False, "ADOPTION_PREDECESSOR_MISMATCH")


def test_commitment_head_must_be_on_the_claimed_chain(theory):
    m = theory.build_machine(random.Random(8), "head")
    before = theory.identity_of(m["active"], m["components"])
    ev = m["active"].evidence()
    claim = {"head": "0" * 64, "cites": list(ev)[:1]}
    assert not theory.attributable(claim, before, m["active"], ev)


def test_new_evidence_is_not_pre_restart_evidence(theory):
    m = theory.build_machine(random.Random(9), "evidence")
    before = theory.identity_of(m["active"], m["components"])
    ev = m["active"].evidence()
    m["active"].append({"kind": "ADMIT", "eid": "new", "payload": "new"})
    claim = theory.commit_after(m, ["new"])
    assert theory.attributable(claim, before, m["active"], ev) is False


def test_one_lucky_guess_does_not_prove_an_undeclared_channel(theory):
    assert len(theory.version_space([((0, 0), 0), ((0, 1), 0)])) == 4
    assert theory.arm_label({"INSTRUCTION": 2}, 2) == "IDENTIFICATION_NOT_ESTABLISHED"
    assert theory.arm_label({"INSTRUCTION": 2}, 2, guaranteed_identification=True) == "BELOW_LOWER_BOUND_UNDECLARED_CHANNEL"


def test_bidirectional_decision_controls_both_tails(theory):
    assert theory.paired_decision(5, 0) == "DESCRIPTIVE"
    assert theory.paired_decision(0, 5) == "DESCRIPTIVE"
    assert theory.paired_decision(6, 0) == "RESIDUAL_SUPPORTED"
    assert theory.paired_decision(0, 6) == "PARENT_DOMINATES"
    for n in range(1, 15):
        size = sum((theory.binom_pmf(n, w, Fraction(1, 2)) for w in range(n + 1)
                    if theory.paired_decision(w, n - w) != "DESCRIPTIVE"), Fraction(0))
        assert size <= theory.ALPHA


@pytest.mark.parametrize("n,block", [(0, 1), (3, 0), (7, 2), (True, 1)])
def test_block_model_rejects_undefined_inputs(theory, n, block):
    with pytest.raises(theory.CannotCheck):
        theory.size_under_block_dependence(n, block)


def test_no_rejection_region_is_zero_size(theory):
    assert theory.size_under_block_dependence(3, 3) == 0


def test_empty_observation_does_not_manufacture_one_lifetime(theory):
    assert theory.lifetime_design([], distinct_streams=False) == (0, "CANNOT_CHECK")


def test_shared_evidence_grade_is_not_a_scalar_semiring_homomorphism(theory):
    p = theory.cert({"e"})[0]
    assert theory.meet(p, p) == p
    g = {"e": Fraction(1, 2)}
    v = theory.graded_value_recompute(p, g, frozenset())
    assert theory.graded_value_recompute(theory.meet(p, p), g, frozenset()) == v != v * v


def test_declared_side_information_is_counted(theory):
    assert theory.arm_label({"INSTRUCTION": 2, "CERTIFICATE": 2}, 2, guaranteed_identification=True) == "CONSISTENT_WITH_MATCHED"


def test_non_power_of_two_capacity_rounds_up(theory):
    assert theory.unmeasured_bits_lower_bound(0, class_size=3) == 2


def test_reference_is_not_a_performance_upper_bound(theory):
    assert "upper reference" not in theory.comparison_report((6, 0), (0, 6), "REFERENCE")["reference"]["reading"]


def test_assertion_disabled_checker_cannot_claim_pass(theory):
    import subprocess
    import sys
    r = subprocess.run([sys.executable, "-O", theory.__file__], capture_output=True, text=True)
    assert r.returncode == 2 and "CANNOT_CHECK" in r.stdout
