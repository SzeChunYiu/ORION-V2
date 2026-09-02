#!/usr/bin/env bash
#SBATCH --job-name=o2-pra-llm-v2-smoke
#SBATCH --account=lu2026-2-51
#SBATCH --partition=gpua100
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=05:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/v2-smoke-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/v2-smoke-%j.err
# Design V2 development smoke + pre-registered GPC competence check. DEV SPLIT ONLY.
#   part 1 (dev-smoke/): 8 instances (4 F3_P2_CANON + 4 F1_P0), every stage, both models -> pipeline proof
#   part 2 (dev-gpc/):   full dev split (36 instances, 72 arms), revision stage only, then competence-gate
# The protected split is never generated here: the V2 design carries only the sealed seed's commitment
# and no --protected-seed-file is passed. V1 files at $BASE are not touched (V1 R1 array is queued).
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm
V2="$BASE/v2"
# PRA_DEVICE=cuda (one A100-80GB, default) or auto (layer-wise sharding over 2x A100-40GB on gpua100i:
#   sbatch -p gpua100i --gres=gpu:a100:2 --export=ALL,PRA_DEVICE=auto,PRA_WORK_SUFFIX=-2x40 ...)
DEVICE="${PRA_DEVICE:-cuda}"
SUFFIX="${PRA_WORK_SUFFIX:-}"
SMOKE="$BASE/campaign-pra-llm-v2/dev-smoke$SUFFIX"
GPC="$BASE/campaign-pra-llm-v2/dev-gpc$SUFFIX"
export HF_HOME="$BASE/hf-cache" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONHASHSEED=0 CUBLAS_WORKSPACE_CONFIG=:4096:8
PY="$BASE/.venv/bin/python"
RUNNER="$V2/pra_real_llm_audit.py"
DESIGN="$V2/PRA_REAL_LLM_AUDIT_DESIGN_V2.json"
MODELS=(qwen2.5-32b-instruct mistral-small-24b-instruct-2501)
mkdir -p "$SMOKE" "$GPC"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
sha256sum "$RUNNER" "$DESIGN"
"$PY" "$RUNNER" --stage generate-suite --workdir "$SMOKE" --design "$DESIGN" --backend hf
"$PY" "$RUNNER" --stage generate-suite --workdir "$GPC" --design "$DESIGN" --backend hf
# background VRAM sampler (peak reported in the env receipt)
( while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits; sleep 20; done ) > "$BASE/logs/v2-smoke-${SLURM_JOB_ID}.vram" 2>/dev/null &
VRAM_PID=$!
for MODEL in "${MODELS[@]}"; do
  for STAGE in present-gate revision probe kv-channel; do
    /usr/bin/time -f "TIMING part=smoke model=$MODEL stage=$STAGE wall=%e s maxrss=%M KB" \
      "$PY" "$RUNNER" --stage "$STAGE" --workdir "$SMOKE" --design "$DESIGN" --backend hf --model "$MODEL" --split dev --max-instances 8 --families F3_P2_CANON,F1_P0 --device "$DEVICE"
  done
  /usr/bin/time -f "TIMING part=gpc model=$MODEL stage=revision wall=%e s maxrss=%M KB" \
    "$PY" "$RUNNER" --stage revision --workdir "$GPC" --design "$DESIGN" --backend hf --model "$MODEL" --split dev --device "$DEVICE"
  "$PY" "$RUNNER" --stage competence-gate --workdir "$GPC" --design "$DESIGN" --backend hf --model "$MODEL" --split dev --device "$DEVICE"
done
kill "$VRAM_PID" 2>/dev/null || true
"$PY" "$RUNNER" --stage rollup --workdir "$SMOKE" --design "$DESIGN" --backend hf --split dev
"$PY" "$RUNNER" --stage rollup --workdir "$GPC" --design "$DESIGN" --backend hf --split dev
echo V2_SMOKE_DONE
