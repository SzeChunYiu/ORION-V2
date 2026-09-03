# H-EXT-2 — Execution-Blocked Receipt (V1)

**Study:** H-EXT-2 `INTERNAL_SALIENCE_GOODHART_REPLICATION` — register row
`research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md#H-EXT-2`.
**Frozen design:** `research/experiments/h-ext2/H_EXT2_SALIENCE_GOODHART_REPLICATION_DESIGN_V1.{md,json}`,
md sha256 `d13c8718997d9671f7fabcba2113a6403e89530c29a2eee97d2cb255de556365`,
json sha256 `f1f28bcd000c118c055660e531eb74eddb8a0140ba220508c900d6168fc69718`.
**Frozen code (verified against the design's own §10 declarations, both match):** runner
`scripts/h_ext2_salience_runner.py` sha256 `a96c3a471a55f9b238bbfa799a8f13676ce50f9083f304a9aedc09cf7be9ba4e`;
screen `research/experiments/h-ext2/h_ext2_salience_screen.py` sha256
`984e352d6ccf0ce8d8ac09c4662642f709081fe9d75a28a4813d594f19a149ce`.
**Checkpoint:** 2026-09-03, against `main` `e79482a219cb21d4fcb9d81fa3f4722b07ed89ae`.
**Machine record:** `results/H_EXT2_EXECUTION_BLOCKED_CHECKPOINT_V1.json`.

## 1. Status

```text
H_EXT2_STATUS                     = EXECUTION_BLOCKED_PRE_DISPATCH
H_EXT2_NATIVE_RUNS_EXECUTED       = 0
H_EXT2_DECISION_CALLS_EXECUTED    = 0
H_EXT2_RUNTIME_PROBE_EXECUTED     = 0        (§3 probe: NOT run -- see §6)
H_EXT2_PROTECTED_RUN_AUTHORIZATION = NEVER_REQUESTED__NEVER_ARMED
H_EXT2_SEED_COMMITMENT_PUBLISHED  = NO       (nothing to commit: no run)
H_EXT2_TERMINAL                   = NONE__STUDY_REMAINS_PROSPECTIVE
H_EXT2_LADDER_STATE               = UNCONSUMED (DCDFG-LIN -> igsp -> grnboost, all untried)
M5P_OBSERVATION_STATUS            = UNREPLICATED__UNREFUTED (single-learner, in-sample, as filed)
```

`EXECUTION_BLOCKED_PRE_DISPATCH` is **not** a member of the H-EXT-2 routing table (§7 of the
design) and is **not** the screen's `CANNOT_CHECK__CAMPAIGN_INVALID`. That route is an
evaluation-time verdict reached *after* dispatch, on campaign evidence, and the screen returns
exit 2 for it. This receipt is reached *before* dispatch, on no campaign evidence. It carries no
ρ, no gate outcome and no claim about the hypothesis, because none was measured. **The m5′
Stage-1 observation is neither replicated nor filed as an artefact by this document.**

## 2. `H-EXT-2-BLOCK-1` — the design's own dispatch licence is unsatisfiable

**One-stage attribution: the registered dependency in design §9.**

§9 reads: *"Dispatch is licensed only after E40-m5′ Stage-2b terminates … Its eval job (controls →
audit → analysis) and outcome receipt define 'terminates'."* The register custody row (checked
this session, unchanged) still reads *"H-EXT-2: design freeze only until Stage-2b terminates;
dispatch under its own identity."* No lane has re-pointed that dependency.

Stage-2b did not terminate. It was cancelled before it ever started, and the stage was superseded.

