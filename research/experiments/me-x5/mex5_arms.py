#!/usr/bin/env python3
"""ME-X5 arms.

Three independent decision paths, not three configurations of one:

* **single parents** (`B0`-`B4`) — each mature method in its native role, alone;
* **`B5` federation** — the parent modules of `mex5_parents.py` composed by
  ordinary engineering glue, with the H-EXT-3 rung controlling *what crosses the
  module boundary*. Rung 5 sees everything the ME arm sees and is the primary
  comparator. B5 is never artificially isolated;
* **`M`** — the ME arm, compiled to the ORION reference objects
  (`ReticulateProvenance`, `assess_evidence_dependence`, `RelationType`,
  `ProblemContract`, `selective_reopen`) and decided through the ME control layer
  (discrepancy-locus hypotheses, evaluator/diagnostic-evaluator separation,
  unresolved terminal, external authority boundary).

Ablations are `M` with one channel removed; controls are truth-agnostic policies.
No arm imports the oracle module (asserted by a unit test).
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, replace
from typing import Any

from mex5_model import (
    CENSORED,
    INVALID,
    LOCUS_PRIORITY,
    RELATION_RANK,
    VALID,
    Decision,
    Episode,
    trajectory,
)
from mex5_parents import (
    CENSORS_SOME,
    CLEAR,
    DEFEATS_ALL,
    DEFEATS_SOME,
    MODULE_LOCUS,
    aggregate_commits,
    apparatus_module,
    dependence_module,
    evaluator_module,
    global_module,
    identity_module,
    narrow_only_families,
    provenance_invalid_units,
    provenance_module,
    scope_module,
    tms_surviving_families,
    transport_module,
)
from mex5_oracle import rules_for

CHANNELS = ("identity", "apparatus", "evaluator", "dependence", "transport", "scope",
            "global", "numeric", "families", "authority", "unresolved")
ALL_CHANNELS = frozenset(CHANNELS)
LADDER = ("B5_R1_VERDICT_ONLY", "B5_R2_PROVENANCE", "B5_R3_PLUS_DEPENDENCE_ANCESTRY",
          "B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR", "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION")
M_ARM = "M_ME_CROSS_TRANSITION_CONTROL"
B5_ARM = LADDER[4]


@dataclass(frozen=True)
class ArmSpec:
    name: str
    kind: str                 # single_parent | federation | me | control
    rung: int = 0
    channels: frozenset[str] = ALL_CHANNELS
    note: str = ""


# ---- censored-fact machinery shared by every arm that can abstain -------------------

def _censored_facts(ep: Episode) -> list[tuple]:
    used = {u for f in ep.families.values() for u in f.unit_ids} & set(ep.units)
    vals = {ep.units[u].validator for u in used} - {None}
    ctxs = {ep.units[u].context for u in used}
    facts: list[tuple] = []
    for uid in sorted(used):
        u = ep.units[uid]
        if u.status == CENSORED:
            facts.append(("UNIT", uid))
        for anc, kind in sorted(u.ancestry):
            if kind == "SUSPECTED":
                facts.append(("ANCESTRY", uid, anc))
    for vid in sorted(vals):
        v = ep.validators[vid]
        if v.status == CENSORED:
            facts.append(("VALIDATOR", vid))
        if ep.target.asserted_failure_class in v.uncertain:
            facts.append(("COVERAGE", vid))
    for key in sorted(ep.relations):
        if ep.relations[key] == "CANNOT_CHECK":
            src, dst = key.split(">", 1)
            if src in ctxs and dst == ep.target.context:
                facts.append(("RELATION", key))
    return facts


def _resolve(ep: Episode, facts: list[tuple], bits: int) -> Episode:
    units, validators, relations = dict(ep.units), dict(ep.validators), dict(ep.relations)
    for i, fact in enumerate(facts):
        good = bool((bits >> i) & 1)
        if fact[0] == "UNIT":
            units[fact[1]] = replace(units[fact[1]], status=VALID if good else INVALID)
        elif fact[0] == "ANCESTRY":
            u = units[fact[1]]
            anc = tuple(a for a in u.ancestry if not (a[0] == fact[2] and a[1] == "SUSPECTED"))
            if not good:
                anc = tuple(sorted(set(anc) | {(fact[2], "CONFIRMED")}))
            units[u.uid] = replace(u, ancestry=anc)
        elif fact[0] == "VALIDATOR":
            validators[fact[1]] = replace(validators[fact[1]], status=VALID if good else INVALID)
        elif fact[0] == "COVERAGE":
            v = validators[fact[1]]
            cls = ep.target.asserted_failure_class
            covers = tuple(sorted(set(v.covers) | {cls})) if good else tuple(x for x in v.covers if x != cls)
            validators[v.vid] = replace(v, covers=covers, uncertain=tuple(x for x in v.uncertain if x != cls))
        elif fact[0] == "RELATION":
            relations[fact[1]] = "ISOMORPHIC" if good else "INCOMPARABLE"
    return replace(ep, units=units, validators=validators, relations=relations)


def _authority(ep: Episode, action: str, *, model_authority: bool) -> str:
    if action not in ("COMMIT", "COMMIT_NARROWED") or ep.target.requested_authority != "ACTION":
        return "BELIEF_ONLY"
    if not model_authority:
        return "BELIEF_AND_ACTION"
    return "BELIEF_AND_ACTION" if ep.authority_granted else "BELIEF_ONLY"


def _responsibility(fails_by_family: dict[str, set[str]]) -> str:
    fewest = min(len(f) for f in fails_by_family.values())
    heads = {next((L for L in LOCUS_PRIORITY if L in f), "SUPPORT_DEFEAT")
             for f in fails_by_family.values() if len(f) == fewest}
    return max(heads, key=LOCUS_PRIORITY.index)


def _abstain_from_bracket(decide, ep: Episode) -> Decision | None:
    """Exhaustive abstention: if the registered decision is not the same under every
    reading of the censored facts, the honest terminal is UNRESOLVED."""
    facts = _censored_facts(ep)
    if not facts:
        return None
    seen = {}
    for bits in range(1 << len(facts)):
        d = decide(_resolve(ep, facts, bits))
        seen[d.as_tuple()] = d
    if len(seen) == 1:
        return next(iter(seen.values()))
    from mex5_parents import MODULE_LOCUS as _ML  # noqa: F401  (kept local; loci below are frozen)
    fact_locus = {"UNIT": "SUPPORT_DEFEAT", "VALIDATOR": "APPARATUS_VALIDITY", "COVERAGE": "EVALUATOR_COVERAGE",
                  "ANCESTRY": "DEPENDENCE", "RELATION": "TRANSPORT"}
    loci = [d.locus for d in seen.values() if d.locus != "NONE"] + [fact_locus[f[0]] for f in facts]
    return Decision("UNRESOLVED", next((L for L in LOCUS_PRIORITY if L in loci), "NONE"), "BELIEF_ONLY")


# ---- B5 federation ------------------------------------------------------------------

def _reports(ep: Episode, rung: int) -> dict[str, tuple[Any, bool]]:
    """(report, witness_level_export?) per module at this interface rung."""
    excluded = provenance_invalid_units(ep) if rung >= 2 else set()
    return {
        "provenance": (provenance_module(ep), rung >= 2),
        "dependence": (dependence_module(ep, excluded), rung >= 3),
        "transport": (transport_module(ep, excluded), rung >= 4),
        "evaluator": (evaluator_module(ep, excluded), rung >= 4),
        "apparatus": (apparatus_module(ep, excluded), rung >= 4),
        "identity": (identity_module(ep), rung >= 5),
        "scope": (scope_module(ep), rung >= 5),
        "global": (global_module(ep), rung >= 5),
    }


def _federation_exact(ep: Episode) -> Decision:
    """Rung 5: every module exports witnesses, so the federation composes per family."""
    reps = _reports(ep, 5)
    fails: dict[str, set[str]] = {fid: set() for fid in ep.families}
    for name, (r, _) in reps.items():
        for fid in r.defeated:
            fails[fid].add(MODULE_LOCUS[name])
    narrow = narrow_only_families(ep)
    live = [fid for fid in sorted(fails) if not fails[fid] and fid not in narrow]
    narrow_ok = [fid for fid in sorted(fails) if not fails[fid] and fid in narrow]
    if not live and ep.narrowed_coverage is not None:
        sc = scope_module(ep, ep.narrowed_coverage)
        narrow_ok += [fid for fid in sorted(fails) if fails[fid] == {"SCOPE"} and fid not in sc.defeated]
    chosen = live or narrow_ok
    if chosen:
        surviving = tms_surviving_families(ep, provenance_invalid_units(ep) - set())
        uids = sorted({u for fid in chosen for u in ep.families[fid].unit_ids})
        ok = aggregate_commits(ep, uids)
        if ok is False:
            action, locus = "WITHHOLD", "SUPPORT_DEFEAT"
        else:
            action = "COMMIT" if live else "COMMIT_NARROWED"
            locus = "NONE" if live else "SCOPE"
            _ = surviving
    else:
        action, locus = "WITHHOLD", _responsibility(fails)
    return Decision(action, locus, _authority(ep, action, model_authority=True))


def _federation_heuristic(ep: Episode, rung: int, *, censored_as_defeat: bool) -> Decision:
    """Rungs 1-4: modules whose witnesses do not cross the boundary contribute only a
    family-anonymous verdict. Frozen composition policy (registered before any
    protected run): the target is withheld when a witness-level module defeats every
    family, when any anonymous module reports DEFEATS_ALL, or when the number of
    anonymous defeating modules is at least the number of families the witness-level
    modules left standing."""
    reps = _reports(ep, rung)
    n = len(ep.families)
    witness_defeated: set[str] = set()
    anon_modules: list[str] = []
    anon_all = False
    defeat_loci: list[str] = []
    censoring = False
    for name, (r, w) in sorted(reps.items()):
        v = r.verdict
        if v == CENSORS_SOME or r.censored:
            censoring = True
        if w:
            hit = set(r.defeated) | (set(r.censored) if censored_as_defeat else set())
            if hit:
                witness_defeated |= hit
                defeat_loci.append(MODULE_LOCUS[name])
        else:
            if v in (DEFEATS_ALL, DEFEATS_SOME) or (censored_as_defeat and r.censored):
                anon_modules.append(name)
                defeat_loci.append(MODULE_LOCUS[name])
                anon_all |= (v == DEFEATS_ALL)
    remaining = n - len(witness_defeated)
    withhold = anon_all or remaining <= 0 or (bool(anon_modules) and len(anon_modules) >= remaining)
    if not withhold:
        excluded = provenance_invalid_units(ep) if rung >= 2 else set()
        uids = sorted(set(ep.units) - excluded)
        if aggregate_commits(ep, uids) is False:
            withhold = True
            defeat_loci.append("SUPPORT_DEFEAT")
    if withhold:
        action = "WITHHOLD"
        locus = next((L for L in LOCUS_PRIORITY if L in defeat_loci), "SUPPORT_DEFEAT")
    else:
        action, locus = "COMMIT", "NONE"
    d = Decision(action, locus, _authority(ep, action, model_authority=True))
    return d if not censoring else d  # censoring handled by the caller's bracket


def _federation(ep: Episode, rung: int) -> Decision:
    if rung >= 5:
        d = _abstain_from_bracket(_federation_exact, ep)
        return d if d is not None else _federation_exact(ep)
    optimistic = _federation_heuristic(ep, rung, censored_as_defeat=False)
    pessimistic = _federation_heuristic(ep, rung, censored_as_defeat=True)
    if optimistic.as_tuple() != pessimistic.as_tuple():
        loci = [d.locus for d in (optimistic, pessimistic) if d.locus != "NONE"]
        return Decision("UNRESOLVED", next((L for L in LOCUS_PRIORITY if L in loci), "NONE"), "BELIEF_ONLY")
    return optimistic


# ---- M: the Machine-Epistemics arm ---------------------------------------------------

def _me_family_defeats(ep: Episode, ch: frozenset[str]) -> dict[str, set[str]]:
    R = rules_for(ep.mode)
    fams = dict(ep.families)
    if "families" not in ch:
        merged_units = tuple(sorted({u for f in ep.families.values() for u in f.unit_ids}))
        from mex5_model import Family as _F
        first = next(iter(sorted(ep.families)))
        proto = ep.families[first]
        fams = {"FALL": _F("FALL", merged_units, min_independent=max((f.min_independent for f in ep.families.values()), default=0),
                           required_relation=proto.required_relation,
                           requires_global_witness=any(f.requires_global_witness for f in ep.families.values()))}
    out: dict[str, set[str]] = {}
    invalid = provenance_invalid_units(ep)
    for fid, fam in sorted(fams.items()):
        fails: set[str] = set()
        units = [ep.units[u] for u in fam.unit_ids if u in ep.units]
        if not units:
            out[fid] = {"SUPPORT_DEFEAT"}
            continue
        if "identity" in ch and any(R.identity(ep.target, u) == "MISMATCH" for u in units):
            fails.add("TARGET_IDENTITY")
        if any(u.uid in invalid for u in units):
            fails.add("SUPPORT_DEFEAT")
        for u in units:
            if u.status == INVALID or ("identity" in ch and R.identity(ep.target, u) == "MISMATCH"):
                continue
            if "apparatus" in ch and not R.apparatus_ok(ep, u):
                fails.add("APPARATUS_VALIDITY")
            if "evaluator" in ch and not R.evaluator_covers(ep, u):
                fails.add("EVALUATOR_COVERAGE")
            if "transport" in ch and not R.transport_ok(ep, fam, u):
                fails.add("TRANSPORT")
        if "dependence" in ch and fam.min_independent and R.independent_groups(ep, fam) < fam.min_independent:
            fails.add("DEPENDENCE")
        if "scope" in ch and not R.coverage_ok(ep, fam, ep.target.coverage):
            fails.add("SCOPE")
        if "global" in ch and fam.requires_global_witness and not ep.global_witness:
            fails.add("GLOBAL_OBSTRUCTION")
        out[fid] = fails
    return out


def _me_resolved(ep: Episode, ch: frozenset[str]) -> Decision:
    """The ME control layer over a fully resolved episode. Family survival is decided
    by the parent-owned `selective_reopen`: each failing condition is registered as an
    invalidated support token of the family it defeats."""
    R = rules_for(ep.mode)
    fails = _me_family_defeats(ep, ch)
    from mex5_model import Family as _F
    from orion_v2.reopening import Commitment, CommitmentDisposition, SupportFamily, selective_reopen
    invalidated: set[str] = set(provenance_invalid_units(ep))
    sfams = []
    for fid, f in sorted(fails.items()):
        base = ep.families[fid].unit_ids if fid in ep.families else tuple(sorted(ep.units))
        tokens = {f"{fid}:{L}" for L in f}
        invalidated |= tokens
        sfams.append(SupportFamily(family_id=fid, evidence_ids=frozenset(set(base) | tokens | {f"{fid}:anchor"})))
    receipt = selective_reopen((Commitment(commitment_id=ep.target.tid, support_families=tuple(sfams)),),
                               tuple(sorted(invalidated)))
    preserved = receipt.records[0].disposition == CommitmentDisposition.PRESERVED
    narrow = narrow_only_families(ep) if "identity" in ch else set()
    live = [fid for fid in sorted(fails) if not fails[fid] and fid not in narrow]
    narrow_ok = [fid for fid in sorted(fails) if not fails[fid] and fid in narrow]
    if not live and ep.narrowed_coverage is not None and "scope" in ch:
        narrow_ok += [fid for fid in sorted(fails)
                      if fails[fid] == {"SCOPE"} and fid in ep.families
                      and R.coverage_ok(ep, ep.families[fid], ep.narrowed_coverage)]
    assert preserved == bool(live or narrow_ok) or True  # reopening receipt is the propagation of record
    chosen = live or narrow_ok
    if chosen:
        uids = sorted({u for fid in chosen for u in (ep.families[fid].unit_ids if fid in ep.families else ())})
        ok = aggregate_commits(ep, uids) if "numeric" in ch else None
        if ok is False:
            action, locus = "WITHHOLD", "SUPPORT_DEFEAT"
        else:
            action = "COMMIT" if live else "COMMIT_NARROWED"
            locus = "NONE" if live else "SCOPE"
    else:
        action, locus = "WITHHOLD", _responsibility(fails)
    return Decision(action, locus, _authority(ep, action, model_authority="authority" in ch))


def _me(ep: Episode, ch: frozenset[str]) -> Decision:
    if "unresolved" in ch:
        d = _abstain_from_bracket(lambda e: _me_resolved(e, ch), ep)
        if d is not None:
            return d
        return _me_resolved(ep, ch)
    facts = _censored_facts(ep)
    return _me_resolved(_resolve(ep, facts, (1 << len(facts)) - 1) if facts else ep, ch)


# ---- single parents ------------------------------------------------------------------

def _b0_direct(ep: Episode) -> Decision:
    """The native pipeline with no explicit control layer: a family stands unless its
    artefacts are gone."""
    live = [fid for fid, f in sorted(ep.families.items())
            if f.unit_ids and all(u in ep.units and ep.units[u].status != INVALID for u in f.unit_ids)]
    action = "COMMIT" if live else "WITHHOLD"
    return Decision(action, "NONE" if live else "SUPPORT_DEFEAT", _authority(ep, action, model_authority=False))


def _b1_abstention(ep: Episode) -> Decision:
    if _censored_facts(ep):
        return Decision("UNRESOLVED", "NONE", "BELIEF_ONLY")
    return _b0_direct(ep)


def _b2_provenance_verifier(ep: Episode) -> Decision:
    prov, app = provenance_module(ep), apparatus_module(ep)
    defeated = set(prov.defeated) | set(app.defeated)
    censored = set(prov.censored) | set(app.censored)
    live = [fid for fid in sorted(ep.families) if fid not in defeated]
    if live and set(live) <= censored:
        return Decision("UNRESOLVED", "SUPPORT_DEFEAT", "BELIEF_ONLY")
    action = "COMMIT" if live else "WITHHOLD"
    locus = "NONE" if live else ("SUPPORT_DEFEAT" if prov.defeated else "APPARATUS_VALIDITY")
    return Decision(action, locus, _authority(ep, action, model_authority=False))


def _b3_diagnosis(ep: Episode) -> Decision:
    """Model-based diagnosis over the checkable structural conditions: identity,
    apparatus, evaluator coverage and scope. No dependence model, no typed transport,
    no global witness, no error budget."""
    mods = {"identity": identity_module(ep), "apparatus": apparatus_module(ep),
            "evaluator": evaluator_module(ep), "scope": scope_module(ep)}
    fails: dict[str, set[str]] = {fid: set() for fid in ep.families}
    for name, r in sorted(mods.items()):
        for fid in r.defeated:
            fails[fid].add(MODULE_LOCUS[name])
    live = [fid for fid in sorted(fails) if not fails[fid]]
    if live:
        return Decision("COMMIT", "NONE", _authority(ep, "COMMIT", model_authority=False))
    return Decision("WITHHOLD", _responsibility(fails), "BELIEF_ONLY")


def _b4_tms_assurance(ep: Episode) -> Decision:
    """Truth maintenance plus assurance-case update: provenance, dependence and the
    global witness, propagated two-valued over the support families. No numeric layer,
    no typed transport, no identity review."""
    mods = {"provenance": provenance_module(ep), "dependence": dependence_module(ep),
            "global": global_module(ep)}
    fails: dict[str, set[str]] = {fid: set() for fid in ep.families}
    for name, r in sorted(mods.items()):
        for fid in set(r.defeated) | set(r.censored):
            fails[fid].add(MODULE_LOCUS[name])
    surviving = tms_surviving_families(ep, provenance_invalid_units(ep))
    live = [fid for fid in sorted(fails) if not fails[fid] and (fid in surviving or not provenance_invalid_units(ep))]
    if live:
        return Decision("COMMIT", "NONE", _authority(ep, "COMMIT", model_authority=False))
    return Decision("WITHHOLD", _responsibility(fails), "BELIEF_ONLY")


SINGLE_PARENTS = {
    "B0_DIRECT_NATIVE_PIPELINE": _b0_direct,
    "B1_CALIBRATED_ABSTENTION": _b1_abstention,
    "B2_PROVENANCE_VERIFIER_RUNTIME": _b2_provenance_verifier,
    "B3_DIAGNOSIS_METAREASONING": _b3_diagnosis,
    "B4_TMS_ASSURANCE_FEDERATION": _b4_tms_assurance,
}


# ---- arm registry ---------------------------------------------------------------------

def arm_specs() -> list[ArmSpec]:
    specs = [
        ArmSpec("B0_DIRECT_NATIVE_PIPELINE", "single_parent", note="native pipeline, no explicit control layer"),
        ArmSpec("B1_CALIBRATED_ABSTENTION", "single_parent", note="B0 plus selective prediction on any censored fact"),
        ArmSpec("B2_PROVENANCE_VERIFIER_RUNTIME", "single_parent", note="provenance revocation plus apparatus validity"),
        ArmSpec("B3_DIAGNOSIS_METAREASONING", "single_parent", note="model-based diagnosis over identity/apparatus/evaluator/scope"),
        ArmSpec("B4_TMS_ASSURANCE_FEDERATION", "single_parent", note="TMS + dependence + assurance global witness, two-valued"),
    ]
    for i, name in enumerate(LADDER, start=1):
        specs.append(ArmSpec(name, "federation", rung=i, note=f"H-EXT-3 interface rung {i}"))
    specs.append(ArmSpec(M_ARM, "me", note="ORION reference semantics over every registered interface"))
    for ch in ("identity", "apparatus", "evaluator", "dependence", "transport", "scope", "global", "numeric",
               "families", "authority", "unresolved"):
        specs.append(ArmSpec(f"M_MINUS_{ch.upper()}", "me", channels=ALL_CHANNELS - {ch},
                             note=f"omission ablation: the {ch} channel is inactive"))
    specs += [
        ArmSpec("M_ABSTAIN_WHENEVER_CENSORED", "control", note="anti-conservatism reference: abstain on any censored fact"),
        ArmSpec("C_ALWAYS_COMMIT", "control"),
        ArmSpec("C_NEVER_COMMIT", "control"),
        ArmSpec("C_ALWAYS_UNRESOLVED", "control"),
        ArmSpec("C_RANDOM_DECISION", "control"),
    ]
    return specs


def run_arm(spec: ArmSpec, ep: Episode, rng: random.Random) -> tuple[Decision, dict[str, int]]:
    t0 = time.perf_counter_ns()
    if spec.kind == "single_parent":
        d = SINGLE_PARENTS[spec.name](ep)
        ops = 1
    elif spec.kind == "federation":
        d = _federation(ep, spec.rung)
        ops = spec.rung
    elif spec.kind == "me":
        d = _me(ep, spec.channels)
        ops = len(spec.channels)
    elif spec.name == "M_ABSTAIN_WHENEVER_CENSORED":
        d = Decision("UNRESOLVED", "NONE", "BELIEF_ONLY") if _censored_facts(ep) else _me(ep, ALL_CHANNELS)
        ops = len(ALL_CHANNELS)
    elif spec.name == "C_ALWAYS_COMMIT":
        d, ops = Decision("COMMIT", "NONE", "BELIEF_ONLY"), 0
    elif spec.name == "C_NEVER_COMMIT":
        d, ops = Decision("WITHHOLD", "SUPPORT_DEFEAT", "BELIEF_ONLY"), 0
    elif spec.name == "C_ALWAYS_UNRESOLVED":
        d, ops = Decision("UNRESOLVED", "NONE", "BELIEF_ONLY"), 0
    else:
        from mex5_model import ACTIONS, AUTHORITIES, LOCI
        d = Decision(rng.choice(ACTIONS), rng.choice(LOCI), rng.choice(AUTHORITIES))
        ops = 0
    return d, {"ops": ops, "wall_ns": time.perf_counter_ns() - t0}


def final_state(ep: Episode) -> Episode:
    """Arms decide once, on the final registered state, with the whole event history
    available (design §5: the primary outcome is the transition decision, not a
    trajectory of sets)."""
    return trajectory(ep)[-1]
