#!/usr/bin/env bash
#SBATCH --job-name=o2-pra-llm-r1
#SBATCH --account=lu2026-2-51
#SBATCH --partition=gpua100
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --time=16:00:00
#SBATCH --array=0-1
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/r1-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/r1-%A_%a.err
# PROTECTED RUN (campaign-pra-llm-r1). One array task per frozen model. Requires the explicit
# authorization token from the design JSON; submit ONLY after the design has been reviewed and
# the protected run has been authorized. Do not edit the design, suite, runner or gates afterwards.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm
WORK="$BASE/campaign-pra-llm-r1/protected"
export HF_HOME="$BASE/hf-cache" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONHASHSEED=0 CUBLAS_WORKSPACE_CONFIG=:4096:8
PY="$BASE/.venv/bin/python"
RUNNER="$BASE/pra_real_llm_audit.py"
DESIGN="$BASE/PRA_REAL_LLM_AUDIT_DESIGN_V1.json"
AUTH="${PRA_PROTECTED_AUTHORIZATION:?set PRA_PROTECTED_AUTHORIZATION to the design token to run the protected split}"
MODELS=(qwen2.5-7b-instruct mistral-7b-instruct-v0.3)
MODEL="${MODELS[$SLURM_ARRAY_TASK_ID]}"
mkdir -p "$WORK"
sha256sum "$RUNNER" "$DESIGN"
# Suite generation is serialized across array tasks (flock) and re-checked inside the lock.
mkdir -p "$WORK/suite"
flock "$WORK/suite/.generate.lock" bash -c '
  if [ ! -f "$0/suite/suite_protected.sha256.json" ]; then
    "$1" "$2" --stage generate-suite --workdir "$0" --design "$3" --backend hf
  fi' "$WORK" "$PY" "$RUNNER" "$DESIGN"
test -f "$WORK/suite/suite_protected.sha256.json" || { echo "protected suite missing after generation"; exit 1; }
for STAGE in present-gate revision probe kv-channel; do
  /usr/bin/time -f "TIMING model=$MODEL stage=$STAGE wall=%e s maxrss=%M KB" \
    "$PY" "$RUNNER" --stage "$STAGE" --workdir "$WORK" --design "$DESIGN" --backend hf --model "$MODEL" --split protected --protected-authorization "$AUTH"
done
# rollup is run once, manually, after both array tasks finish:
#   $PY $RUNNER --stage rollup --workdir $WORK --design $DESIGN --backend hf --split protected --protected-authorization "$AUTH"
echo R1_MODEL_DONE "$MODEL"
