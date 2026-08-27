"""Frontier-opportunity screening reference model V0.

This module separates scientific opportunity proposal from novelty, interestingness
and agenda authority. It is a small exact research aid, not an admitted problem-
finding system.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


BENEFIT_FIELDS = ("importance", "expected_information", "unmet_need", "novelty")
COST_FIELDS = ("cost", "risk")


class OpportunityInputError(ValueError):
    pass


def _number(record: Mapping[str, Any], field: str) -> float:
    value = record.get(field)
    if not isinstance(value, (int, float)):
        raise OpportunityInputError(f"{field} must be numeric")
    return float(value)


def classify_opportunity(
    record: Mapping[str, Any],
    budget: Mapping[str, float],
) -> str:
    """Classify proposal readiness without ranking scientific agendas."""

    for field in (*BENEFIT_FIELDS, *COST_FIELDS):
        _number(record, field)

    if not bool(record.get("ethically_admissible")):
        return "HARD_CONSTRAINT_BLOCKED"
    if not bool(record.get("falsifiable")) or not bool(
        record.get("decisive_probe_available")
    ):
        return "INTERESTINGNESS_WITHOUT_SCIENTIFIC_TEST"
    if _number(record, "cost") > float(budget.get("cost", 0.0)) or _number(
        record, "risk"
    ) > float(budget.get("risk", 0.0)):
        return "RESOURCE_INFEASIBLE"
    if str(record.get("authority_state")) == "EXTERNAL_AGENDA_AUTHORITY_REQUIRED":
        return "AGENDA_AUTHORITY_REQUIRED"
    if str(record.get("authority_state")) != "PROPOSAL_ALLOWED":
        return "CANNOT_CHECK"
    return "OPPORTUNITY_CANDIDATE"


def dominates(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Pareto dominance: benefits maximize; costs and risks minimize."""

    benefit_not_worse = all(_number(left, field) >= _number(right, field) for field in BENEFIT_FIELDS)
    cost_not_worse = all(_number(left, field) <= _number(right, field) for field in COST_FIELDS)
    strictly_better = any(_number(left, field) > _number(right, field) for field in BENEFIT_FIELDS) or any(
        _number(left, field) < _number(right, field) for field in COST_FIELDS
    )
    return benefit_not_worse and cost_not_worse and strictly_better


def pareto_frontier(records: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    ids = [str(record.get("id", "")) for record in records]
    if any(not item for item in ids) or len(set(ids)) != len(ids):
        raise OpportunityInputError("candidate ids must be non-empty and unique")
    survivors = [
        ids[index]
        for index, record in enumerate(records)
        if not any(
            other_index != index and dominates(other, record)
            for other_index, other in enumerate(records)
        )
    ]
    return tuple(sorted(survivors))


__all__ = [
    "BENEFIT_FIELDS",
    "COST_FIELDS",
    "OpportunityInputError",
    "classify_opportunity",
    "dominates",
    "pareto_frontier",
]
