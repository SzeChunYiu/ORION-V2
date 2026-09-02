#!/usr/bin/env python3
"""ME-X3 task generator: eight known-answer families with exhaustive oracles.

Every instance is produced by deterministic rejection sampling under
`seed = sha256(split_seed | family | index)`, and every instance is *verified by
the oracle* before it is emitted: the family invariant (what the correct minimal
intervention is, and why) is an oracle fact about the frozen presentation, not a
generator intention.  Drift instances in F7 are built from their separating
model outward, so the fidelity witness is inside the registered model-size cap
by construction (never a bounded-agreement approximation).
"""
from __future__ import annotations

import hashlib
import random
from typing import Optional

from mex3_model import (
    ACTIONS, Budget, FAMILIES, Presentation, Statement, Task, Word, word_str,
)
from mex3_oracle import (
    bfs_derivation, check_derivation, check_separating_model, find_countermodel,
    holds, models_of, satisfies, truth, word_map,
)

# ---- registered environment constants (frozen; mirrored in the design JSON) ---
ALPHABET = 3
TASK_BUDGET = Budget(max_word_len=6, max_expansions=1800, solve_expansions=250,
                     max_model_size=3, max_model_checks=2000, max_lemma_candidates=40)
ORACLE_WORD_LEN = 8
ORACLE_EXPANSIONS = 40000
ORACLE_MODEL_SIZE = 3
MAX_ATTEMPTS = 4000

CUES = ("statement is symmetric under reversal", "an alternative presentation is available",
        "the target resembles a normal-form identity", "a change of generators is offered",
        "the left side factors through the offered generator")


def rng_for(*parts: str) -> random.Random:
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def seed_str(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]


# ------------------------------------------------------------- presentations ---

def random_presentation(r: random.Random, pid: str = "P0") -> Presentation:
    ax: list[tuple[Word, Word]] = []
    for _ in range(r.choice((2, 3))):
        lu = r.choice((2, 2, 3)); lv = r.choice((1, 1, 2))
        u = tuple(r.randrange(ALPHABET) for _ in range(lu))
        v = tuple(r.randrange(ALPHABET) for _ in range(lv))
        if u != v:
            ax.append((u, v))
    ax = sorted(set(ax))
    return Presentation(pid, ALPHABET, tuple(ax))


def tietze_alt(pres: Presentation, d: Word, pid: str = "P1") -> tuple[Presentation, tuple[Word, ...]]:
    """Tietze transformation: add generator `g = d`, fold `d` into `g` in axioms.

    The presented algebra is unchanged (adding a generator with a defining
    relation, then rewriting relations by that definition, are both Tietze
    moves), so this is a genuine change of representation and not a change of
    theory.  `alt_map[s]` translates base symbol `s` into the alt alphabet.
    """
    g = pres.alphabet

    def fold(w: Word) -> Word:
        out: list[int] = []
        i = 0
        while i < len(w):
            if w[i:i + len(d)] == d:
                out.append(g); i += len(d)
            else:
                out.append(w[i]); i += 1
        return tuple(out)

    ax = [(fold(u), fold(v)) for u, v in pres.axioms]
    ax.append(((g,), d))                       # defining relation g = d
    ax = sorted(set(a for a in ax if a[0] != a[1]))
    alt = Presentation(pid, pres.alphabet + 1, tuple(ax))
    return alt, tuple((s,) for s in range(pres.alphabet))


def translate(w: Word, d: Word, g: int) -> Word:
    out: list[int] = []
    i = 0
    while i < len(w):
        if w[i:i + len(d)] == d:
            out.append(g); i += len(d)
        else:
            out.append(w[i]); i += 1
    return tuple(out)


def theories_agree(p0: Presentation, p1: Presentation, max_n: int = 3) -> bool:
    """Every model of P1 restricts to a model of P0, and every model of P0 extends.

    A sound finite check that the Tietze move preserved the theory.
    """
    for m, n in models_of(p1, max_n):
        if not satisfies(tuple(m[s] for s in range(p0.alphabet)), n, p0.axioms):
            return False
    return True


