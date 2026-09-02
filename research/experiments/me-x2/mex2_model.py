"""ME-X2 exact study: registered objects (frozen with design V1).

An *instance* is a registered scientific episode: a symptom shared by a pair,
a live set of cause hypotheses (each carrying its obstruction class and its
discrepancy locus), diagnostic probes with exact registered outcome tables,
candidate interventions with a Jump level, a cost and a registered
``resolves`` set, and a total budget.  The true cause is hidden from every
arm; only the environment (``mex2_oracle.Environment``) reads it.

Nothing here is authorizing.  Class/locus/level vocabularies are those of
``MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md`` S4.2/S4.3,
``ME_X2_LOCUS_DIAGNOSIS_PROTOCOL_V2.md`` axis A/B and
``src/orion_v2/ontic_epistemic_boundary.py``.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

# ---- registered vocabularies ------------------------------------------------------------

CLASSES: tuple[str, ...] = (
    "SEARCH_INSUFFICIENT",
    "MISSING_PREMISE_OR_DATA",
    "MODEL_FAMILY_INADEQUATE",
    "REPRESENTATION_INSUFFICIENT",
    "PROBE_ACTION_INSUFFICIENT",
    "MEASUREMENT_OR_EVALUATOR_BLIND",
    "FORMALISM_OR_OPERATOR_INSUFFICIENT",
    "PROBLEM_OBJECTIVE_MISSPECIFIED",
    "TOOL_INSTRUMENT_INADEQUATE",
    "WORKFLOW_INADEQUATE",
    "NO_ESCALATION_NEEDED",
    "CANNOT_IDENTIFY",
)
STRATA: tuple[str, ...] = CLASSES  # stratum = oracle obstruction class

LOCI: tuple[str, ...] = (
    "TARGET_WORLD",
    "OBSERVATION_MEASUREMENT",
    "EPISTEMIC_MODEL",
    "REPRESENTATION_REGIME",
    "PROBLEM_CRITERION",
    "EVALUATOR_VALIDATION",
    "PROCESS_TOOL_WORKFLOW",
    "NO_MATERIAL_DISCREPANCY",
    "CANNOT_IDENTIFY",
)

LEVEL_NAMES: dict[int, str] = {
    0: "ACTION_PARAMETER",
    1: "LOCAL_REPAIR_COMPOSITION",
    2: "MODEL_HYPOTHESIS_EXPANSION",
    3: "REPRESENTATION_REGIME_TRANSITION",
    4: "PROBLEM_OBJECTIVE_REFORMULATION",
    5: "METHOD_TOOL_INSTRUMENT_INVENTION",
    6: "WORKFLOW_META_SKILL_REVISION",
}

# class-typical minimal level (used by the taxonomy arm and for decoy bookkeeping only;
# the oracle level is registered per instance from the resolves sets, never from this table)
TYPICAL_LEVEL: dict[str, int | None] = {
    "SEARCH_INSUFFICIENT": 0,
    "MISSING_PREMISE_OR_DATA": 1,
    "MODEL_FAMILY_INADEQUATE": 2,
    "REPRESENTATION_INSUFFICIENT": 3,
    "PROBE_ACTION_INSUFFICIENT": 0,
    "MEASUREMENT_OR_EVALUATOR_BLIND": 5,
    "FORMALISM_OR_OPERATOR_INSUFFICIENT": 3,
    "PROBLEM_OBJECTIVE_MISSPECIFIED": 4,
    "TOOL_INSTRUMENT_INADEQUATE": 5,
    "WORKFLOW_INADEQUATE": 6,
    "NO_ESCALATION_NEEDED": 0,
    "CANNOT_IDENTIFY": None,
}

# strictly increasing cost bands per level (so the minimum-cost resolving intervention is the
# minimum-level one; frozen)
LEVEL_COST_BANDS: dict[int, tuple[int, int]] = {0: (1, 2), 1: (3, 4), 2: (5, 8), 3: (9, 12), 4: (13, 16), 5: (17, 22), 6: (23, 30)}
PROBE_COST_RANGE: tuple[int, int] = (1, 6)
MAX_PROBES = 7
MAX_CHEAP_INTERVENTIONS = 5  # level <= 1 interventions usable as repair-as-test discriminators

SUCCESS = "SUCCESS"
RECURRENCE = "RECURRENCE"


# ---- registered objects -----------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Cause:
    cause_id: str
    obstruction_class: str
    locus: str
    typical_fix: str  # intervention kind that is this cause's canonical minimal repair

    def __post_init__(self) -> None:
        if self.obstruction_class not in CLASSES or self.obstruction_class == "CANNOT_IDENTIFY":
            raise ValueError(f"cause class must be a registered non-CANNOT_IDENTIFY class: {self.obstruction_class}")
        if self.locus not in LOCI or self.locus == "CANNOT_IDENTIFY":
            raise ValueError(f"cause locus must be a registered locus: {self.locus}")


@dataclass(frozen=True, slots=True)
class Probe:
    probe_id: str
    cost: int
    evaluator_mediated: bool
    nominal: str
    table: dict[str, str]  # cause_id -> outcome symbol (effective table; registered, visible to arms)
    designed_table: dict[str, str] | None = None  # pre-laundering table (what the probe's module believes it measures)

    def __post_init__(self) -> None:
        if self.designed_table is None:
            object.__setattr__(self, "designed_table", dict(self.table))

    def outcome(self, cause_id: str) -> str:
        return self.table.get(cause_id, self.nominal)

    def designed_outcome(self, cause_id: str) -> str:
        return self.designed_table.get(cause_id, self.nominal)

    def splits(self, live: tuple[str, ...]) -> bool:
        return len({self.outcome(c) for c in live}) > 1


@dataclass(frozen=True, slots=True)
class Intervention:
    intervention_id: str
    kind: str
    level: int
    cost: int
    resolves: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.level not in LEVEL_NAMES:
            raise ValueError("intervention level outside the registered lattice 0-6")
        lo, hi = LEVEL_COST_BANDS[self.level]
        if not lo <= self.cost <= hi:
            raise ValueError(f"intervention cost {self.cost} outside band {lo}-{hi} for level {self.level}")

    def outcome(self, cause_id: str) -> str:
        return SUCCESS if cause_id in self.resolves else RECURRENCE

    @property
    def is_cheap(self) -> bool:
        return self.level <= 1


@dataclass(frozen=True, slots=True)
class Instance:
    instance_id: str
    pair_id: str
    partner_instance_id: str
    template: str
    seed: str
    variant: str
    symptom: str
    pattern: str  # trajectory pattern label (ARFT-equivalent taxonomy input)
    apparent_class: str
    causes: tuple[Cause, ...]
    probes: tuple[Probe, ...]
    interventions: tuple[Intervention, ...]
    budget: int
    truth: str  # hidden from arms
    features: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ids = [c.cause_id for c in self.causes]
        if len(ids) != len(set(ids)) or self.truth not in ids:
            raise ValueError("instance causes must be unique and contain the truth")
        if len(self.probes) > MAX_PROBES:
            raise ValueError("too many probes")
        if len([i for i in self.interventions if i.is_cheap]) > MAX_CHEAP_INTERVENTIONS:
            raise ValueError("too many cheap interventions")
        if self.apparent_class not in CLASSES:
            raise ValueError("apparent class must be registered")

    def cause(self, cause_id: str) -> Cause:
        for c in self.causes:
            if c.cause_id == cause_id:
                return c
        raise KeyError(cause_id)

    def probe(self, probe_id: str) -> Probe:
        for p in self.probes:
            if p.probe_id == probe_id:
                return p
        raise KeyError(probe_id)

    def intervention(self, intervention_id: str) -> Intervention:
        for i in self.interventions:
            if i.intervention_id == intervention_id:
                return i
        raise KeyError(intervention_id)

    def live_ids(self) -> tuple[str, ...]:
        return tuple(c.cause_id for c in self.causes)

    def min_fix(self, cause_id: str) -> Intervention | None:
        """Minimum-level (hence minimum-cost) registered intervention resolving ``cause_id``."""
        cands = [i for i in self.interventions if cause_id in i.resolves]
        if not cands:
            return None
        return min(cands, key=lambda i: (i.level, i.cost, i.intervention_id))


# ---- actions and history (shared by environment and arms) -------------------------------

@dataclass(frozen=True, slots=True)
class Action:
    kind: str  # PROBE | INTERVENE | DECLARE_CANNOT_IDENTIFY | STOP
    target: str | None = None
    declared_class: str | None = None
    declared_locus: str | None = None
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class Step:
    action: Action
    outcome: str | None
    cost: int


# ---- JSON ----------------------------------------------------------------------------------

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def instance_to_json(inst: Instance, *, include_truth: bool = True) -> dict:
    d = {
        "instance_id": inst.instance_id, "pair_id": inst.pair_id, "partner_instance_id": inst.partner_instance_id,
        "template": inst.template, "seed": inst.seed, "variant": inst.variant, "symptom": inst.symptom, "pattern": inst.pattern,
        "apparent_class": inst.apparent_class,
        "causes": [{"cause_id": c.cause_id, "obstruction_class": c.obstruction_class, "locus": c.locus, "typical_fix": c.typical_fix} for c in inst.causes],
        "probes": [{"probe_id": p.probe_id, "cost": p.cost, "evaluator_mediated": p.evaluator_mediated, "nominal": p.nominal, "table": dict(sorted(p.table.items())), "designed_table": dict(sorted(p.designed_table.items()))} for p in inst.probes],
        "interventions": [{"intervention_id": i.intervention_id, "kind": i.kind, "level": i.level, "cost": i.cost, "resolves": list(i.resolves)} for i in inst.interventions],
        "budget": inst.budget, "features": inst.features,
    }
    if include_truth:
        d["truth"] = inst.truth
    return d


def instance_from_json(d: dict) -> Instance:
    return Instance(
        instance_id=d["instance_id"], pair_id=d["pair_id"], partner_instance_id=d["partner_instance_id"], template=d["template"], seed=d["seed"],
        variant=d["variant"], symptom=d["symptom"], pattern=d["pattern"], apparent_class=d["apparent_class"],
        causes=tuple(Cause(**c) for c in d["causes"]),
        probes=tuple(Probe(p["probe_id"], p["cost"], p["evaluator_mediated"], p["nominal"], dict(p["table"]), dict(p.get("designed_table", p["table"]))) for p in d["probes"]),
        interventions=tuple(Intervention(i["intervention_id"], i["kind"], i["level"], i["cost"], tuple(i["resolves"])) for i in d["interventions"]),
        budget=d["budget"], truth=d["truth"], features=dict(d.get("features", {})),
    )
