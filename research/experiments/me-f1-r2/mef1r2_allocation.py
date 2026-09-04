"""ME-F1 R2 — probe allocation re-derived for the action budget actually given.

`ME_F1_G0E_OUTCOME_RECEIPT_V1.md` section 5.1 makes a **conjunctive** precondition on
any ME-F1 successor: no successor may freeze `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`
until (a) its control text carries the `INCONCLUSIVE` -> switch-tool fallback its own
algorithmic core already implements, **and** (b) *"its probe allocation is re-derived
for the action budget it is actually given"*.

Clause (a) is met. This module discharges clause (b), and it does so on the
**deterministic** federation, where no model call is involved and the measurement is
byte-reproducible.

The measured problem. `B5_ALGORITHMIC_CORE_NO_MODEL` scores 0.925 on the development
split at the ~120 actions it naturally takes (8 campaigns, 12-18 actions each). Every
model arm gets **7 actions plus a closing call**. Capped at 7 the same federation
collapses. An under-budgeted parent is artificially isolated in exactly the way an
under-prompted one is, and the prompt asymmetry has already been repaired.

Nothing here edits ME-F1 V1. `mef1_arms.run_deterministic_arm` is untouched; the
`FROZEN` policy below is a replica whose fidelity to it is asserted by an executable
control (`policy_frozen_reproduces_the_shipped_core`), so a re-derived policy is
compared against the real thing and not against a lookalike.

Two independent defects are separated, because the receipt requires attribution to ONE
stage before a lever is applied:

  SCHEDULE   the core selects every probe with `Bisector.next_probe()`, the midpoint.
             With five rungs per block the midpoint is local index 2 -- the critical
             rung, alpha = 4.267, the hardest instance in the block by construction.
             Binary search is the right parent when the budget suffices to localise a
             boundary (~ceil(log2 5) = 3 probes per block, 12 for four blocks); at 7
             actions it never gets there, and it spends what it has on the rungs least
             likely to return anything. The federation ALREADY CONTAINS the component
             that fixes this -- `portfolio_schedule`, whose docstring is "order rungs by
             expected information per unit cost (cheap ends first)" -- and the core
             never calls it.

  LUBY       the core sizes its restart schedule with `luby_budgets(checks // 2, 12)`,
             a hardcoded 12 probes. Given 7 actions it uses the first 7 terms of a
             12-term split and leaves the rest of the check budget unspent. Sizing the
             same published schedule to the probes actually available is the whole fix.

Both levers are re-derivations WITHIN the federation's own published components. No new
method is introduced, and the parent is not strengthened by anything a faithful
implementer would not already have.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

V1 = Path(__file__).resolve().parent.parent / "me-f1"
if str(V1) not in sys.path:
    sys.path.insert(0, str(V1))

from mef1_arms import _State, run_action  # noqa: E402
from mef1_model import Action, Campaign, CampaignRecord, Claim  # noqa: E402
from mef1_toolbox import Meter  # noqa: E402
from mef1_parents import (  # noqa: E402
    RungFeatures,
    calibrated_abstention,
    luby_budgets,
    portfolio_schedule,
    portfolio_select,
)

# Levers, one per suspected defect, so a repair can be attributed to ONE stage.
FROZEN = "FROZEN"                      # the shipped core, replicated exactly
LUBY_SIZED = "LUBY_SIZED"              # midpoint probes, Luby sized to the action budget
SCHEDULE_ONLY = "SCHEDULE_ONLY"        # information-ordered probes, Luby hardcoded 12
BUDGET_AWARE = "BUDGET_AWARE"          # schedule + Luby sizing
TRAINED_TOOL = "TRAINED_TOOL"          # midpoint probes, SOLVER SELECTION TRAINED ON THE
                                       # DEVELOPMENT SPLIT (SATzilla's own procedure)
REDERIVED = "REDERIVED"                # trained tool + Luby sized: the re-derived allocation
POLICIES = (FROZEN, LUBY_SIZED, SCHEDULE_ONLY, BUDGET_AWARE, TRAINED_TOOL, REDERIVED)

TRAINED_TOOL_POLICIES = (TRAINED_TOOL, REDERIVED)
SCHEDULED_POLICIES = (SCHEDULE_ONLY, BUDGET_AWARE)
LUBY_SIZED_POLICIES = (LUBY_SIZED, BUDGET_AWARE, REDERIVED)

FROZEN_N_PROBES = 12                   # the hardcoded probe count in the shipped core

# ---- the trained portfolio ------------------------------------------------------------
# Rice (1976) / SATzilla (Xu et al. 2008) do not ship a fixed rule: they TRAIN the
# selector on the instance distribution the solver will face.  The shipped
# `portfolio_select` instead hardcodes the random-3-SAT literature threshold
# (4.267 +/- 0.15) and prescribes "in the critical band, try the cheap witness first" --
# a rule whose premise is that the complete method is the expensive one.
#
# Measured on the development split at the SELECTED geometry (L2, n_vars = 30,
# 300 000 checks), one probe per (rung, tool) at the cap-7 Luby unit budget of 12 500
# checks, 32 probes per cell (8 campaigns x 4 blocks):
#
#   ratio   exact_solve settled   local_search settled   exact checks   local checks
#   3.200   32/32 = 1.00          23/32 = 0.72            4 346          7 888
#   4.000   32/32 = 1.00           9/32 = 0.28           15 156         11 335
#   4.267   32/32 = 1.00           4/32 = 0.12           23 127         11 986
#   4.700   32/32 = 1.00           1/32 = 0.03           24 384         12 545
#   5.600   32/32 = 1.00           0/32 = 0.00           19 930         12 813
#
# `local_search` is dominated at every ratio, and at the cheapest rung it is dominated on
# BOTH resources (0.72 settled for 7 888 checks against 1.00 for 4 346).  At n_vars = 30
# the complete solver is not the expensive one, so the premise of the shipped rule does
# not hold at this geometry.  The trained selector is therefore `exact_solve` everywhere.
# This is the published method applied, not replaced: the training step the shipped
# implementation skipped is what produces the difference.
TRAINED_PORTFOLIO_TABLE: dict[float, str] = {
    3.200: "exact_solve", 4.000: "exact_solve", 4.267: "exact_solve",
    4.700: "exact_solve", 5.600: "exact_solve",
}


def trained_select(feat: RungFeatures) -> str:
    """Solver selection trained on the development split rather than hardcoded.

    **At this geometry the trained selector is constant.** Every entry in the table is
    `exact_solve`, so this function is currently indistinguishable from
    `return "exact_solve"`, and the nearest-key lookup is structure for a future geometry
    rather than a guard that does anything today. Said plainly here because a lookup that
    cannot branch would otherwise read as one that might.

    An unseen ratio falls back to the nearest trained key rather than silently reverting
    to the shipped rule. `trained_select_is_extrapolating` reports whether that fallback
    was an interpolation or a reach, so a geometry change is visible rather than absorbed.
    """
    key = min(TRAINED_PORTFOLIO_TABLE, key=lambda k: abs(k - feat.ratio))
    return TRAINED_PORTFOLIO_TABLE[key]


#: How far a ratio may sit from a trained key before the selection is an extrapolation
#: rather than a lookup.  Half the smallest gap between trained keys (4.267 - 4.000).
TRAINED_KEY_TOLERANCE = 0.134


def trained_select_is_extrapolating(feat: RungFeatures) -> bool:
    """True when no trained key is close to this rung's ratio.

    The training table covers the five ratios this ladder generates. A geometry that
    produces other ratios is outside what was measured, and this makes that visible
    instead of letting the nearest-key lookup absorb it silently.
    """
    key = min(TRAINED_PORTFOLIO_TABLE, key=lambda k: abs(k - feat.ratio))
    return abs(key - feat.ratio) > TRAINED_KEY_TOLERANCE


@dataclass(frozen=True, slots=True)
class Allocation:
    policy: str
    max_actions: int | None
    n_probes_for_luby: int


def _luby_probe_count(policy: str, max_actions: int | None) -> int:
    """How many probes the restart schedule is sized for.

    FROZEN and SCHEDULE_ONLY keep the shipped hardcoded 12. LUBY_SIZED and BUDGET_AWARE
    size it to the actions actually available, which is conservative: a fallback costs a
    second action, so the realised probe count is at most `max_actions`.
    """
    if policy not in LUBY_SIZED_POLICIES or max_actions is None:
        return FROZEN_N_PROBES
    return max(1, max_actions)


def _block_schedule(campaign: Campaign, st: _State) -> dict[int, list[tuple[int, str]]]:
    """`portfolio_schedule` applied within each block, in the federation's own order.

    Closure never crosses a block (`_State.local`), so the schedule is computed per
    block: highest-ratio easy-SAT rung first and lowest-ratio easy-UNSAT rung first --
    each settles the most rungs by monotone closure per probe -- and the critical rung
    last, because it is the one a probe is most likely to return nothing on.
    """
    out: dict[int, list[tuple[int, str]]] = {}
    for blk, rungs in st.local.items():
        feats = [RungFeatures(r, campaign.rungs[r].n_vars, campaign.rungs[r].clause_count)
                 for r in rungs]
        out[blk] = portfolio_schedule(feats)
    return out


def _next_probe_frozen(st: _State, stuck: set[int]) -> tuple[int, int] | None:
    for b in sorted(st.local):
        if b in stuck:
            continue
        nxt = st.bisect[b].next_probe()
        if nxt is not None:
            return st.local[b][nxt], b
    return None


def _next_probe_scheduled(st: _State, sched: dict[int, list[tuple[int, str]]],
                          used: set[int], stuck: set[int]) -> tuple[int, int, str] | None:
    """Round-robin over blocks, next unsettled scheduled rung in each.

    A rung already entailed by that block's version space is skipped: spending an action
    on a rung whose verdict is already licensed is the same waste the schedule exists to
    avoid.
    """
    for b in sorted(st.local):
        if b in stuck or st.bisect[b].next_probe() is None:
            continue
        for rung, tool in sched[b]:
            if rung in used or st.entailed(rung) is not None:
                continue
            return rung, b, tool
    return None


def run_core(campaign: Campaign, policy: str = FROZEN,
             max_actions: int | None = None) -> CampaignRecord:
    """The federation's deterministic core under a given allocation policy and action cap.

    With `policy=FROZEN` and `max_actions=None` this is the shipped
    `B5_ALGORITHMIC_CORE_NO_MODEL` exactly; the control test asserts that against the
    real function rather than trusting the replica.
    """
    if policy not in POLICIES:
        raise ValueError(f"unregistered allocation policy: {policy}")
    rec = CampaignRecord(campaign.campaign_id, f"B5_CORE[{policy}]")
    meter = Meter(limit=campaign.budget_checks)
    st = _State(campaign)
    budgets = luby_budgets(campaign.budget_checks // 2,
                           _luby_probe_count(policy, max_actions))
    sched = _block_schedule(campaign, st) if policy in SCHEDULED_POLICIES else {}
    used: set[int] = set()
    stuck: set[int] = set()
    bi = 0

    def _cap_reached() -> bool:
        return max_actions is not None and len(rec.actions) >= max_actions

    while meter.remaining > 0 and bi < len(budgets) and not _cap_reached():
        if policy not in SCHEDULED_POLICIES:
            nxt = _next_probe_frozen(st, stuck)
            if nxt is None:
                break
            probe, blk = nxt
            feat = RungFeatures(probe, campaign.rungs[probe].n_vars,
                                campaign.rungs[probe].clause_count)
            tool = (trained_select(feat) if policy in TRAINED_TOOL_POLICIES
                    else portfolio_select(feat))
        else:
            nxt3 = _next_probe_scheduled(st, sched, used, stuck)
            if nxt3 is None:
                break
            probe, blk, tool = nxt3
            if policy in TRAINED_TOOL_POLICIES:
                tool = trained_select(RungFeatures(probe, campaign.rungs[probe].n_vars,
                                                  campaign.rungs[probe].clause_count))
        used.add(probe)
        r = run_action(campaign, meter, Action(tool, probe, budgets[bi], "none"),
                       campaign.seed + bi)
        rec.actions.append(r)
        st.note(r)
        if r.outcome == "INCONCLUSIVE" and meter.remaining > 0 and not _cap_reached():
            other = "exact_solve" if tool == "local_search" else "local_search"
            r2 = run_action(campaign, meter, Action(other, probe, budgets[bi], "none"),
                            campaign.seed + 100 + bi)
            rec.actions.append(r2)
            st.note(r2)
            if r2.outcome == "INCONCLUSIVE":
                stuck.add(blk)
        bi += 1

    _emit_claims(campaign, st, rec)
    rec.checks_spent = meter.spent
    return rec


def _emit_claims(campaign: Campaign, st: _State, rec: CampaignRecord) -> None:
    """Claim exactly what the version space entails -- never more.

    Copied verbatim in behaviour from the shipped core so that a policy comparison is a
    comparison of ALLOCATION and nothing else. The warranted-claim discipline
    (Mitchell version spaces + calibrated abstention) is not a variable here.
    """
    for i in range(campaign.n_rungs):
        blk = st.block_of[i]
        same = [r for r in range(campaign.n_rungs) if st.block_of[r] == blk]
        verdict = calibrated_abstention(st.entailed(i))
        if verdict == "UNRESOLVED":
            rec.claims.append(Claim(i, "UNRESOLVED", "NONE"))
        elif i in st.witness_rungs:
            rec.claims.append(Claim(i, verdict, "VERIFIED_WITNESS"))
        elif i in st.refuted_rungs:
            rec.claims.append(Claim(i, verdict, "COMPLETED_REFUTATION"))
        elif verdict == "SATISFIABLE":
            src = min((w for w in st.witness_rungs if w in same and w >= i), default=None)
            rec.claims.append(Claim(i, verdict, "MONOTONE_CLOSURE", src)
                              if src is not None else Claim(i, "UNRESOLVED", "NONE"))
        else:
            src = max((u for u in st.refuted_rungs if u in same and u <= i), default=None)
            rec.claims.append(Claim(i, verdict, "MONOTONE_CLOSURE", src)
                              if src is not None else Claim(i, "UNRESOLVED", "NONE"))


def action_signature(rec: CampaignRecord) -> list[tuple[str, int, int, str]]:
    return [(r.action.tool, r.action.rung, r.action.budget, r.outcome) for r in rec.actions]


def claim_signature(rec: CampaignRecord) -> list[tuple[int, str, str, Any]]:
    return [(c.rung, c.verdict, c.warrant, c.source_rung) for c in rec.claims]
