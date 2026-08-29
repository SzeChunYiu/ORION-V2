# Execution Readiness Audit V1

**Branch:** `research/wave6-contraction-closure-20260827`  
**Status:** fixable-preflight audit before outcome-generating execution.

## Fixed in this tranche

### 1. Execution is now one master backlog

A single machine-readable registry now covers local preflight, BugsInPy pilot/confirmation, CausalBench, Matbench Discovery, component ablations, anti-copy controls, paper-specific experiments, parity, claim updates and external review.

Canonical registry:

`research/experiments/EXECUTION_BACKLOG_V1.json`.

### 2. AI-session handoff updated

`AI_SESSION_REAL_PROBLEM_HANDOFF_V2.md` was useful but did not include the latest response validator, claim updater, P-G identity resolution, full paper-specific compute backlog or the distinction between runnable and externally blocked tasks.

Canonical successor:

`research/experiments/AI_SESSION_EXECUTION_MASTER_HANDOFF_V3.md`.

### 3. Real-problem CI coverage hardened

The workflow is updated to compile and test:

- provider-neutral suite runner;
- workspace materializer;
- response schema validator;
- fresh native evaluator;
- paired analysis;
- evidence-bound paper claim updater.

It also validates both pilot and confirmatory manifests and checks that the execution backlog cannot grant publication/field authority.

### 4. Paper-progress state corrected

The older paper progress receipt still listed foundation saturation as an unfinished prerequisite. That became stale after the bounded internal foundation synthesis earned its clean-pass terminal.

The new progress receipt records conceptual foundation completion while preserving all empirical and external blockers.

### 5. P-G identity collision resolved

Two distinct contingent ideas were using P-G:

- Scientific Knowledge Metabolism;
- Scientific Warrant Factorisation.

Until admission, their stable internal IDs are now:

- `P-G-KM` — knowledge metabolism, active execution-linked candidate;
- `P-G-WF` — warrant factorisation, formal candidate.

Only one may later receive the portfolio paper ID `P-G`, after its admission threshold is satisfied.

## Already runnable without redesign

- local preflight/reference tests;
- manifest validation;
- three-task BugsInPy pilot once agent arms are bound;
- 40-task BugsInPy confirmatory run once agent arms are bound;
- schema validation, fresh evaluator, paired analysis and claim updater;
- component ablation requests once arm executables exist.

## Prepared but externally blocked

### Model/agent execution

Requires actual provider/model executables or interactive AI sessions for each arm.

### CausalBench

Requires exact data and compute binding plus independent domain adjudication.

### Matbench Discovery

Requires exact data/model assets and compute plus independent domain adjudication.

### P-A

Requires held-out remote-domain benchmark corpus and expert donor-card reproduction.

### P-B

Requires formal theorem/countermodel work and two native-domain representation-change studies.

### P-D

Requires blinded independent semantic/evaluator study and a fully instantiated assurance parent federation.

### P-E

Requires genuine prospective or valid time-sliced opportunity follow-up.

### P-F

Requires a predeclared machine-native mechanism and matched-compute cross-domain experiment.

### V1 parity

Requires independent PARITY-C/D reviewer custody and strongest-parent implementation binding under issue #8.

### Flagship

Requires external parent-field demarcation under issue #38 after specialist R3 evidence.

## Scientific stop conditions

Execution should stop and report rather than repair the story when:

- F0 ties or beats F2;
- a component is redundant or harmful;
- ORION only wins through more resources;
- anti-copy controls destroy the apparent gain;
- cross-domain transfer fails;
- independent reviewers reject the semantic decision;
- the result is underpowered;
- data, credentials or evaluator access are unavailable.

Those outcomes update paper scope but do not invalidate the execution programme.

## Current terminal

```text
FIXABLE_PRE_EXECUTION_GAPS = CLOSED_BY_THIS_TRANCHE
LOCAL_EXECUTION_INFRASTRUCTURE = READY_FOR_CI_VALIDATION
OUTCOME_GENERATING_RUNS = OPEN
EXTERNAL_DATA_COMPUTE_AND_REVIEW = OPEN
AUTO_MANUSCRIPT_PROMOTION = FORBIDDEN
FIELD_STATUS = NOT_ESTABLISHED
SUBMISSION_READY = NONE
```
