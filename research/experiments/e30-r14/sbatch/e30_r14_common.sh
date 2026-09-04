# Shared bindings for the E30-R14 SLURM lane (sourced by every e30_r14_*.sbatch).
# R11's campaign tree is READ-ONLY here; every write lands under $R14.
E45=/projects/hep/fs9/users/scyiu/orion-v2-e45
R11="$E45/campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6"
: "${R14:?set R14=$E45/campaign-e30-r14-channelcontract-core4-rep3-<date>-<sha8>}"
R14SRC="$R14/source"                       # ORION-V2 clone at the R14 anchor sha
PY="$R11/run/venv/bin/python"              # the driver interpreter the frozen lane used
# That venv carries an EDITABLE install of orion_v2 pointing at R11's PRE-#168 source, so
# without this the arms would import the very code the fix replaced while every compile
# and every py_compile still passed.  PYTHONPATH takes precedence over the editable
# finder (verified on the node); e30_r14_setup.sbatch asserts the resolved file path.
export PYTHONPATH="$R14SRC/src${PYTHONPATH:+:$PYTHONPATH}"
RUN="$R14/run"
ADAPTER="$RUN/e30_r11_arm_eval_frozen_lane.py"     # sha256 829abb41..., copied verbatim
RUNNER="$R14SRC/research/experiments/e30-r14/e30_r14_fullreg_eval.py"
ANALYSIS="$R14SRC/research/experiments/e30-r14/e30_r14_analysis.py"
R13ANALYSIS="$R14SRC/research/experiments/e30-r13/e30_r13_analysis.py"   # imported, sha-pinned
R12ANALYSIS="$R14SRC/research/experiments/e30-r12/e30_r12_analysis.py"   # imported, sha-pinned
# The registered request-body contract.  E30-R12 registered no such contract and
# inherited a provider default that then moved under it at an unchanged served model
# id; these two bindings are what make the condition, not just the model, registered.
CHANNEL_CONTRACT="${E30R14_CHANNEL_CONTRACT:-thinking_disabled}"
export ORION_ARM_CHANNEL_CONTRACT="$CHANNEL_CONTRACT"
# The registered arm<->workspace interface (E30-R14's own registration).  E30-R13 pinned the
# model and the request body and left the interface free; 346/480 diffs did not apply.
# No default: an interface that silently fell back to unified_diff/per_file_cap would run
# E30-R13 again under a new name.
EDIT_INTERFACE="${E30R14_EDIT_INTERFACE:?set E30R14_EDIT_INTERFACE to the registered edit interface}"
PRESENTATION_POLICY="${E30R14_PRESENTATION_POLICY:?set E30R14_PRESENTATION_POLICY to the registered presentation policy}"
export ORION_EDIT_INTERFACE="$EDIT_INTERFACE"
export ORION_PRESENTATION_POLICY="$PRESENTATION_POLICY"
ANALYZER="$R14SRC/scripts/analyze_orion_real_problem_results.py"
DESIGN="$R14SRC/research/experiments/e30-r14/E30_R14_INTERFACE_CONTRACT_RERUN_DESIGN_V1.json"
ARMS="SIMPLE_DIRECT SAME_MODEL_REFLECTION F0_PARENT_FEDERATION F2_ORION_METABOLIC_FULL"
LOGD="$E45/logs-e30-r14"
COMMON=(--e30r14-campaign "$R14" --adapter "$ADAPTER" --out "$R14/fullreg")
# Exported because the drivers embed python heredocs that read them from os.environ;
# a shell-local assignment here is invisible to those child processes.
export E45 R11 R14 R14SRC RUN ADAPTER RUNNER ANALYSIS R12ANALYSIS ANALYZER DESIGN LOGD PY
export CHANNEL_CONTRACT EDIT_INTERFACE PRESENTATION_POLICY R13ANALYSIS
mkdir -p "$LOGD" "$R14/fullreg" "$R14/infra"
echo "E30-R14 job ${SLURM_JOB_ID:-local} array ${SLURM_ARRAY_TASK_ID:-n/a} host $(hostname) python=$($PY --version 2>&1)"
