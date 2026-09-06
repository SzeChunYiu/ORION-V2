"""Exact finite checker for KSO_FIELD_FRONTIER_THEOREMS_BATCH9_V1.md (stdlib only, exact).

One check function per field-frontier row of `field_dynamics_v1/FRONTIER.md` taken in batch 9:
I1 = FDX-08 (stochastic warrant dynamics), I2 = FDX-11 (epistemic bifurcation / obstruction),
I3 = FDX-13 (self-model calibration and reflexive dependence), I4 = FDX-15 (parent-product
equivalence / residual attribution).  Every check performs (a) the positive statement by exhaustive
enumeration of a finite fixture, (b) at least one planted hostile whose mutation is asserted applied
and which must be caught, and (c) a no-alarm control.  Items whose honest status is PARENT_OWNED /
PARENT_SUFFICIENT, an exact impossibility or a conjecture report the falsifier they ran and the
smallest holding / failing fixture.  The objects are re-implemented here (two-state evidence chains
and test martingales, an antichain warrant lattice with nogoods and authority bits, a routed
self-prediction loop, a paired-lifetime comparison with an ablation arm); nothing is imported from
``ocm``.  Every count is an integer; every probability an exact ``Fraction``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from math import comb


class CannotCheck(RuntimeError):
    pass


def F(a, b=1):
    return Fraction(a, b)


def subsets(universe, min_size=0):
    universe = tuple(universe)
    for k in range(min_size, len(universe) + 1):
        for combo in itertools.combinations(universe, k):
            yield frozenset(combo)


def binom_tail(n, k, p):
    """P(Bin(n, p) >= k), exact."""
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


# =============================================================================================
# I1 · FDX-08 · stochastic warrant dynamics
# =============================================================================================

T1 = 6                                   # ledger horizon (steps observed)
GRID = (F(1, 4), F(1, 2), F(3, 4))
MODELS = {f"M(a={a},b={b})": (a, b) for a in GRID for b in GRID}     # two-state chains: P(L->D)=a, P(D->L)=b; x0 = LIVE
IID_MEMBERS = tuple(m for m, (a, b) in MODELS.items() if a + b == 1)   # the i.i.d. subclass (next state independent of the current one)


def paths(T=T1):
    return list(itertools.product((1, 0), repeat=T))        # 1 = LIVE, 0 = DEAD


def path_probability(model, path):
    a, b = MODELS[model]
    prob, prev = F(1), 1
    for x in path:
        prob *= (1 - a if x == 1 else a) if prev == 1 else (b if x == 1 else 1 - b)
        prev = x
    return prob


def marginal_live(model, t):
    """P_M(x_t = LIVE) by the Chapman–Kolmogorov recursion from x0 = LIVE."""
    a, b = MODELS[model]
    p = F(1)
    for _ in range(t):
        p = p * (1 - a) + (1 - p) * b
    return p


def flips(path):
    prev, n = 1, 0
    for x in path:
        n += int(x != prev)
        prev = x
    return n


def revocations(path):
    prev, n = 1, 0
    for x in path:
        n += int(prev == 1 and x == 0)
        prev = x
    return n


def predictive(model, path):
    """P_M(x_{T+1} = LIVE | ledger path) — a function of (path, M), never of the path alone."""
    a, b = MODELS[model]
    return 1 - a if path[-1] == 1 else b


def receipt(path, model=None):
    """What a receipt may state: the ledger liveness now (exact), and a predictive probability only as a
    claim CONDITIONAL on a registered generating model whose id enters the receipt as a revocable
    assumption.  With no model registered the receipt states the ledger fact and nothing stochastic."""
    now = "LIVE" if path[-1] == 1 else "DEAD"
    if model is None:
        return (now, "NO_MODEL_REGISTERED", None)
    return (now, "CONDITIONAL_ON_MODEL:" + model, predictive(model, path))


def mutant_frequency_as_warrant(path, threshold=F(2, 3)):
    """Planted: the empirical LIVE frequency over the ledger read as the atom's warrant (now and next)."""
    return F(sum(path), len(path)) >= threshold


def mutant_rate_as_probability(path):
    """Planted: the empirical rate reported as 'the probability the atom is LIVE next' with no model."""
    return F(sum(path), len(path))


def posterior(models, path, prior=None):
    w = {m: (prior[m] if prior else F(1, len(models))) * path_probability(m, path) for m in models}
    z = sum(w.values())
    return {m: v / z for m, v in w.items()}


def marginal_likelihood_without(model, path, j):
    """Honest revocation of the observation at step j (0-based): marginalise x_j."""
    return sum(path_probability(model, path[:j] + (x,) + path[j + 1:]) for x in (0, 1))


def mutant_divide_out(model, path, j):
    """Planted Bayesian 'un-update': divide the likelihood by the revoked step's transition factor."""
    a, b = MODELS[model]
    prev = 1 if j == 0 else path[j - 1]
    x = path[j]
    factor = (1 - a if x == 1 else a) if prev == 1 else (b if x == 1 else 1 - b)
    return path_probability(model, path) / factor


# sequential monitoring of a registered operator guarantee ("success probability >= 3/4")
T2, P_NULL, P_ALT, ALPHA = 12, F(3, 4), F(1, 2), F(1, 20)


def interval_liveness(lower, upper, revoked=frozenset()):
    """KS-T21 three-valued liveness of a warrant interval ⟦lower, upper⟧ (antichains of evidence sets)."""
    if any(not (w & revoked) for w in lower):
        return "LIVE"
    if not any(not (w & revoked) for w in upper):
        return "DEAD"
    return "UNKNOWN"


def mutant_evalue_promotes_output(e_t):
    """Planted: a low e-value (evidence for the guarantee) read as exact truth of an individual output."""
    return "LIVE" if e_t < 1 else "UNKNOWN"


def e_process(outcomes):
    """Likelihood-ratio test martingale (alternative P_ALT against the guaranteed P_NULL): a nonnegative
    martingale with E_null = 1 at every step (Wald 1945; Ville 1939)."""
    e, out = F(1), []
    for x in outcomes:
        e *= (P_ALT if x == 1 else 1 - P_ALT) / (P_NULL if x == 1 else 1 - P_NULL)
        out.append(e)
    return out


def anytime_revoke(outcomes):
    return any(e >= 1 / ALPHA for e in e_process(outcomes))


def mutant_stepwise_fixed_level_revoke(outcomes):
    """Planted: at every step t re-run a fixed-level exact binomial test of the guarantee (revoke when the
    failure count is in the level-ALPHA rejection region for that t) — no anytime validity."""
    fails = 0
    for t, x in enumerate(outcomes, start=1):
        fails += int(x == 0)
        if binom_tail(t, fails, 1 - P_NULL) <= ALPHA:
            return True
    return False


