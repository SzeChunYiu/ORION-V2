# Prospective Revision Audit Protocol V1

**Issue:** #51  
**Status:** theory-derived assessment protocol; no real-LLM result is claimed.  
**Purpose:** turn the surviving #51 contribution into a fully specified learning-system assessment task rather than a vague suggestion for future experiments.

## 1. Assessment question

> After two representations have been matched on the declared linguistic prediction target and the registered current decision, does one retain historical information that is necessary to revise the decision correctly after later evidence?

This protocol tests **representation retention**. It is not a generic belief-revision benchmark.

Belief-R (Wilie et al., EMNLP 2024) is the closest mandatory output-level parent: it tests update versus maintain after additional evidence. The present protocol adds a representation intervention and a present-equivalence gate so that a later difference can be attributed to retained information rather than to an already visible current-performance gap.

---

# 2. Registered episode object

Each audit episode is

```text
ProspectiveRevisionEpisode = (
    episode_id,
    H0,
    linguistic_target,
    responsibility_now,
    current_gold,
    future_evidence_sequence,
    responsibility_future,
    future_gold,
    update_or_maintain_class,
    dormant_cross_channel_variables,
    nuisance_variables,
    admissible_representation_interventions,
    resource_budget,
    provenance
)
```

### `H0`

The complete initially accessible history/information.

### `linguistic_target`

A declared language-prediction target or a finite exact proxy for the complete linguistic future. The theoretical suite uses exact future-law equivalence. A real-model study must state a measurable surrogate and may not claim exact `S_P` recovery.

### `responsibility_now`

A registered decision contract `(Q, actions, loss, semantics)`.

### `current_gold`

The Bayes/known-answer acceptable current action or action set.

### `future_evidence_sequence`

One or more later observations. Every observation must bind to its intended object/source rather than merely add generic text.

### `responsibility_future`

The decision contract after the future evidence. It may equal the current contract with updated evidence, or be a prospectively registered future responsibility.

### `future_gold`

The correct update/retain terminal/action after the future evidence.

### `update_or_maintain_class`

At minimum:

- `UPDATE_REQUIRED`
- `MAINTAIN_REQUIRED`

Optional additional mechanically distinct classes may include `UNRESOLVED_REQUIRED`, but these must be pre-registered and not introduced after model outcomes are seen.

### `dormant_cross_channel_variables`

Variables that are irrelevant to the registered present language/current-decision equivalence but may affect later revision, e.g. source identity, support path, dependence class, scope epoch, evaluator identity or claim lineage.

### `nuisance_variables`

Surface variables deliberately randomized or counterbalanced so they cannot explain revision performance.

---

# 3. Four required phase families

The audit must include negative controls. A suite containing only cases designed to demonstrate a prospective gap is invalid.

## F0 — acquisition/non-identifiability control

The full initial history plus later evidence is insufficient to identify the correct future decision.

Expected terminal:

`CANNOT_CHECK / UNRESOLVED` according to the registered contract.

Purpose:

prevent a representation failure claim when the information was never available.

## F1 — P0 predictive-decisional control

The current language-relevant state already suffices for both current and future responsibility.

Expected:

```text
C_stat^* = 0
Omega_dyn = 0
```

Purpose:

show that extra Machine-Epistemic memory is **not** universally required.

## F2 — P1 current cross-channel family

Histories match the linguistic target but require different current responsibility actions because of a cross-channel distinction.

Expected:

```text
C_stat^* > 0
Omega_dyn = 0  # in the canonical P1 control
```

Purpose:

distinguish an ordinary current decision-state deficit from a prospective-revision deficit.

## F3 — P2 prospective-revision family

Histories match the linguistic target and have the same acceptable current action, but some later evidence sequence makes their future correct decisions diverge.

Canonical expected:

```text
current decision: equal
future decision: different after evidence
Omega_dyn > 0
```

At least one F3 construction must use a **unique current action** so the result cannot be explained by tie-breaking.

---

# 4. Canonical provenance/retraction P2 fixture

The canonical exact fixture has two equiprobable initial histories:

```text
h_A: claim C currently supported through source A
h_B: claim C currently supported through source B
```

Registered current decision:

`RETAIN_CLAIM` in both histories.

Declared linguistic predictive state:

the histories are equivalent for the synthetic linguistic-future target.

Dormant variable:

`support_source in {A,B}`.

Future observation:

`RETRACT(A)`.

Future decision:

```text
h_A -> REOPEN/REJECT according to contract
h_B -> RETAIN
```

With equal prior and exact finite state:

```text
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
```

Mandatory maintain mirror:

