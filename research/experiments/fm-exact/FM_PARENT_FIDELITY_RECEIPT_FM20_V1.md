# FM20 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Status:** development artifacts only. **No protected outcome has been generated
or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent, so
`fm_run.py FM20 protected` refuses (exit 3), asserted by
`tests/unit/test_fm_exact_suites.py::test_protected_stage_refuses_without_authorization`.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM20 selftest` then `dev`;
each completes in well under a second. Two consecutive runs are byte-identical.

## 1. Frozen code and artifacts (sha256)

| file | sha256 |
|---|---|
| `fm_core.py` | `137b14eb5be171e50b24cfe36539e625c081be5ab548e71093fa3d2a81313ed9` |
| `fm_run.py` | `26878681a8f273025d052c5497c2a5773000d10f43ac317fc635b74cde47fe67` |
| `fm20_suite.py` | `ac7bb1cd3dd972e859445101b1fc7a6aabb96c1a4dc9c466484ffba014ba60ef` |
| `FM20_..._DESIGN_V1.json` | `ce97a64234f08d1c4657dc215e3a512c494982d310849cb753a7f1c22c591c98` |
| `fm20/results/FM20_DEVELOPMENT_RESULTS_V1.json` | `735f7ebfdd01c6d8d03a167780324c59b67334ac8419d4a3e086c7aedfe29604` |
| `fm20/results/FM20_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `85ec0d4f2b86427b79c3f783337b290fb1f9bfa4d5b08218954061f531e4e91c` |
| `fm20/results/FM20_SELFTEST_REPORT.json` | `6bf061ccc0fa9f5320d920bee9eb7f0718aef37b004f6a2139239c3a31134a15` |

FM20 protected seed commitment:
`2b4eb309a77211c7aabbf4eb0fd760c8a31842888574b5c3a00f64f3a1291aae`.

## 2. Parent fidelity: native known-answer tests (24/24 PASS)

| parent | tests (all PASS) |
|---|---|
| `P1_PLOTKIN_LGG` (Plotkin 1970; Reynolds 1970) | textbook LGG of two terms; **a repeated disagreement shares one variable** (`f(a,a)`, `f(b,b)` → `f(X,X)`) while distinct disagreements take distinct variables (`f(a,b)`, `f(c,d)` → `f(X,Y)`) — the property that separates anti-unification from position-wise variablisation; different top symbols give a bare variable; identical terms generalize to themselves; nested structure is preserved; the three-term fold is a common generalization; documented boundary — anti-unification has no negative examples in its theory, so it always accepts |
| `P2_CANDIDATE_ELIMINATION` (Mitchell 1982) | accepts when no negative is covered; rejects when the specific boundary covers a negative; documented boundary — version spaces have no compression criterion, so a vacuous bare variable consistent with the negatives is accepted |
| `P3_MDL_COMPRESSION` | prefers a pattern that compresses the examples; reports vacuity when nothing is shared; documented boundary — selects by description length, not by consistency, so it has no negative test |
| `P0_FIXED_LESSON_INJECTION` | over-generalises repeated structure with fresh variables (`f(a,a)`, `f(b,b)` → `f(X,Y)`); keeps the shared skeleton otherwise |
| `ORACLE_PAIR` | the exhaustive lattice minimum equals Plotkin's LGG on four hand-built term pairs, **and the minimum is verified unique** in each case |
| `MATCHER` | a variable matches any ground term; a repeated variable requires equal arguments and accepts equal ones; constants must match exactly |

Three boundaries are recorded as scope notes rather than defects, and they are
precisely why the federation is the honest comparator: P1 cannot reject, P2
cannot detect vacuity, P3 cannot test consistency.

## 3. Known-answer fixtures (G0a): 10/10

All ten reproduced by the exhaustive oracle and the independent Plotkin
cross-check, on disposition, LGG and held-out coverage. `KA-05` pins the
registered classification order (vacuity dominates over-generality).

## 4. Planted positives (G0e): 6/6 fire

| gate | planted case | fires |
|---|---|---|
| `G0b` | the position-wise generalizer must disagree with the exhaustive lattice minimum on a term with repeated structure | yes |
| `G0a` | a deliberately wrong expected disposition | yes |
| `G2` | `C_ALWAYS_ACCEPT` on an instance the oracle rejects | yes |
| `G0f` | a synthetic all-ceiling arm table must **FAIL** the discrimination gate | yes |
| `G3` | `M_MINUS_COMPRESSION_CRITERION` must be wrong on a vacuous instance where `M` is right | yes |
| `G0b` | the lattice enumeration reports a *verified* unique minimum, so the uniqueness field is computed rather than assumed | yes |

## 5. Development split (15 instances, 3 per family — DEVELOPMENT, not protected)

