# SD70-V2 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Design:** `SD70_V2_EXECUTION_DESIGN_V1.{md,json}` (this PR); design JSON sha256
`96d933e00cbc8d09222fd4e86e27d1fe8604164521aea1feedd483ddcbd28bf4`.
**Status:** development fixtures only. **No protected task has been generated and no protected
outcome inspected.** The protected seed lives only in `~/.orion-custody/sd70-v2/` (sha256
`4343cdae9fd451f5f4ca23e7a6bb33796deeb6e6d7f355e0a3a6e281bef3b51e`); `prepare` refuses any other seed.
**Run:** Mac (local), 2026-09-02, CPython 3.13, `python3 sd70v2_run.py selftest` (9 s) then
`dev --seeds 3 --tasks 200` (25 s); deterministic, byte-identical across re-runs.

## 1. Frozen code (sha256)

| file | sha256 |
|---|---|
| `sd70v2_generator.py` | `6163a3658349e416246a2331fe7a381f42104d132f32bbad168d5ad2fde1a56a` |
| `sd70v2_parents.py` | `5883fae4c8fb5ddd13970037d76c67dc850c1ce97b332b8180ce969358365808` |
| `sd70v2_stats.py` | `5c20d2a05868abc02c48c2b895f37bb38d37e897a2e3204eae45d167a239515c` |
| `sd70v2_model_arm.py` | `17e9dd812f8ae2afd0e1bcc76fc3d0d639430e342e9a141a7ca9154eae954349` |
| `sd70v2_run.py` | `aa6faf35608b156b624f366dcc873a9e45a067adbdfbcecad1643da00328c1db` |
| `SD70_V2_EXECUTION_DESIGN_V1.json` | `96d933e00cbc8d09222fd4e86e27d1fe8604164521aea1feedd483ddcbd28bf4` |
| `results/SD70_V2_DEVELOPMENT_RESULTS_V1.json` | `fa98de121ac4423b033145d764fb460c66153eda419878f762d1f8add8467cc2` |
| `results/SD70_V2_SELFTEST_V1.json` | `b110e7b60281783afe3110c862db1ea8597f2f8ba3106fe3ac0db4af919a50ec` |

## 2. Parent fidelity: native known-answer tests (29/29 PASS)

Every comparator passed its own native tests before use (`sd70v2_parents.fidelity_selftests`,
executed by `selftest` and by `tests/unit/test_sd70_v2_execution.py`).

| parent | passed | tests |
|---|---|---|
| SIMPLE_FREQUENCY_PARENT | 5/5 | planted majority act-y; empty evidence -> first candidate; same fixture: frequency picks act-x (separation); label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| MATCHED_CASE_PARENT | 3/3 | identical context wins over global frequency; label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| NAIVE_BAYES_PARENT | 4/4 | planted indicator feature -> act-a; planted indicator feature -> act-b; label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| DECISION_LIST_PARENT | 4/4 | recovers planted 3-rule decision list on every context; first induced rule is a single literal on ctx-0 -> act-a; label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| PERCEPTRON_PARENT | 3/3 | reproduces planted linear argmax rule when all contexts are observed (training consistency); label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| MAXMARGIN_PARENT | 3/3 | reproduces planted linear argmax rule when all contexts are observed (training consistency); label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| PAIRWISE_LINEAR_PARENT | 3/3 | reproduces planted linear argmax rule on >= 97% of observed contexts (pairwise-vote cycle boundary); label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| FIXED_META_LESSON | 2/2 | label-permuted (candidate bijection) planted data stays within +0.12 of chance; no evidence -> first candidate (frozen tie break) |
| TARGET_ONLY_DETERMINISTIC | 1/1 | no evidence -> first candidate (frozen tie break) |
| F0_PARENT_FEDERATION | 1/1 | returns a candidate and records every member pick |

Documented boundaries: the pairwise-vote parent can cycle (Condorcet), so its planted-rule test
requires >= 97% rather than exact reproduction (observed 154/155); the frequency, matched-case and
fixed-lesson scorers are not equivariant learners in the strict sense but their label-permutation
nulls still sit at chance (table below).

## 3. Development split (3 seeds x 200 tasks = 600 tasks; chance 0.262) — DEVELOPMENT, not protected

