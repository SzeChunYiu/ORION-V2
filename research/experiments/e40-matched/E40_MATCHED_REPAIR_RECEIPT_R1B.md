# E40-M1 Repair Receipt R1b — Custody Canonicalization + Control-Pool Guard

**Lane:** E40 T3a (owner issue #45) · **Repairs:** dispatch R1 (jobs 3554313/3554314, receipt V1)
**Written:** 2026-08-30, before any re-run outcome was read (the R1 rollup never executed).

## 1. What failed in R1

1. **All 36 chain tasks → `CANNOT_CHECK.json`** ("arguments.json drift on training_regime") after
   their FIRST native run completed (exit 0, valid metrics). No chain advanced past cycle 1 / run 0.
2. **Eval job 3554314 failed in 42 s** at `control-uninformative`: `ZeroDivisionError` because the
   other-dataset feedback pool was empty (zero `redacted_feedback.json` existed — every chain had
   aborted at custody).

## 2. Root cause (single stage: custody comparison, not the runs)

Upstream CausalBench `main_app` (commit `1a2143cf…`) accepts enum **VALUES** on the CLI
(`--training_regime partial_interventional`) but serializes enum **NAMES** into
`results/<exp_id>/arguments.json` — including upstream's own misspelling:

| passed CLI value | recorded `arguments.json` |
|---|---|
| `observational` | `Observational` |
| `partial_interventional` | `PartialIntervational` (upstream misspelling of *PartialInterventional*) |
| `interventional` | `Interventional` |

The R1 custody check compared raw strings → every run "drifted". A mechanical normalization
(lowercase/strip underscores) cannot survive the `Parti**a**lIntervational` typo, so an explicit
canonicalization map is required:

```python
_REGIME_CANON = {"observational": "obs", "partialinterventional": "partial",
                 "partialintervational": "partial", "interventional": "inter", "intervational": "inter"}
```

The **native runs themselves were valid** — this is a record-comparison defect, not a substrate
defect. Dry-runs could not catch it: dry-run mode fabricates `arguments.json` from our own config
dict, so the mismatch only appears on the real substrate (recorded as a dry-run blind spot).

## 3. Fixes (runner sha256 `90842cee…` → `386fd1943b27e5bf22bb34440692f13708677a5077e4cbbb4612309fd5e48fa8`)

1. **Regime canonicalization** in the custody check (`canon_regime` on both sides); all other keys
   remain exact-string.
2. **Stale `CANNOT_CHECK.json` unlink** at chain start after the `ALREADY_COMPLETE` check (markers
   from an aborted pass must not linger over a now-valid chain).
3. **`control-uninformative` pool guard**: if any dataset's other-dataset feedback pool is empty,
   emit an explicit `CANNOT_CHECK__NO_FEEDBACK_POOL` verdict document instead of crashing
   (distinct "cannot check" vs "checked and fine"; eval's `set -euo pipefail` still aborts the
   rollup).
4. **Selftest cases** for the canon map (5 accept/reject cases incl. the misspelled record form
   and a true mismatch `partial_interventional` vs `Interventional`).

No arm prompt, plant, gate, statistic, or audit rule changed — the treatment surface is untouched.

## 4. Validation of the repair (all pre-outcome)

| Check | Result |
|---|---|
| Static re-verification of all 36 real R1 `arguments.json` vs the configs actually passed (F0 `upfront/config_1.json`, F2 `cycle1/config_1.json`, SIMPLE reconstructed from the deterministic E40 R1 default; 8 keys each) | **36/36 match, 0 drift, 0 unknown-canon** |
| `selftest` on LUNARC with the deployed runner | **0 failures** |
| Live resume of task 0 (SIMPLE — zero model calls, native metrics-skip) on the real campaign root | **`COMPLETE`** → `CHAIN_COMPLETE.json`, `redacted_feedback.json`, `exp_id` written; stale marker cleared |

## 5. Re-dispatch (R1b)

| Job | Type | Scope |
|---|---|---|
| **3554361** | array `0-35%6` (`o2-e40m1-chain`), 8 cpus / 64G / 2d | same frozen sbatch as R1 |
| **3554362** | single (`o2-e40m1-eval`), `--dependency=afterok:3554361` | control-planted → control-nullcal → control-uninformative → audit → rollup |

## 6. Resume semantics (why the re-run is clean, not a restart)

- `native_run` skips when `metrics.json` exists → the 36 valid R1 first-runs are **reused**, not
  repeated (108-run invocation budget unchanged in substance: 72 fresh + 36 reused).
- F2 `cycle1/decision.json` and F0 `upfront/decision.json` exist on disk → decisions are **reused,
  no model re-asks**; SIMPLE's config is deterministic (no model call by design). No arm-visible
  input differs from R1.
- The R1 rollup never executed and no held-out `quantitative_test_evaluation` was read by any
  operator or artifact — the receipt-before-outcomes ordering of V1 is preserved through the repair.

## 7. Checker-validation history (appended to V1 §5)

- v5 lesson (R1): custody comparisons against upstream-serialized records must canonicalize
  against the **recorded** vocabulary, including upstream spelling defects; validated against all
  36 real records before re-dispatch, not only fixtures.

skills-applied: none (repair receipt, no manuscript content)
