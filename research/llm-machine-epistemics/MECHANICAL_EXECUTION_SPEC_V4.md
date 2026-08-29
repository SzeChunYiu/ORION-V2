# Mechanical Execution Spec V4 — Final Authoritative Execution Contract

**Issue:** #51  
**Supersedes:** V1–V3 execution/handoff documents for current task order and expected outputs.  
**Executor role:** theorem checker, exact enumerator, metadata retriever and renderer. **No open-ended scientific thinking is delegated.**

## 0. Canonical scientific inputs

Read:

1. `CURRENT_RESEARCH_STATUS_V3.md`
2. `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V3.md`
3. `papers/llm-machine-epistemics/CLAIM_LEDGER_V3.json`
4. `RESPONSIBILITY_DECISION_QUOTIENT_V2.md`
5. `JOINT_DYNAMIC_STATE_OPTIMIZATION_V1.md`
6. `EPISTEMIC_DEFICIENCY_DECOMPOSITION_V1.md`
7. `RESPONSIBILITY_UNIVERSALITY_BOUND_V1.md`
8. `HOSTILE_REVIEW_DECISION_MATRIX_V1.md`
9. `NEAREST_WORK_PASS_02_DYNAMIC_STATE.md`
10. `papers/llm-machine-epistemics/JMLR_SUBMISSION_GATE_V1.md`

Older documents are provenance unless explicitly cited by one of these.

---

# 1. Formal theorem IDs

## Predictive base
- `L1_PREDICTIVE_SUFFICIENT_REFINES_SP`
- `T2_ENTROPY_MINIMAL_PREDICTIVE_ISOMORPHIC_SP`

## Static responsibility decisions
- `R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY`
- `R22_CANONICAL_ACTION_COST`
- `R23_OPTIMAL_ACTION_SET_COST`
- `R24_ACTION_AND_RISK_COST`
- `R25_EXACT_TARGET_SPECIAL_CASE`
- `R26_JOINT_ANY_OPTIMAL_SELECTOR_COST`
- `R27_ZERO_COST_COMMON_OPTIMAL_ACTION`

## Deficit identities
- `D1_ACQUISITION_COMPRESSION_DECOMPOSITION`
- `D2_NEW_OBSERVATION_GAIN`
- `D3_PROSPECTIVE_DEFICIENCY_IDENTITY`

## Classical approximate benchmarks
- `T8A_SINGLE_LOGLOSS_FRONTIER`
- `T8B_INDEPENDENT_RESPONSIBILITY_FRONTIER`
- `T8C_SHARED_EXACT_STATE_SAVING`
- `T8D_WORST_FIBRE_CARDINALITY`

## Joint dynamic optimization
- `J1_STATIC_PARTITION_SELECTOR_EQUIVALENCE`
- `J2_DYNAMIC_ADMISSIBLE_PARTITION_OPTIMUM`
- `J3_SELECTOR_REFINEMENT_DYNAMIC_OPTIMUM_EQUIVALENCE`
- `J4_OPTIONALITY_PREMIUM_NONNEGATIVE`
- `J5_CANONICAL_ONE_BIT_PREMIUM`

## Universality
- `U1_RESPONSIBILITY_OVERHEAD_BOUND`
- `U2_FIBRE_SEPARATING_SATURATION`
- `U3_UNRESTRICTED_RESPONSIBILITY_FULL_HISTORY`
- `U4_NONINJECTIVE_FAILING_BINARY_RESPONSIBILITY`
- `U5_RESPONSIBILITY_FAMILY_MONOTONICITY`

No additional load-bearing theorem ID may be created by the executor.

---

# 2. Exact finite structural model

Use finite history states `H={0,...,n-1}`.

Required primitive data:

- predictive partition `P` represented by restricted-growth-string class IDs;
- input alphabet `X={0,...,m-1}`;
- deterministic partial transition `delta[h][x]` with explicit `UNDEFINED`;
- optimal-action set `A_star[h]` as nonempty subset of finite action alphabet;
- positive rational probability `p[h]`.

All partition comparisons are up to canonical restricted-growth relabelling.

---

# 3. Bell-complete partition generation

Enumerate all partitions for `n<=6`; attempt n=7 if practical.

Reference Bell numbers:

