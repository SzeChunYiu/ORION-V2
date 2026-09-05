#!/bin/bash
# ME-X naturalistic cells deferred dispatcher (billy-old): waits for the channel window, refuses without the authorization file,
# runs the three cells' proxy stages idempotently (responses on disk are skipped), logs everything.
set -u
cd ~/sd10run/ORION-V2-ctrl/research/experiments/me-x-naturalistic || exit 2
LOG=~/sd10run/logs-fmfg/mex-nat-deferred.log
[ -f PROTECTED_RUN_AUTHORIZATION.json ] || { echo "REFUSED: authorization absent $(date -Is)" >> "$LOG"; exit 3; }
START=$(date -d "2026-09-07 16:25" +%s)
echo "=== ME-X-NAT dispatcher armed $(date -Is) pid $$ head $(git -C ~/sd10run/ORION-V2-ctrl rev-parse --short HEAD) ===" >> "$LOG"
while [ "$(date +%s)" -lt "$START" ]; do sleep 900; done
for cell in ME-X2-NAT ME-X4-NAT ME-X5-NAT; do
  attempt=0
  while true; do
    attempt=$((attempt+1)); echo "--- $cell attempt $attempt $(date -Is) ---" >> "$LOG"
    python3 mex_nat_run.py run --cell "$cell" --workdir ".mex-nat-$cell" --channel codex --max-concurrency 2 >> "$LOG" 2>&1; rc=$?
    echo "--- $cell exit=$rc ---" >> "$LOG"
    [ "$rc" -eq 0 ] && break; [ "$rc" -eq 5 ] && { echo "CANNOT_CHECK; stopping" >> "$LOG"; exit 5; }; sleep 1800
  done
done
echo "=== ME-X-NAT dispatcher COMPLETE $(date -Is) ===" >> "$LOG"
