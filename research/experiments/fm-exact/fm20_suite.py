#!/usr/bin/env python3
"""FM20 — anti-unification / least general generalization: exact study.

The registered task is **not** "compute the LGG".  Plotkin's anti-unification
decides that exactly, so a study built on it would report parent sufficiency by
construction rather than by measurement.  Each instance instead presents

    positives P   ground terms the abstraction must cover,
    negatives N   ground terms it must not cover,
    held-out H    ground terms whose coverage the arm must predict,

and asks for a **registered disposition plus a held-out coverage vector**:

    ACCEPT_LGG                    the least general generalization of P covers
                                  no negative and is not vacuous;
    REJECT_OVER_GENERAL           the LGG covers at least one negative;
    REJECT_NO_COMMON_STRUCTURE    the LGG is a bare variable - the positives
                                  share no structure at all, so the "abstraction"
                                  is vacuous and accepting it would be a false
                                  analogy.

Note a fact about the generalization lattice that the design depends on and does
not hide: every common generalization of P is *more general than or equal to*
the LGG (Plotkin 1970), so if the LGG covers a negative then so does every
common generalization.  There is therefore no "specialize until consistent"
disposition in pure anti-unification, and the three dispositions above are
exhaustive.  Vacuity is registered as dominating over-generality: a bare
variable is not an abstraction at all.

Consequence, and the reason the suite is worth running: **no single parent owns
the endpoint.**  Plotkin's LGG produces the right term but has no notion of a
negative example and no notion of vacuity.  Candidate elimination (Mitchell
1982) owns the negatives but will happily return a bare variable when no
negative excludes it.  An MDL/compression criterion owns vacuity but chooses its
own term and can over-generalize away a real shared regularity.  The strongest
faithful comparator is their federation under a pre-registered, outcome-blind
rule.

Oracle validity rests on two independent algorithms agreeing on the LGG:

  * `lgg_plotkin`     - anti-unification proper: fold pairwise generalization
    with a substitution table keyed by the pair of disagreeing subterms, which
    is what makes repeated structure share one variable;
  * `lgg_exhaustive`  - enumerate the generalization lattice directly.  Every
    generalization of `P[0]` is `P[0]` with an antichain of positions replaced
    by variables, where positions sharing a variable carry equal subterms in
    `P[0]`.  Enumerate all of them, keep those covering every positive, and take
    the unique minimum under the generality order - verifying uniqueness rather
    than assuming Plotkin's theorem.

They share no code beyond the term representation and the matcher.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from typing import Iterable, Sequence

from fm_core import ArmSpec, PlantedPositive, SuiteSpec

# --------------------------------------------------------------------------
# term representation
# --------------------------------------------------------------------------
# A term is a tuple: (symbol, *subterms).  A variable is ("?", name).
# Ground terms contain no variables.

VAR = "?"
FUNCTIONS = (("f", 2), ("g", 1), ("h", 2))
CONSTANTS = ("a", "b", "c", "d")

Term = tuple


def is_var(t: Term) -> bool:
    return len(t) == 2 and t[0] == VAR and isinstance(t[1], str)


def term_str(t: Term) -> str:
    if is_var(t):
        return str(t[1])
    if len(t) == 1:
        return str(t[0])
    return f"{t[0]}({','.join(term_str(x) for x in t[1:])})"


def size(t: Term) -> int:
    if is_var(t):
        return 1
    return 1 + sum(size(x) for x in t[1:])


def variables(t: Term) -> set[str]:
    if is_var(t):
        return {t[1]}
    return set().union(*(variables(x) for x in t[1:])) if len(t) > 1 else set()


def positions(t: Term, prefix: tuple = ()) -> list[tuple]:
    out = [prefix]
    if not is_var(t):
        for i, sub in enumerate(t[1:]):
            out.extend(positions(sub, prefix + (i,)))
    return out


def at(t: Term, pos: tuple) -> Term:
    for i in pos:
        t = t[1 + i]
    return t


def replace_at(t: Term, pos: tuple, new: Term) -> Term:
    if not pos:
        return new
    i = pos[0]
    return t[: 1 + i] + (replace_at(t[1 + i], pos[1:], new),) + t[2 + i :]


def match(pattern: Term, target: Term, binding: dict | None = None) -> dict | None:
    """One-way matching: return a substitution s with pattern*s == target."""
    binding = {} if binding is None else binding
    if is_var(pattern):
        prev = binding.get(pattern[1])
        if prev is not None:
            return binding if prev == target else None
        binding = dict(binding)
        binding[pattern[1]] = target
        return binding
    if is_var(target) or pattern[0] != target[0] or len(pattern) != len(target):
        return None
    for p, t in zip(pattern[1:], target[1:]):
        binding = match(p, t, binding)
        if binding is None:
            return None
    return binding


def covers(pattern: Term, ground: Term) -> bool:
    return match(pattern, ground) is not None


def more_general(a: Term, b: Term) -> bool:
    """a is more general than or equal to b (a subsumes b under substitution)."""
    return match(a, b) is not None


def alpha_key(t: Term) -> str:
    """Canonical form up to variable renaming, for identity comparisons."""
    names: dict[str, str] = {}

    def go(x: Term) -> str:
        if is_var(x):
            names.setdefault(x[1], f"V{len(names)}")
            return names[x[1]]
        if len(x) == 1:
            return str(x[0])
        return f"{x[0]}({','.join(go(s) for s in x[1:])})"

    return go(t)


# --------------------------------------------------------------------------
# oracle 1 — Plotkin anti-unification
# --------------------------------------------------------------------------


def lgg_plotkin(terms: Sequence[Term]) -> Term:
    """Least general generalization (Plotkin 1970; Reynolds 1970).

    Pairwise generalization is folded across the list.  The substitution table
    is keyed by the *pair* of disagreeing subterms, which is exactly what makes
    two occurrences of the same disagreement share one variable - the property
    that distinguishes anti-unification from position-wise variablisation.
    """

    def pair(s: Term, t: Term, table: dict, counter: list) -> Term:
        if s == t and not is_var(s):
            return s
        if not is_var(s) and not is_var(t) and s[0] == t[0] and len(s) == len(t):
            return (s[0],) + tuple(pair(a, b, table, counter) for a, b in zip(s[1:], t[1:]))
        key = (alpha_key(s), alpha_key(t)) if (is_var(s) or is_var(t)) else (s, t)
        if key not in table:
            table[key] = (VAR, f"X{counter[0]}")
            counter[0] += 1
        return table[key]

    if not terms:
        raise ValueError("lgg of the empty set is undefined")
    acc = terms[0]
    for nxt in terms[1:]:
        acc = pair(acc, nxt, {}, [0])
    # renumber variables canonically
    names: dict[str, str] = {}

    def renum(x: Term) -> Term:
        if is_var(x):
            names.setdefault(x[1], f"X{len(names)}")
            return (VAR, names[x[1]])
        if len(x) == 1:
            return x
        return (x[0],) + tuple(renum(s) for s in x[1:])

    return renum(acc)


# --------------------------------------------------------------------------
# oracle 2 — exhaustive generalization-lattice enumeration
# --------------------------------------------------------------------------


def _antichains(pos_list: Sequence[tuple], limit: int = 4096) -> Iterable[tuple]:
    """All antichains of positions (no position a prefix of another)."""
    out: list[tuple] = [()]
    for p in pos_list:
        new = []
        for chain in out:
            if all(not (p[: len(q)] == q or q[: len(p)] == p) for q in chain):
                new.append(chain + (p,))
        out.extend(new)
        if len(out) > limit:  # pragma: no cover - generator keeps terms small
            raise RuntimeError("antichain enumeration exceeded the registered bound")
    return out


def _partitions(items: Sequence[tuple], equal) -> Iterable[list[list[tuple]]]:
    """Partitions of `items` whose blocks are pairwise `equal`."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for sub in _partitions(rest, equal):
        for i, block in enumerate(sub):
            if all(equal(first, m) for m in block):
                yield sub[:i] + [[first] + block] + sub[i + 1 :]
        yield [[first]] + sub


