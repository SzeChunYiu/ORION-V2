"""ME-X7 — witness surfaces, the parent federation, M, the ablations and the
controls.

This module never imports the oracle.  It carries **two independently written
implementations of the frozen §2.3 check table**, and the arms are split
between them:

* `MODULE_CHECK_M` — the ORION-registered semantics that the claim-sufficient
  witness is a projection of: `ProblemContract` metadata for criterion binding,
  an ancestor walk over the registered provenance graph,
  `orion_v2.evidence.assess_evidence_dependence` over ancestor-set overlap,
  `orion_v2.correspondence.assess_correspondence_chain` for preservation,
  `RelationType` rank for transport, evaluator coverage, and the recorded
  environment/seed identities.
* `MODULE_CHECK_B5` — the faithful parent federation's own engines:
  `ReticulateProvenance.affected_by_revocation` reachability (the opposite
  traversal direction), dependence pairs from that same descendant walk,
  `orion_v2.comparability.ComparabilityCertificate` for preservation, and an
  actual re-execution of the replay machine under the recorded versus the
  actual environment rather than a comparison of recorded identities.

Four of the eleven checks therefore run different code on the two sides —
source status, dependence, environment identity (computational mode) and
preservation.  The remaining seven are arithmetic thin enough that two
implementations would be the same three lines, and the receipt says so rather
than claiming eleven.  Both tables re-run the resolution checker and the replay
machine instead of trusting a recorded flag.

An arm is a *witness surface* (a set of exported fields), a registry-visibility
policy, a check table, and an adjudicator.  Surface arms and M share one frozen
adjudication rule; the single-parent arms use their own native semantics and
break where those semantics predict.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from orion_v2.comparability import Anchor, ComparabilityCertificate, ComparabilityStatus
from orion_v2.contracts import ProblemContract
from orion_v2.correspondence import (
    CorrespondenceLink,
    CorrespondenceStatus,
    assess_correspondence_chain,
)

from mex7_model import (
    ACCEPT,
    CANNOT_CHECK,
    CENSORED,
    CHECKS,
    CHECK_FOR_CLASS,
    CLASS_FOR_CHECK,
    FIELDS,
    INVALID,
    MODE_FORMAL,
    NOT_APPLICABLE,
    REJECT,
    RELATION_CANNOT_CHECK,
    RELATION_RANK,
    REQUIRED_FIELDS,
    CAL_INVALID,
    CAL_UNDER_REVIEW,
    Episode,
    F_ARTIFACT,
    F_ASSUMPTION_VERSION,
    F_AUTHORITY_CEILING,
    F_DEPENDENCE,
    F_EVALUATOR_CONTRACT,
    F_MEASUREMENT_CALIBRATION,
    F_PRESERVATION,
    F_PROBLEM_BINDING,
    F_PROVENANCE,
    F_RESULT,
    F_ROUTE_LEDGER,
    F_TRANSPORT_RELATION,
    NODE_DISPUTED,
    NODE_RETRACTED,
    NODE_SUPERSEDED,
    VALID,
)
from mex7_parents import (
    AssuranceCase,
    DependenceAudit,
    ProvenanceLineage,
    ReplayMachine,
    ResolutionChecker,
    SelectiveAbstention,
)

ALL_FIELDS = frozenset(FIELDS)
CHECKER = ResolutionChecker()
MACHINE = ReplayMachine()
LINEAGE = ProvenanceLineage()
DEPENDENCE = DependenceAudit()
ASSURANCE = AssuranceCase()
ABSTAIN = SelectiveAbstention()


def env_modulus(env: str) -> int:
    import hashlib

    return 1_000_003 + int(hashlib.sha256(env.encode("utf-8")).hexdigest()[:4], 16)


# ---- registry visibility ------------------------------------------------------

def visible_nodes(ep: Episode, *, full_registry: bool) -> frozenset[str]:
    """What the auditor can resolve.  `full_registry=True` models an
    identity-exporting witness whose identities are resolved against the shared
    registry; `False` models a self-contained witness carrying only the values
    the producing system declared."""
    return frozenset(ep.node_ids()) if full_registry else ep.declared_node_ids()


def _support_roots(ep: Episode, visible: frozenset[str]) -> dict[str, tuple[str, ...]]:
    return {
        s.support_id: tuple(r for r in s.root_node_ids if r in visible) for s in ep.supports
    }


def _node_parents(ep: Episode, visible: frozenset[str], *, include_suspected: bool) -> dict[str, tuple[str, ...]]:
    out: dict[str, tuple[str, ...]] = {}
    for n in ep.nodes:
        if n.node_id not in visible:
            continue
        if n.suspected_parent and not include_suspected:
            out[n.node_id] = ()
        else:
            out[n.node_id] = tuple(p for p in n.parents if p in visible)
    return out


# ---- the eleven module checks (independent implementation) --------------------

def m_spec_binding(ep: Episode, visible: frozenset[str]) -> str:
    contract = ProblemContract(
        problem_id=ep.contract.problem_id,
        target=ep.contract.target,
        decision_class=ep.contract.decision_class,
        scope=ep.contract.scope,
        replay_required=ep.contract.replay_required,
        metadata=(("intended_question_digest", ep.contract.intended_question_digest),),
    )
    declared = dict(contract.metadata)["intended_question_digest"]
    if not declared:
        return CENSORED
    return VALID if declared == ep.claim.formalization_digest else INVALID


def _ancestors(ep: Episode, root: str, visible: frozenset[str], *, include_suspected: bool) -> set[str]:
    seen: set[str] = set()
    stack = [root]
    while stack:
        cur = stack.pop()
        if cur in seen or cur not in visible:
            continue
        seen.add(cur)
        node = ep.node(cur)
        if node.suspected_parent and not include_suspected:
            continue
        stack.extend(node.parents)
    return seen


def _m_ancestries(ep: Episode, visible: frozenset[str], *, include_suspected: bool) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for s in ep.supports:
        acc: set[str] = set()
        for root in s.root_node_ids:
            acc |= _ancestors(ep, root, visible, include_suspected=include_suspected)
        out[s.support_id] = acc
    return out


def m_source_status(ep: Episode, visible: frozenset[str]) -> str:
    """M side: walk *up* from the claim's supports over the registered
    provenance graph and read the statuses reached."""
    anc = _m_ancestries(ep, visible, include_suspected=True)
    reached = set().union(*anc.values()) if anc else set()
    statuses = {ep.node(n).status for n in reached}
    if statuses & {NODE_RETRACTED, NODE_SUPERSEDED}:
        return INVALID
    if NODE_DISPUTED in statuses:
        return CENSORED
    return VALID


def b5_source_status(ep: Episode, visible: frozenset[str]) -> str:
    """B5 side: revocation reachability through
    `orion_v2.provenance.ReticulateProvenance` descendants — the opposite
    traversal direction, using the parent's own engine."""
    roots = _support_roots(ep, visible)
    parents = _node_parents(ep, visible, include_suspected=True)
    revoked = {
        n.node_id
        for n in ep.nodes
        if n.node_id in visible and n.status in (NODE_RETRACTED, NODE_SUPERSEDED)
    }
    if LINEAGE.revoked_supports(roots, parents, revoked):
        return INVALID
    disputed = {n.node_id for n in ep.nodes if n.node_id in visible and n.status == NODE_DISPUTED}
    if LINEAGE.revoked_supports(roots, parents, disputed):
        return CENSORED
    return VALID


