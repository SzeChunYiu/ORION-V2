import json
from pathlib import Path
from orion_v2.parity import load_and_validate_capability_census, validate_capability_census
ROOT=Path(__file__).resolve().parents[2]

def test_bound_v1_capability_census_has_exactly_59_unique_cells() -> None:
    result=load_and_validate_capability_census(ROOT/'provenance'/'V1_CAPABILITY_CENSUS_V1.json')
    assert result.valid, result.errors
    assert result.capability_count==59

def test_missing_capability_fails_census() -> None:
    data=json.loads((ROOT/'provenance'/'V1_CAPABILITY_CENSUS_V1.json').read_text()); data['capabilities'].pop(); result=validate_capability_census(data)
    assert result.valid is False and any('expected 59' in e for e in result.errors)
