# ME-X7 analysis — DEVELOPMENT

**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**

Results sha256 `fba9ddda78ca2e5b2f36dfecaf7d62daba3f82f5190f94acda8c8b789ef174aa`; custody sha256 `abbcfc5a8db92bcdff6f2410db8b29fa7d36f2ac4a357f353d6dd154663142b4`; instances 25.

## Per-arm outcomes (§6)

| arm | exact | false accept (n) | false reject (n) | misclassified | abstain on decidable (n) | missed censoring (n) | mean export | mean checks | wall ms |
|---|---|---|---|---|---|---|---|---|---|
| S0_OPAQUE_OUTPUT_ONLY | 0.080 | 21 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 1.0 | 0.0 | 0.2 |
| S1_PROVENANCE_PLUS_OUTPUT | 0.200 | 19 (21) | 0 (2) | 0 | 0 (23) | 1 (2) | 9.0 | 1.0 | 1.5 |
| S2_FULL_HUMAN_STYLE_TRACE | 0.240 | 17 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 48.0 | 2.0 | 0.3 |
| S3_PROOF_OR_CERTIFICATE_PARENT | 0.240 | 17 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 5.0 | 2.0 | 0.3 |
| L1_OUTPUT_ONLY | 0.080 | 21 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 1.0 | 0.0 | 0.1 |
| L2_PLUS_PROVENANCE | 0.200 | 19 (21) | 0 (2) | 0 | 0 (23) | 1 (2) | 9.0 | 1.0 | 1.3 |
| L3_PLUS_PROBLEM_ARTIFACT | 0.360 | 15 (21) | 0 (2) | 0 | 0 (23) | 1 (2) | 14.0 | 3.0 | 1.9 |
| L4_PLUS_VERSION_CALIBRATION_TRANSPORT | 0.600 | 10 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 18.1 | 6.0 | 1.7 |
| L5_PLUS_DEPENDENCE_ROUTE_AUTHORITY_PRESERVATION | 0.920 | 2 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 30.5 | 10.0 | 2.8 |
| L6_FULL_WITNESS | 1.000 | 0 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 43.5 | 11.0 | 2.8 |
| M_CLAIM_SUFFICIENT_WITNESS | 1.000 | 0 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 43.5 | 11.0 | 2.8 |
| M_MINUS_REGISTRY_RESOLUTION | 1.000 | 0 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 41.2 | 11.0 | 3.3 |
| M_MINUS_PROVENANCE | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 35.5 | 10.0 | 1.7 |
| M_MINUS_PROBLEM_BINDING | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 40.5 | 10.0 | 2.9 |
| M_MINUS_DEPENDENCE | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 37.5 | 10.0 | 2.1 |
| M_MINUS_ARTIFACT | 0.760 | 0 (21) | 0 (2) | 0 | 6 (23) | 0 (2) | 41.5 | 9.0 | 3.1 |
| M_MINUS_ASSUMPTION_VERSION | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 41.5 | 10.0 | 2.8 |
| M_MINUS_CALIBRATION | 0.880 | 0 (21) | 0 (2) | 0 | 3 (23) | 0 (2) | 43.0 | 10.0 | 3.6 |
| M_MINUS_TRANSPORT | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 41.9 | 10.0 | 2.8 |
| M_MINUS_ROUTE_LEDGER | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 40.6 | 10.0 | 3.0 |
| M_MINUS_EVALUATOR_CONTRACT | 0.920 | 2 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 30.5 | 10.0 | 3.3 |
| M_MINUS_AUTHORITY_CEILING | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 41.5 | 10.0 | 3.2 |
| M_MINUS_PRESERVATION | 0.840 | 0 (21) | 0 (2) | 0 | 4 (23) | 0 (2) | 41.9 | 10.0 | 3.1 |
| B5_STRONGEST_FAITHFUL_AUDIT_PARENT | 1.000 | 0 (21) | 0 (2) | 0 | 0 (23) | 0 (2) | 43.5 | 11.0 | 3.2 |
| A0_PROOF_CERTIFICATE_ONLY | 0.160 | 19 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 3.0 | 1.0 | 0.2 |
| A1_PROVENANCE_ONLY | 0.160 | 19 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 9.0 | 1.0 | 0.9 |
| A2_REPLAY_ONLY | 0.160 | 19 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 5.0 | 1.0 | 0.2 |
| A3_ASSURANCE_CASE | 0.160 | 18 (21) | 0 (2) | 1 | 0 (23) | 2 (2) | 9.5 | 2.0 | 0.9 |
| A4_DEPENDENCE_AUDIT | 0.160 | 19 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 7.0 | 1.0 | 0.5 |
| A5_CALIBRATED_ABSTENTION | 0.120 | 19 (21) | 0 (2) | 0 | 2 (23) | 1 (2) | 9.0 | 1.0 | 0.9 |
| C_ALWAYS_ACCEPT | 0.080 | 21 (21) | 0 (2) | 0 | 0 (23) | 2 (2) | 1.0 | 0.0 | 0.0 |
| C_ALWAYS_CANNOT_CHECK | 0.080 | 0 (21) | 0 (2) | 0 | 23 (23) | 0 (2) | 1.0 | 0.0 | 0.0 |
| C_RANDOM_VERDICT | 0.120 | 13 (21) | 0 (2) | 4 | 5 (23) | 0 (2) | 1.0 | 0.0 | 0.1 |

