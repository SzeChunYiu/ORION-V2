# Prospective Revision Audit Protocol V2

**Issue:** #51  
**Status:** canonical prospective-revision assessment protocol.  
**Supersedes:** `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1.md`.  
**Scientific authority:** none; this is a frozen assessment design, not a real-LLM result.

## 1. Core assessment question

> After two representations have been matched on the declared linguistic prediction target and the registered current responsibility decision, does one retain historical information that is necessary to revise that decision correctly after later evidence?

The audit targets **representation retention under future evidence**. It is not a generic belief-revision benchmark, not a generic memory benchmark, and not a claim that every useful representation must retain all history.

---

# 2. Mandatory parent controls

A valid execution must treat the following as direct or strong parents rather than novelty baselines:

- Belief-R — update versus maintain after new evidence;
- MEMENTO — learned compression of reasoning/context with evidence that nominally removed content can persist through another internal KV channel;
- PM-Bench — prospective memory for delayed intentions/cues;
- State Compression in Two-Agent LLM Relays — lossy representation can change exact downstream constraint satisfaction;
- Router-Mem — evidence-conditioned current-memory sufficiency routing;
- Decision-Aware Memory Cards — decision-utility-aware context selection/compression;
- AgenticSTS — bounded typed long-horizon agent memory;
- evidence-informed continual LLM belief work and selected/omitted-evidence updating studies.

The #51 delta is the **matched-present representation intervention followed by later evidence**, with explicit acquisition/current-state/prospective-state separation.

---