def bernoulli_prob(outcomes, p):
    prob = F(1)
    for x in outcomes:
        prob *= p if x == 1 else 1 - p
    return prob


def check_i1_stochastic_warrant():
    P = paths()
    counts = {"horizon": T1, "paths": len(P), "models": len(MODELS), "iid_members": len(IID_MEMBERS)}
    assert len(P) == 2 ** T1 and len(IID_MEMBERS) == 3
    # (i) time-indexed claims: the ledger liveness at t is exact; the stochastic object is the law of paths under
    #     a registered model; path enumeration agrees with the recursion for every (M, t)
    agree = 0
    for m in MODELS:
        assert sum(path_probability(m, p) for p in P) == 1
        for t in range(1, T1 + 1):
            assert sum(path_probability(m, p) for p in P if p[t - 1] == 1) == marginal_live(m, t)
            agree += 1
    counts["marginal_recursion_agrees"] = agree
    # (ii) reopening rates: expected flips are exact under a registered model; under an adversary with a declared
    #      envelope rho (at most rho revocations) the flip count is at most min(2 rho, T); with no envelope and no
    #      model the only bound is T itself — every smaller claimed bound has an admissible counter-path
    counts["expected_flips_by_model"] = {m: str(sum(path_probability(m, p) * flips(p) for p in P)) for m in MODELS}
    by_budget = {}
    for rho in range(T1 + 1):
        admissible = [p for p in P if revocations(p) <= rho]
        mx = max(flips(p) for p in admissible)
        assert mx == min(2 * rho, T1)
        by_budget[str(rho)] = mx
    counts["adversary_max_flips_by_envelope"] = by_budget
    counts["unbudgeted_max_flips"] = max(flips(p) for p in P)
    assert counts["unbudgeted_max_flips"] == T1
    witnesses = 0
    for claimed in range(T1):
        assert any(flips(p) > claimed for p in P)
        witnesses += 1
    counts["impossibility_no_rate_bound_without_model_or_envelope_witnesses"] = witnesses
    # (iii) receipts: ledger fact exact; predictive probability only CONDITIONAL_ON_MODEL; none without a model
    for p in P:
        r = receipt(p)
        assert r[1] == "NO_MODEL_REGISTERED" and r[2] is None and r[0] == ("LIVE" if p[-1] else "DEAD")
        for m in MODELS:
            r2 = receipt(p, m)
            assert r2[1].startswith("CONDITIONAL_ON_MODEL:") and 0 < r2[2] < 1
    counts["receipts_typed"] = len(P) * (len(MODELS) + 1)
    # (iv) hostile: frequency as warrant — wrong about the present on every path whose ledger ends DEAD with a high
    #      frequency; wrong about the future with positive probability under every registered model
    wrong_now = [p for p in P if mutant_frequency_as_warrant(p) and p[-1] == 0]
    counts["mutant_frequency_as_warrant_wrong_now_paths"] = len(wrong_now)
    assert wrong_now and all(sum(p) >= 4 for p in wrong_now)
    wrong_next = {}
    for m in MODELS:
        pr = sum(path_probability(m, p) * (1 - predictive(m, p)) for p in P if mutant_frequency_as_warrant(p))
        assert pr > 0
        wrong_next[m] = str(pr)
    counts["mutant_frequency_as_warrant_wrong_next_prob_by_model"] = wrong_next
    counts["honest_now_reads_ledger"] = sum(1 for p in P if receipt(p)[0] == ("LIVE" if p[-1] else "DEAD"))
    # (v) hostile: the empirical rate as a probability without a model — the predictive probability is not a
    #     function of the path: every registered model has positive likelihood on every path and they disagree
    sizes, freq_matches = {}, 0
    max_lr = F(0)
    for p in P:
        S = {predictive(m, p) for m in MODELS}
        assert all(path_probability(m, p) > 0 for m in MODELS)
        sizes[len(S)] = sizes.get(len(S), 0) + 1
        if mutant_rate_as_probability(p) in S:
            freq_matches += 1
        probs = [path_probability(m, p) for m in MODELS]
        max_lr = max(max_lr, max(probs) / min(probs))
    counts["predictive_set_sizes"] = {str(k): v for k, v in sorted(sizes.items())}
    assert set(sizes) == {3}
    counts["predictive_spread_every_path"] = str(F(1, 2))
    assert all(max(predictive(m, p) for m in MODELS) - min(predictive(m, p) for m in MODELS) == F(1, 2) for p in P)
    counts["mutant_rate_equals_some_registered_prediction_paths"] = freq_matches
    counts["mutant_rate_is_no_registered_prediction_paths"] = len(P) - freq_matches
    counts["max_likelihood_ratio_between_models_at_T"] = str(max_lr)
    assert max_lr < 1000       # finite data weighs models; it never rules one out (all likelihoods positive)
    # (vi) Bayesian updating with revocation: the honest posterior after revoking observation j marginalises x_j;
    #      dividing out the transition factor is exact on the i.i.d. subclass and at the last step only
    differ = same_last = iid_exact = interior_differ = 0
    pairs = 0
    for p in P:
        for j in range(T1):
            pairs += 1
            honest = {m: marginal_likelihood_without(m, p, j) for m in MODELS}
            mut = {m: mutant_divide_out(m, p, j) for m in MODELS}
            zh, zm = sum(honest.values()), sum(mut.values())
            post_h = {m: honest[m] / zh for m in MODELS}
            post_m = {m: mut[m] / zm for m in MODELS}
            if post_h != post_m:
                differ += 1
                if j < T1 - 1:
                    interior_differ += 1
            if j == T1 - 1:
                assert post_h == post_m
                same_last += 1
            for m in IID_MEMBERS:
                assert honest[m] == mut[m]
                iid_exact += 1
    counts["revocation_pairs"] = pairs
    counts["mutant_divide_out_posterior_differs"] = differ
    counts["mutant_divide_out_interior_step_differs"] = interior_differ
    counts["divide_out_exact_at_last_step"] = same_last
    counts["divide_out_exact_on_iid_subclass_checks"] = iid_exact
    assert differ > 0 and differ == interior_differ and same_last == len(P)
    # (vii) sequential monitoring of a registered guarantee: the e-process is a martingale under the guarantee and
    #       revoking when it reaches 1/ALPHA is anytime-valid (Ville); the fixed-level per-step test is not
    outcomes = list(itertools.product((1, 0), repeat=T2))
    martingale_checks = 0
    for t in range(1, T2 + 1):
        assert sum(bernoulli_prob(o, P_NULL) * e_process(o)[t - 1] for o in outcomes) == 1
        martingale_checks += 1
    counts["martingale_checks"] = martingale_checks
    ville = sum(bernoulli_prob(o, P_NULL) for o in outcomes if anytime_revoke(o))
    stepwise = sum(bernoulli_prob(o, P_NULL) for o in outcomes if mutant_stepwise_fixed_level_revoke(o))
    assert ville <= ALPHA < stepwise
    counts["guarantee_horizon"] = T2
    counts["anytime_false_revocation_prob"] = str(ville)
    counts["mutant_stepwise_false_revocation_prob"] = str(stepwise)
    counts["alpha"] = str(ALPHA)
    counts["anytime_power_under_alternative"] = str(sum(bernoulli_prob(o, P_ALT) for o in outcomes if anytime_revoke(o)))
    counts["stepwise_power_under_alternative"] = str(sum(bernoulli_prob(o, P_ALT) for o in outcomes if mutant_stepwise_fixed_level_revoke(o)))
    # the guarantee is a scoped assumption id g: an individual output resting on it alone is ⟦0, {g}⟧ and stays
    # UNKNOWN whatever the e-value says (D3 / KS-T21); the planted promotion mints LIVE on every path with e_T < 1
    output_interval = ((), (frozenset({"g"}),))
    honest_unknown = sum(1 for o in outcomes if interval_liveness(*output_interval) == "UNKNOWN")
    promoted = sum(1 for o in outcomes if mutant_evalue_promotes_output(e_process(o)[-1]) == "LIVE")
    assert honest_unknown == len(outcomes) and promoted > 0
    counts["individual_output_unknown_under_every_evalue"] = honest_unknown
    counts["mutant_evalue_promotes_output_caught"] = promoted
    # no-alarm: a registered model gives every marginal, every predictive and every reopening rate exactly
    counts["no_alarm_registered_model_gives_exact_receipts"] = len(MODELS)
    counts["status"] = ("PROVED (finite): ledger liveness exact; stochastic claims only CONDITIONAL_ON_MODEL; reopening rate bounded iff a model or envelope is registered "
                        "(EXACTLY_BOUNDED_IMPOSSIBILITY otherwise); frequency-as-warrant and rate-as-probability caught; Bayesian revocation = marginalisation; "
                        "anytime-valid guarantee revocation (Ville) vs fixed-level re-testing; PARENT_OWNED (Markov chains, test martingales / SPRT, Bayes)")
    return counts


