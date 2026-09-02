# E30-R12 — Confirmatory BugsInPy re-run under arm-side apply-clean patch emission

**Registered design V1 · 2026-09-02 · `PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS`**
**Canonical object:** `E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json` (this file is its prose form; the JSON governs on any discrepancy)
**Anchor commit:** `8945cec` (PR #168, arm-side apply-clean emission)
**Class:** new prospective confirmatory study with new model dispatch. **Not** a re-analysis of E30-R11.

## 1. Why this study exists

E30-R11 was the programme's confirmatory real-problem study: 4 arms × 40 frozen
BugsInPy tasks × 3 repetitions = 480 responses, every arm at 10–15% success, no arm
separation, all Holm p = 1.0. Three later frozen studies show that null was measured
through a broken interface rather than produced by solver behaviour:

- **E70-GC1** localized the *entire* raw-endpoint variance between arms to unified-diff
  hunk-header miscounting: `success_iff_header_unchanged = true` for all four arms, and
  the syntax-normalized endpoint was 24/24 for every arm.
- **E70-GC2** found raw header-exact success 0/16 at every one of three difficulty rungs,
  with 48/48 diffs needing syntax-only canonicalization.
- **PC-R6**, re-evaluating E30-R11's own frozen proposals, found `NONE_PATCH_NOT_APPLIED`
  in **78–83% of evaluations per arm**; the frozen lane had already recorded **311/480**
  patch-apply `rc=128`.

Roughly four in five E30-R11 evaluations therefore never tested a repair. They tested
whether a model can count lines in a hunk header. PR #168 moved canonicalization to the
emission side in both arm executables, with a CI gate holding that path gold-blind and
non-mutating. The registered question has consequently never been asked under a working
interface. R12 asks it.

This is the most defensible "does the framework actually work" experiment currently
available to the programme: the task is real, the endpoint is externally verified by each
project's own test suite, the ceiling is far away (best arm 15%), and the confound that
flattened the previous run is fixed.

## 2. What R12 shares with E30-R11, and what it changes

E30-R11's endpoints are **frozen and terminal**. R12 may not revise, re-score or
reinterpret them, and does not present itself as a correction of them.

| | |
|---|---|
| **Unchanged** | the 8 projects; the same 40 frozen task ids; the 4 arms; 3 repetitions; gold-blind and oracle-custody discipline; the registered primary endpoint |
| **Changed** | arm-side apply-clean patch emission (`8945cec`); a fail-closed served-model assertion; the full-regression critical-failure endpoint checkable from the first evaluation instead of structurally `CANNOT_CHECK`; a registered apply-rate diagnostic |

## 3. Substrate

BugsInPy at `11c5f1eea954a42132cfd06bf257766a7963e0fd`; projects `ansible, black,
cookiecutter, fastapi, pandas, scrapy, tornado, tqdm`; the 40 task ids listed verbatim in
the design JSON.

The substrate is **reused, not regenerated**. R12's campaign copies E30-R11's gold-blind
requests, frozen task table, taskmap and setup receipt, and symlinks its read-only trees:
`prepared` (the solver workspaces the requests name by absolute path), `evaluator_private`
(the oracle tree, which the adapter only ever `copytree()`s out of), `inputs` (the pinned
BugsInPy checkout) and `baseline_lanes` (gold patches, read only by GR0b). Only
`responses` and `evaluations` are new, and every R12 write lands under the R12 campaign
directory.

That is deliberate rather than merely cheap: it makes the arm code and the served-model
pin the *only* differences between R11's inputs and R12's, so a difference in outcome
cannot be attributed to a rebuilt substrate.

For the scale-up discussion in §7: the pinned commit carries **501** numeric bug ids in
total and **295** within the 8 registered projects.

## 4. Model binding — assert the served id, fail closed

The z.ai Anthropic-compatible endpoint silently substitutes models. Verified live on
2026-09-02 against the campaign credential: **requesting `glm-5.2` is served `glm-5.3`**,
HTTP 200, no warning. E30-R11's campaign env requested `glm-5.2`.

R12 therefore requests `glm-5.3` and pins `ORION_ARM_SERVED_MODEL=glm-5.3`. Every call
reads `data["model"]` from the response body and raises `ServedModelMismatch` unless it
matches exactly. The exception is re-raised out of `run_arm` instead of being folded into
an `EXECUTION_FAILED_MODEL_RESPONSE` envelope, so a substitution stops the arm with a
non-zero exit rather than quietly producing a mixed-model dataset. Each envelope records
`resource_receipt.served_model_ids`, and gate **GR0c** refuses to compute any contrast
unless all 480 envelopes record exactly one served id and all of them are identical.

**Stated limitation.** E30-R11's envelopes record no served id, so R11's served model is
*inferred* (almost certainly `glm-5.3`), not verified. R12-vs-R11 comparison is descriptive
only. Within R12, both arms of every contrast are served-model homogeneous by assertion.

The codex CLI channel is unaffected by the substitution and is not used by this study.

## 5. Endpoints

**E1 — primary.** `registered_failing_test_fixed`: the task's registered failing test
passes after the arm's patch applies and the workspace compiles. Unit = task, after
within-task majority over the 3 repetitions. Denominator 40.

**E2 — co-primary.** `any_critical_new_failure`: at least one test that passes in the
baseline suite fails after the patch, derived exactly as PC-R6 §3 derives
`critical_new_failure_count`. Non-inferiority direction: F2 must not exceed F0 by more
than 0.02 — the margin fixed pre-outcome in the analysis plan §7. Companion measure
`full_regression_suite_passed = 1` iff the registered test passes and
`critical_new_failure_count == 0`.

This is the endpoint E30-R11 left structurally `CANNOT_CHECK` because its frozen-lane
adapter ran only the registered-test binding. R12 runs the full-regression lane from the
first evaluation, so the hard gate is checkable from the start by construction.

**D1 — registered diagnostic.** `patch_apply_rate`: the proportion of an arm's 120
evaluations whose `git apply` returns 0. Reported per arm with an exact binomial interval.
Its purpose is to make the emission fix's effect *measured* rather than assumed.

The comparator is PC-R6's per-arm apply-**fail** rates — F2 0.8167, F0 0.8000,
SAME_MODEL_REFLECTION 0.8083, SIMPLE_DIRECT 0.7833 — because only the PC-R6 evaluator is
the same code R12 runs. The frozen lane's 311/480 `rc=128` is a different application path
and is not an apples-to-apples comparator. **Registered directional prediction:** every
arm's apply-fail rate falls below its PC-R6 comparator, and below 0.40 absolutely.

D1 cannot support any claim about arm separation or repair quality.

## 6. Task dispositions — registered before dispatch

PC-R6 surfaced four arm-independent substrate pathologies among these 40 tasks. Deciding
their treatment after seeing R12's numbers would be `criterion_mutation`, a registered hard
failure, so the dispositions are fixed here and keyed to **machine-detected condition
codes**, not to task names or observed outcomes.

| Condition code | E1 | E2 | Expected ids |
|---|---|---|---|
| `BASELINE_SUITE_NO_PASSING_TESTS` — no test passes before patching, so none can newly fail | RETAIN | **EXCLUDE WITH COUNT**, ids reported | `ansible-4`, `fastapi-3` |
| `REGISTERED_TEST_BASELINE_FAILS_IN_SUITE` — the registered test is order-dependent and already fails inside the module run | RETAIN (E1 runs the test binding, not the module suite) | RETAIN for `any_critical_new_failure`; `full_regression_suite_passed` = `CANNOT_CHECK` | `black-1` |
| `REGISTERED_TEST_UNFIXABLE_BY_SOURCE_ONLY_PATCH` — the fixed commit adds a fixture the checkout never copies | RETAIN in the primary denominator, **plus** a pre-registered 39-task sensitivity denominator | RETAIN | `cookiecutter-1` |

The third condition is not detectable from the baseline pass; it is carried as a named
pre-outcome finding from PC-R6's GR0(b) and applies only if R12's own GR0(b) gold control
reproduces the same failure on the same task. Retaining it in E1 is safe rather than
generous: it is concordant-negative for every arm by construction, so it contributes no
discordant information and cannot bias a paired contrast — it only dilutes the marginal
rates, which the 39-task sensitivity denominator exposes.

Expected denominators: **E1 = 40** (sensitivity 39), **E2 ≤ 38**, exact count reported.

## 7. Prospective power note — 40 tasks cannot detect a plausible effect

Computed by `e30_r12_power_note.py`: pure arithmetic, exact enumeration, no simulation, no
outcome input. The registered test is an exact two-sided McNemar/sign-binomial on
task-level discordant pairs under Holm with family size 3, so the first step compares
against α/3 = 0.01667 and power depends on exactly two quantities: the discordance
proportion ψ and the true risk difference δ.

**Arithmetic floor.** With fewer than **7** discordant tasks all pointing the same way,
the exact test cannot reach 0.01667 *at any effect size*. At n = 40 that is a risk
difference of **0.175** before the test can reject even in principle.

| ψ (discordance) | MDE at n = 40, 80% power | Power at the registered 5 pp MID | Tasks needed for 80% power at 5 pp |
|---|---|---|---|
| 0.10 | unreachable | 0.0116 | 430 |
| 0.20 | unreachable | 0.0185 | 863 |
| 0.30 | 0.2675 | 0.0168 | 1287 |
| 0.40 | 0.3170 | 0.0157 | 1708 |

Stated plainly: **40 tasks cannot detect a plausible effect.** Power against the
programme's own registered 5-percentage-point minimum important difference is 1–2%. And
the proposed task count that *could* detect it does not exist on this benchmark: 430 tasks
in the most favourable discordance regime already approaches the whole pinned pool of 501,
and the plausible regimes (863–1708) exceed BugsInPy entirely. Within the 8 registered
projects only 295 bugs exist.

**So R12 is registered as an estimation and diagnostic study at n = 40** — comparable to
E30-R11, powered for the apply-rate diagnostic, and explicitly *not* a powered superiority
test. Failure to reject is the expected outcome under any effect below 0.175 and must
never be reported as evidence of equivalence. A genuinely powered confirmatory test of the
registered MID needs either a materially larger real-problem substrate than BugsInPy, or a
MID re-registered — before dispatch, never after outcomes — at what the available n can
actually detect.

**Repetitions.** Three matches E30-R11 and the suite's `minimum_stochastic_repetitions`.
E30-R11 documented 2–6 tasks per arm flipping across reps, so 5 would reduce task-level
misclassification; but repetitions buy reliability, not power — the test is on tasks, and
the 7-discordant-task floor is unchanged. R12 stays at 3.

## 8. Execution-lane contract — registered, not improvised

E30-R11 diagnosed two failure signatures that produce `EXECUTION_FAILED_MODEL_RESPONSE`
envelopes carrying no model output, and repaired both. One repair was campaign-local and
never reached `main`, so any later run silently inherits the defect; the other was a
procedure rather than code. Both are registered here **before** dispatch so R12's
execution lane is identical to R11's terminal one by declaration.

1. **Strict-parse reject.** The model emits literal newlines inside JSON string values,
   which `json.loads`' default `strict=True` rejects ("Invalid control character at line
   N") although `strict=False` decodes the identical object. `_json_object` in
   `scripts/orion_claude_arms.py` now passes `strict=False`. This is decoder tolerance
   only: same bytes, same Python object, with prompts, schema, model, temperature, arm
   structure and scoring untouched. It accounted for 4 of E30-R11's 13 stuck cells.
2. **Truncation starvation.** The served model emits a thinking block counted inside
   `max_tokens`; on the largest tasks the thinking consumes the whole per-call budget
   before the JSON closes (`stop_reason=max_tokens`, zero visible text). The primary
   budget is `ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET=6000` — the budget under which 466 of
   E30-R11's 480 envelopes completed — and **from pass 3** the dispatch loop applies R11's
   registered raise to 36000 (12000 per call on the 3-call arms), **only** to envelopes
   that carry no model output. That is an execution-resource raise, not resampling: a
   `COMPLETED_PROPOSAL_ONLY` response is never re-rolled.

   Pass 3 rather than a long plateau because the starvation is **deterministic at
   temperature 0**, not noise. A pre-dispatch smoke call on the exact channel returned
   `output_tokens` pinned exactly at the 6000 cap with zero visible text; the identical
   request at 36000 used 3669. Further passes at the primary budget would re-truncate the
   same cells — E30-R11's own loop plateaued at 13 and only the raise cleared them. Two
   full passes preserve R11's resourcing for everything that can complete there.

   The policy is identical across arms, so it cannot bias a paired contrast. Arms do starve
   at different rates, because the total budget is divided by the arm's call count
   (SIMPLE_DIRECT 1, F0 and F2 3) exactly as in E30-R11 — but an envelope failure is a
   *missing datum*, not a failure outcome, so rescuing more of them reduces missingness
   rather than favouring an arm.

The outcome receipt reports envelopes completed at the primary budget, envelopes completed
only after escalation, envelopes never completed by signature, and actual wall-clock and
model-call counts per arm.

## 9. Evaluation lane

`e30_r12_fullreg_eval.py` registers an `e30r12` cell on PC-R6's evaluator and delegates.
The PC-R6 evaluator is **imported, not forked**, so R12's apply rates are produced by
literally the same code that produced the D1 comparator, and the PC-R6 evaluator in turn
imports the frozen E30-R11 adapter (`sha256 829abb41…`) verbatim for workspace
provisioning, patch application and compile. No imputation: non-applying, non-compiling
and timed-out evaluations carry `critical_new_failure_count = None` with a reason code and
are excluded from denominators with a count. Per-task suite timeout 900 s.

## 10. Gates

| Gate | Hard | Statement | On failure |
|---|---|---|---|
| **GR0a** `LANE_SELF_CONSISTENCY` | yes | the full-regression lane's registered-failing-test vector reproduces the campaign's own frozen-lane vector bit-exactly for all 480 evaluations | halt, receipt, re-freeze; no endpoint read |
| **GR0b** `GOLD_KNOWN_ANSWER_CONTROL` | yes | on a frozen 5-task subset the gold patch flips the registered test *and* yields zero critical new failures | halt, receipt, re-freeze |
| **GR0c** `SERVED_MODEL_HOMOGENEITY` | yes | all 480 envelopes record exactly one served id, all identical, equal to the frozen id | halt; no contrast computed |
| **GR1** `APPLY_RATE_DIAGNOSTIC` | no | every arm's apply-fail rate below 0.40 and below its PC-R6 comparator | R12 reports it measured a still-broken interface |
| **GR2** `PRIMARY_SEPARATION` | no | E1: any F2-vs-control contrast rejects at Holm-adjusted α = 0.05 | non-rejection expected; never equivalence |
| **GR3** `CRITICAL_NON_INFERIORITY` | yes | E2: one-sided 97.5% upper bound for RD(F2 − F0) ≤ 0.02 | non-compensatory; no E1 gain may offset it |

PC-R6's GR0(a) checked against a pre-existing frozen vector. R12 has none, so GR0a is
replaced by self-consistency: R12 runs **both** evaluators over its own 480 proposals and
requires exact agreement. GR0b transfers verbatim.

## 11. Pre-registered routing

| Case | Terminal |
|---|---|
| GR0a/GR0b/GR0c fails | `LANE_DEFECT` — halt, receipt, re-freeze; no endpoint is read |
| GR1 fails | `INTERFACE_STILL_BROKEN` — emission-side canonicalization did not materially raise the apply rate; E1/E2 reported with the measured apply rate attached to every number, and the study does not claim to have tested repair |
| GR1 passes, GR2 null, GR3 passes | `NO_ARM_SEPARATION` under a working interface, tail-safe at the registered margin — **an expected and legitimate terminal**, not a failed study |
| GR1 passes, GR2 null, F0 numerically ≥ F2 on E1 | `PARENT_SUFFICIENT` — the strongest native parent suffices on this substrate; closes the F2-superiority line on real debugging |
| GR1 passes, GR2 rejects for F2, GR3 passes | `FIRST_REGISTERED_POSITIVE` — requires independent replication under a new identity before any paper claim |
| GR2 rejects against F2 | `F2_HARMFUL` on this substrate, reported as plainly as a positive |
| GR3 fails | `CRITICAL_REGRESSION` — non-compensatory; no F2 advantage of any size may be claimed |

**Precedence.** The cases are evaluated in the order `LANE_DEFECT`, `F2_HARMFUL`,
`CRITICAL_REGRESSION`, `INTERFACE_STILL_BROKEN`, `FIRST_REGISTERED_POSITIVE`,
`PARENT_SUFFICIENT`, `NO_ARM_SEPARATION`; the first match is the terminal. Hard-gate and
adverse terminals precede favourable ones, and `PARENT_SUFFICIENT` precedes
`NO_ARM_SEPARATION` because it is the more specific description of the same state.

## 12. No-rescue clause

R12 may not: revise, re-score, re-analyze or reinterpret E30-R11's, E60's or PC-R6's
endpoints; present itself as a correction of E30-R11; use the apply-rate diagnostic to
re-read E30-R11's null as anything other than what E30-R11's terminal receipt states;
change any endpoint, margin, family, disposition rule or suite definition after the first
response is written; drop a task after seeing which arm fails on it; or re-roll a completed
model response — only `EXECUTION_FAILED_MODEL_RESPONSE` envelopes, which contain no model
output, may be re-dispatched, exactly as E30-R11's guarded redispatch did.

**If the arms still do not separate once patches actually apply, that is a real and
important result, and it is reported as plainly as a positive would be.**

## 13. Custody

Seed `20260902`. Dispatch is gated on `E30_R12_COORDINATOR_AUTHORIZATION.json` carrying
`coordinator_written = true`, the operator's **verbatim** instruction quoted from human
chat input, `operator_instruction_source` naming where that instruction came from, and
`acknowledged_design_sha256` equal to the sha256 of the design JSON — absent at design
freeze, written immediately before dispatch. The distinction is deliberate: the quoted
instruction is human input, the record of it is not, and a field claiming the file itself
was human-written would be a fabricated custody claim. Arms read only the
gold-blind solver workspace; gold patches are read only by GR0b, after all responses are
written. Outputs: `E30_R12_FULLREG_RAW_ROLLUP_V1.json`, `E30_R12_ROLLUP_V1.{json,md}`,
`E30_R12_OUTCOME_RECEIPT.md`, `JOB_IDS.env`.

**Authority.** This study grants no scientific truth, field status, supertheory status or
publication readiness. `PARENT_SUFFICIENT` and `NO_ARM_SEPARATION` are valid terminals.

skills-applied: none (registered design, no manuscript content)