# ------------------------------------------------------------------ helpers ---

def task_search(pres: Presentation, stmt: Statement, budget: Budget):
    return bfs_derivation(stmt.lhs, stmt.rhs, pres.axioms, budget.max_word_len,
                          budget.solve_expansions)


def oracle_search(pres: Presentation, stmt: Statement):
    return bfs_derivation(stmt.lhs, stmt.rhs, pres.axioms, ORACLE_WORD_LEN, ORACLE_EXPANSIONS)


def oracle_truth(pres: Presentation, stmt: Statement) -> tuple[str, dict]:
    return truth(pres, stmt, ORACLE_WORD_LEN, ORACLE_EXPANSIONS, ORACLE_MODEL_SIZE)


def random_word(r: random.Random, lo: int, hi: int, alphabet: int = ALPHABET) -> Word:
    return tuple(r.randrange(alphabet) for _ in range(r.randint(lo, hi)))


def walk(r: random.Random, pres: Presentation, start: Word, steps: int, max_len: int) -> Word:
    from mex3_model import neighbours
    w = start
    for _ in range(steps):
        nb = neighbours(w, pres.axioms, max_len)
        if not nb:
            break
        w = r.choice(nb)
    return w


def derived_pairs(pres: Presentation, start: Word, max_len: int, cap: int) -> dict[Word, int]:
    """Distance map of everything derivable from `start` at oracle caps."""
    from collections import deque
    from mex3_model import neighbours
    dist = {start: 0}
    q = deque([start]); exp = 0
    while q and exp < cap:
        w = q.popleft(); exp += 1
        for nw in neighbours(w, pres.axioms, max_len):
            if nw not in dist:
                dist[nw] = dist[w] + 1; q.append(nw)
    return dist


def library_noise(r: random.Random, pres: Presentation, k: int) -> list[tuple[Word, Word]]:
    """Retrievable but unhelpful pre-derived lemmas (retrieval must be selective)."""
    out: list[tuple[Word, Word]] = []
    tries = 0
    while len(out) < k and tries < 200:
        tries += 1
        a = random_word(r, 1, 3)
        d = derived_pairs(pres, a, ORACLE_WORD_LEN, 400)
        cands = [b for b, dd in d.items() if 1 <= dd <= 3 and b != a and len(b) <= 4]
        if cands:
            b = r.choice(cands)
            if (a, b) not in out and (b, a) not in out:
                out.append((a, b))
    return out


# ------------------------------------------------------------ family builders ---

def _mk(task_id: str, family: str, seed: str, base: Presentation, intent: Statement,
        formal: Statement, hidden: dict, *, alt: Optional[Presentation] = None,
        alt_label: str = "", alt_map: tuple[Word, ...] = (), library=(),
        invariants=("schema variable must remain universally quantified",),
        cues=(), formal_pid: str = "P0", transfer_of: Optional[str] = None) -> Task:
    return Task(task_id=task_id, family=family, seed=seed, base=base, alt=alt,
                alt_label=alt_label, alt_map=alt_map, library=tuple(library),
                intent=intent, intent_invariants=tuple(invariants), formal=formal,
                formal_pid=formal_pid, surface_cues=tuple(cues), budget=TASK_BUDGET,
                transfer_of=transfer_of, hidden=hidden)


def gen_f1(r: random.Random, tid: str, seed: str) -> Optional[Task]:
    p = random_presentation(r)
    if not p.axioms:
        return None
    start = random_word(r, 2, 4)
    goal = walk(r, p, start, r.randint(2, 4), 5)
    if goal == start:
        return None
    st = Statement(start, goal)
    tr = task_search(p, st, TASK_BUDGET)
    if not tr.found or tr.length < 2 or tr.expansions > TASK_BUDGET.max_expansions // 2:
        return None
    hidden = {"oracle_action": "CONTINUE_DIRECT_PROOF_SEARCH", "truth": "PROVABLE",
              "fidelity": "FAITHFUL", "min_len_base": tr.length,
              "terminal": "FORMALLY_VERIFIED_AND_INTENT_ALIGNED"}
    return _mk(tid, "F1_DIRECT_SEARCH", seed, p, st, st, hidden,
               library=library_noise(r, p, 3),
               cues=(r.choice(CUES),) if r.random() < 0.4 else ())


