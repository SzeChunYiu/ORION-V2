#!/usr/bin/env python3
"""Exact reproducibility control for the PRA one-step compatibility theorem.

This checker is deliberately tiny.  It verifies the counterexample used to show
that non-empty pairwise acceptable-action intersections do not imply a non-empty
joint intersection over an entire merged representation/evidence cell.

It is a reproducibility check only; the theorem proof does not depend on this
script and the script grants no empirical LLM claim.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Iterable


def _sorted(values: Iterable[str]) -> list[str]:
    return sorted(set(values))


def assess() -> dict[str, object]:
    acceptable = {
        "h1": {"a", "b"},
        "h2": {"b", "c"},
        "h3": {"a", "c"},
    }

    pairwise: dict[str, list[str]] = {}
    for left, right in combinations(acceptable, 2):
        pairwise[f"{left}&{right}"] = _sorted(acceptable[left] & acceptable[right])

    joint = set.intersection(*(set(v) for v in acceptable.values()))
    pairwise_nonempty = all(bool(v) for v in pairwise.values())
    one_step_compatible = bool(joint)

    result = {
        "schema": "orion-v2.llm-pra-three-history-compatibility.v1",
        "acceptable_action_sets": {k: _sorted(v) for k, v in acceptable.items()},
        "pairwise_intersections": pairwise,
        "all_pairwise_intersections_nonempty": pairwise_nonempty,
        "joint_intersection": _sorted(joint),
        "joint_intersection_empty": not bool(joint),
        "one_step_compatible": one_step_compatible,
        "expected": {
            "all_pairwise_intersections_nonempty": True,
            "joint_intersection_empty": True,
            "one_step_compatible": False,
        },
        "scientific_authority": False,
        "empirical_llm_result": False,
    }

    assert result["all_pairwise_intersections_nonempty"] is True
    assert result["joint_intersection_empty"] is True
    assert result["one_step_compatible"] is False
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    args = parser.parse_args()

    result = assess()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered, encoding="utf-8")

    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(
            "# Three-History Compatibility Receipt V1\n\n"
            "**Status:** PASS — exact deterministic reproducibility control.\n\n"
            "The acceptable-action sets are `{a,b}`, `{b,c}`, and `{a,c}`. "
            "Every pair overlaps, but the joint intersection is empty. Therefore, "
            "under exact `ANY_OPTIMAL_ACTION` semantics, the merged cell is not "
            "one-step compatible. This confirms the manuscript's complete-intersection "
            "control and is not an empirical LLM result.\n\n"
            "```text\n"
            "all_pairwise_intersections_nonempty = true\n"
            "joint_intersection = empty\n"
            "one_step_compatible = false\n"
            "```\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
