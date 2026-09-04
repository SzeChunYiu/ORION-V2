# FM60 — Obstruction and counterexample discovery: PROTECTED outcome

**Terminal: `PARENT_SUFFICIENT`.** Reason as routed: *no significant M
advantage over the strongest faithful parent.*

**This receipt reports a PROTECTED run.** It supersedes, as this study's
terminal, the 15-instance DEVELOPMENT analysis that stood before it. **The two
legs do not say the same thing**, and §3 records the difference plainly: the
development leg reported the federation reproducing the mechanic at identity
1.0000; the protected leg reports the mechanic falling one instance short of
the federation, which fails `G1a` and lands the same terminal by its other
branch.

- Design (frozen): `FM60_OBSTRUCTION_COUNTEREXAMPLE_EXACT_STUDY_DESIGN_V1.json`,
  sha256 `f8fe7f09463938c25df3b8ddba0ead71a06616de5affddc1622b744fde463a69`
- Pre-run audit (written before the run): `FM60_PRE_RUN_AUDIT_V1.md`
- Authorization (archived after use, byte-identical to the file consumed):
  `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM60.json`, sha256
  `e0c732f9f6ea997b1b076e9a79fb2903e99f1c768b979b5b5c9b9d9e1d662852`
- Protected seed, **revealed**: `FM60-PROTECTED-6a2d4a4f73c810b9c93e4fe2f9351173b7cced5d0cf9a020`
  (sha256 `54a74a5960b88ed7973b690890a3fcb21bf80580d2a459075aae799aacbe02f2`,
  equal to the commitment published in the frozen design before the run)
- Results sha256 `20041fd5ed96b4286ca2382ff7acac837af27950cb64d0bf468033cc64713ffd`;
  custody `4095a452b06f1e32b98ab9f2e11838628e46b4a183fbeb81cbf0d2db6b440505`;
  analysis json `aed96a0d343f41e5cad431940fde6cd88a6f66e18ef8dd63f77c1f8e2472e023`,
  md `99196847f292fb850e5a32c927f2cf1ff1759d343cd6ae58ab23444dca2b1ab9`;
  timing `b3500a6185e709f0d58bf43cad52170825cd55030ac3b7705f5c6e3e181e7505`;
  selftest report (G0a/G0e source) `adae22fd5b5856b4e790b792cd51c5dc37ab7517e1620bf094be56d9055b300e`
- Instances: 125 (25 per family x 5 families), generator rejections 2,688
  (misleading_surface_support 1,965, minimal_counterexample 362,
  single_hidden_obstruction 191, multiple_obstruction 109, no_obstruction 61 —
  published per family; a random conjecture rarely has both a confirming ratio
  >= 0.88 and at most 6 countermodels in the whole space)
- Run: Mac (local), 2026-09-04, `python3.12 fm_run.py FM60 protected`,
  **executed exactly once**, exit 0, generation+dispatch+cross-check 0.581 s;
  analysis ran once inside the same invocation. Interpreter CPython 3.12.13.
  Runner `fm_run.py` sha256 `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59`;
  `fm_core.py` `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d`;
  `fm60_suite.py` `f008258f0db82af5a855396858f37d8a4180c334affa8f104ea7ef5300d9f55c`
  (pre-run commit `b107493`). None was modified after the outcome existed.

## 1. Terminal

