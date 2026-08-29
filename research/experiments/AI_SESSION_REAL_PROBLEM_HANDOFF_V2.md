# AI-Session Handoff V2 — Run ORION on Real Problems Immediately

**Branch:** `research/wave6-contraction-closure-20260827`  
**Status:** exact runnable handoff. No result, superiority, field or publication claim is embedded.

## 1. What has already been decided

Do not redesign the experiment before running the pilot.

- Pilot registry: `ORION_REAL_PROBLEM_SUITE_V1.json`
- Confirmatory registry: `ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json`
- Analysis plan: `ORION_REAL_PROBLEM_ANALYSIS_PLAN_V1.md`
- Lifecycle: `src/orion_v2/knowledge_metabolism.py`
- Provider-neutral dispatcher: `scripts/run_orion_real_problem_suite.py`
- Fail-closed evaluator: `scripts/evaluate_orion_real_problem_responses_v2.py`
- Paired analysis: `scripts/analyze_orion_real_problem_results.py`
- Paper claim ledger: `papers/verification/KNOWLEDGE_METABOLISM_CLAIM_EXPERIMENT_LEDGER_V1.json`

The study asks whether ORION's full lifecycle improves executable/native scientific outcomes beyond direct generation, same-model reflection and the strongest parent federation under matched resources.

## 2. Fastest valid start

Bind any available arm executables before running. Each command must accept:

```text
--request REQUEST.json --response RESPONSE.json
```

Example:

```bash
export ORION_ARM_SIMPLE_DIRECT='python /path/to/direct_agent.py'
export ORION_ARM_SAME_MODEL_REFLECTION='python /path/to/reflection_agent.py'
export ORION_ARM_F0_PARENT_FEDERATION='python /path/to/f0_agent.py'
export ORION_ARM_F2_ORION_METABOLIC_FULL='python /path/to/orion_agent.py --profile full'
export ORION_ARM_F2_MINUS_DECOMPOSITION='python /path/to/orion_agent.py --profile minus-decomposition'
export ORION_ARM_F2_MINUS_NATIVE_RECOVERY='python /path/to/orion_agent.py --profile minus-native-recovery'
export ORION_ARM_F2_MINUS_COUNTERPROBE='python /path/to/orion_agent.py --profile minus-counterprobe'
```

Then run:

```bash
bash scripts/run_orion_bugsinpy_pilot.sh
```

This single command:

1. compiles the new lifecycle and runners;
2. runs focused unit tests;
3. validates the prospective manifest;
4. checks out the exact BugsInPy commit;
5. bootstraps native framework wrappers;
6. materializes three gold-blind buggy workspaces;
7. verifies the bugs are reproducible;
8. creates arm-specific requests;
9. dispatches every bound agent;
10. preserves missing agents as `CANNOT_CHECK`;
11. evaluates proposals in fresh native workspaces;
12. writes summaries, paired comparisons and component-effect scaffolds.

Default work directory:

```text
.orion-real-problem-suite/
```

## 3. Interactive AI-session route

An interactive AI session can execute requests without a wrapper program.

For each JSON file under:

```text
.orion-real-problem-suite/requests/ARM_ID/
```

perform only the operations allowed by the request and inspect the path in:

```text
task.solver_workspace
```

Do not inspect fixed versions, hidden evaluator workspaces or gold patches.

Write the response to:

```text
.orion-real-problem-suite/responses/ARM_ID/TASK_ID.json
```

Minimum response:

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
  "source_ids_used": ["actual inspected files and test outputs"],
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

For the full ORION arm, explicitly record:

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

A stage with insufficient evidence is `CANNOT_CHECK`; do not manufacture a plausible narrative.

After interactive responses are written:

```bash
python scripts/evaluate_orion_real_problem_responses_v2.py \
  --workdir .orion-real-problem-suite

python scripts/run_orion_real_problem_suite.py \
  --workdir .orion-real-problem-suite summarize

python scripts/analyze_orion_real_problem_results.py \
  --workdir .orion-real-problem-suite
```

## 4. Why this is not a memorization benchmark

The pilot uses real historical bugs, but no single historical benchmark can prove independence from training data. The confirmatory programme therefore combines:

