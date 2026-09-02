#!/usr/bin/env python3
"""ME-X5 episode generator with per-mode planters and an enforced stratum invariant.

Every instance is generated from `sha256(split_seed|mode|stratum|index)`, is
checked to be a *warranted commitment before its registered events* (v0 =
COMMIT/NONE), and is rejected unless the exact oracle reproduces the stratum's
hand-declared final decision (the invariant table `STRATUM_INVARIANT`). The
invariant table is the study's known-answer specification: it is written by hand
in the design, not read off the oracle.

Planting is shared across modes; *semantics* are not. The same planted structure
("two supports turn out to share an ancestor") is evaluated by three native rule
sets that disagree about what it implies, which is why the same plant yields a
hard defeat in the deductive mode, an error-budget change in the measurement mode
and a deduplication in the synthesis mode.
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import replace
from typing import Any

import mex5_native_formal as NF
import mex5_native_measurement as NM
import mex5_native_synthesis as NS
from mex5_model import (
    CENSORED,
    INVALID,
    MODES,
    STRATA,
    VALID,
    Episode,
    Family,
    Target,
    Unit,
    Validator,
    unit_to_json,
)
from mex5_oracle import MAX_CENSORED_FACTS, censored_facts, oracle_trajectory, rules_for, valid_at_v0

MAX_TRIES = 400

# Hand-declared expected final decision per stratum (action, locus). `None` means
# the field is variant-dependent and is checked by the per-variant rule below.
STRATUM_INVARIANT: dict[str, tuple[str, str | None]] = {
    "TARGET_IDENTITY_DRIFT": ("WITHHOLD", "TARGET_IDENTITY"),
    "APPARATUS_INVALID": ("WITHHOLD", "APPARATUS_VALIDITY"),
    "BLIND_EVALUATOR": ("WITHHOLD", "EVALUATOR_COVERAGE"),
    "HIDDEN_DEPENDENCE": ("WITHHOLD", "DEPENDENCE"),
    "INVALID_TRANSPORT": ("WITHHOLD", "TRANSPORT"),
    "DEFEATED_SUPPORT": ("WITHHOLD", "SUPPORT_DEFEAT"),
    "SCOPE_OVERREACH": (None, "SCOPE"),
    "LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION": ("WITHHOLD", "GLOBAL_OBSTRUCTION"),
    "AUTHORITY_MISMATCH": ("COMMIT", "NONE"),
    "CENSORED_UNRESOLVED": ("UNRESOLVED", None),
    "FULLY_WARRANTED_CONTROL": ("COMMIT", "NONE"),
    "SINGLE_PARENT_SUFFICIENT": ("WITHHOLD", "SUPPORT_DEFEAT"),
}


def _rng(split_seed: str, mode: str, stratum: str, index: int) -> random.Random:
    h = hashlib.sha256(f"{split_seed}|{mode}|{stratum}|{index}".encode()).hexdigest()[:16]
    return random.Random(int(h, 16))


def _validator(R, vid: str, covers, *, status: str = VALID, uncertain=(), lo=None, hi=None) -> Validator:
    return Validator(vid=vid, kind=R.VALIDATOR_KIND, covers=tuple(covers), uncertain=tuple(uncertain),
                     status=status, range_lo=lo, range_hi=hi)


def _unit(R, rng, uid, *, kind=None, sig=None, ctx="ctx0", cov=("h1", "h2"), validator="v0",
          est=None, stat=0.20, syst=0.10, syst_source=None, weight=None, ancestry=(), status=VALID) -> Unit:
    return Unit(
        uid=uid, kind=kind or R.UNIT_KIND_MAIN, signature=tuple(sig or R.BASE_SIGNATURE), context=ctx,
        coverage=tuple(cov), ancestry=tuple(ancestry), validator=validator, status=status,
        estimate=(2.0 + rng.uniform(-0.15, 0.15)) if est is None else est,
        stat_err=stat, syst_err=syst, syst_source=syst_source,
        weight=weight if weight is not None else rng.randint(400, 4000),
    )


def _target(R, rng, *, coverage=("h1",), authority="BELIEF", failure_class=None, sig=None) -> Target:
    return Target(
        tid="t0", signature=tuple(sig or R.BASE_SIGNATURE), coverage=tuple(coverage),
        asserted_failure_class=failure_class or R.FAILURE_CLASSES[0],
        requested_authority=authority, context="ctx0", threshold=1.0 if R.NUMERIC else 0.0,
    )


def _episode(mode, stratum, seed, target, units, families, validators, **kw) -> Episode:
    return Episode(
        mode=mode, episode_id=kw.pop("episode_id", ""), stratum=stratum, seed=seed, target=target,
        units={u.uid: u for u in units}, families={f.fid: f for f in families},
        validators={v.vid: v for v in validators},
        relations=kw.pop("relations", {}), operating_point=kw.pop("operating_point", 0.0),
        global_witness=kw.pop("global_witness", True), authority_granted=kw.pop("authority_granted", True),
        narrowed_coverage=kw.pop("narrowed_coverage", None), events=tuple(kw.pop("events", ())),
        features=kw.pop("features", {}),
    )


# ---- per-stratum planters ----------------------------------------------------------

def _plant(mode: str, stratum: str, rng: random.Random) -> Episode:
    R = rules_for(mode)
    fcs = R.FAILURE_CLASSES
    fc = fcs[0]
    V = [_validator(R, "v0", fcs, lo=-10.0, hi=10.0), _validator(R, "v1", fcs, lo=-10.0, hi=10.0)]
    req = R.TRANSPORT_REQUIRED
    noop = {"op": "REGISTERED_NO_OP", "note": R.EVENT_LABELS["REGISTERED_NO_OP"]}

    if stratum == "TARGET_IDENTITY_DRIFT":
        # a shared artefact turns out to establish a different registered target
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u0", "u2"), required_relation=req)]
        ev = [{"op": "SET_UNIT_SIGNATURE", "uid": "u0", "signature": list(R.drift(R.BASE_SIGNATURE)),
               "note": R.EVENT_LABELS["SET_UNIT_SIGNATURE"]}]
        if rng.random() < 0.5:
            ev.insert(0, noop)
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev, features={"variant": "SHARED_ARTEFACT_DRIFT"})

    if stratum == "APPARATUS_INVALID":
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        if R.NUMERIC and rng.random() < 0.5:
            ev = [{"op": "SET_OPERATING_POINT", "value": 50.0, "note": R.EVENT_LABELS["SET_OPERATING_POINT"]}]
            variant = "OPERATING_POINT_LEFT_CALIBRATED_RANGE"
        else:
            ev = [{"op": "SET_VALIDATOR_STATUS", "vid": "v0", "status": INVALID, "note": R.EVENT_LABELS["SET_VALIDATOR_STATUS"]}]
            variant = "APPARATUS_WITHDRAWN"
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev, features={"variant": variant})

    if stratum == "BLIND_EVALUATOR":
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        ev = [{"op": "SET_VALIDATOR_COVERAGE", "vid": "v0", "covers": [c for c in fcs if c != fc], "uncertain": [],
               "note": R.EVENT_LABELS["SET_VALIDATOR_COVERAGE"]}]
        return _episode(mode, stratum, "", _target(R, rng, failure_class=fc), units, fams, V, events=ev,
                        features={"variant": "COVERAGE_NARROWED_BELOW_ASSERTED_CLASS"})

    if stratum == "HIDDEN_DEPENDENCE":
        units = [_unit(R, rng, "u0", syst_source="s_a"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT, syst_source="s_b"),
                 _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT, syst_source="s_c"), _unit(R, rng, "u3", kind=R.UNIT_KIND_SUPPORT, syst_source="s_d")]
        fams = [Family("F1", ("u0", "u1"), min_independent=2, required_relation=req),
                Family("F2", ("u2", "u3"), min_independent=2, required_relation=req)]
        ev = [{"op": "ADD_ANCESTRY", "uid": "u0", "ancestor": "a_shared", "kind": "CONFIRMED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
              {"op": "ADD_ANCESTRY", "uid": "u1", "ancestor": "a_shared", "kind": "CONFIRMED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
              {"op": "ADD_ANCESTRY", "uid": "u2", "ancestor": "a_shared2", "kind": "CONFIRMED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
              {"op": "ADD_ANCESTRY", "uid": "u3", "ancestor": "a_shared2", "kind": "CONFIRMED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]}]
        if rng.random() < 0.5:
            # decoy: an ancestry edge that merges two units already in one component
            ev.append({"op": "ADD_ANCESTRY", "uid": "u0", "ancestor": "a_shared", "kind": "CONFIRMED",
                       "note": R.EVENT_LABELS["ADD_ANCESTRY"]})
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev,
                        features={"variant": "CONFIRMED_SHARED_ANCESTOR_IN_EVERY_REDUNDANT_FAMILY"})

    if stratum == "INVALID_TRANSPORT":
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1"),
                 _unit(R, rng, "u2", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1")]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        rel = {"ctx1>ctx0": "ISOMORPHIC"}
        ev = [{"op": "SET_RELATION", "src": "ctx1", "dst": "ctx0", "relation": R.TRANSPORT_BREAKING_RELATION,
               "note": R.EVENT_LABELS["SET_RELATION"]}]
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, relations=rel, events=ev,
                        features={"variant": "REUSE_LICENCE_RETYPED_BELOW_REQUIREMENT"})

    if stratum == "DEFEATED_SUPPORT":
        numeric_route = R.NUMERIC and rng.random() < 0.5
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        if numeric_route:
            newu = _unit(R, rng, "u9", kind=R.UNIT_KIND_SUPPORT, est=0.0, stat=0.05, syst=0.02, syst_source="s_new", weight=9000)
            ev = [{"op": "ADD_UNIT", "fid": "F1", "unit": unit_to_json(newu), "note": R.EVENT_LABELS["ADD_UNIT"]}]
            variant = "NUMERIC_AGGREGATE_FALLS_BELOW_THRESHOLD"
        else:
            ev = [{"op": "SET_UNIT_STATUS", "uid": "u0", "status": INVALID, "note": R.EVENT_LABELS["SET_UNIT_STATUS"]},
                  {"op": "SET_UNIT_STATUS", "uid": "u2", "status": INVALID, "note": R.EVENT_LABELS["SET_UNIT_STATUS"]}]
            variant = "EVERY_SUFFICIENT_SUPPORT_WITHDRAWN"
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev, features={"variant": variant})

    if stratum == "SCOPE_OVERREACH":
        narrowable = rng.random() < 0.6
        if R.NUMERIC and R.narrowed_variant(R.BASE_SIGNATURE) is not None and rng.random() < 0.4:
            # native identity-narrowing route (fiducial vs total)
            units = [_unit(R, rng, "u0", sig=R.narrowed_variant(R.BASE_SIGNATURE)),
                     _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT, sig=R.narrowed_variant(R.BASE_SIGNATURE)),
                     _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT, sig=R.narrowed_variant(R.BASE_SIGNATURE))]
            fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
            ev = [{"op": "SET_UNIT_SIGNATURE", "uid": "u0", "signature": list(R.narrowed_variant(R.BASE_SIGNATURE)),
                   "note": R.EVENT_LABELS["SET_UNIT_SIGNATURE"]}]
            base_units = [replace(u, signature=tuple(R.BASE_SIGNATURE)) for u in units]
            return _episode(mode, stratum, "", _target(R, rng), base_units, fams, V,
                            events=[{"op": "SET_UNIT_SIGNATURE", "uid": u.uid, "signature": list(R.narrowed_variant(R.BASE_SIGNATURE)),
                                     "note": R.EVENT_LABELS["SET_UNIT_SIGNATURE"]} for u in base_units],
                            features={"variant": "FIDUCIAL_RESTRICTION"})
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        ev = [{"op": "SET_TARGET_COVERAGE", "coverage": ["h1", "h3"], "note": R.EVENT_LABELS["SET_TARGET_COVERAGE"]}]
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev,
                        narrowed_coverage=("h1",) if narrowable else None,
                        features={"variant": "REGISTERED_SCOPE_WIDENED_BEYOND_COVERAGE",
                                  "narrowing_registered": narrowable})

    if stratum == "LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION":
        units = [_unit(R, rng, "u0", kind=R.UNIT_KIND_CASE, cov=("h1", "h2")),
                 _unit(R, rng, "u1", kind=R.UNIT_KIND_CASE, cov=("h1", "h2")),
                 _unit(R, rng, "u2", kind=R.UNIT_KIND_CASE, cov=("h1", "h2"))]
        fams = [Family("F1", ("u0", "u1"), required_relation=req, requires_global_witness=True),
                Family("F2", ("u2",), required_relation=req, requires_global_witness=True)]
        ev = [{"op": "SET_GLOBAL_WITNESS", "value": False, "note": R.EVENT_LABELS["SET_GLOBAL_WITNESS"]}]
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev,
                        features={"variant": "PAIRWISE_COMPATIBLE_NO_GLOBAL_WITNESS"})

    if stratum == "AUTHORITY_MISMATCH":
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        ev = [{"op": "SET_AUTHORITY_GRANT", "value": False, "note": R.EVENT_LABELS["SET_AUTHORITY_GRANT"]}]
        return _episode(mode, stratum, "", _target(R, rng, authority="ACTION"), units, fams, V, events=ev,
                        features={"variant": "OPERATIONAL_MANDATE_WITHDRAWN_BELIEF_INTACT"})

    if stratum == "CENSORED_UNRESOLVED":
        variant = rng.choice(["UNIT", "VALIDATOR", "COVERAGE", "ANCESTRY", "RELATION"])
        if variant == "UNIT":
            units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
            fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u0", "u2"), required_relation=req)]
            ev = [{"op": "SET_UNIT_STATUS", "uid": "u0", "status": CENSORED, "note": R.EVENT_LABELS["SET_UNIT_STATUS"]}]
        elif variant == "VALIDATOR":
            units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
            fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
            ev = [{"op": "SET_VALIDATOR_STATUS", "vid": "v0", "status": CENSORED, "note": R.EVENT_LABELS["SET_VALIDATOR_STATUS"]}]
        elif variant == "COVERAGE":
            units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
            fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
            ev = [{"op": "SET_VALIDATOR_COVERAGE", "vid": "v0", "covers": [c for c in fcs if c != fc], "uncertain": [fc],
                   "note": R.EVENT_LABELS["SET_VALIDATOR_COVERAGE"]}]
        elif variant == "ANCESTRY":
            units = [_unit(R, rng, "u0", syst_source="s_a"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT, syst_source="s_b"),
                     _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT, syst_source="s_c"), _unit(R, rng, "u3", kind=R.UNIT_KIND_SUPPORT, syst_source="s_d")]
            fams = [Family("F1", ("u0", "u1"), min_independent=2, required_relation=req),
                    Family("F2", ("u2", "u3"), min_independent=2, required_relation=req)]
            ev = [{"op": "ADD_ANCESTRY", "uid": "u0", "ancestor": "a_s", "kind": "SUSPECTED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
                  {"op": "ADD_ANCESTRY", "uid": "u1", "ancestor": "a_s", "kind": "SUSPECTED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
                  {"op": "ADD_ANCESTRY", "uid": "u2", "ancestor": "a_t", "kind": "SUSPECTED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
                  {"op": "ADD_ANCESTRY", "uid": "u3", "ancestor": "a_t", "kind": "SUSPECTED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]}]
        else:
            units = [_unit(R, rng, "u0", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1"),
                     _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1")]
            fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
            ev = [{"op": "SET_RELATION", "src": "ctx1", "dst": "ctx0", "relation": "CANNOT_CHECK", "note": R.EVENT_LABELS["SET_RELATION"]}]
            return _episode(mode, stratum, "", _target(R, rng), units, fams, V, relations={"ctx1>ctx0": "ISOMORPHIC"},
                            events=ev, features={"variant": f"CENSORED_{variant}"})
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev, features={"variant": f"CENSORED_{variant}"})

    if stratum == "FULLY_WARRANTED_CONTROL":
        variant = rng.choice(["SAFE_RETYPE", "COVERAGE_WIDENED", "CONSISTENT_UNIT_ADDED", "IRRELEVANT_ANCESTRY", "NO_OP"])
        units = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        rel: dict[str, str] = {}
        if variant == "SAFE_RETYPE":
            units[1] = _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT, ctx="ctx1")
            rel = {"ctx1>ctx0": "ISOMORPHIC"}
            ev = [{"op": "SET_RELATION", "src": "ctx1", "dst": "ctx0", "relation": R.TRANSPORT_SAFE_RELATION,
                   "note": R.EVENT_LABELS["SET_RELATION"]}]
        elif variant == "COVERAGE_WIDENED":
            ev = [{"op": "SET_VALIDATOR_COVERAGE", "vid": "v0", "covers": list(fcs), "uncertain": [],
                   "note": R.EVENT_LABELS["SET_VALIDATOR_COVERAGE"]}]
        elif variant == "CONSISTENT_UNIT_ADDED":
            newu = _unit(R, rng, "u9", kind=R.UNIT_KIND_SUPPORT, syst_source="s_new")
            ev = [{"op": "ADD_UNIT", "fid": "F2", "unit": unit_to_json(newu), "note": R.EVENT_LABELS["ADD_UNIT"]}]
        elif variant == "IRRELEVANT_ANCESTRY":
            ev = [{"op": "ADD_ANCESTRY", "uid": "u0", "ancestor": "a_x", "kind": "CONFIRMED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]},
                  {"op": "ADD_ANCESTRY", "uid": "u1", "ancestor": "a_x", "kind": "CONFIRMED", "note": R.EVENT_LABELS["ADD_ANCESTRY"]}]
        else:
            ev = [noop, noop]
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, relations=rel, events=ev,
                        features={"variant": variant})

    if stratum == "SINGLE_PARENT_SUFFICIENT":
        units = [_unit(R, rng, "u0")]
        fams = [Family("F1", ("u0",), required_relation=req)]
        ev = [{"op": "SET_UNIT_STATUS", "uid": "u0", "status": INVALID, "note": R.EVENT_LABELS["SET_UNIT_STATUS"]}]
        return _episode(mode, stratum, "", _target(R, rng), units, fams, V, events=ev,
                        features={"variant": "PROVENANCE_ALONE_DECIDES"})

    raise ValueError(f"unknown stratum {stratum!r}")


# ---- instance generation with invariant enforcement ---------------------------------

def _invariant_holds(ep: Episode, traj) -> bool:
    exp_action, exp_locus = STRATUM_INVARIANT[ep.stratum]
    d = traj[-1].decision
    if ep.stratum == "SCOPE_OVERREACH":
        want = "COMMIT_NARROWED" if (ep.narrowed_coverage is not None or ep.features.get("variant") == "FIDUCIAL_RESTRICTION") else "WITHHOLD"
        return d.action == want and d.locus == "SCOPE"
    if ep.stratum == "AUTHORITY_MISMATCH":
        return d.action == "COMMIT" and d.locus == "NONE" and d.authority == "BELIEF_ONLY" and traj[0].decision.authority == "BELIEF_AND_ACTION"
    if exp_action is not None and d.action != exp_action:
        return False
    if exp_locus is not None and d.locus != exp_locus:
        return False
    return True


def generate_instance(split: str, split_seed: str, mode: str, stratum: str, index: int):
    for attempt in range(MAX_TRIES):
        rng = _rng(split_seed, mode, stratum, index * MAX_TRIES + attempt)
        ep = _plant(mode, stratum, rng)
        ep = replace(ep, episode_id=f"{split}-{mode}-{stratum}-{index:04d}",
                     seed=hashlib.sha256(f"{split_seed}|{mode}|{stratum}|{index}|{attempt}".encode()).hexdigest()[:12])
        if any(len(censored_facts(s)) > MAX_CENSORED_FACTS for s in __import__("mex5_model").trajectory(ep)):
            continue
        if not valid_at_v0(ep):
            continue
        traj = oracle_trajectory(ep)
        if not _invariant_holds(ep, traj):
            continue
        return ep, traj
    raise RuntimeError(f"could not plant {mode}/{stratum}/{index} in {MAX_TRIES} attempts")


def generate_split(split: str, split_seed: str, per_mode_stratum: int):
    out = []
    for mode in MODES:
        for stratum in STRATA:
            for i in range(per_mode_stratum):
                out.append(generate_instance(split, split_seed, mode, stratum, i))
    return out


# ---- hand-authored known-answer fixtures (G0a) ------------------------------------

def known_answer_fixtures() -> list[dict[str, Any]]:
    """Nine episodes whose correct decision is written out by hand here. They
    exercise the shell's tricky corners: a partial family failure that must NOT
    defeat the target, a censored fact that must NOT produce UNRESOLVED, and the
    narrowing route."""
    out: list[dict[str, Any]] = []
    for mode in MODES:
        R = rules_for(mode)
        rng = random.Random(11)
        fcs = R.FAILURE_CLASSES
        req = R.TRANSPORT_REQUIRED
        V = [_validator(R, "v0", fcs, lo=-10.0, hi=10.0), _validator(R, "v1", fcs, lo=-10.0, hi=10.0)]

        # KA-a: one family is destroyed, an independent family survives -> COMMIT.
        units = [_unit(R, rng, "u0", est=2.0), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT, est=2.0),
                 _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT, est=2.0, validator="v1")]
        fams = [Family("F1", ("u0", "u1"), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        ep = _episode(mode, "KA", "ka", _target(R, rng), units, fams, V,
                      events=[{"op": "SET_UNIT_STATUS", "uid": "u0", "status": INVALID}],
                      episode_id=f"KA-a-{mode}")
        out.append({"name": f"KA-a-{mode}-PARTIAL_FAILURE_DOES_NOT_DEFEAT",
                    "episode": ep, "expected": {"action": "COMMIT", "locus": "NONE", "authority": "BELIEF_ONLY"}})

        # KA-b: a censored element that cannot change the decision -> still COMMIT,
        # not UNRESOLVED (the surviving family is untouched by the censored fact).
        units = [_unit(R, rng, "u0", est=2.0), _unit(R, rng, "u2", kind=R.UNIT_KIND_SUPPORT, est=2.0, validator="v1")]
        fams = [Family("F1", ("u0",), required_relation=req), Family("F2", ("u2",), required_relation=req)]
        ep = _episode(mode, "KA", "ka", _target(R, rng), units, fams, V,
                      events=[{"op": "SET_VALIDATOR_STATUS", "vid": "v0", "status": CENSORED}],
                      episode_id=f"KA-b-{mode}")
        out.append({"name": f"KA-b-{mode}-CENSORING_THAT_CANNOT_FLIP_THE_DECISION",
                    "episode": ep, "expected": {"action": "COMMIT", "locus": "NONE", "authority": "BELIEF_ONLY"}})

        # KA-c: registered scope widened beyond every family's coverage, with a
        # narrowed scope registered -> COMMIT_NARROWED on SCOPE.
        units = [_unit(R, rng, "u0", est=2.0), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT, est=2.0)]
        fams = [Family("F1", ("u0", "u1"), required_relation=req)]
        ep = _episode(mode, "KA", "ka", _target(R, rng), units, fams, V,
                      events=[{"op": "SET_TARGET_COVERAGE", "coverage": ["h1", "h3"]}],
                      narrowed_coverage=("h1",), episode_id=f"KA-c-{mode}")
        out.append({"name": f"KA-c-{mode}-NARROWED_COMMITMENT",
                    "episode": ep, "expected": {"action": "COMMIT_NARROWED", "locus": "SCOPE", "authority": "BELIEF_ONLY"}})
    return out


# ---- H-EXT-3 finite separation pair ------------------------------------------------

def separation_pair() -> list[dict[str, Any]]:
    """A finite pair on which any federation whose inter-module channel carries only
    *family-anonymous* per-target verdicts must err, while witness-level exchange is
    exact on both. P and Q share the identical event sequence and the identical
    per-module verdict tuple; they differ only in whether the two defeats land on the
    same family."""
    mode = "FORMAL"
    R = rules_for(mode)
    rng = random.Random(5)
    fcs = R.FAILURE_CLASSES
    V = [_validator(R, "v0", fcs)]
    req = R.TRANSPORT_REQUIRED
    rel = {"ctx1>ctx0": "ISOMORPHIC"}
    ev = [{"op": "ADD_ANCESTRY", "uid": "u0", "ancestor": "a_s", "kind": "CONFIRMED"},
          {"op": "ADD_ANCESTRY", "uid": "u1", "ancestor": "a_s", "kind": "CONFIRMED"},
          {"op": "SET_RELATION", "src": "ctx1", "dst": "ctx0", "relation": R.TRANSPORT_BREAKING_RELATION}]
    # P: dependence defeats F1, transport defeats F2 -> every family defeated.
    unitsP = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT),
              _unit(R, rng, "u2", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1")]
    famsP = [Family("F1", ("u0", "u1"), min_independent=2, required_relation=req),
             Family("F2", ("u2",), required_relation=req)]
    P = _episode(mode, "SEP", "sep", _target(R, rng), unitsP, famsP, V, relations=dict(rel), events=ev, episode_id="SEP-P")
    # Q: both defeats land on F1 (k = 3 is no longer met AND the ported lemma loses its
    # licence); F2 is a native, independent family -> COMMIT. Every module emits the same
    # family-anonymous verdict as in P, and there are two families in both.
    unitsQ = [_unit(R, rng, "u0"), _unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT),
              _unit(R, rng, "u2", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1"), _unit(R, rng, "u3", kind=R.UNIT_KIND_SUPPORT)]
    famsQ = [Family("F1", ("u0", "u1", "u2"), min_independent=3, required_relation=req),
             Family("F2", ("u3",), required_relation=req)]
    Q = _episode(mode, "SEP", "sep", _target(R, rng), unitsQ, famsQ, V, relations=dict(rel), events=ev, episode_id="SEP-Q")
    return [{"name": "SEP-P", "episode": P, "expected": {"action": "WITHHOLD", "locus": "TRANSPORT", "authority": "BELIEF_ONLY"}},
            {"name": "SEP-Q", "episode": Q, "expected": {"action": "COMMIT", "locus": "NONE", "authority": "BELIEF_ONLY"}}]