def _shared_pairs(ep: Episode, visible: frozenset[str], *, include_suspected: bool) -> list[tuple[str, str, bool]]:
    """Support pairs joined by a shared visible ancestor, found by walking
    *down* from every registry node (the opposite direction to the oracle)."""
    roots = _support_roots(ep, visible)
    parents = _node_parents(ep, visible, include_suspected=include_suspected)
    reach: dict[str, set[str]] = {}
    for support, rs in roots.items():
        seen: set[str] = set()
        stack = list(rs)
        while stack:
            cur = stack.pop()
            if cur in seen or cur not in visible:
                continue
            seen.add(cur)
            stack.extend(parents.get(cur, ()))
        reach[support] = seen
    ids = sorted(reach)
    out: list[tuple[str, str, bool]] = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if reach[a] & reach[b]:
                out.append((a, b, True))
    return out


def _m_pairs(ep: Episode, visible: frozenset[str], *, include_suspected: bool) -> list[tuple[str, str, bool]]:
    anc = _m_ancestries(ep, visible, include_suspected=include_suspected)
    ids = sorted(anc)
    out: list[tuple[str, str, bool]] = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if anc[a] & anc[b]:
                out.append((a, b, True))
    return out


def _components_from(pairs_fn, ep: Episode, visible: frozenset[str]) -> str:
    k = ep.independence_k
    ids = tuple(sorted(s.support_id for s in ep.supports))
    if k <= 1 or len(ids) < k:
        return NOT_APPLICABLE
    confirmed = DEPENDENCE.independent_components(
        ids, pairs_fn(ep, visible, include_suspected=False), include_suspected=False
    )
    if confirmed < k:
        return INVALID
    with_suspected = DEPENDENCE.independent_components(
        ids, pairs_fn(ep, visible, include_suspected=True), include_suspected=False
    )
    if with_suspected < k:
        return CENSORED
    return VALID