def lgg_exhaustive(terms: Sequence[Term]) -> tuple[Term, int, bool]:
    """Enumerate the generalization lattice of terms[0] and take the minimum.

    Returns (lgg, n_covering_patterns, minimum_is_unique).  Uniqueness is
    *verified* here rather than assumed from Plotkin's theorem.
    """
    base = terms[0]
    pos_list = positions(base)
    covering: list[Term] = []
    seen: set[str] = set()
    for chain in _antichains(pos_list):
        for part in _partitions(list(chain), lambda p, q: at(base, p) == at(base, q)):
            pat = base
            for k, block in enumerate(part):
                for p in block:
                    pat = replace_at(pat, p, (VAR, f"X{k}"))
            key = alpha_key(pat)
            if key in seen:
                continue
            seen.add(key)
            if all(covers(pat, t) for t in terms):
                covering.append(pat)
    if not covering:  # pragma: no cover - the bare variable always covers
        raise RuntimeError("no covering pattern; the lattice enumeration is wrong")
    minima = [p for p in covering if all(more_general(q, p) for q in covering)]
    unique = len({alpha_key(p) for p in minima}) == 1
    return minima[0], len(covering), unique


# --------------------------------------------------------------------------
# dispositions
# --------------------------------------------------------------------------

FAMILIES = (
    "LEAST_GENERAL_PATTERN",
    "DISTRACTOR_REGULARITY",
    "OVER_GENERALIZATION",
    "UNDER_GENERALIZATION",
    "NO_VALID_COMMON_ABSTRACTION",
)

DISPOSITIONS = ("ACCEPT_LGG", "REJECT_OVER_GENERAL", "REJECT_NO_COMMON_STRUCTURE")


@dataclass(frozen=True)
class Instance:
    instance_id: str
    family: str
    seed: int
    positives: tuple[Term, ...]
    negatives: tuple[Term, ...]
    held_out: tuple[Term, ...]

    def as_json(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,
            "positives": [term_str(t) for t in self.positives],
            "negatives": [term_str(t) for t in self.negatives],
            "held_out": [term_str(t) for t in self.held_out],
        }


@dataclass(frozen=True)
class OracleAnswer:
    disposition: str
    lgg: str
    coverage: tuple[bool, ...]
    n_covering_patterns: int
    minimum_unique: bool

    def as_dict(self) -> dict:
        return {
            "disposition": self.disposition,
            "lgg": self.lgg,
            "coverage": list(self.coverage),
            "n_covering_patterns": self.n_covering_patterns,
            "minimum_unique": self.minimum_unique,
        }


def classify(lgg: Term, negatives: Sequence[Term]) -> str:
    if is_var(lgg):
        return "REJECT_NO_COMMON_STRUCTURE"  # vacuity dominates, by registration
    if any(covers(lgg, n) for n in negatives):
        return "REJECT_OVER_GENERAL"
    return "ACCEPT_LGG"


def oracle_exhaustive(inst: Instance) -> OracleAnswer:
    lgg, n_cov, unique = lgg_exhaustive(inst.positives)
    return OracleAnswer(
        classify(lgg, inst.negatives),
        alpha_key(lgg),
        tuple(covers(lgg, h) for h in inst.held_out),
        n_cov,
        unique,
    )


def oracle_plotkin(inst: Instance) -> OracleAnswer:
    lgg = lgg_plotkin(inst.positives)
    return OracleAnswer(
        classify(lgg, inst.negatives),
        alpha_key(lgg),
        tuple(covers(lgg, h) for h in inst.held_out),
        -1,
        True,
    )


def oracle_agrees(inst: Instance) -> tuple[bool, OracleAnswer, OracleAnswer]:
    a, b = oracle_exhaustive(inst), oracle_plotkin(inst)
    same = a.disposition == b.disposition and a.lgg == b.lgg and a.coverage == b.coverage
    return same and a.minimum_unique, a, b


# --------------------------------------------------------------------------
# generator
# --------------------------------------------------------------------------


def _random_ground(rng: random.Random, depth: int) -> Term:
    if depth <= 0 or rng.random() < 0.35:
        return (rng.choice(CONSTANTS),)
    sym, ar = rng.choice(FUNCTIONS)
    return (sym,) + tuple(_random_ground(rng, depth - 1) for _ in range(ar))


