from orion_v2.evidence_network import (
    DependenceCluster,
    EvidenceItem,
    EvidenceNetworkStatus,
    assess_evidence_network,
)


def test_correlated_sources_do_not_count_as_four_independent_sources() -> None:
    items = tuple(EvidenceItem(f"e{i}", 1, 1.0, 2) for i in range(4))
    cluster = DependenceCluster(
        "shared-model",
        tuple(item.evidence_id for item in items),
        0.5,
        "model-lineage",
    )
    result = assess_evidence_network(items, (cluster,))
    assert result.status is EvidenceNetworkStatus.DEPENDENCE_ADJUSTED
    assert result.naive_count == 4
    assert abs(result.effective_count - 1.6) < 1e-12
    assert result.adjusted_signed_support < result.naive_signed_support


def test_unidentified_dependence_is_not_independence() -> None:
    items = (
        EvidenceItem("a", 1, 1.0, 1),
        EvidenceItem("b", 1, 1.0, 1),
    )
    result = assess_evidence_network(
        items, (DependenceCluster("unknown", ("a", "b"), None),)
    )
    assert result.status is EvidenceNetworkStatus.DEPENDENCE_UNIDENTIFIED
    assert result.effective_count is None