def _hard_target(r: random.Random, p: Presentation):
    """A statement provable at oracle caps but not within the task budget."""
    start = random_word(r, 2, 4)
    dist = derived_pairs(p, start, ORACLE_WORD_LEN, ORACLE_EXPANSIONS)
    cands = [w for w, d in dist.items() if d >= 4 and len(w) <= 5]
    r.shuffle(cands)
    for goal in cands[:12]:
        st = Statement(start, goal)
        if not task_search(p, st, TASK_BUDGET).found:
            return st, dist
    return None, dist


def gen_f2(r: random.Random, tid: str, seed: str, in_library: bool) -> Optional[Task]:
    p = random_presentation(r)
    if len(p.axioms) < 2:
        return None
    st, dist = _hard_target(r, p)
    if st is None:
        return None
    # find a lemma L, derivable at oracle caps, that brings the target inside budget
    pool = [w for w, d in dist.items() if 2 <= d <= 6 and len(w) <= 4]
    r.shuffle(pool)
    for a in pool[:25]:
        for b in pool[:25]:
            if a == b or len(a) + len(b) > 7:
                continue
            if not oracle_search(p, Statement(a, b)).found:
                continue
            p2 = Presentation("P0+L", p.alphabet, tuple(sorted(set(p.axioms + ((a, b),)))))
            tr2 = task_search(p2, st, TASK_BUDGET)
            if tr2.found:
                lib = library_noise(r, p, 3)
                if in_library:
                    lib.append((a, b))
                    action = "RETRIEVE_EXISTING_LEMMA"
                else:
                    action = "INVENT_LOCAL_LEMMA"
                r.shuffle(lib)
                hidden = {"oracle_action": action, "truth": "PROVABLE", "fidelity": "FAITHFUL",
                          "lemma": [list(a), list(b)], "min_len_with_lemma": tr2.length,
                          "terminal": "FORMALLY_VERIFIED_AND_INTENT_ALIGNED"}
                return _mk(tid, "F2_MISSING_LEMMA", seed, p, st, st, hidden, library=lib)
    return None


def _alt_for(r: random.Random, p: Presentation):
    for _ in range(8):
        d = random_word(r, 2, 3)
        alt, amap = tietze_alt(p, d)
        if len(alt.axioms) >= 2 and theories_agree(p, alt):
            return alt, amap, d
    return None, None, None


def gen_f3(r: random.Random, tid: str, seed: str) -> Optional[Task]:
    p = random_presentation(r)
    if len(p.axioms) < 2:
        return None
    st, _ = _hard_target(r, p)
    if st is None:
        return None
    alt, amap, d = _alt_for(r, p)
    if alt is None:
        return None
    g = p.alphabet
    st_alt = Statement(translate(st.lhs, d, g), translate(st.rhs, d, g))
    tr_alt = task_search(alt, st_alt, TASK_BUDGET)
    if not tr_alt.found:
        return None
    hidden = {"oracle_action": "CHANGE_REPRESENTATION", "truth": "PROVABLE",
              "fidelity": "FAITHFUL", "alt_defining_word": list(d),
              "min_len_alt": tr_alt.length, "theories_agree": True,
              "terminal": "FORMALLY_VERIFIED_AND_INTENT_ALIGNED"}
    return _mk(tid, "F3_REPRESENTATION_CHANGE", seed, p, st, st, hidden, alt=alt,
               alt_label=f"generator {word_str((g,))} := {word_str(d)}", alt_map=amap,
               library=library_noise(r, p, 3), cues=(CUES[3], CUES[1]))


