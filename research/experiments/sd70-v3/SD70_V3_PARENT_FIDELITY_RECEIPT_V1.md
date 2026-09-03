# SD70-V3 — Parent Fidelity and Freeze Receipt (V1)

Frozen before any protected task was generated and before any protected outcome existed.

## Design freeze

| artifact | sha256 |
|---|---|
| `SD70_V3_EXECUTION_DESIGN_V1.json` | `7c62d291ddd5cbc18e3fb9f368290050b2aee27379b4c535724ca3d7f87d32ee` |
| `SD70_V3_EXECUTION_DESIGN_V1.md` | `54de620a022056353d063b5cdd5e28700858c581c9d593c357e9f2421426639a` |

Protected seed sha256 (seed itself never in the repository, never on the dispatch host): `d032efa9a570c5baa8fb7b5d86d3d879f3fd087adfb3088459fc68aee6d150cc`  
Committed at 2026-09-03T05:46:41.374388+00:00; custody `~/.orion-custody/sd70-v3/SD70_V3_MASTER_SEED.txt` (Mac, mode 600).

## Code hashes

| file | sha256 | lines |
|---|---|---|
| `sd70v3_generator.py` | `4cbc36d1cafbf7605655590c9c703d461b7a185d22dff08b7a8531d94f8a5f0c` | 321 |
| `sd70v3_parents.py` | `e7cc1efe384245579be5cb31c2a67d379fbbfdd789df43e8d3fedcfdd4774309` | 565 |
| `sd70v3_stats.py` | `d3b7777f166760f7a99e7598c3727dca72898a853b36018ecd123f31a0ed9f79` | 118 |
| `sd70v3_model_arm.py` | `312f9ea19ca161f41ffd8f8c9c6cf1103bbcf99d540b96d2e8b5a0066d976ae8` | 282 |
| `sd70v3_channel.py` | `8980eceeb0f6462f8bed9b83e4a60e9a55b3f54b17eb30829abe6996b0f28ae0` | 225 |
| `sd70v3_run.py` | `b217ce6ab181d928d74d4ad784b1236fdbf5900efe9533d905f103e3881fc7f9` | 930 |
| `sd70v3_remote_dispatch.py` | `a1409610fdea8dfcfde4a4e3774d9194b28558b46d356f2b9f7c98ec32b23c58` | 153 |

Interpreter pinned for generation, deterministic arms and evaluation: **CPython 3.13.12** (`/Users/billy/miniforge3/bin/python3`).

## Native parent known-answer tests

`sd70v3_run.py selftest`: **29 passed, 0 failed** (denominator 29).

| test | passed |
|---|---|
| planted majority act-y | True |
| empty evidence -> first candidate | True |
| identical context wins over global frequency | True |
| same fixture: frequency picks act-x (separation) | True |
| planted indicator feature -> act-a | True |
| planted indicator feature -> act-b | True |
| recovers planted 3-rule decision list on every context | True |
| first induced rule is a single literal on ctx-0 -> act-a | True |
| reproduces planted linear argmax rule when all contexts are observed (training consistency) | True |
| reproduces planted linear argmax rule when all contexts are observed (training consistency) | True |
| reproduces planted linear argmax rule on >= 97% of observed contexts (pairwise-vote cycle boundary) | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| label-permuted (candidate bijection) planted data stays within +0.12 of chance | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| no evidence -> first candidate (frozen tie break) | True |
| returns a candidate and records every member pick | True |

## Development split (V3 seeds, protected outcomes never inspected)

3 seeds x 200 tasks = 600 tasks; seeds `sha256("SD70-V3-DEV|k")`, k = 0,1,2. Chance level 0.2629.

