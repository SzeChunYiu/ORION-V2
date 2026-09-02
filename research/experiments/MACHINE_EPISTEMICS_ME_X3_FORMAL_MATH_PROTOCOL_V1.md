# ME-X3 — Formal Mathematical Discovery and Regime Change Protocol V1

**State date:** 2026-09-01  
**Status:** prospective design; no protected ME-X3 outcome inspected  
**Parent protocol:** `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md`  
**Related existing ORION protocol:** `CONCEPTUAL_TRANSFER_DISCOVERY_PROTOCOL_V2_ALL_SCIENCE_MATHEMATICS_FIRST.json`

## 0. Scientific question

The study does **not** ask whether an LLM can prove Lean theorems. That is already a mature and fast-moving research area.

It asks:

> **When a formal mathematical problem is not being solved efficiently, can explicit epistemic obstruction diagnosis identify whether the right next move is more proof search, a missing lemma, a representation change, a new probe/counterexample, or honest unresolvedness—and does choosing the minimum responsible move improve verified mathematical reach and cost beyond the strongest matched parent systems?**

The claimed mechanism is therefore:

`failure evidence -> obstruction diagnosis -> intervention-level choice -> verified mathematical consequence`.

A success that skips the diagnostic mediation or merely spends more compute is not evidence for the ME mechanism.

---

## 1. Strong parents and 2026 collisions

### Discover and Prove (ACL 2026)

Hard Mode separates **answer discovery** from formal proof. DAP uses natural-language reasoning and explicit self-reflection to discover the answer, rewrites the task into an easier formal-proof form, and composes with ATP systems. It reports a large gap between answer accuracy and formal proof success.

**Consequence:** ME-X3 must compare against a discovery-then-prove architecture; “reason first, prove second” is parent-owned.

### FormalScience (ACL 2026)

FormalScience demonstrates scalable agentic autoformalization and documents **semantic drift despite formal validity**, including notational collapse and abstraction elevation.

**Consequence:** Lean acceptance cannot be the only primary endpoint. A separate specification/intent-preservation outcome is mandatory.

### Lemma/conjecture discovery and verified self-improvement

Existing theorem-discovery systems generate/reuse verified intermediate results and abstractions.

**Consequence:** “invent a lemma” is not an ME novelty. ME must show better **decision control over when lemma/representation invention is warranted** and avoid false invention on direct-search cases.

### Wang/Buehler regime transition

Representational-regime change with verification/preservation has direct 2026 formal precedent.

**Consequence:** the novelty target is not representation change itself but minimum-responsible intervention under diagnosed obstruction, plus transfer/specification consequences.

---

## 2. Exact hypotheses

### H3-A — obstruction discrimination

Given matched observed search failure, ME predicts the hidden minimal intervention family better than B5.

### H3-B — intervention value

Conditioning action on the diagnosed obstruction improves verified solve/cost frontier relative to B5.

### H3-C — false-change control

On `DIRECT_SEARCH` and `DECEPTIVE_CHANGE` strata, ME does not pay a representation/lemma proliferation penalty large enough to erase gains elsewhere.

### H3-D — transferable invention

A genuinely useful invented lemma/representation improves held-out related problems without sacrificing predecessor-valid cases or specification fidelity.

### H3-E — verifier/specification separation

ME detects or avoids a subset of cases where a formally valid theorem/proof is semantically misaligned with the intended mathematical/scientific statement beyond a proof-only baseline.

---

## 3. Environment freeze

Before protected generation/solving, bind:

- Lean major/minor version;
- exact mathlib commit;
- build toolchain and CPU/memory limits;
- base model/provider/version and decoding settings;
- maximum tokens, wall-clock, Lean invocations and retrieval calls per problem;
- whether network retrieval is disabled or which indexed corpus is allowed;
- exact accessible theorem/library namespace;
- problem generator commit/digest;
- train/dev/protected split identities;
- theorem-name and source-string leakage audit;
- evaluator code and independent semantic-adjudication packet.

A protected problem must not be moved back into development after an outcome is seen.

---

## 4. Problem families

Each family should contain exact positive/negative controls and multiple surface realizations.

### F1 — DIRECT_SEARCH

The registered representation and library already contain a reasonably short proof route. Additional lemma/representation invention should usually be unnecessary.

Purpose: false-escalation control.

### F2 — MISSING_LEMMA

A reusable intermediate lemma materially shortens or enables the target proof, but the base representation remains adequate.

Purpose: distinguish lemma invention from full representation change.

### F3 — REPRESENTATION_CHANGE

The original encoding yields a large/unproductive search space; a known but hidden alternative representation or transformation makes the problem tractable.

Examples may include hidden change of variables, dualization, quotienting, invariant-based encoding, normalization, generating-function style recoding, alternate induction measure or equivalent finite structure.

