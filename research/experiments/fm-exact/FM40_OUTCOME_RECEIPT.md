# FM40 — Invariance/equivariance discovery: PROTECTED outcome

**Terminal: `PARENT_SUFFICIENT`.** Reason as routed: *F0 reproduces M's
dispositions (identity 1.0000)* — and that identity is entailed, not measured;
§1 says so at the point the number appears.

**This receipt reports a PROTECTED run.** It supersedes, as this study's
terminal, the 21-instance DEVELOPMENT analysis that stood before it. The two
legs agree on every gate and on the route (§3).

- Design (frozen): `FM40_INVARIANCE_EQUIVARIANCE_DISCOVERY_EXACT_STUDY_DESIGN_V1.json`,
  sha256 `1802ac220e8f945847c21caa1c5c541b6d5ed8d8f2f901fd5482075b302acd0a`
- Pre-run audit (written before the run): `FM40_PRE_RUN_AUDIT_V1.md`
- Authorization (archived after use, byte-identical to the file consumed):
  `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM40.json`, sha256
  `342202946d7c58e7d39eab3537882f1e80d9d0cda8f1ecdb12cddeb00af54e1b`
- Protected seed, **revealed**: `FM40-PROTECTED-30f03eaaee7b789f3b895b389ec8b08e7e094ea895b90184`
  (sha256 `7431279476019dd15235002757be9fe80f3ad739cfc7964abd7aca83eaa5b93a`,
  equal to the commitment published in the frozen design before the run)
- Results sha256 `6f867184fc3e8de8b467f3c553659a57b7428500c95652c8404073a88dfd3969`;
  custody `723a56f0131751aeae784011c0f58c841394e32d7ff8448f5638d859896ddfa2`;
  analysis json `231e741351b7b93d8c291be78624a9e24d2cdfaa602e0b7792ab4c6253ff9e91`,
  md `342bae63f21ee1c0df0bd88630d8878439214bb0c3a2a559ca18a590ed3162bb`;
  timing `433b70a527aa497fa26549c3e12d957ab783e2c51e4491c4bf4bd11ab363aa0f`;
  selftest report (G0a/G0e source) `f0b2cb3a80b36c5718e4981e878491eb32d45944d80459a8abb7dc05de294e7d`
- Instances: 126 (18 per family x 7 families), generator rejections 169
  (published per `family|reason` in the results file; the largest single
  reason is `UNSEEN_TRANSFORMATION_BREAK|shape_incompatible_with_recipe`, 53)
- Run: Mac (local), 2026-09-04, `python3.12 fm_run.py FM40 protected`,
  **executed exactly once**, exit 0, generation+dispatch 0.185 s; analysis ran
  once inside the same invocation. Interpreter CPython 3.12.13. Runner
  `fm_run.py` sha256 `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59`;
  `fm_core.py` `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d`;
  `fm40_suite.py` `1461dd3fc90191ec044488eac0d41a4bff4907de2c315e9a489ea862cd0a3b9f`
  (pre-run commit `b107493`). None was modified after the outcome existed.

## 1. Terminal

```text
FM40_STATUS            = EXECUTED_PROTECTED
ROUTE                  = PARENT_SUFFICIENT
PRIMARY_COMPARATOR     = F0_PARENT_FEDERATION
COMPARATOR_CLASS       = ALGEBRAIC_IDENTITY_TO_THE_ORACLE__NOT_AN_INDEPENDENT_MEASUREMENT
                         -- F0 composes three COMPLETE per-stratum procedures (P2, then P4,
                            then P0) under the registered precedence, so it computes the
                            oracle function BY CONSTRUCTION.  Pre-registered in the design's
                            known_definitional_results; checked pre-run by the fidelity test
                            composition_rule_reproduces_the_oracle_..._IDENTITY_NOT_MEASUREMENT.
                         -- On this protected split F0 differs from the oracle 0 times in 126;
                            on four public seeds at the same size, 0 times in 4 x 126.
                         -- CONSEQUENCE: the 126/126 identity below is an IDENTITY, not a
                            measurement.  G1b_M_ADVANTAGE cannot fire against an
                            oracle-identical comparator, so FM_RESIDUAL_CANDIDATE and
                            M_OVER_ACCEPTS were unreachable routes on this design.
WHAT_THE_LEG_MEASURES  = (a) every non-F0 arm against the oracle (36..108 differences);
                         (b) M on the 18 instances where EVERY single parent is wrong
                             (all SURFACE_ONLY_SYMMETRY): M exact on 18/18;
                         (c) M on the 36 instances the best single parent (P2) gets wrong:
                             M exact on 36/36;
                         (d) whether M falls short of the oracle anywhere: it does not (0/126).
COST_FLAG              = COST_ADVANTAGE_PARENT (M 28.9 ms vs F0 2.9 ms; reported, no route)
FIELD_STATUS_AUTHORITY = NONE
```

