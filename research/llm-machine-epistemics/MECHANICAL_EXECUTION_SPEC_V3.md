# Mechanical Execution Spec V3 — Authoritative No-Thinking Handoff

**Issue:** #51  
**Supersedes:** `COMPUTE_HANDOFF_V1.md` and `MECHANICAL_EXECUTION_SPEC_V2.md` for execution ordering and exact required outputs.  
**Rule:** the executor verifies/falsifies registered statements. It does not invent mathematics, choose a novelty defense, redesign responsibility semantics, or write a new paper argument.

## 0. Canonical scientific inputs

Read exactly in this order:

1. `CURRENT_RESEARCH_STATUS_V2.md`
2. `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V2.md`
3. `papers/llm-machine-epistemics/CLAIM_LEDGER_V2.json`
4. `RESPONSIBILITY_DECISION_QUOTIENT_V2.md`
5. `THEORY_STRENGTHENING_V2.md`
6. `EPISTEMIC_DEFICIENCY_DECOMPOSITION_V1.md`
7. `RESPONSIBILITY_UNIVERSALITY_BOUND_V1.md`
8. `HOSTILE_REVIEW_DECISION_MATRIX_V1.md`
9. `NEAREST_WORK_PASS_02_DYNAMIC_STATE.md`
10. `papers/llm-machine-epistemics/JMLR_SUBMISSION_GATE_V1.md`

If an older file conflicts, the newest version named above controls.

---

# 1. Fixed terminal vocabulary

Every execution stage returns one of:

- `PASS`
- `FAIL_COUNTEREXAMPLE_FOUND`
- `CANNOT_CHECK_FORMALIZATION_GAP`
- `CANNOT_CHECK_TOOLCHAIN`
- `PARENT_OWNED`
- `PARTIAL_OVERLAP`
- `NO_DIRECT_OVERLAP`
- `CANNOT_CHECK_FULL_TEXT`

The final paper returns exactly one of:

- `THEORY_PAPER_RESIDUAL_SUPPORTED`
- `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`
- `REPRESENTATION_IDENTIFIABILITY_ONLY__NO_NEW_RESIDUAL`
- `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`
- `CANNOT_CHECK_FORMAL_PROOF`

No “promising”, “likely”, or unregistered rescue terminal is allowed.

---

# 2. Formal theorem/check identifiers

The formal/symbolic package must map exactly to these IDs.

## Predictive/static foundation

- `L1_PREDICTIVE_SUFFICIENT_REFINES_SP`
- `T2_ENTROPY_MINIMAL_PREDICTIVE_ISOMORPHIC_SP`

## Responsibility decision semantics

- `R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY`
- `R22_CANONICAL_ACTION_COST`
- `R23_OPTIMAL_ACTION_SET_COST`
- `R24_ACTION_AND_RISK_COST`
- `R25_EXACT_TARGET_SPECIAL_CASE`
- `R26_JOINT_ANY_OPTIMAL_SELECTOR_COST`
- `R27_ZERO_COST_COMMON_OPTIMAL_ACTION`

## Information deficits

- `D1_ACQUISITION_COMPRESSION_DECOMPOSITION`
- `D2_NEW_OBSERVATION_FULL_HISTORY_GAIN`
- `D3_PROSPECTIVE_DEFICIENCY_IDENTITY`

## Approximate benchmarks

- `T8A_SINGLE_LOGLOSS_FRONTIER`
- `T8B_INDEPENDENT_RESPONSIBILITY_FRONTIER`
- `T8C_SHARED_EXACT_STATE_SAVING`
- `T8D_WORST_FIBRE_CARDINALITY`

## Dynamic fixed-policy theory

- `T10_HORIZON_REFINEMENT_MONOTONICITY`
- `T11_COARSEST_RIGHT_CONGRUENT_REFINEMENT`
- `T12_FIXED_POLICY_RECURSIVE_IMPLEMENTABILITY`
- `T13_ZERO_STATIC_POSITIVE_DYNAMIC_WITNESS`

## Universality/bounded responsibility

- `U1_RESPONSIBILITY_OVERHEAD_UPPER_BOUND`
- `U2_FIBRE_SEPARATING_SATURATION`
- `U3_UNRESTRICTED_RESPONSIBILITY_FULL_HISTORY`
- `U4_NONINJECTIVE_STATE_FAILING_BINARY_RESPONSIBILITY`
- `U5_RESPONSIBILITY_FAMILY_MONOTONICITY`

