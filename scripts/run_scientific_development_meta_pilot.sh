#!/usr/bin/env bash
set -euo pipefail

WORKDIR="${1:-.orion-sd70-meta-pilot}"
TASKS="${ORION_SD70_TASKS:-120}"
TRAIN_EPISODES="${ORION_SD70_TRAIN_EPISODES:-16}"
MAX_CONCURRENCY="${ORION_SD70_MAX_CONCURRENCY:-2}"
ARMS="${ORION_SD70_ARMS:-TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL}"

python scripts/run_scientific_development_meta_suite.py prepare \
  --workdir "$WORKDIR" \
  --tasks "$TASKS" \
  --train-episodes "$TRAIN_EPISODES" \
  --arms "$ARMS"

python scripts/run_scientific_development_meta_suite.py dispatch \
  --workdir "$WORKDIR" \
  --arms "$ARMS" \
  --max-concurrency "$MAX_CONCURRENCY"

python scripts/run_scientific_development_meta_suite.py evaluate \
  --workdir "$WORKDIR" \
  --arms "$ARMS"

printf 'SD70 pilot complete: %s\n' "$WORKDIR/EVALUATION_SUMMARY.json"
