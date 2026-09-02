#!/usr/bin/env python3
"""ME-X4 parent baselines (frozen with design V1, §4).

Each parent is implemented against its native semantics and carries its own
known-answer tests (`fidelity_selftests()`), which must pass before the parent
is used as a comparator (ME_X4_PARENT_FIDELITY_RECEIPT_V1.md).

  JTMS            Doyle 1979 (IN/OUT labels, SL-justifications with in/out
                  lists, well-founded support, dependency-directed
                  contradiction handling); algorithm structure after Forbus &
                  de Kleer 1993, "Building Problem Solvers", ch. 7.
  ATMS            de Kleer 1986 (assumptions, environments, minimal consistent
                  labels, nogoods, subsumption).
  KernelBase      AGM-style belief-base contraction: Hansson kernel
                  contraction with an entrenchment-driven incision function
                  (success, inclusion, core-retainment, vacuity), Levi
                  revision.
  NoisyOrSupport  Bayesian/support-graph baseline: noisy-OR propagation with
                  registered reliabilities and a frozen decision threshold.
  AssuranceCase   GSN-style change-impact analysis (challenged -> suspect
                  propagation over supported-by / in-context-of links).
  ProvenanceOnly  orion_v2.provenance.ReticulateProvenance revocation
                  descendants (parent-owned reopenable provenance).
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Iterable

from orion_v2.provenance import InheritanceRelation, ProvenanceEdge, ProvenanceNode, ReticulateProvenance

IN = "IN"
OUT = "OUT"
ENABLED_ASSUMPTION = "ENABLED_ASSUMPTION"


# =============================================================================
# JTMS
# =============================================================================

@dataclass
class Justification:
    just_id: int
    informant: str
    consequence: str
    inlist: tuple[str, ...]
    outlist: tuple[str, ...]


@dataclass
class JNode:
    node_id: str
    is_assumption: bool = False
    is_contradiction: bool = False
    label: str = OUT
    support: object = None  # Justification | ENABLED_ASSUMPTION | None
    justs: list[Justification] = field(default_factory=list)
    consequences: list[Justification] = field(default_factory=list)


class JTMS:
    """Justification-based TMS with well-founded support."""

    def __init__(self) -> None:
        self.nodes: dict[str, JNode] = {}
        self.justs: list[Justification] = []
        self.ops = 0
        self._enable_order: dict[str, int] = {}
        self._tick = 0
        self.nogoods: list[frozenset[str]] = []

    # --- construction ---
    def create_node(self, node_id: str, *, assumption: bool = False, contradiction: bool = False) -> JNode:
        if node_id in self.nodes:
            raise ValueError(f"duplicate node {node_id}")
        n = JNode(node_id, assumption, contradiction)
        self.nodes[node_id] = n
        return n

    def justify_node(self, informant: str, consequence: str, inlist: Iterable[str], outlist: Iterable[str] = ()) -> Justification:
        j = Justification(len(self.justs), informant, consequence, tuple(inlist), tuple(outlist))
        self.justs.append(j)
        self.nodes[consequence].justs.append(j)
        for n in (*j.inlist, *j.outlist):
            self.nodes[n].consequences.append(j)
        self._check_justification(j)
        return j

    # --- queries ---
    def is_in(self, node_id: str) -> bool:
        return self.nodes[node_id].label == IN

    def supporting_justification(self, node_id: str):
        return self.nodes[node_id].support

    def assumptions_of(self, node_id: str) -> frozenset[str]:
        """Enabled assumptions in the well-founded support of node."""
        found: set[str] = set(); seen: set[str] = set(); stack = [node_id]
        while stack:
            nid = stack.pop()
            if nid in seen:
                continue
            seen.add(nid)
            n = self.nodes[nid]
            if n.label != IN:
                continue
            if n.support == ENABLED_ASSUMPTION:
                found.add(nid)
            elif isinstance(n.support, Justification):
                stack.extend(n.support.inlist)
        return frozenset(found)

    def explain(self, node_id: str) -> list[str]:
        out: list[str] = []; seen: set[str] = set(); stack = [node_id]
        while stack:
            nid = stack.pop()
            if nid in seen:
                continue
            seen.add(nid); n = self.nodes[nid]
            if n.support == ENABLED_ASSUMPTION:
                out.append(f"{nid} <- enabled assumption")
            elif isinstance(n.support, Justification):
                out.append(f"{nid} <- {n.support.informant}({', '.join(n.support.inlist)}; not {', '.join(n.support.outlist)})")
                stack.extend(n.support.inlist)
            else:
                out.append(f"{nid} is OUT")
        return out

    # --- label maintenance ---
    def _satisfied(self, j: Justification) -> bool:
        self.ops += 1
        return all(self.nodes[n].label == IN for n in j.inlist) and all(self.nodes[n].label == OUT for n in j.outlist)

    def _check_justification(self, j: Justification) -> bool:
        c = self.nodes[j.consequence]
        if c.label == OUT and self._satisfied(j):
            self._make_node_in(j.consequence, j)
            return True
        return False

    def _make_node_in(self, node_id: str, reason) -> None:
        n = self.nodes[node_id]
        n.label = IN; n.support = reason; self.ops += 1
        self._propagate_inness(node_id)

    def _propagate_inness(self, node_id: str) -> None:
        queue = [node_id]
        while queue:
            nid = queue.pop(0)
            for j in list(self.nodes[nid].consequences):
                c = self.nodes[j.consequence]
                if c.label == OUT and self._satisfied(j):
                    c.label = IN; c.support = j; self.ops += 1
                    queue.append(j.consequence)
                    if c.is_contradiction:
                        self._on_contradiction(j.consequence)
        # non-monotonic: nodes that just became IN may have knocked out consequences with outlists
        self._retract_unsupported()

    def _make_node_out(self, node_id: str) -> None:
        n = self.nodes[node_id]
        n.label = OUT; n.support = None; self.ops += 1

    def _propagate_outness(self, node_id: str) -> list[str]:
        """Doyle/BPS out-propagation: everything whose current support rests on
        node_id goes OUT; returns the out-queue for alternative-support search."""
        out_queue = [node_id]; i = 0
        while i < len(out_queue):
            nid = out_queue[i]; i += 1
            for j in self.nodes[nid].consequences:
                c = self.nodes[j.consequence]
                if c.support is j:
                    self._make_node_out(j.consequence)
                    out_queue.append(j.consequence)
        return out_queue

    def _find_alternative_support(self, out_queue: list[str]) -> None:
        changed = True
        while changed:
            changed = False
            for nid in list(out_queue):
                n = self.nodes[nid]
                if n.label == IN:
                    continue
                for j in n.justs:
                    if self._satisfied(j):
                        self._make_node_in(nid, j); changed = True
                        break
            # justifications with outlist members that just went OUT may now fire
            for j in self.justs:
                if self.nodes[j.consequence].label == OUT and j.outlist and self._satisfied(j):
                    self._make_node_in(j.consequence, j); changed = True

    def _retract_unsupported(self) -> None:
        """Well-foundedness repair for non-monotonic justifications: a node
        whose supporting justification is no longer satisfied goes OUT with
        its dependents, then alternative support is sought."""
        changed = True
        while changed:
            changed = False
            for n in list(self.nodes.values()):
                if n.label == IN and isinstance(n.support, Justification) and not self._satisfied(n.support):
                    alt = next((j for j in n.justs if self._satisfied(j)), None)
                    if alt is not None:
                        n.support = alt; self.ops += 1
                        continue
                    self._make_node_out(n.node_id)
                    q = self._propagate_outness(n.node_id)
                    self._find_alternative_support(q)
                    changed = True

    def enable_assumption(self, node_id: str) -> None:
        n = self.nodes[node_id]
        if not n.is_assumption:
            raise ValueError(f"{node_id} is not an assumption")
        if n.label == IN:
            return
        self._tick += 1; self._enable_order[node_id] = self._tick
        n.label = IN; n.support = ENABLED_ASSUMPTION; self.ops += 1
        self._propagate_inness(node_id)

    def retract_assumption(self, node_id: str) -> None:
        n = self.nodes[node_id]
        if n.support != ENABLED_ASSUMPTION:
            return
        self._make_node_out(node_id)
        q = self._propagate_outness(node_id)
        self._find_alternative_support(q)

    def _on_contradiction(self, node_id: str) -> None:
        """Dependency-directed contradiction handling: record the nogood
        (the well-founded assumption set) and retract the culprit = the most
        recently enabled assumption in that set."""
        nogood = self.assumptions_of(node_id)
        if not nogood:
            return
        self.nogoods.append(nogood)
        culprit = max(nogood, key=lambda a: self._enable_order.get(a, -1))
        self.retract_assumption(culprit)


# =============================================================================
# ATMS
# =============================================================================

class ATMS:
    """Assumption-based TMS: labels are sets of minimal consistent environments."""

    def __init__(self) -> None:
        self.assumptions: set[str] = set()
        self.labels: dict[str, frozenset[frozenset[str]]] = {}
        self.justs: list[tuple[tuple[str, ...], str]] = []
        self.nogoods: set[frozenset[str]] = set()
        self.ops = 0

    def create_node(self, node_id: str, *, assumption: bool = False, premise: bool = False) -> None:
        if node_id in self.labels:
            raise ValueError(f"duplicate node {node_id}")
        if assumption:
            self.assumptions.add(node_id); self.labels[node_id] = frozenset({frozenset({node_id})})
        elif premise:
            self.labels[node_id] = frozenset({frozenset()})
        else:
            self.labels[node_id] = frozenset()

    def _inconsistent(self, env: frozenset[str]) -> bool:
        self.ops += 1
        return any(ng <= env for ng in self.nogoods)

    def _minimize(self, envs: Iterable[frozenset[str]]) -> frozenset[frozenset[str]]:
        envs = {e for e in envs if not self._inconsistent(e)}
        keep = set()
        for e in sorted(envs, key=lambda x: (len(x), sorted(x))):
            self.ops += 1
            if not any(k < e for k in keep):
                keep.add(e)
        return frozenset(keep)

    def justify(self, consequent: str, antecedents: Iterable[str]) -> None:
        ants = tuple(antecedents)
        self.justs.append((ants, consequent))
        self._propagate({consequent})

    def _compute_label(self, node: str) -> frozenset[frozenset[str]]:
        if node in self.assumptions:
            return self.labels[node]
        envs: set[frozenset[str]] = set(e for e in self.labels[node] if len(e) == 0)  # premise env survives
        for ants, cons in self.justs:
            if cons != node:
                continue
            if not ants:
                envs.add(frozenset()); continue
            for combo in itertools.product(*(self.labels[a] for a in ants)):
                self.ops += 1
                envs.add(frozenset().union(*combo))
        return self._minimize(envs)

    def _propagate(self, dirty: set[str]) -> None:
        guard = 0
        while dirty:
            guard += 1
            if guard > 10000:
                raise RuntimeError("ATMS propagation did not converge")
            node = sorted(dirty).pop(0); dirty.discard(node)
            new = self._compute_label(node)
            if new != self.labels[node]:
                self.labels[node] = new
                for ants, cons in self.justs:
                    if node in ants:
                        dirty.add(cons)

    def add_nogood(self, env: Iterable[str]) -> None:
        ng = frozenset(env)
        self.nogoods.add(ng)
        for node in list(self.labels):
            self.labels[node] = self._minimize(self.labels[node])

    def label(self, node: str) -> frozenset[frozenset[str]]:
        return self.labels[node]

    def holds_in(self, node: str, environment: Iterable[str]) -> bool:
        env = frozenset(environment); self.ops += 1
        return any(e <= env for e in self.labels[node])


# =============================================================================
# AGM-style belief base: Hansson kernel contraction
# =============================================================================

@dataclass(frozen=True)
class Rule:
    rule_id: str
    body: frozenset[str]
    head: str


class KernelBase:
    """Belief base of atoms and Horn rules with kernel contraction.

    entrenchment(element) -> int; higher = more entrenched. Incision removes,
    from every kernel, its least entrenched element (ties broken by name)."""

    def __init__(self, atoms: Iterable[str], rules: Iterable[Rule], entrenchment: dict[str, int] | None = None) -> None:
        self.atoms: set[str] = set(atoms)
        self.rules: dict[str, Rule] = {r.rule_id: r for r in rules}
        self.entrenchment = dict(entrenchment or {})
        self.ops = 0

    def elements(self) -> frozenset[str]:
        return frozenset(self.atoms) | frozenset(self.rules)

    def _closure(self, atoms: set[str], rules: dict[str, Rule]) -> set[str]:
        derived = set(atoms); changed = True
        while changed:
            changed = False
            for r in rules.values():
                self.ops += 1
                if r.head not in derived and r.body <= derived:
                    derived.add(r.head); changed = True
        return derived

    def derives(self, phi: str) -> bool:
        return phi in self._closure(self.atoms, self.rules)

    def kernels(self, phi: str) -> frozenset[frozenset[str]]:
        """All minimal subsets of the base that derive phi."""
        memo: dict[str, frozenset[frozenset[str]]] = {}

        def rec(target: str, path: frozenset[str]) -> frozenset[frozenset[str]]:
            if target in memo:
                return memo[target]
            out: set[frozenset[str]] = set()
            if target in self.atoms:
                out.add(frozenset({target}))
            for r in self.rules.values():
                if r.head != target or r.rule_id in path:
                    continue
                body_kernels = [rec(b, path | {r.rule_id}) for b in sorted(r.body)]
                if any(not bk for bk in body_kernels):
                    continue
                for combo in itertools.product(*body_kernels):
                    self.ops += 1
                    out.add(frozenset({r.rule_id}).union(*combo))
            minimal = frozenset(k for k in out if not any(o < k for o in out))
            memo[target] = minimal
            return minimal
        return rec(phi, frozenset())

    def _rank(self, element: str) -> tuple[int, str]:
        return (self.entrenchment.get(element, 0), element)

    def contract(self, phi: str) -> frozenset[str]:
        """Kernel contraction by phi; returns the incision (removed elements)."""
        incision: set[str] = set()
        for k in self.kernels(phi):
            if k & incision:
                continue
            incision.add(min(k, key=self._rank))
        for e in incision:
            self.atoms.discard(e); self.rules.pop(e, None)
        return frozenset(incision)

    def expand(self, atom: str) -> None:
        self.atoms.add(atom)

    def revise_against(self, claim: str, negation_atom: str) -> frozenset[str]:
        """Levi identity: contract by claim, then expand by its negation."""
        inc = self.contract(claim)
        self.expand(negation_atom)
        return inc


# =============================================================================
# Bayesian / support-graph baseline: noisy-OR
# =============================================================================

class NoisyOrSupport:
    """belief(c) = nocontra(c) * (1 - prod_F (1 - prod_{a in F} v(a) * prod_{p in prereq(F)} belief(p)))."""

    def __init__(self, families: dict[str, tuple[str, tuple[str, ...], tuple[str, ...]]], claims: Iterable[str], contra_atoms: dict[str, tuple[str, ...]], reliability: dict[str, float], threshold: float = 0.5) -> None:
        # families: family_id -> (claim_id, atoms, prerequisite claims)
        self.families = families
        self.claims = list(claims)
        self.contra_atoms = contra_atoms
        self.reliability = reliability
        self.threshold = threshold
        self.ops = 0

    def beliefs(self, atom_values: dict[str, float]) -> dict[str, float]:
        out: dict[str, float] = {}

        def v(a: str) -> float:
            return atom_values[a] * self.reliability.get(a, 1.0)

        def bel(c: str) -> float:
            if c in out:
                return out[c]
            prod = 1.0
            for fid, (cid, atoms, prereqs) in self.families.items():
                if cid != c:
                    continue
                self.ops += 1
                p = 1.0
                for a in atoms:
                    p *= v(a)
                for q in prereqs:
                    p *= bel(q)
                prod *= (1.0 - p)
            b = 1.0 - prod
            for a in self.contra_atoms.get(c, ()):
                b *= v(a)
            out[c] = b
            return b
        for c in self.claims:
            bel(c)
        return out

    def decide(self, optimistic: dict[str, float], pessimistic: dict[str, float]) -> dict[str, str]:
        d: dict[str, str] = {}
        for c in self.claims:
            if pessimistic[c] >= self.threshold:
                d[c] = "PRESERVED"
            elif optimistic[c] < self.threshold:
                d[c] = "REOPENED"
            else:
                d[c] = "UNRESOLVED"
        return d


# =============================================================================
# Assurance-case change impact (GSN-style)
# =============================================================================

class AssuranceCase:
    """Elements: goals, strategies, solutions, contexts. Links: supported_by
    (child supports parent), in_context_of (context attached to element).
    change_impact(changed) -> (challenged, suspect): challenged = changed
    elements; suspect = every element reachable upward from a challenged
    element through supported_by or in_context_of links."""

    def __init__(self) -> None:
        self.kind: dict[str, str] = {}
        self.parents: dict[str, set[str]] = {}
        self.ops = 0

    def add(self, element_id: str, kind: str) -> None:
        self.kind[element_id] = kind; self.parents.setdefault(element_id, set())

    def supported_by(self, parent: str, child: str) -> None:
        self.parents.setdefault(child, set()).add(parent)

    def in_context_of(self, element: str, context: str) -> None:
        self.parents.setdefault(context, set()).add(element)

    def change_impact(self, changed: Iterable[str]) -> tuple[frozenset[str], frozenset[str]]:
        challenged = frozenset(changed)
        suspect: set[str] = set(); stack = list(challenged)
        while stack:
            e = stack.pop(); self.ops += 1
            for p in self.parents.get(e, ()):
                if p not in suspect:
                    suspect.add(p); stack.append(p)
        return challenged, frozenset(suspect)


# =============================================================================
# Provenance-only invalidation (orion_v2.provenance, parent-owned)
# =============================================================================

class ProvenanceOnly:
    def __init__(self, nodes: Iterable[tuple[str, str]], edges: Iterable[tuple[str, str, str, str]]) -> None:
        self.graph = ReticulateProvenance(
            nodes=tuple(ProvenanceNode(n, k, "v0") for n, k in nodes),
            edges=tuple(ProvenanceEdge(p, c, InheritanceRelation(r), comp) for p, c, r, comp in edges),
        )
        self.ops = 0

    def affected(self, revoked_roots: Iterable[str]) -> frozenset[str]:
        out: set[str] = set()
        for r in revoked_roots:
            self.ops += 1
            out.update(self.graph.affected_by_revocation(r))
        return frozenset(out)


# =============================================================================
# Native known-answer tests (parent fidelity)
# =============================================================================

def fidelity_selftests() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    def rec(parent: str, name: str, passed: bool, detail: str = "") -> None:
        results.append({"parent": parent, "test": name, "passed": bool(passed), "detail": detail})

    # --- JTMS -------------------------------------------------------------
    j = JTMS()
    for n in ("A", "B", "C"):
        j.create_node(n, assumption=True)
    for n in ("x", "y", "z"):
        j.create_node(n)
    j.justify_node("jx", "x", ["A"]); j.justify_node("jy", "y", ["B"]); j.justify_node("jz1", "z", ["x", "y"]); j.justify_node("jz2", "z", ["C"])
    j.enable_assumption("A"); j.enable_assumption("B")
    rec("JTMS", "propagation_chain", j.is_in("x") and j.is_in("y") and j.is_in("z"), j.explain("z")[0])
    rec("JTMS", "well_founded_assumptions_of", j.assumptions_of("z") == frozenset({"A", "B"}), str(sorted(j.assumptions_of("z"))))
    j.retract_assumption("A")
    rec("JTMS", "retraction_propagates_out", (not j.is_in("x")) and (not j.is_in("z")) and j.is_in("y"))
    j.enable_assumption("C")
    rec("JTMS", "alternative_justification_restores", j.is_in("z") and j.assumptions_of("z") == frozenset({"C"}))
    j.enable_assumption("A"); j.retract_assumption("C")
    rec("JTMS", "alternative_support_found_after_retraction", j.is_in("z") and j.assumptions_of("z") == frozenset({"A", "B"}))
    # non-monotonic: p IN iff q OUT
    j2 = JTMS(); j2.create_node("q", assumption=True); j2.create_node("p"); j2.justify_node("default", "p", [], ["q"])
    rec("JTMS", "outlist_default_in_when_q_out", j2.is_in("p"))
    j2.enable_assumption("q")
    rec("JTMS", "outlist_default_out_when_q_in", not j2.is_in("p"))
    j2.retract_assumption("q")
    rec("JTMS", "outlist_default_restored", j2.is_in("p"))
    # well-foundedness: mutual support without premise stays OUT
    j3 = JTMS(); j3.create_node("u"); j3.create_node("v"); j3.justify_node("uv", "u", ["v"]); j3.justify_node("vu", "v", ["u"])
    rec("JTMS", "circular_support_not_in", (not j3.is_in("u")) and (not j3.is_in("v")))
    # dependency-directed contradiction handling
    j4 = JTMS(); j4.create_node("A", assumption=True); j4.create_node("B", assumption=True); j4.create_node("bot", contradiction=True)
    j4.justify_node("clash", "bot", ["A", "B"]); j4.enable_assumption("A"); j4.enable_assumption("B")
    rec("JTMS", "ddb_records_nogood_and_retracts_culprit", j4.nogoods == [frozenset({"A", "B"})] and (not j4.is_in("bot")) and j4.is_in("A") and (not j4.is_in("B")), f"nogoods={[sorted(n) for n in j4.nogoods]}")

    # --- ATMS -------------------------------------------------------------
    a = ATMS()
    for n in ("A", "B", "C"):
        a.create_node(n, assumption=True)
    for n in ("x", "y", "z"):
        a.create_node(n)
    a.justify("x", ["A"]); a.justify("y", ["B"]); a.justify("z", ["x", "y"])
    rec("ATMS", "label_conjunction", a.label("z") == frozenset({frozenset({"A", "B"})}), str([sorted(e) for e in a.label("z")]))
    a.justify("z", ["C"])
    rec("ATMS", "label_disjunction_two_environments", a.label("z") == frozenset({frozenset({"A", "B"}), frozenset({"C"})}))
    a.create_node("w"); a.justify("w", ["z", "A"])
    rec("ATMS", "label_subsumption_minimal", a.label("w") == frozenset({frozenset({"A", "B"}), frozenset({"A", "C"})}), str([sorted(e) for e in a.label("w")]))
    a.add_nogood(["A", "B"])
    rec("ATMS", "nogood_removes_inconsistent_environments", a.label("z") == frozenset({frozenset({"C"})}) and a.label("w") == frozenset({frozenset({"A", "C"})}))
    rec("ATMS", "holds_in_environment_lattice", a.holds_in("z", {"C", "B"}) and (not a.holds_in("z", {"A", "B"})) and (not a.holds_in("z", {"A"})))
    a.create_node("prem", premise=True); a.create_node("t"); a.justify("t", ["prem", "B"])
    rec("ATMS", "premise_empty_environment", a.label("prem") == frozenset({frozenset()}) and a.label("t") == frozenset({frozenset({"B"})}))

    # --- AGM kernel contraction -------------------------------------------
    ent = {"e1": 2, "e2": 2, "e3": 2, "r1": 1, "r2": 1, "r3": 1}
    kb = KernelBase({"e1", "e2", "e3"}, [Rule("r1", frozenset({"e1"}), "c"), Rule("r2", frozenset({"e2"}), "c"), Rule("r3", frozenset({"c", "e3"}), "d")], ent)
    rec("AGM", "closure_derives", kb.derives("c") and kb.derives("d"))
    ks = kb.kernels("c")
    rec("AGM", "kernels_are_minimal_derivations", ks == frozenset({frozenset({"e1", "r1"}), frozenset({"e2", "r2"})}), str([sorted(k) for k in ks]))
    before = kb.elements()
    inc = kb.contract("c")
    rec("AGM", "success", not kb.derives("c"))
    rec("AGM", "inclusion", kb.elements() <= before)
    rec("AGM", "core_retainment", all(any(x in k for k in ks) for x in inc), str(sorted(inc)))
    rec("AGM", "entrenchment_cuts_rules_not_evidence", inc == frozenset({"r1", "r2"}) and {"e1", "e2", "e3"} <= kb.atoms)
    rec("AGM", "downstream_lost_with_contracted_support", not kb.derives("d"))
    kb2 = KernelBase({"e1"}, [Rule("r1", frozenset({"e1"}), "c")], ent); b2 = kb2.elements(); kb2.contract("zzz")
    rec("AGM", "vacuity", kb2.elements() == b2)
    kb3 = KernelBase({"e1"}, [Rule("r1", frozenset({"e1"}), "c")], ent); kb3.contract("e1")
    rec("AGM", "atom_contraction_removes_atom_only", kb3.atoms == set() and "r1" in kb3.rules and not kb3.derives("c"))
    kb4 = KernelBase({"e1"}, [Rule("r1", frozenset({"e1"}), "c")], ent); inc4 = kb4.revise_against("c", "not_c")
    rec("AGM", "levi_revision", (not kb4.derives("c")) and "not_c" in kb4.atoms and inc4 == frozenset({"r1"}))

    # --- Noisy-OR ---------------------------------------------------------
    fams = {"F1": ("c", ("a1", "a2"), ()), "F2": ("c", ("a3",), ()), "G1": ("d", (), ("c",))}
    rel = {"a1": 0.9, "a2": 0.9, "a3": 0.9}
    no = NoisyOrSupport(fams, ["c", "d"], {}, rel, 0.5)
    b = no.beliefs({"a1": 1.0, "a2": 1.0, "a3": 1.0})
    rec("NOISY_OR", "noisy_or_arithmetic", abs(b["c"] - (1 - (1 - 0.81) * (1 - 0.9))) < 1e-12 and abs(b["d"] - b["c"]) < 1e-12, f"bel(c)={b['c']:.4f}")
    b0 = no.beliefs({"a1": 0.0, "a2": 1.0, "a3": 0.0})
    rec("NOISY_OR", "all_support_lost_below_threshold", b0["c"] == 0.0 and no.decide(b0, b0)["c"] == "REOPENED")
    opt = no.beliefs({"a1": 1.0, "a2": 1.0, "a3": 0.0}); pes = no.beliefs({"a1": 0.0, "a2": 1.0, "a3": 0.0})
    rec("NOISY_OR", "envelope_unresolved", no.decide(opt, pes)["c"] == "UNRESOLVED")
    big = NoisyOrSupport({"F": ("c", tuple(f"a{i}" for i in range(7)), ())}, ["c"], {}, {f"a{i}": 0.9 for i in range(7)}, 0.5)
    bb = big.beliefs({f"a{i}": 1.0 for i in range(7)})
    rec("NOISY_OR", "family_size_boundary_documented", bb["c"] < 0.5, f"7-item family at r=0.9 -> {bb['c']:.4f} < 0.5 (generator caps families at <=4 items)")

    # --- Assurance case ---------------------------------------------------
    ac = AssuranceCase()
    for e, k in (("G1", "goal"), ("G2", "goal"), ("S1", "strategy"), ("S2", "strategy"), ("Sn1", "solution"), ("Sn2", "solution"), ("Ctx", "context")):
        ac.add(e, k)
    ac.supported_by("G1", "S1"); ac.supported_by("S1", "Sn1"); ac.supported_by("G2", "S2"); ac.supported_by("S2", "Sn2"); ac.in_context_of("S2", "Ctx")
    ch, sus = ac.change_impact(["Sn1"])
    rec("ASSURANCE", "solution_change_marks_own_argument_suspect", sus == frozenset({"S1", "G1"}), str(sorted(sus)))
    ch, sus = ac.change_impact(["Ctx"])
    rec("ASSURANCE", "context_change_marks_contextualised_argument_suspect", sus == frozenset({"S2", "G2"}), str(sorted(sus)))

    # --- Provenance-only --------------------------------------------------
    po = ProvenanceOnly([("src", "source"), ("cal", "calibration"), ("e1", "evidence"), ("e2", "evidence"), ("c", "commitment")], [("src", "e1", "DERIVES", "source"), ("cal", "e2", "CALIBRATES_FROM", "calibration"), ("e1", "c", "DERIVES", "support"), ("e2", "c", "DERIVES", "support")])
    rec("PROVENANCE_ONLY", "revocation_descendants", po.affected(["src"]) == frozenset({"src", "e1", "c"}) and po.affected(["cal"]) == frozenset({"cal", "e2", "c"}))
    return results
