#!/usr/bin/env python3
"""ME-X5 exact oracle.

The *shell* below is mode-neutral: it encodes the hypothesised common decision
object (which family survives; which registered element is responsible; what
authority the evidence licenses). The *rules* it calls are native and disagree
across modes (see the three `mex5_native_*` modules).

Registered honesty note (design §10): the common object is a **design input**,
not a finding of this study. ME-X5 tests whether the strongest faithful parent
federation needs it, and — through the changed-vocabulary gate — whether the
object is recoverable from native surface features without ORION vocabulary. It
cannot and does not establish that the object was discovered independently in
three fields.

The oracle's definition is **exhaustive enumeration** over the censored facts.
A three-valued envelope is *not* sound here: in the two numeric modes a censored
study or channel can move a pooled estimate in either direction, so the decision
is not monotone in the censored facts. G0b therefore cross-checks the
enumeration against (i) the all-optimistic / all-pessimistic bracket wherever the
bracket is conclusive and (ii) a full relabelling permutation of every element
identifier.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Callable

import mex5_native_formal as NF
import mex5_native_measurement as NM
import mex5_native_synthesis as NS
from mex5_model import (
    CENSORED,
    INVALID,
    LOCUS_PRIORITY,
    VALID,
    Decision,
    Episode,
    trajectory,
)

RULES: dict[str, Any] = {"FORMAL": NF, "MEASUREMENT": NM, "SYNTHESIS": NS}
MAX_CENSORED_FACTS = 6


def rules_for(mode: str):
    return RULES[mode]


# ---- family evaluation on a fully resolved episode -------------------------------

def family_failures(ep: Episode, fid: str) -> tuple[set[str], bool]:
    """Return (failing loci, narrow_only). A family is a conjunction: every
    registered member must be usable."""
    R = rules_for(ep.mode)
    fam = ep.families[fid]
    fails: set[str] = set()
    units = [ep.units[u] for u in fam.unit_ids if u in ep.units]
    if not units:
        return ({"SUPPORT_DEFEAT"}, False)
    ids = [R.identity(ep.target, u) for u in units]
    if any(i == "MISMATCH" for i in ids):
        fails.add("TARGET_IDENTITY")
    if any(u.status == INVALID for u in units):
        fails.add("SUPPORT_DEFEAT")
    for u, ident in zip(units, ids):
        if u.status == INVALID or ident == "MISMATCH":
            continue
        if not R.apparatus_ok(ep, u):
            fails.add("APPARATUS_VALIDITY")
        if not R.evaluator_covers(ep, u):
            fails.add("EVALUATOR_COVERAGE")
        if not R.transport_ok(ep, fam, u):
            fails.add("TRANSPORT")
    if fam.min_independent and R.independent_groups(ep, fam) < fam.min_independent:
        fails.add("DEPENDENCE")
    if not R.coverage_ok(ep, fam, ep.target.coverage):
        fails.add("SCOPE")
    if fam.requires_global_witness and not ep.global_witness:
        fails.add("GLOBAL_OBSTRUCTION")
    narrow_only = bool(ids) and "MISMATCH" not in ids and "EXACT" not in ids and "NARROWED" in ids
    return (fails, narrow_only)


def _agg_commits(ep: Episode, uids: list[str]) -> bool:
    R = rules_for(ep.mode)
    agg = R.aggregate(ep, uids)
    if agg is None:
        return True
    return bool(R.commits(ep, agg))


def decide_resolved(ep: Episode) -> Decision:
    """The frozen decision shell, applied to an episode with no censored facts."""
    ff = {fid: family_failures(ep, fid) for fid in sorted(ep.families)}
    live = [fid for fid, (f, nar) in ff.items() if not f and not nar]
    narrow = [fid for fid, (f, nar) in ff.items() if (not f and nar)]
    if not live and ep.narrowed_coverage is not None:
        R = rules_for(ep.mode)
        narrow += [fid for fid, (f, nar) in ff.items()
                   if f == {"SCOPE"} and R.coverage_ok(ep, ep.families[fid], ep.narrowed_coverage)]
    if live:
        uids = sorted({u for fid in live for u in ep.families[fid].unit_ids})
        action, locus = ("COMMIT", "NONE") if _agg_commits(ep, uids) else ("WITHHOLD", "SUPPORT_DEFEAT")
    elif narrow:
        uids = sorted({u for fid in narrow for u in ep.families[fid].unit_ids})
        action, locus = ("COMMIT_NARROWED", "SCOPE") if _agg_commits(ep, uids) else ("WITHHOLD", "SUPPORT_DEFEAT")
    else:
        # Frozen responsibility rule, chosen to be invariant under relabelling:
        # among the families closest to repair (fewest failing loci) take each
        # family's highest-priority failing locus, then report the most
        # downstream of those - the nearest repair that would restore support.
        fewest = min(len(f) for f, _ in ff.values())
        heads = {next((L for L in LOCUS_PRIORITY if L in f), "SUPPORT_DEFEAT")
                 for f, _ in ff.values() if len(f) == fewest}
        locus = max(heads, key=LOCUS_PRIORITY.index)
        action = "WITHHOLD"
    if action in ("COMMIT", "COMMIT_NARROWED") and ep.target.requested_authority == "ACTION" and ep.authority_granted:
        authority = "BELIEF_AND_ACTION"
    else:
        authority = "BELIEF_ONLY"
    return Decision(action, locus, authority)


# ---- censoring and exhaustive enumeration ----------------------------------------

FACT_LOCUS = {
    "UNIT": "SUPPORT_DEFEAT",
    "VALIDATOR": "APPARATUS_VALIDITY",
    "COVERAGE": "EVALUATOR_COVERAGE",
    "ANCESTRY": "DEPENDENCE",
    "RELATION": "TRANSPORT",
}


def censored_facts(ep: Episode) -> list[tuple]:
    """Registered facts whose value is currently unreadable. Only facts that can
    touch the decision are listed (a censored element not used by any family is
    not a censored fact of this decision)."""
    used_units = {u for f in ep.families.values() for u in f.unit_ids} & set(ep.units)
    used_validators = {ep.units[u].validator for u in used_units} - {None}
    used_contexts = {ep.units[u].context for u in used_units}
    facts: list[tuple] = []
    for uid in sorted(used_units):
        u = ep.units[uid]
        if u.status == CENSORED:
            facts.append(("UNIT", uid))
        for anc, kind in sorted(u.ancestry):
            if kind == "SUSPECTED":
                facts.append(("ANCESTRY", uid, anc))
    for vid in sorted(used_validators):
        v = ep.validators[vid]
        if v.status == CENSORED:
            facts.append(("VALIDATOR", vid))
        if ep.target.asserted_failure_class in v.uncertain:
            facts.append(("COVERAGE", vid))
    for key in sorted(ep.relations):
        if ep.relations[key] != "CANNOT_CHECK":
            continue
        src, dst = key.split(">", 1)
        if src in used_contexts and dst == ep.target.context:
            facts.append(("RELATION", key))
    return facts


def resolve(ep: Episode, facts: list[tuple], bits: int) -> Episode:
    """bit 1 = the optimistic reading, bit 0 = the pessimistic reading."""
    units = dict(ep.units)
    validators = dict(ep.validators)
    relations = dict(ep.relations)
    for i, fact in enumerate(facts):
        good = bool((bits >> i) & 1)
        if fact[0] == "UNIT":
            u = units[fact[1]]
            units[u.uid] = replace(u, status=VALID if good else INVALID)
        elif fact[0] == "ANCESTRY":
            u = units[fact[1]]
            anc = tuple(a for a in u.ancestry if not (a[0] == fact[2] and a[1] == "SUSPECTED"))
            if not good:
                anc = tuple(sorted(set(anc) | {(fact[2], "CONFIRMED")}))
            units[u.uid] = replace(u, ancestry=anc)
        elif fact[0] == "VALIDATOR":
            v = validators[fact[1]]
            validators[v.vid] = replace(v, status=VALID if good else INVALID)
        elif fact[0] == "COVERAGE":
            v = validators[fact[1]]
            cls = ep.target.asserted_failure_class
            covers = tuple(sorted(set(v.covers) | {cls})) if good else tuple(x for x in v.covers if x != cls)
            validators[v.vid] = replace(v, covers=covers, uncertain=tuple(x for x in v.uncertain if x != cls))
        elif fact[0] == "RELATION":
            relations[fact[1]] = "ISOMORPHIC" if good else "INCOMPARABLE"
        else:  # pragma: no cover - guarded by censored_facts
            raise ValueError(fact)
    return replace(ep, units=units, validators=validators, relations=relations)


@dataclass(frozen=True)
class OracleVersion:
    decision: Decision
    n_censored: int
    resolutions: int
    bracket_conclusive: bool
    bracket_agrees: bool

    def as_dict(self) -> dict[str, Any]:
        return {"decision": self.decision.as_dict(), "n_censored": self.n_censored,
                "resolutions": self.resolutions, "bracket_conclusive": self.bracket_conclusive,
                "bracket_agrees": self.bracket_agrees}


def oracle_version(ep: Episode) -> OracleVersion:
    facts = censored_facts(ep)
    if len(facts) > MAX_CENSORED_FACTS:
        raise ValueError(f"{len(facts)} censored facts exceeds the frozen cap {MAX_CENSORED_FACTS}")
    if not facts:
        d = decide_resolved(ep)
        return OracleVersion(d, 0, 1, True, True)
    seen: set[tuple[str, str, str]] = set()
    decisions: list[Decision] = []
    for bits in range(1 << len(facts)):
        d = decide_resolved(resolve(ep, facts, bits))
        if d.as_tuple() not in seen:
            seen.add(d.as_tuple())
            decisions.append(d)
    if len(seen) == 1:
        d = decisions[0]
        return OracleVersion(d, len(facts), 1 << len(facts), True, True)
    loci = [d.locus for d in decisions if d.locus != "NONE"]
    loci += [FACT_LOCUS[f[0]] for f in facts]
    locus = next((L for L in LOCUS_PRIORITY if L in loci), "NONE")
    d = Decision("UNRESOLVED", locus, "BELIEF_ONLY")
    # bracket cross-check: all-optimistic vs all-pessimistic
    opt = decide_resolved(resolve(ep, facts, (1 << len(facts)) - 1))
    pes = decide_resolved(resolve(ep, facts, 0))
    conclusive = opt.as_tuple() != pes.as_tuple()
    return OracleVersion(d, len(facts), 1 << len(facts), conclusive, conclusive)


def oracle_trajectory(ep: Episode) -> list[OracleVersion]:
    return [oracle_version(v) for v in trajectory(ep)]


# ---- G0b independent cross-check: relabelling permutation ------------------------

def relabelled(ep: Episode) -> Episode:
    """Deterministic relabelling of every element identifier, with the dictionary
    insertion order reversed. The decision must be invariant."""
    umap = {uid: f"z{len(ep.units) - i}" for i, uid in enumerate(sorted(ep.units))}
    vmap = {vid: f"w{len(ep.validators) - i}" for i, vid in enumerate(sorted(ep.validators))}
    fmap = {fid: f"y{len(ep.families) - i}" for i, fid in enumerate(sorted(ep.families))}
    units = {}
    for uid in reversed(sorted(ep.units)):
        u = ep.units[uid]
        units[umap[uid]] = replace(u, uid=umap[uid], validator=vmap.get(u.validator) if u.validator else None)
    validators = {vmap[v]: replace(ep.validators[v], vid=vmap[v]) for v in reversed(sorted(ep.validators))}
    families = {}
    for fid in reversed(sorted(ep.families)):
        f = ep.families[fid]
        families[fmap[fid]] = replace(f, fid=fmap[fid], unit_ids=tuple(umap[u] for u in reversed(f.unit_ids) if u in umap))
    return replace(ep, units=units, validators=validators, families=families)


def permutation_invariant(ep: Episode) -> bool:
    for state in trajectory(ep):
        a = oracle_version(state).decision
        b = oracle_version(relabelled(state)).decision
        if a.as_tuple() != b.as_tuple():
            return False
    return True


def valid_at_v0(ep: Episode) -> bool:
    """Every episode must be a warranted commitment before its registered events."""
    d = oracle_version(ep).decision
    return d.action == "COMMIT" and d.locus == "NONE"
