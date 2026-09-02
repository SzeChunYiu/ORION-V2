#!/usr/bin/env python3
"""ME-X5 native mode 2: MEASUREMENT / experimental-computational physical science.

Native objects: a registered observable and its fiducial phase space; measurement
channels (independent analyses of the same observable); a calibration valid over
a stated operating range; a closure / null test that can expose a named
mis-modelling class; the run regime a calibration or efficiency was derived in;
a systematic-uncertainty source shared between channels; a covariance-aware
global consistency witness.

Native rules that differ materially from the other two modes:

* **identity admits a fiducial restriction.** A channel that measures the target
  observable in a strictly smaller phase space is not measuring something else —
  it measures the fiducial version, and the honest transition is a *narrowed*
  commitment, not a rejection. (Signature = (observable, phase_space).)
* **dependence lives in the error budget.** Two channels are correlated if they
  share a systematic source *or* share a confirmed upstream ancestor (the same
  detector simulation, the same generator tune). Correlated systematics are added
  linearly within a source group and in quadrature across groups; the decision is
  therefore a *real-valued* function of the retained channels, not a Boolean
  formula over defeat atoms.
* **apparatus validity is range-valued.** A calibration is valid only inside the
  operating range it was derived in; moving the operating point can invalidate a
  calibration that nobody touched.
* **scope may be assembled.** The union of the channels' acceptance covers the
  registered phase space; unlike the deductive mode, no single channel need cover
  it alone.

The decision is a threshold on a combined estimate: commit only when
`estimate - 2 sigma > threshold`. This removes Boolean-parent optimality (a truth
maintenance system cannot express the error budget) but not exact-computability
optimality — see the honest limitation in design §10.
"""
from __future__ import annotations

import math

from mex5_model import CENSORED, INVALID, RELATION_RANK, Episode, Family, Unit

MODE = "MEASUREMENT"

NATIVE_VOCABULARY = {
    "target": "registered observable at a stated phase space and decision threshold",
    "unit_kinds": {
        "measurement_channel": "an independent analysis of the observable",
        "transported_efficiency": "an efficiency or calibration derived in another run regime and reused",
        "partial_acceptance_channel": "a channel covering part of the registered phase space",
    },
    "validator_kinds": {
        "calibration_and_closure_test": "the calibration valid over an operating range, plus the closure/null test that exposes a named mis-modelling class",
    },
    "statuses": {
        "VALID": "channel unblinded and accepted",
        "CENSORED": "calibration or channel under review; the result is not currently readable",
        "INVALID": "channel withdrawn (found to be mis-reconstructed) or its calibration invalidated",
    },
    "contexts": "run regimes (beam energy, pile-up condition, detector configuration)",
    "relations": {
        "ISOMORPHIC": "same run regime",
        "BEHAVIORALLY_EQUIVALENT": "detector response verified identical within tolerance",
        "PREDICTIVELY_EQUIVALENT": "the simulation predicts both regimes equally well",
        "DECISION_DOMINATES": "the source regime bounds the target regime conservatively",
        "APPROXIMATELY_EQUIVALENT": "regimes agree only to an unquantified approximation",
        "INCOMPARABLE": "no validated regime relation",
        "CANNOT_CHECK": "the regime comparison has not been performed",
    },
    "global_witness": "a covariance-aware global consistency test (bins agree pairwise but the correlated fit does not)",
    "authority": "a measurement licenses belief in the value; changing an operational setpoint requires a separate registered authorization",
    "failure_classes": ("DETECTOR_MISMODELLING", "PILEUP_BIAS", "CALIBRATION_DRIFT", "UNBLINDING_BIAS"),
}

