from orion_v2.comparability import Anchor, ComparabilityCertificate, ComparabilityStatus

def _anchor() -> Anchor: return Anchor("anchor", "old", "new", ("construct", "scale"), uncertainty=0.1)

def test_exact_comparability_requires_anchors_and_invariants() -> None:
    certificate = ComparabilityCertificate("cert", "v1", "v2", "task", ("map",), (_anchor(),), ("construct", "scale"), accumulated_uncertainty=0.1, tolerance=0.2)
    assert certificate.status is ComparabilityStatus.COMPARABLE

def test_uncertainty_above_tolerance_is_partial_not_exact() -> None:
    certificate = ComparabilityCertificate("cert", "v1", "v2", "task", ("map",), (_anchor(),), ("construct", "scale"), accumulated_uncertainty=0.3, tolerance=0.2)
    assert certificate.status is ComparabilityStatus.PARTIALLY_COMPARABLE

def test_violated_invariant_is_noncomparable() -> None:
    certificate = ComparabilityCertificate("cert", "v1", "v2", "task", ("map",), (_anchor(),), ("construct", "scale"), violated_invariant_ids=("construct",))
    assert certificate.status is ComparabilityStatus.NONCOMPARABLE
