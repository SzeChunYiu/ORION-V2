# FM70 Gate 0 Terminal Receipt — INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD

**Lane:** `FM70_CONTEXTUAL_REGIME_SELECTOR` (owner issue #48)
**Executed:** 2026-08-30 (LUNARC, read-only over frozen artifacts)
**Design:** `FM70_CONTEXTUAL_REGIME_SELECTOR_PROSPECTIVE_DESIGN_V1.md` (PR #87, main `93d89cd`)
**Machine result:** `FM70_GATE0_RESULT_V1.json` (this directory)
**Feature freeze:** `FM70_PRE_OUTCOME_FEATURES_V1.json` (40 dev tasks, 0 extraction errors)

## Verdict

**`GATE0_FAIL_INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD` — lane terminal.**
No held-out dispatch occurs. The lane's terminal rule (selector beats every always-arm on
the held-out frontier) cannot be reached: the pre-condition it depends on — recoverable
routing signal in pre-outcome task features on the development fold — is absent.

## Result

| Quantity | Value |
|---|---|
| CV selector successes (leave-one-project-out, 8 folds) | **3/40** |
| Always-best arm (SIMPLE_DIRECT) | **6/40** |
| Per-arm always successes | SIMPLE 6, F0 5, F2 5 |
| Oracle routing ceiling (any routable arm succeeds) | 8/40 |
| One-sided label-permutation p (1000 perms, shuffle-equal-n) | **1.0** |
| Pass rule (CV ≥ always-best + 2 AND p < 0.05) | not met (deficit of 3, p = 1.0) |

The CV selector *underperforms* the best always-arm by 3 tasks: the fitted models route
worse than an unconditional prior on this fold. This is not a marginal miss; the
permutation null places the observed statistic at the extreme wrong tail (every permuted
labeling produced a CV statistic ≥ the observed one).

## Checker validation (validate-the-checker-first rule)

Embedded in the driver (`fm70_gate0_dev_cv.py`, `positive_controls()`), run in the same
execution as the verdict:

- **Control A (agreeable signal):** outcomes synthesized so ALL arms succeed iff P02
  (test-file LOC) is above its median — a strong, learnable, *routing-irrelevant* signal.
  CV selector 20/40 = best always-arm 20/40 → the machinery fabricates no routing gain
  when the labels contain none.
- **Control B (planted routing signal):** outcomes synthesized so SIMPLE succeeds iff P06
  high / F0 succeeds iff P06 low (a genuine routing structure the features CAN encode).
  CV selector 22/40 > best always-arm 20/40 → the machinery recovers real routing signal
  when it exists.

Both controls behaved exactly as expected, so the FAIL is a property of the data, not of
the pipeline.

## Scientific finding (recorded, binding)

On this benchmark class (40 BugsInPy defect-repair tasks, 8 projects, frozen t=0 features
P01–P06 as amended in V1.1), pre-outcome task-content features carry **no recoverable
routing signal** among SIMPLE_DIRECT / F0_PARENT_FEDERATION / F2_ORION_METABOLIC_FULL.
Contextual activation is therefore excluded as a revival mechanism for the E30 R11 null:

- The dev-fold oracle ceiling was already 8/40 vs 6/40 always-best (+2 max gain), and the
  realized CV selector reaches only 3/40.
- The E30 contraction stands: no arm separation, no routing revival. The remaining
  positive paths for P-C are the E60 component ablation (in flight) and the
  naturalistic-domain cells — not routing.

## Boundary inheritance (binding, from design §7 / E30 R11 receipt §5)

The registered-failing-test lane does not run full regression suites. **No
critical-failure, safety or non-inferiority endpoint claims** may be made from FM70
outcomes — including from this negative. Routing claims are success-resource claims only.

## Custody and reproducibility

- Driver `fm70_gate0_dev_cv.py` (stdlib + numpy + scikit-learn) is committed with this
  receipt; it reads only the frozen feature JSON and the E30 R11 terminal rollup
  (`E30_R11_TERMINAL_RAW_ROLLUP.json`, PR #86, main `833fe0b`, 480/480 COMPLETED).
- Seeds fixed (`np.random.default_rng(7022026)` for the permutation null; controls use a
  deterministic median split). Re-running reproduces cv=3, p=1.0, controls A 20=20,
  B 22>20.
- Implementation note (recorded before the fit): the design pre-registered a multinomial
  logistic; the executed selector is per-arm binary logistic regression + argmax — the
  routing decision needs only per-arm P(success), and with 5–6 positives per arm this is
  the better-conditioned equivalent. Faithful operationalization, not a design change.
- Leakage discipline held: E30 outcomes were used as FM70 training/development data only;
  no held-out task was ever dispatched, so no held-out outcome exists to contaminate.

## Disposition

- Lane `FM70_CONTEXTUAL_REGIME_SELECTOR` → **terminal**, vocabulary
  `INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD` (the cheap pre-declared branch).
- Backlog `V2_COMPUTATION_ONLY_SUCCESSOR_BACKLOG_V1.json` readiness updated accordingly.
- P-C manuscript: no import now (playbook §9 — flagship rewritten only after specialist
  dispositions frozen); the E-chain terminal import will fold this in as the routing
  exclusion note.

skills-applied: none (terminal receipt, no manuscript content)
