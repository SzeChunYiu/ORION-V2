#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r11-top429
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/top429-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/top429-%j.err
set -euo pipefail
# 429-DEFICIT TOPUP for E30 R11: 247/480 response envelopes carry
# agent_status=EXECUTION_FAILED_MODEL_RESPONSE (HTTP 429; NO model output
# inside -- per the mission's disposition rule these are infra failures,
# safe to rerun; rerunning cannot resample a model output that does not
# exist). GUARD: each pass re-scans envelopes and invokes the one-shot
# command ONLY for envelopes still in EXECUTION_FAILED_MODEL_RESPONSE
# status; COMPLETED_PROPOSAL_ONLY responses are never rewritten.
# Command pattern identical to e30_agents_r11_core480_retry.sbatch.
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; SRC="$CAMP/source"; PY="$RUN/venv/bin/python"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET=6000
export ORION_ARM_HTTP_RETRIES=10
cd "$SRC"

MAX_PASSES=8
for PASS in $(seq 1 $MAX_PASSES); do
  date -u +"PASS $PASS SCAN %Y-%m-%dT%H:%M:%SZ"
  "$PY" - > "$RUN/e30-429-pending.tsv" <<'PY'
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
PY
  N=$(grep -c . "$RUN/e30-429-pending.tsv" || true)
  echo "PASS $PASS pending=$N"
  if [ "$N" -eq 0 ]; then echo "ALL_RESPONSES_REAL"; break; fi
  WORKER=$(mktemp /tmp/e30top429.XXXXXX.sh)
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
  xargs -P 2 -n 3 "$WORKER" < "$RUN/e30-429-pending.tsv" || echo "PASS $PASS had nonzero worker exits (continuing)"
  sleep 180
done

"$PY" - <<'PY'
import json
from pathlib import Path
from collections import Counter
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
frozen = json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())
tasks = [t["task_id"] for t in frozen["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION",
        "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
c = Counter()
for rep in ("1", "2", "3"):
    for arm in arms:
        for task in tasks:
            d = json.loads((run / f"confirmatory-r{rep}/responses/{arm}/{task}.json").read_text())
            c[d.get("status")] += 1
print("FINAL response statuses:", dict(c))
PY
echo TOP429_DONE
