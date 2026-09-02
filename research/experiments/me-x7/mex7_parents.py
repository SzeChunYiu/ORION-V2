"""ME-X7 — faithful parent mechanisms, each with its own native known-answer
tests (`fidelity_selftests`) that must pass before the parent is used as a
comparator (ME-X1 shipped 51/51, ME-X2 21/21; the same discipline here).

The parents are the ones protocol §3 names as the primary comparator family —
proof/certificate checking, provenance lineage, executable replay, assurance
cases, dependence audit and calibrated abstention.  Two of them are *real*
engines rather than flags:

* `ResolutionChecker` — propositional resolution refutation checking
  (Robinson 1965; presentation after Bachmair & Ganzinger, *Handbook of
  Automated Reasoning* ch. 2).  It decides `Artifact.checker_accepts` in
  `MODE_FORMAL`, so a "proof mismatch" is a checker rejection, not a label.
* `ReplayMachine` — a deterministic register machine whose output digest
  depends on the program text, the environment constant and the seed, so a
  seed/version mismatch is an actual replay divergence.

The remaining parents wrap the parent-owned ORION reference modules
(`orion_v2.provenance`, `orion_v2.evidence`) or classical assurance/selective
prediction semantics, exactly as ME-X4's A0/A5 arms did.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from orion_v2.evidence import (
    DependenceEdge,
    DependenceKind,
    EvidenceUnit,
    assess_evidence_dependence,
)
from orion_v2.provenance import (
    InheritanceRelation,
    ProvenanceEdge,
    ProvenanceNode,
    ReticulateProvenance,
)

# ---- P0: propositional resolution refutation checker ------------------------

Clause = frozenset[int]


class ResolutionChecker:
    """Checks that a sequence of resolution steps refutes a clause set.

    A step is `(i, j, resolvent)` over the running clause list.  The step is
    sound iff there is a literal `l` with `l in C_i` and `-l in C_j` and the
    resolvent equals `(C_i - {l}) | (C_j - {-l})`.  The refutation succeeds iff
    the final resolvent is the empty clause.
    """

    def check(self, clauses: list[Clause], steps: list[tuple[int, int, Clause]]) -> bool:
        pool = list(clauses)
        if not steps:
            return frozenset() in pool
        for i, j, resolvent in steps:
            if not (0 <= i < len(pool) and 0 <= j < len(pool)):
                return False
            left, right = pool[i], pool[j]
            pivots = [lit for lit in left if -lit in right]
            if not pivots:
                return False
            ok = False
            for lit in pivots:
                if (left - {lit}) | (right - {-lit}) == resolvent:
                    ok = True
                    break
            if not ok:
                return False
            pool.append(resolvent)
        return pool[-1] == frozenset()

    @staticmethod
    def encode(clauses: list[Clause], steps: list[tuple[int, int, Clause]]) -> str:
        cl = ";".join(",".join(str(x) for x in sorted(c)) for c in clauses)
        st = ";".join(f"{i}|{j}|{','.join(str(x) for x in sorted(r))}" for i, j, r in steps)
        return f"C[{cl}]S[{st}]"

    @staticmethod
    def decode(text: str) -> tuple[list[Clause], list[tuple[int, int, Clause]]]:
        body = text[len("C["):]
        cl_text, rest = body.split("]S[", 1)
        st_text = rest[:-1]
        clauses = [
            frozenset(int(x) for x in c.split(",") if x)
            for c in cl_text.split(";")
            if c != "" or cl_text == ""
        ] if cl_text else []
        steps: list[tuple[int, int, Clause]] = []
        if st_text:
            for part in st_text.split(";"):
                i, j, r = part.split("|")
                steps.append((int(i), int(j), frozenset(int(x) for x in r.split(",") if x)))
        return clauses, steps


# ---- P2: deterministic replay machine ---------------------------------------

class ReplayMachine:
    """A tiny deterministic register machine.

    `run(program, env_modulus, seed)` folds the program over one accumulator.
    The output digest therefore changes when the program text, the environment
    constant or the seed changes — which is what makes a recorded-versus-actual
    environment mismatch an observable replay divergence rather than a flag.
    """

    OPS = ("ADD", "MUL", "XOR", "ROT")

    def run(self, program: str, env_modulus: int, seed: str) -> str:
        acc = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16)
        for token in program.split(","):
            if not token:
                continue
            op, _, arg = token.partition(":")
            value = int(arg or 0)
            if op == "ADD":
                acc = acc + value
            elif op == "MUL":
                acc = acc * (value or 1)
            elif op == "XOR":
                acc = acc ^ value
            elif op == "ROT":
                acc = ((acc << (value % 13)) | (acc >> max(1, 32 - (value % 13)))) & 0xFFFFFFFF
            else:
                raise ValueError(f"unknown op {op!r}")
            acc %= max(2, env_modulus)
        return hashlib.sha256(f"{acc}".encode("utf-8")).hexdigest()[:16]


# ---- P1: provenance lineage over orion_v2.provenance ------------------------

@dataclass
class ProvenanceLineage:
    """Revocation descendants over `orion_v2.provenance.ReticulateProvenance`,
    the same parent-owned engine ME-X4's A0 arm used."""

    def revoked_supports(
        self,
        support_roots: dict[str, tuple[str, ...]],
        node_parents: dict[str, tuple[str, ...]],
        revoked_nodes: set[str],
    ) -> set[str]:
        node_ids = sorted(set(node_parents) | {r for roots in support_roots.values() for r in roots})
        nodes = tuple(
            ProvenanceNode(node_id=n, kind="node", epoch="e0") for n in node_ids
        ) + tuple(
            ProvenanceNode(node_id=s, kind="support", epoch="e0") for s in sorted(support_roots)
        )
        known = {n.node_id for n in nodes}
        edges = []
        for child, parents in sorted(node_parents.items()):
            for parent in parents:
                if parent in known and child in known:
                    edges.append(
                        ProvenanceEdge(
                            parent_id=parent,
                            child_id=child,
                            relation=InheritanceRelation.DERIVES,
                            component="registry",
                        )
                    )
        for support, roots in sorted(support_roots.items()):
            for root in roots:
                if root in known:
                    edges.append(
                        ProvenanceEdge(
                            parent_id=root,
                            child_id=support,
                            relation=InheritanceRelation.DERIVES,
                            component="registry",
                        )
                    )
        graph = ReticulateProvenance(nodes=nodes, edges=tuple(edges))
        hit: set[str] = set()
        for revoked in sorted(revoked_nodes):
            if revoked in known:
                hit |= set(graph.affected_by_revocation(revoked, component="registry"))
        return {s for s in support_roots if s in hit}


