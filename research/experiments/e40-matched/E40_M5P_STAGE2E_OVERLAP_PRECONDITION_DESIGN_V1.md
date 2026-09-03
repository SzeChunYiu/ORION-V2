# E40-m5′ Stage-2e — Replica-Overlap Precondition Probe, Design V1 (frozen before any run)

**Lineage:** Stage-2c outcome receipt (main `01cc8418`) — `CHECKER_INVALID__NO_VERDICT`, the E40
line stays open; Stage-2d outcome receipt (main `a67bd85`) — `PROMPT_IMPLICATED (D2)`,
mandate-induced exploration collapse, model exonerated as a sufficient cause.
**Class:** substrate precondition probe. **ZERO model calls** — every config is fixed by this
design, so there is no prompt, no mandate, no served-model channel and no channel drift.
**Cost:** 34 native `gies` runs, 0 decision calls, exp_ids **505000–505033**.
Freeze precedes run (m-series discipline).

## 1. Why this probe exists, and what it is not

Stage-2c's seed-replica stability probe rests on a premise it never tested. Its statistic is
`J_c = mean_{k<l} |E_k ∩ E_l| / |E_k ∪ E_l|` over **replicas of the same cell**, and the
hypothesis is that "cycles where independent replicas converge on the same output graph are
tracking substrate-determined structure". Stage-2c reported J = 0.0093–0.0520 (mean 0.0282) and
called the statistic degenerate.

**That reading was not established.** A config census of the 48 live Stage-2c F2 chains
(read-only, descriptive, non-gating; `campaign-e40-m5p-stage2c/run/chains`) shows the replicas
were mostly **not running the same config**:

| across the 4 replicas of a cell, at one cycle | distinct non-seed configs | cell-cycles |
|---|---|---|
| all four differ | 4 | **26 / 48** |
| three differ | 3 | 19 / 48 |
| two differ | 2 | 3 / 48 |
| all four agree | 1 | **0 / 48** |

and within a chain, 15/48 held **one** config for all four cycles (mandate collapse in the live
arm, matching Stage-2d), 25/48 held two, 8/48 held three or four. So Stage-2c's J conflated seed
variation with config variation, and **the seed-only quantity the premise is about was never
measured**. This probe measures it, with nothing else in the loop.

This is a **precondition** probe. It cannot revive the E40 line, cannot authorize m6, cannot
alter the Stage-2c or Stage-2d dispositions, and produces no claim about the metabolic-drag
hypothesis. Its sole output is whether the Stage-2c probe is testable on this substrate at all.

## 2. Frozen grid (published before any run)

- Substrate pins byte-identical to m2/m3/Stage-2c: model `gies`, datasets `weissmann_k562` /
  `weissmann_rpe1`, `subset_data=0.05`, `do_filter`, `max_path_length=-1`,
  `omission_estimation_size=1000`. No substrate modification.
- **Seed table inherited VERBATIM from the Stage-2c replica table** (§2.1 there):
  `s0`=11/13, `s1`=29/31, `s2`=47/53, `s3`=71/79 (`model_seed`/`partial_intervention_seed`).
- **Non-seed configs fixed by this design** (no model chooses them), spanning the regime axis:
  `c0` interventional @ 0.0 · `c1` partial_interventional @ 0.5 · `c2` partial_interventional @ 0.8
  · `c3` observational @ 0.0.
- Grid: 2 datasets × 4 configs × 4 seeds = **32 runs**, plus **2 determinism repeats**
  (`c0`,`s0` re-run once per dataset at its own exp_id) = **34 runs**, exp_ids 505000–505033.

### 2.1 Seed / RNG commitment (complete; nothing else is random)

| use | value |
|---|---|
| replica seed table | 11/13, 29/31, 47/53, 71/79 (inherited, unchanged) |
| P2 permutation | **exhaustive, no RNG** — every within-stratum relabelling, C(8,4)² = 4,900 |
| Jaccard/round-trip control fixtures | 20260902 (inherited from Stage-2c) |
| null-calibration control | 20260903, 400 reps |

There is no other stochastic element. All sums via `math.fsum` (interpreter-independent).

## 3. The two contrasts (both computed inside this campaign; nothing is re-pooled)

- **seed-only J**: for each (dataset, config), consensus J over its 4 seeds — 8 values.
  This is the most-favourable-possible condition for replica consensus: identical substrate
  config, only the seed pair differs.
- **config-only J**: for each (dataset, seed), consensus J over its 4 configs — 8 values.
  The reference the statistic must beat if it is measuring replication rather than config spread.

No Stage-2c, m2, m3 or m4 envelope is re-rolled, re-pooled or re-analysed into a new condition.
The Stage-2c config census in §1 is descriptive and explicitly non-gating.

## 4. Gates (frozen before computing)

Controls are evaluated **first** and **gate the verdict** (Stage-2c REPAIR R1 pattern: the checker
CONSUMES its control verdicts; absence is its own status, never a pass).