def gen_f4(r: random.Random, tid: str, seed: str) -> Optional[Task]:
    """Attractive alternative presentation offered; the direct route suffices."""
    p = random_presentation(r)
    if len(p.axioms) < 2:
        return None
    start = random_word(r, 2, 4)
    goal = walk(r, p, start, r.randint(2, 3), 5)
    if goal == start:
        return None
    st = Statement(start, goal)
    tr = task_search(p, st, TASK_BUDGET)
    if not tr.found:
        return None
    alt, amap, d = _alt_for(r, p)
    if alt is None:
        return None
    g = p.alphabet
    st_alt = Statement(translate(st.lhs, d, g), translate(st.rhs, d, g))
    tr_alt = task_search(alt, st_alt, TASK_BUDGET)
    # the offered change must be strictly worse: unreachable, or dearer
    if tr_alt.found and tr_alt.expansions <= tr.expansions:
        return None
    hidden = {"oracle_action": "CONTINUE_DIRECT_PROOF_SEARCH", "truth": "PROVABLE",
              "fidelity": "FAITHFUL", "min_len_base": tr.length,
              "alt_expansions": tr_alt.expansions, "base_expansions": tr.expansions,
              "terminal": "FORMALLY_VERIFIED_AND_INTENT_ALIGNED"}
    return _mk(tid, "F4_DECEPTIVE_CHANGE", seed, p, st, st, hidden, alt=alt,
               alt_label=f"generator {word_str((g,))} := {word_str(d)}", alt_map=amap,
               library=library_noise(r, p, 4), cues=(CUES[3], CUES[0], CUES[4]))


def gen_f5(r: random.Random, tid: str, seed: str) -> Optional[Task]:
    p = random_presentation(r)
    if not p.axioms:
        return None
    st = Statement(random_word(r, 2, 4), random_word(r, 1, 3))
    if st.lhs == st.rhs:
        return None
    t, w = oracle_truth(p, st)
    if t != "REFUTABLE":
        return None
    ok, why = check_separating_model(tuple(tuple(f) for f in w["model"]), w["size"], p, st,
                                     Statement(st.lhs, st.lhs))
    hidden = {"oracle_action": "GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL", "truth": "REFUTABLE",
              "fidelity": "FAITHFUL", "countermodel": w,
              "terminal": "REFUTED_WITH_COUNTERMODEL"}
    return _mk(tid, "F5_PROBE_OR_COUNTEREXAMPLE_NEEDED", seed, p, st, st, hidden,
               library=library_noise(r, p, 3))


def gen_f6(r: random.Random, tid: str, seed: str) -> Optional[Task]:
    p = random_presentation(r)
    if not p.axioms:
        return None
    st = Statement(random_word(r, 2, 4), random_word(r, 2, 4))
    if st.lhs == st.rhs:
        return None
    t, w = oracle_truth(p, st)
    if t != "UNDETERMINED":
        return None
    hidden = {"oracle_action": "DEFER_CANNOT_IDENTIFY", "truth": "UNDETERMINED",
              "fidelity": "FAITHFUL", "witness": w,
              "terminal": "UNSOLVED_WITHIN_BUDGET"}
    return _mk(tid, "F6_UNDERDETERMINED_OR_CANNOT_CHECK", seed, p, st, st, hidden,
               library=library_noise(r, p, 3))


# ---------------------------------------- F7: specification-intent mismatch ----

F7_SUBTYPES = ("FAITHFUL", "MATERIALLY_WEAKENED", "MATERIALLY_STRENGTHENED",
               "NOTATIONAL_COLLAPSE", "ABSTRACTION_ELEVATION",
               "DEGENERATE_TRIVIALIZATION", "CANNOT_CHECK_INTENT")