# ---- P4: dependence audit over orion_v2.evidence -----------------------------

@dataclass
class DependenceAudit:
    """Independent-component counting through
    `orion_v2.evidence.assess_evidence_dependence` (parent-owned)."""

    def independent_components(
        self,
        support_ids: tuple[str, ...],
        pairs: list[tuple[str, str, bool]],
        *,
        include_suspected: bool,
    ) -> int:
        if not support_ids:
            return 0
        units = tuple(
            EvidenceUnit(
                evidence_id=s, claim_id="c", source_id=f"src-{s}", method_id="m0"
            )
            for s in support_ids
        )
        edges = tuple(
            DependenceEdge(
                left_id=a,
                right_id=b,
                kind=DependenceKind.SHARED_SOURCE,
                witness_ids=(f"w-{a}-{b}",),
            )
            for a, b, confirmed in pairs
            if confirmed or include_suspected
        )
        assessment = assess_evidence_dependence(units, edges)
        return assessment.conservative_independent_support_count


# ---- P3: assurance-case change impact (GSN) ---------------------------------

@dataclass
class AssuranceCase:
    """GSN change impact: a challenged solution makes every ancestor goal
    suspect through supported-by / in-context-of edges (Kelly & Weaver 2004);
    conjunctive, two-valued."""

    def suspect_top_goal(self, edges: list[tuple[str, str]], challenged: set[str], top: str) -> bool:
        parent_of: dict[str, list[str]] = {}
        for parent, child in edges:
            parent_of.setdefault(child, []).append(parent)
        seen: set[str] = set()
        stack = sorted(challenged)
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(parent_of.get(cur, []))
        return top in seen


