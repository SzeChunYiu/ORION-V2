"""Exact finite checker for KSO_SELF_MODEL_PREREQUISITE_THEOREMS_BATCH5_V1.md (stdlib only, exact).

One check function per theorem (E1–E8, plus the three residual halves R1–R3: MEG-19 deconsolidation,
MEG-27 open inventory, MEG-02 graded semiring).  Every check performs (a) the positive statement,
(b) at least one planted mutant whose mutation is asserted applied and which must be caught, and
(c) a no-alarm control.  The minimal objects of the OCM core are re-implemented here (antichain
semiring, warrant intervals, Kleene liveness, authority meet, frozen-denominator navigation with
exact rational fixed points, impact cone, the batch-1 T4 stamping / rollback, the batch-2 B7
consolidation fixture and B8 DPO rewrite on the M4 Boolean fixture, the batch-1 T8 metered
system); nothing is imported from ``ocm``.

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
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21) — as in batches 1–4
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


def kand(a, b):
    return DEAD if DEAD in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else LIVE)


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
IUNKNOWN = (ZERO, ONE)


def evidence_of(iv):
    return frozenset(e for side in iv for w in side for e in w)


def subsets(universe):
    u = sorted(universe, key=repr)
    return [frozenset(c) for k in range(len(u) + 1) for c in itertools.combinations(u, k)]


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=repr).encode()).hexdigest()


def auth_meet(*items):
    keys = set().union(*(set(a) for a in items))
    return {k: min(a.get(k, 0) for a in items) for k in keys}


def edge(eid, tails, heads, w=1, hw=None, iv=IONE, rel="DEPENDENCE"):
    tails = (tails,) if isinstance(tails, str) else tuple(tails)
    heads = (heads,) if isinstance(heads, str) else tuple(heads)
    return (eid, tails, heads, Fraction(w), tuple(Fraction(x) for x in (hw or [1] * len(heads))), iv, rel)


# ---------------------------------------------------------------------------------------------
# navigation: frozen denominators, gated matrix, exact restart fixed point (KS-T03/T04b/T05); cone
# ---------------------------------------------------------------------------------------------


def nav_matrix(atoms, edges, revoked):
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


ALPHA_NAV = Fraction(1, 3)


def activation(atoms, edges, revoked, seed_atom, alpha=ALPHA_NAV):
    ids, p = nav_matrix(atoms, edges, revoked)
    seed = [Fraction(int(x == seed_atom)) if liveness(atoms[x], revoked) == LIVE else Fraction(0) for x in ids]
    return dict(zip(ids, fixed_point(p, seed, alpha)))


def impact_cone(changed, edges):
    out = set(changed)
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


def random_space(rng, n_atoms, n_edges, n_ev, prefix="v", ev_prefix=""):
    atoms = {}
    for i in range(n_atoms):
        w1 = frozenset(f"{ev_prefix}{e}" for e in rng.sample(range(n_ev), rng.randint(1, 2)))
        atoms[f"{prefix}{i}"] = cert(w1) if rng.random() < 0.7 else cert(w1, frozenset(f"{ev_prefix}{e}" for e in rng.sample(range(n_ev), 1)))
    edges = []
    names = list(atoms)
    for j in range(n_edges):
        t = rng.choice(names)
        h = rng.choice([x for x in names if x != t])
        edges.append(edge(f"{prefix}e{j}", t, h, w=rng.randint(1, 3)))
    return atoms, edges


# ---------------------------------------------------------------------------------------------
# E1 · MEG-29 (extension) · self-model fibre without self-authority
# ---------------------------------------------------------------------------------------------

SELF_AUTH = {"self_model": 1}            # no world_truth, no commit
PROPOSAL_AUTH = {"proposal": 1}
OBJECT_SCOPE, SELF_SCOPE = frozenset({"task"}), frozenset({"self"})


def admissible_edge(e, self_atoms):
    """Rule E1(i): an edge with a K_self tail may only have K_self heads (diagnoses propose, never derive)."""
    tails, heads = set(e[1]), set(e[2])
    return not (tails & self_atoms) or heads <= self_atoms


def mutant_self_edge_into_object(edges, self_atom, object_atom):
    """Planted: a self-diagnosis used as a SUPPORT tail of an object-level claim."""
    return list(edges) + [edge("selfdiag->obj", self_atom, object_atom, rel="SUPPORT")]


def closure_certificate(target_iv, cert_scope, cert_channel, target_scope):
    """T10(i) closure ⟦L,U⟧ ↦ ⟦L,L⟧, admitted only for an EXPERIMENTATION/EXACT_CHECKER certificate whose scope meets the target's."""
    if cert_channel not in ("EXPERIMENTATION", "EXACT_CHECKER") or not (cert_scope & target_scope):
        return "REFUSED_SCOPE_OR_CHANNEL", target_iv
    return "APPLIED", (target_iv[0], target_iv[0])


def mutant_self_diagnosis_promotes_object(target_iv):
    """Planted: a K_self record ('operator op is correct on the task scope') applied as a closure certificate on an object claim."""
    return (target_iv[0], target_iv[0])


def internal_compose_authority(op_authority, tail_authorities):
    return auth_meet(op_authority, *tail_authorities)


def mutant_self_record_raises_world_truth(op_authority, tail_authorities):
    keys = set(op_authority).union(*(set(a) for a in tail_authorities))
    return {k: max([op_authority.get(k, 0)] + [a.get(k, 0) for a in tail_authorities]) for k in keys}


def proposal_atom(trigger_ids, prediction_id):
    """A self-change proposal: ⟦0, U⟧ with U = its trigger evidence ⊗ its prediction record (all in E_self); authority proposal only."""
    return (ZERO, meet(cert(frozenset(trigger_ids))[1], cert({prediction_id})[1])), PROPOSAL_AUTH


def adopt(proposal_iv, receipt):
    """External adoption: the adopted-change atom is ⟦{{e_A}}⟧ ⊗ the proposal's upper support; only an external commit receipt counts."""
    if receipt.get("authority", {}).get("commit", 0) < 1 or receipt.get("source") != "external":
        return "REFUSED_NOT_EXTERNAL_COMMIT", proposal_iv
    e_a = receipt["evidence_id"]
    return "ADOPTED", (meet(cert({e_a})[0], proposal_iv[1]), meet(cert({e_a})[1], proposal_iv[1]))


def mutant_adopted_by_own_prediction(proposal_iv, prediction_id):
    """Planted: the proposal's own prediction record used as the adoption evidence."""
    return (meet(cert({prediction_id})[0], proposal_iv[1]), meet(cert({prediction_id})[1], proposal_iv[1]))


