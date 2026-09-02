# ME-X1 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Design:** `ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.{md,json}` (this PR).
**Status:** development fixtures only. **No protected outcome has been generated
or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent; the `protected`
stage refuses (exit 3/4; asserted by `tests/unit/test_me_x1_exact_study.py`).
**Run:** Mac (local), 2026-09-02, `python3 mex1_run.py selftest` then `dev`;
selftest + 40-instance development split complete in < 1 s wall each; results
and custody files byte-identical across two consecutive runs (`cmp`).

## 1. Frozen code (sha256)

| file | sha256 |
|---|---|
| `mex1_model.py` | `e31fba5ec2319f566d4a7f3948e54c48b0194bcab8d0a7854ad606a83506543a` |
| `mex1_oracle.py` | `5a34146ca067f03c0557cdb71d229aca0d0f6dfeea690d2dce20f1f95fba696f` |
| `mex1_generator.py` | `08a50948c7fd12e4b0a0cbb24adc4b2b3225253bc9f821b1c5bddd2b539cc31d` |
| `mex1_parents.py` | `d13ebe5e0b4e56ba12cfe8370e5837f0b182c5a39ab75b944dbf9e282cb5726f` |
| `mex1_arms.py` | `cbe3d48e4feaab6b802af04306f1bb50f4820e2bdea231f3b1d3abab19680bf8` |
| `mex1_run.py` | `f4c8ed6be76bb44e78a2dac6259c01148e5b6b7091c08e1f082b3a373bbab4bc` |
| `ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.json` | `b9ae7b02fe0168ec94fed3bf36e4a7d223aac52e7f30a0fd44e9cfe0c664d7de` |
| `results/ME_X1_DEVELOPMENT_RESULTS_V1.json` | `634f33941bd59d15089bbd8b06452c4473f2b4728fe024409eab6aa9b833ac15` |
| `results/ME_X1_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `ff9dd17424de0a8ece8d763ac7a452662ab5a7d21c5a583ffaeb8060910ee248` |
| `results/ME_X1_SELFTEST_REPORT.json` | `1f4b8a6eac26072c4b25fda4a05b09a306f9cacabbc974514a5e1bb4f48e0353` |

Protected seed commitment (sha256 of the custody seed string):
`84ae78f5676879bfa022460bc17ae36233935e3bdfef4a63a670d9eda431c34d`.
A protected run requires `acknowledged_design_sha256` = the design-JSON hash above.

## 2. Parent fidelity: native known-answer tests (51/51 PASS)

Every parent passed its own native tests before being used inside any arm
(`mex1_parents.fidelity_selftests`, executed by `selftest` and by the unit test).

| parent | role | tests (all PASS) |
|---|---|---|
| JTMS (Doyle 1979; BPS ch. 7; vendored from ME-X4) | B4/B5 support engine | propagation chain; well-founded `assumptions_of`; retraction propagates OUT; alternative justification restores; alternative support after retraction; out-list default IN/OUT; circular support stays OUT; DDB records the nogood and retracts the culprit |
| Assurance case (GSN change impact; vendored) | B3 | solution change marks its own argument suspect; context change marks the contextualised argument suspect |
| Provenance-only (`orion_v2.provenance`; vendored) | B2 | revocation descendants; unrelated root unaffected |
| Contract binding (design-by-contract) | IDENT | matching identity satisfies; mismatch violates even with valid output; unrecoverable binding cannot check; same / registered-equivalent criterion satisfies; non-equivalent or unregistered violates; uncheckable equivalence cannot check |
| Refinement fidelity (formal refinement) | IDENT | identical statement faithful; registered unfaithful refinement violates; faithful refinement satisfies; unassessed cannot check; checker verdict separate from fidelity |
| Independence witness (`orion_v2.evidence.assess_evidence_dependence`) | DEP | three components without edges; confirmed edge defeats k=3; one edge leaves k=2 satisfied; suspected edge censors; no requirement → no atom |
| Transport licence (`orion_v2.structural.RelationType`) | TRANS | ISOMORPHIC licenses any requirement; weaker relation does not; equal strength licenses; absent relation blocks; CANNOT_CHECK censors |
| Metrology comparability (`orion_v2.comparability.ComparabilityCertificate`) | PROV | violated invariant NONCOMPARABLE; missing mapping/anchors CANNOT_CHECK; anchored invariants COMPARABLE |
| Evaluator coverage | EVAL | covered class passes; blind with registered alternative replaceable; blind without alternative uncheckable; invalidated contract replaceable; uncertain coverage censors |
| Atlas gluing (`orion_v2.epistemic_atlas.assess_atlas_gluing`) | ATLAS | pairwise compatibility is MATCHING_FAMILY_ONLY; separate witness glues; incompatible overlap obstructs; unresolved overlap cannot check |
| Authority lattice | AUTH | within ceiling allowed; exceeding blocked; policy under review cannot check; monotone in the ceiling |

## 3. Selftest (G0a, separation, G0b, G0c): PASS

- G0a: the 14 public development fixtures (`ME_X1_X2_DEVELOPMENT_KNOWN_ANSWER_FIXTURES_V1.json`,
  X1-DEV-001…014) are each bound to a concrete registered world; the oracle
  returns the fixture's expected action on 14/14 (incl. the reopened sets
  {c1, c2} for 004 and {p_cal, q} for 008 with the independent claim
  preserved), never a forbidden action; M and B5 are exact on all 14. The X2
  obstruction fixtures are the ME-X2 identity and are not bound here.
- Separation pair (H-EXT-3): the verdict-only rung outputs `PRESERVE` on
  both P and Q (identical, blind to the difference) and errs on P; rung 5 and
  M give P → `SELECTIVELY_REOPEN {c}`, Q → `PRESERVE`. Exact check, executed.
- G0b: walk/Kleene = exhaustive on every generated instance (selftest split
  and development split; max 2 censored atoms on development).
- G0c (development split): `C_ALWAYS_UPDATE` exact 0/27 where the oracle is
  not warranted; `C_ALWAYS_DEFER` exact 0/31 where the oracle is determinate;
  `C_RANDOM` exact 0.100; M vs permuted oracle decisions 0.1565 (chance
  0.1575, 200 permutations).

## 4. Development split (40 instances, 4 per family: POS, NEG, AMB, POS; DEVELOPMENT — not protected)

Instance sizes: 3–7 claims, 4–22 evidence units, 0–2 events. Oracle action mix:
UPDATE 0.25, DEFER_CANNOT_CHECK 0.225, REVALIDATE 0.15, PRESERVE 0.075,
SELECTIVELY_REOPEN 0.075, ABSTAIN / BLOCK / REFORMULATE / REPLACE 0.05 each,
REQUEST_NEW_EVIDENCE 0.025.

| arm | exact | false upd. | missed warr. | over/under-reopen | inv. transport | false closure | eval. / prob-spec / auth. laundering | correct unres. | warr. recall | unnec. defer |
|---|---|---|---|---|---|---|---|---|---|---|
| B0_DIRECT | 0.325 | 22 | 0 | 0 / 5 | 2 | 9 | 2 / 4 / 2 | 0.00 | 1.000 | 0.000 |
| B1_CALIBRATED_ABSTENTION | 0.375 | 3 | 4 | 0 / 5 | 0 | 1 | 0 / 2 / 0 | 0.89 | 0.538 | 0.690 |
| B2_PROVENANCE_PLUS_VERIFIER | 0.425 | 16 | 0 | 2 / 1 | 1 | 8 | 2 / 2 / 2 | 0.00 | 0.923 | 0.000 |
| B3_PARENT_NATIVE_ASSURANCE | 0.500 | 0 | 0 | 5 / 0 | 0 | 0 | 0 / 0 / 0 | 0.00 | 0.923 | 0.000 |
| B4_PARENT_MODULES_WITH_SHARED_STATE | 0.825 | 7 | 0 | 0 / 0 | 0 | 3 | 0 / 2 / 2 | 0.67 | 1.000 | 0.000 |
| B5_R1_VERDICT_ONLY | 1.000 | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| B5_R2_PROV | 1.000 | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| B5_R3_PROV+DEP | 1.000 | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| B5_R4_PROV+DEP+TRANS+EVAL | 1.000 | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| **B5_STRONGEST_FAITHFUL_PARENT_FEDERATION** | **1.000** | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| **M_ME_TRANSITION_CONTROL** | **1.000** | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| M_MINUS_PROBLEM_IDENTITY | 0.850 | 6 | 0 | 0 / 0 | 0 | 2 | 0 / 4 / 0 | 0.78 | 1.000 | 0.000 |
| M_MINUS_DEPENDENCE | 0.925 | 1 | 0 | 0 / 1 | 0 | 1 | 0 / 0 / 0 | 0.89 | 1.000 | 0.000 |
| M_MINUS_EVALUATOR_CONTRACT | 0.925 | 3 | 0 | 0 / 0 | 0 | 1 | 2 / 0 / 0 | 0.89 | 1.000 | 0.000 |
| M_MINUS_TRANSPORT | 0.925 | 3 | 0 | 0 / 0 | 2 | 1 | 0 / 0 / 0 | 0.89 | 1.000 | 0.000 |
| M_MINUS_SUPPORT_REOPENING | 0.950 | 0 | 0 | 2 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 0.923 | 0.000 |
| M_MINUS_AUTHORITY | 0.925 | 3 | 0 | 0 / 0 | 0 | 1 | 0 / 0 / 2 | 0.89 | 1.000 | 0.000 |
| M_MINUS_UNRESOLVED_TERMINAL | 0.775 | 7 | 0 | 0 / 0 | 0 | 9 | 0 / 0 / 0 | 0.00 | 1.000 | 0.000 |
| M_MINUS_MEASUREMENT_COMPARABILITY | 0.925 | 3 | 0 | 0 / 0 | 0 | 1 | 0 / 0 / 0 | 0.89 | 1.000 | 0.000 |
| M_MINIMAL_RECEIPT | 1.000 | 0 | 0 | 0 / 0 | 0 | 0 | 0 / 0 / 0 | 1.00 | 1.000 | 0.000 |
| C_ALWAYS_UPDATE | 0.325 | 22 | 0 | 0 / 5 | 2 | 9 | 2 / 4 / 2 | 0.00 | 1.000 | 0.000 |
| C_ALWAYS_DEFER | 0.225 | 0 | 10 | 0 / 5 | 0 | 0 | 0 / 0 / 0 | 1.00 | 0.000 | 1.000 |
| C_RANDOM_ACTION | 0.100 | 1 | 9 | 15 / 5 | 0 | 1 | 0 / 0 / 0 | 0.22 | 0.077 | 0.207 |

**B5 exactly reproduces M's transition decisions on every development instance
of every family** (G1a decision identity 40/40 = 1.000; G1b discordant pairs
= 0; G2 unnecessary defer M 0 = B5 0, warranted recall 1.000 = 1.000). On
development this predicts the pre-registered route **`PARENT_SUFFICIENT`** with
ladder terminal **`RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`**. G3 not
applicable (no claimed advantage).

**Ladder (H-EXT-3) on development: flat at 1.000 from rung 1.** The 40
development instances happen not to contain the sub-variants that separate
the rungs (criterion mismatch, checker-invalid, retracted-source basis,
unsupported local piece, and the family-composition structure of the
separation pair); the separation pair itself, checked in selftest, is where
the verdict-only rung breaks (blind on P/Q, wrong on P). On the protected
split those sub-variants are generated at their frozen rates, and the design
predicts the gap to appear at the **R4→R5 step** (identity/criterion/spec,
atlas and authority witnesses are verdict-level below rung 5). This is a
prediction, not a result.

**Per-family attribution (where B0–B4 break, development):**
`B0` launders every positive (0.10 on positives) and closes every ambiguity
(false closure 9); `B1` defers on 69% of determinate cases (unnecessary defer
0.690, warranted recall 0.538) — the generic uncertainty gate is
over-conservative exactly as §8 anticipates; `B2` catches binding mismatch
through artifact lineage and calibration through revocation but has no
transport-rank, coverage, dependence, atlas or authority vocabulary (false
update 16, invalid transport 1, false closure 8) and re-validates on the
registered ontic `TARGET_CHANGED` control; `B3` never launders but over-reopens
(5) under AND semantics and answers every challenge with `REVALIDATE` (0.25
on D/E/F/G/I); `B4` (the TMS federation) is exact on B–F (typed
provenance/dependence/transport/evaluator) and fails precisely where the
cross-transition conditions are not TMS-owned: authority (0.25), criterion /
spec fidelity (A 0.75, H 0.25), and the atlas witness (I: pairwise taken as
global, false closure). Ablations behave as their omission predicts: minus
problem identity fails A and H (0.25 each); minus dependence fails C (0.25);
minus transport fails D (0.25); minus evaluator contract fails F (0.25); minus
authority fails G (0.25); minus measurement/comparability fails B (0.25);
minus support reopening over-reopens the independent-route controls (E 0.50,
J negative); minus unresolved terminal closes all nine ambiguities (0.10 on
AMB). Each omission has causal value **for M and equally for B5** — they are
properties of the typed interface.

**M_MINIMAL_RECEIPT (frozen from development):** backward elimination dropped
`witness, piece, evc, tr, comparability, ident, checker, criterion, nocontra`
while staying exact on all 40 development instances — i.e. the development
split does not exercise those kinds. The protected split measures what a
receipt minimised on development loses (a prospective, not a tuned, ablation).

Cost (wall-clock, Mac, 40 instances): M 7.4 ms vs B5 15.0 ms → ratio 2.03,
flag `COST_ADVANTAGE_M`; ops M 3 436 (obligations + selective-reopen size
proxy) vs B5 8 288 (JTMS justification checks), not commensurable. A 2× ratio
on 40 tiny instances is a laptop timing, not a claim; nothing routes on cost.

## 5. Estimated protected-run cost

1 000 instances × 23 arms, deterministic, single core: development throughput
(40 instances in ≈ 0.5 s including generation, 23 arms, minimal-receipt
derivation and analysis) extrapolates to **≈ 10–30 CPU-seconds**; budget 2
CPU-minutes. Deterministic Python on the Mac; never CI on the Mac mini.

## 6. Development-time defects fixed before freeze

Two arm-glue defects were caught by the development fixtures and fixed
before the freeze, with no change to any oracle rule, gate or constant:
(1) support-level verdict compression deleted the status of atoms whose ids
are shared with the request level (`cal:e`, `ident:e`), so the verdict-only
rung under-reported PROV conditions; (2) the request-level verdict for the
ATLAS module was computed before the piece dispositions existed. Both were
visible as R1 misses on the 14 public fixtures (X1-DEV-003, -014).

## 7. Authority

Development numbers are development numbers. Nothing here grants field status,
novelty, or publication authority. The route above is a prediction of what the
frozen gates will say on the protected split, not a result.
