#!/usr/bin/env python3
"""ME-X4 known-answer support-graph generator (frozen with design V1, §2–§3).

Every instance = registered world at v0 + typed event sequence (1–3 events).
The generator plants the stratum's structure, then checks the stratum
invariant with the exact oracle (rejection sampling, deterministic under the
instance seed). Hidden expected sets are computed by mex4_oracle and written
to protected custody by the runner, never handed to arms.

Also holds the 12 hand-authored known-answer fixtures (G0a) and the H-EXT-3
finite separation pair (P, Q).
"""
from __future__ import annotations

import hashlib
import random
from typing import Any, Callable

from mex4_model import (
    CAL_VALID, DEP_CONFIRMED, RELATION_CANNOT_CHECK, RELATION_RANK, SOURCE_VALID, STRATA, Calibration, Claim,
    DependenceDeclaration, Evaluator, Event, Evidence, Family, Instance, Relation, World, apply_event,
)
from mex4_oracle import (
    REOPENED, PRESERVED, UNRESOLVED, Expected, all_accepted_supported_at_v0, condition_table, expected_trajectory, oracle,
)

CONTEXTS = ("ctx0", "ctx1", "ctx2")
FAILURE_CLASSES = ("FC_A", "FC_B", "FC_C")
SCOPE_ELEMENTS = ("S1", "S2", "S3")
STRONG_RELATIONS = ("ISOMORPHIC", "BEHAVIORALLY_EQUIVALENT", "PREDICTIVELY_EQUIVALENT", "DECISION_DOMINATES")
DEP_KINDS = ("SHARED_DATA", "SHARED_SOURCE", "SHARED_MODEL", "SHARED_INSTRUMENT", "COMMON_CAUSE")
MAX_UNKNOWN_ATOMS = 8
MAX_ATTEMPTS = 400


def instance_seed(split_seed: str, stratum: str, index: int) -> int:
    return int(hashlib.sha256(f"{split_seed}|{stratum}|{index}".encode()).hexdigest()[:12], 16)


# ---- base world -------------------------------------------------------------

class _Builder:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.w = World()
        self.n_ev = 0
        self.n_fam = 0

    def new_evidence(self, claim: Claim, *, source: str | None = None, context: str | None = None, coverage: tuple[str, ...] | None = None, calibration: str | None = None, evaluator: str | None = None, supports: bool = True) -> Evidence:
        rng, w = self.rng, self.w
        self.n_ev += 1
        eid = f"e{self.n_ev:02d}"
        src = source or rng.choice(sorted(w.sources))
        ctx = context or claim.context_id
        cov = coverage if coverage is not None else tuple(sorted(set(claim.scope) | ({rng.choice(SCOPE_ELEMENTS)} if rng.random() < 0.4 else set())))
        if calibration is None and rng.random() < 0.45:
            calibration = rng.choice(sorted(w.calibrations))
        if evaluator is None:
            eligible = sorted(e for e, ev in w.evaluators.items() if claim.failure_class in ev.coverage)
            evaluator = rng.choice(eligible) if eligible and rng.random() < 0.8 else ""
        e = Evidence(eid, claim.claim_id, src, ctx, cov, evaluator or "", calibration or "", data_id=f"data:{src}", model_id="", instrument_id=(w.calibrations[calibration].instrument_id if calibration else ""), supports=supports)
        w.evidence[eid] = e
        return e

    def new_family(self, claim: Claim, evidence_ids: tuple[str, ...], prereqs: tuple[str, ...] = (), *, min_independent: int = 0, required_relation: str = "") -> Family:
        self.n_fam += 1
        fid = f"{claim.claim_id}.F{self.n_fam}"
        fam = Family(fid, claim.claim_id, tuple(evidence_ids), tuple(prereqs), min_independent, required_relation)
        self.w.families[fid] = fam
        return fam

    def transported_evidence(self, claim: Claim, family_required: str | None = None) -> tuple[Evidence, str]:
        """Evidence produced in a foreign context whose relation to the claim context is adequate."""
        rng, w = self.rng, self.w
        others = [c for c in CONTEXTS if c != claim.context_id]
        ctx = rng.choice(others)
        key = w.relation_key(ctx, claim.context_id)
        if key not in w.relations:
            w.relations[key] = Relation(ctx, claim.context_id, rng.choice(STRONG_RELATIONS))
        rank = RELATION_RANK[w.relations[key].relation_type]
        candidates = [r for r, k in RELATION_RANK.items() if 1 <= k <= rank]
        req = family_required or rng.choice(candidates)
        return self.new_evidence(claim, context=ctx), req


def build_base_world(rng: random.Random) -> _Builder:
    b = _Builder(rng)
    w = b.w
    for i in range(rng.randint(4, 7)):
        w.sources[f"src{i}"] = SOURCE_VALID
    w.sources["src_unused"] = SOURCE_VALID
    for inst in ("inst0", "inst1"):
        for j in range(rng.randint(1, 2)):
            cid = f"cal:{inst}:{j}"
            w.calibrations[cid] = Calibration(cid, inst, CAL_VALID)
    w.calibrations["cal:inst_unused:0"] = Calibration("cal:inst_unused:0", "inst_unused", CAL_VALID)
    w.evaluators["ev0"] = Evaluator("ev0", FAILURE_CLASSES)
    w.evaluators["ev1"] = Evaluator("ev1", tuple(sorted(rng.sample(FAILURE_CLASSES, 2))))
    w.evaluators["ev2"] = Evaluator("ev2", tuple(sorted(rng.sample(FAILURE_CLASSES, rng.randint(1, 2)))))
    for a in CONTEXTS:
        for c in CONTEXTS:
            if a != c and rng.random() < 0.7:
                w.relations[w.relation_key(a, c)] = Relation(a, c, rng.choice(STRONG_RELATIONS))
    n_claims = rng.randint(4, 8)
    layers: list[list[str]] = [[], [], []]
    for i in range(n_claims):
        cid = f"c{i}"
        layer = 0 if i < 2 else rng.choice((0, 1, 1, 2))
        scope = tuple(sorted(rng.sample(SCOPE_ELEMENTS, rng.randint(1, 2))))
        w.claims[cid] = Claim(cid, rng.choice(CONTEXTS[:2]), rng.choice(FAILURE_CLASSES), scope, True)
        layers[layer].append(cid)
    for layer_idx, layer in enumerate(layers):
        lower = [c for lo in layers[:layer_idx] for c in lo]
        for cid in layer:
            claim = w.claims[cid]
            for _ in range(rng.choice((1, 1, 2, 2, 3))):
                ev_ids: list[str] = []
                req = ""
                prereq_only = bool(lower) and rng.random() < 0.2
                for _k in range(0 if prereq_only else rng.randint(1, 3)):
                    if rng.random() < 0.2 and req == "":
                        e, req = b.transported_evidence(claim)
                    else:
                        e = b.new_evidence(claim)
                    ev_ids.append(e.evidence_id)
                prereqs = tuple(sorted(rng.sample(lower, min(len(lower), rng.choice((1, 2)) if prereq_only else rng.choice((0, 0, 1, 1, 2)))))) if lower else ()
                if not ev_ids and not prereqs:
                    ev_ids.append(b.new_evidence(claim).evidence_id)
                k = 2 if (len(ev_ids) >= 2 and rng.random() < 0.35) else 0
                b.new_family(claim, tuple(ev_ids), prereqs, min_independent=k, required_relation=req)
    # alternative hypothesis (rejected at v0 by valid negative evidence)
    if rng.random() < 0.5:
        target = rng.choice(sorted(w.claims))
        alt = Claim("alt0", w.claims[target].context_id, w.claims[target].failure_class, w.claims[target].scope, False, alternative_of=target)
        w.claims["alt0"] = alt
        e = b.new_evidence(alt)
        b.new_family(alt, (e.evidence_id,))
        b.new_evidence(alt, supports=False)
    # coverage repair: every family must cover its claim scope at v0
    for fam in w.families.values():
        claim = w.claims[fam.claim_id]
        pos = w.positive_evidence_of_family(fam)
        if pos and not set(claim.scope) <= {s for e in pos for s in e.scope_coverage}:
            e0 = w.evidence[pos[0].evidence_id]
            e0.scope_coverage = tuple(sorted(set(e0.scope_coverage) | set(claim.scope)))
    w.validate()
    return b


