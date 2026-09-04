# ME-X2-V2 — Lookahead + best-hypothesis reachability revival: PROTECTED outcome

**Route terminal: `PARENT_SUFFICIENT`** — no M2 advantage over B5 (discordance
without significance).
**Lever verdict: `LEVERS_RECOVER_M`** — and this is the decisive content of the
lane. It is **not** what the development split said.

**This receipt reports a PROTECTED run.** It supersedes, as this study's terminal,
the 48-instance DEVELOPMENT analysis that stood before it. On the development
split the lever verdict was `LEVERS_NULL`; on the protected split it is
`LEVERS_RECOVER_M`. §3 says exactly why, and why the development verdict could
not have been anything else.

- Design (frozen): `ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.json`,
  sha256 `9ea8c8cd890a0f2e2df1395e58a49f10708e5b0a48f13474c9044fba61a800de`
- Pre-run audit (written before the run): `ME_X2_V2_PRE_RUN_AUDIT_V2.md`
- Authorization (archived after use): `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_V2.json`
- Protected seed, **revealed**: `ME-X2-V2-PROTECTED-682fac0fd5929ccf3291b42f5fcecf7e24184384bfd612e6`
  (sha256 `f85372cf187678f7517dcf73d41d6595add7dfd4ed04b6c218e08bb1854646fe`,
  equal to the commitment published in the frozen design before the run)
- Results sha256 `3503863a7292f77978026b230604f43a16c652324293bc75cf35c722ea1781bb`;
  custody sha256 `f71aba5dac2427754852a91a4b8d38e1bfdc59e32bb867fa90f98fe527425daf`
- Instances: 1200 (50 pairs per stratum x 12 strata), 25 arms, 21 s wall
- Interpreter: CPython 3.12.13, which reproduces the frozen development results
  byte-identically (`533b38af...`)

## 1. Headline numbers

