# ME-X3 DEVELOPMENT analysis V1

- instances: 27
- results sha256: `76c07c75a6d189087768eeae6206197f07c8e82c1a5d0c621da4b19a2345856e`
- custody sha256: `c59fb4c78b0a67429ea978dc85d912399e806ea428825835e44fad5473840ac6`

**Route: PARENT_SUFFICIENT** — M 0.889 vs B5 0.889, paired exact p=1: no protected decision advantage over the strongest faithful federation (cost 520 vs 553 expansions, -6.1%)

Ladder terminal (H-EXT-3): `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`

## Outcome vector (pooled, per arm)

| arm | validity | fidelity | minimal action | terminal | joint | false change | false defer | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `A0_DIRECT` | 0.444 | 0.926 | 0.259 | 0.407 | 0.259 | 0.000 | 0.000 | 1.000 | 0.000 | 0.333 | 156.3 |
| `A1_RETRIEVAL` | 0.444 | 0.926 | 0.407 | 0.407 | 0.407 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 373.9 |
| `A2_SELF_REFLECT` | 0.296 | 0.926 | 0.259 | 0.259 | 0.259 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 271.0 |
| `A3_DISCOVER_AND_PROVE_PARENT` | 0.593 | 0.926 | 0.519 | 0.556 | 0.519 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 335.2 |
| `A4_LEMMA_ABSTRACTION_PARENT` | 0.519 | 0.926 | 0.593 | 0.481 | 0.481 | 0.000 | 0.000 | 1.000 | 0.000 | 0.333 | 621.7 |
| `B5_R1_VERDICT_ONLY` | 0.741 | 1.000 | 0.889 | 0.889 | 0.741 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 611.9 |
| `B5_R2_SATURATION` | 0.741 | 1.000 | 0.889 | 0.889 | 0.741 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 553.2 |
| `B5_R3_FRONTIER` | 0.741 | 1.000 | 0.889 | 0.889 | 0.741 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 553.2 |
| `B5_R4_SEMANTIC` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 553.2 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 553.2 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 519.6 |
| `M_MINUS_OBSTRUCTION_CLASS` | 0.889 | 1.000 | 0.741 | 0.889 | 0.741 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 545.5 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 510.4 |
| `M_MINUS_FALSE_CHANGE_PENALTY` | 0.889 | 1.000 | 0.778 | 0.889 | 0.778 | 0.111 | 0.111 | 0.000 | 0.000 | 0.333 | 516.9 |
| `M_MINUS_SPECIFICATION_PRESERVATION` | 0.889 | 0.926 | 0.815 | 0.852 | 0.815 | 0.000 | 0.111 | 1.000 | 0.000 | 0.333 | 515.4 |
| `M_MINUS_PRESERVATION_CONTRACT` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 519.6 |
| `M_MINUS_UNRESOLVED_TERMINAL` | 0.778 | 1.000 | 0.778 | 0.778 | 0.778 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 519.6 |
| `M_MINUS_TRANSFER_REUSE_TRACKING` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 548.3 |
| `M_LOCUS_LABELS_SHUFFLED` | 0.889 | 1.000 | 0.741 | 0.889 | 0.741 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 542.4 |
| `M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK` | 0.889 | 1.000 | 0.889 | 0.889 | 0.889 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 510.4 |
| `M_NEVER_CHANGE_REPRESENTATION` | 0.778 | 1.000 | 0.778 | 0.778 | 0.778 | 0.000 | 0.222 | 0.000 | 0.000 | 0.333 | 512.2 |
| `M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM` | 0.889 | 1.000 | 0.741 | 0.889 | 0.741 | 0.000 | 0.111 | 0.000 | 0.000 | 0.333 | 545.5 |
| `M_MINUS_COUNTEREXAMPLE_PROBE` | 0.741 | 1.000 | 0.778 | 0.741 | 0.741 | 0.000 | 0.222 | 0.000 | 0.000 | 0.333 | 596.5 |
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
| `F8_TRANSFER` | 6 | 0.500 | 0.500 | 0 | 0 | +0.000 | 1 | TIED |

A pooled average may not hide a family-specific failure; the table above is the primary report and the pooled row is secondary.

## F8 held-out reuse: carry versus no-carry

- M (carries its own invention): 0.333 (1/3)
- M minus transfer tracking (no carry): 0.333 (1/3)

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
| `B5_R1_VERDICT_ONLY` | 0.741 |
| `B5_R2_SATURATION` | 0.741 |
| `B5_R3_FRONTIER` | 0.741 |
| `B5_R4_SEMANTIC` | 0.889 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.889 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 0.889 |

## No-rescue clause

no threshold, family, arm or budget in this analysis may be changed after these outcomes were inspected
