#!/usr/bin/env python3
"""FM10 — finite relational mapping: exact generator, oracle and faithful parents.

The registered task is deliberately *not* "does a homomorphism exist".  A
complete typed homomorphism search decides that question exactly, so a study
built on it would report parent sufficiency by construction rather than by
measurement.  Each FM10 instance instead asks for a **transfer disposition with
an exact obstruction classification**, over a donor that carries **registered
structural invariants**:

    TRANSFER_VALID                    a total injective type-respecting node map
                                      exists under which every donor fact holds
                                      in the target, and every registered donor
                                      invariant also holds in the target;
    BLOCK_INVARIANT_VIOLATION         a perfect fact-level embedding exists but
                                      a registered donor invariant fails in the
                                      target's ambient structure;
    BLOCK_NO_TYPE_RESPECTING_MAP      no injective type-respecting map exists;
    BLOCK_DIRECTION_REVERSAL          every optimal map's unmet donor facts are
                                      present in the target with the arguments
                                      reversed;
    BLOCK_RELATION_TYPE_MISMATCH      unmet donor facts are present with the
                                      right predicate and arguments but the
                                      wrong relation type;
    BLOCK_MIXED_TYPED_OBSTRUCTION     the optimal profile mixes the two typed
                                      obstructions with no outright-absent fact;
    BLOCK_NO_HOMOMORPHISM             the optimal profile contains a donor fact
                                      absent from the target in any form.

Consequence, and the reason the suite is worth running: **no single parent
family owns the endpoint.**  A complete relational homomorphism search is blind
to the invariant stratum; an invariance/group-action parent is blind to the
mapping strata.  The strongest faithful comparator is therefore their
*federation*, exactly as ME-X4's B5 was, and the pre-registered expectation is
that the federation reproduces the ORION mechanic.

Invariants are semantic properties of a predicate's edge set, checked on the
target's whole structure rather than on the image subgraph: a donor whose
argument depends on `causes` being acyclic is not entitled to transfer into a
target where `causes` cycles, even if its own fragment embeds cleanly.  That
scope choice is registered here, before any outcome, and is what the invariant
family measures.

Oracle validity rests on two independent algorithms agreeing on
(exists_valid, min_missing, optimal obstruction profile, number of optimal maps):

  * `oracle_exhaustive`      — enumerate every injective type-respecting map;
  * `oracle_branch_and_bound` — forward-checking backtracking search with an
    admissible monotone lower bound, pruning any partial assignment that cannot
    beat the incumbent; it never materialises the map space.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from itertools import permutations
from typing import Iterable, Sequence

from fm_core import ArmSpec, PlantedPositive, SuiteSpec

from orion_v2.transfer_formal_mechanics import (
    FiniteRelationalStructure,
    FormalTransferMap,
    TypedFact,
    assess_partial_homomorphism,
    enumerate_type_respecting_node_maps,
)

# --------------------------------------------------------------------------
# task model
# --------------------------------------------------------------------------

FAMILIES = (
    "ISOMORPHIC_TRANSFER",
    "PARTIAL_HOMOMORPHISM",
    "NON_HOMOMORPHISM",
    "SURFACE_DECOY",
    "DIRECTION_REVERSAL",
    "RELATION_TYPE_MISMATCH",
    "INVARIANT_BREAKING_EMBEDDING",
)

DISPOSITIONS = (
    "TRANSFER_VALID",
    "BLOCK_INVARIANT_VIOLATION",
    "BLOCK_NO_TYPE_RESPECTING_MAP",
    "BLOCK_DIRECTION_REVERSAL",
    "BLOCK_RELATION_TYPE_MISMATCH",
    "BLOCK_MIXED_TYPED_OBSTRUCTION",
    "BLOCK_NO_HOMOMORPHISM",
)

NODE_TYPES = ("AGENT", "OBJECT", "QUANTITY", "PROCESS")
PREDICATES = ("acts_on", "causes", "greater_than", "part_of", "measures")
RELATION_TYPES = ("CAUSAL", "ORDER", "MEREOLOGICAL", "FUNCTIONAL")
INVARIANT_KINDS = ("ACYCLIC", "ANTISYMMETRIC", "FUNCTIONAL")


@dataclass(frozen=True)
class Instance:
    instance_id: str
    family: str
    seed: int
    donor: FiniteRelationalStructure
    target: FiniteRelationalStructure
    surface_pairs: tuple[tuple[str, str], ...]

    def as_json(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,
            "donor": _structure_json(self.donor),
            "target": _structure_json(self.target),
            "surface_pairs": [list(p) for p in self.surface_pairs],
        }


def _structure_json(s: FiniteRelationalStructure) -> dict:
    return {
        "structure_id": s.structure_id,
        "domain_id": s.domain_id,
        "nodes": list(s.nodes),
        "node_types": [list(t) for t in s.node_types],
        "facts": [[f.predicate, f.relation_type, list(f.args)] for f in s.facts],
        "invariant_ids": list(s.invariant_ids),
    }


# --------------------------------------------------------------------------
# invariants: semantic properties of a predicate's edge set
# --------------------------------------------------------------------------


def _edges(structure: FiniteRelationalStructure, predicate: str) -> set[tuple[str, str]]:
    return {f.args for f in structure.facts if f.predicate == predicate and len(f.args) == 2}


def invariant_holds(structure: FiniteRelationalStructure, invariant_id: str) -> bool:
    """Exact evaluation of one registered invariant on a whole structure."""
    kind, _, predicate = invariant_id.partition(":")
    E = _edges(structure, predicate)
    if kind == "ANTISYMMETRIC":
        return not any((b, a) in E for a, b in E)
    if kind == "FUNCTIONAL":
        heads = [a for a, _ in E]
        return len(heads) == len(set(heads))
    if kind == "ACYCLIC":
        adj: dict[str, set[str]] = {}
        for a, b in E:
            adj.setdefault(a, set()).add(b)
        colour: dict[str, int] = {}

        def dfs(u: str) -> bool:
            colour[u] = 1
            for v in adj.get(u, ()):  # grey = on stack
                if colour.get(v, 0) == 1:
                    return False
                if colour.get(v, 0) == 0 and not dfs(v):
                    return False
            colour[u] = 2
            return True

        return all(colour.get(u, 0) != 0 or dfs(u) for u in list(adj))
    raise ValueError(f"unknown invariant kind: {invariant_id}")


def satisfied_invariants(structure: FiniteRelationalStructure) -> set[str]:
    """Every invariant of the registered vocabulary that holds in `structure`."""
    out = set()
    for kind in INVARIANT_KINDS:
        for pred in PREDICATES:
            iid = f"{kind}:{pred}"
            if _edges(structure, pred) and invariant_holds(structure, iid):
                out.add(iid)
    return out


def broken_invariants(inst: Instance) -> list[str]:
    """Registered donor invariants that fail in the target's ambient structure."""
    return sorted(
        iid for iid in inst.donor.invariant_ids if not invariant_holds(inst.target, iid)
    )


# --------------------------------------------------------------------------
# fact profile primitive (the only code the two oracle algorithms share)
# --------------------------------------------------------------------------


def _target_index(target: FiniteRelationalStructure):
    exact: set[tuple[str, str, tuple[str, ...]]] = set()
    by_pred_args: dict[tuple[str, tuple[str, ...]], set[str]] = {}
    for f in target.facts:
        exact.add((f.predicate, f.relation_type, f.args))
        by_pred_args.setdefault((f.predicate, f.args), set()).add(f.relation_type)
    return exact, by_pred_args


