# ME-X3 — Parent fidelity receipt and development-split summary V1

**State date:** 2026-09-02
**Design:** `ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.{md,json}`
**Split reported here:** `DEVELOPMENT` (27 instances, public seed
`ME-X3-DEV-20260902`). **No protected outcome has been generated or
inspected.** Development numbers are not evidence for or against any hypothesis;
they exist to show the environment discriminates and the parents behave like
their sources.

## 1. Why this receipt exists

A federation whose members do not actually behave like the systems they stand for
is a strawman, and a study built on one is worthless. Before any protected run,
each parent must reproduce, on a hand-authored case, the behaviour its source is
known for — and the oracle must be shown to agree with an independent
implementation of itself.

## 2. G0: selftests

| test | result | detail |
|---|---|---|
| `A0_proves_a_short_target` | PASS | VERIFIED |
| `A0_derivation_is_axiom_sound` | PASS | OK |
| `A3_discovers_the_answer_before_proving` | PASS | REFUTED |
| `A3_countermodel_is_a_model_of_the_axioms` | PASS | OK |
| `A0_cannot_settle_a_false_statement` | PASS | UNVERIFIED |
| `A1_retrieval_uses_the_library` | PASS |  |
| `federation_runs_a_specification_check` | PASS | REFUTED/MATERIALLY_WEAKENED |
| `proof_only_parent_reports_alignment_it_never_checked` | PASS | FAITHFUL |
| `two_independent_searches_agree_on_minimal_length` | PASS |  |
| `model_enumeration_fast_path_is_exact` | PASS | 130 vs 130 |
| `null_calibration_B5_does_not_escalate_on_an_identity` | PASS | CONTINUE_DIRECT_PROOF_SEARCH/VERIFIED |
| `null_calibration_M_does_not_escalate_on_an_identity` | PASS | CONTINUE_DIRECT_PROOF_SEARCH/VERIFIED |
| `fixture_short_proof_is_direct` | PASS |  |
| `fixture_false_statement_is_refuted` | PASS |  |
| `fixture_provable_but_wrong_question` | PASS |  |
| `fixture_trivialised_statement_is_drift` | PASS |  |

`16/16` passed.

Two of these carry more weight than the rest.
`two_independent_searches_agree_on_minimal_length` runs breadth-first search and
iterative-deepening depth-first search over the same rewrite graph and requires
identical minimal lengths, so a bug in one would have to be exactly mirrored in
the other. `model_enumeration_fast_path_is_exact` checks the definable-generator
optimisation — which drops the alternative presentation's model enumeration from
`n^(n·4)` to `n^(n·3)` — against brute-force enumeration of every function tuple,
so the speedup is verified to be exact rather than assumed to be.

## 3. Parent behaviour on the development split

| arm | validity | fidelity | minimal action | joint | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|
| `A0_DIRECT` | 0.444 | 0.926 | 0.259 | 0.259 | 1.000 | 0.000 | 0.333 | 156 |
| `A1_RETRIEVAL` | 0.444 | 0.926 | 0.407 | 0.407 | 1.000 | 0.000 | 0.000 | 374 |
| `A2_SELF_REFLECT` | 0.296 | 0.926 | 0.259 | 0.259 | 1.000 | 0.000 | 0.000 | 271 |
| `A3_DISCOVER_AND_PROVE_PARENT` | 0.593 | 0.926 | 0.519 | 0.519 | 1.000 | 0.000 | 0.000 | 335 |
| `A4_LEMMA_ABSTRACTION_PARENT` | 0.630 | 0.926 | 0.593 | 0.593 | 1.000 | 0.000 | 1.000 | 653 |
| `B5_R1_VERDICT_ONLY` | 0.852 | 1.000 | 1.000 | 0.852 | 0.000 | 0.000 | 1.000 | 646 |
| `B5_R2_SATURATION` | 0.852 | 1.000 | 1.000 | 0.852 | 0.000 | 0.000 | 1.000 | 542 |
| `B5_R3_FRONTIER` | 0.852 | 1.000 | 1.000 | 0.852 | 0.000 | 0.000 | 1.000 | 542 |
| `B5_R4_SEMANTIC` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 542 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 542 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 509 |

Read the `drift missed` column first. Every proof-only parent (`A0`–`A4`) misses
**every** specification drift, because a system that treats proof success as
intent success has no way to see it; every arm that runs the specification check
misses **none**. That is the FormalScience result reproduced inside this
environment, and it is the reason proof validity and specification fidelity are
scored as separate endpoints rather than combined.

`false drift alarm` is `0.000` everywhere: no arm buys its drift detection by
crying wolf on the faithful controls.

`M` and the top-rung federation are tied on every decision endpoint and `M` is
cheaper, which is what the pre-registered `PARENT_SUFFICIENT` expectation looks
like: on an exhaustive finite oracle, control buys ordering, not reach.

### 3.1 F7 by realized drift subtype

| subtype | n | M fidelity | A0 fidelity |
|---|---|---|---|
| `ABSTRACTION_ELEVATION` | 1 | 1.000 | 0.000 |
| `FAITHFUL` | 1 | 1.000 | 1.000 |
| `MATERIALLY_WEAKENED` | 1 | 1.000 | 0.000 |

