#!/usr/bin/env bash
# E30-R14 dispatch: write the coordinator authorization, then submit the whole chain.
#
# Run on the LUNARC login node AFTER the design PR merges:
#   bash e30_r14_dispatch_chain.sh <merge_sha> <design_sha256>
#
# Custody: the authorization file is written HERE, by the coordinator, and says so.
# The instruction it quotes is verbatim human chat input; the record of it is not
# human-written, and does not claim to be.  The dispatch gate in e30_r14_agents.sbatch
# refuses to run unless this file exists, quotes an attributed instruction, and
# acknowledges the exact design bytes -- so a design edited after authorization halts
# the study rather than silently running a different one.
set -euo pipefail
MERGE_SHA="${1:?usage: e30_r14_dispatch_chain.sh <merge_sha> <design_sha256>}"
DESIGN_SHA="${2:?usage: e30_r14_dispatch_chain.sh <merge_sha> <design_sha256>}"
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R14="${R14:?set R14=$E45/campaign-e30-r14-channelcontract-core4-rep3-<date>-<sha8>}"
# The per-call output-token cap, derived in E30_R14_BUDGET_NOTE_V1.json and registered in
# the design.  No default: a cap that silently falls back to a historical number is how
# E30-R12 inherited two budgets that were both inadequate.
: "${E30R14_PER_CALL_MAX_TOKENS:?set E30R14_PER_CALL_MAX_TOKENS to the registered per-call cap}"
E30R14_CHANNEL_CONTRACT="${E30R14_CHANNEL_CONTRACT:-thinking_disabled}"
: "${E30R14_EDIT_INTERFACE:?set E30R14_EDIT_INTERFACE to the registered edit interface}"
: "${E30R14_PRESENTATION_POLICY:?set E30R14_PRESENTATION_POLICY to the registered presentation policy}"
SB="$R14/source/research/experiments/e30-r14/sbatch"
mkdir -p "$E45/logs-e30-r14"

git -C "$R14/source" fetch --quiet origin main
git -C "$R14/source" checkout --quiet --force "$MERGE_SHA"
HEAD_SHA=$(git -C "$R14/source" rev-parse HEAD)
[ "$HEAD_SHA" = "$MERGE_SHA" ] || { echo "SOURCE_CHECKOUT_FAILED $HEAD_SHA"; exit 2; }
GOT=$(sha256sum "$R14/source/research/experiments/e30-r14/E30_R14_INTERFACE_CONTRACT_RERUN_DESIGN_V1.json" | cut -c1-64)
[ "$GOT" = "$DESIGN_SHA" ] || { echo "DESIGN_SHA_MISMATCH got=$GOT want=$DESIGN_SHA"; exit 2; }

cat > "$R14/PROTECTED_RUN_AUTHORIZATION.json" <<AUTH
{
  "schema_version": "orion.v2.e30-r14-coordinator-authorization.v1",
  "study_id": "E30-R14",
  "design": "E30_R14_INTERFACE_CONTRACT_RERUN_DESIGN_V1",
  "acknowledged_design_sha256": "$DESIGN_SHA",
  "source_sha": "$MERGE_SHA",
  "coordinator_written": true,
  "record_authorship": "written by the ORION-V2 coordinator, not by a human; the instruction quoted below is verbatim human input and the record of it is not",
  "verbatim_operator_instruction": "run all the computation tasks.. finish all the researxh asap",
  "operator_instruction_source": "human operator, chat, standing authorization of 2026-09-02",
  "scope": "LUNARC dispatch of the 480 E30-R14 responses and the registered evaluation and analysis chain",
  "authority_granted": "EXECUTION_ONLY",
  "grants_scientific_truth": false,
  "grants_field_status": false,
  "grants_publication_readiness": false,
  "recorded_utc": "$(date -u +%FT%TZ)"
}
AUTH
echo "AUTHORIZATION_WRITTEN design_sha256=$DESIGN_SHA"

export R14 R14_SOURCE_SHA="$MERGE_SHA" E30R14_PER_CALL_MAX_TOKENS E30R14_CHANNEL_CONTRACT E30R14_EDIT_INTERFACE E30R14_PRESENTATION_POLICY
# --export=ALL, not a comma list: SLURM splits --export on commas, so a value that
# itself contains one is silently truncated.  (Measured here: a comma-separated arms
# list submitted that way reached the job as its first element only.)
X="ALL"
J_SETUP=$(sbatch --parsable --export="$X" "$SB/e30_r14_setup.sbatch")
J_AGENTS=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_SETUP" "$SB/e30_r14_agents.sbatch")
J_FROZEN=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_AGENTS" "$SB/e30_r14_frozen_lane_eval.sbatch")
J_GR0A=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_FROZEN" "$SB/e30_r14_fullreg_gr0a.sbatch")
J_GR0V=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_GR0A" "$SB/e30_r14_fullreg_gr0_verify.sbatch")
J_SUITE=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_GR0V" "$SB/e30_r14_fullreg_suite.sbatch")
J_ROLL=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_SUITE" "$SB/e30_r14_rollup_and_analysis.sbatch")

cat > "$R14/JOB_IDS.env" <<IDS
E30R14_CAMPAIGN=$R14
E30R14_SOURCE_SHA=$MERGE_SHA
E30R14_DESIGN_SHA256=$DESIGN_SHA
E30R14_CHANNEL_CONTRACT=$E30R14_CHANNEL_CONTRACT
E30R14_EDIT_INTERFACE=$E30R14_EDIT_INTERFACE
E30R14_PRESENTATION_POLICY=$E30R14_PRESENTATION_POLICY
E30R14_PER_CALL_MAX_TOKENS=$E30R14_PER_CALL_MAX_TOKENS
E30R14_SETUP=$J_SETUP
E30R14_AGENTS=$J_AGENTS
E30R14_FROZEN_LANE=$J_FROZEN
E30R14_FULLREG_GR0A=$J_GR0A
E30R14_GR0_VERIFY=$J_GR0V
E30R14_FULLREG_SUITE=$J_SUITE
E30R14_ROLLUP_ANALYSIS=$J_ROLL
IDS
cat "$R14/JOB_IDS.env"
