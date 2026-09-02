# FM40 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Scope of this file:** FM40 only. It is a separate file from
`FM_PARENT_FIDELITY_RECEIPT_V1.md` (which covers FM10) so that sibling suites
landing in parallel do not contend for the same lines. Together they are the
place where a comparator earns the right to be used.

**Status:** development artifacts only. **No protected outcome has been generated
or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent, so
`fm_run.py FM40 protected` refuses (exit 3), asserted by
`tests/unit/test_fm_exact_suites.py::test_protected_stage_refuses_without_authorization`.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM40 selftest` then `dev`;
each completes in well under a second. Two consecutive runs produce
byte-identical results and custody files (asserted by
`test_development_split_is_deterministic`).

## 1. Frozen code and artifacts (sha256)

| file | sha256 |
|---|---|
| `fm_core.py` (unchanged) | `2b345a707d099e93a30d4b9431f206dd03c6f3fdad3edb85e3a175194e26a7ca` |
| `fm_run.py` (unchanged) | `058acc3350603dbe6a247fb8ec739335993b0a27a0fa008251b49a210138b4ec` |
| `fm40_suite.py` | `20eac1ceb747621445999bac10cbd90c01c975ef87bf97b184f520fb938b5728` |
| `FM40_..._DESIGN_V1.json` | `1802ac220e8f945847c21caa1c5c541b6d5ed8d8f2f901fd5482075b302acd0a` |
| `fm40/results/FM40_DEVELOPMENT_RESULTS_V1.json` | `7c3d608fe077d0ee2536ffc90bac0d5049b4173ee8f5d2c8166f5e2c35d47c50` |
| `fm40/results/FM40_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `b0003c9669914511757e0335a0ae818a22eafbcc5e0eb9e73fd7393a51590bb6` |
| `fm40/results/FM40_SELFTEST_REPORT.json` | `e85fa9f66bcd51ef2b1b88c972622baeb18fbe986bbfca3c4cdcbdcf00fa61c7` |

`fm_core.py` and `fm_run.py` hash exactly as they do in the FM10 receipt: the
shared harness was not edited for FM40, and `fm_run.SUITES` already carried the
`FM40 -> fm40_suite` entry.

FM40 protected seed commitment (sha256 of the custody seed file's bytes after
`strip()`, which is what `stage_protected` recomputes):
`7431279476019dd15235002757be9fe80f3ad739cfc7964abd7aca83eaa5b93a`.
A protected run additionally requires `acknowledged_design_sha256` to equal the
design-JSON hash above and `suite` to equal `FM40`.

## 2. FM40 parent fidelity: native known-answer tests (25/25 PASS)

Every comparator passed its own native tests before being used
(`fm40_suite.parent_fidelity`, executed by `selftest` and by the unit test).

| parent | tests (all PASS) |
|---|---|
| `GROUP_ACTION` (the model itself) | composition is a genuine left action, `act(compose(g,h),x) == act(g, act(h,x))` on every configuration in both orders; the site-`S3` × colour-swap group closes to order 12; every closure element is a permutation of the domain; Cayley saturation and breadth-first closure return the *same* element set; and invariance under the generators implies invariance under the whole closure — the subgroup theorem the second oracle algorithm rests on, checked rather than assumed |
| `P1_ORBIT_STABILISER` | cyclic rotation on three binary sites has exactly four orbits; the sorted colour histogram is constant on every orbit and is reported invariant; a site-indexed property is not constant on orbits and is reported broken; documented boundary recorded — orbit constancy decides invariance only, so an equivariant property is reported as broken |
| `P2_EQUIVARIANCE_SOLVER` | a colour permutation makes the colour histogram equivariant rather than broken; an invariant property is reported as such; a genuine break (colour count under a 3-colour swap) is reported as non-invariant; the solver reaches elements that are not generators (group order 6 on the equivariant hand case); documented boundary recorded — `P2` has no sub-regime and no surface encoding, so it flattens both of those strata to `BLOCK_NON_INVARIANT` |
| `P0_SURFACE_SYMMETRY_SCAN` | declares invariance from a symmetric re-description while the property itself breaks — the false-invariance behaviour the surface family exists to expose; declares non-invariance when the encoding itself moves |
| `P3_AUGMENTATION_EMPIRICAL` | exact on the witnessed subgroup; documented boundary recorded — it reports invariance on an instance the exhaustive oracle blocks, because the breaking element is not among the witnessed transformations. Measured symmetry is symmetry under the augmentations you actually have |
| `P4_REGIME_RESTRICTION` | finds the registered sub-regime on which the property is invariant; declines when the declaration covers the whole domain; documented boundary recorded — no value-space action, so an equivariant property is reported as broken |
| `P5_FIXED_LESSON_TABLE` | reproduces the frozen lesson for a covered property; documented boundary recorded — the same property under a site-only group is genuinely invariant while the name-keyed table still answers "equivariant", because a table cannot see which group is acting |
| `ORACLE_CROSS_THEOREM` | the block-system criterion and the pointwise-relation criterion agree on all seven hand-built instances spanning every stratum |
| `REFERENCE_MODULE` (`orion_v2.transfer_formal_mechanics`) | `assess_invariance` agrees with the suite's own invariance primitive on a materialised group element |

