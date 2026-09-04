# E30-R13 — outcome receipt

**Terminal: `INTERFACE_STILL_BROKEN`.** The campaign completed, every registered gate was
computed, and both endpoints were read. Patches still do not apply: the apply-rate
diagnostic GR1 failed on all four arms, which is the registered clause that fires first,
so E1 and E2 are reported with the measured apply rate attached and **the study does not
claim to have tested repair**.

Campaign `campaign-e30-r13-channelcontract-core4-rep3-20260903-427bfc90`, source
`b1bc039`, design `E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1` sha256 `427bfc90e03c…`,
seed revealed post-run as **20260903**. SLURM 3569288 setup → 3569289 agents → 3569290
frozen lane → 3569291 GR0a (40) → 3569292 GR0 verify → 3569293 suite (40) → 3569294
rollup and analysis; every stage `COMPLETED` with exit `0:0`, 2026-09-03 09:31:51 →
20:08:19 (10 h 36 min wall).

---

## 1. Was there anything to collect?

`COMPLETED 0:0` is a rendered status and a three-second rollup is a suspicious one, so
this was established before anything was analysed.

| question | answer | how it was established |
|---|---|---|
| did the rollup find records? | yes | `complete: true` over **40/40 baselines and 480/480 evaluation records** (160 arm-task keys × 3 repetitions, 0 missing); it wrote a 321 KB raw rollup and a 150 KB read manifest |
| was the 3-second job real? | yes | the output files span **1.27 s** of write time (20:06:25.93 → 20:06:27.20), consistent with a 3 s job over 520 small JSON reads |
| why do file times disagree with `sacct`? | clock skew, not a missing run | fs9's clock runs ≈110 s behind the compute node; the job's own `date -u` inside the log reads `18:08:19Z`, which agrees with `sacct`'s 20:08:19 CEST exactly |
| were all responses written? | yes | **480/480 envelopes, every one `COMPLETED_PROPOSAL_ONLY`, 0 non-completed**, 1080 model calls, all 480 recording served model `glm-5.3` |
| did the guard re-arm? | yes | `PROTECTED_RUN_AUTHORIZATION.json` is gone, `…_ARCHIVED.json` is present (the `mv` preserves the original 09:29:47 mtime, as expected) |

Compare E30-R12, which reached this point with 119 of 480 responses written, 116 of them
envelope failures, and 0 evaluations.

The response figures come from `e30_r13_execution_tally.py`
(`results/E30_R13_EXECUTION_TALLY_V1.json`); the reconciliation figures come from
`e30_r13_outcome_verification.py` (`results/E30_R13_OUTCOME_VERIFICATION_V1.json`, **12
checks, 12 PASS, exit 0**, verifier Python 3.11.5). Neither computes an endpoint, a
contrast or a terminal.

## 2. Why this campaign exists, and whether its gate does the job

E30-R12 terminated at `EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`. The measured cause:
on the identical frozen prompt the provider default returned `stop_reason max_tokens` at
6 000 output tokens with one 27 624-character `thinking` block and **0 text characters**;
with thinking disabled, `end_turn`, 775 tokens, text present. The arm reads only `text`
blocks. Same task, same arm, byte-identical prompt (`input_tokens` 61 557 both), five
days apart: **R11 completed at 763 output tokens in 12.5 s; R12 hit the cap in 71.0 s and
failed.**

**The central finding R13 exists to gate against: pinning a served model id does not pin
an experimental condition.** All 119 of R12's envelopes recorded the correct served id
and its served-model gate held on every one of them. The drift was in channel *behaviour*
at a *fixed* served id, and no registered gate in the programme observed it.

R13 registers the request body by sha256 over its bytes, records the configuration per
envelope, and gates over it with GR0d and GR0e. Four things were checked, not assumed:

**(a) The gates hold across the full run, not just an early sample.** GR0d: 480/480
envelopes carry a channel receipt, 1080/1080 calls report a contract, one distinct
contract sha256 (`3312fc45…`), 0 offenders. GR0e: 480/480 receipts, stop reasons
`{end_turn: 480}`, 0 zero-text calls, 0 offenders. Both recomputed independently from the
envelopes on disk and both reproduce the published values exactly (check `V1`).

