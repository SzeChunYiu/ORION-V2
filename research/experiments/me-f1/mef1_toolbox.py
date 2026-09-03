"""ME-F1 toolbox: the identical search primitives every arm is given (frozen with design V1).

Design S4.1 (identical-toolbox constraint).  Every arm -- ``SIMPLE_DIRECT``, the
parent federation, ``M`` and every ablation -- calls exactly these functions through
exactly this meter.  No arm has a primitive another lacks.  This forecloses the
strongest objection available against any residual this study might find: that the
openness of the search was an artefact of denying some arm a solver.

**The meter.**  The single budget unit is the *constraint check*: one evaluation of
one clause against one assignment.  It is the only primitive shared by stochastic
local search and backtracking search, it is hardware- and language-independent, and
it is exactly countable, which wall-clock is not.  Wall-clock is recorded as a
reported secondary and never as a matched budget (design S5.3).

Soundness is the property G0b checks: ``WITNESS_FOUND`` is emitted only with an
assignment this module has just verified clause-by-clause, and ``REFUTED`` with
``refutation_complete=True`` only when the DPLL search exhausted its space without
hitting the node limit.  Nothing else may set those flags.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from mef1_model import Action, ActionResult, Campaign, Clause


class BudgetExhausted(Exception):
    """Raised inside a primitive when the campaign budget is spent."""


@dataclass
class Meter:
    """Campaign-level budget in constraint checks.  Shared by every tool call."""

    limit: int
    spent: int = 0

    @property
    def remaining(self) -> int:
        return max(0, self.limit - self.spent)

    def charge(self, n: int = 1) -> None:
        self.spent += n
        if self.spent >= self.limit:
            raise BudgetExhausted()


def _clauses_for(campaign: Campaign, rung_index: int, mode: str) -> tuple[tuple[Clause, ...], int]:
    """Clause list for a rung under a preprocessing mode, plus the checks preprocessing cost.

    Preprocessing is a *representation* move (level 3): it can only remove clauses that
    are redundant for satisfiability, so it never changes any rung's true status.  That
    invariant is asserted by G0b; it is what makes re-encoding a legitimate escalation
    rather than a way to change the answer.
    """
    rung = campaign.rungs[rung_index]
    base = rung.clauses(campaign.pool_of(rung_index))
    if mode == "none":
        return base, 0

    cost = len(base)
    if mode == "unit_pure":
        # Pure-literal elimination: drop clauses containing a literal whose complement
        # never appears.  Satisfiability-preserving.
        present: set[int] = set()
        for c in base:
            present.update(c.lits)
        pure = {lit for lit in present if -lit not in present}
        if not pure:
            return base, cost
        kept = tuple(c for c in base if not any(lit in pure for lit in c.lits))
        return kept, cost

    if mode == "subsumption":
        # Remove clauses subsumed by a shorter one.  All clauses here are 3-literal, so
        # this only removes exact duplicates -- honest, and honestly weak.
        seen: set[frozenset[int]] = set()
        kept_list = []
        for c in base:
            key = frozenset(c.lits)
            if key not in seen:
                seen.add(key)
                kept_list.append(c)
        return tuple(kept_list), cost

    if mode == "symmetry":
        # Variable-order canonicalisation: does not change the clause set, but reorders
        # it, which changes the trajectory of both search tools.  Satisfiability is
        # trivially preserved because the multiset of clauses is unchanged.
        kept = tuple(sorted(base, key=lambda c: tuple(sorted(c.lits))))
        return kept, cost

    raise ValueError(f"unregistered preprocess mode: {mode}")


def _base_clauses(campaign: Campaign, rung_index: int) -> tuple[Clause, ...]:
    """The rung's clauses as generated -- the UNPREPROCESSED formula, which is what
    ``WITNESS_FOUND`` must be verified against (design G0b)."""
    rung = campaign.rungs[rung_index]
    return rung.clauses(campaign.pool_of(rung_index))


def _lift_witness(campaign: Campaign, rung_index: int, mode: str,
                  witness: tuple[bool, ...]) -> tuple[bool, ...]:
    """Lift a witness for the PREPROCESSED formula back to the unpreprocessed rung.

    ``unit_pure`` deletes every clause containing a pure literal *without recording the
    assignment that justified the deletion*, so a satisfying assignment of the reduced
    formula need not satisfy the rung itself.  Pure-literal elimination preserves
    satisfiability only when the pure literals are then set: if ``+v`` is pure then ``-v``
    never occurs anywhere, and every surviving clause is free of ``v`` altogether, so
    forcing every pure literal true is consistent and cannot disturb a surviving clause.
    ``subsumption`` deletes only duplicates and ``symmetry`` only reorders, so both are
    lifted by the identity.  The caller verifies the lifted witness against the
    unpreprocessed rung regardless, so the invariant holds for every mode structurally
    rather than by this argument.
    """
    if mode != "unit_pure":
        return witness
    base = _base_clauses(campaign, rung_index)
    present: set[int] = set()
    for c in base:
        present.update(c.lits)
    pure = {lit for lit in present if -lit not in present}
    if not pure:
        return witness
    out = list(witness)
    for lit in pure:
        out[abs(lit) - 1] = lit > 0
    return tuple(out)


def local_search(campaign: Campaign, meter: Meter, rung_index: int, budget: int,
                 mode: str, seed: int) -> ActionResult:
    """WalkSAT.  Returns a *verified* witness or INCONCLUSIVE.  Never returns UNSAT.

    A local-search failure is evidence of nothing: that asymmetry is the substantive
    fact this world is built around, and the reason ``REFUTED`` is unreachable here.
    """
    action = Action("local_search", rung_index, budget, mode)
    clauses, pre_cost = _clauses_for(campaign, rung_index, mode)
    start = meter.spent
    rng = random.Random(seed)
    n = campaign.rungs[rung_index].n_vars
    allow = min(budget, meter.remaining)
    if allow <= 0:
        return ActionResult(action, "REJECTED", 0, note="no budget remaining")

    try:
        if pre_cost:
            meter.charge(pre_cost)
        assign = tuple(rng.random() < 0.5 for _ in range(n))
        assign_l = list(assign)
        while meter.spent - start < allow:
            unsat: list[Clause] = []
            for c in clauses:
                meter.charge()
                if not c.satisfied_by(tuple(assign_l)):
                    unsat.append(c)
                    if len(unsat) > 64:
                        break
            if not unsat:
                witness = _lift_witness(campaign, rung_index, mode, tuple(assign_l))
                # G0b: WITNESS_FOUND is emitted only against the UNPREPROCESSED rung.
                if not _verify(_base_clauses(campaign, rung_index), witness):
                    return ActionResult(action, "INCONCLUSIVE", meter.spent - start,
                                        note="witness does not satisfy the unpreprocessed rung")
                return ActionResult(action, "WITNESS_FOUND", meter.spent - start, witness=witness)
            c = unsat[rng.randrange(len(unsat))]
            if rng.random() < 0.5:
                v = abs(c.lits[rng.randrange(len(c.lits))]) - 1
            else:
                best, best_break = None, None
                for lit in c.lits:
                    idx = abs(lit) - 1
                    assign_l[idx] = not assign_l[idx]
                    brk = 0
                    for cc in clauses:
                        meter.charge()
                        if not cc.satisfied_by(tuple(assign_l)):
                            brk += 1
                            if best_break is not None and brk > best_break:
                                break
                    assign_l[idx] = not assign_l[idx]
                    if best_break is None or brk < best_break:
                        best, best_break = idx, brk
                v = best if best is not None else abs(c.lits[0]) - 1
            assign_l[v] = not assign_l[v]
    except BudgetExhausted:
        pass
    return ActionResult(action, "INCONCLUSIVE", meter.spent - start,
                        note="search budget exhausted without a witness")


def exact_solve(campaign: Campaign, meter: Meter, rung_index: int, node_limit: int,
                mode: str) -> ActionResult:
    """DPLL with unit propagation.

    Emits ``REFUTED`` with ``refutation_complete=True`` **only** when the search space
    was exhausted within the node limit.  Hitting the node limit yields INCONCLUSIVE --
    the distinction the whole study turns on.
    """
    action = Action("exact_solve", rung_index, node_limit, mode)
    clauses, pre_cost = _clauses_for(campaign, rung_index, mode)
    start = meter.spent
    nodes = [0]
    exhausted = [True]

    try:
        if pre_cost:
            meter.charge(pre_cost)
        assign: dict[int, bool] = {}
        witness = _dpll(clauses, campaign.rungs[rung_index].n_vars, assign, meter,
                        nodes, node_limit, exhausted)
    except BudgetExhausted:
        return ActionResult(action, "INCONCLUSIVE", meter.spent - start,
                            note="campaign budget exhausted mid-search")

    spent = meter.spent - start
    if witness is not None:
        witness = _lift_witness(campaign, rung_index, mode, witness)
        # G0b: WITNESS_FOUND is emitted only against the UNPREPROCESSED rung.
        if not _verify(_base_clauses(campaign, rung_index), witness):
            return ActionResult(action, "INCONCLUSIVE", spent,
                                note="witness does not satisfy the unpreprocessed rung")
        return ActionResult(action, "WITNESS_FOUND", spent, witness=witness)
    if exhausted[0]:
        return ActionResult(action, "REFUTED", spent, refutation_complete=True,
                            note=f"search space exhausted in {nodes[0]} nodes")
    return ActionResult(action, "INCONCLUSIVE", spent,
                        note=f"node limit {node_limit} reached; space not exhausted")


def _dpll(clauses: tuple[Clause, ...], n_vars: int, assign: dict[int, bool], meter: Meter,
          nodes: list[int], node_limit: int, exhausted: list[bool]) -> tuple[bool, ...] | None:
    nodes[0] += 1
    if nodes[0] > node_limit:
        exhausted[0] = False
        return None

    # unit propagation
    local = dict(assign)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            meter.charge()
            unassigned: list[int] = []
            sat = False
            for lit in c.lits:
                v = abs(lit)
                if v in local:
                    if local[v] == (lit > 0):
                        sat = True
                        break
                else:
                    unassigned.append(lit)
            if sat:
                continue
            if not unassigned:
                return None  # conflict; this branch is genuinely closed
            if len(unassigned) == 1:
                lit = unassigned[0]
                local[abs(lit)] = lit > 0
                changed = True

    undecided = [v for v in range(1, n_vars + 1) if v not in local]
    if not undecided:
        full = tuple(local.get(v, False) for v in range(1, n_vars + 1))
        return full if _verify_counted(clauses, full, meter) else None

    var = undecided[0]
    for val in (True, False):
        nxt = dict(local)
        nxt[var] = val
        got = _dpll(clauses, n_vars, nxt, meter, nodes, node_limit, exhausted)
        if got is not None:
            return got
        if not exhausted[0]:
            return None
    return None


def _verify(clauses: tuple[Clause, ...], assign: tuple[bool, ...]) -> bool:
    """Free mechanical verification (design S2.3): never metered, available to all arms."""
    return all(c.satisfied_by(assign) for c in clauses)


def _verify_counted(clauses: tuple[Clause, ...], assign: tuple[bool, ...], meter: Meter) -> bool:
    for c in clauses:
        meter.charge()
        if not c.satisfied_by(assign):
            return False
    return True


def verify_witness(campaign: Campaign, rung_index: int, assign: tuple[bool, ...]) -> bool:
    """Public, free verifier over the UNPREPROCESSED rung -- the definition of truth here."""
    rung = campaign.rungs[rung_index]
    return _verify(rung.clauses(campaign.pool_of(rung_index)), assign)


def run_action(campaign: Campaign, meter: Meter, action: Action, seed: int) -> ActionResult:
    """Dispatch one metered action.  The only entry point arms are permitted to use."""
    if action.rung < 0 or action.rung >= campaign.n_rungs:
        return ActionResult(action, "REJECTED", 0, note="rung out of range")
    if action.tool == "stop":
        return ActionResult(action, "REJECTED", 0, note="stop is a control decision, not a tool")
    if action.tool == "preprocess":
        _, cost = _clauses_for(campaign, action.rung, action.mode)
        charged = min(cost, meter.remaining)
        meter.spent += charged
        return ActionResult(action, "PREPROCESSED", charged, note=f"mode={action.mode}")
    if action.tool == "local_search":
        return local_search(campaign, meter, action.rung, max(1, action.budget), action.mode, seed)
    if action.tool == "exact_solve":
        return exact_solve(campaign, meter, action.rung, max(1, action.budget), action.mode)
    return ActionResult(action, "REJECTED", 0, note=f"unknown tool {action.tool}")
