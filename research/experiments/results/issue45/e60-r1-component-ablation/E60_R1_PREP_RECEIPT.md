# E60 R1 component-ablation campaign — prep + submission receipt (2026-08-29)

## What was staged

Fresh same-epoch **paired** component-ablation campaign on the frozen real-problem
confirmatory suite (`orion-v2-real-problem-confirmatory-2026-08-28`), LUNARC root
`/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e60-r1-component-ablation-20260829-38aedc50/`
(manifest8 `38aedc50`). Supersedes the earlier unpaired
`campaign-e60-ablation-minus4-rep3-20260829` (478/480 responses; left untouched).

- **Design**: `F2_ORION_METABOLIC_FULL` + 4 ablations (`F2_MINUS_DECOMPOSITION`,
  `F2_MINUS_NATIVE_RECOVERY`, `F2_MINUS_COUNTERPROBE`, `F2_MINUS_SELECTIVE_REOPEN`) ×
  the same 40 frozen BugsinPy tasks × 3 confirmatory reps = **600 items** (200/rep).
- **SELECTIVE_REOPEN ablation** is declared via `removed_components` (behavioural), the
  manifest's real contract key; no `full_stages` key exists.
- **R11 reuse is read-only**: `source/`, `evaluator_private/`, `SETUP_RECEIPT.json` are
  `cp -al` hardlinks; every E60 write lands under the E60 root.

## Jobs (submitted 2026-08-29, verified PENDING on their dependencies)

| Job | ID | Dependency |
|---|---|---|
| Agent array, 24 shards `%2` (probe-confirm → dispatch) | **3554050** | `afterok:3553440` (E30 R11) |
| Redispatch/terminal chain (probe → guarded retry → completeness gate → eval+analysis) | **3554051** | `afterany:3554050` |
| Eval 600 (frozen-lane driver, 6 workers, resumable) + analysis (`component_effects.json`) | chained inside 3554051 | fires only on 600/600 `COMPLETED_PROPOSAL_ONLY`, else exit 3 |

sbatch: `E45/e60_agents_r1.sbatch`, `e60_redispatch_terminal_r1.sbatch`,
`e60_eval_r1_core600_single.sbatch`, `e60_analysis_r1_terminal.sbatch`; logs `E45/logs-e60-r1/`.

## Validations (all PASS; details in PREP_RECEIPT.json)

1. **Requests** — 600/600 parse; arm/task/schema/suite-id correct; gold-blind
   (`gold_or_outcome_data_included=false`, ceiling `PROPOSAL_ONLY`, per-task
   `gold_withheld:true`); leak scan over string values = 0 hits (null-case control fires);
   all 5 arm contracts exact across reps.
2. **Construction identity** — 40/40 rep-1 `F2_ORION_METABOLIC_FULL` requests byte-identical
   to R11's (frozen builder reproduces R11 construction).
3. **Scripts + slicing** — `bash -n` clean ×4; strided shards 24×25=600 (max 25 ≤ 30);
   all 600 entries have request files; uniqueness 600.
4. **Submission** — squeue confirms both jobs PENDING as designed.
5. **R11 mutation check** (marker `.e60_marker_1788037481`) — 34 newer files, all under
   R11 `responses/` (its own live job); frozen surface zero mutations.

## Status

PROSPECTIVE — no responses, no evaluation, no results yet. Nothing here grants scientific
truth, field status or publication readiness (`requested_authority_ceiling=PROPOSAL_ONLY`).
