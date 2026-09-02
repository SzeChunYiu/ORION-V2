# ME-X7 analysis — PROTECTED

Results sha256 `45315747f5539d469ea9c82510139c2240a58bdb544944c13fcc00f45e10dcb0`; custody sha256 `5e26e0bb024ba038f3c69b99eebc6cbff79e7cd9fe999ac6490da557e58eb3c2`; instances 1250.

## Per-arm outcomes (§6)

| arm | exact | false accept (n) | false reject (n) | misclassified | abstain on decidable (n) | missed censoring (n) | mean export | mean checks | wall ms |
|---|---|---|---|---|---|---|---|---|---|
| S0_OPAQUE_OUTPUT_ONLY | 0.080 | 1050 (1050) | 0 (100) | 0 | 0 (1150) | 100 (100) | 1.0 | 0.0 | 5.9 |
| S1_PROVENANCE_PLUS_OUTPUT | 0.174 | 950 (1050) | 0 (100) | 0 | 0 (1150) | 83 (100) | 9.0 | 1.0 | 9.9 |
| S2_FULL_HUMAN_STYLE_TRACE | 0.247 | 850 (1050) | 0 (100) | 0 | 0 (1150) | 91 (100) | 45.4 | 2.0 | 11.1 |
| S3_PROOF_OR_CERTIFICATE_PARENT | 0.242 | 850 (1050) | 0 (100) | 0 | 0 (1150) | 98 (100) | 5.0 | 2.0 | 8.8 |
| L1_OUTPUT_ONLY | 0.080 | 1050 (1050) | 0 (100) | 0 | 0 (1150) | 100 (100) | 1.0 | 0.0 | 3.7 |
| L2_PLUS_PROVENANCE | 0.174 | 950 (1050) | 0 (100) | 0 | 0 (1150) | 83 (100) | 9.0 | 1.0 | 8.2 |
| L3_PLUS_PROBLEM_ARTIFACT | 0.342 | 750 (1050) | 0 (100) | 0 | 0 (1150) | 73 (100) | 14.0 | 3.0 | 20.0 |
| L4_PLUS_VERSION_CALIBRATION_TRANSPORT | 0.557 | 500 (1050) | 0 (100) | 0 | 0 (1150) | 54 (100) | 18.2 | 6.0 | 20.9 |
| L5_PLUS_DEPENDENCE_ROUTE_AUTHORITY_PRESERVATION | 0.904 | 100 (1050) | 0 (100) | 0 | 0 (1150) | 20 (100) | 30.7 | 10.0 | 61.0 |
| L6_FULL_WITNESS | 0.995 | 0 (1050) | 0 (100) | 0 | 0 (1150) | 6 (100) | 43.7 | 11.0 | 58.8 |
| M_CLAIM_SUFFICIENT_WITNESS | 0.995 | 0 (1050) | 0 (100) | 0 | 0 (1150) | 6 (100) | 43.7 | 11.0 | 58.5 |
| M_MINUS_REGISTRY_RESOLUTION | 0.953 | 53 (1050) | 0 (100) | 0 | 0 (1150) | 6 (100) | 41.5 | 11.0 | 63.7 |
| M_MINUS_PROVENANCE | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 35.7 | 10.0 | 54.0 |
| M_MINUS_PROBLEM_BINDING | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 40.7 | 10.0 | 51.2 |
| M_MINUS_DEPENDENCE | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 37.6 | 10.0 | 28.7 |
| M_MINUS_ARTIFACT | 0.760 | 0 (1050) | 0 (100) | 0 | 300 (1150) | 0 (100) | 41.7 | 9.0 | 51.8 |
| M_MINUS_ASSUMPTION_VERSION | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 41.7 | 10.0 | 56.2 |
| M_MINUS_CALIBRATION | 0.875 | 0 (1050) | 0 (100) | 0 | 150 (1150) | 6 (100) | 43.2 | 10.0 | 55.7 |
| M_MINUS_TRANSPORT | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 42.1 | 10.0 | 55.7 |
| M_MINUS_ROUTE_LEDGER | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 40.8 | 10.0 | 56.2 |
| M_MINUS_EVALUATOR_CONTRACT | 0.904 | 100 (1050) | 0 (100) | 0 | 0 (1150) | 20 (100) | 30.7 | 10.0 | 55.3 |
| M_MINUS_AUTHORITY_CEILING | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 41.7 | 10.0 | 56.1 |
| M_MINUS_PRESERVATION | 0.835 | 0 (1050) | 0 (100) | 0 | 200 (1150) | 6 (100) | 42.1 | 10.0 | 51.8 |
| B5_STRONGEST_FAITHFUL_AUDIT_PARENT | 0.995 | 0 (1050) | 0 (100) | 0 | 0 (1150) | 6 (100) | 43.7 | 11.0 | 134.8 |
| A0_PROOF_CERTIFICATE_ONLY | 0.160 | 950 (1050) | 0 (100) | 0 | 0 (1150) | 100 (100) | 3.0 | 1.0 | 7.8 |
| A1_PROVENANCE_ONLY | 0.160 | 950 (1050) | 0 (100) | 0 | 0 (1150) | 100 (100) | 9.0 | 1.0 | 39.9 |
| A2_REPLAY_ONLY | 0.166 | 950 (1050) | 0 (100) | 0 | 0 (1150) | 92 (100) | 5.0 | 1.0 | 7.1 |
| A3_ASSURANCE_CASE | 0.160 | 900 (1050) | 0 (100) | 50 | 0 (1150) | 100 (100) | 9.5 | 2.0 | 39.7 |
| A4_DEPENDENCE_AUDIT | 0.160 | 950 (1050) | 0 (100) | 0 | 0 (1150) | 100 (100) | 7.1 | 1.0 | 24.1 |
| A5_CALIBRATED_ABSTENTION | 0.094 | 950 (1050) | 0 (100) | 0 | 100 (1150) | 83 (100) | 9.0 | 1.0 | 37.8 |
| C_ALWAYS_ACCEPT | 0.080 | 1050 (1050) | 0 (100) | 0 | 0 (1150) | 100 (100) | 1.0 | 0.0 | 1.9 |
| C_ALWAYS_CANNOT_CHECK | 0.080 | 0 (1050) | 0 (100) | 0 | 1150 (1150) | 0 (100) | 1.0 | 0.0 | 1.5 |
| C_RANDOM_VERDICT | 0.083 | 348 (1050) | 38 (100) | 310 | 386 (1150) | 64 (100) | 1.0 | 0.0 | 2.7 |

