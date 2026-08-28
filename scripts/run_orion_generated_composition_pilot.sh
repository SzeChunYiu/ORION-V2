#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

WORKDIR="${ORION_GC1_WORKDIR:-$REPO_ROOT/.orion-generated-composition-suite}"
ARMS="${ORION_GC1_ARMS:-SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL}"
TASK_COUNT="${ORION_GC1_TASK_COUNT:-24}"
SEED="${ORION_GC1_SEED:-20260828}"
MAX_CONCURRENCY="${ORION_GC1_MAX_CONCURRENCY:-2}"

python -m py_compile \
  src/orion_v2/unified_diff_interface.py \
  scripts/orion_codex_arms.py \
  scripts/run_orion_generated_composition_suite.py

python -m pytest -q \
  tests/unit/test_unified_diff_interface_wave6.py \
  tests/unit/test_generated_composition_suite_wave6.py

python scripts/run_orion_generated_composition_suite.py generate \
  --workdir "$WORKDIR" \
  --arms "$ARMS" \
  --task-count "$TASK_COUNT" \
  --seed "$SEED" \
  --force

python scripts/run_orion_generated_composition_suite.py dispatch \
  --workdir "$WORKDIR" \
  --arms "$ARMS" \
  --max-concurrency "$MAX_CONCURRENCY"

python scripts/run_orion_generated_composition_suite.py evaluate \
  --workdir "$WORKDIR" \
  --arms "$ARMS"

python scripts/run_orion_generated_composition_suite.py analyze \
  --workdir "$WORKDIR" \
  --arms "$ARMS" \
  --seed "$SEED"

cat "$WORKDIR/EXECUTION_SUMMARY.md"

echo
printf '%s\n' \
  "E70-GC1 generated-composition pilot complete." \
  "Workdir: $WORKDIR" \
  "Arms: $ARMS" \
  "Tasks: $TASK_COUNT" \
  "Seed: $SEED" \
  "This is secondary fresh anti-copy/composition evidence and cannot replace E30/E40/E50."
