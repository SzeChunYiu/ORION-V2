"""ME-X7 — claim-sufficient external witnesses: frozen episode model.

An *episode* is one machine-produced scientific result offered for an external
audit.  The registry it lives in is fully explicit here; every arm sees a
*projection* of it (a witness surface, `mex7_arms`), and the exact oracle
(`mex7_oracle`) recomputes the audit verdict from the whole structure.

Nothing in this module knows the planted defect class: the stratum label lives
on the `Instance`, never inside the episode a surface can export.  The schema
test in `tests/unit/test_me_x7_exact_study.py` asserts that.

Zero model calls; deterministic; no ORION module is imported here (the arms do
that).  Protocol: `ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_PROTOCOL_V1.md` §2–§10 and
`MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§2, §9.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

# ---- registered vocabularies (frozen) ---------------------------------------

MODE_FORMAL = "MODE_FORMAL"
MODE_COMPUTATIONAL = "MODE_COMPUTATIONAL"
MODES = (MODE_FORMAL, MODE_COMPUTATIONAL)

# Protocol §5 failure injections, in the frozen check order used by the
# adjudication rule (first INVALID check in this order names the class).
INJECTION_CLASSES = (
    "WRONG_PROBLEM_OR_SPECIFICATION",
    "STALE_OR_WRONG_SOURCE",
    "HIDDEN_DEPENDENCE",
    "CODE_OR_PROOF_MISMATCH",
    "SEED_OR_VERSION_MISMATCH",
    "INVALID_CALIBRATION",
    "INVALID_TRANSPORT",
    "OMITTED_FAILED_ROUTE",
    "EVALUATOR_BLIND_SPOT",
    "AUTHORITY_OVERREACH",
    "REPRESENTATION_CHANGE_LOSES_INFORMATION",
)

CONTROL_STRATA = ("NO_DEFECT_WARRANTED", "CENSORED_UNDECIDABLE")
STRATA = INJECTION_CLASSES + CONTROL_STRATA

# Mode applicability, frozen in the design.  A (stratum, mode) cell that is not
# applicable is generated zero times and every per-cell count is reported with
# its `n_evaluated`, so "0 violations" can never be read as "checked and fine".
NOT_APPLICABLE_CELLS = {("INVALID_CALIBRATION", MODE_FORMAL)}


def cell_applicable(stratum: str, mode: str) -> bool:
    return (stratum, mode) not in NOT_APPLICABLE_CELLS


CELLS = tuple(
    (s, m) for s in STRATA for m in MODES if cell_applicable(s, m)
)

# Audit verdicts (finite, registered).
ACCEPT = "ACCEPT"
REJECT = "REJECT"
CANNOT_CHECK = "CANNOT_CHECK"
VERDICTS = (ACCEPT, REJECT, CANNOT_CHECK)

# Check statuses.
VALID = "VALID"
INVALID = "INVALID"
CENSORED = "CENSORED"
NOT_APPLICABLE = "NOT_APPLICABLE"

# Witness fields (protocol §2).  A surface is a subset of these; a check is
# runnable iff all of its required fields are present.
F_RESULT = "RESULT"
F_PROVENANCE = "PROVENANCE"
F_PROBLEM_BINDING = "PROBLEM_BINDING"
F_ARTIFACT = "ARTIFACT"
F_ASSUMPTION_VERSION = "ASSUMPTION_VERSION"
F_MEASUREMENT_CALIBRATION = "MEASUREMENT_CALIBRATION"
F_TRANSPORT_RELATION = "TRANSPORT_RELATION"
F_DEPENDENCE = "DEPENDENCE"
F_EVALUATOR_CONTRACT = "EVALUATOR_CONTRACT"
F_PRESERVATION = "PRESERVATION"
F_ROUTE_LEDGER = "ROUTE_LEDGER"
F_AUTHORITY_CEILING = "AUTHORITY_CEILING"

FIELDS = (
    F_RESULT,
    F_PROVENANCE,
    F_PROBLEM_BINDING,
    F_ARTIFACT,
    F_ASSUMPTION_VERSION,
    F_MEASUREMENT_CALIBRATION,
    F_TRANSPORT_RELATION,
    F_DEPENDENCE,
    F_EVALUATOR_CONTRACT,
    F_PRESERVATION,
    F_ROUTE_LEDGER,
    F_AUTHORITY_CEILING,
)

# Checks, in frozen order; each is a bijection onto one injection class.
CHECKS = (
    "C_SPEC_BINDING",
    "C_SOURCE_STATUS",
    "C_DEPENDENCE",
    "C_ARTIFACT_DIGEST",
    "C_ENV_IDENTITY",
    "C_CALIBRATION",
    "C_TRANSPORT",
    "C_ROUTE_COMPLETENESS",
    "C_EVALUATOR_COVERAGE",
    "C_AUTHORITY",
    "C_PRESERVATION",
)

CLASS_FOR_CHECK = dict(zip(CHECKS, INJECTION_CLASSES))
CHECK_FOR_CLASS = {v: k for k, v in CLASS_FOR_CHECK.items()}

# Required fields per check (frozen).  `C_ROUTE_COMPLETENESS` needs two: an
# omission is only detectable when an independent execution count (the
# artifact's log) can be compared with the declared ledger (design §9(3)).
REQUIRED_FIELDS = {
    "C_SPEC_BINDING": (F_PROBLEM_BINDING,),
    "C_SOURCE_STATUS": (F_PROVENANCE,),
    "C_DEPENDENCE": (F_DEPENDENCE,),
    "C_ARTIFACT_DIGEST": (F_ARTIFACT,),
    "C_ENV_IDENTITY": (F_ASSUMPTION_VERSION,),
    "C_CALIBRATION": (F_MEASUREMENT_CALIBRATION,),
    "C_TRANSPORT": (F_TRANSPORT_RELATION,),
    "C_ROUTE_COMPLETENESS": (F_ROUTE_LEDGER, F_ARTIFACT),
    "C_EVALUATOR_COVERAGE": (F_EVALUATOR_CONTRACT,),
    "C_AUTHORITY": (F_AUTHORITY_CEILING,),
    "C_PRESERVATION": (F_PRESERVATION,),
}

# Which omission ablation is predicted to break which class (design §6, G3).
FIELD_FOR_CLASS = {
    "WRONG_PROBLEM_OR_SPECIFICATION": F_PROBLEM_BINDING,
    "STALE_OR_WRONG_SOURCE": F_PROVENANCE,
    "HIDDEN_DEPENDENCE": F_DEPENDENCE,
    "CODE_OR_PROOF_MISMATCH": F_ARTIFACT,
    "SEED_OR_VERSION_MISMATCH": F_ASSUMPTION_VERSION,
    "INVALID_CALIBRATION": F_MEASUREMENT_CALIBRATION,
    "INVALID_TRANSPORT": F_TRANSPORT_RELATION,
    "OMITTED_FAILED_ROUTE": F_ROUTE_LEDGER,
    "EVALUATOR_BLIND_SPOT": F_EVALUATOR_CONTRACT,
    "AUTHORITY_OVERREACH": F_AUTHORITY_CEILING,
    "REPRESENTATION_CHANGE_LOSES_INFORMATION": F_PRESERVATION,
}

# Provenance node statuses.
NODE_VALID = "VALID"
NODE_RETRACTED = "RETRACTED"
NODE_SUPERSEDED = "SUPERSEDED"
NODE_DISPUTED = "DISPUTED"

CAL_VALID = "VALID"
CAL_INVALID = "INVALID"
CAL_UNDER_REVIEW = "UNDER_REVIEW"

# Typed context relation strength (identical order to ME-X4 §2.3).
RELATION_RANK = {
    "ISOMORPHIC": 5,
    "BEHAVIORALLY_EQUIVALENT": 4,
    "PREDICTIVELY_EQUIVALENT": 3,
    "DECISION_DOMINATES": 2,
    "APPROXIMATELY_EQUIVALENT": 1,
    "INCOMPARABLE": 0,
    "DISTINGUISHED_BY": 0,
}
RELATION_CANNOT_CHECK = "CANNOT_CHECK"

# Defect loci (where in the registry the planted defect lives).
LOCUS_DIRECT = "DIRECT"
LOCUS_TRANSITIVE = "TRANSITIVE_ANCESTOR"
LOCUS_UNDECLARED = "UNDECLARED_SHARED_UPSTREAM"
LOCI = (LOCUS_DIRECT, LOCUS_TRANSITIVE, LOCUS_UNDECLARED)


# ---- episode structure -------------------------------------------------------

@dataclass(frozen=True)
class Node:
    """A provenance registry node: a source, dataset, model or instrument.

    `declared` is False when the producing system never recorded the node, so
    no witness the system emits can mention it; only a full-registry audit
    reaches it.  `suspected_parent` marks an ancestry edge that is registered
    but unconfirmed (a censoring channel for dependence).
    """
    node_id: str
    kind: str
    status: str = NODE_VALID
    parents: tuple[str, ...] = ()
    declared: bool = True
    suspected_parent: bool = False


@dataclass(frozen=True)
class Support:
    support_id: str
    root_node_ids: tuple[str, ...]
    evaluator_id: str
    context_id: str
    calibration_id: str = ""


@dataclass(frozen=True)
class Evaluator:
    evaluator_id: str
    coverage: tuple[str, ...]
    uncertain: tuple[str, ...] = ()


@dataclass(frozen=True)
class Artifact:
    """The executable proof or program that produced the reported result.

    `declared_digest` is what the witness/certificate advertises;
    `actual_digest` is the digest of the artifact that in fact ran.
    `checker_target` is the statement the checker verified (formal mode) or the
    output the replay produced (computational mode).
    """
    artifact_id: str
    kind: str                       # PROOF | PROGRAM
    declared_digest: str
    actual_digest: str
    checker_accepts: bool
    checker_target: str
    recorded_env: str
    actual_env: str
    recorded_seed: str
    actual_seed: str
    attempted_route_count: int
    payload: str = ""               # serialized proof / program text


@dataclass(frozen=True)
class Route:
    route_id: str
    outcome: str                    # SUCCEEDED | FAILED
    registered: bool


@dataclass(frozen=True)
class Representation:
    """A registered representation change with its correspondence evidence."""
    link_ids: tuple[str, ...]
    source_epoch: str
    target_epoch: str
    required_invariant_ids: tuple[str, ...]
    preserved_invariant_ids: tuple[str, ...]
    violated_invariant_ids: tuple[str, ...] = ()
    unresolved_invariant_ids: tuple[str, ...] = ()
    mapping_ids: tuple[str, ...] = ("map0",)
    anchor_ids: tuple[str, ...] = ("anchor0",)
    uncertainty: float = 0.0
    tolerance: float = 0.5
    exact: bool = True


@dataclass(frozen=True)
class Contract:
    problem_id: str
    target: str
    decision_class: str
    scope: tuple[str, ...]
    intended_question_digest: str
    replay_required: bool
    requested_authority_level: int
    authority_ceiling: int
    decision_relevant_classes: tuple[str, ...]


@dataclass(frozen=True)
class Claim:
    claim_id: str
    context_id: str
    asserted_failure_class: str
    formalization_digest: str
    result_digest: str


@dataclass(frozen=True)
class Episode:
    episode_id: str
    mode: str
    claim: Claim
    contract: Contract
    supports: tuple[Support, ...]
    nodes: tuple[Node, ...]
    evaluators: tuple[Evaluator, ...]
    calibrations: tuple[tuple[str, str], ...]
    relations: tuple[tuple[str, str, str], ...]     # (src_ctx, tgt_ctx, relation)
    required_relation: str
    independence_k: int
    artifact: Artifact | None
    routes: tuple[Route, ...]
    representation: Representation | None
    internal_steps: tuple[str, ...]

    # -- lookups ---------------------------------------------------------
    def node(self, node_id: str) -> Node:
        for n in self.nodes:
            if n.node_id == node_id:
                return n
        raise KeyError(node_id)

    def node_ids(self) -> tuple[str, ...]:
        return tuple(n.node_id for n in self.nodes)

    def evaluator(self, evaluator_id: str) -> Evaluator:
        for e in self.evaluators:
            if e.evaluator_id == evaluator_id:
                return e
        raise KeyError(evaluator_id)

    def calibration_status(self, calibration_id: str) -> str:
        for cid, status in self.calibrations:
            if cid == calibration_id:
                return status
        raise KeyError(calibration_id)

    def relation(self, src_ctx: str, tgt_ctx: str) -> str | None:
        for a, b, rel in self.relations:
            if a == src_ctx and b == tgt_ctx:
                return rel
        return None

    def ancestry(self, node_id: str, *, visible: frozenset[str]) -> set[str]:
        """Transitive ancestor closure of `node_id` restricted to `visible`."""
        seen: set[str] = set()
        stack = [node_id]
        while stack:
            cur = stack.pop()
            if cur in seen or cur not in visible:
                continue
            seen.add(cur)
            stack.extend(self.node(cur).parents)
        return seen

    def declared_node_ids(self) -> frozenset[str]:
        """Nodes a witness emitted by the producing system can name: the
        supports' declared roots plus their declared ancestry."""
        allv = frozenset(self.node_ids())
        out: set[str] = set()
        for s in self.supports:
            for root in s.root_node_ids:
                for nid in self.ancestry(root, visible=allv):
                    if self.node(nid).declared:
                        out.add(nid)
        return frozenset(out)