`1,2,5,15,52,203,877` for n=1..7.

Abort structural result generation if counts mismatch.

Output `PARTITION_ENUMERATION_RECEIPT_V1.json`.

---

# 4. Static action-compatible optimization

A partition `Pi` is static admissible iff:

1. it refines predictive partition `P`;
2. for every block B, `intersection_{h in B} A_star[h]` is nonempty.

Compute exactly:

`C_stat_star = min H(Pi(H)|P)`

over static-admissible partitions.

Independently enumerate every Bayes-optimal selector `d(h) in A_star[h]` and compute

`min H(d(H)|P)`.

Required equality: `J1`.

### Tie fixture

Two equal-probability histories, one predictive fibre:

- `A*(h0)={a,b}`
- `A*(h1)={b,c}`

Expected:

- `C_stat_star=0` under ANY_OPTIMAL_ACTION;
- min selector action `b,b`;
- full option-set signature cost=1 bit;
- exact target/full distinct labels cost=1 bit if target distinguishes histories.

Output `STATIC_RESPONSIBILITY_OPTIMIZATION_V1.json`.

---

# 5. Dynamic action-compatible optimization

A static-admissible partition is dynamically admissible iff for every two states in a block and every input:

- transition definedness matches;
- when defined, successors occupy the same partition block.

Compute

`C_dyn_star = min H(Pi(H)|P)`

over dynamic-admissible partitions.

Verify implementation equivalence:

- each dynamic partition supports a common optimal action per block and deterministic next-state function;
- every deterministic recurrent state with optimal-action decoder induces a dynamic-admissible partition.

This checks `J2`.

Output `DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json`.

---

# 6. Independent selector-refinement route

For every Bayes-optimal selector `d`:

1. form base label `(P(h),d(h))`;
2. repeatedly refine by transition successor class signatures until stable;
3. compute `H(S_inf^d|P)`.

Take minimum over selectors.

Required exact equality:

`min_d H(S_inf^d|P) == C_dyn_star`.

This checks `J3` independently of direct dynamic-partition enumeration.

Output `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json`.

---

# 7. Dynamic optionality premium

Compute

`Omega_dyn = C_dyn_star - C_stat_star`.

Verify `Omega_dyn >= 0` for every enumerated fixture (`J4`).

## Canonical one-bit fixture

Current states h0,h1 equally likely:

- same predictive P block;
- unique current optimal action `{a}` for each;
- input `x` sends them to successor histories s0,s1;
- s0 unique optimal action `{b0}`;
- s1 unique optimal action `{b1}`, b0 != b1.

Expected:

- `C_stat_star=0`;
- no dynamically admissible merge of h0/h1;
- `C_dyn_star=1 bit`;
- `Omega_dyn=1 bit`.

This checks `J5` and proves premium is not tie-policy artefact.

## Tie-sensitive search

Enumerate `n<=7`, action alphabet<=3 for a case where two valid current selectors induce different dynamic costs. If found, freeze smallest witness. If absent, return `CANNOT_CHECK_NO_SMALL_TIE_DYNAMIC_WITNESS`; no theorem of selector irrelevance.

---

# 8. Probability/entropy implementation

Use exact rational input probabilities with denominator grids 2..8, positive support only.

Structural conditions are exact. Entropies:

- implementation A >=80 decimal digits;
- independent implementation B >=50 digits;
- agreement tolerance 1e-30.

For deterministic partition `Pi` refining P:

`H(Pi|P) = H(Pi)-H(P)`.

Output all raw rational distributions used in headline fixtures.

---

# 9. Predictive-compression mutation battery

Original exact deterministic theorem only.

Mutations:

1. no entropy minimality;
2. approximate predictive sufficiency;
3. stochastic representation;
4. cardinality rather than entropy minimality;
5. zero-mass nominal histories;
6. near-minimal entropy `H(Z)<=H(S_P)+delta`.

Find smallest counterexample or exact corollary under each. Do not formulate new approximate theorem after seeing results.

Output `PREDICTIVE_COMPRESSION_ASSUMPTION_MATRIX_V1.json`.

---

# 10. Deficit identities

Using finite exact joint probability tables independently compute:

