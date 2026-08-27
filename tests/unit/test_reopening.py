from orion_v2.reopening import Commitment, CommitmentDisposition, SupportFamily, selective_reopen

def test_alternative_support_preserves_commitment() -> None:
    c=Commitment("claim",(SupportFamily("family-a",frozenset({"e1"})),SupportFamily("family-b",frozenset({"e2"}))))
    receipt=selective_reopen((c,),("e1",)); assert receipt.preserved_commitment_ids==("claim",) and receipt.reopened_commitment_ids==()

def test_reopening_propagates_to_dependent_commitment() -> None:
    base=Commitment("base",(SupportFamily("base-family",frozenset({"e1"})),)); derived=Commitment("derived",(SupportFamily("derived-family",frozenset(),frozenset({"base"})),))
    assert selective_reopen((base,derived),("e1",)).reopened_commitment_ids==("base","derived")

def test_dependency_cycle_is_cannot_check_not_silent_reopen() -> None:
    a=Commitment("a",(SupportFamily("fa",frozenset(),frozenset({"b"})),)); b=Commitment("b",(SupportFamily("fb",frozenset(),frozenset({"a"})),))
    assert all(r.disposition is CommitmentDisposition.CANNOT_CHECK_CYCLE for r in selective_reopen((a,b),()).records)
