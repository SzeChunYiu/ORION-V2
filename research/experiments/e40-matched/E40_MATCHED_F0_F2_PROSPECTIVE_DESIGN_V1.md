# E40-M1 Matched F0/F2 Around the Native Causal Learner — Prospective Design V1

**Lane:** E40 T3a CausalBench cross-domain execution (owner issue #45)
**Frozen:** 2026-08-30 (before any dispatch)
**done_when addressed:** "F0 and F2 share native causal algorithms/data and held-out/permuted
variants are independently scored" — this design makes F0 and F2 share the pinned native
learner, data, and invocation budget; held-out scoring is the untouched upstream
quantitative test split; permutation nulls and the independent adjudicator are bound below.

## 1. Scientific question

Does the ORION metabolic loop (F2) improve orchestration of a **native causal learner**
over the parent federation (F0) and a naive single config (SIMPLE), at **matched native
compute** (same number of native invocations, same pinned code and data)? The treatment
is information: F2 chooses configs sequentially **with** interim feedback; F0 commits all
configs **without** feedback; SIMPLE runs the default once.

## 2. Frozen substrate (exists, verified this session)

- CausalBench at commit `1a2143cffdc85f835b41ce8d52034be1bf903e71`
  (`campaign-e40-r3/causalbench`, invocation `python -m causalscbench.apps.main_app`).
- Datasets `weissmann_k562`, `weissmann_rpe1` with sha256s in
  `research/experiments/results/issue45/e40/RUN_IDENTITY.json`; `--do_filter`,
  `--subset_data 0.05`, `--max_path_length -1` fixed as in E40 R1–R3.
- Upstream scorer per run (`results/<exp_id>/metrics.json`):
  `quantitative_test_evaluation.output_graph` = **held-out final score** (mean Wasserstein
  distance, TP, FP); `corum_evaluation`, `string_network_evaluation`,
  `string_physical_evaluation`, `ligand_receptor_evaluation`, `false_omission_rate` =
  external-knowledge/diagnostic channel.
- Orchestratable knobs (the complete CLI surface): `training_regime`
  {Observational, PartialInterventional, ...}, `fraction_partial_intervention`,
  `partial_intervention_seed`, `model_seed`, `subset_data`, `max_path_length`,
  `omission_estimation_size`. Model fixed to `pc` (E40 native learner).

## 3. Arms (matched)

| Arm | Protocol | Native invocations per chain |
|---|---|---|
| SIMPLE_DIRECT_CONTROL | one run, default config (E40 R1 flags verbatim) | 1 |
| F0_PARENT_FEDERATION_MATCHED | parent-federation protocol proposes **all K=4 configs upfront**, no feedback | 4 |
| F2_ORION_METABOLIC_FULL_MATCHED | metabolic loop proposes config k after seeing cycles 1..k-1 feedback | 4 |

Chains: 2 datasets × R=6 `model_seed` reps = **12 chains per arm**; SIMPLE reuses its run
across the K budget by re-running with the 6 seeds (compute floor, not matched-ceiling).
Native runs per arm: F0/F2 = 4×12 = 48; SIMPLE = 12. Total ≈ 108 runs.

## 4. Leakage rule (binding)

Feedback to F2 between cycles = the run's `metrics.json` **with
`quantitative_test_evaluation` redacted** (external-knowledge evals + omission stats +
arguments only). Neither arm ever sees any held-out quantitative-test number before its
configs are final. Final scoring reads `quantitative_test_evaluation.output_graph` once,
after all configs are frozen. SIMPLE sees nothing (default).

## 5. Independent adjudicator binding

Scoring is performed by the **upstream CausalBench scorer at the pinned commit** — code
not authored in this programme, ground truth bundled with the benchmark, identical for all
arms. `independent_native_domain_adjudicator` := pinned-commit upstream scorer + frozen
rollup script (`E40_MATCHED_ROLLUP_V1`, to be committed before dispatch with its sha256
in the dispatch receipt).

## 6. Pre-registered analysis

- **Primary:** mean held-out Wasserstein distance (`output_graph`), lower = better.
  Conservative comparison **F2_final vs F0_max** (F0's best-of-4, since F0 has no order);
  secondary: both-max and both-final.
- **Secondary:** TP, FP, `false_omission_rate`, CORUM/STRING TPs.
- **Null:** arm-label permutation over the 12 chain-level paired statistics
  (2 datasets × 6 seeds), one-sided, 5000 perms; report exact p.
- **Positive control (checker validation, mandatory before verdict):** a planted-feedback
  replay where cycle feedback is synthesized so the best test config is identifiable from
  the feedback channel alone — the F2 harness must recover ≥3/4 of the planted optimum
  sequence, else `CHECKER_INVALID__NO_VERDICT`.
- **No-fabrication control:** arms given identical (uninformative) feedback must show no
  F2 advantage beyond chance in replay.

## 7. Gates / terminal vocabulary

- `F2_METABOLIC_ADVANTAGE_MATCHED_NATIVE`: F2_final < F0_max on primary across the pooled
  chains, permutation p<0.05, AND no per-dataset collapse (F2_final median TP ≥ SIMPLE's).
- `NO_DETECTED_ADVANTAGE_MATCHED_NATIVE`: direction holds, p≥0.05 (negative retained).
- `METABOLIC_DRAG_MATCHED_NATIVE`: F2_final ≥ F0_max (negative; feeds component
  attribution alongside E60).
- Any infrastructure failure → `CANNOT_CHECK` for the affected cells only; no silent fill.

## 8. Boundary inheritance

Success-resource claims about generated causal-discovery orchestration only. No biological
claim about K562/RPE1 perturbation networks, no field-status, no cross-domain transfer
license (that is E40 T3b/FM80 territory), authority block false in all machine outputs.

## 9. Execution plan (after this freeze PR)

Runner: `e40_matched_runner.py` (config-prompt builder + native run driver + redacting
feedback channel + rollup), dispatch via LUNARC sbatch array (native runs) + the codex
lane (arm decisions, 0.150.1 musl, same channel as E60). One chain = sequential K runs;
chains parallel across the array. Dispatch receipt (with runner sha256 + config freeze)
before outcomes are read; terminal receipt with gates and controls after evaluate.

skills-applied: none (prospective design, no manuscript content)
