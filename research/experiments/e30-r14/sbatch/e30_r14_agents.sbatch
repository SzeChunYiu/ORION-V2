#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r14-agents
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/agents-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/agents-%j.err
# E30-R14 model dispatch: 4 arms x 40 tasks x 3 reps = 480 responses.
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
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R14 (exported by the submitting environment) instead.
: "${R14:?set R14=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R14_SBATCH_DIR:-$R14/source/research/experiments/e30-r14/sbatch}"
source "$SBATCH_DIR/e30_r14_common.sh"
set -a; source "$HOME/.orion-campaign.env"; set +a
export ANTHROPIC_MODEL="${E30R14_REQUESTED_MODEL:-glm-5.3}"
export ORION_ARM_SERVED_MODEL="${E30R14_SERVED_MODEL:-glm-5.3}"
# ---- registered execution-resource contract (design section: execution_lane_contract) ----
#
# E30-R14 sets the PER-CALL cap directly and does NOT set
# ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET.  The runner divides that total by the arm's call
# count, so E30-R12's single registered figure silently gave SIMPLE_DIRECT three times
# the per-call headroom of F0 and F2 -- an execution asymmetry inside a paired contrast,
# registered as if it were one number.  A per-call cap is identical across arms by
# construction.
#
# There is also no escalation ladder.  The cap is derived from the measured output-length
# distribution under the registered contract (E30_R14_BUDGET_NOTE_V1.json) at four times
# the observed maximum, so it is intended to be NON-BINDING; if a call ever stops at
# max_tokens, that is a channel-behaviour violation for GR0e to catch and report, not a
# resource shortfall to be topped up mid-campaign.
export ORION_ARM_MAX_TOKENS="${E30R14_PER_CALL_MAX_TOKENS:?set E30R14_PER_CALL_MAX_TOKENS to the registered per-call cap}"
unset ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET
export ORION_ARM_HTTP_RETRIES=10
echo "CHANNEL_CONTRACT=$ORION_ARM_CHANNEL_CONTRACT PER_CALL_MAX_TOKENS=$ORION_ARM_MAX_TOKENS EDIT_INTERFACE=$ORION_EDIT_INTERFACE PRESENTATION=$ORION_PRESENTATION_POLICY"

# ---- coordinator authorization gate (design section 13) ----
# Dispatch is refused unless a coordinator authorization exists, quotes the operator's
# verbatim instruction with its source, and acknowledges the exact design bytes: a design
# edited after authorization is a different study.  The file is coordinator-written by
# construction -- claiming otherwise would fabricate custody -- so what is asserted is that
# the human instruction it quotes is present and attributed, not that a human typed the file.
AUTH="$R14/PROTECTED_RUN_AUTHORIZATION.json"
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
if auth.get("coordinator_written") is not True:
    problems.append("coordinator_written is not true")
if auth.get("human_written") is not None:
    problems.append("human_written must not be claimed: this file is coordinator-written")
if not str(auth.get("operator_instruction_source", "")).strip():
    problems.append("operator_instruction_source is empty")
if auth.get("acknowledged_design_sha256") != expected:
    problems.append(f"acknowledged_design_sha256 {auth.get('acknowledged_design_sha256')} != {expected}")
if not str(auth.get("verbatim_operator_instruction", "")).strip():
    problems.append("verbatim_operator_instruction is empty")
if problems:
    print("AUTHORIZATION_INVALID:", "; ".join(problems)); sys.exit(4)
print("AUTHORIZATION_OK design_sha256", expected)
AUTHZ

# ---- the arms must import the post-#168 emission module from the R14 tree ----
R14SRC="$R14SRC" "$PY" -c "
import inspect, os, sys
import orion_v2.patch_emission as m
path = inspect.getfile(m)
print('patch_emission ->', path)
sys.exit(0 if path.startswith(os.environ['R14SRC']) else 3)"

MAX_PASSES=${E30R14_MAX_PASSES:-12}
for PASS in $(seq 1 "$MAX_PASSES"); do
  date -u +"PASS $PASS SCAN %Y-%m-%dT%H:%M:%SZ"
  R14="$R14" "$PY" - > "$RUN/e30r14-pending.tsv" <<'SCAN'
import json, os, sys
from pathlib import Path
run = Path(os.environ["R14"]) / "run"
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
  N=$(grep -c . "$RUN/e30r14-pending.tsv" || true)
  echo "PASS $PASS pending=$N per_call_max_tokens=$ORION_ARM_MAX_TOKENS contract=$ORION_ARM_CHANNEL_CONTRACT"
  [ "$N" -eq 0 ] && { echo "ALL_RESPONSES_REAL"; break; }
  rm -f "$RUN/.served-model-mismatch"
  WORKER=$(mktemp /tmp/e30r14.XXXXXX.sh)
  cat > "$WORKER" <<W
#!/usr/bin/env bash
set -uo pipefail
REP="\$1"; ARM="\$2"; TASK="\$3"
RUN="$RUN"; PY="$PY"; SRC="$R14SRC"
export PYTHONPATH="$R14SRC/src"
# ORION_ARM_MAX_TOKENS and ORION_ARM_CHANNEL_CONTRACT are inherited through xargs.
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
  xargs -P "${E30R14_CONCURRENCY:-2}" -n 3 "$WORKER" < "$RUN/e30r14-pending.tsv" \
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

R14="$R14" "$PY" - <<'FINAL'
import json, os, sys
from collections import Counter
from pathlib import Path
run = Path(os.environ["R14"]) / "run"
tasks = [t["task_id"] for t in json.loads((run / "confirmatory-r1/frozen_tasks.json").read_text())["tasks"]]
arms = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
counts, pending, served = Counter(), 0, Counter()
contracts, stops = Counter(), Counter()
envelopes_with_a_channel_receipt = 0
envelopes_with_an_interface_receipt, interface_shas = 0, Counter()
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
            iface = d.get("interface_receipt")
            if isinstance(iface, dict):
                envelopes_with_an_interface_receipt += 1
                interface_shas[iface.get("edit_interface_sha256")] += 1
            channel = d.get("channel_receipt")
            if isinstance(channel, dict):
                envelopes_with_a_channel_receipt += 1
                for value in channel.get("contract_sha256s", []):
                    contracts[value] += 1
                for value in channel.get("stop_reasons", []):
                    stops[value] += 1
print("FINAL response statuses:", dict(counts))
print("FINAL served model ids:", dict(served))
# Denominators, printed: a homogeneity line over zero receipts is not a pass, and the
# exit below refuses it rather than letting a silent 0/0 read as agreement.
print(f"FINAL channel receipts: {envelopes_with_a_channel_receipt}/480 envelopes")
print("FINAL channel contract sha256s:", dict(contracts))
print("FINAL stop reasons:", dict(stops))
print(f"FINAL interface receipts: {envelopes_with_an_interface_receipt}/480 envelopes; sha256s:", dict(interface_shas))
ok = (pending == 0 and len(served) == 1
      and envelopes_with_a_channel_receipt == 480
      and len(contracts) == 1
      and envelopes_with_an_interface_receipt == 480
      and len(interface_shas) == 1
      and set(stops) <= {"end_turn"})
sys.exit(0 if ok else 3)
FINAL
echo "AGENTS_COMPLETE_480 $(date -u +%FT%TZ)"
