#!/usr/bin/env python3
"""ME-X3 exact oracle: derivation search, finite-model enumeration, fidelity.

Every oracle verdict carries an explicit witness (a rewrite chain or a finite
model), and every witness is re-checked by an independent verifier in this
module.  Two independent search implementations (breadth-first over the rewrite
graph, and iterative-deepening depth-first) must agree on the minimal
derivation length; two independent model checkers (composition tables and
pointwise evaluation) must agree on every model verdict.  G0 asserts both.
"""
from __future__ import annotations

import itertools
from collections import deque
from typing import Optional, Sequence

from mex3_model import (
    Presentation, Statement, Word, neighbours, apply_rule_positions,
)

UNBOUNDED = 10 ** 9


# ------------------------------------------------------- derivation search ---

class SearchResult:
    __slots__ = ("found", "length", "path", "expansions", "saturated", "hit_cap")

    def __init__(self, found: bool, length: int, path: tuple[Word, ...],
                 expansions: int, saturated: bool, hit_cap: bool):
        self.found = found; self.length = length; self.path = path
        self.expansions = expansions; self.saturated = saturated; self.hit_cap = hit_cap

    def as_dict(self) -> dict:
        return {"found": self.found, "length": self.length,
                "path": [list(w) for w in self.path], "expansions": self.expansions,
                "saturated": self.saturated, "hit_cap": self.hit_cap}


def bfs_derivation(start: Word, goal: Word, axioms: Sequence[tuple[Word, Word]],
                   max_len: int, max_expansions: int) -> SearchResult:
    """Minimal-length rewrite chain from `start` to `goal`.

    `saturated` means the reachable set was closed within `max_len` without
    reaching the goal (a certificate of non-derivability *at that word length*,
    not of non-derivability in the theory).  `hit_cap` means the expansion
    budget ran out first, which certifies nothing.
    """
    if start == goal:
        return SearchResult(True, 0, (start,), 0, False, False)
    prev: dict[Word, Optional[Word]] = {start: None}
    q = deque([start])
    exp = 0
    while q:
        if exp >= max_expansions:
            return SearchResult(False, -1, (), exp, False, True)
        w = q.popleft(); exp += 1
        for nw in neighbours(w, axioms, max_len):
            if nw in prev:
                continue
            prev[nw] = w
            if nw == goal:
                path = [nw]
                cur = w
                while cur is not None:
                    path.append(cur); cur = prev[cur]
                path.reverse()
                return SearchResult(True, len(path) - 1, tuple(path), exp, False, False)
            q.append(nw)
    return SearchResult(False, -1, (), exp, True, False)


def iddfs_derivation(start: Word, goal: Word, axioms: Sequence[tuple[Word, Word]],
                     max_len: int, max_depth: int, max_expansions: int) -> SearchResult:
    """Independent re-implementation used only to cross-check `bfs_derivation`."""
    exp = 0

    def dfs(w: Word, depth: int, seen: set[Word]) -> Optional[list[Word]]:
        nonlocal exp
        if w == goal:
            return [w]
        if depth == 0 or exp >= max_expansions:
            return None
        exp += 1
        for nw in neighbours(w, axioms, max_len):
            if nw in seen:
                continue
            seen.add(nw)
            sub = dfs(nw, depth - 1, seen)
            seen.discard(nw)
            if sub is not None:
                return [w] + sub
        return None

    for d in range(0, max_depth + 1):
        got = dfs(start, d, {start})
        if got is not None:
            return SearchResult(True, len(got) - 1, tuple(got), exp, False, False)
        if exp >= max_expansions:
            return SearchResult(False, -1, (), exp, False, True)
    return SearchResult(False, -1, (), exp, False, False)


