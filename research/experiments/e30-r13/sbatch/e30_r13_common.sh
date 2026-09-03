# Shared bindings for the E30-R13 SLURM lane (sourced by every e30_r13_*.sbatch).
# R11's campaign tree is READ-ONLY here; every write lands under $R13.
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R11="$E45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
: "${R13:?set R13=$E45/campaign-e30-r13-channelcontract-core4-rep3-<date>-<sha8>}"
R13SRC="$R13/source"                       # ORION-V2 clone at the R13 anchor sha
PY="$R11/run/venv/bin/python"              # the driver interpreter the frozen lane used
# That venv carries an EDITABLE install of orion_v2 pointing at R11's PRE-#168 source, so
# without this the arms would import the very code the fix replaced while every compile
# and every py_compile still passed.  PYTHONPATH takes precedence over the editable
# finder (verified on the node); e30_r13_setup.sbatch asserts the resolved file path.
export PYTHONPATH="$R13SRC/src${PYTHONPATH:+:$PYTHONPATH}"
RUN="$R13/run"
ADAPTER="$RUN/e30_r11_arm_eval_frozen_lane.py"     # sha256 829abb41..., copied verbatim
RUNNER="$R13SRC/research/experiments/e30-r13/e30_r13_fullreg_eval.py"
ANALYSIS="$R13SRC/research/experiments/e30-r13/e30_r13_analysis.py"
R12ANALYSIS="$R13SRC/research/experiments/e30-r12/e30_r12_analysis.py"   # imported, sha-pinned
# The registered request-body contract.  E30-R12 registered no such contract and
# inherited a provider default that then moved under it at an unchanged served model
# id; these two bindings are what make the condition, not just the model, registered.
CHANNEL_CONTRACT="${E30R13_CHANNEL_CONTRACT:-thinking_disabled}"
export ORION_ARM_CHANNEL_CONTRACT="$CHANNEL_CONTRACT"
ANALYZER="$R13SRC/scripts/analyze_orion_real_problem_results.py"
DESIGN="$R13SRC/research/experiments/e30-r13/E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json"
ARMS="SIMPLE_DIRECT SAME_MODEL_REFLECTION F0_PARENT_FEDERATION F2_ORION_METABOLIC_FULL"
LOGD="$E45/logs-e30-r13"
COMMON=(--e30r13-campaign "$R13" --adapter "$ADAPTER" --out "$R13/fullreg")
# Exported because the drivers embed python heredocs that read them from os.environ;
# a shell-local assignment here is invisible to those child processes.
export E45 R11 R13 R13SRC RUN ADAPTER RUNNER ANALYSIS R12ANALYSIS ANALYZER DESIGN LOGD PY
export CHANNEL_CONTRACT
mkdir -p "$LOGD" "$R13/fullreg" "$R13/infra"
echo "E30-R13 job ${SLURM_JOB_ID:-local} array ${SLURM_ARRAY_TASK_ID:-n/a} host $(hostname) python=$($PY --version 2>&1)"