```text
FM60_STATUS            = EXECUTED_PROTECTED
ROUTE                  = PARENT_SUFFICIENT  (by the "no significant M advantage" branch;
                         G1a_PARENT_REPRODUCES_M FAILS at identity 0.992)
PRIMARY_COMPARATOR     = F0_PARENT_FEDERATION
COMPARATOR_CLASS       = ALGEBRAIC_IDENTITY_TO_THE_ORACLE_ON_THE_GENERATOR_POPULATION__NOT_AN_INDEPENDENT_MEASUREMENT
                         -- F0 = the saturating derivation parent (P3) on the acceptance side,
                            the exhaustive model parent (P2) on the reject side.  Every reject
                            family is decided exactly by exhaustive search, and no_obstruction
                            conclusions are drawn from the rule base's closure, which P3
                            saturates: on the generator's population F0 computes the oracle
                            BY CONSTRUCTION (design known_definitional_results; fidelity test
                            composition_rule_reproduces_the_oracle_..._IDENTITY_NOT_MEASUREMENT).
                         -- On this protected split F0 differs from the oracle 0 times in 125;
                            on four public seeds at the same size, 0 times in 4 x 125.
                         -- Off the population it is NOT an identity: a bounded-valid claim
                            not derivable in the registered rule base makes F0 abstain where
                            the oracle accepts (fidelity test abstains_when_neither_parent_
                            can_discharge_the_claim).  No such instance is in this split.
                         -- CONSEQUENCE: F0's 125/125 is an IDENTITY.  G1b cannot fire against
                            it; FM_RESIDUAL_CANDIDATE and M_OVER_ACCEPTS were unreachable.
WHAT_THE_LEG_MEASURES  = (a) every non-F0 arm against the oracle (1..105 differences);
                         (b) M against the oracle: 124/125 -- ONE instance short, a
                             no_obstruction conjecture M abstains on (UNDECIDED_BUDGET_EXHAUSTED)
                             where P3 derives the proof;
                         (c) M on the 25 instances the best single parent (P2) gets wrong
                             (all no_obstruction): M exact on 24/25;
                         (d) no instance is missed by every single parent (0/125).
G2_NOTE                = PASS on 100 oracle-blocked instances, M 0 <= F0 0, but for every
                         witness-validated arm this is ENTAILED by rule-base soundness plus the
                         witness gate, not measured restraint; liveness is carried only by the
                         registered-exempt controls (C_ALWAYS_ACCEPT 100, C_RANDOM 12).
COST_FLAG              = COST_ADVANTAGE_PARENT (M 24.6 ms vs F0 4.0 ms; reported, no route)
FIELD_STATUS_AUTHORITY = NONE
```

**Obstruction discovery for bounded conjectures is parent-owned, and the
mechanic falls short of the parent by one instance.** Paired difference
M - F0 = **-0.008** (0 M-only-exact, 1 F0-only-exact), exact two-sided p =
1.0, Wald 95% CI [-0.024, +0.008]; Holm across the five per-family paired
tests: every adjusted p = 1.0. The shortfall is not statistically significant
at this size and it is in the parent's favour, so `PARENT_SUFFICIENT` lands by
the `else` branch. Read F0's 125/125 as an identity; read M's 124/125 as a
measurement.

## 2. Gate block, with denominators

| gate | verdict | violations | n evaluated | hard | numbers |
|---|---|---|---|---|---|
| G0a_KNOWN_ANSWER | PASS | 0 | 12 | yes | 12 fixtures reproduced by the exhaustive oracle and by the stratified DPLL cross-check |
| G0b_ORACLE_SELF_AGREEMENT | PASS | 0 | 125 | yes | agreement on disposition, failing conjuncts, minimal size and shallowest hypothesis model size, every instance |
| G0c_NULL_CALIBRATION | PASS | 0 | 4 | yes | C_ALWAYS_ACCEPT 0.200, C_ALWAYS_BLOCK 0.200, random 0.160, M vs shuffled labels 0.304 (all <= 0.40) |
| G0d_DECOY_COVERAGE | PASS | 0 | 3 | yes | 25 instances in each decoy family (minimum 3) |
| G0e_PLANTED_POSITIVES | PASS | 0 | 7 | yes | all seven trip-wires fired, including the 0.267 floor table and the witness-gate rewrite |
| G0f_FAMILY_DISCRIMINATION | PASS | 0 | 2 | yes | solvable: F0 1.000 over 11 non-control arms (not the R2 floor); separating: weak arms 0.192 / 0.192 / 0.200 / 0.728, all <= 0.85 |
| G1a_PARENT_REPRODUCES_M | **FAIL** | 1 | 125 | yes | identity **0.992** (1 discordant, `no_obstruction`); per-family clause satisfied (1 <= effective allowance 1 at n = 25) but the global 99.5% clause permits **0** discordances at n = 125 (`int(0.005 x 125)`); **liveness**: 101 / 29 / 26 / 25 ablation disagreements |
| G1b_M_ADVANTAGE | NOT_FIRED | 1 | 125 | no | diff -0.008, 0 M-only-exact; **unfirable by construction** (§1) |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | **100** | yes | registered clause, bound pre-run (§7): M accepts 0 <= F0 0 of the 100 oracle-blocked conjectures; **liveness** C_ALWAYS_ACCEPT 100, C_RANDOM 12; every validated arm 0, entailed by soundness (§1) |
| G3_MECHANISM_BY_OMISSION | NOT_APPLICABLE | 0 | 0 | no | no claimed advantage |

`unchecked_hard_gates` is **empty**. Every hard gate was evaluated on this
split — including the one the development split could not.

## 3. What changed against the development leg — reported plainly

