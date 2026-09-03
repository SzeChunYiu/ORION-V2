# FM30 — Formal concept closure and revision: PROTECTED outcome

**Terminal: `PARENT_SUFFICIENT`.** Reason as routed: *no significant M advantage
over the strongest faithful parent.*

**This receipt reports a PROTECTED run.** It supersedes, as this study's terminal,
the 15-instance DEVELOPMENT analysis that stood before it. The two do not say the
same thing, and §3 records the difference plainly.

- Design (frozen): `FM30_FORMAL_CONCEPT_REVISION_EXACT_STUDY_DESIGN_V1.json`,
  sha256 `d3e1fbf0d09b45e4d266ed55545f1cc07c90f10aaf0e97e36484f8898bf26a3c`
- Pre-run audit (written before the run): `FM30_PRE_RUN_AUDIT_V1.md`
- Authorization (archived after use): `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM30.json`
- Protected seed, **revealed**: `FM30-PROTECTED-7a69e127cbe954997652762ec36c7bde05764929fbc95e15`
  (sha256 `af34cfe913bff1ef0f661b1ee4b46ff68360fa3a6bea2d06b776ca2b35857e4a`,
  equal to the commitment published in the frozen design before the run)
- Results sha256 `15f4895d7309b3ea8ed529a599b53e0e7712b9aab042444d2b0a159fc6d98fb0`;
  custody sha256 `359e594211054635bfaf592c8a9cb12a61722da8be7186ff70ebbed9d8009810`;
  selftest report sha256 `2d501ef3e31096ddc8c1aa8715d1f99aaf4c60c772bf1edda66ab65ef4e22dd0`
- Instances: 100 (20 per family x 5 families), generator rejections 313
- Interpreter: CPython 3.12.13. Runner `fm_run.py` sha256
  `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59`;
  `fm_core.py` sha256 `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d`;
  `fm30_suite.py` sha256 `3259b79262595f27a71d664f7ff8ecc2014c022c987a5a1a5a5dacb6a5ef4011`.
  None of these was modified for this run.

## 1. Why a protected run was needed at all

FM30's only terminal was a **development** terminal, and it carried an
unevaluated hard gate. `FM30_DEVELOPMENT_ANALYSIS_V1.md` routed
`PARENT_SUFFICIENT` on 15 instances with
`G2_ANTI_PERMISSIVENESS = CANNOT_CHECK`, evaluated on **1** instance against a
registered minimum of 10. The analysis correctly refused to report that gate as
passing, but "could not check" is not "checked and fine", and a development
split is not protected evidence. Both defects are closed by this run.

## 2. Gate block, with denominators

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | PASS | 0 | 9 | yes |
| G0b_ORACLE_SELF_AGREEMENT | PASS | 0 | 100 | yes |
| G0c_NULL_CALIBRATION | PASS | 0 | 4 | yes |
| G0d_DECOY_COVERAGE | PASS | 0 | 4 | yes |
| G0e_PLANTED_POSITIVES | PASS | 0 | 6 | yes |
| G0f_FAMILY_DISCRIMINATION | PASS | 0 | 2 | yes |
| G1a_PARENT_REPRODUCES_M | **FAIL** | 1 | 100 | yes |
| G1b_M_ADVANTAGE | NOT_FIRED | 1 | 100 | no |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | **36** | yes |
| G3_MECHANISM_BY_OMISSION | NOT_APPLICABLE | 0 | 0 | no |

`unchecked_hard_gates` is **empty**. Every hard gate was evaluated on this split.

**G2 is now a real verdict, not an absence.** Scope was 36 instances on which the
oracle says old-valid-case retention genuinely fails — above the registered
minimum of 10, and consistent with the 26-29 the pre-run audit measured on public
seeds at this size. On those 36 instances M claimed retention 0 times and the
federation claimed it 0 times. The zero is not a counter that never ran: on the
same 36 instances `M_MINUS_OLD_CASE_RETENTION` registered 36 unsafe claims,
`C_ALWAYS_NO_CHANGE` 36, `C_ALWAYS_SPECIALIZE` 36 and `C_RANDOM_TRANSITION` 23.
The counter is demonstrably live and both M and the parent are clean on it.

Null calibration on the protected split: random 0.070, constant arms 0.120 and
0.200, shuffled-label null 0.120 — all far below the 0.40 ceiling.

## 3. What changed against the development leg — reported plainly

| quantity | DEVELOPMENT (n=15) | PROTECTED (n=100) |
|---|---|---|
| M exact rate | 1.000 | **0.920** |
| F0 exact rate | 1.000 | 1.000 |
| M-vs-F0 endpoint identity | 1.0000 | **0.9200** |
| G1a | PASS | **FAIL** |
| G2 | CANNOT_CHECK (1 evaluated) | **PASS** (36 evaluated) |
| route | PARENT_SUFFICIENT | PARENT_SUFFICIENT |
| routed reason | "F0 reproduces M's dispositions (identity 1.0000)" | "no significant M advantage over the strongest faithful parent" |

**The terminal is the same; the sentence under it is not.** The development claim
was that the federation *reproduces* the mechanic exactly. That claim does not
survive the protected split: at n=100 the mechanic and the federation disagree on
8 instances, and every one of the 8 is a **parent-only-exact** instance. Paired
difference M - F0 = **-0.080**, exact two-sided p = **0.0078**, 95% CI
[-0.133, -0.027]. The mechanic is significantly *worse* than the strongest
faithful parent on this endpoint.