def check_e1_meg29_self_model_fibre():
    rng = random.Random(51)
    spaces = liveness_checks = activation_checks = edge_rule_checks = self_query_checks = 0
    mutant_edge_refused = mutant_edge_changes_activation = 0
    for _ in range(30):
        obj_atoms, obj_edges = random_space(rng, 6, 8, 3, prefix="o", ev_prefix="e")
        self_atoms, self_edges = random_space(rng, 4, 5, 3, prefix="s", ev_prefix="t")   # traces / receipts t0..t2
        e_obj = frozenset().union(*(evidence_of(iv) for iv in obj_atoms.values()))
        e_self = frozenset().union(*(evidence_of(iv) for iv in self_atoms.values()))
        assert not (e_obj & e_self)                                          # disjoint supports (scope task vs self)
        joint_atoms, joint_edges = {**obj_atoms, **self_atoms}, obj_edges + self_edges
        assert all(admissible_edge(e, frozenset(self_atoms)) for e in joint_edges)
        edge_rule_checks += len(joint_edges)
        seed, self_seed = next(iter(obj_atoms)), next(iter(self_atoms))
        for R in [r | s for r in subsets(e_obj) for s in (frozenset(), frozenset({"t0"}))]:
            # (i) liveness of every object atom depends on R ∩ E_obj only; admitting K_self (or revoking a trace) changes nothing
            for x, iv in obj_atoms.items():
                assert liveness(iv, R) == liveness(iv, R & e_obj) == liveness(joint_atoms[x], R)
                liveness_checks += 1
            # (i) activation on the object fibre identical with and without the self fibre (no rows from K_self)
            a_obj = activation(obj_atoms, obj_edges, R, seed)
            a_joint = activation(joint_atoms, joint_edges, R, seed)
            assert all(a_joint[x] == a_obj[x] for x in obj_atoms)
            activation_checks += 1
        # a query seeded in K_self activates no object atom (the other direction of non-interference)
        a_self = activation(joint_atoms, joint_edges, frozenset(), self_seed)
        assert all(a_self[x] == 0 for x in obj_atoms)
        self_query_checks += 1
        # planted: a diagnosis edge into the object level — refused by the rule; if applied, a self-seeded query activates the object atom it feeds
        target = next(x for x in obj_atoms if x != seed)
        bad_edges = mutant_self_edge_into_object(joint_edges, self_seed, target)
        assert not all(admissible_edge(e, frozenset(self_atoms)) for e in bad_edges)
        mutant_edge_refused += 1
        a_bad = activation(joint_atoms, bad_edges, frozenset(), self_seed)
        assert a_bad[target] > 0 and a_self[target] == 0
        mutant_edge_changes_activation += 1
        spaces += 1
    # (ii) authority: a composition with a K_self tail has world_truth 0 and commit 0; the mutant raises both
    obj_auth = {"world_truth": 1, "commit": 1}
    composed = internal_compose_authority({"world_truth": 1}, [obj_auth, SELF_AUTH])
    assert composed.get("world_truth", 0) == 0 and composed.get("commit", 0) == 0
    raised = mutant_self_record_raises_world_truth({"world_truth": 1}, [obj_auth, SELF_AUTH])
    assert raised["world_truth"] == 1 and raised["commit"] == 1 and raised != composed
    # (ii) a self record cannot act as a closure certificate on an object claim (scope self ∩ task = ∅): the verdict of the claim is untouched
    claim = (cert({"e0"})[0], join(cert({"e0"})[0], cert({"e1"})[0]))        # ⟦{{e0}}, {{e0},{e1}}⟧: UNKNOWN under {e0}
    status, after = closure_certificate(claim, SELF_SCOPE, "OBSERVATION", OBJECT_SCOPE)
    assert status == "REFUSED_SCOPE_OR_CHANNEL" and after == claim and liveness(claim, {"e0"}) == UNKNOWN
    promoted = mutant_self_diagnosis_promotes_object(claim)
    assert promoted != claim and liveness(promoted, {"e0"}) == DEAD          # mutation applied: a self record moved an object verdict
    ok, closed = closure_certificate(claim, OBJECT_SCOPE, "EXPERIMENTATION", OBJECT_SCOPE)
    assert ok == "APPLIED" and closed == promoted                             # no-alarm: an object-scope closure certificate does close
    # (iii) a proposal is ⟦0,U⟧: never LIVE under any R; adopted only through an external commit receipt
    p_iv, p_auth = proposal_atom(("t0", "t1"), "pred1")
    assert p_auth == PROPOSAL_AUTH and p_auth.get("commit", 0) == 0
    for R in subsets(["t0", "t1", "pred1"]):
        assert liveness(p_iv, R) in (UNKNOWN, DEAD)
    ext = {"evidence_id": "eA", "authority": {"commit": 1}, "source": "external"}
    status, adopted = adopt(p_iv, ext)
    assert status == "ADOPTED" and liveness(adopted, frozenset()) == LIVE and liveness(adopted, {"eA"}) == DEAD and liveness(adopted, {"t0"}) == DEAD
    assert adopt(p_iv, {"evidence_id": "pred1", "authority": SELF_AUTH, "source": "internal"})[0] == "REFUSED_NOT_EXTERNAL_COMMIT"
    assert adopt(p_iv, {"evidence_id": "x", "authority": {"commit": 1}, "source": "internal"})[0] == "REFUSED_NOT_EXTERNAL_COMMIT"   # the machine signing its own commit
    bad = mutant_adopted_by_own_prediction(p_iv, "pred1")
    assert liveness(bad, frozenset()) == LIVE and not (evidence_of(bad) - frozenset({"t0", "t1", "pred1"}))   # LIVE with self evidence only: caught
    return {"random_spaces": spaces, "object_liveness_checks": liveness_checks, "object_activation_checks": activation_checks, "edge_rule_checks": edge_rule_checks,
            "self_seeded_query_inert_on_objects": self_query_checks, "mutant_self_edge_refused": mutant_edge_refused, "mutant_self_edge_activates_object": mutant_edge_changes_activation, "mutant_world_truth_raised_caught": 1,
            "mutant_self_diagnosis_promotes_object_caught": 1, "object_closure_no_alarm": 1, "proposal_never_live_checks": 8, "adoption_refusals": 2,
            "mutant_adopted_by_own_prediction_caught": 1}


# ---------------------------------------------------------------------------------------------
# E2 · M11 §3 · diagnostic layer soundness on a finite trace grammar
# ---------------------------------------------------------------------------------------------

FIELDS = {"complete": (True, False), "resource": ("OK", "EXHAUSTED"), "authority": ("OK", "MISSING"), "drift": ("NONE", "DRIFT"), "info": ("PRESENT", "MISSING"),
          "order": ("OK", "BAD"), "router": ("CORRECT", "WRONG"), "operator": ("OK", "DEFECT"), "adapter": ("OK", "BAD")}
ALTERNATIVES = ("router_alt", "operator_alt", "adapter_alt")
ATTEMPT = (None, (LIVE, False), (LIVE, True), (DEAD, False), (DEAD, True))      # untried | (warrant, succeeded)
METHOD = ("WRONG_OPERATOR", "OPERATOR_WRONG", "BAD_ADAPTER")
OTHER = ("CANNOT_CHECK", "RESOURCE", "AUTHORITY", "DRIFT", "MISSING_INFORMATION", "BAD_ORDER")


def certificate_valid(attempts, witness):
    """E3 content: every registered lower-level alternative tried, none succeeded, every attempt warrant LIVE, ceiling witness present."""
    return all(attempts[a] is not None for a in ALTERNATIVES) and not any(attempts[a][1] for a in ALTERNATIVES) and all(attempts[a][0] == LIVE for a in ALTERNATIVES) and witness


def classify(trace):
    """Layer classifier: a pure function of the typed trace (stage verdicts + registered attempts + witness)."""
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
        return "MISSING_INFORMATION"                     # a missing registered input is a GAP, never an obstruction (S5)
    if f["order"] == "BAD":
        return "BAD_ORDER"
    if certificate_valid(attempts, witness):
        return "REPRESENTATION"                           # the certificate contains the method attempts: it dominates the run's own fields
    if f["router"] == "WRONG":
        return "WRONG_OPERATOR"
    if f["operator"] == "DEFECT":
        return "OPERATOR_WRONG"
    if f["adapter"] == "BAD":
        return "BAD_ADAPTER"
    return "INSUFFICIENT_EVIDENCE"                        # all stages nominal, no certificate: gather evidence (CANNOT_CHECK class), never escalate


def mutant_repeated_failure_escalates(trace, frequency=3):
    """Planted (M11 §2/§4 hostile): repeated failure without a certificate is read as an architecture problem."""
    f, attempts, witness = trace
    honest = classify(trace)
    if honest in METHOD + ("INSUFFICIENT_EVIDENCE",) and frequency >= 3:
        return "REPRESENTATION"
    return honest


def mutant_ignore_certificate(trace):
    """Planted (M11 §4 hostile, 'representation failure blamed on method'): the run's own method fields are read before the certificate."""
    f, attempts, witness = trace
    honest = classify(trace)
    if honest == "REPRESENTATION":
        if f["router"] == "WRONG":
            return "WRONG_OPERATOR"
        if f["operator"] == "DEFECT":
            return "OPERATOR_WRONG"
        if f["adapter"] == "BAD":
            return "BAD_ADAPTER"
    return honest


def all_traces():
    keys = list(FIELDS)
    for values in itertools.product(*(FIELDS[k] for k in keys)):
        f = dict(zip(keys, values))
        for att in itertools.product(ATTEMPT, repeat=3):
            attempts = dict(zip(ALTERNATIVES, att))
            for witness in (True, False):
                yield (f, attempts, witness)


