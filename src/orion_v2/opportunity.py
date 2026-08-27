from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class OpportunityStatus(str, Enum):
    PROPOSAL_ONLY="PROPOSAL_ONLY"; READY_FOR_PROTECTED_TRIAGE="READY_FOR_PROTECTED_TRIAGE"; INTERESTINGNESS_ONLY="INTERESTINGNESS_ONLY"; BLOCKED_NO_DOWNSTREAM_DECISION="BLOCKED_NO_DOWNSTREAM_DECISION"; CANNOT_CHECK="CANNOT_CHECK"

@dataclass(frozen=True, slots=True)
class ResearchOpportunityCandidate:
    opportunity_id:str; problem_statement:str; observation_ids:tuple[str,...]; anomaly_or_gap_ids:tuple[str,...]; candidate_mechanism_ids:tuple[str,...]; discriminating_probe_ids:tuple[str,...]; falsifier_ids:tuple[str,...]; downstream_decision_ids:tuple[str,...]; donor_ids:tuple[str,...]=(); agenda_authority_required:bool=True; protected_outcome_seen:bool=False
    def __post_init__(self)->None:
        if not self.opportunity_id.strip() or not self.problem_statement.strip(): raise ValueError("opportunity identity and statement must be non-blank")
        for name in ("observation_ids","anomaly_or_gap_ids","candidate_mechanism_ids","discriminating_probe_ids","falsifier_ids","downstream_decision_ids","donor_ids"):
            if any(not item.strip() for item in getattr(self,name)): raise ValueError(f"{name} may not contain blanks")

def assess_opportunity(candidate:ResearchOpportunityCandidate)->OpportunityStatus:
    if candidate.protected_outcome_seen: return OpportunityStatus.CANNOT_CHECK
    if not candidate.downstream_decision_ids: return OpportunityStatus.BLOCKED_NO_DOWNSTREAM_DECISION
    if not candidate.falsifier_ids or not candidate.discriminating_probe_ids: return OpportunityStatus.INTERESTINGNESS_ONLY
    if not candidate.observation_ids or not candidate.anomaly_or_gap_ids: return OpportunityStatus.PROPOSAL_ONLY
    return OpportunityStatus.READY_FOR_PROTECTED_TRIAGE