| arm | exact | Wilson 95% | CFD rate | LP control | QS control | wall s |
|---|---|---|---|---|---|---|
| SIMPLE_FREQUENCY_PARENT | 0.570 | [0.530, 0.609] | 0.112 | 0.277 | 0.258 | 0.01 |
| MATCHED_CASE_PARENT | 0.613 | [0.574, 0.651] | 0.090 | 0.277 | 0.252 | 0.01 |
| NAIVE_BAYES_PARENT | 0.645 | [0.606, 0.682] | 0.072 | 0.262 | 0.250 | 0.02 |
| DECISION_LIST_PARENT | 0.653 | [0.614, 0.690] | 0.060 | 0.255 | 0.258 | 0.25 |
| PERCEPTRON_PARENT | 0.698 | [0.660, 0.734] | 0.045 | 0.257 | 0.258 | 1.42 |
| MAXMARGIN_PARENT | 0.720 | [0.683, 0.754] | 0.037 | 0.252 | 0.248 | 3.94 |
| PAIRWISE_LINEAR_PARENT | 0.687 | [0.648, 0.722] | 0.047 | 0.260 | 0.263 | 0.60 |
| FIXED_META_LESSON | 0.633 | [0.594, 0.671] | 0.070 | 0.270 | 0.247 | 0.01 |
| F0_PARENT_FEDERATION | 0.708 | [0.671, 0.743] | 0.045 | nan | nan | 0.00 |
| TARGET_ONLY_DETERMINISTIC | 0.298 | [0.263, 0.336] | 0.312 | 0.298 | 0.355 | 0.00 |

**Strongest generator-faithful parent (frozen rule: highest development exact accuracy among the
five faithful candidates; tie -> lower wall time): `MAXMARGIN_PARENT`.** Ranking:
MAXMARGIN_PARENT > PERCEPTRON_PARENT > PAIRWISE_LINEAR_PARENT > DECISION_LIST_PARENT > NAIVE_BAYES_PARENT. Strongest vs second (PERCEPTRON_PARENT):
discordance 0.118, paired delta +0.022
[-0.005, +0.048] (b/c = 42/29). F0 federation
(0.708) does not beat its strongest member; the
frozen comparator is the strongest parent as the protocol prescribes.

Negative controls on development: label permutation (candidate bijection) puts every parent at
0.20–0.28 against chance 0.262; query-to-task shuffle at 0.25–0.26. TARGET_ONLY_DETERMINISTIC
(first candidate) sits at 0.298 on protected-like tasks and 0.355 on QS, showing the shared
low-index tie-break bias the control tolerance (0.05 on the Wilson lower bound) absorbs.

## 4. Power and budget (frozen in the design JSON)

delta_min 0.10, assumed discordance 0.30 (development top-two discordance 0.118), alpha 0.025
one-sided worst case under Holm, power 0.80 -> 234 tasks; **N = 240** (power 0.811 at 0.30,
0.748 at 0.35). Model calls 240 x 4 + 3 x 60 = 1 140, one per arm-task, timeout 600 s,
at most one bounded rerun, concurrency <= 2. At the 25–65 s per call observed on the E70-GC1
pilot this is 8–20 wall-hours on a LUNARC lu48 node (2 CPUs, 8 GB).

## 5. Unit tests (18 passed)

`tests/unit/test_sd70_v2_execution.py` exercises `main()` on development fixtures with stub
model processes: the strongest parent recovers the planted policy (>= chance + 0.25) and sits at
chance under the label-permutation null; the V2 generator reproduces V1 public tasks
byte-for-byte; target-only surfaces carry no training token; sanitized manifests hash-match the
files; a federation-copying solver routes PARENT_SUFFICIENT with the oracle absent and the public
pool and requests unreadable from inside the child; a planted perfect solver routes
PROSPECTIVE_META_POLICY_RESIDUAL with every gate true; a failing solver is scored as failure and
routes CANNOT_CHECK with one bounded rerun then no further attempts; wrong protected seed,
tampered design and missing response are refused.

## 5b. Post-freeze implementation fix (outcome-blind)

A live probe on the execution host showed the Codex CLI reading additional
prompt input from an inherited non-tty stdin, which would have hung every model
call to its 600 s timeout. Both subprocess launches now pass
`stdin=subprocess.DEVNULL`. This is an execution-fidelity fix: no arm, surface,
outcome, threshold, gate, terminal or task distribution changed. Hashes above are
post-fix.

## 6. Authority

Development numbers are development numbers. Nothing here grants field status, novelty, or
publication authority. `PARENT_SUFFICIENT` is the pre-registered expectation and a successful
terminal; the frozen gates, not this receipt, decide the protected route.
