#!/usr/bin/env bash
#SBATCH --job-name=o2-pra-llm-smoke
#SBATCH --account=lu2026-2-51
#SBATCH --partition=gpua100
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=01:30:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/smoke-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/smoke-%j.err
# Development smoke test ONLY: dev split, 8 instances (4 F3_P2_CANON + 4 F1_P0 so the probe split is non-empty).
# Never touches the protected split.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm
WORK="$BASE/campaign-pra-llm-r1/dev-smoke"
export HF_HOME="$BASE/hf-cache" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONHASHSEED=0 CUBLAS_WORKSPACE_CONFIG=:4096:8
PY="$BASE/.venv/bin/python"
RUNNER="$BASE/pra_real_llm_audit.py"
DESIGN="$BASE/PRA_REAL_LLM_AUDIT_DESIGN_V1.json"
mkdir -p "$WORK"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
sha256sum "$RUNNER" "$DESIGN"
"$PY" "$RUNNER" --stage generate-suite --workdir "$WORK" --design "$DESIGN" --backend hf
for MODEL in qwen2.5-7b-instruct mistral-7b-instruct-v0.3; do
  for STAGE in present-gate revision probe kv-channel; do
    /usr/bin/time -f "TIMING model=$MODEL stage=$STAGE wall=%e s maxrss=%M KB" \
      "$PY" "$RUNNER" --stage "$STAGE" --workdir "$WORK" --design "$DESIGN" --backend hf --model "$MODEL" --split dev --max-instances 8 --families F3_P2_CANON,F1_P0
  done
done
"$PY" "$RUNNER" --stage rollup --workdir "$WORK" --design "$DESIGN" --backend hf --split dev
echo SMOKE_DONE
