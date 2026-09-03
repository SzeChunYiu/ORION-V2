#!/usr/bin/env bash
# E30-R13 dispatch: write the coordinator authorization, then submit the whole chain.
#
# Run on the LUNARC login node AFTER the design PR merges:
#   bash e30_r13_dispatch_chain.sh <merge_sha> <design_sha256>
#
# Custody: the authorization file is written HERE, by the coordinator, and says so.
# The instruction it quotes is verbatim human chat input; the record of it is not
# human-written, and does not claim to be.  The dispatch gate in e30_r13_agents.sbatch
# refuses to run unless this file exists, quotes an attributed instruction, and
# acknowledges the exact design bytes -- so a design edited after authorization halts
# the study rather than silently running a different one.
set -euo pipefail
MERGE_SHA="${1:?usage: e30_r13_dispatch_chain.sh <merge_sha> <design_sha256>}"
DESIGN_SHA="${2:?usage: e30_r13_dispatch_chain.sh <merge_sha> <design_sha256>}"
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R13="${R13:?set R13=$E45/campaign-e30-r13-channelcontract-core4-rep3-<date>-<sha8>}"
# The per-call output-token cap, derived in E30_R13_BUDGET_NOTE_V1.json and registered in
# the design.  No default: a cap that silently falls back to a historical number is how
# E30-R12 inherited two budgets that were both inadequate.
: "${E30R13_PER_CALL_MAX_TOKENS:?set E30R13_PER_CALL_MAX_TOKENS to the registered per-call cap}"
E30R13_CHANNEL_CONTRACT="${E30R13_CHANNEL_CONTRACT:-thinking_disabled}"
SB="$R13/source/research/experiments/e30-r13/sbatch"
mkdir -p "$E45/logs-e30-r13"

git -C "$R13/source" fetch --quiet origin main
git -C "$R13/source" checkout --quiet --force "$MERGE_SHA"
HEAD_SHA=$(git -C "$R13/source" rev-parse HEAD)
[ "$HEAD_SHA" = "$MERGE_SHA" ] || { echo "SOURCE_CHECKOUT_FAILED $HEAD_SHA"; exit 2; }
GOT=$(sha256sum "$R13/source/research/experiments/e30-r13/E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json" | cut -c1-64)
[ "$GOT" = "$DESIGN_SHA" ] || { echo "DESIGN_SHA_MISMATCH got=$GOT want=$DESIGN_SHA"; exit 2; }

cat > "$R13/PROTECTED_RUN_AUTHORIZATION.json" <<AUTH
{
  "schema_version": "orion.v2.e30-r13-coordinator-authorization.v1",
  "study_id": "E30-R13",
  "design": "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1",
  "acknowledged_design_sha256": "$DESIGN_SHA",
  "source_sha": "$MERGE_SHA",
  "coordinator_written": true,
  "record_authorship": "written by the ORION-V2 coordinator, not by a human; the instruction quoted below is verbatim human input and the record of it is not",
  "verbatim_operator_instruction": "run all the computation tasks.. finish all the researxh asap",
  "operator_instruction_source": "human operator, chat, standing authorization of 2026-09-02",
  "scope": "LUNARC dispatch of the 480 E30-R13 responses and the registered evaluation and analysis chain",
  "authority_granted": "EXECUTION_ONLY",
  "grants_scientific_truth": false,
  "grants_field_status": false,
  "grants_publication_readiness": false,
  "recorded_utc": "$(date -u +%FT%TZ)"
}
AUTH
echo "AUTHORIZATION_WRITTEN design_sha256=$DESIGN_SHA"

export R13 R13_SOURCE_SHA="$MERGE_SHA" E30R13_PER_CALL_MAX_TOKENS E30R13_CHANNEL_CONTRACT
# --export=ALL, not a comma list: SLURM splits --export on commas, so a value that
# itself contains one is silently truncated.  (Measured here: a comma-separated arms
# list submitted that way reached the job as its first element only.)
X="ALL"
J_SETUP=$(sbatch --parsable --export="$X" "$SB/e30_r13_setup.sbatch")
J_AGENTS=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_SETUP" "$SB/e30_r13_agents.sbatch")
J_FROZEN=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_AGENTS" "$SB/e30_r13_frozen_lane_eval.sbatch")
J_GR0A=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_FROZEN" "$SB/e30_r13_fullreg_gr0a.sbatch")
J_GR0V=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_GR0A" "$SB/e30_r13_fullreg_gr0_verify.sbatch")
J_SUITE=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_GR0V" "$SB/e30_r13_fullreg_suite.sbatch")
J_ROLL=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_SUITE" "$SB/e30_r13_rollup_and_analysis.sbatch")

cat > "$R13/JOB_IDS.env" <<IDS
E30R13_CAMPAIGN=$R13
E30R13_SOURCE_SHA=$MERGE_SHA
E30R13_DESIGN_SHA256=$DESIGN_SHA
E30R13_CHANNEL_CONTRACT=$E30R13_CHANNEL_CONTRACT
E30R13_PER_CALL_MAX_TOKENS=$E30R13_PER_CALL_MAX_TOKENS
E30R13_SETUP=$J_SETUP
E30R13_AGENTS=$J_AGENTS
E30R13_FROZEN_LANE=$J_FROZEN
E30R13_FULLREG_GR0A=$J_GR0A
E30R13_GR0_VERIFY=$J_GR0V
E30R13_FULLREG_SUITE=$J_SUITE
E30R13_ROLLUP_ANALYSIS=$J_ROLL
IDS
cat "$R13/JOB_IDS.env"
