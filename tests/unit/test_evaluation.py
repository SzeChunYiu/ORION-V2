import pytest

from orion_v2.evaluation import CapabilityParityRecord, ParityDisposition, SaturationVector


def test_deprecation_requires_protected_noninferiority() -> None:
    with pytest.raises(ValueError, match="non-inferiority"):
        CapabilityParityRecord(
            "SEARCH",
            ParityDisposition.DEPRECATE_AFTER_PROTECTED_NONINFERIORITY,
            ("v1:search",),
            ("v2:solver",),
        )


def test_saturation_fails_when_mandatory_routes_missing() -> None:
    vector = SaturationVector(0, 0, 0, 0, 0, 0, 0, 0, 0, False)
    assert vector.is_no_material_change() is False


def test_zero_vector_with_completed_routes_is_no_material_change() -> None:
    vector = SaturationVector(0, 0, 0, 0, 0, 0, 0, 0, 0, True)
    assert vector.is_no_material_change() is True
