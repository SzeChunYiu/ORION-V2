"""Exact finite checker for KSO_LIFETIME_PREREQUISITE_THEOREMS_BATCH6_V1.md (stdlib only, exact).

One check function per item (F1–F8).  Every check performs (a) the positive statement by exhaustive
enumeration of a finite fixture, (b) at least one planted hostile whose mutation is asserted applied
and which must be caught, and (c) a no-alarm control.  The minimal objects of the OCM core are
re-implemented here (antichain semiring, warrant intervals, Kleene liveness, the batch-5 E2 trace
grammar and E3 certificate shape, a hash-chained ledger); nothing is imported from ``ocm``.  Every
probability, power and size is an exact ``Fraction``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import sys
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


# ---------------------------------------------------------------------------------------------
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21) — as in batches 1–5
# ---------------------------------------------------------------------------------------------


def canon(items):
    unique = {frozenset(w) for w in items}
    return tuple(sorted((w for w in unique if not any(v < w for v in unique)), key=lambda w: (len(w), sorted(map(repr, w)))))


ZERO, ONE = (), (frozenset(),)


def join(p, q):
    return canon((*p, *q))


def meet(p, q):
    if not p or not q:
        return ZERO
    return canon(a | b for a in p for b in q)


def live(p, r):
    r = frozenset(r)
    return any(not (w & r) for w in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def liveness(iv, r):
    lo, up = iv
    if live(lo, r):
        return LIVE
    if not live(up, r):
        return DEAD
    return UNKNOWN


def cert(*warrants):
    p = canon(frozenset(w) for w in warrants)
    return (p, p)


def subsets(universe, max_size=None):
    u = sorted(universe, key=repr)
    top = len(u) if max_size is None else max_size
    return [frozenset(c) for k in range(top + 1) for c in itertools.combinations(u, k)]


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=repr).encode()).hexdigest()


ALPHA = Fraction(1, 20)


def binom_pmf(n, k, p):
    return Fraction(math.comb(n, k)) * p ** k * (1 - p) ** (n - k)


def binom_tail(n, k, p):
    """P(Bin(n, p) ≥ k), exact."""
    return sum((binom_pmf(n, j, p) for j in range(k, n + 1)), Fraction(0))


# ---------------------------------------------------------------------------------------------
# F1 · P1 · capability-level revocation over ⊕ warrants
# ---------------------------------------------------------------------------------------------

EVIDENCE_F1 = ("e1", "e2", "e3", "e4")


def capability_profile(alternatives):
    """A capability resting on several warrants: the antichain (⊕) of its alternative evidence sets."""
    return canon(frozenset(w) for w in alternatives)


def live_alternatives(profile, revoked):
    return [w for w in profile if not (w & revoked)]


def revoke_named(profile, revoked, named, authority):
    """Reading 1: revoke the named evidence id only (what `revoke <eid>` does)."""
    if named not in authority:
        return revoked, {"reading": "REVOKE_NAMED", "status": "REFUSED_UNAUTHORIZED"}
    r2 = frozenset(revoked) | {named}
    rem = live_alternatives(profile, r2)
    return r2, {"reading": "REVOKE_NAMED", "status": "APPLIED", "capability": LIVE if rem else DEAD, "remainder": rem}


def revoke_all(profile, revoked, named, authority):
    """Reading 2: revoke every evidence id of the capability the speaker has authority over."""
    if named not in authority:
        return revoked, {"reading": "REVOKE_ALL", "status": "REFUSED_UNAUTHORIZED"}
    targets = {e for w in profile for e in w} & frozenset(authority)
    r2 = frozenset(revoked) | targets
    rem = live_alternatives(profile, r2)
    return r2, {"reading": "REVOKE_ALL", "status": "APPLIED", "capability": LIVE if rem else DEAD, "remainder": rem, "unauthorized_remainder": rem}


def notice_semantics(intent, profile, revoked, named, authority):
    """The licensed reply to a revocation notice as a policy over the warrant lattice.

    intent ∈ {LESSON, CAPABILITY, UNSPECIFIED}.  The named lesson is always revoked (the speaker asked
    for that); what differs is what else is revoked and what is *reported*: a live remainder is never
    silent."""
    if named not in authority:
        return revoked, "REFUSED_UNAUTHORIZED", []
    if intent == "LESSON":
        r2, rep = revoke_named(profile, revoked, named, authority)
        return r2, ("REVOKED_NAMED_REMAINDER_REPORTED" if rep["remainder"] else "REVOKED"), rep["remainder"]
    if intent == "CAPABILITY":
        r2, rep = revoke_all(profile, revoked, named, authority)
        return r2, ("CAPABILITY_PERSISTS_UNAUTHORIZED_REMAINDER" if rep["remainder"] else "CAPABILITY_REMOVED"), rep["remainder"]
    r2, rep = revoke_named(profile, revoked, named, authority)                      # UNSPECIFIED: revoke the named one, ask about the rest
    return r2, ("CLARIFY_REMAINDER" if rep["remainder"] else "REVOKED"), rep["remainder"]


def mutant_revoke_named_silent(intent, profile, revoked, named, authority):
    """Planted (M12 P1 shape): every notice is read as revoke-named and answered 'Revoked.' — a live remainder is never reported."""
    if named not in authority:
        return revoked, "REFUSED_UNAUTHORIZED", []
    r2, rep = revoke_named(profile, revoked, named, authority)
    return r2, "REVOKED", []


def check_f1_capability_revocation():
    pieces = [w for w in subsets(EVIDENCE_F1, 2) if w]                                   # alternatives of size 1–2
    profiles = []
    for k in (1, 2, 3):
        for combo in itertools.combinations(pieces, k):
            if len(canon(combo)) == k:                                               # antichains only
                profiles.append(canon(combo))
    priors = [frozenset()] + [frozenset({e}) for e in EVIDENCE_F1]
    n = cut_iff = hit_iff = monotone = honest_never_claims = clarify_cases = 0
    mutant_cases = mutant_caught = refused = 0
    for profile in profiles:
        evidence = sorted({e for w in profile for e in w})
        for named in evidence:
            for auth in subsets(EVIDENCE_F1):
                for R in priors:
                    n += 1
                    alive = live_alternatives(profile, R)
                    r_named, rep_named = revoke_named(profile, R, named, auth)
                    r_all, rep_all = revoke_all(profile, R, named, auth)
                    if named not in auth:
                        assert rep_named["status"] == rep_all["status"] == "REFUSED_UNAUTHORIZED" and r_named == r_all == R
                        refused += 1
                        continue
                    # (i) revoke-named kills the capability iff the named id is a cut of the live alternatives
                    assert (rep_named["capability"] == DEAD) == all(named in w for w in alive)
                    cut_iff += 1
                    # (ii) revoke-all kills the capability iff the speaker's authority hits every live alternative
                    assert (rep_all["capability"] == DEAD) == all(w & auth for w in alive)
                    hit_iff += 1
                    # (iii) monotone: revoke-all revokes at least what revoke-named does; the remainder is exactly the unauthorized alternatives
                    assert r_named <= r_all and set(rep_all["remainder"]) <= set(rep_named["remainder"])
                    assert all(not (w & auth) for w in rep_all["remainder"])
                    monotone += 1
                    # (iv) the licensed reply never claims removal while the capability is LIVE; a live remainder is named
                    for intent in ("LESSON", "CAPABILITY", "UNSPECIFIED"):
                        r2, reply, remainder = notice_semantics(intent, profile, R, named, auth)
                        assert (reply in ("CAPABILITY_REMOVED", "REVOKED")) == (not live_alternatives(profile, r2))
                        assert remainder == live_alternatives(profile, r2)
                        honest_never_claims += 1
                        clarify_cases += reply == "CLARIFY_REMAINDER"
                        # hostile: silent revoke-named answers 'Revoked.' while the capability is still LIVE
                        if intent in ("CAPABILITY", "UNSPECIFIED") and remainder:
                            mutant_cases += 1
                            _, m_reply, m_rem = mutant_revoke_named_silent(intent, profile, R, named, auth)
                            assert m_reply == "REVOKED" and m_rem == [] and live_alternatives(profile, r2)     # mutation applied; capability persists silently
                            mutant_caught += 1
    # M12 P1 fixture: the lesson word already had a LIVE sense from earlier in the lifetime; `revoke <later lesson>` (intent unspecified)
    word = capability_profile([{"L_early"}, {"L_late"}])
    r2, reply, remainder = notice_semantics("UNSPECIFIED", word, frozenset(), "L_late", {"L_early", "L_late"})
    assert reply == "CLARIFY_REMAINDER" and remainder == [frozenset({"L_early"})] and live(word, r2)
    _, m_reply, _ = mutant_revoke_named_silent("UNSPECIFIED", word, frozenset(), "L_late", {"L_early", "L_late"})
    assert m_reply == "REVOKED" and live(word, r2)                                            # 'revoked_stops' false: the M12 4/6 shape
    r3, reply3, rem3 = notice_semantics("CAPABILITY", word, frozenset(), "L_late", {"L_early", "L_late"})
    assert reply3 == "CAPABILITY_REMOVED" and not live(word, r3)                              # the capability reading removes it
    r4, reply4, rem4 = notice_semantics("CAPABILITY", word, frozenset(), "L_late", {"L_late"})
    assert reply4 == "CAPABILITY_PERSISTS_UNAUTHORIZED_REMAINDER" and rem4 == [frozenset({"L_early"})]   # without authority over L_early: reported, never silent
    # no-alarm: a single-warrant capability — all readings coincide, nothing to report (the fresh-arm 6/6 shape)
    single = capability_profile([{"L1"}])
    replies = {notice_semantics(i, single, frozenset(), "L1", {"L1"})[1] for i in ("LESSON", "CAPABILITY", "UNSPECIFIED")}
    assert replies == {"REVOKED", "CAPABILITY_REMOVED"} and all(not notice_semantics(i, single, frozenset(), "L1", {"L1"})[2] for i in ("LESSON", "CAPABILITY", "UNSPECIFIED"))
    return {"profiles": len(profiles), "cases": n, "refused_unauthorized": refused, "cut_iff_checks": cut_iff, "hitting_set_iff_checks": hit_iff, "monotone_checks": monotone,
            "reply_never_claims_removal_while_live": honest_never_claims, "clarify_cases": clarify_cases, "mutant_silent_cases": mutant_cases, "mutant_silent_caught": mutant_caught,
            "m12_two_sense_word": {"unspecified": reply, "capability": reply3, "capability_without_authority": reply4, "mutant": m_reply}, "single_warrant_no_alarm": 1}


# ---------------------------------------------------------------------------------------------
# F2 · P2 · the unit of inference for lifetime residuals
# ---------------------------------------------------------------------------------------------


def sign_test_p(n_d, wins):
    """One-sided exact sign test: P(Bin(n_d, ½) ≥ wins)."""
    return binom_tail(n_d, wins, Fraction(1, 2)) if n_d else Fraction(1)


def critical_value(n, alpha=ALPHA):
    """Smallest c with P(Bin(n, ½) ≥ c) ≤ α, or None when no rejection region exists."""
    for c in range(n + 1):
        if binom_tail(n, c, Fraction(1, 2)) <= alpha:
            return c
    return None


def pooled_orderings(per_ordering):
    """Planted design (S32): pool the discordant counts of k orderings of one lifetime as if k independent lifetimes."""
    return sum(w for w, _ in per_ordering), sum(l for _, l in per_ordering)


def lifetime_design(per_ordering, distinct_streams):
    """Honest unit accounting: orderings of ONE task stream are re-orderings of one lifetime (n_lifetimes = 1); only distinct
    streams count.  Returns the unit count and the verdict tier."""
    if not per_ordering:
        return 0, "CANNOT_CHECK"
    n_units = len(per_ordering) if distinct_streams else 1
    if n_units < 5:                                                                    # no sign-test rejection region below 5 units
        return n_units, "DESCRIPTIVE"
    wins = sum(1 for w, l in per_ordering if w > l)
    ties = sum(1 for w, l in per_ordering if w == l)
    return n_units, ("RESIDUAL_SUPPORTED" if sign_test_p(n_units - ties, wins) <= ALPHA else "DESCRIPTIVE")


def mutant_pool_orderings(per_ordering):
    """Planted: report the pooled McNemar/sign p as inferential."""
    w, l = pooled_orderings(per_ordering)
    return "RESIDUAL_SUPPORTED" if sign_test_p(w + l, max(w, l)) <= ALPHA else "DESCRIPTIVE"


def size_under_block_dependence(n, block):
    """Exact size of the item-level sign test at α when the n items fall into n/block blocks whose outcomes are decided by one
    fair latent coin each (ρ = 1 within a block, independent across blocks)."""
    if type(n) is not int or type(block) is not int or n <= 0 or block <= 0 or n % block:
        raise CannotCheck("positive integer n must be exactly partitioned into equal positive blocks")
    c = critical_value(n)
    if c is None:
        return Fraction(0)
    m = n // block
    need = -(-c // block)                                                                # ⌈c / block⌉ blocks must favour one arm
    return binom_tail(m, need, Fraction(1, 2))


def paired_lifetime_power(m, p, alpha=ALPHA):
    """Exact power of the sign test over m independent paired lifetimes when P(OCM beats parent within a pair) = p."""
    c = critical_value(m, alpha)
    return Fraction(0) if c is None else binom_tail(m, c, p)


def order_permutation_p(stats_by_ordering):
    """Within-lifetime permutation over task order: the exact reference distribution is the registered ordering family; tests
    order sensitivity, not the residual."""
    obs = stats_by_ordering[0]
    return Fraction(sum(1 for s in stats_by_ordering if s >= obs), len(stats_by_ordering))


def check_f2_unit_of_inference():
    # (a) pooling identical re-orderings: the M12 revoked_stops shape (OCM 4/6, parent 6/6 → discordant 0 OCM wins, 2 parent wins), replicated 3×
    single = (0, 2)
    p_single = sign_test_p(2, 2)
    p_pooled = [sign_test_p(*(lambda w, l: (w + l, max(w, l)))(*pooled_orderings([single] * k))) for k in (1, 2, 3)]
    assert p_single == Fraction(1, 4) and p_pooled == [Fraction(1, 4), Fraction(1, 16), Fraction(1, 64)]
    assert p_pooled[2] <= ALPHA < p_single                                                # significance manufactured from zero new information
    between_ordering_variance = Fraction(0)                                              # the three vectors are byte-identical (M12 V2 phases.*.A.post_deployment)
    n_eff = Fraction(3 * 2, 1 + (3 - 1) * 1)                                              # Kish design effect with ρ = 1 → n_eff = n
    assert between_ordering_variance == 0 and n_eff == 2
    # exhaustive: for every discordant table with n_d ≤ 6 and k ∈ {2, 3}, pooling never raises the p-value; count the tables where it crosses α
    monotone = crossings = 0
    for n_d in range(1, 7):
        for w in range(n_d + 1):
            p1 = sign_test_p(n_d, max(w, n_d - w))
            for k in (2, 3):
                pk = sign_test_p(k * n_d, k * max(w, n_d - w))
                assert pk <= p1
                monotone += 1
                crossings += (pk <= ALPHA) and (p1 > ALPHA)
    # honest unit accounting refuses; the planted pooling declares a residual
    n_units, verdict = lifetime_design([(2, 0)] * 3, distinct_streams=False)
    assert (n_units, verdict) == (1, "DESCRIPTIVE") and mutant_pool_orderings([(2, 0)] * 3) == "RESIDUAL_SUPPORTED"
    # (b) exact size of the item-level test under within-lifetime dependence: n = 54 items (the M12 conversations family)
    sizes = {b: size_under_block_dependence(54, b) for b in (1, 2, 3, 6, 9, 18, 27, 54)}
    assert sizes[1] <= ALPHA and sizes[54] == Fraction(1, 2) and all(sizes[b] >= sizes[1] for b in sizes)
    assert all(sizes[b] > ALPHA for b in (6, 9, 18, 27, 54))
    # a lifetime whose items are one latent coin: size ½ at every n ≥ 5 regardless of n
    assert all(size_under_block_dependence(n, n) == Fraction(1, 2) for n in (5, 12, 54))
    # (c) valid design: m independent paired lifetimes with matched task streams; exact size ≤ α and exact power
    size_ok = 0
    for m in range(5, 31):
        c = critical_value(m)
        assert c is not None and binom_tail(m, c, Fraction(1, 2)) <= ALPHA
        size_ok += 1
    assert critical_value(4) is None                                                      # no rejection region below 5 lifetimes
    power = {m: {str(p): paired_lifetime_power(m, p) for p in (Fraction(7, 10), Fraction(4, 5), Fraction(9, 10), Fraction(19, 20))} for m in (5, 6, 8, 10, 12, 16, 20)}
    assert power[5]["9/10"] == Fraction(9, 10) ** 5 and power[8]["9/10"] == Fraction(9, 10) ** 8 + 8 * Fraction(9, 10) ** 7 * Fraction(1, 10)
    assert power[8]["9/10"] > Fraction(4, 5) and power[5]["7/10"] < Fraction(1, 5)
    # pooling genuinely independent lifetimes is valid: exact size of the sign test over k·m independent units stays ≤ α (no alarm)
    assert all(binom_tail(k * 6, critical_value(k * 6), Fraction(1, 2)) <= ALPHA for k in (1, 2, 3))
    honest_units, honest_verdict = lifetime_design([(2, 0), (2, 0), (1, 0), (2, 0), (2, 0), (1, 0)], distinct_streams=True)
    assert (honest_units, honest_verdict) == (6, "RESIDUAL_SUPPORTED")                   # 6 independent lifetimes, all favouring OCM: p = 1/64
    # (d) within-lifetime permutation over task order on the deterministic replicas: statistic identical → p = 1 (valid, uninformative about the residual)
    assert order_permutation_p([4, 4, 4]) == 1 and order_permutation_p([5, 4, 3]) == Fraction(1, 3)
    return {"m12_revoked_stops_p_single": str(p_single), "pooled_p_by_k": [str(x) for x in p_pooled], "between_ordering_variance": str(between_ordering_variance), "n_eff_kish_rho1": str(n_eff),
            "pooling_monotone_checks": monotone, "pooling_crosses_alpha_tables": crossings, "mutant_pool_orderings_caught": 1, "honest_units_for_three_orderings": n_units,
            "size_n54_by_block": {str(b): str(v) for b, v in sizes.items()}, "latent_coin_size": "1/2", "sign_test_size_ok_m5_30": size_ok, "min_lifetimes_for_rejection": 5,
            "power_by_m_and_p": {str(m): {p: str(v) for p, v in row.items()} for m, row in power.items()}, "independent_pooling_no_alarm": 1, "order_permutation_p_identical": "1"}


# ---------------------------------------------------------------------------------------------
# F3 · P3 · observational limits of self-diagnosis (batch-5 E2 grammar)
# ---------------------------------------------------------------------------------------------

FIELDS = {"complete": (True, False), "resource": ("OK", "EXHAUSTED"), "authority": ("OK", "MISSING"), "drift": ("NONE", "DRIFT"), "info": ("PRESENT", "MISSING"),
          "order": ("OK", "BAD"), "router": ("CORRECT", "WRONG"), "operator": ("OK", "DEFECT"), "adapter": ("OK", "BAD")}
ALTERNATIVES = ("router_alt", "operator_alt", "adapter_alt")
ATTEMPT = (None, (LIVE, False), (LIVE, True), (DEAD, False), (DEAD, True))
TRIED = ATTEMPT[1:]
METHOD = ("WRONG_OPERATOR", "OPERATOR_WRONG", "BAD_ADAPTER")


def certificate_valid(attempts, witness):
    return all(attempts[a] is not None for a in ALTERNATIVES) and not any(attempts[a][1] for a in ALTERNATIVES) and all(attempts[a][0] == LIVE for a in ALTERNATIVES) and witness


def nominal(f):
    return f["complete"] and f["resource"] == "OK" and f["authority"] == "OK" and f["drift"] == "NONE" and f["info"] == "PRESENT" and f["order"] == "OK"


def classify(trace):
    """Batch-5 E2 classifier (pure function of the typed trace)."""
    f, attempts, witness = trace
    if not f["complete"]:
        return "CANNOT_CHECK"
    if f["resource"] == "EXHAUSTED":
        return "RESOURCE"
    if f["authority"] == "MISSING":
        return "AUTHORITY"
    if f["drift"] == "DRIFT":
        return "DRIFT"
    if f["info"] == "MISSING":
        return "MISSING_INFORMATION"
    if f["order"] == "BAD":
        return "BAD_ORDER"
    if certificate_valid(attempts, witness):
        return "REPRESENTATION"
    return observational_method_verdict(f)


def observational_method_verdict(f):
    if f["router"] == "WRONG":
        return "WRONG_OPERATOR"
    if f["operator"] == "DEFECT":
        return "OPERATOR_WRONG"
    if f["adapter"] == "BAD":
        return "BAD_ADAPTER"
    return "INSUFFICIENT_EVIDENCE"


def all_observations():
    keys = list(FIELDS)
    for values in itertools.product(*(FIELDS[k] for k in keys)):
        yield dict(zip(keys, values))


def completions():
    for att in itertools.product(ATTEMPT, repeat=3):
        for witness in (True, False):
            yield dict(zip(ALTERNATIVES, att)), witness


def consistent_verdicts(f):
    """The set of layer verdicts consistent with the observational record alone (no counterfactual access)."""
    return {classify((f, attempts, w)) for attempts, w in completions()}


def posterior_rep(prior_rep, f, repeats):
    """Honest Bayes: the observation f is implied by REPRESENTATION and by m(f) alike (likelihood ratio 1), so repetition leaves the
    posterior at the prior."""
    return prior_rep if nominal(f) else (Fraction(1) if consistent_verdicts(f) == {"REPRESENTATION"} else Fraction(0))


def mutant_posterior_from_repetition(prior_rep, f, repeats, factor=Fraction(2)):
    """Planted (M11 §2/§4 hostile in distribution form): each repeated failure doubles the odds of an architecture problem."""
    odds = prior_rep / (1 - prior_rep) * factor ** repeats
    return odds / (1 + odds)


def identify_adaptive(trace):
    """Cheapest counterfactual identification: run the registered alternatives in order, stop at the first success; if all fail,
    read the attempt warrants from the ledger (observational) and evaluate the ceiling witness (a check, not a run)."""
    f, attempts, witness = trace
    if not nominal(f):
        return classify(trace), 0
    runs = 0
    for a in ALTERNATIVES:
        runs += 1
        if attempts[a][1]:
            return observational_method_verdict(f), runs                                 # one success ⇒ certificate invalid ⇒ verdict observational
    return ("REPRESENTATION" if certificate_valid(attempts, witness) else observational_method_verdict(f)), runs


def mutant_two_run_design(trace):
    """Planted: a fixed two-counterfactual design (router, operator) certifies the ceiling without trying the adapter alternative."""
    f, attempts, witness = trace
    if not nominal(f):
        return classify(trace)
    two = {a: attempts[a] for a in ALTERNATIVES[:2]}
    if all(v is not None and not v[1] and v[0] == LIVE for v in two.values()) and witness:
        return "REPRESENTATION"
    return observational_method_verdict(f)


def check_f3_observational_limits():
    n_obs = identified = ambiguous = 0
    rep_completions = other_completions = 0
    for f in all_observations():
        n_obs += 1
        C = consistent_verdicts(f)
        if nominal(f):
            assert C == {"REPRESENTATION", observational_method_verdict(f)}
            ambiguous += 1
            rep_completions += sum(1 for att, w in completions() if classify((f, att, w)) == "REPRESENTATION")
            other_completions += sum(1 for att, w in completions() if classify((f, att, w)) != "REPRESENTATION")
        else:
            assert len(C) == 1
            identified += 1
    assert (n_obs, identified, ambiguous) == (512, 504, 8) and rep_completions == 8 and other_completions == 8 * 249
    # (ii) no observational update: the honest posterior after k identical failures equals the prior; the planted one converges to 1
    prior = Fraction(1, 250)
    f0 = {k: v[0] for k, v in FIELDS.items()}
    honest = [posterior_rep(prior, f0, k) for k in range(6)]
    mutant = [mutant_posterior_from_repetition(prior, f0, k) for k in range(6)]
    assert all(h == prior for h in honest) and mutant[0] == prior and mutant[5] > mutant[3] > prior and mutant[5] > Fraction(1, 10)
    # (iii) adaptive identification is exact on every fully-tried trace; worst case 3 runs; expected runs exact
    n_full = agree = runs_total = 0
    max_runs = 0
    two_run_caught = two_run_cases = 0
    zero_runs_on_identified = 0
    for f in all_observations():
        for att in itertools.product(TRIED, repeat=3):
            attempts = dict(zip(ALTERNATIVES, att))
            for witness in (True, False):
                trace = (f, attempts, witness)
                v, runs = identify_adaptive(trace)
                assert v == classify(trace)
                n_full += 1
                agree += 1
                if nominal(f):
                    runs_total += runs
                    max_runs = max(max_runs, runs)
                    if attempts["adapter_alt"][1] and all(attempts[a] == (LIVE, False) for a in ALTERNATIVES[:2]) and witness:
                        two_run_cases += 1
                        assert mutant_two_run_design(trace) == "REPRESENTATION" and classify(trace) != "REPRESENTATION"   # restoring adapter solves the task: caught
                        two_run_caught += 1
                else:
                    zero_runs_on_identified += runs == 0
    n_nominal_full = 8 * 64 * 2
    expected_runs = Fraction(runs_total, n_nominal_full)
    assert max_runs == 3 and n_full == 512 * 128
    # (iv) no fixed design with fewer than three runs identifies: for every proper subset S of the alternatives there is a pair of
    # fully-tried nominal traces agreeing on f, on the attempts in S and on the witness, with different verdicts
    nonidentifying = 0
    for k in range(3):
        for S in itertools.combinations(ALTERNATIVES, k):
            rest = [a for a in ALTERNATIVES if a not in S]
            base = {a: (LIVE, False) for a in ALTERNATIVES}
            other = dict(base)
            other[rest[0]] = (LIVE, True)
            t1, t2 = (f0, base, True), (f0, other, True)
            assert all(t1[1][a] == t2[1][a] for a in S) and classify(t1) == "REPRESENTATION" and classify(t2) == "INSUFFICIENT_EVIDENCE"
            nonidentifying += 1
    assert nonidentifying == 7
    return {"observations": n_obs, "identified_by_observation": identified, "ambiguous_nominal": ambiguous, "verdict_set_size_on_nominal": 2,
            "representation_completions_per_nominal": 1, "completions_per_observation": 250, "honest_posterior_constant_over_repeats": [str(h) for h in honest],
            "mutant_posterior_over_repeats": [str(m) for m in mutant], "mutant_repetition_caught": 1, "fully_tried_traces": n_full, "adaptive_exact": agree,
            "adaptive_worst_case_runs": max_runs, "adaptive_expected_runs_uniform": str(expected_runs), "zero_runs_on_identified_observations": zero_runs_on_identified,
            "mutant_two_run_cases": two_run_cases, "mutant_two_run_caught": two_run_caught, "proper_subsets_nonidentifying": nonidentifying}


# ---------------------------------------------------------------------------------------------
# F4 · P4 · false-structural-alarm lemma
# ---------------------------------------------------------------------------------------------

EVIDENCE_F4 = ("e1", "e2", "e3")
LAYER_ORDER = ("D0", "D1", "D2", "D5", "D6", "D3")                                    # OCM diagnose.ORDER prefix; D3 = representation
LOCAL = {"D0", "D1", "D2", "D5", "D6"}


def run_path(path, used, revoked, defect, ceiling):
    """A run succeeds iff every object on the path is used through a LIVE warrant, no operator defect, and the target is inside
    the representation (no ceiling)."""
    for alts, j in zip(path, used):
        if liveness(cert(alts[j]), revoked) != LIVE:
            return False
    return not defect and not ceiling


def dead_on_path(path, used, revoked):
    return [i for i, (alts, j) in enumerate(zip(path, used)) if liveness(cert(alts[j]), revoked) != LIVE]


def ablate(layer, path, used, revoked, defect, ceiling):
    """Single-layer counterfactuals: D1 reroute each dead object to a LIVE alternative if one exists; D2 restore the operator
    (reinstate the used warrant's evidence / clear the defect); D3 lift the ceiling.  D0/D5/D6 are inert on this fixture."""
    if layer == "D1":
        new_used = list(used)
        for i in dead_on_path(path, used, revoked):
            alive = [k for k, w in enumerate(path[i]) if liveness(cert(w), revoked) == LIVE]
            if not alive:
                return False
            new_used[i] = alive[0]
        return run_path(path, new_used, revoked, defect, ceiling)
    if layer == "D2":
        r2 = frozenset(revoked) - frozenset().union(*(path[i][used[i]] for i in dead_on_path(path, used, revoked))) if dead_on_path(path, used, revoked) else frozenset(revoked)
        return run_path(path, used, r2, False, ceiling)
    if layer == "D3":
        return run_path(path, used, revoked, defect, False)
    return False


def minimum_sufficient(path, used, revoked, defect, ceiling):
    for layer in LAYER_ORDER:
        if ablate(layer, path, used, revoked, defect, ceiling):
            return layer
    return None


def certificate_status(path, used, revoked, ceiling):
    """E3 shape: the LIVE clause first, then the ceiling witness."""
    if dead_on_path(path, used, revoked):
        return "REINSTATE_FIRST"
    return "OBSTRUCTION" if ceiling else "LOWER_LEVEL_SUFFICIENT"


def mutant_dead_is_structural(path, used, revoked, defect, ceiling):
    """Planted (M11 S5 / M12 F shape): a revoked dependency makes every task fail, so the failure is read as structural (D3)."""
    if dead_on_path(path, used, revoked):
        return "D3"
    return minimum_sufficient(path, used, revoked, defect, ceiling)


def check_f4_false_structural_alarm():
    alt_sets = [tuple(sorted(w)) for w in subsets(EVIDENCE_F4, 2) if w]                   # an object's alternatives: 1–2 singleton warrants
    objects = [tuple(frozenset({e}) for e in alts) for alts in alt_sets]
    n = explained = lemma = converse_dead_not_explained = converse_local_without_dead = cert_invalid_when_dead = 0
    reinstate_then_escalate = mutant_caught = no_dead_no_alarm = failed = 0
    for k in (1, 2, 3):
        for path in itertools.product(objects, repeat=k):
            for used in itertools.product(*(range(len(o)) for o in path)):
                for R in subsets(EVIDENCE_F4):
                    for defect in (False, True):
                        for ceiling in (False, True):
                            n += 1
                            ok = run_path(path, used, R, defect, ceiling)
                            dead = dead_on_path(path, used, R)
                            ms = minimum_sufficient(path, used, R, defect, ceiling)
                            if ok:
                                continue
                            failed += 1
                            reinstated_ok = ablate("D2", path, used, R, defect, ceiling) if dead else None
                            is_explained = bool(dead) and (not defect and not ceiling)
                            if is_explained:
                                # lemma: a failure explained by a DEAD warrant on the path has minimum-sufficient layer ≤ D2
                                assert ms in ("D1", "D2") and reinstated_ok
                                assert certificate_status(path, used, R, ceiling) == "REINSTATE_FIRST"
                                explained += 1
                                lemma += 1
                                assert mutant_dead_is_structural(path, used, R, defect, ceiling) == "D3"                  # mutation applied and caught
                                mutant_caught += 1
                            if dead and not is_explained:
                                # converse (a): a dead warrant with a genuine defect/ceiling does not explain the failure; the certificate is
                                # still REINSTATE_FIRST — escalation waits for reinstatement, after which the fresh verdict is the true one
                                assert certificate_status(path, used, R, ceiling) == "REINSTATE_FIRST"
                                r2 = frozenset(R) - frozenset().union(*(path[i][used[i]] for i in dead))
                                fresh = minimum_sufficient(path, used, r2, defect, ceiling)
                                assert fresh == ("D2" if defect and not ceiling else ("D3" if ceiling and not defect else None))
                                assert certificate_status(path, used, r2, ceiling) == ("OBSTRUCTION" if ceiling else "LOWER_LEVEL_SUFFICIENT")
                                converse_dead_not_explained += 1
                                reinstate_then_escalate += ceiling and not defect
                            if dead:
                                assert certificate_status(path, used, R, ceiling) != "OBSTRUCTION"
                                cert_invalid_when_dead += 1
                            if not dead:
                                # converse (b): a local verdict without any dead warrant (plain operator defect) — the lemma is silent, no alarm
                                assert ms == ("D2" if defect and not ceiling else ("D3" if ceiling and not defect else None))
                                assert mutant_dead_is_structural(path, used, R, defect, ceiling) == ms
                                converse_local_without_dead += defect
                                no_dead_no_alarm += 1
    assert explained > 0 and converse_dead_not_explained > 0 and converse_local_without_dead > 0
    return {"fixtures": n, "failed_runs": failed, "explained_by_dead_warrant": explained, "lemma_checks": lemma, "certificate_never_obstruction_when_dead": cert_invalid_when_dead,
            "converse_dead_but_not_explained": converse_dead_not_explained, "reinstate_then_fresh_obstruction": reinstate_then_escalate, "converse_local_without_dead": converse_local_without_dead,
            "mutant_dead_is_structural_caught": mutant_caught, "no_dead_no_alarm": no_dead_no_alarm}


# ---------------------------------------------------------------------------------------------
# F5 · P5 · epistemic identity of a persistent machine
# ---------------------------------------------------------------------------------------------


def chain_head(genesis, events):
    h = genesis
    for ev in events:
        h = hashlib.sha256((h + digest(ev)).encode()).hexdigest()
    return h


class Ledger:
    def __init__(self, root_id, events=None):
        self.root_id = root_id
        self.genesis = hashlib.sha256(f"genesis:{root_id}".encode()).hexdigest()
        self.events = list(events or [])

    def append(self, ev):
        self.events.append(ev)

    def head(self):
        return chain_head(self.genesis, self.events)

    def heads(self):
        return [chain_head(self.genesis, self.events[:i]) for i in range(len(self.events) + 1)]

    def evidence(self):
        return {ev["eid"]: ev["payload"] for ev in self.events if ev["kind"] == "ADMIT"}

    def fingerprints(self):
        fps = {}
        for ev in self.events:
            if ev["kind"] == "ADOPT":
                fps[ev["component"]] = ev["fp"]
        return fps

    def lineage(self):
        return [(ev["component"], ev["prev"], ev["fp"]) for ev in self.events if ev["kind"] == "ADOPT"]

    def revoked(self):
        return frozenset(ev["eid"] for ev in self.events if ev["kind"] == "REVOKE")


def identity_of(ledger, running_components):
    return {"genesis": ledger.genesis, "head": ledger.head(), "fingerprints": ledger.fingerprints(), "lineage": ledger.lineage(), "running": dict(running_components)}


def same_machine(before, ledger_after, running_after):
    """Honest identity check: same genesis; the pre-restart head is on the reopened chain (prefix); the running component
    fingerprints are the ledger-derived ones; the adoption lineage is the ledger-derived one (a prefix extension)."""
    if ledger_after.genesis != before["genesis"] or before["head"] not in ledger_after.heads():
        return False, "ROOT_OR_PREFIX_BROKEN"
    fingerprints = {}
    for component, previous, current in ledger_after.lineage():
        if previous != fingerprints.get(component):
            return False, "ADOPTION_PREDECESSOR_MISMATCH"
        fingerprints[component] = current
    if ledger_after.fingerprints() != dict(running_after):
        return False, "COMPONENT_NOT_ADOPTED_THROUGH_LEDGER"
    if ledger_after.lineage()[: len(before["lineage"])] != before["lineage"]:
        return False, "LINEAGE_REWRITTEN"
    return True, "SAME_MACHINE"


def stale_handle_check(machine):
    """Planted (M12 S31): identity judged by object identity of a runtime handle."""
    return machine["handle"] is machine["runtime_at_start"]


def path_check(machine, before_root):
    """Planted: identity judged by the root path string."""
    return machine["active"].root_id == before_root


class Machine:
    pass


def build_machine(rng, tag):
    led = Ledger(f"/root/{tag}")
    comps = {"router": f"router-{tag}-v1", "operator": f"op-{tag}-v1"}
    for c, fp in comps.items():
        led.append({"kind": "ADOPT", "component": c, "prev": None, "fp": fp})
    atoms = {}
    for i in range(rng.randint(3, 6)):
        eid = f"{tag}:ev{i}"
        led.append({"kind": "ADMIT", "eid": eid, "payload": {"bytes": rng.randint(0, 999)}})
        atoms[f"{tag}:x{i}"] = cert({eid}) if i % 2 == 0 or i == 0 else cert({eid}, {f"{tag}:ev{i-1}"})
    if rng.random() < 0.5:
        led.append({"kind": "REVOKE", "eid": f"{tag}:ev0"})
    led.append({"kind": "ADOPT", "component": "operator", "prev": comps["operator"], "fp": f"op-{tag}-v2"})
    adopted_in_memory = {f"op-{tag}-v2": {"previous": comps["operator"]}}                # a rollback artifact kept only in process memory
    comps["operator"] = f"op-{tag}-v2"
    return {"active": led, "handle": led, "runtime_at_start": led, "components": comps, "atoms": atoms, "adopted_in_memory": adopted_in_memory}


def restart_honest(m):
    reopened = Ledger(m["active"].root_id, m["active"].events)                          # persist + reopen: replay of the same chain
    return {**m, "active": reopened, "handle": reopened, "adopted_in_memory": {}}         # process memory does not survive a restart


def rollback_possible(m, from_ledger):
    """Rollback of the last adoption needs its lineage: derivable from the ledger, or lost with process memory."""
    if from_ledger:
        return any(prev is not None for _, prev, _ in m["active"].lineage())
    return bool(m["adopted_in_memory"])


def restart_split(m):
    """S31: the inherited restart reopens a session at a different path; the machine keeps its old handle (stale)."""
    fresh = Ledger(m["active"].root_id + "/reopened")
    for c, fp in m["components"].items():
        fresh.append({"kind": "ADOPT", "component": c, "prev": None, "fp": fp})
    return {**m, "active": fresh}                                                          # handle unchanged: stale


def restart_same_path_truncated(m):
    fresh = Ledger(m["active"].root_id)                                                   # same path, the event log replaced
    for c, fp in m["components"].items():
        fresh.append({"kind": "ADOPT", "component": c, "prev": None, "fp": fp})
    return {**m, "active": fresh, "handle": fresh}


def restart_component_swapped_out_of_band(m):
    r = restart_honest(m)
    return {**r, "components": {**r["components"], "router": r["components"]["router"] + "-patched"}}


def restart_lineage_rewritten(m):
    events = [ev for ev in m["active"].events if not (ev["kind"] == "ADOPT" and ev["prev"] is not None)]   # the adoption event deleted from the log
    reopened = Ledger(m["active"].root_id, events)
    comps = dict(m["components"])
    comps["operator"] = next(ev["fp"] for ev in events if ev["kind"] == "ADOPT" and ev["component"] == "operator")
    return {**m, "active": reopened, "handle": reopened, "components": comps}


def commit_after(m, eids):
    """A commitment made after the restart cites evidence ids; it is the same machine's iff every id resolves on the active chain to
    the pre-restart bytes and the chain extends the pre-restart head."""
    return {"cites": list(eids), "head": m["active"].head()}


def attributable(commitment, before, ledger_after, evidence_before):
    heads = ledger_after.heads()
    if ledger_after.genesis != before["genesis"] or before["head"] not in heads or commitment.get("head") not in heads:
        return False
    committed_at = heads.index(commitment["head"])
    if committed_at < heads.index(before["head"]):
        return False
    ev = Ledger(ledger_after.root_id, ledger_after.events[:committed_at]).evidence()
    return all(e in evidence_before and e in ev and ev[e] == evidence_before[e] for e in commitment["cites"])


def check_f5_epistemic_identity():
    rng = random.Random(6)
    machines = [build_machine(rng, f"m{i}") for i in range(20)]
    honest_pass = liveness_preserved = split_caught = stale_passes_split = path_passes_truncated = truncated_caught = 0
    swap_caught = lineage_caught = commitments_not_attributable = commitments_attributable = lineage_in_memory_lost = 0
    reasons = {}
    for m in machines:
        before = identity_of(m["active"], m["components"])
        evidence_before = m["active"].evidence()
        R = m["active"].revoked()
        # (i) honest restart: same machine; every atom's liveness unchanged by the restart; later commitments attributable
        h = restart_honest(m)
        ok, why = same_machine(before, h["active"], h["components"])
        assert ok and why == "SAME_MACHINE"
        assert all(liveness(iv, R) == liveness(iv, h["active"].revoked()) for iv in m["atoms"].values())
        liveness_preserved += len(m["atoms"])
        c = commit_after(h, list(evidence_before)[:2])
        assert attributable(c, before, h["active"], evidence_before)
        commitments_attributable += 1
        honest_pass += 1
        # lineage must live in the ledger: identity passes, yet an in-memory rollback artifact is gone after the restart
        assert rollback_possible(m, from_ledger=False) and rollback_possible(h, from_ledger=True) and not rollback_possible(h, from_ledger=False)
        lineage_in_memory_lost += 1
        # (ii) S31 split: the stale-handle check passes (mutation applied); the honest check catches it; commitments not attributable
        s = restart_split(m)
        assert stale_handle_check(s)
        stale_passes_split += 1
        ok, why = same_machine(before, s["active"], s["components"])
        assert not ok and why == "ROOT_OR_PREFIX_BROKEN"
        reasons[why] = reasons.get(why, 0) + 1
        split_caught += 1
        c = commit_after(s, list(evidence_before)[:2])
        assert not attributable(c, before, s["active"], evidence_before)
        commitments_not_attributable += 1
        # (iii) same path, truncated log: the path check passes; genesis equal but the prefix is broken
        t = restart_same_path_truncated(m)
        assert path_check(t, before_root=m["active"].root_id) and t["active"].genesis == before["genesis"]
        path_passes_truncated += 1
        ok, why = same_machine(before, t["active"], t["components"])
        assert not ok and why == "ROOT_OR_PREFIX_BROKEN"
        truncated_caught += 1
        # (iv) necessity of the other coordinates: out-of-band component swap (root fine) and lineage rewrite (fingerprints fine)
        w = restart_component_swapped_out_of_band(m)
        ok, why = same_machine(before, w["active"], w["components"])
        assert not ok and why == "COMPONENT_NOT_ADOPTED_THROUGH_LEDGER" and w["active"].genesis == before["genesis"]
        swap_caught += 1
        l = restart_lineage_rewritten(m)
        ok, why = same_machine(before, l["active"], l["components"])
        assert not ok and why == "ROOT_OR_PREFIX_BROKEN"                                    # deleting an event rewrites the chain: caught by the prefix
        lineage_caught += 1
    # lineage coordinate is independently necessary: a chain that keeps the prefix but appends a lineage that contradicts the recorded one
    m = machines[0]
    before = identity_of(m["active"], m["components"])
    forged = Ledger(m["active"].root_id, m["active"].events)
    forged.append({"kind": "ADOPT", "component": "operator", "prev": "op-nowhere", "fp": "op-m0-v3"})
    running = {**m["components"], "operator": "op-m0-v3"}
    ok, why = same_machine(before, forged, running)
    assert not ok and why == "ADOPTION_PREDECESSOR_MISMATCH"
    rewritten = Ledger(m["active"].root_id, m["active"].events)
    rewritten.append({"kind": "ADOPT", "component": "operator", "prev": "op-m0-v2", "fp": "op-m0-v3"})
    ok2, why2 = same_machine(before, rewritten, running)
    assert ok2 and why2 == "SAME_MACHINE"
    return {"machines": len(machines), "honest_restart_same_machine": honest_pass, "atom_liveness_preserved_checks": liveness_preserved, "commitments_attributable_after_honest_restart": commitments_attributable,
            "s31_split_stale_handle_passes": stale_passes_split, "s31_split_caught": split_caught, "commitments_not_attributable_after_split": commitments_not_attributable,
            "truncated_log_path_check_passes": path_passes_truncated, "truncated_log_caught": truncated_caught, "out_of_band_component_swap_caught": swap_caught, "lineage_rewrite_caught": lineage_caught,
            "in_memory_lineage_lost_after_restart": lineage_in_memory_lost, "honest_extension_no_alarm": 1, "reasons": reasons}


# ---------------------------------------------------------------------------------------------
# F6 · MEG-02 graded half · graded antichain under (max, ×) is exact; scalar retraction is not a function
# ---------------------------------------------------------------------------------------------

EVIDENCE_F6 = ("a", "b", "c", "d")


def grade_of(monomial, grades):
    out = Fraction(1)
    for e in monomial:
        out *= grades[e]
    return out


def graded_value_recompute(derivations, grades, revoked):
    """Ground truth: (max, ×) over the surviving derivations, recomputed from scratch."""
    vals = [grade_of(d, grades) for d in derivations if not (d & revoked)]
    return max(vals) if vals else Fraction(0)


def graded_antichain(derivations, grades):
    """The graded label: monomial → grade over the antichain reduction only."""
    return {w: grade_of(w, grades) for w in canon(derivations)}


def graded_retract(label, revoked):
    """Exact-share retraction on the graded label: drop the monomials hit by R (KS-T04b's 0/1 gate), grades ride outside the gate."""
    vals = [g for w, g in label.items() if not (w & revoked)]
    return max(vals) if vals else Fraction(0)


def mutant_scalar_subtract(scalar, revoked_grade):
    """Planted: retraction by subtracting the revoked derivation's grade from the collapsed scalar."""
    return max(scalar - revoked_grade, Fraction(0))


def probability_live(derivations, grades, revoked):
    """The (+, ×)-shaped grading read as a measure: P(some derivation survives) with independent evidence, revoked ids forced false;
    exact by world enumeration."""
    ids = sorted({e for d in derivations for e in d})
    eff = {e: (Fraction(0) if e in revoked else grades[e]) for e in ids}               # a revoked id is forced false
    total = Fraction(0)
    for bits in itertools.product((0, 1), repeat=len(ids)):
        world = frozenset(e for e, b in zip(ids, bits) if b)
        p = Fraction(1)
        for e, b in zip(ids, bits):
            p *= eff[e] if b else (1 - eff[e])
        if any(d <= world for d in derivations):
            total += p
    return total


def plus_times_sum(derivations, grades, revoked):
    return sum((grade_of(d, grades) for d in derivations if not (d & revoked)), Fraction(0))


def check_f6_graded_semiring_half():
    rng = random.Random(62)
    pieces = [w for w in subsets(EVIDENCE_F6, 3) if w]
    families = [set(c) for k in (1, 2, 3) for c in itertools.combinations(pieces, k)]
    grid = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]
    gradings = [{e: Fraction(1) for e in EVIDENCE_F6}] + [{e: rng.choice(grid) for e in EVIDENCE_F6} for _ in range(7)]
    revs = subsets(EVIDENCE_F6)
    n = absorption_exact = retraction_exact = gate_iff_live = 0
    for D in families:
        for grades in gradings:
            label = graded_antichain(D, grades)
            for R in revs:
                n += 1
                truth = graded_value_recompute(D, grades, R)
                # (a) absorption is exact for grades ≤ 1: the antichain label loses nothing
                assert graded_value_recompute(canon(D), grades, R) == truth
                absorption_exact += 1
                # (b) retraction on the graded label = recomputation over survivors (exact-share retraction lifts verbatim)
                assert graded_retract(label, R) == truth
                retraction_exact += 1
                # (c) the graded value is positive iff the antichain is LIVE under R (grade rides outside the 0/1 gate)
                assert (truth > 0) == (liveness((canon(D), canon(D)), R) == LIVE)
                gate_iff_live += 1
    # necessity of grades ≤ 1: with a grade above 1 absorption fails (superset monomial outgrades its subset)
    big = {"a": Fraction(1), "b": Fraction(2), "c": Fraction(1), "d": Fraction(1)}
    D_big = {frozenset({"a"}), frozenset({"a", "b"})}
    assert graded_value_recompute(D_big, big, frozenset()) == 2 and graded_value_recompute(canon(D_big), big, frozenset()) == 1
    # (d) scalar retraction is not a function of (scalar, revoked grade): exhaustive search for the smallest witness pair
    small_pieces = [w for w in subsets(("a", "b"), 1) if w] + [frozenset({"a", "b"})]
    small_families = [set(c) for k in (1, 2) for c in itertools.combinations(small_pieces, k)]
    small_grades = {"a": Fraction(9, 10), "b": Fraction(3, 5)}
    witnesses = []
    for D1, D2 in itertools.combinations(small_families, 2):
        for e in ("a", "b"):
            v1, v2 = graded_value_recompute(D1, small_grades, frozenset()), graded_value_recompute(D2, small_grades, frozenset())
            r1, r2 = graded_value_recompute(D1, small_grades, {e}), graded_value_recompute(D2, small_grades, {e})
            if v1 == v2 and r1 != r2:
                witnesses.append((sorted(sorted(d) for d in D1), sorted(sorted(d) for d in D2), e, str(v1), str(r1), str(r2)))
    witnesses.sort(key=lambda w: (sum(len(d) for d in w[0]) + sum(len(d) for d in w[1]), repr(w)))
    assert witnesses and witnesses[0][0] == [["a"]] and witnesses[0][1] == [["a"], ["b"]] and witnesses[0][2] == "a" and witnesses[0][3:] == ("9/10", "0", "3/5")
    # planted scalar subtraction is wrong on the witness (mutation applied: it returns 0 where the survivors give 3/5)
    D_w = {frozenset({"a"}), frozenset({"b"})}
    assert mutant_scalar_subtract(graded_value_recompute(D_w, small_grades, frozenset()), small_grades["a"]) == 0 != graded_value_recompute(D_w, small_grades, {"a"})
    # (e) (+, ×) read as a sum is not the measure: exact iff a single monomial survives; the measure itself retracts exactly on the antichain
    sum_exact = sum_over = measure_retract = 0
    sharing_witness = None
    for D in families:
        for grades in gradings[:3]:
            for R in (frozenset(), frozenset({"a"})):
                pl = plus_times_sum(D, grades, R)
                pr = probability_live(D, grades, R)
                survivors = [d for d in canon(D) if not (d & R)]
                if len([d for d in D if not (d & R)]) <= 1:                            # the sum is the measure iff at most one derivation survives
                    assert pl == pr
                    sum_exact += 1
                else:
                    assert pl >= pr
                    sum_over += pl > pr
                # retraction on the measure: forcing the revoked ids false equals the measure over the surviving monomials
                assert probability_live(set(survivors), grades, frozenset()) == pr
                measure_retract += 1
                if sharing_witness is None and pl > pr and any(x & y for x, y in itertools.combinations(survivors, 2)):
                    sharing_witness = (sorted(sorted(d) for d in survivors), str(pl), str(pr))
    pa, pb1, pb2 = Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)
    r3 = probability_live({frozenset({"a", "b"}), frozenset({"a", "c"})}, {"a": pa, "b": pb1, "c": pb2, "d": Fraction(1)}, frozenset())
    assert r3 == pa * (pb1 + pb2 - pb1 * pb2) == Fraction(3, 8)                             # batch-5 R3 witness reproduced as the measure
    # no-alarm: a single-derivation family — scalar subtraction and monomial retraction agree; (+, ×) sum equals the measure
    D1 = {frozenset({"a"})}
    assert mutant_scalar_subtract(graded_value_recompute(D1, small_grades, frozenset()), small_grades["a"]) == graded_value_recompute(D1, small_grades, {"a"}) == 0
    assert plus_times_sum(D1, small_grades, frozenset()) == probability_live(D1, small_grades, frozenset())
    return {"families": len(families), "gradings": len(gradings), "cases": n, "absorption_exact": absorption_exact, "graded_retraction_exact": retraction_exact, "positive_iff_live": gate_iff_live,
            "grade_above_one_breaks_absorption": 1, "scalar_witnesses_found": len(witnesses), "smallest_scalar_witness": witnesses[0], "mutant_scalar_subtract_caught": 1,
            "plus_times_sum_exact_cases": sum_exact, "plus_times_sum_strictly_over": sum_over, "measure_retraction_exact": measure_retract, "sharing_witness": sharing_witness,
            "r3_witness_as_measure": str(r3), "single_derivation_no_alarm": 1, "status": "PROVED (max,×) graded antichain; (+,×) measure PARENT_OWNED (inclusion–exclusion), not a semiring homomorphism"}