# =============================================================================================
# I2 · FDX-11 · epistemic bifurcation / obstruction
# =============================================================================================

EVID = ("e1", "e2", "e3", "e4")
AUTH_BITS = ("s1", "s2")
NOGOOD_CANDIDATES = (frozenset({"e1", "e2"}), frozenset({"e2", "e3"}), frozenset({"e1", "e3"}))
# atoms: alternatives (antichain) and the authority bit each requires for commitment
ATOMS2 = {
    "x1": ((frozenset({"e1"}),), "s1"),
    "x2": ((frozenset({"e1"}), frozenset({"e2"})), "s1"),
    "x3": ((frozenset({"e1", "e2"}), frozenset({"e3"})), "s1"),
    "x4": ((frozenset({"e2", "e3"}),), "s1"),
    "x5": ((frozenset({"e4"}),), "s2"),
    "c": ((frozenset({"e1", "e2", "e3"}),), "s1"),          # x1 ⊗ x4
}
CONFLICT = ("x3", "x4")                                    # a registered symmetric conflict (argumentation attack)


def states2():
    for R in subsets(EVID):
        for N in subsets(range(len(NOGOOD_CANDIDATES))):
            for A in subsets(AUTH_BITS):
                yield (R, N, A)


def unfiltered(alts, N):
    ngs = [NOGOOD_CANDIDATES[i] for i in N]
    return tuple(w for w in alts if not any(n <= w for n in ngs))


def live_alts(alts, R, N):
    return tuple(w for w in unfiltered(alts, N) if not (w & R))


def committed(atom, s):
    R, N, A = s
    alts, bit = ATOMS2[atom]
    return bool(live_alts(alts, R, N)) and bit in A


def commitment_set(s):
    return frozenset(x for x in ATOMS2 if committed(x, s))


def changes(s):
    R, N, A = s
    for e in EVID:
        yield ("revoke" if e not in R else "reinstate", e), (R ^ {e}, N, A)
    for i in range(len(NOGOOD_CANDIDATES)):
        if i not in N:
            yield ("add_nogood", i), (R, N | {i}, A)
    for b in AUTH_BITS:
        yield ("grant" if b not in A else "withdraw", b), (R, N, A ^ {b})


def predicted_flips(s, change):
    """Exact characterisation of the boundary: which atoms flip under one registered change."""
    R, N, A = s
    kind, arg = change
    out = set()
    for x, (alts, bit) in ATOMS2.items():
        la = live_alts(alts, R, N)
        if kind == "revoke":
            if bit in A and la and all(arg in w for w in la):                      # arg is a cut of the live alternatives
                out.add(x)
        elif kind == "reinstate":
            if bit in A and not la and any((w & R) == {arg} for w in unfiltered(alts, N)):   # arg completes an alternative
                out.add(x)
        elif kind == "add_nogood":
            n = NOGOOD_CANDIDATES[arg]
            if bit in A and la and all(n <= w for w in la):                         # the nogood covers every live alternative
                out.add(x)
        elif kind == "withdraw":
            if bit == arg and la:
                out.add(x)
        elif kind == "grant":
            if bit == arg and la:
                out.add(x)
    return frozenset(out)


def mutant_flip_is_mechanism_failure(delta, k=2):
    """Planted: a commitment jump of size >= k under one change is read as a mechanism defect."""
    return len(delta) >= k


def graded_score(atom, s):
    R, N, A = s
    alts, _ = ATOMS2[atom]
    uf = unfiltered(alts, N)
    return F(len(live_alts(alts, R, N)), len(uf)) if uf else F(0)


def mutant_graded_continuity(atom, s, s2, tol=F(1, 2)):
    """Planted: 'stable' whenever the graded support score moves by at most tol."""
    return abs(graded_score(atom, s) - graded_score(atom, s2)) <= tol


def grounded_extension(args, attacks):
    """Dung 1995 grounded extension: least fixed point of the characteristic function."""
    ext = set()
    while True:
        defended = {a for a in args if all(any((c, b) in attacks for c in ext) for b in args if (b, a) in attacks)}
        if defended == ext:
            return frozenset(ext)
        ext = defended


def stable_extensions(args, attacks):
    out = []
    for S in subsets(args):
        if any((a, b) in attacks for a in S for b in S):
            continue
        if all(any((a, b) in attacks for a in S) for b in args if b not in S):
            out.append(S)
    return out


def mutant_pick_a_stable_extension(args, attacks):
    """Planted: commit the lexicographically first stable extension (a credulous choice, not a function of evidence)."""
    return sorted(stable_extensions(args, attacks), key=lambda S: sorted(S))[0]


