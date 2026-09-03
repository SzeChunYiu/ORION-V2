"""ME-F1 parent methods: named published techniques, implemented faithfully.

These are the components of ``B5_STRONGEST_FAITHFUL_PARENT_FEDERATION``.  The brief for
this study is explicit that B5 must be information- and resource-matched, allowed
ordinary glue, and **not artificially isolated** -- ME-X2's B5 beat M, and that is the
bar.  Each component below names the work it implements and is exercised by a native
known-answer test in ``fidelity_selftests`` (house style: parent fidelity is asserted
by the parents' own tests, before any arm contrast exists).

Components
----------
``luby_sequence``          Luby, Sinclair & Zuckerman (1993), "Optimal speedup of Las
                          Vegas algorithms": the universal restart schedule
                          1,1,2,1,1,2,4,... which is within a log factor of optimal
                          without knowing the runtime distribution.
``portfolio_select``       Rice (1976) algorithm selection; Xu, Hutter, Hoos &
                          Leyton-Brown (2008) SATzilla: choose a solver per instance
                          from cheap syntactic features.  The feature here is the
                          clause/variable ratio, which is the single strongest
                          predictor of which solver wins on random 3-SAT.
``heavy_tail_restart``     Gomes, Selman & Kautz (1998): randomized rapid restarts
                          exploit heavy-tailed runtime distributions in backtracking
                          search.
``bisect_threshold``       Binary search over a monotone predicate.  This is the
                          structurally correct parent for a nested ladder and the
                          component most likely to make B5 hard to beat: it localises
                          the SAT/UNSAT boundary in O(log L) probes instead of L.
``version_space_claims``   Mitchell (1982) version spaces: maintain the most specific
                          and most general hypotheses consistent with the evidence and
                          assert only what every consistent hypothesis entails.
``calibrated_abstention``  Standard solver semantics (SAT / UNSAT / UNKNOWN): a solver
                          that hits its limit reports UNKNOWN and never guesses.

Note on what these parents already do well.  ``version_space_claims`` combined with
``calibrated_abstention`` is, deliberately, a *correct* warranted-claim discipline for
this world.  The parents are not strawmen on the endpoint this study cares most about;
if ORION's control layer shows no residual against them, that is a real finding and the
design says so in advance (design S1.2).
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---- Luby, Sinclair & Zuckerman (1993) ---------------------------------------------------

def luby_sequence(n: int) -> list[int]:
    """First ``n`` terms of the universal Las Vegas restart schedule."""
    # Doubling construction: S_1 = [1]; S_{k+1} = S_k ++ S_k ++ [2^k].
    # This yields 1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,... as published.
    seq: list[int] = [1]
    power = 1
    while len(seq) < n:
        seq = seq + seq + [power * 2]
        power *= 2
    return seq[:n]


def luby_budgets(total: int, probes: int, unit: int | None = None) -> list[int]:
    """Split ``total`` budget over ``probes`` restarts on the Luby schedule."""
    seq = luby_sequence(probes)
    s = sum(seq)
    unit = unit or max(1, total // max(1, s))
    return [max(1, t * unit) for t in seq]


# ---- Rice (1976) / SATzilla (Xu et al. 2008) ---------------------------------------------

@dataclass(frozen=True, slots=True)
class RungFeatures:
    """Cheap syntactic features, computable without search (SATzilla's design principle)."""

    rung: int
    n_vars: int
    n_clauses: int

    @property
    def ratio(self) -> float:
        return self.n_clauses / max(1, self.n_vars)


#: Random 3-SAT satisfiability threshold.  Below it instances are overwhelmingly
#: satisfiable and local search dominates; above it they are unsatisfiable and only a
#: complete method can produce a certificate.  This is the portfolio's decision boundary.
SAT_THRESHOLD_RATIO = 4.267


def portfolio_select(feat: RungFeatures) -> str:
    """Per-rung solver selection from features alone.  Returns a tool name."""
    if feat.ratio <= SAT_THRESHOLD_RATIO - 0.15:
        return "local_search"      # almost surely SAT; incomplete search is far faster
    if feat.ratio >= SAT_THRESHOLD_RATIO + 0.15:
        return "exact_solve"       # almost surely UNSAT; only a complete method certifies
    return "local_search"          # in the critical band, try the cheap witness first


def portfolio_schedule(feats: list[RungFeatures]) -> list[tuple[int, str]]:
    """Order rungs by expected information per unit cost (cheap ends first)."""
    easy_sat = [f for f in feats if f.ratio <= SAT_THRESHOLD_RATIO - 0.15]
    easy_unsat = [f for f in feats if f.ratio >= SAT_THRESHOLD_RATIO + 0.15]
    critical = [f for f in feats if f not in easy_sat and f not in easy_unsat]
    order: list[tuple[int, str]] = []
    for f in sorted(easy_sat, key=lambda x: -x.ratio):      # highest SAT rung first: closes most by closure
        order.append((f.rung, "local_search"))
    for f in sorted(easy_unsat, key=lambda x: x.ratio):     # lowest UNSAT rung first: same reason
        order.append((f.rung, "exact_solve"))
    for f in critical:
        order.append((f.rung, portfolio_select(f)))
    return order


# ---- Gomes, Selman & Kautz (1998) --------------------------------------------------------

def heavy_tail_restart(total: int, cutoff_fraction: float = 0.1) -> list[int]:
    """Many short runs beat one long run when the runtime distribution is heavy-tailed."""
    cut = max(1, int(total * cutoff_fraction))
    out = []
    left = total
    while left > 0:
        take = min(cut, left)
        out.append(take)
        left -= take
    return out


# ---- monotone threshold localisation -----------------------------------------------------

@dataclass
class Bisector:
    """Binary search for the SAT/UNSAT boundary of a monotone ladder.

    ``lo`` is the highest rung known SAT (or -1), ``hi`` the lowest known UNSAT (or
    ``n_rungs``).  ``next_probe`` returns the midpoint of the open interval, which is the
    optimal probe when probes are equally informative and equally costly -- the standard
    reason binary search is the right parent here.
    """

    n_rungs: int
    lo: int = -1
    hi: int | None = None

    def __post_init__(self) -> None:
        if self.hi is None:
            self.hi = self.n_rungs

    def next_probe(self) -> int | None:
        assert self.hi is not None
        if self.hi - self.lo <= 1:
            return None  # boundary localised
        return (self.lo + self.hi) // 2

    def record_sat(self, rung: int) -> None:
        self.lo = max(self.lo, rung)

    def record_unsat(self, rung: int) -> None:
        assert self.hi is not None
        self.hi = min(self.hi, rung)

    def settled(self) -> set[int]:
        assert self.hi is not None
        return set(range(0, self.lo + 1)) | set(range(self.hi, self.n_rungs))


# ---- Mitchell (1982) version spaces ------------------------------------------------------

@dataclass
class VersionSpace:
    """Version space over the single free parameter of a monotone ladder: the threshold.

    A hypothesis is "the boundary is at ``t``", meaning rungs ``< t`` are SAT and rungs
    ``>= t`` are UNSAT.  Evidence removes hypotheses; the arm may assert a verdict for a
    rung only when **every** surviving hypothesis agrees on it.  That is precisely
    Mitchell's "assert only what the whole version space entails", and it yields a
    correct warranted-claim discipline for this world without any ORION machinery.
    """

    n_rungs: int
    candidates: set[int] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.candidates:
            self.candidates = set(range(0, self.n_rungs + 1))

    def observe_sat(self, rung: int) -> None:
        # rung is SAT => boundary is strictly above it
        self.candidates = {t for t in self.candidates if t > rung}

    def observe_unsat(self, rung: int) -> None:
        # rung is UNSAT => boundary is at or below it
        self.candidates = {t for t in self.candidates if t <= rung}

    def entailed(self, rung: int) -> str | None:
        """Verdict entailed by every surviving hypothesis, else None."""
        if not self.candidates:
            return None
        sat = all(rung < t for t in self.candidates)
        unsat = all(rung >= t for t in self.candidates)
        if sat:
            return "SATISFIABLE"
        if unsat:
            return "UNSATISFIABLE"
        return None


def calibrated_abstention(entailed: str | None) -> str:
    """Standard solver semantics: never guess past what is entailed."""
    return entailed if entailed is not None else "UNRESOLVED"


# ---- native known-answer fidelity tests --------------------------------------------------

def fidelity_selftests() -> tuple[int, int, list[str]]:
    """Each parent is checked against a hand-computed answer.  Returns (passed, total, failures)."""
    failures: list[str] = []
    checks: list[tuple[str, bool]] = []

    # Luby: the published prefix is 1,1,2,1,1,2,4,1,1,2,1,1,2,4,8
    checks.append(("luby_prefix",
                   luby_sequence(15) == [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8]))
    checks.append(("luby_monotone_blocks", luby_sequence(1) == [1]))
    b = luby_budgets(1000, 7)
    checks.append(("luby_budgets_positive", all(x >= 1 for x in b) and len(b) == 7))

    # Portfolio: below threshold -> local search, above -> exact
    checks.append(("portfolio_low", portfolio_select(RungFeatures(0, 50, 130)) == "local_search"))
    checks.append(("portfolio_high", portfolio_select(RungFeatures(0, 50, 340)) == "exact_solve"))
    checks.append(("portfolio_critical",
                   portfolio_select(RungFeatures(0, 50, int(50 * 4.267))) == "local_search"))
    sched = portfolio_schedule([RungFeatures(i, 50, c) for i, c in enumerate([130, 213, 340])])
    checks.append(("portfolio_schedule_covers", {r for r, _ in sched} == {0, 1, 2}))

    # Heavy-tail restarts partition the budget exactly
    ht = heavy_tail_restart(1000, 0.1)
    checks.append(("heavy_tail_partition", sum(ht) == 1000 and max(ht) <= 100))

    # Bisection on a 12-rung ladder with true boundary 7 finds it in <= 4 probes
    bs = Bisector(12)
    probes = 0
    while (p := bs.next_probe()) is not None:
        probes += 1
        if p < 7:
            bs.record_sat(p)
        else:
            bs.record_unsat(p)
    checks.append(("bisect_finds_boundary", bs.lo == 6 and bs.hi == 7))
    checks.append(("bisect_probe_count", probes <= 4))
    checks.append(("bisect_settles_all", bs.settled() == set(range(12))))

    # Version space: after SAT at 3 and UNSAT at 8, rungs <=3 and >=8 are entailed,
    # rungs 4..7 are not.  This is the discipline the parents already get right.
    vs = VersionSpace(12)
    vs.observe_sat(3)
    vs.observe_unsat(8)
    checks.append(("vs_entails_low", vs.entailed(2) == "SATISFIABLE"))
    checks.append(("vs_entails_high", vs.entailed(9) == "UNSATISFIABLE"))
    checks.append(("vs_silent_middle", all(vs.entailed(r) is None for r in (4, 5, 6, 7))))
    checks.append(("vs_abstains", calibrated_abstention(vs.entailed(5)) == "UNRESOLVED"))
    checks.append(("vs_boundary_sat", vs.entailed(3) == "SATISFIABLE"))
    checks.append(("vs_boundary_unsat", vs.entailed(8) == "UNSATISFIABLE"))

    # Version space must never entail a contradiction after consistent evidence
    vs2 = VersionSpace(12)
    vs2.observe_sat(5)
    checks.append(("vs_no_upward_leak", vs2.entailed(6) is None))
    vs3 = VersionSpace(12)
    vs3.observe_unsat(5)
    checks.append(("vs_no_downward_leak", vs3.entailed(4) is None))

    for name, ok in checks:
        if not ok:
            failures.append(name)
    return (len(checks) - len(failures), len(checks), failures)
