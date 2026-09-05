#!/usr/bin/env bash
# E40-R4A deferred dispatcher (LUNARC login node, nohup): waits for the channel window, probes the model channel every 30 min,
# then submits the 64-chain array.  Refuses without PROTECTED_RUN_AUTHORIZATION.json next to the design (minted at dispatch).
set -u
C=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-r4a
D="$C/src/research/experiments/e40-r4a"
LOG="$C/logs/dispatch.log"; mkdir -p "$C/logs"
[ -f "$D/PROTECTED_RUN_AUTHORIZATION.json" ] || { echo "REFUSED: authorization absent $(date -Is)" >> "$LOG"; exit 3; }
START=$(date -d "2026-09-07 16:25" +%s)
echo "=== E40-R4A dispatcher armed $(date -Is) pid $$ ===" >> "$LOG"
while [ "$(date +%s)" -lt "$START" ]; do sleep 900; done
while true; do
  if "$C/src/.venv/bin/python" "$C/src/scripts/e40_matched_runner.py" chain --task 0 --dry-run >> "$LOG" 2>&1; then
    sbatch "$D/e40_r4a_chain_array.sbatch" >> "$LOG" 2>&1; echo "submitted $(date -Is)" >> "$LOG"; break
  fi
  echo "channel not answering $(date -Is); retry in 30 min" >> "$LOG"; sleep 1800
done