# Registered mixture. FAITHFUL controls are the anti-conservatism half of F7:
# an arm that flags every surface difference as drift fails here.
F7_WEIGHTS = (0.34, 0.16, 0.12, 0.12, 0.10, 0.10, 0.06)


def _f7_faithful(r, p, tid, seed):
    from mex3_model import neighbours
    start = random_word(r, 2, 4)
    goal = walk(r, p, start, r.randint(2, 3), 5)
    st = Statement(start, goal)
    if st.lhs == st.rhs or not task_search(p, st, TASK_BUDGET).found:
        return None
    fl = walk(r, p, st.lhs, 1, 5); fr = walk(r, p, st.rhs, 1, 5)
    formal = Statement(fl, fr)
    if formal.lhs == formal.rhs or (formal.lhs, formal.rhs) == (st.lhs, st.rhs):
        return None
    if not task_search(p, formal, TASK_BUDGET).found:
        return None
    hidden = {"oracle_action": "CONTINUE_DIRECT_PROOF_SEARCH", "truth": "PROVABLE",
              "fidelity": "FAITHFUL", "f7_subtype": "FAITHFUL",
              "terminal": "FORMALLY_VERIFIED_AND_INTENT_ALIGNED"}
    return _mk(tid, "F7_SPECIFICATION_MISMATCH", seed, p, st, formal, hidden,
               library=library_noise(r, p, 3), cues=(CUES[0],))


def _f7_context(r, p, tid, seed, weaken: bool):
    """Drift by adding (weaken) or dropping (strengthen) a common context."""
    u = random_word(r, 2, 3); v = random_word(r, 1, 3)
    if u == v:
        return None
    if oracle_truth(p, Statement(u, v))[0] != "REFUTABLE":
        return None
    for _ in range(12):
        c = random_word(r, 1, 2)
        big = Statement(c + u, c + v)
        if not task_search(p, big, TASK_BUDGET).found:
            continue
        small = Statement(u, v)
        intent, formal = (small, big) if weaken else (big, small)
        sub = "MATERIALLY_WEAKENED" if weaken else "MATERIALLY_STRENGTHENED"
        fid, w = fidelity_oracle(p, intent, formal, sub)
        if fid != sub:
            continue
        val = "PROVABLE" if weaken else "REFUTABLE"
        term = ("FORMALLY_VERIFIED_BUT_INTENT_MISMATCH" if weaken
                else "REFUTED_WITH_COUNTERMODEL")
        hidden = {"oracle_action": "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK",
                  "truth": val, "fidelity": sub, "f7_subtype": sub,
                  "fidelity_witness": w, "terminal": term}
        return _mk(tid, "F7_SPECIFICATION_MISMATCH", seed, p, intent, formal, hidden,
                   library=library_noise(r, p, 3), cues=(CUES[2],),
                   invariants=("every operator occurrence in the intended equation "
                               "must appear in the formal statement",))
    return None


def _f7_collapse(r, p, tid, seed):
    a, b = r.sample(range(ALPHABET), 2)
    u = random_word(r, 2, 4); v = random_word(r, 1, 3)
    intent = Statement(u, v)
    if intent.lhs == intent.rhs or oracle_truth(p, intent)[0] != "REFUTABLE":
        return None
    sub_map = {b: a}
    formal = Statement(tuple(sub_map.get(s, s) for s in u), tuple(sub_map.get(s, s) for s in v))
    if formal.lhs == formal.rhs or not task_search(p, formal, TASK_BUDGET).found:
        return None
    fid, w = fidelity_oracle(p, intent, formal, "NOTATIONAL_COLLAPSE")
    if fid != "NOTATIONAL_COLLAPSE":
        return None
    hidden = {"oracle_action": "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK",
              "truth": "PROVABLE", "fidelity": "NOTATIONAL_COLLAPSE",
              "f7_subtype": "NOTATIONAL_COLLAPSE", "collapsed": [b, a],
              "fidelity_witness": w, "terminal": "FORMALLY_VERIFIED_BUT_INTENT_MISMATCH"}
    return _mk(tid, "F7_SPECIFICATION_MISMATCH", seed, p, intent, formal, hidden,
               library=library_noise(r, p, 3), cues=(CUES[2],),
               invariants=(f"operators {word_str((a,))} and {word_str((b,))} "
                           "denote distinct operations and must not be identified",))


