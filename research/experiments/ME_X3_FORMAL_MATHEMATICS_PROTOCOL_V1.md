# ME-X3 — Formal Mathematical Discovery and Regime-Control Protocol V1

**State date:** 2026-09-01  
**Status:** prospective, unexecuted  
**Purpose:** test Machine Epistemics in a domain with exact local proof verification without confusing proof validity with correct problem formalization.

## 1. Question

Can explicit discrepancy/obstruction diagnosis improve the decision **when to remain in ordinary proof search and when to introduce a lemma, expand a model/concept repertoire, change representation, or stop with an unresolved/specification-mismatch terminal**, beyond the strongest matched theorem-proving and abstraction parents?

This study does not test whether an LLM can merely prove more theorems with extra search.

## 2. Parent systems and collision boundary

The experiment must treat the following as parents/baselines rather than Machine Epistemics novelty:

- **Discover and Prove (ACL 2026):** Hard Mode separates answer discovery from formal proof and exposes a large gap between answer-level reasoning and formal theorem proving.
- **Conjecturing-Proving Loop (NALOMA 2026):** iteratively reuses self-generated formally verified theorems to improve later theorem discovery/proof.
- **FormalScience / FormalPhysics (ACL 2026):** distinguishes syntactic/formal validity from semantic alignment and documents semantic drift in autoformalization.
- strongest contemporary Lean proof-search, retrieval, lemma-generation, abstraction and autoformalization systems available at protocol freeze.
- Wang–Buehler-style representational-regime revision where a formalized regime-transition parent can be instantiated faithfully.

ME-X3 may not claim novelty for formal verification, theorem discovery, self-reflection, lemma reuse, autoformalization, abstraction invention or representation change in isolation.

## 3. Environment freeze

Before any protected run, freeze:

- Lean version;
- Mathlib commit;
- theorem/problem corpus hashes;
- natural-language and formal statement versions;
- allowed tactics/tools;
- retrieval index and library visibility per arm;
- base model/provider/version and decoding settings;
- context/token/tool-call/wall-clock budgets;
- retry policy;
- contamination audit procedure;
- semantic-intent adjudication protocol;
- protected task and transformation labels.

No network access is allowed during protected solving unless a retrieval arm is explicitly registered and matched across comparators.

## 4. Problem strata

### M3-A — direct search

The incumbent representation and available library are sufficient. A successful controller should avoid unnecessary abstraction/regime changes.

### M3-B — missing lemma

A reusable intermediate lemma materially reduces proof cost. The relevant intervention is local/model-level abstraction, not wholesale representation change.

### M3-C — representation change

An alternative encoding, change of variables, dual formulation, quotient, invariant or other declared representation materially reduces protected proof/search cost or makes the theorem reachable.

### M3-D — deceptive representation change

A plausible representation change adds overhead, semantic risk or search branching while the incumbent route is sufficient. This is the false-escalation control.

### M3-E — underdetermined current probes

Available lemmas/probes cannot distinguish candidate proof routes or constructions; a new discriminating lemma/probe is required or `CANNOT_CHECK` is correct.

### M3-F — specification mismatch

Lean accepts or could accept a formal statement that does not faithfully represent the intended natural-language mathematical/scientific problem. Formal proof success must not erase semantic mismatch.

### M3-G — transfer/reuse

An invented lemma/representation is tested on a held-out related family to determine whether it is a genuine reusable capability rather than a one-problem search artifact.

## 5. Task construction

Use a mixture of:

1. time-sliced public problems whose relevant solutions/formalizations postdate model-training cutoffs where feasible;
2. newly generated theorem families with machine-checkable ground truth and hidden transformation structure;
3. human-authored Hard Mode tasks;
4. semantic-drift/autoformalization cases adapted from scientific formalization parents;
5. negative controls where no representation change is needed.

Protected theorem names, intended transformations and oracle intervention classes must not be visible to the solving system.

## 6. Arms

All arms receive matched information and resource budgets.

