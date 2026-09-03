"""ME-F1 arms (frozen with design V1).

Every arm drives the SAME toolbox through the SAME meter with the SAME per-campaign
budget and the SAME model-call cap.  Arms differ only in their control discipline --
which action to take next, when to stop, and what to claim.  The arm-specific control
text below is frozen verbatim in the design JSON; it is the experimental manipulation
and there is nothing else up any arm's sleeve.

Two families of arm:

* **model arms** spend their control-call budget on the Codex channel;
* **deterministic arms** spend zero model calls and exist to bound the model arms from
  below (``C_*``) and, in the case of ``B5_ALGORITHMIC_CORE_NO_MODEL``, from *above* --
  it runs the parent federation in pure code.  If that arm beats every model arm, the
  honest reading is that model control adds nothing here, and the design says so before
  the run (design S1.2).
"""
from __future__ import annotations

import json
import random
from typing import Any, Callable

from mef1_channel import call_control
from mef1_model import (Action, Campaign, Claim, CampaignRecord, OBSTRUCTION_CLASSES)
from mef1_parents import (Bisector, RungFeatures, VersionSpace, calibrated_abstention,
                          luby_budgets, portfolio_schedule,
                          portfolio_select)
from mef1_toolbox import Meter, run_action

# ---- arm roster --------------------------------------------------------------------------

MODEL_ARMS: tuple[str, ...] = (
    "SIMPLE_DIRECT",
    "SAME_MODEL_REFLECTION",
    "B5_R1_VERDICT_ONLY",
    "B5_R2_PLUS_CANDIDATE_SET",
    "B5_R3_PLUS_FEATURE_TABLES",
    "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION",
    "M_ME_FRONTIER_CONTROL",
    "M_MINUS_WARRANT_GATE",
    "M_MINUS_LOCUS_DIAGNOSIS",
    "M_MINUS_MINIMUM_ESCALATION",
    "M_LOCUS_LABELS_SHUFFLED",
)
DETERMINISTIC_ARMS: tuple[str, ...] = (
    "B5_ALGORITHMIC_CORE_NO_MODEL",
    "C_UNIFORM_ALLOCATION",
    "C_RANDOM_ALLOCATION",
    "C_NEVER_CLAIM",
)
ALL_ARMS: tuple[str, ...] = MODEL_ARMS + DETERMINISTIC_ARMS

#: Arms whose contrast is the primary endpoint, and the arms carried at full n.
PRIMARY_ARMS: tuple[str, ...] = (
    "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION",
    "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION", "M_ME_FRONTIER_CONTROL",
)
SUBSET_ARMS: tuple[str, ...] = tuple(a for a in MODEL_ARMS if a not in PRIMARY_ARMS)


# ---- frozen control text -----------------------------------------------------------------

_COMMON = """You are the CONTROL layer of a bounded combinatorial discovery campaign.
You do not search yourself. You choose what the search tools do next, and what the
campaign claims at the end.

WORLD. A campaign is {n_blocks} INDEPENDENT sub-ladders ("blocks"), {n_rungs} rungs in
total, sharing ONE budget. Each block has its own variables and its own clause pool.
Within a block, a rung's clause set is a strict subset of the next rung's. Therefore,
WITHIN A BLOCK ONLY:
  - a satisfying assignment verified at a rung also satisfies every LOWER rung of that
    same block;
  - a completed refutation at a rung also refutes every HIGHER rung of that same block.
Blocks are independent: nothing you establish in one block tells you anything about
another. You must earn evidence in each block separately.
Blocks (block id, variables, global rung indices, clause counts): {blocks}

TOOLS (each call spends the shared budget, measured in constraint checks):
  local_search(rung, budget, mode)  -> WITNESS_FOUND (verified) or INCONCLUSIVE.
        It can never establish unsatisfiability.
  exact_solve(rung, node_limit, mode) -> WITNESS_FOUND, REFUTED (only when the search
        space was exhausted), or INCONCLUSIVE (node limit hit; nothing established).
  preprocess(rung, mode)  mode in {{none, unit_pure, subsumption, symmetry}}.
  stop  -> end the campaign now.

BUDGET. {budget} constraint checks total; {spent} spent ({pct:.1f}%).
Control decisions remaining: {calls_left}.

LOG SO FAR:
{log}

CURRENT CLAIM SHEET (rungs you have not claimed are UNRESOLVED):
{claims}
"""

