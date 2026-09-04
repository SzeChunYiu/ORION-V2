#!/usr/bin/env python3
"""FM50 - functoriality and commuting diagrams: exact generator, oracle, parents.

Each FM50 instance registers a **transfer claim in categorical form**: a donor
finite category `D`, a target finite category `T`, a candidate functor
`F : D -> T` (a total object map and a total morphism map), a set of donor
morphism pairs whose *distinction the claim depends on*, and a set of registered
commuting diagrams.  The endpoint is the exact disposition of that claim:

    TRANSFER_VALID                   F satisfies every functor law and keeps
                                     every registered distinction distinct;
    BLOCK_ENDPOINT_VIOLATION         some donor morphism's image does not run
                                     between the images of its endpoints - F is
                                     not even a map of the underlying graphs;
    BLOCK_IDENTITY_NOT_PRESERVED     endpoints hold but some identity is not
                                     sent to an identity;
    BLOCK_COMPOSITION_NOT_PRESERVED  endpoints and identities hold but some
                                     composite is not preserved;
    BLOCK_MIXED_LAW_OBSTRUCTION      both identity and composition fail;
    BLOCK_FALSE_EQUIVALENCE          F is a genuine functor but collapses a
                                     registered distinction, so the claim it
                                     licenses is a false equivalence.

The registered precedence is endpoint > (identity, composition) > distinction,
and the mixed class exists so that the order is visible rather than hidden.

**Why the valid disposition is spelled `TRANSFER_VALID` and not
`FUNCTOR_VALID`.**  The shared runner defines over-acceptance as
`prediction == "TRANSFER_VALID"` and defines the G2 denominator as the
instances whose label is not `TRANSFER_VALID`.  Under a renamed token every
instance would count as blocked, `m_over` and `p_over` would both be
structurally pinned to zero, and `G2_ANTI_PERMISSIVENESS` would print a full
denominator while being incapable of firing - the exact defect class this
programme exists to catch.  `FUNCTOR_VALID` is kept as a readable alias.

**Consequence, and the reason the suite is worth running: no single parent owns
the endpoint.**  The category-law parent (`assess_functor` in the reference
module) decides endpoint/identity/composition exactly and is structurally blind
to false equivalence, because collapsing two morphisms is not a violation of any
functor law.  The faithfulness parent owns exactly that stratum and is blind to
every law.  The diagram-chasing parent owns the registered diagrams and is blind
to identity preservation and to unregistered composites.  The strongest faithful
comparator is therefore their federation under a rule fixed before any outcome.

**Eligibility is a gate, not a filter.**  A proposed native construction forms
the required categorical structure only if it contains identities and is closed
under composition with an associative, endpoint-correct composition table.
`FiniteCategory.__post_init__` decides that exactly and raises when it fails.  A
construction that fails is `INELIGIBLE`: it is never negative evidence and never
silently dropped - it is counted per family and published.  The eligibility
checker is itself audited by planted law-breaking constructions (a deleted
composite, a rebound identity, and a non-associative monoid table) that must be
caught in the same execution, so the guard can never become a checker that
reports zero violations having never run.

Oracle validity rests on two independent algorithms agreeing on the disposition,
the full violation profile and the exhaustively determined number of valid
claim-respecting functors `D -> T`:

  * `oracle_exhaustive`      - the claim profile from this module's own
    law-by-law loop, and `n_valid_functors` by enumerating every object map and
    every endpoint-respecting morphism map (the identity morphisms are pinned by
    the identity law, which is definitional, not a heuristic);
  * `oracle_constraint_search` - the claim profile from the reference module's
    `assess_functor` plus this module's distinction check, and
    `n_valid_functors` by a forward-checking backtracking search that charges
    each law the moment its members are assigned and never materialises the map
    space.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence

from fm_core import ArmSpec, GateResult, PlantedPositive, SuiteSpec

from orion_v2.transfer_formal_mechanics import (
    FiniteCategory,
    FunctorCandidate,
    assess_functor,
)

# --------------------------------------------------------------------------
# task model
# --------------------------------------------------------------------------

FAMILIES = (
    "VALID_FUNCTOR",
    "SURFACE_NAME_DECOY",
    "LICENSED_COLLAPSE",
    "ENDPOINT_VIOLATION",
    "IDENTITY_NOT_PRESERVED",
    "COMPOSITION_NOT_PRESERVED",
    "MIXED_LAW_OBSTRUCTION",
    "FALSE_EQUIVALENCE",
)

FUNCTOR_VALID = "TRANSFER_VALID"  # readable alias; see the module docstring

DISPOSITIONS = (
    "TRANSFER_VALID",
    "BLOCK_ENDPOINT_VIOLATION",
    "BLOCK_IDENTITY_NOT_PRESERVED",
    "BLOCK_COMPOSITION_NOT_PRESERVED",
    "BLOCK_MIXED_LAW_OBSTRUCTION",
    "BLOCK_FALSE_EQUIVALENCE",
)

EXPECTED_DISPOSITION = {
    "VALID_FUNCTOR": {"TRANSFER_VALID"},
    "SURFACE_NAME_DECOY": {"TRANSFER_VALID"},
    "LICENSED_COLLAPSE": {"TRANSFER_VALID"},
    "ENDPOINT_VIOLATION": {"BLOCK_ENDPOINT_VIOLATION"},
    "IDENTITY_NOT_PRESERVED": {"BLOCK_IDENTITY_NOT_PRESERVED"},
    "COMPOSITION_NOT_PRESERVED": {"BLOCK_COMPOSITION_NOT_PRESERVED"},
    "MIXED_LAW_OBSTRUCTION": {"BLOCK_MIXED_LAW_OBSTRUCTION"},
    "FALSE_EQUIVALENCE": {"BLOCK_FALSE_EQUIVALENCE"},
}

# every function {0,1} -> {0,1}; (0, 1) is the identity
FUNCS2 = ((0, 1), (1, 0), (0, 0), (1, 1))

ENUMERATION_CAP = 24000  # per-instance ceiling on the exhaustive map space


class MapSpaceTooLarge(RuntimeError):
    """The exhaustive branch would exceed the registered enumeration cap."""


# --------------------------------------------------------------------------
# concrete finite categories (subcategories of FinSet: lawful by construction)
# --------------------------------------------------------------------------
#
# A morphism is a triple (source object, target object, mapping), where mapping
# is a tuple of length |carrier(source)| with entries in range(|carrier(target)|).
# Composition is function composition, so associativity holds for free; the
# construction forms a category exactly when the morphism set contains every
# identity and is closed under composition, which is what makes eligibility a
# property of the proposal rather than of the checker.

Mor = tuple[str, str, tuple[int, ...]]


def _identity(obj: str, size: int) -> Mor:
    return (obj, obj, tuple(range(size)))


def _compose(f: Mor, g: Mor) -> Mor:
    """`g` after `f`; requires target(f) == source(g)."""
    return (f[0], g[1], tuple(g[2][x] for x in f[2]))


def close_under_composition(
    carriers: dict[str, int], generators: Sequence[Mor], *, cap: int
) -> set[Mor] | None:
    mors: set[Mor] = {_identity(o, s) for o, s in carriers.items()}
    mors |= set(generators)
    changed = True
    while changed:
        changed = False
        for f in sorted(mors):
            for g in sorted(mors):
                if f[1] != g[0]:
                    continue
                h = _compose(f, g)
                if h not in mors:
                    mors.add(h)
                    changed = True
                    if len(mors) > cap:
                        return None
    return mors


def _morphism_names(carriers: dict[str, int], mors: set[Mor]) -> dict[Mor, str]:
    ids = {_identity(o, s): f"id_{o}" for o, s in carriers.items()}
    names = dict(ids)
    for k, m in enumerate(sorted(m for m in mors if m not in ids)):
        names[m] = f"m{k}"
    return names


def build_category(
    carriers: dict[str, int],
    mors: set[Mor],
    *,
    object_alias: dict[str, str] | None = None,
) -> FiniteCategory:
    """Assemble a `FiniteCategory` from an explicit morphism set.

    The composition table binds exactly those composable pairs whose composite
    is present in the set.  A proposal that is not closed under composition
    therefore produces an incomplete table and `FiniteCategory.__post_init__`
    raises - which is precisely the eligibility verdict we want.
    """
    alias = object_alias or {}

    def on(o: str) -> str:
        return alias.get(o, o)

    names = _morphism_names(carriers, mors)
    items = sorted(names.items(), key=lambda kv: kv[1])
    composition = []
    for f in sorted(mors):
        for g in sorted(mors):
            if f[1] != g[0]:
                continue
            h = _compose(f, g)
            if h in names:
                composition.append((names[f], names[g], names[h]))
    return FiniteCategory(
        objects=tuple(on(o) for o in sorted(carriers)),
        morphisms=tuple(n for _, n in items),
        source_target=tuple((n, on(m[0]), on(m[1])) for m, n in items),
        identities=tuple(
            (on(o), names[_identity(o, carriers[o])]) for o in sorted(carriers)
        ),
        composition=tuple(composition),
    )


def try_build_category(
    carriers: dict[str, int],
    mors: set[Mor],
    *,
    object_alias: dict[str, str] | None = None,
) -> tuple[FiniteCategory | None, str | None]:
    """The eligibility decision for one proposed native construction."""
    try:
        return build_category(carriers, mors, object_alias=object_alias), None
    except ValueError as exc:
        return None, str(exc)


# --------------------------------------------------------------------------
# instance
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Instance:
    instance_id: str
    family: str
    seed: int
    donor: FiniteCategory
    target: FiniteCategory
    candidate: FunctorCandidate
    distinguished_pairs: tuple[tuple[str, str], ...]
    registered_diagrams: tuple[tuple[str, str, str], ...]
    surface_pairs: tuple[tuple[str, str], ...]

    def as_json(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,
            "donor": _category_json(self.donor),
            "target": _category_json(self.target),
            "candidate": {
                "object_map": [list(p) for p in self.candidate.object_map],
                "morphism_map": [list(p) for p in self.candidate.morphism_map],
            },
            "distinguished_pairs": [list(p) for p in self.distinguished_pairs],
            "registered_diagrams": [list(d) for d in self.registered_diagrams],
            "surface_pairs": [list(p) for p in self.surface_pairs],
        }


def _category_json(c: FiniteCategory) -> dict:
    return {
        "objects": list(c.objects),
        "morphisms": list(c.morphisms),
        "source_target": [list(t) for t in c.source_target],
        "identities": [list(t) for t in c.identities],
        "composition": [list(t) for t in c.composition],
    }


# --------------------------------------------------------------------------
# the claim profile (this module's own law-by-law implementation)
# --------------------------------------------------------------------------


def claim_profile(inst: Instance) -> dict[str, int]:
    """Exact violation profile of the registered candidate.

    Implemented here directly from the category axioms rather than through the
    reference module, so that the cross-check oracle - which does use
    `assess_functor` - is a genuinely independent second computation.
    """
    donor, target, cand = inst.donor, inst.target, inst.candidate
    om = dict(cand.object_map)
    mm = dict(cand.morphism_map)
    dep, tep = donor.endpoints, target.endpoints
    endpoint = 0
    for m, (s, t) in dep.items():
        if tep[mm[m]] != (om[s], om[t]):
            endpoint += 1
    tid = target.identity_map
    identity = sum(
        1 for o in donor.objects if mm[donor.identity_map[o]] != tid[om[o]]
    )
    tc = target.compose
    composition = sum(
        1 for (f, g), h in donor.compose.items() if tc.get((mm[f], mm[g])) != mm[h]
    )
    collapse = sum(1 for a, b in inst.distinguished_pairs if mm[a] == mm[b])
    return {
        "ENDPOINT": endpoint,
        "IDENTITY": identity,
        "COMPOSITION": composition,
        "COLLAPSE": collapse,
        "TOTAL": endpoint + identity + composition + collapse,
    }


def classify(prof: dict[str, int]) -> str:
    """Registered precedence: endpoint > (identity, composition) > distinction."""
    if prof["ENDPOINT"]:
        return "BLOCK_ENDPOINT_VIOLATION"
    if prof["IDENTITY"] and prof["COMPOSITION"]:
        return "BLOCK_MIXED_LAW_OBSTRUCTION"
    if prof["IDENTITY"]:
        return "BLOCK_IDENTITY_NOT_PRESERVED"
    if prof["COMPOSITION"]:
        return "BLOCK_COMPOSITION_NOT_PRESERVED"
    if prof["COLLAPSE"]:
        return "BLOCK_FALSE_EQUIVALENCE"
    return "TRANSFER_VALID"


# --------------------------------------------------------------------------
# oracle 1 - exhaustive enumeration of the functor space
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class OracleAnswer:
    disposition: str
    total_violations: int
    best_profile: tuple[tuple[str, int], ...]
    n_maps_explored: int
    n_valid_functors: int
    witness: tuple[tuple[str, str], ...] | None

    def as_dict(self) -> dict:
        return {
            "disposition": self.disposition,
            "total_violations": self.total_violations,
            "best_profile": {k: v for k, v in self.best_profile},
            "n_maps_explored": self.n_maps_explored,
            "n_valid_functors": self.n_valid_functors,
            "witness": [list(p) for p in self.witness] if self.witness else None,
        }


def _candidate_images(donor: FiniteCategory, target: FiniteCategory, om: dict[str, str]):
    """Endpoint-respecting image sets, with identities pinned by the identity law."""
    dep, tep = donor.endpoints, target.endpoints
    tid, did = target.identity_map, donor.identity_map
    pinned = {did[o]: tid[om[o]] for o in donor.objects}
    out: list[tuple[str, list[str]]] = []
    for m in donor.morphisms:
        if m in pinned:
            out.append((m, [pinned[m]]))
            continue
        s, t = dep[m]
        want = (om[s], om[t])
        cands = [tm for tm in target.morphisms if tep[tm] == want]
        if not cands:
            return None
        out.append((m, cands))
    return out


def enumerate_valid_functors(
    donor: FiniteCategory,
    target: FiniteCategory,
    distinguished: Sequence[tuple[str, str]] = (),
    *,
    cap: int = ENUMERATION_CAP,
    collect: bool = False,
) -> tuple[int, int, list[tuple[dict[str, str], dict[str, str]]]]:
    """Exhaustive: every object map x every endpoint-respecting morphism map."""
    tc = target.compose
    total = 0
    explored = 0
    found: list[tuple[dict[str, str], dict[str, str]]] = []
    for omv in product(target.objects, repeat=len(donor.objects)):
        om = dict(zip(donor.objects, omv))
        slots = _candidate_images(donor, target, om)
        if slots is None:
            continue
        size = 1
        for _, cands in slots:
            size *= len(cands)
        explored += size
        if explored > cap:
            raise MapSpaceTooLarge(f"{explored} > {cap}")
        keys = [m for m, _ in slots]
        for choice in product(*[c for _, c in slots]):
            mm = dict(zip(keys, choice))
            if any(tc.get((mm[f], mm[g])) != mm[h] for (f, g), h in donor.compose.items()):
                continue
            if any(mm[a] == mm[b] for a, b in distinguished):
                continue
            total += 1
            if collect:
                found.append((dict(om), mm))
    return total, explored, found


def oracle_exhaustive(inst: Instance) -> OracleAnswer:
    prof = claim_profile(inst)
    n_valid, explored, _ = enumerate_valid_functors(
        inst.donor, inst.target, inst.distinguished_pairs
    )
    prof = dict(prof)
    prof["N_VALID_FUNCTORS"] = n_valid
    return OracleAnswer(
        disposition=classify(prof),
        total_violations=prof["TOTAL"],
        best_profile=tuple(sorted(prof.items())),
        n_maps_explored=explored,
        n_valid_functors=n_valid,
        witness=tuple(sorted(dict(inst.candidate.morphism_map).items())),
    )


# --------------------------------------------------------------------------
# oracle 2 - independent constraint search (never materialises the map space)
# --------------------------------------------------------------------------


def count_valid_functors_by_search(
    donor: FiniteCategory,
    target: FiniteCategory,
    distinguished: Sequence[tuple[str, str]] = (),
) -> int:
    """Forward-checking backtracking count.

    Morphisms are assigned in a fixed order; every law is charged the moment all
    of its members are assigned, and a partial assignment that has already
    violated a law is abandoned.  No product over the map space is ever formed.
    """
    tc = target.compose
    total = 0
    for omv in product(target.objects, repeat=len(donor.objects)):
        om = dict(zip(donor.objects, omv))
        slots = _candidate_images(donor, target, om)
        if slots is None:
            continue
        order = [m for m, _ in slots]
        domains = {m: c for m, c in slots}
        pos = {m: i for i, m in enumerate(order)}
        # composition triples indexed by the last of their members to be assigned
        triples_by_last: dict[str, list[tuple[str, str, str]]] = {m: [] for m in order}
        for (f, g), h in donor.compose.items():
            last = max((f, g, h), key=lambda m: pos[m])
            triples_by_last[last].append((f, g, h))
        pairs_by_last: dict[str, list[tuple[str, str]]] = {m: [] for m in order}
        for a, b in distinguished:
            pairs_by_last[max((a, b), key=lambda m: pos[m])].append((a, b))

        assign: dict[str, str] = {}

        def rec(i: int) -> int:
            if i == len(order):
                return 1
            m = order[i]
            count = 0
            for image in domains[m]:
                assign[m] = image
                ok = True
                for f, g, h in triples_by_last[m]:
                    if tc.get((assign[f], assign[g])) != assign[h]:
                        ok = False
                        break
                if ok:
                    for a, b in pairs_by_last[m]:
                        if assign[a] == assign[b]:
                            ok = False
                            break
                if ok:
                    count += rec(i + 1)
                del assign[m]
            return count

        total += rec(0)
    return total


def oracle_constraint_search(inst: Instance) -> OracleAnswer:
    """Cross-check: the reference module decides the laws, a search does the count."""
    donor, target, cand = inst.donor, inst.target, inst.candidate
    a = assess_functor(donor, target, cand)
    mm = dict(cand.morphism_map)
    collapse = sum(1 for x, y in inst.distinguished_pairs if mm[x] == mm[y])
    prof = {
        "ENDPOINT": a.endpoint_violations,
        "IDENTITY": a.identity_violations,
        "COMPOSITION": a.composition_violations,
        "COLLAPSE": collapse,
        "TOTAL": a.endpoint_violations
        + a.identity_violations
        + a.composition_violations
        + collapse,
    }
    n_valid = count_valid_functors_by_search(donor, target, inst.distinguished_pairs)
    prof["N_VALID_FUNCTORS"] = n_valid
    return OracleAnswer(
        disposition=classify(prof),
        total_violations=prof["TOTAL"],
        best_profile=tuple(sorted(prof.items())),
        n_maps_explored=-1,
        n_valid_functors=n_valid,
        witness=tuple(sorted(mm.items())),
    )


def oracle_agrees(inst: Instance) -> tuple[bool, OracleAnswer, OracleAnswer]:
    a = oracle_exhaustive(inst)
    b = oracle_constraint_search(inst)
    same = (
        a.disposition == b.disposition
        and a.total_violations == b.total_violations
        and a.best_profile == b.best_profile
        and a.n_valid_functors == b.n_valid_functors
    )
    return same, a, b


# --------------------------------------------------------------------------
# eligibility: law-breaking probes that must be caught in the same execution
# --------------------------------------------------------------------------


def _kwargs_of(cat: FiniteCategory) -> dict:
    return {
        "objects": cat.objects,
        "morphisms": cat.morphisms,
        "source_target": cat.source_target,
        "identities": cat.identities,
        "composition": cat.composition,
    }


def probe_deleted_composite(cat: FiniteCategory) -> dict:
    """Remove one composition binding: the table no longer binds every pair."""
    kw = _kwargs_of(cat)
    kw["composition"] = tuple(kw["composition"][1:])
    return kw


def probe_rebound_identity(cat: FiniteCategory) -> dict:
    """Point one object's identity at a morphism that is not its identity."""
    kw = _kwargs_of(cat)
    ids = dict(cat.identities)
    obj = cat.objects[0]
    other = next(m for m in cat.morphisms if m != ids[obj])
    kw["identities"] = tuple(
        (o, other if o == obj else i) for o, i in cat.identities
    )
    return kw


