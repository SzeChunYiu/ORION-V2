#!/usr/bin/env python3
"""ME-X4 exact oracle (frozen with design V1, §2.4).

Computes, for a registered World, the three-valued status of every atomic
support condition, then the disposition of every accepted commitment:

  PRESERVED   -- supported under EVERY resolution of censored conditions
  REOPENED    -- unsupported under EVERY resolution
  UNRESOLVED  -- depends on the resolution of censored conditions

Two independent computations are always run and must agree (G0b):
  (1) Kleene three-valued fixed point over the monotone support formula;
  (2) exhaustive enumeration of all 2^u resolutions of the u censored atoms.

This module is protected custody: arms never import it.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Optional

from mex4_model import (
    CAL_INVALID, CAL_UNDER_REVIEW, DEP_CONFIRMED, DEP_SUSPECTED, RELATION_CANNOT_CHECK, RELATION_RANK,
    SOURCE_DISPUTED, SOURCE_RETRACTED, STATUS_INVALID, STATUS_UNKNOWN, STATUS_VALID, Family, World,
)

Tri = Optional[bool]  # True / False / None(unknown)

PRESERVED = "PRESERVED"
REOPENED = "REOPENED"
UNRESOLVED = "UNRESOLVED"


def _tri(status: str) -> Tri:
    return {STATUS_VALID: True, STATUS_INVALID: False, STATUS_UNKNOWN: None}[status]


def _and(values) -> Tri:
    seen_unknown = False
    for v in values:
        if v is False:
            return False
        if v is None:
            seen_unknown = True
    return None if seen_unknown else True


def _or(values) -> Tri:
    seen_unknown = False
    for v in values:
        if v is True:
            return True
        if v is None:
            seen_unknown = True
    return None if seen_unknown else False


# ---- atomic condition semantics (§2.3) --------------------------------------

def evidence_validity(w: World, evidence_id: str) -> str:
    e = w.evidence[evidence_id]
    src = w.sources[e.source_id]
    if src == SOURCE_RETRACTED:
        return STATUS_INVALID
    cal = w.calibrations[e.calibration_id].status if e.calibration_id else None
    if cal == CAL_INVALID:
        return STATUS_INVALID
    if src == SOURCE_DISPUTED or cal == CAL_UNDER_REVIEW:
        return STATUS_UNKNOWN
    return STATUS_VALID


def evaluator_coverage(w: World, evidence_id: str) -> str | None:
    e = w.evidence[evidence_id]
    if not e.evaluator_id:
        return None
    fc = w.claims[e.claim_id].failure_class
    ev = w.evaluators[e.evaluator_id]
    if fc in ev.coverage:
        return STATUS_VALID
    if fc in ev.uncertain:
        return STATUS_UNKNOWN
    return STATUS_INVALID


def transport_status(w: World, family: Family, evidence_id: str) -> str | None:
    e = w.evidence[evidence_id]
    claim = w.claims[family.claim_id]
    if e.context_id == claim.context_id:
        return None
    rel = w.relations.get(w.relation_key(e.context_id, claim.context_id))
    if rel is None:
        return STATUS_INVALID
    if rel.relation_type == RELATION_CANNOT_CHECK:
        return STATUS_UNKNOWN
    required = family.required_relation or "APPROXIMATELY_EQUIVALENT"
    return STATUS_VALID if RELATION_RANK[rel.relation_type] >= RELATION_RANK[required] else STATUS_INVALID


def _components(nodes: set[str], pairs) -> int:
    adj = {n: set() for n in nodes}
    for a, b in pairs:
        if a in adj and b in adj:
            adj[a].add(b); adj[b].add(a)
    seen: set[str] = set(); count = 0
    for n in sorted(nodes):
        if n in seen:
            continue
        count += 1; stack = [n]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x); stack.extend(adj[x] - seen)
    return count


def independence_status(w: World, family: Family) -> str | None:
    if family.min_independent <= 0:
        return None
    nodes = {e.evidence_id for e in w.positive_evidence_of_family(family)}
    confirmed = [(d.left_id, d.right_id) for d in w.dependence if d.status == DEP_CONFIRMED]
    all_edges = confirmed + [(d.left_id, d.right_id) for d in w.dependence if d.status == DEP_SUSPECTED]
    if _components(nodes, confirmed) < family.min_independent:
        return STATUS_INVALID
    if _components(nodes, all_edges) < family.min_independent:
        return STATUS_UNKNOWN
    return STATUS_VALID


def scope_status(w: World, family: Family) -> str | None:
    """Scope sufficiency of a family's own evidence. Prerequisite-only families
    carry no scope atom: their scope is inherited through the prerequisites."""
    pos = w.positive_evidence_of_family(family)
    if not pos:
        return None
    cov: set[str] = set()
    for e in pos:
        cov.update(e.scope_coverage)
    return STATUS_VALID if set(w.claims[family.claim_id].scope) <= cov else STATUS_INVALID


def nocontra_status(w: World, claim_id: str) -> str:
    vals = [evidence_validity(w, e.evidence_id) for e in w.negative_evidence_against(claim_id)]
    if any(v == STATUS_VALID for v in vals):
        return STATUS_INVALID
    if any(v == STATUS_UNKNOWN for v in vals):
        return STATUS_UNKNOWN
    return STATUS_VALID


@dataclass
class ConditionTable:
    atoms: dict[str, str]                 # atom id -> VALID/INVALID/UNKNOWN
    family_atoms: dict[str, tuple[str, ...]]
    claim_atoms: dict[str, tuple[str, ...]]  # nocontra atoms per claim


def condition_table(w: World) -> ConditionTable:
    atoms: dict[str, str] = {}
    family_atoms: dict[str, tuple[str, ...]] = {}
    claim_atoms: dict[str, tuple[str, ...]] = {}
    for fam in sorted(w.families.values(), key=lambda f: f.family_id):
        ids: list[str] = []
        for e in fam.evidence_ids:
            if not w.evidence[e].supports:
                continue
            a = f"ev:{e}"; atoms[a] = evidence_validity(w, e); ids.append(a)
            s = evaluator_coverage(w, e)
            if s is not None:
                a = f"evc:{e}"; atoms[a] = s; ids.append(a)
            s = transport_status(w, fam, e)
            if s is not None:
                a = f"tr:{fam.family_id}:{e}"; atoms[a] = s; ids.append(a)
        s = independence_status(w, fam)
        if s is not None:
            a = f"ind:{fam.family_id}"; atoms[a] = s; ids.append(a)
        s = scope_status(w, fam)
        if s is not None:
            a = f"scope:{fam.family_id}"; atoms[a] = s; ids.append(a)
        family_atoms[fam.family_id] = tuple(ids)
    for c in w.claims:
        a = f"nocontra:{c}"; atoms[a] = nocontra_status(w, c); claim_atoms[c] = (a,)
    return ConditionTable(atoms, family_atoms, claim_atoms)


# ---- support evaluation -----------------------------------------------------

def evaluate_support(w: World, atom_values: dict[str, Tri], table: ConditionTable) -> dict[str, Tri]:
    """Three-valued support of every claim, bottom-up over the prerequisite DAG."""
    support: dict[str, Tri] = {}
    for c in w.prerequisite_topological_order():
        fams = w.families_of(c)
        fam_vals = []
        for fam in fams:
            parts = [atom_values[a] for a in table.family_atoms[fam.family_id]]
            parts += [support[p] for p in fam.prerequisite_ids]
            fam_vals.append(_and(parts))
        s = _or(fam_vals) if fams else False
        support[c] = _and([s] + [atom_values[a] for a in table.claim_atoms[c]])
    return support


@dataclass(frozen=True)
class Expected:
    reopened: tuple[str, ...]
    preserved: tuple[str, ...]
    unresolved: tuple[str, ...]
    unknown_atoms: tuple[str, ...]
    exhaustive_agrees: bool

    def as_dict(self) -> dict[str, list[str] | bool]:
        return {"reopened": list(self.reopened), "preserved": list(self.preserved), "unresolved": list(self.unresolved), "unknown_atoms": list(self.unknown_atoms), "exhaustive_agrees": self.exhaustive_agrees}


def oracle(w: World, accepted: tuple[str, ...], *, max_unknown: int = 14) -> Expected:
    table = condition_table(w)
    tri = {a: _tri(s) for a, s in table.atoms.items()}
    kleene = evaluate_support(w, tri, table)
    unknown = tuple(sorted(a for a, v in tri.items() if v is None))
    # exhaustive enumeration over all resolutions of the censored atoms
    if len(unknown) > max_unknown:
        raise ValueError(f"too many censored atoms for exhaustive oracle: {len(unknown)}")
    always_true = {c: True for c in accepted}
    always_false = {c: True for c in accepted}
    for bits in itertools.product((True, False), repeat=len(unknown)):
        vals = dict(tri); vals.update(zip(unknown, bits))
        sup = evaluate_support(w, vals, table)
        for c in accepted:
            if sup[c]:
                always_false[c] = False
            else:
                always_true[c] = False
    reopened, preserved, unresolved = [], [], []
    for c in accepted:
        k = kleene[c]
        if k is True:
            preserved.append(c)
        elif k is False:
            reopened.append(c)
        else:
            unresolved.append(c)
    exhaustive_pres = [c for c in accepted if always_true[c]]
    exhaustive_reop = [c for c in accepted if always_false[c]]
    exhaustive_unres = [c for c in accepted if not always_true[c] and not always_false[c]]
    agrees = (exhaustive_pres == preserved and exhaustive_reop == reopened and exhaustive_unres == unresolved)
    return Expected(tuple(reopened), tuple(preserved), tuple(unresolved), unknown, agrees)


def all_accepted_supported_at_v0(w: World) -> bool:
    acc = w.accepted_ids()
    exp = oracle(w, acc)
    return exp.preserved == acc and not exp.unknown_atoms


def expected_trajectory(world_v0: World, events, accepted: tuple[str, ...]) -> list[Expected]:
    from mex4_model import apply_event
    out = []
    w = world_v0
    for ev in events:
        w = apply_event(w, ev)
        out.append(oracle(w, accepted))
    return out
