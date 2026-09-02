"""ME-X2 faithful parent engines (frozen with design V1).

Each parent passes its own native known-answer tests (``fidelity_selftests``)
before being used by any arm.  Parents receive only registered information.

  ConsistencyDiagnosis   GDE-style consistency-based candidate generation (de Kleer &
                         Williams 1987) over registered component/observation tables.
  MyopicVoI              one-step value of information / rational metareasoning
                         (Russell & Wefald 1991; Howard 1966): expected reduction of
                         the expected cost of the best immediate act minus probe cost.
  ExactPlanner           finite-horizon expected-cost dynamic programme over
                         (candidate set, remaining budget): Bayes-optimal sequential
                         test-and-repair under a uniform prior (Kalagnanam & Henrion
                         1990 style test sequencing, exact by enumeration).
  Abstention             calibrated selective prediction with threshold tau on the
                         class posterior (Chow 1970; Geifman & El-Yaniv 2017).
  TaxonomyClassifier     ARFT-equivalent process-failure pattern -> standard-fix table
                         (arXiv:2608.14905 stands as parent benchmark; not licensed/used).
  MDARule                model-discovery-agent style criticism -> model-family expansion
                         (arXiv:2608.09696 style: posterior-predictive rejection triggers
                         expansion of the hypothesis family).
"""
from __future__ import annotations

from functools import lru_cache

from mex2_catalogue import TAXONOMY_PATTERNS, TEMPLATES
from mex2_model import CLASSES, RECURRENCE, SUCCESS, Intervention, Probe

TAU = 0.9
FAILURE_PENALTY_MULTIPLIER = 10  # registered: an unresolved episode costs 10x the budget to every expected-cost parent


# ---- consistency-based diagnosis ---------------------------------------------------------------

class ConsistencyDiagnosis:
    """Candidates = hypotheses consistent with every observation under the registered tables."""

    @staticmethod
    def candidates(hypotheses: tuple[str, ...], observations: list[tuple[object, str]], *, designed: bool = False) -> tuple[str, ...]:
        out = []
        for h in hypotheses:
            ok = True
            for comp, obs in observations:
                pred = comp.designed_outcome(h) if (designed and isinstance(comp, Probe)) else comp.outcome(h)
                if pred != obs:
                    ok = False; break
            if ok:
                out.append(h)
        return tuple(out)


def min_separating_total(target: str, rivals: tuple[str, ...], probes: list[Probe], repairs: list[Intervention], fix_cost: int, budget: int, *, designed: bool = False) -> int | None:
    """Minimal total (tests + fix) to establish ``target`` against ``rivals`` from registered tables
    (branch-and-bound over the available tests; a repair resolving the target counts as its fix).
    Returns None when no affordable set exists.  Used by arms; independent of the oracle module."""
    tests: list[tuple[int, frozenset[str], bool]] = []
    for p in probes:
        f = p.designed_outcome if designed else p.outcome
        t = f(target)
        tests.append((p.cost, frozenset(r for r in rivals if f(r) != t), False))
    for i in repairs:
        t = i.outcome(target)
        tests.append((i.cost, frozenset(r for r in rivals if i.outcome(r) != t), target in i.resolves))
    tests.sort(key=lambda x: x[0])
    need = frozenset(rivals)
    best = [None]

    def rec(idx: int, cost: int, sep: frozenset[str], resolved: bool) -> None:
        total = cost + (0 if resolved else fix_cost)
        if total > budget or (best[0] is not None and total >= best[0]):
            return
        if sep >= need:
            best[0] = total; return
        if idx >= len(tests):
            return
        c, sp, rs = tests[idx]
        rec(idx + 1, cost + c, sep | sp, resolved or rs)
        rec(idx + 1, cost, sep, resolved)

    rec(0, 0, frozenset(), False)
    return best[0]


# ---- myopic VoI ---------------------------------------------------------------------------------

def uniform_mass(live: tuple[str, ...], subset) -> float:
    return len([c for c in live if c in subset]) / len(live) if live else 0.0


