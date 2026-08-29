#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from orion_v2.parity import load_and_validate_capability_census
result=load_and_validate_capability_census(ROOT/'provenance'/'V1_CAPABILITY_CENSUS_V1.json')
print(result.terminal)
for error in result.errors: print(f'- {error}')
raise SystemExit(0 if result.valid else 1)
