# FM20 — Anti-Unification and Generalization: Exact Known-Answer Study Design (V1)

**Lane:** FM20, L4 formal transfer mechanics (issues #48, #50 §C1).
**Status:** frozen prospective design. No protected outcome has been generated or inspected.
**Machine-readable companion:** `FM20_ANTI_UNIFICATION_EXACT_STUDY_DESIGN_V1.json`.
**House style:** `me-x1`, `me-x2`, `me-x4`, and the FM10 sibling in this directory.

## 1. Task and endpoint

Each instance presents **positives** `P` (ground terms the abstraction must
cover), **negatives** `N` (terms it must not cover) and **held-out** `H` (terms
whose coverage the arm must predict). The registered endpoint is the **pair**
(disposition, held-out coverage vector), scored as an exact match:

| disposition | meaning |
|---|---|
| `ACCEPT_LGG` | the least general generalization of `P` covers no negative and is not vacuous |
| `REJECT_OVER_GENERAL` | the LGG covers at least one negative |
| `REJECT_NO_COMMON_STRUCTURE` | the LGG is a bare variable — the positives share no structure, so the "abstraction" is vacuous and accepting it would be a false analogy |

**Computing the LGG alone is deliberately not the endpoint.** Plotkin's
anti-unification decides it exactly, so a study built on it would report parent
sufficiency by construction rather than by measurement. The endpoint adds
negatives, a vacuity criterion, and held-out coverage prediction — which are the
protocol's own FM20 primaries (generalization correctness, held-out instance
prediction, unnecessary abstraction).

### A lattice fact the design depends on, stated rather than hidden

Every common generalization of `P` is *more general than or equal to* their LGG
(Plotkin 1970). So if the LGG covers a negative, **every** common generalization
covers it. There is therefore no "specialize until consistent" disposition
available in pure anti-unification, and the three dispositions above are
exhaustive. Registering a fourth would have been a design error.

Classification order is registered: **vacuity dominates over-generality**. A bare
variable is not an abstraction at all, so `REJECT_NO_COMMON_STRUCTURE` is
returned even when negatives are also covered. Fixture `KA-05` pins this.

## 2. Oracle and its independent cross-check

`lgg_exhaustive` enumerates the generalization lattice directly: every
generalization of `P[0]` is `P[0]` with an antichain of positions replaced by
variables, where positions sharing a variable carry equal subterms in `P[0]`.
It keeps the covering patterns and takes the minimum under the generality order
— and **verifies that the minimum is unique** up to renaming rather than
assuming Plotkin's theorem.

`lgg_plotkin` is anti-unification proper: fold pairwise generalization with a
substitution table keyed by the *pair* of disagreeing subterms, which is exactly
what makes two occurrences of the same disagreement share one variable.

They must agree on `disposition`, `lgg` and `coverage` for every instance of
every split (`G0b`), and share no code beyond the term representation and the
matcher. The generator proposes a family and the oracle verifies it; mismatches
are rejected, resampled, and the rejection counts published per family.

## 3. Arms, and why the comparator is the federation

| arm | kind | fidelity |
|---|---|---|
| `P0_FIXED_LESSON_INJECTION` | parent | the protocol's frozen-lesson baseline: common skeleton, fresh variable at every disagreement, no sharing |
| `P1_PLOTKIN_LGG` | parent | Plotkin 1970 / Reynolds 1970 anti-unification |
| `P2_CANDIDATE_ELIMINATION` | parent | Mitchell 1982 version spaces; the specific boundary after all positives is the LGG, rejected when it covers a negative |
| `P3_MDL_COMPRESSION` | parent | minimum description length selection over the covering patterns |
| `F0_PARENT_FEDERATION` | federation | **primary comparator** |
| `M_F2_ABSTRACTION_INDUCTION_FULL` | mechanic | ORION cover-driven abstraction induction |
| four `M_MINUS_*` | ablation | variable identity / negative challenge / compression / least generality |
| three `C_*` | control | always-accept, always-reject, random |

**No single parent owns the endpoint.** Plotkin's LGG is exact on the term but
has no negative examples and no vacuity criterion *in its own theory* — it always
accepts. Candidate elimination owns the negatives exactly but has no compression
criterion, so a bare variable consistent with the negatives is for it a perfectly
good hypothesis. MDL owns vacuity but selects by description length, so it can
generalize away a real shared regularity and has no consistency test. Each
boundary is recorded as a scope note and tested; none is a strawman.

