#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CAMPAIGN_ROOT="${1:-.orion-formal-discovery-campaign}"
MAX_CONCURRENCY="${ORION_FORMAL_MAX_CONCURRENCY:-2}"
STUDIES="${ORION_FORMAL_STUDIES:-}"

args=(
  all
  --campaign-root "$CAMPAIGN_ROOT"
  --max-concurrency "$MAX_CONCURRENCY"
)
if [[ -n "$STUDIES" ]]; then
  args+=(--studies "$STUDIES")
fi
if [[ "${ORION_FORMAL_FORCE:-0}" == "1" ]]; then
  args+=(--force)
fi
if [[ "${ORION_FORMAL_OVERWRITE:-0}" == "1" ]]; then
  args+=(--overwrite)
fi

python scripts/run_formal_discovery_campaign.py "${args[@]}"
