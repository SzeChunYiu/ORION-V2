# FM50 — Functoriality and Commuting Diagrams: Exact Known-Answer Study Design (V1)

**Status:** `FROZEN_PROSPECTIVE_DESIGN_NO_PROTECTED_OUTCOME_ACCESS`.
**Owner issues:** #48, #50 §C1. **Protocol:** `ORION-TD-FORMAL-MECHANICS-V1`, study FM50.
**Machine-readable twin:** `FM50_FUNCTORIALITY_COMMUTING_DIAGRAMS_EXACT_STUDY_DESIGN_V1.json`
(authoritative for every number in this file).

This design is frozen before any protected outcome exists. It grants no
scientific truth, no F2 superiority, no field status and no submission
readiness.

## 1. Why this suite exists, given FM/FG R2

The FM/FG R2 registered-scale campaign dispatched an `fm50` cell through an LLM
and it landed near ceiling — 1.000 / 0.927 / 0.969 / 1.000 / 0.990 across its
five arms. A cell on which every arm scores the same could not have detected a
difference had one existed, so it is uninformative rather than null. `G0f`, the
family-discrimination gate, now fails that condition explicitly and a planted
positive proves the predicate fires on a synthetic all-ceiling table in the same
execution that reports the study's zeros.

The second reason is specific to this suite. FM50's protocol entry carries an
**eligibility clause** — "only cases whose native construction forms the required
finite categorical structure" — and on 2026-09-02 this programme found a checker
nested inside an applicability guard that excluded the whole family under test,
so it reported zero violations having never run. An eligibility clause is
exactly the shape of condition that produces that defect. FM50 therefore treats
eligibility as a **gate with a published denominator**, not as a filter.

## 2. Task and endpoint

Each instance registers a transfer claim in categorical form: a donor finite
category `D`, a target finite category `T`, a candidate functor `F : D → T`
(total object map and total morphism map), the donor morphism pairs whose
**distinction the claim depends on**, and the **commuting diagrams** the claim
writes down. The endpoint is the exact disposition of that claim:

| disposition | meaning |
|---|---|
| `TRANSFER_VALID` | every functor law holds and every registered distinction survives |
| `BLOCK_ENDPOINT_VIOLATION` | some arrow's image does not run between the images of its endpoints — `F` is not even a map of the underlying graphs |
| `BLOCK_IDENTITY_NOT_PRESERVED` | endpoints hold, some identity is not sent to an identity |
| `BLOCK_COMPOSITION_NOT_PRESERVED` | endpoints and identities hold, some composite is not preserved |
| `BLOCK_MIXED_LAW_OBSTRUCTION` | both unit and composition laws fail |
| `BLOCK_FALSE_EQUIVALENCE` | `F` is a genuine functor but collapses a registered distinction |

Registered precedence: endpoint > (identity, composition) > distinction. The
mixed class exists so that the order is visible and pinnable by a fixture rather
than hidden inside a tie-break; `KA-06`, `KA-09` and `KA-10` pin it.

### Why the valid token is `TRANSFER_VALID` and not `FUNCTOR_VALID`

The shared runner defines over-acceptance as `prediction == "TRANSFER_VALID"`
and defines the `G2` denominator as the instances whose label is not
`TRANSFER_VALID`. Under a renamed token every FM50 instance would count as
blocked, both over-acceptance counters would be structurally pinned to zero, and
`G2_ANTI_PERMISSIVENESS` would print a denominator of 104 while being incapable
of firing — the precise defect class this programme exists to catch.
`FUNCTOR_VALID` is kept as a readable module alias and nothing else.

### Eligibility is a gate, not a filter

Categories are built as **concrete subcategories of FinSet**: objects carry
finite carriers, morphisms are functions between them, composition is function
composition. Associativity is therefore free, and eligibility turns entirely on
whether the proposed native vocabulary contains the identities and is closed
under composition — a property of the *proposal*, not of the checker.
`FiniteCategory.__post_init__` decides it exactly and raises when it fails.

* One proposal in four is emitted **without closing under composition**. Such a
  vocabulary does not form the required categorical structure, the composition
  table is incomplete, and the construction is `INELIGIBLE`.
