# E30-R13 — confirmatory BugsInPy re-run under a registered channel request-body contract

Prose companion to `E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json`, which governs.
Status: `PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS`. Nothing in this document reports an
outcome, because none exists.

## 1. Why this study exists

E30-R12 was registered to ask whether the four solver arms separate on real BugsInPy
repair once patches are canonicalized at emission so they actually apply. It dispatched
its registered chain and halted during model dispatch at
`EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`: 119 of 480 responses written, 116 of them
envelope failures whose output tokens sat at or above the registered 6000-token cap with
the diagnosis `model did not return a JSON object`, **0 of 480 evaluations, no gate
computed, no endpoint read**. The registered question is still unasked.

The cause was measured, not inferred. On the identical frozen prompt, the bound z.ai
Anthropic-compatible channel answered two ways:

| request body | stop reason | output tokens | content blocks | text chars |
|---|---|---|---|---|
| provider default | `max_tokens` | 6000 | `thinking` (27 624 chars) | **0** |
| `thinking: {type: disabled}` | `end_turn` | 775 | `thinking` (745) + `text` (2903) | 2903 |

The arm reads only `text` blocks, so under the default it receives nothing and writes an
envelope failure that contains no model output. And on the same task, the same arm and a
byte-identical prompt (`input_tokens` 61 557 in both), five days apart: E30-R11 completed
at **763 output tokens in 12.5 s**; E30-R12 hit the **6000 cap in 71.0 s** and failed.

## 2. The finding this design is built around

**Pinning a served model id does not pin an experimental condition.**

All 119 of E30-R12's envelopes recorded exactly one served model id, `glm-5.3`, equal to
the frozen value. Its GR0c served-model homogeneity condition held for every envelope
written. What moved was the channel's *behaviour* at a *fixed* served id — and no gate in
the programme observed that.

E30-R12's `model_binding` registered the channel, the base URL, the requested model, the
frozen served model, the served-model assertion and the per-envelope served-id record. It
registered **no request-body contract**. That is the hole. The condition was inherited
from a provider default, and a provider default is free to move.

E30-R13 closes it in three places, which are the three things the previous lane's queued
amendment asked for:

1. **A registered channel request-body contract**, frozen by sha256 over its bytes.
2. **Output-token budgets re-derived from measurement**, replacing the inherited pair.
3. **A per-envelope channel-configuration record and a homogeneity gate over it.**

## 3. The registered request-body contract

The contract is the request body minus `model`, `max_tokens` and `messages` — the part a
study freezes. It is selected by `ORION_ARM_CHANNEL_CONTRACT`; an unknown value raises
`ChannelContractUnknown` rather than falling back to the default, because a silent
fallback would run the study under exactly the unregistered condition the contract exists
to exclude while every receipt still said the contract applied.

The registered contract for E30-R13 is `thinking_disabled`, whose fingerprint covers the
contract id, the system prompt, `temperature` and the extra body. The fingerprint is
computed by the arms executable itself and asserted against the design in setup, so a
label can never pass while the bytes behind it differ.

**The contract choice is measured, not preferred.** Three request bodies were run
through the same frozen prompts at the same 16 000-token headroom, outside any campaign
tree (`results/E30_R13_CALIBRATION_*.json`):

| contract | calls | stop reasons | calls with zero text | output tokens (min–max) | final calls parsing as JSON |
|---|---|---|---|---|---|
| `provider_default` | 4 | 3 × `max_tokens`, 1 × `end_turn` | **3** | 7418 – 16 000 | 1/4 |
| `thinking_enabled_2048` | 4 | 3 × `max_tokens`, 1 × `end_turn` | **3** | 9436 – 16 000 | 1/4 |
| `thinking_disabled` | **108** | 108 × `end_turn` | **0** | 271 – 3292 | 47/48 |

Three things follow. The provider default reaches a 16 000-token headroom with **zero
text characters** on three of four tasks — including the *smallest* task in the frozen
set, at 132 571 prompt characters — so E30-R12's description of this signature as
affecting "the largest tasks" does not hold. Its one completing call still spent 7418
output tokens, above E30-R12's registered 6000-token primary cap. And requesting thinking
with an explicit `budget_tokens` of 2048 changes nothing: three of four calls still reach
the headroom with no text, so the bound endpoint does not honour the requested budget and
"enabled with a small budget" is not a registrable condition on this channel.

**What is registered, and what is not.** What is registered is the *bytes* of the request
body and three *gateable properties* of the response: `stop_reason == end_turn`, text
characters greater than zero, and output tokens below the cap. This design does **not**
claim that the contract disables the provider's reasoning. Under
`thinking: {type: disabled}` the measured response still carried a thinking block — 745
characters in E30-R12's probe. Saying "thinking is off" would be an inference where a
measurement is available, which is the error this lane's predecessor had to correct once
already.

## 4. Budgets, derived rather than inherited

