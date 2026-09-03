"""ME-F1 frontier study: registered objects (frozen with design V1).

An *instance* is a **discovery campaign**: ``k`` INDEPENDENT sub-ladders ("blocks"),
each a monotone chain of constraint systems over its own variable set, sharing one
frozen resource budget.  Within a block, rung ``i``'s constraint set is a strict subset
of rung ``i+1``'s, so the solution sets are nested downward::

    solutions(rung 0) >= solutions(rung 1) >= ... >= solutions(rung L-1)   [within a block]

That nesting is the whole epistemic point of this world.  It licenses exactly two
generalising inferences and forbids their converses:

* a **verified witness** at rung ``i`` licenses ``SATISFIABLE`` at every rung
  ``<= i`` **of the same block** (downward closure), and
* a **completed refutation** at rung ``i`` licenses ``UNSATISFIABLE`` at every
  rung ``>= i`` **of the same block** (upward closure).

Blocks are independent, and that independence is load-bearing.  With a single ladder,
two verified events bracketing the boundary entail *every* rung, so the primary endpoint
saturates however hard the rungs are made -- measured on the development split at
n_vars=40, where deterministic arms scored 12/12.  Splitting the campaign into blocks
makes the arm buy a bracket in each block separately, which is what turns the endpoint
back into a measurement of how well a controller allocates a binding budget.

Failing to find a witness licenses nothing at all.  An arm that converts
"I searched and did not find one" into ``UNSATISFIABLE`` -- or that generalises a
witness *upward* -- has made an unwarranted claim, and this module gives the
scorer the structure it needs to detect that from the arm's own execution log,
without consulting ground truth.

Nothing here is authorizing.  The obstruction/locus vocabulary is a registered
*subset* of ``MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md`` S4.2/S4.3:
this world faithfully realises levels 0-4 only, and the design says so rather
than pretending levels 5-6 have a realisation here (design S2.4).

Ground truth is NEVER an attribute an arm can read.  It is attached to the
campaign only by ``mef1_reference`` after the arms have run, and the arm-facing
views in this module deliberately do not carry it.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

# ---- registered vocabularies ------------------------------------------------------------

#: Terminal an arm may assign to a single rung.
VERDICTS: tuple[str, ...] = ("SATISFIABLE", "UNSATISFIABLE", "UNRESOLVED")

#: How an arm says its verdict is licensed.  Only the first three can ever be valid;
#: ``NONE`` is the honest label for "I am asserting this without a licence", and is
#: retained in the vocabulary precisely so that an arm *can* be honest about it.
WARRANTS: tuple[str, ...] = (
    "VERIFIED_WITNESS",      # this rung: a mechanically verified satisfying assignment
    "MONOTONE_CLOSURE",      # inherited from a verified witness below / refutation above
    "COMPLETED_REFUTATION",  # this rung: an exhaustive search that closed the space
    "NONE",                  # asserted without a licence
)

#: Tools.  Identical for every arm (design S4.1: the identical-toolbox constraint).
TOOLS: tuple[str, ...] = ("local_search", "exact_solve", "preprocess", "stop")

PREPROCESS_MODES: tuple[str, ...] = ("none", "unit_pure", "subsumption", "symmetry")

#: Registered escalation levels that this world *faithfully* realises.  Levels 5-6 of
#: the protocol (method/tool invention, workflow revision) have no faithful realisation
#: in a fixed-toolbox world and are therefore out of scope by registration, not by
#: oversight (design S2.4).
LEVEL_NAMES: dict[int, str] = {
    0: "ACTION_PARAMETER",              # more budget, same tool, same rung, same encoding
    1: "LOCAL_REPAIR_COMPOSITION",      # restart / reseed / switch heuristic within a tool
    2: "MODEL_HYPOTHESIS_EXPANSION",    # switch tool class (local search <-> exact)
    3: "REPRESENTATION_REGIME_TRANSITION",  # re-encode: preprocess mode change
    4: "PROBLEM_OBJECTIVE_REFORMULATION",   # attack a different rung / a relaxation
}
MAX_LEVEL = 4

#: Obstruction classes an arm may diagnose for a rung it has failed to settle.
#: Subset of protocol S4.2 restricted to those with a faithful realisation here.
OBSTRUCTION_CLASSES: tuple[str, ...] = (
    "SEARCH_INSUFFICIENT",          # more of the same search plausibly settles it
    "REPRESENTATION_INSUFFICIENT",  # the encoding is the obstacle
    "MODEL_FAMILY_INADEQUATE",      # wrong tool class for this rung's structure
    "PROBE_ACTION_INSUFFICIENT",    # budget granularity / allocation is the obstacle
    "NO_OBSTRUCTION",               # settled
    "CANNOT_IDENTIFY",              # the evidence does not discriminate
)

#: Discrepancy loci (protocol S4.3 subset).
LOCI: tuple[str, ...] = (
    "TARGET_WORLD",
    "REPRESENTATION_REGIME",
    "PROCESS_TOOL_WORKFLOW",
    "NO_MATERIAL_DISCREPANCY",
    "CANNOT_IDENTIFY",
)

#: Ground-truth status of a rung, established only by ``mef1_reference``.
GT_STATUS: tuple[str, ...] = ("SAT", "UNSAT", "UNSETTLED")


# ---- registered objects -----------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Clause:
    """A 3-literal clause.  Literals are signed 1-based variable indices."""

    lits: tuple[int, ...]

    def satisfied_by(self, assign: tuple[bool, ...]) -> bool:
        for lit in self.lits:
            if assign[abs(lit) - 1] == (lit > 0):
                return True
        return False


@dataclass(frozen=True, slots=True)
class Block:
    """One independent sub-ladder: its own variable set and its own clause pool.

    Blocks are the reason this world does not collapse.  Monotone closure is a powerful
    inference, and within a single ladder two verified events that bracket the boundary
    entail *every* rung -- which makes the primary endpoint saturate no matter how hard
    the individual rungs are.  Partitioning a campaign into independent blocks makes the
    arm pay for a bracket in each block separately, so the primary rate is continuous in
    the budget and, more importantly, sensitive to how well the arm allocates it.
    """

    block_id: int
    n_vars: int
    pool: tuple[Clause, ...]


@dataclass(frozen=True, slots=True)
class Rung:
    """One constraint system, inside one block.

    ``clause_count`` clauses are the *prefix* of that block's clause pool, which is what
    makes each sub-ladder monotone by construction rather than by check.
    """

    index: int          # global index across the campaign
    block: int          # which independent sub-ladder this rung belongs to
    local_index: int    # position within that sub-ladder
    n_vars: int
    clause_count: int

    def clauses(self, pool: tuple[Clause, ...]) -> tuple[Clause, ...]:
        return pool[: self.clause_count]


@dataclass(frozen=True, slots=True)
class Campaign:
    """A discovery campaign: the unit of analysis and the unit of budget.

    The arm sees ``arm_view()``.  It never sees ``pool`` in solved form, and never
    sees ground truth -- ground truth is not even a field of this object.
    """

    campaign_id: str
    family: str
    blocks: tuple[Block, ...]
    rungs: tuple[Rung, ...]
    budget_checks: int
    max_control_calls: int
    seed: int

    def __post_init__(self) -> None:
        for b in self.blocks:
            counts = [r.clause_count for r in self.rungs if r.block == b.block_id]
            if counts != sorted(counts) or len(set(counts)) != len(counts):
                raise ValueError(f"block {b.block_id} ladder must be strictly increasing")
            if counts and counts[-1] > len(b.pool):
                raise ValueError(f"block {b.block_id} top rung exceeds its clause pool")

    def block_of(self, rung_index: int) -> Block:
        return self.blocks[self.rungs[rung_index].block]

    def pool_of(self, rung_index: int) -> tuple[Clause, ...]:
        return self.block_of(rung_index).pool

    def rungs_in_block(self, block_id: int) -> tuple[Rung, ...]:
        return tuple(r for r in self.rungs if r.block == block_id)

    @property
    def n_rungs(self) -> int:
        return len(self.rungs)

    def arm_view(self) -> dict[str, Any]:
        """Exactly what every arm is told about the campaign before it acts.

        Deliberately excludes: ground truth, the reference budget, the seed, and any
        per-rung difficulty annotation.  Every arm sees this same dictionary, which is
        what makes the information matching in design S4.2 checkable rather than
        asserted.
        """
        return {
            "campaign_id": self.campaign_id,
            "family": self.family,
            "n_blocks": len(self.blocks),
            "n_rungs": self.n_rungs,
            "blocks": [{"block": b.block_id, "n_vars": b.n_vars,
                        "rungs": [r.index for r in self.rungs_in_block(b.block_id)],
                        "clause_counts": [r.clause_count
                                          for r in self.rungs_in_block(b.block_id)]}
                       for b in self.blocks],
            "budget_checks": self.budget_checks,
            "max_control_calls": self.max_control_calls,
            "monotonicity": (
                "WITHIN a block, a rung's clause set is a strict subset of the next rung's in "
                "that block, so a verified witness at a rung also satisfies every lower rung "
                "OF THE SAME BLOCK, and a completed refutation at a rung also refutes every "
                "higher rung OF THE SAME BLOCK. Blocks are independent: nothing established "
                "in one block licenses anything in another."
            ),
            "tools": list(TOOLS),
            "preprocess_modes": list(PREPROCESS_MODES),
        }


@dataclass(frozen=True, slots=True)
class Action:
    """One metered toolbox invocation requested by an arm's control layer."""

    tool: str
    rung: int
    budget: int
    mode: str = "none"

    def __post_init__(self) -> None:
        if self.tool not in TOOLS:
            raise ValueError(f"unregistered tool: {self.tool}")
        if self.mode not in PREPROCESS_MODES:
            raise ValueError(f"unregistered preprocess mode: {self.mode}")


