"""ME-X7 V2 — the exact audit oracle and the frozen adjudication rule.

Two computations decide every audit verdict and must agree on every instance
(gate G0b): the direct rule `adjudicate` and the independent
`adjudicate_exhaustive`, which enumerates every resolution of the censored
checks.  The oracle verdict is `adjudicate` at full field visibility and full
registry visibility; the planter's declared defect class is cross-checked
against it (exactly the planted check INVALID, and for the censored stratum
exactly the censored set the drawn variant declares).

Two registered corrections separate this module from ME-X7 V1, both forced by
the V1 protected run's hard-gate failure (`ME_X7_OUTCOME_RECEIPT.md` §2, §7,
repair 3).  Neither is a tuning change and neither may be applied alone:

  **Correction 1 — the check table gains a censored state for
  `C_ARTIFACT_DIGEST`.**  In `MODE_COMPUTATIONAL` the second half of that check
  — whether the checker accepts — can only be decided by re-executing the
  artifact, which needs the environment that ran.  V1's table gave the check no
  censored state, so the registered `CENSOR_ENV` condition (environment not
  recoverable) was misread as a proof/code mismatch by the arms and as a clean
  VALID by the oracle.  The declared/actual digest comparison is unaffected and
  stays decidable: an unrecoverable environment with mismatched digests is
  still INVALID.

  **Correction 2 — `planter_agrees` drops its "exactly one censored check"
  count invariant** for a declared per-variant, per-mode expected-censored set
  (`EXPECTED_CENSORED_CHECKS`).  The count invariant was false for a variant
  whose erased field more than one check depends on; keeping it while applying
  correction 1 would have made the generator re-draw every computational
  `CENSOR_ENV` episode, deleting the six instances that exposed the defect.

No arm imports this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product

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
    NOT_APPLICABLE,
    REJECT,
    RELATION_CANNOT_CHECK,
    RELATION_RANK,
    REQUIRED_FIELDS,
    CAL_INVALID,
    CAL_UNDER_REVIEW,
    Episode,
    F_EVALUATOR_CONTRACT,
    MODE_COMPUTATIONAL,
    MODE_FORMAL,
    NODE_DISPUTED,
    NODE_RETRACTED,
    NODE_SUPERSEDED,
    VALID,
)

ALL_FIELDS = frozenset(FIELDS)


# ---- ancestry with a suspected-edge switch -----------------------------------

def ancestry(
    ep: Episode,
    root: str,
    *,
    visible: frozenset[str],
    include_suspected: bool,
) -> set[str]:
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


def support_ancestries(
    ep: Episode, *, visible: frozenset[str], include_suspected: bool
) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for s in ep.supports:
        acc: set[str] = set()
        for root in s.root_node_ids:
            acc |= ancestry(ep, root, visible=visible, include_suspected=include_suspected)
        out[s.support_id] = acc
    return out


def _components(ancestries: dict[str, set[str]]) -> int:
    ids = sorted(ancestries)
    parent = {i: i for i in ids}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if ancestries[a] & ancestries[b]:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    return len({find(i) for i in ids})


# ---- the eleven checks -------------------------------------------------------

def check_spec_binding(ep: Episode, visible: frozenset[str]) -> str:
    if not ep.contract.intended_question_digest:
        return CENSORED
    return VALID if ep.claim.formalization_digest == ep.contract.intended_question_digest else INVALID


def check_source_status(ep: Episode, visible: frozenset[str]) -> str:
    anc = support_ancestries(ep, visible=visible, include_suspected=True)
    reached = set().union(*anc.values()) if anc else set()
    statuses = {ep.node(n).status for n in reached}
    if statuses & {NODE_RETRACTED, NODE_SUPERSEDED}:
        return INVALID
    if NODE_DISPUTED in statuses:
        return CENSORED
    return VALID


def check_dependence(ep: Episode, visible: frozenset[str]) -> str:
    k = ep.independence_k
    if k <= 1 or len(ep.supports) < k:
        return NOT_APPLICABLE
    confirmed = _components(support_ancestries(ep, visible=visible, include_suspected=False))
    if confirmed < k:
        return INVALID
    with_suspected = _components(support_ancestries(ep, visible=visible, include_suspected=True))
    if with_suspected < k:
        return CENSORED
    return VALID


def check_artifact_digest(ep: Episode, visible: frozenset[str]) -> str:
    a = ep.artifact
    if a is None:
        return NOT_APPLICABLE
    # The declared/actual digest comparison needs no environment, so it decides
    # first and an unrecoverable environment never suppresses a real mismatch.
    if a.declared_digest != a.actual_digest:
        return INVALID
    # V2 correction 1: what remains — whether the checker accepts — is decided
    # in MODE_COMPUTATIONAL by re-executing the artifact, so an unrecoverable
    # environment makes it undecidable rather than mismatched.  MODE_FORMAL is
    # untouched: that branch runs the resolution checker over the payload and
    # never consults the environment or the seed.
    if ep.mode == MODE_COMPUTATIONAL and (not a.actual_env or not a.actual_seed):
        return CENSORED
    if not a.checker_accepts:
        return INVALID
    return VALID


def check_env_identity(ep: Episode, visible: frozenset[str]) -> str:
    a = ep.artifact
    if a is None or not ep.contract.replay_required:
        return NOT_APPLICABLE
    if not a.actual_env or not a.actual_seed:
        return CENSORED
    if a.recorded_env != a.actual_env or a.recorded_seed != a.actual_seed:
        return INVALID
    return VALID


def check_calibration(ep: Episode, visible: frozenset[str]) -> str:
    ids = [s.calibration_id for s in ep.supports if s.calibration_id]
    if not ids:
        return NOT_APPLICABLE
    statuses = {ep.calibration_status(cid) for cid in ids}
    if CAL_INVALID in statuses:
        return INVALID
    if CAL_UNDER_REVIEW in statuses:
        return CENSORED
    return VALID


def check_transport(ep: Episode, visible: frozenset[str]) -> str:
    transported = [s for s in ep.supports if s.context_id != ep.claim.context_id]
    if not transported:
        return NOT_APPLICABLE
    required = RELATION_RANK[ep.required_relation]
    censored = False
    for s in transported:
        rel = ep.relation(s.context_id, ep.claim.context_id)
        if rel is None:
            return INVALID
        if rel == RELATION_CANNOT_CHECK:
            censored = True
            continue
        if RELATION_RANK[rel] < required:
            return INVALID
    return CENSORED if censored else VALID


def check_route_completeness(ep: Episode, visible: frozenset[str]) -> str:
    a = ep.artifact
    if a is None:
        return NOT_APPLICABLE
    if a.attempted_route_count < 0:
        return CENSORED
    declared = sum(1 for r in ep.routes if r.registered)
    return INVALID if declared < a.attempted_route_count else VALID


def check_evaluator_coverage(ep: Episode, visible: frozenset[str]) -> str:
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


def check_authority(ep: Episode, visible: frozenset[str]) -> str:
    c = ep.contract
    if c.authority_ceiling < 0:
        return CENSORED
    return INVALID if c.requested_authority_level > c.authority_ceiling else VALID


def check_preservation(ep: Episode, visible: frozenset[str]) -> str:
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


CHECK_FN = {
    "C_SPEC_BINDING": check_spec_binding,
    "C_SOURCE_STATUS": check_source_status,
    "C_DEPENDENCE": check_dependence,
    "C_ARTIFACT_DIGEST": check_artifact_digest,
    "C_ENV_IDENTITY": check_env_identity,
    "C_CALIBRATION": check_calibration,
    "C_TRANSPORT": check_transport,
    "C_ROUTE_COMPLETENESS": check_route_completeness,
    "C_EVALUATOR_COVERAGE": check_evaluator_coverage,
    "C_AUTHORITY": check_authority,
    "C_PRESERVATION": check_preservation,
}
assert set(CHECK_FN) == set(CHECKS)


def run_checks(ep: Episode, *, visible: frozenset[str]) -> dict[str, str]:
    return {name: CHECK_FN[name](ep, visible) for name in CHECKS}


# ---- the frozen adjudication rule (identical for every arm) -------------------

@dataclass(frozen=True)
class Adjudication:
    verdict: str
    detected_class: str | None
    runnable: tuple[str, ...]
    fired: tuple[str, ...]
    censored: tuple[str, ...]
    unchecked_required_classes: tuple[str, ...]


def _runnable(fields: frozenset[str]) -> tuple[str, ...]:
    return tuple(c for c in CHECKS if set(REQUIRED_FIELDS[c]) <= fields)


def adjudicate(
    statuses: dict[str, str], fields: frozenset[str], ep: Episode
) -> Adjudication:
    runnable = _runnable(fields)
    fired = tuple(c for c in runnable if statuses[c] == INVALID)
    censored = tuple(c for c in runnable if statuses[c] == CENSORED)
    if F_EVALUATOR_CONTRACT in fields:
        unchecked = tuple(
            cls
            for cls in ep.contract.decision_relevant_classes
            if CHECK_FOR_CLASS[cls] not in runnable
        )
    else:
        unchecked = ()
    if fired:
        return Adjudication(REJECT, CLASS_FOR_CHECK[fired[0]], runnable, fired, censored, unchecked)
    if censored or unchecked:
        return Adjudication(CANNOT_CHECK, None, runnable, fired, censored, unchecked)
    return Adjudication(ACCEPT, None, runnable, fired, censored, unchecked)


def adjudicate_exhaustive(
    statuses: dict[str, str], fields: frozenset[str], ep: Episode
) -> str:
    """Independent recomputation: enumerate every resolution of the censored
    runnable checks.  A verdict is definite only when every resolution agrees;
    an unchecked decision-relevant class makes ACCEPT unreachable."""
    runnable = _runnable(fields)
    censored = [c for c in runnable if statuses[c] == CENSORED]
    if F_EVALUATOR_CONTRACT in fields:
        unchecked = [
            cls
            for cls in ep.contract.decision_relevant_classes
            if CHECK_FOR_CLASS[cls] not in runnable
        ]
    else:
        unchecked = []
    outcomes: set[str] = set()
    for assignment in product((VALID, INVALID), repeat=len(censored)):
        resolved = dict(statuses)
        for name, value in zip(censored, assignment):
            resolved[name] = value
        fired = [c for c in runnable if resolved[c] == INVALID]
        if fired:
            outcomes.add(REJECT)
        elif unchecked:
            outcomes.add(CANNOT_CHECK)
        else:
            outcomes.add(ACCEPT)
    if outcomes == {REJECT}:
        return REJECT
    if outcomes == {ACCEPT}:
        return ACCEPT
    return CANNOT_CHECK


# ---- the oracle --------------------------------------------------------------

@dataclass(frozen=True)
class Expected:
    verdict: str
    defect_class: str | None
    statuses: tuple[tuple[str, str], ...]
    exhaustive_agrees: bool
    invalid_checks: tuple[str, ...]
    censored_checks: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "verdict": self.verdict,
            "defect_class": self.defect_class,
            "statuses": {k: v for k, v in self.statuses},
            "exhaustive_agrees": self.exhaustive_agrees,
            "invalid_checks": list(self.invalid_checks),
            "censored_checks": list(self.censored_checks),
        }


def oracle(ep: Episode) -> Expected:
    visible = frozenset(ep.node_ids())
    statuses = run_checks(ep, visible=visible)
    adj = adjudicate(statuses, ALL_FIELDS, ep)
    exhaustive = adjudicate_exhaustive(statuses, ALL_FIELDS, ep)
    return Expected(
        verdict=adj.verdict,
        defect_class=adj.detected_class,
        statuses=tuple(sorted(statuses.items())),
        exhaustive_agrees=exhaustive == adj.verdict,
        invalid_checks=adj.fired,
        censored_checks=adj.censored,
    )


# ---- V2 correction 2: the declared per-variant, per-mode censored set --------

# One registered censoring variant per check, plus the one variant whose erased
# field two checks depend on.  The table is total over the drawable
# (variant, mode) pairs — `MODE_FORMAL` cannot draw `CENSOR_CALIBRATION`, which
# has no meaning where no measurement calibration exists — and an unregistered
# pair raises rather than falling back to a permissive default, so a censoring
# variant added later cannot enter a split unchecked.
_ONE_CHECK_PER_VARIANT = {
    "CENSOR_SPEC": "C_SPEC_BINDING",
    "CENSOR_SOURCE": "C_SOURCE_STATUS",
    "CENSOR_DEPENDENCE": "C_DEPENDENCE",
    "CENSOR_ENV": "C_ENV_IDENTITY",
    "CENSOR_CALIBRATION": "C_CALIBRATION",
    "CENSOR_TRANSPORT": "C_TRANSPORT",
    "CENSOR_ROUTE": "C_ROUTE_COMPLETENESS",
    "CENSOR_EVALUATOR": "C_EVALUATOR_COVERAGE",
    "CENSOR_AUTHORITY": "C_AUTHORITY",
    "CENSOR_PRESERVATION": "C_PRESERVATION",
}

EXPECTED_CENSORED_CHECKS: dict[tuple[str, str], frozenset[str]] = {
    (variant, mode): frozenset({check})
    for variant, check in _ONE_CHECK_PER_VARIANT.items()
    for mode in (MODE_FORMAL, MODE_COMPUTATIONAL)
    if not (variant == "CENSOR_CALIBRATION" and mode == MODE_FORMAL)
}
# The only entry that is not a single check, and the reason correction 2 exists:
# erasing the environment makes the environment identity undecidable *and* the
# artifact re-execution that needs it (correction 1).
EXPECTED_CENSORED_CHECKS[("CENSOR_ENV", MODE_COMPUTATIONAL)] = frozenset(
    {"C_ENV_IDENTITY", "C_ARTIFACT_DIGEST"}
)
assert set(_ONE_CHECK_PER_VARIANT.values()) <= set(CHECKS)
assert all(set(v) <= set(CHECKS) for v in EXPECTED_CENSORED_CHECKS.values())


def expected_censored_checks(variant: str, mode: str) -> frozenset[str]:
    """The censored set a censoring variant is declared to produce in a mode.
    An unregistered pair is an error, never a permissive default."""
    try:
        return EXPECTED_CENSORED_CHECKS[(variant, mode)]
    except KeyError:
        raise ValueError(
            f"no declared expected-censored set for ({variant}, {mode})"
        ) from None


def planter_agrees(
    ep: Episode, stratum: str, *, censor_variant: str | None = None
) -> tuple[bool, str]:
    """Independent cross-check of the planter's declared stratum against a
    full-structure recomputation: exactly the planted class INVALID, nothing
    else INVALID; the control strata have their own signatures.

    For `CENSORED_UNDECIDABLE` the drawn variant is required and its censored
    set must equal the set `EXPECTED_CENSORED_CHECKS` declares for that
    (variant, mode) pair — V2 correction 2, replacing V1's count invariant.
    """
    exp = oracle(ep)
    if stratum == "NO_DEFECT_WARRANTED":
        if exp.verdict != ACCEPT:
            return False, f"expected ACCEPT, got {exp.verdict} ({exp.invalid_checks}{exp.censored_checks})"
        return True, ""
    if stratum == "CENSORED_UNDECIDABLE":
        if censor_variant is None:
            raise ValueError(
                "the censored stratum requires the drawn censoring variant: its "
                "expected censored set is declared per variant and per mode"
            )
        want = expected_censored_checks(censor_variant, ep.mode)
        if exp.verdict != CANNOT_CHECK:
            return False, f"expected CANNOT_CHECK, got {exp.verdict}"
        if exp.invalid_checks:
            return False, f"censored stratum must have no INVALID check, got {exp.invalid_checks}"
        got = frozenset(exp.censored_checks)
        if got != want:
            return False, (
                f"{censor_variant}/{ep.mode} declares censored set {sorted(want)}, "
                f"got {sorted(got)}"
            )
        return True, ""
    want = CHECK_FOR_CLASS[stratum]
    if exp.verdict != REJECT:
        return False, f"expected REJECT for {stratum}, got {exp.verdict}"
    if tuple(exp.invalid_checks) != (want,):
        return False, f"expected exactly {want} INVALID, got {exp.invalid_checks}"
    if exp.defect_class != stratum:
        return False, f"class mismatch {exp.defect_class} != {stratum}"
    if exp.censored_checks:
        return False, f"a planted defect must not co-occur with censoring, got {exp.censored_checks}"
    return True, ""
