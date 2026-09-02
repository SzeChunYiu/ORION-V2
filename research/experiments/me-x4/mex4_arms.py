#!/usr/bin/env python3
"""ME-X4 arms (frozen with design V1, §4 and H-EXT-3 ladder).

Every arm receives the SAME registered information (the World at each
version, the event history, the accepted-commitment list). Arms differ in
(i) which analysis modules interpret the typed information and how
(typed vs untyped), (ii) what crosses the module boundary into the
propagation engine (verdict-level vs witness-level; the B5 ladder), and
(iii) the propagation engine itself (JTMS / ATMS / kernel contraction /
noisy-OR / assurance impact / provenance descendants / orion selective_reopen).

No arm imports mex4_oracle.
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable

from mex4_model import (
    CAL_INVALID, CAL_UNDER_REVIEW, DEP_CONFIRMED, DEP_SUSPECTED, RELATION_CANNOT_CHECK, RELATION_RANK,
    SOURCE_DISPUTED, SOURCE_RETRACTED, STATUS_INVALID, STATUS_UNKNOWN, STATUS_VALID, Event, Family, World,
)
from mex4_parents import ATMS, JTMS, AssuranceCase, KernelBase, NoisyOrSupport, ProvenanceOnly, Rule
from orion_v2.contracts import ProblemContract
from orion_v2.evidence import DependenceEdge, DependenceKind, EvidenceUnit, assess_evidence_dependence
from orion_v2.provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance
from orion_v2.reopening import Commitment, CommitmentDisposition, SupportFamily, selective_reopen
from orion_v2.structural import RelationType

PRESERVED, REOPENED, UNRESOLVED = "PRESERVED", "REOPENED", "UNRESOLVED"
MODULES = ("PROV", "DEP", "TRANS", "EVAL", "SCOPE", "CONTRA")


@dataclass
class ArmView:
    world_v0: World
    world: World
    events: list[Event]
    accepted: tuple[str, ...]


# ---- registered condition slots (structure, not status) ---------------------

def condition_slots(w: World) -> dict[str, list[tuple[str, str]]]:
    """family_id -> [(atom_id, owning module)]. The slot set is a pure
    function of the registered family (evidence ids, evaluator ids, contexts,
    independence requirement, own evidence for scope)."""
    slots: dict[str, list[tuple[str, str]]] = {}
    for fam in sorted(w.families.values(), key=lambda f: f.family_id):
        s: list[tuple[str, str]] = []
        pos = [w.evidence[e] for e in fam.evidence_ids if w.evidence[e].supports]
        for e in pos:
            s.append((f"ev:{e.evidence_id}", "PROV"))
            if e.evaluator_id:
                s.append((f"evc:{e.evidence_id}", "EVAL"))
            if e.context_id != w.claims[fam.claim_id].context_id:
                s.append((f"tr:{fam.family_id}:{e.evidence_id}", "TRANS"))
        if fam.min_independent > 0:
            s.append((f"ind:{fam.family_id}", "DEP"))
        if pos:
            s.append((f"scope:{fam.family_id}", "SCOPE"))
        slots[fam.family_id] = s
    return slots


def contra_slot(c: str) -> str:
    return f"nocontra:{c}"


# ---- analysis modules ----------------------------------------------------------
# Each returns {atom_id: status} for the atoms it owns. Unassigned atoms default
# to VALID ("no registered defeat").

def _provenance_graph(w: World) -> ReticulateProvenance:
    nodes = [ProvenanceNode(s, "source", "v0") for s in sorted(w.sources)]
    nodes += [ProvenanceNode(c, "calibration", "v0") for c in sorted(w.calibrations)]
    insts = sorted({c.instrument_id for c in w.calibrations.values()})
    nodes += [ProvenanceNode(i, "instrument", "v0") for i in insts]
    nodes += [ProvenanceNode(e, "evidence", "v0") for e in sorted(w.evidence)]
    edges = []
    for c in w.calibrations.values():
        edges.append(ProvenanceEdge(c.instrument_id, c.calibration_id, InheritanceRelation.CALIBRATES_FROM, "instrument"))
    for e in w.evidence.values():
        edges.append(ProvenanceEdge(e.source_id, e.evidence_id, InheritanceRelation.DERIVES, "source"))
        if e.calibration_id:
            edges.append(ProvenanceEdge(e.calibration_id, e.evidence_id, InheritanceRelation.CALIBRATES_FROM, "calibration"))
    return ReticulateProvenance(tuple(nodes), tuple(edges))


def prov_typed(v: ArmView, ops: dict) -> dict[str, str]:
    """Evidence validity through orion_v2.provenance revocation descendants."""
    w = v.world
    g = _provenance_graph(w)
    revoked = [s for s, st in w.sources.items() if st == SOURCE_RETRACTED] + [c for c, cal in w.calibrations.items() if cal.status == CAL_INVALID]
    disputed = [s for s, st in w.sources.items() if st == SOURCE_DISPUTED] + [c for c, cal in w.calibrations.items() if cal.status == CAL_UNDER_REVIEW]
    inv = set(g.descendants(tuple(revoked))) if revoked else set()
    unk = set(g.descendants(tuple(disputed))) if disputed else set()
    ops["n"] = ops.get("n", 0) + len(revoked) + len(disputed)
    out = {}
    for e in w.evidence:
        out[f"ev:{e}"] = STATUS_INVALID if e in inv else STATUS_UNKNOWN if e in unk else STATUS_VALID
    return out


def prov_direct(v: ArmView, ops: dict, *, two_valued: bool) -> dict[str, str]:
    """Direct-identity evidence status (source/calibration status looked up by
    id, no provenance graph). Two-valued parents treat DISPUTED/UNDER_REVIEW as
    not-retracted (policy: contract only on confirmed information)."""
    w = v.world
    out = {}
    for e in w.evidence.values():
        ops["n"] = ops.get("n", 0) + 1
        src = w.sources[e.source_id]; cal = w.calibrations[e.calibration_id].status if e.calibration_id else None
        if src == SOURCE_RETRACTED or cal == CAL_INVALID:
            out[f"ev:{e.evidence_id}"] = STATUS_INVALID
        elif src == SOURCE_DISPUTED or cal == CAL_UNDER_REVIEW:
            out[f"ev:{e.evidence_id}"] = STATUS_VALID if two_valued else STATUS_UNKNOWN
        else:
            out[f"ev:{e.evidence_id}"] = STATUS_VALID
    return out


def dep_typed(v: ArmView, ops: dict) -> dict[str, str]:
    """Independence witnesses through orion_v2.evidence.assess_evidence_dependence."""
    w = v.world
    out = {}
    for fam in w.families.values():
        if fam.min_independent <= 0:
            continue
        units = tuple(EvidenceUnit(e.evidence_id, fam.claim_id, e.source_id, "registered", e.data_id, e.model_id, e.instrument_id, True) for e in w.positive_evidence_of_family(fam))
        if not units:
            continue
        ids = {u.evidence_id for u in units}
        def edges(statuses):
            return tuple(DependenceEdge(d.left_id, d.right_id, DependenceKind(d.kind), ("registered",)) for d in w.dependence if d.status in statuses and d.left_id in ids and d.right_id in ids)
        ops["n"] = ops.get("n", 0) + 1
        confirmed = assess_evidence_dependence(units, edges({DEP_CONFIRMED})).conservative_independent_support_count
        with_suspected = assess_evidence_dependence(units, edges({DEP_CONFIRMED, DEP_SUSPECTED})).conservative_independent_support_count
        a = f"ind:{fam.family_id}"
        out[a] = STATUS_INVALID if confirmed < fam.min_independent else STATUS_UNKNOWN if with_suspected < fam.min_independent else STATUS_VALID
    return out


def dep_untyped(v: ArmView, ops: dict) -> dict[str, str]:
    return {}


def trans_typed(v: ArmView, ops: dict) -> dict[str, str]:
    w = v.world
    out = {}
    for fam in w.families.values():
        claim = w.claims[fam.claim_id]
        for e in w.positive_evidence_of_family(fam):
            if e.context_id == claim.context_id:
                continue
            ops["n"] = ops.get("n", 0) + 1
            a = f"tr:{fam.family_id}:{e.evidence_id}"
            rel = w.relations.get(w.relation_key(e.context_id, claim.context_id))
            if rel is None:
                out[a] = STATUS_INVALID; continue
            rt = RelationType(rel.relation_type)
            if rt is RelationType.CANNOT_CHECK:
                out[a] = STATUS_UNKNOWN; continue
            req = RelationType(fam.required_relation or "APPROXIMATELY_EQUIVALENT")
            out[a] = STATUS_VALID if RELATION_RANK[rt.value] >= RELATION_RANK[req.value] else STATUS_INVALID
    return out


def trans_untyped(v: ArmView, ops: dict, *, two_valued: bool) -> dict[str, str]:
    """Binary transport: any change of the relation since v0 defeats the witness."""
    w = v.world
    out = {}
    for fam in w.families.values():
        claim = w.claims[fam.claim_id]
        for e in w.positive_evidence_of_family(fam):
            if e.context_id == claim.context_id:
                continue
            ops["n"] = ops.get("n", 0) + 1
            key = w.relation_key(e.context_id, claim.context_id)
            now = w.relations.get(key); before = v.world_v0.relations.get(key)
            a = f"tr:{fam.family_id}:{e.evidence_id}"
            if now is None:
                out[a] = STATUS_INVALID
            elif now.relation_type == RELATION_CANNOT_CHECK:
                out[a] = STATUS_INVALID if two_valued else STATUS_UNKNOWN
            elif before is None or before.relation_type != now.relation_type:
                out[a] = STATUS_INVALID
            else:
                out[a] = STATUS_VALID
    return out


def eval_typed(v: ArmView, ops: dict) -> dict[str, str]:
    w = v.world
    out = {}
    for e in w.evidence.values():
        if not e.evaluator_id or not e.supports:
            continue
        ops["n"] = ops.get("n", 0) + 1
        fc = w.claims[e.claim_id].failure_class; ev = w.evaluators[e.evaluator_id]
        out[f"evc:{e.evidence_id}"] = STATUS_VALID if fc in ev.coverage else STATUS_UNKNOWN if fc in ev.uncertain else STATUS_INVALID
    return out


def eval_untyped(v: ArmView, ops: dict) -> dict[str, str]:
    """Evaluator identity semantics only: any coverage change of an evaluator
    (or failure-class change of a claim) defeats every evidence it evaluated."""
    w, w0 = v.world, v.world_v0
    out = {}
    for e in w.evidence.values():
        if not e.evaluator_id or not e.supports:
            continue
        ops["n"] = ops.get("n", 0) + 1
        ev_now = w.evaluators[e.evaluator_id]; ev_before = w0.evaluators.get(e.evaluator_id)
        changed = ev_before is None or set(ev_before.coverage) != set(ev_now.coverage) or set(ev_before.uncertain) != set(ev_now.uncertain)
        fc_changed = e.claim_id in w0.claims and w0.claims[e.claim_id].failure_class != w.claims[e.claim_id].failure_class
        out[f"evc:{e.evidence_id}"] = STATUS_INVALID if (changed or fc_changed) else STATUS_VALID
    return out


def scope_typed(v: ArmView, ops: dict) -> dict[str, str]:
    w = v.world
    out = {}
    for fam in w.families.values():
        pos = w.positive_evidence_of_family(fam)
        if not pos:
            continue
        ops["n"] = ops.get("n", 0) + 1
        claim = w.claims[fam.claim_id]
        contract = ProblemContract(problem_id=claim.claim_id, target="registered claim", decision_class="support", scope=tuple(claim.scope))
        cov = {s for e in pos for s in e.scope_coverage}
        out[f"scope:{fam.family_id}"] = STATUS_VALID if set(contract.scope) <= cov else STATUS_INVALID
    return out


def scope_untyped_noop(v: ArmView, ops: dict) -> dict[str, str]:
    return {}


def scope_untyped_context(v: ArmView, ops: dict) -> dict[str, str]:
    """Assurance-context semantics: a scope change challenges every family of the claim."""
    w, w0 = v.world, v.world_v0
    out = {}
    for fam in w.families.values():
        if not w.positive_evidence_of_family(fam):
            continue
        ops["n"] = ops.get("n", 0) + 1
        c = fam.claim_id
        changed = c in w0.claims and tuple(w0.claims[c].scope) != tuple(w.claims[c].scope)
        out[f"scope:{fam.family_id}"] = STATUS_INVALID if changed else STATUS_VALID
    return out


def contra_module(v: ArmView, ops: dict, ev_status: dict[str, str]) -> dict[str, str]:
    w = v.world
    out = {}
    for c in w.claims:
        vals = [ev_status.get(f"ev:{e.evidence_id}", STATUS_VALID) for e in w.negative_evidence_against(c)]
        ops["n"] = ops.get("n", 0) + 1
        out[contra_slot(c)] = STATUS_INVALID if any(x == STATUS_VALID for x in vals) else STATUS_UNKNOWN if any(x == STATUS_UNKNOWN for x in vals) else STATUS_VALID
    return out


# ---- structure = families with atom lists ---------------------------------------

@dataclass
class Structure:
    families: dict[str, tuple[str, tuple[str, ...], tuple[str, ...]]]  # fid -> (claim, atoms, prereqs)
    claim_atoms: dict[str, tuple[str, ...]]
    claims: tuple[str, ...]

    def key(self) -> tuple:
        return (tuple(sorted((f, c, a, p) for f, (c, a, p) in self.families.items())), tuple(sorted(self.claim_atoms.items())), self.claims)


def build_structure(w: World, slots: dict[str, list[tuple[str, str]]], *, merge_families: bool = False) -> Structure:
    fams: dict[str, tuple[str, tuple[str, ...], tuple[str, ...]]] = {}
    if merge_families:
        for c in w.claims:
            atoms: list[str] = []; prereqs: list[str] = []
            for fam in w.families_of(c):
                atoms += [a for a, _ in slots[fam.family_id]]; prereqs += list(fam.prerequisite_ids)
            fams[f"{c}.MERGED"] = (c, tuple(atoms), tuple(sorted(set(prereqs))))
    else:
        for fam in w.families.values():
            fams[fam.family_id] = (fam.claim_id, tuple(a for a, _ in slots[fam.family_id]), tuple(fam.prerequisite_ids))
    return Structure(fams, {c: (contra_slot(c),) for c in w.claims}, tuple(sorted(w.claims)))


def topo(struct: Structure) -> list[str]:
    prereqs = {c: set() for c in struct.claims}
    for cid, _a, p in struct.families.values():
        prereqs[cid].update(p)
    order: list[str] = []; done: set[str] = set()
    while len(order) < len(struct.claims):
        ready = sorted(c for c in struct.claims if c not in done and prereqs[c] <= done)
        if not ready:
            raise ValueError("cycle")
        order += ready; done.update(ready)
    return order


# ---- verdict-level compression (B5 ladder rungs 1-4) --------------------------------

def compress_module_to_verdicts(struct: Structure, slots: dict[str, list[tuple[str, str]]], status: dict[str, str], module: str) -> tuple[Structure, dict[str, str]]:
    """Replace module-owned witness atoms by one per-claim verdict atom
    verdict:<module>:<claim>, attached to every family of the claim.
    INVALID if the module defeats every family; UNKNOWN if it defeats-or-
    censors every family with at least one censored; VALID otherwise."""
    owned = {a for fid in slots for a, m in slots[fid] if m == module}
    new_fams = {}
    per_claim_fams: dict[str, list[str]] = {}
    for fid, (c, atoms, prereqs) in struct.families.items():
        per_claim_fams.setdefault(c, []).append(fid)
    new_status = {a: s for a, s in status.items() if a not in owned}
    for c in struct.claims:
        fam_ids = per_claim_fams.get(c, [])
        defeated = []; censored = []
        for fid in fam_ids:
            atoms = [a for a in struct.families[fid][1] if a in owned]
            defeated.append(any(status.get(a, STATUS_VALID) == STATUS_INVALID for a in atoms))
            censored.append(any(status.get(a, STATUS_VALID) == STATUS_UNKNOWN for a in atoms))
        va = f"verdict:{module}:{c}"
        if fam_ids and all(defeated):
            new_status[va] = STATUS_INVALID
        elif fam_ids and all(d or u for d, u in zip(defeated, censored)) and any(censored):
            new_status[va] = STATUS_UNKNOWN
        else:
            new_status[va] = STATUS_VALID
        for fid in fam_ids:
            cc, atoms, prereqs = struct.families[fid]
            new_fams[fid] = (cc, tuple(a for a in atoms if a not in owned) + (va,), prereqs)
    return Structure(new_fams, struct.claim_atoms, struct.claims), new_status


# ---- engines ----------------------------------------------------------------------

def engine_selective_reopen(struct: Structure, status: dict[str, str], accepted: tuple[str, ...], cost: dict) -> dict[str, str]:
    """M's propagation: orion_v2.reopening.selective_reopen, run twice
    (optimistic: censored = valid; pessimistic: censored = invalid)."""
    by_claim: dict[str, list[SupportFamily]] = {c: [] for c in struct.claims}
    for fid, (c, atoms, prereqs) in struct.families.items():
        by_claim[c].append(SupportFamily(fid, frozenset(atoms) | frozenset(struct.claim_atoms[c]), frozenset(prereqs)))
    commitments = tuple(Commitment(c, tuple(by_claim[c])) for c in struct.claims if by_claim[c])
    invalid = tuple(sorted(a for a, s in status.items() if s == STATUS_INVALID))
    unknown = tuple(sorted(a for a, s in status.items() if s == STATUS_UNKNOWN))
    opt = selective_reopen(commitments, invalid)
    pes = selective_reopen(commitments, invalid + unknown) if unknown else opt
    n_atoms = sum(len(f.evidence_ids) for c in commitments for f in c.support_families)
    cost["ops"] = cost.get("ops", 0) + (2 if unknown else 1) * (len(commitments) + n_atoms)
    out = {}
    pes_pres = set(pes.preserved_commitment_ids); opt_reop = set(opt.reopened_commitment_ids)
    for c in accepted:
        out[c] = PRESERVED if c in pes_pres else REOPENED if c in opt_reop else UNRESOLVED
    return out


class JTMSEngine:
    def __init__(self) -> None:
        self.tms: JTMS | None = None
        self.key = None
        self.enabled: set[str] = set()

    def _build(self, struct: Structure) -> None:
        t = JTMS()
        atoms = sorted({a for _c, at, _p in struct.families.values() for a in at} | {a for ats in struct.claim_atoms.values() for a in ats})
        for a in atoms:
            t.create_node(a, assumption=True)
        for c in struct.claims:
            t.create_node(c)
        for fid, (c, at, prereqs) in struct.families.items():
            t.create_node(fid)
            t.justify_node("family", fid, list(at) + list(prereqs))
            t.justify_node("support", c, [fid] + list(struct.claim_atoms[c]))
        self.tms = t; self.key = struct.key(); self.enabled = set()

    def _set(self, want: set[str]) -> None:
        assert self.tms is not None
        for a in sorted(self.enabled - want):
            self.tms.retract_assumption(a)
        for a in sorted(want - self.enabled):
            self.tms.enable_assumption(a)
        self.enabled = set(want)

    def run(self, struct: Structure, status: dict[str, str], accepted: tuple[str, ...], cost: dict, *, three_valued: bool = True) -> dict[str, str]:
        if self.tms is None or self.key != struct.key():
            self._build(struct)
        assert self.tms is not None
        before = self.tms.ops
        atoms = set(self.tms.nodes) - set(struct.claims) - set(struct.families)
        valid = {a for a in atoms if status.get(a, STATUS_VALID) == STATUS_VALID}
        unknown = {a for a in atoms if status.get(a, STATUS_VALID) == STATUS_UNKNOWN}
        if not three_valued:
            self._set(valid | unknown)
            out = {c: PRESERVED if self.tms.is_in(c) else REOPENED for c in accepted}
        else:
            self._set(valid | unknown); opt = {c: self.tms.is_in(c) for c in accepted}
            if unknown:
                self._set(valid); pes = {c: self.tms.is_in(c) for c in accepted}
            else:
                pes = opt
            out = {c: PRESERVED if pes[c] else REOPENED if not opt[c] else UNRESOLVED for c in accepted}
        cost["ops"] = cost.get("ops", 0) + (self.tms.ops - before)
        return out


class ATMSEngine:
    def __init__(self) -> None:
        self.atms: ATMS | None = None
        self.key = None

    def _build(self, struct: Structure) -> None:
        a = ATMS()
        atoms = sorted({x for _c, at, _p in struct.families.values() for x in at} | {x for ats in struct.claim_atoms.values() for x in ats})
        for x in atoms:
            a.create_node(x, assumption=True)
        for c in struct.claims:
            a.create_node(c)
        for fid in struct.families:
            a.create_node(fid)
        for c in topo(struct):
            for fid, (cc, at, prereqs) in struct.families.items():
                if cc != c:
                    continue
                a.justify(fid, list(at) + list(prereqs))
                a.justify(c, [fid] + list(struct.claim_atoms[c]))
        self.atms = a; self.key = struct.key()

    def run(self, struct: Structure, status: dict[str, str], accepted: tuple[str, ...], cost: dict) -> dict[str, str]:
        if self.atms is None or self.key != struct.key():
            self._build(struct)
        assert self.atms is not None
        before = self.atms.ops
        atoms = self.atms.assumptions
        valid = {a for a in atoms if status.get(a, STATUS_VALID) == STATUS_VALID}
        unknown = {a for a in atoms if status.get(a, STATUS_VALID) == STATUS_UNKNOWN}
        out = {}
        for c in accepted:
            if self.atms.holds_in(c, valid):
                out[c] = PRESERVED
            elif unknown and self.atms.holds_in(c, valid | unknown):
                out[c] = UNRESOLVED
            else:
                out[c] = REOPENED
        cost["ops"] = cost.get("ops", 0) + (self.atms.ops - before)
        return out


class AGMEngine:
    """Stateful kernel-contraction base: atoms enter/leave by expansion/
    contraction as their status changes; a valid contradiction triggers Levi
    revision against the claim (family rules are cut; base contraction has
    no recovery, so later corrections do not restore the cut rules)."""

    def __init__(self) -> None:
        self.kb: KernelBase | None = None
        self.key = None
        self.present: set[str] = set()
        self.contradicted: set[str] = set()

    def _build(self, struct: Structure) -> None:
        rules = []
        ent: dict[str, int] = {}
        for fid, (c, at, prereqs) in struct.families.items():
            rules.append(Rule(f"rule:{fid}", frozenset(at) | frozenset(prereqs), c)); ent[f"rule:{fid}"] = 1
        self.kb = KernelBase(set(), rules, ent); self.key = struct.key(); self.present = set(); self.contradicted = set()

    def run(self, struct: Structure, status: dict[str, str], accepted: tuple[str, ...], cost: dict) -> dict[str, str]:
        if self.kb is None or self.key != struct.key():
            self._build(struct)
        assert self.kb is not None
        before = self.kb.ops
        atoms = {a for _c, at, _p in struct.families.values() for a in at}
        want = {a for a in atoms if status.get(a, STATUS_VALID) != STATUS_INVALID}  # two-valued: censored stays
        for a in sorted(self.present - want):
            self.kb.contract(a)
        for a in sorted(want - self.present):
            self.kb.expand(a)
        self.present = set(want)
        for c in struct.claims:
            contra = status.get(contra_slot(c), STATUS_VALID) == STATUS_INVALID
            if contra and c not in self.contradicted:
                self.kb.revise_against(c, f"neg:{c}"); self.contradicted.add(c)
            elif not contra and c in self.contradicted:
                self.kb.contract(f"neg:{c}"); self.contradicted.discard(c)
        out = {c: (REOPENED if (c in self.contradicted or not self.kb.derives(c)) else PRESERVED) for c in accepted}
        cost["ops"] = cost.get("ops", 0) + (self.kb.ops - before)
        return out


def engine_noisy_or(struct: Structure, status: dict[str, str], accepted: tuple[str, ...], cost: dict) -> dict[str, str]:
    rel = {a: (0.9 if a.startswith("ev:") else 1.0) for _c, at, _p in struct.families.values() for a in at}
    model = NoisyOrSupport(struct.families, struct.claims, struct.claim_atoms, rel, 0.5)
    atoms = set(rel) | {a for ats in struct.claim_atoms.values() for a in ats}
    def values(unknown_as: float) -> dict[str, float]:
        return {a: (1.0 if status.get(a, STATUS_VALID) == STATUS_VALID else 0.0 if status.get(a, STATUS_VALID) == STATUS_INVALID else unknown_as) for a in atoms}
    opt = model.beliefs(values(1.0)); pes = model.beliefs(values(0.0))
    d = model.decide(opt, pes)
    cost["ops"] = cost.get("ops", 0) + model.ops
    return {c: d[c] for c in accepted}


def engine_assurance(struct: Structure, status: dict[str, str], accepted: tuple[str, ...], cost: dict) -> dict[str, str]:
    ac = AssuranceCase()
    for c in struct.claims:
        ac.add(c, "goal")
    for fid, (c, at, prereqs) in struct.families.items():
        ac.add(fid, "strategy"); ac.supported_by(c, fid)
        for a in at:
            if a not in ac.kind:
                ac.add(a, "solution" if a.startswith("ev:") else "context")
            if a.startswith("ev:"):
                ac.supported_by(fid, a)
            else:
                ac.in_context_of(fid, a)
        for p in prereqs:
            ac.supported_by(fid, p)
    for c, ats in struct.claim_atoms.items():
        for a in ats:
            if a not in ac.kind:
                ac.add(a, "context")
            ac.in_context_of(c, a)
    changed = [a for a in ac.kind if ac.kind[a] in ("solution", "context") and status.get(a, STATUS_VALID) != STATUS_VALID]
    _ch, suspect = ac.change_impact(changed)
    cost["ops"] = cost.get("ops", 0) + ac.ops
    return {c: (REOPENED if c in suspect else PRESERVED) for c in accepted}


def engine_provenance_only(v: ArmView, cost: dict) -> dict[str, str]:
    """No families: every commitment downstream of a revoked node reopens.
    Roots: retracted sources, invalid calibrations, evaluators whose coverage
    changed, relations whose type changed, claims whose scope changed
    (scope node), valid contradictions (nocontra node). Disputed/censored
    = not revoked (two-valued). Dependence has no provenance node."""
    w, w0 = v.world, v.world_v0
    nodes: list[tuple[str, str]] = []
    edges: list[tuple[str, str, str, str]] = []
    nodes += [(s, "source") for s in w.sources] + [(c, "calibration") for c in w.calibrations]
    nodes += [(f"evaluator:{e}", "evaluator") for e in w.evaluators] + [(f"relation:{k}", "relation") for k in w.relations]
    nodes += [(f"scope:{c}", "scope") for c in w.claims] + [(f"nocontra:{c}", "contradiction") for c in w.claims]
    nodes += [(e, "evidence") for e in w.evidence] + [(f, "family") for f in w.families] + [(c, "commitment") for c in w.claims]
    for e in w.evidence.values():
        edges.append((e.source_id, e.evidence_id, "DERIVES", "source"))
        if e.calibration_id:
            edges.append((e.calibration_id, e.evidence_id, "CALIBRATES_FROM", "calibration"))
        if e.evaluator_id:
            edges.append((f"evaluator:{e.evaluator_id}", e.evidence_id, "EVALUATED_BY", "evaluator"))
    for fam in w.families.values():
        claim = w.claims[fam.claim_id]
        for e in w.positive_evidence_of_family(fam):
            edges.append((e.evidence_id, fam.family_id, "DERIVES", "support"))
            if e.context_id != claim.context_id:
                key = w.relation_key(e.context_id, claim.context_id)
                if key in w.relations:
                    edges.append((f"relation:{key}", fam.family_id, "TRANSLATES", "transport"))
        if fam.evidence_ids:
            edges.append((f"scope:{fam.claim_id}", fam.family_id, "REFINES", "scope"))
        edges.append((fam.family_id, fam.claim_id, "DERIVES", "support"))
        for p in fam.prerequisite_ids:
            edges.append((p, fam.family_id, "DERIVES", "prerequisite"))
    for c in w.claims:
        edges.append((f"nocontra:{c}", c, "REFINES", "contradiction"))
    po = ProvenanceOnly(nodes, edges)
    roots = [s for s, st in w.sources.items() if st == SOURCE_RETRACTED] + [c for c, cal in w.calibrations.items() if cal.status == CAL_INVALID]
    for e, ev in w.evaluators.items():
        b = w0.evaluators.get(e)
        if b is None or set(b.coverage) != set(ev.coverage) or set(b.uncertain) != set(ev.uncertain):
            roots.append(f"evaluator:{e}")
    for k, r in w.relations.items():
        b = w0.relations.get(k)
        if b is None or b.relation_type != r.relation_type:
            roots.append(f"relation:{k}")
    for c in w.claims:
        if c in w0.claims and tuple(w0.claims[c].scope) != tuple(w.claims[c].scope):
            roots.append(f"scope:{c}")
        if any(w.sources[e.source_id] != SOURCE_RETRACTED and not (e.calibration_id and w.calibrations[e.calibration_id].status == CAL_INVALID) for e in w.negative_evidence_against(c)):
            roots.append(f"nocontra:{c}")
    affected = po.affected(roots)
    cost["ops"] = cost.get("ops", 0) + po.ops + len(affected)
    return {c: (REOPENED if c in affected else PRESERVED) for c in v.accepted}


# ---- arm definitions -------------------------------------------------------------

@dataclass
class ArmSpec:
    name: str
    family: str          # SINGLE_PARENT / B5_LADDER / M / M_ABLATION / CONTROL
    modules: dict[str, str]   # module -> "typed" | "untyped" | "untyped3" | "context" | "noop"
    engine: str
    witness_level: tuple[str, ...] = MODULES   # modules exported at witness level (others verdict-level)
    merge_families: bool = False
    note: str = ""


def _status_for(spec: ArmSpec, v: ArmView, ops: dict) -> dict[str, str]:
    st: dict[str, str] = {}
    mode = spec.modules
    two_valued = spec.engine in ("jtms2", "agm", "assurance")
    if mode["PROV"] == "typed":
        st.update(prov_typed(v, ops))
    else:
        st.update(prov_direct(v, ops, two_valued=two_valued))
    st.update(dep_typed(v, ops) if mode["DEP"] == "typed" else dep_untyped(v, ops))
    if mode["TRANS"] == "typed":
        st.update(trans_typed(v, ops))
    else:
        st.update(trans_untyped(v, ops, two_valued=two_valued))
    st.update(eval_typed(v, ops) if mode["EVAL"] == "typed" else eval_untyped(v, ops))
    st.update(scope_typed(v, ops) if mode["SCOPE"] == "typed" else scope_untyped_context(v, ops) if mode["SCOPE"] == "context" else scope_untyped_noop(v, ops))
    st.update(contra_module(v, ops, st))
    return st


TYPED = {m: "typed" for m in MODULES}
UNTYPED = {"PROV": "direct", "DEP": "untyped", "TRANS": "untyped", "EVAL": "untyped", "SCOPE": "noop", "CONTRA": "typed"}


def arm_specs() -> list[ArmSpec]:
    specs = [
        ArmSpec("A0_PROVENANCE_ONLY_INVALIDATION", "SINGLE_PARENT", dict(UNTYPED), "provenance_only", note="revocation descendants over the full provenance graph; no support families"),
        ArmSpec("A1_JTMS_CLASSICAL", "SINGLE_PARENT", dict(UNTYPED), "jtms2", note="Doyle JTMS over registered families; untyped events; two-valued (censored = valid)"),
        ArmSpec("A2_ATMS_CLASSICAL", "SINGLE_PARENT", dict(UNTYPED), "atms", note="de Kleer ATMS; untyped events; censored atoms expressed as environments"),
        ArmSpec("A3_AGM_KERNEL_CONTRACTION", "SINGLE_PARENT", dict(UNTYPED), "agm", note="Hansson kernel contraction, rules less entrenched than evidence; Levi revision on contradiction; two-valued"),
        ArmSpec("A4_BAYES_NOISY_OR", "SINGLE_PARENT", dict(UNTYPED), "noisy_or", note="noisy-OR support graph, r=0.9 evidence, tau=0.5, envelope on censored"),
        ArmSpec("A5_ASSURANCE_CASE_UPDATE", "SINGLE_PARENT", {**UNTYPED, "SCOPE": "context"}, "assurance", note="GSN change-impact: challenged -> suspect ancestors; two-valued; contexts typed as context elements"),
    ]
    ladder = {1: (), 2: ("PROV",), 3: ("PROV", "DEP"), 4: ("PROV", "DEP", "TRANS", "EVAL"), 5: MODULES}
    for r, wl in ladder.items():
        name = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION" if r == 5 else f"B5_R{r}_{'VERDICT_ONLY' if r == 1 else '+'.join(wl)}"
        specs.append(ArmSpec(name, "B5_LADDER", dict(TYPED), "jtms", witness_level=tuple(wl) + ("CONTRA",), note=f"federation rung {r}: typed modules; witness-level export {wl or 'none'}; JTMS propagation with censored-atom envelope"))
    specs += [
        ArmSpec("M_ME_SELECTIVE_REOPENING", "M", dict(TYPED), "selective_reopen", note="orion_v2 provenance + evidence dependence + typed transport + evaluator contract + ProblemContract scope -> orion_v2.reopening.selective_reopen envelope"),
        ArmSpec("M_MINUS_DEPENDENCE_ANCESTRY", "M_ABLATION", {**TYPED, "DEP": "untyped"}, "selective_reopen"),
        ArmSpec("M_MINUS_TYPED_TRANSPORT", "M_ABLATION", {**TYPED, "TRANS": "untyped"}, "selective_reopen"),
        ArmSpec("M_MINUS_EVALUATOR_CONTRACT", "M_ABLATION", {**TYPED, "EVAL": "untyped"}, "selective_reopen"),
        ArmSpec("M_MINUS_SUPPORT_FAMILIES", "M_ABLATION", dict(TYPED), "selective_reopen", merge_families=True),
        ArmSpec("M_GLOBAL_RESET_CONTROL", "CONTROL", dict(TYPED), "global_reset"),
        ArmSpec("M_PROVENANCE_ONLY_CONTROL", "CONTROL", dict(UNTYPED), "provenance_only"),
        ArmSpec("C_NEVER_REOPEN", "CONTROL", dict(UNTYPED), "never"),
        ArmSpec("C_RANDOM_DISPOSITION", "CONTROL", dict(UNTYPED), "random"),
    ]
    return specs


class ArmRunner:
    """Runs one arm across the versions of one instance (stateful engines are
    kept across versions to allow native incrementality)."""

    def __init__(self, spec: ArmSpec, instance_seed: int) -> None:
        self.spec = spec
        self.rng = random.Random(instance_seed ^ 0x5EED)
        self.jtms = JTMSEngine(); self.atms = ATMSEngine(); self.agm = AGMEngine()

    def run_version(self, v: ArmView) -> tuple[dict[str, str], dict[str, float]]:
        spec = self.spec
        cost: dict = {"ops": 0, "module_ops": 0}
        t0 = time.perf_counter_ns()
        if spec.engine == "never":
            out = {c: PRESERVED for c in v.accepted}
        elif spec.engine == "random":
            out = {c: self.rng.choice((PRESERVED, REOPENED, UNRESOLVED)) for c in v.accepted}
        elif spec.engine == "provenance_only":
            out = engine_provenance_only(v, cost)
        else:
            mops: dict = {}
            status = _status_for(spec, v, mops)
            cost["module_ops"] = mops.get("n", 0)
            slots = condition_slots(v.world)
            struct = build_structure(v.world, slots, merge_families=spec.merge_families)
            for m in MODULES:
                if m not in spec.witness_level and m != "CONTRA":
                    struct, status = compress_module_to_verdicts(struct, slots, status, m)
            if spec.engine == "global_reset":
                bad = any(s != STATUS_VALID for s in status.values())
                out = {c: (REOPENED if bad else PRESERVED) for c in v.accepted}
            elif spec.engine == "selective_reopen":
                out = engine_selective_reopen(struct, status, v.accepted, cost)
            elif spec.engine == "jtms":
                out = self.jtms.run(struct, status, v.accepted, cost, three_valued=True)
            elif spec.engine == "jtms2":
                out = self.jtms.run(struct, status, v.accepted, cost, three_valued=False)
            elif spec.engine == "atms":
                out = self.atms.run(struct, status, v.accepted, cost)
            elif spec.engine == "agm":
                out = self.agm.run(struct, status, v.accepted, cost)
            elif spec.engine == "noisy_or":
                out = engine_noisy_or(struct, status, v.accepted, cost)
            elif spec.engine == "assurance":
                out = engine_assurance(struct, status, v.accepted, cost)
            else:
                raise ValueError(spec.engine)
        cost["wall_ns"] = time.perf_counter_ns() - t0
        return out, cost
