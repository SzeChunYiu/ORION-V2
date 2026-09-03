#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r13-setup
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r13/setup-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r13/setup-%j.err
# Build the E30-R13 campaign from E30-R11's frozen substrate.
#
# R13 must present the SAME 40 frozen tasks under the SAME per-project runtimes, so
# the gold-blind requests, the frozen task table and the evaluator's private oracle
# tree are reused verbatim rather than regenerated -- the only thing that changes is
# the arm code (apply-clean emission) and the served-model pin.  responses/ and
# evaluations/ start EMPTY: R13 makes its own model calls.
#
# evaluator_private (11G) is symlinked, not copied: the frozen-lane adapter only ever
# copytree()s out of it into per-evaluation scratch, so the tree stays byte-identical
# and R11's custody is untouched.
set -euo pipefail
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R13 (exported by the submitting environment) instead.
: "${R13:?set R13=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R13_SBATCH_DIR:-$R13/source/research/experiments/e30-r13/sbatch}"
source "$SBATCH_DIR/e30_r13_common.sh"
set -a; source "$HOME/.orion-campaign.env"; set +a

test -d "$R11" || { echo "R11 campaign missing"; exit 2; }
mkdir -p "$RUN"

# ---- gold-blind requests, frozen task table, taskmap, adapter ----
for REP in 1 2 3; do
  SRCREP="$R11/run/confirmatory-r$REP"; DSTREP="$RUN/confirmatory-r$REP"
  mkdir -p "$DSTREP/responses" "$DSTREP/evaluations" "$DSTREP/aggregate" "$DSTREP/logs"
  # Per-arm directories up front: the evaluator derives the cell's arm set from the
  # responses/ subdirectories, so without them it cannot construct the cell at all and
  # the layout is unvalidatable until the first response lands.
  for ARM in $ARMS; do mkdir -p "$DSTREP/responses/$ARM" "$DSTREP/evaluations/$ARM"; done
  # Idempotent and LOUD: a swallowed copy failure here would leave the dispatch with
  # no requests, which the 480-request assertion below would then have to catch.
  [ -d "$DSTREP/requests" ] || cp -a "$SRCREP/requests" "$DSTREP/requests"
  [ -f "$DSTREP/frozen_tasks.json" ] || cp -a "$SRCREP/frozen_tasks.json" "$DSTREP/frozen_tasks.json"
done
[ -f "$RUN/e30-taskmap-core480.json" ] || cp -a "$R11/run/e30-taskmap-core480.json" "$RUN/e30-taskmap-core480.json"
[ -f "$ADAPTER" ] || cp -a "$R11/run/e30_r11_arm_eval_frozen_lane.py" "$ADAPTER"
[ -f "$R13/TASKMAP.json" ] || cp -a "$R11/TASKMAP.json" "$R13/TASKMAP.json"
[ -f "$R13/SETUP_RECEIPT.json" ] || cp -a "$R11/SETUP_RECEIPT.json" "$R13/SETUP_RECEIPT.json"
# prepared/solver_public holds the gold-blind solver workspaces the reused requests name
# by ABSOLUTE path; symlinked so the arms read the identical frozen trees rather than a
# copy that could drift.  Read-only: emission's git apply --check never mutates them.
[ -e "$R13/prepared" ] || ln -s "$R11/prepared" "$R13/prepared"
[ -e "$R13/evaluator_private" ] || ln -s "$R11/evaluator_private" "$R13/evaluator_private"
[ -e "$R13/inputs" ] || ln -s "$R11/inputs" "$R13/inputs"
# GR0(b) reads gold patches from baseline_lanes/<task>/BugsInPy/.../bug_patch.txt.
# Symlinked read-only: it is the same frozen BugsInPy checkout, and the gold control
# runs only after every arm response is written (design section 10, GR0b).
[ -e "$R13/baseline_lanes" ] || ln -s "$R11/baseline_lanes" "$R13/baseline_lanes"

# ---- adapter identity (the whole evaluation lane is pinned to this sha) ----
EXPECT=829abb411ccf0bd71182eea4c11d2e07fae60f3b743872f7b4fce0a8635aae93
GOT=$(sha256sum "$ADAPTER" | cut -c1-64)
[ "$GOT" = "$EXPECT" ] || { echo "ADAPTER_SHA_MISMATCH $GOT != $EXPECT"; exit 3; }

