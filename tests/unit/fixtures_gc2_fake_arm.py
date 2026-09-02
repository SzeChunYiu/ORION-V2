"""Test-only fake arm for the E70-GC2 suite.

Re-derives the hidden spec from the (test-supplied) nonce + seed + task index and
emits the reference patch (correct) or a deliberately broken patch, with a
per-level success probability from FAKE_ARM_SUCCESS_BY_LEVEL.  Never used in a
protected run: production runs draw a secret nonce that no child process sees.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
import run_orion_generated_composition_gc2_suite as gc2  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    task = request["task"]
    workspace = Path(task["solver_workspace"])
    frozen = json.loads((workspace.parent.parent / "FROZEN_TASKS.json").read_text())
    nonce = os.environ["FAKE_ARM_NONCE"]
    assert hashlib.sha256(nonce.encode()).hexdigest() == frozen["nonce_sha256"]
    rng = random.Random(gc2.derive_run_seed(int(frozen["seed"]), nonce))
    index = int(task["task_id"].split("-")[1]) - 1
    spec = None
    for i in range(index + 1):
        task_rng = random.Random(rng.getrandbits(64))
        if i == index:
            spec = gc2.generate_spec(task_rng, i, frozen["ladder_level"])
    assert spec is not None
    rates = dict(item.split(":") for item in os.environ.get("FAKE_ARM_SUCCESS_BY_LEVEL", "L1:1.0,L2:0.5,L3:0.0").split(","))
    arm_bias = float(os.environ.get(f"FAKE_ARM_BIAS_{request['arm_id']}", "0"))
    p = min(1.0, max(0.0, float(rates[frozen["ladder_level"]]) + arm_bias))
    draw = random.Random(f"{nonce}:{task['task_id']}:{request['arm_id']}:{request.get('rep', 1)}")
    files = gc2.reference_solution(spec)
    if draw.random() >= p:
        files["solver.py"] = files["solver.py"].replace("return LABELS['review']", "return LABELS['reject']", 1) if "LABELS" in files["solver.py"] \
            else files["solver.py"].replace(f"return {spec['labels']['review']!r}", f"return {spec['labels']['reject']!r}", 1)
    patch = gc2.rooted_patch(workspace, files)
    if os.environ.get("FAKE_ARM_MISCOUNT_HEADERS") == "1":
        patch = re.sub(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", lambda m: f"@@ -{m.group(1)},{int(m.group(2)) + 3} +{m.group(3)},{int(m.group(4)) + 5} @@", patch, count=1)
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(json.dumps({
        "schema_version": "orion.v2.agent-response.v1", "task_id": task["task_id"], "arm_id": request["arm_id"],
        "status": "COMPLETED_PROPOSAL_ONLY", "proposed_patch_or_artifact": {"type": "unified_diff", "content": patch},
        "source_ids_used": ["gold-blind-solver-workspace"],
        "resource_receipt": {"total_tokens_reported_by_cli": 1000, "wall_time_seconds": 0.5, "model_calls": 1},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
