#!/usr/bin/env python3
"""FM80 §9 — the executable subset of the standalone survival gate (#308 R11a).

FM80's gate (`FM80_NATURALISTIC_TRANSFER_DECISIVE_PROTOCOL_V1`) is blocked on a person: four clauses need an
independent adjudicator (§4.4, §7, §9.4, §9.7).  This module enumerates every clause of §3/§4/§9 into one of
three classes and RUNS the exact class:

  EXACT        computable from a frozen case table by arithmetic or string/set operations, no judgement
  MODEL_PROXY  a judgement a fresh-session model can render, labelled HUMAN_GATE_BYPASSED__MODEL_PROXY,
               never claimed external (design: FM80_MODEL_PROXY_ADJUDICATION_DESIGN_V1.md)
  HUMAN_ONLY   independence-from-construction of a person; not manufacturable by computation

The executor consumes a case table (one row per eligible case: domain, arm dispositions, the frozen witness
disposition, per-arm critical-fidelity flags, donor visibility flags, remoteness flags) and returns every
EXACT clause's verdict with its denominator, the paired exact tests with Holm, and the corrected sample rule
(FM80_PRE_OUTCOME_DESIGN_CORRECTION_V1: at the 10 pp bar the exact paired test needs ≥ 61 cases per domain;
below that the gate reports UNDERPOWERED_AT_REGISTERED_BAR, never a negative).  Exit codes: 0 gate computed,
2 CANNOT_CHECK (input missing / malformed) — distinct from any verdict.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

CLAUSES: dict[str, dict[str, str]] = {
    "3a": {"class": "MODEL_PROXY", "text": "question and protected decision written without the answer"},
    "3b": {"class": "MODEL_PROXY", "text": "strongest native parent method(s) named"},
    "3c": {"class": "EXACT", "text": "a candidate remote donor exists in the private key (or a prospective discovery criterion)"},
    "3d": {"class": "EXACT", "text": "donor outside the target's ordinary retrieval neighbourhood under the frozen baseline (top-K membership)"},
    "3e": {"class": "EXACT", "text": "transfer consequence nontrivial: correct handling changes the registered disposition"},
    "3f": {"class": "MODEL_PROXY", "text": "a formal or empirical witness capable of exposing a wrong transfer"},
    "3g": {"class": "EXACT", "text": "prompt-visible materials do not contain the hidden donor key / gold relation / disposition (string containment)"},
    "4.1": {"class": "EXACT", "text": "donor outside the primary field/taxonomy branch or frozen semantic neighbourhood (set membership on frozen taxonomy)"},
    "4.2": {"class": "EXACT", "text": "donor absent from top-K of the frozen lexical+dense retrieval baseline at matched budget"},
    "4.3": {"class": "EXACT", "text": "donor not named in prompt/metadata/citation neighbourhood/support files"},
    "4.4": {"class": "HUMAN_ONLY", "text": "an independent adjudicator accepts scientific relevance of the donor (proxy available, labelled)"},
    "7": {"class": "HUMAN_ONLY", "text": ">= 2 qualified adjudicators per domain who did not build the arm, blinded; third for terminal disagreements"},
    "9.1": {"class": "EXACT", "text": "A3 improves the protected decision endpoint by >= 10 pp over the frozen strongest baseline in >= 2 of 3 domains"},
    "9.2": {"class": "EXACT", "text": "paired 95% interval excludes zero after Holm for those two domains (exact paired test)"},
    "9.3": {"class": "EXACT", "text": "no increase in critical native-fidelity failures in any domain (given per-arm fidelity flags: formal domain machine-checkable; empirical flags are MODEL_PROXY inputs)"},
    "9.4": {"class": "HUMAN_ONLY", "text": "at least one winning domain contains genuinely REMOTE cases under §4 (inherits 4.4)"},
    "9.5": {"class": "EXACT", "text": "A2 does not reproduce the A3 protected-decision gain (paired exact test A3 vs A2 in the winning domains)"},
    "9.6": {"class": "EXACT", "text": "effect remains after excluding cases where the donor was inadvertently visible to the baseline or prompt (flags from 4.2/4.3)"},
    "9.7": {"class": "HUMAN_ONLY", "text": "independent adjudication finds no stronger omitted parent collapsing the residual"},
}
EXACT_CLAUSES = tuple(k for k, v in CLAUSES.items() if v["class"] == "EXACT")
MIN_PP = 10.0
ALPHA = 0.05
REGISTERED_MIN_PER_DOMAIN = 30
POWERED_MIN_PER_DOMAIN = 61   # FM80_PRE_OUTCOME_DESIGN_CORRECTION_V1 §2: 10 pp = 7 net cases at n = 70 clears Holm-first; 61 is the smallest n whose best-case exact p at 10 pp clears 0.0167


def exact_paired_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n)


def holm(pvals: dict[str, float], alpha: float = ALPHA) -> dict[str, bool]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    out, ok = {}, True
    for r, (k, p) in enumerate(items):
        ok = ok and p <= alpha / (len(items) - r)
        out[k] = ok
    return out


def best_case_exact_p_at_bar(n: int, pp: float = MIN_PP) -> float:
    net = math.ceil(n * pp / 100.0)
    return min(1.0, 2 * 0.5 ** net)


def load_case_table(path: Path) -> list[dict]:
    rows = json.loads(path.read_text())
    if not isinstance(rows, list) or not rows:
        raise SystemExit(2)
    need = {"case_id", "domain", "eligible", "witness_disposition", "dispositions", "critical_fidelity_failure", "donor_visible_to_baseline_or_prompt"}
    for r in rows:
        if not need <= set(r):
            print(f"CANNOT_CHECK: case {r.get('case_id')} lacks {sorted(need - set(r))}", file=sys.stderr)
            raise SystemExit(2)
    return rows


def preconditions(rows: list[dict]) -> dict:
    """§3c–e/§3g/§4.1–4.3 per case, exact, from the flags a case carries; a missing flag is CANNOT_CHECK for that clause."""
    out = {}
    for cl in ("3c", "3d", "3e", "3g", "4.1", "4.2", "4.3"):
        key = {"3c": "has_donor_key", "3d": "donor_outside_baseline_topk", "3e": "transfer_consequence_nontrivial", "3g": "hidden_keys_absent_from_visible_files",
               "4.1": "donor_outside_taxonomy_branch", "4.2": "donor_outside_baseline_topk", "4.3": "donor_not_named_in_visible_files"}[cl]
        vals = [r.get(key) for r in rows]
        n_known = sum(1 for v in vals if isinstance(v, bool))
        out[cl] = {"class": "EXACT", "n_cases": len(rows), "n_checkable": n_known, "n_pass": sum(1 for v in vals if v is True),
                   "status": "CANNOT_CHECK" if n_known == 0 else ("PASS_ALL" if all(v is True for v in vals if isinstance(v, bool)) else "SOME_FAIL")}
    return out


def survival_exact(rows: list[dict], baseline_rule: dict[str, str]) -> dict:
    """§9.1/9.2/9.3/9.5/9.6 from arm dispositions.  `baseline_rule[domain]` names the pre-outcome strongest of A0/A1."""
    elig = [r for r in rows if r["eligible"]]
    domains = sorted({r["domain"] for r in elig})
    per: dict[str, Any] = {}
    pvals: dict[str, float] = {}
    for d in domains:
        rs = [r for r in elig if r["domain"] == d]
        base = baseline_rule.get(d)
        if base not in ("A0", "A1"):
            per[d] = {"status": "CANNOT_CHECK_NO_BASELINE_RULE", "n": len(rs)}
            continue
        def correct(r, arm): return r["dispositions"].get(arm) == r["witness_disposition"]
        n = len(rs)
        a3 = sum(correct(r, "A3") for r in rs); bl = sum(correct(r, base) for r in rs)
        b = sum(1 for r in rs if correct(r, "A3") and not correct(r, base)); c = sum(1 for r in rs if correct(r, base) and not correct(r, "A3"))
        gain_pp = 100.0 * (a3 - bl) / n if n else 0.0
        p = exact_paired_two_sided(b, c); pvals[d] = p
        fid3 = sum(bool((r["critical_fidelity_failure"] or {}).get("A3")) for r in rs); fidb = sum(bool((r["critical_fidelity_failure"] or {}).get(base)) for r in rs)
        a2 = sum(correct(r, "A2") for r in rs); b2 = sum(1 for r in rs if correct(r, "A3") and not correct(r, "A2")); c2 = sum(1 for r in rs if correct(r, "A2") and not correct(r, "A3"))
        clean = [r for r in rs if not r["donor_visible_to_baseline_or_prompt"]]
        a3c = sum(correct(r, "A3") for r in clean); blc = sum(correct(r, base) for r in clean)
        per[d] = {"status": "EVALUATED", "n": n, "baseline": base, "A3_correct": a3, "baseline_correct": bl, "gain_pp": gain_pp, "b": b, "c": c, "exact_p": p,
                  "meets_10pp": gain_pp >= MIN_PP, "best_case_p_at_bar": best_case_exact_p_at_bar(n),
                  "powered_at_registered_bar": n >= POWERED_MIN_PER_DOMAIN, "at_registered_minimum": n >= REGISTERED_MIN_PER_DOMAIN,
                  "fidelity_A3": fid3, "fidelity_baseline": fidb, "no_fidelity_increase": fid3 <= fidb,
                  "A2_correct": a2, "A3_vs_A2": {"b": b2, "c": c2, "exact_p": exact_paired_two_sided(b2, c2), "A2_reproduces_A3_gain": a2 >= a3},
                  "sensitivity_excluding_visible_donors": {"n_clean": len(clean), "gain_pp_clean": (100.0 * (a3c - blc) / len(clean)) if clean else None}}
    hm = holm(pvals) if pvals else {}
    winners = [d for d in domains if per[d].get("status") == "EVALUATED" and per[d]["meets_10pp"] and hm.get(d)]
    underpowered = [d for d in domains if per[d].get("status") == "EVALUATED" and not per[d]["powered_at_registered_bar"]]
    verdict = {
        "9.1": {"pass": sum(1 for d in domains if per[d].get("meets_10pp")) >= 2, "domains_meeting_10pp": [d for d in domains if per[d].get("meets_10pp")]},
        "9.2": {"pass": len(winners) >= 2, "holm": hm, "winning_domains": winners},
        "9.3": {"pass": all(per[d]["no_fidelity_increase"] for d in domains if per[d].get("status") == "EVALUATED")},
        "9.5": {"pass": all(not per[d]["A3_vs_A2"]["A2_reproduces_A3_gain"] for d in winners) if winners else None, "note": "evaluated on winning domains only"},
        "9.6": {"pass": all((per[d]["sensitivity_excluding_visible_donors"]["gain_pp_clean"] or 0) >= MIN_PP for d in winners) if winners else None},
        "power": {"underpowered_domains_at_registered_bar": underpowered, "rule": f">= {POWERED_MIN_PER_DOMAIN} eligible cases per domain for the 10 pp bar under the exact paired test + Holm (pre-outcome correction); registered minimum {REGISTERED_MIN_PER_DOMAIN} is jointly unsatisfiable with 9.1+9.2"},
    }
    exact_all = all(bool(verdict[k]["pass"]) for k in ("9.1", "9.2", "9.3")) and verdict["9.5"]["pass"] is True and verdict["9.6"]["pass"] is True
    if any(per[d].get("status") != "EVALUATED" for d in domains) or not domains:
        terminal = "CANNOT_CHECK"
    elif underpowered and not exact_all:
        terminal = "UNDERPOWERED_AT_REGISTERED_BAR"
    elif exact_all:
        terminal = "EXACT_SUBSET_PASS__HUMAN_CLAUSES_4.4_7_9.4_9.7_PENDING"
    else:
        terminal = "EXACT_SUBSET_FAIL"
    return {"per_domain": per, "clauses": verdict, "terminal": terminal, "human_only_remainder": [k for k, v in CLAUSES.items() if v["class"] == "HUMAN_ONLY"],
            "model_proxy_clauses": [k for k, v in CLAUSES.items() if v["class"] == "MODEL_PROXY"]}


def planted_and_no_alarm() -> dict:
    """Self-test: a planted positive table at n = 70/domain must pass the exact subset; the same table at
    n = 30/domain must report UNDERPOWERED (not a negative); a null table must FAIL 9.1; a fidelity
    regression must fail 9.3; and a table where A2 reproduces A3 must fail 9.5."""
    import random
    def table(n, gain, fid3=0, a2_equal=False, seed=1):
        rng = random.Random(seed); rows = []
        for d in ("FORMAL", "EMP1", "EMP2"):
            for i in range(n):
                a3 = i < int(n * (0.6 + gain)); a0 = i < int(n * 0.6)
                a2 = a3 if a2_equal else a0
                rows.append({"case_id": f"{d}-{i}", "domain": d, "eligible": True, "witness_disposition": "TRANSFER",
                             "dispositions": {"A3": "TRANSFER" if a3 else "BLOCK_TRANSFER", "A0": "TRANSFER" if a0 else "BLOCK_TRANSFER", "A1": "BLOCK_TRANSFER", "A2": "TRANSFER" if a2 else "BLOCK_TRANSFER"},
                             "critical_fidelity_failure": {"A3": i < fid3, "A0": False}, "donor_visible_to_baseline_or_prompt": False})
        return rows
    br = {"FORMAL": "A0", "EMP1": "A0", "EMP2": "A0"}
    pos70 = survival_exact(table(70, 0.15), br); pos30 = survival_exact(table(30, 0.10), br)
    null = survival_exact(table(70, 0.0), br); fid = survival_exact(table(70, 0.15, fid3=5), br); a2 = survival_exact(table(70, 0.15, a2_equal=True), br)
    return {"planted_positive_n70_passes_exact_subset": pos70["terminal"].startswith("EXACT_SUBSET_PASS"),
            "registered_minimum_n30_at_bar_is_underpowered_not_negative": pos30["terminal"] == "UNDERPOWERED_AT_REGISTERED_BAR" and pos30["clauses"]["9.1"]["pass"] and not pos30["clauses"]["9.2"]["pass"],
            "null_table_fails_9_1": not null["clauses"]["9.1"]["pass"] and null["terminal"] in ("EXACT_SUBSET_FAIL",),
            "fidelity_regression_fails_9_3": not fid["clauses"]["9.3"]["pass"],
            "a2_reproduction_fails_9_5": fid["clauses"]["9.5"]["pass"] is not False and a2["clauses"]["9.5"]["pass"] is False,
            "best_case_p_at_bar_n30": best_case_exact_p_at_bar(30), "best_case_p_at_bar_n61": best_case_exact_p_at_bar(61),
            **_precondition_controls()}


def _precondition_controls() -> dict:
    """No-alarm and vacuity controls for the precondition reader (#308 R11b).

    The 2026-09-06 correction makes an ABSENT donor-key field report CANNOT_CHECK instead of a rejection.  A
    fix that achieved this by never reporting a failure would be worse than the mislabel it removes, so the
    genuine-False case is asserted here too: the gate must still say SOME_FAIL when a case really carries a
    checked negative.
    """
    base = {"case_id": "X", "domain": "D", "eligible": None, "witness_disposition": None, "dispositions": {},
            "critical_fidelity_failure": {}, "donor_visible_to_baseline_or_prompt": None}
    absent = preconditions([{**base, "has_donor_key": None}])
    real_false = preconditions([{**base, "has_donor_key": False}])
    real_true = preconditions([{**base, "has_donor_key": True}])
    mixed = preconditions([{**base, "has_donor_key": True}, {**base, "has_donor_key": False}])
    return {
        "absent_donor_key_field_is_cannot_check_not_a_rejection":
            absent["3c"]["status"] == "CANNOT_CHECK" and absent["3c"]["n_checkable"] == 0,
        "no_alarm_a_genuine_false_still_reports_some_fail":
            real_false["3c"]["status"] == "SOME_FAIL" and real_false["3c"]["n_checkable"] == 1,
        "a_genuine_true_reports_pass_all":
            real_true["3c"]["status"] == "PASS_ALL" and real_true["3c"]["n_pass"] == 1,
        "a_mixed_table_reports_some_fail_with_its_denominator":
            mixed["3c"]["status"] == "SOME_FAIL" and mixed["3c"]["n_checkable"] == 2 and mixed["3c"]["n_pass"] == 1,
        "sd80_token_mapping_pass_fail_pending":
            tri_from_sd80_item("PASS") is True
            and tri_from_sd80_item("PASS_BY_CONSTRUCTION") is True
            and tri_from_sd80_item("FAIL_NO_OUTCOME_FREE_CONTRACT") is False
            and tri_from_sd80_item("NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY") is None
            and tri_from_sd80_item(None) is None,
    }


SD80_ELIGIBILITY_ITEM_FOR_FLAG = {
    "has_donor_key": "c_remote_donor_known_or_prospective_criterion",
    "donor_outside_baseline_topk": "d_donor_outside_local_retrieval_neighbourhood",
    "transfer_consequence_nontrivial": "e_transfer_consequence_nontrivial",
    "hidden_keys_absent_from_visible_files": "g_visible_materials_free_of_hidden_key",
}
# The eligibility items SD80 actually evaluates on its own records, i.e. the clauses whose inputs exist in
# this pool.  §3c/d/e and §4 remoteness are NOT among them: SD80 records them as NOT_APPLICABLE…PENDING.
SD80_CLAUSE_SCOPE_NOTES = {
    "3g": ("SD80's g_visible_materials_free_of_hidden_key covers the DISPOSITION/verdict-leak component of "
           "§3g only (is the registered answer absent from the visible materials). §3g's donor-key and "
           "gold-relation components remain unevaluable on this pool because no donor key exists, so a "
           "SOME_FAIL/PASS here is partial evidence on one component, never the whole clause."),
}
SD80_CHECKABLE_ELIGIBILITY_ITEMS = (
    "a_question_and_decision_written_without_answer",
    "b_strongest_native_parent_named",
    "f_witness_exposes_wrong_decision",
    "g_visible_materials_free_of_hidden_key",
)


def tri_from_sd80_item(value: Any) -> bool | None:
    """SD80 eligibility tokens -> tri-state.  PASS* is True, FAIL* is False, and NOT_APPLICABLE/PENDING is
    None, i.e. CANNOT_CHECK.  The distinction is the point: a clause whose input does not exist in the pool
    is unevaluable, never a checked rejection (#308 R11b)."""
    if not isinstance(value, str):
        return None
    if value.startswith("PASS"):
        return True
    if value.startswith("FAIL"):
        return False
    return None


def case_table_from_sd80(path: Path) -> list[dict]:
    """The SD80 case-matrix intake as an FM80 case table.

    Every donor-dependent flag is read from the record's own `eligibility.items` through `tri_from_sd80_item`
    rather than assumed.  SD80 carries no donor key, no frozen retrieval baseline and no arm run: it records
    §3c/§3d/§3e as `NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY` on 455/455 cases, so those
    flags are None (CANNOT_CHECK).  `eligible` is None because §3a/b/f are MODEL_PROXY judgements not yet
    rendered under the frozen proxy design.

    Corrected 2026-09-06 (#308 R11b): this adapter previously hardcoded `has_donor_key = False`, which turned
    the pool's PENDING token into a checked rejection and produced the "§3c fails 455/455" reading.  The
    literal is gone; the value now comes from the record.
    """
    d = json.loads(path.read_text())
    rows = []
    for c in d["cases"]:
        items = (c.get("eligibility") or {}).get("items") or {}
        row = {"case_id": c["case_id"], "domain": c["domain"], "eligible": None, "witness_disposition": None,
               "dispositions": {}, "critical_fidelity_failure": {}, "donor_visible_to_baseline_or_prompt": None,
               "donor_outside_taxonomy_branch": None, "donor_not_named_in_visible_files": None,
               "witness_class": c.get("witness_class"), "source_record_sha256": c.get("record_sha256"),
               "sd80_eligibility_items": items}
        for flag, item in SD80_ELIGIBILITY_ITEM_FOR_FLAG.items():
            row[flag] = tri_from_sd80_item(items.get(item))
        rows.append(row)
    return rows


def sd80_eligibility_ceiling(rows: list[dict]) -> dict:
    """Per-domain ceiling on eligible cases from the clauses SD80 can actually evaluate, against the
    registered bar of 61 (#308 R11b).

    This is an upper bound and is stated as one: Stage A of the frozen proxy design marks a case INELIGIBLE
    whenever the proxy proposes no donor, so realized eligibility is <= this ceiling.  A domain whose ceiling
    is already below 61 cannot reach the registered bar no matter what Stage A returns, and the yield a
    domain would need from Stage A to reach 61 is reported for the domains that still can.
    """
    from collections import Counter, defaultdict
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_domain[r["domain"]].append(r)
    out: dict[str, Any] = {"bar_per_domain": POWERED_MIN_PER_DOMAIN, "domains": {}}
    for dom in sorted(by_domain):
        rs = by_domain[dom]
        per_item = {}
        for item in SD80_CHECKABLE_ELIGIBILITY_ITEMS:
            vals = [tri_from_sd80_item((r.get("sd80_eligibility_items") or {}).get(item)) for r in rs]
            per_item[item] = {"pass": sum(1 for v in vals if v is True),
                             "fail": sum(1 for v in vals if v is False),
                             "cannot_check": sum(1 for v in vals if v is None),
                             "fail_reasons": dict(Counter((r.get("sd80_eligibility_items") or {}).get(item)
                                                          for r in rs
                                                          if tri_from_sd80_item((r.get("sd80_eligibility_items") or {}).get(item)) is False))}
        ceiling = sum(1 for r in rs
                      if all(tri_from_sd80_item((r.get("sd80_eligibility_items") or {}).get(i)) is True
                             for i in SD80_CHECKABLE_ELIGIBILITY_ITEMS))
        reachable = ceiling >= POWERED_MIN_PER_DOMAIN
        out["domains"][dom] = {
            "n_cases": len(rs), "per_item": per_item, "checkable_ceiling": ceiling,
            "bar_reachable_before_stage_a": reachable,
            "required_stage_a_joint_yield": (round(POWERED_MIN_PER_DOMAIN / ceiling, 4) if ceiling else None),
            "status": ("CEILING_ABOVE_BAR__STAGE_A_YIELD_REQUIRED" if reachable
                       else "CEILING_BELOW_BAR__UNDERPOWERED_AT_REGISTERED_BAR_BY_ARITHMETIC"),
        }
    below = sorted(d for d, v in out["domains"].items() if not v["bar_reachable_before_stage_a"])
    out["domains_below_bar_before_stage_a"] = below
    out["reading"] = (
        "Upper bound on eligible cases per domain from the eligibility clauses SD80 evaluates on its own "
        "records. Stage A can only reduce it. Domains already below the registered bar of "
        f"{POWERED_MIN_PER_DOMAIN} cannot reach it under any Stage A outcome: {below or 'none'}."
    )
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("enumerate", "selftest", "preconditions", "survival", "sd80-preconditions", "sd80-eligibility-ceiling"))
    ap.add_argument("--sd80", type=Path)
    ap.add_argument("--cases", type=Path); ap.add_argument("--baseline-rule", type=Path); ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if a.mode == "enumerate":
        rep = {"clauses": CLAUSES, "exact": EXACT_CLAUSES, "counts": {c: sum(1 for v in CLAUSES.values() if v["class"] == c) for c in ("EXACT", "MODEL_PROXY", "HUMAN_ONLY")}}
    elif a.mode == "selftest":
        rep = planted_and_no_alarm(); rep["passed"] = all(v for k, v in rep.items() if isinstance(v, bool))
    elif a.mode == "sd80-preconditions":
        if not a.sd80:
            print("CANNOT_CHECK: --sd80 required", file=sys.stderr); return 2
        rows = case_table_from_sd80(a.sd80)
        pre = preconditions(rows)
        from collections import Counter
        rep = {"source": str(a.sd80), "n_cases": len(rows), "domains": dict(Counter(r["domain"] for r in rows)), "preconditions": pre,
               "clause_scope_notes": SD80_CLAUSE_SCOPE_NOTES,
               "reading": "FM80 §3c/3d/3e/3g and §4.1-4.3 are all CANNOT_CHECK on the SD80 pool: the records carry NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY on 455/455 for the donor clauses, so no donor-dependent clause has an input to score. Corrected 2026-09-06 (#308 R11b): §3c previously read SOME_FAIL 0/455 because the adapter hardcoded has_donor_key=False; the pool never rejected a donor, it never carried one. The exact-checkable state of the only naturalistic pool is NOT_ASSEMBLED, not negative."}
    elif a.mode == "sd80-eligibility-ceiling":
        if not a.sd80:
            print("CANNOT_CHECK: --sd80 required", file=sys.stderr); return 2
        rep = {"source": str(a.sd80), **sd80_eligibility_ceiling(case_table_from_sd80(a.sd80))}
    elif a.mode == "preconditions":
        if not a.cases:
            print("CANNOT_CHECK: --cases required", file=sys.stderr); return 2
        rep = preconditions(load_case_table(a.cases))
    else:
        if not a.cases or not a.baseline_rule:
            print("CANNOT_CHECK: --cases and --baseline-rule required", file=sys.stderr); return 2
        rep = survival_exact(load_case_table(a.cases), json.loads(a.baseline_rule.read_text()))
    text = json.dumps(rep, indent=2, sort_keys=True)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True); a.out.write_text(text + "\n")
    print(text if len(text) < 4000 else text[:4000] + "\n…")
    if a.mode == "selftest" and not rep["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