# ---- ORION-V2 source at the R13 anchor ----
# NO FALLBACK.  A degraded source tree here would dispatch the pre-#168 arm code that
# this whole study exists to replace, and every compile check would still pass, so a
# failure to reach the anchor sha must abort setup rather than silently continue.
: "${R13_SOURCE_SHA:?set R13_SOURCE_SHA to the merged PR sha}"
test -d "$R13SRC/.git" || { echo "R13SRC is not a git clone: $R13SRC"; exit 3; }
# A clone pre-staged at the anchor needs no network; anything else must reach it.
if [ "$(git -C "$R13SRC" rev-parse HEAD)" != "$R13_SOURCE_SHA" ]; then
  git -C "$R13SRC" fetch --all --tags
  git -C "$R13SRC" checkout --force "$R13_SOURCE_SHA"
fi
HEAD_SHA=$(git -C "$R13SRC" rev-parse HEAD)
[ "$HEAD_SHA" = "$R13_SOURCE_SHA" ] || { echo "SOURCE_SHA_MISMATCH $HEAD_SHA != $R13_SOURCE_SHA"; exit 3; }
echo "$HEAD_SHA" > "$R13/infra/source_head.txt"
"$PY" -m py_compile "$R13SRC/scripts/orion_claude_arms.py"

# ---- the arms must import the POST-#168 emission module, from THIS tree ----
grep -q "emit_apply_clean_patch" "$R13SRC/scripts/orion_claude_arms.py" \
  || { echo "ARM_EXECUTABLE_PREDATES_PR168"; exit 3; }
grep -q "ORION_ARM_SERVED_MODEL" "$R13SRC/scripts/orion_claude_arms.py" \
  || { echo "ARM_EXECUTABLE_LACKS_SERVED_MODEL_PIN"; exit 3; }
grep -q "ORION_ARM_CHANNEL_CONTRACT" "$R13SRC/scripts/orion_claude_arms.py" \
  || { echo "ARM_EXECUTABLE_LACKS_CHANNEL_CONTRACT"; exit 3; }
R13SRC="$R13SRC" "$PY" - <<'PROV'
import inspect, os, sys
import orion_v2.patch_emission as emission
import orion_v2.unified_diff_interface as canon
src = os.environ["R13SRC"]
for module in (emission, canon):
    path = inspect.getfile(module)
    print(module.__name__, "->", path)
    if not path.startswith(src):
        print(f"IMPORT_PROVENANCE_FAIL: {module.__name__} resolves outside {src}")
        sys.exit(3)
assert hasattr(emission, "emit_apply_clean_patch")
print("IMPORT_PROVENANCE_OK")
PROV

# ---- the dispatched request-body contract IS the one the design froze ----
# Compared by sha256 over the contract bytes, computed by the arms executable itself.
# A label comparison would pass while the body behind the label changed -- which is the
# class of drift that ended E30-R12, one level up.
R13SRC="$R13SRC" DESIGN="$DESIGN" CONTRACT="$CHANNEL_CONTRACT" \
CAP="${E30R13_PER_CALL_MAX_TOKENS:?set E30R13_PER_CALL_MAX_TOKENS}" "$PY" - <<'CONTRACT'
import importlib.util, json, os, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location(
    "arms", os.environ["R13SRC"] + "/scripts/orion_claude_arms.py")
arms = importlib.util.module_from_spec(spec); spec.loader.exec_module(arms)
name = os.environ["CONTRACT"]
design = json.loads(Path(os.environ["DESIGN"]).read_text())
registered = design["model_binding"]["request_body_contract"]
problems = []
if registered["contract_id"] != name:
    problems.append(f"dispatching {name!r} but the design registers {registered['contract_id']!r}")
if arms.CHANNEL_CONTRACTS.get(name) != registered["extra_body"]:
    problems.append(f"executable body {arms.CHANNEL_CONTRACTS.get(name)} != registered {registered['extra_body']}")
got = arms.channel_contract_sha256(name)
if got != registered["contract_sha256"]:
    problems.append(f"contract sha256 {got} != registered {registered['contract_sha256']}")
if arms.ARM_SYSTEM_PROMPT != registered["system"]:
    problems.append("system prompt differs from the registered contract")