def _instantiate(pattern: Term, rng: random.Random, depth: int = 1) -> Term:
    sub = {v: _random_ground(rng, depth) for v in sorted(variables(pattern))}

    def go(t: Term) -> Term:
        if is_var(t):
            return sub[t[1]]
        if len(t) == 1:
            return t
        return (t[0],) + tuple(go(s) for s in t[1:])

    return go(pattern)


def _random_pattern(rng: random.Random, n_vars: int) -> Term:
    """A skeleton with `n_vars` distinct variables, used to plant a known LGG."""
    base = _random_ground(rng, 2)
    pos = [p for p in positions(base) if p]
    rng.shuffle(pos)
    chosen: list[tuple] = []
    for p in pos:
        if len(chosen) >= n_vars:
            break
        if all(not (p[: len(q)] == q or q[: len(p)] == p) for q in chosen):
            chosen.append(p)
    for k, p in enumerate(chosen):
        base = replace_at(base, p, (VAR, f"X{k}"))
    return base


def _repeated_variable_pattern(rng: random.Random) -> Term | None:
    """A pattern with one variable occurring at two independent positions."""
    for _ in range(24):
        sym, ar = rng.choice([f for f in FUNCTIONS if f[1] == 2])
        inner = _random_ground(rng, 1)
        pat = (sym, (VAR, "X0"), (VAR, "X0"))
        if rng.random() < 0.5:
            pat = (sym, (VAR, "X0"), ("g", (VAR, "X0")))
        _ = inner
        return pat
    return None  # pragma: no cover


def _break_repetition(pattern: Term, rng: random.Random) -> Term | None:
    """Instantiate a repeated variable with two different ground terms."""
    vs = sorted(variables(pattern))
    if not vs:
        return None
    v = vs[0]
    first = [True]

    def go(t: Term) -> Term:
        if is_var(t):
            if t[1] == v:
                if first[0]:
                    first[0] = False
                    return (CONSTANTS[0],)
                return (CONSTANTS[1],)
            return _random_ground(rng, 1)
        if len(t) == 1:
            return t
        return (t[0],) + tuple(go(x) for x in t[1:])

    return go(pattern)


def _generate_one(family: str, seed: int, idx: int) -> Instance | None:
    rng = random.Random(seed)
    if family == "NO_VALID_COMMON_ABSTRACTION":
        # positives with different top symbols: the LGG is a bare variable
        pos = [_random_ground(rng, 2), _random_ground(rng, 2)]
        if pos[0][0] == pos[1][0]:
            return None
        negs = tuple(_random_ground(rng, 2) for _ in range(rng.randint(0, 2)))
        held = tuple(_random_ground(rng, 2) for _ in range(3))
        return Instance(f"{family}-{idx:05d}", family, seed, tuple(pos), negs, held)

    if family == "DISTRACTOR_REGULARITY":
        # a pattern with the SAME variable at two positions: anti-unification
        # shares one variable there, position-wise variablisation does not, and
        # the negative below separates the two
        pattern = _repeated_variable_pattern(rng)
        if pattern is None:
            return None
    else:
        pattern = _random_pattern(rng, rng.randint(1, 2))
    if not variables(pattern):
        return None
    pos = [_instantiate(pattern, rng) for _ in range(rng.randint(2, 3))]
    if len({alpha_key(p) for p in pos}) < 2:
        return None

    if family == "LEAST_GENERAL_PATTERN":
        negs = tuple(t for t in (_random_ground(rng, 2) for _ in range(2)) if not covers(pattern, t))
        held = tuple(_instantiate(pattern, rng) for _ in range(2)) + (_random_ground(rng, 2),)
    elif family == "DISTRACTOR_REGULARITY":
        # the negative instantiates the two repeated positions DIFFERENTLY: the
        # true (variable-sharing) LGG does not cover it, a position-wise
        # generalizer's pattern does
        neg = _break_repetition(pattern, rng)
        if neg is None or covers(pattern, neg):
            return None
        negs = (neg,)
        held = tuple(_instantiate(pattern, rng) for _ in range(3))
    elif family == "OVER_GENERALIZATION":
        # a negative that the LGG covers: instantiate the pattern itself
        negs = (_instantiate(pattern, rng),)
        if any(alpha_key(negs[0]) == alpha_key(p) for p in pos):
            return None
        held = tuple(_instantiate(pattern, rng) for _ in range(3))
    elif family == "UNDER_GENERALIZATION":
        # held-out positives that only the true (least general) LGG covers;
        # an under-general arm predicts their coverage wrongly
        negs = tuple(t for t in (_random_ground(rng, 2) for _ in range(2)) if not covers(pattern, t))
        held = tuple(_instantiate(pattern, rng) for _ in range(4))
    else:  # pragma: no cover
        raise ValueError(family)
    return Instance(f"{family}-{idx:05d}", family, seed, tuple(pos), tuple(negs), tuple(held))


EXPECTED_DISPOSITION = {
    "LEAST_GENERAL_PATTERN": {"ACCEPT_LGG"},
    "DISTRACTOR_REGULARITY": {"ACCEPT_LGG"},
    "OVER_GENERALIZATION": {"REJECT_OVER_GENERAL"},
    "UNDER_GENERALIZATION": {"ACCEPT_LGG"},
    "NO_VALID_COMMON_ABSTRACTION": {"REJECT_NO_COMMON_STRUCTURE"},
}


def generate_split(split: str, seed: str, per_family: dict[str, int]):
    pairs: list[tuple[Instance, OracleAnswer]] = []
    rejects = {f: 0 for f in FAMILIES}
    for family in FAMILIES:
        want = per_family.get(family, 0)
        made = counter = 0
        while made < want:
            counter += 1
            if counter > 4000 * (want + 1):  # pragma: no cover
                raise RuntimeError(f"{split}/{family}: generator could not fill quota")
            s = int.from_bytes(
                hashlib.sha256(f"{seed}|{split}|{family}|{counter}".encode()).digest()[:8], "big"
            )
            inst = _generate_one(family, s, counter)
            if inst is None:
                rejects[family] += 1
                continue
            try:
                same, a, _ = oracle_agrees(inst)
            except RuntimeError:
                rejects[family] += 1
                continue
            if not same or a.disposition not in EXPECTED_DISPOSITION[family]:
                rejects[family] += 1
                continue
            # UNDER_GENERALIZATION must actually discriminate: at least one
            # held-out instance must be covered by the LGG
            if family == "UNDER_GENERALIZATION" and not any(a.coverage):
                rejects[family] += 1
                continue
            made += 1
            pairs.append((inst, a))
    return pairs, rejects


