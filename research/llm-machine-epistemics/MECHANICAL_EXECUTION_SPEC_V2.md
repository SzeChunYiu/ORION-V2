# Mechanical Execution Spec V2

**Issue:** #51  
**Purpose:** remove discretionary scientific design from the next execution session. The next AI should run these checks exactly, report PASS/FAIL/counterexamples, and make only theorem-scope edits forced by mechanical findings.

The scientific concepts, theorem identities, counterexamples, publication criteria and parent boundaries are already specified in:

- `THEORY_V1.md`
- `THEORY_STRENGTHENING_V2.md`
- `EPISTEMIC_DEFICIENCY_DECOMPOSITION_V1.md`
- `NEAREST_WORK_AND_NOVELTY_V1.md`
- `INTERNAL_PARENT_ALIGNMENT_V1.md`

No new theorem family should be invented during execution unless a checker falsifies a registered statement and the smallest valid repair is uniquely determined.

---

# A. Formal proof contract

## A1. Required theorem identifiers

The proof package must contain exact named counterparts for:

- `L1_predictive_sufficient_refines_SP`
- `T1_predictive_epistemic_separation`
- `T2_entropy_minimal_predictive_isomorphic_SP`
- `T3_exact_deterministic_overhead`
- `T4_logloss_deficiency_identity`
- `T5_postprocessing_monotonicity`
- `T6_external_observation_gain`
- `T7_responsibility_refinement`
- `T8A_exact_logloss_frontier`
- `T8B_independent_responsibility_frontier`
- `T8D_cardinality_overhead`
- `T10_horizon_refinement_monotonicity`
- `T11_coarsest_right_congruent_refinement`
- `T12_recursive_implementability`
- `T13_static_zero_dynamic_positive_witness`
- `D1_acquisition_compression_decomposition`
- `D2_prospective_deficiency_identity`

If a theorem cannot be stated exactly in the chosen formal system, the artifact must emit `CANNOT_CHECK_FORMALIZATION_GAP` with the exact unsupported construct.

## A2. Preferred proof stack

Try in this order:

1. Lean 4 + Mathlib;
2. Isabelle/HOL;
3. Coq;
4. if all are impractical for the entropy layer, use one theorem prover for partition/right-congruence results and a second independently implemented symbolic checker for finite information identities.

No single Python script checking its own generated fixtures counts as independent proof of a headline theorem.

## A3. Assumption ledger

For every theorem emit:

| field | required content |
|---|---|
| theorem_id | exact id above |
| finite_support | yes/no |
| deterministic_encoder | yes/no |
| deterministic_Q | yes/no |
| stochastic_augmentation_allowed | yes/no |
| positive_support_requirement | exact statement |
| exact_predictive_sufficiency | yes/no |
| exact_responsibility_recovery | yes/no |
| entropy_finiteness | yes/no |
| transition_totality | total/partial with semantics |
| result | PASS/FAIL/CANNOT_CHECK |
| smallest_counterexample | pointer or null |

No assumption may exist only in proof code.

---

# B. Exact finite countermodel enumerator

## B1. Structural enumeration

Enumerate history sets of size

`n = 2,3,4,5,6`.

Enumerate all set partitions of the history set as candidate:

- predictive partition `P`;
- deterministic responsibility partition `Q`;
- deterministic representation partition `Z`.

Use canonical restricted-growth-string enumeration so every partition occurs exactly once.

For structural theorems, the actual future distribution is represented by the predictive partition: histories in one `P` block are declared to have the same full-future law and histories in different blocks distinct laws. This is sufficient for exact partition/refinement statements and avoids fake numerical distinctions.

### Checks per triple `(P,Q,Z)`

1. `Z` is predictive-sufficient iff every `Z` block lies inside one `P` block.
2. `Z` is exact-Q-sufficient iff every `Z` block lies inside one `Q` block.
3. verify every predictive-sufficient `Z` refines `P`.
4. identify `P∨Q` as the common refinement.
5. verify minimum state cardinality among joint-sufficient partitions equals number of blocks in `P∨Q`.
6. find smallest witnesses where `P` is not `Q`-sufficient.
7. find zero-overhead controls where `Q` is coarser than/equal to `P`.

