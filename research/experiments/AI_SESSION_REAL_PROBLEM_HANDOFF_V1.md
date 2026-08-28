# AI-Session Handoff — ORION-V2 Real-Problem and Knowledge-Metabolism Study V1

**Branch:** `research/wave6-contraction-closure-20260827`  
**Status:** runnable prospective handoff. No outcome, superiority, field or publication claim is encoded here.

## 1. Mission

Execute the frozen real-problem study without redesigning it:

1. confirm reference semantics;
2. prepare exact benchmark commits;
3. solve gold-blind real tasks under frozen experimental arms;
4. evaluate by execution/native benchmark outcomes;
5. compute component and resource effects;
6. update paper claim ledgers only from produced evidence.

The primary scientific question is whether the full ORION lifecycle—decompose, preserve native meaning, absorb, recombine and challenge—improves justified problem solving beyond direct generation, retrieval, same-model reflection and the strongest parent federation.

## 2. Files that define the experiment

- Registry: `research/experiments/ORION_REAL_PROBLEM_SUITE_V1.json`
- Runner: `scripts/run_orion_real_problem_suite.py`
- Gold-blind workspace materializer: `scripts/materialize_orion_solver_workspaces.py`
- Lifecycle semantics: `src/orion_v2/knowledge_metabolism.py`
- Lifecycle tests: `tests/unit/test_knowledge_metabolism_wave6.py`
- Runner tests: `tests/unit/test_real_problem_suite_runner_wave6.py`
- F0–F3 parent protocol: `research/experiments/FOUNDATION_CANDIDATE_DISCRIMINATOR_PROTOCOL_V1.md`
- Theory dominance: `research/foundation-saturation/THEORY_DOMINANCE_AND_SUPERTHEORY_TEST_V1.md`
- Publication gate: `papers/pipeline/PUBLICATION_READINESS_GATE_2026_V2.md`

Do not substitute a newer benchmark commit, modify outcomes, add an easier baseline or expose a gold fix without creating a new protocol identity.

## 3. Environment

Recommended minimum for the debugging tranche:

- Linux;
- Python 3.12;
- Git;
- Docker or the native toolchain required by BugsInPy projects;
- 4 CPU cores;
- 16 GB RAM;
- 50 GB free disk;
- model credentials or an interactive tool-capable AI session for the chosen arms.

CausalBench and Matbench Discovery require their native datasets and substantially more compute. Their exact repositories and commits are already pinned in the registry.

## 4. Zero-outcome validation

From the repository root:

```bash
python -m pytest -q \
  tests/unit/test_knowledge_metabolism_wave6.py \
  tests/unit/test_real_problem_suite_runner_wave6.py

python scripts/run_orion_real_problem_suite.py validate
```

Expected terminal:

```text
REFERENCE_SEMANTICS = GREEN
PROTECTED_REAL_PROBLEM_RESULTS = NONE
```

A local pass validates orchestration semantics only.

## 5. Prepare the immediate executable tranche

```bash
export ORION_WORKDIR="$PWD/.orion-real-problem-suite"

python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" \
  prepare --benchmarks bugsinpy --install

python scripts/materialize_orion_solver_workspaces.py \
  --workdir "$ORION_WORKDIR" \
  --verify-baseline
```

This produces:

- exact BugsInPy checkout at commit `11c5f1eea954a42132cfd06bf257766a7963e0fd`;
- deterministic first-existing bug selection for pandas, black, fastapi and tornado;
- gold-blind buggy workspaces;
- a frozen task registry;
- optional baseline-reproduction receipts.

The fixed version and gold patch are not present in solver requests.

## 6. Pilot before the full matrix

Start with three tasks and these arms:

```text
SIMPLE_DIRECT
SAME_MODEL_REFLECTION
F0_PARENT_FEDERATION
F2_ORION_METABOLIC_FULL
F2_MINUS_DECOMPOSITION
F2_MINUS_NATIVE_RECOVERY
F2_MINUS_COUNTERPROBE
```

