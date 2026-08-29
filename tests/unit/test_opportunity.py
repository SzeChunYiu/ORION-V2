from orion_v2.opportunity import OpportunityStatus, ResearchOpportunityCandidate, assess_opportunity

def _candidate(**overrides):
    values=dict(opportunity_id="opportunity",problem_statement="explain unresolved regularity",observation_ids=("obs",),anomaly_or_gap_ids=("gap",),candidate_mechanism_ids=("mechanism",),discriminating_probe_ids=("probe",),falsifier_ids=("falsifier",),downstream_decision_ids=("decision",)); values.update(overrides); return ResearchOpportunityCandidate(**values)

def test_complete_candidate_is_only_ready_for_protected_triage() -> None: assert assess_opportunity(_candidate()) is OpportunityStatus.READY_FOR_PROTECTED_TRIAGE

def test_no_falsifier_is_interestingness_only() -> None: assert assess_opportunity(_candidate(falsifier_ids=())) is OpportunityStatus.INTERESTINGNESS_ONLY

def test_protected_outcome_leakage_fails_closed() -> None: assert assess_opportunity(_candidate(protected_outcome_seen=True)) is OpportunityStatus.CANNOT_CHECK