Six boundaries are recorded as **scope notes rather than defects**, because they
are what makes the federation the honest comparator: `P1` cannot see a value-space
action; `P2` cannot see the regime or surface strata; `P0` is exact about the
encoding and silent about the property; `P3` is exact about the witnessed
subgroup and blind outside it; `P4` has no value action; `P5` has no group. None
is a strawman; each is complete within its own competence, and each is the way
the mature owner of that competence actually works.

## 3. Known-answer fixtures (G0a): 11/11, no hand-authoring correction needed

All eleven hand-authored fixtures are reproduced by the exhaustive
element-closure oracle and by the independent generator-block cross-check, at
first authoring. They span every disposition and pin the two order-sensitive
decisions:

| fixture | pins |
|---|---|
| `KA-01` … `KA-03`, `KA-09` | invariance under a mixed group, equivariance of the colour histogram, a site-indexed break, and invariance of the histogram under a **site-only** group (the same property, a different group, a different answer) |
| `KA-04` | the surface-only class: a broken property whose break is invisible in a `G`-invariant re-description |
| `KA-05`, `KA-11` | regime-bounded invariance, on the constants class of a 3-site domain and on the `(1,3)` histogram class of a 4-site domain |
| `KA-06` | **the registered classification order**: an actionable sub-regime dominates the surface-only diagnosis when both hold |
| `KA-07`, `KA-08` | unseen transformations: the witnessed subgroup fixes the property, and the full group breaks it (`KA-07`) or only covaries with it (`KA-08`) |
| `KA-10` | majority colour with a tie sentinel is equivariant under a colour permutation |

## 3a. Independence of the mechanic from its own comparator

FM10's blocking defect was an `M` that issued the same calls as `F0`, which made
`G1a`'s decision identity an **algebraic identity rather than a measurement**.
FM40's `M` calls no parent, no federation and no oracle function:

- it closes the group by **Cayley saturation**, not breadth-first frontier
  expansion (both routes are separately verified to agree in `parent_fidelity`);
- it tests invariance by **set-image fixation of the level-set partition**, not
  pointwise on values;
- it discovers the value action by **bounded sampling with exhaustive
  verification** through `orion_v2.transfer_formal_mechanics.assess_invariance`,
  not by direct construction;
- it **discovers** the maximal orbit-union on which the property is constant
  before comparing the registered declaration against it.

That discovery step is sound but not complete. **The divergence is demonstrated,
not asserted:** planted positive
`G1a_PARENT_REPRODUCES_M / mechanic_can_diverge_from_its_own_comparator` runs
`M`'s own pipeline with a shortened sample schedule on the equivariant fixture
and shows it returning a *different* disposition from the federation, in the same
execution that reports the study's zeros. The decision-identity counter therefore
has a subject that can move. At the registered schedule the final stratified
round represents every property value, so `M` and `F0` are expected to coincide
**by mathematics rather than by shared code**, and that coincidence is what the
run measures.

`G1a` also carries the shared **liveness control**: on the development split the
discordance counter registers 12 (`M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE`), 6
(`M_MINUS_EQUIVARIANCE_TEST`), 3 (`M_MINUS_REGIME_RESTRICTION`) and 3
(`M_MINUS_SURFACE_AUDIT`) disagreements with the parent, so the zero it reports
for `M` is a zero the counter was capable of not reporting. No ablation is dead.

## 3b. Four results that are definitional, and are labelled as such