_ARM_CONTROL: dict[str, str] = {
    "SIMPLE_DIRECT": """
YOUR PROCEDURE. Settle as many rungs as you can within the budget, then report a
verdict for every rung you have an opinion about. Report SATISFIABLE or UNSATISFIABLE
wherever you believe it, and UNRESOLVED only where you truly have no view.
""",
    "SAME_MODEL_REFLECTION": """
YOUR PROCEDURE. Settle as many rungs as you can within the budget, then report a
verdict for every rung you have an opinion about. Before you finalise, re-read your own
log and reconsider each verdict once, asking whether you would defend it. Revise
anything you would not. Report SATISFIABLE or UNSATISFIABLE wherever you believe it,
and UNRESOLVED only where you truly have no view.
""",
    "B5_R1_VERDICT_ONLY": """
YOUR PROCEDURE (portfolio solver, verdict interface).
Choose the next tool by the clause/variable ratio of the rung: ratio <= 4.12 favours
local_search, ratio >= 4.42 favours exact_solve. Report only a verdict per rung.
Report UNKNOWN as UNRESOLVED when your solver hit its limit.
""",
    "B5_R2_PLUS_CANDIDATE_SET": """
YOUR PROCEDURE (portfolio solver + version space).
Choose the next tool by the clause/variable ratio (<=4.12 local_search, >=4.42
exact_solve). Maintain the set of still-possible boundary positions t, where "boundary
t" means rungs < t are satisfiable and rungs >= t are not. A verified witness at rung i
removes every t <= i; a completed refutation at rung i removes every t > i. Assert a
verdict for a rung ONLY when every surviving t agrees on it; otherwise UNRESOLVED.
The surviving boundary set is given to you below.
""",
    "B5_R3_PLUS_FEATURE_TABLES": """
YOUR PROCEDURE (portfolio solver + version space + feature table).
As above, and you are additionally given the per-rung feature table and the portfolio's
recommended schedule. Follow the schedule unless the log gives you a concrete reason not
to. Assert a verdict for a rung ONLY when every surviving boundary position agrees on it.
""",
    "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION": """
YOUR PROCEDURE (the strongest published federation, applied faithfully).
You are running four established techniques together. Use all of them.
 1. ALGORITHM SELECTION (Rice 1976; SATzilla, Xu et al. 2008). Pick the solver per rung
    from the feature table: ratio <= 4.12 -> local_search; ratio >= 4.42 -> exact_solve;
    in between, try local_search first. The recommended schedule is given below.
 2. BINARY SEARCH within each block. That block's satisfiable rungs form a prefix, so
    its boundary can be localised in about log2(rungs per block) probes instead of one
    probe per rung. Probe the midpoint of each block's still-open interval, given below.
    Do not probe rungs already settled by closure. Budget is shared across blocks, so
    spend it where it buys the most closure.
 3. RESTART POLICY (Luby et al. 1993; Gomes et al. 1998). Backtracking runtimes are
    heavy tailed: prefer several shorter attempts over one long one. The Luby budget
    schedule for your remaining probes is given below.
 4. VERSION SPACE (Mitchell 1982) + CALIBRATED ABSTENTION. Maintain the surviving
    boundary positions; assert a verdict for a rung ONLY when every surviving position
    entails it. Where the evidence does not entail a verdict, report UNRESOLVED, exactly
    as a solver reports UNKNOWN rather than guessing.
""",
    "M_ME_FRONTIER_CONTROL": """
YOUR PROCEDURE (ORION machine-epistemics control).
 1. WARRANT GATE. Every verdict you assert must carry a licence, and you must name it:
      VERIFIED_WITNESS       a witness verified at THIS rung;
      MONOTONE_CLOSURE       inherited from a verified witness at a HIGHER rung
                             (for SATISFIABLE) or a completed refutation at a LOWER rung
                             (for UNSATISFIABLE); name the source rung;
      COMPLETED_REFUTATION   an exhaustive search that closed THIS rung.
    Failing to find a witness is not a refutation and licenses nothing. If you cannot
    name a licence, the verdict is UNRESOLVED. Asserting more than you have established
    is the single failure this control layer exists to prevent.
 2. LOCUS DIAGNOSIS. For each unsettled rung, name what is obstructing you:
    SEARCH_INSUFFICIENT (more of the same search would plausibly settle it),
    REPRESENTATION_INSUFFICIENT (the encoding is the obstacle),
    MODEL_FAMILY_INADEQUATE (wrong tool class for this rung),
    PROBE_ACTION_INSUFFICIENT (budget allocation is the obstacle),
    CANNOT_IDENTIFY (the evidence does not discriminate). Your next action should
    address the diagnosed obstruction, not merely repeat the last one.
 3. MINIMUM ESCALATION. Take the CHEAPEST action that addresses the diagnosis. Escalate
    one level at a time and only when the level below has been tried and diagnosed:
      L0 more budget, same tool, same rung, same encoding
      L1 restart / reseed the same tool
      L2 switch tool class (local_search <-> exact_solve)
      L3 re-encode (change the preprocess mode)
      L4 attack a different rung
    Do not jump to L3 or L4 when L0 or L1 has not been tried on a rung you are still
    working. Escalating past a warranted cheaper step is as much a failure as not
    escalating at all.
""",
    "M_MINUS_WARRANT_GATE": """
YOUR PROCEDURE (ORION control, warrant gate REMOVED).
 1. LOCUS DIAGNOSIS. For each unsettled rung name the obstruction: SEARCH_INSUFFICIENT,
    REPRESENTATION_INSUFFICIENT, MODEL_FAMILY_INADEQUATE, PROBE_ACTION_INSUFFICIENT,
    CANNOT_IDENTIFY. Address the diagnosis with your next action.
 2. MINIMUM ESCALATION. Take the cheapest action that addresses the diagnosis; escalate
    one level at a time (L0 more budget, L1 restart, L2 switch tool, L3 re-encode,
    L4 different rung).
 3. CLAIMS. Report your best judgement of each rung's status. Use UNRESOLVED only where
    you have no view at all.
""",
    "M_MINUS_LOCUS_DIAGNOSIS": """
YOUR PROCEDURE (ORION control, locus diagnosis REMOVED).
 1. WARRANT GATE. Every verdict must name its licence: VERIFIED_WITNESS,
    MONOTONE_CLOSURE (name the source rung), or COMPLETED_REFUTATION. Failing to find a
    witness licenses nothing. Without a licence the verdict is UNRESOLVED.
 2. MINIMUM ESCALATION. Take the cheapest action available; escalate one level at a time
    (L0 more budget, L1 restart, L2 switch tool, L3 re-encode, L4 different rung).
""",
    "M_MINUS_MINIMUM_ESCALATION": """
YOUR PROCEDURE (ORION control, minimum-escalation ordering REMOVED).
 1. WARRANT GATE. Every verdict must name its licence: VERIFIED_WITNESS,
    MONOTONE_CLOSURE (name the source rung), or COMPLETED_REFUTATION. Failing to find a
    witness licenses nothing. Without a licence the verdict is UNRESOLVED.
 2. LOCUS DIAGNOSIS. Name the obstruction for each unsettled rung.
 3. ACTION. Choose whatever action you judge best. There is no ordering constraint and
    no requirement to try cheaper actions first.
""",
    "M_LOCUS_LABELS_SHUFFLED": """
YOUR PROCEDURE (ORION control, with a PERMUTED obstruction vocabulary).
 1. WARRANT GATE. Every verdict must name its licence: VERIFIED_WITNESS,
    MONOTONE_CLOSURE (name the source rung), or COMPLETED_REFUTATION. Failing to find a
    witness licenses nothing. Without a licence the verdict is UNRESOLVED.
 2. LOCUS DIAGNOSIS. For each unsettled rung name the obstruction, using these
    definitions:
      SEARCH_INSUFFICIENT          = the encoding is the obstacle
      REPRESENTATION_INSUFFICIENT  = wrong tool class for this rung
      MODEL_FAMILY_INADEQUATE      = budget allocation is the obstacle
      PROBE_ACTION_INSUFFICIENT    = more of the same search would settle it
      CANNOT_IDENTIFY              = the evidence does not discriminate
    Address the diagnosis with your next action.
 3. MINIMUM ESCALATION. Take the cheapest action that addresses the diagnosis; escalate
    one level at a time (L0 more budget, L1 restart, L2 switch tool, L3 re-encode,
    L4 different rung).
""",
}

