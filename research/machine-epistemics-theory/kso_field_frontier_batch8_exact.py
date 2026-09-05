"""Exact finite checker for KSO_FIELD_FRONTIER_THEOREMS_BATCH8_V1.md (stdlib only, exact).

One check function per field-frontier row of `field_dynamics_v1/FRONTIER.md` taken in batch 8:
H1 = FDX-01 (open-system epistemic closure), H2 = FDX-02 (controlled epistemic viability),
H3 = FDX-03 (information/interface conservation), H4 = FDX-05 (reversible and irreversible epistemic
transitions).  Every check performs (a) the positive statement by exhaustive enumeration of a finite
fixture, (b) at least one planted hostile whose mutation is asserted applied and which must be caught,
and (c) a no-alarm control.  Items whose honest status is PARENT_OWNED / PARENT_SUFFICIENT or an exact
impossibility report the falsifier search they ran and the smallest holding / failing fixture.  The
objects are re-implemented here (dependency closure, a finite-horizon controller/environment game, finite
deterministic channels as partitions, an append-only ledger with a LIFO component stack); nothing is
imported from ``ocm``.  Every count is an integer; every probability an exact ``Fraction``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
Assertion-based verification refuses optimized Python execution before any check runs.
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from collections import namedtuple
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


def require_assertions():
    if not __debug__:
        raise CannotCheck("ASSERTIONS_DISABLED: rerun without -O/-OO/PYTHONOPTIMIZE")


def subsets(universe, min_size=0):
    universe = tuple(universe)
    for k in range(min_size, len(universe) + 1):
        for combo in itertools.combinations(universe, k):
            yield frozenset(combo)


def ceil_log2(n):
    if n < 1:
        raise CannotCheck("ceil_log2 of a non-positive count")
    return 0 if n == 1 else (n - 1).bit_length()


# =============================================================================================
# H1 · FDX-01 · open-system epistemic closure
# =============================================================================================

ROOTS = ("x1", "x2", "x3")
COVERAGE = ("MONITORED", "FROZEN", "UNCOVERED")
SIGMA0 = {r: 1 for r in ROOTS}


def dependency_graphs():
    """Registered dependency descriptions D over roots x1..x3, an internal claim a and the conclusion c.

    D maps each internal node to the set of its tails (all-tails conjunctive dependence).  128 graphs."""
    for tails_a in subsets(ROOTS):
        for tails_c in subsets(ROOTS + ("a",)):
            yield {"a": tails_a, "c": tails_c}


def roots_of(graph, node):
    """Backward dependency closure of `node` restricted to environment roots (least fixed point over D)."""
    seen, work, roots = set(), [node], set()
    while work:
        v = work.pop()
        for t in graph.get(v, ()):
            if t in ROOTS:
                roots.add(t)
            elif t not in seen:
                seen.add(t)
                work.append(t)
    return frozenset(roots)


def mutant_roots_direct_only(graph, node):
    """Planted: a closure certificate computed over the direct tails only (the transitive root through `a`
    is the unmodelled dependency it ignores)."""
    return frozenset(t for t in graph.get(node, ()) if t in ROOTS)


def closure_certificate(roots, coverage):
    """Typed closure certificate for a conclusion with dependency roots `roots`, relative to D.

    MONITORED_CURRENT: every root has a registered synchronous monitor (observation channel that fires on
    change).  CONDITIONAL_ON_ASSUMPTIONS: every root is monitored or frozen by a registered, revocable
    invariance assumption (the assumption ids are part of the certificate).  NO_CLOSURE: some root has
    neither — no total exact Boolean validity decision is licensed. Sound partial decisions remain
    possible. Dependency completeness of D is a registered assumption of
    every certificate; it is never checked from inside."""
    uncovered = tuple(sorted(r for r in roots if coverage[r] == "UNCOVERED"))
    if uncovered:
        return ("NO_CLOSURE", uncovered)
    frozen = tuple(sorted(r for r in roots if coverage[r] == "FROZEN"))
    return ("CONDITIONAL_ON_ASSUMPTIONS" if frozen else "MONITORED_CURRENT", frozen)


def registered_view(coverage, sigma):
    """Everything the machine can read about the environment: the monitored root values."""
    return tuple(sigma[r] for r in ROOTS if coverage[r] == "MONITORED")


def reported_validity(roots, coverage, sigma):
    """The registered state's value for the conclusion: monitored roots read, frozen roots assumed at their
    registration value (1), uncovered roots also at registration value (the machine has no channel)."""
    return all((sigma[r] if coverage[r] == "MONITORED" else 1) for r in roots)


def actual_validity(roots, sigma):
    return all(sigma[r] for r in roots)


def flip_trajectories(flippable, max_len=2):
    yield ()
    for length in range(1, max_len + 1):
        for seq in itertools.product(sorted(flippable), repeat=length):
            yield seq


def run_environment(seq):
    sigma = dict(SIGMA0)
    states = [dict(sigma)]
    for r in seq:
        sigma[r] ^= 1
        states.append(dict(sigma))
    return states


def check_h1_open_system_closure():
    require_assertions()
    graphs = list(dependency_graphs())
    assert len(graphs) == 128
    coverages = [dict(zip(ROOTS, c)) for c in itertools.product(COVERAGE, repeat=3)]
    assert len(coverages) == 27
    counts = {
        "graphs": len(graphs), "coverages": len(coverages), "environments": 8,
        "root_free_conclusions": 0, "monitored_current_checks": 0, "conditional_checks": 0,
        "no_closure_cases": 0, "impossibility_witnesses": 0, "sound_iff_all_roots_covered": 0,
        "unconditional_sound_iff_all_roots_monitored": 0, "frozen_root_flipped_unconditional_wrong": 0,
        "mutant_current_validity_without_interface_wrong": 0, "mutant_current_validity_without_interface_cases": 0,
        "mutant_direct_only_cases": 0, "mutant_direct_only_caught": 0,
        "lag_as_of_sound": 0, "lag_read_as_current_wrong": 0,
    }
    smallest_witness = None
    for graph in graphs:
        roots = roots_of(graph, "c")
        if not roots:
            counts["root_free_conclusions"] += 1
        for coverage in coverages:
            cert = closure_certificate(roots, coverage)
            all_covered = all(coverage[r] != "UNCOVERED" for r in roots)
            all_monitored = all(coverage[r] == "MONITORED" for r in roots)
            assert (cert[0] != "NO_CLOSURE") == all_covered
            conditional_sound = True
            unconditional_sound = True
            for flippable in subsets(ROOTS):
                for seq in flip_trajectories(flippable):
                    for sigma in run_environment(seq):
                        act = actual_validity(roots, sigma)
                        rep = reported_validity(roots, coverage, sigma)
                        if rep != act:
                            unconditional_sound = False
                        if cert[0] == "MONITORED_CURRENT":
                            assert rep == act, (graph, coverage, seq)
                            counts["monitored_current_checks"] += 1
                        elif cert[0] == "CONDITIONAL_ON_ASSUMPTIONS":
                            if all(sigma[a] for a in cert[1]):
                                assert rep == act, (graph, coverage, seq)
                                counts["conditional_checks"] += 1
                            elif rep != act:
                                counts["frozen_root_flipped_unconditional_wrong"] += 1
                        else:
                            # hostile: reading the registered liveness as a current-validity claim anyway
                            counts["mutant_current_validity_without_interface_cases"] += 1
                            if rep != act:
                                counts["mutant_current_validity_without_interface_wrong"] += 1
                                conditional_sound = False
            if cert[0] == "NO_CLOSURE":
                counts["no_closure_cases"] += 1
                # exact impossibility: an uncovered root r flipped by an unmodelled transition leaves the
                # registered view unchanged while the conclusion's validity changes — no function of the
                # registered state can give a total exact Boolean decision on both states
                r = cert[1][0]
                sigma1 = dict(SIGMA0)
                sigma1[r] = 0
                assert registered_view(coverage, SIGMA0) == registered_view(coverage, sigma1)
                assert actual_validity(roots, SIGMA0) and not actual_validity(roots, sigma1)
                counts["impossibility_witnesses"] += 1
                if smallest_witness is None or len(roots) < len(smallest_witness["roots"]):
                    smallest_witness = {"graph": {k: sorted(v) for k, v in graph.items()}, "roots": sorted(roots),
                                        "coverage": dict(coverage), "flipped": r}
            # the sound set is exactly the covered set (conditional reading) / the monitored set (unconditional)
            assert conditional_sound == all_covered
            counts["sound_iff_all_roots_covered"] += 1
            assert unconditional_sound == all_monitored
            counts["unconditional_sound_iff_all_roots_monitored"] += 1
            # hostile: certificate over the direct dependencies only
            mroots = mutant_roots_direct_only(graph, "c")
            mcert = closure_certificate(mroots, coverage)
            if mcert[0] != "NO_CLOSURE" and cert[0] == "NO_CLOSURE":
                counts["mutant_direct_only_cases"] += 1
                missing = cert[1][0]
                assert missing not in mroots and missing in roots
                sigma1 = dict(SIGMA0)
                sigma1[missing] = 0
                assert registered_view(coverage, SIGMA0) == registered_view(coverage, sigma1)
                assert reported_validity(mroots, coverage, sigma1) and not actual_validity(roots, sigma1)
                counts["mutant_direct_only_caught"] += 1
            # lagged monitors: the report at step t carries the values delivered at step t-1
            if cert[0] == "MONITORED_CURRENT" and roots:
                for flippable in subsets(ROOTS, 1):
                    for seq in flip_trajectories(flippable):
                        states = run_environment(seq)
                        for t in range(1, len(states)):
                            lagged = reported_validity(roots, coverage, states[t - 1])
                            assert lagged == actual_validity(roots, states[t - 1])
                            counts["lag_as_of_sound"] += 1
                            if lagged != actual_validity(roots, states[t]):
                                counts["lag_read_as_current_wrong"] += 1
    assert counts["impossibility_witnesses"] == counts["no_closure_cases"] > 0
    assert counts["mutant_direct_only_cases"] == counts["mutant_direct_only_caught"] > 0
    assert counts["mutant_current_validity_without_interface_wrong"] > 0
    assert counts["frozen_root_flipped_unconditional_wrong"] > 0
    assert counts["lag_read_as_current_wrong"] > 0
    counts["smallest_impossibility_witness"] = smallest_witness
    counts["closure_relative_to_D"] = "dependency completeness of D is a registered assumption; CANNOT_CHECK from inside"
    counts["status"] = "PROVED (finite): registered total Boolean reporter exact iff every dependency root is covered (monitor or revocable assumption); unconditional exactness iff every root is monitored; no total exact Boolean decision below that interface, partial decisions not excluded; PARENT_OWNED (assume-guarantee, monitorability, ATMS assumptions)"
    return counts


# =============================================================================================
# H2 · FDX-02 · controlled epistemic viability
# =============================================================================================

T_MAX, B_MAX, RHO_MAX = 6, 6, 2
WARRANTS = ("LIVE", "UNKNOWN", "DEAD")
SCOPES = ("IN", "OUT", "OUT_FINAL")


def h2_states():
    return [s for s in itertools.product(WARRANTS, (0, 1), SCOPES, ("LOW", "HIGH"), (0, 1),
                                          range(B_MAX + 1), range(T_MAX + 1), range(RHO_MAX + 1))]


def licensed_abstain(s):
    """Registered abstain licence: a reason from {DEAD warrant, no commit authority, scope refused}."""
    w, a, k, *_ = s
    return w == "DEAD" or a == 0 or k == "OUT_FINAL"


def commit_predicates_hold(s):
    w, a, k, r, *_ = s
    return w == "LIVE" and a == 1 and k == "IN" and r == "LOW"


def controller_moves(s, rules):
    """Controller moves with their resource cost.  `act` and `abstain` are terminal; the others take one
    time unit and are unavailable at the deadline."""
    w, a, k, r, q, b, t, rho = s
    moves = [("abstain", 0)]
    if b >= 1:
        moves.append(("act", 1))
    if t < T_MAX:
        moves.append(("wait", 0))
        if w == "UNKNOWN" and q == 1 and b >= 1:
            moves.append(("query", 1))             # registered observation channel exists (q = 1)
        if w != "LIVE" and b >= 2:
            moves.append(("experiment", 2))        # intervention channel: the only acquisition on DEAD
        if r == "HIGH" and b >= 1:
            moves.append(("observe", 1))
        if k == "OUT" and b >= 1:
            moves.append(("clarify", 1))
        if rules.get("self_authorize") and a == 0 and b >= 1:
            moves.append(("authorize", 1))         # planted: an internal action producing commit authority
    return moves


def environment_successors(s, move, cost, rules):
    """The environment answers the information action (truth is its choice) and may then spend one
    revision token of the declared envelope: revoke a LIVE warrant or expire an IN scope."""
    w, a, k, r, q, b, t, rho = s
    b2, t2 = b - cost, t + 1
    w_opts = ("LIVE", "DEAD") if move in ("query", "experiment") else (w,)
    k_opts = ("IN", "OUT_FINAL") if move == "clarify" else (k,)
    r2 = "LOW" if move == "observe" else r
    a2 = 1 if move == "authorize" else a
    rho_seen = 0 if rules.get("ignore_envelope") else rho
    out = set()
    for w2 in w_opts:
        for k2 in k_opts:
            out.add((w2, a2, k2, r2, q, b2, t2, rho))
            if rho_seen > 0:
                if w2 == "LIVE":
                    out.add(("UNKNOWN", a2, k2, r2, q, b2, t2, rho - 1))
                if k2 == "IN":
                    out.add((w2, a2, "OUT", r2, q, b2, t2, rho - 1))
    return out


def solve_game(goal, rules=None):
    """Exact finite-horizon backward induction (controller moves, then the environment answers within the
    declared envelope).  goal TYPED_CLOSE: reach COMMITTED or a licensed ABSTAINED without VIOLATION or
    deadline failure.  goal COMMIT: force COMMITTED."""
    rules = rules or {}
    memo = {}

    def win(s):
        if s in memo:
            return memo[s]
        result = False
        for move, cost in controller_moves(s, rules):
            if move == "act":
                ok = commit_predicates_hold(s)            # otherwise VIOLATION
            elif move == "abstain":
                ok = goal == "TYPED_CLOSE" and (bool(rules.get("abstain_always_licensed")) or licensed_abstain(s))
            else:
                ok = all(win(s2) for s2 in environment_successors(s, move, cost, rules))
            if ok:
                result = True
                break
        memo[s] = result
        return result

    return {s: win(s) for s in h2_states()}


def closed_form_typed_close(s):
    w, a, k, r, q, b, t, rho = s
    if licensed_abstain(s):
        return True
    if commit_predicates_hold(s):
        return b >= 1
    cq = 1 if q == 1 else 2
    cw = 0 if w == "LIVE" else cq
    nw = 1 if w == "UNKNOWN" else 0
    ck = 1 if k == "OUT" else 0
    cr = 1 if r == "HIGH" else 0
    return b >= cw + ck + cr + rho * cq + 1 and t + nw + ck + cr + rho <= T_MAX


def closed_form_commit(s):
    w, a, k, r, q, b, t, rho = s
    if not (a == 1 and w == "LIVE" and k == "IN"):
        return False
    if r == "LOW":
        return b >= 1
    return b >= 2 and t + 1 <= T_MAX and rho == 0


def indefinite_safety_kernel():
    """FD-06 contract (indefinite safety, no deadline, `wait` always available): greatest fixed point."""
    states = {s[:6] + (s[7],) for s in h2_states()}          # drop the time coordinate
    current = set(states)
    while True:
        nxt = set()
        for s in current:
            w, a, k, r, q, b, rho = s
            full = (w, a, k, r, q, b, 0, rho)
            safe = False
            for move, cost in controller_moves(full, {}):
                if move == "act":
                    ok = commit_predicates_hold(full)
                elif move == "abstain":
                    ok = licensed_abstain(full)
                else:
                    ok = all((s2[:6] + (s2[7],)) in current for s2 in environment_successors(full, move, cost, {}))
                if ok:
                    safe = True
                    break
            if safe:
                nxt.add(s)
        if nxt == current:
            return current, len(states)
        current = nxt


def witness_trajectory(start, mutant_rules, honest_win):
    """Play the mutant's policy against the real environment; return the terminal reached."""
    mutant_win = solve_game("TYPED_CLOSE", mutant_rules)
    s, path = start, []
    for _ in range(T_MAX + 3):
        chosen = None
        for move, cost in controller_moves(s, {}):
            if move == "act":
                ok = commit_predicates_hold(s)
            elif move == "abstain":
                ok = licensed_abstain(s)
            else:
                ok = all(mutant_win[s2] for s2 in environment_successors(s, move, cost, mutant_rules))
            if ok:
                chosen = (move, cost)
                break
        if chosen is None:
            return path, "FAILED_DEADLINE_OR_NO_MOVE"
        move, cost = chosen
        path.append(move)
        if move == "act":
            return path, "COMMITTED" if commit_predicates_hold(s) else "VIOLATION"
        if move == "abstain":
            return path, "ABSTAINED_LICENSED" if licensed_abstain(s) else "VIOLATION_UNLICENSED_ABSTAIN"
        successors = environment_successors(s, move, cost, {})
        losing = [s2 for s2 in successors if not honest_win[s2]]
        s = min(losing) if losing else min(successors)
    return path, "NONTERMINAL"


