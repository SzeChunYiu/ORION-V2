#!/usr/bin/env python3
"""E30 R11 sensitivity stage 1: audit diffs (arm-blind) + build syntax workdirs.

Per rep R:
  - runs the frozen audit over confirmatory-rR/responses (via subprocess to the
    frozen scripts/audit_orion_diff_interface.py from campaign source)
  - writes run/sensitivity/audit-rR.json and canonical patches under
    run/sensitivity/canonical-rR/
  - builds run/confirmatory-syntax-rR/ with responses whose unified diff is
    replaced by the canonical text ONLY where canonical_sha256 != original_sha256
  - copies raw evaluation JSONs for unchanged tasks (byte-identical inputs)
  - writes run/sensitivity/syntax-workdir-manifest-rR.json
"""
import json, hashlib, os, shutil, subprocess, sys, datetime
from pathlib import Path

CAMP = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6")
RUN = CAMP / "run"
SRC = CAMP / "source"
PY = RUN / "venv/bin/python"
REPS = ["1", "2", "3"]
SENS = RUN / "sensitivity"

def main() -> int:
    SENS.mkdir(parents=True, exist_ok=True)
    summary = {"schema_version": "orion.v2.e30-r11.syntax-workdir-build.v1",
               "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "reps": {}}
    for R in REPS:
        raw_wd = RUN / f"confirmatory-r{R}"
        syn_wd = RUN / f"confirmatory-syntax-r{R}"
        audit_out = SENS / f"audit-r{R}.json"
        canonical_dir = SENS / f"canonical-r{R}"
        # 1. frozen audit (arm-blind, gold-blind)
        proc = subprocess.run(
            [str(PY), str(SRC / "scripts/audit_orion_diff_interface.py"),
             "--workdir", str(raw_wd), "--output", str(audit_out),
             "--canonical-dir", str(canonical_dir)],
            cwd=str(SRC), capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"AUDIT FAILED r{R}: {proc.stderr}", file=sys.stderr)
            return 1
        audit = json.loads(audit_out.read_text())
        # 2. build syntax workdir
        if syn_wd.exists():
            shutil.rmtree(syn_wd)
        (syn_wd / "responses").mkdir(parents=True)
        shutil.copyfile(raw_wd / "frozen_tasks.json", syn_wd / "frozen_tasks.json")
        changed, unchanged_no_diff, unchanged_identical = [], [], []
        for row in audit["rows"]:
            arm, task = row["arm_id"], row["task_id"]
            src_resp = raw_wd / "responses" / arm / f"{task}.json"
            dst_resp = syn_wd / "responses" / arm / f"{task}.json"
            dst_resp.parent.mkdir(parents=True, exist_ok=True)
            canon_sha = row.get("canonical_sha256")
            orig_sha = row.get("original_sha256")
            if canon_sha and orig_sha and canon_sha != orig_sha:
                d = json.loads(src_resp.read_text())
                a = d.get("proposed_patch_or_artifact")
                canonical_text = (canonical_dir / arm / f"{task}.patch").read_text()
                if isinstance(a, dict):
                    a["content"] = canonical_text
                else:
                    d["proposed_patch_or_artifact"] = canonical_text
                dst_resp.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")
                changed.append({"arm_id": arm, "task_id": task,
                                "interface_status": row["interface_status"]})
            else:
                shutil.copyfile(src_resp, dst_resp)
                if orig_sha is None:
                    unchanged_no_diff.append(f"{arm}/{task}")
                else:
                    unchanged_identical.append(f"{arm}/{task}")
                # copy raw evaluation for unchanged tasks (byte-identical patch input)
                raw_ev = raw_wd / "evaluations" / arm / f"{task}.json"
                if raw_ev.exists():
                    dst_ev = syn_wd / "evaluations" / arm / f"{task}.json"
                    dst_ev.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(raw_ev, dst_ev)
        manifest = {
            "rep": R, "audit_output": str(audit_out), "canonical_dir": str(canonical_dir),
            "audit_counts": audit["counts"],
            "changed_response_count": len(changed), "changed": changed,
            "unchanged_identical_count": len(unchanged_identical),
            "unchanged_no_diff_count": len(unchanged_no_diff),
            "copied_raw_evaluation_count": len(list((syn_wd / "evaluations").glob("*/*.json"))) if (syn_wd / "evaluations").exists() else 0,
        }
        (SENS / f"syntax-workdir-manifest-r{R}.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        summary["reps"][f"r{R}"] = manifest
        print(f"r{R}: audit={audit[\"counts\"]} changed={len(changed)}")
    (SENS / "syntax-workdir-build-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    taskmap = []
    for R in REPS:
        for item in summary["reps"][f"r{R}"]["changed"]:
            taskmap.append({"repeat": R, "arm": item["arm_id"], "task": item["task_id"]})
    (SENS / "syntax-eval-taskmap.json").write_text(json.dumps(taskmap, indent=2, sort_keys=True) + "\n")
    print("syntax-eval-taskmap size:", len(taskmap))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
