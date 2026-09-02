#!/usr/bin/env python3
"""ME-X5 native mode 1: FORMAL / deductive (mathematics, theorem proving,
formal verification).

Native objects: a registered theorem statement; proof terms and lemmas; a
kernel/checker at a pinned version together with the linters that certify the
absence of a named defect class; the axiom set and the dependency closure of a
proof; the algebraic structure a lemma was proved over; the hypothesis class the
theorem quantifies over; a case-analysis (gluing) witness.

Native rules that differ materially from the other two modes:

* **identity is exact.** A proof term whose statement signature differs from the
  registered theorem — even by a universe level or a binder shape — proves a
  different theorem. There is no "approximately the same theorem"; narrowing is
  available only by *restricting the hypothesis class*, never by accepting a
  weaker statement as the registered one.
* **dependence is strict.** Two proofs sharing *any* confirmed lemma or axiom in
  their dependency closure are one proof for independence purposes. Physics
  tolerates shared systematics with a correlation term; deduction does not.
* **scope must be carried by a single artefact.** A theorem covers exactly its
  own hypotheses. Coverage cannot be assembled from the union of several proofs
  unless a case-analysis witness is registered (that is the global-witness
  condition, not the scope condition).
* **transport of a ported lemma requires isomorphism.** A lemma proved over a
  different structure transports only along an isomorphism when the result is an
  identity-type statement; the family's declared requirement is raised to
  `ISOMORPHIC` for units of kind `ported_lemma`.

Boolean mode: there is no numeric aggregation. An exact planner over the
registered facts is optimal by construction here — declared in design §10.
"""
from __future__ import annotations

from mex5_model import CENSORED, INVALID, RELATION_RANK, Episode, Family, Unit

MODE = "FORMAL"

NATIVE_VOCABULARY = {
    "target": "registered theorem statement",
    "unit_kinds": {
        "proof_term": "a checked proof of the statement",
        "lemma": "a supporting lemma in the dependency closure",
        "ported_lemma": "a lemma proved over another structure and reused here",
        "case_proof": "a proof covering one case of the hypothesis class",
    },
    "validator_kinds": {
        "kernel_and_linters": "the proof kernel at a pinned version plus the linters certifying a named defect class",
    },
    "statuses": {
        "VALID": "checked and accepted by the kernel",
        "CENSORED": "the axiom or lemma is under review (consistency not currently established)",
        "INVALID": "admitted without proof (`sorry`), or the axiom was retracted as inconsistent",
    },
    "contexts": "algebraic structures / type-class instances the lemma was proved over",
    "relations": {
        "ISOMORPHIC": "structures are isomorphic",
        "BEHAVIORALLY_EQUIVALENT": "a structure-preserving embedding exists",
        "PREDICTIVELY_EQUIVALENT": "the relevant predicates agree",
        "DECISION_DOMINATES": "the source decides everything the target needs",
        "APPROXIMATELY_EQUIVALENT": "agreement only up to an unquantified approximation",
        "INCOMPARABLE": "no registered morphism",
        "CANNOT_CHECK": "the morphism has not been checked",
    },
    "global_witness": "a registered case-analysis / gluing lemma tying the case proofs together",
    "authority": "a proof licenses belief in the theorem; deploying the verified artefact requires a separate registered obligation",
    "failure_classes": ("SORRY_IN_CLOSURE", "UNIVERSE_INCONSISTENCY", "AXIOM_RETRACTED", "SPEC_DRIFT"),
}

# Protocol ME-X5 §3 native-domain ownership record.
NATIVE_REVIEW = {
    "mode": MODE,
    "native_objects_and_vocabulary": NATIVE_VOCABULARY,
    "strongest_native_methods": [
        "kernel-level proof checking at a pinned toolchain version",
        "axiom / `sorry` audit over the dependency closure (`#print axioms`)",
        "specification review against the informal mathematical question",
        "type-class / structure instance checking for lemma reuse",
        "library provenance and version pinning",
    ],
    "valid_and_invalid_transitions": {
        "valid": "accept the registered theorem as established when a checked proof of exactly that statement exists, its closure is free of admitted or retracted steps, the checker exposes the asserted defect class, ported lemmas transport along a licensed morphism, and the hypotheses cover the registered scope",
        "invalid": "accept a checked proof of a different statement; accept a closure containing an admitted lemma; accept a case-split without the gluing lemma; treat two proofs sharing a lemma as independent confirmations",
    },
    "native_failure_classes": list(NATIVE_VOCABULARY["failure_classes"]),
    "evaluator_assumptions": "the kernel is trusted at the pinned version; linters certify only the defect classes they implement; nothing outside a linter's coverage is certified by its silence",
    "lossy_or_invalid_ME_abstractions": [
        "LOSSY: 'support family' flattens the distinction between a proof path and its dependency closure — the closure is not a set of alternatives",
        "LOSSY: three-valued censoring reads an unreviewed axiom as UNKNOWN, whereas a formalist would refuse the statement outright",
        "REDUNDANT: 'measurement validity' collapses onto checker validity; there is no instrument here",
        "INVALID IF PUSHED: the numeric aggregation layer has no formal counterpart and is disabled in this mode",
    ],
    "strongest_plausible_parent_composition": "kernel + axiom audit + specification review checklist + instance/transport check + library provenance, composed by ordinary engineering glue",
    "reviewer": "study author (no independent domain reviewer was available; registered as a limitation in design §10)",
}

