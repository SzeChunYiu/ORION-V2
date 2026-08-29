# SD20 bounded pilot — arXiv version-transition operator discovery

Population: 2067 multi-version trajectories (2933 single-version censored), 3220 transitions (train 2210 / test 1010, trajectory-level split).

Variant run: `--alphabet coarse9`, `--context category` (revival pass; fixed-lesson and F0 arms are skipped on variant alphabets, recorded in skipped_arms).

## heldout_transition_prediction (mean log-score, test)

| Arm | mean log-score | Δ vs baseline | bootstrap 95% CI | CI excludes 0 |
|---|---|---|---|---|
| SIMPLE_FREQUENCY_BASELINE | -1.1877 | +0.0000 | [0.0000, 0.0000] | False |
| TEMPORAL_SEQUENCE_MODEL_PARENT | -1.1951 | -0.0073 | [-0.0206, 0.0062] | False |

## operator_stability

Bootstrap TV distance (B=200): mean 0.0504, max 0.4643.

## cross_domain_support

| Category | n_test | LOO Δ vs baseline | CI excludes 0 |
|---|---|---|---|
| astro-ph | 178 | +0.0000 | False |
| cond-mat | 218 | +0.0000 | False |
| cs | 1114 | +0.0000 | False |
| econ | 35 | +0.0000 | False |
| eess | 108 | +0.0000 | False |
| gr-qc | 77 | +0.0000 | False |
| hep-ex | 13 | +0.0000 | False |
| hep-lat | 13 | +0.0000 | False |
| hep-ph | 102 | +0.0000 | False |
| hep-th | 68 | +0.0000 | False |
| math | 806 | +0.0000 | False |
| math-ph | 13 | +0.0000 | False |
| nlin | 12 | +0.0000 | False |
| nucl-ex | 1 | TOO_FEW | — |
| nucl-th | 8 | TOO_FEW | — |
| physics | 162 | +0.0000 | False |
| q-bio | 39 | +0.0000 | False |
| q-fin | 26 | +0.0000 | False |
| quant-ph | 148 | +0.0000 | False |
| stat | 79 | +0.0000 | False |

LOO beats baseline in 0 / 18 evaluated categories.

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