# --------------------------------------------------------------------------
# parents
# --------------------------------------------------------------------------


def _out(pattern: Term | None, disposition: str, inst: Instance) -> dict:
    cov = tuple(covers(pattern, h) for h in inst.held_out) if pattern is not None else tuple(
        False for _ in inst.held_out
    )
    return {
        "disposition": disposition,
        "pattern": alpha_key(pattern) if pattern is not None else None,
        "coverage": list(cov),
    }


def parent_fixed_lesson(inst: Instance) -> dict:
    """P0 — fixed-lesson injection.

    The frozen rule the protocol requires: keep the common skeleton and put a
    *fresh* variable at every position where the positives disagree, with no
    variable sharing.  This is a real and commonly used heuristic; it differs
    from anti-unification exactly in that repeated disagreements do not share a
    variable, so it over-generalises whenever structure repeats.
    """
    base = inst.positives[0]
    pat = base
    counter = [0]

    def go(t: Term, others: list[Term]) -> Term:
        if any(is_var(o) for o in others):
            counter[0] += 1
            return (VAR, f"Y{counter[0]}")
        if all(o == t for o in others):
            return t
        if all(not is_var(o) and o[0] == t[0] and len(o) == len(t) for o in others):
            return (t[0],) + tuple(
                go(t[1 + i], [o[1 + i] for o in others]) for i in range(len(t) - 1)
            )
        counter[0] += 1
        return (VAR, f"Y{counter[0]}")

    pat = go(base, list(inst.positives[1:]))
    if is_var(pat):
        return _out(pat, "REJECT_NO_COMMON_STRUCTURE", inst)
    return _out(pat, "ACCEPT_LGG", inst)


def parent_plotkin(inst: Instance) -> dict:
    """P1 — Plotkin/Reynolds anti-unification.

    Computes the least general generalization exactly.  It has no notion of a
    negative example and no notion of vacuity: within its own theory every LGG
    is a legitimate answer, so it always accepts.  That is its native boundary,
    not a handicap imposed here.
    """
    return _out(lgg_plotkin(inst.positives), "ACCEPT_LGG", inst)


def parent_candidate_elimination(inst: Instance) -> dict:
    """P2 — candidate elimination / version spaces (Mitchell 1982).

    The specific boundary S after processing all positives is the LGG; the
    hypothesis is rejected when S covers a negative example.  Owns the negatives
    exactly.  It has no compression criterion, so a bare variable consistent
    with the negatives is, for it, a perfectly good hypothesis - its boundary.
    """
    s = lgg_plotkin(inst.positives)
    if any(covers(s, n) for n in inst.negatives):
        return _out(s, "REJECT_OVER_GENERAL", inst)
    return _out(s, "ACCEPT_LGG", inst)


def parent_mdl(inst: Instance) -> dict:
    """P3 — minimum description length selection.

    Chooses the covering pattern minimising |pattern| + sum of the sizes of the
    substitutions each positive needs, then rejects the result if it does not
    compress at all (a bare variable).  A genuine, different criterion: MDL is
    free to prefer a *more* general pattern than the LGG when the substitutions
    it saves outweigh the structure it drops, so it can generalise away a real
    shared regularity.  That is its native boundary.
    """
    base = inst.positives[0]
    best, best_cost = None, None
    for chain in _antichains(positions(base)):
        for part in _partitions(list(chain), lambda p, q: at(base, p) == at(base, q)):
            pat = base
            for k, block in enumerate(part):
                for p in block:
                    pat = replace_at(pat, p, (VAR, f"X{k}"))
            if not all(covers(pat, t) for t in inst.positives):
                continue
            cost = size(pat)
            for t in inst.positives:
                b = match(pat, t)
                cost += sum(size(v) for v in b.values())
            if best_cost is None or cost < best_cost:
                best, best_cost = pat, cost
    if best is None or is_var(best):  # pragma: no cover - bare variable always covers
        return _out(best, "REJECT_NO_COMMON_STRUCTURE", inst)
    return _out(best, "ACCEPT_LGG", inst)


# --------------------------------------------------------------------------
# federation, mechanic, ablations, controls
# --------------------------------------------------------------------------


def federation(inst: Instance) -> dict:
    """F0 — strongest faithful parent federation, pre-registered and outcome-blind.

    P1 supplies the term (it is the exact owner of the generalization question);
    P3's compression criterion may veto it as vacuous; P2's negative test may
    then veto it as over-general.  Vacuity is checked first, per the registered
    classification order.  No parent is consulted outside its competence and
    none ever sees the oracle.
    """
    p1 = parent_plotkin(inst)
    lgg = lgg_plotkin(inst.positives)
    if is_var(lgg):
        return {**_out(lgg, "REJECT_NO_COMMON_STRUCTURE", inst), "source": "P3"}
    if any(covers(lgg, n) for n in inst.negatives):
        return {**_out(lgg, "REJECT_OVER_GENERAL", inst), "source": "P2"}
    return {**p1, "source": "P1+P2+P3"}