**(b) Replayed over E30-R12's archive, the gates do not pass — they refuse.** R13's own
GR0d and GR0e predicates were run read-only over R12's 119 written envelopes. **0 of them
carry a channel receipt**, so both gates return `COULD_NOT_CHECK` and the registered
precedence routes to `EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ` — which is precisely the
terminal R12 actually reached. The gate does not silently pass an unreceipted campaign
(check `V2`). This is the honest form of "would it have caught R12": it halts, and
`COULD_NOT_CHECK` is a distinct status from `PASS`, never reportable as a null or an
equivalence.

**(c) The predicates can fire.** A gate that has never been shown to fail is a gate whose
`0 offenders` means nothing. Fed 40 envelopes carrying R12's measured signature —
`stop_reason max_tokens` at the cap, zero text characters — GR0e returns **FAIL with 80
offenders**, one truncation and one zero-text offence each. Rewritten with `end_turn` and
text present, the same 40 return **PASS with 0 offenders**: the gate does not cry wolf.
One envelope given a different contract digest makes GR0d **FAIL with 1 offender over 2
distinct digests** — the R12 drift mode itself (checks `V3`, `V3b`, `V3c`). Note that the
offender *list* is capped at 50 entries while the *count* is not; the listed reasons sum
to 50, the count to 80.

**(d) What GR0d actually observes, precisely.** The expected digest is re-derived at
rollup time from the same `channel_contract_sha256()` the arms used, deliberately, so no
digest is hand-typed. The consequence is that GR0d detects **heterogeneity across
envelopes — the R12 drift mode — not whether the registered contract was the right one to
register.** That second question is answered by the pre-freeze calibration contrast
(`channel_condition_contrast_measured_pre_freeze`), not by this gate.

**(e) What R12 could not have seen about itself.** Of R12's 119 envelopes, **116 sat at
or above its 6 000-token cap and 116 carry `EXECUTION_FAILED_MODEL_RESPONSE`; 119 of 119
carry no `stop_reasons` field at all.** R12's receipts could not express its own failure
mode. Token counts are a proxy here and are labelled as one.

## 3. Endpoints

Registered arithmetic imported verbatim from `e30_r12_analysis.py` under a sha256 pin
(`056996ebfea1…`). 10 000 bootstrap draws, PROJECT-stratified, two independent Holm
families of three, one per endpoint, no imputation.

| arm | E1 fixed / checkable | E1 rate | E2 any-critical / checkable | D1 apply rate | D1 apply-fail | PC-R6 comparator |
|---|---|---|---|---|---|---|
| `F2_ORION_METABOLIC_FULL` | 10/40 | 0.250 | 0/11 | 0.3083 | 0.6917 | 0.8167 |
| `SIMPLE_DIRECT` | 7/40 | 0.175 | 1/12 | 0.2833 | 0.7167 | 0.7833 |
| `F0_PARENT_FEDERATION` | 6/40 | 0.150 | 1/11 | 0.3083 | 0.6917 | 0.8000 |
| `SAME_MODEL_REFLECTION` | 4/40 | 0.100 | 0/6 | 0.2167 | 0.7833 | 0.8083 |

**E1 — registered failing test fixed (primary), n = 40.**

| contrast | discordant (L-only/R-only) | RD [CI95] | exact p | Holm p | reject |
|---|---|---|---|---|---|
| F2 − F0_PARENT_FEDERATION | 5/1 | 0.1000 [0.0000, 0.2000] | 0.2188 | 0.4375 | no |
| F2 − SIMPLE_DIRECT | 5/2 | 0.0750 [−0.0250, 0.1750] | 0.4531 | 0.4531 | no |
| F2 − SAME_MODEL_REFLECTION | 6/0 | 0.1500 [0.0500, 0.2500] | 0.0312 | 0.0938 | no |

The sensitivity denominator (39 tasks, excluding `bugsinpy-cookiecutter-1` under
`REGISTERED_TEST_UNFIXABLE_BY_SOURCE_ONLY_PATCH`) moves no decision: 0.1026 / 0.0769 /
0.1538, same p values, no rejection.

**E2 — any critical new failure (co-primary), n = 38** after excluding
`bugsinpy-ansible-4` and `bugsinpy-fastapi-3` with count under
`BASELINE_SUITE_NO_PASSING_TESTS`. Paired contrasts resolve on 8, 9 and 6 tasks
respectively; RD −0.1250, −0.1111 and 0.0000, no rejection.