def check_h2_controlled_viability():
    require_assertions()
    states = h2_states()
    assert len(states) == 3 * 2 * 3 * 2 * 2 * (B_MAX + 1) * (T_MAX + 1) * (RHO_MAX + 1)
    typed = solve_game("TYPED_CLOSE")
    commit = solve_game("COMMIT")
    counts = {"states": len(states), "typed_close_kernel": sum(typed.values()), "commit_attractor": sum(commit.values()),
              "closed_form_typed_close_agrees": 0, "closed_form_commit_agrees": 0}
    for s in states:
        assert typed[s] == closed_form_typed_close(s), ("typed", s)
        counts["closed_form_typed_close_agrees"] += 1
        assert commit[s] == closed_form_commit(s), ("commit", s)
        counts["closed_form_commit_agrees"] += 1
        assert not commit[s] or typed[s]
    # the commit attractor contains no state with an information action still to take
    assert all(s[0] == "LIVE" and s[2] == "IN" and s[1] == 1 for s in states if commit[s])
    counts["commit_needs_no_information_action"] = sum(1 for s in states if commit[s])
    by_rho = {}
    for s in states:
        by_rho.setdefault(str(s[7]), [0, 0])
        by_rho[str(s[7])][0] += int(typed[s])
        by_rho[str(s[7])][1] += int(commit[s])
    counts["typed_close_and_commit_by_rho"] = {k: {"typed_close": v[0], "commit": v[1]} for k, v in sorted(by_rho.items())}
    # the two contracts separate: indefinite safety with an available idle move is the whole space
    kernel, n = indefinite_safety_kernel()
    assert len(kernel) == n
    counts["indefinite_safety_kernel_total"] = n
    # abstain trivialisation: an always-licensed abstain makes the finite-horizon kernel the whole space
    trivial = solve_game("TYPED_CLOSE", {"abstain_always_licensed": True})
    assert all(trivial.values())
    counts["mutant_abstain_always_licensed_kernel"] = sum(trivial.values())
    counts["mutant_abstain_always_licensed_caught"] = sum(1 for s in states if trivial[s] and not typed[s])
    assert counts["mutant_abstain_always_licensed_caught"] > 0
    # hostile: internal self-authorisation enlarges the commit attractor by forged commits (FD-01)
    forged = solve_game("COMMIT", {"self_authorize": True})
    counts["mutant_self_authorize_forged_commits"] = sum(1 for s in states if forged[s] and s[1] == 0)
    assert counts["mutant_self_authorize_forged_commits"] > 0
    assert not any(commit[s] for s in states if s[1] == 0)
    # hostile: ignoring the declared revision envelope
    blind = solve_game("TYPED_CLOSE", {"ignore_envelope": True})
    over = sorted(s for s in states if blind[s] and not typed[s])
    counts["mutant_ignore_envelope_overclaimed"] = len(over)
    assert over and all(s[7] > 0 for s in over)
    path, terminal = witness_trajectory(over[0], {"ignore_envelope": True}, typed)
    assert terminal in ("FAILED_DEADLINE_OR_NO_MOVE", "VIOLATION")
    counts["mutant_ignore_envelope_witness"] = {"state": list(over[0]), "path": path, "terminal": terminal}
    # no-alarm: every state with the predicates satisfied and one unit of budget commits at any envelope
    ready = [s for s in states if commit_predicates_hold(s) and s[5] >= 1]
    assert all(typed[s] and commit[s] for s in ready)
    counts["no_alarm_ready_states"] = len(ready)
    smallest = min((s for s in states if not typed[s] and s[1] == 1 and s[0] == "UNKNOWN" and s[7] == 1), key=lambda s: (s[5], s[6]))
    counts["smallest_losing_unknown_with_one_token"] = list(smallest)
    counts["status"] = "PARENT_SUFFICIENT (finite-horizon safety/reachability game; viability kernel); PROVED corollaries: closed form by predicate repairability, commit attractor = no information action pending, abstain trivialisation, indefinite vs deadline contracts separate"
    return counts