| quantity | DEVELOPMENT (n = 15) | PROTECTED (n = 125) |
|---|---|---|
| M exact rate | 1.000 | **0.992** |
| F0 exact rate | 1.000 | 1.000 |
| M-vs-F0 identity | 1.0000 | **0.9920** |
| G1a | PASS | **FAIL** |
| G2 | CANNOT_CHECK (9 evaluated, generic binding); PASS (12, registered binding, re-derived pre-run) | **PASS (100 evaluated)** |
| route | PARENT_SUFFICIENT | PARENT_SUFFICIENT |
| routed reason | "F0 reproduces M's dispositions (identity 1.0000)" | "no significant M advantage over the strongest faithful parent" |

**The terminal is the same; the sentence under it is not.** The development
claim was that the federation *reproduces* the mechanic exactly. At n = 125 it
does not: the mechanic abstains on one `no_obstruction` conjecture
(`no_obstruction-00036`, claimed `UNDECIDED_BUDGET_EXHAUSTED`, an honest
abstention with no witness) where the derivation parent finds the proof. Both
wordings were registered in `FM60_PRE_RUN_AUDIT_V1.md` §A7 before the run, and
the audit's public-seed probes at this size (M-vs-F0 discordant 2 / 4 / 1 / 0,
all but one the same abstention signature) predicted this branch. Nothing here
is a surprise to the frozen design, which anticipates it in its own text: *"If
G1a fails because M is WORSE than the federation, the route is still
PARENT_SUFFICIENT and that is recorded explicitly rather than presented as a
study defect."* The discordance is real and it is not re-sliced away: at n =
125 one instance is 0.8%, above the 0.5% the registered global clause allows,
so the gate fails as registered.

## 4. Single-stage attribution of the loss, and the revival honestly stated

The one failing stage is nameable and was named before the run: **M's bounded
proof attempt**, `PROOF_STEP_BUDGET = 12` rule applications of forward chaining
in its own rule order, against the parent's saturating derivation search. On
the instance in question the conclusion is derivable (P3 derives it, and the
derivation passes the independent validator) but not within 12 applications
in M's order, so M abstains. This is M's own registered mechanic constant
(design `mechanic_independence`), not a handicap on the comparator, which is
complete and unbudgeted. The same stage produced 6 of the 7 public-seed
discordances at this size.

**Revival, honestly stated.** The lever that repairs the loss is a saturating
proof search. That computation *is* `P3_DERIVATION_PROOF_SEARCH`, one of the
two parents the federation composes. Applying the lever therefore means
adopting the parent, which is the definition of parent sufficiency, not a
residual. There is no mechanic-side change that closes the gap on this endpoint
without importing the parent's own procedure; the negative is not left
unrevived — the revival was identified and it terminates in the parent.

## 5. Per-arm outcomes (125 instances) and per-family exact rate (25 each)

Because the registered `G2` clause is bound explicitly (§7), the `over-accept`
column counts *conjectures accepted where the oracle blocks* and the
`under-accept` column is not computed on this suite (the runner's hook path
reports it as 0); read the per-family columns for the reject-side content.

| arm | exact | rate | over-accept | no_obs | single | multi | minimal | misleading |
|---|---|---|---|---|---|---|---|---|
| **F0_PARENT_FEDERATION** | **125/125** | **1.000** | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **M_F2_OBSTRUCTION_DISCOVERY_FULL** | **124/125** | **0.992** | 0 | **0.96** | 1.00 | 1.00 | 1.00 | 1.00 |
| P2_EXHAUSTIVE_MODEL_SEARCH | 100/125 | 0.800 | 0 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_PROOF_WITNESS | 100/125 | 0.800 | 0 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_MULTIPLICITY_CHECK | 99/125 | 0.792 | 0 | 0.96 | 1.00 | 0.00 | 1.00 | 1.00 |
| M_MINUS_MINIMALITY_ESCALATION | 96/125 | 0.768 | 0 | 0.96 | 1.00 | 1.00 | 0.00 | 0.88 |
| P4_SMALL_SCOPE_BOUNDED_CHECK | 91/125 | 0.728 | 0 | 0.00 | 1.00 | 0.92 | 0.84 | 0.88 |
| C_ALWAYS_ACCEPT | 25/125 | 0.200 | **100** | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_BLOCK | 25/125 | 0.200 | 0 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| P1_FIXED_LESSON_TABLE | 25/125 | 0.200 | 0 | 0.00 | 0.40 | 0.28 | 0.00 | 0.32 |
| P3_DERIVATION_PROOF_SEARCH | 25/125 | 0.200 | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P0_INDUCTIVE_CONFIRMATION | 24/125 | 0.192 | 0 | 0.00 | 0.96 | 0.00 | 0.00 | 0.00 |
| M_MINUS_OBSTRUCTION_SEARCH | 24/125 | 0.192 | 0 | 0.96 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 20/125 | 0.160 | 12 | 0.20 | 0.20 | 0.04 | 0.20 | 0.16 |

