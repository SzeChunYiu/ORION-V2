# ME-F1 — Task-family feasibility table (V1)

**Purpose.** The brief for this study named four candidate task families and required that the
choice be recorded with costs and reasons. This is that record, written **before** the design was
frozen and before any protected campaign existed. Costs are measured on the execution host where
they are marked *measured*, and estimated where marked *est.*

**The binding requirement.** Verification must be mechanical, discovery must be genuinely open at
the registered budget, instances must be generatable fresh after the freeze so there is no
memorisation route, and the endpoint must be externally verifiable without a hidden oracle the arms
could have been tuned on.

---

## 1. The candidates

| # | Family | Verification | Discovery open at budget? | Fresh post-freeze? | Measured / estimated cost | Verdict |
|---|---|---|---|---|---|---|
| **F1a** | **Monotone constraint sub-ladders, model arms over a mechanical toolbox** | O(clauses), free | **Yes** — no arm can settle every rung; reference needs 40× the arm budget | **Yes** — generated from the custody seed | **measured**: 20 s/model call, ~21 k tokens/call, 8 calls/campaign; ground truth 3–6 s/campaign on the Mac | **SELECTED** |
| F1b | Same world, **deterministic Python arms, zero model calls** | same | same | same | **measured**: 18 s for 24 campaigns × 4 arms | **REJECTED** — see §2 |
| F2 | Open lemma / formal synthesis against a mechanical checker (Lean) | Mechanical (kernel) | Yes | Weakly — fresh *statements* are hard to generate at controlled difficulty | Toolchain work in progress in `lane-mex3`; not costed here | **REJECTED** — see §3 |
| F3 | Program synthesis against hidden tests | Mechanical (test run) | Partly | Requires an external spec author | est. 30–120 s/task plus corpus construction | **REJECTED** — see §4 |
| F4 | Real defect repair at genuine difficulty (BugsInPy) | Mechanical (test suite) | Yes | No — a fixed public corpus, with a memorisation route | Already funded in `lane-e30r12` | **REJECTED as duplicate** — see §5 |

---

## 2. F1b — why the deterministic variant was rejected

This was the family the feasibility pass first converged on, and rejecting it was not obvious. Its
merits are real: it is cheap, exactly reproducible, and it holds the ME-X1/X2/X4 methodology fixed
(arms as Python policies) while varying only the one dimension the gap identifies — whether an exact
planner exists. That is a clean single-variable change.

It was rejected for three reasons, in order of weight.

1. **It would have collapsed the boundary with FG80.** `lane-fg` is building FG80: generated
   post-freeze mini-frontier episodes, exact known-answer oracle, deterministic, **zero model
   calls**, mechanism versus faithful parent. A deterministic generated search world here would have
   put two lanes on the same ground. The coordinator's ruling separates them: FG80 asks whether the
   mechanism can do it *at all* in a world where the answer is knowable; ME-F1 asks whether the whole
   system holds up *under resource pressure* against a real federation in a world where nothing can
   compute the answer at budget. Resource-to-solution curves, false-completion rate and correct
   abstention are things an exact deterministic suite cannot measure.
2. **It would have made this study's substrate clauses dead letters.** The brief requires asserting
   the served model id per call and failing closed, and names tokens as a matched budget dimension.
   Neither means anything if no arm issues a model call. Freezing a clause that can never fire is
   worse than not having one.
3. **The residual it could detect is the narrower one.** With Python arms on both sides, the contrast
   is between two search heuristics. With model arms, the contrast is between two *control
   disciplines* given the same model, the same toolbox and the same budget — which is what the
   programme's control layer actually claims to be.

**It is not discarded.** `B5_ALGORITHMIC_CORE_NO_MODEL` carries the deterministic federation into the
selected design as a registered arm with zero model-call cost. It bounds the model arms from above,
and if it beats all of them, the design says in advance that the honest reading is that model control
adds nothing in this world.

---

## 3. F2 — open lemma / formal synthesis

Mechanically the strongest verification available: a kernel-checked proof is not a matter of opinion.
Rejected for this study on three grounds.

- **Difficulty is not tunable at the granularity a resource-to-solution curve needs.** A lemma is
  typically proved or not; there is no dial comparable to clause density that moves the success rate
  smoothly across a calibration window.
- **Fresh post-freeze generation is the weak point.** Generating genuinely open *statements* at
  controlled difficulty is itself an unsolved problem; drawing from an existing corpus reintroduces
  the memorisation route this study's brief specifically excludes.
- **It would duplicate toolchain work.** `lane-mex3` is assessing Lean feasibility on LUNARC. Per the
  brief, that work is not duplicated here, and no toolchain request was made of that lane.

Recorded as the natural second family for a future ME-F2 if `lane-mex3` establishes the toolchain and
a difficulty dial.

---

## 4. F3 — program synthesis against hidden tests

