#!/usr/bin/env python3
"""FM40 — invariance/equivariance discovery: exact generator, oracle and faithful parents.

The registered task is deliberately *not* "is this property invariant".  Testing
invariance under a given generating set is a two-line check, so a study built on
it would report parent sufficiency by construction rather than by measurement.
Each FM40 instance instead asks for a **transfer disposition over a finite group
action**, which forces four strata to be decided together:

    TRANSFER_VALID                      the candidate property is invariant under
                                        the WHOLE generated group; the donor's
                                        claim transfers unrestricted;
    BLOCK_EQUIVARIANT_NOT_INVARIANT     the property is not preserved pointwise
                                        but covaries: some value-space action rho
                                        satisfies p(g.x) = rho(g)(p(x)) for every
                                        g and x, so the transformation must be
                                        carried along with the claim;
    BLOCK_REGIME_BOUNDED_INVARIANT      some group element genuinely breaks the
                                        property, but the property is invariant on
                                        the registered proper G-stable sub-regime;
    BLOCK_SURFACE_SYMMETRY_ONLY         the property is broken, and the break is
                                        invisible in the registered surface
                                        encoding: the symmetry that is present is
                                        a symmetry of the re-description, not of
                                        the property (the false-invariance trap);
    BLOCK_NON_INVARIANT                 the property is broken and the break is
                                        visible at the surface, with no regime
                                        that rescues it.

`TRANSFER_VALID` is the FM-series name for the unrestricted-transfer
disposition; here it means exactly INVARIANT-UNDER-THE-WHOLE-GROUP.  The shared
runner's anti-permissiveness gate (`G2`) is keyed on that string, which makes
`G2` FM40's **false-invariance gate** — a registered primary of the protocol —
rather than a check with an empty denominator.

Consequence, and the reason the suite is worth running: **no single parent family
owns the endpoint.**  Orbit/stabiliser computation decides invariance exactly and
has no notion of a value-space action; an equivariance solver owns the
invariance/equivariance stratum and is blind to the regime and surface strata;
an augmentation-based empirical symmetry detector is exact on the witnessed
subgroup and structurally blind to everything outside it.  The strongest faithful
comparator is therefore their *federation*, exactly as ME-X4's B5 was, and the
pre-registered expectation is that the federation reproduces the ORION mechanic.

Unseen transformations are a first-class part of the model: every instance
publishes a generating set for `G` and a **witnessed subset** `W` whose generated
subgroup is a proper subgroup of `G`.  Two families are built so that the answer
read off `<W>` alone is wrong, which is the protocol's own
`unseen_transformation_generalization` primary.

Oracle validity rests on two algorithms that rest on *different theorems*
agreeing on (disposition, stratum profile, orbit count, value count):

  * `oracle_element_closure`     — materialise the whole group by BFS closure and
    classify every element pointwise by the relation R_g = {(p(x), p(g.x))};
  * `oracle_generator_blocks`    — never materialise the group at all: use the
    fact that the stabiliser of `p` and the set of block-preserving elements are
    both subgroups, so checking the *generators* suffices, and decide each
    generator by set-image block-system tests on the level-set partition.

If the closure in the first is wrong, or the subgroup argument in the second is
misapplied, they disagree and `G0b` fires.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, replace
from itertools import permutations
from typing import Callable, Sequence

from fm_core import ArmSpec, PlantedPositive, SuiteSpec

from orion_v2.transfer_formal_mechanics import TransformationCase, assess_invariance

# --------------------------------------------------------------------------
# task model
# --------------------------------------------------------------------------

FAMILIES = (
    "FULL_INVARIANCE",
    "EQUIVARIANT_ACTION",
    "NON_INVARIANT",
    "SURFACE_ONLY_SYMMETRY",
    "PARTIAL_REGIME_INVARIANCE",
    "UNSEEN_TRANSFORMATION_BREAK",
    "UNSEEN_TRANSFORMATION_EQUIVARIANCE",
)

DISPOSITIONS = (
    "TRANSFER_VALID",
    "BLOCK_EQUIVARIANT_NOT_INVARIANT",
    "BLOCK_REGIME_BOUNDED_INVARIANT",
    "BLOCK_SURFACE_SYMMETRY_ONLY",
    "BLOCK_NON_INVARIANT",
)

# registered instance envelope
SHAPES = ((3, 2), (3, 3), (4, 2))
MAX_GROUP_ORDER = 64

# M's registered sample schedule (see `mechanic_full`)
SAMPLE_SCHEDULE = (("random", 6), ("random", 14), ("random", 24), ("stratified", 24))

Elt = tuple[tuple[int, ...], tuple[int, ...]]  # (site permutation, colour permutation)


@dataclass(frozen=True)
class Instance:
    instance_id: str
    family: str
    seed: int
    n_sites: int
    n_colors: int
    generators: tuple[Elt, ...]
    witnessed: tuple[Elt, ...]
    property_id: str
    surface_id: str
    regime_tag_id: str
    regime_values: tuple[str, ...]

    def as_json(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,
            "n_sites": self.n_sites,
            "n_colors": self.n_colors,
            "generators": [[list(s), list(c)] for s, c in self.generators],
            "witnessed": [[list(s), list(c)] for s, c in self.witnessed],
            "property_id": self.property_id,
            "surface_id": self.surface_id,
            "regime_tag_id": self.regime_tag_id,
            "regime_values": list(self.regime_values),
        }


# --------------------------------------------------------------------------
# the group action:  (sigma, tau) . x  =  y   with   y[sigma(i)] = tau(x[i])
# --------------------------------------------------------------------------


def act(elt: Elt, x: tuple[int, ...]) -> tuple[int, ...]:
    sigma, tau = elt
    y = [0] * len(x)
    for i, c in enumerate(x):
        y[sigma[i]] = tau[c]
    return tuple(y)


def compose(a: Elt, b: Elt) -> Elt:
    """`a` after `b`: act(compose(a, b), x) == act(a, act(b, x))."""
    sa, ta = a
    sb, tb = b
    return (tuple(sa[i] for i in sb), tuple(ta[c] for c in tb))


def identity_elt(m: int, q: int) -> Elt:
    return (tuple(range(m)), tuple(range(q)))


def configurations(m: int, q: int) -> tuple[tuple[int, ...], ...]:
    out: list[tuple[int, ...]] = [()]
    for _ in range(m):
        out = [x + (c,) for x in out for c in range(q)]
    return tuple(sorted(out))


# --------------------------------------------------------------------------
# candidate properties (also used as surface encodings and as regime tags)
# --------------------------------------------------------------------------


def property_value(pid: str, x: tuple[int, ...], q: int):
    """Exact evaluation of one registered property on one configuration."""
    m = len(x)
    if pid == "SORTED_COLOR_HISTOGRAM":
        return tuple(sorted(x.count(c) for c in range(q)))
    if pid == "COLOR_HISTOGRAM":
        return tuple(x.count(c) for c in range(q))
    if pid == "N_DISTINCT_COLORS":
        return len(set(x))
    if pid == "IS_CONSTANT":
        return int(len(set(x)) == 1)
    if pid == "ADJACENT_EQUAL_COUNT":
        return sum(1 for i in range(m) if x[i] == x[(i + 1) % m])
    if pid == "MAJORITY_COLOR":
        counts = [x.count(c) for c in range(q)]
        top = max(counts)
        winners = [c for c in range(q) if counts[c] == top]
        return winners[0] if len(winners) == 1 else -1
    head, _, arg = pid.rpartition("_")
    if head == "COLOR_AT_SITE":
        return x[int(arg)]
    if head == "COUNT_OF_COLOR":
        return x.count(int(arg))
    if head == "PARITY_OF_COLOR":
        return x.count(int(arg)) % 2
    if pid.startswith("SITE_PAIR_EQUAL_"):
        i, j = (int(t) for t in pid[len("SITE_PAIR_EQUAL_") :].split("_"))
        return int(x[i] == x[j])
    raise ValueError(f"unknown property: {pid}")


def _vkey(value) -> str:
    return repr(value)


# --------------------------------------------------------------------------
# per-instance indexed field (built once, shared by every algorithm)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Field:
    n: int
    configs: tuple[tuple[int, ...], ...]
    gens: tuple[tuple[int, ...], ...]  # generators as permutations of range(n)
    witnessed: tuple[tuple[int, ...], ...]
    pv: tuple[int, ...]  # interned property values
    ev: tuple[int, ...]  # interned surface-encoding values
    regime: tuple[bool, ...]  # membership of the registered sub-regime
    n_property_values: int


_FIELD_CACHE: dict[Instance, Field] = {}


def _permutation_of(elt: Elt, configs, index) -> tuple[int, ...]:
    return tuple(index[act(elt, x)] for x in configs)


def field(inst: Instance) -> Field:
    cached = _FIELD_CACHE.get(inst)
    if cached is not None:
        return cached
    m, q = inst.n_sites, inst.n_colors
    configs = configurations(m, q)
    index = {x: i for i, x in enumerate(configs)}
    raw_p = [property_value(inst.property_id, x, q) for x in configs]
    raw_e = [property_value(inst.surface_id, x, q) for x in configs]
    pvals = sorted(set(raw_p))
    evals = sorted(set(raw_e))
    pmap = {v: i for i, v in enumerate(pvals)}
    emap = {v: i for i, v in enumerate(evals)}
    allowed = set(inst.regime_values)
    regime = tuple(
        _vkey(property_value(inst.regime_tag_id, x, q)) in allowed for x in configs
    )
    out = Field(
        n=len(configs),
        configs=configs,
        gens=tuple(_permutation_of(g, configs, index) for g in inst.generators),
        witnessed=tuple(_permutation_of(g, configs, index) for g in inst.witnessed),
        pv=tuple(pmap[v] for v in raw_p),
        ev=tuple(emap[v] for v in raw_e),
        regime=regime,
        n_property_values=len(pvals),
    )
    if len(_FIELD_CACHE) > 8192:  # pragma: no cover - bounded cache, not semantics
        _FIELD_CACHE.clear()
    _FIELD_CACHE[inst] = out
    return out


# --------------------------------------------------------------------------
# group closure (algorithm A's route; also used by the parents that need it)
# --------------------------------------------------------------------------


def closure_bfs(gens: Sequence[tuple[int, ...]], n: int, cap: int = MAX_GROUP_ORDER):
    """Materialise the generated group by breadth-first frontier expansion.

    Returns the sorted element list, or None if the group exceeds `cap`.
    """
    ident = tuple(range(n))
    seen = {ident}
    frontier = [ident]
    while frontier:
        nxt: list[tuple[int, ...]] = []
        for g in frontier:
            for h in gens:
                composed = tuple(h[i] for i in g)  # h after g
                if composed not in seen:
                    if len(seen) >= cap:
                        return None
                    seen.add(composed)
                    nxt.append(composed)
        frontier = nxt
    return sorted(seen)


def saturate(gens: Sequence[tuple[int, ...]], n: int, cap: int = MAX_GROUP_ORDER):
    """Cayley saturation: repeatedly close the current set under composition.

    An independent route to the same subgroup, used by `M` so that the mechanic
    does not share the oracle's or the parents' closure code.
    """
    ident = tuple(range(n))
    current = {ident, *[tuple(g) for g in gens]}
    for _ in range(16):
        grown = set(current)
        for a in sorted(current):
            for b in sorted(current):
                grown.add(tuple(a[i] for i in b))
                if len(grown) > cap:
                    return None
        if grown == current:
            return sorted(current)
        current = grown
    return None  # pragma: no cover - 16 squarings exceed the registered cap


# --------------------------------------------------------------------------
# oracle 1 — element closure, pointwise relation R_g
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class OracleAnswer:
    disposition: str
    best_profile: tuple[tuple[str, int], ...]
    n_group_elements: int
    n_breaking_elements: int
    witness: tuple[tuple[str, str], ...] | None

    def as_dict(self) -> dict:
        return {
            "disposition": self.disposition,
            "best_profile": {k: v for k, v in self.best_profile},
            "n_group_elements": self.n_group_elements,
            "n_breaking_elements": self.n_breaking_elements,
            "witness": [list(p) for p in self.witness] if self.witness else None,
        }


def _classify_from_strata(strata: dict[str, int]) -> str:
    """Registered classification order, frozen before any outcome.

    Invariance dominates equivariance; a genuine break is then rescued first by
    the registered regime (an actionable positive: transfer is valid inside it),
    then diagnosed as surface-only (a warning: the break is invisible in the
    re-description), and otherwise reported as an outright non-invariance.
    """
    if strata["invariant_under_G"]:
        return "TRANSFER_VALID"
    if strata["equivariant_under_G"]:
        return "BLOCK_EQUIVARIANT_NOT_INVARIANT"
    if strata["regime_bounded_invariant"]:
        return "BLOCK_REGIME_BOUNDED_INVARIANT"
    if strata["surface_encoding_invariant_under_G"]:
        return "BLOCK_SURFACE_SYMMETRY_ONLY"
    return "BLOCK_NON_INVARIANT"


def _element_class(perm: tuple[int, ...], values: Sequence[int]) -> str:
    """Classify one element by the relation R_g = {(p(x), p(g.x))}."""
    rho: dict[int, int] = {}
    for i, image in enumerate(perm):
        a, b = values[i], values[image]
        if rho.setdefault(a, b) != b:
            return "BREAKING"
    if len(set(rho.values())) != len(rho):
        return "BREAKING"
    return "FIXING" if all(a == b for a, b in rho.items()) else "COVARIANT"


def oracle_element_closure(inst: Instance) -> OracleAnswer:
    F = field(inst)
    group = closure_bfs(F.gens, F.n)
    if group is None:  # pragma: no cover - generator rejects these
        raise ValueError(f"{inst.instance_id}: group exceeds the registered cap")
    witness_group = closure_bfs(F.witnessed, F.n)
    if witness_group is None:  # pragma: no cover
        raise ValueError(f"{inst.instance_id}: witnessed subgroup exceeds the cap")

    classes = [_element_class(g, F.pv) for g in group]
    n_breaking = sum(1 for c in classes if c == "BREAKING")
    n_covariant = sum(1 for c in classes if c == "COVARIANT")

    regime_idx = [i for i in range(F.n) if F.regime[i]]
    proper = 0 < len(regime_idx) < F.n
    stable = all(F.regime[g[i]] == F.regime[i] for g in group for i in range(F.n))
    regime_invariant = proper and stable and all(
        F.pv[g[i]] == F.pv[i] for g in group for i in regime_idx
    )
    surface_invariant = all(F.ev[g[i]] == F.ev[i] for g in group for i in range(F.n))
    witness_invariant = all(
        F.pv[g[i]] == F.pv[i] for g in witness_group for i in range(F.n)
    )

    # orbits of X under the whole materialised group
    seen = [False] * F.n
    n_orbits = 0
    for start in range(F.n):
        if seen[start]:
            continue
        n_orbits += 1
        stack = [start]
        seen[start] = True
        while stack:
            i = stack.pop()
            for g in group:
                j = g[i]
                if not seen[j]:
                    seen[j] = True
                    stack.append(j)

    strata = {
        "invariant_under_G": int(n_breaking == 0 and n_covariant == 0),
        "equivariant_under_G": int(n_breaking == 0),
        "regime_bounded_invariant": int(bool(regime_invariant)),
        "surface_encoding_invariant_under_G": int(bool(surface_invariant)),
        "invariant_under_witnessed_subgroup": int(bool(witness_invariant)),
        "n_orbits": n_orbits,
        "n_property_values": F.n_property_values,
    }
    breaker = next(
        (i for i, c in enumerate(classes) if c == "BREAKING"),
        next((i for i, c in enumerate(classes) if c == "COVARIANT"), None),
    )
    wit = (
        (("element_index", str(breaker)), ("element_class", classes[breaker]))
        if breaker is not None
        else None
    )
    return OracleAnswer(
        _classify_from_strata(strata), tuple(sorted(strata.items())), len(group), n_breaking, wit
    )


# --------------------------------------------------------------------------
# oracle 2 — generators only, block-system criterion
# --------------------------------------------------------------------------


def _blocks_of(values: Sequence[int]) -> tuple[frozenset[int], ...]:
    buckets: dict[int, list[int]] = {}
    for i, v in enumerate(values):
        buckets.setdefault(v, []).append(i)
    return tuple(frozenset(b) for _, b in sorted(buckets.items()))


def _block_class(perm: tuple[int, ...], blocks, index: dict) -> str:
    """Classify one element by what it does to the level-set partition."""
    moved = False
    for block in blocks:
        image = frozenset(perm[i] for i in block)
        if image not in index:
            return "BREAKING"
        if image != block:
            moved = True
    return "COVARIANT" if moved else "FIXING"


def _union_find_orbits(gens, n: int) -> int:
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for g in gens:
        for i in range(n):
            ra, rb = find(i), find(g[i])
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    return len({find(i) for i in range(n)})


def oracle_generator_blocks(inst: Instance) -> OracleAnswer:
    """Independent algorithm: the group is never materialised.

    The stabiliser of `p` and the set of block-preserving elements are both
    subgroups of `G`, so an element set that generates `G` decides both
    questions.  Each generator is decided by set-image tests on the level-set
    partition rather than pointwise on values.  The same argument gives the
    witnessed subgroup and the regime and surface strata.
    """
    F = field(inst)
    blocks = _blocks_of(F.pv)
    bindex = {b: k for k, b in enumerate(blocks)}
    classes = [_block_class(g, blocks, bindex) for g in F.gens]
    breaking = any(c == "BREAKING" for c in classes)
    moving = any(c == "COVARIANT" for c in classes)

    sblocks = _blocks_of(F.ev)
    sindex = {b: k for k, b in enumerate(sblocks)}
    surface_invariant = all(_block_class(g, sblocks, sindex) == "FIXING" for g in F.gens)

    witness_invariant = all(_block_class(g, blocks, bindex) == "FIXING" for g in F.witnessed)

    regime_set = frozenset(i for i in range(F.n) if F.regime[i])
    proper = 0 < len(regime_set) < F.n
    stable = all(frozenset(g[i] for i in regime_set) == regime_set for g in F.gens)
    regime_invariant = proper and stable
    if regime_invariant:
        for g in F.gens:
            for block in blocks:
                inside = block & regime_set
                if inside and frozenset(g[i] for i in inside) - block:
                    regime_invariant = False
                    break
            if not regime_invariant:
                break

    strata = {
        "invariant_under_G": int(not breaking and not moving),
        "equivariant_under_G": int(not breaking),
        "regime_bounded_invariant": int(bool(regime_invariant)),
        "surface_encoding_invariant_under_G": int(bool(surface_invariant)),
        "invariant_under_witnessed_subgroup": int(bool(witness_invariant)),
        "n_orbits": _union_find_orbits(F.gens, F.n),
        "n_property_values": len(blocks),
    }
    return OracleAnswer(
        _classify_from_strata(strata), tuple(sorted(strata.items())), -1, -1, None
    )


def oracle_agrees(inst: Instance) -> tuple[bool, OracleAnswer, OracleAnswer]:
    a = oracle_element_closure(inst)
    b = oracle_generator_blocks(inst)
    return (a.disposition == b.disposition and a.best_profile == b.best_profile), a, b


# --------------------------------------------------------------------------
# generator
# --------------------------------------------------------------------------

ALWAYS_INVARIANT_PROPERTIES = ("SORTED_COLOR_HISTOGRAM", "N_DISTINCT_COLORS", "IS_CONSTANT")


def _rot(m: int) -> tuple[int, ...]:
    return tuple((i + 1) % m for i in range(m))


def _swap(m: int, i: int, j: int) -> tuple[int, ...]:
    p = list(range(m))
    p[i], p[j] = p[j], p[i]
    return tuple(p)


def _reverse(m: int) -> tuple[int, ...]:
    return tuple(m - 1 - i for i in range(m))


def _site_generators(rng: random.Random, m: int) -> list[tuple[int, ...]]:
    kind = rng.choice(("rot", "full", "swap", "reverse"))
    if kind == "rot":
        return [_rot(m)]
    if kind == "full":
        return [_rot(m), _swap(m, 0, 1)]
    if kind == "swap":
        return [_swap(m, 0, 1)]
    return [_reverse(m)]


def _color_generators(rng: random.Random, q: int) -> list[tuple[int, ...]]:
    if q == 2:
        return [(1, 0)]
    return [_swap(q, 0, 1)] if rng.random() < 0.5 else [_rot(q)]


def _site_sensitive_property(rng: random.Random, m: int, q: int) -> str:
    choice = rng.choice(("color_at_site", "adjacent", "pair"))
    if choice == "color_at_site":
        return f"COLOR_AT_SITE_{rng.randrange(m)}"
    if choice == "adjacent":
        return "ADJACENT_EQUAL_COUNT"
    i, j = sorted(rng.sample(range(m), 2))
    return f"SITE_PAIR_EQUAL_{i}_{j}"


def _site_invariant_property(rng: random.Random, m: int, q: int) -> str:
    choice = rng.choice(("histogram", "majority", "count", "parity"))
    if choice == "histogram":
        return "COLOR_HISTOGRAM"
    if choice == "majority":
        return "MAJORITY_COLOR"
    if choice == "count":
        return f"COUNT_OF_COLOR_{rng.randrange(q)}"
    return f"PARITY_OF_COLOR_{rng.randrange(q)}"


def _surface_property(rng: random.Random, m: int, q: int, *, invariant: bool) -> str:
    if invariant:
        return rng.choice(ALWAYS_INVARIANT_PROPERTIES)
    return rng.choice(
        (
            f"COLOR_AT_SITE_{rng.randrange(m)}",
            "COLOR_HISTOGRAM",
            "ADJACENT_EQUAL_COUNT",
            f"COUNT_OF_COLOR_{rng.randrange(q)}",
        )
    )


def _orbit_partition(m: int, q: int, gens: Sequence[Elt]) -> tuple[list[int], int]:
    configs = configurations(m, q)
    index = {x: i for i, x in enumerate(configs)}
    perms = [_permutation_of(g, configs, index) for g in gens]
    parent = list(range(len(configs)))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for p in perms:
        for i in range(len(configs)):
            ra, rb = find(i), find(p[i])
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    labels = [find(i) for i in range(len(configs))]
    return labels, len(set(labels))


def _rescuing_regime_values(
    m: int, q: int, gens: Sequence[Elt], pid: str, tag_id: str
) -> list[str]:
    """Tag classes on which `p` is constant along every orbit.

    The generator uses this to *construct* a candidate sub-regime.  It does not
    label anything: the exhaustive oracle recomputes the regime stratum from the
    published declaration and rejects the instance if the family does not hold.
    """
    configs = configurations(m, q)
    labels, _ = _orbit_partition(m, q, gens)
    pvals = [property_value(pid, x, q) for x in configs]
    tags = [_vkey(property_value(tag_id, x, q)) for x in configs]
    by_orbit: dict[int, set] = {}
    for i, lab in enumerate(labels):
        by_orbit.setdefault(lab, set()).add(pvals[i])
    good: list[str] = []
    for tag in sorted(set(tags)):
        members = [i for i in range(len(configs)) if tags[i] == tag]
        orbits = {labels[i] for i in members}
        if all(len(by_orbit[o]) == 1 for o in orbits):
            good.append(tag)
    return good


def _declare_regime(
    rng: random.Random, m: int, q: int, tag_id: str, *, full: bool
) -> tuple[str, tuple[str, ...]]:
    values = sorted({_vkey(property_value(tag_id, x, q)) for x in configurations(m, q)})
    if full or len(values) < 2:
        return tag_id, tuple(values)
    k = rng.randrange(1, len(values))
    return tag_id, tuple(sorted(rng.sample(values, k)))


def _generate_one(family: str, seed: int) -> tuple[Instance | None, str]:
    """Propose one instance of `family`.  The oracle, not this function, labels it."""
    rng = random.Random(seed)
    m, q = rng.choice(SHAPES)
    site = _site_generators(rng, m)
    color = _color_generators(rng, q)
    ident_s, ident_c = tuple(range(m)), tuple(range(q))
    site_elts = [(s, ident_c) for s in site]
    color_elts = [(ident_s, c) for c in color]
    tag_id = "SORTED_COLOR_HISTOGRAM"

    if family == "FULL_INVARIANCE":
        if rng.random() < 0.5:
            pid = rng.choice(ALWAYS_INVARIANT_PROPERTIES)
            gens = site_elts + color_elts
        else:
            pid = _site_invariant_property(rng, m, q)
            gens = site_elts
        witnessed = [gens[0]]
        eid = _surface_property(rng, m, q, invariant=rng.random() < 0.5)
    elif family == "EQUIVARIANT_ACTION":
        if rng.random() < 0.5:
            pid = rng.choice(("COLOR_HISTOGRAM", "MAJORITY_COLOR"))
            gens = site_elts + color_elts
        else:
            pid = f"COLOR_AT_SITE_{rng.randrange(m)}"
            gens = color_elts
        witnessed = [gens[0]]
        eid = _surface_property(rng, m, q, invariant=rng.random() < 0.5)
    elif family == "NON_INVARIANT":
        pid = _site_sensitive_property(rng, m, q)
        gens = site_elts + (color_elts if rng.random() < 0.5 else [])
        witnessed = [gens[0]]
        eid = _surface_property(rng, m, q, invariant=False)
    elif family == "SURFACE_ONLY_SYMMETRY":
        pid = _site_sensitive_property(rng, m, q)
        gens = site_elts + (color_elts if rng.random() < 0.5 else [])
        witnessed = [gens[0]]
        eid = rng.choice(ALWAYS_INVARIANT_PROPERTIES)
    elif family == "PARTIAL_REGIME_INVARIANCE":
        pid = _site_sensitive_property(rng, m, q)
        gens = site_elts + (color_elts if rng.random() < 0.5 else [])
        witnessed = [gens[0]]
        eid = _surface_property(rng, m, q, invariant=False)
        good = _rescuing_regime_values(m, q, gens, pid, tag_id)
        allv = sorted({_vkey(property_value(tag_id, x, q)) for x in configurations(m, q)})
        good = [v for v in good if v in allv]
        if not good or len(good) == len(allv):
            return None, "no_proper_rescuing_regime"
        k = rng.randrange(1, len(good) + 1)
        return (
            _mk_instance(family, seed, m, q, gens, witnessed, pid, eid, tag_id,
                         tuple(sorted(rng.sample(good, k)))),
            "",
        )
    elif family == "UNSEEN_TRANSFORMATION_BREAK":
        if rng.random() < 0.5:
            if q < 3:
                return None, "shape_incompatible_with_recipe"
            pid = rng.choice((f"COUNT_OF_COLOR_{rng.randrange(q)}",
                              f"PARITY_OF_COLOR_{rng.randrange(q)}"))
            gens = site_elts + color_elts
            witnessed = site_elts
        else:
            if m < 4:
                return None, "shape_incompatible_with_recipe"
            pid = rng.choice(("ADJACENT_EQUAL_COUNT", "SITE_PAIR_EQUAL_0_2"))
            gens = color_elts + [(_swap(m, 0, 1), ident_c)]
            witnessed = color_elts
        eid = _surface_property(rng, m, q, invariant=False)
    elif family == "UNSEEN_TRANSFORMATION_EQUIVARIANCE":
        pid = rng.choice(("COLOR_HISTOGRAM", "MAJORITY_COLOR"))
        gens = site_elts + color_elts
        witnessed = site_elts
        eid = _surface_property(rng, m, q, invariant=rng.random() < 0.5)
    else:  # pragma: no cover
        raise ValueError(family)

    tag_id, regime_values = _declare_regime(rng, m, q, tag_id, full=rng.random() < 0.5)
    return _mk_instance(family, seed, m, q, gens, witnessed, pid, eid, tag_id, regime_values), ""


def _mk_instance(family, seed, m, q, gens, witnessed, pid, eid, tag_id, regime_values):
    return Instance(
        instance_id="",
        family=family,
        seed=seed,
        n_sites=m,
        n_colors=q,
        generators=tuple(sorted(set(tuple(g) for g in gens))),
        witnessed=tuple(sorted(set(tuple(g) for g in witnessed))),
        property_id=pid,
        surface_id=eid,
        regime_tag_id=tag_id,
        regime_values=tuple(regime_values),
    )


EXPECTED_DISPOSITION = {
    "FULL_INVARIANCE": {"TRANSFER_VALID"},
    "EQUIVARIANT_ACTION": {"BLOCK_EQUIVARIANT_NOT_INVARIANT"},
    "NON_INVARIANT": {"BLOCK_NON_INVARIANT"},
    "SURFACE_ONLY_SYMMETRY": {"BLOCK_SURFACE_SYMMETRY_ONLY"},
    "PARTIAL_REGIME_INVARIANCE": {"BLOCK_REGIME_BOUNDED_INVARIANT"},
    "UNSEEN_TRANSFORMATION_BREAK": {"BLOCK_NON_INVARIANT"},
    "UNSEEN_TRANSFORMATION_EQUIVARIANCE": {"BLOCK_EQUIVARIANT_NOT_INVARIANT"},
}

UNSEEN_FAMILIES = ("UNSEEN_TRANSFORMATION_BREAK", "UNSEEN_TRANSFORMATION_EQUIVARIANCE")
SURFACE_MUST_BE_VISIBLE = ("NON_INVARIANT", "UNSEEN_TRANSFORMATION_BREAK")


def generate_split(split: str, seed: str, per_family: dict[str, int]):
    """Generate (instance, oracle) pairs.

    The generator *proposes* a family; the exhaustive oracle *verifies* it.  Any
    instance whose exhaustive disposition is not in its family's registered set,
    on which the two oracle algorithms disagree, or which fails one of the four
    structural preconditions the oracle does not itself express, is rejected and
    resampled.  Rejections are counted per `family|reason` and published; the
    counts sum to the true number of rejections.
    """
    pairs: list[tuple[Instance, OracleAnswer]] = []
    rejects: dict[str, int] = {}

    def drop(family: str, reason: str) -> None:
        rejects[f"{family}|{reason}"] = rejects.get(f"{family}|{reason}", 0) + 1

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
            proposed, reason = _generate_one(family, s)
            if proposed is None:
                drop(family, reason)
                continue
            inst = replace(proposed, instance_id=f"{family}-{counter:05d}")
            F = field(inst)
            if closure_bfs(F.gens, F.n) is None:
                drop(family, "group_exceeds_registered_cap")
                continue
            if closure_bfs(F.witnessed, F.n) is None:  # pragma: no cover
                drop(family, "witness_subgroup_exceeds_registered_cap")
                continue
            group = closure_bfs(F.gens, F.n)
            if len(group) < 2:
                drop(family, "trivial_group")
                continue
            if F.n_property_values < 2:
                drop(family, "degenerate_single_valued_property")
                continue
            if inst.surface_id == inst.property_id:
                drop(family, "surface_encoding_is_not_a_re_description")
                continue
            same, a, _ = oracle_agrees(inst)
            if not same:
                drop(family, "oracle_disagreement")
                continue
            strata = {k: v for k, v in a.best_profile}
            if family in UNSEEN_FAMILIES:
                wgroup = closure_bfs(F.witnessed, F.n)
                if len(wgroup) >= len(group):
                    drop(family, "witnessed_subgroup_not_proper")
                    continue
                if not strata["invariant_under_witnessed_subgroup"]:
                    drop(family, "witnessed_subgroup_does_not_fix_the_property")
                    continue
            if (
                family in SURFACE_MUST_BE_VISIBLE
                and strata["surface_encoding_invariant_under_G"]
            ):
                drop(family, "surface_encoding_invariant_would_collapse_the_family")
                continue
            if a.disposition not in EXPECTED_DISPOSITION[family]:
                drop(family, "family_disposition_mismatch")
                continue
            made += 1
            pairs.append((inst, a))
    return pairs, rejects


# --------------------------------------------------------------------------
# parents (each with native known-answer tests; see `parent_fidelity`)
# --------------------------------------------------------------------------


def parent_surface_symmetry_scan(inst: Instance) -> dict:
    """P0 — feature-level symmetry scan, the "the re-description looks symmetric"
    baseline.

    It tests the registered surface encoding for invariance under the generators
    and reports the property's disposition from that alone.  This is a real
    practice (symmetry screening on summary features), not a strawman: it is
    exact about the *encoding* and says nothing about the property.  The
    `SURFACE_ONLY_SYMMETRY` family exists to expose exactly that gap.
    """
    F = field(inst)
    invariant = all(F.ev[g[i]] == F.ev[i] for g in F.gens for i in range(F.n))
    return {
        "disposition": "TRANSFER_VALID" if invariant else "BLOCK_NON_INVARIANT",
        "witness": (("surface_encoding", inst.surface_id),),
    }


def parent_orbit_stabiliser(inst: Instance) -> dict:
    """P1 — orbit/stabiliser computation, the mature owner of invariance.

    Computes the orbit partition of the domain under the group action and
    reports invariance iff the property is constant on every orbit.  This is how
    computational group theory decides the question and it is exact for it.
    Registered boundary: it has no notion of an action on the value space, so it
    cannot distinguish equivariance from a break, and it never consults the
    regime declaration or the surface encoding.
    """
    F = field(inst)
    parent = list(range(F.n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for g in F.gens:
        for i in range(F.n):
            ra, rb = find(i), find(g[i])
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    by_orbit: dict[int, set[int]] = {}
    for i in range(F.n):
        by_orbit.setdefault(find(i), set()).add(F.pv[i])
    constant = all(len(v) == 1 for v in by_orbit.values())
    return {
        "disposition": "TRANSFER_VALID" if constant else "BLOCK_NON_INVARIANT",
        "witness": (("n_orbits", str(len(by_orbit))),),
    }


def parent_equivariance_solver(inst: Instance) -> dict:
    """P2 — equivariance solver over the materialised group.

    Owns the invariance/equivariance stratum: it materialises the group and, for
    each element, constructs the induced relation on property values, accepting
    it as a value-space action iff it is a well-defined injection.  Registered
    boundary: it knows nothing about sub-regimes or surface encodings, so on a
    genuine break it can only say `BLOCK_NON_INVARIANT`.
    """
    F = field(inst)
    group = closure_bfs(F.gens, F.n)
    if group is None:  # pragma: no cover - outside the registered envelope
        return {"disposition": "BLOCK_NON_INVARIANT", "witness": None}
    classes = [_element_class(g, F.pv) for g in group]
    if any(c == "BREAKING" for c in classes):
        disp = "BLOCK_NON_INVARIANT"
    elif any(c == "COVARIANT" for c in classes):
        disp = "BLOCK_EQUIVARIANT_NOT_INVARIANT"
    else:
        disp = "TRANSFER_VALID"
    return {"disposition": disp, "witness": (("group_order", str(len(group))),)}


def parent_augmentation_empirical(inst: Instance) -> dict:
    """P3 — empirical symmetry detection from witnessed transformations.

    The standard applied practice: measure the property under the augmentations
    you actually have and conclude invariance if none of them changes it.  It is
    exact about the witnessed subgroup.  Registered boundary: it is structurally
    blind to every transformation outside it, which is what the two
    `UNSEEN_TRANSFORMATION_*` families measure.
    """
    F = field(inst)
    invariant = all(F.pv[g[i]] == F.pv[i] for g in F.witnessed for i in range(F.n))
    return {
        "disposition": "TRANSFER_VALID" if invariant else "BLOCK_NON_INVARIANT",
        "witness": (("n_witnessed_generators", str(len(F.witnessed))),),
    }


def parent_regime_restriction(inst: Instance) -> dict:
    """P4 — regime-restriction parent.

    Owns the sub-regime stratum: it checks the registered declaration for
    properness and G-stability and reports a regime-bounded invariance when the
    property is invariant there but not globally.  Registered boundary: it has no
    value-space action and no surface encoding, so it reports every remaining
    break as `BLOCK_NON_INVARIANT`.
    """
    F = field(inst)
    if all(F.pv[g[i]] == F.pv[i] for g in F.gens for i in range(F.n)):
        return {"disposition": "TRANSFER_VALID", "witness": None}
    inside = [i for i in range(F.n) if F.regime[i]]
    proper = 0 < len(inside) < F.n
    stable = all(F.regime[g[i]] == F.regime[i] for g in F.gens for i in range(F.n))
    if proper and stable and all(F.pv[g[i]] == F.pv[i] for g in F.gens for i in inside):
        return {
            "disposition": "BLOCK_REGIME_BOUNDED_INVARIANT",
            "witness": (("regime_size", str(len(inside))),),
        }
    return {"disposition": "BLOCK_NON_INVARIANT", "witness": None}


FIXED_LESSONS = {
    "SORTED_COLOR_HISTOGRAM": "TRANSFER_VALID",
    "N_DISTINCT_COLORS": "TRANSFER_VALID",
    "IS_CONSTANT": "TRANSFER_VALID",
    "COLOR_HISTOGRAM": "BLOCK_EQUIVARIANT_NOT_INVARIANT",
    "MAJORITY_COLOR": "BLOCK_EQUIVARIANT_NOT_INVARIANT",
    "ADJACENT_EQUAL_COUNT": "BLOCK_NON_INVARIANT",
    "COLOR_AT_SITE": "BLOCK_NON_INVARIANT",
    "COUNT_OF_COLOR": "BLOCK_NON_INVARIANT",
    "PARITY_OF_COLOR": "BLOCK_NON_INVARIANT",
    "SITE_PAIR_EQUAL": "BLOCK_NON_INVARIANT",
}


def parent_fixed_lesson_table(inst: Instance) -> dict:
    """P5 — frozen lesson table, the protocol's fixed-lesson baseline.

    A table from property name to disposition, frozen before the run and applied
    without looking at the group at all.  Real heuristics, no computation.
    Registered boundary: the same property is invariant under one group and not
    under another, and a name-keyed table cannot see that.
    """
    pid = inst.property_id
    disp = FIXED_LESSONS.get(pid)
    if disp is None:
        for prefix, value in sorted(FIXED_LESSONS.items()):
            if pid.startswith(prefix + "_"):
                disp = value
                break
    return {"disposition": disp or "BLOCK_NON_INVARIANT", "witness": (("lesson_key", pid),)}


# --------------------------------------------------------------------------
# federation, mechanic and ablations
# --------------------------------------------------------------------------


def federation(inst: Instance) -> dict:
    """F0 — strongest faithful parent federation, under a pre-registered rule.

    Registered before any outcome and blind to it: the invariance/equivariance
    stratum is decided by the equivariance solver (P2); only when P2 reports an
    outright break is the regime parent (P4) consulted, and only when P4 declines
    is the surface scan (P0) consulted, whose invariant verdict on a broken
    property is exactly the surface-only diagnosis.  No parent is used outside
    its native competence and none ever sees the oracle.
    """
    p2 = parent_equivariance_solver(inst)
    if p2["disposition"] in ("TRANSFER_VALID", "BLOCK_EQUIVARIANT_NOT_INVARIANT"):
        return {"disposition": p2["disposition"], "witness": p2["witness"], "source": "P2"}
    p4 = parent_regime_restriction(inst)
    if p4["disposition"] == "BLOCK_REGIME_BOUNDED_INVARIANT":
        return {"disposition": p4["disposition"], "witness": p4["witness"], "source": "P4"}
    p0 = parent_surface_symmetry_scan(inst)
    if p0["disposition"] == "TRANSFER_VALID":
        return {
            "disposition": "BLOCK_SURFACE_SYMMETRY_ONLY",
            "witness": p0["witness"],
            "source": "P0",
        }
    return {"disposition": "BLOCK_NON_INVARIANT", "witness": None, "source": "P2"}


def _discover_value_action(
    perm: tuple[int, ...],
    values: Sequence[int],
    n_values: int,
    schedule,
    seed: int,
) -> dict[int, int] | None:
    """M's anytime value-action discovery: sample, construct, verify exhaustively.

    A candidate `rho` is *built* from a bounded sample of the domain and then
    *verified* on every configuration through the reference module's
    `assess_invariance`.  A candidate that fails verification is discarded and
    the next, larger sample is tried.  If the schedule runs out the element is
    reported as breaking, so the procedure is sound but **not complete**: with a
    shortened schedule it returns `None` for elements that do have a value
    action, which is what makes `M` capable of diverging from the federation.
    """
    n = len(values)
    rng = random.Random(seed)
    all_values = list(range(n_values))
    cases = tuple(TransformationCase(f"c{i}", i, perm[i], "g") for i in range(n))
    for mode, size in schedule:
        k = min(size, n)
        if mode == "stratified":
            first: dict[int, int] = {}
            for i in range(n):
                first.setdefault(values[i], i)
            sample = sorted(first.values())
            for i in range(n):
                if len(sample) >= k:
                    break
                if i not in first.values():
                    sample.append(i)
            sample = sorted(set(sample))
        else:
            sample = sorted(rng.sample(range(n), k))
        rho: dict[int, int] = {}
        consistent = True
        for i in sample:
            a, b = values[i], values[perm[i]]
            if rho.setdefault(a, b) != b:
                consistent = False
                break
        if not consistent or len(set(rho.values())) != len(rho):
            continue
        missing = [v for v in all_values if v not in rho]
        free = [v for v in all_values if v not in set(rho.values())]
        if len(missing) != len(free):
            continue
        if not missing:
            candidates = [dict(rho)]
        elif len(missing) <= 2:
            candidates = [
                {**rho, **dict(zip(missing, order))} for order in permutations(free)
            ]
        else:
            continue
        for cand in candidates:
            assessment = assess_invariance(
                cases,
                lambda i: values[i],
                lambda _tid, v: cand.get(v, -1),
            )
            if not assessment.violated_case_ids:
                return cand
    return None


def mechanic_full(
    inst: Instance,
    *,
    use_equivariance: bool = True,
    use_regime: bool = True,
    use_surface: bool = True,
    scope: str = "GROUP",
    schedule=SAMPLE_SCHEDULE,
) -> dict:
    """M — F2 invariance/equivariance discovery, full (issue #50 L2 pipeline).

    structural description -> transformation closure -> invariance test ->
    value-action discovery -> native regime recovery -> surface audit ->
    disposition.

    **This is an independent implementation, and deliberately so.**  FM10's
    blocking defect was an `M` that issued the same calls as its own comparator,
    which made `G1a`'s decision identity an algebraic identity rather than a
    measurement.  `M` here calls no parent, no federation and no oracle: it
    closes the group by Cayley saturation rather than breadth-first frontier
    expansion, tests invariance by set-image fixation of the level-set partition
    rather than pointwise on values, discovers the value action by bounded
    sampling with exhaustive verification through
    `orion_v2.transfer_formal_mechanics.assess_invariance` rather than by direct
    construction, and *discovers* the maximal orbit-union on which the property
    is constant before comparing the registered declaration against it.
    """
    F = field(inst)
    gens = F.gens if scope == "GROUP" else F.witnessed
    group = saturate(gens, F.n)
    if group is None:  # pragma: no cover - outside the registered envelope
        return {"disposition": "BLOCK_NON_INVARIANT", "witness": None}

    level_sets = _blocks_of(F.pv)
    level_index = {b: k for k, b in enumerate(level_sets)}
    fixes = [all(frozenset(g[i] for i in b) == b for b in level_sets) for g in group]
    if all(fixes):
        return {"disposition": "TRANSFER_VALID", "witness": (("group_order", str(len(group))),)}

    if use_equivariance:
        actions = []
        for pos, g in enumerate(group):
            if fixes[pos]:
                continue
            rho = _discover_value_action(
                g, F.pv, F.n_property_values, schedule, inst.seed ^ (pos * 2654435761)
            )
            if rho is None:
                actions = None
                break
            actions.append(rho)
        if actions is not None:
            return {
                "disposition": "BLOCK_EQUIVARIANT_NOT_INVARIANT",
                "witness": (("value_actions_discovered", str(len(actions))),),
            }

    if use_regime:
        # native recovery: discover the maximal union of orbits on which the
        # property is constant, then check the registered declaration against it
        seen = [-1] * F.n
        orbit_id = 0
        for start in range(F.n):
            if seen[start] >= 0:
                continue
            stack, members = [start], []
            seen[start] = orbit_id
            while stack:
                i = stack.pop()
                members.append(i)
                for g in group:
                    j = g[i]
                    if seen[j] < 0:
                        seen[j] = orbit_id
                        stack.append(j)
            orbit_id += 1
        constant_orbits = {
            o for o in range(orbit_id)
            if len({F.pv[i] for i in range(F.n) if seen[i] == o}) == 1
        }
        recovered = frozenset(i for i in range(F.n) if seen[i] in constant_orbits)
        declared = frozenset(i for i in range(F.n) if F.regime[i])
        stable = all(frozenset(g[i] for i in declared) == declared for g in group)
        if declared and declared != frozenset(range(F.n)) and stable and declared <= recovered:
            return {
                "disposition": "BLOCK_REGIME_BOUNDED_INVARIANT",
                "witness": (("recovered_regime_size", str(len(recovered))),
                            ("declared_regime_size", str(len(declared)))),
            }

    if use_surface:
        surface_sets = _blocks_of(F.ev)
        if all(
            all(frozenset(g[i] for i in b) == b for b in surface_sets) for g in group
        ):
            return {
                "disposition": "BLOCK_SURFACE_SYMMETRY_ONLY",
                "witness": (("surface_encoding", inst.surface_id),),
            }

    return {
        "disposition": "BLOCK_NON_INVARIANT",
        "witness": (("n_level_sets", str(len(level_index))),),
    }


def ablation_minus_equivariance_test(inst: Instance) -> dict:
    """M without value-action discovery: every non-fixing element is a break."""
    return mechanic_full(inst, use_equivariance=False)


def ablation_minus_unseen_transformation_closure(inst: Instance) -> dict:
    """M restricted to the witnessed subgroup: no generalization to unseen elements."""
    return mechanic_full(inst, scope="WITNESSED")


def ablation_minus_regime_restriction(inst: Instance) -> dict:
    """M without native regime recovery."""
    return mechanic_full(inst, use_regime=False)


def ablation_minus_surface_audit(inst: Instance) -> dict:
    """M without the surface audit: a surface-invisible break is reported flatly."""
    return mechanic_full(inst, use_surface=False)


def control_always_invariant(inst: Instance) -> dict:
    return {"disposition": "TRANSFER_VALID", "witness": None}


def control_always_non_invariant(inst: Instance) -> dict:
    return {"disposition": "BLOCK_NON_INVARIANT", "witness": None}


def control_random(inst: Instance) -> dict:
    return {"disposition": random.Random(inst.seed ^ 0x5EED).choice(DISPOSITIONS),
            "witness": None}


ARM_FUNCTIONS: dict[str, Callable[[Instance], dict]] = {
    "P0_SURFACE_SYMMETRY_SCAN": parent_surface_symmetry_scan,
    "P1_ORBIT_STABILISER": parent_orbit_stabiliser,
    "P2_EQUIVARIANCE_SOLVER": parent_equivariance_solver,
    "P3_AUGMENTATION_EMPIRICAL": parent_augmentation_empirical,
    "P4_REGIME_RESTRICTION": parent_regime_restriction,
    "P5_FIXED_LESSON_TABLE": parent_fixed_lesson_table,
    "F0_PARENT_FEDERATION": federation,
    "M_F2_INVARIANCE_DISCOVERY_FULL": mechanic_full,
    "M_MINUS_EQUIVARIANCE_TEST": ablation_minus_equivariance_test,
    "M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE": ablation_minus_unseen_transformation_closure,
    "M_MINUS_REGIME_RESTRICTION": ablation_minus_regime_restriction,
    "M_MINUS_SURFACE_AUDIT": ablation_minus_surface_audit,
    "C_ALWAYS_INVARIANT": control_always_invariant,
    "C_ALWAYS_NON_INVARIANT": control_always_non_invariant,
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
# hand-built instances used by the fidelity tests and the fixtures
# --------------------------------------------------------------------------


def _all_tag_values(m: int, q: int, tag: str) -> tuple[str, ...]:
    return tuple(sorted({_vkey(property_value(tag, x, q)) for x in configurations(m, q)}))


def _inst(
    name: str,
    family: str,
    m: int,
    q: int,
    gens: Sequence[Elt],
    witnessed: Sequence[Elt],
    pid: str,
    eid: str,
    regime_values: Sequence[str] | None = None,
    tag: str = "SORTED_COLOR_HISTOGRAM",
    seed: int = 0,
) -> Instance:
    return Instance(
        instance_id=name,
        family=family,
        seed=seed,
        n_sites=m,
        n_colors=q,
        generators=tuple(gens),
        witnessed=tuple(witnessed),
        property_id=pid,
        surface_id=eid,
        regime_tag_id=tag,
        regime_values=tuple(regime_values) if regime_values is not None
        else _all_tag_values(m, q, tag),
    )


def _rot_site(m: int, q: int) -> Elt:
    return (_rot(m), tuple(range(q)))


def _swap_site(m: int, q: int, i: int, j: int) -> Elt:
    return (_swap(m, i, j), tuple(range(q)))


def _swap_color(m: int, q: int, a: int, b: int) -> Elt:
    return (tuple(range(m)), _swap(q, a, b))


# --------------------------------------------------------------------------
# parent fidelity: native known-answer tests (must pass before use)
# --------------------------------------------------------------------------


def parent_fidelity() -> list[dict]:
    T: list[dict] = []

    def check(parent: str, name: str, ok: bool, detail: str = "") -> None:
        T.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    # ---- the group action itself -----------------------------------------
    m, q = 3, 2
    configs = configurations(m, q)
    g1, g2 = _rot_site(m, q), _swap_color(m, q, 0, 1)
    check(
        "GROUP_ACTION",
        "composition_is_a_left_action",
        all(act(compose(g1, g2), x) == act(g1, act(g2, x)) for x in configs)
        and all(act(compose(g2, g1), x) == act(g2, act(g1, x)) for x in configs),
    )
    index = {x: i for i, x in enumerate(configs)}
    s3 = [_rot_site(m, q), _swap_site(m, q, 0, 1)]
    perms = [_permutation_of(g, configs, index) for g in s3 + [g2]]
    grp = closure_bfs(perms, len(configs))
    check(
        "GROUP_ACTION",
        "site_S3_times_colour_swap_closes_to_order_12",
        grp is not None and len(grp) == 12,
        str(len(grp) if grp else None),
    )
    check(
        "GROUP_ACTION",
        "every_closure_element_is_a_permutation_of_the_domain",
        all(sorted(g) == list(range(len(configs))) for g in (grp or [])),
    )
    check(
        "GROUP_ACTION",
        "cayley_saturation_and_breadth_first_closure_agree",
        saturate(perms, len(configs)) == grp,
    )
    pv = [property_value("SORTED_COLOR_HISTOGRAM", x, q) for x in configs]
    gen_ok = all(pv[g[i]] == pv[i] for g in perms for i in range(len(configs)))
    grp_ok = all(pv[g[i]] == pv[i] for g in (grp or []) for i in range(len(configs)))
    check(
        "GROUP_ACTION",
        "invariance_under_generators_implies_invariance_under_the_group",
        gen_ok and grp_ok,
        "the subgroup theorem oracle 2 rests on",
    )

    # ---- reusable hand instances -----------------------------------------
    inv = _inst("FID-INV", "FULL_INVARIANCE", 3, 2, [g1, g2], [g1],
                "SORTED_COLOR_HISTOGRAM", "COLOR_AT_SITE_0")
    equi = _inst("FID-EQUI", "EQUIVARIANT_ACTION", 3, 2, [g1, g2], [g1],
                 "COLOR_HISTOGRAM", "COLOR_AT_SITE_0")
    broke = _inst("FID-BREAK", "NON_INVARIANT", 3, 2, [g1], [g1],
                  "COLOR_AT_SITE_0", "COLOR_AT_SITE_1")
    surf = _inst("FID-SURF", "SURFACE_ONLY_SYMMETRY", 3, 2, [g1], [g1],
                 "COLOR_AT_SITE_0", "SORTED_COLOR_HISTOGRAM")
    const_only = (_vkey((0, 3)),)
    regime = _inst("FID-REGIME", "PARTIAL_REGIME_INVARIANCE", 3, 2, [g1], [g1],
                   "COLOR_AT_SITE_0", "COLOR_AT_SITE_1", const_only)
    unseen = _inst("FID-UNSEEN", "UNSEEN_TRANSFORMATION_BREAK", 3, 3,
                   [_rot_site(3, 3), _swap_color(3, 3, 0, 1)], [_rot_site(3, 3)],
                   "COUNT_OF_COLOR_0", "COLOR_AT_SITE_0")
    site_only = _inst("FID-SITEONLY", "FULL_INVARIANCE", 3, 2,
                      [_rot_site(3, 2), _swap_site(3, 2, 0, 1)], [_rot_site(3, 2)],
                      "COLOR_HISTOGRAM", "COLOR_AT_SITE_0")

    # ---- P1 orbit/stabiliser --------------------------------------------
    check(
        "P1_ORBIT_STABILISER",
        "cyclic_rotation_on_three_binary_sites_has_four_orbits",
        dict(parent_orbit_stabiliser(broke)["witness"])["n_orbits"] == "4",
    )
    check(
        "P1_ORBIT_STABILISER",
        "sorted_histogram_is_constant_on_every_orbit",
        parent_orbit_stabiliser(inv)["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P1_ORBIT_STABILISER",
        "a_site_indexed_property_is_not_constant_on_orbits",
        parent_orbit_stabiliser(broke)["disposition"] == "BLOCK_NON_INVARIANT",
    )
    check(
        "P1_ORBIT_STABILISER",
        "documented_boundary_cannot_see_a_value_space_action",
        parent_orbit_stabiliser(equi)["disposition"] == "BLOCK_NON_INVARIANT",
        "scope note: orbit constancy decides invariance only",
    )

    # ---- P2 equivariance solver -----------------------------------------
    check(
        "P2_EQUIVARIANCE_SOLVER",
        "a_colour_permutation_makes_the_histogram_equivariant",
        parent_equivariance_solver(equi)["disposition"] == "BLOCK_EQUIVARIANT_NOT_INVARIANT",
    )
    check(
        "P2_EQUIVARIANCE_SOLVER",
        "an_invariant_property_is_reported_as_such",
        parent_equivariance_solver(inv)["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P2_EQUIVARIANCE_SOLVER",
        "a_genuine_break_is_reported_as_non_invariant",
        parent_equivariance_solver(unseen)["disposition"] == "BLOCK_NON_INVARIANT",
    )
    check(
        "P2_EQUIVARIANCE_SOLVER",
        "the_solver_reaches_elements_that_are_not_generators",
        dict(parent_equivariance_solver(equi)["witness"])["group_order"] == "6",
        "rotation x colour swap on three binary sites closes to order 6",
    )
    check(
        "P2_EQUIVARIANCE_SOLVER",
        "documented_boundary_blind_to_the_regime_and_surface_strata",
        parent_equivariance_solver(regime)["disposition"] == "BLOCK_NON_INVARIANT"
        and parent_equivariance_solver(surf)["disposition"] == "BLOCK_NON_INVARIANT",
        "scope note: P2 has no sub-regime and no surface encoding",
    )

    # ---- P0 surface scan -------------------------------------------------
    check(
        "P0_SURFACE_SYMMETRY_SCAN",
        "declares_invariance_from_a_symmetric_re_description_while_the_property_breaks",
        parent_surface_symmetry_scan(surf)["disposition"] == "TRANSFER_VALID",
        "the false-invariance behaviour the surface family exists to expose",
    )
    check(
        "P0_SURFACE_SYMMETRY_SCAN",
        "declares_non_invariance_when_the_encoding_itself_moves",
        parent_surface_symmetry_scan(broke)["disposition"] == "BLOCK_NON_INVARIANT",
    )

    # ---- P3 empirical augmentation --------------------------------------
    check(
        "P3_AUGMENTATION_EMPIRICAL",
        "exact_on_the_witnessed_subgroup",
        parent_augmentation_empirical(broke)["disposition"] == "BLOCK_NON_INVARIANT",
    )
    check(
        "P3_AUGMENTATION_EMPIRICAL",
        "documented_boundary_misses_an_unwitnessed_breaking_element",
        parent_augmentation_empirical(unseen)["disposition"] == "TRANSFER_VALID"
        and oracle_element_closure(unseen).disposition == "BLOCK_NON_INVARIANT",
        "scope note: measured symmetry is symmetry under the augmentations you have",
    )

    # ---- P4 regime restriction ------------------------------------------
    check(
        "P4_REGIME_RESTRICTION",
        "finds_the_registered_sub_regime_on_which_the_property_is_invariant",
        parent_regime_restriction(regime)["disposition"] == "BLOCK_REGIME_BOUNDED_INVARIANT",
    )
    check(
        "P4_REGIME_RESTRICTION",
        "declines_when_the_declaration_covers_the_whole_domain",
        parent_regime_restriction(broke)["disposition"] == "BLOCK_NON_INVARIANT",
    )
    check(
        "P4_REGIME_RESTRICTION",
        "documented_boundary_reports_an_equivariant_property_as_broken",
        parent_regime_restriction(equi)["disposition"] == "BLOCK_NON_INVARIANT",
        "scope note: P4 has no value-space action",
    )

    # ---- P5 fixed lesson table ------------------------------------------
    check(
        "P5_FIXED_LESSON_TABLE",
        "reproduces_the_frozen_lesson_for_a_covered_property",
        parent_fixed_lesson_table(equi)["disposition"] == "BLOCK_EQUIVARIANT_NOT_INVARIANT"
        and parent_fixed_lesson_table(inv)["disposition"] == "TRANSFER_VALID",
    )
    check(
        "P5_FIXED_LESSON_TABLE",
        "documented_boundary_the_same_property_under_a_different_group",
        parent_fixed_lesson_table(site_only)["disposition"]
        == "BLOCK_EQUIVARIANT_NOT_INVARIANT"
        and oracle_element_closure(site_only).disposition == "TRANSFER_VALID",
        "scope note: a name-keyed table cannot see which group is acting",
    )

    # ---- oracle cross-theorem and reference module -----------------------
    check(
        "ORACLE_CROSS_THEOREM",
        "block_system_criterion_and_pointwise_relation_agree",
        all(
            oracle_agrees(i)[0]
            for i in (inv, equi, broke, surf, regime, unseen, site_only)
        ),
    )
    F = field(equi)
    grp2 = closure_bfs(F.gens, F.n)
    g = grp2[1]
    cases = tuple(TransformationCase(f"c{i}", i, g[i], "g") for i in range(F.n))
    native = assess_invariance(cases, lambda i: F.pv[i])
    check(
        "REFERENCE_MODULE",
        "assess_invariance_agrees_with_the_suites_own_invariance_primitive",
        (not native.violated_case_ids)
        == all(F.pv[g[i]] == F.pv[i] for i in range(F.n)),
    )
    return T


# --------------------------------------------------------------------------
# hand-authored known-answer fixtures (G0a)
# --------------------------------------------------------------------------


def known_answer_fixtures() -> list[dict]:
    F: list[dict] = []

    def add(name, family, inst, expected):
        F.append({"name": name, "instance": inst, "expected": expected})

    r3 = _rot_site(3, 2)
    c2 = _swap_color(3, 2, 0, 1)
    add("KA-01-INVARIANT_SORTED_HISTOGRAM", "FULL_INVARIANCE",
        _inst("KA-01", "FULL_INVARIANCE", 3, 2, [r3, c2], [r3],
              "SORTED_COLOR_HISTOGRAM", "COLOR_AT_SITE_0"),
        "TRANSFER_VALID")
    add("KA-02-EQUIVARIANT_HISTOGRAM", "EQUIVARIANT_ACTION",
        _inst("KA-02", "EQUIVARIANT_ACTION", 3, 2, [r3, c2], [r3],
              "COLOR_HISTOGRAM", "COLOR_AT_SITE_0"),
        "BLOCK_EQUIVARIANT_NOT_INVARIANT")
    add("KA-03-NON_INVARIANT_SITE_INDEXED", "NON_INVARIANT",
        _inst("KA-03", "NON_INVARIANT", 3, 2, [r3], [r3],
              "COLOR_AT_SITE_0", "COLOR_AT_SITE_1"),
        "BLOCK_NON_INVARIANT")
    add("KA-04-SURFACE_ONLY_SYMMETRY", "SURFACE_ONLY_SYMMETRY",
        _inst("KA-04", "SURFACE_ONLY_SYMMETRY", 3, 2, [r3], [r3],
              "COLOR_AT_SITE_0", "SORTED_COLOR_HISTOGRAM"),
        "BLOCK_SURFACE_SYMMETRY_ONLY")
    constants = (_vkey((0, 3)),)
    add("KA-05-REGIME_BOUNDED_INVARIANT", "PARTIAL_REGIME_INVARIANCE",
        _inst("KA-05", "PARTIAL_REGIME_INVARIANCE", 3, 2, [r3], [r3],
              "COLOR_AT_SITE_0", "COLOR_AT_SITE_1", constants),
        "BLOCK_REGIME_BOUNDED_INVARIANT")
    # the registered classification order: an actionable sub-regime dominates the
    # surface-only diagnosis.  This fixture is what pins it.
    add("KA-06-REGIME_DOMINATES_SURFACE", "PARTIAL_REGIME_INVARIANCE",
        _inst("KA-06", "PARTIAL_REGIME_INVARIANCE", 3, 2, [r3], [r3],
              "COLOR_AT_SITE_0", "SORTED_COLOR_HISTOGRAM", constants),
        "BLOCK_REGIME_BOUNDED_INVARIANT")
    r3q3, c3 = _rot_site(3, 3), _swap_color(3, 3, 0, 1)
    add("KA-07-UNSEEN_TRANSFORMATION_BREAK", "UNSEEN_TRANSFORMATION_BREAK",
        _inst("KA-07", "UNSEEN_TRANSFORMATION_BREAK", 3, 3, [r3q3, c3], [r3q3],
              "COUNT_OF_COLOR_0", "COLOR_AT_SITE_0"),
        "BLOCK_NON_INVARIANT")
    add("KA-08-UNSEEN_TRANSFORMATION_EQUIVARIANCE", "UNSEEN_TRANSFORMATION_EQUIVARIANCE",
        _inst("KA-08", "UNSEEN_TRANSFORMATION_EQUIVARIANCE", 3, 3, [r3q3, c3], [r3q3],
              "COLOR_HISTOGRAM", "COLOR_AT_SITE_0"),
        "BLOCK_EQUIVARIANT_NOT_INVARIANT")
    add("KA-09-INVARIANT_UNDER_A_SITE_ONLY_GROUP", "FULL_INVARIANCE",
        _inst("KA-09", "FULL_INVARIANCE", 3, 2, [r3, _swap_site(3, 2, 0, 1)], [r3],
              "COLOR_HISTOGRAM", "COLOR_AT_SITE_0"),
        "TRANSFER_VALID")
    add("KA-10-MAJORITY_COLOUR_IS_EQUIVARIANT", "EQUIVARIANT_ACTION",
        _inst("KA-10", "EQUIVARIANT_ACTION", 3, 3, [c3], [c3],
              "MAJORITY_COLOR", "COLOR_AT_SITE_0"),
        "BLOCK_EQUIVARIANT_NOT_INVARIANT")
    add("KA-11-ADJACENCY_REGIME_ON_FOUR_SITES", "PARTIAL_REGIME_INVARIANCE",
        _inst("KA-11", "PARTIAL_REGIME_INVARIANCE", 4, 2,
              [_swap_site(4, 2, 0, 1)], [_swap_site(4, 2, 0, 1)],
              "ADJACENT_EQUAL_COUNT", "COLOR_AT_SITE_0", (_vkey((1, 3)),)),
        "BLOCK_REGIME_BOUNDED_INVARIANT")
    return F


# --------------------------------------------------------------------------
# planted positives (trip-wires: every no-alarm assertion must be shown to fire)
# --------------------------------------------------------------------------


def planted_positives() -> list[PlantedPositive]:
    from fm_core import discrimination_gate

    P = [
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "witnessed_only_pseudo_oracle_is_detected",
            "a deliberately incomplete oracle that classifies using only the "
            "witnessed transformations must disagree with the exhaustive closure",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "wrong_expected_label_is_detected",
            "the known-answer comparison must reject a deliberately wrong "
            "expected disposition",
        ),
        PlantedPositive(
            "G2_ANTI_PERMISSIVENESS",
            "false_invariance_claim_is_counted",
            "the over-acceptance counter must count C_ALWAYS_INVARIANT on an "
            "instance whose property the oracle reports as broken",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_ceiling_split_is_detected",
            "a synthetic per-arm table where every arm scores 1.0 must FAIL the "
            "discrimination gate (the FM/FG R2 ceiling defect, which the R2 fm40 "
            "cell exhibited with 1.000 for all five arms)",
        ),
        PlantedPositive(
            "G3_MECHANISM_BY_OMISSION",
            "surface_audit_ablation_loses_the_surface_family",
            "M_MINUS_SURFACE_AUDIT must be wrong on a hand-built surface-only "
            "instance on which M is right",
        ),
        PlantedPositive(
            "G1a_PARENT_REPRODUCES_M",
            "mechanic_can_diverge_from_its_own_comparator",
            "M's own pipeline, run with a shortened value-action sample schedule, "
            "must return a different disposition from the federation: the "
            "decision-identity counter has a subject that can move",
        ),
    ]
    fx = {f["name"]: f for f in known_answer_fixtures()}

    unseen = fx["KA-07-UNSEEN_TRANSFORMATION_BREAK"]["instance"]
    truth = oracle_element_closure(unseen)
    F = field(unseen)
    witnessed_only = _classify_from_strata(
        {
            "invariant_under_G": int(
                all(F.pv[g[i]] == F.pv[i] for g in F.witnessed for i in range(F.n))
            ),
            "equivariant_under_G": 1,
            "regime_bounded_invariant": 0,
            "surface_encoding_invariant_under_G": 0,
        }
    )
    P[0].fired = witnessed_only != truth.disposition

    P[1].fired = (
        oracle_element_closure(fx["KA-01-INVARIANT_SORTED_HISTOGRAM"]["instance"]).disposition
        != "BLOCK_NON_INVARIANT"
    )

    blocked = fx["KA-04-SURFACE_ONLY_SYMMETRY"]["instance"]
    P[2].fired = control_always_invariant(blocked)["disposition"] == "TRANSFER_VALID" and (
        oracle_element_closure(blocked).disposition != "TRANSFER_VALID"
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

    P[4].fired = (
        mechanic_full(blocked)["disposition"] == "BLOCK_SURFACE_SYMMETRY_ONLY"
        and ablation_minus_surface_audit(blocked)["disposition"]
        != "BLOCK_SURFACE_SYMMETRY_ONLY"
    )

    equi = fx["KA-02-EQUIVARIANT_HISTOGRAM"]["instance"]
    P[5].fired = (
        mechanic_full(equi)["disposition"] == federation(equi)["disposition"]
        and mechanic_full(equi, schedule=(("random", 1),))["disposition"]
        != federation(equi)["disposition"]
    )
    return P


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------

SPEC = SuiteSpec(
    suite_id="FM40",
    title="Invariance/equivariance discovery over finite transformation actions",
    families=FAMILIES,
    arms=(
        ArmSpec("P0_SURFACE_SYMMETRY_SCAN", "PARENT", "feature-level symmetry screen"),
        ArmSpec("P1_ORBIT_STABILISER", "PARENT", "orbit/stabiliser computation"),
        ArmSpec("P2_EQUIVARIANCE_SOLVER", "PARENT", "value-space action solver over the group"),
        ArmSpec("P3_AUGMENTATION_EMPIRICAL", "PARENT", "empirical symmetry detection from witnessed transformations"),
        ArmSpec("P4_REGIME_RESTRICTION", "PARENT", "sub-regime restriction parent"),
        ArmSpec("P5_FIXED_LESSON_TABLE", "PARENT", "frozen transfer-lesson table"),
        ArmSpec(
            "F0_PARENT_FEDERATION",
            "FEDERATION",
            "strongest faithful parent federation under a pre-registered outcome-blind rule",
        ),
        ArmSpec("M_F2_INVARIANCE_DISCOVERY_FULL", "MECHANIC", "ORION L2 invariance/equivariance discovery, full"),
        ArmSpec("M_MINUS_EQUIVARIANCE_TEST", "ABLATION", ""),
        ArmSpec("M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE", "ABLATION", ""),
        ArmSpec("M_MINUS_REGIME_RESTRICTION", "ABLATION", ""),
        ArmSpec("M_MINUS_SURFACE_AUDIT", "ABLATION", ""),
        ArmSpec("C_ALWAYS_INVARIANT", "CONTROL", ""),
        ArmSpec("C_ALWAYS_NON_INVARIANT", "CONTROL", ""),
        ArmSpec("C_RANDOM_DISPOSITION", "CONTROL", ""),
    ),
    mechanic_arm="M_F2_INVARIANCE_DISCOVERY_FULL",
    strongest_parent_arm="F0_PARENT_FEDERATION",
    federation_arm="F0_PARENT_FEDERATION",
    weak_arms=(
        "P0_SURFACE_SYMMETRY_SCAN",
        "P3_AUGMENTATION_EMPIRICAL",
        "P5_FIXED_LESSON_TABLE",
        "M_MINUS_EQUIVARIANCE_TEST",
    ),
    constant_arms=("C_ALWAYS_INVARIANT", "C_ALWAYS_NON_INVARIANT"),
    random_arm="C_RANDOM_DISPOSITION",
    ablation_for_family={
        "EQUIVARIANT_ACTION": "M_MINUS_EQUIVARIANCE_TEST",
        "SURFACE_ONLY_SYMMETRY": "M_MINUS_SURFACE_AUDIT",
        "PARTIAL_REGIME_INVARIANCE": "M_MINUS_REGIME_RESTRICTION",
        "UNSEEN_TRANSFORMATION_BREAK": "M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE",
        "UNSEEN_TRANSFORMATION_EQUIVARIANCE": "M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE",
    },
    default_ablation="M_MINUS_EQUIVARIANCE_TEST",
    decoy_families=(
        "SURFACE_ONLY_SYMMETRY",
        "PARTIAL_REGIME_INVARIANCE",
        "UNSEEN_TRANSFORMATION_BREAK",
        "UNSEEN_TRANSFORMATION_EQUIVARIANCE",
    ),
    min_tasks=120,
    dev_per_family=3,
    protected_per_family=18,  # 7 x 18 = 126 >= 120
    design_json="FM40_INVARIANCE_EQUIVARIANCE_DISCOVERY_EXACT_STUDY_DESIGN_V1.json",
    generate=generate_split,
    oracle=oracle_element_closure,
    cross_check=oracle_generator_blocks,
    run_arm=run_arm,
    parent_fidelity=parent_fidelity,
    known_answer_fixtures=known_answer_fixtures,
    planted_positives=planted_positives,
)