| probe | result |
|---|---|
| `sacct -j 3563453` (the chain array §9 names) | `3563453_[0-47%8]` — **`CANCELLED by 6350`**, Submit `2026-09-02T06:23:08`, Eligible `2026-09-05T04:45:00`, **Start `None`**, End `2026-09-02T16:43:21`, **Elapsed `00:00:00`**, Reason `BeginTime` |
| LUNARC `campaign-e40-m5p-stage2b/run/` | absent (`find` by directory name across `$HOME`, 0 hits) |
| `E40_M5P_STAGE2B_OUTCOME_RECEIPT.md` on `main` | **does not exist.** Only `E40_M5P_STAGE2B_DISPATCH_RECEIPT_V1.md` is present |
| successor | `3564928` `o2-e40m5p2c-chain`, 60/60 COMPLETED, started `2026-09-02T16:43:22` — one second after 3563453 was cancelled |

**Stage-2c cannot stand in for the dependency.** §9 does not merely require that *something*
ran; it registers two branches, both keyed to an **admissible** parent verdict: *"with G1 passed
on the parent cell, `replica_J` is a validated truth-anchor and G2 is a specificity contrast
against it; with G1 failed, G2 is only an absence-of-anti-ranking check."* Stage-2c's authoritative
disposition is `CHECKER_INVALID__NO_VERDICT` (its planted control failed at terminal quality
0.6412; see `rollup-m5p-stage2c/DISPOSITION_SUPERSEDED.md`, which exists precisely to stop lanes
reading its `gates.disposition` programmatically). Its numeric G1 FAIL is therefore inadmissible.
**Neither registered branch resolves, so G2's registered reading is undetermined** — the gate
would be evaluated with no fixed meaning.

This blocker is documentary: it rests on a job record, an absent directory, an absent file and
the design's own text. It requires no inference about what would have happened.

## 3. `H-EXT-2-BLOCK-2` — the P′ cohort's registered G0 control is already measured FAIL

**Independent of BLOCK-1. Clearing BLOCK-1 alone would not make this study runnable.**

**One-stage attribution: the cycle-1 mandate carried by the P′ prompt policy, on the current
served channel.**

Design G0 is registered **per cohort** and includes *"planted-feedback control PASS (m3
machinery, same prompt policy as the cohort)."* Three code-level facts make that control fully
determined before any campaign exists:

1. **The planted control performs zero native runs.** `control_planted()` in the frozen runner
   loops `ask_config_f2(...)` over 9 cycles against `synth_feedback()` — synthetic feedback from
   a closed-form plant. No `native_run` call appears in it. **`E40M_MODEL` — the study's single
   registered delta — cannot influence it.** The control depends only on (prompt policy, served
   model, plant, PASS rule).
2. **The plant and PASS rule are plant v4 verbatim.** Quality
   `regime_factor(regime) · exp(-((frac-0.8)/0.45)²)`, factors partial 1.0 / observational 0.7 /
   interventional 0.55; PASS = last 3 cycles ≥ 0.9 and no post-arrival dip below 0.8.
3. **The prompts are byte-identical to a control that has already been run.** Rendered locally
   from both frozen sources and compared with `/usr/bin/diff` (exit 0) and sha256:

| cycle | H-EXT-2 P′ (`E40M_CYCLE1_ANCHOR=1`) | Stage-2d `B_REGIME_ANCHOR` | identical |
|---|---|---|---|
| 1 | `93d5f77ebcb9a55332780a8ffa27a3dc49f04ac101bcc304e725c874e3f42e3c` (2113 B) | same sha, same length | **yes** |
| 2, 3, 4, 5, 9 | `737bec1e…`, `f9930ea3…`, `a7fe09d5…`, `4692a21b…`, `5bf1cd37…` (2438 B each) | same shas | **yes** |

| cycle | H-EXT-2 R′ (`E40M_CYCLE1_ANCHOR=0`) | Stage-2d `A_NO_MANDATE` | identical |
|---|---|---|---|
| 1 | `95db82fb0c059df8d6f54b4d6da9d36fe160ac502723dca852e5a2e3a1fde4e1` (1811 B) | same sha, same length | **yes** |

