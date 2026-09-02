# H-EXT-1 Design V1 — Conditional Activation with Channel-External Witnesses

**Status:** `FROZEN_PROSPECTIVE_DESIGN_NO_GATED_RESULTS` (frozen 2026-09-02, before any
gated evaluation). Machine-readable twin: `H_EXT1_CONDITIONAL_ACTIVATION_DESIGN_V1.json`
(its sha256 is recorded in `H_EXT1_GATE_FREEZE.json` at gate freeze). Register row:
`research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md` §H-EXT-1.
Reconnaissance: `H_EXT1_RECONNAISSANCE_RECEIPT.md`. Runner: `scripts/h_ext1_gate_study.py`.

## 1. Claim under test

On the P-D generated suite the dependence machinery is decisive where dependence is
present (PD-S1 A/C: `P_D_FULL` ≈ 1.000 vs `P_D_MINUS_DEPENDENCE` 0.000) and a drag where it
is absent (PD-S2-D 0.933, PD-S4-B 0.767 vs 1.000). H-EXT-1 asks whether a **cheap,
input-computable gate** — a function of the evidence records exactly as the arms see them,
never the oracle stratum, never any arm's output — can activate the machinery only where
it helps, so that `GATED_M` Pareto-dominates always-on `M` and always-off `OFF` on the
quality–cost frontier, and also matches the strongest parent.

## 2. Arms and cells

| Role | Arm | Notes |
|---|---|---|
| `M` (always-on) | `P_D_FULL` | model arm, 1 codex call per task |
| `OFF` (always-off) | `P_D_MINUS_DEPENDENCE` | same substrate, dependence modelling removed |
| `PARENT` (reference) | `STRONGEST_ASSURANCE_FEDERATION` | strongest parent emulation |
| `GATED_M` | `M(x)` if `gate(x)` else `OFF(x)` | correctness/cost taken from the routed arm's row for the same task |

| Cell | Instances | Substrate | Role |
|---|---|---|---|
| `RETROSPECTIVE_DEV` | frozen 520 with `sha256(task_id)[0]` even (~260) | gpt-5.6-terra, seed 20260903 | gate selection only |
| `RETROSPECTIVE_EVAL` | frozen 520 with first byte odd (~260) | same | secondary evaluation, labelled |
| `PROSPECTIVE` | fresh seed **20260902**, 520 new tasks | **gpt-5.5** (pinned codex rejects gpt-5.6-terra: HTTP 400 on 2026-09-02) | **binding** evaluation |

The prospective cell is a new evaluation identity on both axes (seed and model). A gate
selected on terra-substrate outcomes and evaluated on gpt-5.5 outcomes is a transfer test;
the design accepts that as the stronger reading.

## 3. Gate input and validity (G0)

The gate receives a deep copy of the public task object (`requests/<arm>/<id>.json['task']`)
with every key in `{strata, stratum, answers, expected, answer, correct, actual,
private_oracle, oracle}` removed at all nesting levels. A canary assertion re-runs the gate on
a copy with forbidden keys injected and aborts if any output changes. Evidence records are
every dict carrying both `lineage_root` and `replay_hash`, wherever they sit in the task
(`items`, `evidence`, `evidence_items`); tasks with no records have all witnesses false.
`study_id` is arm-visible but **excluded from the candidate family** (a metadata gate is
reported only as a diagnostic reference).

## 4. Witness features and candidate family (frozen)

