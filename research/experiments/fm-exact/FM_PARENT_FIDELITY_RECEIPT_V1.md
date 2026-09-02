# FM series — Parent Fidelity Receipt and Development-Split Summary (V1)

**Scope of this revision:** FM10. Later suites append their own sections to this
file as they land; the file is the single place where a comparator earns the
right to be used.

**Status:** development artifacts only. **No protected outcome has been
generated or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent, so
`fm_run.py FM10 protected` refuses (exit 3), asserted by
`tests/unit/test_fm_exact_suites.py::test_protected_stage_refuses_without_authorization`.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM10 selftest` then `dev`;
each completes in well under a second. Two consecutive runs produce
byte-identical results and custody files (asserted by
`test_development_split_is_deterministic`).

## 1. Frozen code and artifacts (sha256)

| file | sha256 |
|---|---|
| `fm_core.py` | `408a5b20f26b642935b41d1e1b391e447439cdff82f5362e3840c20bb4110cc6` |
| `fm_run.py` | `f183c9a15b158a9933d6a9bbaf55a1c9d94ccd6ad960714d3bd8f3ef44382da6` |
| `fm10_suite.py` | `0074f9cc8ae69ca0b9c29496fae494496dc381c94f82e06adb167baa73adff40` |
| `FM10_..._DESIGN_V1.json` | `5d8cb8ee93258c17e2b0b054fd6406dbab06baa231892842f85011f0cff2a3ba` |
| `fm10/results/FM10_DEVELOPMENT_RESULTS_V1.json` | `100c5718d99aa39dbfc8a03d48fec5329b4fff1dc70a24a6568e8c75da2ec1cd` |
| `fm10/results/FM10_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `b3fc3433d9378f86becd7398b9b2488fb000d9a4e1d04514ffd32e1bfaa6f18f` |
| `fm10/results/FM10_SELFTEST_REPORT.json` | `08fa50bc18324dc855b97820b2bc703d2931026b3acaf6acda094c973dd74a0c` |

FM10 protected seed commitment (sha256 of the custody seed string):
`b630beec4e60723caa3435b8c06754ecc184f66b2fc0787d27430979e4e447a4`.
A protected run additionally requires `acknowledged_design_sha256` to equal the
design-JSON hash above and `suite` to equal `FM10`.

## 2. FM10 parent fidelity: native known-answer tests (21/21 PASS)

Every comparator passed its own native tests before being used
(`fm10_suite.parent_fidelity`, executed by `selftest` and by the unit test).

| parent | tests (all PASS) |
|---|---|
| `P1_SME_STRUCTURE_MAPPING` (Falkenhainer, Forbus & Gentner 1989) | the Rutherford analogy recovers sun→nucleus / planet→electron from shared relational structure across differing object attributes, and reports a valid transfer; one-to-one correspondence is enforced when two base nodes compete for one target node; systematicity prefers the larger connected system over an isolated match; documented boundary recorded — the gmap merge is greedy and never backtracks, which is the published algorithm, not a handicap imposed here |
| `P2_COMPLETE_HOMOMORPHISM` | an exact embedding is found; the absence of any injective type-respecting map is reported as such rather than as a missing fact; a relation-type mismatch is distinguished from an outright absence; symmetric node types correctly absorb a relabelling that looks like a reversal; documented boundary recorded — P2 is fact-level and structurally blind to the registered-invariant stratum |
| `P4_INVARIANCE_PARENT` | acyclicity holds in a DAG and fails on a two-cycle and on a three-cycle; antisymmetry fails on a two-cycle; functionality fails when a source has two images; a perfect embedding whose presupposed invariant fails in the target is blocked; documented boundary recorded — P4 performs no alignment and is blind to every mapping obstruction |
| `P0_SURFACE_SIMILARITY` | prefers the name-similar target node over the structurally correct one (the behaviour surface decoys exist to expose) |
| `P3_FIXED_LESSON_INJECTION` | blocks when the surface correspondence misses a fact; transfers when it is perfect |
| `REFERENCE_MODULE` (`orion_v2.transfer_formal_mechanics`) | `assess_partial_homomorphism` agrees with the study's own profile primitive on a hand-built valid embedding |

Two boundaries are recorded as scope notes rather than defects, because they are
what makes the federation the honest comparator: P2 cannot see invariants and P4
cannot align. Neither is a strawman; each is complete within its own competence.

## 3. Known-answer fixtures (G0a): 11/11, with one correction recorded

All eleven hand-authored fixtures are reproduced by the exhaustive oracle and by
the independent branch-and-bound cross-check.

One hand-authoring error was caught by the oracle during development and is
recorded here as the only semantic correction made: the first draft of
`KA-06-MIXED` used two interchangeable `OBJECT` nodes, so a *cheaper* map existed
that traded the intended mixed profile for a single absent fact — making
`BLOCK_NO_HOMOMORPHISM` the correct class, not `BLOCK_MIXED_TYPED_OBSTRUCTION`.
The fixture was rebuilt with distinct node types so exactly one typed map exists.
The oracle was not changed; the fixture was.

A second development-time correction was made to the *generator*, not to any
answer: target node ordering is now shuffled, because without it the intended
embedding was always the first map in identifier order, which made the
`M_MINUS_OBSTRUCTION_SEARCH` ablation vacuous (1.000 across every family). After
the fix that ablation scores 0.468 on a same-size probe. This was an artifact of
the generator, and it is exactly the class of defect the `G0f` discrimination
gate exists to catch.

## 4. Planted positives (G0e): 5/5 fire