# The dispatched cap must BE the registered cap.  GR0e only catches truncation, so a cap
# of 9000 or 40000 would run to completion, pass every gate, and be reported as the
# registered condition -- the same registered-value-versus-dispatched-value gap this
# study exists to close, one level down.
cap = int(os.environ["CAP"])
registered_cap = design["execution_lane_contract"]["per_call_output_token_cap"]
if cap != registered_cap:
    problems.append(f"per-call cap {cap} != registered {registered_cap}")
if problems:
    print("CHANNEL_CONTRACT_MISMATCH:", "; ".join(problems)); sys.exit(3)
print("CHANNEL_CONTRACT_OK", name, got, "per_call_max_tokens", cap)
CONTRACT

# ---- responses/ and evaluations/ must start EMPTY, on the FIRST setup only ----
# A new campaign identity means a clean run.  E30-R12 left 3 envelopes completed under
# the provider default; pooling them into a differently-configured campaign would mix
# two channel conditions inside one paired contrast while every gate still passed.
#
# Gated on a sentinel rather than applied unconditionally: the registered execution lane
# is resumable by pass rescan, and setup re-runs whenever the chain is resubmitted, so an
# unconditional assertion would block a legitimate resume and force a post-dispatch design
# change to unblock it.  The sentinel is written only after the first setup succeeds.
FIRST_SETUP="$R13/infra/first_setup_completed"
if [ -f "$FIRST_SETUP" ]; then
  echo "RESUMED_SETUP: emptiness assertion skipped (first setup completed $(cat "$FIRST_SETUP"))"
else
  R13="$R13" "$PY" - <<'EMPTY'
import json, os, sys
from pathlib import Path
run = Path(os.environ["R13"]) / "run"
responses = sorted(run.rglob("responses/*/*.json"))
evaluations = sorted(run.rglob("evaluations/*/*.json"))
print(f"pre-existing responses={len(responses)} evaluations={len(evaluations)} (both must be 0)")
for path in (responses + evaluations)[:10]:
    print("  ", path)
sys.exit(0 if not responses and not evaluations else 3)
EMPTY
fi

# ---- every reused request must name a solver workspace that exists and is readable ----
# Without it emit_apply_clean_patch cannot run its git apply --check verification: the
# patch would still be canonicalized, but blind, which quietly guts the study's premise
# while the arm keeps writing COMPLETED_PROPOSAL_ONLY.
R13="$R13" "$PY" - <<'WS'
import json, os, sys
from pathlib import Path
run = Path(os.environ["R13"]) / "run"
missing, checked = [], 0
for rep in ("1", "2", "3"):
    for request in sorted((run / f"confirmatory-r{rep}" / "requests").rglob("*.json")):
        raw = str(json.loads(request.read_text()).get("task", {}).get("solver_workspace", "")).strip()
        checked += 1
        if not raw or not Path(raw).is_dir() or not os.access(raw, os.R_OK):
            missing.append(f"{request.parent.name}/{request.stem}: {raw or '<empty>'}")
print(f"requests checked={checked} unreadable_workspaces={len(missing)}")
for item in missing[:10]:
    print("  ", item)
sys.exit(0 if checked == 480 and not missing else 3)
WS

# ---- served-model probe on the EXACT dispatch channel, fail closed ----
export ANTHROPIC_MODEL="${E30R13_REQUESTED_MODEL:-glm-5.3}"
export ORION_ARM_SERVED_MODEL="${E30R13_SERVED_MODEL:-glm-5.3}"
"$PY" - > "$R13/infra/served_model_probe.json" <<'PROBE'
import json, os, sys, urllib.request
base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
body = json.dumps({"model": os.environ["ANTHROPIC_MODEL"], "max_tokens": 16, "temperature": 0,
                   "system": "You are a bounded experimental software-debugging arm.",
                   "messages": [{"role": "user", "content": "Reply with exactly the single word OK."}]}).encode()