# obstruction fixture (batch-5 E3 shape): features {1, a, b}, feature warrants fa <- e1, fb <- e2; targets as 4-bit tables
def span(features):
    out = {0}
    for f in features:
        out |= {v ^ f for v in out}
    return out


CONST1, FA, FB, FAB = 0b1111, 0b1100, 0b1010, 0b1000         # tables over inputs (a,b) in order 11,10,01,00 → bit3..bit0
TARGETS = {"a": FA, "xor": FA ^ FB, "and": FAB}


def live_features(R):
    return [CONST1] + ([FA] if "e1" not in R else []) + ([FB] if "e2" not in R else [])


def fails(target, R, extra=()):
    return TARGETS[target] not in span(live_features(R) + list(extra))


def certificate(target, R):
    """E3 certificate: OBSTRUCTION iff the failure is invariant under every evidence state of the registered
    representation (no reinstatement helps) with the parity witness; REINSTATE_FIRST iff some feature is dead
    and a reinstatement solves it; SUCCESS otherwise."""
    if not fails(target, R):
        return "SUCCESS"
    if all(fails(target, R2) for R2 in subsets(("e1", "e2"))):
        return "OBSTRUCTION"
    return "REINSTATE_FIRST"


def mutant_certify_on_boundary(target, R):
    """Planted: OBSTRUCTION whenever the target fails at the current evidence state."""
    return "OBSTRUCTION" if fails(target, R) else "SUCCESS"


def check_i2_bifurcation():
    S = list(states2())
    counts = {"states": len(S), "atoms": len(ATOMS2)}
    assert len(S) == 16 * 8 * 4
    pairs = predicted_ok = total_flips = 0
    hist = {}
    boundary_pairs = 0
    kind_max = {}
    explained = 0
    mutant_alarms = 0
    masked = 0
    monotone_checks = 0
    for s in S:
        C = commitment_set(s)
        for change, s2 in changes(s):
            pairs += 1
            delta = C ^ commitment_set(s2)
            assert delta == predicted_flips(s, change), (s, change, delta, predicted_flips(s, change))
            predicted_ok += 1
            total_flips += len(delta)
            hist[len(delta)] = hist.get(len(delta), 0) + 1
            kind_max[change[0]] = max(kind_max.get(change[0], 0), len(delta))
            explained += len(delta)                    # every flipped atom is named by the characterisation
            if mutant_flip_is_mechanism_failure(delta):
                mutant_alarms += 1
            for x in delta:
                if mutant_graded_continuity(x, s, s2):
                    masked += 1
            # monotonicity of the commitment indicator in the evidence coordinate (a monotone Boolean function)
            if change[0] == "reinstate":
                assert commitment_set(s) <= commitment_set(s2)
                monotone_checks += 1
        if any(predicted_flips(s, ch) for ch, _ in changes(s)):
            boundary_pairs += 1
    counts["state_change_pairs"] = pairs
    counts["boundary_characterisation_exact"] = predicted_ok
    counts["total_flips"] = total_flips
    counts["flips_explained_by_cut_completion_nogood_authority"] = explained
    counts["jump_size_histogram"] = {str(k): v for k, v in sorted(hist.items())}
    counts["max_jump_by_change_kind"] = kind_max
    counts["states_on_a_boundary"] = boundary_pairs
    counts["monotone_in_evidence_checks"] = monotone_checks
    counts["mutant_flip_is_mechanism_failure_alarms"] = mutant_alarms
    assert mutant_alarms > 0 and explained == total_flips
    counts["mutant_graded_continuity_masked_flips"] = masked
    assert masked > 0
    # sensitivity = number of single evidence flips changing the atom's commitment; zero exactly when no live
    # alternative id is a cut and no dead alternative is one id short (no-alarm: x2 at R = ∅ has sensitivity 0)
    s0 = (frozenset(), frozenset(), frozenset(AUTH_BITS))
    sens = {x: sum(1 for ch, s2 in changes(s0) if ch[0] in ("revoke", "reinstate") and (x in commitment_set(s0)) != (x in commitment_set(s2))) for x in ATOMS2}
    counts["sensitivity_at_full_evidence"] = sens
    assert sens["x2"] == 0 and sens["x1"] == 1 and sens["c"] == 3
    # authority: withdrawing one bit flips every committed atom that requires it (the meet), a jump of size up to 5
    counts["authority_withdraw_s1_jump_at_full_state"] = len(predicted_flips(s0, ("withdraw", "s1")))
    assert counts["authority_withdraw_s1_jump_at_full_state"] == 5
    # argumentation reading: LIVE atoms are arguments, the registered conflict is a symmetric attack; the C7 policy
    # (UNKNOWN while both live) is the grounded extension; a credulous stable choice is not a function of evidence
    grounded_eq = 0
    two_stable = 0
    flip_by_design = 0
    for s in S:
        args = frozenset(x for x in ATOMS2 if committed(x, s))
        attacks = {(a, b) for a in CONFLICT for b in CONFLICT if a != b and a in args and b in args}
        g = grounded_extension(args, attacks)
        policy = args - (set(CONFLICT) if set(CONFLICT) <= args else set())
        assert g == policy
        grounded_eq += 1
        st = stable_extensions(args, attacks)
        assert all(g <= e for e in st)
        if len(st) == 2:
            two_stable += 1
            pick = mutant_pick_a_stable_extension(args, attacks)
            assert pick != g and len(pick - g) == 1
        if set(CONFLICT) <= args:
            R, N, A = s
            for e in EVID:
                if e not in R:
                    s2 = (R | {e}, N, A)
                    args2 = frozenset(x for x in ATOMS2 if committed(x, s2))
                    if len(set(CONFLICT) & args2) == 1:
                        flip_by_design += 1
                        break
    counts["grounded_extension_equals_c7_policy"] = grounded_eq
    counts["states_with_two_stable_extensions"] = two_stable
    counts["mutant_pick_a_stable_extension_caught"] = two_stable
    counts["conflict_resolved_by_one_revocation_states"] = flip_by_design
    assert two_stable > 0 and flip_by_design > 0
    # obstruction: an obstruction is a failure on no evidence boundary (invariant over every evidence state of the
    # registered representation) and on a representation boundary (the Jump to {1, a, b, ab} reaches it)
    cert_table = {}
    invariant_iff = 0
    mutant_boundary_caught = 0
    for target in TARGETS:
        for R in subsets(("e1", "e2")):
            c = certificate(target, R)
            cert_table[f"{target}@dead={sorted(R)}"] = c
            invariant = all(fails(target, R2) for R2 in subsets(("e1", "e2")))
            assert (c == "OBSTRUCTION") == (fails(target, R) and invariant)
            invariant_iff += 1
            if mutant_certify_on_boundary(target, R) == "OBSTRUCTION" and c != "OBSTRUCTION":
                mutant_boundary_caught += 1
                assert any(not fails(target, R2) for R2 in subsets(("e1", "e2")))    # a reinstatement solves it
    counts["certificate_table"] = cert_table
    counts["obstruction_iff_evidence_invariant_failure"] = invariant_iff
    counts["mutant_certify_on_boundary_caught"] = mutant_boundary_caught
    assert mutant_boundary_caught > 0
    assert all(certificate("and", R) == "OBSTRUCTION" for R in subsets(("e1", "e2")))
    assert certificate("xor", frozenset()) == "SUCCESS" and certificate("xor", frozenset({"e1"})) == "REINSTATE_FIRST"
    assert not fails("and", frozenset(), extra=(FAB,))            # the R-transition (Jump) moves the obstruction
    counts["obstruction_moved_only_by_representation_change"] = 1
    counts["obstruction_evidence_neighbours_flipping"] = sum(1 for R in subsets(("e1", "e2")) if not fails("and", R))
    assert counts["obstruction_evidence_neighbours_flipping"] == 0
    counts["status"] = ("PROVED (finite): boundary = {revoked id is a cut of the live alternatives} ∪ {reinstated id completes an alternative} ∪ "
                        "{new nogood covers every live alternative} ∪ {authority bit of the meet}; every flip explained, none a mechanism failure; "
                        "commitment set = grounded extension; obstruction certificate ⇔ evidence-invariant failure (no E-boundary), moved only by R; "
                        "PARENT_OWNED (monotone Boolean sensitivity, ATMS label change, Dung 1995, batch-5 E3 / batch-7 G1)")
    return counts


