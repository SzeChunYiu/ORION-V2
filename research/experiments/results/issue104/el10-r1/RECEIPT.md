# EL10-R1 Terminal Receipt — Epistemic Locality Known-Answer Suite

**Stage:** EL10 (issue #104), run r1. **Status:** TERMINAL, run valid (192/192 responses, custody verified).
**Design freeze:** `research/experiments/EPISTEMIC_LOCALITY_EL10_SUITE_FREEZE_V1.md` (PR #105, merged BEFORE
dispatch; Bugbot findings fixed and mutation-validated before any arm ran). **Executor:** codex-cli
`gpt-5.6-terra`, billy-old, concurrency 6. **Custody:** oracle sha256 `5e2fd1d4…` committed then removed
before dispatch (`ORION_GOLD_ACCESS=NONE`), restored+hash-matched after; all 192 return codes zero.

## Headline result

| metric | GLOBAL_RANKING | CURRENT_F0 | CURRENT_F2 | F2+LOCALITY |
|---|---|---|---|---|
| local_decision_correctness | 0.500 | 0.958 | 0.958 | **0.979** |
| false_universalization_rate (critical) | 0.333 | 0.000 | 0.000 | **0.000** |
| invalid_comparison_detection (critical) | 1.000 | 1.000 | 1.000 | 1.000 |
| cross_frame_transport_error (critical) | 0.286 | 0.024 | 0.024 | **0.024** |
| perspective_dependence_detection | 0.433 | 1.000 | 1.000 | 1.000 |
| method_routing_correctness | 0.567 | 0.933 | 0.933 | **0.967** |
| wall-time sum (s) | 791.3 | 755.4 | 601.2 | 687.1 |

McNemar ×12 (Holm): LOCALITY vs GLOBAL significant on 3 contrasts (decision correctness
p=2.4e-05; false universalization p=0.0013; transport error p=0.0098). **No contrast vs CURRENT_F0 or
CURRENT_F2 reaches significance** — the locality interface's +1 task (47/48 vs 46/48) is within noise.

## Verdict (frozen kill rule, applied honestly)

`LOCALITY_STRICTLY_WORSE_ON_A_CRITICAL_METRIC__NULL_TERMINAL` (third branch: others match on every
critical metric AND locality cost 1.14x the cheapest arm — above the frozen 1.10 kill-cost gate, so
not formally KILLED; no protected residual, so not protected either). Substantive reading per protocol:

1. **Context-free universalization is falsified hard** (GLOBAL_RANKING fails across ALL classes,
   including the ELC1 invariance control — it cannot even use a pooled ranking to pick a seeded
   winner). The suite discriminates; the null below is not vacuous.
2. **Strongest parents + current ProblemFrame are sufficient** on every critical metric:
   false universalization 0.000, invalid-comparison 6/6, transport error 1/42 each.
   `PARENT_SUFFICIENCY = VALID_TERMINAL`.
3. **The explicit PerspectiveFrame interface adds no protected incremental value at r1** — it buys
   one extra correct routing task (ELC5-03) for 14% more wrapper cost, and still shares the one
   suite-wide transport miss (`el10-elc2-01`, all four arms). It contracts to a
   **documentation/analysis convention**, not a required runtime component.
4. **EL30 stays closed**: its gate (protected residual not parent-owned) did not open.
5. Residual diagnostic (lead, not verdict): all conditioned-arm errors concentrate on the
   `system_boundary` coordinate (ELC5) — the boundary dimension is the hardest to bind; noted for
   EL20's anti-analogy work on system boundaries, no new stage opened on this basis.

## Authority

```text
grants_scientific_truth = false        grants_primary_endpoint_change = false
grants_universal_intelligence_definition = false   grants_evolution_eq_cognition = false
parent_sufficiency_is_valid_terminal = true        claim_limit = interface discriminator only
```

No paper endpoint changes; no K7; FLAGSHIP may still state the locality principle as
field-boundary/falsification (donor-motivated, EL10-null on runtime-interface necessity).
