# E30-R12 — outcome receipt

**Status: `EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`.**

The registered chain was dispatched under the standing operator authorization and halted
during model dispatch. **Zero of the 480 evaluations were produced, no gate was computed, and
no endpoint was read.** This is reported here as its own status. It is **not** a null on E1,
not a null on E2, not `NO_ARM_SEPARATION`, not `PARENT_SUFFICIENT`, and not `LANE_DEFECT`.
Nothing in this receipt says anything about whether the four arms separate on real BugsInPy
repair. That question remains unasked.

| | |
|---|---|
| design | `E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json`, sha256 `b5aa3a6ff1f875858df3a84409f99a2b544dbebcaf035f6f2afa88ee253a595e` |
| registered as | PR #178, squash-merged `8196c36a` |
| dispatched | 2026-09-02T23:45:03Z, LUNARC cosmos, jobs 3566403–3566409 (`afterok`) |
| halted | 2026-09-03T01:05Z |
| responses | 119 of 480 written — **116 `EXECUTION_FAILED_MODEL_RESPONSE`, 3 `COMPLETED_PROPOSAL_ONLY`** |
| evaluations | 0 of 480 |
| gates evaluated | none |

## What this study is, and what it was registered to be

E30-R12 is a **new prospective confirmatory study**, not a re-analysis. It asks E30-R11's
registered question again under the arm-side apply-clean patch emission that landed in PR #168
(anchor `8945cec`). E30-R11's, E60's and PC-R6's endpoints stay **frozen terminal**; nothing
here revises, re-scores or reinterprets them, and a CI step fails this PR if it touches their
archives.

**E30-R12 is an estimation and diagnostic study, and a non-rejection is not evidence of
equivalence.** Run from the merged tree, `e30_r12_power_note.py` (pure arithmetic, no outcome
input; output archived as `results/E30_R12_POWER_NOTE_OUTPUT_V1.json`) gives:

- at n = 40 the exact test **cannot reject at any effect size** unless at least **7 tasks are
  discordant in the same direction** — an implied minimum observable **risk difference of 0.175**;
- power against the programme's registered **5 pp MID is 1–2 %** (0.0116 / 0.0185 / 0.0168 /
  0.0157 at discordance psi = 0.10 / 0.20 / 0.30 / 0.40);
- 80 % power at 5 pp would need **430 / 863 / 1287 / 1708 tasks** at those same psi values, while
  the pinned BugsInPy commit `11c5f1e` holds **501 numeric bug ids in total** and **295 inside the
  8 registered projects**.

**`PARENT_SUFFICIENT` and `NO_ARM_SEPARATION` are registered, legitimate terminals.** If the arms
do not separate once patches actually apply, that is a real finding and would be reported as
plainly as a positive. Neither terminal was reached here, because nothing was measured.

## Why execution stopped

Every one of the 116 failed envelopes carries `output_tokens` at or above the registered
primary cap of 6000 and the diagnosis `model did not return a JSON object`. The cause is on the
provider side and is measured, not inferred.

**The channel now spends the whole output budget on a thinking block.** On the identical frozen
prompt (`results/E30_R12_CHANNEL_BEHAVIOUR_PROBE_V1.json`), with `max_tokens` 6000:

| request body | stop reason | output tokens | content blocks | text chars |
|---|---|---|---|---|
| provider default | `max_tokens` | 6000 | `thinking` (27 624 chars) | **0** |
| `thinking: {type: disabled}` | `end_turn` | 775 | `thinking` (745) + `text` (2903) | 2903 |

The arm reads only `text` blocks, so under the default configuration it receives nothing and
records an envelope failure that contains no model output.

**The same prompt, the same arm, the same task, five days apart** —
`results/E30_R12_EXECUTION_LANE_TALLY_V1.json`, `SIMPLE_DIRECT / bugsinpy-ansible-1`:

| | input tokens | output tokens | wall time | status |
|---|---|---|---|---|
| E30-R11 (2026-08-29) | 61 557 | **763** | 12.5 s | `COMPLETED_PROPOSAL_ONLY` |
| E30-R12 (2026-09-03) | 61 557 | **6000** (cap) | 71.0 s | `EXECUTION_FAILED_MODEL_RESPONSE` |

Identical input token count, so the request is the same; the difference is entirely in what the
provider does with it.

**The registered remedy is marginal for the single-call arm and structurally insufficient for
the multi-call arms.** The design registers this exact failure mode as
`execution_lane_contract.signature_2_truncation_starved`, describes it as affecting *the largest
tasks*, and registers a budget escalation to 36 000 from pass 3, citing a pre-dispatch smoke in
which the identical request at 36 000 used 3669 output tokens. In execution the mode affected
**116 of 116 failures across three arms**. Two diagnostic runs of the same cell at the escalated
budget, outside the campaign tree, measured:

| run | stop reason | output tokens | thinking chars | text chars | wall |
|---|---|---|---|---|---|
| through the arm — `results/E30_R12_ESCALATED_BUDGET_DIAGNOSTIC_ENVELOPE_V1.json` | budget exhausted | 36 000 | not recorded | no parseable JSON object | 510 s |
| direct, capturing blocks — `results/E30_R12_ESCALATED_BUDGET_BLOCK_PROBE_V1.json` | `end_turn` | 35 937 | 161 644 | 5 895 | 786 s |