# =============================================================================================
# I3 · FDX-13 · self-model calibration and reflexive dependence
# =============================================================================================

RATES = tuple(F(k, 4) for k in range(5))
THETAS = (F(1, 4), F(1, 2), F(3, 4))
PRED_GRID = tuple(F(k, 8) for k in range(9))


def realised_under_adoption(pred, rA, rB, theta):
    """Router adopts the self-prediction: at or above theta every task (4 easy + 4 hard) goes to the operator,
    below theta only the easy tasks do.  The realised operator success rate depends on the prediction."""
    return (rA + rB) / 2 if pred >= theta else rA


def counterfactual_rate(rA, rB):
    """The shadow arm: every task runs on the operator, nothing reads the prediction."""
    return (rA + rB) / 2


def fixed_points(rA, rB, theta):
    return tuple(p for p in PRED_GRID if realised_under_adoption(p, rA, rB, theta) == p)


def closed_form_fixed_points(rA, rB, theta):
    m = (rA + rB) / 2
    out = set()
    if rA < theta:
        out.add(rA)
    if m >= theta:
        out.add(m)
    return tuple(sorted(out))


def orbit(pred, rA, rB, theta, steps=6):
    seq = [pred]
    for _ in range(steps):
        seq.append(realised_under_adoption(seq[-1], rA, rB, theta))
    return seq


def mutant_score_on_caused_outcomes(pred, rA, rB, theta, tol=F(1, 8)):
    """Planted: the self-prediction is scored on the outcomes its own adoption produced."""
    return abs(pred - realised_under_adoption(pred, rA, rB, theta)) <= tol


def counterfactual_calibrated(pred, rA, rB, tol=F(1, 8)):
    return abs(pred - counterfactual_rate(rA, rB)) <= tol


def mutant_prediction_as_warrant(pred, threshold=F(7, 8)):
    """Planted: a confident self-prediction read as exact truth of the operator's next output."""
    return "LIVE" if pred >= threshold else "UNKNOWN"


def mutant_reuse_heldout_selects_best(table):
    """Planted (adaptive data analysis): k candidate self-predictors scored on one shared held-out set; the best
    held-out score is reported as the selected predictor's calibration."""
    scores = [sum(row) for row in table]
    return max(scores)


