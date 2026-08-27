#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from orion_v2.handoff import load_and_validate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the exact ORION V1 handoff receipt")
    parser.add_argument(
        "receipt",
        nargs="?",
        default=ROOT / "provenance" / "ORION_V1_HANDOFF_RECEIPT_V1.json",
        type=Path,
    )
    args = parser.parse_args()
    result = load_and_validate(args.receipt)
    print(result.terminal)
    for error in result.errors:
        print(f"- {error}")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
