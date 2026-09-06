"""KSO_MECHANISED_CORE_BATCH12_V1 — the finite-oracle side of the Lean ↔ OCM correspondence table, re-run
in stdlib Python over the same fixtures OCM uses (no Lean, no ``ocm`` import), plus source checks on the
Lean project (files exist, toolchain pinned, no external dependency, every theorem named in the tables is
present, no ``sorry`` / ``axiom``).  Python 3.8 compatible (billy-laptop)."""
from __future__ import annotations

import itertools
import re
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Tuple

import pytest

ROOT = Path(__file__).resolve().parents[2]
THEORY = ROOT / "research" / "machine-epistemics-theory"
DOC = THEORY / "KSO_MECHANISED_CORE_BATCH12_V1.md"
LEAN = THEORY / "lean" / "kso_core"
MODULES = ["Liveness", "Profile", "Interval", "Reopening", "Authority", "Mutants"]

# ------------------------------------------------------------------------------------------------
# exact re-implementation of the oracle (OCM src/ocm/kso/warrant.py, types.py, revocation.py)
# ------------------------------------------------------------------------------------------------

Warrant = FrozenSet[int]
Profile = Tuple[Warrant, ...]


def _wkey(w: Warrant):
    return (len(w), tuple(sorted(w)))


def canon(items: Iterable[Iterable[int]]) -> Profile:
    unique = {frozenset(i) for i in items}
    minimal = [w for w in unique if not any(v < w for v in unique)]
    return tuple(sorted(minimal, key=_wkey))


ZERO: Profile = ()
ONE: Profile = (frozenset(),)


def join(a: Profile, b: Profile) -> Profile:
    return canon((*a, *b))


def meet(a: Profile, b: Profile) -> Profile:
    if not a or not b:
        return ZERO
    return canon(x | y for x in a for y in b)


def leq(lower: Profile, upper: Profile) -> bool:
    return all(any(w2 <= w1 for w2 in upper) for w1 in lower)


