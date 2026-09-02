#!/usr/bin/env bash
#SBATCH --job-name=o2-pcr6-gr0b
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/gr0b-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/gr0b-%j.err
set -euo pipefail
# GR0(b) known-answer control: frozen 5-task subset (one per project, lexicographic,
# lowest bug_id), gold patch must flip the registered failing test AND yield
# critical_new_failure_count == 0 under the same suite definition.  The ONLY stage
# that reads gold patches (records marked gold_or_fixed_solution_accessed=true).
# SLURM runs a spooled copy of this script, so locate the shared bindings via the clone.
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"
source "$PCR6_SRC/research/experiments/pc-r6/sbatch/pc_r6_common.sh"
"$PY" "$RUNNER" --stage gr0b "${COMMON[@]}"
