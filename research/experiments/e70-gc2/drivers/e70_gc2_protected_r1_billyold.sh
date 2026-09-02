#!/usr/bin/env bash
# E70-GC2 R1 protected dispatch on the fallback host (billy-old): same pipeline, nohup.
set -euo pipefail
BASE=/home/billy/orion-v2-e70gc2
export ORION_CODEX_BIN="$BASE/codex150/node_modules/.bin/codex"
export ORION_CODEX_MODEL=gpt-5.6-terra
export ORION_GC2_WORKDIR="$BASE/campaign-e70-gc2-r1"
export ORION_GC2_MAX_CONCURRENCY="${ORION_GC2_MAX_CONCURRENCY:-3}"
export ORION_GC2_STAGE="${ORION_GC2_STAGE:-all}"
export PYTHONPATH="$BASE/repo/src"
cd "$BASE/repo"
echo "host=$(hostname) date=$(date -u +%FT%TZ) commit=$(git rev-parse HEAD) codex=$($ORION_CODEX_BIN --version) model=$ORION_CODEX_MODEL"
bash scripts/run_orion_generated_composition_gc2_pilot.sh
