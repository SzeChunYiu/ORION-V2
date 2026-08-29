# AI-Session Handoff V3 — Execute ORION Real-Problem Evidence Programme

**Branch:** `research/wave6-contraction-closure-20260827`  
**Canonical status:** immediate runnable handoff; supersedes V1/V2 where commands differ. No result, superiority, field or publication status is encoded.

## 1. Fast path

Bind available arm executables. Each executable accepts:

```text
--request REQUEST.json --response RESPONSE.json
```

Example:

```bash
export ORION_ARM_SIMPLE_DIRECT='python /agents/direct.py'
export ORION_ARM_SAME_MODEL_REFLECTION='python /agents/reflection.py'
export ORION_ARM_F0_PARENT_FEDERATION='python /agents/f0.py'
export ORION_ARM_F2_ORION_METABOLIC_FULL='python /agents/orion.py --profile full'
export ORION_ARM_F2_MINUS_DECOMPOSITION='python /agents/orion.py --profile minus-decomposition'
export ORION_ARM_F2_MINUS_NATIVE_RECOVERY='python /agents/orion.py --profile minus-native-recovery'
export ORION_ARM_F2_MINUS_COUNTERPROBE='python /agents/orion.py --profile minus-counterprobe'
```

Then execute:

```bash
bash scripts/run_orion_bugsinpy_pilot.sh
bash scripts/run_orion_fresh_counterfactual_pilot.sh
```

The first command runs the three-task historical-bug infrastructure pilot. The second generates fresh post-freeze defects and tests active problem solving without exposing their reverse patches or original fixed Git histories.

## 2. Optional container isolation

For an agent image that contains its own model/tool client:

```bash
export ORION_AGENT_IMAGE='your-agent-image:immutable-tag'
export ORION_AGENT_COMMAND='python /app/agent.py'
export ORION_AGENT_NETWORK_MODE='none'

export ORION_ARM_F2_ORION_METABOLIC_FULL='python scripts/run_orion_agent_in_container.py'
```

The container adapter mounts only:

- the public request;
- the solver workspace;
- explicitly declared read-only support paths;
- the response directory.

Private evaluator and gold directories are not mounted. Remote API agents require an explicit network-mode change and a named environment-variable allowlist; record that weaker isolation in the resource/access receipt.

## 3. Required response boundary

Every arm writes `orion.v2.agent-response.v1`. The response validator runs before any native evaluator.

Minimum fields:

```json
{
  "schema_version": "orion.v2.agent-response.v1",
  "task_id": "TASK_ID",
  "arm_id": "ARM_ID",
  "status": "PROPOSAL_READY_FOR_EXECUTION_TEST",
  "proposed_patch_or_artifact": {
    "type": "unified_diff",
    "content": "diff --git ..."
  },
  "diagnosis": {
    "observed_failure": "...",
    "candidate_causes": ["..."],
    "selected_cause": "...",
    "failure_class": "...",
    "confidence": 0.0
  },
  "source_ids_used": ["actual inspected files, outputs and allowed sources"],
  "assumptions": ["..."],
  "uncertainty": "...",
  "discriminator_or_tests": ["..."],
  "falsifier": "...",
  "requested_authority": "EXECUTION_TEST_ONLY",
  "resource_receipt": {
    "wall_time_seconds": 0,
    "model_tokens": null,
    "human_minutes": 0,
    "external_tool_calls": 0
  }
}
```

The full F2 arm also supplies a non-empty `metabolic_stages` object containing:

```text
INGEST
DECOMPOSE
SORT
NATIVE_RECONSTRUCT
REDUCE
ABSORB
RECOMBINE
CHALLENGE
ASSIMILATE_OR_RECYCLE
```

Unknown information is recorded explicitly as `CANNOT_CHECK`; do not manufacture stage narratives.

## 4. What ORION “knowledge metabolism” means operationally

```text
INGEST                bind actual source/workspace identities
DECOMPOSE             separate observations, claims, assumptions, methods,
                      relations, failures, counterexamples and authority constraints
SORT                  retain provenance, dependence, scope and relevance
NATIVE_RECONSTRUCT    recover what the parent code/theory/practice means locally
REDUCE                 determine what direct or mature parent methods already solve
ABSORB                  retain valid pieces with their assumptions and ceilings
RECOMBINE              construct a solution, model, experiment or scientific proposal
CHALLENGE              generate a discriminator, hidden-failure test and falsifier
ASSIMILATE_OR_RECYCLE  adopt only what passes; retain refutations and unused material
                       as negative knowledge rather than deleting them
```

The protein-digestion and recycling-centre analogies motivated this lifecycle. They are not evidence that it works. Its value is decided by execution, native scientific outcomes, component ablations and resource costs.

## 5. Pilot artifacts

Historical pilot default:

```text
.orion-real-problem-suite/
```

Fresh counterfactual default:

```text
.orion-fresh-counterfactual-suite/
```

