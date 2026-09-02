"""ME-X2 exact oracle and environment (frozen with design V1).

Oracle (truth known; never imported by an arm):
  tests   = probes + level<=1 interventions used as repair-as-test discriminators
  a test separates the truth from rival r when its registered outcome differs
  the *total* of a test set S is cost(S) + cost(min fix of truth), except that a
  repair in S that resolves the truth already is the fix (no extra fix cost)
  affordable(S) <-> total(S) <= budget
  identifiable          <-> some affordable S separates every rival
  U (indistinguishable) = {truth} + rivals no affordable S separates individually
  identifiable_up_to_U  <-> some affordable S separates every rival outside U
  oracle_class / locus  = the common class / locus over U (else CANNOT_IDENTIFY)
  oracle_level          = the common minimum-fix level over U when every member of U
                          has the same minimum-fix intervention, else null
  (if not identifiable_up_to_U everything is CANNOT_IDENTIFY / null)
Two implementations compute the minimal separating totals: bitmask enumeration
over all 2^n test subsets and an independent branch-and-bound DFS; they must
agree on every instance (gate G0b).

Environment: runs an arm policy against the hidden truth; enforces the budget
and a step cap; records the trajectory used by the scorer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Callable

from mex2_model import RECURRENCE, SUCCESS, Action, Instance, Intervention, Probe, Step

INF = 10 ** 9
MAX_STEPS = 40


# ---- public view (truth stripped) ---------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PublicInstance:
    instance_id: str
    template: str
    symptom: str
    pattern: str
    apparent_class: str
    causes: tuple
    probes: tuple[Probe, ...]
    interventions: tuple[Intervention, ...]
    budget: int

    def cause(self, cause_id: str):
        for c in self.causes:
            if c.cause_id == cause_id:
                return c
        raise KeyError(cause_id)

    def probe(self, probe_id: str) -> Probe:
        for p in self.probes:
            if p.probe_id == probe_id:
                return p
        raise KeyError(probe_id)

    def intervention(self, intervention_id: str) -> Intervention:
        for i in self.interventions:
            if i.intervention_id == intervention_id:
                return i
        raise KeyError(intervention_id)

    def live_ids(self) -> tuple[str, ...]:
        return tuple(c.cause_id for c in self.causes)

    def min_fix(self, cause_id: str) -> Intervention | None:
        cands = [i for i in self.interventions if cause_id in i.resolves]
        return min(cands, key=lambda i: (i.level, i.cost, i.intervention_id)) if cands else None


def public_of(inst: Instance) -> PublicInstance:
    return PublicInstance(inst.instance_id, inst.template, inst.symptom, inst.pattern, inst.apparent_class, inst.causes, inst.probes, inst.interventions, inst.budget)


# ---- tests ---------------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Test:
    test_id: str
    kind: str  # PROBE | REPAIR
    cost: int
    outcome: Callable[[str], str]
    resolves: tuple[str, ...] = ()


def tests_for(inst: Instance | PublicInstance) -> list[Test]:
    tests = [Test(p.probe_id, "PROBE", p.cost, p.outcome) for p in inst.probes]
    tests += [Test(i.intervention_id, "REPAIR", i.cost, i.outcome, i.resolves) for i in inst.interventions if i.is_cheap]
    return tests


def separated(test: Test, truth: str, rivals: tuple[str, ...]) -> frozenset[str]:
    t = test.outcome(truth)
    return frozenset(r for r in rivals if test.outcome(r) != t)


# ---- exact enumeration ------------------------------------------------------------------------

def _subset_totals(inst: Instance, truth: str, tests: list[Test]) -> list[tuple[int, frozenset[str], bool]]:
    """Every subset: (total cost incl. fix, separated rivals, probe_only)."""
    rivals = tuple(c for c in inst.live_ids() if c != truth)
    fix = inst.min_fix(truth)
    c_fix = fix.cost if fix else INF
    seps = [separated(t, truth, rivals) for t in tests]
    n = len(tests)
    out = []
    for mask in range(1 << n):
        cost = 0; sep: frozenset[str] = frozenset(); resolves_truth = False; probe_only = True
        for k in range(n):
            if mask >> k & 1:
                cost += tests[k].cost; sep = sep | seps[k]
                if tests[k].kind == "REPAIR":
                    probe_only = False
                    if truth in tests[k].resolves:
                        resolves_truth = True
        total = cost + (0 if resolves_truth else c_fix)
        out.append((total, sep, probe_only))
    return out


def _dfs_min_total(inst: Instance, truth: str, tests: list[Test], need: frozenset[str], *, probe_only: bool) -> int:
    """Independent branch-and-bound: minimal total to separate every rival in ``need``."""
    rivals = tuple(c for c in inst.live_ids() if c != truth)
    fix = inst.min_fix(truth)
    c_fix = fix.cost if fix else INF
    seps = [separated(t, truth, rivals) & need for t in tests]
    order = sorted(range(len(tests)), key=lambda k: tests[k].cost)
    best = [INF]

    def rec(idx: int, cost: int, sep: frozenset[str], resolved: bool) -> None:
        total = cost + (0 if resolved else c_fix)
        if sep >= need:
            best[0] = min(best[0], total); return
        if idx >= len(order) or cost >= best[0]:
            return
        k = order[idx]
        t = tests[k]
        if not (probe_only and t.kind == "REPAIR"):
            rec(idx + 1, cost + t.cost, sep | seps[k], resolved or (t.kind == "REPAIR" and truth in t.resolves))
        rec(idx + 1, cost, sep, resolved)

    rec(0, 0, frozenset(), False)
    return best[0]


def oracle_targets(inst: Instance) -> dict:
    truth = inst.truth
    live = inst.live_ids()
    rivals = tuple(c for c in live if c != truth)
    fix = inst.min_fix(truth)
    if fix is None:
        raise ValueError(f"{inst.instance_id}: truth has no registered resolving intervention")
    tests = tests_for(inst)
    subsets = _subset_totals(inst, truth, tests)
    all_rivals = frozenset(rivals)
    joint = min((tot for tot, sep, _ in subsets if sep >= all_rivals), default=INF)
    joint_probe = min((tot for tot, sep, po in subsets if po and sep >= all_rivals), default=INF)
    per_rival = {r: min((tot for tot, sep, _ in subsets if r in sep), default=INF) for r in rivals}
    budget = inst.budget
    identifiable = joint <= budget
    probe_identifiable = joint_probe <= budget
    U = (truth,) + tuple(r for r in rivals if per_rival[r] > budget)
    need = all_rivals - frozenset(U)
    up_to_U = min((tot for tot, sep, _ in subsets if sep >= need), default=INF)
    identifiable_up_to_U = up_to_U <= budget
    # independent cross-check
    dfs_joint = _dfs_min_total(inst, truth, tests, all_rivals, probe_only=False)
    dfs_joint_probe = _dfs_min_total(inst, truth, tests, all_rivals, probe_only=True)
    dfs_up = _dfs_min_total(inst, truth, tests, need, probe_only=False)
    exhaustive_agrees = (dfs_joint == joint) and (dfs_joint_probe == joint_probe) and (dfs_up == up_to_U)
    if identifiable_up_to_U:
        classes = {inst.cause(u).obstruction_class for u in U}
        loci = {inst.cause(u).locus for u in U}
        fixes = {inst.min_fix(u).intervention_id if inst.min_fix(u) else None for u in U}
        oracle_class = classes.pop() if len(classes) == 1 else "CANNOT_IDENTIFY"
        oracle_locus = loci.pop() if len(loci) == 1 else "CANNOT_IDENTIFY"
        oracle_level = fix.level if len(fixes) == 1 else None
    else:
        oracle_class = "CANNOT_IDENTIFY"; oracle_locus = "CANNOT_IDENTIFY"; oracle_level = None
    return {
        "truth": truth, "truth_class": inst.cause(truth).obstruction_class, "truth_locus": inst.cause(truth).locus,
        "oracle_class": oracle_class, "oracle_locus": oracle_locus, "oracle_level": oracle_level,
        "oracle_fix": fix.intervention_id if oracle_level is not None else None, "oracle_cost": fix.cost if oracle_level is not None else None,
        "truth_fix": fix.intervention_id, "truth_fix_level": fix.level, "truth_fix_cost": fix.cost,
        "identifiable": identifiable, "probe_identifiable": probe_identifiable, "identifiable_up_to_U": identifiable_up_to_U,
        "indistinguishable_set": list(U), "min_identification_total": None if joint >= INF else joint,
        "min_identification_total_probe_only": None if joint_probe >= INF else joint_probe,
        "exhaustive_agrees": bool(exhaustive_agrees), "n_tests": len(tests),
    }


# ---- uniform decidability (truth-agnostic policy tree; exact) ----------------------------------------

def per_cause_targets(inst: Instance) -> dict[str, dict]:
    """Oracle targets for every live cause taken as the truth (same registered instance)."""
    out = {}
    for c in inst.live_ids():
        alt = Instance(**{**{k: getattr(inst, k) for k in inst.__dataclass_fields__}, "truth": c, "features": {}})
        out[c] = oracle_targets(alt)
    return out


def uniformly_decidable(inst: Instance, targets: dict[str, dict] | None = None) -> bool:
    """True iff one policy (no access to the truth) is decision-correct for every live cause.

    Decision-correct for cause c: if c's oracle level is null, the policy declares
    CANNOT_IDENTIFY having applied no level>=2 intervention; else it succeeds with
    c's minimum fix as its last intervention and never applied a higher level.
    """
    targets = targets or per_cause_targets(inst)
    goal = {c: (None if t["oracle_level"] is None else (t["oracle_fix"], t["oracle_level"])) for c, t in targets.items()}
    probes = inst.probes; ivs = inst.interventions
    memo: dict = {}

    def ok(live: frozenset[str], budget: int, used: frozenset[str], applied: frozenset[str], maxlv: int) -> bool:
        key = (live, budget, used, applied, maxlv)
        if key in memo:
            return memo[key]
        res = False
        if all(goal[c] is None for c in live) and maxlv < 2:
            res = True
        if not res:
            for iv in ivs:
                if iv.cost > budget or iv.intervention_id in applied:
                    continue
                resolved = [c for c in live if c in iv.resolves]
                if not resolved:
                    continue
                if any(goal[c] is None or goal[c][0] != iv.intervention_id or maxlv > goal[c][1] for c in resolved):
                    continue
                rest = frozenset(c for c in live if c not in iv.resolves)
                if not rest or ok(rest, budget - iv.cost, used, applied | {iv.intervention_id}, max(maxlv, iv.level)):
                    res = True; break
        if not res:
            for pr in probes:
                if pr.cost > budget or pr.probe_id in used:
                    continue
                groups: dict[str, list[str]] = {}
                for c in live:
                    groups.setdefault(pr.outcome(c), []).append(c)
                if len(groups) <= 1:
                    continue
                if all(ok(frozenset(g), budget - pr.cost, used | {pr.probe_id}, applied, maxlv) for g in groups.values()):
                    res = True; break
        memo[key] = res
        return res

    return ok(frozenset(inst.live_ids()), inst.budget, frozenset(), frozenset(), -1)


# ---- environment ------------------------------------------------------------------------------

class ArmError(RuntimeError):
    pass


@dataclass
class ArmView:
    inst: PublicInstance
    steps: list[Step]
    budget_left: int

    def affordable_probes(self) -> list[Probe]:
        return [p for p in self.inst.probes if p.cost <= self.budget_left]

    def affordable_interventions(self) -> list[Intervention]:
        return [i for i in self.inst.interventions if i.cost <= self.budget_left]

    def probes_run(self) -> set[str]:
        return {s.action.target for s in self.steps if s.action.kind == "PROBE"}

    def interventions_failed(self) -> set[str]:
        return {s.action.target for s in self.steps if s.action.kind == "INTERVENE" and s.outcome == RECURRENCE}

    def consistent_causes(self) -> tuple[str, ...]:
        """GDE-style candidate set: causes consistent with every observation (typed, uses the registered tables)."""
        live = []
        for c in self.inst.live_ids():
            ok = True
            for s in self.steps:
                if s.action.kind == "PROBE" and self.inst.probe(s.action.target).outcome(c) != s.outcome:
                    ok = False; break
                if s.action.kind == "INTERVENE" and self.inst.intervention(s.action.target).outcome(c) != s.outcome:
                    ok = False; break
            if ok:
                live.append(c)
        return tuple(live)


@dataclass
class Trajectory:
    steps: list[Step] = field(default_factory=list)
    terminal: str = "UNSTARTED"
    total_cost: int = 0
    success: bool = False

    def decisive(self) -> Action | None:
        """Declaration attached to the successful intervention, else the last INTERVENE/DECLARE action."""
        for s in reversed(self.steps):
            if s.action.kind in ("INTERVENE", "DECLARE_CANNOT_IDENTIFY"):
                return s.action
        return None

    def as_dict(self) -> dict:
        return {"terminal": self.terminal, "total_cost": self.total_cost, "success": self.success,
                "steps": [{"kind": s.action.kind, "target": s.action.target, "declared_class": s.action.declared_class, "declared_locus": s.action.declared_locus,
                           "confidence": s.action.confidence, "outcome": s.outcome, "cost": s.cost} for s in self.steps]}


class Environment:
    def __init__(self, inst: Instance, *, max_steps: int = MAX_STEPS) -> None:
        self.inst = inst
        self.public = public_of(inst)
        self.max_steps = max_steps

    def run(self, policy) -> Trajectory:
        traj = Trajectory()
        left = self.inst.budget
        while True:
            if len(traj.steps) >= self.max_steps:
                traj.terminal = "MAX_STEPS"; break
            view = ArmView(self.public, list(traj.steps), left)
            action: Action = policy.act(view)
            if action.kind == "PROBE":
                p = self.inst.probe(action.target)
                if p.cost > left:
                    raise ArmError(f"{policy.name}: unaffordable probe {p.probe_id}")
                left -= p.cost; traj.total_cost += p.cost
                traj.steps.append(Step(action, p.outcome(self.inst.truth), p.cost))
            elif action.kind == "INTERVENE":
                i = self.inst.intervention(action.target)
                if i.cost > left:
                    raise ArmError(f"{policy.name}: unaffordable intervention {i.intervention_id}")
                left -= i.cost; traj.total_cost += i.cost
                out = i.outcome(self.inst.truth)
                traj.steps.append(Step(action, out, i.cost))
                if out == SUCCESS:
                    traj.terminal = "SUCCESS"; traj.success = True; break
            elif action.kind == "DECLARE_CANNOT_IDENTIFY":
                traj.steps.append(Step(action, None, 0)); traj.terminal = "CANNOT_IDENTIFY_DECLARED"; break
            elif action.kind == "STOP":
                traj.steps.append(Step(action, None, 0)); traj.terminal = "STOPPED"; break
            else:
                raise ArmError(f"{policy.name}: unknown action {action.kind}")
        return traj
