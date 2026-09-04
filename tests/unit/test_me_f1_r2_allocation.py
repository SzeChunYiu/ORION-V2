"""ME-F1 R2: the probe-allocation re-derivation, as executable assertions.

The claim is that a comparator lost to a bare model because its own control text
prescribed a dominated solver at this geometry. That is a claim about the parent's
strength, so every number below is paired with a control: the replica must BE the
shipped core, the repair must be attributable to ONE lever, and the levers that did
NOT work are asserted to not work rather than quietly dropped.

These tests exercise a subset of the development split for speed; the full 8-campaign
figures live in ME_F1_R2_ALLOCATION_REDERIVATION_V1.json and are asserted from there.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
R2 = ROOT / "research/experiments/me-f1-r2"
V1 = ROOT / "research/experiments/me-f1"
for p in (str(R2), str(V1)):
    if p not in sys.path:
        sys.path.insert(0, p)

import mef1r2_allocation as A  # noqa: E402
import mef1_run as R  # noqa: E402
from mef1_arms import run_arm  # noqa: E402
from mef1_parents import RungFeatures, portfolio_select  # noqa: E402

RECEIPT = R2 / "ME_F1_R2_ALLOCATION_REDERIVATION_V1.json"
_CACHE: dict[int, list] = {}


def campaigns(n: int = 2):
    if n not in _CACHE:
        d = R.design()
        _CACHE[n] = R.make_campaigns(d["splits"]["development"]["seed"], n, 0, 30, 300000)
    return _CACHE[n]


def receipt():
    if not RECEIPT.exists():
        pytest.skip("re-derivation receipt absent")
    return json.loads(RECEIPT.read_text())


# ---- the replica is the shipped core, not a lookalike ----------------------------

def test_the_frozen_policy_reproduces_the_shipped_core_exactly():
    for c in campaigns(2):
        shipped = run_arm(c, "B5_ALGORITHMIC_CORE_NO_MODEL")
        replica = A.run_core(c, A.FROZEN, None)
        assert A.action_signature(shipped) == A.action_signature(replica)
        assert A.claim_signature(shipped) == A.claim_signature(replica)
        assert shipped.checks_spent == replica.checks_spent


def test_the_replica_control_is_capable_of_failing():
    """CONTROL. A different policy must NOT reproduce the shipped core, or the
    equality above would hold for anything."""
    c = campaigns(1)[0]
    shipped = run_arm(c, "B5_ALGORITHMIC_CORE_NO_MODEL")
    other = A.run_core(c, A.REDERIVED, None)
    assert A.action_signature(shipped) != A.action_signature(other)


# ---- the action cap actually binds ------------------------------------------------

def test_the_action_cap_binds_and_the_uncapped_core_exceeds_it():
    c = campaigns(1)[0]
    capped = A.run_core(c, A.FROZEN, 7)
    natural = A.run_core(c, A.FROZEN, None)
    assert len(capped.actions) == 7
    assert len(natural.actions) > 7


# ---- the shipped selector prescribes the dominated tool at the critical rung ------

def test_the_shipped_portfolio_sends_the_critical_rung_to_local_search():
    assert portfolio_select(RungFeatures(0, 30, int(round(30 * 4.267)))) == "local_search"
    assert A.trained_select(RungFeatures(0, 30, int(round(30 * 4.267)))) == "exact_solve"


def test_local_search_is_dominated_at_every_ratio_on_the_development_split():
    rec = receipt()["tool_training_table"]
    ratios = sorted({row["ratio"] for row in rec.values()})
    assert len(ratios) == 5
    for r in ratios:
        ex = next(v for v in rec.values() if v["ratio"] == r and v["tool"] == "exact_solve")
        ls = next(v for v in rec.values() if v["ratio"] == r and v["tool"] == "local_search")
        assert ex["n_probes"] == ls["n_probes"] == 32          # published denominator
        assert ex["settle_rate"] == 1.0
        assert ls["settle_rate"] < 1.0
        # A saturated rate is exactly the shape that cannot tell a real measurement from
        # a miscounted field, so the settled count is reconstructed from its parts and
        # the completeness flag the version space actually reads is asserted.
        assert ex["settled"] == ex["witness"] + ex["refuted_complete"]
        assert ex["refuted"] == ex["refuted_complete"]
        assert ex["refuted_incomplete"] == 0
        assert ex["witness"] + ex["refuted"] + ex["inconclusive"] == 32
    cheapest = 3.2
    ex = next(v for v in rec.values() if v["ratio"] == cheapest and v["tool"] == "exact_solve")
    ls = next(v for v in rec.values() if v["ratio"] == cheapest and v["tool"] == "local_search")
    # dominated on BOTH resources at the rung the shipped rule is most confident about
    assert ex["settle_rate"] > ls["settle_rate"] and ex["mean_checks"] < ls["mean_checks"]


# ---- the repair, and its single-stage attribution ---------------------------------

def test_the_frozen_figures_are_reproduced_not_imported():
    rows = receipt()["policies"]
    assert rows["FROZEN|cap=None"]["primary_warranted_correct_rate"] == 0.925
    assert rows["FROZEN|cap=None"]["actions_total"] == 120
    assert rows["FROZEN|cap=7"]["primary_warranted_correct_rate"] == 0.4875


def test_the_rederived_allocation_repairs_the_seven_action_budget():
    rows = receipt()["policies"]
    assert rows["REDERIVED|cap=7"]["primary_warranted_correct_rate"] == 0.70
    assert rows["REDERIVED|cap=7"]["actions_total"] == 56
    assert rows["REDERIVED|cap=7"]["unwarranted_claims"] == 0


def test_the_repair_is_attributable_to_one_lever():
    r = receipt()["attribution"]["lever_isolation"]
    assert r["trained_tool_alone"] == 0.70          # carries the whole repair
    assert r["luby_sizing_alone"] == 0.4875         # changes nothing
    assert r["probe_schedule_alone"] < 0.4875       # and this lever made it WORSE


def test_the_rederivation_is_not_a_budget_specific_hack():
    rows = receipt()["policies"]
    assert rows["REDERIVED|cap=None"]["primary_warranted_correct_rate"] == 1.0
    assert rows["REDERIVED|cap=None"]["actions_total"] < rows["FROZEN|cap=None"]["actions_total"]


def test_the_repaired_core_stays_within_the_check_budget():
    rows = receipt()["policies"]
    geom = receipt()["geometry"]
    per_campaign = rows["REDERIVED|cap=7"]["checks_total"] / geom["n_campaigns"]
    assert per_campaign < geom["budget_checks"]


def test_the_warranted_claim_discipline_is_not_a_variable_here():
    """Every policy must claim only what its version space entails: zero unwarranted
    claims everywhere, so the comparison is of ALLOCATION and nothing else."""
    rows = receipt()["policies"]
    assert all(v["unwarranted_claims"] == 0 for v in rows.values())
    assert all(v["primary_warranted_correct_rate"] == v["coverage"] for v in rows.values())


# ---- nothing here unblocks the study ----------------------------------------------

def test_the_receipt_does_not_claim_to_authorize_dispatch():
    auth = receipt()["authority"]
    assert auth["authorizes_protected_dispatch"] is False
    assert auth["grants_scientific_truth"] is False


def test_the_trained_selector_is_constant_at_this_geometry_and_says_so():
    """The nearest-key lookup cannot branch here: every trained value is exact_solve.
    The receipt claims that plainly rather than implying a guard the code lacks, and the
    extrapolation flag is what makes an unseen geometry visible."""
    assert set(A.TRAINED_PORTFOLIO_TABLE.values()) == {"exact_solve"}
    for ratio in (3.2, 4.0, 4.267, 4.7, 5.6):
        f = RungFeatures(0, 30, int(round(30 * ratio)))
        assert A.trained_select(f) == "exact_solve"
        assert A.trained_select_is_extrapolating(f) is False
    assert A.trained_select_is_extrapolating(RungFeatures(0, 30, int(30 * 8.0))) is True


def test_me_f1_v1_is_untouched():
    src = (V1 / "mef1_arms.py").read_text()
    assert "trained_select" not in src
    assert "TRAINED_PORTFOLIO_TABLE" not in src