# ---------------------------------------------------------------------------------------------
# F7 · MEG-28 · ceilings for J2/J3 on the 3-input Boolean tower; MEG-07 per-source normalisation left OPEN
# ---------------------------------------------------------------------------------------------

INPUTS3 = list(itertools.product((0, 1), repeat=3))


_ANF = {}


def anf(table):
    """Algebraic normal form by Möbius transform: monomial (as a frozenset of variable indices) → coefficient."""
    if table in _ANF:
        return _ANF[table]
    coeff = {}
    for S in subsets(range(3)):
        s = 0
        for x in INPUTS3:
            if all(x[i] == 0 for i in range(3) if i not in S):
                s ^= table[INPUTS3.index(x)]
        coeff[S] = s
    _ANF[table] = coeff
    return coeff


def degree(table):
    return max((len(S) for S, c in anf(table).items() if c), default=0)


def witness_check(table, S):
    """Independent witness check: the parity of the table over the sub-cube {x : x_i = 0 for i ∉ S} is odd."""
    return sum(table[INPUTS3.index(x)] for x in INPUTS3 if all(x[i] == 0 for i in range(3) if i not in S)) % 2 == 1


ALL3 = [tuple(bits) for bits in itertools.product((0, 1), repeat=8)]
_LEVELS = {}


