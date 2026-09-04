# E40 — line closure receipt V1

**Scope:** what closure of the E40 line requires under the registered design, the revival attempt
the programme demands before a negative is filed, and the disposition that follows.
**Lineage:** m1 (`rollup-r2`), m2, m3, m4, m5′ Stage-1, Stage-2c, Stage-2d, and Stage-2e (frozen
in PR #253, run under the operator's standing compute authorization of 2026-09-02, *"run all the
computation tasks.. finish all the researxh asap"*, reaffirmed 2026-09-03 as *"you will fix
everything"*).

## 1. The negative, as measured

Every routed primary across the E40 line puts the **parent ahead of the mechanism**. All figures
below are reproduced from the archived rollup JSON in this directory, not from prose.

| stage | cycle-1 prompt rule | contrast | mean_d | perm p | wins (f2 / f0) | controls |
|---|---|---|---|---|---|---|
| m1 (`rollup-r2`) | none | F2_final vs F0_best | −0.000968 | 0.625 | 2 / 4 (6 ties) | PASS |
| **m2** | **none — mandate-free** | F2_final vs F0_best | **−0.008979** | 0.9990 | **1 / 11** | PASS (planted 1.0) |
| m3 | regime-extreme anchor | F2_final vs F0_best | −0.007414 | 0.9861 | 2 / 10 | PASS (planted 0.9877) |
| m4 CT1 | (shipping counterfactual) | f2_ship − f0_best | −0.011271 | 0.99951 | 1 / 11 | PASS |
| 2c G0 | seed mandate | TERMINAL | −0.009778 | 0.99976 | 1 / 11 | **planted FAIL → run voided** |

`mean_d` is on `wasserstein_distance.mean` where lower is better, in the m-series convention where
negative means the parent (F0) is better. The effect is consistent in sign and size, −0.007 to
−0.011, across four independent campaigns and three different cycle-1 prompt forms. m1 is the
underpowered pilot (6 of 12 cells tied) and is reported for completeness, not as support.

## 2. What closure actually requires under the registered design

Read from Stage-2c design §6, not inferred from the receipts:

| registered row | condition | route |
|---|---|---|
| 1 | G1 ∧ G2 ∧ G3 ∧ G4, G0 passed | authorize m6 under its own freeze |
| 2 | G0 passed, any of G1–G4 fails | **E40 line TERMINAL** |
| 3 | G0 failed | CANNOT_CHECK; diagnose mechanics before re-dispatch |

For completeness on how the line reached Stage-2c at all: m4's own routing row that fired
(`G2 ∧ ¬G1`) **authorized drafting m5′**, it did not terminate anything. Only m4's `¬G1 ∧ ¬G2` row
mentions leaving the line "terminal-negative", and that row did not fire. m4's CT3 TP family
appears in neither G1 nor G2 — it is a reported contrast, not a gate-bearing one (verified against
`E40_M4_SHIPPING_OPERATOR_COUNTERFACTUAL_DESIGN_V1.md` §3–§5).

Two facts follow, and both must be stated plainly:

1. **`E40_TERMINAL` is available only from a valid probe run.** Stage-2c computed the row-2 gate
   pattern (G0 pass, G1/G2/G4 fail) but its registered planted positive control FAILed, so no
   verdict was admissible. Row 2 has never been reached by a valid run.
2. **The design contains no registered row for "a registered control failed."** The Stage-2c
   receipt mapped that event onto row 3, reasoning that it is "the same class of event — the
   campaign cannot answer its question." That mapping is the receipt's judgment and is defensible,
   but it is **not literally registered**, and this receipt does not pretend otherwise. There is
   therefore no pre-registered disposition that terminates the E40 line without a valid probe run.

So closure requires either (a) a valid re-run of the seed-replica probe — the last named lever in
the m4/m5′ routing — or (b) a **new, distinctly named** disposition establishing that the probe
cannot be validly executed at all. Option (b) is not a repackaging of row 2; a precondition
terminal and a science terminal are different claims and are kept apart throughout.

## 3. The checker repair, and why it does not unblock closure

`E40_M5P_STAGE2C_CHECKER_REPAIR_RECEIPT_R1.md` records the fix in full. In summary: the Stage-2c
analysis read its control verdicts but never consumed them, so it emitted `E40_TERMINAL` while the
planted control was FAILing. `evaluate_gates()` now takes the verdicts as a mandatory argument and
refuses to route, with a **distinct** disposition and exit code for "a control failed" (4) versus
"a control could not be obtained" (5).

Validated against the real archived campaign: the archived verdicts route
`CHECKER_INVALID__NO_VERDICT`; the no-alarm twin (identical numbers, planted PASS) still routes
`E40_TERMINAL`; the five computed gate values are unchanged. A mutation test confirms the guard
has teeth.

**The repair returns the same disposition the Stage-2c receipt applied by hand.** That is the
honest outcome and it is worth saying directly: the 2c verdict was voided because the checker was
invalid, and a valid checker voids it too. The repair buys correctness going forward, not closure.

The planted control's 0.6412 was never a checker bug. It was the checker correctly reporting that
a seed-mandated arm cannot follow an informative feedback channel on `glm-5.3`. Making it pass
would be outcome tuning and is forbidden by Stage-2c design §9.

## 4. Revival attempt — attribution, lever, re-test

A negative is INTERMEDIATE until a revival has been attempted. This is that attempt.

**Attribution to ONE stage.** Stage-2d did the work and filed `PROMPT_IMPLICATED (D2)`: on the
same served model that failed in Stage-2c, the mandate-free arm recovers the planted optimum by
cycle 2 and holds it (0.9877 PASS), while the seed-mandated arm freezes at one point in the
decision space for all nine cycles (0.0233 FAIL). The failure is **mandate-induced exploration
collapse**; the model channel is exonerated as a sufficient cause.

This reproduces in the live Stage-2c arm, not just its control. A read-only config census of the
48 live F2 chains (descriptive, non-gating) finds **15 of 48 chains held a single non-seed config
for all four cycles**, 25 held two, and only 8 held three or four.

**The lever: remove the mandate.**

**The lever splits into two claims, and they do not have the same status.** The mandate broke the
*probe's* planted control; it is not, on its face, a statement about the drag. So the re-test has
two halves and this receipt keeps them apart:

| claim the lever bears on | is a mandate-free re-test available? |
|---|---|
| **(a) the drag** — does the parent still beat the mechanism without a cycle-1 mandate? | **Yes, and it is already valid: m2.** Result below. |
| **(b) the probe** — does a mandate-free arm restore a passing planted control and let the seed-replica gate be read? | **No. m2 has no replicas, no J, no G1/G2 — it never ran the probe.** This half is open, and Stage-2e (§6) is what addresses it. |

**(a) The re-test against the strongest parent — and its result.** The mandate-free condition is
not hypothetical: it is **m2**, whose `f2_prompt` in `scripts/e40_matched_runner.py` carries no
cycle-1 rule at all (verified by reading the source, not by trusting Stage-2d's summary table).
Under it, with all controls passing and the planted control at 1.0:

> the parent still beats the mechanism **11 cells to 1**, mean_d **−0.008979**, perm p **0.9990** —
> the same size as under the regime anchor (−0.007414) and the seed mandate (−0.009778).

**Removing the mandate does not restore the mechanism's performance on the drag.** The revival
lever was identified, followed, and for claim (a) it does not rescue the result: the negative is
earned. This also answers Stage-2d §4's stated worry that the Stage-2c G0 drag might itself be a
mandate artefact — the drag reproduces in a mandate-free arm, at the same magnitude.

**(b) remains open on the evidence in hand.** Nothing above tells us whether a mandate-free arm
would yield a *readable* seed-replica probe, because no mandate-free arm has ever run one. Worse,
there is a structural tension to confront first: the probe's replica mechanism **is** the seed
mandate — mandating different seeds is how the four replicas are made independent — so the obvious
fix (drop the mandate) removes the very thing that creates the replicas. A way out exists and is
cheap: inject the seed pair **out-of-band**, into `native_run`'s command line, leaving the prompt
byte-identical to m2's mandate-free `f2_prompt`. Before spending a campaign on that, Stage-2e asks
the prior question nobody had asked: whether the probe's statistic can carry signal on this
substrate at all (§6).

**Boundary, carried rather than buried.** m2's served model is unrecoverable (Stage-2c dispatch
receipt §2), so "the drag survives a mandate-free prompt" is established **across two model
epochs**, not *on `glm-5.3`*. Stage-2d showed the same prompt form flipping a verdict across
models (arm B: 0.9877 PASS under the m3-era model, 0.9518 FAIL on `glm-5.3`). Nothing in the
evidence suggests a mandate-free arm on `glm-5.3` would reverse an 11–1 result three times
replicated, but that specific run does not exist and is not claimed.

## 5. The registered secondary that is NOT promoted

The true-positive family favours the mechanism, and does so reproducibly:

| campaign | contrast | mean_d | perm p |
|---|---|---|---|
| m2 secondary | F0_best − F2_final, true_positives | −13.42 (i.e. F2 **+13.42**) | 0.99951 |
| m3 secondary | F0_best − F2_final, true_positives | −13.08 (F2 **+13.08**) | 0.99585 |
| m4 CT3 | f2_ship − f0_best, true_positives | **+14.58** | 0.00073 |
| m4 CT3 | f2_ship − f0_best, corum_tp | **+10.33** | 0.00122 |
| m4 CT3 | f2_ship − f0_best, string_tp | **+28.17** | 0.00171 |

This is a real, three-times-replicated signal, and it is **registered as a non-terminal-bearing
secondary**. m4's terminal was awarded on G2 — proxy-truth ρ ≈ 0, selection at chance — not on the
TP gap. It is not promoted here, and the reason is visible inside m4's own rollup: its
`reproduction.tp_family_by_orientation` block shows the *identical data* yielding p = 0.0049 when
oriented f2 − f0 and p = 0.9958 when oriented f0 − f2. Orientation is a registration choice, which
is precisely why a secondary cannot be allowed to carry a terminal it was not registered to carry.

Named, not promoted: this belongs to a **new line with the TP family as its registered primary**,
not to a rescue of E40.

## 6. The last named lever, and the precondition nobody had checked

Stage-2c design §1 names the seed-replica probe as "the last named lever in the m4/m5′ routing; if
its gate fails, the E40 line is terminal." Its premise is that cycles where **independent
seed-replicas converge on the same output graph** are tracking substrate-determined structure.

Stage-2c reported J = 0.0093–0.0520 (mean 0.0282) and called the statistic degenerate. **That
reading was not established.** The config census shows the replicas were mostly not running the
same config:

| across the 4 replicas of a cell, at one cycle | distinct non-seed configs | cell-cycles |
|---|---|---|
| all four differ | 4 | **26 / 48** |
| three differ | 3 | 19 / 48 |
| two differ | 2 | 3 / 48 |
| all four agree | 1 | **0 / 48** |

So the reported J conflated seed variation with config variation, and the seed-only quantity the
premise is actually about **was never measured**. Stage-2e (design frozen in PR #253) measures it
directly: 34 native `gies` runs, **zero model calls** — every config fixed by the design, so no
prompt, no mandate, no served-model channel, and therefore no channel to drift.

## 7. Substrate facts that must survive into any later reading of this line

1. **The model channel silently substitutes models.** Requesting `glm-5.2` on the E60-lane
   endpoint is served `glm-5.3` at HTTP 200 with no warning field (Stage-2c dispatch receipt §2).
   m2 and m3 logged prompt/response hashes and token counts but **no served model id anywhere**
   across 1,810 files, so their reference model is **INFERRED, not verified**, and is
   unrecoverable. Every m2/m3-based cross-model statement in this receipt carries that.
2. **Pinning a served id does not pin an experimental condition.** Stage-2c pinned `SERVED_MODEL`
   and held it on all 207 logged decision calls — and its planted control still failed, because
   what changed was channel *behaviour*, not channel identity. The same lesson is written in
   E30-R12's 119 correctly-pinned envelopes. An id assertion is necessary and nowhere near
   sufficient.
3. **Consequently Stage-2e was designed with no model channel at all.** Its configs are fixed by
   the design, so there is no request body to drift; the frozen slot table *is* the request-body
   contract, and it is asserted per envelope (design §5) rather than once at dispatch. An envelope
   whose `arguments.json` disagrees with its frozen slot is INHOMOGENEOUS — excluded, counted,
   reported, and it fails the validity gate.
4. **"Could not check" is never "checked and fine."** Both the repaired Stage-2c checker and the
   Stage-2e checker give it a distinct disposition and a distinct exit code (5), separate from a
   failed control (4) and from a clean pass (0).

## 8. Stage-2e result: the last lever cannot be tested on this substrate

`E40_M5P_STAGE2E_OUTCOME_RECEIPT.md` carries the full record. Disposition
**`E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT`**, all controls PASS, 34/34 envelopes
homogeneous, zero model calls.

| quantity | k562 | rpe1 | pooled |
|---|---|---|---|
| seed-only J (same config, seeds differ) | 0.011–0.021 | 0.036–0.051 | **0.030** |
| config-only J (same seed, configs differ) | 0.011–0.015 | 0.037–0.045 | 0.027 |
| determinism repeat J (same run twice) | **1.0** | **1.0** | — |

The substrate is deterministic given a seed and the seed alone erases 97–98 % of the graph: under
`subset_data = 0.05` the seed picks the 5 % cell subsample and the inferred graph is sampling noise
on top of a ~3 % stable core. Stage-2c's J band is exactly this floor. The consensus statistic
therefore has no dynamic range **under any prompt form, mandate, or served model** — none of which
touch the substrate — so the seed-replica gate G1 has nothing to rank, and the open half (b) of the
revival in §4 is closed too: a mandate-free arm cannot rescue a statistic with no range.

Descriptive, non-gating, and worth carrying: **the five knobs the metabolic loop tunes move the
output graph less than the seed does** (config-only 0.027 vs seed-only 0.030). On this substrate the
loop is optimising below the noise floor of its own output. That is not a registered finding of any
E40 stage; it is the constraint that points at the adjacent niche.

## 9. Disposition

**The E40 line is CLOSED, as a well-measured negative whose last named lever is untestable on the
pinned substrate.** Filed disposition: `E40_LINE_CLOSED__NEGATIVE_AND_LAST_LEVER_UNTESTABLE`.

Precisely what that is and is not:

- **It is** the registered drag negative — parent beats mechanism 11–1 (m2, mandate-free), 10–2
  (m3), 11–1 (m4 CT1), reproduced again at 11–1 in Stage-2c's G0 — with the programme's revival
  discipline applied: attribution to one stage (Stage-2d, `PROMPT_IMPLICATED`), the lever followed
  (mandate removed), the re-test on the strongest parent already valid in m2 and **not** rescuing
  the result, and the residual question (a readable probe) resolved by Stage-2e as unanswerable
  here.
- **It is not** the registered `E40_TERMINAL`. That terminal is awarded only by a valid probe run
  with G0 passed and one of G1–G4 failed (Stage-2c design §6, row 2). No such run exists, and
  Stage-2e establishes that none can be produced on this substrate. **The single artifact that
  would award the registered terminal is a valid seed-replica probe run, and it is unobtainable
  without a substrate change — which the design itself classes as a new mechanism class, outside
  the E40 line.** Stated once, plainly: the registered terminal is unreachable, not merely unreached.
- **m6 is not authorized.** No F2 claim, no component claim, no revival of any frozen negative.
- **Stage-2c's disposition stays `CHECKER_INVALID__NO_VERDICT`** and Stage-2d's stays
  `PROMPT_IMPLICATED`; nothing here re-reads either.
- **The TP-family secondary is not promoted** (§5). It is named as the registered primary of a
  possible *new* line, which would need its own freeze and its own orientation registered before
  any data.
- **What a successor line inherits as constraints:** (i) `subset_data = 0.05` on `gies`/weissmann
  puts the loop's whole config space below the seed-noise floor of its output — any mechanism
  claim on this substrate must first show its lever moves the graph more than the seed does;
  (ii) the served model of every E40 stage before Stage-2c is INFERRED, not verified; (iii) a
  cycle-1 mandate of any specificity suppresses exploration on `glm-5.3` (Stage-2d), so mandated
  quantities must be injected out-of-band, never through the prompt.

## 10. Custody of this receipt

Lane branch `lane/e40-closure-20260903` (PR #253). Files: this receipt;
`E40_M5P_STAGE2C_CHECKER_REPAIR_RECEIPT_R1.md`; `E40_M5P_STAGE2E_OVERLAP_PRECONDITION_DESIGN_V1.{md,json}`;
`E40_M5P_STAGE2E_OUTCOME_RECEIPT.md`; `rollup-m5p-stage2e/`; `e40_m5p_stage2e_overlap_precondition.py`;
`sbatch/e40_m5p_stage2e_{r1,eval_r1}.sbatch`; `tests/unit/test_e40_m5p_stage2{c,e}.py`. Every number in
§1, §5 and §8 was re-read from the archived rollup JSON files in this directory by script, not
copied from prose; the m4 CT3 orientation reversal was read from `rollup-m4/…json`
`reproduction.tp_family_by_orientation`. Tests: 37 pass under Python 3.13.12 (project floor ≥3.12);
the Stage-2e selftest passes on the node under the campaign venv (3.11.5) and locally.
