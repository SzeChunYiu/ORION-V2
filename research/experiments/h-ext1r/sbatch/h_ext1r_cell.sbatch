#!/usr/bin/env bash
#SBATCH --job-name=o2-hext1r
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=06:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-h-ext1r/%x-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-h-ext1r/%x-%j.err
# H-EXT-1R: one cell (dev or protected) of the witnessed-latent regime study.
#   HEXT1R_CELL=dev        prepare the development split from the constant seed, gate-audit,
#                          dispatch the three model arms, evaluate, analyze (feasibility F1)
#   HEXT1R_CELL=protected  refuses unless the design is frozen, the authorization present and
#                          the custody seed hashes to the commitment; then the same chain with
#                          the protected gates
# The private oracle is removed by the dispatcher before any model call and restored after.
set -euo pipefail
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R11="$E45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
BASE="${HEXT1R_DIR:-$E45/h-ext1r}"
SRC="$BASE/source"
PY="$R11/run/venv/bin/python"
CELL="${HEXT1R_CELL:?set HEXT1R_CELL to dev or protected}"
: "${HEXT1R_SOURCE_SHA:?set HEXT1R_SOURCE_SHA to the branch sha the cell runs from}"
mkdir -p "$E45/logs-h-ext1r" "$BASE/$CELL"
set -a; source "$HOME/.orion-campaign.env"; set +a
test -d "$SRC/.git" || { echo "SRC is not a git clone: $SRC"; exit 3; }
HEAD_SHA=$(git -C "$SRC" rev-parse HEAD)
[ "$HEAD_SHA" = "$HEXT1R_SOURCE_SHA" ] || { echo "SOURCE_SHA_MISMATCH $HEAD_SHA != $HEXT1R_SOURCE_SHA"; exit 3; }
export PYTHONPATH="$SRC/src"
# The registered channel condition (E30-R13's), carried verbatim.
export ORION_ARM_CHANNEL_CONTRACT=thinking_disabled
export ANTHROPIC_MODEL=glm-5.3
export ORION_ARM_SERVED_MODEL=glm-5.3
export ORION_ARM_MAX_TOKENS="${HEXT1R_MAX_TOKENS:-4000}"
export ORION_ARM_HTTP_RETRIES=10
export ORION_FORMAL_TIMEOUT=900
WD="$BASE/$CELL/$( [ "$CELL" = dev ] && echo dev-split || echo protected-split )"
STUDY="$SRC/scripts/h_ext1r_regime_study.py"
echo "python=$($PY --version 2>&1) source=$HEAD_SHA cell=$CELL contract=$ORION_ARM_CHANNEL_CONTRACT cap=$ORION_ARM_MAX_TOKENS wd=$WD"
"$PY" "$STUDY" selftest --out "$BASE/$CELL/selftest"
if [ "$CELL" = dev ]; then
  "$PY" "$STUDY" prepare --cell dev --workdir "$WD" ${HEXT1R_FORCE:+--force}
else
  "$PY" "$STUDY" protected-prepare --workdir "$WD" --seed-file "${HEXT1R_SEED_FILE:?set HEXT1R_SEED_FILE}" ${HEXT1R_FORCE:+--force}
fi
"$PY" "$STUDY" gate-audit --workdir "$WD"
"$PY" "$STUDY" dispatch --workdir "$WD" --max-concurrency "${HEXT1R_CONCURRENCY:-3}"
"$PY" "$STUDY" evaluate --workdir "$WD"
"$PY" "$STUDY" analyze --cell "$CELL" --workdir "$WD" --out "$BASE/$CELL/results"
echo "CELL_COMPLETE $CELL $(date -u +%FT%TZ)"