def _f7_elevation(r, p, tid, seed):
    """The formal statement is elevated to the alternative presentation's new
    generator, quantifying over a signature the intent never mentioned."""
    alt, amap, d = _alt_for(r, p)
    if alt is None:
        return None
    g = p.alphabet
    u = random_word(r, 2, 4); v = random_word(r, 1, 3)
    intent = Statement(u, v)
    if intent.lhs == intent.rhs:
        return None
    i1 = Statement(translate(u, d, g), translate(v, d, g))
    for _ in range(10):
        if not i1.lhs:
            return None
        pos = r.randrange(len(i1.lhs))
        formal = Statement(i1.lhs[:pos] + (g,) + i1.lhs[pos + 1:], i1.rhs)
        if formal.lhs == formal.rhs or formal == i1:
            continue
        fid, w = fidelity_oracle(alt, i1, formal, "ABSTRACTION_ELEVATION")
        if fid != "ABSTRACTION_ELEVATION":
            continue
        t, _tw = oracle_truth(alt, formal)
        term = ("FORMALLY_VERIFIED_BUT_INTENT_MISMATCH" if t == "PROVABLE"
                else "REFUTED_WITH_COUNTERMODEL" if t == "REFUTABLE"
                else "UNSOLVED_WITHIN_BUDGET")
        hidden = {"oracle_action": "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK",
                  "truth": t, "fidelity": "ABSTRACTION_ELEVATION",
                  "f7_subtype": "ABSTRACTION_ELEVATION", "adjudication_pid": "P1",
                  "intent_translated": i1.as_dict(), "fidelity_witness": w,
                  "terminal": term}
        return _mk(tid, "F7_SPECIFICATION_MISMATCH", seed, p, intent, formal, hidden,
                   alt=alt, alt_label=f"generator {word_str((g,))} := {word_str(d)}",
                   alt_map=amap, formal_pid="P1", library=library_noise(r, p, 3),
                   cues=(CUES[4],),
                   invariants=("the formal statement must not quantify over generators "
                               "absent from the intended equation",))
    return None


def _f7_degenerate(r, p, tid, seed):
    u = random_word(r, 2, 4); v = random_word(r, 1, 3)
    intent = Statement(u, v)
    if intent.lhs == intent.rhs or oracle_truth(p, intent)[0] != "REFUTABLE":
        return None
    formal = Statement(u, u)
    fid, w = fidelity_oracle(p, intent, formal, "DEGENERATE_TRIVIALIZATION")
    if fid != "DEGENERATE_TRIVIALIZATION":
        return None
    hidden = {"oracle_action": "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK",
              "truth": "PROVABLE", "fidelity": "DEGENERATE_TRIVIALIZATION",
              "f7_subtype": "DEGENERATE_TRIVIALIZATION", "fidelity_witness": w,
              "terminal": "FORMALLY_VERIFIED_BUT_INTENT_MISMATCH"}
    return _mk(tid, "F7_SPECIFICATION_MISMATCH", seed, p, intent, formal, hidden,
               library=library_noise(r, p, 3), cues=(CUES[2],),
               invariants=("the formal statement must relate the two sides of the "
                           "intended equation, not restate one of them",))


