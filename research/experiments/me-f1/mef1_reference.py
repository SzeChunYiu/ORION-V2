"""ME-F1 reference solver: post-hoc ground truth (frozen with design V1).

Ground truth is established by running the SAME sound primitives at ``K`` times the
arm budget, entirely outside the experiment, and is never visible to any arm.  That
is what makes this study's endpoint externally verifiable without a hidden oracle the
arms could have been tuned on: there is no oracle *at the arm budget* at all, and the
one that exists post-hoc is only the same mechanics given far more room.

A rung the reference cannot settle even at ``K`` x budget has NO ground truth.  It is
recorded ``UNSETTLED`` and excluded from the primary endpoint by the pre-registered
per-instance rule (design S6.2).  The *global* integrity gate (design S6.3) routes the
whole study to ``CANNOT_CHECK`` if the unsettled fraction exceeds its registered
threshold, so an unsettleable suite can never be reported as a primary on the residue.

Determinism: the reference pass depends only on the campaign and ``K``, never on any
arm, so it may be computed before or after the arms run without affecting anything.
"""
from __future__ import annotations

from dataclasses import dataclass

from mef1_model import Campaign
from mef1_toolbox import Meter, exact_solve, local_search


@dataclass(frozen=True, slots=True)
class RungTruth:
    rung: int
    status: str  # SAT | UNSAT | UNSETTLED
    checks_used: int
    method: str


def settle_rung(campaign: Campaign, rung_index: int, budget: int, node_limit: int,
                ls_seed: int) -> RungTruth:
    """Settle one rung: try local search for a witness, then exhaustive DPLL."""
    meter = Meter(limit=budget)
    got = local_search(campaign, meter, rung_index, budget // 4, "none", ls_seed)
    if got.outcome == "WITNESS_FOUND":
        return RungTruth(rung_index, "SAT", meter.spent, "local_search")
    res = exact_solve(campaign, meter, rung_index, node_limit, "none")
    if res.outcome == "WITNESS_FOUND":
        return RungTruth(rung_index, "SAT", meter.spent, "exact_solve")
    if res.outcome == "REFUTED" and res.refutation_complete:
        return RungTruth(rung_index, "UNSAT", meter.spent, "exact_solve")
    return RungTruth(rung_index, "UNSETTLED", meter.spent, "exhausted_reference_budget")


def ground_truth(campaign: Campaign, k: int, node_limit: int) -> list[RungTruth]:
    """Ground truth for every rung at K x the campaign's arm budget."""
    budget = campaign.budget_checks * k
    return [settle_rung(campaign, i, budget, node_limit, campaign.seed ^ (0xA11CE + i))
            for i in range(campaign.n_rungs)]


def monotone_repair(truths: list[RungTruth], block_of: dict[int, int] | None = None
                    ) -> list[RungTruth]:
    """Close ground truth under the ladder's own monotonicity.

    If rung i is SAT then every rung below it is SAT; if rung i is UNSAT then every
    rung above it is UNSAT.  This is a *sound* inference from the prefix construction,
    not a guess, so applying it can only convert ``UNSETTLED`` into a known status and
    can never overwrite a settled one.  It is applied to ground truth only -- arms get
    no such help beyond what they establish themselves.
    """
    out = list(truths)
    block_of = block_of or {t.rung: 0 for t in truths}
    for blk in set(block_of.values()):
        members = [t for t in out if block_of.get(t.rung) == blk]
        highest_sat = max((t.rung for t in members if t.status == "SAT"), default=None)
        lowest_unsat = min((t.rung for t in members if t.status == "UNSAT"), default=None)
        for i, t in enumerate(out):
            if t.status != "UNSETTLED" or block_of.get(t.rung) != blk:
                continue
            if highest_sat is not None and t.rung < highest_sat:
                out[i] = RungTruth(t.rung, "SAT", t.checks_used, "monotone_closure")
            elif lowest_unsat is not None and t.rung > lowest_unsat:
                out[i] = RungTruth(t.rung, "UNSAT", t.checks_used, "monotone_closure")
    return out


def check_consistency(truths: list[RungTruth], block_of: dict[int, int] | None = None
                      ) -> tuple[bool, str]:
    """G0b invariant: within every block, settled ground truth is monotone."""
    block_of = block_of or {t.rung: 0 for t in truths}
    for blk in set(block_of.values()):
        members = [t for t in truths if block_of.get(t.rung) == blk]
        highest_sat = max((t.rung for t in members if t.status == "SAT"), default=-1)
        lowest_unsat = min((t.rung for t in members if t.status == "UNSAT"), default=10**9)
        if highest_sat > lowest_unsat:
            return (False, f"block {blk}: SAT at rung {highest_sat} above UNSAT at {lowest_unsat}")
    return (True, "")
