from __future__ import annotations

import pytest

from orion_v2.transfer_formal_mechanics import FiniteCategory


def test_finite_category_rejects_missing_composable_pair() -> None:
    with pytest.raises(ValueError, match="composition table"):
        FiniteCategory(
            objects=("A", "B"),
            morphisms=("idA", "idB", "f"),
            source_target=(("idA", "A", "A"), ("idB", "B", "B"), ("f", "A", "B")),
            identities=(("A", "idA"), ("B", "idB")),
            composition=(("idA", "idA", "idA"), ("idB", "idB", "idB"), ("f", "idB", "f")),
        )


def test_finite_category_rejects_wrong_composite_endpoint() -> None:
    with pytest.raises(ValueError, match="incorrect endpoints"):
        FiniteCategory(
            objects=("A", "B"),
            morphisms=("idA", "idB", "f"),
            source_target=(("idA", "A", "A"), ("idB", "B", "B"), ("f", "A", "B")),
            identities=(("A", "idA"), ("B", "idB")),
            composition=(
                ("idA", "idA", "idA"),
                ("idB", "idB", "idB"),
                ("idA", "f", "idA"),
                ("f", "idB", "f"),
            ),
        )