#: Extra structured context each arm is given.  This is the H-EXT-3 interface ladder axis:
#: what crosses the module boundary, holding the model and the budget fixed.
_ARM_INTERFACE: dict[str, tuple[str, ...]] = {
    "SIMPLE_DIRECT": (),
    "SAME_MODEL_REFLECTION": (),
    "B5_R1_VERDICT_ONLY": ("features",),
    "B5_R2_PLUS_CANDIDATE_SET": ("features", "version_space"),
    "B5_R3_PLUS_FEATURE_TABLES": ("features", "version_space", "schedule"),
    "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION": ("features", "version_space", "schedule",
                                                "bisect", "luby"),
    "M_ME_FRONTIER_CONTROL": ("features", "established"),
    "M_MINUS_WARRANT_GATE": ("features", "established"),
    "M_MINUS_LOCUS_DIAGNOSIS": ("features", "established"),
    "M_MINUS_MINIMUM_ESCALATION": ("features", "established"),
    "M_LOCUS_LABELS_SHUFFLED": ("features", "established"),
}


#: H-EXT-3 interface ladder, rung 0: arms whose claim schema carries NO warrant field.
#:
#: The earlier schema required a ``warrant`` from a closed enum on every claim for every
#: arm, on the stated assumption that "arms that are not told to use them simply do not".
#: The G0e development measurement falsified that assumption directly: SIMPLE_DIRECT was
#: never told to use warrants and named a correct licence on 121 of 121 claims, and no arm
#: ever paired a definite verdict with NONE in 480 claims.  Requiring the field handed
#: every arm organ (1) of M -- the warrant gate -- so laundering demanded typing a licence
#: the model did not hold, rather than the silent slide ME-X1 measured.  Rung 0 is now
#: given a rung-0 interface, and the scorer determines warrant from the arm's own
#: execution log instead of from a self-report.
#:
#: This changes nothing about the M-versus-B5 primary contrast: neither arm is in this set.
UNNAMED_WARRANT_ARMS: frozenset[str] = frozenset({"SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"})


