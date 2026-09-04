"""H-EXT-1P pre-freeze audit: the load-bearing facts as executable assertions.

The receipt built on this script makes two claims that decide whether H-EXT-1P is worth
running at all.  Both are asserted here, and each is paired with a control that must
fail when the fact is removed, so neither can pass vacuously.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from h_ext1p_estimand_audit import (  # noqa: E402
    FROZEN_CONTROL_PROSPECTIVE,
    GATE_FREEZE,
    TABLES,
    audit,
    control_check,
    critical_k,
    mcnemar_exact_two_sided,
    paired_table,
    power_exact,
    reconstruct,
)

GRID = (520, 1200)


def _rows():
    if not GATE_FREEZE.exists() or not TABLES["PROSPECTIVE"].exists():
        pytest.skip("frozen H-EXT-1 artifacts absent")
    gate_id = json.loads(GATE_FREEZE.read_text())["selected_gate"]
    table = json.loads(TABLES["PROSPECTIVE"].read_text())
    return reconstruct(table, gate_id)


# ---- the reconstruction is the frozen study's, not a lookalike -------------------

def test_reconstruction_reproduces_the_six_frozen_published_control_numbers():
    ok, got = control_check(_rows())
    assert ok, f"expected {FROZEN_CONTROL_PROSPECTIVE}, got {got}"


def test_the_control_check_can_fail():
    """A wrong routing rule must be caught, or the check above proves nothing."""
    rows = deepcopy(_rows())
    for r in rows:                      # GATED := always-on M, the wrong rule
        r["gated"] = r["m"]
    ok, got = control_check(rows)
    assert not ok
    assert got["gated_correct"] == FROZEN_CONTROL_PROSPECTIVE["m_correct"]


# ---- finding 1: the mechanism-attributable estimand is a ceiling tie -------------

def test_gate_active_subset_is_a_ceiling_tie_with_zero_discordant_pairs():
    rows = _rows()
    a = audit("PROSPECTIVE", rows, GRID)["paired_GATED_vs_PARENT"]["GATE_ACTIVE"]
    assert a["n"] == 170
    assert a["gated_correct"] == a["other_correct"] == a["n"] == 170
    assert a["gated_only_b"] == 0 and a["other_only_c"] == 0
    assert a["discordant"] == 0


def test_every_discordant_pair_lies_where_the_gate_never_fires():
    p = audit("PROSPECTIVE", _rows(), GRID)["paired_GATED_vs_PARENT"]
    assert p["SUITE"]["discordant"] == 29
    assert p["GATE_INACTIVE"]["discordant"] == p["SUITE"]["discordant"]
    assert p["GATE_ACTIVE"]["discordant"] == 0
    # and the whole net margin, to within the single PDS1D task, is one study family
    assert p["BY_STUDY"]["PD-S2-ARGUMENT-AND-ADEQUACY"]["discordant"] == 28
    assert p["BY_STUDY"]["PD-S2-ARGUMENT-AND-ADEQUACY"]["gate_activations"] == 0


def test_the_gate_active_decomposition_would_report_discordance_if_any_existed():
    """CONTROL for the two tests above: a zero must be a measurement, not an empty slot."""
    rows = deepcopy(_rows())
    flipped = 0
    for r in rows:
        if r["gate_active"] and flipped < 7:
            r["parent"] = not r["parent"]
            flipped += 1
    assert flipped == 7
    a = audit("PROSPECTIVE", rows, GRID)["paired_GATED_vs_PARENT"]["GATE_ACTIVE"]
    assert a["gated_only_b"] == 7 and a["other_only_c"] == 0
    assert a["exact_mcnemar_two_sided_p"] < 0.05


# ---- finding 2: the suite estimand is measurable, and underpowered at n = 520 ----

def test_suite_estimand_matches_the_frozen_receipt_margin_and_is_not_significant():
    s = audit("PROSPECTIVE", _rows(), GRID)["paired_GATED_vs_PARENT"]["SUITE"]
    assert (s["gated_correct"], s["other_correct"]) == (508, 497)
    assert (s["gated_only_b"], s["other_only_c"]) == (20, 9)
    assert round(s["margin_pp"], 1) == 2.1
    assert s["exact_mcnemar_two_sided_p"] == pytest.approx(0.061428, abs=1e-5)


def test_a_naive_repeat_at_the_frozen_n_is_a_coin_flip_but_n_1200_is_not():
    pb, pc = 20 / 520, 9 / 520
    assert power_exact(520, pb, pc) == pytest.approx(0.4605, abs=2e-3)
    assert power_exact(1200, pb, pc) > 0.80


# ---- the statistics themselves, with their own no-alarm controls ----------------

def test_exact_mcnemar_known_values():
    assert mcnemar_exact_two_sided(0, 0) == 1.0
    assert mcnemar_exact_two_sided(6, 0) == pytest.approx(2 / 64)
    assert mcnemar_exact_two_sided(20, 9) == pytest.approx(0.061428, abs=1e-5)
    assert mcnemar_exact_two_sided(20, 5) < 0.05


def test_five_discordant_pairs_can_never_reject_however_they_fall():
    assert critical_k(5, 0.05) == -1
    assert critical_k(6, 0.05) == 0
    assert power_exact(1000, 0.0, 0.0) == 0.0


def test_power_is_calibrated_under_the_null_and_saturates_under_a_large_effect():
    assert power_exact(520, 0.03, 0.03) <= 0.05      # size, not power
    assert power_exact(520, 0.10, 0.01) > 0.99


def test_paired_table_partitions_its_denominator():
    t = paired_table([True, True, False, False], [True, False, True, False])
    assert t["both"] + t["gated_only_b"] + t["other_only_c"] + t["neither"] == t["n"] == 4