def check_e2_m11_diagnostic_layer_soundness():
    n = rep = method = insufficient = 0
    rep_iff = replay = other_agree = 0
    m1_caught = m2_caught = 0
    restoring_operator_traces = 0
    for trace in all_traces():
        f, attempts, witness = trace
        v = classify(trace)
        n += 1
        nominal = f["complete"] and f["resource"] == "OK" and f["authority"] == "OK" and f["drift"] == "NONE" and f["info"] == "PRESENT" and f["order"] == "OK"
        # (a) REPRESENTATION ⇔ nominal ∧ certificate valid (the certificate checked independently)
        assert (v == "REPRESENTATION") == (nominal and certificate_valid(attempts, witness))
        rep_iff += 1
        # (b) every METHOD verdict has an invalid certificate; INSUFFICIENT_EVIDENCE never escalates
        if v in METHOD:
            assert not certificate_valid(attempts, witness)
            method += 1
        rep += v == "REPRESENTATION"
        insufficient += v == "INSUFFICIENT_EVIDENCE"
        # (c) replay: the verdict is a function of the serialised trace (sampled)
        if n % 101 == 0:
            ser = json.loads(json.dumps(trace))
            assert classify((ser[0], {k: (tuple(x) if x else None) for k, x in ser[1].items()}, ser[2])) == v
            replay += 1
        # (d) hostiles
        if attempts["operator_alt"] is not None and attempts["operator_alt"][1] and nominal and v in METHOD + ("INSUFFICIENT_EVIDENCE",):
            restoring_operator_traces += 1
            assert mutant_repeated_failure_escalates(trace) == "REPRESENTATION" and v != "REPRESENTATION"    # method failure triggers a Jump: caught
            m1_caught += 1
        if v == "REPRESENTATION" and (f["router"] == "WRONG" or f["operator"] == "DEFECT" or f["adapter"] == "BAD"):
            assert mutant_ignore_certificate(trace) in METHOD                                                  # representation failure blamed on method: caught
            m2_caught += 1
        # no-alarm: the mutants agree with the honest verdict on the OTHER classes (they only differ on the two hostile shapes)
        if v in OTHER:
            assert mutant_repeated_failure_escalates(trace) == mutant_ignore_certificate(trace) == v
            other_agree += 1
    # S5 false structural alarm: missing dependency plus a valid-looking certificate is MISSING_INFORMATION
    s5 = ({**{k: v[0] for k, v in FIELDS.items()}, "info": "MISSING"}, {a: (LIVE, False) for a in ALTERNATIVES}, True)
    assert classify(s5) == "MISSING_INFORMATION" and certificate_valid(s5[1], s5[2])
    return {"traces": n, "representation_iff_certificate_checks": rep_iff, "representation_verdicts": rep, "method_verdicts_all_without_certificate": method,
            "insufficient_evidence_verdicts": insufficient, "replay_checks": replay, "restoring_operator_traces": restoring_operator_traces, "mutant_repeated_failure_escalates_caught": m1_caught,
            "mutant_ignore_certificate_caught": m2_caught, "other_class_no_alarm": other_agree, "s5_missing_dependency_is_gap": 1}


# ---------------------------------------------------------------------------------------------
# E3 · MEG-28 / M11 §4 · obstruction certificate content on the M4 Boolean fixture; B8 DPO machinery
# ---------------------------------------------------------------------------------------------

F1, FA, FB, FAB = (1, 1, 1, 1), (0, 0, 1, 1), (0, 1, 0, 1), (0, 0, 0, 1)
FEATURES = {"feat_1": F1, "feat_a": FA, "feat_b": FB, "feat_ab": FAB}
FEATURE_EVIDENCE = {"feat_1": "r1", "feat_a": "r2", "feat_b": "r3", "feat_ab": "r4"}
ALL_TABLES = [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]


def xor_span(tables):
    out = set()
    for coeffs in itertools.product((0, 1), repeat=len(tables)):
        out.add(tuple(sum(c * f[i] for c, f in zip(coeffs, tables)) % 2 for i in range(4)))
    return frozenset(out)


def name(table):
    return "h_" + "".join(map(str, table))


def parity_witness(q, span):
    """A checkable ceiling witness: every composition has even weight while q has odd weight."""
    return "PARITY" if all(sum(t) % 2 == 0 for t in span) and sum(q) % 2 == 1 else None


def obstruction_certificate(Q, representation, revoked):
    """ObstructionCertificate(Q, R, witness): every registered operator composition under R fails on every q ∈ Q with all warrants LIVE, plus a ceiling witness."""
    ops = {f: FEATURES[f] for f in representation}
    warrants = {f: liveness(cert({FEATURE_EVIDENCE[f]}), revoked) for f in ops}
    if any(w != LIVE for w in warrants.values()):
        return {"status": "REINSTATE_FIRST", "dead": sorted(f for f, w in warrants.items() if w != LIVE)}
    span = xor_span(list(ops.values()))
    fails = {q: q not in span for q in Q}
    if not all(fails.values()):
        return {"status": "LOWER_LEVEL_SUFFICIENT", "reachable": sorted(name(q) for q in Q if q in span)}
    witnesses = {name(q): parity_witness(q, span) for q in Q}
    if any(w is None for w in witnesses.values()):
        return {"status": "NO_WITNESS"}
    return {"status": "OBSTRUCTION", "compositions_tried": len(span), "witness": witnesses, "attempts_live": True}


def mutant_certificate_without_live_clause(Q, representation, revoked):
    """Planted: the LIVE-warrant clause dropped — compositions over the *live* features only, dead alternatives counted as failures."""
    ops = [FEATURES[f] for f in representation if liveness(cert({FEATURE_EVIDENCE[f]}), revoked) == LIVE]
    span = xor_span(ops)
    return {"status": "OBSTRUCTION" if all(q not in span for q in Q) else "LOWER_LEVEL_SUFFICIENT"}


def mutant_partial_enumeration(Q, representation, revoked):
    """Planted: only depth-1 operators tried (no compositions)."""
    singles = frozenset(FEATURES[f] for f in representation)
    return {"status": "OBSTRUCTION" if all(q not in singles for q in Q) else "LOWER_LEVEL_SUFFICIENT"}


STRONG_TRIGGERS = frozenset({"EXPRESSIVE_CEILING", "STRUCTURAL_NONIDENTIFIABILITY", "MODEL_FAMILY_INADEQUACY", "GLOBAL_OBSTRUCTION"})


def trigger_from_certificate(cert_record):
    """The governed-Jump trigger is built from the certificate and from nothing else."""
    if cert_record["status"] != "OBSTRUCTION":
        return None
    return {"kind": "EXPRESSIVE_CEILING", "incumbent_level": 1, "proposal_level": 3, "witness_ids": sorted(cert_record["witness"])}


def space_digest(space):
    atoms, edges = space
    return digest((sorted((x, t, iv) for x, (t, iv) in atoms.items()), sorted(edges)))


def dpo_apply(space, rule, trigger, assessment, commit_receipt):
    """B8's DPO rewrite L ← I → R with identity match; refuses with a typed reason."""
    atoms, edges = space
    L, I, R = rule
    if trigger is None or trigger["kind"] not in STRONG_TRIGGERS or trigger["incumbent_level"] >= trigger["proposal_level"] or not trigger.get("witness_ids"):
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


def m4_fixture():
    feats = {"feat_1": ("representation", cert({"r1"})), "feat_a": ("representation", cert({"r2"})), "feat_b": ("representation", cert({"r3"}))}
    atoms = dict(feats)
    atoms["phi_affine"] = ("representation", cert({"r1", "r2", "r3"}))
    edges = [(f"{f}->phi", (f,), ("phi_affine",), "COMPOSITION") for f in feats]
    for table in sorted(xor_span([F1, FA, FB])):
        atoms[name(table)] = ("procedure", cert({"r1", "r2", "r3"}))
        edges.append((f"feats->{name(table)}", ("feat_1", "feat_a", "feat_b"), (name(table),), "COMPOSITION"))
    atoms.update({"goal_AND": ("goal", cert({"g"})), "renderer": ("procedure", cert({"v"})), "report": ("summary", cert({"v"})), "archive": ("summary", cert({"v"})), "unrelated": ("claim", cert({"u"}))})
    edges += [("phi->renderer", ("phi_affine",), ("renderer",), "DEPENDENCE"), ("renderer->report", ("renderer",), ("report",), "DEPENDENCE"), ("report->archive", ("report",), ("archive",), "DEPENDENCE")]
    L_atoms = {**feats, "phi_affine": atoms["phi_affine"], "renderer": atoms["renderer"]}
    L_edges = [e for e in edges if e[0] in {"feat_1->phi", "feat_a->phi", "feat_b->phi", "phi->renderer"}]
    I = (("feat_1", "feat_a", "feat_b", "renderer"), ())
    R_atoms = {**feats, "renderer": atoms["renderer"], "feat_ab": ("representation", cert({"r4"})), "phi_quad": ("representation", cert({"r1", "r2", "r3", "r4"})), "h_0001": ("procedure", cert({"r4"}))}
    R_edges = [(f"{f}->phi_quad", (f,), ("phi_quad",), "COMPOSITION") for f in ("feat_1", "feat_a", "feat_b", "feat_ab")] + [("feat_ab->h_0001", ("feat_ab",), ("h_0001",), "COMPOSITION"), ("phi_quad->renderer", ("phi_quad",), ("renderer",), "DEPENDENCE")]
    return (atoms, edges), ((L_atoms, L_edges), I, (R_atoms, R_edges))


