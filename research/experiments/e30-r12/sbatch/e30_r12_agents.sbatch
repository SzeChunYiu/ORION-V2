#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r12-agents
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/agents-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/agents-%j.err
# E30-R12 model dispatch: 4 arms x 40 tasks x 3 reps = 480 responses.
#
# Guarded and resumable exactly as E30-R11's redispatch was: each pass rescans the
# response envelopes and invokes the arm ONLY where the response is absent or carries
# EXECUTION_FAILED_MODEL_RESPONSE (an envelope failure holds no model output, so
# re-dispatching it is execution repair, not resampling).  A COMPLETED_PROPOSAL_ONLY
# response is never touched -- design section 12, no-rescue clause.
#
# The served-model pin is fatal: scripts/orion_claude_arms.py raises ServedModelMismatch
# out of run_arm, so a substituted model kills the worker instead of writing a mixed
# dataset.  A pass whose workers all die that way leaves the pending set unchanged and
# the final stock check refuses to chain evaluation.
set -euo pipefail
source "$(dirname "$0")/e30_r12_common.sh"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ANTHROPIC_MODEL="${E30R12_REQUESTED_MODEL:-glm-5.3}"
export ORION_ARM_SERVED_MODEL="${E30R12_SERVED_MODEL:-glm-5.3}"
# Registered execution-resource contract (design, execution_lane_contract): the primary
# budget is the one under which 466 of E30-R11's 480 envelopes completed; passes 7+ apply
# R11's registered raise, and ONLY to envelopes that carry no model output.
PRIMARY_BUDGET=${E30R12_PRIMARY_BUDGET:-6000}
ESCALATED_BUDGET=${E30R12_ESCALATED_BUDGET:-36000}
ESCALATE_FROM_PASS=${E30R12_ESCALATE_FROM_PASS:-7}
export ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET="$PRIMARY_BUDGET"
export ORION_ARM_HTTP_RETRIES=10

# ---- coordinator authorization gate (design section 13) ----
# Dispatch is refused unless a human-written authorization exists AND acknowledges the
# exact design bytes: a design edited after authorization is a different study.
AUTH="$R12/E30_R12_COORDINATOR_AUTHORIZATION.json"
DESIGN_SHA=$(sha256sum "$DESIGN" | cut -c1-64)
AUTH="$AUTH" DESIGN_SHA="$DESIGN_SHA" "$PY" - <<'AUTHZ'
import json, os, sys
from pathlib import Path
path = Path(os.environ["AUTH"])
if not path.is_file():
    print(f"AUTHORIZATION_ABSENT: {path}"); sys.exit(4)
auth = json.loads(path.read_text())
expected = os.environ["DESIGN_SHA"]
problems = []
if auth.get("human_written") is not True:
    problems.append("human_written is not true")
if len(str(auth.get("human_written_token", ""))) < 16:
    problems.append("human_written_token shorter than 16 characters")
if auth.get("acknowledged_design_sha256") != expected:
    problems.append(f"acknowledged_design_sha256 {auth.get('acknowledged_design_sha256')} != {expected}")
if not str(auth.get("verbatim_operator_instruction", "")).strip():
    problems.append("verbatim_operator_instruction is empty")
if problems:
    print("AUTHORIZATION_INVALID:", "; ".join(problems)); sys.exit(4)
print("AUTHORIZATION_OK design_sha256", expected)
AUTHZ

# ---- the arms must import the post-#168 emission module from the R12 tree ----
R12SRC="$R12SRC" "$PY" -c "
import inspect, os, sys
import orion_v2.patch_emission as m
path = inspect.getfile(m)
print('patch_emission ->', path)
sys.exit(0 if path.startswith(os.environ['R12SRC']) else 3)"

MAX_PASSES=${E30R12_MAX_PASSES:-12}
for PASS in $(seq 1 "$MAX_PASSES"); do
  date -u +"PASS $PASS SCAN %Y-%m-%dT%H:%M:%SZ"
  R12="$R12" "$PY" - > "$RUN/e30r12-pending.tsv" <<'SCAN'