introduce a case where the later retraction concerns an unrelated source and the correct terminal remains `RETAIN`. This prevents an “always revise after retraction language” strategy.

---

# 5. Representation conditions

A real-system evaluation should use at least four conditions when feasible.

## R0 — full-history reference

The decision receives all history permitted by the episode contract.

Role:

known-information ceiling, not an architectural baseline.

## R1 — prediction-preserving / cross-channel-removed state

A representation intended to preserve the declared language target while removing or collapsing the registered dormant variable.

Possible mechanisms:

- controlled synthetic encoding;
- context/material deletion;
- source-ID removal;
- representation projection;
- typed-memory ablation;
- a compression map frozen before future evidence.

Role:

test whether present prediction sufficiency alone preserves later revision.

## R2 — current-decision-sufficient state

A representation explicitly constructed or selected to preserve current responsibility behavior while removing distinctions unnecessary to the present acceptable action.

Role:

test the gap between present decision sufficiency and prospective revision sufficiency.

## R3 — prospective-augmented state

R2 plus the smallest registered dormant variable(s) predicted by the theory to be needed after future evidence.

Role:

mechanism-specific positive control.

The audit does not require R3 to be a new neural architecture. It may be an external memory field or controlled representation bit.

---

# 6. Present-equivalence gate

A future-revision comparison is interpretable only after present equivalence is established.

Before future evidence is revealed, require the compared representation conditions to satisfy registered tolerances for:

1. linguistic-prediction performance;
2. current responsibility action/terminal;
3. current responsibility risk/calibration if included in the contract;
4. tool/resource access other than the intended state intervention.

If a compared condition already performs worse on the current responsibility, label the case:

`CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`.

Do not count it as P2 evidence.

---

# 7. Core metrics

## 7.1 Linguistic predictive deficiency

In a finite exact log-loss fixture:

`Delta_pred(Z) = H(Y+|Z) - H(Y+|H)`.

In a real LLM study, use the frozen prediction surrogate specified by the protocol. Do not silently replace it after seeing outcomes.

## 7.2 Current responsibility regret

`delta_now(Z,r) = R_r(Z) - R_r(H)`.

## 7.3 Prospective revision regret

For evidence horizon `k`:

`delta_rev_k(Z,r) = R_future(Z_t, X_1:k) - R_future(H_t, X_1:k)`.

## 7.4 Update accuracy

Fraction correct on `UPDATE_REQUIRED` cases.

## 7.5 Maintain accuracy

Fraction correct on `MAINTAIN_REQUIRED` cases.

This is mandatory and should be reported separately, following the important update/maintain distinction in belief-revision evaluation.

## 7.6 Revision balanced score

If a scalar summary is useful, pre-register a balanced average of update and maintain accuracy. Never use it to hide a catastrophic failure in one class; the components remain primary.

## 7.7 False revision rate

Probability of revising a conclusion that should remain standing.

## 7.8 Missed revision rate

Probability of retaining a conclusion whose registered support has been defeated.

## 7.9 Representation cost

Use the exact conditional entropy in the finite theorem suite.

For actual systems, pre-register one or more operational capacity measures, such as:

- retained tokens;
- transmitted bits under a fixed encoder;
- memory slots;
- serialized memory bytes;
- intervention-specific retained fields.

Hidden-state dimension alone is not an information measure.

---

# 8. Primary causal contrasts

The strongest audit is not a leaderboard. It asks mechanism-specific contrasts.

## Contrast A — prediction state versus current-decision state

`R1` vs `R2` on P1 cases.

Question:

does explicitly retaining the current cross-channel decision distinction remove current responsibility regret while language performance remains matched?

## Contrast B — current-decision state versus prospective state

`R2` vs `R3` on P2 cases.

Question:

does retaining the dormant variable improve later update/maintain performance while present prediction/current action remain matched?

This is the load-bearing #51 contrast.

## Contrast C — full history versus prospective state

`R0` vs `R3`.

Question:

does the registered prospective state recover the relevant revision capability without retaining the entire history?

A tie supports bounded state sufficiency for that responsibility/horizon; it does not establish universal sufficiency.

---

# 9. Required counterfactual and leakage controls

## Surface counterbalance

Names, phrasing, source labels and lexical cues should be permuted so the dormant state cannot be inferred from a shortcut introduced by the benchmark author.

## Evidence-binding control

A future event must identify which source/claim/assumption it concerns. Generic words such as “retracted” are insufficient.

## Unrelated-evidence control

Introduce later evidence with similar surface form that does not affect the current support path.

## Independent-support control

Where the claim has two sufficient supports and only one is defeated, the correct action may remain `RETAIN`. This tests selective rather than global revision.

