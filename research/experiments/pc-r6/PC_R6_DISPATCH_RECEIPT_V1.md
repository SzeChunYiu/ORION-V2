# PC-R6 dispatch receipt (V1)

**Design:** `PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1.{md,json}` (frozen, unchanged by this PR)
**Class:** registered evaluator-lane extension, zero model calls, native suite compute only, no mean rescue
**Campaign id:** `campaign-pc-r6-fullreg-e30r11-e60-20260902-774903e1`
**Input manifest:** `PC_R6_INPUT_MANIFEST.sha256` — `2858` entries, sha256 `774903e14ff2bb2b0ac8a274fbb6b8a2ecead2a7545613199662f4dd44d445f9` (manifest8 `774903e1`)
**Dispatch date:** 2026-09-02 (LUNARC, account `lu2026-2-51`, partition `lu48`)

## 1. Frozen code (sha256 stamped at dispatch)

| artefact | path | sha256 |
|---|---|---|
| runner (v2, re-frozen after GR0(b) defect, §7) | `research/experiments/pc-r6/pc_r6_fullreg_eval.py` | `4c62a32e0ea92752b8d94402b53a554caaae5ed9ad7e62320758945d857dba86` |
| runner v1 (executed GR0(a) array 3563415; superseded) | same path at PR #141 merge `d1c7e92` | `284d04df88f42844f5711eb2674045700e79776a740363d84893f9c9b8e0c025` |
| analysis | `research/experiments/pc-r6/pc_r6_fullreg_analysis.py` | `a7c689c013c2d511a9e471ca5ef7ba084ab1bec98134856b18cb1efd40da111b` |
| frozen-lane adapter (imported verbatim, asserted at every run) | `research/experiments/results/issue45/e30-r11/drivers/e30_r11_arm_eval_frozen_lane.py` = LUNARC `R11/run/e30_r11_arm_eval_frozen_lane.py` | `829abb411ccf0bd71182eea4c11d2e07fae60f3b743872f7b4fce0a8635aae93` |
| frozen analyzer (imported for §4 statistics) | `scripts/analyze_orion_real_problem_results.py` | `ef195f7b8d6edafb9b48f3873eeb3f4041fcce6d87aad288e7ede1865428e3f2` |
| truth anchor, E30-R11 | `research/experiments/results/issue45/e30-r11/E30_R11_TERMINAL_RAW_ROLLUP.json` (internal freeze `4663435c…`) | `791320f47d644f9e3381e97a108ee5677d0c91fcee44b84d61a3063cc97d5761` |
| truth anchor, E60 | `research/experiments/results/issue45/e60-r1-component-ablation/component_effects.json` | `7aaf429654115ccfb293032b2ed21d378bc0e46b78c7d12d6c16c69479b50795` |
| truth anchor, E60 | `…/e60-r1-component-ablation/E60_R1_COMPONENT_ABLATION_ANALYSIS.json` | `2c8237f5862a5d9308d51dc5a124f14dcf38c82e049731cd55a5e4276554016a` |
| truth anchor, E60 | `…/e60-r1-component-ablation/supersede.sha256` | `7b340337f8ec7ba9476028becfc6385ece61b91a6bf895977866bb31d339c20f` |
| SLURM templates | `research/experiments/pc-r6/sbatch/pc_r6_{common.sh,gr0a_array,gr0b,gr0_verify,suite_array,rollup}.sbatch` | in PR |
| unit + end-to-end tests | `tests/unit/test_pc_r6_lane.py` (15 tests, `main()` driven on a synthetic two-cell campaign through the real adapter closure and the real frozen runtime) | in PR |

## 2. Lane construction (design §3, verbatim reuse)

- The adapter's `make_frozen_lane_evaluate_bugsinpy(...)` closure is imported and executed unchanged for
  workspace copy/restore, `git apply --whitespace=nowarn -`, `compile_workspace`, the registered
  failing-test binding and the stock pass predicate. A `RuntimeProxy` wraps only
  `execute_test_binding`: the registered test runs first (verbatim), then the frozen suite runs in the
  same compiled workspace; the closure's record (`orion.v2.task-evaluation.v1`) is kept and extended
  under `pc_r6`, with the closure's original `CANNOT_CHECK_NOT_RUN` fields preserved under
  `frozen_lane_original`.
- Driver interpreter on LUNARC: `R11/run/venv/bin/python` (3.11.5), the interpreter the frozen lane and
  the E60 eval used. No module loads (the precedent eval jobs used none; gcc resolved on the default path).
- Cells: `e30r11` = 4 arms × 40 tasks × 3 reps (480); `e60` = 5 arms × 40 × 3 (600). E60's
  `evaluator_private/`, `source/`, `SETUP_RECEIPT.json` are `cp -al` hardlinks of R11's (E60 prep receipt).