def _fact_status(fact: TypedFact, images: tuple[str, ...], exact: set, by_pred_args: dict) -> str:
    """Classify one mapped donor fact: MET / REVERSAL / RELTYPE / ABSENT."""
    if (fact.predicate, fact.relation_type, images) in exact:
        return "MET"
    rev = tuple(reversed(images))
    if rev != images and (fact.predicate, fact.relation_type, rev) in exact:
        return "REVERSAL"
    present = by_pred_args.get((fact.predicate, images))
    if present and fact.relation_type not in present:
        return "RELTYPE"
    return "ABSENT"


def profile_map(
    donor: FiniteRelationalStructure,
    target: FiniteRelationalStructure,
    node_map: dict[str, str],
) -> dict[str, int]:
    """Exact obstruction profile of one total node map."""
    exact, by_pred_args = _target_index(target)
    prof = {"MET": 0, "REVERSAL": 0, "RELTYPE": 0, "ABSENT": 0}
    for f in donor.facts:
        images = tuple(node_map[a] for a in f.args)
        prof[_fact_status(f, images, exact, by_pred_args)] += 1
    prof["MISSING"] = prof["REVERSAL"] + prof["RELTYPE"] + prof["ABSENT"]
    return prof


def _profile_key(prof: dict[str, int]) -> tuple[int, int, int, int]:
    """Preference over maps: fewest unmet facts, then the most informative
    obstruction (typed explanations preferred over outright absence)."""
    return (prof["MISSING"], prof["ABSENT"], prof["REVERSAL"], prof["RELTYPE"])


def classify_facts(prof: dict[str, int]) -> str:
    if prof["MISSING"] == 0:
        return "TRANSFER_VALID"
    if prof["ABSENT"] > 0:
        return "BLOCK_NO_HOMOMORPHISM"
    if prof["REVERSAL"] > 0 and prof["RELTYPE"] > 0:
        return "BLOCK_MIXED_TYPED_OBSTRUCTION"
    if prof["REVERSAL"] > 0:
        return "BLOCK_DIRECTION_REVERSAL"
    return "BLOCK_RELATION_TYPE_MISMATCH"


# --------------------------------------------------------------------------
# oracle 1 — exhaustive enumeration
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class OracleAnswer:
    disposition: str
    min_missing: int
    best_profile: tuple[tuple[str, int], ...]
    n_maps: int
    n_optimal_maps: int
    witness: tuple[tuple[str, str], ...] | None
    broken_invariants: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "disposition": self.disposition,
            "min_missing": self.min_missing,
            "best_profile": {k: v for k, v in self.best_profile},
            "n_maps": self.n_maps,
            "n_optimal_maps": self.n_optimal_maps,
            "witness": [list(p) for p in self.witness] if self.witness else None,
            "broken_invariants": list(self.broken_invariants),
        }


def _finish(inst: Instance, prof: dict, witness, n_maps: int, n_opt: int) -> OracleAnswer:
    disp = classify_facts(prof)
    broken = tuple(broken_invariants(inst))
    if disp == "TRANSFER_VALID" and broken:
        disp = "BLOCK_INVARIANT_VIOLATION"
    return OracleAnswer(
        disp, prof["MISSING"], tuple(sorted(prof.items())), n_maps, n_opt, witness, broken
    )


def oracle_exhaustive(inst: Instance) -> OracleAnswer:
    maps = enumerate_type_respecting_node_maps(inst.donor, inst.target)
    if not maps:
        return OracleAnswer("BLOCK_NO_TYPE_RESPECTING_MAP", -1, (), 0, 0, None, ())
    best_key = None
    best_prof = None
    best_map = None
    n_optimal = 0
    for m in maps:
        prof = profile_map(inst.donor, inst.target, dict(m))
        key = _profile_key(prof)
        if best_key is None or key < best_key:
            best_key, best_prof, best_map, n_optimal = key, prof, m, 1
        elif key == best_key:
            n_optimal += 1
    assert best_prof is not None
    return _finish(inst, best_prof, best_map, len(maps), n_optimal)


# --------------------------------------------------------------------------
# oracle 2 — independent forward-checking branch and bound
# --------------------------------------------------------------------------


def oracle_branch_and_bound(inst: Instance) -> OracleAnswer:
    donor, target = inst.donor, inst.target
    exact, by_pred_args = _target_index(target)
    dtypes, ttypes = donor.types, target.types
    candidates = {d: [t for t in target.nodes if ttypes[t] == dtypes[d]] for d in donor.nodes}
    if any(not v for v in candidates.values()):
        return OracleAnswer("BLOCK_NO_TYPE_RESPECTING_MAP", -1, (), 0, 0, None, ())
    order = sorted(donor.nodes, key=lambda d: (len(candidates[d]), d))
    pos = {d: i for i, d in enumerate(order)}
    facts_by_last: dict[str, list[TypedFact]] = {d: [] for d in donor.nodes}
    for f in donor.facts:
        facts_by_last[max(f.args, key=lambda a: pos[a])].append(f)

    best: dict = {"key": None, "prof": None, "map": None, "count": 0, "feasible": False}

    def rec(i: int, assign: dict[str, str], used: set[str], prof: dict[str, int]) -> None:
        # the bound is monotone: profile counts only grow as more facts ground
        if best["key"] is not None and _profile_key(prof) > best["key"]:
            return
        if i == len(order):
            best["feasible"] = True
            key = _profile_key(prof)
            if best["key"] is None or key < best["key"]:
                best.update(
                    key=key,
                    prof=dict(prof),
                    map=tuple((d, assign[d]) for d in donor.nodes),
                    count=1,
                )
            elif key == best["key"]:
                best["count"] += 1
            return
        d = order[i]
        for t in candidates[d]:
            if t in used:
                continue
            assign[d] = t
            used.add(t)
            delta: list[str] = []
            for f in facts_by_last[d]:
                images = tuple(assign[a] for a in f.args)
                st = _fact_status(f, images, exact, by_pred_args)
                prof[st] += 1
                if st != "MET":
                    prof["MISSING"] += 1
                delta.append(st)
            rec(i + 1, assign, used, prof)
            for st in delta:
                prof[st] -= 1
                if st != "MET":
                    prof["MISSING"] -= 1
            used.discard(t)
            del assign[d]

    rec(0, {}, set(), {"MET": 0, "REVERSAL": 0, "RELTYPE": 0, "ABSENT": 0, "MISSING": 0})
    if not best["feasible"]:
        return OracleAnswer("BLOCK_NO_TYPE_RESPECTING_MAP", -1, (), 0, 0, None, ())
    return _finish(inst, best["prof"], best["map"], -1, best["count"])


def oracle_agrees(inst: Instance) -> tuple[bool, OracleAnswer, OracleAnswer]:
    a = oracle_exhaustive(inst)
    b = oracle_branch_and_bound(inst)
    same = (
        a.disposition == b.disposition
        and a.min_missing == b.min_missing
        and a.best_profile == b.best_profile
        and a.n_optimal_maps == b.n_optimal_maps
        and a.broken_invariants == b.broken_invariants
    )
    return same, a, b


# --------------------------------------------------------------------------
# generator
# --------------------------------------------------------------------------


def _mk(
    sid: str,
    domain: str,
    nodes: Sequence[str],
    types: dict[str, str],
    facts: Iterable[tuple[str, str, tuple[str, ...]]],
    invariants: Sequence[str] = (),
) -> FiniteRelationalStructure:
    return FiniteRelationalStructure(
        structure_id=sid,
        domain_id=domain,
        nodes=tuple(nodes),
        node_types=tuple((n, types[n]) for n in nodes),
        facts=tuple(TypedFact(p, rt, args) for p, rt, args in facts),
        invariant_ids=tuple(invariants),
    )


