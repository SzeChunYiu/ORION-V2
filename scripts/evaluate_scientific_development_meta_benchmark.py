#!/usr/bin/env python3
"""Score SD70 predictions against a private oracle file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", required=True)
    parser.add_argument("--private", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    public = json.loads(Path(args.public).read_text(encoding="utf-8"))
    private = json.loads(Path(args.private).read_text(encoding="utf-8"))
    predictions = json.loads(Path(args.predictions).read_text(encoding="utf-8"))
    public_ids = {task["task_id"] for task in public["tasks"]}
    oracle = {task["task_id"]: task["correct_action"] for task in private["tasks"]}
    if public_ids != set(oracle):
        raise SystemExit("public/private task identities differ")
    pred_map = {item["task_id"]: item["selected_action"] for item in predictions["predictions"]}
    missing = sorted(public_ids - set(pred_map))
    extras = sorted(set(pred_map) - public_ids)
    correct = sum(pred_map.get(task_id) == oracle[task_id] for task_id in public_ids)
    receipt = {
        "schema_version": "orion.v2.sd70-evaluation.v1",
        "task_count": len(public_ids),
        "completed_predictions": len(public_ids) - len(missing),
        "correct": correct,
        "accuracy": correct / len(public_ids) if public_ids else 0.0,
        "missing_task_ids": missing,
        "extra_task_ids": extras,
        "authority": {
            "grants_scientific_truth": False,
            "grants_meta_principle": False,
            "grants_F2_superiority": False,
        },
    }
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