Registered trip-wires, all executed in the same run that reports the study's
zeros:

| gate | planted case | fires |
|---|---|---|
| `G0b_ORACLE_SELF_AGREEMENT` | a deliberately incomplete "first typed map, no optimisation" pseudo-oracle on an instance whose first map is bad and a later one perfect | yes |
| `G0a_KNOWN_ANSWER` | a deliberately wrong expected disposition | yes |
| `G2_ANTI_PERMISSIVENESS` | `C_ALWAYS_TRANSFER` on an oracle-blocked instance | yes |
| `G0f_FAMILY_DISCRIMINATION` | a synthetic per-arm table in which every arm scores 1.000 (the FM/FG R2 ceiling defect) must **FAIL** the gate | yes |
| `G3_MECHANISM_BY_OMISSION` | `M_MINUS_INVARIANCE_TEST` must be wrong on an invariant-break instance where `M` is right | yes |

## 5. FM10 development split (21 instances, 3 per family — DEVELOPMENT, not protected)

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| `P0_SURFACE_SIMILARITY` | 11/21 | 0.524 | 2 | 4 |
| `P1_SME_STRUCTURE_MAPPING` | 18/21 | 0.857 | 3 | 0 |
| `P2_COMPLETE_HOMOMORPHISM` | 18/21 | 0.857 | 3 | 0 |
| `P3_FIXED_LESSON_INJECTION` | 9/21 | 0.429 | 3 | 3 |
| `P4_INVARIANCE_PARENT` | 9/21 | 0.429 | 10 | 0 |
| **`F0_PARENT_FEDERATION`** | **21/21** | **1.000** | 0 | 0 |
| **`M_F2_TRANSFER_DISCOVERY_FULL`** | **21/21** | **1.000** | 0 | 0 |
| `M_MINUS_RELATIONAL_MAPPING` | 12/21 | 0.571 | 0 | 3 |
| `M_MINUS_INVARIANCE_TEST` | 18/21 | 0.857 | 3 | 0 |
| `M_MINUS_OBSTRUCTION_SEARCH` | 8/21 | 0.381 | 0 | 5 |
| `M_MINUS_TYPE_DISCIPLINE` | 21/21 | 1.000 | 0 | 0 |
| `C_ALWAYS_TRANSFER` | 6/21 | 0.286 | 15 | 0 |
| `C_ALWAYS_BLOCK` | 6/21 | 0.286 | 0 | 6 |
| `C_RANDOM_DISPOSITION` | 2/21 | 0.095 | 6 | 5 |

`M_MINUS_TYPE_DISCIPLINE` is **not separated on the 21-instance development
split** (1.000): an untyped injective search recovers the same optimal maps at
these sizes. On a same-size probe of the protected split it separates only
marginally (0.984, one instance). It is recorded as the weakest of the four
ablations and nothing is claimed from it.

Exact per-family and per-arm numbers are in
`fm10/results/FM10_DEVELOPMENT_ANALYSIS_V1.{json,md}`; the table above is a
summary and the JSON is authoritative.

### 5.1 Development gate block

| gate | verdict | evaluated |
|---|---|---|
| `G0a_KNOWN_ANSWER` | PASS | 11 fixtures |
| `G0b_ORACLE_SELF_AGREEMENT` | PASS | 21 instances |
| `G0c_NULL_CALIBRATION` | PASS | 4 checks |
| `G0d_DECOY_COVERAGE` | PASS | 4 decoy families |
| `G0e_PLANTED_POSITIVES` | PASS | 5 trip-wires |
| `G0f_FAMILY_DISCRIMINATION` | PASS | 14 arms |
| `G1a_PARENT_REPRODUCES_M` | PASS | 21 instances (identity 1.000) |
| `G1b_M_ADVANTAGE` | NOT_FIRED | 21 instances, 0 discordant pairs |
| `G2_ANTI_PERMISSIVENESS` | PASS | 15 oracle-blocked instances |
| `G3_MECHANISM_BY_OMISSION` | NOT_APPLICABLE | no claimed advantage |

Every verdict is printed with the number of instances its rule was actually
evaluated on. On development this predicts the pre-registered route
**`PARENT_SUFFICIENT`**.

### 5.2 Reading (development only; nothing here is protected evidence)

No single parent reaches the endpoint: the complete relational search misses the
whole invariant family, the invariance parent misses every mapping family, the
fixed-lesson table and surface similarity fail the decoys. Their pre-registered
federation is exact, and the ORION mechanic is decision-identical to it. If this
holds on the protected split, FM10's content is an attribution — *which* parent
family owns *which* obstruction class — plus the finding that ORION's
transfer-discovery loop for finite relational mapping is the composition of two
mature parents and nothing more.

Ablations behave as their omissions predict: removing relational alignment
collapses the decoy and typed-obstruction families; removing the invariance test
collapses exactly the invariant family and nothing else; removing obstruction
search collapses to whatever the arbitrary first typed map happens to give.
These are properties of the typed composition, and they are load-bearing for
`F0` exactly as much as for `M`.

Generator rejections (development): 33 across 21 accepted instances, concentrated
in `SURFACE_DECOY` where a random relabelling frequently leaves the surface map
valid and therefore not a decoy. Rejections are counted per family and published
in the results file.

## 6. Estimated protected-run cost

126 instances × 14 arms, deterministic, single core: a same-size probe completed
generation, dispatch and scoring in **0.58 s** wall. Budget: 1 CPU-minute. Runs
on the Mac; no CI on the Mac mini, and no cluster time is needed.
