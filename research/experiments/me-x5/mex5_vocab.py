#!/usr/bin/env python3
"""ME-X5 changed-vocabulary reviewer (protocol §8).

Protocol §8 asks whether the common decision structure survives when Machine
Epistemics terminology is hidden. What can be automated here is the *formal*
half of that question, and only the formal half:

  a **mode-blind rule set**, written once in ordinary scientific English and
  containing no ORION vocabulary, is applied to each episode through a
  **per-mode adapter** that reads raw native fields (signatures, statuses,
  ranges, cohort identifiers, relation names) and reports neutral surface
  predicates. The adapters do not call the native rule modules and do not see the
  oracle. If one rule set recovers the responsibility class in all three modes,
  the structure is recoverable from native surface features without ORION
  vocabulary.

**Registered limitation.** This is a formal recoverability surrogate, not the
independent human reviewer protocol §8 asks for. No independent native reviewer
classified these episodes. Because §11's `R2_EMERGING_INTERDISCIPLINARY_RESIDUAL`
requires independent adjudication, R2 is **not grantable by this study** whatever
the numbers say; the strongest reachable terminal is a *candidate* pending
independent adjudication. This is stated in design §7 and §10.

The null is the **scrambled adapter**: read each mode's episodes through another
mode's adapter. A rule set that recovers the class under scrambled adapters is
reading the label scheme, not the science.
"""
from __future__ import annotations

from typing import Any

from mex5_model import LOCUS_PRIORITY, RELATION_RANK, Episode

NEUTRAL_RULES = {
    "TARGET_IDENTITY": "something counted as support does not answer the registered question",
    "APPARATUS_VALIDITY": "the apparatus that validated it was not usable under the conditions it was used in",
    "EVALUATOR_COVERAGE": "the check that was run cannot reveal the problem the claim says is absent",
    "DEPENDENCE": "things counted as separate confirmations share an origin, so there are fewer than required",
    "TRANSPORT": "a result obtained elsewhere is being reused without a sufficient licence",
    "SUPPORT_DEFEAT": "part of the supporting set has been withdrawn, or the combined quantity no longer clears the registered threshold",
    "SCOPE": "the claim as registered is broader than what the supporting set covers",
    "GLOBAL_OBSTRUCTION": "the pieces agree with each other but nothing ties them into a whole",
}


def _components(pairs: list[tuple[str, str]], items: list[str]) -> int:
    parent = {x: x for x in items}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return len({find(x) for x in items}) if items else 0


def _shared_confirmed(ep: Episode, a: str, b: str) -> bool:
    aa = {k for k, v in ep.units[a].ancestry if v == "CONFIRMED"}
    bb = {k for k, v in ep.units[b].ancestry if v == "CONFIRMED"}
    return bool(aa & bb)


# ---- per-mode adapters: raw native fields -> neutral surface predicates -------------

def adapter_formal(ep: Episode, fid: str) -> dict[str, Any]:
    t, fam = ep.target, ep.families[fid]
    uids = [u for u in fam.unit_ids if u in ep.units]
    out = {"items": {}, "group": {}}
    for uid in uids:
        u = ep.units[uid]
        v = ep.validators.get(u.validator) if u.validator else None
        need = 5 if u.kind == "ported_lemma" else RELATION_RANK[fam.required_relation]
        out["items"][uid] = {
            "answers_the_registered_question": tuple(u.signature) == tuple(t.signature),
            "apparatus_usable_here": (v is None) or v.status == "VALID",
            "check_can_reveal_the_asserted_problem": (v is None) or (t.asserted_failure_class in v.covers),
            "reuse_licence_sufficient": u.context == t.context or RELATION_RANK.get(ep.relation(u.context, t.context), 0) >= need,
            "withdrawn": u.status == "INVALID",
        }
    live = [u for u in uids if ep.units[u].status != "INVALID"]
    out["group"] = {
        "distinct_origins": _components([(a, b) for i, a in enumerate(live) for b in live[i + 1:] if _shared_confirmed(ep, a, b)], live),
        "required_distinct_origins": fam.min_independent,
        "covers_the_registered_range": any(set(t.coverage) <= set(ep.units[u].coverage) for u in live),
        "pieces_tied_together": (not fam.requires_global_witness) or ep.global_witness,
        "combined_quantity_clears_threshold": True,
    }
    return out


def _numeric_group(ep: Episode, uids: list[str]) -> bool:
    live = [ep.units[u] for u in uids if ep.units[u].status != "INVALID"]
    if not live:
        return False
    ws, num = [], 0.0
    for u in live:
        var = u.stat_err ** 2 + u.syst_err ** 2
        ws.append(1.0 / var if var > 0 else 1e6)
    tot = sum(ws)
    num = sum(w * u.estimate for w, u in zip(ws, live)) / tot
    sig = (1.0 / tot) ** 0.5
    return num - 2.0 * sig > ep.target.threshold


