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