class MyopicVoI:
    def __init__(self, failure_penalty: float) -> None:
        self.F = failure_penalty

    def expected_cost(self, iv: Intervention, live: tuple[str, ...]) -> float:
        p = uniform_mass(live, iv.resolves)
        return iv.cost + (1.0 - p) * self.F

    def best_act(self, live: tuple[str, ...], interventions: list[Intervention]) -> tuple[Intervention | None, float]:
        best, bv = None, self.F  # declare/abstain costs the failure penalty
        for iv in sorted(interventions, key=lambda i: (i.level, i.cost, i.intervention_id)):
            v = self.expected_cost(iv, live)
            if v < bv:
                best, bv = iv, v
        return best, bv

    def value(self, probe: Probe, live: tuple[str, ...], interventions: list[Intervention], *, designed: bool = False) -> float:
        _, now = self.best_act(live, interventions)
        groups: dict[str, list[str]] = {}
        for c in live:
            groups.setdefault(probe.designed_outcome(c) if designed else probe.outcome(c), []).append(c)
        after = sum(len(g) / len(live) * self.best_act(tuple(g), [i for i in interventions if i.cost <= 10 ** 9])[1] for g in groups.values())
        return now - after - probe.cost


# ---- exact planner -------------------------------------------------------------------------------

class ExactPlanner:
    """Minimal expected total cost to success; declare costs the failure penalty F.

    tau gate: an intervention of level >= 2 is admissible only if the posterior mass of its
    resolves set is >= tau (federation never commits a regime change on weak evidence).
    """

    def __init__(self, probes: tuple[Probe, ...], interventions: tuple[Intervention, ...], failure_penalty: float, *, tau: float | None, designed: bool = False) -> None:
        self.probes = probes; self.interventions = interventions; self.F = failure_penalty; self.tau = tau; self.designed = designed
        self._memo: dict = {}

    def _out(self, p: Probe, c: str) -> str:
        return p.designed_outcome(c) if self.designed else p.outcome(c)

    def admissible(self, iv: Intervention, live: tuple[str, ...]) -> bool:
        if self.tau is None or iv.level <= 1:
            return True
        return uniform_mass(live, iv.resolves) >= self.tau

    def value(self, live: tuple[str, ...], used: frozenset[str], failed: frozenset[str], budget: int) -> tuple[float, tuple | None]:
        key = (live, used, failed, budget)
        if key in self._memo:
            return self._memo[key]
        best_v, best_a = float(self.F), None  # declare
        n = len(live)
        for iv in self.interventions:
            if iv.cost > budget or iv.intervention_id in failed or not self.admissible(iv, live):
                continue
            p = uniform_mass(live, iv.resolves)
            rest = tuple(c for c in live if c not in iv.resolves)
            v = iv.cost
            if rest:
                v += (1 - p) * self.value(rest, used, failed | {iv.intervention_id}, budget - iv.cost)[0]
            if v < best_v - 1e-12 or (abs(v - best_v) <= 1e-12 and best_a is not None and best_a[0] == "INTERVENE" and iv.level < self.interventions_by_id(best_a[1]).level):
                best_v, best_a = v, ("INTERVENE", iv.intervention_id)
        for pr in self.probes:
            if pr.cost > budget or pr.probe_id in used:
                continue
            groups: dict[str, list[str]] = {}
            for c in live:
                groups.setdefault(self._out(pr, c), []).append(c)
            if len(groups) <= 1:
                continue
            v = pr.cost + sum(len(g) / n * self.value(tuple(g), used | {pr.probe_id}, failed, budget - pr.cost)[0] for g in groups.values())
            if v < best_v - 1e-12:
                best_v, best_a = v, ("PROBE", pr.probe_id)
        self._memo[key] = (best_v, best_a)
        return best_v, best_a

    def interventions_by_id(self, iid: str) -> Intervention:
        return next(i for i in self.interventions if i.intervention_id == iid)


# ---- abstention ----------------------------------------------------------------------------------

class Abstention:
    def __init__(self, tau: float = TAU) -> None:
        self.tau = tau

    @staticmethod
    def class_posterior(live: tuple[str, ...], cls_of) -> dict[str, float]:
        post: dict[str, float] = {}
        for c in live:
            post[cls_of(c)] = post.get(cls_of(c), 0.0) + 1.0 / len(live)
        return post

    def decide(self, live: tuple[str, ...], cls_of) -> tuple[str | None, float]:
        post = self.class_posterior(live, cls_of)
        cls = max(post, key=lambda k: (post[k], -(CLASSES.index(k) if k in CLASSES else 10 ** 6)))
        return (cls if post[cls] >= self.tau else None), post[cls]


