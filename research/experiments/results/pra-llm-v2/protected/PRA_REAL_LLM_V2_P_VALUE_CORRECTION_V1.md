# PRA real-LLM V2 — dated correction: exact two-sided p values

**Date: 2026-09-05.** Correction to the p values printed in
`PRA_REAL_LLM_AUDIT_ROLLUP_V2__protected.json` / `.md` (merge `3858bc4`). The frozen protected
outcome files are **not rewritten**; this record states the defect, the corrected values, and what
does and does not change, in the same form as the dated H-EXT-1 receipt correction.

**No terminal, gate verdict, route or accuracy changes.** The defect made every reported p value
far *larger* than the truth, so it was conservative in the direction that matters, and every gate
comparison at its registered alpha yields the identical decision before and after.

## 1. The defect

`binom_two_sided_p` in `research/llm-machine-epistemics/pra_real_llm_audit.py` selected the
outcomes "at least as extreme as k" by comparing **probabilities** with an absolute tolerance:

```python
pk = math.comb(n, k) / 2 ** n
total = sum(math.comb(n, i) for i in range(n + 1) if math.comb(n, i) / 2 ** n <= pk + 1e-15) / 2 ** n
```

Once the point mass at `k` falls far below `1e-15`, that predicate is satisfied by every outcome
whose probability is under roughly `1e-15` — nearly the whole distribution — so the sum saturates
near `1e-15` no matter how extreme the data are. The signature is visible in the record itself: the
reported p barely moves as the discordant count rises, `1.7e-15` at 82 discordant pairs and
`1.2e-15` at 221, where a correct test must fall by tens of orders of magnitude.

The fix replaces the float comparison with exact integer arithmetic on binomial coefficients
(`math.comb(n, i) <= math.comb(n, k)`), with the final division taken as a `Fraction`. Verified
against an independent exact recomputation on nine cases including the textbook `k=1, n=10`
(0.021484375) and the symmetric `k=5, n=10` (1.0); a control confirms the old and new forms differ
where the defect bit.

## 2. Corrected values

Every non-degenerate contrast in the V2 protected rollup. `k = min(b, c) = 0` in all of them, so
each is a one-directional discordance; `m = b + c`.

| model | contrast | m | recorded p | **corrected p** |
|---|---|---|---|---|
| qwen2.5-32b-instruct | GP0 contrast A (R1 vs R2, P1 current) | 60 | 1.06e-16 | **1.7347e-18** |
| qwen2.5-32b-instruct | GP1 contrast B (R2→R3, P2 canonical) | 221 | 1.25e-15 | **5.9347e-67** |
| qwen2.5-32b-instruct | GP1 contrast B, instance level | 120 | 1.98e-15 | **1.5046e-36** |
| qwen2.5-32b-instruct | GP1 contrast B, same fibre | 182 | 1.00e-15 | **3.2627e-55** |
| qwen2.5-32b-instruct | GP1 contrast B, same fibre, instance level | 120 | 1.98e-15 | **1.5046e-36** |
| qwen2.5-32b-instruct | GP1 maintain-only | 108 | 1.01e-15 | **6.1630e-33** |
| qwen2.5-32b-instruct | GP1 update-only | 113 | 4.10e-16 | **1.9259e-34** |
| qwen2.5-32b-instruct | GP2 contrast D (true removal vs KV retained) | 221 | 1.25e-15 | **5.9347e-67** |
| mistral-small-24b-instruct-2501 | GP0 contrast A | 82 | 1.73e-15 | **4.1359e-25** |
| mistral-small-24b-instruct-2501 | GP1 contrast B | 180 | 2.52e-15 | **1.3051e-54** |
| mistral-small-24b-instruct-2501 | GP1 contrast B, instance level | 119 | 5.86e-16 | **3.0093e-36** |
| mistral-small-24b-instruct-2501 | GP1 contrast B, same fibre | 239 | 2.03e-15 | **2.2639e-72** |
| mistral-small-24b-instruct-2501 | GP1 contrast B, same fibre, instance level | 120 | 1.98e-15 | **1.5046e-36** |
| mistral-small-24b-instruct-2501 | GP1 maintain-only | 112 | 7.12e-16 | **3.8519e-34** |
| mistral-small-24b-instruct-2501 | GP1 update-only | 68 | 3.56e-16 | **6.7763e-21** |
| mistral-small-24b-instruct-2501 | GP2 contrast D | 180 | 2.52e-15 | **1.3051e-54** |

Contrasts with zero discordant pairs (`contrast_C`, `contrast_E`, GP3 `p0` and `recon`) reported
`p = 1.0`; that value is correct and unchanged — with no discordant pairs there is nothing to test,
and the record's degenerate-contrast caveats stand as written.

## 3. What does not change

Gate decisions were re-evaluated per contrast at the registered alpha: **identical in every case**,
because both the recorded and the corrected p are many orders of magnitude below any registered
threshold. So:

- qwen2.5-32b-instruct remains `P2_PROSPECTIVE_REVISION_STATE_REQUIRED` (GP0–GP3 all pass).
- mistral-small-24b-instruct-2501 remains `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`,
  disqualified by its own present-equivalence gate (per-unit 0.296), which is not a p-value test.
- The overall terminal remains `P2_SINGLE_MODEL_ONLY__REGISTERED_BOUNDARY_RESULT`.
- The dormant-information control and the three-history joint-intersection control are unaffected.

No accuracy, count, discordance or interval in the rollup is touched by this defect; only the p
column was computed by the defective function.

## 4. Scope beyond this rollup

The same function computed p values in the earlier PRA real-LLM r1 campaign and anywhere else this
runner was used. Those records inherit the same conservative inflation and should be read with this
correction; each needs its own dated correction before any of its p values is quoted. The fix is in
the runner from this commit forward, so any future run reports exact values directly.

**Manuscript instruction:** PRA must quote the corrected values from this table, not the values in
the frozen rollup, and cite this record beside the rollup. Reporting the old numbers would
understate the evidence; reporting the new ones without this record would misrepresent what the
frozen artifact says.
