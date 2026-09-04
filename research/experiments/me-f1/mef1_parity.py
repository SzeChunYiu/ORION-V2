"""ME-F1 arm-glue parity: does each arm's control text expose what its code can do?

Why this module exists
----------------------
`ME_F1_G0E_OUTCOME_RECEIPT_V1.md` S5.1 recorded, and explicitly did not repair, an
arm-glue fidelity gap: `B5_ALGORITHMIC_CORE_NO_MODEL` -- the same published federation
implemented in code -- falls back to the other tool when a probe returns `INCONCLUSIVE`,
while `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`'s frozen control text never told the
model to do so.  A comparator that is under-prompted relative to its own implementation
is a weakened comparator, and a win over a weakened comparator is worth nothing.

This module makes that claim mechanically checkable instead of asserted in prose, and
keeps it checkable: `check_control_text_parity` fails if the sentence is ever removed
again, and `fallback_ablation` measures what the fallback is worth at zero model cost.

Scope of the claim -- stated precisely, because the receipt's wording is looser
-----------------------------------------------------------------------------
The shared preamble `_COMMON` already tells EVERY arm that `local_search` "can never
establish unsatisfiability" and that `INCONCLUSIVE` establishes nothing.  So the
*information* was never withheld from B5, and `SIMPLE_DIRECT` reads the identical
preamble and spends 53/56 actions on `exact_solve` anyway.  What was absent from B5's
arm text is the *procedural rule*: what to DO when a probe comes back `INCONCLUSIVE`.
`M_ME_FRONTIER_CONTROL` names that rule explicitly (escalation level L2, "switch tool
class").  That asymmetry -- not the raw information -- is the fairness defect.

Exit-code discipline
--------------------
"Could not check" is never reported as "checked and fine".  Every probe below carries
its own denominator, and the no-alarm case is asserted as well as the alarm case.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent

#: Arms whose control text is required to expose the INCONCLUSIVE -> switch-tool rule
#: their own action space supports.  Both of these are comparator or mechanism arms
#: whose standing depends on being run at their strongest.
PARITY_REQUIRED_ARMS: tuple[str, ...] = (
    "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION",
    "M_ME_FRONTIER_CONTROL",
)

#: Surface forms that constitute telling an arm to change tool class.  Matched
#: case-insensitively against the arm's own control text only -- never the preamble.
_TOOL_SWITCH_FORMS: tuple[str, ...] = (
    "switch tool class",
    "switch to the other tool",
    "the other tool",
    "local_search <-> exact_solve",
)

#: The literal guard in `mef1_arms.run_deterministic_arm`'s B5 branch.  If this string
#: stops appearing, the code no longer has the capability and the parity question is
#: a different question -- which is reported as NOT_CHECKED, not as a pass.
_CODE_FALLBACK_GUARD = 'if r.outcome == "INCONCLUSIVE"'

_BRANCH_START = 'elif arm == "B5_ALGORITHMIC_CORE_NO_MODEL":'


def _b5_code_branch(source: str) -> str | None:
    """The source of the deterministic B5 branch, or None if it cannot be located."""
    i = source.find(_BRANCH_START)
    if i < 0:
        return None
    rest = source[i + len(_BRANCH_START):]
    # the branch ends at the next dedented `else:` / `elif ` at 4-space indent
    m = re.search(r"\n    (?:else:|elif )", rest)
    return rest[: m.start()] if m else rest


def check_control_text_parity() -> dict[str, Any]:
    """Compare, per arm, what the control text exposes against what the code can do.

    Returns a report carrying every probe's denominator and a three-valued verdict:
    ``PARITY`` (checked, no gap), ``GAP`` (checked, a gap is present) or
    ``NOT_CHECKED`` (the question could not be put -- never conflated with a pass).
    """
    from mef1_arms import _ARM_CONTROL, _COMMON  # noqa: PLC0415  (checked at call time)

    source = (HERE / "mef1_arms.py").read_text()
    branch = _b5_code_branch(source)

    probes: list[dict[str, Any]] = []

    # ---- control probe: the search must be able to find what is known to be there ----
    # If this fails, every absence claim below is unfounded and the whole check is void.
    preamble_states_limit = "can never establish unsatisfiability" in _COMMON
    probes.append({
        "probe": "CONTROL_preamble_states_local_search_limit",
        "must_hold": True, "observed": preamble_states_limit,
        "note": "the shared preamble already carries the INFORMATION; the claim under "
                "test is about the procedural rule, not the information",
    })

    # ---- control probe: the code capability must actually exist ----------------------
    code_has_fallback = branch is not None and _CODE_FALLBACK_GUARD in branch
    probes.append({
        "probe": "CONTROL_code_branch_locatable",
        "must_hold": True, "observed": branch is not None,
    })
    probes.append({
        "probe": "CONTROL_code_has_inconclusive_fallback",
        "must_hold": True, "observed": code_has_fallback,
        "note": f"literal guard {_CODE_FALLBACK_GUARD!r} in the deterministic B5 branch",
    })

    if not (preamble_states_limit and code_has_fallback):
        return {"verdict": "NOT_CHECKED", "arms": {},
                "n_arms_checked": 0, "n_arms_required": len(PARITY_REQUIRED_ARMS),
                "probes": probes,
                "reason": "a control probe that must hold did not hold; the parity "
                          "question was not put and no arm is reported as passing"}

    arms: dict[str, Any] = {}
    for arm in PARITY_REQUIRED_ARMS:
        text = _ARM_CONTROL.get(arm)
        if text is None:
            arms[arm] = {"status": "NOT_CHECKED", "reason": "arm not registered"}
            continue
        low = text.lower()
        forms = [f for f in _TOOL_SWITCH_FORMS if f in low]
        # The gate is whether the arm is told it may CHANGE TOOL CLASS at all.  Naming
        # the `INCONCLUSIVE` trigger by that word is reported separately and does NOT
        # gate: `M_ME_FRONTIER_CONTROL` reaches the same action through its own
        # diagnosis ladder ("L2 switch tool class") without using the word, and folding
        # the two predicates together would charge M with a defect it does not have --
        # a false alarm that would invite an edit to the mechanism arm.
        arms[arm] = {
            "status": "EXPOSED" if forms else "NOT_EXPOSED",
            "names_tool_switch_action": bool(forms),
            "names_inconclusive_trigger_by_name": "inconclusive" in low,
            "tool_switch_forms_matched": forms,
            "n_forms_matched": len(forms),
            "n_forms_probed": len(_TOOL_SWITCH_FORMS),
            "control_text_chars": len(text),
        }

    checked = [a for a, v in arms.items() if v.get("status") != "NOT_CHECKED"]
    gaps = [a for a in checked if arms[a]["status"] == "NOT_EXPOSED"]
    if len(checked) < len(PARITY_REQUIRED_ARMS):
        verdict = "NOT_CHECKED"
    else:
        verdict = "GAP" if gaps else "PARITY"
    return {"verdict": verdict, "arms": arms,
            "n_arms_checked": len(checked), "n_arms_required": len(PARITY_REQUIRED_ARMS),
            "n_gaps": len(gaps), "gap_arms": gaps, "probes": probes,
            "code_capability": "INCONCLUSIVE -> switch tool class -> if still "
                               "INCONCLUSIVE, abandon this block"}


def fallback_ablation(n_campaigns: int = 8, action_cap: int = 7) -> dict[str, Any]:
    """What the `INCONCLUSIVE` -> switch-tool fallback is worth, with no model calls.

    Two variants of `run_deterministic_arm` are built from ONE source string by two
    textual transforms.  The action cap is applied to BOTH -- so that the deterministic
    arm is measured in the same 7-action regime the model arms are given -- and the
    fallback block is removed from one.  The only behavioural difference between the two
    numbers below is therefore the fallback itself, and the function asserts that before
    it measures anything.
    """
    import difflib
    import types

    import mef1_run as R

    source = (HERE / "mef1_arms.py").read_text()

    while_old = "        while meter.remaining > 0 and bi < len(budgets):"
    while_new = ("        while (meter.remaining > 0 and bi < len(budgets)\n"
                 "               and len(rec.actions) < _ACTION_CAP):")
    branch = _b5_code_branch(source)
    if branch is None or while_old not in source:
        return {"verdict": "NOT_CHECKED",
                "reason": "the deterministic B5 branch or its loop header moved; the "
                          "ablation was not performed"}

    m = re.search(r"[ ]{12}if r\.outcome == \"INCONCLUSIVE\".*?\n(?=[ ]{12}bi \+= 1)",
                  source, re.S)
    if m is None:
        return {"verdict": "NOT_CHECKED",
                "reason": "the fallback block could not be delimited; not performed"}
    fallback = m.group(0)
    fallback_capped = fallback.replace(
        'if r.outcome == "INCONCLUSIVE" and meter.remaining > 0:',
        'if (r.outcome == "INCONCLUSIVE" and meter.remaining > 0\n'
        '                    and len(rec.actions) < _ACTION_CAP):')

    def build(name: str, strip: bool) -> tuple[types.ModuleType, str]:
        s = source.replace(while_old, while_new)
        s = s.replace(fallback, "" if strip else fallback_capped)
        lines = s.splitlines(True)
        ins = max(i for i, l in enumerate(lines) if l.startswith("from __future__")) + 1
        lines.insert(ins, f"_ACTION_CAP = {action_cap}\n")
        s = "".join(lines)
        mod = types.ModuleType(name)
        mod.__file__ = str(HERE / "mef1_arms.py")
        exec(compile(s, name, "exec"), mod.__dict__)  # noqa: S102
        return mod, s

    with_mod, src_with = build("mef1_arms__with_fallback", strip=False)
    without_mod, src_without = build("mef1_arms__without_fallback", strip=True)

    changed = [l for l in difflib.unified_diff(src_with.splitlines(),
                                               src_without.splitlines(), lineterm="", n=0)
               if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    allowed = ("INCONCLUSIVE", "other", "r2", "stuck", "st.note", "rec.actions.append",
               "run_action", "campaign.seed", "advanced", "Neither tool", "_ACTION_CAP")
    outside = [l for l in changed if not any(t in l for t in allowed)]
    if outside:
        return {"verdict": "NOT_CHECKED",
                "reason": "the two variants differ outside the fallback block",
                "unexpected_lines": outside}

    d = R.design()
    level, n_vars, budget, why = R._selected_geometry(HERE / "results")
    campaigns = R.make_campaigns(d["splits"]["development"]["seed"], n_campaigns, 0,
                                 n_vars, budget)

    out: dict[str, Any] = {}
    for label, mod in (("WITH_FALLBACK", with_mod), ("WITHOUT_FALLBACK", without_mod)):
        inc = tot = crit = 0
        tools: dict[str, int] = {}
        scores = []
        for c in campaigns:
            rec = mod.run_deterministic_arm(c, "B5_ALGORITHMIC_CORE_NO_MODEL")
            block_of = R._block_of(c)
            blocks: dict[int, list[int]] = {}
            for rung, b in block_of.items():
                blocks.setdefault(b, []).append(rung)
            # the block midpoint binary search targets: local index 2 of five rungs
            critical = {sorted(v)[2] for v in blocks.values() if len(v) > 2}
            for a in rec.actions:
                tot += 1
                inc += a.outcome == "INCONCLUSIVE"
                crit += a.action.rung in critical
                tools[a.action.tool] = tools.get(a.action.tool, 0) + 1
            gt, _, _, _ = R.campaign_ground_truth(c)
            scores.append(R.score_campaign(rec, gt, c.family, c.n_rungs, block_of))
        agg = R.aggregate(scores)
        out[label] = {
            "n_actions": tot, "n_inconclusive": inc,
            "inconclusive_rate": round(inc / tot, 4) if tot else None,
            "n_actions_on_block_critical_rung": crit,
            "tool_counts": tools,
            "primary": round(agg["warranted_correct_rate"], 4),
            "coverage": round(agg["coverage"], 4),
            "n_claimed_rungs": agg["n_claimed_rungs"],
            "unwarranted_claims": agg["unwarranted_claims"],
            "n_decided_rungs": agg["n_decided_rungs"],
        }
    return {"verdict": "MEASURED", "arm": "B5_ALGORITHMIC_CORE_NO_MODEL",
            "n_campaigns": len(campaigns), "action_cap": action_cap,
            "geometry": {"level": level, "n_vars": n_vars, "budget_checks": budget,
                         "why": why},
            "variants": out,
            "delta_lines_between_variants": len(changed)}
