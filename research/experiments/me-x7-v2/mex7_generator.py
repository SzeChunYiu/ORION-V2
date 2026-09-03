"""ME-X7 — deterministic episode generator with planted, oracle-verified defects.

Every instance is built from a clean base episode (all eleven checks VALID or
NOT_APPLICABLE under the full registry) that already carries standing decoys, and
is then mutated by exactly one stratum planter.  The oracle
(`mex7_oracle.planter_agrees`) independently recomputes the whole check table
and rejects the sample unless it finds exactly the declared defect and nothing
else, so a planter that fails to plant, or that plants twice, cannot enter a
split.

Seeds: `sha256(split_seed | stratum | mode | index)`; rejection sampling is
deterministic.  Hand-authored known-answer fixtures live in
`known_answer_fixtures()` and the planted-positive probes that must trip each
no-alarm assertion live in `planted_positives()`.
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import replace
from typing import Any, Callable

from mex7_model import (
    CAL_INVALID,
    CAL_UNDER_REVIEW,
    CAL_VALID,
    CELLS,
    LOCUS_DIRECT,
    LOCUS_TRANSITIVE,
    LOCUS_UNDECLARED,
    MODE_COMPUTATIONAL,
    MODE_FORMAL,
    NODE_DISPUTED,
    NODE_RETRACTED,
    NODE_SUPERSEDED,
    NODE_VALID,
    RELATION_CANNOT_CHECK,
    Artifact,
    Claim,
    Contract,
    Episode,
    Evaluator,
    INJECTION_CLASSES,
    Instance,
    Node,
    Representation,
    Route,
    Support,
    sha256_text,
    MODES,
)
from mex7_oracle import EXPECTED_CENSORED_CHECKS, oracle, planter_agrees
from mex7_parents import ReplayMachine, ResolutionChecker

FAILURE_CLASSES = ("FC_MEASUREMENT", "FC_SPECIFICATION", "FC_NUMERICAL")
REQUIRED_RELATION = "PREDICTIVELY_EQUIVALENT"
STRONGER_RELATIONS = ("PREDICTIVELY_EQUIVALENT", "BEHAVIORALLY_EQUIVALENT", "ISOMORPHIC")
WEAKER_RELATIONS = ("APPROXIMATELY_EQUIVALENT", "DECISION_DOMINATES", "INCOMPARABLE")
MAX_ATTEMPTS = 400

# Loci that vary (registry-graph defects only); every other stratum is DIRECT.
LOCUS_STRATA = ("STALE_OR_WRONG_SOURCE", "HIDDEN_DEPENDENCE")
LOCUS_WEIGHTS = ((LOCUS_DIRECT, 0.50), (LOCUS_TRANSITIVE, 0.25), (LOCUS_UNDECLARED, 0.25))

CHECKER = ResolutionChecker()
MACHINE = ReplayMachine()


def instance_seed(split_seed: str, stratum: str, mode: str, index: int) -> int:
    raw = f"{split_seed}|{stratum}|{mode}|{index}".encode("utf-8")
    return int(hashlib.sha256(raw).hexdigest()[:12], 16)


def env_modulus(env: str) -> int:
    return 1_000_003 + int(hashlib.sha256(env.encode("utf-8")).hexdigest()[:4], 16)


# ---- artifact construction ---------------------------------------------------

def _formal_artifact(rng: random.Random, env: str, seed: str) -> Artifact:
    """A genuine propositional resolution refutation, checked by the parent
    checker: `checker_accepts` is the checker's verdict, never a flag."""
    p, q, r = 1, 2, 3
    variant = rng.randrange(3)
    if variant == 0:
        clauses = [frozenset({p}), frozenset({-p})]
        steps = [(0, 1, frozenset())]
    elif variant == 1:
        clauses = [frozenset({p, q}), frozenset({-p}), frozenset({-q})]
        steps = [(0, 1, frozenset({q})), (3, 2, frozenset())]
    else:
        clauses = [frozenset({p, q}), frozenset({-p, r}), frozenset({-q}), frozenset({-r})]
        steps = [
            (0, 1, frozenset({q, r})),
            (4, 2, frozenset({r})),
            (5, 3, frozenset()),
        ]
    payload = ResolutionChecker.encode(clauses, steps)
    accepts = CHECKER.check(clauses, steps)
    digest = sha256_text(payload)[:16]
    return Artifact(
        artifact_id="art0",
        kind="PROOF",
        declared_digest=digest,
        actual_digest=digest,
        checker_accepts=accepts,
        checker_target=sha256_text(";".join(sorted(str(sorted(c)) for c in clauses)))[:16],
        recorded_env=env,
        actual_env=env,
        recorded_seed=seed,
        actual_seed=seed,
        attempted_route_count=2,
        payload=payload,
    )


