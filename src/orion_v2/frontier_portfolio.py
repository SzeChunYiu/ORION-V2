from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations


class FrontierStatus(str, Enum):
    PARETO_PORTFOLIO_SET = "PARETO_PORTFOLIO_SET"
    NO_ADMISSIBLE_OPPORTUNITY = "NO_ADMISSIBLE_OPPORTUNITY"
    AGENDA_AUTHORITY_REQUIRED = "AGENDA_AUTHORITY_REQUIRED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class FrontierOpportunity:
    opportunity_id: str
    importance: float
    information_gain: float
    falsifiability: float
    tractability: float
    option_value: float
    cost: float
    risk: float
    diversity_tags: frozenset[str]
    downstream_decision_ids: tuple[str, ...]
    agenda_authority_required: bool = True
    protected_outcome_seen: bool = False

    def __post_init__(self) -> None:
        if not self.opportunity_id.strip() or self.cost < 0 or self.risk < 0:
            raise ValueError("opportunity identity, cost and risk are invalid")
        for value in (
            self.importance,
            self.information_gain,
            self.falsifiability,
            self.tractability,
            self.option_value,
        ):
            if value < 0:
                raise ValueError(
                    "opportunity benefit coordinates must be non-negative"
                )
        if any(not tag.strip() for tag in self.diversity_tags):
            raise ValueError("diversity tags may not be blank")

    @property
    def admissible(self) -> bool:
        return (
            not self.protected_outcome_seen
            and self.falsifiability > 0
            and bool(self.downstream_decision_ids)
        )


@dataclass(frozen=True, slots=True)
class FrontierPortfolio:
    opportunity_ids: tuple[str, ...]
    importance: float
    information_gain: float
    falsifiability: float
    tractability: float
    option_value: float
    diversity: int
    cost: float
    risk: float


def _portfolio(
    opportunities: tuple[FrontierOpportunity, ...],
) -> FrontierPortfolio:
    return FrontierPortfolio(
        tuple(sorted(item.opportunity_id for item in opportunities)),
        sum(item.importance for item in opportunities),
        sum(item.information_gain for item in opportunities),
        sum(item.falsifiability for item in opportunities),
        sum(item.tractability for item in opportunities),
        sum(item.option_value for item in opportunities),
        len(set().union(*(item.diversity_tags for item in opportunities))),
        sum(item.cost for item in opportunities),
        sum(item.risk for item in opportunities),
    )


def _dominates(left: FrontierPortfolio, right: FrontierPortfolio) -> bool:
    benefits_left = (
        left.importance,
        left.information_gain,
        left.falsifiability,
        left.tractability,
        left.option_value,
        left.diversity,
    )
    benefits_right = (
        right.importance,
        right.information_gain,
        right.falsifiability,
        right.tractability,
        right.option_value,
        right.diversity,
    )
    weak = (
        all(
            a >= b
            for a, b in zip(benefits_left, benefits_right, strict=True)
        )
        and left.cost <= right.cost
        and left.risk <= right.risk
    )
    strict = (
        any(
            a > b
            for a, b in zip(benefits_left, benefits_right, strict=True)
        )
        or left.cost < right.cost
        or left.risk < right.risk
    )
    return weak and strict


def pareto_frontier_portfolios(
    opportunities: tuple[FrontierOpportunity, ...],
    *,
    budget: float,
    risk_limit: float,
) -> tuple[FrontierPortfolio, ...]:
    if budget < 0 or risk_limit < 0:
        raise ValueError("budget and risk limit must be non-negative")
    admissible = tuple(item for item in opportunities if item.admissible)
    candidates: list[FrontierPortfolio] = []
    for size in range(1, len(admissible) + 1):
        for subset in combinations(admissible, size):
            portfolio = _portfolio(subset)
            if portfolio.cost <= budget and portfolio.risk <= risk_limit:
                candidates.append(portfolio)
    frontier = [
        candidate
        for candidate in candidates
        if not any(
            _dominates(other, candidate)
            for other in candidates
            if other != candidate
        )
    ]
    return tuple(sorted(frontier, key=lambda item: item.opportunity_ids))


def assess_frontier_portfolio(
    opportunities: tuple[FrontierOpportunity, ...],
    *,
    budget: float,
    risk_limit: float,
    agenda_authority_bound: bool,
) -> tuple[FrontierStatus, tuple[FrontierPortfolio, ...]]:
    if not agenda_authority_bound and any(
        item.admissible and item.agenda_authority_required
        for item in opportunities
    ):
        return FrontierStatus.AGENDA_AUTHORITY_REQUIRED, ()
    frontier = pareto_frontier_portfolios(
        opportunities, budget=budget, risk_limit=risk_limit
    )
    if not frontier:
        return FrontierStatus.NO_ADMISSIBLE_OPPORTUNITY, ()
    return FrontierStatus.PARETO_PORTFOLIO_SET, frontier
