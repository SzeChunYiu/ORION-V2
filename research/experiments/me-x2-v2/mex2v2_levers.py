"""ME-X2 V2 revival levers (frozen with design V2).

The V1 design (§4.1) registered two orderings that the ORION reference semantics
do **not** fix, as ``M``'s rendering rather than as discoveries:

  (i)  among admissible discriminators ``M`` takes the **cheapest** — the
       semantics say which actions are admissible, never which to try first, so
       ``M`` has no lookahead;
  (ii) the reachability rule is **fail-closed over every live hypothesis**, so
       where the budget forces foreclosing one live hypothesis to establish
       another, ``M`` abstains instead of choosing.

This module renders the same ORION semantics with the other two choices.  No
ORION engine, no ``orion_v2`` call and no oracle is touched: ``M2`` inherits
``mex2_arms.MLocusMinimumEscalation`` and overrides exactly two methods —
``_reserve_ok`` (lever L2) and ``_discriminators`` (lever L1).  The locus
receipt (``assess_discrepancy_locus``), the witnessed-obstruction route
(``route_frontier_action``) and the Jump / ``minimum_level`` policy are
inherited unchanged, so what varies between ``M`` and ``M2`` is only the
rendering of (i) and (ii).

**L1 — one-step lookahead on discriminator choice.**  For each admissible
discriminator the registered outcome tables give its one-step successors.  Each
successor branch is scored with the quantities M already reasons about — the
prospective adequacy of the diagnostic evaluator (does any live hypothesis stay
establishable?), which hypotheses are foreclosed, and how much ambiguity is
left.  Candidates are ordered lexicographically by

    (expected_abstention, best_foreclosed, foreclosed, ambiguity, cost, kind, id)

whose tail ``(cost, kind, id)`` is V1's total order, so M2 reduces to M whenever
the diagnostic terms are indifferent.  There is no cost model beyond the
registered costs and no free parameter: L1 is not a planner and does not
minimise expected total cost — it ranks admissible discriminators by prospective
diagnostic adequacy, then by discrimination, then by V1's own tie-break.

**L2 — best-live-hypothesis reachability.**  V1 admits a discriminating action
only if *every* hypothesis establishable now stays establishable under every
registered outcome.  L2 requires instead that *some* establishable hypothesis
survives in every branch, and L1's ``best_foreclosed`` term prefers the action
that preserves the **minimum-responsible** one (lowest minimal-fix level, then
cost, then id) — the same minimum-escalation preference the arm already applies
to interventions.  Where the budget forces foreclosing an alternative, M2
chooses rather than abstains.

Both levers are mechanic changes registered before any protected outcome; no
gate, threshold, generator rule or oracle rule differs from V1.
"""
from __future__ import annotations

import sys
from pathlib import Path

V1_DIR = Path(__file__).resolve().parent.parent / "me-x2"
if str(V1_DIR) not in sys.path:
    sys.path.insert(0, str(V1_DIR))

from mex2_arms import (  # noqa: E402
    MLocusMinimumEscalation,
    MLocusLabelsShuffled,
    MMinusLocusDiagnosis,
)
from mex2_model import Intervention, Probe  # noqa: E402  (typing only)
from mex2_oracle import ArmView  # noqa: E402

UNRANKED = (10 ** 6, 10 ** 6)