COMMIT = {"commit": 1, "source": "external"}
AFFINE, QUAD = ("feat_1", "feat_a", "feat_b"), ("feat_1", "feat_a", "feat_b", "feat_ab")


def check_e3_meg28_obstruction_certificate():
    space, rule = m4_fixture()
    revs = subsets(["r1", "r2", "r3"])
    # (i) the certificate is exactly the precondition of the governed Jump: over all 16 targets × 8 revocations of the affine features
    agree = obstructions = 0
    for q in ALL_TABLES:
        for R in revs:
            c = obstruction_certificate([q], AFFINE, R)
            status, _ = dpo_apply(space, rule, trigger_from_certificate(c), "CANDIDATE_FOR_PROTECTED_EVALUATION", COMMIT)
            assert (status == "APPLIED") == (c["status"] == "OBSTRUCTION")
            agree += 1
            obstructions += c["status"] == "OBSTRUCTION"
    assert obstructions == 8                              # exactly the 8 odd-weight tables under R = ∅ (parity witness), never under a revocation
    assert obstruction_certificate([FAB], AFFINE, frozenset())["status"] == "OBSTRUCTION"           # AND ∉ affine span: obstruction, Jump admissible
    xor = (0, 1, 1, 0)
    assert obstruction_certificate([xor], AFFINE, frozenset())["status"] == "LOWER_LEVEL_SUFFICIENT"   # XOR ∈ affine span: no certificate, Jump refused
    assert obstruction_certificate([FAB], QUAD, frozenset())["status"] == "LOWER_LEVEL_SUFFICIENT"     # after the Jump the same query is reachable
    # (ii) a dead-warrant failure is not an obstruction: with feat_b revoked, XOR is unreachable from {1, a} — REINSTATE_FIRST, not OBSTRUCTION
    dead_b = frozenset({"r3"})
    honest = obstruction_certificate([xor], AFFINE, dead_b)
    assert honest["status"] == "REINSTATE_FIRST" and honest["dead"] == ["feat_b"]
    bad = mutant_certificate_without_live_clause([xor], AFFINE, dead_b)
    assert bad["status"] == "OBSTRUCTION"                                                           # mutation applied and caught
    assert obstruction_certificate([xor], AFFINE, frozenset())["status"] == "LOWER_LEVEL_SUFFICIENT"   # reinstating feat_b makes XOR reachable
    assert dpo_apply(space, rule, trigger_from_certificate(honest), "CANDIDATE_FOR_PROTECTED_EVALUATION", COMMIT)[0] == "REFUSED_TRIGGER_NOT_ADMISSIBLE"
    # (iii) a partial enumeration (depth-1 only) certifies XOR falsely
    partial = mutant_partial_enumeration([xor], AFFINE, frozenset())
    assert partial["status"] == "OBSTRUCTION" and obstruction_certificate([xor], AFFINE, frozenset())["status"] != "OBSTRUCTION"
    # (iv) no-alarm: a query family fully inside the span never produces a certificate; the AND certificate names its witness and 8 compositions
    c_and = obstruction_certificate([FAB], AFFINE, frozenset())
    assert c_and["compositions_tried"] == 8 and c_and["witness"] == {"h_0001": "PARITY"}
    assert obstruction_certificate([F1, FA, xor], AFFINE, frozenset())["status"] == "LOWER_LEVEL_SUFFICIENT"
    return {"target_x_revocation_checks": agree, "obstructions_found": obstructions, "and_obstruction": 1, "xor_lower_level_sufficient": 1, "post_jump_reachable": 1,
            "mutant_without_live_clause_caught": 1, "reinstate_makes_reachable": 1, "mutant_partial_enumeration_caught": 1, "compositions_tried_for_and": c_and["compositions_tried"], "in_span_family_no_alarm": 1}


# ---------------------------------------------------------------------------------------------
# E4 · M11 §5/§8/§10 · proposal object, pre-outcome prediction, external adoption on unseen tasks
# ---------------------------------------------------------------------------------------------

CLASSES = ("C0", "C1", "C2", "C3", "C4", "C5", "C6")
PROTECTED = ("adoption.", "assurance.", "constitution.", "meter.", "authority.")


def adopt_decision(proposal, prediction_digest_before_access, realised_heldout, token, self_score=None):
    """ADOPT iff the external adopter confirms the realised held-out effect matches the pre-registered prediction within its margin.
    `self_score` (the proposer's own evaluation) is accepted as an argument and never read."""
    if proposal["change_class"] == "C6" or any(proposal["target"].startswith(p) for p in PROTECTED):
        return "REFUSED_CONSTITUTION_OR_PROTECTED"
    if token is None or token.get("source") != "external":
        return "REFUSED_NOT_EXTERNAL"
    if digest(proposal["prediction"]) != prediction_digest_before_access:
        return "REFUSED_PREDICTION_AFTER_OUTCOME"
    if set(realised_heldout) & set(proposal["dev_tasks"]):
        return "REFUSED_TASKS_SEEN_BY_PROPOSER"
    pred, m = proposal["prediction"]["effect"], proposal["prediction"]["margin"]
    if all(abs(realised_heldout[f] - pred[f]) <= m for f in pred):
        return "ADOPT"
    return "REFUSED_PREDICTION_MISSED"


def mutant_graded_on_dev_tasks(proposal, prediction_digest_before_access, realised_dev, token):
    """Planted: the realised effect measured on the proposer's own dev tasks."""
    p = dict(proposal)
    p["dev_tasks"] = ()
    return adopt_decision(p, prediction_digest_before_access, realised_dev, token)


def check_e4_m11_proposal_prediction_adoption():
    deltas = (-2, -1, 0, 1, 2)
    fams = ("fam_x", "fam_y")
    ext, internal = {"source": "external", "id": "gov"}, {"source": "internal", "id": "self"}
    n = adopts = overfit_caught = overfit_cases = pessimistic_cases = 0
    spec_agree = leak = nondep = 0
    for pred in itertools.product(deltas, repeat=2):
        for real_h in itertools.product(deltas, repeat=2):
            for real_d in itertools.product((-2, 0, 2), repeat=2):
                for m in (0, 1):
                    prop = {"id": "p", "change_class": "C2", "target": "operator.parse", "dev_tasks": ("d1", "d2"),
                            "prediction": {"effect": dict(zip(fams, pred)), "margin": m, "families": fams}}
                    before = digest(prop["prediction"])
                    rh, rd = dict(zip(fams, real_h)), dict(zip(fams, real_d))
                    v = adopt_decision(prop, before, rh, ext)
                    # (i) the decision equals the specification predicate written independently
                    spec = "ADOPT" if all(abs(rh[f] - pred[i]) <= m for i, f in enumerate(fams)) else "REFUSED_PREDICTION_MISSED"
                    assert v == spec
                    spec_agree += 1
                    adopts += v == "ADOPT"
                    # (ii) syntactic non-dependence on the proposer's own evaluation
                    assert adopt_decision(prop, before, rh, ext, self_score=+99) == v == adopt_decision(prop, before, rh, ext, self_score=-99)
                    nondep += 1
                    # (iii) self-adoption and post-outcome prediction are refused
                    assert adopt_decision(prop, before, rh, internal) == "REFUSED_NOT_EXTERNAL" and adopt_decision(prop, before, rh, None) == "REFUSED_NOT_EXTERNAL"
                    late = dict(prop, prediction={"effect": rh, "margin": m, "families": fams})   # prediction written after seeing the outcome
                    assert adopt_decision(late, before, rh, ext) == ("REFUSED_PREDICTION_AFTER_OUTCOME" if digest(late["prediction"]) != before else v)
                    leak += 1
                    # (iv) the dev-task mutant: adopts on memorised dev gains the held-out refutes
                    bad = mutant_graded_on_dev_tasks(prop, before, rd, ext)
                    if bad == "ADOPT" and v != "ADOPT":
                        overfit_cases += 1
                        overfit_caught += 1
                    if bad != "ADOPT" and v == "ADOPT":
                        pessimistic_cases += 1
                    n += 1
    # the memorising challenger witness: dev +2 on both families, held-out −1; predicted +2, margin 1
    prop = {"id": "p", "change_class": "C2", "target": "operator.parse", "dev_tasks": ("d1", "d2"), "prediction": {"effect": {"fam_x": 2, "fam_y": 2}, "margin": 1, "families": fams}}
    before = digest(prop["prediction"])
    assert adopt_decision(prop, before, {"fam_x": -1, "fam_y": -1}, ext) == "REFUSED_PREDICTION_MISSED"
    assert mutant_graded_on_dev_tasks(prop, before, {"fam_x": 2, "fam_y": 2}, ext) == "ADOPT"
    # held-out tasks the proposer saw are refused as held-out; C6 and protected targets refused regardless of outcome
    assert adopt_decision(prop, before, {"d1": 2, "fam_y": 2}, ext) == "REFUSED_TASKS_SEEN_BY_PROPOSER"
    assert adopt_decision(dict(prop, change_class="C6"), before, {"fam_x": 2, "fam_y": 2}, ext) == "REFUSED_CONSTITUTION_OR_PROTECTED"
    assert adopt_decision(dict(prop, target="adoption.threshold", change_class="C0"), before, {"fam_x": 2, "fam_y": 2}, ext) == "REFUSED_CONSTITUTION_OR_PROTECTED"
    # no-alarm: an honest proposal whose prediction is realised on unseen tasks is adopted
    assert adopt_decision(prop, before, {"fam_x": 2, "fam_y": 1}, ext) == "ADOPT"
    return {"decision_cases": n, "spec_agreement": spec_agree, "adopted": adopts, "self_score_nondependence": nondep, "leak_and_self_adoption_refusals": leak,
            "mutant_dev_tasks_overfit_cases": overfit_cases, "mutant_dev_tasks_caught": overfit_caught, "mutant_dev_tasks_pessimistic_cases": pessimistic_cases,
            "memorising_challenger_refused": 1, "seen_tasks_refused": 1, "c6_and_protected_refused": 2, "honest_adopted_no_alarm": 1}