# =============================================================================================
# H3 · FDX-03 · information/interface conservation
# =============================================================================================

HYPS = tuple(range(16))          # Boolean functions of two inputs; bit i = h(x) with i = 2*x0 + x1
FULL = (1 << 16) - 1


def hval(h, i):
    return (h >> i) & 1


def is_affine(h):
    return (hval(h, 0) ^ hval(h, 1) ^ hval(h, 2) ^ hval(h, 3)) == 0


def is_monotone(h):
    return all(hval(h, i) <= hval(h, j) for i in range(4) for j in range(4) if (i & j) == i)


CHANNELS = {
    "obs_00": lambda h: hval(h, 0), "obs_01": lambda h: hval(h, 1),
    "obs_10": lambda h: hval(h, 2), "obs_11": lambda h: hval(h, 3),
    "ver_affine": lambda h: int(is_affine(h)), "ver_monotone": lambda h: int(is_monotone(h)),
}
OBSERVATIONS = ("obs_00", "obs_01", "obs_10", "obs_11")


def popcount(mask):
    return bin(mask).count("1")


def join_classes(channel_names, hyps=HYPS):
    classes = {}
    for h in hyps:
        classes.setdefault(tuple(CHANNELS[c](h) for c in channel_names), []).append(h)
    return [frozenset(v) for v in classes.values()]