Verification is mechanical and the openness is real, but the specification must be **externally
authored** for the endpoint to be honest, and authoring a fresh post-freeze specification corpus is a
substantial project in its own right. Writing the specifications inside this lane would put the same
hand on the task and the scoring, which is the failure mode the brief's "no hidden oracle the arms
could have been tuned on" clause exists to prevent.

---

## 5. F4 — real defect repair

The naturalistic arm of exactly this question, and **already funded**: `lane-e30r12` is re-running the
BugsInPy confirmatory suite under the fixed patch emission. Duplicating it would waste channel
capacity that lane needs. It also carries a memorisation route a fixed public corpus cannot avoid,
which is precisely the weakness that the freshly generated family does not have. The two are
complementary: F4 is naturalistic with a memorisation risk; F1a is controlled with none.

---

## 6. Channel feasibility (measured, 2026-09-02)

| Question | Finding |
|---|---|
| Where do the glm credentials live? | LUNARC only (`https://api.z.ai/api/anthropic`, requesting `glm-5.2`). Not on the Mac. |
| Does the z.ai channel substitute models? | **Yes, silently.** A `glm-5.2` request is served `glm-5.3`, HTTP 200, no warning (issue #45). Disqualifying for a call-matched budget. |
| Codex CLI: latency | **measured** 10.1 s for a short control prompt; **20 s** for a full campaign prompt |
| Codex CLI: tokens | **measured** 20.7–21.1 k per call (the CLI's own system prompt dominates) |
| Codex CLI: structured output | **measured** working via `--output-schema` + `--output-last-message`; strict mode requires **every** declared property to appear in `required`, so optionality must be expressed as a nullable type |
| Codex CLI: served-model attestation | **Not available.** The `model:` header is an *echo of the request* — a probe requesting `definitely-not-a-real-model-xyz` printed that id back verbatim. With `--json` no model id appears at all. |
| Codex CLI: does it substitute? | **No — it refuses.** The bogus-model probe returned rc=1 with an HTTP 400 `not found`. This refusal property, not a faked attestation, is what the fail-closed guarantee rests on. |
| Ground-truth cost | **measured** 3–6 s per campaign at the selected geometry; runs on the Mac, no LUNARC dispatch needed |
| Channel allocation | codex CLI, up to ~8 000 calls, concurrency ≤ 3, coordinator-allocated. z.ai left clear for `lane-e30r12`. |

---

## 7. What the feasibility pass changed in the design

Three things were found by measurement rather than by reasoning, and each changed a frozen constant.

1. **The primary endpoint saturated.** With a single ladder per campaign, two verified events that
   bracket the boundary entail *every* rung by monotone closure. Deterministic arms scored 12/12 at
   `n_vars=40`. The fix is independent sub-ladders ("blocks"), which make an arm buy a bracket in each
   block separately. After the change: `C_UNIFORM_ALLOCATION` 0.575, `B5_ALGORITHMIC_CORE_NO_MODEL`
   0.912 — a wide, control-sensitive band.
2. **The calibration endpoint was a proxy.** The first calibration measured the fraction of rungs a
   uniform policy settles *directly by a tool*, which is not the primary endpoint and was inside the
   window while the primary was saturated at 1.0. Calibration now runs on the primary endpoint itself.
3. **The last action's evidence was unclaimable.** The control loop ended after its final action, so
   whatever that action established could never be claimed. Every arm now receives a **closing call**
   that executes no action and exists solely to emit the final claim sheet.

A fourth was found by an independent reviewer of the code rather than by measurement: the scorer was
not passing the block map into the warrant checker, so monotone closure would have been licensed
**across independent sub-ladders** — inflating warrant validity for every arm.

### The pattern, which is itself the finding

All four are the same shape: **each would have produced a number that looked fine.** None would have
crashed, none would have failed a type check, and none would have been visible in the output. The
saturating endpoint returned 12/12 — a plausible score. The proxy calibration returned 0.6146, sitting
comfortably inside the window, while the endpoint the study actually reports was pinned at 1.0. The
unclaimable final action would have depressed every arm equally, which reads as difficulty rather than
as a bug. The missing block map would have raised warrant validity uniformly, which reads as arms being
well behaved.

The sharpest of them is the second, and it is worth naming precisely: **the calibration was tuning
against a measurement that was not the one the study reports.** That is the same failure shape as the
earlier confirmatory repair study, which came to measure diff syntax instead of reasoning. Four
instances of "the instrument agreed with itself and was pointed at the wrong thing" inside a single
calibration pass is not four unlucky bugs; it is the characteristic failure mode of this kind of
study, and the reason the development split exists.

They are recorded here rather than quietly fixed, because a reader assessing this design is entitled
to know what the development split caught — and because the count matters more than any one of them.

---

*Development numbers are development numbers. Nothing in this table is a result, and no field status,
novelty or publication authority is granted or implied.*
