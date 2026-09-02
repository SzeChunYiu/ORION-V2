# Machine Epistemics — Parent Recovery: Wang/Buehler and El Agente Gráfico V1

**State date:** 2026-09-01  
**Status:** hostile parent-recovery artifact; no novelty/field authority  
**ORION-V2 base:** `4165dd2d3c621d9f60e0ff492560baf3afbf7c5f`

## 0. Purpose

Two 2026 systems collide directly with the Machine Epistemics formal surface:

1. Fiona Y. Wang & Markus J. Buehler, **Self-Revising Discovery Systems for Science: A Categorical Framework for Agentic Artificial Intelligence**, arXiv:2606.01444v1, submitted 2026-05-31.
2. Jiaru Bai et al., **El Agente Gráfico**, arXiv:2602.17902. The February version develops structured/type-safe execution graphs; the August-revised public abstract sharpens the language to validation, transfer and recording of scientific state and admissible scientific-state transitions.

This document gives those parents the strongest reasonable reading before any ORION residual is claimed.

Disposition labels:

- `PARENT_RECOVERED` — ORION must not claim the concept as a Machine Epistemics novelty.
- `PARTIAL_OVERLAP` — related object exists, but scope/semantics differ materially.
- `RESIDUAL_CANDIDATE_ONLY` — not found in this source at comparable explicitness; still requires broader parent search and protected evidence.
- `ORION_NOT_NEEDED` — parent object is stronger/more precise for the stated role and should be reused rather than duplicated.

---

## 1. Wang/Buehler source reconstruction

### 1.1 Native scientific object

Wang/Buehler model an agentic discovery system as a **typed artifact system**. In a regime `b`, a schema category `S_b` contains artifact types as objects and admissible operations as morphisms. The current artifact population is a copresheaf

`I_t : S_b -> Set`,

and the category of elements recovers realized typed provenance. Gates/verifiers control acceptance, rejection or supersession. A richer knowledge-computation object includes schema, grammar, typed state, provenance, verifier, optional description-length functional, discourse and publication map.

Their central distinction is:

- retrieval: add an already representable artifact;
- search: find a path/object inside a fixed schema;
- discovery: change the representational regime itself.

A fixed-regime update is `Phi_b` on artifact states. A discovery move uses a schema map

`u : S_b -> S_b'`

and transports old evidence by left Kan extension. An explicit preservation map binds old accepted artifacts into the new state; residual content outside transported evidence identifies what the new regime had to add beyond reinterpretation.

The formalism explicitly handles new types, morphisms, verifiers, grammar productions or tool classes and includes a Kan obstruction: transport alone cannot populate isolated new types.

### 1.2 Strongest interpretation

The source should be read as more than a metaphor. It supplies a formal representation of typed scientific artifact states, provenance, gate-controlled commitment, fixed-regime dynamics, verified regime transition, preservation and residual structure. ORION cannot preserve novelty by calling its own objects “more operational” without a direct discriminator.

---

## 2. Wang/Buehler <-> ORION mapping

