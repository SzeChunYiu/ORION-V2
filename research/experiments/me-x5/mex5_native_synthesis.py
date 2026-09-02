#!/usr/bin/env python3
"""ME-X5 native mode 3: SYNTHESIS / evidence synthesis and recommendation revision.

Native objects: a registered PICO question (population, intervention, comparator,
outcome) with a decision threshold; primary studies with effect estimates and
standard errors; risk-of-bias assessment plus outcome ascertainment (does the
measured outcome reveal the asserted harm, or only a surrogate?); the population
a study recruited; a cohort identifier shared by overlapping reports; a network
consistency witness for indirect comparisons.

Native rules that differ materially from the other two modes:

* **identity is over intervention, comparator and outcome only.** A study in a
  different *population* is not answering a different question — it raises a
  transportability question. Deduction has no such slot; physics puts the
  analogous slot (run regime) in transport too, but keeps phase space in identity.
* **dependence deduplicates rather than defeats.** Two reports of the same cohort
  are not two studies; the synthesis keeps the largest and drops the rest. A
  shared cohort therefore changes the pooled estimate and its precision, it does
  not by itself invalidate the body of evidence — unless the declared minimum
  number of independent cohorts is no longer met.
* **scope may be assembled**, as in the measurement mode, from the union of the
  studies' population coverage.
* **the global obstruction is network intransitivity**: A-vs-B and B-vs-C
  comparisons can each be internally consistent while the indirect A-vs-C
  contrast has no registered consistency witness.

The decision is a threshold on the pooled effect: commit only when
`pooled - 2 sigma > threshold`, computed *after* deduplication and after removing
retracted studies. As in the measurement mode this removes Boolean-parent
optimality but not exact-computability optimality (design §10).
"""
from __future__ import annotations

import math

from mex5_model import CENSORED, INVALID, RELATION_RANK, Episode, Family, Unit

MODE = "SYNTHESIS"

NATIVE_VOCABULARY = {
    "target": "registered PICO question with a decision threshold on the pooled effect",
    "unit_kinds": {
        "primary_study": "a randomised or observational primary study",
        "transported_study": "a study conducted in a different population and reused",
        "subgroup_report": "a report covering part of the registered population",
    },
    "validator_kinds": {
        "rob_and_outcome_ascertainment": "risk-of-bias assessment plus the outcome ascertainment method, which determines which harm classes the study can reveal",
    },
    "statuses": {
        "VALID": "included in the synthesis",
        "CENSORED": "under an expression of concern; inclusion currently undecidable",
        "INVALID": "retracted, or excluded at full-text screening",
    },
    "contexts": "populations / care settings",
    "relations": {
        "ISOMORPHIC": "the same population",
        "BEHAVIORALLY_EQUIVALENT": "effect-modifier distributions verified equivalent",
        "PREDICTIVELY_EQUIVALENT": "transportability established for the registered outcome",
        "DECISION_DOMINATES": "the source population bounds the target conservatively",
        "APPROXIMATELY_EQUIVALENT": "populations judged broadly similar without a transport analysis",
        "INCOMPARABLE": "no transportability argument",
        "CANNOT_CHECK": "the effect-modifier distribution was not reported",
    },
    "global_witness": "a registered network consistency (transitivity) check for the indirect comparison",
    "authority": "evidence licenses belief in the effect; issuing a practice recommendation requires a separate registered mandate",
    "failure_classes": ("SERIOUS_HARM", "SELECTION_BIAS", "ATTRITION_BIAS", "SURROGATE_ONLY"),
}

NATIVE_REVIEW = {
    "mode": MODE,
    "native_objects_and_vocabulary": NATIVE_VOCABULARY,
    "strongest_native_methods": [
        "retraction / expression-of-concern screening and provenance tracking",
        "overlapping-cohort detection and deduplication",
        "risk-of-bias and outcome-ascertainment assessment (does the outcome reveal the asserted harm?)",
        "inverse-variance pooling with an explicit certainty rating",
        "transportability assessment against effect modifiers",
        "network consistency (transitivity) checks for indirect comparisons",
    ],
    "valid_and_invalid_transitions": {
        "valid": "revise the recommendation when the pooled effect over deduplicated, non-retracted, transportable studies clears the threshold by two sigma, ascertainment can reveal the asserted harm, and coverage spans the registered population",
        "invalid": "double-count overlapping cohorts; pool a retracted study; transport an effect across populations without an effect-modifier argument; accept a surrogate outcome as evidence about a hard harm; treat an indirect comparison as consistent without a transitivity check",
    },
    "native_failure_classes": list(NATIVE_VOCABULARY["failure_classes"]),
    "evaluator_assumptions": "ascertainment determines what a study can show; a study measuring only a surrogate is silent about the asserted harm regardless of its risk-of-bias rating",
    "lossy_or_invalid_ME_abstractions": [
        "LOSSY: 'dependence' is modelled as defeat, whereas overlapping cohorts are deduplicated and change the pooled estimate",
        "LOSSY: a binary commit/withhold hides the certainty rating a guideline panel actually carries",
        "REDUNDANT: 'apparatus validity' and 'evaluator coverage' are one native artefact (the appraisal) split in two by the abstraction",
        "VALID: the authority boundary matches the native separation of evidence appraisal from recommendation mandate",
    ],
    "strongest_plausible_parent_composition": "retraction/provenance screening + overlap deduplication + risk-of-bias/ascertainment appraisal + inverse-variance pooling + transportability assessment + network consistency, composed by ordinary engineering glue",
    "reviewer": "study author (no independent domain reviewer was available; registered as a limitation in design §10)",
}

RELATION_LABELS = NATIVE_VOCABULARY["relations"]
Z_COMMIT = 2.0


