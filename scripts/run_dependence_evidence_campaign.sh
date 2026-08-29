#!/usr/bin/env bash
# P-D dependence-evidence generated campaign driver (design §9).
#
# Full run (needs a live codex backend; codex pinned 0.129.0-alpha.15):
#   ORION_CODEX_BIN=/path/to/codex bash scripts/run_dependence_evidence_campaign.sh all
#
# Offline smoke (deterministic arms only, zero model calls; model arms come
# back EXECUTION_FAILED -> the campaign must end CAMPAIGN INVALID, exit 3):
#   ORION_PD_OFFLINE_ONLY=1 bash scripts/run_dependence_evidence_campaign.sh all
#
# Sub-commands: prepare | dispatch | evaluate | analyze | status | all
# Extra flags pass through after the sub-command, e.g.
#   bash scripts/run_dependence_evidence_campaign.sh all --force
set -euo pipefail
cd "$(dirname "$0")/.."

command="${1:-all}"
shift || true

export ORION_PD_CAMPAIGN="${ORION_PD_CAMPAIGN:-.orion-dependence-evidence-campaign}"
exec python3 scripts/run_dependence_evidence_generated_suite.py "$command" \
  --campaign-root "$ORION_PD_CAMPAIGN" "$@"
