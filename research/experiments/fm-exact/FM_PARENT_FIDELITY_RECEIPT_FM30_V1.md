# FM30 — Parent Fidelity Receipt and Development-Split Summary (V1)

> **SUPERSEDED IN PART, 2026-09-03.** The status line below was true when this
> receipt was written and is no longer true. FM30's protected run has since been
> executed under `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM30.json`; the terminal
> now stands on `FM30_OUTCOME_RECEIPT.md` (100 protected instances, route
> `PARENT_SUFFICIENT`, `G2_ANTI_PERMISSIVENESS` PASS on 36 in-scope instances,
> `G1a_PARENT_REPRODUCES_M` FAIL at identity 0.920). **Everything below this line
> describes the development split only and must not be read as this study's
> terminal.** The parent-fidelity and frozen-hash content remains valid.

**Status:** development artifacts only. **No protected outcome has been generated
or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent, so
`fm_run.py FM30 protected` refuses (exit 3), asserted by test.

**Run:** Mac (local), 2026-09-02, `selftest` then `dev`; each well under a second,
byte-identical across consecutive runs, and identical under `PYTHONHASHSEED`
0/1/12345.

## 1. Frozen code and artifacts (sha256)

| file | sha256 |
|---|---|
| `fm_core.py` | `edb1711218f7d7c170141eaac494222c9913cc7d3d12c90a14cb0aef802e5c8d` |
| `fm_run.py` | `888037788ca3fa4eb6cecb9dcfaec930975727e4d924bf2c94a8e5e20c10cb59` |
| `fm30_suite.py` | `3259b79262595f27a71d664f7ff8ecc2014c022c987a5a1a5a5dacb6a5ef4011` |
| `FM30_..._DESIGN_V1.json` | `d3e1fbf0d09b45e4d266ed55545f1cc07c90f10aaf0e97e36484f8898bf26a3c` |
| `fm30/results/FM30_DEVELOPMENT_RESULTS_V1.json` | `8517dab07655e83cf7bab6ccd204cf3dacdc748c522461329be7c18ecf656d92` |
| `fm30/results/FM30_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `5d62bfe2f67d4921edd412af1febfc9a495404223e0c9cff5cd9c006e1ec00c6` |
| `fm30/results/FM30_SELFTEST_REPORT.json` | `2d501ef3e31096ddc8c1aa8715d1f99aaf4c60c772bf1edda66ab65ef4e22dd0` |

Protected seed commitment:
`af34cfe913bff1ef0f661b1ee4b46ff68360fa3a6bea2d06b776ca2b35857e4a`.

## 2. Parent fidelity: native known-answer tests (17/17 PASS)

| parent | tests (all PASS) |
|---|---|
| `P1_GALOIS_CLOSURE` (Ganter-Wille) | derivation of an object set is the shared attributes; derivation of an attribute set is the common objects; the empty object set derives every attribute and vice versa; closure is idempotent and extensive; derivation is antitone; documented boundary - the closure parent classifies only intent growth and computes no extent geometry |
| `P2_LATTICE_ORDER_GEOMETRY` | detects a genuine split of a tracked extent; documented boundary - extent geometry never inspects intents, so specialization is invisible to it |
| `P0_FIXED_LESSON_INJECTION` | says specialize whenever an attribute is added; says no change when only objects are added |
| `ORACLE_PAIR` | powerset closure equals NextClosure on the textbook context, an empty-incidence context, a full-incidence context and a chain; the textbook context's lattice has the expected size |

One fidelity test was itself wrong before the parent disagreed with it: the first
draft asserted a split from a single new attribute distinguishing one object,
which is a differentiation but not a split under the registered definition. The
test was corrected, not the parent.

## 3. Known-answer fixtures (G0a): 9/9

All nine reproduced by the exhaustive oracle and the NextClosure cross-check.
`KA-09` pins the registered precedence — a revision on which both `MERGE` and
`SPECIALIZE` hold is classified `MERGE` with both published in the hold-set.

## 4. Planted positives (G0e): 6/6 fire

| gate | planted case | fires |
|---|---|---|
| `G0b` | a deliberately non-idempotent "closure" (one derivation instead of two) must produce a different concept set from NextClosure | yes |
| `G0a` | a deliberately wrong expected transition | yes |
| `G2` | an arm claiming retention where the oracle says retention fails | yes |
| `G0f` | a synthetic all-ceiling arm table must **FAIL** the gate | yes |
| `G3` | `M_MINUS_EXTENT_GEOMETRY` must be wrong on a hand-built split where `M` is right | yes |
| `G0a` | the registered precedence is exercised and the full hold-set published | yes |

## 5. Development split (15 instances, 3 per family — DEVELOPMENT, not protected)

| arm | exact | rate |
|---|---|---|
| `F0_PARENT_FEDERATION` | 15/15 | 1.000 |
| `M_F2_CONCEPTUAL_DEVELOPMENT_FULL` | 15/15 | 1.000 |
| `M_MINUS_OLD_CASE_RETENTION` | 14/15 | 0.933 |
| `M_MINUS_BRIDGE_DETECTION` | 12/15 | 0.800 |
| `M_MINUS_CLOSURE_RECOMPUTATION` | 12/15 | 0.800 |
| `M_MINUS_EXTENT_GEOMETRY` | 9/15 | 0.600 |
| `P2_LATTICE_ORDER_GEOMETRY` | 9/15 | 0.600 |
| `P0_FIXED_LESSON_INJECTION` | 6/15 | 0.400 |
| `P1_GALOIS_CLOSURE` | 6/15 | 0.400 |
| `P3_ATTRIBUTE_EXPLORATION` | 6/15 | 0.400 |
| `C_ALWAYS_SPECIALIZE` | 3/15 | 0.200 |
| `C_ALWAYS_NO_CHANGE` | 2/15 | 0.133 |
| `C_RANDOM_TRANSITION` | 1/15 | 0.067 |

### 5.1 Development gate block

Every G0 gate PASS with its denominator printed; `G1a` PASS (identity
1.000); `G1b` NOT_FIRED; `G3` NOT_APPLICABLE.

**`G2` returns `CANNOT_CHECK`** on this split: only 1 instance has
`retention_ok = False`, below the registered minimum of 10. The route line names
it explicitly rather than letting an unchecked hard gate read as agreement. On a
100-instance probe the scope is 26 instances and the counter registers 26 unsafe
claims from the retention ablation, so the protected split will have a real
denominator.

G1a liveness control on development: {'M_MINUS_BRIDGE_DETECTION': 3, 'M_MINUS_CLOSURE_RECOMPUTATION': 3, 'M_MINUS_EXTENT_GEOMETRY': 6, 'M_MINUS_OLD_CASE_RETENTION': 1}.

## 6. Development probe at protected scale (100 instances — not protected evidence)

`F0` 1.000, **`M` 0.980**, `M_MINUS_BRIDGE_DETECTION` 0.800,
`M_MINUS_CLOSURE_RECOMPUTATION` 0.780, `M_MINUS_OLD_CASE_RETENTION` 0.740,
`P2` and `M_MINUS_EXTENT_GEOMETRY` 0.600, `P0`/`P1`/`P3` 0.400, controls
0.200/0.120/0.050.

`M` diverges on two bridge instances where its attribute-seeded sub-concept count
reaches two while the full lattice's maximal proper sub-extent count does not.
This is the price of closing a handful of seeds instead of enumerating: the count
is a lower bound, and comparing two lower bounds can flip an inequality. Verified
**not** to be a scope artifact — restricting `M` to the pre-existing objects
changes neither instance.

## 7. Corrections recorded

Three defects in `M` itself, all found on development probes and repaired before
freezing:

1. it reported `MERGE` for concepts that were **already** merged (no "before"
   test — a transition has to be a change);
2. its split test counted attribute-cuts that are not themselves concepts, which
   over-fired `SPLIT` on bridges;
3. an earlier draft looked only at **new** attributes and so missed splits formed
   by an old attribute together with a new one.

And one in the suite's own gate design: `G2`'s inherited over-acceptance rule had
an **empty scope** here, since no transition is an "accept". It would have passed
vacuously on `0 ≤ 0`. The non-compensatory endpoint was re-registered as
old-valid-case loss, and a registered fraction of revisions now retract an
incidence pair so that the endpoint has a denominator at all.

## 8. Estimated protected-run cost

100 instances × 13 arms: a same-size probe completed in **0.33 s** wall.
Budget: 1 CPU-minute. Runs on the Mac.