| ORION object | Wang/Buehler object | Recovery | Consequence |
|---|---|---|---|
| Generative regime `Gamma_t` | discovery regime `b=(S_b,Gamma_b,V_b,L_b)` plus schema/grammar/verifier/tool vocabulary | `PARENT_RECOVERED_HIGH` | ORION does not own the idea of an explicit mutable scientific generative/representational regime. |
| Fixed-regime search/action | `Phi_b` update inside fixed schema | `PARENT_RECOVERED_HIGH` | “search within a regime” vs “change the regime” is directly overlapped. |
| `mu_t: Gamma_t -> Gamma_{t+1}` | verified regime transition `u:S_b -> S_b'` | `PARENT_RECOVERED_HIGH` | The transition concept and novelty slogan must contract. |
| Representation/model/tool/verifier expansion | new object/morphism/verifier/grammar/tool class in `S_b'` | `PARENT_RECOVERED_HIGH` | Broad regime-change scope is directly formalized. |
| Preservation obligations | preservation map `rho:I_t -> u* I'_{t+1}` + Kan transport | `PARENT_RECOVERED_HIGH` | Generic “preserve old valid structure across change” is parent-owned here. |
| Provenance lineage | category of elements / typed provenance graph | `PARENT_RECOVERED_HIGH` | Wang/Buehler provides a more mathematically explicit provenance object for its domain. |
| Accepted/rejected/superseded alternatives | gates/verifiers and recorded rejected alternatives | `PARENT_RECOVERED_HIGH` | Rejection/supersession history is not an ORION novelty. |
| Novel residual after transition | artifacts outside image of comparison map after Kan transport | `PARENT_RECOVERED_HIGH` | “new content beyond transport” has an explicit parent formalization. |
| Regime-change cost | optional relative description-length/MDL cost | `PARENT_RECOVERED` | ORION should not invent a generic scalar novelty/progress metric where parent cost semantics suffice. |
| Typed scientific state | copresheaf/artifact knowledge-computation state | `PARENT_RECOVERED_PARTIAL_SCOPE` | Strong overlap, though ORION's `E_t` additionally binds problem/criterion, obligations, resources, evidence dependence, history and external authority. |
| Transition receipt `rho_t` | typed provenance + gate records + regime-transition audits + preservation map | `PARTIAL_OVERLAP_HIGH` | ORION receipt cannot claim priority; residual must be omission-specific recovery of cross-parent decision state not captured by the parent graph. |
| Frontier obstruction | Kan transport obstruction / evidence pressure / failure that current vocabulary cannot express | `PARTIAL_OVERLAP` | Parent has a precise structural obstruction for transport/schema reach; ORION's wider obstruction taxonomy needs evidence, not terminology. |
| Prospective discriminator before escalation | gates, stress tests, model-selection criteria | `PARTIAL_OVERLAP` | Parent has tests/gates; no generic claim should be made until we show a distinct prospective discriminator burden changes decisions. |
| Minimum-sufficient escalation across levels | no comparable general intervention lattice/lower-level-disposition rule identified in this source | `RESIDUAL_CANDIDATE_ONLY` | Test against metareasoning/diagnosis/MDA; do not infer novelty from source absence. |
| Lower-level disposition before higher-level change | no direct general analogue identified | `RESIDUAL_CANDIDATE_ONLY` | Potential ORION-specific control condition; decisive false-escalation study required. |
| Selective reopening of support families | retraction/supersession and preservation exist, but no generic sufficient-support-family reopening calculus identified | `PARTIAL_OVERLAP` | Must compare directly with TMS/ATMS/assurance parents before residual claim. |
| External authority ceiling `K_t` | no explicit external scientific/action authority ceiling identified in the formal object | `RESIDUAL_CANDIDATE_ONLY` | Governance/control parents may own this; requires changed-vocabulary search. |
| Typed context transport/local-global atlas | regime/schema transport is formalized; finite local-chart gluing/horizon object not directly matched | `PARTIAL_OVERLAP` | Do not conflate schema transport with ORION atlas, but atlas still must earn scientific decision value. |
| `CANNOT_CHECK` as terminal | gates may reject/hold/review; no exact ORION terminal semantics identified | `PARTIAL_OVERLAP` | Compare to verification/abstention/partial-decision parents. |

### 2.1 Parent-recovery conclusion

The following ORION phrases are **not safe novelty carriers** after this source:

- fixed-regime versus regime-changing discovery;
- representational-regime transition;
- typed scientific artifacts/operations/verifiers;
- preservation of old valid artifacts/provenance across regime change;
- residual content beyond transported old evidence;
- explicit recorded accepted/rejected alternatives and gates.

A surviving ORION claim must sit *outside or across* these recovered objects.

---

## 3. El Agente Gráfico source reconstruction

### 3.1 Native object

The original 2026 Gráfico paper argues that scientific execution context should be first-class, structured, typed and persistent rather than transient free text. Scientific/computational state is represented as typed Python object graphs and stored in a knowledge graph through an object graph mapper. Execution graphs define admissible data flow, including conditional/cyclic transitions; schema validation constrains inputs and transitions; a routing LLM chooses among admissible successors.

