#!/usr/bin/env python3
"""ME-X5 cross-domain field residual test: shared episode container.

The three native epistemic modes (FORMAL, MEASUREMENT, SYNTHESIS) share this
serialization container and nothing else. Every *rule* that turns a container
into a scientific decision lives in the mode module (`mex5_native_*.py`) and is
written in that mode's own vocabulary; the modes disagree about what identity,
dependence, scope and validity mean. The container is deliberately thin so that
cross-mode recurrence of the decision object is something the study *measures*
(the changed-vocabulary gate G5) rather than something the container asserts.

Registered limitation (design §10): the three modes were authored by one team in
one repository. Shared authorship is a common cause for any cross-mode
recurrence found here; the changed-vocabulary gate bounds, but cannot remove, it.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, replace
from typing import Any

MODES: tuple[str, ...] = ("FORMAL", "MEASUREMENT", "SYNTHESIS")

# Episode families (strata). Protocol ME-X5 §9 negative controls are the last
# four; the first eight are the coupled-contract families of the decisive-studies
# protocol §3.2 instantiated natively in each mode.
STRATA: tuple[str, ...] = (
    "TARGET_IDENTITY_DRIFT",
    "APPARATUS_INVALID",
    "BLIND_EVALUATOR",
    "HIDDEN_DEPENDENCE",
    "INVALID_TRANSPORT",
    "DEFEATED_SUPPORT",
    "SCOPE_OVERREACH",
    "LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION",
    "AUTHORITY_MISMATCH",
    "CENSORED_UNRESOLVED",
    "FULLY_WARRANTED_CONTROL",
    "SINGLE_PARENT_SUFFICIENT",
)

ACTIONS: tuple[str, ...] = ("COMMIT", "COMMIT_NARROWED", "WITHHOLD", "UNRESOLVED")
AUTHORITIES: tuple[str, ...] = ("BELIEF_ONLY", "BELIEF_AND_ACTION")

# Responsibility loci. Mode-neutral by construction: whether they are *recoverable*
# from native surface features without ORION vocabulary is gate G5.
LOCI: tuple[str, ...] = (
    "NONE",
    "TARGET_IDENTITY",
    "APPARATUS_VALIDITY",
    "EVALUATOR_COVERAGE",
    "DEPENDENCE",
    "TRANSPORT",
    "SUPPORT_DEFEAT",
    "SCOPE",
    "GLOBAL_OBSTRUCTION",
)
# Frozen responsibility ordering used when one family fails for several reasons.
LOCUS_PRIORITY: tuple[str, ...] = (
    "TARGET_IDENTITY",
    "APPARATUS_VALIDITY",
    "EVALUATOR_COVERAGE",
    "DEPENDENCE",
    "TRANSPORT",
    "SUPPORT_DEFEAT",
    "SCOPE",
    "GLOBAL_OBSTRUCTION",
)

VALID, CENSORED, INVALID = "VALID", "CENSORED", "INVALID"

# Typed transport vocabulary. Ranks are the parent-owned ORION structural
# relation ranks (orion_v2.structural.RelationType); each mode names them
# natively (mex5_native_*.RELATION_LABELS) but the order is shared.
RELATION_RANK: dict[str, int] = {
    "ISOMORPHIC": 5,
    "BEHAVIORALLY_EQUIVALENT": 4,
    "PREDICTIVELY_EQUIVALENT": 3,
    "DECISION_DOMINATES": 2,
    "APPROXIMATELY_EQUIVALENT": 1,
    "INCOMPARABLE": 0,
    "DISTINGUISHED_BY": 0,
    "CANNOT_CHECK": -1,  # censored
}


@dataclass(frozen=True)
class Decision:
    action: str
    locus: str
    authority: str

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.action, self.locus, self.authority)

    def as_dict(self) -> dict[str, str]:
        return {"action": self.action, "locus": self.locus, "authority": self.authority}


@dataclass(frozen=True)
class Unit:
    """A native support artefact: a lemma/proof term, a measurement channel, a
    primary study. `kind` is the native noun; the mode module decides what its
    fields mean."""
    uid: str
    kind: str
    signature: tuple[str, ...]
    context: str
    coverage: tuple[str, ...]
    ancestry: tuple[tuple[str, str], ...]  # (ancestor_id, CONFIRMED|SUSPECTED)
    validator: str | None
    status: str = VALID
    estimate: float = 0.0
    stat_err: float = 0.0
    syst_err: float = 0.0
    syst_source: str | None = None
    weight: float = 1.0  # native size (cohort n, exposure, proof strength)


@dataclass(frozen=True)
class Family:
    """A sufficient support family: an independent proof path, an independent
    measurement channel, an evidence body."""
    fid: str
    unit_ids: tuple[str, ...]
    min_independent: int = 0
    required_relation: str = "PREDICTIVELY_EQUIVALENT"
    requires_global_witness: bool = False


@dataclass(frozen=True)
class Validator:
    """The native checking apparatus: kernel+linter, calibration+closure test,
    risk-of-bias + outcome ascertainment."""
    vid: str
    kind: str
    covers: tuple[str, ...]
    uncertain: tuple[str, ...] = ()
    status: str = VALID
    range_lo: float | None = None
    range_hi: float | None = None


@dataclass(frozen=True)
class Target:
    tid: str
    signature: tuple[str, ...]
    coverage: tuple[str, ...]
    asserted_failure_class: str
    requested_authority: str  # BELIEF | ACTION
    context: str
    threshold: float = 0.0


@dataclass(frozen=True)
class Episode:
    mode: str
    episode_id: str
    stratum: str
    seed: str
    target: Target
    units: dict[str, Unit]
    families: dict[str, Family]
    validators: dict[str, Validator]
    relations: dict[str, str]  # "src>dst" -> relation name
    operating_point: float = 0.0
    global_witness: bool = True
    authority_granted: bool = True
    narrowed_coverage: tuple[str, ...] | None = None
    events: tuple[dict[str, Any], ...] = ()
    features: dict[str, Any] | None = None

    def relation(self, src: str, dst: str) -> str:
        if src == dst:
            return "ISOMORPHIC"
        return self.relations.get(f"{src}>{dst}", "INCOMPARABLE")


# ---- events -------------------------------------------------------------------

EVENT_OPS: tuple[str, ...] = (
    "SET_UNIT_STATUS",
    "SET_UNIT_SIGNATURE",
    "SET_VALIDATOR_STATUS",
    "SET_VALIDATOR_COVERAGE",
    "SET_RELATION",
    "ADD_ANCESTRY",
    "SET_TARGET_COVERAGE",
    "SET_OPERATING_POINT",
    "SET_GLOBAL_WITNESS",
    "SET_AUTHORITY_GRANT",
    "ADD_UNIT",
    "REGISTERED_NO_OP",
)


def apply_event(ep: Episode, ev: dict[str, Any]) -> Episode:
    op = ev["op"]
    if op == "SET_UNIT_STATUS":
        u = ep.units[ev["uid"]]
        return replace(ep, units={**ep.units, u.uid: replace(u, status=ev["status"])})
    if op == "SET_UNIT_SIGNATURE":
        u = ep.units[ev["uid"]]
        return replace(ep, units={**ep.units, u.uid: replace(u, signature=tuple(ev["signature"]))})
    if op == "SET_VALIDATOR_STATUS":
        v = ep.validators[ev["vid"]]
        return replace(ep, validators={**ep.validators, v.vid: replace(v, status=ev["status"])})
    if op == "SET_VALIDATOR_COVERAGE":
        v = ep.validators[ev["vid"]]
        return replace(ep, validators={**ep.validators, v.vid: replace(v, covers=tuple(ev["covers"]), uncertain=tuple(ev.get("uncertain", ())))})
    if op == "SET_RELATION":
        return replace(ep, relations={**ep.relations, f"{ev['src']}>{ev['dst']}": ev["relation"]})
    if op == "ADD_ANCESTRY":
        u = ep.units[ev["uid"]]
        anc = tuple(sorted(set(u.ancestry) | {(ev["ancestor"], ev["kind"])}))
        return replace(ep, units={**ep.units, u.uid: replace(u, ancestry=anc)})
    if op == "SET_TARGET_COVERAGE":
        return replace(ep, target=replace(ep.target, coverage=tuple(ev["coverage"])))
    if op == "SET_OPERATING_POINT":
        return replace(ep, operating_point=float(ev["value"]))
    if op == "SET_GLOBAL_WITNESS":
        return replace(ep, global_witness=bool(ev["value"]))
    if op == "SET_AUTHORITY_GRANT":
        return replace(ep, authority_granted=bool(ev["value"]))
    if op == "ADD_UNIT":
        u = unit_from_json(ev["unit"])
        fam = ep.families[ev["fid"]]
        return replace(
            ep,
            units={**ep.units, u.uid: u},
            families={**ep.families, fam.fid: replace(fam, unit_ids=tuple(fam.unit_ids) + (u.uid,))},
        )
    if op == "REGISTERED_NO_OP":
        return ep
    raise ValueError(f"unknown event op {op!r}")


def trajectory(ep: Episode) -> list[Episode]:
    """v0 (pre-event) followed by one episode state per registered event."""
    out = [ep]
    cur = ep
    for ev in ep.events:
        cur = apply_event(cur, ev)
        out.append(cur)
    return out


# ---- serialization ------------------------------------------------------------

def unit_to_json(u: Unit) -> dict[str, Any]:
    return {
        "uid": u.uid, "kind": u.kind, "signature": list(u.signature), "context": u.context,
        "coverage": list(u.coverage), "ancestry": [list(a) for a in u.ancestry], "validator": u.validator,
        "status": u.status, "estimate": u.estimate, "stat_err": u.stat_err, "syst_err": u.syst_err,
        "syst_source": u.syst_source, "weight": u.weight,
    }


def unit_from_json(d: dict[str, Any]) -> Unit:
    return Unit(
        uid=d["uid"], kind=d["kind"], signature=tuple(d["signature"]), context=d["context"],
        coverage=tuple(d["coverage"]), ancestry=tuple((a[0], a[1]) for a in d["ancestry"]),
        validator=d["validator"], status=d["status"], estimate=d["estimate"], stat_err=d["stat_err"],
        syst_err=d["syst_err"], syst_source=d["syst_source"], weight=d["weight"],
    )


def episode_to_json(ep: Episode) -> dict[str, Any]:
    t = ep.target
    return {
        "mode": ep.mode, "episode_id": ep.episode_id, "stratum": ep.stratum, "seed": ep.seed,
        "target": {"tid": t.tid, "signature": list(t.signature), "coverage": list(t.coverage),
                   "asserted_failure_class": t.asserted_failure_class, "requested_authority": t.requested_authority,
                   "context": t.context, "threshold": t.threshold},
        "units": {k: unit_to_json(v) for k, v in sorted(ep.units.items())},
        "families": {k: {"fid": v.fid, "unit_ids": list(v.unit_ids), "min_independent": v.min_independent,
                         "required_relation": v.required_relation, "requires_global_witness": v.requires_global_witness}
                     for k, v in sorted(ep.families.items())},
        "validators": {k: {"vid": v.vid, "kind": v.kind, "covers": list(v.covers), "uncertain": list(v.uncertain),
                           "status": v.status, "range_lo": v.range_lo, "range_hi": v.range_hi}
                       for k, v in sorted(ep.validators.items())},
        "relations": dict(sorted(ep.relations.items())),
        "operating_point": ep.operating_point, "global_witness": ep.global_witness,
        "authority_granted": ep.authority_granted,
        "narrowed_coverage": list(ep.narrowed_coverage) if ep.narrowed_coverage is not None else None,
        "events": [dict(e) for e in ep.events], "features": ep.features or {},
    }


def episode_from_json(d: dict[str, Any]) -> Episode:
    t = d["target"]
    return Episode(
        mode=d["mode"], episode_id=d["episode_id"], stratum=d["stratum"], seed=d["seed"],
        target=Target(tid=t["tid"], signature=tuple(t["signature"]), coverage=tuple(t["coverage"]),
                      asserted_failure_class=t["asserted_failure_class"], requested_authority=t["requested_authority"],
                      context=t["context"], threshold=t["threshold"]),
        units={k: unit_from_json(v) for k, v in d["units"].items()},
        families={k: Family(fid=v["fid"], unit_ids=tuple(v["unit_ids"]), min_independent=v["min_independent"],
                            required_relation=v["required_relation"], requires_global_witness=v["requires_global_witness"])
                  for k, v in d["families"].items()},
        validators={k: Validator(vid=v["vid"], kind=v["kind"], covers=tuple(v["covers"]), uncertain=tuple(v["uncertain"]),
                                 status=v["status"], range_lo=v["range_lo"], range_hi=v["range_hi"])
                    for k, v in d["validators"].items()},
        relations=dict(d["relations"]), operating_point=d["operating_point"], global_witness=d["global_witness"],
        authority_granted=d["authority_granted"],
        narrowed_coverage=tuple(d["narrowed_coverage"]) if d["narrowed_coverage"] is not None else None,
        events=tuple(dict(e) for e in d["events"]), features=d.get("features") or {},
    )


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