def mechanic_full(inst: Instance) -> dict:
    """M — ORION abstraction induction, full.

    **Independent implementation, deliberately.**  M does not call Plotkin's
    algorithm.  It runs a cover-driven specific-to-general search of the kind
    used in inductive logic programming: start from the first positive, and for
    each still-uncovered positive find the minimal set of positions where the
    current pattern fails to match and variablise exactly those, sharing a
    variable between positions that carry equal subterms.  Iterate until every
    positive is covered, then apply the compression criterion and the negative
    challenge.

    A cover-driven search is not guaranteed to reach the least general
    generalization - it can variablise a position higher in the term than
    necessary - so M can diverge from the parent federation, and "the federation
    reproduces M" is measured rather than guaranteed.
    """
    pat = inst.positives[0]
    fresh = [0]  # monotonic: names must never collide with a variable already in pat

    def new_var() -> Term:
        fresh[0] += 1
        return (VAR, f"Z{fresh[0]}")

    for target in inst.positives[1:]:
        guard = 0
        while not covers(pat, target) and guard < 32:
            guard += 1
            # shallowest positions of disagreement between pat and target
            bad: list[tuple] = []

            def walk(p: Term, t: Term, pos: tuple) -> None:
                if is_var(p):
                    return
                if is_var(t) or p[0] != t[0] or len(p) != len(t):
                    bad.append(pos)
                    return
                for i in range(len(p) - 1):
                    walk(p[1 + i], t[1 + i], pos + (i,))

            walk(pat, target, ())
            if bad:
                # share one variable across positions carrying equal subterms
                groups: list[list[tuple]] = []
                for p in bad:
                    for grp in groups:
                        if at(pat, p) == at(pat, grp[0]):
                            grp.append(p)
                            break
                    else:
                        groups.append([p])
                for grp in groups:
                    v = new_var()
                    for p in grp:
                        pat = replace_at(pat, p, v)
                continue
            # Structure agrees everywhere, so the failure is a variable bound
            # to two different subterms.  Split that variable: occurrences keep
            # sharing where the target agrees and separate where it does not.
            split = False
            for v in sorted(variables(pat)):
                occ = [p for p in positions(pat) if is_var(at(pat, p)) and at(pat, p)[1] == v]
                vals = [at(target, p) for p in occ]
                if len({alpha_key(x) for x in vals}) <= 1:
                    continue
                buckets: dict[str, list[tuple]] = {}
                for p, val in zip(occ, vals):
                    buckets.setdefault(alpha_key(val), []).append(p)
                for grp in buckets.values():
                    nv = new_var()
                    for p in grp:
                        pat = replace_at(pat, p, nv)
                split = True
                break
            if not split:
                break
    # canonicalise variable names
    names: dict[str, str] = {}

    def renum(x: Term) -> Term:
        if is_var(x):
            names.setdefault(x[1], f"X{len(names)}")
            return (VAR, names[x[1]])
        if len(x) == 1:
            return x
        return (x[0],) + tuple(renum(s) for s in x[1:])

    pat = renum(pat)
    if not all(covers(pat, t) for t in inst.positives):  # pragma: no cover - safety
        pat = (VAR, "X0")
    # compression criterion, then negative challenge (registered order)
    if is_var(pat):
        return _out(pat, "REJECT_NO_COMMON_STRUCTURE", inst)
    if any(covers(pat, n) for n in inst.negatives):
        return _out(pat, "REJECT_OVER_GENERAL", inst)
    return _out(pat, "ACCEPT_LGG", inst)


def ablation_minus_variable_identity(inst: Instance) -> dict:
    """M without shared variables: a fresh variable at every disagreement.

    Keeps M's compression criterion and negative challenge, so the omission is
    isolated to variable identity.
    """
    fl = parent_fixed_lesson(inst)
    pat = fl["pattern"]
    base = inst.positives[0]
    # rebuild the concrete pattern object for the checks below
    pat_term = None
    for chain in _antichains(positions(base)):
        for part in _partitions(list(chain), lambda p, q: at(base, p) == at(base, q)):
            cand = base
            for k, block in enumerate(part):
                for p in block:
                    cand = replace_at(cand, p, (VAR, f"X{k}"))
            if alpha_key(cand) == pat:
                pat_term = cand
                break
        if pat_term is not None:
            break
    if pat_term is None or is_var(pat_term):
        return _out(pat_term, "REJECT_NO_COMMON_STRUCTURE", inst)
    if any(covers(pat_term, n) for n in inst.negatives):
        return _out(pat_term, "REJECT_OVER_GENERAL", inst)
    return _out(pat_term, "ACCEPT_LGG", inst)


def ablation_minus_negative_challenge(inst: Instance) -> dict:
    """M without the negative challenge."""
    full = mechanic_full(inst)
    if full["disposition"] == "REJECT_OVER_GENERAL":
        return {**full, "disposition": "ACCEPT_LGG"}
    return full


def ablation_minus_compression(inst: Instance) -> dict:
    """M without the vacuity/compression criterion."""
    full = mechanic_full(inst)
    if full["disposition"] == "REJECT_NO_COMMON_STRUCTURE":
        lgg = lgg_plotkin(inst.positives)
        disp = "REJECT_OVER_GENERAL" if any(covers(lgg, n) for n in inst.negatives) else "ACCEPT_LGG"
        return _out(lgg, disp, inst)
    return full


def ablation_minus_least_generality(inst: Instance) -> dict:
    """M stopping at the first covering pattern rather than the least general one."""
    pat = (VAR, "X0")
    return _out(pat, "ACCEPT_LGG", inst)


def control_always_accept(inst: Instance) -> dict:
    """Constant control: accept, with no abstraction of its own.

    It must not borrow a parent's pattern - an "always accept" arm that computes
    the true LGG for its coverage vector is the LGG parent wearing a control's
    label, and it scored 0.60 on the selftest split before this was corrected.
    """
    return _out(None, "ACCEPT_LGG", inst)


def control_always_reject(inst: Instance) -> dict:
    return _out(None, "REJECT_OVER_GENERAL", inst)


def control_random(inst: Instance) -> dict:
    rng = random.Random(inst.seed ^ 0x5EED)
    return {
        "disposition": rng.choice(DISPOSITIONS),
        "pattern": None,
        "coverage": [rng.random() < 0.5 for _ in inst.held_out],
    }