@dataclass(frozen=True)
class Instance:
    """One generated study case.  `stratum` and `locus` are labels for scoring;
    they never enter an episode and no arm receives them."""
    instance_id: str
    stratum: str
    mode: str
    locus: str
    episode: Episode
    facts: tuple[tuple[str, str], ...] = ()   # generator bookkeeping


# ---- serialization -----------------------------------------------------------

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def episode_to_json(ep: Episode) -> dict[str, Any]:
    return asdict(ep)


def _tuples(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_tuples(v) for v in value)
    return value


def episode_from_json(data: dict[str, Any]) -> Episode:
    d = dict(data)
    d["claim"] = Claim(**d["claim"])
    d["contract"] = Contract(
        **{k: (tuple(v) if isinstance(v, list) else v) for k, v in d["contract"].items()}
    )
    d["supports"] = tuple(
        Support(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in s.items()})
        for s in d["supports"]
    )
    d["nodes"] = tuple(
        Node(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in n.items()})
        for n in d["nodes"]
    )
    d["evaluators"] = tuple(
        Evaluator(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in e.items()})
        for e in d["evaluators"]
    )
    d["calibrations"] = tuple(tuple(x) for x in d["calibrations"])
    d["relations"] = tuple(tuple(x) for x in d["relations"])
    d["artifact"] = Artifact(**d["artifact"]) if d["artifact"] else None
    d["routes"] = tuple(Route(**r) for r in d["routes"])
    if d["representation"]:
        d["representation"] = Representation(
            **{k: (tuple(v) if isinstance(v, list) else v) for k, v in d["representation"].items()}
        )
    d["internal_steps"] = tuple(d["internal_steps"])
    return Episode(**d)


def instance_to_json(inst: Instance) -> dict[str, Any]:
    return {
        "instance_id": inst.instance_id,
        "stratum": inst.stratum,
        "mode": inst.mode,
        "locus": inst.locus,
        "facts": [list(x) for x in inst.facts],
        "episode": episode_to_json(inst.episode),
    }


def instance_from_json(data: dict[str, Any]) -> Instance:
    return Instance(
        instance_id=data["instance_id"],
        stratum=data["stratum"],
        mode=data["mode"],
        locus=data["locus"],
        facts=tuple(tuple(x) for x in data["facts"]),
        episode=episode_from_json(data["episode"]),
    )