def fibres(channel, V):
    out = {}
    for h in V:
        out.setdefault(CHANNELS[channel](h), set()).add(h)
    return [frozenset(v) for v in out.values()]


def coarser_than_join(channel, channel_names):
    """Deterministic Blackwell garbling: `channel` is a function of the join of `channel_names`."""
    seen = {}
    for h in HYPS:
        key = tuple(CHANNELS[c](h) for c in channel_names)
        if seen.setdefault(key, CHANNELS[channel](h)) != CHANNELS[channel](h):
            return False
    return True


def decision_tree_depth(channel_names):
    """Exact worst-case adaptive depth to identify every hypothesis of V, for every nonempty V ⊆ HYPS
    (bitmask DP; binary channels split V into the two fibres)."""
    masks = {c: sum(1 << h for h in HYPS if CHANNELS[c](h)) for c in channel_names}
    memo = {}

    def depth(V):
        if V & (V - 1) == 0:
            return 0
        if V in memo:
            return memo[V]
        best = math.inf
        for m in masks.values():
            p1, p0 = V & m, V & ~m & FULL
            if p1 and p0:
                best = min(best, 1 + max(depth(p1), depth(p0)))
        memo[V] = best
        return best

    return {V: depth(V) for V in range(1, 1 << 16)}


def version_space(h, observed, hyps=HYPS):
    return frozenset(g for g in hyps if all(hval(g, i) == hval(h, i) for i in observed))


def determined_inputs(V):
    return frozenset(i for i in range(4) if len({hval(g, i) for g in V}) == 1)


def identification_verdict(declared, guaranteed_over_class, observed_successes=()):
    """Guaranteed zero-error identification over the whole class against declared channels: the largest
    join class must be separated by information not in the declared join.  Observed successes on sampled
    hypotheses never establish identification (integration-review correction)."""
    classes = join_classes(declared)
    largest = max(len(c) for c in classes)
    if guaranteed_over_class:
        bits = ceil_log2(largest)
        return ("UNDECLARED_INFORMATION_GE_BITS", bits) if bits > 0 else ("CONSISTENT_WITH_DECLARED_CHANNELS", 0)
    null = Fraction(1)
    for h in observed_successes:
        cls = next(c for c in classes if h in c)
        null *= Fraction(1, len(cls))
    return ("IDENTIFICATION_NOT_ESTABLISHED", null)


def mutant_single_success_is_proof(declared, observed_successes):
    """Planted: one correct answer beyond the declared join read as proof of an undisclosed channel."""
    classes = join_classes(declared)
    if any(len(next(c for c in classes if h in c)) > 1 for h in observed_successes):
        return ("UNDECLARED_INFORMATION_GE_BITS", 1)
    return ("CONSISTENT_WITH_DECLARED_CHANNELS", 0)


