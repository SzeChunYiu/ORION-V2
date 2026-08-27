# ORION-V2 V1 Capability Parity Closure Matrix — Wave 06

**Status:** closeout planning against the exact 59-cell frozen V1 capability census. This is not a claim that parity has been earned.

## 1. Source identity

The census is bound to:

- ORION V1 freeze commit `8f250fc3e55d6d6a28fb1fb33d9932ef1a8760b5`;
- workflow blob `d91e9e34fc7031b181ecf9ad9f65569e71f87838`;
- decomposition blob `6e0852883487e64cdd38f3a183cafe8905011eaa`;
- action blob `4e470d44807bd1cd66ad4eee07734036bd9171c1`;
- 59 declared root/operator/child/cross-cutting capabilities.

The objective is **capability parity**, not module-name parity. A V1 capability can be merged into a deeper V2 kernel object or replaced by a stronger parent implementation, but it may not silently disappear.

## 2. Evidence grades

- `R0 — MAPPED_ONLY`: a candidate V2 owner exists; no executable known-answer coverage.
- `R1 — REFERENCE_KNOWN_ANSWER`: finite/reference tests exercise the scientific distinction.
- `R2 — INTEGRATED_REFERENCE`: multiple V2 objects compose and current CI checks the path.
- `R3 — MATCHED_V1_CONTROL_REQUIRED`: a paired frozen-V1 versus V2 comparison is still required.
- `R4 — PROTECTED_PARITY_EARNED`: protected non-regression under matched resources and frozen evaluator. No current capability is assigned R4 by this planning artifact.

Reference coverage is useful for correctness and contraction; it is not parity evidence by itself.

## 3. Exact family census

### Root and top-level operators — 10 capabilities

`ORION_SOLVE.v1`, `FRAME.v1`, `SEARCH.v1`, `ABSORB.v1`, `RECONSTRUCT.v1`, `DETECT.v1`, `DIAGNOSE.v1`, `REFRAME.v1`, `REOPEN.v1`, `SATURATE_BOUNDED.v3`.

**Candidate V2 ownership:** K0–K6 together, especially K4 solver/action/recovery and K6 parity/saturation.

**Current grade:** R2 at reference-composition level; R3 required for all ten as end-to-end behaviour.

**Parity question:** can the contracted V2 solver reproduce or improve the frozen V1 capability outcome under matched problem, information, resource, authority and evaluator contracts without unnecessary extra work or escalation?

---

### FRAME family — 5 child capabilities

1. `FRAME.QUESTION.v0`
2. `FRAME.CONTEXT.v0`
3. `FRAME.AUTHORITY_TARGET.v0`
4. `FRAME.RESOURCES.v0`
5. `FRAME.DECOMPOSE.v0`

**V2 owners:** K0 contract/obligations; K1 state; K4 workflow/decomposition.

**Reference evidence:** `ProblemContract`, obligations, resource ceilings, workflow constraints and authority-required terminals are executable.

**Current grade:** R2 for contract/authority/resource invariants; R1 for decomposition constraints; R3 for all five.

**Needed controls:** direct/simple tasks where decomposition is unnecessary; coupled tasks where naive decomposition is invalid; explicit authority/resource-bound cases. V2 is harmed if it adds decomposition or escalation cost to a direct V1-solvable case.

---

### SEARCH family — 5 child capabilities

1. `SEARCH.ROUTE.v0`
2. `SEARCH.QUERY.v0`
3. `SEARCH.SOURCE.v0`
4. `SEARCH.RETRIEVE.v0`
5. `SEARCH.ROUTE_STOP.v0`

**V2 owners:** K4 action interface plus external search/retrieval adapters; K6 coverage/saturation.

**Reference evidence:** route censoring and coverage semantics are represented, but the current V2 reference package does not yet constitute a production heterogeneous search engine or matched V1 retrieval campaign.

**Current grade:** R0/R1 only; **high-priority R3 gap**.

**Needed controls:** identical source universe, query budget and provider access; censored-route cases; source-quality/lineage cases; route stop without task closure; search-universe expansion. The parity study should prefer mature search/retrieval adapters rather than rebuilding V1 retrieval mechanics in the kernel.

---

### ABSORB family — 6 child capabilities

1. `ABSORB.SCIENTIFIC_LANGUAGE.v0`
2. `ABSORB.CLAIM.v0`
3. `ABSORB.REFERENCE_IDENTITY.v0`
4. `ABSORB.CONTEXT.v0`
5. `ABSORB.REPRESENTATION_MAP.v0`
6. `ABSORB.EVIDENCE_BIND.v0`