| arm | exact accuracy | LP control | QS control | CFD rate |
|---|---|---|---|---|
| MAXMARGIN_PARENT | 0.6783 | 0.2683 | 0.2517 | 0.0500 |
| F0_PARENT_FEDERATION | 0.6633 | - | - | 0.0517 |
| PAIRWISE_LINEAR_PARENT | 0.6567 | 0.2783 | 0.2650 | 0.0533 |
| PERCEPTRON_PARENT | 0.6567 | 0.2650 | 0.2500 | 0.0633 |
| DECISION_LIST_PARENT | 0.6283 | 0.2767 | 0.2583 | 0.0833 |
| NAIVE_BAYES_PARENT | 0.6183 | 0.2617 | 0.2533 | 0.0917 |
| FIXED_META_LESSON | 0.6133 | 0.2667 | 0.2583 | 0.0783 |
| MATCHED_CASE_PARENT | 0.6117 | 0.2717 | 0.2583 | 0.0817 |
| SIMPLE_FREQUENCY_PARENT | 0.5633 | 0.2600 | 0.2783 | 0.1217 |
| TARGET_ONLY_DETERMINISTIC | 0.3433 | 0.3433 | 0.4000 | 0.2900 |

**Selection (frozen before protected generation):** highest mean development exact accuracy among GENERATOR_FAITHFUL_CANDIDATES; tie -> lower wall time → **MAXMARGIN_PARENT**. Ranking: MAXMARGIN_PARENT > PAIRWISE_LINEAR_PARENT > PERCEPTRON_PARENT > DECISION_LIST_PARENT > NAIVE_BAYES_PARENT. Second candidate PAIRWISE_LINEAR_PARENT; strongest-vs-second discordance 0.1483.

**Comparator (frozen):** max(strongest parent, F0 federation) on development = MAXMARGIN_PARENT (0.6783) over F0 (0.6633).

Every LP and QS control sits at chance (0.25-0.28 against 0.2629), so the control machinery and the evaluator are valid on development data.

## Gate validation before freeze (both directions)

Every gate added over V2 was validated on real data in a development rehearsal, in the clean
direction **and** the broken direction. A gate validated only on the failing case is how a checker
ends up crying wolf on its first protected run.

| gate | clean case | broken case |
|---|---|---|
| arm divergence | passed on 8 development tasks: all 3 contrasted pairs differ on 8/8 requests and 8/8 prompts | fired when the no-federation ablation's requests were overwritten with the full arm's (8/8 violations reported with denominator 8) |
| positive control on divergence | full arm carries `parent_advisory` on 8/8 and FAILURE episodes on 8/8, so the two absence checks are not vacuous | — |
| channel contract | `CHANNEL_CONTRACT_OK` over real start/end measurements, all 8 checks with non-zero denominators (12, 12, 12, 12, 12, 12, 9, 3) | unit tests drive `CHANNEL_DRIFT_DETECTED` (comp_hash change, slug-list change, E30-R12-style +5,970 reasoning-token blowup), `CHANNEL_CONTRACT_UNOBSERVABLE` (manifest not scrapeable), `CHANNEL_CANARY_DISPATCH_FAILED` |
| no-cry-wolf assertion | the full calibrated jitter (input 13,593 → 14,875; output 31 → 49; reasoning 0 → 16) is asserted to stay `CHANNEL_CONTRACT_OK` | — |
| envelope homogeneity | `CHANNEL_CONTRACT_OK` over 56 real envelopes: usage observed 56/56, residual within tolerance 56/56, reasoning-cap exceedances 0/56, comp_hash mismatches 0 of 56 observable | the first drafted band would have failed 56/56 and was replaced before freezing |

Unit tests: `tests/unit/test_sd70_v3_channel_gates.py`, 17 tests, all passing under the pinned
interpreter, alongside the untouched V2 suites (33 tests total, 0 failures).

## Relationship to SD70-V2

SD70-V2's files are **not modified by this work** (`git status` over `research/experiments/sd70-v2/`
and `research/experiments/results/issue50/sd70/` reports zero changed paths). V2 keeps its frozen
artifacts, its sealed seed, its single-run authorization and its `EXECUTION_BLOCKED_PRE_DISPATCH`
state; it remains prospective with zero protected observations and its `PARENT_SUFFICIENT`
expectation **unobserved**. V3 carries its own seed, its own design freeze and its own run
authorization. The generator, parents and statistics are **copied, not imported**, so V3's freeze
does not depend on V2's files and cannot perturb them.

## Authority

This receipt grants nothing: no scientific truth, no causal law, no field status, no submission or
publication readiness.