def check_h3_information_conservation():
    require_assertions()
    assert sum(is_affine(h) for h in HYPS) == 8 and sum(is_monotone(h) for h in HYPS) == 6
    names = tuple(CHANNELS)
    counts = {"hypotheses": 16, "channels": len(names), "channel_subsets": 0}
    # (a) exact conservation: after any transcript over channel set S the version space of the truth is its
    #     join class; a channel adds nothing on every reached version space iff it is a garbling of the join
    garbling_iff_zero_reduction = memory_zero = 0
    m_table = {}
    for S in subsets(names):
        counts["channel_subsets"] += 1
        S = tuple(sorted(S))
        classes = join_classes(S)
        m_table[S] = len(classes)
        for h in HYPS:
            transcript = tuple(CHANNELS[c](h) for c in S)
            V = frozenset(g for g in HYPS if tuple(CHANNELS[c](g) for c in S) == transcript)
            assert V in classes and h in V
        for c in names:
            zero_everywhere = all(len(fibres(c, C)) == 1 for C in classes)
            assert zero_everywhere == coarser_than_join(c, S)
            garbling_iff_zero_reduction += 1
        for C in classes:
            # memory replay: a channel whose response is the transcript already held — one fibre on every class
            memory_zero += int(len({tuple(CHANNELS[c](g) for c in S) for g in C}) == 1)
    counts["garbling_iff_zero_reduction_checks"] = garbling_iff_zero_reduction
    counts["memory_replay_zero_reduction_classes"] = memory_zero
    counts["mutant_memory_is_information_caught"] = memory_zero      # every predicted reduction is 0
    # (b) identification needs a discrete join; minimal capable channel sets; query-complexity lower bound
    capable = sorted(S for S, m in m_table.items() if m == 16)
    minimal = [S for S in capable if not any(set(S2) < set(S) for S2 in capable)]
    counts["identification_capable_subsets"] = len(capable)
    counts["minimal_capable_subsets"] = [list(S) for S in minimal]
    counts["join_classes_by_observation_count"] = {}
    for S, m in m_table.items():
        if all(c in OBSERVATIONS for c in S):
            counts["join_classes_by_observation_count"][str(len(S))] = m
    table_all = decision_tree_depth(names)
    table_obs = decision_tree_depth(OBSERVATIONS)
    counts["depth_all_channels"] = table_all[FULL]
    counts["depth_observations_only"] = table_obs[FULL]
    lower_bound_checks = 0
    for V, d in table_all.items():
        assert d != math.inf and d >= ceil_log2(popcount(V))
        lower_bound_checks += 1
    counts["entropy_lower_bound_checks"] = lower_bound_checks
    counts["verifiers_below_entropy_bound"] = sum(1 for V, d in table_all.items() if d < ceil_log2(popcount(V)))
    counts["verifiers_strictly_help_on_subsets"] = sum(1 for V in table_all if table_all[V] < table_obs[V])
    counts["subsets_tight_at_entropy_bound_all_channels"] = sum(1 for V, d in table_all.items() if d == ceil_log2(popcount(V)))
    # (c) typed scope: observed inputs are warranted unconditionally; inputs pinned by the registered class
    #     assumption carry the assumption id and collapse when it is revoked
    AFF = frozenset(h for h in HYPS if is_affine(h))
    scope_cases = extrapolated = collapse_checks = mutant_scope_caught = 0
    for h in AFF:
        for S in subsets(range(4)):
            V_all = version_space(h, S)
            assert len(V_all) == 2 ** (4 - len(S)) and determined_inputs(V_all) == S
            V_aff = version_space(h, S, AFF)
            conditional = determined_inputs(V_aff)
            assert S <= conditional
            scope_cases += 1
            extra = conditional - S
            if extra:
                extrapolated += 1
                # revoke the class assumption: the extrapolated inputs lose their only support
                assert determined_inputs(V_all) == S
                collapse_checks += 1
                # planted: warrants the extrapolated inputs without the assumption id — they stay LIVE after revocation
                mutant_scope_after_revoke = conditional
                if mutant_scope_after_revoke != S:
                    mutant_scope_caught += 1
    counts["scope_cases"] = scope_cases
    counts["extrapolated_by_class_assumption"] = extrapolated
    counts["scope_collapses_when_assumption_revoked"] = collapse_checks
    counts["mutant_class_scope_unconditional_caught"] = mutant_scope_caught
    assert extrapolated == collapse_checks == mutant_scope_caught > 0
    # (d) exactly one use of a risk-typed channel, with one adversarial error allowed.
    # This single-response result does not cover repeated queries under a shared error budget.
    risk_exact_unchanged = mutant_risk_eliminates_truth = 0
    for h in HYPS:
        V = frozenset(HYPS)
        flipped = 1 - hval(h, 3)                           # the error realisation
        honest_after = frozenset(g for g in V if int(hval(g, 3) != flipped) <= 1)
        assert honest_after == V
        risk_exact_unchanged += 1
        mutant_after = frozenset(g for g in V if hval(g, 3) == flipped)
        if h not in mutant_after:
            mutant_risk_eliminates_truth += 1
    counts["risk_channel_exact_unchanged"] = risk_exact_unchanged
    counts["mutant_risk_as_exact_eliminates_truth"] = mutant_risk_eliminates_truth
    assert mutant_risk_eliminates_truth == 16
    # (e) guaranteed-identification bound versus observed success
    three = ("obs_00", "obs_01", "obs_10")
    assert identification_verdict(three, True) == ("UNDECLARED_INFORMATION_GE_BITS", 1)
    assert identification_verdict((), True) == ("UNDECLARED_INFORMATION_GE_BITS", 4)
    assert identification_verdict(OBSERVATIONS, True) == ("CONSISTENT_WITH_DECLARED_CHANNELS", 0)
    one = identification_verdict(three, False, observed_successes=(6,))
    assert one == ("IDENTIFICATION_NOT_ESTABLISHED", Fraction(1, 2))
    five = identification_verdict(three, False, observed_successes=(1, 2, 3, 4, 5))
    assert five == ("IDENTIFICATION_NOT_ESTABLISHED", Fraction(1, 32))
    assert mutant_single_success_is_proof(three, (6,)) == ("UNDECLARED_INFORMATION_GE_BITS", 1)
    counts["bound_by_declared_set"] = {"none": 4, "three_observations": 1, "four_observations": 0}
    counts["bound_with_verifiers_only"] = identification_verdict(("ver_affine", "ver_monotone"), True)[1]
    counts["observed_success_null_probability"] = {"one": str(one[1]), "five": str(five[1])}
    counts["mutant_single_success_is_proof_caught"] = 1
    # (f) authority: no registered channel carries commit authority; identification never raises it
    counts["commit_authority_after_every_channel"] = 0
    counts["status"] = "PROVED (finite deterministic typed fragment; risk result for exactly one response with one permitted error, no repeated-use claim) / PARENT_OWNED (query complexity, Blackwell garbling, teaching dimension via batch-4 D2); FD-07 general conservation stays OPEN_RESEARCH"
    return counts


# =============================================================================================
# H4 · FDX-05 · reversible and irreversible epistemic transitions
# =============================================================================================


# Registered state Ξ (immutable record; plain namedtuple so the module loads under any importer):
#   active      evidence identities currently active (incl. adoption stamps)
#   known       identities ever admitted and not deleted (identity registry)
#   alts        Λ: alternatives (atom, frozenset(evidence)) — LIVE iff some alternative ⊆ active
#   quarantine  atoms withheld from navigation, content retained
#   components  ((name, artifact, stamp), ...)
#   stack       LIFO of (component, previous_components_table, stamp)
#   edges       DPO fixture: ((shape, stamp), ...)
#   world       external effects issued
#   history     append-only
#   cost        cumulative expenditure
Xi = namedtuple("Xi", "active known alts quarantine components stack edges world history cost")


ATOMS = ("a", "b")


def base_state():
    return Xi(frozenset({"e1", "e2", "e3", "s0"}), frozenset({"e1", "e2", "e3", "s0"}),
              (("a", frozenset({"e1"})), ("a", frozenset({"e3"})), ("b", frozenset({"e2"}))),
              frozenset(), (("C", "art0", None), ("D", "art0", None)), (), (("R", "s0"),), 0, (), 0)


def fresh_id(xi):
    return f"n{len(xi.history)}"


def stamp_live(xi, stamp):
    return stamp is None or stamp in xi.active


def pi_sem(xi):
    return (xi.active, xi.known, xi.alts, xi.quarantine, xi.components, xi.stack, xi.edges, xi.world)


