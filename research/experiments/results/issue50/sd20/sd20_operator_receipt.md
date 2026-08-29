# SD20 bounded pilot — arXiv version-transition operator discovery

Population: 2067 multi-version trajectories (2933 single-version censored), 3220 transitions (train 2210 / test 1010, trajectory-level split).

## heldout_transition_prediction (mean log-score, test)

| Arm | mean log-score | Δ vs baseline | bootstrap 95% CI | CI excludes 0 |
|---|---|---|---|---|
| SIMPLE_FREQUENCY_BASELINE | -1.5714 | +0.0000 | [0.0000, 0.0000] | False |
| TEMPORAL_SEQUENCE_MODEL_PARENT | -1.6535 | -0.0821 | [-0.1021, -0.0623] | True |
| FIXED_META_LESSON_INJECTION__abstract_grows | -4.2303 | -2.6589 | [-2.7949, -2.5222] | True |
| FIXED_META_LESSON_INJECTION__authors_nondecreasing | -2.9729 | -1.4014 | [-1.4869, -1.3107] | True |
| FIXED_META_LESSON_INJECTION__gaps_lengthen | -3.1408 | -1.5694 | [-1.6542, -1.4775] | True |
| F0_META_PARENT_FEDERATION | -1.8404 | -0.2690 | [-0.3382, -0.2028] | True |

## operator_stability

Bootstrap TV distance (B=200): mean 0.0690, max 0.5668.

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

Classification: **BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM** (no terminal claim; scale-up is a re-run of the same adapters).

