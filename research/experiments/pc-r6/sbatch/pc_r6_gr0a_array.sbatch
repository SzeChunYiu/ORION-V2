#!/usr/bin/env bash
#SBATCH --job-name=o2-pcr6-gr0a
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=03:00:00
#SBATCH --array=0-79%24
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/gr0a-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/gr0a-%A_%a.err
set -euo pipefail
# GR0(a) execute: one (cell, task) per array index -> every arm x rep re-run through
# the frozen-lane adapter closure VERBATIM (registered failing test only, no suite).
# Index map: 0-39 = e30r11 tasks (sorted task_id), 40-79 = e60 tasks.
# SLURM runs a spooled copy of this script, so locate the shared bindings via the clone.
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"
source "$PCR6_SRC/research/experiments/pc-r6/sbatch/pc_r6_common.sh"
"$PY" "$RUNNER" --stage gr0a --execute --index "$SLURM_ARRAY_TASK_ID" "${COMMON[@]}"
