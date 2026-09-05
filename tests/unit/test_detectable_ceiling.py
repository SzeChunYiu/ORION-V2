"""Every contrast must report the difference it could have detected.

`mcnemar_mde` existed from the start and was called nowhere, so no rollup carried a ceiling and
"no difference" was unfalsifiable by a reader. These tests pin the wiring and both regimes.
"""
import importlib.util
import math
import sys
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parents[2] / "research/llm-machine-epistemics/pra_real_llm_audit.py"
_spec = importlib.util.spec_from_file_location("pra_ceiling_test", _SRC)
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)


def test_every_contrast_reports_a_ceiling():
    """The regression that matters: the field must be present on every mcnemar result."""
    for pairs in ([(True, True)] * 10,
                  [(True, False)] * 5 + [(False, True)] * 3 + [(True, True)] * 12,
                  [(False, False)] * 7):
        assert "detectable_ceiling" in _mod.mcnemar(pairs)


@pytest.mark.parametrize("n,expected", [(240, 0.015253), (120, 0.030273), (480, 0.007656)])
def test_zero_discordance_uses_the_exact_bound(n, expected):
    r = _mod.mcnemar([(True, True)] * n)["detectable_ceiling"]
    assert r["method"] == "clopper_pearson_upper_0_of_n"
    assert r["bound"] == pytest.approx(expected, abs=5e-7)
    assert r["bound"] == pytest.approx(1.0 - 0.025 ** (1.0 / n), rel=0, abs=0)


def test_flagship_published_case_reproduces():
    """0 of 480 -> 0.0077, the value the FLAGSHIP Article already reports for its own case."""
    assert round(_mod.mcnemar([(True, True)] * 480)["detectable_ceiling"]["bound"], 4) == 0.0077


def test_nonzero_discordance_uses_the_mde_branch():
    pairs = [(True, False)] * 20 + [(False, True)] * 10 + [(True, True)] * 210
    r = _mod.mcnemar(pairs)["detectable_ceiling"]
    assert r["method"] == "mcnemar_mde_normal_approx"
    assert math.isfinite(r["bound"]) and 0.0 < r["bound"] <= 1.0


def test_the_bound_tightens_as_the_design_grows():
    """A larger zero-discordance control must bound a smaller difference, or the ceiling is useless."""
    bounds = [_mod.mcnemar([(True, True)] * n)["detectable_ceiling"]["bound"]
              for n in (60, 120, 240, 480, 1440)]
    assert all(a > b for a, b in zip(bounds, bounds[1:])), bounds


def test_mde_alone_would_not_have_covered_the_zero_case():
    """Why the exact branch exists: the pre-existing function returns nan at zero discordance."""
    assert math.isnan(_mod.mcnemar_mde(240, 0.0))