- **P0 `CONTROLS_AND_ENVELOPES_VALID` (validity):** all four registered controls PASS **and**
  every one of the 34 envelopes is COMPLETE and homogeneous (§5). Fail ⇒ `CANNOT_CHECK`,
  **exit code 5**, nothing filed.
- **P1 `SEED_REPLICATION_INFORMATIVE`:** pooled mean seed-only J ∈ **[0.20, 0.98]**.
  Both bounds are live and both void the premise:
  *below 0.20* — replicas are near-disjoint, the statistic has no resolution;
  *above 0.98* — the seed knob generates no replica independence, so "independent
  seed-replicas" do not exist here and the only thing that ever moved the graphs was the model's
  own config choices, i.e. the feedback channel the probe was meant to be independent of.
- **P2 `CONSENSUS_DISCRIMINATES`:** pooled mean seed-only J > pooled mean config-only J, by a
  one-sided **stratified exhaustive** permutation (strata = dataset), p ≤ 0.05.

## 5. Per-envelope homogeneity gate (E30-R12 lesson, applied)

Pinning an identifier does not pin an experimental condition. Every run's `arguments.json` must
equal, field by field, the config this design froze for its slot; any mismatch marks that envelope
**INHOMOGENEOUS** — excluded, counted and reported, never silently used, and it fails P0. Because
this campaign makes **zero model calls**, there is no request body, no served-model id and no
channel to drift: the request-body contract is the frozen slot table itself, asserted per envelope.

## 6. Registered routing

| outcome | route |
|---|---|
| P0 fail | `CANNOT_CHECK` (exit 5). Could-not-check, filed as such; never reported as clean |
| P0 ∧ ¬P1, J < 0.20 | **`E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT`** — the consensus statistic has no dynamic range on this substrate under ANY prompt, mandate or model; the Stage-2c probe is not testable here, and the E40 line closes on a **precondition** terminal |
| P0 ∧ ¬P1, J > 0.98 | **`E40_PROBE_PRECONDITION_UNMET__REPLICATION_DEGENERATE`** — the seed knob generates no independence; the probe's premise is void; same precondition terminal |
| P0 ∧ P1 ∧ ¬P2 | `AMBIGUOUS__PRECONDITION_MET_STATISTIC_NON_DISCRIMINATING`, reported in exactly those words |
| P0 ∧ P1 ∧ P2 | `PROBE_PRECONDITION_MET` — closure requires a mandate-free re-run of the seed-replica probe under its own freeze; **that campaign is then the single blocking artifact** |

**A precondition terminal is NOT the registered `E40_TERMINAL`.** Design §6 of Stage-2c awards
`E40_TERMINAL` only on a valid run with G0 passed and one of G1–G4 failed. No such run exists, and
this probe does not create one. The two precondition dispositions close the line on the distinct
ground that the last named lever cannot be tested on this substrate — they must never be reported
as, or merged into, the registered terminal.

## 7. Controls

| control | rule |
|---|---|
| `jaccard` | J(E,E)=1; J(E, rewired-E) < 0.05; J(E,∅)=0; J on a known 100/300 overlap = 1/3 exactly |
| `edge_roundtrip` | 417-edge fixture writes and re-parses identically; a malformed header is REJECTED (a parser that silently returns ∅ would manufacture J≈0) |
| `nullcal` | the stratified exhaustive permutation rejects at 0.02–0.09 under H0 (400 reps, seed 20260903) |
| `determinism` | the (c0,s0) repeat pair exists and parses in both datasets; its J is **recorded**, and is the known-answer showing what the pipeline returns when two runs are genuinely identical |

There is no reduced/`--fast` control variant: a mode that can return a different verdict from the
same code is the silent-failure pattern this programme exists to prevent.

## 8. Validation required before the freeze

`selftest` must reach **every** routing branch from a fixture — a `high` fixture ⇒
`PROBE_PRECONDITION_MET`, a `disjoint` fixture ⇒ `…REPLICAS_DISJOINT`, a `degenerate` fixture ⇒
`…REPLICATION_DEGENERATE`, an inhomogeneous envelope ⇒ `CANNOT_CHECK` with exit 5 — plus the
no-alarm case (clean controls and clean statistics must NOT fire), both P1 boundaries
(0.19/0.20/0.98/0.99), and a failed control voiding an otherwise perfect result. A unit test
asserts the edge/Jaccard primitives are **character-for-character** the Stage-2c definitions, so
"the same statistic as the probe it is a precondition for" is verified rather than asserted.

## 9. Non-goals / no-rescue clause

Whatever this shows: no F2 claim, no component claim, no revival of any frozen negative, no m6
authorization, no change to the Stage-2c or Stage-2d dispositions. Re-running with an altered
grid, seed table, threshold or gate after seeing the result is outcome tuning and is forbidden.