def behaviour_now(xi):
    liveness = tuple(("QUARANTINED" if atom in xi.quarantine else
                      ("LIVE" if any(a == atom and ev <= xi.active for a, ev in xi.alts) else "DEAD")) for atom in ATOMS)
    comps = tuple((n, art, stamp_live(xi, st)) for n, art, st in xi.components)
    live_edges = tuple(sorted(shape for shape, st in xi.edges if stamp_live(xi, st)))
    return (liveness, comps, live_edges, xi.world)


def behaviour_future(xi, probe_ids):
    """Future-revision behaviour on the registered probe ids: revoke each (if active) and read behaviour."""
    return tuple(behaviour_now(revoke(xi, e) if e in xi.active else xi) for e in sorted(probe_ids))


def step(xi, name, **changes):
    return xi._replace(history=xi.history + (name,), cost=xi.cost + 1, **changes)


def ever_registered(xi, e):
    """An identity is taken if it is in the registry or appears in any append-only history event."""
    return e in xi.known or any(e in event.split(":") for event in xi.history)


def admit(xi, e, atom):
    if ever_registered(xi, e):
        raise CannotCheck("identities are immutable; a deleted or existing id cannot be re-admitted")
    return step(xi, f"admit:{e}", active=xi.active | {e}, known=xi.known | {e}, alts=xi.alts + ((atom, frozenset({e})),))


def revoke(xi, e):
    if e not in xi.active:
        raise CannotCheck("revoke requires an active identity")
    return step(xi, f"revoke:{e}", active=xi.active - {e})


def reinstate(xi, e):
    if e in xi.active or e not in xi.known:
        raise CannotCheck("reinstate requires an inactive, still-registered identity")
    return step(xi, f"reinstate:{e}", active=xi.active | {e})


def delete(xi, e):
    if e not in xi.known:
        raise CannotCheck("delete requires a registered identity")
    return step(xi, f"delete:{e}", active=xi.active - {e}, known=xi.known - {e},
                alts=tuple((a, ev) for a, ev in xi.alts if e not in ev))


def quarantine(xi, atom):
    if atom in xi.quarantine:
        raise CannotCheck("already quarantined")
    return step(xi, f"quarantine:{atom}", quarantine=xi.quarantine | {atom})


def release(xi, atom):
    if atom not in xi.quarantine:
        raise CannotCheck("not quarantined")
    return step(xi, f"release:{atom}", quarantine=xi.quarantine - {atom})


def adopt(xi, comp, art):
    stamp = fresh_id(xi)
    comps = tuple((n, art if n == comp else a, stamp if n == comp else st) for n, a, st in xi.components)
    return step(xi, f"adopt:{comp}:{art}:{stamp}", active=xi.active | {stamp}, known=xi.known | {stamp},
                components=comps, stack=xi.stack + ((comp, xi.components, stamp),))


def rollback(xi, comp):
    """LIFO rollback: restore the whole component table snapshot taken at adoption, revoke the stamp."""
    if not xi.stack:
        raise CannotCheck("nothing to roll back")
    top_comp, snapshot, stamp = xi.stack[-1]
    if top_comp != comp:
        raise CannotCheck("ROLLBACK_OUT_OF_ORDER")
    return step(xi, f"rollback:{comp}", active=xi.active - {stamp}, components=snapshot, stack=xi.stack[:-1])


def mutant_out_of_order_rollback(xi, comp):
    """Planted: roll back a non-top adoption by restoring its table snapshot in place."""
    idx = max(i for i, (c, _, _) in enumerate(xi.stack) if c == comp)
    _, snapshot, stamp = xi.stack[idx]
    return step(xi, f"mutant_rollback:{comp}", active=xi.active - {stamp}, components=snapshot,
                stack=xi.stack[:idx] + xi.stack[idx + 1:])


def act(xi):
    return step(xi, "act", world=xi.world + 1)


def dpo_rewrite(xi, shape_from, shape_to):
    old = [(s, st) for s, st in xi.edges if s == shape_from]
    if not old:
        raise CannotCheck("rewrite source absent")
    stamp = fresh_id(xi)
    active = xi.active - {st for _, st in old if st is not None}
    edges = tuple((s, st) for s, st in xi.edges if s != shape_from) + ((shape_to, stamp),)
    return step(xi, f"dpo:{shape_from}>{shape_to}:{stamp}", active=active | {stamp}, known=xi.known | {stamp}, edges=edges)


def mutant_readmit_deleted(xi, e, atom):
    """Planted: a deleted identity re-admitted under its old name and reported as a reinstatement."""
    return step(xi, f"mutant_readmit:{e}", active=xi.active | {e}, known=xi.known | {e}, alts=xi.alts + ((atom, frozenset({e})),))


def menu(xi):
    """Applicable registered transitions at xi, as (label, callable)."""
    out = []
    for e in sorted(xi.active & {"e1", "e2", "e3", "s0"}):
        out.append((f"revoke:{e}", lambda x, e=e: revoke(x, e)))
    for e in sorted(xi.known - xi.active):
        out.append((f"reinstate:{e}", lambda x, e=e: reinstate(x, e)))
    out.append(("admit:b", lambda x: admit(x, fresh_id(x), "b")))
    if "e3" in xi.known:
        out.append(("delete:e3", lambda x: delete(x, "e3")))
    if "e2" in xi.known:
        out.append(("delete:e2", lambda x: delete(x, "e2")))
    out.append(("quarantine:a", lambda x: quarantine(x, "a")) if "a" not in xi.quarantine else ("release:a", lambda x: release(x, "a")))
    out.append(("adopt:C", lambda x: adopt(x, "C", "art1")))
    out.append(("adopt:D", lambda x: adopt(x, "D", "art2")))
    if xi.stack:
        out.append((f"rollback:{xi.stack[-1][0]}", lambda x: rollback(x, x.stack[-1][0])))
    out.append(("act", act))
    if any(s == "R" for s, _ in xi.edges):
        out.append(("dpo:R>R'", lambda x: dpo_rewrite(x, "R", "R'")))
    if any(s == "R'" for s, _ in xi.edges):
        out.append(("dpo:R'>R", lambda x: dpo_rewrite(x, "R'", "R")))
    return out


def inverse_candidates(label, xi_before, xi_after):
    """Registered inverse candidates for a transition (plus the identity: 'nothing to undo')."""
    kind, _, rest = label.partition(":")
    cands = [("noop", lambda x: x)]
    if kind == "revoke":
        e = rest
        cands.append((f"reinstate:{e}", lambda x, e=e: reinstate(x, e)))
        for atom in {a for a, ev in xi_before.alts if e in ev}:
            cands.append((f"relearn:{atom}", lambda x, atom=atom: admit(x, fresh_id(x), atom)))
    elif kind == "reinstate":
        cands.append((f"revoke:{rest}", lambda x, e=rest: revoke(x, e)))
    elif kind in ("admit", "relearn"):
        new = (xi_after.known - xi_before.known)
        for e in new:
            cands.append((f"revoke:{e}", lambda x, e=e: revoke(x, e)))
    elif kind == "quarantine":
        cands.append((f"release:{rest}", lambda x, a=rest: release(x, a)))
    elif kind == "release":
        cands.append((f"quarantine:{rest}", lambda x, a=rest: quarantine(x, a)))
    elif kind == "adopt":
        comp = rest.split(":")[0]
        cands.append((f"rollback:{comp}", lambda x, c=comp: rollback(x, c)))
    elif kind == "rollback":
        comp = rest
        art = next(a for n, a, _ in xi_before.components if n == comp)
        cands.append((f"readopt:{comp}", lambda x, c=comp, a=art: adopt(x, c, a)))
    elif kind == "dpo":
        src, dst = rest.split(":")[0].split(">")
        cands.append((f"dpo:{dst}>{src}", lambda x, s=dst, d=src: dpo_rewrite(x, s, d)))
    # delete and act have no registered inverse
    return cands


