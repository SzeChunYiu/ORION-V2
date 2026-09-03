#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r13-gr0a
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=08:00:00
#SBATCH --array=0-39
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r13/gr0a-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r13/gr0a-%A_%a.err
set -euo pipefail
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R13 (exported by the submitting environment) instead.
: "${R13:?set R13=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R13_SBATCH_DIR:-$R13/source/research/experiments/e30-r13/sbatch}"
source "$SBATCH_DIR/e30_r13_common.sh"
"$PY" "$RUNNER" --stage gr0a --execute --index "$SLURM_ARRAY_TASK_ID" "${COMMON[@]}"
