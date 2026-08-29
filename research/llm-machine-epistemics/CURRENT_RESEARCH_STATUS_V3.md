# Current Research Status V3 — Theory/Planning Complete, Mechanical Execution Only

**Issue:** #51  
**Branch:** `research/llm-epistemic-sufficiency-theory-20260829`  
**Supersedes:** `CURRENT_RESEARCH_STATUS_V1.md` and `CURRENT_RESEARCH_STATUS_V2.md`.

## Governing paper question

> **Starting from a state sufficient for the complete linguistic future, what is the minimum additional state required to fulfill a declared epistemic decision responsibility now, what further state is required for some Bayes-optimal responsibility policy to remain recursively implementable under future observations, and how do these costs depend on the declared responsibility family and horizon?**

Working title:

> **Beyond Predictive Sufficiency: Static and Prospective Epistemic State Requirements for Autoregressive Models**

Canonical manuscript: `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V3.md`.

## Status summary

```text
OPEN_ENDED_SCIENTIFIC_PLANNING = COMPLETE
RESPONSIBILITY_SEMANTICS = COMPLETE
STATIC_THEORY = COMPLETE_AS_CANDIDATE
JOINT_DYNAMIC_THEORY = COMPLETE_AS_CANDIDATE
APPROXIMATE_BENCHMARK_THEORY = COMPLETE_AND_PARENT_ATTRIBUTED
UNIVERSALITY_BOUNDARY = COMPLETE_AS_CANDIDATE
HOSTILE_REVIEW_RESPONSES = PRE_REGISTERED
NEAREST_PARENT_THREATS = IDENTIFIED
MANUSCRIPT_ARGUMENT = WRITTEN
CLAIM_LEDGER = WRITTEN
JMLR_GATE = WRITTEN
MECHANICAL_EXECUTION_SPEC = FINAL_V4
REMAINING_WORK = PROOF_ENUMERATION_METADATA_RENDERING
```

No scientific invention is delegated to the next AI.

---

# 1. Final responsibility semantics

Responsibility contract:

`r=(Q, actions, loss, semantics)`.

Exact semantics:

- `ANY_OPTIMAL_ACTION`
- `CANONICAL_ACTION`
- `OPTIMAL_ACTION_SET`
- `ACTION_AND_RISK`
- `EXACT_TARGET`

For `ANY_OPTIMAL_ACTION`, with `A*(h)` the Bayes-optimal action set and `D` all valid selectors `d(h) in A*(h)`, the exact current-state cost beyond `S_P` is

\[
\boxed{
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}
H(d(H)\mid S_P)
}
\]

and is equivalently the minimum entropy of a predictive-refining partition whose every block has a common optimal action.

This corrects the older over-strong assumption that preserving the complete optimal-action set is always required.

Exact target recovery remains the special case `H(Q|S_P)`.

---

# 2. Final joint dynamic theory

No arbitrary fixed tie policy is required in the main dynamic quantity.

A partition is **static admissible** iff:

1. it refines `S_P`;
2. every block has nonempty intersection of Bayes-optimal action sets.

A partition is **dynamic admissible** iff it is static admissible and a right congruence for the registered observation/history transition system.

Define

\[
C_{\mathrm{stat}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{stat}}}
H(\Pi(H)\mid S_P),
\]

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

The candidate theorem package establishes:

1. static partition optimum equals minimum Bayes-selector action entropy;
2. dynamic-admissible partitions are exactly deterministic recurrent states with a Bayes-optimal action decoder under the finite exact setup;
3. dynamic optimum equals

   \[
   \min_{d\in\mathcal D}H(S_\infty^d\mid S_P),
   \]

   where `S_inf^d` is the coarsest right-congruent refinement of `(S_P,d)`;
4. therefore policy tie selection and recurrent-state minimization are jointly optimized.

Define the central dynamic quantity

\[
\boxed{
\Omega_{\mathrm{dyn}}
=
C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*
\ge0.
}
\]

This is the **dynamic epistemic optionality premium**.

Canonical equal-prior witness:

```text
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
```

because current histories share a unique optimal action but one future observation leads to successor histories with disjoint unique optimal actions.

This witness is not an artefact of arbitrary tie-breaking.

---

# 3. Classical parent ownership of dynamic substrate

The executor/reviewer must grant ownership to classical incompletely specified FSM minimization and related automata theory for:

- compatible states;
- non-transitive compatibility under incomplete outputs;
- closed compatible covers / state reduction;
- right-congruence/state-transition consistency;
- non-uniqueness and computational difficulty of exact minimization.

The current paper does **not** claim a new finite-state minimization algorithm.

The possible residual is:

- predictive state `S_P` as explicit linguistic base;
- Bayes-optimal epistemic action compatibility as the output constraint;
- conditional entropy/state-rate rather than only number-of-states cost;
- static-versus-dynamic minimum difference `Omega_dyn`;
- its interpretation as future epistemic revision optionality;
- resulting LLM representation evaluation criterion.

This remains under severe parent pressure from ISFSM minimization plus Approximate Information State/POMDP theory.

---

# 4. Other completed theory

## Predictive compression

Parent-owned exact minimality is used only for consequence:

> compression all the way to `S_P` is responsibility-safe iff a valid responsibility policy is implementable from `S_P`.

No claim that ordinary language-model training actually produces `S_P`.

## Deficits

