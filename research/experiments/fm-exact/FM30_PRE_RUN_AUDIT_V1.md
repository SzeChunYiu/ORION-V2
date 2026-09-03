# FM30 — pre-run audit of the frozen design, recorded BEFORE the protected run

**Status when written: no protected instance of FM30 has been generated or
inspected.** Everything below is a check on the frozen design, its runner and
its public development surfaces. Nothing here changes a design, a gate, a
threshold, a seed or an arm. Every item is a *pre-outcome* finding.

Interpreter: `/opt/homebrew/bin/python3.12` (CPython 3.12.13).
Frozen inputs, sha256 at audit time:

| file | sha256 |
|---|---|
| `FM30_FORMAL_CONCEPT_REVISION_EXACT_STUDY_DESIGN_V1.json` | `d3e1fbf0d09b45e4d266ed55545f1cc07c90f10aaf0e97e36484f8898bf26a3c` |
| `fm30_suite.py` | `3259b79262595f27a71d664f7ff8ecc2014c022c987a5a1a5a5dacb6a5ef4011` |
| `fm_run.py` (shared) | `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59` |
| `fm_core.py` (shared) | `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d` |

## A1 — The reason the development terminal is not a protected terminal

`FM30_DEVELOPMENT_ANALYSIS_V1.md` routes `PARENT_SUFFICIENT` on **15 instances**
and its hard gate `G2_ANTI_PERMISSIVENESS` returns **`CANNOT_CHECK`**, evaluated
on **1** instance against a registered minimum of 10. The analysis file already
refuses to report that gate as passing, and the route line names it. That is the
correct behaviour and it is also the reason the development route cannot stand as
this study's terminal: a hard gate that could not be evaluated is not a hard gate
that passed.

## A2 — Is `G2_ANTI_PERMISSIVENESS` evaluable at the registered protected size?

This is the question the development split leaves open, and it had to be answered
before spending the single authorized protected run.

G2's scope is `unsafe_scope = lambda e: e["retention_ok"] is False` — the oracle
instances on which old-valid-case retention genuinely fails. Registered minimum:
10 (`requires_evaluated=10`). Registered protected size: 20 per family x 5
families = 100.

Measured on **public** seeds at the protected size (no protected instance
touched), counting oracle instances with `retention_ok is False`:

| public seed | n | in G2 scope |
|---|---|---|
| `FM30-G2SCOPE-PUBLIC-A` | 100 | 26 |
| `FM30-G2SCOPE-PUBLIC-B` | 100 | 28 |
| `FM30-G2SCOPE-PUBLIC-C` | 100 | 29 |
| `FM30-DEV-20260902` at per-family 20 | 100 | 29 |

26-29 against a minimum of 10. The development `CANNOT_CHECK` is a small-n
artefact of 15 instances, **not** a structural defect that would survive to the
protected size. Recorded before the run so that a protected G2 verdict cannot be
read as luck.

G2's liveness control (`max_over > 0`) is satisfied by construction and not by
hope: `ablation_minus_old_case_retention` returns `{**full, "retention_ok": True}`
unconditionally, so on every scope instance that arm registers an unsafe claim.
The counter cannot be dead.

## A3 — Registered gate clauses vs. what the runner enforces

Checked for the failure mode "a registered gate clause the runner silently
narrows".

- **G1a** is registered as three clauses: identity >= 99.5%, no family above 5%
  discordance, **and** the discordance counter shown live by at least one
  ablation. `fm_run.py` enforces all three (`identity_rate >= 0.995` and the
  per-family rule and `counter_is_live`), and publishes the per-family integer
  allowance so a "0 permitted" threshold is visible as such. Not narrowed.
- **G2** is registered as the unsafe-claim comparison **and** a liveness control
  **and** a >= 10 minimum. All three are enforced. Not narrowed.
- **G3** is registered applicable only if G1b fires; the runner marks it
  `NOT_APPLICABLE` otherwise, which is distinct from `PASS`. Correct.

## A4 — Hard G0 verdicts are read from a file; that file was re-derived, not trusted

