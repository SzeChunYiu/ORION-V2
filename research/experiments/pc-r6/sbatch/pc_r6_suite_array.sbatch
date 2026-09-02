#!/usr/bin/env bash
#SBATCH --job-name=o2-pcr6-suite
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --array=0-79%24
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/suite-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/suite-%A_%a.err
set -euo pipefail
# Full-regression suite: one (cell, task) per index = 1 baseline pass (marker patch)
# + every arm x rep patched pass (adapter closure verbatim + frozen suite, 900 s
# wall per suite).  Submit with --dependency=afterok:<gr0 verify job>.
# Time budget: worst case 16 evaluations x (compile ~300 s + registered test + 900 s suite) ~ 6 h.
# SLURM runs a spooled copy of this script, so locate the shared bindings via the clone.
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"
source "$PCR6_SRC/research/experiments/pc-r6/sbatch/pc_r6_common.sh"
"$PY" "$RUNNER" --stage suite --index "$SLURM_ARRAY_TASK_ID" "${COMMON[@]}"