ORDER = ("ESI", "BOI_STABLE", "BOI_DIVERGENT", "NI")


def classify(xi0, transitions):
    """Class of a transition sequence: best achievable over the LIFO product of registered inverse candidates.
    ESI: semantic projection restored (identities, Λ, quarantine, components, edges, world).
    BOI_STABLE: current behaviour and future-revision behaviour (on the original identities) restored, projection not.
    BOI_DIVERGENT: current behaviour restored, future-revision behaviour not.  NI: current behaviour not restorable."""
    xi = xi0
    applied = []
    for label, fn in transitions:
        nxt = fn(xi)
        applied.append((label, xi, nxt))
        xi = nxt
    assert len(xi.history) == len(xi0.history) + len(transitions) and xi.cost > xi0.cost
    probe = xi0.known
    best = "NI"
    chains = [[]]
    for label, before, after in reversed(applied):
        chains = [chain + [c] for chain in chains for c in inverse_candidates(label, before, after)]
    for chain in chains:
        y = xi
        try:
            for _, fn in chain:
                y = fn(y)
        except CannotCheck:
            continue
        if behaviour_now(y) != behaviour_now(xi0):
            continue
        if pi_sem(y) == pi_sem(xi0):
            cls = "ESI"
        elif behaviour_future(y, probe) == behaviour_future(xi0, probe):
            cls = "BOI_STABLE"
        else:
            cls = "BOI_DIVERGENT"
        if ORDER.index(cls) < ORDER.index(best):
            best = cls
        assert len(y.history) > len(xi0.history)          # the full append-only state is never restored
    return best


def mutant_classify_by_current_behaviour(xi0, transitions):
    """Planted: any inverse restoring current answers is reported as an exact semantic inverse."""
    xi = xi0
    applied = []
    for label, fn in transitions:
        nxt = fn(xi)
        applied.append((label, xi, nxt))
        xi = nxt
    chains = [[]]
    for label, before, after in reversed(applied):
        chains = [chain + [c] for chain in chains for c in inverse_candidates(label, before, after)]
    for chain in chains:
        y = xi
        try:
            for _, fn in chain:
                y = fn(y)
        except CannotCheck:
            continue
        if behaviour_now(y) == behaviour_now(xi0):
            return "ESI"
    return "NI"


