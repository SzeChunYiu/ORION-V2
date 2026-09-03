#!/usr/bin/env bash
#SBATCH --job-name=o2-pra-llm-v3-r1
#SBATCH --account=lu2026-2-51
#SBATCH --partition=gpua100
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=160G
#SBATCH --time=40:00:00
#SBATCH --array=0-1
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/v3-r1-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/logs/v3-r1-%A_%a.err
#
# PROTECTED RUN, design V3 (campaign-pra-llm-v3).  **NOT SUBMITTED, AND NOT AUTHORIZED.**
# Compute authorization for a V3 run is out of scope of the design PR and is not requested.
# This script exists so the design's execution path is reviewable, not so it can be queued.
#
# Preconditions, ALL of which are open at the time this file lands:
#   1. the V2 protected run (array 3566415, campaign-pra-llm-v2) has COMPLETED and its rollup
#      has landed.  V3 must never compete with, or be confused for, the in-flight V2 campaign.
#   2. the operator has decided that V3 should run at all, given V2's outcome.
#   3. `--stage certify` PASSES on the dev split (exit 0).  It is blocking: it proves every
#      registered clause is implemented and reachable and that the probe label is identifiable
#      in exactly the conditions the design registers.  A run started without it can produce
#      the very defect V3 exists to repair.
#   4. the protected seed has been sealed on LUNARC and its sha256 published into
#      PRA_REAL_LLM_AUDIT_DESIGN_V3.json as protected_commitment_sha256, in a commit of its
#      own.  Until then the design carries PENDING_... and the runner refuses the split.
#   5. PRA_PROTECTED_AUTHORIZATION is set to the V3 design token.
#
# V3 uses its OWN runner copy (pra_real_llm_audit_v3.py) under $BASE/v3/.  The V1 files at the
# base directory and the V2 files under v2/ are left untouched; array 3566415 depends on them.
#
# Partition: gpua100 (1xA100-80GB) so a V3 run never competes with V2 on gpua100i.  Both V3
# models are the V2 models (32.5 / 23.6 GB bf16 -> 65.5 / 47.2 GB) and fit one 80 GB card.
# --time sized from measured V2 dev latency: ~26.3 h for the slower model on 1xA100-80GB.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-pra-llm
V3="$BASE/v3"
WORK="$BASE/campaign-pra-llm-v3/protected"
export HF_HOME="$BASE/hf-cache" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONHASHSEED=0 CUBLAS_WORKSPACE_CONFIG=:4096:8
DEVICE="${PRA_DEVICE:-cuda}"
PY="$BASE/.venv/bin/python"
RUNNER="$V3/pra_real_llm_audit_v3.py"
DESIGN="$V3/PRA_REAL_LLM_AUDIT_DESIGN_V3.json"
SEED_FILE="${PRA_PROTECTED_SEED_FILE:-$V3/protected_seed.sealed}"
AUTH="${PRA_PROTECTED_AUTHORIZATION:?set PRA_PROTECTED_AUTHORIZATION to the V3 design token to run the protected split}"
test -r "$SEED_FILE" || { echo "sealed protected seed file missing: $SEED_FILE"; exit 1; }
MODELS=(qwen2.5-32b-instruct mistral-small-24b-instruct-2501)
MODEL="${MODELS[$SLURM_ARRAY_TASK_ID]}"
mkdir -p "$WORK/suite"
sha256sum "$RUNNER" "$DESIGN" "$SEED_FILE"
flock "$WORK/suite/.generate.lock" bash -c '
  if [ ! -f "$0/suite/suite_protected.sha256.json" ]; then
    "$1" "$2" --stage generate-suite --workdir "$0" --design "$3" --backend hf --protected-seed-file "$4"
  fi' "$WORK" "$PY" "$RUNNER" "$DESIGN" "$SEED_FILE"
test -f "$WORK/suite/suite_protected.sha256.json" || { echo "protected suite missing after generation"; exit 1; }

# BLOCKING pre-run gate.  Exit 4 = a registered clause is unimplemented or unreachable; exit 3 =
# a clause could not be checked.  Neither may be stepped over: the whole point of V3 is that a
# structurally determined clause is caught here rather than reported as an accuracy afterwards.
"$PY" "$RUNNER" --stage certify --workdir "$WORK" --design "$DESIGN" --backend hf \
  --split protected --protected-authorization "$AUTH"

for STAGE in present-gate revision probe kv-channel; do
  /usr/bin/time -f "TIMING model=$MODEL stage=$STAGE wall=%e s maxrss=%M KB" \
    "$PY" "$RUNNER" --stage "$STAGE" --workdir "$WORK" --design "$DESIGN" --backend hf --model "$MODEL" --split protected --protected-authorization "$AUTH" --device "$DEVICE"
done
# rollup is run once, manually, after both array tasks finish; then the sealed seed file is
# archived next to the rollup (post-run reveal):
#   $PY $RUNNER --stage rollup --workdir $WORK --design $DESIGN --backend hf --split protected --protected-authorization "$AUTH"
echo V3_R1_MODEL_DONE "$MODEL"