def probe_non_associative_monoid() -> dict:
    """A one-object table that is complete and unital but not associative.

    Elements {e, a, b} with e the identity and a*a = b, a*b = a, b*a = b,
    b*b = a.  Then (a*a)*b = b*b = a while a*(a*b) = a*a = b.  A one-object
    construction makes the completeness check automatic, so the failure the
    probe demonstrates is genuinely the associativity law and not an earlier
    check firing first.  Convention: `(f, g, h)` means `g` after `f` equals `h`.
    """
    els = ("e", "a", "b")
    table = {
        ("e", "e"): "e", ("e", "a"): "a", ("e", "b"): "b",
        ("a", "e"): "a", ("b", "e"): "b",
        ("a", "a"): "b", ("a", "b"): "a",
        ("b", "a"): "b", ("b", "b"): "a",
    }
    return {
        "objects": ("O",),
        "morphisms": els,
        "source_target": tuple((m, "O", "O") for m in els),
        "identities": (("O", "e"),),
        "composition": tuple((f, g, h) for (f, g), h in sorted(table.items())),
    }


def probe_verdict(kwargs: dict) -> tuple[bool, str]:
    """(caught, reason) for one proposed construction."""
    try:
        FiniteCategory(**kwargs)
    except ValueError as exc:
        return True, str(exc)
    return False, "ADMITTED"


