#!/usr/bin/env python3
"""Exact/hostile checker for MACHINE_EPISTEMICS_FOUNDATION_V1.

Exit codes: 0=holds, 1=defect, 2=CANNOT_CHECK. Stdlib only.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction
import argparse, hashlib, itertools, json
from pathlib import Path
from typing import Iterable, FrozenSet, Tuple

LIVE, DEAD, UNKNOWN, CONTRADICTED = "LIVE", "DEAD", "UNKNOWN", "CONTRADICTED"
AUTH_NONE = "NONE"
AUTH_PARITY = "OCM_ABSORPTION_ELIGIBLE_AFTER_PARITY"
AUTH_SCOPED = "SCOPED_ONLY_AFTER_PARITY"
ALLOWED_STATUSES = {"PROVED","ADOPTED","PARENT_OWNED","FINITE_CALIBRATION","OPEN","CANNOT_CHECK","PROPOSED_PENDING_PR"}
NO_AUTHORITY_STATUSES = {"OPEN","CANNOT_CHECK","PROPOSED_PENDING_PR"}

class CannotCheck(RuntimeError):
    pass

def canonical_digest(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(raw).hexdigest()

@dataclass(frozen=True)
class BehaviorIdentity:
    implementation_digest: str
    model_digest: str
    configuration_digest: str
    runtime_digest: str
    checker_digest: str
    calibration_digest: str
    assumption_digest: str
    scope_digest: str
    epoch: str
    def validate(self) -> None:
        for k, v in asdict(self).items():
            if not isinstance(v, str) or not v.strip():
                raise CannotCheck(f"unbound behavior-identity field: {k}")
    @property
    def digest(self) -> str:
        self.validate()
        return canonical_digest(asdict(self))

@dataclass(frozen=True)
class CoverageCertificate:
    behavior_digest: str
    guarantee_kind: str
    error_numerator: int
    error_denominator: int
    scope_digest: str
    assumption_digest: str
    epoch: str
    @property
    def error_rate(self) -> Fraction:
        if self.error_denominator <= 0:
            raise CannotCheck("non-positive error denominator")
        a = Fraction(self.error_numerator, self.error_denominator)
        if a < 0 or a > 1:
            raise CannotCheck("error rate outside [0,1]")
        return a

@dataclass(frozen=True)
class ActionPolicy:
    policy_id: str
    max_error_numerator: int
    max_error_denominator: int
    accepted_guarantee_kinds: Tuple[str, ...]
    scope_digest: str
    assumption_digest: str
    epoch: str
    @property
    def max_error(self) -> Fraction:
        if self.max_error_denominator <= 0:
            raise CannotCheck("non-positive policy denominator")
        x = Fraction(self.max_error_numerator, self.max_error_denominator)
        if x < 0 or x > 1:
            raise CannotCheck("policy risk outside [0,1]")
        return x

def statistical_candidate_truth(*, exact_or_observation_certificate: bool) -> str:
    return LIVE if exact_or_observation_certificate else UNKNOWN

def policy_actionability(cert: CoverageCertificate, current_identity: BehaviorIdentity, policy: ActionPolicy) -> str:
    current_identity.validate()
    if cert.behavior_digest != current_identity.digest:
        return "REVALIDATE_IDENTITY_DRIFT"
    if cert.scope_digest != current_identity.scope_digest or policy.scope_digest != cert.scope_digest:
        return "REVALIDATE_SCOPE_DRIFT"
    if cert.assumption_digest != current_identity.assumption_digest or policy.assumption_digest != cert.assumption_digest:
        return "REVALIDATE_ASSUMPTION_DRIFT"
    if cert.epoch != current_identity.epoch or policy.epoch != cert.epoch:
        return "REVALIDATE_EPOCH_DRIFT"
    if cert.guarantee_kind not in policy.accepted_guarantee_kinds:
        return "NOT_AUTHORIZED_GUARANTEE_KIND"
    if cert.error_rate > policy.max_error:
        return "NOT_AUTHORIZED_RISK_BUDGET"
    return "AUTHORIZED_RISK_BOUNDED"

def mutant_coverage_promotes_individual_truth(cert: CoverageCertificate) -> str:
    return LIVE if cert.error_rate <= Fraction(1, 20) else UNKNOWN

Support = FrozenSet[str]
Profile = Tuple[Support, ...]
Interval = Tuple[Profile, Profile]

def antichain(supports: Iterable[Iterable[str]]) -> Profile:
    xs = {frozenset(x) for x in supports}
    mins = []
    for x in sorted(xs, key=lambda s: (len(s), tuple(sorted(s)))):
        if not any(y <= x for y in mins):
            mins.append(x)
    return tuple(mins)

ZERO: Profile = tuple()
ONE: Profile = (frozenset(),)

def plus(p: Profile, q: Profile) -> Profile:
    return antichain(list(p) + list(q))

def times(p: Profile, q: Profile) -> Profile:
    if not p or not q:
        return ZERO
    return antichain([a | b for a in p for b in q])

def filter_nogoods(p: Profile, nogoods: Profile) -> Profile:
    return antichain(w for w in p if not any(n <= w for n in nogoods))

def times_nogood(p: Profile, q: Profile, nogoods: Profile) -> Profile:
    return filter_nogoods(times(filter_nogoods(p, nogoods), filter_nogoods(q, nogoods)), nogoods)

def mutant_prefilter_only_times(p: Profile, q: Profile, nogoods: Profile) -> Profile:
    return times(filter_nogoods(p, nogoods), filter_nogoods(q, nogoods))

def support_alive(p: Profile, revoked: FrozenSet[str]) -> bool:
    return any(not (w & revoked) for w in p)

def interval_status(interval: Interval, revoked: FrozenSet[str], nogoods: Profile) -> str:
    lower, upper = interval
    lf, uf = filter_nogoods(lower, nogoods), filter_nogoods(upper, nogoods)
    if support_alive(lf, revoked):
        return LIVE
    raw_upper_alive, filtered_upper_alive = support_alive(upper, revoked), support_alive(uf, revoked)
    if not filtered_upper_alive and raw_upper_alive:
        return CONTRADICTED
    if not filtered_upper_alive:
        return DEAD
    return UNKNOWN

def interval_times_nogood(a: Interval, b: Interval, nogoods: Profile) -> Interval:
    return (times_nogood(a[0], b[0], nogoods), times_nogood(a[1], b[1], nogoods))

def kleene_and(a: str, b: str) -> str:
    if CONTRADICTED in (a, b):
        raise ValueError("CONTRADICTED is a composition terminal, not a Kleene truth value")
    if DEAD in (a, b):
        return DEAD
    if a == LIVE and b == LIVE:
        return LIVE
    return UNKNOWN

def nogood_separable(a: Interval, b: Interval, nogoods: Profile) -> bool:
    au, bu = filter_nogoods(a[1], nogoods), filter_nogoods(b[1], nogoods)
    return all(not any(n <= (x | y) for n in nogoods) for x in au for y in bu)

def all_antichains(universe=("a", "b", "c")):
    subsets = [frozenset(s) for r in range(len(universe)+1) for s in itertools.combinations(universe, r)]
    out = set()
    for mask in range(1 << len(subsets)):
        out.add(antichain(subsets[i] for i in range(len(subsets)) if (mask >> i) & 1))
    return sorted(out, key=lambda p: (len(p), tuple((len(x), tuple(sorted(x))) for x in p)))

def check_meg02_truth_action_split() -> dict:
    ident = BehaviorIdentity("impl:1","model:1","cfg:1","runtime:1","checker:1","cal:1","assume:exchangeable","scope:a","2026Q3")
    cert = CoverageCertificate(ident.digest,"MARGINAL_COVERAGE",1,20,ident.scope_digest,ident.assumption_digest,ident.epoch)
    policy = ActionPolicy("reversible",1,20,("MARGINAL_COVERAGE",),ident.scope_digest,ident.assumption_digest,ident.epoch)
    assert statistical_candidate_truth(exact_or_observation_certificate=False) == UNKNOWN
    assert mutant_coverage_promotes_individual_truth(cert) == LIVE
    assert policy_actionability(cert, ident, policy) == "AUTHORIZED_RISK_BOUNDED"
    assert statistical_candidate_truth(exact_or_observation_certificate=False) == UNKNOWN
    assert statistical_candidate_truth(exact_or_observation_certificate=True) == LIVE
    strict = ActionPolicy("strict",1,100,("MARGINAL_COVERAGE",),ident.scope_digest,ident.assumption_digest,ident.epoch)
    assert policy_actionability(cert, ident, strict) == "NOT_AUTHORIZED_RISK_BUDGET"
    return {"truth_without_exact_certificate":UNKNOWN,"risk_bounded_action":"AUTHORIZED_RISK_BOUNDED","mutant_score_to_truth_caught":1,"strict_policy_refused":1}

def check_identity_drift() -> dict:
    base = BehaviorIdentity("impl:A","model:A","cfg:A","runtime:A","checker:A","cal:A","assumption:A","scope:A","epoch:A")
    policy = ActionPolicy("p",1,10,("MARGINAL_COVERAGE",),"scope:A","assumption:A","epoch:A")
    cert = CoverageCertificate(base.digest,"MARGINAL_COVERAGE",1,20,"scope:A","assumption:A","epoch:A")
    assert policy_actionability(cert, base, policy) == "AUTHORIZED_RISK_BOUNDED"
    caught = 0
    for field in asdict(base):
        vals = asdict(base); vals[field] += ":DRIFT"
        assert policy_actionability(cert, BehaviorIdentity(**vals), policy).startswith("REVALIDATE_")
        caught += 1
    vals = asdict(base); vals["configuration_digest"] = ""
    try:
        BehaviorIdentity(**vals).digest
    except CannotCheck:
        missing = 1
    else:
        raise AssertionError("unbound identity field silently accepted")
    return {"drift_fields_caught":caught,"unbound_fields_cannot_check":missing}

def check_meg16_nogood_algebra() -> dict:
    profiles = all_antichains()
    nogoods_list = [antichain([{x}]) for x in ("a","b","c")] + [antichain([x]) for x in ({"a","b"},{"a","c"},{"b","c"},{"a","b","c"})]
    pc = tc = ac = 0
    for n in nogoods_list:
        for p in profiles:
            for q in profiles:
                assert filter_nogoods(plus(p,q),n) == filter_nogoods(plus(filter_nogoods(p,n),filter_nogoods(q,n)),n); pc += 1
                assert filter_nogoods(times(p,q),n) == times_nogood(p,q,n); tc += 1
        basis = [ZERO,ONE,antichain([{"a"}]),antichain([{"b"}]),antichain([{"c"}]),antichain([{"a"},{"b"}]),antichain([{"a","b"}])]
        for p in basis:
            for q in basis:
                for r in basis:
                    assert times_nogood(times_nogood(p,q,n),r,n) == times_nogood(p,times_nogood(q,r,n),n); ac += 1
    n, p, q = antichain([{"a","b"}]), antichain([{"a"}]), antichain([{"b"}])
    assert mutant_prefilter_only_times(p,q,n) == antichain([{"a","b"}])
    assert times_nogood(p,q,n) == ZERO
    a, b = (p,p), (q,q)
    assert interval_status(a,frozenset(),n) == LIVE and interval_status(b,frozenset(),n) == LIVE
    assert not nogood_separable(a,b,n)
    terminal = CONTRADICTED
    ib = [(ONE,ONE),(ZERO,ZERO),(ZERO,ONE),(antichain([{"a"}]),antichain([{"a"}])),(ZERO,antichain([{"a"}])),(antichain([{"b"}]),antichain([{"b"}]))]
    cc = 0
    for n in nogoods_list:
        for a in ib:
            for b in ib:
                if not nogood_separable(a,b,n):
                    continue
                for revoked in map(frozenset,[(),("a",),("b",),("c",),("a","b")]):
                    sa, sb = interval_status(a,revoked,n), interval_status(b,revoked,n)
                    if CONTRADICTED in (sa,sb):
                        continue
                    sp = interval_status(interval_times_nogood(a,b,n),revoked,n)
                    assert sp != CONTRADICTED and sp == kleene_and(sa,sb); cc += 1
    return {"profiles_n3":len(profiles),"plus_filter_checks":pc,"product_postfilter_checks":tc,"associativity_checks":ac,"prefilter_only_mutant_caught":1,"live_live_cross_nogood_terminal":terminal,"conditional_kleene_checks":cc,"atlas_unconditional_kleene_statement_refuted":1}

def validate_registry(data: dict) -> dict:
    required = {"foundation_id","version","status","source_main_sha","authority_rule","allowed_statuses","primitives","atlas_obligations","ocm_absorption_contract","non_consequences"}
    if required - set(data): raise CannotCheck(f"registry missing top-level fields: {sorted(required-set(data))}")
    if set(data["allowed_statuses"]) != ALLOWED_STATUSES: raise AssertionError("registry status vocabulary drift")
    if data["status"] not in {"FROZEN_CANDIDATE","FROZEN"}: raise AssertionError("invalid foundation status")
    def rows(xs, kind):
        ids=[r.get("id") for r in xs]
        if len(ids)!=len(set(ids)): raise AssertionError(f"duplicate {kind} id")
        for r in xs:
            for k in ("id","status","terminal","authority_effect","source","reopen_conditions"):
                if k not in r: raise CannotCheck(f"{kind} {r.get('id')} missing {k}")
            s=r["status"]
            if s not in ALLOWED_STATUSES: raise AssertionError(f"unknown status {s}")
            if s in NO_AUTHORITY_STATUSES and r["authority_effect"] != AUTH_NONE: raise AssertionError(f"{r['id']} mints authority from {s}")
            if s in {"PROVED","ADOPTED","PARENT_OWNED"}:
                if r["authority_effect"] != AUTH_PARITY: raise AssertionError(f"{r['id']} settled row lacks parity gate")
                if not r["source"].get("commit"): raise CannotCheck(f"{r['id']} settled row missing source commit")
                if not (r["source"].get("artifact") or r["source"].get("issue")): raise CannotCheck(f"{r['id']} settled row missing source artifact/issue")
            if s == "FINITE_CALIBRATION" and r["authority_effect"] not in {AUTH_NONE,AUTH_SCOPED}: raise AssertionError(f"{r['id']} finite calibration has unscoped authority")
            if s == "PROPOSED_PENDING_PR":
                if not r["source"].get("pr"): raise CannotCheck(f"{r['id']} pending row missing PR")
                if r["source"].get("merged",False): raise AssertionError(f"{r['id']} pending row falsely marked merged")
    rows(data["primitives"],"primitive"); rows(data["atlas_obligations"],"atlas")
    expected={f"MEG-{i:02d}" for i in range(1,37)}; actual={r["id"] for r in data["atlas_obligations"]}
    if actual != expected: raise AssertionError(f"atlas coverage mismatch: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
    pending=[r for r in data["atlas_obligations"] if r["source"].get("pr") == 317]
    if not pending or any(r["status"] != "PROPOSED_PENDING_PR" for r in pending): raise AssertionError("PR #317 authority laundering or missing pending rows")
    c=data["ocm_absorption_contract"]; binds=set(c.get("required_bindings",[])); need={"v2_issue_or_study","theorem_or_rule","terminal","source_commit","parity_test"}
    if not need <= binds: raise AssertionError("OCM absorption contract missing required bindings")
    if not NO_AUTHORITY_STATUSES <= set(c.get("blocked_statuses",[])): raise AssertionError("OCM absorption contract does not block all non-authority statuses")
    return {"primitives":len(data["primitives"]),"atlas_obligations":len(data["atlas_obligations"]),"pending_pr317_rows":len(pending),"absorption_bindings":len(binds)}

def check_registry_mutants(data: dict) -> dict:
    caught=0
    d=json.loads(json.dumps(data)); d["primitives"].append(dict(d["primitives"][0]))
    try: validate_registry(d)
    except AssertionError: caught+=1
    else: raise AssertionError("duplicate-id mutant survived")
    d=json.loads(json.dumps(data)); next(r for r in d["atlas_obligations"] if r["status"]=="OPEN")["authority_effect"]=AUTH_PARITY
    try: validate_registry(d)
    except AssertionError: caught+=1
    else: raise AssertionError("OPEN-authority mutant survived")
    d=json.loads(json.dumps(data)); next(r for r in d["atlas_obligations"] if r["status"]=="PROPOSED_PENDING_PR")["source"]["merged"]=True
    try: validate_registry(d)
    except AssertionError: caught+=1
    else: raise AssertionError("pending-as-merged mutant survived")
    d=json.loads(json.dumps(data)); next(r for r in d["atlas_obligations"] if r["status"]=="PROVED")["source"]["commit"]=""
    try: validate_registry(d)
    except CannotCheck: caught+=1
    else: raise AssertionError("missing-source-commit mutant survived")
    d=json.loads(json.dumps(data)); d["ocm_absorption_contract"]["blocked_statuses"]=["OPEN"]
    try: validate_registry(d)
    except AssertionError: caught+=1
    else: raise AssertionError("absorption-blocklist mutant survived")
    return {"registry_mutants_caught":caught}

def run_all(registry_path: Path|None=None) -> dict:
    out={"meg02":check_meg02_truth_action_split(),"identity_drift":check_identity_drift(),"meg16":check_meg16_nogood_algebra()}
    if registry_path is not None:
        try: data=json.loads(registry_path.read_text())
        except (OSError,json.JSONDecodeError) as exc: raise CannotCheck(f"cannot read registry: {exc}") from exc
        out["registry"]=validate_registry(data); out["registry_mutants"]=check_registry_mutants(data)
    return out

def main(argv=None) -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--registry",type=Path); ns=ap.parse_args(argv)
    try:
        print(json.dumps(run_all(ns.registry),sort_keys=True,indent=2)); return 0
    except CannotCheck as exc:
        print(json.dumps({"status":"CANNOT_CHECK","reason":str(exc)},sort_keys=True)); return 2
    except Exception as exc:
        print(json.dumps({"status":"FAIL","reason":f"{type(exc).__name__}: {exc}"},sort_keys=True)); return 1

if __name__ == "__main__":
    raise SystemExit(main())