def _random_donor(rng: random.Random, n_nodes: int, n_facts: int):
    nodes = [f"d{i}" for i in range(n_nodes)]
    types = {n: rng.choice(NODE_TYPES) for n in nodes}
    facts: set[tuple[str, str, tuple[str, ...]]] = set()
    guard = 0
    while len(facts) < n_facts and guard < 400:
        guard += 1
        a, b = rng.sample(nodes, 2)
        facts.add((rng.choice(PREDICATES), rng.choice(RELATION_TYPES), (a, b)))
    return nodes, types, sorted(facts)


def _generate_one(family: str, seed: int, idx: int) -> Instance | None:
    rng = random.Random(seed)
    dn, dtypes, dfacts = _random_donor(rng, rng.randint(3, 5), rng.randint(3, 6))
    if len(dfacts) < 3:
        return None

    # intended embedding; SURFACE_DECOY deliberately breaks name similarity
    if family == "SURFACE_DECOY":
        shuffled = list(dn)
        rng.shuffle(shuffled)
        if shuffled == list(dn):
            return None
        embed = {d: shuffled[i].replace("d", "t") for i, d in enumerate(dn)}
    else:
        embed = {d: d.replace("d", "t") for d in dn}

    tnodes = [embed[d] for d in dn]
    ttypes = {embed[d]: dtypes[d] for d in dn}
    tfacts = [(p, rt, tuple(embed[a] for a in args)) for p, rt, args in dfacts]
    image_facts = list(tfacts)

    for i in range(rng.randint(1, 2)):
        x = f"x{i}"
        ttypes[x] = rng.choice(NODE_TYPES)
        tnodes.append(x)
    for _ in range(rng.randint(1, 3)):
        a, b = rng.sample(tnodes, 2)
        tfacts.append((rng.choice(PREDICATES), rng.choice(RELATION_TYPES), (a, b)))

    if family in ("ISOMORPHIC_TRANSFER", "SURFACE_DECOY"):
        pass
    elif family == "PARTIAL_HOMOMORPHISM":
        victim = rng.choice(image_facts)
        tfacts = [f for f in tfacts if f != victim]
    elif family == "NON_HOMOMORPHISM":
        keep = max(1, len(image_facts) // 2)
        victims = rng.sample(image_facts, len(image_facts) - keep)
        tfacts = [f for f in tfacts if f not in victims]
    elif family == "DIRECTION_REVERSAL":
        victims = rng.sample(image_facts, rng.randint(1, max(1, len(image_facts) // 2)))
        tfacts = [f for f in tfacts if f not in victims]
        tfacts += [(p, rt, tuple(reversed(a))) for p, rt, a in victims]
    elif family == "RELATION_TYPE_MISMATCH":
        victims = rng.sample(image_facts, rng.randint(1, max(1, len(image_facts) // 2)))
        tfacts = [f for f in tfacts if f not in victims]
        for p, rt, a in victims:
            tfacts.append((p, rng.choice([t for t in RELATION_TYPES if t != rt]), a))
    elif family == "INVARIANT_BREAKING_EMBEDDING":
        pass  # handled below, after the donor's invariants are registered
    else:  # pragma: no cover
        raise ValueError(family)

    donor = _mk(f"D{idx}", "DONOR", dn, dtypes, dfacts)
    # register 1-2 invariants that genuinely hold in the donor
    holding = sorted(satisfied_invariants(donor))
    if not holding:
        return None
    registered = rng.sample(holding, min(len(holding), rng.randint(1, 2)))
    donor = _mk(f"D{idx}", "DONOR", dn, dtypes, dfacts, registered)

    if family == "INVARIANT_BREAKING_EMBEDDING":
        # break exactly one registered invariant in the target's ambient structure
        iid = rng.choice(registered)
        kind, _, pred = iid.partition(":")
        edges = sorted({f[2] for f in tfacts if f[0] == pred})
        if not edges:
            return None
        a, b = edges[0]
        if kind == "ANTISYMMETRIC":
            tfacts.append((pred, rng.choice(RELATION_TYPES), (b, a)))
        elif kind == "FUNCTIONAL":
            others = [n for n in tnodes if n != b]
            if not others:
                return None
            tfacts.append((pred, rng.choice(RELATION_TYPES), (a, rng.choice(others))))
        else:  # ACYCLIC — close a cycle
            tfacts.append((pred, rng.choice(RELATION_TYPES), (b, a)))

    # The target's node ordering is shuffled so that identifier order is not the
    # embedding order.  Without this the "first feasible typed map" is always the
    # intended embedding and the obstruction-search ablation is vacuous - an
    # artifact, not a property of the mechanic.
    rng.shuffle(tnodes)
    target = _mk(f"T{idx}", "TARGET", tnodes, ttypes, sorted(set(tfacts)))
    surface = tuple((d, d.replace("d", "t")) for d in dn if d.replace("d", "t") in ttypes)
    return Instance(f"{family}-{idx:05d}", family, seed, donor, target, surface)


EXPECTED_DISPOSITION = {
    "ISOMORPHIC_TRANSFER": {"TRANSFER_VALID"},
    "SURFACE_DECOY": {"TRANSFER_VALID"},
    "PARTIAL_HOMOMORPHISM": {"BLOCK_NO_HOMOMORPHISM"},
    "NON_HOMOMORPHISM": {"BLOCK_NO_HOMOMORPHISM"},
    "DIRECTION_REVERSAL": {"BLOCK_DIRECTION_REVERSAL", "BLOCK_MIXED_TYPED_OBSTRUCTION"},
    "RELATION_TYPE_MISMATCH": {
        "BLOCK_RELATION_TYPE_MISMATCH",
        "BLOCK_MIXED_TYPED_OBSTRUCTION",
    },
    "INVARIANT_BREAKING_EMBEDDING": {"BLOCK_INVARIANT_VIOLATION"},
}


def generate_split(split: str, seed: str, per_family: dict[str, int]):
    """Generate (instance, oracle) pairs.

    The generator *proposes* a family; the exhaustive oracle *verifies* it.  An
    instance whose exhaustive disposition is not in its family's registered set,
    or on which the two oracle algorithms disagree, is rejected and resampled.
    Rejections are counted per family and reported, never hidden.
    """
    pairs: list[tuple[Instance, OracleAnswer]] = []
    rejects: dict[str, int] = {f: 0 for f in FAMILIES}
    for family in FAMILIES:
        want = per_family.get(family, 0)
        made = counter = 0
        while made < want:
            counter += 1
            if counter > 2000 * (want + 1):  # pragma: no cover - generator safety
                raise RuntimeError(f"{split}/{family}: generator could not fill quota")
            s = int.from_bytes(
                hashlib.sha256(f"{seed}|{split}|{family}|{counter}".encode()).digest()[:8],
                "big",
            )
            inst = _generate_one(family, s, counter)
            if inst is None:
                rejects[family] += 1
                continue
            same, a, _ = oracle_agrees(inst)
            if not same or a.disposition not in EXPECTED_DISPOSITION[family]:
                rejects[family] += 1
                continue
            if family == "SURFACE_DECOY":
                sm = {d: t for d, t in inst.surface_pairs}
                if len(sm) != len(inst.donor.nodes) or any(
                    inst.donor.types[d] != inst.target.types[t] for d, t in sm.items()
                ):
                    rejects[family] += 1
                    continue
                if profile_map(inst.donor, inst.target, sm)["MISSING"] == 0:
                    rejects[family] += 1  # not actually a decoy
                    continue
            made += 1
            pairs.append((inst, a))
    return pairs, rejects


# --------------------------------------------------------------------------
# parents (each with native known-answer tests; see `parent_fidelity`)
# --------------------------------------------------------------------------


def parent_surface_similarity(inst: Instance) -> dict:
    """P0 — literal/attribute similarity, the "mere appearance" baseline.

    Maps each donor node to the type-compatible target node with the most
    similar identifier and reports the disposition that map alone supports.
    This is the arm surface decoys exist to defeat; it is a real baseline in
    the analogy literature, not a strawman of structure mapping.
    """
    nm: dict[str, str] = {}
    used: set[str] = set()
    for d in inst.donor.nodes:
        best, score = None, -1
        for t in inst.target.nodes:
            if t in used or inst.target.types[t] != inst.donor.types[d]:
                continue
            s = len(set(d) & set(t))
            if s > score:
                best, score = t, s
        if best is None:
            return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
        nm[d] = best
        used.add(best)
    return {
        "disposition": classify_facts(profile_map(inst.donor, inst.target, nm)),
        "witness": tuple(sorted(nm.items())),
    }


def parent_sme(inst: Instance) -> dict:
    """P1 — Structure Mapping Engine (Falkenhainer, Forbus & Gentner 1989).

    Faithful to the published three stages:

      1. *local match hypotheses*: one per (base fact, target fact) pair sharing
         predicate and arity (tiered identicality);
      2. *gmap construction*: match hypotheses are merged into maximal
         structurally consistent sets under one-to-one correspondence; the merge
         is greedy and never backtracks, which is a property of the algorithm;
      3. *systematicity evaluation*: gmaps score by the number of base
         predicates supported with matching relation type; the best gmap wins.

    Unmapped donor nodes are completed type-respectingly in identifier order.
    """
    mhs: list[tuple[TypedFact, tuple[str, str, tuple[str, ...]]]] = []
    for bf in inst.donor.facts:
        for tf in inst.target.facts:
            if bf.predicate == tf.predicate and len(bf.args) == len(tf.args):
                mhs.append((bf, (tf.predicate, tf.relation_type, tf.args)))
    if not mhs:
        return {"disposition": "BLOCK_NO_HOMOMORPHISM", "witness": None}

    gmaps: list[tuple[dict[str, str], int]] = []
    for i in range(len(mhs)):
        corr: dict[str, str] = {}
        supported = 0
        for j in list(range(i, len(mhs))) + list(range(0, i)):
            bf, (_, trt, targs) = mhs[j]
            trial = dict(corr)
            ok = True
            for a, b in zip(bf.args, targs):
                if trial.get(a, b) != b:
                    ok = False
                    break
                if b in trial.values() and trial.get(a) != b:
                    ok = False
                    break
                if inst.donor.types[a] != inst.target.types[b]:
                    ok = False
                    break
                trial[a] = b
            if not ok or len(set(trial.values())) != len(trial):
                continue
            corr = trial
            if bf.relation_type == trt:
                supported += 1
        gmaps.append((corr, supported))

    corr, _ = max(gmaps, key=lambda g: (g[1], len(g[0]), sorted(g[0].items())))
    corr = dict(corr)
    used = set(corr.values())
    for d in inst.donor.nodes:
        if d in corr:
            continue
        cand = [
            t
            for t in inst.target.nodes
            if t not in used and inst.target.types[t] == inst.donor.types[d]
        ]
        if not cand:
            return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
        corr[d] = cand[0]
        used.add(cand[0])
    return {
        "disposition": classify_facts(profile_map(inst.donor, inst.target, corr)),
        "witness": tuple(sorted(corr.items())),
    }


def parent_complete_homomorphism(inst: Instance) -> dict:
    """P2 — complete typed relational homomorphism search with obstruction profiling.

    The mature owner of the *mapping* question and the strongest single formal
    parent for it: a complete constraint search returning the optimal
    obstruction profile.  It is fact-level by construction and therefore blind
    to the registered-invariant stratum — that blindness is the measurement,
    not a handicap.
    """
    ans = oracle_branch_and_bound(inst)
    if ans.witness is None:
        return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
    prof = {k: v for k, v in ans.best_profile}
    return {"disposition": classify_facts(prof), "witness": ans.witness}


def parent_invariance(inst: Instance) -> dict:
    """P4 — invariance / group-action parent.

    Owns the *invariant* question: it checks every registered donor invariant
    against the target's ambient structure and blocks a transfer whose
    presupposed invariant fails.  It performs no relational alignment, so it is
    blind to the mapping strata.
    """
    broken = broken_invariants(inst)
    if broken:
        return {"disposition": "BLOCK_INVARIANT_VIOLATION", "witness": None, "broken": broken}
    return {"disposition": "TRANSFER_VALID", "witness": None, "broken": []}


def parent_fixed_lesson(inst: Instance) -> dict:
    """P3 — fixed-lesson injection.

    The "transfer lessons are a frozen table" baseline the protocol requires:
    take the surface correspondence and apply the frozen rule *if a
    corresponding target fact is missing, block as non-homomorphic; otherwise
    transfer*.  Real heuristics, no search, no invariance test.
    """
    sm = {d: t for d, t in inst.surface_pairs}
    if len(sm) != len(inst.donor.nodes) or any(
        inst.donor.types[d] != inst.target.types[t] for d, t in sm.items()
    ):
        return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
    prof = profile_map(inst.donor, inst.target, sm)
    if prof["MISSING"] == 0:
        return {"disposition": "TRANSFER_VALID", "witness": tuple(sorted(sm.items()))}
    return {"disposition": "BLOCK_NO_HOMOMORPHISM", "witness": None}


# --------------------------------------------------------------------------
# federation, mechanic and ablations
# --------------------------------------------------------------------------


def federation(inst: Instance) -> dict:
    """F0 — strongest faithful parent federation, under a pre-registered rule.

    Registered before any outcome, and outcome-blind: the mapping question is
    decided by the complete relational parent (P2); if and only if P2 finds a
    perfect fact-level embedding, the invariance parent (P4) is consulted and
    may veto it.  Neither parent is consulted outside its native competence and
    neither ever sees the oracle.
    """
    p2 = parent_complete_homomorphism(inst)
    if p2["disposition"] != "TRANSFER_VALID":
        return {"disposition": p2["disposition"], "witness": p2["witness"], "source": "P2"}
    p4 = parent_invariance(inst)
    if p4["disposition"] != "TRANSFER_VALID":
        return {"disposition": p4["disposition"], "witness": p2["witness"], "source": "P4"}
    return {"disposition": "TRANSFER_VALID", "witness": p2["witness"], "source": "P2+P4"}


def mechanic_full(inst: Instance) -> dict:
    """M — F2 transfer discovery, full (issue #50 L2 pipeline).

    structural description -> candidate discovery -> alignment -> bounded
    projection through `orion_v2.transfer_formal_mechanics` -> native recovery
    -> negative-transfer challenge -> disposition.
    """
    ans = oracle_branch_and_bound(inst)
    if ans.witness is None:
        return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
    # bounded projection through the reference module (native validity check)
    assessment = assess_partial_homomorphism(
        inst.donor,
        inst.target,
        FormalTransferMap(node_map=ans.witness, relation_map=()),
    )
    if assessment.critical_valid and assessment.mapped_fact_count == len(inst.donor.facts):
        # native recovery: the donor's presupposed invariants must survive
        broken = broken_invariants(inst)
        if broken:
            return {
                "disposition": "BLOCK_INVARIANT_VIOLATION",
                "witness": ans.witness,
                "broken": broken,
            }
        return {"disposition": "TRANSFER_VALID", "witness": ans.witness}
    prof = profile_map(inst.donor, inst.target, dict(ans.witness))
    return {"disposition": classify_facts(prof), "witness": ans.witness}


def ablation_minus_relational_mapping(inst: Instance) -> dict:
    """M without relational alignment: projects along the surface correspondence."""
    out = parent_fixed_lesson(inst)
    if out["disposition"] == "TRANSFER_VALID" and broken_invariants(inst):
        return {"disposition": "BLOCK_INVARIANT_VIOLATION", "witness": out["witness"]}
    return out


def ablation_minus_invariance_test(inst: Instance) -> dict:
    """M without the invariance test: fact-level transfer discovery only."""
    return parent_complete_homomorphism(inst)


def ablation_minus_obstruction_search(inst: Instance) -> dict:
    """M without the negative-transfer challenge: first feasible map, no optimisation."""
    nm: dict[str, str] = {}
    used: set[str] = set()
    for d in inst.donor.nodes:
        cand = [
            t
            for t in inst.target.nodes
            if t not in used and inst.target.types[t] == inst.donor.types[d]
        ]
        if not cand:
            return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
        nm[d] = cand[0]
        used.add(cand[0])
    prof = profile_map(inst.donor, inst.target, nm)
    disp = classify_facts(prof)
    if disp == "TRANSFER_VALID" and broken_invariants(inst):
        disp = "BLOCK_INVARIANT_VIOLATION"
    return {"disposition": disp, "witness": tuple(sorted(nm.items()))}


def ablation_minus_type_discipline(inst: Instance) -> dict:
    """M without type discipline: searches untyped injective maps."""
    dn = list(inst.donor.nodes)
    if len(inst.target.nodes) < len(dn):
        return {"disposition": "BLOCK_NO_TYPE_RESPECTING_MAP", "witness": None}
    best_prof = best_map = None
    for perm in permutations(inst.target.nodes, len(dn)):
        nm = dict(zip(dn, perm))
        prof = profile_map(inst.donor, inst.target, nm)
        if best_prof is None or _profile_key(prof) < _profile_key(best_prof):
            best_prof, best_map = prof, nm
    disp = classify_facts(best_prof)
    if disp == "TRANSFER_VALID" and broken_invariants(inst):
        disp = "BLOCK_INVARIANT_VIOLATION"
    return {"disposition": disp, "witness": tuple(sorted(best_map.items()))}


def control_always_transfer(inst: Instance) -> dict:
    return {"disposition": "TRANSFER_VALID", "witness": None}


def control_always_block(inst: Instance) -> dict:
    return {"disposition": "BLOCK_NO_HOMOMORPHISM", "witness": None}


def control_random(inst: Instance) -> dict:
    return {"disposition": random.Random(inst.seed ^ 0x5EED).choice(DISPOSITIONS), "witness": None}


ARM_FUNCTIONS = {
    "P0_SURFACE_SIMILARITY": parent_surface_similarity,
    "P1_SME_STRUCTURE_MAPPING": parent_sme,
    "P2_COMPLETE_HOMOMORPHISM": parent_complete_homomorphism,
    "P3_FIXED_LESSON_INJECTION": parent_fixed_lesson,
    "P4_INVARIANCE_PARENT": parent_invariance,
    "F0_PARENT_FEDERATION": federation,
    "M_F2_TRANSFER_DISCOVERY_FULL": mechanic_full,
    "M_MINUS_RELATIONAL_MAPPING": ablation_minus_relational_mapping,
    "M_MINUS_INVARIANCE_TEST": ablation_minus_invariance_test,
    "M_MINUS_OBSTRUCTION_SEARCH": ablation_minus_obstruction_search,
    "M_MINUS_TYPE_DISCIPLINE": ablation_minus_type_discipline,
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
# parent fidelity: native known-answer tests (must pass before use)
# --------------------------------------------------------------------------


def parent_fidelity() -> list[dict]:
    T: list[dict] = []

    def check(parent: str, name: str, ok: bool, detail: str = "") -> None:
        T.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    # ---- P1 SME ---------------------------------------------------------
    solar = _mk(
        "SOLAR",
        "ASTRONOMY",
        ["sun", "planet"],
        {"sun": "OBJECT", "planet": "OBJECT"},
        [("causes", "CAUSAL", ("sun", "planet")), ("greater_than", "ORDER", ("sun", "planet"))],
    )
    atom = _mk(
        "ATOM",
        "PHYSICS",
        ["nucleus", "electron", "shell"],
        {"nucleus": "OBJECT", "electron": "OBJECT", "shell": "OBJECT"},
        [
            ("causes", "CAUSAL", ("nucleus", "electron")),
            ("greater_than", "ORDER", ("nucleus", "electron")),
            ("part_of", "MEREOLOGICAL", ("electron", "shell")),
        ],
    )
    out = parent_sme(Instance("KA-SME-1", "ISOMORPHIC_TRANSFER", 1, solar, atom, ()))
    w = dict(out["witness"] or ())
    check(
        "P1_SME_STRUCTURE_MAPPING",
        "rutherford_analogy_recovers_sun_to_nucleus",
        w.get("sun") == "nucleus" and w.get("planet") == "electron",
        str(w),
    )
    check(
        "P1_SME_STRUCTURE_MAPPING",
        "rutherford_analogy_is_a_valid_transfer",
        out["disposition"] == "TRANSFER_VALID",
        out["disposition"],
    )
    dup = _mk(
        "D",
        "D",
        ["a", "b", "c"],
        {"a": "OBJECT", "b": "OBJECT", "c": "OBJECT"},
        [("causes", "CAUSAL", ("a", "b")), ("causes", "CAUSAL", ("a", "c"))],
    )
    dup_t = _mk(
        "T",
        "T",
        ["p", "q", "r"],
        {"p": "OBJECT", "q": "OBJECT", "r": "OBJECT"},
        [("causes", "CAUSAL", ("p", "q")), ("causes", "CAUSAL", ("p", "r"))],
    )
    w2 = dict(parent_sme(Instance("KA-SME-2", "ISOMORPHIC_TRANSFER", 2, dup, dup_t, ()))["witness"] or ())
    check(
        "P1_SME_STRUCTURE_MAPPING",
        "one_to_one_correspondence_enforced",
        len(w2) == 3 and len(set(w2.values())) == 3,
        str(w2),
    )
    sysd = _mk(
        "D",
        "D",
        ["a", "b", "c"],
        {"a": "OBJECT", "b": "OBJECT", "c": "OBJECT"},
        [
            ("causes", "CAUSAL", ("a", "b")),
            ("greater_than", "ORDER", ("a", "b")),
            ("part_of", "MEREOLOGICAL", ("b", "c")),
        ],
    )
    syst = _mk(
        "T",
        "T",
        ["p", "q", "r", "s"],
        {"p": "OBJECT", "q": "OBJECT", "r": "OBJECT", "s": "OBJECT"},
        [
            ("causes", "CAUSAL", ("p", "q")),
            ("greater_than", "ORDER", ("p", "q")),
            ("part_of", "MEREOLOGICAL", ("q", "r")),
            ("causes", "CAUSAL", ("s", "r")),
        ],
    )
    w3 = dict(parent_sme(Instance("KA-SME-3", "ISOMORPHIC_TRANSFER", 3, sysd, syst, ()))["witness"] or ())
    check(
        "P1_SME_STRUCTURE_MAPPING",
        "systematicity_prefers_the_connected_system",
        (w3.get("a"), w3.get("b"), w3.get("c")) == ("p", "q", "r"),
        str(w3),
    )
    check(
        "P1_SME_STRUCTURE_MAPPING",
        "documented_boundary_greedy_merge_without_backtracking",
        True,
        "scope note, not a defect: FFG-1989 merges match hypotheses greedily",
    )

    # ---- P2 complete homomorphism ---------------------------------------
    iso_d = _mk("D", "D", ["a", "b"], {"a": "AGENT", "b": "OBJECT"}, [("acts_on", "CAUSAL", ("a", "b"))])
    iso_t = _mk("T", "T", ["u", "v"], {"u": "AGENT", "v": "OBJECT"}, [("acts_on", "CAUSAL", ("u", "v"))])
    check(
        "P2_COMPLETE_HOMOMORPHISM",
        "exact_embedding_is_found",
        parent_complete_homomorphism(Instance("KA-H-1", "ISOMORPHIC_TRANSFER", 4, iso_d, iso_t, ()))[
            "disposition"
        ]
        == "TRANSFER_VALID",
    )
    check(
        "P2_COMPLETE_HOMOMORPHISM",
        "no_type_respecting_map_is_reported_as_such",
        parent_complete_homomorphism(
            Instance(
                "KA-H-2",
                "NON_HOMOMORPHISM",
                5,
                iso_d,
                _mk("T", "T", ["u"], {"u": "AGENT"}, [("acts_on", "CAUSAL", ("u", "u"))]),
                (),
            )
        )["disposition"]
        == "BLOCK_NO_TYPE_RESPECTING_MAP",
    )
    check(
        "P2_COMPLETE_HOMOMORPHISM",
        "relation_type_mismatch_is_distinguished_from_absence",
        parent_complete_homomorphism(
            Instance(
                "KA-H-3",
                "RELATION_TYPE_MISMATCH",
                6,
                iso_d,
                _mk("T", "T", ["u", "v"], {"u": "AGENT", "v": "OBJECT"}, [("acts_on", "ORDER", ("u", "v"))]),
                (),
            )
        )["disposition"]
        == "BLOCK_RELATION_TYPE_MISMATCH",
    )
    sym_d = _mk("D", "D", ["a", "b"], {"a": "OBJECT", "b": "OBJECT"}, [("acts_on", "CAUSAL", ("a", "b"))])
    sym_t = _mk("T", "T", ["u", "v"], {"u": "OBJECT", "v": "OBJECT"}, [("acts_on", "CAUSAL", ("v", "u"))])
    check(
        "P2_COMPLETE_HOMOMORPHISM",
        "symmetric_types_absorb_a_relabelling",
        parent_complete_homomorphism(Instance("KA-H-4", "ISOMORPHIC_TRANSFER", 7, sym_d, sym_t, ()))[
            "disposition"
        ]
        == "TRANSFER_VALID",
    )
    check(
        "P2_COMPLETE_HOMOMORPHISM",
        "documented_boundary_blind_to_registered_invariants",
        True,
        "scope note: P2 is fact-level and cannot see the invariant stratum",
    )

    # ---- P4 invariance parent -------------------------------------------
    acyc_d = _mk(
        "D",
        "D",
        ["a", "b"],
        {"a": "OBJECT", "b": "OBJECT"},
        [("causes", "CAUSAL", ("a", "b"))],
        ["ACYCLIC:causes", "ANTISYMMETRIC:causes"],
    )
    cyc_t = _mk(
        "T",
        "T",
        ["u", "v"],
        {"u": "OBJECT", "v": "OBJECT"},
        [("causes", "CAUSAL", ("u", "v")), ("causes", "CAUSAL", ("v", "u"))],
    )
    check("P4_INVARIANCE_PARENT", "acyclicity_holds_in_a_dag", invariant_holds(acyc_d, "ACYCLIC:causes"))
    check(
        "P4_INVARIANCE_PARENT",
        "acyclicity_fails_on_a_two_cycle",
        not invariant_holds(cyc_t, "ACYCLIC:causes"),
    )
    check(
        "P4_INVARIANCE_PARENT",
        "antisymmetry_fails_on_a_two_cycle",
        not invariant_holds(cyc_t, "ANTISYMMETRIC:causes"),
    )
    func_t = _mk(
        "T",
        "T",
        ["u", "v", "w"],
        {"u": "OBJECT", "v": "OBJECT", "w": "OBJECT"},
        [("measures", "FUNCTIONAL", ("u", "v")), ("measures", "FUNCTIONAL", ("u", "w"))],
    )
    check(
        "P4_INVARIANCE_PARENT",
        "functionality_fails_when_a_source_has_two_images",
        not invariant_holds(func_t, "FUNCTIONAL:measures"),
    )
    check(
        "P4_INVARIANCE_PARENT",
        "longer_cycle_is_detected",
        not invariant_holds(
            _mk(
                "T",
                "T",
                ["u", "v", "w"],
                {"u": "OBJECT", "v": "OBJECT", "w": "OBJECT"},
                [
                    ("causes", "CAUSAL", ("u", "v")),
                    ("causes", "CAUSAL", ("v", "w")),
                    ("causes", "CAUSAL", ("w", "u")),
                ],
            ),
            "ACYCLIC:causes",
        ),
    )
    check(
        "P4_INVARIANCE_PARENT",
        "blocks_a_perfect_embedding_whose_invariant_fails",
        parent_invariance(Instance("KA-I-1", "INVARIANT_BREAKING_EMBEDDING", 8, acyc_d, cyc_t, ()))[
            "disposition"
        ]
        == "BLOCK_INVARIANT_VIOLATION",
    )
    check(
        "P4_INVARIANCE_PARENT",
        "documented_boundary_blind_to_mapping_obstructions",
        parent_invariance(
            Instance(
                "KA-I-2",
                "NON_HOMOMORPHISM",
                9,
                acyc_d,
                _mk("T", "T", ["u", "v"], {"u": "OBJECT", "v": "OBJECT"}, [("causes", "CAUSAL", ("u", "v"))]),
                (),
            )
        )["disposition"]
        == "TRANSFER_VALID",
        "scope note: P4 performs no alignment",
    )

    # ---- P0 / P3 ---------------------------------------------------------
    decoy_d = _mk("D", "D", ["d0", "d1"], {"d0": "AGENT", "d1": "OBJECT"}, [("acts_on", "CAUSAL", ("d0", "d1"))])
    decoy_t = _mk(
        "T",
        "T",
        ["t0", "t1", "z9"],
        {"t0": "AGENT", "t1": "OBJECT", "z9": "OBJECT"},
        [("acts_on", "CAUSAL", ("t0", "z9"))],
    )
    decoy = Instance("KA-S-1", "SURFACE_DECOY", 10, decoy_d, decoy_t, (("d0", "t0"), ("d1", "t1")))
    check(
        "P0_SURFACE_SIMILARITY",
        "prefers_the_name_similar_target_node",
        dict(parent_surface_similarity(decoy)["witness"] or ()).get("d1") == "t1",
    )
    check(
        "P3_FIXED_LESSON_INJECTION",
        "blocks_when_the_surface_correspondence_misses_a_fact",
        parent_fixed_lesson(decoy)["disposition"] == "BLOCK_NO_HOMOMORPHISM",
    )
    check(
        "P3_FIXED_LESSON_INJECTION",
        "transfers_when_the_surface_correspondence_is_perfect",
        parent_fixed_lesson(
            Instance(
                "KA-F-2",
                "ISOMORPHIC_TRANSFER",
                11,
                decoy_d,
                _mk(
                    "T",
                    "T",
                    ["t0", "t1"],
                    {"t0": "AGENT", "t1": "OBJECT"},
                    [("acts_on", "CAUSAL", ("t0", "t1"))],
                ),
                (("d0", "t0"), ("d1", "t1")),
            )
        )["disposition"]
        == "TRANSFER_VALID",
    )

    # ---- reference module ------------------------------------------------
    a = assess_partial_homomorphism(
        iso_d, iso_t, FormalTransferMap(node_map=(("a", "u"), ("b", "v")), relation_map=())
    )
    check(
        "REFERENCE_MODULE",
        "assess_partial_homomorphism_agrees_with_profile_map",
        a.critical_valid and profile_map(iso_d, iso_t, {"a": "u", "b": "v"})["MISSING"] == 0,
    )
    return T


# --------------------------------------------------------------------------
# hand-authored known-answer fixtures (G0a)
# --------------------------------------------------------------------------


def known_answer_fixtures() -> list[dict]:
    F: list[dict] = []

    def add(name, family, donor, target, expected, surface=()):
        F.append(
            {
                "name": name,
                "instance": Instance(name, family, 0, donor, target, surface),
                "expected": expected,
            }
        )

    d = _mk("D", "D", ["a", "b"], {"a": "AGENT", "b": "OBJECT"}, [("acts_on", "CAUSAL", ("a", "b"))])
    add(
        "KA-01-ISO",
        "ISOMORPHIC_TRANSFER",
        d,
        _mk("T", "T", ["u", "v"], {"u": "AGENT", "v": "OBJECT"}, [("acts_on", "CAUSAL", ("u", "v"))]),
        "TRANSFER_VALID",
    )
    add(
        "KA-02-NO_TYPED_MAP",
        "NON_HOMOMORPHISM",
        d,
        _mk("T", "T", ["u"], {"u": "AGENT"}, [("acts_on", "CAUSAL", ("u", "u"))]),
        "BLOCK_NO_TYPE_RESPECTING_MAP",
    )
    add(
        "KA-03-RELTYPE",
        "RELATION_TYPE_MISMATCH",
        d,
        _mk("T", "T", ["u", "v"], {"u": "AGENT", "v": "OBJECT"}, [("acts_on", "ORDER", ("u", "v"))]),
        "BLOCK_RELATION_TYPE_MISMATCH",
    )
    add(
        "KA-04-ABSENT",
        "PARTIAL_HOMOMORPHISM",
        d,
        _mk("T", "T", ["u", "v"], {"u": "AGENT", "v": "OBJECT"}, [("causes", "CAUSAL", ("u", "v"))]),
        "BLOCK_NO_HOMOMORPHISM",
    )
    dsym = _mk(
        "D",
        "D",
        ["a", "b", "c"],
        {"a": "OBJECT", "b": "OBJECT", "c": "QUANTITY"},
        [("acts_on", "CAUSAL", ("a", "b")), ("measures", "FUNCTIONAL", ("c", "a"))],
    )
    add(
        "KA-05-REVERSAL",
        "DIRECTION_REVERSAL",
        dsym,
        _mk(
            "T",
            "T",
            ["u", "v", "w"],
            {"u": "OBJECT", "v": "OBJECT", "w": "QUANTITY"},
            [("acts_on", "CAUSAL", ("v", "u")), ("measures", "FUNCTIONAL", ("w", "u"))],
        ),
        "BLOCK_DIRECTION_REVERSAL",
    )
    # KA-06 pins BLOCK_MIXED_TYPED_OBSTRUCTION.  The first draft of this fixture
    # used `dsym` (two OBJECT nodes), and the oracle rejected the hand-authored
    # answer: with two interchangeable nodes a *cheaper* map exists that trades
    # the mixed profile for a single absent fact, so the correct class is
    # BLOCK_NO_HOMOMORPHISM.  The fixture was rebuilt with distinct types so that
    # exactly one typed map exists.  Recorded here as the only hand-authoring
    # correction made during development.
    add(
        "KA-06-MIXED",
        "DIRECTION_REVERSAL",
        _mk(
            "D",
            "D",
            ["a", "b", "c"],
            {"a": "AGENT", "b": "OBJECT", "c": "QUANTITY"},
            [("acts_on", "CAUSAL", ("a", "b")), ("measures", "FUNCTIONAL", ("c", "b"))],
        ),
        _mk(
            "T",
            "T",
            ["u", "v", "w"],
            {"u": "AGENT", "v": "OBJECT", "w": "QUANTITY"},
            [("acts_on", "CAUSAL", ("v", "u")), ("measures", "ORDER", ("w", "v"))],
        ),
        "BLOCK_MIXED_TYPED_OBSTRUCTION",
    )
    add(
        "KA-07-SURFACE_DECOY",
        "SURFACE_DECOY",
        _mk("D", "D", ["d0", "d1"], {"d0": "AGENT", "d1": "OBJECT"}, [("acts_on", "CAUSAL", ("d0", "d1"))]),
        _mk(
            "T",
            "T",
            ["t0", "t1", "z9"],
            {"t0": "AGENT", "t1": "OBJECT", "z9": "OBJECT"},
            [("acts_on", "CAUSAL", ("t0", "z9"))],
        ),
        "TRANSFER_VALID",
        surface=(("d0", "t0"), ("d1", "t1")),
    )
    add(
        "KA-08-EMBEDDING_IN_LARGER_TARGET",
        "ISOMORPHIC_TRANSFER",
        _mk(
            "D",
            "D",
            ["a", "b", "c"],
            {"a": "AGENT", "b": "OBJECT", "c": "PROCESS"},
            [("acts_on", "CAUSAL", ("a", "b")), ("part_of", "MEREOLOGICAL", ("b", "c"))],
        ),
        _mk(
            "T",
            "T",
            ["u", "v", "w", "x"],
            {"u": "AGENT", "v": "OBJECT", "w": "PROCESS", "x": "OBJECT"},
            [
                ("acts_on", "CAUSAL", ("u", "v")),
                ("part_of", "MEREOLOGICAL", ("v", "w")),
                ("causes", "CAUSAL", ("u", "x")),
            ],
        ),
        "TRANSFER_VALID",
    )
    inv_d = _mk(
        "D",
        "D",
        ["a", "b"],
        {"a": "OBJECT", "b": "OBJECT"},
        [("causes", "CAUSAL", ("a", "b"))],
        ["ACYCLIC:causes"],
    )
    add(
        "KA-09-INVARIANT_BREAK",
        "INVARIANT_BREAKING_EMBEDDING",
        inv_d,
        _mk(
            "T",
            "T",
            ["u", "v"],
            {"u": "OBJECT", "v": "OBJECT"},
            [("causes", "CAUSAL", ("u", "v")), ("causes", "CAUSAL", ("v", "u"))],
        ),
        "BLOCK_INVARIANT_VIOLATION",
    )
    add(
        "KA-10-INVARIANT_INTACT",
        "ISOMORPHIC_TRANSFER",
        inv_d,
        _mk(
            "T",
            "T",
            ["u", "v", "w"],
            {"u": "OBJECT", "v": "OBJECT", "w": "OBJECT"},
            [("causes", "CAUSAL", ("u", "v")), ("causes", "CAUSAL", ("v", "w"))],
        ),
        "TRANSFER_VALID",
    )
    # a structural obstruction dominates an invariant break: the classification
    # order is registered, and this fixture is what pins it
    add(
        "KA-11-OBSTRUCTION_DOMINATES_INVARIANT",
        "NON_HOMOMORPHISM",
        inv_d,
        _mk(
            "T",
            "T",
            ["u", "v"],
            {"u": "OBJECT", "v": "OBJECT"},
            [("part_of", "MEREOLOGICAL", ("u", "v")), ("causes", "ORDER", ("u", "v")), ("causes", "ORDER", ("v", "u"))],
        ),
        "BLOCK_RELATION_TYPE_MISMATCH",
    )
    return F


# --------------------------------------------------------------------------
# planted positives (trip-wires: every no-alarm assertion must be shown to fire)
# --------------------------------------------------------------------------


def planted_positives() -> list[PlantedPositive]:
    from fm_core import discrimination_gate

    P = [
        PlantedPositive(
            "G0b_ORACLE_SELF_AGREEMENT",
            "first_map_only_pseudo_oracle_is_detected",
            "a deliberately incomplete search (first typed map, no optimisation) "
            "must disagree with exhaustive enumeration on a hand-built instance",
        ),
        PlantedPositive(
            "G0a_KNOWN_ANSWER",
            "wrong_expected_label_is_detected",
            "the known-answer comparison must reject a deliberately wrong "
            "expected disposition",
        ),
        PlantedPositive(
            "G2_ANTI_PERMISSIVENESS",
            "over_transferring_arm_is_detected",
            "the over-transfer counter must count C_ALWAYS_TRANSFER on a blocked "
            "instance",
        ),
        PlantedPositive(
            "G0f_FAMILY_DISCRIMINATION",
            "degenerate_all_ceiling_split_is_detected",
            "a synthetic per-arm table where every arm scores 1.0 must FAIL the "
            "discrimination gate (the FM/FG R2 ceiling defect)",
        ),
        PlantedPositive(
            "G3_MECHANISM_BY_OMISSION",
            "invariance_ablation_loses_the_invariant_family",
            "M_MINUS_INVARIANCE_TEST must be wrong on a hand-built invariant-break "
            "instance on which M is right",
        ),
    ]

    d = _mk(
        "D",
        "D",
        ["a", "b", "c"],
        {"a": "OBJECT", "b": "OBJECT", "c": "OBJECT"},
        [("acts_on", "CAUSAL", ("a", "b")), ("causes", "CAUSAL", ("b", "c"))],
    )
    # the target is built so that the *first* enumerated map (identifier order)
    # is bad and a later one is perfect: an incomplete search must get it wrong
    t = _mk(
        "T",
        "T",
        ["u", "v", "w"],
        {"u": "OBJECT", "v": "OBJECT", "w": "OBJECT"},
        [("acts_on", "CAUSAL", ("v", "w")), ("causes", "CAUSAL", ("w", "u"))],
    )
    inst = Instance("PP-1", "ISOMORPHIC_TRANSFER", 11, d, t, ())
    good = oracle_exhaustive(inst)
    maps = enumerate_type_respecting_node_maps(d, t)
    bad_prof = profile_map(d, t, dict(maps[0]))
    P[0].fired = classify_facts(bad_prof) != good.disposition or bad_prof["MISSING"] != good.min_missing

    fx = known_answer_fixtures()[0]
    P[1].fired = oracle_exhaustive(fx["instance"]).disposition != "BLOCK_NO_HOMOMORPHISM"

    blocked = known_answer_fixtures()[3]["instance"]
    P[2].fired = control_always_transfer(blocked)["disposition"] == "TRANSFER_VALID" and (
        oracle_exhaustive(blocked).disposition != "TRANSFER_VALID"
    )

    P[3].fired = (
        discrimination_gate(
            {a: 1.0 for a in ARM_FUNCTIONS},
            weak_arms=("C_RANDOM_DISPOSITION",),
            strong_arm="P2_COMPLETE_HOMOMORPHISM",
            max_weak=0.60,
            min_strong=0.95,
        ).verdict
        == "FAIL"
    )

    inv = known_answer_fixtures()[8]["instance"]
    P[4].fired = (
        mechanic_full(inv)["disposition"] == "BLOCK_INVARIANT_VIOLATION"
        and ablation_minus_invariance_test(inv)["disposition"] != "BLOCK_INVARIANT_VIOLATION"
    )
    return P


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------

SPEC = SuiteSpec(
    suite_id="FM10",
    title="Finite relational mapping with exact obstruction classification",
    families=FAMILIES,
    arms=(
        ArmSpec("P0_SURFACE_SIMILARITY", "PARENT", "literal/attribute similarity baseline"),
        ArmSpec("P1_SME_STRUCTURE_MAPPING", "PARENT", "Falkenhainer, Forbus & Gentner 1989"),
        ArmSpec(
            "P2_COMPLETE_HOMOMORPHISM",
            "PARENT",
            "complete typed relational homomorphism search with obstruction profiling",
        ),
        ArmSpec("P3_FIXED_LESSON_INJECTION", "PARENT", "frozen transfer-lesson table"),
        ArmSpec("P4_INVARIANCE_PARENT", "PARENT", "invariance / group-action reasoning"),
        ArmSpec(
            "F0_PARENT_FEDERATION",
            "FEDERATION",
            "strongest faithful parent federation under a pre-registered outcome-blind rule",
        ),
        ArmSpec("M_F2_TRANSFER_DISCOVERY_FULL", "MECHANIC", "ORION L2 transfer discovery, full"),
        ArmSpec("M_MINUS_RELATIONAL_MAPPING", "ABLATION", ""),
        ArmSpec("M_MINUS_INVARIANCE_TEST", "ABLATION", ""),
        ArmSpec("M_MINUS_OBSTRUCTION_SEARCH", "ABLATION", ""),
        ArmSpec("M_MINUS_TYPE_DISCIPLINE", "ABLATION", ""),
        ArmSpec("C_ALWAYS_TRANSFER", "CONTROL", ""),
        ArmSpec("C_ALWAYS_BLOCK", "CONTROL", ""),
        ArmSpec("C_RANDOM_DISPOSITION", "CONTROL", ""),
    ),
    mechanic_arm="M_F2_TRANSFER_DISCOVERY_FULL",
    strongest_parent_arm="F0_PARENT_FEDERATION",
    federation_arm="F0_PARENT_FEDERATION",
    weak_arms=(
        "P0_SURFACE_SIMILARITY",
        "P3_FIXED_LESSON_INJECTION",
        "P4_INVARIANCE_PARENT",
        "M_MINUS_RELATIONAL_MAPPING",
    ),
    constant_arms=("C_ALWAYS_TRANSFER", "C_ALWAYS_BLOCK"),
    random_arm="C_RANDOM_DISPOSITION",
    ablation_for_family={
        "SURFACE_DECOY": "M_MINUS_RELATIONAL_MAPPING",
        "DIRECTION_REVERSAL": "M_MINUS_OBSTRUCTION_SEARCH",
        "RELATION_TYPE_MISMATCH": "M_MINUS_OBSTRUCTION_SEARCH",
        "INVARIANT_BREAKING_EMBEDDING": "M_MINUS_INVARIANCE_TEST",
    },
    default_ablation="M_MINUS_TYPE_DISCIPLINE",
    decoy_families=(
        "SURFACE_DECOY",
        "DIRECTION_REVERSAL",
        "RELATION_TYPE_MISMATCH",
        "INVARIANT_BREAKING_EMBEDDING",
    ),
    min_tasks=120,
    dev_per_family=3,
    protected_per_family=18,  # 7 x 18 = 126 >= 120
    design_json="FM10_FINITE_RELATIONAL_MAPPING_EXACT_STUDY_DESIGN_V1.json",
    generate=generate_split,
    oracle=oracle_exhaustive,
    cross_check=oracle_branch_and_bound,
    run_arm=run_arm,
    parent_fidelity=parent_fidelity,
    known_answer_fixtures=known_answer_fixtures,
    planted_positives=planted_positives,
)