@dataclass(frozen=True, slots=True)
class ActionResult:
    """What the toolbox returns.  This is the arm's entire evidence base."""

    action: Action
    outcome: str  # WITNESS_FOUND | REFUTED | INCONCLUSIVE | PREPROCESSED | REJECTED
    checks_spent: int
    witness: tuple[bool, ...] | None = None
    refutation_complete: bool = False
    note: str = ""


@dataclass(frozen=True, slots=True)
class Claim:
    """A verdict an arm asserts about one rung, with the licence it asserts for it."""

    rung: int
    verdict: str
    warrant: str
    source_rung: int | None = None  # for MONOTONE_CLOSURE: the rung the licence comes from

    def __post_init__(self) -> None:
        if self.verdict not in VERDICTS:
            raise ValueError(f"unregistered verdict: {self.verdict}")
        if self.warrant not in WARRANTS:
            raise ValueError(f"unregistered warrant: {self.warrant}")


@dataclass
class CampaignRecord:
    """Everything one arm did on one campaign.  The scorer reads only this."""

    campaign_id: str
    arm_id: str
    actions: list[ActionResult] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    diagnoses: dict[int, tuple[str, str]] = field(default_factory=dict)  # rung -> (class, locus)
    checks_spent: int = 0
    model_calls: int = 0
    model_tokens: int = 0
    wall_ms: int = 0
    stopped_early: bool = False
    cannot_check: str = ""  # non-empty => this record is excluded and the reason recorded

    def verified_witness_rungs(self) -> set[int]:
        return {r.action.rung for r in self.actions if r.outcome == "WITNESS_FOUND"}

    def completed_refutation_rungs(self) -> set[int]:
        return {r.action.rung for r in self.actions if r.outcome == "REFUTED" and r.refutation_complete}