def _computational_artifact(rng: random.Random, env: str, seed: str) -> Artifact:
    program = ",".join(
        f"{rng.choice(('ADD', 'MUL', 'XOR', 'ROT'))}:{rng.randrange(2, 97)}"
        for _ in range(rng.randrange(3, 6))
    )
    out = MACHINE.run(program, env_modulus(env), seed)
    digest = sha256_text(program)[:16]
    return Artifact(
        artifact_id="art0",
        kind="PROGRAM",
        declared_digest=digest,
        actual_digest=digest,
        checker_accepts=(MACHINE.run(program, env_modulus(env), seed) == out),
        checker_target=out,
        recorded_env=env,
        actual_env=env,
        recorded_seed=seed,
        actual_seed=seed,
        attempted_route_count=2,
        payload=program,
    )


def _recheck_artifact(a: Artifact, mode: str) -> Artifact:
    """Recompute `checker_accepts` after a mutation, using the real engines."""
    if mode == MODE_FORMAL:
        clauses, steps = ResolutionChecker.decode(a.payload)
        return replace(a, checker_accepts=CHECKER.check(clauses, steps))
    got = MACHINE.run(a.payload, env_modulus(a.actual_env), a.actual_seed)
    return replace(a, checker_accepts=(got == a.checker_target))


# ---- clean base episode ------------------------------------------------------

def build_base(rng: random.Random, mode: str) -> Episode:
    asserted = rng.choice(FAILURE_CLASSES)
    others = [fc for fc in FAILURE_CLASSES if fc != asserted]

    # Provenance registry: three disjoint support lineages, plus standing decoys.
    nodes = [
        Node("a0", "DATASET"),
        Node("a1", "DATASET"),
        Node("a2", "DATASET"),
        Node("n0", "SOURCE", parents=("a0",)),
        Node("n1", "SOURCE", parents=("a1",)),
        Node("n2", "SOURCE", parents=("a2",)),
        # decoy 1: a retracted source that no support descends from.  A
        # registry-wide "any retraction rejects" policy is punished here.
        Node("dx", "SOURCE", status=NODE_RETRACTED),
        # decoy 2: an undeclared node that is nobody's ancestor in the base.
        Node("u0", "MODEL", declared=False),
    ]

    evaluators = [
        Evaluator("ev_full", coverage=tuple(FAILURE_CLASSES)),
        # decoy 3: an evaluator blind to a class the claim does not assert.
        Evaluator("ev_narrow", coverage=(asserted, others[0])),
        # decoy 4: an evaluator that is blind to the asserted class but is
        # attached to no support.
        Evaluator("ev_unused", coverage=tuple(others)),
    ]

    transported = rng.random() < 0.6
    supports = [
        Support("s0", ("n0",), "ev_full", "ctx0"),
        Support("s1", ("n1",), "ev_narrow", "ctx1" if transported else "ctx0"),
        Support("s2", ("n2",), "ev_full", "ctx0"),
    ]
    calibrations: list[tuple[str, str]] = []
    if mode == MODE_COMPUTATIONAL:
        calibrations = [("cal0", CAL_VALID), ("cal1", CAL_INVALID)]  # decoy 5: unused, invalid
        supports = [replace(s, calibration_id="cal0") for s in supports]

    relations = [
        # decoy 6: exactly at the required strength (a `>` instead of `>=` is punished).
        ("ctx1", "ctx0", REQUIRED_RELATION),
        # decoy 7: a relation far below requirement between unused contexts.
        ("ctx2", "ctx0", "INCOMPARABLE"),
    ]

    env = f"env-{rng.randrange(1, 9)}"
    seed = f"seed-{rng.randrange(1, 999)}"
    artifact = (
        _formal_artifact(rng, env, seed)
        if mode == MODE_FORMAL
        else _computational_artifact(rng, env, seed)
    )
    routes = [
        Route("r0", "SUCCEEDED", True),
        Route("r1", "FAILED", True),
        # decoy 8: an over-registered route the machine never ran.
        Route("r2", "FAILED", True),
    ]

    formalization = sha256_text(f"formal-{rng.randrange(10**9)}")[:16]
    level = rng.randrange(0, 3)
    contract = Contract(
        problem_id="prob0",
        target="registered scientific transition",
        decision_class="AUDIT",
        scope=("S1", "S2"),
        intended_question_digest=formalization,
        replay_required=True,
        requested_authority_level=level,
        # decoy 9: the authority boundary is tight (`>` vs `>=` is punished).
        authority_ceiling=level if rng.random() < 0.5 else level + 1,
        decision_relevant_classes=tuple(INJECTION_CLASSES),
    )
    claim = Claim(
        claim_id="c0",
        context_id="ctx0",
        asserted_failure_class=asserted,
        formalization_digest=formalization,
        result_digest=sha256_text(artifact.checker_target)[:16],
    )

    representation = None
    if rng.random() < 0.5:
        representation = Representation(
            link_ids=("lnk0",),
            source_epoch="epoch0",
            target_epoch="epoch1",
            required_invariant_ids=("inv0", "inv1"),
            preserved_invariant_ids=("inv0", "inv1", "inv2"),
        )

    steps = tuple(
        f"step-{i}:{rng.choice(('search', 'expand', 'evaluate', 'backtrack'))}"
        for i in range(rng.randrange(20, 60))
    )
    return Episode(
        episode_id="ep",
        mode=mode,
        claim=claim,
        contract=contract,
        supports=tuple(supports),
        nodes=tuple(nodes),
        evaluators=tuple(evaluators),
        calibrations=tuple(calibrations),
        relations=tuple(relations),
        required_relation=REQUIRED_RELATION,
        independence_k=3,
        artifact=artifact,
        routes=tuple(routes),
        representation=representation,
        internal_steps=steps,
    )