# ---------------------------------------------------------------------------------------------
# E5 · M11 §9 · shadow execution non-interference and the assurance receipt chain
# ---------------------------------------------------------------------------------------------


def incumbent_op(task):
    return (task[0] + task[1]) % 2          # XOR


def challenger_op(task):
    return task[0] & task[1]                # AND


def hard_gates(answer, task):
    """The same hard gates for both arms: a typed answer, an authority record, a scope."""
    return {"typed": answer in (0, 1), "authority": "world_truth", "scope": "task"}


def run_stream(stream, shadow=None, mutant=None):
    obj, commits, kself, chain = {}, [], [], "genesis"
    for i, task in enumerate(stream):
        ans = incumbent_op(task)
        obj[f"task:{task}"] = ans
        commits.append((task, ans, "incumbent"))
        if shadow is not None:
            snapshot = digest(obj)
            cans = shadow(task)
            receipt = {"i": i, "task": task, "snapshot": snapshot, "challenger": cans, "incumbent": ans, "gates": hard_gates(cans, task), "prev": chain}
            chain = digest(receipt)
            receipt["hash"] = chain
            kself.append(receipt)
            if mutant == "writes_object":
                obj[f"task:{task}"] = cans
            if mutant == "commits_externally":
                commits.append((task, cans, "shadow"))
    return digest(obj), digest(commits), kself


def chain_valid(kself):
    prev = "genesis"
    for r in kself:
        body = {k: v for k, v in r.items() if k != "hash"}
        if body["prev"] != prev or digest(body) != r["hash"]:
            return False
        prev = r["hash"]
    return True


def mutant_edit_receipt(kself):
    """Planted: a shadow receipt edited after the fact (a gate verdict flipped)."""
    out = [dict(r) for r in kself]
    out[0]["gates"] = dict(out[0]["gates"], typed=False)
    return out


def check_e5_m11_shadow_non_interference():
    rng = random.Random(55)
    streams = identical = receipts = object_mutant_caught = 0
    for _ in range(30):
        stream = [(rng.randint(0, 1), rng.randint(0, 1)) for _ in range(rng.randint(1, 8))]
        o0, c0, k0 = run_stream(stream)
        o1, c1, k1 = run_stream(stream, shadow=challenger_op)
        # (i) object-level state and every external commitment identical with and without the shadow; K_self grew by one receipt per task
        assert o0 == o1 and c0 == c1 and k0 == [] and len(k1) == len(stream)
        # (ii) the shadow read the frozen snapshot the incumbent produced at the same index (replay)
        for i, r in enumerate(k1):
            assert r["snapshot"] == run_stream(stream[: i + 1])[0]
        # (iii) assurance = the receipt chain under the same hard gates, tamper-evident
        assert chain_valid(k1) and all(r["gates"] == hard_gates(r["incumbent"], r["task"]) for r in k1)
        bad = mutant_edit_receipt(k1)
        assert bad[0]["gates"] != k1[0]["gates"] and not chain_valid(bad)
        # planted: the shadow writes to the object store / commits externally — caught by the digests
        o2, c2, _ = run_stream(stream, shadow=challenger_op, mutant="writes_object")
        o3, c3, _ = run_stream(stream, shadow=challenger_op, mutant="commits_externally")
        assert c2 == c0 and (o2 != o0) == any(incumbent_op(t) != challenger_op(t) for t in stream)
        object_mutant_caught += o2 != o0
        assert o3 == o0 and c3 != c0
        identical += 1
        receipts += len(k1)
        streams += 1
    assert object_mutant_caught > 0
    # a stream on which the two operators agree everywhere is the no-alarm case for the object-store mutant (nothing to catch, nothing alarmed)
    agree_stream = [(0, 0), (0, 0)]
    assert run_stream(agree_stream, shadow=challenger_op, mutant="writes_object")[0] == run_stream(agree_stream)[0]
    return {"streams": streams, "object_and_commitments_identical": identical, "shadow_receipts": receipts, "snapshot_replay_checks": receipts,
            "mutant_shadow_writes_object_caught": object_mutant_caught, "mutant_shadow_commits_externally_caught": streams, "mutant_edit_receipt_caught": streams, "agreeing_stream_no_alarm": 1}


# ---------------------------------------------------------------------------------------------
# E6 · MEG-18 / MEG-28 / M11 §11–12 · adoption as a stamped DPO rewrite; exact rollback incl. caches
# ---------------------------------------------------------------------------------------------


def stamp_rule(rule, e_a):
    """Every object the adoption produces (R ∖ I) carries the adoption evidence e_A in its warrant (batch-1 T4 stamping)."""
    L, I, R = rule
    R_atoms = {x: (attr if x in I[0] else (attr[0], imeet(attr[1], cert({e_a})))) for x, attr in R[0].items()}
    return (L, I, (R_atoms, R[1]))


def compile_cache(space):
    """A compiled cache: which goal tables are reachable (FOUND) under the current representation."""
    atoms, _ = space
    reachable = frozenset(x for x, (t, _) in atoms.items() if t == "procedure" and x.startswith("h_"))
    return {name(q): ("FOUND" if name(q) in reachable else "GAP") for q in ALL_TABLES}


def adopt_change(space, cache, rule, e_a, trigger):
    stamped = stamp_rule(rule, e_a)
    status, after = dpo_apply(space, stamped, trigger, "CANDIDATE_FOR_PROTECTED_EVALUATION", COMMIT)
    if status != "APPLIED":
        return status, space, cache, None
    # a cached conclusion derived from the produced procedure (an object the change produced transitively)
    after[0]["cached_and_conclusion"] = ("claim", imeet(after[0]["h_0001"][1], cert({"c"})))
    after[1].append(("h_0001->cached", ("h_0001",), ("cached_and_conclusion",), "DEPENDENCE"))
    return status, after, compile_cache(after), stamped


def rollback_change(space, cache, stamped_rule, e_a):
    """Revoke e_A, quarantine every object whose evidence contains e_A, apply the inverse rewrite, recompile the cache."""
    atoms, edges = space
    quarantined = frozenset(x for x, (_, iv) in atoms.items() if e_a in evidence_of(iv))
    kept = {x: a for x, a in atoms.items() if x not in quarantined}
    kept_edges = [e for e in edges if not ((set(e[1]) | set(e[2])) & quarantined)]
    L, I, R = stamped_rule
    R_left = ({x: a for x, a in R[0].items() if x in I[0]}, [])            # the produced objects are already quarantined; the inverse re-inserts L
    status, restored = dpo_apply((kept, kept_edges), (R_left, I, L), {"kind": "EXPRESSIVE_CEILING", "incumbent_level": 1, "proposal_level": 3, "witness_ids": ["rollback"]}, "CANDIDATE_FOR_PROTECTED_EVALUATION", COMMIT)
    return status, restored, compile_cache(restored), quarantined