def m_dependence(ep: Episode, visible: frozenset[str]) -> str:
    """M side: independence over ancestor-set overlap, counted by
    `orion_v2.evidence.assess_evidence_dependence`."""
    return _components_from(_m_pairs, ep, visible)


def b5_dependence(ep: Episode, visible: frozenset[str]) -> str:
    """B5 side: the same parent counter over pairs found by walking *down*
    from every registry node."""
    return _components_from(_shared_pairs_kw, ep, visible)


def _shared_pairs_kw(ep: Episode, visible: frozenset[str], *, include_suspected: bool):
    return _shared_pairs(ep, visible, include_suspected=include_suspected)


def m_artifact_digest(ep: Episode, visible: frozenset[str]) -> str:
    a = ep.artifact
    if a is None:
        return NOT_APPLICABLE
    if a.declared_digest != a.actual_digest:
        return INVALID
    # re-run the checker rather than trusting the recorded flag
    if ep.mode == MODE_FORMAL:
        clauses, steps = ResolutionChecker.decode(a.payload)
        accepts = CHECKER.check(clauses, steps)
    else:
        accepts = MACHINE.run(a.payload, env_modulus(a.actual_env), a.actual_seed) == a.checker_target
    return VALID if accepts else INVALID


def m_env_identity(ep: Episode, visible: frozenset[str]) -> str:
    """M side: the recorded assumption/version identities must equal the ones
    that actually ran."""
    a = ep.artifact
    if a is None or not ep.contract.replay_required:
        return NOT_APPLICABLE
    if not a.actual_env or not a.actual_seed:
        return CENSORED
    return VALID if (a.recorded_env, a.recorded_seed) == (a.actual_env, a.actual_seed) else INVALID


def b5_env_identity(ep: Episode, visible: frozenset[str]) -> str:
    """B5 side: actually replay under the recorded identities and compare the
    output with the one the actual environment produced."""
    a = ep.artifact
    if a is None or not ep.contract.replay_required:
        return NOT_APPLICABLE
    if not a.actual_env or not a.actual_seed:
        return CENSORED
    if ep.mode == MODE_FORMAL:
        return VALID if (a.recorded_env, a.recorded_seed) == (a.actual_env, a.actual_seed) else INVALID
    replayed = MACHINE.run(a.payload, env_modulus(a.recorded_env), a.recorded_seed)
    actual = MACHINE.run(a.payload, env_modulus(a.actual_env), a.actual_seed)
    return VALID if replayed == actual else INVALID


def m_calibration(ep: Episode, visible: frozenset[str]) -> str:
    used = [s.calibration_id for s in ep.supports if s.calibration_id]
    if not used:
        return NOT_APPLICABLE
    statuses = {ep.calibration_status(c) for c in used}
    if CAL_INVALID in statuses:
        return INVALID
    if CAL_UNDER_REVIEW in statuses:
        return CENSORED
    return VALID