**Invariance/equivariance discovery is parent-owned.** On 126 protected
instances across all seven families the pre-registered federation and the
mechanic are decision-identical on every instance (0 discordant pairs; exact
two-sided p = 1.0; Wald CI [0, 0]; Holm across the seven per-family paired
tests: every adjusted p = 1.0). **Read that 126/126 as an identity, not a
measurement.** What the run establishes is that M reaches the oracle
everywhere — including on the surface-only stratum where no single parent
does — and that it adds nothing the composition does not already compute.

## 2. Gate block, with denominators

| gate | verdict | violations | n evaluated | hard | numbers |
|---|---|---|---|---|---|
| G0a_KNOWN_ANSWER | PASS | 0 | 11 | yes | 11 hand-authored fixtures reproduced by both oracle algorithms |
| G0b_ORACLE_SELF_AGREEMENT | PASS | 0 | 126 | yes | element-closure and generator-block criteria agree on every instance |
| G0c_NULL_CALIBRATION | PASS | 0 | 4 | yes | C_ALWAYS_INVARIANT 0.143, C_ALWAYS_NON_INVARIANT 0.286, random 0.190, M vs shuffled labels 0.214 (all <= 0.40) |
| G0d_DECOY_COVERAGE | PASS | 0 | 4 | yes | 18 instances in each decoy family (minimum 3) |
| G0e_PLANTED_POSITIVES | PASS | 0 | 6 | yes | all six trip-wires fired in the execution that reports the zeros |
| G0f_FAMILY_DISCRIMINATION | PASS | 0 | 2 | yes | solvable: F0 1.000 >= 0.95 over 12 non-control arms; separating: weak arms 0.714 / 0.397 / 0.262 / 0.579, all <= 0.85 |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 126 | yes | identity 1.000; 0/18 discordant in every family (effective per-family allowance **0** at n = 18); **liveness**: the same counter registers 36 / 64 / 18 / 18 disagreements for the four ablations |
| G1b_M_ADVANTAGE | NOT_FIRED | 1 | 126 | no | 0 discordant pairs; **unfirable by construction** (§4) |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | **108** | yes | M false-invariance claims 0 <= F0 0 on the 108 oracle-blocked instances; **liveness**: C_ALWAYS_INVARIANT 108, P3 52, M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE 52, P0 51, C_RANDOM 21 |
| G3_MECHANISM_BY_OMISSION | NOT_APPLICABLE | 0 | 0 | no | no claimed advantage |

`unchecked_hard_gates` is **empty**. Every hard gate was evaluated on this split.

## 3. Protected leg against development leg

| quantity | DEVELOPMENT (n = 21) | PROTECTED (n = 126) |
|---|---|---|
| M exact rate | 1.000 | 1.000 |
| F0 exact rate | 1.000 | 1.000 |
| M-vs-F0 identity | 1.0000 | 1.0000 |
| G1a / G2 (n in scope) | PASS / PASS (18) | PASS / PASS (108) |
| route, reason | PARENT_SUFFICIENT, "F0 reproduces M" | PARENT_SUFFICIENT, "F0 reproduces M" |

**The protected leg agrees with the development leg** on every gate, every
route field and every M/F0 number. What changes is the denominator and the
separation of the weaker arms, which is the measured content of the study.

## 4. Per-arm outcomes (126 instances) and per-family exact rate (18 each)

| arm | exact | rate | over-accept (false invariance) | under-accept | FULL | EQUIV | NON_INV | SURFACE | REGIME | UNSEEN_BRK | UNSEEN_EQ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **F0_PARENT_FEDERATION** | **126/126** | **1.000** | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **M_F2_INVARIANCE_DISCOVERY_FULL** | **126/126** | **1.000** | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_REGIME_RESTRICTION | 108/126 | 0.857 | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 |
| M_MINUS_SURFACE_AUDIT | 108/126 | 0.857 | 0 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_EQUIVARIANCE_TEST | 90/126 | 0.714 | 0 | 0 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| P2_EQUIVARIANCE_SOLVER | 90/126 | 0.714 | 0 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| P5_FIXED_LESSON_TABLE | 73/126 | 0.579 | 0 | 10 | 0.44 | 0.61 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| P4_REGIME_RESTRICTION | 72/126 | 0.571 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 |
| M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE | 62/126 | 0.492 | 52 | 0 | 1.00 | 0.39 | 0.22 | 0.89 | 0.94 | 0.00 | 0.00 |
| P1_ORBIT_STABILISER | 54/126 | 0.429 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| P0_SURFACE_SYMMETRY_SCAN | 50/126 | 0.397 | 51 | 4 | 0.78 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| C_ALWAYS_NON_INVARIANT | 36/126 | 0.286 | 0 | 18 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| P3_AUGMENTATION_EMPIRICAL | 33/126 | 0.262 | 52 | 0 | 1.00 | 0.00 | 0.83 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 24/126 | 0.190 | 21 | 16 | 0.11 | 0.06 | 0.22 | 0.06 | 0.22 | 0.33 | 0.33 |
| C_ALWAYS_INVARIANT | 18/126 | 0.143 | 108 | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