def mutant_rollback_leaves_cache(space, cache, stamped_rule, e_a):
    status, restored, _, q = rollback_change(space, cache, stamped_rule, e_a)
    return status, restored, cache, q


def mutant_rollback_without_revoke(space, cache, stamped_rule, e_a):
    """Planted: the component table is rolled back (the rule's own R ∖ I removed, L re-inserted) without revoking e_A —
    an object derived from the adoption outside the rule's image is never found and stays LIVE."""
    L, I, R = stamped_rule
    produced_by_rule = set(R[0]) - set(I[0])
    atoms, edges = space
    kept = {x: a for x, a in atoms.items() if x not in produced_by_rule}
    kept_edges = [e for e in edges if not ((set(e[1]) | set(e[2])) & produced_by_rule)]
    R_left = ({x: a for x, a in R[0].items() if x in I[0]}, [])
    status, restored = dpo_apply((kept, kept_edges), (R_left, I, L), {"kind": "EXPRESSIVE_CEILING", "incumbent_level": 1, "proposal_level": 3, "witness_ids": ["rollback"]}, "CANDIDATE_FOR_PROTECTED_EVALUATION", COMMIT)
    return status, restored, compile_cache(restored), frozenset(produced_by_rule)


def check_e6_meg18_reopen_and_exact_rollback():
    space, rule = m4_fixture()
    cache = compile_cache(space)
    h_before = digest([space_digest(space), cache])
    e_a = "eA"
    trigger = trigger_from_certificate(obstruction_certificate([FAB], AFFINE, frozenset()))
    status, after, cache_after, stamped = adopt_change(space, cache, rule, e_a, trigger)
    assert status == "APPLIED" and cache["h_0001"] == "GAP" and cache_after["h_0001"] == "FOUND"
    # (i) every produced object carries e_A; every interface / untouched object keeps its interval (B8 (i))
    produced = frozenset(x for x, (_, iv) in after[0].items() if e_a in evidence_of(iv))
    assert produced == {"feat_ab", "phi_quad", "h_0001", "cached_and_conclusion"}
    preserved = sum(1 for x, attr in space[0].items() if x in after[0] and after[0][x] == attr)
    assert preserved == len(space[0]) - 1                                    # only phi_affine left the space
    # (ii) revoking e_A kills exactly the produced objects; the reopening set is their impact cone (KS-T22), nothing else
    dead = frozenset(x for x, (_, iv) in after[0].items() if liveness(iv, {e_a}) == DEAD)
    cone = impact_cone(produced, [edge(e[0], e[1], e[2], rel=e[3]) for e in after[1]])
    assert dead == produced and cone == produced | {"renderer", "report", "archive"} and "unrelated" not in cone
    # (iii) rollback = revoke + quarantine + inverse rewrite + cache recompile: state hash equality with the pre-adoption state
    st, restored, cache_back, quarantined = rollback_change(after, cache_after, stamped, e_a)
    assert st == "APPLIED" and quarantined == produced and space_digest(restored) == space_digest(space) and cache_back == cache
    assert digest([space_digest(restored), cache_back]) == h_before
    # planted: rollback that leaves the compiled cache — the hash differs and the cache still answers FOUND for AND on the affine space
    st2, restored2, cache2, _ = mutant_rollback_leaves_cache(after, cache_after, stamped, e_a)
    assert st2 == "APPLIED" and space_digest(restored2) == space_digest(space) and cache2 != cache and cache2["h_0001"] == "FOUND"
    assert digest([space_digest(restored2), cache2]) != h_before
    # planted: rollback without revocation — the cached conclusion derived from the adoption survives LIVE
    st3, restored3, _, q3 = mutant_rollback_without_revoke(after, cache_after, stamped, e_a)
    assert st3 == "APPLIED" and q3 == {"feat_ab", "phi_quad", "h_0001"} and q3 < produced
    assert "cached_and_conclusion" in restored3[0] and liveness(restored3[0]["cached_and_conclusion"][1], frozenset()) == LIVE and space_digest(restored3) != space_digest(space)
    assert "cached_and_conclusion" not in restored[0]
    # no-alarm: an atom outside the cone keeps interval and liveness through adoption and rollback
    assert after[0]["unrelated"] == space[0]["unrelated"] == restored[0]["unrelated"]
    return {"adoption_applied": 1, "produced_objects": sorted(produced), "interface_and_untouched_preserved": preserved, "reopening_set": sorted(cone),
            "rollback_state_hash_equal": 1, "mutant_rollback_leaves_cache_caught": 1, "mutant_rollback_without_revoke_caught": 1, "unrelated_unchanged": 1}


# ---------------------------------------------------------------------------------------------
# E7 · MEG-30 (extension) · meta-level termination: metered proposals, no meter edits, bounded adoptions
# ---------------------------------------------------------------------------------------------


def run_self_loop(rng, budget, charge, cap=200, schedule=None, meter_edit=None, window_budget=None):
    """Self-modification loop: every proposal charges δ (a registered schedule may only raise it); an adoption is a metered proposal that passed."""
    meter, proposals, adoptions, steps, log = Fraction(0), 0, 0, 0, []
    delta = Fraction(charge)
    while steps < cap:
        steps += 1
        if meter_edit is not None and proposals >= 1:
            delta = meter_edit(delta)                    # planted: a proposal that edits the meter's charge for future proposals
        elif schedule is not None:
            delta = max(delta, Fraction(schedule(proposals)))
        if delta <= 0:
            return "REFUSED_UNMETERED", log, steps
        if meter + delta > budget:
            log.append(("CANNOT_CHECK", meter))
            return "CANNOT_CHECK", log, steps
        meter += delta
        proposals += 1
        if window_budget is not None and adoptions >= window_budget:
            log.append(("ADOPTION_REFUSED_WINDOW", proposals))
            continue
        if rng.random() < 0.5:
            adoptions += 1
            log.append(("adopt", proposals, meter))
    return "LIVELOCK_AT_CAP", log, steps


def mutant_proposal_sets_charge_zero(delta):
    return Fraction(0)


def mutant_proposal_halves_future_charge(delta):
    return delta / 2


def proposal_touches_meter(proposal):
    return proposal["target"].startswith("meter.") or any(str(k).startswith("meter") for k in proposal["change"])


def check_e7_meg30_meta_termination():
    rng = random.Random(57)
    runs = 0
    for budget in (1, 2, 3, 5, 8, 13, 21):
        for charge in (Fraction(1), Fraction(1, 2), Fraction(2)):
            status, log, steps = run_self_loop(rng, budget, charge)
            proposals = sum(1 for e in log if e[0] == "adopt") + sum(1 for e in log if e[0] == "ADOPTION_REFUSED_WINDOW")
            # (i) the loop terminates in CANNOT_CHECK and the number of metered proposals is ≤ ⌊B/δ⌋
            assert status == "CANNOT_CHECK" and steps - 1 <= budget // charge
            runs += 1
    # (ii) adoptions per window bounded by the window budget, independent of the outcome draws
    for w in (0, 1, 2, 3):
        status, log, _ = run_self_loop(random.Random(w), budget=20, charge=1, window_budget=w)
        assert sum(1 for e in log if e[0] == "adopt") <= w and status == "CANNOT_CHECK"
    # (iii) the schedule may raise the charge, never lower it: a rising schedule terminates faster
    s_flat = run_self_loop(random.Random(3), budget=10, charge=1)[2]
    s_rise = run_self_loop(random.Random(3), budget=10, charge=1, schedule=lambda k: 1 + k)[2]
    assert s_rise < s_flat
    # planted 1: a proposal that sets the charge to zero — refused as unmetered by the loop (KS-S7); the protected-target rule refuses it before it runs
    status0, _, _ = run_self_loop(random.Random(1), budget=5, charge=1, meter_edit=mutant_proposal_sets_charge_zero)
    assert status0 == "REFUSED_UNMETERED"
    assert proposal_touches_meter({"target": "meter.charge", "change": {"charge": 0}}) and not proposal_touches_meter({"target": "operator.parse", "change": {"impl": "v2"}})
    # planted 2: a proposal that halves the future charge — Σ δ/2^k < 2δ ≤ B, so the loop never reaches the budget: livelock at the cap
    status_h, log_h, steps_h = run_self_loop(random.Random(2), budget=2, charge=1, meter_edit=mutant_proposal_halves_future_charge, cap=60)
    assert status_h == "LIVELOCK_AT_CAP" and steps_h == 60
    # no-alarm: a window budget that is never reached leaves every adoption in place
    status_n, log_n, _ = run_self_loop(random.Random(4), budget=3, charge=1, window_budget=10)
    assert status_n == "CANNOT_CHECK" and not any(e[0] == "ADOPTION_REFUSED_WINDOW" for e in log_n)
    return {"budget_x_charge_runs": runs, "window_bound_checks": 4, "rising_schedule_terminates_faster": 1, "mutant_charge_zero_refused": 1, "mutant_halving_livelocks_at_cap": 1,
            "meter_target_detected": 1, "unreached_window_no_alarm": 1}