ARM_FUNCTIONS = {
    "P0_FIXED_LESSON_INJECTION": parent_fixed_lesson,
    "P1_PLOTKIN_LGG": parent_plotkin,
    "P2_CANDIDATE_ELIMINATION": parent_candidate_elimination,
    "P3_MDL_COMPRESSION": parent_mdl,
    "F0_PARENT_FEDERATION": federation,
    "M_F2_ABSTRACTION_INDUCTION_FULL": mechanic_full,
    "M_MINUS_VARIABLE_IDENTITY": ablation_minus_variable_identity,
    "M_MINUS_NEGATIVE_CHALLENGE": ablation_minus_negative_challenge,
    "M_MINUS_COMPRESSION_CRITERION": ablation_minus_compression,
    "M_MINUS_LEAST_GENERALITY": ablation_minus_least_generality,
    "C_ALWAYS_ACCEPT": control_always_accept,
    "C_ALWAYS_REJECT": control_always_reject,
    "C_RANDOM_DISPOSITION": control_random,
}


def run_arm(arm: str, inst: Instance) -> dict:
    out = ARM_FUNCTIONS[arm](inst)
    return {
        "disposition": out["disposition"],
        "pattern": out.get("pattern"),
        "coverage": list(out.get("coverage", [])),
    }


# --------------------------------------------------------------------------
# scoring key: the endpoint is the (disposition, coverage) pair
# --------------------------------------------------------------------------


def endpoint(record: dict) -> str:
    cov = "".join("1" if c else "0" for c in record.get("coverage", []))
    return f"{record['disposition']}|{cov}"


def oracle_endpoint(ans: OracleAnswer) -> str:
    return f"{ans.disposition}|" + "".join("1" if c else "0" for c in ans.coverage)


# --------------------------------------------------------------------------
# parent fidelity
# --------------------------------------------------------------------------


def T(s: str) -> Term:
    """Tiny parser for the fidelity tests: f(a,g(b)) -> nested tuples."""
    s = s.strip()
    if "(" not in s:
        return (s,) if not s.isupper() else (VAR, s)
    sym, rest = s.split("(", 1)
    assert rest.endswith(")")
    depth, cur, args = 0, "", []
    for ch in rest[:-1]:
        if ch == "," and depth == 0:
            args.append(cur)
            cur = ""
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        cur += ch
    args.append(cur)
    return (sym,) + tuple(T(a) for a in args)


def parent_fidelity() -> list[dict]:
    R: list[dict] = []

    def check(parent: str, name: str, ok: bool, detail: str = "") -> None:
        R.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    # ---- P1 Plotkin anti-unification -------------------------------------
    check(
        "P1_PLOTKIN_LGG",
        "textbook_lgg_of_two_terms",
        alpha_key(lgg_plotkin([T("f(a,b)"), T("f(a,c)")])) == alpha_key(T("f(a,V0)")),
        alpha_key(lgg_plotkin([T("f(a,b)"), T("f(a,c)")])),
    )
    check(
        "P1_PLOTKIN_LGG",
        "repeated_disagreement_shares_one_variable",
        alpha_key(lgg_plotkin([T("f(a,a)"), T("f(b,b)")])) == alpha_key(T("f(V0,V0)")),
        alpha_key(lgg_plotkin([T("f(a,a)"), T("f(b,b)")])),
    )
    check(
        "P1_PLOTKIN_LGG",
        "distinct_disagreements_take_distinct_variables",
        alpha_key(lgg_plotkin([T("f(a,b)"), T("f(c,d)")])) == alpha_key(T("f(V0,V1)")),
        alpha_key(lgg_plotkin([T("f(a,b)"), T("f(c,d)")])),
    )
    check(
        "P1_PLOTKIN_LGG",
        "different_top_symbols_give_a_bare_variable",
        is_var(lgg_plotkin([T("f(a,b)"), T("g(a)")])),
    )
    check(
        "P1_PLOTKIN_LGG",
        "identical_terms_generalize_to_themselves",
        alpha_key(lgg_plotkin([T("f(a,g(b))"), T("f(a,g(b))")])) == alpha_key(T("f(a,g(b))")),
    )
    check(
        "P1_PLOTKIN_LGG",
        "nested_structure_is_preserved",
        alpha_key(lgg_plotkin([T("f(g(a),b)"), T("f(g(c),b)")])) == alpha_key(T("f(g(V0),b)")),
        alpha_key(lgg_plotkin([T("f(g(a),b)"), T("f(g(c),b)")])),
    )
    check(
        "P1_PLOTKIN_LGG",
        "three_term_fold_is_the_common_generalization",
        alpha_key(lgg_plotkin([T("f(a,a)"), T("f(b,b)"), T("f(c,d)")])) == alpha_key(T("f(V0,V1)")),
        alpha_key(lgg_plotkin([T("f(a,a)"), T("f(b,b)"), T("f(c,d)")])),
    )
    check(
        "P1_PLOTKIN_LGG",
        "documented_boundary_always_accepts_no_negative_notion",
        parent_plotkin(
            Instance("KA", "LEAST_GENERAL_PATTERN", 0, (T("f(a,b)"), T("f(a,c)")), (T("f(a,d)"),), ())
        )["disposition"]
        == "ACCEPT_LGG",
        "scope note: anti-unification has no negative examples in its theory",
    )

    # ---- oracle agreement: Plotkin == exhaustive lattice -------------------
    for lhs, rhs in [
        ("f(a,b)", "f(a,c)"),
        ("f(a,a)", "f(b,b)"),
        ("g(f(a,b))", "g(f(c,b))"),
        ("f(g(a),a)", "f(g(b),b)"),
    ]:
        terms = [T(lhs), T(rhs)]
        ex, _, unique = lgg_exhaustive(terms)
        check(
            "ORACLE_PAIR",
            f"exhaustive_equals_plotkin_on_{lhs}_vs_{rhs}",
            alpha_key(ex) == alpha_key(lgg_plotkin(terms)) and unique,
            f"{alpha_key(ex)} vs {alpha_key(lgg_plotkin(terms))}",
        )

    # ---- P2 candidate elimination ----------------------------------------
    inst_ok = Instance("KA", "LEAST_GENERAL_PATTERN", 0, (T("f(a,b)"), T("f(a,c)")), (T("g(a)"),), ())
    inst_bad = Instance("KA", "OVER_GENERALIZATION", 0, (T("f(a,b)"), T("f(a,c)")), (T("f(a,d)"),), ())
    check(
        "P2_CANDIDATE_ELIMINATION",
        "accepts_when_no_negative_is_covered",
        parent_candidate_elimination(inst_ok)["disposition"] == "ACCEPT_LGG",
    )
    check(
        "P2_CANDIDATE_ELIMINATION",
        "rejects_when_the_specific_boundary_covers_a_negative",
        parent_candidate_elimination(inst_bad)["disposition"] == "REJECT_OVER_GENERAL",
    )
    vac = Instance("KA", "NO_VALID_COMMON_ABSTRACTION", 0, (T("f(a,b)"), T("g(a)")), (), ())
    check(
        "P2_CANDIDATE_ELIMINATION",
        "documented_boundary_accepts_a_vacuous_bare_variable",
        parent_candidate_elimination(vac)["disposition"] == "ACCEPT_LGG",
        "scope note: version spaces have no compression criterion",
    )

    # ---- P3 MDL ----------------------------------------------------------
    check(
        "P3_MDL_COMPRESSION",
        "prefers_a_pattern_that_compresses_the_examples",
        parent_mdl(inst_ok)["pattern"] is not None,
    )
    check(
        "P3_MDL_COMPRESSION",
        "reports_vacuity_when_nothing_is_shared",
        parent_mdl(vac)["disposition"] == "REJECT_NO_COMMON_STRUCTURE",
    )
    check(
        "P3_MDL_COMPRESSION",
        "documented_boundary_has_no_negative_test",
        parent_mdl(inst_bad)["disposition"] == "ACCEPT_LGG",
        "scope note: MDL selects by description length, not by consistency",
    )

    # ---- P0 fixed lesson --------------------------------------------------
    fl = parent_fixed_lesson(
        Instance("KA", "LEAST_GENERAL_PATTERN", 0, (T("f(a,a)"), T("f(b,b)")), (), ())
    )
    check(
        "P0_FIXED_LESSON_INJECTION",
        "over_generalises_repeated_structure_with_fresh_variables",
        fl["pattern"] == alpha_key(T("f(V0,V1)")),
        str(fl["pattern"]),
    )
    check(
        "P0_FIXED_LESSON_INJECTION",
        "keeps_the_shared_skeleton",
        parent_fixed_lesson(
            Instance("KA", "LEAST_GENERAL_PATTERN", 0, (T("f(a,b)"), T("f(a,c)")), (), ())
        )["pattern"]
        == alpha_key(T("f(a,V0)")),
    )

    # ---- matcher ---------------------------------------------------------
    check("MATCHER", "variable_matches_any_ground_term", covers(T("X"), T("f(a,b)")))
    check("MATCHER", "repeated_variable_requires_equal_arguments", not covers(T("f(X,X)"), T("f(a,b)")))
    check("MATCHER", "repeated_variable_accepts_equal_arguments", covers(T("f(X,X)"), T("f(a,a)")))
    check("MATCHER", "constants_must_match_exactly", not covers(T("f(a,X)"), T("f(b,c)")))
    return R


