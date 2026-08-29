#!/usr/bin/env python3
"""Prepare, dispatch and evaluate the fresh SD70 recursive meta-policy suite.

Private oracle bytes are removed from disk during model dispatch and restored only
after all child model processes terminate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def prepare(workdir: Path, tasks: int, train_episodes: int, seed: int | None, arms: list[str], force: bool) -> None:
    if workdir.exists():
        if not force:
            raise RuntimeError(f"workdir exists: {workdir}; use --force")
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    public_path = workdir / "public_tasks.json"
    private_path = workdir / "private_oracle.json"
    command = [
        sys.executable,
        str(ROOT / "scripts/generate_scientific_development_meta_benchmark.py"),
        "--public", str(public_path), "--private", str(private_path),
        "--tasks", str(tasks), "--train-episodes", str(train_episodes),
    ]
    if seed is not None:
        command += ["--seed", str(seed)]
    subprocess.run(command, check=True, cwd=ROOT)
    public = json.loads(public_path.read_text(encoding="utf-8"))
    for arm in arms:
        for task in public["tasks"]:
            _write(
                workdir / "requests" / arm / f"{task['task_id']}.json",
                {
                    "schema_version": "orion.v2.sd70-agent-request.v1",
                    "task_id": task["task_id"],
                    "arm_id": arm,
                    "task": task,
                    "gold_access": "NONE",
                    "outcome_access": "NONE",
                    "scientific_truth_authorized": False,
                },
            )
    _write(workdir / "FROZEN_SUITE.json", {
        "schema_version": "orion.v2.sd70-freeze.v1",
        "task_count": public["task_count"],
        "seed_commitment": public["seed_commitment"],
        "arms": arms,
        "private_oracle_visible_to_solver": False,
    })


def _arm_command() -> list[str]:
    override = os.environ.get("ORION_SD70_ARM_COMMAND", "").strip()
    if override:
        return shlex.split(override)
    return [sys.executable, str(ROOT / "scripts/orion_scientific_development_arms.py")]


def dispatch(workdir: Path, arms: list[str], max_concurrency: int, overwrite: bool) -> None:
    private_path = (workdir / "private_oracle.json").resolve()
    private_bytes = private_path.read_bytes()
    commitment = hashlib.sha256(private_bytes).hexdigest()
    _write(workdir / "PRIVATE_ORACLE_COMMITMENT.json", {
        "schema_version": "orion.v2.sd70-private-commitment.v1",
        "sha256": commitment,
        "private_removed_before_dispatch": True,
    })
    private_path.unlink()
    env = os.environ.copy()
    env["ORION_GOLD_ACCESS"] = "NONE"
    env["ORION_OUTCOME_ACCESS"] = "NONE"
    jobs = []
    for arm in arms:
        for request in sorted((workdir / "requests" / arm).glob("*.json")):
            response = workdir / "responses" / arm / request.name
            if response.exists() and not overwrite:
                continue
            jobs.append((arm, request, response))

    def run_one(job):
        arm, request, response = job
        response.parent.mkdir(parents=True, exist_ok=True)
        completed = subprocess.run(_arm_command() + ["--request", str(request), "--response", str(response)], cwd=ROOT, env=env, check=False)
        return {"arm": arm, "task": request.stem, "returncode": completed.returncode}

    results = []
    try:
        with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
            futures = [pool.submit(run_one, job) for job in jobs]
            for future in as_completed(futures):
                results.append(future.result())
    finally:
        if private_path.exists():
            raise RuntimeError("private oracle unexpectedly reappeared during dispatch")
        private_path.write_bytes(private_bytes)
        if hashlib.sha256(private_path.read_bytes()).hexdigest() != commitment:
            raise RuntimeError("private oracle restoration hash mismatch")
    _write(workdir / "DISPATCH_RECEIPT.json", {"jobs": results, "all_returncodes_zero": all(item["returncode"] == 0 for item in results)})
    if not all(item["returncode"] == 0 for item in results):
        raise RuntimeError("one or more arm jobs failed")


def evaluate(workdir: Path, arms: list[str]) -> None:
    private = json.loads((workdir / "private_oracle.json").read_text(encoding="utf-8"))
    oracle = {item["task_id"]: item["correct_action"] for item in private["tasks"]}
    summaries = {}
    for arm in arms:
        responses = []
        for path in sorted((workdir / "responses" / arm).glob("*.json")):
            item = json.loads(path.read_text(encoding="utf-8"))
            responses.append({"task_id": item["task_id"], "selected_action": item.get("selected_action")})
        correct = sum(item["selected_action"] == oracle.get(item["task_id"]) for item in responses)
        summaries[arm] = {"completed": len(responses), "correct": correct, "accuracy": correct / len(oracle) if oracle else 0.0}
    _write(workdir / "EVALUATION_SUMMARY.json", {
        "schema_version": "orion.v2.sd70-arm-evaluation.v1",
        "task_count": len(oracle),
        "arms": summaries,
        "authority": {"grants_scientific_truth": False, "grants_meta_principle": False, "grants_F2_superiority": False},
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--tasks", type=int, default=120)
    p.add_argument("--train-episodes", type=int, default=16)
    p.add_argument("--seed", type=int)
    p.add_argument("--arms", default="TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL")
    p.add_argument("--force", action="store_true")
    d = sub.add_parser("dispatch")
    d.add_argument("--workdir", type=Path, required=True)
    d.add_argument("--arms", required=True)
    d.add_argument("--max-concurrency", type=int, default=2)
    d.add_argument("--overwrite-responses", action="store_true")
    e = sub.add_parser("evaluate")
    e.add_argument("--workdir", type=Path, required=True)
    e.add_argument("--arms", required=True)
    args = parser.parse_args()
    arms = [item.strip() for item in args.arms.split(",") if item.strip()]
    if args.command == "prepare":
        prepare(args.workdir, args.tasks, args.train_episodes, args.seed, arms, args.force)
    elif args.command == "dispatch":
        dispatch(args.workdir, arms, args.max_concurrency, args.overwrite_responses)
    else:
        evaluate(args.workdir, arms)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