def eligibility_audit() -> dict:
    """Deterministic audit of the eligibility checker, both directions.

    Six lawful constructions must be admitted and six law-breaking ones caught.
    Asserting only the alarm half would leave a checker that cries wolf
    undetected, and asserting only the no-alarm half would leave a checker that
    never fires undetected, so both halves carry their own denominator.
    """
    lawful: list[dict] = []
    breaking: list[dict] = []
    for k in range(6):
        rng = random.Random(0xE11 + k)
        carriers = {"A": 2, "B": 2}
        gens = [
            ("A", "A", rng.choice([f for f in FUNCS2 if f != (0, 1)])),
            ("A", "B", rng.choice(FUNCS2)),
        ]
        mors = close_under_composition(carriers, gens, cap=10)
        cat, reason = try_build_category(carriers, mors)
        lawful.append({"name": f"closed_concrete_category_{k}", "admitted": cat is not None,
                       "reason": reason})
        if cat is not None:
            breaking.append({"name": f"deleted_composite_{k}",
                             **dict(zip(("caught", "reason"), probe_verdict(probe_deleted_composite(cat))))})
            breaking.append({"name": f"rebound_identity_{k}",
                             **dict(zip(("caught", "reason"), probe_verdict(probe_rebound_identity(cat))))})
        # a proposal that was never closed under composition.  It is only a
        # law-breaking probe when it genuinely is not closed: a generator set
        # that happens to be closed already IS a category and admitting it is
        # the correct verdict, so it is recorded on the lawful side instead.
        # Never conflate "did not need to fire" with "fired correctly".
        proposal = {_identity(o, s) for o, s in carriers.items()} | set(gens)
        closed = close_under_composition(carriers, gens, cap=10)
        c2, r2 = try_build_category(carriers, proposal)
        if proposal == closed:
            lawful.append({"name": f"already_closed_proposal_{k}",
                           "admitted": c2 is not None, "reason": r2})
        else:
            breaking.append({"name": f"unclosed_proposal_{k}",
                             "caught": c2 is None, "reason": r2 or "ADMITTED"})
    caught_assoc, assoc_reason = probe_verdict(probe_non_associative_monoid())
    breaking.append(
        {"name": "non_associative_monoid", "caught": caught_assoc, "reason": assoc_reason}
    )
    n_eval = len(lawful) + len(breaking)
    viol = sum(1 for x in lawful if not x["admitted"]) + sum(
        1 for x in breaking if not x["caught"]
    )
    return {
        "lawful": lawful,
        "law_breaking": breaking,
        "n_evaluated": n_eval,
        "n_violations": viol,
        "associativity_probe_reason": assoc_reason,
    }


def eligibility_gate(audit: dict, live_counts: dict[str, int] | None = None) -> GateResult:
    """G0g - the eligibility guard, with its own denominator.

    `n_evaluated` counts every construction the checker actually ruled on: the
    audit's lawful and law-breaking constructions, plus, when a split is being
    scored, the live eligible and ineligible constructions of that split.
    """
    live = live_counts or {}
    n_live = sum(live.values())
    return GateResult(
        name="G0g_ELIGIBILITY",
        rule=(
            "every proposed native construction is ruled on by "
            "FiniteCategory.__post_init__: lawful constructions are admitted, "
            "law-breaking ones (deleted composite, rebound identity, unclosed "
            "proposal, non-associative table) are caught and counted INELIGIBLE, "
            "never counted as negative evidence"
        ),
        n_evaluated=audit["n_evaluated"] + n_live,
        n_violations=audit["n_violations"],
        requires_evaluated=12,
        detail={"audit": audit, "live_counts": live},
    )


# --------------------------------------------------------------------------
# generator
# --------------------------------------------------------------------------

DONOR_OBJECTS = {"A": 2, "B": 2, "I": 2}
TARGET_OBJECTS = {"A": 2, "B": 2, "I": 2, "Z": 1}
NORMAL_ALIAS = {"A": "A_t", "B": "B_t", "I": "I_t", "Z": "Z_t"}
DECOY_ALIAS = {"A": "B_t", "B": "I_t", "I": "A_t", "Z": "Z_t"}


def _parallel_pairs(names: dict[Mor, str], mors: Iterable[Mor]) -> list[tuple[str, str]]:
    by_ep: dict[tuple[str, str], list[str]] = {}
    for m in sorted(mors):
        by_ep.setdefault((m[0], m[1]), []).append(names[m])
    out: list[tuple[str, str]] = []
    for group in by_ep.values():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                out.append((a, b))
    return sorted(out)