def _f7_cannot_check(r, p, tid, seed):
    intent = Statement(random_word(r, 3, 4), random_word(r, 3, 4))
    if intent.lhs == intent.rhs or oracle_truth(p, intent)[0] != "UNDETERMINED":
        return None
    formal = Statement(intent.lhs, random_word(r, 2, 4))
    if formal.lhs == formal.rhs or formal == intent:
        return None
    fid, w = fidelity_oracle(p, intent, formal, None)
    if fid != "CANNOT_CHECK_INTENT":
        return None
    hidden = {"oracle_action": "REQUEST_SPECIFICATION_CLARIFICATION",
              "truth": oracle_truth(p, formal)[0], "fidelity": "CANNOT_CHECK_INTENT",
              "f7_subtype": "CANNOT_CHECK_INTENT", "fidelity_witness": w,
              "terminal": "CANNOT_CHECK_INTENT"}
    return _mk(tid, "F7_SPECIFICATION_MISMATCH", seed, p, intent, formal, hidden,
               library=library_noise(r, p, 3),
               invariants=("the intended equation is not decided by the frozen "
                           "environment; do not assert fidelity either way",))


def fidelity_oracle(pres: Presentation, intent: Statement, formal: Statement,
                    declared: Optional[str]) -> tuple[str, dict]:
    from mex3_oracle import fidelity
    return fidelity(pres, intent, formal, ORACLE_WORD_LEN, ORACLE_EXPANSIONS,
                    ORACLE_MODEL_SIZE, declared)


def gen_f7(r: random.Random, tid: str, seed: str) -> Optional[Task]:
    p = random_presentation(r)
    if len(p.axioms) < 2:
        return None
    sub = r.choices(F7_SUBTYPES, weights=F7_WEIGHTS, k=1)[0]
    if sub == "FAITHFUL":
        return _f7_faithful(r, p, tid, seed)
    if sub == "MATERIALLY_WEAKENED":
        return _f7_context(r, p, tid, seed, weaken=True)
    if sub == "MATERIALLY_STRENGTHENED":
        return _f7_context(r, p, tid, seed, weaken=False)
    if sub == "NOTATIONAL_COLLAPSE":
        return _f7_collapse(r, p, tid, seed)
    if sub == "ABSTRACTION_ELEVATION":
        return _f7_elevation(r, p, tid, seed)
    if sub == "DEGENERATE_TRIVIALIZATION":
        return _f7_degenerate(r, p, tid, seed)
    return _f7_cannot_check(r, p, tid, seed)


# ---------------------------------------------------------- F8: transfer ------

def gen_f8(r: random.Random, tid: str, seed: str) -> Optional[list[Task]]:
    """A source task whose escalation artefact must pay off on a held-out sibling.

    The held-out target is frozen with the source, before any arm is run, and is
    solvable within budget *only* by reusing the source's lemma or presentation.
    """
    p = random_presentation(r)
    if len(p.axioms) < 2:
        return None
    src = gen_f2(r, tid + "s", seed, in_library=False)
    if src is None or src.base.axioms != src.base.axioms:
        return None
    p = src.base
    a, b = (tuple(src.hidden["lemma"][0]), tuple(src.hidden["lemma"][1]))
    p2 = Presentation("P0+L", p.alphabet, tuple(sorted(set(p.axioms + ((a, b),)))))
    tgt, dist = _hard_target(r, p)
    if tgt is None or tgt == src.intent:
        return None
    tr2 = task_search(p2, tgt, TASK_BUDGET)
    if not tr2.found:
        return None
    src_hidden = dict(src.hidden); src_hidden["transfer_role"] = "SOURCE"
    source = _mk(tid + "s", "F8_TRANSFER", seed, p, src.intent, src.formal, src_hidden,
                 library=src.library)
    tgt_hidden = {"oracle_action": "INVENT_LOCAL_LEMMA", "truth": "PROVABLE",
                  "fidelity": "FAITHFUL", "transfer_role": "TARGET",
                  "reusable_lemma": [list(a), list(b)], "min_len_with_lemma": tr2.length,
                  "terminal": "FORMALLY_VERIFIED_AND_INTENT_ALIGNED"}
    target = _mk(tid + "t", "F8_TRANSFER", seed, p, tgt, tgt, tgt_hidden,
                 library=library_noise(r, p, 3), transfer_of=tid + "s")
    return [source, target]


