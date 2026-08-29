import pytest
from orion_v2.provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance

def test_component_level_multi_parent_inheritance() -> None:
    graph = ReticulateProvenance(nodes=(ProvenanceNode("representation-v1", "representation", "v1"), ProvenanceNode("method-v1", "method", "v1"), ProvenanceNode("framework-v2", "framework", "v2"), ProvenanceNode("paper-v2", "paper", "v2")), edges=(ProvenanceEdge("representation-v1", "framework-v2", InheritanceRelation.REFINES, "representation"), ProvenanceEdge("method-v1", "framework-v2", InheritanceRelation.COMPOSES, "method"), ProvenanceEdge("framework-v2", "paper-v2", InheritanceRelation.DERIVES, "claim")))
    assert graph.parents("framework-v2") == ("method-v1", "representation-v1")
    assert graph.affected_by_revocation("representation-v1") == ("representation-v1", "framework-v2", "paper-v2")
    assert graph.affected_by_revocation("representation-v1", component="representation") == ("representation-v1", "framework-v2")

def test_provenance_cycle_is_rejected() -> None:
    with pytest.raises(ValueError, match="acyclic"):
        ReticulateProvenance(nodes=(ProvenanceNode("a", "x", "1"), ProvenanceNode("b", "x", "1")), edges=(ProvenanceEdge("a", "b", InheritanceRelation.DERIVES, "x"), ProvenanceEdge("b", "a", InheritanceRelation.DERIVES, "x")))