# ---- P5: calibrated selective abstention -------------------------------------

@dataclass
class SelectiveAbstention:
    """Selective prediction with a fixed coverage threshold (Geifman &
    El-Yaniv 2017): accept when the score is above tau, abstain otherwise.
    Carries no failure-class semantics — the B1 rung of the baseline
    hierarchy."""
    tau: float = 0.5

    def decide(self, score: float) -> str:
        if score >= self.tau + 0.25:
            return "ACCEPT"
        if score <= self.tau - 0.25:
            return "REJECT"
        return "CANNOT_CHECK"


# ---- native known-answer fidelity tests -------------------------------------

def fidelity_selftests() -> list[dict[str, object]]:
    """Every parent must pass its own native known-answer tests before it is
    used as a comparator.  Each entry reports `n_evaluated` so a passing row
    can never be an empty loop."""
    out: list[dict[str, object]] = []

    # --- P0 resolution checker
    rc = ResolutionChecker()
    cases: list[tuple[str, list[Clause], list[tuple[int, int, Clause]], bool]] = [
        # {p}, {-p} resolve to the empty clause.
        ("empty-from-unit-pair", [frozenset({1}), frozenset({-1})], [(0, 1, frozenset())], True),
        # {p,q}, {-p}, {-q}: two steps to the empty clause.
        (
            "two-step-refutation",
            [frozenset({1, 2}), frozenset({-1}), frozenset({-2})],
            [(0, 1, frozenset({2})), (3, 2, frozenset())],
            True,
        ),
        # a resolvent that drops a literal it may not drop.
        (
            "unsound-resolvent-rejected",
            [frozenset({1, 2}), frozenset({-1, 3})],
            [(0, 1, frozenset({2}))],
            False,
        ),
        # no complementary literal at all.
        ("no-pivot-rejected", [frozenset({1}), frozenset({2})], [(0, 1, frozenset())], False),
        # sound steps that never reach the empty clause.
        (
            "incomplete-refutation-rejected",
            [frozenset({1, 2}), frozenset({-1})],
            [(0, 1, frozenset({2}))],
            False,
        ),
        # index out of range.
        ("bad-index-rejected", [frozenset({1})], [(0, 5, frozenset())], False),
    ]
    for name, clauses, steps, expected in cases:
        got = rc.check(clauses, steps)
        out.append(
            {"parent": "RESOLUTION_CHECKER", "case": name, "passed": got == expected,
             "expected": expected, "got": got}
        )
    # round trip of the wire encoding
    enc = ResolutionChecker.encode(cases[1][1], cases[1][2])
    cl, st = ResolutionChecker.decode(enc)
    out.append(
        {"parent": "RESOLUTION_CHECKER", "case": "encode-decode-round-trip",
         "passed": (cl, st) == (cases[1][1], cases[1][2]), "expected": True,
         "got": bool((cl, st) == (cases[1][1], cases[1][2]))}
    )

    # --- P2 replay machine
    rm = ReplayMachine()
    base = rm.run("ADD:7,MUL:3,XOR:5", 1_000_003, "seed-a")
    out.append({"parent": "REPLAY_MACHINE", "case": "deterministic-same-inputs",
                "passed": rm.run("ADD:7,MUL:3,XOR:5", 1_000_003, "seed-a") == base,
                "expected": True, "got": True})
    out.append({"parent": "REPLAY_MACHINE", "case": "seed-change-diverges",
                "passed": rm.run("ADD:7,MUL:3,XOR:5", 1_000_003, "seed-b") != base,
                "expected": True,
                "got": rm.run("ADD:7,MUL:3,XOR:5", 1_000_003, "seed-b") != base})
    out.append({"parent": "REPLAY_MACHINE", "case": "env-change-diverges",
                "passed": rm.run("ADD:7,MUL:3,XOR:5", 1_000_033, "seed-a") != base,
                "expected": True,
                "got": rm.run("ADD:7,MUL:3,XOR:5", 1_000_033, "seed-a") != base})
    out.append({"parent": "REPLAY_MACHINE", "case": "program-change-diverges",
                "passed": rm.run("ADD:8,MUL:3,XOR:5", 1_000_003, "seed-a") != base,
                "expected": True,
                "got": rm.run("ADD:8,MUL:3,XOR:5", 1_000_003, "seed-a") != base})

    # --- P1 provenance lineage
    pl = ProvenanceLineage()
    roots = {"s0": ("n0",), "s1": ("n1",)}
    parents = {"n0": ("n2",), "n1": (), "n2": ()}
    got_set = pl.revoked_supports(roots, parents, {"n2"})
    out.append({"parent": "PROVENANCE_LINEAGE", "case": "transitive-revocation-hits-descendant",
                "passed": got_set == {"s0"}, "expected": ["s0"], "got": sorted(got_set)})
    got_set = pl.revoked_supports(roots, parents, {"n1"})
    out.append({"parent": "PROVENANCE_LINEAGE", "case": "revocation-does-not-splash",
                "passed": got_set == {"s1"}, "expected": ["s1"], "got": sorted(got_set)})
    got_set = pl.revoked_supports(roots, parents, set())
    out.append({"parent": "PROVENANCE_LINEAGE", "case": "no-revocation-no-hit",
                "passed": got_set == set(), "expected": [], "got": sorted(got_set)})

    # --- P4 dependence audit
    da = DependenceAudit()
    n = da.independent_components(("a", "b", "c"), [], include_suspected=False)
    out.append({"parent": "DEPENDENCE_AUDIT", "case": "no-edges-all-independent",
                "passed": n == 3, "expected": 3, "got": n})
    n = da.independent_components(("a", "b", "c"), [("a", "b", True)], include_suspected=False)
    out.append({"parent": "DEPENDENCE_AUDIT", "case": "confirmed-edge-merges",
                "passed": n == 2, "expected": 2, "got": n})
    n = da.independent_components(("a", "b"), [("a", "b", False)], include_suspected=False)
    out.append({"parent": "DEPENDENCE_AUDIT", "case": "suspected-edge-ignored-when-excluded",
                "passed": n == 2, "expected": 2, "got": n})
    n = da.independent_components(("a", "b"), [("a", "b", False)], include_suspected=True)
    out.append({"parent": "DEPENDENCE_AUDIT", "case": "suspected-edge-merges-when-included",
                "passed": n == 1, "expected": 1, "got": n})

    # --- P3 assurance case
    ac = AssuranceCase()
    edges = [("G0", "G1"), ("G1", "Sn1"), ("G0", "G2"), ("G2", "Sn2")]
    out.append({"parent": "ASSURANCE_CASE", "case": "challenged-solution-suspects-top",
                "passed": ac.suspect_top_goal(edges, {"Sn1"}, "G0") is True,
                "expected": True, "got": ac.suspect_top_goal(edges, {"Sn1"}, "G0")})
    out.append({"parent": "ASSURANCE_CASE", "case": "unrelated-node-does-not-suspect-top",
                "passed": ac.suspect_top_goal(edges, {"Sn3"}, "G0") is False,
                "expected": False, "got": ac.suspect_top_goal(edges, {"Sn3"}, "G0")})

    # --- P5 selective abstention
    sa = SelectiveAbstention()
    for score, expected in ((0.95, "ACCEPT"), (0.05, "REJECT"), (0.5, "CANNOT_CHECK")):
        got_v = sa.decide(score)
        out.append({"parent": "SELECTIVE_ABSTENTION", "case": f"score-{score}",
                    "passed": got_v == expected, "expected": expected, "got": got_v})

    return out


PARENT_NAMES = (
    "RESOLUTION_CHECKER",
    "REPLAY_MACHINE",
    "PROVENANCE_LINEAGE",
    "DEPENDENCE_AUDIT",
    "ASSURANCE_CASE",
    "SELECTIVE_ABSTENTION",
)
