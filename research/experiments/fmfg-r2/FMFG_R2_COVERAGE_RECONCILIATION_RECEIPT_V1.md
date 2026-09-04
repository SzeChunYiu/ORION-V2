# FM/FG R2 Coverage Reconciliation Receipt (R2 runner-coverage lane, owner issue #48)

**Status:** repair landed; **one frozen terminal is affected and is NOT re-run here.**
**Non-amending.** This receipt adds to the R2 record. `FMFG_R2_REGISTERED_SCALE_DISPATCH_RECEIPT.md`
and `FMFG_R2_SUITE_TERMINAL_RESULTS_RECEIPT.md` are frozen and are byte-untouched.
Machine artifact: `rollup-r2/COVERAGE_AUDIT_R2.json` (auditor exit `6`).
Interpreter for every number below: CPython 3.12.13 / 3.13.12 (never `/usr/bin/python3`, which is 3.9).

## 1. The three numbers

Computed from the archived per-leg `rollup-r2/EVALUATION_SUMMARY_{n80,n96,n120,n160}.json`
and `FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`. `ran` is read out of the
evidence, not multiplied from intent.

| | dispatches |
|---|---|
| **registered** (plan: Σ tasks × per-study arms) | **13,168** |
| **ran** (archived evaluation summaries) | **8,560** |
| **valid** (ran − missing_or_invalid) | **8,560** |

The merged terminal reports `8,560/8,560 valid`. That is true, and it is a rate over the
executed subset presented as completeness. The registered denominator never appears.

## 2. The shortfall is larger than a subset difference — the identity rule decides it

The naive reading (13,168 − 8,560 = 4,608 never ran) assumes the executed dispatches are a
*subset* of the registered ones. They are not. `DEFAULT_ARMS` in the suite runner carried arm
ids that the plan does not register:

- FM studies register `F2_STATIC_NO_TRANSFER_DISCOVERY` / `F2_TRANSFER_DISCOVERY_FULL`;
  the run used `F2_STATIC_NO_FORMAL_DISCOVERY` / `F2_FORMAL_DISCOVERY_FULL` — **registered by no study**.
- FG studies register `CURRENT_FORMALISM_ONLY` and `F0_FORMAL_PARENT_FEDERATION`;
  the run used `TARGET_ONLY_DIRECT` and `F0_PARENT_FEDERATION`.

**Identity rule declared: exact arm-id match.** Under it:

| | dispatches |
|---|---|
| registered **and** ran | 3,056 |
| **registered, never ran** | **10,112** |
| ran, registered for no study | 5,504 |

Both directions close: 3,056 + 10,112 = 13,168 and 3,056 + 5,504 = 8,560.
**3 of 17 registered arm ids were ever executed.** Per-study, FM studies matched 3 of their
6–9 registered arms; every FG study matched exactly **1** (`STRONGEST_DOMAIN_FORMAL_PARENT`).

Every named parent baseline is among the 14 that never ran: `STRUCTURE_MAPPING_PARENT`,
`ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE`, `FCA_PARENT_WHEN_APPLICABLE`.

## 3. The deeper defect: registered arms that could not have been distinct

`arm_instruction()` dispatched by **substring**, with no registry and an unconditional final
`return "Use the smallest justified formal method."`. Consequences, measured against the live
pre-repair function:

- **17 registered arm ids resolved to 6 distinct instructions.** Not one registered arm had an
  instruction of its own.
- `"PARENT" in arm` swallowed **six** arms into one sentence, including all three named parent
  baselines and both federation ids. Had the missing 10,112 dispatches simply been run, the
  campaign would have published `13,168/13,168` coverage over six duplicate parent arms.
- `SEMANTIC_RETRIEVAL`, `SEMANTIC_RETRIEVAL_OF_EXISTING_FORMALISM` and
  `LOCAL_PATCH_OR_EXTRA_VARIABLE` matched nothing and fell through to the generic default —
  **byte-identical to what an entirely fabricated arm id received** (control: a made-up id
  returned the same sentence). A named control arm running an unnamed default procedure.

This is why "read the plan's arm list" is necessary and not sufficient, and why the repair
carries a constructibility clause.

### 3.1 Two of the five executed arms were the same arm

