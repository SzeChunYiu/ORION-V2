#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r14-calib
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=08:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/calib-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/calib-%j.err
# E30-R14 interface calibration: the 2x2 (edit interface x presentation policy) probe on
# SIMPLE_DIRECT over the 40 frozen tasks, ONE call per cell, under E30-R13's registered
# channel condition (thinking_disabled, served glm-5.3, 14000 per-call cap).
#
# Runs OUTSIDE any campaign tree (E45/e30-r14-calibration), reads E30-R13's frozen
# gold-blind requests read-only, never evaluates a patch, never runs a test, and keeps
# no response text.  See e30_r14_interface_calibration.py.
set -euo pipefail
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R13="$E45/campaign-e30-r13-channelcontract-core4-rep3-20260903-427bfc90"
R11="$E45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
CAL="${E30R14_CALIBRATION_DIR:-$E45/e30-r14-calibration}"
SRC="$CAL/source"
PY="$R11/run/venv/bin/python"
: "${E30R14_SOURCE_SHA:?set E30R14_SOURCE_SHA to the branch sha the calibration runs from}"
mkdir -p "$CAL/results" "$E45/logs-e30-r14"
set -a; source "$HOME/.orion-campaign.env"; set +a
test -d "$SRC/.git" || { echo "SRC is not a git clone: $SRC"; exit 3; }
HEAD_SHA=$(git -C "$SRC" rev-parse HEAD)
[ "$HEAD_SHA" = "$E30R14_SOURCE_SHA" ] || { echo "SOURCE_SHA_MISMATCH $HEAD_SHA != $E30R14_SOURCE_SHA"; exit 3; }
export PYTHONPATH="$SRC/src"
"$PY" - <<'PROV'
import inspect, os, sys
import orion_v2.anchored_edit_interface as m
path = inspect.getfile(m)
print("anchored_edit_interface ->", path)
sys.exit(0 if path.startswith(os.environ["PYTHONPATH"].split(":")[0]) else 3)
PROV
# E30-R13's registered channel condition, carried verbatim.
export ORION_ARM_CHANNEL_CONTRACT=thinking_disabled
export ANTHROPIC_MODEL=glm-5.3
export ORION_ARM_SERVED_MODEL=glm-5.3
export ORION_ARM_MAX_TOKENS=14000
unset ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET
export ORION_ARM_HTTP_RETRIES=10
echo "python=$($PY --version 2>&1) source=$HEAD_SHA contract=$ORION_ARM_CHANNEL_CONTRACT cap=$ORION_ARM_MAX_TOKENS"
"$PY" "$SRC/research/experiments/e30-r14/e30_r14_interface_calibration.py" \
  --source "$SRC" \
  --requests-root "$R13/run/confirmatory-r1/requests" \
  --tasks ALL --arm SIMPLE_DIRECT --conditions "${E30R14_CONDITIONS:-ALL}" \
  --concurrency "${E30R14_CONCURRENCY:-2}" \
  --out "$CAL/results/E30_R14_INTERFACE_CALIBRATION_V1.json"
echo "CALIBRATION_COMPLETE $(date -u +%FT%TZ)"
