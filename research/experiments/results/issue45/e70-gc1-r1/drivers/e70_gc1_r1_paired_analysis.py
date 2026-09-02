#!/usr/bin/env python3
"""E70-GC1 R1 task-level paired analysis (E30-R11 conventions).

Unit = frozen task (24). Exact two-sided discordant (sign) test per contrast, Holm
step-down over the registered family {F2 vs F0, F2 vs SIMPLE_DIRECT, F2 vs
SAME_MODEL_REFLECTION}. Endpoints are read verbatim from the pilot's evaluation
records; nothing is re-scored. Descriptive contrasts outside the family are
labelled as such and receive no correction.
"""
from __future__ import annotations
import json, math, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
F2 = "F2_ORION_METABOLIC_FULL"
CONTROLS = ["F0_PARENT_FEDERATION", "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"]
ARMS = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", F2]
ENDPOINTS = {
    "raw_hidden_oracle_success": "PRIMARY (registered): raw emitted diff applies and passes all 96 hidden cases",
    "raw_patch_apply_success": "SECONDARY: raw emitted diff applies under git apply",
    "syntax_normalized_hidden_oracle_success": "SECONDARY: hidden-oracle success after syntax-only canonicalization (E20 protocol; semantic repair forbidden)",
}

def exact_two_sided(left: int, right: int) -> float | None:
    n = left + right
    if n == 0:
        return None
    tail = min(left, right)
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(tail + 1)) / 2 ** n)

def holm(ps: list[float | None]) -> list[float | None]:
    idx = [i for i, p in enumerate(ps) if p is not None]
    idx.sort(key=lambda i: ps[i])
    out: list[float | None] = [None] * len(ps)
    m, running = len(idx), 0.0
    for rank, i in enumerate(idx):
        running = max(running, min(1.0, (m - rank) * ps[i]))
        out[i] = running
    return out

def main() -> int:
    rollup = json.loads((HERE / "E70_GC1_R1_EVALUATION_ROLLUP.json").read_text())
    ev = {(r["arm_id"], r["task_id"]): r for r in rollup["records"]}
    tasks = sorted({t for _, t in ev})
    assert len(tasks) == 24 and len(ev) == 96, (len(tasks), len(ev))
    out = {"schema_version": "orion.v2.issue45.e70-gc1.paired-analysis.v1", "run_id": "e70-gc1-r1",
           "analysis_unit": "frozen task (24)", "test": "exact two-sided discordant (sign) test",
           "correction": "Holm step-down, family size 3 (F2 vs each control) per endpoint",
           "alpha": 0.05, "endpoints": {}}
    for ep, desc in ENDPOINTS.items():
        g = lambda a, t: bool(ev[(a, t)].get(ep))
        counts = {a: sum(g(a, t) for t in tasks) for a in ARMS}
        fam = []
        for c in CONTROLS:
            l = sum(g(F2, t) and not g(c, t) for t in tasks)
            r = sum(g(c, t) and not g(F2, t) for t in tasks)
            both = sum(g(F2, t) and g(c, t) for t in tasks)
            fam.append({"left_arm": F2, "right_arm": c, "both_true": both, "both_false": 24 - both - l - r,
                        "left_only": l, "right_only": r, "risk_difference": (counts[F2] - counts[c]) / 24,
                        "exact_p": exact_two_sided(l, r)})
        for row, hp in zip(fam, holm([x["exact_p"] for x in fam])):
            row["holm_p"] = hp
            row["reject_at_0_05"] = bool(hp is not None and hp < 0.05)
        desc_rows = []
        for c in ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"]:
            l = sum(g("F0_PARENT_FEDERATION", t) and not g(c, t) for t in tasks)
            r = sum(g(c, t) and not g("F0_PARENT_FEDERATION", t) for t in tasks)
            desc_rows.append({"left_arm": "F0_PARENT_FEDERATION", "right_arm": c, "left_only": l, "right_only": r,
                              "exact_p_uncorrected_descriptive_only": exact_two_sided(l, r)})
        per_task = {t: sum(g(a, t) for a in ARMS) for t in tasks}
        out["endpoints"][ep] = {"description": desc, "arm_counts_of_24": counts, "registered_family": fam,
                                "descriptive_outside_family": desc_rows,
                                "tasks_by_number_of_arms_succeeding": dict(sorted(Counter(per_task.values()).items())),
                                "tasks_no_arm_succeeds": [t for t in tasks if per_task[t] == 0]}
    # failure ledger per arm on the primary endpoint
    ledger = {}
    for a in ARMS:
        c = Counter()
        for t in tasks:
            e = ev[(a, t)]
            if e["raw_hidden_oracle_success"]:
                c["SUCCESS_EXACT_HUNK_HEADER"] += 1
            elif not e["raw_patch_apply_success"]:
                c["HUNK_HEADER_OVERCOUNT_GIT_APPLY_CORRUPT_PATCH"] += 1
            elif e["raw_hidden_accuracy"] == 0:
                c["HUNK_HEADER_UNDERCOUNT_SILENT_TRUNCATION_ZERO_ACCURACY"] += 1
            else:
                c["HUNK_HEADER_UNDERCOUNT_SILENT_TRUNCATION_PARTIAL_ACCURACY"] += 1
        ledger[a] = {"ledger": dict(c),
                     "syntax_canonicalization_changed": sum(ev[(a, t)]["syntax_audit_status"] == "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION" for t in tasks),
                     "success_iff_header_unchanged": all((ev[(a, t)]["syntax_audit_status"] == "VALID_UNCHANGED") == bool(ev[(a, t)]["raw_hidden_oracle_success"]) for t in tasks),
                     "model_tokens_total": sum(ev[(a, t)]["model_tokens"] or 0 for t in tasks),
                     "model_tokens_median": sorted(ev[(a, t)]["model_tokens"] or 0 for t in tasks)[12],
                     "model_wall_time_seconds_total": round(sum(ev[(a, t)]["model_wall_time_seconds"] or 0 for t in tasks), 1),
                     "patch_size_bytes_total": sum(ev[(a, t)]["patch_size_bytes"] for t in tasks)}
    out["primary_endpoint_failure_ledger"] = ledger
    n = 9
    out["power_note"] = {"discordant_pairs_F2_vs_F0": n,
                         "smallest_two_sided_p_attainable_with_9_discordants": exact_two_sided(0, 9),
                         "split_needed_to_reject_at_0_05_with_9_discordants": "1 vs 8 (p=0.039) or more extreme; the observed 2 vs 7 gives p=0.180",
                         "reading": "24 paired tasks can reject only near-total one-sided dominance; this pilot is not powered to detect moderate arm differences"}
    (HERE / "E70_GC1_R1_PAIRED_ANALYSIS.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({ep: [(r["right_arm"], r["left_only"], r["right_only"], r["exact_p"], r["holm_p"]) for r in v["registered_family"]] for ep, v in out["endpoints"].items()}, indent=1))
    print(json.dumps({a: v["ledger"] | {"iff": v["success_iff_header_unchanged"]} for a, v in ledger.items()}, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())
