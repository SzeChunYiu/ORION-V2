# SD70-V3 — Synthetic Recursive Meta-Policy Study on a Runnable Model: Frozen Execution Design (V1)

**Protocol served:** `research/experiments/SCIENTIFIC_DEVELOPMENT_SD70_PROSPECTIVE_PROTOCOL_V2.json`
(`ORION-SD70-SYNTHETIC-META-POLICY-V2`, issue #50).
**Companion files:** `SD70_V3_EXECUTION_DESIGN_V1.json` (every constant below; its sha256 is bound
into every frozen suite), `SD70_V3_PARENT_FIDELITY_RECEIPT_V1.md` (code hashes, native parent
tests, development split), `results/SD70_V3_DEVELOPMENT_RESULTS_V1.json`, `provenance/`.
**Status at freeze:** no protected task generated, no protected outcome inspected. The protected
seed exists only at `~/.orion-custody/sd70-v3/SD70_V3_MASTER_SEED.txt` (Mac, mode 600); its
sha256 is published in the JSON and `prepare` refuses any other seed.

## 0. Why this version exists — and what it does not touch

SD70-V2 is **blocked, not refuted**. Three commitments cannot all hold at once:

1. V2's design §5 pins the model `gpt-5.6-terra`;
2. the standing operator pin fixes the Codex CLI at `0.129.0-alpha.15` on every machine;
3. the server refuses that model on that CLI.

Measured on billy-old on 2026-09-03 under `codex-cli 0.129.0-alpha.15`, with the identical call
form V2 registers:

```
{"type":"error","status":400,"error":{"type":"invalid_request_error",
 "message":"The 'gpt-5.6-terra' model requires a newer version of Codex.
            Please upgrade to the latest app or CLI and try again."}}
```

`thread.started` and `turn.started` were emitted **before** the 400, so the credential is live and
end-to-end dispatch works; the refusal is model availability, not authentication. Independently,
`gpt-5.6-terra` does **not appear** in the served-model manifest the CLI logs for this account
(`gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex-spark`, `codex-auto-review`). Two independent
lines, not one error string. Raw artifacts and their sha256 are in `provenance/`.

Separately, the pinned CLI is **unrunnable on the Mac**: Apple revoked its signing certificate, so
AMFI SIGKILLs it on `execve` (`spctl` reports `CSSMERR_TP_CERT_REVOKED` while `codesign --verify
--strict` still passes — the signature is intact, the *certificate* is revoked). All model dispatch
therefore runs on billy-old, which runs the pinned CLI normally.

**V3 is a new design with a new seed commitment. It is not an edit to V2.** V2 keeps its frozen
artifacts, its sealed seed, its single-run authorization and its `EXECUTION_BLOCKED_PRE_DISPATCH`
state. V2 remains prospective with zero protected observations, and its `PARENT_SUFFICIENT`
expectation remains **unobserved**. V3 spends none of V2's authorization and retro-fits nothing.
The generator family, the parent implementations and the statistical machinery are **copied, not
imported**, so V3's freeze does not depend on V2's files and cannot perturb them.

## 1. Question, null, expectation

**Q.** On fresh synthetic hidden-policy episodes, does a recursive meta-discovery arm improve
exact held-out action selection over the strongest faithful mature rule-induction parent under
matched public information and prospectively fixed resource limits?

**H0 (parent sufficiency).** The strongest generator-faithful parent makes the same or better
held-out decisions at lower cost. **Pre-registered expectation:** `PARENT_SUFFICIENT`, a
successful terminal. The generator family is a linear multiclass argmax; the max-margin parent's
hypothesis class contains it. **MAXMARGIN_PARENT is optimal by construction on this family**, up
to its regularization and optimizer budget — that is declared here, not discovered later.

**What a null means.** "No residual detectable in the registered decision problems the parents
already solve exactly." Never "no residual exists."

**Scope.** Supports, if valid, synthetic rule-induction mechanism evidence inside the frozen
generator family. Does not support naturalistic scientific-development superiority,
science-of-science superiority, a Machine Epistemics field residual, causal law, or publication
readiness.

## 2. Generator (family unchanged from V1/V2)

`sd70v3_generator.build_suite`: 4–7 binary context features, 3–5 actions, integer weights in
[−3, 4] with distinct rows, argmax with lowest-index tie break, 8 unseen training contexts each
yielding one SUCCESS (best action) and one FAILURE (uniformly random other action), one unseen
held-out context, random codeword tokens. The private file additionally carries the worst-action
set and latent query scores (for the critical-false-direction outcome). Nothing private reaches
any arm. Because every FAILURE is paired with a SUCCESS on the same context, failure evidence adds
strictness only; the no-failure-evidence ablation is expected to cost the parents nothing and is
informative only about the model arms.

## 3. Arms and information surfaces

| arm | kind | surface | tasks |
|---|---|---|---|
| TARGET_ONLY_DETERMINISTIC | deterministic | TARGET_ONLY | all |
| TARGET_ONLY_NEGATIVE_CONTROL | model | TARGET_ONLY (physically no `training_episodes` key) | 60 |
| SIMPLE_FREQUENCY, MATCHED_CASE, NAIVE_BAYES, DECISION_LIST, PERCEPTRON, MAXMARGIN, PAIRWISE_LINEAR parents | deterministic | COMMON | all |
| STRONGEST_GENERATOR_FAITHFUL_PARENT | alias of the development-selected parent (**MAXMARGIN_PARENT**) | COMMON | all |
| FIXED_META_LESSON | deterministic fixed heuristic | COMMON | all |
| F0_PARENT_FEDERATION | deterministic plurality of the seven parents; strongest breaks ties | COMMON | all |
| F2_STATIC_NO_RECURSION | model, recursion disabled | COMMON + parent advisory | all |
| F2_RECURSIVE_META_DISCOVERY_FULL | model, full registered procedure | COMMON + parent advisory | all |
| F2_FULL_MINUS_FAILURE_EVIDENCE | model ablation | COMMON with FAILURE episodes removed + advisory on that surface | all |
| F2_FULL_MINUS_PARENT_FEDERATION | model ablation | COMMON (no advisory) | all |
| `<deterministic arm>__LP`, `__QS` | deterministic on control pools | as the arm | all |
| F2_RECURSIVE_META_DISCOVERY_FULL__LP, `__QS` | model on control pools | COMMON + advisory | 60 |

Surfaces are defined in `sd70v3_generator.surface_for`; a request holds only its surface keys. The
parent advisory is computed from the arm's own surface (so the success-only arm's advisory never
sees failures). `REQUEST_SURFACE_MANIFEST.json` records the sha256 of every request, an
arm-surface hash, the surface keys per arm, and the count of training-only tokens found in any
TARGET_ONLY request (must be 0).