def check_i3_self_model_calibration():
    fixtures = [(rA, rB, th) for rA in RATES for rB in RATES for th in THETAS]
    counts = {"fixtures": len(fixtures), "prediction_grid": len(PRED_GRID)}
    fp_hist = {}
    closed_ok = 0
    converge = period2 = 0
    no_stable_but_observational_defined = 0
    unregistered_loop_wrong = 0
    for rA, rB, th in fixtures:
        fps = fixed_points(rA, rB, th)
        assert fps == closed_form_fixed_points(rA, rB, th)
        closed_ok += 1
        fp_hist[len(fps)] = fp_hist.get(len(fps), 0) + 1
        for p0 in PRED_GRID:
            seq = orbit(p0, rA, rB, th)
            if seq[-1] == seq[-2]:
                assert seq[-1] in fps
                converge += 1
            else:
                assert not fps and seq[-1] == seq[-3] and seq[-1] != seq[-2]
                period2 += 1
        if not fps:
            no_stable_but_observational_defined += 1          # the shadow rate is a fixed number regardless of the loop
        m = counterfactual_rate(rA, rB)
        if realised_under_adoption(m, rA, rB, th) != m:
            unregistered_loop_wrong += 1                      # self-model that ignores the loop predicts m and is wrong under adoption
    counts["closed_form_fixed_points_agree"] = closed_ok
    counts["fixed_point_count_histogram"] = {str(k): v for k, v in sorted(fp_hist.items())}
    counts["orbits_converge"] = converge
    counts["orbits_period_two"] = period2
    counts["fixtures_without_stable_self_prediction"] = no_stable_but_observational_defined
    counts["unregistered_loop_prediction_wrong_under_adoption"] = unregistered_loop_wrong
    assert fp_hist.get(0, 0) > 0 and fp_hist.get(2, 0) > 0 and period2 > 0
    # bistability witness: two self-confirming predictions, chosen by the starting point
    two = next((f for f in fixtures if len(fixed_points(*f)) == 2), None)
    assert two is not None
    counts["bistable_witness"] = {"rA": str(two[0]), "rB": str(two[1]), "theta": str(two[2]), "fixed_points": [str(p) for p in fixed_points(*two)]}
    # hostile: scored on caused outcomes — 'calibrated' under adoption while miscalibrated against the counterfactual
    caused_ok_cf_bad = perf_cases = 0
    for rA, rB, th in fixtures:
        for p in PRED_GRID:
            perf_cases += 1
            if mutant_score_on_caused_outcomes(p, rA, rB, th) and not counterfactual_calibrated(p, rA, rB):
                caused_ok_cf_bad += 1
    counts["prediction_cases"] = perf_cases
    counts["mutant_score_on_caused_outcomes_caught"] = caused_ok_cf_bad
    assert caused_ok_cf_bad > 0
    # E4 tightened: held-out tasks disjoint from dev tasks but routed by the prediction under test are performative;
    # the honest adopter scores the prediction on the shadow (nothing reads it).  Self-fulfilling set per fixture:
    self_fulfilling = sum(1 for rA, rB, th in fixtures for p in PRED_GRID if mutant_score_on_caused_outcomes(p, rA, rB, th))
    cf_calibrated = sum(1 for rA, rB, th in fixtures for p in PRED_GRID if counterfactual_calibrated(p, rA, rB))
    cf_ok_perf_bad = sum(1 for rA, rB, th in fixtures for p in PRED_GRID
                         if counterfactual_calibrated(p, rA, rB) and not mutant_score_on_caused_outcomes(p, rA, rB, th))
    counts["self_fulfilling_prediction_cases"] = self_fulfilling
    counts["counterfactual_calibrated_cases"] = cf_calibrated
    counts["counterfactual_calibrated_but_performatively_wrong"] = cf_ok_perf_bad
    assert caused_ok_cf_bad > 0 and cf_ok_perf_bad > 0        # the two calibration receipts disagree in both directions
    # adaptive data analysis: k = 3 candidates, one shared held-out of n = 3 fair coins each (true rate 1/2 for all)
    n, k = 3, 3
    tables = list(itertools.product(itertools.product((0, 1), repeat=n), repeat=k))
    assert len(tables) == 2 ** (n * k)
    reported = sum(F(mutant_reuse_heldout_selects_best(t), n) for t in tables) / len(tables)
    fresh = F(1, 2)                                          # a fresh held-out for the selected predictor: E = true rate
    counts["adaptive_reuse_tables"] = len(tables)
    counts["mutant_reuse_heldout_expected_reported_score"] = str(reported)
    counts["fresh_heldout_expected_score"] = str(fresh)
    counts["adaptive_optimism_bias"] = str(reported - fresh)
    assert reported > fresh
    # self-authority: a self-prediction may steer routing (a J0 feedback move) but is never a warrant — the output
    # resting on the prediction record r alone is ⟦0, {r}⟧, UNKNOWN at every predicted rate (E1 / KS-T21)
    counts["prediction_record_authority"] = {"self_model": 1, "world_truth": 0, "commit": 0}
    assert all(interval_liveness((), (frozenset({"r"}),)) == "UNKNOWN" for _ in PRED_GRID)
    counts["mutant_prediction_as_warrant_caught"] = sum(1 for p in PRED_GRID if mutant_prediction_as_warrant(p) == "LIVE")
    assert counts["mutant_prediction_as_warrant_caught"] > 0
    # no-alarm: with the loop registered (router policy and rates known) the stable prediction is computed exactly
    counts["no_alarm_registered_loop_fixed_point_computable"] = sum(1 for f in fixtures if fixed_points(*f))
    counts["status"] = ("PROVED (finite): performative fixed points = {rA if rA < θ} ∪ {(rA+rB)/2 if ≥ θ} (0/1/2), repeated retraining converges "
                        "iff a fixed point exists in the reached regime else period 2; scoring on caused outcomes is self-fulfilling; shadow = counterfactual arm "
                        "(E4 tightened); shared held-out reuse is optimistic; PARENT_OWNED (performative prediction, adaptive data analysis, E1/E4/E5)")
    return counts


# =============================================================================================
# I4 · FDX-15 · parent-product equivalence / residual attribution
# =============================================================================================

TASKS = tuple(f"F{i}" for i in range(1, 5)) + tuple(f"V{i}" for i in range(1, 5)) + tuple(f"O{i}" for i in range(1, 5))
WORLD_TRUE_OOS = {"O1", "O2"}
M_LIFETIMES = 8


def arm_outcomes(channels, delta, variation, grading="licence"):
    """An arm as a function of its information channels and the declared mechanism difference Δ (typed
    revocation machinery).  F: factual in-scope (MANIFEST answers; MANIFEST_PARTIAL answers F1, F2 only).
    V: a lesson taught then revoked — Δ honours the revocation exactly; without Δ the coarse per-domain flag
    coincides with the right answer only where the lifetime's stream variation makes it (bit v_i).
    O: out of scope — licensed UNKNOWN; an arm with the unbound channel U answers the world instead."""
    out = {}
    for t in TASKS:
        if t[0] == "F":
            out[t] = int("MANIFEST" in channels or ("MANIFEST_PARTIAL" in channels and t in ("F1", "F2")))
        elif t[0] == "V":
            i = int(t[1]) - 1
            out[t] = int("LESSONS" in channels and (delta or variation[i] == 1))
        else:
            answers_world = "U" in channels
            if grading == "licence":
                out[t] = int(not answers_world)
            else:
                out[t] = int(answers_world)              # truth grading rewards the unbound channel (G7)
    return out


def family_score(outcomes, family):
    ts = [t for t in TASKS if t[0] == family]
    return F(sum(outcomes[t] for t in ts), len(ts))


def sign_test_one_sided(diffs, alpha=F(1, 20)):
    nz = [d for d in diffs if d != 0]
    pos = sum(1 for d in nz if d > 0)
    collapsed = len(set(diffs)) == 1 and len(diffs) > 1
    if not nz:
        return {"n": 0, "positive": 0, "p": F(1), "collapsed": collapsed, "verdict": "TIES_ONLY"}
    p = binom_tail(len(nz), pos, F(1, 2)) if pos > 0 else F(1)
    return {"n": len(nz), "positive": pos, "p": p, "collapsed": collapsed, "verdict": "OCM_RESIDUAL" if p <= alpha else "INCONCLUSIVE"}


def decide_discordant(n10, n01, alpha=F(1, 20), delta=F(1, 10)):
    """Batch-4 D1 on one lifetime's discordant pairs (never pooled across lifetimes)."""
    nd = n10 + n01
    if nd == 0:
        return "INCONCLUSIVE"
    if binom_tail(nd, n10, F(1, 2) + delta) <= alpha:
        return "RESIDUAL_SUPPORTED"
    if binom_tail(nd, n01, F(1, 2) + delta) <= alpha:
        return "PARENT_DOMINATES"
    if binom_tail(nd, n10, F(1, 2) - delta) <= alpha and binom_tail(nd, n01, F(1, 2) - delta) <= alpha:
        return "PARENT_SUFFICIENT"
    return "INCONCLUSIVE"


def attribute_residual(test, matched_by_ablation, reference_inside=False, pseudo_replicated=False):
    """The residual theorem's decision: a measured residual is attributable to the declared difference iff the
    decision rejects at registered size on independent units, the reference arm is outside, no pooling, the
    differences are not one coin, and the ablation arm (OCM minus Δ) equals the parent on every matched unit."""
    if reference_inside:
        return "REFUSED_REFERENCE_ARM_IN_DECISION"
    if pseudo_replicated:
        return "REFUSED_PSEUDO_REPLICATION"
    if test["verdict"] != "OCM_RESIDUAL":
        return "INCONCLUSIVE_UNDERPOWERED" if test["verdict"] == "INCONCLUSIVE" else "TIES_ONLY"
    if not matched_by_ablation:
        return "RESIDUAL_CONFOUNDED_BY_UNMATCHED_INFORMATION"      # attribution fails before the evidence is weighed
    if test["collapsed"]:
        return "RESIDUAL_ONE_COIN_FLAGGED"
    return "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE"