`stage_analyze` reads `FM30_SELFTEST_REPORT.json` from the output directory and
takes the hard gates `G0a_KNOWN_ANSWER` and `G0e_PLANTED_POSITIVES` from it
rather than recomputing them. A protected analysis written into a directory that
already holds a development-era selftest report would therefore *inherit* its
hard validity verdicts — a rendered status standing in for the thing.

Closed by re-derivation, not by assumption: `fm_run.py FM30 selftest` was re-run
under 3.12 into a scratch directory and `/usr/bin/diff` against the committed
`fm30/results/FM30_SELFTEST_REPORT.json` reports the two files **identical**
(a control diff against a different file in the same directory returns 1, so the
comparison is live). Selftest verdict: parents 17/17, known-answer 9/9, planted
6/6, oracle agreement 10/10, null calibration PASS.

The committed development results were also re-derived: `fm_run.py FM30 dev`
under 3.12 reproduces `FM30_DEVELOPMENT_RESULTS_V1.json` at sha256
`8517dab07655e83cf7bab6ccd204cf3dacdc748c522461329be7c18ecf656d92`, byte-identical
to the frozen value. There is no interpreter drift between the frozen artifacts
and the interpreter that will run the protected split.

## A5 — A trip-wire that could not fail (audited, inert, named)

`fm30_suite.planted_positives()` registers the G2 trip-wire as

```python
P[2].fired = bool(abl["retention_ok"] and not o.retention_ok) or bool(o.retention_ok)
```

The second disjunct means the planted positive would also "fire" on an instance
where the oracle says retention holds — that is, on an instance that is not a
retention-violating case at all. As written this trip-wire cannot fail.

Evaluated on the constructed instance `PP-RET`: `oracle.retention_ok = False`,
`ablation.retention_ok = True`, so the **intended** clause is `True` on its own
merits and the escape disjunct contributes nothing. The trip-wire is therefore
**live today and reporting a true positive**, not a vacuous pass. It is recorded
here as a latent hazard rather than repaired, because repairing it after the
design freeze would change a registered validity artifact for no change in
value; the correct disposition is that the receipt states the value and the
audit rather than leaving a reader to assume the disjunct was intended.

## A6 — Numerical safety at the registered protected size

Checked for the failure mode "a hard gate raising at the registered protected
size". The exact two-sided binomial used by the paired tests is integer-exact
(`math.comb` over Python ints divided by `2**n`); evaluated at the protected
extremes it returns without raising. FM30's protected n is 100, far below the
1200-scale probe at which the same routine was exercised.

## A7 — Route wording registered in advance (both branches)

The design's own development probe at 100 instances records M at **0.980**
against the federation's 1.000, diverging on 2 bridge instances. At n = 100 an
identity rate of 0.98 is **below** G1a's 99.5% threshold. Both branches are
therefore registered here, before the protected split exists, so that neither
wording can read as post-hoc narration:

- **If G1a passes**, the route is `PARENT_SUFFICIENT` with reason "F0 reproduces
  M's dispositions (identity ...)".
- **If G1a fails because M is worse than the federation**, the route is *still*
  `PARENT_SUFFICIENT`, by the `else` branch, with reason "no significant M
  advantage over the strongest faithful parent". The design anticipates exactly
  this: *"If G1a fails because M is WORSE than the federation, the route is still
  PARENT_SUFFICIENT and that is recorded explicitly rather than presented as a
  study defect."*

Same terminal, materially different sentence. Which one lands is decided by the
protected split, not by the writer.

## A8 — What this audit did not do

No protected-scale dry run of the protected seed. The protected seed was hashed
against the frozen commitment and not otherwise read. No G2, G1a or G0 threshold
was moved. No arm, oracle rule, generator rule or stratum weight was touched.
`fm_core.py` and `fm_run.py` are shared with FM10-FM60 and were **not modified**;
A3 and A4 are read-only findings about them.

Authority: this audit grants nothing. It establishes only that the frozen FM30
design can be executed at its registered size with its registered gates
evaluable, and it fixes the wording of both admissible routes in advance.
