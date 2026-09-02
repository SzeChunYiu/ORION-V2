#!/usr/bin/env bash
#SBATCH --job-name=o2-pcr6-gr0verify
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/gr0verify-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/gr0verify-%j.err
set -euo pipefail
# Submit with --dependency=afterok:<gr0a array>:<gr0b job>.  Collects the GR0(a)
# vectors (bit-exact diff vs frozen native_success, checker negative control first)
# and combines GR0(a)+(b).  Non-zero exit => the dependent suite array never starts.
# SLURM runs a spooled copy of this script, so locate the shared bindings via the clone.
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"
source "$PCR6_SRC/research/experiments/pc-r6/sbatch/pc_r6_common.sh"
"$PY" "$RUNNER" --stage gr0a "${COMMON[@]}"
"$PY" "$RUNNER" --stage gr0 --out "$PCR6_OUT"