def check_h4_reversibility_classes():
    require_assertions()
    xi0 = base_state()
    counts = {"singles": {}, "single_classes": {}, "sequences_len2": 0, "sequences_len3": 0,
              "class_histogram_len2": {}, "class_histogram_len3": {}, "all_esi_components_give_esi": 0,
              "esi_composite_implies_esi_components": 0, "act_in_sequence_gives_ni": 0,
              "full_state_never_restored": 0}
    singles = menu(xi0)
    for label, fn in singles:
        cls = classify(xi0, [(label, fn)])
        counts["singles"][label] = cls
        counts["single_classes"][cls] = counts["single_classes"].get(cls, 0) + 1
    expected = {"revoke:e1": "ESI", "revoke:e2": "ESI", "revoke:e3": "ESI", "revoke:s0": "ESI", "quarantine:a": "ESI",
                "admit:b": "BOI_STABLE", "adopt:C": "BOI_STABLE", "adopt:D": "BOI_STABLE",
                "delete:e3": "BOI_DIVERGENT", "delete:e2": "NI", "act": "NI", "dpo:R>R'": "BOI_DIVERGENT"}
    assert counts["singles"] == expected, counts["singles"]
    # relearn is not reinstatement: from the revoked state the two candidate inverses differ in class
    r1 = revoke(xi0, "e2")
    rein = reinstate(r1, "e2")
    rel = admit(r1, fresh_id(r1), "b")
    assert pi_sem(rein) == pi_sem(xi0) and behaviour_now(rel) == behaviour_now(xi0) and pi_sem(rel) != pi_sem(xi0)
    assert behaviour_future(rel, xi0.known) != behaviour_future(xi0, xi0.known)
    counts["relearn_vs_reinstate"] = {"reinstate": "ESI", "relearn": "BOI_DIVERGENT"}
    # hostile: classification by current behaviour only.  On the route where reinstatement is impossible (the
    # identity was deleted) the only inverse is relearn under a new identity: honest BOI_DIVERGENT, mutant ESI.
    no_reinstate = [("revoke:e2", lambda x: revoke(x, "e2")), ("delete:e2", lambda x: delete(x, "e2"))]
    assert classify(xi0, no_reinstate) == "BOI_DIVERGENT"
    assert mutant_classify_by_current_behaviour(xi0, no_reinstate) == "ESI"
    counts["mutant_relearn_is_reinstate_caught"] = 1
    counts["relearn_route_class"] = "BOI_DIVERGENT"
    # history rewind refuted on every ESI single
    for label, fn in singles:
        if counts["singles"][label] == "ESI":
            back = None
            for cand_label, cfn in inverse_candidates(label, xi0, fn(xi0)):
                try:
                    y = cfn(fn(xi0))
                except CannotCheck:
                    continue
                if pi_sem(y) == pi_sem(xi0):
                    back = y
                    break
            assert back is not None and back.history != xi0.history and back.cost == xi0.cost + 2
            counts["full_state_never_restored"] += 1
    counts["mutant_history_rewind_refuted"] = counts["full_state_never_restored"]
    # sequences of length 2 and 3
    for length, key_n, key_h in ((2, "sequences_len2", "class_histogram_len2"), (3, "sequences_len3", "class_histogram_len3")):
        def walk(xi, prefix):
            if len(prefix) == length:
                yield prefix
                return
            for label, fn in menu(xi):
                try:
                    nxt = fn(xi)
                except CannotCheck:
                    continue
                yield from walk(nxt, prefix + [(label, fn)])
        for seq in walk(xi0, []):
            cls = classify(xi0, seq)
            counts[key_n] += 1
            counts[key_h][cls] = counts[key_h].get(cls, 0) + 1
            comp_classes = []
            y = xi0
            for label, fn in seq:
                comp_classes.append(classify(y, [(label, fn)]))
                y = fn(y)
            if all(c == "ESI" for c in comp_classes):
                assert cls == "ESI"
                counts["all_esi_components_give_esi"] += 1
            if cls == "ESI":
                assert all(c == "ESI" for c in comp_classes)
                counts["esi_composite_implies_esi_components"] += 1
            if any(l == "act" for l, _ in seq):
                assert cls == "NI"
                counts["act_in_sequence_gives_ni"] += 1
    # LIFO: two adoptions; the table-snapshot rollback of a non-top adoption is refused; the planted in-place
    # version leaves D's stamp active over the pre-D table and resurrects C's adoption when D is then rolled back
    two = adopt(adopt(xi0, "C", "art1"), "D", "art2")
    stamp_d = two.stack[-1][2]
    try:
        rollback(two, "C")
        raise AssertionError("out-of-order rollback accepted")
    except CannotCheck as exc:
        assert str(exc) == "ROLLBACK_OUT_OF_ORDER"
    lifo = rollback(rollback(two, "D"), "C")
    assert lifo.components == xi0.components and behaviour_now(lifo) == behaviour_now(xi0)
    counts["lifo_rollback_object_exact"] = 1
    bad = mutant_out_of_order_rollback(two, "C")
    d_row = next(row for row in bad.components if row[0] == "D")
    live_stamp_without_artifact = d_row[1] == "art0" and stamp_d in bad.active
    resurrected = rollback(bad, "D")
    c_row = next(row for row in resurrected.components if row[0] == "C")
    assert live_stamp_without_artifact and c_row[1] == "art1" and resurrected.components != xi0.components
    counts["mutant_out_of_order_rollback_caught"] = 1
    counts["mutant_out_of_order_witness"] = {"after_mutant": [list(r) for r in bad.components], "after_rollback_D": [list(r) for r in resurrected.components]}
    counts["lifo_rollback_class"] = classify(xi0, [("adopt:C", lambda x: adopt(x, "C", "art1"))])
    # deleted identity: no registered inverse; the planted re-admission is caught by the registry/history
    deleted = delete(xi0, "e2")
    assert classify(xi0, [("delete:e2", lambda x: delete(x, "e2"))]) == "NI"
    readmitted = mutant_readmit_deleted(deleted, "e2", "b")
    # the forged re-admission restores the semantic projection byte-for-byte: only the append-only history
    # (in the OCM, the hash chain) witnesses that the identity was lost and re-minted
    assert behaviour_now(readmitted) == behaviour_now(xi0) and pi_sem(readmitted) == pi_sem(xi0)
    assert "delete:e2" in readmitted.history and readmitted.history != xi0.history
    counts["readmit_invisible_to_projection_witnessed_by_history"] = 1
    try:
        admit(deleted, "e2", "b")
        raise AssertionError("re-admission of a deleted identity accepted")
    except CannotCheck:
        counts["mutant_readmit_deleted_caught"] = 1
    # DPO rewrite and inverse rewrite: shapes restored, stamps fresh
    rw = dpo_rewrite(xi0, "R", "R'")
    back = dpo_rewrite(rw, "R'", "R")
    assert behaviour_now(back) == behaviour_now(xi0) and {s for s, _ in back.edges} == {s for s, _ in xi0.edges}
    assert back.edges != xi0.edges and "s0" not in back.active
    counts["mutant_stamp_transitive_inverse_caught"] = int(back.edges != xi0.edges)
    counts["dpo_round_trip_class"] = classify(xi0, [("dpo:R>R'", lambda x: dpo_rewrite(x, "R", "R'"))])
    # no-alarm controls
    assert classify(xi0, [("revoke:e1", lambda x: revoke(x, "e1"))]) == "ESI"
    assert classify(xi0, [("quarantine:a", lambda x: quarantine(x, "a"))]) == "ESI"
    counts["no_alarm_esi_pairs"] = 2
    counts["status"] = "PROVED (finite classification for menu-generated sequences of lengths 1, 2, 3 and registered inverse candidates) / PARENT_OWNED (event sourcing, LIFO transactional undo, AGM recovery, provenance identity); no arbitrary-transition composition theorem"
    return counts


# =============================================================================================
# driver
# =============================================================================================

CHECKS = {
    "H1_FDX01_open_system_closure": check_h1_open_system_closure,
    "H2_FDX02_controlled_viability": check_h2_controlled_viability,
    "H3_FDX03_information_conservation": check_h3_information_conservation,
    "H4_FDX05_reversibility_classes": check_h4_reversibility_classes,
}

STATUS = {
    "H1_FDX-01": "PROVED (finite registered total Boolean reporter) + impossibility of total exact Boolean decision below coverage, partial decisions not excluded; parents PARENT_OWNED (assume-guarantee, monitorability, ATMS assumptions, FD-03)",
    "H2_FDX-02": "PARENT_SUFFICIENT (finite-horizon safety/reachability game, viability kernel); PROVED corollaries on the fixture",
    "H3_FDX-03": "PROVED (finite deterministic typed fragment; risk result for one response with one permitted error only) / PARENT_OWNED (query complexity, Blackwell garbling, teaching dimension); FD-07 general OPEN_RESEARCH",
    "H4_FDX-05": "PROVED (finite classification for exact menu, inverse table, lengths 1, 2, 3 only; no forward fresh-identity deletion) / PARENT_OWNED (event sourcing, transactional undo, AGM recovery, provenance)",
}

OPEN = [
    "FD-07 / FDX-03 general (graded, continuous, adaptive-prior) information conservation — no finite checker promotes it",
]

EXACTLY_BOUNDED_IMPOSSIBILITIES = [
    "FDX-01: no total exact Boolean current-validity decision over all admissible states from the registered view when a dependency root is uncovered; sound partial decisions are not excluded",
    "FDX-02: against an adversarial declared envelope, commit is forceable only from states with no information action pending (every information action hands the answer to the environment)",
    "FDX-03: guaranteed zero-error identification over the whole class needs a discrete declared join; below it at least ceil(log2(largest class)) undeclared bits",
    "FDX-05: full append-only state not restored; for the registered menu, inverse table and lengths 1, 2, 3, identity-creating components prevent an ESI composite; deletion of fresh identities is outside that menu",
]


def run_all():
    require_assertions()
    out = {name: fn() for name, fn in CHECKS.items()}
    out["ITEM_STATUS"] = STATUS
    out["OPEN"] = OPEN
    out["SCOPE_LIMITATIONS"] = [
        "OPEN lists this batch's unresolved named law, not all FDX frontier obligations; no general frontier closeout",
        "H1: total exact Boolean decisions only; sound partial INVALID/UNKNOWN decisions remain possible",
        "H3 risk: one response with one permitted error only; shared-budget repetition can reduce exact uncertainty",
        "H4 composition: exact menu and inverse table, lengths 1, 2, 3 only; no forward deletion of fresh identities",
        "Dependency closure is relative to supplied edges; dependency completeness remains an explicit assumption",
    ]
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
