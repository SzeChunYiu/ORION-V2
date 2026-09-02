#!/usr/bin/env python3
"""ME-X4 registered-information model (frozen with design V1).

Everything in this module is *registered information*: the versioned support
graph every arm receives, and the typed event vocabulary that updates it. No
answer key lives here. The oracle (mex4_oracle.py) interprets this model under
the frozen §2 semantics; arms interpret it under their own semantics.

Design: research/experiments/me-x4/ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.{md,json}
"""
from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass, field
from typing import Any

# Frozen strength order over orion_v2.structural.RelationType names used for
# typed transport. CANNOT_CHECK is not ranked: it is the censored status.
RELATION_RANK: dict[str, int] = {
    "ISOMORPHIC": 5,
    "BEHAVIORALLY_EQUIVALENT": 4,
    "PREDICTIVELY_EQUIVALENT": 3,
    "DECISION_DOMINATES": 2,
    "APPROXIMATELY_EQUIVALENT": 1,
    "INCOMPARABLE": 0,
    "DISTINGUISHED_BY": 0,
}
RELATION_CANNOT_CHECK = "CANNOT_CHECK"

STATUS_VALID = "VALID"
STATUS_INVALID = "INVALID"
STATUS_UNKNOWN = "UNKNOWN"

SOURCE_VALID = "VALID"
SOURCE_RETRACTED = "RETRACTED"
SOURCE_DISPUTED = "DISPUTED"

CAL_VALID = "VALID"
CAL_INVALID = "INVALID"
CAL_UNDER_REVIEW = "UNDER_REVIEW"

DEP_CONFIRMED = "CONFIRMED"
DEP_SUSPECTED = "SUSPECTED"

STRATA: tuple[str, ...] = (
    "SOURCE_RETRACTED",
    "DEPENDENCE_DISCOVERED",
    "CALIBRATION_INVALIDATED",
    "TRANSPORT_RELATION_INVALIDATED",
    "EVALUATOR_BLIND_OR_REPLACED",
    "PROBLEM_SCOPE_CHANGED",
    "NEW_INDEPENDENT_SUPPORT",
    "CORRECTION_RESTORES_SUPPORT",
    "PARTIAL_SUPPORT_FAILURE",
    "ALL_SUFFICIENT_SUPPORT_FAILED",
    "CANNOT_CHECK_EDGE",
    "NO_REOPENING_NEEDED",
)

EVENT_KINDS: tuple[str, ...] = (
    "SOURCE_RETRACTED",
    "SOURCE_RETRACTION_DISPUTED",
    "SOURCE_CORRECTED",
    "CALIBRATION_INVALIDATED",
    "CALIBRATION_UNDER_REVIEW",
    "CALIBRATION_REVALIDATED",
    "DEPENDENCE_DISCOVERED",
    "DEPENDENCE_SUSPECTED",
    "RELATION_RETYPED",
    "EVALUATOR_COVERAGE_CHANGED",
    "CLAIM_FAILURE_CLASS_CHANGED",
    "CLAIM_SCOPE_CHANGED",
    "FAMILY_ADDED",
    "EVIDENCE_ADDED",
)


@dataclass
class Claim:
    claim_id: str
    context_id: str
    failure_class: str
    scope: tuple[str, ...]
    accepted_v0: bool = True
    alternative_of: str = ""


@dataclass
class Evidence:
    evidence_id: str
    claim_id: str
    source_id: str
    context_id: str
    scope_coverage: tuple[str, ...]
    evaluator_id: str = ""
    calibration_id: str = ""
    data_id: str = ""
    model_id: str = ""
    instrument_id: str = ""
    supports: bool = True


@dataclass
class Family:
    family_id: str
    claim_id: str
    evidence_ids: tuple[str, ...]
    prerequisite_ids: tuple[str, ...] = ()
    min_independent: int = 0
    required_relation: str = ""


@dataclass
class Calibration:
    calibration_id: str
    instrument_id: str
    status: str = CAL_VALID


@dataclass
class Evaluator:
    evaluator_id: str
    coverage: tuple[str, ...]
    uncertain: tuple[str, ...] = ()


@dataclass
class Relation:
    source_context: str
    target_context: str
    relation_type: str


@dataclass
class DependenceDeclaration:
    left_id: str
    right_id: str
    kind: str
    status: str = DEP_CONFIRMED


@dataclass
class Event:
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    note: str = ""