NATIVE_REVIEW = {
    "mode": MODE,
    "native_objects_and_vocabulary": NATIVE_VOCABULARY,
    "strongest_native_methods": [
        "uncertainty budget with an explicit correlation model across systematic sources",
        "calibration validity check against the operating range",
        "closure / null tests targeted at named mis-modelling classes",
        "blind-analysis protocol and unblinding discipline",
        "regime-transfer validation for efficiencies imported from another run condition",
        "covariance-aware global consistency (global chi-square) rather than bin-by-bin agreement",
    ],
    "valid_and_invalid_transitions": {
        "valid": "commit to the observable exceeding the threshold when the combined estimate minus two combined sigma exceeds it, all retained channels are calibrated at the operating point, the closure test can expose the asserted mis-modelling class, imported efficiencies transport, and the acceptance covers the phase space",
        "invalid": "combine channels sharing a systematic source in quadrature; keep a calibration outside its range; accept bin-by-bin agreement in place of the covariance-aware test; report the fiducial result as the total",
    },
    "native_failure_classes": list(NATIVE_VOCABULARY["failure_classes"]),
    "evaluator_assumptions": "a closure test certifies only the mis-modelling class it was designed to expose; a null result from a test blind to the class asserts nothing",
    "lossy_or_invalid_ME_abstractions": [
        "LOSSY: a Boolean 'support family' cannot carry the error budget — the decisive quantity is a real number with a correlation structure",
        "LOSSY: 'dependence discovered' is treated as a defeat, whereas physics treats it as a correlation term that changes the combined uncertainty",
        "REDUNDANT: 'target identity' partly duplicates the fiducial-versus-total distinction, which is native and quantitative",
        "VALID: typed transport maps cleanly onto regime-transfer validation",
    ],
    "strongest_plausible_parent_composition": "uncertainty-budget propagation with a correlation model + calibration range checks + closure-test coverage + regime-transfer validation + acceptance bookkeeping, composed by ordinary engineering glue",
    "reviewer": "study author (no independent domain reviewer was available; registered as a limitation in design §10)",
}

RELATION_LABELS = NATIVE_VOCABULARY["relations"]
Z_COMMIT = 2.0  # frozen: commit only if estimate - 2 sigma exceeds the threshold


def identity(target, u: Unit) -> str:
    """Signature = (observable, phase_space). Same observable in a strictly
    smaller phase space is a fiducial measurement: narrowing, not mismatch."""
    if tuple(u.signature) == tuple(target.signature):
        return "EXACT"
    if u.signature and target.signature and u.signature[0] == target.signature[0]:
        if len(u.signature) > 1 and len(target.signature) > 1 and u.signature[1] == "FIDUCIAL" and target.signature[1] == "TOTAL":
            return "NARROWED"
    return "MISMATCH"


def apparatus_ok(ep: Episode, u: Unit) -> bool:
    """Calibration validity is range-valued: valid status *and* the operating
    point inside the range the calibration was derived in."""
    if u.validator is None:
        return True
    v = ep.validators[u.validator]
    if v.status in (INVALID, CENSORED):
        return False
    if v.range_lo is not None and ep.operating_point < v.range_lo:
        return False
    if v.range_hi is not None and ep.operating_point > v.range_hi:
        return False
    return True


def evaluator_covers(ep: Episode, u: Unit) -> bool:
    if u.validator is None:
        return True
    v = ep.validators[u.validator]
    return ep.target.asserted_failure_class in v.covers


def _correlated(ep: Episode, a: str, b: str) -> bool:
    ua, ub = ep.units[a], ep.units[b]
    if ua.syst_source is not None and ua.syst_source == ub.syst_source:
        return True
    anc_a = {x for x, k in ua.ancestry if k == "CONFIRMED"}
    anc_b = {x for x, k in ub.ancestry if k == "CONFIRMED"}
    return bool(anc_a & anc_b)


def independent_groups(ep: Episode, fam: Family) -> int:
    uids = [x for x in fam.unit_ids if x in ep.units and ep.units[x].status != INVALID and identity(ep.target, ep.units[x]) != "MISMATCH"]
    parent = {x: x for x in uids}

    def find(a: str) -> str:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, a in enumerate(uids):
        for b in uids[i + 1:]:
            if _correlated(ep, a, b):
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    return len({find(x) for x in uids})


