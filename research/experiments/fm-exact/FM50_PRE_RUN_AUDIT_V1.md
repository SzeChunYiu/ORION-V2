# FM50 — pre-run audit of the frozen design, recorded BEFORE the protected run

**Status when written: no protected instance of FM50 has been generated or
inspected.** Everything below is a check on the frozen design, its runner and
its public development surfaces. Nothing here changes a design, a gate, a
threshold, a seed or an arm. Every item is a *pre-outcome* finding; the one
code change (A4) adds fidelity checks and touches no generator, arm, oracle or
gate.

Interpreter: `/opt/homebrew/bin/python3.12` (CPython 3.12.13). Frozen inputs,
sha256 at audit time:

| file | sha256 |
|---|---|
| `FM50_FUNCTORIALITY_COMMUTING_DIAGRAMS_EXACT_STUDY_DESIGN_V1.json` | `3d647d0b028327df127bd7fdd45fbc9dfd38409f2148a236f543135a1015b387` (unchanged) |
| `fm50_suite.py` before A4 (as on `origin/main` `3d28db4`) | `c485034f4904653e15102809588f850381c8b007de5363e652bb7830b78d262b` |
| `fm50_suite.py` after A4 (the file the protected run executes) | `d056e281c0101bd4ef645b6ad7dd6fe1a1f84807c8136da10d9c565b66af75f4` |
| `fm_run.py` (shared, unchanged) | `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59` |
| `fm_core.py` (shared, unchanged) | `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d` |

## A1 — Why the development terminal is not a protected terminal

`FM50_DEVELOPMENT_ANALYSIS_V1.md` routes `PARENT_SUFFICIENT` on **24 eligible
instances** (3 per family). Every hard gate passes there; the defect is that a
development split is not protected evidence, and `origin/main` carries **no**
`FM50_PROTECTED_*` artifact (verified by listing `fm50/results/`; control:
`fm10/results/` and `fm20/results/` carry full protected sets).

## A2 — The comparator is the oracle, algebraically; what the run can measure

`F0_PARENT_FEDERATION` composes the category-law parent (P2) and the
faithfulness parent (P4): P2 decides every functor law, P4 is consulted only
when every law holds. Measured on four **public** seeds at the protected size
(13 per family, 104 eligible instances; no protected instance touched): F0
differs from the exhaustive oracle **0 times on each of 4 x 104**; the other
non-M arms differ 13-91 times. Registered consequences, before any outcome:

- **`G1a` is an identity when M is also exact**, and the design says so more
  strongly than for any sibling (`mechanic_independence.honest_limit`): the
  law fragment is a total function of the registered candidate, so any correct
  implementation agrees with any other. What the protected leg measures is
  whether M's own precedence resolution and its *discovered* (not registered)
  diagram set agree with the oracle everywhere, and whether M is exact on the
  instances where each single parent fails.
- **`G1b_M_ADVANTAGE` cannot fire** (>= 5 M-only-exact instances in a family is
  impossible against an oracle-identical comparator), so
  `FM_RESIDUAL_CANDIDATE` and `M_OVER_ACCEPTS` are **unreachable routes**.
  Named as a `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` in the unfirable
  direction; `NOT_FIRED` is reported with that reading, not as a measured
  absence of advantage.
- `G2`'s comparator side is fixed at 0; the gate reduces to "M accepts no
  transfer the oracle blocks", failable by an M bug and carried live by
  `C_ALWAYS_TRANSFER`.

## A3 — Is every hard gate evaluable at the registered protected size?

Run through the **full** `gates()` at 13 per family on the public development
seed (`FM50-DEV-20260902`): no exception; every hard gate `PASS`;
`unchecked_hard_gates` empty. Denominators: G0a 11, G0b 104, G0c 4, G0d 4, G0e
6, G0f 2, G1a 104, **G2 65** (minimum 10), G3 not applicable. G2 liveness on
those instances: `C_ALWAYS_TRANSFER` 65, `P0`/`P1`/`P4` 52, `P3` 45, `P5` 39,
`P2` 13, each ablation 13, `C_RANDOM_DISPOSITION` 11. G1a liveness: 13 / 26 /
26 / 13. Generator rejections at this size 65-77 across the four public seeds;
the eligibility gate `G0g` is suite-owned and its INELIGIBLE count is published
per family inside `generator_rejections`, never scored against an arm.

