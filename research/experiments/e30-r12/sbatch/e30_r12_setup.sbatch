#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r12-setup
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/setup-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r12/setup-%j.err
# Build the E30-R12 campaign from E30-R11's frozen substrate.
#
# R12 must present the SAME 40 frozen tasks under the SAME per-project runtimes, so
# the gold-blind requests, the frozen task table and the evaluator's private oracle
# tree are reused verbatim rather than regenerated -- the only thing that changes is
# the arm code (apply-clean emission) and the served-model pin.  responses/ and
# evaluations/ start EMPTY: R12 makes its own model calls.
#
# evaluator_private (11G) is symlinked, not copied: the frozen-lane adapter only ever
# copytree()s out of it into per-evaluation scratch, so the tree stays byte-identical
# and R11's custody is untouched.
set -euo pipefail
source "$(dirname "$0")/e30_r12_common.sh"
set -a; source "$HOME/.orion-campaign.env"; set +a

test -d "$R11" || { echo "R11 campaign missing"; exit 2; }
mkdir -p "$RUN"

# ---- gold-blind requests, frozen task table, taskmap, adapter ----
for REP in 1 2 3; do
  SRCREP="$R11/run/confirmatory-r$REP"; DSTREP="$RUN/confirmatory-r$REP"
  mkdir -p "$DSTREP/responses" "$DSTREP/evaluations" "$DSTREP/aggregate" "$DSTREP/logs"
  cp -an "$SRCREP/requests" "$DSTREP/requests" 2>/dev/null || true
  cp -n "$SRCREP/frozen_tasks.json" "$DSTREP/frozen_tasks.json"
done
cp -n "$R11/run/e30-taskmap-core480.json" "$RUN/e30-taskmap-core480.json"
cp -n "$R11/run/e30_r11_arm_eval_frozen_lane.py" "$ADAPTER"
cp -n "$R11/TASKMAP.json" "$R12/TASKMAP.json"
cp -rn "$R11/prepared" "$R12/prepared" 2>/dev/null || true
[ -e "$R12/evaluator_private" ] || ln -s "$R11/evaluator_private" "$R12/evaluator_private"
[ -e "$R12/inputs" ] || ln -s "$R11/inputs" "$R12/inputs"
# GR0(b) reads gold patches from baseline_lanes/<task>/BugsInPy/.../bug_patch.txt.
# Symlinked read-only: it is the same frozen BugsInPy checkout, and the gold control
# runs only after every arm response is written (design section 9, GR0b).
[ -e "$R12/baseline_lanes" ] || ln -s "$R11/baseline_lanes" "$R12/baseline_lanes"

# ---- adapter identity (the whole evaluation lane is pinned to this sha) ----
EXPECT=829abb411ccf0bd71182eea4c11d2e07fae60f3b743872f7b4fce0a8635aae93
GOT=$(sha256sum "$ADAPTER" | cut -c1-64)
[ "$GOT" = "$EXPECT" ] || { echo "ADAPTER_SHA_MISMATCH $GOT != $EXPECT"; exit 3; }

# ---- ORION-V2 source at the R12 anchor ----
: "${R12_SOURCE_SHA:?set R12_SOURCE_SHA to the merged PR sha}"
if [ ! -d "$R12SRC/.git" ]; then
  git clone --no-checkout https://github.com/SzeChunYiu/ORION-V2.git "$R12SRC" 2>/dev/null \
    || cp -a "$R11/source" "$R12SRC"
fi
if [ -d "$R12SRC/.git" ]; then
  git -C "$R12SRC" fetch --all --tags
  git -C "$R12SRC" checkout --force "$R12_SOURCE_SHA"
fi
git -C "$R12SRC" rev-parse HEAD > "$R12/infra/source_head.txt" 2>/dev/null || true
"$PY" -m py_compile "$R12SRC/scripts/orion_claude_arms.py"

# ---- served-model probe on the EXACT dispatch channel, fail closed ----
export ANTHROPIC_MODEL="${E30R12_REQUESTED_MODEL:-glm-5.3}"
export ORION_ARM_SERVED_MODEL="${E30R12_SERVED_MODEL:-glm-5.3}"
"$PY" - > "$R12/infra/served_model_probe.json" <<'PROBE'
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

# ---- run identity ----
"$PY" - <<'ID'
import json, os, hashlib
from pathlib import Path
r12 = Path(os.environ["R12"]); src = Path(os.environ["R12SRC"])
design = src / "research/experiments/e30-r12/E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json"
(r12 / "RUN_IDENTITY.json").write_text(json.dumps({
    "schema_version": "orion.v2.execution-run-identity.v1",
    "run_id": r12.name, "study_id": "E30-R12",
    "design": "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1",
    "design_sha256": hashlib.sha256(design.read_bytes()).hexdigest() if design.is_file() else None,
    "source_sha": os.environ.get("R12_SOURCE_SHA"),
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
echo "SETUP_OK $(date -u +%FT%TZ)"
