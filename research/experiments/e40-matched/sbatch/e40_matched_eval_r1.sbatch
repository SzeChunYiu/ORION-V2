#!/usr/bin/env bash
#SBATCH --job-name=o2-e40m1-eval
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=1-00:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m1-eval-%A.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m1-eval-%A.err
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
ROOT="$BASE/campaign-e40-m1"
PY="$BASE/campaign-e40-r3/run/venv/bin/python"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ORION_ARM_HTTP_RETRIES=10
export E40M_BASE="$BASE" E40M_ROOT="$ROOT"
cd "$ROOT"
# Controls execute BEFORE the rollup reads any held-out outcome; audit failure
# (leakage or pinned-knob drift) aborts before a verdict can be produced.
"$PY" e40_matched_runner.py control-planted
"$PY" e40_matched_runner.py control-nullcal
"$PY" e40_matched_runner.py control-uninformative
"$PY" e40_matched_runner.py audit
"$PY" e40_matched_runner.py rollup