- `B0_DIRECT_LEAN_SEARCH`
- `B1_RETRIEVAL_LIBRARY_SEARCH`
- `B2_SELF_REFLECTION_RETRY`
- `B3_DISCOVER_AND_PROVE_STYLE`
- `B4_LEMMA_OR_ABSTRACTION_PARENT`
- `B5_STRONGEST_FAITHFUL_MATH_PARENT_FEDERATION`
- `M_ME_LOCUS_OBSTRUCTION_MINIMUM_ESCALATION`

Where appropriate, add a `WANG_BUEHLER_STYLE_REGIME_PARENT` rather than forcing it into B5 invisibly.

## 7. Machine-Epistemics arm

The M arm may maintain hypotheses that the blocker is:

- ordinary search insufficiency;
- missing lemma/model-family insufficiency;
- representation/generative-regime insufficiency;
- specification mismatch;
- tool/formalism limitation;
- unresolved/non-identifiable.

The diagnosis may suggest a candidate action family but does not authorize it. Higher-level intervention must pass the existing witnessed Jump conditions and preservation/falsifier contracts.

## 8. Primary outcome vector

- Lean-verified solve rate;
- semantic/specification-intent match;
- proof/search token and wall-clock cost;
- tool/tactic calls;
- false escalation rate;
- missed necessary escalation;
- obstruction/locus calibration;
- exact `CANNOT_CHECK` calibration;
- invented lemma/abstraction reuse on held-out tasks;
- transfer gain per unit cost;
- semantic drift or formalization corruption;
- verified success after intervention versus matched additional search.

A pooled solve-rate improvement cannot compensate for worse specification fidelity.

## 9. Mechanistic ablations

- `M_MINUS_LOCUS_DIAGNOSIS`
- `M_MINUS_LOWER_LEVEL_DISPOSITION`
- `M_MINUS_PRESERVATION_CONTRACT`
- `M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK`
- `M_NEVER_CHANGE_REPRESENTATION`
- `M_LOCUS_LABELS_SHUFFLED`
- `M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM`

A causal representation-change claim requires that a pre-registered representation intervention improves the protected result and that a matched-search alternative does not recover the same gain.

## 10. Contamination and leakage controls

- theorem-name/string search audit;
- paraphrase and symbol-renaming controls;
- hidden transformation labels;
- train/dev/protected split by generated family, not only instance;
- retrieval-only control;
- time-sliced source audit;
- duplicate/near-duplicate screening;
- model-family holdout where feasible;
- no use of protected success/failure to tune intervention thresholds.

## 11. Specification-intent control

Proof checking establishes only that the formal theorem follows under the formal environment. For tasks with a natural-language or scientific intent, bind a separate semantic contract and adjudication procedure.

Required terminals include:

- `FORMALLY_VERIFIED_AND_INTENT_ALIGNED`
- `FORMALLY_VERIFIED_BUT_INTENT_MISMATCH`
- `UNVERIFIED_CANDIDATE`
- `CANNOT_CHECK_INTENT`
- `UNSOLVED_WITHIN_BUDGET`

This prevents a valid proof of the wrong statement from counting as a Machine Epistemics success.

## 12. Kill and contraction conditions

Contract the math residual if:

- B5 matches or beats M on the validity–intent–cost frontier;
- gains disappear against matched lemma/abstraction discovery;
- gains are explained by extra search, retrieval, context or tool calls;
- representation changes are post-hoc labels for ordinary search;
- false representation change or semantic drift offsets solve-rate gains;
- the locus diagnosis does not predict successful intervention;
- transfer/reuse disappears on held-out families;
- contamination controls explain the apparent improvement.

A negative or parent-sufficient result remains a successful scientific terminal.

## Terminal

```text
ME_X3_STATUS = PROSPECTIVE_UNEXECUTED
LOCAL_VERIFIER = LEAN
PROOF_VALIDITY_EQUALS_INTENT_FIDELITY = FALSE
PRIMARY_DECISION = SEARCH_VS_LEMMA_VS_REPRESENTATION_VS_UNRESOLVED
PRIMARY_COMPARATOR = STRONGEST_FAITHFUL_MATH_PARENT_FEDERATION
EXTRA_COMPUTE_COUNTS_AS_ME_RESIDUAL = FALSE
FIELD_STATUS_AUTHORITY = NONE
```
