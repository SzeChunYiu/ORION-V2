from orion_v2.frontier_portfolio import (
    FrontierOpportunity,
    FrontierStatus,
    assess_frontier_portfolio,
)


def _opportunity(
    identifier: str,
    *,
    importance: float,
    info: float,
    cost: float,
    tag: str,
    falsifiability: float = 1.0,
) -> FrontierOpportunity:
    return FrontierOpportunity(
        identifier,
        importance,
        info,
        falsifiability,
        1.0,
        1.0,
        cost,
        0.1,
        frozenset({tag}),
        ("decision",),
    )


def test_frontier_returns_non_scalar_pareto_portfolios() -> None:
    opportunities = (
        _opportunity(
            "high-importance",
            importance=5,
            info=1,
            cost=2,
            tag="biology",
        ),
        _opportunity(
            "high-information",
            importance=1,
            info=5,
            cost=2,
            tag="physics",
        ),
    )
    status, portfolios = assess_frontier_portfolio(
        opportunities,
        budget=2,
        risk_limit=1,
        agenda_authority_bound=True,
    )
    assert status is FrontierStatus.PARETO_PORTFOLIO_SET
    assert {portfolio.opportunity_ids for portfolio in portfolios} == {
        ("high-importance",),
        ("high-information",),
    }


def test_interesting_but_unfalsifiable_item_is_not_admitted() -> None:
    item = _opportunity(
        "interesting",
        importance=10,
        info=10,
        cost=1,
        tag="novel",
        falsifiability=0,
    )
    status, portfolios = assess_frontier_portfolio(
        (item,),
        budget=10,
        risk_limit=10,
        agenda_authority_bound=True,
    )
    assert status is FrontierStatus.NO_ADMISSIBLE_OPPORTUNITY
    assert portfolios == ()