**What P0 actually claimed before witness validation** (the decoy family's
measured content, recorded because a 0.00 is not one phenomenon): on
`misleading_surface_support` it claimed `TRANSFER_VALID` on **25/25** — fooled
by confirming evidence on every instance — and every claim was rewritten for
lack of a witness; on `no_obstruction` 25/25 claims without a witness; on
`single_hidden_obstruction` 24 correct with a valid countermodel and 1 fooled;
on `multiple_obstruction` and `minimal_counterexample` 25/25 valid witnesses
with the wrong class. `P4` at 0.728 is exhaustive inside its scope and misses
4 minimal and 3 misleading instances whose obstruction first appears above it,
plus 2 multiplicity cases; its 0.00 on `no_obstruction` is 24 acceptances
without a derivation and 1 abstention.

## 6. Comparator fairness and the null

F0 receives the same instance object as M, no oracle access, and a
pre-registered outcome-blind rule (P3 first, because only a derivation
discharges the witness gate; P2 only if P3 fails; abstain if neither
decides). Its parents are complete and unbudgeted; the only budgets in the
study are M's own registered constants. No parent was isolated by information
or budget; if anything the asymmetry runs against the mechanic, which is the
direction that cannot inflate a residual claim. **The federation is optimal by
construction on this decision problem**, so the largest result available was
parity, and the finding is that the mechanic does not quite reach it. The null
is: *no residual is detectable in FM60's registered decision problem, because
the parents already solve it exactly and the mechanic solves it one instance
less well.* It is a statement about this endpoint, at this size, against this
comparator.

## 7. Pre-outcome corrections and audited hazards

Recorded in `FM60_PRE_RUN_AUDIT_V1.md` before the run and unchanged after it:

- **`G2` was evaluating a narrower clause than the one registered
  (`REGISTERED_SCOPE_DIVERGENCE`), repaired pre-run.** The design registers
  "on instances the oracle blocks, M accepts no more conjectures than F0"; the
  runner's generic fallback dropped every `MULTIPLE_INDEPENDENT_OBSTRUCTIONS`
  instance from scope and counted abstentions, witness failures and
  multiplicity verdicts as acceptances — the false liveness PR #238 found and
  deferred. Bound explicitly in `fm60_suite.SPEC` (`unsafe_scope`,
  `unsafe_claim`); the design JSON is unchanged. On the public seed at this
  size the scope went 75 -> 100 and `C_ALWAYS_BLOCK`'s spurious 75 went to 0;
  on the 15-instance development split the gate went from `CANNOT_CHECK` (9) to
  `PASS` (12), and the development analysis was re-derived under the binding.
  A `CANNOT_CHECK` hard gate was never carried downstream as passed.
- **What G2 can measure here, stated before the run.** With all 50 rules
  verified valid and every non-control witness validated, an unsafe claim by a
  validated arm is impossible; the gate's pass for M is entailed, its liveness
  is the exempt controls'. Named as `STRUCTURALLY_DETERMINED` (unfailable
  direction) rather than read as restraint.
- **Both G1a branches registered in advance**, with the public-seed evidence
  that predicted the failing one (§3, §4).
- **Fidelity: F0 already tested; the identity now checked and labelled**
  (one added test, `parents 33/33`), with the off-population non-identity
  stated in the source.
- **Inherited G0 verdicts re-derived, not trusted.** The committed selftest
  report and development results reproduced byte-identical under 3.12 before
  any edit (control diff exit 1).
- **Seed live**; **gates evaluable at scale** (three public seeds at 125, no
  exception, `unchecked_hard_gates` empty on each).

Neither `fm_core.py` nor `fm_run.py` was modified.

## 8. Execution discipline

One protected run, one analysis run, as authorized. The authorization was
moved to `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM60.json` immediately after use
and the guard verified re-armed (`REFUSED: PROTECTED_RUN_AUTHORIZATION.json
absent`, exit 3). No design, gate, threshold, seed, arm, oracle rule,
generator rule or budget constant was changed at any point after the outcome
existed. The split regenerates byte-for-byte from the revealed seed and the
frozen code.

Authority: grants nothing — no scientific truth, no F2 superiority, no field
status, no submission readiness. `PARENT_SUFFICIENT` is a successful scientific
terminal for a registered decision problem, not a verdict on the mechanic in
general. F0 is an oracle-identical (on this population) federation of faithful
parents — a Prover9-style saturating derivation search and a Mace4-style
exhaustive finite-model search — named here as what it is and not as prior
work.

skills-applied: none (lane outcome receipt, no manuscript content)
