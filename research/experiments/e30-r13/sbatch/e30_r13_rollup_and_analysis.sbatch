#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r13-rollup
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r13/rollup-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r13/rollup-%j.err
# Rollup, then the registered analysis.  The analysis refuses to start without a GR0
# PASS receipt and computes no gate until the served-model homogeneity check is done.
set -euo pipefail
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R13 (exported by the submitting environment) instead.
: "${R13:?set R13=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R13_SBATCH_DIR:-$R13/source/research/experiments/e30-r13/sbatch}"
source "$SBATCH_DIR/e30_r13_common.sh"
# The contract fingerprint the gate compares against is computed BY THE ARMS
# EXECUTABLE, not retyped here: a hand-copied digest would pass the gate while the
# dispatched bytes differed.
CONTRACT_SHA=$(CONTRACT="$CHANNEL_CONTRACT" "$PY" -c "
import os, sys
sys.path.insert(0, os.environ['R13SRC'] + '/scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('arms', os.environ['R13SRC'] + '/scripts/orion_claude_arms.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.channel_contract_sha256(os.environ['CONTRACT']))")
echo "CHANNEL_CONTRACT=$CHANNEL_CONTRACT sha256=$CONTRACT_SHA"
"$PY" "$RUNNER" --stage rollup "${COMMON[@]}"
"$PY" -c "
import json,sys
r=json.load(open('$R13/fullreg/PC_R6_FULLREG_RAW_ROLLUP_V1.json'))
print('rollup complete:', r.get('complete'))
sys.exit(0 if r.get('complete') else 6)"
"$PY" "$ANALYSIS" \
  --rollup "$R13/fullreg/E30_R13_FULLREG_RAW_ROLLUP_V1.json" \
  --gr0 "$R13/fullreg/PC_R6_GR0_RECEIPT.json" \
  --gr0b "$R13/fullreg/PC_R6_GR0B_RECEIPT.json" \
  --campaign "$R13" --analyzer "$ANALYZER" --design "$DESIGN" \
  --served-model "${E30R13_SERVED_MODEL:-glm-5.3}" \
  --r12-analysis "$R12ANALYSIS" \
  --r12-analysis-sha256 "$(sha256sum "$R12ANALYSIS" | cut -c1-64)" \
  --channel-contract "$CHANNEL_CONTRACT" \
  --channel-contract-sha256 "$CONTRACT_SHA" \
  --out "$R13/fullreg"
# Exit code 5 is CANNOT-CHECK on a channel gate and 4 is a gate FAIL; neither is a
# null, and neither may be reported as one.  They are distinct on purpose.
# Archive the authorization so the dispatch guard re-arms: a spent authorization left in
# place would let a later resubmission run without a fresh one.
AUTH="$R13/PROTECTED_RUN_AUTHORIZATION.json"
if [ -f "$AUTH" ]; then
  mv "$AUTH" "$R13/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json"
  echo "AUTHORIZATION_ARCHIVED $R13/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json"
fi
echo "ROLLUP_AND_ANALYSIS_COMPLETE $(date -u +%FT%TZ)"