The escalated budget is consumed almost entirely by thinking and clears the cap only marginally,
at roughly 13 minutes per call — and `ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET` is divided by the arm's
call count, so `F0_PARENT_FEDERATION` and `F2_ORION_METABOLIC_FULL` receive **12 000 per call**,
a third of what one call needed to close here. Reading the thinking block captured at the
6000-token cap, its tail is still non-convergent recall about the task ("this is getting nowhere
with pure recall"), not a JSON answer under construction.

**This is not a served-model substitution.** All 119 envelopes record exactly one served model
id, `glm-5.3`, equal to the frozen value; GR0c's condition was met by every envelope written.
The drift is in channel *behaviour* at a *fixed* served id — which no registered gate observes.

## What this does to the R11 comparison, and to the R11 caveat

E30-R11's campaign env requested `glm-5.2`, which this endpoint answers with `glm-5.3` at HTTP
200 and no warning — re-verified live immediately before dispatch and archived as
`results/E30_R12_SERVED_MODEL_PROBE_V1.json` (requested `glm-5.3` → served `glm-5.3`; requested
`glm-5.2` → served `glm-5.3`; both 200, no warning key in either body). R11's envelopes **record
no served model id**, so **R11's served model is INFERRED, NOT VERIFIED**, and any
**R12-vs-R11 comparison is descriptive only**.

The execution failure strengthens that caveat rather than resolving it: even holding the served
id fixed at `glm-5.3`, the channel's behaviour on a byte-identical prompt is not stable across
five days. Pinning a served model id does not pin an experimental condition.

## What was deliberately not done

- **No design, gate, endpoint, margin, family, disposition rule or budget was changed**, before
  or after dispatch. The design file is untouched and still reads
  `PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS`.
- **No in-flight repair was applied.** Adding `thinking: {type: disabled}` to the request body
  restores a parseable answer inside the registered 6000 budget, and it was *not* applied. The
  design's `model_binding` registers the channel, base URL, requested model, frozen served model,
  the served-model assertion and the per-envelope record — it registers **no request-body
  contract**. Pinning a thinking parameter after seeing the registered configuration fail is an
  unregistered instrument choice made post-dispatch. It would also have split the campaign across
  two channel configurations, because 3 responses had already completed under the provider default
  and the no-rescue clause forbids re-rolling a completed response.
- **The 3 completed envelopes were not re-rolled and not discarded**; they are recorded in
  `results/E30_R12_EXECUTION_LANE_TALLY_V1.json` (all `SIMPLE_DIRECT`, 5137–5910 output tokens —
  i.e. they completed only because their thinking block happened to fit under the cap).
- **E30-R11, E60 and PC-R6 archives were not read for scoring and not modified.**

## Queued next step

A **registered amendment, merged before dispatch, run under a new campaign identity**. It must
register:

1. the **channel request-body contract** — including the thinking parameter — explicitly, rather
   than inheriting a provider default that has now been shown to move;
2. **output-token budgets re-derived under that contract**, rather than inherited from E30-R11's
   6000/36 000, both of which are now known to be inadequate;
3. a **per-envelope record of the channel request configuration and a homogeneity gate over it**,
   because GR0c over the served model id alone did not detect this drift.

It must not reuse this campaign directory, whose 3 completed cells were produced under the
provider-default configuration.

## Authority

This receipt grants no scientific truth, no field status, no supertheory status and no
publication readiness. It records an execution outcome and a substrate observation. The
registered question E30-R12 exists to ask has **not** been answered.

## Artifacts

| file | what it is |
|---|---|
| `results/E30_R12_EXECUTION_TERMINAL_V1.json` | the machine-readable terminal status and root cause |
| `results/E30_R12_EXECUTION_LANE_TALLY_V1.json` | envelope tally, served-id tally, the 3 completed cells, the paired R11/R12 cell |
| `results/E30_R12_CHANNEL_BEHAVIOUR_PROBE_V1.json` | content-block behaviour of the bound channel on the frozen prompt |
| `results/E30_R12_ESCALATED_BUDGET_DIAGNOSTIC_ENVELOPE_V1.json` | one cell re-run at the registered escalated budget, outside the campaign tree |
| `results/E30_R12_ESCALATED_BUDGET_BLOCK_PROBE_V1.json` | the same cell at the escalated budget with the per-block breakdown measured |
| `results/E30_R12_SERVED_MODEL_PROBE_V1.json` | live re-verification of the glm-5.2 → glm-5.3 substitution |
| `results/E30_R12_POWER_NOTE_OUTPUT_V1.json` | transcribed output of the registered power-note generator |
| `results/E30_R12_DISPATCH_RECEIPT_V1.json` | the dispatched chain and its registered execution parameters |
| `results/E30_R12_COORDINATOR_AUTHORIZATION_ARCHIVED.json` | the authorization the dispatch gate validated |