def level_space(level):
    """Nested tower: level 1 = affine (J1 composition closure), level 2 = degree ≤ 2 (J2 hypothesis expansion), level 3 = all (J3)."""
    if level not in _LEVELS:
        _LEVELS[level] = frozenset(t for t in ALL3 if degree(t) <= level)
    return _LEVELS[level]


def ceiling_certificate(table, level, enumerator=None):
    """C_ℓ(q): q ∉ S_ℓ with a checkable witness (a monomial of degree > ℓ with odd sub-cube parity)."""
    space = enumerator(level) if enumerator else level_space(level)
    if table in space:
        return {"status": "LOWER_LEVEL_SUFFICIENT", "level": level}
    ws = [S for S, c in anf(table).items() if c and len(S) > level]
    ws = [S for S in ws if witness_check(table, S)]
    return {"status": "CEILING", "level": level, "witness": sorted(sorted(S) for S in ws)}


def minimum_level(table, oracles=None):
    """Minimum sufficient level through the ceiling chain; CANNOT_CHECK where a level's ceiling predicate is unavailable."""
    for level in (1, 2, 3):
        if oracles and oracles.get(level) == "CANNOT_CHECK":
            return "CANNOT_CHECK"
        c = ceiling_certificate(table, level)
        if c["status"] == "LOWER_LEVEL_SUFFICIENT":
            return level
    return None


