# FM60 — pre-run audit of the frozen design, recorded BEFORE the protected run

**Status when written: no protected instance of FM60 has been generated or
inspected.** Everything below is a check on the frozen design, its runner and
its public development surfaces. Nothing here changes the design JSON, a
threshold, a seed, an arm, an oracle rule or a generator rule. Two code changes
are made and both are pre-outcome corrections: A2 binds `G2` to the clause the
design registers, and A4 adds one fidelity check.

Interpreter: `/opt/homebrew/bin/python3.12` (CPython 3.12.13). Frozen inputs,
sha256 at audit time:

| file | sha256 |
|---|---|
| `FM60_OBSTRUCTION_COUNTEREXAMPLE_EXACT_STUDY_DESIGN_V1.json` | `f8fe7f09463938c25df3b8ddba0ead71a06616de5affddc1622b744fde463a69` (unchanged) |
| `fm60_suite.py` before A2/A4 (as on `origin/main` `3d28db4`) | `4fc0ef81385708a4c1efa3d8cc6c15efecd739d38954ae02a502f7e5ceb6cf6a` |
| `fm60_suite.py` after A2/A4 (the file the protected run executes) | `f008258f0db82af5a855396858f37d8a4180c334affa8f104ea7ef5300d9f55c` |
| `fm_run.py` (shared, unchanged) | `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59` |
| `fm_core.py` (shared, unchanged) | `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d` |

## A1 — Why the development terminal is not a protected terminal

`FM60_DEVELOPMENT_ANALYSIS_V1.md` (as re-derived by PR #238) routed
`PARENT_SUFFICIENT` on **15 instances** with the hard gate
`G2_ANTI_PERMISSIVENESS = CANNOT_CHECK`, evaluated on **9** instances against a
registered minimum of 10, and the analysis refused to report that gate as
passing. A hard gate that could not be evaluated is not a hard gate that
passed; and `origin/main` carries **no** `FM60_PROTECTED_*` artifact. Both
defects are closed by the protected run — but the 9 was itself the symptom of a
second defect, A2, which had to be repaired first.

## A2 — `G2` was evaluating a narrower clause than the one registered (repaired pre-run)

The design registers G2 as: *"on instances the oracle blocks, M accepts no
more conjectures than F0 (>= 10 blocked instances required)"*. FM60 did not
declare the `unsafe_scope` / `unsafe_claim` hooks, so the shared runner fell
back to its generic reading: an oracle label counts as blocked only if it starts
with `BLOCK` or `REJECT`, and an arm's label counts as an acceptance unless it
does. FM60's `MULTIPLE_INDEPENDENT_OBSTRUCTIONS` starts with neither, so every
multiple-obstruction instance was **dropped from G2's scope** (a fifth of the
blocked population), and three arm outputs that are not acceptances —
`MULTIPLE_INDEPENDENT_OBSTRUCTIONS`, `UNDECIDED_BUDGET_EXHAUSTED`,
`CLAIM_WITHOUT_VALID_WITNESS` — were **counted as unsafe claims**. PR #238's
re-derivation found the second half (a liveness nonzero contributed by
`C_ALWAYS_BLOCK`, an arm that never accepts anything) and deferred the fix
because "declaring the hooks changes what the gate evaluates". It does: it
changes it to the registered clause. This is `REGISTERED_SCOPE_DIVERGENCE`,
and a narrowed clause is `CANNOT_CHECK`, never pass — so it is repaired before
the single authorized run, not carried into it.

Repair, in `fm60_suite.SPEC` only:

```python
unsafe_scope=lambda e: e["disposition"] != "TRANSFER_VALID",
unsafe_claim=lambda rec, e: rec["disposition"] == "TRANSFER_VALID",
unsafe_name="conjecture accepted where the oracle blocks it",
```

Measured effect on the **public** development seed at the protected size (25
per family, 125 instances; no protected instance touched):