Both wordings were registered before the run, in `FM30_PRE_RUN_AUDIT_V1.md` §A7,
precisely so that whichever landed could not read as post-hoc narration. The
design anticipates this branch in its own text: *"If G1a fails because M is WORSE
than the federation, the route is still PARENT_SUFFICIENT and that is recorded
explicitly rather than presented as a study defect."*

Nothing here is a surprise to the frozen design either: its pre-registered
expectation was *"PARENT_SUFFICIENT, with M expected to fall slightly short of
the federation on the development probe's evidence"*, and its 100-instance public
development probe had already recorded M at 0.980 diverging on bridge instances.
The protected split confirms the direction and sharpens the magnitude.

## 4. Single-stage attribution of the 8 losses

All 8 discordant instances have the same signature: **M declares `SPLIT` where
the oracle declares something else.**

| family | n | M said | oracle said |
|---|---|---|---|
| BRIDGE | 5 | SPLIT | BRIDGE |
| MERGE | 2 | SPLIT | MERGE |
| NO_CHANGE | 1 | SPLIT | NO_CHANGE |

Zero instances are M-only-exact, in any family. Per-family exact rate for M:
NO_CHANGE 0.95, SPECIALIZE 1.00, SPLIT 1.00, MERGE 0.90, BRIDGE 0.75.

The failing stage is **one** and it is nameable: M's split test. M never
enumerates the concept lattice; it closes one seed per attribute outward from the
tracked concept and compares sub-concept counts, which yields a **lower bound**
on the number of sub-concepts. A lower bound that reaches two fires the split
predicate, and because `SPLIT` is first in the registered precedence, a false
split masks the true class in every family below it. That is exactly the
divergence mode the frozen design named in `mechanic_independence` before any
protected instance existed, and the protected split shows it costing 8 of 100.

**Revival, honestly stated.** The lever that would repair the split test is to
count maximal proper sub-extents of the tracked extent rather than seeded closure
lower bounds. That computation *is* `P2_LATTICE_ORDER_GEOMETRY`, one of the
parents the federation already composes. Applying the lever therefore means
adopting the parent, which is the definition of parent sufficiency, not a
residual. There is no mechanic-side change that improves M on this endpoint
without importing the parent's own procedure, so the negative is not left
unrevived: the revival was identified and it terminates in the parent.

## 5. What is optimal by construction, and what this null means

The endpoint is decided exactly by the Ganter-Wille derivation operators plus
extent geometry plus implication counterexamples. The federation composes those
three under a pre-registered, outcome-blind rule and is exact on 100/100. **The
federation is optimal by construction on this decision problem**, so the largest
result available here was always parity, and the finding is that ORION's L3
conceptual development does not reach it.

The null is therefore: *no residual is detectable in FM30's registered decision
problem, because the parents already solve it exactly and the mechanic solves it
less well.* It is not a statement that conceptual development is worthless; it is
a statement about this endpoint, at this size, against this comparator.

## 6. Comparator fairness

`F0_PARENT_FEDERATION` is the strongest faithful parent and is not disadvantaged:
it receives the same instances, the same information, and ordinary engineering
glue in the form of a pre-registered outcome-blind composition rule (extent
geometry decides split/merge, then the implication parent may report a bridge,
then the closure parent decides specialization versus no change). No parent was
artificially isolated: each of P0-P3 is also reported separately (0.400, 0.400,
0.600, 0.400) and each is exact on precisely the families it owns. The federation
beat the mechanic; if anything the asymmetry runs against the mechanic, which is
the direction that cannot inflate a residual claim.

## 7. Pre-outcome corrections and audited hazards

Recorded in `FM30_PRE_RUN_AUDIT_V1.md` before the run and unchanged after it:

- **Inherited G0 verdicts, re-derived not trusted.** `stage_analyze` reads
  `G0a_KNOWN_ANSWER` and `G0e_PLANTED_POSITIVES` from a selftest JSON in the
  output directory rather than recomputing them. The selftest was re-run under
  3.12 and `/usr/bin/diff` reports it byte-identical to the committed report
  (control diff against a different file returns 1). The committed development
  results were likewise reproduced byte-identically. No interpreter drift.
- **A trip-wire that could not fail.** `planted_positives()[2]` is registered as
  `bool(abl and not oracle) or bool(oracle)`; the second disjunct would make it
  "fire" on a non-retention-violating instance. Evaluated: oracle
  `retention_ok = False`, ablation `retention_ok = True`, so the intended clause
  is True on its own merits and the disjunct contributes nothing. Live and
  reporting a true positive today; named here as a latent hazard rather than
  silently relied on.
- **No registered gate clause is narrowed by the runner.** G1a's three clauses
  (identity, per-family, ablation liveness) and G2's three (comparison, liveness,
  minimum n) are all enforced.
- **No numerical failure at the registered size.** The exact two-sided binomial is
  integer-exact and returns without raising at the protected extremes.

Neither `fm_core.py` nor `fm_run.py` was modified; they are shared with FM10-FM60
and the findings above about them are read-only observations.

## 8. Execution discipline

One protected run, one analysis run, as authorized. The authorization was moved to
`PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM30.json` immediately after use and the
guard was verified re-armed (`REFUSED: PROTECTED_RUN_AUTHORIZATION.json absent`).
No design, gate, threshold, seed, arm, oracle rule or generator rule was changed
at any point after the outcome existed.

Authority: grants nothing — no scientific truth, no F2 superiority, no field
status, no submission readiness. `PARENT_SUFFICIENT` is a successful scientific
terminal for a registered decision problem, not a verdict on the mechanic in
general.

skills-applied: none (lane outcome receipt, no manuscript content)
