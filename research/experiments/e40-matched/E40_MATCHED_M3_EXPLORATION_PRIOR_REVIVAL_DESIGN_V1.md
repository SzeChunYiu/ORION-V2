# E40-m3 design addendum V1 — cycle-1 regime-extreme anchor (exploration-prior revival)

**Pre-registered before dispatch.** Parent: e40-m2 (verdict
`METABOLIC_DRAG_MATCHED_NATIVE`, mean_d = −0.00898, perm_p_exact = 0.999,
f0 wins 11/12, 0/108 NaN; receipt `E40_M2_GIES_REVIVAL_OUTCOME_RECEIPT.md`).
This is the operator-directed revival pass on that negative
(diagnose → attribute → apply the matching lever → re-test); it changes
**one** policy dimension and leaves every other frozen quantity untouched.

## 1. Failure attribution (from the m2 frozen chains, not re-derived here)

m2 §3 mechanism census: f0's best-of-4 lands on **regime extremes**
(interventional 5 / observational 4 / partial 3) while F2's finals land in the
**interior** (partial 0.5–0.9 in 6/12, observational-interior 1/12); extremes
beat interior on 11/12 pairs. The planted-feedback control PASSES — the loop
follows feedback when the feedback points at the target. Attribution: the drag
is **greedy sequential exploration spending cycle 1 (and often later cycles)
off the extreme family**, a *policy* property of the prompted arm, not broken
plumbing and not substrate degeneracy (gies scores every regime).

The named, untested lever: give cycle 1 the exploration prior the m2 arm
lacked — a **binding cycle-1 regime-extreme anchor**.

## 2. Single delta (everything else byte-identical in behavior to m2)

- **F2 prompt, cycle 1 only** — a binding rule appended to the TASK text:
  cycle 1 MUST choose `training_regime ∈ {"observational", "interventional"}`
  (NOT `partial_interventional`); interior fractions are reserved for cycles
  2+. Enforcement: an `ask_config_f2` wrapper re-asks with an explicit
  VIOLATION note (≤ 3 attempts); exhaustion ⇒ chain `CANNOT_CHECK`
  (never a silent fill). The mandate transcript (`asked`/`violations`) is
  frozen into `decision.json` `call_log`.
  Cycles 2–4 prompts render **byte-identical to m2** (verified:
  `cycle2_byte_identical_to_m2: True`).
- **SIMPLE and F0 are NOT re-run.** Their frozen m2 chains (and native
  results) are reused read-only as the reference via `E40M_REF` (default
  `campaign-e40-m2`). Rationale: an F2-prompt delta cannot perturb the
  no-feedback arms, and re-proposing them would inject LLM proposal variance
  into the reference — the contrast would stop being single-delta.

Not changed: substrate pins (`gies`, subset 0.05, mpl −1, do_filter), free-knob
domains, K_CYCLES=4, leakage rule (structural redaction + FORBIDDEN_SUBSTRINGS
audit), primary metric, permutation test, gate map, NaN policy (rollup
schema v2), planted/nullcal/uninformative controls, model channel.

## 3. Protocol table

| Quantity | Value |
|---|---|
| Arms executed | F2 only — 12 chains (weissmann_k562/rpe1 × 6 reps) |
| F2 native runs | 4 cycles × 12 chains = **48** (exp_ids 501000–501047) |
| SIMPLE/F0 source | frozen m2 chains (108 runs, untouched) |
| Decision calls | 12×4 F2 + planted-control replay (9) + audit/rollup |
| Contrast | `d = F0_best(m2) − F2_final(m3)` per (dataset, rep), 12 pairs |
| Test | exact sign-flip permutation, one-sided for F2 better (n=12 ⇒ 4096 flips) |

## 4. Controls

- **Planted feedback recovery** runs the SAME prompted policy, so it inherits
  the anchor: cycle 1 lands on an extreme (planted quality ≤ 0.7 — not
  penalized by the PASS rule, which scores terminal residence). Mandate
  exhaustion is a recorded `FAIL` of the control, never an eval crash.
- **Nullcal** (permutation-null calibration) and **uninformative** replay
  unchanged. **Audit** unchanged (leakage + pin over all m3 arm-visible
  artifacts).

## 5. Pre-registered decision rule (frozen gate map + m3 labels)

Let `d̄` = mean over the 12 pairs of (F0_best − F2_final), `p` = exact
one-sided permutation p for F2 better.

| Gate | Condition | Reading |
|---|---|---|
| `F2_METABOLIC_ADVANTAGE_UNDER_ANCHOR` | `p ≤ 0.05` and `d̄ > 0` | the m2 drag was an exploration-prior artifact; anchored loop beats the federation |
| `EXPLORATION_PRIOR_EXPLAINS_DRAG` | `p > 0.05` and `|d̄| < 0.005` | drag was policy, not loop-intrinsic — loop ≈ federation once cycle-1 coverage is mandated |
| `METABOLIC_DRAG_ROBUST_TO_ANCHOR` | `d̄ < 0` and `p ≥ 0.95` | terminal: the drag is not an exploration-prior artifact; the loop pays 4× compute anyway |
| (interior) | otherwise | `NO_DETECTED_ADVANTAGE` — no revision to the m2 reading |

Secondary, pre-registered mechanism readouts (descriptive, not gating):
- f2_final regime census (extreme vs interior) — did the anchor stick to
  cycle 4 or did cycles 2–4 pull the loop interior anyway?
- f2 cycle-1 mandate transcript census (`violations` distribution).
- If drag persists AND finals sit on extremes, the surviving explanation is
  **proxy-objective misalignment** (the cycle-visible external-knowledge
  diagnostics point interior while true wasserstein favors extremes) —
  that names the *next* lever class (feedback-channel design), to be opened
  only if this gate fires.

## 6. Compute + custody

48 gies runs at ~2–2.5 min each ⇒ ~10 min native per chain + 4 decision
calls; 12-task SLURM array (2 tasks/slot), then a chained eval job
(controls → audit → rollup). Runner:
`scripts/e40_matched_runner_m3.py` (sha256 in dispatch receipt). Rollup
doc carries `"variant": "e40-m3-cycle1-anchor-revival"` and
`"reference_arms_root"`. Frozen artifacts: `campaign-e40-m3/run/` (chains,
results 501000+, controls, rollup). Selftest: m2 cases + mandate re-ask
paths (interior→interior→extreme accepted; 3× interior ⇒ CANNOT_CHECK;
no binding outside cycle 1) + synthetic-root reference pairing
(simple/f0 resolve from the m2 root, f2 from the live root, absent ⇒ MISSING).