*Controls on that comparison (asserted, not assumed):* R′ cycle-1 ≠ P′ cycle-1 (`True`);
`"CYCLE-1 RULE"` present in P′ and absent in R′; and a deliberately mismatched pair
(`weissmann_rpe1` vs `weissmann_k562`) compares unequal (`False`). The identity is therefore a
finding, not an artefact of a comparison that could only return `True`.

**So H-EXT-2's P′ planted control is, prompt for prompt, the computation Stage-2d already ran on
`glm-5.3`** — and it **FAILED**:

| Stage-2d arm | = H-EXT-2 cohort | verdict | terminal quality | cycle-1..4 qualities |
|---|---|---|---|---|
| `A_NO_MANDATE` (`a2cedcfe…`) | **R′** | **PASS** | 0.98773 | 0.3526, 0.9877, 0.9518, 0.9877 |
| `B_REGIME_ANCHOR` (`9d6de7c8…`) | **P′** | **FAIL** | 0.95182 | **0.02332, 0.02332, 0.02332, 0.02332** |

The arm-quality values reproduce plant v4 exactly under independent arithmetic
(0.0233 = 0.55·exp(−((0−0.8)/0.45)²) = interventional@0.0; 0.9518 = partial@0.9;
0.8208 = partial@1.0; 0.9877 = partial@0.85), confirming the plant is the same function, not a
similar one.

**Why this blocks the study.** G0 fail on a cohort routes to `CANNOT_CHECK__CAMPAIGN_INVALID`
with no claim. G1 is a **conjunction** that requires P′: *"R′ raw ρ > 0 with p ≤ 0.05 **AND** P′
raw ρ > 0 (same sign)"* — and the frozen screen implements it as `g1 = g1_r and g1_sign`. With
P′'s G0 already measured failing on the current channel, the 144 native runs and 96 decision
calls the design budgets would purchase a verdict that is knowable now, for free, and is
`CANNOT_CHECK`. Spending them would not be an experiment.

**Prediction (labelled as such; not measured for the live arm).** Stage-2d arm B sat frozen at
one config — `interventional @ frac 0.0`, quality 0.02332 — for **cycles 1 through 4**, escaping
only at cycles 5–6. **H-EXT-2 chains are K = 4 cycles.** If the same mandate-induced exploration
collapse acts on P′'s *live* arm, its chains would emit a single config across their entire
horizon, making `sig_purity` constant and failing G0's own non-degeneracy clause (≥ 8/12 chains
with ≥ 3 distinct `sig_purity` values) as well. This is a prediction from a synthetic-feedback
control to a live arm and is **not** used to support the blocked disposition; BLOCK-2 rests on the
measured control alone.

**Not resolvable by this lane.** The cause is an interaction between the mandate text and the
served model (Stage-2d §3: arm B *passed* under the m3-era model at 0.9877 and *fails* on
`glm-5.3`), and the m2/m3-era served model is unrecoverable. There is no code fix.

**Explicitly not done:** the design was **not** amended to drop P′ or to re-point G1 to R′ alone.
Dropping a registered cohort *because it has been measured to fail* is outcome-directed
amendment, not a pre-outcome correction, and §11 forbids cohort re-assignment. The successor
design in §7 changes the cohort structure under a **new identity and its own freeze**.

## 4. Pre-run design findings (recorded, not applied — the freeze stands)

These were found during the pre-run audit. Because the study is blocked, none was applied: there
is no run to protect and amending a frozen design that is not going to execute would only
obscure the record. **They are corrections the successor freeze must carry.**

### D1 — `G2` is an absence test with no power floor; a dead external anchor scores PASS

This is the on-theme finding. G2 asks whether the channel-external signal shows *no* significant
anti-ranking. The frozen screen implements it as:

```python
usable = row["chains_used"] >= 8 and nonconst >= 8      # nonconst = chains with >=2 distinct values
anti   = row["raw_pooled_rho"] > 0 and row["perm_p_two_sided"] <= 0.05
verdict = "CANNOT_CHECK" if not usable else ("PASS" if not anti else "FAIL")
```