Features: `w_dup_hash` (two records share a `replay_hash`), `w_shared_root` (share a
`lineage_root`), `w_declared_overlap`, `w_xref_root` (a record's `method_text` contains
another record's `lineage_root`), `w_shared_token` (an uppercase token `[A-Z][A-Z0-9-]{3,}`
occurs in ≥2 records' `method_text`), `n_records`, `n_roots`, `root_ratio`.

| gate_id | activate iff |
|---|---|
| `G_A_PROVENANCE_WITNESS` | `w_dup_hash ∨ w_shared_root` |
| `G_B_PLUS_XREF` | `G_A ∨ w_xref_root` |
| `G_C_PLUS_DECLARED` | `G_B ∨ w_declared_overlap` |
| `G_D_PLUS_SHARED_TOKEN` | `G_C ∨ w_shared_token` |
| `G_E_COUNT_GE4` | `n_records ≥ 4` |
| `G_F_ROOT_RATIO_GT1` | `root_ratio > 1` |

Reference gates (never selectable): `ALWAYS_ON` (= M), `ALWAYS_OFF` (= OFF),
`STUDY_ID_IS_PDS1` (diagnostic), `ORACLE_STRATUM` (activates on PDS1A/PDS1C from the private
oracle; a ceiling, computed only in evaluation reporting).

## 5. Selection rule (development phase)

On `RETROSPECTIVE_DEV` only: `dev_advantage = acc(GATED_M) − max(acc(M), acc(OFF))`
pooled; choose the argmax over the family, ties → lower activation rate → family order.
If no candidate has `dev_advantage > 0`: terminal `NO_CANDIDATE_GATE_ON_DEV`, nothing else is
scored. The selected gate, feature definitions and design sha256 are written to
`H_EXT1_GATE_FREEZE.json` before any evaluation cell is scored.

## 6. Metrics, null, gates

Primary metric: exact-decision accuracy (`EVALUATION_ROWS.correct`), paired per instance.
Cost: model calls per instance (primary; every arm is exactly 1) and mean
`wall_time_seconds` of the routed arm (secondary).

`NULL_POOLED`: 2000 random gates (seed 20260902) activating exactly the selected gate's
number of instances, drawn uniformly from the cell. `NULL_WITHIN_STUDY`: 2000 random gates
matching the selected gate's activation count inside each study (removes the "which study"
information; a gate that only knows the study cannot beat it).

| Gate | Pass condition |
|---|---|
| G0 | dev/eval task-id sets disjoint; prospective seed ≠ 20260903; canary passes on every task; all arms `run_valid` in the scored cell |
| G1 | `acc(GATED_M) ≥ acc(M)` and `calls(GATED_M) ≤ calls(M)` and `mean_wall(GATED_M) ≤ 1.05·mean_wall(M)` |
| G2 | `acc(GATED_M) > acc(OFF)` and `acc(GATED_M) ≥ acc(PARENT)` |
| G3 | advantage `acc(GATED_M) − max(acc(M), acc(OFF))` > 95th percentile of `NULL_POOLED` |
| G3S | same advantage > 95th percentile of `NULL_WITHIN_STUDY` |
| G4 | in every study, `acc_s(GATED_M) ≥ max(acc_s(M), acc_s(OFF))` (ties allowed) |

## 7. Pre-registered routing (precedence top-down)

| Condition | Terminal |
|---|---|
| prospective run has missing/failed responses | `CANNOT_CHECK_PROSPECTIVE_RUN_INVALID` (not a negative) |
| G0 fails | `DESIGN_VIOLATION_RUN_VOID` |
| G1 fails | `GATING_DOES_NOT_DOMINATE_ALWAYS_ON` |
| G2 fails vs OFF | `GATING_DOES_NOT_DOMINATE_ALWAYS_OFF` |
| G2 fails vs PARENT | `STRONGEST_PARENT_SUFFICIENT_UNDER_GATING` |
| G3 fails | `ACTIVATION_POLICY_NOT_IDENTIFIABLE_FROM_INPUTS` |
| G4 fails | `ACTIVATION_ADVANTAGE_NOT_SIGN_CONSISTENT` |
| G3 passes, G3S fails | `ACTIVATION_POLICY_IDENTIFIABLE_ONLY_AT_STUDY_GRANULARITY` |
| all pass | `CONDITIONAL_ACTIVATION_IDENTIFIABLE_FROM_EVIDENCE_STRUCTURE` |

The `PROSPECTIVE` cell is binding. `RETROSPECTIVE_EVAL` is reported alongside, labelled;
disagreement is reported and does not rescue the prospective verdict.

## 8. No-rescue clause

After the gate freeze: no re-selection, threshold change, feature edit, instance or study
exclusion, null redefinition, or arm substitution. A failed gate is recorded under its
routed terminal. Any repair is a new identity (V2) with its own freeze.

## 9. Honest limits (frozen before results)

- The suite plants dependence by construction; witnesses that separate its strata need not
  separate real corpora. A positive here is a **suite-internal identifiability** result.
- The prospective substrate (gpt-5.5) differs from the frozen one (gpt-5.6-terra); the
  prospective cell is internally paired (all three arms on the same substrate) but its
  absolute accuracies are not comparable to PD R1's.
- The candidate family is small and enumerated; a negative says these six evidence-structure
  witnesses do not identify the regime, not that no input-computable gate exists.

```text
H_EXT1_DESIGN = FROZEN_PROSPECTIVE_NO_GATED_RESULTS
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_FIELD_STATUS = false
GRANTS_MANUSCRIPT_CHANGE = false
```
