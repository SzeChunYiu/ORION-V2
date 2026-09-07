"""FM80 §9 amendment V2: the registered routing table must fire on every row AND stay silent on a
healthy instrument, the witness screen must reject a constant witness, and the frozen design's
sha256 must match its markdown twin so the freeze cannot drift from the document it names."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "research" / "experiments" / "fm80-exec"
P = BASE / "fm80_s9_v2.py"
spec = importlib.util.spec_from_file_location("fm80_s9_v2", P)
M = importlib.util.module_from_spec(spec)
sys.modules["fm80_s9_v2"] = M
spec.loader.exec_module(M)


def test_selftest_passes() -> None:
    assert M._self_test() == 0


@pytest.mark.parametrize(
    "acc0,acc1,maj,row",
    [(0.95, 0.30, 0.60, 1), (0.90, 0.10, 0.50, 1), (0.05, 0.08, 0.02, 2),
     (0.60, 0.55, 0.64, 3), (0.85, 0.40, 0.60, 4), (0.72, 0.55, 0.64, 5)],
)
def test_every_row_is_reachable(acc0: float, acc1: float, maj: float, row: int) -> None:
    assert M.route_domain(acc0, acc1, maj)["row"] == row


def test_no_alarm_healthy_instrument_proceeds_and_counts() -> None:
    r = M.route_domain(0.75, 0.68, 0.64)
    assert r["disposition"] == M.PROCEED_ROW
    assert r["counts_toward_section_9"] is True


def test_ceiling_threshold_is_derived_from_the_10pp_bar() -> None:
    # s9.1 needs A3 >= best + 0.10 and accuracy <= 1.00, so 0.90 is where the clause dies.
    assert M.CEILING == 0.90
    assert M.route_domain(0.8999, 0.10, 0.50)["row"] != 1
    assert M.route_domain(0.9000, 0.10, 0.50)["row"] == 1


def test_out_of_range_refuses_rather_than_reporting_a_row() -> None:
    with pytest.raises(ValueError):
        M.route_domain(1.5, 0.5, 0.5)
    with pytest.raises(ValueError):
        M.route_domain(0.5, 0.5, -0.1)


def test_witness_screen_rejects_constant_and_accepts_a_real_split() -> None:
    assert M.witness_screen(["PASS"] * 50)["status"] == M.DEGENERATE
    assert M.witness_screen(["PASS"] * 36 + ["FAIL"] * 64)["status"] == "NON_DEGENERATE"
    assert M.witness_screen([])["status"] == "CANNOT_CHECK"


def test_programme_terminal_needs_three_counting_domains() -> None:
    two = {"a": {"counts_toward_section_9": True}, "b": {"counts_toward_section_9": True},
           "c": {"counts_toward_section_9": False}}
    assert M.programme_terminal(two)["terminal"] == M.PROGRAMME_NO_RANGE
    assert "silent, not exculpatory" in M.programme_terminal(two)["reading"]
    three = {k: {"counts_toward_section_9": True} for k in "abc"}
    assert M.programme_terminal(three)["terminal"] == "PROCEED_TO_STAGE_A"


def test_frozen_design_json_matches_its_markdown_twin() -> None:
    obj = json.loads((BASE / "FM80_SECTION_9_EXECUTION_AMENDMENT_V2.json").read_text())
    md = BASE / "FM80_SECTION_9_EXECUTION_AMENDMENT_V2.md"
    assert obj["markdown_twin"]["sha256"] == hashlib.sha256(md.read_bytes()).hexdigest()
    assert obj["repair_branch"]["selected"] == "BRANCH_1__RAISE_SAMPLE_FLOOR"
    assert obj["repair_branch"]["sample_floor_per_domain"] == M.BAR_PER_DOMAIN == 61
    assert obj["repair_branch"]["effect_bar_pp"] == 10.0
    assert obj["authority"]["alters_submission_authorized"] is False
    assert obj["seed_commitment"]["sha256"] and len(obj["seed_commitment"]["sha256"]) == 64
    assert len(obj["domains"]["counting"]) == 3


def test_reserve_draw_is_deterministic_and_seed_sensitive() -> None:
    ids = [f"C-{i}" for i in range(200)]
    assert M.draw_reserve("s1", ids, 30) == M.draw_reserve("s1", ids, 30)
    assert M.draw_reserve("s1", ids, 30) != M.draw_reserve("s2", ids, 30)