### 3.1 Custody across the host boundary (stronger than V2's)

Generation and evaluation run on the **Mac**; model dispatch runs on **billy-old**.

- The protected seed and `private_oracle.json` exist **only on the Mac**.
- **Only** the `requests/` tree and the two standalone executables are copied to billy-old.
  `public_tasks.json`, `private_oracle.json` and the seed are never copied.
- Gold-blindness on the dispatch host is therefore **physical, not permissional**: the oracle is
  not on that machine at all. This is strictly stronger than V2's same-host `chmod 000` lock.
- The shipped payload is verified against `REQUEST_SURFACE_MANIFEST.json` on arrival: every
  request sha256 must match, and **no other file may be present**.
- Each model child runs in an empty temporary cwd with a private copy of its own request only.
- Responses are copied back and frozen before evaluation, which runs where the oracle lives.
- The Mac-side dispatch stage still deletes and hash-exactly restores `private_oracle.json` around
  the deterministic arms, so V2's same-host guarantee is retained there too.

## 4. Parents (all deterministic, stdlib, frozen hyper-parameters, no tuning on any task)

Frozen tie break everywhere: highest score, then candidate-list order.

- **SIMPLE_FREQUENCY_PARENT** — global success − failure count per action.
- **MATCHED_CASE_PARENT** — kernel vote, weight 1/(1 + Hamming distance), ± by outcome.
- **NAIVE_BAYES_PARENT** — naive-Bayes log odds success-vs-failure, Laplace(1).
- **DECISION_LIST_PARENT** — Rivest decision list, sequential covering over ≤ 2-literal conjunctions.
- **PERCEPTRON_PARENT** — averaged Kesler multiclass perceptron, margin 1, 50 epochs, bias.
- **MAXMARGIN_PARENT** — Crammer–Singer hinge + L2 (λ = 0.01), full-batch subgradient, step 0.1 × 200, bias.
- **PAIRWISE_LINEAR_PARENT** — averaged binary perceptron per pair (documented boundary: vote cycles).
- **FIXED_META_LESSON** — additive per-feature (success − failure)/support evidence.
- **F0_PARENT_FEDERATION** — plurality over the seven parents; ties → strongest parent.