## Detection recall by failure class (n evaluated in brackets)

| class | S0_OPAQUE_OUTPUT_ONLY | S1_PROVENANCE_PLUS_OUTPUT | S2_FULL_HUMAN_STYLE_TRACE | S3_PROOF_OR_CERTIFICATE_PARENT | L6_FULL_WITNESS | M_CLAIM_SUFFICIENT_WITNESS | M_MINUS_REGISTRY_RESOLUTION | M_MINUS_PROVENANCE | M_MINUS_PROBLEM_BINDING | M_MINUS_DEPENDENCE | M_MINUS_ARTIFACT | M_MINUS_ASSUMPTION_VERSION | M_MINUS_CALIBRATION | M_MINUS_TRANSPORT | M_MINUS_ROUTE_LEDGER | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_AUTHORITY_CEILING | M_MINUS_PRESERVATION | B5_STRONGEST_FAITHFUL_AUDIT_PARENT | A0_PROOF_CERTIFICATE_ONLY | A1_PROVENANCE_ONLY | A2_REPLAY_ONLY | A3_ASSURANCE_CASE | A4_DEPENDENCE_AUDIT | A5_CALIBRATED_ABSTENTION | C_ALWAYS_ACCEPT | C_ALWAYS_CANNOT_CHECK | C_RANDOM_VERDICT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WRONG_PROBLEM_OR_SPECIFICATION | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| STALE_OR_WRONG_SOURCE | 0.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| HIDDEN_DEPENDENCE | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| CODE_OR_PROOF_MISMATCH | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| SEED_OR_VERSION_MISMATCH | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| INVALID_CALIBRATION | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 0.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.00 (1) |
| INVALID_TRANSPORT | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| OMITTED_FAILED_ROUTE | 0.00 (2) | 0.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| EVALUATOR_BLIND_SPOT | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| AUTHORITY_OVERREACH | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |
| REPRESENTATION_CHANGE_LOSES_INFORMATION | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 1.00 (2) | 0.00 (2) | 1.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) | 0.00 (2) |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True, n_evaluated=31 — hand-authored fixture per applicable (stratum, mode) cell, the P/Q separation pair and the planted positives are reproduced in the selftest report
- **G0b_ORACLE_SELF_AGREEMENT**: pass=True, n_evaluated=25 — direct rule == exhaustive enumeration; the planter's declared defect == the full-structure recomputation (exactly one INVALID check, no censoring); the arms' independent module implementation == the oracle's check table at full visibility
- **G0c_NULL_CALIBRATION**: pass=True, n_evaluated=21 — the degenerate always-accept and always-abstain controls score 0 where their answer is wrong; random and shuffled-label nulls stay under the ceiling
- **G1a_B5_REPRODUCES_M**: pass=True, n_evaluated=25 — identical exact-match indicator on >= 99.5% of instances and no cell above 5% discordant
- **G1b_M_ADVANTAGE**: pass=False, n_evaluated=25 — paired exact-match difference M - B5 > 0, exact two-sided p <= 0.05, and at least one cell with >= 5 M-only-exact instances
- **G1c_B5_AHEAD**: pass=False, n_evaluated=25 — its own positive test, not the negation of G1b: paired difference M - B5 < 0 with exact two-sided p <= 0.05
- **G2_ANTI_CONSERVATISM**: pass=True, n_evaluated=2 — on fully warranted episodes M must not refuse or abstain more often than B5
- **G3_MECHANISM_BY_OMISSION**: pass=True, n_evaluated=21 — for every injection class, the set of field omissions that lower its detection recall equals exactly the set of fields its check requires (FIELD_FOR_CLASS is the designated member); no other omission blinds it
- **G4_INTERFACE_LADDER**: pass=True, n_evaluated=25 — no rung k+1 significantly worse than rung k (rung k+1's fields contain rung k's, so a reversal is a lane defect of the surface definitions, not a finding)
- **G5_SUFFICIENCY**: pass=True, n_evaluated=5 — 
- **G6_CROSS_MODE_TRANSFER**: pass=True, n_evaluated=25 — the ladder is monotone and M is non-inferior to B5 separately in each epistemic mode (protocol §10: results that fail to transfer across a second mode are killed)
  - S1_FAILURE_CLASS_PRESERVATION: pass=True, n_evaluated=21
  - S2_REPLAY_SUPPORT: pass=True, n_evaluated=25
  - S3_SELECTIVE_REOPENING_WITHOUT_HIDDEN_HISTORY: pass=True, n_evaluated=5
  - S4_FALSE_ACCEPTANCE_NONINFERIORITY: pass=True, n_evaluated=21
  - S5_PREFERABLE_TO_FULL_TRACE: pass=True, n_evaluated=25

## Route

`PARENT_SUFFICIENT` — the federation is matched, and the compact witness meets every sufficiency conjunct. Witness terminal: `WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT`. Cost: `COST_COMPARABLE`.