**V2 owners:** K1 plural state; K2 relation/transport; K3 evidence/provenance; native-domain adapters.

**Reference evidence:** `DomainProblem`, native-recovery, structural relation, comparability, provenance and evidence objects cover the post-extraction semantics. Generic scientific-language/claim extraction is not yet a protected V2-native capability.

**Current grade:** R1/R2 for mapping/context/evidence semantics; R0 for generic language and claim extraction; **high-priority R3 gap**.

**Contraction rule:** language parsing, entity resolution and scientific IE should default to mature parent/model adapters. V2 owns the typed acceptance/quarantine/evidence contract, not necessarily the parser.

---

### RECONSTRUCT family — 4 child capabilities

1. `RECONSTRUCT.ATLAS_UPDATE.v0`
2. `RECONSTRUCT.GLUE.v0`
3. `RECONSTRUCT.PORTRAIT.v0`
4. `RECONSTRUCT.SEARCH_UNIVERSE.v0`

**V2 owners:** K1 plural state; K2 structural relation/gluing; K3 provenance/revalidation; K6 coverage.

**Reference evidence:** local/global obstruction, scale/gluing, plural structural relations, provenance and future-query unsafe quotients have exact known-answer tests.

**Current grade:** R2; R3 still required on frozen V1 cases.

**Needed controls:** local compatibility with global obstruction; multiple justified portraits; representation update that expands the search universe; negative case where a forced global portrait is invalid.

---

### DETECT family — 4 child capabilities

1. `DETECT.CONTRADICTION.v0`
2. `DETECT.GAP.v0`
3. `DETECT.COVERAGE.v0`
4. `DETECT.FAILURE.v0`

**V2 owners:** K1 obligations/defeaters; K4 solver terminals; K6 coverage/failure ledgers.

**Reference evidence:** contradiction/obstruction, non-identifiability, coverage/censoring and typed failure terminals are represented.

**Current grade:** R2 for semantic distinction; R3 for detection sensitivity/specificity.

**Needed controls:** missing evidence versus contradiction; structural non-identifiability versus resource failure; censored search versus absence; failed execution versus scientific negative result.

---

### DIAGNOSE family — 4 child capabilities

1. `DIAGNOSE.HYPOTHESES.v0`
2. `DIAGNOSE.EXPERIENCE_RETRIEVAL.v0`
3. `DIAGNOSE.DISCRIMINATOR.v0`
4. `DIAGNOSE.ATTRIBUTION.v0`

**V2 owners:** K4 responsibility/probes; K3 dependence; external experience/memory adapter.

**Reference evidence:** multiple/distributed/interaction responsibility and minimum distinguishing probes have finite known-answer support. Experience retrieval itself is not yet a complete V2 runtime service.

**Current grade:** R2 for diagnosis/discriminator mathematics; R0/R1 for experience retrieval; R3 required.

**Needed controls:** single-fault, multiple-fault, cancellation, interaction-only and unresolved cases; cases where earliest-stage attribution is correct and cases where forcing a single owner is wrong.

---

### REFRAME family — 5 child capabilities

1. `REFRAME.REPRESENTATION.v0`
2. `REFRAME.DECOMPOSITION.v0`
3. `REFRAME.SEARCH_POLICY.v0`
4. `REFRAME.METHOD.v0`
5. `REFRAME.OBJECTIVE.v0`

**V2 owners:** K2 transport/adaptation; K4 recovery; K5 witnessed escalation.

**Reference evidence:** exact/stochastic transport, target adaptation, Jump minimum-level controls, performative evaluation and policy/workflow reference objects are present.

**Current grade:** R2; R3 required.

**Needed controls:** lower-level repair sufficient; model expansion sufficient; true representation insufficiency; target objective/proxy invalidation; strategic response; invalid post-outcome reframe.

---

### REOPEN family — 3 child capabilities

1. `REOPEN.DEPENDENCY.v0`
2. `REOPEN.CLOSURE.v0`
3. `REOPEN.FIBRE.v0`

**V2 owners:** K3 provenance/revalidation plus K4 recovery.

**Reference evidence:** selective reopen, alternative support families, component inheritance and changed-epoch/correspondence cases are executable.

**Current grade:** R2; R3 required.

**Needed controls:** one support invalidated but alternative support survives; multi-parent component change; unaffected commitments must remain closed; exact versus approximate transport change; new evidence revokes only dependent closure.

---

### SATURATE family — 5 child capabilities

1. `SATURATE.KNOWLEDGE_FLATNESS.v0`
2. `SATURATE.FORMULATION_FLATNESS.v0`
3. `SATURATE.ROUTE_COVERAGE.v0`
4. `SATURATE.OMISSION_CHALLENGE.v0`
5. `SATURATE.STOP.v0`

