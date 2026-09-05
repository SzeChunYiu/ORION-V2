#!/usr/bin/env bash
#SBATCH --job-name=o2-pcr6b-suite
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --array=0-79%24
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6b/logs/suite-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6b/logs/suite-%A_%a.err
set -euo pipefail
# PC-R6B: the parent's array lane on the enlarged paired task set (E30-R13 campaign + new arm evaluations from the channel window).
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"
[ -f "$PCR6_SRC/research/experiments/pc-r6b/PROTECTED_RUN_AUTHORIZATION.json" ] || { echo REFUSED; exit 3; }
source "$PCR6_SRC/research/experiments/pc-r6/sbatch/pc_r6_common.sh"
"$PY" "$RUNNER" --stage suite --index "$SLURM_ARRAY_TASK_ID" "${COMMON[@]}" --min-discordant 3 --max-ci-halfwidth 0.15