# 3. Registered episode object

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
    alternate_state_channels,
    resource_budget,
    provenance
)
```

### `alternate_state_channels`

Every execution must enumerate all state surfaces through which a supposedly removed dormant variable could survive, where observable/controllable. Examples:

- remaining prompt/context text;
- KV cache;
- residual/hidden activations;
- summary embeddings;
- retrieval keys/index metadata;
- explicit tool state;
- external memory fields;
- controller/session metadata.

If a channel cannot be observed or manipulated, record `CANNOT_CHECK_ALTERNATE_CHANNEL_<name>` rather than assuming the information is absent.

---

# 4. Required phase families

A suite containing only favorable P2 examples is invalid.

## F0 — acquisition/non-identifiability control

`H0 + future_evidence` is insufficient to determine the correct future responsibility action.

Terminal:

`ACQUISITION_LIMIT__FULL_HISTORY_INSUFFICIENT`.

## F1 — P0 predictive-decisional control

The declared language-predictive state already supports current and future responsibility.

Expected:

```text
C_stat^* = 0
Omega_dyn = 0
```

Purpose: demonstrate cases where extra epistemic memory is unnecessary.

## F2 — P1 current cross-channel family

Histories are equivalent for the declared linguistic target but require different current responsibility decisions because of a non-linguistic/history-side distinction.

Expected canonical shape:

```text
C_stat^* > 0
Omega_dyn = 0
```

Purpose: prevent an ordinary current-state deficit from being mislabeled as prospective loss.

## F3 — P2 prospective-revision family

Histories are equivalent for the declared linguistic target and support the same acceptable present decision, but common later evidence makes their future correct decisions diverge.

Expected canonical shape:

```text
present decision equal
future decision differs after evidence
Omega_dyn > 0
```

At least one F3 family must have a **unique current action**.

---

# 5. Canonical provenance/retraction fixture

Two equiprobable initial histories:

```text
h_A: claim C currently supported through source A
h_B: claim C currently supported through source B
```

Current responsibility action:

`RETAIN_CLAIM` for both.

Dormant variable:

`support_source in {A,B}`.

Future evidence:

`RETRACT(A)`.

Future decisions:

```text
h_A -> REOPEN/REJECT according to contract
h_B -> RETAIN
```

Exact finite target:

```text
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
```

Mandatory mirrors/controls:

- retraction of an unrelated source -> `RETAIN`;
- two independent sufficient supports, only one defeated -> selective `RETAIN` when the second support suffices;
- future evidence explicitly contains the source identity -> dormant variable may be reconstructed, so retention is not required.

---

# 6. Representation conditions

## R0 — full-history reference

Receives every history field allowed by the episode contract.

## R1 — prediction-preserving / cross-channel-targeted compression

Designed to preserve the frozen language target while removing/collapsing a specified dormant variable.

## R2 — current-decision-sufficient state

Designed/selected to preserve present responsibility performance while discarding distinctions unnecessary to the current acceptable action.

## R3 — prospective-augmented state

R2 plus the minimum registered variable(s) predicted to be required after future evidence.

R3 is a mechanism-specific positive control, not a proposed universal architecture.

---

# 7. Present-equivalence gate

Future revision comparisons are valid only after current equivalence is established within frozen tolerances on:

1. declared linguistic prediction metric/surrogate;
2. current action/terminal;
3. current responsibility risk/calibration if registered;
4. tool/resource access aside from the intended representation intervention;
5. inference budget aside from the declared state-size difference.

Failure terminal:

`CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`.

---

# 8. Alternate-channel retention gate — new in V2

A representation intervention may claim to remove dormant variable `B` only if the experiment checks the surviving state channels declared in the episode.

## Gate A — recoverability

Where feasible, attempt to recover `B` from each surviving channel or their registered combination using a probe frozen before future revision outcomes are examined.

Pure linear decodability is not enough to prove use, but strong recoverability falsifies a claim that `B` was removed.

## Gate B — causal use

Where feasible, intervene on the surviving channel/state direction and test whether the variable changes downstream behavior while present-equivalence constraints remain acceptable.

## Gate C — channel ablation

If a candidate alternate channel is removable (e.g. retained KV segment, summary embedding, memory key), ablate it and repeat the future-revision condition.

## Terminals

- `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION`
- `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`

A P2 representation-retention claim is authorized only under the first terminal, or under an explicitly scoped statement naming the unchecked channels.

### Why this gate is mandatory

MEMENTO provides direct practical evidence that text/reasoning content can be evicted while useful information persists implicitly in downstream KV states. Therefore visible-text deletion or summary replacement is not sufficient evidence of information removal.

---

# 9. Core metrics

Report separately:

## Linguistic predictive deficiency

Finite exact log-loss reference:

`Delta_pred(Z) = H(Y+|Z) - H(Y+|H)`.

Real-model execution uses a prospectively frozen surrogate; no claim of exact `S_P` recovery.

## Current responsibility regret

`delta_now(Z,r) = R_r(Z) - R_r(H)`.

## Prospective revision regret

`delta_rev_k(Z,r) = R_future(Z_t,X_1:k) - R_future(H_t,X_1:k)`.

## Update accuracy

Primary for `UPDATE_REQUIRED` cases.

## Maintain accuracy

Primary for `MAINTAIN_REQUIRED` cases.

## False revision rate

Revision when the conclusion should remain standing.

## Missed revision rate

Failure to revise after registered support has been defeated.

## Representation cost

Exact conditional entropy in finite fixtures. For actual models, a registered operational proxy such as retained tokens, serialized bytes, memory slots, transmitted bits under a fixed encoder, or a controlled cache budget.

Hidden dimension alone is not a valid information measure.

---

# 10. Primary causal contrasts

## Contrast A — R1 vs R2 on P1

Does retaining the current cross-channel distinction remove present decision regret while language performance remains matched?

## Contrast B — R2 vs R3 on P2

Does adding the registered dormant variable improve later update/maintain/selective-reopening performance while current language/current action remain matched?

This is the load-bearing #51 contrast.

## Contrast C — R0 vs R3

Does the bounded prospective state recover the relevant revision behavior without retaining full history?

## Contrast D — R2-with-alternate-channel vs truly ablated R2

When a nominally removed variable survives in another channel, does removing that alternate channel expose the predicted revision deficit?

This distinguishes actual retention from an intervention that merely moved information.

---

# 11. Prospective revision collision certificate

Use `PROSPECTIVE_REVISION_COLLISION_DIAGNOSTIC_V1.md`.

A matched collision `(h,h',x)` requires:

- same audited representation state;
- present language equivalence;
- same acceptable current action;
- same feasible future evidence event;
- disjoint acceptable future action sets.

If present-equivalence and alternate-channel gates pass, a collision certifies prospective insufficiency for the registered representation/responsibility.

Aggregate metrics must never replace the exact collision witness when one exists.

---

# 12. Required leakage and causal controls

- lexical/source-name permutation;
- nuisance-variable randomization;
- evidence object-binding;
- unrelated-evidence mirror;
- independent-support selective-reopening control;
- P1 current-visible control;
- future-evidence-reconstructs-variable control;
- alternate-channel retention control;
- same-token-budget/current-inference-budget control;
- full-history acquisition ceiling.

No benchmark surface feature should reveal the required terminal independently of the registered evidence relation.

---

# 13. Relation to direct LLM-memory/revision parents

## Belief-R

Tests output update versus maintain after new evidence.

#51 addition:

present-match + representation intervention + future evidence.

## MEMENTO

Learns compressed internal reasoning state and shows nominally removed content can persist through another internal channel.

#51 response:

mandatory alternate-channel retention gate.

## PM-Bench

Tests prospective memory for delayed intentions.

#51 distinction:

future **revision of an existing epistemic decision**, not remembering a future intention.

## State Compression in Two-Agent LLM Relays

Tests downstream constraint preservation across compressed hand-off representations.

#51 distinction:

current decision must first be matched; later common evidence is the discriminator.

## Router-Mem

Asks whether current evidence/memory is sufficient and routes to deeper retrieval.

#51 distinction:

state is sufficient **now** but may fail **after future evidence**.

## Evidence-informed continual LLM beliefs / selected-evidence studies

Model changing evidence and belief availability.

#51 distinction:

separate acquisition/selection from same-information state-retention loss.

---

# 14. Interpretation terminals

- `P0_CURRENT_AND_PROSPECTIVE_SUFFICIENT`
- `P1_CURRENT_CROSS_CHANNEL_STATE_REQUIRED`
- `P2_PROSPECTIVE_REVISION_STATE_REQUIRED`
- `ACQUISITION_LIMIT__FULL_HISTORY_INSUFFICIENT`
- `FUTURE_EVIDENCE_RECONSTRUCTS_DORMANT_STATE__NO_RETENTION_REQUIRED`
- `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`
- `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`
- `NO_MECHANISM_EFFECT__PROSPECTIVE_AUGMENTATION_REDUNDANT`
- `CANNOT_CHECK_MATCHED_PRESENT_EQUIVALENCE`

A P0-dominated suite is a valid negative result.

---

# 15. Minimal exact/synthetic suite

Required families:

1. P0 zero-extra-state control;
2. P1 current cross-channel case;
3. P2 unique-current-action provenance/retraction case;
4. P2 maintain mirror;
5. independent-support selective-reopening case;
6. future-evidence-reconstructs-state negative control;
7. acquisition-limit case;
8. tie-semantics case;
9. alternate-channel-survival synthetic control;
10. alternate-channel-true-removal positive intervention control.

Publication tables must be generated from frozen receipts/scripts when executed.

---

# 16. Optional frozen-LLM extension

No training is required.

Possible surfaces:

- context/prompt memory;
- external agent memory;
- deterministic summaries;
- retrieval memory;
- KV state where accessible;
- hidden-state projections/interventions;
- learned compression only if using an already available model/method, not required for core #51.

The result must distinguish:

- acquisition failure;
- information still retained but not used;
- information actually removed;
- information reconstructed by later evidence;
- ordinary reasoning failure despite retained state.

---

# 17. Falsifiers

The proposed P2 interpretation fails or contracts if:

1. present equivalence cannot be established;
2. the alleged dormant variable remains in an alternate state channel;
3. future evidence reconstructs the variable;
4. full history itself cannot identify the correct future decision;
5. adding the proposed prospective state does not improve the registered future decision;
6. gain is explained by more compute/tokens/tools rather than retained information;
7. a strongest existing memory/state baseline reproduces the same mechanism with no need for the proposed diagnostic decomposition;
8. all adequately controlled real-model cases are P0.

---

# 18. Current authority

```text
PROTOCOL_ID = ORION51.PROSPECTIVE_REVISION_AUDIT.v2
THEORY_SUPPORT = MECHANICALLY_VERIFIED_FINITE_NO_CERTIFICATION_WITNESS
DIRECT_MEMORY_AND_REVISION_PARENTS = ABSORBED
ALTERNATE_CHANNEL_GATE = MANDATORY
REAL_LLM_EXECUTION = NOT_REQUIRED__NOT_EXECUTED_HERE
EMPIRICAL_LLM_CLAIM = NONE
PUBLICATION_ROLE = PRACTICAL_UTILITY / FORMAL_ASSESSMENT_TASK
```