# --------------------------------------------------------------------------
# hand-authored known-answer fixtures
# --------------------------------------------------------------------------


def known_answer_fixtures() -> list[dict]:
    F: list[dict] = []

    def add(name, family, pos, neg, held, expected):
        F.append(
            {
                "name": name,
                "instance": Instance(
                    name,
                    family,
                    0,
                    tuple(T(x) for x in pos),
                    tuple(T(x) for x in neg),
                    tuple(T(x) for x in held),
                ),
                "expected": expected,
            }
        )

    add("KA-01-SIMPLE_LGG", "LEAST_GENERAL_PATTERN", ["f(a,b)", "f(a,c)"], ["g(a)"], ["f(a,d)"], "ACCEPT_LGG")
    add("KA-02-SHARED_VARIABLE", "LEAST_GENERAL_PATTERN", ["f(a,a)", "f(b,b)"], ["f(a,b)"], ["f(c,c)"], "ACCEPT_LGG")
    add("KA-03-OVER_GENERAL", "OVER_GENERALIZATION", ["f(a,b)", "f(a,c)"], ["f(a,d)"], ["f(a,d)"], "REJECT_OVER_GENERAL")
    add("KA-04-VACUOUS", "NO_VALID_COMMON_ABSTRACTION", ["f(a,b)", "g(a)"], [], ["h(a,b)"], "REJECT_NO_COMMON_STRUCTURE")
    add(
        "KA-05-VACUITY_DOMINATES_OVER_GENERALITY",
        "NO_VALID_COMMON_ABSTRACTION",
        ["f(a,b)", "g(a)"],
        ["h(c,d)"],
        ["h(a,b)"],
        "REJECT_NO_COMMON_STRUCTURE",
    )
    add("KA-06-NESTED", "LEAST_GENERAL_PATTERN", ["f(g(a),b)", "f(g(c),b)"], ["f(a,b)"], ["f(g(d),b)", "f(g(a),c)"], "ACCEPT_LGG")
    add("KA-07-THREE_POSITIVES", "LEAST_GENERAL_PATTERN", ["f(a,a)", "f(b,b)", "f(c,c)"], ["f(a,b)"], ["f(d,d)", "f(a,b)"], "ACCEPT_LGG")
    add("KA-08-IDENTICAL_POSITIVES", "LEAST_GENERAL_PATTERN", ["f(a,g(b))", "f(a,g(b))"], ["f(a,g(c))"], ["f(a,g(b))"], "ACCEPT_LGG")
    add("KA-09-DEEP_SHARED_SKELETON", "DISTRACTOR_REGULARITY", ["h(f(a,b),c)", "h(f(a,d),c)"], ["h(f(e,b),c)"], ["h(f(a,e),c)"], "ACCEPT_LGG")
    add("KA-10-NEGATIVE_OUTSIDE_PATTERN", "LEAST_GENERAL_PATTERN", ["g(a)", "g(b)"], ["f(a,b)"], ["g(c)", "f(a,a)"], "ACCEPT_LGG")
    return F


# --------------------------------------------------------------------------
# planted positives
# --------------------------------------------------------------------------


