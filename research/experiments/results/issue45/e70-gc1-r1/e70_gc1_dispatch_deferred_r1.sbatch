#!/usr/bin/env bash
#SBATCH --job-name=o2-e70gc1-r1
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=24:00:00
#SBATCH --begin=2026-09-04T08:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e70gc1-r1-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e70gc1-r1-%j.err
# E70-GC1 deferred dispatch. The bound OpenAI codex account is usage-walled by
# the server until 2026-09-03 18:26 (timezone as stated by server). This job
# begins 2026-09-04 08:00 local (covers UTC and PT readings), probes auth
# availability, then runs the frozen pilot verbatim.
# NOTE: codex-home/auth.json is a copy of the Mac codex login. Codex refresh
# rotation on the Mac will likely invalidate this copy; re-sync it shortly
# before the begin time:  scp mac:~/.codex/auth.json lunarc:/projects/hep/fs9/users/scyiu/orion-v2-e45/codex-home/auth.json
set -euo pipefail
BASE=/projects/hep/fs9/users/scyiu/orion-v2-e45
CLONE=/projects/hep/fs9/users/scyiu/orion-v2-wave6
export CODEX_HOME="$BASE/codex-home"
export ORION_CODEX_BIN="$BASE/codex-cli/pkg150/package/vendor/x86_64-unknown-linux-musl/bin/codex"
export ORION_GC1_WORKDIR="$BASE/campaign-e70-gc1-r1"
export PATH="$CLONE/.venv/bin:$PATH"
set -a; source "$HOME/.orion-campaign.env"; set +a
PROBE_OUT=$(mktemp)
PROBE_OK=0
for ATTEMPT in $(seq 1 20); do
  if "$ORION_CODEX_BIN" exec --ephemeral --ignore-user-config --ignore-rules \
      --skip-git-repo-check --sandbox read-only -C /tmp -m gpt-5.6-terra \
      -o "$PROBE_OUT" "Reply with exactly the single word OK and nothing else." \
      >"$BASE/campaign-e70-gc1-r1/infra/dispatch_probe_attempt_${ATTEMPT}.stdout" \
      2>"$BASE/campaign-e70-gc1-r1/infra/dispatch_probe_attempt_${ATTEMPT}.log"; then
    if [ -s "$PROBE_OUT" ]; then PROBE_OK=1; echo "PROBE_OK attempt=$ATTEMPT reply=$(cat $PROBE_OUT)"; break; fi
  fi
  [ "$ATTEMPT" -eq 20 ] && { echo "PROBE_EXHAUSTED_AFTER_20_ATTEMPTS"; exit 3; }
  sleep 1800
done
cd "$CLONE"
bash scripts/run_orion_generated_composition_pilot.sh
