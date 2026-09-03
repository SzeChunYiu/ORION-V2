"""ME-F1 scoring and gates (frozen with design V1).

Two axes are kept strictly separate throughout, and the separation is the point of the
study:

* **correctness** -- does the claim agree with ground truth?  Ground truth comes from
  ``mef1_reference`` and no arm ever sees it.
* **warrant** -- was the arm *entitled* to the claim, given what its own execution log
  establishes?  Computed by ``mef1_model.warrant_is_valid``, which never reads ground
  truth.

An arm can be correct-and-unwarranted (the laundering failure ME-X1 measured: the direct
arm made 492 unwarranted updates) or, in a sound world, warranted-and-correct.  A study
that only scored correctness would rank a laundering arm at the top of the upper rungs,
because those rungs really are unsatisfiable -- it would just have no right to say so.

PRIMARY ENDPOINT: ``warranted_correct_rate`` over ground-truth-decided rungs.  Abstention
scores zero, so no arm can win this endpoint by refusing to answer.  That is the direct
structural repair of the failure ME-X2 found, where M's ``CANNOT_IDENTIFY`` on decidable
episodes was its loss and its ``G2`` pass at the same time.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mef1_model import CampaignRecord, warrant_is_valid
from mef1_stats import (cluster_bootstrap_ci, exact_two_sided, paired_wald_ci, wilson95)


@dataclass
class RungScore:
    rung: int
    gt: str
    verdict: str
    warrant: str
    correct: bool
    warranted: bool
    warrant_reason: str

    @property
    def warranted_correct(self) -> bool:
        return self.correct and self.warranted

    @property
    def claimed(self) -> bool:
        return self.verdict != "UNRESOLVED"


@dataclass
class CampaignScore:
    campaign_id: str
    arm_id: str
    family: str
    rungs: list[RungScore] = field(default_factory=list)
    checks_spent: int = 0
    model_calls: int = 0
    model_tokens: int = 0
    wall_ms: int = 0
    cannot_check: str = ""
    resource_curve: list[tuple[int, int]] = field(default_factory=list)

    @property
    def decided(self) -> list[RungScore]:
        return [r for r in self.rungs if r.gt in ("SAT", "UNSAT")]

    def rate(self) -> float:
        d = self.decided
        return sum(r.warranted_correct for r in d) / len(d) if d else 0.0

    def coverage(self) -> float:
        d = self.decided
        return sum(r.claimed for r in d) / len(d) if d else 0.0


def score_campaign(record: CampaignRecord, gt: dict[int, str], family: str,
                   n_rungs: int, block_of: dict[int, int] | None = None) -> CampaignScore:
    """Score one arm's record on one campaign.

    ``block_of`` maps each global rung index to its block and MUST be supplied whenever the
    campaign has more than one block: monotone closure is block-local (design S2.2,
    "nothing crosses a block boundary"), and without the map ``warrant_is_valid`` will
    licence a closure inference drawn from an independent sub-ladder.
    """
    cs = CampaignScore(record.campaign_id, record.arm_id, family,
                       checks_spent=record.checks_spent, model_calls=record.model_calls,
                       model_tokens=record.model_tokens, wall_ms=record.wall_ms,
                       cannot_check=record.cannot_check)
    by_rung = {c.rung: c for c in record.claims}
    for i in range(n_rungs):
        claim = by_rung.get(i)
        verdict = claim.verdict if claim else "UNRESOLVED"
        warrant = claim.warrant if claim else "NONE"
        g = gt.get(i, "UNSETTLED")
        if claim is None:
            ok, reason = True, "no claim"
        else:
            ok, reason = warrant_is_valid(claim, record, block_of)
        correct = ((g == "SAT" and verdict == "SATISFIABLE")
                   or (g == "UNSAT" and verdict == "UNSATISFIABLE"))
        cs.rungs.append(RungScore(i, g, verdict, warrant, correct, ok, reason))

    # resource-to-solution curve: cumulative checks -> cumulative rungs ESTABLISHED
    # (verified witness or completed refutation).  Establishment, not claiming, because
    # this curve is about what the search bought, not what the arm chose to say.
    spent = 0
    established: set[int] = set()
    for res in record.actions:
        spent += res.checks_spent
        if res.outcome == "WITNESS_FOUND" or (res.outcome == "REFUTED" and res.refutation_complete):
            established.add(res.action.rung)
        cs.resource_curve.append((spent, len(established)))
    return cs


# ---- arm-level aggregation ---------------------------------------------------------------


def aggregate(scores: list[CampaignScore]) -> dict[str, Any]:
    usable = [s for s in scores if not s.cannot_check]
    decided = [r for s in usable for r in s.decided]
    claimed = [r for r in decided if r.claimed]
    sat_rungs = [r for r in decided if r.gt == "SAT"]

    n_dec = len(decided)
    wc = sum(r.warranted_correct for r in decided)
    correct_only = sum(r.correct for r in decided)
    unwarranted = [r for r in claimed if not r.warranted]
    false_completion = [r for r in claimed if not r.correct]
    # correct abstention: UNRESOLVED on a rung the arm never established
    abstained = [r for r in decided if not r.claimed]

    return {
        "n_campaigns": len(scores),
        "n_usable_campaigns": len(usable),
        "n_cannot_check": len(scores) - len(usable),
        "n_decided_rungs": n_dec,
        # The denominator of every rate below.  Reported explicitly because a rate of
        # 0.0 over zero claims and a rate of 0.0 over eighty claims are different facts,
        # and an artifact that prints only the rate cannot tell a reader which it holds.
        "n_claimed_rungs": len(claimed),
        "warranted_correct_rate": (wc / n_dec) if n_dec else 0.0,
        "warranted_correct_wilson95": wilson95(wc, n_dec),
        "correct_rate_ignoring_warrant": (correct_only / n_dec) if n_dec else 0.0,
        "coverage": (len(claimed) / n_dec) if n_dec else 0.0,
        "witness_found_rate": (
            sum(1 for r in sat_rungs if r.warrant == "VERIFIED_WITNESS" and r.warranted)
            / len(sat_rungs)) if sat_rungs else 0.0,
        "false_completion_rate": (len(false_completion) / len(claimed)) if claimed else 0.0,
        "false_completions": len(false_completion),
        "unwarranted_claim_rate": (len(unwarranted) / len(claimed)) if claimed else 0.0,
        "unwarranted_claims": len(unwarranted),
        "correct_and_unwarranted": sum(1 for r in unwarranted if r.correct),
        "abstention_rate": (len(abstained) / n_dec) if n_dec else 0.0,
        "mean_checks": (sum(s.checks_spent for s in usable) / len(usable)) if usable else 0.0,
        "model_calls": sum(s.model_calls for s in scores),
        "model_tokens": sum(s.model_tokens for s in scores),
        "mean_wall_ms": (sum(s.wall_ms for s in usable) / len(usable)) if usable else 0.0,
    }


def resource_curve(scores: list[CampaignScore], fractions: tuple[float, ...]) -> dict[str, float]:
    """Mean rungs established by each registered fraction of the budget."""
    out: dict[str, float] = {}
    usable = [s for s in scores if not s.cannot_check and s.resource_curve]
    for f in fractions:
        vals = []
        for s in usable:
            total = s.resource_curve[-1][0] if s.resource_curve else 0
            cap = total * f
            best = 0
            for spent, est in s.resource_curve:
                if spent <= cap:
                    best = est
            vals.append(best)
        out[f"{int(f * 100)}pct"] = (sum(vals) / len(vals)) if vals else 0.0
    return out


# ---- paired contrast ---------------------------------------------------------------------


def paired_contrast(a: list[CampaignScore], b: list[CampaignScore]) -> dict[str, Any]:
    """Paired comparison of arm A against arm B over the campaigns both completed."""
    ai = {s.campaign_id: s for s in a if not s.cannot_check}
    bi = {s.campaign_id: s for s in b if not s.cannot_check}
    shared = sorted(set(ai) & set(bi))

    # campaign-level paired sign test on the primary rate
    wins = losses = ties = 0
    diffs: list[int] = []
    clusters: list[tuple[int, int]] = []
    for cid in shared:
        ra, rb = ai[cid].rate(), bi[cid].rate()
        if ra > rb:
            wins += 1
            diffs.append(1)
        elif rb > ra:
            losses += 1
            diffs.append(-1)
        else:
            ties += 1
            diffs.append(0)
        da, db = ai[cid].decided, bi[cid].decided
        num = sum(r.warranted_correct for r in da) - sum(r.warranted_correct for r in db)
        clusters.append((num, len(da)))

    a_wc = sum(r.warranted_correct for cid in shared for r in ai[cid].decided)
    b_wc = sum(r.warranted_correct for cid in shared for r in bi[cid].decided)
    n_dec = sum(len(ai[cid].decided) for cid in shared)

    return {
        "n_paired_campaigns": len(shared),
        "campaign_wins_a": wins, "campaign_wins_b": losses, "campaign_ties": ties,
        "sign_test_p": exact_two_sided(wins, losses),
        "campaign_level_diff_ci95": paired_wald_ci(diffs),
        "rung_level_rate_a": (a_wc / n_dec) if n_dec else 0.0,
        "rung_level_rate_b": (b_wc / n_dec) if n_dec else 0.0,
        "rung_level_diff": ((a_wc - b_wc) / n_dec) if n_dec else 0.0,
        "rung_level_diff_cluster_bootstrap_ci95": cluster_bootstrap_ci(clusters),
    }


# ---- gates -------------------------------------------------------------------------------


def evaluate_gates(agg: dict[str, dict[str, Any]], contrast: dict[str, Any],
                   design: dict[str, Any]) -> dict[str, Any]:
    """Apply the frozen gates.  No gate reads anything not registered in the design."""
    g = design["gates"]
    out: dict[str, Any] = {}
    M = "M_ME_FRONTIER_CONTROL"
    B5 = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"

    # G0c null calibration
    never = agg.get("C_NEVER_CLAIM", {})
    rand = agg.get("C_RANDOM_ALLOCATION", {})
    out["G0c_NULL_CALIBRATION"] = {
        "pass": (never.get("warranted_correct_rate", 1.0) == 0.0
                 and rand.get("warranted_correct_rate", 1.0)
                 <= g["G0c_NULL_CALIBRATION"]["random_max_rate"]),
        "never_claim_rate": never.get("warranted_correct_rate"),
        "random_rate": rand.get("warranted_correct_rate"),
    }

    # G1 primary
    diff = contrast["rung_level_diff"]
    p = contrast["sign_test_p"]
    alpha = g["G1_M_ADVANTAGE"]["alpha_two_sided"]
    out["G1_M_ADVANTAGE"] = {"fired": diff > 0 and p <= alpha, "diff": diff, "p": p}
    out["G1c_B5_ADVANTAGE"] = {"fired": diff < 0 and p <= alpha, "diff": diff, "p": p}

    # G2 anti-conservatism: M may not win by abstaining
    delta = g["G2_ANTI_CONSERVATISM"]["max_coverage_shortfall"]
    cov_m = agg.get(M, {}).get("coverage", 0.0)
    cov_b5 = agg.get(B5, {}).get("coverage", 0.0)
    out["G2_ANTI_CONSERVATISM"] = {
        "pass": cov_m >= cov_b5 - delta,
        "coverage_m": cov_m, "coverage_b5": cov_b5, "shortfall": cov_b5 - cov_m,
        "max_allowed_shortfall": delta,
    }

    # G3 mechanism by omission -- only meaningful if G1 fired
    if out["G1_M_ADVANTAGE"]["fired"]:
        abl = {a: agg[a]["warranted_correct_rate"] for a in agg
               if a.startswith("M_") and a != M}
        base = agg[M]["warranted_correct_rate"]
        out["G3_MECHANISM"] = {
            "pass": all(v < base for v in abl.values()) if abl else False,
            "m_rate": base, "ablations": abl,
        }
    else:
        out["G3_MECHANISM"] = {"applicable": False,
                               "reason": "no M advantage to attribute"}

    # G4 interface ladder (H-EXT-3)
    rungs = g["G4_INTERFACE_LADDER"]["order"]
    vals = [agg.get(a, {}).get("warranted_correct_rate") for a in rungs]
    known = [v for v in vals if v is not None]
    monotone = all(known[i] <= known[i + 1] + g["G4_INTERFACE_LADDER"]["tolerance"]
                   for i in range(len(known) - 1)) if len(known) > 1 else True
    out["G4_INTERFACE_LADDER"] = {"pass": monotone, "ladder": dict(zip(rungs, vals))}
    return out


def route(gates: dict[str, Any], integrity: dict[str, Any], power: dict[str, Any],
          design: dict[str, Any]) -> tuple[str, str]:
    """Pre-registered routing.  CANNOT_CHECK is evaluated FIRST and pre-empts every
    scientific route (design S7.1), exactly as SD70-V2 orders its decision rules."""
    if not integrity["pass"]:
        return ("CANNOT_CHECK", integrity["reason"])
    if not gates["G0c_NULL_CALIBRATION"]["pass"]:
        return ("CANNOT_CHECK", "null calibration failed: the scoring machinery is invalid")

    if gates["G1_M_ADVANTAGE"]["fired"]:
        if not gates["G2_ANTI_CONSERVATISM"]["pass"]:
            return ("RESOURCE_EFFICIENCY_RESIDUAL_ONLY",
                    "M leads the primary but its coverage shortfall exceeds the registered "
                    "bound: the advantage is not distinguishable from answering less often")
        if not gates["G3_MECHANISM"].get("pass", False):
            return ("CANNOT_CHECK",
                    "M advantage is not attributable to any registered component by omission")
        return ("FRONTIER_RESIDUAL_CANDIDATE",
                "M exceeds the strongest faithful parent federation on the primary endpoint "
                "under matched resources, with the advantage attributable by omission")

    if gates["G1c_B5_ADVANTAGE"]["fired"]:
        return ("PARENT_SUFFICIENT", "B5 strictly exceeds M on the primary endpoint")

    # a null: only reportable as parent sufficiency if the study could have seen the effect
    if not power["adequately_powered"]:
        return ("CANNOT_CHECK",
                f"null at an MDE of {power['mde']:.3f}, above the registered detectable "
                f"effect of {design['power']['minimum_effect']}: this study cannot "
                f"distinguish parent sufficiency from an undetected residual")
    return ("PARENT_SUFFICIENT", "no detectable difference at an adequate MDE")
