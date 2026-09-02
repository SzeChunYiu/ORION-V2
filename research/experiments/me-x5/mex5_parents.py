#!/usr/bin/env python3
"""ME-X5 faithful parent methods.

Each function below is one mature parent mechanism in its native role. They are
the building blocks of the `B5` federation and of the single-parent arms; the ME
arm uses the same parent-owned ORION reference implementations for provenance,
dependence and family reopening (per the field synthesis: provenance and
reopenability are *parent-owned*, not ME inventions).

`fidelity_selftests()` runs a hand-authored known-answer test for every parent in
its own native terms. A parent that fails its own test may not be used as a
baseline: a strawman baseline would make any residual meaningless.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from orion_v2.contracts import ProblemContract  # noqa: E402
from orion_v2.evidence import DependenceEdge, DependenceKind, EvidenceUnit, assess_evidence_dependence  # noqa: E402
from orion_v2.provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance  # noqa: E402
from orion_v2.reopening import Commitment, CommitmentDisposition, SupportFamily, selective_reopen  # noqa: E402
from orion_v2.structural import RelationType  # noqa: E402

from mex5_model import CENSORED, INVALID, RELATION_RANK, Episode  # noqa: E402
from mex5_oracle import rules_for  # noqa: E402

DEFEATS_ALL, DEFEATS_SOME, CENSORS_SOME, CLEAR = "DEFEATS_ALL", "DEFEATS_SOME", "CENSORS_SOME", "CLEAR"

MODULE_LOCUS = {
    "identity": "TARGET_IDENTITY",
    "apparatus": "APPARATUS_VALIDITY",
    "evaluator": "EVALUATOR_COVERAGE",
    "dependence": "DEPENDENCE",
    "transport": "TRANSPORT",
    "provenance": "SUPPORT_DEFEAT",
    "scope": "SCOPE",
    "global": "GLOBAL_OBSTRUCTION",
    "aggregate": "SUPPORT_DEFEAT",
}


@dataclass(frozen=True)
class ModuleReport:
    module: str
    defeated: frozenset[str]
    censored: frozenset[str]
    n_families: int

    @property
    def verdict(self) -> str:
        if self.defeated and len(self.defeated) == self.n_families:
            return DEFEATS_ALL
        if self.defeated:
            return DEFEATS_SOME
        if self.censored:
            return CENSORS_SOME
        return CLEAR


def _report(module: str, ep: Episode, defeated, censored=()) -> ModuleReport:
    return ModuleReport(module, frozenset(defeated), frozenset(censored), len(ep.families))


# ---- parent 1: provenance revocation (ORION ReticulateProvenance) -------------------

def provenance_module(ep: Episode) -> ModuleReport:
    """Revocation descendants over the registered provenance graph. Parent-owned:
    W3C-PROV-style revocation, implemented by `orion_v2.provenance`."""
    nodes, edges = [], []
    for uid in sorted(ep.units):
        nodes.append(ProvenanceNode(node_id=uid, kind="evidence", epoch=ep.episode_id or "e0"))
    for fid, f in sorted(ep.families.items()):
        nodes.append(ProvenanceNode(node_id=fid, kind="family", epoch=ep.episode_id or "e0"))
        for uid in f.unit_ids:
            if uid in ep.units:
                edges.append(ProvenanceEdge(parent_id=uid, child_id=fid,
                                            relation=InheritanceRelation.DERIVES, component="support"))
    graph = ReticulateProvenance(nodes=tuple(nodes), edges=tuple(edges))
    revoked = tuple(sorted(provenance_invalid_units(ep)))
    tainted: set[str] = set(graph.descendants(revoked)) if revoked else set()
    defeated = {fid for fid in ep.families if fid in tainted}
    censored = {fid for fid, f in ep.families.items()
                if any(uid in ep.units and ep.units[uid].status == CENSORED for uid in f.unit_ids)}
    return _report("provenance", ep, defeated, censored - defeated)


def provenance_invalid_units(ep: Episode) -> set[str]:
    return {uid for uid, u in ep.units.items() if u.status == INVALID}


# ---- parent 2: dependence assessment (ORION assess_evidence_dependence) -------------

def dependence_module(ep: Episode, excluded: set[str] | None = None) -> ModuleReport:
    """Independence witnesses over the registered dependence declarations. The
    native rule for *what makes two supports dependent* is mode-owned; the
    witness machinery is `orion_v2.evidence.assess_evidence_dependence`."""
    R = rules_for(ep.mode)
    excluded = excluded or set()
    defeated, censored = set(), set()
    for fid, fam in sorted(ep.families.items()):
        if not fam.min_independent:
            continue
        uids = [u for u in fam.unit_ids if u in ep.units and u not in excluded]
        units = tuple(EvidenceUnit(evidence_id=u, claim_id=ep.target.tid, source_id=ep.units[u].syst_source or u,
                                   method_id=ep.units[u].kind) for u in uids)
        edges = []
        for i, a in enumerate(uids):
            for b in uids[i + 1:]:
                anc_a = dict(ep.units[a].ancestry)
                anc_b = dict(ep.units[b].ancestry)
                shared_conf = {k for k, v in anc_a.items() if v == "CONFIRMED"} & {k for k, v in anc_b.items() if v == "CONFIRMED"}
                shared_susp = {k for k, v in anc_a.items() if v == "SUSPECTED"} & {k for k, v in anc_b.items() if v == "SUSPECTED"}
                if shared_conf:
                    edges.append(DependenceEdge(a, b, DependenceKind.SHARED_SOURCE, tuple(sorted(shared_conf))))
                elif shared_susp:
                    edges.append(DependenceEdge(a, b, DependenceKind.COMMON_CAUSE, tuple(sorted(shared_susp))))
        assess = assess_evidence_dependence(units, tuple(edges))
        groups = R.independent_groups(ep, fam)
        if groups < fam.min_independent:
            defeated.add(fid)
        elif getattr(assess, "suspected_pairs", ()) or any(k == "SUSPECTED" for u in uids for _, k in ep.units[u].ancestry):
            censored.add(fid)
    return _report("dependence", ep, defeated, censored)


# ---- parent 3: typed transport (ORION RelationType rank) ---------------------------

def transport_module(ep: Episode, excluded: set[str] | None = None) -> ModuleReport:
    R = rules_for(ep.mode)
    excluded = excluded or set()
    defeated, censored = set(), set()
    for fid, fam in sorted(ep.families.items()):
        for uid in fam.unit_ids:
            u = ep.units.get(uid)
            if u is None or uid in excluded:
                continue
            if u.context == ep.target.context:
                continue
            rel = ep.relation(u.context, ep.target.context)
            assert rel in RELATION_RANK
            if rel == "CANNOT_CHECK":
                censored.add(fid)
            elif not R.transport_ok(ep, fam, u):
                defeated.add(fid)
    return _report("transport", ep, defeated, censored - defeated)


# ---- parent 4: evaluator coverage contract ------------------------------------------

def evaluator_module(ep: Episode, excluded: set[str] | None = None) -> ModuleReport:
    R = rules_for(ep.mode)
    excluded = excluded or set()
    cls = ep.target.asserted_failure_class
    defeated, censored = set(), set()
    for fid, fam in sorted(ep.families.items()):
        for uid in fam.unit_ids:
            u = ep.units.get(uid)
            if u is None or uid in excluded or u.validator is None:
                continue
            v = ep.validators[u.validator]
            if cls in v.uncertain:
                censored.add(fid)
            elif not R.evaluator_covers(ep, u):
                defeated.add(fid)
    return _report("evaluator", ep, defeated, censored - defeated)


# ---- parent 5: apparatus validity (calibration / kernel / appraisal) ---------------

def apparatus_module(ep: Episode, excluded: set[str] | None = None) -> ModuleReport:
    R = rules_for(ep.mode)
    excluded = excluded or set()
    defeated, censored = set(), set()
    for fid, fam in sorted(ep.families.items()):
        for uid in fam.unit_ids:
            u = ep.units.get(uid)
            if u is None or uid in excluded or u.validator is None:
                continue
            v = ep.validators[u.validator]
            if v.status == CENSORED:
                censored.add(fid)
            elif not R.apparatus_ok(ep, u):
                defeated.add(fid)
    return _report("apparatus", ep, defeated, censored - defeated)


# ---- parent 6: specification / target identity review -------------------------------

def identity_module(ep: Episode) -> ModuleReport:
    R = rules_for(ep.mode)
    defeated = set()
    for fid, fam in sorted(ep.families.items()):
        for uid in fam.unit_ids:
            u = ep.units.get(uid)
            if u is not None and R.identity(ep.target, u) == "MISMATCH":
                defeated.add(fid)
    return _report("identity", ep, defeated)


def narrow_only_families(ep: Episode) -> set[str]:
    R = rules_for(ep.mode)
    out = set()
    for fid, fam in sorted(ep.families.items()):
        ids = [R.identity(ep.target, ep.units[u]) for u in fam.unit_ids if u in ep.units]
        if ids and "MISMATCH" not in ids and "EXACT" not in ids and "NARROWED" in ids:
            out.add(fid)
    return out


# ---- parent 7: scope bookkeeping (ProblemContract.scope) ----------------------------

def scope_module(ep: Episode, coverage=None) -> ModuleReport:
    R = rules_for(ep.mode)
    contract = ProblemContract(problem_id=ep.target.tid, target=ep.target.tid, decision_class="scientific_transition",
                               scope=tuple(sorted(coverage if coverage is not None else ep.target.coverage)))
    need = contract.scope
    defeated = {fid for fid, fam in sorted(ep.families.items()) if not R.coverage_ok(ep, fam, need)}
    return _report("scope", ep, defeated)


# ---- parent 8: assurance-case / global witness --------------------------------------

def global_module(ep: Episode) -> ModuleReport:
    defeated = {fid for fid, fam in sorted(ep.families.items()) if fam.requires_global_witness and not ep.global_witness}
    return _report("global", ep, defeated)


# ---- parent 9: numeric aggregation (error budget / inverse-variance pooling) --------

def aggregate_commits(ep: Episode, uids) -> bool | None:
    R = rules_for(ep.mode)
    agg = R.aggregate(ep, sorted(uids))
    if agg is None:
        return None
    return bool(R.commits(ep, agg))


# ---- parent 10: TMS family propagation (ORION selective_reopen) ---------------------

def tms_surviving_families(ep: Episode, defeated_units: set[str]) -> set[str]:
    """Truth-maintenance propagation over support families, run through the
    parent-owned `orion_v2.reopening.selective_reopen`."""
    fams = tuple(SupportFamily(family_id=fid, evidence_ids=frozenset(f.unit_ids)) for fid, f in sorted(ep.families.items()))
    commit = Commitment(commitment_id=ep.target.tid, support_families=fams)
    receipt = selective_reopen((commit,), tuple(sorted(defeated_units)))
    rec = receipt.records[0]
    if rec.disposition == CommitmentDisposition.PRESERVED:
        return {f.family_id for f in fams if not (set(f.evidence_ids) & defeated_units)}
    return set()


# ---- native fidelity self-tests -----------------------------------------------------

def fidelity_selftests() -> list[dict]:
    """Every parent must pass a hand-authored test in its own native terms."""
    import mex5_generator as G  # local import: generator depends on the oracle only

    out: list[dict] = []

    def check(parent: str, name: str, ok: bool, detail: str) -> None:
        out.append({"parent": parent, "test": name, "passed": bool(ok), "detail": detail})

    R = rules_for("FORMAL")
    rng = __import__("random").Random(3)
    fcs = R.FAILURE_CLASSES
    V = [G._validator(R, "v0", fcs)]
    u = [G._unit(R, rng, "u0"), G._unit(R, rng, "u1", kind=R.UNIT_KIND_SUPPORT)]
    fams = [__import__("mex5_model").Family("F1", ("u0",)), __import__("mex5_model").Family("F2", ("u1",))]
    ep = G._episode("FORMAL", "FID", "fid", G._target(R, rng), u, fams, V)

    # PROVENANCE: revoking u0 must taint F1 and only F1.
    ep_rev = __import__("dataclasses").replace(
        ep, units={**ep.units, "u0": __import__("dataclasses").replace(ep.units["u0"], status=INVALID)})
    r = provenance_module(ep_rev)
    check("PROVENANCE_REVOCATION", "revocation descendants reach exactly the derived family",
          r.defeated == {"F1"} and r.verdict == DEFEATS_SOME, f"defeated={sorted(r.defeated)}")

    # TMS: with F1's evidence invalidated the commitment survives on F2.
    surv = tms_surviving_families(ep_rev, {"u0"})
    check("TMS_SELECTIVE_REOPENING", "an alternative support family preserves the commitment",
          surv == {"F2"}, f"surviving={sorted(surv)}")
    check("TMS_SELECTIVE_REOPENING", "losing every family reopens the commitment",
          tms_surviving_families(ep_rev, {"u0", "u1"}) == set(), "")

    # DEPENDENCE: k=2 over two units sharing a confirmed ancestor is defeated;
    # the same edge with k=1 is not.
    M = __import__("mex5_model")
    dep_units = [G._unit(R, rng, "a0", ancestry=(("anc", "CONFIRMED"),)), G._unit(R, rng, "a1", ancestry=(("anc", "CONFIRMED"),))]
    ep_k2 = G._episode("FORMAL", "FID", "fid", G._target(R, rng), dep_units, [M.Family("F1", ("a0", "a1"), min_independent=2)], V)
    ep_k1 = G._episode("FORMAL", "FID", "fid", G._target(R, rng), dep_units, [M.Family("F1", ("a0", "a1"), min_independent=1)], V)
    check("DEPENDENCE_ASSESSMENT", "shared confirmed ancestry defeats a k=2 family",
          dependence_module(ep_k2).defeated == {"F1"}, "")
    check("DEPENDENCE_ASSESSMENT", "the same ancestry leaves a k=1 family standing",
          dependence_module(ep_k1).defeated == set(), "")
    susp = [G._unit(R, rng, "a0", ancestry=(("anc", "SUSPECTED"),)), G._unit(R, rng, "a1", ancestry=(("anc", "SUSPECTED"),))]
    ep_s = G._episode("FORMAL", "FID", "fid", G._target(R, rng), susp, [M.Family("F1", ("a0", "a1"), min_independent=2)], V)
    check("DEPENDENCE_ASSESSMENT", "suspected ancestry censors rather than defeats",
          dependence_module(ep_s).verdict == CENSORS_SOME, "")

    # TYPED TRANSPORT: rank ordering, the ported-lemma escalation and censoring.
    tu = [G._unit(R, rng, "t0", kind=R.UNIT_KIND_TRANSPORTED, ctx="ctx1")]
    fam1 = [M.Family("F1", ("t0",), required_relation="PREDICTIVELY_EQUIVALENT")]
    ep_t = G._episode("FORMAL", "FID", "fid", G._target(R, rng), tu, fam1, V, relations={"ctx1>ctx0": "BEHAVIORALLY_EQUIVALENT"})
    check("TYPED_TRANSPORT", "a ported lemma needs an isomorphism, not a mere embedding",
          transport_module(ep_t).defeated == {"F1"}, "")
    ep_t2 = G._episode("FORMAL", "FID", "fid", G._target(R, rng), tu, fam1, V, relations={"ctx1>ctx0": "ISOMORPHIC"})
    check("TYPED_TRANSPORT", "an isomorphism licenses the reuse", transport_module(ep_t2).defeated == set(), "")
    ep_t3 = G._episode("FORMAL", "FID", "fid", G._target(R, rng), tu, fam1, V, relations={"ctx1>ctx0": "CANNOT_CHECK"})
    check("TYPED_TRANSPORT", "an unchecked morphism censors", transport_module(ep_t3).verdict == CENSORS_SOME, "")
    check("TYPED_TRANSPORT", "ranks follow the parent-owned RelationType order",
          RELATION_RANK["ISOMORPHIC"] > RELATION_RANK["PREDICTIVELY_EQUIVALENT"] > RELATION_RANK["APPROXIMATELY_EQUIVALENT"]
          and RelationType.ISOMORPHIC.name == "ISOMORPHIC", "")

    # EVALUATOR COVERAGE
    Vb = [G._validator(R, "v0", [c for c in fcs if c != fcs[0]])]
    ep_e = G._episode("FORMAL", "FID", "fid", G._target(R, rng, failure_class=fcs[0]), u, fams, Vb)
    check("EVALUATOR_COVERAGE_CONTRACT", "a checker blind to the asserted class defeats every family that uses it",
          evaluator_module(ep_e).verdict == DEFEATS_ALL, "")
    Vu = [G._validator(R, "v0", [c for c in fcs if c != fcs[0]], uncertain=[fcs[0]])]
    ep_u = G._episode("FORMAL", "FID", "fid", G._target(R, rng, failure_class=fcs[0]), u, fams, Vu)
    check("EVALUATOR_COVERAGE_CONTRACT", "uncertain coverage censors rather than defeats",
          evaluator_module(ep_u).verdict == CENSORS_SOME, "")

    # APPARATUS: the measurement mode's range rule.
    RM = rules_for("MEASUREMENT")
    Vm = [G._validator(RM, "v0", RM.FAILURE_CLASSES, lo=-1.0, hi=1.0)]
    um = [G._unit(RM, rng, "m0")]
    fm = [M.Family("F1", ("m0",))]
    inside = G._episode("MEASUREMENT", "FID", "fid", G._target(RM, rng), um, fm, Vm, operating_point=0.0)
    outside = G._episode("MEASUREMENT", "FID", "fid", G._target(RM, rng), um, fm, Vm, operating_point=9.0)
    check("APPARATUS_VALIDITY", "a calibration is valid inside its range", apparatus_module(inside).defeated == set(), "")
    check("APPARATUS_VALIDITY", "and invalid outside it, with nothing else changed",
          apparatus_module(outside).defeated == {"F1"}, "")

    # AGGREGATION: correlated systematics must not be combined in quadrature.
    corr = [G._unit(RM, rng, "c0", est=2.0, stat=0.0, syst=1.0, syst_source="s"),
            G._unit(RM, rng, "c1", est=2.0, stat=0.0, syst=1.0, syst_source="s")]
    uncorr = [G._unit(RM, rng, "c0", est=2.0, stat=0.0, syst=1.0, syst_source="sa"),
              G._unit(RM, rng, "c1", est=2.0, stat=0.0, syst=1.0, syst_source="sb")]
    ep_c = G._episode("MEASUREMENT", "FID", "fid", G._target(RM, rng), corr, [M.Family("F1", ("c0", "c1"))], Vm)
    ep_n = G._episode("MEASUREMENT", "FID", "fid", G._target(RM, rng), uncorr, [M.Family("F1", ("c0", "c1"))], Vm)
    sc = RM.aggregate(ep_c, ["c0", "c1"])[1]
    sn = RM.aggregate(ep_n, ["c0", "c1"])[1]
    check("UNCERTAINTY_AGGREGATION", "a fully correlated systematic does not shrink with more channels",
          abs(sc - 1.0) < 1e-9, f"sigma_correlated={sc:.4f}")
    check("UNCERTAINTY_AGGREGATION", "independent systematics do shrink", sn < sc - 0.2, f"sigma_uncorrelated={sn:.4f}")

    # SYNTHESIS pooling: overlapping cohorts are deduplicated, not double-counted.
    RS = rules_for("SYNTHESIS")
    Vs = [G._validator(RS, "v0", RS.FAILURE_CLASSES)]
    dup = [G._unit(RS, rng, "s0", est=2.0, stat=0.2, weight=1000, ancestry=(("coh", "CONFIRMED"),)),
           G._unit(RS, rng, "s1", est=2.0, stat=0.2, weight=500, ancestry=(("coh", "CONFIRMED"),))]
    ind = [G._unit(RS, rng, "s0", est=2.0, stat=0.2, weight=1000),
           G._unit(RS, rng, "s1", est=2.0, stat=0.2, weight=500)]
    ep_d = G._episode("SYNTHESIS", "FID", "fid", G._target(RS, rng), dup, [M.Family("F1", ("s0", "s1"))], Vs)
    ep_i = G._episode("SYNTHESIS", "FID", "fid", G._target(RS, rng), ind, [M.Family("F1", ("s0", "s1"))], Vs)
    sd = RS.aggregate(ep_d, ["s0", "s1"])[1]
    si = RS.aggregate(ep_i, ["s0", "s1"])[1]
    check("EVIDENCE_SYNTHESIS_POOLING", "two reports of one cohort give the precision of one study",
          abs(sd - 0.2) < 1e-9, f"sigma_dup={sd:.4f}")
    check("EVIDENCE_SYNTHESIS_POOLING", "two genuine cohorts give more precision", si < sd - 0.02, f"sigma_ind={si:.4f}")

    # SCOPE and GLOBAL WITNESS
    ep_sc = G._episode("FORMAL", "FID", "fid", G._target(R, rng, coverage=("h1", "h9")), u, fams, V)
    check("SCOPE_BOOKKEEPING", "a registered scope no artefact covers defeats every family",
          scope_module(ep_sc).verdict == DEFEATS_ALL, "")
    ep_g = G._episode("FORMAL", "FID", "fid", G._target(R, rng), u, [M.Family("F1", ("u0",), requires_global_witness=True)], V,
                      global_witness=False)
    check("ASSURANCE_GLOBAL_WITNESS", "pairwise agreement without the gluing witness is an obstruction",
          global_module(ep_g).defeated == {"F1"}, "")
    return out