### Required exact counts

The enumerator must print the Bell-number count of partitions at each `n` and compare against a hard-coded independent Bell-number reference for `n<=6`.

---

# C. Probability/entropy fixture grid

Structural enumeration is separate from information values.

Use positive rational distributions over `n<=5` history states from denominator grids:

- denominator 2, 3, 4, 5, 6;
- retain only vectors with all enumerated support entries positive and exact sum 1.

Represent probabilities as exact rational fractions. Entropies may be emitted numerically at >=80 decimal digits, but structural equalities should be verified algebraically before evaluating logs.

For every selected `(P,Q)`:

1. compute `H(P)`;
2. compute `H(Q|P)`;
3. compute `H(P,Q)`;
4. verify `H(P,Q)-H(P)=H(Q|P)`;
5. compute `k_s` per predictive block;
6. verify joint-state block count `sum_s k_s`;
7. verify augmentation alphabet lower bound `max_s k_s` by brute-force label assignments for small cases.

---

# D. T2 assumption mutation battery

Start from the exact T2 statement. Mutate **one assumption at a time**.

## D1 — remove entropy minimality
Expected: counterexample exists (`Z=(S_P,Q)` can preserve Q while remaining predictive-sufficient).

## D2 — replace exact sufficiency by approximate prediction
Expected: original exact isomorphism conclusion no longer follows. Emit smallest numerical counterexample rather than repairing it ad hoc.

## D3 — allow stochastic `Z`
Question to check mechanically: equality/minimality conditions may require reformulation in mutual-information rather than entropy terms. Do not generalize the theorem unless the formal result is exact.

## D4 — cardinality-minimal rather than entropy-minimal
Verify whether every cardinality-minimal predictive sufficient partition is isomorphic to `S_P` in the deterministic finite partition model. Expected: yes, because the predictive quotient has the minimum number of blocks and any equal-block refinement must coincide. Record as a separate corollary if checker confirms.

## D5 — zero-mass nominal histories
Expected: uniqueness only on support. Counterexamples involving zero-mass states must lead to `almost surely/on positive support` wording, not theorem rejection.

Output: `T2_ASSUMPTION_ATTACK_MATRIX_V1.json`.

---

# E. Exact T8 benchmark

## E1 — single responsibility

For every finite fixture with deterministic `Q`:

- baseline entropy `h = H(Q|S)`;
- distortion grid `D/h in {0, 0.1, ..., 1}` when `h>0`;
- expected frontier `R=h-D`.

Construct the registered erasure channel exactly at every grid point.

Verify:

- achieved `H(Q|S,U)=D`;
- achieved `I(H;U|S)=h-D`;
- random alternative channels never violate the analytical lower bound beyond numerical tolerance.

The random-channel sweep is sanity evidence only; the theorem proof carries authority.

## E2 — independent responsibilities

Generate fixtures where `Q_1,...,Q_m` are conditionally independent given `S`, `m=2,3`.

For coordinate distortions use product grid `{0,.25,.5,.75,1}` of normalized entropy.

Expected exact value:

`sum_i max(H(Q_i|S)-D_i,0)`.

Construct independent erasure encoders; verify coordinate entropies and total conditional rate.

## E3 — correlated controls

Include:

1. identical responsibilities `Q_2=Q_1`;
2. nested responsibility `Q_1=g(Q_2)`;
3. partially correlated binary pair;
4. independent pair.

Purpose: demonstrate that additive cost is valid only under conditional independence and that shared responsibility state can reduce cost.

No executor may extrapolate the independent formula to correlated cases.

---

# F. Dynamic right-congruence / optionality checker

## F1 — finite machine input format

A fixture is JSON:

```json
{
  "states": ["h0", "h1"],
  "alphabet": ["x"],
  "base_label": {"h0": "b0", "h1": "b0"},
  "transition": {"h0": {"x": "h0x"}, "h1": {"x": "h1x"}},
  "probability": {"h0": 0.5, "h1": 0.5}
}
```

The full fixture must include all successor states in `states` or use an explicitly layered finite horizon format. Undefined transitions are represented explicitly, never by missing-key ambiguity.

## F2 — partition refinement algorithm

Initialize class id from `base_label`.

