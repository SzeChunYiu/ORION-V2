#!/usr/bin/env python3
"""SD70-V3 runner: selftest, development benchmarking, protected prepare,
oracle-absent dispatch with physical request locking, and the frozen evaluator.

Stages
  selftest   native parent known-answer tests (development only)
  dev        development-seed benchmarking; strongest-parent selection rule
  prepare    protected generation (seed must match the committed sha256)
  dispatch   deterministic arms in-process, model arms via the gold-blind
             executable; private oracle absent and public task files locked
             (mode 000) while any model child runs; resumable
  evaluate   every registered outcome, control, gate and terminal

All design constants are read from SD70_V3_EXECUTION_DESIGN_V1.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import stat
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import sd70v3_generator as G  # noqa: E402
import sd70v3_parents as P  # noqa: E402
import sd70v3_stats as S  # noqa: E402
import sd70v3_channel as CH  # noqa: E402

DESIGN_PATH = HERE / "SD70_V3_EXECUTION_DESIGN_V1.json"
MODEL_ARM_SCRIPT = HERE / "sd70v3_model_arm.py"

DETERMINISTIC_ARMS = {
    "TARGET_ONLY_DETERMINISTIC": ("TARGET_ONLY", "TARGET_ONLY_DETERMINISTIC"),
    "SIMPLE_FREQUENCY_PARENT": ("COMMON", "SIMPLE_FREQUENCY_PARENT"),
    "MATCHED_CASE_PARENT": ("COMMON", "MATCHED_CASE_PARENT"),
    "NAIVE_BAYES_PARENT": ("COMMON", "NAIVE_BAYES_PARENT"),
    "DECISION_LIST_PARENT": ("COMMON", "DECISION_LIST_PARENT"),
    "PERCEPTRON_PARENT": ("COMMON", "PERCEPTRON_PARENT"),
    "MAXMARGIN_PARENT": ("COMMON", "MAXMARGIN_PARENT"),
    "PAIRWISE_LINEAR_PARENT": ("COMMON", "PAIRWISE_LINEAR_PARENT"),
    "FIXED_META_LESSON": ("COMMON", "FIXED_META_LESSON"),
    "F0_PARENT_FEDERATION": ("COMMON", "F0_PARENT_FEDERATION"),
}
MODEL_ARM_SURFACES = {
    "TARGET_ONLY_NEGATIVE_CONTROL": "TARGET_ONLY",
    "F2_STATIC_NO_RECURSION": "COMMON_WITH_ADVISORY",
    "F2_RECURSIVE_META_DISCOVERY_FULL": "COMMON_WITH_ADVISORY",
    "F2_FULL_MINUS_FAILURE_EVIDENCE": "COMMON_SUCCESS_ONLY_WITH_ADVISORY",
    "F2_FULL_MINUS_PARENT_FEDERATION": "COMMON",
}
CONTROL_SUFFIXES = ("LP", "QS")


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(G.canonical_bytes(value))


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


ACTIVE_DESIGN_PATH = DESIGN_PATH


def load_design(path: Path = DESIGN_PATH) -> dict[str, Any]:
    global ACTIVE_DESIGN_PATH
    ACTIVE_DESIGN_PATH = Path(path)
    return _read(path)


def design_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or ACTIVE_DESIGN_PATH).read_bytes()).hexdigest()


def dev_seed(k: int) -> int:
    return int(hashlib.sha256(f"SD70-V3-DEV|{k}".encode()).hexdigest()[:15], 16)


# ---------------------------------------------------------------------------
# selftest / dev
# ---------------------------------------------------------------------------

def stage_selftest(out: Path) -> int:
    results = P.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    _write(out, {"schema_version": "orion.v2.sd70-v3.selftest.v1", "results": results,
                 "passed": len(results) - len(failed), "failed": len(failed)})
    print(json.dumps({"selftest_passed": len(results) - len(failed), "selftest_failed": len(failed)}))
    return 1 if failed else 0


def _deterministic_pick(arm: str, surface: dict[str, Any], strongest: str) -> tuple[str, dict[str, Any]]:
    if arm == "F0_PARENT_FEDERATION":
        pick, members = P.federation(surface, strongest)
        return pick, {"member_picks": members}
    if arm == "STRONGEST_GENERATOR_FAITHFUL_PARENT":
        pick, scores = P.select(strongest, surface)
        return pick, {"alias_of": strongest, "scores": [round(s, 6) for s in scores]}
    _surface, fn = DETERMINISTIC_ARMS[arm]
    pick, scores = P.select(fn, surface)
    return pick, {"scores": [round(s, 6) for s in scores]}


def stage_dev(out: Path, seeds: int, tasks: int, train_episodes: int) -> dict[str, Any]:
    arms = [a for a in DETERMINISTIC_ARMS if a != "F0_PARENT_FEDERATION"]
    per_seed = []
    correct: dict[str, list[bool]] = {a: [] for a in arms}
    cfd: dict[str, list[bool]] = {a: [] for a in arms}
    ctrl: dict[str, dict[str, list[bool]]] = {a: {"LP": [], "QS": []} for a in arms}
    wall: dict[str, float] = {a: 0.0 for a in arms}
    chance: list[float] = []
    chance_ctrl: dict[str, list[float]] = {"LP": [], "QS": []}
    for k in range(seeds):
        seed = dev_seed(k)
        pub, priv = G.build_suite(seed, tasks, train_episodes, task_prefix=f"dev{k}")
        oracle = {t["task_id"]: t for t in priv["tasks"]}
        for t in priv["tasks"]:
            chance.append(t["chance_level"])
        for task in pub["tasks"]:
            for arm in arms:
                surf = G.surface_for(DETERMINISTIC_ARMS[arm][0], task, None)
                t0 = time.perf_counter()
                pick, _ = _deterministic_pick(arm, surf, "")
                wall[arm] += time.perf_counter() - t0
                o = oracle[task["task_id"]]
                correct[arm].append(pick == o["correct_action"])
                cfd[arm].append(pick in o["worst_actions"])
        for label, fn in (("LP", G.label_permutation_controls), ("QS", G.query_shuffle_controls)):
            cp, cv = fn(pub, priv, seed)
            co = {t["task_id"]: t for t in cv["tasks"]}
            for t in cv["tasks"]:
                chance_ctrl[label].append(t["chance_level"])
            for task in cp["tasks"]:
                for arm in arms:
                    surf = G.surface_for(DETERMINISTIC_ARMS[arm][0], task, None)
                    pick, _ = _deterministic_pick(arm, surf, "")
                    ctrl[arm][label].append(pick == co[task["task_id"]]["correct_action"])
        per_seed.append({"seed_index": k, "seed_sha256": hashlib.sha256(str(seed).encode()).hexdigest(), "tasks": tasks})
    n = len(chance)
    summary = {}
    for arm in arms:
        acc = sum(correct[arm]) / n
        summary[arm] = {
            "exact_accuracy": acc,
            "wilson95": S.wilson(sum(correct[arm]), n)[1:],
            "critical_false_direction_rate": sum(cfd[arm]) / n,
            "control_LP_accuracy": sum(ctrl[arm]["LP"]) / len(ctrl[arm]["LP"]),
            "control_QS_accuracy": sum(ctrl[arm]["QS"]) / len(ctrl[arm]["QS"]),
            "wall_seconds_total": wall[arm],
        }
    # Frozen selection rule: highest mean development exact accuracy among the
    # generator-faithful candidates; ties (within 1e-12) -> lower wall time.
    ranked = sorted(P.GENERATOR_FAITHFUL_CANDIDATES,
                    key=lambda a: (-round(summary[a]["exact_accuracy"], 12), summary[a]["wall_seconds_total"]))
    strongest = ranked[0]
    second = ranked[1]
    disc = sum(1 for x, y in zip(correct[strongest], correct[second]) if x != y) / n
    # Federation with the selected strongest parent (post-selection, development only).
    fed_correct = []
    fed_cfd = []
    for k in range(seeds):
        seed = dev_seed(k)
        pub, priv = G.build_suite(seed, tasks, train_episodes, task_prefix=f"dev{k}")
        oracle = {t["task_id"]: t for t in priv["tasks"]}
        for task in pub["tasks"]:
            surf = G.surface_for("COMMON", task, None)
            pick, _ = P.federation(surf, strongest)
            fed_correct.append(pick == oracle[task["task_id"]]["correct_action"])
            fed_cfd.append(pick in oracle[task["task_id"]]["worst_actions"])
    summary["F0_PARENT_FEDERATION"] = {
        "exact_accuracy": sum(fed_correct) / n,
        "wilson95": S.wilson(sum(fed_correct), n)[1:],
        "critical_false_direction_rate": sum(fed_cfd) / n,
        "strongest_member": strongest,
    }
    result = {
        "schema_version": "orion.v2.sd70-v3.development-results.v1",
        "development_only": True,
        "protected_outcomes_inspected": False,
        "seeds": per_seed,
        "task_total": n,
        "train_episodes": train_episodes,
        "mean_chance_level": sum(chance) / n,
        "mean_chance_level_controls": {k: sum(v) / len(v) for k, v in chance_ctrl.items()},
        "arms": summary,
        "selection_rule": "highest mean development exact accuracy among GENERATOR_FAITHFUL_CANDIDATES; tie -> lower wall time",
        "generator_faithful_ranking": ranked,
        "strongest_generator_faithful_parent": strongest,
        "second_candidate": second,
        "strongest_vs_second_discordance": disc,
        "strongest_vs_second_paired": S.paired_difference(correct[strongest], correct[second], bootstrap=2000),
    }
    _write(out, result)
    return result


# ---------------------------------------------------------------------------
# prepare (protected)
# ---------------------------------------------------------------------------

def _all_arms(design: dict[str, Any]) -> tuple[list[str], list[str]]:
    det = list(DETERMINISTIC_ARMS) + ["STRONGEST_GENERATOR_FAITHFUL_PARENT"]
    det_all = det + [f"{a}__{s}" for a in det for s in CONTROL_SUFFIXES]
    model = list(design["model_arms"]["full_task_arms"]) + list(design["model_arms"]["subset_arms"])
    return det_all, model


def _arm_surface_kind(arm: str) -> str:
    base = arm.split("__", 1)[0]
    if base in DETERMINISTIC_ARMS:
        return DETERMINISTIC_ARMS[base][0]
    if base == "STRONGEST_GENERATOR_FAITHFUL_PARENT":
        return "COMMON"
    return MODEL_ARM_SURFACES[base]


def _tasks_for_arm(arm: str, design: dict[str, Any], protected: dict, lp: dict, qs: dict) -> list[dict]:
    base, _, suffix = arm.partition("__")
    pool = {"": protected, "LP": lp, "QS": qs}[suffix]["tasks"]
    if base in design["model_arms"]["subset_arms"] or arm in design["model_arms"]["subset_arms"]:
        n = int(design["controls"]["model_control_subset_size"])
        return sorted(pool, key=lambda t: t["task_id"])[:n]
    return pool


def stage_prepare(workdir: Path, seed: int, design: dict[str, Any], force: bool, development: bool = False) -> None:
    commitment = hashlib.sha256(str(seed).encode()).hexdigest()
    if not development and commitment != design["seed_commitment"]["seed_sha256"]:
        raise RuntimeError("seed does not match the committed sha256 in the design; refusing protected generation")
    if workdir.exists():
        if not force:
            raise RuntimeError(f"workdir exists: {workdir}; use --force")
        if (workdir / "responses").exists():
            raise RuntimeError("refusing to overwrite a workdir that already holds responses")
        import shutil
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    tasks = int(design["power"]["task_count"])
    train_episodes = int(design["generator"]["train_episodes"])
    prefix = "sd70v3dev" if development else "sd70v3"
    public, private = G.build_suite(seed, tasks, train_episodes, task_prefix=prefix)
    lp_pub, lp_priv = G.label_permutation_controls(public, private, seed)
    qs_pub, qs_priv = G.query_shuffle_controls(public, private, seed)
    _write(workdir / "public_tasks.json", {"protected": public, "LP": lp_pub, "QS": qs_pub})
    private_all = {
        "schema_version": G.SCHEMA_PRIVATE,
        "seed": seed,
        "protected": private,
        "LP": lp_priv,
        "QS": qs_priv,
    }
    _write(workdir / "private_oracle.json", private_all)
    strongest = design["strongest_generator_faithful_parent"]
    det_arms, model_arms = _all_arms(design)
    manifest: dict[str, Any] = {"schema_version": "orion.v2.sd70-v3.request-surface-manifest.v1", "arms": {}}
    training_only_tokens: dict[str, set[str]] = {}
    for pool in (public, lp_pub, qs_pub):
        for t in pool["tasks"]:
            toks = G.surface_tokens({"training_episodes": t["training_episodes"]})
            toks -= set(t["candidate_actions"]) | set(t["query_context_features"])
            toks -= {"SUCCESS", "FAILURE", "episode_id", "context_features", "chosen_action", "validated_outcome", "resource_cost", "training_episodes"}
            training_only_tokens[t["task_id"]] = toks
    for arm in det_arms + model_arms:
        kind = _arm_surface_kind(arm)
        files = {}
        keys_seen: set[str] = set()
        leak_count = 0
        for task in _tasks_for_arm(arm, design, public, lp_pub, qs_pub):
            base_kind = kind.replace("_WITH_ADVISORY", "")
            adv = None
            if kind.endswith("_WITH_ADVISORY"):
                adv = P.advisory(G.surface_for(base_kind, task, None), strongest)
            surface = G.surface_for(kind, task, adv)
            request = G.build_request(task["task_id"], arm, surface)
            path = workdir / "requests" / arm / f"{task['task_id']}.json"
            _write(path, request)
            files[task["task_id"]] = hashlib.sha256(path.read_bytes()).hexdigest()
            keys_seen.update(surface.keys())
            if kind == "TARGET_ONLY":
                leak_count += len(G.surface_tokens(surface) & training_only_tokens[task["task_id"]])
        arm_hash = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
        manifest["arms"][arm] = {
            "surface_kind": kind,
            "surface_keys": sorted(keys_seen),
            "request_count": len(files),
            "request_sha256": files,
            "arm_surface_sha256": arm_hash,
            "training_token_leaks_into_target_only": leak_count if kind == "TARGET_ONLY" else None,
        }
    manifest["manifest_sha256"] = hashlib.sha256(json.dumps(manifest["arms"], sort_keys=True).encode()).hexdigest()
    _write(workdir / "REQUEST_SURFACE_MANIFEST.json", manifest)
    _write(workdir / "FROZEN_SUITE.json", {
        "schema_version": "orion.v2.sd70-v3.freeze.v1",
        "development": development,
        "design_sha256": design_sha256(),
        "seed_commitment": commitment,
        "task_count": tasks,
        "control_task_count": {"LP": lp_pub["task_count"], "QS": qs_pub["task_count"]},
        "deterministic_arms": det_arms,
        "model_arms": model_arms,
        "strongest_generator_faithful_parent": strongest,
        "manifest_sha256": manifest["manifest_sha256"],
        "private_oracle_visible_to_solver": False,
    })
    print(json.dumps({"workdir": str(workdir), "tasks": tasks, "seed_commitment": commitment,
                      "manifest_sha256": manifest["manifest_sha256"], "model_requests": sum(manifest["arms"][a]["request_count"] for a in model_arms)}))


# ---------------------------------------------------------------------------
# dispatch
# ---------------------------------------------------------------------------

VALID = "VALID"
ARM_FAILURE = "ARM_FAILURE"
INTEGRITY_VIOLATION = "INTEGRITY_VIOLATION"


def validate_response(request_path: Path, response_path: Path, arm: str) -> dict[str, Any]:
    result: dict[str, Any] = {"arm": arm, "task": request_path.stem, "category": INTEGRITY_VIOLATION, "valid": False}
    if not response_path.is_file():
        result["error"] = "MISSING_RESPONSE"
        return result
    try:
        req = _read(request_path)
        resp = _read(response_path)
    except (OSError, json.JSONDecodeError) as exc:
        result["error"] = f"UNREADABLE_RESPONSE:{type(exc).__name__}"
        return result
    result["status"] = resp.get("status")
    result["attempt"] = resp.get("attempt", 1)
    if resp.get("task_id") != req.get("task_id"):
        result["error"] = "TASK_ID_MISMATCH"
        return result
    if resp.get("arm_id") != arm or req.get("arm_id") != arm:
        result["error"] = "ARM_ID_MISMATCH"
        return result
    candidates = set(req.get("surface", {}).get("candidate_actions", []))
    if resp.get("status") != "COMPLETED_PROPOSAL_ONLY":
        result["category"] = ARM_FAILURE
        result["error"] = f"NONCOMPLETED:{resp.get('failure_reason', resp.get('status'))}"
        return result
    if resp.get("selected_action") not in candidates:
        result["category"] = ARM_FAILURE
        result["error"] = "SELECTED_ACTION_OUTSIDE_FROZEN_CANDIDATES"
        return result
    result["category"] = VALID
    result["valid"] = True
    return result


def _model_command() -> list[str]:
    override = os.environ.get("ORION_SD70V2_MODEL_COMMAND", "").strip()
    if override:
        return shlex.split(override)
    return [sys.executable, str(MODEL_ARM_SCRIPT)]


class _Lock:
    """Make the public task pool and every request directory unreadable
    (mode 000) while model children run; restore on exit."""

    def __init__(self, paths: list[Path]):
        self.paths = [p for p in paths if p.exists()]
        self.modes: dict[Path, int] = {}

    def __enter__(self):
        for p in self.paths:
            self.modes[p] = stat.S_IMODE(p.stat().st_mode)
            os.chmod(p, 0)
        return self

    def __exit__(self, *exc):
        for p, m in self.modes.items():
            os.chmod(p, m)
        return False


def stage_dispatch(workdir: Path, design: dict[str, Any], max_concurrency: int, retry_failed: bool) -> dict[str, Any]:
    private_path = (workdir / "private_oracle.json").resolve()
    private_bytes = private_path.read_bytes()
    commitment = hashlib.sha256(private_bytes).hexdigest()
    _write(workdir / "PRIVATE_ORACLE_COMMITMENT.json", {
        "schema_version": "orion.v2.sd70-v3.private-commitment.v1", "sha256": commitment,
        "private_removed_before_dispatch": True})
    frozen = _read(workdir / "FROZEN_SUITE.json")
    strongest = frozen["strongest_generator_faithful_parent"]
    det_arms, model_arms = frozen["deterministic_arms"], frozen["model_arms"]
    max_attempts = int(design["resource_budget"]["max_attempts_per_arm_task"])

    # Deterministic arms: in-process, from their own request surfaces, oracle already irrelevant.
    private_path.unlink()
    det_results = []
    try:
        for arm in det_arms:
            for req_path in sorted((workdir / "requests" / arm).glob("*.json")):
                resp_path = workdir / "responses" / arm / req_path.name
                if resp_path.exists():
                    continue
                req = _read(req_path)
                t0 = time.perf_counter()
                pick, extra = _deterministic_pick(arm.split("__", 1)[0], req["surface"], strongest)
                dt = time.perf_counter() - t0
                _write(resp_path, {
                    "schema_version": "orion.v2.sd70-v3.response.v1", "task_id": req["task_id"], "arm_id": arm,
                    "status": "COMPLETED_PROPOSAL_ONLY", "selected_action": pick, "attempt": 1,
                    "detail": extra,
                    "resource_receipt": {"model_calls": 0, "input_tokens": 0, "output_tokens": 0, "total_tokens": 0,
                                         "tool_calls": 0, "wall_time_seconds": dt, "executor": "deterministic"},
                    "scientific_truth_authorized": False, "causal_law_authorized": False, "field_status_authorized": False,
                })
                det_results.append({"arm": arm, "task": req["task_id"], "returncode": 0})

        # Model arms: read requests into memory, lock the public surfaces, run children in empty cwds.
        expected: list[tuple[str, Path, Path]] = []
        jobs: list[tuple[str, Path, Path, dict, int]] = []
        for arm in model_arms:
            for req_path in sorted((workdir / "requests" / arm).glob("*.json")):
                resp_path = workdir / "responses" / arm / req_path.name
                expected.append((arm, req_path, resp_path))
                attempt = 1
                if resp_path.exists():
                    prev = validate_response(req_path, resp_path, arm)
                    if prev["category"] == VALID:
                        continue
                    if prev["category"] == ARM_FAILURE and retry_failed:
                        attempt = int(prev.get("attempt", 1)) + 1
                        if attempt > max_attempts:
                            continue
                    else:
                        continue
                jobs.append((arm, req_path, resp_path, _read(req_path), attempt))
        env = os.environ.copy()
        env["ORION_GOLD_ACCESS"] = "NONE"
        env["ORION_OUTCOME_ACCESS"] = "NONE"
        lock_paths = [workdir / "public_tasks.json", workdir / "requests"]

        def run_one(job):
            arm, req_path, resp_path, request, attempt = job
            import tempfile
            with tempfile.TemporaryDirectory(prefix="sd70v3-job-") as tmp:
                tmp_req = Path(tmp) / "request.json"
                tmp_req.write_bytes(G.canonical_bytes(request))
                tmp_resp = Path(tmp) / "response.json"
                completed = subprocess.run(_model_command() + ["--request", str(tmp_req), "--response", str(tmp_resp)],
                                           cwd=tmp, env=env, check=False, stdin=subprocess.DEVNULL,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if tmp_resp.exists():
                    data = _read(tmp_resp)
                    data["attempt"] = attempt
                    resp_path.parent.mkdir(parents=True, exist_ok=True)
                    resp_path.write_bytes(G.canonical_bytes(data))
            return {"arm": arm, "task": req_path.stem, "returncode": completed.returncode, "attempt": attempt,
                    "stderr_tail": completed.stderr[-300:]}

        model_results = []
        if jobs:
            with _Lock(lock_paths):
                with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
                    futures = [pool.submit(run_one, job) for job in jobs]
                    for fut in as_completed(futures):
                        model_results.append(fut.result())
    finally:
        if private_path.exists():
            raise RuntimeError("private oracle unexpectedly reappeared during dispatch")
        private_path.write_bytes(private_bytes)
        if hashlib.sha256(private_path.read_bytes()).hexdigest() != commitment:
            raise RuntimeError("private oracle restoration hash mismatch")
    _write(workdir / "PRIVATE_ORACLE_RESTORATION.json", {"sha256": commitment, "restored_hash_exact": True})

    validations = []
    for arm in det_arms + model_arms:
        for req_path in sorted((workdir / "requests" / arm).glob("*.json")):
            validations.append(validate_response(req_path, workdir / "responses" / arm / req_path.name, arm))
    by_cat = {c: sum(1 for v in validations if v["category"] == c) for c in (VALID, ARM_FAILURE, INTEGRITY_VIOLATION)}
    receipt = {
        "schema_version": "orion.v2.sd70-v3.dispatch-receipt.v1",
        "deterministic_jobs": len(det_results),
        "model_jobs_executed": len(model_results),
        "model_jobs": sorted(model_results, key=lambda r: (r["arm"], r["task"])),
        "expected_response_count": len(validations),
        "categories": by_cat,
        "responses": validations,
        "all_returncodes_zero": all(r["returncode"] == 0 for r in det_results + model_results),
        "all_responses_valid": by_cat[ARM_FAILURE] == 0 and by_cat[INTEGRITY_VIOLATION] == 0,
        "integrity_violations": by_cat[INTEGRITY_VIOLATION],
        "dispatch_integrity_passed": by_cat[INTEGRITY_VIOLATION] == 0,
    }
    _write(workdir / "DISPATCH_RECEIPT.json", receipt)
    print(json.dumps({k: receipt[k] for k in ("deterministic_jobs", "model_jobs_executed", "categories", "dispatch_integrity_passed")}))
    return receipt


# ---------------------------------------------------------------------------
# evaluate
# ---------------------------------------------------------------------------

def _arm_records(workdir: Path, arm: str, oracle: dict[str, dict]) -> dict[str, Any]:
    recs = []
    for req_path in sorted((workdir / "requests" / arm).glob("*.json")):
        resp_path = workdir / "responses" / arm / req_path.name
        v = validate_response(req_path, resp_path, arm)
        if v["category"] == INTEGRITY_VIOLATION:
            raise RuntimeError(f"integrity violation in arm {arm} task {req_path.stem}: {v.get('error')}")
        o = oracle[req_path.stem]
        resp = _read(resp_path)
        rr = resp.get("resource_receipt", {})
        sel = resp.get("selected_action") if v["category"] == VALID else None
        recs.append({
            "task_id": req_path.stem, "valid": v["category"] == VALID, "selected_action": sel,
            "correct": bool(sel is not None and sel == o["correct_action"]),
            "cfd": bool(sel is not None and sel in o["worst_actions"]),
            "chance": o["chance_level"], "attempt": int(resp.get("attempt", 1)),
            "model_calls": int(rr.get("model_calls", 0) or 0),
            "input_tokens": rr.get("input_tokens"), "output_tokens": rr.get("output_tokens"),
            "total_tokens": rr.get("total_tokens"), "tool_calls": int(rr.get("tool_calls", 0) or 0),
            "wall": float(rr.get("wall_time_seconds", 0.0) or 0.0),
        })
    if not recs:
        raise RuntimeError(f"no requests for arm {arm}")
    n = len(recs)
    k = sum(r["correct"] for r in recs)
    kf = sum(r["cfd"] for r in recs)
    failures = sum(1 for r in recs if not r["valid"])
    chance = sum(r["chance"] for r in recs) / n
    acc, lo, hi = S.wilson(k, n)

    def _sum(key):
        vals = [r[key] for r in recs if isinstance(r[key], int)]
        return sum(vals) if vals else None

    return {
        "n": n, "correct": k, "exact_accuracy": acc, "wilson95": [lo, hi],
        "critical_false_direction": kf, "critical_false_direction_rate": kf / n,
        "arm_failures": failures, "arm_failure_rate": failures / n, "chance_level": chance,
        "resource_cost": {
            "model_calls": sum(r["model_calls"] for r in recs),
            "attempts_total": sum(r["attempt"] for r in recs),
            "retries": sum(r["attempt"] - 1 for r in recs),
            "input_tokens": _sum("input_tokens"), "output_tokens": _sum("output_tokens"), "total_tokens": _sum("total_tokens"),
            "tool_calls": sum(r["tool_calls"] for r in recs),
            "wall_seconds_total": sum(r["wall"] for r in recs),
            "wall_seconds_mean": sum(r["wall"] for r in recs) / n,
            "aggregation_rule": "sum over arm-tasks (failed attempts included); mean = total / n",
        },
        "records": recs,
    }


def _paired(a: dict[str, Any], b: dict[str, Any], key: str = "correct", bootstrap: int = 10000) -> dict[str, Any]:
    ta = {r["task_id"]: r[key] for r in a["records"]}
    tb = {r["task_id"]: r[key] for r in b["records"]}
    ids = sorted(set(ta) & set(tb))
    pd = S.paired_difference([ta[i] for i in ids], [tb[i] for i in ids], bootstrap=bootstrap)
    pd["midp_one_sided_a_gt_b"] = S.mcnemar_midp_one_sided(pd["b"], pd["c"])
    return pd


def _control_behaves(arm_stats: dict[str, Any], tol: float) -> dict[str, Any]:
    chance = arm_stats["chance_level"]
    lo, hi = arm_stats["wilson95"]
    # Frozen rule: the control behaves iff its accuracy is not significantly
    # above chance: Wilson 95% lower bound <= chance + tol (tol absorbs the
    # shared low-index tie-break bias of the generator family).
    ok = lo <= chance + tol
    return {"accuracy": arm_stats["exact_accuracy"], "chance": chance, "wilson95": [lo, hi], "behaves": ok}


# ---------------------------------------------------------------------------
# V3 gates: arm divergence, channel contract, per-envelope homogeneity
# ---------------------------------------------------------------------------

def check_arm_divergence(workdir: Path, design: dict[str, Any]) -> dict[str, Any]:
    """Taxonomy item 2. Assert every contrasted pair of arms COULD have differed.

    A contrast between two arms whose requests are byte-identical can only ever
    report the same number twice. Every assertion below is reported with the
    denominator it ran over, so a zero is never printed without its count.
    """
    import sd70v3_model_arm as MA

    spec = design["arm_divergence_assertion"]
    rows: list[dict[str, Any]] = []
    for a, b in spec["pairs"]:
        da, db = workdir / "requests" / a, workdir / "requests" / b
        ids_a = {p.stem for p in da.glob("*.json")}
        ids_b = {p.stem for p in db.glob("*.json")}
        shared = sorted(ids_a & ids_b)
        req_diff = prompt_diff = 0
        for tid in shared:
            ra, rb = _read(da / f"{tid}.json"), _read(db / f"{tid}.json")
            if hashlib.sha256(G.canonical_bytes(ra)).hexdigest() != hashlib.sha256(G.canonical_bytes(rb)).hexdigest():
                req_diff += 1
            if MA.build_prompt(ra).encode() != MA.build_prompt(rb).encode():
                prompt_diff += 1
        rows.append({"pair": [a, b], "shared_tasks": len(shared),
                     "requests_differing": req_diff, "prompts_differing": prompt_diff,
                     "all_requests_differ": bool(shared) and req_diff == len(shared),
                     "all_prompts_differ": bool(shared) and prompt_diff == len(shared)})
    # structural assertions on the two surface ablations
    struct: list[dict[str, Any]] = []
    npf = workdir / "requests" / "F2_FULL_MINUS_PARENT_FEDERATION"
    files = sorted(npf.glob("*.json"))
    with_adv = sum(1 for f in files if "parent_advisory" in _read(f)["surface"])
    struct.append({"assertion": "F2_FULL_MINUS_PARENT_FEDERATION has no parent_advisory",
                   "denominator": len(files), "violations": with_adv, "passed": len(files) > 0 and with_adv == 0})
    nfe = workdir / "requests" / "F2_FULL_MINUS_FAILURE_EVIDENCE"
    files = sorted(nfe.glob("*.json"))
    with_fail = 0
    for f in files:
        eps = _read(f)["surface"].get("training_episodes", [])
        if any(e.get("validated_outcome") == "FAILURE" for e in eps):
            with_fail += 1
    struct.append({"assertion": "F2_FULL_MINUS_FAILURE_EVIDENCE has no FAILURE episode",
                   "denominator": len(files), "violations": with_fail, "passed": len(files) > 0 and with_fail == 0})
    # control assertion that MUST fail-to-be-clean: the full arm DOES carry both
    full = sorted((workdir / "requests" / "F2_RECURSIVE_META_DISCOVERY_FULL").glob("*.json"))
    full_adv = sum(1 for f in full if "parent_advisory" in _read(f)["surface"])
    full_fail = sum(1 for f in full if any(e.get("validated_outcome") == "FAILURE"
                                           for e in _read(f)["surface"].get("training_episodes", [])))
    struct.append({"assertion": "POSITIVE CONTROL: the full arm DOES carry parent_advisory and FAILURE episodes "
                                "(if this fails the two checks above are vacuous)",
                   "denominator": len(full), "advisory_present": full_adv, "failure_present": full_fail,
                   "passed": len(full) > 0 and full_adv == len(full) and full_fail == len(full)})
    passed = (all(r["all_requests_differ"] and r["all_prompts_differ"] for r in rows) and bool(rows)
              and all(x["passed"] for x in struct))
    return {"schema_version": "orion.v2.sd70-v3.arm-divergence.v1", "passed": passed,
            "pairs": rows, "structural": struct}


def check_envelope_homogeneity(workdir: Path, design: dict[str, Any], model_arms: list[str]) -> dict[str, Any]:
    """Per-envelope channel homogeneity across the whole model dispatch."""
    spec = design["envelope_homogeneity"]
    g = spec["gates"]
    lm = g["input_tokens_linear_model"]
    cap = g["reasoning_output_tokens_cap"]
    expected_comp = design["channel_contract"]["expected_comp_hash"]
    n = usage_ok = ratio_ok = reasoning_over = comp_observable = comp_mismatch = 0
    ratios: list[float] = []
    for arm in model_arms:
        for rp in sorted((workdir / "responses" / arm).glob("*.json")):
            r = _read(rp).get("resource_receipt", {})
            n += 1
            if r.get("usage_source") == "TURN_COMPLETED_USAGE":
                usage_ok += 1
            it, pb = r.get("input_tokens"), r.get("prompt_bytes")
            if isinstance(it, int) and isinstance(pb, int) and pb > 0:
                resid = it - (lm["base"] + lm["slope"] * pb)
                ratios.append(resid)
                if abs(resid) <= lm["residual_abs_tolerance"]:
                    ratio_ok += 1
            rot = r.get("reasoning_output_tokens")
            if isinstance(rot, int) and rot > cap:
                reasoning_over += 1
            co = r.get("channel_observation") or {}
            if co.get("observable"):
                comp_observable += 1
                if co.get("gpt_5_5_comp_hash") != expected_comp:
                    comp_mismatch += 1
    if n == 0:
        return {"schema_version": "orion.v2.sd70-v3.envelope-homogeneity.v1", "denominator": 0,
                "verdict": CH.CONTRACT_UNOBSERVABLE, "passed": False,
                "reason": "no model envelopes to check"}
    checks = {
        "usage_observed_fraction": {"value": usage_ok / n, "denominator": n,
                                    "threshold": g["usage_observed_fraction"], "passed": usage_ok / n >= g["usage_observed_fraction"]},
        "input_tokens_linear_model_residual_within_tolerance": {
            "value": ratio_ok / n, "denominator": n, "model": lm,
            "threshold": lm["min_fraction_within"],
            "passed": ratio_ok / n >= lm["min_fraction_within"],
            "residual_min": round(min(ratios), 1) if ratios else None,
            "residual_max": round(max(ratios), 1) if ratios else None},
        "reasoning_cap_exceed_fraction": {"value": reasoning_over / n, "denominator": n, "cap": cap,
                                          "threshold": g["reasoning_cap_max_exceed_fraction"],
                                          "passed": reasoning_over / n <= g["reasoning_cap_max_exceed_fraction"]},
        "comp_hash_consistency": {"observable_envelopes": comp_observable, "denominator": n,
                                  "mismatches": comp_mismatch, "expected": expected_comp,
                                  "passed": comp_mismatch == 0},
    }
    unobservable = comp_observable == 0 or usage_ok == 0
    passed = all(c["passed"] for c in checks.values()) and not unobservable
    verdict = CH.CONTRACT_OK if passed else (CH.CONTRACT_UNOBSERVABLE if unobservable else CH.CONTRACT_DRIFT)
    return {"schema_version": "orion.v2.sd70-v3.envelope-homogeneity.v1", "denominator": n,
            "checks": checks, "verdict": verdict, "passed": passed,
            "unobservable_note": ("comp_hash never observable on any envelope" if comp_observable == 0 else None)}


def stage_evaluate(workdir: Path, design: dict[str, Any]) -> dict[str, Any]:
    frozen = _read(workdir / "FROZEN_SUITE.json")
    if frozen["design_sha256"] != design_sha256() and not frozen.get("development"):
        raise RuntimeError("design JSON changed after the suite was frozen; refusing to evaluate")
    receipt = _read(workdir / "DISPATCH_RECEIPT.json")
    if not receipt["dispatch_integrity_passed"]:
        raise RuntimeError("dispatch integrity failed; CANNOT_CHECK")
    private = _read(workdir / "private_oracle.json")
    oracle: dict[str, dict] = {}
    for pool in ("protected", "LP", "QS"):
        for t in private[pool]["tasks"]:
            oracle[t["task_id"]] = t
    public = _read(workdir / "public_tasks.json")
    if {t["task_id"] for t in public["protected"]["tasks"]} != {t["task_id"] for t in private["protected"]["tasks"]}:
        raise RuntimeError("public/private task identities differ")
    det_arms, model_arms = frozen["deterministic_arms"], frozen["model_arms"]
    sp = "STRONGEST_GENERATOR_FAITHFUL_PARENT"
    f2 = "F2_RECURSIVE_META_DISCOVERY_FULL"
    f2s = "F2_STATIC_NO_RECURSION"
    stats: dict[str, Any] = {}
    for arm in det_arms + model_arms:
        stats[arm] = _arm_records(workdir, arm, oracle)
    g = design["gates"]
    miss = design["missingness"]

    # --- missingness / integrity gate -------------------------------------
    model_total = sum(stats[a]["n"] for a in model_arms)
    model_fail = sum(stats[a]["arm_failures"] for a in model_arms)
    global_fail_rate = model_fail / model_total if model_total else 0.0
    per_arm_exceed = [a for a in model_arms if stats[a]["arm_failure_rate"] > miss["per_arm_failure_threshold"]]
    cannot_check_reasons = []
    if global_fail_rate > miss["global_failure_threshold"]:
        cannot_check_reasons.append(f"global model failure rate {global_fail_rate:.3f} > {miss['global_failure_threshold']}")
    for a in per_arm_exceed:
        if a in (f2, f2s, "TARGET_ONLY_NEGATIVE_CONTROL"):
            cannot_check_reasons.append(f"arm {a} failure rate {stats[a]['arm_failure_rate']:.3f} > {miss['per_arm_failure_threshold']}")
    # evaluator validity: the parent's own label-permutation control must sit at chance
    sp_lp = _control_behaves(stats[f"{sp}__LP"], g["control_tolerance"])
    if not sp_lp["behaves"]:
        cannot_check_reasons.append("strongest parent label-permutation control not at chance (evaluator/control machinery invalid)")

    # --- V3 gate: arms could actually have differed (taxonomy item 2) ------
    divergence = check_arm_divergence(workdir, design)
    if not divergence["passed"]:
        cannot_check_reasons.append("arm-divergence assertion failed: a contrasted pair could not have differed")

    # --- V3 gate: per-envelope channel homogeneity ------------------------
    homogeneity = check_envelope_homogeneity(workdir, design, model_arms)
    if not homogeneity["passed"]:
        cannot_check_reasons.append(f"envelope homogeneity {homogeneity['verdict']}")

    # --- V3 gate: start/end channel contract ------------------------------
    cs, ce = workdir / "CHANNEL_START.json", workdir / "CHANNEL_END.json"
    if not (cs.exists() and ce.exists()):
        channel = {"verdict": CH.CONTRACT_UNOBSERVABLE,
                   "reason": "CHANNEL_START.json and/or CHANNEL_END.json absent; the contract was never measured"}
    else:
        channel = CH.verdict(_read(cs), _read(ce), design["channel_contract"])
    if channel["verdict"] != CH.CONTRACT_OK:
        cannot_check_reasons.append(f"channel contract {channel['verdict']}")

    # --- primary outcomes ---------------------------------------------------
    primary = {
        "F2_FULL_vs_SP": _paired(stats[f2], stats[sp]),
        "F2_STATIC_vs_SP": _paired(stats[f2s], stats[sp]),
    }
    holm = S.holm({k: v["midp_one_sided_a_gt_b"] for k, v in primary.items()}, alpha=g["alpha_family"])
    secondary = {
        "F2_FULL_vs_F0": _paired(stats[f2], stats["F0_PARENT_FEDERATION"], bootstrap=4000),
        "F0_vs_SP": _paired(stats["F0_PARENT_FEDERATION"], stats[sp], bootstrap=4000),
        "FIXED_vs_SP": _paired(stats["FIXED_META_LESSON"], stats[sp], bootstrap=4000),
        "FIXED_vs_F2_FULL": _paired(stats["FIXED_META_LESSON"], stats[f2], bootstrap=4000),
        "SP_vs_SIMPLE_FREQUENCY": _paired(stats[sp], stats["SIMPLE_FREQUENCY_PARENT"], bootstrap=4000),
    }
    ablations = {
        "no_recursion": _paired(stats[f2], stats[f2s], bootstrap=4000),
        "no_failure_evidence": _paired(stats[f2], stats["F2_FULL_MINUS_FAILURE_EVIDENCE"], bootstrap=4000),
        "no_parent_federation": _paired(stats[f2], stats["F2_FULL_MINUS_PARENT_FEDERATION"], bootstrap=4000),
    }
    cfd = {
        "F2_FULL_vs_SP": _paired(stats[f2], stats[sp], key="cfd", bootstrap=4000),
        "F2_STATIC_vs_SP": _paired(stats[f2s], stats[sp], key="cfd", bootstrap=4000),
    }
    controls = {
        "TARGET_ONLY_NEGATIVE_CONTROL": _control_behaves(stats["TARGET_ONLY_NEGATIVE_CONTROL"], g["control_tolerance"]),
        "TARGET_ONLY_DETERMINISTIC": _control_behaves(stats["TARGET_ONLY_DETERMINISTIC"], g["control_tolerance"]),
        f"{f2}__LP": _control_behaves(stats[f"{f2}__LP"], g["control_tolerance"]),
        f"{f2}__QS": _control_behaves(stats[f"{f2}__QS"], g["control_tolerance"]),
        f"{sp}__LP": sp_lp,
        f"{sp}__QS": _control_behaves(stats[f"{sp}__QS"], g["control_tolerance"]),
    }

    # --- gates ---------------------------------------------------------------
    d = primary["F2_FULL_vs_SP"]
    budget = design["resource_budget"]
    f2_cost = stats[f2]["resource_cost"]
    gates = {
        "effect_minimum": d["point"] >= g["minimum_effect"],
        "effect_significant_holm": bool(holm["F2_FULL_vs_SP"]["reject"]),
        "non_regression": d["ci_low"] > -g["non_inferiority_margin"],
        "critical_false_direction": cfd["F2_FULL_vs_SP"]["point"] <= g["cfd_margin"],
        "cost_within_budget": (stats[f2]["arm_failure_rate"] <= miss["per_arm_failure_threshold"]
                               and f2_cost["attempts_total"] <= budget["max_attempts_per_arm_task"] * stats[f2]["n"]),
        "mechanism_recursion": (ablations["no_recursion"]["point"] >= g["ablation_minimum_effect"]
                                and ablations["no_recursion"]["midp_one_sided_a_gt_b"] < g["ablation_alpha"]),
        "no_ablation_beats_full": all(v["point"] >= -g["ablation_noise_tolerance"] for v in ablations.values()),
        "model_negative_controls_behave": all(controls[k]["behaves"] for k in ("TARGET_ONLY_NEGATIVE_CONTROL", f"{f2}__LP", f"{f2}__QS")),
        "parent_ties_or_exceeds_f2": d["point"] <= 0.0,
    }
    fixed_ge_f2 = secondary["FIXED_vs_F2_FULL"]["point"] >= 0.0

    if cannot_check_reasons:
        route = "CANNOT_CHECK"
    elif gates["parent_ties_or_exceeds_f2"] or not (gates["effect_minimum"] and gates["effect_significant_holm"]
                                                     and gates["non_regression"] and gates["critical_false_direction"]
                                                     and gates["cost_within_budget"] and gates["mechanism_recursion"]
                                                     and gates["no_ablation_beats_full"] and gates["model_negative_controls_behave"]):
        route = "PARENT_SUFFICIENT"
    elif fixed_ge_f2:
        route = "FIXED_META_LESSON_SUFFICIENT"
    else:
        route = "PROSPECTIVE_META_POLICY_RESIDUAL"

    summary_arms = {a: {k: v for k, v in stats[a].items() if k != "records"} for a in stats}
    rollup = {
        "schema_version": "orion.v2.sd70-v3.rollup.v1",
        "study_id": "SD70-V3",
        "design_sha256": design_sha256(),
        "development": bool(frozen.get("development")),
        "task_count": frozen["task_count"],
        "strongest_generator_faithful_parent": frozen["strongest_generator_faithful_parent"],
        "arms": summary_arms,
        "missingness": {"model_arm_tasks": model_total, "model_arm_failures": model_fail, "global_failure_rate": global_fail_rate,
                        "per_arm_exceeding_threshold": per_arm_exceed},
        "primary_outcomes": {"protected_decision_quality": primary, "holm": holm, "critical_false_direction": cfd,
                             "parent_non_regression": {"delta_ci_low": d["ci_low"], "margin": g["non_inferiority_margin"], "holds": gates["non_regression"]},
                             "resource_cost": {a: stats[a]["resource_cost"] for a in stats}},
        "secondary": secondary,
        "ablations": ablations,
        "negative_controls": controls,
        "gates": gates,
        "arm_divergence": divergence,
        "envelope_homogeneity": homogeneity,
        "channel_contract": channel,
        "cannot_check_reasons": cannot_check_reasons,
        "route": route,
        "authority": {"grants_scientific_truth": False, "grants_causal_law": False, "grants_field_status": False,
                      "grants_submission_readiness": False, "grants_publication_readiness": False},
    }
    _write(workdir / "SD70_V3_ROLLUP.json", rollup)
    _write(workdir / "SD70_V3_ARM_RECORDS.json", {a: stats[a]["records"] for a in stats})
    (workdir / "SD70_V3_ROLLUP.md").write_text(render_rollup(rollup), encoding="utf-8")
    print(json.dumps({"route": route, "F2_FULL_vs_SP": {k: d[k] for k in ("point", "ci_low", "ci_high")},
                      "channel_contract": channel["verdict"],
                      "envelope_homogeneity": homogeneity["verdict"],
                      "arm_divergence_passed": divergence["passed"],
                      "cannot_check_reasons": cannot_check_reasons}))
    return rollup


def render_rollup(r: dict[str, Any]) -> str:
    lines = [f"# SD70-V3 rollup ({'DEVELOPMENT' if r['development'] else 'PROTECTED'})", "",
             f"Route: **{r['route']}**  ", f"Design sha256: `{r['design_sha256']}`  ",
             f"Strongest generator-faithful parent: `{r['strongest_generator_faithful_parent']}`  ", f"Tasks: {r['task_count']}", "",
             "| arm | n | exact | Wilson 95% | CFD rate | failures | model calls | tokens | wall s |", "|---|---|---|---|---|---|---|---|---|"]
    for a, s in r["arms"].items():
        c = s["resource_cost"]
        lines.append(f"| {a} | {s['n']} | {s['exact_accuracy']:.3f} | [{s['wilson95'][0]:.3f}, {s['wilson95'][1]:.3f}] | {s['critical_false_direction_rate']:.3f} | {s['arm_failures']} | {c['model_calls']} | {c['total_tokens']} | {c['wall_seconds_total']:.1f} |")
    p = r["primary_outcomes"]["protected_decision_quality"]
    lines += ["", "## Primary paired contrasts (a - b, exact accuracy)", "", "| contrast | point | 95% boot CI | b/c | mid-p | Holm reject |", "|---|---|---|---|---|---|"]
    for k, v in p.items():
        h = r["primary_outcomes"]["holm"][k]
        lines.append(f"| {k} | {v['point']:+.3f} | [{v['ci_low']:+.3f}, {v['ci_high']:+.3f}] | {v['b']}/{v['c']} | {v['midp_one_sided_a_gt_b']:.4f} | {h['reject']} |")
    lines += ["", "## Ablations (F2_FULL - ablation)", ""]
    for k, v in r["ablations"].items():
        lines.append(f"- {k}: {v['point']:+.3f} [{v['ci_low']:+.3f}, {v['ci_high']:+.3f}] mid-p {v['midp_one_sided_a_gt_b']:.4f}")
    lines += ["", "## Negative controls", ""]
    for k, v in r["negative_controls"].items():
        lines.append(f"- {k}: acc {v['accuracy']:.3f} vs chance {v['chance']:.3f} -> {'behaves' if v['behaves'] else 'FAILS'}")
    lines += ["", "## Gates", ""] + [f"- {k}: {v}" for k, v in r["gates"].items()]
    if r["cannot_check_reasons"]:
        lines += ["", "## CANNOT_CHECK reasons", ""] + [f"- {x}" for x in r["cannot_check_reasons"]]
    lines += ["", "No authority is granted by this rollup (scientific truth, causal law, field status, submission or publication readiness all false)."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("selftest")
    s.add_argument("--output", type=Path, default=HERE / "results" / "SD70_V3_SELFTEST_V1.json")
    d = sub.add_parser("dev")
    d.add_argument("--output", type=Path, default=HERE / "results" / "SD70_V3_DEVELOPMENT_RESULTS_V1.json")
    d.add_argument("--seeds", type=int, default=3)
    d.add_argument("--tasks", type=int, default=200)
    d.add_argument("--train-episodes", type=int, default=16)
    p = sub.add_parser("prepare")
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--design", type=Path, default=DESIGN_PATH)
    p.add_argument("--force", action="store_true")
    p.add_argument("--development", action="store_true", help="development seed; commitment check skipped; never protected")
    di = sub.add_parser("dispatch")
    di.add_argument("--workdir", type=Path, required=True)
    di.add_argument("--design", type=Path, default=DESIGN_PATH)
    di.add_argument("--max-concurrency", type=int, default=2)
    di.add_argument("--retry-failed", action="store_true")
    e = sub.add_parser("evaluate")
    e.add_argument("--workdir", type=Path, required=True)
    e.add_argument("--design", type=Path, default=DESIGN_PATH)
    args = parser.parse_args(argv)
    if args.command == "selftest":
        return stage_selftest(args.output)
    if args.command == "dev":
        stage_dev(args.output, args.seeds, args.tasks, args.train_episodes)
        return 0
    design = load_design(args.design)
    if args.command == "prepare":
        stage_prepare(args.workdir, args.seed, design, args.force, args.development)
    elif args.command == "dispatch":
        if int(args.max_concurrency) > int(design["resource_budget"]["max_concurrency"]):
            raise SystemExit("max-concurrency exceeds the frozen budget")
        stage_dispatch(args.workdir, design, args.max_concurrency, args.retry_failed)
    else:
        stage_evaluate(args.workdir, design)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