def m_transport(ep: Episode, visible: frozenset[str]) -> str:
    transported = [s for s in ep.supports if s.context_id != ep.claim.context_id]
    if not transported:
        return NOT_APPLICABLE
    need = RELATION_RANK[ep.required_relation]
    censored = False
    for s in transported:
        rel = ep.relation(s.context_id, ep.claim.context_id)
        if rel is None:
            return INVALID
        if rel == RELATION_CANNOT_CHECK:
            censored = True
        elif RELATION_RANK[rel] < need:
            return INVALID
    return CENSORED if censored else VALID


def m_route_completeness(ep: Episode, visible: frozenset[str]) -> str:
    a = ep.artifact
    if a is None:
        return NOT_APPLICABLE
    if a.attempted_route_count < 0:
        return CENSORED
    return INVALID if sum(1 for r in ep.routes if r.registered) < a.attempted_route_count else VALID


def m_evaluator_coverage(ep: Episode, visible: frozenset[str]) -> str:
    fc = ep.claim.asserted_failure_class
    censored = False
    for s in ep.supports:
        ev = ep.evaluator(s.evaluator_id)
        if fc in ev.coverage:
            continue
        if fc in ev.uncertain:
            censored = True
            continue
        return INVALID
    return CENSORED if censored else VALID


def m_authority(ep: Episode, visible: frozenset[str]) -> str:
    c = ep.contract
    if c.authority_ceiling < 0:
        return CENSORED
    return INVALID if c.requested_authority_level > c.authority_ceiling else VALID


def m_preservation(ep: Episode, visible: frozenset[str]) -> str:
    """M side: preservation through
    `orion_v2.correspondence.assess_correspondence_chain`."""
    rep = ep.representation
    if rep is None:
        return NOT_APPLICABLE
    links = tuple(
        CorrespondenceLink(
            link_id=lid,
            source_epoch=rep.source_epoch if i == 0 else f"{rep.source_epoch}-{i}",
            target_epoch=(
                f"{rep.source_epoch}-{i + 1}" if i + 1 < len(rep.link_ids) else rep.target_epoch
            ),
            mapping_ids=rep.mapping_ids,
            anchor_ids=rep.anchor_ids,
            preserved_invariant_ids=rep.preserved_invariant_ids,
            uncertainty_upper_bound=rep.uncertainty,
            violated_invariant_ids=rep.violated_invariant_ids,
            unresolved_invariant_ids=rep.unresolved_invariant_ids,
            exact=rep.exact,
        )
        for i, lid in enumerate(rep.link_ids)
    )
    assessment = assess_correspondence_chain(
        links,
        context_id=ep.claim.context_id,
        required_invariant_ids=rep.required_invariant_ids,
        tolerance=rep.tolerance,
    )
    if assessment.status is CorrespondenceStatus.NONCOMPARABLE:
        return INVALID
    if assessment.status is CorrespondenceStatus.CANNOT_CHECK:
        return CENSORED
    if assessment.status is CorrespondenceStatus.PARTIALLY_COMPARABLE:
        return INVALID
    return VALID


def b5_preservation(ep: Episode, visible: frozenset[str]) -> str:
    """B5 side: the same question through
    `orion_v2.comparability.ComparabilityCertificate` — a different ORION
    engine with its own status lattice."""
    rep = ep.representation
    if rep is None:
        return NOT_APPLICABLE
    required = set(rep.required_invariant_ids)
    preserved = set(rep.preserved_invariant_ids)
    violated = required & set(rep.violated_invariant_ids)
    unresolved = (required & set(rep.unresolved_invariant_ids)) | (
        required - preserved - set(rep.violated_invariant_ids) - set(rep.unresolved_invariant_ids)
    )
    cert = ComparabilityCertificate(
        certificate_id="cert0",
        old_epoch=rep.source_epoch,
        new_epoch=rep.target_epoch,
        target_context_id=ep.claim.context_id,
        mapping_ids=rep.mapping_ids,
        anchors=(Anchor("anchor0", "old", "new", tuple(sorted(preserved)) or ("inv_none",)),),
        required_invariant_ids=tuple(sorted(required)),
        violated_invariant_ids=tuple(sorted(violated)),
        unresolved_invariant_ids=tuple(sorted(unresolved)),
        accumulated_uncertainty=rep.uncertainty,
        tolerance=rep.tolerance,
    )
    status = cert.status
    if status is ComparabilityStatus.NONCOMPARABLE:
        return INVALID
    if status is ComparabilityStatus.CANNOT_CHECK:
        return CENSORED
    if status is ComparabilityStatus.PARTIALLY_COMPARABLE:
        return INVALID
    return VALID


