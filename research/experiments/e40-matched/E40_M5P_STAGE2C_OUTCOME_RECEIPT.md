# E40-m5′ Stage-2c — Seed-Replica Stability Probe: outcome receipt (V1)

**Campaign:** `campaign-e40-m5p-stage2c` (LUNARC), exp_ids 504000–504239 — 48 F2 seed-replica chains
(12 cells × `f2r0`..`f2r3` × 4 cycles = 192 native runs) + 12 in-campaign F0 federation chains
(4 upfront runs each = 48), all on one pinned SERVED model.
**Design:** `E40_M5P_STAGE2C_SEED_REPLICA_PROBE_DESIGN_V1.{md,json}` (PR #162, main `400dd745`),
md sha256 `8f578922459d8cdc8d118197f464ba6691b865b8ec71d35c57640f07a8afe78c`,
json sha256 `edb3bd2879b46e328be02ed0525794d594ae82fc7c6fd05851f185b0fc3e14bb`.
**Scripts (unchanged from main at run time, verified on the node):** runner
`092a62819c86fb659c6a59af04b23376a5978523b828b2fc57c22a4b35d54271`, analysis
`bb11b95316c383e0bb34c070a06dd756385208ef5407efb6476c1ac43ea8ea11`.
**Runs:** chain array SLURM **3564928** (60/60 COMPLETED); eval SLURM **3565922** (COMPLETED,
controls → audit → analysis selftest → analysis; the analysis ran **exactly once on the real
campaign**, the selftest before it touching only synthetic fixtures under rebound roots).
**Rollup:** `rollup-m5p-stage2c/E40_M5P_STAGE2C_ROLLUP_V1.{json,md}`, json sha256
`b9266001db3851def4d6bffd0ee3ebd2c9090400fd749a8706b110eaaf6e1a7c`, md sha256
`7458c089edcc16ca9547ddce916d048cca47d0c4520e069765ba2f57ca4aea5a`; 1,478-file sha256 manifest.
**Authorization (unblinding):** operator, in chat, 2026-09-02, verbatim *"run all the computation
tasks.. finish all the researxh asap"*; the eval submission was authorized by the session
coordinator under that standing instruction, not by a separate operator act. The instruction covers
executing a fully frozen analysis whose gates, seeds, statistics and routing were fixed before any
campaign datum existed (design shas above; campaign identity `campaign-e40-m5p-stage2c`), so no
discretion remained at run time.

## 1. Disposition: `CHECKER_INVALID__NO_VERDICT` — the E40 line is **NOT** terminated by this run

The frozen analysis computed the routing terminal `E40_TERMINAL` (G0 pass, G1/G2/G4 fail — §3).
**That verdict is not admissible, because a registered positive control failed.** Design §7 requires
"**Planted control** (m2/m3 form, plant v4): known-config planted signal **must pass**", inheriting
the m2/m3 semantics in which a failed planted or nullcal control forces
`CHECKER_INVALID__NO_VERDICT` regardless of the contrast (`e40_matched_runner_m3.py rollup()`:
`controls_ok = planted PASS and nullcal PASS`). Applying the pre-registered rule — not a post-hoc
change — the campaign yields **no science verdict**: no E40 termination, no m6 authorization, no
claim about the probe hypothesis.

| control | Stage-2c | m2 / m3 (same plant, same code, same PASS rule) |
|---|---|---|
| planted feedback recovery | **FAIL** — terminal quality **0.6412**, 0/8 cycles in the ≥0.8 basin | **PASS** — terminal quality 0.9877 (m3), 1.0 (m2) |
| permutation null calibration | PASS — rejection 0.055 ∈ [0.02, 0.09] | PASS — 0.055 |
| leakage + pin + seed-mandate audit | PASS — 765 artifacts, **0 violations** | PASS |

**Planted trajectory (9 cycles, synthetic feedback whose optimum sits at `partial_interventional`
@ frac 0.8, legible from any two probes):**

| cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| config | int@0.5 | int@0.5 | int@0.5 | int@0.5 | int@0.5 | int@0.5 | part@0.5 | part@0.5 | part@0.5 |
| planted quality | 0.353 | 0.353 | 0.353 | 0.353 | 0.353 | 0.353 | 0.641 | 0.641 | 0.641 |

**Failure mode: exploration collapse, not gradient-blindness.** Across nine cycles the arm emitted
only two distinct configs, and `fraction_partial_intervention` stayed at **0.5 in all nine** — the
plant's quality gradient lives in `frac`, so that gradient was never sampled at two points and the
feedback could not have guided it. The one axis the arm did vary, `training_regime`, moved once
(`interventional` → `partial_interventional`) and quality rose accordingly 0.353 → 0.641, i.e. it
responded to the axis it probed. In m2/m3 the identical plant reached 0.9877 by cycle 4 and stayed.
So the unmet precondition is that **the arm generates distinct probes**, not that it ignores a
visible gradient; either way a trajectory that never leaves one point in the decision space cannot
support a drag or probe reading.

**Attribution: two non-excluded candidates, not one.** The plant, the quality function, the PASS
rule and the surrounding runner code are inherited verbatim, but **two** things differ between the
passing and failing executions:

1. **Served model** (dominant candidate). The endpoint now serves `glm-5.3` for every requested id
   (Stage-2c dispatch receipt §2) and the m2/m3 served model is unrecoverable. This is the same
   substrate change that forced the Stage-2b → Stage-2c re-freeze; Stage-2c removed it from the
   *contrast* (both arms on one model) but cannot remove it from the arm's capability.
2. **Cycle-1 mandate content** (second candidate, not excluded). The planted control runs the same
   prompted policy as the live arm, so it inherits whatever cycle-1 rule that arm carries: m2 had
   **none** (`ask_config` on a plain `f2_prompt`, terminal quality 1.0), m3 had the
   **regime-extreme anchor** (0.9877), Stage-2c has the **seed mandate** with `training_regime` and
   `frac` left free (0.6412). The mandate texts differ, so a prompt-level cause is possible.

Discriminating them is cheap and belongs to Stage-2d: re-run the 9-cycle plant on `glm-5.3` three
ways — no mandate (m2 form), regime-extreme anchor (m3 form), seed mandate (Stage-2c form) — 27
model calls total, **zero native runs**. If all three fail, the cause is the model channel; if only
the seed-mandate arm fails, the cause is the prompt. Filing a single-stage attribution before that
test would be the attribution error the m-series rules exist to prevent.

## 2. Campaign integrity (everything that did hold)

| check | result |
|---|---|
| chains settled | **60/60 COMPLETE, 0 CANNOT_CHECK, 0 MISSING/IN_PROGRESS** |
| native runs | **240/240** (240 `metrics.json`, 240 `output_network.csv`) |
| served-model pin | **held on every call** — 207 logged decision calls across 204 decision files, all `glm-5.3` = frozen `SERVED_MODEL`; 0 chains failed the assertion |
| cycle-1 seed mandate | **48/48 satisfied on the first ask** (`asked: 1, violations: 0` in every F2 chain) |
| leakage audit | 765 artifacts, 0 violations |
| cells analysable | **12/12** complete, 0 CANNOT_CHECK cells |
| analysis executions | exactly one on the real campaign (the preceding selftest exercises `main()` only on synthetic fixtures under rebound roots) |

## 3. Numbers as computed (reported faithfully; **not** a verdict — see §1)

Gates from the frozen analysis: **G0 PASS**, **G1 FAIL**, **G2 FAIL**, **G3 PASS**, **G4 FAIL**;
script disposition `E40_TERMINAL`.

| rule | n | mean_d (F0_best − shipped) | perm p | F0 wins | F2 wins |
|---|---|---|---|---|---|
| TERMINAL (baseline) | 12 | **−0.009778** | 0.99976 | **11** | 1 |
| CONSENSUS-ARGMAX (the probe) | 12 | **−0.009417** | 0.99951 | 11 | 1 |
| PURITY-ARGMAX (anti-control) | 12 | −0.011239 | 0.99951 | 11 | 1 |
| ORACLE-BEST (ceiling) | 12 | −0.002253 | 0.91113 | 7 | 5 |

- **G0 PASS** — the metabolic drag reproduces in-campaign under one served model (mean_d −0.0098,
  11/12 cells), the same size as m2 (−0.0090) and m3 (−0.0074).
- **G1 FAIL** — pooled ρ(J_c, T_c) raw **+0.00185**, directed **−0.00185**, permutation p **0.9893**
  (10,000 draws, seed 20260902, 12/12 cells). Per-cell ρ spans −0.800 … +1.000 with median **0.000**:
  consensus carries no ranking signal about truth.
- **G2 FAIL** — consensus shipping does not close the drag (−0.0094 ≪ −0.001).
- **G3 PASS** — the registered anti-control also fails to close the drag (−0.0112), as expected.
- **G4 FAIL** — split-inconsistent: k562 consensus −0.01208 vs terminal −0.01128 (consensus worse),
  rpe1 consensus −0.00675 vs terminal −0.00828 (consensus better).
- Secondary 48-diff per-replica contrasts agree in sign and size (TERMINAL −0.009778, F0 39/48).
- Historical m2-F0 panel (**cross-model, non-gating**): TERMINAL −0.009619 (11/12), CONSENSUS
  −0.009258, PURITY −0.011081, ORACLE −0.002094 — materially identical to the in-campaign panel.
- Shipping-cycle census: CONSENSUS-ARGMAX lands on cycles {1:4, 2:4, 3:20, 4:20}; ORACLE-BEST on
  {1:22, 2:13, 3:10, 4:3} — the best cycle is usually the *first*, i.e. the trajectories drift away
  from their own optimum, consistent with §1's frozen-policy picture.

## 4. Mechanism observation: the probe statistic is degenerate on this substrate

Consensus **J_c ranged 0.0093 – 0.0520, mean 0.0282** across all 48 cell-cycles (edge sets of
161–432 edges). Independent seed-replicas of the same cell agree on roughly **3 %** of their edges —
they are very nearly disjoint graphs. Whatever the decision-maker's condition, a statistic with that
little shared structure cannot rank anything: this is why ρ ≈ 0 rather than negative. Any future
attempt at a replica-consistency truth-anchor on `gies`/weissmann must first establish that replicas
overlap enough to carry signal. This observation is descriptive, is not a registered gate, and does
not by itself refute the hypothesis under a valid control.

## 5. Disclosed defect in the frozen analysis (no post-hoc repair)

The Stage-2c analysis records the runner's control verdicts under `controls_runner` but its
`evaluate_gates()` does **not** consume them, so it emitted `E40_TERMINAL` while the planted control
was failing; the m2/m3 runner gated on exactly this. The script was **not** modified after seeing
the outcome — the design's §7 requirement is applied here in the receipt instead, and the fix
(control-gating inside `evaluate_gates`, plus a fixture asserting `CHECKER_INVALID__NO_VERDICT` on a
failed planted control) belongs to the next freeze. The frozen artifacts stand as produced.

## 6. Pre-registered routing applied

Design §6 routes a G0 failure to "CANNOT_CHECK disposition; diagnose campaign mechanics before any
re-dispatch (separate freeze)". A failed registered control is the same class of event — the
campaign cannot answer its question — so this run takes that row:

- **The E40 line is not terminated.** The `E40_TERMINAL` row requires G0 passed *and* a valid
  campaign; validity fails here.
- **m6 is not authorized.**
- **Next step (separate freeze, new identity):** run the three-arm plant discrimination in §1
  (27 model calls, no native runs) to separate the served-model candidate from the mandate-text
  candidate, then restore a passing planted control on the current channel — or establish that the
  probe-generation precondition cannot be met on it. Only then can a seed-replica probe (with the
  §4 overlap precondition checked first) be re-dispatched. No re-run of Stage-2c with a tweaked
  plant, threshold or PASS rule: that would be outcome tuning and is forbidden by design §9.

## 7. Custody

- Chains `campaign-e40-m5p-stage2c/run/chains/` (60 × CHAIN_COMPLETE.json, per-cycle decision.json
  with prompt sha, raw response, served model id, mandate transcript), results 504000–504239,
  controls `run/controls/`, rollup `run/rollup/`.
- Archived here: rollup json/md, `planted.json` (sha256 `a919807a…`), `nullcal.json`
  (`47594996…`), `endpoint_probe.json` (`632ea287…`), eval log `eval-3565922.out`
  (`5812992b…`) — all byte-identical to the LUNARC originals.
- Determinism: only RNGs are the frozen-seed shuffles (ρ permutation seed 20260902, 10,000 draws;
  nullcal seed 20260830); all sums via `math.fsum` (interpreter-independent).
- No design constant, gate, threshold, seed, seed-table entry, statistic or routing row was changed
  at any point after the freeze.