class M2LookaheadBestHypothesis(MLocusMinimumEscalation):
    """M with both revival levers.  Primary V2 arm."""

    name = "M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS"
    lookahead = True                     # L1
    best_hypothesis_reachability = True  # L2

    def __init__(self, seed: str) -> None:
        super().__init__(seed)
        self.lever_receipts: list[dict] = []
        self._est_cache: dict = {}
        self._reach_cache: dict = {}

    # ---- cached registered-information queries -------------------------------------------------

    def _establishable(self, view: ArmView, live: tuple[str, ...], c: str) -> bool:
        key = (c, live, view.budget_left, tuple(sorted(view.probes_run())), tuple(sorted(self.applied(view))))
        if key not in self._est_cache:
            self._est_cache[key] = super()._establishable(view, live, c)
        return self._est_cache[key]

    def _reachable_after(self, view: ArmView, group: tuple[str, ...], c: str, left: int, used: set[str], applied: set[str]) -> bool:
        key = (c, tuple(group), left, tuple(sorted(used)), tuple(sorted(applied)))
        if key not in self._reach_cache:
            self._reach_cache[key] = super()._reachable_after(view, group, c, left, used, applied)
        return self._reach_cache[key]

    # ---- one-step successors under the registered outcome tables -------------------------------

    def _branches(self, view: ArmView, live: tuple[str, ...], target: str, kind: str) -> tuple[list[tuple[float, tuple[str, ...], bool]], set[str], set[str]]:
        """Registered one-step successors of an action: ``[(weight, group, terminal)]`` plus the
        successor's used-probe and applied-intervention sets.  Weights are the uniform prior over
        live causes shared by every arm.  A repair-as-test that resolves the truth ends the episode
        in SUCCESS: that branch is terminal and carries no residual diagnosis."""
        used = set(view.probes_run())
        applied = set(self.applied(view))
        n = len(live)
        if kind == "PROBE":
            p = view.inst.probe(target)
            f = p.designed_outcome if self.designed_tables else p.outcome
            groups: dict[str, list[str]] = {}
            for c in live:
                groups.setdefault(f(c), []).append(c)
            return [(len(g) / n, tuple(g), False) for g in groups.values()], used | {target}, applied
        iv = view.inst.intervention(target)
        resolved = tuple(c for c in live if c in iv.resolves)
        rest = tuple(c for c in live if c not in iv.resolves)
        out: list[tuple[float, tuple[str, ...], bool]] = []
        if resolved:
            out.append((len(resolved) / n, resolved, True))
        if rest:
            out.append((len(rest) / n, rest, False))
        return out, used, applied | {target}

    def _responsible_rank(self, view: ArmView, c: str) -> tuple[int, int]:
        """Minimum-responsible order over live hypotheses: the hypothesis whose warranted
        intervention is the least escalating comes first (registered, truth-agnostic)."""
        fix = self.fix_of(view, c)
        return (fix.level, fix.cost) if fix is not None else UNRANKED

    # ---- L2: fail-closed on the best live hypothesis, not on every one --------------------------

    def _best_live(self, view: ArmView, live: tuple[str, ...]) -> str | None:
        """The best live hypothesis: the establishable account that requires the least escalation
        (minimum-responsible order).  Registered, truth-agnostic, and the same preference the arm
        already applies to interventions."""
        establishable = [c for c in live if self._establishable(view, live, c)]
        if not establishable:
            return None
        return min(establishable, key=lambda c: (self._responsible_rank(view, c), c))

    def _reserve_ok(self, view: ArmView, live: tuple[str, ...], cost: int, target: str, kind: str) -> bool:
        if not self.best_hypothesis_reachability:
            return super()._reserve_ok(view, live, cost, target, kind)
        left = view.budget_left - cost
        if left < 0:
            return False
        best = self._best_live(view, live)
        if best is None:
            return True
        branches, used, applied = self._branches(view, live, target, kind)
        for _w, grp, terminal in branches:
            if best not in grp:      # the outcome refutes `best`: a defeat, not a resource foreclosure
                continue
            if terminal:             # the repair-as-test resolves `best`: the test is its own fix
                return True
            return self._reachable_after(view, grp, best, left, used, applied)
        return True

    # ---- L1: one-step lookahead terms -----------------------------------------------------------

    def _lookahead_terms(self, view: ArmView, live: tuple[str, ...], cost: int, target: str, kind: str) -> tuple[float, float, float, float]:
        left = view.budget_left - cost
        branches, used, applied = self._branches(view, live, target, kind)
        abstention = 0.0
        best_foreclosed = 0.0
        foreclosed = 0.0
        ambiguity = 0.0
        for w, grp, terminal in branches:
            if terminal:                       # SUCCESS: the repair is the fix; no residual diagnosis
                continue
            survivors = [c for c in grp if self._reachable_after(view, grp, c, left, used, applied)]
            if not survivors:
                abstention += w                # the diagnostic evaluator is inadequate in that branch
            establishable_now = [c for c in grp if self._establishable(view, live, c)]
            lost = [c for c in establishable_now if c not in survivors]
            foreclosed += w * len(lost)
            if establishable_now:
                best = min(establishable_now, key=lambda c: (self._responsible_rank(view, c), c))
                if best in lost:
                    best_foreclosed += w
            ambiguity += w * (len(grp) - 1)
        return abstention, best_foreclosed, foreclosed, ambiguity

    def _key(self, view: ArmView, live: tuple[str, ...], cost: int, target: str, kind: str, kind_rank: int) -> tuple:
        a, bf, f, amb = self._lookahead_terms(view, live, cost, target, kind)
        return (a, bf, f, amb, cost, kind_rank, target)

    def _discriminators(self, view: ArmView, live: tuple[str, ...]) -> list[tuple[int, int, str, str]]:
        if not self.lookahead or not self.prospective_discriminator:
            return super()._discriminators(view, live)
        cands: list[tuple[tuple, int, int, str, str]] = []
        v1_admissible = 0
        if self.probing:
            for p in view.affordable_probes():
                if p.probe_id in view.probes_run() or not self.splits(view, p, live):
                    continue
                if not self._reserve_ok(view, live, p.cost, p.probe_id, "PROBE"):
                    continue
                v1_admissible += int(MLocusMinimumEscalation._reserve_ok(self, view, live, p.cost, p.probe_id, "PROBE"))
                cands.append((self._key(view, live, p.cost, p.probe_id, "PROBE", 0), p.cost, 0, p.probe_id, "PROBE"))
        if self.lower_level_disposition:
            for i in view.affordable_interventions():
                if not i.is_cheap or i.intervention_id in self.applied(view):
                    continue
                hit = [c for c in live if c in i.resolves]
                if not hit or len(hit) >= len(live):
                    continue
                if not self._reserve_ok(view, live, i.cost, i.intervention_id, "INTERVENE"):
                    continue
                v1_admissible += int(MLocusMinimumEscalation._reserve_ok(self, view, live, i.cost, i.intervention_id, "INTERVENE"))
                cands.append((self._key(view, live, i.cost, i.intervention_id, "INTERVENE", 1), i.cost, 1, i.intervention_id, "INTERVENE"))
        cands.sort(key=lambda t: t[0])
        if cands:
            key, cost, kind_rank, target, kind = cands[0]
            self.lever_receipts.append({
                "step": len(view.steps), "live": list(live), "action": target, "kind": kind,
                "expected_abstention": key[0], "best_foreclosed": key[1], "foreclosed": key[2], "ambiguity": key[3], "cost": cost,
                "n_admissible": len(cands), "n_admissible_under_v1_rule": v1_admissible,
                "l2_only_admissible": not MLocusMinimumEscalation._reserve_ok(self, view, live, cost, target, kind),
                "l1_changed_choice": [t[3] for t in sorted(cands, key=lambda t: (t[1], t[2], t[3]))][0] != target,
            })
        return [(c, k, t, kd) for _key, c, k, t, kd in cands]


