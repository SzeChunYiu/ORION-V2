# FM50 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Scope:** FM50 only. FM10's receipt (`FM_PARENT_FIDELITY_RECEIPT_V1.md`) is not
edited by this PR; each suite carries its own file so that concurrent suites do
not contend for one document.

**Status:** development artifacts only. **No protected outcome has been
generated or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent, so
`fm_run.py FM50 protected` refuses (exit 3), asserted by
`tests/unit/test_fm_exact_suites.py::test_protected_stage_refuses_without_authorization`.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM50 selftest` then `dev`;
the pair completes in about 0.2 s. Two consecutive runs produce byte-identical
results and custody files (asserted by `test_development_split_is_deterministic`).

**Shared harness untouched.** `fm_core.py` and `fm50`'s `fm_run.py` hash to
exactly the values FM10's receipt published, which is the check that this suite
added no gate, loosened no threshold and changed no scoring rule for anyone else.
The `SUITES` dict already carried the `FM50` entry, so `fm_run.py` needed no edit
at all.

## 1. Frozen code and artifacts (sha256)

| file | sha256 |
|---|---|
| `fm_core.py` | `2b345a707d099e93a30d4b9431f206dd03c6f3fdad3edb85e3a175194e26a7ca` |
| `fm_run.py` | `058acc3350603dbe6a247fb8ec739335993b0a27a0fa008251b49a210138b4ec` |
| `fm50_suite.py` | `c485034f4904653e15102809588f850381c8b007de5363e652bb7830b78d262b` |
| `FM50_..._DESIGN_V1.json` | `3d647d0b028327df127bd7fdd45fbc9dfd38409f2148a236f543135a1015b387` |
| `fm50/results/FM50_DEVELOPMENT_RESULTS_V1.json` | `ed6b1faa8e4f756499bc31545b9c8a694e544a234959afd06fb965a3b69d5bec` |
| `fm50/results/FM50_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `8cd3f791851e09baa4113969cb0b5baddd366ef5dcd27ca7e6322bc06595e4f5` |
| `fm50/results/FM50_SELFTEST_REPORT.json` | `6f305144ea31ba51a63960255a3f13d1d898ff835d05dcc991f1c246d5a48e7d` |

FM50 protected seed commitment (sha256 of the custody seed's **stripped** bytes,
which is what `fm_run.stage_protected` hashes — `sha256sum` on the file includes
the trailing newline and will not match):
`b45a1644e3219ce0cca4e3307dacc7c4c20e50833095fc4d1ed579fa3948fe46`.
A protected run additionally requires `acknowledged_design_sha256` to equal the
design-JSON hash above and `suite` to equal `FM50`.

## 2. Parent fidelity: native known-answer tests (28/28 PASS)

**22 comparator tests across six parents and the reference module, plus 6
eligibility-gate tests.** The two counts are reported separately on purpose: gate
tests are not evidence that a comparator earned its place, and folding them in
would inflate the number that is.

| parent | tests (all PASS) |
|---|---|
| `P2_CATEGORY_LAW_FUNCTOR` (`assess_functor`) — 6 | the identity functor is valid; an endpoint violation is reported as such; **the classic non-functor** — a candidate that preserves objects and endpoints but breaks composition — is caught; a unit-law violation is caught; a simultaneous unit and composition failure is reported as mixed rather than as either half; documented boundary recorded — it is structurally blind to false equivalence, because the constant functor satisfies every functor law |
| `P3_DIAGRAM_CHASE` — 3 | a commuting diagram whose image commutes is accepted; a registered diagram that fails to commute is caught; documented boundary recorded — the unit laws are not among the diagrams a claim writes down, so an identity violation passes it |
| `P4_FAITHFULNESS` — 3 | a collapsed registered distinction is blocked; separated distinctions license a collapse elsewhere; documented boundary recorded — it performs no law checking at all |
| `P1_GRAPH_HOMOMORPHISM` — 3 | accepts a morphism of the underlying graphs; rejects an image with the wrong endpoints; documented boundary recorded — composition is invisible to a graph map, which is exactly the gap between graph theory and category theory |
| `P0_NAME_SIMILARITY` — 2 | prefers the name-similar object and so fails the decoy (the behaviour surface decoys exist to expose); accepts when the names line up with the registered candidate |
| `P5_FIXED_LESSON_INJECTION` — 2 | blocks when the one frozen lesson is violated; transfers whenever the frozen lesson is satisfied, composition unexamined |
| `REFERENCE_MODULE` (`orion_v2.transfer_formal_mechanics`) — 3 | `assess_functor` agrees with this module's own law loop on a mixed-obstruction instance; `FiniteCategory` admits a closed concrete construction; `FiniteCategory` rejects a non-associative composition table, and the raised message is matched against `associativity` specifically rather than against `ValueError` |

