#!/usr/bin/env bash
#SBATCH --job-name=o2-ocm-r1a
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-ocm-r1a/logs/protected-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-ocm-r1a/logs/protected-%j.err
set -euo pipefail
# OCM-R1A protected run: exact, stdlib, no channel.  SRC = clone at the frozen PR head; the
# authorization file is copied to its live name immediately before the stage and archived by the
# runner; the custody seed was scp'd with md5 verified on both sides.
: "${R1A_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-ocm-r1a/src}"
: "${R1A_OUT:=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-ocm-r1a/results}"
PY=/projects/hep/fs9/users/scyiu/orion-v2-wave6/.venv/bin/python
D="$R1A_SRC/research/experiments/ocm-r1a"
mkdir -p "$R1A_OUT"
echo "OCM-R1A job ${SLURM_JOB_ID:-local} host $(hostname) python=$($PY --version 2>&1) head=$(git -C "$R1A_SRC" rev-parse --short HEAD)"
sha256sum "$D/ocm_r1a_run.py" "$D/OCM_R1A_CONTROLLER_VS_FEDERATION_VSW_DESIGN_V1.json"
cd "$R1A_SRC"
$PY "$D/ocm_r1a_run.py" selftest --out "$R1A_OUT"
cp "$D/PROTECTED_RUN_AUTHORIZATION_MINTED_V1.json" "$D/PROTECTED_RUN_AUTHORIZATION.json"
$PY "$D/ocm_r1a_run.py" protected --out "$R1A_OUT" --seed-file "$HOME/.orion-custody/ocm-r1a/PROTECTED_SEED_V1.txt"
echo "exit=$? $(date -Is)"
