#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r11-redis
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=24:00:00
#SBATCH --begin=2026-09-04T13:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/redispatch-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/redispatch-%j.err
# E30 R11 DEFERRED RE-DISPATCH of the 194 model-dispatch-failed envelopes.
# Same frozen R11 identity: same requests, same task map, same one-shot
# command pattern as the frozen agent array. GUARD: each pass re-scans
# response envelopes and invokes the one-shot command ONLY while
# status==EXECUTION_FAILED_MODEL_RESPONSE; the 286 COMPLETED_PROPOSAL_ONLY
# responses are never touched (SKIP), so no completed model output is
# overwritten or resampled. Envelope failures contain no model output,
# so re-dispatching them is execution repair, not resampling.
# Availability window: begins 2026-09-04T13:00 (after SD70 job 3553181,
# --begin 2026-09-03T19:30 ~15h earlier; overlaps at most the tail of
# E70-GC1 job 3553088, --begin 2026-09-04T08:00). Probe-confirm loop
# follows the SD70/E70-GC1 deferred pattern (ORION_CODEX_BIN + CODEX_HOME
# under orion-v2-e45); the dispatch gate itself is a probe on the EXACT
# channel the frozen E30 R11 command uses (ANTHROPIC_BASE_URL/MODEL via
# scripts/orion_claude_arms.py), so the loop only releases the 194
# requests when that channel demonstrably serves a trivial completion.
# On full stock, chains the terminal eval driver (and, afterok, the
# frozen terminal analysis sequence). Receipts:
#   E30_R11_MODEL_DISPATCH_DEFICIT_RECEIPT.json (triage + legitimacy)
#   E30_R11_EVALUATION_LANE_DEFECT_AND_ADAPTER.json (eval lane)
set -euo pipefail
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
RUN="$CAMP/run"; SRC="$CAMP/source"; PY="$RUN/venv/bin/python"
export CODEX_HOME="$E45/codex-home"
export ORION_CODEX_BIN="$E45/codex-cli/pkg150/package/vendor/x86_64-unknown-linux-musl/bin/codex"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET=6000
export ORION_ARM_HTTP_RETRIES=10
mkdir -p "$CAMP/infra"

# ---- probe-confirm loop (SD70/E70-GC1 deferred pattern) ----
# Each attempt: (a) codex availability probe (pattern evidence, logged),
# (b) anthropic-channel probe -- the actual frozen dispatch channel.
# PROBE_OK gates on (b); (a) is recorded alongside it.
PROBE_OUT=$(mktemp)
PROBE_OK=0
for ATTEMPT in $(seq 1 20); do
  CODEX_STATUS=unavailable
  if "$ORION_CODEX_BIN" exec --ephemeral --ignore-user-config --ignore-rules \
      --skip-git-repo-check --sandbox read-only -C /tmp -m gpt-5.6-terra \
      -o "$PROBE_OUT" "Reply with exactly the single word OK and nothing else." \
      >"$CAMP/infra/redispatch_codex_probe_attempt_${ATTEMPT}.stdout" \
      2>"$CAMP/infra/redispatch_codex_probe_attempt_${ATTEMPT}.log"; then
    if [ -s "$PROBE_OUT" ]; then CODEX_STATUS=ok; fi
  fi
  rm -f "$PROBE_OUT"; PROBE_OUT=$(mktemp)
  if "$PY" - "$PROBE_OUT" >"$CAMP/infra/redispatch_channel_probe_attempt_${ATTEMPT}.json" 2>"$CAMP/infra/redispatch_channel_probe_attempt_${ATTEMPT}.log" <<'PROBE'