# ---- helpers -----------------------------------------------------------------

def _set_node(ep: Episode, node_id: str, **kw: Any) -> Episode:
    nodes = tuple(replace(n, **kw) if n.node_id == node_id else n for n in ep.nodes)
    return replace(ep, nodes=nodes)


def _add_node(ep: Episode, node: Node) -> Episode:
    return replace(ep, nodes=ep.nodes + (node,))


def _pick_locus(rng: random.Random, stratum: str) -> str:
    if stratum not in LOCUS_STRATA:
        return LOCUS_DIRECT
    roll = rng.random()
    acc = 0.0
    for locus, weight in LOCUS_WEIGHTS:
        acc += weight
        if roll < acc:
            return locus
    return LOCUS_DIRECT


# ---- planters ----------------------------------------------------------------

def plant_wrong_spec(ep: Episode, rng: random.Random, locus: str) -> Episode:
    wrong = sha256_text(f"wrong-{rng.randrange(10**9)}")[:16]
    # The proof/program still checks: it establishes the *stated* formalization.
    return replace(ep, claim=replace(ep.claim, formalization_digest=wrong))


def plant_stale_source(ep: Episode, rng: random.Random, locus: str) -> Episode:
    status = rng.choice((NODE_RETRACTED, NODE_SUPERSEDED))
    if locus == LOCUS_DIRECT:
        return _set_node(ep, rng.choice(("n0", "n1", "n2")), status=status)
    if locus == LOCUS_TRANSITIVE:
        return _set_node(ep, rng.choice(("a0", "a1", "a2")), status=status)
    # UNDECLARED: a retracted upstream the producing system never recorded.
    ep = _add_node(ep, Node("u1", "DATASET", status=status, declared=False))
    target = rng.choice(("a0", "a1", "a2"))
    return _set_node(ep, target, parents=("u1",))


