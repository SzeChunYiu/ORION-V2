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
| `A4_LEMMA_ABSTRACTION_PARENT` | 0.519 | 0.926 | 0.593 | 0.481 | 1.000 | 0.000 | 0.333 | 622 |
| `B5_R1_VERDICT_ONLY` | 0.741 | 1.000 | 0.889 | 0.741 | 0.000 | 0.000 | 0.333 | 612 |
| `B5_R2_SATURATION` | 0.741 | 1.000 | 0.889 | 0.741 | 0.000 | 0.000 | 0.333 | 553 |
| `B5_R3_FRONTIER` | 0.741 | 1.000 | 0.889 | 0.741 | 0.000 | 0.000 | 0.333 | 553 |
| `B5_R4_SEMANTIC` | 0.889 | 1.000 | 0.889 | 0.889 | 0.000 | 0.000 | 0.333 | 553 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.889 | 1.000 | 0.889 | 0.889 | 0.000 | 0.000 | 0.333 | 553 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 0.889 | 1.000 | 0.889 | 0.889 | 0.000 | 0.000 | 0.333 | 520 |

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

## 4. Ablations on the development split

| arm | joint | fidelity | minimal action | false change | drift missed | held-out reuse |
|---|---|---|---|---|---|---|
| `M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK` | 0.889 | 1.000 | 0.889 | 0.000 | 0.000 | 0.333 |
| `M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM` | 0.741 | 1.000 | 0.741 | 0.000 | 0.000 | 0.333 |
| `M_LOCUS_LABELS_SHUFFLED` | 0.741 | 1.000 | 0.741 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_FALSE_CHANGE_PENALTY` | 0.778 | 1.000 | 0.778 | 0.111 | 0.000 | 0.333 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 0.889 | 1.000 | 0.889 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_OBSTRUCTION_CLASS` | 0.741 | 1.000 | 0.741 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_PRESERVATION_CONTRACT` | 0.889 | 1.000 | 0.889 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_SPECIFICATION_PRESERVATION` | 0.815 | 0.926 | 0.815 | 0.000 | 1.000 | 0.333 |
| `M_MINUS_TRANSFER_REUSE_TRACKING` | 0.889 | 1.000 | 0.889 | 0.000 | 0.000 | 0.333 |
| `M_MINUS_UNRESOLVED_TERMINAL` | 0.778 | 1.000 | 0.778 | 0.000 | 0.000 | 0.333 |
| `M_NEVER_CHANGE_REPRESENTATION` | 0.778 | 1.000 | 0.778 | 0.000 | 0.000 | 0.333 |

Each registered omission moves the column it is supposed to control:
`M_MINUS_SPECIFICATION_PRESERVATION` loses fidelity and misses every drift;
`M_MINUS_FALSE_CHANGE_PENALTY` picks up a false representation-change rate;
`M_NEVER_CHANGE_REPRESENTATION` loses the representation family;
`M_MINUS_UNRESOLVED_TERMINAL` loses the underdetermined family. On the protected
split these are gated (G3) rather than described.

## 5. Development route

`PARENT_SUFFICIENT` — M 0.889 vs B5 0.889, paired exact p=1: no protected decision advantage over the strongest faithful federation (cost 520 vs 553 expansions, -6.1%)

Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`.

This is a development observation, not a result. It is recorded here so that the
protected outcome cannot be presented as a surprise if it agrees, or quietly
reframed if it does not.

## 6. Frozen code

| file | sha256 |
|---|---|
| `mex3_arms.py` | `7d94a4c5c96473f71f89d49332b2202e8fd7a1f535f6f0f373c491cb975f0089` |
| `mex3_generator.py` | `0976ecc8b575d9f200b26e64a5a5684108619f6409daee000b13f70186b4e21a` |
| `mex3_lean.py` | `5f6b41a30c26473bf36b8ee48d29ecb93525d76d6d8d725601ee5b7d5a2703da` |
| `mex3_model.py` | `4ada65bbe31cb95ebc94fd48859473c54cdec63417f438569c4c8c53e0ec6ae0` |
| `mex3_oracle.py` | `736003f17d2f2c44851b8b66ff56ff222384f599fb6a51bea1e369b04174129d` |
| `mex3_parents.py` | `52dfbfe7bd9a4cfa802cc24dc1e7b86e4fb37fdacb281f52409f0f5ef9110fe2` |
| `mex3_run.py` | `aad0fc2291a124d7682e06f4c9a2a1f4990847f8147326b03506f4e01c810402` |
| `mex3_verdict.py` | `c8e4365fa44a1ceb7975463a0a868c7f78e072f1c9be2033641fbd035b7d8bf9` |

Design JSON sha256: `4bfc4857e750c02e4b38b33514f1847ea80dfc79451d86a59381af65af219c4a`
Custody seed sha256: `cb799f89499cea4a088c6df071e9ce12bff2fceb02c4adc06ab7ce4eecdbb3f8`

## Terminal

```text
PARENT_FIDELITY = PASSED
ORACLE_SELF_AGREEMENT = PASSED
PROOF_ONLY_PARENTS_MISS_ALL_SPECIFICATION_DRIFT = TRUE
PROTECTED_OUTCOMES_INSPECTED = FALSE
```