Purpose: test level-3 intervention.

### F4 — DECEPTIVE_CHANGE

Surface cues strongly suggest a sophisticated transformation, but direct/local proof repair is sufficient and cheaper.

Purpose: punish “creativity = progress”.

### F5 — PROBE_OR_COUNTEREXAMPLE_NEEDED

The next rational action is not proof construction but a small-model search, counterexample probe or discriminating computation that eliminates an incorrect route.

Purpose: connect horizon refinement to action.

### F6 — UNDERDETERMINED_OR_CANNOT_CHECK

Within the frozen budget/library, the available evidence does not identify a justified next high-level transformation. The correct control output may be `CANNOT_IDENTIFY`/`UNRESOLVED`.

Purpose: calibration and anti-fabrication.

### F7 — SPECIFICATION_MISMATCH

A formally provable statement is available but differs from the intended problem through dropped conditions, strengthened/weakened quantifiers, notational collapse, degenerate objects, abstraction elevation or other semantic drift.

Purpose: verifier-specification separation.

### F8 — TRANSFER

A lemma or representation discovered on one task family should improve a held-out sibling family. The held-out targets and reuse criterion are frozen before the invention is inspected.

Purpose: distinguish one-off proof hack from epistemic capability expansion.

---

## 5. Task sourcing and contamination strategy

Use a mixture; no single source class is sufficient.

### S1 — public Hard Mode benchmarks

Use DAP-style Hard Mode tasks for calibration/compatibility only. Famous public tasks cannot establish discovery novelty because training contamination is plausible.

### S2 — fresh generated formal worlds

Reuse the existing ORION mathematics-first protocol's strengths:

- generated after protocol freeze;
- hidden correct transition class;
- hidden donor/representation identity;
- arbitrary relation/operation/token renaming;
- formal witness/counterexample hidden from solver;
- explicit `NO_CHANGE` tasks.

These are strongest for known-answer mechanism tests.

### S3 — transformed held-out theorem families

Take source theorems from an allowed formal corpus and generate semantics-preserving but nontrivial transformed families after freeze. Scrub source names and run nearest-string/theorem lookup audits.

### S4 — independently authored challenge set

Require a subset authored or adjudicated by a formal-math reviewer who did not build the ME controller. This is required before any cross-domain/field claim.

### S5 — scientific autoformalization cases

Include a small FormalScience-like stratum where the natural-language scientific/mathematical intent and Lean statement must both be judged.

---

## 6. Arms

### A0 — DIRECT

Base model + Lean tools under the frozen budget, no explicit metacognitive or regime-control scaffold.

### A1 — RETRIEVAL

A0 + permitted mathlib/theorem retrieval/search.

### A2 — SELF_REFLECT

A1 + generic self-reflection/retry loop with the same total budget.

### A3 — DISCOVER_AND_PROVE_PARENT

A strong Hard Mode composition: answer/discovery reasoning followed by formal proof search.

### A4 — LEMMA_ABSTRACTION_PARENT

A strong parent allowed to propose intermediate lemmas/abstractions and reuse verified discoveries.

### A5 — B5_FORMAL_MATH_FEDERATION

Composition of the strongest applicable parents: retrieval + DAP-style discovery + proof search + lemma/abstraction generation + counterexample/small-model tools + standard uncertainty/control.

Ordinary engineering communication/shared state is permitted.

### M — ME_CONTROL

A5 receives the same tools/information, plus the candidate ME control contract:

- explicit obstruction hypotheses;
- evidence/witnesses for the obstruction;
- discriminators where ambiguity remains;
- lower-level disposition;
- minimum-intervention selection;
- versioned lemma/representation transition when selected;
- preservation/specification obligations;
- non-authorizing transition receipt;
- unresolved terminal.

The experiment is invalid if M receives hidden oracle obstruction labels unavailable to A5.

---

## 7. Required ME ablations

- `M_MINUS_OBSTRUCTION_CLASS`
- `M_MINUS_LOWER_LEVEL_DISPOSITION`
- `M_MINUS_FALSE_CHANGE_PENALTY`
- `M_MINUS_SPECIFICATION_PRESERVATION`
- `M_MINUS_TRANSFER_REUSE_TRACKING`
- `M_MINUS_UNRESOLVED_TERMINAL`

The primary mechanistic claim requires the relevant ablation to degrade the exact protected behavior it is supposed to control.

---

## 8. Registered intervention vocabulary

The controller chooses among a finite set before free-form execution:

- `CONTINUE_DIRECT_PROOF_SEARCH`
- `RETRIEVE_EXISTING_LEMMA`
- `INVENT_LOCAL_LEMMA`
- `GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL`
- `CHANGE_REPRESENTATION`
- `REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK`
- `REQUEST_SPECIFICATION_CLARIFICATION`
- `DEFER_CANNOT_IDENTIFY`