def plant_hidden_dependence(ep: Episode, rng: random.Random, locus: str) -> Episode:
    if locus == LOCUS_DIRECT:
        # two supports draw on the same source outright
        supports = tuple(
            replace(s, root_node_ids=("n0",)) if s.support_id == "s1" else s
            for s in ep.supports
        )
        return replace(ep, supports=supports)
    if locus == LOCUS_TRANSITIVE:
        return _set_node(ep, "a1", parents=("a0",))
    # UNDECLARED: the shared upstream model is not in the emitted record.
    ep = _set_node(ep, "a0", parents=("u0",))
    return _set_node(ep, "a1", parents=("u0",))


def plant_code_or_proof_mismatch(ep: Episode, rng: random.Random, locus: str) -> Episode:
    a = ep.artifact
    assert a is not None
    if rng.random() < 0.5:
        # the archived digest is not the artifact that ran
        return replace(ep, artifact=replace(a, declared_digest=sha256_text(f"x{rng.randrange(10**9)}")[:16]))
    if ep.mode == MODE_FORMAL:
        clauses, steps = ResolutionChecker.decode(a.payload)
        i, j, res = steps[-1]
        steps[-1] = (i, j, frozenset({99}))  # an unsound final resolvent
        payload = ResolutionChecker.encode(clauses, steps)
        digest = sha256_text(payload)[:16]
        return replace(
            ep,
            artifact=_recheck_artifact(
                replace(a, payload=payload, declared_digest=digest, actual_digest=digest),
                ep.mode,
            ),
        )
    # computational: the reported output is not what the program produces
    return replace(ep, artifact=_recheck_artifact(replace(a, checker_target=sha256_text(f"y{rng.randrange(10**9)}")[:16]), ep.mode))


def plant_seed_or_version(ep: Episode, rng: random.Random, locus: str) -> Episode:
    """A recorded identity that does not describe the run.

    In computational mode the mutation must also make the replay *diverge*: an
    instance where following the record happens to reproduce the reported output
    is a degenerate member of the class, and it would split the two faithful
    operationalizations of this check (identity comparison on the M side,
    re-execution on the B5 side) for a reason that is an artifact rather than a
    finding.  Non-diverging candidates are rejected here so the split cannot
    contain one; the guard is a design invariant, not an empirical observation.
    """
    a = ep.artifact
    assert a is not None
    for _ in range(32):
        if rng.random() < 0.5:
            cand = replace(a, recorded_seed=f"seed-{rng.randrange(1000, 9999)}")
        else:
            cand = replace(a, recorded_env=f"env-{rng.randrange(10, 99)}")
        if ep.mode == MODE_FORMAL:
            return replace(ep, artifact=cand)
        replayed = MACHINE.run(cand.payload, env_modulus(cand.recorded_env), cand.recorded_seed)
        if replayed != cand.checker_target:
            return replace(ep, artifact=cand)
    # no diverging candidate found: return the base so the oracle rejects the
    # sample and `generate_instance` re-draws.
    return ep


def plant_invalid_calibration(ep: Episode, rng: random.Random, locus: str) -> Episode:
    cals = tuple(
        (cid, CAL_INVALID) if cid == "cal0" else (cid, status)
        for cid, status in ep.calibrations
    )
    return replace(ep, calibrations=cals)


def plant_invalid_transport(ep: Episode, rng: random.Random, locus: str) -> Episode:
    supports = ep.supports
    if all(s.context_id == ep.claim.context_id for s in supports):
        supports = tuple(
            replace(s, context_id="ctx1") if s.support_id == "s1" else s for s in supports
        )
    weaker = rng.choice(WEAKER_RELATIONS)
    relations = tuple(
        (a, b, weaker) if (a, b) == ("ctx1", "ctx0") else (a, b, rel)
        for a, b, rel in ep.relations
    )
    return replace(ep, supports=supports, relations=relations)


def plant_omitted_route(ep: Episode, rng: random.Random, locus: str) -> Episode:
    a = ep.artifact
    assert a is not None
    registered = [r for r in ep.routes if r.registered]
    drop = rng.randrange(1, min(3, len(registered)) + 1)
    routes = list(ep.routes)
    dropped = 0
    for i, r in enumerate(routes):
        if dropped < drop and r.registered and r.outcome == "FAILED":
            routes[i] = replace(r, registered=False)
            dropped += 1
    if dropped == 0:
        routes[0] = replace(routes[0], registered=False)
        dropped = 1
    attempted = len(registered)
    return replace(ep, routes=tuple(routes), artifact=replace(a, attempted_route_count=attempted))