The federation is combined under a rule fixed before any outcome and blind to
it: *P1 supplies the term; P3's compression criterion may veto it as vacuous;
P2's negative test may then veto it as over-general* — vacuity first, per the
registered classification order.

### M is an independent implementation, deliberately

`M` does not call Plotkin's algorithm. It runs a **cover-driven
specific-to-general search** of the kind used in inductive logic programming:
start from the first positive; for each still-uncovered positive, variablise the
minimal set of positions where the current pattern fails to match, sharing a
variable across positions carrying equal subterms; split a variable that is bound
inconsistently; iterate until every positive is covered; then apply the
compression criterion and the negative challenge.

Such a search can variablise a position higher in the term than necessary, so it
**can** diverge from the least general generalization — which is what makes
"the federation reproduces M" a measurement. FM10 had to repair exactly this
before its protected run.

On a 125-instance development probe the search did diverge, on 2 instances. Both
were traced to defects in `M` itself — a wrong fallback when a variable was bound
inconsistently, and a variable-name collision that forced accidental sharing —
and were repaired before freezing. A broken mechanic is as much a strawman as a
broken parent.

## 4. Gates

| gate | rule | hard |
|---|---|---|
| `G0a_KNOWN_ANSWER` | every hand-authored fixture reproduced by the oracle (≥ 8) | yes |
| `G0b_ORACLE_SELF_AGREEMENT` | the two oracle algorithms agree on disposition, lgg and coverage | yes |
| `G0c_NULL_CALIBRATION` | constant arms ≤ 0.40, random ≤ 0.40, shuffled-label null ≤ 0.40 | yes |
| `G0d_DECOY_COVERAGE` | each decoy family ≥ 3 instances | yes |
| `G0e_PLANTED_POSITIVES` | every planted positive trips its own gate predicate (≥ 3) | yes |
| `G0f_FAMILY_DISCRIMINATION` | two halves with separate denominators: *solvable* and *separating* | yes |
| `G1a_PARENT_REPRODUCES_M` | F0 reproduces M on ≥ 99.5%, no family > 5% discordant, **and** the counter is shown live by ≥ 1 ablation | yes |
| `G1b_M_ADVANTAGE` | detector | no |
| `G2_ANTI_PERMISSIVENESS` | on oracle-rejected instances M accepts no more than F0 (≥ 10 required) | yes |
| `G3_MECHANISM_BY_OMISSION` | applicable only if G1b fires | no |

Multiplicity: Holm across the five per-family paired tests.

**Reporting rules.** Every gate publishes the number of instances its rule was
actually evaluated on; a gate below its registered minimum returns
`CANNOT_CHECK`, never `PASS`, and the route line **names every hard gate that
could not be evaluated** rather than letting it read as silent agreement. On the
15-instance development split `G2` correctly returns `CANNOT_CHECK` (only 6
rejected instances, below its minimum of 10) — the machinery working as intended.
Six planted positives must all fire in the same execution that reports the
study's zeros.

## 5. Routes

`PARENT_SUFFICIENT` is a first-class successful terminal and the pre-registered
expectation. If `G1a` fails because `M` is **worse** than the federation, the
route is still `PARENT_SUFFICIENT` — the parent is at least as good — and that is
recorded explicitly rather than presented as a study defect.

## 6. Sizes, seeds and execution

125 protected instances (25 per family × 5 ≥ the 120 required by issue #50 §C1);
15 development; 10 selftest. Deterministic, single-core, well under a second.

Protected seed commitment:
`2b4eb309a77211c7aabbf4eb0fd760c8a31842888574b5c3a00f64f3a1291aae`
(sha256 of the seed held at `~/.orion-custody/fm/FM20_PROTECTED_SEED_V1.txt`).
Development and selftest seeds are public.

Exactly one protected run and one analysis. No design constant, gate, arm, oracle
rule or seed may change after outcome access.

## 7. Authority

Grants no scientific truth, no F2 superiority, no field status, no submission
readiness. A formal witness does not establish empirical truth.