**The E2 denominator is a count of tasks, not of evaluations.** 11 / 11 / 6 / 12 tasks
resolve by majority over three repetitions, against 35 / 33 / 23 / 32 *countable
evaluations* out of 120 per arm. Those are different quantities and the second does not
divide by three; the receipt quotes the first because that is what the endpoint uses
(check `V6`).

## 4. Gates

| gate | status | what it observed |
|---|---|---|
| GR0c SERVED_MODEL_HOMOGENEITY | **PASS** | 480 envelopes, `{glm-5.3: 480}`, 0 offenders |
| GR0d CHANNEL_CONTRACT_HOMOGENEITY | **PASS** | 480/480 receipts, 1080/1080 calls report a contract, 1 distinct sha256, 0 offenders |
| GR0e CHANNEL_BEHAVIOUR_CONFORMANCE | **PASS** | 480/480 receipts, `{end_turn: 480}`, 0 zero-text calls, peak 13 885 output tokens, 0 offenders |
| GR1 APPLY_RATE_DIAGNOSTIC | **FAIL** | apply-failure 0.6917–0.7833 on every arm against the registered 0.40 ceiling; below the PC-R6 comparator on all four, but the ceiling is the binding clause |
| GR2 PRIMARY_SEPARATION | **NULL** | no E1 contrast rejects after Holm |
| GR3 CRITICAL_NON_INFERIORITY | **PASS**, and not informative | see below |

**GR3's PASS carries no information at the denominator it got.** n = 8 paired tasks, so
the smallest risk difference the table can express is 1/8 = 0.1250 — **6.2× coarser than
the registered 0.02 margin**. No achievable outcome at this n separates non-inferiority
within 0.02 from a 12.5-point regression. The observed one-sided upper bound of *exactly*
0.0000 is the tell. The gate status is real; treating it as evidence of critical-failure
safety would not be (check `V7`).

**The terminal is the first firing registered clause, verified against the design, not
asserted.** Registered precedence: channel terminals → `LANE_DEFECT` → `F2_HARMFUL` →
`CRITICAL_REGRESSION` → **`INTERFACE_STILL_BROKEN`** → `FIRST_REGISTERED_POSITIVE` →
`PARENT_SUFFICIENT` → `NO_ARM_SEPARATION`. GR1's failure fires ahead of both
`PARENT_SUFFICIENT` and `NO_ARM_SEPARATION`, so **neither was reachable in this run**.
Counterfactually, had GR1 passed, F0's E1 rate (0.150) sits below F2's (0.250), so
`PARENT_SUFFICIENT` would still not have fired and the terminal would have been
`NO_ARM_SEPARATION` (check `V8`).

## 5. What the run cost, and where the budget actually landed

The registered per-call cap is 14 000, derived as `1000 × ceil(4 × 3292 / 1000)` from 108
calibration calls whose largest was 3 292 output tokens, and intended to be non-binding.

**It was non-binding by 115 tokens.** The largest single call in the campaign used
**13 885 output tokens — 99.18 % of the cap, and 4.22× the calibration maximum the 4×
rule was built on.** All 480 envelopes still closed at `end_turn`, so GR0e's PASS is
genuine and no call was truncated.

The tail that nearly bound is thin, and that is the point. Across the 480 envelopes the
largest single call has median 1 287.5 tokens and p90 6 850; the maximum is **10.8× the
median**. Only **2 of 480** envelopes carry a call above 13 000 and exactly **1 of 480**
reaches 13 885. An in-flight check over 15 envelopes therefore had a **6.2 % chance of
containing either near-cap envelope and a 3.1 % chance of containing the binding one** —
so an early sample reporting comfortable headroom was the overwhelmingly likely outcome
whether or not the headroom was real. (An in-flight check during this campaign did report
a largest single call of 6 741 tokens. That figure has **no archived artifact in this
repository** and is recorded here as the unarchived in-flight observation it was, not as
evidence; the distribution above is the evidence, and 49 of 480 envelopes exceed 6 741 in
the completed run.) An early check is not the run.

The near-cap calls sit in the arms that make *fewer, larger* calls: per-arm peaks are
13 885 (`SAME_MODEL_REFLECTION`, 2 calls/envelope) and 13 529 (`SIMPLE_DIRECT`, 1), against
12 727 (`F0_PARENT_FEDERATION`, 3) and 12 662 (`F2_ORION_METABOLIC_FULL`, 3).

