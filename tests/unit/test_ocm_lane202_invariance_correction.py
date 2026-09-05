"""Independent scoped checks of directional compiler bounds, not old outcomes."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import sys
import pytest

PATH = Path(__file__).resolve().parents[2] / "research/orion-machine/reference/ocm_lane202_invariance_correction_exact.py"
SPEC = importlib.util.spec_from_file_location("lane202_invariance_correction", PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)


def test_actual_programs_refute_absolute_bound_despite_mutual_linear_compilation():
    programs = ("000000000", "11000")  # both output eight zeros
    assert m.run("A", programs[0]) == m.Run("0"*8, 9, 17)
    assert m.run("A", programs[1]) == m.Run("0"*8, 5, 29)
    assert m.run("B", programs[1]) == m.Run("0"*8, 5, 13)
    assert m.compiler_contract("A", "B", programs, programs, length_overhead=0, time_factor=3)
    assert m.compiler_contract("B", "A", programs, programs, length_overhead=0, time_factor=3)
    assert m.minimum_bits("A", 8, 17) == 9
    assert m.minimum_bits("B", 8, 51) == 5
    assert abs(9-5) > 0  # declared compiler description overhead is exactly zero


def test_reverse_compilation_needs_its_own_time_budget():
    # B's five-bit program cannot meet A's original 17-tick budget.
    assert m.run("A", "11000").ticks > 17
    # The reverse compiler has the registered 3*51 budget, not 17.
    assert m.minimum_bits("A", 8, 3*51) <= m.minimum_bits("B", 8, 51)


@pytest.mark.parametrize("constant", range(6))
def test_gap_family_outgrows_each_registered_description_constant(constant):
    n = 2**(constant+2)
    assert n <= 128
    gap = m.minimum_bits("A", n, 2*n+1) - m.minimum_bits("B", n, 3*(2*n+1))
    assert gap == n-n.bit_length() and gap > constant


def test_unavailable_bound_is_not_zero_cost():
    assert m.minimum_bits("A", 8, 0) is None


def test_actual_compiler_mutation_is_detected():
    assert m.run("A", "110").output != m.run("B", "111").output
    assert not m.compiler_contract("A", "B", ("110",), ("111",), length_overhead=0, time_factor=3)
    assert not m.compiler_contract("B", "A", ("11",), ("11",), length_overhead=0, time_factor=1)


@pytest.mark.parametrize("call", [
    lambda: m.run("UNKNOWN", "11"),
    lambda: m.run("A", "100"),  # noncanonical length
    lambda: m.run("A", "111111111"),  # 255 output bits exceed cap
    lambda: m.minimum_bits("A", True, 2),
    lambda: m.minimum_bits("A", 8, False),
    lambda: m.compiler_contract("A", "B", iter(["11"]), ("11",), length_overhead=0, time_factor=3),
    lambda: m.compiler_contract("A", "B", (), (), length_overhead=0, time_factor=3),
    lambda: m.compiler_contract("A", "B", ("11",), ("11",), length_overhead=0, time_factor=0),
])
def test_outside_model_is_explicit_cannot_check(call):
    with pytest.raises(m.CannotCheck):
        call()


def test_calibration_counts_derive_from_actual_enumeration_and_cli(capsys):
    result = m.calibrate()
    assert result["directional_program_checks"] == 512
    assert result["absolute_bound_zero_overhead_violations"] == 126
    assert result["largest_registered_witness"]["gap"] == 120
    assert m.main(["--n-max", "129"]) == 2
    assert "CANNOT_CHECK" in capsys.readouterr().out