- `H(Q|Z)-H(Q|H)` and `I(Q;H|Z)`;
- `H(Q|H)-H(Q|H,X)` and `I(Q;X|H)`;
- `H(Qf|Zt,Xf)-H(Qf|Ht,Xf)` and `I(Qf;Ht|Zt,Xf)`.

Mandatory controls:

1. acquisition deficit only;
2. compression deficit only;
3. prospective deficit only (canonical provenance case);
4. future observation fully reconstructs forgotten provenance => prospective deficit zero;
5. state retains provenance => prospective deficit zero.

Output `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json`.

---

# 11. Approximate log-loss benchmark

Use the registered reveal/erasure construction for deterministic exact target Q.

Verify at distortion ratios 0..1 in increments .1:

`R(D)=max(H(Q|P)-D,0)`.

For conditionally independent Q_i given P, verify product sum at normalized distortion grid `{0,.25,.5,.75,1}`.

Correlated controls:

- Q2=Q1;
- Q1 deterministic function of Q2;
- partially correlated pair;
- independent pair.

No independent novelty credit in output.

Output `LOGLOSS_PARENT_BENCHMARK_V1.json`.

---

# 12. Universality checker

## U1
For every fixed-signature responsibility family:

`0 <= H(C_R|P) <= H(H|P)`.

## U2
Generate families that separate every history pair within predictive fibres. Verify

`H(H|P,C_R)=0`
and
`H(C_R|P)=H(H|P)`.

## U3/U4
For every non-injective candidate representation partition Z:

- select smallest positive-mass collided history pair;
- construct binary exact target differing on pair;
- compute best Z-based 0–1 Bayes error;
- verify positive error and full-history zero error.

## U5
For nested responsibility families verify monotonic fixed-signature overhead.

Output `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json`.

---

# 13. Formal proof stack

Preferred:

1. Lean 4 + Mathlib;
2. Isabelle/HOL;
3. Coq;
4. split structural theorem prover + two independent exact entropy checkers if needed.

All proof assumptions serialized in `FORMAL_THEOREM_LEDGER_V2.json`.

For J1–J5, theorem prover may prove finite partition equivalences while brute-force enumeration independently tests all registered small instances.

---

# 14. Parent theorem matrix

Mandatory parent search now additionally includes:

- incompletely specified finite-state machine minimization;
- compatible states / closed covers;
- exact binate-cover formulations;
- incomplete Moore/Mealy minimization complexity.

Previously frozen parents remain mandatory:

- Blackwell/sufficiency;
- causal states;
- PSR/R-PSR;
- IB/DIB;
- multi-task sufficient representation;
- minimal contrastive sufficiency/downstream-task loss;
- Approximate Information State JMLR 2022;
- POMDP belief/information states;
- right congruence/Myhill–Nerode;
- log-loss RD;
- representation identifiability;
- LLM belief/truth/uncertainty work.

For each source return exact theorem/definition IDs, assumptions, and overlaps with `CLAIM_LEDGER_V3.json` C01–C18.

No novelty defense is delegated.

Output `NEAREST_THEOREM_CLAIM_MATRIX_V3.csv`.

---

# 15. Manuscript update contract

Starting manuscript: `MANUSCRIPT_DRAFT_V3.md`.

Allowed only:

- replace candidate theorem labels with checked status/numbers;
- insert assumptions forced by formalization;
- delete failed/parent-absorbed claims;
- insert generated tables/figures;
- verify/insert bibliography;
- convert to JMLR format if J1–J8 gate passes.

Forbidden:

- new theorem family;
- new responsibility semantics;
- post-result novelty rescue;
- empirical LLM claims;
- changing finite fixture definitions because outcomes are inconvenient.

---

# 16. Final terminal logic

1. Load-bearing theorem false beyond scope-preserving assumption repair -> `CANNOT_CHECK_FORMAL_PROOF` or successor issue.
2. Parent product owns full static+dynamic package/consequence -> `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.
3. Only generic representation-identifiability result survives -> `REPRESENTATION_IDENTIFIABILITY_ONLY__NO_NEW_RESIDUAL`.
4. Sound residual but JMLR significance/breadth fails -> `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`.
5. Sound nontrivial residual and every JMLR gate passes -> `THEORY_PAPER_RESIDUAL_SUPPORTED`.

No other terminal.
