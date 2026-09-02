"""FG series parent formalisms: faithful native implementations + the native
known-answer selftests each must pass before it may be used as a comparator.

Six parents, each implemented to its own published semantics and each tested
against its *own* literature examples, not against the FG task:

* `LGG`        -- Plotkin (1970) least general generalization / anti-unification.
* `FCA`        -- Ganter & Wille formal concept analysis: derivation operators,
                  closure, concepts, attribute implications; the Galois
                  adjunction is checked through
                  `orion_v2.meta_formalization.assess_galois_connection`.
* `MDL`        -- two-part minimum description length over a frozen code, with a
                  native-recovery constraint (a hypothesis that loses a
                  registered distinction is inadmissible).
* `MODEL_SEARCH` -- finite model / countermodel search by exhaustion.
* `CONSERVATIVE` -- conservative-extension checking through
                  `orion_v2.meta_formalization.assess_conservative_extension`.
* `THEORY_REVISION` -- AGM-style contraction-plus-exception base revision.

A parent that cannot be implemented faithfully is `CANNOT_CHECK`, never a
strawman.  None of these modules imports `fg_oracle`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence

from orion_v2.meta_formalization import (  # noqa: F401
    ConservativeExtensionStatus,
    FiniteConsequenceTheory,
    FiniteGaloisConnection,
    FinitePoset,
    LawStatus,
    assess_conservative_extension,
    assess_galois_connection,
)

VARIABLE = "?"


# ---------------------------------------------------------------------------
# P1 -- Plotkin least general generalization / anti-unification
# ---------------------------------------------------------------------------


def lgg_pair(left: Sequence[str], right: Sequence[str]) -> tuple[str, ...]:
    """Plotkin's lgg of two ground tuples of equal arity."""

    if len(left) != len(right):
        raise ValueError("anti-unification requires equal arity")
    return tuple(a if a == b else VARIABLE for a, b in zip(left, right))


def lgg_set(rows: Sequence[Sequence[str]]) -> tuple[str, ...]:
    if not rows:
        raise ValueError("lgg of the empty set is undefined")
    current = tuple(rows[0])
    for row in rows[1:]:
        current = lgg_pair(current, row)
    return current


def subsumes(pattern: Sequence[str], ground: Sequence[str]) -> bool:
    """theta-subsumption for flat ground tuples."""

    return all(p == VARIABLE or p == g for p, g in zip(pattern, ground))


def lgg_is_least_general(rows: Sequence[Sequence[str]], alphabet: Sequence[str]) -> bool:
    """Exhaustive check that no strictly-less-general pattern covers all rows."""

    target = lgg_set(rows)
    arity = len(target)
    for candidate in _all_patterns(arity, alphabet):
        if not all(subsumes(candidate, row) for row in rows):
            continue
        # candidate must be subsumed by (i.e. at least as general as) target
        if not subsumes(target, candidate) and candidate != target:
            if sum(1 for value in candidate if value == VARIABLE) < sum(
                1 for value in target if value == VARIABLE
            ):
                return False
    return True


def _all_patterns(arity: int, alphabet: Sequence[str]) -> Iterable[tuple[str, ...]]:
    values = list(alphabet) + [VARIABLE]
    if arity == 0:
        yield ()
        return
    for head in values:
        for tail in _all_patterns(arity - 1, alphabet):
            yield (head,) + tail


# ---------------------------------------------------------------------------
# P2 -- Formal concept analysis (Ganter & Wille)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalContext:
    objects: tuple[str, ...]
    attributes: tuple[str, ...]
    incidence: frozenset[tuple[str, str]]

    def object_intent(self, obj: str) -> frozenset[str]:
        return frozenset(m for m in self.attributes if (obj, m) in self.incidence)

    def attribute_extent(self, attribute: str) -> frozenset[str]:
        return frozenset(g for g in self.objects if (g, attribute) in self.incidence)

    def derive_objects(self, objects: Iterable[str]) -> frozenset[str]:
        objects = list(objects)
        if not objects:
            return frozenset(self.attributes)
        result = self.object_intent(objects[0])
        for obj in objects[1:]:
            result &= self.object_intent(obj)
        return result

    def derive_attributes(self, attributes: Iterable[str]) -> frozenset[str]:
        attributes = list(attributes)
        if not attributes:
            return frozenset(self.objects)
        result = self.attribute_extent(attributes[0])
        for attribute in attributes[1:]:
            result &= self.attribute_extent(attribute)
        return result

    def closure_objects(self, objects: Iterable[str]) -> frozenset[str]:
        return self.derive_attributes(self.derive_objects(objects))

    def concepts(self) -> tuple[tuple[frozenset[str], frozenset[str]], ...]:
        seen: set[tuple[frozenset[str], frozenset[str]]] = set()
        for size in range(len(self.attributes) + 1):
            for subset in combinations(self.attributes, size):
                extent = self.derive_attributes(subset)
                intent = self.derive_objects(extent)
                seen.add((extent, intent))
        return tuple(sorted(seen, key=lambda pair: (len(pair[0]), sorted(pair[0]))))

    def implication_holds(self, premise: Iterable[str], conclusion: Iterable[str]) -> bool:
        return self.derive_attributes(premise) <= self.derive_attributes(conclusion)