MODULE_CHECK_M = {
    "C_SPEC_BINDING": m_spec_binding,
    "C_SOURCE_STATUS": m_source_status,
    "C_DEPENDENCE": m_dependence,
    "C_ARTIFACT_DIGEST": m_artifact_digest,
    "C_ENV_IDENTITY": m_env_identity,
    "C_CALIBRATION": m_calibration,
    "C_TRANSPORT": m_transport,
    "C_ROUTE_COMPLETENESS": m_route_completeness,
    "C_EVALUATOR_COVERAGE": m_evaluator_coverage,
    "C_AUTHORITY": m_authority,
    "C_PRESERVATION": m_preservation,
}

MODULE_CHECK_B5 = dict(
    MODULE_CHECK_M,
    C_SOURCE_STATUS=b5_source_status,
    C_DEPENDENCE=b5_dependence,
    C_ENV_IDENTITY=b5_env_identity,
    C_PRESERVATION=b5_preservation,
)

# the four checks whose two sides are genuinely different code
DISTINCT_IMPLEMENTATIONS = (
    "C_SOURCE_STATUS", "C_DEPENDENCE", "C_ENV_IDENTITY", "C_PRESERVATION",
)

TABLES = {"M": MODULE_CHECK_M, "B5": MODULE_CHECK_B5}
assert set(MODULE_CHECK_M) == set(MODULE_CHECK_B5) == set(CHECKS)


# ---- export accounting (structural audit cost) --------------------------------

def export_units(ep: Episode, fields: frozenset[str], visible: frozenset[str], *, with_trace: bool) -> int:
    total = 0
    if F_RESULT in fields:
        total += 1
    if F_PROVENANCE in fields:
        total += len(visible)
    if F_PROBLEM_BINDING in fields:
        total += 1 + len(ep.contract.scope)
    if F_ARTIFACT in fields:
        total += 2
    if F_ASSUMPTION_VERSION in fields:
        total += 2
    if F_MEASUREMENT_CALIBRATION in fields:
        total += len({s.calibration_id for s in ep.supports if s.calibration_id})
    if F_TRANSPORT_RELATION in fields:
        total += 1 + sum(1 for s in ep.supports if s.context_id != ep.claim.context_id)
    if F_DEPENDENCE in fields:
        total += len(ep.supports) + sum(
            len([p for p in n.parents if p in visible]) for n in ep.nodes if n.node_id in visible
        )
    if F_EVALUATOR_CONTRACT in fields:
        total += len({s.evaluator_id for s in ep.supports}) + len(ep.contract.decision_relevant_classes)
    if F_PRESERVATION in fields:
        rep = ep.representation
        total += 0 if rep is None else len(rep.link_ids) + len(rep.required_invariant_ids)
    if F_ROUTE_LEDGER in fields:
        total += sum(1 for r in ep.routes if r.registered)
    if F_AUTHORITY_CEILING in fields:
        total += 2
    if with_trace:
        total += len(ep.internal_steps)
    return total


# ---- arm specification --------------------------------------------------------

@dataclass(frozen=True)
class ArmOutput:
    verdict: str
    detected_class: str | None
    checks_run: int
    export_units: int
    check_statuses: dict[str, str] | None = None


@dataclass(frozen=True)
class ArmSpec:
    name: str
    kind: str                       # SURFACE | PARENT | CONTROL
    fields: frozenset[str] = frozenset()
    full_registry: bool = True
    with_trace: bool = False
    native: Callable[[Episode, frozenset[str]], ArmOutput] | None = None
    table: str = "M"
    note: str = ""


def _runnable(fields: frozenset[str]) -> tuple[str, ...]:
    return tuple(c for c in CHECKS if set(REQUIRED_FIELDS[c]) <= fields)


