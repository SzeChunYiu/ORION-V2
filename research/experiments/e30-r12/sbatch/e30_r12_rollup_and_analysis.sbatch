#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r12-rollup
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/rollup-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/rollup-%j.err
# Rollup, then the registered analysis.  The analysis refuses to start without a GR0
# PASS receipt and computes no gate until the served-model homogeneity check is done.
set -euo pipefail
source "$(dirname "$0")/e30_r12_common.sh"
"$PY" "$RUNNER" --stage rollup "${COMMON[@]}"
"$PY" -c "
import json,sys
r=json.load(open('$R12/fullreg/PC_R6_FULLREG_RAW_ROLLUP_V1.json'))
print('rollup complete:', r.get('complete'))
sys.exit(0 if r.get('complete') else 6)"
"$PY" "$ANALYSIS" \
  --rollup "$R12/fullreg/E30_R12_FULLREG_RAW_ROLLUP_V1.json" \
  --gr0 "$R12/fullreg/PC_R6_GR0_RECEIPT.json" \
  --campaign "$R12" --analyzer "$ANALYZER" --design "$DESIGN" \
  --served-model "${E30R12_SERVED_MODEL:-glm-5.3}" \
  --out "$R12/fullreg"
echo "ROLLUP_AND_ANALYSIS_COMPLETE $(date -u +%FT%TZ)"
