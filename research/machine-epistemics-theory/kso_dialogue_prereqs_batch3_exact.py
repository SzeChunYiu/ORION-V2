"""Exact finite checker for KSO_DIALOGUE_PREREQUISITE_THEOREMS_BATCH3_V1.md (stdlib only, exact).

One check function per theorem (C1–C8, atlas ids MEG-33/25/27/11/10/15/16/21).  Every check performs
(a) the positive statement, (b) at least one planted mutant whose mutation is asserted applied and which
must be caught, and (c) a no-alarm control.  The minimal objects of the OCM core are re-implemented
here (antichain semiring, warrant intervals, Kleene liveness, authority meet, impact cone / reopening
report, version spaces, nogood filter, procedure terms, a seven-stage solve pipeline); nothing is
imported from ``ocm``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


# ---------------------------------------------------------------------------------------------
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21) — as in batches 1–2
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


def meet_all(ps):
    out = ONE
    for p in ps:
        out = meet(out, p)
    return out


def live(p, r):
    r = frozenset(r)
    return any(not (w & r) for w in p)


def leq(p, q):  # P ≤ Q ⇔ every warrant of P contains a warrant of Q
    return all(any(w2 <= w1 for w2 in q) for w1 in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"
ORDER3 = {DEAD: 0, UNKNOWN: 1, LIVE: 2}


def kand(a, b):
    return DEAD if DEAD in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else LIVE)


def kor(a, b):
    return LIVE if LIVE in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else DEAD)


def liveness(iv, r):
    lo, up = iv
    if live(lo, r):
        return LIVE
    if not live(up, r):
        return DEAD
    return UNKNOWN


def imeet(p, q):
    return (meet(p[0], q[0]), meet(p[1], q[1]))


def cert(*warrants):
    p = canon(frozenset(w) for w in warrants)
    return (p, p)


IONE = (ONE, ONE)
IUNKNOWN = (ZERO, ONE)


def subsets(universe):
    u = sorted(universe, key=repr)
    return [frozenset(c) for k in range(len(u) + 1) for c in itertools.combinations(u, k)]


def all_profiles(n):
    subs = subsets(range(n))
    out = set()
    for mask in range(1 << len(subs)):
        out.add(canon([subs[i] for i in range(len(subs)) if mask & (1 << i)]))
    return sorted(out, key=lambda p: (len(p), [sorted(w) for w in p]))


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=repr).encode()).hexdigest()


def auth_meet(*items):
    keys = set().union(*(set(a) for a in items))
    return {k: min(a.get(k, 0) for a in items) for k in keys}


DEPENDENCY = frozenset({"DEPENDENCE", "SUPPORT", "COMPOSITION", "CONSTRAINT"})


def edge(eid, tails, heads, iv=IONE, rel="DEPENDENCE"):
    tails = (tails,) if isinstance(tails, str) else tuple(tails)
    heads = (heads,) if isinstance(heads, str) else tuple(heads)
    return (eid, tails, heads, iv, rel)


def impact_cone(changed, edges):
    out = set(changed)
    grew = True
    while grew:
        grew = False
        for _, tails, heads, _, rel in edges:
            if rel in DEPENDENCY and any(t in out for t in tails):
                for h in heads:
                    if h not in out:
                        out.add(h)
                        grew = True
    return frozenset(out)


def reopening_report(atoms, edges, r0, r1):
    """KS-T22: (REOPEN, RECHECK, UNAFFECTED) for the delta R0 → R1."""
    changed = {x for x in atoms if liveness(atoms[x], r0) != liveness(atoms[x], r1)}
    for _, _, heads, ew, _ in edges:
        if liveness(ew, r0) != liveness(ew, r1):
            changed.update(heads)
    cone = impact_cone(changed, edges)
    return {"changed": frozenset(changed), "cone": cone, "reopen": cone & changed, "recheck": cone - changed, "unaffected": frozenset(atoms) - cone}


# version spaces (batch-2 B2) and the nogood filter (KS-T25)
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
ALL16 = tuple(itertools.product((0, 1), repeat=4))
AFFINE8 = tuple(t for t in ALL16 if sum(t) % 2 == 0)


def version_space(cls, examples):
    return [h for h in cls if all(h[i] == v for i, v in examples.items())]


def agrees_at(vs, i):
    return bool(vs) and len({h[i] for h in vs}) == 1


def vsw(cls, S, inputs):
    out = {}
    idxs = list(S)
    for i in inputs:
        working = [frozenset(S[j][1] for j in J) for J in subsets(idxs) if agrees_at(version_space(cls, {j: S[j][0] for j in J}), i)]
        out[i] = canon(working)
    return out


def nogood_filter(profile, nogoods):
    return canon(w for w in profile if not any(n <= w for n in nogoods))


# ---------------------------------------------------------------------------------------------
# C1 · MEG-33 · epistemic action value over intervals (clarification as an information action)
# ---------------------------------------------------------------------------------------------

QF = ("q0", "q1", "q2")                                   # registered query family
HYP = tuple(itertools.product((0, 1), repeat=4))          # (q0, q1, q2, hidden r): r is NOT in the family


def agreed(V):
    """Cells of the query family on which every hypothesis of V agrees."""
    return frozenset(i for i in range(len(QF)) if len({h[i] for h in V}) == 1)


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def expected_moved(V, blocks):
    """E[#cells UNKNOWN → decided | question with answer blocks] under the uniform prior on V."""
    base = agreed(V)
    return sum(Fraction(len(B), len(V)) * len(agreed(B) - base) for B in blocks)


def action_value(V, blocks, cost, risk):
    return expected_moved(V, blocks) - cost - risk


def refines(fine, coarse):
    return all(any(set(B) <= set(A) for A in coarse) for B in fine)


def restrict(blocks, V):
    return [[h for h in B if h in V] for B in blocks if any(h in V for h in B)]


def select_question(V, questions, cost, risk):
    """Ask the highest-value question, and only if its value is positive."""
    best = max(questions, key=lambda q: (action_value(V, restrict(q, V), cost, risk), repr(q)))
    return best if action_value(V, restrict(best, V), cost, risk) > 0 else None


def mutant_value_by_separation(V, blocks, cost, risk):
    """Planted (M4 §14 'irrelevant ambiguity triggers clarification loop'): counts hypotheses separated
    instead of cells decided on the query family."""
    pairs = sum(Fraction(len(A) * len(B), 1) for A, B in itertools.combinations(blocks, 2))
    return pairs / Fraction(len(V) * (len(V) - 1), 2) - cost - risk if len(V) > 1 else -cost - risk


def mutant_never_clarify(V, questions, cost, risk):
    """Planted (M4 §14 'consequential ambiguity ignored')."""
    return None


def query_refine(iv, new_evidence):
    """An INTERACTION answer exhibits a new warrant: L ⊕ {e}; the upper profile is untouched."""
    lo, up = iv
    return (join(lo, canon([frozenset({new_evidence})])), up)


def closure_certificate(iv):
    """An EXPERIMENTATION closure on the scope pins U := L (WLL-7 manifest)."""
    return (iv[0], iv[0])


def mutant_query_closes_upper(iv, new_evidence):
    """Planted: treats a speaker's answer as a closure certificate (U := L ⊕ {e})."""
    lo = join(iv[0], canon([frozenset({new_evidence})]))
    return (lo, lo)


def check_c1_meg33_epistemic_action_value():
    cost, risk = Fraction(1, 4), Fraction(0)
    irrelevant_zero = pairs_checked = strict_refinement = repeat_nonpositive = 0
    subsetsV = [V for k in (2, 3, 4) for V in itertools.combinations(HYP, k)]
    for V in subsetsV:
        parts = list(set_partitions(list(V)))
        values = [expected_moved(V, p) for p in parts]
        # (i) ambiguity irrelevant to the family ⇒ every question has zero information value
        if agreed(V) == frozenset(range(len(QF))):
            assert all(v == 0 for v in values)
            irrelevant_zero += 1
        # (iii) after any answer the same question is pointless: value = −cost − risk < 0
        for p in parts:
            for B in p:
                assert expected_moved(B, restrict(p, B)) == 0 and action_value(B, restrict(p, B), cost, risk) < 0
                repeat_nonpositive += 1
        # (ii) refinement monotonicity (only for |V| ≤ 3 pairs, exhaustive)
        if len(V) <= 3:
            for (pa, va), (pb, vb) in itertools.permutations(zip(parts, values), 2):
                if refines(pb, pa):
                    assert vb >= va
                    pairs_checked += 1
                    strict_refinement += int(vb > va)
    assert irrelevant_zero > 0 and strict_refinement > 0
    # (iv) queries move LIVE-side only; closure certificates are the only DEAD-side movers — exhaustive n=3
    query_never_dead = closure_only_dead = never_live_to_dead = 0
    for lo in all_profiles(3):
        iv = (lo, ONE)
        for R in subsets(range(3)):
            before = liveness(iv, R)
            after_q = liveness(query_refine(iv, "x"), R)
            after_c = liveness(closure_certificate(iv), R)
            assert after_q != DEAD and (before != LIVE or after_q == LIVE)
            query_never_dead += 1
            assert (after_c == DEAD) == (not live(lo, R)) and (before != LIVE or after_c == LIVE)
            closure_only_dead += 1
            later = set(R) | {"x"}                       # the answer's evidence is later revoked
            bad, honest = liveness(mutant_query_closes_upper(iv, "x"), later), liveness(query_refine(iv, "x"), later)
            never_live_to_dead += int(bad == DEAD and honest == UNKNOWN)   # the mutant minted DEAD-side certainty
    assert never_live_to_dead > 0
    # M4 §4 four cases in the microworld: hypotheses differ (A) only in the hidden bit, (B) on q0
    ask_q0 = [[h for h in HYP if h[0] == 0], [h for h in HYP if h[0] == 1]]
    ask_q1 = [[h for h in HYP if h[1] == 0], [h for h in HYP if h[1] == 1]]
    ask_r = [[h for h in HYP if h[3] == 0], [h for h in HYP if h[3] == 1]]
    questions = [ask_q0, ask_q1, ask_r]
    VA = [(1, 0, 1, 0), (1, 0, 1, 1)]
    assert select_question(VA, questions, cost, risk) is None                              # A: proceed, no question
    assert mutant_value_by_separation(VA, restrict(ask_r, VA), cost, risk) > 0                # mutant asks anyway
    VB = [(0, 0, 1, 0), (1, 0, 1, 0)]
    chosen = select_question(VB, questions, cost, risk)
    assert chosen == ask_q0 and action_value(VB, restrict(ask_q0, VB), cost, risk) == Fraction(3, 4)   # B: clarify
    oracle_gain = expected_moved(VB, restrict(ask_q0, VB))
    regret_mutant = oracle_gain - 0                                                            # never-clarify decides 0 cells
    assert mutant_never_clarify(VB, questions, cost, risk) is None and regret_mutant == 1
    VC = [(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0)]                                            # C: a separates 1|2, b separates all
    q_a = [[VC[0]], [VC[1], VC[2]]]
    q_b = [[VC[0]], [VC[1]], [VC[2]]]
    assert refines(q_b, q_a) and action_value(VC, q_b, cost, risk) > action_value(VC, q_a, cost, risk)
    # D: repeated pointless clarification after the answer is in
    VD = restrict(ask_q0, VB)[0]
    assert action_value(VD, restrict(ask_q0, VD), cost, risk) == -cost - risk < 0
    return {"hypothesis_sets": len(subsetsV), "irrelevant_ambiguity_zero_value_sets": irrelevant_zero, "refinement_pairs_checked": pairs_checked, "refinement_strict_cases": strict_refinement, "repeated_question_nonpositive": repeat_nonpositive, "query_never_dead_checks": query_never_dead, "closure_only_dead_side_checks": closure_only_dead, "mutant_query_closes_upper_mints_dead": never_live_to_dead, "case_A_no_question": 1, "case_B_clarify": 1, "case_C_refinement_preferred": 1, "case_D_repeat_penalised": 1, "mutant_value_by_separation_caught": 1, "mutant_never_clarify_regret": str(regret_mutant)}


# ---------------------------------------------------------------------------------------------
# C2 · MEG-25 · external commitment / codec gate: the renderer cannot mint support
# ---------------------------------------------------------------------------------------------

ASSERT, HEDGE, WITHHOLD = "ASSERT", "HEDGE", "WITHHOLD"
MARKER = {LIVE: ASSERT, UNKNOWN: HEDGE, DEAD: WITHHOLD}
REQUIREMENT = {ASSERT: {"world_truth": 1}, HEDGE: {}}


def plan_meaning(plan):
    return frozenset((p, m) for p, m in plan if m != WITHHOLD)


def render(plan):
    """Honest codec: a pure function of the plan (no store parameter exists in its signature)."""
    return tuple(sorted((p, m) for p, m in plan if m != WITHHOLD))


def decode(surface):
    return frozenset(surface)


def gate(surface, plan, store, R, protected, task_scope="world"):
    got = decode(surface)
    if digest(sorted(got)) != digest(sorted(plan_meaning(plan))):
        return "REFUSED:MEANING_DIGEST_MISMATCH"
    for p, m in got:
        if p in protected:
            return "REFUSED:PROTECTED_ANSWER"
        if p not in store:
            return "REFUSED:UNKNOWN_PROPOSITION"
        st = liveness(store[p]["iv"], R)
        if m != MARKER[st]:
            return f"REFUSED:MARKER_{m}_FOR_{st}"
        if m == ASSERT and (task_scope not in store[p]["scope"] or any(store[p]["auth"].get(k, 0) < v for k, v in REQUIREMENT[ASSERT].items())):
            return "REFUSED:WARRANT_SCOPE_OR_AUTHORITY"
    return "COMMITTED"


def mutant_renderer_injects_fact(plan, store, R):
    """Planted (M4 §14): a renderer holding a store handle adds a LIVE fact absent from the plan."""
    extra = next(p for p in store if all(p != q for q, _ in plan) and liveness(store[p]["iv"], R) == LIVE)
    return tuple(sorted(render(plan) + ((extra, ASSERT),)))


def mutant_uncertainty_dropped(plan):
    return tuple(sorted((p, ASSERT if m == HEDGE else m) for p, m in render(plan)))


def mutant_protected_leak(plan, gold):
    return tuple(sorted(render(plan) + ((gold, ASSERT),)))


def mutant_paraphrase_flips(plan):
    return tuple(sorted(("not:" + p if m == ASSERT else p, m) for p, m in render(plan)))


def check_c2_meg25_commitment_gate():
    props = ("p0", "p1", "p2")
    accept_iff_honest = 0
    for states in itertools.product((LIVE, DEAD, UNKNOWN), repeat=3):
        store, R = {}, set()
        for p, st in zip(props, states):
            store[p] = {"iv": IUNKNOWN if st == UNKNOWN else cert({"e_" + p}), "auth": {"world_truth": 1}, "scope": frozenset({"world"})}
            if st == DEAD:
                R.add("e_" + p)
        assert all(liveness(store[p]["iv"], R) == st for p, st in zip(props, states))
        for modes in itertools.product((ASSERT, HEDGE, WITHHOLD), repeat=3):
            plan = tuple(zip(props, modes))
            honest = all(m == MARKER[st] for m, st in zip(modes, states) if m != WITHHOLD)   # withholding is never laundering
            assert (gate(render(plan), plan, store, R, frozenset()) == "COMMITTED") == honest
            accept_iff_honest += 1
    # mutants on every honest plan; the protected gold answer sits in the store, never in a plan
    store = {"p0": {"iv": cert({"a"}), "auth": {"world_truth": 1}, "scope": frozenset({"world"})}, "p1": {"iv": IUNKNOWN, "auth": {"world_truth": 1}, "scope": frozenset({"world"})}, "p2": {"iv": cert({"c"}), "auth": {"world_truth": 1}, "scope": frozenset({"world"})}, "gold": {"iv": cert({"g"}), "auth": {"world_truth": 1}, "scope": frozenset({"world"})}, "said_p3": {"iv": cert({"t"}), "auth": {"speaker": 1}, "scope": frozenset({"world", "conversation"})}}
    protected = frozenset({"gold"})
    caught = {"inject": 0, "drop_uncertainty": 0, "protected_leak": 0, "paraphrase_flip": 0, "launder_said": 0}
    honest_plans = 0
    for R in (set(), {"c"}):
        for modes in itertools.product((ASSERT, HEDGE, WITHHOLD), repeat=3):
            plan = tuple(zip(("p0", "p1", "p2"), modes))
            if not all(m == MARKER[liveness(store[p]["iv"], R)] for p, m in plan if m != WITHHOLD):
                continue
            honest_plans += 1
            assert gate(render(plan), plan, store, R, protected) == "COMMITTED"           # no-alarm
            bad = mutant_renderer_injects_fact(plan, store, R)
            assert set(bad) > set(render(plan)) and gate(bad, plan, store, R, protected).startswith("REFUSED")
            caught["inject"] += 1
            bad = mutant_uncertainty_dropped(plan)
            assert (bad == render(plan)) == (HEDGE not in modes)
            if HEDGE in modes:
                assert gate(bad, plan, store, R, protected).startswith("REFUSED")
                caught["drop_uncertainty"] += 1
            bad = mutant_protected_leak(plan, "gold")
            assert ("gold", ASSERT) in bad and gate(bad, plan, store, R, protected).startswith("REFUSED")
            caught["protected_leak"] += 1
            bad = mutant_paraphrase_flips(plan)
            if ASSERT in modes:
                assert bad != render(plan) and gate(bad, plan, store, R, protected).startswith("REFUSED")
                caught["paraphrase_flip"] += 1
    # semantic half, authority: a speaker record LIVE as a record cannot be asserted as world fact
    plan = (("said_p3", ASSERT),)
    assert liveness(store["said_p3"]["iv"], set()) == LIVE and gate(render(plan), plan, store, set(), protected) == "REFUSED:WARRANT_SCOPE_OR_AUTHORITY"
    caught["launder_said"] = 1
    # a protected answer cannot pass even inside a plan (defence in depth over the capability half)
    plan = (("gold", ASSERT),)
    assert gate(render(plan), plan, store, set(), protected) == "REFUSED:PROTECTED_ANSWER"
    return {"accept_iff_honest_checks": accept_iff_honest, "honest_plans": honest_plans, **{f"mutant_{k}_caught": v for k, v in caught.items()}, "protected_in_plan_refused": 1}


# ---------------------------------------------------------------------------------------------
# C3 · MEG-27 · prefix commitment and bounded-lookahead satisfiability
# ---------------------------------------------------------------------------------------------

# construction inventory: a finite language over tokens; each sentence carries (claim, marker) pairs
# and referent requirements.  Discourse state: claim states ∈ {LIVE, UNKNOWN, DEAD}, #treatments ∈ {1, 2}.
NP = {("the", "second", "treatment"): ("T2", 2), ("treatment", "A"): ("T1", 1), ("it",): ("T1", 1)}
VP = {
    ("is", "safer"): ((("safer", ASSERT),), ()),
    ("may", "be", "safer"): ((("safer", HEDGE),), ()),
    ("is", "safer", "because", "of", "the", "dose"): ((("safer", ASSERT), ("dose", ASSERT)), ()),
    ("is", "safer", ";", "the", "reason", "is", "not", "established"): ((("safer", ASSERT), ("dose", HEDGE)), ()),
    ("is", "the", "second", "option"): (((), ), ()),
}


def sentences():
    out = []
    for np, (ref, need) in NP.items():
        for vp, (claims, _) in VP.items():
            claims = tuple(c for c in claims if c)
            out.append((np + vp, {"claims": frozenset(claims), "referents_needed": need}))
    return out


def acceptable(sentence_meaning, state):
    if sentence_meaning["referents_needed"] > state["treatments"]:
        return False
    return all(MARKER[state["claims"][c]] == m for c, m in sentence_meaning["claims"])


def lookahead(prefix, state, k, lang):
    """SAT if an acceptable completion of length ≤ k exists; UNSAT if no completion at all is acceptable;
    CANNOT_CHECK if the bound cut off unfinished continuations."""
    conts = [(s, m) for s, m in lang if s[: len(prefix)] == tuple(prefix)]
    if any(acceptable(m, state) and len(s) - len(prefix) <= k for s, m in conts):
        return "SAT"
    if any(len(s) - len(prefix) > k for s, m in conts):
        return "CANNOT_CHECK"
    return "UNSAT"


def commit_prefix(prefix, state, k, lang, repair_budget=0, repair_cost=1):
    la = lookahead(prefix, state, k, lang)
    if la == "SAT":
        return "COMMIT"
    if repair_budget >= repair_cost and any(acceptable(m, state) for _, m in lang):
        return "COMMIT_WITH_REPAIR"      # a registered repair act (retract prefix, restart) is affordable
    return "REFUSE:" + la


def mutant_greedy_prefix(prefix, state, lang):
    """Planted: commits whenever the prefix has not yet completed an unsupported claim."""
    return "COMMIT"


def mutant_bound_is_pass(prefix, state, k, lang):
    la = lookahead(prefix, state, k, lang)
    return "COMMIT" if la in ("SAT", "CANNOT_CHECK") else "REFUSE"


def realise(state, k, lang):
    """Token-by-token realiser under the prefix rule; returns the committed sentence or a reopen event."""
    prefix = []
    while True:
        options = sorted({s[len(prefix)] for s, m in lang if s[: len(prefix)] == tuple(prefix) and len(s) > len(prefix)})
        if not options:
            return ("DONE", tuple(prefix)) if any(s == tuple(prefix) and acceptable(m, state) for s, m in lang) else ("REOPEN", tuple(prefix))
        nxt = [t for t in options if commit_prefix(prefix + [t], state, k, lang) == "COMMIT"]
        if not nxt:
            return ("REOPEN", tuple(prefix))
        prefix.append(nxt[0])


def check_c3_meg27_prefix_commitment():
    lang = sentences()
    kmax = max(len(s) for s, _ in lang)
    prefixes = sorted({s[:i] for s, _ in lang for i in range(1, len(s) + 1)})
    states = [{"claims": {"safer": a, "dose": b}, "treatments": t} for a in (LIVE, UNKNOWN, DEAD) for b in (LIVE, UNKNOWN, DEAD) for t in (1, 2)]
    committed_have_completion = exact_at_full_bound = bounded_never_pass = greedy_forced = refused_have_none = 0
    for st in states:
        for pre in prefixes:
            full = lookahead(pre, st, kmax, lang)
            assert full in ("SAT", "UNSAT")                                    # (ii) full bound is exact
            exact_at_full_bound += 1
            verdict = commit_prefix(pre, st, kmax, lang)
            if verdict == "COMMIT":
                assert any(s[: len(pre)] == pre and acceptable(m, st) for s, m in lang)   # (i) never forced
                committed_have_completion += 1
            else:
                assert not any(s[: len(pre)] == pre and acceptable(m, st) for s, m in lang)
                refused_have_none += 1
                if mutant_greedy_prefix(pre, st, lang) == "COMMIT":
                    greedy_forced += 1                                             # mutant commits a dead-end prefix
            for k in range(0, kmax):
                la = lookahead(pre, st, k, lang)
                if la == "CANNOT_CHECK":
                    assert commit_prefix(pre, st, k, lang) == "REFUSE:CANNOT_CHECK"
                    if mutant_bound_is_pass(pre, st, k, lang) == "COMMIT" and full == "UNSAT":
                        bounded_never_pass += 1                                    # mutant commits an unsatisfiable prefix
                elif la == "SAT":
                    assert full == "SAT"
    assert greedy_forced > 0 and bounded_never_pass > 0
    # the three protected reopen cases of #8 §7 through the realiser
    lang_t2 = [(s, m) for s, m in lang if s[:3] == ("the", "second", "treatment")]
    missing_ref = realise({"claims": {"safer": LIVE, "dose": LIVE}, "treatments": 1}, kmax, lang_t2)
    assert missing_ref[0] == "REOPEN" and missing_ref[1] == ()                    # (a) no referent: nothing committed, reopen reference
    weakened = realise({"claims": {"safer": UNKNOWN, "dose": DEAD}, "treatments": 2}, kmax, [(s, m) for s, m in lang_t2 if "safer" in s])
    assert weakened == ("DONE", ("the", "second", "treatment", "may", "be", "safer"))   # (b) comparative weakened
    gap_stated = realise({"claims": {"safer": LIVE, "dose": UNKNOWN}, "treatments": 2}, kmax, [(s, m) for s, m in lang_t2 if "because" in s or "reason" in s])
    assert gap_stated == ("DONE", ("the", "second", "treatment", "is", "safer", ";", "the", "reason", "is", "not", "established"))   # (c) missing premise stated as a gap
    # no-alarm: everything LIVE and resolvable ⇒ every prefix of the plain assertion commits
    st = {"claims": {"safer": LIVE, "dose": LIVE}, "treatments": 2}
    s = ("the", "second", "treatment", "is", "safer", "because", "of", "the", "dose")
    assert all(commit_prefix(s[:i], st, kmax, lang) == "COMMIT" for i in range(1, len(s) + 1))
    # a repair act at bounded cost turns a refused prefix into COMMIT_WITH_REPAIR, never into COMMIT
    st_u = {"claims": {"safer": UNKNOWN, "dose": UNKNOWN}, "treatments": 2}
    assert commit_prefix(("the", "second", "treatment", "is", "safer"), st_u, kmax, lang) == "REFUSE:UNSAT"
    assert commit_prefix(("the", "second", "treatment", "is", "safer"), st_u, kmax, lang, repair_budget=1) == "COMMIT_WITH_REPAIR"
    return {"sentences": len(lang), "prefixes": len(prefixes), "discourse_states": len(states), "committed_prefixes_have_completion": committed_have_completion, "refused_prefixes_have_none": refused_have_none, "full_bound_exact": exact_at_full_bound, "mutant_greedy_commits_dead_end": greedy_forced, "mutant_bound_is_pass_caught": bounded_never_pass, "reopen_missing_referent": 1, "reopen_weakened_comparative": 1, "reopen_missing_premise_stated": 1, "no_alarm_all_live": 1, "repair_at_bounded_cost": 1}


# ---------------------------------------------------------------------------------------------
# C4 · MEG-11 · small-step operational semantics of the solve pipeline
# ---------------------------------------------------------------------------------------------

STAGES = ("ATOMIZE", "NAVIGATE", "FIRE", "EXTRACT", "COMPOSE", "CHECK", "COMMIT")
FOUND, GAP, OBSTRUCTION, CANNOT = "FOUND", "GAP", "OBSTRUCTION", "CANNOT_CHECK"
TERMINALS = (FOUND, GAP, OBSTRUCTION, CANNOT)


def kleene_reach(atoms, edges, seeds, R):
    """Three-valued reachability: r(seed) = λ(seed); r(head) = ⊕₃ over edges of λ(edge) ⊗₃ ⊗₃ r(tails)."""
    r = {x: DEAD for x in atoms}
    for s in seeds:
        r[s] = liveness(atoms[s], R)
    changed = True
    while changed:
        changed = False
        for _, tails, heads, ew, _ in edges:
            v = liveness(ew, R)
            for t in tails:
                v = kand(v, r[t])
            for h in heads:
                nv = kor(r[h], kand(v, liveness(atoms[h], R)))
                if nv != r[h]:
                    r[h], changed = nv, True
    return r


def step(cfg, fx, R, mutant=None):
    """One small step.  cfg: {stage, status, payload…}.  Returns the successor configuration."""
    i = STAGES.index(cfg["stage"])
    nxt = STAGES[i + 1] if i + 1 < len(STAGES) else None
    out = dict(cfg)
    if cfg["status"] == CANNOT and mutant != "launder":
        out.update(stage=nxt, status=CANNOT, reason="ABSORBED")          # absorbing
        return out if nxt else {**out, "stage": None, "terminal": CANNOT}
    atoms, edges = fx["atoms"], fx["edges"]
    if cfg["stage"] == "ATOMIZE":
        seeds = [s for s in fx["seeds"] if s in atoms]
        if len(seeds) < len(fx["seeds"]):
            return {**out, "stage": None, "terminal": GAP, "reason": "UNBOUND_SEED"}
        out.update(stage=nxt, status="PASS", seeds=seeds)
    elif cfg["stage"] == "NAVIGATE":
        r = kleene_reach(atoms, edges, cfg["seeds"], R)
        tgt = fx["target"]
        if tgt not in atoms:
            return {**out, "stage": None, "terminal": GAP, "reason": "TARGET_ABSENT"}
        if liveness(atoms[tgt], R) == DEAD:
            return {**out, "stage": None, "terminal": OBSTRUCTION, "reason": "TARGET_WARRANT_DEAD"}
        if r[tgt] == DEAD:
            return {**out, "stage": None, "terminal": GAP, "reason": "TARGET_UNREACHABLE"}
        out.update(stage=nxt, status=CANNOT if r[tgt] == UNKNOWN else "PASS", reach=r, reason="REACH_" + r[tgt])
    elif cfg["stage"] == "FIRE":
        derived = {s: {"steps": (), "mark": liveness(atoms[s], R)} for s in cfg["seeds"]}
        changed = True
        while changed:
            changed = False
            for eid, tails, heads, ew, _ in edges:
                if not all(t in derived for t in tails):
                    continue
                v = liveness(ew, R)
                for t in tails:
                    v = kand(v, derived[t]["mark"])
                enabled = v == LIVE or (mutant == "fire_unknown" and v == UNKNOWN)
                if not enabled:
                    continue
                for h in heads:
                    if h not in derived and liveness(atoms[h], R) != DEAD:
                        derived[h] = {"steps": tuple(sorted({eid, *itertools.chain.from_iterable(derived[t]["steps"] for t in tails)})), "mark": LIVE if (v == LIVE and liveness(atoms[h], R) == LIVE) or mutant == "fire_unknown" else UNKNOWN}
                        changed = True
        out.update(stage=nxt, status="PASS", derived=derived)
    elif cfg["stage"] == "EXTRACT":
        react = {x for x, d in cfg["derived"].items() if d["mark"] == LIVE}
        if fx["target"] not in react:
            return {**out, "stage": None, "terminal": GAP, "reason": "NO_WARRANTED_REACTION"}
        out.update(stage=nxt, status="PASS", reacting=react)
    elif cfg["stage"] == "COMPOSE":
        d = cfg["derived"][fx["target"]]
        ivs = [atoms[s] for s in cfg["seeds"]] + [e[3] for e in edges if e[0] in d["steps"]] + [atoms[fx["target"]], fx["operator"]["iv"]]
        cand = IONE
        for iv in ivs:
            cand = imeet(cand, iv)
        st = liveness(cand, R)
        out.update(stage=nxt, status="PASS" if st == LIVE else (CANNOT if st == UNKNOWN else "FAIL"), candidate=cand, reason="CANDIDATE_" + st)
        if st == DEAD:
            return {**out, "stage": None, "terminal": GAP, "reason": "CANDIDATE_DEAD"}
    elif cfg["stage"] == "CHECK":
        verdict = fx["operator"]["checker"]           # PASS | FAIL | CANNOT_CHECK from the registered checker
        if verdict == "FAIL":
            return {**out, "stage": None, "terminal": GAP, "reason": "CHECK_FAILED"}
        out.update(stage=nxt, status="PASS" if verdict == "PASS" else CANNOT, reason="CHECK_" + verdict)
        if mutant == "launder" and verdict == "PASS":
            out["candidate"] = (cfg["candidate"][1], cfg["candidate"][1])   # planted: the checker's pass mints the warrant
    elif cfg["stage"] == "COMMIT":
        ok = cfg["status"] == "PASS" and liveness(cfg["candidate"], R) == LIVE
        return {**out, "stage": None, "terminal": FOUND if ok else CANNOT, "reason": "COMMITTED" if ok else "REFUSED"}
    return out


def run_pipeline(fx, R, mutant=None):
    cfg = {"stage": "ATOMIZE", "status": "PASS"}
    trace = [cfg]
    while cfg.get("stage") is not None:
        cfg = step(cfg, fx, R, mutant)
        trace.append(cfg)
    return trace


def derivation_all_live(fx, R, derived, x):
    """A LIVE derivation: every fired edge and every atom on it (tails, heads, x) is LIVE — no UNKNOWN/DEAD step."""
    emap = {e[0]: e for e in fx["edges"]}
    steps = derived[x]["steps"]
    on_it = {x, *itertools.chain.from_iterable((*emap[e][1], *emap[e][2]) for e in steps)}
    return all(liveness(emap[e][3], R) == LIVE for e in steps) and all(liveness(fx["atoms"][y], R) == LIVE for y in on_it)


def random_fixture(rng, n=5):
    ids = [f"v{i}" for i in range(n)]
    atoms = {}
    for x in ids:
        kind = rng.choice(("cert", "cert", "partial", "one"))
        atoms[x] = IONE if kind == "one" else (cert(frozenset(rng.sample(range(3), rng.randint(1, 2)))) if kind == "cert" else (canon([frozenset({rng.randint(0, 2)})]), ONE))
    edges = [edge(f"c{i}", ids[i], ids[i + 1], iv=rng.choice((IONE, cert({rng.randint(0, 2)}), (canon([frozenset({rng.randint(0, 2)})]), ONE)))) for i in range(n - 1)]
    for _ in range(rng.randint(0, 2)):
        i, j = sorted(rng.sample(range(n), 2))
        edges.append(edge(f"x{i}{j}", ids[i], ids[j], iv=IONE, rel="SUPPORT"))
    target = ids[-1] if rng.random() < 0.85 else "absent"
    return {"atoms": atoms, "edges": edges, "seeds": [ids[0]], "target": target, "operator": {"iv": rng.choice((IONE, IONE, (canon([frozenset({0})]), ONE))), "checker": rng.choice(("PASS", "PASS", "PASS", "FAIL", CANNOT))}}


def trace_digest(trace):
    return digest([{k: v for k, v in c.items() if k in ("stage", "status", "terminal", "reason")} for c in trace])


def check_c4_meg11_pipeline_semantics():
    rng = random.Random(11)
    fixtures = [random_fixture(rng) for _ in range(40)]
    terminals = {t: 0 for t in TERMINALS}
    configs = progress = preserved = absorbed = replay = mutant_fire_caught = mutant_launder_caught = stale_caught = 0
    for fx in fixtures:
        cache = {}
        for R in subsets(range(3)):
            trace = run_pipeline(fx, R)
            last = trace[-1]
            assert last["terminal"] in TERMINALS
            terminals[last["terminal"]] += 1
            for c in trace[:-1]:                                                      # progress: non-terminal ⇒ steps
                assert c.get("stage") in STAGES and step(c, fx, R) is not None
                configs += 1
            progress += 1
            # preservation: every LIVE-marked derived atom has an all-LIVE derivation and a LIVE interval
            for c in trace:
                for x, d in c.get("derived", {}).items():
                    if d["mark"] == LIVE:
                        assert derivation_all_live(fx, R, c["derived"], x) and liveness(fx["atoms"][x], R) == LIVE
                        preserved += 1
            # absorption: after the first CANNOT_CHECK every later status is CANNOT_CHECK and the terminal is CANNOT_CHECK
            seen = False
            for c in trace:
                if seen:
                    assert c.get("status") == CANNOT and (c.get("terminal") in (None, CANNOT))
                seen = seen or c.get("status") == CANNOT
            if seen:
                assert last["terminal"] == CANNOT
                absorbed += 1
            if last["terminal"] == FOUND:
                assert liveness(trace[-2]["candidate"], R) == LIVE
            # restart-invariant replay: persist the fixture and R, reload, same trace digest
            persisted = json.loads(json.dumps({"R": sorted(R)}))
            assert trace_digest(run_pipeline(fx, frozenset(persisted["R"]))) == trace_digest(trace)
            replay += 1
            # stale-cache mutant: navigation cached by target only (ignores R) — differs after a revocation
            key = fx["target"]
            r_now = kleene_reach(fx["atoms"], fx["edges"], fx["seeds"], R).get(key)
            if key in cache and cache[key] != r_now:
                stale_caught += 1
            cache.setdefault(key, r_now)
            # planted mutants
            bad = run_pipeline(fx, R, mutant="fire_unknown")
            for c in bad:
                for x, d in c.get("derived", {}).items():
                    if d["mark"] == LIVE and not derivation_all_live(fx, R, c["derived"], x):
                        mutant_fire_caught += 1
                        break
            bad = run_pipeline(fx, R, mutant="launder")
            if bad[-1]["terminal"] == FOUND and any(c.get("status") == CANNOT for c in bad):
                mutant_launder_caught += 1
    assert all(v > 0 for v in terminals.values()) and mutant_fire_caught > 0 and mutant_launder_caught > 0 and stale_caught > 0
    return {"fixtures": len(fixtures), "runs": progress, "non_terminal_configs_step": configs, "terminals": terminals, "live_marks_preserved": preserved, "cannot_check_absorbed_runs": absorbed, "replay_identical": replay, "mutant_fire_on_unknown_caught": mutant_fire_caught, "mutant_launder_cannot_check_caught": mutant_launder_caught, "mutant_stale_cache_caught": stale_caught}


# ---------------------------------------------------------------------------------------------
# C5 · MEG-10 · procedure-algebra warrant laws (⊗ sequencing, ⊕ alternative, guarded choice, metered loop)
# ---------------------------------------------------------------------------------------------


def P(name, w, fn=lambda v: v):
    return ("PRIM", name, w, fn)


SKIP, FAIL = ("SKIP",), ("FAIL",)


def SEQ(p, q):
    return ("SEQ", p, q)


def ALT(p, q, certified=True):
    """Alternative derivations of one registered function: warrant ⊕ only under an equivalence certificate
    on the query family; without it the choice is read as worst case (⊗), exactly like guarded choice."""
    return ("ALT", p, q, certified)


def IF(g, p, q):
    return ("IF", g, p, q)


def LOOP(g, p, n):
    return ("LOOP", g, p, n)


def static(t):
    k = t[0]
    if k == "PRIM":
        return t[2]
    if k == "SKIP":
        return ONE
    if k == "FAIL":
        return ZERO
    if k == "SEQ":
        return meet(static(t[1]), static(t[2]))
    if k == "ALT":
        return join(static(t[1]), static(t[2])) if t[3] else meet(static(t[1]), static(t[2]))
    if k == "IF":
        return meet(t[1][2], meet(static(t[2]), static(t[3])))
    if k == "LOOP":
        return t[1][2] if t[3] == 0 else meet(t[1][2], static(t[2]))
    raise CannotCheck(k)


def run(t, x, meter, budget, unmetered=False):
    """TRACE reading: ⊗ of what fired; the meter counts loop iterations against the registered budget."""
    k = t[0]
    if k == "PRIM":
        return t[3](x), t[2], meter
    if k == "SKIP":
        return x, ONE, meter
    if k == "FAIL":
        return None, ZERO, meter
    if k == "SEQ":
        a, wa, m = run(t[1], x, meter, budget, unmetered)
        b, wb, m = run(t[2], a, m, budget, unmetered)
        return b, meet(wa, wb), m
    if k == "ALT":                                     # registered alternative: the first method that yields
        a, wa, m = run(t[1], x, meter, budget, unmetered)
        return (a, wa, m) if a is not None else run(t[2], x, meter, budget, unmetered)
    if k == "IF":
        g = t[1]
        branch = t[2] if g[3](x) else t[3]
        v, w, m = run(branch, x, meter, budget, unmetered)
        return v, meet(g[2], w), m
    if k == "LOOP":
        g, body, n = t[1], t[2], t[3]
        w, v, it = g[2], x, 0
        while g[3](v):
            if it >= n or (meter + 1 > budget):
                if unmetered:
                    return v, w, meter
                raise CannotCheck("BUDGET_EXHAUSTED")
            v, wb, meter = run(body, v, meter, budget, unmetered)
            w, it = meet(w, wb), it + 1
            meter += 1
        return v, w, meter
    raise CannotCheck(k)


def mutant_if_as_alternative(t):
    """Planted: reads guarded choice as ⊕ in the STATIC reading."""
    return meet(t[1][2], join(static(t[2]), static(t[3])))


def mutant_alt_join_without_certificate(t):
    """Planted: ⊕ over two methods that are not certified equivalent."""
    return join(static(t[1]), static(t[2]))


def check_c5_meg10_procedure_algebra_laws():
    ps = all_profiles(3)
    revs = subsets(range(3))
    laws = {"seq_assoc": 0, "seq_unit_annihilator": 0, "seq_warrant_commutes": 0, "alt_assoc_comm_idem_unit": 0, "distributive": 0, "if_static_below_trace": 0, "live_static_implies_live_trace": 0, "loop_idempotent": 0}
    for wa, wb, wc in itertools.product(ps, repeat=3):
        a, b, c = P("a", wa), P("b", wb), P("c", wc)
        assert static(SEQ(SEQ(a, b), c)) == static(SEQ(a, SEQ(b, c)))
        laws["seq_assoc"] += 1
        assert static(SEQ(a, SKIP)) == wa == static(SEQ(SKIP, a)) and static(SEQ(a, FAIL)) == ZERO == static(SEQ(FAIL, a))
        laws["seq_unit_annihilator"] += 1
        assert static(SEQ(a, b)) == static(SEQ(b, a))
        laws["seq_warrant_commutes"] += 1
        assert static(ALT(ALT(a, b), c)) == static(ALT(a, ALT(b, c))) and static(ALT(a, b)) == static(ALT(b, a)) and static(ALT(a, a)) == wa and static(ALT(a, FAIL)) == wa
        laws["alt_assoc_comm_idem_unit"] += 1
        assert static(SEQ(a, ALT(b, c))) == static(ALT(SEQ(a, b), SEQ(a, c))) and static(SEQ(ALT(a, b), c)) == static(ALT(SEQ(a, c), SEQ(b, c)))
        laws["distributive"] += 1
    # guarded choice and the metered loop (guard warrant wg, branches wa/wb), all revocations
    if_strict = 0
    for wg, wa, wb in itertools.product(ps[:8], ps, ps):
        g = ("TEST", "g", wg, lambda v: v % 2 == 0)
        prog = IF(g, P("a", wa, lambda v: v + 2), P("b", wb, lambda v: v + 1))
        st = static(prog)
        for x in (2, 3):
            _, tr, _ = run(prog, x, 0, 10)
            assert leq(st, tr)
            laws["if_static_below_trace"] += 1
            for R in revs:
                assert liveness((st, st), R) != LIVE or liveness((tr, tr), R) == LIVE
                laws["live_static_implies_live_trace"] += 1
                if liveness((st, st), R) == DEAD and liveness((tr, tr), R) == LIVE:
                    if_strict += 1
        # loop: static idempotent in the bound; trace = guard ⊗ body whenever ≥ 1 iteration ran
        body = P("dec", wa, lambda v: v - 1)
        g2 = ("TEST", "pos", wg, lambda v: v > 0)
        assert static(LOOP(g2, body, 1)) == static(LOOP(g2, body, 2)) == static(LOOP(g2, body, 3)) == meet(wg, wa) and static(LOOP(g2, body, 0)) == wg
        v, tr, m = run(LOOP(g2, body, 3), 2, 0, 10)
        assert v == 0 and tr == meet(wg, wa) and m == 2
        laws["loop_idempotent"] += 1
    assert if_strict > 0
    # meter: exceeding the registered bound or budget is CANNOT_CHECK, never a warranted result
    g2 = ("TEST", "pos", ONE, lambda v: v > 0)
    body = P("dec", ONE, lambda v: v - 1)
    exhausted = 0
    for bound, budget, x in ((1, 10, 3), (5, 2, 3), (0, 10, 1)):
        try:
            run(LOOP(g2, body, bound), x, 0, budget)
        except CannotCheck:
            exhausted += 1
    assert exhausted == 3
    v, w, m = run(LOOP(g2, body, 1), 3, 0, 10, unmetered=True)                       # mutation applied: returns a result
    assert v == 2 and liveness((w, w), set()) == LIVE and m == 1                       # …with a LIVE trace warrant: the mutant
    # if-as-alternative mutant: LIVE while the taken branch is DEAD
    g = ("TEST", "g", ONE, lambda v: v % 2 == 0)
    prog = IF(g, P("a", cert({0})[0], lambda v: v), P("b", cert({1})[0], lambda v: v))
    assert liveness((static(prog), static(prog)), {1}) == DEAD and liveness((mutant_if_as_alternative(prog), mutant_if_as_alternative(prog)), {1}) == LIVE
    _, tr_odd, _ = run(prog, 3, 0, 10)
    assert liveness((tr_odd, tr_odd), {1}) == DEAD                                      # the run that takes b is DEAD; the mutant said LIVE
    # static-for-trace mutant (KS-T26 shape, re-witnessed): the even run is LIVE though static is DEAD
    _, tr_even, _ = run(prog, 2, 0, 10)
    assert liveness((tr_even, tr_even), {1}) == LIVE and liveness((static(prog), static(prog)), {1}) == DEAD
    # certified alternative: trace ≤ join (the atom is at least as live as either derivation); without the
    # certificate the join warrants an output the live method does not produce
    alt = ALT(P("m1", cert({0})[0], lambda v: v * 10), P("m2", cert({1})[0], lambda v: v * 10))
    out1, tr, _ = run(alt, 3, 0, 10)
    assert leq(tr, static(alt)) and liveness((static(alt), static(alt)), {0}) == LIVE and liveness((tr, tr), {0}) == DEAD
    unc = ALT(P("m1", cert({0})[0], lambda v: v * 10), P("m3", cert({1})[0], lambda v: v + 1), certified=False)
    out_taken, tr_u, _ = run(unc, 3, 0, 10)
    out_other = run(unc[2], 3, 0, 10)[0]
    assert liveness((static(unc), static(unc)), {0}) == DEAD                                    # honest: worst case
    assert liveness((mutant_alt_join_without_certificate(unc), mutant_alt_join_without_certificate(unc)), {0}) == LIVE and out_taken != out_other   # mutant warrants an output the live method never produces
    # static ≤ trace on random programs of depth ≤ 3 (no-alarm over the whole grammar; uncertified choice)
    rng = random.Random(10)

    def rand_prog(d):
        if d == 0 or rng.random() < 0.3:
            return P("p", rng.choice(ps), lambda v: v + 1)
        k = rng.choice(("SEQ", "ALT", "IF", "LOOP"))
        if k == "SEQ":
            return SEQ(rand_prog(d - 1), rand_prog(d - 1))
        if k == "ALT":
            return ALT(rand_prog(d - 1), rand_prog(d - 1), certified=False)
        if k == "IF":
            return IF(("TEST", "g", rng.choice(ps), lambda v: v % 2 == 0), rand_prog(d - 1), rand_prog(d - 1))
        return LOOP(("TEST", "g", rng.choice(ps), lambda v: v < 3), rand_prog(d - 1), 2)

    random_ok = 0
    for _ in range(300):
        prog = rand_prog(3)
        try:
            _, tr, _ = run(prog, 0, 0, 50)
        except CannotCheck:
            continue
        assert leq(static(prog), tr)
        random_ok += 1
    assert random_ok > 200
    return {"profiles_at_n3": len(ps), **laws, "if_strict_static_dead_trace_live": if_strict, "meter_exhaustion_cannot_check": exhausted, "mutant_unmetered_loop_caught": 1, "mutant_if_as_alternative_caught": 1, "mutant_static_for_trace_caught": 1, "certified_alternative_trace_below_join": 1, "mutant_alt_without_certificate_caught": 1, "random_programs_static_below_trace": random_ok}


# ---------------------------------------------------------------------------------------------
# C6 · MEG-15 · discriminating-interaction certificate (feedback never warrants; outcomes do)
# ---------------------------------------------------------------------------------------------


def observe(omega, world, u, scope):
    """Registered outcome function ω on scope S: an OBSERVATION atom about the outcome claim, or CANNOT_CHECK."""
    if u not in scope:
        return None
    return {"claim": ("outcome", u), "value": omega(world, u), "iv": cert({f"o_{u}"}), "channel": "EXPERIMENTATION"}


def eliminate(V, u, o):
    return [h for h in V if h[u] == o]


def feedback_atom(reward):
    return {"claim": "reward", "value": reward, "iv": (ZERO, ZERO), "channel": "FEEDBACK"}


def mutant_reward_as_outcome(V, u, reward):
    """Planted: treats an unregistered endpoint reward as the outcome value."""
    return eliminate(V, u, reward)


def mutant_feedback_raises_interval(proc_iv, reward):
    return (join(proc_iv[0], canon([frozenset({"reward"})])), proc_iv[1])


def check_c6_meg15_discriminating_interaction():
    omega = lambda world, u: world[u]                      # the sandbox evaluates the utterance's registered probe
    rewards = (lambda w, u: w[u], lambda w, u: 1 - w[u], lambda w, u: 0, lambda w, u: 1)
    sound = unsound_mutant = out_of_scope = feedback_zero = 0
    scope = (0, 1, 2)
    proc_iv = cert({"lesson"})
    for world in ALL16:
        for u in range(4):
            obs = observe(omega, world, u, scope)
            if obs is None:
                out_of_scope += 1                               # u ∉ S: no atom, no elimination
                continue
            V1 = eliminate(list(ALL16), u, obs["value"])
            assert world in V1 and liveness(obs["iv"], set()) == LIVE and obs["channel"] == "EXPERIMENTATION"
            sound += 1
            for rw in rewards:
                fb = feedback_atom(rw(world, u))
                assert fb["iv"] == (ZERO, ZERO) and liveness(fb["iv"], set()) == DEAD    # FEEDBACK admits nothing
                feedback_zero += 1
                Vbad = mutant_reward_as_outcome(list(ALL16), u, fb["value"])
                if world not in Vbad:
                    unsound_mutant += 1                         # the true world eliminated by a reward
    assert unsound_mutant > 0
    # the procedure's own interval is feedback-free: identical before and after any interaction sequence
    bad = mutant_feedback_raises_interval(proc_iv, 1)
    assert bad != proc_iv and liveness(bad, {"lesson"}) == LIVE and liveness(proc_iv, {"lesson"}) == DEAD   # mutation applied and wrong
    # the claim "procedure achieves the goal on Q" carries the VSW warrant of the outcome observations (B2);
    # revoking one outcome observation reopens exactly its per-input set; the procedure atom is untouched
    world = AFFINE8[3]
    S = {u: (world[u], f"o_{u}") for u in scope}
    W = vsw(AFFINE8, S, range(4))
    assert all(W[u] != ZERO for u in range(4)) and liveness((W[3], W[3]), set()) == LIVE       # input 3 pinned by the class
    reopened = frozenset(u for u in range(4) if liveness((W[u], W[u]), set()) == LIVE and liveness((W[u], W[u]), {"o_0"}) != LIVE)
    assert reopened == frozenset({0, 3}) and proc_iv == cert({"lesson"})     # inputs 1, 2 keep their own observation
    # same utterance, registered vs unregistered outcome: only the registered one moves any interval
    claim_iv = (W[0], ONE)
    assert liveness(claim_iv, set()) == LIVE and liveness((ZERO, ONE), set()) == UNKNOWN
    return {"worlds": len(ALL16), "sound_eliminations": sound, "out_of_scope_cannot_check": out_of_scope, "feedback_interval_zero": feedback_zero, "mutant_reward_as_outcome_eliminates_truth": unsound_mutant, "mutant_feedback_raises_interval_caught": 1, "claim_warrant_is_vsw": 1, "per_input_reopen_on_o0": sorted(reopened), "procedure_interval_unchanged": 1}


# ---------------------------------------------------------------------------------------------
# C7 · MEG-16 · contradiction resolution policy over nogood-lifted intervals
# ---------------------------------------------------------------------------------------------


def machine_verdict(store, prop, neg, R, nogoods=()):
    """Verdict on p: UNKNOWN while p and ¬p both LIVE on an overlapping scope (their joint warrant is a
    registered nogood); otherwise the Kleene liveness of p's own nogood-filtered interval."""
    def iv_of(q):
        auth = [a for a in store if a["prop"] == q and a["auth"].get("world_truth", 0) >= 1]
        if not auth:
            return IUNKNOWN, frozenset()
        lo = up = ZERO
        sc = frozenset()
        for a in auth:
            lo, up, sc = join(lo, a["iv"][0]), join(up, a["iv"][1]), sc | a["scope"]
        return (nogood_filter(lo, nogoods), nogood_filter(up, nogoods)), sc
    ivp, sp = iv_of(prop)
    ivn, sn = iv_of(neg)
    if liveness(ivp, R) == LIVE and liveness(ivn, R) == LIVE and sp & sn:
        return UNKNOWN, "CONTRADICTION_ACTIVE"
    return liveness(ivp, R), "OWN_INTERVAL"


def said(who, prop, ev, epoch=(0, float("inf"))):
    return {"kind": "said", "who": who, "prop": prop, "iv": cert({ev}), "auth": {"speaker": 1}, "scope": frozenset({"conversation"}), "epoch": epoch, "ev": ev}


def bridge(prop, ev, scope):
    return {"kind": "bridge", "prop": prop, "iv": cert({ev}), "auth": {"world_truth": 1}, "scope": frozenset(scope), "ev": ev}


def history_digest(store):
    return digest(sorted((a["who"], a["prop"], a["ev"]) for a in store if a["kind"] == "said"))


def records_active(store, R):
    return {a["ev"] for a in store if a["kind"] == "said" and liveness(a["iv"], R) == LIVE}


def mutant_majority_resolves(store, prop, R, k=3):
    n = sum(1 for a in store if a["kind"] == "said" and a["prop"] == prop and liveness(a["iv"], R) == LIVE)
    return LIVE if n >= k else UNKNOWN


def check_c7_meg16_contradiction_policy():
    p, np_ = "flight_tue", "not:flight_tue"
    t1, t2 = said("u1", p, "t1"), said("u2", np_, "t2")
    store = [t1, t2]
    h0 = history_digest(store)
    nog = (frozenset({"t1", "t2"}),)                                     # workspace.commit registers contradicts=(t1) for t2
    # (i) two live records: neither promoted, machine UNKNOWN both ways, contradiction ACTIVE, composite DEAD
    assert records_active(store, set()) == {"t1", "t2"} and machine_verdict(store, p, np_, set()) == (UNKNOWN, "OWN_INTERVAL")
    joint = meet(t1["iv"][0], t2["iv"][0])
    assert nogood_filter(joint, nog) == ZERO and nogood_filter(t1["iv"][0], nog) == t1["iv"][0]   # KS-T25(iv): composite dead, parts intact
    # (ii) majority never resolves: up to ten more records on either side
    majority_checks = 0
    for k in range(1, 11):
        for side in (p, np_):
            st = store + [said(f"u{10 + i}", side, f"t{10 + i}") for i in range(k)]
            assert machine_verdict(st, p, np_, set())[0] == UNKNOWN and machine_verdict(st, np_, p, set())[0] == UNKNOWN
            assert history_digest(st) != h0 and history_digest(st[:2]) == h0        # history only grows
            majority_checks += 1
    bad = mutant_majority_resolves(store + [said(f"u{10 + i}", p, f"t{10 + i}") for i in range(3)], p, set())
    assert bad == LIVE
    # (iii) a scoped bridge resolves for the machine on its scope; the records are untouched
    b1 = bridge(p, "b1", {"world"})
    st = store + [b1]
    assert machine_verdict(st, p, np_, set()) == (LIVE, "OWN_INTERVAL") and machine_verdict(st, np_, p, set())[0] == UNKNOWN
    assert records_active(st, set()) == {"t1", "t2"} and history_digest(st) == h0
    # two bridges on overlapping scope: machine-level nogood, verdict UNKNOWN while both live; exhaustive over R
    b2 = bridge(np_, "b2", {"world"})
    st2 = store + [b1, b2]
    nog2 = nog + (frozenset({"b1", "b2"}),)
    table = 0
    for R in subsets({"t1", "t2", "b1", "b2"}):
        v, why = machine_verdict(st2, p, np_, R, nog2)
        both = liveness(b1["iv"], R) == LIVE and liveness(b2["iv"], R) == LIVE
        assert (why == "CONTRADICTION_ACTIVE") == both and (v == UNKNOWN if both else v == liveness(b1["iv"], R))
        assert machine_verdict(st2, np_, p, R, nog2)[0] == (UNKNOWN if both else liveness(b2["iv"], R))
        table += 1
    # disjoint scopes (epochs): no contradiction — each LIVE on its own scope
    st3 = store + [bridge(p, "b1", {"epoch1"}), bridge(np_, "b2", {"epoch2"})]
    assert machine_verdict(st3, p, np_, set()) == (LIVE, "OWN_INTERVAL") and machine_verdict(st3, np_, p, set()) == (LIVE, "OWN_INTERVAL")
    # (iv) retraction of one record: contradiction inactive; the survivor is still not machine knowledge
    R_ret = {"t2"}
    assert records_active(store, R_ret) == {"t1"} and machine_verdict(store, p, np_, R_ret) == (UNKNOWN, "OWN_INTERVAL") and history_digest(store) == h0
    # (v) supersession (B5): u1 corrects Tuesday → Wednesday at t=3; Γ_time ends t1; dependents reopen exactly
    atoms = {"c_tue": t1["iv"], "c_not_tue": t2["iv"], "venue": cert({"e_v"}), "plan": cert({"t1", "e_v"}), "other_entity": cert({"e_o"}), "note": cert({"e_o"}), "gaz": cert({"e_gaz"})}
    edges = [edge("tue_plan", "c_tue", "plan", rel="COMPOSITION"), edge("venue_plan", "venue", "plan", rel="COMPOSITION"), edge("o_note", "other_entity", "note", rel="DEPENDENCE")]
    epochs = {"t1": (1, 3), "t2": (1, float("inf")), "e_v": (0, float("inf")), "e_o": (0, float("inf")), "e_gaz": (0, float("inf"))}
    R2, R3 = frozenset(e for e, (_, d) in epochs.items() if d <= 2), frozenset(e for e, (_, d) in epochs.items() if d <= 3)
    rep = reopening_report(atoms, edges, R2, R3)
    assert R3 == {"t1"} and rep["reopen"] == {"c_tue", "plan"} and rep["unaffected"] >= {"venue", "other_entity", "note", "gaz", "c_not_tue"}
    assert records_active(store, R3) == {"t2"} and machine_verdict(store, p, np_, R3) == (UNKNOWN, "OWN_INTERVAL") and history_digest(store) == h0
    # the four hostiles of M4 §5 as mutants
    edited = [dict(a) for a in store]
    edited[0]["ev"] = "t1_edited"                                          # (1) correction rewrites history
    assert history_digest(edited) != h0
    cached_plan = liveness(atoms["plan"], R2)                              # (2) stale cached answer
    assert cached_plan == LIVE and liveness(atoms["plan"], R3) == DEAD
    R3_bad = R3 | {"e_o"}                                                  # (3) correction touches an unrelated entity
    rep_bad = reopening_report(atoms, edges, R2, R3_bad)
    assert rep_bad["reopen"] > rep["reopen"] and "note" in rep_bad["reopen"] and "note" in rep["unaffected"]
    gaz_store = store + [bridge("paris_in_france", "e_gaz", {"world"})]     # (4) retraction of an unadmitted record moves world knowledge
    before = machine_verdict(gaz_store, "paris_in_france", "not:paris_in_france", {"t1"})
    assert before[0] == LIVE and machine_verdict(gaz_store, "paris_in_france", "not:paris_in_france", {"t1", "e_gaz"})[0] == DEAD  # the mutant revokes e_gaz with t1
    assert machine_verdict(gaz_store, "paris_in_france", "not:paris_in_france", {"t1", "t2"})[0] == LIVE                            # honest retraction: unchanged
    return {"records_live_neither_promoted": 1, "composite_dead_parts_intact": 1, "majority_checks": majority_checks, "mutant_majority_resolves_caught": 1, "scoped_bridge_resolves_on_scope": 1, "two_bridge_verdict_table": table, "disjoint_scopes_no_contradiction": 1, "retraction_no_laundering": 1, "supersession_reopen": sorted(rep["reopen"]), "hostile_history_rewrite_caught": 1, "hostile_stale_cache_caught": 1, "hostile_unrelated_touched_caught": 1, "hostile_retraction_moves_world_caught": 1}


# ---------------------------------------------------------------------------------------------
# C8 · MEG-21 · non-quotient representation lifts (admissible ι, exact rollback, M4 affine→quadratic)
# ---------------------------------------------------------------------------------------------


def outcome(K, q, R):
    """Four-valued outcome of query q = (seeds, target) on K."""
    atoms, edges = K
    seeds, tgt = q
    if tgt not in atoms or any(s not in atoms for s in seeds):
        return (GAP, None)
    if liveness(atoms[tgt][1], R) == DEAD:
        return (OBSTRUCTION, None)
    r = kleene_reach({x: iv for x, (_, iv) in atoms.items()}, edges, seeds, R)
    return ({LIVE: FOUND, DEAD: GAP, UNKNOWN: CANNOT}[r[tgt]], atoms[tgt][0] if r[tgt] == LIVE else None)


def admissible(K, K2, iota, Q, gammas):
    atoms, edges = K
    atoms2, edges2 = K2
    if len(set(iota.values())) != len(iota) or set(iota) != set(atoms):
        return "REFUSED:NOT_INJECTIVE_OR_PARTIAL"
    for x in atoms:
        if iota[x] not in atoms2 or atoms2[iota[x]][1] != atoms[x][1]:
            return "REFUSED:INTERVAL_CHANGED"
        if atoms2[iota[x]][0] != atoms[x][0]:
            return "REFUSED:CONTENT_CHANGED"
    for eid, tails, heads, ew, rel in edges:
        if not any(set(t2) == {iota[t] for t in tails} and set(h2) == {iota[h] for h in heads} and ew2 == ew and rel2 == rel for _, t2, h2, ew2, rel2 in edges2):
            return "REFUSED:NOT_A_HOMOMORPHISM"
    for x in atoms:
        for R in gammas:
            if liveness(atoms2[iota[x]][1], R) != liveness(atoms[x][1], R):
                return "REFUSED:SIGNATURE_CHANGED"
    for q in Q:
        q2 = (tuple(iota[s] for s in q[0]), iota.get(q[1], q[1]))
        for R in gammas:
            o1, o2 = outcome(K, q, R), outcome(K2, q2, R)
            if o1[0] == FOUND and o2 != o1:
                return "REFUSED:FOUND_OUTCOME_CHANGED"
            if o1[0] != FOUND and o2[0] not in (o1[0], FOUND):
                return "REFUSED:OUTCOME_DEGRADED"
    return "ADMISSIBLE"


def rollback(K2, iota, K):
    """Revoke e_J and quarantine the added structure: the image restricted to ι(K) is K byte-identically."""
    atoms2, edges2 = K2
    inv = {v: k for k, v in iota.items()}
    atoms = {inv[x]: attr for x, attr in atoms2.items() if x in inv}
    edges = [(eid, tuple(inv[t] for t in tails), tuple(inv[h] for h in heads), ew, rel) for eid, tails, heads, ew, rel in edges2 if all(t in inv for t in tails) and all(h in inv for h in heads)]
    return digest([sorted(atoms.items(), key=lambda kv: kv[0]), sorted(edges)]) == digest([sorted(K[0].items(), key=lambda kv: kv[0]), sorted(K[1])])


def xor_span(features):
    return frozenset(tuple(sum(c * f[i] for c, f in zip(coeffs, features)) % 2 for i in range(4)) for coeffs in itertools.product((0, 1), repeat=len(features)))


def check_c8_meg21_representation_lifts():
    F1, FA, FB, FAB = (1, 1, 1, 1), (0, 0, 1, 1), (0, 1, 0, 1), (0, 0, 0, 1)
    affine, quad = xor_span([F1, FA, FB]), xor_span([F1, FA, FB, FAB])
    assert len(affine) == 8 and FAB not in affine and len(quad) == 16 and FAB in quad
    # K: affine repertoire; atoms carry (content, interval); content of h_t = coefficient vector
    def coeffs(t, feats):
        return next(c for c in itertools.product((0, 1), repeat=len(feats)) if tuple(sum(a * f[i] for a, f in zip(c, feats)) % 2 for i in range(4)) == t)
    atoms = {"seed": (None, IONE), "phi_aff": ("affine", cert({"r1", "r2", "r3"}))}
    edges = [edge("seed_phi", "seed", "phi_aff", rel="DEPENDENCE")]
    for t in sorted(affine):
        name = "h_" + "".join(map(str, t))
        atoms[name] = (coeffs(t, [F1, FA, FB]) + (0,), cert({"r" + str(1 + t.index(1) if 1 in t else 1)}))
        edges.append(edge("phi_" + name, "phi_aff", name, rel="COMPOSITION"))
    K = (atoms, edges)
    Q = [(("seed",), x) for x in atoms if x.startswith("h_")] + [(("seed",), "h_0001")]
    gammas = (frozenset(), frozenset({"r1"}), frozenset({"r2"}), frozenset({"r3"}))   # Γ ⊆ 2^E(K) (S4)
    # honest lift: same atoms (coefficient vectors already carry the zero ab-coefficient), new feature and AND
    atoms2 = dict(atoms)
    atoms2["phi_quad"] = ("quadratic", cert({"r1", "r2", "r3", "r4"}))
    atoms2["h_0001"] = (coeffs(FAB, [F1, FA, FB, FAB]), cert({"r4"}))
    edges2 = list(edges) + [edge("seed_phiq", "seed", "phi_quad", rel="DEPENDENCE"), edge("phiq_h0001", "phi_quad", "h_0001", rel="COMPOSITION")]
    iota = {x: x for x in atoms}
    K2 = (atoms2, edges2)
    assert admissible(K, K2, iota, Q, gammas) == "ADMISSIBLE" and rollback(K2, iota, K)
    assert outcome(K, (("seed",), "h_0001"), frozenset())[0] == GAP and outcome(K2, (("seed",), "h_0001"), frozenset())[0] == FOUND   # the obstructed query improves
    found_preserved = sum(1 for q in Q for R in gammas if outcome(K, q, R)[0] == FOUND and outcome(K2, q, R) == outcome(K, q, R))
    # planted lifts
    bad = (dict(atoms2), edges2)
    bad[0]["h_0110"] = (atoms2["h_0110"][0], cert({"r2"}, {"r4"}))          # changes one liveness signature (under R = {r2})
    assert liveness(bad[0]["h_0110"][1], {"r2"}) != liveness(atoms["h_0110"][1], {"r2"}) and admissible(K, bad, iota, Q, gammas) == "REFUSED:INTERVAL_CHANGED"
    bad = (dict(atoms2), edges2)
    bad[0]["h_0110"] = ((1, 1, 1, 1), atoms2["h_0110"][1])                     # changes a FOUND answer's content
    assert admissible(K, bad, iota, Q, gammas) == "REFUSED:CONTENT_CHANGED"
    bad = (atoms2, [e for e in edges2 if e[0] != "phi_h_0110"])                 # degrades a FOUND query to GAP
    assert outcome(bad, (("seed",), "h_0110"), frozenset())[0] == GAP and admissible(K, bad, iota, Q, gammas) == "REFUSED:NOT_A_HOMOMORPHISM"
    merged = dict(iota)
    merged["h_0110"] = "h_1001"                                                # quotient move: two atoms identified
    assert admissible(K, K2, merged, Q, gammas) == "REFUSED:NOT_INJECTIVE_OR_PARTIAL"
    # a lift may not silently change an outcome even with intervals intact: extra edge makes GAP→FOUND on Q is allowed,
    # but a lift dropping a seed reachability while keeping intervals is refused
    bad_edges = [e if e[0] != "seed_phi" else edge("seed_phi", "seed", "phi_aff", iv=(canon([frozenset({"r9"})]), ONE), rel="DEPENDENCE") for e in edges2]
    assert admissible(K, (atoms2, bad_edges), iota, Q, gammas) == "REFUSED:NOT_A_HOMOMORPHISM"
    # exhaustive small case: every injective map of a 2-atom K into a 3-atom K' family; admissibility is decided
    # by the finite predicate and every admissible candidate rolls back exactly
    small = ({"a": ("x", cert({"e"})), "b": ("y", cert({"f"}))}, [edge("ab", "a", "b", rel="DEPENDENCE")])
    Qs = [(("a",), "b")]
    gs = (frozenset(), frozenset({"e"}), frozenset({"f"}))
    candidates = admitted = refused = 0
    names = ("a", "b", "c")
    for d_iv in (cert({"g"}), IUNKNOWN, cert({"e"})):
        for extra in subsets([("a", "c"), ("c", "b"), ("b", "c"), ("c", "a")]):
            atoms3 = {"a": ("x", cert({"e"})), "b": ("y", cert({"f"})), "c": ("z", d_iv)}
            edges3 = [edge("ab", "a", "b", rel="DEPENDENCE")] + [edge(f"{t}{h}", t, h, rel="DEPENDENCE") for t, h in sorted(extra)]
            for img in itertools.permutations(names, 2):
                io = {"a": img[0], "b": img[1]}
                verdict = admissible(small, (atoms3, edges3), io, Qs, gs)
                candidates += 1
                if verdict == "ADMISSIBLE":
                    admitted += 1
                    assert rollback((atoms3, edges3), io, small)
                else:
                    refused += 1
    assert admitted > 0 and refused > 0
    return {"affine_span": len(affine), "quadratic_span": len(quad), "m4_lift_admissible": 1, "m4_rollback_exact": 1, "found_outcomes_preserved": found_preserved, "obstructed_query_improves": 1, "mutant_signature_change_refused": 1, "mutant_content_change_refused": 1, "mutant_degrading_lift_refused": 1, "mutant_quotient_merge_refused": 1, "mutant_edge_interval_change_refused": 1, "small_candidates": candidates, "small_admitted": admitted, "small_refused": refused}


# ---------------------------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------------------------

CHECKS = {
    "C1_MEG33_epistemic_action_value": check_c1_meg33_epistemic_action_value,
    "C2_MEG25_commitment_gate": check_c2_meg25_commitment_gate,
    "C3_MEG27_prefix_commitment": check_c3_meg27_prefix_commitment,
    "C4_MEG11_pipeline_semantics": check_c4_meg11_pipeline_semantics,
    "C5_MEG10_procedure_algebra_laws": check_c5_meg10_procedure_algebra_laws,
    "C6_MEG15_discriminating_interaction": check_c6_meg15_discriminating_interaction,
    "C7_MEG16_contradiction_policy": check_c7_meg16_contradiction_policy,
    "C8_MEG21_representation_lifts": check_c8_meg21_representation_lifts,
}


def run_all():
    out = {name: fn() for name, fn in CHECKS.items()}
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
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