| quantity | generic fallback (before) | registered clause (after) |
|---|---|---|
| G2 scope (oracle-blocked instances) | 75 | **100** |
| unsafe claims, `C_ALWAYS_ACCEPT` | 75 | 100 |
| unsafe claims, `C_ALWAYS_BLOCK` | 75 (false: it never accepts) | **0** |
| unsafe claims, `P3_DERIVATION_PROOF_SEARCH` | 75 (abstentions miscounted) | **0** |
| unsafe claims, `M` / `F0` | 0 / 0 | 0 / 0 |
| liveness carried by | `C_ALWAYS_ACCEPT`, `C_ALWAYS_BLOCK`, `P3`, … | `C_ALWAYS_ACCEPT` 100, `C_RANDOM_DISPOSITION` 15 |

On the 15-instance development split the registered clause puts **12** instances
in scope (minimum 10) and the gate is `PASS`; `FM60_DEVELOPMENT_ANALYSIS_V1.{json,md}`
were re-derived under the binding by `fm_run.py FM60 analyze` (results, custody
and timing untouched), and this re-derivation is recorded here as a
pre-outcome correction of a development artifact. The design JSON is not
changed: the code now does what the design says.

**What G2 can and cannot measure on FM60, stated before the run.** Every
non-control arm passes the witness validator, all 50 registered rules are
verified valid over the whole 4,164-structure space, and a derivation citing
an unregistered rule or an unavailable premise is rejected. A validated
derivation of a conjunct that has a countermodel is therefore impossible, and
so is an unsafe claim by any validated arm. G2's `PASS` for M is **entailed by
the soundness of the rule base plus the witness gate**, not measured; the gate
checks that the machinery is wired, and its liveness is carried only by the
registered-exempt controls. That is what the design's `control_exemption`
paragraph says in other words; it is restated here so the protected `0 <= 0
over 100` cannot be read as restraint on M's part.

## A3 — Is every hard gate evaluable at the registered protected size?

Under the registered binding, the **full** `gates()` at 25 per family on three
public seeds: no exception; `unchecked_hard_gates` empty on every seed; G2
evaluated on 100 with `PASS`. Denominators: G0a 12, G0b 125, G0c 4, G0d 3, G0e
7, G0f 2, G1a 125, G2 100. G1a's liveness control at this size: 102 / 25 / 30 /
27 ablation-vs-parent disagreements. Generator rejections 2,563-3,331 per
public seed, published per family.

**G1a is not expected to pass, and both branches are registered (A7).** The
effective per-family allowance at n = 25 is **1** (`int(0.05 * 25)`). On the
four public seeds at protected size M and F0 were discordant **2 / 4 / 1 / 0**
times (identity 0.984 / 0.968 / 0.992 / 1.000), and G1a **fails on three of the
four** because a family carries two or more discordances. All seven public
discordances have one signature: **M abstains (`UNDECIDED_BUDGET_EXHAUSTED`)
where F0 decides** — six on `no_obstruction` instances where the derivation
parent finds the proof, one on a `misleading_surface_support` instance where
the model parent finds the deep countermodel. The single stage is M's
registered proof budget, `PROOF_STEP_BUDGET = 12` rule applications of bounded
forward chaining, against the parent's saturating search. That is M's own
mechanic constant, frozen in the design (`mechanic_independence`), not a
handicap on the comparator: the parent is complete and unbudgeted. The
fidelity receipt's budget-starvation table already showed M's rate moves off
1.000 when its exploration is cut; the public seeds now show it moving at the
registered budget, which the 15-instance development split was too small to
see. The protected split decides which branch lands; neither is a study defect.

## A4 — Fidelity: F0 was tested; the identity is now checked and labelled

