# Current Research Status V4 — Scientific Thinking Closed, Mechanical Verification Pending

**Issue:** #51  
**Branch:** `research/llm-epistemic-sufficiency-theory-20260829`  
**Canonical status:** this file supersedes V1–V3 status files.

## Final governing question

> **Starting from a state sufficient for the complete linguistic future, what is the minimum additional state required by a declared cross-channel epistemic decision responsibility, what further state is required for some Bayes-optimal responsibility policy to remain recursively implementable under future observations, and how do these costs vary with responsibility family and horizon?**

Working manuscript:

> **Beyond Predictive Sufficiency: Cross-Channel and Prospective Epistemic State for Autoregressive Models**

Canonical manuscript: `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V4.md`.

## Handoff status

```text
SCIENTIFIC_QUESTION = FROZEN
RESPONSIBILITY_SEMANTICS = FROZEN
STATIC_STATE_THEORY = SPECIFIED
JOINT_DYNAMIC_OPTIMIZATION = SPECIFIED
PHASE_HORIZON_THEORY = SPECIFIED
DEFICIT_DECOMPOSITION = SPECIFIED
UNIVERSALITY_BOUNDARY = SPECIFIED
MAJOR_PARENT_THREATS = SCIENTIFICALLY_ADJUDICATED
HOSTILE_REVIEW_RESPONSES = PRE_REGISTERED
MANUSCRIPT = WRITTEN
CLAIM_LEDGER = WRITTEN
JMLR_GATE = FROZEN
COMPUTE_ALGORITHMS = FROZEN
NEXT_AI_ROLE = MECHANICAL_EXECUTOR_ONLY
```

---

# 1. Final theoretical structure

## 1.1 Linguistic predictive base

`S_P` is the minimal complete-linguistic-future predictive state. This is parent-owned causal/predictive-state theory.

## 1.2 Decisional-state parent control

Brodu 2011 directly owns utility-defined decision states over causal states and discrete decisional complexity.

Therefore:

- if a responsibility's Bayes-optimal action can be implemented as a function of `S_P`, exact extra static state cost is zero;
- positive state cost is meaningful only for a **cross-channel** responsibility whose optimal decision depends on history/world variables not measurable from the linguistic predictive state.

“Cross-channel” means non-measurable from `S_P`, not statistical independence.

## 1.3 Static exact cost under ANY_OPTIMAL_ACTION

For Bayes-optimal action sets `A*(h)` and valid selectors `d(h) in A*(h)`:

\[
\boxed{
C_{\mathrm{stat}}^*
=
\min_d H(d(H)\mid S_P)
}
\]

Equivalently minimize entropy over predictive-refining state partitions whose every block admits a common optimal action.

Other exact responsibility semantics remain:

- canonical action;
- full optimal-action set;
- action+risk;
- exact target.

## 1.4 Joint dynamic exact cost

A dynamic state partition is static action-compatible plus right-congruent under future observations.

\[
\boxed{
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P)
}
\]

and equivalently

\[
\boxed{
C_{\mathrm{dyn}}^*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_P)
}
\]

where `S_inf^d` is the coarsest right-congruent refinement of `(S_P,d)`.

This closes joint optimization of tied Bayes action selection and deterministic recurrent state in the finite exact partition model.

The compatible-state/right-congruence substrate is strongly parent-owned by incompletely specified FSM minimization and automata/information-state theory.

## 1.5 Dynamic optionality premium

\[
\boxed{
\Omega_{\mathrm{dyn}}
=C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*
\ge0
}
\]

Canonical provenance witness:

```text
C_stat^* = 0 bits
C_dyn^* = 1 bit
Omega_dyn = 1 bit
```

This witness is insensitive to current tie optimization because the current optimal action is unique.

---

# 2. Final state phases

## P0 — predictive-decisional

```text
C0=0
Omega_dyn=0
```

The linguistic predictive state already supports current and future registered responsibility process. Brodu-like regime / mandatory no-extra-state control.

## P1 — static cross-channel refinement

```text
C0>0
Omega_dyn=0
```

Additional history-side state is needed for current epistemic decision, but the optimal current state is already recursively adequate.

## P2 — prospective refinement

```text
Omega_dyn>0
```

Even optimal current responsibility compression loses future revision capability.

P2 can occur with zero or positive static cost.

## Acquisition pre-gate

If target/responsibility information is not identifiable from full accessible history, the principal failure is acquisition/non-identifiability rather than state compression.

---

# 3. Horizon curve

For k-horizon admissible partitions define

\[
C_k^*
=
\min H(\Pi(H)\mid S_P).
\]

Registered candidate law:

\[
C_0^*\le C_1^*\le\cdots\le C_\infty^*.
\]

Define

\[
\Omega_k=C_k^*-C_0^*.
\]

Finite fixtures stabilize. Compute

\[
K_{\mathrm{epi}}
=
\min\{k:C_k^*=C_\infty^*\}.
\]

This is a finite-system responsibility memory horizon, not a universal cognitive constant.

---

# 4. Supporting theory completed

