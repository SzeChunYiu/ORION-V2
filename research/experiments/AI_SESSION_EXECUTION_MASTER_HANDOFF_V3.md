# AI Session Execution Master Handoff V3

**Branch:** `research/wave6-contraction-closure-20260827`  
**Canonical foundation issue:** #41  
**Paper programme:** #7  
**External demarcation:** #38  
**Status:** executable handoff for outcome-generating work only. Protocol redesign is prohibited after outcome access unless an infrastructure defect creates a new run identity.

## 1. Mission

The next AI session should execute the already prepared ORION-V2 evidence programme, not continue general prose work.

The goal is to determine, under matched resources and fail-closed evaluation, whether the complete ORION lifecycle:

`INGEST -> DECOMPOSE -> SORT -> NATIVE_RECONSTRUCT -> REDUCE -> ABSORB -> RECOMBINE -> CHALLENGE -> ASSIMILATE_OR_RECYCLE`

solves real problems better than direct generation, same-model reflection and the strongest parent federation, while identifying components that are necessary, contextual, parent-replaceable, redundant drag or harmful.

No run may self-grant field status, superiority, novelty, submission readiness or journal acceptance.

## 2. Canonical execution artifacts

Use these exact repository artifacts before creating anything new:

- `research/experiments/EXECUTION_BACKLOG_V1.json`
- `research/experiments/ORION_REAL_PROBLEM_SUITE_V1.json`
- `research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json`
- `research/experiments/ORION_REAL_PROBLEM_ANALYSIS_PLAN_V1.md`
- `src/orion_v2/knowledge_metabolism.py`
- `scripts/run_orion_real_problem_suite.py`
- `scripts/bootstrap_bugsinpy_environment.py`
- `scripts/materialize_orion_solver_workspaces.py`
- `scripts/validate_orion_agent_responses.py`
- `scripts/evaluate_orion_real_problem_responses_v2.py`
- `scripts/analyze_orion_real_problem_results.py`
- `scripts/update_paper_claims_from_real_results.py`
- `papers/verification/KNOWLEDGE_METABOLISM_CLAIM_EXPERIMENT_LEDGER_V1.json`

Before running, record the exact ORION branch SHA and all external model/checkpoint/provider identities in the run receipt.

## 3. Preflight — mandatory and outcome blind

Run first:

```bash
python -m pip install -e . pytest
python -m py_compile src/orion_v2/knowledge_metabolism.py
python -m py_compile scripts/run_orion_real_problem_suite.py
python -m py_compile scripts/materialize_orion_solver_workspaces.py
python -m py_compile scripts/validate_orion_agent_responses.py
python -m py_compile scripts/evaluate_orion_real_problem_responses_v2.py
python -m py_compile scripts/analyze_orion_real_problem_results.py
python -m py_compile scripts/update_paper_claims_from_real_results.py

python -m pytest -q \
  tests/unit/test_knowledge_metabolism_wave6.py \
  tests/unit/test_real_problem_suite_runner_wave6.py \
  tests/unit/test_real_problem_evaluator_analysis_wave6.py \
  tests/unit/test_real_problem_claim_update_wave6.py

python scripts/run_orion_real_problem_suite.py validate
python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  validate
```

If this fails, fix only the infrastructure defect, record it under `research/failures/`, increment the run identity and rerun preflight. Do not inspect gold outcomes while fixing infrastructure.

## 4. Bind arms

Each automated arm executable must accept:

```text
--request REQUEST.json --response RESPONSE.json
```

Bind, where available:

```bash
export ORION_ARM_SIMPLE_DIRECT='...'
export ORION_ARM_RETRIEVAL_ONLY='...'
export ORION_ARM_SAME_MODEL_REFLECTION='...'
export ORION_ARM_F0_PARENT_FEDERATION='...'
export ORION_ARM_F2_ORION_METABOLIC_FULL='...'
export ORION_ARM_F2_MINUS_DECOMPOSITION='...'
export ORION_ARM_F2_MINUS_NATIVE_RECOVERY='...'
export ORION_ARM_F2_MINUS_COUNTERPROBE='...'
export ORION_ARM_F2_MINUS_SELECTIVE_REOPEN='...'
export ORION_ARM_MACHINE_NATIVE='...'
```

