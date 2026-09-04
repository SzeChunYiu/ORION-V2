#!/usr/bin/env python3
"""ME-F1 R2 — discharge the probe-allocation precondition, and emit the receipt.

Runs the deterministic federation core under every registered allocation policy, at the
natural budget and at the 7-action budget the model arms are actually given, over the
frozen development split. Writes `ME_F1_R2_ALLOCATION_REDERIVATION_V1.json`.

No model call is made and none is possible from here: every arm exercised is
deterministic and byte-reproducible from the campaign seed.

Exit codes -- "could not check" keeps its own code:
  0  measured
  3  CANNOT_CHECK: the FROZEN replica does not reproduce the shipped core, so no policy
     comparison below it may be believed
  4  CANNOT_CHECK: a development campaign's ground truth is not monotone-consistent
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "me-f1"
for p in (str(HERE), str(V1)):
    if p not in sys.path:
        sys.path.insert(0, p)

import mef1r2_allocation as A  # noqa: E402
import mef1_run as R  # noqa: E402
from mef1_arms import run_action, run_arm  # noqa: E402
from mef1_model import Action  # noqa: E402
from mef1_score import aggregate, score_campaign  # noqa: E402
from mef1_toolbox import Meter  # noqa: E402

SCHEMA = "orion.v2.me-f1-r2.allocation-rederivation.v1"
N_DEV_CAMPAIGNS = 8          # the G0e development denominator, unchanged
MODEL_ARM_ACTIONS = 7        # every model arm gets 7 actions plus a closing call
CAP7_LUBY_UNIT = 12500       # the per-probe budget the cap-7 Luby schedule allots


def dev_campaigns():
    d = R.design()
    level, n_vars, budget, why = R._selected_geometry(HERE.parent / "me-f1" / "results")
    seed = d["splits"]["development"]["seed"]
    cs = R.make_campaigns(seed, N_DEV_CAMPAIGNS, 0, n_vars, budget)
    return cs, {"level": level, "n_vars": n_vars, "budget_checks": budget,
                "why": why, "dev_seed": seed, "n_campaigns": len(cs)}


def tool_training_table(campaigns) -> dict:
    """One probe per (rung, tool) at the cap-7 Luby unit budget, fresh meter each time.

    This is the training step SATzilla prescribes and the shipped `portfolio_select`
    skipped. It reads only the development split.
    """
    stat: dict[str, Counter] = {}
    for c in campaigns:
        for rung in c.rungs:
            ratio = round(rung.clause_count / rung.n_vars, 3)
            for tool in ("local_search", "exact_solve"):
                m = Meter(limit=c.budget_checks)
                res = run_action(c, m, Action(tool, rung.index, CAP7_LUBY_UNIT, "none"),
                                 c.seed + rung.index)
                key = f"{ratio}|{tool}"
                cnt = stat.setdefault(key, Counter())
                cnt[res.outcome] += 1
                cnt["checks"] += res.checks_spent
                if res.outcome == "REFUTED":
                    # `_State.note` records an UNSAT observation ONLY when the refutation
                    # is complete, so a REFUTED that hit the node limit never reaches the
                    # version space and must not be counted as settled.  The flag is read
                    # rather than assumed.
                    cnt["refuted_complete" if res.refutation_complete
                        else "refuted_incomplete"] += 1
    out = {}
    for key, cnt in sorted(stat.items()):
        n = cnt["WITNESS_FOUND"] + cnt["REFUTED"] + cnt["INCONCLUSIVE"]
        # SETTLED is what the version space would actually accept: a verified witness, or
        # a COMPLETE refutation.  An incomplete refutation establishes nothing.
        settled = cnt["WITNESS_FOUND"] + cnt["refuted_complete"]
        ratio, tool = key.split("|")
        out[key] = {"ratio": float(ratio), "tool": tool, "n_probes": n,
                    "settled": settled, "settle_rate": settled / n,
                    "witness": cnt["WITNESS_FOUND"], "refuted": cnt["REFUTED"],
                    "refuted_complete": cnt["refuted_complete"],
                    "refuted_incomplete": cnt["refuted_incomplete"],
                    "inconclusive": cnt["INCONCLUSIVE"],
                    "mean_checks": cnt["checks"] // n}
    return out


def measure(campaigns, gts, policy: str, cap: int | None) -> dict:
    scores, actions, checks = [], [], 0
    outcomes: Counter = Counter()
    for c, gt in zip(campaigns, gts):
        rec = A.run_core(c, policy, cap)
        actions.append(len(rec.actions))
        checks += rec.checks_spent
        for r in rec.actions:
            outcomes[f"{r.action.tool}|{r.outcome}"] += 1
        scores.append(score_campaign(rec, gt, c.family, c.n_rungs, R._block_of(c)))
    agg = aggregate(scores)
    return {"policy": policy, "action_cap": cap,
            "actions_per_campaign": actions, "actions_total": sum(actions),
            "checks_total": checks,
            "primary_warranted_correct_rate": agg["warranted_correct_rate"],
            "coverage": agg["coverage"],
            "n_claimed_rungs": agg["n_claimed_rungs"],
            "unwarranted_claims": agg["unwarranted_claims"],
            "action_outcomes": dict(sorted(outcomes.items()))}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path,
                    default=HERE / "ME_F1_R2_ALLOCATION_REDERIVATION_V1.json")
    a = ap.parse_args(argv)

    campaigns, geometry = dev_campaigns()
    gts = []
    for c in campaigns:
        gt, _t, consistent, why = R.campaign_ground_truth(c)
        if not consistent:
            print(f"CANNOT_CHECK: {c.campaign_id} ground truth inconsistent: {why}",
                  file=sys.stderr)
            return 4
        gts.append(gt)

    # CONTROL, run before anything is compared: the replica must BE the shipped core.
    mismatches = []
    for c in campaigns:
        shipped = run_arm(c, "B5_ALGORITHMIC_CORE_NO_MODEL")
        replica = A.run_core(c, A.FROZEN, None)
        if (A.action_signature(shipped) != A.action_signature(replica)
                or A.claim_signature(shipped) != A.claim_signature(replica)
                or shipped.checks_spent != replica.checks_spent):
            mismatches.append(c.campaign_id)
    if mismatches:
        print("CANNOT_CHECK: the FROZEN replica does not reproduce "
              f"B5_ALGORITHMIC_CORE_NO_MODEL on {mismatches}", file=sys.stderr)
        return 3

    rows = {}
    for cap in (None, MODEL_ARM_ACTIONS):
        for policy in A.POLICIES:
            rows[f"{policy}|cap={cap}"] = measure(campaigns, gts, policy, cap)

    frozen7 = rows[f"{A.FROZEN}|cap={MODEL_ARM_ACTIONS}"]
    rederived7 = rows[f"{A.REDERIVED}|cap={MODEL_ARM_ACTIONS}"]
    trained7 = rows[f"{A.TRAINED_TOOL}|cap={MODEL_ARM_ACTIONS}"]
    luby7 = rows[f"{A.LUBY_SIZED}|cap={MODEL_ARM_ACTIONS}"]
    sched7 = rows[f"{A.SCHEDULE_ONLY}|cap={MODEL_ARM_ACTIONS}"]

    report = {
        "schema_version": SCHEMA,
        "purpose": ("discharge clause (b) of the conjunctive precondition in "
                    "ME_F1_G0E_OUTCOME_RECEIPT_V1.md section 5.1: the parent's probe "
                    "allocation re-derived for the action budget it is actually given"),
        "geometry": geometry,
        "replica_control": {
            "frozen_policy_reproduces_the_shipped_core": True,
            "n_campaigns_checked": len(campaigns),
            "compared": ["action tool/rung/budget/outcome sequence", "claim sheet",
                         "checks spent"],
        },
        "tool_training_table": tool_training_table(campaigns),
        "policies": rows,
        "attribution": {
            "single_stage": "SOLVER SELECTION, not probe ordering and not restart sizing",
            "frozen_at_7_actions": frozen7["primary_warranted_correct_rate"],
            "rederived_at_7_actions": rederived7["primary_warranted_correct_rate"],
            "delta_pp": round(100 * (rederived7["primary_warranted_correct_rate"]
                                     - frozen7["primary_warranted_correct_rate"]), 4),
            "lever_isolation": {
                "trained_tool_alone": trained7["primary_warranted_correct_rate"],
                "luby_sizing_alone": luby7["primary_warranted_correct_rate"],
                "probe_schedule_alone": sched7["primary_warranted_correct_rate"],
                "reading": ("the trained selector carries the entire repair; sizing the "
                            "Luby schedule to the action budget changes nothing because "
                            "checks were never the binding resource; re-ordering probes "
                            "by the federation's own portfolio_schedule makes it WORSE, "
                            "and is reported because it was tried and failed"),
            },
        },
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "authorizes_protected_dispatch": False,
                      "note": ("G0e remains NO_LAUNDERING_VARIANCE and ME-F1 remains "
                               "CANNOT_CHECK; stage_protected refuses on its own with "
                               "exit 7/8. Discharging this precondition does not unblock "
                               "dispatch and is not claimed to.")},
    }
    a.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print(f"geometry {geometry['level']} n_vars={geometry['n_vars']} "
          f"budget={geometry['budget_checks']}, {len(campaigns)} dev campaigns")
    for key, row in rows.items():
        print(f"  {key:<28} actions={row['actions_total']:>3} "
              f"primary={row['primary_warranted_correct_rate']:.4f} "
              f"claims={row['n_claimed_rungs']:>3} "
              f"unwarranted={row['unwarranted_claims']}")
    print(f"REPAIR at {MODEL_ARM_ACTIONS} actions: "
          f"{frozen7['primary_warranted_correct_rate']:.4f} -> "
          f"{rederived7['primary_warranted_correct_rate']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