# ---- taxonomy ---------------------------------------------------------------------------------------

class TaxonomyClassifier:
    @staticmethod
    def standard_fix(pattern: str) -> str | None:
        return TAXONOMY_PATTERNS[pattern]["standard_fix_kind"]

    @staticmethod
    def escalation_order(interventions: tuple[Intervention, ...], pattern: str) -> list[Intervention]:
        std = TaxonomyClassifier.standard_fix(pattern)
        first = [i for i in interventions if i.kind == std]
        rest = sorted([i for i in interventions if i.kind != std], key=lambda i: (i.level, i.cost, i.intervention_id))
        return first + rest


# ---- MDA rule ----------------------------------------------------------------------------------------

class MDARule:
    REJECT = {"REJECT", "ALL_REJECTED"}

    @staticmethod
    def criticism_probes(probes: tuple[Probe, ...]) -> list[Probe]:
        return [p for p in probes if p.evaluator_mediated]

    @staticmethod
    def should_expand(live: tuple[str, ...], locus_of, criticism_rejected: bool) -> bool:
        return criticism_rejected and any(locus_of(c) == "EPISTEMIC_MODEL" for c in live)


# ---- native fidelity tests -------------------------------------------------------------------------

def fidelity_selftests() -> list[dict]:
    res: list[dict] = []

    def add(parent, name, passed):
        res.append({"parent": parent, "test": name, "passed": bool(passed)})

    # GDE: two components, three hypotheses; observation eliminates exactly the predicted set
    pA = Probe("a", 1, False, "OK", {"h1": "BAD"})
    pB = Probe("b", 1, True, "OK", {"h2": "BAD"}, {"h2": "BAD", "h3": "BAD"})
    add("GDE", "single observation eliminates exactly the inconsistent hypothesis", ConsistencyDiagnosis.candidates(("h1", "h2", "h3"), [(pA, "OK")]) == ("h2", "h3"))
    add("GDE", "two observations intersect candidate sets", ConsistencyDiagnosis.candidates(("h1", "h2", "h3"), [(pA, "OK"), (pB, "BAD")]) == ("h2",))
    add("GDE", "designed table trusts the evaluator (laundered row not applied)", ConsistencyDiagnosis.candidates(("h1", "h2", "h3"), [(pB, "OK")], designed=True) == ("h1",) and ConsistencyDiagnosis.candidates(("h1", "h2", "h3"), [(pB, "OK")]) == ("h1", "h3"))
    add("GDE", "repair recurrence eliminates the resolved hypotheses", ConsistencyDiagnosis.candidates(("h1", "h2"), [(Intervention("fix", "fix", 1, 3, ("h1",)), RECURRENCE)]) == ("h2",))
    # VoI: hand-computed
    voi = MyopicVoI(failure_penalty=20.0)
    live = ("h1", "h2")
    i1 = Intervention("f1", "f1", 1, 3, ("h1",)); i2 = Intervention("f2", "f2", 2, 8, ("h2",))
    # best act now: f1: 3 + 0.5*20 = 13; f2: 8 + 10 = 18 -> 13
    add("VOI", "expected cost of best immediate act", abs(voi.best_act(live, [i1, i2])[1] - 13.0) < 1e-9)
    perfect = Probe("p", 2, False, "X", {"h2": "Y"})
    # after perfect probe: 0.5*3 + 0.5*8 = 5.5 ; VoI = 13 - 5.5 - 2 = 5.5
    add("VOI", "perfect probe value = 13 - 5.5 - 2 = 5.5", abs(voi.value(perfect, live, [i1, i2]) - 5.5) < 1e-9)
    useless = Probe("u", 2, False, "X", {})
    add("VOI", "non-splitting probe value = -cost", abs(voi.value(useless, live, [i1, i2]) + 2.0) < 1e-9)
    # exact planner: cheap-first beats commit (3 + 0.5*8 = 7 < 8); a 1-cost perfect probe beats both (1 + 0.5*3 + 0.5*8 = 6.5)
    i2b = Intervention("f2", "f2", 2, 8, ("h1", "h2"))
    pl = ExactPlanner((), (i1, i2b), failure_penalty=12.0, tau=None)
    v, a = pl.value(live, frozenset(), frozenset(), 12)
    add("PLANNER", "cheap repair-as-test first: 3 + 0.5*8 = 7 < 8", abs(v - 7.0) < 1e-9 and a == ("INTERVENE", "f1"))
    pl2 = ExactPlanner((Probe("p", 1, False, "X", {"h2": "Y"}),), (i1, i2), failure_penalty=12.0, tau=None)
    v2, a2 = pl2.value(live, frozenset(), frozenset(), 12)
    add("PLANNER", "perfect 1-cost probe first: 1 + 0.5*3 + 0.5*8 = 6.5", abs(v2 - 6.5) < 1e-9 and a2 == ("PROBE", "p"))
    pl3 = ExactPlanner((), (i1, i2b), failure_penalty=12.0, tau=0.9)
    v3, a3 = pl3.value(live, frozenset(), frozenset(), 12)
    add("PLANNER", "tau gate admits a level-2 act only when it resolves the whole candidate set", a3 == ("INTERVENE", "f1") and pl3.admissible(i2b, live) and not pl3.admissible(i2, live))
    pl4 = ExactPlanner((), (i2,), failure_penalty=12.0, tau=0.9)
    add("PLANNER", "no admissible act -> declare at the failure penalty", pl4.value(live, frozenset(), frozenset(), 12) == (12.0, None))
    add("PLANNER", "budget-infeasible act excluded", ExactPlanner((), (i1,), failure_penalty=12.0, tau=None).value(("h1",), frozenset(), frozenset(), 2)[1] is None)
    # abstention
    ab = Abstention(0.9)
    add("TEST_SEQUENCING", "a repair that resolves the target is its own test and fix (3 < probe 1 + fix 8)", min_separating_total("h1", ("h2", "h3"), [pA, pB], [i1], 8, 20) == 3)
    add("TEST_SEQUENCING", "probe route when no repair resolves the target (pA separates both: 1 + 8 = 9)", min_separating_total("h1", ("h2", "h3"), [pA, pB], [], 8, 20) == 9)
    add("TEST_SEQUENCING", "unaffordable -> None", min_separating_total("h1", ("h2", "h3"), [pA, pB], [], 8, 8) is None)
    add("ABSTENTION", "posterior below tau abstains", ab.decide(("h1", "h2"), lambda c: {"h1": "A", "h2": "B"}[c]) == (None, 0.5))
    add("ABSTENTION", "shared class reaches tau", ab.decide(("h1", "h2"), lambda c: "A") == ("A", 1.0))
    # taxonomy: every pattern's standard fix exists in its template and the order is level-ascending after it
    ok = True
    for t, d in TEMPLATES.items():
        std = TAXONOMY_PATTERNS[d["pattern"]]["standard_fix_kind"]
        ok &= any(i[0] == std for i in d["interventions"])
    add("TAXONOMY", "every registered pattern maps to an intervention kind of its template", ok)
    order = TaxonomyClassifier.escalation_order((i1, i2, Intervention("std", "expand_model_family", 2, 6, ("h2",))), "PREDICTIVE_RESIDUAL_AFTER_T0")
    add("TAXONOMY", "standard fix first, then ascending level", [i.intervention_id for i in order] == ["std", "f1", "f2"])
    add("TAXONOMY", "NO_MAPPING pattern registered as hostile counterexample", TAXONOMY_PATTERNS["UNMAPPED_AGENT_LOOP_PATTERN"]["orion_mapping"] == "NO_MAPPING")
    # MDA
    add("MDA", "expansion fires only after criticism rejection with a model-locus candidate", MDARule.should_expand(("m", "b"), lambda c: {"m": "EPISTEMIC_MODEL", "b": "PROCESS_TOOL_WORKFLOW"}[c], True) and not MDARule.should_expand(("m", "b"), lambda c: "EPISTEMIC_MODEL", False) and not MDARule.should_expand(("b",), lambda c: "PROCESS_TOOL_WORKFLOW", True))
    return res
