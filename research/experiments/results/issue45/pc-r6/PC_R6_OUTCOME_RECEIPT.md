# PC-R6 outcome receipt

**Design:** `PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1` (sha256 `5cdbb89aa09c…`)  
**Campaign:** `campaign-pc-r6-fullreg-e30r11-e60-20260902-774903e1`  
**Rollup:** `PC_R6_FULLREG_RAW_ROLLUP_V1.json` sha256 `eb33a7be38fd3f568107d6c1c0872d27fb5850a5b849e78a0b4afc74a2969a97`  
**GR0 receipt:** sha256 `0d74b701f9edfb653cc653c2423381cca7d5538db7b426669869b9c84163025e` (PASS, enforced before any gate)  
**Seed:** 20260902; bootstrap 10000 draws, PROJECT-stratified; Holm within families 3 and 4.

| gate | status |
|---|---|
| GR0 LANE_VALID | PASS |
| GR1 CRITICAL_NON_INFERIORITY | PASS |
| GR2 TAIL_INSURANCE | NULL |
| GR3 COMPONENT_NECESSITY_TAIL | NULL |

**Pre-registered routing:** GR1_pass_GR2_GR3_null: P-C closes as mean-null + tail-safe at the registered margin; theory revision B survives as a boundary claim; no component earns tail-necessity

No mean-success claim issues from this lane (design §7).


---

<!-- ORION-RECEIPT-BOUNDARY-V1
generated_bytes: 948
generated_sha256: 0e86f52151b70b8c9395cc8921f1b92549081702fde9876d2289a9ab35baaa2f
generator: research/experiments/pc-r6/pc_r6_fullreg_analysis.py
checked_by: scripts/check_receipt_boundaries.py
-->

> ### ⚠ HAND-WRITTEN BELOW THIS LINE — NOT MACHINE OUTPUT
> The first **948 bytes** of this file (everything above the rule) are the verbatim output of
> `pc_r6_fullreg_analysis.py`, sha256 `0e86f52151b7…35baaa2f`. That digest and this banner are
> asserted in CI by `scripts/check_receipt_boundaries.py`; if the generated region is edited the
> check fails.
> Everything below was written by hand at archive time. **Every figure below names the
> machine-generated artifact and field it was computed from.** A figure quoted out of this region
> without that citation is unsourced — do not propagate it.

## Archive addendum (2026-09-02) — denominators, power and honest reading

### Execution

*Sources:* job ids `JOB_IDS.env`; suite scale `PC_R6_FULLREG_RAW_ROLLUP_V1.json`
`.cells.<cell>.baselines.<task>.counts`; frozen inputs `PC_R6_INPUT_MANIFEST.json` `.entry_count`.

| item | value |
|---|---|
| Suite array | **3563626** (`JOB_IDS.env` `SUITE2`), 80/80 COMPLETED (one array index = one task: baseline pass + every arm x rep patched pass) |
| Rollup | **3563627** (`ROLLUP2`) COMPLETED, `"complete": true` |
| Analysis | run deliberately after the rollup was verified complete; refused to start without the GR0 PASS receipt (asserted before any gate was read) |
| Suite scale | 2,256 test cases collected across the 40 baseline suites per cell (median 43 per task, min 1, max 260) |
| Frozen inputs | 2,858 hashed entries, campaign `campaign-pc-r6-fullreg-e30r11-e60-20260902-774903e1` |

### What the endpoint actually observed

The endpoint is **not vacuous** — six evaluations recorded critical new failures
(`PC_R6_FULLREG_RAW_ROLLUP_V1.json`, every
`.cells.<cell>.evaluations.<arm>/<task>.<rep>` with `critical_new_failure_count > 0`):

| cell | arm / task | rep | count | kind |
|---|---|---|---|---|
| e30r11 | `F0_PARENT_FEDERATION` / `bugsinpy-pandas-2` | r3 | 6 | failed |
| e60 | `F2_MINUS_DECOMPOSITION` / `bugsinpy-ansible-2` | r2 | 7 | failed |
| e60 | `F2_MINUS_DECOMPOSITION` / `bugsinpy-scrapy-3` | r2 / r3 | 3 / 2 | failed |
| e60 | `F2_MINUS_SELECTIVE_REOPEN` / `bugsinpy-scrapy-3` | r3 | 2 | failed |
| e60 | `F2_ORION_METABOLIC_FULL` / `bugsinpy-scrapy-3` | r3 | 10 | error |

After the registered majority-over-reps aggregation exactly **one** task-arm cell is True
(`F2_MINUS_DECOMPOSITION` / `bugsinpy-scrapy-3`, 2 of 3 reps). `bugsinpy-scrapy-3` is
CANNOT_CHECK in the FULL arm (r1/r2 never applied, only r3 counted → majority `None`), so
that single positive is excluded from every paired contrast by the no-imputation rule. This
is the mechanical reason GR2 and GR3 are NULL rather than firing, and it is a power
limitation, not evidence of tail safety in that comparison.

### Denominators (the headline caveat)

Every paired contrast is concordant-negative, so all seven risk differences are exactly
0.0000 with a **degenerate** bootstrap interval [0.0000, 0.0000]: a bootstrap cannot produce
width from an all-identical difference vector, and with zero discordant pairs the exact test
is undefined (`exact_discordant_p = null`) and Holm has no testable hypothesis in either
family. GR1 therefore passes at the registered 2 pp margin **on 5 paired tasks out of 40**
(`PC_R6_FULLREG_ROLLUP_V1.json` `.cells.<cell>.contrasts[].checkable_task_count`):

