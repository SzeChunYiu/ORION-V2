#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r11-analysis
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e30r11-analysis-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e30r11-analysis-%j.err
set -euo pipefail
CAMP=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6
RUN="$CAMP/run"; SRC="$CAMP/source"; PY="$RUN/venv/bin/python"
MANIFEST=research/experiments/ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json
ARMS=SIMPLE_DIRECT,SAME_MODEL_REFLECTION,F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL
cd "$SRC"
date -u +"ANALYSIS_START %Y-%m-%dT%H:%M:%SZ"
for R in 1 2 3; do
  W="$RUN/confirmatory-r$R"
  echo "== validate rep$R"
  "$PY" scripts/validate_orion_agent_responses.py --manifest "$MANIFEST" --workdir "$W" --arms "$ARMS" > "$W/aggregate/response_validation_terminal480.json"
  echo "== summarize rep$R"
  "$PY" scripts/run_orion_real_problem_suite.py --manifest "$MANIFEST" --workdir "$W" summarize > "$W/aggregate/summary_terminal480.json"
done
echo "== analyze cross-rep (nested confirmatory-r1..r3)"
"$PY" scripts/analyze_orion_real_problem_results.py --workdir "$RUN" > "$CAMP/E30_R11_TERMINAL_ANALYSIS_480.json"
echo "== terminal raw rollup"
"$PY" "$RUN/e30_r11_terminal_raw_rollup.py"
date -u +"ANALYSIS_END %Y-%m-%dT%H:%M:%SZ"
