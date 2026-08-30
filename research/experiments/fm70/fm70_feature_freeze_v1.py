#!/usr/bin/env python3
"""FM70 pre-outcome feature freeze V1 — read-only over frozen E30 task workdirs.

Extracts t=0-computable, arm-independent features for the 40 development tasks.
Amendment V1.1 (recorded before any selector fit):
- P02/P03 read the FAILING-TEST file, not the gold-patch-revealed buggy file
  (the patchfile metadata is not available to the solver at t=0; using it would
  leak outcome-adjacent information).
- P07 (prompt context tokens) DROPPED: prompt size differs per arm, so it is
  not an arm-independent routing feature.
- Held-out candidate pool is frozen as an ID LIST here (metadata only);
  per-task content features for held-out are extracted at Gate 1, before any
  held-out response exists.

Writes FM70_PRE_OUTCOME_FEATURES_V1.json next to this driver.
"""
import json, os, re, hashlib, datetime, glob

CAMP = "/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
WORK = os.path.join(CAMP, "evaluator_private")
BUGSINPY = os.path.join(CAMP, "baseline_lanes", "bugsinpy-ansible-1", "BugsInPy")
BUGSINPY_COMMIT = "11c5f1eea954a42132cfd06bf257766a7963e0fd"

DEF_RE = re.compile(r"^\s*(?:async\s+)?def\s+\w+|^\s*class\s+\w+", re.M)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def count_py_files(root):
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        n += sum(1 for f in filenames if f.endswith(".py"))
    return n

def features_for(workdir):
    info = {}
    with open(os.path.join(workdir, "bugsinpy_bug.info")) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                info[k] = v.strip('"')
    test_files = [t for t in info["test_file"].split(";") if t]
    srcs = [open(os.path.join(workdir, t), encoding="utf-8", errors="replace").read() for t in test_files]
    run_test = open(os.path.join(workdir, "bugsinpy_run_test.sh")).read().strip()
    # count failing test selectors (pytest node ids "path::name", possibly several)
    selectors = re.findall(r"::[\w<>\[\]]+", run_test)
    return {
        "P01_project": info.get("project") or os.path.basename(workdir).split("-")[1],
        "P02_test_file_loc": sum(s.count("\n") + 1 for s in srcs),
        "P03_test_file_def_class_count": sum(len(DEF_RE.findall(s)) for s in srcs),
        "P04_failing_test_count": max(1, len(selectors)),
        "P05_test_file_source_chars": sum(len(s) for s in srcs),
        "P06_project_python_file_count": count_py_files(workdir),
        "buggy_commit_id": info.get("buggy_commit_id"),
        "test_files": test_files,
        "run_test_sh": run_test,
        "bug_info_sha256": sha(os.path.join(workdir, "bugsinpy_bug.info")),
        "run_test_sha256": sha(os.path.join(workdir, "bugsinpy_run_test.sh")),
    }

def main():
    head = open(os.path.join(BUGSINPY, ".git", "HEAD")).read().strip()
    ref = head.split(" ", 1)
    sha_path = os.path.join(BUGSINPY, ".git", *ref[1].split("/")) if len(ref) == 2 else os.path.join(BUGSINPY, ".git", "HEAD")
    commit = open(sha_path).read().strip()
    assert commit == BUGSINPY_COMMIT, f"BugsInPy clone at {commit}, expected {BUGSINPY_COMMIT}"
    tasks = {}
    for workdir in sorted(glob.glob(os.path.join(WORK, "bugsinpy-*"))):
        task_id = os.path.basename(workdir)
        try:
            tasks[task_id] = features_for(workdir)
        except Exception as e:  # fail closed per task
            tasks[task_id] = {"extraction_error": f"{type(e).__name__}: {e}"}
    errors = {t: v for t, v in tasks.items() if "extraction_error" in v}
    dev_ids = sorted(tasks)
    # held-out candidate id list: next numeric ids per project after dev ids,
    # restricted to ids that EXIST in the BugsInPy tree at the exact commit
    by_proj = {}
    for t in dev_ids:
        proj = t.split("-")[1]
        num = int(t.split("-")[-1])
        by_proj.setdefault(proj, []).append(num)
    heldout_pool = {}
    for proj, nums in sorted(by_proj.items()):
        bugs_dir = os.path.join(BUGSINPY, "projects", proj, "bugs")
        existing = sorted(
            int(d) for d in os.listdir(bugs_dir) if d.isdigit()
        )
        used = set(nums)
        pool = [f"bugsinpy-{proj}-{i}" for i in existing if i > max(used)][:8]
        heldout_pool[proj] = pool
    out = {
        "schema_version": "orion.v2.fm70.pre-outcome-features.v1",
        "frozen_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "amendment_v1_1": "P02/P03 read the failing-test file (gold patchfile not t=0-visible); P07 dropped as arm-dependent; held-out pool frozen as id list, content features at Gate 1",
        "campaign": os.path.basename(CAMP),
        "feature_rule": "arm-independent, computable at dispatch time t=0 from the frozen task workdir; gold-patch geometry, evaluation outcomes and run telemetry excluded",
        "dev_task_count": len(dev_ids),
        "extraction_errors": errors,
        "tasks": tasks,
        "heldout_candidate_pool_id_list": heldout_pool,
        "authority": {"field_status": False, "scientific_truth": False, "publication_readiness": False},
    }
    op = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FM70_PRE_OUTCOME_FEATURES_V1.json")
    json.dump(out, open(op, "w"), indent=2, sort_keys=True)
    open(op, "a").write("\n")
    print(f"wrote {op}")
    print(f"dev tasks: {len(dev_ids)}  errors: {len(errors)}")
    for proj, pool in heldout_pool.items():
        print(f"  {proj}: held-out pool {pool}")

if __name__ == "__main__":
    main()