RELATION_LABELS = NATIVE_VOCABULARY["relations"]


def identity(target, u: Unit) -> str:
    """Exact statement identity. Signature = (statement_id, universe_level, binder_shape)."""
    return "EXACT" if tuple(u.signature) == tuple(target.signature) else "MISMATCH"


def apparatus_ok(ep: Episode, u: Unit) -> bool:
    """Kernel/linter validity. No operating range: a kernel is either the pinned
    validated version or it is not."""
    if u.validator is None:
        return True
    return ep.validators[u.validator].status not in (INVALID, CENSORED)


def evaluator_covers(ep: Episode, u: Unit) -> bool:
    if u.validator is None:
        return True
    v = ep.validators[u.validator]
    return ep.target.asserted_failure_class in v.covers


def independent_groups(ep: Episode, fam: Family) -> int:
    """Strict deductive independence: any shared confirmed lemma or axiom in the
    dependency closure merges two proofs."""
    uids = [x for x in fam.unit_ids if x in ep.units]
    parent = {x: x for x in uids}

    def find(a: str) -> str:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i, a in enumerate(uids):
        anc_a = {x for x, k in ep.units[a].ancestry if k == "CONFIRMED"}
        for b in uids[i + 1:]:
            anc_b = {x for x, k in ep.units[b].ancestry if k == "CONFIRMED"}
            if anc_a & anc_b:
                union(a, b)
    live = [x for x in uids if ep.units[x].status != INVALID and identity(ep.target, ep.units[x]) != "MISMATCH"]
    return len({find(x) for x in live})


def transport_ok(ep: Episode, fam: Family, u: Unit) -> bool:
    if u.context == ep.target.context:
        return True
    required = fam.required_relation
    if u.kind == "ported_lemma":
        required = "ISOMORPHIC"  # identity-type results transport only along isomorphism
    rel = ep.relation(u.context, ep.target.context)
    return RELATION_RANK.get(rel, 0) >= RELATION_RANK[required]


def coverage_ok(ep: Episode, fam: Family, coverage: tuple[str, ...]) -> bool:
    """A theorem covers exactly its own hypotheses: a *single* artefact must
    carry the registered scope. Unions need a gluing witness, handled separately."""
    need = set(coverage)
    for uid in fam.unit_ids:
        u = ep.units.get(uid)
        if u is None or u.status == INVALID or identity(ep.target, u) == "MISMATCH":
            continue
        if need <= set(u.coverage):
            return True
    return False


def aggregate(ep: Episode, uids: list[str]):
    """No numeric layer in a deductive mode."""
    return None


# ---- generator hooks (native surface constants) ---------------------------------
NUMERIC = False
BASE_SIGNATURE = ("thm_main", "u0", "binder_a")
UNIT_KIND_MAIN = "proof_term"
UNIT_KIND_SUPPORT = "lemma"
UNIT_KIND_TRANSPORTED = "ported_lemma"
UNIT_KIND_CASE = "case_proof"
VALIDATOR_KIND = "kernel_and_linters"
FAILURE_CLASSES = NATIVE_VOCABULARY["failure_classes"]
TRANSPORT_REQUIRED = "PREDICTIVELY_EQUIVALENT"
TRANSPORT_BREAKING_RELATION = "BEHAVIORALLY_EQUIVALENT"   # < ISOMORPHIC, so a ported lemma fails
TRANSPORT_SAFE_RELATION = "BEHAVIORALLY_EQUIVALENT"       # >= PREDICTIVELY_EQUIVALENT for a non-ported lemma
EVENT_LABELS = {
    "SET_UNIT_STATUS": "a lemma is admitted without proof or its axiom is retracted",
    "SET_UNIT_SIGNATURE": "the formalised statement is corrected and no longer matches the registered theorem",
    "SET_VALIDATOR_STATUS": "the pinned kernel version is withdrawn",
    "SET_VALIDATOR_COVERAGE": "a linter is found not to check the asserted defect class",
    "SET_RELATION": "the structure morphism between the two settings is retyped",
    "ADD_ANCESTRY": "a shared lemma is discovered in both dependency closures",
    "SET_TARGET_COVERAGE": "the registered hypothesis class is widened",
    "SET_OPERATING_POINT": "(not native to this mode)",
    "SET_GLOBAL_WITNESS": "the case-analysis lemma is withdrawn",
    "SET_AUTHORITY_GRANT": "the deployment obligation is withdrawn",
    "ADD_UNIT": "a further lemma is contributed",
    "REGISTERED_NO_OP": "a registered change that touches nothing the theorem depends on",
}


def drift(sig: tuple[str, ...]) -> tuple[str, ...]:
    return (sig[0], "u1", sig[2])   # a universe-level mismatch: a different theorem


def narrowed_variant(sig: tuple[str, ...]):
    return None   # a weaker statement is a different theorem, never a narrowed one


def commits(ep, agg) -> bool:
    return True
