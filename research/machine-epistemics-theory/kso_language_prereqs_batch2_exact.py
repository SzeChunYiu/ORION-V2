"""Exact finite checker for KSO_LANGUAGE_PREREQUISITE_THEOREMS_BATCH2_V1.md (stdlib only, exact).

One check function per theorem (B1–B8, atlas ids MEG-05/12/13/24/03/17/19/28).  Every check performs
(a) the positive statement, (b) a planted mutant whose mutation is asserted applied and which must be
caught, and (c) a no-alarm control.  The minimal objects of the OCM core are re-implemented here
(antichain semiring, warrant intervals, Kleene liveness, authority meet, epoch scopes, frozen-
denominator navigation, impact cone / reopening report, version spaces, typed hypergraph fragments,
DPO rewriting); nothing is imported from ``ocm``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import random
import sys
from fractions import Fraction

INF = float("inf")


class CannotCheck(RuntimeError):
    pass


# ---------------------------------------------------------------------------------------------
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21)
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


def ijoin(p, q):
    return (join(p[0], q[0]), join(p[1], q[1]))


def cert(*warrants):
    p = canon(frozenset(w) for w in warrants)
    return (p, p)


IONE = (ONE, ONE)
IUNKNOWN = (ZERO, ONE)   # partial: nothing exhibited, anything might still warrant it


def evidence_of(iv):
    return frozenset(e for side in iv for w in side for e in w)


def subsets(universe):
    u = sorted(universe, key=repr)
    return [frozenset(c) for k in range(len(u) + 1) for c in itertools.combinations(u, k)]


def all_profiles(n):
    subs = subsets(range(n))
    out = set()
    for mask in range(1 << len(subs)):
        out.add(canon([subs[i] for i in range(len(subs)) if mask & (1 << i)]))
    return sorted(out, key=lambda p: (len(p), [sorted(w) for w in p]))


def all_intervals(n):
    ps = all_profiles(n)
    return [(lo, up) for lo in ps for up in ps if leq(lo, up)]


# ---------------------------------------------------------------------------------------------
# authority meet (MEG-04 / batch-1 T1), typed hypergraph, navigation, impact cone, reopening
# ---------------------------------------------------------------------------------------------

COORDS = ("world_truth", "speaker", "task_contract", "commit")
DEPENDENCY = frozenset({"DEPENDENCE", "SUPPORT", "COMPOSITION", "CONSTRAINT"})


def auth_meet(*items):
    keys = set().union(*(set(a) for a in items))
    return {k: min(a.get(k, 0) for a in items) for k in keys}


def edge(eid, tails, heads, w=1, hw=None, iv=IONE, rel="DEPENDENCE"):
    tails = (tails,) if isinstance(tails, str) else tuple(tails)
    heads = (heads,) if isinstance(heads, str) else tuple(heads)
    return (eid, tails, heads, Fraction(w), tuple(Fraction(x) for x in (hw or [1] * len(heads))), iv, rel)


def nav_matrix(atoms, edges, revoked):
    """Gated matrix with denominators frozen on the registered structure; dead mass dissipates."""
    ids = list(atoms)
    idx = {x: i for i, x in enumerate(ids)}
    out = [[Fraction(0) for _ in ids] for _ in ids]
    denom = {x: Fraction(0) for x in ids}
    for _, tails, _, w, _, _, _ in edges:
        for t in tails:
            denom[t] += w
    lv = {x: liveness(atoms[x], revoked) == LIVE for x in ids}
    for _, tails, heads, w, hw, ew, _ in edges:
        if w == 0 or liveness(ew, revoked) != LIVE or not all(lv[t] for t in tails):
            continue
        total = sum(hw, Fraction(0))
        for t in tails:
            if denom[t] == 0:
                continue
            for h, x in zip(heads, hw):
                if lv[h]:
                    out[idx[t]][idx[h]] += (w / denom[t]) * (x / total)
    return ids, out


def fixed_point(p, seed, alpha):
    n = len(p)
    aug = [[Fraction(int(i == j)) - (1 - alpha) * p[j][i] for j in range(n)] + [alpha * seed[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if piv is None:
            raise CannotCheck("singular navigation system")
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return [row[-1] for row in aug]


def activation(atoms, edges, revoked, seed_atom, alpha=Fraction(1, 3)):
    ids, p = nav_matrix(atoms, edges, revoked)
    seed = [Fraction(int(x == seed_atom)) * (1 if liveness(atoms[x], revoked) == LIVE else 0) for x in ids]
    return dict(zip(ids, fixed_point(p, seed, alpha)))


def impact_cone(changed, edges):
    """Impact_D(X): least dependency-closed superset (KS-T09) over dependency relation types only."""
    out = set(changed)
    grew = True
    while grew:
        grew = False
        for _, tails, heads, *_, rel in edges:
            if rel in DEPENDENCY and any(t in out for t in tails):
                for h in heads:
                    if h not in out:
                        out.add(h)
                        grew = True
    return frozenset(out)


def forward_reach(start, edges):
    out = set(start)
    grew = True
    while grew:
        grew = False
        for _, tails, heads, *_ in edges:
            if any(t in out for t in tails):
                for h in heads:
                    if h not in out:
                        out.add(h)
                        grew = True
    return frozenset(out)


def reopening_report(atoms, edges, r0, r1):
    """KS-T22: (REOPEN, RECHECK, UNAFFECTED) for the delta R0 → R1."""
    changed = {x for x in atoms if liveness(atoms[x], r0) != liveness(atoms[x], r1)}
    for _, _, heads, _, _, ew, _ in edges:
        if liveness(ew, r0) != liveness(ew, r1):
            changed.update(heads)
    cone = impact_cone(changed, edges)
    return {"changed": frozenset(changed), "cone": cone, "reopen": cone & changed, "recheck": cone - changed, "unaffected": frozenset(atoms) - cone}


# ---------------------------------------------------------------------------------------------
# B1 · MEG-05 · discourse-state warrant: said / committed / Λ_machine, non-laundering
# ---------------------------------------------------------------------------------------------

OP_AUTHORITY = {"world_truth": 2, "speaker": 2, "task_contract": 2}   # internal operator: commit undeclared = 0


def said(speaker, prop, transcript_evidence):
    """OBSERVATION atom certified by the transcript hash: authority `speaker` only."""
    return {"kind": "said", "who": speaker, "prop": prop, "iv": cert({transcript_evidence}), "auth": {"speaker": 1}, "scope": frozenset({"conversation"})}


def committed(speaker, prop, said_atoms):
    """Derived atom (scope = conversation): warrant ⊗ of the said atoms, authority the internal meet."""
    iv = IONE
    for s in said_atoms:
        iv = imeet(iv, s["iv"])
    return {"kind": "committed", "who": speaker, "prop": prop, "iv": iv, "auth": auth_meet(OP_AUTHORITY, *(s["auth"] for s in said_atoms)), "scope": frozenset({"conversation"})}


def compose_discourse(atoms, mode="meet"):
    """Any internal composition of discourse atoms: warrant ⊗ (or ⊕), authority the meet with the operator."""
    iv = IONE if mode == "meet" else (ZERO, ZERO)
    for a in atoms:
        iv = imeet(iv, a["iv"]) if mode == "meet" else ijoin(iv, a["iv"])
    return {"kind": "composed", "prop": atoms[0]["prop"], "iv": iv, "auth": auth_meet(OP_AUTHORITY, *(a["auth"] for a in atoms)), "scope": frozenset({"conversation"})}


def machine_interval(prop, store):
    """Λ_machine(p): ⊕ over the atoms asserting p that carry world_truth authority ≥ 1; else ⟦0,1⟧."""
    authorised = [a["iv"] for a in store if a["prop"] == prop and a["auth"].get("world_truth", 0) >= 1]
    if not authorised:
        return IUNKNOWN
    out = (ZERO, ZERO)
    for iv in authorised:
        out = ijoin(out, iv)
    return out


def promote(dialogue_object, scope, bridge=None):
    """propose_promote = an admit transaction: warrant Λ_bridge (world-warranting tails), authority the
    meet of operator and tails; the dialogue object is provenance (REPORTED_BY, non-dependency)."""
    tails = [bridge] if bridge is not None else [dialogue_object]
    iv = IONE
    for t in tails:
        iv = imeet(iv, t["iv"])
    auth = auth_meet(OP_AUTHORITY, *(t["auth"] for t in tails))
    return {"kind": "machine", "prop": dialogue_object["prop"], "iv": iv, "auth": auth, "scope": frozenset(scope), "reported_by": dialogue_object["who"]}


def mutant_majority_promote(said_atoms, k):
    """Planted (KS-T23 shape): ≥ k speakers agreeing mints world_truth 1 and a ⊕-merged warrant."""
    if len(said_atoms) < k:
        return None
    iv = (ZERO, ZERO)
    for s in said_atoms:
        iv = ijoin(iv, s["iv"])
    return {"kind": "machine", "prop": said_atoms[0]["prop"], "iv": iv, "auth": {"speaker": 1, "world_truth": 1}, "scope": frozenset({"conversation"})}


def check_b1_meg05_discourse_state():
    p, q = "Paris is in Germany", "Paris is in France"
    store = []
    one = said("u1", p, "t_u1")
    store += [one, committed("u1", p, [one])]
    assert machine_interval(p, store) == IUNKNOWN and liveness(machine_interval(p, store), set()) == UNKNOWN
    assert store[-1]["auth"].get("world_truth", 0) == 0
    ten = [said(f"u{i}", p, f"t_u{i}") for i in range(1, 11)]
    store += ten
    composed_meet, composed_join = compose_discourse(ten, "meet"), compose_discourse(ten, "join")
    store += [composed_meet, composed_join]
    assert composed_meet["auth"].get("world_truth", 0) == 0 and composed_join["auth"].get("world_truth", 0) == 0
    assert liveness(composed_join["iv"], set()) == LIVE  # LIVE as a speech record, yet not machine knowledge
    assert machine_interval(p, store) == IUNKNOWN            # ten speakers compose to the same bottom
    assert composed_meet["scope"] == frozenset({"conversation"})
    # exhaustive: every chain of internal compositions over speaker-layer atoms keeps world_truth = 0
    chains = 0
    for ranks in itertools.product(range(3), repeat=3):
        a = {"speaker": ranks[0], "task_contract": ranks[1], "commit": ranks[2]}  # world_truth undeclared = 0
        acc = a
        for _ in range(10):
            acc = auth_meet(OP_AUTHORITY, acc, a)
            assert acc.get("world_truth", 0) == 0
            chains += 1
    # promote without a bridge is the same bottom (authority meet cannot raise)
    no_bridge = promote(one, {"conversation"})
    assert no_bridge["auth"].get("world_truth", 0) == 0 and no_bridge["auth"].get("commit", 0) == 0
    store.append(no_bridge)
    assert machine_interval(p, store) == IUNKNOWN
    # retraction of an un-admitted claim: machine knowledge unchanged (evidence disjoint, KS-T22 C = ∅)
    before = machine_interval(p, store)
    for R in ({"t_u1"}, {f"t_u{i}" for i in range(1, 11)}):
        assert machine_interval(p, store) == before and liveness(before, R) == UNKNOWN
    # a registered OBSERVATION bridge (gazetteer lookup) makes a different proposition LIVE
    gaz = {"kind": "observation", "prop": q, "iv": cert({"e_gazetteer"}), "auth": {"world_truth": 1, "speaker": 0}, "scope": frozenset({"world"})}
    said_q = said("u2", q, "t_u2")
    store += [said_q, promote(said_q, {"world"}, bridge=gaz)]
    mq = machine_interval(q, store)
    assert liveness(mq, set()) == LIVE and store[-1]["auth"]["world_truth"] == 1 and store[-1]["auth"].get("commit", 0) == 0
    assert liveness(mq, {"t_u2", "t_u1"}) == LIVE          # no-alarm: transcripts are not its evidence
    assert liveness(mq, {"e_gazetteer"}) == DEAD            # and the bridge evidence is
    assert machine_interval(p, store) == IUNKNOWN            # p untouched by q's bridge
    # planted majority mutant
    bad = mutant_majority_promote(ten, 3)
    assert bad is not None and bad["auth"]["world_truth"] == 1 and liveness(bad["iv"], set()) == LIVE  # mutation applied
    assert bad["auth"]["world_truth"] > auth_meet(OP_AUTHORITY, *(s["auth"] for s in ten)).get("world_truth", 0)
    assert liveness(machine_interval(p, store + [bad]), set()) == LIVE and liveness(machine_interval(p, store), set()) == UNKNOWN
    return {"speakers": 10, "said_layer_world_truth_zero": 1, "meet_and_join_compositions_bottom": 2, "authority_chains_checked": chains, "promote_without_bridge_bottom": 1, "retraction_leaves_machine_unchanged": 2, "bridge_makes_other_proposition_live": 1, "bridge_evidence_is_the_only_support": 1, "mutant_majority_promote_caught": 1}


# ---------------------------------------------------------------------------------------------
# B2 · MEG-12 · per-input version-space warrant (VSW) and per-input reopening
# ---------------------------------------------------------------------------------------------

INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
ALL16 = tuple(itertools.product((0, 1), repeat=4))
AFFINE8 = tuple(t for t in ALL16 if sum(t) % 2 == 0)
MONOTONE6 = tuple(t for t in ALL16 if all(t[i] <= t[j] for i in range(4) for j in range(4) if all(a <= b for a, b in zip(INPUTS[i], INPUTS[j]))))
CLASSES = {"ALL16": ALL16, "AFFINE8": AFFINE8, "MONOTONE6": MONOTONE6}


def version_space(cls, examples):
    return [h for h in cls if all(h[i] == v for i, v in examples.items())]


def agrees_at(vs, i):
    return bool(vs) and len({h[i] for h in vs}) == 1


def vsw(cls, S, inputs):
    """Per-input warrant W(x) for x ∈ inputs: the antichain of minimal J ⊆ S with V(J) agreeing at x.
    S: {input_index: (value, evidence_id)}.  Certified (exhaustive over 2^|S|), so ⟦W, W⟧."""
    out = {}
    idxs = list(S)
    for i in inputs:
        working = []
        for J in subsets(idxs):
            if agrees_at(version_space(cls, {j: S[j][0] for j in J}), i):
                working.append(frozenset(S[j][1] for j in J))
        out[i] = canon(working)
    return out


def vsw_family(cls, S, Q):
    """Minimal J with V(J) agreeing on all of Q, computed directly (must equal ⊗_{q∈Q} W(q))."""
    working = []
    for J in subsets(list(S)):
        vs = version_space(cls, {j: S[j][0] for j in J})
        if all(agrees_at(vs, q) for q in Q):
            working.append(frozenset(S[j][1] for j in J))
    return canon(working)


def reopen_per_input(W, e):
    """Inputs whose every minimal agreement set contains e (KS-T22 applied per input)."""
    return frozenset(i for i, w in W.items() if w and all(e in J for J in w))


def mutant_whole_procedure_reopen(W, S, e):
    """Planted: one warrant {all examples} for the whole procedure — any example revocation reopens
    every input that was live."""
    whole = canon([frozenset(v[1] for v in S.values())])
    return frozenset(i for i, w in W.items() if w and not live(whole, {e}))


def check_b2_meg12_per_input_vsw():
    exact = 0
    reopen_eq = 0
    mutant_over = 0
    mutant_checks = 0
    no_alarm = 0
    family_eq = 0
    per_class = {}
    for name, cls in CLASSES.items():
        strict_witness = 0
        for target in cls:
            for chosen in subsets(range(4)):
                S = {i: (target[i], f"e{i}") for i in sorted(chosen)}
                W = vsw(cls, S, range(4))
                ev = {v[1] for v in S.values()}
                for R in subsets(ev):
                    remaining = {i: S[i][0] for i in S if S[i][1] not in R}
                    vs = version_space(cls, remaining)
                    for i in range(4):
                        assert live(W[i], R) == agrees_at(vs, i), (name, target, chosen, R, i)
                        exact += 1
                for e in sorted(ev):
                    predicted = reopen_per_input(W, e)
                    observed = frozenset(i for i in range(4) if liveness((W[i], W[i]), set()) == LIVE and liveness((W[i], W[i]), {e}) != LIVE)
                    assert predicted == observed
                    reopen_eq += 1
                    bad = mutant_whole_procedure_reopen(W, S, e)
                    assert bad >= predicted
                    mutant_checks += 1
                    if bad > predicted:
                        mutant_over += 1
                        strict_witness += 1
                assert reopen_per_input(W, "e_unrelated") == frozenset() and mutant_whole_procedure_reopen(W, S, "e_unrelated") == frozenset()
                no_alarm += 1
                for Q in ((0, 1), (0, 1, 2, 3), (3,)):
                    assert vsw_family(cls, S, Q) == meet_all(W[q] for q in Q)
                    family_eq += 1
        per_class[name] = {"hypotheses": len(cls), "whole_procedure_overreopens_cases": strict_witness}
    assert mutant_over > 0
    # named witness: AFFINE8, all four examples, revoking e0 keeps x0 live through the other three
    W = vsw(AFFINE8, {i: (AFFINE8[3][i], f"e{i}") for i in range(4)}, range(4))
    assert W[0] == canon([{"e0"}, {"e1", "e2", "e3"}]) and reopen_per_input(W, "e0") == frozenset()
    assert mutant_whole_procedure_reopen(W, {i: (0, f"e{i}") for i in range(4)}, "e0") == frozenset(range(4))
    return {"classes": per_class, "liveness_equals_agreement_checks": exact, "per_input_reopen_checks": reopen_eq, "family_warrant_is_meet_of_per_input": family_eq, "mutant_whole_procedure_checks": mutant_checks, "mutant_whole_procedure_overreopens": mutant_over, "unrelated_evidence_no_alarm": no_alarm, "affine_alternative_witness": 1}


# ---------------------------------------------------------------------------------------------
# B3 · MEG-13 · gap-learning soundness on a finite class (S1–S7, agreement region, VSW, CONTRADICTION)
# ---------------------------------------------------------------------------------------------

WARRANTING = frozenset({"INSTRUCTION", "DEMONSTRATION", "OBSERVATION", "INTERACTION", "EXPERIMENTATION", "EXACT_CHECKER", "IMPORTED"})
GAP_CHANNELS = {
    "TARGET_ABSENT": frozenset({"INSTRUCTION", "DEMONSTRATION", "OBSERVATION"}),
    "WARRANT_GATED": frozenset({"EXPERIMENTATION", "INTERACTION"}),
    "WARRANT_UNKNOWN": frozenset({"EXPERIMENTATION", "INTERACTION"}),
}


class Gov:
    """Minimal governed space: immutable-by-copy atoms, certificates, Γ, meter."""

    def __init__(self, atoms, edges, certs, gammas):
        self.atoms, self.edges, self.certs, self.gammas, self.events, self.revoked = dict(atoms), list(edges), dict(certs), tuple(gammas), 0, frozenset()

    def signature(self, x):
        return tuple(liveness(self.atoms[x], R | self.revoked) for R in self.gammas)

    def evidence(self):
        ev = set()
        for iv in self.atoms.values():
            ev |= evidence_of(iv)
        for e in self.edges:
            ev |= evidence_of(e[5])
        return frozenset(ev)

    def admit(self, atom_id, iv, cert_kind, new_edges):
        if atom_id in self.atoms:
            raise CannotCheck("DUPLICATE_ATOM")
        if cert_kind == "FEEDBACK":
            iv = (ZERO, ZERO)
        elif iv[0] == ZERO:
            raise CannotCheck("WARRANTING_CHANNEL_WITHOUT_WARRANT")
        if not new_edges or not all(atom_id in (*e[1], *e[2]) for e in new_edges):
            raise CannotCheck("ISOLATED_ATOM_REJECTED")
        self.atoms[atom_id] = iv
        self.edges += list(new_edges)
        self.certs[atom_id] = cert_kind
        self.events += 1


def genome(g, previous_sigs, expected_events):
    """KS-S1, S4, S5, S6, S7 (S2 has no COMPOSITION head here; S3 is KS-T02/T04 gating, not re-checked)."""
    s1 = all(g.certs.get(x) in WARRANTING for x, iv in g.atoms.items() if iv[0] != ZERO)
    s4 = all(R <= g.evidence() for R in g.gammas)
    s5 = all(g.signature(x) == sig for x, sig in previous_sigs.items())
    s6 = all(leq(iv[0], iv[1]) and canon(iv[0]) == iv[0] and canon(iv[1]) == iv[1] for iv in g.atoms.values())
    s7 = g.events == expected_events
    return {"S1": s1, "S4": s4, "S5": s5, "S6": s6, "S7": s7}


def navigate(g, seed_atom, target):
    if target not in g.atoms:
        return "GAP_NOT_FOUND", "TARGET_ABSENT"
    lv = liveness(g.atoms[target], g.revoked)
    if lv != LIVE:
        return "GAP_NOT_FOUND", "WARRANT_UNKNOWN" if lv == UNKNOWN else "WARRANT_GATED"
    reach = forward_reach({seed_atom}, [e for e in g.edges if liveness(e[5], g.revoked) == LIVE and all(liveness(g.atoms[t], g.revoked) == LIVE for t in e[1])])
    return ("FOUND", "ACTIVATION") if target in reach else ("GAP_NOT_FOUND", "BUDGET_EXHAUSTED_TARGET_CLOSURE_REACHABLE")


def propose(cls, examples, Q):
    """examples: list of (input_index, value, evidence_id).  Returns (status, payload)."""
    seen = {}
    for i, v, e in examples:
        if i in seen and seen[i][0] != v:
            return "CONTRADICTION", {"conflict": (seen[i][1], e)}
        seen.setdefault(i, (v, e))
    S = {i: (v, e) for i, (v, e) in seen.items()}
    vs = version_space(cls, {i: v for i, (v, _) in S.items()})
    if not vs:
        return "FAIL", {}
    if not all(agrees_at(vs, q) for q in Q):
        return ("GAP_AMBIGUOUS" if len(vs) > 1 else "GAP_INSUFFICIENT"), {"candidates": len(vs)}
    W = vsw(cls, S, Q)
    warrant = meet_all(W[q] for q in Q)
    if warrant == ZERO:
        return "GAP_INSUFFICIENT", {}
    return "PASS", {"table": {q: vs[0][q] for q in Q}, "warrant": warrant, "per_input": W}


def mutant_admit_without_agreement(cls, examples, Q):
    """Planted: admits the first consistent hypothesis although the version space disagrees on Q."""
    S = {i: (v, e) for i, v, e in examples}
    vs = version_space(cls, {i: v for i, (v, _) in S.items()})
    return "PASS", {"table": {q: vs[0][q] for q in Q}, "warrant": canon([frozenset(e for _, e in S.values())])}


def mutant_average_contradiction(cls, examples, Q):
    """Planted: contradictory examples are majority-voted into one hypothesis with warrant ONE."""
    votes = {h: sum(1 for i, v, _ in examples if h[i] == v) for h in cls}
    best = max(cls, key=lambda h: (votes[h], h))
    return "PASS", {"table": {q: best[q] for q in Q}, "warrant": ONE}


def check_b3_meg13_gap_learning_soundness():
    cls, Q = AFFINE8, (0, 1)
    target = (0, 1, 1, 0)   # a ⊕ b, in AFFINE8
    gammas = (frozenset(), frozenset({"d0"}), frozenset({"e0"}), frozenset({"e1"}))
    g = Gov({"q_seed": IONE, "dom": cert({"d0"}), "aux": cert({"a0"})}, [edge("seed_dom", "q_seed", "dom"), edge("seed_aux", "q_seed", "aux")], {"q_seed": "EXACT_CHECKER", "dom": "OBSERVATION", "aux": "OBSERVATION"}, gammas)
    prior = {x: g.signature(x) for x in g.atoms}
    assert navigate(g, "q_seed", "f_xor") == ("GAP_NOT_FOUND", "TARGET_ABSENT")
    assert "DEMONSTRATION" in GAP_CHANNELS["TARGET_ABSENT"] and not any("FEEDBACK" in v for v in GAP_CHANNELS.values())
    # two demonstrations: version space {xor, 1⊕a⊕b?} — check the ambiguity is reported, nothing admitted
    ex2 = [(0, target[0], "e0"), (3, target[3], "e3")]
    status, _ = propose(cls, ex2, Q)
    assert status == "GAP_AMBIGUOUS" and len(g.atoms) == 3
    # the mutant admits anyway: another consistent hypothesis disagrees with the admitted table on Q
    st_bad, bad = mutant_admit_without_agreement(cls, ex2, Q)
    vs2 = version_space(cls, {0: target[0], 3: target[3]})
    assert st_bad == "PASS" and len(vs2) > 1 and any(h[q] != bad["table"][q] for h in vs2 for q in Q)   # mutation applied and unsound
    # four demonstrations: agreement on Q; admitted warrant is the VSW antichain, not the whole-set pin
    ex4 = [(i, target[i], f"e{i}") for i in range(4)]
    status, ok = propose(cls, ex4, Q)
    assert status == "PASS" and ok["table"] == {0: target[0], 1: target[1]}
    assert ok["warrant"] == canon([{"e0", "e1"}, {"e0", "e2", "e3"}, {"e1", "e2", "e3"}])
    g.admit("f_xor", (ok["warrant"], ok["warrant"]), "DEMONSTRATION", [edge("dom_f", "dom", "f_xor", rel="SUPPORT")])
    gen = genome(g, prior, 1)
    assert all(gen.values()), gen
    assert navigate(g, "q_seed", "f_xor") == ("FOUND", "ACTIVATION")
    assert liveness(g.atoms["f_xor"], {"e0"}) == LIVE and liveness(g.atoms["f_xor"], {"e0", "e1"}) == DEAD   # MEG-12 locality
    # contradictory examples: CONTRADICTION, never an average
    exc = ex4 + [(0, 1 - target[0], "e0b")]
    status, payload = propose(cls, exc, Q)
    assert status == "CONTRADICTION" and payload["conflict"] == ("e0", "e0b")
    st_avg, avg = mutant_average_contradiction(cls, exc, Q)
    assert st_avg == "PASS" and avg["warrant"] == ONE   # mutation applied: a warranted object from a conflict
    # WARRANT_UNKNOWN gap (a partial profile whose exhibited warrant was revoked) closed by an
    # EXPERIMENTATION closure: a successor atom with a certified interval and a LINEAGE link (S5 strict)
    g.admit("g_partial", (canon([{"p0"}]), ONE), "DEMONSTRATION", [edge("dom_g", "dom", "g_partial", rel="SUPPORT")])
    g.revoked = frozenset({"p0"})
    prior2 = {x: g.signature(x) for x in g.atoms}
    assert navigate(g, "q_seed", "g_partial") == ("GAP_NOT_FOUND", "WARRANT_UNKNOWN") and "EXPERIMENTATION" in GAP_CHANNELS["WARRANT_UNKNOWN"]
    g.admit("g_closed", cert({"x_closure"}), "EXPERIMENTATION", [edge("dom_gc", "dom", "g_closed", rel="SUPPORT"), edge("lineage_g", "g_partial", "g_closed", rel="LINEAGE")])
    assert all(genome(g, prior2, 3).values()) and navigate(g, "q_seed", "g_closed") == ("FOUND", "ACTIVATION")
    # no-alarm: prior atoms keep their signatures throughout; FEEDBACK admits nothing warranted
    assert all(g.signature(x) == prior[x] for x in prior)
    g.admit("fb", cert({"reward"}), "FEEDBACK", [edge("dom_fb", "dom", "fb", rel="SUPPORT")])
    assert g.atoms["fb"] == (ZERO, ZERO) and all(genome(g, prior2, 4).values())
    return {"class": "AFFINE8", "query_family": list(Q), "target_absent_then_found": 1, "ambiguous_not_admitted": 1, "mutant_admit_without_agreement_caught": 1, "admitted_warrant_is_vsw_antichain": 1, "genome_after_admit": gen, "contradiction_not_averaged": 1, "mutant_average_contradiction_caught": 1, "warrant_unknown_closed_by_experimentation": 1, "prior_signatures_preserved": len(prior), "feedback_admits_zero": 1}


# ---------------------------------------------------------------------------------------------
# B4 · MEG-24 · canonical meaning graph: exact canonical form for |V| ≤ 7, WL-1 collision
# ---------------------------------------------------------------------------------------------

CAN_MAX_VERTICES = 7


def encode(vtypes, hedges, order):
    pos = {old: new for new, old in enumerate(order)}
    return (tuple(vtypes[old] for old in order), tuple(sorted((rel, tuple(pos[v] for v in vs)) for rel, vs in hedges)))


def can(vtypes, hedges):
    """Canonical form: the lexicographically least encoding over every vertex ordering (bounded fragments)."""
    n = len(vtypes)
    if n > CAN_MAX_VERTICES:
        raise CannotCheck(f"canonical form by exhaustive relabelling is bounded at |V| ≤ {CAN_MAX_VERTICES}; got {n}")
    return min(encode(vtypes, hedges, order) for order in itertools.permutations(range(n)))


def isomorphic(g1, g2):
    if len(g1[0]) != len(g2[0]):
        return False
    target = encode(g2[0], g2[1], tuple(range(len(g2[0]))))
    return any(encode(g1[0], g1[1], order) == target for order in itertools.permutations(range(len(g1[0]))))


def wl1(vtypes, hedges, rounds=None):
    """Weisfeiler–Leman-1 colour refinement (hyperedge-aware); the multiset of final colours."""
    n = len(vtypes)
    colour = [("t", t) for t in vtypes]
    for _ in range(rounds or n):
        nxt = []
        for v in range(n):
            ctx = []
            for rel, vs in hedges:
                for k, u in enumerate(vs):
                    if u == v:
                        ctx.append((rel, k, tuple(colour[w] for w in vs)))
            nxt.append((colour[v], tuple(sorted(ctx))))
        colour = nxt
    return tuple(sorted(colour))


def seed_of(key):
    """seed ∘ can: a deterministic distribution over the canonical vertices and relation instances
    (a function of the canonical key only — question atomisation binds typed parts, contract §28)."""
    vt, he = key
    parts = [f"{t}#{i}" for i, t in enumerate(vt)] + [f"{rel}{vs}" for rel, vs in he]
    return tuple((name, Fraction(1, len(parts))) for name in parts)


def eta(g):
    return seed_of(can(*g))


def mutant_eta_wl(g):
    """Planted: WL-1 hash used as the canonical form."""
    return seed_of((tuple(str(c) for c in wl1(*g)), ()))   # the hash is all the mutant keeps


def relabel(g, rng):
    order = list(range(len(g[0])))
    rng.shuffle(order)
    pos = {old: new for new, old in enumerate(order)}
    vt = [None] * len(order)
    for old, new in pos.items():
        vt[new] = g[0][old]
    he = [(rel, tuple(pos[v] for v in vs)) for rel, vs in g[1]]
    rng.shuffle(he)
    return (tuple(vt), tuple(he))


def check_b4_meg24_canonical_meaning_graph():
    # two parsers, different code paths (vertex numbering, edge order) → same can → same seed (KS-T10a)
    parser_a = (("event", "entity", "entity"), (("ROLE:agent", (0, 1)), ("ROLE:patient", (0, 2)), ("TENSE:past", (0,))))
    parser_b = (("entity", "entity", "event"), (("TENSE:past", (2,)), ("ROLE:patient", (2, 0)), ("ROLE:agent", (2, 1))))
    assert can(*parser_a) == can(*parser_b) and eta(parser_a) == eta(parser_b)
    # exhaustive: every directed graph on 3 vertices (one type): can equal ⇔ isomorphic (64² pairs)
    pairs = [(a, b) for a in range(3) for b in range(3) if a != b]
    graphs = [(("e", "e", "e"), tuple(("r", pr) for i, pr in enumerate(pairs) if mask & (1 << i))) for mask in range(1 << len(pairs))]
    cans = [can(*g) for g in graphs]
    completeness = 0
    for i, g1 in enumerate(graphs):
        for j, g2 in enumerate(graphs):
            assert (cans[i] == cans[j]) == isomorphic(g1, g2)
            completeness += 1
    # isomorphism invariance on random 5-vertex typed hyper-fragments (no-alarm)
    rng = random.Random(7)
    invariance = 0
    for _ in range(40):
        vt = tuple(rng.choice(("entity", "event", "property")) for _ in range(5))
        he = tuple((rng.choice(("ROLE:agent", "MODIFIES", "COREF")), tuple(rng.sample(range(5), rng.choice((1, 2, 3))))) for _ in range(rng.randint(1, 5)))
        g = (vt, he)
        g2 = relabel(g, rng)
        assert can(*g) == can(*g2) and eta(g) == eta(g2) and wl1(*g) == wl1(*g2)
        invariance += 1
    # WL-1 collision: directed 6-cycle vs two directed 3-cycles ("A loves B, B loves C, C loves A" twice)
    c6 = (("entity",) * 6, tuple(("loves", (i, (i + 1) % 6)) for i in range(6)))
    c3c3 = (("entity",) * 6, tuple(("loves", (i, (i + 1) % 3)) for i in range(3)) + tuple(("loves", (3 + i, 3 + (i + 1) % 3)) for i in range(3)))
    assert not isomorphic(c6, c3c3) and can(*c6) != can(*c3c3) and eta(c6) != eta(c3c3)
    assert wl1(*c6) == wl1(*c3c3)                       # mutation applied: the hash collides
    assert mutant_eta_wl(c6) == mutant_eta_wl(c3c3)     # the mutant seeds two non-isomorphic meanings identically
    # bounded: the exact algorithm refuses beyond its bound with CANNOT_CHECK, never a silent answer
    refused = 0
    try:
        can(("e",) * (CAN_MAX_VERTICES + 1), ())
    except CannotCheck:
        refused = 1
    assert refused == 1
    return {"two_parsers_same_seed": 1, "exhaustive_3_vertex_graphs": len(graphs), "can_equal_iff_isomorphic_pairs": completeness, "random_relabel_invariance": invariance, "wl1_collision_c6_vs_2c3": 1, "mutant_wl_hash_as_canonical_caught": 1, "beyond_bound_cannot_check": refused}


# ---------------------------------------------------------------------------------------------
# B5 · MEG-03 · scope / epoch / supersession
# ---------------------------------------------------------------------------------------------


def revoked_at(epochs, t):
    """R_t = evidence whose validity epoch ends at or before t."""
    return frozenset(e for e, (_, d) in epochs.items() if d <= t)


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def gamma_time_measurable(epochs, blocks, times):
    return all(all(len({e in revoked_at(epochs, t) for e in B}) == 1 for B in blocks) for t in times)


def epoch_intersect(a, b):
    return (max(a[0], b[0]), min(a[1], b[1]))


def epoch_empty(a):
    return a[0] >= a[1]


def supersede(atoms, edges, epochs, old_id, old_evidence, new_id, new_evidence, t):
    """supersede(x, x') := admit x' (evidence valid from t) + end the conversation-scoped evidence of x at t
    + SUPERSEDED_BY link (non-dependency)."""
    epochs = dict(epochs)
    epochs[old_evidence] = (epochs[old_evidence][0], t)
    epochs[new_evidence] = (t, INF)
    atoms = dict(atoms)
    atoms[new_id] = cert({new_evidence})
    edges = list(edges) + [edge(f"sup:{old_id}", old_id, new_id, rel="SUPERSEDED_BY")]
    return atoms, edges, epochs


def mutant_stale_plan(atoms, epochs, x, t):
    """Planted: evaluates liveness at time t without Γ_time (ignores the epoch end)."""
    return liveness(atoms[x], set())


def check_b5_meg03_scope_epoch_supersession():
    # (i) Γ_time lies in σ(blocks) iff end-epochs are block-constant — exhaustive on |E| = 4
    E = ["e0", "e1", "e2", "e3"]
    times = (1, 2, 3)
    measurability_checks = 0
    for blocks in set_partitions(E):
        for ends in itertools.product(times, repeat=4):
            epochs = {e: (0, d) for e, d in zip(E, ends)}
            lhs = gamma_time_measurable(epochs, blocks, times)
            rhs = all(len({epochs[e][1] for e in B}) == 1 for B in blocks)
            assert lhs == rhs
            measurability_checks += 1
    # (iii) epoch ∩ is associative, commutative, has identity [0, ∞) and every empty epoch annihilates
    grid = [0, 1, 2, 3, INF]
    intervals = [(a, b) for a in grid for b in grid]
    algebra = 0
    for a in intervals:
        assert epoch_intersect(a, (0, INF)) == a if not epoch_empty(a) else epoch_empty(epoch_intersect(a, (0, INF)))
        for b in intervals:
            assert epoch_intersect(a, b) == epoch_intersect(b, a)
            if epoch_empty(a):
                assert epoch_empty(epoch_intersect(a, b))
            for c in intervals:
                assert epoch_intersect(epoch_intersect(a, b), c) == epoch_intersect(a, epoch_intersect(b, c))
                algebra += 1
    # (ii) "Tuesday" → "Wednesday" fixture
    atoms = {"day_tue": cert({"e1"}), "venue": cert({"e2"}), "plan": cert({"e1", "e2"}), "unrelated": cert({"e5"}), "note": cert({"e5"})}
    edges = [edge("tue_plan", "day_tue", "plan", rel="COMPOSITION"), edge("venue_plan", "venue", "plan", rel="COMPOSITION"), edge("unrel_note", "unrelated", "note", rel="DEPENDENCE")]
    epochs = {"e1": (1, INF), "e2": (1, INF), "e5": (0, INF)}
    assert liveness(atoms["plan"], revoked_at(epochs, 2)) == LIVE
    atoms2, edges2, epochs2 = supersede(atoms, edges, epochs, "day_tue", "e1", "day_wed", "e3", 3)
    r_before, r_after = revoked_at(epochs2, 2), revoked_at(epochs2, 3)
    assert r_before == frozenset() and r_after == frozenset({"e1"})
    rep = reopening_report(atoms2, edges2, r_before, r_after)
    assert rep["reopen"] == frozenset({"day_tue", "plan"}) and rep["recheck"] == frozenset() and rep["unaffected"] == frozenset({"venue", "unrelated", "note", "day_wed"})
    assert liveness(atoms2["day_wed"], r_after) == LIVE and liveness(atoms2["day_tue"], r_after) == DEAD and liveness(atoms2["plan"], r_after) == DEAD
    # supersession reopening = KS-T22 on the superseded evidence alone
    assert rep == reopening_report(atoms2, edges2, frozenset(), frozenset({"e1"}))
    # planted stale-plan mutant: the plan for Tuesday stays LIVE on Wednesday
    bad = mutant_stale_plan(atoms2, epochs2, "plan", 3)
    assert bad == LIVE and bad != liveness(atoms2["plan"], r_after)
    # no-alarm: nothing reopens before the supersession time; the unrelated entity is untouched
    early = reopening_report(atoms2, edges2, revoked_at(epochs2, 1), revoked_at(epochs2, 2))
    assert early["reopen"] == frozenset() and early["recheck"] == frozenset()
    assert liveness(atoms2["unrelated"], r_after) == LIVE and liveness(atoms2["note"], r_after) == LIVE
    # a second supersession chains: "Wednesday" → "Thursday" reopens only day_wed (no dependents yet)
    atoms3, edges3, epochs3 = supersede(atoms2, edges2, epochs2, "day_wed", "e3", "day_thu", "e4", 5)
    rep3 = reopening_report(atoms3, edges3, revoked_at(epochs3, 4), revoked_at(epochs3, 5))
    assert rep3["reopen"] == frozenset({"day_wed"}) and "plan" in rep3["unaffected"]
    return {"measurability_checks": measurability_checks, "epoch_algebra_checks": algebra, "tuesday_wednesday_reopen": sorted(rep["reopen"]), "tuesday_wednesday_unaffected": sorted(rep["unaffected"]), "supersession_equals_ks_t22": 1, "mutant_stale_plan_caught": 1, "no_alarm_before_supersession": 1, "chained_supersession_local": 1}


# ---------------------------------------------------------------------------------------------
# B6 · MEG-17 · repair after REOPEN: reinstate exact, relearn under a new id with LINEAGE, work bound
# ---------------------------------------------------------------------------------------------


def random_space(rng, n=7):
    """Seeded typed hypergraph: chain 0→…→n−1 plus random forward edges; certified warrants over
    evidence {0,1,2,3}; the target (last atom) cites e* = 0 in every warrant so revoking {0} kills it."""
    ids = [f"v{i}" for i in range(n)]
    atoms = {}
    for i, x in enumerate(ids):
        ws = [frozenset(rng.sample([1, 2, 3], rng.randint(1, 2))) for _ in range(rng.randint(1, 2))]
        atoms[x] = cert(*ws)
    atoms[ids[-1]] = cert({0, rng.choice([1, 2, 3])}, {0, rng.choice([1, 2, 3])})
    edges = [edge(f"c{i}", ids[i], ids[i + 1], rel=rng.choice(["DEPENDENCE", "COMPOSITION"])) for i in range(n - 1)]
    for _ in range(rng.randint(1, 3)):
        i, j = sorted(rng.sample(range(n), 2))
        edges.append(edge(f"x{i}{j}", ids[i], ids[j], rel="SUPPORT"))
    return ids, atoms, edges


def relearn(atoms, edges, x, new_id, new_evidence, table):
    """Admit new support under a new evidence id with a LINEAGE link; content (behaviour) copied."""
    atoms = dict(atoms)
    atoms[new_id] = cert({new_evidence})
    edges = list(edges) + [edge(f"lineage:{x}", x, new_id, rel="LINEAGE")]
    return atoms, edges, {x: table, new_id: table}


def local_repair(atoms, edges, report):
    """Repair touches exactly the atoms whose liveness changed (B/F changed-derivability set)."""
    return frozenset(report["reopen"]), len(report["reopen"])


def mutant_global_rederivation_counted_local(atoms, edges, report):
    """Planted: re-derives every atom in the space but reports the work as |REOPEN|."""
    return frozenset(atoms), len(report["reopen"])


def check_b6_meg17_repair_after_reopen():
    rng = random.Random(17)
    spaces = 30
    counts = {"works_before": 0, "fails_after": 0, "unrelated_liveness_intact": 0, "activation_outside_reach_intact": 0, "reinstate_exact": 0, "relearn_live_new_id": 0, "behaviour_equal_lifecycle_differs": 0, "work_exact_leq_cone": 0, "mutant_global_touches_more": 0}
    for _ in range(spaces):
        ids, atoms, edges = random_space(rng)
        seed, target = ids[0], ids[-1]
        R0, R1 = frozenset(), frozenset({0})
        a0 = activation(atoms, edges, R0, seed)
        assert liveness(atoms[target], R0) == LIVE and a0[target] > 0
        counts["works_before"] += 1
        a1 = activation(atoms, edges, R1, seed)
        rep = reopening_report(atoms, edges, R0, R1)
        assert liveness(atoms[target], R1) == DEAD and target in rep["reopen"] and a1[target] == 0
        counts["fails_after"] += 1
        for x in rep["unaffected"]:
            assert liveness(atoms[x], R0) == liveness(atoms[x], R1)
        counts["unrelated_liveness_intact"] += 1
        dead = {x for x in atoms if liveness(atoms[x], R1) != LIVE}
        reach = forward_reach(dead, edges)
        for x in atoms:
            if x not in reach:
                assert a0[x] == a1[x]
        counts["activation_outside_reach_intact"] += 1
        # reinstate restores exactly (KS-T04b (iv)): intervals are immutable, only R moves back
        back = activation(atoms, edges, R0, seed)
        assert back == a0 and all(liveness(atoms[x], R0) == liveness(atoms[x], frozenset()) for x in atoms)
        counts["reinstate_exact"] += 1
        # relearn: new support under a new evidence id, LINEAGE link, behaviour identical
        table = {q: (q[0] ^ q[1]) for q in INPUTS}
        atoms2, edges2, behaviour = relearn(atoms, edges, target, target + "'", "e_new", table)
        gammas = (frozenset(), R1, frozenset({"e_new"}))
        assert liveness(atoms2[target + "'"], R1) == LIVE and liveness(atoms2[target], R1) == DEAD
        counts["relearn_live_new_id"] += 1
        sig_old = tuple(liveness(atoms2[target], R) for R in gammas)
        sig_new = tuple(liveness(atoms2[target + "'"], R) for R in gammas)
        assert behaviour[target] == behaviour[target + "'"] and sig_old != sig_new     # WLL-1 strictness
        counts["behaviour_equal_lifecycle_differs"] += 1
        touched, work = local_repair(atoms, edges, rep)
        assert touched == rep["reopen"] and work == len(rep["reopen"]) <= len(rep["cone"])
        counts["work_exact_leq_cone"] += 1
        bad_touched, bad_work = mutant_global_rederivation_counted_local(atoms, edges, rep)
        assert bad_touched == frozenset(atoms) and bad_work == work            # mutation applied: same reported work
        if len(bad_touched) > len(rep["cone"]):
            counts["mutant_global_touches_more"] += 1
    assert counts["mutant_global_touches_more"] > 0
    return {"random_spaces": spaces, **counts}


# ---------------------------------------------------------------------------------------------
# B7 · MEG-19 · consolidation locality: liveness through exports, content through provenance χ
# ---------------------------------------------------------------------------------------------


def summary_interval(corr, exported_ivs):
    out = corr
    for iv in exported_ivs:
        out = imeet(out, iv)
    return out


def content_recheck(report, X, chi, exceptions):
    """Parts of m to recheck: χ⁻¹(REOPEN ∩ X) plus any registered exception whose liveness changed."""
    hit = report["reopen"] & frozenset(X)
    parts = frozenset(p for p, x in chi.items() if x in hit)
    return parts | frozenset(f"exception:{ex}" for ex in exceptions if ex in report["changed"])


def mutant_recheck_only_on_liveness_change(report, X, chi, m_before, m_after):
    """Planted: rechecks content only when λ(m) changed — misses stale parts from non-exported constituents."""
    return frozenset(chi) if m_before != m_after else frozenset()


def mutant_summary_majority(constituent_ivs):
    out = (ZERO, ZERO)
    for iv in constituent_ivs:
        out = ijoin(out, iv)
    return out


def semantic_equal(m_table, g_table, scope, certificate):
    if certificate != ("EXPERIMENTATION_CLOSURE", tuple(scope)):
        return "CANNOT_CHECK"
    return "EQUAL" if all(m_table[q] == g_table[q] for q in scope) else "NOT_EQUAL"


def mutant_equal_by_liveness(m_live, g_live):
    return "EQUAL" if m_live == g_live == LIVE else "CANNOT_CHECK"


def check_b7_meg19_consolidation_locality():
    # (i) exhaustive at |E| = 2 over the correspondence and two exported constituents
    ivs = all_intervals(2)
    revs = subsets(range(2))
    only_if = transfer = converse_fails = 0
    for c in ivs:
        for x in ivs:
            for y in ivs:
                for R0 in revs:
                    for R1 in revs:
                        m0, m1 = liveness(summary_interval(c, [x, y]), R0), liveness(summary_interval(c, [x, y]), R1)
                        changed = [liveness(z, R0) != liveness(z, R1) for z in (c, x, y)]
                        if m0 != m1:
                            assert any(changed)
                            only_if += 1
                        if changed[1] and liveness(c, R0) == liveness(c, R1) == LIVE and liveness(y, R0) == liveness(y, R1) == LIVE:
                            assert m0 != m1
                            transfer += 1
                        if changed[1] and m0 == m1:
                            converse_fails += 1
    assert converse_fails > 0
    # (ii) fixture: macro m over X = {x1..x4}, exported {x1, x4}, provenance χ: parts p_i ← x_i, exception ex1
    atoms = {"x1": cert({"a"}), "x2": cert({"d"}), "x3": cert({"a", "c"}), "x4": cert({"a", "c"}, {"f"}), "ex1": cert({"g"}), "other": cert({"z"})}
    edges = [edge("x1x3", "x1", "x3", rel="COMPOSITION"), edge("x3x4", "x3", "x4", rel="COMPOSITION"), edge("x2x4", "x2", "x4", rel="DEPENDENCE")]
    X, Xe, chi = ("x1", "x2", "x3", "x4"), ("x1", "x4"), {"p1": "x1", "p2": "x2", "p3": "x3", "p4": "x4"}
    corr = cert({"k"})
    atoms["m"] = summary_interval(corr, [atoms[x] for x in Xe])
    edges += [edge("sum", X, "m", rel="COMPOSITION"), edge("exc", "ex1", "m", rel="LINEAGE")]   # dependency-typed (see limitation)
    cases = {}
    for name, R1 in {"deep_non_exported": {"d"}, "middle": {"c"}, "exported_dies": {"a"}, "alternative_only": {"f"}, "exception": {"g"}, "unrelated": {"z"}}.items():
        R1 = frozenset(R1)
        rep = reopening_report(atoms, edges, frozenset(), R1)
        m0, m1 = liveness(atoms["m"], frozenset()), liveness(atoms["m"], R1)
        exact = content_recheck(rep, X, chi, ("ex1",))
        assert len(exact) == len(frozenset(p for p, x in chi.items() if x in (rep["reopen"] & frozenset(X)))) + (1 if "ex1" in rep["changed"] else 0)
        cases[name] = {"lambda_m": [m0, m1], "reopen": sorted(rep["reopen"]), "recheck": sorted(rep["recheck"]), "content_recheck": sorted(exact)}
    assert cases["deep_non_exported"]["lambda_m"] == [LIVE, LIVE] and cases["deep_non_exported"]["content_recheck"] == ["p2"]
    assert cases["middle"]["lambda_m"] == [LIVE, LIVE] and cases["middle"]["content_recheck"] == ["p3"] and cases["middle"]["recheck"] == ["m", "x4"]
    assert cases["exported_dies"]["lambda_m"] == [LIVE, DEAD] and "p1" in cases["exported_dies"]["content_recheck"]
    assert cases["alternative_only"]["content_recheck"] == [] and cases["alternative_only"]["reopen"] == []
    assert cases["exception"]["content_recheck"] == ["exception:ex1"] and cases["exception"]["lambda_m"] == [LIVE, LIVE]
    assert cases["unrelated"]["content_recheck"] == [] and cases["unrelated"]["reopen"] == ["other"] and cases["unrelated"]["lambda_m"] == [LIVE, LIVE]   # no-alarm: m untouched
    # planted: recheck only when λ(m) changed — misses the stale part p2 (mutation applied: empty set)
    rep_d = reopening_report(atoms, edges, frozenset(), frozenset({"d"}))
    bad = mutant_recheck_only_on_liveness_change(rep_d, X, chi, LIVE, LIVE)
    assert bad == frozenset() and content_recheck(rep_d, X, chi, ("ex1",)) == frozenset({"p2"})
    # KS-T23 mutant stays caught: x1 DEAD, x4 LIVE → majority says LIVE, the exact summary is DEAD
    Ra = frozenset({"a"})
    assert liveness(mutant_summary_majority([atoms[x] for x in X]), Ra) == LIVE and liveness(atoms["m"], Ra) == DEAD
    # (iii) semantic equality only under an EXPERIMENTATION closure certificate on the registered scope
    scope = INPUTS
    g_table = {q: q[0] & q[1] for q in scope}
    m_table = dict(g_table)
    m_bad = dict(g_table)
    m_bad[(1, 1)] = 0
    assert semantic_equal(m_table, g_table, scope, None) == "CANNOT_CHECK"
    assert semantic_equal(m_table, g_table, scope, ("EXPERIMENTATION_CLOSURE", scope)) == "EQUAL"
    assert semantic_equal(m_bad, g_table, scope, ("EXPERIMENTATION_CLOSURE", scope)) == "NOT_EQUAL"
    assert mutant_equal_by_liveness(LIVE, LIVE) == "EQUAL" and semantic_equal(m_bad, g_table, scope, ("EXPERIMENTATION_CLOSURE", scope)) != "EQUAL"
    return {"intervals_at_n2": len(ivs), "liveness_change_only_through_exports": only_if, "change_transfers_when_others_live": transfer, "unqualified_converse_fails": converse_fails, "fixture_cases": cases, "mutant_recheck_only_on_liveness_caught": 1, "mutant_summary_majority_caught": 1, "semantic_equality_cannot_check_without_closure": 1, "mutant_equal_by_liveness_caught": 1, "deconsolidation": "PARENT_SUFFICIENT_EXPECTED"}


# ---------------------------------------------------------------------------------------------
# B8 · MEG-28 · Jump preservation as a DPO rewrite on the M4 Boolean fixture
# ---------------------------------------------------------------------------------------------

STRONG_TRIGGERS = frozenset({"EXPRESSIVE_CEILING", "STRUCTURAL_NONIDENTIFIABILITY", "MODEL_FAMILY_INADEQUACY", "GLOBAL_OBSTRUCTION"})


def xor_span(features):
    """All Boolean functions reachable as XOR-combinations of the feature truth tables."""
    out = set()
    for coeffs in itertools.product((0, 1), repeat=len(features)):
        out.add(tuple(sum(c * f[i] for c, f in zip(coeffs, features)) % 2 for i in range(4)))
    return frozenset(out)


def digest(space):
    atoms, edges = space
    return (tuple(sorted((x, t, iv) for x, (t, iv) in atoms.items())), tuple(sorted(edges)))


def dpo_apply(space, rule, trigger, assessment, commit_receipt):
    """DPO rewrite L ← I → R with identity match; refuses with a typed reason.  Atoms: id → (type, iv);
    edges: (eid, tails, heads, rel).  I is given as (atom ids, edge ids) shared by L and R."""
    atoms, edges = space
    L, I, R = rule
    if trigger["kind"] not in STRONG_TRIGGERS or trigger["incumbent_level"] >= trigger["proposal_level"]:
        return "REFUSED_TRIGGER_NOT_ADMISSIBLE", space
    if assessment != "CANDIDATE_FOR_PROTECTED_EVALUATION":
        return "REFUSED_NOT_CANDIDATE", space
    if commit_receipt is None or commit_receipt.get("commit", 0) < 1 or commit_receipt.get("source") != "external":
        return "REFUSED_NO_EXTERNAL_COMMIT", space
    for x, attr in L[0].items():
        if atoms.get(x) != attr:
            return "REFUSED_NO_MATCH", space
    for x in I[0]:
        if L[0][x] != R[0][x]:
            return "REFUSED_INTERFACE_ATTRIBUTE_CHANGED", space
    l_edge_ids = {e[0] for e in L[1]}
    deleted_atoms = set(L[0]) - set(I[0])
    for e in edges:
        if (set(e[1]) | set(e[2])) & deleted_atoms and e[0] not in l_edge_ids:
            return "REFUSED_DANGLING", space
    if not set(L[1]) <= set(edges):
        return "REFUSED_NO_MATCH", space
    deleted_edges = {e for e in L[1] if e[0] not in I[1]}
    new_atoms = {x: attr for x, attr in atoms.items() if x not in deleted_atoms}
    new_atoms.update({x: attr for x, attr in R[0].items() if x not in I[0]})
    new_edges = [e for e in edges if e not in deleted_edges] + [e for e in R[1] if e[0] not in I[1]]
    return "APPLIED", (new_atoms, new_edges)


def jump_reopening(before, after, rule):
    """C_J = deleted atoms ∪ heads of deleted edges ∪ heads of added edges ∪ added atoms; Impact_D over both structures."""
    L, I, R = rule
    deleted_atoms = set(L[0]) - set(I[0])
    added_atoms = set(R[0]) - set(I[0])
    heads = set()
    for e in L[1]:
        if e[0] not in I[1]:
            heads |= set(e[2])
    for e in R[1]:
        if e[0] not in I[1]:
            heads |= set(e[2])
    C = deleted_atoms | added_atoms | heads
    union_edges = [edge(e[0], e[1], e[2], rel=e[3]) for e in {*before[1], *after[1]}]
    return frozenset(C), impact_cone(C, union_edges)


def mutant_one_hop_reopening(before, after, rule):
    C, _ = jump_reopening(before, after, rule)
    out = set(C)
    for e in {*before[1], *after[1]}:
        if e[3] in DEPENDENCY and any(t in C for t in e[1]):
            out |= set(e[2])
    return frozenset(out)


def m4_fixture():
    F1, FA, FB, FAB = (1, 1, 1, 1), (0, 0, 1, 1), (0, 1, 0, 1), (0, 0, 0, 1)
    feats = {"feat_1": ("representation", cert({"r1"})), "feat_a": ("representation", cert({"r2"})), "feat_b": ("representation", cert({"r3"}))}
    atoms = dict(feats)
    atoms["phi_affine"] = ("representation", cert({"r1", "r2", "r3"}))
    edges = [(f"{f}->phi", (f,), ("phi_affine",), "COMPOSITION") for f in feats]
    for table in xor_span([F1, FA, FB]):
        atoms["h_" + "".join(map(str, table))] = ("procedure", cert({"r1", "r2", "r3"}))
        edges.append((f"feats->h_{''.join(map(str, table))}", ("feat_1", "feat_a", "feat_b"), ("h_" + "".join(map(str, table)),), "COMPOSITION"))
    atoms.update({"goal_AND": ("goal", cert({"g"})), "witness_parity": ("counterexample", cert({"w"})), "renderer": ("procedure", cert({"v"})), "report": ("summary", cert({"v"})), "archive": ("summary", cert({"v"})), "unrelated": ("claim", cert({"u"})), "note": ("claim", cert({"u"}))})
    edges += [("phi->renderer", ("phi_affine",), ("renderer",), "DEPENDENCE"), ("renderer->report", ("renderer",), ("report",), "DEPENDENCE"), ("report->archive", ("report",), ("archive",), "DEPENDENCE"), ("goal-witness", ("goal_AND",), ("witness_parity",), "CONSTRAINT"), ("unrelated->note", ("unrelated",), ("note",), "DEPENDENCE")]
    L_atoms = {**feats, "phi_affine": atoms["phi_affine"], "renderer": atoms["renderer"]}
    L_edges = [e for e in edges if e[0] in {"feat_1->phi", "feat_a->phi", "feat_b->phi", "phi->renderer"}]
    I = (("feat_1", "feat_a", "feat_b", "renderer"), ())
    R_atoms = {**feats, "renderer": atoms["renderer"], "feat_ab": ("representation", cert({"r4"})), "phi_quad": ("representation", cert({"r1", "r2", "r3", "r4"})), "h_0001": ("procedure", cert({"r4"}))}
    R_edges = [(f"{f}->phi_quad", (f,), ("phi_quad",), "COMPOSITION") for f in ("feat_1", "feat_a", "feat_b", "feat_ab")] + [("feat_ab->h_0001", ("feat_ab",), ("h_0001",), "COMPOSITION"), ("phi_quad->renderer", ("phi_quad",), ("renderer",), "DEPENDENCE")]
    return (atoms, edges), ((L_atoms, L_edges), I, (R_atoms, R_edges)), (F1, FA, FB, FAB)


def check_b8_meg28_dpo_jump_preservation():
    space, rule, (F1, FA, FB, FAB) = m4_fixture()
    L, I, R = rule
    # the ceiling is exact: AND ∉ XOR-span{1,a,b} (parity), AND ∈ span{1,a,b,ab}, old eight embed with c3 = 0
    affine, quad = xor_span([F1, FA, FB]), xor_span([F1, FA, FB, FAB])
    assert len(affine) == 8 and FAB not in affine and all(sum(t) % 2 == 0 for t in affine) and len(quad) == 16 and FAB in quad and affine <= quad
    trigger = {"kind": "EXPRESSIVE_CEILING", "incumbent_level": 1, "proposal_level": 3}
    commit = {"commit": 1, "source": "external"}
    gammas = (frozenset(), frozenset({"r1"}), frozenset({"v"}), frozenset({"g"}), frozenset({"r4"}))
    # (iii) adoption only through CANDIDATE_FOR_PROTECTED_EVALUATION and an external Commit
    assert dpo_apply(space, rule, trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", None)[0] == "REFUSED_NO_EXTERNAL_COMMIT"
    assert dpo_apply(space, rule, trigger, "JUMP_PROPOSAL_INCOMPLETE", commit)[0] == "REFUSED_NOT_CANDIDATE"
    assert dpo_apply(space, rule, {**trigger, "kind": "POOR_SCORE"}, "CANDIDATE_FOR_PROTECTED_EVALUATION", commit)[0] == "REFUSED_TRIGGER_NOT_ADMISSIBLE"
    self_adopt = {"commit": 1, "source": "internal"}   # mutant: the machine signs its own commit
    assert dpo_apply(space, rule, trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", self_adopt)[0] == "REFUSED_NO_EXTERNAL_COMMIT"
    status, after = dpo_apply(space, rule, trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", commit)
    assert status == "APPLIED" and "phi_affine" not in after[0] and "phi_quad" in after[0] and "h_0001" in after[0]
    # (i) every atom in I and every atom outside m(L) keeps interval and liveness signature over Γ
    preserved = 0
    for x, (t, iv) in space[0].items():
        if x in I[0] or x not in L[0]:
            assert after[0][x] == (t, iv) and tuple(liveness(iv, g) for g in gammas) == tuple(liveness(after[0][x][1], g) for g in gammas)
            preserved += 1
    old_repertoire = {x: attr for x, attr in space[0].items() if x.startswith("h_")}
    assert all(after[0][x] == attr for x, attr in old_repertoire.items()) and len(old_repertoire) == 8   # no-alarm: old affine repertoire byte-identical
    # (ii) the reopening set is Impact_D of the rewritten region; everything outside keeps its incidences
    C, cone = jump_reopening(space, after, rule)
    assert C == frozenset({"phi_affine", "phi_quad", "h_0001", "feat_ab", "renderer"}) and cone == C | {"report", "archive"}
    for x in after[0]:
        if x not in cone and x not in L[0]:   # interface atoms keep attributes, not incidences (they are the gluing boundary)
            inc_before = {e for e in space[1] if x in e[1] or x in e[2]}
            inc_after = {e for e in after[1] if x in e[1] or x in e[2]}
            assert inc_before == inc_after and space[0][x] == after[0][x]
    one_hop = mutant_one_hop_reopening(space, after, rule)
    assert "archive" not in one_hop and "archive" in cone     # mutation applied and caught
    # (iv) rollback exact: the inverse rule R ← I → L restores 𝒦 byte-identically
    status_back, restored = dpo_apply(after, (R, I, L), trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", commit)
    assert status_back == "APPLIED" and digest(restored) == digest(space)
    # planted: an interface object whose interval changes must be refused
    R_bad = (dict(R[0]), R[1])
    R_bad[0]["feat_a"] = ("representation", cert({"r2", "r4"}))
    assert R_bad[0]["feat_a"] != L[0]["feat_a"]   # mutation applied
    assert dpo_apply(space, (L, I, R_bad), trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", commit)[0] == "REFUSED_INTERFACE_ATTRIBUTE_CHANGED"
    # dangling: deleting phi_affine without naming its external edge is refused (quarantine, not deletion)
    L_dangling = (L[0], [e for e in L[1] if e[0] != "phi->renderer"])
    assert dpo_apply(space, (L_dangling, I, R), trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", commit)[0] == "REFUSED_DANGLING"
    return {"affine_span": len(affine), "quadratic_span": len(quad), "and_outside_affine_inside_quadratic": 1, "adoption_refusals": 4, "applied": 1, "atoms_preserved_interval_and_signature": preserved, "old_repertoire_byte_identical": len(old_repertoire), "reopening_set": sorted(cone), "mutant_one_hop_caught": 1, "rollback_exact": 1, "mutant_interface_attribute_change_refused": 1, "dangling_refused": 1, "improvement_half": "OPEN"}


# ---------------------------------------------------------------------------------------------


def run_all():
    return {
        "B1_MEG-05": check_b1_meg05_discourse_state(),
        "B2_MEG-12": check_b2_meg12_per_input_vsw(),
        "B3_MEG-13": check_b3_meg13_gap_learning_soundness(),
        "B4_MEG-24": check_b4_meg24_canonical_meaning_graph(),
        "B5_MEG-03": check_b5_meg03_scope_epoch_supersession(),
        "B6_MEG-17": check_b6_meg17_repair_after_reopen(),
        "B7_MEG-19": check_b7_meg19_consolidation_locality(),
        "B8_MEG-28": check_b8_meg28_dpo_jump_preservation(),
        "NOVELTY": "NOT_ESTABLISHED",
    }


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
