#!/usr/bin/env bash
#SBATCH --job-name=o2-e40m5p2b-chain
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --array=0-47%8
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2b-chain-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2b-chain-%A_%a.err
# E40-m5' Stage-2b seed-replica stability probe: 48 independent F2 chains
# (12 cells x 4 seed-replicas), 4 cycles each = 192 native gies runs
# (exp_ids 503000-503191). m3 chains took 12-24 min each (sacct 3554920);
# 3 h wall is a wide margin for endpoint retries.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
ROOT="$BASE/campaign-e40-m5p-stage2b"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ORION_ARM_HTTP_RETRIES=10
export E40M_BASE="$BASE" E40M_ROOT="$ROOT" E40M_REF="$BASE/campaign-e40-m2"
cd "$ROOT"
PY="$BASE/campaign-e40-r3/run/venv/bin/python"
# Pre-flight probe gate: the E60 lane must answer (model id recorded) BEFORE any
# chain work starts. A walled endpoint exits 75 here without touching the chain
# dir, so the array can simply be resubmitted (chains resume idempotently).
ORION_ARM_HTTP_RETRIES=2 "$PY" e40_matched_runner_m5p_stage2b.py probe-endpoint \
  > "$BASE/logs/e40m5p2b-probe-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.json" \
  || { echo "ENDPOINT_PROBE_FAILED task=${SLURM_ARRAY_TASK_ID}"; exit 75; }
"$PY" e40_matched_runner_m5p_stage2b.py chain --task "$SLURM_ARRAY_TASK_ID"