* `INELIGIBLE` is a third outcome, not a rejection and not a negative result. It
  is counted per family and published in `generator_rejections` of every results
  and analysis file, next to the per-family eligible counts in the per-arm table.
* Every accepted instance additionally has two law-breaking perturbations of its
  own donor (a deleted composite, a rebound identity) pushed through the same
  checker in the same execution. A probe that is admitted is counted as
  `ELIGIBILITY_PROBE_MISSED`. The guard cannot become a checker that never runs.

## 3. Oracle and its independent cross-check

The constant functor `X ↦ o`, `f ↦ id_o` is a valid functor from any small
category into any non-empty one. "Does a valid functor exist" is therefore
trivially yes, and the minimum-violation profile over the whole functor space is
unstable across the identity, composition and distinction classes. The
disposition is consequently the exact status of the **registered candidate**,
and the exhaustive enumeration is carried as a cross-checked agreement field
that no arm ever sees.

* `oracle_exhaustive` — the claim's violation profile from this module's own
  law-by-law loop, and `n_valid_functors` by enumerating **every** object map
  and, for each, the complete endpoint-respecting morphism-map product. Identity
  morphisms are pinned by the identity law, which is definitional (a map that
  breaks it is not a functor), not a heuristic.
* `oracle_constraint_search` — the claim's violation profile from the reference
  module's `assess_functor` plus this module's distinction check, and
  `n_valid_functors` by a forward-checking backtracking search that charges each
  law the moment its members are assigned and **never materialises the map
  space**.

The two must agree on disposition, total violations, the full profile and
`n_valid_functors` for every instance of every split (`G0b`). The enumeration
cap is 24 000 maps per instance; a proposal above it is rejected and counted.

## 4. Arms, and why the comparator is the federation

| arm | role |
|---|---|
| `P0_NAME_SIMILARITY` | identifier correspondence, the "mere appearance" baseline |
| `P1_GRAPH_HOMOMORPHISM` | underlying-graph homomorphism: endpoints only |
| `P2_CATEGORY_LAW_FUNCTOR` | the category-law parent (`assess_functor`) |
| `P3_DIAGRAM_CHASE` | diagram chasing over the registered commuting diagrams |
| `P4_FAITHFULNESS` | faithfulness on the registered distinctions |
| `P5_FIXED_LESSON_INJECTION` | frozen one-lesson table |
| **`F0_PARENT_FEDERATION`** | **the primary comparator** |
| `M_F2_FUNCTORIAL_TRANSFER_FULL` | the ORION mechanic |
| four `M_MINUS_*` ablations, three controls | attribution and null calibration |

**No single parent owns the endpoint.** `P2` decides every functor law exactly
and is structurally blind to false equivalence, because collapsing two distinct
morphisms violates no functor law. `P4` owns exactly that stratum and is blind to
every law. `P1` cannot see composition at all — that is the gap between graph
theory and category theory. `P3` sees only the diagrams the claim wrote down and
never the unit laws. The strongest faithful comparator is therefore the
**federation** of `P2` and `P4` under a rule fixed before any outcome and blind
to it: `P2` decides the law question; if and only if `P2` finds every law
satisfied, `P4` is consulted and may veto the claim as a false equivalence.

`P3` is deliberately not a member. On this endpoint every registered diagram is
a composable pair of the donor's composition table and `P2` checks every such
pair, so diagram chasing is subsumed by the law parent. Recording that is a
finding about the parent landscape, not an omission.

### M is an independent implementation — and its limit is stated

