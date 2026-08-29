#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

WORKDIR="${ORION_NATIVE_WORKDIR:-$REPO_ROOT/.orion-native-science-suite}"
MANIFEST="research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json"
ARMS="${ORION_NATIVE_ARMS:-F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL,MACHINE_NATIVE,HUMAN_EXPERT}"

python -m py_compile \
  scripts/run_orion_real_problem_suite.py \
  scripts/materialize_native_result_templates.py \
  scripts/run_pinned_native_benchmark_task.py \
  scripts/bind_native_benchmark_evaluation.py

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" validate

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" \
  --workdir "$WORKDIR" \
  prepare --benchmarks causalbench,matbench_discovery --install

python scripts/run_orion_real_problem_suite.py \
  --manifest "$MANIFEST" \
  --workdir "$WORKDIR" \
  issue --arms "$ARMS"

python scripts/materialize_native_result_templates.py \
  --workdir "$WORKDIR" \
  --arms "$ARMS"

cat <<EOF
Pinned native-science environment prepared.
Work directory: $WORKDIR
Manifest: $MANIFEST
Arms: $ARMS

Next:
1. Bind content-addressed dataset directories and licences.
2. Execute one task with scripts/run_pinned_native_benchmark_task.py.
3. Populate the corresponding native_result_inputs/ARM/TASK.json.
4. Bind all raw metrics/configuration artifacts with scripts/bind_native_benchmark_evaluation.py.
5. Run scripts/evaluate_orion_real_problem_responses_v2.py and the shared analysis pipeline.

No native scientific result has been inferred by preparation alone.
EOF