The development split is far too small to cover the subtype space; the point of
this table is that the scorer reports the realized draw rather than the
generator's proposal weights, so a family average cannot hide a subtype that is
never detected on the protected split.

## 4. Ablations on the development split

| arm | joint | fidelity | minimal action | false change | drift missed | held-out reuse |
|---|---|---|---|---|---|---|
| `M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK` | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| `M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM` | 0.852 | 1.000 | 0.852 | 0.000 | 0.000 | 1.000 |
| `M_LOCUS_LABELS_SHUFFLED` | 0.852 | 1.000 | 0.852 | 0.000 | 0.000 | 1.000 |
| `M_MINUS_COUNTEREXAMPLE_PROBE` | 0.852 | 1.000 | 0.889 | 0.000 | 0.000 | 1.000 |
| `M_MINUS_FALSE_CHANGE_PENALTY` | 0.889 | 1.000 | 0.889 | 0.111 | 0.000 | 1.000 |
| `M_MINUS_LEMMA_INVENTION` | 0.815 | 1.000 | 0.815 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_LEMMA_LEVEL` | 0.667 | 1.000 | 0.667 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| `M_MINUS_OBSTRUCTION_CLASS` | 0.852 | 1.000 | 0.852 | 0.000 | 0.000 | 1.000 |
| `M_MINUS_PRESERVATION_CONTRACT` | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| `M_MINUS_SPECIFICATION_PRESERVATION` | 0.926 | 0.926 | 0.926 | 0.000 | 1.000 | 1.000 |
| `M_MINUS_TRANSFER_REUSE_TRACKING` | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| `M_MINUS_UNRESOLVED_TERMINAL` | 0.889 | 1.000 | 0.889 | 0.000 | 0.000 | 1.000 |
| `M_NEVER_CHANGE_REPRESENTATION` | 0.889 | 1.000 | 0.889 | 0.000 | 0.000 | 1.000 |

Each registered omission moves the column it is supposed to control:
`M_MINUS_SPECIFICATION_PRESERVATION` loses fidelity and misses every drift;
`M_MINUS_FALSE_CHANGE_PENALTY` picks up a false representation-change rate;
`M_NEVER_CHANGE_REPRESENTATION` loses the representation family;
`M_MINUS_UNRESOLVED_TERMINAL` loses the underdetermined family.
`M_MINUS_TRANSFER_REUSE_TRACKING` does **not** move, for the structural reason
recorded as a limitation in §5 of the design: the held-out target admits
independent re-invention as well as reuse, so F8 measures held-out reach rather
than reuse gain. On the protected split these are gated (G3) rather than
described, and the F8 no-carry counterfactual is printed beside the rate.

## 5. Development route

`PARENT_SUFFICIENT` — M 1.000 vs B5 1.000, paired exact p=1: no protected decision advantage over the strongest faithful federation (cost 509 vs 542 expansions, -6.1%)

Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`.

This is a development observation, not a result. It is recorded here so that the
protected outcome cannot be presented as a surprise if it agrees, or quietly
reframed if it does not.

## 6. Frozen code

| file | sha256 |
|---|---|
| `mex3_arms.py` | `6e073fea26fc327a1ea8e5f160a4164a4ff9c3785cc4105e1e7a9d4088f720a1` |
| `mex3_generator.py` | `a7febb50c3ef1bb5e106e5f3ff142c33cf825347f824478067bf02be1e78a473` |
| `mex3_lean.py` | `5160144a0d8002fc74913c229e2d988ac44c2980392bdef1e9b1fccbed608de4` |
| `mex3_model.py` | `e9d0209a747159b7b0845d1a221de072be3326da233a3349886496ad7e3af562` |
| `mex3_oracle.py` | `736003f17d2f2c44851b8b66ff56ff222384f599fb6a51bea1e369b04174129d` |
| `mex3_parents.py` | `9dab66b14ae072193ef2e6cfbc46f1531fcb85265ede0e854ec3476a9a36d459` |
| `mex3_run.py` | `9c75d73ed25b8008d3e1797655b35381337ca69cd044c9650c3ce23d9be80b86` |
| `mex3_verdict.py` | `e7e2cd8536d97ae384389fe079058c76eda7b15880326adbae21025ef00bd1e8` |

Design JSON sha256: `d13b7a7a30bb932afc899f2993dbf64ce4a15c4fb8f3041a50f48cd9c8d82ae9`
Custody seed sha256: `cb799f89499cea4a088c6df071e9ce12bff2fceb02c4adc06ab7ce4eecdbb3f8`

## Terminal

```text
PARENT_FIDELITY = PASSED
ORACLE_SELF_AGREEMENT = PASSED
PROOF_ONLY_PARENTS_MISS_ALL_SPECIFICATION_DRIFT = TRUE
F8_MEASURES_HELD_OUT_REACH_NOT_REUSE_GAIN = TRUE
PROTECTED_OUTCOMES_INSPECTED = FALSE
```