Human expert arms are separately scheduled and never simulated by the subject model.

For every arm freeze:

- provider/model/checkpoint/version;
- system prompt or executable digest;
- retrieval/network policy;
- token/compute budget;
- wall-time ceiling;
- tool permissions;
- human minutes;
- seed/temperature or deterministic settings.

A later resource increase creates a new comparator identity.

## 5. T1 — three-task BugsInPy pilot

Fastest valid route:

```bash
bash scripts/run_orion_bugsinpy_pilot.sh
```

Required terminal:

```text
EXACT_BENCHMARK_COMMIT_BOUND
GOLD_BLIND_WORKSPACES_MATERIALIZED
BASELINE_BUGS_REPRODUCED_OR_INVALID_TASKS_RECORDED
REQUESTS_ISSUED
AVAILABLE_ARMS_EXECUTED
RESPONSES_SCHEMA_VALIDATED
FRESH_NATIVE_EVALUATION_COMPLETED
PAIRED_ANALYSIS_WRITTEN
RESOURCE_AND_FAILURE_ARTIFACTS_WRITTEN
NO_CLAIM_OVERPROMOTION
```

T1 is infrastructure evidence only. It cannot support superiority, field status or submission readiness.

## 6. T2 — 40-task / eight-project confirmatory debugging run

After T1 infrastructure is valid:

```bash
export ORION_WORKDIR="$PWD/.orion-real-problem-confirmatory"

python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  --workdir "$ORION_WORKDIR" \
  prepare --benchmarks bugsinpy

python scripts/bootstrap_bugsinpy_environment.py --workdir "$ORION_WORKDIR"

python scripts/materialize_orion_solver_workspaces.py \
  --workdir "$ORION_WORKDIR" --verify-baseline

python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  --workdir "$ORION_WORKDIR" issue

python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  --workdir "$ORION_WORKDIR" dispatch

python scripts/validate_orion_agent_responses.py --workdir "$ORION_WORKDIR"
python scripts/evaluate_orion_real_problem_responses_v2.py --workdir "$ORION_WORKDIR"
python scripts/run_orion_real_problem_suite.py --workdir "$ORION_WORKDIR" summarize
python scripts/analyze_orion_real_problem_results.py --workdir "$ORION_WORKDIR"
```

For stochastic arms execute at least three frozen repetitions. Repetitions are nested within task and never counted as independent tasks.

Do not remove hard tasks after seeing which system fails.

## 7. T3a — CausalBench

Pinned commit:

```text
1a2143cffdc85f835b41ce8d52034be1bf903e71
```

Before execution bind:

- exact dataset identity/checksum/licence;
- observational and partial-intervention data identities;
- held-out intervention subset;
- seeded label permutation;
- model/hyperparameter versions;
- graph metrics and oracle-sensitivity tests;
- CPU/GPU and time budget;
- independent native-domain adjudicator.

Run F0 and F2 against the same native causal algorithms and data. ORION may improve model selection, uncertainty handling, experiment choice, transfer rejection, diagnostic reopening or result assurance; it must not receive a stronger causal learner unless the same learner is available to F0.

Primary paper mapping: P-B, P-C, P-D, P-F and the flagship.

## 8. T3b — Matbench Discovery

Pinned commit:

```text
0ba474661cf615d10987ba9a2acb8132943aa491
```

Before execution bind:

- exact dataset/model/result identities;
- held-out material family;
- unit/identifier permutation seed;
- uncertainty and false-discovery rule;
- cost/resource constraints;
- evaluator epoch/version;
- CPU/GPU and time budget;
- independent materials-domain adjudicator.

ORION is evaluated on decision quality, robustness, uncertainty, false-discovery control, selective reopening and resource-aware choice around strong native materials models. It does not receive credit for merely rerunning a leaderboard model.

Primary paper mapping: P-B, P-C, P-D, P-F and the flagship.

## 9. Component and drag study

After T2 and at least one T3 domain, compute:

- FULL F2;
- MINUS decomposition/sorting;
- MINUS native recovery;
- MINUS counterprobe/challenge;
- MINUS selective reopening;
- F0 parent replacement;
- simplified/merged variant if indicated;
- registered pair interactions where synergy is plausible.

Every component must terminate as:

```text
NECESSARY
PARENT_REPLACEABLE
CONTEXTUAL
REDUNDANT_DRAG
HARMFUL
CANNOT_CHECK
```

Report quality and cost separately. A component that raises average success but creates a critical source, authority or false-completion failure is not admitted as a universal improvement.

## 10. Anti-memorization / active-solving controls

Do not claim proof of “not in training”. Instead report converging evidence:

- gold/fixed commits withheld;
- fresh evaluator workspaces;
- network/retrieval-off arms where feasible;
- identifier/label/unit permutations generated after protocol freeze;
- hidden regression/intervention tests;
- dynamic counterfactual variants;
- source-use receipts;
- post-outcome similarity diagnostic only;
- surface-template trap cases where memorized-looking behaviour is wrong.

Primary evidence is executable/native success under changed hidden conditions.

## 11. Claim update — no direct manuscript editing

After analysis:

```bash
python scripts/update_paper_claims_from_real_results.py \
  --workdir "$ORION_WORKDIR"
```

The updater may propose claim-state changes only. It must not edit manuscripts automatically.

Allowed evidence terminals include:

```text
PILOT_OR_UNDERPOWERED
SUPPORTED_IN_BOUNDED_DEBUGGING_TRANCHE
PARENT_TIE_OR_WIN
NEGATIVE_RESULT
CANNOT_CHECK
P_G_STANDALONE_CANDIDATE_FOR_INDEPENDENT_REVIEW
```

Even a positive bounded result must leave:

```text
FIELD_STATUS = NOT_ESTABLISHED
SUBMISSION_READINESS = NOT_ESTABLISHED
```

until the paper-specific R3/R4 gates are satisfied.

## 12. Paper-specific computation backlog beyond the shared suite

### P-A

Run the hidden-known-parent benchmark with held-out remote domains, strongest retrieval/analogy/LBD/MDL/expert union, resource matching, false-analogy hard gates and expert donor-card reproduction.

### P-B

Complete native known-answer relation suites; obtain at least one formal composition theorem/obstruction/countermodel; run two naturalistic representation/measurement changes with native experts.

### P-C

Use T2/T3 plus fresh expert-owned scientific tasks to measure justified terminals, false completion, minimum escalation, self-model calibration, exploration/constructive action value, resilience and component drag.

### P-D

Run dependence positive/negative controls, test/oracle adequacy, assurance/argumentation F0 product, criticism-uptake study, dynamic evaluator cases and blinded adjudication.

### P-E

Only execute if a genuinely prospective or time-sliced opportunity cohort with later-outcome follow-up is available. Otherwise merge into P-C.

### P-F

Freeze one machine-native mechanism before outcomes, run matched-compute human-mimetic/F0/hybrid controls, mechanism ablation, external-witness scoring and second-domain transfer.

### P-G candidates

Use `P_G_CANDIDATE_IDENTITY_RESOLUTION_V1.md`. Only one future portfolio ID may be P-G. Neither candidate is admitted without its explicit theorem/protected-result threshold.

## 13. Independent evaluation tasks

The AI execution session may prepare packets but may not fabricate reviewer identities.

Open external tasks include:

- PARITY-C/D reviewer custody under issue #8;
- native domain adjudicators for T3;
- external Machine Epistemics demarcation under issue #38;
- hostile editorial review after R3 evidence freezes.

Unavailable independent humans/models are `CANNOT_CHECK`, not permission to self-review.

## 14. Required final artifacts from the execution session

At minimum produce:

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

Record all invalid tasks, timeouts, missing credentials, unavailable datasets and failed evaluators explicitly.

## 15. Final stop rule for the AI session

Do not continue changing protocols after substantive outcome access. End the session when all runnable tasks are executed or explicitly `CANNOT_CHECK`, results are frozen, claim updates are proposed, and unresolved work is written back to the master execution issue.

The session may conclude with parent wins or negative results. That is successful scientific execution.