def _generate_one(family: str, seed: int, idx: int) -> tuple[Instance | None, str]:
    """Propose one instance.  Returns (instance, verdict).

    verdict is `OK`, `INELIGIBLE` (the proposed construction is not a category)
    or `REJECT_<reason>` (a well-formed construction that does not realise the
    family; the oracle, not the generator, decides which).
    """
    rng = random.Random(seed)

    # ---- donor proposal -------------------------------------------------
    dgens: list[Mor] = []
    for _ in range(rng.randint(1, 2)):
        dgens.append(("A", "A", rng.choice([f for f in FUNCS2 if f != (0, 1)])))
    for _ in range(rng.randint(1, 2)):
        dgens.append(("A", "B", rng.choice(FUNCS2)))
    dgens = sorted(set(dgens))

    # A quarter of proposals are emitted without closing under composition:
    # a native vocabulary that is not composition-closed does not form the
    # required categorical structure and is INELIGIBLE, never negative evidence.
    propose_unclosed = rng.random() < 0.25
    if propose_unclosed:
        dmors: set[Mor] | None = {
            _identity(o, s) for o, s in DONOR_OBJECTS.items()
        } | set(dgens)
    else:
        dmors = close_under_composition(DONOR_OBJECTS, dgens, cap=8)
    if dmors is None:
        return None, "REJECT_DONOR_CLOSURE_TOO_LARGE"
    donor, reason = try_build_category(DONOR_OBJECTS, dmors)
    if donor is None:
        return None, "INELIGIBLE"
    dnames = _morphism_names(DONOR_OBJECTS, dmors)

    hom_ab = [m for m in dmors if (m[0], m[1]) == ("A", "B")]
    hom_aa = [m for m in dmors if (m[0], m[1]) == ("A", "A")]
    if family in ("LICENSED_COLLAPSE", "FALSE_EQUIVALENCE") and (
        len(hom_ab) < 2 or len(hom_aa) < 2
    ):
        return None, "REJECT_NO_ROOM_FOR_PARTIAL_COLLAPSE"

    # ---- target proposal ------------------------------------------------
    tgens: list[Mor] = list(dgens)
    for _ in range(rng.randint(0, 2)):
        tgens.append(("A", "A", rng.choice(FUNCS2)))
    for _ in range(rng.randint(0, 2)):
        tgens.append(("A", "B", rng.choice(FUNCS2)))
    tgens.append(("I", "I", (0, 0)))  # a non-identity idempotent at the isolated object
    tgens.append(("A", "Z", (0, 0)))  # the unique map to the singleton object
    tgens.append(("Z", "B", (rng.randint(0, 1),)))
    tmors = close_under_composition(TARGET_OBJECTS, sorted(set(tgens)), cap=18)
    if tmors is None:
        return None, "REJECT_TARGET_CLOSURE_TOO_LARGE"
    alias = DECOY_ALIAS if family == "SURFACE_NAME_DECOY" else NORMAL_ALIAS
    target, reason = try_build_category(TARGET_OBJECTS, tmors, object_alias=alias)
    if target is None:
        return None, "INELIGIBLE"
    tnames = _morphism_names(TARGET_OBJECTS, tmors)

    # ---- the inclusion functor: valid by construction --------------------
    inclusion_objects = {o: alias[o] for o in sorted(DONOR_OBJECTS)}
    inclusion_morphisms = {dnames[m]: tnames[m] for m in sorted(dmors)}
    tep = target.endpoints
    t_by_ep: dict[tuple[str, str], list[str]] = {}
    for n, (s, t) in tep.items():
        t_by_ep.setdefault((s, t), []).append(n)
    for v in t_by_ep.values():
        v.sort()

    om = dict(inclusion_objects)
    mm = dict(inclusion_morphisms)
    d_parallel = _parallel_pairs(dnames, dmors)
    if not d_parallel:
        return None, "REJECT_NO_PARALLEL_PAIR"
    non_identity = sorted(dnames[m] for m in dmors if m not in
                          {_identity(o, s) for o, s in DONOR_OBJECTS.items()})

    if family in ("VALID_FUNCTOR", "SURFACE_NAME_DECOY"):
        distinguished = tuple(rng.sample(d_parallel, min(2, len(d_parallel))))
    elif family in ("LICENSED_COLLAPSE", "FALSE_EQUIVALENCE"):
        try:
            _, _, found = enumerate_valid_functors(donor, target, (), collect=True)
        except MapSpaceTooLarge:
            return None, "REJECT_MAP_SPACE_TOO_LARGE"
        chosen = None
        for cand_om, cand_mm in found:
            collapsed = [p for p in d_parallel if cand_mm[p[0]] == cand_mm[p[1]]]
            separated = [p for p in d_parallel if cand_mm[p[0]] != cand_mm[p[1]]]
            if collapsed and separated:
                chosen = (cand_om, cand_mm, collapsed, separated)
                break
        if chosen is None:
            return None, "REJECT_NO_PARTIAL_COLLAPSE_FUNCTOR"
        om, mm, collapsed, separated = dict(chosen[0]), dict(chosen[1]), chosen[2], chosen[3]
        if family == "LICENSED_COLLAPSE":
            distinguished = tuple(rng.sample(separated, min(2, len(separated))))
        else:
            distinguished = (rng.choice(collapsed),)
    elif family == "ENDPOINT_VIOLATION":
        victim = rng.choice(non_identity)
        want = tep[mm[victim]]
        others = [n for n in target.morphisms if tep[n] != want]
        if not others:
            return None, "REJECT_NO_WRONG_ENDPOINT_IMAGE"
        mm[victim] = rng.choice(others)
        distinguished = tuple(rng.sample(d_parallel, min(1, len(d_parallel))))
    elif family == "IDENTITY_NOT_PRESERVED":
        # the isolated object I carries no composites beyond (id_I, id_I), so
        # breaking its identity cannot induce a composition violation
        mm["id_I"] = tnames[("I", "I", (0, 0))]
        distinguished = ()
    elif family == "MIXED_LAW_OBSTRUCTION":
        cands = [n for n in t_by_ep.get((alias["A"], alias["A"]), []) if n != mm["id_A"]]
        if not cands:
            return None, "REJECT_NO_NON_IDENTITY_ENDOMORPHISM"
        mm["id_A"] = rng.choice(cands)
        distinguished = ()
    elif family == "COMPOSITION_NOT_PRESERVED":
        victim = rng.choice(non_identity)
        want = tep[mm[victim]]
        alts = [n for n in t_by_ep.get(want, []) if n != mm[victim]]
        if not alts:
            return None, "REJECT_NO_PARALLEL_ALTERNATIVE"
        mm[victim] = rng.choice(alts)
        distinguished = ()
    else:  # pragma: no cover - guarded by FAMILIES
        raise ValueError(family)

    # ---- registered commuting diagrams ----------------------------------
    ident_names = {f"id_{o}" for o in DONOR_OBJECTS}
    nontrivial = sorted(
        (f, g, h) for (f, g), h in donor.compose.items()
        if f not in ident_names and g not in ident_names
    )
    pool = nontrivial or sorted((f, g, h) for (f, g), h in donor.compose.items())
    k = max(1, len(pool) // 2)
    diagrams = tuple(sorted(rng.sample(pool, k)))

    # the surface hint: the name-similarity pairing a reader would guess.  In
    # SURFACE_NAME_DECOY the target display names are deranged, so this pairing
    # is exactly wrong while the registered candidate is exactly right.
    surface = tuple((o, f"{o}_t") for o in sorted(DONOR_OBJECTS))
    candidate = FunctorCandidate(
        object_map=tuple(sorted(om.items())),
        morphism_map=tuple(sorted(mm.items())),
    )
    inst = Instance(
        instance_id=f"{family}-{idx:05d}",
        family=family,
        seed=seed,
        donor=donor,
        target=target,
        candidate=candidate,
        distinguished_pairs=tuple(distinguished),
        registered_diagrams=diagrams,
        surface_pairs=surface,
    )
    return inst, "OK"


def generate_split(split: str, seed: str, per_family: dict[str, int]):
    """Generate (instance, oracle) pairs.

    The generator *proposes* a family; the exhaustive oracle *verifies* it.  An
    instance whose exhaustive disposition is not in its family's registered set,
    or on which the two oracle algorithms disagree, is rejected and resampled.
    A proposal whose construction is not a finite category is INELIGIBLE - a
    third outcome, counted separately from a rejection, because an ineligible
    construction is not negative evidence about any arm.
    """
    pairs: list[tuple[Instance, OracleAnswer]] = []
    rejects: dict[str, int] = {f: 0 for f in FAMILIES}
    for f in FAMILIES:
        rejects[f"INELIGIBLE_NOT_A_CATEGORY:{f}"] = 0
        rejects[f"ELIGIBILITY_PROBE_MISSED:{f}"] = 0
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
            inst, verdict = _generate_one(family, s, counter)
            if verdict == "INELIGIBLE":
                rejects[f"INELIGIBLE_NOT_A_CATEGORY:{family}"] += 1
                continue
            if inst is None:
                rejects[family] += 1
                continue
            try:
                same, a, _ = oracle_agrees(inst)
            except MapSpaceTooLarge:
                rejects[family] += 1
                continue
            if not same or a.disposition not in EXPECTED_DISPOSITION[family]:
                rejects[family] += 1
                continue
            # the eligibility checker is exercised on this very instance: two
            # law-breaking perturbations of the accepted donor must be caught
            for probe in (probe_deleted_composite, probe_rebound_identity):
                caught, _reason = probe_verdict(probe(inst.donor))
                if not caught:
                    rejects[f"ELIGIBILITY_PROBE_MISSED:{family}"] += 1
            made += 1
            pairs.append((inst, a))
    return pairs, rejects


# --------------------------------------------------------------------------
# parents (each with native known-answer tests; see `parent_fidelity`)
# --------------------------------------------------------------------------


def parent_name_similarity(inst: Instance) -> dict:
    """P0 - name/label correspondence, the "mere appearance" baseline.

    Rebuilds the object correspondence from identifier similarity and accepts
    the claim exactly when its own guess reproduces the registered candidate's
    object map.  This is the arm the name decoys exist to defeat; it is a real
    baseline in the analogy literature, not a strawman.
    """
    om = dict(inst.candidate.object_map)
    guess: dict[str, str] = {}
    used: set[str] = set()
    for d in inst.donor.objects:
        best, score = None, -1
        for t in inst.target.objects:
            if t in used:
                continue
            s = len(set(d) & set(t))
            if s > score:
                best, score = t, s
        if best is None:
            return {"disposition": "BLOCK_ENDPOINT_VIOLATION", "witness": None}
        guess[d] = best
        used.add(best)
    if guess == om:
        return {"disposition": "TRANSFER_VALID", "witness": tuple(sorted(guess.items()))}
    return {"disposition": "BLOCK_ENDPOINT_VIOLATION", "witness": tuple(sorted(guess.items()))}


def parent_graph_homomorphism(inst: Instance) -> dict:
    """P1 - underlying-graph homomorphism, composition-blind by construction.

    Checks only that every donor arrow's image runs between the images of its
    endpoints: the candidate is a morphism of directed graphs.  Identity and
    composition preservation are outside its competence, which is exactly the
    boundary between graph theory and category theory.
    """
    om = dict(inst.candidate.object_map)
    mm = dict(inst.candidate.morphism_map)
    tep = inst.target.endpoints
    for m, (s, t) in inst.donor.endpoints.items():
        if tep[mm[m]] != (om[s], om[t]):
            return {"disposition": "BLOCK_ENDPOINT_VIOLATION", "witness": None}
    return {"disposition": "TRANSFER_VALID", "witness": tuple(sorted(om.items()))}


def parent_category_law(inst: Instance) -> dict:
    """P2 - the category-law parent: `orion_v2.transfer_formal_mechanics.assess_functor`.

    The mature owner of the functor-law question and the strongest single formal
    parent for it: endpoint, identity and composition preservation, decided
    exactly.  It is law-level by construction and therefore blind to false
    equivalence - a functor that collapses two distinct morphisms violates no
    functor law.  That blindness is the measurement, not a handicap.
    """
    a = assess_functor(inst.donor, inst.target, inst.candidate)
    prof = {
        "ENDPOINT": a.endpoint_violations,
        "IDENTITY": a.identity_violations,
        "COMPOSITION": a.composition_violations,
        "COLLAPSE": 0,
        "TOTAL": a.endpoint_violations + a.identity_violations + a.composition_violations,
    }
    return {"disposition": classify(prof), "witness": None, "profile": prof}


def parent_diagram_chase(inst: Instance) -> dict:
    """P3 - diagram chasing over the registered commuting diagrams.

    The working mathematician's check: write down the diagrams the claim
    depends on and verify that their images commute.  Its documented boundary
    is that it sees only the registered diagrams and never the unit laws, so a
    claim that breaks an identity or an unregistered composite passes it.
    """
    mm = dict(inst.candidate.morphism_map)
    om = dict(inst.candidate.object_map)
    tep, tc = inst.target.endpoints, inst.target.compose
    dep = inst.donor.endpoints
    involved = sorted({m for d in inst.registered_diagrams for m in d})
    for m in involved:
        s, t = dep[m]
        if tep[mm[m]] != (om[s], om[t]):
            return {"disposition": "BLOCK_ENDPOINT_VIOLATION", "witness": None}
    for f, g, h in inst.registered_diagrams:
        if tc.get((mm[f], mm[g])) != mm[h]:
            return {"disposition": "BLOCK_COMPOSITION_NOT_PRESERVED", "witness": None}
    return {"disposition": "TRANSFER_VALID", "witness": None}


def parent_faithfulness(inst: Instance) -> dict:
    """P4 - the faithfulness parent: owns the false-equivalence stratum.

    Checks whether the candidate keeps the registered distinctions distinct and
    nothing else.  It performs no law checking at all, so it is blind to every
    functor-law obstruction; it is complete within its own competence.
    """
    mm = dict(inst.candidate.morphism_map)
    collapsed = [(a, b) for a, b in inst.distinguished_pairs if mm[a] == mm[b]]
    if collapsed:
        return {
            "disposition": "BLOCK_FALSE_EQUIVALENCE",
            "witness": None,
            "collapsed": [list(p) for p in collapsed],
        }
    return {"disposition": "TRANSFER_VALID", "witness": None, "collapsed": []}


def parent_fixed_lesson(inst: Instance) -> dict:
    """P5 - fixed-lesson injection.

    The "transfer lessons are a frozen table" baseline the protocol requires:
    the table holds exactly one lesson learned once - *a categorical transfer is
    valid when identities go to identities* - and applies it with no search, no
    composition chase and no faithfulness test.
    """
    mm = dict(inst.candidate.morphism_map)
    om = dict(inst.candidate.object_map)
    tid, did = inst.target.identity_map, inst.donor.identity_map
    for o in inst.donor.objects:
        if mm[did[o]] != tid[om[o]]:
            return {"disposition": "BLOCK_IDENTITY_NOT_PRESERVED", "witness": None}
    return {"disposition": "TRANSFER_VALID", "witness": None}


# --------------------------------------------------------------------------
# federation, mechanic and ablations
# --------------------------------------------------------------------------


def federation(inst: Instance) -> dict:
    """F0 - strongest faithful parent federation, under a pre-registered rule.

    Registered before any outcome and blind to it: the functor-law question is
    decided by the category-law parent (P2); if and only if P2 finds every law
    satisfied, the faithfulness parent (P4) is consulted and may veto the claim
    as a false equivalence.  Neither parent is consulted outside its native
    competence and neither ever sees the oracle.

    P3 is deliberately *not* a member.  On this endpoint every registered
    diagram is a composable pair of the donor's composition table, and P2
    checks every such pair, so diagram chasing is subsumed by the law parent.
    Recording that is a finding about the parent landscape, not an omission.
    """
    p2 = parent_category_law(inst)
    if p2["disposition"] != "TRANSFER_VALID":
        return {"disposition": p2["disposition"], "witness": None, "source": "P2"}
    p4 = parent_faithfulness(inst)
    if p4["disposition"] != "TRANSFER_VALID":
        return {"disposition": p4["disposition"], "witness": None, "source": "P4"}
    return {"disposition": "TRANSFER_VALID", "witness": None, "source": "P2+P4"}


def _mechanic(inst: Instance, *, endpoints=True, units=True, diagrams=True, recovery=True) -> dict:
    """M - ORION L2 functorial transfer discovery, with switchable stages.

    An independent implementation: it never calls `assess_functor` (the parent's
    call) and never calls the study's own `claim_profile` (the oracle's).  It
    rebuilds the donor's structural description from `source_target` and
    `composition`, discovers the donor's commuting triangles for itself rather
    than trusting the registered diagram list, projects the claim through the
    target's composition index, runs native recovery on the registered
    distinctions, and resolves the obstruction precedence itself.
    """
    donor, target, cand = inst.donor, inst.target, inst.candidate
    om = dict(cand.object_map)
    mm = dict(cand.morphism_map)

    # --- structural description, rebuilt from the raw tables ---------------
    d_src = {m: s for m, s, _ in donor.source_target}
    d_dst = {m: t for m, _, t in donor.source_target}
    d_unit = {o: i for o, i in donor.identities}
    d_tri = sorted((f, g, h) for f, g, h in donor.composition)
    t_src = {m: s for m, s, _ in target.source_target}
    t_dst = {m: t for m, _, t in target.source_target}
    t_unit = {o: i for o, i in target.identities}
    t_comp = {(f, g): h for f, g, h in target.composition}

    endpoint_v = unit_v = triangle_v = collapse_v = 0
    if endpoints:
        for m in donor.morphisms:
            image = mm[m]
            if t_src[image] != om[d_src[m]] or t_dst[image] != om[d_dst[m]]:
                endpoint_v += 1
    if units:
        for o in donor.objects:
            if mm[d_unit[o]] != t_unit[om[o]]:
                unit_v += 1
    if diagrams:
        # discovered, not registered: every commuting triangle the donor has
        for f, g, h in d_tri:
            if t_comp.get((mm[f], mm[g])) != mm[h]:
                triangle_v += 1
    if recovery:
        for a, b in inst.distinguished_pairs:
            if mm[a] == mm[b]:
                collapse_v += 1

    prof = {
        "ENDPOINT": endpoint_v,
        "IDENTITY": unit_v,
        "COMPOSITION": triangle_v,
        "COLLAPSE": collapse_v,
        "TOTAL": endpoint_v + unit_v + triangle_v + collapse_v,
    }
    return {"disposition": classify(prof), "witness": None, "profile": prof}


def mechanic_full(inst: Instance) -> dict:
    return _mechanic(inst)


def ablation_minus_endpoint_discipline(inst: Instance) -> dict:
    return _mechanic(inst, endpoints=False)


def ablation_minus_identity_check(inst: Instance) -> dict:
    return _mechanic(inst, units=False)


def ablation_minus_composition_check(inst: Instance) -> dict:
    return _mechanic(inst, diagrams=False)


def ablation_minus_faithfulness_recovery(inst: Instance) -> dict:
    return _mechanic(inst, recovery=False)


def control_always_transfer(inst: Instance) -> dict:
    return {"disposition": "TRANSFER_VALID", "witness": None}


def control_always_block(inst: Instance) -> dict:
    return {"disposition": "BLOCK_COMPOSITION_NOT_PRESERVED", "witness": None}


def control_random(inst: Instance) -> dict:
    return {"disposition": random.Random(inst.seed ^ 0x5EED).choice(DISPOSITIONS), "witness": None}


ARM_FUNCTIONS = {
    "P0_NAME_SIMILARITY": parent_name_similarity,
    "P1_GRAPH_HOMOMORPHISM": parent_graph_homomorphism,
    "P2_CATEGORY_LAW_FUNCTOR": parent_category_law,
    "P3_DIAGRAM_CHASE": parent_diagram_chase,
    "P4_FAITHFULNESS": parent_faithfulness,
    "P5_FIXED_LESSON_INJECTION": parent_fixed_lesson,
    "F0_PARENT_FEDERATION": federation,
    "M_F2_FUNCTORIAL_TRANSFER_FULL": mechanic_full,
    "M_MINUS_ENDPOINT_DISCIPLINE": ablation_minus_endpoint_discipline,
    "M_MINUS_IDENTITY_CHECK": ablation_minus_identity_check,
    "M_MINUS_COMPOSITION_CHECK": ablation_minus_composition_check,
    "M_MINUS_FAITHFULNESS_RECOVERY": ablation_minus_faithfulness_recovery,
    "C_ALWAYS_TRANSFER": control_always_transfer,
    "C_ALWAYS_BLOCK": control_always_block,
    "C_RANDOM_DISPOSITION": control_random,
}


def run_arm(arm: str, inst: Instance) -> dict:
    out = ARM_FUNCTIONS[arm](inst)
    w = out.get("witness")
    return {
        "disposition": out["disposition"],
        "witness": [list(p) for p in w] if w else None,
        "source": out.get("source"),
    }


# --------------------------------------------------------------------------
# hand-authored known-answer fixtures (G0a)
# --------------------------------------------------------------------------


def _build(carriers: dict[str, int], gens: Sequence[Mor], alias: dict[str, str] | None = None,
           cap: int = 18):
    mors = close_under_composition(carriers, gens, cap=cap)
    if mors is None:  # pragma: no cover - fixtures are sized by hand
        raise RuntimeError("fixture closure exceeded the cap")
    return build_category(carriers, mors, object_alias=alias), _morphism_names(carriers, mors), mors


def _fixture(
    name: str,
    family: str,
    dcar: dict[str, int],
    dgens: Sequence[Mor],
    tcar: dict[str, int],
    tgens: Sequence[Mor],
    objmap: dict[str, str],
    mormap: dict[Mor, Mor],
    distinguished: Sequence[tuple[Mor, Mor]],
    expected: str,
    alias: dict[str, str] | None = None,
) -> dict:
    donor, dnames, dmors = _build(dcar, dgens)
    target, tnames, tmors = _build(tcar, tgens, alias)
    on = alias or {}
    mm: dict[str, str] = {}
    for m in sorted(dmors):
        image = mormap.get(m, m)
        mm[dnames[m]] = tnames[image]
    om = {d: on.get(t, t) for d, t in objmap.items()}
    ident = {f"id_{o}" for o in dcar}
    diagrams = tuple(
        sorted((f, g, h) for f, g, h in donor.composition if f not in ident and g not in ident)
    ) or tuple(sorted(donor.composition))
    inst = Instance(
        instance_id=name,
        family=family,
        seed=0,
        donor=donor,
        target=target,
        candidate=FunctorCandidate(
            object_map=tuple(sorted(om.items())),
            morphism_map=tuple(sorted(mm.items())),
        ),
        distinguished_pairs=tuple(sorted((dnames[a], dnames[b]) for a, b in distinguished)),
        registered_diagrams=diagrams,
        surface_pairs=tuple((o, f"{o}_t") for o in sorted(dcar)),
    )
    return {"name": name, "instance": inst, "expected": expected}


# the running example: A with a swap endomorphism, an injective arrow A -> B
SWAP = ("A", "A", (1, 0))
ARROW = ("A", "B", (0, 1))
ARROW2 = ("A", "B", (1, 0))
ID_A = ("A", "A", (0, 1))
ID_B = ("B", "B", (0, 1))
CONST_A = ("A", "A", (0, 0))
BASE_CAR = {"A": 2, "B": 2}
BASE_GENS = (SWAP, ARROW)


def known_answer_fixtures() -> list[dict]:
    F: list[dict] = []

    F.append(_fixture(
        "KA-01-IDENTITY-FUNCTOR", "VALID_FUNCTOR",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {}, [(ID_A, SWAP)], "TRANSFER_VALID",
    ))
    F.append(_fixture(
        "KA-02-EMBEDDING-IN-LARGER-TARGET", "VALID_FUNCTOR",
        BASE_CAR, BASE_GENS,
        {"A": 2, "B": 2, "Z": 1}, (SWAP, ARROW, ("A", "Z", (0, 0)), ("Z", "B", (0,))),
        {"A": "A", "B": "B"}, {}, [(ARROW, ARROW2)], "TRANSFER_VALID",
    ))
    F.append(_fixture(
        "KA-03-ENDPOINT-VIOLATION", "ENDPOINT_VIOLATION",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {ARROW: SWAP}, [], "BLOCK_ENDPOINT_VIOLATION",
    ))
    # a one-object monoid {id, c} with c idempotent: sending the unit to c
    # breaks the unit law and nothing else, so the class is pure
    F.append(_fixture(
        "KA-04-IDENTITY-NOT-PRESERVED", "IDENTITY_NOT_PRESERVED",
        {"A": 2}, (CONST_A,), {"A": 2}, (CONST_A,),
        {"A": "A"}, {ID_A: CONST_A}, [], "BLOCK_IDENTITY_NOT_PRESERVED",
    ))
    F.append(_fixture(
        "KA-05-COMPOSITION-NOT-PRESERVED", "COMPOSITION_NOT_PRESERVED",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {ARROW: ARROW2}, [], "BLOCK_COMPOSITION_NOT_PRESERVED",
    ))
    F.append(_fixture(
        "KA-06-MIXED-LAW-OBSTRUCTION", "MIXED_LAW_OBSTRUCTION",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {ID_A: SWAP}, [], "BLOCK_MIXED_LAW_OBSTRUCTION",
    ))
    # the constant functor to the terminal category is always a functor; it is a
    # false equivalence exactly when the claim depends on a distinction it kills
    F.append(_fixture(
        "KA-07-FALSE-EQUIVALENCE-CONSTANT-FUNCTOR", "FALSE_EQUIVALENCE",
        BASE_CAR, BASE_GENS, {"O": 1}, (),
        {"A": "O", "B": "O"},
        {ID_A: ("O", "O", (0,)), SWAP: ("O", "O", (0,)), ARROW: ("O", "O", (0,)),
         ARROW2: ("O", "O", (0,)), ID_B: ("O", "O", (0,))},
        [(ARROW, ARROW2)], "BLOCK_FALSE_EQUIVALENCE",
    ))
    F.append(_fixture(
        "KA-08-LICENSED-COLLAPSE", "LICENSED_COLLAPSE",
        BASE_CAR, BASE_GENS,
        {"A": 2, "B": 2, "Z": 1}, (SWAP, ARROW, ("A", "Z", (0, 0)), ("Z", "B", (0,))),
        {"A": "A", "B": "Z"},
        {ARROW: ("A", "Z", (0, 0)), ARROW2: ("A", "Z", (0, 0)), ID_B: ("Z", "Z", (0,))},
        [(ID_A, SWAP)], "TRANSFER_VALID",
    ))
    # precedence pins: an endpoint violation dominates a collapse, and a mixed
    # law obstruction is reported as mixed rather than as either half
    F.append(_fixture(
        "KA-09-ENDPOINT-DOMINATES-COLLAPSE", "ENDPOINT_VIOLATION",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {ARROW: SWAP, ARROW2: SWAP}, [(ARROW, ARROW2)],
        "BLOCK_ENDPOINT_VIOLATION",
    ))
    F.append(_fixture(
        "KA-10-COMPOSITION-DOMINATES-COLLAPSE", "COMPOSITION_NOT_PRESERVED",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {ARROW: ARROW2}, [(ARROW, ARROW2)],
        "BLOCK_COMPOSITION_NOT_PRESERVED",
    ))
    # a decoy whose target object names are deranged: the registered candidate is
    # correct and the name-similarity guess is exactly wrong
    F.append(_fixture(
        "KA-11-SURFACE-NAME-DECOY", "SURFACE_NAME_DECOY",
        BASE_CAR, BASE_GENS, BASE_CAR, BASE_GENS,
        {"A": "A", "B": "B"}, {}, [(ARROW, ARROW2)], "TRANSFER_VALID",
        alias={"A": "B_t", "B": "A_t"},
    ))
    return F


# --------------------------------------------------------------------------
# parent fidelity: native known-answer tests (must pass before use)
# --------------------------------------------------------------------------


def parent_fidelity() -> list[dict]:
    """Native tests every comparator must pass before it is used as one.

    Entries whose `parent` is `ELIGIBILITY_GATE` are gate tests, not comparator
    tests; the receipt reports the two counts separately so that the number of
    parents that earned their place is not inflated by them.
    """
    T: list[dict] = []
    fx = {f["name"]: f["instance"] for f in known_answer_fixtures()}

    def check(parent: str, name: str, ok: bool, detail: str = "") -> None:
        T.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    # ---- P2 category-law parent (the reference module's assess_functor) ----
    check(
        "P2_CATEGORY_LAW_FUNCTOR", "identity_functor_is_valid",
        parent_category_law(fx["KA-01-IDENTITY-FUNCTOR"])["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P2_CATEGORY_LAW_FUNCTOR", "endpoint_violation_is_reported_as_such",
        parent_category_law(fx["KA-03-ENDPOINT-VIOLATION"])["disposition"]
        == "BLOCK_ENDPOINT_VIOLATION",
    )
    check(
        "P2_CATEGORY_LAW_FUNCTOR",
        "object_preserving_non_functor_that_breaks_composition_is_caught",
        parent_category_law(fx["KA-05-COMPOSITION-NOT-PRESERVED"])["disposition"]
        == "BLOCK_COMPOSITION_NOT_PRESERVED",
        "the classic non-functor: objects and endpoints preserved, composition not",
    )
    check(
        "P2_CATEGORY_LAW_FUNCTOR", "unit_law_violation_is_caught",
        parent_category_law(fx["KA-04-IDENTITY-NOT-PRESERVED"])["disposition"]
        == "BLOCK_IDENTITY_NOT_PRESERVED",
    )
    check(
        "P2_CATEGORY_LAW_FUNCTOR", "mixed_unit_and_composition_failure_is_reported_as_mixed",
        parent_category_law(fx["KA-06-MIXED-LAW-OBSTRUCTION"])["disposition"]
        == "BLOCK_MIXED_LAW_OBSTRUCTION",
    )
    check(
        "P2_CATEGORY_LAW_FUNCTOR", "documented_boundary_blind_to_false_equivalence",
        parent_category_law(fx["KA-07-FALSE-EQUIVALENCE-CONSTANT-FUNCTOR"])["disposition"]
        == "TRANSFER_VALID",
        "scope note: the constant functor satisfies every functor law, so a "
        "law parent cannot see a collapsed distinction",
    )

    # ---- P3 diagram chasing ----------------------------------------------
    check(
        "P3_DIAGRAM_CHASE", "commuting_diagram_whose_image_commutes_is_accepted",
        parent_diagram_chase(fx["KA-01-IDENTITY-FUNCTOR"])["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P3_DIAGRAM_CHASE", "registered_diagram_that_fails_to_commute_is_caught",
        parent_diagram_chase(fx["KA-05-COMPOSITION-NOT-PRESERVED"])["disposition"]
        == "BLOCK_COMPOSITION_NOT_PRESERVED",
    )
    check(
        "P3_DIAGRAM_CHASE", "documented_boundary_unit_laws_are_outside_the_registered_diagrams",
        parent_diagram_chase(fx["KA-04-IDENTITY-NOT-PRESERVED"])["disposition"]
        == "TRANSFER_VALID",
        "scope note: diagram chasing checks the diagrams the claim writes down; "
        "unit preservation is not one of them",
    )

    # ---- P4 faithfulness --------------------------------------------------
    check(
        "P4_FAITHFULNESS", "collapsed_registered_distinction_is_blocked",
        parent_faithfulness(fx["KA-07-FALSE-EQUIVALENCE-CONSTANT-FUNCTOR"])["disposition"]
        == "BLOCK_FALSE_EQUIVALENCE",
    )
    check(
        "P4_FAITHFULNESS", "separated_distinctions_license_the_collapse_elsewhere",
        parent_faithfulness(fx["KA-08-LICENSED-COLLAPSE"])["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P4_FAITHFULNESS", "documented_boundary_blind_to_every_functor_law",
        parent_faithfulness(fx["KA-05-COMPOSITION-NOT-PRESERVED"])["disposition"]
        == "TRANSFER_VALID",
        "scope note: P4 performs no law checking",
    )

    # ---- P1 graph homomorphism -------------------------------------------
    check(
        "P1_GRAPH_HOMOMORPHISM", "accepts_a_morphism_of_the_underlying_graphs",
        parent_graph_homomorphism(fx["KA-01-IDENTITY-FUNCTOR"])["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P1_GRAPH_HOMOMORPHISM", "rejects_an_image_with_the_wrong_endpoints",
        parent_graph_homomorphism(fx["KA-03-ENDPOINT-VIOLATION"])["disposition"]
        == "BLOCK_ENDPOINT_VIOLATION",
    )
    check(
        "P1_GRAPH_HOMOMORPHISM", "documented_boundary_composition_is_invisible_to_a_graph_map",
        parent_graph_homomorphism(fx["KA-05-COMPOSITION-NOT-PRESERVED"])["disposition"]
        == "TRANSFER_VALID",
        "scope note: this is exactly the gap between graph theory and category theory",
    )

    # ---- P0 name similarity ----------------------------------------------
    check(
        "P0_NAME_SIMILARITY", "prefers_the_name_similar_object_and_so_fails_the_decoy",
        parent_name_similarity(fx["KA-11-SURFACE-NAME-DECOY"])["disposition"]
        == "BLOCK_ENDPOINT_VIOLATION",
        "the behaviour surface decoys exist to expose",
    )
    check(
        "P0_NAME_SIMILARITY", "accepts_when_the_names_line_up_with_the_registered_candidate",
        parent_name_similarity(fx["KA-01-IDENTITY-FUNCTOR"])["disposition"] == "TRANSFER_VALID",
    )

    # ---- P5 fixed lesson --------------------------------------------------
    check(
        "P5_FIXED_LESSON_INJECTION", "blocks_when_the_one_frozen_lesson_is_violated",
        parent_fixed_lesson(fx["KA-04-IDENTITY-NOT-PRESERVED"])["disposition"]
        == "BLOCK_IDENTITY_NOT_PRESERVED",
    )
    check(
        "P5_FIXED_LESSON_INJECTION", "transfers_whenever_the_frozen_lesson_is_satisfied",
        parent_fixed_lesson(fx["KA-05-COMPOSITION-NOT-PRESERVED"])["disposition"]
        == "TRANSFER_VALID",
        "scope note: one lesson, applied without search",
    )

    # ---- reference module -------------------------------------------------
    inst = fx["KA-06-MIXED-LAW-OBSTRUCTION"]
    a = assess_functor(inst.donor, inst.target, inst.candidate)
    own = claim_profile(inst)
    check(
        "REFERENCE_MODULE", "assess_functor_agrees_with_this_modules_own_law_loop",
        (a.endpoint_violations, a.identity_violations, a.composition_violations)
        == (own["ENDPOINT"], own["IDENTITY"], own["COMPOSITION"]),
        f"{a} vs {own}",
    )
    lawful_cat, lawful_reason = try_build_category(
        BASE_CAR, close_under_composition(BASE_CAR, BASE_GENS, cap=10)
    )
    check(
        "REFERENCE_MODULE", "finite_category_admits_a_closed_concrete_construction",
        lawful_cat is not None, str(lawful_reason),
    )
    caught_assoc, assoc_reason = probe_verdict(probe_non_associative_monoid())
    check(
        "REFERENCE_MODULE", "finite_category_rejects_a_non_associative_composition_table",
        caught_assoc and "associativity" in assoc_reason, assoc_reason,
    )

    # ---- eligibility gate (gate tests, not comparator tests) --------------
    audit = eligibility_audit()
    gate = eligibility_gate(audit)
    check(
        "ELIGIBILITY_GATE", "lawful_constructions_are_admitted",
        all(x["admitted"] for x in audit["lawful"]),
        f"{sum(x['admitted'] for x in audit['lawful'])}/{len(audit['lawful'])}",
    )
    check(
        "ELIGIBILITY_GATE", "law_breaking_constructions_are_caught",
        all(x["caught"] for x in audit["law_breaking"]),
        f"{sum(x['caught'] for x in audit['law_breaking'])}/{len(audit['law_breaking'])}",
    )
    check(
        "ELIGIBILITY_GATE", "non_associative_table_is_caught_by_the_associativity_law",
        "associativity" in audit["associativity_probe_reason"],
        audit["associativity_probe_reason"],
    )
    caught_del, reason_del = probe_verdict(probe_deleted_composite(fx["KA-01-IDENTITY-FUNCTOR"].donor))
    check(
        "ELIGIBILITY_GATE", "deleted_composite_is_caught_by_the_completeness_law",
        caught_del and "composition table" in reason_del, reason_del,
    )
    caught_id, reason_id = probe_verdict(probe_rebound_identity(fx["KA-01-IDENTITY-FUNCTOR"].donor))
    check(
        "ELIGIBILITY_GATE", "rebound_identity_is_caught_by_the_identity_laws",
        caught_id and "identity" in reason_id, reason_id,
    )
    empty = eligibility_gate({"lawful": [], "law_breaking": [], "n_evaluated": 0,
                              "n_violations": 0, "associativity_probe_reason": ""})
    check(
        "ELIGIBILITY_GATE", "an_unevaluated_eligibility_gate_reports_CANNOT_CHECK_not_PASS",
        empty.verdict == "CANNOT_CHECK" and gate.verdict == "PASS",
        f"empty={empty.verdict} live={gate.verdict} n={gate.n_evaluated}",
    )

    # ---- F0 federation: the named comparator, tested like any parent ------
    # A comparator whose fidelity is asserted but never checked is a rendered
    # status.  F0 composes the law parent (P2) and the faithfulness parent (P4)
    # under the registered rule (P2 decides every law; P4 is consulted only when
    # every law holds), so the identity check at the end is a check on that rule
    # and is labelled as an identity, not as independent evidence about M.
    law_fixtures = {
        "KA-03-ENDPOINT-VIOLATION": "BLOCK_ENDPOINT_VIOLATION",
        "KA-04-IDENTITY-NOT-PRESERVED": "BLOCK_IDENTITY_NOT_PRESERVED",
        "KA-05-COMPOSITION-NOT-PRESERVED": "BLOCK_COMPOSITION_NOT_PRESERVED",
        "KA-06-MIXED-LAW-OBSTRUCTION": "BLOCK_MIXED_LAW_OBSTRUCTION",
        "KA-09-ENDPOINT-DOMINATES-COLLAPSE": "BLOCK_ENDPOINT_VIOLATION",
        "KA-10-COMPOSITION-DOMINATES-COLLAPSE": "BLOCK_COMPOSITION_NOT_PRESERVED",
    }
    check(
        "F0_PARENT_FEDERATION",
        "takes_the_law_parent_on_every_law_violation_including_the_precedence_fixtures",
        all(
            federation(fx[k])["source"] == "P2" and federation(fx[k])["disposition"] == d
            for k, d in law_fixtures.items()
        ),
    )
    fe = federation(fx["KA-07-FALSE-EQUIVALENCE-CONSTANT-FUNCTOR"])
    check(
        "F0_PARENT_FEDERATION",
        "consults_the_faithfulness_parent_only_after_every_law_holds",
        fe["source"] == "P4" and fe["disposition"] == "BLOCK_FALSE_EQUIVALENCE",
    )
    check(
        "F0_PARENT_FEDERATION",
        "accepts_only_when_both_parents_accept",
        all(
            federation(fx[k])["source"] == "P2+P4" and federation(fx[k])["disposition"] == "TRANSFER_VALID"
            for k in ("KA-01-IDENTITY-FUNCTOR", "KA-08-LICENSED-COLLAPSE", "KA-11-SURFACE-NAME-DECOY")
        ),
    )
    ident = [
        (f["name"], federation(f["instance"])["disposition"], oracle_exhaustive(f["instance"]).disposition)
        for f in known_answer_fixtures()
    ]
    check(
        "F0_PARENT_FEDERATION",
        "composition_rule_reproduces_the_oracle_on_every_registered_fixture__IDENTITY_NOT_MEASUREMENT",
        all(a == b for _, a, b in ident),
        f"{sum(a == b for _, a, b in ident)}/{len(ident)} fixtures; F0 composes two "
        "complete predicates, so its agreement with the oracle is entailed by "
        "construction: this checks the composition rule and is not evidence about M",
    )
    return T


# --------------------------------------------------------------------------
# planted positives (trip-wires: every no-alarm assertion must be shown to fire)
# --------------------------------------------------------------------------


def _pseudo_count_first_object_map(inst: Instance) -> int:
    """A deliberately incomplete oracle: only the first object map is searched."""
    donor, target = inst.donor, inst.target
    tc = target.compose
    om = dict(zip(donor.objects, [target.objects[0]] * len(donor.objects)))
    slots = _candidate_images(donor, target, om)
    if slots is None:
        return 0
    keys = [m for m, _ in slots]
    total = 0
    for choice in product(*[c for _, c in slots]):
        mm = dict(zip(keys, choice))
        if any(tc.get((mm[f], mm[g])) != mm[h] for (f, g), h in donor.compose.items()):
            continue
        if any(mm[a] == mm[b] for a, b in inst.distinguished_pairs):
            continue
        total += 1
    return total


def planted_positives() -> list[PlantedPositive]:
    from fm_core import discrimination_gate

    P = [
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "single_object_map_pseudo_oracle_is_detected",
            "an oracle that searches only the first object map must disagree with "
            "exhaustive enumeration on the valid-functor count of a hand-built instance",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "wrong_expected_label_is_detected",
            "the known-answer comparison must reject a deliberately wrong expected "
            "disposition",
        ),
        PlantedPositive(
            "G2_ANTI_PERMISSIVENESS",
            "over_transferring_arm_is_detected",
            "the over-transfer counter must count C_ALWAYS_TRANSFER on an "
            "oracle-blocked instance",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_ceiling_split_is_detected",
            "a synthetic per-arm table where every arm scores 1.0 must FAIL the "
            "discrimination gate (the FM/FG R2 ceiling defect that made the "
            "LLM-dispatch fm50 cell uninformative)",
        ),
        PlantedPositive(
            "G3_MECHANISM_BY_OMISSION",
            "faithfulness_ablation_loses_the_false_equivalence_family",
            "M_MINUS_FAITHFULNESS_RECOVERY must be wrong on a hand-built false "
            "equivalence on which M is right",
        ),
        PlantedPositive(
            "G0g_ELIGIBILITY",
            "non_associative_construction_is_caught_not_counted_as_a_negative",
            "a deliberately non-associative composition table must be caught by "
            "the eligibility checker and reported INELIGIBLE, never scored as a "
            "negative result about any arm",
        ),
    ]
    fx = {f["name"]: f for f in known_answer_fixtures()}

    emb = fx["KA-02-EMBEDDING-IN-LARGER-TARGET"]["instance"]
    P[0].fired = _pseudo_count_first_object_map(emb) != oracle_exhaustive(emb).n_valid_functors

    P[1].fired = oracle_exhaustive(fx["KA-01-IDENTITY-FUNCTOR"]["instance"]).disposition != (
        "BLOCK_COMPOSITION_NOT_PRESERVED"
    )

    blocked = fx["KA-05-COMPOSITION-NOT-PRESERVED"]["instance"]
    P[2].fired = control_always_transfer(blocked)["disposition"] == "TRANSFER_VALID" and (
        oracle_exhaustive(blocked).disposition != "TRANSFER_VALID"
    )

    P[3].fired = (
        discrimination_gate(
            {a: 1.0 for a in ARM_FUNCTIONS},
            weak_arms=("C_RANDOM_DISPOSITION",),
            max_weak=0.60,
            min_strong=0.95,
        ).verdict
        == "FAIL"
    )

    fe = fx["KA-07-FALSE-EQUIVALENCE-CONSTANT-FUNCTOR"]["instance"]
    P[4].fired = (
        mechanic_full(fe)["disposition"] == "BLOCK_FALSE_EQUIVALENCE"
        and ablation_minus_faithfulness_recovery(fe)["disposition"] != "BLOCK_FALSE_EQUIVALENCE"
    )

    caught, reason = probe_verdict(probe_non_associative_monoid())
    P[5].fired = caught and "associativity" in reason
    return P


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------

SPEC = SuiteSpec(
    suite_id="FM50",
    title="Functoriality and commuting diagrams with exact obstruction classification",
    families=FAMILIES,
    arms=(
        ArmSpec("P0_NAME_SIMILARITY", "PARENT", "identifier/label correspondence baseline"),
        ArmSpec("P1_GRAPH_HOMOMORPHISM", "PARENT",
                "underlying-graph homomorphism; composition- and unit-blind"),
        ArmSpec("P2_CATEGORY_LAW_FUNCTOR", "PARENT",
                "category-law parent: orion_v2.transfer_formal_mechanics.assess_functor"),
        ArmSpec("P3_DIAGRAM_CHASE", "PARENT",
                "diagram chasing over the registered commuting diagrams"),
        ArmSpec("P4_FAITHFULNESS", "PARENT",
                "faithfulness on the registered distinctions; owns false equivalence"),
        ArmSpec("P5_FIXED_LESSON_INJECTION", "PARENT", "frozen one-lesson transfer table"),
        ArmSpec("F0_PARENT_FEDERATION", "FEDERATION",
                "strongest faithful parent federation under a pre-registered outcome-blind rule"),
        ArmSpec("M_F2_FUNCTORIAL_TRANSFER_FULL", "MECHANIC",
                "ORION L2 functorial transfer discovery, full"),
        ArmSpec("M_MINUS_ENDPOINT_DISCIPLINE", "ABLATION", ""),
        ArmSpec("M_MINUS_IDENTITY_CHECK", "ABLATION", ""),
        ArmSpec("M_MINUS_COMPOSITION_CHECK", "ABLATION", ""),
        ArmSpec("M_MINUS_FAITHFULNESS_RECOVERY", "ABLATION", ""),
        ArmSpec("C_ALWAYS_TRANSFER", "CONTROL", ""),
        ArmSpec("C_ALWAYS_BLOCK", "CONTROL", ""),
        ArmSpec("C_RANDOM_DISPOSITION", "CONTROL", ""),
    ),
    mechanic_arm="M_F2_FUNCTORIAL_TRANSFER_FULL",
    strongest_parent_arm="F0_PARENT_FEDERATION",
    federation_arm="F0_PARENT_FEDERATION",
    weak_arms=(
        "P0_NAME_SIMILARITY",
        "P1_GRAPH_HOMOMORPHISM",
        "P3_DIAGRAM_CHASE",
        "P5_FIXED_LESSON_INJECTION",
    ),
    constant_arms=("C_ALWAYS_TRANSFER", "C_ALWAYS_BLOCK"),
    random_arm="C_RANDOM_DISPOSITION",
    ablation_for_family={
        "LICENSED_COLLAPSE": "M_MINUS_FAITHFULNESS_RECOVERY",
        "FALSE_EQUIVALENCE": "M_MINUS_FAITHFULNESS_RECOVERY",
        "ENDPOINT_VIOLATION": "M_MINUS_ENDPOINT_DISCIPLINE",
        "IDENTITY_NOT_PRESERVED": "M_MINUS_IDENTITY_CHECK",
        "COMPOSITION_NOT_PRESERVED": "M_MINUS_COMPOSITION_CHECK",
        "MIXED_LAW_OBSTRUCTION": "M_MINUS_COMPOSITION_CHECK",
    },
    default_ablation="M_MINUS_IDENTITY_CHECK",
    decoy_families=(
        "SURFACE_NAME_DECOY",
        "LICENSED_COLLAPSE",
        "IDENTITY_NOT_PRESERVED",
        "FALSE_EQUIVALENCE",
    ),
    min_tasks=96,
    dev_per_family=3,
    protected_per_family=13,  # 8 x 13 = 104 >= 96
    design_json="FM50_FUNCTORIALITY_COMMUTING_DIAGRAMS_EXACT_STUDY_DESIGN_V1.json",
    generate=generate_split,
    oracle=oracle_exhaustive,
    cross_check=oracle_constraint_search,
    run_arm=run_arm,
    parent_fidelity=parent_fidelity,
    known_answer_fixtures=known_answer_fixtures,
    planted_positives=planted_positives,
)