def transport_ok(ep: Episode, fam: Family, u: Unit) -> bool:
    if u.context == ep.target.context:
        return True
    rel = ep.relation(u.context, ep.target.context)
    return RELATION_RANK.get(rel, 0) >= RELATION_RANK[fam.required_relation]


def coverage_ok(ep: Episode, fam: Family, coverage: tuple[str, ...]) -> bool:
    """Acceptance may be assembled from several channels."""
    have: set[str] = set()
    for uid in fam.unit_ids:
        u = ep.units.get(uid)
        if u is None or u.status == INVALID or identity(ep.target, u) == "MISMATCH":
            continue
        have |= set(u.coverage)
    return set(coverage) <= have


def aggregate(ep: Episode, uids: list[str]):
    """Inverse-variance combination. Statistical errors add in quadrature;
    systematic errors add *linearly within a shared source group* and in
    quadrature across groups. Returns (point, sigma)."""
    live = [ep.units[u] for u in uids if u in ep.units and ep.units[u].status != INVALID]
    if not live:
        return None
    weights = []
    for u in live:
        var = u.stat_err ** 2 + u.syst_err ** 2
        weights.append(1.0 / var if var > 0 else 1.0e6)
    wsum = sum(weights)
    point = sum(w * u.estimate for w, u in zip(weights, live)) / wsum
    stat = math.sqrt(sum((w / wsum) ** 2 * u.stat_err ** 2 for w, u in zip(weights, live)))
    groups: dict[str, float] = {}
    for w, u in zip(weights, live):
        key = u.syst_source if u.syst_source is not None else f"__uncorr__{u.uid}"
        groups[key] = groups.get(key, 0.0) + (w / wsum) * u.syst_err  # linear within a source
    syst = math.sqrt(sum(v ** 2 for v in groups.values()))            # quadrature across sources
    return (point, math.sqrt(stat ** 2 + syst ** 2))


def commits(ep: Episode, agg) -> bool:
    point, sigma = agg
    return point - Z_COMMIT * sigma > ep.target.threshold


# ---- generator hooks (native surface constants) ---------------------------------
NUMERIC = True
BASE_SIGNATURE = ("sigma_incl", "TOTAL")
UNIT_KIND_MAIN = "measurement_channel"
UNIT_KIND_SUPPORT = "measurement_channel"
UNIT_KIND_TRANSPORTED = "transported_efficiency"
UNIT_KIND_CASE = "partial_acceptance_channel"
VALIDATOR_KIND = "calibration_and_closure_test"
FAILURE_CLASSES = NATIVE_VOCABULARY["failure_classes"]
TRANSPORT_REQUIRED = "PREDICTIVELY_EQUIVALENT"
TRANSPORT_BREAKING_RELATION = "APPROXIMATELY_EQUIVALENT"
TRANSPORT_SAFE_RELATION = "BEHAVIORALLY_EQUIVALENT"
EVENT_LABELS = {
    "SET_UNIT_STATUS": "a channel is withdrawn after a reconstruction fault is found",
    "SET_UNIT_SIGNATURE": "the channel is found to measure a different observable",
    "SET_VALIDATOR_STATUS": "the calibration is invalidated",
    "SET_VALIDATOR_COVERAGE": "the closure test is found blind to the asserted mis-modelling class",
    "SET_RELATION": "the run-regime relation is retyped",
    "ADD_ANCESTRY": "a shared detector simulation is discovered behind two channels",
    "SET_TARGET_COVERAGE": "the registered phase space is widened",
    "SET_OPERATING_POINT": "the operating point moves outside the calibrated range",
    "SET_GLOBAL_WITNESS": "the covariance-aware global consistency test is withdrawn",
    "SET_AUTHORITY_GRANT": "the setpoint-change authorization is withdrawn",
    "ADD_UNIT": "a further channel reports",
    "REGISTERED_NO_OP": "a registered change that touches nothing the measurement depends on",
}


def drift(sig: tuple[str, ...]) -> tuple[str, ...]:
    return ("sigma_other", sig[1])


def narrowed_variant(sig: tuple[str, ...]):
    return (sig[0], "FIDUCIAL")