def mutant_attribute_any_rejection_to_delta(test):
    """Planted: every rejection is read as the declared difference at work."""
    return "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE" if test["verdict"] == "OCM_RESIDUAL" else "INCONCLUSIVE"


def variations(case):
    if case == "real":
        return [(k & 1, (k >> 1) & 1, (k >> 2) & 1, 0) for k in range(M_LIFETIMES)]        # parent V-score 0..3/4, varies
    if case == "undetectable":
        return [(1, 1, 1, 1) if k < 5 else (1, 1, 1, 0) for k in range(M_LIFETIMES)]           # 5 ties, 3 OCM wins
    if case == "collapsed":
        return [(0, 0, 0, 0)] * M_LIFETIMES                                                   # deterministic design: one coin
    raise CannotCheck(case)


def compare(ocm_channels, parent_channels, case, family="V", grading="licence"):
    vs = variations(case)
    ocm = [arm_outcomes(ocm_channels, True, v, grading) for v in vs]
    par = [arm_outcomes(parent_channels, False, v, grading) for v in vs]
    abl = [arm_outcomes(ocm_channels, False, v, grading) for v in vs]          # OCM minus Δ
    ppd = [arm_outcomes(parent_channels, True, v, grading) for v in vs]        # parent plus Δ
    diffs = [family_score(o, family) - family_score(p, family) for o, p in zip(ocm, par)]
    test = sign_test_one_sided(diffs)
    matched = all(a == p for a, p in zip(abl, par))
    equivalent = all(q == o for q, o in zip(ppd, ocm))
    return {"diffs": diffs, "test": test, "matched_by_ablation": matched, "parent_plus_delta_equals_ocm": equivalent,
            "ablation_mismatched_units": sum(1 for a, p in zip(abl, par) for t in TASKS if a[t] != p[t])}