def planted_positives() -> list[PlantedPositive]:
    from fm_core import discrimination_gate

    P = [
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "position_wise_variablisation_pseudo_oracle_is_detected",
            "the fixed-lesson generalizer (fresh variable per disagreement, no "
            "sharing) must disagree with the exhaustive lattice minimum on a "
            "term with repeated structure",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "wrong_expected_label_is_detected",
            "a deliberately wrong expected disposition must fail the comparison",
        ),
        PlantedPositive(
            "G2_ANTI_PERMISSIVENESS",
            "over_accepting_arm_is_detected",
            "C_ALWAYS_ACCEPT must be counted as over-accepting on an instance "
            "the oracle rejects",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_ceiling_split_is_detected",
            "a synthetic per-arm table where every arm scores 1.0 must FAIL the "
            "discrimination gate",
        ),
        PlantedPositive(
            "G3_MECHANISM_BY_OMISSION",
            "compression_ablation_loses_the_vacuity_family",
            "M_MINUS_COMPRESSION_CRITERION must be wrong on a vacuous instance "
            "where M is right",
        ),
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "lattice_minimum_uniqueness_is_actually_verified",
            "the exhaustive enumeration reports a unique minimum on a term where "
            "one exists, so the uniqueness field is computed rather than assumed",
        ),
    ]

    rep = [T("f(a,a)"), T("f(b,b)")]
    fl = parent_fixed_lesson(Instance("PP", "LEAST_GENERAL_PATTERN", 0, tuple(rep), (), ()))
    ex, _, unique = lgg_exhaustive(rep)
    P[0].fired = fl["pattern"] != alpha_key(ex)

    fx = known_answer_fixtures()[0]
    P[1].fired = oracle_exhaustive(fx["instance"]).disposition != "REJECT_OVER_GENERAL"

    rej = known_answer_fixtures()[2]["instance"]
    P[2].fired = control_always_accept(rej)["disposition"] == "ACCEPT_LGG" and (
        oracle_exhaustive(rej).disposition != "ACCEPT_LGG"
    )

    P[3].fired = (
        discrimination_gate(
            {a: 1.0 for a in ARM_FUNCTIONS}, weak_arms=("C_RANDOM_DISPOSITION",),
            max_weak=0.60, min_strong=0.95,
        ).verdict
        == "FAIL"
    )

    vac = known_answer_fixtures()[3]["instance"]
    P[4].fired = (
        mechanic_full(vac)["disposition"] == "REJECT_NO_COMMON_STRUCTURE"
        and ablation_minus_compression(vac)["disposition"] != "REJECT_NO_COMMON_STRUCTURE"
    )

    P[5].fired = bool(unique)
    return P


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------

SPEC = SuiteSpec(
    suite_id="FM20",
    title="Anti-unification and generalization with negatives, vacuity and held-out coverage",
    families=FAMILIES,
    arms=(
        ArmSpec("P0_FIXED_LESSON_INJECTION", "PARENT", "frozen position-wise variablisation table"),
        ArmSpec("P1_PLOTKIN_LGG", "PARENT", "Plotkin 1970 / Reynolds 1970 anti-unification"),
        ArmSpec("P2_CANDIDATE_ELIMINATION", "PARENT", "Mitchell 1982 version spaces, specific boundary"),
        ArmSpec("P3_MDL_COMPRESSION", "PARENT", "minimum description length selection"),
        ArmSpec("F0_PARENT_FEDERATION", "FEDERATION", "pre-registered outcome-blind composition"),
        ArmSpec("M_F2_ABSTRACTION_INDUCTION_FULL", "MECHANIC", "ORION cover-driven abstraction induction"),
        ArmSpec("M_MINUS_VARIABLE_IDENTITY", "ABLATION", ""),
        ArmSpec("M_MINUS_NEGATIVE_CHALLENGE", "ABLATION", ""),
        ArmSpec("M_MINUS_COMPRESSION_CRITERION", "ABLATION", ""),
        ArmSpec("M_MINUS_LEAST_GENERALITY", "ABLATION", ""),
        ArmSpec("C_ALWAYS_ACCEPT", "CONTROL", ""),
        ArmSpec("C_ALWAYS_REJECT", "CONTROL", ""),
        ArmSpec("C_RANDOM_DISPOSITION", "CONTROL", ""),
    ),
    mechanic_arm="M_F2_ABSTRACTION_INDUCTION_FULL",
    strongest_parent_arm="F0_PARENT_FEDERATION",
    federation_arm="F0_PARENT_FEDERATION",
    weak_arms=("P0_FIXED_LESSON_INJECTION", "P1_PLOTKIN_LGG", "P3_MDL_COMPRESSION", "M_MINUS_LEAST_GENERALITY"),
    constant_arms=("C_ALWAYS_ACCEPT", "C_ALWAYS_REJECT"),
    random_arm="C_RANDOM_DISPOSITION",
    ablation_for_family={
        "OVER_GENERALIZATION": "M_MINUS_NEGATIVE_CHALLENGE",
        "NO_VALID_COMMON_ABSTRACTION": "M_MINUS_COMPRESSION_CRITERION",
        "DISTRACTOR_REGULARITY": "M_MINUS_VARIABLE_IDENTITY",
        "UNDER_GENERALIZATION": "M_MINUS_LEAST_GENERALITY",
    },
    default_ablation="M_MINUS_LEAST_GENERALITY",
    decoy_families=("DISTRACTOR_REGULARITY", "OVER_GENERALIZATION", "UNDER_GENERALIZATION", "NO_VALID_COMMON_ABSTRACTION"),
    min_tasks=120,
    dev_per_family=3,
    protected_per_family=25,  # 5 x 25 = 125 >= 120
    design_json="FM20_ANTI_UNIFICATION_EXACT_STUDY_DESIGN_V1.json",
    oracle_agreement_fields=("disposition", "lgg", "coverage"),
    endpoint_key=lambda rec: endpoint(rec),
    oracle_endpoint_key=lambda e: f"{e['disposition']}|" + "".join("1" if c else "0" for c in e["coverage"]),
    generate=generate_split,
    oracle=oracle_exhaustive,
    cross_check=oracle_plotkin,
    run_arm=run_arm,
    parent_fidelity=parent_fidelity,
    known_answer_fixtures=known_answer_fixtures,
    planted_positives=planted_positives,
)