**Effective G1a per-family allowance at n = 13 is 0** (`int(0.05 * 13)`): the
5% rule is exactly "no discordance in any family", and the runner publishes
that integer.

## A4 — Fidelity gap closed: F0 was the named comparator and had no fidelity test

`FM_PARENT_FIDELITY_RECEIPT_FM50_V1.md` §2 tests P0-P5, the reference module
and the eligibility gate — **not F0**, the primary comparator. Closed before
the run by adding four `F0_PARENT_FEDERATION` checks to
`fm50_suite.parent_fidelity`: F0 takes the law parent on every law violation
including the two precedence fixtures (`KA-09`, `KA-10`), consults the
faithfulness parent only after every law holds (`KA-07`, the constant functor),
accepts only when both parents accept (`KA-01`, `KA-08`, `KA-11`), and the
composition rule reproduces the oracle on all 11 fixtures — **labelled in its
own test name as an identity, not a measurement**. Selftest now `parents
32/32` (26 comparator tests + 6 eligibility-gate tests, still reported
separately). No arm, gate, threshold, oracle rule or generator rule changed;
development results and custody regenerate byte-identical (A5).

## A5 — Inherited G0 verdicts re-derived, not trusted

Before A4, `fm_run.py FM50 selftest` under 3.12 into a scratch directory
reproduced the committed `FM50_SELFTEST_REPORT.json` **byte-identical**
(`/usr/bin/diff` exit 0; control diff against another suite's report exit 1),
and `fm_run.py FM50 dev` reproduced `FM50_DEVELOPMENT_RESULTS_V1.json` at
sha256 `ed6b1faa…` and the custody file byte-identical; the analysis JSON is
identical modulo `wall_ms`. After A4 the selftest report was regenerated in
place (the four new rows are its only change).

## A6 — Audited against the ledger's shape classes

- *Seed doing nothing*: two seeds at 13 per family give different
  results+custody hashes (`1b912ea0…` vs `140c0ead…`). Live.
- *Contrast that could not exist*: M never calls `assess_functor` or
  `claim_profile` (`test_mechanic_is_not_a_wrapper_of_its_own_comparator`
  passes); the honest limit — identity expected by mathematics — is
  pre-registered in the design and restated in A2, and the ablation liveness
  control is 13/26/26/13 at protected size.
- *Registered clause silently narrowed*: FM50's dispositions are
  `TRANSFER_VALID` and `BLOCK_*`, so the runner's generic acceptance test is
  the registered G2 clause; G1a's three clauses are enforced. Not narrowed.
- *Unfailable / unsatisfiable clause*: G1b unfirable (A2) — named.
- *Parent isolated by information or budget*: F0 gets the same instance object;
  both of its parents are complete decision procedures with no budget. No
  handicap.
- *Hard gate raising at scale*: A3.

## A7 — Route wording registered in advance (both branches)

- **If G1a passes**: `PARENT_SUFFICIENT`, "F0 reproduces M's dispositions
  (identity …)", with the identity stated as entailed at the point the number
  appears and the non-F0 arms reported against the oracle as the measured
  content.
- **If G1a fails because M is worse than F0**: still `PARENT_SUFFICIENT` by
  the `else` branch, "no significant M advantage over the strongest faithful
  parent", with M's shortfall attributed to one stage (its precedence
  resolution or its discovered diagram set are the only channels). On four
  public seeds at protected size M was discordant 0 / 0 / 0 / 0 times; the
  branch is registered so it cannot read as narration if it lands.

A protected leg that disagrees with the development leg is the finding.

## A8 — What this audit did not do

No protected-scale dry run of the protected seed; the custody seed was hashed
against the frozen commitment (`b45a1644e3219ce0cca4e3307dacc7c4c20e50833095fc4d1ed579fa3948fe46`)
and not otherwise read. No threshold moved; no arm, oracle rule, generator
rule or eligibility rule touched. `fm_core.py` and `fm_run.py` not modified.

Authority: this audit grants nothing.
