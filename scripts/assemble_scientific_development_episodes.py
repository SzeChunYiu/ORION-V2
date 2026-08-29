#!/usr/bin/env python3
"""Assemble source-adapter observations into trajectory-level episode JSONL.

This command performs no acquisition and never infers scientific success from citation,
fame or other proxy metrics. Validated success/failure requires an explicit outcome
binding with witness identities.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind, OutcomeBinding, assemble_all


def load_jsonl(path: Path):
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: {exc}") from exc


def observation(v):
    return DevelopmentObservation(
        observation_id=v["observation_id"], trajectory_id=v["trajectory_id"], domain_id=v["domain_id"],
        epoch_id=v["epoch_id"], source_mode_id=v["source_mode_id"], ordinal=int(v["ordinal"]),
        kind=ObservationKind(v["kind"]), action_feature_ids=tuple(v["action_feature_ids"]),
        result_feature_ids=tuple(v.get("result_feature_ids", ())), failure_feature_ids=tuple(v.get("failure_feature_ids", ())),
        source_ids=tuple(v.get("source_ids", ())), validation_ids=tuple(v.get("validation_ids", ())),
        institution_ids=tuple(v.get("institution_ids", ())), team_id=v.get("team_id", ""),
        proxy_metrics=tuple((str(k), float(x)) for k, x in v.get("proxy_metrics", {}).items()),
        bias_flag_ids=tuple(v.get("bias_flag_ids", ())), resource_cost=float(v.get("resource_cost", 0.0)),
    )


def binding(v):
    return OutcomeBinding(v["trajectory_id"], v["outcome_class"], tuple(v.get("witness_ids", ())), tuple(v.get("source_ids", ())))


def episode_dict(ep):
    value = asdict(ep)
    value["outcome_class"] = ep.outcome_class.value
    value["proxy_metrics"] = dict(ep.proxy_metrics)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation", action="append", required=True)
    parser.add_argument("--outcome-binding", action="append", default=[])
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    observations = [observation(v) for raw in args.observation for v in load_jsonl(Path(raw))]
    bindings = [binding(v) for raw in args.outcome_binding for v in load_jsonl(Path(raw))]
    episodes = assemble_all(observations, bindings)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(episode_dict(ep), sort_keys=True) + "\n" for ep in episodes), encoding="utf-8")
    receipt = {
        "schema_version": "orion.v2.scientific-development-source-assembly.v1",
        "observation_records": len(observations),
        "episodes": len(episodes),
        "validated_outcome_bindings": len(bindings),
        "unknown_outcome_episodes": sum(ep.outcome_class.value == "UNKNOWN" for ep in episodes),
        "citation_or_fame_infers_outcome": False,
        "acquisition_performed": False,
        "authority": {"grants_scientific_truth": False, "grants_causal_law": False},
    }
    Path(args.receipt).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
