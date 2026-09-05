#!/usr/bin/env bash
#SBATCH --job-name=o2-mex6-v4
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=06:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x6-v4/logs/protected-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x6-v4/logs/protected-%j.err
set -euo pipefail
: "${V4_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x6-v4/src}"
: "${V4_OUT:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-me-x6-v4/results}"
PY=/projects/hep/fs9/users/scyiu/orion-v2-wave6/.venv/bin/python
D="$V4_SRC/research/experiments/me-x6-v4"
mkdir -p "$V4_OUT"
echo "ME-X6-V4 job ${SLURM_JOB_ID:-local} host $(hostname) python=$($PY --version 2>&1) head=$(git -C "$V4_SRC" rev-parse --short HEAD)"
sha256sum "$D/mex6v4_run.py" "$D/ME_X6_V4_COVERAGE_LIMITED_REGIME_DESIGN_V1.json" "$D/ME_X6_V4_DEVELOPMENT_FIT_V1.json"
cd "$V4_SRC"
$PY "$D/mex6v4_run.py" selftest --out "$V4_OUT"
$PY "$D/mex6v4_run.py" dev --out "$V4_OUT" --per-cell 2
cp "$D/PROTECTED_RUN_AUTHORIZATION_MINTED_V1.json" "$D/PROTECTED_RUN_AUTHORIZATION.json"
$PY "$D/mex6v4_run.py" protected --out "$V4_OUT" --seed-file "$HOME/.orion-custody/me-x6-v4/PROTECTED_SEED_V1.txt"
echo "exit=$? $(date -Is)"