# ---------------------------------------------------------------------------------------------
# E8 · KS-T12 / KS-T14 improvement halves as CONJECTURES with exact falsifiers
# ---------------------------------------------------------------------------------------------


def nav_cost(edges, seed, target):
    """Exact navigation cost: edges traversed by a breadth-first walk from the seed until the target is reached (all edges if never)."""
    seen, frontier, cost = {seed}, [seed], 0
    while frontier:
        nxt = []
        for x in frontier:
            for e in edges:
                if x in e[1]:
                    cost += 1
                    for h in e[2]:
                        if h == target:
                            return cost, True
                        if h not in seen:
                            seen.add(h)
                            nxt.append(h)
        frontier = nxt
    return cost, False


def chain_space(k):
    """Seed s → x1 → … → xk → t; consolidated: s → m → t with m exporting x1..xk (B7 shape)."""
    fine = [edge("s->x1", "s", "x1")] + [edge(f"x{i}->x{i+1}", f"x{i}", f"x{i+1}") for i in range(1, k)] + [edge(f"x{k}->t", f"x{k}", "t")]
    coarse = [edge("s->m", "s", "m"), edge("m->t", "m", "t")]
    return fine, coarse


def multiscale_cost(fine, coarse, target, exported):
    """D7's rule: coarse walk first; a coarse GAP (target not exported) is REFINE_REQUIRED and the fine walk runs too."""
    c_cost, found = nav_cost(coarse, "s", target if target in exported else "__absent__")
    if found:
        return c_cost
    f_cost, _ = nav_cost(fine, "s", target)
    return c_cost + f_cost


def falsify_ks_t12(k, Q):
    fine, coarse = chain_space(k)
    exported = {"t", "m", "s"}
    before = sum(nav_cost(fine, "s", q)[0] for q in Q)
    after = sum(multiscale_cost(fine, coarse, q, exported) for q in Q)
    return before, after, after < before


def falsify_ks_t14(Q, before_rep, after_rep):
    span0, span1 = xor_span([FEATURES[f] for f in before_rep]), xor_span([FEATURES[f] for f in after_rep])
    c0, c1 = sum(q in span0 for q in Q), sum(q in span1 for q in Q)
    return c0, c1, c1 > c0


def check_e8_improvement_conjectures():
    # KS-T12: consolidation improves future navigation cost on the registered Q — holds on the smallest chain with two internals, fails once Q reaches an internal
    holds = [(k, falsify_ks_t12(k, ["t"])) for k in (1, 2, 3, 4)]
    smallest_hold = next(k for k, (b, a, ok) in holds if ok)
    assert smallest_hold == 2 and holds[0][1] == (2, 2, False)               # k = 1: 2 edges either way — no improvement; k = 2: 3 → 2
    fails = [(k, falsify_ks_t12(k, ["t", "x1"])) for k in (1, 2, 3, 4)]
    smallest_fail = next(k for k, (b, a, ok) in fails if not ok)
    assert smallest_fail == 1 and fails[0][1][1] > fails[0][1][0]            # coarse GAP + descend costs more than the fine walk alone
    assert all(not ok for _, (_, _, ok) in fails[:2]) and fails[3][1][2]     # the failure is Q-dependent: at k = 4 the export saving dominates again
    # KS-T14: a Jump improves the expressive ceiling on Q — holds for Q = {AND}, fails (no change) for Q = {XOR}, and a lift can even lower it (S6 shape)
    and_ok = falsify_ks_t14([FAB], AFFINE, QUAD)
    xor_same = falsify_ks_t14([(0, 1, 1, 0)], AFFINE, QUAD)
    harmful = falsify_ks_t14([(0, 1, 1, 0)], AFFINE, ("feat_1", "feat_ab"))
    assert and_ok == (0, 1, True) and xor_same == (1, 1, False) and harmful == (1, 0, False)
    whole = falsify_ks_t14(ALL_TABLES, AFFINE, QUAD)
    assert whole == (8, 16, True)
    # the falsifiers are exact functions of the fixture: replay gives the same verdicts
    assert falsify_ks_t12(2, ["t"]) == (3, 2, True) and falsify_ks_t14([FAB], AFFINE, QUAD) == and_ok
    return {"ks_t12_status": "CONJECTURE", "ks_t12_smallest_holding_chain": smallest_hold, "ks_t12_smallest_failing_chain_with_internal_query": smallest_fail,
            "ks_t12_costs_by_k_target_only": {k: [b, a] for k, (b, a, _) in holds}, "ks_t12_costs_by_k_with_internal": {k: [b, a] for k, (b, a, _) in fails},
            "ks_t14_status": "CONJECTURE", "ks_t14_holds_on": "Q={AND}: 0→1", "ks_t14_fails_on": "Q={XOR}: 1→1", "ks_t14_harmful_lift": "R'={1,ab} on Q={XOR}: 1→0",
            "ks_t14_whole_family": list(whole[:2])}


# ---------------------------------------------------------------------------------------------
# R1 · MEG-19 deconsolidation half · R2 · MEG-27 open-inventory half · R3 · MEG-02 graded half
# ---------------------------------------------------------------------------------------------


def summary_interval(corr, exported):
    out = corr
    for iv in exported:
        out = imeet(out, iv)
    return out


def b7_space():
    atoms = {"x1": cert({"a"}), "x2": cert({"d"}), "x3": cert({"a", "c"}), "x4": cert({"a", "c"}, {"f"}), "ex1": cert({"g"}), "other": cert({"z"})}
    edges = [edge("x1x3", "x1", "x3", rel="COMPOSITION"), edge("x3x4", "x3", "x4", rel="COMPOSITION"), edge("x2x4", "x2", "x4", rel="DEPENDENCE")]
    return atoms, edges


def consolidate(space):
    atoms, edges = space
    a2, e2 = dict(atoms), list(edges)
    a2["m"] = summary_interval(cert({"k"}), [atoms["x1"], atoms["x4"]])
    e2 += [edge("sum", ("x1", "x2", "x3", "x4"), "m", rel="COMPOSITION"), edge("exc", "ex1", "m", rel="LINEAGE")]
    return a2, e2


def deconsolidate(space):
    atoms, edges = space
    return {x: iv for x, iv in atoms.items() if x != "m"}, [e for e in edges if "m" not in e[1] and "m" not in e[2]]


def mutant_deconsolidate_keeps_summary_edge(space):
    atoms, edges = space
    return {x: iv for x, iv in atoms.items() if x != "m"}, list(edges)


def check_r1_meg19_deconsolidation():
    space = b7_space()
    cons = consolidate(space)
    back = deconsolidate(cons)
    # exactness: undo restores the constituent space byte-identically; answers on Q (liveness of the exports over Γ) identical before and after
    assert back[0] == space[0] and [e[0] for e in back[1]] == [e[0] for e in space[1]]
    gammas = subsets(["a", "c", "d", "f", "g", "k", "z"])
    agree = 0
    for R in gammas:
        for x in ("x1", "x4", "other"):
            assert liveness(space[0][x], R) == liveness(cons[0][x], R) == liveness(back[0][x], R)
            agree += 1
    bad = mutant_deconsolidate_keeps_summary_edge(cons)
    assert "m" not in bad[0] and any("m" in e[2] for e in bad[1])            # a dangling summary edge: not the undo
    # cost table (a fact about the fixture, not a law): through the macro an answer costs 1 hop plus one check per registered exception; direct costs the chain
    fine, coarse = chain_space(3)
    direct = nav_cost(fine, "s", "t")[0]
    via = {k: nav_cost(coarse, "s", "t")[0] + k for k in range(0, 5)}
    crossover = next(k for k, c in via.items() if c >= direct)
    return {"undo_exact": 1, "answers_preserved_over_gamma": agree, "mutant_dangling_summary_caught": 1, "direct_cost_chain3": direct, "via_macro_cost_by_exceptions": via,
            "exception_crossover": crossover, "decision_criterion": "OPEN_PARENT_OWNED (MDL library choice: DreamCoder/LILO)"}