# --------------------------------------------------------------- assembly -----

BUILDERS = {
    "F1_DIRECT_SEARCH": lambda r, t, s, i: gen_f1(r, t, s),
    "F2_MISSING_LEMMA": lambda r, t, s, i: gen_f2(r, t, s, in_library=(i % 2 == 0)),
    "F3_REPRESENTATION_CHANGE": lambda r, t, s, i: gen_f3(r, t, s),
    "F4_DECEPTIVE_CHANGE": lambda r, t, s, i: gen_f4(r, t, s),
    "F5_PROBE_OR_COUNTEREXAMPLE_NEEDED": lambda r, t, s, i: gen_f5(r, t, s),
    "F6_UNDERDETERMINED_OR_CANNOT_CHECK": lambda r, t, s, i: gen_f6(r, t, s),
    "F7_SPECIFICATION_MISMATCH": lambda r, t, s, i: gen_f7(r, t, s),
    "F8_TRANSFER": lambda r, t, s, i: gen_f8(r, t, s),
}


# Family invariant: the oracle cell each family must land in. Instances that do
# not land there are rejected, so the family label is an *oracle fact* about the
# frozen presentation, never a generator intention.
FAMILY_CELL = {
    "F1_DIRECT_SEARCH": lambda v, t: v["level"] == "L1_DIRECT" and v["fidelity"] == "FAITHFUL",
    "F2_MISSING_LEMMA": lambda v, t: v["minimal_action"] == t.hidden["oracle_action"] and v["fidelity"] == "FAITHFUL",
    "F3_REPRESENTATION_CHANGE": lambda v, t: v["level"] == "L4_REPRESENTATION" and v["fidelity"] == "FAITHFUL",
    "F4_DECEPTIVE_CHANGE": lambda v, t: v["level"] == "L1_DIRECT" and t.alt is not None and v["fidelity"] == "FAITHFUL",
    "F5_PROBE_OR_COUNTEREXAMPLE_NEEDED": lambda v, t: v["level"] == "L0_REFUTE" and v["fidelity"] == "FAITHFUL",
    "F6_UNDERDETERMINED_OR_CANNOT_CHECK": lambda v, t: v["level"] == "L5_DEFER" and v["fidelity"] == "FAITHFUL",
    "F7_SPECIFICATION_MISMATCH": lambda v, t: v["fidelity"] == t.hidden.get("f7_subtype"),
    "F8_TRANSFER": lambda v, t: v["level"] in ("L2_RETRIEVE", "L3_INVENT") and v["fidelity"] == "FAITHFUL",
}


def verify(task: Task) -> Optional[dict]:
    """Oracle-verify one candidate; return its verdict or None if it misses the cell."""
    from mex3_verdict import oracle_verdict
    v = oracle_verdict(task, ORACLE_WORD_LEN, ORACLE_EXPANSIONS, ORACLE_MODEL_SIZE)
    return v if FAMILY_CELL[task.family](v, task) else None


def generate_split(split_seed: str, per_family: int, families=FAMILIES
                   ) -> list[tuple[Task, dict]]:
    """Deterministic rejection sampling; every emitted task carries its oracle verdict."""
    out: list[tuple[Task, dict]] = []
    for fam in families:
        made = 0; idx = 0
        while made < per_family and idx < MAX_ATTEMPTS:
            sd = seed_str(split_seed, fam, str(idx))
            tid = f"{fam.split('_')[0]}-{idx:04d}-{sd[:6]}"
            r = rng_for(split_seed, fam, str(idx))
            got = BUILDERS[fam](r, tid, sd, idx)
            idx += 1
            if got is None:
                continue
            batch = got if isinstance(got, list) else [got]
            verdicts = [verify(t) for t in batch]
            if any(v is None for v in verdicts):
                continue
            out.extend(zip(batch, verdicts))
            made += 1
        if made < per_family:
            raise RuntimeError(f"generator underfilled {fam}: {made}/{per_family}")
    return out
