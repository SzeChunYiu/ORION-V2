# FM50 — Functoriality and commuting diagrams: PROTECTED outcome

**Terminal: `PARENT_SUFFICIENT`.** Reason as routed: *F0 reproduces M's
dispositions (identity 1.0000)* — and on this endpoint that identity is
expected by mathematics before it is observed; §1 says so at the point the
number appears.

**This receipt reports a PROTECTED run.** It supersedes, as this study's
terminal, the 24-instance DEVELOPMENT analysis that stood before it. The two
legs agree on every gate and on the route (§3).

- Design (frozen): `FM50_FUNCTORIALITY_COMMUTING_DIAGRAMS_EXACT_STUDY_DESIGN_V1.json`,
  sha256 `3d647d0b028327df127bd7fdd45fbc9dfd38409f2148a236f543135a1015b387`
- Pre-run audit (written before the run): `FM50_PRE_RUN_AUDIT_V1.md`
- Authorization (archived after use, byte-identical to the file consumed):
  `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM50.json`, sha256
  `1ce43385a31d6c9f2f846b661f0faec36d20ef109056a81022ea04a23996a6e1`
- Protected seed, **revealed**: `FM50-PROTECTED-bf064cdf6bb612a48608b7e49e479b135c2fb7e32061131f`
  (sha256 `b45a1644e3219ce0cca4e3307dacc7c4c20e50833095fc4d1ed579fa3948fe46`,
  equal to the commitment published in the frozen design before the run)
- Results sha256 `e99bd75710a0445524f940e4a395ebd77a902ae104ee0b70e287dda5ff8e0cd0`;
  custody `46b622996b71ff1874bfbbbf2bf65c6583aec390227adcd5bd5abbf43267d4fd`;
  analysis json `4ba3d9b4bf99de67bb4bef4c9be06d271147d26056269d2e6aac8f873948a245`,
  md `f72817807bfe1f2c0a889cd155c67e7e534a9852cddce960ca8867b2035978ed`;
  timing `e4a2c1ffc3cdafc667193ec153c8dde8b8631526cb170251c8689234848c351c`;
  selftest report (G0a/G0e source) `5d0bb6e50c674735d44dcf41b0da8704185646495f1d5b2ebc51dbba9576bf45`
- Instances: 104 eligible (13 per family x 8 families). Eligibility ledger
  (published per family in `generator_rejections`, never scored against an
  arm): **22 INELIGIBLE** constructions (not a category: COMPOSITION 3,
  ENDPOINT 4, FALSE_EQUIVALENCE 6, IDENTITY 1, LICENSED_COLLAPSE 5, MIXED 3),
  **43 rejected** as not realising the intended family (FALSE_EQUIVALENCE 17,
  COMPOSITION 8, LICENSED_COLLAPSE 8, ENDPOINT 3, IDENTITY 2, MIXED 2, VALID 2,
  SURFACE 1), **0 of 208 eligibility probes missed**.
- Run: Mac (local), 2026-09-04, `python3.12 fm_run.py FM50 protected`,
  **executed exactly once**, exit 0, generation+dispatch 0.53 s; analysis ran
  once inside the same invocation. Interpreter CPython 3.12.13. Runner
  `fm_run.py` sha256 `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59`;
  `fm_core.py` `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d`;
  `fm50_suite.py` `d056e281c0101bd4ef645b6ad7dd6fe1a1f84807c8136da10d9c565b66af75f4`
  (pre-run commit `b107493`). None was modified after the outcome existed.

## 1. Terminal

