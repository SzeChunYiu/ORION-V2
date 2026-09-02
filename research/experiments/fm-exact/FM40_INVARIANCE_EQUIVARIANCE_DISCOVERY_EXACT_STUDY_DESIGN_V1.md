# FM40 — Invariance/Equivariance Discovery: Exact Known-Answer Study Design (V1)

**Lane:** FM40, L4 formal transfer mechanics (issues #48, #50 §C1).
**Status:** frozen prospective design. No protected outcome has been generated or inspected.
**Machine-readable companion:** `FM40_INVARIANCE_EQUIVARIANCE_DISCOVERY_EXACT_STUDY_DESIGN_V1.json`.
**House style:** `research/experiments/me-x1`, `me-x2`, `me-x4`, and the FM10 exemplar
in this directory — exact generator, exhaustive oracle cross-checked by an
independent algorithm, seed commitment in operator custody, development split
separate from protected.

## 1. Why this suite exists, given FM/FG R2

The FM/FG R2 registered-scale campaign (2026-08-30,
`research/experiments/fmfg-r2/`) already dispatched a *model-arm* version of
FM40 at registered counts. Its own receipt records the outcome: **`fm40` scored
1.000 for all five arms** at n120. A comparison in which every arm is perfect
could not have detected a difference had one existed; it is a ceiling family, not
a null result.

FM40 here is the *exact algorithmic* study the backlog actually asks for: real
parent implementations rather than model prompts, an exhaustive oracle, and — as
a first-class hard gate — a **non-degeneracy requirement** (`G0f`) that fails the
run if the task family cannot separate a registered weak arm from the strongest
parent. On the development split the arms span 0.286 to 1.000, so the ceiling
defect that made R2 uninformative is now a gate rather than a footnote.

## 2. Task and endpoint

Each instance is a finite domain `X` of configurations, a finite group `G`
acting on it, a candidate property `p`, a registered surface re-description `e`,
a declared sub-regime, and a published set of witnessed transformations. The
registered question is a **transfer disposition with an exact obstruction
stratum**, not "is `p` invariant":

| disposition | meaning |
|---|---|
| `TRANSFER_VALID` | `p` is invariant under the **whole** group; the donor's claim transfers unrestricted |
| `BLOCK_EQUIVARIANT_NOT_INVARIANT` | `p` is not preserved pointwise but covaries: a value-space action `rho` exists with `p(g.x) = rho(g)(p(x))` for every `g` and `x`, so the transformation must be carried along with the claim |
| `BLOCK_REGIME_BOUNDED_INVARIANT` | some element genuinely breaks `p`, but `p` is invariant on the registered proper, `G`-stable sub-regime |
| `BLOCK_SURFACE_SYMMETRY_ONLY` | `p` is broken and the break is invisible in the registered surface encoding: the symmetry present is a symmetry of the re-description, not of the property |
| `BLOCK_NON_INVARIANT` | `p` is broken, the break is visible at the surface, and no regime rescues it |

**Invariance testing is deliberately not the endpoint.** Checking `p` against a
supplied generating set is a two-line computation, so a study built on it would
report parent sufficiency *by construction* rather than by measurement. Four
things are added instead: a value-space action that must be **discovered**, a
registered sub-regime stratum, a surface-encoding stratum, and unseen
transformations that a witnessed subgroup cannot reach.

### `TRANSFER_VALID` is a deliberate name, not an inherited one

The shared runner's over-acceptance counter and the `G2` anti-permissiveness gate
are keyed on the literal string `TRANSFER_VALID`. FM40's unrestricted-transfer
disposition therefore carries that name, and it means exactly
*invariant-under-the-whole-group*. The consequence is the point: **`G2` becomes
FM40's false-invariance gate** — a registered primary of the protocol — evaluated
over the oracle-blocked instances (108 of 126 at protected size). Had the
disposition been named anything else, `blocked_idx` would have been every
instance, `M_over_accept` and `P_over_accept` would have been identically zero,
and `G2` would have printed a full denominator over an effective denominator of
zero: the mirror form of the defect FM10 was rewritten to avoid.

### The model

`X` is every colouring of `m` sites with `q` colours, for registered shapes
`(m,q)` in `{(3,2), (3,3), (4,2)}`, so `8 <= |X| <= 27`. `G` is a subgroup of
`S_m x S_q` acting by `(sigma,tau).x = y` with `y[sigma(i)] = tau(x[i])`,
published as a **generating set** and closed by the study under a registered cap
of 64 elements. Properties, surface encodings and regime tags all come from one
registered vocabulary of finite-valued functions on `X` (sorted colour histogram,
colour histogram, number of distinct colours, constancy, adjacent-equal count,
majority colour with a tie sentinel, colour at a site, count/parity of a colour,
equality of a site pair). The sub-regime is the preimage of a declared set of tag
values, and its properness and `G`-stability are verified **exhaustively** — the
tag being `G`-invariant is not accepted as an argument for stability.

Classification order is registered and frozen: invariance dominates equivariance;
a genuine break is rescued first by the sub-regime (an actionable positive:
transfer *is* valid inside it), then diagnosed as surface-only (a warning), and
otherwise reported flatly. Fixture `KA-06` pins the regime-over-surface
precedence.

## 3. Oracle and its independent cross-check

The two algorithms rest on **different theorems** and touch different objects.

`oracle_element_closure` materialises the whole group by breadth-first frontier
expansion and classifies every element pointwise by the relation
`R_g = {(p(x), p(g.x))}`: `FIXING` when `R_g` is the identity, `COVARIANT` when it
is a well-defined injection on values (which is exactly a value-space action),
`BREAKING` otherwise.

`oracle_generator_blocks` **never materialises the group**. The stabiliser of `p`
and the set of block-preserving elements are both subgroups of `G`, so a set that
generates `G` decides both questions; each generator is decided by set-image
block-system tests on the level-set partition, and orbits come from union-find
over generator images. A wrong closure in the first algorithm, or a misapplied
subgroup argument in the second, makes them disagree.

They must agree on the disposition and on every stratum field — invariance,
equivariance, regime-bounded invariance, surface invariance, invariance under the
witnessed subgroup, orbit count and property-value count — for **every** instance
of every split (`G0b`).

### The generator proposes; the oracle labels

An instance whose exhaustive disposition is not in its family's registered set,
or on which the two algorithms disagree, is rejected and resampled. Four further
structural preconditions that the oracle does not itself express are checked
explicitly, because the oracle would not catch them:

1. in both `UNSEEN_TRANSFORMATION_*` families the witnessed subgroup must be a
   **proper** subgroup of `G` and must **fix** the property, verified by closing
   both;
2. in the two families whose registered answer is `BLOCK_NON_INVARIANT` the
   surface encoding must **not** be `G`-invariant, so they cannot collapse into
   the surface class;
3. the surface encoding must be a different function from the property (a
   re-description, not a copy);
4. the group must be non-trivial and the property non-degenerate.

Rejections are counted under `family|reason` keys, published in every results
file, and sum to the true rejection total. On the development split there were 19
rejections across 21 accepted instances, concentrated in `NON_INVARIANT` where a
randomly drawn surface encoding is often `G`-invariant and would have collapsed
the family.

## 4. Arms, and why the comparator is the federation

| arm | kind | fidelity |
|---|---|---|
| `P0_SURFACE_SYMMETRY_SCAN` | parent | feature-level symmetry screen: exact about the *encoding*, silent about the property |
| `P1_ORBIT_STABILISER` | parent | orbit/stabiliser computation — how computational group theory decides invariance |
| `P2_EQUIVARIANCE_SOLVER` | parent | value-space action solver over the materialised group |
| `P3_AUGMENTATION_EMPIRICAL` | parent | empirical symmetry detection from witnessed transformations, the standard applied practice |
| `P4_REGIME_RESTRICTION` | parent | properness, `G`-stability and restricted invariance of the registered declaration |
| `P5_FIXED_LESSON_TABLE` | parent | the protocol's frozen-lesson-table baseline |
| `F0_PARENT_FEDERATION` | federation | **primary comparator** |
| `M_F2_INVARIANCE_DISCOVERY_FULL` | mechanic | ORION L2 invariance/equivariance discovery |
| four `M_MINUS_*` ablations | ablation | equivariance test / unseen-transformation closure / regime restriction / surface audit |
| three `C_*` controls | control | always-invariant, always-non-invariant, random |

**No single parent owns the endpoint.** `P1` is exact on invariance and has no
notion of an action on the value space. `P2` owns the invariance/equivariance
stratum and knows nothing about sub-regimes or surface encodings. `P3` is exact
on the witnessed subgroup and structurally blind outside it. `P5` cannot see
which group is acting. The strongest faithful comparator is therefore their
federation under a rule fixed before any outcome and blind to it: *`P2` decides
the invariance/equivariance stratum; only on an outright break is `P4` consulted;
only when `P4` declines is `P0` consulted, and its invariant verdict on a broken
property is precisely the surface-only diagnosis.* No parent is used outside its
native competence and none ever sees the oracle.

Every parent passes its own native known-answer tests before it is used as a
comparator; see `FM_PARENT_FIDELITY_RECEIPT_FM40_V1.md` (25/25 for FM40).

### M is an independent implementation, and its divergence is demonstrated

`M` calls no parent, no federation and no oracle function. It closes the group by
**Cayley saturation** rather than breadth-first frontier expansion; it tests
invariance by **set-image fixation of the level-set partition** rather than
pointwise on values; it discovers the value action by **bounded sampling with
exhaustive verification** through
`orion_v2.transfer_formal_mechanics.assess_invariance` rather than by direct
construction; and it **discovers** the maximal orbit-union on which the property
is constant before comparing the registered declaration against it.

That discovery step is sound but **not complete**: a candidate `rho` built from a
bounded sample and refuted by exhaustive verification is discarded, and if the
schedule runs out the element is reported as breaking. A registered planted
positive runs `M`'s own pipeline with a shortened schedule and shows it returning
a **different disposition from the federation** — so the decision-identity
counter has a subject that can move, and this is shown rather than asserted. At
the registered schedule the final stratified round represents every property
value, so `M` and `F0` are expected to coincide *by mathematics rather than by
shared code*, and that coincidence is what the run measures.

`G1a` additionally carries the shared **liveness control**: at least one ablation
arm must register discordance against the parent on the same split. On
development all four do (12, 6, 3, 3).

### Four results that are definitional, and are labelled as such

- `F0_PARENT_FEDERATION` is exact **by composition**: each sub-decision is a
  complete procedure for its own stratum and the combination rule reproduces the
  registered classification order. Its 1.000 is a statement about the
  stratification, not a horse-race win.
- `P2_EQUIVARIANCE_SOLVER` is the first oracle algorithm's element classification
  minus the regime and surface strata, so its 1.00 on the invariance/equivariance
  families and 0.00 on the regime and surface families are by construction. Its
  row is not independent parent evidence.
- `SURFACE_ONLY_SYMMETRY` instances carry a surface encoding drawn from the
  always-invariant vocabulary, so `P0` scoring 0.00 there is definitional. The
  informative number is its **over-acceptance count**: what false invariance
  costs.
- `UNSEEN_TRANSFORMATION_*` instances are rejected unless the witnessed subgroup
  is proper and fixes the property, so `P3` scoring 0.00 there is definitional
  too.

## 5. Gates

All gates are frozen here, before protected outcome access.

| gate | rule | hard |
|---|---|---|
| `G0a_KNOWN_ANSWER` | every hand-authored fixture's disposition reproduced by the oracle (≥ 8 required; 11 registered) | yes |
| `G0b_ORACLE_SELF_AGREEMENT` | the two independent oracle algorithms agree on every instance | yes |
| `G0c_NULL_CALIBRATION` | constant arms ≤ 0.40, random ≤ 0.40, M against within-split shuffled oracle labels ≤ 0.40 | yes |
| `G0d_DECOY_COVERAGE` | each registered decoy family carries ≥ 3 instances | yes |
| `G0e_PLANTED_POSITIVES` | every registered planted positive trips its own gate predicate (≥ 3; 6 registered) | yes |
| `G0f_FAMILY_DISCRIMINATION` | two halves, each with its own denominator: *solvable* (some non-control arm ≥ 0.95) **and** *separating* (some registered weak arm ≤ 0.85) | yes |
| `G1a_PARENT_REPRODUCES_M` | F0 reproduces M on ≥ 99.5% of instances, no family > 5% discordant, **and** the counter is shown live by ≥ 1 ablation disagreeing with the parent | yes |
| `G1b_M_ADVANTAGE` | detector: paired diff > 0, exact two-sided p ≤ 0.05, ≥ 1 family with ≥ 5 M-only-exact | no |
| `G2_ANTI_PERMISSIVENESS` | **false-invariance gate**: on oracle-blocked instances, M claims unrestricted invariance no more often than F0 (≥ 10 blocked) | yes |
| `G3_MECHANISM_BY_OMISSION` | if G1b fires: the matching omission ablation's rate ≤ the parent's on that family | no |

Multiplicity: Holm across the seven per-family paired tests, reported for every
run.

### Two reporting rules, both inherited from defects found on 2026-09-02

1. **Every gate publishes its own denominator.** A gate whose denominator is
   below its registered minimum returns `CANNOT_CHECK` — never `PASS`. "Could not
   check" is never "checked and fine".
2. **Every no-alarm assertion is paired with a planted positive.** Six trip-wires
   are registered for FM40 and must all fire in the same execution that reports
   the study's zeros: a witnessed-only pseudo-oracle must be caught by `G0b`'s
   predicate; a deliberately wrong expected label by `G0a`'s; the over-acceptance
   counter must count `C_ALWAYS_INVARIANT` on a blocked instance; a synthetic
   all-ceiling arm table must **fail** `G0f` (the exact shape of the R2 fm40
   cell); `M_MINUS_SURFACE_AUDIT` must be wrong where `M` is right; and `M` under
   a shortened sample schedule must **disagree with `F0`**, which is what makes
   `G1a` a measurement.

## 6. Routes

`PARENT_SUFFICIENT` is a first-class successful terminal, and it is the
pre-registered expectation: three sibling exact studies (ME-X1, ME-X2, ME-X4) have
already found the strongest faithful parent sufficient. A residual
(`FM_RESIDUAL_CANDIDATE`) requires G1b to fire, G2 to hold and G3 to attribute the
advantage to a named omission — and would deserve correspondingly hard scrutiny.
`M_OVER_ACCEPTS` and `CANNOT_CHECK` are the remaining terminals.

## 7. Sizes, seeds and execution

126 protected instances (18 per family × 7 families ≥ the 120 required by issue
#50 §C1); 21 development; 14 selftest. Deterministic and single-core; a same-size
probe completed generation, dispatch, scoring and gating in **0.23 s** wall on the
Mac.

Protected seed commitment, frozen here:
`7431279476019dd15235002757be9fe80f3ad739cfc7964abd7aca83eaa5b93a`
(sha256 of the stripped bytes of the seed file held at
`~/.orion-custody/fm/FM40_PROTECTED_SEED_V1.txt`, which is exactly what
`fm_run.stage_protected` recomputes). Development and selftest seeds are public
(`FM40-DEV-20260902`, `FM40-SELFTEST`).

`fm_run.py FM40 protected` refuses (exit 3/4) unless a human-written
`PROTECTED_RUN_AUTHORIZATION.json` is present, names this suite, and carries this
file's sha256; and unless the custody seed hashes to the commitment above.
Exactly one protected run and one analysis are permitted. No design constant,
gate, arm, oracle rule or seed may change after outcome access; a legitimate
repair gets a new prospective identity.

## 8. Authority

This design grants no scientific truth, no F2 superiority, no field status and no
submission readiness. A formal witness does not establish empirical truth.