def assess_jump(table, incumbent, proposal_level, trigger, enumerator=None):
    """Governed Jump assessment on the tower (OCM assess_jump shape)."""
    if trigger.get("kind") not in {"EXPRESSIVE_CEILING"} or not trigger.get("witness_ids"):
        return "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
    if proposal_level <= incumbent:
        return "NOT_A_JUMP"
    for level in range(incumbent, proposal_level):
        c = ceiling_certificate(table, level, enumerator)
        if c["status"] != "CEILING" or not c["witness"]:
            return "NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT"
    if ceiling_certificate(table, proposal_level, enumerator)["status"] == "CEILING":
        return "PROPOSED_LEVEL_INSUFFICIENT"
    return "CANDIDATE_FOR_PROTECTED_EVALUATION"


def trigger_from_chain(table, incumbent, proposal_level):
    """The trigger is built from the incumbent level's ceiling certificate and from nothing else."""
    c = ceiling_certificate(table, incumbent)
    if c["status"] != "CEILING":
        return {"kind": None, "witness_ids": []}
    return {"kind": "EXPRESSIVE_CEILING", "witness_ids": [str(w) for w in c["witness"]]}


_PARTIAL2 = None


def mutant_partial_level2(level):
    """Planted: level-2 enumeration that only forms the products xy and yz (misses xz)."""
    global _PARTIAL2
    if level != 2:
        return level_space(level)
    if _PARTIAL2 is None:
        _PARTIAL2 = frozenset(t for t in ALL3 if all(not c or len(S) <= 1 or S in (frozenset({0, 1}), frozenset({1, 2})) for S, c in anf(t).items()))
    return _PARTIAL2