```text
FM50_STATUS            = EXECUTED_PROTECTED
ROUTE                  = PARENT_SUFFICIENT
PRIMARY_COMPARATOR     = F0_PARENT_FEDERATION
COMPARATOR_CLASS       = ALGEBRAIC_IDENTITY_TO_THE_ORACLE__NOT_AN_INDEPENDENT_MEASUREMENT
                         -- F0 composes two COMPLETE predicates (P2 decides every functor
                            law; P4 is consulted only when every law holds), so it computes
                            the oracle function BY CONSTRUCTION.  Pre-registered in the
                            design's known_definitional_results; checked pre-run by the
                            fidelity test composition_rule_reproduces_the_oracle_..._IDENTITY_NOT_MEASUREMENT.
                         -- On this protected split F0 differs from the oracle 0 times in 104;
                            on four public seeds at the same size, 0 times in 4 x 104.
                         -- AND, stronger than any sibling (design mechanic_independence.
                            honest_limit): the law fragment is a TOTAL FUNCTION of the
                            registered candidate, so M and P2 agree by mathematics, not by
                            shared code.  The 104/104 identity below is an IDENTITY, not a
                            measurement.  G1b_M_ADVANTAGE cannot fire against an
                            oracle-identical comparator; FM_RESIDUAL_CANDIDATE and
                            M_OVER_ACCEPTS were unreachable routes on this design.
WHAT_THE_LEG_MEASURES  = (a) every non-F0 arm against the oracle (13..91 differences);
                         (b) M on the 13 instances the best single parent (P2, the law
                             checker) gets wrong -- the whole FALSE_EQUIVALENCE family:
                             M exact on 13/13;
                         (c) whether M's own precedence resolution and its DISCOVERED
                             diagram set (the only channels along which it could diverge)
                             fall short of the oracle anywhere: they do not (0/104);
                         (d) no instance is missed by every single parent (0/104): every
                             family is owned by some parent, which is the attribution.
COST_FLAG              = COST_ADVANTAGE_M (M 0.98 ms vs F0 3.85 ms; reported, no route)
FIELD_STATUS_AUTHORITY = NONE
```

**Functorial transfer is parent-owned.** On 104 protected eligible instances
across all eight families the federation and the mechanic are
decision-identical on every instance (0 discordant pairs; exact two-sided p =
1.0; Wald CI [0, 0]; Holm across the eight per-family paired tests: every
adjusted p = 1.0). **Read that 104/104 as an identity, not a measurement.**
What the run establishes is the separation of the other twelve arms
(0.125-0.875) and that functoriality alone cannot certify a categorical
transfer claim: the constant functor satisfies every law and destroys every
distinction the claim depends on, which is the whole `FALSE_EQUIVALENCE`
family and the only family the law parent misses.

## 2. Gate block, with denominators

| gate | verdict | violations | n evaluated | hard | numbers |
|---|---|---|---|---|---|
| G0a_KNOWN_ANSWER | PASS | 0 | 11 | yes | 11 fixtures reproduced by exhaustive enumeration and by constraint search, on disposition, profile and valid-functor count |
| G0b_ORACLE_SELF_AGREEMENT | PASS | 0 | 104 | yes | both oracle algorithms agree on every instance |
| G0c_NULL_CALIBRATION | PASS | 0 | 4 | yes | C_ALWAYS_BLOCK 0.125, C_ALWAYS_TRANSFER 0.375 (three of eight families are registered valid — arithmetic), random 0.192, M vs shuffled labels 0.269 (all <= 0.40) |
| G0d_DECOY_COVERAGE | PASS | 0 | 4 | yes | 13 instances in each decoy family (minimum 3) |
| G0e_PLANTED_POSITIVES | PASS | 0 | 6 | yes | all six trip-wires fired, including the eligibility trip-wire and the all-ceiling table |
| G0f_FAMILY_DISCRIMINATION | PASS | 0 | 2 | yes | solvable: F0 1.000 over 12 non-control arms; separating: weak arms 0.125 / 0.500 / 0.567 / 0.500, all <= 0.85 |
| G0g_ELIGIBILITY (suite-owned) | PASS | — | 126 constructions | yes | 104 admitted, 22 INELIGIBLE, 0 of 208 probes missed |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 104 | yes | identity 1.000; 0/13 discordant in every family (effective per-family allowance **0** at n = 13); **liveness**: the same counter registers 26 / 13 / 13 / 26 disagreements for the four ablations |
| G1b_M_ADVANTAGE | NOT_FIRED | 1 | 104 | no | 0 discordant pairs; **unfirable by construction** (§4) |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | **65** | yes | M accepts 0 <= F0 0 on the 65 oracle-blocked instances; **liveness**: C_ALWAYS_TRANSFER 65, P0 / P1 / P4 52, P3 43, P5 39, P2 13, three ablations 13, C_RANDOM 8 |
| G3_MECHANISM_BY_OMISSION | NOT_APPLICABLE | 0 | 0 | no | no claimed advantage |

