#!/usr/bin/env python3
"""FM60 — obstruction and counterexample discovery: exact generator, oracles, parents.

The registered task is a **bounded conjecture**: given a finite set of
hypotheses `H` and a conclusion `C = c_1 and ... and c_k` over a registered
first-order signature (one binary relation `R`, one unary predicate `P`, no
constants), decide the conjecture's disposition over the bounded model space of
all structures with domain size <= 3 — and **exhibit the witness that decides
it**:

    TRANSFER_VALID                          no countermodel exists in the
    (gloss: ACCEPT_WITH_PROOF_WITNESS)      bounded space AND the arm supplies a
                                            derivation of every conjunct from H
                                            in the registered rule base;
    REJECT_WITH_COUNTEREXAMPLE              exactly one conjunct fails and its
                                            countermodel is no deeper than the
                                            shallowest model of H; the arm must
                                            exhibit a countermodel;
    REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED  exactly one conjunct fails and every
                                            countermodel is strictly deeper than
                                            the shallowest model of H; the arm
                                            must exhibit one of minimum size;
    MULTIPLE_INDEPENDENT_OBSTRUCTIONS       two or more conjuncts fail, and no
                                            failing conjunct's countermodel set
                                            contains another's; the arm must
                                            exhibit a countermodel for at least
                                            two of them;
    UNDECIDED_BUDGET_EXHAUSTED              honest abstention (never an oracle
                                            label; not an acceptance);
    CLAIM_WITHOUT_VALID_WITNESS             the arm's claim failed witness
                                            validation (never an oracle label).

**Why the accept label is spelled `TRANSFER_VALID`.**  The shared runner's
over-acceptance / under-acceptance counters and the `G2_ANTI_PERMISSIVENESS`
gate key on that literal string.  Spelling FM60's acceptance anything else would
have made `G2` print a full denominator over a predicate that could never fire —
the exact defect `fm_core` exists to prevent, in mirror form.  The registered
gloss is `ACCEPT_WITH_PROOF_WITNESS`; the string is chosen so a hard gate stays
live.

**Witness validity is part of the endpoint, not a side report.**  The protocol's
hard gate `formal_claim_without_witness_allowed: false` is enforced in
`run_arm`: a non-control arm whose witness fails the registered validator has
its disposition rewritten to `CLAIM_WITHOUT_VALID_WITNESS`, which is never an
oracle label and is therefore always scored wrong.  Control arms are
**registered as exempt** — a control exists to exercise a counter, and exempting
them is what keeps `G2`'s over-acceptance predicate capable of firing.

Oracle validity rests on two independent algorithms agreeing on
(disposition, failing conjuncts, minimal countermodel size, shallowest
hypothesis model size):

  * `oracle_exhaustive`   — materialise the whole bounded model space once and
    compute each formula's truth column as a bitset; dispositions are then set
    algebra over those columns;
  * `oracle_stratified_dpll` — never materialises the space: a size-ascending
    depth-first search over the cells of a partial model, pruned by three-valued
    (Kleene) evaluation of the hypotheses, which yields the minimal countermodel
    by construction.

They share only the grounded-circuit representation of a formula, exactly as
FM10's two oracle algorithms shared only the per-fact status primitive.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from typing import Any, Iterator, Sequence

from fm_core import ArmSpec, PlantedPositive, SuiteSpec

# --------------------------------------------------------------------------
# registered constants (every numeric constant of the study lives here)
# --------------------------------------------------------------------------

DOMAIN_BOUND = 3  # registered finite-model bound N
SIZES: tuple[int, ...] = tuple(range(1, DOMAIN_BOUND + 1))
MAX_HYPOTHESIS_MODELS = 400  # generator: H must be restrictive enough to search
MIN_HYPOTHESIS_MODELS = 4
INDUCTIVE_SAMPLE_SIZE = 12  # models of H presented with the conjecture
MISLEADING_MIN_CONFIRMING_RATIO = 0.88
MISLEADING_MAX_COUNTERMODELS = 6
SMALL_SCOPE_BOUND = 2  # P4's registered scope
PROOF_STEP_BUDGET = 12  # M: max rule applications in its bounded proof attempt
M_SEED_TARGET = 8  # M: entry points sought per size before local-repair exploration
M_PROBE_BUDGET = 6000  # M: model probes per size (seeding plus local repair)
M_EXHAUSTIVE_SIZE_CUTOFF = 2  # M is exhaustive at sizes <= this, heuristic above

FAMILIES = (
    "no_obstruction",
    "single_hidden_obstruction",
    "multiple_obstruction",
    "minimal_counterexample",
    "misleading_surface_support",
)

DISPOSITIONS = (
    "TRANSFER_VALID",
    "REJECT_WITH_COUNTEREXAMPLE",
    "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED",
    "MULTIPLE_INDEPENDENT_OBSTRUCTIONS",
    "UNDECIDED_BUDGET_EXHAUSTED",
    "CLAIM_WITHOUT_VALID_WITNESS",
)

DISPOSITION_GLOSS = {
    "TRANSFER_VALID": "ACCEPT_WITH_PROOF_WITNESS",
    "REJECT_WITH_COUNTEREXAMPLE": "REJECT_WITH_COUNTEREXAMPLE",
    "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED": "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED",
    "MULTIPLE_INDEPENDENT_OBSTRUCTIONS": "MULTIPLE_INDEPENDENT_OBSTRUCTIONS",
    "UNDECIDED_BUDGET_EXHAUSTED": "UNDECIDED_BUDGET_EXHAUSTED",
    "CLAIM_WITHOUT_VALID_WITNESS": "CLAIM_WITHOUT_VALID_WITNESS",
}

# --------------------------------------------------------------------------
# formula syntax (one AST per registered formula; the single source of truth)
# --------------------------------------------------------------------------


def R(x: str, y: str) -> tuple:
    return ("R", x, y)


def Pp(x: str) -> tuple:
    return ("P", x)


def EQ(x: str, y: str) -> tuple:
    return ("EQ", x, y)


def NOT(f: tuple) -> tuple:
    return ("NOT", f)


def AND(*fs: tuple) -> tuple:
    return ("AND", tuple(fs))


def OR(*fs: tuple) -> tuple:
    return ("OR", tuple(fs))


def IMP(a: tuple, b: tuple) -> tuple:
    return OR(NOT(a), b)


def ALL(v: str, f: tuple) -> tuple:
    return ("ALL", v, f)


def EX(v: str, f: tuple) -> tuple:
    return ("EX", v, f)


FORMULAS: dict[str, tuple[str, tuple]] = {
    "REFLEXIVE": ("every element is R-related to itself", ALL("x", R("x", "x"))),
    "IRREFLEXIVE": ("no element is R-related to itself", ALL("x", NOT(R("x", "x")))),
    "SYMMETRIC": (
        "R is symmetric",
        ALL("x", ALL("y", IMP(R("x", "y"), R("y", "x")))),
    ),
    "ANTISYMMETRIC": (
        "R is antisymmetric",
        ALL("x", ALL("y", IMP(AND(R("x", "y"), R("y", "x")), EQ("x", "y")))),
    ),
    "ASYMMETRIC": (
        "R is asymmetric",
        ALL("x", ALL("y", NOT(AND(R("x", "y"), R("y", "x"))))),
    ),
    "TRANSITIVE": (
        "R is transitive",
        ALL("x", ALL("y", ALL("z", IMP(AND(R("x", "y"), R("y", "z")), R("x", "z"))))),
    ),
    "CONNEX": (
        "R relates every ordered pair in one direction or the other",
        ALL("x", ALL("y", OR(R("x", "y"), R("y", "x")))),
    ),
    "SERIAL": ("every element has an R-successor", ALL("x", EX("y", R("x", "y")))),
    "FUNCTIONAL": (
        "R has at most one successor per element",
        ALL("x", ALL("y", ALL("z", IMP(AND(R("x", "y"), R("x", "z")), EQ("y", "z"))))),
    ),
    "INJECTIVE_R": (
        "R has at most one predecessor per element",
        ALL("x", ALL("y", ALL("z", IMP(AND(R("x", "z"), R("y", "z")), EQ("x", "y"))))),
    ),
    "EUCLIDEAN": (
        "R is Euclidean",
        ALL("x", ALL("y", ALL("z", IMP(AND(R("x", "y"), R("x", "z")), R("y", "z"))))),
    ),
    "DENSE": (
        "every R-edge factors through an intermediate element",
        ALL(
            "x",
            ALL("y", IMP(R("x", "y"), EX("z", AND(R("x", "z"), R("z", "y"))))),
        ),
    ),
    "EMPTY_R": ("R is empty", ALL("x", ALL("y", NOT(R("x", "y"))))),
    "NONEMPTY_R": ("R has at least one edge", EX("x", EX("y", R("x", "y")))),
    "HAS_R_SOURCE": (
        "some element has no R-predecessor",
        EX("x", ALL("y", NOT(R("y", "x")))),
    ),
    "HAS_R_SINK": (
        "some element has no R-successor",
        EX("x", ALL("y", NOT(R("x", "y")))),
    ),
    "P_EMPTY": ("P is empty", ALL("x", NOT(Pp("x")))),
    "P_NONEMPTY": ("P is inhabited", EX("x", Pp("x"))),
    "P_ALL": ("P holds everywhere", ALL("x", Pp("x"))),
    "P_FORWARD_CLOSED": (
        "P is closed under R-successors",
        ALL("x", ALL("y", IMP(AND(Pp("x"), R("x", "y")), Pp("y")))),
    ),
    "P_BACKWARD_CLOSED": (
        "P is closed under R-predecessors",
        ALL("x", ALL("y", IMP(AND(Pp("y"), R("x", "y")), Pp("x")))),
    ),
    "R_INTO_P": (
        "every R-successor lies in P",
        ALL("x", ALL("y", IMP(R("x", "y"), Pp("y")))),
    ),
    "P_SERIAL": (
        "every P element has a P successor",
        ALL("x", IMP(Pp("x"), EX("y", AND(R("x", "y"), Pp("y"))))),
    ),
    "P_ISOLATED": (
        "no P element has a proper R-successor",
        ALL("x", ALL("y", IMP(AND(Pp("x"), R("x", "y")), EQ("x", "y")))),
    ),
    "SINGLETON_DOMAIN": ("the domain has exactly one element", ALL("x", ALL("y", EQ("x", "y")))),
    "AT_LEAST_TWO": (
        "the domain has at least two elements",
        EX("x", EX("y", NOT(EQ("x", "y")))),
    ),
}

FORMULA_IDS: tuple[str, ...] = tuple(sorted(FORMULAS))

# --------------------------------------------------------------------------
# bounded model space
# --------------------------------------------------------------------------

_COUNT = {n: 1 << (n * n + n) for n in SIZES}
_OFFSET: dict[int, int] = {}
_acc = 0
for _n in SIZES:
    _OFFSET[_n] = _acc
    _acc += _COUNT[_n]
TOTAL_MODELS = _acc
ALL_MODELS_MASK = (1 << TOTAL_MODELS) - 1
SIZE_MASK: dict[int, int] = {
    n: ((1 << _COUNT[n]) - 1) << _OFFSET[n] for n in SIZES
}
_SIZE_OF_INDEX = bytes(
    next(n for n in SIZES if _OFFSET[n] <= i < _OFFSET[n] + _COUNT[n])
    for i in range(TOTAL_MODELS)
)


def model_index(n: int, rmask: int, pmask: int) -> int:
    """Global index of the model (domain size `n`, edge set `rmask`, P set `pmask`)."""
    return _OFFSET[n] + (rmask << n) + pmask


def model_of_index(idx: int) -> tuple[int, int, int]:
    n = _SIZE_OF_INDEX[idx]
    local = idx - _OFFSET[n]
    return n, local >> n, local & ((1 << n) - 1)


def size_of_index(idx: int) -> int:
    return _SIZE_OF_INDEX[idx]


def lowest_index(mask: int) -> int:
    return (mask & -mask).bit_length() - 1


def model_json(n: int, rmask: int, pmask: int) -> dict:
    return {
        "domain_size": n,
        "R": sorted([i, j] for i in range(n) for j in range(n) if (rmask >> (i * n + j)) & 1),
        "P": sorted(i for i in range(n) if (pmask >> i) & 1),
    }


# --------------------------------------------------------------------------
# grounding: one circuit per (formula, domain size)
# --------------------------------------------------------------------------


def _ground(ast: tuple, n: int, env: dict[str, int]) -> tuple:
    t = ast[0]
    if t == "R":
        return ("AR", env[ast[1]] * n + env[ast[2]])
    if t == "P":
        return ("AP", env[ast[1]])
    if t == "EQ":
        return ("C", env[ast[1]] == env[ast[2]])
    if t == "NOT":
        return ("N", _ground(ast[1], n, env))
    if t in ("AND", "OR"):
        return ("A" if t == "AND" else "O", tuple(_ground(f, n, env) for f in ast[1]))
    if t in ("ALL", "EX"):
        return (
            "A" if t == "ALL" else "O",
            tuple(_ground(ast[2], n, {**env, ast[1]: i}) for i in range(n)),
        )
    raise ValueError(f"unknown node {t}")  # pragma: no cover


_CIRCUIT: dict[tuple[str, int], tuple] = {}


def circuit(fid: str, n: int) -> tuple:
    key = (fid, n)
    c = _CIRCUIT.get(key)
    if c is None:
        c = _ground(FORMULAS[fid][1], n, {})
        _CIRCUIT[key] = c
    return c


# --------------------------------------------------------------------------
# three evaluators over the grounded circuit
# --------------------------------------------------------------------------


def eval_scalar(c: tuple, n: int, rmask: int, pmask: int) -> bool:
    """Two-valued evaluation on one complete model."""
    t = c[0]
    if t == "AR":
        return bool((rmask >> c[1]) & 1)
    if t == "AP":
        return bool((pmask >> c[1]) & 1)
    if t == "C":
        return bool(c[1])
    if t == "N":
        return not eval_scalar(c[1], n, rmask, pmask)
    if t == "A":
        return all(eval_scalar(k, n, rmask, pmask) for k in c[1])
    return any(eval_scalar(k, n, rmask, pmask) for k in c[1])


def eval_kleene(c: tuple, state: Sequence[int | None], nsq: int) -> int | None:
    """Three-valued (Kleene) evaluation on a partial model.

    `state` holds one entry per cell: the n*n edge cells followed by the n
    membership cells; `None` means undecided.  Returns 1, 0 or None.
    """
    t = c[0]
    if t == "AR":
        return state[c[1]]
    if t == "AP":
        return state[nsq + c[1]]
    if t == "C":
        return 1 if c[1] else 0
    if t == "N":
        v = eval_kleene(c[1], state, nsq)
        return None if v is None else 1 - v
    if t == "A":
        unknown = False
        for k in c[1]:
            v = eval_kleene(k, state, nsq)
            if v == 0:
                return 0
            if v is None:
                unknown = True
        return None if unknown else 1
    unknown = False
    for k in c[1]:
        v = eval_kleene(k, state, nsq)
        if v == 1:
            return 1
        if v is None:
            unknown = True
    return None if unknown else 0


def _eval_bits(c: tuple, atoms: Sequence[int], nsq: int, full: int) -> int:
    """Bitset evaluation: one column over every model of a single domain size."""
    t = c[0]
    if t == "AR":
        return atoms[c[1]]
    if t == "AP":
        return atoms[nsq + c[1]]
    if t == "C":
        return full if c[1] else 0
    if t == "N":
        return full & ~_eval_bits(c[1], atoms, nsq, full)
    if t == "A":
        acc = full
        for k in c[1]:
            acc &= _eval_bits(k, atoms, nsq, full)
            if not acc:
                return 0
        return acc
    acc = 0
    for k in c[1]:
        acc |= _eval_bits(k, atoms, nsq, full)
        if acc == full:
            return full
    return acc


# --------------------------------------------------------------------------
# exhaustive truth table (built once per process, lazily)
# --------------------------------------------------------------------------

_TABLE: dict[str, int] = {}
_ROW: dict[str, bytes] = {}


def _atom_columns(n: int) -> tuple[list[int], int, int]:
    nsq = n * n
    block = (1 << (1 << n)) - 1  # every pmask of one rmask block
    atoms: list[int] = []
    for k in range(nsq):
        col = 0
        for rmask in range(1 << nsq):
            if (rmask >> k) & 1:
                col |= block << (rmask << n)
        atoms.append(col)
    for i in range(n):
        pat = 0
        for pmask in range(1 << n):
            if (pmask >> i) & 1:
                pat |= 1 << pmask
        col = 0
        for rmask in range(1 << nsq):
            col |= pat << (rmask << n)
        atoms.append(col)
    return atoms, nsq, (1 << _COUNT[n]) - 1


def _build_table() -> None:
    if _TABLE:
        return
    per_size = {n: _atom_columns(n) for n in SIZES}
    nbytes = (TOTAL_MODELS + 7) // 8
    for fid in FORMULA_IDS:
        mask = 0
        for n in SIZES:
            atoms, nsq, full = per_size[n]
            mask |= _eval_bits(circuit(fid, n), atoms, nsq, full) << _OFFSET[n]
        _TABLE[fid] = mask
        raw = mask.to_bytes(nbytes, "little")
        _ROW[fid] = bytes(
            (raw[i >> 3] >> (i & 7)) & 1 for i in range(TOTAL_MODELS)
        )


def sat_mask(fid: str) -> int:
    """Bitset of every model in the bounded space that satisfies `fid`."""
    _build_table()
    return _TABLE[fid]


def holds_at(fid: str, idx: int) -> bool:
    """Constant-time model check used by the arms; never reveals a disposition."""
    _build_table()
    return _ROW[fid][idx] == 1


def hypothesis_mask(hyps: Sequence[str]) -> int:
    m = ALL_MODELS_MASK
    for h in hyps:
        m &= sat_mask(h)
    return m


# --------------------------------------------------------------------------
# registered rule base (the derivation vocabulary; every rule is verified)
# --------------------------------------------------------------------------

RULE_BASE: tuple[tuple[tuple[str, ...], str], ...] = (
    (("ASYMMETRIC",), "IRREFLEXIVE"),
    (("ASYMMETRIC",), "ANTISYMMETRIC"),
    (("IRREFLEXIVE", "TRANSITIVE"), "ASYMMETRIC"),
    (("IRREFLEXIVE", "EUCLIDEAN"), "EMPTY_R"),
    (("SYMMETRIC", "ASYMMETRIC"), "EMPTY_R"),
    (("EMPTY_R",), "IRREFLEXIVE"),
    (("EMPTY_R",), "SYMMETRIC"),
    (("EMPTY_R",), "TRANSITIVE"),
    (("EMPTY_R",), "ANTISYMMETRIC"),
    (("EMPTY_R",), "FUNCTIONAL"),
    (("EMPTY_R",), "INJECTIVE_R"),
    (("EMPTY_R",), "EUCLIDEAN"),
    (("EMPTY_R",), "DENSE"),
    (("EMPTY_R",), "HAS_R_SOURCE"),
    (("EMPTY_R",), "HAS_R_SINK"),
    (("EMPTY_R",), "P_FORWARD_CLOSED"),
    (("EMPTY_R",), "P_BACKWARD_CLOSED"),
    (("EMPTY_R",), "R_INTO_P"),
    (("EMPTY_R",), "P_ISOLATED"),
    (("REFLEXIVE",), "SERIAL"),
    (("REFLEXIVE",), "NONEMPTY_R"),
    (("REFLEXIVE",), "DENSE"),
    (("CONNEX",), "REFLEXIVE"),
    (("CONNEX",), "SERIAL"),
    (("CONNEX",), "NONEMPTY_R"),
    (("SYMMETRIC", "TRANSITIVE"), "EUCLIDEAN"),
    (("REFLEXIVE", "EUCLIDEAN"), "SYMMETRIC"),
    (("REFLEXIVE", "EUCLIDEAN"), "TRANSITIVE"),
    (("SERIAL", "R_INTO_P"), "P_NONEMPTY"),
    (("P_ALL",), "P_NONEMPTY"),
    (("P_ALL",), "P_FORWARD_CLOSED"),
    (("P_ALL",), "P_BACKWARD_CLOSED"),
    (("P_ALL",), "R_INTO_P"),
    (("P_EMPTY",), "P_FORWARD_CLOSED"),
    (("P_EMPTY",), "P_BACKWARD_CLOSED"),
    (("P_EMPTY",), "P_SERIAL"),
    (("P_EMPTY",), "P_ISOLATED"),
    (("P_ALL", "SERIAL"), "P_SERIAL"),
    (("SINGLETON_DOMAIN",), "SYMMETRIC"),
    (("SINGLETON_DOMAIN",), "ANTISYMMETRIC"),
    (("SINGLETON_DOMAIN",), "TRANSITIVE"),
    (("SINGLETON_DOMAIN",), "FUNCTIONAL"),
    (("SINGLETON_DOMAIN",), "INJECTIVE_R"),
    (("SINGLETON_DOMAIN",), "EUCLIDEAN"),
    (("SINGLETON_DOMAIN",), "P_ISOLATED"),
    (("SINGLETON_DOMAIN", "NONEMPTY_R"), "REFLEXIVE"),
    (("SINGLETON_DOMAIN", "NONEMPTY_R"), "CONNEX"),
    (("FUNCTIONAL", "SERIAL", "SINGLETON_DOMAIN"), "REFLEXIVE"),
    (("IRREFLEXIVE", "TRANSITIVE"), "ANTISYMMETRIC"),
    (("REFLEXIVE", "TRANSITIVE"), "DENSE"),
)


def invalid_rules() -> list[dict]:
    """Every registered rule, checked exhaustively against the bounded space."""
    bad: list[dict] = []
    for i, (prem, concl) in enumerate(RULE_BASE):
        m = ALL_MODELS_MASK
        for p in prem:
            m &= sat_mask(p)
        counter = m & ~sat_mask(concl) & ALL_MODELS_MASK
        if counter:
            bad.append(
                {
                    "rule_index": i,
                    "premises": list(prem),
                    "conclusion": concl,
                    "countermodel": model_json(*model_of_index(lowest_index(counter))),
                }
            )
    return bad


def forward_chain(
    hyps: Sequence[str], budget: int = 10**6, rule_order: Sequence[int] | None = None
) -> tuple[set[str], list[list], int]:
    """Forward chaining over the registered rule base.

    Returns the derived set, the derivation (a list of `[rule_index,
    conclusion]` steps in application order) and the number of rule
    applications consumed.
    """
    order = list(rule_order) if rule_order is not None else list(range(len(RULE_BASE)))
    derived = set(hyps)
    steps: list[list] = []
    changed = True
    while changed and len(steps) < budget:
        changed = False
        for i in order:
            prem, concl = RULE_BASE[i]
            if concl in derived or not all(p in derived for p in prem):
                continue
            derived.add(concl)
            steps.append([i, concl])
            changed = True
            if len(steps) >= budget:
                break
    return derived, steps, len(steps)


# --------------------------------------------------------------------------
# task model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Instance:
    """One bounded conjecture, plus the confirming/refuting evidence shown with it."""

    instance_id: str
    family: str
    seed: int
    hypotheses: tuple[str, ...]
    conjuncts: tuple[str, ...]
    surface_support: tuple[int, ...]  # registered sample of models of H (global indices)

    def as_json(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,
            "domain_bound": DOMAIN_BOUND,
            "hypotheses": list(self.hypotheses),
            "conjuncts": list(self.conjuncts),
            "surface_support": [model_json(*model_of_index(i)) for i in self.surface_support],
        }


def _classify(
    failing: Sequence[int], minimal_size: int, min_h_size: int
) -> str:
    """Registered classification order: multiplicity dominates minimality."""
    if not failing:
        return "TRANSFER_VALID"
    if len(failing) >= 2:
        return "MULTIPLE_INDEPENDENT_OBSTRUCTIONS"
    if minimal_size > min_h_size:
        return "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED"
    return "REJECT_WITH_COUNTEREXAMPLE"


@dataclass(frozen=True)
class OracleAnswer:
    disposition: str
    failing_conjuncts: tuple[int, ...]
    minimal_size: int
    min_hypothesis_model_size: int
    n_hypothesis_models: int
    n_countermodels: int
    witness: Any

    def as_dict(self) -> dict:
        return {
            "disposition": self.disposition,
            "best_profile": {
                "disposition": self.disposition,
                "failing_conjuncts": list(self.failing_conjuncts),
                "minimal_size": self.minimal_size,
                "min_hypothesis_model_size": self.min_hypothesis_model_size,
            },
            "n_hypothesis_models": self.n_hypothesis_models,
            "n_countermodels": self.n_countermodels,
            "witness": self.witness,
        }


# --------------------------------------------------------------------------
# oracle 1 — exhaustive enumeration as bitset set algebra
# --------------------------------------------------------------------------


def _derivation_for(inst: Instance) -> list[list] | None:
    derived, steps, _ = forward_chain(inst.hypotheses)
    if all(c in derived for c in inst.conjuncts):
        return steps
    return None


def oracle_exhaustive(inst: Instance) -> OracleAnswer:
    hm = hypothesis_mask(inst.hypotheses)
    if hm == 0:  # pragma: no cover - the generator rejects unsatisfiable hypotheses
        return OracleAnswer("UNDECIDED_BUDGET_EXHAUSTED", (), -1, -1, 0, 0, None)
    min_h = size_of_index(lowest_index(hm))
    failing: list[int] = []
    per_conjunct: dict[int, int] = {}
    for i, c in enumerate(inst.conjuncts):
        cm = hm & ~sat_mask(c) & ALL_MODELS_MASK
        if cm:
            failing.append(i)
            per_conjunct[i] = cm
    union = 0
    for cm in per_conjunct.values():
        union |= cm
    minimal_size = size_of_index(lowest_index(union)) if union else -1
    disp = _classify(failing, minimal_size, min_h)
    if disp == "TRANSFER_VALID":
        steps = _derivation_for(inst)
        witness = {"kind": "DERIVATION", "steps": steps} if steps is not None else None
    elif disp == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS":
        witness = {
            "kind": "OBSTRUCTION_SET",
            "models": [
                model_json(*model_of_index(lowest_index(per_conjunct[i]))) for i in failing
            ],
        }
    else:
        best = min(
            (i for i in failing),
            key=lambda i: lowest_index(per_conjunct[i]),
        )
        witness = {
            "kind": "COUNTERMODEL",
            "model": model_json(*model_of_index(lowest_index(per_conjunct[best]))),
        }
    return OracleAnswer(
        disp,
        tuple(failing),
        minimal_size,
        min_h,
        hm.bit_count(),
        union.bit_count(),
        witness,
    )


def countermodel_indices(inst: Instance) -> int:
    """Bitset of every model of H in the bounded space that falsifies some conjunct."""
    hm = hypothesis_mask(inst.hypotheses)
    cm = 0
    for c in inst.conjuncts:
        cm |= hm & ~sat_mask(c) & ALL_MODELS_MASK
    return cm


def confirming_ratio(inst: Instance) -> float:
    hm = hypothesis_mask(inst.hypotheses)
    if hm == 0:  # pragma: no cover
        return 0.0
    return 1.0 - countermodel_indices(inst).bit_count() / hm.bit_count()


# --------------------------------------------------------------------------
# oracle 2 — size-stratified DFS with Kleene propagation (independent)
# --------------------------------------------------------------------------


def _dfs_models(hyps: Sequence[str], n: int) -> Iterator[tuple[int, int]]:
    """Every model of `hyps` at domain size `n`, without materialising the space.

    Cells are assigned one at a time; after each assignment every hypothesis is
    evaluated under Kleene semantics and the branch is cut as soon as one is
    definitely false.  The search never enumerates models it has already
    excluded, and because sizes are visited in ascending order by the caller the
    first countermodel it reports is of minimum size by construction.
    """
    nsq = n * n
    ncell = nsq + n
    circuits = [circuit(h, n) for h in hyps]
    state: list[int | None] = [None] * ncell

    def rec(k: int) -> Iterator[tuple[int, int]]:
        if k == ncell:
            rmask = sum(1 << c for c in range(nsq) if state[c])
            pmask = sum(1 << (c - nsq) for c in range(nsq, ncell) if state[c])
            yield rmask, pmask
            return
        for v in (0, 1):
            state[k] = v
            if all(eval_kleene(c, state, nsq) != 0 for c in circuits):
                yield from rec(k + 1)
        state[k] = None

    yield from rec(0)


def oracle_stratified_dpll(inst: Instance) -> OracleAnswer:
    conj_circuits = {n: [circuit(c, n) for c in inst.conjuncts] for n in SIZES}
    min_h = -1
    first_size: dict[int, int] = {}
    witness_model: dict[int, tuple[int, int, int]] = {}
    remaining = set(range(len(inst.conjuncts)))
    for n in SIZES:
        for rmask, pmask in _dfs_models(inst.hypotheses, n):
            if min_h < 0:
                min_h = n
            if not remaining:
                break
            for i in sorted(remaining):
                if not eval_scalar(conj_circuits[n][i], n, rmask, pmask):
                    first_size[i] = n
                    witness_model[i] = (n, rmask, pmask)
                    remaining.discard(i)
        if min_h >= 0 and not remaining:
            break
    if min_h < 0:  # pragma: no cover - the generator rejects unsatisfiable hypotheses
        return OracleAnswer("UNDECIDED_BUDGET_EXHAUSTED", (), -1, -1, -1, -1, None)
    failing = sorted(first_size)
    minimal_size = min(first_size.values()) if failing else -1
    disp = _classify(failing, minimal_size, min_h)
    if disp == "TRANSFER_VALID":
        steps = _derivation_for(inst)
        witness = {"kind": "DERIVATION", "steps": steps} if steps is not None else None
    elif disp == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS":
        witness = {
            "kind": "OBSTRUCTION_SET",
            "models": [model_json(*witness_model[i]) for i in failing],
        }
    else:
        witness = {"kind": "COUNTERMODEL", "model": model_json(*witness_model[failing[0]])}
    return OracleAnswer(disp, tuple(failing), minimal_size, min_h, -1, -1, witness)


def oracle_agrees(inst: Instance) -> tuple[bool, OracleAnswer, OracleAnswer]:
    a = oracle_exhaustive(inst)
    b = oracle_stratified_dpll(inst)
    same = a.disposition == b.disposition and a.as_dict()["best_profile"] == b.as_dict()["best_profile"]
    return same, a, b


# --------------------------------------------------------------------------
# generator: proposes a family, the exhaustive oracle verifies it
# --------------------------------------------------------------------------

EXPECTED_DISPOSITION = {
    "no_obstruction": {"TRANSFER_VALID"},
    "single_hidden_obstruction": {"REJECT_WITH_COUNTEREXAMPLE"},
    "multiple_obstruction": {"MULTIPLE_INDEPENDENT_OBSTRUCTIONS"},
    "minimal_counterexample": {"REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED"},
    "misleading_surface_support": {
        "REJECT_WITH_COUNTEREXAMPLE",
        "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED",
    },
}


def _mask_indices(mask: int) -> list[int]:
    out: list[int] = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def obstructions_are_independent(inst: Instance) -> bool:
    """No failing conjunct's countermodel set is contained in another's.

    This is a *generator* acceptance predicate, not an oracle agreement field:
    it needs the full countermodel sets, which the stratified search never
    materialises, so claiming both algorithms agree on it would be a check that
    cannot actually be run.
    """
    hm = hypothesis_mask(inst.hypotheses)
    sets = []
    for c in inst.conjuncts:
        cm = hm & ~sat_mask(c) & ALL_MODELS_MASK
        if cm:
            sets.append(cm)
    if len(sets) < 2:
        return False
    return all(a & ~b for a in sets for b in sets if a is not b)


def _sample_evidence(inst_seed: int, hm: int, confirming_only_mask: int | None) -> tuple[int, ...]:
    """The evidence set presented with the conjecture (registered, deterministic)."""
    pool_mask = hm if confirming_only_mask is None else confirming_only_mask
    pool = _mask_indices(pool_mask)
    if not pool:
        return ()
    rng = random.Random(inst_seed ^ 0x5E1DE)
    k = min(INDUCTIVE_SAMPLE_SIZE, len(pool))
    return tuple(sorted(rng.sample(pool, k)))


def _propose(family: str, seed: int, idx: int) -> Instance | None:
    rng = random.Random(seed)
    hyps = tuple(sorted(rng.sample(FORMULA_IDS, rng.choice((2, 3)))))
    hm = hypothesis_mask(hyps)
    n_h = hm.bit_count()
    if not (MIN_HYPOTHESIS_MODELS <= n_h <= MAX_HYPOTHESIS_MODELS):
        return None
    rest = [f for f in FORMULA_IDS if f not in hyps]
    if family == "no_obstruction":
        derived, _, _ = forward_chain(hyps)
        pool = sorted(d for d in derived if d not in hyps)
        if not pool:
            return None
        conj = tuple(sorted(rng.sample(pool, min(len(pool), rng.choice((1, 2))))))
    else:
        want = rng.choice((2, 3)) if family == "multiple_obstruction" else rng.choice((1, 2, 3))
        conj = tuple(sorted(rng.sample(rest, want)))
    if set(conj) & set(hyps):  # pragma: no cover - disjoint by construction
        return None
    probe = Instance(f"{family}-{idx:05d}", family, seed, hyps, conj, ())
    if family == "misleading_surface_support":
        confirming = hm & ~countermodel_indices(probe) & ALL_MODELS_MASK
        evidence = _sample_evidence(seed, hm, confirming)
    else:
        evidence = _sample_evidence(seed, hm, None)
    if len(evidence) < min(INDUCTIVE_SAMPLE_SIZE, n_h):
        return None
    return Instance(f"{family}-{idx:05d}", family, seed, hyps, conj, evidence)


def _family_predicate(family: str, inst: Instance, ans: OracleAnswer) -> bool:
    if ans.disposition not in EXPECTED_DISPOSITION[family]:
        return False
    ratio = confirming_ratio(inst)
    if family == "no_obstruction":
        return _derivation_for(inst) is not None
    if family == "single_hidden_obstruction":
        return ratio < MISLEADING_MIN_CONFIRMING_RATIO
    if family == "multiple_obstruction":
        return obstructions_are_independent(inst)
    if family == "minimal_counterexample":
        return ans.minimal_size > ans.min_hypothesis_model_size
    # misleading_surface_support: rare countermodel, and the presented evidence
    # confirms the conjecture without exception
    return (
        ratio >= MISLEADING_MIN_CONFIRMING_RATIO
        and ans.n_countermodels <= MISLEADING_MAX_COUNTERMODELS
        and all(
            all(holds_at(c, i) for c in inst.conjuncts) for i in inst.surface_support
        )
    )


def generate_split(split: str, seed: str, per_family: dict[str, int]):
    """Generate (instance, oracle) pairs.

    The generator *proposes* a family; the exhaustive oracle *verifies* it.  An
    instance whose exhaustive disposition is not in its family's registered set,
    whose family predicate fails, or on which the two oracle algorithms
    disagree, is rejected and resampled.  Rejections are counted per family and
    reported, never hidden.
    """
    pairs: list[tuple[Instance, OracleAnswer]] = []
    rejects: dict[str, int] = {f: 0 for f in FAMILIES}
    for family in FAMILIES:
        want = per_family.get(family, 0)
        made = counter = 0
        while made < want:
            counter += 1
            if counter > 4000 * (want + 1):  # pragma: no cover - generator safety
                raise RuntimeError(f"{split}/{family}: generator could not fill quota")
            s = int.from_bytes(
                hashlib.sha256(f"{seed}|{split}|{family}|{counter}".encode()).digest()[:8],
                "big",
            )
            inst = _propose(family, s, counter)
            if inst is None:
                rejects[family] += 1
                continue
            a = oracle_exhaustive(inst)
            if not _family_predicate(family, inst, a):
                rejects[family] += 1
                continue
            b = oracle_stratified_dpll(inst)
            if b.disposition != a.disposition or b.as_dict()["best_profile"] != a.as_dict()["best_profile"]:
                rejects[family] += 1
                continue
            made += 1
            pairs.append((inst, a))
    return pairs, rejects


# --------------------------------------------------------------------------
# witness validation (the protocol's hard gate, made operational)
# --------------------------------------------------------------------------

WITNESS_REQUIRED = {
    "TRANSFER_VALID": "DERIVATION",
    "REJECT_WITH_COUNTEREXAMPLE": "COUNTERMODEL",
    "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED": "COUNTERMODEL",
    "MULTIPLE_INDEPENDENT_OBSTRUCTIONS": "OBSTRUCTION_SET",
    "UNDECIDED_BUDGET_EXHAUSTED": None,
}


def _model_from_json(m: dict) -> tuple[int, int, int] | None:
    try:
        n = int(m["domain_size"])
        if n not in SIZES:
            return None
        rmask = 0
        for a, b in m["R"]:
            if not (0 <= a < n and 0 <= b < n):
                return None
            rmask |= 1 << (a * n + b)
        pmask = 0
        for a in m["P"]:
            if not (0 <= a < n):
                return None
            pmask |= 1 << a
    except (KeyError, TypeError, ValueError):
        return None
    return n, rmask, pmask


def _satisfies_hypotheses(inst: Instance, n: int, rmask: int, pmask: int) -> bool:
    return all(eval_scalar(circuit(h, n), n, rmask, pmask) for h in inst.hypotheses)


def _falsified_conjuncts(inst: Instance, n: int, rmask: int, pmask: int) -> list[int]:
    return [
        i
        for i, c in enumerate(inst.conjuncts)
        if not eval_scalar(circuit(c, n), n, rmask, pmask)
    ]


def validate_witness(inst: Instance, disposition: str, witness: Any) -> tuple[bool, str]:
    """Registered witness validator, applied identically to every non-control arm.

    Model checking is done by direct evaluation of the grounded circuit, so the
    validator does not depend on the oracle's disposition logic.  The one place
    it consults the exhaustive truth table is the minimality clause, which is a
    bounded *verification* ("no smaller countermodel exists"), never a solve on
    the arm's behalf.
    """
    if disposition not in WITNESS_REQUIRED:
        return False, f"unregistered_disposition:{disposition}"
    kind = WITNESS_REQUIRED[disposition]
    if kind is None:
        return (witness is None), "abstention_must_carry_no_witness"
    if not isinstance(witness, dict) or witness.get("kind") != kind:
        return False, f"missing_or_wrong_witness_kind:expected_{kind}"
    if kind == "DERIVATION":
        steps = witness.get("steps")
        if not isinstance(steps, list):
            return False, "derivation_steps_missing"
        derived = set(inst.hypotheses)
        for step in steps:
            if not (isinstance(step, list) and len(step) == 2):
                return False, "malformed_derivation_step"
            ri, concl = step
            if not isinstance(ri, int) or not (0 <= ri < len(RULE_BASE)):
                return False, "unregistered_rule_index"
            prem, real = RULE_BASE[ri]
            if real != concl:
                return False, "step_conclusion_does_not_match_rule"
            if not all(p in derived for p in prem):
                return False, "rule_premises_not_yet_available"
            derived.add(concl)
        missing = [c for c in inst.conjuncts if c not in derived]
        if missing:
            return False, f"conjuncts_not_derived:{sorted(missing)}"
        return True, "derivation_checked"
    if kind == "COUNTERMODEL":
        m = _model_from_json(witness.get("model"))
        if m is None:
            return False, "malformed_model"
        n, rmask, pmask = m
        if not _satisfies_hypotheses(inst, n, rmask, pmask):
            return False, "witness_does_not_satisfy_hypotheses"
        if not _falsified_conjuncts(inst, n, rmask, pmask):
            return False, "witness_does_not_falsify_the_conclusion"
        if disposition == "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED":
            smaller = countermodel_indices(inst) & ((1 << _OFFSET[n]) - 1)
            if smaller:
                return False, "a_strictly_smaller_countermodel_exists"
        return True, "countermodel_checked"
    models = witness.get("models")
    if not isinstance(models, list) or len(models) < 2:
        return False, "obstruction_set_needs_at_least_two_models"
    covered: set[int] = set()
    for mj in models:
        m = _model_from_json(mj)
        if m is None:
            return False, "malformed_model"
        n, rmask, pmask = m
        if not _satisfies_hypotheses(inst, n, rmask, pmask):
            return False, "witness_does_not_satisfy_hypotheses"
        covered.update(_falsified_conjuncts(inst, n, rmask, pmask))
    if len(covered) < 2:
        return False, "fewer_than_two_distinct_conjuncts_refuted"
    return True, "obstruction_set_checked"


# --------------------------------------------------------------------------
# parents (each with native known-answer tests; see `parent_fidelity`)
# --------------------------------------------------------------------------

# P1's frozen reference corpus: three structures fixed once, never re-derived.
REFERENCE_CORPUS: tuple[tuple[int, int, int], ...] = (
    (1, 0, 0),
    (2, 1 << 1, 1 << 0),
    (3, (1 << 1) | (1 << 5), 1 << 2),
)


def parent_inductive_confirmation(inst: Instance) -> dict:
    """P0 — inductive confirmation from the presented evidence.

    The baseline the protocol's `misleading_surface_support` family exists to
    defeat, and a real method rather than a strawman: generalise from the
    confirming instances actually shown with the conjecture, and refute only if
    one of them happens to be a countermodel.  It performs no search of its own,
    and it has no proof procedure, so an acceptance it issues is a formal claim
    without a witness — which is precisely what the hard gate forbids.
    """
    for idx in inst.surface_support:
        bad = [c for c in inst.conjuncts if not holds_at(c, idx)]
        if bad:
            n, r, p = model_of_index(idx)
            return {
                "disposition": "REJECT_WITH_COUNTEREXAMPLE",
                "witness": {"kind": "COUNTERMODEL", "model": model_json(n, r, p)},
            }
    return {"disposition": "TRANSFER_VALID", "witness": None}


def parent_fixed_lesson(inst: Instance) -> dict:
    """P1 — fixed-lesson injection: a frozen verdict table, no search.

    The protocol's frozen-lesson baseline.  Each conclusion formula carries a
    verdict and a canned countermodel learned once from `REFERENCE_CORPUS`; the
    hypotheses are not consulted at all, which is the whole point of a frozen
    table.
    """
    refuted: list[dict] = []
    for c in inst.conjuncts:
        for n, r, p in REFERENCE_CORPUS:
            if not eval_scalar(circuit(c, n), n, r, p):
                refuted.append(model_json(n, r, p))
                break
    if len(refuted) >= 2:
        return {
            "disposition": "MULTIPLE_INDEPENDENT_OBSTRUCTIONS",
            "witness": {"kind": "OBSTRUCTION_SET", "models": refuted[:2]},
        }
    if len(refuted) == 1:
        return {
            "disposition": "REJECT_WITH_COUNTEREXAMPLE",
            "witness": {"kind": "COUNTERMODEL", "model": refuted[0]},
        }
    return {"disposition": "TRANSFER_VALID", "witness": None}


def _model_search(inst: Instance, scope_mask: int) -> dict:
    """Exhaustive finite-model search restricted to `scope_mask`."""
    hm = hypothesis_mask(inst.hypotheses) & scope_mask
    if hm == 0:
        return {"disposition": "UNDECIDED_BUDGET_EXHAUSTED", "witness": None}
    min_h = size_of_index(lowest_index(hm))
    per: dict[int, int] = {}
    for i, c in enumerate(inst.conjuncts):
        cm = hm & ~sat_mask(c) & ALL_MODELS_MASK
        if cm:
            per[i] = cm
    if not per:
        # No countermodel in scope.  A model searcher has no proof to offer:
        # the claim it can make is a bare one.
        return {"disposition": "TRANSFER_VALID", "witness": None}
    failing = sorted(per)
    minimal = min(size_of_index(lowest_index(per[i])) for i in failing)
    disp = _classify(failing, minimal, min_h)
    if disp == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS":
        return {
            "disposition": disp,
            "witness": {
                "kind": "OBSTRUCTION_SET",
                "models": [model_json(*model_of_index(lowest_index(per[i]))) for i in failing],
            },
        }
    best = min(failing, key=lambda i: lowest_index(per[i]))
    return {
        "disposition": disp,
        "witness": {
            "kind": "COUNTERMODEL",
            "model": model_json(*model_of_index(lowest_index(per[best]))),
        },
    }


def parent_exhaustive_model_search(inst: Instance) -> dict:
    """P2 — exhaustive finite-model search to the registered bound (Mace4-style).

    The mature owner of the countermodel question: it materialises the bounded
    model space and decides, exactly, which conjuncts fail, at what minimum size
    and how many independent obstructions there are.  Its documented boundary is
    the other half of the endpoint: exhausting the space without a countermodel
    yields no derivation, so its acceptance is a claim without a proof witness.
    """
    return _model_search(inst, ALL_MODELS_MASK)


def parent_small_scope_check(inst: Instance) -> dict:
    """P4 — bounded small-scope check (Alloy-style small-scope hypothesis).

    Exhaustive within a registered scope of `SMALL_SCOPE_BOUND`, and blind
    beyond it.  A mature and widely used method whose real boundary is exactly
    the `minimal_counterexample` family: an obstruction that first appears one
    size above the scope is invisible to it.
    """
    scope = 0
    for n in SIZES:
        if n <= SMALL_SCOPE_BOUND:
            scope |= SIZE_MASK[n]
    return _model_search(inst, scope)


def parent_derivation_search(inst: Instance) -> dict:
    """P3 — saturating derivation search over the registered rule base.

    The mature owner of the acceptance question: forward chaining to the
    fixpoint of the registered rule base, emitting the derivation as the proof
    witness.  Its documented boundary is that a prover produces no
    countermodels: failing to derive the conclusion is not a refutation, so it
    abstains rather than rejecting.
    """
    derived, steps, _ = forward_chain(inst.hypotheses)
    if all(c in derived for c in inst.conjuncts):
        return {"disposition": "TRANSFER_VALID", "witness": {"kind": "DERIVATION", "steps": steps}}
    return {"disposition": "UNDECIDED_BUDGET_EXHAUSTED", "witness": None}


# --------------------------------------------------------------------------
# federation
# --------------------------------------------------------------------------


def federation(inst: Instance) -> dict:
    """F0 — strongest faithful parent federation, under a pre-registered rule.

    Registered before any outcome and blind to it: the acceptance question is
    put to the derivation parent (P3) first, because only a derivation can
    discharge the protocol's witness requirement; **only if** P3 fails to derive
    the conclusion is the countermodel parent (P2) consulted, and its verdict
    and witness are taken as they stand.  If neither parent produces anything,
    the federation abstains.  Neither parent is consulted outside its native
    competence and neither ever sees the oracle.
    """
    p3 = parent_derivation_search(inst)
    if p3["disposition"] == "TRANSFER_VALID":
        return {**p3, "source": "P3"}
    p2 = parent_exhaustive_model_search(inst)
    if p2["disposition"] == "TRANSFER_VALID":
        # bounded-valid but not derivable in the registered base: neither parent
        # can discharge the claim, and the federation says so.
        return {"disposition": "UNDECIDED_BUDGET_EXHAUSTED", "witness": None, "source": "P2+P3"}
    return {**p2, "source": "P2"}


# --------------------------------------------------------------------------
# mechanic and ablations
# --------------------------------------------------------------------------

_M_RULE_ORDER = sorted(range(len(RULE_BASE)), key=lambda i: (len(RULE_BASE[i][0]), i))


def _m_explore(inst: Instance, n: int) -> list[int]:
    """M's anytime exploration of the hypothesis region at domain size `n`.

    Exhaustive at sizes at or below `M_EXHAUSTIVE_SIZE_CUTOFF`, where the space
    is small enough to certify minimality; above it, M seeds from the presented
    evidence plus bounded random probing and then explores by **local repair** —
    breadth-first over single-cell edits that stay inside the hypothesis region.
    That is complete only on the components its seeds reach, so M can miss an
    obstruction the complete parent finds.  The divergence is real, which is
    what makes `G1a` a measurement rather than an algebraic identity.
    """
    hyps = inst.hypotheses
    if n <= M_EXHAUSTIVE_SIZE_CUTOFF:
        lo, hi = _OFFSET[n], _OFFSET[n] + _COUNT[n]
        return [i for i in range(lo, hi) if all(holds_at(h, i) for h in hyps)]
    nsq = n * n
    rng = random.Random((inst.seed ^ 0x0F60) + n)
    region = [i for i in inst.surface_support if size_of_index(i) == n]
    seen = set(region)
    probes = 0
    while len(region) < M_SEED_TARGET and probes < M_PROBE_BUDGET // 2:
        probes += 1
        idx = _OFFSET[n] + rng.randrange(_COUNT[n])
        if idx in seen:
            continue
        seen.add(idx)
        if all(holds_at(h, idx) for h in hyps):
            region.append(idx)
    frontier = list(region)
    expansions = 0
    while frontier and expansions < M_PROBE_BUDGET:
        idx = frontier.pop()
        expansions += 1
        _, r, p = model_of_index(idx)
        for cell in range(nsq + n):
            nb = (
                model_index(n, r ^ (1 << cell), p)
                if cell < nsq
                else model_index(n, r, p ^ (1 << (cell - nsq)))
            )
            if nb in seen:
                continue
            seen.add(nb)
            if all(holds_at(h, nb) for h in hyps):
                region.append(nb)
                frontier.append(nb)
    return sorted(region)


def _m_pipeline(
    inst: Instance,
    *,
    proof: bool = True,
    search: bool = True,
    minimality: bool = True,
    multiplicity: bool = True,
) -> dict:
    """M — F2 obstruction discovery (issue #50 L2 pipeline), and its ablations.

    structural description -> bounded proof attempt -> anytime obstruction
    search by local repair -> minimality escalation -> multiplicity check ->
    disposition plus witness.

    **This is an independent implementation, and deliberately so.**  M never
    calls the parents' procedures: its proof stage is budgeted and uses its own
    rule ordering, and its obstruction stage explores the hypothesis region by
    local repair from the presented evidence rather than materialising the
    space.  Both stages can fail where the complete parents succeed, so
    "the federation reproduces M" is measured, not guaranteed.
    """
    if proof:
        derived, steps, _ = forward_chain(
            inst.hypotheses, budget=PROOF_STEP_BUDGET, rule_order=_M_RULE_ORDER
        )
        if all(c in derived for c in inst.conjuncts):
            return {
                "disposition": "TRANSFER_VALID",
                "witness": {"kind": "DERIVATION", "steps": steps},
                "source": "proof",
            }
    if not search:
        return {"disposition": "TRANSFER_VALID", "witness": None, "source": "no_search"}
    first_size: dict[int, int] = {}
    wit: dict[int, int] = {}
    min_h = -1
    for n in SIZES:
        region = _m_explore(inst, n)
        if region and min_h < 0:
            min_h = n
        for idx in region:
            for i, c in enumerate(inst.conjuncts):
                if i in first_size or holds_at(c, idx):
                    continue
                first_size[i] = n
                wit[i] = idx
                if not multiplicity:
                    break
            if first_size and not multiplicity:
                break
        if min_h >= 0 and (len(first_size) == len(inst.conjuncts) or (first_size and not multiplicity)):
            break
    if not first_size:
        return {"disposition": "UNDECIDED_BUDGET_EXHAUSTED", "witness": None, "source": "exhausted"}
    failing = sorted(first_size)
    minimal = min(first_size.values())
    disp = _classify(failing, minimal, min_h)
    if not minimality and disp == "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED":
        disp = "REJECT_WITH_COUNTEREXAMPLE"
    if disp == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS":
        return {
            "disposition": disp,
            "witness": {
                "kind": "OBSTRUCTION_SET",
                "models": [model_json(*model_of_index(wit[i])) for i in failing],
            },
            "source": "search",
        }
    best = min(failing, key=lambda i: (first_size[i], wit[i]))
    return {
        "disposition": disp,
        "witness": {"kind": "COUNTERMODEL", "model": model_json(*model_of_index(wit[best]))},
        "source": "search",
    }


def mechanic_full(inst: Instance) -> dict:
    return _m_pipeline(inst)


def ablation_minus_obstruction_search(inst: Instance) -> dict:
    """M without the obstruction search: it claims before looking for a counterexample."""
    return _m_pipeline(inst, search=False)


def ablation_minus_proof_witness(inst: Instance) -> dict:
    """M without the proof stage: obstruction search only, so acceptance is bare."""
    return _m_pipeline(inst, proof=False)


def ablation_minus_minimality_escalation(inst: Instance) -> dict:
    """M without minimality escalation: any single obstruction is reported flat."""
    return _m_pipeline(inst, minimality=False)


def ablation_minus_multiplicity_check(inst: Instance) -> dict:
    """M without the multiplicity check: it stops at the first obstruction found."""
    return _m_pipeline(inst, multiplicity=False)


# --------------------------------------------------------------------------
# controls (registered as exempt from witness validation)
# --------------------------------------------------------------------------


def control_always_accept(inst: Instance) -> dict:
    return {"disposition": "TRANSFER_VALID", "witness": None}


def control_always_block(inst: Instance) -> dict:
    return {"disposition": "MULTIPLE_INDEPENDENT_OBSTRUCTIONS", "witness": None}


def control_random(inst: Instance) -> dict:
    return {
        "disposition": random.Random(inst.seed ^ 0x5EED).choice(DISPOSITIONS),
        "witness": None,
    }


ARM_FUNCTIONS = {
    "P0_INDUCTIVE_CONFIRMATION": parent_inductive_confirmation,
    "P1_FIXED_LESSON_TABLE": parent_fixed_lesson,
    "P2_EXHAUSTIVE_MODEL_SEARCH": parent_exhaustive_model_search,
    "P3_DERIVATION_PROOF_SEARCH": parent_derivation_search,
    "P4_SMALL_SCOPE_BOUNDED_CHECK": parent_small_scope_check,
    "F0_PARENT_FEDERATION": federation,
    "M_F2_OBSTRUCTION_DISCOVERY_FULL": mechanic_full,
    "M_MINUS_OBSTRUCTION_SEARCH": ablation_minus_obstruction_search,
    "M_MINUS_PROOF_WITNESS": ablation_minus_proof_witness,
    "M_MINUS_MINIMALITY_ESCALATION": ablation_minus_minimality_escalation,
    "M_MINUS_MULTIPLICITY_CHECK": ablation_minus_multiplicity_check,
    "C_ALWAYS_ACCEPT": control_always_accept,
    "C_ALWAYS_BLOCK": control_always_block,
    "C_RANDOM_DISPOSITION": control_random,
}

CONTROL_ARMS = ("C_ALWAYS_ACCEPT", "C_ALWAYS_BLOCK", "C_RANDOM_DISPOSITION")


def run_arm(arm: str, inst: Instance) -> dict:
    """Dispatch one arm and enforce the protocol's witness gate.

    `formal_claim_without_witness_allowed: false` is enforced here, uniformly:
    a non-control arm whose witness fails the registered validator has its
    disposition rewritten to `CLAIM_WITHOUT_VALID_WITNESS`, which is never an
    oracle label and is therefore always scored wrong.  Control arms are
    registered exempt, because a control exists to exercise a counter — and the
    over-acceptance counter behind `G2` could not fire at all if every bare
    claim were rewritten before it was counted.
    """
    out = ARM_FUNCTIONS[arm](inst)
    claimed = out["disposition"]
    witness = out.get("witness")
    if arm in CONTROL_ARMS:
        return {
            "disposition": claimed,
            "claimed_disposition": claimed,
            "witness_valid": None,
            "witness_check": "registered_control_exempt_from_witness_validation",
            "witness": witness,
            "source": out.get("source"),
        }
    valid, reason = validate_witness(inst, claimed, witness)
    return {
        "disposition": claimed if valid else "CLAIM_WITHOUT_VALID_WITNESS",
        "claimed_disposition": claimed,
        "witness_valid": bool(valid),
        "witness_check": reason,
        "witness": witness,
        "source": out.get("source"),
    }


# --------------------------------------------------------------------------
# hand-authored known-answer fixtures (G0a)
# --------------------------------------------------------------------------


def _fixture(name: str, family: str, hyps: Sequence[str], conj: Sequence[str]) -> Instance:
    return Instance(name, family, 0, tuple(hyps), tuple(conj), ())


def known_answer_fixtures() -> list[dict]:
    F: list[dict] = []

    def add(name, family, hyps, conj, expected):
        F.append(
            {
                "name": name,
                "instance": _fixture(name, family, hyps, conj),
                "expected": expected,
            }
        )

    add(
        "KA-01-ASYMMETRIC-ENTAILS-IRREFLEXIVE",
        "no_obstruction",
        ["ASYMMETRIC"],
        ["IRREFLEXIVE"],
        "TRANSFER_VALID",
    )
    add(
        "KA-02-STRICT-ORDER-IS-ANTISYMMETRIC",
        "no_obstruction",
        ["IRREFLEXIVE", "TRANSITIVE"],
        ["ANTISYMMETRIC"],
        "TRANSFER_VALID",
    )
    add(
        "KA-03-EQUIVALENCE-WITHOUT-REFLEXIVITY",
        "single_hidden_obstruction",
        ["SYMMETRIC", "TRANSITIVE"],
        ["REFLEXIVE"],
        "REJECT_WITH_COUNTEREXAMPLE",
    )
    # the classical minimal counterexample: irreflexive antisymmetric relations
    # are transitive at every domain size below three, and first fail at three
    add(
        "KA-04-TRANSITIVITY-FAILS-FIRST-AT-SIZE-THREE",
        "minimal_counterexample",
        ["IRREFLEXIVE", "ANTISYMMETRIC"],
        ["TRANSITIVE"],
        "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED",
    )
    add(
        "KA-05-TWO-INDEPENDENT-OBSTRUCTIONS",
        "multiple_obstruction",
        ["AT_LEAST_TWO"],
        ["REFLEXIVE", "SYMMETRIC"],
        "MULTIPLE_INDEPENDENT_OBSTRUCTIONS",
    )
    add(
        "KA-06-CONNEX-ENTAILS-REFLEXIVE",
        "no_obstruction",
        ["CONNEX"],
        ["REFLEXIVE"],
        "TRANSFER_VALID",
    )
    add(
        "KA-07-SERIALITY-IS-NOT-REFLEXIVITY",
        "minimal_counterexample",
        ["SERIAL"],
        ["REFLEXIVE"],
        "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED",
    )
    add(
        "KA-08-EMPTY-RELATION-ENTAILS-BOTH",
        "no_obstruction",
        ["EMPTY_R"],
        ["SYMMETRIC", "TRANSITIVE"],
        "TRANSFER_VALID",
    )
    add(
        "KA-09-INHABITED-IS-NOT-UNIVERSAL",
        "single_hidden_obstruction",
        ["P_NONEMPTY", "AT_LEAST_TWO"],
        ["P_ALL"],
        "REJECT_WITH_COUNTEREXAMPLE",
    )
    add(
        "KA-10-SINGLETON-DOMAIN-ENTAILS-BOTH",
        "no_obstruction",
        ["SINGLETON_DOMAIN"],
        ["SYMMETRIC", "TRANSITIVE"],
        "TRANSFER_VALID",
    )
    # KA-11 pins the registered classification order: multiplicity dominates
    # minimality.  TRANSITIVE first fails at size three and NONEMPTY_R already
    # fails at size one, so a minimality-first reading would call this
    # REJECT_WITH_COUNTEREXAMPLE; the registered order calls it MULTIPLE.
    add(
        "KA-11-MULTIPLICITY-DOMINATES-MINIMALITY",
        "multiple_obstruction",
        ["IRREFLEXIVE", "ANTISYMMETRIC"],
        ["TRANSITIVE", "NONEMPTY_R"],
        "MULTIPLE_INDEPENDENT_OBSTRUCTIONS",
    )
    add(
        "KA-12-EUCLIDEAN-REFLEXIVE-ENTAILS-SYMMETRY",
        "no_obstruction",
        ["REFLEXIVE", "EUCLIDEAN"],
        ["SYMMETRIC", "TRANSITIVE"],
        "TRANSFER_VALID",
    )
    return F


# --------------------------------------------------------------------------
# parent fidelity: native known-answer tests (must pass before use)
# --------------------------------------------------------------------------


def parent_fidelity() -> list[dict]:
    T: list[dict] = []

    def check(parent: str, name: str, ok: bool, detail: str = "") -> None:
        T.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    fx = {f["name"]: f["instance"] for f in known_answer_fixtures()}
    theorem = fx["KA-01-ASYMMETRIC-ENTAILS-IRREFLEXIVE"]
    non_theorem = fx["KA-03-EQUIVALENCE-WITHOUT-REFLEXIVITY"]
    deep = fx["KA-04-TRANSITIVITY-FAILS-FIRST-AT-SIZE-THREE"]
    multi = fx["KA-05-TWO-INDEPENDENT-OBSTRUCTIONS"]

    # ---- model machinery -------------------------------------------------
    round_trip = all(
        model_index(*model_of_index(i)) == i for i in range(TOTAL_MODELS)
    )
    check("MODEL_SPACE", "index_round_trip_over_the_whole_bounded_space", round_trip,
          f"{TOTAL_MODELS} models")
    mismatch = 0
    for fid in FORMULA_IDS:
        for idx in range(TOTAL_MODELS):
            n, r, p = model_of_index(idx)
            if eval_scalar(circuit(fid, n), n, r, p) != holds_at(fid, idx):
                mismatch += 1
    check(
        "MODEL_SPACE",
        "vectorised_truth_column_agrees_with_scalar_evaluation_everywhere",
        mismatch == 0,
        f"{len(FORMULA_IDS) * TOTAL_MODELS} model-formula pairs, {mismatch} mismatches",
    )
    check(
        "MODEL_SPACE",
        "size_strata_partition_the_space",
        sum(SIZE_MASK[n].bit_count() for n in SIZES) == TOTAL_MODELS,
    )
    check(
        "MODEL_SPACE",
        "singleton_and_at_least_two_are_complementary",
        sat_mask("SINGLETON_DOMAIN") | sat_mask("AT_LEAST_TWO") == ALL_MODELS_MASK
        and sat_mask("SINGLETON_DOMAIN") & sat_mask("AT_LEAST_TWO") == 0,
    )

    # ---- P3 derivation proof search --------------------------------------
    bad_rules = invalid_rules()
    check(
        "P3_DERIVATION_PROOF_SEARCH",
        "every_registered_rule_is_valid_over_the_bounded_space",
        not bad_rules,
        f"{len(RULE_BASE)} rules, {len(bad_rules)} invalid",
    )
    p3 = parent_derivation_search(theorem)
    check(
        "P3_DERIVATION_PROOF_SEARCH",
        "derives_asymmetry_entails_irreflexivity",
        p3["disposition"] == "TRANSFER_VALID",
        p3["disposition"],
    )
    check(
        "P3_DERIVATION_PROOF_SEARCH",
        "its_derivation_passes_the_independent_validator",
        validate_witness(theorem, "TRANSFER_VALID", p3["witness"])[0],
    )
    chain = _fixture("KA-CHAIN", "no_obstruction", ["IRREFLEXIVE", "TRANSITIVE"], ["ANTISYMMETRIC"])
    check(
        "P3_DERIVATION_PROOF_SEARCH",
        "chains_two_premise_rules_to_a_new_conclusion",
        parent_derivation_search(chain)["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P3_DERIVATION_PROOF_SEARCH",
        "documented_boundary_abstains_instead_of_refuting",
        parent_derivation_search(non_theorem)["disposition"] == "UNDECIDED_BUDGET_EXHAUSTED",
        "scope note: a prover produces no countermodels",
    )

    # ---- P2 exhaustive finite-model search --------------------------------
    p2 = parent_exhaustive_model_search(non_theorem)
    check(
        "P2_EXHAUSTIVE_MODEL_SEARCH",
        "finds_a_countermodel_for_a_known_non_theorem",
        p2["disposition"] == "REJECT_WITH_COUNTEREXAMPLE",
        p2["disposition"],
    )
    check(
        "P2_EXHAUSTIVE_MODEL_SEARCH",
        "its_countermodel_passes_the_independent_validator",
        validate_witness(non_theorem, p2["disposition"], p2["witness"])[0],
    )
    p2d = parent_exhaustive_model_search(deep)
    check(
        "P2_EXHAUSTIVE_MODEL_SEARCH",
        "returns_the_minimum_size_countermodel_not_merely_a_countermodel",
        p2d["disposition"] == "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED"
        and p2d["witness"]["model"]["domain_size"] == 3,
        str(p2d["witness"]),
    )
    p2m = parent_exhaustive_model_search(multi)
    check(
        "P2_EXHAUSTIVE_MODEL_SEARCH",
        "counts_two_independent_obstructions",
        p2m["disposition"] == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS"
        and len(p2m["witness"]["models"]) == 2,
        str(p2m["disposition"]),
    )
    check(
        "P2_EXHAUSTIVE_MODEL_SEARCH",
        "documented_boundary_accepts_without_a_proof_witness",
        parent_exhaustive_model_search(theorem)["disposition"] == "TRANSFER_VALID"
        and parent_exhaustive_model_search(theorem)["witness"] is None,
        "scope note: exhausting the space yields no derivation",
    )

    # ---- P4 small-scope bounded check -------------------------------------
    check(
        "P4_SMALL_SCOPE_BOUNDED_CHECK",
        "finds_the_in_scope_countermodel",
        parent_small_scope_check(non_theorem)["disposition"] == "REJECT_WITH_COUNTEREXAMPLE",
    )
    check(
        "P4_SMALL_SCOPE_BOUNDED_CHECK",
        "its_in_scope_countermodel_passes_the_validator",
        validate_witness(
            non_theorem,
            "REJECT_WITH_COUNTEREXAMPLE",
            parent_small_scope_check(non_theorem)["witness"],
        )[0],
    )
    check(
        "P4_SMALL_SCOPE_BOUNDED_CHECK",
        "documented_boundary_blind_to_an_obstruction_above_its_scope",
        parent_small_scope_check(deep)["disposition"] == "TRANSFER_VALID",
        "scope note: the small-scope hypothesis is exactly this bet",
    )

    # ---- P0 inductive confirmation ----------------------------------------
    hm = hypothesis_mask(non_theorem.hypotheses)
    cm = countermodel_indices(non_theorem)
    refuting = _fixture("KA-P0-A", "single_hidden_obstruction", non_theorem.hypotheses,
                        non_theorem.conjuncts)
    refuting = Instance(
        refuting.instance_id, refuting.family, 0, refuting.hypotheses, refuting.conjuncts,
        (lowest_index(cm),),
    )
    check(
        "P0_INDUCTIVE_CONFIRMATION",
        "refutes_when_the_presented_evidence_contains_a_countermodel",
        parent_inductive_confirmation(refuting)["disposition"] == "REJECT_WITH_COUNTEREXAMPLE",
    )
    confirming = Instance(
        "KA-P0-B", "misleading_surface_support", 0, non_theorem.hypotheses,
        non_theorem.conjuncts, tuple(_mask_indices(hm & ~cm & ALL_MODELS_MASK)[:6]),
    )
    p0c = parent_inductive_confirmation(confirming)
    check(
        "P0_INDUCTIVE_CONFIRMATION",
        "generalises_from_confirming_evidence_alone",
        p0c["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P0_INDUCTIVE_CONFIRMATION",
        "documented_boundary_its_acceptance_carries_no_witness",
        p0c["witness"] is None
        and not validate_witness(confirming, "TRANSFER_VALID", p0c["witness"])[0],
        "scope note: induction from instances is not a proof",
    )

    # ---- P1 fixed-lesson table --------------------------------------------
    same_conclusion_other_hyps = _fixture(
        "KA-P1", "single_hidden_obstruction", ["EMPTY_R"], non_theorem.conjuncts
    )
    check(
        "P1_FIXED_LESSON_TABLE",
        "verdict_ignores_the_hypotheses_entirely",
        parent_fixed_lesson(non_theorem)["disposition"]
        == parent_fixed_lesson(same_conclusion_other_hyps)["disposition"],
        "scope note: a frozen lesson table is not context sensitive",
    )
    check(
        "P1_FIXED_LESSON_TABLE",
        "reports_multiplicity_when_two_conclusions_are_refuted_by_the_corpus",
        parent_fixed_lesson(multi)["disposition"] == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS",
    )
    canned_misfit = _fixture("KA-P1B", "single_hidden_obstruction", ["CONNEX"], ["EMPTY_R"])
    p1c = parent_fixed_lesson(canned_misfit)
    check(
        "P1_FIXED_LESSON_TABLE",
        "documented_boundary_its_canned_witness_can_fail_validation",
        not validate_witness(canned_misfit, p1c["disposition"], p1c["witness"])[0],
        "scope note: a canned countermodel need not satisfy this instance's hypotheses",
    )

    # ---- F0 federation -----------------------------------------------------
    check(
        "F0_PARENT_FEDERATION",
        "takes_the_derivation_parent_on_a_bounded_theorem",
        federation(theorem)["source"] == "P3",
    )
    check(
        "F0_PARENT_FEDERATION",
        "takes_the_model_parent_on_a_non_theorem",
        federation(non_theorem)["source"] == "P2"
        and federation(non_theorem)["disposition"] == "REJECT_WITH_COUNTEREXAMPLE",
    )
    undis = _fixture("KA-F0", "no_obstruction", ["DENSE", "AT_LEAST_TWO"], ["HAS_R_SINK"])
    check(
        "F0_PARENT_FEDERATION",
        "abstains_when_neither_parent_can_discharge_the_claim",
        federation(undis)["disposition"]
        in ("UNDECIDED_BUDGET_EXHAUSTED", "REJECT_WITH_COUNTEREXAMPLE",
            "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED", "MULTIPLE_INDEPENDENT_OBSTRUCTIONS"),
        federation(undis)["disposition"],
    )

    # ---- witness validator -------------------------------------------------
    good = parent_exhaustive_model_search(non_theorem)["witness"]
    check(
        "WITNESS_VALIDATOR",
        "rejects_a_countermodel_that_does_not_satisfy_the_hypotheses",
        not validate_witness(
            non_theorem,
            "REJECT_WITH_COUNTEREXAMPLE",
            {"kind": "COUNTERMODEL", "model": model_json(2, 1 << 1, 0)},
        )[0],
    )
    check(
        "WITNESS_VALIDATOR",
        "accepts_a_genuine_countermodel",
        validate_witness(non_theorem, "REJECT_WITH_COUNTEREXAMPLE", good)[0],
    )
    check(
        "WITNESS_VALIDATOR",
        "rejects_a_non_minimal_model_for_a_minimality_claim",
        not validate_witness(
            deep,
            "REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED",
            {"kind": "COUNTERMODEL", "model": model_json(2, 1 << 1, 0)},
        )[0],
    )
    check(
        "WITNESS_VALIDATOR",
        "rejects_a_derivation_citing_an_unregistered_rule",
        not validate_witness(
            theorem, "TRANSFER_VALID", {"kind": "DERIVATION", "steps": [[10**6, "IRREFLEXIVE"]]}
        )[0],
    )
    check(
        "WITNESS_VALIDATOR",
        "rejects_a_derivation_whose_premises_are_not_yet_available",
        not validate_witness(
            _fixture("KA-W", "no_obstruction", ["SYMMETRIC"], ["EMPTY_R"]),
            "TRANSFER_VALID",
            {"kind": "DERIVATION", "steps": [[4, "EMPTY_R"]]},
        )[0],
    )

    # ---- the two oracle algorithms on the hand-authored fixtures -----------
    disagree = [f["name"] for f in known_answer_fixtures() if not oracle_agrees(f["instance"])[0]]
    check(
        "ORACLE_PAIR",
        "both_algorithms_agree_on_every_hand_authored_fixture",
        not disagree,
        str(disagree),
    )
    return T


# --------------------------------------------------------------------------
# planted positives (trip-wires: every no-alarm assertion must be shown to fire)
# --------------------------------------------------------------------------


def _planted_forged_witness_arm(inst: Instance) -> dict:
    """A planted arm that returns the oracle's own label with a forged witness.

    Registered in `ARM_FUNCTIONS` but deliberately **not** in `SPEC.arms`, so it
    never contributes to the study: it exists only so the witness trip-wire runs
    through the real dispatcher rather than through a copy of it.
    """
    truth = oracle_exhaustive(inst)
    # a structure that is not a model of this instance's hypotheses at all: the
    # careless witness an arm offers when it never checks what it is exhibiting
    off_model = next(
        model_json(*model_of_index(i))
        for i in range(TOTAL_MODELS)
        if not _satisfies_hypotheses(inst, *model_of_index(i))
    )
    forged: Any
    if truth.disposition == "TRANSFER_VALID":
        forged = {"kind": "DERIVATION", "steps": [[len(RULE_BASE), "IRREFLEXIVE"]]}
    elif truth.disposition == "MULTIPLE_INDEPENDENT_OBSTRUCTIONS":
        forged = {"kind": "OBSTRUCTION_SET", "models": [off_model, off_model]}
    else:
        forged = {"kind": "COUNTERMODEL", "model": off_model}
    return {"disposition": truth.disposition, "witness": forged}


ARM_FUNCTIONS["X_PLANTED_FORGED_WITNESS"] = _planted_forged_witness_arm

# the FM/FG R2 fm60 row: five arms, all exactly 32/120
R2_FM60_FLOOR_RATE = 32 / 120


def planted_positives() -> list[PlantedPositive]:
    from fm_core import discrimination_gate

    P = [
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "small_scope_pseudo_oracle_is_detected",
            "a deliberately incomplete oracle that searches only to the small "
            "scope must disagree with exhaustive enumeration on an instance "
            "whose obstruction first appears one size above that scope",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "wrong_expected_label_is_detected",
            "the known-answer comparison must reject a deliberately wrong "
            "expected disposition",
        ),
        PlantedPositive(
            "G2_ANTI_PERMISSIVENESS",
            "over_accepting_arm_is_detected",
            "the over-acceptance counter must count C_ALWAYS_ACCEPT on an "
            "instance the oracle blocks",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_ceiling_split_is_detected",
            "a synthetic per-arm table in which every arm scores 1.000 must FAIL "
            "the discrimination gate (the FM/FG R2 ceiling defect)",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_floor_split_is_detected",
            "a synthetic per-arm table in which every arm scores 0.267 — the "
            "literal FM/FG R2 fm60 row, all five arms at 32/120 — must FAIL the "
            "discrimination gate on its solvable half",
        ),
        PlantedPositive(
            "HARD_GATE_FORMAL_CLAIM_WITHOUT_WITNESS",
            "right_label_with_a_forged_witness_is_caught",
            "an arm that returns the oracle's own disposition but supplies an "
            "invalid witness must be rewritten to CLAIM_WITHOUT_VALID_WITNESS by "
            "the same dispatcher that produces the study's numbers",
        ),
        PlantedPositive(
            "G3_MECHANISM_BY_OMISSION",
            "minimality_ablation_loses_the_deep_counterexample",
            "M_MINUS_MINIMALITY_ESCALATION must be wrong on a hand-built "
            "minimal-counterexample instance on which M is right",
        ),
    ]

    fx = known_answer_fixtures()
    theorem = fx[0]["instance"]
    blocked = fx[2]["instance"]
    deep = fx[3]["instance"]

    scope = 0
    for n in SIZES:
        if n <= SMALL_SCOPE_BOUND:
            scope |= SIZE_MASK[n]
    pseudo = _model_search(deep, scope)
    P[0].fired = pseudo["disposition"] != oracle_exhaustive(deep).disposition

    P[1].fired = oracle_exhaustive(theorem).disposition != "MULTIPLE_INDEPENDENT_OBSTRUCTIONS"

    P[2].fired = (
        control_always_accept(blocked)["disposition"] == "TRANSFER_VALID"
        and oracle_exhaustive(blocked).disposition != "TRANSFER_VALID"
    )

    P[3].fired = (
        discrimination_gate(
            {a: 1.0 for a in ARM_FUNCTIONS},
            weak_arms=("C_RANDOM_DISPOSITION",),
            max_weak=0.85,
            min_strong=0.95,
        ).verdict
        == "FAIL"
    )

    floor = discrimination_gate(
        {a: R2_FM60_FLOOR_RATE for a in ARM_FUNCTIONS},
        weak_arms=("C_RANDOM_DISPOSITION",),
        max_weak=0.85,
        min_strong=0.95,
    )
    P[4].fired = (
        floor.verdict == "FAIL" and floor.detail["halves"]["solvable"]["violation"] is True
    )

    forged = run_arm("X_PLANTED_FORGED_WITNESS", blocked)
    honest = run_arm("P2_EXHAUSTIVE_MODEL_SEARCH", blocked)
    P[5].fired = (
        forged["claimed_disposition"] == oracle_exhaustive(blocked).disposition
        and forged["disposition"] == "CLAIM_WITHOUT_VALID_WITNESS"
        and honest["disposition"] == oracle_exhaustive(blocked).disposition
    )

    truth = oracle_exhaustive(deep).disposition
    P[6].fired = (
        run_arm("M_F2_OBSTRUCTION_DISCOVERY_FULL", deep)["disposition"] == truth
        and run_arm("M_MINUS_MINIMALITY_ESCALATION", deep)["disposition"] != truth
    )
    return P


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------

SPEC = SuiteSpec(
    suite_id="FM60",
    title="Obstruction and counterexample discovery with exact witness validation",
    families=FAMILIES,
    arms=(
        ArmSpec(
            "P0_INDUCTIVE_CONFIRMATION",
            "PARENT",
            "inductive confirmation from the presented evidence set",
        ),
        ArmSpec("P1_FIXED_LESSON_TABLE", "PARENT", "frozen verdict table, no search"),
        ArmSpec(
            "P2_EXHAUSTIVE_MODEL_SEARCH",
            "PARENT",
            "exhaustive finite-model search to the registered bound (Mace4-style)",
        ),
        ArmSpec(
            "P3_DERIVATION_PROOF_SEARCH",
            "PARENT",
            "saturating derivation search over the registered rule base",
        ),
        ArmSpec(
            "P4_SMALL_SCOPE_BOUNDED_CHECK",
            "PARENT",
            "bounded small-scope check (Alloy-style small-scope hypothesis)",
        ),
        ArmSpec(
            "F0_PARENT_FEDERATION",
            "FEDERATION",
            "strongest faithful parent federation under a pre-registered outcome-blind rule",
        ),
        ArmSpec(
            "M_F2_OBSTRUCTION_DISCOVERY_FULL",
            "MECHANIC",
            "ORION L2 obstruction and counterexample discovery, full",
        ),
        ArmSpec("M_MINUS_OBSTRUCTION_SEARCH", "ABLATION", ""),
        ArmSpec("M_MINUS_PROOF_WITNESS", "ABLATION", ""),
        ArmSpec("M_MINUS_MINIMALITY_ESCALATION", "ABLATION", ""),
        ArmSpec("M_MINUS_MULTIPLICITY_CHECK", "ABLATION", ""),
        ArmSpec("C_ALWAYS_ACCEPT", "CONTROL", ""),
        ArmSpec("C_ALWAYS_BLOCK", "CONTROL", ""),
        ArmSpec("C_RANDOM_DISPOSITION", "CONTROL", ""),
    ),
    mechanic_arm="M_F2_OBSTRUCTION_DISCOVERY_FULL",
    strongest_parent_arm="F0_PARENT_FEDERATION",
    federation_arm="F0_PARENT_FEDERATION",
    weak_arms=(
        "P0_INDUCTIVE_CONFIRMATION",
        "P1_FIXED_LESSON_TABLE",
        "P4_SMALL_SCOPE_BOUNDED_CHECK",
        "M_MINUS_OBSTRUCTION_SEARCH",
    ),
    constant_arms=("C_ALWAYS_ACCEPT", "C_ALWAYS_BLOCK"),
    random_arm="C_RANDOM_DISPOSITION",
    ablation_for_family={
        "no_obstruction": "M_MINUS_PROOF_WITNESS",
        "single_hidden_obstruction": "M_MINUS_OBSTRUCTION_SEARCH",
        "multiple_obstruction": "M_MINUS_MULTIPLICITY_CHECK",
        "minimal_counterexample": "M_MINUS_MINIMALITY_ESCALATION",
        "misleading_surface_support": "M_MINUS_OBSTRUCTION_SEARCH",
    },
    default_ablation="M_MINUS_OBSTRUCTION_SEARCH",
    decoy_families=(
        "multiple_obstruction",
        "minimal_counterexample",
        "misleading_surface_support",
    ),
    min_tasks=120,
    dev_per_family=3,
    protected_per_family=25,  # 5 x 25 = 125 >= 120
    design_json="FM60_OBSTRUCTION_COUNTEREXAMPLE_EXACT_STUDY_DESIGN_V1.json",
    generate=generate_split,
    oracle=oracle_exhaustive,
    cross_check=oracle_stratified_dpll,
    run_arm=run_arm,
    parent_fidelity=parent_fidelity,
    known_answer_fixtures=known_answer_fixtures,
    planted_positives=planted_positives,
)
