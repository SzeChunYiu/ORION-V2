#!/usr/bin/env python3
"""Normalize source-adapter JSONL records into the ORION scientific-development episode contract.

This script deliberately performs no web scraping. Source-specific acquisition stays
in lawful adapters with their own provenance/custody receipts; this command only
merges already acquired normalized records and emits coverage/bias diagnostics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {"episode_id", "domain_id", "epoch_id", "outcome_class", "steps", "source_mode_ids"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, help="normalized JSONL source adapter output; repeatable")
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    records = []
    source_files = []
    for raw in args.input:
        path = Path(raw)
        source_files.append(str(path))
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            missing = sorted(REQUIRED - set(value))
            if missing:
                raise SystemExit(f"{path}:{line_number}: missing required fields {missing}")
            records.append(value)
    ids = [record["episode_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate episode_id across source adapters")
    Path(args.output).write_text(json.dumps({"schema_version": "orion.v2.scientific-development-corpus.v1", "episodes": records}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": "orion.v2.scientific-development-corpus-receipt.v1",
        "input_files": source_files,
        "episodes": len(records),
        "domains": sorted({record["domain_id"] for record in records}),
        "epochs": sorted({record["epoch_id"] for record in records}),
        "source_modes": sorted({mode for record in records for mode in record["source_mode_ids"]}),
        "bias_audit_required_before_population_claim": True,
        "unpublished_failure_absence_may_be_interpreted_as_no_failure": False,
        "citation_or_prize_metric_is_truth_label": False,
        "authority": {"grants_scientific_truth": False, "grants_causal_law": False},
    }
    Path(args.receipt).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