`unchecked_hard_gates` is **empty**. Every hard gate was evaluated on this split.

## 3. Protected leg against development leg

| quantity | DEVELOPMENT (n = 24) | PROTECTED (n = 104) |
|---|---|---|
| M exact rate | 1.000 | 1.000 |
| F0 exact rate | 1.000 | 1.000 |
| M-vs-F0 identity | 1.0000 | 1.0000 |
| G1a / G2 (n in scope) | PASS / PASS (15) | PASS / PASS (65) |
| route, reason | PARENT_SUFFICIENT, "F0 reproduces M" | PARENT_SUFFICIENT, "F0 reproduces M" |
| cost flag | COST_ADVANTAGE_M | COST_ADVANTAGE_M |

**The protected leg agrees with the development leg** on every gate, every
route field and every M/F0 number. The one arm that moves materially is
`P3_DIAGRAM_CHASE`, 0.458 -> 0.567: at protected size it catches 10 of 13
endpoint violations and 10 of 13 composition failures through the registered
diagrams it happens to be handed, and still cannot see the unit laws (0.00 on
`IDENTITY_NOT_PRESERVED` and `MIXED_LAW_OBSTRUCTION`).

## 4. Per-arm outcomes (104 instances) and per-family exact rate (13 each)

| arm | exact | rate | over-accept | under-accept | VALID | DECOY | COLLAPSE | ENDPOINT | IDENTITY | COMPOSITION | MIXED | FALSE_EQ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F0_PARENT_FEDERATION** | **104/104** | **1.000** | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **M_F2_FUNCTORIAL_TRANSFER_FULL** | **104/104** | **1.000** | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| P2_CATEGORY_LAW_FUNCTOR | 91/104 | 0.875 | 13 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| M_MINUS_ENDPOINT_DISCIPLINE | 91/104 | 0.875 | 0 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_FAITHFULNESS_RECOVERY | 91/104 | 0.875 | 13 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| M_MINUS_IDENTITY_CHECK | 78/104 | 0.750 | 13 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 |
| M_MINUS_COMPOSITION_CHECK | 78/104 | 0.750 | 13 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| P3_DIAGRAM_CHASE | 59/104 | 0.567 | 43 | 0 | 1.00 | 1.00 | 1.00 | 0.77 | 0.00 | 0.77 | 0.00 | 0.00 |
| P1_GRAPH_HOMOMORPHISM | 52/104 | 0.500 | 52 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P4_FAITHFULNESS | 52/104 | 0.500 | 52 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| P5_FIXED_LESSON_INJECTION | 52/104 | 0.500 | 39 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_TRANSFER | 39/104 | 0.375 | 65 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 20/104 | 0.192 | 8 | 29 | 0.15 | 0.23 | 0.38 | 0.15 | 0.08 | 0.23 | 0.15 | 0.15 |
| P0_NAME_SIMILARITY | 13/104 | 0.125 | 52 | 26 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_BLOCK | 13/104 | 0.125 | 0 | 39 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |

**G1b is unfirable, and is reported as such rather than as a measured
absence.** Its clause needs >= 5 M-only-exact instances in a family; against
a comparator exact on every instance, none is possible. The routes gated on it
were unreachable before any instance existed (pre-run audit §A2; ledger class
`STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE`, unfirable direction). The reachable
content is whether M loses to the oracle anywhere or over-accepts; it does
neither.

## 5. What is measured, and what is definitional