@dataclass
class World:
    """Registered support graph at one version."""

    claims: dict[str, Claim] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    families: dict[str, Family] = field(default_factory=dict)
    sources: dict[str, str] = field(default_factory=dict)
    calibrations: dict[str, Calibration] = field(default_factory=dict)
    evaluators: dict[str, Evaluator] = field(default_factory=dict)
    relations: dict[str, Relation] = field(default_factory=dict)
    dependence: list[DependenceDeclaration] = field(default_factory=list)

    # ---- structure accessors (registered information) -------------------
    def accepted_ids(self) -> tuple[str, ...]:
        return tuple(sorted(c for c, claim in self.claims.items() if claim.accepted_v0))

    def families_of(self, claim_id: str) -> tuple[Family, ...]:
        return tuple(f for f in sorted(self.families.values(), key=lambda x: x.family_id) if f.claim_id == claim_id)

    def positive_evidence_of_family(self, family: Family) -> tuple[Evidence, ...]:
        return tuple(self.evidence[e] for e in family.evidence_ids if self.evidence[e].supports)

    def negative_evidence_against(self, claim_id: str) -> tuple[Evidence, ...]:
        return tuple(e for e in sorted(self.evidence.values(), key=lambda x: x.evidence_id) if e.claim_id == claim_id and not e.supports)

    def relation_key(self, source_context: str, target_context: str) -> str:
        return f"{source_context}->{target_context}"

    def copy(self) -> "World":
        return copy.deepcopy(self)

    def validate(self) -> None:
        for fam in self.families.values():
            if fam.claim_id not in self.claims:
                raise ValueError(f"family {fam.family_id} references unknown claim")
            for e in fam.evidence_ids:
                if e not in self.evidence:
                    raise ValueError(f"family {fam.family_id} references unknown evidence {e}")
            for p in fam.prerequisite_ids:
                if p not in self.claims:
                    raise ValueError(f"family {fam.family_id} references unknown prerequisite {p}")
        for ev in self.evidence.values():
            if ev.source_id not in self.sources:
                raise ValueError(f"evidence {ev.evidence_id} references unknown source")
            if ev.calibration_id and ev.calibration_id not in self.calibrations:
                raise ValueError(f"evidence {ev.evidence_id} references unknown calibration")
            if ev.evaluator_id and ev.evaluator_id not in self.evaluators:
                raise ValueError(f"evidence {ev.evidence_id} references unknown evaluator")
        # prerequisite graph must be acyclic (scientific support is a DAG by construction)
        order = self.prerequisite_topological_order()
        if len(order) != len(self.claims):
            raise ValueError("prerequisite graph contains a cycle")

    def prerequisite_topological_order(self) -> tuple[str, ...]:
        prereqs = {c: set() for c in self.claims}
        for fam in self.families.values():
            prereqs[fam.claim_id].update(fam.prerequisite_ids)
        order: list[str] = []
        done: set[str] = set()
        while True:
            ready = sorted(c for c in self.claims if c not in done and prereqs[c] <= done)
            if not ready:
                break
            order.extend(ready)
            done.update(ready)
        return tuple(order)