### Explicit non-theorem

`JOINT_DYNAMIC_POLICY_AND_STATE_OPTIMIZATION` is **NOT SOLVED / NOT CLAIMED**. Do not prove a weaker statement and label it solved.

---

# 3. Formal proof stack

Try:

1. Lean 4 + Mathlib;
2. Isabelle/HOL;
3. Coq;
4. if entropy formalization is disproportionately blocked, split:
   - theorem prover for finite partitions/right congruence/selector state;
   - two independently implemented exact symbolic checkers for finite entropy/information identities.

A single implementation validating its own generated data is not independent support.

For every theorem emit `FORMAL_THEOREM_LEDGER_V1.json` row:

```json
{
  "theorem_id": "...",
  "result": "PASS|FAIL_COUNTEREXAMPLE_FOUND|CANNOT_CHECK_FORMALIZATION_GAP",
  "assumptions": {
    "finite_positive_support": true,
    "deterministic_base_representation": true,
    "exact_predictive_sufficiency": true,
    "decision_semantics": "...",
    "fixed_policy_for_dynamic_theorems": true,
    "partial_transition_semantics": "explicit_UNDEFINED"
  },
  "proof_artifact": "path",
  "counterexample": null
}
```

All actual assumptions must be serialized.

---

# 4. Partition enumerator

Use restricted-growth strings to enumerate all set partitions for `n=1..7` where tractable. At minimum complete `n=1..6`.

Independent Bell number reference:

```text
B1=1
B2=2
B3=5
B4=15
B5=52
B6=203
B7=877
```

Abort if enumerated counts disagree.

Each history partition object is a canonical tuple of integer class IDs starting at 0 in first-occurrence order.

## Structural predictive check

A candidate deterministic state partition `Z` is predictive-sufficient relative to predictive partition `P` iff every `Z` block is a subset of one `P` block.

Verify:

- every predictive-sufficient `Z` refines `P`;
- minimum block count equals `|P|`;
- equal-block-count predictive refinement equals `P` up to labels.

Output `PREDICTIVE_PARTITION_AUDIT_V1.json`.

---

# 5. Responsibility-action fixtures

Represent one responsibility by, for each history, a nonempty finite optimal-action set `A_star[h]`. The target/loss need not be reconstructed for structural tie tests; separate probability fixtures handle target-derived Bayes actions.

## 5.1 ANY_OPTIMAL_ACTION checker

A state fibre is valid iff

`intersection(A_star[h] for h in fibre)` is nonempty.

For every candidate state partition `Z` refining predictive partition `P`:

1. check fibre validity;
2. enumerate every deterministic valid selector `d(h) in A_star[h]`;
3. compute selector action partitions;
4. under a supplied history distribution compute `H(d(H)|P)`;
5. verify the minimum selector entropy equals the minimum conditional entropy among all valid action-sufficient state partitions.

This independently checks `R21`.

## 5.2 Mandatory tie-overstatement fixture

Two equal-probability histories in one predictive fibre:

```text
A*(h1)={a,b}
A*(h2)={b,c}
```

Expected:

- ANY_OPTIMAL_ACTION: 0-bit extra cost by choosing `b` both histories;
- OPTIMAL_ACTION_SET: 1-bit cost;
- canonical selector `[a,b]`: 1 bit;
- canonical selector `[b,b]`: 0 bits if explicitly registered.

Any different result = `FAIL_TIE_SEMANTICS`.

## 5.3 EXACT_TARGET control

For deterministic target `Q(h)` and zero-one loss, set `A*(h)={Q(h)}`. Verify `R21` reduces exactly to `H(Q|P)`.

## 5.4 Family selector optimization

For `m=2,3` responsibilities with ANY_OPTIMAL_ACTION, enumerate Cartesian product of valid selectors and compute

`min H(d1(H),...,dm(H)|P)`.

Also compute sum of individually minimized selector entropies. Search for a fixture where joint optimization gives a strict saving or where individually chosen minimizers are not jointly minimizing.

If found, freeze smallest witness. If none for registered search space (`n<=6`, actions<=3, m<=3), emit `CANNOT_CHECK_NO_SMALL_JOINT_SELECTOR_WITNESS`; do not state a universal theorem either way.

Output `RESPONSIBILITY_SELECTOR_AUDIT_V1.json`.