# ---- warrant validity (structural; ground truth NOT consulted) ---------------------------


def warrant_is_valid(claim: Claim, record: CampaignRecord,
                     block_of: dict[int, int] | None = None) -> tuple[bool, str]:
    """Is this claim *licensed* by what the arm actually established?

    This is the study's laundering detector, and it is deliberately independent of
    ground truth: it asks only whether the arm's own execution log entitles it to the
    claim it made.  An arm can therefore be *correct and unwarranted* (a lucky guess)
    or *wrong and warranted* (only possible if the toolbox is unsound, which G0b
    checks).  Keeping the two axes separate is what lets the receipt distinguish
    "got it right" from "was entitled to say so".

    Returns ``(valid, reason)``.
    """
    if claim.verdict == "UNRESOLVED":
        # An honest non-answer needs no licence, and must never be counted as one.
        return (claim.warrant == "NONE", "UNRESOLVED must carry warrant NONE")

    if claim.warrant == "NONE":
        return (False, "verdict asserted with no warrant")

    witnesses = record.verified_witness_rungs()
    refutations = record.completed_refutation_rungs()
    if block_of is not None:
        # Closure is block-local: evidence from another sub-ladder licenses nothing.
        blk = block_of.get(claim.rung)
        witnesses = {w for w in witnesses if block_of.get(w) == blk}
        refutations = {r for r in refutations if block_of.get(r) == blk}

    if claim.verdict == "SATISFIABLE":
        if claim.warrant == "VERIFIED_WITNESS":
            ok = claim.rung in witnesses
            return (ok, "" if ok else "no verified witness at this rung")
        if claim.warrant == "MONOTONE_CLOSURE":
            # Licensed only DOWNWARD from a witness at a rung >= this one.
            src = claim.source_rung
            if src is None:
                ok = any(w >= claim.rung for w in witnesses)
                return (ok, "" if ok else "no witness at or above this rung to close downward from")
            ok = src in witnesses and src >= claim.rung
            return (ok, "" if ok else f"source rung {src} is not a verified witness at or above {claim.rung}")
        return (False, "COMPLETED_REFUTATION cannot license SATISFIABLE")

    # UNSATISFIABLE
    if claim.warrant == "COMPLETED_REFUTATION":
        ok = claim.rung in refutations
        return (ok, "" if ok else "no completed refutation at this rung")
    if claim.warrant == "MONOTONE_CLOSURE":
        # Licensed only UPWARD from a refutation at a rung <= this one.
        src = claim.source_rung
        if src is None:
            ok = any(r <= claim.rung for r in refutations)
            return (ok, "" if ok else "no refutation at or below this rung to close upward from")
        ok = src in refutations and src <= claim.rung
        return (ok, "" if ok else f"source rung {src} is not a completed refutation at or below {claim.rung}")
    return (False, "VERIFIED_WITNESS cannot license UNSATISFIABLE")


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode()).hexdigest()
