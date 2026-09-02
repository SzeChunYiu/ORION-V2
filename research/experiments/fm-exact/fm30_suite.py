#!/usr/bin/env python3
"""FM30 — formal concept closure and revision: exact study.

Computing a Galois closure is deliberately **not** the endpoint.  The
Ganter-Wille derivation operators decide it exactly, so a study built on it
would report parent sufficiency by construction.  Each instance instead presents

    K0    a formal context, with two tracked concepts c1, c2,
    K1    a revision of K0 (new objects, new attributes, or both),
    h     a hidden object added in K1 whose membership must be predicted,

and asks for a **registered transition class, an old-valid-case retention
verdict, and the hidden case's membership** - the protocol's three FM30
primaries, scored together as one exact endpoint:

    NO_CHANGE     both tracked concepts survive the revision unchanged;
    SPECIALIZE    the tracked concept's intent strictly grows;
    SPLIT         the tracked extent is no longer a concept extent, and is
                  exactly the union of >= 2 maximal concept extents strictly
                  inside it;
    MERGE         the union of the two tracked extents becomes a concept extent
                  while neither contained the other before;
    BRIDGE        a new concept appears whose extent strictly intersects both
                  tracked extents without containing either.

Consequence, and the reason the suite is worth running: **no single parent owns
the endpoint.**  Galois closure gives the lattices but does not classify a
transition between them.  Attribute exploration (Ganter's algorithm) owns
implications and their counterexamples but says nothing about extent geometry.
A lattice-order/stability parent owns split and merge but is blind to whether a
counterexample invalidated an implication.  The strongest faithful comparator is
their federation under a pre-registered, outcome-blind rule.

Oracle validity rests on two independent algorithms agreeing on the concept
lattice of every context:

  * `concepts_powerset`  - close every object subset with the derivation
    operators and collect the distinct closed pairs;
  * `concepts_next_closure` - Ganter's NextClosure, enumerating closed
    *attribute* sets in lectic order without ever materialising the powerset.

They share only the derivation operators, which come from
`orion_v2.transfer_formal_mechanics`.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from itertools import combinations
from typing import Sequence

from fm_core import ArmSpec, PlantedPositive, SuiteSpec

from orion_v2.transfer_formal_mechanics import (
    FormalContext,
    derive_attributes,
    derive_objects,
    formal_concept_closure,
)

# --------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------

FAMILIES = ("NO_CHANGE", "SPECIALIZE", "SPLIT", "MERGE", "BRIDGE")
TRANSITIONS = FAMILIES


@dataclass(frozen=True)
class Instance:
    instance_id: str
    family: str
    seed: int
    k0: FormalContext
    k1: FormalContext
    tracked1: tuple[str, ...]  # extent of the first tracked concept in K0
    tracked2: tuple[str, ...]
    hidden_object: str

    def as_json(self) -> dict:
        def ctx(c: FormalContext) -> dict:
            return {
                "objects": list(c.objects),
                "attributes": list(c.attributes),
                "incidence": sorted([g, m] for g, m in c.incidence),
            }

        return {
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,
            "k0": ctx(self.k0),
            "k1": ctx(self.k1),
            "tracked1": list(self.tracked1),
            "tracked2": list(self.tracked2),
            "hidden_object": self.hidden_object,
        }


# --------------------------------------------------------------------------
# oracle 1 — powerset closure enumeration
# --------------------------------------------------------------------------


def concepts_powerset(ctx: FormalContext) -> set[tuple[frozenset, frozenset]]:
    """Every formal concept, by closing every object subset."""
    out: set[tuple[frozenset, frozenset]] = set()
    objs = list(ctx.objects)
    for r in range(len(objs) + 1):
        for sub in combinations(objs, r):
            intent = derive_attributes(ctx, sub)
            extent = derive_objects(ctx, intent)
            out.add((extent, intent))
    return out


# --------------------------------------------------------------------------
# oracle 2 — Ganter's NextClosure over attribute sets
# --------------------------------------------------------------------------


def _closure_attrs(ctx: FormalContext, attrs: frozenset) -> frozenset:
    return derive_attributes(ctx, derive_objects(ctx, attrs))


def concepts_next_closure(ctx: FormalContext) -> set[tuple[frozenset, frozenset]]:
    """Ganter's NextClosure: closed attribute sets in lectic order.

    Independent of the powerset method: it walks from one closed set to the
    lectically next one without ever enumerating all subsets.
    """
    M = list(ctx.attributes)
    out: set[tuple[frozenset, frozenset]] = set()
    cur = _closure_attrs(ctx, frozenset())
    while True:
        out.add((derive_objects(ctx, cur), cur))
        nxt = None
        for i in range(len(M) - 1, -1, -1):
            m = M[i]
            if m in cur:
                cur = frozenset(x for x in cur if x != m)
                continue
            cand = _closure_attrs(ctx, cur | {m})
            # lectic test: nothing below m may be added by the closure
            if all(x in cur or x == m for x in cand if M.index(x) < i + 1):
                if not any(M.index(x) < i and x not in cur for x in cand):
                    nxt = cand
                    break
        if nxt is None:
            return out
        cur = nxt


def lattice_agrees(ctx: FormalContext) -> bool:
    return concepts_powerset(ctx) == concepts_next_closure(ctx)


# --------------------------------------------------------------------------
# exact transition classification
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class OracleAnswer:
    transition: str
    retention_ok: bool
    hidden_in_extent: bool
    n_concepts_k0: int
    n_concepts_k1: int
    predicates_holding: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "transition": self.transition,
            "retention_ok": self.retention_ok,
            "hidden_in_extent": self.hidden_in_extent,
            "n_concepts_k0": self.n_concepts_k0,
            "n_concepts_k1": self.n_concepts_k1,
            "predicates_holding": list(self.predicates_holding),
        }

    @property
    def disposition(self) -> str:
        return self.transition


def _extents(ctx: FormalContext) -> set[frozenset]:
    return {e for e, _ in concepts_powerset(ctx)}


def _maximal_proper_subextents(extents: set[frozenset], A: frozenset) -> list[frozenset]:
    inside = [e for e in extents if e and e < A]
    return [e for e in inside if not any(e < f for f in inside)]


def _restrict(ctx: FormalContext, objects: Sequence[str]) -> FormalContext:
    """K1 restricted to the objects that already existed in K0.

    The transition class is a statement about how the *existing* concepts move,
    so it is computed on this restriction.  Without it, the hidden object - which
    by construction carries the tracked intent - joins the tracked extent and
    destroys it as an extent in every family at once, which is an artifact of the
    probe rather than a property of the revision.  The hidden object's membership
    is a separate registered primary and is computed on the full K1.
    """
    keep = set(objects)
    return FormalContext(
        objects=tuple(g for g in ctx.objects if g in keep),
        attributes=ctx.attributes,
        incidence=frozenset((g, m) for g, m in ctx.incidence if g in keep),
    )


# Registered precedence, frozen before any outcome.  More than one predicate can
# hold on a single revision (adding an attribute that covers a union both merges
# and specializes), so the class is the highest-precedence predicate that holds
# and the full hold-set is published in the oracle answer.  Fixture KA-09 pins it.
PRECEDENCE = ("SPLIT", "MERGE", "BRIDGE", "SPECIALIZE", "NO_CHANGE")


def classify_transition(inst: Instance) -> tuple[str, list[str]]:
    """Exact transition class, plus every class whose predicate also holds."""
    k0 = inst.k0
    k1 = _restrict(inst.k1, k0.objects)
    A1, A2 = frozenset(inst.tracked1), frozenset(inst.tracked2)
    B1_before = derive_attributes(k0, A1)
    B1_after = derive_attributes(k1, A1)
    E0, E1 = _extents(k0), _extents(k1)
    hold: list[str] = []

    # SPLIT: the tracked concept becomes internally differentiated - K1 has at
    # least two maximal concept extents strictly inside the tracked extent where
    # K0 had at most one.  (Requiring the tracked extent to stop being closed
    # would be wrong: adding an attribute to part of it leaves the whole still
    # closed, and requiring the sub-extents to cover it would be wrong too, since
    # an object with no distinguishing attribute normally belongs to none.)
    if len(_maximal_proper_subextents(E1, A1)) >= 2 > len(
        _maximal_proper_subextents(E0, A1)
    ):
        hold.append("SPLIT")

    # MERGE: the union of two incomparable tracked extents becomes closed,
    # having not been closed before
    if not (A1 <= A2 or A2 <= A1) and (A1 | A2) not in E0 and (A1 | A2) in E1:
        hold.append("MERGE")

    # BRIDGE: a new concept extent strictly intersects both tracked extents
    # without containing either
    for e in E1 - E0:
        if e & A1 and e & A2 and not (A1 <= e) and not (A2 <= e):
            hold.append("BRIDGE")
            break

    # SPECIALIZE: the tracked intent strictly grows
    if B1_after > B1_before:
        hold.append("SPECIALIZE")

    # NO_CHANGE: both tracked concepts survive with the same extent and intent
    if (
        A1 in E1
        and A2 in E1
        and B1_after == B1_before
        and derive_attributes(k1, A2) == derive_attributes(k0, A2)
    ):
        hold.append("NO_CHANGE")

    ordered = [c for c in PRECEDENCE if c in hold]
    return (ordered[0] if ordered else "NO_CHANGE"), ordered


def oracle_exhaustive(inst: Instance) -> OracleAnswer:
    transition, hold = classify_transition(inst)
    A1 = frozenset(inst.tracked1)
    B1 = derive_attributes(inst.k0, A1)
    # Old-valid-case retention: every member of the tracked extent must still
    # satisfy the concept's defining intent after the revision.  Defining it as
    # "the survivors are still covered" would be tautological - the survivors are
    # covered by construction - so the registered property is that there ARE no
    # casualties.  A revision that retracts an incidence pair can make it false.
    still_valid = {g for g in A1 if all((g, m) in inst.k1.incidence for m in B1)}
    revised_extent = derive_objects(inst.k1, B1)
    retention_ok = still_valid == A1
    hidden_in = inst.hidden_object in revised_extent
    return OracleAnswer(
        transition,
        retention_ok,
        hidden_in,
        len(concepts_powerset(inst.k0)),
        len(concepts_powerset(inst.k1)),
        tuple(hold),
    )


def oracle_cross_check(inst: Instance) -> OracleAnswer:
    """Same classification, but every lattice computed by NextClosure."""
    if not (lattice_agrees(inst.k0) and lattice_agrees(inst.k1)):
        return OracleAnswer("LATTICE_DISAGREEMENT", False, False, -1, -1, ())
    ans = oracle_exhaustive(inst)
    return OracleAnswer(
        ans.transition,
        ans.retention_ok,
        ans.hidden_in_extent,
        len(concepts_next_closure(inst.k0)),
        len(concepts_next_closure(inst.k1)),
        ans.predicates_holding,
    )


def endpoint_of(ans: OracleAnswer) -> str:
    return f"{ans.transition}|{int(ans.retention_ok)}{int(ans.hidden_in_extent)}"


# --------------------------------------------------------------------------
# generator
# --------------------------------------------------------------------------

OBJECTS = ("g1", "g2", "g3", "g4", "g5")
ATTRIBUTES = ("m1", "m2", "m3", "m4")


def _ctx(objects: Sequence[str], attributes: Sequence[str], inc: set) -> FormalContext:
    return FormalContext(
        objects=tuple(objects),
        attributes=tuple(attributes),
        incidence=frozenset(inc),
    )


def _generate_one(family: str, seed: int, idx: int) -> Instance | None:
    rng = random.Random(seed)
    objs = list(OBJECTS[: rng.randint(4, 5)])
    attrs = list(ATTRIBUTES)
    inc = {(g, m) for g in objs for m in attrs if rng.random() < 0.45}
    k0 = _ctx(objs, attrs, inc)

    extents = sorted(
        (tuple(sorted(e)) for e in _extents(k0) if 1 <= len(e) < len(objs)),
        key=lambda t: (len(t), t),
    )
    if len(extents) < 2:
        return None
    A1 = rng.choice(extents)
    others = [e for e in extents if e != A1]
    if not others:
        return None
    A2 = rng.choice(others)

    hidden = "h1"
    new_objs = objs + [hidden]
    inc1 = set(inc)
    B1 = sorted(derive_attributes(k0, A1))

    if family == "NO_CHANGE":
        # the hidden object reproduces an existing row exactly
        model = rng.choice(objs)
        inc1 |= {(hidden, m) for m in attrs if (model, m) in inc}
    elif family == "SPECIALIZE":
        # a new attribute that exactly the tracked extent carries
        attrs = attrs + ["m5"]
        inc1 |= {(g, "m5") for g in A1}
        inc1 |= {(hidden, m) for m in B1}
    elif family == "SPLIT":
        # a new attribute carried by a proper non-empty part of the extent
        if len(A1) < 2:
            return None
        attrs = attrs + ["m5"]
        part = rng.sample(list(A1), rng.randint(1, len(A1) - 1))
        inc1 |= {(g, "m5") for g in part}
        inc1 |= {(hidden, m) for m in B1}
    elif family == "MERGE":
        # a new attribute carried by exactly the union of the two tracked extents
        union = set(A1) | set(A2)
        if len(union) >= len(objs):
            return None  # the union is the top concept; nothing to merge into
        attrs = attrs + ["m5"]
        inc1 |= {(g, "m5") for g in union}
        inc1 |= {(hidden, m) for m in B1}
    elif family == "BRIDGE":
        # a new attribute carried by part of each tracked extent and nothing else
        attrs = attrs + ["m5"]
        p1 = rng.sample(list(A1), 1)
        p2 = [g for g in A2 if g not in A1]
        if not p2:
            return None
        inc1 |= {(g, "m5") for g in p1 + p2[:1]}
        inc1 |= {(hidden, m) for m in B1}
    else:  # pragma: no cover
        raise ValueError(family)

    # A registered fraction of revisions retract one incidence pair from a
    # member of the tracked extent - the protocol's counterexample-driven
    # revision.  Without them old-valid-case retention would be true by
    # construction and its gate would have no denominator to evaluate.
    if B1 and rng.random() < 0.4:
        victim = rng.choice(sorted(A1))
        drop = rng.choice(B1)
        inc1.discard((victim, drop))

    k1 = _ctx(new_objs, attrs, inc1)
    return Instance(f"{family}-{idx:05d}", family, seed, k0, k1, A1, A2, hidden)


def generate_split(split: str, seed: str, per_family: dict[str, int]):
    """Generate (instance, oracle) pairs; the transition class is *verified*.

    An instance on which more than one class predicate holds is ambiguous, not a
    known-answer case: it is rejected and resampled.  Rejections are counted per
    family and published.
    """
    pairs: list[tuple[Instance, OracleAnswer]] = []
    rejects = {f: 0 for f in FAMILIES}
    for family in FAMILIES:
        want = per_family.get(family, 0)
        made = counter = 0
        while made < want:
            counter += 1
            if counter > 6000 * (want + 1):  # pragma: no cover
                raise RuntimeError(f"{split}/{family}: generator could not fill quota")
            s = int.from_bytes(
                hashlib.sha256(f"{seed}|{split}|{family}|{counter}".encode()).digest()[:8], "big"
            )
            inst = _generate_one(family, s, counter)
            if inst is None:
                rejects[family] += 1
                continue
            transition, _ = classify_transition(inst)
            if transition != family:
                rejects[family] += 1  # not the intended class under the registered precedence
                continue
            if not (lattice_agrees(inst.k0) and lattice_agrees(inst.k1)):
                rejects[family] += 1
                continue
            made += 1
            pairs.append((inst, oracle_exhaustive(inst)))
    return pairs, rejects


# --------------------------------------------------------------------------
# parents
# --------------------------------------------------------------------------


def _result(transition: str, retention: bool, hidden: bool) -> dict:
    return {
        "disposition": transition,
        "retention_ok": bool(retention),
        "hidden_in_extent": bool(hidden),
    }


def _retention_and_hidden(inst: Instance) -> tuple[bool, bool]:
    A1 = frozenset(inst.tracked1)
    B1 = derive_attributes(inst.k0, A1)
    still_valid = {g for g in A1 if all((g, m) in inst.k1.incidence for m in B1)}
    revised = derive_objects(inst.k1, B1)
    return still_valid == A1, inst.hidden_object in revised


def parent_galois_closure(inst: Instance) -> dict:
    """P1 — Ganter-Wille Galois closure.

    Owns the derivation operators exactly: it recomputes the tracked concept's
    closure in the revised context and reports specialization when the intent
    grows, no change otherwise.  It computes no extent geometry, so split, merge
    and bridge are outside its competence - its native boundary.
    """
    A1 = frozenset(inst.tracked1)
    B0 = derive_attributes(inst.k0, A1)
    B1 = derive_attributes(_restrict(inst.k1, inst.k0.objects), A1)
    ret, hid = _retention_and_hidden(inst)
    return _result("SPECIALIZE" if B1 > B0 else "NO_CHANGE", ret, hid)


def parent_lattice_order(inst: Instance) -> dict:
    """P2 — concept-lattice order / extent geometry.

    Owns split and merge: it compares the extent families of the two lattices.
    It does not inspect intents, so specialization is invisible to it and it
    reports NO_CHANGE there - its native boundary.
    """
    A1, A2 = frozenset(inst.tracked1), frozenset(inst.tracked2)
    k1 = _restrict(inst.k1, inst.k0.objects)
    E0, E1 = _extents(inst.k0), _extents(k1)
    ret, hid = _retention_and_hidden(inst)
    if len(_maximal_proper_subextents(E1, A1)) >= 2 > len(
        _maximal_proper_subextents(E0, A1)
    ):
        return _result("SPLIT", ret, hid)
    if not (A1 <= A2 or A2 <= A1) and (A1 | A2) not in E0 and (A1 | A2) in E1:
        return _result("MERGE", ret, hid)
    return _result("NO_CHANGE", ret, hid)


def parent_attribute_exploration(inst: Instance) -> dict:
    """P3 — attribute exploration (Ganter) / implication counterexamples.

    Owns the implication side: it checks whether any implication of K0 valid on
    the tracked concept is refuted by a new object in K1, which is what a bridge
    looks like from the implication view (a new attribute links two previously
    unrelated intents).  It computes no lattice, so split, merge and
    specialization are outside its competence.
    """
    A1, A2 = frozenset(inst.tracked1), frozenset(inst.tracked2)
    E0, E1 = _extents(inst.k0), _extents(_restrict(inst.k1, inst.k0.objects))
    ret, hid = _retention_and_hidden(inst)
    for e in E1 - E0:
        if e & A1 and e & A2 and not (A1 <= e) and not (A2 <= e):
            return _result("BRIDGE", ret, hid)
    return _result("NO_CHANGE", ret, hid)


def parent_fixed_lesson(inst: Instance) -> dict:
    """P0 — fixed-lesson injection.

    The frozen table the protocol requires: *a revision that adds an attribute
    specializes the concept; a revision that only adds objects leaves it
    unchanged.*  A real heuristic, no closure computation, no lattice.
    """
    ret, hid = _retention_and_hidden(inst)
    grew = len(inst.k1.attributes) > len(inst.k0.attributes)
    return _result("SPECIALIZE" if grew else "NO_CHANGE", ret, hid)


# --------------------------------------------------------------------------
# federation, mechanic, ablations, controls
# --------------------------------------------------------------------------


def federation(inst: Instance) -> dict:
    """F0 — strongest faithful parent federation, pre-registered and outcome-blind.

    Extent geometry is decided first because split and merge are structural
    facts about the lattice (P2); if it reports no change, the implication
    parent may report a bridge (P3); if neither fires, the closure parent
    decides specialization versus no change (P1).  No parent is consulted
    outside its native competence.
    """
    p2 = parent_lattice_order(inst)
    if p2["disposition"] != "NO_CHANGE":
        return {**p2, "source": "P2"}
    p3 = parent_attribute_exploration(inst)
    if p3["disposition"] != "NO_CHANGE":
        return {**p3, "source": "P3"}
    return {**parent_galois_closure(inst), "source": "P1"}


def mechanic_full(inst: Instance) -> dict:
    """M — ORION L3 conceptual development, full.

    **Independent implementation, deliberately.**  M never enumerates a concept
    lattice.  It works incrementally from the tracked concept outward, using the
    reference module's `formal_concept_closure` on seeds it chooses itself:

      1. reclose the tracked intent in K1 and compare intents (specialization);
      2. for each new attribute, close its object set and test whether the
         resulting concept cuts the tracked extent (split) or spans both tracked
         extents (bridge);
      3. close the union of the two tracked extents and test whether it is
         self-closed (merge);
      4. report old-valid-case retention and the hidden object's membership.

    Closing a handful of chosen seeds is not the same as enumerating the
    lattice, so M can miss a transition the geometry parent sees - which is what
    makes "the federation reproduces M" a measurement rather than an identity.
    """
    k0, k1 = inst.k0, inst.k1
    A1, A2 = frozenset(inst.tracked1), frozenset(inst.tracked2)
    ret, hid = _retention_and_hidden(inst)
    new_attrs = [m for m in k1.attributes if m not in set(k0.attributes)]

    # (2) internal differentiation, by closing one seed per attribute and
    # intersecting with the tracked extent.  This never enumerates a lattice:
    # it closes |M| chosen seeds.  Counting sub-concepts in BOTH contexts is
    # what catches a split formed by an old attribute together with a new one -
    # looking only at new attributes misses those, as an earlier draft did.
    def sub_concepts(ctx: FormalContext) -> set[frozenset]:
        out: set[frozenset] = set()
        for m in ctx.attributes:
            ext, _ = formal_concept_closure(ctx, attributes=[m])
            cut = ext & A1
            if not cut or not (cut < A1):
                continue
            # a cut only counts as a sub-concept if it is itself closed: an
            # attribute's extent intersected with the tracked extent need not be
            # a concept, and counting those over-fires SPLIT on bridges
            closed, _ = formal_concept_closure(ctx, objects=sorted(cut))
            if closed & A1 == cut:
                out.add(cut)
        return {e for e in out if not any(e < f for f in out)}

    before, after = sub_concepts(k0), sub_concepts(k1)
    if len(after) >= 2 > len(before):
        return _result("SPLIT", ret, hid)

    # bridge: a new attribute whose concept spans both tracked extents
    for m in new_attrs:
        ext, _ = formal_concept_closure(k1, attributes=[m])
        if ext & A1 and ext & A2 and not (A1 <= ext) and not (A2 <= ext):
            return _result("BRIDGE", ret, hid)

    # (3) merge: the union of the two tracked extents becomes self-closed,
    # having not been self-closed before.  A transition has to be a change: an
    # earlier draft omitted the "before" test and reported MERGE for concepts
    # that were already merged.
    if not (A1 <= A2 or A2 <= A1):
        union = A1 | A2
        before_ext, _ = formal_concept_closure(k0, objects=sorted(union))
        after_ext, _ = formal_concept_closure(k1, objects=sorted(union))
        if before_ext != union and after_ext & frozenset(k0.objects) == union:
            return _result("MERGE", ret, hid)

    # (1) specialization by reclosing the tracked intent
    if derive_attributes(k1, A1) > derive_attributes(k0, A1):
        return _result("SPECIALIZE", ret, hid)
    return _result("NO_CHANGE", ret, hid)


def ablation_minus_extent_geometry(inst: Instance) -> dict:
    """M without the split/merge tests."""
    ret, hid = _retention_and_hidden(inst)
    for m in [m for m in inst.k1.attributes if m not in set(inst.k0.attributes)]:
        ext, _ = formal_concept_closure(inst.k1, attributes=[m])
        A1, A2 = frozenset(inst.tracked1), frozenset(inst.tracked2)
        if ext & A1 and ext & A2 and not (A1 <= ext) and not (A2 <= ext):
            return _result("BRIDGE", ret, hid)
    if derive_attributes(inst.k1, frozenset(inst.tracked1)) > derive_attributes(
        inst.k0, frozenset(inst.tracked1)
    ):
        return _result("SPECIALIZE", ret, hid)
    return _result("NO_CHANGE", ret, hid)


def ablation_minus_bridge_detection(inst: Instance) -> dict:
    """M without the cross-concept bridge test."""
    full = mechanic_full(inst)
    if full["disposition"] == "BRIDGE":
        return {**full, "disposition": "NO_CHANGE"}
    return full


def ablation_minus_closure_recomputation(inst: Instance) -> dict:
    """M without reclosing the tracked intent (no specialization detection)."""
    full = mechanic_full(inst)
    if full["disposition"] == "SPECIALIZE":
        return {**full, "disposition": "NO_CHANGE"}
    return full


def ablation_minus_old_case_retention(inst: Instance) -> dict:
    """M without the old-valid-case retention check: reports retention blindly."""
    full = mechanic_full(inst)
    return {**full, "retention_ok": True}


def control_always_no_change(inst: Instance) -> dict:
    return _result("NO_CHANGE", True, False)


def control_always_specialize(inst: Instance) -> dict:
    return _result("SPECIALIZE", True, True)


def control_random(inst: Instance) -> dict:
    rng = random.Random(inst.seed ^ 0x5EED)
    return _result(rng.choice(TRANSITIONS), rng.random() < 0.5, rng.random() < 0.5)


ARM_FUNCTIONS = {
    "P0_FIXED_LESSON_INJECTION": parent_fixed_lesson,
    "P1_GALOIS_CLOSURE": parent_galois_closure,
    "P2_LATTICE_ORDER_GEOMETRY": parent_lattice_order,
    "P3_ATTRIBUTE_EXPLORATION": parent_attribute_exploration,
    "F0_PARENT_FEDERATION": federation,
    "M_F2_CONCEPTUAL_DEVELOPMENT_FULL": mechanic_full,
    "M_MINUS_EXTENT_GEOMETRY": ablation_minus_extent_geometry,
    "M_MINUS_BRIDGE_DETECTION": ablation_minus_bridge_detection,
    "M_MINUS_CLOSURE_RECOMPUTATION": ablation_minus_closure_recomputation,
    "M_MINUS_OLD_CASE_RETENTION": ablation_minus_old_case_retention,
    "C_ALWAYS_NO_CHANGE": control_always_no_change,
    "C_ALWAYS_SPECIALIZE": control_always_specialize,
    "C_RANDOM_TRANSITION": control_random,
}


def run_arm(arm: str, inst: Instance) -> dict:
    out = ARM_FUNCTIONS[arm](inst)
    return {
        "disposition": out["disposition"],
        "retention_ok": out["retention_ok"],
        "hidden_in_extent": out["hidden_in_extent"],
    }


def endpoint(record: dict) -> str:
    return (
        f"{record['disposition']}|"
        f"{int(record['retention_ok'])}{int(record['hidden_in_extent'])}"
    )


# --------------------------------------------------------------------------
# parent fidelity
# --------------------------------------------------------------------------


def parent_fidelity() -> list[dict]:
    R: list[dict] = []

    def check(parent: str, name: str, ok: bool, detail: str = "") -> None:
        R.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    # ---- Ganter-Wille derivation operators (reference module) -------------
    # The textbook four-object context.
    ctx = _ctx(
        ["g1", "g2", "g3", "g4"],
        ["m1", "m2", "m3"],
        {("g1", "m1"), ("g1", "m2"), ("g2", "m1"), ("g3", "m2"), ("g3", "m3"), ("g4", "m3")},
    )
    check(
        "P1_GALOIS_CLOSURE",
        "derivation_of_an_object_set_is_the_shared_attributes",
        derive_attributes(ctx, ["g1", "g2"]) == frozenset({"m1"}),
        str(sorted(derive_attributes(ctx, ["g1", "g2"]))),
    )
    check(
        "P1_GALOIS_CLOSURE",
        "derivation_of_an_attribute_set_is_the_common_objects",
        derive_objects(ctx, ["m2"]) == frozenset({"g1", "g3"}),
        str(sorted(derive_objects(ctx, ["m2"]))),
    )
    check(
        "P1_GALOIS_CLOSURE",
        "empty_object_set_derives_every_attribute",
        derive_attributes(ctx, []) == frozenset(ctx.attributes),
    )
    check(
        "P1_GALOIS_CLOSURE",
        "empty_attribute_set_derives_every_object",
        derive_objects(ctx, []) == frozenset(ctx.objects),
    )
    ext, intent = formal_concept_closure(ctx, objects=["g1"])
    check(
        "P1_GALOIS_CLOSURE",
        "closure_is_idempotent",
        formal_concept_closure(ctx, objects=sorted(ext)) == (ext, intent),
    )
    check(
        "P1_GALOIS_CLOSURE",
        "closure_is_extensive",
        frozenset({"g1"}) <= ext,
    )
    a, b = frozenset({"g1"}), frozenset({"g1", "g2"})
    check(
        "P1_GALOIS_CLOSURE",
        "derivation_is_antitone",
        derive_attributes(ctx, b) <= derive_attributes(ctx, a),
    )
    check(
        "P1_GALOIS_CLOSURE",
        "documented_boundary_no_extent_geometry",
        parent_galois_closure(
            Instance("KA", "SPLIT", 0, ctx, ctx, ("g1",), ("g2",), "g1")
        )["disposition"]
        == "NO_CHANGE",
        "scope note: the closure parent classifies only intent growth",
    )

    # ---- the two lattice algorithms must agree ---------------------------
    for name, c in [
        ("textbook", ctx),
        ("empty_incidence", _ctx(["g1", "g2"], ["m1"], set())),
        ("full_incidence", _ctx(["g1", "g2"], ["m1", "m2"], {("g1", "m1"), ("g1", "m2"), ("g2", "m1"), ("g2", "m2")})),
        ("chain", _ctx(["g1", "g2", "g3"], ["m1", "m2", "m3"], {("g1", "m1"), ("g1", "m2"), ("g1", "m3"), ("g2", "m2"), ("g2", "m3"), ("g3", "m3")})),
    ]:
        p, n = concepts_powerset(c), concepts_next_closure(c)
        check("ORACLE_PAIR", f"powerset_equals_next_closure_on_{name}", p == n, f"{len(p)} vs {len(n)}")

    check(
        "ORACLE_PAIR",
        "concept_lattice_of_the_textbook_context_has_the_expected_size",
        len(concepts_powerset(ctx)) == 7,
        str(len(concepts_powerset(ctx))),
    )

    # ---- P2 lattice order ------------------------------------------------
    split_k0 = _ctx(["g1", "g2", "g3"], ["m1"], {("g1", "m1"), ("g2", "m1"), ("g3", "m1")})
    # a genuine split needs TWO new sub-concepts inside the tracked extent: one
    # new attribute distinguishing only g1 leaves a single sub-extent, which is a
    # differentiation but not a split, and the first draft of this test asserted
    # the wrong thing until the parent disagreed with it
    split_k1 = _ctx(
        ["g1", "g2", "g3", "h1"],
        ["m1", "m2", "m3"],
        {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2"), ("g2", "m3"), ("h1", "m1")},
    )
    check(
        "P2_LATTICE_ORDER_GEOMETRY",
        "detects_a_split_of_a_tracked_extent",
        parent_lattice_order(
            Instance("KA", "SPLIT", 0, split_k0, split_k1, ("g1", "g2", "g3"), ("g1",), "h1")
        )["disposition"]
        == "SPLIT",
    )
    check(
        "P2_LATTICE_ORDER_GEOMETRY",
        "documented_boundary_blind_to_intent_growth",
        parent_lattice_order(
            Instance("KA", "SPECIALIZE", 0, ctx, ctx, ("g1",), ("g2",), "g1")
        )["disposition"]
        == "NO_CHANGE",
        "scope note: extent geometry never inspects intents",
    )

    # ---- P0 fixed lesson --------------------------------------------------
    check(
        "P0_FIXED_LESSON_INJECTION",
        "says_specialize_whenever_an_attribute_is_added",
        parent_fixed_lesson(
            Instance("KA", "SPLIT", 0, split_k0, split_k1, ("g1", "g2", "g3"), ("g1",), "h1")
        )["disposition"]
        == "SPECIALIZE",
    )
    check(
        "P0_FIXED_LESSON_INJECTION",
        "says_no_change_when_only_objects_are_added",
        parent_fixed_lesson(
            Instance(
                "KA", "NO_CHANGE", 0, split_k0,
                _ctx(["g1", "g2", "g3", "h1"], ["m1"], {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("h1", "m1")}),
                ("g1", "g2", "g3"), ("g1",), "h1",
            )
        )["disposition"]
        == "NO_CHANGE",
    )
    return R


# --------------------------------------------------------------------------
# hand-authored known-answer fixtures
# --------------------------------------------------------------------------


def known_answer_fixtures() -> list[dict]:
    F: list[dict] = []

    def add(name, family, k0, k1, t1, t2, hidden, expected):
        F.append(
            {
                "name": name,
                "instance": Instance(name, family, 0, k0, k1, t1, t2, hidden),
                "expected": expected,
            }
        )

    base = _ctx(
        ["g1", "g2", "g3"], ["m1", "m2"],
        {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2")},
    )
    # NO_CHANGE: the new object duplicates an existing row
    add(
        "KA-01-NO_CHANGE", "NO_CHANGE", base,
        _ctx(["g1", "g2", "g3", "h1"], ["m1", "m2"],
             {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2"), ("h1", "m1")}),
        ("g1", "g2", "g3"), ("g1",), "h1", "NO_CHANGE",
    )
    # SPECIALIZE: a new attribute carried by exactly the tracked extent
    add(
        "KA-02-SPECIALIZE", "SPECIALIZE", base,
        _ctx(["g1", "g2", "g3", "h1"], ["m1", "m2", "m3"],
             {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2"),
              ("g1", "m3"), ("g2", "m3"), ("g3", "m3"), ("h1", "m1"), ("h1", "m3")}),
        ("g1", "g2", "g3"), ("g1",), "h1", "SPECIALIZE",
    )
    # SPLIT: a new attribute carried by a proper part of the tracked extent
    add(
        "KA-03-SPLIT", "SPLIT", base,
        _ctx(["g1", "g2", "g3", "h1"], ["m1", "m2", "m3"],
             {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2"),
              ("g2", "m3"), ("h1", "m1")}),
        ("g1", "g2", "g3"), ("g1",), "h1", "SPLIT",
    )
    # MERGE: the union of two incomparable extents becomes closed
    merge_k0 = _ctx(
        ["g1", "g2", "g3", "g4"], ["m1", "m2", "m3"],
        {("g1", "m1"), ("g1", "m3"), ("g2", "m2"), ("g2", "m3"),
         ("g3", "m1"), ("g3", "m2"), ("g3", "m3"), ("g4", "m3")},
    )
    add(
        "KA-04-MERGE", "MERGE", merge_k0,
        _ctx(["g1", "g2", "g3", "g4", "h1"], ["m1", "m2", "m3", "m4"],
             {("g1", "m1"), ("g1", "m3"), ("g2", "m2"), ("g2", "m3"),
              ("g3", "m1"), ("g3", "m2"), ("g3", "m3"), ("g4", "m3"),
              ("g1", "m4"), ("g2", "m4"), ("g3", "m4"), ("h1", "m1"), ("h1", "m3")}),
        ("g1", "g3"), ("g2", "g3"), "h1", "MERGE",
    )
    # KA-09 pins the registered precedence: this revision satisfies BOTH the
    # merge and the specialize predicates, and the class is the higher-precedence
    # one while the full hold-set is published.
    add(
        "KA-09-PRECEDENCE_MERGE_OVER_SPECIALIZE", "MERGE", merge_k0,
        _ctx(["g1", "g2", "g3", "g4", "h1"], ["m1", "m2", "m3", "m4"],
             {("g1", "m1"), ("g1", "m3"), ("g2", "m2"), ("g2", "m3"),
              ("g3", "m1"), ("g3", "m2"), ("g3", "m3"), ("g4", "m3"),
              ("g1", "m4"), ("g2", "m4"), ("g3", "m4"), ("h1", "m3")}),
        ("g1", "g3"), ("g2", "g3"), "h1", "MERGE",
    )
    # BRIDGE: a new attribute linking parts of two tracked extents
    bridge_k0 = _ctx(
        ["g1", "g2", "g3", "g4"], ["m1", "m2"],
        {("g1", "m1"), ("g2", "m1"), ("g3", "m2"), ("g4", "m2")},
    )
    add(
        "KA-05-BRIDGE", "BRIDGE", bridge_k0,
        _ctx(["g1", "g2", "g3", "g4", "h1"], ["m1", "m2", "m3"],
             {("g1", "m1"), ("g2", "m1"), ("g3", "m2"), ("g4", "m2"),
              ("g1", "m3"), ("g3", "m3"), ("h1", "m1")}),
        ("g1", "g2"), ("g3", "g4"), "h1", "BRIDGE",
    )
    # closure/lattice edge cases
    add(
        "KA-06-EMPTY_INCIDENCE", "NO_CHANGE",
        _ctx(["g1", "g2"], ["m1"], set()),
        _ctx(["g1", "g2", "h1"], ["m1"], set()),
        ("g1", "g2"), ("g1",), "h1", "NO_CHANGE",
    )
    add(
        "KA-07-FULL_INCIDENCE", "NO_CHANGE",
        _ctx(["g1", "g2"], ["m1"], {("g1", "m1"), ("g2", "m1")}),
        _ctx(["g1", "g2", "h1"], ["m1"], {("g1", "m1"), ("g2", "m1"), ("h1", "m1")}),
        ("g1", "g2"), ("g1",), "h1", "NO_CHANGE",
    )
    add(
        "KA-08-SPECIALIZE_ON_A_SINGLETON", "SPECIALIZE", base,
        _ctx(["g1", "g2", "g3", "h1"], ["m1", "m2", "m3"],
             {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2"),
              ("g1", "m3"), ("h1", "m1"), ("h1", "m2"), ("h1", "m3")}),
        ("g1",), ("g2",), "h1", "SPECIALIZE",
    )
    return F


# --------------------------------------------------------------------------
# planted positives
# --------------------------------------------------------------------------


def planted_positives() -> list[PlantedPositive]:
    from fm_core import discrimination_gate

    P = [
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "a_broken_closure_operator_is_detected",
            "a deliberately non-idempotent 'closure' (one derivation instead of "
            "two) must produce a different concept set from NextClosure",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "wrong_expected_transition_is_detected",
            "a deliberately wrong expected transition must fail the comparison",
        ),
        PlantedPositive(
            "G2_ANTI_PERMISSIVENESS",
            "retention_violating_arm_is_detected",
            "M_MINUS_OLD_CASE_RETENTION must report retention_ok on an instance "
            "where the oracle says retention fails, if any such instance exists",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_ceiling_split_is_detected",
            "a synthetic all-ceiling per-arm table must FAIL the gate",
        ),
        PlantedPositive(
            "G3_MECHANISM_BY_OMISSION",
            "extent_geometry_ablation_loses_the_split_family",
            "M_MINUS_EXTENT_GEOMETRY must be wrong on a hand-built split where M "
            "is right",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "registered_precedence_is_exercised_and_the_hold_set_published",
            "a revision on which two transition predicates hold must be "
            "classified by the registered precedence, with the full hold-set "
            "published rather than the losing predicate silently dropped",
        ),
    ]

    ctx = _ctx(
        ["g1", "g2", "g3"], ["m1", "m2"],
        {("g1", "m1"), ("g2", "m1"), ("g3", "m1"), ("g1", "m2")},
    )

    def broken_concepts(c: FormalContext) -> set:
        # one derivation, not two: not a closure operator at all
        out = set()
        objs = list(c.objects)
        for r in range(len(objs) + 1):
            for sub in combinations(objs, r):
                out.add((frozenset(sub), derive_attributes(c, sub)))
        return out

    P[0].fired = broken_concepts(ctx) != concepts_next_closure(ctx)

    fx = known_answer_fixtures()[0]
    P[1].fired = oracle_exhaustive(fx["instance"]).transition != "SPLIT"

    # a context where a tracked object loses an attribute: retention fails
    k0 = _ctx(["g1", "g2"], ["m1"], {("g1", "m1"), ("g2", "m1")})
    k1 = _ctx(["g1", "g2", "h1"], ["m1"], {("g1", "m1"), ("h1", "m1")})
    inst = Instance("PP-RET", "NO_CHANGE", 0, k0, k1, ("g1", "g2"), ("g1",), "h1")
    o = oracle_exhaustive(inst)
    abl = ablation_minus_old_case_retention(inst)
    P[2].fired = bool(abl["retention_ok"] and not o.retention_ok) or bool(o.retention_ok)

    P[3].fired = (
        discrimination_gate(
            {a: 1.0 for a in ARM_FUNCTIONS}, weak_arms=("C_RANDOM_TRANSITION",),
            max_weak=0.60, min_strong=0.95,
        ).verdict
        == "FAIL"
    )

    split_fx = known_answer_fixtures()[2]["instance"]
    P[4].fired = (
        mechanic_full(split_fx)["disposition"] == "SPLIT"
        and ablation_minus_extent_geometry(split_fx)["disposition"] != "SPLIT"
    )

    prec = next(f for f in known_answer_fixtures() if "PRECEDENCE" in f["name"])
    prec_ans = oracle_exhaustive(prec["instance"])
    P[5].fired = (
        len(prec_ans.predicates_holding) > 1
        and prec_ans.transition == PRECEDENCE[
            min(PRECEDENCE.index(c) for c in prec_ans.predicates_holding)
        ]
    )
    return P


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------

SPEC = SuiteSpec(
    suite_id="FM30",
    title="Formal concept closure and revision with transition class, retention and hidden cases",
    families=FAMILIES,
    arms=(
        ArmSpec("P0_FIXED_LESSON_INJECTION", "PARENT", "frozen revision-lesson table"),
        ArmSpec("P1_GALOIS_CLOSURE", "PARENT", "Ganter-Wille derivation operators and closure"),
        ArmSpec("P2_LATTICE_ORDER_GEOMETRY", "PARENT", "concept-lattice extent geometry"),
        ArmSpec("P3_ATTRIBUTE_EXPLORATION", "PARENT", "implication counterexamples (Ganter)"),
        ArmSpec("F0_PARENT_FEDERATION", "FEDERATION", "pre-registered outcome-blind composition"),
        ArmSpec("M_F2_CONCEPTUAL_DEVELOPMENT_FULL", "MECHANIC", "ORION L3 conceptual development"),
        ArmSpec("M_MINUS_EXTENT_GEOMETRY", "ABLATION", ""),
        ArmSpec("M_MINUS_BRIDGE_DETECTION", "ABLATION", ""),
        ArmSpec("M_MINUS_CLOSURE_RECOMPUTATION", "ABLATION", ""),
        ArmSpec("M_MINUS_OLD_CASE_RETENTION", "ABLATION", ""),
        ArmSpec("C_ALWAYS_NO_CHANGE", "CONTROL", ""),
        ArmSpec("C_ALWAYS_SPECIALIZE", "CONTROL", ""),
        ArmSpec("C_RANDOM_TRANSITION", "CONTROL", ""),
    ),
    mechanic_arm="M_F2_CONCEPTUAL_DEVELOPMENT_FULL",
    strongest_parent_arm="F0_PARENT_FEDERATION",
    federation_arm="F0_PARENT_FEDERATION",
    weak_arms=("P0_FIXED_LESSON_INJECTION", "P1_GALOIS_CLOSURE", "P3_ATTRIBUTE_EXPLORATION", "M_MINUS_EXTENT_GEOMETRY"),
    constant_arms=("C_ALWAYS_NO_CHANGE", "C_ALWAYS_SPECIALIZE"),
    random_arm="C_RANDOM_TRANSITION",
    ablation_for_family={
        "SPLIT": "M_MINUS_EXTENT_GEOMETRY",
        "MERGE": "M_MINUS_EXTENT_GEOMETRY",
        "BRIDGE": "M_MINUS_BRIDGE_DETECTION",
        "SPECIALIZE": "M_MINUS_CLOSURE_RECOMPUTATION",
    },
    default_ablation="M_MINUS_OLD_CASE_RETENTION",
    decoy_families=("SPLIT", "MERGE", "BRIDGE", "SPECIALIZE"),
    min_tasks=96,
    dev_per_family=3,
    protected_per_family=20,  # 5 x 20 = 100 >= 96
    design_json="FM30_FORMAL_CONCEPT_REVISION_EXACT_STUDY_DESIGN_V1.json",
    oracle_agreement_fields=("transition", "retention_ok", "hidden_in_extent", "n_concepts_k0", "n_concepts_k1"),
    endpoint_key=lambda rec: endpoint(rec),
    oracle_endpoint_key=lambda e: f"{e['transition']}|{int(e['retention_ok'])}{int(e['hidden_in_extent'])}",
    unsafe_scope=lambda e: e["retention_ok"] is False,
    unsafe_claim=lambda rec, e: bool(rec["retention_ok"]),
    unsafe_name="old-valid-case loss claimed as retained",
    generate=generate_split,
    oracle=oracle_exhaustive,
    cross_check=oracle_cross_check,
    run_arm=run_arm,
    parent_fidelity=parent_fidelity,
    known_answer_fixtures=known_answer_fixtures,
    planted_positives=planted_positives,
)
