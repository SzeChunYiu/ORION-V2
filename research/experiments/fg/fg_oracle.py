"""FG series exact oracle: two independent computations of the cheapest repair.

The oracle answers one question exactly, by exhaustion: given the registered
case set `X`, decision family `J`, active formalism `F`, registered parent
formalism library `L`, observable set and relational structures, **what is the
cheapest tier of the §L5 search order that resolves every collision of `C_F`?**

Two independent implementations run on every instance and must agree (gate
G0b):

* `tier_search`   -- signature-bucket collisions + bitmask cover over the
  required-pair set + subset enumeration for the patch tier;
* `tier_search_partition` -- set-partition meet semantics: a repair resolves
  iff no block of the common refinement holds two cases with different
  decisions; the patch tier is decided from the *kept* set instead of the cover.

Neither implementation imports `orion_v2.formalism_genesis`; no arm imports
this module.  Agreement between the oracle and `M`'s mechanism is necessary,
not sufficient, for a residual (cf. ME-X4 design §9(5)).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Sequence

from fg_model import (
    ADD_ONE_OBSERVATION,
    LOCAL_PATCH,
    NEW_PRIMITIVE,
    NO_CHANGE,
    PARENT_FORMALISM_SUFFICIENT,
    REPRESENTATION_CHANGE,
    Instance,
    derived_term_space,
    evaluate_term,
    relational_term_space,
    signatures,
)

MAX_REPRESENTATION_TERMS = 2


# ---------------------------------------------------------------------------
# Method A primitives: signature buckets + required-pair bitmasks
# ---------------------------------------------------------------------------


def collisions_by_bucket(instance: Instance, term_ids: Sequence[str]) -> tuple[tuple[str, str], ...]:
    """Collision set C computed by bucketing cases on their signature."""

    sig = signatures(term_ids, instance)
    buckets: dict[tuple[str, ...], list[str]] = {}
    for case in instance.cases:
        buckets.setdefault(sig[case.case_id], []).append(case.case_id)
    decision = {case.case_id: case.decision_id for case in instance.cases}
    out: list[tuple[str, str]] = []
    for members in buckets.values():
        for left, right in combinations(sorted(members), 2):
            if decision[left] != decision[right]:
                out.append((left, right))
    return tuple(sorted(out))


def collisions_by_pairwise(instance: Instance, term_ids: Sequence[str]) -> tuple[tuple[str, str], ...]:
    """Collision set C computed by an independent pairwise scan."""

    columns = {term_id: evaluate_term(term_id, instance) for term_id in term_ids}
    decision = {case.case_id: case.decision_id for case in instance.cases}
    ids = sorted(decision)
    out: list[tuple[str, str]] = []
    for left, right in combinations(ids, 2):
        if decision[left] == decision[right]:
            continue
        if all(columns[t][left] == columns[t][right] for t in term_ids):
            out.append((left, right))
    return tuple(sorted(out))


def _pair_index(pairs: Sequence[tuple[str, str]]) -> dict[tuple[str, str], int]:
    return {pair: index for index, pair in enumerate(pairs)}


def _cover_mask(term_id: str, instance: Instance, pairs: Sequence[tuple[str, str]]) -> int:
    """Bit i set iff `term_id` takes different values on pair i (separates it)."""

    column = evaluate_term(term_id, instance)
    mask = 0
    for index, (left, right) in enumerate(pairs):
        if column[left] != column[right]:
            mask |= 1 << index
    return mask


# ---------------------------------------------------------------------------
# Method B primitives: set partitions
# ---------------------------------------------------------------------------


def partition_of(term_ids: Sequence[str], instance: Instance) -> tuple[frozenset[str], ...]:
    sig = signatures(term_ids, instance)
    blocks: dict[tuple[str, ...], set[str]] = {}
    for case in instance.cases:
        blocks.setdefault(sig[case.case_id], set()).add(case.case_id)
    return tuple(sorted((frozenset(block) for block in blocks.values()), key=lambda b: sorted(b)))


def partition_resolves(
    term_ids: Sequence[str],
    instance: Instance,
    restricted_to: frozenset[str] | None = None,
) -> bool:
    """True iff no block of the common refinement mixes two decisions."""

    decision = {case.case_id: case.decision_id for case in instance.cases}
    for block in partition_of(term_ids, instance):
        members = block if restricted_to is None else block & restricted_to
        if len({decision[case_id] for case_id in members}) > 1:
            return False
    return True


# ---------------------------------------------------------------------------
# Tier verdicts
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TierVerdict:
    terminal: str
    witness: tuple[str, ...]
    collisions: tuple[tuple[str, str], ...]
    feasible_tiers: tuple[str, ...]
    candidates_evaluated: tuple[tuple[str, int], ...]
    near_miss_counts: tuple[tuple[str, int], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "terminal": self.terminal,
            "witness": list(self.witness),
            "collisions": [list(pair) for pair in self.collisions],
            "feasible_tiers": list(self.feasible_tiers),
            "candidates_evaluated": {name: count for name, count in self.candidates_evaluated},
            "near_miss_counts": {name: count for name, count in self.near_miss_counts},
        }


def _parent_candidates(instance: Instance) -> list[tuple[str, tuple[str, ...]]]:
    return [(f.formalism_id, f.term_ids) for f in instance.parent_formalisms]


def _single_atom_candidates(instance: Instance) -> list[str]:
    active = set(instance.active_formalism.term_ids)
    return [term for term in instance.all_atoms() if term not in active]


def tier_search(instance: Instance) -> TierVerdict:
    """Method A. Exhaustive, cost-ordered; returns the cheapest feasible tier."""

    active = tuple(instance.active_formalism.term_ids)
    collisions = collisions_by_bucket(instance, active)
    evaluated: list[tuple[str, int]] = []
    near_miss: list[tuple[str, int]] = []
    feasible: list[str] = []
    witness: tuple[str, ...] = ()

    if not collisions:
        evaluated.append((NO_CHANGE, 1))
        return TierVerdict(NO_CHANGE, (), collisions, (NO_CHANGE,), tuple(evaluated), tuple(near_miss))

    full = (1 << len(collisions)) - 1

    # tier 1: an existing registered parent formalism
    parents = _parent_candidates(instance)
    evaluated.append((PARENT_FORMALISM_SUFFICIENT, len(parents)))
    parent_hits = [
        name for name, terms in parents if not collisions_by_bucket(instance, terms)
    ]
    parent_near = sum(
        1 for name, terms in parents if len(collisions_by_bucket(instance, terms)) == 1
    )
    near_miss.append((PARENT_FORMALISM_SUFFICIENT, parent_near))
    if parent_hits:
        feasible.append(PARENT_FORMALISM_SUFFICIENT)
        witness = witness or (f"parent={sorted(parent_hits)[0]}",)

    # tier 2: one missing variable/observation (a single atom added to F)
    atoms = _single_atom_candidates(instance)
    evaluated.append((ADD_ONE_OBSERVATION, len(atoms)))
    atom_masks = {term: _cover_mask(term, instance, collisions) for term in atoms}
    atom_hits = [term for term, mask in atom_masks.items() if mask == full]
    near_miss.append(
        (
            ADD_ONE_OBSERVATION,
            sum(1 for mask in atom_masks.values() if bin(full ^ mask).count("1") == 1),
        )
    )
    if atom_hits:
        feasible.append(ADD_ONE_OBSERVATION)
        witness = witness or (f"observation={sorted(atom_hits)[0]}",)

    # tier 3: a local patch / scope condition (a vertex cover of the collision graph)
    vertices = sorted({case_id for pair in collisions for case_id in pair})
    patch_hits: list[tuple[str, ...]] = []
    patch_evaluated = 0
    for size in range(1, instance.patch_budget + 1):
        for subset in combinations(vertices, size):
            patch_evaluated += 1
            chosen = set(subset)
            if all(left in chosen or right in chosen for left, right in collisions):
                patch_hits.append(subset)
        if patch_hits:
            break
    over_budget_cover = 0
    if not patch_hits:
        for subset in combinations(vertices, min(instance.patch_budget + 1, len(vertices))):
            chosen = set(subset)
            if all(left in chosen or right in chosen for left, right in collisions):
                over_budget_cover = 1
                break
    evaluated.append((LOCAL_PATCH, patch_evaluated))
    near_miss.append((LOCAL_PATCH, over_budget_cover))
    if patch_hits:
        feasible.append(LOCAL_PATCH)
        witness = witness or (f"patch={'+'.join(sorted(patch_hits[0]))}",)

    # tier 4: representation change (<= 2 derived terms over recorded observables)
    derived_terms = derived_term_space(instance)
    derived_masks = {term: _cover_mask(term, instance, collisions) for term in derived_terms}
    single = [term for term, mask in derived_masks.items() if mask == full]
    pair_hits: list[tuple[str, str]] = []
    pair_evaluated = 0
    if not single and MAX_REPRESENTATION_TERMS >= 2:
        items = sorted(derived_masks.items())
        for (left, left_mask), (right, right_mask) in combinations(items, 2):
            pair_evaluated += 1
            if left_mask | right_mask == full:
                pair_hits.append((left, right))
                break
    evaluated.append((REPRESENTATION_CHANGE, len(derived_terms) + pair_evaluated))
    near_miss.append(
        (
            REPRESENTATION_CHANGE,
            sum(1 for mask in derived_masks.values() if bin(full ^ mask).count("1") == 1),
        )
    )
    if single or pair_hits:
        feasible.append(REPRESENTATION_CHANGE)
        chosen_terms = (sorted(single)[0],) if single else pair_hits[0]
        witness = witness or tuple(f"representation={t}" for t in chosen_terms)

    # tier 5: a candidate new primitive (a relational primitive + derived operation)
    relational_terms = relational_term_space(instance)
    evaluated.append((NEW_PRIMITIVE, len(relational_terms)))
    relational_masks = {t: _cover_mask(t, instance, collisions) for t in relational_terms}
    relational_hits = [t for t, mask in relational_masks.items() if mask == full]
    near_miss.append(
        (
            NEW_PRIMITIVE,
            sum(1 for mask in relational_masks.values() if bin(full ^ mask).count("1") == 1),
        )
    )
    if relational_hits:
        feasible.append(NEW_PRIMITIVE)
        witness = witness or (f"primitive={sorted(relational_hits)[0]}",)

    terminal = feasible[0] if feasible else "UNRESOLVABLE_BY_REGISTERED_REPAIRS"
    return TierVerdict(terminal, witness, collisions, tuple(feasible), tuple(evaluated), tuple(near_miss))


def tier_search_partition(instance: Instance) -> TierVerdict:
    """Method B. Same ladder, computed through set-partition meets only."""

    active = tuple(instance.active_formalism.term_ids)
    collisions = collisions_by_pairwise(instance, active)
    all_ids = frozenset(case.case_id for case in instance.cases)
    evaluated: list[tuple[str, int]] = []
    feasible: list[str] = []
    witness: tuple[str, ...] = ()

    if partition_resolves(active, instance):
        evaluated.append((NO_CHANGE, 1))
        return TierVerdict(NO_CHANGE, (), collisions, (NO_CHANGE,), tuple(evaluated), ())

    parents = _parent_candidates(instance)
    evaluated.append((PARENT_FORMALISM_SUFFICIENT, len(parents)))
    hits = [name for name, terms in parents if partition_resolves(terms, instance)]
    if hits:
        feasible.append(PARENT_FORMALISM_SUFFICIENT)
        witness = witness or (f"parent={sorted(hits)[0]}",)

    atoms = _single_atom_candidates(instance)
    evaluated.append((ADD_ONE_OBSERVATION, len(atoms)))
    atom_hits = [t for t in atoms if partition_resolves(active + (t,), instance)]
    if atom_hits:
        feasible.append(ADD_ONE_OBSERVATION)
        witness = witness or (f"observation={sorted(atom_hits)[0]}",)

    # patch decided from the *kept* set, not from the cover
    vertices = sorted({case_id for pair in collisions for case_id in pair})
    patch_evaluated = 0
    patch_hit: tuple[str, ...] | None = None
    for size in range(1, instance.patch_budget + 1):
        for dropped in combinations(vertices, size):
            patch_evaluated += 1
            kept = all_ids - set(dropped)
            if partition_resolves(active, instance, restricted_to=kept):
                patch_hit = dropped
                break
        if patch_hit is not None:
            break
    evaluated.append((LOCAL_PATCH, patch_evaluated))
    if patch_hit is not None:
        feasible.append(LOCAL_PATCH)
        witness = witness or (f"patch={'+'.join(sorted(patch_hit))}",)

    derived_terms = derived_term_space(instance)
    single = [t for t in derived_terms if partition_resolves(active + (t,), instance)]
    pair_hit: tuple[str, str] | None = None
    pair_evaluated = 0
    if not single:
        for left, right in combinations(derived_terms, 2):
            pair_evaluated += 1
            if partition_resolves(active + (left, right), instance):
                pair_hit = (left, right)
                break
    evaluated.append((REPRESENTATION_CHANGE, len(derived_terms) + pair_evaluated))
    if single or pair_hit is not None:
        feasible.append(REPRESENTATION_CHANGE)
        chosen = (sorted(single)[0],) if single else pair_hit
        witness = witness or tuple(f"representation={t}" for t in chosen)

    relational_terms = relational_term_space(instance)
    evaluated.append((NEW_PRIMITIVE, len(relational_terms)))
    relational_hits = [t for t in relational_terms if partition_resolves(active + (t,), instance)]
    if relational_hits:
        feasible.append(NEW_PRIMITIVE)
        witness = witness or (f"primitive={sorted(relational_hits)[0]}",)

    terminal = feasible[0] if feasible else "UNRESOLVABLE_BY_REGISTERED_REPAIRS"
    return TierVerdict(terminal, witness, collisions, tuple(feasible), tuple(evaluated), ())


def oracle_agrees(instance: Instance) -> tuple[bool, TierVerdict, TierVerdict]:
    a = tier_search(instance)
    b = tier_search_partition(instance)
    same = (
        a.terminal == b.terminal
        and a.collisions == b.collisions
        and a.feasible_tiers == b.feasible_tiers
    )
    return same, a, b
