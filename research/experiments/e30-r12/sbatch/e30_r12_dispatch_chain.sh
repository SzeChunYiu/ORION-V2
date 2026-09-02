#!/usr/bin/env bash
# E30-R12 dispatch: write the coordinator authorization, then submit the whole chain.
#
# Run on the LUNARC login node AFTER the design PR merges:
#   bash e30_r12_dispatch_chain.sh <merge_sha> <design_sha256>
#
# Custody: the authorization file is written HERE, by the coordinator, and says so.
# The instruction it quotes is verbatim human chat input; the record of it is not
# human-written, and does not claim to be.  The dispatch gate in e30_r12_agents.sbatch
# refuses to run unless this file exists, quotes an attributed instruction, and
# acknowledges the exact design bytes -- so a design edited after authorization halts
# the study rather than silently running a different one.
set -euo pipefail
MERGE_SHA="${1:?usage: e30_r12_dispatch_chain.sh <merge_sha> <design_sha256>}"
DESIGN_SHA="${2:?usage: e30_r12_dispatch_chain.sh <merge_sha> <design_sha256>}"
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R12="${R12:-$E45/campaign-e30-r12-applyclean-core4-rep3-20260902-8940881d}"
SB="$R12/source/research/experiments/e30-r12/sbatch"
mkdir -p "$E45/logs-e30-r12"

git -C "$R12/source" fetch --quiet origin main
git -C "$R12/source" checkout --quiet --force "$MERGE_SHA"
HEAD_SHA=$(git -C "$R12/source" rev-parse HEAD)
[ "$HEAD_SHA" = "$MERGE_SHA" ] || { echo "SOURCE_CHECKOUT_FAILED $HEAD_SHA"; exit 2; }
GOT=$(sha256sum "$R12/source/research/experiments/e30-r12/E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json" | cut -c1-64)
[ "$GOT" = "$DESIGN_SHA" ] || { echo "DESIGN_SHA_MISMATCH got=$GOT want=$DESIGN_SHA"; exit 2; }

cat > "$R12/E30_R12_COORDINATOR_AUTHORIZATION.json" <<AUTH
{
  "schema_version": "orion.v2.e30-r12-coordinator-authorization.v1",
  "study_id": "E30-R12",
  "design": "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1",
  "acknowledged_design_sha256": "$DESIGN_SHA",
  "source_sha": "$MERGE_SHA",
  "coordinator_written": true,
  "record_authorship": "written by the ORION-V2 coordinator, not by a human; the instruction quoted below is verbatim human input and the record of it is not",
  "verbatim_operator_instruction": "run all the computation tasks.. finish all the researxh asap",
  "operator_instruction_source": "human operator, chat, standing authorization of 2026-09-02",
  "scope": "LUNARC dispatch of the 480 E30-R12 responses and the registered evaluation and analysis chain",
  "authority_granted": "EXECUTION_ONLY",
  "grants_scientific_truth": false,
  "grants_field_status": false,
  "grants_publication_readiness": false,
  "recorded_utc": "$(date -u +%FT%TZ)"
}
AUTH
echo "AUTHORIZATION_WRITTEN design_sha256=$DESIGN_SHA"

X="ALL,R12=$R12,R12_SOURCE_SHA=$MERGE_SHA"
J_SETUP=$(sbatch --parsable --export="$X" "$SB/e30_r12_setup.sbatch")
J_AGENTS=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_SETUP" "$SB/e30_r12_agents.sbatch")
J_FROZEN=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_AGENTS" "$SB/e30_r12_frozen_lane_eval.sbatch")
J_GR0A=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_FROZEN" "$SB/e30_r12_fullreg_gr0a.sbatch")
J_GR0V=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_GR0A" "$SB/e30_r12_fullreg_gr0_verify.sbatch")
J_SUITE=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_GR0V" "$SB/e30_r12_fullreg_suite.sbatch")
J_ROLL=$(sbatch --parsable --export="$X" --dependency=afterok:"$J_SUITE" "$SB/e30_r12_rollup_and_analysis.sbatch")

cat > "$R12/JOB_IDS.env" <<IDS
E30R12_CAMPAIGN=$R12
E30R12_SOURCE_SHA=$MERGE_SHA
E30R12_DESIGN_SHA256=$DESIGN_SHA
E30R12_SETUP=$J_SETUP
E30R12_AGENTS=$J_AGENTS
E30R12_FROZEN_LANE=$J_FROZEN
E30R12_FULLREG_GR0A=$J_GR0A
E30R12_GR0_VERIFY=$J_GR0V
E30R12_FULLREG_SUITE=$J_SUITE
E30R12_ROLLUP_ANALYSIS=$J_ROLL
IDS
cat "$R12/JOB_IDS.env"