Repeatedly compute canonical signature

`signature(h) = (base_label(h), successor_class_or_UNDEFINED for each alphabet symbol in fixed order)`.

Canonicalize equal signatures to equal new class ids.

Stop when the partition is unchanged.

Emit:

- class assignment for every iteration;
- number of blocks per iteration;
- entropy per iteration under the registered state distribution;
- stabilization iteration;
- stable signatures.

## F3 — independent coarseness check

For `|states|<=7`, enumerate every set partition and select those that:

1. refine the base-label partition;
2. are right congruences for the registered transition system.

Verify every valid candidate partition refines the algorithm's stable partition. This independently checks the “coarsest right-congruent refinement” claim.

## F4 — canonical T13 witness

Fixture must yield:

- `|S_0|=1` on current states `h0,h1`;
- equal current predictive/responsibility label;
- horizon-1 partition separates them;
- equal prior entropy `H(S_0)=0` bits;
- required horizon state entropy `H(S_1)=1` bit;
- optionality cost `1` bit.

Any different result is `FAIL_CANONICAL_DYNAMIC_WITNESS`.

## F5 — zero-dynamic-overhead control

Include a system whose base-label partition is already right congruent. Expected stable partition equals base partition exactly and `C_dyn=0`.

---

# G. Prospective deficiency checker

For a finite sequential probability model, compute directly:

`Delta_k = H(Q_future | Z_now, X_future) - H(Q_future | H_now, X_future)`.

Also compute conditional mutual information independently from the joint table:

`I(Q_future; H_now | Z_now, X_future)`.

Require equality to 1e-12 in ordinary double implementation and tighter in arbitrary precision.

Fixtures:

1. dynamic one-bit provenance witness: expected positive `Delta_1`;
2. state retaining provenance bit: expected zero `Delta_1`;
3. future observation itself reveals provenance fully: expected zero `Delta_1` even if current state discarded it;
4. current responsibility differs but no future need: current compression deficit positive, prospective selected future deficit may be zero.

These controls distinguish current loss from future-option loss.

---

# H. Bibliographic theorem matrix — mechanical search protocol

Search strings are frozen in `COMPUTE_HANDOFF_V1.md`. Add these dynamic terms:

- `right congruence sufficient statistic sequential update`
- `Myhill Nerode predictive state sufficient statistic`
- `minimal recursively updateable sufficient statistic`
- `dynamic sufficient statistic future tasks`
- `causal state recursive calculability`
- `reward predictive state minimal`
- `belief state sufficient statistic future decision`
- `provenance future belief revision state`
- `information state control sufficient statistic`

For every source, the executor records theorem ownership; it does not write novelty prose beyond the registered verdict categories.

Required direct-parent checks now include:

- Shalizi–Crutchfield causal-state recursive calculability/minimality;
- Myhill–Nerode/right-congruence automata theory;
- PSR and R-PSR reward sufficiency;
- deterministic information bottleneck;
- multi-task sufficient representation;
- conditional/multiterminal log-loss rate-distortion.

---

# I. Final deterministic terminal logic

After all mechanical outputs exist, assign the paper terminal by this exact decision tree.

1. **Any T2/T3/T10–T13 headline theorem formally false under its manuscript assumptions?**
   - yes → `CANNOT_CHECK_FORMAL_PROOF` unless the smallest assumption correction preserves the same scientific question; otherwise open successor identity.
2. **Strongest-parent theorem matrix contains one existing construction proving the full static + dynamic result with the same interpretation/consequence?**
   - yes → `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.
3. **Static results survive but dynamic optionality theorem/interpretation is parent-owned and no stronger residual remains?**
   - yes → assess field-theory viability; JMLR gate fails.
4. **Static + dynamic theorem package survives as a real residual but approximate frontier is entirely classical?**
   - keep T8 as background benchmark, not novelty; JMLR remains possible only if dynamic theorem significance is strong under hostile review.
5. **Residual sound but editor simulation rates significance below JMLR threshold?**
   - `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`.
6. Otherwise → `THEORY_PAPER_RESIDUAL_SUPPORTED` pending actual manuscript/submission audit.

The execution AI has no discretion to declare “promising” instead of selecting one of these outcomes.
