#!/usr/bin/env python3
"""ME-X3 arms: parent baselines, the strongest faithful federation, and M.

Every arm is built from the **same** module toolkit and runs under the **same**
per-task resource ledger.  No arm sees the family label, the oracle action, the
oracle truth value or any oracle witness.  The only thing that varies between
arms is (a) which modules the controller calls, (b) in what order, and (c) what
the modules are allowed to *report back* — the H-EXT-3 interface ladder, which
is a property of the federation's internal channel and never of `M`'s
privilege.  `B5` sits at the top rung and receives everything `M` receives.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from mex3_model import (
    ACTIONS, Answer, Budget, Presentation, Statement, Task, Word,
)
from mex3_oracle import (
    bfs_derivation, check_derivation, find_countermodel, holds, models_of,
)

RUNGS = ("R1_VERDICT_ONLY", "R2_SATURATION", "R3_FRONTIER", "R4_SEMANTIC", "R5_FULL_STRUCTURE")


class Ledger:
    """Shared per-task resource account. Identical caps for every arm."""

    __slots__ = ("budget", "expansions", "model_checks", "module_calls", "lemma_tries")

    def __init__(self, budget: Budget):
        self.budget = budget
        self.expansions = 0
        self.model_checks = 0
        self.module_calls = 0
        self.lemma_tries = 0

    @property
    def left(self) -> int:
        return max(0, self.budget.max_expansions - self.expansions)

    def exhausted(self) -> bool:
        return self.left <= 0

    def as_dict(self) -> dict:
        return {"expansions": self.expansions, "model_checks": self.model_checks,
                "module_calls": self.module_calls, "lemma_tries": self.lemma_tries}


# ------------------------------------------------------------ module reports ---

@dataclass
class SearchReport:
    ok: bool
    path: tuple[Word, ...]
    saturated: bool          # R2+: reachable set closed (certified unreachable at cap)
    hit_cap: bool            # R2+: budget ran out (certifies nothing)
    frontier: int            # R3+: number of expansions actually made
    reached: int             # R3+: size of the reachable set explored

    def project(self, rung: str) -> "SearchReport":
        if rung == "R1_VERDICT_ONLY":
            return SearchReport(self.ok, self.path, False, False, 0, 0)
        if rung == "R2_SATURATION":
            return SearchReport(self.ok, self.path, self.saturated, self.hit_cap, 0, 0)
        return self


@dataclass
class SemanticReport:
    countermodel: Optional[dict]
    separating: Optional[dict]      # separating model for intent vs formal
    interderivable: bool
    checked: bool

    def project(self, rung: str) -> "SemanticReport":
        if rung in ("R1_VERDICT_ONLY", "R2_SATURATION", "R3_FRONTIER"):
            return SemanticReport(None, None, self.interderivable, self.checked)
        return self


# ------------------------------------------------------------------ modules ---

def m_search(led: Ledger, pres: Presentation, stmt: Statement, slice_: Optional[int] = None
             ) -> SearchReport:
    led.module_calls += 1
    cap = min(led.left, slice_ if slice_ is not None else led.left)
    if cap <= 0:
        return SearchReport(False, (), False, True, 0, 0)
    r = bfs_derivation(stmt.lhs, stmt.rhs, pres.axioms, led.budget.max_word_len, cap)
    led.expansions += r.expansions
    return SearchReport(r.found, r.path, r.saturated, r.hit_cap, r.expansions, r.expansions)


def m_countermodel(led: Ledger, pres: Presentation, stmt: Statement) -> Optional[dict]:
    led.module_calls += 1
    if led.model_checks >= led.budget.max_model_checks:
        return None
    led.model_checks += len(models_of(pres, led.budget.max_model_size))
    cm = find_countermodel(pres, stmt, led.budget.max_model_size)
    if cm is None:
        return None
    m, n = cm
    return {"model": [list(f) for f in m], "size": n}


def m_separating(led: Ledger, pres: Presentation, a: Statement, b: Statement) -> Optional[dict]:
    led.module_calls += 1
    led.model_checks += len(models_of(pres, led.budget.max_model_size))
    for m, n in models_of(pres, led.budget.max_model_size):
        ha, hb = holds(m, n, a), holds(m, n, b)
        if ha != hb:
            return {"model": [list(f) for f in m], "size": n,
                    "intent_holds": ha, "formal_holds": hb}
    return None


def m_interderivable(led: Ledger, pres: Presentation, a: Statement, b: Statement,
                     slice_: int) -> bool:
    for x, y in ((b.lhs, b.rhs), (b.rhs, b.lhs)):
        r1 = m_search(led, pres, Statement(a.lhs, x), slice_)
        r2 = m_search(led, pres, Statement(a.rhs, y), slice_)
        if r1.ok and r2.ok:
            return True
    return (a.lhs, a.rhs) == (b.lhs, b.rhs)


def m_spec_check(led: Ledger, task: Task, rung: str) -> tuple[str, SemanticReport]:
    """Bounded specification-fidelity check. Runs at *task* caps, not oracle caps,
    so it can honestly return CANNOT_CHECK_INTENT."""
    pres, intent, formal = _adjudication(task)
    slice_ = max(30, led.budget.solve_expansions // 3)
    inter = m_interderivable(led, pres, intent, formal, slice_)
    if inter:
        return "FAITHFUL", SemanticReport(None, None, True, True)
    sep = m_separating(led, pres, intent, formal)
    rep = SemanticReport(None, sep, False, True).project(rung)
    if sep is None:
        return "CANNOT_CHECK_INTENT", rep
    return _classify_drift(task, intent, formal, sep), rep


def _adjudication(task: Task) -> tuple[Presentation, Statement, Statement]:
    """Fidelity is adjudicated in the presentation the formal statement is written
    in; when that is the alternative presentation, the intent is translated."""
    if task.formal_pid == "P1" and task.alt is not None:
        it = task.hidden.get("intent_translated") if task.hidden else None
        if it:
            return task.alt, Statement(tuple(it["lhs"]), tuple(it["rhs"])), task.formal
        return task.alt, task.intent, task.formal
    return task.base, task.intent, task.formal


def _classify_drift(task: Task, intent: Statement, formal: Statement, sep: dict) -> str:
    """Name the drift from *syntax the arm can see* plus the separating model."""
    if formal.lhs == formal.rhs:
        return "DEGENERATE_TRIVIALIZATION"
    isyms = set(intent.lhs) | set(intent.rhs)
    fsyms = set(formal.lhs) | set(formal.rhs)
    if fsyms - isyms and task.formal_pid == "P1":
        return "ABSTRACTION_ELEVATION"
    if len(fsyms) < len(isyms) and fsyms < isyms:
        return "NOTATIONAL_COLLAPSE"
    li, lf = len(intent.lhs) + len(intent.rhs), len(formal.lhs) + len(formal.rhs)
    if lf > li and formal.lhs[-len(intent.lhs):] == intent.lhs:
        return "MATERIALLY_WEAKENED"
    if lf < li and intent.lhs[-len(formal.lhs):] == formal.lhs:
        return "MATERIALLY_STRENGTHENED"
    if sep.get("formal_holds") and not sep.get("intent_holds"):
        return "MATERIALLY_WEAKENED"
    if sep.get("intent_holds") and not sep.get("formal_holds"):
        return "MATERIALLY_STRENGTHENED"
    return "OTHER_SEMANTIC_DRIFT"


def m_retrieve(led: Ledger, task: Task, stmt: Statement, slice_: int
               ) -> Optional[tuple[tuple[Word, Word], SearchReport]]:
    for lem in task.library:
        led.lemma_tries += 1
        if led.exhausted() or led.lemma_tries > led.budget.max_lemma_candidates:
            return None
        base = working_pres(task)
        aug = Presentation("P0+lib", base.alphabet, tuple(sorted(set(base.axioms + (lem,)))))
        r = m_search(led, aug, stmt, slice_)
        if r.ok:
            return lem, r
    return None


def m_invent(led: Ledger, task: Task, stmt: Statement, slice_: int
             ) -> Optional[tuple[tuple[Word, Word], SearchReport]]:
    """Propose an intermediate lemma from the registered candidate space.

    The candidate space is the same frozen, deterministic function the oracle's
    L3 level uses (`registered_lemma_pool`), evaluated here under *task* caps
    rather than oracle caps: the arm therefore searches the same space the oracle
    searches, and loses only where its own budget runs out first.  A proposed
    lemma counts only if the arm also derives it.
    """
    from mex3_verdict import registered_lemma_pool
    pres = working_pres(task)
    b = led.budget
    pool = registered_lemma_pool(pres, stmt, b.max_word_len, b.solve_expansions)
    for a, bb in pool:
        led.lemma_tries += 1
        if led.exhausted() or led.lemma_tries > b.max_lemma_candidates:
            return None
        chk = m_search(led, pres, Statement(a, bb), max(40, slice_ // 3))
        if not chk.ok:
            continue
        aug = Presentation(pres.pid + "+L", pres.alphabet,
                           tuple(sorted(set(pres.axioms + ((a, bb),)))))
        r = m_search(led, aug, stmt, slice_)
        if r.ok:
            return (a, bb), r
    return None


def m_alt_statement(task: Task) -> Optional[Statement]:
    """The presented statement written in the offered alternative presentation."""
    if task.alt is None or not task.alt_defining_word:
        return None
    from mex3_generator import translate
    d, g = task.alt_defining_word, task.base.alphabet
    return Statement(translate(task.formal.lhs, d, g), translate(task.formal.rhs, d, g))


def m_preservation_ok(task: Task) -> bool:
    """Does the offered alternative present the *same* theory? (Tietze check.)"""
    from mex3_generator import theories_agree
    if task.alt is None:
        return False
    return theories_agree(task.base, task.alt, 3)


# ---------------------------------------------------------------- terminals ---

def terminal_of(validity: str, fidelity: str) -> str:
    if fidelity == "CANNOT_CHECK_INTENT":
        return "CANNOT_CHECK_INTENT"
    if validity == "VERIFIED":
        return ("FORMALLY_VERIFIED_AND_INTENT_ALIGNED" if fidelity == "FAITHFUL"
                else "FORMALLY_VERIFIED_BUT_INTENT_MISMATCH")
    if validity == "REFUTED":
        return "REFUTED_WITH_COUNTERMODEL"
    if validity == "DEFERRED":
        return "UNSOLVED_WITHIN_BUDGET"
    return "UNVERIFIED_CANDIDATE"


# ================================ arm controllers ==============================

class ArmState:
    """Carried across an F8 source -> held-out target pair (and nothing else)."""

    def __init__(self, keep_transfer: bool = True):
        self.keep_transfer = keep_transfer
        self.lemmas: list[tuple[Word, Word]] = []
        self.representations: list[str] = []

    def remember(self, lemma, repr_label):
        if not self.keep_transfer:
            return
        if lemma and lemma not in self.lemmas:
            self.lemmas.append(lemma)
        if repr_label and repr_label not in self.representations:
            self.representations.append(repr_label)


def working_pres(task: Task) -> Presentation:
    """The presentation the presented statement is actually written in.

    Available to every arm: it is read off `formal_pid`, which is part of the
    task view, and is not oracle information.
    """
    return task.alt if (task.formal_pid == "P1" and task.alt is not None) else task.base


def _augment(pres: Presentation, lem) -> Presentation:
    return Presentation(pres.pid + "+L", pres.alphabet,
                        tuple(sorted(set(pres.axioms + (lem,)))))


def _try_carried(led: Ledger, task: Task, state: ArmState, slice_: int):
    """Reuse an artefact the arm itself invented on the F8 source, if it applies."""
    for lem in state.lemmas:
        if led.exhausted():
            break
        r = m_search(led, _augment(working_pres(task), lem), task.formal, slice_)
        if r.ok:
            return lem, r
    return None


def act_under_fidelity(action: str, fidelity: str) -> str:
    """A proof of the wrong statement is not the right next move.

    When the specification check reports drift, the high-level decision is to
    repair the formalization, whatever the proof search returned; when the intent
    cannot be adjudicated at all, it is to ask.  Both `B5` and `M` apply this,
    because both run the check -- the rule is part of the shared contract, not an
    `M` privilege.
    """
    if fidelity == "CANNOT_CHECK_INTENT":
        return "REQUEST_SPECIFICATION_CLARIFICATION"
    if fidelity != "FAITHFUL":
        return "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK"
    return action


def _answer(action, validity, fidelity, led, *, path=(), pid="P0", cm=None,
            lemma=None, repr_="") -> Answer:
    action = act_under_fidelity(action, fidelity)
    return Answer(action=action, validity=validity, fidelity=fidelity,
                  terminal=terminal_of(validity, fidelity), derivation=tuple(path),
                  derivation_pid=pid, countermodel=cm, invented_lemma=lemma,
                  used_representation=repr_, cost=led.as_dict())


# ---- A0..A4: individual parents -------------------------------------------------

def arm_a0(task: Task, led: Ledger, state: ArmState) -> Answer:
    """Base model + proof search. No metacognitive scaffold, no intent check."""
    r = m_search(led, working_pres(task), task.formal)
    if r.ok:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", "FAITHFUL", led, path=r.path)
    return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "UNVERIFIED", "FAITHFUL", led)


def arm_a1(task: Task, led: Ledger, state: ArmState) -> Answer:
    """A0 + library retrieval."""
    sl = led.budget.solve_expansions
    r = m_search(led, working_pres(task), task.formal, sl)
    if r.ok:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", "FAITHFUL", led, path=r.path)
    got = m_retrieve(led, task, task.formal, sl)
    if got:
        lem, rr = got
        return _answer("RETRIEVE_EXISTING_LEMMA", "VERIFIED", "FAITHFUL", led,
                       path=rr.path, lemma=lem)
    return _answer("RETRIEVE_EXISTING_LEMMA", "UNVERIFIED", "FAITHFUL", led)


def arm_a2(task: Task, led: Ledger, state: ArmState) -> Answer:
    """A1 + generic self-reflection/retry: re-runs the same search under the same
    total budget, which buys nothing but spends the account (the honest parent)."""
    sl = max(40, led.budget.solve_expansions // 3)
    for _ in range(3):
        r = m_search(led, working_pres(task), task.formal, sl)
        if r.ok:
            return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", "FAITHFUL", led,
                           path=r.path)
        if led.exhausted():
            break
    got = m_retrieve(led, task, task.formal, sl)
    if got:
        lem, rr = got
        return _answer("RETRIEVE_EXISTING_LEMMA", "VERIFIED", "FAITHFUL", led,
                       path=rr.path, lemma=lem)
    return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "UNVERIFIED", "FAITHFUL", led)


def arm_a3(task: Task, led: Ledger, state: ArmState) -> Answer:
    """Discover-and-Prove parent: settle the answer semantically first, then prove."""
    cm = m_countermodel(led, working_pres(task), task.formal)
    if cm is not None:
        return _answer("GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL", "REFUTED", "FAITHFUL",
                       led, cm=cm)
    sl = led.budget.solve_expansions
    r = m_search(led, working_pres(task), task.formal, sl)
    if r.ok:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", "FAITHFUL", led, path=r.path)
    got = m_retrieve(led, task, task.formal, sl)
    if got:
        lem, rr = got
        return _answer("RETRIEVE_EXISTING_LEMMA", "VERIFIED", "FAITHFUL", led,
                       path=rr.path, lemma=lem)
    return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "UNVERIFIED", "FAITHFUL", led)


def arm_a4(task: Task, led: Ledger, state: ArmState) -> Answer:
    """Lemma/abstraction discovery parent: retrieve, then invent, then reuse."""
    sl = led.budget.solve_expansions
    r = m_search(led, working_pres(task), task.formal, sl)
    if r.ok:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", "FAITHFUL", led, path=r.path)
    car = _try_carried(led, task, state, sl)
    if car:
        lem, rr = car
        return _answer("INVENT_LOCAL_LEMMA", "VERIFIED", "FAITHFUL", led,
                       path=rr.path, lemma=lem)
    got = m_retrieve(led, task, task.formal, sl)
    if got:
        lem, rr = got
        return _answer("RETRIEVE_EXISTING_LEMMA", "VERIFIED", "FAITHFUL", led,
                       path=rr.path, lemma=lem)
    inv = m_invent(led, task, task.formal, sl)
    if inv:
        lem, rr = inv
        state.remember(lem, "")
        return _answer("INVENT_LOCAL_LEMMA", "VERIFIED", "FAITHFUL", led,
                       path=rr.path, lemma=lem)
    return _answer("INVENT_LOCAL_LEMMA", "UNVERIFIED", "FAITHFUL", led)


# ---- B5: strongest faithful parent federation, at an interface rung -------------

def federation(task: Task, led: Ledger, state: ArmState, rung: str,
               *, spec: bool = True) -> Answer:
    """Composition of every parent above with ordinary engineering glue.

    Stage order and budget slices were fixed on the DEVELOPMENT split and are
    frozen.  `rung` restricts only what the modules may report back to the glue
    (H-EXT-3): it is a property of the federation's internal channel, and the top
    rung `R5_FULL_STRUCTURE` receives exactly what `M` receives.
    """
    B = led.budget.solve_expansions
    fid = "FAITHFUL"; sem = SemanticReport(None, None, False, False)
    if spec:
        fid, sem = m_spec_check(led, task, rung)
    pres = working_pres(task)

    # discovery (DAP): is the statement even true?
    cm = m_countermodel(led, pres, task.formal)
    if cm is not None:
        witness = cm if rung in ("R4_SEMANTIC", "R5_FULL_STRUCTURE") else None
        return _answer("GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL", "REFUTED", fid, led, cm=witness)

    sl = B
    r = m_search(led, pres, task.formal, sl)
    if r.ok:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", fid, led,
                       path=r.path, pid=pres.pid)
    # at R1 the glue cannot tell a closed reachable set from an exhausted budget,
    # so it must keep cascading; from R2 up it can stop searching and escalate.
    if rung == "R1_VERDICT_ONLY":
        r = m_search(led, pres, task.formal, sl)
        if r.ok:
            return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", fid, led,
                           path=r.path, pid=pres.pid)

    car = _try_carried(led, task, state, sl)
    if car:
        lem, rr = car
        return _answer("INVENT_LOCAL_LEMMA", "VERIFIED", fid, led,
                       path=rr.path, lemma=lem, pid=pres.pid)
    got = m_retrieve(led, task, task.formal, sl)
    if got:
        lem, rr = got
        return _answer("RETRIEVE_EXISTING_LEMMA", "VERIFIED", fid, led,
                       path=rr.path, lemma=lem, pid=pres.pid)
    inv = m_invent(led, task, task.formal, sl)
    if inv:
        lem, rr = inv
        state.remember(lem, "")
        return _answer("INVENT_LOCAL_LEMMA", "VERIFIED", fid, led,
                       path=rr.path, lemma=lem, pid=pres.pid)

    if task.alt is not None and task.formal_pid == "P0":
        alt_stmt = m_alt_statement(task)
        if alt_stmt is not None and m_preservation_ok(task):
            ra = m_search(led, task.alt, alt_stmt, B)
            if ra.ok:
                state.remember(None, task.alt_label)
                return _answer("CHANGE_REPRESENTATION", "VERIFIED", fid, led,
                               path=ra.path, pid="P1", repr_=task.alt_label)
    if fid != "FAITHFUL":
        act = ("REQUEST_SPECIFICATION_CLARIFICATION" if fid == "CANNOT_CHECK_INTENT"
               else "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK")
        return _answer(act, "DEFERRED", fid, led)
    return _answer("DEFER_CANNOT_IDENTIFY", "DEFERRED", fid, led)


# ---- M: obstruction diagnosis + minimum responsible escalation ------------------

OBSTRUCTIONS = ("NO_ESCALATION_NEEDED", "SPECIFICATION_MISMATCH", "STATEMENT_FALSE",
                "SEARCH_INSUFFICIENT", "MISSING_LEMMA", "REPRESENTATION_INSUFFICIENT",
                "CANNOT_IDENTIFY")


def m_arm(task: Task, led: Ledger, state: ArmState, *,
          diagnose: bool = True, lower_first: bool = True, cue_driven: bool = False,
          spec: bool = True, preservation: bool = True, unresolved: bool = True,
          shuffle_labels: bool = False, always_change: bool = False,
          never_change: bool = False, extra_search: bool = False) -> Answer:
    """The Machine-Epistemics controller and every registered ablation of it.

    It calls the same modules as `federation` at `R5_FULL_STRUCTURE` and receives
    no information the top-rung federation does not receive.  Its only delta is
    control: a witnessed obstruction hypothesis, a lower-level disposition, a
    minimum-sufficient escalation, a preservation obligation attached to any
    representation change, and an unresolved terminal.
    """
    B = led.budget.solve_expansions
    rung = "R5_FULL_STRUCTURE"
    fid = "FAITHFUL"
    if spec:
        fid, _sem = m_spec_check(led, task, rung)
    pres = working_pres(task)

    if cue_driven and task.surface_cues and task.alt is not None:
        alt_stmt = m_alt_statement(task)
        if alt_stmt is not None:
            ra = m_search(led, task.alt, alt_stmt, B)
            if ra.ok:
                return _answer("CHANGE_REPRESENTATION", "VERIFIED", fid, led,
                               path=ra.path, pid="P1", repr_=task.alt_label)

    # ---- witnessed obstruction probe (a small, registered slice) -------------
    probe = m_search(led, pres, task.formal, max(40, B // 3))
    if probe.ok:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", fid, led,
                       path=probe.path, pid=pres.pid)
    obstruction = "CANNOT_IDENTIFY"
    cm = m_countermodel(led, pres, task.formal)
    if cm is not None:
        # the statement is false: settle validity with the witness. The action is
        # still governed by the fidelity verdict (see `act_under_fidelity`).
        return _answer("GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL", "REFUTED", fid, led, cm=cm)
    if diagnose:
        if fid != "FAITHFUL":
            obstruction = "SPECIFICATION_MISMATCH"
        elif probe.saturated:
            obstruction = "REPRESENTATION_INSUFFICIENT"
        else:
            obstruction = "MISSING_LEMMA"
    if shuffle_labels:
        i = (OBSTRUCTIONS.index(obstruction) + 3) % len(OBSTRUCTIONS)
        obstruction = OBSTRUCTIONS[i]

    sl = B

    def try_lemma():
        car = _try_carried(led, task, state, sl)
        if car:
            lem, rr = car
            return _answer("INVENT_LOCAL_LEMMA", "VERIFIED", fid, led,
                           path=rr.path, lemma=lem, pid=pres.pid)
        got = m_retrieve(led, task, task.formal, sl)
        if got:
            lem, rr = got
            return _answer("RETRIEVE_EXISTING_LEMMA", "VERIFIED", fid, led,
                           path=rr.path, lemma=lem, pid=pres.pid)
        inv = m_invent(led, task, task.formal, sl)
        if inv:
            lem, rr = inv
            state.remember(lem, "")
            return _answer("INVENT_LOCAL_LEMMA", "VERIFIED", fid, led,
                           path=rr.path, lemma=lem, pid=pres.pid)
        return None

    def try_repr():
        if never_change or task.alt is None or task.formal_pid != "P0":
            return None
        if preservation and not m_preservation_ok(task):
            return None                       # preservation obligation unmet
        alt_stmt = m_alt_statement(task)
        if alt_stmt is None:
            return None
        ra = m_search(led, task.alt, alt_stmt, B)
        if ra.ok:
            state.remember(None, task.alt_label)
            return _answer("CHANGE_REPRESENTATION", "VERIFIED", fid, led,
                           path=ra.path, pid="P1", repr_=task.alt_label)
        return None

    def try_more_search():
        r = m_search(led, pres, task.formal, led.left)
        if r.ok:
            return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "VERIFIED", fid, led,
                           path=r.path, pid=pres.pid)
        return None

    if extra_search:
        order = [try_more_search, try_lemma, try_repr]
    elif always_change:
        order = [try_repr, try_lemma, try_more_search]
    elif not lower_first:
        order = [try_repr, try_lemma, try_more_search]
    elif obstruction == "REPRESENTATION_INSUFFICIENT":
        order = [try_lemma, try_repr, try_more_search]     # minimum sufficient first
    elif obstruction == "MISSING_LEMMA":
        order = [try_lemma, try_more_search, try_repr]
    elif obstruction == "SPECIFICATION_MISMATCH":
        order = [try_lemma, try_repr]
    else:
        order = [try_more_search, try_lemma, try_repr]

    for step in order:
        if led.exhausted():
            break
        got = step()
        if got is not None:
            return got

    if fid == "CANNOT_CHECK_INTENT":
        return _answer("REQUEST_SPECIFICATION_CLARIFICATION", "DEFERRED", fid, led)
    if fid != "FAITHFUL":
        return _answer("REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK",
                       "DEFERRED", fid, led)
    if not unresolved:
        return _answer("CONTINUE_DIRECT_PROOF_SEARCH", "UNVERIFIED", fid, led)
    return _answer("DEFER_CANNOT_IDENTIFY", "DEFERRED", fid, led)


# ------------------------------------------------------------------ registry ---

@dataclass
class ArmSpec:
    name: str
    fn: Callable
    keep_transfer: bool = True


M_ARM = "M_ME_OBSTRUCTION_MINIMUM_ESCALATION"
B5_ARM = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
LADDER = ["B5_R1_VERDICT_ONLY", "B5_R2_SATURATION", "B5_R3_FRONTIER",
          "B5_R4_SEMANTIC", B5_ARM]


def arm_specs() -> list[ArmSpec]:
    def fed(rung, spec=True):
        return lambda t, l, s: federation(t, l, s, rung, spec=spec)

    def m(**kw):
        return lambda t, l, s: m_arm(t, l, s, **kw)

    return [
        ArmSpec("A0_DIRECT", arm_a0),
        ArmSpec("A1_RETRIEVAL", arm_a1),
        ArmSpec("A2_SELF_REFLECT", arm_a2),
        ArmSpec("A3_DISCOVER_AND_PROVE_PARENT", arm_a3),
        ArmSpec("A4_LEMMA_ABSTRACTION_PARENT", arm_a4),
        ArmSpec("B5_R1_VERDICT_ONLY", fed("R1_VERDICT_ONLY")),
        ArmSpec("B5_R2_SATURATION", fed("R2_SATURATION")),
        ArmSpec("B5_R3_FRONTIER", fed("R3_FRONTIER")),
        ArmSpec("B5_R4_SEMANTIC", fed("R4_SEMANTIC")),
        ArmSpec(B5_ARM, fed("R5_FULL_STRUCTURE")),
        ArmSpec(M_ARM, m()),
        ArmSpec("M_MINUS_OBSTRUCTION_CLASS", m(diagnose=False)),
        ArmSpec("M_MINUS_LOWER_LEVEL_DISPOSITION", m(lower_first=False)),
        ArmSpec("M_MINUS_FALSE_CHANGE_PENALTY", m(cue_driven=True)),
        ArmSpec("M_MINUS_SPECIFICATION_PRESERVATION", m(spec=False)),
        ArmSpec("M_MINUS_PRESERVATION_CONTRACT", m(preservation=False)),
        ArmSpec("M_MINUS_UNRESOLVED_TERMINAL", m(unresolved=False)),
        ArmSpec("M_MINUS_TRANSFER_REUSE_TRACKING", m(), keep_transfer=False),
        ArmSpec("M_LOCUS_LABELS_SHUFFLED", m(shuffle_labels=True)),
        ArmSpec("M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK", m(always_change=True)),
        ArmSpec("M_NEVER_CHANGE_REPRESENTATION", m(never_change=True)),
        ArmSpec("M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM", m(extra_search=True)),
    ]
