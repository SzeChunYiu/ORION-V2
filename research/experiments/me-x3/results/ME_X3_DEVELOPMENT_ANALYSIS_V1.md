# ME-X3 DEVELOPMENT analysis V1

- instances: 27
- results sha256: `81c390465aeb9a305fa4d09b8f4b933851c19d76b20de907f6dd9f77ec8b97a5`
- custody sha256: `be4e1b47e9289e51f336662f788f5773fd32c2fcfa9a564812e594207b33e38f`

**Route: PARENT_SUFFICIENT** — M 1.000 vs B5 1.000, paired exact p=1: no protected decision advantage over the strongest faithful federation (cost 509 vs 542 expansions, -6.1%)

Ladder terminal (H-EXT-3): `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`

## Outcome vector (pooled, per arm)

| arm | validity | fidelity | minimal action | terminal | joint | false change | false defer | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `A0_DIRECT` | 0.444 | 0.926 | 0.259 | 0.407 | 0.259 | 0.000 | 0.000 | 1.000 | 0.000 | 0.333 | 156.3 |
| `A1_RETRIEVAL` | 0.444 | 0.926 | 0.407 | 0.407 | 0.407 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 373.9 |
| `A2_SELF_REFLECT` | 0.296 | 0.926 | 0.259 | 0.259 | 0.259 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 271.0 |
| `A3_DISCOVER_AND_PROVE_PARENT` | 0.593 | 0.926 | 0.519 | 0.556 | 0.519 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 335.2 |
| `A4_LEMMA_ABSTRACTION_PARENT` | 0.630 | 0.926 | 0.593 | 0.593 | 0.593 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 653.0 |
| `B5_R1_VERDICT_ONLY` | 0.852 | 1.000 | 1.000 | 1.000 | 0.852 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 645.7 |
| `B5_R2_SATURATION` | 0.852 | 1.000 | 1.000 | 1.000 | 0.852 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 541.6 |
| `B5_R3_FRONTIER` | 0.852 | 1.000 | 1.000 | 1.000 | 0.852 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 541.6 |
| `B5_R4_SEMANTIC` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 541.6 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 541.6 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 508.6 |
| `M_MINUS_OBSTRUCTION_CLASS` | 1.000 | 1.000 | 0.852 | 1.000 | 0.852 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 569.9 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 499.3 |
| `M_MINUS_FALSE_CHANGE_PENALTY` | 1.000 | 1.000 | 0.889 | 1.000 | 0.889 | 0.111 | 0.000 | 0.000 | 0.000 | 1.000 | 505.8 |
| `M_MINUS_SPECIFICATION_PRESERVATION` | 1.000 | 0.926 | 0.926 | 0.963 | 0.926 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 504.4 |
| `M_MINUS_PRESERVATION_CONTRACT` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 508.6 |
| `M_MINUS_UNRESOLVED_TERMINAL` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 508.6 |
| `M_MINUS_TRANSFER_REUSE_TRACKING` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 601.2 |
| `M_LOCUS_LABELS_SHUFFLED` | 1.000 | 1.000 | 0.852 | 1.000 | 0.852 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 566.8 |
| `M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 499.3 |
| `M_NEVER_CHANGE_REPRESENTATION` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 1.000 | 501.2 |
| `M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM` | 1.000 | 1.000 | 0.852 | 1.000 | 0.852 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 569.9 |
| `M_MINUS_COUNTEREXAMPLE_PROBE` | 0.852 | 1.000 | 0.889 | 0.852 | 0.852 | 0.000 | 0.111 | 0.000 | 0.000 | 1.000 | 625.3 |
| `M_MINUS_LEMMA_INVENTION` | 0.889 | 1.000 | 0.815 | 0.889 | 0.815 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 376.5 |
| `M_MINUS_LEMMA_LEVEL` | 0.815 | 1.000 | 0.667 | 0.815 | 0.667 | 0.000 | 0.185 | 0.000 | 0.000 | 0.333 | 199.7 |

## Per family: M vs B5 (paired, exact binomial)

| family | n | M joint | B5 joint | M-only | B5-only | diff | exact p | route |
|---|---|---|---|---|---|---|---|---|
| `F1_DIRECT_SEARCH` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F2_MISSING_LEMMA` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F3_REPRESENTATION_CHANGE` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F4_DECEPTIVE_CHANGE` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F5_PROBE_OR_COUNTEREXAMPLE_NEEDED` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F6_UNDERDETERMINED_OR_CANNOT_CHECK` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F7_SPECIFICATION_MISMATCH` | 3 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F8_TRANSFER` | 6 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |

A pooled average may not hide a family-specific failure; the table above is the primary report and the pooled row is secondary.

## F7 by registered drift subtype (realized draw)

| subtype | n | M fidelity | B5 fidelity | A0 fidelity | M drift missed | M false drift alarm |
|---|---|---|---|---|---|---|
| `ABSTRACTION_ELEVATION` | 1 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| `FAITHFUL` | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| `MATERIALLY_WEAKENED` | 1 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 |

Counts are the realized draw after oracle-verified rejection sampling, not the generator's proposal weights.

## F8 held-out reuse: carry versus no-carry

- M (carries its own invention): 1.000 (3/3)
- M minus transfer tracking (no carry): 1.000 (3/3)

The held-out target admits independent re-invention from the registered candidate pool as well as reuse of the source artefact, so a difference of zero here is the expected reading and F8 does not support a strong reusability claim. The counterfactual is printed so that this is visible rather than inferred from a passing rate.

## Gates

| gate | pass | note |
|---|---|---|
| G0 | PASS | oracle self-agreement, known-answer fixtures, parent fidelity, null calibration |
| G1 | FAIL | M is compared with the TOP-RUNG federation, which receives exactly what M receives; the ladder is a property of the federation's internal channel, never of M's privilege |
| G2 | PASS | M may not buy accuracy by escalating or deferring more than B5 |
| G3 | PASS | a mechanism claim requires the named omission to break the exact behaviour it is supposed to control |
| G4 | PASS | H-EXT-3: what crosses the federation's module boundary |

## H-EXT-3 interface ladder

| rung | joint rate |
|---|---|
| `B5_R1_VERDICT_ONLY` | 0.852 |
| `B5_R2_SATURATION` | 0.852 |
| `B5_R3_FRONTIER` | 0.852 |
| `B5_R4_SEMANTIC` | 1.000 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 1.000 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 1.000 |

## No-rescue clause

no threshold, family, arm or budget in this analysis may be changed after these outcomes were inspected
