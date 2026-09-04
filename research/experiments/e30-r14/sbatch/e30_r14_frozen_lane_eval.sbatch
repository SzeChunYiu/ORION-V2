#!/usr/bin/env bash
#SBATCH --job-name=o2-e30r14-frozenlane
#SBATCH --account=lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --cpus-per-task=24
#SBATCH --mem=96G
#SBATCH --time=12:00:00
#SBATCH --output=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/frozenlane-%j.out
#SBATCH --error=/projects/hep/fs9/users/scyiu/orion-v2-e45/logs-e30-r14/frozenlane-%j.err
# Frozen-lane evaluation of the 480 R13 proposals (registered failing test only).
# This produces the vector GR0a checks the full-regression lane against: two
# independent evaluators over the same proposals must agree bit-exactly.
set -euo pipefail
# SLURM copies the batch script into its per-job spool directory, so `dirname "$0"` is
# /var/spool/slurm/... and not this file's location in the source tree. Resolve the
# shared bindings from $R14 (exported by the submitting environment) instead.
: "${R14:?set R14=<campaign dir> in the submitting environment (sbatch --export)}"
SBATCH_DIR="${E30R14_SBATCH_DIR:-$R14/source/research/experiments/e30-r14/sbatch}"
source "$SBATCH_DIR/e30_r14_common.sh"
LOGI="$LOGD/frozenlane-items"; mkdir -p "$LOGI"
R14="$R14" "$PY" - > "$RUN/e30r14-eval-pending.tsv" <<'PY'
import json, os, sys
from pathlib import Path
run = Path(os.environ["R13"]) / "run"
items = json.loads((run / "e30-taskmap-core480.json").read_text())
pending = done = 0
for x in items:
    ev = run / f"confirmatory-r{x['repeat']}/evaluations/{x['arm']}/{x['task']}.json"
    if ev.is_file():
        try:
            if "evaluation_lane" in json.loads(ev.read_text()):
                done += 1; continue
        except Exception:
            pass
    print(x["repeat"], x["arm"], x["task"], sep="\t"); pending += 1
print(f"already_done={done} pending={pending}", file=sys.stderr)
PY
WORKER=$(mktemp /tmp/e30r14eval.XXXXXX.sh)
cat > "$WORKER" <<W
#!/usr/bin/env bash
set -euo pipefail
REP="\$1"; ARM="\$2"; TASK="\$3"
{ date -u +"START %FT%TZ \$REP \$ARM \$TASK"
  "$PY" "$ADAPTER" --campaign "$R14" --workdir "$RUN/confirmatory-r\$REP" \
    --arms "\$ARM" --tasks "\$TASK" --timeout-seconds 10800
  date -u +"END %FT%TZ \$REP \$ARM \$TASK"; } > "$LOGI/r\${REP}-\${ARM}-\${TASK}.log" 2>&1
W
chmod +x "$WORKER"
[ -s "$RUN/e30r14-eval-pending.tsv" ] && xargs -P 6 -n 3 "$WORKER" < "$RUN/e30r14-eval-pending.tsv"
rm -f "$WORKER"
R14="$R14" "$PY" - <<'PY'
import json, os, sys
from pathlib import Path
run = Path(os.environ["R13"]) / "run"
items = json.loads((run / "e30-taskmap-core480.json").read_text())
missing = [x for x in items
           if not (run / f"confirmatory-r{x['repeat']}/evaluations/{x['arm']}/{x['task']}.json").is_file()]
print("missing:", len(missing), [f"r{x['repeat']}/{x['arm']}/{x['task']}" for x in missing[:10]])
sys.exit(0 if not missing else 3)
PY
echo "FROZEN_LANE_COMPLETE_480 $(date -u +%FT%TZ)"