def live(p: Profile, r: Iterable[int]) -> bool:
    rv = frozenset(r)
    return any(not (w & rv) for w in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"
RANK = {DEAD: 0, UNKNOWN: 1, LIVE: 2}  # Lean constructor order = Kleene truth order


def kand(a: str, b: str) -> str:
    if a == DEAD or b == DEAD:
        return DEAD
    if a == UNKNOWN or b == UNKNOWN:
        return UNKNOWN
    return LIVE


def kor(a: str, b: str) -> str:
    if a == LIVE or b == LIVE:
        return LIVE
    if a == UNKNOWN or b == UNKNOWN:
        return UNKNOWN
    return DEAD


def liveness(lo: Profile, up: Profile, r: Iterable[int]) -> str:
    rv = frozenset(r)
    if live(lo, rv):
        return LIVE
    if not live(up, rv):
        return DEAD
    return UNKNOWN


def powerset(n: int) -> List[FrozenSet[int]]:
    items = tuple(range(n))
    out: List[FrozenSet[int]] = []
    for k in range(n + 1):
        out.extend(frozenset(c) for c in itertools.combinations(items, k))
    return out


def all_profiles(n: int) -> List[Profile]:
    subsets = powerset(n)
    seen = set()
    for mask in range(1 << len(subsets)):
        seen.add(canon(subsets[i] for i in range(len(subsets)) if mask & (1 << i)))
    return sorted(seen, key=lambda p: (len(p), tuple(_wkey(w) for w in p)))


def sem_leq(lo: Profile, up: Profile, revocations: List[FrozenSet[int]]) -> bool:
    """Lean ``Leq``: ∀ R, live lo R → live up R (finite universe)."""
    return all(live(up, r) for r in revocations if live(lo, r))


def impact_cone(edges: List[Tuple[Tuple[str, ...], Tuple[str, ...]]], changed: Iterable[str]) -> FrozenSet[str]:
    cone = set(changed)
    while True:
        add = {u for tails, heads in edges if set(tails) & cone for u in heads}
        if add <= cone:
            return frozenset(cone)
        cone |= add


def one_hop(edges, changed) -> FrozenSet[str]:
    c = set(changed)
    return frozenset(c | {u for tails, heads in edges if set(tails) & c for u in heads})


def auth_meet(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
    keys = set(a) | set(b)
    return {k: min(a.get(k, 0), b.get(k, 0)) for k in keys}


def auth_le(a: Dict[str, int], b: Dict[str, int]) -> bool:
    return all(a.get(k, 0) <= b.get(k, 0) for k in set(a) | set(b))


# ------------------------------------------------------------------------------------------------
# fixtures
# ------------------------------------------------------------------------------------------------

N = 3


@pytest.fixture(scope="module")
def universe():
    ps = all_profiles(N)
    revs = powerset(N)
    intervals = [(lo, up) for lo in ps for up in ps if leq(lo, up)]
    lam = {(i, r): liveness(i[0], i[1], r) for i in intervals for r in revs}
    return ps, revs, intervals, lam


# ------------------------------------------------------------------------------------------------
# Liveness.lean — truth tables, order, monotonicity
# ------------------------------------------------------------------------------------------------

VALUES = (DEAD, UNKNOWN, LIVE)


def test_kleene_tables_match_lean_case_order():
    expect_and = {(DEAD, DEAD): DEAD, (DEAD, UNKNOWN): DEAD, (DEAD, LIVE): DEAD,
                  (UNKNOWN, DEAD): DEAD, (UNKNOWN, UNKNOWN): UNKNOWN, (UNKNOWN, LIVE): UNKNOWN,
                  (LIVE, DEAD): DEAD, (LIVE, UNKNOWN): UNKNOWN, (LIVE, LIVE): LIVE}
    expect_or = {(a, b): {DEAD: LIVE, UNKNOWN: UNKNOWN, LIVE: DEAD}[expect_and[({DEAD: LIVE, UNKNOWN: UNKNOWN, LIVE: DEAD}[a],
                                                                            {DEAD: LIVE, UNKNOWN: UNKNOWN, LIVE: DEAD}[b])]]
                 for a in VALUES for b in VALUES}
    assert {(a, b): kand(a, b) for a in VALUES for b in VALUES} == expect_and
    assert {(a, b): kor(a, b) for a in VALUES for b in VALUES} == expect_or  # De Morgan dual, 9/9


def test_kand_is_min_kor_is_max_and_lattice_laws():
    for a in VALUES:
        assert kand(a, a) == a and kor(a, a) == a
        for b in VALUES:
            assert kand(a, b) == (a if RANK[a] <= RANK[b] else b)      # kand_eq_min
            assert kor(a, b) == (b if RANK[a] <= RANK[b] else a)       # kor_eq_max
            assert kand(a, b) == kand(b, a) and kor(a, b) == kor(b, a)
            assert kand(a, kor(a, b)) == a and kor(a, kand(a, b)) == a  # absorption
            for c in VALUES:
                assert kand(kand(a, b), c) == kand(a, kand(b, c))
                assert kor(kor(a, b), c) == kor(a, kor(b, c))
                assert kand(a, kor(b, c)) == kor(kand(a, b), kand(a, c))


def test_kleene_monotone_all_81_quadruples():
    n = 0
    for a, a2, b, b2 in itertools.product(VALUES, repeat=4):
        if RANK[a] <= RANK[a2] and RANK[b] <= RANK[b2]:
            assert RANK[kand(a, b)] <= RANK[kand(a2, b2)]
            assert RANK[kor(a, b)] <= RANK[kor(a2, b2)]
        n += 1
    assert n == 81
    # a wrong Kleene order (UNKNOWN < DEAD < LIVE) breaks kand_eq_min at (DEAD, UNKNOWN)
    mutant = {UNKNOWN: 0, DEAD: 1, LIVE: 2}
    assert kand(DEAD, UNKNOWN) != (DEAD if mutant[DEAD] <= mutant[UNKNOWN] else UNKNOWN)


# ------------------------------------------------------------------------------------------------
# Profile.lean / Interval.lean — semiring, order coincidence, KS-T21
# ------------------------------------------------------------------------------------------------


def test_profile_counts_and_semiring_up_to_liveness(universe):
    ps, revs, intervals, _ = universe
    assert (len(ps), len(intervals), len(revs)) == (20, 168, 8)  # Dedekind D(3) = 20 antichains
    pair = 0
    for a in ps:
        assert join(a, ZERO) == a and meet(a, ONE) == a and meet(a, ZERO) == ZERO and join(a, a) == a
        for b in ps:
            pair += 1
            for r in revs:
                assert live(join(a, b), r) == (live(a, r) or live(b, r))   # live_join
                assert live(meet(a, b), r) == (live(a, r) and live(b, r))  # live_meet
            assert join(a, b) == join(b, a) and meet(a, b) == meet(b, a)
    assert pair == 400


def test_syntactic_leq_iff_semantic_order(universe):
    """synLeq_iff_leq: OCM ``leq`` equals ∀R (live lo R → live up R) on all 20 × 20 pairs."""
    ps, revs, _, _ = universe
    agree = 0
    for lo in ps:
        for up in ps:
            assert leq(lo, up) == sem_leq(lo, up, revs)
            agree += 1
    assert agree == 400


def test_ks_t21_homomorphism_reduction_refinement(universe):
    ps, revs, intervals, lam = universe
    reduction = homomorphism = refinement = wf = 0
    for a in ps:
        for r in revs:
            v = liveness(a, a, r)
            assert v != UNKNOWN and (v == LIVE) == live(a, r)
            reduction += 1
    for p in intervals:
        for q in intervals:
            m = (meet(p[0], q[0]), meet(p[1], q[1]))
            j = (join(p[0], q[0]), join(p[1], q[1]))
            assert leq(*m) and leq(*j)  # interval well-formedness preserved (oplus / otimes wf)
            wf += 2
            refines = leq(p[0], q[0]) and leq(q[1], p[1])
            for r in revs:
                lp, lq = lam[(p, r)], lam[(q, r)]
                assert liveness(m[0], m[1], r) == kand(lp, lq)
                assert liveness(j[0], j[1], r) == kor(lp, lq)
                homomorphism += 1
                if refines:
                    assert lp == lq or lp == UNKNOWN
                    refinement += 1
    assert (reduction, homomorphism, refinement, wf) == (160, 225792, 27920, 56448)


def test_completeness_bit_counterexample():
    """§1.3: bit-based composite reads UNKNOWN where ∧₃ says DEAD; the interval reads DEAD."""
    def bit_lam(profile, complete, r):
        return LIVE if live(profile, r) else (DEAD if complete else UNKNOWN)
    p, pc = ZERO, False
    q, qc = canon([{2}]), True
    r = {2}
    assert bit_lam(meet(p, q), pc and qc, r) == UNKNOWN
    assert kand(bit_lam(p, pc, r), bit_lam(q, qc, r)) == DEAD
    assert liveness(meet(p, q), meet(ONE, q), r) == DEAD


def test_mutants_unknown_as_dead_live_and_meet_as_union():
    lo, up = ZERO, ONE                         # ⟦0,1⟧ partial, nothing exhibited
    assert liveness(lo, up, ()) == UNKNOWN
    assert (LIVE if live(lo, ()) else DEAD) == DEAD                              # mutant_unknown_as_dead
    lo2, up2 = ZERO, canon([{0}])
    assert liveness(lo2, up2, {0}) == DEAD
    assert (LIVE if live(lo2, {0}) else (DEAD if lo2 == up2 else LIVE)) == LIVE  # mutant_unknown_as_live
    p, q = canon([{0}]), canon([{1}])
    assert live(join(p, q), {1}) and not live(meet(p, q), {1})                  # mutant_meet_as_union


# ------------------------------------------------------------------------------------------------
# Reopening.lean — antitone liveness, revoked support, cone
# ------------------------------------------------------------------------------------------------


def test_liveness_antitone_in_revocation(universe):
    _, revs, intervals, lam = universe
    checks = 0
    for i in intervals:
        for r in revs:
            for r2 in revs:
                if r <= r2:
                    assert RANK[lam[(i, r2)]] <= RANK[lam[(i, r)]]  # lam_antitone
                    checks += 1
    assert checks == 4536  # batch-10 J1 (i) count
    # revoked-support: every exhibited warrant hit ⇒ never LIVE; every possible warrant hit ⇒ DEAD
    for lo, up in intervals:
        for r in revs:
            if all(w & r for w in lo):
                assert lam[((lo, up), r)] != LIVE
            if all(w & r for w in up):
                assert lam[((lo, up), r)] == DEAD
    assert all(liveness(ZERO, ZERO, r) == DEAD for r in revs)  # KS-T18 corollary
    assert all(liveness(ONE, ONE, r) == LIVE for r in revs)


WITNESS_EDGES = [(("a",), ("b",)), (("b",), ("c",)), (("c",), ("d",)), (("a",), ("e",)),
                 (("x",), ("y",)), (("y",), ("x",)), (("b", "z"), ("d",))]
WITNESS_ATOMS = ["a", "b", "c", "d", "e", "x", "y", "z"]


def test_impact_cone_witness_and_union_distributivity():
    cone = impact_cone(WITNESS_EDGES, {"a"})
    assert cone == frozenset("abcde")
    assert impact_cone(WITNESS_EDGES, {"x"}) == frozenset("xy")           # cycle
    assert impact_cone(WITNESS_EDGES, set()) == frozenset()                # reach_nil
    shallow = one_hop(WITNESS_EDGES, {"a"})
    assert shallow != cone and "c" not in shallow                          # mutant_impact_cone_direct_only
    for extra in ({"x"}, {"x", "y"}, {"z"}):
        assert cone <= impact_cone(WITNESS_EDGES, {"a"} | extra)           # reach_mono
    subsets = [frozenset(s) for k in range(len(WITNESS_ATOMS) + 1) for s in itertools.combinations(WITNESS_ATOMS, k)]
    unions = 0
    for s1 in subsets[:16]:
        for s2 in subsets[:16]:
            assert impact_cone(WITNESS_EDGES, s1 | s2) == impact_cone(WITNESS_EDGES, s1) | impact_cone(WITNESS_EDGES, s2)
            unions += 1
    assert unions == 256                                                   # reach_union
    # liveness-changed set ⊆ cone; unchanged outside (KS-T22 (1)/(2) liveness halves)
    ival = {"a": (canon([{0}]), canon([{0}])), "e": (canon([{0}, {5}]), canon([{0}, {5}]))}
    for v in WITNESS_ATOMS:
        ival.setdefault(v, (ONE, ONE))
    changed = {v for v in WITNESS_ATOMS if liveness(*ival[v], ()) != liveness(*ival[v], (0,))}
    assert changed == {"a"} and changed <= impact_cone(WITNESS_EDGES, changed)
    assert all(liveness(*ival[v], ()) == liveness(*ival[v], (0,)) for v in WITNESS_ATOMS if v not in impact_cone(WITNESS_EDGES, changed))


def test_dead_seed_and_cone_monotone_in_revocation(universe):
    """deadSet_mono / reachDead_mono on the witness with the 168 intervals on atom ``a``."""
    _, revs, intervals, lam = universe
    for i in intervals:
        for r in revs:
            for r2 in revs:
                if r <= r2:
                    dead_r = {"a"} if lam[(i, r)] != LIVE else set()
                    dead_r2 = {"a"} if lam[(i, r2)] != LIVE else set()
                    assert dead_r <= dead_r2
                    assert impact_cone(WITNESS_EDGES, dead_r) <= impact_cone(WITNESS_EDGES, dead_r2)


# ------------------------------------------------------------------------------------------------
# Authority.lean — meet never raises, glb, commit bottom
# ------------------------------------------------------------------------------------------------


def test_authority_meet_glb_and_max_mutant():
    coords = ("world_truth", "speaker", "commit")
    lattice = [dict(zip(coords, v)) for v in itertools.product((0, 1, 2), repeat=3)]
    pairs = caught = 0
    for a in lattice:
        for b in lattice:
            m = auth_meet(a, b)
            assert auth_le(m, a) and auth_le(m, b)                                   # meet_le_left/right
            for c in lattice:
                if auth_le(c, a) and auth_le(c, b):
                    assert auth_le(c, m)                                              # le_meet
            assert auth_meet(a, b) == auth_meet(b, a) and auth_meet(a, a) == a
            mx = {k: max(a.get(k, 0), b.get(k, 0)) for k in coords}
            if not auth_le(mx, a):
                caught += 1                                                          # mutant_authority_max
            pairs += 1
    assert pairs == 729 and caught > 0


def test_internal_authority_commit_bottom():
    op = {"world_truth": 1, "speaker": 1}            # commit undeclared = 0
    receipt = {"world_truth": 1, "commit": 1}
    other = {"world_truth": 2, "speaker": 2, "commit": 1}
    m = op
    for t in (receipt, other):
        m = auth_meet(m, t)
    internal = {k: v for k, v in m.items() if k != "commit"}
    assert m.get("commit", 0) == 0 and internal.get("commit", 0) == 0      # InternalOnly.commit_zero
    assert auth_le(internal, receipt) and auth_le(internal, other)          # meetAll_le_mem
    assert internal.get("world_truth", 0) == 1                              # no-alarm: world_truth kept
    tails_only = auth_meet(receipt, {"commit": 1, "speaker": 1})
    assert tails_only["commit"] == 1                                        # dropping the operator factor mints commit


# ------------------------------------------------------------------------------------------------
# Lean source checks (no Lean needed)
# ------------------------------------------------------------------------------------------------


def _lean_sources() -> Dict[str, str]:
    return {m: (LEAN / "KsoCore" / f"{m}.lean").read_text(encoding="utf-8") for m in MODULES}


def test_lean_project_layout_and_pin():
    assert (LEAN / "lakefile.lean").exists() and (LEAN / "KsoCore.lean").exists()
    assert (LEAN / "lean-toolchain").read_text().strip() == "leanprover/lean4:v4.14.0"
    lakefile = (LEAN / "lakefile.lean").read_text()
    code = re.sub(r"--[^\n]*", "", lakefile)
    assert not re.search(r"^\s*require\b", code, flags=re.M) and "mathlib" not in code.lower()   # no external dependency
    root = (LEAN / "KsoCore.lean").read_text()
    for m in MODULES:
        assert f"import KsoCore.{m}" in root
    for m, src in _lean_sources().items():
        assert src.strip(), m


def _declared_names(src: str) -> set:
    names = set(re.findall(r"^(?:theorem|def|instance|structure|inductive)\s+([A-Za-z_][A-Za-z0-9_.']*)", src, flags=re.M))
    # constructors of inductives count as declared names for the table (e.g. InternalOnly.commit_zero is a theorem)
    return names


def test_every_table_name_is_declared_and_no_sorry_or_axiom():
    text = DOC.read_text(encoding="utf-8")
    sources = _lean_sources()
    declared = set()
    for src in sources.values():
        declared |= _declared_names(src)
    # names come from the first column of the §2 table and from the controls paragraph / §4 table
    table_names = set()
    for line in text.splitlines():
        if line.startswith("| `") and "|" in line[3:]:
            first_col = line[1:].split("|")[0]
            table_names |= set(re.findall(r"`([A-Za-z_][A-Za-z0-9_.']*)`", first_col))
    controls = re.search(r"Controls \(all PROVED.*?\n\n", text, flags=re.S)
    assert controls is not None
    control_names = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_.']*)`", controls.group(0)))
    wanted = {n for n in table_names | control_names if n not in {"KsoCore", "example"}}  # `example` is the Lean keyword
    # strip a leading module qualifier (`Interval.oplus` → both forms acceptable)
    missing = [n for n in wanted if n not in declared and n.split(".")[-1] not in declared]
    assert not missing, missing
    assert len(wanted) >= 90
    for m, src in sources.items():
        code = re.sub(r"/-.*?-/", "", src, flags=re.S)
        code = re.sub(r"--[^\n]*", "", code)
        assert not re.search(r"\bsorry\b", code), m
        assert not re.search(r"^\s*axiom\b", code, flags=re.M), m
        assert "sorryAx" not in code


def test_document_receipt_lines_present():
    text = DOC.read_text(encoding="utf-8")
    assert "Build completed successfully." in text and "rc=0" in text and "audit_rc=0" in text
    assert "leanprover/lean4:v4.14.0" in text
    assert "sorryAx" not in text.split("== axiom audit")[1].split("audit_rc")[0]
    assert "NOVELTY   NOT_ESTABLISHED" in text