def galois_adjunction_witness(context: FormalContext) -> str:
    """Check A subseteq B' <=> B subseteq A' via the ORION Galois-connection law."""

    objects = tuple(sorted(context.objects))
    attributes = tuple(sorted(context.attributes))
    object_sets = [frozenset(s) for k in range(len(objects) + 1) for s in combinations(objects, k)]
    attribute_sets = [
        frozenset(s) for k in range(len(attributes) + 1) for s in combinations(attributes, k)
    ]
    concrete = FinitePoset(
        "OBJ",
        frozenset(object_sets),
        frozenset((a, b) for a in object_sets for b in object_sets if a <= b),
    )
    # the abstract side is ordered by *reverse* inclusion, as FCA requires
    abstract = FinitePoset(
        "ATT",
        frozenset(attribute_sets),
        frozenset((a, b) for a in attribute_sets for b in attribute_sets if a >= b),
    )
    connection = FiniteGaloisConnection(
        "FCA",
        "OBJ",
        "ATT",
        {s: context.derive_objects(s) for s in object_sets},
        {s: context.derive_attributes(s) for s in attribute_sets},
    )
    return assess_galois_connection(concrete, abstract, connection).status.value


# ---------------------------------------------------------------------------
# P3 -- MDL two-part code (native, not the registered tier order)
# ---------------------------------------------------------------------------

RESIDUAL_PENALTY_BITS = 12.0
OBSERVATION_ACQUISITION_BITS = 6.0


def _bits(count: int) -> float:
    return math.log2(max(count, 1))


def mdl_model_bits(
    tier: str,
    *,
    n_parents: int,
    n_atoms: int,
    n_cases: int,
    n_decisions: int,
    patch_size: int,
    n_derived_terms: int,
    n_representation_terms: int,
    n_observables: int,
    n_relational_ops: int,
) -> float:
    """Frozen native MDL code for each repair kind."""

    if tier == "NO_CHANGE":
        return 0.0
    if tier == "PARENT_FORMALISM_SUFFICIENT":
        return _bits(n_parents)
    if tier == "ADD_ONE_OBSERVATION":
        return _bits(n_atoms) + OBSERVATION_ACQUISITION_BITS
    if tier == "LOCAL_PATCH":
        return patch_size * (_bits(n_cases) + _bits(n_decisions))
    if tier == "REPRESENTATION_CHANGE":
        return n_representation_terms * (_bits(3) + 2.0 * _bits(n_observables))
    if tier == "NEW_PRIMITIVE":
        return n_cases * (n_cases - 1) / 2.0 + _bits(n_relational_ops)
    raise ValueError(tier)


def mdl_total_bits(model_bits: float, residual_collisions: int) -> float:
    return model_bits + residual_collisions * RESIDUAL_PENALTY_BITS


# ---------------------------------------------------------------------------
# P4 -- finite model / countermodel search
# ---------------------------------------------------------------------------


def countermodel_of_functional_dependency(
    rows: Sequence[Mapping[str, str]], determiners: Sequence[str], target: str
) -> tuple[int, int] | None:
    """First witness that `determiners -> target` fails, or None."""

    for i, j in combinations(range(len(rows)), 2):
        if all(rows[i][key] == rows[j][key] for key in determiners) and rows[i][target] != rows[j][target]:
            return (i, j)
    return None


# ---------------------------------------------------------------------------
# P6 -- AGM-style base revision with exceptions
# ---------------------------------------------------------------------------


def kernel_contraction(base: frozenset[str], kernels: Sequence[frozenset[str]]) -> frozenset[str]:
    """Hansson kernel contraction with an incision function taking one element
    of each kernel (canonical: the lexicographically greatest)."""

    incisions = {max(kernel) for kernel in kernels if kernel}
    return frozenset(base - incisions)


# ---------------------------------------------------------------------------
# Native known-answer selftests (must all pass before any parent is used)
# ---------------------------------------------------------------------------


def _check(results: list[dict[str, Any]], parent: str, name: str, ok: bool, detail: str = "") -> None:
    results.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})


