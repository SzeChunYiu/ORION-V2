#!/usr/bin/env bash
#SBATCH --job-name=o2-sd70-v4-dev
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-sd70-v4/logs/dev-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-sd70-v4/logs/dev-%j.err
set -euo pipefail
: "${V4_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-sd70-v4/src}"
: "${V4_OUT:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-sd70-v4/results}"
PY=/projects/hep/fs9/users/scyiu/orion-v2-wave6/.venv/bin/python
D="$V4_SRC/research/experiments/sd70-v4"
mkdir -p "$V4_OUT"
echo "SD70-V4 dev job ${SLURM_JOB_ID:-local} host $(hostname) python=$($PY --version 2>&1) head=$(git -C "$V4_SRC" rev-parse --short HEAD)"
sha256sum "$D"/sd70v4_*.py "$D/SD70_V4_GATED_FAMILY_DESIGN_V1.json"
cd "$V4_SRC"
$PY "$D/sd70v4_run.py" selftest --out "$V4_OUT"
$PY "$D/sd70v4_run.py" dev --out "$V4_OUT"
echo "exit=$? $(date -Is)"