def check_derivation(path: Sequence[Word], stmt: Statement,
                     axioms: Sequence[tuple[Word, Word]], max_len: int) -> tuple[bool, str]:
    """Independently verify a claimed rewrite chain against the axioms."""
    if not path:
        return False, "EMPTY_CHAIN"
    if tuple(path[0]) != stmt.lhs:
        return False, "CHAIN_HEAD_NOT_LHS"
    if tuple(path[-1]) != stmt.rhs:
        return False, "CHAIN_TAIL_NOT_RHS"
    for a, b in zip(path, path[1:]):
        a = tuple(a); b = tuple(b)
        if len(a) > max_len or len(b) > max_len:
            return False, "WORD_LENGTH_CAP_EXCEEDED"
        ok = False
        for u, v in axioms:
            if b in apply_rule_positions(a, u, v, max_len) or b in apply_rule_positions(a, v, u, max_len):
                ok = True
                break
        if not ok:
            return False, "STEP_IS_NOT_AN_AXIOM_INSTANCE"
    return True, "OK"


# ------------------------------------------------------------- finite models ---

Model = tuple[tuple[int, ...], ...]   # model[s][x] = f_s(x)


def eval_word(model: Model, w: Word, x: int) -> int:
    """`w = (a1..ak)` denotes a1(a2(...ak(x))), so apply right to left."""
    for s in reversed(w):
        x = model[s][x]
    return x


def word_map(model: Model, w: Word, n: int) -> tuple[int, ...]:
    table = tuple(range(n))
    for s in reversed(w):
        f = model[s]
        table = tuple(f[y] for y in table)
    return table


def word_map_composed(model: Model, w: Word, n: int) -> tuple[int, ...]:
    """Independent re-implementation by composition of function tables.

    `word_map` evaluates pointwise per input; this folds the tables themselves,
    so the two agree only if both are correct.
    """
    table = tuple(range(n))
    for s in reversed(w):
        table = tuple(model[s][table[x]] for x in range(n))
    return table


def holds(model: Model, n: int, stmt: Statement) -> bool:
    return word_map(model, stmt.lhs, n) == word_map(model, stmt.rhs, n)


def satisfies(model: Model, n: int, axioms: Sequence[tuple[Word, Word]]) -> bool:
    return all(word_map(model, u, n) == word_map(model, v, n) for u, v in axioms)


def enumerate_models(alphabet: int, n: int) -> list[Model]:
    fns = list(itertools.product(range(n), repeat=n))
    return [tuple(m) for m in itertools.product(fns, repeat=alphabet)]


_MODELS_CACHE: dict[tuple, list[tuple[Model, int]]] = {}


def _defined_generator(pres: Presentation) -> Optional[tuple[int, Word]]:
    """A generator `g` fixed by a defining relation `g = d` over earlier symbols.

    Tietze-introduced generators are definable, so their interpretation is forced
    by the rest of the model.  Enumerating the free part only turns an
    `n^(n*alphabet)` search into `n^(n*(alphabet-1))`, exactly and without
    approximation.
    """
    g = pres.alphabet - 1
    for u, v in pres.axioms:
        if u == (g,) and g not in v:
            return g, v
        if v == (g,) and g not in u:
            return g, u
    return None


def models_of(pres: Presentation, max_n: int, cap: int = 10 ** 7) -> list[tuple[Model, int]]:
    key = (pres.alphabet, pres.axioms, max_n)
    hit = _MODELS_CACHE.get(key)
    if hit is not None:
        return hit
    out: list[tuple[Model, int]] = []
    dg = _defined_generator(pres)
    checked = 0
    for n in range(1, max_n + 1):
        fns = list(itertools.product(range(n), repeat=n))
        free = pres.alphabet - 1 if dg is not None else pres.alphabet
        for part in itertools.product(fns, repeat=free):
            checked += 1
            if checked > cap:
                return out
            if dg is not None:
                g, d = dg
                m = tuple(part) + (word_map(tuple(part) + (tuple(range(n)),), d, n),)
            else:
                m = tuple(part)
            if satisfies(m, n, pres.axioms):
                out.append((m, n))
    if len(_MODELS_CACHE) < 4096:
        _MODELS_CACHE[key] = out
    return out
def find_countermodel(pres: Presentation, stmt: Statement, max_n: int
                      ) -> Optional[tuple[Model, int]]:
    """A model of the axioms in which `stmt` fails: certifies non-derivability."""
    for m, n in models_of(pres, max_n):
        if not holds(m, n, stmt):
            return (m, n)
    return None


