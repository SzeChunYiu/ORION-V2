#!/usr/bin/env bash
# E70-GC2 protected pipeline: preflight -> generate (frozen rung, fresh secret nonce)
# -> oracle-absent blinded dispatch -> count-robust evaluation -> analysis.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

WORKDIR="${ORION_GC2_WORKDIR:-$REPO_ROOT/.orion-generated-composition-gc2}"
ARMS="${ORION_GC2_ARMS:-SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL}"
MAX_CONCURRENCY="${ORION_GC2_MAX_CONCURRENCY:-3}"
DESIGN="${ORION_GC2_DESIGN:-research/experiments/e70-gc2/E70_GC2_OFFCEILING_DESIGN_V1.json}"
STAGE="${ORION_GC2_STAGE:-all}"   # all | generate | dispatch | evaluate | analyze

python -m py_compile \
  src/orion_v2/unified_diff_interface.py \
  scripts/orion_codex_arms.py \
  scripts/run_orion_generated_composition_suite.py \
  scripts/run_orion_generated_composition_gc2_suite.py \
  scripts/dispatch_orion_gc1_blinded.py

if [ "$STAGE" = "all" ] || [ "$STAGE" = "generate" ]; then
  python -m pytest -q \
    tests/unit/test_unified_diff_interface_wave6.py \
    tests/unit/test_generated_composition_gc2_suite.py
  # Task count, rung, reps and seed come from the frozen design; no overrides.
  python scripts/run_orion_generated_composition_gc2_suite.py generate \
    --design "$DESIGN" --workdir "$WORKDIR" --arms "$ARMS" --force
fi

if [ "$STAGE" = "all" ] || [ "$STAGE" = "dispatch" ]; then
  # Hidden-oracle bytes (incl. the nonce) are hashed, removed from disk before any
  # child/model process exists, and restored + hash-verified afterwards.
  python scripts/dispatch_orion_gc1_blinded.py \
    --workdir "$WORKDIR" --arms "$ARMS" --max-concurrency "$MAX_CONCURRENCY" \
    --runner-script scripts/run_orion_generated_composition_gc2_suite.py
fi

if [ "$STAGE" = "all" ] || [ "$STAGE" = "evaluate" ]; then
  python scripts/run_orion_generated_composition_gc2_suite.py evaluate \
    --design "$DESIGN" --workdir "$WORKDIR" --arms "$ARMS"
fi

if [ "$STAGE" = "all" ] || [ "$STAGE" = "analyze" ]; then
  python scripts/run_orion_generated_composition_gc2_suite.py analyze \
    --design "$DESIGN" --workdir "$WORKDIR" --arms "$ARMS"
  cat "$WORKDIR/EXECUTION_SUMMARY.md"
fi

echo "E70-GC2 stage '$STAGE' complete. Workdir: $WORKDIR. Secondary anti-copy/composition evidence only; cannot replace E30/E40/E50."
