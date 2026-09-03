"""ME-F1 frontier open-discovery study: unit tests for the frozen modules and every
runner stage that can be exercised without a model call.

Everything here runs on TINY development-scale campaigns (<= 12 variables, <= 20 000
checks, 2 blocks) and NEVER touches the model channel: the model arms are driven through
an injected ``call_fn`` that returns a canned ``mef1_channel.CallReceipt``.  Nothing in
this file is protected evidence, and the protected stage is only ever exercised through
its refusal path.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEF1 = ROOT / "research" / "experiments" / "me-f1"
# The me-f1 modules import each other by bare name, so the study directory has to be on
# sys.path before any of them is loaded.
if str(MEF1) not in sys.path:
    sys.path.insert(0, str(MEF1))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, MEF1 / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mef1_model = _load("mef1_model")
mef1_generator = _load("mef1_generator")
mef1_toolbox = _load("mef1_toolbox")
mef1_reference = _load("mef1_reference")
mef1_parents = _load("mef1_parents")
mef1_channel = _load("mef1_channel")
mef1_arms = _load("mef1_arms")
mef1_score = _load("mef1_score")
mef1_stats = _load("mef1_stats")
mef1_run = _load("mef1_run")

Action = mef1_model.Action
ActionResult = mef1_model.ActionResult
Claim = mef1_model.Claim
CampaignRecord = mef1_model.CampaignRecord

N_VARS = 12
BUDGET = 20_000
N_BLOCKS = 2
MODES = ("none", "unit_pure", "subsumption", "symmetry")


def tiny(index: int = 0, family: str = "F_CRITICAL"):
    """A development-scale campaign: two independent sub-ladders over 12 variables."""
    return mef1_generator.make_campaign("ME-F1-UNIT", index, family, N_VARS, BUDGET, 8,
                                        n_blocks=N_BLOCKS)


def tiny_ground_truth(campaign) -> dict[int, str]:
    """Reference statuses at a small K -- 12 variables are exhaustible in milliseconds."""
    block_of = {r.index: r.block for r in campaign.rungs}
    truths = mef1_reference.monotone_repair(
        mef1_reference.ground_truth(campaign, 2, 50_000), block_of)
    return {t.rung: t.status for t in truths}


def block_of(campaign) -> dict[int, int]:
    return {r.index: r.block for r in campaign.rungs}


# =====================================================================================
# parents
# =====================================================================================


def test_every_parent_passes_its_native_known_answer_tests() -> None:
    passed, total, failures = mef1_parents.fidelity_selftests()
    assert failures == [], failures
    assert passed == total > 0


# =====================================================================================
# warrant validity (G0a)
# =====================================================================================


@pytest.mark.parametrize("fixture", mef1_run.warrant_validity_fixtures(),
                         ids=lambda f: f["name"])
def test_every_hand_authored_warrant_fixture_gets_its_registered_answer(fixture) -> None:
    valid, reason = mef1_model.warrant_is_valid(
        fixture["claim"], fixture["record"], fixture["block_of"])
    assert bool(valid) is fixture["expected_valid"], (fixture["name"], reason)


def test_the_fixture_set_covers_both_licensed_and_forbidden_inferences() -> None:
    kinds = {f["kind"] for f in mef1_run.warrant_validity_fixtures()}
    assert kinds == {"LICENSED", "FORBIDDEN"}
    names = {f["name"] for f in mef1_run.warrant_validity_fixtures()}
    # the five inferences the world explicitly forbids, each present by name
    assert "failure_to_find_is_not_a_refutation" in names
    assert "witness_generalised_upward_named" in names
    assert "refutation_generalised_downward_named" in names
    assert "closure_across_blocks_satisfiable_named" in names
    assert "unresolved_with_a_non_none_warrant" in names


def test_failing_to_find_a_witness_never_licenses_unsatisfiable() -> None:
    rec = mef1_run._fixture_record(inconclusive=(2,))
    for warrant in ("COMPLETED_REFUTATION", "MONOTONE_CLOSURE", "NONE"):
        valid, _ = mef1_model.warrant_is_valid(
            Claim(2, "UNSATISFIABLE", warrant), rec, mef1_run.FIXTURE_BLOCK_OF)
        assert valid is False


def test_a_witness_generalises_downward_only() -> None:
    rec = mef1_run._fixture_record(witnesses=(3,))
    b = mef1_run.FIXTURE_BLOCK_OF
    assert mef1_model.warrant_is_valid(
        Claim(1, "SATISFIABLE", "MONOTONE_CLOSURE", 3), rec, b)[0] is True
    assert mef1_model.warrant_is_valid(
        Claim(4, "SATISFIABLE", "MONOTONE_CLOSURE", 3), rec, b)[0] is False


def test_a_refutation_generalises_upward_only() -> None:
    rec = mef1_run._fixture_record(refutations=(2,))
    b = mef1_run.FIXTURE_BLOCK_OF
    assert mef1_model.warrant_is_valid(
        Claim(4, "UNSATISFIABLE", "MONOTONE_CLOSURE", 2), rec, b)[0] is True
    assert mef1_model.warrant_is_valid(
        Claim(0, "UNSATISFIABLE", "MONOTONE_CLOSURE", 2), rec, b)[0] is False


def test_closure_never_crosses_a_block_boundary() -> None:
    """Rungs 0-4 are block 0 and rungs 5-9 are block 1: evidence earned in one sub-ladder
    licenses nothing at all in the other, whether or not the source rung is named."""
    b = mef1_run.FIXTURE_BLOCK_OF
    sat = mef1_run._fixture_record(witnesses=(7,))
    unsat = mef1_run._fixture_record(refutations=(0,))
    for claim in (Claim(0, "SATISFIABLE", "MONOTONE_CLOSURE", 7),
                  Claim(0, "SATISFIABLE", "MONOTONE_CLOSURE", None)):
        assert mef1_model.warrant_is_valid(claim, sat, b)[0] is False
    for claim in (Claim(6, "UNSATISFIABLE", "MONOTONE_CLOSURE", 0),
                  Claim(6, "UNSATISFIABLE", "MONOTONE_CLOSURE", None)):
        assert mef1_model.warrant_is_valid(claim, unsat, b)[0] is False
    # ... and the SAME inference inside one block is licensed, so the refusal above is
    # about the boundary and not about closure in general.
    assert mef1_model.warrant_is_valid(
        Claim(5, "SATISFIABLE", "MONOTONE_CLOSURE", 7), sat, b)[0] is True


def test_unresolved_must_carry_warrant_none() -> None:
    rec = mef1_run._fixture_record(witnesses=(2,))
    assert mef1_model.warrant_is_valid(Claim(2, "UNRESOLVED", "NONE"), rec)[0] is True
    for warrant in ("VERIFIED_WITNESS", "MONOTONE_CLOSURE", "COMPLETED_REFUTATION"):
        assert mef1_model.warrant_is_valid(
            Claim(2, "UNRESOLVED", warrant), rec)[0] is False


# =====================================================================================
# toolbox soundness (G0b)
# =====================================================================================


def test_every_witness_found_verifies_against_the_unpreprocessed_rung() -> None:
    """Iterates every preprocess mode on purpose: a version of this test that only
    exercised ``none`` would pass while a preprocessed witness silently failed to satisfy
    the rung it was claimed for."""
    seen = 0
    seen_preprocessed = 0
    for index in range(4):
        for family in ("F_CRITICAL", "F_PLANTED"):
            c = tiny(index, family)
            for rung in range(c.n_rungs):
                base = mef1_toolbox._base_clauses(c, rung)
                for mode in MODES:
                    kept, _ = mef1_toolbox._clauses_for(c, rung, mode)
                    for tool, budget in (("local_search", 3000), ("exact_solve", 3000)):
                        meter = mef1_toolbox.Meter(limit=BUDGET)
                        res = mef1_toolbox.run_action(
                            c, meter, Action(tool, rung, budget, mode), 7)
                        if res.outcome != "WITNESS_FOUND":
                            continue
                        seen += 1
                        if mode != "none" and kept != base:
                            seen_preprocessed += 1
                        assert res.witness is not None
                        assert mef1_toolbox.verify_witness(c, rung, res.witness), (
                            family, index, rung, mode, tool)
    assert seen > 0
    # the test must actually observe a witness produced from a CHANGED clause set,
    # otherwise it has not checked preprocessing at all
    assert seen_preprocessed > 0


def test_refuted_is_emitted_only_with_a_completed_refutation() -> None:
    refuted = inconclusive = 0
    for index in range(3):
        c = tiny(index)
        for rung in range(c.n_rungs):
            for node_limit in (1, 20, 5000):
                meter = mef1_toolbox.Meter(limit=BUDGET)
                res = mef1_toolbox.exact_solve(c, meter, rung, node_limit, "none")
                if res.outcome == "REFUTED":
                    refuted += 1
                    assert res.refutation_complete is True
                else:
                    inconclusive += 1
                    assert res.refutation_complete is False
    assert refuted > 0 and inconclusive > 0


def test_local_search_can_never_establish_unsatisfiability() -> None:
    for index in range(3):
        c = tiny(index)
        for rung in range(c.n_rungs):
            meter = mef1_toolbox.Meter(limit=BUDGET)
            res = mef1_toolbox.local_search(c, meter, rung, 2000, "none", 11)
            assert res.outcome in ("WITNESS_FOUND", "INCONCLUSIVE", "REJECTED")
            assert res.refutation_complete is False


def test_the_meter_never_exceeds_its_limit() -> None:
    """With ``mode="none"`` -- which is what every deterministic arm and the reference
    pass use -- the meter is exact.  Under a preprocess mode the one-shot preprocessing
    charge is not capped against the remaining budget, so the meter can overshoot by at
    most the rung's clause count; that documented bound is asserted rather than glossed.
    """
    for index in range(3):
        c = tiny(index)
        for rung in range(c.n_rungs):
            n_clauses = c.rungs[rung].clause_count
            for limit in (40, 300, BUDGET):
                for mode in MODES:
                    for tool, budget in (("local_search", 5000), ("exact_solve", 5000)):
                        meter = mef1_toolbox.Meter(limit=limit)
                        mef1_toolbox.run_action(
                            c, meter, Action(tool, rung, budget, mode), 5)
                        if mode == "none":
                            assert meter.spent <= limit, (rung, mode, tool, limit)
                        else:
                            assert meter.spent <= limit + n_clauses, (rung, mode, tool)


def test_preprocessing_never_changes_a_rungs_status() -> None:
    for index in range(3):
        c = tiny(index)
        gt = tiny_ground_truth(c)
        for rung in range(c.n_rungs):
            for mode in MODES:
                meter = mef1_toolbox.Meter(limit=BUDGET)
                res = mef1_toolbox.run_action(
                    c, meter, Action("exact_solve", rung, 5000, mode), 3)
                if res.outcome == "WITNESS_FOUND":
                    assert gt[rung] != "UNSAT", (rung, mode)
                elif res.outcome == "REFUTED":
                    assert gt[rung] != "SAT", (rung, mode)


# =====================================================================================
# generator (G0d)
# =====================================================================================


def test_sub_ladders_are_strictly_increasing_and_prefix_nested() -> None:
    c = tiny()
    for b in c.blocks:
        rungs = c.rungs_in_block(b.block_id)
        counts = [r.clause_count for r in rungs]
        assert counts == sorted(counts) and len(set(counts)) == len(counts)
        for lower, higher in zip(rungs, rungs[1:]):
            lo = lower.clauses(b.pool)
            hi = higher.clauses(b.pool)
            assert hi[:len(lo)] == lo, "a rung's clause set must be a PREFIX of the next"


def test_blocks_are_independent() -> None:
    c = tiny()
    assert len(c.blocks) == N_BLOCKS
    pools = [b.pool for b in c.blocks]
    assert pools[0] != pools[1], "independent sub-ladders must not share a clause pool"
    for r in c.rungs:
        assert c.block_of(r.index).block_id == r.block
        assert c.pool_of(r.index) is c.blocks[r.block].pool
    # every rung belongs to exactly one block and the blocks partition the campaign
    assert sum(len(c.rungs_in_block(b.block_id)) for b in c.blocks) == c.n_rungs


def test_planted_campaigns_are_satisfiable_at_every_rung() -> None:
    """The planted assignment is internal to the generator, so the observable consequence
    is what is asserted: an exhaustive search settles every rung with a verified witness
    and no rung of a planted campaign is ever refuted."""
    for index in range(3):
        c = tiny(index, "F_PLANTED")
        for rung in range(c.n_rungs):
            meter = mef1_toolbox.Meter(limit=200_000)
            res = mef1_toolbox.exact_solve(c, meter, rung, 100_000, "none")
            assert res.outcome == "WITNESS_FOUND", (index, rung, res.outcome, res.note)
            assert mef1_toolbox.verify_witness(c, rung, res.witness)


def test_critical_campaigns_carry_both_satisfiable_and_unsatisfiable_rungs() -> None:
    statuses = set()
    for index in range(3):
        statuses.update(tiny_ground_truth(tiny(index)).values())
    assert "SAT" in statuses and "UNSAT" in statuses


# =====================================================================================
# reference
# =====================================================================================


def _truth(rung: int, status: str):
    return mef1_reference.RungTruth(rung, status, 0, "unit")


def test_monotone_repair_is_block_local() -> None:
    """Rungs 0-2 are block 0 and 3-5 are block 1.  A witness in block 0 must not settle an
    unsettled rung in block 1, even though its global index is lower."""
    bo = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1}
    truths = [_truth(0, "UNSETTLED"), _truth(1, "UNSETTLED"), _truth(2, "SAT"),
              _truth(3, "UNSETTLED"), _truth(4, "UNSETTLED"), _truth(5, "UNSETTLED")]
    out = {t.rung: t.status for t in mef1_reference.monotone_repair(truths, bo)}
    assert out[0] == "SAT" and out[1] == "SAT"          # below a SAT rung, same block
    assert out[3] == out[4] == out[5] == "UNSETTLED"    # a different block: untouched


def test_monotone_repair_never_overwrites_a_settled_status() -> None:
    bo = {i: 0 for i in range(4)}
    truths = [_truth(0, "UNSAT"), _truth(1, "UNSETTLED"), _truth(2, "SAT"),
              _truth(3, "UNSETTLED")]
    out = {t.rung: t.status for t in mef1_reference.monotone_repair(truths, bo)}
    assert out[0] == "UNSAT" and out[2] == "SAT"   # settled statuses survive verbatim
    assert out[1] == "SAT"                         # only UNSETTLED is ever converted
    methods = {t.rung: t.method for t in mef1_reference.monotone_repair(truths, bo)}
    assert methods[1] == "monotone_closure" and methods[0] == "unit"


def test_check_consistency_catches_an_injected_non_monotone_case() -> None:
    bo = {i: 0 for i in range(3)}
    good = [_truth(0, "SAT"), _truth(1, "UNSETTLED"), _truth(2, "UNSAT")]
    assert mef1_reference.check_consistency(good, bo) == (True, "")
    bad = [_truth(0, "UNSAT"), _truth(1, "UNSETTLED"), _truth(2, "SAT")]
    ok, reason = mef1_reference.check_consistency(bad, bo)
    assert ok is False and "block 0" in reason
    # the same pair in DIFFERENT blocks is not an inconsistency at all
    assert mef1_reference.check_consistency(bad, {0: 0, 1: 0, 2: 1})[0] is True


def test_generated_ground_truth_is_monotone_within_every_block() -> None:
    for index in range(3):
        c = tiny(index)
        bo = block_of(c)
        truths = mef1_reference.monotone_repair(
            mef1_reference.ground_truth(c, 2, 50_000), bo)
        assert mef1_reference.check_consistency(truths, bo) == (True, "")


# =====================================================================================
# statistics
# =====================================================================================


def test_paired_sample_size_reproduces_the_sd70v2_reference_value() -> None:
    assert mef1_stats.paired_sample_size(0.1, 0.3) == 234


def test_exact_two_sided_is_symmetric_and_bounded() -> None:
    for b, c in ((0, 0), (1, 0), (3, 7), (10, 2), (25, 25)):
        assert mef1_stats.exact_two_sided(b, c) == mef1_stats.exact_two_sided(c, b)
        assert 0.0 <= mef1_stats.exact_two_sided(b, c) <= 1.0
    assert mef1_stats.exact_two_sided(0, 0) == 1.0
    assert mef1_stats.exact_two_sided(25, 25) == 1.0
    assert mef1_stats.exact_two_sided(20, 0) < 0.05


def test_mde_at_n_is_decreasing_in_n() -> None:
    for discordance in (0.30, 0.45, 0.60):
        mdes = [mef1_stats.mde_at_n(n, discordance) for n in (50, 100, 150, 300, 600)]
        assert all(a > b for a, b in zip(mdes, mdes[1:])), (discordance, mdes)
    # and reproduces the sensitivity band frozen in the design
    design = mef1_run.design()
    for key, expected in design["power"]["mde_sensitivity_band"].items():
        discordance = float(key.split("_")[-1])
        assert abs(mef1_stats.mde_at_n(150, discordance) - expected) < 0.001


# =====================================================================================
# scoring
# =====================================================================================


def test_a_correct_but_unwarranted_claim_scores_zero_on_the_primary() -> None:
    """The laundering case: the arm names the right answer with no licence for it.  It is
    correct, it is worth nothing on the primary endpoint, and it is counted separately so
    a correctness-only reading of the receipt is impossible."""
    rec = CampaignRecord("C1", "LAUNDERER")
    rec.actions.append(ActionResult(Action("local_search", 0, 1, "none"), "INCONCLUSIVE", 0))
    rec.claims = [Claim(0, "UNSATISFIABLE", "NONE"), Claim(1, "UNRESOLVED", "NONE")]
    gt = {0: "UNSAT", 1: "SAT"}
    score = mef1_score.score_campaign(rec, gt, "F_CRITICAL", 2, {0: 0, 1: 0})

    row = score.rungs[0]
    assert row.correct is True and row.warranted is False
    assert row.warranted_correct is False
    assert score.rate() == 0.0

    agg = mef1_score.aggregate([score])
    assert agg["warranted_correct_rate"] == 0.0
    assert agg["correct_rate_ignoring_warrant"] == 0.5
    assert agg["correct_and_unwarranted"] == 1
    assert agg["unwarranted_claims"] == 1
    assert agg["unwarranted_claim_rate"] == 1.0


def test_a_warranted_correct_claim_scores_one() -> None:
    rec = CampaignRecord("C1", "HONEST")
    rec.actions.append(ActionResult(Action("exact_solve", 0, 1, "none"), "REFUTED", 0,
                                    refutation_complete=True))
    rec.claims = [Claim(0, "UNSATISFIABLE", "COMPLETED_REFUTATION")]
    score = mef1_score.score_campaign(rec, {0: "UNSAT"}, "F_CRITICAL", 1, {0: 0})
    assert score.rate() == 1.0 and score.coverage() == 1.0


def test_the_scorer_refuses_a_cross_block_closure() -> None:
    """``score_campaign`` is the laundering detector: given the campaign's block map it
    must reject a closure drawn from an independent sub-ladder."""
    rec = CampaignRecord("C1", "CROSS_BLOCK")
    rec.actions.append(ActionResult(Action("local_search", 3, 1, "none"), "WITNESS_FOUND",
                                    0, witness=(True,)))
    rec.claims = [Claim(0, "SATISFIABLE", "MONOTONE_CLOSURE", 3)]
    gt = {0: "SAT", 1: "SAT", 2: "SAT", 3: "SAT"}
    bo = {0: 0, 1: 0, 2: 1, 3: 1}
    score = mef1_score.score_campaign(rec, gt, "F_CRITICAL", 4, bo)
    assert score.rungs[0].correct is True
    assert score.rungs[0].warranted is False
    assert score.rate() == 0.0


def test_c_never_claim_scores_exactly_zero_on_the_primary() -> None:
    c = tiny()
    gt = tiny_ground_truth(c)
    rec = mef1_arms.run_deterministic_arm(c, "C_NEVER_CLAIM")
    assert {cl.verdict for cl in rec.claims} == {"UNRESOLVED"}
    score = mef1_score.score_campaign(rec, gt, c.family, c.n_rungs, block_of(c))
    assert score.rate() == 0.0
    agg = mef1_score.aggregate([score])
    assert agg["warranted_correct_rate"] == 0.0
    assert agg["coverage"] == 0.0
    assert agg["abstention_rate"] == 1.0


def test_deterministic_arms_only_claim_what_the_version_space_entails() -> None:
    for arm in ("C_UNIFORM_ALLOCATION", "B5_ALGORITHMIC_CORE_NO_MODEL"):
        c = tiny(1)
        gt = tiny_ground_truth(c)
        rec = mef1_arms.run_deterministic_arm(c, arm)
        score = mef1_score.score_campaign(rec, gt, c.family, c.n_rungs, block_of(c))
        unwarranted = [r for r in score.rungs if r.claimed and not r.warranted]
        assert unwarranted == [], (arm, [(r.rung, r.warrant_reason) for r in unwarranted])
        wrong = [r for r in score.decided if r.claimed and not r.correct]
        assert wrong == [], (arm, [(r.rung, r.verdict, r.gt) for r in wrong])


def test_the_resource_curve_is_monotone_in_the_budget() -> None:
    c = tiny(2)
    gt = tiny_ground_truth(c)
    rec = mef1_arms.run_deterministic_arm(c, "C_UNIFORM_ALLOCATION")
    score = mef1_score.score_campaign(rec, gt, c.family, c.n_rungs, block_of(c))
    curve = mef1_score.resource_curve([score], (0.1, 0.25, 0.5, 0.75, 1.0))
    values = [curve[k] for k in ("10pct", "25pct", "50pct", "75pct", "100pct")]
    assert all(a <= b for a, b in zip(values, values[1:])), values


# =====================================================================================
# routing
# =====================================================================================


def _gates(*, g0c: bool = True, g1: bool = False, g1c: bool = False,
           g2: bool = True, g3: bool = True) -> dict:
    return {
        "G0c_NULL_CALIBRATION": {"pass": g0c},
        "G1_M_ADVANTAGE": {"fired": g1, "diff": 0.2 if g1 else 0.0, "p": 0.01},
        "G1c_B5_ADVANTAGE": {"fired": g1c, "diff": -0.2 if g1c else 0.0, "p": 0.01},
        "G2_ANTI_CONSERVATISM": {"pass": g2},
        "G3_MECHANISM": {"pass": g3},
        "G4_INTERFACE_LADDER": {"pass": True, "ladder": {}},
    }


def _power(adequate: bool) -> dict:
    return {"adequately_powered": adequate, "mde": 0.1 if adequate else 0.42}


def test_cannot_check_pre_empts_every_scientific_route() -> None:
    """Integrity is evaluated FIRST: a study that cannot be checked cannot report a
    residual, however emphatically the scientific gates fire."""
    bad = {"pass": False, "reason": "unsettled fraction above the registered threshold"}
    routed, reason = mef1_score.route(_gates(g1=True), bad, _power(True), mef1_run.design())
    assert routed == "CANNOT_CHECK"
    assert "unsettled" in reason
    # ... and a failed null calibration pre-empts it too
    routed, _ = mef1_score.route(_gates(g0c=False, g1=True), {"pass": True, "reason": ""},
                                 _power(True), mef1_run.design())
    assert routed == "CANNOT_CHECK"


def test_an_underpowered_null_routes_cannot_check_not_parent_sufficient() -> None:
    ok = {"pass": True, "reason": ""}
    routed, reason = mef1_score.route(_gates(), ok, _power(False), mef1_run.design())
    assert routed == "CANNOT_CHECK"
    assert "0.42" in reason
    # the same null at an adequate MDE is the honest parent-sufficiency terminal
    routed, _ = mef1_score.route(_gates(), ok, _power(True), mef1_run.design())
    assert routed == "PARENT_SUFFICIENT"


def test_a_g2_failure_routes_resource_efficiency_residual_only() -> None:
    ok = {"pass": True, "reason": ""}
    routed, _ = mef1_score.route(_gates(g1=True, g2=False), ok, _power(True),
                                 mef1_run.design())
    assert routed == "RESOURCE_EFFICIENCY_RESIDUAL_ONLY"
    # G1 with G2 and G3 both passing is the only route to a residual candidate
    routed, _ = mef1_score.route(_gates(g1=True), ok, _power(True), mef1_run.design())
    assert routed == "FRONTIER_RESIDUAL_CANDIDATE"
    # an unattributable advantage is not a residual
    routed, _ = mef1_score.route(_gates(g1=True, g3=False), ok, _power(True),
                                 mef1_run.design())
    assert routed == "CANNOT_CHECK"


def test_b5_advantage_is_a_parent_sufficient_terminal() -> None:
    routed, _ = mef1_score.route(_gates(g1c=True), {"pass": True, "reason": ""},
                                 _power(True), mef1_run.design())
    assert routed == "PARENT_SUFFICIENT"


def test_the_power_dict_refuses_to_call_a_zero_information_contrast_powered() -> None:
    """With no discordant campaign there is no MDE to estimate, and a null in that state
    must never be reported as parent sufficiency it has not earned."""
    contrast = {"n_paired_campaigns": 40, "campaign_wins_a": 0, "campaign_wins_b": 0}
    power = mef1_run._power(contrast)
    assert power["adequately_powered"] is False
    assert power["mde_estimable"] is False
    assert isinstance(power["mde"], float)
    empty = mef1_run._power({"n_paired_campaigns": 0, "campaign_wins_a": 0,
                             "campaign_wins_b": 0})
    assert empty["adequately_powered"] is False
    routed, _ = mef1_score.route(_gates(), {"pass": True, "reason": ""}, power,
                                 mef1_run.design())
    assert routed == "CANNOT_CHECK"


# =====================================================================================
# model arms, driven through an injected channel (NO model call is ever made)
# =====================================================================================


def _receipt(body, ok: bool = True, failure: str = ""):
    return mef1_channel.CallReceipt(ok=ok, body=body, model_calls=1, total_tokens=123,
                                    wall_seconds=0.0, requested_model="fake-model",
                                    failure=failure, prompt_sha256="0" * 64)


def _canned_call(campaign, verdict: str = "UNRESOLVED", warrant: str = "NONE"):
    """A deterministic stand-in for the Codex channel: one legal action, then a full
    claim sheet.  It records every prompt it was given so the caller can assert on them."""
    prompts: list[str] = []

    def call(prompt, schema, **kw):
        prompts.append(prompt)
        return _receipt({
            "next_action": {"tool": "local_search", "rung": 0, "budget": 500,
                            "mode": "none"},
            "rationale": "canned", "escalation_level": 0,
            "claims": [{"rung": i, "verdict": verdict, "warrant": warrant,
                        "source_rung": None} for i in range(campaign.n_rungs)],
            "diagnoses": [{"rung": 0, "obstruction": "SEARCH_INSUFFICIENT"}],
            "stop_now": False,
        })
    return call, prompts


def test_a_model_arm_runs_its_whole_control_budget_and_claims_every_rung() -> None:
    c = tiny()
    call, prompts = _canned_call(c)
    rec = mef1_arms.run_model_arm(c, "M_ME_FRONTIER_CONTROL", call_fn=call)
    assert rec.model_calls == c.max_control_calls
    assert len(prompts) == c.max_control_calls
    assert {cl.rung for cl in rec.claims} == set(range(c.n_rungs))
    assert rec.cannot_check == ""
    # the last call is the CLOSING call and executes no action
    assert "THIS IS YOUR FINAL CALL" in prompts[-1]
    assert len(rec.actions) == c.max_control_calls - 1


def test_every_arm_sees_the_same_campaign_view_and_no_ground_truth() -> None:
    """Information matching is a property of the code: ``arm_view`` carries no ground
    truth, no reference budget, no seed and no per-rung difficulty annotation."""
    c = tiny()
    view = c.arm_view()
    assert "seed" not in view and "ground_truth" not in view
    blob = json.dumps(view)
    assert str(c.seed) not in blob
    prompts_by_arm = {}
    for arm in ("SIMPLE_DIRECT", "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION",
                "M_ME_FRONTIER_CONTROL"):
        call, prompts = _canned_call(c)
        mef1_arms.run_model_arm(c, arm, call_fn=call)
        prompts_by_arm[arm] = prompts[0]
        assert str(c.seed) not in prompts[0]
        assert "ground_truth" not in prompts[0]
    # The world, the blocks, the toolbox and the budget reach every arm as ONE identical
    # preamble; the arms differ only after it, in their frozen control text and in what
    # crosses the module boundary (the H-EXT-3 interface axis).
    preambles = {a: p.split("CURRENT CLAIM SHEET")[0] for a, p in prompts_by_arm.items()}
    assert len(set(preambles.values())) == 1, "arms do not share one campaign preamble"
    assert len(set(prompts_by_arm.values())) == 3, "the control text must differ per arm"


def test_a_failed_model_call_marks_the_campaign_cannot_check_and_is_still_booked() -> None:
    c = tiny()

    def failing(prompt, schema, **kw):
        return _receipt(None, ok=False, failure="RC1:boom")

    rec = mef1_arms.run_model_arm(c, "SIMPLE_DIRECT", call_fn=failing)
    assert rec.cannot_check.startswith("model call failed")
    # a failure consumes channel capacity and must appear in the matched budget
    assert rec.model_calls == 1
    score = mef1_score.score_campaign(rec, tiny_ground_truth(c), c.family, c.n_rungs,
                                      block_of(c))
    assert score.cannot_check
    agg = mef1_score.aggregate([score])
    assert agg["n_cannot_check"] == 1 and agg["n_usable_campaigns"] == 0


def test_an_unwarranted_model_arm_is_detected_from_its_own_log() -> None:
    """The end-to-end laundering path: a model arm that asserts UNSATISFIABLE everywhere
    with no licence scores zero on the primary however many rungs it happens to get right.
    """
    c = tiny()
    call, _ = _canned_call(c, verdict="UNSATISFIABLE", warrant="NONE")
    rec = mef1_arms.run_model_arm(c, "SIMPLE_DIRECT", call_fn=call)
    gt = tiny_ground_truth(c)
    score = mef1_score.score_campaign(rec, gt, c.family, c.n_rungs, block_of(c))
    agg = mef1_score.aggregate([score])
    assert agg["warranted_correct_rate"] == 0.0
    assert agg["unwarranted_claim_rate"] == 1.0
    assert agg["correct_and_unwarranted"] > 0
    assert agg["coverage"] == 1.0  # it answered everywhere; it just had no right to


def test_the_run_dispatcher_logs_every_model_call_with_its_prompt_hash() -> None:
    c = tiny()
    call, _ = _canned_call(c)
    records, log = mef1_run.run_arms([(c, "SIMPLE_DIRECT"), (c, "C_NEVER_CLAIM")],
                                     max_concurrency=2, call_fn=call)
    assert set(records) == {(c.campaign_id, "SIMPLE_DIRECT"),
                            (c.campaign_id, "C_NEVER_CLAIM")}
    assert len(log) == c.max_control_calls
    for entry in log:
        assert entry["arm"] == "SIMPLE_DIRECT"
        assert entry["prompt_sha256"] and entry["requested_model"] == "fake-model"
        assert entry["served_model_observed"] is None
        assert entry["body"] is not None


# =====================================================================================
# runner stages and guards
# =====================================================================================


def test_the_design_sha256_is_the_hash_of_the_raw_design_bytes() -> None:
    import hashlib
    expected = hashlib.sha256(mef1_run.DESIGN_JSON.read_bytes()).hexdigest()
    assert mef1_run.design_sha256() == expected


def test_the_protected_stage_refuses_without_an_authorization_file(tmp_path) -> None:
    if mef1_run.AUTH_FILE.exists():
        pytest.skip("PROTECTED_RUN_AUTHORIZATION.json is present; the refusal path cannot "
                    "be exercised without disturbing an authorized run")
    assert mef1_run.main(["protected", "--out", str(tmp_path)]) == 3
    # and nothing was generated
    assert list(tmp_path.iterdir()) == []


def _authorize(tmp_path, monkeypatch, *, human_written=True, token="a" * 16,
               design_sha=None):
    """Point the runner's authorization constant at a TEMPORARY file.

    The real ``PROTECTED_RUN_AUTHORIZATION.json`` is never created by this suite: these
    tests exercise the guard, not the run, and every one of them stops at a refusal.
    """
    auth = tmp_path / "AUTH.json"
    auth.write_text(json.dumps({
        "human_written": human_written, "human_written_token": token,
        "acknowledged_design_sha256": (mef1_run.design_sha256() if design_sha is None
                                       else design_sha)}))
    monkeypatch.setattr(mef1_run, "AUTH_FILE", auth)
    return auth


@pytest.mark.parametrize("kwargs", [
    {"human_written": False},
    {"token": "short"},
    {"design_sha": "0" * 64},
], ids=["not_human_written", "token_too_short", "design_sha_mismatch"])
def test_the_protected_stage_refuses_a_defective_authorization(tmp_path, monkeypatch,
                                                               kwargs) -> None:
    _authorize(tmp_path, monkeypatch, **kwargs)
    seed = tmp_path / "seed.txt"
    seed.write_text("irrelevant")
    assert mef1_run.stage_protected(tmp_path / "out", seed, ["C_NEVER_CLAIM"], 1) == 3
    assert not (tmp_path / "out").exists()


def test_the_protected_stage_refuses_a_seed_that_misses_the_commitment(tmp_path,
                                                                       monkeypatch) -> None:
    """Exit 4: even a fully valid authorization cannot start a protected run without the
    custody seed whose sha256 the design committed to before any campaign existed."""
    commitment = mef1_run.design()["seed_commitment"]["protected_seed_sha256"]
    _authorize(tmp_path, monkeypatch)
    missing = tmp_path / "absent.txt"
    assert mef1_run.stage_protected(tmp_path / "out", missing, ["C_NEVER_CLAIM"], 1) == 4
    wrong = tmp_path / "seed.txt"
    wrong.write_text("definitely-not-the-committed-seed")
    import hashlib
    assert hashlib.sha256(b"definitely-not-the-committed-seed").hexdigest() != commitment
    assert mef1_run.stage_protected(tmp_path / "out", wrong, ["C_NEVER_CLAIM"], 1) == 4
    assert not (tmp_path / "out").exists()


def test_max_concurrency_above_the_frozen_channel_budget_is_refused() -> None:
    with pytest.raises(SystemExit):
        mef1_run.main(["selftest",
                       "--max-concurrency", str(mef1_run.MAX_CONCURRENCY + 1)])
    assert mef1_run.MAX_CONCURRENCY >= 3


def test_the_cli_defaults_to_three_concurrent_model_calls(tmp_path, monkeypatch) -> None:
    seen: dict[str, int] = {}

    def spy(out_dir, n_campaigns, arms, max_concurrency, call_fn=None):
        seen["max_concurrency"] = max_concurrency
        return 0

    monkeypatch.setattr(mef1_run, "stage_dev", spy)
    assert mef1_run.main(["dev", "--out", str(tmp_path)]) == 0
    assert seen["max_concurrency"] == 3


def test_an_unregistered_arm_is_a_usage_error(tmp_path) -> None:
    assert mef1_run.main(["dev", "--out", str(tmp_path), "--arms", "NOT_AN_ARM"]) == 2


def test_the_development_split_is_capped(tmp_path) -> None:
    assert mef1_run.stage_dev(tmp_path, mef1_run.DEV_CAP + 1, ["C_NEVER_CLAIM"], 1) == 2


def test_the_warrant_fixture_gate_reports_every_row(tmp_path) -> None:
    report = mef1_run.check_warrant_fixtures()
    assert report["pass"] is True
    assert report["n"] == report["n_pass"] == len(mef1_run.warrant_validity_fixtures())
    assert all(set(row) >= {"name", "kind", "expected_valid", "observed_valid", "pass"}
               for row in report["rows"])


def test_analyze_scores_a_split_end_to_end(tmp_path) -> None:
    """A whole split through the real dispatcher, custody writer, scorer and router --
    deterministic arms plus one canned model arm, so no model call is made."""
    c = tiny(0)
    call, _ = _canned_call(c, verdict="UNSATISFIABLE", warrant="NONE")
    geometry = {"level": "UNIT", "n_vars": N_VARS, "budget_checks": BUDGET,
                "n_blocks": N_BLOCKS, "why": "unit test"}
    rp, cp = mef1_run.run_split(
        "UNIT", "ME-F1-UNIT", [c],
        ["C_NEVER_CLAIM", "C_UNIFORM_ALLOCATION", "SIMPLE_DIRECT"],
        tmp_path, 1, None, geometry, call)
    rc, analysis = mef1_run.stage_analyze(rp, cp, tmp_path, "UNIT")
    assert rc == 0
    assert analysis["per_arm"]["C_NEVER_CLAIM"]["warranted_correct_rate"] == 0.0
    assert analysis["per_arm"]["SIMPLE_DIRECT"]["unwarranted_claim_rate"] == 1.0
    # no M or B5 campaigns were run, so the contrast is empty and the route must not
    # report parent sufficiency it has not earned
    assert analysis["power"]["adequately_powered"] is False
    assert analysis["route"]["route"] == "CANNOT_CHECK"
    # the audit table puts claim, evidence and oracle verdict side by side
    rows = [r for r in analysis["per_campaign_audit"] if r["arm"] == "SIMPLE_DIRECT"]
    assert len(rows) == c.n_rungs
    assert set(rows[0]) >= {"claimed_verdict", "actually_established", "oracle_verdict"}
    assert (tmp_path / "ME_F1_UNIT_ANALYSIS_V1.md").exists()
    assert (tmp_path / "ME_F1_UNIT_CALL_LOG_V1.json").exists()
    custody = json.loads(cp.read_text())
    assert all(r["monotone_within_blocks"] for r in custody["campaigns"])


class _FakeScore:
    def __init__(self, rate: float) -> None:
        self._rate = rate

    def rate(self) -> float:
        return self._rate


def _calibrate_with(tmp_path, monkeypatch, rates, consistent: bool = True) -> dict:
    """Drive the calibration ladder at controlled primary rates.

    The point of the exercise is the TERMINAL, so the rate is injected rather than earned:
    every terminal in ``calibration.procedure`` must be reachable and none may be arrived
    at by falling through.
    """
    import copy
    d = copy.deepcopy(mef1_run.design())
    d["calibration"]["ladder"] = {"L1": {"n_vars": 10, "budget_checks": 8000},
                                  "L2": {"n_vars": 10, "budget_checks": 9000}}
    d["calibration"]["ladder_order"] = ["L1", "L2"]
    d["calibration"]["dev_campaigns_per_level"] = 2
    monkeypatch.setattr(mef1_run, "_DESIGN", d)

    seq = iter([r for r in rates for _ in range(2)])
    monkeypatch.setattr(mef1_run, "score_campaign",
                        lambda *a, **k: _FakeScore(next(seq)))
    monkeypatch.setattr(mef1_run, "campaign_ground_truth",
                        lambda c: ({i: "SAT" for i in range(c.n_rungs)}, [], consistent,
                                   "" if consistent else "block 0: SAT above UNSAT"))
    assert mef1_run.stage_calibrate(tmp_path) == 0
    return json.loads((tmp_path / "ME_F1_CALIBRATION_RECEIPT.json").read_text())


@pytest.mark.parametrize("rates,consistent,terminal", [
    ([0.9, 0.5], True, "WINDOW_HIT"),
    ([0.9, 0.85], True, "SUITE_STILL_SATURATED"),
    ([0.9, 0.1], True, "LADDER_OVERSHOT_NO_WINDOW_HIT"),
    ([0.1, 0.1], True, "SUITE_AT_FLOOR_AT_FIRST_RUNG"),
    ([0.5, 0.5], False, "CALIBRATION_INVALID_INCONSISTENT_GROUND_TRUTH"),
])
def test_every_calibration_terminal_is_reachable_and_explicit(tmp_path, monkeypatch,
                                                              rates, consistent,
                                                              terminal) -> None:
    receipt = _calibrate_with(tmp_path, monkeypatch, rates, consistent)
    assert receipt["decision"] == terminal
    assert receipt["reason"]
    assert receipt["selected_level"] == ("L2" if terminal == "WINDOW_HIT" else None)
    assert set(receipt["rows"][0]) >= {"level", "n_vars", "budget", "campaigns", "rate",
                                       "sd", "unsettled_gt", "inconsistent", "in_window"}


def test_calibration_stops_at_the_first_rung_inside_the_window(tmp_path,
                                                               monkeypatch) -> None:
    """Ascend and STOP: a rung inside the window freezes the difficulty and the ladder is
    never re-tuned afterwards (``calibration.if_no_window_hit``)."""
    receipt = _calibrate_with(tmp_path, monkeypatch, [0.5, 0.4])
    assert receipt["decision"] == "WINDOW_HIT" and receipt["selected_level"] == "L1"
    assert len(receipt["rows"]) == 1, "the ladder must not be climbed past a WINDOW_HIT"
    assert receipt["window"] == mef1_run.design()["calibration"]["window"]


def test_the_integrity_gate_is_strict_at_the_threshold() -> None:
    """``comparisons_are_strict``: exactly at a threshold PASSES; only a strict excess
    routes the study to CANNOT_CHECK."""
    threshold = mef1_run.design()["integrity"]["global_unsettled_threshold"]
    n = 100
    at = int(round(threshold * n))

    def custody_with(unsettled: int) -> dict:
        statuses = {str(i): ("UNSETTLED" if i < unsettled else "SAT") for i in range(n)}
        return {"campaigns": [{"campaign_id": "C", "ground_truth": statuses,
                               "monotone_within_blocks": True}]}

    results = {"design_sha256": mef1_run.design_sha256()}
    assert mef1_run._integrity(results, custody_with(at), {})["pass"] is True
    over = mef1_run._integrity(results, custody_with(at + 1), {})
    assert over["pass"] is False and "settle" in over["reason"]


def test_the_integrity_gate_catches_a_non_monotone_ground_truth() -> None:
    custody = {"campaigns": [{"campaign_id": "C", "ground_truth": {"0": "SAT"},
                              "monotone_within_blocks": False}]}
    got = mef1_run._integrity({"design_sha256": mef1_run.design_sha256()}, custody, {})
    assert got["pass"] is False and "non-monotone" in got["reason"]
