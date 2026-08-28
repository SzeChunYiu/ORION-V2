#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

WORKDIR="${ORION_WORKDIR:-$REPO_ROOT/.orion-real-problem-suite}"
ARMS="${ORION_PILOT_ARMS:-SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL,F2_MINUS_DECOMPOSITION,F2_MINUS_NATIVE_RECOVERY,F2_MINUS_COUNTERPROBE}"
TASK_COUNT="${ORION_PILOT_TASK_COUNT:-3}"
TIMEOUT="${ORION_PILOT_TIMEOUT_SECONDS:-2700}"

python -m py_compile \
  src/orion_v2/knowledge_metabolism.py \
  scripts/run_orion_real_problem_suite.py \
  scripts/bootstrap_bugsinpy_environment.py \
  scripts/materialize_orion_solver_workspaces.py \
  scripts/evaluate_orion_real_problem_responses_v2.py \
  scripts/analyze_orion_real_problem_results.py

python -m pytest -q \
  tests/unit/test_knowledge_metabolism_wave6.py \
  tests/unit/test_real_problem_suite_runner_wave6.py \
  tests/unit/test_real_problem_evaluator_analysis_wave6.py

python scripts/run_orion_real_problem_suite.py validate
python scripts/run_orion_real_problem_suite.py \
  --workdir "$WORKDIR" \
  prepare --benchmarks bugsinpy

python scripts/bootstrap_bugsinpy_environment.py \
  --workdir "$WORKDIR" \
  --timeout-seconds "$TIMEOUT"

python scripts/materialize_orion_solver_workspaces.py \
  --workdir "$WORKDIR" \
  --timeout-seconds "$TIMEOUT" \
  --verify-baseline

TASKS="$({ ORION_WORKDIR="$WORKDIR" ORION_PILOT_TASK_COUNT="$TASK_COUNT" python - <<'PY'
import json
import os
from pathlib import Path

workdir = Path(os.environ["ORION_WORKDIR"])
limit = int(os.environ["ORION_PILOT_TASK_COUNT"])
tasks = json.loads((workdir / "frozen_tasks.json").read_text())["tasks"]
print(",".join(task["task_id"] for task in tasks[:limit]))
PY
} )"

if [[ -z "$TASKS" ]]; then
  echo "No BugsInPy tasks were frozen" >&2
  exit 1
fi

python scripts/run_orion_real_problem_suite.py \
  --workdir "$WORKDIR" \
  issue --arms "$ARMS" --tasks "$TASKS"

python scripts/run_orion_real_problem_suite.py \
  --workdir "$WORKDIR" \
  dispatch --arms "$ARMS" --tasks "$TASKS" --timeout-seconds "$TIMEOUT"

python scripts/evaluate_orion_real_problem_responses_v2.py \
  --workdir "$WORKDIR" \
  --arms "$ARMS" \
  --tasks "$TASKS" \
  --timeout-seconds "$TIMEOUT"

python scripts/run_orion_real_problem_suite.py \
  --workdir "$WORKDIR" summarize \
  > "$WORKDIR/aggregate/summary.json"

python scripts/analyze_orion_real_problem_results.py \
  --workdir "$WORKDIR" \
  > "$WORKDIR/aggregate/analysis_stdout.json"

cat <<EOF
ORION BugsInPy pilot handoff complete.
Work directory: $WORKDIR
Tasks: $TASKS
Arms: $ARMS

Missing arm executables are recorded as CANNOT_CHECK, not failures.
No field, superiority or publication claim is granted by this pilot.
EOF
