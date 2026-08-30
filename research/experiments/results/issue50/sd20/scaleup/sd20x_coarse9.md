# SD20 bounded pilot — arXiv version-transition operator discovery

Population: 19961 multi-version trajectories (25039 single-version censored), 31070 transitions (train 21595 / test 9475, trajectory-level split).

Variant run: `--alphabet coarse9`, `--context default` (revival pass; fixed-lesson and F0 arms are skipped on variant alphabets, recorded in skipped_arms).

## heldout_transition_prediction (mean log-score, test)

| Arm | mean log-score | Δ vs baseline | bootstrap 95% CI | CI excludes 0 |
|---|---|---|---|---|
| SIMPLE_FREQUENCY_BASELINE | -1.2048 | +0.0000 | [0.0000, 0.0000] | False |
| TEMPORAL_SEQUENCE_MODEL_PARENT | -1.1980 | +0.0068 | [0.0032, 0.0099] | True |

## operator_stability

Bootstrap TV distance (B=200): mean 0.0500, max 0.4724.

## cross_domain_support

| Category | n_test | LOO Δ vs baseline | CI excludes 0 |
|---|---|---|---|
| astro-ph | 1323 | +0.0000 | False |
| cond-mat | 1886 | +0.0000 | False |
| cs | 13869 | +0.0000 | False |
| econ | 280 | +0.0000 | False |
| eess | 1011 | +0.0000 | False |
| gr-qc | 617 | +0.0000 | False |
| hep-ex | 164 | +0.0000 | False |
| hep-lat | 66 | +0.0000 | False |
| hep-ph | 744 | +0.0000 | False |
| hep-th | 630 | +0.0000 | False |
| math | 5777 | +0.0000 | False |
| math-ph | 164 | +0.0000 | False |
| nlin | 93 | +0.0000 | False |
| nucl-ex | 42 | +0.0000 | False |
| nucl-th | 120 | +0.0000 | False |
| physics | 1457 | +0.0000 | False |
| q-bio | 294 | +0.0000 | False |
| q-fin | 144 | +0.0000 | False |
| quant-ph | 1485 | +0.0000 | False |
| stat | 904 | +0.0000 | False |

LOO beats baseline in 0 / 20 evaluated categories.

## failed_trajectory_explanation

**CANNOT_CHECK** — outcome-censored corpus; no failed-trajectory labels exist and none are invented.

## CANNOT_CHECK_ON_SLICE arms

- BIBLIOMETRIC_SCIENCE_OF_SCIENCE_PARENT: Atom metadata carries no citation/fame fields on this slice
- NETWORK_SCIENCE_PARENT: no disambiguated author network in the inputs (SD10 CANNOT_CHECK)
- CAUSAL_OR_QUASI_EXPERIMENTAL_PARENT_WHEN_IDENTIFIABLE: no interventions or quasi-experimental variation in version deposits
- F2_RECURSIVE_SCIENTIFIC_DEVELOPMENT_FULL: recursive promotion requires SD50 machinery; bounded pilot has one level

## SKIPPED_ALPHABET_VARIANT arms

- FIXED_META_LESSON_INJECTION__abstract_grows: defined on the 27-cell default alphabet only; not re-encoded on a variant cell space
- FIXED_META_LESSON_INJECTION__authors_nondecreasing: defined on the 27-cell default alphabet only; not re-encoded on a variant cell space
- FIXED_META_LESSON_INJECTION__gaps_lengthen: defined on the 27-cell default alphabet only; not re-encoded on a variant cell space
- F0_META_PARENT_FEDERATION: pools the fixed lessons; skipped with them on variant alphabets

Classification: **BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM** (no terminal claim; scale-up is a re-run of the same adapters).