| arm | exact | rate |
|---|---|---|
| **`F0_PARENT_FEDERATION`** | **15/15** | **1.000** |
| **`M_F2_ABSTRACTION_INDUCTION_FULL`** | **15/15** | **1.000** |
| `M_MINUS_VARIABLE_IDENTITY` | 15/15 | 1.000 |
| `P0_FIXED_LESSON_INJECTION` | 12/15 | 0.800 |
| `P2_CANDIDATE_ELIMINATION` | 12/15 | 0.800 |
| `M_MINUS_COMPRESSION_CRITERION` | 12/15 | 0.800 |
| `M_MINUS_NEGATIVE_CHALLENGE` | 12/15 | 0.800 |
| `P3_MDL_COMPRESSION` | 11/15 | 0.733 |
| `P1_PLOTKIN_LGG` | 9/15 | 0.600 |
| `M_MINUS_LEAST_GENERALITY` | 5/15 | 0.333 |
| `C_RANDOM_DISPOSITION` | 1/15 | 0.067 |
| `C_ALWAYS_ACCEPT` | 0/15 | 0.000 |
| `C_ALWAYS_REJECT` | 0/15 | 0.000 |

### 5.1 Development gate block

| gate | verdict | evaluated |
|---|---|---|
| `G0a_KNOWN_ANSWER` | PASS | 10 fixtures |
| `G0b_ORACLE_SELF_AGREEMENT` | PASS | 15 instances |
| `G0c_NULL_CALIBRATION` | PASS | 4 checks |
| `G0d_DECOY_COVERAGE` | PASS | 4 decoy families |
| `G0e_PLANTED_POSITIVES` | PASS | 6 trip-wires |
| `G0f_FAMILY_DISCRIMINATION` | PASS | 2 halves |
| `G1a_PARENT_REPRODUCES_M` | PASS | 15 instances (identity 1.000) |
| `G1b_M_ADVANTAGE` | NOT_FIRED | 0 discordant pairs |
| **`G2_ANTI_PERMISSIVENESS`** | **CANNOT_CHECK** | 6 oracle-rejected instances, below the registered minimum of 10 |
| `G3_MECHANISM_BY_OMISSION` | NOT_APPLICABLE | no claimed advantage |

`G2` returning `CANNOT_CHECK` on a 15-instance split is the machinery working as
designed, and the route line names it explicitly rather than letting an unchecked
hard gate read as silent agreement. The protected split (125 instances, two
rejecting families) supplies a sufficient denominator.

G1a liveness control on development: the same discordance counter registered 10,
3, 3 and 2 disagreements for the four ablation arms.

## 6. Three development-time corrections, recorded

1. **`C_ALWAYS_ACCEPT` was not a control.** It computed the true LGG for its
   coverage vector and scored 0.60 on the selftest split — the LGG parent wearing
   a control's label. It now carries no abstraction of its own and scores 0.000.
2. **The `DISTRACTOR_REGULARITY` family did not discriminate.** Its positives did
   not force a repeated variable, so `M_MINUS_VARIABLE_IDENTITY` was never
   falsified (0 discordance). The family now plants a variable occurring at two
   positions and a negative that instantiates them differently; the ablation now
   separates.
3. **Two defects in `M` itself**, found on a 125-instance development probe where
   the cover-driven search diverged from the LGG on 2 instances: a wrong fallback
   when a variable was bound inconsistently (it re-variablised an unrelated
   position instead of splitting the conflicted variable), and a variable-name
   collision across iterations that forced accidental sharing. Both repaired
   before freezing. A broken mechanic is as much a strawman as a broken parent,
   and reporting a parent-sufficiency verdict produced by a crippled `M` would
   have been worthless.

All three were found on development seeds. No protected outcome existed.

## 7. Reproducibility checks (added after a sibling lane hit a seed-reproduction bug)

- **Hash-seed independence, verified not assumed.** The generator draws only
  from ordered sequences, never while iterating an unordered set. The split's
  canonical digest is identical under `PYTHONHASHSEED` 0, 1 and 12345 for both
  FM10 and FM20 — asserted permanently by
  `test_generator_is_independent_of_python_hash_seed`. Without this a committed
  seed regenerates a different split in another process, because Python
  randomises string hashing per process.
- **Anti-conservatism gate liveness.** `G2` now carries a computed liveness
  control: on the oracle-rejected instances, at least one arm must register a
  nonzero over-acceptance count, or the gate's `0 <= 0` is vacuous and it cannot
  pass. On FM20 development the counter registers 6; on FM10 development, 15.
  Checked retrospectively against the frozen FM10 protected artifact without
  re-running it: 90 over-accepts on the same 90 blocked instances, so FM10's
  published `G2` pass was live.
- **Per-family threshold transparency.** `G1a`'s 5% per-family rule is now
  reported together with the integer number of discordant instances it actually
  permits at the given family size, so a threshold that collapses to "no
  discordance at all" is not read as something laxer.

## 8. Estimated protected-run cost

125 instances × 13 arms: a same-size probe completed generation, dispatch and
scoring in **0.11 s** wall. Budget: 1 CPU-minute. Runs on the Mac.
