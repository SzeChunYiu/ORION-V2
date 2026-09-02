#!/usr/bin/env bash
#SBATCH --job-name=o2-e70gc2-r1
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
#SBATCH --time=48:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e70gc2-r1-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e70gc2-r1-%j.err
# E70-GC2 R1 protected dispatch (LUNARC). Probe auth, then run the frozen pipeline verbatim.
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
CLONE=/projects/hep/fs9/users/scyiu/orion-v2-wave6
export CODEX_HOME="$BASE/codex-home"
export ORION_CODEX_BIN="$BASE/codex-cli/pkg150/package/vendor/x86_64-unknown-linux-musl/bin/codex"
export ORION_GC2_WORKDIR="$BASE/campaign-e70-gc2-r1"
export ORION_GC2_MAX_CONCURRENCY=3
export PATH="$CLONE/.venv/bin:$PATH"
mkdir -p "$BASE/campaign-e70-gc2-r1-infra"
PROBE_OUT=$(mktemp)
for ATTEMPT in $(seq 1 20); do
  if "$ORION_CODEX_BIN" exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check --sandbox read-only -C /tmp -m gpt-5.6-terra \
      -o "$PROBE_OUT" "Reply with exactly the single word OK and nothing else." >"$BASE/campaign-e70-gc2-r1-infra/probe_${ATTEMPT}.log" 2>&1 \
      && [ -s "$PROBE_OUT" ]; then echo "PROBE_OK attempt=$ATTEMPT reply=$(cat $PROBE_OUT)"; break; fi
  [ "$ATTEMPT" -eq 20 ] && { echo "PROBE_EXHAUSTED_AFTER_20_ATTEMPTS"; exit 3; }
  sleep 1800
done
cd "$CLONE"
git rev-parse HEAD
bash scripts/run_orion_generated_composition_gc2_pilot.sh