Unlike FM10/FM20/FM40/FM50, `FM_PARENT_FIDELITY_RECEIPT_FM60_V1.md` already
carries three `F0_PARENT_FEDERATION` checks (P3 on a theorem, P2 on a
non-theorem, abstention when neither can discharge). One check is added: the
composition rule reproduces the oracle on all 12 registered fixtures,
**labelled in its own test name as an identity, not a measurement**, with the
honest scope stated in the source — on the generator's population F0 is
oracle-identical by construction (reject families are decided by the
exhaustive parent; `no_obstruction` conclusions are drawn from the rule base's
closure, which the derivation parent saturates), but **not** off-population:
the abstention fixture is a bounded-valid claim the oracle accepts and neither
parent can discharge. Measured: F0 differs from the oracle **0 times on each of
4 x 125** public instances. Selftest now `parents 33/33`.

Consequences registered before the run: `G1b_M_ADVANTAGE` cannot fire (no
M-only-exact instance is possible against an oracle-identical comparator), so
`FM_RESIDUAL_CANDIDATE` and `M_OVER_ACCEPTS` are unreachable routes and
`NOT_FIRED` is reported with that reading, not as a measured absence.

## A5 — Inherited G0 verdicts re-derived, not trusted

Before any edit, `fm_run.py FM60 selftest` under 3.12 into a scratch directory
reproduced the committed `FM60_SELFTEST_REPORT.json` **byte-identical**
(`/usr/bin/diff` exit 0; control diff exit 1), and `fm_run.py FM60 dev`
reproduced `FM60_DEVELOPMENT_RESULTS_V1.json` at sha256 `a97a9bd2…` and the
custody file byte-identical (analysis identical modulo `wall_ms`). After A2/A4
the selftest report was regenerated in place (one new fidelity row is its only
content change) and the development analysis re-derived as described in A2.

## A6 — Audited against the ledger's shape classes

- *Seed doing nothing*: two seeds at 25 per family give different
  results+custody hashes (`9c88da21…` vs `2cfdc151…`). Live.
- *Contrast that could not exist*: M's local-repair search and bounded proof
  are its own; the budget-starvation probe in the fidelity receipt and the
  public-seed discordances in A3 show M diverging from F0 at the registered
  budget. The contrast exists.
- *Registered clause silently narrowed*: G2 — found and repaired (A2). G1a's
  three clauses enforced.
- *Unfailable / unsatisfiable clause*: G1b unfirable (A4); G2 unfailable for
  validated arms by soundness (A2) — both named.
- *Parent isolated by information or budget*: the comparator is complete and
  unbudgeted; the only budgets are M's own registered constants
  (`PROOF_STEP_BUDGET`, `M_PROBE_BUDGET`, `M_SEED_TARGET`). No handicap runs
  against F0; if anything the asymmetry runs against M, which is the direction
  that cannot inflate a residual.
- *Hard gate raising at scale*: A3.

## A7 — Route wording registered in advance (both branches)

- **If G1a passes**: `PARENT_SUFFICIENT`, "F0 reproduces M's dispositions
  (identity …)", the identity stated as entailed where the number appears.
- **If G1a fails because M is worse than F0** (the branch three of four public
  seeds predict): still `PARENT_SUFFICIENT` by the `else` branch, "no
  significant M advantage over the strongest faithful parent", with the
  receipt reporting M's shortfall, its single-stage attribution (A3) and the
  revival honestly stated — the lever that repairs it is a saturating proof
  search, which *is* `P3_DERIVATION_PROOF_SEARCH`, so applying it means
  adopting the parent.

A protected leg that disagrees with the 15-instance development leg (which
recorded identity 1.0000) is the finding, and it is reported without
re-slicing.

## A8 — What this audit did not do

No protected-scale dry run of the protected seed; the custody seed was hashed
against the frozen commitment (`54a74a5960b88ed7973b690890a3fcb21bf80580d2a459075aae799aacbe02f2`)
and not otherwise read. No threshold, arm, oracle rule, generator rule or
budget constant was moved. `fm_core.py` and `fm_run.py` were not modified.

Authority: this audit grants nothing.