def identity(target, u: Unit) -> str:
    """Signature = (population, intervention, comparator, outcome). Only I, C and O
    carry identity; the population slot is a transportability question."""
    ts, us = tuple(target.signature), tuple(u.signature)
    if us == ts:
        return "EXACT"
    if len(us) == 4 and len(ts) == 4 and us[1:] == ts[1:]:
        return "EXACT"  # different population, same I/C/O: identity holds, transport decides
    if len(us) == 4 and len(ts) == 4 and us[1:3] == ts[1:3] and us[3] != ts[3]:
        return "MISMATCH"  # different outcome: a different question
    return "MISMATCH"


def apparatus_ok(ep: Episode, u: Unit) -> bool:
    if u.validator is None:
        return True
    return ep.validators[u.validator].status not in (INVALID, CENSORED)


def evaluator_covers(ep: Episode, u: Unit) -> bool:
    """Outcome ascertainment: a surrogate-only study cannot reveal the asserted harm."""
    if u.validator is None:
        return True
    v = ep.validators[u.validator]
    return ep.target.asserted_failure_class in v.covers


def _cohort_groups(ep: Episode, uids: list[str]) -> list[list[str]]:
    parent = {x: x for x in uids}

    def find(a: str) -> str:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, a in enumerate(uids):
        anc_a = {x for x, k in ep.units[a].ancestry if k == "CONFIRMED"}
        for b in uids[i + 1:]:
            anc_b = {x for x, k in ep.units[b].ancestry if k == "CONFIRMED"}
            if anc_a & anc_b:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    groups: dict[str, list[str]] = {}
    for x in uids:
        groups.setdefault(find(x), []).append(x)
    return [sorted(v) for _, v in sorted(groups.items())]


def independent_groups(ep: Episode, fam: Family) -> int:
    uids = [x for x in fam.unit_ids if x in ep.units and ep.units[x].status != INVALID and identity(ep.target, ep.units[x]) != "MISMATCH"]
    return len(_cohort_groups(ep, uids)) if uids else 0


def transport_ok(ep: Episode, fam: Family, u: Unit) -> bool:
    if u.context == ep.target.context:
        return True
    rel = ep.relation(u.context, ep.target.context)
    return RELATION_RANK.get(rel, 0) >= RELATION_RANK[fam.required_relation]


def coverage_ok(ep: Episode, fam: Family, coverage: tuple[str, ...]) -> bool:
    have: set[str] = set()
    for uid in fam.unit_ids:
        u = ep.units.get(uid)
        if u is None or u.status == INVALID or identity(ep.target, u) == "MISMATCH":
            continue
        have |= set(u.coverage)
    return set(coverage) <= have


def aggregate(ep: Episode, uids: list[str]):
    """Deduplicate overlapping cohorts (keep the largest report per cohort group),
    then pool inverse-variance on the statistical error."""
    live = [u for u in uids if u in ep.units and ep.units[u].status != INVALID]
    if not live:
        return None
    retained: list[Unit] = []
    for group in _cohort_groups(ep, live):
        best = max((ep.units[x] for x in group), key=lambda u: (u.weight, -u.stat_err, u.estimate))
        retained.append(best)
    weights = []
    for u in retained:
        var = u.stat_err ** 2
        weights.append(1.0 / var if var > 0 else 1.0e6)
    wsum = sum(weights)
    point = sum(w * u.estimate for w, u in zip(weights, retained)) / wsum
    sigma = math.sqrt(1.0 / wsum)
    return (point, sigma)


def commits(ep: Episode, agg) -> bool:
    point, sigma = agg
    return point - Z_COMMIT * sigma > ep.target.threshold


# ---- generator hooks (native surface constants) ---------------------------------
NUMERIC = True
BASE_SIGNATURE = ("pop_A", "drugX", "placebo", "mortality")
UNIT_KIND_MAIN = "primary_study"
UNIT_KIND_SUPPORT = "primary_study"
UNIT_KIND_TRANSPORTED = "transported_study"
UNIT_KIND_CASE = "subgroup_report"
VALIDATOR_KIND = "rob_and_outcome_ascertainment"
FAILURE_CLASSES = NATIVE_VOCABULARY["failure_classes"]
TRANSPORT_REQUIRED = "PREDICTIVELY_EQUIVALENT"
TRANSPORT_BREAKING_RELATION = "APPROXIMATELY_EQUIVALENT"
TRANSPORT_SAFE_RELATION = "BEHAVIORALLY_EQUIVALENT"
EVENT_LABELS = {
    "SET_UNIT_STATUS": "a study is retracted",
    "SET_UNIT_SIGNATURE": "the study is found to report a different outcome",
    "SET_VALIDATOR_STATUS": "the risk-of-bias appraisal is invalidated",
    "SET_VALIDATOR_COVERAGE": "the outcome ascertainment is found to capture only a surrogate",
    "SET_RELATION": "the transportability judgement between populations is retyped",
    "ADD_ANCESTRY": "two reports are found to draw on the same cohort",
    "SET_TARGET_COVERAGE": "the registered population is widened",
    "SET_OPERATING_POINT": "(not native to this mode)",
    "SET_GLOBAL_WITNESS": "the network consistency (transitivity) check is withdrawn",
    "SET_AUTHORITY_GRANT": "the recommendation mandate is withdrawn",
    "ADD_UNIT": "a further study is included",
    "REGISTERED_NO_OP": "a registered change that touches nothing the synthesis depends on",
}


def drift(sig: tuple[str, ...]) -> tuple[str, ...]:
    return (sig[0], sig[1], sig[2], "biomarker")   # a different outcome is a different question


def narrowed_variant(sig: tuple[str, ...]):
    return None   # narrowing in this mode is by restricting the population coverage
