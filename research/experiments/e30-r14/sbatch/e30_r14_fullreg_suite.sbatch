#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r14-suite
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=24:00:00
#SBATCH --array=0-39
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/suite-%A_%a.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/suite-%A_%a.err
# One array index = one task: the baseline suite pass plus every arm x rep patched pass.
set -euo pipefail
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R14 (exported by the submitting environment) instead.
: "${R14:?set R14=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R14_SBATCH_DIR:-$R14/source/research/experiments/e30-r14/sbatch}"
source "$SBATCH_DIR/e30_r14_common.sh"
test -f "$R14/fullreg/PC_R6_GR0_RECEIPT.json" || { echo "GR0 receipt absent -- refusing"; exit 5; }
"$PY" -c "
import json,sys
sys.exit(0 if json.load(open('$R14/fullreg/PC_R6_GR0_RECEIPT.json')).get('gr0_status')=='PASS' else 5)"
"$PY" "$RUNNER" --stage suite --index "$SLURM_ARRAY_TASK_ID" "${COMMON[@]}"