`M` never calls `assess_functor` (the parent's call) and never calls the study's
own `claim_profile` (the oracle's). It rebuilds the donor's structural
description from `source_target` and `composition`, **discovers** the donor's
commuting triangles for itself instead of trusting the registered diagram list,
projects the claim through the target's composition index, runs native recovery
on the registered distinctions, and resolves the precedence itself.

That is an independent implementation, but it is **not an independent result**,
and the design says so before any outcome. Unlike FM10, where `M`'s anytime local
search could genuinely fail to reach the optimum the complete parent found,
FM50's law fragment is a *total function of the registered candidate*: any
correct implementation of the functor laws must agree with any other. `M` and
`P2` are therefore expected to be decision-identical by mathematics rather than
by shared code, and `G1a`'s zero is reported as such rather than as a
measurement of an alignment that could have diverged. The channels along which
`M` could still diverge are its own precedence resolution (the mixed class is a
design choice, not a forced one) and its discovered rather than registered
diagram set.

What carries `G1a` is therefore the **liveness control**: all four ablations are
known-different mechanics and each disagrees with the federation on the
development split, so the counter that reports zero for `M` is a counter that was
capable of reporting nonzero on that very split.

### Results that are definitional, and are labelled as such

* `P2` is exact on every law family and 0.00 on `FALSE_EQUIVALENCE` **by
  construction**; `P4` is its mirror image. Their informative content is that
  neither property alone reaches the endpoint.
* `C_ALWAYS_TRANSFER` is pinned at 3/8 = 0.375 on any balanced split because
  three of the eight families are registered `TRANSFER_VALID`. That is
  arithmetic, and it is what the 0.40 null-calibration ceiling was checked
  against **before** the generator was written.
* `SURFACE_NAME_DECOY` deranges the target's display names while leaving the
  registered candidate correct, so `P0` scoring 0.00 there is definitional.

## 5. Gates

`G0a` known answer (11 hand-authored fixtures, both oracles) · `G0b` oracle
self-agreement · `G0c` null calibration · `G0d` decoy coverage · `G0e` planted
positives (6) · `G0f` family discrimination (two halves, each with its own
denominator) · **`G0g` eligibility** · `G1a` parent reproduces M (with liveness
control) · `G1b` M advantage detector · `G2` anti-permissiveness · `G3`
mechanism by omission · Holm across the eight per-family paired tests.

### Two reporting rules, both learned from defects found on 2026-09-02

1. **Every gate reports the number of instances its rule was actually evaluated
   on.** A gate whose denominator is below its registered minimum returns
   `CANNOT_CHECK` and never `PASS`: "could not check" is never "checked and
   fine". `G0g` has an explicit `CANNOT_CHECK` test of its own — an eligibility
   gate handed an empty ledger must not report a pass.
2. **Every no-alarm assertion is paired with a planted positive that fires in the
   same execution.** Six are registered, including an all-ceiling arm table that
   must FAIL `G0f`, and a deliberately non-associative composition table that
   must be caught by the eligibility checker's associativity law and reported
   `INELIGIBLE` rather than scored as a negative result about any arm.

`G0g` carries both halves with their own denominators. Asserting only the alarm
half would leave a checker that cries wolf undetected; asserting only the
no-alarm half would leave a checker that never runs undetected.

## 6. Routes

`PARENT_SUFFICIENT` · `FM_RESIDUAL_CANDIDATE` · `M_OVER_ACCEPTS` ·
`CANNOT_CHECK`. The pre-registered expectation is `PARENT_SUFFICIENT`, and on
this endpoint more strongly than for FM10 for the reason given in §4. A residual
would require correspondingly hard scrutiny.

## 7. Sizes, seeds and execution

104 protected instances (8 families × 13; ≥ 96 required by issue #50 §C1), all
of them **eligible** — ineligible constructions are counted separately and are
not part of the split. 24 development; 16 selftest. Deterministic and
single-core; the whole development stage completes in well under a second.

Protected seed commitment (sha256 of the custody seed's stripped bytes):
`b45a1644e3219ce0cca4e3307dacc7c4c20e50833095fc4d1ed579fa3948fe46`, custody path
`~/.orion-custody/fm/FM50_PROTECTED_SEED_V1.txt`. Note the convention:
`fm_run.stage_protected` hashes `read_bytes().strip()`, so `sha256sum` on the
file — which includes the trailing newline — will not match.

One protected run, gated by a `PROTECTED_RUN_AUTHORIZATION.json` that carries a
human-written token, names `FM50`, and acknowledges this design JSON's sha256.
That file is absent from the repository and a unit test asserts it stays absent;
the protected stage refuses with exit 3 while it is.

## 8. Authority

This study grants no scientific truth, no F2 superiority, no field status and no
submission readiness. It is one exact known-answer measurement of one formal
transfer mechanic against the strongest faithful parents for that mechanic, and
`PARENT_SUFFICIENT` is a first-class successful terminal.
