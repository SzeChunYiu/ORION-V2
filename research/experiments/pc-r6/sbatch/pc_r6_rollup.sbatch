#!/usr/bin/env bash
#SBATCH --job-name=o2-pcr6-rollup
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/rollup-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/rollup-%j.err
set -euo pipefail
# Raw rollup only (submit with --dependency=afterany:<suite array>).  The analysis
# stage (pc_r6_fullreg_analysis.py) is NOT chained: it is run deliberately, after the
# rollup is verified complete, and refuses to run without a GR0 PASS receipt.
# SLURM runs a spooled copy of this script, so locate the shared bindings via the clone.
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"
source "$PCR6_SRC/research/experiments/pc-r6/sbatch/pc_r6_common.sh"
"$PY" "$RUNNER" --stage rollup "${COMMON[@]}"