---

# 6. Exact probability/entropy grid

Use exact rational probability masses over history supports `n<=5`.

Generate positive probability vectors with common denominators `2..8`; retain vectors summing to 1.

Compute entropies at >=80 decimal digits using one implementation and cross-check at >=50 digits with an independent library/implementation.

Required identities:

- `H(P,C)-H(P)=H(C|P)` for fixed deterministic signatures;
- `H(Q|Z)=H(Q|H)+I(Q;H|Z)` under representation Markov condition;
- `H(Q|S,U)=...` for T8 fixtures;
- prospective identity in section 9.

Tolerance for numerical equality after exact structural conditions: `1e-30` in high precision outputs.

---

# 7. T2 compression mutation battery

Original exact claim: deterministic predictive-sufficient `Z` has `H(Z)>=H(S_P)` and equality implies a.s. isomorphism on positive support.

Mutate one assumption at a time:

1. remove entropy minimality — expected counterexample `Z=(S_P,extra)`;
2. replace exact predictive sufficiency with approximate — expected exact isomorphism failure;
3. allow stochastic `Z` — do not generalize without exact theorem;
4. replace entropy minimality with cardinality minimality — expected deterministic partition corollary that equal minimal block count implies predictive quotient;
5. add zero-mass nominal histories — expected uniqueness only on positive support;
6. allow `H(Z)<=H(S_P)+delta` — search finite lower bounds; no new theorem unless pre-existing statement follows exactly.

Output `T2_ASSUMPTION_ATTACK_MATRIX_V1.json` with smallest counterexample for every failed strengthened form.

---

# 8. Approximate log-loss benchmark

## 8.1 Single target

For deterministic `Q` and exact `S_P`, baseline `h=H(Q|S_P)`.

Distortion ratios:

`{0,.1,.2,...,1}`.

Expected:

`R(D)=max(h-D,0)`.

Use registered reveal/erasure channel. Verify exact/near-exact analytical values. Random channels are only lower-bound sanity tests.

## 8.2 Conditional independent family

Generate `m=2,3` conditionally independent deterministic responsibility variables given `S_P` using latent construction in which histories encode `(S,q1,...,qm)` with product probabilities inside each S fibre.

Normalized distortion grid `{0,.25,.5,.75,1}`.

Expected sum formula. Correlated controls must violate/additional-sharing behavior as appropriate; no additive formula beyond independence.

Output `LOGLOSS_FRONTIER_AUDIT_V1.json` and label all headline formulas `PARENT_OWNED_BENCHMARK`.

---

# 9. Dynamic fixed-policy state checker

## 9.1 Fixture format

Every state machine JSON contains:

- finite `states`;
- finite ordered `alphabet`;
- `base_label[state]` representing `(S_P, fixed registered responsibility policy/risk signature)`;
- explicit transition table for every state/symbol with value either target state or string `UNDEFINED`;
- positive state distribution for entropy reporting.

No missing transition key semantics.

## 9.2 Refinement

Initialize class by `base_label`.

Iterate canonical signatures:

`sig(h)=(base_label(h), class(next(h,x1)) or UNDEFINED, ..., class(next(h,xm)) or UNDEFINED)`.

Reassign canonical restricted-growth class IDs by signature equality. Stop when class assignment unchanged.

Emit every iteration.

## 9.3 Independent coarseness audit

For machines with `|states|<=7`, enumerate all partitions. A partition is admissible iff:

1. it refines base-label equality;
2. equivalent states have matched definedness for every symbol;
3. corresponding successors remain equivalent.

Verify every admissible partition refines the algorithm's stable partition. This checks coarsest right congruence independently.

## 9.4 Canonical dynamic witness

Two current equally likely histories have same base label. Under one future symbol their successors have different base labels.

Expected:

- current state entropy difference beyond base = 0;
- horizon-1/stable split = two classes;
- `C_dyn=1` bit on equal prior.

## 9.5 Negative control

Base partition already right congruent; expected `C_dyn=0`.

Output `DYNAMIC_STATE_AUDIT_V1.json`.

### Critical boundary

This checker validates **fixed-policy** dynamic state only. It does not solve joint policy-selector/state optimization.

---

# 10. Prospective deficiency checker

Construct exact finite joint tables for `(H_now,Z_now,X_future,Q_future)`.

Compute independently:

1. `H(Q_future|Z_now,X_future)-H(Q_future|H_now,X_future)`;
2. `I(Q_future;H_now|Z_now,X_future)`.

Require equality.

Mandatory fixtures:

- provenance witness with positive prospective deficit;
- state retaining provenance, deficit zero;
- future observation independently reveals provenance, deficit zero despite current compression;
- current compression deficit positive but selected future responsibility deficit zero.

Output `PROSPECTIVE_DEFICIENCY_AUDIT_V1.json`.

---

# 11. Universality/bounded responsibility checker

For small predictive partitions:

1. generate responsibility signatures that are constant within predictive fibres — overhead zero;
2. progressively add responsibilities that split predictive fibres;
3. calculate `G(R)=H(C_R|S_P)` for fixed signatures;
4. verify monotonicity for nested families;
5. construct a family separating every positive-support history within each predictive fibre;
6. verify overhead saturates at `H(H|S_P)`;
7. for every non-injective candidate representation, choose a collided positive-mass pair and mechanically construct binary exact target that differs on the pair; verify optimal Z-based 0–1 error positive.

Output `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json`.

---

# 12. Nearest-work metadata/theorem audit

The scientific disposition is pre-decided in `HOSTILE_REVIEW_DECISION_MATRIX_V1.md` and `NEAREST_WORK_PASS_02_DYNAMIC_STATE.md`. Executor only establishes exact bibliographic/theorem facts.

Mandatory parent families:

- Blackwell/statistical sufficiency/Le Cam;
- computational mechanics causal states and recursive calculability;
- PSR;
- Baisero & Amato R-PSR;
- Information Bottleneck and Deterministic Information Bottleneck;
- multi-task information-theoretic sufficient representations;
- Wang et al. CVPR 2022 minimal sufficient contrastive/downstream information loss;
- Subramanian et al. JMLR 2022 Approximate Information State;
- POMDP belief/information states;
- Myhill–Nerode/right congruence/automata minimization;
- log-loss rate distortion / Courtade-Weissman;
- representation identifiability;
- LLM belief/truth/uncertainty internal-state work.

For each source emit:

- verified metadata;
- stable identifier;
- theorem/proposition/definition numbers relevant to #51;
- exact assumptions;
- claim IDs C01–C20 overlapped;
- verdict.

The executor may add a newly found parent but must not write a new defense. A new direct parent is fed through the existing fatality decision rules.

Output `NEAREST_THEOREM_CLAIM_MATRIX_V2.csv` + generated summary.

---

# 13. Manuscript mechanical update

Starting manuscript: `MANUSCRIPT_DRAFT_V2.md`.

Only permitted edits after computation:

- replace candidate theorem labels with checked theorem numbers/status;
- insert exact assumptions forced by formal audit;
- delete/contract claims that fail or are parent-absorbed;
- insert generated theorem/counterexample tables;
- insert verified bibliography;
- convert to JMLR LaTeX if JMLR gates pass;
- correct arithmetic/notation exposed by checkers.

Not permitted without a new scientific issue/successor identity:

- inventing a new theorem to replace a failed load-bearing theorem;
- changing responsibility semantics after seeing favorable/unfavorable computations;
- reframing a parent-owned result as novelty;
- adding empirical LLM claims.

---

# 14. JMLR gate execution

Evaluate `JMLR_SUBMISSION_GATE_V1.md` J1–J8 mechanically against final artifacts where possible.

J1/J2 require the pre-registered hostile reviewer decision matrix plus theorem-parent matrix; do not substitute model self-confidence.

If any gate fails, JMLR submission is not authorized.

---

# 15. Final decision tree

1. Any load-bearing formal theorem false under stated assumptions?
   - if smallest assumption correction preserves scientific identity: update assumption, rerun all checks.
   - otherwise `CANNOT_CHECK_FORMAL_PROOF` / successor issue.
2. Strongest parent or obvious parent composition proves the full static+prospective package and consequence?
   - `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.
3. Only generic representation-identifiability separation survives?
   - `REPRESENTATION_IDENTIFIABILITY_ONLY__NO_NEW_RESIDUAL`.
4. Sound residual exists but JMLR J1/J2 fail significance/breadth?
   - `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`.
5. Sound nontrivial residual + all JMLR gates pass?
   - `THEORY_PAPER_RESIDUAL_SUPPORTED`.

This decision tree is exhaustive for the current research identity.