**The per-arm channel load matches the registered execution-lane contract exactly**:
360 / 360 / 240 / 120 calls over 120 envelopes each, i.e. 3 / 3 / 2 / 1 per
task-repetition, summing to the registered 1 080. This breakdown is recorded because GR0d
and GR0e aggregate over all 1 080 calls and neither would notice arms that had collapsed
onto the same load (check `V4`).

Cost and time: 49.5 M input tokens, 1.70 M output tokens, **10.51 serial wall hours over
1 080 calls = 35.04 s/call**, against the registered feasibility estimate of 20.33 s/call.
The estimate was optimistic by 72 %, and the campaign still fitted its allocation
comfortably (agents job 7 h 09 m against a 24 h limit) — the margin was real, the point
estimate was not. Under the provider default at R12's escalated budget the same 1 080
calls were projected at 785.81 s/call and 235.7 serial hours, which fits in no single
allocation at any concurrency this lane uses.

The agents stage ran five resumption passes with pending counts 480 → 178 → 17 → 3 → 0,
re-dispatching only `EXECUTION_FAILED_MODEL_RESPONSE` envelopes as the registered
resumability clause permits. **No completed response was re-rolled**, and the final tally
is 480 `COMPLETED_PROPOSAL_ONLY` with 0 failures.

`F2_ORION_METABOLIC_FULL` and `F0_PARENT_FEDERATION` both applied on exactly 37 of 120
slots. That equality is a coincidence, not shared state: the two sets of applying
(repetition, task) slots overlap on 25 and are distinct (check `V5`). Equal cardinality
alone would not have distinguished the two.

## 6. Registered facts, carried verbatim

- **At n = 40 the exact test cannot reject unless at least 7 tasks are discordant in the
  same direction — a risk difference of 0.175 — at ANY effect size.** Power against the
  registered 5-percentage-point minimum important difference is **1–2 %**. 80 % power at
  5 pp needs **430 / 863 / 1287 / 1708** tasks at ψ = 0.10 / 0.20 / 0.30 / 0.40. The
  pinned commit holds **501** numeric bugs in total and **295** within the 8 registered
  projects. **n did not change: E1 ran at the registered denominator of 40**, so this
  arithmetic stands unaltered.
- **This is an estimation and diagnostic study. A non-rejection is NOT evidence of
  equivalence.**
- **E30-R11's served model stays INFERRED, NOT VERIFIED** — its envelopes record no served
  id, and it ran under no registered request-body contract — so any comparison of R13 to
  R11 is **descriptive only**, twice over. **R13 versus R12 is not a comparison at all**:
  R12 read no endpoint.
- **`PARENT_SUFFICIENT` and `NO_ARM_SEPARATION` are registered, legitimate terminals with
  explicit precedence.** Neither fired here because GR1 preempts both. If the arms do not
  separate once patches actually apply, that is reported as plainly as a positive would
  be.

## 7. What this receipt does not do

It does not revise, re-score or reinterpret E30-R11's, E60's, PC-R6's or E30-R12's
endpoints, all of which stay frozen terminal. It changes no design, gate, endpoint,
margin, family, disposition or budget — the freeze is the freeze, and every artifact here
was produced by code frozen before dispatch. It grants no scientific-truth, field-status,
supertheory or publication-readiness authority. It claims no repair of the patch
interface: GR1 failed, and the apply rate is attached to every endpoint number above for
that reason.

## 8. Provenance

| artifact | what it is |
|---|---|
| `results/E30_R13_OUTCOME_ROLLUP_V1.json` / `.md` | the frozen analysis output, byte-identical to the campaign copy |
| `results/E30_R13_EXECUTION_TALLY_V1.json` | descriptive transcription of the 480 envelopes; no endpoint, contrast or gate |
| `results/E30_R13_OUTCOME_VERIFICATION_V1.json` | 12 reconciliation and non-vacuity checks, 12 PASS, exit 0 |
| `results/E30_R13_GR0_RECEIPT_V1.json`, `…GR0A…`, `…GR0B…` | evaluator-lane validity receipts; GR0a reproduced 480/480 bit-exact and detected its own seeded dropped and flipped records |
| `results/E30_R13_RUN_IDENTITY_V1.json`, `…JOB_IDS_V1.env` | campaign identity, anchor sha, and the SLURM chain |
| `e30_r13_outcome_verification.py` | the verifier; `PASS` / `FAIL` / `COULD_NOT_CHECK` are distinct statuses with distinct exit codes 0 / 4 / 5, and it refuses to run below Python 3.11 |