def _claim_item(arm: str) -> dict[str, Any]:
    """One claim's schema.  Rung-0 arms report a verdict; every other arm names a licence."""
    verdict = {"type": "string", "enum": ["SATISFIABLE", "UNSATISFIABLE", "UNRESOLVED"]}
    if arm in UNNAMED_WARRANT_ARMS:
        return {"type": "object", "additionalProperties": False,
                "required": ["rung", "verdict"],
                "properties": {"rung": {"type": "integer"}, "verdict": verdict}}
    return {
        "type": "object", "additionalProperties": False,
        "required": ["rung", "verdict", "warrant", "source_rung"],
        "properties": {
            "rung": {"type": "integer"},
            "verdict": verdict,
            "warrant": {"type": "string",
                        "enum": ["VERIFIED_WITNESS", "MONOTONE_CLOSURE",
                                 "COMPLETED_REFUTATION", "NONE"]},
            "source_rung": {"type": ["integer", "null"]},
        },
    }


def response_schema(arm: str) -> dict[str, Any]:
    """Strict output schema.

    Every arm gets the same world description, tools, budget and call count.  What differs
    at rung 0 of the H-EXT-3 ladder is the *output* interface: those arms report a verdict
    and are not asked to name its licence.  The diagnosis field is still present for every
    arm so the schema does not advantage one on that axis."""
    # The endpoint enforces strict structured output: every declared property must appear
    # in "required".  Optionality is therefore expressed as a nullable type, never by
    # omission from "required".
    return {
        "type": "object", "additionalProperties": False,
        "required": ["next_action", "rationale", "escalation_level", "claims",
                     "diagnoses", "stop_now"],
        "properties": {
            "next_action": {
                "type": "object", "additionalProperties": False,
                "required": ["tool", "rung", "budget", "mode"],
                "properties": {
                    "tool": {"type": "string", "enum": ["local_search", "exact_solve",
                                                        "preprocess", "stop"]},
                    "rung": {"type": "integer"},
                    "budget": {"type": "integer"},
                    "mode": {"type": "string",
                             "enum": ["none", "unit_pure", "subsumption", "symmetry"]},
                },
            },
            "rationale": {"type": "string"},
            "escalation_level": {"type": ["integer", "null"]},
            "claims": {"type": "array", "items": _claim_item(arm)},
            "diagnoses": {
                "type": "array",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["rung", "obstruction"],
                    "properties": {
                        "rung": {"type": "integer"},
                        "obstruction": {"type": "string", "enum": list(OBSTRUCTION_CLASSES)},
                    },
                },
            },
            "stop_now": {"type": "boolean"},
        },
    }


