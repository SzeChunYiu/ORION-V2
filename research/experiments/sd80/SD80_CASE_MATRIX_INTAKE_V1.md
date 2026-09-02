# SD80 Case-Matrix Intake V1 — naturalistic witness sources + PC-R7 obligation-provenance tagging calibration

**Class:** `CASE_MATRIX_INTAKE__NO_ARM_RUN__NO_OUTCOME_ACCESS_BY_TAGGERS_OR_ARMS`  
**Computed:** 2026-09-02T13:49:10Z · **Host:** Mac (intake, hashing, tagging orchestration); LUNARC unreachable during intake (expired 2FA socket); billy-old reserved for any arm compute  
**Frozen inputs:** PC-R7 design (`research/experiments/pc-r7/`), FM80 protocol (`research/experiments/`), tagging rule `SD80_PC_R7_OBLIGATION_PROVENANCE_TAGGING_RULE_V1.md` (sha256 `e8f782a581e22cd7…`), cases file sha256 `a13eff3558abf209…`, hidden-key file sha256 `91237f3e6db8cd61…`.

## Terminal: `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES`

- TAG_POPULATION_BELOW_15_IN_SOME_DOMAIN: PSYCHOLOGY_RPP:{'EXTERNAL_VERIFIABLE': 100, 'INTERNAL': 0}, CANCER_BIOLOGY_RPCB:{'EXTERNAL_VERIFIABLE': 50, 'INTERNAL': 0}, FORMAL_MATHEMATICS_1000PLUS:{'EXTERNAL_VERIFIABLE': 59, 'INTERNAL': 1}

## 1. Lawful public witness sources

| Domain | Class | Source (public, no auth) | Witness class | Raw records | PC-R7-eligible |
|---|---|---|---|---|---|
| `PSYCHOLOGY_RPP` | empirical | OSF public API + published dataset (ezcuj/ytpuq rpp_data.csv; registrations via api.osf.io per project) | `REGISTERED_REPLICATION_VERDICT` | 100 | 100 |
| `CANCER_BIOLOGY_RPCB` | empirical | OSF public API + published final-analysis dataset (e5nvr); eLife Registered Reports | `REGISTERED_REPORT_REPLICATION_OUTCOME` | 76 | 50 |
| `FORMAL_MATHEMATICS_1000PLUS` | formal | mathlib4 docs/1000.yaml at master commit 8571709fdb0fea8d447fb72b4516559122daf569 + Wikidata EntityData | `MACHINE_CHECKED_FORMALIZATION_WITNESS` | 243 | 243 |
| `MACHINE_LEARNING_MLRC` | empirical/computational | SD30 MLRC journal-track inventory (OpenReview/TMLR) | `INDEPENDENT_PROSE_REPRODUCTION_VERDICT` | 36 | 0 |

MLRC is recorded but **not counted**: RECORDED_NOT_COUNTED: no outcome-free evidence layer (report text carries the verdict; OpenReview API challenge-gated 2026-09-02).

Source snapshots with sha256 live in `research/experiments/sd80/sources/raw/` (manifest in the cases JSON). Every case record and every hidden key is sha256-hashed (`record_sha256`, `hidden_key_sha256`); the hidden-key file `SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json` carries verdicts/outcomes and is never mounted in a tagger or arm workspace.

## 2. FM80 eligibility and remoteness

FM80 s3 items c-e and s4 remoteness are donor-specific; recorded NOT_APPLICABLE for PC-R7 (no donor arm) and PENDING for FM80 (no donor key / K / corpus freeze exists yet). FM80 eligibility is therefore PENDING for every case; PC-R7 eligibility uses items a, b, f, g.

## 3. GN0 — tagging calibration (two independent fresh-context taggers)

- Calibration set: 20 cases (seeded; 7 RP:P, 7 RP:CB, 6 formal). Agreement **20/20 = 1.00** (threshold 0.9) → GN0 **PASS**.
- Tag counts A: {'EXTERNAL_VERIFIABLE': 20, 'INTERNAL': 0}; B: {'EXTERNAL_VERIFIABLE': 20, 'INTERNAL': 0}.
- Disagreements: 0. Rule clarified to V1.1 on three ambiguities both taggers raised independently (per-registration withdrawal reading; accepted+linked Registered Report governs; formal enwiki entry must name the theorem or its object). Semantics unchanged.

## 4. Full tagging round (all PC-R7-eligible cases in the tagging pool)

| Domain | Eligible | Tagging pool | Tagged | A/B agreement | EXTERNAL_VERIFIABLE | INTERNAL | both ≥ 15 |
|---|---|---|---|---|---|---|---|
| `PSYCHOLOGY_RPP` | 100 | 100 | 100 | 1.000 | 100 | 0 | **no** |
| `CANCER_BIOLOGY_RPCB` | 50 | 50 | 50 | 1.000 | 50 | 0 | **no** |
| `FORMAL_MATHEMATICS_1000PLUS` | 243 | 60 | 60 | 1.000 | 59 | 1 | **no** |

Cross-tagger disagreements in the full round: 0; untagged: 0. Formal domain tagged on a frozen seeded 60-case sample of the 243 eligible entries (remainder `ELIGIBLE_UNTAGGED_RESERVE`).

## 5. Reading

Under the frozen PC-R7 §1 semantics, every registered-replication-verdict-class case is, by construction of the witness sources, externally constrained: RP:P cases carry an OSF registration, RP:CB cases a peer-reviewed eLife Registered Report, and formal cases an externally authored theorem statement. The `INTERNAL` stratum is therefore empty (or a single unverifiable record) in every domain, and the PC-R7 pre-registered population condition (both tags ≥ 15 cases/domain) cannot be met from these sources. Per PC-R7 §6 this is the contraction terminal `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` — a registered result, not a defect: the naturalistic obligation cell cannot test theory A's internal-vs-external contrast because naturalistic witness sources with verifiable outcomes do not supply an internally-constrained stratum. No arm was run; no outcome was read by any tagger or arm.

## 6. Custody

- Intake scripts: `scripts/sd80_case_matrix_intake.py`, `scripts/sd80_case_matrix_finalize.py`, `scripts/sd80_case_matrix_render_md.py`; custody tests `tests/unit/test_sd80_case_matrix_intake.py`.
- Tagger outputs: `research/experiments/sd80/tagging/` (calibration + full round, both taggers, GN0 receipt, final merged tags).
- Authority: grants no claim; no arm run; scientific truth not authorized.