import json, os, sys, urllib.request
out_path = sys.argv[1]
base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
body = json.dumps({
    "model": os.environ["ANTHROPIC_MODEL"], "max_tokens": 16, "temperature": 0,
    "system": "You are a bounded experimental software-debugging arm.",
    "messages": [{"role": "user", "content": "Reply with exactly the single word OK and nothing else."}],
}).encode()
req = urllib.request.Request(url, data=body, headers={
    "x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"],
    "anthropic-version": "2023-06-01", "content-type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as raw:
    data = json.load(raw)
text = "".join(str(x.get("text", "")) for x in data.get("content", []) if isinstance(x, dict))
open(out_path, "w").write(text)
print(json.dumps({"http": "ok", "reply": text}))
PROBE
  then
    if [ -s "$PROBE_OUT" ]; then
      PROBE_OK=1
      echo "PROBE_OK attempt=$ATTEMPT codex=$CODEX_STATUS channel_reply=$(cat "$PROBE_OUT")"
      break
    fi
  fi
  echo "PROBE_FAIL attempt=$ATTEMPT codex=$CODEX_STATUS (channel probe did not complete)"
  [ "$ATTEMPT" -eq 20 ] && { echo "PROBE_EXHAUSTED_AFTER_20_ATTEMPTS"; exit 3; }
  sleep 1800
done
rm -f "$PROBE_OUT"

# ---- guarded re-dispatch of EXECUTION_FAILED_MODEL_RESPONSE envelopes ----
cd "$SRC"
MAX_PASSES=12
for PASS in $(seq 1 $MAX_PASSES); do
  date -u +"PASS $PASS SCAN %Y-%m-%dT%H:%M:%SZ"
  "$PY" - > "$RUN/e30-redispatch-pending.tsv" <<'SCAN'
import json
from pathlib import Path
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
frozen = json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())
tasks = [t["task_id"] for t in frozen["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION",
        "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
pending = 0
for rep in ("1", "2", "3"):
    for arm in arms:
        for task in tasks:
            p = run / f"confirmatory-r{rep}/responses/{arm}/{task}.json"
            if not p.is_file():
                print(rep, arm, task, sep="\t"); pending += 1; continue
            try:
                d = json.loads(p.read_text())
            except Exception:
                print(rep, arm, task, sep="\t"); pending += 1; continue
            if d.get("status") == "EXECUTION_FAILED_MODEL_RESPONSE":
                print(rep, arm, task, sep="\t"); pending += 1
import sys
print(f"pass_pending={pending}", file=sys.stderr)
SCAN
  N=$(grep -c . "$RUN/e30-redispatch-pending.tsv" || true)
  echo "PASS $PASS pending=$N"
  if [ "$N" -eq 0 ]; then echo "ALL_RESPONSES_REAL"; break; fi
  WORKER=$(mktemp /tmp/e30redis.XXXXXX.sh)
  cat > "$WORKER" <<'W'
#!/usr/bin/env bash
set -uo pipefail
REP="$1"; ARM="$2"; TASK="$3"
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; PY="$RUN/venv/bin/python"; SRC="$CAMP/source"
RESP="$RUN/confirmatory-r$REP/responses/$ARM/$TASK.json"
ST=$("$PY" -c "import json,sys;print(json.load(open(sys.argv[1])).get('status'))" "$RESP" 2>/dev/null || echo BROKEN)
if [ "$ST" != "EXECUTION_FAILED_MODEL_RESPONSE" ]; then
  echo "SKIP $REP $ARM $TASK status=$ST"; exit 0
fi
cd "$SRC"
"$PY" scripts/orion_claude_arms.py --request "$RUN/confirmatory-r$REP/requests/$ARM/$TASK.json" --response "$RESP"
echo "DONE $REP $ARM $TASK -> $("$PY" -c "import json,sys;print(json.load(open(sys.argv[1])).get('status'))" "$RESP" 2>/dev/null || echo unreadable)"
W
  chmod +x "$WORKER"
  xargs -P 2 -n 3 "$WORKER" < "$RUN/e30-redispatch-pending.tsv" || echo "PASS $PASS had nonzero worker exits (continuing)"
  sleep 300
done

# ---- final stock + chain terminal eval on complete stock ----
FINAL_PENDING=0
"$PY" - <<'FINAL'
import json
from pathlib import Path
from collections import Counter
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
frozen = json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())
tasks = [t["task_id"] for t in frozen["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION",
        "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
c = Counter(); pending = 0
for rep in ("1", "2", "3"):
    for arm in arms:
        for task in tasks:
            p = run / f"confirmatory-r{rep}/responses/{arm}/{task}.json"
            d = json.loads(p.read_text())
            c[d.get("status")] += 1
            if d.get("status") != "COMPLETED_PROPOSAL_ONLY":
                pending += 1
print("FINAL response statuses:", dict(c))
print(f"final_pending={pending}")
FINAL
FINAL_PENDING=$("$PY" - <<'FINAL'
import json
from pathlib import Path
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
frozen = json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())
tasks = [t["task_id"] for t in frozen["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION",
        "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
pending = 0
for rep in ("1", "2", "3"):
    for arm in arms:
        for task in tasks:
            d = json.loads((run / f"confirmatory-r{rep}/responses/{arm}/{task}.json").read_text())
            if d.get("status") != "COMPLETED_PROPOSAL_ONLY":
                pending += 1
print(pending)
FINAL
)
echo "FINAL_PENDING=$FINAL_PENDING"
if [ "$FINAL_PENDING" -ne 0 ]; then
  echo "STOCK_INCOMPLETE_PENDING_$FINAL_PENDING -- eval NOT chained; inspect and re-defer (receipt: E30_R11_MODEL_DISPATCH_DEFICIT_RECEIPT.json)"
  exit 3
fi
EVALJOB=$(sbatch --parsable "$E45/e30_eval_r11_core480_single.sbatch")
echo "CHAINED_EVAL_JOB=$EVALJOB"
ANAJOB=$(sbatch --parsable --dependency=afterok:"$EVALJOB" "$E45/e30_analysis_r11_terminal.sbatch")
echo "CHAINED_ANALYSIS_JOB=$ANAJOB (afterok:$EVALJOB)"
echo REDISPATCH_DONE $(date -u +%FT%TZ)