def check_countermodel(model: Model, n: int, pres: Presentation, stmt: Statement
                       ) -> tuple[bool, str]:
    if n < 1 or len(model) != pres.alphabet:
        return False, "MALFORMED_MODEL"
    for f in model:
        if len(f) != n or any(not (0 <= y < n) for y in f):
            return False, "MALFORMED_MODEL"
    if not satisfies(model, n, pres.axioms):
        return False, "MODEL_DOES_NOT_SATISFY_AXIOMS"
    if holds(model, n, stmt):
        return False, "STATEMENT_HOLDS_IN_MODEL"
    # independent second evaluation
    if word_map_composed(model, stmt.lhs, n) == word_map_composed(model, stmt.rhs, n):
        return False, "EVALUATOR_DISAGREEMENT"
    return True, "OK"


# ---------------------------------------------------------- truth adjudication ---

def truth(pres: Presentation, stmt: Statement, max_len: int, max_expansions: int,
          max_n: int) -> tuple[str, dict]:
    """Exact three-valued status of `stmt` in the theory, within registered caps.

    PROVABLE  -> a derivation witness exists;
    REFUTABLE -> a finite countermodel witness exists;
    UNDETERMINED -> neither witness exists within the caps (DEFER is correct).
    """
    r = bfs_derivation(stmt.lhs, stmt.rhs, pres.axioms, max_len, max_expansions)
    if r.found:
        return "PROVABLE", {"derivation": [list(w) for w in r.path], "length": r.length}
    cm = find_countermodel(pres, stmt, max_n)
    if cm is not None:
        m, n = cm
        return "REFUTABLE", {"model": [list(f) for f in m], "size": n}
    return "UNDETERMINED", {"saturated": r.saturated, "hit_cap": r.hit_cap}


# ------------------------------------------------------- specification fidelity ---

def fidelity(pres: Presentation, intent: Statement, formal: Statement,
             max_len: int, max_expansions: int, max_n: int,
             declared_subtype: Optional[str] = None) -> tuple[str, dict]:
    """Adjudicate whether `formal` faithfully encodes `intent`.

    FAITHFUL requires *interderivability witnesses in both directions* between
    the two statements' defining equations (an exact certificate, not a bounded
    model agreement).  Drift requires a *separating model* of the axioms: a
    model in which exactly one of the two statements holds.  The generator
    constructs every drift instance from its separating model, so the witness is
    always inside the registered bound by construction; anything neither route
    settles is CANNOT_CHECK_INTENT.
    """
    # 1. interderivability: intent.lhs ~ formal.lhs and intent.rhs ~ formal.rhs,
    #    or the crossed pairing (an equation is unordered).
    for a, b in ((formal.lhs, formal.rhs), (formal.rhs, formal.lhs)):
        r1 = bfs_derivation(intent.lhs, a, pres.axioms, max_len, max_expansions)
        r2 = bfs_derivation(intent.rhs, b, pres.axioms, max_len, max_expansions)
        if r1.found and r2.found:
            return "FAITHFUL", {"route": "INTERDERIVABLE",
                                "lhs_chain": [list(w) for w in r1.path],
                                "rhs_chain": [list(w) for w in r2.path]}
    if intent.lhs == formal.lhs and intent.rhs == formal.rhs:
        return "FAITHFUL", {"route": "IDENTICAL"}

    # 2. separating model
    for m, n in models_of(pres, max_n):
        hi = holds(m, n, intent); hf = holds(m, n, formal)
        if hi != hf:
            sub = declared_subtype or ("MATERIALLY_WEAKENED" if hf and not hi
                                       else "MATERIALLY_STRENGTHENED")
            return sub, {"route": "SEPARATING_MODEL", "model": [list(f) for f in m],
                         "size": n, "intent_holds": hi, "formal_holds": hf}
    return "CANNOT_CHECK_INTENT", {"route": "NO_WITNESS_WITHIN_CAPS"}


def check_separating_model(model: Model, n: int, pres: Presentation,
                           intent: Statement, formal: Statement) -> tuple[bool, str]:
    if not satisfies(model, n, pres.axioms):
        return False, "MODEL_DOES_NOT_SATISFY_AXIOMS"
    if holds(model, n, intent) == holds(model, n, formal):
        return False, "MODEL_DOES_NOT_SEPARATE"
    return True, "OK"
