# Shared bindings for the E30-R12 SLURM lane (sourced by every e30_r12_*.sbatch).
# R11's campaign tree is READ-ONLY here; every write lands under $R12.
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R11="$E45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
: "${R12:?set R12=$E45/campaign-e30-r12-applyclean-core4-rep3-<date>-<sha8>}"
R12SRC="$R12/source"                       # ORION-V2 clone at the R12 anchor sha
PY="$R11/run/venv/bin/python"              # the driver interpreter the frozen lane used
# That venv carries an EDITABLE install of orion_v2 pointing at R11's PRE-#168 source, so
# without this the arms would import the very code the fix replaced while every compile
# and every py_compile still passed.  PYTHONPATH takes precedence over the editable
# finder (verified on the node); e30_r12_setup.sbatch asserts the resolved file path.
export PYTHONPATH="$R12SRC/src${PYTHONPATH:+:$PYTHONPATH}"
RUN="$R12/run"
ADAPTER="$RUN/e30_r11_arm_eval_frozen_lane.py"     # sha256 829abb41..., copied verbatim
RUNNER="$R12SRC/research/experiments/e30-r12/e30_r12_fullreg_eval.py"
ANALYSIS="$R12SRC/research/experiments/e30-r12/e30_r12_analysis.py"
ANALYZER="$R12SRC/scripts/analyze_orion_real_problem_results.py"
DESIGN="$R12SRC/research/experiments/e30-r12/E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json"
ARMS="SIMPLE_DIRECT SAME_MODEL_REFLECTION F0_PARENT_FEDERATION F2_ORION_METABOLIC_FULL"
LOGD="$E45/logs-e30-r12"
COMMON=(--e30r12-campaign "$R12" --adapter "$ADAPTER" --out "$R12/fullreg")
mkdir -p "$LOGD" "$R12/fullreg" "$R12/infra"
echo "E30-R12 job ${SLURM_JOB_ID:-local} array ${SLURM_ARRAY_TASK_ID:-n/a} host $(hostname) python=$($PY --version 2>&1)"
