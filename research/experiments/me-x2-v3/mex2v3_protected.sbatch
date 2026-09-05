#!/usr/bin/env bash
#SBATCH --job-name=o2-mex2-v3
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x2-v3/logs/protected-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x2-v3/logs/protected-%j.err
set -euo pipefail
: "${V3_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x2-v3/src}"
: "${V3_OUT:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x2-v3/results}"
PY=/projects/hep/fs9/users/scyiu/orion-v2-wave6/.venv/bin/python
D="$V3_SRC/research/experiments/me-x2-v3"
mkdir -p "$V3_OUT"
echo "ME-X2-V3 job ${SLURM_JOB_ID:-local} host $(hostname) python=$($PY --version 2>&1) head=$(git -C "$V3_SRC" rev-parse --short HEAD)"
sha256sum "$D/mex2v3_run.py" "$D/mex2v3_levers.py" "$D/ME_X2_V3_IDENTIFICATION_THRESHOLD_DESIGN_V1.json" "$D/ME_X2_V3_CALIBRATION_V1.json"
cd "$V3_SRC"
$PY "$D/mex2v3_run.py" selftest --out "$V3_OUT"
$PY "$D/mex2v3_run.py" dev --out "$V3_OUT"
cp "$D/PROTECTED_RUN_AUTHORIZATION_MINTED_V1.json" "$D/PROTECTED_RUN_AUTHORIZATION.json"
$PY "$D/mex2v3_run.py" protected --out "$V3_OUT" --seed-file "$HOME/.orion-custody/me-x2-v3/PROTECTED_SEED_V3.txt"
echo "exit=$? $(date -Is)"