E30-R12 registered 6000 as its primary budget and an escalation to 36 000 from pass 3,
the latter derived from a *single* pre-dispatch smoke measurement. Both were inadequate:
116 of 116 failures sat at or above the primary cap, and a diagnostic run of one cell at
the escalated budget closed at 35 937 output tokens with a 161 644-character thinking
block and 5895 characters of text after 786 s. Because the runner divides the registered
total by the arm's call count, `F0_PARENT_FEDERATION` and `F2_ORION_METABOLIC_FULL` would
each have received **12 000 per call** — a third of what one call needed to close there.

E30-R13 measures instead. `e30_r13_channel_calibration.py` runs the frozen prompts for
every call shape the campaign issues, with replicates, **outside any campaign run tree**,
and records token accounting, stop reasons, content-block shapes and a JSON-parseability
boolean. 108 calls were measured under the registered contract, across six tasks spanning
the frozen set's prompt-size range (132 571 to 633 957 characters), all four arms and all
seven call shapes, at two replicates each. It retains no response text, evaluates no patch, reads no gold tree and reads no
endpoint. `e30_r13_budget_note.py` then applies a rule fixed in code before the numbers
were known: the per-call cap is four times the observed maximum, rounded up to the next
thousand. If any calibration call had stopped at `max_tokens`, the derivation refuses —
a censored draw is a floor on the true maximum, and four times a floor means nothing.

Two structural changes follow from the same measurement:

All 108 calls ended at `end_turn`, none reached the headroom, none emitted zero text
characters, and the largest single call used **3292** output tokens — so the registered
per-call cap is **14 000**, four times that maximum rounded up to the next thousand.

* the cap is set **per call**, directly, and the divide-by-call-count total is left
  unset, so every arm gets the identical per-call headroom rather than an asymmetry
  registered as if it were one number;
* there is **no escalation ladder**. The cap is derived to be non-binding; a call that
  stops at `max_tokens` is a channel-behaviour violation for GR0e to report, not a
  shortfall to top up mid-campaign. Raising a budget after seeing failures is an
  unregistered instrument change made post-dispatch.

The same arithmetic settles feasibility. The campaign issues **1080 model calls**, not
480: the four arms cost 1 + 2 + 3 + 3 = 9 calls per (task, repetition). Costing the
campaign in envelopes understates the dispatch by a factor of 2.25, and at the
provider-default behaviour E30-R12 measured — 786 s for one call at the 36 000-token
escalated budget — 1080 calls cost about 236 h serially and roughly 118 h at the
concurrency of 2 this lane used, against a 24-hour SLURM allocation. That path is not
merely expensive; it is undispatchable. Under the registered contract the same 1080 calls
cost about 6.1 h serially at the measured median of 20.3 s per call, and about 1.5 h at
concurrency 4.

## 5. The two new gates

**GR0d `CHANNEL_CONTRACT_HOMOGENEITY`** — every one of the 480 response envelopes carries
a `channel_receipt` recording exactly one request-body contract sha256, equal to the
registered fingerprint, and every model call inside every envelope reported a contract.
Compared by digest, not by label.

**GR0e `CHANNEL_BEHAVIOUR_CONFORMANCE`** — no model call stopped at `max_tokens` and no
model call emitted zero text characters. This is the behavioural half of the same lesson:
E30-R12's 116 failures were exactly truncation-with-no-text at a correct served model id.

Both are hard gates evaluated before any endpoint is read, and both publish their
denominators: `envelopes_expected`, `envelopes_with_a_channel_receipt` and the model-call
counts are printed, so `0 offenders` can never be read out of `0 envelopes examined`.
Both return **`COULD_NOT_CHECK`** as a status distinct from `PASS` and from `FAIL`, with
a distinct process exit code (5 rather than 4 or 0), and it routes to
`EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ` — not to a null, and not to an equivalence.

Setup gains a **channel-behaviour probe** beside the existing served-model probe, which
asserts those three gateable properties on the live channel before a single campaign call
is made, and a check that the campaign's `responses/` and `evaluations/` start **empty**.

## 6. Endpoints, and where the arithmetic comes from

E1 registered failing test fixed (primary, denominator 40, sensitivity 39) · E2 any
critical new failure (co-primary, non-inferiority margin 0.02) · D1 patch-apply rate
(registered diagnostic, comparator = PC-R6's per-arm rates measured by the same code).

None of this is retyped. `e30_r13_analysis.py` **imports** `e30_r12_analysis.py` by path
under a sha256 pin asserted at run time and reuses `build_tables`, `family`,
`evaluate_gates` and `route` verbatim. E30-R12's endpoint arithmetic was never exercised
on data and is not in question; what failed was the channel. Importing makes the two
studies' endpoint definitions the same code rather than a similar transcription of it.
E30-R12's file is frozen and is not modified.

## 7. What this study can and cannot detect

Carried forward from E30-R12's registered power note, unchanged, because the substrate,
the denominator and the test are unchanged:

* at n = 40 the exact test **cannot reject at any effect size** unless at least **7 tasks
  are discordant in the same direction** — an implied minimum observable **risk
  difference of 0.175**;
* power against the programme's registered **5 pp MID is 1–2 %** (0.0116 / 0.0185 /
  0.0168 / 0.0157 at psi = 0.10 / 0.20 / 0.30 / 0.40);