def adapter_measurement(ep: Episode, fid: str) -> dict[str, Any]:
    t, fam = ep.target, ep.families[fid]
    uids = [u for u in fam.unit_ids if u in ep.units]
    out = {"items": {}, "group": {}}
    for uid in uids:
        u = ep.units[uid]
        v = ep.validators.get(u.validator) if u.validator else None
        in_range = True
        if v is not None:
            if v.range_lo is not None and ep.operating_point < v.range_lo:
                in_range = False
            if v.range_hi is not None and ep.operating_point > v.range_hi:
                in_range = False
        out["items"][uid] = {
            "answers_the_registered_question": bool(u.signature) and u.signature[0] == t.signature[0],
            "apparatus_usable_here": (v is None) or (v.status == "VALID" and in_range),
            "check_can_reveal_the_asserted_problem": (v is None) or (t.asserted_failure_class in v.covers),
            "reuse_licence_sufficient": u.context == t.context or RELATION_RANK.get(ep.relation(u.context, t.context), 0) >= RELATION_RANK[fam.required_relation],
            "withdrawn": u.status == "INVALID",
        }
    live = [u for u in uids if ep.units[u].status != "INVALID"]
    pairs = [(a, b) for i, a in enumerate(live) for b in live[i + 1:]
             if _shared_confirmed(ep, a, b) or (ep.units[a].syst_source is not None and ep.units[a].syst_source == ep.units[b].syst_source)]
    have: set[str] = set()
    for u in live:
        have |= set(ep.units[u].coverage)
    out["group"] = {
        "distinct_origins": _components(pairs, live),
        "required_distinct_origins": fam.min_independent,
        "covers_the_registered_range": set(t.coverage) <= have,
        "pieces_tied_together": (not fam.requires_global_witness) or ep.global_witness,
        "combined_quantity_clears_threshold": _numeric_group(ep, sorted(set(ep.units))),
    }
    return out


def adapter_synthesis(ep: Episode, fid: str) -> dict[str, Any]:
    t, fam = ep.target, ep.families[fid]
    uids = [u for u in fam.unit_ids if u in ep.units]
    out = {"items": {}, "group": {}}
    for uid in uids:
        u = ep.units[uid]
        v = ep.validators.get(u.validator) if u.validator else None
        out["items"][uid] = {
            "answers_the_registered_question": len(u.signature) == 4 and len(t.signature) == 4 and tuple(u.signature[1:]) == tuple(t.signature[1:]),
            "apparatus_usable_here": (v is None) or v.status == "VALID",
            "check_can_reveal_the_asserted_problem": (v is None) or (t.asserted_failure_class in v.covers),
            "reuse_licence_sufficient": u.context == t.context or RELATION_RANK.get(ep.relation(u.context, t.context), 0) >= RELATION_RANK[fam.required_relation],
            "withdrawn": u.status == "INVALID",
        }
    live = [u for u in uids if ep.units[u].status != "INVALID"]
    pairs = [(a, b) for i, a in enumerate(live) for b in live[i + 1:] if _shared_confirmed(ep, a, b)]
    have: set[str] = set()
    for u in live:
        have |= set(ep.units[u].coverage)
    out["group"] = {
        "distinct_origins": _components(pairs, live),
        "required_distinct_origins": fam.min_independent,
        "covers_the_registered_range": set(t.coverage) <= have,
        "pieces_tied_together": (not fam.requires_global_witness) or ep.global_witness,
        "combined_quantity_clears_threshold": _numeric_group(ep, sorted(set(ep.units))),
    }
    return out


ADAPTERS = {"FORMAL": adapter_formal, "MEASUREMENT": adapter_measurement, "SYNTHESIS": adapter_synthesis}
SCRAMBLE = {"FORMAL": "SYNTHESIS", "MEASUREMENT": "FORMAL", "SYNTHESIS": "MEASUREMENT"}


# ---- the mode-blind rule set --------------------------------------------------------

def classify(ep: Episode, adapter=None) -> str:
    """One rule set, no ORION vocabulary, applied through a per-mode adapter.
    Returns the responsibility class, or NONE when nothing is wrong."""
    adapter = adapter or ADAPTERS[ep.mode]
    fails: dict[str, set[str]] = {}
    for fid in sorted(ep.families):
        surf = adapter(ep, fid)
        f: set[str] = set()
        items = surf["items"]
        g = surf["group"]
        if not items:
            f.add("SUPPORT_DEFEAT")
        if any(not it["answers_the_registered_question"] for it in items.values()):
            f.add("TARGET_IDENTITY")
        if any(it["withdrawn"] for it in items.values()):
            f.add("SUPPORT_DEFEAT")
        for it in items.values():
            if it["withdrawn"] or not it["answers_the_registered_question"]:
                continue
            if not it["apparatus_usable_here"]:
                f.add("APPARATUS_VALIDITY")
            if not it["check_can_reveal_the_asserted_problem"]:
                f.add("EVALUATOR_COVERAGE")
            if not it["reuse_licence_sufficient"]:
                f.add("TRANSPORT")
        if g["required_distinct_origins"] and g["distinct_origins"] < g["required_distinct_origins"]:
            f.add("DEPENDENCE")
        if not g["covers_the_registered_range"]:
            f.add("SCOPE")
        if not g["pieces_tied_together"]:
            f.add("GLOBAL_OBSTRUCTION")
        fails[fid] = f
    if any(not f for f in fails.values()):
        surf = adapter(ep, next(fid for fid, f in sorted(fails.items()) if not f))
        return "NONE" if surf["group"]["combined_quantity_clears_threshold"] else "SUPPORT_DEFEAT"
    fewest = min(len(f) for f in fails.values())
    heads = {next((L for L in LOCUS_PRIORITY if L in f), "SUPPORT_DEFEAT") for f in fails.values() if len(f) == fewest}
    return max(heads, key=LOCUS_PRIORITY.index)


def classify_scrambled(ep: Episode) -> str:
    """Null: the same rule set reading the episode through another mode's adapter."""
    try:
        return classify(ep, ADAPTERS[SCRAMBLE[ep.mode]])
    except Exception:  # noqa: BLE001 - a scrambled adapter may not parse the fields at all
        return "CANNOT_PARSE"