List frozen task IDs:

```bash
python - <<'PY'
import json, os
from pathlib import Path
p=Path(os.environ['ORION_WORKDIR'])/'frozen_tasks.json'
for task in json.loads(p.read_text())['tasks'][:3]:
    print(task['task_id'])
PY
```

Then issue requests, replacing the task list with the printed IDs:

```bash
python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" \
  issue \
  --arms SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL,F2_MINUS_DECOMPOSITION,F2_MINUS_NATIVE_RECOVERY,F2_MINUS_COUNTERPROBE \
  --tasks TASK_1,TASK_2,TASK_3
```

## 7. Two ways an AI session can execute an arm

### Route A — interactive session

For each request file:

1. read the JSON request;
2. inspect only `task.solver_workspace` and permitted sources;
3. run failing tests and inspect code;
4. solve according to the arm contract;
5. return a unified diff, not a modified gold-aware repository;
6. write the required response JSON at the corresponding response path.

Response template:

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
    "confidence": 0.0,
    "failure_class": "..."
  },
  "source_ids_used": ["workspace commit and inspected files"],
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

For `F2_ORION_METABOLIC_FULL`, preserve explicit stage outputs:

```text
INGEST: source/workspace identities actually inspected
DECOMPOSE: claims, assumptions, methods, failures and counterexamples
SORT: dependence, authority and relevance grouping
NATIVE_RECONSTRUCT: what the code/tests/domain currently mean
REDUCE: strongest parent/direct explanation and what it already solves
ABSORB: valid elements retained with assumptions
RECOMBINE: proposed patch/solution and bridge relations
CHALLENGE: discriminator, hidden-failure hypothesis and falsifier
ASSIMILATE_OR_RECYCLE: adopted proposal versus retained negative knowledge
```

Do not fabricate a stage when no evidence supports it; return `CANNOT_CHECK` instead.

### Route B — executable agent commands

Bind an executable for each arm. It must accept `--request` and `--response`:

```bash
export ORION_ARM_SIMPLE_DIRECT='python /path/to/direct_agent.py'
export ORION_ARM_SAME_MODEL_REFLECTION='python /path/to/reflection_agent.py'
export ORION_ARM_F0_PARENT_FEDERATION='python /path/to/f0_agent.py'
export ORION_ARM_F2_ORION_METABOLIC_FULL='python /path/to/orion_agent.py --profile full'
export ORION_ARM_F2_MINUS_DECOMPOSITION='python /path/to/orion_agent.py --profile minus-decomposition'
export ORION_ARM_F2_MINUS_NATIVE_RECOVERY='python /path/to/orion_agent.py --profile minus-native-recovery'
export ORION_ARM_F2_MINUS_COUNTERPROBE='python /path/to/orion_agent.py --profile minus-counterprobe'

python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" \
  dispatch --arms SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL,F2_MINUS_DECOMPOSITION,F2_MINUS_NATIVE_RECOVERY,F2_MINUS_COUNTERPROBE
```

Missing commands produce `CANNOT_CHECK_MISSING_AGENT_COMMAND`; they do not count as losses or successes.

## 8. Evaluate and summarize

```bash
python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" evaluate

python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" summarize \
  | tee "$ORION_WORKDIR/aggregate/summary.txt"
```

The evaluator creates a fresh buggy checkout, applies the proposed diff and runs the native compile/test commands. Solver workspaces are not reused as evaluators.

Do not claim ORION improvement from three pilot tasks. The pilot decides only whether the full experiment is executable and whether the outcome schema needs a pre-outcome correction.

## 9. Full debugging matrix

After a clean pilot, issue all frozen BugsInPy tasks and all frozen arms. Use at least three stochastic repetitions for model-based arms where feasible. Bind seeds and model/checkpoint identities.

Primary comparisons:

```text
F2_FULL vs SIMPLE_DIRECT
F2_FULL vs SAME_MODEL_REFLECTION
F2_FULL vs F0_PARENT_FEDERATION
F2_FULL vs every F2_MINUS component
MACHINE_NATIVE vs human-mimetic controls under the same witness contract
```