- gold/fixed commits withheld from solver requests;
- fresh evaluator workspaces;
- network-off and retrieval-off arms where feasible;
- newly seeded identifier, label and unit permutations;
- hidden regression/intervention tests;
- dynamically generated counterfactual variants;
- native execution/scientific outcomes as primary endpoints;
- exact source-use receipts;
- post-outcome text similarity as a diagnostic only;
- cases where familiar surface patterns lead to the wrong solution.

Claim only convergent evidence of active problem solving. Do not claim proof that no related training material existed.

## 5. Confirmatory debugging run

After the three-task pilot verifies infrastructure, run the 40-task, eight-project frozen registry:

```bash
export ORION_WORKDIR="$PWD/.orion-real-problem-confirmatory"

python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  --workdir "$ORION_WORKDIR" \
  prepare --benchmarks bugsinpy

python scripts/bootstrap_bugsinpy_environment.py \
  --workdir "$ORION_WORKDIR"

python scripts/materialize_orion_solver_workspaces.py \
  --workdir "$ORION_WORKDIR" \
  --verify-baseline

python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  --workdir "$ORION_WORKDIR" issue

python scripts/run_orion_real_problem_suite.py \
  --manifest research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json \
  --workdir "$ORION_WORKDIR" dispatch

python scripts/evaluate_orion_real_problem_responses_v2.py \
  --workdir "$ORION_WORKDIR"

python scripts/analyze_orion_real_problem_results.py \
  --workdir "$ORION_WORKDIR"
```

For stochastic agents, repeat with at least three frozen seeds/checkpoint identities. Do not count seeds as independent tasks.

## 6. Heavy scientific domains

### CausalBench

Pinned commit:

```text
1a2143cffdc85f835b41ce8d52034be1bf903e71
```

The study must bind data checksum/licence, observational and partial-interventional regimes, held-out intervention identities, seeded label permutations, model/hyperparameter identities, metrics, oracle sensitivity and compute.

Potential ORION value is safer model selection, uncertainty handling, experiment choice, transfer rejection or selective reopening—not an assumed new causal algorithm.

### Matbench Discovery

Pinned commit:

```text
0ba474661cf615d10987ba9a2acb8132943aa491
```

Bind data/model/result identities and vary hidden decision contracts over false-discovery tolerance, robustness, compute/cost, uncertainty, held-out material families and evaluator epoch.

Potential ORION value is scientific decision quality under changing constraints, not reproduction of leaderboard descriptions.

Native benchmark results are registered under:

```text
WORKDIR/native_evaluations/ARM_ID/TASK_ID.json
```

The V2 evaluator imports those content-bound artifacts without granting scientific truth or field authority.

## 7. How results update papers

Only evidence in the frozen evaluation and aggregate directories may update claims.

Possible statuses:

```text
REFERENCE_SEMANTICS
PILOT_EXECUTABLE
SUPPORTED_IN_BOUNDED_TRANCHE
PARENT_TIE
PARENT_WIN
NEGATIVE_RESULT
CANNOT_CHECK
```

The pilot cannot produce:

```text
FIELD_FOUNDED
SUPERIOR_THEORY_PROVEN
TOP_TIER_READY
SUBMISSION_READY
```

P-G survives as a standalone paper only when the lifecycle has a protected residual beyond F0 across at least two materially different domains, with component attribution and matched resources. Otherwise its findings merge into P-A–P-D.

## 8. Session completion checklist

A valid next session ends with:

```text
REFERENCE_TESTS_GREEN_OR_FAILURE_RECORDED
EXACT_BENCHMARK_COMMIT_BOUND
GOLD_BLIND_WORKSPACES_MATERIALIZED
BASELINE_BUGS_REPRODUCED_OR_INVALID_TASKS_RECORDED
REQUESTS_ISSUED
AVAILABLE_ARMS_EXECUTED
MISSING_ARMS_CANNOT_CHECK
FRESH_NATIVE_EVALUATION_COMPLETED
PAIRED_ANALYSIS_WRITTEN
RESOURCE_AND_FAILURE_ARTIFACTS_WRITTEN
PAPER_CLAIMS_NOT_OVERPROMOTED
```
