#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r12-gr0verify
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/gr0verify-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/gr0verify-%j.err
# GR0a collect (self-consistency vs the campaign's own frozen-lane records) and the
# GR0 combine.  Hard: a FAIL here halts the study before any endpoint is read.
set -euo pipefail
source "$(dirname "$0")/e30_r12_common.sh"
"$PY" "$RUNNER" --stage manifest "${COMMON[@]}" --truth-dir "$R12SRC/research/experiments/results/issue45"
"$PY" "$RUNNER" --stage gr0a "${COMMON[@]}" --truth-dir "$R12SRC/research/experiments/results/issue45"
"$PY" "$RUNNER" --stage gr0b "${COMMON[@]}"
"$PY" "$RUNNER" --stage gr0 "${COMMON[@]}"
"$PY" -c "
import json,sys
r=json.load(open('$R12/fullreg/PC_R6_GR0_RECEIPT.json'))
print(json.dumps(r,indent=1))
sys.exit(0 if r.get('gr0_status')=='PASS' else 5)"