# MEG-27: prefix commitment over a *regular* (infinite) inventory decided by DFA reachability, no bound
DFA = {(0, "NP"): 1, (1, "VP"): 2, (1, "CONJ"): 3, (3, "NP"): 1}
ACCEPT = {2}
TOKENS = {"NP1": ("NP", "ref1", None), "NP2": ("NP", "ref2", None), "CONJ": ("CONJ", None, None), "VP1": ("VP", None, "c1"), "VP2": ("VP", None, "c2")}


def token_ok(tok, state):
    _, ref, claim = TOKENS[tok]
    return (ref is None or ref in state["refs"]) and (claim is None or state["live"].get(claim) == LIVE)


def dfa_state(prefix):
    s = 0
    for tok in prefix:
        s = DFA.get((s, TOKENS[tok][0]))
        if s is None:
            return None
    return s


def lookahead_regular(prefix, state):
    """SAT iff an accepting DFA state is reachable from the prefix's state through acceptable tokens (reachability: exact, no bound)."""
    if any(not token_ok(t, state) for t in prefix):
        return "UNSAT"
    s = dfa_state(prefix)
    if s is None:
        return "UNSAT"
    seen, frontier = {s}, [s]
    while frontier:
        nxt = []
        for q in frontier:
            if q in ACCEPT:
                return "SAT"
            for tok in TOKENS:
                q2 = DFA.get((q, TOKENS[tok][0]))
                if q2 is not None and token_ok(tok, state) and q2 not in seen:
                    seen.add(q2)
                    nxt.append(q2)
        frontier = nxt
    return "UNSAT"


def lookahead_bounded(prefix, state, k):
    """Batch-3 C3's bounded check: SAT / UNSAT / CANNOT_CHECK when continuations remain at the bound."""
    if any(not token_ok(t, state) for t in prefix) or dfa_state(prefix) is None:
        return "UNSAT"
    cut = False
    frontier = {dfa_state(prefix)}
    for depth in range(k + 1):
        if any(q in ACCEPT for q in frontier):
            return "SAT"
        if depth == k:
            cut = bool(frontier)
            break
        frontier = {DFA[(q, TOKENS[t][0])] for q in frontier for t in TOKENS if (q, TOKENS[t][0]) in DFA and token_ok(t, state)}
    return "CANNOT_CHECK" if cut else "UNSAT"


def mutant_bound_is_pass(prefix, state, k):
    v = lookahead_bounded(prefix, state, k)
    return "SAT" if v == "CANNOT_CHECK" else v


def check_r2_meg27_regular_inventory():
    prefixes = [p for n in range(0, 4) for p in itertools.product(TOKENS, repeat=n) if dfa_state(p) is not None]
    states = [{"live": {"c1": l1, "c2": l2}, "refs": set(r)} for l1 in (LIVE, DEAD) for l2 in (LIVE, DEAD) for r in subsets(["ref1", "ref2"])]
    n_states = len({q for (q, _) in DFA} | set(DFA.values()))
    agree = decided = cannot = sat_complete = cyclic_cannot = 0
    mutant_caught = 0
    for p in prefixes:
        for st in states:
            reg = lookahead_regular(p, st)
            for k in range(0, n_states + 1):
                b = lookahead_bounded(p, st, k)
                if b != "CANNOT_CHECK":
                    assert b == reg                                          # the bounded verdict never contradicts reachability
                    agree += 1
                else:
                    cannot += 1
                    decided += 1                                             # reachability decides what the bound could not
                    if mutant_bound_is_pass(p, st, k) == "SAT" and reg == "UNSAT":
                        mutant_caught += 1
            # a completion exists iff one of length < |states| exists (a simple path), so the bound k = |states| is complete for SAT;
            # UNSAT on a cyclic inventory is never reached by the bound (the frontier cycles NP CONJ NP …): only reachability decides it
            b_full = lookahead_bounded(p, st, n_states)
            assert (reg == "SAT") == (b_full == "SAT") and (reg != "UNSAT" or b_full in ("UNSAT", "CANNOT_CHECK"))
            sat_complete += 1
            cyclic_cannot += reg == "UNSAT" and b_full == "CANNOT_CHECK"
    assert cannot > 0 and mutant_caught > 0 and cyclic_cannot > 0
    # no-alarm: with every claim LIVE and every referent resolvable, every prefix of NP1 VP1 commits
    full = {"live": {"c1": LIVE, "c2": LIVE}, "refs": {"ref1", "ref2"}}
    assert all(lookahead_regular(("NP1", "VP1")[:i], full) == "SAT" for i in range(3))
    # the inventory is infinite (NP CONJ NP CONJ … VP), so batch-3's finite-inventory theorem did not cover it
    assert dfa_state(("NP1", "CONJ", "NP2", "CONJ", "NP1", "VP1")) in ACCEPT
    return {"prefixes": len(prefixes), "discourse_states": len(states), "dfa_states": n_states, "bounded_agrees_when_decisive": agree, "bounded_cannot_check_cases": cannot,
            "decided_by_reachability": decided, "sat_complete_at_state_bound": sat_complete, "unsat_unreachable_by_bound_cases": cyclic_cannot, "mutant_bound_is_pass_caught": mutant_caught,
            "status": "PROVED_REGULAR_INVENTORY; non-regular acceptability OPEN"}


# MEG-02 graded half: recorded witness that the naive graded lifts break exact-share retraction (T11(ii) / KS-T04b), not a theorem
def check_r3_meg02_graded_witness():
    # (max, ×) Viterbi: two derivations of x with scores; revoking the top source leaves no inverse — the label must be recomputed, not adjusted
    s1, s2 = Fraction(9, 10), Fraction(6, 10)
    viterbi = max(s1, s2)
    after_revoke_top = max([s2])                                             # recomputation over the surviving derivations
    subtractive = viterbi - s1                                               # a 'retraction by subtraction' has no meaning in (max, ×)
    assert after_revoke_top == s2 and subtractive != after_revoke_top
    # (+, ×) probability-sum: two sources sharing an assumption a count it twice (T11(ii) violated), unlike the antichain semiring
    pa, pb1, pb2 = Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)
    naive_sum = pa * pb1 + pa * pb2                                          # counts a twice
    exact = pa * (pb1 + pb2 - pb1 * pb2)                                     # a once, then either b
    antichain = liveness((canon([frozenset({"a", "b1"}), frozenset({"a", "b2"})]),) * 2, {"a"})
    assert naive_sum != exact and antichain == DEAD
    return {"status": "OPEN", "reason": "no additive inverse in (max,×); (+,×) double-counts shared assumptions — exact-share retraction (KS-T04b) needs certified-only gating (D3) or a new rule",
            "viterbi_recompute_vs_subtract": [str(after_revoke_top), str(subtractive)], "shared_assumption_naive_vs_exact": [str(naive_sum), str(exact)]}


# ---------------------------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------------------------

CHECKS = {
    "E1_MEG29_self_model_fibre": check_e1_meg29_self_model_fibre,
    "E2_M11S3_diagnostic_layer_soundness": check_e2_m11_diagnostic_layer_soundness,
    "E3_MEG28_obstruction_certificate": check_e3_meg28_obstruction_certificate,
    "E4_M11S5_proposal_prediction_adoption": check_e4_m11_proposal_prediction_adoption,
    "E5_M11S9_shadow_non_interference": check_e5_m11_shadow_non_interference,
    "E6_MEG18_reopen_and_exact_rollback": check_e6_meg18_reopen_and_exact_rollback,
    "E7_MEG30_meta_termination": check_e7_meg30_meta_termination,
    "E8_KST12_KST14_conjectures": check_e8_improvement_conjectures,
    "R1_MEG19_deconsolidation": check_r1_meg19_deconsolidation,
    "R2_MEG27_regular_inventory": check_r2_meg27_regular_inventory,
    "R3_MEG02_graded_witness": check_r3_meg02_graded_witness,
}


def run_all():
    out = {name_: fn() for name_, fn in CHECKS.items()}
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