- **`F0_PARENT_FEDERATION` is exact by composition.** Each of its three
  sub-decisions is a complete procedure for its own stratum, and the
  pre-registered combination rule reproduces the registered classification order.
  Its 1.000 is a statement about the stratification, not a horse-race win.
- **`P2_EQUIVARIANCE_SOLVER` is the first oracle algorithm minus the regime and
  surface strata**, so its 1.00 on the invariance/equivariance families and 0.00
  on the regime and surface families are both by construction. A group-element
  solver genuinely *is* the mature parent for that question, which is why the arm
  is kept, but its row is not independent parent evidence.
- **`SURFACE_ONLY_SYMMETRY` instances carry an always-invariant surface
  encoding**, so `P0` scoring 0.00 there is definitional. The informative number
  is its over-acceptance count (11 of 21) — what false invariance costs.
- **`UNSEEN_TRANSFORMATION_*` instances are rejected unless the witnessed
  subgroup is proper and fixes the property**, so `P3` scoring 0.00 there is
  definitional too (9 over-accepts). Rejection counts are published per family
  and reason.

## 4. Planted positives (G0e): 6/6 fire

Registered trip-wires, all executed in the same run that reports the study's
zeros:

| gate | planted case | fires |
|---|---|---|
| `G0b_ORACLE_SELF_AGREEMENT` | a deliberately incomplete oracle that classifies using only the *witnessed* transformations, on an instance whose break lives outside the witnessed subgroup | yes |
| `G0a_KNOWN_ANSWER` | a deliberately wrong expected disposition | yes |
| `G2_ANTI_PERMISSIVENESS` | `C_ALWAYS_INVARIANT` on an instance the oracle blocks — a false-invariance claim, counted | yes |
| `G0f_FAMILY_DISCRIMINATION` | a synthetic per-arm table in which every arm scores 1.000 must **FAIL** the gate. This is the exact shape of the FM/FG R2 `fm40` cell | yes |
| `G3_MECHANISM_BY_OMISSION` | `M_MINUS_SURFACE_AUDIT` must be wrong on a surface-only instance where `M` is right | yes |
| `G1a_PARENT_REPRODUCES_M` | `M`'s own pipeline under a shortened sample schedule must return a different disposition from `F0` | yes |

## 5. FM40 development split (21 instances, 3 per family — DEVELOPMENT, not protected)

| arm | exact | rate | over-accept (false invariance) | under-accept |
|---|---|---|---|---|
| `P0_SURFACE_SYMMETRY_SCAN` | 8/21 | 0.381 | 11 | 1 |
| `P1_ORBIT_STABILISER` | 9/21 | 0.429 | 0 | 0 |
| `P2_EQUIVARIANCE_SOLVER` | 15/21 | 0.714 | 0 | 0 |
| `P3_AUGMENTATION_EMPIRICAL` | 6/21 | 0.286 | 9 | 0 |
| `P4_REGIME_RESTRICTION` | 12/21 | 0.571 | 0 | 0 |
| `P5_FIXED_LESSON_TABLE` | 11/21 | 0.524 | 0 | 2 |
| **`F0_PARENT_FEDERATION`** | **21/21** | **1.000** | 0 | 0 |
| **`M_F2_INVARIANCE_DISCOVERY_FULL`** | **21/21** | **1.000** | 0 | 0 |
| `M_MINUS_EQUIVARIANCE_TEST` | 15/21 | 0.714 | 0 | 0 |
| `M_MINUS_UNSEEN_TRANSFORMATION_CLOSURE` | 9/21 | 0.429 | 9 | 0 |
| `M_MINUS_REGIME_RESTRICTION` | 18/21 | 0.857 | 0 | 0 |
| `M_MINUS_SURFACE_AUDIT` | 18/21 | 0.857 | 0 | 0 |
| `C_ALWAYS_INVARIANT` | 3/21 | 0.143 | 18 | 0 |
| `C_ALWAYS_NON_INVARIANT` | 6/21 | 0.286 | 0 | 3 |
| `C_RANDOM_DISPOSITION` | 4/21 | 0.190 | 1 | 1 |

Every arm is separated: the spread runs 0.143 to 1.000 and no arm ties the
mechanic. **No ablation is dead** — the weakest separation is 3 instances
(`M_MINUS_REGIME_RESTRICTION`, `M_MINUS_SURFACE_AUDIT`), which is exactly the
size of their target families on a 3-per-family split. Exact per-family and
per-arm numbers are in `fm40/results/FM40_DEVELOPMENT_ANALYSIS_V1.{json,md}`; the
table above is a summary and the JSON is authoritative.

