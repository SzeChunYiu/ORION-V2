#!/usr/bin/env bash
#SBATCH --job-name=o2-e40-r4a
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=06:00:00
#SBATCH --array=0-63%8
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-r4a/logs/chain-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-r4a/logs/chain-%A_%a.err
set -euo pipefail
# 64 fresh chains: index < 32 -> m2 configuration, else m3; task index = seed-derived (design seed_commitment); 4 cycles each.
C=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-r4a
[ -f "$C/src/research/experiments/e40-r4a/PROTECTED_RUN_AUTHORIZATION.json" ] || { echo REFUSED; exit 3; }
COHORT=$([ "$SLURM_ARRAY_TASK_ID" -lt 32 ] && echo m2 || echo m3)
export ORION_E40_CAMPAIGN="$C/campaign-$COHORT-r4a" ORION_E40_SEED_FILE="$HOME/.orion-custody/e40-r4a/PROTECTED_SEED_V1.txt"
cd "$C/src" && .venv/bin/python scripts/e40_matched_runner.py chain --task "$SLURM_ARRAY_TASK_ID"
