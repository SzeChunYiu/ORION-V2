#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SOURCE_WORKDIR="${ORION_SOURCE_WORKDIR:-$REPO_ROOT/.orion-real-problem-suite}"
FRESH_WORKDIR="${ORION_FRESH_WORKDIR:-$REPO_ROOT/.orion-fresh-counterfactual-suite}"
ARMS="${ORION_FRESH_ARMS:-SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL,F2_MINUS_DECOMPOSITION,F2_MINUS_NATIVE_RECOVERY,F2_MINUS_COUNTERPROBE,MACHINE_NATIVE}"
TASK_COUNT="${ORION_FRESH_TASK_COUNT:-5}"
SEED="${ORION_FRESH_SEED:-20260828}"
TIMEOUT="${ORION_FRESH_TIMEOUT_SECONDS:-2700}"
MANIFEST="research/experiments/ORION_FRESH_COUNTERFACTUAL_REPAIR_SUITE_V1.json"

python -m py_compile \
  scripts/generate_fresh_bugsinpy_counterfactuals.py \
  scripts/enrich_fresh_counterfactual_support_mounts.py \
  scripts/validate_orion_agent_responses.py \
  scripts/evaluate_fresh_bugsinpy_counterfactuals.py \
  scripts/analyze_orion_real_problem_results.py \
  scripts/summarize_orion_anti_copy_controls.py \
  scripts/update_paper_claims_from_real_results.py

python -m pytest -q \
  tests/unit/test_fresh_counterfactual_generator_wave6.py \
  tests/unit/test_real_problem_evaluator_analysis_wave6.py \
  tests/unit/test_real_problem_claim_update_wave6.py

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" validate

# The fresh generator needs a pinned, bootstrapped BugsInPy source environment.
if [[ ! -f "$SOURCE_WORKDIR/frozen_tasks.json" ]]; then
  python scripts/run_orion_real_problem_suite.py \
    --workdir "$SOURCE_WORKDIR" \
    prepare --benchmarks bugsinpy
  python scripts/bootstrap_bugsinpy_environment.py \
    --workdir "$SOURCE_WORKDIR" \
    --timeout-seconds "$TIMEOUT"
  python scripts/materialize_orion_solver_workspaces.py \
    --workdir "$SOURCE_WORKDIR" \
    --timeout-seconds "$TIMEOUT"
fi

rm -rf "$FRESH_WORKDIR"
python scripts/generate_fresh_bugsinpy_counterfactuals.py \
  --source-workdir "$SOURCE_WORKDIR" \
  --output-workdir "$FRESH_WORKDIR" \
  --count "$TASK_COUNT" \
  --seed "$SEED" \
  --timeout-seconds "$TIMEOUT"

python scripts/enrich_fresh_counterfactual_support_mounts.py \
  --source-workdir "$SOURCE_WORKDIR" \
  --fresh-workdir "$FRESH_WORKDIR"

TASKS="$({ ORION_FRESH_WORKDIR="$FRESH_WORKDIR" python - <<'PY'
import json
import os
from pathlib import Path

workdir = Path(os.environ["ORION_FRESH_WORKDIR"])
tasks = json.loads((workdir / "frozen_tasks.json").read_text())["tasks"]
print(",".join(task["task_id"] for task in tasks))
PY
} )"

if [[ -z "$TASKS" ]]; then
  echo "No fresh counterfactual tasks were generated" >&2
  exit 2
fi

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" \
  --workdir "$FRESH_WORKDIR" \
  issue --arms "$ARMS" --tasks "$TASKS"

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" \
  --workdir "$FRESH_WORKDIR" \
  dispatch --arms "$ARMS" --tasks "$TASKS" --timeout-seconds "$TIMEOUT"

python scripts/validate_orion_agent_responses.py \
  --manifest "$MANIFEST" \
  --workdir "$FRESH_WORKDIR" \
  --arms "$ARMS" \
  --tasks "$TASKS" || true

python scripts/evaluate_fresh_bugsinpy_counterfactuals.py \
  --manifest "$MANIFEST" \
  --workdir "$FRESH_WORKDIR" \
  --arms "$ARMS" \
  --tasks "$TASKS" \
  --timeout-seconds "$TIMEOUT"

python scripts/analyze_orion_real_problem_results.py \
  --workdir "$FRESH_WORKDIR" \
  > "$FRESH_WORKDIR/aggregate/analysis_stdout.json"

python scripts/summarize_orion_anti_copy_controls.py \
  --historical-workdir "$SOURCE_WORKDIR" \
  --fresh-workdir "$FRESH_WORKDIR" \
  --output-workdir "$SOURCE_WORKDIR" \
  > "$SOURCE_WORKDIR/aggregate/anti_copy_stdout.json"

if [[ -f "$SOURCE_WORKDIR/aggregate/analysis.json" ]]; then
  python scripts/update_paper_claims_from_real_results.py \
    --workdir "$SOURCE_WORKDIR" \
    > "$SOURCE_WORKDIR/aggregate/paper_claim_updates_stdout.json"
fi

cat <<EOF
ORION fresh-counterfactual pilot complete.
Source workdir: $SOURCE_WORKDIR
Fresh workdir: $FRESH_WORKDIR
Generated tasks: $TASKS
Arms: $ARMS
Seed: $SEED

Private gold patches and fixed Git histories were not mounted into solver workspaces.
Missing or malformed agents remain CANNOT_CHECK.
This run supplies bounded anti-copy evidence only; it cannot prove absence of all training-data influence.
EOF
