#!/usr/bin/env bash
#SBATCH --job-name=o2-e40m5p2c-eval
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=06:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2c-eval-%A.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2c-eval-%A.err
# E40-m5' Stage-2c evaluation: runner controls (planted replay = 9 model calls,
# nullcal) -> audit (leakage + pin + seed mandate) -> analysis selftest (full
# control battery through main() on fixtures) -> analysis on the real campaign.
# The analysis refuses (exit 3) unless all 60 chains are settled. NOT submitted
# at dispatch time: submit only after `status` reports all_settled (unblinding
# is an operator decision, per the design's no-rescue clause).
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
ROOT="$BASE/campaign-e40-m5p-stage2c"
PY="$BASE/campaign-e40-r3/run/venv/bin/python"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ORION_ARM_HTTP_RETRIES=10
export E40M_BASE="$BASE" E40M_ROOT="$ROOT" E40M_REF="$BASE/campaign-e40-m2"
export E40M5P2C_OUT="$ROOT/run/rollup"
cd "$ROOT"
"$PY" e40_matched_runner_m5p_stage2c.py status
"$PY" e40_matched_runner_m5p_stage2c.py control-planted
"$PY" e40_matched_runner_m5p_stage2c.py control-nullcal
"$PY" e40_matched_runner_m5p_stage2c.py audit
"$PY" e40_m5p_stage2c_analysis.py selftest
"$PY" e40_m5p_stage2c_analysis.py run