- Array index map: 0–39 = e30r11 tasks (sorted task_id), 40–79 = e60 tasks. One index = one task's
  baseline + all arm×rep patched passes. Resumable: existing records with the lane marker are skipped.
- No imputation: `critical_new_failure_count = None` with a reason code
  (`NONE_PATCH_NOT_APPLIED`, `NONE_COMPILE_FAILED`, `NONE_SUITE_TIMEOUT`, `NONE_SUITE_NOT_COLLECTED`,
  `NONE_BASELINE_UNAVAILABLE`, `NONE_RESPONSE_UNCHECKABLE`, `NONE_EVALUATOR_EXCEPTION`,
  `NONE_WORKSPACE_CHECKOUT_FAILED`); per-arm `compile_failure_rate`, `patch_apply_failure_rate` reported.
- Read-only over the frozen trees: all writes land under the PC-R6 campaign directory; every input read
  is hashed (`PC_R6_INPUT_MANIFEST.sha256` at freeze; per-stage read manifests unioned into
  `PC_R6_READ_MANIFEST.sha256` at rollup).

## 3. Amendments (conservative readings, recorded BEFORE any suite execution)

| id | ambiguity in the design | reading adopted |
|---|---|---|
| A1 | "all test cases collected by the frozen runtime in the test file(s)" — which runner collects | the registered command's own runner family: pytest for `pytest` / `python -m pytest` / `tox` lines (tox keeps the frozen `-q -o addopts=` rewrite), the stdlib unittest loader for `python -m unittest` lines (black, scrapy, tornado). Per-test identity = junit `classname::name` / `TestCase.id()`; parametrized instances count individually. Files taken from the registered command; `bugsinpy_bug.info` `test_file` cross-checked and recorded |
| A2 | "failing patched" | a baseline-passing test that is failed, errored, skipped or **missing** (not collected because the patch broke the module) counts as a new failure; breakdown recorded per evaluation |
| A3 | baseline pass mechanics | the same adapter path with a marker patch that creates one untracked dotfile (`git apply` refuses empty input); baseline run per cell (80 suites, not 40) so each cell is compared against a baseline from its own frozen tree — an extra replicate, identical trees by construction |
| A4 | "frozen 5-task subset (one per project where available)" | projects in lexicographic order, lowest `bug_id` per project, first five with an existing gold patch: `ansible-1, black-1, cookiecutter-1, fastapi-1, pandas-1` (covers the pytest, unittest and tox families). Gold source = BugsInPy `projects/<p>/bugs/<id>/bug_patch.txt` in the campaign's `baseline_lanes/`; forward direction verified by `git apply --check` on all five. Only the `gr0b` stage reads gold; its records carry `gold_or_fixed_solution_accessed = true` |
| A5 | GR2 "each MINUS_X vs FULL" vs P-B2 "F2 (or a component) strictly REDUCING critical failures" | GR2 evaluates all 7 contrasts with F2/FULL on the left (RD < 0 ⇔ the full architecture has fewer critical failures); GR3 evaluates RD(MINUS_X − FULL) lower bound ≥ +0.02 as written. Both orientations are reported for every contrast (negation-consistent by construction, same seed) |
| A6 | GR0(b) validity when a baseline collects nothing | lane-validity preconditions: the baseline suite must contain ≥ 1 passing test and the gold patch must flip ≥ 1 baseline-failing test inside the suite; a baseline with zero passing tests is `BASELINE_SUITE_NO_PASSING_TESTS` and its task is excluded with count (this guard was added after the synthetic end-to-end test exposed a vacuous zero-count pass caused by a `sys.path` defect in the unittest recorder — fixed and retested) |
| A7 | GR0(a) E60 truth vector | `component_effects.json` carries task-level paired tables only; the 600 per-evaluation `native_success` values come from the frozen campaign evaluation records, bound to in-repo anchors (arm_summaries success counts per arm and per project, component_effects success paired tables, `supersede.sha256` on the superseding rep-3 record). The E30-R11 vector comes from the in-repo raw rollup and is cross-checked bit-exactly against the 480 campaign records |
| A8 | "exact discordant tests when discordants ≤ 10" | the exact two-sided discordant test is computed for every contrast (valid at any n); a continuity-corrected asymptotic McNemar p is reported as a supplement only; Holm (families 3 and 4) is applied to the exact p |
| A9 | rep aggregation "majority over reps, as E60" vs E60's ANY_TRUE rule for critical failure | strict majority (`frozen_majority`, `None` stays in the denominator) is the gate aggregation as the design fixes; E60's ANY_TRUE aggregation is reported as a labelled non-gating sensitivity annex |
| A10 | GR0(a) ordering vs compute | GR0(a) runs as its own pre-suite array (registered test only, adapter verbatim, ≈ 8 CPU-h) so the lane is validated before the suite spends compute; the suite stage re-derives `native_success` a second time (recorded as a determinism replicate, not a gate) |
| A11 | timeouts | 900 s wall per suite (frozen), enforced with a process-group kill; compile + registered test keep the frozen lane's 10 800 s |
| A12 | "queued behind SD70 (3553181) and E70-GC1 (3553088)" | those jobs are no longer in the queue at dispatch; no SLURM dependency on them is possible. Throttle `%24` (48 cores ≈ one lu48 node-equivalent) |

