#!/usr/bin/env python3
"""ME-X3 object formal system: finite equational logic over a unary signature.

A **term** is a word `w = (a_1, ..., a_k)` over a finite alphabet of unary
operator symbols, read as `a_1(a_2(... a_k(x) ...))` applied to a schema
variable `x`. A **statement** is a schematic equation `lhs =?= rhs` meaning
`forall x. lhs(x) = rhs(x)`.

A **presentation** is a finite set of equational axioms `u = v` (word pairs).
Because every operator is unary, Birkhoff derivation in this theory is exactly
two-sided factor rewriting: `p u s -> p v s` for any prefix `p` and suffix `s`
(the prefix is congruence, the suffix is instantiation of the schema variable).
So a derivation is a finite rewrite chain, and proof validity is decidable by
breadth-first search under a registered word-length / expansion cap.

A **model** of a presentation is a finite set `[0..n)` together with a function
`f_a : [n] -> [n]` for each symbol `a`, such that every axiom holds as an
equality of the composed functions. By soundness, a model in which a statement
fails certifies that the statement is *not* derivable; the model class up to
`max_model_size` is enumerated exhaustively.

Everything the study needs is therefore exactly computable:

* proof validity  -> BFS in the rewrite graph (a derivation is a witness);
* refutation      -> exhaustive finite-model enumeration (a model is a witness);
* specification fidelity -> a bidirectional derivation between the intended and
  the presented statement (FAITHFUL) or a model of the axioms that separates
  them (drift), both constructed as explicit witnesses.

No external prover is required for any of this. The separate Lean 4 receipt
(`mex3_lean.py`) re-checks the positive derivations as genuine proof terms over
an inductive `Derives` relation, and requires the invalid ones to be rejected
by the Lean kernel with a registered error signature.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Iterable, Optional, Sequence

Word = tuple[int, ...]

# ---------------------------------------------------------------- families ---

FAMILIES = (
    "F1_DIRECT_SEARCH",
    "F2_MISSING_LEMMA",
    "F3_REPRESENTATION_CHANGE",
    "F4_DECEPTIVE_CHANGE",
    "F5_PROBE_OR_COUNTEREXAMPLE_NEEDED",
    "F6_UNDERDETERMINED_OR_CANNOT_CHECK",
    "F7_SPECIFICATION_MISMATCH",
    "F8_TRANSFER",
)

# Registered intervention vocabulary (protocol V1 section 8), frozen order.
ACTIONS = (
    "CONTINUE_DIRECT_PROOF_SEARCH",
    "RETRIEVE_EXISTING_LEMMA",
    "INVENT_LOCAL_LEMMA",
    "GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL",
    "CHANGE_REPRESENTATION",
    "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK",
    "REQUEST_SPECIFICATION_CLARIFICATION",
    "DEFER_CANNOT_IDENTIFY",
)

# Registered specification-fidelity verdicts (protocol V1 section 10).
FIDELITY_VERDICTS = (
    "FAITHFUL",
    "MATERIALLY_WEAKENED",
    "MATERIALLY_STRENGTHENED",
    "NOTATIONAL_COLLAPSE",
    "ABSTRACTION_ELEVATION",
    "DEGENERATE_TRIVIALIZATION",
    "OTHER_SEMANTIC_DRIFT",
    "CANNOT_CHECK_INTENT",
)
DRIFT_VERDICTS = tuple(v for v in FIDELITY_VERDICTS if v not in ("FAITHFUL", "CANNOT_CHECK_INTENT"))

# Registered joint terminals (protocol V1 section 11 of ME_X3_FORMAL_MATHEMATICS_PROTOCOL_V1).
TERMINALS = (
    "FORMALLY_VERIFIED_AND_INTENT_ALIGNED",
    "FORMALLY_VERIFIED_BUT_INTENT_MISMATCH",
    "REFUTED_WITH_COUNTERMODEL",
    "UNVERIFIED_CANDIDATE",
    "CANNOT_CHECK_INTENT",
    "UNSOLVED_WITHIN_BUDGET",
)

VALIDITY_VERDICTS = ("VERIFIED", "REFUTED", "UNVERIFIED", "DEFERRED")


# ------------------------------------------------------------- structures ----

@dataclass(frozen=True)
class Presentation:
    """A finite equational presentation over `alphabet` unary symbols."""

    pid: str
    alphabet: int
    axioms: tuple[tuple[Word, Word], ...]

    def as_dict(self) -> dict:
        return {"pid": self.pid, "alphabet": self.alphabet,
                "axioms": [[list(u), list(v)] for u, v in self.axioms]}


@dataclass(frozen=True)
class Statement:
    lhs: Word
    rhs: Word

    def as_dict(self) -> dict:
        return {"lhs": list(self.lhs), "rhs": list(self.rhs)}

    def trivial(self) -> bool:
        return self.lhs == self.rhs


@dataclass(frozen=True)
class Budget:
    """Registered per-task resource caps. Identical for every arm."""

    max_word_len: int
    max_expansions: int        # total BFS node expansions across ALL module calls
    solve_expansions: int      # cap on any ONE solving search (the level test)
    max_model_size: int
    max_model_checks: int
    max_lemma_candidates: int

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Task:
    """One protected problem instance. `hidden` is never exposed to an arm."""

    task_id: str
    family: str
    seed: str
    base: Presentation
    alt: Optional[Presentation]           # offered alternative presentation, or None
    alt_label: str                        # surface label for the offered alternative
    alt_map: tuple[Word, ...]             # translation of base symbols into alt words
    library: tuple[tuple[Word, Word], ...]  # retrievable pre-derived lemmas
    intent: Statement                     # the intended mathematical question
    intent_invariants: tuple[str, ...]    # mandatory semantic obligations (visible)
    formal: Statement                     # the statement actually presented for proof
    formal_pid: str                       # which presentation `formal` is written in
    surface_cues: tuple[str, ...]         # deceptive/attractive surface hints (visible)
    budget: Budget
    alt_defining_word: Word = ()          # the alternative's defining word d (g := d)
    transfer_of: Optional[str] = None     # task_id of the F8 source, if this is a target
    hidden: dict = field(default_factory=dict, repr=False, compare=False)

    # ---- the exact view every arm receives (no family, no oracle labels) ----
    def view(self) -> dict:
        return {
            "task_id": self.task_id,
            "base": self.base.as_dict(),
            "alt": self.alt.as_dict() if self.alt else None,
            "alt_label": self.alt_label,
            "alt_map": [list(w) for w in self.alt_map],
            # The offered alternative presentation comes with its defining word:
            # it is part of the offer (the label already states it), not oracle
            # information, and every arm and the witness checker read it here so
            # that neither has to re-derive it from a sorted axiom list.
            "alt_defining_word": list(self.alt_defining_word),
            "library": [[list(u), list(v)] for u, v in self.library],
            "intent": self.intent.as_dict(),
            "intent_invariants": list(self.intent_invariants),
            "formal": self.formal.as_dict(),
            "formal_pid": self.formal_pid,
            "surface_cues": list(self.surface_cues),
            "budget": self.budget.as_dict(),
            "transfer_of": self.transfer_of,
        }


@dataclass(frozen=True)
class Answer:
    """What an arm returns for one task."""

    action: str                   # first high-level decision (registered vocabulary)
    validity: str                 # VERIFIED / REFUTED / UNVERIFIED / DEFERRED
    fidelity: str                 # registered fidelity verdict
    terminal: str                 # registered joint terminal
    derivation: tuple[Word, ...] = ()      # rewrite chain witness, if VERIFIED
    derivation_pid: str = ""               # presentation the chain is written in
    countermodel: Optional[dict] = None    # separating model witness, if REFUTED
    invented_lemma: Optional[tuple[Word, Word]] = None
    used_representation: str = ""
    cost: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "action": self.action, "validity": self.validity, "fidelity": self.fidelity,
            "terminal": self.terminal,
            "derivation": [list(w) for w in self.derivation],
            "derivation_pid": self.derivation_pid,
            "countermodel": self.countermodel,
            "invented_lemma": None if self.invented_lemma is None
            else [list(self.invented_lemma[0]), list(self.invented_lemma[1])],
            "used_representation": self.used_representation,
            "cost": self.cost,
        }


# ------------------------------------------------------------- primitives ----

def word_str(w: Word) -> str:
    return "e" if not w else "".join(chr(ord("a") + s) for s in w)


def apply_rule_positions(w: Word, u: Word, v: Word, max_len: int) -> list[Word]:
    """All results of replacing one occurrence of factor `u` in `w` by `v`."""
    out: list[Word] = []
    lu = len(u)
    if lu > len(w):
        return out
    for i in range(len(w) - lu + 1):
        if w[i:i + lu] == u:
            nw = w[:i] + v + w[i + lu:]
            if len(nw) <= max_len:
                out.append(nw)
    return out


def neighbours(w: Word, axioms: Sequence[tuple[Word, Word]], max_len: int) -> list[Word]:
    """One-step two-sided rewrites of `w` (equational logic is symmetric)."""
    seen: list[Word] = []
    got: set[Word] = set()
    for u, v in axioms:
        for nw in apply_rule_positions(w, u, v, max_len):
            if nw not in got:
                got.add(nw); seen.append(nw)
        if u != v:
            for nw in apply_rule_positions(w, v, u, max_len):
                if nw not in got:
                    got.add(nw); seen.append(nw)
    return seen


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def task_to_json(t: Task) -> dict:
    d = t.view()
    d.update({"family": t.family, "seed": t.seed, "hidden": t.hidden})
    return d


def all_words(alphabet: int, max_len: int) -> Iterable[Word]:
    frontier: list[Word] = [()]
    yield ()
    for _ in range(max_len):
        nxt = []
        for w in frontier:
            for s in range(alphabet):
                nw = w + (s,)
                nxt.append(nw); yield nw
        frontier = nxt