## Detection recall by failure class (n evaluated in brackets)

| class | S0_OPAQUE_OUTPUT_ONLY | S1_PROVENANCE_PLUS_OUTPUT | S2_FULL_HUMAN_STYLE_TRACE | S3_PROOF_OR_CERTIFICATE_PARENT | L6_FULL_WITNESS | M_CLAIM_SUFFICIENT_WITNESS | M_MINUS_REGISTRY_RESOLUTION | M_MINUS_PROVENANCE | M_MINUS_PROBLEM_BINDING | M_MINUS_DEPENDENCE | M_MINUS_ARTIFACT | M_MINUS_ASSUMPTION_VERSION | M_MINUS_CALIBRATION | M_MINUS_TRANSPORT | M_MINUS_ROUTE_LEDGER | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_AUTHORITY_CEILING | M_MINUS_PRESERVATION | B5_STRONGEST_FAITHFUL_AUDIT_PARENT | A0_PROOF_CERTIFICATE_ONLY | A1_PROVENANCE_ONLY | A2_REPLAY_ONLY | A3_ASSURANCE_CASE | A4_DEPENDENCE_AUDIT | A5_CALIBRATED_ABSTENTION | C_ALWAYS_ACCEPT | C_ALWAYS_CANNOT_CHECK | C_RANDOM_VERDICT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WRONG_PROBLEM_OR_SPECIFICATION | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.02 (100) |
| STALE_OR_WRONG_SOURCE | 0.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 0.79 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.07 (100) |
| HIDDEN_DEPENDENCE | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 0.68 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.02 (100) |
| CODE_OR_PROOF_MISMATCH | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.07 (100) |
| SEED_OR_VERSION_MISMATCH | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.05 (100) |
| INVALID_CALIBRATION | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 0.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 1.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.00 (50) | 0.04 (50) |
| INVALID_TRANSPORT | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.04 (100) |
| OMITTED_FAILED_ROUTE | 0.00 (100) | 0.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.02 (100) |
| EVALUATOR_BLIND_SPOT | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.03 (100) |
| AUTHORITY_OVERREACH | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.01 (100) |
| REPRESENTATION_CHANGE_LOSES_INFORMATION | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 1.00 (100) | 0.00 (100) | 1.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.00 (100) | 0.01 (100) |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True, n_evaluated=31 — hand-authored fixture per applicable (stratum, mode) cell, the P/Q separation pair and the planted positives are reproduced in the selftest report
- **G0b_ORACLE_SELF_AGREEMENT**: pass=False, n_evaluated=1250 — direct rule == exhaustive enumeration; the planter's declared defect == the full-structure recomputation (exactly one INVALID check, no censoring); the arms' independent module implementation == the oracle's check table at full visibility
- **G0c_NULL_CALIBRATION**: pass=True, n_evaluated=1050 — the degenerate always-accept and always-abstain controls score 0 where their answer is wrong; random and shuffled-label nulls stay under the ceiling
- **G1a_B5_REPRODUCES_M**: pass=True, n_evaluated=1250 — identical exact-match indicator on >= 99.5% of instances and no cell above 5% discordant
- **G1b_M_ADVANTAGE**: pass=False, n_evaluated=1250 — paired exact-match difference M - B5 > 0, exact two-sided p <= 0.05, and at least one cell with >= 5 M-only-exact instances
- **G1c_B5_AHEAD**: pass=False, n_evaluated=1250 — its own positive test, not the negation of G1b: paired difference M - B5 < 0 with exact two-sided p <= 0.05
- **G2_ANTI_CONSERVATISM**: pass=True, n_evaluated=100 — on fully warranted episodes M must not refuse or abstain more often than B5
- **G3_MECHANISM_BY_OMISSION**: pass=True, n_evaluated=1050 — for every injection class, the set of field omissions that lower its detection recall equals exactly the set of fields its check requires (FIELD_FOR_CLASS is the designated member); no other omission blinds it
- **G4_INTERFACE_LADDER**: pass=True, n_evaluated=1250 — no rung k+1 significantly worse than rung k (rung k+1's fields contain rung k's, so a reversal is a lane defect of the surface definitions, not a finding)
- **G5_SUFFICIENCY**: pass=False, n_evaluated=250 — 
- **G6_CROSS_MODE_TRANSFER**: pass=True, n_evaluated=1250 — the ladder is monotone and M is non-inferior to B5 separately in each epistemic mode (protocol §10: results that fail to transfer across a second mode are killed)
- **G7_WITNESS_SELF_CONTAINMENT**: pass=True, n_evaluated=53 — a positive test with its own denominator: on undeclared-upstream episodes the identity-exporting witness is strictly more exact than the self-contained one, and the two are identical on every other episode — so the separation is the mechanism, not a rate. Zero such episodes reports CANNOT_CHECK, never a pass.
  - S1_FAILURE_CLASS_PRESERVATION: pass=True, n_evaluated=1050
  - S2_REPLAY_SUPPORT: pass=False, n_evaluated=1250
  - S3_SELECTIVE_REOPENING_WITHOUT_HIDDEN_HISTORY: pass=True, n_evaluated=250
  - S4_FALSE_ACCEPTANCE_NONINFERIORITY: pass=True, n_evaluated=1050
  - S5_PREFERABLE_TO_FULL_TRACE: pass=True, n_evaluated=1250

## Registered-mechanism coverage

- all registered mechanisms exercised: **True**
- never exercised — censor_variants: none
- never exercised — cells: none
- never exercised — loci: none

M/B5 implementation agreement (distinct code on C_SOURCE_STATUS, C_DEPENDENCE, C_ENV_IDENTITY, C_PRESERVATION): C_SPEC_BINDING 1250/1250, C_SOURCE_STATUS 1250/1250, C_DEPENDENCE 1250/1250, C_ARTIFACT_DIGEST 1250/1250, C_ENV_IDENTITY 1250/1250, C_CALIBRATION 1250/1250, C_TRANSPORT 1250/1250, C_ROUTE_COMPLETENESS 1250/1250, C_EVALUATOR_COVERAGE 1250/1250, C_AUTHORITY 1250/1250, C_PRESERVATION 1250/1250


## Route

`CANNOT_CHECK` — a hard G0 gate failed — lane defect; repair, re-freeze, no arm verdict. Witness terminal: `NONE`. Cost: `COST_ADVANTAGE_M`.