def check_i4_residual_attribution():
    counts = {"tasks": len(TASKS), "lifetimes": M_LIFETIMES}
    matched_channels = frozenset({"LESSONS", "MANIFEST"})
    # (a) a real residual: matched channels, Δ declared; differences vary; ablation equals the parent unit for unit
    a = compare(matched_channels, matched_channels, "real")
    assert a["test"]["verdict"] == "OCM_RESIDUAL" and not a["test"]["collapsed"] and a["matched_by_ablation"] and a["parent_plus_delta_equals_ocm"]
    counts["real"] = {"diffs": [str(d) for d in a["diffs"]], "p": str(a["test"]["p"]), "verdict": attribute_residual(a["test"], a["matched_by_ablation"]),
                      "ablation_mismatched_units": a["ablation_mismatched_units"]}
    assert counts["real"]["verdict"] == "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE" and a["test"]["p"] == F(1, 256)
    # (b) an artefact of unmatched information: the parent lacks half the manifest; the family F rejects 8/8 although Δ
    #     plays no role there — the ablation arm still beats the parent, so the residual is the channel's
    b = compare(matched_channels, frozenset({"LESSONS", "MANIFEST_PARTIAL"}), "real", family="F")
    assert b["test"]["verdict"] == "OCM_RESIDUAL" and not b["matched_by_ablation"] and b["ablation_mismatched_units"] > 0
    counts["unmatched"] = {"diffs": [str(d) for d in b["diffs"]], "verdict": attribute_residual(b["test"], b["matched_by_ablation"]),
                           "ablation_mismatched_units": b["ablation_mismatched_units"],
                           "mutant_verdict": mutant_attribute_any_rejection_to_delta(b["test"])}
    assert counts["unmatched"]["verdict"] == "RESIDUAL_CONFOUNDED_BY_UNMATCHED_INFORMATION"
    assert counts["unmatched"]["mutant_verdict"] == "RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE"
    counts["mutant_attribute_any_rejection_caught_unmatched"] = 1
    # (c) undetectable at this n: the residual is real on three lifetimes (one item each) and the design cannot reject
    c = compare(matched_channels, matched_channels, "undetectable")
    assert c["test"]["verdict"] == "INCONCLUSIVE" and c["test"]["n"] == 3 and c["test"]["p"] == F(1, 8) and c["matched_by_ablation"]
    counts["undetectable"] = {"diffs": [str(d) for d in c["diffs"]], "p": str(c["test"]["p"]), "verdict": attribute_residual(c["test"], c["matched_by_ablation"])}
    assert counts["undetectable"]["verdict"] == "INCONCLUSIVE_UNDERPOWERED"
    power = {str(p): str(binom_tail(M_LIFETIMES, 7, p)) for p in (F(1, 2), F(6, 10), F(7, 10), F(8, 10), F(9, 10))}
    counts["power_ge_7_of_8_by_win_probability"] = power
    mdp = next(F(k, 100) for k in range(50, 101) if binom_tail(M_LIFETIMES, 7, F(k, 100)) >= F(8, 10))
    counts["minimum_detectable_win_probability_power_0_8"] = str(mdp)
    assert F(85, 100) < mdp <= F(9, 10)
    # within one lifetime the D1 discordant rule with 4 items can never reject either way; PARENT_SUFFICIENT needs
    # n_d >= 76 (batch-4 D1) — the lifetime-level test is the only one with any size at m = 8
    within = {f"{n10}-{n01}": decide_discordant(n10, n01) for n10 in range(5) for n01 in range(5 - n10)}
    assert set(within.values()) == {"INCONCLUSIVE"}
    counts["within_lifetime_d1_on_four_items"] = "INCONCLUSIVE on all 15 tables"
    counts["smallest_n_d_all_ocm_wins_for_residual_supported"] = next(n for n in range(1, 40) if decide_discordant(n, 0) == "RESIDUAL_SUPPORTED")
    counts["smallest_n_d_for_parent_sufficient_at_p_half"] = next(n for n in range(1, 200) if n % 2 == 0 and decide_discordant(n // 2, n // 2) == "PARENT_SUFFICIENT")
    assert counts["smallest_n_d_all_ocm_wins_for_residual_supported"] == 6 and counts["smallest_n_d_for_parent_sufficient_at_p_half"] == 76
    # (d) collapsed one coin: a deterministic family rejects 8/8 with identical differences — flagged, one coin
    d = compare(matched_channels, matched_channels, "collapsed")
    assert d["test"]["verdict"] == "OCM_RESIDUAL" and d["test"]["collapsed"]
    counts["collapsed"] = {"diffs": [str(x) for x in d["diffs"]], "verdict": attribute_residual(d["test"], d["matched_by_ablation"]),
                           "mutant_verdict": mutant_attribute_any_rejection_to_delta(d["test"]), "one_coin_size": str(F(1, 2))}
    assert counts["collapsed"]["verdict"] == "RESIDUAL_ONE_COIN_FLAGGED"
    counts["mutant_attribute_any_rejection_caught_collapsed"] = 1
    # (e) pseudo-replication: three orderings of one lifetime pooled as discordant pairs (F2)
    single = binom_tail(3, 3, F(1, 2))
    pooled = binom_tail(9, 9, F(1, 2))
    assert single == F(1, 8) > F(1, 20) >= pooled
    counts["pseudo_replication"] = {"one_lifetime_3_0_p": str(single), "pooled_x3_9_0_p": str(pooled), "verdict": attribute_residual(c["test"], True, pseudo_replicated=True)}
    assert counts["pseudo_replication"]["verdict"] == "REFUSED_PSEUDO_REPLICATION"
    # (f) the reference arm (unbound channel U) inside the decision: the verdict on O flips with the grader (G7/F8)
    ref_lic = compare(matched_channels, matched_channels | {"U"}, "real", family="O", grading="licence")
    ref_tru = compare(matched_channels, matched_channels | {"U"}, "real", family="O", grading="truth")
    assert all(dd == 1 for dd in ref_lic["diffs"]) and all(dd == -1 for dd in ref_tru["diffs"])
    counts["reference_inside"] = {"licence_grading_diffs": str(ref_lic["diffs"][0]), "truth_grading_diffs": str(ref_tru["diffs"][0]),
                                  "verdict": attribute_residual(ref_lic["test"], ref_lic["matched_by_ablation"], reference_inside=True)}
    assert counts["reference_inside"]["verdict"] == "REFUSED_REFERENCE_ARM_IN_DECISION"
    assert not ref_lic["matched_by_ablation"]                         # U is an unmatched channel: the ablation check also refuses
    # equivalence on the fixture: parent + Δ ≡ OCM and OCM − Δ ≡ parent on every matched case (by construction of the
    # arm as a function of channels and Δ); the general claim is a conjecture with this as its falsifier shape
    eq = 0
    for case in ("real", "undetectable", "collapsed"):
        r = compare(matched_channels, matched_channels, case)
        assert r["parent_plus_delta_equals_ocm"] and r["matched_by_ablation"]
        eq += 1
    counts["parent_plus_delta_equals_ocm_cases"] = eq
    # no-alarm: matched arms without Δ on either side tie everywhere
    tie = compare(matched_channels, matched_channels, "real", family="F")
    assert tie["test"]["verdict"] == "TIES_ONLY" and attribute_residual(tie["test"], tie["matched_by_ablation"]) == "TIES_ONLY"
    counts["no_alarm_matched_family_ties"] = 1
    counts["status"] = ("PROVED (finite attribution theorem): attributable iff registered-size rejection on independent lifetimes ∧ not one coin ∧ no pooling ∧ "
                        "reference outside ∧ OCM−Δ ≡ parent unit for unit; artefact (unmatched channel), one-coin and underpowered cases separated; "
                        "PARENT_SUFFICIENT on the fixture (parent+Δ ≡ OCM by construction); general product equivalence CONJECTURE with the ablation falsifier; "
                        "PARENT_OWNED (matched designs / ablation, exact sign test, D1, F2, F8, G7, G8)")
    return counts


# =============================================================================================
# driver
# =============================================================================================

CHECKS = {
    "I1_FDX08_stochastic_warrant": check_i1_stochastic_warrant,
    "I2_FDX11_bifurcation": check_i2_bifurcation,
    "I3_FDX13_self_model_calibration": check_i3_self_model_calibration,
    "I4_FDX15_residual_attribution": check_i4_residual_attribution,
}

STATUS = {
    "I1_FDX-08": "PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY (no reopening-rate bound and no predictive probability without a registered model or envelope); PARENT_OWNED (Markov chains, Ville / test martingales / SPRT, Bayesian updating); graded semiring not reopened (D3/F6/G6)",
    "I2_FDX-11": "PROVED (finite): exact boundary characterisation (cut / completion / nogood cover / authority meet); commitment set = grounded extension; obstruction ⇔ evidence-invariant failure, moved only by R; PARENT_OWNED (monotone Boolean sensitivity, ATMS, Dung 1995, E3/G1)",
    "I3_FDX-13": "PROVED (finite): performative fixed points and orbits; caused-outcome scoring self-fulfilling; shadow = counterfactual arm (E4 tightened); held-out reuse optimistic; PARENT_OWNED (performative prediction, adaptive data analysis, E1/E4/E5)",
    "I4_FDX-15": "PROVED (finite attribution theorem) / PARENT_SUFFICIENT on the fixture / CONJECTURE for the general parent-product equivalence (falsifier: an ablation arm differing from the parent on matched channels); PARENT_OWNED statistics (D1, F2, F8, G7, G8)",
}

OPEN = []

CONJECTURES = [
    "FDX-15 general: for every OCM mechanism there is a composition of the registered parents plus the typed interface that is outcome-identical on matched channels (FORMALISM_USEFUL_NO_ARCHITECTURE_RESIDUAL); falsifier = an OCM-minus-Δ arm that differs from the parent product on a matched unit",
]

EXACTLY_BOUNDED_IMPOSSIBILITIES = [
    "FDX-08: no bound below T on the number of liveness flips over T steps without a registered generating model or a declared revision envelope (every smaller bound has an admissible counter-path)",
    "FDX-08: no predictive probability is a function of the observed ledger path alone (every registered model has positive likelihood on every path and they disagree by 1/2)",
    "FDX-11: an obstruction certificate cannot be issued at any state with an evidence neighbour that solves the task; conversely an obstruction is moved by no evidence change",
    "FDX-13: with the reflexive loop unregistered no self-prediction is stable on 9 of 75 fixtures (period-2 orbits); the counterfactual (shadow) rate is defined on all of them",
    "FDX-15: within one lifetime of four items the D1 rule can reject in neither direction; PARENT_SUFFICIENT needs n_d ≥ 76 discordant pairs; at m = 8 lifetimes the minimum detectable win probability at power 0.8 is 0.90",
]


def run_all():
    out = {name: fn() for name, fn in CHECKS.items()}
    out["ITEM_STATUS"] = STATUS
    out["OPEN"] = OPEN
    out["CONJECTURES"] = CONJECTURES
    out["EXACTLY_BOUNDED_IMPOSSIBILITIES"] = EXACTLY_BOUNDED_IMPOSSIBILITIES
    out["NOVELTY"] = "NOT_ESTABLISHED"
    out["status"] = "ALL_HOLD"
    return out


def main(argv=None):
    try:
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "reason": repr(exc)}))
        return 1
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