| arm | decision-correct (n = 1200) |
|---|---|
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | **0.9908** |
| `M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS` | **0.9850** |
| `M2_L1_LOOKAHEAD_ONLY` | 0.9708 |
| `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` (V1's mechanic) | **0.9658** |
| `M2_L2_BEST_HYPOTHESIS_ONLY` | 0.9142 |
| `C_RANDOM_POLICY` | 0.1850 |
| `C_NEVER_INTERVENE` | 0.1258 |

## 2. Gate block

| gate | verdict | key quantity |
|---|---|---|
| G0a KNOWN_ANSWER | PASS | fixtures + separation pair + V2 lever fixtures |
| G0b ORACLE_SELF_AGREEMENT | PASS | exhaustive agrees on all 1200; decoy and inverse-decoy coverage OK; variant invariants hold |
| G0c NULL_CALIBRATION | PASS | `C_NEVER_INTERVENE` 0/1049 identifiable; random 0.185 (<= 0.25); M2 vs partner's oracle 0.208 vs 0.985 |
| G0d V1_PROVENANCE | PASS | all 8 frozen V1 files byte-identical |
| G1a B5_REPRODUCES_M2 | FAIL | decision identity 0.6608 |
| G1b M2_ADVANTAGE | **not fired** | M2 - B5 = **-0.0058**, 11 vs 18 discordant, exact p = **0.265** |
| G1c B5_ADVANTAGE | **not fired** | the difference is not significant in either direction |
| G2 ANTI_ESCALATION | **PASS** | M2 false escalations **0**, spec damage **0**; B5 11 and 0; V1's M 0 and 0 |
| G3 MEDIATION | NOT_APPLICABLE | consulted only if G1b fires |
| G4 INTERFACE_LADDER | PASS | no rung significantly worse than its predecessor; rung-5 gap null |
| G5 LEVER_ATTRIBUTION | **PASS (all four clauses)** | see §4 |
| COST | `COST_ADVANTAGE_B5` | B5 lower regret on 247 instances, M2 on 172, sign-test p = 0.00029 |

## 3. What changed against the development leg, and why the development leg could not have shown it

| quantity | DEVELOPMENT (n = 48) | PROTECTED (n = 1200) |
|---|---|---|
| M2 | 1.000 | 0.9850 |
| V1's M | 1.000 | 0.9658 |
| B5 | 0.979 | 0.9908 |
| G1b: M2 - B5 discordant pairs | **1** (p = 1.0) | 29 (p = 0.265) |
| G5a: M2 - V1's M discordant pairs | **0** (p = 1.0) | **29** (26 M2-only, 3 V1-only, p = **1.5e-05**) |
| G5c denominator (M2-only-correct) | **0** | **26** |
| G5d comparison | 0 < 0 (false) | 3 < 26 (true) |
| instances with an L2-only-admissible action | **0** | **44** |
| instances with an L1-changed choice | 15 | 347 |
| route | PARENT_SUFFICIENT | PARENT_SUFFICIENT |
| **lever verdict** | **`LEVERS_NULL`** | **`LEVERS_RECOVER_M`** |
| cost flag | COST_PARITY | COST_ADVANTAGE_B5 |

**The development `LEVERS_NULL` was not a measurement.** M2 and V1's M produced
identical decision-correct vectors on all 48 development instances — zero
discordant pairs — so the exact test that routes the lever verdict returned
p = 1.0 by arithmetic, not by evidence. G5's clauses (c) and (d) were computed on
empty denominators. `LEVERS_NULL` is simply what the routing returns when the
contrast could not exist. The pre-run audit recorded all of this before the
protected split was generated (`ME_X2_V2_PRE_RUN_AUDIT_V2.md` §A2).

At n = 1200 the contrast exists, and it is decisive in the opposite direction:
**the levers recover 26 decisions V1's rendering lost and give back 3**, a paired
difference of **+0.0192** (95% CI [+0.0104, +0.0279], exact two-sided
p = 1.5e-05).

The route terminal did not change. It is `PARENT_SUFFICIENT` on both splits — but
for a different reason and on a real denominator: 29 discordant pairs between M2
and B5, 11 to M2 and 18 to B5, p = 0.265. Neither arm dominates the other on the
primary endpoint at this size.

## 4. The lever verdict, clause by clause

`G5_LEVER_ATTRIBUTION` passes on all four registered clauses:

- **(a) The revival beats its own parent rendering.** M2 - V1's M = +0.0192,
  26 M2-only-correct against 3 V1-only-correct, exact p = 1.5e-05.
- **(b) Neither single lever beats the conjunction.** `M2_L1_LOOKAHEAD_ONLY`
  gains +0.005 over V1's M (p = 0.070, not significant); `M2_L2_BEST_HYPOTHESIS_ONLY`
  **loses** 0.0517 (83 instances lost, 21 gained, p = 6.7e-10). Both are at or
  below the conjunction's +0.0192.
- **(c) The gain is attributed to the executed lever receipts.** Mechanism rate
  **1.00 on all 26** M2-only-correct instances: every one is an instance where
  V1 declared a false `CANNOT_IDENTIFY` **and** M2's executed receipts show an
  L2-only-admissible action or an L1-changed choice. Not 80% — 100%, on a
  denominator of 26.
- **(d) The failure was not merely moved.** 3 V1-only-correct against 26
  M2-only-correct.

**The interaction is the finding.** L2 alone is actively harmful and L1 alone is
not significant, yet the conjunction recovers a highly significant +1.9 points.
Widening the admissible set (L2) without an ordering that can tell which of the
newly admissible actions is worth taking (L1) trades good decisions for bad ones;
the ordering without the widening rarely has a better option to reach for. The
levers are not additive and neither is sufficient alone. Recorded as measured,
not as anticipated: the design's own lever expectation was that L2 would carry
the foreclosure-induced abstentions.

Lever activity denominators on the protected split, published so the attribution
is legible: 2459 executed receipts, 5 considered-not-executed; 347 instances with
an L1-changed choice; 44 with an L2-only-admissible action; 44 with permitted
foreclosure; 336 with positive expected abstention.

## 5. Escalation harm — the lane's live gate

`G2_ANTI_ESCALATION` holds M2 to **both** B5's and V1's M's harm, and V1's M is
the tighter bound at zero. M2 meets it exactly:

| arm | false escalations | specification damage |
|---|---|---|
| `M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS` | **0** | **0** |
| `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` | 0 | 0 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 11 | 0 |
| `M2_ALWAYS_ESCALATE_WHEN_STUCK` (ablation) | 847 | 101 |

The revival bought 26 decisions and paid **nothing** in escalation harm. The
counter is not dead: the ablation registers 847 on the same split.

Note the shape of the comparison this creates. B5 reaches 0.9908 while committing
11 false escalations and 0 missed; M2 reaches 0.9850 with 0 false escalations and
18 missed. On the registered primary endpoint they are statistically
indistinguishable; on escalation harm they differ in kind, and M2 is the
conservative arm.

## 6. Cost

`COST_ADVANTAGE_B5`: B5 has lower per-instance regret on 247 instances, M2 on
172, sign-test p = 0.00029. Mean regret M2 3.448, B5 3.429, V1's M 2.998; mean
cost M2 10.57, B5 10.53. Wall-clock (reported only, routes nothing): M2 808 ms,
B5 692 ms over 1200 instances.

The revival is not free: V1's M has the lowest mean regret of the three because
it abstains more, and M2 spends to convert those abstentions into decisions.

## 7. A registered prediction, partly corroborated and partly CORRECTED

The design registered a falsifiable, non-gating prediction: M2's residual
failures should shift toward missed escalation concentrated on the high-level
strata `MEASUREMENT_OR_EVALUATOR_BLIND`, `TOOL_INSTRUMENT_INADEQUATE` and
`WORKFLOW_INADEQUATE`. M2's 18 residual missed escalations fall as:

| stratum | M2 missed | n | rate | V1's M missed |
|---|---|---|---|---|
| PROBLEM_OBJECTIVE_MISSPECIFIED | **9** | 86 | 10.5% | 11 |
| MEASUREMENT_OR_EVALUATOR_BLIND | 3 | 68 | 4.4% | 5 |
| NO_ESCALATION_NEEDED | 3 | 277 | 1.1% | 12 |
| TOOL_INSTRUMENT_INADEQUATE | 1 | 65 | 1.5% | 2 |
| MODEL_FAMILY_INADEQUATE | 1 | 93 | 1.1% | 4 |
| REPRESENTATION_INSUFFICIENT | 1 | 64 | 1.6% | 2 |
| WORKFLOW_INADEQUATE | **0** | 51 | 0% | 0 |

**Partly right, partly wrong, and the wrong part is the dominant one.**
`MEASUREMENT_OR_EVALUATOR_BLIND` is indeed the second most concentrated residual,
as predicted. But `WORKFLOW_INADEQUATE` is clean and `TOOL_INSTRUMENT_INADEQUATE`
nearly so, while `PROBLEM_OBJECTIVE_MISSPECIFIED` — a stratum the prediction did
not name — carries half of M2's remaining loss at more than twice the rate of any
other. `CORRECTED`: the residual is not "high-level strata" in general; it is
objective misspecification specifically, where B5 is perfect (86/86) and both M2
and V1's M are not. That is a named, testable target for any successor and it is
recorded here rather than smoothed away.

## 8. Comparator fairness

`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` is an exact planner over the same
registered outcome tables, receiving the same instances, budgets and uniform
prior as M2. Both arms are code; neither is given a rule the other is denied, so
the procedural asymmetry recently found in ME-F1 has no analogue here. The
comparator is not isolated: its ladder is reported rung by rung (0.684, 0.816,
0.867, 0.949, 0.991) and a deliberately stronger variant `B5_NO_ABSTENTION_GATE`
(0.911) is also run. G4 confirms no rung is significantly worse than its
predecessor. The comparator won the primary endpoint numerically; the asymmetry,
if any, runs against the mechanic.

## 9. What is optimal by construction

The registered outcome tables make locus diagnosis a **finite** decision problem,
and an exact finite-horizon planner is optimal on it. B5 is that planner. The
largest result available to any myopic rendering of minimum-escalation semantics
was therefore parity, and 0.9850 against 0.9908 with p = 0.265 is parity within
this study's power. `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL` stands: what
separates the rungs is what the interface carries, not what controls the search.

The null is precise: **no residual is detectable in ME-X2's registered decision
problem, because an exact planner over the registered tables already solves it and
the mechanic's improved rendering reaches statistical parity with it without
exceeding it.** The lever verdict is the positive finding inside that null — the
registered levers do recover decisions the parent rendering lost, attributably and
without escalation harm, even though recovering them does not produce a residual
against the exact planner.

## 10. Revival status

This lane *is* the revival of ME-X2 V1 (`LEVERS_NULL` was V1's unfinished
business), and the revival succeeded on its own terms: `LEVERS_RECOVER_M`, fully
attributed, no escalation harm. The remaining gap to B5 is horizon-shaped exactly
as the design predicted — an action can be individually harmless yet leave a
warranted high-level fix unaffordable two steps later, which no one-step rule can
see and a finite-horizon planner can. The next lever is named and it is not a
third one-step rule: it is finite-horizon reasoning, which *is* B5. Per the
design's registered reading, that makes `PARENT_SUFFICIENT` the honest terminal
rather than a deferred one.

The one concrete successor target this run produces is §7's: objective
misspecification, where the exact planner is perfect and both renderings are not.

## 11. Execution discipline

One protected run, one analysis run, as authorized. The authorization was moved to
`PROTECTED_RUN_AUTHORIZATION_ARCHIVED_V2.json` immediately after use and the guard
was verified re-armed (`REFUSED: PROTECTED_RUN_AUTHORIZATION.json absent`). The
seed was hashed against the frozen commitment before generation and revealed above
after the outcome. No design, gate, threshold, seed, arm, lever, oracle rule or
generator rule was changed at any point after the outcome existed. The pre-run
audit's §A2-A9 stand unmodified.

Authority: grants nothing — no scientific truth, no field status, no novelty, no
architecture adoption, no submission readiness. `PARENT_SUFFICIENT` is a
successful scientific terminal for a registered decision problem;
`LEVERS_RECOVER_M` is a statement about two registered levers on synthetic
ORION-authored episodes, and the design's registered limitations — synthetic
episodes cannot alone support a field-level residual — are unchanged by this run.

skills-applied: none (lane outcome receipt, no manuscript content)