Four boundaries are recorded as scope notes rather than defects, because they are
what makes the federation the honest comparator: `P2` cannot see a collapsed
distinction, `P4` cannot check a law, `P1` cannot see composition, `P3` cannot
see the unit laws. None is a strawman; each is complete within its own competence.

### 2a. Eligibility gate `G0g` (6 tests, PASS on 25 evaluated constructions)

| test | result |
|---|---|
| 9 lawful constructions are admitted | PASS |
| 16 law-breaking constructions are caught | PASS |
| a non-associative composition table is caught **by the associativity law** (message matched, not just `ValueError`) | PASS |
| a deleted composite is caught by the completeness law | PASS |
| a rebound identity is caught by the identity laws | PASS |
| an eligibility gate handed an empty ledger reports `CANNOT_CHECK`, never `PASS` | PASS |

The audit carries both directions with their own denominators. Asserting only
the alarm half would leave a checker that cries wolf undetected; asserting only
the no-alarm half would leave a checker that never runs undetected. One further
precision was added during development and is recorded here: a generator set that
happens to *already* be closed under composition genuinely is a category, so
admitting it is the correct verdict — it is counted on the lawful side, not as a
law-breaking probe that fired. "Did not need to fire" is never recorded as "fired
correctly".

## 3. Known-answer fixtures (G0a): 11/11, no hand-authoring correction needed

All eleven hand-authored fixtures are reproduced by the exhaustive oracle and by
the independent constraint-search cross-check, on disposition, total violations,
the full profile and the exhaustively determined valid-functor count. Unlike
FM10, no fixture had to be rebuilt: the disposition here is a total function of
the registered candidate, so a hand-written expectation cannot be undercut by a
cheaper map the author did not consider.

Three fixtures exist only to pin the registered precedence — `KA-06` (a
simultaneous unit and composition failure is *mixed*), `KA-09` (an endpoint
violation dominates a collapse) and `KA-10` (a composition failure dominates a
collapse). `KA-07` pins the fact that the constant functor into the terminal
category is a **valid functor** that is nonetheless a false equivalence, which is
the whole reason `P2` alone cannot reach the endpoint.

## 4. Eligibility ledger, development split (per family)

Eligible instances are the split; ineligible constructions are counted and
published and are **never** scored as a negative result about any arm.

| family | eligible | INELIGIBLE (not a category) | rejected (family not realised) | eligibility probes missed |
|---|---|---|---|---|
| `VALID_FUNCTOR` | 3 | 0 | 0 | 0 |
| `SURFACE_NAME_DECOY` | 3 | 0 | 1 | 0 |
| `LICENSED_COLLAPSE` | 3 | 0 | 3 | 0 |
| `ENDPOINT_VIOLATION` | 3 | 1 | 0 | 0 |
| `IDENTITY_NOT_PRESERVED` | 3 | 2 | 0 | 0 |
| `COMPOSITION_NOT_PRESERVED` | 3 | 0 | 4 | 0 |
| `MIXED_LAW_OBSTRUCTION` | 3 | 0 | 2 | 0 |
| `FALSE_EQUIVALENCE` | 3 | 2 | 5 | 0 |
| **total** | **24** | **5** | **15** | **0 of 48 probes** |

The 15 rejections are proposals that were well-formed categories but did not
realise the family the generator intended — the oracle, not the generator,
decides, and `test_generated_family_intent_is_verified_not_assumed` asserts it.
The 48 probes are the two law-breaking perturbations (a deleted composite, a
rebound identity) pushed through the eligibility checker for each of the 24
accepted instances, in the same execution that reports the zero.

