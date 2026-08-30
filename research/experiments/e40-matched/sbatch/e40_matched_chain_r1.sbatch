#!/usr/bin/env bash
#SBATCH --job-name=o2-e40m1-chain
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=2-00:00:00
#SBATCH --array=0-35%6
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m1-chain-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m1-chain-%A_%a.err
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
ROOT="$BASE/campaign-e40-m1"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ORION_ARM_HTTP_RETRIES=10
export E40M_BASE="$BASE" E40M_ROOT="$ROOT"
cd "$ROOT"
"$BASE/campaign-e40-r3/run/venv/bin/python" e40_matched_runner.py chain --task "$SLURM_ARRAY_TASK_ID"