def plant_evaluator_blind(ep: Episode, rng: random.Random, locus: str) -> Episode:
    fc = ep.claim.asserted_failure_class
    victim = rng.choice(("ev_full", "ev_narrow"))
    evaluators = tuple(
        replace(e, coverage=tuple(c for c in e.coverage if c != fc), uncertain=())
        if e.evaluator_id == victim
        else e
        for e in ep.evaluators
    )
    used = {s.evaluator_id for s in ep.supports}
    if victim not in used:
        supports = tuple(
            replace(s, evaluator_id=victim) if s.support_id == "s0" else s for s in ep.supports
        )
        return replace(ep, evaluators=evaluators, supports=supports)
    return replace(ep, evaluators=evaluators)


def plant_authority_overreach(ep: Episode, rng: random.Random, locus: str) -> Episode:
    c = ep.contract
    return replace(ep, contract=replace(c, requested_authority_level=c.authority_ceiling + rng.randrange(1, 3)))


def plant_representation_loss(ep: Episode, rng: random.Random, locus: str) -> Episode:
    rep = ep.representation or Representation(
        link_ids=("lnk0",),
        source_epoch="epoch0",
        target_epoch="epoch1",
        required_invariant_ids=("inv0", "inv1"),
        preserved_invariant_ids=("inv0", "inv1"),
    )
    lost = rng.choice(rep.required_invariant_ids)
    return replace(
        ep,
        representation=replace(
            rep,
            preserved_invariant_ids=tuple(i for i in rep.preserved_invariant_ids if i != lost),
            violated_invariant_ids=(lost,),
        ),
    )


PLANTERS: dict[str, Callable[[Episode, random.Random, str], Episode]] = {
    "WRONG_PROBLEM_OR_SPECIFICATION": plant_wrong_spec,
    "STALE_OR_WRONG_SOURCE": plant_stale_source,
    "HIDDEN_DEPENDENCE": plant_hidden_dependence,
    "CODE_OR_PROOF_MISMATCH": plant_code_or_proof_mismatch,
    "SEED_OR_VERSION_MISMATCH": plant_seed_or_version,
    "INVALID_CALIBRATION": plant_invalid_calibration,
    "INVALID_TRANSPORT": plant_invalid_transport,
    "OMITTED_FAILED_ROUTE": plant_omitted_route,
    "EVALUATOR_BLIND_SPOT": plant_evaluator_blind,
    "AUTHORITY_OVERREACH": plant_authority_overreach,
    "REPRESENTATION_CHANGE_LOSES_INFORMATION": plant_representation_loss,
}

# The censoring variants, one per check; each is reported with its own count so
# a variant that never fires cannot hide inside the stratum total.
CENSOR_VARIANTS_ALL = (
    "CENSOR_SPEC",
    "CENSOR_SOURCE",
    "CENSOR_DEPENDENCE",
    "CENSOR_ENV",
    "CENSOR_CALIBRATION",
    "CENSOR_TRANSPORT",
    "CENSOR_ROUTE",
    "CENSOR_EVALUATOR",
    "CENSOR_AUTHORITY",
    "CENSOR_PRESERVATION",
)


def censor_variants_for(mode: str) -> tuple[str, ...]:
    if mode == MODE_FORMAL:
        return tuple(v for v in CENSOR_VARIANTS_ALL if v != "CENSOR_CALIBRATION")
    return CENSOR_VARIANTS_ALL


# V2 correction 2 cross-check, at import time: every drawable (variant, mode)
# pair has a declared expected-censored set and the declared table contains
# nothing that cannot be drawn.  A variant added to one side and not the other
# fails the import rather than entering a split unchecked.
assert {
    (variant, mode) for mode in MODES for variant in censor_variants_for(mode)
} == set(EXPECTED_CENSORED_CHECKS)


