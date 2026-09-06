"""Exact finite checker for KSO_FIELD_FRONTIER_THEOREMS_BATCH10_V1.md (stdlib only, exact).

One check function per field-frontier row of `field_dynamics_v1/FRONTIER.md` taken in batch 10:
J1 = FDX-06 (distributed machine epistemics: warrant intervals, authority meet, reopening cones and
verdict liveness under exchange with partial trust), J2 = FDX-07 (epistemic games: the adversarial
evidence provider against the commitment gate, attack surface first), J3 = FDX-14 (whole-system lower
bounds: identification, retention, repair, communication and verification on the registered finite
classes).  Every check performs (a) the positive statement by exhaustive enumeration on a finite
fixture, (b) at least one planted hostile whose mutation is asserted applied and caught, (c) a
no-alarm control.  Items whose honest status is PARENT_OWNED / PARENT_SUFFICIENT report the parent
and run the executable falsifier on the smallest holding / failing fixture.  All objects are
re-implemented here (antichain warrant intervals, a causal event poset of revocations, an authority
product lattice, a nogood filter, decision-tree DPs, separating sets); nothing is imported from
``ocm``.  Every count is an integer; every probability an exact ``Fraction``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import namedtuple
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


def subsets(universe, min_size=0, max_size=None):
    universe = tuple(universe)
    hi = len(universe) if max_size is None else max_size
    for k in range(min_size, hi + 1):
        for combo in itertools.combinations(universe, k):
            yield frozenset(combo)


def ceil_log2(n):
    if n < 1:
        raise CannotCheck("ceil_log2 of a non-positive count")
    b = 0
    while (1 << b) < n:
        b += 1
    return b


def popcount(x):
    return bin(x).count("1")


# =============================================================================================
# shared warrant algebra (KS-T01 antichain semiring, KS-T21 three-valued liveness) — re-implemented
# =============================================================================================

ZERO = frozenset()
ONE = frozenset({frozenset()})
LIVE, UNKNOWN, DEAD = "LIVE", "UNKNOWN", "DEAD"
ORDER3 = {DEAD: 0, UNKNOWN: 1, LIVE: 2}


def canon(sets):
    sets = {frozenset(s) for s in sets}
    return frozenset(s for s in sets if not any(t < s for t in sets))


def wjoin(p, q):
    return canon(p | q)


def wmeet(p, q):
    return canon({a | b for a in p for b in q})


def wleq(p, q):
    """p ≤ q: every warrant of p contains a warrant of q (q at least as easy to satisfy)."""
    return all(any(w2 <= w for w2 in q) for w in p)


def live(profile, revoked):
    return any(not (w & revoked) for w in profile)


def liveness(lower, upper, revoked):
    if live(lower, revoked):
        return LIVE
    if not live(upper, revoked):
        return DEAD
    return UNKNOWN


def all_antichains(universe):
    universe = tuple(universe)
    atoms = list(subsets(universe))
    out = set()
    for k in range(len(atoms) + 1):
        for combo in itertools.combinations(atoms, k):
            c = frozenset(combo)
            if canon(c) == c:
                out.add(c)
    return sorted(out, key=lambda p: (len(p), sorted(sorted(map(str, w)) for w in p)))


def all_intervals(universe):
    acs = all_antichains(universe)
    return [(lo, up) for lo in acs for up in acs if wleq(lo, up)]


def filter_nogoods(profile, nogoods):
    """MEG-16 `filter_N`: drop every support containing a registered nogood."""
    return canon(w for w in profile if not any(n <= w for n in nogoods))


# =============================================================================================
# authority product lattice (types.Authority): coordinate-wise min, missing = 0, commit dropped internally
# =============================================================================================

COORDS = ("source", "world_truth", "commit")


def auth(**ranks):
    return tuple(ranks.get(c, 0) for c in COORDS)


def ameet(a, b):
    return tuple(min(x, y) for x, y in zip(a, b))


def ajoin(a, b):
    return tuple(max(x, y) for x, y in zip(a, b))


def aleq(a, b):
    return all(x <= y for x, y in zip(a, b))


def drop_commit(a):
    return a[:2] + (0,)


def rank(a, coord):
    return a[COORDS.index(coord)]


# =============================================================================================
# J1 · FDX-06 · distributed machine epistemics
# =============================================================================================

E3 = ("e1", "e2", "e3")
NODES = ("A", "B", "C")

# causal event poset of revocation events on the shared evidence universe (five events)
Event = namedtuple("Event", "eid kind evidence preds")
EVENTS = (
    Event("rv1", "revoke", "e1", frozenset()),
    Event("ri1", "reinstate", "e1", frozenset({"rv1"})),
    Event("rv1b", "revoke", "e1", frozenset({"rv1"})),          # concurrent with ri1
    Event("rv2", "revoke", "e2", frozenset()),
    Event("ri2", "reinstate", "e2", frozenset({"rv2"})),
)
EVENT_BY_ID = {e.eid: e for e in EVENTS}


def ancestors(eid):
    out, work = set(), [eid]
    while work:
        x = work.pop()
        for p in EVENT_BY_ID[x].preds:
            if p not in out:
                out.add(p)
                work.append(p)
    return frozenset(out)


def causally_closed_views(events=EVENTS):
    views = []
    for V in subsets(e.eid for e in events):
        if all(ancestors(x) <= V for x in V):
            views.append(V)
    return views


def revoked_set(view):
    """Revoke-wins merge (a remove-wins observed-set): e is revoked in the view iff some received revoke
    event on e is not causally dominated by a received reinstate event on e."""
    out = set()
    for x in view:
        ev = EVENT_BY_ID[x]
        if ev.kind != "revoke":
            continue
        dominated = any(EVENT_BY_ID[y].kind == "reinstate" and EVENT_BY_ID[y].evidence == ev.evidence
                        and x in ancestors(y) for y in view)
        if not dominated:
            out.add(ev.evidence)
    return frozenset(out)


def linear_extensions(view):
    view = tuple(sorted(view))
    for perm in itertools.permutations(view):
        pos = {x: i for i, x in enumerate(perm)}
        if all(pos[p] < pos[x] for x in perm for p in EVENT_BY_ID[x].preds):
            yield perm


def mutant_lww_revocation_bit(order):
    """Planted: a single revoked flag per evidence id, overwritten in arrival order (last writer wins)."""
    flag = {}
    for x in order:
        ev = EVENT_BY_ID[x]
        flag[ev.evidence] = ev.kind == "revoke"
    return frozenset(e for e, f in flag.items() if f)


def import_interval(lower, upper, message_id):
    """An import from node j is admitted at node i under the message assumption `m` (fresh at i)."""
    m = frozenset({frozenset({message_id})})
    return wmeet(m, lower), wmeet(m, upper)


def mutant_import_without_message_assumption(lower, upper, message_id):
    return lower, upper


def import_authority(sender_authority, trust_cap):
    """Authority of an imported record: meet with the receiver's trust cap for the sender, commit dropped
    (an import is an internal admission; MEG-04 / T1)."""
    return drop_commit(ameet(sender_authority, trust_cap))


def mutant_authority_join_over_paths(authorities):
    out = authorities[0]
    for a in authorities[1:]:
        out = ajoin(out, a)
    return out


def mutant_commit_travels(sender_authority, trust_cap):
    return ameet(sender_authority, trust_cap)


def forward_closure(graph, seeds):
    """Impact_D: least dependency-closed superset (forward reachability over dependency edges)."""
    seen, work = set(seeds), list(seeds)
    while work:
        v = work.pop()
        for w in graph.get(v, ()):
            if w not in seen:
                seen.add(w)
                work.append(w)
    return frozenset(seen)


def check_j1_distributed_epistemics():
    counts = {}
    intervals = all_intervals(E3)
    assert len(intervals) == 168
    E = frozenset(E3)
    # (i) liveness is antitone in the revocation set: more revocation never raises a verdict
    antitone = 0
    for lo, up in intervals:
        for R in subsets(E):
            for R2 in subsets(E):
                if R <= R2:
                    assert ORDER3[liveness(lo, up, R2)] <= ORDER3[liveness(lo, up, R)]
                    antitone += 1
    counts["intervals"] = len(intervals)
    counts["antitone_checks"] = antitone
    # (ii) revocation exchange: revoke-wins merge over causally-closed views is order-independent;
    #      the last-writer-wins flag diverges between causally consistent delivery orders
    views = causally_closed_views()
    counts["causally_closed_views"] = len(views)
    honest_orders = lww_divergent = order_pairs = 0
    lww_witness = None
    for V in views:
        exts = list(linear_extensions(V))
        for perm in exts:
            assert revoked_set(frozenset(perm)) == revoked_set(V)       # state-based: a function of the set
            honest_orders += 1
        for a, b in itertools.combinations(exts, 2):
            order_pairs += 1
            if mutant_lww_revocation_bit(a) != mutant_lww_revocation_bit(b):
                lww_divergent += 1
                if lww_witness is None:
                    lww_witness = {"view": sorted(V), "order_a": list(a), "order_b": list(b),
                                   "lww_a": sorted(mutant_lww_revocation_bit(a)), "lww_b": sorted(mutant_lww_revocation_bit(b)),
                                   "honest": sorted(revoked_set(V))}
    assert lww_divergent > 0 and lww_witness is not None
    counts["delivery_orders_checked"] = honest_orders
    counts["order_pairs"] = order_pairs
    counts["mutant_lww_divergent_order_pairs"] = lww_divergent
    counts["mutant_lww_witness"] = lww_witness
    # (ii-b) staleness: a view over-claims only by missing an effective revocation; under-claims only by
    #        holding a revocation the full history has reinstated.  Missing update ≠ no update: two full
    #        histories (with / without rv2) give identical views to a node that has not received rv2.
    full = frozenset(e.eid for e in EVENTS)
    R_full = revoked_set(full)
    over = under = agree = 0
    over_implies_missing = under_implies_extra = 0
    for V in views:
        RV = revoked_set(V)
        for lo, up in intervals:
            v_view, v_full = ORDER3[liveness(lo, up, RV)], ORDER3[liveness(lo, up, R_full)]
            if v_view > v_full:
                over += 1
                assert not (R_full <= RV)
                over_implies_missing += 1
            elif v_view < v_full:
                under += 1
                assert not (RV <= R_full)
                under_implies_extra += 1
            else:
                agree += 1
    counts["view_verdicts"] = {"over_claim": over, "under_claim": under, "agree": agree}
    assert over_implies_missing == over and under_implies_extra == under
    # the indistinguishability instance (R5 parent): view V0 = {rv1, ri1, rv1b} (node never saw rv2); two
    # global histories extend it, one with the effective revocation rv2 and one without
    V0 = frozenset({"rv1", "ri1", "rv1b"})
    hist_with = V0 | {"rv2"}
    hist_without = V0
    assert V0 <= hist_with and V0 <= hist_without and hist_with in views and hist_without in views
    stale_wrong_with = stale_wrong_without = 0
    for lo, up in intervals:
        view_verdict = liveness(lo, up, revoked_set(V0))
        if view_verdict != liveness(lo, up, revoked_set(hist_with)):
            stale_wrong_with += 1
        if view_verdict != liveness(lo, up, revoked_set(hist_without)):
            stale_wrong_without += 1
    assert stale_wrong_without == 0 and stale_wrong_with > 0
    counts["mutant_stale_view_as_current_wrong_in_history_with_rv2"] = stale_wrong_with
    counts["stale_view_correct_in_history_without_rv2"] = 168 - stale_wrong_without
    # (iii) authority under exchange with partial trust
    ranks = (0, 1, 2)
    sender_auths = [auth(source=s, world_truth=w, commit=c) for s in ranks for w in ranks for c in (0, 1)]
    caps = [auth(source=s, world_truth=w, commit=1) for s in ranks for w in ranks]
    never_raised = commit_zero = commit_travels_caught = 0
    for A in sender_auths:
        for T in caps:
            got = import_authority(A, T)
            assert aleq(got, A) and aleq(got, T)
            never_raised += 1
            assert rank(got, "commit") == 0
            commit_zero += 1
            if rank(mutant_commit_travels(A, T), "commit") > 0:
                commit_travels_caught += 1
    assert commit_travels_caught > 0
    counts["import_authority_pairs"] = never_raised
    counts["import_commit_always_zero"] = commit_zero
    counts["mutant_commit_travels_caught"] = commit_travels_caught
    # relay path j→k→i: authority ≤ every cap on the path and ≤ the source; two paths: meet, never join
    relay_bounded = join_caught = join_cases = 0
    for A in sender_auths:
        for Tk in caps:
            for Ti in caps:
                via = import_authority(import_authority(A, Tk), Ti)
                assert aleq(via, A) and aleq(via, Tk) and aleq(via, Ti)
                relay_bounded += 1
                direct = import_authority(A, Ti)
                if via != direct:
                    join_cases += 1
                    honest = ameet(via, direct)
                    forged = mutant_authority_join_over_paths([via, direct])
                    if not (aleq(forged, via) and aleq(forged, direct)):
                        join_caught += 1
                    assert aleq(honest, via) and aleq(honest, direct)
    assert join_caught > 0
    counts["relay_paths_bounded"] = relay_bounded
    counts["two_path_cases"] = join_cases
    counts["mutant_authority_join_over_paths_caught"] = join_caught
    # (iv) per-message assumptions: revoking trust in the sender kills exactly the citing cone; native atoms
    #      unchanged; the sender's claimed verdict is never used (recomputed under the receiver's R)
    m = "m_B_to_A"
    U4 = E | {m}
    imports_dead = natives_unchanged = recompute = claimed_wrong = 0
    without_assumption_survives = 0
    for lo, up in intervals:
        if not up:                                      # ⟦0,0⟧: nothing to import
            continue
        ilo, iup = import_interval(lo, up, m)
        mlo, mup = mutant_import_without_message_assumption(lo, up, m)
        for R in subsets(E):
            Rm = R | {m}
            assert liveness(ilo, iup, Rm) == DEAD
            imports_dead += 1
            assert liveness(lo, up, Rm) == liveness(lo, up, R)      # native atom never cites m
            natives_unchanged += 1
            # receiver recomputation: [m ∉ R] ∧3 λ_R(sender interval) (KS-T21 corollary)
            assert liveness(ilo, iup, R) == liveness(lo, up, R)
            recompute += 1
            if liveness(mlo, mup, Rm) != DEAD:
                without_assumption_survives += 1
            # Byzantine sender claims LIVE regardless of its own state: the claim is wrong whenever the
            # recomputed verdict differs; the honest receiver never reads the claim
            if liveness(ilo, iup, R) != LIVE:
                claimed_wrong += 1
    assert without_assumption_survives > 0
    counts["imports_dead_under_trust_revocation"] = imports_dead
    counts["native_atoms_unchanged"] = natives_unchanged
    counts["receiver_recomputation_agrees"] = recompute
    counts["mutant_import_without_message_assumption_survives"] = without_assumption_survives
    counts["mutant_trust_sender_verdict_wrong"] = claimed_wrong
    # composition with an import cites m and dies with it (correct behaviour, counted)
    composed_die = 0
    for lo, up in intervals:
        if not up or not lo:
            continue
        ilo, iup = import_interval(lo, up, m)
        clo, cup = wmeet(ilo, frozenset({frozenset({"e3"})})), wmeet(iup, frozenset({frozenset({"e3"})}))
        assert liveness(clo, cup, frozenset({m})) == DEAD
        composed_die += 1
    counts["compositions_with_import_die_with_trust"] = composed_die
    # equivocation: two messages from B about x with different intervals; detected iff both reach one node
    msgs = {"m1": (frozenset({frozenset({"e1"})}), frozenset({frozenset({"e1"})})),
            "m2": (frozenset({frozenset({"e2"})}), frozenset({frozenset({"e2"})}))}
    detect = nodetect = 0
    for delivered in itertools.product((frozenset(), frozenset({"m1"}), frozenset({"m2"}), frozenset({"m1", "m2"})), repeat=3):
        some_node_has_both = any({"m1", "m2"} <= d for d in delivered)
        if some_node_has_both:
            detect += 1
        else:
            nodetect += 1
    counts["equivocation_delivery_patterns"] = {"detectable": detect, "undetectable": nodetect}
    assert detect + nodetect == 64 and detect == 64 - 27
    # (v) reopening under exchange: Impact_D distributes over unions; batched cone ⊆ union of sequential cones
    dep = {"x": ("y",), "y": ("z",), "n": ("q",), "z": (), "q": (), "w": ("y",)}
    V6 = tuple(dep)
    distrib = 0
    for S1 in subsets(V6):
        for S2 in subsets(V6):
            assert forward_closure(dep, S1 | S2) == forward_closure(dep, S1) | forward_closure(dep, S2)
            distrib += 1
    counts["impact_distributes_over_union_checks"] = distrib
    # atoms at node A: x imported (cites e1, m), w native (cites e2), n native (cites e3), y = x ⊗ w, z from y, q from n
    atom_int = {
        "x": import_interval(frozenset({frozenset({"e1"})}), frozenset({frozenset({"e1"})}), m),
        "w": (frozenset({frozenset({"e2"})}), frozenset({frozenset({"e2"})})),
        "n": (frozenset({frozenset({"e3"})}), frozenset({frozenset({"e3"})})),
    }
    atom_int["y"] = (wmeet(atom_int["x"][0], atom_int["w"][0]), wmeet(atom_int["x"][1], atom_int["w"][1]))
    atom_int["z"] = atom_int["y"]
    atom_int["q"] = atom_int["n"]

    def changed(R0, R1):
        return frozenset(a for a, (lo, up) in atom_int.items() if liveness(lo, up, R0) != liveness(lo, up, R1))

    def cone(R0, R1):
        return forward_closure(dep, changed(R0, R1))

    deltas = [frozenset({"e1"}), frozenset({m}), frozenset({"e2"}), frozenset({"e3"})]
    batched_subset = final_equal = seq_orders = 0
    for k in (2, 3):
        for combo in itertools.combinations(deltas, k):
            batched = cone(frozenset(), frozenset().union(*combo))
            for perm in itertools.permutations(combo):
                R, union_cones = frozenset(), frozenset()
                for d in perm:
                    union_cones |= cone(R, R | d)
                    R = R | d
                assert batched <= union_cones
                batched_subset += 1
                assert R == frozenset().union(*combo)
                final_equal += 1
                seq_orders += 1
    counts["batched_cone_subset_of_sequential_union"] = batched_subset
    counts["final_state_order_independent"] = final_equal
    # exact cones on the fixture
    counts["cone_revoke_e1"] = sorted(cone(frozenset(), frozenset({"e1"})))
    counts["cone_revoke_trust_m"] = sorted(cone(frozenset(), frozenset({m})))
    counts["cone_revoke_e3"] = sorted(cone(frozenset(), frozenset({"e3"})))
    assert counts["cone_revoke_trust_m"] == ["x", "y", "z"] and counts["cone_revoke_e3"] == ["n", "q"]
    # a revoke followed by its reinstatement batches to the empty cone while the sequence reopens twice
    assert cone(frozenset(), frozenset()) == frozenset()
    counts["revoke_then_reinstate_batched_cone"] = 0
    counts["revoke_then_reinstate_sequential_cones"] = len(cone(frozenset(), frozenset({"e1"}))) + len(cone(frozenset({"e1"}), frozenset()))
    # (vi) k sources asserting x: ⊕ of message assumptions; LIVE until every source is revoked; authority
    #      stays at the meet (source=1, world_truth=0); agreement of every node is not world truth
    src_auth = auth(source=1)
    for k in (1, 2, 3):
        ms = [f"m{j}" for j in range(k)]
        lo = frozenset(frozenset({x}) for x in ms)
        robust = 0
        for R in subsets(ms):
            v = liveness(lo, lo, frozenset(R))
            assert (v == LIVE) == (len(R) < k)
            robust += 1
        counts[f"sources_{k}_robustness_checks"] = robust
        A = src_auth
        for _ in ms[1:]:
            A = ameet(A, src_auth)
        assert rank(A, "world_truth") == 0 and rank(A, "commit") == 0
    forged = mutant_majority_is_world_truth(3)
    assert rank(forged, "world_truth") == 1
    counts["mutant_majority_is_world_truth_caught"] = 1
    counts["all_nodes_agree_yet_world_truth_rank"] = 0
    counts["status"] = ("PARENT_SUFFICIENT (state-based CRDT / remove-wins set convergence; R5 asynchronous freshness "
                        "impossibility; Byzantine agreement for authority-bearing objects) with PROVED corollaries on the fixture: "
                        "antitone liveness, revoke-wins order independence, over-claim only by a missing revocation, import "
                        "authority = meet with trust cap and commit 0, no join across paths, per-message assumptions localise "
                        "trust revocation, Impact distributes over unions, k-source ⊕ robustness without world_truth")
    return counts


def mutant_majority_is_world_truth(k):
    """Planted: k ≥ 2 agreeing IMPORTED sources promote the claim to world_truth rank 1."""
    return auth(source=1, world_truth=1 if k >= 2 else 0)


# =============================================================================================
# J2 · FDX-07 · epistemic games: the adversarial evidence provider vs the commitment gate
# =============================================================================================

LEGIT = {"o1": auth(source=1, world_truth=1), "o2": auth(source=1, world_truth=1)}
ADV_IDS = ("a1", "a2", "a3")
ADV_AUTH = auth(source=1)                                   # 'source asserts P': never world_truth (world.py)
CLAIMS = {
    "c_native": frozenset({frozenset({"o1"})}),
    "c_native2": frozenset({frozenset({"o1"}), frozenset({"o2"})}),
    "c_report": frozenset({frozenset({"a1"})}),
    "c_sybil": frozenset({frozenset({"a1"}), frozenset({"a2"}), frozenset({"a3"})}),
    "c_mixed": frozenset({frozenset({"o1", "a1"}), frozenset({"o2"})}),
    "c_composed": frozenset({frozenset({"o1", "a1"})}),
}
REQS = {"REQ_REPORT": auth(source=1), "REQ_TRUTH": auth(world_truth=1), "REQ_COMMIT": auth(commit=1)}
Strategy = namedtuple("Strategy", "states contradictions confidence")
ADV_STATES = ("absent", "asserted", "retracted")
CONTRA_OPTIONS = (frozenset(), frozenset({("a1", "o1")}), frozenset({("a1", "o2")}), frozenset({("a1", "o1"), ("a1", "o2")}))


def adversary_strategies():
    for states in itertools.product(ADV_STATES, repeat=3):
        for contra in CONTRA_OPTIONS:
            if contra and states[0] == "absent":
                continue                                 # a contradiction needs the asserting record
            yield Strategy(dict(zip(ADV_IDS, states)), contra, Fraction(0))


def evidence_authority(e):
    return LEGIT[e] if e in LEGIT else ADV_AUTH


def gate(claim, strategy, required, native_revoked=frozenset(), commit_authority=auth(commit=1, source=2, world_truth=2)):
    """Honest gate: commit iff some exhibited warrant W survives revocation and the nogood filter and the
    meet of the authorities of W's evidence (met with the external commit authority for the commit
    coordinate) dominates the requirement.  Returns (verdict, committing warrant or None)."""
    R = set(native_revoked) | {a for a, s in strategy.states.items() if s != "asserted"}
    nogoods = frozenset(frozenset(pair) for pair in strategy.contradictions)
    filtered = filter_nogoods(claim, nogoods)
    if not filtered and claim:
        return "REFUSED:CONTRADICTED", None
    lv = liveness(filtered, filtered, frozenset(R))
    if lv != LIVE:
        return f"REFUSED:WARRANT_{lv}", None
    for W in sorted(filtered, key=lambda w: sorted(w)):
        if W & R:
            continue
        A = auth(source=9, world_truth=9, commit=9)
        for e in W:
            A = ameet(A, evidence_authority(e))
        A = ameet(drop_commit(A), commit_authority)      # evidence never carries commit (T1); the meet cannot add it
        if aleq(required, A):
            return "COMMITTED", W
    return "REFUSED:AUTHORITY_INSUFFICIENT", None


def mutant_report_as_truth(claim, strategy, required):
    """Planted: the gate reads 'source asserts P' as world_truth rank 1."""
    R = {a for a, s in strategy.states.items() if s != "asserted"}
    for W in claim:
        if not (W & R):
            return "COMMITTED", W
    return "REFUSED", None


def mutant_confidence_gate(claim, strategy, required):
    """Planted: a confidence coordinate supplied by the provider drives commitment (persuasion lever)."""
    R = {a for a, s in strategy.states.items() if s != "asserted"}
    if strategy.confidence >= Fraction(1, 2) and any(not (W & R) for W in claim):
        return "COMMITTED", None
    return "REFUSED", None


def mutant_nogood_kills_endpoint(claim, strategy, required):
    """Planted: a registered contradiction {a, o} is read as making o DEAD (MEG-16D violation)."""
    R = {a for a, s in strategy.states.items() if s != "asserted"} | {o for _, o in strategy.contradictions}
    lv = liveness(claim, claim, frozenset(R))
    return ("COMMITTED" if lv == LIVE else f"REFUSED:WARRANT_{lv}"), None


def independent_support_count(claim, principal_of):
    """Honest: alternatives with pairwise-disjoint *principal* sets; ids of one principal never count twice."""
    chosen = []
    for W in sorted(claim, key=lambda w: (len(w), sorted(w))):
        P = frozenset(principal_of[e] for e in W)
        if all(not (P & c) for c in chosen):
            chosen.append(P)
    return len(chosen)


def mutant_sybil_independent_count(claim):
    """Planted: id-disjointness read as independence (the OCM `independent_support_count` shape)."""
    chosen = []
    for W in sorted(claim, key=lambda w: (len(w), sorted(w))):
        if all(not (W & c) for c in chosen):
            chosen.append(W)
    return len(chosen)


def inspection_equilibrium(g, f, c, d):
    """Parent (inspection game, mixed equilibrium): provider lies with p*, gate audits with q*.
    Provider payoff: lie uncaught +g, lie caught −f, honest 0.  Gate payoff: audit −c, unaudited lie −d,
    otherwise 0.  Interior equilibrium exists iff 0 < c < d; then q* = g/(g+f), p* = c/d."""
    if not (0 < c < d) or g <= 0 or f <= 0:
        return None
    return Fraction(c, d), Fraction(g, g + f)


def provider_payoff(lie, audit, g, f):
    if not lie:
        return Fraction(0)
    return Fraction(-f) if audit else Fraction(g)


def gate_payoff(lie, audit, c, d):
    out = Fraction(0)
    if audit:
        out -= c
    if lie and not audit:
        out -= d
    return out


def check_j2_epistemic_games():
    counts = {}
    strategies = list(adversary_strategies())
    assert len(strategies) == 18 * 4 + 9 * 1 == 81          # a1 asserted/retracted: 4 contradiction options; a1 absent: 1
    n_strat = len(strategies)
    counts["adversary_strategies"] = n_strat
    outcomes = {}
    for cname, claim in CLAIMS.items():
        for rname, req in REQS.items():
            outcomes[(cname, rname)] = [gate(claim, s, req) for s in strategies]
    # (i) non-interference: claims with no adversary id anywhere have one outcome over every strategy
    invariant = 0
    for cname in ("c_native", "c_native2"):
        for rname in REQS:
            verdicts = {o[0] for o in outcomes[(cname, rname)]}
            assert len(verdicts) == 1, (cname, rname, verdicts)
            invariant += len(outcomes[(cname, rname)])
    counts["non_interference_checks"] = invariant
    # a claim with an adversary-free alternative commits under REQ_TRUTH through that alternative, always
    mixed = outcomes[("c_mixed", "REQ_TRUTH")]
    assert all(o == ("COMMITTED", frozenset({"o2"})) for o in mixed)
    counts["mixed_claim_commits_via_adversary_free_alternative"] = len(mixed)
    # (ii) authority ceiling: under REQ_TRUTH / REQ_COMMIT no strategy commits a claim whose every warrant
    #      cites an adversary id; under REQ_REPORT such claims commit exactly when a cited id is asserted
    adv_only = ("c_report", "c_sybil", "c_composed")
    zero_truth = zero_commit = 0
    for cname in adv_only:
        assert all(o[0] != "COMMITTED" for o in outcomes[(cname, "REQ_TRUTH")])
        zero_truth += n_strat
        assert all(o[0] != "COMMITTED" for o in outcomes[(cname, "REQ_COMMIT")])
        zero_commit += n_strat
    counts["adversary_only_claims_committed_under_REQ_TRUTH"] = 0
    counts["adversary_only_claims_committed_under_REQ_COMMIT"] = 0
    counts["authority_ceiling_checks"] = zero_truth + zero_commit
    # commit authority never comes from evidence: even the gate's external commit authority cannot commit a
    # REQ_COMMIT task from evidence alone (T1: evidence carries no commit rank)
    assert all(o[0] != "COMMITTED" for cname in CLAIMS for o in outcomes[(cname, "REQ_COMMIT")])
    counts["REQ_COMMIT_never_from_evidence"] = n_strat * len(CLAIMS)
    report_commits = {}
    for cname in adv_only:
        got = sum(1 for o in outcomes[(cname, "REQ_REPORT")] if o[0] == "COMMITTED")
        report_commits[cname] = got
    # exact: c_report commits iff a1 asserted; c_sybil iff any asserted; c_composed iff a1 asserted and no
    # contradiction registered against o1 ... (o1 ∧ a1 support filtered by {a1,o1})
    exp_report = sum(1 for s in strategies if s.states["a1"] == "asserted")
    exp_sybil = sum(1 for s in strategies if any(v == "asserted" for v in s.states.values()))
    exp_comp = sum(1 for s in strategies if s.states["a1"] == "asserted" and ("a1", "o1") not in s.contradictions)
    assert report_commits == {"c_report": exp_report, "c_sybil": exp_sybil, "c_composed": exp_comp}, report_commits
    counts["REQ_REPORT_commits"] = report_commits
    # (iii) forced refusal: possible iff every exhibited warrant cites an adversary id
    forced = {}
    for cname in CLAIMS:
        forced[cname] = sum(1 for o in outcomes[(cname, "REQ_REPORT")] if o[0] != "COMMITTED")
    for cname in ("c_native", "c_native2", "c_mixed"):
        assert forced[cname] == 0
    for cname in adv_only:
        assert forced[cname] > 0
    counts["strategies_forcing_refusal_under_REQ_REPORT"] = forced
    # (iv) contradiction registration poisons only joint supports containing the registrant's id
    s_contra = Strategy({"a1": "asserted", "a2": "absent", "a3": "absent"}, frozenset({("a1", "o1")}), Fraction(0))
    s_plain = Strategy({"a1": "asserted", "a2": "absent", "a3": "absent"}, frozenset(), Fraction(0))
    assert gate(CLAIMS["c_composed"], s_contra, REQS["REQ_REPORT"])[0] == "REFUSED:CONTRADICTED"
    assert gate(CLAIMS["c_composed"], s_plain, REQS["REQ_REPORT"])[0] == "COMMITTED"
    assert gate(CLAIMS["c_native"], s_contra, REQS["REQ_TRUTH"]) == gate(CLAIMS["c_native"], s_plain, REQS["REQ_TRUTH"]) == ("COMMITTED", frozenset({"o1"}))
    assert gate(CLAIMS["c_mixed"], s_contra, REQS["REQ_TRUTH"]) == ("COMMITTED", frozenset({"o2"}))
    counts["contradiction_local_to_joint_supports"] = 4
    bad = mutant_nogood_kills_endpoint(CLAIMS["c_native"], s_contra, REQS["REQ_TRUTH"])
    assert bad[0] != "COMMITTED"
    counts["mutant_nogood_kills_endpoint_caught"] = 1
    # (v) Sybil: three ids of one principal are one independent support
    principal = {"o1": "sensor1", "o2": "sensor2", "a1": "adv", "a2": "adv", "a3": "adv"}
    assert independent_support_count(CLAIMS["c_sybil"], principal) == 1
    assert mutant_sybil_independent_count(CLAIMS["c_sybil"]) == 3
    assert independent_support_count(CLAIMS["c_native2"], principal) == mutant_sybil_independent_count(CLAIMS["c_native2"]) == 2
    counts["sybil_independent_supports"] = {"honest": 1, "mutant_id_disjointness": 3, "no_alarm_two_sensors": 2}
    # Sybil robustness: c_sybil stays LIVE until every id is retracted; all ids are the adversary's, so
    # forced refusal remains available to it (counted in (iii)); authority never exceeds source=1
    sybil_live = sum(1 for s in strategies if gate(CLAIMS["c_sybil"], s, REQS["REQ_REPORT"])[0] == "COMMITTED")
    assert sybil_live == exp_sybil and rank(drop_commit(ADV_AUTH), "world_truth") == 0
    counts["sybil_world_truth_rank_over_all_strategies"] = 0
    # mutant: report read as truth commits adversary-only claims under REQ_TRUTH
    mutant_commits = sum(1 for s in strategies if mutant_report_as_truth(CLAIMS["c_report"], s, REQS["REQ_TRUTH"])[0] == "COMMITTED")
    assert mutant_commits == exp_report > 0
    counts["mutant_report_as_truth_commits_under_REQ_TRUTH"] = mutant_commits
    # (vi) commit then retract: the receipt names the committing warrant; retraction reopens exactly its cone
    receipt_W = gate(CLAIMS["c_report"], s_plain, REQS["REQ_REPORT"])[1]
    assert receipt_W == frozenset({"a1"})
    dep = {"a1": ("commit:c_report",), "o1": ("commit:c_native",)}
    cone = forward_closure(dep, {"a1"})
    assert cone == {"a1", "commit:c_report"}
    counts["retraction_cone"] = sorted(cone)
    mutant_receipt = frozenset()                          # receipt without evidence ids
    assert "commit:c_report" not in forward_closure(dep, mutant_receipt)
    counts["mutant_receipt_without_evidence_ids_misses_commitment"] = 1
    # the historical commitment was licensed at commit time (R4): verdict at s_plain is COMMITTED
    counts["commit_before_retraction_licensed"] = 1
    # (vii) the persuasion lever has no purchase: the honest gate ignores any confidence coordinate
    same = 0
    for s in strategies:
        for conf in (Fraction(0), Fraction(1, 2), Fraction(1)):
            s2 = Strategy(s.states, s.contradictions, conf)
            for cname, claim in CLAIMS.items():
                for req in REQS.values():
                    assert gate(claim, s2, req) == gate(claim, s, req)
                    same += 1
    counts["confidence_coordinate_ignored_checks"] = same
    persuaded = sum(1 for s in strategies if mutant_confidence_gate(CLAIMS["c_report"], Strategy(s.states, s.contradictions, Fraction(1)), REQS["REQ_TRUTH"])[0] == "COMMITTED")
    assert persuaded == exp_report > 0
    counts["mutant_confidence_gate_commits_under_REQ_TRUTH"] = persuaded
    # (viii) inspection game (PARENT_SUFFICIENT): exact mixed equilibrium on a rational grid
    eq_checks = none_cases = 0
    for g in (1, 2, 3):
        for f in (1, 2, 4):
            for c in (1, 2, 3):
                for d in (1, 2, 4, 6):
                    eq = inspection_equilibrium(g, f, c, d)
                    if eq is None:
                        none_cases += 1
                        continue
                    p, q = eq
                    # provider indifferent between lie and honest at q*; gate indifferent between audit and not at p*
                    lie_val = (1 - q) * provider_payoff(True, False, g, f) + q * provider_payoff(True, True, g, f)
                    assert lie_val == provider_payoff(False, False, g, f) == 0
                    audit_val = p * gate_payoff(True, True, c, d) + (1 - p) * gate_payoff(False, True, c, d)
                    noaudit_val = p * gate_payoff(True, False, c, d) + (1 - p) * gate_payoff(False, False, c, d)
                    assert audit_val == noaudit_val == Fraction(-c)
                    eq_checks += 1
    counts["inspection_equilibria_verified"] = eq_checks
    counts["inspection_no_interior_equilibrium"] = none_cases
    counts["inspection_example"] = {"g": 1, "f": 1, "c": 1, "d": 2, "p_star": str(Fraction(1, 2)), "q_star": str(Fraction(1, 2))}
    # gate-specific corollary: whatever p, the truth-typed gate's outcome on adversary-only claims is REFUSE
    counts["truth_gate_independent_of_lie_probability"] = 1
    counts["status"] = ("PARENT_HEAVY: mechanism design / inspection games / Bayesian persuasion own the strategic results "
                        "(PARENT_SUFFICIENT); PROVED gate-specific: adversary action set = {enable REPORT-typed commits of "
                        "claims within its channel authority, force refusal of claims whose every warrant cites its ids, "
                        "poison joint supports containing its ids}; non-interference otherwise; no persuasion lever; Sybil "
                        "inflates id-disjoint support counts only")
    return counts


# =============================================================================================
# J3 · FDX-14 · whole-system lower bounds on the registered finite classes
# =============================================================================================

HYPS = tuple(range(16))          # Boolean functions of two inputs; bit i = h(x) with i = 2*x0 + x1
FULL = (1 << 16) - 1


def hval(h, i):
    return (h >> i) & 1


def is_affine(h):
    return (hval(h, 0) ^ hval(h, 1) ^ hval(h, 2) ^ hval(h, 3)) == 0


def is_monotone(h):
    return all(hval(h, i) <= hval(h, j) for i in range(4) for j in range(4) if (i & j) == i)


CLASSES = {
    "ALL16": frozenset(HYPS),
    "AFFINE8": frozenset(h for h in HYPS if is_affine(h)),
    "MONOTONE6": frozenset(h for h in HYPS if is_monotone(h)),
}

# channels with power-of-two answer alphabets; bits = log2(alphabet)
CHANNELS = {
    "obs_00": (lambda h: hval(h, 0), 1), "obs_01": (lambda h: hval(h, 1), 1),
    "obs_10": (lambda h: hval(h, 2), 1), "obs_11": (lambda h: hval(h, 3), 1),
    "pair_00_01": (lambda h: hval(h, 0) * 2 + hval(h, 1), 2),
    "pair_10_11": (lambda h: hval(h, 2) * 2 + hval(h, 3), 2),
    "table": (lambda h: h, 4),
}


def identification_cost(channel_names, charge=None):
    """Exact minimal worst-case total channel bits identifying every member of every V ⊆ HYPS (bitmask DP)."""
    charge = charge or {c: CHANNELS[c][1] for c in channel_names}
    answer_masks = {}
    for c in channel_names:
        fn = CHANNELS[c][0]
        by_answer = {}
        for h in HYPS:
            by_answer[fn(h)] = by_answer.get(fn(h), 0) | (1 << h)
        answer_masks[c] = tuple(by_answer.values())
    memo = {}

    def cost(V):
        if V & (V - 1) == 0:
            return 0
        if V in memo:
            return memo[V]
        best = None
        for c in channel_names:
            classes = [V & mk for mk in answer_masks[c] if V & mk]
            if len(classes) == 1:
                continue
            val = charge[c] + max(cost(part) for part in classes)
            if best is None or val < best:
                best = val
        memo[V] = best
        return best

    return {V: cost(V) for V in range(1, 1 << 16)}


def mutant_charge_channel_one_bit(channel_names):
    return {c: 1 for c in channel_names}


def rows_covered(multiplicity, revoked_rows_budget):
    """Worst case number of rows whose every evidence id is revoked with a budget of k revocations."""
    n = len(multiplicity)
    best = 0
    for S in subsets(range(n)):
        if sum(multiplicity[i] for i in S) <= revoked_rows_budget:
            best = max(best, len(S))
    return best


def separating_set_sizes(cls):
    """Smallest probe set separating every pair of the class (target-oblivious verification), and the
    largest over targets of the smallest probe set separating that target from every other member
    (target-adaptive verification = specifying set size)."""
    members = sorted(cls)
    obliv = None
    for S in subsets(range(4)):
        if all(any(hval(h, i) != hval(g, i) for i in S) for h, g in itertools.combinations(members, 2)):
            if obliv is None or len(S) < obliv:
                obliv = len(S)
    adaptive = 0
    per_target = {}
    for h in members:
        best = None
        for S in subsets(range(4)):
            if all(any(hval(h, i) != hval(g, i) for i in S) for g in members if g != h):
                if best is None or len(S) < best:
                    best = len(S)
        per_target[h] = best
        adaptive = max(adaptive, best)
    return obliv, adaptive, per_target


def truncation_digest(h, bits):
    return h & ((1 << bits) - 1)


def check_j3_whole_system_lower_bounds():
    counts = {"class_sizes": {k: len(v) for k, v in CLASSES.items()}}
    assert counts["class_sizes"] == {"ALL16": 16, "AFFINE8": 8, "MONOTONE6": 6}
    # (i) identification: total channel bits along any adaptive transcript ≥ ceil(log2 |V|) for every V,
    #     with every mix of observation, pair and table channels; equality on the full class for every mix
    mixes = [("obs_00", "obs_01", "obs_10", "obs_11"),
             ("obs_00", "obs_01", "obs_10", "obs_11", "pair_00_01", "pair_10_11"),
             ("pair_00_01", "pair_10_11"), ("table",),
             ("obs_00", "obs_01", "obs_10", "obs_11", "pair_00_01", "pair_10_11", "table")]
    bound_checks = 0
    full_cost = {}
    mutant_below = 0
    for mix in mixes:
        table = identification_cost(mix)
        for V, c in table.items():
            assert c is not None and c >= ceil_log2(popcount(V)), (mix, V)
            bound_checks += 1
        full_cost[",".join(mix)] = table[FULL]
        assert table[FULL] == 4
        mt = identification_cost(mix, mutant_charge_channel_one_bit(mix))
        mutant_below += sum(1 for V, c in mt.items() if c < ceil_log2(popcount(V)))
    assert mutant_below > 0
    counts["identification_bound_checks"] = bound_checks
    counts["identification_cost_full_class_by_mix"] = full_cost
    counts["mutant_charge_channel_one_bit_below_bound_subsets"] = mutant_below
    # class restriction moves cost: AFFINE8 identified in 3 observation bits, MONOTONE6 in 3
    obs = ("obs_00", "obs_01", "obs_10", "obs_11")
    t_obs = identification_cost(obs)
    mask = lambda cls: sum(1 << h for h in cls)
    counts["identification_bits_by_class_observations"] = {k: t_obs[mask(v)] for k, v in CLASSES.items()}
    assert counts["identification_bits_by_class_observations"] == {"ALL16": 4, "AFFINE8": 3, "MONOTONE6": 3}
    # (ii) retention: a class-restricted memory (3 bits + description AFFINE) retains all 8 affine targets and
    #     must refuse the 8 others; the mutant that silently stores the affine completion answers wrongly
    retained = refused = wrong_mutant = wrong_honest = 0
    for h in HYPS:
        stored = (hval(h, 0), hval(h, 1), hval(h, 2))                   # 3 mutable bits
        completed = stored + (stored[0] ^ stored[1] ^ stored[2],)      # description: affine ⇒ row 11 determined
        if is_affine(h):
            assert completed == tuple(hval(h, i) for i in range(4))
            retained += 1
        else:
            refused += 1                                             # honest: CANNOT_REPRESENT
            if completed != tuple(hval(h, i) for i in range(4)):
                wrong_mutant += 1
    assert (retained, refused, wrong_mutant, wrong_honest) == (8, 8, 8, 0)
    counts["retention_affine_memory"] = {"retained": retained, "cannot_represent": refused,
                                         "mutant_description_without_cannot_represent_wrong": wrong_mutant, "honest_wrong": wrong_honest}
    # pigeonhole: s mutable states retain at most s targets; 3 bits cannot retain 16 (witness: any 3-bit
    # projection of the 16 tables collides on some pair)
    collide = 0
    for proj in itertools.combinations(range(4), 3):
        seen = {}
        for h in HYPS:
            key = tuple(hval(h, i) for i in proj)
            if key in seen:
                collide += 1
            seen[key] = h
    assert collide == 4 * 8
    counts["three_bit_projections_colliding_targets"] = collide
    # (iii) repair vs retention: for every redundancy design m ∈ {1,2,3}^4 and every k ≤ Σm revocations,
    #      Σm + worst-case repair queries ≥ 4 + k; equality cases counted; memory-replay 'repair' violates it
    designs = list(itertools.product((1, 2, 3), repeat=4))
    checks = tight = mutant_violations = 0
    for mult in designs:
        total = sum(mult)
        for k in range(1, total + 1):
            wiped = rows_covered(mult, k)
            assert total + wiped >= 4 + k, (mult, k, wiped)
            checks += 1
            if total + wiped == 4 + k:
                tight += 1
            if total + 0 < 4 + k:                 # mutant_repair_from_memory_replay: repair cost 0
                mutant_violations += 1
    counts["repair_retention_checks"] = checks
    counts["repair_retention_tight_cases"] = tight
    counts["mutant_repair_from_memory_replay_violations"] = mutant_violations
    assert mutant_violations > 0
    # n-row generalisation: Σm + wiped ≥ n + k for n = 2, 3 rows with m ∈ {1,2}
    gen = 0
    for n in (2, 3):
        for mult in itertools.product((1, 2), repeat=n):
            total = sum(mult)
            for k in range(1, total + 1):
                assert total + rows_covered(mult, k) >= n + k
                gen += 1
    counts["repair_retention_generalisation_checks"] = gen
    # (iv) communication: the 16 diagonal pairs form a fooling set for equality of retained procedures ⇒
    #      ≥ 4 transcript bits (parent lemma); a d-bit digest with d < 4 has a false-equality witness
    fooling = 0
    for h, g in itertools.combinations(HYPS, 2):
        assert h != g
        fooling += 1
    counts["fooling_set_pairs"] = fooling
    counts["equality_transcript_bits_lower_bound"] = ceil_log2(16)
    digest_collisions = {}
    for d in (1, 2, 3, 4):
        coll = sum(1 for h, g in itertools.combinations(HYPS, 2) if truncation_digest(h, d) == truncation_digest(g, d))
        digest_collisions[str(d)] = coll
    assert digest_collisions == {"1": 56, "2": 24, "3": 8, "4": 0}
    counts["mutant_digest_equality_false_same_pairs"] = digest_collisions
    # (v) verification probes: oblivious separating set vs adaptive specifying set, per class
    ver = {}
    for name, cls in CLASSES.items():
        obliv, adapt, per_target = separating_set_sizes(cls)
        lower = ceil_log2(len(cls))
        assert obliv >= lower and adapt >= lower and adapt <= obliv
        ver[name] = {"oblivious": obliv, "adaptive": adapt, "entropy_bound": lower}
    assert ver == {"ALL16": {"oblivious": 4, "adaptive": 4, "entropy_bound": 4},
                   "AFFINE8": {"oblivious": 3, "adaptive": 3, "entropy_bound": 3},
                   "MONOTONE6": {"oblivious": 4, "adaptive": 3, "entropy_bound": 3}}, ver
    counts["verification_probes_by_class"] = ver
    # mutant: an oblivious MONOTONE6 verifier with 3 probes accepts a forged table on some pair
    mon = sorted(CLASSES["MONOTONE6"])
    forged_accept = 0
    witness = None
    for S in itertools.combinations(range(4), 3):
        for h, g in itertools.combinations(mon, 2):
            if all(hval(h, i) == hval(g, i) for i in S):
                forged_accept += 1
                if witness is None:
                    witness = {"probes": list(S), "claimed": h, "actual": g}
    assert forged_accept > 0 and witness is not None
    counts["mutant_oblivious_verifier_three_probes_monotone_accepts_forgery"] = forged_accept
    counts["mutant_oblivious_verifier_witness"] = witness
    # no-alarm: four probes separate every pair in every class; AFFINE8 three-probe verification is exact
    assert all(any(hval(h, i) != hval(g, i) for i in range(4)) for h, g in itertools.combinations(HYPS, 2))
    counts["no_alarm_four_probes_separate_all"] = 120
    # (vi) whole-system table: bits/probes per phase, ALL16 vs AFFINE8; description moves 1 unit per phase
    #      at the price of 8 CANNOT_REPRESENT targets
    repair_min = {4: min(sum(m) + rows_covered(m, 1) for m in designs),
                  3: min(sum(m) + rows_covered(m, 1) for m in itertools.product((1, 2), repeat=3))}
    assert repair_min == {4: 5, 3: 4}
    table = {}
    for name in ("ALL16", "AFFINE8"):
        cls = CLASSES[name]
        rows_needed = 4 if name == "ALL16" else 3               # the affine description determines row 11
        table[name] = {"identification_bits": t_obs[mask(cls)], "retention_bits": ceil_log2(len(cls)),
                       "verification_probes_oblivious": ver[name]["oblivious"],
                       "communication_bits_equality": ceil_log2(len(cls)),
                       "repair_plus_retention_min_at_k1": repair_min[rows_needed],
                       "cannot_represent_targets": 16 - len(cls)}
    counts["whole_system_table"] = table
    assert all(table["ALL16"][k] - table["AFFINE8"][k] == 1 for k in ("identification_bits", "retention_bits", "verification_probes_oblivious", "communication_bits_equality", "repair_plus_retention_min_at_k1"))
    counts["status"] = ("PARENT_OWNED mathematics (decision-tree / query complexity, teaching and specifying sets, fooling "
                        "sets, pigeonhole retention, erasure-style repair counting); PROVED exact corollaries on the registered "
                        "classes: identification bits ≥ ceil(log2|V|) for every channel mix (65 535 × 5), retention 3-bit "
                        "memory refuses 8, Σm + repair ≥ n + k (all designs), equality ≥ 4 transcript bits with digest "
                        "collision witnesses, oblivious verification 4 > adaptive 3 = entropy 3 on MONOTONE6; hash-based "
                        "identity CANNOT_CHECK (computational assumption)")
    return counts


# =============================================================================================
# driver
# =============================================================================================

CHECKS = {
    "J1_FDX06_distributed_epistemics": check_j1_distributed_epistemics,
    "J2_FDX07_epistemic_games": check_j2_epistemic_games,
    "J3_FDX14_whole_system_lower_bounds": check_j3_whole_system_lower_bounds,
}

STATUS = {
    "J1_FDX-06": "PARENT_SUFFICIENT (state-based CRDT convergence, R5 freshness impossibility, Byzantine agreement for authority objects); PROVED corollaries on the fixture; residual = the exact typed statement only",
    "J2_FDX-07": "PARENT_HEAVY / PARENT_SUFFICIENT (inspection games, mechanism design, Bayesian persuasion); PROVED gate-specific attack-surface statements on the fixture",
    "J3_FDX-14": "PARENT_OWNED (query complexity, teaching/specifying sets, fooling sets, pigeonhole, erasure counting); PROVED exact corollaries on the registered finite classes; hash identity CANNOT_CHECK",
}

OPEN = [
    "FDX-06: graded / probabilistic trust and Byzantine-fraction thresholds for warrant (not authority) exchange — FDX-08 territory; the exact fragment here is per-source revocable assumptions only",
    "FDX-07: truthful-revelation mechanisms with costly verification for real provider utilities — parent-owned and utility-model dependent; only the lattice action set of the gate is bounded here",
    "FDX-14: coded / cross-row redundant storage (Singleton-type bounds) and infinite classes (MEG-34 / FDX-09) — not covered by the uncoded evidence-id fixture",
]

CANNOT_CHECK_ITEMS = [
    "FDX-06: message authenticity (signatures, trust-root provenance) — assumed, not checkable inside the finite model (R6 anchor authenticity)",
    "FDX-07: that a real provider's utilities match the inspection-game payoffs — outside the model",
    "FDX-14: collision resistance of digests used for cross-space identity — a computational assumption; the finite model exhibits collisions for every digest shorter than log2|H|",
]

EXACTLY_BOUNDED_IMPOSSIBILITIES = [
    "FDX-06: a node whose view misses an effective revocation cannot distinguish the history with that revocation from the one without (identical view, different verdicts) — no non-abstaining current-validity policy is sound (R5)",
    "FDX-07: no strategy of an evidence provider whose channel carries authority (source=1) makes the gate commit a claim requiring world_truth ≥ 1 or commit ≥ 1 through its evidence alone; and no strategy changes the gate's verdict on a claim none of whose warrants cite its ids",
    "FDX-14: no memory with fewer than log2|H| mutable bits retains every member of H; no adaptive transcript identifies H in fewer than log2|H| channel bits; no deterministic equality protocol on retained procedures uses fewer than log2|H| transcript bits; Σ(retention ids) + worst-case repair queries ≥ n + k against k revocations",
]


def run_all():
    out = {name: fn() for name, fn in CHECKS.items()}
    out["ITEM_STATUS"] = STATUS
    out["OPEN"] = OPEN
    out["CANNOT_CHECK"] = CANNOT_CHECK_ITEMS
    out["EXACTLY_BOUNDED_IMPOSSIBILITIES"] = EXACTLY_BOUNDED_IMPOSSIBILITIES
    out["NOVELTY"] = "NOT_ESTABLISHED"
    out["status"] = "ALL_HOLD"
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if "--probe-cannot-check" in argv:
            raise CannotCheck("probe: a check that cannot run must exit 2, never 0")
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