The system tracks provenance and uses both deterministic numerical evaluation and semantic task evaluation. Its benchmark emphasizes computational correctness, task adherence, cost, context pressure, error-recovery cost and trace behavior.

The August-revised public description strengthens the same direction by saying that scientific state must be validated, transferred and recorded across heterogeneous operations and that typed execution graphs enforce admissible scientific-state transitions, record provenance and confine model judgment to explicit decision points.

### 3.2 Strongest interpretation

Gráfico should be treated as a strong systems parent for:

- externalized scientific/computational state;
- typed state-transition graphs;
- admissible workflow transitions;
- schema/type validation;
- provenance and persistent state;
- routing constrained to valid next operations;
- deterministic + semantic evaluator separation.

ORION cannot claim field novelty for those engineering ideas.

---

## 4. Gráfico <-> ORION mapping

| ORION object | Gráfico object | Recovery | Consequence |
|---|---|---|---|
| Structured scientific state | typed Python object graph / `ConceptualAtoms` / KG state | `PARENT_RECOVERED_HIGH` | Externalized structured state is a strong parent capability. |
| Admissible actions/transitions | execution graph edges + schema-conditioned routing | `PARENT_RECOVERED_HIGH` | “admissible scientific state transitions” is not a distinctive ME phrase. |
| State persistence/history | KG/OGM identifiers and persisted objects | `PARENT_RECOVERED_HIGH` | Persistence/memory/provenance is parent-owned. |
| Typed transport across tools | package-specific objects composed through common abstraction, direct Python references, persistent identifiers | `PARENT_RECOVERED_HIGH_EXECUTION_SCOPE` | Tool/data transport has a direct systems solution. |
| Execution validation | pydantic/type validation + deterministic numerical evaluator | `PARENT_RECOVERED_HIGH` | ME should reuse or benchmark against this rather than duplicate it. |
| Semantic task adherence | LLM judge over trace/final output | `PARENT_RECOVERED_PARTIAL` | Scientific warrant cannot be assumed from semantic adherence; evaluator blindness remains an ME test case. |
| Transition receipt | trace + state/provenance records | `PARTIAL_OVERLAP_HIGH` | ORION must show why evidence/support/evaluator/authority deltas alter downstream decisions beyond runtime trace. |
| Evidence dependence | no general scientific support-dependence calculus identified | `RESIDUAL_CANDIDATE_ONLY` | Dependence parents still own the mechanism; possible cross-transition need. |
| Selective reopening | repair loops exist for execution errors; no generic defeated-support reopening semantics identified | `PARTIAL_OVERLAP` | Distinguish execution repair from scientific commitment reopening. |
| Scientific evaluator fitness | deterministic/semantic evaluators are present, but no general contract that evaluator sensitivity must match claimed failure class identified | `RESIDUAL_CANDIDATE_ONLY` | Must test against VVUQ/verification parents. |
| Cross-context scientific transport | execution/data handoff across packages exists; causal/measurement/scientific generalization transport is not the central formal object | `PARTIAL_OVERLAP` | Do not call tool-state transfer the same as scientific claim transport. |
| External authority ceiling | no general external adoption/action authority object identified | `RESIDUAL_CANDIDATE_ONLY` | Governance parents may absorb it. |
| Minimum-sufficient escalation / regime change | workflow routing/repair exists, not a general evidence-witnessed intervention-level theory | `PARTIAL_OVERLAP` | Must compare with diagnosis/metareasoning/MDA. |
| Local/global atlas/horizon | no direct match identified | `RESIDUAL_CANDIDATE_ONLY` | Still no novelty claim without parent/empirical test. |

### 4.1 Critical distinction for ME-X1

The strongest scientifically useful difference to test is:

> **A runtime transition may be type-correct, numerically correct and provenance-complete while the scientific transition remains unwarranted.**

Candidate examples:

- correct computation under an invalid calibration;
- correct result attached to a wrong claim identity;
- correct local result transported to an unsupported target context;
- correct execution using evidence whose independence assumption has failed;
- correct formal verification of a semantically drifted specification;
- correct calculation followed by an action above the external authority ceiling.

This distinction is only a field residual if the strongest parent federation—including Gráfico-like runtime validity plus measurement/provenance/transport/assurance parents—still fails without an additional cross-transition condition.

