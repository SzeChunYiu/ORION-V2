"""FG series arms: M, the strongest faithful parent federation, six single
parents, and the controls/ablations.

Every arm receives exactly the same registered information (`fg_model.arm_view`,
which never carries the stratum or the planted decoy labels) and returns one
terminal of the §L5 search order plus a witness.  No arm imports `fg_oracle`.

`M_FG_SEARCH_ORDER` is the ORION reference mechanism: it detects the deficit
with `orion_v2.formalism_genesis.representation_collisions`, finds minimal
distinctions with `minimal_discriminating_feature_sets`, walks the §L5 ladder,
and submits any candidate new primitive to the fail-closed admission gate
`assess_formalism_candidate`.  It is not the oracle: the oracle is an
independent exhaustive tier search, and M can be blocked by its own admission
gate where the oracle cannot.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Mapping, Sequence

from orion_v2.formalism_genesis import (
    DistinctionCase,
    FormalismCandidate,
    FormalismGenesisEvidence,
    FormalismGenesisStatus,
    assess_formalism_candidate,
    minimal_discriminating_feature_sets,
    representation_collisions,
)

from fg_model import (
    ADD_ONE_OBSERVATION,
    LOCAL_PATCH,
    NEW_PRIMITIVE,
    NO_CHANGE,
    PARENT_FORMALISM_SUFFICIENT,
    REPRESENTATION_CHANGE,
    REPAIR_TIERS,
    Instance,
    derived_term_space,
    evaluate_term,
    instance_from_json,
    relational_term_space,
    signatures,
    term_kind,
)
import fg_parents as P

CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ArmDecision:
    terminal: str
    witness: tuple[str, ...] = ()
    admission_status: str = ""
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "terminal": self.terminal,
            "witness": list(self.witness),
            "admission_status": self.admission_status,
            "notes": list(self.notes),
        }


def instance_from_view(view: Mapping[str, Any]) -> Instance:
    payload = dict(view)
    payload["stratum"] = "HIDDEN"
    payload["planted_decoys"] = []
    payload.pop("repair_tiers", None)
    return instance_from_json(payload)


# ---------------------------------------------------------------------------
# shared arm-side candidate spaces (registered information only)
# ---------------------------------------------------------------------------


@dataclass
class Candidates:
    instance: Instance
    active: tuple[str, ...]
    decisions: dict[str, str] = field(default_factory=dict)
    columns: dict[str, dict[str, str]] = field(default_factory=dict)

    @classmethod
    def build(cls, instance: Instance) -> "Candidates":
        active = tuple(instance.active_formalism.term_ids)
        decisions = {c.case_id: c.decision_id for c in instance.cases}
        terms = set(active)
        terms.update(instance.all_atoms())
        terms.update(derived_term_space(instance))
        terms.update(relational_term_space(instance))
        for parent in instance.parent_formalisms:
            terms.update(parent.term_ids)
        columns = {term: evaluate_term(term, instance) for term in sorted(terms)}
        return cls(instance, active, decisions, columns)

    def collisions(self, term_ids: Sequence[str]) -> list[tuple[str, str]]:
        ids = sorted(self.decisions)
        out = []
        for left, right in combinations(ids, 2):
            if self.decisions[left] == self.decisions[right]:
                continue
            if all(self.columns[t][left] == self.columns[t][right] for t in term_ids):
                out.append((left, right))
        return out

    def separates_all(self, term: str, pairs: Sequence[tuple[str, str]]) -> bool:
        column = self.columns[term]
        return all(column[a] != column[b] for a, b in pairs)

    def residual(self, term_ids: Sequence[str]) -> int:
        return len(self.collisions(term_ids))

    def new_atoms(self) -> list[str]:
        return [t for t in self.instance.all_atoms() if t not in set(self.active)]

    def derived(self) -> list[str]:
        return list(derived_term_space(self.instance))

    def relational(self) -> list[str]:
        return list(relational_term_space(self.instance))

    def patch_cover(self, pairs: Sequence[tuple[str, str]], budget: int) -> tuple[str, ...] | None:
        vertices = sorted({v for pair in pairs for v in pair})
        for size in range(1, budget + 1):
            for subset in combinations(vertices, size):
                chosen = set(subset)
                if all(a in chosen or b in chosen for a, b in pairs):
                    return subset
        return None

    def representation_witness(self, pairs: Sequence[tuple[str, str]]) -> tuple[str, ...] | None:
        singles = [t for t in self.derived() if self.separates_all(t, pairs)]
        if singles:
            return (sorted(singles)[0],)
        terms = sorted(self.derived())
        for left, right in combinations(terms, 2):
            cl, cr = self.columns[left], self.columns[right]
            if all(cl[a] != cl[b] or cr[a] != cr[b] for a, b in pairs):
                return (left, right)
        return None

    def relational_witness(self, pairs: Sequence[tuple[str, str]]) -> str | None:
        hits = [t for t in self.relational() if self.separates_all(t, pairs)]
        return sorted(hits)[0] if hits else None

    def sufficient_parents(self) -> list[str]:
        return [
            parent.formalism_id
            for parent in self.instance.parent_formalisms
            if not self.collisions(parent.term_ids)
        ]


# ---------------------------------------------------------------------------
# M -- the ORION reference mechanism
# ---------------------------------------------------------------------------


def _distinction_cases(cand: Candidates) -> tuple[DistinctionCase, ...]:
    features = sorted(set(cand.columns) - set(cand.active))
    out = []
    for case in cand.instance.cases:
        out.append(
            DistinctionCase(
                case_id=case.case_id,
                current_signature=tuple(cand.columns[t][case.case_id] for t in cand.active),
                required_decision_id=case.decision_id,
                candidate_feature_values=tuple(
                    (feature, cand.columns[feature][case.case_id]) for feature in features
                ),
            )
        )
    return tuple(out)


def _admission_receipt(cand: Candidates, primitive: str, cheaper_available: bool) -> str:
    """Fail-closed admission of a candidate new primitive (issue #50 §L5 binding)."""

    candidate = FormalismCandidate(
        formalism_id=f"FG70_CANDIDATE::{primitive}",
        parent_formalism_ids=tuple(p.formalism_id for p in cand.instance.parent_formalisms),
        primitive_ids=(primitive,),
        relation_ids=tuple(r.rel_id for r in cand.instance.relations),
        operation_ids=("COMPONENT_OF", "REACHABLE_FROM"),
        axiom_ids=("REFLEXIVE", "SYMMETRIC", "TRANSITIVE_CLOSURE"),
        semantic_model_ids=("FINITE_RELATIONAL_STRUCTURE_OVER_REGISTERED_CASES",),
        recovery_map_ids=("FORGET_PRIMITIVE_RECOVERS_ACTIVE_FORMALISM",),
        proof_or_derivation_rule_ids=("UNION_FIND_CLOSURE",),
        intended_deficit_ids=("C_F_NONEMPTY",),
        prospective_consequence_ids=("SEPARATES_EVERY_REGISTERED_COLLISION",),
    )
    evidence = FormalismGenesisEvidence(
        registered_deficit_present=True,
        strongest_parent_executed=True,
        strongest_parent_sufficient=False,
        expressibility_or_collision_reduction_pass=True,
        semantic_model_witness_pass=True,
        consistency_or_model_check_pass=True,
        parent_recovery_pass=True,
        old_valid_case_retention_pass=True,
        prospective_new_consequence_pass=True,
        hidden_problem_success_pass=True,
        # the minimality / simpler-patch control: a cheaper adequate repair
        # existing is exactly the condition that must block invention
        minimality_or_simpler_patch_check_pass=not cheaper_available,
        resource_accounted=True,
    )
    return assess_formalism_candidate(candidate, evidence).status.value


def _m_route(cand: Candidates, *, skip: frozenset[str] = frozenset(), admission: bool = True,
             reverse: bool = False, deficit_check: bool = True) -> ArmDecision:
    """`skip` may name any tier, including NEW_PRIMITIVE, so every stratum has a
    like-for-like tier-omission ablation."""
    collisions = tuple(
        (c.left_case_id, c.right_case_id)
        for c in representation_collisions(_distinction_cases(cand))
    )
    if not collisions and deficit_check:
        return ArmDecision(NO_CHANGE, (), "", ("representation_collisions returned the empty set",))

    minimal_sets = minimal_discriminating_feature_sets(_distinction_cases(cand))
    minimal_features = {f for solution in minimal_sets for f in solution}

    feasible: list[tuple[str, tuple[str, ...]]] = []

    if PARENT_FORMALISM_SUFFICIENT not in skip:
        hits = cand.sufficient_parents()
        if hits:
            feasible.append((PARENT_FORMALISM_SUFFICIENT, (f"parent={sorted(hits)[0]}",)))

    if ADD_ONE_OBSERVATION not in skip:
        atoms = [
            t for t in cand.new_atoms()
            if t in minimal_features and cand.separates_all(t, collisions)
        ] or [t for t in cand.new_atoms() if cand.separates_all(t, collisions)]
        if atoms:
            feasible.append((ADD_ONE_OBSERVATION, (f"observation={sorted(atoms)[0]}",)))

    if LOCAL_PATCH not in skip:
        cover = cand.patch_cover(collisions, cand.instance.patch_budget)
        if cover is not None:
            feasible.append((LOCAL_PATCH, (f"patch={'+'.join(sorted(cover))}",)))

    if REPRESENTATION_CHANGE not in skip:
        witness = cand.representation_witness(collisions)
        if witness is not None:
            feasible.append(
                (REPRESENTATION_CHANGE, tuple(f"representation={t}" for t in witness))
            )

    primitive = None if NEW_PRIMITIVE in skip else cand.relational_witness(collisions)
    admission_status = ""
    if primitive is not None:
        cheaper = bool(feasible)
        admission_status = _admission_receipt(cand, primitive, cheaper) if admission else "SKIPPED"
        admitted = (not admission) or admission_status in {
            FormalismGenesisStatus.PROTECTED_FORMALISM_RESIDUAL.value,
            FormalismGenesisStatus.READY_FOR_PROTECTED_EVALUATION.value,
            FormalismGenesisStatus.INDEPENDENTLY_CHECKED_FORMALISM_RESIDUAL.value,
        }
        if admitted:
            feasible.append((NEW_PRIMITIVE, (f"primitive={primitive}",)))

    if not feasible:
        return ArmDecision(CANNOT_CHECK, (), admission_status,
                           ("no registered repair resolved the deficit",))
    order = {name: index for index, name in enumerate(REPAIR_TIERS)}
    feasible.sort(key=lambda item: order[item[0]], reverse=reverse)
    terminal, witness = feasible[0]
    return ArmDecision(terminal, witness, admission_status)


# ---------------------------------------------------------------------------
# single parents (native semantics; each may only express its own repertoire)
# ---------------------------------------------------------------------------


def _lgg_deficit(cand: Candidates) -> bool:
    """LGG's native deficit test: some class generalization subsumes a foreign case."""

    classes: dict[str, list[tuple[str, ...]]] = {}
    for case in cand.instance.cases:
        row = tuple(cand.columns[t][case.case_id] for t in cand.active)
        classes.setdefault(case.decision_id, []).append(row)
    patterns = {label: P.lgg_set(rows) for label, rows in classes.items()}
    for label, pattern in patterns.items():
        for other, rows in classes.items():
            if other == label:
                continue
            if any(P.subsumes(pattern, row) for row in rows):
                return True
    return False


def arm_lgg(cand: Candidates) -> ArmDecision:
    if not _lgg_deficit(cand):
        return ArmDecision(NO_CHANGE, (), "", ("no class generalization subsumes a foreign case",))
    collisions = cand.collisions(cand.active)
    if not collisions:
        # LGG detects a deficit its repertoire cannot repair by extension
        return ArmDecision(CANNOT_CHECK, (), "",
                           ("class generalizations cross-subsume but no case pair collides",))
    atoms = [t for t in cand.new_atoms() if cand.separates_all(t, collisions)]
    if atoms:
        return ArmDecision(ADD_ONE_OBSERVATION, (f"observation={sorted(atoms)[0]}",))
    witness = cand.representation_witness(collisions)
    if witness is not None:
        return ArmDecision(REPRESENTATION_CHANGE, tuple(f"representation={t}" for t in witness))
    primitive = cand.relational_witness(collisions)
    if primitive is not None:
        return ArmDecision(NEW_PRIMITIVE, (f"primitive={primitive}",))
    return ArmDecision(CANNOT_CHECK, (), "", ("no argument-position extension separates the classes",))


def _context_of(cand: Candidates, term_ids: Sequence[str]) -> P.FormalContext:
    objects = tuple(sorted(cand.decisions))
    attributes = tuple(
        f"{term}={value}"
        for term in term_ids
        for value in sorted({cand.columns[term][o] for o in objects})
    )
    incidence = {
        (obj, f"{term}={cand.columns[term][obj]}") for obj in objects for term in term_ids
    }
    return P.FormalContext(objects, attributes, frozenset(incidence))


def _fca_intent_collisions(cand: Candidates, term_ids: Sequence[str]) -> list[tuple[str, str]]:
    context = _context_of(cand, term_ids)
    out = []
    for left, right in combinations(context.objects, 2):
        if cand.decisions[left] == cand.decisions[right]:
            continue
        if context.object_intent(left) == context.object_intent(right):
            out.append((left, right))
    return out


def arm_fca(cand: Candidates) -> ArmDecision:
    collisions = _fca_intent_collisions(cand, cand.active)
    if not collisions:
        return ArmDecision(NO_CHANGE, (), "", ("every decision class is a union of extents",))
    hits = [
        parent.formalism_id
        for parent in cand.instance.parent_formalisms
        if not _fca_intent_collisions(cand, parent.term_ids)
    ]
    if hits:
        return ArmDecision(PARENT_FORMALISM_SUFFICIENT, (f"parent={sorted(hits)[0]}",))
    atoms = [t for t in cand.new_atoms() if cand.separates_all(t, collisions)]
    if atoms:
        return ArmDecision(ADD_ONE_OBSERVATION, (f"observation={sorted(atoms)[0]}",))
    witness = cand.representation_witness(collisions)
    if witness is not None:
        return ArmDecision(REPRESENTATION_CHANGE, tuple(f"representation={t}" for t in witness))
    primitive = cand.relational_witness(collisions)
    if primitive is not None:
        return ArmDecision(NEW_PRIMITIVE, (f"primitive={primitive}",))
    return ArmDecision(CANNOT_CHECK, (), "", ("no attribute set separates the decision classes",))


def arm_mdl(cand: Candidates) -> ArmDecision:
    """Native two-part MDL argmin over every registered repair, own code."""

    instance = cand.instance
    collisions = cand.collisions(cand.active)
    n_obs = len(instance.observables)
    common = dict(
        n_parents=max(len(instance.parent_formalisms), 1),
        n_atoms=max(len(cand.new_atoms()), 1),
        n_cases=len(instance.cases),
        n_decisions=len({c.decision_id for c in instance.cases}),
        n_derived_terms=max(len(cand.derived()), 1),
        n_observables=n_obs,
        n_relational_ops=2,
    )
    options: list[tuple[float, str, tuple[str, ...]]] = []

    options.append(
        (
            P.mdl_total_bits(P.mdl_model_bits("NO_CHANGE", patch_size=0, n_representation_terms=0, **common), len(collisions)),
            NO_CHANGE,
            (),
        )
    )
    for parent in instance.parent_formalisms:
        options.append(
            (
                P.mdl_total_bits(
                    P.mdl_model_bits("PARENT_FORMALISM_SUFFICIENT", patch_size=0,
                                     n_representation_terms=0, **common),
                    cand.residual(parent.term_ids),
                ),
                PARENT_FORMALISM_SUFFICIENT,
                (f"parent={parent.formalism_id}",),
            )
        )
    for term in cand.new_atoms():
        options.append(
            (
                P.mdl_total_bits(
                    P.mdl_model_bits("ADD_ONE_OBSERVATION", patch_size=0,
                                     n_representation_terms=0, **common),
                    cand.residual(tuple(cand.active) + (term,)),
                ),
                ADD_ONE_OBSERVATION,
                (f"observation={term}",),
            )
        )
    if collisions:
        cover = cand.patch_cover(collisions, instance.patch_budget)
        if cover is not None:
            options.append(
                (
                    P.mdl_total_bits(
                        P.mdl_model_bits("LOCAL_PATCH", patch_size=len(cover),
                                         n_representation_terms=0, **common),
                        0,
                    ),
                    LOCAL_PATCH,
                    (f"patch={'+'.join(sorted(cover))}",),
                )
            )
        witness = cand.representation_witness(collisions)
        if witness is not None:
            options.append(
                (
                    P.mdl_total_bits(
                        P.mdl_model_bits("REPRESENTATION_CHANGE", patch_size=0,
                                         n_representation_terms=len(witness), **common),
                        0,
                    ),
                    REPRESENTATION_CHANGE,
                    tuple(f"representation={t}" for t in witness),
                )
            )
        primitive = cand.relational_witness(collisions)
        if primitive is not None:
            options.append(
                (
                    P.mdl_total_bits(
                        P.mdl_model_bits("NEW_PRIMITIVE", patch_size=0,
                                         n_representation_terms=0, **common),
                        0,
                    ),
                    NEW_PRIMITIVE,
                    (f"primitive={primitive}",),
                )
            )
    options.sort(key=lambda item: (item[0], item[1], item[2]))
    bits, terminal, witness = options[0]
    return ArmDecision(terminal, witness, "", (f"mdl_bits={bits:.3f}",))


def arm_model_search(cand: Candidates) -> ArmDecision:
    """Countermodel search with no cost model: canonical (alphabetical) scan."""

    rows = [
        {**{t: cand.columns[t][case.case_id] for t in cand.columns}, "J": case.decision_id}
        for case in cand.instance.cases
    ]
    if P.countermodel_of_functional_dependency(rows, cand.active, "J") is None:
        return ArmDecision(NO_CHANGE, (), "", ("no countermodel for the active determination",))
    collisions = cand.collisions(cand.active)
    for terminal in sorted(REPAIR_TIERS):
        if terminal == NO_CHANGE:
            continue
        if terminal == ADD_ONE_OBSERVATION:
            hits = [
                t for t in cand.new_atoms()
                if P.countermodel_of_functional_dependency(rows, tuple(cand.active) + (t,), "J") is None
            ]
            if hits:
                return ArmDecision(terminal, (f"observation={sorted(hits)[0]}",))
        elif terminal == LOCAL_PATCH:
            cover = cand.patch_cover(collisions, cand.instance.patch_budget)
            if cover is not None:
                return ArmDecision(terminal, (f"patch={'+'.join(sorted(cover))}",))
        elif terminal == NEW_PRIMITIVE:
            primitive = cand.relational_witness(collisions)
            if primitive is not None:
                return ArmDecision(terminal, (f"primitive={primitive}",))
        elif terminal == PARENT_FORMALISM_SUFFICIENT:
            hits = [
                p.formalism_id for p in cand.instance.parent_formalisms
                if P.countermodel_of_functional_dependency(rows, p.term_ids, "J") is None
            ]
            if hits:
                return ArmDecision(terminal, (f"parent={sorted(hits)[0]}",))
        elif terminal == REPRESENTATION_CHANGE:
            witness = cand.representation_witness(collisions)
            if witness is not None:
                return ArmDecision(terminal, tuple(f"representation={t}" for t in witness))
    return ArmDecision(CANNOT_CHECK, (), "", ("no hypothesis survived countermodel search",))


def arm_conservative(cand: Candidates) -> ArmDecision:
    """Conservative-extension checking is an admission filter, not a selector."""

    collisions = cand.collisions(cand.active)
    if not collisions:
        return ArmDecision(NO_CHANGE, (), "", ("nothing to extend",))
    old_language = frozenset(f"sep({a},{b})" for a, b in combinations(sorted(cand.decisions), 2))
    old_consequences = frozenset(
        f"sep({a},{b})"
        for a, b in combinations(sorted(cand.decisions), 2)
        if any(cand.columns[t][a] != cand.columns[t][b] for t in cand.active)
    )
    source = P.FiniteConsequenceTheory("F_ACTIVE", old_language, old_consequences)
    admissible: list[str] = []
    for terminal, terms in _repair_signatures(cand, collisions):
        extension_language = old_language | {f"tier({terminal})"}
        extension_consequences = frozenset(
            f"sep({a},{b})"
            for a, b in combinations(sorted(cand.decisions), 2)
            if any(cand.columns[t][a] != cand.columns[t][b] for t in terms)
        ) | {f"tier({terminal})"}
        status = P.assess_conservative_extension(
            source,
            P.FiniteConsequenceTheory("F_EXT", extension_language, extension_consequences),
        ).status
        if status is not P.ConservativeExtensionStatus.LOST_OLD_LANGUAGE_CONSEQUENCE:
            admissible.append(terminal)
    unique = sorted(set(admissible))
    if len(unique) == 1:
        return ArmDecision(unique[0], (), "", ("single admissible extension",))
    return ArmDecision(CANNOT_CHECK, (), "",
                       (f"{len(unique)} admissible extensions; the native check does not select",))


def _repair_signatures(cand: Candidates, collisions) -> list[tuple[str, tuple[str, ...]]]:
    out: list[tuple[str, tuple[str, ...]]] = []
    for parent in cand.instance.parent_formalisms:
        if not cand.collisions(parent.term_ids):
            out.append((PARENT_FORMALISM_SUFFICIENT, tuple(parent.term_ids)))
    for term in cand.new_atoms():
        if cand.separates_all(term, collisions):
            out.append((ADD_ONE_OBSERVATION, tuple(cand.active) + (term,)))
    witness = cand.representation_witness(collisions)
    if witness is not None:
        out.append((REPRESENTATION_CHANGE, tuple(cand.active) + tuple(witness)))
    primitive = cand.relational_witness(collisions)
    if primitive is not None:
        out.append((NEW_PRIMITIVE, tuple(cand.active) + (primitive,)))
    return out


def arm_theory_revision(cand: Candidates) -> ArmDecision:
    collisions = cand.collisions(cand.active)
    if not collisions:
        return ArmDecision(NO_CHANGE, (), "", ("base is consistent with every registered decision",))
    kernels = [frozenset(pair) for pair in collisions]
    contracted = P.kernel_contraction(frozenset(cand.decisions), kernels)
    excepted = sorted(set(cand.decisions) - set(contracted))
    if len(excepted) <= cand.instance.patch_budget:
        return ArmDecision(LOCAL_PATCH, (f"patch={'+'.join(excepted)}",))
    cover = cand.patch_cover(collisions, cand.instance.patch_budget)
    if cover is not None:
        return ArmDecision(LOCAL_PATCH, (f"patch={'+'.join(sorted(cover))}",))
    return ArmDecision(CANNOT_CHECK, (), "",
                       (f"minimal contraction excepts {len(excepted)} cases > budget "
                        f"{cand.instance.patch_budget}; base revision cannot extend the language",))


# ---------------------------------------------------------------------------
# B -- strongest faithful parent federation
# ---------------------------------------------------------------------------


def arm_federation(cand: Candidates) -> ArmDecision:
    """FCA deficit detection + parent evaluation, LGG extension search,
    AGM contraction for the patch tier, conservative-extension admission,
    MDL within-tier minimality, all walked in the *registered* (public) order."""

    collisions = _fca_intent_collisions(cand, cand.active)
    verify = P.countermodel_of_functional_dependency(
        [{**{t: cand.columns[t][c.case_id] for t in cand.columns}, "J": c.decision_id}
         for c in cand.instance.cases],
        cand.active,
        "J",
    )
    if not collisions:
        if verify is not None:  # modules disagree: refuse rather than guess
            return ArmDecision(CANNOT_CHECK, (), "", ("FCA and model search disagree",))
        return ArmDecision(NO_CHANGE)

    hits = [
        p.formalism_id for p in cand.instance.parent_formalisms
        if not _fca_intent_collisions(cand, p.term_ids)
    ]
    if hits:
        return ArmDecision(PARENT_FORMALISM_SUFFICIENT, (f"parent={sorted(hits)[0]}",))

    atoms = [t for t in cand.new_atoms() if cand.separates_all(t, collisions)]
    if atoms:
        return ArmDecision(ADD_ONE_OBSERVATION, (f"observation={sorted(atoms)[0]}",))

    kernels = [frozenset(pair) for pair in collisions]
    contracted = P.kernel_contraction(frozenset(cand.decisions), kernels)
    excepted = sorted(set(cand.decisions) - set(contracted))
    cover = cand.patch_cover(collisions, cand.instance.patch_budget)
    if cover is not None or len(excepted) <= cand.instance.patch_budget:
        chosen = cover if cover is not None else tuple(excepted)
        return ArmDecision(LOCAL_PATCH, (f"patch={'+'.join(sorted(chosen))}",))

    witness = cand.representation_witness(collisions)
    if witness is not None:
        return ArmDecision(REPRESENTATION_CHANGE, tuple(f"representation={t}" for t in witness))

    primitive = cand.relational_witness(collisions)
    if primitive is not None:
        return ArmDecision(NEW_PRIMITIVE, (f"primitive={primitive}",))
    return ArmDecision(CANNOT_CHECK, (), "", ("federation exhausted every registered repair",))


# ---------------------------------------------------------------------------
# controls and ablations
# ---------------------------------------------------------------------------


def arm_always_invent(cand: Candidates) -> ArmDecision:
    collisions = cand.collisions(cand.active)
    if not collisions:
        return ArmDecision(NO_CHANGE)
    primitive = cand.relational_witness(collisions)
    return ArmDecision(NEW_PRIMITIVE, (f"primitive={primitive}",) if primitive else ())


def arm_never_invent(cand: Candidates) -> ArmDecision:
    decision = _m_route(cand, skip=frozenset())
    if decision.terminal != NEW_PRIMITIVE:
        return decision
    fallback = _m_route(cand, skip=frozenset({NEW_PRIMITIVE}), admission=False)
    if fallback.terminal in {NEW_PRIMITIVE, CANNOT_CHECK}:
        return ArmDecision(LOCAL_PATCH, (), "", ("never-invent floor",))
    return fallback


def arm_random(cand: Candidates, seed: int) -> ArmDecision:
    rng = random.Random(f"{seed}|{cand.instance.instance_id}")
    return ArmDecision(rng.choice(REPAIR_TIERS), (), "", ("random control",))


ARM_SPECS: tuple[str, ...] = (
    "P1_LGG_ANTIUNIFICATION",
    "P2_FCA_GALOIS_CLOSURE",
    "P3_MDL_ABSTRACTION_SEARCH",
    "P4_MODEL_COUNTERMODEL_SEARCH",
    "P5_CONSERVATIVE_EXTENSION_CHECK",
    "P6_THEORY_REVISION_BASELINE",
    "B_STRONGEST_FAITHFUL_PARENT_FEDERATION",
    "M_FG_SEARCH_ORDER",
    "M_MINUS_PARENT_SEARCH",
    "M_MINUS_DATA_TIER",
    "M_MINUS_PATCH_TIER",
    "M_MINUS_REPRESENTATION_TIER",
    "M_MINUS_INVENTION_TIER",
    "M_MINUS_DEFICIT_CHECK",
    "M_MINUS_ADMISSION_GATE",
    "M_MINUS_COST_ORDER",
    "M_MINUS_ORDER_AND_GATE",
    "M_EAGER_INVENT",
    "C_ALWAYS_INVENT",
    "C_NEVER_INVENT",
    "C_NEVER_CHANGE",
    "C_RANDOM_TERMINAL",
)
M_ARM = "M_FG_SEARCH_ORDER"
B_ARM = "B_STRONGEST_FAITHFUL_PARENT_FEDERATION"
PARENT_ARMS = ARM_SPECS[:6]
#: Every stratum gets an ablation that omits a mechanism the stratum *needs*.
#: The fail-closed admission gate can only ever block, so removing it cannot
#: degrade the stratum where invention is correct; the gate's mechanism is
#: measured on the anti-invention axis by the 2x2 factorial in G3 instead, and
#: NEW_PRIMITIVE is attributed to omitting the escalation tier itself.
ABLATION_FOR_STRATUM = {
    NO_CHANGE: "M_MINUS_DEFICIT_CHECK",
    PARENT_FORMALISM_SUFFICIENT: "M_MINUS_PARENT_SEARCH",
    ADD_ONE_OBSERVATION: "M_MINUS_DATA_TIER",
    LOCAL_PATCH: "M_MINUS_PATCH_TIER",
    REPRESENTATION_CHANGE: "M_MINUS_REPRESENTATION_TIER",
    NEW_PRIMITIVE: "M_MINUS_INVENTION_TIER",
}
DEFAULT_ABLATION = "M_MINUS_COST_ORDER"
RANDOM_CONTROL_SEED = 20260902


def run_arm(name: str, view: Mapping[str, Any]) -> ArmDecision:
    cand = Candidates.build(instance_from_view(view))
    if name == "P1_LGG_ANTIUNIFICATION":
        return arm_lgg(cand)
    if name == "P2_FCA_GALOIS_CLOSURE":
        return arm_fca(cand)
    if name == "P3_MDL_ABSTRACTION_SEARCH":
        return arm_mdl(cand)
    if name == "P4_MODEL_COUNTERMODEL_SEARCH":
        return arm_model_search(cand)
    if name == "P5_CONSERVATIVE_EXTENSION_CHECK":
        return arm_conservative(cand)
    if name == "P6_THEORY_REVISION_BASELINE":
        return arm_theory_revision(cand)
    if name == B_ARM:
        return arm_federation(cand)
    if name == M_ARM:
        return _m_route(cand)
    if name == "M_MINUS_PARENT_SEARCH":
        return _m_route(cand, skip=frozenset({PARENT_FORMALISM_SUFFICIENT}))
    if name == "M_MINUS_DATA_TIER":
        return _m_route(cand, skip=frozenset({ADD_ONE_OBSERVATION}))
    if name == "M_MINUS_PATCH_TIER":
        return _m_route(cand, skip=frozenset({LOCAL_PATCH}))
    if name == "M_MINUS_REPRESENTATION_TIER":
        return _m_route(cand, skip=frozenset({REPRESENTATION_CHANGE}))
    if name == "M_MINUS_INVENTION_TIER":
        return _m_route(cand, skip=frozenset({NEW_PRIMITIVE}))
    if name == "M_MINUS_DEFICIT_CHECK":
        return _m_route(cand, deficit_check=False)
    if name == "M_MINUS_ADMISSION_GATE":
        return _m_route(cand, admission=False)
    if name == "M_MINUS_COST_ORDER":
        return _m_route(cand, reverse=True)
    if name == "M_MINUS_ORDER_AND_GATE":
        return _m_route(cand, reverse=True, admission=False)
    if name == "M_EAGER_INVENT":
        return _m_route(
            cand,
            skip=frozenset({PARENT_FORMALISM_SUFFICIENT, ADD_ONE_OBSERVATION, LOCAL_PATCH}),
            admission=False,
        )
    if name == "C_ALWAYS_INVENT":
        return arm_always_invent(cand)
    if name == "C_NEVER_INVENT":
        return arm_never_invent(cand)
    if name == "C_NEVER_CHANGE":
        return ArmDecision(NO_CHANGE, (), "", ("never-change control: the mirror of C_ALWAYS_INVENT",))
    if name == "C_RANDOM_TERMINAL":
        return arm_random(cand, RANDOM_CONTROL_SEED)
    raise ValueError(f"unknown arm {name!r}")