# ---- shared campaign state ---------------------------------------------------------------


class _State:
    """Bookkeeping shared by every arm.  Derived only from what the arm actually did."""

    def __init__(self, campaign: Campaign) -> None:
        self.c = campaign
        # One version space and one bisector PER BLOCK: closure never crosses a block.
        self.local = {b.block_id: [r.index for r in campaign.rungs_in_block(b.block_id)]
                      for b in campaign.blocks}
        self.vs = {b: VersionSpace(len(rs)) for b, rs in self.local.items()}
        self.bisect = {b: Bisector(len(rs)) for b, rs in self.local.items()}
        self.block_of = {r.index: r.block for r in campaign.rungs}
        self.li = {r.index: r.local_index for r in campaign.rungs}
        self.log: list[str] = []
        self.witness_rungs: set[int] = set()
        self.refuted_rungs: set[int] = set()

    def note(self, res: Any) -> None:
        a = res.action
        blk = self.block_of.get(a.rung)
        self.log.append(
            f"  {a.tool}(rung={a.rung} [block {blk}], budget={a.budget}, mode={a.mode})"
            f" -> {res.outcome} [{res.checks_spent} checks]"
            f"{(' ' + res.note) if res.note else ''}")
        if blk is None:
            return
        j = self.li[a.rung]
        if res.outcome == "WITNESS_FOUND":
            self.witness_rungs.add(a.rung)
            self.vs[blk].observe_sat(j)
            self.bisect[blk].record_sat(j)
        elif res.outcome == "REFUTED" and res.refutation_complete:
            self.refuted_rungs.add(a.rung)
            self.vs[blk].observe_unsat(j)
            self.bisect[blk].record_unsat(j)

    def entailed(self, rung: int) -> str | None:
        blk = self.block_of[rung]
        return self.vs[blk].entailed(self.li[rung])

    def features(self) -> list[RungFeatures]:
        return [RungFeatures(r.index, r.n_vars, r.clause_count) for r in self.c.rungs]

    def context_block(self, keys: tuple[str, ...]) -> str:
        parts: list[str] = []
        if "features" in keys:
            rows = ["  rung  block  clauses  ratio",
                    *[f"  {f.rung:>4}  {self.block_of[f.rung]:>5}  {f.n_clauses:>7}  {f.ratio:.3f}"
                      for f in self.features()]]
            parts.append("FEATURE TABLE:\n" + "\n".join(rows))
        if "version_space" in keys:
            rows = []
            for b, rungs in self.local.items():
                surviving = sorted(self.vs[b].candidates)
                rows.append(f"  block {b} (rungs {rungs}): surviving boundary positions "
                            f"{surviving}")
            parts.append("VERSION SPACE PER BLOCK\n"
                         "(boundary t in a block means that block's rungs with local index "
                         "< t are satisfiable and >= t are not):\n" + "\n".join(rows))
        if "schedule" in keys:
            sched = portfolio_schedule(self.features())
            parts.append("PORTFOLIO SCHEDULE (rung, recommended tool): "
                         + ", ".join(f"({r},{t})" for r, t in sched))
        if "bisect" in keys:
            rows = []
            for b, rungs in self.local.items():
                bi = self.bisect[b]
                nxt = bi.next_probe()
                glob = rungs[nxt] if nxt is not None else None
                rows.append(f"  block {b}: highest local index known satisfiable = {bi.lo}, "
                            f"lowest known unsatisfiable = {bi.hi}, next midpoint probe = "
                            + (f"rung {glob}" if glob is not None else "boundary localised"))
            parts.append("BINARY SEARCH PER BLOCK:\n" + "\n".join(rows))
        if "luby" in keys:
            parts.append(f"LUBY BUDGET SCHEDULE for remaining probes: "
                         f"{luby_budgets(max(1, self.c.budget_checks // 4), 8)}")
        if "established" in keys:
            parts.append(f"ESTABLISHED BY YOU SO FAR: verified witnesses at rungs "
                         f"{sorted(self.witness_rungs) or 'none'}; completed refutations at rungs "
                         f"{sorted(self.refuted_rungs) or 'none'}")
        return "\n\n".join(parts)


