# E30-R13 rollup (V1)

Analysis `orion.v2.e30-r13-analysis.v1` over rollup `9351b4b8e72f…` (GR0 receipt `a16724cf9371…`, design `427bfc90e03c…`, generated 2026-09-03T18:08:19.820185+00:00).

Endpoint arithmetic imported verbatim from `e30_r12_analysis.py` (sha256 `056996ebfea1…`). Seed 20260903; bootstrap 10000 draws, PROJECT-stratified; two independent Holm families of three, one per endpoint. No imputation.

## Per-arm endpoints and the apply-rate diagnostic

| arm | E1 success / checkable | E1 rate | E2 any-critical / checkable | D1 apply rate | D1 apply-fail | PC-R6 comparator |
|---|---|---|---|---|---|---|
| `F2_ORION_METABOLIC_FULL` | 10/40 | 0.250 | 0/11 | 0.3083 | 0.6917 | 0.8167 |
| `F0_PARENT_FEDERATION` | 6/40 | 0.150 | 1/11 | 0.3083 | 0.6917 | 0.8000 |
| `SIMPLE_DIRECT` | 7/40 | 0.175 | 1/12 | 0.2833 | 0.7167 | 0.7833 |
| `SAME_MODEL_REFLECTION` | 4/40 | 0.100 | 0/6 | 0.2167 | 0.7833 | 0.8083 |

## E1 — registered failing test fixed (primary)

| contrast | paired (bothF/bothT/L-only/R-only) | checkable | RD [CI95] | exact p | Holm p | reject |
|---|---|---|---|---|---|---|
| F2_ORION_METABOLIC_FULL − F0_PARENT_FEDERATION | 29/5/5/1 | 40 | 0.1000 [0.0000, 0.2000] | 0.2188 | 0.4375 | no |
| F2_ORION_METABOLIC_FULL − SIMPLE_DIRECT | 28/5/5/2 | 40 | 0.0750 [-0.0250, 0.1750] | 0.4531 | 0.4531 | no |
| F2_ORION_METABOLIC_FULL − SAME_MODEL_REFLECTION | 30/4/6/0 | 40 | 0.1500 [0.0500, 0.2500] | 0.0312 | 0.0938 | no |

## E1 — sensitivity denominator (39 tasks, excluding ['bugsinpy-cookiecutter-1'])

| contrast | paired (bothF/bothT/L-only/R-only) | checkable | RD [CI95] | exact p | Holm p | reject |
|---|---|---|---|---|---|---|
| F2_ORION_METABOLIC_FULL − F0_PARENT_FEDERATION | 28/5/5/1 | 39 | 0.1026 [0.0000, 0.2051] | 0.2188 | 0.4375 | no |
| F2_ORION_METABOLIC_FULL − SIMPLE_DIRECT | 27/5/5/2 | 39 | 0.0769 [-0.0256, 0.1795] | 0.4531 | 0.4531 | no |
| F2_ORION_METABOLIC_FULL − SAME_MODEL_REFLECTION | 29/4/6/0 | 39 | 0.1538 [0.0513, 0.2564] | 0.0312 | 0.0938 | no |

## E2 — any critical new failure (co-primary)

| contrast | paired (bothF/bothT/L-only/R-only) | checkable | RD [CI95] | exact p | Holm p | reject |
|---|---|---|---|---|---|---|
| F2_ORION_METABOLIC_FULL − F0_PARENT_FEDERATION | 7/0/0/1 | 8 | -0.1250 [-0.3750, 0.0000] | 1.0000 | 1.0000 | no |
| F2_ORION_METABOLIC_FULL − SIMPLE_DIRECT | 8/0/0/1 | 9 | -0.1111 [-0.3333, 0.0000] | 1.0000 | 1.0000 | no |
| F2_ORION_METABOLIC_FULL − SAME_MODEL_REFLECTION | 6/0/0/0 | 6 | 0.0000 [0.0000, 0.0000] | — | — | no |

## Channel gates (E30-R13's addition; denominators published)

| gate | status | denominators | detail |
|---|---|---|---|
| GR0d CHANNEL_CONTRACT_HOMOGENEITY | **PASS** | 480/480 envelopes carry a receipt; 1080/1080 calls report a contract | distinct contract sha256s: {'3312fc45f376f09feab984bb6ffe9f1dfadc5cfbb201288dc32e1ab7b50ba2ab': 480}; offenders 0 |
| GR0e CHANNEL_BEHAVIOUR_CONFORMANCE | **PASS** | 480/480 envelopes carry a receipt; 1080 calls checked | stop reasons {'end_turn': 480}; max output tokens 13885; offenders 0 |

`COULD_NOT_CHECK` is a distinct status from `PASS` and routes to `EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`, not to a null.

## Registered gates (imported from E30-R12)

| gate | status | detail |
|---|---|---|
| GR0c SERVED_MODEL_HOMOGENEITY | **PASS** | 480 envelopes, 0 offenders, ids {'glm-5.3': 480} |
| GR1 APPLY_RATE_DIAGNOSTIC | **FAIL** | all arms below 0.4 apply-fail and below the PC-R6 comparator: False |
| GR2 PRIMARY_SEPARATION | **NULL** | rejected: none |
| GR3 CRITICAL_NON_INFERIORITY | **PASS** | RD=-0.1250, upper=0.0000, n=8, margin 0.02 |

## Dispositions applied (registered pre-dispatch)

- E2 excluded with count under `BASELINE_SUITE_NO_PASSING_TESTS`: ['bugsinpy-ansible-4', 'bugsinpy-fastapi-3']
- E1 denominator 40; E1 sensitivity denominator 39; E2 denominator 38

## Pre-registered routing

**INTERFACE_STILL_BROKEN** — emission-side canonicalization did not materially raise the apply rate; E1/E2 are reported with the measured apply rate attached and the study does not claim to have tested repair

## Power boundary (registered pre-dispatch)

At n = 40 the exact test cannot reject unless at least 7 tasks are discordant in the same direction (risk difference ≥ 0.175). Power against the registered 5-percentage-point minimum important difference is 1–2%. A non-rejection here is NOT evidence of equivalence.

## Comparison to earlier runs

E30-R11 recorded no served model id and ran under no registered request-body contract, so **any R13-vs-R11 comparison is descriptive only** — twice over. E30-R12 read no endpoint at all, so there is nothing to compare R13 with.

