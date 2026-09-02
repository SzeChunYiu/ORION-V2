"""FG70 generator: balanced `formalism needed or not` instances with hidden
known answers, plus the hand-authored known-answer fixtures for gate G0a.

Every instance is planted for one terminal of the §L5 search order and then
*verified by exhaustion* with `fg_oracle` (both independent methods) before it
is emitted; a planted instance whose cheapest feasible tier is not the intended
one is rejected and resampled.  The label is therefore never an assumption.

Decoy discipline (the point of the suite): each stratum carries structure that
would reward the wrong, more expensive answer, so that an arm which escalates
without exhausting the cheaper tiers is punished on the 5/6 of the split whose
truth is not NEW_PRIMITIVE.
"""

from __future__ import annotations

import hashlib
import random
from typing import Any, Sequence

from fg_model import (
    ADD_ONE_OBSERVATION,
    LOCAL_PATCH,
    NEW_PRIMITIVE,
    NO_CHANGE,
    PARENT_FORMALISM_SUFFICIENT,
    REPRESENTATION_CHANGE,
    Case,
    Formalism,
    Instance,
    Observable,
    Relation,
    atom,
    derived,
)
from fg_oracle import collisions_by_bucket, oracle_agrees

SUITE = "FG70"
STRATA: tuple[str, ...] = (
    NO_CHANGE,
    PARENT_FORMALISM_SUFFICIENT,
    ADD_ONE_OBSERVATION,
    LOCAL_PATCH,
    REPRESENTATION_CHANGE,
    NEW_PRIMITIVE,
)
PATCH_BUDGET = 2
N_CASES = 12
MAX_ATTEMPTS = 4000
DECISIONS = ("d0", "d1", "d2")


# Determinism invariant: no planter may iterate an unordered set. Python
# randomises str hashing per process (PYTHONHASHSEED), so `for k in set(...)`
# would draw different RNG values in different processes and the "same" split
# would not regenerate. Every set that drives an RNG draw is sorted first;
# `tests/unit/test_fg70_exact_study.py` asserts cross-process reproducibility.