Report:

- pass rate and interval;
- critical-failure rate;
- wall time, compute, token and human-labour curves;
- task-level paired differences;
- failure topology;
- cases where simple or parent methods win;
- interaction/synergy effects;
- all missing and `CANNOT_CHECK` outcomes.

A component survives only when its removal or parent replacement produces a protected regression worth its cost.

## 10. CausalBench tranche

Prepare the pinned repository:

```bash
python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" \
  prepare --benchmarks causalbench --install
```

Exact commit:

```text
1a2143cffdc85f835b41ce8d52034be1bf903e71
```

Use native data acquisition and scoring. Before downloading, record dataset identity, licence and checksum. Freeze:

- observational and partial-interventional regimes;
- held-out perturbation subset;
- seeded gene-label permutation generated after protocol freeze;
- candidate model identities and hyperparameters;
- metric/test-sensitivity profile;
- compute budget.

The F2 contribution is not a new causal-discovery algorithm unless evidence supports it. It may instead improve model selection, uncertainty representation, invalid-transfer detection, experiment choice or selective reopening beyond the strongest causal parent product.

## 11. Matbench Discovery tranche

Prepare the pinned repository:

```bash
python scripts/run_orion_real_problem_suite.py \
  --workdir "$ORION_WORKDIR" \
  prepare --benchmarks matbench_discovery --install
```

Exact commit:

```text
0ba474661cf615d10987ba9a2acb8132943aa491
```

Freeze native benchmark data and model-result identities. Use private, outcome-blind decision contracts that vary:

- accuracy versus compute/cost;
- robustness under held-out material families;
- false-discovery tolerance;
- uncertainty requirement;
- resource constraint;
- model/evaluator epoch.

The study asks whether ORION makes safer or more effective scientific model-selection and discovery decisions—not whether it can reproduce published leaderboard prose.

## 12. Anti-copy and machine-native evidence

No single test can prove absence of training-data influence. Use converging controls:

1. gold fixes and fixed commits withheld;
2. network disabled during solution where feasible;
3. newly seeded identifier/gene/unit permutations;
4. hidden regression/intervention tests;
5. dynamically generated counterfactual variants;
6. execution and scientific outcomes as primary endpoints;
7. text similarity to known fixes used only as a post-outcome diagnostic;
8. source identities logged;
9. retrieval-off and no-memory controls;
10. machine-native arm required to expose the same scientific witness without imitating a human transcript.

A correct low-similarity solution supports independent problem solving more strongly than a verbal answer. A high-similarity solution is not automatically copying, and a different-looking wrong solution is not intelligence.

## 13. Paper update rule

After every completed tranche, update only claims whose evidence identity exists in:

- `evaluations/`;
- `aggregate/arm_metrics.json`;
- resource and component-effect artifacts;
- independent adjudication receipts.

Allowed claim statuses:

```text
REFERENCE_SEMANTICS
PILOT_EXECUTABLE
SUPPORTED_IN_BOUNDED_TRANCHE
PARENT_TIE
PARENT_WIN
NEGATIVE_RESULT
CANNOT_CHECK
```

Do not use `FIELD_FOUNDED`, `SUPERIOR`, `TOP_TIER_READY` or `SUBMISSION_READY` unless the publication gate independently passes.

## 14. Immediate completion terminal for the next AI session

A single session should finish with all of the following, even when the scientific result is negative:

```text
RUNNER_VALIDATED
BUGSINPY_WORKSPACES_MATERIALIZED
PILOT_REQUESTS_ISSUED
AVAILABLE_ARMS_EXECUTED
RESPONSES_SCHEMA_VALIDATED
NATIVE_EVALUATION_RUN
SUMMARY_WRITTEN
FAILURES_RECORDED
CLAIMS_NOT_OVERPROMOTED
```

If credentials, data or compute are missing, record exactly which arm/task is `CANNOT_CHECK` and continue every independently executable part.