---

## 5. Combined reduction

### 5.1 Fully or substantially parent-recovered surface

After giving both sources their strongest reading, Machine Epistemics should not attempt to own:

1. structured scientific state;
2. typed scientific artifacts and operations;
3. admissible typed execution transitions;
4. provenance/persistent state;
5. fixed-regime search versus regime-changing discovery;
6. verified representational-regime transition;
7. preservation/transport of old valid artifacts;
8. gates/verifiers and recorded rejected alternatives;
9. workflow mutation in self-revising scientific agents.

### 5.2 Surviving candidates, still unproven

The strongest candidates left after this two-parent recovery are:

1. **cross-parent warrant coupling:** evidence/provenance/evaluator/transport/reopening/authority interactions that change downstream scientific decisions even when local parent operations are correct;
2. **minimum-responsible-level escalation:** a witnessed obstruction + discriminator + lower-level disposition rule that predicts when to search, gather data, expand a model, change representation, reformulate the problem, build a tool or change workflow;
3. **selective cross-mode reopening:** exact propagation of support defeat across heterogeneous scientific commitments while independent support is preserved;
4. **external authority separation:** warrant to believe/revise does not itself create authority to take higher-impact actions;
5. **local/global witness discipline:** local validity/compatibility does not imply a warranted global scientific synthesis;
6. **bounded unresolvedness:** explicit missing-warrant identity that supports defer/CANNOT_CHECK rather than either execution failure or blanket rejection.

Every item above is a **residual candidate only**. Metareasoning, TMS, assurance, governance, category/sheaf methods, formal learning and other parents may still absorb it.

---

## 6. Decisive discriminator matrix

| Residual candidate | Strong next parent comparator | Required ORION test |
|---|---|---|
| cross-parent warrant coupling | Gráfico-like runtime + verification-first science + provenance + domain assurance | `ME-X1`, then `ME-X5` |
| minimum-responsible escalation | diagnosis + metareasoning + VoI + Model Discovery Agent | `ME-X2` |
| regime-change residual | Wang/Buehler + formal refinement + model discovery | `ME-X3` plus formal mapping |
| selective reopening | ATMS/TMS + assurance/provenance | `ME-X4` |
| local/global witness | causal transport + measurement invariance + category/sheaf/native relation parents | `ME-X5` |
| unresolvedness | selective prediction + verification/robust decision | `ME-X1` unresolved strata |
| authority ceiling | governance/decision rights/safety case parents | dedicated changed-vocabulary recovery before claim |

---

## 7. Immediate changes to public claim posture

Use formulations like:

- “Machine Epistemics tests whether cross-transition constraints add decision value beyond strong existing components.”
- “Representational-regime transitions are a major contemporary parent/neighbor, not an ORION priority claim.”
- “Typed scientific-state runtimes and provenance already have strong systems realizations.”

Avoid formulations like:

- “Machine Epistemics introduces scientific-state transitions.”
- “ORION is the first framework to distinguish search from regime change.”
- “ORION uniquely formalizes representation-changing discovery.”
- “A transition receipt is novel because other agents only output text.”

---

## Current terminal

```text
WANG_BUEHLER_PARENT_RECOVERY = HIGH
GRAFICO_PARENT_RECOVERY = HIGH
GAMMA_REGIME_CHANGE_NOVELTY = CONTRACTED
TYPED_SCIENTIFIC_STATE_NOVELTY = CONTRACTED
PROVENANCE_TRANSITION_NOVELTY = CONTRACTED
CROSS_PARENT_WARRANT_COUPLING = RESIDUAL_CANDIDATE_ONLY
MINIMUM_RESPONSIBLE_ESCALATION = RESIDUAL_CANDIDATE_ONLY
SELECTIVE_CROSS_MODE_REOPENING = RESIDUAL_CANDIDATE_ONLY
EXTERNAL_AUTHORITY = RESIDUAL_CANDIDATE_ONLY
LOCAL_GLOBAL_WARRANT = RESIDUAL_CANDIDATE_ONLY
FIELD_STATUS = UNRESOLVED
```