def _ingest_claim(arm: str, item: dict[str, Any]) -> Claim:
    """Build a Claim from the model's own JSON.  Nothing is filtered or repaired here.

    A rung-0 arm's schema has no warrant field, so its claims carry ``UNNAMED``: the
    scorer decides from the execution log whether the assertion was entitled, rather than
    the arm being asked to declare it.
    """
    rung, verdict = int(item["rung"]), str(item["verdict"])
    if arm in UNNAMED_WARRANT_ARMS:
        return Claim(rung, verdict, "UNNAMED", None)
    return Claim(rung, verdict, str(item["warrant"]),
                 int(item["source_rung"]) if item.get("source_rung") is not None else None)


def _claims_text(claims: dict[int, Claim]) -> str:
    """Render the running claim sheet back to the arm.

    A rung-0 arm never sees a warrant column -- echoing one would re-teach through the
    context the discipline its schema deliberately withholds.
    """
    if not claims:
        return "  (none yet)"
    out = []
    for r, c in sorted(claims.items()):
        if c.warrant == "UNNAMED":
            out.append(f"  rung {r}: {c.verdict}")
        else:
            out.append(f"  rung {r}: {c.verdict} (warrant {c.warrant}"
                       + (f", source rung {c.source_rung}" if c.source_rung is not None
                          else "") + ")")
    return "\n".join(out)


# ---- model-arm driver --------------------------------------------------------------------