Inspect:

```text
frozen_tasks.json
requests/
responses/
response_validation/
evaluations/
aggregate/arm_metrics.json
aggregate/paired_comparisons.json
aggregate/component_effects.json
aggregate/resource_pareto.json
aggregate/failure_ledger.json
aggregate/anti_copy_controls.json
aggregate/paper_claim_updates.json
```

Missing agent commands, data, credentials or evaluators remain `CANNOT_CHECK`; they are not scored as losses or successes.

## 6. Confirmatory debugging study

The frozen confirmatory manifest specifies at least 40 paired BugsInPy tasks across eight projects and at least three repetitions for stochastic arms:

```bash
export ORION_WORKDIR="$PWD/.orion-real-problem-confirmatory"
export MANIFEST='research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json'

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" --workdir "$ORION_WORKDIR" \
  prepare --benchmarks bugsinpy
python scripts/bootstrap_bugsinpy_environment.py --workdir "$ORION_WORKDIR"
python scripts/materialize_orion_solver_workspaces.py \
  --workdir "$ORION_WORKDIR" --verify-baseline
python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" --workdir "$ORION_WORKDIR" issue
python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" --workdir "$ORION_WORKDIR" dispatch
python scripts/validate_orion_agent_responses.py \
  --manifest "$MANIFEST" --workdir "$ORION_WORKDIR" || true
python scripts/evaluate_orion_real_problem_responses_v2.py \
  --workdir "$ORION_WORKDIR"
python scripts/analyze_orion_real_problem_results.py \
  --workdir "$ORION_WORKDIR"
python scripts/update_paper_claims_from_real_results.py \
  --workdir "$ORION_WORKDIR"
```

Do not count model seeds as independent tasks. Preserve every task-level result, parent win, simple-control win and failure.

## 7. Native causal and materials studies

Pinned repositories:

```text
CausalBench:
1a2143cffdc85f835b41ce8d52034be1bf903e71

Matbench Discovery:
0ba474661cf615d10987ba9a2acb8132943aa491
```

Run their native commands and record results using:

```bash
python scripts/bind_native_benchmark_evaluation.py \
  --workdir WORKDIR \
  --task-id TASK_ID \
  --arm-id ARM_ID \
  --result native-result.json \
  --artifact result-file-1 \
  --artifact result-file-2
```

Use `research/experiments/NATIVE_BENCHMARK_RESULT_TEMPLATE_V1.json` as the schema template. The binder requires exact data, command, evaluator, resource and source identities and stores artifact SHA-256 receipts.

## 8. Anti-copy interpretation

The experiment uses converging controls:

- gold/fixed solutions withheld;
- fresh post-freeze defects;
- stripped source Git history in fresh tasks;
- private reverse patches;
- network-off/container controls where feasible;
- hidden/native tests and interventions;
- seeded identifier, label and unit changes;
- execution and scientific outcomes as primary scores;
- source-use receipts;
- retrieval-off/no-memory controls;
- solution similarity only after primary scoring.

A successful fresh counterfactual repair supports bounded active problem solving. It does not prove the model has never encountered related code or establish general intelligence.

## 9. Result-to-paper custody

`update_paper_claims_from_real_results.py` writes a review proposal only. It never edits manuscript prose or the canonical claim ledger.

Allowed automatic proposed statuses include:

```text
PILOT_OR_UNDERPOWERED
SUPPORTED_IN_BOUNDED_DEBUGGING_TRANCHE
PARENT_TIE_OR_WIN
COMPONENT_VALUE_CANDIDATE_IN_BOUNDED_TRANCHE
CANNOT_CHECK
P_G_STANDALONE_CANDIDATE_FOR_INDEPENDENT_REVIEW
P_G_MERGE_OR_CANNOT_CHECK
```

The following remain externally governed and cannot be produced by this runner:

```text
FIELD_FOUNDED
SUPERIOR_THEORY_PROVEN
TOP_TIER_READY
SUBMISSION_READY
```

## 10. Session completion terminal

A valid execution session ends with:

```text
REFERENCE_TESTS_GREEN_OR_FAILURE_RECORDED
EXACT_BENCHMARK_IDENTITIES_BOUND
GOLD_BLIND_WORKSPACES_MATERIALIZED
BASELINE_FAILURES_REPRODUCED_OR_INVALID_TASKS_RECORDED
REQUESTS_ISSUED
AVAILABLE_ARMS_EXECUTED
MISSING_ARMS_CANNOT_CHECK
RESPONSES_VALIDATED
FRESH_NATIVE_EVALUATION_COMPLETED
PAIRED_ANALYSIS_WRITTEN
ANTI_COPY_CONTROLS_WRITTEN
RESOURCE_AND_FAILURE_ARTIFACTS_WRITTEN
PAPER_CLAIM_UPDATE_PROPOSAL_WRITTEN
CLAIMS_NOT_OVERPROMOTED
```