- **No single parent reaches the endpoint; each family is owned by exactly
  the parent its competence predicts.** The law parent decides every law and
  misses the whole false-equivalence family (13 over-accepts); the faithfulness
  parent owns that family and misses every law (52 over-accepts); the graph
  parent cannot see composition or units (52); the diagram chaser cannot see
  the unit laws (43); name similarity fails every non-trivial family and is the
  only parent that under-accepts (26). Their composition is exact, and M is
  exact on the 13 instances the best single parent misses. No instance is
  missed by *every* parent — that is the attribution FM50 contributes.
- **Ablations behave as their omissions predict**, and each omission is
  load-bearing for F0 exactly as much as for M: removing the unit stage loses
  exactly the identity and mixed families; the triangle stage exactly the
  composition and mixed families; the graph stage exactly the endpoint family;
  native recovery exactly the false-equivalence family.
- **Definitional rows, labelled.** F0's 1.000 (composition of two complete
  predicates); P2's 1.00 on every law family and 0.00 on `FALSE_EQUIVALENCE`
  (it is a complete decision procedure for the laws and is also the
  cross-check oracle's law counter); `C_ALWAYS_TRANSFER`'s 0.375 (three of
  eight families are registered valid — the arithmetic the 0.40 ceiling was
  checked against before the generator was written).
- **Cost is for the mechanic**: M makes one pass (0.98 ms) where the
  federation issues two parent calls (3.85 ms). A wall-clock flag; routes
  nothing.

## 6. Comparator fairness and the null

F0 receives the same instance object as M, no oracle access, and a
pre-registered outcome-blind composition rule. Both of its parents are complete
decision procedures with no budget; M has no budget either. No parent was
isolated by information or budget. **The federation is optimal by construction
on this decision problem**, so parity was the largest result available, and
parity is what landed. The null is: *no residual is detectable in FM50's
registered decision problem, because the pre-registered composition of the
category-law parent and the faithfulness parent already solves it exactly and
the mechanic solves it exactly too.* It is a statement about this endpoint, at
this size, against this comparator.

## 7. Pre-outcome corrections and audited hazards

Recorded in `FM50_PRE_RUN_AUDIT_V1.md` before the run and unchanged after it:

- **Fidelity gap closed.** F0, the named comparator, had no fidelity test.
  Four `F0_PARENT_FEDERATION` checks were added to `parent_fidelity` (the law
  parent on every law violation including both precedence fixtures, the
  faithfulness parent only after every law holds, acceptance only when both
  parents accept, and the oracle identity on all 11 fixtures, labelled in its
  own name as an identity). Selftest `parents 32/32` (26 comparator tests + 6
  eligibility-gate tests, still counted separately). No arm, gate, threshold,
  oracle or generator rule changed; the development results and custody files
  regenerate byte-identical.
- **Inherited G0 verdicts re-derived, not trusted.** The committed selftest
  report reproduced byte-identical under 3.12 before the edit (control diff
  exit 1); the development results reproduced at the frozen sha256.
- **G1b unfirable** (§4) and **G2's comparator side fixed at 0** — named
  pre-run. **Per-family allowance 0** at n = 13 — published by the runner.
- **Seed live**; **gates evaluable at scale** (full `gates()` on a public seed
  at 104, no exception, G2 on 65).

Neither `fm_core.py` nor `fm_run.py` was modified.

## 8. Execution discipline

One protected run, one analysis run, as authorized. The authorization was
moved to `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM50.json` immediately after use
and the guard verified re-armed (`REFUSED: PROTECTED_RUN_AUTHORIZATION.json
absent`, exit 3). No design, gate, threshold, seed, arm, oracle rule,
generator rule or eligibility rule was changed at any point after the outcome
existed. The split regenerates byte-for-byte from the revealed seed and the
frozen code.

Authority: grants nothing — no scientific truth, no F2 superiority, no field
status, no submission readiness. `PARENT_SUFFICIENT` is a successful scientific
terminal for a registered decision problem, not a verdict on the mechanic in
general. F0 is an oracle-identical federation of faithful parents (the functor
laws and faithfulness on registered distinctions), named here as what it is
and not as prior work.

skills-applied: none (lane outcome receipt, no manuscript content)