| contrast | checkable paired tasks | excluded |
|---|---|---|
| F2 − F0 (GR1) | **5** (`ansible-2, black-5, scrapy-4, tqdm-4, tqdm-5`) | 35 |
| F2 − SAME_MODEL_REFLECTION | 4 | 36 |
| F2 − SIMPLE_DIRECT | 4 | 36 |
| FULL − each MINUS_X (all four) | 7 | 33 |

The dominant exclusion is `NONE_PATCH_NOT_APPLIED`: **90–99 of the 120 evaluations in every arm,
75.0%–82.5%** pooled over the nine arm rows. The frozen proposals largely do not apply to the
frozen workspaces — a property of the imported proposals, not of this lane.

*Sources for the table:* `PC_R6_FULLREG_RAW_ROLLUP_V1.json`,
`.cells.<cell>.arm_totals.<arm>.none_reasons.NONE_PATCH_NOT_APPLIED` over
`.cells.<cell>.arm_totals.<arm>.evaluations`; the `rc` split counted directly from
`.cells.<cell>.evaluations.<arm>/<task>.<rep>.patch_apply_returncode`.

| cell | arm | not applied | of | % | of which `rc=128` | `rc=1` |
|---|---|---|---|---|---|---|
| e30r11 | `F0_PARENT_FEDERATION` | 96 | 120 | 80.0 | 77 | 19 |
| e30r11 | `F2_ORION_METABOLIC_FULL` | 98 | 120 | 81.7 | 78 | 20 |
| e30r11 | `SAME_MODEL_REFLECTION` | 97 | 120 | 80.8 | 83 | 14 |
| e30r11 | `SIMPLE_DIRECT` | 94 | 120 | **78.3** | 73 | 21 |
| e60 | `F2_ORION_METABOLIC_FULL` | 98 | 120 | 81.7 | 79 | 19 |
| e60 | `F2_MINUS_COUNTERPROBE` | 99 | 120 | **82.5** | 82 | 17 |
| e60 | `F2_MINUS_DECOMPOSITION` | 90 | 120 | **75.0** | 68 | 22 |
| e60 | `F2_MINUS_NATIVE_RECOVERY` | 96 | 120 | 80.0 | 74 | 22 |
| e60 | `F2_MINUS_SELECTIVE_REOPEN` | 93 | 120 | 77.5 | 78 | 15 |

Pooled: **75.0%–82.5%** (e30r11 alone 78.3%–81.7%; e60 alone 75.0%–82.5%). By cell the `rc=128`
totals are **311 of the 480 e30r11 evaluations** and **381 of the 600 e60 evaluations**
(692 of 1,080 overall); the remaining non-applications are `rc=1` — 74 and 95 respectively.

> **Correction (2026-09-02). Two figures in this addendum were wrong as first written.**
>
> 1. The range was given as "78–83%". That pairs the e30r11 minimum with the e60 maximum and is
>    supported under neither scoping. Correct: **75.0%–82.5%** pooled, as tabulated above.
> 2. `311/480 patch-apply rc=128` was attributed to "the frozen lane". No result artifact under
>    `research/experiments/results/issue45/e30-r11/` records patch-apply return codes at all —
>    `E30_R11_TERMINAL_RAW_ROLLUP.json` `.per_arm_totals.<arm>` carries only `evaluations`,
>    `native_success`, `cannot_check` and `native_success_rate_over_120`, and the only `rc=128`
>    in that tree is a single worked example in `E30_R11_EVALUATION_LANE_DEFECT_AND_ADAPTER.json`
>    — so the attribution cannot be checked against that lane. The count itself is correct and
>    reproducible from **this** lane's own raw rollup (field cited above). Both lanes have 480
>    e30r11 evaluations (4 arms × 40 tasks × 3 reps; `E30_R11_TERMINAL_RAW_ROLLUP.json` sums to
>    480 as well), so the denominator alone does not distinguish them — the likely origin of the
>    misattribution.
>
> The second is the more instructive of the two: its *value* verifies, and only its *citation*
> resolves to nothing. A reader checking the arithmetic finds it fine; a reader checking the
> source finds no artifact.
>
> Both figures reached `papers/prospectuses/SILENT_FAILURE_MODES_ADMISSION_ASSESSMENT_V1.md` §2.1
> before the source was re-read. The boundary marker, the rendered banner at the top of this
> region and `scripts/check_receipt_boundaries.py` exist because of them.

Two tasks (`bugsinpy-ansible-4`, `bugsinpy-fastapi-3`) have baselines whose registered test file
contains no passing test at all (`BASELINE_SUITE_NO_PASSING_TESTS`,
`.cells.<cell>.baselines.<task>.status`) and are excluded with count in both cells; compile
failure after a successful apply is rare (0–4.3% per arm,
`.cells.<cell>.arm_totals.<arm>.compile_failure_rate`).

**Honest reading.** The hard gate that E30-R11 left structurally `CANNOT_CHECK` is now
*checkable and checked*: it is answered on real suite executions with no imputation, and it
passes. But "F2 is non-inferior to F0 on critical new failures" rests on five paired tasks in
which neither arm produced a single critical failure. The pre-registered terminal
(mean-null + tail-safe at the registered margin, theory revision B surviving as a boundary
claim) is the correct route; the claim must be stated with its denominator attached, and
this cell cannot support a tail-safety claim of any strength beyond that margin at n = 5. No
mean-success claim issues from this lane (design §7).

### Substrate findings carried forward (from GR0(b), receipt §7 of the dispatch receipt)

- **F1** `bugsinpy-cookiecutter-1`'s registered failing test cannot be flipped by any
  source-only patch: the fixed commit adds a fixture the BugsInPy checkout never copies.
- **F2** `bugsinpy-black-1`'s registered test is order-dependent in the full-module run
  (baseline-failing inside the suite → it can never be a critical new failure).
