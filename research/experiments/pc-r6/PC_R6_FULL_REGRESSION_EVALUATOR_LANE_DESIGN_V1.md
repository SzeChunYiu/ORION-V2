# PC-R6 — Full-Regression Evaluator Lane (Registered Design V1)

**Class:** registered evaluator-lane extension over frozen proposals — **zero new
model calls**; new native compute ONLY for test-suite execution (re-evaluating
frozen patches). It makes an originally-registered but structurally
`CANNOT_CHECK` endpoint measurable. It cannot rescue any frozen null on the
mean-success endpoint; it can only evaluate the tail-safety endpoint that was
registered pre-outcome and never observed.

**Parent verdict this serves:** P-C (obligation-driven solver) status
`R2_REGISTERED_SCALE_NULL_IMPORTED…E60_COMPONENT_NULL` with the PC-R5
critical-failure slot `CANNOT_CHECK`. E30-R11 (480/480 complete) and E60
(600/600 complete) are mean-null: no arm separation (all primary exact p=1.0),
both analyzed components exactly outcome-neutral. The critical-failure hard
gate was `CANNOT_CHECK ×480` because the frozen-lane adapter executes only the
registered failing-test binding and writes
`full_regression_suite_status = "CANNOT_CHECK_NOT_RUN"`,
`critical_new_failure_count = None` per record
(`run/e30_r11_arm_eval_frozen_lane.py`; E30-R11 terminal receipt §"root cause";
E60 receipt §4 confirmed 0 checkable tasks in all four contrasts).

**Theory revision under test (licensed, pre-registered):** **B — "obligations
are tail insurance, not mean alpha."** The obligation ledger / decomposition /
reopen machinery may not raise mean task success yet still prevent damage the
mean endpoint cannot see: new failures among previously-passing tests. This is
not a post-hoc endpoint: `ORION_REAL_PROBLEM_CONFIRMATORY_SUITE_V1.json`
registers `full_regression_suite_passed` and `critical_new_failure_count` as
**primary outcomes**, and `ORION_REAL_PROBLEM_ANALYSIS_PLAN_V1.md` fixes the
margin pre-outcome: *"critical-failure non-inferiority margin: no more than 2
percentage points worse than F0"* and *"An average gain cannot offset a
critical gate failure."* The E30-R11 terminal receipt names this exact
follow-up: "a new frozen-lane stage that runs each project's full regression
suite — a named follow-up, not a re-analysis."

## 1. Question and falsifiable predictions

Q: On the frozen E30-R11/E60 proposals, does full-regression evaluation reveal
critical-failure structure invisible to the registered-failing-test lane?

| Prediction (pre-registered) | Gate |
|---|---|
| P-B1 (non-inferiority, the registered hard gate finally checkable): F2 critical-failure rate ≤ F0 + 2 pp | GR1 |
| P-B2 (tail insurance, the positive form): some contrast shows F2 (or a component) strictly REDUCING critical failures, CI excluding 0 | GR2 |
| P-B3 (component necessity via the registered necessity criterion): removing a component raises critical failures ≥ 2 pp | GR3 |
| P-B0 (lane validity): the new lane reproduces the frozen native_success vector bit-exactly and gold patches produce zero critical failures | GR0 |

## 2. Frozen inputs (no new dispatch)

- **Cell 1 (primary):** E30-R11 campaign
  `campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6`,
  `run/confirmatory-r{1,2,3}/{responses,evaluations}/<ARM>/<task_id>.json` —
  4 arms (`F2_ORION_METABOLIC_FULL`, `F0_PARENT_FEDERATION`,
  `SAME_MODEL_REFLECTION`, `SIMPLE_DIRECT`) × 40 tasks × 3 reps = 480 proposals.
- **Cell 2 (component map):** E60 campaign
  `campaign-e60-r1-component-ablation-20260829-38aedc50`,
  `run/confirmatory-r{1,2,3}/…` — 5 arms (`F2_ORION_METABOLIC_FULL`,
  `F2_MINUS_{DECOMPOSITION, NATIVE_RECOVERY, COUNTERPROBE,
  SELECTIVE_REOPEN}`) × 40 × 3 = 600 proposals.
- Substrate: BugsInPy at `11c5f1eea954a42132cfd06bf257766a7963e0fd`, 8
  projects, 40 tasks, frozen runtimes (unchanged from the existing lane).
- Truth anchors: `E30_R11_TERMINAL_RAW_ROLLUP.json` (freeze sha256 `4663435c…`)
  and the E60 `component_effects.json` / `supersede.sha256` manifests.

## 3. Evaluator stage spec (`full_regression_suite`)

Per task, three workspace executions under the frozen per-project runtime:

1. **Baseline pass (per task, arm-independent):** buggy workspace + task test
   patch → run the **frozen suite** = all test cases collected by the frozen
   runtime in the test file(s) referenced by the task's registered test
   command (parametrized instances count individually). Records per-test
   pass/fail; tests failing at baseline cannot become "new" failures.
2. **Patched pass (per arm × rep):** apply the arm's proposal patch with the
   existing application machinery (identical to the `registered_failing_test`
   stage), compile, run the same frozen suite. Record per-test pass/fail.
