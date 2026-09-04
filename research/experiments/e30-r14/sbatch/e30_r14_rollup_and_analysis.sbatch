#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r14-rollup
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/rollup-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/rollup-%j.err
# Rollup, then the registered analysis.  The analysis refuses to start without a GR0
# PASS receipt and computes no gate until the served-model homogeneity check is done.
set -euo pipefail
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R14 (exported by the submitting environment) instead.
: "${R14:?set R14=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R14_SBATCH_DIR:-$R14/source/research/experiments/e30-r14/sbatch}"
source "$SBATCH_DIR/e30_r14_common.sh"
# The contract fingerprint the gate compares against is computed BY THE ARMS
# EXECUTABLE, not retyped here: a hand-copied digest would pass the gate while the
# dispatched bytes differed.
CONTRACT_SHA=$(CONTRACT="$CHANNEL_CONTRACT" "$PY" -c "
import os, sys
sys.path.insert(0, os.environ['R14SRC'] + '/scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('arms', os.environ['R14SRC'] + '/scripts/orion_claude_arms.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.channel_contract_sha256(os.environ['CONTRACT']))")
echo "CHANNEL_CONTRACT=$CHANNEL_CONTRACT sha256=$CONTRACT_SHA"
"$PY" "$RUNNER" --stage rollup "${COMMON[@]}"
"$PY" -c "
import json,sys
r=json.load(open('$R14/fullreg/PC_R6_FULLREG_RAW_ROLLUP_V1.json'))
print('rollup complete:', r.get('complete'))
sys.exit(0 if r.get('complete') else 6)"
# Exit 4 (a hard gate FAILED) and exit 5 (a hard gate COULD NOT BE CHECKED) are
# REGISTERED TERMINALS, not crashes.  Under `set -e` a bare invocation would abort the
# script on them and skip the authorization archive below, leaving a spent authorization
# live for a later resubmit to dispatch on.  Capture the code, archive, then exit with it.
ANALYSIS_RC=0
"$PY" "$ANALYSIS" \
  --rollup "$R14/fullreg/E30_R14_FULLREG_RAW_ROLLUP_V1.json" \
  --gr0 "$R14/fullreg/PC_R6_GR0_RECEIPT.json" \
  --gr0b "$R14/fullreg/PC_R6_GR0B_RECEIPT.json" \
  --campaign "$R14" --analyzer "$ANALYZER" --design "$DESIGN" \
  --served-model "${E30R14_SERVED_MODEL:-glm-5.3}" \
  --r12-analysis "$R12ANALYSIS" \
  --r12-analysis-sha256 "$(sha256sum "$R12ANALYSIS" | cut -c1-64)" \
  --channel-contract "$CHANNEL_CONTRACT" \
  --channel-contract-sha256 "$CONTRACT_SHA" \
  --out "$R14/fullreg" || ANALYSIS_RC=$?
echo "ANALYSIS_EXIT=$ANALYSIS_RC (0 complete, 3 precondition refused, 4 gate FAIL, 5 gate CANNOT-CHECK)"
# 4 and 5 are distinct on purpose: neither is a null, and neither may be reported as one.
# Archive the authorization so the dispatch guard re-arms: a spent authorization left in
# place would let a later resubmission run without a fresh one.
AUTH="$R14/PROTECTED_RUN_AUTHORIZATION.json"
if [ -f "$AUTH" ]; then
  mv "$AUTH" "$R14/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json"
  echo "AUTHORIZATION_ARCHIVED $R14/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json"
fi
echo "ROLLUP_AND_ANALYSIS_COMPLETE $(date -u +%FT%TZ) analysis_exit=$ANALYSIS_RC"
exit "$ANALYSIS_RC"