**V2 owners:** K6 evaluation/parity/saturation; all-domain coverage registry.

**Reference evidence:** multidimensional saturation vector and route-completeness conditions are executable; Wave 06 closeout requires two post-contraction no-material-change passes.

**Current grade:** R1/R2; omission challenge and full-route coverage remain real-world R3 gaps.

**Needed controls:** false flatness caused by censored routes; new donor found only by changed vocabulary; no-growth pass with incomplete route denominator; two complete no-material-change passes.

---

### Cross-cutting family — 8 capabilities

1. `CROSS.MEMORY.v0`
2. `CROSS.AUTHORITY.v0`
3. `CROSS.EXPERIENCE.v0`
4. `CROSS.REVIEW.v0`
5. `CROSS.BENCHMARK.v0`
6. `CROSS.EXPERIMENT_SELECTION.v0`
7. `CROSS.EXECUTION.v0`
8. `CROSS.CONTEXT_POLICY.v0`

**V2 owners:** K0 receipts/contracts, K3 evidence/provenance, K4 action/execution, K6 evaluation/authority; memory/review/experience can be parent services.

**Reference evidence:** authority is fail-closed; benchmark/evaluator identity and non-compensation are represented; minimum probe/action selection and step receipts are executable. Persistent memory, independent review, experience retrieval/learning and real tool/lab execution are not fully exercised as end-to-end V2 services.

**Current grade:**

- authority: R2 -> R3;
- benchmark/evaluator: R2 -> R3;
- experiment selection: R2 -> R3;
- context policy: R1 -> R3;
- memory: R0/R1 -> **high-priority R3 gap**;
- experience: R0/R1 -> **high-priority R3 gap**;
- review: R0/R1 -> **high-priority R3 gap**;
- execution: R1/R2 -> **high-priority R3 gap** for real provider/tool/environment effects.

## 4. Parity campaign compression

Fifty-nine cells do not require fifty-nine independent campaigns. The minimum current paired suite can be compressed into nine campaign families, each carrying multiple exact cell obligations:

| Campaign | V1 families exercised | Primary V2 kernel | Essential hostile control |
|---|---|---|---|
| `PARITY-A` direct contract/decomposition | FRAME + root | K0/K4 | V2 over-decomposes simple case |
| `PARITY-B` search/acquisition | SEARCH + coverage | K4/K6 | censored route mistaken for absence |
| `PARITY-C` absorption/native semantics | ABSORB | K1/K2/K3 | parser/map erases native context |
| `PARITY-D` reconstruction/gluing | RECONSTRUCT | K1/K2 | local compatibility, global obstruction |
| `PARITY-E` detection/diagnosis | DETECT + DIAGNOSE | K1/K4 | multiple causes forced into single owner |
| `PARITY-F` reframe/reopen | REFRAME + REOPEN | K2/K3/K4/K5 | unnecessary Jump versus lower repair |
| `PARITY-G` stopping/saturation | SATURATE | K6 | flatness under incomplete coverage |
| `PARITY-H` authority/review/benchmark | cross-cutting authority/review/benchmark | K0/K3/K6 | correlated self-review counted independent |
| `PARITY-I` execution/memory/experience/context | remaining cross-cutting | K0/K3/K4 | failed external effect or missing memory treated as success |

The campaign suite must retain per-cell scoring internally, so compression cannot hide one lost capability behind a family average.

## 5. Non-compensatory parity rule

For each capability cell, record:

- opportunity denominator;
- V1 terminal/decision;
- V2 terminal/decision;
- correctness/validity;
- false completion;
- authority/integrity;
- semantic/provenance preservation;
- selective reopen correctness if applicable;
- resource/cost;
- unnecessary escalation/work;
- `CANNOT_CHECK` calibration;
- replay identity.

Frontier gain cannot compensate for regression on mandatory coordinates.

## 6. Current parity terminal

```text
V1_CAPABILITY_CENSUS = EXACT_59_BOUND
REFERENCE_OWNER_MAPPING = PRESENT
REFERENCE_KNOWN_ANSWER_COVERAGE = SUBSTANTIAL_BUT_INCOMPLETE
PROTECTED_MATCHED_V1_V2_PARITY = NOT_RUN
FIRST_HIGH_PRIORITY_GAPS = SEARCH_ABSORB_MEMORY_EXPERIENCE_REVIEW_REAL_EXECUTION
G1_V1_PARITY = OPEN
```

The next parity work should therefore build the nine campaign protocols and strongest parent adapters; it should **not** create 59 new V2 modules.