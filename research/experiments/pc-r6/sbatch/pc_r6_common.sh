# Shared bindings for the PC-R6 SLURM lane (sourced by every pc_r6_*.sbatch).
# Frozen campaign trees are READ-ONLY; every write lands under $PCR6_OUT.
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R11="$E45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
E60="$E45/campaign-e60-r1-component-ablation-20260829-38aedc50"
PCR6_BASE=/projects/hep/fs9/users/scyiu/orion-v2-pc-r6
: "${PCR6_SRC:=/projects/hep/fs9/users/scyiu/orion-v2-wave6}"   # ORION-V2 clone at the merged PR sha
: "${PCR6_OUT:?set PCR6_OUT=<PCR6_BASE>/campaign-pc-r6-fullreg-e30r11-e60-<date>-<manifest8>}"
PY="$R11/run/venv/bin/python"                                      # same driver interpreter the frozen lane used (3.11.5)
RUNNER="$PCR6_SRC/research/experiments/pc-r6/pc_r6_fullreg_eval.py"
TRUTH="$PCR6_SRC/research/experiments/results/issue45"
ADAPTER="$R11/run/e30_r11_arm_eval_frozen_lane.py"                 # sha256 829abb41... asserted by the runner
COMMON=(--e30-campaign "$R11" --e60-campaign "$E60" --adapter "$ADAPTER" --out "$PCR6_OUT" --truth-dir "$TRUTH")
mkdir -p "$PCR6_BASE/logs" "$PCR6_OUT"
echo "PC-R6 job ${SLURM_JOB_ID:-local} array ${SLURM_ARRAY_TASK_ID:-n/a} host $(hostname) gcc=$(command -v gcc || true) python=$($PY --version 2>&1)"
echo "runner sha256 $(sha256sum "$RUNNER" | cut -c1-64)  adapter sha256 $(sha256sum "$ADAPTER" | cut -c1-64)"