**G1b is unfirable, and is reported as such rather than as a measured
absence.** Its clause needs >= 5 M-only-exact instances in a family; against
a comparator that is exact on every instance, M-only-exact is impossible. The
routes gated on it (`FM_RESIDUAL_CANDIDATE`, `M_OVER_ACCEPTS`) were therefore
unreachable before any instance was generated — registered in the pre-run
audit (§A2), and the ledger class is `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE`
in the unfirable direction. The reachable content of this design is whether M
*loses* to the oracle anywhere (G1a in the parent's favour) and whether it
makes a false-invariance claim (G2); it does neither.

## 5. What is measured, and what is definitional

- **No single parent reaches the endpoint, and the strata are owned
  separately.** P2 (group-element solver) is exact on the four
  invariance/equivariance families and 0.00 on the regime and surface strata;
  P4 owns the regime stratum and cannot see a value action; P0 is exact about
  the encoding and blind to the property. Their composition is exact. The
  surface-only stratum is the one **no** single parent reaches (18 instances
  where every P-arm is wrong); M is exact on all 18, and so is F0 — by the
  precedence rule, not by a contest.
- **Where the weaker parents break, at protected size.** The empirical
  augmentation parent is the weakest arm (0.262) and its errors are
  over-acceptances (52): symmetry under the transformations you happened to
  witness is not symmetry. The surface scan over-accepts 51 times. The fixed
  lesson table under-accepts 10 times and is 0.44 on plain invariance, because
  a name-keyed table cannot see which group is acting.
- **Ablations behave as their omissions predict**, and the same omissions are
  load-bearing for F0: removing the value-action test costs exactly the two
  equivariance families; removing regime recovery exactly the regime family;
  removing the surface audit exactly the surface family. Removing closure to
  unseen transformations is not family-local — it loses both `UNSEEN_*`
  families and degrades `NON_INVARIANT` (0.22) and `EQUIVARIANT_ACTION`
  (0.39), with 52 over-acceptances, the same failure mode as P3.
- **Definitional rows, labelled.** F0's 1.000 (composition of complete
  procedures); P2's 1.00/0.00 split (it is the first oracle algorithm minus
  two strata); P0's 0.00 on `SURFACE_ONLY_SYMMETRY` and P3's 0.00 on the two
  `UNSEEN_*` families (both by the generator's acceptance rule). The
  informative numbers on those rows are the over-acceptance counts.
- **Cost is against the mechanic**: M is ~10x slower than the federation
  (sampled-then-verified value-action discovery pays exhaustive verification
  per group element). Reported; routes nothing.

## 6. Comparator fairness and the null

F0 receives the same instance object as M, no oracle access, and ordinary
engineering glue (a pre-registered, outcome-blind precedence). Its parents are
complete and unbudgeted; the only budgeted procedure in the study is M's own
registered sample schedule. No parent was isolated by information or budget,
and each of P0-P5 is also reported separately. **The federation is optimal by
construction on this decision problem**, so the largest result available was
parity, and parity is what landed. The null is: *no residual is detectable in
FM40's registered decision problem, because the pre-registered composition of
the parents already solves it exactly and the mechanic solves it exactly too.*
It is not a statement that invariance discovery is worthless; it is a
statement about this endpoint, at this size, against this comparator.

## 7. Pre-outcome corrections and audited hazards

Recorded in `FM40_PRE_RUN_AUDIT_V1.md` before the run and unchanged after it:

- **Fidelity gap closed.** F0, the named comparator, had no fidelity test.
  Five `F0_PARENT_FEDERATION` checks were added to `parent_fidelity` (the
  precedence rule on each stratum, the `KA-06` dominance fixture, and the
  oracle identity on all 11 fixtures, the last labelled in its own name as an
  identity). Selftest `parents 30/30`. No arm, gate, threshold, oracle or
  generator rule changed; the development results and custody files
  regenerate byte-identical.
- **Inherited G0 verdicts re-derived, not trusted.** The committed selftest
  report reproduced byte-identical under 3.12 before the edit (control diff
  exit 1); the development results reproduced at the frozen sha256.
- **G1b unfirable** (§4) and **G2's comparator side fixed at 0** — both named
  pre-run. **Per-family allowance 0** at n = 18 — published by the runner.
- **Seed live** (two seeds, two hashes); **gates evaluable at scale** (full
  `gates()` on a public seed at 126, no exception, G2 on 108).

Neither `fm_core.py` nor `fm_run.py` was modified.

## 8. Execution discipline

One protected run, one analysis run, as authorized. The authorization was
moved to `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM40.json` immediately after use
and the guard verified re-armed (`REFUSED: PROTECTED_RUN_AUTHORIZATION.json
absent`, exit 3). No design, gate, threshold, seed, arm, oracle rule or
generator rule was changed at any point after the outcome existed. The split
regenerates byte-for-byte from the revealed seed and the frozen code.

Authority: grants nothing — no scientific truth, no F2 superiority, no field
status, no submission readiness. `PARENT_SUFFICIENT` is a successful scientific
terminal for a registered decision problem, not a verdict on the mechanic in
general. F0 is an oracle-identical federation of faithful parents (orbit /
stabiliser and equivariance solving, regime restriction, surface symmetry
scanning), named here as what it is and not as prior work.

skills-applied: none (lane outcome receipt, no manuscript content)
