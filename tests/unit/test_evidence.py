from orion_v2.evidence import DependenceEdge, DependenceKind, EvidenceUnit, assess_evidence_dependence

def _unit(identifier: str) -> EvidenceUnit: return EvidenceUnit(identifier, "claim", f"source:{identifier}", "method")

def test_correlated_sources_do_not_count_as_independent() -> None:
    assessment = assess_evidence_dependence((_unit("a"), _unit("b"), _unit("c")), (DependenceEdge("a", "b", DependenceKind.SHARED_DATA, ("dataset:1",)),))
    assert assessment.naive_support_count == 3 and assessment.conservative_independent_support_count == 2

def test_unknown_dependence_fails_closed_when_complete_disposition_required() -> None:
    assessment = assess_evidence_dependence((_unit("a"), _unit("b"), _unit("c")), (DependenceEdge("a", "b", DependenceKind.DECLARED_INDEPENDENT, ("audit",)),), require_complete_pair_disposition=True)
    assert assessment.dependence_unknown is True and assessment.conservative_independent_support_count == 0
