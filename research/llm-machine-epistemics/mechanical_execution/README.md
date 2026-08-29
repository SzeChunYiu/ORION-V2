# Mechanical Execution — audit scripts and receipts (issue #51)

Exact-arithmetic theorem audits for the LLM Machine Epistemics lane.
Shared library: `llm_epistemics_common.py` (prime-exponent log-linear algebra
over Fractions as implementation A, Decimal >=110 digits as implementation B;
agreement tolerance 1e-30; structural checks pure integer arithmetic).

## Batch 1 — static layer (landed 2026-08-29)

| Script | Spec | Output (out/) | Verdict |
|---|---|---|---|
| `llm_epistemics_partition_audit.py` | V4 §3 | `PARTITION_ENUMERATION_RECEIPT_V1.json` | PASS — Bell-complete n=1..7; L1 refines S_P; T2a minimal block count; T2b equal-count iso |
| `llm_epistemics_selector_audit.py` | V4 §4 + RDQ_V2 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | PASS — R21-R27 all exact; §5.2 tie fixture; R26 witness frozen (joint 1 bit < 2 bits individual sum) |
| `llm_epistemics_deficit_audit.py` | V4 §10 | `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json` | PASS — D1/D2/D3 identities exact over 900 randomized rational worlds; controls C1-C5 exact |

## Re-run (billy-old)

```bash
cd /tmp/i51_lane  # or this directory
python3 llm_epistemics_partition_audit.py --n-max 7 --output out/PARTITION_ENUMERATION_RECEIPT_V1.json
nohup python3 llm_epistemics_selector_audit.py --seed 20260829 --trials 300 --samples 2000 --output out/RESPONSIBILITY_SELECTOR_AUDIT_V1.json &
python3 llm_epistemics_deficit_audit.py --seed 20260829 --trials 300 --output out/EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json
```

Exit code 0 = PASS/CANNOT_CHECK; 3 = FAIL_COUNTEREXAMPLE_FOUND.

Verdict vocabulary is fixed by MECHANICAL_EXECUTION_SPEC_V4/V5: PASS,
FAIL_COUNTEREXAMPLE_FOUND, CANNOT_CHECK_* — nothing else.


## Batch 2 — dynamic layer, universality, log-loss benchmark (2026-08-29)

| Script | Spec | Output (out/) | Verdict |
|---|---|---|---|
| `llm_epistemics_dynamic_phase_audit.py` | V4 §5–§7 + V5 phases | `DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json`, `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json`, `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json`, `RESPONSIBILITY_HORIZON_CURVE_V1.json` | 12 checks: J2, tie-sensitive witness search, J3, J4, J5, DS1, DS2, P2 canonical, PH1, PH2, PH3 PASS; `MIXED_P2_WITNESS_SEARCH` = CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS (5826 machines searched — spec-mandated preserved negative, not a theorem) |
| `llm_epistemics_universality_audit.py` | V4 §12 | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | PASS — U1 sandwich, U2 separating saturation, U3/U4 collided-pair 0–1 error, U5 nested monotone |
| `llm_epistemics_logloss_benchmark.py` | V4 §11 | `LOGLOSS_PARENT_BENCHMARK_V1.json` | PASS — A achievability (shared r, 11 ratios), A registered-class tightness converse, B conditionally-independent product sum (shared-Θ and per-coordinate-Θ, normalized grid), C correlated controls with exact inflation. Scope: the converse is exact within the registered per-fibre erasure class only; Q-dependent-erasure counterexample frozen in `part_a_converse.scope_counterexample` |
| `llm_epistemics_theorem_locations.py` | §1 provenance map | `PARENT_THEOREM_LOCATIONS_V1.json` + `PARENT_THEOREM_LOCATIONS_V1.md` | PASS — 38 rows: 36 SUPPORTED (every row re-validated against its receipt JSON at generation time), `T8D_WORST_FIBRE_CARDINALITY` NOT_MECHANIZED (explicit gap for the theory lane), mutation battery PENDING (run in flight) |

## Re-run batch 2 (billy-old)

```bash
python3 llm_epistemics_dynamic_phase_audit.py --outdir out
python3 llm_epistemics_universality_audit.py --output out/RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json
python3 llm_epistemics_logloss_benchmark.py --output out/LOGLOSS_PARENT_BENCHMARK_V1.json
python3 llm_epistemics_theorem_locations.py --output out/PARENT_THEOREM_LOCATIONS_V1.json
```

The theorem-locations generator is itself a validator: it re-derives every
SUPPORTED verdict from the receipt JSONs and exits 3 if any row's evidence is
missing or contradicts the receipt (negative-control tested). Exit codes and
verdict vocabulary as in batch 1.
