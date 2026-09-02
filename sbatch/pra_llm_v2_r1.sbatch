#!/usr/bin/env bash
#SBATCH --job-name=o2-pra-llm-v2-r1
#SBATCH --account=lu2026-2-51
#SBATCH --partition=gpua100
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=160G
#SBATCH --time=TIME_PLACEHOLDER
#SBATCH --array=0-1
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/v2-r1-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/v2-r1-%A_%a.err
# PROTECTED RUN, design V2 (campaign-pra-llm-v2). One array task per frozen model. NOT SUBMITTED by the
# design PR. Requires (i) the explicit V2 authorization token from the design JSON and (ii) the sealed
# protected seed file whose sha256 equals design.suite_generator.seed.protected_commitment_sha256.
# Submit ONLY after the design has been reviewed, the protected run authorized, AND the V1 R1 array
# (campaign-pra-llm-r1, job 3563787) has finished - the two protected runs must not compete for gpua100.
# Do not edit the design, suite, runner or gates afterwards.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm
V2="$BASE/v2"
WORK="$BASE/campaign-pra-llm-v2/protected"
export HF_HOME="$BASE/hf-cache" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONHASHSEED=0 CUBLAS_WORKSPACE_CONFIG=:4096:8
PY="$BASE/.venv/bin/python"
RUNNER="$V2/pra_real_llm_audit.py"
DESIGN="$V2/PRA_REAL_LLM_AUDIT_DESIGN_V2.json"
SEED_FILE="${PRA_PROTECTED_SEED_FILE:-$V2/protected_seed.sealed}"
AUTH="${PRA_PROTECTED_AUTHORIZATION:?set PRA_PROTECTED_AUTHORIZATION to the V2 design token to run the protected split}"
test -r "$SEED_FILE" || { echo "sealed protected seed file missing: $SEED_FILE"; exit 1; }
MODELS=(qwen2.5-32b-instruct mistral-small-24b-instruct-2501)
MODEL="${MODELS[$SLURM_ARRAY_TASK_ID]}"
mkdir -p "$WORK/suite"
sha256sum "$RUNNER" "$DESIGN" "$SEED_FILE"
# Suite generation is serialized across array tasks (flock) and re-checked inside the lock; the runner
# refuses to generate the protected split unless the seed file hashes to the design commitment.
flock "$WORK/suite/.generate.lock" bash -c '
  if [ ! -f "$0/suite/suite_protected.sha256.json" ]; then
    "$1" "$2" --stage generate-suite --workdir "$0" --design "$3" --backend hf --protected-seed-file "$4"
  fi' "$WORK" "$PY" "$RUNNER" "$DESIGN" "$SEED_FILE"
test -f "$WORK/suite/suite_protected.sha256.json" || { echo "protected suite missing after generation"; exit 1; }
( while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits; sleep 60; done ) > "$BASE/logs/v2-r1-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.vram" 2>/dev/null &
VRAM_PID=$!
for STAGE in present-gate revision probe kv-channel; do
  /usr/bin/time -f "TIMING model=$MODEL stage=$STAGE wall=%e s maxrss=%M KB" \
    "$PY" "$RUNNER" --stage "$STAGE" --workdir "$WORK" --design "$DESIGN" --backend hf --model "$MODEL" --split protected --protected-authorization "$AUTH"
done
kill "$VRAM_PID" 2>/dev/null || true
# rollup is run once, manually, after both array tasks finish:
#   $PY $RUNNER --stage rollup --workdir $WORK --design $DESIGN --backend hf --split protected --protected-authorization "$AUTH"
# then the sealed seed file is archived next to the rollup (post-run reveal).
echo V2_R1_MODEL_DONE "$MODEL"
