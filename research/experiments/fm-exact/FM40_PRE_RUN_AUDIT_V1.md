# FM40 — pre-run audit of the frozen design, recorded BEFORE the protected run

**Status when written: no protected instance of FM40 has been generated or
inspected.** Everything below is a check on the frozen design, its runner and
its public development surfaces. Nothing here changes a design, a gate, a
threshold, a seed or an arm. Every item is a *pre-outcome* finding; the one
code change (A4) adds fidelity checks and touches no generator, arm, oracle or
gate.

Interpreter: `/opt/homebrew/bin/python3.12` (CPython 3.12.13). Frozen inputs,
sha256 at audit time:

| file | sha256 |
|---|---|
| `FM40_INVARIANCE_EQUIVARIANCE_DISCOVERY_EXACT_STUDY_DESIGN_V1.json` | `1802ac220e8f945847c21caa1c5c541b6d5ed8d8f2f901fd5482075b302acd0a` (unchanged) |
| `fm40_suite.py` before A4 (as on `origin/main` `3d28db4`) | `20eac1ceb747621445999bac10cbd90c01c975ef87bf97b184f520fb938b5728` |
| `fm40_suite.py` after A4 (the file the protected run executes) | `1461dd3fc90191ec044488eac0d41a4bff4907de2c315e9a489ea862cd0a3b9f` |
| `fm_run.py` (shared, unchanged) | `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59` |
| `fm_core.py` (shared, unchanged) | `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d` |

## A1 — Why the development terminal is not a protected terminal

`FM40_DEVELOPMENT_ANALYSIS_V1.md` routes `PARENT_SUFFICIENT` on **21
instances** (3 per family). Every hard gate passes there, so unlike FM30 and
FM60 there is no unevaluated gate to close; the reason is simpler and it is the
one the design itself states: a development split is not protected evidence,
and `origin/main` carries **no** `FM40_PROTECTED_*` artifact (verified by
listing `fm40/results/`; the control listing of `fm10/results/` shows the full
protected set). A terminal computed on 21 instances reads stronger than it is.

## A2 — The comparator is the oracle, algebraically; what the run can measure

`F0_PARENT_FEDERATION` composes three complete per-stratum procedures under the
registered precedence (P2, then P4, then P0). Measured on four **public** seeds
at the protected size (18 per family, 126 instances; no protected instance
touched): F0 differs from the exhaustive oracle **0 times on each of 4 x 126**,
while the other non-M arms differ 18-108 times. The design's
`known_definitional_results` already says F0's 1.000 "is a statement about the
stratification, not a horse-race win". Consequences registered here, before
any outcome:

- **`G1a` decision identity is an identity when M is also exact.** A
  `126/126` on the protected split would be entailed by both arms computing the
  oracle function, not a contest between them. What the protected leg *does*
  measure is (i) whether M is exact on instances where every single parent
  fails, and (ii) whether M falls short of the oracle anywhere, which shows up
  as G1a discordance in the parent's favour.
- **`G1b_M_ADVANTAGE` cannot fire.** Its clause requires >= 5 M-only-exact
  instances in some family; with F0 exact on every instance, M-only-exact is
  impossible. `FM_RESIDUAL_CANDIDATE` and `M_OVER_ACCEPTS` (both gated on
  G1b) are therefore **unreachable routes on this design**. The detector is a
  `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` in the unfirable direction; it is
  reported `NOT_FIRED` with that reading attached, never as a measured absence
  of advantage. The reachable routes are `PARENT_SUFFICIENT` (two wordings, A7)
  and `CANNOT_CHECK` (G0 failure).
- `G2`'s comparator side is fixed at 0 by the same identity; the gate reduces
  to "M makes no false-invariance claim on the oracle-blocked instances", which
  is failable (a broken closure in M would over-accept) and is carried live by
  `C_ALWAYS_INVARIANT`.

## A3 — Is every hard gate evaluable at the registered protected size?

Run through the **full** `gates()` at 18 per family on the public development
seed (`FM40-DEV-20260902`, not the protected seed): no exception; every hard
gate returned `PASS`; `unchecked_hard_gates` empty. Denominators: G0a 11, G0b
126, G0c 4, G0d 4, G0e 6, G0f 2, G1a 126, **G2 108** (registered minimum 10),
G3 not applicable. G2's counter is live on those instances:
`C_ALWAYS_INVARIANT` 108, `P0_SURFACE_SYMMETRY_SCAN` 51,
`P3_AUGMENTATION_EMPIRICAL` 45, `M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE` 45,
`C_RANDOM_DISPOSITION` 21. G1a's counter is live: ablation-vs-parent
discordance 36 / 60 / 18 / 18. Generator rejections at this size 152-206
across the four public seeds, published per `family|reason`.