* 80 % power at 5 pp would need **430 / 863 / 1287 / 1708 tasks** at those psi values,
  while the pinned BugsInPy commit `11c5f1e` holds **501 numeric bug ids in total** and
  **295 inside the 8 registered projects**.

**n was reconsidered for this study and stays at 40.** The frozen substrate holds
prepared gold-blind solver workspaces and baseline lanes for exactly 40 tasks — counted
on the campaign tree, 40 entries in each. Reaching 430 would mean building roughly 390
further workspaces, per-project offline runtimes and baseline lanes before a single model
call. E30-R12 died without asking its question; a substrate build that consumes the
window and leaves the question unasked again reaches the same terminal by a longer route.
A powered confirmatory test is pre-registered here as a **separate study**, and E30-R12's
verdict is carried forward: even the whole pinned benchmark is underpowered for 5 pp at
psi ≥ 0.20.

**E30-R13 is an estimation and diagnostic study, and a non-rejection is NOT evidence of
equivalence.**

## 8. Relationship to the earlier runs

E30-R11's, E60's and PC-R6's endpoints and E30-R12's receipt are **frozen terminal**.
E30-R13 revises, re-scores and reinterprets none of them, and a CI step fails the pull
request if it touches their archives.

**R13 vs R11 is descriptive only, twice over.** R11's response envelopes record no served
model id, and its campaign env requested `glm-5.2`, which this endpoint answers with
`glm-5.3` at HTTP 200 and no warning — so R11's served model is **INFERRED, NOT
VERIFIED**. R11 also ran under no registered request-body contract and recorded none, so
its channel condition is unknown as well as its model.

**R13 vs R12 is not a comparison at all.** E30-R12 produced 0 of 480 evaluations,
computed no gate and read no endpoint. There is no R12 result to compare against.

**R13 does not reuse R12's campaign directory** and does not pool its 3 completed
envelopes, which were produced under the provider default. A new campaign identity means
a clean run, and setup refuses to start otherwise.

## 9. Terminals

Evaluated in the registered order:
`EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ` → `CHANNEL_CONTRACT_VIOLATION` →
`CHANNEL_BEHAVIOUR_VIOLATION` → `LANE_DEFECT` → `F2_HARMFUL` → `CRITICAL_REGRESSION` →
`INTERFACE_STILL_BROKEN` → `FIRST_REGISTERED_POSITIVE` → `PARENT_SUFFICIENT` →
`NO_ARM_SEPARATION`.

The channel terminals precede everything because a campaign run under an unverified or
non-conformant channel cannot support any endpoint claim. Hard-gate and adverse terminals
precede favourable ones.

**`PARENT_SUFFICIENT` and `NO_ARM_SEPARATION` are registered, legitimate terminals.** If
the arms do not separate once patches actually apply, that is a real and important result
and is reported as plainly as a positive would be.

## 10. Custody

The design and every gate are frozen before dispatch; no design, gate, endpoint, margin,
family, disposition rule or budget may change after dispatch, for any reason. Setup
asserts three things against the frozen design before a campaign call is made: that the
dispatched contract's sha256 is the registered one, that the dispatched per-call cap is
the registered **14 000** — GR0e catches truncation, but only this catches a cap that is
simply the wrong number — and, on the first setup only, that `responses/` and
`evaluations/` are empty. The emptiness assertion is gated on a sentinel rather than
applied unconditionally, because the registered execution lane is resumable and setup
re-runs on a chain resubmit; an unconditional assertion would block a legitimate resume
and force a post-dispatch design change to unblock it.

The dispatch gate refuses to run without `PROTECTED_RUN_AUTHORIZATION.json`, which is
coordinator-written and says so, quotes the operator's verbatim instruction with its
source, and acknowledges the exact design bytes — so a design edited after authorization
halts the study rather than silently running a different one. It does **not** claim human
authorship, because it is not human-written; what is asserted is that the human
instruction it quotes is present and attributed. The rollup step renames it to
`PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json`, so the guard re-arms and a later
resubmission cannot run on a spent authorization.

The seed is **20260903**, published here in the clear before dispatch and also as its
sha256. A hash-commit-then-reveal protocol would be weaker here rather than stronger: the
seed is a bootstrap resampling seed compiled into `e30_r13_analysis.py`, which this same
pull request freezes and hashes, so it is already publicly checkable and cannot be
re-chosen after an outcome. Claiming a commit-and-reveal that was not run would be a
rendered status standing in for the thing itself.

Arms read only the gold-blind solver workspace; gold patches are read only by GR0b, after
every response is written.

## 11. Authority

This design grants no scientific truth, no field status, no supertheory status and no
publication readiness.
