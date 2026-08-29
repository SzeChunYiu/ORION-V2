# E60 launch-readiness receipt + taskmap path fix (V1, 2026-08-29)

**Scope:** engineering-only launch readiness for deferred SLURM array 3553083
(`e60_agents_minus480.sbatch`, `--array=0-47%2`, `--begin` gated behind
`afterany:3552883`). No frozen input was modified.

## Defect found

The sbatch mapfile step reads the taskmap from `$RUN/e60-taskmap-minus480.json`
(`RUN=$CAMP/run`), but the frozen taskmap lives at the campaign root
(`campaign-e60-ablation-minus4-rep3-20260829/e60-taskmap-minus480.json`). Process-substitution
failure is not caught by `set -euo pipefail`: every element would have completed as a
silent no-op (`SHARD n DONE items=0`) with zero responses generated.

## Fix

Byte-identical copy `e60-taskmap-minus480.json` -> `run/e60-taskmap-minus480.json`
(`cp -p`). Both files sha256 `621ea8a7b15893b25e74d88c8573721e9152ce985f2ad69061317fa0f0df664a`,
matching `inputs_frozen.taskmap_sha256_prefix = 621ea8a7b15893b2` in
`E60_MODEL_CALL_GATE.json`. Original untouched; gate pins remain valid.

## Launch-readiness verification (pre-dependency)

- taskmap: 480 entries; arms = {F2_MINUS_COUNTERPROBE, F2_MINUS_DECOMPOSITION,
  F2_MINUS_NATIVE_RECOVERY, F2_MINUS_SELECTIVE_REOPEN}; repeats = {1,2,3}
- requests present: 480/480, missing 0; responses present: 0 (clean, no partial state)
- shard-0 mapfile simulation (venv python, exact sbatch logic): 10 items, first =
  {arm: F2_MINUS_DECOMPOSITION, repeat: 1, task: bugsinpy-ansible-1}
- RUN_IDENTITY.json: run_id campaign-e60-ablation-minus4-rep3-20260829,
  orion_source_sha ffcc8ed613a6e75ce4ae530f1d25be21bd25dd3b, phase
  E60_COMPONENT_ABLATION_MINUS4_ARMS_PROSPECTIVE, model_calls_authorized true
- E60_MODEL_CALL_GATE.json: state OPEN_INPUTS_FROZEN_MODEL_CALLS_QUEUED_AFTER_PARENT
- credentials: ~/.orion-campaign.env present (600), defines ANTHROPIC_AUTH_TOKEN /
  ANTHROPIC_BASE_URL / ANTHROPIC_MODEL; proven live by the running E30 array on the
  same env file.

E60_TASKMAP_PATH_DEFECT = FIXED_SILENT_NOOP_PREVENTED
E60_LAUNCH_READINESS = VERIFIED_PENDING_DEPENDENCY_3552883
