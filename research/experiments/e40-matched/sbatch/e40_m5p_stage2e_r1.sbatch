#!/usr/bin/env bash
#SBATCH --job-name=o2-e40m5p2e
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --array=0-33%8
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2e-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2e-%A_%a.err
# E40-m5' Stage-2e replica-overlap precondition probe: 34 native gies runs,
# exp_ids 505000-505033, ZERO model calls. No endpoint probe gate is needed or
# wanted here: this campaign never contacts the model channel, which is the point.
# m3/Stage-2c native runs took 12-24 min each; 3 h wall is a wide margin.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
ROOT="$BASE/campaign-e40-m5p-stage2e"
export E40M_BASE="$BASE" E40M_ROOT="$ROOT"
cd "$ROOT"
PY="$BASE/campaign-e40-r3/run/venv/bin/python"
"$PY" e40_m5p_stage2e_overlap_precondition.py run --task "$SLURM_ARRAY_TASK_ID"