**Effective G1a per-family allowance at n = 18 is 0** (`int(0.05 * 18)`), so
the registered 5% rule is exactly "no discordance in any family". The runner
publishes that integer (`per_family_effective_allowance`) so the threshold is
visible as what it is.

## A4 — Fidelity gap closed: F0 was the named comparator and had no fidelity test

`FM_PARENT_FIDELITY_RECEIPT_FM40_V1.md` §2 tests nine subjects (the group
action, P0-P5, the oracle cross-theorem and the reference module) — **not F0**,
the primary comparator. A comparator whose fidelity is asserted but never
checked is a rendered status. Closed before the run by adding five
`F0_PARENT_FEDERATION` checks to `fm40_suite.parent_fidelity`: the precedence
rule on each stratum (P2 on invariance/equivariance, P4 only after an outright
break, P0 only after P4 declines), the registered dominance fixture `KA-06`
(an actionable sub-regime dominates the surface diagnosis), and the composition
rule reproducing the oracle on all 11 fixtures, the last **labelled in its own
test name as an identity, not a measurement**. Selftest now `parents 30/30`.
This is the only code change; it adds no arm, gate, threshold, oracle rule or
generator rule, and the development results and custody files regenerate
**byte-identical** after it (A5).

## A5 — Inherited G0 verdicts re-derived, not trusted

`stage_analyze` reads `G0a`/`G0e` from `FM40_SELFTEST_REPORT.json` in the
output directory. Before A4, `fm_run.py FM40 selftest` under 3.12 into a scratch
directory reproduced the committed report **byte-identical** (`/usr/bin/diff`
exit 0; control diff against the FM50 report exit 1). `fm_run.py FM40 dev`
reproduced `FM40_DEVELOPMENT_RESULTS_V1.json` at sha256 `7c3d608f…` and the
custody file byte-identical; the analysis JSON is identical modulo the
machine-dependent `wall_ms` fields. After A4 the selftest report was
regenerated in place (the five new fidelity rows are its only change) and is
the report the protected analysis will read.

## A6 — Audited against the ledger's shape classes

- *Seed doing nothing*: two different seeds at 18 per family produce different
  results+custody hashes (`4222df15…` vs `d04f7cb6…`). The seed is live.
- *Contrast that could not exist (`x == x`)*: M calls no parent, federation or
  oracle function (design `mechanic_independence`); the registered planted
  positive `mechanic_can_diverge_from_its_own_comparator` moves M off F0 with a
  shortened sample schedule in the same execution that reports the zeros; the
  ablation liveness control registers 36/60/18/18 at protected size.
- *Registered clause silently narrowed*: G1a's three clauses (identity,
  per-family, ablation liveness) and G2's three (comparison, liveness, >= 10)
  are all enforced by `fm_run.py`; FM40's dispositions are `TRANSFER_VALID` and
  `BLOCK_*`, so the runner's generic acceptance test coincides with the
  registered clause "M claims unrestricted invariance no more often than F0 on
  oracle-blocked instances". Not narrowed.
- *Unfailable / unsatisfiable clause*: G1b unfirable (A2) — named, not hidden.
- *Parent isolated by information or budget*: F0 receives the same instance
  object as M and its parents are complete procedures with no budget; the only
  budgeted procedure is M's own value-action sample schedule, a registered
  constant of the mechanic. No handicap runs against the comparator.
- *Hard gate raising at scale*: A3.

## A7 — Route wording registered in advance (both branches)

- **If G1a passes**, the route is `PARENT_SUFFICIENT` with reason "F0
  reproduces M's dispositions (identity …)". The receipt will state at the
  point the number appears that this identity is entailed by F0 being the
  oracle, and will report the non-F0 arms against the oracle as the measured
  content.
- **If G1a fails because M is worse than F0**, the route is still
  `PARENT_SUFFICIENT` by the `else` branch, with reason "no significant M
  advantage over the strongest faithful parent", and the receipt records M's
  shortfall plainly with a single-stage attribution. On the four public seeds
  at protected size M was discordant 0 / 0 / 0 / 0 times, so this branch is
  not expected; it is registered so it cannot read as post-hoc narration if it
  lands.

If the protected leg disagrees with the development leg, that is the finding
and it is reported without re-slicing.

## A8 — What this audit did not do

No protected-scale dry run of the protected seed; the custody seed was hashed
against the frozen commitment (`7431279476019dd15235002757be9fe80f3ad739cfc7964abd7aca83eaa5b93a`)
and not otherwise read. No threshold moved; no arm, oracle rule, generator
rule or stratum weight touched. `fm_core.py` and `fm_run.py` were not modified.

Authority: this audit grants nothing.
