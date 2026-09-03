"""ME-F1 generator: fresh campaigns from a seed (frozen with design V1).

Campaigns are generated **after** the design is frozen, from a seed held in operator
custody whose sha256 is published in the design.  Nothing an arm could have been
tuned on -- or memorised -- is in the protected split, because the protected split
does not exist until the seed is revealed to the runner.

Each campaign draws ``n_blocks`` INDEPENDENT random 3-SAT clause pools, each over its
own ``n_vars`` variables, and takes prefixes of each as that block's sub-ladder.  Prefix
nesting makes every sub-ladder monotone *by construction*: no check can fail, because a
rung's clause set literally is a subset of the next rung's in the same block.  Blocks
share nothing, so an arm must establish a bracket in each block separately.

The rung densities straddle the satisfiability threshold of random 3-SAT
(alpha = m/n ~ 4.267), so a campaign contains satisfiable rungs low down, unsatisfiable
rungs high up, and -- the point of the study -- a band in the middle where settling a
rung within the arm budget is genuinely open.

FAMILIES.  ``F_CRITICAL`` straddles the threshold.  ``F_PLANTED`` plants a satisfying
assignment in every rung and is used ONLY for G0 generator validity and for clean
false-completion measurement: planting biases instances easier than critical density,
so planted campaigns are excluded from the primary endpoint by registration
(design S3.3), not by a post-hoc decision.
"""
from __future__ import annotations

import hashlib
import random

from mef1_model import Campaign, Clause

FAMILIES: tuple[str, ...] = ("F_CRITICAL", "F_PLANTED")

#: Frozen sub-ladder geometry.  Rung j of a block uses round(n_vars * alpha_j) clauses.
#: Five rungs straddling the random-3-SAT threshold (alpha ~ 4.267): two comfortably
#: satisfiable, one critical, two comfortably unsatisfiable.
ALPHAS: tuple[float, ...] = (3.2, 4.0, 4.267, 4.7, 5.6)


def seed_int(seed_text: str, campaign_index: int) -> int:
    h = hashlib.sha256(f"{seed_text}|{campaign_index}".encode()).digest()
    return int.from_bytes(h[:8], "big")


def _random_pool(rng: random.Random, n_vars: int, m: int) -> tuple[Clause, ...]:
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n_vars + 1), 3)
        out.append(Clause(tuple(v if rng.random() < 0.5 else -v for v in vs)))
    return tuple(out)


def _planted_pool(rng: random.Random, n_vars: int, m: int) -> tuple[Clause, ...]:
    """Every clause is satisfied by a hidden planted assignment, so every rung is SAT."""
    planted = tuple(rng.random() < 0.5 for _ in range(n_vars))
    out = []
    while len(out) < m:
        vs = rng.sample(range(1, n_vars + 1), 3)
        lits = tuple(v if rng.random() < 0.5 else -v for v in vs)
        if any(planted[abs(lit) - 1] == (lit > 0) for lit in lits):
            out.append(Clause(lits))
    return tuple(out)


def make_campaign(seed_text: str, index: int, family: str, n_vars: int,
                  budget_checks: int, max_control_calls: int,
                  n_blocks: int = 4) -> Campaign:
    if family not in FAMILIES:
        raise ValueError(f"unregistered family: {family}")
    s = seed_int(seed_text, index)
    rng = random.Random(s)
    top = int(round(n_vars * ALPHAS[-1]))

    from mef1_model import Block, Rung
    blocks: list[Block] = []
    rungs: list[Rung] = []
    gi = 0
    for b in range(n_blocks):
        pool = (_planted_pool(rng, n_vars, top) if family == "F_PLANTED"
                else _random_pool(rng, n_vars, top))
        blocks.append(Block(b, n_vars, pool))
        counts = sorted({max(1, int(round(n_vars * a))) for a in ALPHAS})
        for j, c in enumerate(counts):
            rungs.append(Rung(gi, b, j, n_vars, c))
            gi += 1

    return Campaign(
        campaign_id=f"{family}-{index:04d}",
        family=family,
        blocks=tuple(blocks),
        rungs=tuple(rungs),
        budget_checks=budget_checks,
        max_control_calls=max_control_calls,
        seed=s,
    )


def make_split(seed_text: str, per_family: dict[str, int], n_vars: int,
               budget_checks: int, max_control_calls: int,
               n_blocks: int = 4) -> list[Campaign]:
    out: list[Campaign] = []
    idx = 0
    for family in FAMILIES:
        for _ in range(per_family.get(family, 0)):
            out.append(make_campaign(seed_text, idx, family, n_vars, budget_checks,
                                     max_control_calls, n_blocks))
            idx += 1
    return out
