# FG80 R3 — the P-F negative attributed to one stage, and re-tested under a categorical contract (Design V1, frozen before dispatch)

**Class:** prospective re-run of FG80 — 80 fresh tasks from a committed seed, the same five arms,
the same single-call budget, the same exact-match scorer, R2's own model channel — with **one**
change applied to every arm identically: the categorical endpoint crosses the interface **as a
categorical**. **Machine-readable twin:** `FG80_R3_INTERFACE_RERUN_DESIGN_V1.json` (the selftest
asserts its constants equal the script's). **Runner:** `fg80_r3.py` (`selftest` / `census` /
`freeze` / `run` / `evaluate`).
**Lineage:** FM/FG R2 (`fmfg-r2/`, terminal `REGISTERED_SCALE_NULL`; FG80 n80 leg
`F2_FORMAL_DISCOVERY_FULL` 23/80 vs `TARGET_ONLY_DIRECT` 42/80, paired exact p = 4.3e-03), the R2
erratum (#270: four distinct conditions, not five; federation claim withdrawn), the P-F trigger
evaluation (`NO_R2_EFFECT_TO_EXPLAIN__P_F_STANDALONE_ROUTE_CLOSED_OR_MERGE`, voiders closed).

## 1. The negative, and the one stage it is attributed to

The P-F trigger receipt records the full machine-native arm **last of five** on FG80, −23.75 pp
against the simple direct control, and closes both voiders (executor purity, budget realisation).
The loss is real under the R2 analysis contract, and nothing here reopens it.

A negative is intermediate until it is attributed to one stage. The descriptive, non-gating census
in `FG80_R2_RENDERING_CENSUS_V1.json` re-reads every wrong FG80 row of the frozen R2 archive
(sha256 custody against the billy-old originals; four controls, all PASS, including the R2 exact
counts reproduced 42/33/34/32/23 and the detector fired on a planted variant and silent on a planted
different answer) and asks one question of it: *is the actual answer the expected answer rendered
differently?* The normalisation is conservative — a second feature id, any connective, any
negation, or a `= 0` in the tail keeps the row **wrong**; only pure decoration of the correct id
(`H_X = 1`, `H_X is active (value 1)`, `H_X is true`) is collapsed.

| arm | exact (registered) | rendering-variant wrongs | semantic (descriptive) |
|---|---|---|---|
| `TARGET_ONLY_DIRECT` | 42/80 | 34 | 76/80 |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 33/80 | 40 | 73/80 |
| `F0_PARENT_FEDERATION` | 34/80 | 42 | 76/80 |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | 32/80 | 44 | 76/80 |
| `F2_FORMAL_DISCOVERY_FULL` | 23/80 | 50 | 73/80 |

Paired `F2_FULL` vs `TARGET_ONLY`: exact **b = 30, c = 11, Δ = −19, p = 4.3e-03**; semantic
**b = 4, c = 1, Δ = −3, p = 0.375**. Sixteen of the nineteen discordant tasks are decoration.
Zero rendering variants exist outside FG80 (the other thirteen studies have no free-string
categorical endpoint), so the artifact is confined to the one study that carried the P-F trigger.

**Stage:** `ANSWER_ENCODING_AT_THE_INTERFACE`. R2 typed `representation_feature` as a free
`"string"` (`run_formal_discovery_generated_suite.py:79`), no arm's procedure text says anything
about encoding, and the scorer is exact canonical-JSON equality. What R2 measured on FG80 was
mostly whether an arm's prose habit happens to emit the bare token. Not the arm's decision.

**What the census is not.** It is descriptive. It changes no registered R2 terminal, it does not
fire or un-fire the P-F trigger (a predicate over the frozen R2 campaign), and it grants nothing.
It is the diagnosis the design below is built on, and the design is the test of it.

## 2. The lever — on the interface, symmetric, never on the scorer or an arm

`answer_contract` names the admissible values (`representation_feature ∈` the task's four feature
ids; `target_decision ∈ {YES, NO}`); the output schema enumerates them (`enum`); the encoding
instruction names them and forbids decoration; `validate_answer` rejects any non-member, and a
rejected answer makes the run **invalid** (`CANNOT_CHECK`) — it is never rescored. Every arm gets
the same contract, the same instruction, the same single call. The generator (`gen_fg80`) and the
five procedure texts are **imported** from the frozen R2 modules, not copied; the selftest asserts
the F2_FULL prompt carries R2's procedure text verbatim.

Untouched: the scorer, the budget, the channel, the arm set, the arm texts.

## 3. Frozen constants

| constant | value |
|---|---|
| seed | 20260904 (committed here before `freeze`; `freeze` is deterministic from it, selftest-asserted) |
| tasks × arms | 80 × 5 = 400 dispatches |
| treatment / parent | `F2_FORMAL_DISCOVERY_FULL` / `TARGET_ONLY_DIRECT` |
| statistic | paired McNemar exact, two-sided, on the discordant pairs (R2's; selftest reproduces R2's 4.32e-03 from 30/11) |
| α / ceiling | 0.05 / 0.90 |
| channel | R2's instrument: `codex exec`, side-by-side codex-cli **0.147.0** at `~/.npm-terra/bin/codex` on billy-old, requested `gpt-5.6-terra`, `--output-schema`, concurrency 3 |

**Arm identity.** Per the R2 erratum, `F0_PARENT_FEDERATION` and `STRONGEST_DOMAIN_FORMAL_PARENT`
are one procedure under two labels. R3 keeps all five ids so its rows align with R2's row-for-row,
reads **four** distinct conditions, and makes no federation claim.

## 4. Controls, consumed by the routing

| control | rule |
|---|---|
| `CENSUS_CONTROLS_ALL_PASS` | the four census controls PASS in the committed census |
| `FREEZE_DETERMINISTIC` | two generations from the seed are byte-identical; a different seed changes the tasks |
| `ORACLE_COMMITMENT_ROUND_TRIP` | oracle sha256 committed before dispatch; file absent during every call; restored file matches |
| `DISPATCH_COMPLETE_AND_VALID` | 400/400 `COMPLETED_PROPOSAL_ONLY` with in-enum answers; any failure or out-of-enum answer invalidates the run |
| `REQUEST_MODEL_UNIFORM` | every `requested_model` equals the pin; the **served** id is not exposed by the CLI and is reported as unavailable, not as a pass |

## 5. Registered routing

| row | condition | terminal |
|---|---|---|
| 0 | a control fails / treatment or parent run invalid | `CANNOT_CHECK__INCOMPLETE_OR_INVALID_DISPATCH` (exit 5) |
| 1 | both ≥ 0.90 and p > 0.05 | `FG80_AT_CEILING_UNDER_A_CATEGORICAL_CONTRACT__NO_DYNAMIC_RANGE_FOR_THE_P_F_TRIGGER` |
| 2 | c > b, p ≤ 0.05 | `F2_FULL_ABOVE_DIRECT_AT_THE_SEMANTIC_LEVEL__CANDIDATE_ONLY__REQUIRES_ITS_OWN_TRIGGER_PROTOCOL` |
| 3 | b > c, p ≤ 0.05 | `F2_FULL_BELOW_DIRECT_AT_THE_SEMANTIC_LEVEL__THE_R2_DEFICIT_IS_NOT_A_RENDERING_ARTIFACT` |
| 4 | otherwise | `NO_SEMANTIC_CONTRAST__R2_DEFICIT_ATTRIBUTED_TO_THE_INTERFACE` |

Row 1 is a **ceiling control named as a ceiling**: it reads as *no dynamic range*, never as a tie
the mechanism earned. Row 2 cannot fire the P-F trigger; it licenses only a prospectively frozen
trigger protocol of its own. Row 3 keeps the negative and moves the attribution to the arm's
procedure — hypothesis (a) architecture or (b) mandate, to be split by a later single-lever test.
Rows 1 and 4 place the R2 deficit at the interface — hypothesis (c), the suite.

## 6. Pre-run reachability audit (failure-ledger classes)

- **Seed does something:** asserted both ways by the selftest.
- **Hard gate at scale:** `evaluate` is 400 file reads; the path is exercised end-to-end by the selftest.
- **Contrast could exist:** b and c each range over 0..80; every routing row is reached by the selftest on synthetic inputs.
- **Clause narrowing:** the runner evaluates exactly §5; the selftest asserts the JSON twin's constants equal the script's.
- **Parent isolation by information or budget:** none — one call, one task, one contract, one instruction per arm; the only per-arm bytes are `ARM:` and `ARM PROCEDURE:`, as in R2.
- **Served-model id:** **not** pinned by the channel (`UNPINNED_SUBSTRATE_CONDITION`, the residual R2 carries). Disclosed, not cleared. The primary is a within-run paired contrast dispatched from one interleaved pool, so a substitution would have to be arm-selective to bias it.
- **Unsatisfiable / unfailable clauses:** none — validity is a precondition, the ceiling row and the null row are both reachable and both distinguished from each other.

## 7. Pre-run expectation, disclosed

The census predicts every arm at 0.91–0.95 under the contract; **row 1 is the expected terminal.**
Stated before dispatch so that a ceiling cannot be read afterwards as a surprise or as support.

## 8. No-rescue clause

No constant, arm set, contract, routing row, seed, scorer or channel changes after dispatch
begins. A defect found afterwards is recorded in the receipt and repaired under a new identity.

skills-applied: none (frozen design, no manuscript content)
