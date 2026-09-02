#!/usr/bin/env python3
"""ME-X3 exact minimum-escalation oracle.

The oracle answer for a task is not a generator intention; it is computed by
**exhaustive search over the registered finite intervention space** and carries
a witness at every level:

    L0  refutation           a finite model of the axioms falsifying the statement
    L1  direct search        a rewrite chain inside the task budget
    L2  library retrieval    a library lemma that puts the target inside budget
    L3  lemma invention      a lemma from the registered candidate pool that is
                             itself derivable at oracle caps and puts the target
                             inside budget
    L4  representation change the offered alternative presentation puts the
                             translated target inside budget, and the alternative
                             presents the same theory (finite Tietze check)
    L5  defer                no level in the registered space succeeds

`minimal action` is the first level that succeeds, so it is minimal *by
construction over the registered space* rather than by assertion.  The
specification-fidelity verdict is computed independently and overrides the
action when the presented statement does not encode the intended question.
"""
from __future__ import annotations

from typing import Optional

from mex3_model import Presentation, Statement, Task, Word
from mex3_oracle import (
    bfs_derivation, fidelity, find_countermodel, truth,
)

LEMMA_POOL_MAX_LEN = 3
LEMMA_POOL_CAP = 12


def _reach(pres: Presentation, start: Word, max_len: int, cap: int) -> dict[Word, int]:
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


def registered_lemma_pool(pres: Presentation, stmt: Statement, oracle_word_len: int,
                          oracle_expansions: int) -> list[tuple[Word, Word]]:
    """Frozen, deterministic candidate space for L3 (no randomness, no oracle labels)."""
    ends: dict[Word, int] = {}
    for side in (stmt.lhs, stmt.rhs):
        for w, d in _reach(pres, side, oracle_word_len, oracle_expansions).items():
            if len(w) <= LEMMA_POOL_MAX_LEN:
                ends[w] = min(ends.get(w, 10 ** 9), d)
    keys = sorted(ends, key=lambda w: (len(w), w))
    out: list[tuple[Word, Word]] = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if len(a) + len(b) <= 6:
                out.append((a, b))
            if len(out) >= LEMMA_POOL_CAP:
                return out
    return out


def _solves(pres: Presentation, stmt: Statement, budget) -> bool:
    return bfs_derivation(stmt.lhs, stmt.rhs, pres.axioms, budget.max_word_len,
                          budget.solve_expansions).found


def oracle_verdict(task: Task, oracle_word_len: int, oracle_expansions: int,
                   oracle_model_size: int) -> dict:
    """Exact (truth, fidelity, minimal action, terminal) with witnesses."""
    from mex3_arms import _adjudication, terminal_of
    from mex3_generator import translate

    b = task.budget
    base, formal = task.base, task.formal
    pres_used = task.alt if (task.formal_pid == "P1" and task.alt) else base

    # ---- specification fidelity (independent of proof validity) -------------
    apres, aintent, aformal = _adjudication(task)
    fid, fw = fidelity(apres, aintent, aformal, oracle_word_len, oracle_expansions,
                       oracle_model_size, task.hidden.get("f7_subtype")
                       if task.hidden.get("f7_subtype") in
                       ("MATERIALLY_WEAKENED", "MATERIALLY_STRENGTHENED",
                        "NOTATIONAL_COLLAPSE", "ABSTRACTION_ELEVATION",
                        "DEGENERATE_TRIVIALIZATION") else None)

    # ---- proof validity ----------------------------------------------------
    tval, tw = truth(pres_used, formal, oracle_word_len, oracle_expansions, oracle_model_size)

    # ---- minimum escalation over the registered intervention space ---------
    level = None; witness: dict = {}
    if tval == "REFUTABLE":
        level = ("L0_REFUTE", "GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL"); witness = tw
    elif _solves(pres_used, formal, b):
        level = ("L1_DIRECT", "CONTINUE_DIRECT_PROOF_SEARCH")
        witness = {"length": bfs_derivation(formal.lhs, formal.rhs, pres_used.axioms,
                                            b.max_word_len, b.solve_expansions).length}
    else:
        for lem in task.library:
            aug = Presentation("P0+lib", pres_used.alphabet,
                               tuple(sorted(set(pres_used.axioms + (lem,)))))
            if _solves(aug, formal, b):
                level = ("L2_RETRIEVE", "RETRIEVE_EXISTING_LEMMA")
                witness = {"lemma": [list(lem[0]), list(lem[1])]}
                break
    if level is None:
        for a, bb in registered_lemma_pool(pres_used, formal, oracle_word_len, oracle_expansions):
            if not bfs_derivation(a, bb, pres_used.axioms, oracle_word_len, oracle_expansions).found:
                continue
            aug = Presentation("P0+L", pres_used.alphabet,
                               tuple(sorted(set(pres_used.axioms + ((a, bb),)))))
            if _solves(aug, formal, b):
                level = ("L3_INVENT", "INVENT_LOCAL_LEMMA")
                witness = {"lemma": [list(a), list(bb)]}
                break
    if level is None and task.alt is not None and task.formal_pid == "P0":
        from mex3_generator import theories_agree
        d = task.alt_defining_word
        if d and theories_agree(base, task.alt, oracle_model_size):
            g = base.alphabet
            st_alt = Statement(translate(formal.lhs, d, g), translate(formal.rhs, d, g))
            if _solves(task.alt, st_alt, b):
                level = ("L4_REPRESENTATION", "CHANGE_REPRESENTATION")
                witness = {"alt_statement": st_alt.as_dict()}
    if level is None:
        level = ("L5_DEFER", "DEFER_CANNOT_IDENTIFY")
        witness = tw

    action = level[1]
    if fid == "CANNOT_CHECK_INTENT":
        action = "REQUEST_SPECIFICATION_CLARIFICATION"
    elif fid != "FAITHFUL":
        action = "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK"

    validity = {"PROVABLE": "VERIFIED", "REFUTABLE": "REFUTED",
                "UNDETERMINED": "DEFERRED"}[tval]
    if tval == "PROVABLE" and not _solves(pres_used, formal, b) and level[0] not in (
            "L2_RETRIEVE", "L3_INVENT", "L4_REPRESENTATION"):
        validity = "DEFERRED"
    return {"truth": tval, "validity": validity, "fidelity": fid,
            "fidelity_witness": fw, "level": level[0], "minimal_action": action,
            "escalation_witness": witness, "truth_witness": tw,
            "terminal": terminal_of(validity, fid)}