## Current-visible control

Include cases where the cross-channel distinction already changes the current decision. These belong to P1 and must not be counted as P2.

## Recoverable-from-future control

Include cases where the later evidence itself fully reconstructs the dormant variable. Such cases can have low prospective deficit despite earlier state loss. They prevent the claim that every discarded variable must be stored permanently.

---

# 10. Interpretation terminals

For each representation family/horizon, use one of:

- `P0_CURRENT_AND_PROSPECTIVE_SUFFICIENT`
- `P1_CURRENT_CROSS_CHANNEL_STATE_REQUIRED`
- `P2_PROSPECTIVE_REVISION_STATE_REQUIRED`
- `ACQUISITION_LIMIT__FULL_HISTORY_INSUFFICIENT`
- `FUTURE_EVIDENCE_RECONSTRUCTS_DORMANT_STATE__NO_RETENTION_REQUIRED`
- `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`
- `NO_MECHANISM_EFFECT__PROSPECTIVE_AUGMENTATION_REDUNDANT`
- `CANNOT_CHECK_MATCHED_PRESENT_EQUIVALENCE`

Do not promote a single P2 example into a universal claim about LLM memory.

---

# 11. Minimal synthetic evaluation suite

The theory paper can include or generate a small exact suite without training an LLM.

Required families:

1. P0 zero-extra-state control.
2. P1 current cross-channel case.
3. P2 unique-current-action provenance/retraction case.
4. P2 maintain mirror.
5. independent-support selective-reopening case.
6. future-evidence-reconstructs-state negative control.
7. acquisition-limit case.
8. tie-semantics case.

The existing mechanical suite already verifies several of these structurally. Any generated publication table must be derived from frozen receipts, not manually typed outcome claims.

---

# 12. Optional frozen-LLM extension

A future extension may use a frozen pretrained model; no training is required.

Possible state surfaces:

- prompt/context memory;
- KV-cache or compressed KV state where accessible;
- hidden-state readouts;
- explicit agent memory;
- a learned-free deterministic summary/intervention;
- retrieval memory with selected fields.

The study must distinguish:

- model reasoning failure despite information being retained;
- representation retention failure;
- acquisition failure;
- later evidence being insufficient.

A hidden-state probe alone is not enough. Prefer a causal state intervention or memory ablation that changes the retained variable while preserving present behavior.

---

# 13. Relation to Belief-R

Belief-R remains the mandatory nearest LLM evaluation baseline.

Belief-R asks roughly:

```text
initial premises -> initial conclusion
additional evidence -> update or maintain conclusion
```

The #51 protocol asks:

```text
initial history
-> construct/compare internal representations
-> verify matched present language + current decision
-> reveal additional evidence
-> test whether representation retention changes update/maintain success
```

Therefore the proposed residual is not “belief revision after evidence”. It is **prospective representation adequacy under a matched-current-state control**.

A future empirical paper should use Belief-R directly where compatible and add the representation intervention rather than inventing an unrelated revision benchmark.

---

# 14. Falsifiers

The proposed audit interpretation weakens or fails if:

1. present equivalence cannot be achieved across representation conditions;
2. the dormant variable can be reconstructed from future evidence, eliminating the predicted retention need;
3. adding the proposed prospective state does not improve the registered future decision;
4. improvements are explained by extra tokens, compute, tools or model calls rather than retained information;
5. the representation manipulation alters the current decision before future evidence;
6. a strongest existing memory/decision-state baseline reproduces the same result with no need for the proposed decomposition;
7. all real-model cases are P0 after adequate controls.

A P0-dominated result is scientifically valuable: it would show the Machine-Epistemic augmentation is unnecessary for the tested responsibilities.

---

# 15. Authority and claim boundary

This protocol establishes no empirical fact about GPT, Claude, Gemini, Llama, or any other model unless such a study is separately executed.

It grants no institutional or scientific authority.

Its current status is:

```text
PROTOCOL_ID = ORION51.PROSPECTIVE_REVISION_AUDIT.v1
THEORY_MOTIVATION = MECHANICALLY_SUPPORTED_FINITE_WITNESS
BELIEF_REVISION_EVALUATION_PARENT = BELIEF_R_ACKNOWLEDGED
REAL_LLM_EXECUTION = NOT_REQUIRED_FOR_CORE_THEORY__NOT_EXECUTED_HERE
EMPIRICAL_LLM_CLAIM = NONE
PUBLICATION_ROLE = PRACTICAL_UTILITY_AND_NEW_ASSESSMENT_TASK_CANDIDATE
```
