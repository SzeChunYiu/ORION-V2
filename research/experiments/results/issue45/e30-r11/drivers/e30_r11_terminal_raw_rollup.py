#!/usr/bin/env python3
"""E30 R11 terminal raw rollup: per-arm per-rep exact counts from evaluations.

Reads run/confirmatory-r{1,2,3}/evaluations/*/*.json plus responses and writes
campaign/E30_R11_TERMINAL_RAW_ROLLUP.json. Read-only over frozen artifacts.
"""
import json, hashlib, glob, os, datetime
from collections import defaultdict, Counter

CAMP = "/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
RUN = os.path.join(CAMP, "run")
REPS = ["1", "2", "3"]
ARMS = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

rollup = {
    "schema_version": "orion.v2.e30-r11.terminal-raw-rollup.v1",
    "campaign": os.path.basename(CAMP),
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "primary": "RAW_END_TO_END_NATIVE (immutable once computed)",
    "per_rep": {}, "per_arm_totals": {}, "paired_task_table": {},
    "response_status_counts": {},
}
task_table = defaultdict(dict)  # (arm, task) -> rep -> record
for R in REPS:
    w = os.path.join(RUN, "confirmatory-r" + R)
    ev_files = sorted(glob.glob(os.path.join(w, "evaluations", "*", "*.json")))
    resp_files = sorted(glob.glob(os.path.join(w, "responses", "*", "*.json")))
    resp_status = Counter()
    per_arm = {}
    for f in resp_files:
        d = json.load(open(f))
        resp_status[str(d.get("status", "UNKNOWN"))] += 1
    for arm in ARMS:
        arm_files = sorted(glob.glob(os.path.join(w, "evaluations", arm, "*.json")))
        st = Counter(); native = 0; uncheck = 0; n = 0
        for f in arm_files:
            d = json.load(open(f)); n += 1
            st[str(d.get("status", "UNKNOWN"))] += 1
            task = os.path.basename(f)[:-5]
            rec = {
                "status": d.get("status"),
                "native_success": d.get("native_success"),
                "full_regression_suite_passed": d.get("full_regression_suite_passed"),
                "agent_status": d.get("agent_status"),
            }
            task_table[(arm, task)][R] = rec
            if d.get("native_success") is True:
                native += 1
            s = str(d.get("status", ""))
            if s.startswith("CANNOT_CHECK"):
                uncheck += 1
        per_arm[arm] = {
            "evaluation_count": n,
            "native_success_count": native,
            "cannot_check_count": uncheck,
            "status_counts": dict(st),
            "native_success_rate": (native / n) if n else None,
        }
    rollup["per_rep"]["r" + R] = {
        "response_file_count": len(resp_files),
        "response_status_counts": dict(resp_status),
        "evaluation_file_count": len(ev_files),
        "arm_metrics": per_arm,
    }

for arm in ARMS:
    tot = {"native_success": 0, "evaluations": 0, "cannot_check": 0}
    for R in REPS:
        m = rollup["per_rep"]["r" + R]["arm_metrics"][arm]
        tot["native_success"] += m["native_success_count"]
        tot["evaluations"] += m["evaluation_count"]
        tot["cannot_check"] += m["cannot_check_count"]
    tot["native_success_rate_over_120"] = tot["native_success"] / 120
    rollup["per_arm_totals"][arm] = tot

for (arm, task), reps in sorted(task_table.items()):
    rollup["paired_task_table"][arm + "/" + task] = {("r" + r): v for r, v in sorted(reps.items())}

freeze = os.path.join(CAMP, "prepared", "E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json")
rollup["freeze_sha256"] = sha(freeze) if os.path.exists(freeze) else "MISSING"
out = os.path.join(CAMP, "E30_R11_TERMINAL_RAW_ROLLUP.json")
with open(out, "w") as f:
    json.dump(rollup, f, indent=2, sort_keys=True)
    f.write("\n")
print("wrote", out)
print(json.dumps({a: rollup["per_arm_totals"][a]["native_success"] for a in ARMS}))