`F0_PARENT_FEDERATION` and `STRONGEST_DOMAIN_FORMAL_PARENT` received **byte-identical**
procedures. On the pure-executor stock they are a same-procedure pair at 0.8263 and 0.8166 —
and those are the **maximum and minimum of all five arms**. So the terminal's five-arm ordering
cannot be read as five distinct arms ranked: its two extremes are one arm wearing two labels.

This withdraws the *ranking* claim. It does **not** establish a noise floor: one same-procedure
pair is a single draw, not an estimate of the null distribution, and a 12-task gap between
identically-instructed arms is consistent both with chance and with a real 12-task effect
elsewhere in the table. The narrower statement is the defensible one, and it is the only one
made here.

## 4. The repair

**Root cause, three levels down.** (1) The receipt published one ratio. (2) `evaluate()` computed
`run_valid` per arm over the arm list it was *handed*, so unrun arms contributed no rows.
(3) The campaign was dispatched through the low-level harness with a silent default arm set,
bypassing `run_formal_discovery_campaign.py` — **which already reads the plan's per-study `tasks`
and `arms` correctly** and has done since wave 6. The defect was never an inability to read the
plan; it was that nothing detected the bypass. The repair therefore hardens detection rather than
duplicating plan-reading into a second reader.

- **`scripts/run_formal_discovery_generated_suite.py`** — `DEFAULT_ARMS` deleted; `--arms` is now
  **required** on `prepare`/`dispatch`/`evaluate`. A campaign-scale run can no longer inherit an
  arm set nobody chose. `evaluate()` takes the registered list *independently* (defaulting to the
  arms frozen at prepare, never to the executed ones) and publishes
  `registered_dispatches` / `ran_dispatches` / `valid_dispatches` plus the set differences **by name**.
- **`scripts/orion_formal_discovery_arms.py`** — substring dispatch replaced by an exact-id
  registry. An unknown id raises `UnregisteredArm`; a registered id with no designed procedure
  raises `UnspecifiedArmProcedure`. Each yields its **own** response status
  (`EXECUTION_FAILED_ARM_UNREGISTERED`, `EXECUTION_FAILED_ARM_PROCEDURE_UNSPECIFIED`), distinct from
  `EXECUTION_FAILED_MODEL_RESPONSE`, so "this arm was never built" can never be filed as "the
  backend was flaky". **No arm procedure was invented** — designing the three undesigned procedures
  is the owning lane's design act, so their absence is *recorded*, not filled in.
- **`scripts/run_formal_discovery_campaign.py`** — `evaluate()` derives executed arms from the
  filesystem (evidence) and the denominator from the plan (registration); `status()` reconciles
  instead of reporting `prepared/dispatched/evaluated` booleans.
- **`scripts/audit_formal_campaign_coverage.py`** (new) — standalone reconciliation.

**Frozen-lane reproducibility preserved.** All five arm ids R2 actually executed return
byte-identical instruction text before and after; 14 of the 17 registered ids are unchanged. Only
the three never-designed arms now refuse. The frozen campaign remains reproducible.

### 4.1 Gate reachability — deliberately two clauses, not one

`COVERAGE` and `CONSTRUCTIBILITY` are **separately failable**, with bitwise exit codes:
`0` both satisfied · `2` coverage violated · `4` constructibility violated · `6` both ·
**`8` COULD NOT CHECK** (plan unreadable, evidence absent, arm table unimportable) — distinct from
every "checked and fine" and every "checked and failed".

A single gate demanding both is **unsatisfiable on the current arm table** (17 ids → 6 procedures),
and an unsatisfiable gate terminates on vocabulary rather than on evidence. Tests assert all four
states are reachable, including `0`: coverage-fails-alone, constructibility-fails-alone, both, and
**both satisfied together**. The no-alarm case is asserted as hard as the alarm case, and the CI
step checks the auditor fires on the archived R2 evidence (exit 6), stays silent on an honoured
plan (exit 0), and returns 8 on absent evidence.

## 5. Blast radius

**AFFECTED — frozen terminal. Named, and NOT re-run.**