req = urllib.request.Request(url, data=body, headers={
    "x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"],
    "anthropic-version": "2023-06-01", "content-type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as raw:
    data = json.load(raw)
served = str(data.get("model", ""))
pinned = os.environ["ORION_ARM_SERVED_MODEL"]
print(json.dumps({"requested": os.environ["ANTHROPIC_MODEL"], "served": served,
                  "pinned": pinned, "match": served == pinned}, indent=2))
sys.exit(0 if served == pinned else 4)
PROBE

# ---- channel BEHAVIOUR probe on the EXACT dispatch channel, fail closed ----
# The served-model probe answers "which model id came back".  It cannot see the failure
# that ended E30-R12, in which the id was correct and the response carried no text at
# all.  This probe asserts the three properties the registered contract exists to
# guarantee: the turn ends of its own accord, text is emitted, and the cap is not
# reached.  It runs the frozen system prompt through the registered contract.
export ORION_ARM_CHANNEL_CONTRACT="$CHANNEL_CONTRACT"
PROBE_MAX_TOKENS="${E30R13_PER_CALL_MAX_TOKENS:?set E30R13_PER_CALL_MAX_TOKENS}" \
"$PY" - > "$R13/infra/channel_behaviour_probe.json" <<'BEHAVIOUR'
import importlib.util, json, os, sys, urllib.request
spec = importlib.util.spec_from_file_location(
    "arms", os.environ["R13SRC"] + "/scripts/orion_claude_arms.py")
arms = importlib.util.module_from_spec(spec); spec.loader.exec_module(arms)
name = arms.channel_contract_id()
base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
max_tokens = int(os.environ["PROBE_MAX_TOKENS"])
payload = {"model": os.environ["ANTHROPIC_MODEL"], "max_tokens": max_tokens,
           "temperature": 0, "system": arms.ARM_SYSTEM_PROMPT,
           "messages": [{"role": "user", "content":
                         "Return only one JSON object with keys patch and diagnosis. "
                         "Use the empty string for patch and the word probe for diagnosis."}]}
payload.update(arms.CHANNEL_CONTRACTS[name])
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
    "x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"],
    "anthropic-version": "2023-06-01", "content-type": "application/json"})
with urllib.request.urlopen(req, timeout=1800) as raw:
    data = json.load(raw)
blocks = [b for b in data.get("content", []) if isinstance(b, dict)]
text = "".join(str(b.get("text", "")) for b in blocks)
usage = data.get("usage", {}) or {}
result = {
    "contract_id": name, "contract_sha256": arms.channel_contract_sha256(name),
    "max_tokens": max_tokens, "served_model": str(data.get("model", "")),
    "stop_reason": data.get("stop_reason"),
    "output_tokens": int(usage.get("output_tokens", 0) or 0),
    "blocks": [{"type": str(b.get("type", "")),
                "chars": len(str(b.get(str(b.get("type", "")), "") or ""))} for b in blocks],
    "text_chars": len(text),
}
checks = {
    "stop_reason_is_end_turn": result["stop_reason"] == "end_turn",
    "text_chars_above_zero": result["text_chars"] > 0,
    "output_tokens_below_cap": 0 < result["output_tokens"] < max_tokens,
    "served_model_matches_pin": result["served_model"] == os.environ["ORION_ARM_SERVED_MODEL"],
}
result["checks"] = checks
result["status"] = "PASS" if all(checks.values()) else "FAIL"
print(json.dumps(result, indent=2, sort_keys=True))
sys.exit(0 if result["status"] == "PASS" else 4)
BEHAVIOUR

# ---- run identity ----
"$PY" - <<'ID'
import json, os, hashlib
from pathlib import Path
r13 = Path(os.environ["R13"]); src = Path(os.environ["R13SRC"])
design = src / "research/experiments/e30-r13/E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json"
(r13 / "RUN_IDENTITY.json").write_text(json.dumps({
    "schema_version": "orion.v2.execution-run-identity.v1",
    "run_id": r13.name, "study_id": "E30-R13",
    "design": "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1",
    "design_sha256": hashlib.sha256(design.read_bytes()).hexdigest() if design.is_file() else None,
    "source_sha": os.environ.get("R13_SOURCE_SHA"),
    "bugsinpy_commit": "11c5f1eea954a42132cfd06bf257766a7963e0fd",
    "requested_model": os.environ.get("ANTHROPIC_MODEL"),
    "pinned_served_model": os.environ.get("ORION_ARM_SERVED_MODEL"),
    "frozen_substrate_reused_from": os.environ["R11"],
    "reused": ["requests", "frozen_tasks.json", "TASKMAP.json", "prepared",
               "evaluator_private (symlink)", "inputs (symlink)",
               "e30_r11_arm_eval_frozen_lane.py"],
    "regenerated": ["responses", "evaluations"],
    "outcome_access": "NONE_UNTIL_RESPONSES_COMPLETE",
}, indent=2, sort_keys=True) + "\n")
ID
date -u +%FT%TZ > "$FIRST_SETUP"
echo "SETUP_OK $(date -u +%FT%TZ)"