`usable` discriminates **constant from non-constant**, not **uninformative from informative**. An
external anchor that is pure noise jitters, so it is "usable"; being noise, it yields ρ ≈ 0, so
`anti` is False, so **G2 = PASS** — and PASS routes to the study's strongest terminal,
`SALIENCE_ANTI_RANKING_REPLICATED_CROSS_LEARNER`. The specificity gate is purchasable by
instrument death.

This is not hypothetical on this substrate family. Stage-2c §4 **measured** the same statistic on
the parent cell: replica edge-set Jaccard `0.0093 – 0.0520, mean 0.0282` — seed-replicas of the
same cell agree on ≈ 3 % of their edges — with pooled ρ `+0.00185` at p `0.9893`. Demonstrated
rather than argued (12 synthetic chains, `sig_purity` strongly anti-ranking, external anchor drawn
uniformly from Stage-2c's own measured `replica_J` range):

| external anchor | chains non-constant | usable | ρ | perm p | **G2** | route |
|---|---|---|---|---|---|---|
| noise on Stage-2c's measured range | 12/12 | True | +0.20000 | 0.2420 | **PASS** | `SALIENCE_ANTI_RANKING_REPLICATED_CROSS_LEARNER` |
| exactly constant | 0/12 | False | +0.00000 | 1.0000 | CANNOT_CHECK | `G2_CANNOT_CHECK` |

Only the *exactly* constant case is caught. **Successor fix:** G2 needs a positive control — the
external anchor must first be shown capable of ranking *something* (e.g. a registered
informativeness floor on replica overlap, or a known-answer recovery) before its silence is read
as evidence of mechanism specificity.

Relatedly, the §3 outcome-blind probe reads only *(a)* primary finiteness and *(b)* wall time. It
does **not** check replica overlap, even though Stage-2c's receipt explicitly warns that *"any
future attempt at a replica-consistency truth-anchor on gies/weissmann must first establish that
replicas overlap enough to carry signal."* The precondition the design most depends on is the one
its mandatory probe does not test.

### D2 — G0's non-degeneracy counter passes vacuously on the maximally degenerate case

In `g0_validity`:

```python
ge3       = sum(1 for ch in chains if sum(1 for t in ch["truth"] if math.isfinite(t)) >= 3)
distinct3 = sum(1 for ch in chains if len(set(round(v, 12) for v in ch["scores"][PRIMARY])) >= 3)
```

`ge3` filters non-finite values; `distinct3` — one line below it — does not. Distinct `NaN`
objects do not collapse in a set. Verified, with a control that must and does come out small:

| `sig_purity` over the chain's 4 cycles | distinct count | passes `>= 3` |
|---|---|---|
| `[nan, nan, nan, nan]` | **4** | **True** |
| `[nan, nan, nan, 0.5]` | **4** | **True** |
| `[0.3, 0.3, 0.3, 0.3]` (control) | 1 | False |

A chain whose primary is entirely `NaN` scores maximum non-degeneracy. The gate specifically
registered to prevent a degenerate primary is the one that cannot see the degenerate case. Nor
does the neighbouring `MAX_NAN_CYCLE_FRACTION` clause cover it — that is computed over `truth`
(the wasserstein primary), not over `sig_purity`, so a chain with finite truth and all-`NaN`
salience passes both. **Successor fix:** filter with `math.isfinite` in `distinct3`, and add a
`NaN`-primary fraction clause on the *candidate* as well as on truth.

### D3 — a registered G0 clause is executed, but not by the gate

G0 registers *"FORBIDDEN_SUBSTRINGS assert on every feedback write and read **and on every
prompt** (executed)."* What is actually wired:

| surface | asserted where | consumed by `g0_validity`? |
|---|---|---|
| feedback (write) | runner `redact_feedback()` raises `ChainCannotCheck` | indirectly — the chain fails to complete |
| feedback (read) | screen `build_cohort()`, hard `assert` per cycle | **yes** — an assert failure stops the screen |
| **prompts** | runner `audit` subcommand, over `*/*/prompt.txt`, `*/upfront/prompt.txt`, `CONTROLS/*/prompt.txt`, `CONTROLS/*/*/prompt.txt` | **no** |

`controls_from_runner()` reads exactly two keys — `planted` and `nullcal_signflip`. The `audit`
verdict is never read, so **prompt-side leakage is checked but not gate-blocking**, while
feedback-side leakage is. This is the same shape as the PRA GP2a narrowing: a clause registered
under two conditions, evaluated under one. It is a narrowing, not a hole — the assert does run —
so it is recorded as a wiring fix, not a vacuous check. **Successor fix:** have
`controls_from_runner` read the audit verdict and add it to the `d["pass"]` conjunction.

## 5. No-alarm set — what was checked and found clean (denominators published)

Reported so that §4 is not mistaken for the whole audit. Each of these is "checked and fine", a
state distinct from "could not check".

| check | method | result |
|---|---|---|
| screen ρ-permutation nullcal at **registered protected scale** | ran `nullcal(reps=400, draws=1000)`, seed 20260904 | **PASS**, rejection **0.055** ∈ [0.02, 0.09], 28.7 s, **no crash** — the ME-X6 "hard gate raises at protected size" class is clear |
| edge-parse / Jaccard selftest | ran `selftest_edges()` | **PASS**, **6/6** checks true (`J_self`, `J_disjoint`, `J_partial`, `J_empty_pair`, `parse_roundtrip`, `parse_empty`) |
| unit suite | `python3 -m pytest tests/unit/test_h_ext2_salience_runner.py tests/unit/test_h_ext2_salience_screen.py -q`, no pipe | **11/11 passed, exit 0** |
| **could the two arms ever have differed?** | read both branch sites; rendered and diffed prompts | **yes** — `CYCLE1_ANCHOR` gates the cycle-1 rule text in the prompt builder *and* the mandate re-ask in the accept branch; R′ and P′ cycle-1 prompts differ (1811 B vs 2113 B, distinct shas) and `"CYCLE-1 RULE"` appears in exactly one. **Not** an `x == x` contrast |
| **does the replica seed do anything?** | read `native_run` call site | **yes** — `rep_cfg = dict(cfg, model_seed=(int(cfg["model_seed"]) + 7919) % 2147483648)` is passed into `native_run`. The replica is not a pure function of `(dataset, rep, cycle)`; the ME-X6 "seed never reaches the window" class is clear. *(Whether `model_seed` perturbs **DCDFG-LIN**'s fit remains an unverified design assumption — see §6.)* |
| exp-id layout collision | arithmetic over the frozen formulas | clean — R′ originals `EXP_BASE+task·4+slot` = 505000–505047, replicas `EXP_BASE+100+task·4+slot` = 505100–505147, P′ 505200–505247, probe 505900–505904; no overlap with m2 (500000s), m3 (501000s), Stage-2b (503000s) |
| parent-learner guard | read `main()` | present — `MODEL == PARENT_MODEL` ("gies") forces a `fresh_learner` FAIL into `screen_controls`; the runner selftest independently fails if `PINNED["model_name"] == "gies"` |
| absent-control handling | read `controls_from_runner` | safe — a missing control file yields `"ABSENT"`, which fails the `== "PASS"` conjunction rather than passing silently |
| replica pin audit | read `build_cohort` | present — replica `arguments.json` is checked for `model_name` **and** for agreement with its original on `training_regime`, `fraction_partial_intervention`, `partial_intervention_seed` |
| freeze integrity | `shasum -a 256` vs the design's §10 declarations | **both match** — runner `a96c3a47…`, screen `984e352d…`, byte-identical to what the design froze |
| exit-code discipline | read `main()` | present — the screen returns **0** on G0 pass and **2** on G0 fail, so "could not check" is already distinct from "checked and fine" |
| register dependency re-pointing | read the custody row on `main` | unchanged — still "design freeze only until Stage-2b terminates"; no lane has re-pointed it to Stage-2c/2d |

## 6. What was deliberately not done

- **The §3 runtime probe (5 native runs, exp 505900–505904) was not run.** §9's licence precedes
  it in the design's own ordering, and the probe is the act that *consumes the registered fallback
  ladder* ("no re-pick after unblinding"). Burning a one-shot registered ladder step inside a
  design whose cohort structure must change anyway would destroy a frozen asset for no gain. The
  ladder is left `UNCONSUMED`. This also means **DCDFG-LIN's wall time and its seed-sensitivity
  remain unverified**, exactly as the design admits — those are facts the successor freeze should
  buy first, since they are cheap and outcome-blind.
- **No `PROTECTED_RUN_AUTHORIZATION.json` was requested**, no seed commitment was published, and
  no guard was disarmed. There was nothing to protect.
- **No design constant, gate, threshold, seed, direction, cohort, statistic or routing row was
  changed.** §4's findings are recorded for a successor, not applied here.

## 7. Revival path (the lever, for a successor freeze under a new identity)

The programme rule is that a blocked or negative result is intermediate. The attribution is
single-stage — **the P′ cohort's cycle-1 mandate on the current served channel** — and it has a
matching lever.

Stage-2d arm A establishes that the **mandate-free** policy has a **passing** planted control on
`glm-5.3` (0.9877, five distinct `frac` values sampled, plant optimum found at cycle 8). R′ is
therefore viable on the current channel; only P′ is not. The successor should keep **one
mandate-free cohort** and relocate G1's same-sign clause.

The obvious move — making *both* cohorts mandate-free — must be avoided: P′ would become a second
sample of R′'s policy, and G1's same-sign clause would silently degrade from "replicates across
prompt policies" to "replicates across a re-run", a weaker claim wearing the same gate's name.
The information-preserving replacement is already in the grid: **carry the same-sign clause on the
`weissmann_k562` / `weissmann_rpe1` split** (6 + 6 chains), under one mandate-free policy. Design
§7 already states the P′ clause "is a sign check by design", so 6 chains per side is adequate for
exactly the function P′ served, and the clause then tests sign stability across *substrate cells*
rather than across prompt policies — which is closer to the register row's own wording ("stable
across native learners and substrates").

That successor must also carry D1 (a positive control / informativeness floor for the G2 external
anchor, and a replica-overlap precondition in the probe), D2 (`isfinite` filter in `distinct3`
plus a candidate-side NaN clause) and D3 (gate-consume the audit verdict).

## 8. Custody

- This receipt and `results/H_EXT2_EXECUTION_BLOCKED_CHECKPOINT_V1.json`.
- Evidence cited, all already on `main` and unmodified by this lane:
  `research/experiments/e40-matched/E40_M5P_STAGE2C_OUTCOME_RECEIPT.md`,
  `research/experiments/e40-matched/E40_M5P_STAGE2D_OUTCOME_RECEIPT.md`,
  `research/experiments/e40-matched/rollup-m5p-stage2c/DISPOSITION_SUPERSEDED.md`,
  `rollup-m5p-stage2d/A_NO_MANDATE_arm.json` (`a2cedcfe…`),
  `rollup-m5p-stage2d/B_REGIME_ANCHOR_arm.json` (`9d6de7c8…`).
- LUNARC access was read-only (`sacct`, `squeue`, `ls`, `find`). No job was submitted, cancelled
  or modified; no campaign directory was created; no file was written on LUNARC.
- All determinations that drive a decision were made with `/usr/bin/git`, `/usr/bin/diff`,
  `/usr/bin/shasum` and parsing inside `/usr/bin/python3`. Every absence claim in this receipt is
  paired with a control that must match and does (the `grep` controls in §5, the prompt-inequality
  control in §3, the `[0.3]*4` control in D2, the constant-anchor row in D1).
- The frozen design, runner and screen are byte-unchanged; this lane added only this receipt and
  its JSON checkpoint.