Free-form reasoning can occur inside an action, but evaluation binds the high-level decision first.

---

## 9. Outcomes

### Primary outcome vector

Report separately:

1. `LEAN_VERIFIED_TARGET_SUCCESS`;
2. `SPECIFICATION_INTENT_MATCH`;
3. `MINIMAL_INTERVENTION_ACCURACY` on known-answer strata;
4. `FALSE_HIGH_LEVEL_CHANGE_RATE`;
5. `RESOURCE_COST`;
6. `HELD_OUT_REUSE_GAIN` for verified inventions.

Do not collapse these into one scalar until after per-component reporting.

### Secondary

- proof length;
- number of Lean compiler/checker calls;
- number of invented lemmas;
- fraction of invented lemmas reused;
- time to first valid proof;
- calibrated unsolved/unresolved prediction;
- recurrence of the same obstruction after intervention.

---

## 10. Specification-intent adjudication

Formal verification is necessary but not sufficient for F7/S5.

For each protected specification case, the adjudication packet should include:

- original natural-language mathematical/scientific intent;
- hidden reference formalization(s) where available;
- mandatory semantic invariants/conditions;
- forbidden simplifications/degeneracies;
- known acceptable equivalent formulations;
- independent reviewer verdict.

Record at least:

- `FAITHFUL`
- `MATERIALLY_WEAKENED`
- `MATERIALLY_STRENGTHENED`
- `NOTATIONAL_COLLAPSE`
- `ABSTRACTION_ELEVATION`
- `OTHER_SEMANTIC_DRIFT`
- `CANNOT_CHECK`.

A Lean proof of a drifted statement is **not** target success.

---

## 11. Statistical/evaluation plan

Use problem-level paired comparisons wherever the same task can be run under all arms.

Primary analysis should estimate per-stratum differences and uncertainty for:

- verified + specification-faithful success;
- minimal-intervention accuracy;
- false-change rate;
- resource use.

Do not let a gain on F3 hide harm on F1/F4. Report the Pareto/quality-cost frontier by stratum.

For stochastic systems, freeze repetitions/seeds prospectively and retain all failures/timeouts.

No post-hoc dropping of “bad prompts” or difficult families.

---

## 12. Success ladder

### M0 — no effect

A5 matches/exceeds M. Contract the ME-math mechanism.

### M1 — diagnostic value only

M predicts obstruction/minimal intervention better but does not improve verified quality-cost outcomes. Publishable as analysis/benchmark at most; no capability claim.

### M2 — mechanism-specific capability gain

M improves verified + faithful solve/cost frontier on at least one prespecified obstruction stratum, and the relevant ablation removes the gain.

### M3 — transferable epistemic gain

M2 plus invented lemma/representation improves held-out family performance under frozen reuse tests.

### M4 — cross-mode support

The same control principle later survives another epistemic domain under ME-X5. Only this begins to support a field-level residual.

---

## 13. Kill criteria

Contract the mathematical ME claim if:

- A5 ties or wins after matched compute/tools;
- M's advantage comes from extra retrieval/library visibility;
- obstruction labels do not mediate intervention value;
- representation/lemma invention is merely a post-hoc narrative around ordinary search;
- false-change overhead erases gains on direct/simple tasks;
- specification drift materially rises;
- held-out reuse fails;
- effects disappear under arbitrary renaming/fresh generated worlds;
- only contaminated/famous public tasks show gains.

---

## 14. Implementation boundary

Do **not** implement the final ME controller before:

1. the task strata and generator contract are frozen;
2. A5 strongest-parent architecture is specified;
3. resource accounting is specified;
4. protected custody is defined;
5. the parent-recovery mapping to DAP, FormalScience, lemma discovery and Wang/Buehler is complete enough to avoid a trivial duplicate study.

Implementation may then be minimal and study-specific. ORION-V2 remains the experimental framework, not the field ontology.

## Terminal

```text
ME_X3_STATUS = PROSPECTIVE_UNEXECUTED
LEAN_VERIFICATION = LOCAL_TRUTH_CHECK_NOT_INTENT_ORACLE
DISCOVER_AND_PROVE = STRONG_PARENT
FORMALSCIENCE_SEMANTIC_DRIFT = REQUIRED_CONTROL
LEMMA_ABSTRACTION_DISCOVERY = PARENT_OWNED_MECHANISM
ME_RESIDUAL = OBSTRUCTION_TO_MINIMUM_INTERVENTION_CONTROL
FALSE_CHANGE_CONTROLS = REQUIRED
HELD_OUT_TRANSFER = REQUIRED_FOR_STRONG_CAPABILITY_CLAIM
PROTECTED_OUTCOMES_INSPECTED = FALSE
```