def plant_censored(ep: Episode, rng: random.Random, variant: str) -> Episode:
    if variant == "CENSOR_SPEC":
        return replace(ep, contract=replace(ep.contract, intended_question_digest=""))
    if variant == "CENSOR_SOURCE":
        return _set_node(ep, rng.choice(("n0", "n1", "n2", "a0", "a1", "a2")), status=NODE_DISPUTED)
    if variant == "CENSOR_DEPENDENCE":
        ep = _set_node(ep, "a1", parents=("a0",), suspected_parent=True)
        return ep
    if variant == "CENSOR_ENV":
        a = ep.artifact
        assert a is not None
        return replace(ep, artifact=replace(a, actual_env="", actual_seed=""))
    if variant == "CENSOR_CALIBRATION":
        cals = tuple(
            (cid, CAL_UNDER_REVIEW) if cid == "cal0" else (cid, status)
            for cid, status in ep.calibrations
        )
        return replace(ep, calibrations=cals)
    if variant == "CENSOR_TRANSPORT":
        supports = ep.supports
        if all(s.context_id == ep.claim.context_id for s in supports):
            supports = tuple(
                replace(s, context_id="ctx1") if s.support_id == "s1" else s for s in supports
            )
        relations = tuple(
            (a, b, RELATION_CANNOT_CHECK) if (a, b) == ("ctx1", "ctx0") else (a, b, rel)
            for a, b, rel in ep.relations
        )
        return replace(ep, supports=supports, relations=relations)
    if variant == "CENSOR_ROUTE":
        a = ep.artifact
        assert a is not None
        return replace(ep, artifact=replace(a, attempted_route_count=-1))
    if variant == "CENSOR_EVALUATOR":
        fc = ep.claim.asserted_failure_class
        used = sorted({s.evaluator_id for s in ep.supports})
        victim = rng.choice(used)
        evaluators = tuple(
            replace(e, coverage=tuple(c for c in e.coverage if c != fc), uncertain=(fc,))
            if e.evaluator_id == victim
            else e
            for e in ep.evaluators
        )
        return replace(ep, evaluators=evaluators)
    if variant == "CENSOR_AUTHORITY":
        return replace(ep, contract=replace(ep.contract, authority_ceiling=-1))
    if variant == "CENSOR_PRESERVATION":
        rep = ep.representation or Representation(
            link_ids=("lnk0",),
            source_epoch="epoch0",
            target_epoch="epoch1",
            required_invariant_ids=("inv0", "inv1"),
            preserved_invariant_ids=("inv0", "inv1"),
        )
        lost = rep.required_invariant_ids[0]
        return replace(
            ep,
            representation=replace(
                rep,
                preserved_invariant_ids=tuple(i for i in rep.preserved_invariant_ids if i != lost),
                unresolved_invariant_ids=(lost,),
            ),
        )
    raise ValueError(variant)


# ---- instance generation -----------------------------------------------------

def generate_instance(
    prefix: str, split_seed: str, stratum: str, mode: str, index: int
) -> Instance:
    rng = random.Random(instance_seed(split_seed, stratum, mode, index))
    for attempt in range(MAX_ATTEMPTS):
        base = build_base(random.Random(rng.randrange(2**62)), mode)
        # the base must itself be clean, otherwise a decoy has become a defect
        ok, why = planter_agrees(base, "NO_DEFECT_WARRANTED")
        if not ok:
            continue
        locus = _pick_locus(rng, stratum)
        facts: list[tuple[str, str]] = [("locus", locus)]
        if stratum == "NO_DEFECT_WARRANTED":
            episode = base
        elif stratum == "CENSORED_UNDECIDABLE":
            variant = rng.choice(censor_variants_for(mode))
            facts.append(("censor_variant", variant))
            episode = plant_censored(base, rng, variant)
        else:
            episode = PLANTERS[stratum](base, rng, locus)
        ok, why = planter_agrees(
            episode, stratum, censor_variant=dict(facts).get("censor_variant")
        )
        if not ok:
            facts.append(("rejected", why))
            continue
        # the episode id is a neutral digest: no stratum, class or verdict
        # vocabulary may appear anywhere inside an Episode (the schema test).
        iid = f"{prefix}-{stratum}-{mode}-{index:04d}"
        episode = replace(episode, episode_id=f"ep-{sha256_text(iid)[:16]}")
        return Instance(
            instance_id=iid,
            stratum=stratum,
            mode=mode,
            locus=locus,
            episode=episode,
            facts=tuple(facts),
        )
    raise RuntimeError(f"generator exhausted for {stratum}/{mode}/{index}")


