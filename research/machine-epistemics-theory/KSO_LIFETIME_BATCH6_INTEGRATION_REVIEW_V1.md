# Lifetime batch 6: integration corrections

The source is ORION-V2 PR #347, commit
`6b7ef9bfdc7b769b7783f6768f45e58a91dff2bb`, imported before integration.
The original 14 tests passed; 11 additional
regression cases failed. The corrected 30-case suite passes. This is a finite
reference study, not a protected runtime result or independent scientific review.

| Finding | Correction | Limit |
|---|---|---|
| A chain extension with an invented adoption predecessor was accepted. | Validate every component predecessor against replayed lineage. | Hash-chain continuity still assumes collision resistance and a trusted starting checkpoint. |
| Commitment attribution ignored the supplied commitment head. | Require an actual chain head at or after the starting checkpoint; resolve evidence at that prefix. | New post-checkpoint evidence is not retroactively classified as pre-checkpoint evidence. |
| A single successful guess was treated as proof of undisclosed information. | The counting bound requires guaranteed zero-error identification over the whole registered target class. Ordinary observed success yields `IDENTIFICATION_NOT_ESTABLISHED`. | A caller-declared guarantee is a theorem hypothesis, not an attestation. |
| Both directional sign-test decisions used the full significance budget. | Use twice the smaller exact tail for the bidirectional decision. | Predesignated one-sided tests retain their one-sided threshold. |
| Exchangeability alone was described as sufficient for binomial inference. | Require independent fair discordant signs under the null or a separately justified randomization distribution. | The one-latent-coin counterexample is exchangeable and still invalidates item-level inference. |
| Empty observations manufactured one lifetime; malformed block models crashed or truncated. | Return zero units / `CANNOT_CHECK`; reject nonintegral partitions; zero rejection region has zero size. | Distinct seeds alone do not certify independence; the design must establish it. |
| Graded antichains were described too broadly as a scalar semiring homomorphism. | Keep source-indexed monomials. Shared evidence obeys `e tensor e = e`, but a scalar grade in `(0,1)` does not obey `g*g = g`. | Exact retraction and absorption remain valid; probabilistic interpretation needs a separate dependence model. |
| An unavailable ceiling oracle was equated with a nonexistent mathematical minimum. | State only the behavior of the registered sequential algorithm. | Another algorithm may compute the minimum; higher-level ceilings remain open. |

The duplicate-ordering example retains its original selected-tail numbers as a
description of the erroneous procedure. Valid two-sided values are `1/2`, `1/8`,
and `1/32`; three copies still cross 0.05 without adding independent information.
The claim direction must not be chosen after seeing the sign and then tested as
though it were predeclared. The distinction between greater/less/two-sided
alternatives follows the [official SciPy binomial-test specification](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html).
The finite-class argument here is elementary counting over 16 truth tables; it
does not estimate model training exposure or make accusations from correct answers.

Verification:

```bash
python -m pytest tests/unit/test_kso_lifetime_prereqs_batch6.py tests/unit/test_kso_lifetime_revision_boundaries.py
python research/machine-epistemics-theory/kso_lifetime_prereqs_batch6_exact.py
```

Independent follow-up also corrected declared side-channel capacity, non-power-of-two ceil-log2 rounding, reference/upper-bound wording, and fail-closed behavior when Python assertions are disabled.

Runtime absorption is separately reviewed in ORION-OCM. Historical study results
and the old protected task stream are not fresh evidence for this revision.