class M2LookaheadOnly(M2LookaheadBestHypothesis):
    """L1 alone: one-step lookahead, V1's fail-closed-over-every-hypothesis reachability."""

    name = "M2_L1_LOOKAHEAD_ONLY"
    best_hypothesis_reachability = False


class M2BestHypothesisOnly(M2LookaheadBestHypothesis):
    """L2 alone: best-live-hypothesis reachability, V1's cheapest-first discriminator choice."""

    name = "M2_L2_BEST_HYPOTHESIS_ONLY"
    lookahead = False


# ---- M2 ablations (protocol V2 required ablations, applied to the arm under test) ----------------

class M2MinusLocusDiagnosis(M2LookaheadBestHypothesis):
    name = "M2_MINUS_LOCUS_DIAGNOSIS"
    probing = False
    live = MMinusLocusDiagnosis.live


class M2LocusLabelsShuffled(M2LookaheadBestHypothesis):
    name = "M2_LOCUS_LABELS_SHUFFLED"
    _perm = MLocusLabelsShuffled._perm
    cls_of = MLocusLabelsShuffled.cls_of
    locus_of = MLocusLabelsShuffled.locus_of
    fix_of = MLocusLabelsShuffled.fix_of


class M2MinusDiagnosticEvaluatorGate(M2LookaheadBestHypothesis):
    name = "M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE"; gate = False


class M2MinusLowerLevelDisposition(M2LookaheadBestHypothesis):
    name = "M2_MINUS_LOWER_LEVEL_DISPOSITION"; lower_level_disposition = False


class M2MinusProspectiveDiscriminator(M2LookaheadBestHypothesis):
    name = "M2_MINUS_PROSPECTIVE_DISCRIMINATOR"; prospective_discriminator = False


class M2AlwaysEscalateWhenStuck(M2LookaheadBestHypothesis):
    name = "M2_ALWAYS_ESCALATE_WHEN_STUCK"; always_escalate = True


class M2NeverEscalate(M2LookaheadBestHypothesis):
    name = "M2_NEVER_ESCALATE"; never_escalate = True; max_level = 1


M2_ARM = M2LookaheadBestHypothesis.name
M2_L1_ARM = M2LookaheadOnly.name
M2_L2_ARM = M2BestHypothesisOnly.name
M2_ABLATIONS = (
    M2MinusLocusDiagnosis.name, M2LocusLabelsShuffled.name, M2MinusDiagnosticEvaluatorGate.name,
    M2MinusLowerLevelDisposition.name, M2MinusProspectiveDiscriminator.name,
    M2AlwaysEscalateWhenStuck.name, M2NeverEscalate.name,
)
M2_LOCUS_ABLATIONS = (M2MinusLocusDiagnosis.name, M2LocusLabelsShuffled.name)