# ---- planters ---------------------------------------------------------------

def _touched_by_source(w: World, source_id: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for fam in w.families.values():
        if any(w.evidence[e].source_id == source_id and w.evidence[e].supports for e in fam.evidence_ids):
            out.setdefault(fam.claim_id, []).append(fam.family_id)
    return out


def _accepted_with_n_families(w: World, n_min: int) -> list[str]:
    return [c for c in w.accepted_ids() if len(w.families_of(c)) >= n_min]


def plant_source_retracted(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    multi = _accepted_with_n_families(w, 2)
    if not multi:
        return None
    a = rng.choice(multi)
    others = [c for c in w.accepted_ids() if c != a]
    if not others:
        return None
    bclaim = rng.choice(others)
    s = rng.choice(sorted(x for x in w.sources if x != "src_unused"))
    fams_a = w.families_of(a)
    # one family of A shares the source; another family of A must avoid it
    w.evidence[fams_a[0].evidence_ids[0]].source_id = s
    for fam in fams_a[1:]:
        for e in fam.evidence_ids:
            if w.evidence[e].source_id == s:
                w.evidence[e].source_id = rng.choice(sorted(x for x in w.sources if x not in (s, "src_unused")))
    for fam in w.families_of(bclaim):
        w.evidence[fam.evidence_ids[0]].source_id = s
    return [Event("SOURCE_RETRACTED", {"source_id": s})], {"target_source": s, "preserved_target": a, "reopened_target": bclaim}


def inv_source_retracted(traj: list[Expected], f: dict[str, Any]) -> bool:
    last = traj[-1]
    return f["reopened_target"] in last.reopened and f["preserved_target"] in last.preserved and not last.unresolved


def plant_dependence_discovered(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    cands = [fam for fam in w.families.values() if w.claims[fam.claim_id].accepted_v0 and len(w.positive_evidence_of_family(fam)) >= 2]
    if not cands:
        return None
    fam = rng.choice(sorted(cands, key=lambda x: x.family_id))
    pos = [e.evidence_id for e in w.positive_evidence_of_family(fam)]
    fam.min_independent = len(pos) if (len(pos) == 3 and rng.random() < 0.5) else 2
    events = [Event("DEPENDENCE_DISCOVERED", {"left_id": pos[0], "right_id": pos[1], "kind": rng.choice(DEP_KINDS)})]
    if fam.min_independent == 3:
        events[0].payload["left_id"], events[0].payload["right_id"] = pos[1], pos[2]
    feats: dict[str, Any] = {"target_family": fam.family_id, "target_claim": fam.claim_id, "decoy": ""}
    decoys = [g for g in w.families.values() if g.family_id != fam.family_id and len(w.positive_evidence_of_family(g)) >= 2 and w.claims[g.claim_id].accepted_v0]
    if decoys and rng.random() < 0.6:
        g = rng.choice(sorted(decoys, key=lambda x: x.family_id))
        gp = [e.evidence_id for e in w.positive_evidence_of_family(g)]
        if len(gp) >= 3 and rng.random() < 0.5:
            g.min_independent = 2  # three items, one edge: still two components
        else:
            g.min_independent = 0  # no independence requirement: dependence is irrelevant
        events.append(Event("DEPENDENCE_DISCOVERED", {"left_id": gp[0], "right_id": gp[1], "kind": rng.choice(DEP_KINDS)}, note="decoy"))
        feats["decoy"] = g.family_id
    return events, feats


def inv_dependence_discovered(traj: list[Expected], f: dict[str, Any], w_final: World) -> bool:
    table = condition_table(w_final)
    if table.atoms.get(f"ind:{f['target_family']}") != "INVALID":
        return False
    if f["decoy"] and table.atoms.get(f"ind:{f['decoy']}", "VALID") != "VALID":
        return False
    return not traj[-1].unresolved


def plant_calibration_invalidated(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    inst_cals = {}
    for c in w.calibrations.values():
        inst_cals.setdefault(c.instrument_id, []).append(c.calibration_id)
    two = [i for i, cs in inst_cals.items() if len(cs) >= 2 and i != "inst_unused"]
    if not two:
        return None
    inst = rng.choice(sorted(two))
    cal_bad, cal_ok = sorted(inst_cals[inst])[:2]
    acc = w.accepted_ids()
    if len(acc) < 2:
        return None
    a, bclaim = rng.sample(list(acc), 2)
    fa = w.families_of(a)[0]; fb = w.families_of(bclaim)[0]
    w.evidence[fa.evidence_ids[0]].calibration_id = cal_bad; w.evidence[fa.evidence_ids[0]].instrument_id = inst
    w.evidence[fb.evidence_ids[0]].calibration_id = cal_ok; w.evidence[fb.evidence_ids[0]].instrument_id = inst
    for fam in w.families_of(bclaim):
        for e in fam.evidence_ids:
            if w.evidence[e].calibration_id == cal_bad:
                w.evidence[e].calibration_id = cal_ok
    return [Event("CALIBRATION_INVALIDATED", {"calibration_id": cal_bad})], {"target_calibration": cal_bad, "sibling_calibration": cal_ok, "touched_claim": a, "sibling_claim": bclaim}


def inv_calibration_invalidated(traj: list[Expected], f: dict[str, Any], w_final: World) -> bool:
    last = traj[-1]
    touched = f["touched_claim"] in last.reopened or f["touched_claim"] in last.preserved
    return touched and f["sibling_claim"] in last.preserved and not last.unresolved and any(k.startswith("ev:") and v == "INVALID" for k, v in condition_table(w_final).atoms.items())


def plant_transport_invalidated(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    c = rng.choice(acc)
    claim = w.claims[c]
    fam = w.families_of(c)[0]
    e, req = b.transported_evidence(claim, family_required=rng.choice(("PREDICTIVELY_EQUIVALENT", "DECISION_DOMINATES", "BEHAVIORALLY_EQUIVALENT")))
    key = w.relation_key(e.context_id, claim.context_id)
    if RELATION_RANK[w.relations[key].relation_type] < RELATION_RANK[req]:
        w.relations[key].relation_type = "ISOMORPHIC"
    fam.evidence_ids = tuple(fam.evidence_ids) + (e.evidence_id,)
    fam.required_relation = req
    weaker = [r for r, k in RELATION_RANK.items() if k < RELATION_RANK[req]]
    events = [Event("RELATION_RETYPED", {"source_context": e.context_id, "target_context": claim.context_id, "relation_type": rng.choice(weaker)})]
    feats: dict[str, Any] = {"target_family": fam.family_id, "target_evidence": e.evidence_id, "decoy_relation": ""}
    # decoy: a different relation downgraded but still sufficient for whoever uses it
    other_keys = [k for k in sorted(w.relations) if k != key]
    if other_keys and rng.random() < 0.6:
        k2 = rng.choice(other_keys)
        rel = w.relations[k2]
        needed = [RELATION_RANK[g.required_relation or "APPROXIMATELY_EQUIVALENT"] for g in w.families.values() for x in g.evidence_ids if w.evidence[x].context_id == rel.source_context and w.claims[g.claim_id].context_id == rel.target_context]
        floor = max(needed) if needed else 1
        ok = [r for r, kk in RELATION_RANK.items() if floor <= kk < RELATION_RANK[rel.relation_type]]
        if ok:
            events.append(Event("RELATION_RETYPED", {"source_context": rel.source_context, "target_context": rel.target_context, "relation_type": rng.choice(ok)}, note="decoy"))
            feats["decoy_relation"] = k2
    return events, feats


def inv_transport_invalidated(traj: list[Expected], f: dict[str, Any], w_final: World) -> bool:
    atoms = condition_table(w_final).atoms
    return atoms.get(f"tr:{f['target_family']}:{f['target_evidence']}") == "INVALID" and not traj[-1].unresolved and bool(traj[-1].preserved)


def plant_evaluator(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    by_fc: dict[str, list[str]] = {}
    for c in acc:
        by_fc.setdefault(w.claims[c].failure_class, []).append(c)
    if len(by_fc) < 2:
        return None
    fc_a, fc_b = rng.sample(sorted(by_fc), 2)
    a = rng.choice(by_fc[fc_a]); bclaim = rng.choice(by_fc[fc_b])
    w.evaluators["ev0"] = Evaluator("ev0", tuple(sorted({fc_a, fc_b} | set(w.evaluators["ev0"].coverage))))
    fa = w.families_of(a)[0]; fb = w.families_of(bclaim)[0]
    w.evidence[fa.evidence_ids[0]].evaluator_id = "ev0"; w.evidence[fb.evidence_ids[0]].evaluator_id = "ev0"
    variant = rng.choice(("BLIND", "REPLACED_NARROWER", "FAILURE_CLASS_CHANGED"))
    if variant == "FAILURE_CLASS_CHANGED":
        # a's evidence is evaluated by an evaluator that will not cover the new class
        new_fc = [x for x in FAILURE_CLASSES if x not in w.evaluators["ev0"].coverage]
        if not new_fc:
            new_fc = [fc_b]
            w.evaluators["ev0"] = Evaluator("ev0", tuple(x for x in w.evaluators["ev0"].coverage if x != fc_b) or (fc_a,))
            if fc_b in w.evaluators["ev0"].coverage:
                return None
            w.evidence[fb.evidence_ids[0]].evaluator_id = ""
        events = [Event("CLAIM_FAILURE_CLASS_CHANGED", {"claim_id": a, "failure_class": new_fc[0]})]
    else:
        events = [Event("EVALUATOR_COVERAGE_CHANGED", {"evaluator_id": "ev0", "coverage": [x for x in w.evaluators["ev0"].coverage if x != fc_a], "uncertain": []}, note=variant)]
    return events, {"variant": variant, "touched_claim": a, "sibling_claim": bclaim, "evaluator": "ev0"}


def inv_evaluator(traj: list[Expected], f: dict[str, Any], w_final: World) -> bool:
    atoms = condition_table(w_final).atoms
    last = traj[-1]
    touched_atoms = [k for k, v in atoms.items() if k.startswith("evc:") and v == "INVALID" and w_final.evidence[k[4:]].claim_id == f["touched_claim"]]
    return bool(touched_atoms) and f["sibling_claim"] in last.preserved and not last.unresolved


def plant_scope_changed(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    c = rng.choice(acc)
    claim = w.claims[c]
    fams = w.families_of(c)
    missing = [s for s in SCOPE_ELEMENTS if s not in claim.scope]
    if not missing:
        claim.scope = tuple(claim.scope[:1]); missing = [s for s in SCOPE_ELEMENTS if s not in claim.scope]
    new_el = rng.choice(missing)
    # first family: coverage restricted to the old scope; if a second family exists, make it cover the new scope
    for e in fams[0].evidence_ids:
        w.evidence[e].scope_coverage = tuple(claim.scope)
    covering = ""
    if len(fams) >= 2 and rng.random() < 0.7:
        e0 = w.evidence[fams[1].evidence_ids[0]]
        e0.scope_coverage = tuple(sorted(set(e0.scope_coverage) | {new_el} | set(claim.scope)))
        covering = fams[1].family_id
    else:
        for fam in fams[1:]:
            for e in fam.evidence_ids:
                w.evidence[e].scope_coverage = tuple(x for x in w.evidence[e].scope_coverage if x != new_el) or tuple(claim.scope)
    new_scope = tuple(sorted(set(claim.scope) | {new_el}))
    return [Event("CLAIM_SCOPE_CHANGED", {"claim_id": c, "scope": list(new_scope)})], {"target_claim": c, "old_family": fams[0].family_id, "covering_family": covering}


def inv_scope_changed(traj: list[Expected], f: dict[str, Any], w_final: World) -> bool:
    atoms = condition_table(w_final).atoms
    last = traj[-1]
    if atoms.get(f"scope:{f['old_family']}") != "INVALID":
        return False
    if f["covering_family"]:
        return f["target_claim"] in last.preserved and atoms.get(f"scope:{f['covering_family']}") == "VALID"
    return f["target_claim"] in last.reopened


def plant_new_support(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    c = rng.choice(acc)
    claim = w.claims[c]
    b.n_ev += 1; b.n_fam += 1
    eid = f"e{b.n_ev:02d}"; fid = f"{c}.F{b.n_fam}"
    new_src = "src_new"
    w.sources[new_src] = SOURCE_VALID
    evidence = {"evidence_id": eid, "claim_id": c, "source_id": new_src, "context_id": claim.context_id, "scope_coverage": list(claim.scope), "evaluator_id": "ev0", "calibration_id": "", "data_id": "data:src_new", "model_id": "", "instrument_id": "", "supports": True}
    family = {"family_id": fid, "claim_id": c, "evidence_ids": [eid], "prerequisite_ids": [], "min_independent": 0, "required_relation": ""}
    add = Event("FAMILY_ADDED", {"family": family, "evidence": [evidence]})
    variant = rng.choice(("ADD_ONLY", "FAIL_THEN_ADD"))
    if variant == "ADD_ONLY":
        return [add], {"variant": variant, "target_claim": c}
    # make every family of c share one source, retract it, then add the new family
    s = rng.choice(sorted(x for x in w.sources if x not in ("src_unused", new_src)))
    for fam in w.families_of(c):
        w.evidence[fam.evidence_ids[0]].source_id = s
    for other in acc:
        if other == c:
            continue
        for fam in w.families_of(other):
            for e in fam.evidence_ids:
                if w.evidence[e].source_id == s:
                    w.evidence[e].source_id = rng.choice(sorted(x for x in w.sources if x not in (s, "src_unused", new_src)))
    return [Event("SOURCE_RETRACTED", {"source_id": s}), add], {"variant": variant, "target_claim": c, "retracted_source": s}


def inv_new_support(traj: list[Expected], f: dict[str, Any]) -> bool:
    last = traj[-1]
    if last.reopened or last.unresolved:
        return False
    if f["variant"] == "FAIL_THEN_ADD":
        return f["target_claim"] in traj[0].reopened and f["target_claim"] in last.preserved
    return True


def plant_correction(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    variant = rng.choice(("SOURCE", "CALIBRATION"))
    acc = list(w.accepted_ids())
    c = rng.choice(acc)
    if variant == "SOURCE":
        s = rng.choice(sorted(x for x in w.sources if x != "src_unused"))
        for fam in w.families_of(c):
            w.evidence[fam.evidence_ids[0]].source_id = s
        return [Event("SOURCE_RETRACTED", {"source_id": s}), Event("SOURCE_CORRECTED", {"source_id": s})], {"variant": variant, "target_claim": c, "entity": s}
    cal = rng.choice(sorted(x for x in w.calibrations if "unused" not in x))
    for fam in w.families_of(c):
        w.evidence[fam.evidence_ids[0]].calibration_id = cal
        w.evidence[fam.evidence_ids[0]].instrument_id = w.calibrations[cal].instrument_id
    return [Event("CALIBRATION_INVALIDATED", {"calibration_id": cal}), Event("CALIBRATION_REVALIDATED", {"calibration_id": cal})], {"variant": variant, "target_claim": c, "entity": cal}


def inv_correction(traj: list[Expected], f: dict[str, Any]) -> bool:
    return f["target_claim"] in traj[0].reopened and not traj[-1].reopened and not traj[-1].unresolved


def plant_partial_failure(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    multi = _accepted_with_n_families(w, 2)
    if not multi:
        return None
    c = rng.choice(multi)
    fams = w.families_of(c)
    s = rng.choice(sorted(x for x in w.sources if x != "src_unused"))
    hit = fams[: rng.randint(1, len(fams) - 1)]
    for fam in hit:
        w.evidence[fam.evidence_ids[0]].source_id = s
    for fam in fams[len(hit):]:
        for e in fam.evidence_ids:
            if w.evidence[e].source_id == s:
                w.evidence[e].source_id = rng.choice(sorted(x for x in w.sources if x not in (s, "src_unused")))
    return [Event("SOURCE_RETRACTED", {"source_id": s})], {"target_claim": c, "defeated_families": [f.family_id for f in hit], "source": s}


def inv_partial_failure(traj: list[Expected], f: dict[str, Any]) -> bool:
    return f["target_claim"] in traj[-1].preserved and not traj[-1].unresolved


def plant_all_failed(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    # need a claim with at least one dependent
    dependents: dict[str, list[str]] = {}
    for fam in w.families.values():
        for p in fam.prerequisite_ids:
            dependents.setdefault(p, []).append(fam.claim_id)
    with_dep = [c for c in acc if c in dependents]
    if not with_dep:
        return None
    c = rng.choice(with_dep)
    variant = rng.choice(("SHARED_SOURCE", "CONTRADICTION", "SEQUENCE"))
    fams = w.families_of(c)
    if variant == "SHARED_SOURCE":
        s = rng.choice(sorted(x for x in w.sources if x != "src_unused"))
        for fam in fams:
            w.evidence[fam.evidence_ids[0]].source_id = s
        events = [Event("SOURCE_RETRACTED", {"source_id": s})]
    elif variant == "CONTRADICTION":
        b.n_ev += 1
        eid = f"e{b.n_ev:02d}"
        w.sources["src_contra"] = SOURCE_VALID
        ev = {"evidence_id": eid, "claim_id": c, "source_id": "src_contra", "context_id": w.claims[c].context_id, "scope_coverage": list(w.claims[c].scope), "evaluator_id": "", "calibration_id": "", "data_id": "data:src_contra", "model_id": "", "instrument_id": "", "supports": False}
        events = [Event("EVIDENCE_ADDED", {"evidence": ev}, note="contradiction registered")]
    else:
        srcs = sorted(x for x in w.sources if x != "src_unused")
        if len(srcs) < 2:
            return None
        s1, s2 = rng.sample(srcs, 2)
        for i, fam in enumerate(fams):
            w.evidence[fam.evidence_ids[0]].source_id = s1 if i % 2 == 0 else s2
        events = [Event("SOURCE_RETRACTED", {"source_id": s1}), Event("SOURCE_RETRACTED", {"source_id": s2})]
    return events, {"variant": variant, "target_claim": c, "dependents": sorted(set(dependents[c]))}


def inv_all_failed(traj: list[Expected], f: dict[str, Any]) -> bool:
    return f["target_claim"] in traj[-1].reopened and not traj[-1].unresolved


def plant_cannot_check(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    variant = rng.choice(("SOURCE_DISPUTED", "CALIBRATION_REVIEW", "DEPENDENCE_SUSPECTED", "RELATION_CANNOT_CHECK", "EVALUATOR_UNCERTAIN"))
    multi = _accepted_with_n_families(w, 2)
    c = rng.choice(acc)
    if variant == "SOURCE_DISPUTED":
        s = rng.choice(sorted(x for x in w.sources if x != "src_unused"))
        for fam in w.families_of(c):
            w.evidence[fam.evidence_ids[0]].source_id = s
        events = [Event("SOURCE_RETRACTION_DISPUTED", {"source_id": s})]
    elif variant == "CALIBRATION_REVIEW":
        cal = rng.choice(sorted(x for x in w.calibrations if "unused" not in x))
        for fam in w.families_of(c):
            w.evidence[fam.evidence_ids[0]].calibration_id = cal
            w.evidence[fam.evidence_ids[0]].instrument_id = w.calibrations[cal].instrument_id
        events = [Event("CALIBRATION_UNDER_REVIEW", {"calibration_id": cal})]
    elif variant == "DEPENDENCE_SUSPECTED":
        cands = [fam for fam in w.families_of(c) if len(w.positive_evidence_of_family(fam)) >= 2]
        if not cands:
            return None
        fam = cands[0]; fam.min_independent = 2
        pos = [e.evidence_id for e in w.positive_evidence_of_family(fam)]
        events = [Event("DEPENDENCE_SUSPECTED", {"left_id": pos[0], "right_id": pos[1], "kind": rng.choice(DEP_KINDS)})]
    elif variant == "RELATION_CANNOT_CHECK":
        claim = w.claims[c]; fam = w.families_of(c)[0]
        e, req = b.transported_evidence(claim, family_required="DECISION_DOMINATES")
        key = w.relation_key(e.context_id, claim.context_id)
        if RELATION_RANK[w.relations[key].relation_type] < RELATION_RANK[req]:
            w.relations[key].relation_type = "ISOMORPHIC"
        fam.evidence_ids = tuple(fam.evidence_ids) + (e.evidence_id,); fam.required_relation = req
        events = [Event("RELATION_RETYPED", {"source_context": e.context_id, "target_context": claim.context_id, "relation_type": RELATION_CANNOT_CHECK})]
    else:
        fc = w.claims[c].failure_class
        for fam in w.families_of(c):
            w.evidence[fam.evidence_ids[0]].evaluator_id = "ev0"
        cov = [x for x in w.evaluators["ev0"].coverage if x != fc]
        events = [Event("EVALUATOR_COVERAGE_CHANGED", {"evaluator_id": "ev0", "coverage": cov, "uncertain": [fc]})]
    # sibling with an alternative intact family (censored + alternative = preserved) when available
    sibling = ""
    if variant in ("SOURCE_DISPUTED", "CALIBRATION_REVIEW"):
        alt = [x for x in multi if x != c]
        if alt:
            sibling = rng.choice(alt)
            fam0 = w.families_of(sibling)[0]
            ent = events[0].payload.get("source_id") or events[0].payload.get("calibration_id")
            if "source_id" in events[0].payload:
                w.evidence[fam0.evidence_ids[0]].source_id = ent
            else:
                w.evidence[fam0.evidence_ids[0]].calibration_id = ent; w.evidence[fam0.evidence_ids[0]].instrument_id = w.calibrations[ent].instrument_id
            for fam in w.families_of(sibling)[1:]:
                for e in fam.evidence_ids:
                    if w.evidence[e].source_id == ent:
                        w.evidence[e].source_id = rng.choice(sorted(x for x in w.sources if x not in (ent, "src_unused")))
                    if w.evidence[e].calibration_id == ent:
                        w.evidence[e].calibration_id = ""
    return events, {"variant": variant, "target_claim": c, "sibling_preserved": sibling}


def inv_cannot_check(traj: list[Expected], f: dict[str, Any]) -> bool:
    last = traj[-1]
    if not last.unresolved or len(last.unknown_atoms) > MAX_UNKNOWN_ATOMS:
        return False
    if f["sibling_preserved"] and f["sibling_preserved"] not in last.preserved:
        return False
    return True


def plant_no_reopening(b: _Builder) -> tuple[list[Event], dict[str, Any]] | None:
    rng, w = b.rng, b.w
    acc = list(w.accepted_ids())
    c = rng.choice(acc)
    claim = w.claims[c]
    options = ["UNUSED_SOURCE", "SCOPE_NARROWED", "RELATION_UPGRADED", "EVALUATOR_WIDENED", "IRRELEVANT_DEPENDENCE", "UNUSED_CALIBRATION"]
    if "alt0" in w.claims:
        options.append("ALTERNATIVE_NEGATIVE_SOURCE_RETRACTED")
    picks = rng.sample(options, rng.randint(1, 2))
    events: list[Event] = []
    touching = False
    for v in picks:
        if v == "UNUSED_SOURCE":
            events.append(Event("SOURCE_RETRACTED", {"source_id": "src_unused"}))
        elif v == "UNUSED_CALIBRATION":
            events.append(Event("CALIBRATION_INVALIDATED", {"calibration_id": "cal:inst_unused:0"}))
        elif v == "SCOPE_NARROWED":
            if len(claim.scope) >= 2:
                events.append(Event("CLAIM_SCOPE_CHANGED", {"claim_id": c, "scope": list(claim.scope[:1])})); touching = True
        elif v == "RELATION_UPGRADED":
            keys = sorted(k for k, r in w.relations.items() if r.relation_type != "ISOMORPHIC")
            if keys:
                k = rng.choice(keys); r = w.relations[k]
                events.append(Event("RELATION_RETYPED", {"source_context": r.source_context, "target_context": r.target_context, "relation_type": "ISOMORPHIC"})); touching = True
        elif v == "EVALUATOR_WIDENED":
            events.append(Event("EVALUATOR_COVERAGE_CHANGED", {"evaluator_id": "ev1", "coverage": list(FAILURE_CLASSES), "uncertain": []})); touching = True
        elif v == "IRRELEVANT_DEPENDENCE":
            fams = [fam for fam in w.families.values() if len(w.positive_evidence_of_family(fam)) >= 2 and w.claims[fam.claim_id].accepted_v0]
            if fams:
                fam = rng.choice(sorted(fams, key=lambda x: x.family_id))
                pos = [e.evidence_id for e in w.positive_evidence_of_family(fam)]
                if len(pos) >= 3 and rng.random() < 0.5:
                    fam.min_independent = 2
                else:
                    fam.min_independent = 0
                events.append(Event("DEPENDENCE_DISCOVERED", {"left_id": pos[0], "right_id": pos[1], "kind": rng.choice(DEP_KINDS)})); touching = True
        elif v == "ALTERNATIVE_NEGATIVE_SOURCE_RETRACTED":
            neg = w.negative_evidence_against("alt0")
            if neg:
                s = neg[0].source_id
                if not any(e.source_id == s and e.supports for e in w.evidence.values()):
                    events.append(Event("SOURCE_RETRACTED", {"source_id": s}, note="negative evidence against a rejected alternative")); touching = True
    if not events or not touching:
        return None
    return events, {"variants": picks, "target_claim": c}


def inv_no_reopening(traj: list[Expected], f: dict[str, Any]) -> bool:
    return all(not x.reopened and not x.unresolved for x in traj)


PLANTERS: dict[str, tuple[Callable[[_Builder], Any], Callable[..., bool]]] = {
    "SOURCE_RETRACTED": (plant_source_retracted, lambda traj, f, w: inv_source_retracted(traj, f)),
    "DEPENDENCE_DISCOVERED": (plant_dependence_discovered, inv_dependence_discovered),
    "CALIBRATION_INVALIDATED": (plant_calibration_invalidated, inv_calibration_invalidated),
    "TRANSPORT_RELATION_INVALIDATED": (plant_transport_invalidated, inv_transport_invalidated),
    "EVALUATOR_BLIND_OR_REPLACED": (plant_evaluator, inv_evaluator),
    "PROBLEM_SCOPE_CHANGED": (plant_scope_changed, inv_scope_changed),
    "NEW_INDEPENDENT_SUPPORT": (plant_new_support, lambda traj, f, w: inv_new_support(traj, f)),
    "CORRECTION_RESTORES_SUPPORT": (plant_correction, lambda traj, f, w: inv_correction(traj, f)),
    "PARTIAL_SUPPORT_FAILURE": (plant_partial_failure, lambda traj, f, w: inv_partial_failure(traj, f)),
    "ALL_SUFFICIENT_SUPPORT_FAILED": (plant_all_failed, lambda traj, f, w: inv_all_failed(traj, f)),
    "CANNOT_CHECK_EDGE": (plant_cannot_check, lambda traj, f, w: inv_cannot_check(traj, f)),
    "NO_REOPENING_NEEDED": (plant_no_reopening, lambda traj, f, w: inv_no_reopening(traj, f)),
}
assert set(PLANTERS) == set(STRATA)


def generate_instance(split: str, split_seed: str, stratum: str, index: int) -> tuple[Instance, list[Expected]]:
    seed = instance_seed(split_seed, stratum, index)
    rng = random.Random(seed)
    planter, invariant = PLANTERS[stratum]
    for attempt in range(MAX_ATTEMPTS):
        b = build_base_world(rng)
        try:
            planted = planter(b)
        except IndexError:  # planter anchored on a prerequisite-only family: reject this base world
            continue
        if planted is None:
            continue
        events, feats = planted
        w0 = b.w
        try:
            w0.validate()
            if not all_accepted_supported_at_v0(w0):
                continue
            accepted = w0.accepted_ids()
            traj = expected_trajectory(w0, events, accepted)
        except ValueError:
            continue
        w_final = w0
        for ev in events:
            w_final = apply_event(w_final, ev)
        if any(not x.exhaustive_agrees for x in traj):
            raise RuntimeError(f"oracle self-disagreement on {stratum}#{index}")
        if any(len(x.unknown_atoms) > MAX_UNKNOWN_ATOMS for x in traj):
            continue
        if not invariant(traj, feats, w_final):
            continue
        feats = dict(feats); feats["attempts"] = attempt + 1
        inst = Instance(f"{split}-{stratum}-{index:03d}", stratum, split, seed, w0, events, feats)
        return inst, traj
    raise RuntimeError(f"could not plant {stratum} within {MAX_ATTEMPTS} attempts (seed {seed})")


def generate_split(split: str, split_seed: str, per_stratum: dict[str, int]) -> list[tuple[Instance, list[Expected]]]:
    out = []
    for stratum in STRATA:
        for i in range(per_stratum.get(stratum, 0)):
            out.append(generate_instance(split, split_seed, stratum, i))
    return out


# ---- hand-authored known-answer fixtures (G0a) ---------------------------------

def _mini_world() -> World:
    w = World()
    for s in ("sA", "sB", "sC", "sD"):
        w.sources[s] = SOURCE_VALID
    w.calibrations["cal1"] = Calibration("cal1", "inst"); w.calibrations["cal2"] = Calibration("cal2", "inst")
    w.evaluators["evX"] = Evaluator("evX", ("FC_A", "FC_B"))
    w.relations["ctx1->ctx0"] = Relation("ctx1", "ctx0", "BEHAVIORALLY_EQUIVALENT")
    return w


def _claim(w: World, cid: str, fc: str = "FC_A", scope=("S1",), ctx: str = "ctx0", accepted: bool = True, alt_of: str = "") -> Claim:
    c = Claim(cid, ctx, fc, tuple(scope), accepted, alt_of); w.claims[cid] = c; return c


def _ev(w: World, eid: str, cid: str, src: str, *, ctx: str = "ctx0", cov=("S1",), cal: str = "", ev: str = "", supports: bool = True) -> str:
    w.evidence[eid] = Evidence(eid, cid, src, ctx, tuple(cov), ev, cal, supports=supports); return eid


def _fam(w: World, fid: str, cid: str, evs, prereqs=(), k: int = 0, req: str = "") -> str:
    w.families[fid] = Family(fid, cid, tuple(evs), tuple(prereqs), k, req); return fid


def known_answer_fixtures() -> list[dict[str, Any]]:
    """Twelve hand-authored instances with hand-computed expected sets.
    `expected` lists the final-version sets; `expected_trajectory` when the
    sequence has intermediate versions."""
    fx: list[dict[str, Any]] = []

    # 1 SOURCE_RETRACTED: shared ancestry; c0 has alternative family, c1 does not; c2 depends on c1.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1"); _claim(w, "c2")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA")]); _fam(w, "c0.F2", "c0", [_ev(w, "e2", "c0", "sB")])
    _fam(w, "c1.F1", "c1", [_ev(w, "e3", "c1", "sA")]); _fam(w, "c2.F1", "c2", [], prereqs=["c1"])
    fx.append({"name": "KA-01-SOURCE_RETRACTED", "stratum": "SOURCE_RETRACTED", "world": w, "events": [Event("SOURCE_RETRACTED", {"source_id": "sA"})], "expected": {"reopened": ["c1", "c2"], "preserved": ["c0"], "unresolved": []}})

    # 2 DEPENDENCE_DISCOVERED: F1 needs 2 independent; discovered shared data; decoy family without requirement.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA"), _ev(w, "e2", "c0", "sB")], k=2)
    _fam(w, "c1.F1", "c1", [_ev(w, "e3", "c1", "sC"), _ev(w, "e4", "c1", "sD")], k=0)
    fx.append({"name": "KA-02-DEPENDENCE_DISCOVERED", "stratum": "DEPENDENCE_DISCOVERED", "world": w, "events": [Event("DEPENDENCE_DISCOVERED", {"left_id": "e1", "right_id": "e2", "kind": "SHARED_DATA"}), Event("DEPENDENCE_DISCOVERED", {"left_id": "e3", "right_id": "e4", "kind": "SHARED_DATA"})], "expected": {"reopened": ["c0"], "preserved": ["c1"], "unresolved": []}})

    # 3 CALIBRATION_INVALIDATED: same instrument, different calibration preserved.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA", cal="cal1")]); _fam(w, "c1.F1", "c1", [_ev(w, "e2", "c1", "sA", cal="cal2")])
    fx.append({"name": "KA-03-CALIBRATION_INVALIDATED", "stratum": "CALIBRATION_INVALIDATED", "world": w, "events": [Event("CALIBRATION_INVALIDATED", {"calibration_id": "cal1"})], "expected": {"reopened": ["c0"], "preserved": ["c1"], "unresolved": []}})

    # 4 TRANSPORT: c0 uses transported e1 requiring PREDICTIVELY_EQUIVALENT; relation downgraded to APPROXIMATELY_EQUIVALENT.
    #   c1 uses the same relation but only requires APPROXIMATELY_EQUIVALENT -> preserved.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA", ctx="ctx1")], req="PREDICTIVELY_EQUIVALENT")
    _fam(w, "c1.F1", "c1", [_ev(w, "e2", "c1", "sB", ctx="ctx1")], req="APPROXIMATELY_EQUIVALENT")
    fx.append({"name": "KA-04-TRANSPORT_RELATION_INVALIDATED", "stratum": "TRANSPORT_RELATION_INVALIDATED", "world": w, "events": [Event("RELATION_RETYPED", {"source_context": "ctx1", "target_context": "ctx0", "relation_type": "APPROXIMATELY_EQUIVALENT"})], "expected": {"reopened": ["c0"], "preserved": ["c1"], "unresolved": []}})

    # 5 EVALUATOR blind to FC_A: c0 (FC_A) reopened, c1 (FC_B) preserved though same evaluator.
    w = _mini_world(); _claim(w, "c0", "FC_A"); _claim(w, "c1", "FC_B")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA", ev="evX")]); _fam(w, "c1.F1", "c1", [_ev(w, "e2", "c1", "sB", ev="evX")])
    fx.append({"name": "KA-05-EVALUATOR_BLIND", "stratum": "EVALUATOR_BLIND_OR_REPLACED", "world": w, "events": [Event("EVALUATOR_COVERAGE_CHANGED", {"evaluator_id": "evX", "coverage": ["FC_B"], "uncertain": []})], "expected": {"reopened": ["c0"], "preserved": ["c1"], "unresolved": []}})

    # 6 SCOPE change: F1 covers S1 only, F2 covers S1,S2 -> preserved; c1 only S1 -> reopened.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA", cov=("S1",))]); _fam(w, "c0.F2", "c0", [_ev(w, "e2", "c0", "sB", cov=("S1", "S2"))])
    _fam(w, "c1.F1", "c1", [_ev(w, "e3", "c1", "sC", cov=("S1",))])
    fx.append({"name": "KA-06-PROBLEM_SCOPE_CHANGED", "stratum": "PROBLEM_SCOPE_CHANGED", "world": w, "events": [Event("CLAIM_SCOPE_CHANGED", {"claim_id": "c0", "scope": ["S1", "S2"]}), Event("CLAIM_SCOPE_CHANGED", {"claim_id": "c1", "scope": ["S1", "S2"]})], "expected": {"reopened": ["c1"], "preserved": ["c0"], "unresolved": []}})

    # 7 NEW_INDEPENDENT_SUPPORT: retraction reopens c0 and dependent c1; new family restores both.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA")]); _fam(w, "c1.F1", "c1", [], prereqs=["c0"])
    new_e = {"evidence_id": "e9", "claim_id": "c0", "source_id": "sD", "context_id": "ctx0", "scope_coverage": ["S1"], "evaluator_id": "", "calibration_id": "", "data_id": "", "model_id": "", "instrument_id": "", "supports": True}
    fx.append({"name": "KA-07-NEW_INDEPENDENT_SUPPORT", "stratum": "NEW_INDEPENDENT_SUPPORT", "world": w, "events": [Event("SOURCE_RETRACTED", {"source_id": "sA"}), Event("FAMILY_ADDED", {"family": {"family_id": "c0.F9", "claim_id": "c0", "evidence_ids": ["e9"], "prerequisite_ids": [], "min_independent": 0, "required_relation": ""}, "evidence": [new_e]})], "expected_trajectory": [{"reopened": ["c0", "c1"], "preserved": [], "unresolved": []}, {"reopened": [], "preserved": ["c0", "c1"], "unresolved": []}], "expected": {"reopened": [], "preserved": ["c0", "c1"], "unresolved": []}})

    # 8 CORRECTION_RESTORES_SUPPORT
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA", cal="cal1")]); _fam(w, "c1.F1", "c1", [_ev(w, "e2", "c1", "sB")])
    fx.append({"name": "KA-08-CORRECTION_RESTORES_SUPPORT", "stratum": "CORRECTION_RESTORES_SUPPORT", "world": w, "events": [Event("CALIBRATION_INVALIDATED", {"calibration_id": "cal1"}), Event("CALIBRATION_REVALIDATED", {"calibration_id": "cal1"})], "expected_trajectory": [{"reopened": ["c0"], "preserved": ["c1"], "unresolved": []}, {"reopened": [], "preserved": ["c0", "c1"], "unresolved": []}], "expected": {"reopened": [], "preserved": ["c0", "c1"], "unresolved": []}})

    # 9 PARTIAL_SUPPORT_FAILURE: one of two families fails; downstream preserved.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA")]); _fam(w, "c0.F2", "c0", [_ev(w, "e2", "c0", "sB")]); _fam(w, "c1.F1", "c1", [_ev(w, "e3", "c1", "sC")], prereqs=["c0"])
    fx.append({"name": "KA-09-PARTIAL_SUPPORT_FAILURE", "stratum": "PARTIAL_SUPPORT_FAILURE", "world": w, "events": [Event("SOURCE_RETRACTED", {"source_id": "sA"})], "expected": {"reopened": [], "preserved": ["c0", "c1"], "unresolved": []}})

    # 10 ALL_SUFFICIENT_SUPPORT_FAILED via contradiction; c1 (only prereq c0) reopened; c2 (own alternative) preserved.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1"); _claim(w, "c2")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA")]); _fam(w, "c0.F2", "c0", [_ev(w, "e2", "c0", "sB")])
    _fam(w, "c1.F1", "c1", [], prereqs=["c0"]); _fam(w, "c2.F1", "c2", [], prereqs=["c0"]); _fam(w, "c2.F2", "c2", [_ev(w, "e3", "c2", "sC")])
    neg = {"evidence_id": "e8", "claim_id": "c0", "source_id": "sD", "context_id": "ctx0", "scope_coverage": ["S1"], "evaluator_id": "", "calibration_id": "", "data_id": "", "model_id": "", "instrument_id": "", "supports": False}
    fx.append({"name": "KA-10-ALL_SUFFICIENT_SUPPORT_FAILED", "stratum": "ALL_SUFFICIENT_SUPPORT_FAILED", "world": w, "events": [Event("EVIDENCE_ADDED", {"evidence": neg})], "expected": {"reopened": ["c0", "c1"], "preserved": ["c2"], "unresolved": []}})

    # 11 CANNOT_CHECK_EDGE: disputed retraction; c0 only support -> unresolved; c1 alternative -> preserved; c2 depends on c0 -> unresolved.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "c1"); _claim(w, "c2")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA")]); _fam(w, "c1.F1", "c1", [_ev(w, "e2", "c1", "sA")]); _fam(w, "c1.F2", "c1", [_ev(w, "e3", "c1", "sB")]); _fam(w, "c2.F1", "c2", [], prereqs=["c0"])
    fx.append({"name": "KA-11-CANNOT_CHECK_EDGE", "stratum": "CANNOT_CHECK_EDGE", "world": w, "events": [Event("SOURCE_RETRACTION_DISPUTED", {"source_id": "sA"})], "expected": {"reopened": [], "preserved": ["c1"], "unresolved": ["c0", "c2"]}})

    # 12 NO_REOPENING_NEEDED: unused source retracted; evaluator widened; dependence in a family with k satisfied; alternative's negative evidence retracted.
    w = _mini_world(); _claim(w, "c0"); _claim(w, "alt0", accepted=False, alt_of="c0")
    _fam(w, "c0.F1", "c0", [_ev(w, "e1", "c0", "sA"), _ev(w, "e2", "c0", "sB"), _ev(w, "e3", "c0", "sC")], k=2)
    _fam(w, "alt0.F1", "alt0", [_ev(w, "e4", "alt0", "sB")]); _ev(w, "e5", "alt0", "sD", supports=False)
    w.sources["sU"] = SOURCE_VALID
    fx.append({"name": "KA-12-NO_REOPENING_NEEDED", "stratum": "NO_REOPENING_NEEDED", "world": w, "events": [Event("SOURCE_RETRACTED", {"source_id": "sU"}), Event("DEPENDENCE_DISCOVERED", {"left_id": "e1", "right_id": "e2", "kind": "SHARED_DATA"}), Event("EVALUATOR_COVERAGE_CHANGED", {"evaluator_id": "evX", "coverage": ["FC_A", "FC_B", "FC_C"], "uncertain": []}), Event("SOURCE_RETRACTED", {"source_id": "sD"})], "expected": {"reopened": [], "preserved": ["c0"], "unresolved": []}})
    for f in fx:
        f["world"].validate()
    return fx


def separation_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    """H-EXT-3 finite separation example (local compatibility / global obstruction).

    P: c has F1={e1,e2 | k=2} and F2={e3 transported via ctx1->ctx0, requires PREDICTIVELY_EQUIVALENT}.
    Q: c has F1={e1,e2,e3(transported) | k=2 over e1,e2} and F2={e4 native}.
    Events (identical): dependence discovered (e1,e2) AND relation ctx1->ctx0 downgraded.
    Per-module family-anonymous verdicts are identical (DEP: DEFEATS_SOME, TRANSPORT: DEFEATS_SOME,
    PROV/EVAL/SCOPE/CONTRA: DEFEATS_NONE) in P and Q, but the oracle differs:
    P -> c REOPENED (defeats cover all families), Q -> c PRESERVED (F2 intact)."""
    events = [Event("DEPENDENCE_DISCOVERED", {"left_id": "e1", "right_id": "e2", "kind": "SHARED_DATA"}), Event("RELATION_RETYPED", {"source_context": "ctx1", "target_context": "ctx0", "relation_type": "APPROXIMATELY_EQUIVALENT"})]
    p = _mini_world(); _claim(p, "c")
    _fam(p, "c.F1", "c", [_ev(p, "e1", "c", "sA"), _ev(p, "e2", "c", "sB")], k=2)
    _fam(p, "c.F2", "c", [_ev(p, "e3", "c", "sC", ctx="ctx1")], req="PREDICTIVELY_EQUIVALENT")
    q = _mini_world(); _claim(q, "c")
    _fam(q, "c.F1", "c", [_ev(q, "e1", "c", "sA"), _ev(q, "e2", "c", "sB"), _ev(q, "e3", "c", "sC", ctx="ctx1")], k=2, req="PREDICTIVELY_EQUIVALENT")
    _fam(q, "c.F2", "c", [_ev(q, "e4", "c", "sD")])
    p.validate(); q.validate()
    return ({"name": "SEP-P", "world": p, "events": events, "expected": {"reopened": ["c"], "preserved": [], "unresolved": []}},
            {"name": "SEP-Q", "world": q, "events": events, "expected": {"reopened": [], "preserved": ["c"], "unresolved": []}})