def mutant_poor_score_trigger():
    return {"kind": "POOR_SCORE", "witness_ids": ["score"]}


def check_f7_j2_j3_ceilings():
    sizes = {l: len(level_space(l)) for l in (1, 2, 3)}
    assert sizes == {1: 16, 2: 128, 3: 256} and level_space(1) < level_space(2) < level_space(3)
    n = min_level_equals_degree = witness_checks = admissible_iff = skip_refused = insufficient_refused = 0
    partial_caught = poor_score_refused = cannot_check_cases = 0
    for t in ALL3:
        n += 1
        m = minimum_level(t)
        assert m == max(1, degree(t))
        min_level_equals_degree += 1
        for level in (1, 2):
            c = ceiling_certificate(t, level)
            if c["status"] == "CEILING":
                assert c["witness"] and all(witness_check(t, frozenset(S)) and len(S) > level for S in c["witness"])
                witness_checks += 1
        # governed jump: admissible iff the proposed level is exactly the minimum sufficient level above the incumbent
        for incumbent in (1, 2):
            for proposal in (2, 3):
                if proposal <= incumbent:
                    continue
                verdict = assess_jump(t, incumbent, proposal, trigger_from_chain(t, incumbent, proposal))
                expected = "CANDIDATE_FOR_PROTECTED_EVALUATION" if (m == proposal and m > incumbent) else ("NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT" if m < proposal else "PROPOSED_LEVEL_INSUFFICIENT")
                if m <= incumbent:
                    expected = "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"                  # no ceiling at the incumbent level: no trigger
                assert verdict == expected
                admissible_iff += 1
                skip_refused += verdict == "NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT" and proposal == 3 and m == 2      # S6 harmful high-level jump refused
                insufficient_refused += verdict == "PROPOSED_LEVEL_INSUFFICIENT"
        # hostiles: POOR_SCORE trigger refused on every target; partial level-2 enumeration certifies falsely
        assert assess_jump(t, 1, 2, mutant_poor_score_trigger()) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
        poor_score_refused += 1
        honest2 = ceiling_certificate(t, 2)["status"]
        partial2 = ceiling_certificate(t, 2, mutant_partial_level2)["status"]
        if honest2 != partial2:
            assert honest2 == "LOWER_LEVEL_SUFFICIENT" and partial2 == "CEILING" and anf(t)[frozenset({0, 2})] == 1 and degree(t) == 2
            partial_caught += 1
        # undecidable ceiling at level 2: the minimum level is CANNOT_CHECK for every target outside level 1, never a jump to 3
        ml = minimum_level(t, oracles={2: "CANNOT_CHECK"})
        assert ml == (1 if degree(t) <= 1 else "CANNOT_CHECK")
        cannot_check_cases += ml == "CANNOT_CHECK"
    # batch-5 E3 embedding: the 2-input AND lifted to 3 inputs (ignoring z) has degree 2 → level-1 ceiling with the parity witness {x, y}
    and3 = tuple(x[0] & x[1] for x in INPUTS3)
    c1 = ceiling_certificate(and3, 1)
    assert c1["status"] == "CEILING" and c1["witness"] == [[0, 1]] and minimum_level(and3) == 2
    xor3 = tuple(x[0] ^ x[1] for x in INPUTS3)
    assert ceiling_certificate(xor3, 1)["status"] == "LOWER_LEVEL_SUFFICIENT"
    # no-alarm: affine targets produce no trigger at any proposed level
    affine_no_jump = sum(1 for t in level_space(1) for p in (2, 3) if assess_jump(t, 1, p, trigger_from_chain(t, 1, p)) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED")
    assert affine_no_jump == 32
    return {"targets": n, "level_sizes": {str(k): v for k, v in sizes.items()}, "minimum_level_equals_anf_degree": min_level_equals_degree, "witness_checks": witness_checks,
            "jump_admissible_iff_minimum_level": admissible_iff, "s6_skip_to_top_refused": skip_refused, "proposed_level_insufficient_refused": insufficient_refused,
            "mutant_poor_score_refused": poor_score_refused, "mutant_partial_level2_caught": partial_caught, "cannot_check_when_level2_oracle_missing": cannot_check_cases,
            "e3_and_embedding": {"level1": c1["status"], "witness": c1["witness"], "minimum_level": 2}, "affine_no_jump_no_alarm": affine_no_jump,
            "meg07_per_source_normalisation": "OPEN (not attempted in this batch)"}


# ---------------------------------------------------------------------------------------------
# F8 · P6 · information-budget binding for a reference arm
# ---------------------------------------------------------------------------------------------

ROWS = list(itertools.product((0, 1), repeat=2))
ALL16 = [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]


def version_space(examples):
    return [h for h in ALL16 if all(h[ROWS.index(x)] == y for x, y in examples)]


def unmeasured_bits_lower_bound(identified_at_k, class_size=16):
    """Worst-case extra binary capacity required for guaranteed zero-error identification.

    This is a capacity theorem under a registered hypothesis class, not evidence that
    a particular successful prediction consumed undisclosed information.
    """
    if type(class_size) is not int or class_size <= 0 or type(identified_at_k) is not int or identified_at_k < 0:
        raise CannotCheck("a positive class size and nonnegative integer observed-bit count are required")
    return max(0, (class_size - 1).bit_length() - identified_at_k)


def arm_label(declared_channels, identified_at_k, bound_k=4, *, guaranteed_identification=False):
    """Only a registered all-target identification guarantee can contradict the counting bound.

    One correct output can be a guess. The Boolean is a model assumption supplied by the
    finite specification, not a runtime attestation or evidence of a hidden channel.
    """
    if any(b == "UNMEASURED" for b in declared_channels.values()):
        return "REFERENCE"
    if any(type(b) is not int or b < 0 for b in declared_channels.values()):
        raise CannotCheck("declared channel capacities must be nonnegative integer bits")
    if type(identified_at_k) is not int or identified_at_k < 0 or type(bound_k) is not int or bound_k < 0:
        raise CannotCheck("identification capacity must be a nonnegative integer")
    # INSTRUCTION is the example budget: only k observed example bits are counted.
    # Other explicitly bounded channels can supply the remaining capacity.
    capacity = identified_at_k + sum(b for name, b in declared_channels.items() if name != "INSTRUCTION")
    if capacity < bound_k:
        return "BELOW_LOWER_BOUND_UNDECLARED_CHANNEL" if guaranteed_identification else "IDENTIFICATION_NOT_ESTABLISHED"
    return "CONSISTENT_WITH_MATCHED"


def paired_decision(ocm_wins, parent_wins):
    """Two-sided exact sign test at α; direction is reported only after both-tail control."""
    n_d = ocm_wins + parent_wins
    if n_d == 0:
        return "DESCRIPTIVE"
    if 2 * sign_test_p(n_d, ocm_wins) <= ALPHA:
        return "RESIDUAL_SUPPORTED"
    if 2 * sign_test_p(n_d, parent_wins) <= ALPHA:
        return "PARENT_DOMINATES"
    return "DESCRIPTIVE"


def comparison_report(matched_table, reference_table, reference_label):
    """The reference arm's result is reported beside the paired decision, never inside it."""
    if reference_label != "REFERENCE":
        raise CannotCheck("an arm with an unmeasured channel must be labelled REFERENCE")
    return {"paired_decision": paired_decision(*matched_table), "reference": {"table": reference_table, "reading": "reference, unmatched information; no performance bound"}}


def mutant_reference_as_matched(matched_table, reference_table):
    """Planted: the reference arm enters the paired decision as if it were the matched parent."""
    return paired_decision(*reference_table)


def mutant_prompt_matching_is_matching(declared_channels, identified_at_k):
    """Planted: identical registered inputs ⇒ 'matched', the version-space audit ignored."""
    return "MATCHED" if "INSTRUCTION" in declared_channels else "REFERENCE"


def check_f8_reference_arm_binding():
    n = vs_exact = identified_iff_four = bits_checks = label_checks = 0
    for target in ALL16:
        for k in range(5):
            for rows in itertools.combinations(ROWS, k):
                n += 1
                ex = [(x, target[ROWS.index(x)]) for x in rows]
                vs = version_space(ex)
                assert len(vs) == 2 ** (4 - k) and target in vs
                vs_exact += 1
                assert (len(vs) == 1) == (k == 4)
                identified_iff_four += 1
                # A zero-error guarantee over every target requires ≥ 4 − k additional bits in the worst case.
                assert unmeasured_bits_lower_bound(k) == 4 - k
                bits_checks += 1
    for declared in ({"INSTRUCTION": 4}, {"INSTRUCTION": 4, "PRETRAINING": "UNMEASURED"}):
        for k in range(5):
            label = arm_label(declared, k, guaranteed_identification=True)
            if "PRETRAINING" in declared:
                assert label == "REFERENCE"
            else:
                assert label == ("CONSISTENT_WITH_MATCHED" if k == 4 else "BELOW_LOWER_BOUND_UNDECLARED_CHANNEL")
            label_checks += 1
    # the M12 shape: OCM vs matched parent discordant 9–1 (p = 11/1024); a reference arm beats OCM 10–0
    matched, reference = (9, 1), (0, 10)
    report = comparison_report(matched, reference, arm_label({"INSTRUCTION": 4, "PRETRAINING": "UNMEASURED"}, 2))
    assert report["paired_decision"] == "RESIDUAL_SUPPORTED"
    assert mutant_reference_as_matched(matched, reference) == "PARENT_DOMINATES"            # mutation applied: the verdict flips
    try:
        comparison_report(matched, reference, "MATCHED")
        raise AssertionError("reference arm admitted as matched")
    except CannotCheck:
        pass                                                                                # the honest report refuses to enter it
    assert mutant_prompt_matching_is_matching({"INSTRUCTION": 4, "PRETRAINING": "UNMEASURED"}, 2) == "MATCHED"
    assert arm_label({"INSTRUCTION": 4}, 2, guaranteed_identification=True) == "BELOW_LOWER_BOUND_UNDECLARED_CHANNEL" and unmeasured_bits_lower_bound(2) == 2
    assert arm_label({"INSTRUCTION": 4}, 2) == "IDENTIFICATION_NOT_ESTABLISHED"
    # no-alarm: the matched parent identifies exactly at the bound; a declared reference reported beside the decision raises nothing
    assert arm_label({"INSTRUCTION": 4}, 4) == "CONSISTENT_WITH_MATCHED" and unmeasured_bits_lower_bound(4) == 0
    assert comparison_report((5, 5), (0, 10), "REFERENCE")["paired_decision"] == "DESCRIPTIVE"
    return {"target_x_example_sets": n, "version_space_exact": vs_exact, "identified_iff_four_examples": identified_iff_four, "outside_bits_checks": bits_checks, "label_checks": label_checks,
            "m12_shape": {"paired": report["paired_decision"], "mutant_reference_as_matched": mutant_reference_as_matched(matched, reference)}, "mutant_reference_as_matched_caught": 1,
            "mutant_prompt_matching_caught": 1, "undeclared_bits_on_k2": 2, "matched_parent_no_alarm": 1, "certified_matched_possible": False}


# ---------------------------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------------------------

CHECKS = {
    "F1_P1_capability_revocation": check_f1_capability_revocation,
    "F2_P2_unit_of_inference": check_f2_unit_of_inference,
    "F3_P3_observational_limits": check_f3_observational_limits,
    "F4_P4_false_structural_alarm": check_f4_false_structural_alarm,
    "F5_P5_epistemic_identity": check_f5_epistemic_identity,
    "F6_MEG02_graded_half": check_f6_graded_semiring_half,
    "F7_MEG28_j2_j3_ceilings": check_f7_j2_j3_ceilings,
    "F8_P6_reference_arm_binding": check_f8_reference_arm_binding,
}

STATUS = {"F1": "PROVED (policy over the warrant lattice; lattice facts PARENT_OWNED: ATMS/hitting sets)", "F2": "PROVED (exact sizes/powers; PARENT_OWNED: Hurlbert 1984, Kish design effect, exact sign test)",
          "F3": "PROVED (finite grammar)", "F4": "PROVED (finite fixture)", "F5": "PROVED (finite; hash chains PARENT_OWNED)",
          "F6": "PROVED (max,×) graded antichain; scalar retraction impossible (witness); (+,×) measure PARENT_OWNED", "F7": "PROVED J2/J3 on the 3-input tower; J4+ OPEN; MEG-07 OPEN",
          "F8": "PROVED (finite; Hartley/teaching dimension PARENT_OWNED)"}


def run_all():
    out = {name_: fn() for name_, fn in CHECKS.items()}
    out["ITEM_STATUS"] = STATUS
    out["OPEN"] = ["MEG-28 ceilings for J4+ (problem reformulation, tool invention)", "MEG-07 per-source normalisation", "MEG-02 (+,×) grading as a semiring homomorphism (not possible with sharing; measure only)"]
    out["NOVELTY"] = "NOT_ESTABLISHED"
    out["status"] = "ALL_HOLD"
    return out


def main(argv=None):
    if not __debug__:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": "assertion-based finite checks require assertions enabled"}))
        return 2
    try:
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
