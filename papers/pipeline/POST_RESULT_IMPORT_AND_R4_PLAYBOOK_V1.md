# Post-Result Import and R4 Playbook V1

**Purpose:** define exactly what happens after protected execution returns results. This prevents outcome-driven narrative drift and keeps the remaining writing work bounded.

## 1. Entry condition

Do not begin result import from screenshots, copied prose, partial logs, or hand summaries.

Require, where applicable:

```text
RUN_IDENTITY.json
ENVIRONMENT_AND_MODEL_BINDINGS.json
frozen_tasks.json
responses/*
evaluations/*
aggregate/arm_metrics.json
aggregate/paired_comparisons.json
aggregate/component_effects.json
aggregate/resource_pareto.json
aggregate/failure_ledger.json
aggregate/paper_claim_updates.json
EXECUTION_SUMMARY.md
```

The run identity, protocol version, benchmark/dataset identity, evaluator identity and resource contract must be recoverable.

## 2. Custody before interpretation

Before reading the scientific conclusion:

1. verify the exact run/source commit;
2. verify protocol/manifest hashes or repository identities;
3. confirm no gold/outcome data entered solver requests;
4. classify amendments as pre-outcome or post-outcome;
5. check task exclusions against the frozen outcome-blind rule;
6. check stochastic repetitions are nested within tasks;
7. check resource/model/tool parity across compared arms;
8. record unavailable resources as `CANNOT_CHECK`.

Any material custody failure blocks headline result import until dispositioned.

## 3. Analysis freeze

Use the registered analysis before creating a new preferred specification.

For every primary comparison report:

- point estimate;
- uncertainty interval;
- paired discordance/task table;
- hard-failure count;
- missingness and `CANNOT_CHECK`;
- resource differences;
- project/domain strata;
- simple/F0 wins;
- negative results.

Run the reasonable-specification audit required by issue #46. If defensible specifications disagree, the disagreement enters the paper.

## 4. Scientificity promotion

For every central concept/claim, update its scientificity card.

Allowed movement:

```text
S0 inspiration/metaphor
S1 operational concept
S2 discriminating hypothesis
S3 prospective tested result
S4 independent replication/material cross-domain result
S5 foundation-proposition candidate
```

No result automatically grants field status or a universal law.

A concept may instead move downward to:

```text
PARENT_OWNED
REDUNDANT_DRAG
HARMFUL
CONTEXTUAL
MERGED
REFUTED
CANNOT_CHECK
```

## 5. Component disposition

Every tested ORION component receives exactly one evidence-bound disposition:

```text
NECESSARY
PARENT_REPLACEABLE
CONTEXTUAL
REDUNDANT_DRAG
HARMFUL
CANNOT_CHECK
```

If a component is removable without protected loss, remove/merge it before the final architecture and paper claims freeze.

## 6. Paper result import order

Import specialist evidence before rewriting the flagship.

### P-A

Require remote-parent recall, false-analogy control and native-verdict fidelity jointly. Recall alone cannot support the paper.

### P-B

Require formal composition/obstruction evidence plus naturalistic relation/transport cases. A schema-only contribution contracts to infrastructure/methods.

### P-C

Require protected controller value: justified terminals, lower critical false completion or better escalation/efficiency, simple-task non-regression, component attribution and resilience.

### P-D

Require value beyond strongest assurance/dependence/evaluator parents: false-corroboration/authority protection without destroying genuine independent evidence, plus evaluator/test adequacy and independent adjudication.

### P-E

Survives only with genuine prospective/time-sliced opportunity value beyond experts/F0/P-C. Otherwise merge into P-C.

### P-F

Survives only with a predeclared machine-native mechanism, matched-compute causal effect, adequate external witness and materially different domain transfer. Otherwise merge into P-C/flagship.

### P-G candidates

`P-G-KM` and `P-G-WF` remain unadmitted. Only one future P-G identity may be assigned after its distinct admission threshold is met.

## 7. Results-section writing rule

Populate the already frozen result identities; do not invent a new headline result because another analysis looks better.

For each result block include:

- registered question;
- design and comparator identity;
- result and uncertainty;
- negative/parent/simple outcomes;
- robustness/specification result;
- component attribution if applicable;
- scientificity level supported;
- exact limitation and falsifier;
- claim IDs updated.

Do not convert an exploratory finding into confirmatory wording.

## 8. Figure freeze

Figures are selected from the evidence spine, not from aesthetic preference.

Every primary display item must answer one scientific question and include uncertainty/failure information where applicable.

Default priority:

1. primary protected comparison;
2. failure/false-completion or scientificity mechanism;
3. component/resource frontier;
4. cross-domain/native-fidelity result.

Supplementary figures carry diagnostic/specification details that are necessary but not central.

## 9. Flagship rewrite last

The flagship is rewritten only after specialist dispositions are frozen.

Its field-level conclusion must match the evidence-supported F0/F1/F2/F3 terminal:

- `F2_ABSORPTIVE_SUPERTHEORY_PLAUSIBLE`;
- `F1_INTERFIELD_ADVANCE_ONLY`;
- `F0_PARENT_FEDERATION_SUFFICIENT`;
- `F3_DOMAIN_FEDERATION_ONLY`;
- `DECEPTIVE_UNIFICATION`;
- `OVERGENERALIZED_THEORY`;
- `CANNOT_CHECK`.

No field language stronger than issue #46 scientificity and issue #38 external demarcation permit.

## 10. R3 gate

A paper reaches R3 only when:

- protected experiment/formal result completed;
- strongest parent actually compared;
- primary estimand and uncertainty reported;
- negative and parent-win outcomes retained;
- critical integrity failures dispositioned;
- component/mechanism attribution sufficient for the claimed mechanism;
- independent semantic/domain evaluation exists where needed;
- claim ledger and figures can be frozen without outcome-conditioned endpoint changes.

## 11. R4 gate

After R3:

1. complete source-by-source and atomic-claim audit;
2. freeze tables, figures and source data;
3. archive code, environment, benchmark/dataset and receipts;
4. run target-journal word/reference/display/declaration QA;
5. complete author contribution, competing interest, data/code availability and AI-use disclosures;
6. run independent hostile-editor review;
7. resolve every critical editorial/scientific concern or contract the claim;
8. prepare cover letter and submission metadata;
9. mark `SUBMISSION_READY_R4` only if every required gate is satisfied.

## 12. No automatic manuscript editing

Analysis tooling may propose claim updates and render result tables. It must not automatically rewrite paper prose, title, abstract or conclusions.

The final narrative is a scientific interpretation step subject to independent review.

## 13. Final close states

Each paper ends in one of:

```text
SUBMISSION_READY_R4
SCIENTIFICALLY_COMPLETE_TARGET_MISMATCH
FALLBACK_VENUE_READY_R4
MERGED_INTO_ANOTHER_PAPER
PARENT_SUBSUMED_METHODS_RESOURCE
NEGATIVE_RESULT_PAPER
CLAIM_CONTRACTED
CANNOT_CHECK
DROP_WITH_PRESERVED_EVIDENCE
```

A negative or contracted paper is a valid scientific closeout.

## Current terminal

```text
POST_RESULT_PLAYBOOK = FROZEN_PRE_RESULTS
RESULT_IMPORT = WAITING_ON_ISSUE_45
SCIENTIFICITY_REVIEW = ISSUE_46
EXTERNAL_DEMARCATION = ISSUE_38
R3_PAPERS = 0
R4_PAPERS = 0
```
