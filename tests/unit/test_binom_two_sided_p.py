"""Exactness of the McNemar two-sided p on discordant pairs.

Regression test for the 2026-09-05 defect: an absolute float tolerance in the
"at least as extreme" comparison made the p value saturate near 1e-15 once the
point mass fell below it, so p barely moved as the discordant count grew.
"""
import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parents[2] / "research/llm-machine-epistemics/pra_real_llm_audit.py"
_spec = importlib.util.spec_from_file_location("pra_real_llm_audit_for_test", _SRC)
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)
binom_two_sided_p = _mod.binom_two_sided_p


def _exact(k: int, n: int) -> float:
    pk = math.comb(n, k)
    total = sum(math.comb(n, i) for i in range(n + 1) if math.comb(n, i) <= pk)
    return float(Fraction(total, 2 ** n))


@pytest.mark.parametrize("k,n", [(0, 1), (0, 60), (0, 82), (0, 119), (0, 120),
                                 (0, 180), (0, 182), (0, 221), (0, 239),
                                 (1, 10), (3, 20), (5, 10), (7, 15)])
def test_matches_exact_integer_computation(k, n):
    assert binom_two_sided_p(k, n) == _exact(k, n)


def test_textbook_values():
    assert binom_two_sided_p(1, 10) == pytest.approx(0.021484375, rel=0, abs=0)
    assert binom_two_sided_p(5, 10) == 1.0
    assert binom_two_sided_p(0, 0) == 1.0


def test_p_falls_as_evidence_grows():
    """The defect's signature: p was nearly constant in n. It must now fall monotonically."""
    ps = [binom_two_sided_p(0, n) for n in (60, 82, 120, 180, 221)]
    assert all(a > b for a, b in zip(ps, ps[1:])), ps
    assert ps[-1] < 1e-60, ps[-1]


def test_planted_defect_is_caught():
    """The old tolerant form must fail this suite -- proving the test can fail."""
    def old(k: int, n: int) -> float:
        if n == 0:
            return 1.0
        pk = math.comb(n, k) / 2 ** n
        tot = sum(math.comb(n, i) for i in range(n + 1)
                  if math.comb(n, i) / 2 ** n <= pk + 1e-15) / 2 ** n
        return min(1.0, tot)
    assert old(0, 221) != _exact(0, 221)
    assert old(0, 221) > 1e-16          # saturates
    assert _exact(0, 221) < 1e-60       # the truth