3. **Derived counts:** `critical_new_failure_count` = # tests passing at
   baseline and failing patched; `full_regression_suite_passed` = 1 iff
   registered failing test passes AND `critical_new_failure_count == 0`.

Conventions frozen now:
- **No imputation.** Non-applying / non-compiling proposals get
  `critical_new_failure_count = None`; excluded from risk-difference
  denominators and counted per arm (`compile_failure_rate` reported). The
  analysis layer, not the summary layer, is authoritative (the summary layer's
  `int(... or 0)` imputation is a known defect and is explicitly not used).
- **Per-task suite timeout 900 s wall** (frozen constant; covers the slowest
  per-file suites of the 8 projects under the frozen runtime). Timed-out
  baseline → task `SUITE_TIMEOUT`, excluded with count; timed-out patched pass
  → `critical_new_failure_count = None` for that evaluation (conservative: not
  counted as safe), counted per arm.
- Per-task scratch workspaces; no network; read-only over the frozen campaign
  trees; every file read enters the sha256 manifest.

## 4. Statistics (E60 conventions verbatim)

Analysis unit = task after within-task rep aggregation (majority over reps, as
E60); binary `any_critical_new_failure` per task per arm; paired risk
differences; **bootstrap 10,000 draws, PROJECT-stratified, seed 20260902**;
exact discordant-pair tests where discordants ≤ 10 (E60 convention). One-sided
upper bounds for non-inferiority at the registered margin; two-sided CIs for
superiority claims. All 7 contrasts (3 in Cell 1, 4 in Cell 2) reported in
full; Holm within each cell's pre-registered family (Cell 1 family size 3,
Cell 2 family size 4 — matching E60's registered family).

## 5. Gates (frozen before any suite run)

- **GR0 `LANE_VALID` (hard):** (a) the new lane's registered-failing-test
  results reproduce the frozen `native_success` vector **bit-exactly for all
  480 + 600 evaluations** from the E30-R11 raw rollup and E60
  `component_effects.json`; (b) known-answer control: on a frozen 5-task
  subset (one per project where available), the task's **gold patch** flips
  the registered failing test to passing AND yields
  `critical_new_failure_count == 0` under the same suite definition.
  GR0(b) failure = lane defect, fix lane, re-freeze; no gate evaluation.
- **GR1 `CRITICAL_NON_INFERIORITY` (the registered hard gate, now checkable):**
  Cell 1, F2 vs F0: upper bound of one-sided 97.5% CI for
  RD(any_critical_new_failure: F2 − F0) ≤ 0.02.
- **GR2 `TAIL_INSURANCE` (positive form):** any pre-registered contrast with
  point RD < 0 and stratified-bootstrap 95% CI excluding 0 (Cell 1: F2 vs
  each other arm; Cell 2: each MINUS_X vs FULL).
- **GR3 `COMPONENT_NECESSITY_TAIL` (registered necessity criterion):** Cell 2,
  some component with RD(MINUS_X − FULL) lower bound ≥ +0.02.

## 6. Pre-registered terminal map

| Outcome | Programme consequence |
|---|---|
| GR0 fail | lane defect — repair + re-freeze; nothing else evaluates |
| GR1 pass, GR2/GR3 null | P-C closes as **mean-null + tail-safe at the registered margin**: theory revision B survives as a boundary claim (contracted-result paper class, P-D precedent); no component earns tail-necessity |
| GR1 fail | revision B refuted in the harmful direction — obligations degrade tail safety; feeds contraction matrix and P-C manuscript's limitation section as a registered result |
| GR2 and/or GR3 fire | P-C's first registered positive evidence class; claim structure becomes "mean-null + tail-insured(/component-necessary)"; manuscript result block re-opened under a new freeze |

## 7. Non-goals / no-rescue clause

No mean-success claim of any kind may issue from this lane (mean endpoints are
frozen terminal). No re-dispatch of arms; only re-evaluation of the exact
frozen proposals listed in §2. No endpoint, margin, family, or suite
definition may change after the first suite execution. Any lane defect found
mid-run → halt, receipt, re-freeze (GR0 discipline).

## 8. Custody

- Designs `PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1.{md,json}` frozen in
  this PR; runner `pc_r6_fullreg_eval.py` sha256-stamped in the PR that
  dispatches it; runner reuses the frozen-lane adapter's patch-application
  path verbatim (import, not fork, where possible).
- Campaign id: `campaign-pc-r6-fullreg-e30r11-e60-<YYYYMMDD>-<manifest8>`.
- Every input file read (proposals, evaluations, task metadata, gold patches
  for GR0(b)) enters the sha256 input manifest; outputs
  `PC_R6_FULLREG_ROLLUP_V1.{json,md}` + `PC_R6_OUTCOME_RECEIPT.md` archived
  in-repo under `research/experiments/results/issue<current>/pc-r6/`.
- Compute: 40 baseline suites + 1,080 patched suites (+ GR0(b) 5 gold suites)
  ≈ 30–90 CPU-hours; LUNARC array job queued behind SD70 (3553181, from Sep 3
  18:35) and E70-GC1 (3553088, from Sep 4 08:00). PROPOSAL_ONLY ceiling
  unchanged — this lane evaluates proposals; it does not execute deployments.