**Selection rule (frozen, re-run on V3's own seeds `sha256("SD70-V3-DEV|k")`, 3 × 200 tasks):**
highest mean development exact accuracy among {PERCEPTRON, MAXMARGIN, PAIRWISE_LINEAR,
DECISION_LIST, NAIVE_BAYES}; tie → lower wall time. Result: **MAXMARGIN 0.6783** > PAIRWISE 0.6567
≈ PERCEPTRON 0.6567 > DECISION_LIST 0.6283 > NAIVE_BAYES 0.6183, against chance 0.2629.

### 4.1 Comparator (pre-registered, frozen on the development split)

The comparator is `max(STRONGEST_GENERATOR_FAITHFUL_PARENT, F0_PARENT_FEDERATION)` by mean
development exact accuracy, frozen **before** protected generation. On the V3 development split
MAXMARGIN scored **0.6783** and the F0 federation **0.6633**, so the comparator is the strongest
parent. Silently comparing against the weaker federation would be baseline-weakening; F0 still
runs on every protected task and is reported as a required arm and a secondary contrast.

## 5. Model arms and the channel/request-body contract

Codex CLI `exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check
--sandbox read-only -C <empty tmp> --json --output-schema`, on **billy-old**, model **`gpt-5.5`**,
`model_reasoning_effort = medium`, timeout 600 s, one call per arm-task, at most one bounded
rerun (max 2 attempts), concurrency ≤ 2. Identical settings for every model arm.

**Model justification.** The binding constraint is that the pinned CLI must be able to *reach* the
model, proven by an actually completed turn rather than by documentation. `gpt-5.5` completed a
turn on 2026-09-03 with exit 0, `turn.completed`, the `--output-schema` honored, and usage
`{input 13581, cached_input 2432, output 61, reasoning_output 24}`.

### 5.1 Why a channel contract, measured twice

**Pinning a served model id does not pin an experimental condition.** In the E30-R12 campaign every
one of 119 envelopes recorded the correct served model id and the campaign still failed:
provider-side channel behaviour drifted between runs, and an identical frozen prompt that had
completed in 763 output tokens five days earlier hit a 6,000-token cap on re-run, the budget
consumed by a reasoning block the arm never reads. A contract measured **once at freeze** could not
have caught that, because the drift happened *between* runs and nothing re-measured.

So the contract is measured at **campaign start and again at campaign end**, on three byte-frozen
canary prompts (sha256 in the JSON) that carry no task surface and no oracle content. Because they
touch nothing protected, their tolerance bands were legitimately calibrated by repeated pre-freeze
dispatch (6 draws per canary, `provenance/calibration/`); that calibration is **part of the frozen
design**, not a post-outcome change.

**Registered request body.** model `gpt-5.5`; reasoning effort `medium`; **reasoning enabled**,
summaries **not emitted** (the served manifest reports `default_reasoning_summary: "none"`, which
suppresses summaries — reasoning itself runs, and the deliberative canary spends 26–31
`reasoning_output_tokens`); 7-field output schema, `additionalProperties: false`; read-only sandbox;
empty cwd; timeout 600 s; attempt cap 2; concurrency 2.

**Bands.** Tolerance on |mean_end − mean_start| (3 repeats a side) = max(8, observed full range,
4·sd/√3), floored at **1300** for `input_tokens` and **20** for output and reasoning tokens. The
input floor exists because one calibration draw came in at 14,875 against a 13,593–13,625 baseline;
applying the tight 8-token band the other two canaries would support would guarantee a false
positive the first time that outlier landed elsewhere.

**Detection floor, stated honestly.** The gate detects canary-mean shifts larger than 1300 input
tokens or 20 output / 20 reasoning tokens. E30-R12's drift was +5,237 output tokens — roughly 260×
this floor. Shifts smaller than the floor are **not** detected, and this design does not claim they
are.

**Observability caveat.** The served-model manifest is visible only as a *side effect* of this CLI
failing to decode it (unknown reasoning variant `max`), which makes it log the raw body to stderr.
If the server response ever becomes decodable, the scrape goes silent. A silent scrape must never
read as "contract verified" — that is exactly a counter that never ran. Hence three distinct
verdicts, all of which route to `CANNOT_CHECK` and **none of which is `OK`**:

| verdict | meaning |
|---|---|
| `CHANNEL_CONTRACT_OK` | every check ran, with a non-zero denominator, and passed |
| `CHANNEL_DRIFT_DETECTED` | a check ran and failed |
| `CHANNEL_CONTRACT_UNOBSERVABLE` | a check **could not run** — distinct from OK |
| `CHANNEL_CANARY_DISPATCH_FAILED` | a canary did not complete |

### 5.2 Per-envelope homogeneity

Start/end canaries straddle a mid-campaign shift without localising it, so every model envelope
also records `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`,
`usage_source`, `prompt_sha256`, `prompt_bytes` and the scraped channel observation. Gates: ≥ 0.98
of envelopes must carry `usage_source == TURN_COMPLETED_USAGE`; ≥ 0.98 must have
`input_tokens / prompt_bytes` inside the frozen band; ≤ 0.02 may exceed the
`reasoning_output_tokens` cap; every observable envelope must report the frozen `comp_hash`.
**Every count is reported with the denominator it was computed over** — a zero without its
denominator is not a result.

The V2 receipt's recursive usage scan silently missed both `cached_input_tokens` and
`reasoning_output_tokens`; V3 reads `turn.completed.usage` explicitly and records `usage_source`
so a fallback parse is never mistaken for a direct observation.

## 6. Controls

- **Label permutation (LP):** a uniformly random bijection of the candidate actions applied to
  every training `chosen_action`. Every relabelling-equivariant learner then predicts π(g), so
  expected accuracy is exactly chance while all training statistics are preserved. V3 development:
  all parents 0.26–0.28 vs chance 0.2629.
- **Query-to-task shuffle (QS):** the held-out context is replaced by another task's query bits and
  the answer is that task's rule mapped positionally; the answer is independent of this task's
  training. V3 development: parents 0.25–0.28.
- **Three F2 ablations:** no failure evidence, no parent federation, no recursion.
- **Physically sanitized target-only:** model and deterministic.
- Model controls run on the 60 lexicographically first task ids of their pool (frozen).

### 6.1 Arm-divergence assertion

A contrast between two arms whose requests are byte-identical can only ever report the same number
twice. Before evaluation, for each contrasted pair the runner asserts that the per-task request
sha256 **and** the built prompt bytes differ on **every** shared task id; that
`F2_FULL_MINUS_PARENT_FEDERATION` carries no `parent_advisory` key on any task; and that
`F2_FULL_MINUS_FAILURE_EVIDENCE` carries no FAILURE episode on any task. A **positive control**
asserts that the full arm *does* carry both — without it the two preceding checks could pass
vacuously. Any failure routes to `CANNOT_CHECK`.

## 7. Outcomes (frozen estimands)

1. **Protected decision quality.** Exact-action correctness; Wilson 95% per arm; primary estimand
   Δ = acc(F2_FULL) − acc(comparator) with a 10,000-draw percentile bootstrap (seed 20260902) and
   an exact one-sided McNemar mid-p; Holm over the two primary contrasts at family α = 0.05.
2. **Critical false direction.** Selecting a worst action (minimal latent score). Rate per arm;
   paired Δ vs the comparator.
3. **Resource cost.** Per arm: model calls, attempts, retries, input/output/total/reasoning tokens,
   tool calls, wall time; aggregation = sum over arm-tasks including failed attempts.
4. **Parent non-regression.** Lower 95% bootstrap bound of Δ > −0.05.

## 8. Power → task count

Carried over from V2 and re-verified, not re-derived silently: the generator family is unchanged on
the public side, so V2's Connor (1987) paired-binary calculation applies — δ_min = 0.10, assumed
discordance 0.30, α = 0.025 one-sided, power 0.80 → 234 tasks; **frozen N = 240**. V3's own
development split gives a strongest-vs-second discordance of **0.1483**, comfortably inside the
deliberately conservative 0.30 (achieved power 0.811 at 0.30, 0.877 at 0.25). Model calls:
240 × 4 + 3 × 60 = **1,140**.

## 9. Missingness

`VALID` / `ARM_FAILURE` (model failure, timeout, out-of-candidate selection → scored incorrect) /
`INTEGRITY_VIOLATION` (missing, unreadable, identity mismatch → evaluation refuses). Global model
failure rate > 0.05 → `CANNOT_CHECK`; F2_FULL, F2_STATIC or TARGET_ONLY model arm failure rate
> 0.10 → `CANNOT_CHECK`. The parent's own LP control must sit at chance or the evaluator is declared
invalid. No silent replacement.

## 10. Decision rules (evaluated in this order)

1. **CANNOT_CHECK** — dispatch integrity, missingness, identity, design-hash or evaluator-validity
   failure; **or** a channel-contract verdict other than `CHANNEL_CONTRACT_OK`; **or** an
   envelope-homogeneity failure; **or** an arm-divergence assertion failure.
2. **PARENT_SUFFICIENT** — the comparator ties or exceeds F2_FULL (Δ ≤ 0), or F2_FULL fails any
   gate: Δ ≥ 0.10; Holm-significant; non-regression (CI low > −0.05); CFD Δ ≤ 0.05; cost within
   budget; mechanism (F2_FULL − F2_STATIC ≥ 0.05 with mid-p < 0.05); no ablation beats the full arm
   by more than 0.03; model negative controls behave.
3. **FIXED_META_LESSON_SUFFICIENT** — F2_FULL passes every gate but FIXED_META_LESSON ≥ F2_FULL.
4. **PROSPECTIVE_META_POLICY_RESIDUAL** — otherwise.

## 11. Custody

Seed generated and committed on the Mac before generation (sha256 published; seed never in the
repository, never on the dispatch host); oracle absent from the dispatch host entirely; raw
responses frozen before evaluation; evaluator separate from the solver executable; no threshold or
baseline change after oracle access (the design hash is bound into `FROZEN_SUITE.json` and
re-checked by `evaluate`); code hashes in the fidelity receipt. The V3 seed is a fresh 63-bit
`secrets.randbits` draw, distinct from V2's.

## 12. Authority

Grants nothing: no scientific truth, causal law, field status, submission or publication readiness.
`PARENT_SUFFICIENT` is a successful terminal. A negative or regime-conditional result is
**intermediate**: attribute the failure to one stage, apply the matching lever, re-test against the
strongest parent. No outcome is ever tuned positive.

## 13. Reproducibility boundary (measured, not asserted)

"Byte-identical on re-run" is a sentence routinely written and not executed. It was executed here,
across three CPython versions, and it is **false across interpreters**:

| comparison | what flipped | magnitude |
|---|---|---|
| 3.9.6 → 3.12.13 | `MAXMARGIN_PARENT` LP-control accuracy 0.26667 → 0.26833 | 1 task in 600 |
| 3.12.13 → 3.13.12 | `FIXED_META_LESSON` accuracy 0.61167 → 0.61333 | 1 task in 600 |

Cause: the parents accumulate float scores, and a near-tie is resolved differently by summation
order. **Invariant across all three interpreters:** every generator-faithful candidate's exact
accuracy, the full ranking, the selected strongest parent, the comparator choice, and the
strongest-vs-second discordance (0.1483). The sensitivity is ≈ 0.17 % of tasks — two orders of
magnitude below the 0.10 minimum effect — and cannot flip a registered gate.

Consequences, registered: the campaign pins **CPython 3.13.12** (`/Users/billy/miniforge3/bin/python3`)
on the Mac for generation, the deterministic arms and evaluation. billy-old (CPython 3.14.4) only
marshals requests into the Codex CLI and never computes a parent decision, so parent numerics do not
depend on it. Byte-identical re-run is claimed **only** under the pinned interpreter, and nowhere
else.

## 14. Projected cost

The development rehearsal (8 development tasks × 7 model arms = 56 envelopes, development seed,
no protected task involved) completed in 894.6 s at concurrency 2 with **0/56 failures**
(15.98 s/envelope). The protected campaign's 1,140 envelopes project to ≈ 18,200 s (≈ 5.1 h) plus
two channel measurements. Concurrency stays at the registered 2: the rehearsal validated exactly
that setting, and an untested higher concurrency risks rate-limit failures that would trip the
missingness gate.

The rehearsal also **caught a gate that would have cried wolf**. The first drafted homogeneity gate
used a raw `input_tokens / prompt_bytes` band of [0.10, 1.20]; the real ratio is 2.30–13.34, because
`input_tokens` is dominated by a ≈ 13.5 k-token fixed harness overhead while `prompt_bytes` varies
1,038–7,163. That band would have failed 100 % of envelopes on first contact. It was replaced with a
fitted linear model before freezing and before any protected task existed. This is recorded because
a checker that raises a false alarm on its first real run gets switched off.