def instance_seed(split_seed: str, stratum: str, index: int) -> int:
    digest = hashlib.sha256(f"{split_seed}|{stratum}|{index}".encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


# ---------------------------------------------------------------------------
# base world
# ---------------------------------------------------------------------------


def _observables(rng: random.Random) -> tuple[Observable, ...]:
    out: list[Observable] = []
    for position in range(5):
        size = rng.choice((2, 3))
        out.append(Observable(f"o{position}", tuple(f"v{i}" for i in range(size)), True))
    out.append(Observable("u0", ("v0", "v1", "v2"), False))
    return tuple(out)


def _cases(rng: random.Random, observables: Sequence[Observable]) -> tuple[Case, ...]:
    seen: set[tuple[str, ...]] = set()
    rows: list[tuple[str, ...]] = []
    guard = 0
    while len(rows) < N_CASES and guard < 5000:
        guard += 1
        row = tuple(rng.choice(o.domain) for o in observables)
        if row in seen:
            continue
        seen.add(row)
        rows.append(row)
    if len(rows) < N_CASES:
        raise RuntimeError("could not sample a distinct case set")
    return tuple(
        Case(
            f"x{index:02d}",
            tuple((o.obs_id, value) for o, value in zip(observables, row)),
            "d0",
        )
        for index, row in enumerate(rows)
    )


def _with_decisions(cases: Sequence[Case], decisions: Sequence[str]) -> tuple[Case, ...]:
    return tuple(
        Case(case.case_id, case.values, decision) for case, decision in zip(cases, decisions)
    )


def _skeleton(observables, cases, active, parents, relations) -> Instance:
    return Instance(
        instance_id="probe",
        suite=SUITE,
        stratum="PROBE",
        observables=tuple(observables),
        cases=tuple(cases),
        active_formalism=Formalism("F_ACTIVE", tuple(active)),
        parent_formalisms=tuple(parents),
        relations=tuple(relations),
        patch_budget=PATCH_BUDGET,
    )


def _signature_of(instance: Instance, term_ids: Sequence[str]) -> dict[str, tuple[str, ...]]:
    from fg_model import signatures

    return signatures(term_ids, instance)


def _path_edges(members: Sequence[str]) -> list[tuple[str, str]]:
    ordered = sorted(members)
    return [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]


def _decision_aligned_relation(cases: Sequence[Case], rel_id: str) -> Relation:
    """Components = decision classes: COMP separates every J-distinct pair."""

    groups: dict[str, list[str]] = {}
    for case in cases:
        groups.setdefault(case.decision_id, []).append(case.case_id)
    edges: list[tuple[str, str]] = []
    for members in groups.values():
        edges.extend(_path_edges(members))
    return Relation(rel_id, tuple(sorted(edges)))


def _grouped_relation(assignment: dict[str, int], rel_id: str) -> Relation:
    groups: dict[int, list[str]] = {}
    for case_id, group in assignment.items():
        groups.setdefault(group, []).append(case_id)
    edges: list[tuple[str, str]] = []
    for members in groups.values():
        edges.extend(_path_edges(members))
    return Relation(rel_id, tuple(sorted(edges)))


# ---------------------------------------------------------------------------
# parent library selection (after J is fixed, by exhaustive classification)
# ---------------------------------------------------------------------------


def _candidate_parent_signatures(observables) -> list[tuple[str, ...]]:
    recorded = [o.obs_id for o in observables if o.recorded]
    out: list[tuple[str, ...]] = []
    for i in range(len(recorded)):
        for j in range(i + 1, len(recorded)):
            out.append((atom(recorded[i]), atom(recorded[j])))
            for k in range(j + 1, len(recorded)):
                out.append((atom(recorded[i]), atom(recorded[j]), atom(recorded[k])))
    return out


def _select_parents(
    rng: random.Random,
    probe: Instance,
    active: Sequence[str],
    want_sufficient: bool,
    forbid_sufficient: bool = True,
) -> tuple[Formalism, ...] | None:
    buckets: dict[int, list[tuple[str, ...]]] = {}
    for terms in _candidate_parent_signatures(probe.observables):
        if set(terms) == set(active):
            continue
        size = len(collisions_by_bucket(probe, terms))
        buckets.setdefault(min(size, 3), []).append(terms)
    chosen: list[tuple[str, ...]] = []
    if want_sufficient:
        if not buckets.get(0):
            return None
        chosen.append(rng.choice(buckets[0]))
    elif forbid_sufficient and buckets.get(0):
        # a sufficient parent exists: this instance cannot carry this stratum
        return None
    if buckets.get(1):
        chosen.append(rng.choice(buckets[1]))
    pool = buckets.get(2, []) + buckets.get(3, [])
    rng.shuffle(pool)
    for terms in pool:
        if len(chosen) >= 4:
            break
        if terms not in chosen:
            chosen.append(terms)
    if len(chosen) < 2:
        return None
    return tuple(
        Formalism(f"P{index}", terms) for index, terms in enumerate(sorted(set(chosen)))
    )


# ---------------------------------------------------------------------------
# stratum planters
# ---------------------------------------------------------------------------


def _plant(rng: random.Random, stratum: str) -> Instance | None:
    observables = _observables(rng)
    blank = _cases(rng, observables)
    recorded = [o.obs_id for o in observables if o.recorded]
    rng.shuffle(recorded)
    active = (atom(recorded[0]), atom(recorded[1]))
    probe0 = _skeleton(observables, blank, active, (Formalism("P0", (atom(recorded[2]),)),), ())
    sig_active = _signature_of(probe0, active)

    decisions: list[str] = []
    relations: list[Relation] = []
    decoys: list[str] = []
    want_sufficient_parent = stratum == PARENT_FORMALISM_SUFFICIENT

    if stratum == NO_CHANGE:
        table = {sig: rng.choice(DECISIONS) for sig in sorted(set(sig_active.values()))}
        if len(set(table.values())) < 2:
            return None
        decisions = [table[sig_active[c.case_id]] for c in blank]
        decoys.append("coarser_projection_shows_apparent_collisions")

    elif stratum == PARENT_FORMALISM_SUFFICIENT:
        target = (atom(recorded[2]), atom(recorded[3]))
        sig_target = _signature_of(probe0, target)
        table = {sig: rng.choice(DECISIONS) for sig in sorted(set(sig_target.values()))}
        if len(set(table.values())) < 2:
            return None
        decisions = [table[sig_target[c.case_id]] for c in blank]
        decoys.append("working_new_primitive_available_but_unnecessary")

    elif stratum == ADD_ONE_OBSERVATION:
        extra = atom("u0") if rng.random() < 0.6 else atom(recorded[4])
        sig_extra = _signature_of(probe0, (extra,))
        table: dict[tuple, str] = {}
        for case in blank:
            key = (sig_active[case.case_id], sig_extra[case.case_id])
            table.setdefault(key, rng.choice(DECISIONS))
        decisions = [table[(sig_active[c.case_id], sig_extra[c.case_id])] for c in blank]
        decoys.append("working_new_primitive_available_but_unnecessary")

    elif stratum == LOCAL_PATCH:
        table = {sig: rng.choice(DECISIONS) for sig in sorted(set(sig_active.values()))}
        if len(set(table.values())) < 2:
            return None
        decisions = [table[sig_active[c.case_id]] for c in blank]
        buckets: dict[tuple, list[int]] = {}
        for index, case in enumerate(blank):
            buckets.setdefault(sig_active[case.case_id], []).append(index)
        big = [members for members in buckets.values() if len(members) >= 2]
        if len(big) < PATCH_BUDGET:
            return None
        rng.shuffle(big)
        for members in big[:PATCH_BUDGET]:
            victim = rng.choice(members)
            others = {decisions[i] for i in members if i != victim}
            alternatives = [d for d in DECISIONS if d not in others]
            if not alternatives:
                return None
            decisions[victim] = rng.choice(alternatives)
        decoys.append("working_new_primitive_available_but_unnecessary")

    elif stratum == REPRESENTATION_CHANGE:
        left, right = recorded[2], recorded[3]
        op = rng.choice(("EQ", "DIFF3"))
        term = derived(op, left, right)
        sig_term = _signature_of(probe0, (term,))
        table = {}
        for case in blank:
            key = (sig_active[case.case_id], sig_term[case.case_id])
            table.setdefault(key, rng.choice(DECISIONS))
        decisions = [table[(sig_active[c.case_id], sig_term[c.case_id])] for c in blank]
        decoys.append("working_new_primitive_available_but_unnecessary")

    elif stratum == NEW_PRIMITIVE:
        groups = {case.case_id: rng.randrange(3) for case in blank}
        table = {}
        for case in blank:
            key = (sig_active[case.case_id], groups[case.case_id])
            table.setdefault(key, rng.choice(DECISIONS))
        decisions = [table[(sig_active[c.case_id], groups[c.case_id])] for c in blank]
        relations.append(_grouped_relation(groups, "R_LATENT"))
        decoys.append("near_miss_parent_and_over_budget_patch")
    else:
        raise ValueError(stratum)

    cases = _with_decisions(blank, decisions)
    if len({c.decision_id for c in cases}) < 2:
        return None

    if stratum != NEW_PRIMITIVE:
        relations.append(_decision_aligned_relation(cases, "R_ALIGNED"))

    probe = _skeleton(observables, cases, active, (Formalism("P0", (atom(recorded[2]),)),), relations)
    parents = _select_parents(
        rng, probe, active, want_sufficient_parent, forbid_sufficient=stratum != NO_CHANGE
    )
    if parents is None:
        return None

    return Instance(
        instance_id="pending",
        suite=SUITE,
        stratum=stratum,
        observables=observables,
        cases=cases,
        active_formalism=Formalism("F_ACTIVE", active),
        parent_formalisms=parents,
        relations=tuple(relations),
        patch_budget=PATCH_BUDGET,
        planted_decoys=tuple(sorted(decoys)),
    )


def generate_instance(split: str, split_seed: str, stratum: str, index: int) -> Instance:
    rng = random.Random(instance_seed(split_seed, stratum, index))
    for _ in range(MAX_ATTEMPTS):
        candidate = _plant(rng, stratum)
        if candidate is None:
            continue
        agree, verdict_a, _ = oracle_agrees(candidate)
        if not agree or verdict_a.terminal != stratum:
            continue
        return Instance(
            instance_id=f"{split}-{stratum}-{index:04d}",
            suite=SUITE,
            stratum=stratum,
            observables=candidate.observables,
            cases=candidate.cases,
            active_formalism=candidate.active_formalism,
            parent_formalisms=candidate.parent_formalisms,
            relations=candidate.relations,
            patch_budget=candidate.patch_budget,
            planted_decoys=candidate.planted_decoys,
        )
    raise RuntimeError(f"generator exhausted for stratum {stratum} index {index}")


def generate_split(split: str, split_seed: str, per_stratum: int) -> tuple[Instance, ...]:
    out: list[Instance] = []
    for stratum in STRATA:
        for index in range(per_stratum):
            out.append(generate_instance(split, split_seed, stratum, index))
    return tuple(out)


# ---------------------------------------------------------------------------
# hand-authored known-answer fixtures (gate G0a)
# ---------------------------------------------------------------------------


def _fixture_observables(unobserved: bool = True) -> tuple[Observable, ...]:
    return (
        Observable("a", ("0", "1"), True),
        Observable("b", ("0", "1"), True),
        Observable("c", ("0", "1"), True),
        Observable("u", ("0", "1"), not unobserved),
    )


def _fx_case(case_id: str, a: str, b: str, c: str, u: str, decision: str) -> Case:
    return Case(case_id, (("a", a), ("b", b), ("c", c), ("u", u)), decision)


def known_answer_fixtures() -> tuple[dict[str, Any], ...]:
    obs = _fixture_observables()
    active = Formalism("F_ACTIVE", (atom("a"),))

    # KA-01 NO_CHANGE: `a` already fixes J; b and c vary freely inside a class.
    ka01 = Instance(
        "KA-01", SUITE, NO_CHANGE, obs,
        (
            _fx_case("x0", "0", "0", "0", "0", "d0"),
            _fx_case("x1", "0", "1", "1", "1", "d0"),
            _fx_case("x2", "1", "0", "1", "0", "d1"),
            _fx_case("x3", "1", "1", "0", "1", "d1"),
        ),
        active, (Formalism("P0", (atom("b"),)),), (), PATCH_BUDGET,
    )

    # KA-02 PARENT_FORMALISM_SUFFICIENT: J = b; P0 = {b} is registered.
    ka02 = Instance(
        "KA-02", SUITE, PARENT_FORMALISM_SUFFICIENT, obs,
        (
            _fx_case("x0", "0", "0", "0", "0", "d0"),
            _fx_case("x1", "0", "1", "1", "1", "d1"),
            _fx_case("x2", "1", "0", "1", "0", "d0"),
            _fx_case("x3", "1", "1", "0", "1", "d1"),
        ),
        active,
        (Formalism("P0", (atom("b"), atom("c"))), Formalism("P1", (atom("c"),))),
        (Relation("R", (("x0", "x2"), ("x1", "x3"))),),
        PATCH_BUDGET,
    )

    # KA-03 ADD_ONE_OBSERVATION: J = u (unobserved); a, b, c alias each pair.
    ka03 = Instance(
        "KA-03", SUITE, ADD_ONE_OBSERVATION, obs,
        (
            _fx_case("x0", "0", "0", "0", "0", "d0"),
            _fx_case("x1", "0", "0", "0", "1", "d1"),
            _fx_case("x2", "1", "1", "1", "0", "d0"),
            _fx_case("x3", "1", "1", "1", "1", "d1"),
        ),
        active,
        (Formalism("P0", (atom("b"), atom("c"))), Formalism("P1", (atom("c"),))),
        (),
        PATCH_BUDGET,
    )

    # KA-04 LOCAL_PATCH: J = a except one exceptional case per a-class.
    ka04 = Instance(
        "KA-04", SUITE, LOCAL_PATCH, obs,
        (
            _fx_case("x0", "0", "0", "0", "0", "d0"),
            _fx_case("x1", "0", "1", "1", "1", "d0"),
            _fx_case("x2", "0", "1", "0", "1", "d1"),
            _fx_case("x3", "1", "0", "1", "0", "d1"),
            _fx_case("x4", "1", "1", "0", "0", "d1"),
            _fx_case("x5", "1", "0", "0", "1", "d0"),
        ),
        active,
        (Formalism("P0", (atom("b"),)), Formalism("P1", (atom("c"),))),
        (),
        PATCH_BUDGET,
    )

    # KA-05 REPRESENTATION_CHANGE: J = EQ(b, c); the registered parents
    # {a,b} and {a,c} each alias a decision-distinct pair, no single atom
    # separates, and the collision graph needs a cover of 4 > budget 2.
    ka05 = Instance(
        "KA-05", SUITE, REPRESENTATION_CHANGE, obs,
        (
            _fx_case("x0", "0", "0", "0", "0", "d0"),
            _fx_case("x1", "0", "0", "1", "0", "d1"),
            _fx_case("x2", "0", "1", "0", "0", "d1"),
            _fx_case("x3", "0", "1", "1", "0", "d0"),
            _fx_case("x4", "1", "0", "0", "1", "d0"),
            _fx_case("x5", "1", "0", "1", "1", "d1"),
            _fx_case("x6", "1", "1", "0", "1", "d1"),
            _fx_case("x7", "1", "1", "1", "1", "d0"),
        ),
        active,
        (Formalism("P0", (atom("a"), atom("b"))), Formalism("P1", (atom("a"), atom("c")))),
        (),
        PATCH_BUDGET,
    )

    # KA-06 NEW_PRIMITIVE: x0/x1, x2/x3 and x4/x5 are pairwise identical in
    # every recorded and unrecorded observable but judged differently, so no
    # parent, observation or derived term can separate them and the collision
    # graph needs a cover of 3 > budget 2; the registered relation's connected
    # components do separate them.
    ka06 = Instance(
        "KA-06", SUITE, NEW_PRIMITIVE, obs,
        (
            _fx_case("x0", "0", "0", "0", "0", "d0"),
            _fx_case("x1", "0", "0", "0", "0", "d1"),
            _fx_case("x2", "0", "1", "1", "1", "d0"),
            _fx_case("x3", "0", "1", "1", "1", "d1"),
            _fx_case("x4", "1", "0", "1", "0", "d0"),
            _fx_case("x5", "1", "0", "1", "0", "d1"),
        ),
        active,
        (Formalism("P0", (atom("a"), atom("b"))), Formalism("P1", (atom("b"), atom("c")))),
        (Relation("R_LATENT", (("x0", "x2"), ("x2", "x4"), ("x1", "x3"), ("x3", "x5"))),),
        PATCH_BUDGET,
    )
    return (
        {"name": "KA-01-NO_CHANGE", "instance": ka01, "expected": NO_CHANGE},
        {"name": "KA-02-PARENT", "instance": ka02, "expected": PARENT_FORMALISM_SUFFICIENT},
        {"name": "KA-03-ADD_ONE_OBSERVATION", "instance": ka03, "expected": ADD_ONE_OBSERVATION},
        {"name": "KA-04-LOCAL_PATCH", "instance": ka04, "expected": LOCAL_PATCH},
        {"name": "KA-05-REPRESENTATION_CHANGE", "instance": ka05, "expected": REPRESENTATION_CHANGE},
        {"name": "KA-06-NEW_PRIMITIVE", "instance": ka06, "expected": NEW_PRIMITIVE},
    )