def run_model_arm(campaign: Campaign, arm: str, *, call_fn: Callable[..., Any] | None = None,
                  ) -> CampaignRecord:
    """Drive one campaign with one model arm.  Exactly one model call per control decision."""
    call_fn = call_fn or call_control
    rec = CampaignRecord(campaign.campaign_id, arm)
    meter = Meter(limit=campaign.budget_checks)
    st = _State(campaign)
    claims: dict[int, Claim] = {}
    schema = response_schema(arm)
    view = campaign.arm_view()

    # The final call is a CLOSING call: no further action is executed, so the arm can
    # claim the evidence its last action produced.  Without it the last action's result
    # is unclaimable by construction, which would penalise every arm identically but
    # would also silently waste one call per campaign.
    for turn in range(campaign.max_control_calls):
        closing = (turn == campaign.max_control_calls - 1) or meter.remaining <= 0
        ctx = st.context_block(_ARM_INTERFACE.get(arm, ()))
        prompt = (
            _COMMON.format(
                n_rungs=campaign.n_rungs, n_blocks=len(campaign.blocks),
                blocks=json.dumps(view["blocks"]), budget=campaign.budget_checks,
                spent=meter.spent, pct=100.0 * meter.spent / campaign.budget_checks,
                calls_left=campaign.max_control_calls - turn,
                log="\n".join(st.log) if st.log else "  (nothing yet)",
                claims=_claims_text(claims))
            + (("\n" + ctx + "\n") if ctx else "")
            + _ARM_CONTROL[arm]
            + ("\nTHIS IS YOUR FINAL CALL. No further action will be executed. Emit your "
               "COMPLETE final claim sheet now: one entry for every rung 0.."
               f"{campaign.n_rungs - 1}, each with its verdict and warrant. Set stop_now "
               "to true and set next_action.tool to \"stop\"." if closing else
               "\nEmit your next action, and update your claim sheet for any rung whose "
               "status your latest evidence has changed.")
            + "\nReply with the JSON object only."
        )
        receipt = call_fn(prompt, schema)
        rec.model_calls += receipt.model_calls
        rec.model_tokens += receipt.total_tokens or 0
        rec.wall_ms += int(receipt.wall_seconds * 1000)
        if not receipt.ok or receipt.body is None:
            rec.cannot_check = f"model call failed at turn {turn}: {receipt.failure}"
            return rec

        body = receipt.body
        for item in body.get("claims", []) or []:
            try:
                cl = _ingest_claim(arm, item)
            except (KeyError, ValueError, TypeError):
                continue
            if 0 <= cl.rung < campaign.n_rungs:
                claims[cl.rung] = cl
        for item in body.get("diagnoses", []) or []:
            try:
                rec.diagnoses[int(item["rung"])] = (str(item["obstruction"]), "")
            except (KeyError, ValueError, TypeError):
                continue

        if closing:
            break
        if body.get("stop_now") or (body.get("next_action", {}) or {}).get("tool") == "stop":
            rec.stopped_early = True
            # An arm that stops early keeps its remaining calls unspent; it still gets one
            # closing call so its evidence is claimable on the same terms as any other arm.
            ctx = st.context_block(_ARM_INTERFACE.get(arm, ()))
            final_prompt = (
                _COMMON.format(
                    n_rungs=campaign.n_rungs, n_blocks=len(campaign.blocks),
                    blocks=json.dumps(view["blocks"]), budget=campaign.budget_checks,
                    spent=meter.spent, pct=100.0 * meter.spent / campaign.budget_checks,
                    calls_left=1,
                    log="\n".join(st.log) if st.log else "  (nothing yet)",
                    claims=_claims_text(claims))
                + (("\n" + ctx + "\n") if ctx else "")
                + _ARM_CONTROL[arm]
                + ("\nTHIS IS YOUR FINAL CALL. Emit your COMPLETE final claim sheet now: one "
                   f"entry for every rung 0..{campaign.n_rungs - 1}, each with its verdict and "
                   "warrant. Set stop_now to true.")
                + "\nReply with the JSON object only.")
            fr = call_fn(final_prompt, schema)
            rec.model_calls += fr.model_calls
            rec.model_tokens += fr.total_tokens or 0
            rec.wall_ms += int(fr.wall_seconds * 1000)
            if fr.ok and fr.body:
                for item in fr.body.get("claims", []) or []:
                    try:
                        cl = _ingest_claim(arm, item)
                    except (KeyError, ValueError, TypeError):
                        continue
                    if 0 <= cl.rung < campaign.n_rungs:
                        claims[cl.rung] = cl
            break
        na = body.get("next_action") or {}
        try:
            action = Action(str(na.get("tool", "local_search")), int(na.get("rung", 0)),
                            max(1, int(na.get("budget", 1000))), str(na.get("mode", "none")))
        except (ValueError, TypeError):
            st.log.append("  (malformed action ignored)")
            continue
        if meter.remaining <= 0:
            break
        res = run_action(campaign, meter, action, campaign.seed ^ (0xC0DE + turn))
        rec.actions.append(res)
        st.note(res)

    rec.claims = list(claims.values())
    rec.checks_spent = meter.spent
    return rec


