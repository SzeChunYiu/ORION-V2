# FG80 R3 — pre-dispatch receipt (V1): the P-F negative attributed to one stage, the re-run frozen

```text
FG80_R2_REGISTERED_TERMINAL  = REGISTERED_SCALE_NULL (suite) / F2_FULL 23/80 vs DIRECT 42/80, p 4.3e-03 (FG80)   -- UNCHANGED
P_F_TRIGGER_TERMINAL         = NO_R2_EFFECT_TO_EXPLAIN__P_F_STANDALONE_ROUTE_CLOSED_OR_MERGE                    -- UNCHANGED
CENSUS_CLASS                 = DESCRIPTIVE, NON-GATING (four controls PASS)
ATTRIBUTION                  = ANSWER_ENCODING_AT_THE_INTERFACE  (failure-ledger class FREE_TEXT_CATEGORICAL_ENDPOINT)
R3_STATE                     = FROZEN (design + twin + suite, seed 20260904, 400 dispatches) -- DISPATCH DEFERRED TO THE FROZEN CHANNEL'S WINDOW
GRANTS_SCIENTIFIC_TRUTH = false   GRANTS_F2_SUPERIORITY = false   FIRES_THE_P_F_TRIGGER = false
```

## 1. The negative

The P-F trigger receipt records the full machine-native arm last of five on FG80 (23/80 against
the simple direct control's 42/80, −23.75 pp, paired exact p = 4.3e-03), both voiders closed, the
trigger not fired, the standalone route closed. Per the R2 erratum (#270), the five ids are four
procedures and the three never-run registered arms are controls, not the treatment. Nothing in this
receipt reopens any of that.

## 2. Attribution to ONE stage — the rendering census

`fg80_r3.py census` re-reads every wrong FG80 row of the archived R2 evaluation rows (sha256
custody asserted against the billy-old originals for all four R2 legs) and asks: *is the actual
answer the expected answer rendered differently?* The normalisation is conservative by
construction — a second feature id, any connective (word or symbol), any negation, or a `= 0` in
the tail keeps the row **wrong**; only pure decoration of the correct id collapses.

**Controls, evaluated before anything was read as a finding (all PASS):**
`R2_FG80_EXACT_COUNTS_REPRODUCED` (42/33/34/32/23 from the archive, tying it to the receipt);
`DETECTOR_FIRES_ON_PLANTED_VARIANT` (a non-FG80 wrong row with its expected leaves decorated);
`DETECTOR_SILENT_ON_A_DIFFERENT_ANSWER` (a conjunction that shares the correct id);
`NO_RENDERING_VARIANTS_OUTSIDE_FG80` (211 + 122 + 4 wrong rows in the other legs carry
token-shaped expected leaves, so the detector had something to fire on there, and fired on none).

| arm | exact (registered) | rendering-variant wrongs | semantic (descriptive) |
|---|---|---|---|
| `TARGET_ONLY_DIRECT` | 42/80 | 34 | 76/80 |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 33/80 | 40 | 73/80 |
| `F0_PARENT_FEDERATION` | 34/80 | 42 | 76/80 |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | 32/80 | 44 | 76/80 |
| `F2_FORMAL_DISCOVERY_FULL` | 23/80 | 50 | 73/80 |

Paired `F2_FULL` vs `TARGET_ONLY`: **exact b = 30, c = 11, Δ = −19, p = 4.3e-03; semantic
b = 4, c = 1, Δ = −3, p = 0.375.** Sixteen of the nineteen discordant tasks are decoration of the
correct id. The observed decorations, by count across all arms: ` = 1` (187), ` is active
(value 1)` (7), `=1` (4), ` is 1` (4), ` is true` / ` is true (1)` / ` equals 1` (2 each), and
singletons; the 25 tails carrying another id, a connective or a `= 0` stay wrong.

**The stage.** R2 typed the field as a free `"string"`
(`run_formal_discovery_generated_suite.py:79`), scored by exact canonical-JSON equality, and no
arm's procedure text mentions encoding. What FG80 measured was mostly whether an arm's prose habit
emits the bare token — and the full arm's procedure text (*"inspect structural relations,
invariants, …"*) plausibly invites `H_X = 1` more often (50 of 80) than *"solve directly"* does
(34 of 80). That is an interface property, not a decision-procedure property. Ledger class:
`FREE_TEXT_CATEGORICAL_ENDPOINT`.

**What this is not.** Descriptive. It alters no registered terminal, does not fire or un-fire the
P-F trigger (a predicate over the frozen R2 campaign), and licenses no claim about the arms. It is
the diagnosis on which the frozen design rests; the design is its test.

## 3. A pre-outcome repair, disclosed

The first detector normalised `H_A AND H_B` to `H_A`: its regex `^([A-Z]_[A-Z]{6})\b` matched at
the space. The selftest caught it (`census: conjunction is NOT a rendering variant` FAILed) before
the census was read. The repair keeps a row wrong whenever the tail carries another feature id, a
connective word or symbol, a negation, or a `0`; the selftest now asserts every tail form observed
in R2 in both directions (7 decorations collapse, 5 non-decorations do not). The uncorrected census
counted 35/42/43/45/52 rendering variants and p = 0.625; the corrected one is the table above. Both
are recorded; only the corrected one is cited.

## 4. The lever and the frozen re-run

**Lever on the interface, symmetric:** the categorical crosses as a categorical — named in the
contract, enumerated in the output schema, rejected on non-membership, with an encoding instruction
that forbids decoration. Applied to every arm identically. Scorer, budget, arm texts, generator and
channel untouched (the last three imported from the frozen R2 modules, not copied).

**Frozen:** `FG80_R3_INTERFACE_RERUN_DESIGN_V1.{md,json}` (constants asserted equal by the
selftest), `FG80_R3_FROZEN_SUITE_V1.json` (seed 20260904, 80 tasks × 5 arms; private-oracle
sha256 `b219f0e0…`, public-tasks sha256 `3e7b7319…`, design sha256 `2affb21f…`), commit `d6eda4c`.
The freeze regenerated on the execution host is byte-identical (`cmp` exit 0 on
`FROZEN_SUITE.json`). Routing rows 0–4 are registered, the ceiling row is named as *no dynamic
range*, and the pre-run expectation (every arm at 0.91–0.95; row 1) is written down before dispatch
so a ceiling cannot be read afterwards as support.

**Dispatch state.** The frozen channel (R2's instrument, codex-cli 0.147.0 side-by-side /
`gpt-5.6-terra` on billy-old) answered the pre-dispatch probe with a channel-unavailable response
(the script's exit-6 class: nothing dispatched, nothing scored). The campaign Messages-API channel
was probed as the alternative and answered in the same class. No third channel with programme
precedent exists (no `api.anthropic.com` served id is recorded anywhere under `research/`). The
design is therefore **not** amended: a deferred dispatcher (`~/sd10run/fg80_r3_deferred_dispatch.sh`
on billy-old, pid 1751039, log `~/sd10run/logs-fmfg/fg80-r3-deferred.log`) waits for the frozen
channel's window, retries `run` (idempotent — existing responses are skipped, a mid-run drop exits 6
and is retried, a `CANNOT_CHECK` stops it), then runs `evaluate`. The outcome receipt is written
when the rollup exists, under the routing frozen here, and not before.

## 5. What the three hypotheses look like from here

| hypothesis | reading |
|---|---|
| (a) the controller's decision procedure is worse | not supported by the census: at the decision level the full arm is 73/80 against 76/80 (p 0.375) |
| (b) handicapped by its own prompt | only in the narrow sense that its procedure text invites decoration; the decoration is scored, the decision is not |
| (c) the suite rewards what it does not do | **this is the census finding, at descriptive strength** — FG80's exact-match contract rewarded the bare-token habit; R3 tests it prospectively |

## 6. Discipline

Archive custody sha256-asserted at load; selftest 30/30 (including every routing row reachable
and the design twin's constants); freeze deterministic and seed-sensitive (asserted); oracle
commitment before dispatch, file absent during every call, restored and re-hashed after; served
model not exposed by the CLI and reported as unavailable, not as a pass (`UNPINNED_SUBSTRATE_CONDITION`
carried, not cleared); `/usr/bin/git` for every decision; interpreter CPython 3.13.12 (Mac) and
3.14.4 (execution host, stdlib only).

skills-applied: none (receipt, no manuscript content)