- acquisition deficit `H(Q|H)`;
- compression deficit `I(Q;H|Z)`;
- prospective deficit `I(Q_future;H_now|Z_now,X_future)`;
- log-loss rate frontiers as parent-owned benchmark;
- responsibility-family overhead <= `H(H|S_P)`;
- fibre-separating families saturate non-predictive history;
- every non-injective state fails some exact constructed binary responsibility;
- unrestricted exact responsibility universality therefore implies history-recoverable state.

---

# 5. Strong parent concessions frozen

Do not re-open these for novelty during mechanical execution:

```text
minimal causal/predictive state = PARENT_OWNED
Brodu causal->decisional states + decisional complexity = DIRECT PARENT
prediction state missing reward/secondary target = R-PSR PARENT
minimal target-sufficient representation losing downstream info = PARENT PATTERN
DIB / multi-task sufficient representation = PARENT AREA
Blackwell/Bayes decision sufficiency = PARENT AREA
conditional information identities = PARENT_OWNED
log-loss rate distortion = PARENT_OWNED
POMDP belief/information states = STRONG PARENT
Approximate Information State JMLR 2022 = STRONG DIRECT PARENT
right congruence / automata minimization = PARENT SUBSTRATE
incompletely specified FSM compatible-state minimization = STRONG DIRECT ALGORITHMIC PARENT
representation identifiability = PARENT AREA
```

---

# 6. Strongest candidate standalone residual

The paper survives only if the following package is not an immediate consequence/rename of the strongest parent product:

1. **cross-channel** state accounting relative to an explicit linguistic predictive quotient;
2. minimum Bayes-policy state under exact responsibility semantics;
3. joint static/dynamic Bayes-policy and recurrent-state optimization;
4. dynamic optionality premium `Omega_dyn`;
5. P0/P1/P2 state-phase classification and horizon cost curve;
6. bounded responsibility-family/horizon law;
7. LLM representation audit distinguishing static probes from controlled future-revision adequacy.

This is now the only plausible JMLR-level residual. It remains high risk.

---

# 7. Canonical paper/review artifacts

- `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V4.md`
- `papers/llm-machine-epistemics/CLAIM_LEDGER_V4.json`
- `papers/llm-machine-epistemics/JMLR_SUBMISSION_GATE_V1.md`
- `NEAREST_WORK_PASS_03_DECISIONAL_STATES.md`
- `NEAREST_WORK_PASS_02_DYNAMIC_STATE.md`
- `HOSTILE_REVIEW_DECISION_MATRIX_V1.md`
- `INTERNAL_PARENT_ALIGNMENT_V1.md`

---

# 8. Final mechanical execution authority

Primary contract:

`MECHANICAL_EXECUTION_SPEC_V5.md`

with exact algorithms in `MECHANICAL_EXECUTION_SPEC_V4.md` incorporated where V5 says unchanged.

The executor does only:

- theorem formalization/checking;
- Bell-complete partition enumeration;
- optimal selector enumeration;
- static/dynamic minimum computation two independent ways;
- horizon curve computation;
- P0/P1/P2 fixture checks;
- assumption countermodel attacks;
- information-identity verification;
- universality construction;
- exact parent metadata/theorem-location retrieval;
- generated tables/figures;
- mechanical manuscript contraction;
- deterministic final terminal.

No scientific narrative/novelty invention is delegated.

---

# 9. Remaining exact checklist

## Formal
- [ ] L1/T2 base checks.
- [ ] R21–R27 responsibility checks.
- [ ] J1–J5 joint dynamic checks.
- [ ] DS1/DS2 Brodu-like zero/positive static checks.
- [ ] PH1–PH3 phase/horizon/family checks.
- [ ] deficit identities.
- [ ] U1–U5 universality checks.
- [ ] parent-owned T8 benchmark checks.

## Enumerative
- [ ] partitions n<=6 complete, n=7 if tractable.
- [ ] selector/static equality.
- [ ] dynamic direct/min-selector equality.
- [ ] canonical tie control.
- [ ] canonical P0/P1/P2 fixtures.
- [ ] mixed P2 witness search.
- [ ] tie-sensitive dynamic selector witness search.
- [ ] horizon stabilization curves.
- [ ] nested responsibility-family curves.
- [ ] predictive-compression assumption attacks.

## Parent metadata
- [ ] Brodu definitions/complexity/transitions.
- [ ] R-PSR theorem details.
- [ ] AIS JMLR 2022 definitions/theorems.
- [ ] ISFSM compatible-state/cover/complexity results.
- [ ] all other frozen parents.

## Manuscript
- [ ] formal theorem status inserted.
- [ ] failed/absorbed claims removed.
- [ ] generated phase/assumption tables inserted.
- [ ] verified refs inserted.
- [ ] JMLR format only if all gates pass.

---

# 10. Deterministic final terminal

Exactly one:

- `THEORY_PAPER_RESIDUAL_SUPPORTED`
- `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`
- `REPRESENTATION_IDENTIFIABILITY_ONLY__NO_NEW_RESIDUAL`
- `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`
- `CANNOT_CHECK_FORMAL_PROOF`

Scientific thinking for this issue identity is closed. Any genuinely new rescue theorem after mechanical falsification requires a successor issue, not an in-place rewrite.
