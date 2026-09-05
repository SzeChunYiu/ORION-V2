# Infinite threshold lifecycle reference

The complete proof and equal-interface parent comparison are in
`PROOFS_AND_PARENT_REDUCTION_V1.md`. `threshold_lifecycle.py` supplies exact
agreement-region answers, all witness revocation units, arbitrary finite
revocation, sharp robustness checks and resource-bounded active repair for
integer thresholds. The class has no fixed bound on its integer parameter or
query domain. The fixed-target authenticated membership oracle is an external
premise; this package supplies no runtime truth or admission authority.

Run from the repository root:

```bash
python research/machine-epistemics-theory/lifecycle_identification_v2/check.py
python -m pytest tests/unit/test_infinite_threshold_lifecycle.py -q
```

Normal checker exit: **0 / PASS**. Optimized Python (`python -O`) deliberately
returns **2 / CANNOT_CHECK** because the calibration uses assertions. The
reference functions themselves validate contracts without assertions.

Validation on 2026-09-05:

- **31 unit cases passed**, including 22,880 finite interval/target repairs,
  every deletion subset in the small witness family, 7 large integer controls,
  malformed oracle/context controls and useful-retention counterexamples.
- The separate CLI checked **3,696** interval/target pairs and **318** revocation
  subsets. `CALIBRATION_RECEIPT_V2.json` binds both protocol versions, proof,
  implementation, checker and tests by SHA-256. Finite execution is not the
  proof of any infinite assertion.
- An internal independent semantics/math reviewer reconstructed T1–T5 and
  found two implementation boundary defects: unhashable oracle revocation
  units raised a raw error, and forged equality inside an observation's
  context field bypassed exact authority matching. Both regression cases
  were first run **RED**, then fixed and included in the 31-case **GREEN** run.
- The review also checked the distinction between source-unit independence
  and statistical independence, and the difference between whole-function
  identification and retaining supported per-input answers.

The original protocol remains addressable. V2 transparently records the
target-information and coordinate-resource clarification after initial local
calibration and before this successor validation. This is internal reference
work, with no retrospective protected-study or external-review claim.

The strongest parent product is sufficient under the matched interface. These
results do **not** close F7's infinite SHRG/CCG construction-inventory problem,
prove architecture advantage, or generalize to unrestricted language or noisy
evidence. They provide a concrete infinite-class lifecycle component and
delimit the remaining research problem.
