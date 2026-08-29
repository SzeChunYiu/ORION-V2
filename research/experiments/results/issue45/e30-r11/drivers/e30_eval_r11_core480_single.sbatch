#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r11-eval480
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=24
#SBATCH --mem=96G
#SBATCH --time=12:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/eval480-single-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/eval480-single-%j.err
set -euo pipefail
# FROZEN-LANE terminal 480 evaluation, single-job form (the account hit
# AssocMaxSubmitJobLimit from a sibling lane's pending array, so this runs
# 6 workers INSIDE one job instead of a 480-element array). Same driver as
# e30_eval_r11_core480.sbatch: run/e30_r11_arm_eval_frozen_lane.py
# (stock orchestration/predicates + campaign frozen runtime; defect record:
# campaign E30_R11_EVALUATION_LANE_DEFECT_AND_ADAPTER.json). Resumable:
# items whose evaluation record already exists with the frozen-lane
# evaluation_lane marker are skipped (deterministic local recompute, never
# touches responses).
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; PY="$RUN/venv/bin/python"
LOGD=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/eval480-items
mkdir -p "$LOGD"

"$PY" - > "$RUN/e30-eval480-pending.tsv" <<'PY'
import json
from pathlib import Path
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
items = json.loads((run / "e30-taskmap-core480.json").read_text())
pending, done = [], 0
for x in items:
    rep, arm, task = x["repeat"], x["arm"], x["task"]
    ev = run / f"confirmatory-r{rep}/evaluations/{arm}/{task}.json"
    if ev.is_file():
        try:
            record = json.loads(ev.read_text())
            if "evaluation_lane" in record:
                done += 1
                continue
        except Exception:
            pass
    pending.append(f"{rep}\t{arm}\t{task}")
print("\n".join(pending))
import sys
print(f"already_done={done} pending={len(pending)}", file=sys.stderr)
PY

WORKER=$(mktemp /tmp/e30evalworker.XXXXXX.sh)
cat > "$WORKER" <<'W'
#!/usr/bin/env bash
set -euo pipefail
REP="$1"; ARM="$2"; TASK="$3"; shift 3
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; PY="$RUN/venv/bin/python"
LOGD=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r11/eval480-items
LOG="$LOGD/r${REP}-${ARM}-${TASK}.log"
{
  date -u +"START %Y-%m-%dT%H:%M:%SZ $REP $ARM $TASK"
  "$PY" "$RUN/e30_r11_arm_eval_frozen_lane.py" \
    --campaign "$CAMP" \
    --workdir "$RUN/confirmatory-r$REP" \
    --arms "$ARM" --tasks "$TASK" \
    --timeout-seconds 10800
  date -u +"END %Y-%m-%dT%H:%M:%SZ $REP $ARM $TASK"
} > "$LOG" 2>&1
W
chmod +x "$WORKER"

if [ -s "$RUN/e30-eval480-pending.tsv" ]; then
  date -u +"EVAL480_START %Y-%m-%dT%H:%M:%SZ"
  xargs -P 6 -n 3 "$WORKER" < "$RUN/e30-eval480-pending.tsv"
else
  date -u +"EVAL480_START %Y-%m-%dT%H:%M:%SZ (nothing pending)"
fi
date -u +"EVAL480_END %Y-%m-%dT%H:%M:%SZ"

# completeness check: every one of the 480 must have a frozen-lane record
"$PY" - <<'PY'
import json, sys
from pathlib import Path
run = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6/run")
items = json.loads((run / "e30-taskmap-core480.json").read_text())
missing, nonlane = [], []
for x in items:
    rep, arm, task = x["repeat"], x["arm"], x["task"]
    ev = run / f"confirmatory-r{rep}/evaluations/{arm}/{task}.json"
    if not ev.is_file():
        missing.append(f"r{rep}/{arm}/{task}")
        continue
    record = json.loads(ev.read_text())
    if "evaluation_lane" not in record:
        nonlane.append(f"r{rep}/{arm}/{task}")
print("missing:", len(missing), missing[:10])
print("non-frozen-lane:", len(nonlane), nonlane[:10])
sys.exit(0 if not missing and not nonlane else 3)
PY
echo EVAL480_COMPLETE