### 5.1 Development gate block

| gate | verdict | evaluated |
|---|---|---|
| `G0a_KNOWN_ANSWER` | PASS | 11 fixtures |
| `G0b_ORACLE_SELF_AGREEMENT` | PASS | 21 instances |
| `G0c_NULL_CALIBRATION` | PASS | 4 checks |
| `G0d_DECOY_COVERAGE` | PASS | 4 decoy families |
| `G0e_PLANTED_POSITIVES` | PASS | 6 trip-wires |
| `G0f_FAMILY_DISCRIMINATION` | PASS | 2 halves |
| `G1a_PARENT_REPRODUCES_M` | PASS | 21 instances (identity 1.000) |
| `G1b_M_ADVANTAGE` | NOT_FIRED | 21 instances, 0 discordant pairs |
| `G2_ANTI_PERMISSIVENESS` | PASS | 18 oracle-blocked instances |
| `G3_MECHANISM_BY_OMISSION` | NOT_APPLICABLE | no claimed advantage |

Every verdict is printed with the number of instances its rule was actually
evaluated on. Holm across the seven per-family paired tests: all raw and adjusted
p = 1.000 (no discordant pair anywhere). On development this predicts the
pre-registered route **`PARENT_SUFFICIENT`**.

Cost flag: `COST_ADVANTAGE_PARENT` (M 10.2 ms, F0 0.8 ms over 21 instances). The
mechanic is roughly 13× the federation's wall time because sampled-then-verified
value-action discovery pays exhaustive verification per group element where the
solver constructs the relation once. This is reported and routes nothing.

### 5.2 Reading (development only; nothing here is protected evidence)

No single parent reaches the endpoint, and each fails in the direction its own
competence predicts. The orbit/stabiliser parent is exact wherever the question
is invariance and collapses everywhere a value-space action or a sub-regime
matters. The equivariance solver adds that stratum and stops at 0.714 because it
has no regime and no surface encoding. The empirical augmentation parent is the
weakest arm at 0.286 and its errors are almost all **over-acceptance** (9 of 15):
declaring invariance from the transformations it happened to witness is exactly
the false-invariance failure the protocol names. Their pre-registered federation
is exact, and the ORION mechanic is decision-identical to it.

If this holds on the protected split, FM40's content is an attribution — *which*
parent family owns *which* stratum of an invariance claim — plus the finding that
ORION's invariance/equivariance discovery loop is the composition of three mature
parents under a fixed rule and nothing more.

Ablations behave as their omissions predict, and their scopes differ in a way
worth recording. Removing the value-action test loses exactly the two
equivariance families (1.00 everywhere else). Removing regime recovery loses
exactly the regime family, and removing the surface audit loses exactly the
surface family. Removing the closure to unseen transformations is **not**
family-local: it loses both `UNSEEN_*` families outright and also degrades
`NON_INVARIANT` (0.00) and `PARTIAL_REGIME_INVARIANCE` (0.33), because
restricting the pipeline to the witnessed subgroup weakens every family whose
breaking element happens to lie outside it. Its 9 over-acceptances are the same
failure mode as `P3`'s. These are properties of the stratified composition, and
they are load-bearing for `F0` exactly as much as for `M`.

Generator rejections (development): 19 across 21 accepted instances, published
per `family|reason`. The largest single reason is
`NON_INVARIANT|surface_encoding_invariant_would_collapse_the_family` (8): a
randomly drawn surface encoding is often `G`-invariant, which would have turned a
`NON_INVARIANT` instance into a `SURFACE_ONLY_SYMMETRY` one. Rejecting those is
what keeps the two families disjoint, and the count is published rather than
hidden.

## 6. Estimated protected-run cost

126 instances × 15 arms, deterministic, single core: a same-size probe (18 per
family, development seed — **not** the protected seed) completed generation,
dispatch, scoring and gating in **0.23 s** wall, with 162 rejections, and
reproduced every development finding at scale (F0 and M both 1.000; P2 0.714; P5
0.563; P0 0.381; P3 0.286; the random control 0.214). Budget: 1 CPU-minute. Runs
on the Mac; no CI on the Mac mini, and no cluster time is needed.
