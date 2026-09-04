#!/usr/bin/env bash
#SBATCH --job-name=o2-e40m5p2e-eval
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2e-eval-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m5p2e-eval-%j.err
# Selftest (every routing branch + no-alarm case) THEN the single real analysis.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
ROOT="$BASE/campaign-e40-m5p-stage2e"
export E40M_BASE="$BASE" E40M_ROOT="$ROOT"
cd "$ROOT"
PY="$BASE/campaign-e40-r3/run/venv/bin/python"
"$PY" e40_m5p_stage2e_overlap_precondition.py selftest
"$PY" e40_m5p_stage2e_overlap_precondition.py analyze
