#!/usr/bin/env python3
"""E30 R11 sensitivity rollup: raw (primary) vs syntax-normalized (secondary).

Reads per-rep raw evaluations, syntax workdir evaluations, audit reports;
produces per-arm per-rep paired comparison with per-task pairing and flips.
Writes campaign/E30_R11_SYNTAX_SENSITIVITY_ROLLUP.json.
"""
import json, os, datetime
from collections import defaultdict, Counter

CAMP = "/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
RUN = os.path.join(CAMP, "run")
SENS = os.path.join(RUN, "sensitivity")
REPS = ["1", "2", "3"]
ARMS = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]

def load(p):
    return json.load(open(p))

def succ(ev):
    if ev is None:
        return "MISSING"
    return bool(ev.get("native_success"))

rollup = {
    "schema_version": "orion.v2.e30-r11.syntax-sensitivity-rollup.v1",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authority": "SENSITIVITY_ONLY_NO_PRIMARY_OUTCOME_AUTHORITY",
    "raw_is_primary": True,
    "per_rep": {}, "per_arm_totals": {}, "flips": {}, "interface_status_counts": {},
    "missing_syntax_evaluations": [],
}
flips_detail = []
for R in REPS:
    audit = load(os.path.join(SENS, f"audit-r{R}.json"))
    rollup["interface_status_counts"]["r" + R] = audit["counts"]
    per_arm = {}
    for arm in ARMS:
        raw_dir = os.path.join(RUN, f"confirmatory-r{R}", "evaluations", arm)
        syn_dir = os.path.join(RUN, f"confirmatory-syntax-r{R}", "evaluations", arm)
        raw_pass = syn_pass = n = 0
        for f in sorted(os.listdir(raw_dir)):
            if not f.endswith(".json"):
                continue
            n += 1
            task = f[:-5]
            raw_ev = load(os.path.join(raw_dir, f))
            syn_path = os.path.join(syn_dir, f)
            syn_ev = load(syn_path) if os.path.exists(syn_path) else None
            if syn_ev is None:
                rollup["missing_syntax_evaluations"].append(f"r{R}/{arm}/{task}")
            rs, ss = succ(raw_ev), succ(syn_ev)
            if rs is True:
                raw_pass += 1
            if ss is True:
                syn_pass += 1
            if rs != ss:
                flips_detail.append({"rep": R, "arm_id": arm, "task_id": task,
                                     "raw_native_success": rs, "syntax_native_success": ss})
        per_arm[arm] = {
            "task_count": n,
            "raw_native_success_count": raw_pass,
            "syntax_normalized_native_success_count": syn_pass,
            "delta": syn_pass - raw_pass,
        }
    rollup["per_rep"]["r" + R] = per_arm
for arm in ARMS:
    raw_t = syn_t = 0
    for R in REPS:
        m = rollup["per_rep"]["r" + R][arm]
        raw_t += m["raw_native_success_count"]
        syn_t += m["syntax_normalized_native_success_count"]
    rollup["per_arm_totals"][arm] = {
        "raw_total_over_120": raw_t,
        "syntax_normalized_total_over_120": syn_t,
        "delta": syn_t - raw_t,
    }
rollup["flips"] = {"count": len(flips_detail), "detail": flips_detail}
out = os.path.join(CAMP, "E30_R11_SYNTAX_SENSITIVITY_ROLLUP.json")
with open(out, "w") as f:
    json.dump(rollup, f, indent=2, sort_keys=True)
    f.write("\n")
print("wrote", out)
print(json.dumps(rollup["per_arm_totals"], indent=1))
