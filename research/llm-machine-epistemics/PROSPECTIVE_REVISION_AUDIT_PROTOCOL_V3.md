# Prospective Revision Audit Protocol V3

**Issue:** #51  
**Status:** canonical assessment protocol for future execution.  
**Supersedes for execution:** `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1.md`, V2, and the compatibility/channel-scope amendments where V3 covers them.  
**Scientific authority:** none; this is a frozen assessment design, not a real-LLM result.

## 1. Core question

> **After two representations have been matched on a registered linguistic prediction target and the registered current responsibility decision, does one fail after the same later evidence because historical information needed for revision was not retained?**

The audit is a representation-retention assessment under a **registered prediction channel and a distinct future evidence-intervention process**. It is not a generic belief-revision benchmark, memory benchmark, or claim that all useful state should retain all history.

---

# 2. Prediction channel and future-intervention scope

Every audit must register separately:

```text
prediction_reference_protocol rho
present_linguistic_target Y_rho
current_responsibility r_0
future_evidence_intervention_family X
future_responsibility r_k
```

`rho` determines the input/channel conditions under which present linguistic predictive adequacy is evaluated. The later evidence event is a separately registered controlled/exogenous input unless the protocol explicitly includes it in `rho`.

The reference predictive equivalence is therefore relative to `rho`:

\[
h\sim_{P,\rho}h'
\iff
P(Y^+_\rho\mid h)=P(Y^+_\rho\mid h').
\]

Do **not** claim sufficiency for “the complete future” without this scope.

### Stronger controlled-state parent control

Include, where feasible, a representation/condition explicitly sufficient for the joint controlled target that includes the registered evidence-intervention family. If the dormant distinction becomes present-state-relevant and P2 disappears, that is a valid control rather than a failure of the audit.

---

# 3. Mandatory parent controls

Treat as direct/strong parents rather than novelty baselines:

- causal states / PSR;
- Brodu decision/decisional states and Blackwell decision sufficiency;
- R-PSR;
- POMDP belief/information state and Approximate Information State;
- compatible/right-congruent FSM minimization and stable quotient/minimal Markovization;
- IB/DIB and value-equivalent decision compression;
- Belief-R — output update versus maintain after new evidence;
- MEMENTO — learned compression plus alternate hidden retention channels;
- PM-Bench — prospective memory for future intentions;
- two-agent LLM state-compression relay studies;
- Router-Mem;
- Decision-Aware Memory Cards;
- AgenticSTS;
- evidence-informed continual LLM beliefs;
- selected/omitted-evidence LLM updating.

The #51 delta is the **matched-present representation intervention followed by common later evidence**, with acquisition/current/prospective-state separation and alternate-channel attribution controls.

---

# 4. Registered episode object

```text
ProspectiveRevisionEpisodeV3 = (
    episode_id,
    H0,
    prediction_reference_protocol,
    linguistic_target,
    responsibility_now,
    current_gold_or_contract,
    future_evidence_intervention_family,
    future_evidence_sequence,
    responsibility_future,
    future_gold_or_contract,
    update_or_maintain_class,
    dormant_cross_channel_variables,
    nuisance_variables,
    admissible_representation_interventions,
    alternate_state_channels,
    parametric_side_information,
    decoding_policy,
    present_equivalence_margins,
    resource_budget,
    provenance
)
```

## 4.1 Alternate state channels

Enumerate every state surface through which a supposedly removed dormant variable could survive, where observable/controllable:

- remaining prompt/context text;
- KV cache;
- residual/hidden activations;
- summary embeddings;
- retrieval keys/index metadata;
- explicit tool state;
- external memory fields;
- controller/session metadata.

## 4.2 Parametric side information

Also register fixed model parameters / parametric knowledge as side information.

A fixed model cannot encode which one of two randomized episode histories actually occurred unless that distinction enters some state/input channel, but parameters can:

- reconstruct public facts about a named source;
- infer a missing variable from content;
- interact with later evidence so storage appears unnecessary.

Therefore distinguish:

```text
dormant variable retained in episode state
vs
variable reconstructable from fixed parametric knowledge + observed inputs/evidence.
```

If parametric reconstruction explains revision success, do not attribute success to retained episode state.

If a state channel or parametric reconstruction route cannot be checked, record a bounded `CANNOT_CHECK` rather than assuming absence.

---

# 5. Required family balance

A suite containing only favorable prospective-loss cases is invalid.

## F0 — acquisition/non-identifiability

Even full registered history plus later evidence is insufficient to determine the correct future responsibility action.

Terminal:

`ACQUISITION_LIMIT__FULL_HISTORY_INSUFFICIENT`.

## F1 — P0 predictive-decisional

The registered prediction state/current representation already supports current and future responsibility.

Expected:

```text
C_stat^* = 0
Omega_dyn = 0
```

## F2 — P1 current cross-channel

Histories are equivalent for the registered linguistic target but require different **current** responsibility decisions.

Expected:

```text
C_stat^* > 0
Omega_dyn = 0
```

## F3 — P2 prospective revision

Histories are equivalent for the registered linguistic target and current acceptable action, but common later evidence makes correct future decisions incompatible unless a dormant distinction is retained or reconstructed.

Expected canonical shape:

```text
present decision equal
future decision differs after common evidence
Omega_dyn > 0
```

At least one F3 family must have a unique current action.

## F4 — controlled-target strengthening control

The reference prediction/state target explicitly includes the registered intervention family or otherwise preserves the dormant distinction prospectively.

Expected:

- former P2 case can contract to P0/P1;
- demonstrates target/channel relativity.

---

# 6. Canonical provenance/retraction fixture

Two equiprobable initial histories:

```text
h_A: claim C currently supported through source A
h_B: claim C currently supported through source B
```

Reference prediction protocol:

`rho` under which support-source identity does not alter the declared linguistic prediction target.

Current action:

`RETAIN_CLAIM` for both.

Dormant variable:

`support_source in {A,B}`.

Future controlled evidence:

`RETRACT(A)` supplied identically to both.

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

Mandatory mirrors:

- unrelated-source retraction -> `RETAIN`;
- independent sufficient support survives -> selective `RETAIN`;
- later evidence itself identifies the support source -> no storage-based P2 attribution;
- stronger controlled reference state already contains support-source distinction -> P2 may vanish.

---

# 7. Representation conditions

## R0 — full-history reference

Receives every history field permitted by the episode contract.

## R1 — prediction-preserving targeted compression

Designed to preserve the frozen `rho` linguistic target while removing/collapsing a specified dormant variable.

## R2 — current-decision-sufficient state

Designed/selected to preserve present responsibility performance while discarding distinctions unnecessary to the current acceptable action.

## R3 — prospective-augmented state

R2 plus the minimum registered variable(s) hypothesized to be needed under the future evidence process.

## R4 — controlled-future state control

State explicitly selected/evaluated for the stronger joint controlled target including the evidence-intervention family.

R3/R4 are mechanism controls, not universal architecture proposals.

---

# 8. Present-equivalence gate

No prospective contrast is interpretable until present equivalence is established.

Freeze before future outcomes:

```text
epsilon_pred
current_action_equivalence_rule
epsilon_current_risk  # if risk/calibration registered
epsilon_resource
sampling/evaluation unit
confidence level / exact rule
```

Required matched dimensions:

1. declared linguistic prediction metric/surrogate under `rho`;
2. current action/terminal;
3. current responsibility risk/calibration if registered;
4. tool/resource access aside from intended representation intervention;
5. inference budget aside from declared state-size difference.

### Statistical rule for empirical runs

Do not interpret `p > 0.05` as evidence of equivalence.

For noisy empirical metrics, use a **prospectively frozen equivalence margin** and either:

- confidence interval wholly inside the equivalence margin; or
- an equivalent registered equivalence-test procedure.

The independent unit is the registered episode/case, not tokens or repeated samples from one case unless the estimand explicitly concerns sampling variation.

Failure terminal:

`CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`.

---

# 9. Representation-removal / alternate-channel gate

A representation intervention may claim to remove dormant variable `B` only after checking the registered surviving channels.

## Gate A — recoverability

Where feasible, attempt to recover `B` from each surviving channel, parametric side information, or their registered combination using a probe frozen before future-revision outcomes are inspected.

Strong recoverability falsifies “removed”. Lack of probe success alone does not prove absence.

## Gate B — causal use

Where feasible, intervene on the candidate retained channel/direction and test whether it changes downstream behavior while present-equivalence remains acceptable.

## Gate C — channel ablation

If a candidate alternate channel can be removed, ablate it and repeat the future-revision contrast.

## Gate D — parametric reconstruction control

Construct cases with randomized/nonce source identities or episode-local support assignments that fixed model parameters cannot know in advance, where the scientific question requires isolating episode-state retention rather than world knowledge.

Do not use this control if nonce identities destroy the semantic responsibility being studied; then report the parametric route as part of the system instead.

## Terminals

- `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION`
- `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- `PARAMETRIC_RECONSTRUCTION_EXPLAINS_SUCCESS`
- `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`

A strong P2 state-retention attribution requires the first terminal. Otherwise scope the result to the channels actually excluded.

---

# 10. Deterministic versus stochastic decision semantics

The core finite theory uses exact deterministic decision rules/zero-regret acceptable actions.

## 10.1 Deterministic execution mode

Preferred for the cleanest real-model audit when available:

- fixed decoding policy;
- deterministic/greedy output mapping;
- exact registered action extraction.

## 10.2 Stochastic system mode

If stochastic decoding is part of the system under study, freeze:

```text
temperature/top_p/etc.
random seed policy
number of samples per episode
aggregation rule
registered expected-regret estimand
```

Do not compare single lucky/unlucky draws as representation adequacy.

### Zero-regret compatibility

A randomized policy with zero regret for every history in a representation/evidence cell can exist only if its support lies in the acceptable-action set of every history; therefore the full joint acceptable-action intersection must be nonempty.

### Approximate regret

When nonzero regret is allowed, randomized mixtures can trade error across histories even if the exact joint intersection is empty. Use the registered decision loss and report expected/worst-case regret according to the frozen estimand rather than applying the exact collision terminal mechanically.

The approximate/stochastic extension is standard decision theory, not a new theorem claim.

---

# 11. Complete one-step compatibility criterion

For representation `Z=z` and common evidence `x`, define

\[
\mathcal C(z,x)
=
\{h: Z(h)=z,\delta(h,x)\text{ defined}\}
\]

and

\[
\boxed{
\mathcal I(z,x)
=
\bigcap_{h\in\mathcal C(z,x)} A_x^*(h).
}
\]

Under exact one-step `ANY_OPTIMAL_ACTION` semantics, a deterministic future rule using only `(z,x)` is acceptable for every history in the cell iff `I(z,x)` is nonempty.

## Pairwise collision

A pair with disjoint future acceptable-action sets is an easy positive insufficiency certificate.

But no pairwise collision is **not** a positive sufficiency certificate in general.

Mandatory control:

```text
A1={a,b}
A2={b,c}
A3={a,c}
```

Every pair overlaps; the joint intersection is empty.

If all future action sets are singleton, pairwise collision detection is complete. The canonical provenance witness is in this unique-action regime.

For multi-step horizons, one-step compatibility is not enough; use the registered recurrent/right-congruent state analysis.

---

# 12. Core metrics

Report separately.

## Linguistic predictive deficiency

Finite exact log-loss reference:

\[
\Delta_{pred}(Z)
=
H(Y^+_\rho\mid Z)-H(Y^+_\rho\mid H).
\]

Real-model execution uses a prospectively frozen surrogate; no exact `S_P` recovery claim.

## Current responsibility regret

\[
\delta_{now}(Z,r)
=
\mathcal R_r(Z)-\mathcal R_r(H).
\]

## Prospective revision regret

\[
\delta_{rev,k}(Z,r)
=
\mathcal R_{future}(Z_t,X_{1:k})
-
\mathcal R_{future}(H_t,X_{1:k}).
\]

## Update accuracy/regret

Primary for `UPDATE_REQUIRED` cases.

## Maintain accuracy/regret

Primary for `MAINTAIN_REQUIRED` cases.

## False revision rate

Revision when the conclusion should remain standing.

## Missed revision rate

Failure to revise when support has been defeated.

## Selective-reopening precision/recall

When dependency structure is registered, reopen only conclusions whose sufficient support was invalidated.

## Compatibility metrics

Primary structural metric:

- incompatible representation/evidence cell count/rate (`I(z,x)=empty`).

Secondary easy witness:

- pairwise disjoint future-action collision count/rate.

## Representation cost

Exact conditional entropy only in finite fixtures. For actual systems use a registered operational measure such as retained tokens, serialized bytes, memory slots, transmitted bits under a fixed encoder, or controlled cache budget.

Hidden dimension alone is not an information measure.

---

# 13. Primary causal contrasts

## A — R1 vs R2 on P1

Does retaining current cross-channel information eliminate present decision regret while `rho` language performance remains equivalent?

## B — R2 vs R3 on P2

Load-bearing contrast: does retaining the registered dormant variable improve later update/maintain/selective-reopening under **identical later evidence** while present behavior remains equivalent?

## C — R0 vs R3

Can bounded prospective state recover the responsibility without full history?

## D — nominal R2 vs truly ablated R2

Does removing an alternate retained channel reveal the predicted revision deficit?

## E — R3 vs R4 stronger controlled-state control

If the reference target itself includes the future intervention family, does prospective state become current-state-relevant and shrink the apparent P2 premium?

---

# 14. Required controls

- prediction-reference protocol frozen before outcomes;
- lexical/source-name permutation;
- nuisance-variable randomization;
- evidence object-binding;
- unrelated-evidence maintain mirror;
- independent-support selective-reopening control;
- P1 current-visible control;
- future-evidence-reconstructs-variable control;
- alternate-channel retention control;
- parametric reconstruction / nonce-identity control when semantically valid;
- controlled-future stronger-state control R4;
- state-budget/current-inference-budget control;
- full-history acquisition ceiling;
- three-history joint-intersection compatibility control;
- deterministic versus stochastic decoding mode frozen.

No benchmark surface feature should reveal the terminal independently of the registered evidence relation.

---

# 15. Interpretation terminals

- `P0_CURRENT_AND_PROSPECTIVE_SUFFICIENT`
- `P1_CURRENT_CROSS_CHANNEL_STATE_REQUIRED`
- `P2_PROSPECTIVE_REVISION_STATE_REQUIRED`
- `ACQUISITION_LIMIT__FULL_HISTORY_INSUFFICIENT`
- `FUTURE_EVIDENCE_RECONSTRUCTS_DORMANT_STATE__NO_RETENTION_REQUIRED`
- `CONTROLLED_TARGET_ALREADY_RETAINS_DISTINCTION__P2_CONTRACTS`
- `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`
- `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- `PARAMETRIC_RECONSTRUCTION_EXPLAINS_SUCCESS`
- `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`
- `NO_MECHANISM_EFFECT__PROSPECTIVE_AUGMENTATION_REDUNDANT`
- `CANNOT_CHECK_MATCHED_PRESENT_EQUIVALENCE`
- `ONE_STEP_INCOMPATIBLE_JOINT_ACTION_INTERSECTION_EMPTY`

A P0-dominated suite is a valid negative result.

---

# 16. Minimal exact/synthetic suite

Required:

1. P0 zero-extra-state control;
2. P1 current cross-channel case;
3. P2 unique-current-action provenance/retraction case;
4. P2 maintain mirror;
5. independent-support selective-reopening case;
6. future-evidence-reconstructs-state negative control;
7. acquisition-limit case;
8. tie-semantics current-action case;
9. alternate-channel-survival synthetic control;
10. alternate-channel-true-removal positive control;
11. three-history pairwise-overlap/joint-empty future-action control;
12. stronger controlled-reference target in which the intervention-relevant distinction is already retained;
13. parametric-reconstruction control where semantically appropriate.

Publication tables must be generated from frozen receipts/scripts when executed.

---

# 17. Optional frozen-LLM extension

No training required.

Possible surfaces:

- context/prompt memory;
- external agent memory;
- deterministic summaries;
- retrieval memory;
- KV state where accessible;
- hidden-state projections/interventions;
- learned compression only if using an already available method/model.

The result must distinguish:

- acquisition failure;
- information retained but not used;
- information actually removed;
- parametric reconstruction;
- information reconstructed by later evidence;
- ordinary reasoning failure despite retained state.

## 17.1 Current-equivalence inference

Freeze equivalence margins before looking at future revision outcomes. Do not use failure to reject a difference as proof of equivalence.

## 17.2 Sampling

If repeated stochastic generations are used, treat episode identity and repeated draws correctly. Repeated samples from one episode do not create independent scientific cases.

---

# 18. Falsifiers

The P2 representation-retention interpretation contracts if:

1. present equivalence cannot be established;
2. the prediction reference protocol actually includes the supposedly omitted intervention behavior and the state is not predictive-equivalent under that target;
3. the dormant variable remains in an alternate state channel;
4. fixed parameters + observed content reconstruct it;
5. later evidence reconstructs it;
6. full history itself cannot identify the correct future decision;
7. prospective augmentation does not improve the registered future decision;
8. gain is explained by extra tokens/compute/tools rather than retained information;
9. a strongest existing memory/state baseline reproduces the same controlled audit conclusion with no added diagnostic value;
10. all adequately controlled real-model cases are P0.

---

# 19. Current authority

```text
PROTOCOL_ID = ORION51.PROSPECTIVE_REVISION_AUDIT.v3
PREDICTION_SCOPE = REGISTERED_REFERENCE_INPUT_PROTOCOL
FUTURE_EVIDENCE = DISTINCT_REGISTERED_INTERVENTION_FAMILY
THEORY_SUPPORT = MECHANICALLY_VERIFIED_FINITE_NO_CERTIFICATION_WITNESS
ONE_STEP_COMPATIBILITY = JOINT_ACTION_INTERSECTION_COMPLETE
PAIRWISE_COLLISION = SUFFICIENT_WITNESS_ONLY
ALTERNATE_CHANNEL_GATE = MANDATORY
PARAMETRIC_SIDE_INFORMATION = REGISTERED
PRESENT_EQUIVALENCE = EQUIVALENCE_MARGIN_NOT_NONSIGNIFICANCE
STOCHASTIC_DECODING = FROZEN_POLICY_EXPECTED_REGRET_IF_USED
REAL_LLM_EXECUTION = NOT_REQUIRED__NOT_EXECUTED_HERE
EMPIRICAL_LLM_CLAIM = NONE
PUBLICATION_ROLE = FORMAL_ASSESSMENT_TASK / PRACTICAL_EVALUATION_FRAMEWORK
```
