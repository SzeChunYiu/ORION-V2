#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r11-syntax
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=24
#SBATCH --mem=96G
#SBATCH --time=12:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/syntax-single-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/syntax-single-%j.err
set -euo pipefail
# SYNTAX-SENSITIVITY re-evaluation (frozen E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1):
# same frozen-lane driver over run/confirmatory-syntax-r<R> (canonicalized
# patches ONLY where canonical_sha256 != original_sha256; unchanged tasks carry
# copied raw evaluation records). Single-job 6-worker form because the account
# hit AssocMaxSubmitJobLimit from a sibling lane's pending array.
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; PY="$RUN/venv/bin/python"
LOGD=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/syntax-items
mkdir -p "$LOGD"

"$PY" - > "$RUN/sensitivity/syntax-eval-pending.tsv" <<'PY'
import json, sys
from pathlib import Path
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
items = json.loads((run / "sensitivity/syntax-eval-taskmap.json").read_text())
pending, done = [], 0
for x in items:
    rep, arm, task = x["repeat"], x["arm"], x["task"]
    ev = run / f"confirmatory-syntax-r{rep}/evaluations/{arm}/{task}.json"
    if ev.is_file():
        try:
            if "evaluation_lane" in json.loads(ev.read_text()):
                done += 1
                continue
        except Exception:
            pass
    pending.append(f"{rep}\t{arm}\t{task}")
print("\n".join(pending))
print(f"already_done={done} pending={len(pending)}", file=sys.stderr)
PY

WORKER=$(mktemp /tmp/e30syntaxworker.XXXXXX.sh)
cat > "$WORKER" <<'W'
#!/usr/bin/env bash
set -euo pipefail
REP="$1"; ARM="$2"; TASK="$3"
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; PY="$RUN/venv/bin/python"
LOGD=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/syntax-items
LOG="$LOGD/r${REP}-${ARM}-${TASK}.log"
{
  date -u +"START %Y-%m-%dT%H:%M:%SZ $REP $ARM $TASK"
  "$PY" "$RUN/e30_r11_arm_eval_frozen_lane.py" \
    --campaign "$CAMP" \
    --workdir "$RUN/confirmatory-syntax-r$REP" \
    --arms "$ARM" --tasks "$TASK" \
    --timeout-seconds 10800
  date -u +"END %Y-%m-%dT%H:%M:%SZ $REP $ARM $TASK"
} > "$LOG" 2>&1
W
chmod +x "$WORKER"

if [ -s "$RUN/sensitivity/syntax-eval-pending.tsv" ]; then
  date -u +"SYNTAX_EVAL_START %Y-%m-%dT%H:%M:%SZ"
  xargs -P 6 -n 3 "$WORKER" < "$RUN/sensitivity/syntax-eval-pending.tsv"
else
  date -u +"SYNTAX_EVAL_START %Y-%m-%dT%H:%M:%SZ (nothing pending)"
fi
date -u +"SYNTAX_EVAL_END %Y-%m-%dT%H:%M:%SZ"

"$PY" - <<'PY'
import json, sys
from pathlib import Path
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
items = json.loads((run / "sensitivity/syntax-eval-taskmap.json").read_text())
missing, nonlane = [], []
for x in items:
    rep, arm, task = x["repeat"], x["arm"], x["task"]
    ev = run / f"confirmatory-syntax-r{rep}/evaluations/{arm}/{task}.json"
    if not ev.is_file():
        missing.append(f"r{rep}/{arm}/{task}")
        continue
    if "evaluation_lane" not in json.loads(ev.read_text()):
        nonlane.append(f"r{rep}/{arm}/{task}")
print("missing:", len(missing), missing[:10])
print("non-frozen-lane:", len(nonlane), nonlane[:10])
sys.exit(0 if not missing and not nonlane else 3)
PY
echo SYNTAX_EVAL_COMPLETE