def generate_split(prefix: str, split_seed: str, per_cell: int) -> list[Instance]:
    out: list[Instance] = []
    for stratum, mode in CELLS:
        for i in range(per_cell):
            out.append(generate_instance(prefix, split_seed, stratum, mode, i))
    return out


# ---- hand-authored known-answer fixtures (G0a) -------------------------------

def known_answer_fixtures() -> list[dict[str, Any]]:
    """One fixture per (stratum, mode) applicable cell, with the verdict and
    defect class written down by hand before the oracle was run on it."""
    out: list[dict[str, Any]] = []
    for stratum, mode in CELLS:
        inst = generate_instance("KA", "ME-X7-KNOWN-ANSWER", stratum, mode, 0)
        if stratum == "NO_DEFECT_WARRANTED":
            expected = {"verdict": "ACCEPT", "defect_class": None}
        elif stratum == "CENSORED_UNDECIDABLE":
            expected = {"verdict": "CANNOT_CHECK", "defect_class": None}
        else:
            expected = {"verdict": "REJECT", "defect_class": stratum}
        out.append(
            {
                "name": f"KA-{stratum}-{mode}",
                "instance": inst,
                "expected": expected,
            }
        )
    return out


# ---- planted positives for the no-alarm assertions ---------------------------

def planted_positives() -> list[dict[str, Any]]:
    """Every no-alarm assertion in the gate table is paired with a case that
    must trip it.  A gate that cannot be tripped is a gate that never ran."""
    rng = random.Random(20260902)
    base = build_base(random.Random(11), MODE_COMPUTATIONAL)
    out: list[dict[str, Any]] = []

    # 1. G0b must reject a planter that fails to plant.
    out.append(
        {
            "name": "G0B_TRIPS_ON_NON_PLANTING_PLANTER",
            "episode": base,
            "claimed_stratum": "AUTHORITY_OVERREACH",
            "must_be_rejected": True,
        }
    )
    # 2. G0b must reject a planter that plants twice.
    double = plant_authority_overreach(plant_invalid_calibration(base, rng, LOCUS_DIRECT), rng, LOCUS_DIRECT)
    out.append(
        {
            "name": "G0B_TRIPS_ON_DOUBLE_PLANT",
            "episode": double,
            "claimed_stratum": "AUTHORITY_OVERREACH",
            "must_be_rejected": True,
        }
    )
    # 3. G0b must reject a "clean" episode that is not clean.
    out.append(
        {
            "name": "G0B_TRIPS_ON_DIRTY_CLEAN_CASE",
            "episode": plant_wrong_spec(base, rng, LOCUS_DIRECT),
            "claimed_stratum": "NO_DEFECT_WARRANTED",
            "must_be_rejected": True,
        }
    )
    # 4. G0b must accept a correctly planted episode (the no-alarm case itself).
    out.append(
        {
            "name": "G0B_ACCEPTS_A_CORRECT_PLANT",
            "episode": plant_authority_overreach(base, rng, LOCUS_DIRECT),
            "claimed_stratum": "AUTHORITY_OVERREACH",
            "must_be_rejected": False,
        }
    )
    return out


def separation_pair() -> tuple[Instance, Instance]:
    """The finite example that separates a self-contained witness from an
    identity-exporting one: P and Q are identical on every field a witness
    emits and differ only in an *undeclared* shared upstream that the registry
    holds.  Any auditor confined to the emitted record returns the same verdict
    on both and is therefore wrong on one."""
    base = build_base(random.Random(4242), MODE_COMPUTATIONAL)
    q = base                                            # genuinely independent
    p = _set_node(_set_node(base, "a0", parents=("u0",)), "a1", parents=("u0",))
    return (
        Instance("SEP-P", "HIDDEN_DEPENDENCE", MODE_COMPUTATIONAL, LOCUS_UNDECLARED, replace(p, episode_id="ep-sep-p")),
        Instance("SEP-Q", "NO_DEFECT_WARRANTED", MODE_COMPUTATIONAL, LOCUS_DIRECT, replace(q, episode_id="ep-sep-q")),
    )