## 4. Checker validation before use

- `stage gr0a` (collect) first runs a negative control on the comparator: a self-compare must be
  bit-exact, one deliberately flipped frozen entry must be reported as exactly one mismatch at that key,
  and one dropped entry as exactly one missing. The receipt records the outcome; a failing control
  invalidates the cell.
- `tests/unit/test_pc_r6_lane.py::test_main_gr0a_execute_collect_and_negative_control` additionally
  corrupts a real new-lane record and a real truth-anchor entry and asserts the collect stage returns
  FAIL with the exact offending key, then restores and re-verifies PASS.

## 5. Dispatch plan (design §8 custody)

| step | job | status |
|---|---|---|
| manifest (login node, read-only) | `--stage manifest` | `done 2026-09-02 (2858 entries: 1080 responses, 1080 frozen evaluation records, 5 gold patches, 80 workspace identities [HEAD + porcelain + deviating files], bindings, registry, adapter, truth anchors)` |
| GR0(a) execute | `pc_r6_gr0a_array.sbatch` (`--array=0-79%24`, 2 CPU, 8 G, 3 h) | **3563415** — 80/80 COMPLETED (runner v1, submitted from branch head `5d8f601` before the #141 merge; sha-identical). Collect: **e30r11 480/480, e60 600/600 bit-exact**, 0 mismatched, 0 missing; checker negative control PASS in both cells; E30 cross-check vs the 480 campaign records bit-exact; E60 anchors: 49/49 substantive checks PASS (arm_summaries counts per arm + per project, component_effects success paired tables) + supersede ledger (v2 semantics) |
| GR0(b) gold control, attempt 1 | `pc_r6_gr0b.sbatch` | **3563416** FAILED (exit 1, 54 min): ansible-1 / fastapi-1 / pandas-1 PASS (count 0 over 57 / 11 / 259 baseline-passing tests); black-1 and cookiecutter-1 non-passing → §7 |
| GR0 verify, attempt 1 | `pc_r6_gr0_verify.sbatch` | 3563417 DependencyNeverSatisfied → cancelled together with 3563418 (suite) and 3563419 (rollup); no suite compute spent |
| GR0(b) gold control, attempt 2 (runner v2) | `pc_r6_gr0b.sbatch` (2 CPU, 8 G, 4 h) | **3563624** (submitted from branch head `8f41aeb`; runner sha `4c62a32e…` verified on LUNARC) |
| GR0 verify + combine, attempt 2 | `pc_r6_gr0_verify.sbatch` `--dependency=afterok:3563624` (re-collects the 3563415 GR0(a) records under runner v2) | **3563625**; login-node pre-check of the v2 collect: GR0(a) PASS 480/480 + 600/600, supersede anchor PASS |
| suite | `pc_r6_suite_array.sbatch` (`--array=0-79%24`, 2 CPU, 8 G, 12 h) `--dependency=afterok:3563625` | **3563626** (starts only on GR0 PASS) |
| rollup | `pc_r6_rollup.sbatch` `--dependency=afterany:3563626` | **3563627** |
| analysis | `pc_r6_fullreg_analysis.py` — **not chained; not run at dispatch**; refuses without a GR0 PASS receipt | deliberate manual step after the rollup is verified complete |

Compute expectation from the frozen records: 480 + 600 registered-test evaluations took 3.4 + 4.7 CPU-h in
the frozen lane (median 3 s, max 530 s); only 95/480 and 124/600 proposals applied AND compiled, so
patched suites run for ≈ 219 evaluations (+ 80 baselines + 5 gold). Expected wall: GR0(a) ≈ 1 h,
GR0(b) ≤ 1 h (parallel), suite array ≈ 2–4 h behind the verify gate.

Logs: `/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/logs/`. Campaign dir:
`/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/campaign-pc-r6-fullreg-e30r11-e60-20260902-774903e1/`.

## 7. GR0(b) attempt-1 failure: diagnosis and re-freeze (2026-09-02)

Job 3563416 returned `{"gr0b": "FAIL"}` with two non-passing tasks; each was traced to ONE cause and only
that cause was changed. The frozen design (gates, margins, seed, families, suite definition) is untouched.

| task | observation (from `records_gr0b/`) | attribution | change |
|---|---|---|---|
| `bugsinpy-black-1` | gold applies, compiles, registered binding passes (`Ran 1 test … OK`), suite count 0 over 128 baseline-passing tests — but `newly_passing_count = 0`: inside the 129-test module run `test_works_in_mono_process_only_environment` fails both at baseline and after gold (`exit_code 1 != 0`), i.e. an order-dependent test that only passes in isolation | **lane defect in amendment A6** (my precondition "gold flips ≥ 1 baseline-failing test inside the suite" assumed the suite-level outcome tracks the registered binding; false for state-dependent unittest modules). The design's GR0(b) criterion (binding flips AND count == 0) was satisfied | **A14:** the `newly_passing ≥ 1` precondition is dropped; the `baseline_passing ≥ 1` guard stays; the registered test's outcome inside the suite (baseline and gold) is recorded as `registered_test_in_suite` and `suite_registered_test_divergence` (informational). Substrate finding **F2** below |
| `bugsinpy-cookiecutter-1` | gold applies, compiles, registered binding still FAILS: `FileNotFoundError: tests/test-generate-context/non_ascii.json`; count 0 over 10 baseline-passing tests | **substrate property, not a lane defect**: BugsInPy `bug_patch.txt` is source-only; the fixed commit `7f6804c` adds the fixture `tests/test-generate-context/non_ascii.json` (verified with `git show --name-only`), which the BugsInPy checkout never copies into the buggy tree. The gold control is therefore not applicable to this task; the frozen E30-R11 records show arms CAN pass it (SAME_MODEL_REFLECTION and SIMPLE_DIRECT 3/3 reps) because their proposals add the fixture themselves | **A13:** selection rule "one per project where available" made executable: within a project, tasks in bug_id order; a task is `GOLD_NOT_APPLICABLE_MISSING_FIXTURE:<path>` only when ALL of (patch applied, compile PASS, binding fails, output names a missing path, path absent from the frozen workspace, path added by the fixed commit) hold; then the next bug_id is tried (cookiecutter-2). Anything else remains a real FAIL. The extra gold patch read enters the gr0b read manifest (the frozen input manifest / campaign id are unchanged — no frozen proposal, workspace or anchor changed) |

Also corrected in runner v2 (found by the GR0(a) collect, not by GR0(b)): **A15** — `supersede.sha256` lists the
sha256 of the SUPERSEDED rep-3 `F2_MINUS_DECOMPOSITION/bugsinpy-scrapy-5` artifacts (preserved under the E60
campaign's `repair/superseded-r3-falsifier/`), not of the live records. The v1 anchor check compared it with
the live record and reported one false alarm (all 49 substantive E60 anchor checks passed). v2 checks that the
in-repo ledger is byte-identical to the preserved `supersede-*.sha256`, that the listed sha matches the
preserved copy, and that the live record differs from it.

Substrate findings recorded for the analysis layer (no gate change): **F1** `bugsinpy-cookiecutter-1`'s
registered failing test cannot be flipped by any source-only patch (the mean endpoint for this task measures
whether a proposal recreates the missing fixture); **F2** `bugsinpy-black-1`'s registered test is
order-dependent in the full-module run (baseline-failing in the suite → it can never be a critical new
failure; `full_regression_suite_passed` still uses the registered binding, as designed).

Reproduced by `tests/unit/test_pc_r6_lane.py::test_gr0b_order_dependent_module_and_missing_fixture_fallthrough`
(synthetic black-like order-dependent module + cookiecutter-like fixture-missing task with fall-through) and
`test_gold_not_applicable_classifier_requires_every_condition`; the supersede semantics are exercised by the
E60 truth fixture. GR0(a) reproduction (480/480 + 600/600) is unaffected: those records come from runner v1
and the comparator is unchanged.

## 6. Outputs (to be archived under `research/experiments/results/issue45/pc-r6/` when they land)

`PC_R6_INPUT_MANIFEST.{sha256,json}`, `PC_R6_GR0A_RECEIPT.json`, `PC_R6_GR0B_RECEIPT.json`,
`PC_R6_GR0_RECEIPT.json`, `PC_R6_FULLREG_RAW_ROLLUP_V1.json`, `PC_R6_READ_MANIFEST.sha256`, then (analysis)
`PC_R6_FULLREG_ROLLUP_V1.{json,md}`, `PC_R6_OUTCOME_RECEIPT.md`.

No mean-success claim may issue from this lane; no endpoint, margin, family or suite definition changes
after the first suite execution (design §7).

skills-applied: none (dispatch receipt, no manuscript content)