def apply_event(world: World, event: Event) -> World:
    """Registered update of the support graph. Pure registry semantics: this
    function records what the event *says*; it never decides what is
    reopened."""
    w = world.copy()
    p = event.payload
    k = event.kind
    if k == "SOURCE_RETRACTED":
        w.sources[p["source_id"]] = SOURCE_RETRACTED
    elif k == "SOURCE_RETRACTION_DISPUTED":
        w.sources[p["source_id"]] = SOURCE_DISPUTED
    elif k == "SOURCE_CORRECTED":
        w.sources[p["source_id"]] = SOURCE_VALID
    elif k == "CALIBRATION_INVALIDATED":
        w.calibrations[p["calibration_id"]].status = CAL_INVALID
    elif k == "CALIBRATION_UNDER_REVIEW":
        w.calibrations[p["calibration_id"]].status = CAL_UNDER_REVIEW
    elif k == "CALIBRATION_REVALIDATED":
        w.calibrations[p["calibration_id"]].status = CAL_VALID
    elif k in ("DEPENDENCE_DISCOVERED", "DEPENDENCE_SUSPECTED"):
        status = DEP_CONFIRMED if k == "DEPENDENCE_DISCOVERED" else DEP_SUSPECTED
        w.dependence = [d for d in w.dependence if {d.left_id, d.right_id} != {p["left_id"], p["right_id"]}]
        w.dependence.append(DependenceDeclaration(p["left_id"], p["right_id"], p["kind"], status))
    elif k == "RELATION_RETYPED":
        key = w.relation_key(p["source_context"], p["target_context"])
        w.relations[key] = Relation(p["source_context"], p["target_context"], p["relation_type"])
    elif k == "EVALUATOR_COVERAGE_CHANGED":
        w.evaluators[p["evaluator_id"]] = Evaluator(p["evaluator_id"], tuple(p["coverage"]), tuple(p.get("uncertain", ())))
    elif k == "CLAIM_FAILURE_CLASS_CHANGED":
        w.claims[p["claim_id"]].failure_class = p["failure_class"]
    elif k == "CLAIM_SCOPE_CHANGED":
        w.claims[p["claim_id"]].scope = tuple(p["scope"])
    elif k == "FAMILY_ADDED":
        fam = Family(**p["family"])
        fam.evidence_ids = tuple(fam.evidence_ids)
        fam.prerequisite_ids = tuple(fam.prerequisite_ids)
        for ev in p.get("evidence", ()):
            e = Evidence(**ev)
            e.scope_coverage = tuple(e.scope_coverage)
            w.evidence[e.evidence_id] = e
        w.families[fam.family_id] = fam
    elif k == "EVIDENCE_ADDED":
        e = Evidence(**p["evidence"])
        e.scope_coverage = tuple(e.scope_coverage)
        w.evidence[e.evidence_id] = e
    else:
        raise ValueError(f"unknown event kind {k}")
    w.validate()
    return w


@dataclass
class Instance:
    instance_id: str
    stratum: str
    split: str
    seed: int
    world_v0: World
    events: list[Event]
    features: dict[str, Any] = field(default_factory=dict)


# ---- JSON (de)serialisation -------------------------------------------------

def world_to_json(w: World) -> dict[str, Any]:
    return {
        "claims": {k: asdict(v) for k, v in sorted(w.claims.items())},
        "evidence": {k: asdict(v) for k, v in sorted(w.evidence.items())},
        "families": {k: asdict(v) for k, v in sorted(w.families.items())},
        "sources": dict(sorted(w.sources.items())),
        "calibrations": {k: asdict(v) for k, v in sorted(w.calibrations.items())},
        "evaluators": {k: asdict(v) for k, v in sorted(w.evaluators.items())},
        "relations": {k: asdict(v) for k, v in sorted(w.relations.items())},
        "dependence": [asdict(d) for d in w.dependence],
    }


def world_from_json(d: dict[str, Any]) -> World:
    w = World()
    for k, v in d["claims"].items():
        v = dict(v); v["scope"] = tuple(v["scope"]); w.claims[k] = Claim(**v)
    for k, v in d["evidence"].items():
        v = dict(v); v["scope_coverage"] = tuple(v["scope_coverage"]); w.evidence[k] = Evidence(**v)
    for k, v in d["families"].items():
        v = dict(v); v["evidence_ids"] = tuple(v["evidence_ids"]); v["prerequisite_ids"] = tuple(v["prerequisite_ids"]); w.families[k] = Family(**v)
    w.sources = dict(d["sources"])
    for k, v in d["calibrations"].items():
        w.calibrations[k] = Calibration(**v)
    for k, v in d["evaluators"].items():
        v = dict(v); v["coverage"] = tuple(v["coverage"]); v["uncertain"] = tuple(v.get("uncertain", ())); w.evaluators[k] = Evaluator(**v)
    for k, v in d["relations"].items():
        w.relations[k] = Relation(**v)
    w.dependence = [DependenceDeclaration(**x) for x in d["dependence"]]
    w.validate()
    return w


def instance_to_json(inst: Instance) -> dict[str, Any]:
    return {
        "instance_id": inst.instance_id,
        "stratum": inst.stratum,
        "split": inst.split,
        "seed": inst.seed,
        "world_v0": world_to_json(inst.world_v0),
        "events": [asdict(e) for e in inst.events],
        "features": inst.features,
    }


def instance_from_json(d: dict[str, Any]) -> Instance:
    return Instance(d["instance_id"], d["stratum"], d["split"], d["seed"], world_from_json(d["world_v0"]), [Event(**e) for e in d["events"]], dict(d.get("features", {})))


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