## 5. Development split (24 instances, 3 per family — DEVELOPMENT, not protected)

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| `P0_NAME_SIMILARITY` | 3/24 | 0.125 | 12 | 6 |
| `P1_GRAPH_HOMOMORPHISM` | 12/24 | 0.500 | 12 | 0 |
| `P2_CATEGORY_LAW_FUNCTOR` | 21/24 | 0.875 | 3 | 0 |
| `P3_DIAGRAM_CHASE` | 11/24 | 0.458 | 12 | 0 |
| `P4_FAITHFULNESS` | 12/24 | 0.500 | 12 | 0 |
| `P5_FIXED_LESSON_INJECTION` | 12/24 | 0.500 | 9 | 0 |
| **`F0_PARENT_FEDERATION`** | **24/24** | **1.000** | 0 | 0 |
| **`M_F2_FUNCTORIAL_TRANSFER_FULL`** | **24/24** | **1.000** | 0 | 0 |
| `M_MINUS_ENDPOINT_DISCIPLINE` | 21/24 | 0.875 | 0 | 0 |
| `M_MINUS_IDENTITY_CHECK` | 18/24 | 0.750 | 3 | 0 |
| `M_MINUS_COMPOSITION_CHECK` | 18/24 | 0.750 | 3 | 0 |
| `M_MINUS_FAITHFULNESS_RECOVERY` | 21/24 | 0.875 | 3 | 0 |
| `C_ALWAYS_TRANSFER` | 9/24 | 0.375 | 15 | 0 |
| `C_ALWAYS_BLOCK` | 3/24 | 0.125 | 0 | 9 |
| `C_RANDOM_DISPOSITION` | 4/24 | 0.167 | 3 | 8 |

Exact per-family numbers are in `fm50/results/FM50_DEVELOPMENT_ANALYSIS_V1.{json,md}`;
the JSON is authoritative and the table above is a summary.

### 5.1 Development gate block

| gate | verdict | violations | n evaluated |
|---|---|---|---|
| `G0a_KNOWN_ANSWER` | PASS | 0 | 11 fixtures |
| `G0b_ORACLE_SELF_AGREEMENT` | PASS | 0 | 24 instances |
| `G0c_NULL_CALIBRATION` | PASS | 0 | 4 checks |
| `G0d_DECOY_COVERAGE` | PASS | 0 | 4 decoy families |
| `G0e_PLANTED_POSITIVES` | PASS | 0 | 6 trip-wires |
| `G0f_FAMILY_DISCRIMINATION` | PASS | 0 | 2 halves |
| `G0g_ELIGIBILITY` (suite-owned) | PASS | 0 | 25 constructions + 29 live |
| `G1a_PARENT_REPRODUCES_M` | PASS | 0 | 24 instances (identity 1.0000) |
| `G1b_M_ADVANTAGE` | NOT_FIRED | 1 | 24 instances, 0 discordant pairs |
| `G2_ANTI_PERMISSIVENESS` | PASS | 0 | 15 oracle-blocked instances |
| `G3_MECHANISM_BY_OMISSION` | NOT_APPLICABLE | 0 | no claimed advantage |

Every verdict is printed with the number of instances its rule was actually
evaluated on. On development this predicts the pre-registered route
**`PARENT_SUFFICIENT`**.

`G0g` is a suite-owned gate: `fm_run.py` is shared across FM10–FM60 and was not
edited, so `G0g` is computed inside `fm50_suite`, is enforced by
`parent_fidelity()` (which the selftest requires to pass in full), and is
published in `FM50_SELFTEST_REPORT.json` and — per family — in
`generator_rejections` of every results and analysis file. Its live denominator
(29) is the 24 eligible plus the 5 ineligible constructions of this split.

## 6. Planted positives (G0e): 6/6 fire

| gate | planted case | fires |
|---|---|---|
| `G0b_ORACLE_SELF_AGREEMENT` | an oracle that searches only the first object map disagrees with exhaustive enumeration on the valid-functor count | yes |
| `G0a_KNOWN_ANSWER` | a deliberately wrong expected disposition | yes |
| `G2_ANTI_PERMISSIVENESS` | `C_ALWAYS_TRANSFER` on an oracle-blocked instance | yes |
| `G0f_FAMILY_DISCRIMINATION` | a synthetic per-arm table in which every arm scores 1.000 must **FAIL** the gate (the FM/FG R2 ceiling defect that made the LLM-dispatch `fm50` cell uninformative) | yes |
| `G3_MECHANISM_BY_OMISSION` | `M_MINUS_FAITHFULNESS_RECOVERY` must be wrong on a false equivalence where `M` is right | yes |
| `G0g_ELIGIBILITY` | a deliberately non-associative composition table must be caught by the associativity law and reported `INELIGIBLE`, never scored as a negative result | yes |