def frozen_rule(ep: Episode, spec: ArmSpec) -> ArmOutput:
    visible = visible_nodes(ep, full_registry=spec.full_registry)
    runnable = _runnable(spec.fields)
    table = TABLES[spec.table]
    statuses = {c: table[c](ep, visible) for c in runnable}
    fired = [c for c in runnable if statuses[c] == INVALID]
    censored = [c for c in runnable if statuses[c] == CENSORED]
    units = export_units(ep, spec.fields, visible, with_trace=spec.with_trace)
    if fired:
        return ArmOutput(REJECT, CLASS_FOR_CHECK[fired[0]], len(runnable), units, dict(statuses))
    if F_EVALUATOR_CONTRACT in spec.fields:
        unchecked = [
            cls
            for cls in ep.contract.decision_relevant_classes
            if CHECK_FOR_CLASS[cls] not in runnable
        ]
    else:
        unchecked = []
    if censored or unchecked:
        return ArmOutput(CANNOT_CHECK, None, len(runnable), units, dict(statuses))
    return ArmOutput(ACCEPT, None, len(runnable), units, dict(statuses))


# ---- native single-parent arms ------------------------------------------------

def native_proof_certificate(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    """A proof/certificate checker alone: it establishes that the derivation is
    sound for the *stated* statement.  It has no access to the intended
    question, so a wrong formalization passes (master §11 rule 10)."""
    status = m_artifact_digest(ep, visible)
    units = export_units(ep, frozenset({F_RESULT, F_ARTIFACT}), visible, with_trace=False)
    if status == INVALID:
        return ArmOutput(REJECT, "CODE_OR_PROOF_MISMATCH", 1, units)
    return ArmOutput(ACCEPT, None, 1, units)


def native_provenance_only(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    """Two-valued provenance invalidation: a disputed ancestor is treated as a
    revoked one, so this parent over-rejects on censored episodes."""
    roots = _support_roots(ep, visible)
    parents = _node_parents(ep, visible, include_suspected=True)
    bad = {
        n.node_id
        for n in ep.nodes
        if n.node_id in visible and n.status in (NODE_RETRACTED, NODE_SUPERSEDED, NODE_DISPUTED)
    }
    units = export_units(ep, frozenset({F_RESULT, F_PROVENANCE}), visible, with_trace=False)
    if LINEAGE.revoked_supports(roots, parents, bad):
        return ArmOutput(REJECT, "STALE_OR_WRONG_SOURCE", 1, units)
    return ArmOutput(ACCEPT, None, 1, units)


def native_replay(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    status = b5_env_identity(ep, visible)
    units = export_units(
        ep, frozenset({F_RESULT, F_ARTIFACT, F_ASSUMPTION_VERSION}), visible, with_trace=False
    )
    if status == INVALID:
        return ArmOutput(REJECT, "SEED_OR_VERSION_MISMATCH", 1, units)
    if status == CENSORED:
        return ArmOutput(CANNOT_CHECK, None, 1, units)
    return ArmOutput(ACCEPT, None, 1, units)


def native_assurance(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    """GSN change impact, two-valued and conjunctive: any challenged solution
    makes the top goal suspect, with no notion of censoring."""
    edges = [("G0", s.support_id) for s in ep.supports]
    roots = _support_roots(ep, visible)
    parents = _node_parents(ep, visible, include_suspected=True)
    bad = {
        n.node_id
        for n in ep.nodes
        if n.node_id in visible and n.status in (NODE_RETRACTED, NODE_SUPERSEDED, NODE_DISPUTED)
    }
    challenged = set(LINEAGE.revoked_supports(roots, parents, bad))
    for s in ep.supports:
        if s.calibration_id and ep.calibration_status(s.calibration_id) in (CAL_INVALID, CAL_UNDER_REVIEW):
            challenged.add(s.support_id)
    units = export_units(
        ep,
        frozenset({F_RESULT, F_PROVENANCE, F_MEASUREMENT_CALIBRATION}),
        visible,
        with_trace=False,
    )
    if ASSURANCE.suspect_top_goal(edges, challenged, "G0"):
        return ArmOutput(REJECT, "STALE_OR_WRONG_SOURCE", 2, units)
    return ArmOutput(ACCEPT, None, 2, units)


def native_dependence(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    """Dependence audit alone, conservative: suspected ancestry counts against
    independence, so this parent over-rejects censored dependence."""
    ids = tuple(sorted(s.support_id for s in ep.supports))
    units = export_units(ep, frozenset({F_RESULT, F_DEPENDENCE}), visible, with_trace=False)
    if ep.independence_k <= 1 or len(ids) < ep.independence_k:
        return ArmOutput(ACCEPT, None, 1, units)
    n = DEPENDENCE.independent_components(
        ids, _shared_pairs(ep, visible, include_suspected=True), include_suspected=False
    )
    if n < ep.independence_k:
        return ArmOutput(REJECT, "HIDDEN_DEPENDENCE", 1, units)
    return ArmOutput(ACCEPT, None, 1, units)


def native_abstention(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    """Calibrated selective prediction with no failure-class semantics: the
    score is the fraction of supports with no visibly flagged ancestor."""
    roots = _support_roots(ep, visible)
    parents = _node_parents(ep, visible, include_suspected=True)
    flagged = {
        n.node_id
        for n in ep.nodes
        if n.node_id in visible and n.status != "VALID"
    }
    hit = LINEAGE.revoked_supports(roots, parents, flagged)
    score = 1.0 - (len(hit) / max(1, len(ep.supports)))
    units = export_units(ep, frozenset({F_RESULT, F_PROVENANCE}), visible, with_trace=False)
    decision = ABSTAIN.decide(score)
    return ArmOutput(
        decision, "STALE_OR_WRONG_SOURCE" if decision == REJECT else None, 1, units
    )


# ---- controls -----------------------------------------------------------------

def control_always_accept(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    return ArmOutput(ACCEPT, None, 0, 1)


def control_always_cannot_check(ep: Episode, visible: frozenset[str]) -> ArmOutput:
    return ArmOutput(CANNOT_CHECK, None, 0, 1)


# ---- registered arm table -----------------------------------------------------

S0 = frozenset({F_RESULT})
S1 = frozenset({F_RESULT, F_PROVENANCE})
S2 = frozenset({F_RESULT, F_ARTIFACT, F_ROUTE_LEDGER})
S3 = frozenset({F_RESULT, F_ARTIFACT, F_ASSUMPTION_VERSION})

LADDER_RUNGS: tuple[tuple[str, frozenset[str]], ...] = (
    ("L1_OUTPUT_ONLY", S0),
    ("L2_PLUS_PROVENANCE", S0 | {F_PROVENANCE}),
    ("L3_PLUS_PROBLEM_ARTIFACT", S0 | {F_PROVENANCE, F_PROBLEM_BINDING, F_ARTIFACT}),
    (
        "L4_PLUS_VERSION_CALIBRATION_TRANSPORT",
        S0 | {F_PROVENANCE, F_PROBLEM_BINDING, F_ARTIFACT, F_ASSUMPTION_VERSION,
              F_MEASUREMENT_CALIBRATION, F_TRANSPORT_RELATION},
    ),
    (
        "L5_PLUS_DEPENDENCE_ROUTE_AUTHORITY_PRESERVATION",
        ALL_FIELDS - {F_EVALUATOR_CONTRACT},
    ),
    ("L6_FULL_WITNESS", ALL_FIELDS),
)

M_ARM = "M_CLAIM_SUFFICIENT_WITNESS"
B5_ARM = "B5_STRONGEST_FAITHFUL_AUDIT_PARENT"

ABLATION_FIELDS: tuple[tuple[str, str], ...] = (
    ("M_MINUS_PROVENANCE", F_PROVENANCE),
    ("M_MINUS_PROBLEM_BINDING", F_PROBLEM_BINDING),
    ("M_MINUS_DEPENDENCE", F_DEPENDENCE),
    ("M_MINUS_ARTIFACT", F_ARTIFACT),
    ("M_MINUS_ASSUMPTION_VERSION", F_ASSUMPTION_VERSION),
    ("M_MINUS_CALIBRATION", F_MEASUREMENT_CALIBRATION),
    ("M_MINUS_TRANSPORT", F_TRANSPORT_RELATION),
    ("M_MINUS_ROUTE_LEDGER", F_ROUTE_LEDGER),
    ("M_MINUS_EVALUATOR_CONTRACT", F_EVALUATOR_CONTRACT),
    ("M_MINUS_AUTHORITY_CEILING", F_AUTHORITY_CEILING),
    ("M_MINUS_PRESERVATION", F_PRESERVATION),
)

ABLATION_FOR_CLASS = {
    cls: name
    for name, fld in ABLATION_FIELDS
    for cls, f2 in __import__("mex7_model").FIELD_FOR_CLASS.items()
    if f2 == fld
}


def arm_specs() -> list[ArmSpec]:
    specs: list[ArmSpec] = [
        ArmSpec("S0_OPAQUE_OUTPUT_ONLY", "SURFACE", S0, note="protocol §3 opaque output only"),
        ArmSpec("S1_PROVENANCE_PLUS_OUTPUT", "SURFACE", S1, note="protocol §3 provenance + output"),
        ArmSpec(
            "S2_FULL_HUMAN_STYLE_TRACE",
            "SURFACE",
            S2,
            with_trace=True,
            note="the machine's own step record: what it executed and what it attempted, "
                 "and nothing about external registry state",
        ),
        ArmSpec(
            "S3_PROOF_OR_CERTIFICATE_PARENT",
            "SURFACE",
            S3,
            note="domain-native proof/replay bundle: statement, derivation, pinned versions",
        ),
    ]
    for name, fields in LADDER_RUNGS:
        specs.append(ArmSpec(name, "SURFACE", fields, note="H-EXT-3 nested ladder rung"))
    specs.append(
        ArmSpec(
            M_ARM,
            "SURFACE",
            ALL_FIELDS,
            full_registry=True,
            note="claim-sufficient structured witness, identity-exporting (protocol §2)",
        )
    )
    specs.append(
        ArmSpec(
            "M_MINUS_REGISTRY_RESOLUTION",
            "SURFACE",
            ALL_FIELDS,
            full_registry=False,
            note="the same witness fields carried as self-contained values",
        )
    )
    for name, fld in ABLATION_FIELDS:
        specs.append(ArmSpec(name, "SURFACE", ALL_FIELDS - {fld}, note=f"omission of {fld}"))
    specs.append(
        ArmSpec(
            B5_ARM,
            "SURFACE",
            ALL_FIELDS,
            full_registry=True,
            table="B5",
            note="strongest faithful audit parent federation at full registry information, "
                 "adjudicated through the parents' own engines (MODULE_CHECK_B5)",
        )
    )
    specs += [
        ArmSpec("A0_PROOF_CERTIFICATE_ONLY", "PARENT", native=native_proof_certificate),
        ArmSpec("A1_PROVENANCE_ONLY", "PARENT", native=native_provenance_only),
        ArmSpec("A2_REPLAY_ONLY", "PARENT", native=native_replay),
        ArmSpec("A3_ASSURANCE_CASE", "PARENT", native=native_assurance),
        ArmSpec("A4_DEPENDENCE_AUDIT", "PARENT", native=native_dependence),
        ArmSpec("A5_CALIBRATED_ABSTENTION", "PARENT", native=native_abstention),
        ArmSpec("C_ALWAYS_ACCEPT", "CONTROL", native=control_always_accept),
        ArmSpec("C_ALWAYS_CANNOT_CHECK", "CONTROL", native=control_always_cannot_check),
        ArmSpec("C_RANDOM_VERDICT", "CONTROL"),
    ]
    return specs


def run_arm(spec: ArmSpec, ep: Episode, rng=None) -> ArmOutput:
    if spec.name == "C_RANDOM_VERDICT":
        assert rng is not None
        verdict = rng.choice((ACCEPT, REJECT, CANNOT_CHECK))
        cls = rng.choice(list(CLASS_FOR_CHECK.values())) if verdict == REJECT else None
        return ArmOutput(verdict, cls, 0, 1)
    if spec.native is not None:
        return spec.native(ep, visible_nodes(ep, full_registry=spec.full_registry))
    return frozen_rule(ep, spec)