- `research/experiments/fmfg-r2/FMFG_R2_SUITE_TERMINAL_RESULTS_RECEIPT.md` — verdict
  **`REGISTERED_SCALE_NULL`**, merged in PR #102. Its §1 is headed
  "Execution completeness (8,560/8,560 valid)". Re-running it against the registered arm set is a
  **new design, not a repair**, and would additionally require the owning lane to design the three
  undesigned arm procedures first. This lane stops here.

**Direction of the bias — it cannot rescue the mechanism.** The under-executed side is the
**comparator** side: all three named parent baselines, both federation ids, the fixed-lesson and
retrieval controls. The treatment arms (`F2_*_FULL`) ran at full registered task counts. A campaign
that under-executes parents **understates parent strength**. Running the missing arms could only
raise the parent envelope, pushing further toward **`PARENT_SUFFICIENT`** — a legitimate terminal
under the programme invariants — never toward mechanism superiority. Combined with §3.1, the
correction runs *with* the null, not against it.

**AFFECTED BY IMPORT — reported, not touched (live lanes).**

- `pc-r6/PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1.json` — `pc_status` opens
  `R2_REGISTERED_SCALE_NULL_IMPORTED__…`; it carries the null forward as a status.
- `FORMALISM_GENESIS_BACKLOG_V1.json` — the FG70 execution-order rationale rests on
  "the fmfg-r2 prior shows the other non-frontier suites are ceiling-heavy"; that ceiling
  observation covers only the 5 executed arms.

**NOT AFFECTED (checked, not assumed).**

- `fg/FG70_OUTCOME_RECEIPT.md`, `fg/FG_PARENT_FIDELITY_RECEIPT_V1.md` — both explicitly disclaim
  data dependence (deterministic, zero model calls, no shared generator/oracle/arm/task). They
  *quote* "1,712 tasks × 5 arms = 8,560 dispatches" as a description of the campaign; that
  description would now be more complete stated as 13,168 registered / 8,560 ran. A citation to
  refresh, not a terminal to reopen. Left to the FG lane.
- `pc-r7` (cites only the plan's `generated_results_alone_grant_…=false` rule),
  `me-x6/ME_X6_COMPARATOR_PROVENANCE_AND_NON_FIDELITY_RECEIPT_V1.md` (list mention only; its
  observation that fmfg-r2 carries no comparator-fidelity establishment is corroborated),
  `V2_COMPUTATION_ONLY_SUCCESSOR_BACKLOG_V1.json` (pointer only).
- `FM80_NATURALISTIC_TRANSFER_DECISIVE_PROTOCOL_V1.json` carries the timing marker
  `FROZEN_BEFORE_FMFG_R2_TERMINAL`. **Reference reported; its repair branch is not selected here** —
  that is the executing lane's design act.

## 6. P-F is not reopened

The FG80 / P-F verdict **stands, unchanged**. Mechanically checked: FG80's three registered arms
that never ran — `LOCAL_PATCH_OR_EXTRA_VARIABLE`, `SEMANTIC_RETRIEVAL_OF_EXISTING_FORMALISM`,
`FIXED_FORMALISM_LESSON_INJECTION` — are **all additional controls**. The treatment
(`F2_FORMALISM_GENESIS_FULL`) ran at the full registered 80 tasks under the legacy id
`F2_FORMAL_DISCOVERY_FULL`, which resolves to the identical `F2_FULL` procedure.

One precision the coverage repair forces: under the exact-id rule FG80's 42/80 comparator is
labelled `TARGET_ONLY_DIRECT` where the registered direct control is `CURRENT_FORMALISM_ONLY`.
Both resolve to the **same `DIRECT` procedure**, so the comparator is behaviourally faithful and
the contrast is intact — the mismatch is in the label, not the arm.

The full machine-native arm at 23/80 against 42/80, last of five arms, **−23.75 pp**, exact paired
McNemar **p = 4.3e-03**, is a measured negative in the direction opposite the hypothesis. Nothing in
this reconciliation moves it, and this repair must not be read as grounds to reopen it.

## 7. Authority

No scientific-truth, F2-superiority, new-mathematical-theory, field-status, R3 or R4 grant.
This receipt reports execution coverage and repairs tooling; it establishes no outcome and
promotes no terminal.

skills-applied: none (coverage/repair receipt, no manuscript content)