## 7. Independence of the mechanic — and its honest limit

`M` never calls `assess_functor` (the parent's call) and never calls the study's
own `claim_profile` (the oracle's). It rebuilds the donor's structural
description from `source_target` and `composition`, discovers the donor's
commuting triangles for itself instead of trusting the registered diagram list,
projects through the target's composition index, runs native recovery on the
registered distinctions and resolves the precedence itself.
`test_mechanic_is_not_a_wrapper_of_its_own_comparator` passes for FM50.

**But this is an independent implementation, not an independent result, and the
design says so before any outcome.** FM10 could honestly call `G1a`'s zero a
measurement because `M`'s anytime local search could fail to reach the optimum
the complete parent found. FM50's law fragment is a *total function of the
registered candidate*: any correct implementation of the functor laws must agree
with any other, so `M` and `P2` are expected to be decision-identical by
mathematics rather than by shared code. Reporting that zero as a measurement of
an alignment that could have diverged would be an overclaim, and it is not made.
The channels along which `M` could still diverge are its own precedence
resolution (the mixed class is a design choice, not a forced one) and its
discovered rather than registered diagram set.

What carries `G1a` is the **liveness control**, and here it is genuinely live.
All four ablations are known-different mechanics and every one of them disagrees
with the federation on this split:

| ablation | disagreements with `F0` (of 24) |
|---|---|
| `M_MINUS_COMPOSITION_CHECK` | 6 |
| `M_MINUS_IDENTITY_CHECK` | 6 |
| `M_MINUS_ENDPOINT_DISCIPLINE` | 3 |
| `M_MINUS_FAITHFULNESS_RECOVERY` | 3 |

The zero reported for `M` is a zero the counter was capable of not reporting.

Two results in the tables above are **definitional and labelled as such**:
`P2_CATEGORY_LAW_FUNCTOR` is a complete decision procedure for the functor laws,
so its 1.00 on every law family and 0.00 on `FALSE_EQUIVALENCE` are by
construction; and `C_ALWAYS_TRANSFER`'s 0.375 is arithmetic — three of the eight
families are registered `TRANSFER_VALID` — which is what the 0.40
null-calibration ceiling was checked against before the generator was written.

## 8. Reading (development only; nothing here is protected evidence)

No single parent reaches the endpoint. The category-law parent decides every
functor law exactly and misses the entire false-equivalence family; the
faithfulness parent owns that family and misses every law; the graph parent
cannot see composition; the diagram chaser cannot see the unit laws and, at
0.458, is the weakest of the structural parents. Their pre-registered federation
is exact, and the ORION mechanic is decision-identical to it.

If this holds on the protected split, FM50's content is an attribution — *which*
parent family owns *which* obstruction class, and the demonstration that
functoriality alone cannot certify a categorical transfer claim because the
constant functor satisfies every law while destroying every distinction the claim
depends on — plus the finding that ORION's functorial transfer loop is the
composition of two mature parents and nothing more.

Ablations behave as their omissions predict: removing the unit stage loses
exactly the identity and mixed families; removing the triangle stage loses
exactly the composition and mixed families; removing the graph stage loses
exactly the endpoint family; removing native recovery loses exactly the
false-equivalence family. These are properties of the typed composition and they
are load-bearing for `F0` exactly as much as for `M`.

Cost is reported and routes nothing: `M` 0.29 ms against `F0` 0.93 ms over the
split, flagged `COST_ADVANTAGE_M` because the federation issues two parent calls
where the mechanic makes one pass. It is a wall-clock flag on a 24-instance
split, not a claim.

## 9. Estimated protected-run cost

104 instances × 15 arms, deterministic, single core: a same-size probe completed
generation, dispatch and scoring in **0.42 s** wall. Budget: 1 CPU-minute. Runs
on the Mac; no CI on the Mac mini, and no cluster time is needed.