def fidelity_selftests() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    # --- LGG / anti-unification (Plotkin 1970) ------------------------------
    _check(results, "LGG", "plotkin_lgg_pair_classic",
           lgg_pair(("a", "b", "a"), ("a", "c", "a")) == ("a", VARIABLE, "a"))
    _check(results, "LGG", "lgg_identical_is_identity",
           lgg_pair(("a", "b"), ("a", "b")) == ("a", "b"))
    _check(results, "LGG", "lgg_disjoint_is_all_variables",
           lgg_pair(("a", "b"), ("c", "d")) == (VARIABLE, VARIABLE))
    _check(results, "LGG", "lgg_set_is_iterated_pair",
           lgg_set((("a", "b", "c"), ("a", "b", "d"), ("a", "e", "d"))) == ("a", VARIABLE, VARIABLE))
    _check(results, "LGG", "lgg_subsumes_every_input",
           all(subsumes(lgg_set((("a", "b"), ("a", "c"))), row) for row in (("a", "b"), ("a", "c"))))
    _check(results, "LGG", "subsumption_rejects_constant_mismatch",
           not subsumes(("a", VARIABLE), ("b", "c")))
    _check(results, "LGG", "lgg_is_least_general_exhaustive",
           lgg_is_least_general((("a", "b"), ("a", "c")), ("a", "b", "c")))
    _check(results, "LGG", "lgg_arity_mismatch_raises",
           _raises(lambda: lgg_pair(("a",), ("a", "b"))))
    _check(results, "LGG", "lgg_empty_set_raises", _raises(lambda: lgg_set(())))

    # --- FCA (Ganter & Wille) ----------------------------------------------
    # Classic 4-object / 4-attribute context (the "living beings" toy context).
    ctx = FormalContext(
        objects=("leech", "bream", "frog", "dog"),
        attributes=("water", "land", "limbs", "milk"),
        incidence=frozenset(
            {
                ("leech", "water"),
                ("bream", "water"),
                ("frog", "water"),
                ("frog", "land"),
                ("frog", "limbs"),
                ("dog", "land"),
                ("dog", "limbs"),
                ("dog", "milk"),
            }
        ),
    )
    _check(results, "FCA", "object_intent", ctx.object_intent("frog") == frozenset({"water", "land", "limbs"}))
    _check(results, "FCA", "attribute_extent", ctx.attribute_extent("water") == frozenset({"leech", "bream", "frog"}))
    _check(results, "FCA", "derivation_of_empty_object_set_is_all_attributes",
           ctx.derive_objects(()) == frozenset(ctx.attributes))
    _check(results, "FCA", "derivation_of_empty_attribute_set_is_all_objects",
           ctx.derive_attributes(()) == frozenset(ctx.objects))
    _check(results, "FCA", "closure_is_extensive",
           frozenset({"frog"}) <= ctx.closure_objects({"frog"}))
    _check(results, "FCA", "closure_is_idempotent",
           ctx.closure_objects(ctx.closure_objects({"frog", "dog"})) == ctx.closure_objects({"frog", "dog"}))
    _check(results, "FCA", "closure_is_monotone",
           all(
               ctx.closure_objects(small) <= ctx.closure_objects(big)
               for small, big in (
                   ({"frog"}, {"frog", "dog"}),
                   ({"dog"}, {"dog", "frog"}),
                   (set(), {"leech"}),
                   ({"bream"}, {"bream", "leech", "frog"}),
               )
           ))
    _check(results, "FCA", "every_concept_is_a_fixed_point",
           all(ctx.derive_attributes(intent) == extent and ctx.derive_objects(extent) == intent
               for extent, intent in ctx.concepts()))
    _check(results, "FCA", "top_and_bottom_concepts_present",
           any(extent == frozenset(ctx.objects) for extent, _ in ctx.concepts())
           and any(intent == frozenset(ctx.attributes) for _, intent in ctx.concepts()))
    _check(results, "FCA", "implication_milk_implies_limbs", ctx.implication_holds(("milk",), ("limbs",)))
    _check(results, "FCA", "implication_limbs_does_not_imply_milk",
           not ctx.implication_holds(("limbs",), ("milk",)))
    _check(results, "FCA", "galois_adjunction_satisfied",
           galois_adjunction_witness(ctx) == "SATISFIED", galois_adjunction_witness(ctx))

    # --- MDL ----------------------------------------------------------------
    kwargs = dict(n_parents=4, n_atoms=4, n_cases=12, n_decisions=3, patch_size=2,
                  n_derived_terms=40, n_representation_terms=1, n_observables=5,
                  n_relational_ops=2)
    _check(results, "MDL", "no_change_costs_nothing", mdl_model_bits("NO_CHANGE", **kwargs) == 0.0)
    _check(results, "MDL", "parent_costs_only_its_name",
           abs(mdl_model_bits("PARENT_FORMALISM_SUFFICIENT", **kwargs) - 2.0) < 1e-9)
    _check(results, "MDL", "new_primitive_costs_its_extension",
           abs(mdl_model_bits("NEW_PRIMITIVE", **kwargs) - (66.0 + 1.0)) < 1e-9)
    _check(results, "MDL", "residual_collisions_dominate",
           mdl_total_bits(0.0, 1) > mdl_total_bits(mdl_model_bits("LOCAL_PATCH", **kwargs), 0))
    _check(results, "MDL", "code_is_monotone_in_residuals",
           mdl_total_bits(5.0, 3) > mdl_total_bits(5.0, 2) > mdl_total_bits(5.0, 1))
    _check(results, "MDL", "patch_cost_grows_with_patch_size",
           mdl_model_bits("LOCAL_PATCH", **{**kwargs, "patch_size": 3})
           > mdl_model_bits("LOCAL_PATCH", **kwargs))
    _check(results, "MDL", "native_order_differs_from_registered_order",
           mdl_model_bits("REPRESENTATION_CHANGE", **kwargs)
           < mdl_model_bits("LOCAL_PATCH", **kwargs),
           "MDL prefers a derived term to a two-case patch; the registered "
           "search order prefers the patch. The disagreement is reported, not repaired.")

    # --- model / countermodel search ---------------------------------------
    rows = [
        {"a": "0", "b": "0", "J": "d0"},
        {"a": "0", "b": "1", "J": "d1"},
        {"a": "1", "b": "0", "J": "d0"},
    ]
    _check(results, "MODEL_SEARCH", "countermodel_found_for_a_determines_J",
           countermodel_of_functional_dependency(rows, ("a",), "J") == (0, 1))
    _check(results, "MODEL_SEARCH", "no_countermodel_for_ab_determines_J",
           countermodel_of_functional_dependency(rows, ("a", "b"), "J") is None)
    _check(results, "MODEL_SEARCH", "empty_determiner_set_finds_first_disagreement",
           countermodel_of_functional_dependency(rows, (), "J") == (0, 1))
    _check(results, "MODEL_SEARCH", "constant_target_has_no_countermodel",
           countermodel_of_functional_dependency(
               [{"a": "0", "J": "d0"}, {"a": "1", "J": "d0"}], ("a",), "J") is None)

    # --- conservative extension (ORION reference semantics) -----------------
    old = FiniteConsequenceTheory("T", frozenset({"p", "q"}), frozenset({"p"}))
    same = FiniteConsequenceTheory("T+", frozenset({"p", "q", "r"}), frozenset({"p", "r"}))
    nonc = FiniteConsequenceTheory("T+", frozenset({"p", "q", "r"}), frozenset({"p", "q", "r"}))
    lost = FiniteConsequenceTheory("T+", frozenset({"p", "q", "r"}), frozenset({"r"}))
    _check(results, "CONSERVATIVE", "conservative_case",
           assess_conservative_extension(old, same).status is ConservativeExtensionStatus.CONSERVATIVE)
    _check(results, "CONSERVATIVE", "nonconservative_case",
           assess_conservative_extension(old, nonc).status
           is ConservativeExtensionStatus.NONCONSERVATIVE_NEW_OLD_LANGUAGE_CONSEQUENCE)
    _check(results, "CONSERVATIVE", "lost_old_consequence_case",
           assess_conservative_extension(old, lost).status
           is ConservativeExtensionStatus.LOST_OLD_LANGUAGE_CONSEQUENCE)
    _check(results, "CONSERVATIVE", "shrinking_language_cannot_check",
           assess_conservative_extension(
               old, FiniteConsequenceTheory("T-", frozenset({"p"}), frozenset({"p"}))
           ).status is ConservativeExtensionStatus.CANNOT_CHECK)
    _check(results, "CONSERVATIVE", "checks_are_non_authorizing",
           assess_conservative_extension(old, same).authority_granted is False)

    # --- AGM-style base revision -------------------------------------------
    base = frozenset({"p", "q", "r"})
    _check(results, "THEORY_REVISION", "kernel_contraction_removes_one_per_kernel",
           kernel_contraction(base, [frozenset({"p", "q"})]) == frozenset({"p", "r"}))
    _check(results, "THEORY_REVISION", "contraction_is_inclusive",
           kernel_contraction(base, [frozenset({"p", "q"})]) <= base)
    _check(results, "THEORY_REVISION", "vacuity_no_kernel_no_change",
           kernel_contraction(base, []) == base)
    _check(results, "THEORY_REVISION", "two_kernels_two_incisions",
           kernel_contraction(base, [frozenset({"p", "q"}), frozenset({"r"})]) == frozenset({"p"}))
    _check(results, "THEORY_REVISION", "empty_kernel_is_ignored",
           kernel_contraction(base, [frozenset()]) == base)
    return results


def _raises(thunk) -> bool:
    try:
        thunk()
    except Exception:
        return True
    return False


PARENT_NAMES = ("LGG", "FCA", "MDL", "MODEL_SEARCH", "CONSERVATIVE", "THEORY_REVISION")