- acquisition: `H(Q|H)`;
- current compression: `I(Q;H|Z)`;
- prospective: `I(Q_future;H_now|Z_now,X_future)`.

Information identities are parent-owned; typed intervention interpretation is supporting framework.

## Approximate benchmark

`[H(Q|S_P)-D]_+` under log loss plus product-source extensions are classical rate-distortion benchmarks only.

## Bounded responsibility

- responsibility-family cost <= `H(H|S_P)`;
- fibre-separating family saturates this bound;
- every non-injective state fails a constructed exact binary responsibility;
- unrestricted exact responsibility universality therefore removes nontrivial compression.

Likely classical/no-free-lunch corollaries; used as framework boundary.

---

# 5. Parent concessions frozen

The next AI may not upgrade these:

```text
S_P / causal-state minimality = PARENT_OWNED
prediction versus secondary target = PARENT_OWNED_PATTERN
minimal target state losing downstream info = PARENT_OWNED_PATTERN
DIB / task-sufficient compression = PARENT_OWNED AREA
multi-task sufficient representation = PARENT_OWNED AREA
Blackwell/Bayes-risk information ordering = PARENT_OWNED
conditional MI identities = PARENT_OWNED
log-loss RD = PARENT_OWNED
POMDP/information-state recurrent sufficiency = STRONG PARENT
Approximate Information State JMLR 2022 = STRONG DIRECT PARENT
right congruence / automata minimization = PARENT_OWNED
incompletely specified FSM compatible-state minimization = STRONG ALGORITHMIC PARENT
representation identifiability = PARENT_OWNED AREA
```

---

# 6. Strongest candidate residual

The paper's standalone identity survives only if the following combination is not already an immediate parent product:

1. exact state cost relative to **registered epistemic decision semantics** beyond a complete-linguistic predictive quotient;
2. joint optimization of tied Bayes-optimal policy and recurrent state under a responsibility process;
3. dynamic optionality premium `Omega_dyn` comparing optimal static versus optimal recurrent responsibility state;
4. bounded responsibility-family/horizon law;
5. LLM representation evaluation implication: predictive performance and static epistemic probes do not certify prospective revision adequacy.

The mathematics underlying each component may individually be classical. JMLR requires the **combined analytical framework/consequence** to be materially non-obvious and useful.

---

# 7. Publication thinking complete

Canonical files:

- `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V3.md`
- `papers/llm-machine-epistemics/CLAIM_LEDGER_V3.json`
- `papers/llm-machine-epistemics/JMLR_SUBMISSION_GATE_V1.md`
- `HOSTILE_REVIEW_DECISION_MATRIX_V1.md`
- `NEAREST_WORK_PASS_02_DYNAMIC_STATE.md`
- `INTERNAL_PARENT_ALIGNMENT_V1.md`

JMLR is high-risk. No submission until J1–J8 pass.

---

# 8. Remaining work is mechanical

Authoritative contract:

`MECHANICAL_EXECUTION_SPEC_V4.md`.

The executor only:

- formal-checks registered theorem IDs;
- enumerates partitions/selectors;
- computes entropy exactly/high precision;
- runs assumption mutation countermodels;
- verifies direct static/dynamic minima two ways;
- verifies one-bit premium witness;
- searches tie-sensitive finite witnesses;
- checks deficit identities;
- checks universality constructions;
- retrieves/deduplicates bibliography metadata;
- locates exact parent theorem numbers;
- generates result tables;
- deletes/contracts claims mechanically forced to fail/parent-owned;
- applies deterministic terminal logic.

It does not:

- invent a theorem;
- alter responsibility semantics;
- choose a novelty argument;
- redesign manuscript narrative;
- add LLM empirical claims;
- rescue a failed theorem under the same identity.

---

# 9. Final mechanical checklist

## Formal
- [ ] L1, T2.
- [ ] R21–R27.
- [ ] D1–D3.
- [ ] T8A–T8D.
- [ ] J1–J5.
- [ ] U1–U5.

## Enumerative
- [ ] Bell-complete partition generation n<=6, n=7 if tractable.
- [ ] static action-compatible partition minimum.
- [ ] selector minimum equality.
- [ ] dynamic right-congruent minimum.
- [ ] selector-refinement dynamic minimum equality.
- [ ] canonical one-bit premium.
- [ ] tie-sensitive dynamic selector witness search.
- [ ] predictive-compression assumption attacks.
- [ ] bounded-responsibility saturation.

## Bibliographic
- [ ] exact metadata/theorem locations for all frozen parents including ISFSM minimization.
- [ ] claim matrix against C01–C18 in Claim Ledger V3.
- [ ] frozen missing-parent searches.

## Manuscript
- [ ] theorem status/numbers inserted.
- [ ] failed claims deleted.
- [ ] parent-owned claims demoted.
- [ ] verified refs inserted.
- [ ] generated tables inserted.
- [ ] JMLR format only if J1–J8 pass.

---

# 10. Deterministic terminal

Exactly one:

- `THEORY_PAPER_RESIDUAL_SUPPORTED`
- `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`
- `REPRESENTATION_IDENTIFIABILITY_ONLY__NO_NEW_RESIDUAL`
- `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`
- `CANNOT_CHECK_FORMAL_PROOF`

The research/planning handoff is now closed. Remaining uncertainty is intentionally resolved by proof, enumeration and parent-theorem evidence rather than further design discussion.