import json, os, sys
from pathlib import Path
run = Path(os.environ["R12"]) / "run"
tasks = [t["task_id"] for t in json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
pending = 0
for rep in ("1", "2", "3"):
    for arm in arms:
        for task in tasks:
            p = run / f"confirmatory-r{rep}/responses/{arm}/{task}.json"
            if not p.is_file():
                print(rep, arm, task, sep="\t"); pending += 1; continue
            try:
                status = json.loads(p.read_text()).get("status")
            except Exception:
                status = "BROKEN"
            if status != "COMPLETED_PROPOSAL_ONLY":
                print(rep, arm, task, sep="\t"); pending += 1
print(f"pass_pending={pending}", file=sys.stderr)
SCAN
  N=$(grep -c . "$RUN/e30r12-pending.tsv" || true)
  if [ "$PASS" -ge "$ESCALATE_FROM_PASS" ]; then
    export ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET="$ESCALATED_BUDGET"
  fi
  echo "PASS $PASS pending=$N budget=$ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET"
  [ "$N" -eq 0 ] && { echo "ALL_RESPONSES_REAL"; break; }
  rm -f "$RUN/.served-model-mismatch"
  WORKER=$(mktemp /tmp/e30r12.XXXXXX.sh)
  cat > "$WORKER" <<W
#!/usr/bin/env bash
set -uo pipefail
REP="\$1"; ARM="\$2"; TASK="\$3"
RUN="$RUN"; PY="$PY"; SRC="$R12SRC"
export PYTHONPATH="$R12SRC/src"
# ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET is inherited from the pass loop through xargs.
RESP="\$RUN/confirmatory-r\$REP/responses/\$ARM/\$TASK.json"
if [ -f "\$RESP" ]; then
  ST=\$("\$PY" -c "import json,sys;print(json.load(open(sys.argv[1])).get('status'))" "\$RESP" 2>/dev/null || echo BROKEN)
  [ "\$ST" = "COMPLETED_PROPOSAL_ONLY" ] && { echo "SKIP \$REP \$ARM \$TASK"; exit 0; }
fi
cd "\$SRC"
ERR=\$(mktemp)
if "\$PY" scripts/orion_claude_arms.py --request "\$RUN/confirmatory-r\$REP/requests/\$ARM/\$TASK.json" --response "\$RESP" 2>"\$ERR"; then
  rm -f "\$ERR"; echo "DONE \$REP \$ARM \$TASK"; exit 0
fi
# A served-model substitution is fatal for the whole study, not for one cell: it would
# split the campaign across two models and destroy every paired contrast.  Raise a
# sentinel the pass loop aborts on instead of quietly retrying 11 more times.
if grep -q "ServedModelMismatch" "\$ERR"; then
  cp "\$ERR" "\$RUN/.served-model-mismatch"
  echo "SERVED_MODEL_MISMATCH \$REP \$ARM \$TASK"; rm -f "\$ERR"; exit 9
fi
echo "ARM_EXIT_NONZERO \$REP \$ARM \$TASK"; sed -n "1,5p" "\$ERR"; rm -f "\$ERR"; exit 0
W
  chmod +x "$WORKER"
  xargs -P "${E30R12_CONCURRENCY:-2}" -n 3 "$WORKER" < "$RUN/e30r12-pending.tsv" \
    || echo "PASS $PASS had nonzero worker exits (continuing)"
  rm -f "$WORKER"
  if [ -f "$RUN/.served-model-mismatch" ]; then
    echo "HALT_SERVED_MODEL_MISMATCH -- the provider substituted a model; the campaign"
    echo "cannot mix served models across a paired contrast (design gate GR0c)."
    cat "$RUN/.served-model-mismatch"
    exit 4
  fi
  sleep 120
done

R12="$R12" "$PY" - <<'FINAL'
import json, os, sys
from collections import Counter
from pathlib import Path
run = Path(os.environ["R12"]) / "run"
tasks = [t["task_id"] for t in json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
counts, pending, served = Counter(), 0, Counter()
for rep in ("1", "2", "3"):
    for arm in arms:
        for task in tasks:
            p = run / f"confirmatory-r{rep}/responses/{arm}/{task}.json"
            if not p.is_file():
                pending += 1; counts["MISSING"] += 1; continue
            d = json.loads(p.read_text())
            counts[d.get("status")] += 1
            if d.get("status") != "COMPLETED_PROPOSAL_ONLY":
                pending += 1
            for value in (d.get("resource_receipt") or {}).get("served_model_ids", []):
                served[value] += 1
print("FINAL response statuses:", dict(counts))
print("FINAL served model ids:", dict(served))
sys.exit(0 if pending == 0 and len(served) == 1 else 3)
FINAL
echo "AGENTS_COMPLETE_480 $(date -u +%FT%TZ)"