# ---- deterministic arms ------------------------------------------------------------------


def run_deterministic_arm(campaign: Campaign, arm: str) -> CampaignRecord:
    rec = CampaignRecord(campaign.campaign_id, arm)
    meter = Meter(limit=campaign.budget_checks)
    st = _State(campaign)

    if arm == "C_NEVER_CLAIM":
        rec.claims = [Claim(i, "UNRESOLVED", "NONE") for i in range(campaign.n_rungs)]
        rec.checks_spent = 0
        return rec

    if arm == "C_UNIFORM_ALLOCATION":
        # The calibration arm: split the budget evenly, claim whatever a tool established,
        # and -- crucially -- claim nothing else.  This is the study's difficulty yardstick.
        per = campaign.budget_checks // campaign.n_rungs
        for i in range(campaign.n_rungs):
            if meter.remaining <= 0:
                break
            r = run_action(campaign, meter, Action("local_search", i, per // 2, "none"),
                           campaign.seed + i)
            rec.actions.append(r)
            st.note(r)
            if r.outcome == "WITNESS_FOUND":
                continue
            r2 = run_action(campaign, meter, Action("exact_solve", i, 2000, "none"),
                            campaign.seed + i)
            rec.actions.append(r2)
            st.note(r2)

    elif arm == "C_RANDOM_ALLOCATION":
        rng = random.Random(campaign.seed ^ 0x5EED)
        while meter.remaining > 0 and len(rec.actions) < 40:
            tool = rng.choice(["local_search", "exact_solve"])
            r = run_action(campaign, meter,
                           Action(tool, rng.randrange(campaign.n_rungs),
                                  max(1, campaign.budget_checks // 20), "none"),
                           campaign.seed + len(rec.actions))
            rec.actions.append(r)
            st.note(r)

    elif arm == "B5_ALGORITHMIC_CORE_NO_MODEL":
        # Portfolio + binary search + Luby restarts + version space + abstention, in code.
        budgets = luby_budgets(campaign.budget_checks // 2, 12)
        bi = 0
        stuck: set[int] = set()
        while meter.remaining > 0 and bi < len(budgets):
            # round-robin over blocks that still have an open bracket
            probe = None
            for b in sorted(st.local):
                if b in stuck:
                    continue
                nxt = st.bisect[b].next_probe()
                if nxt is not None:
                    probe = st.local[b][nxt]
                    blk = b
                    break
            if probe is None:
                break
            feat = RungFeatures(probe, campaign.rungs[probe].n_vars,
                                campaign.rungs[probe].clause_count)
            tool = portfolio_select(feat)
            r = run_action(campaign, meter, Action(tool, probe, budgets[bi], "none"),
                           campaign.seed + bi)
            rec.actions.append(r)
            st.note(r)
            if r.outcome == "INCONCLUSIVE" and meter.remaining > 0:
                other = "exact_solve" if tool == "local_search" else "local_search"
                r2 = run_action(campaign, meter, Action(other, probe, budgets[bi], "none"),
                                campaign.seed + 100 + bi)
                rec.actions.append(r2)
                st.note(r2)
                if r2.outcome == "INCONCLUSIVE":
                    # Neither tool settled this probe; this block's bracket cannot be
                    # advanced, so move to another block rather than burn budget here.
                    stuck.add(blk)
            bi += 1
    else:
        raise ValueError(f"unregistered deterministic arm: {arm}")

    # Claim exactly what the version space entails -- never more.
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

    rec.checks_spent = meter.spent
    return rec


def run_arm(campaign: Campaign, arm: str, **kw: Any) -> CampaignRecord:
    if arm in MODEL_ARMS:
        return run_model_arm(campaign, arm, **kw)
    return run_deterministic_arm(campaign, arm)
