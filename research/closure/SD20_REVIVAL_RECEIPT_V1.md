# SD20 Revival Receipt V1 — head-metric repair + alphabet/context variant sweep (2026-08-29)

Schema: `orion.v2.sd20-operator-discovery.v2` · Outcome of this receipt:
**V1's Stage-2 negative was CONFOUNDED by a labeling defect; the repaired re-run
CONFIRMS the negative with clean labels and explains it as an estimation-variance
floor, not a missed signal.** Classification unchanged:
`BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM`.

Result of record for SD20 Stage 2 = THIS receipt. The tables in
`SD20_EXECUTION_RECEIPT_V1.md` are superseded and must not be cited (correction
banner prepended there). Stage-1 acquisition (both adapters, all data files) was
and remains correct.

## 1. Defect found (why a revival pass was mandatory)

V1's `build_transitions` labeled outcomes with silent `.get(metric, 0.0)`
defaults. SD10 head snapshots carry ONLY `arxiv:author_count`, so every
head-arrival transition was labeled from missing data read as 0.0:

| Degeneracy (V1 corpus) | Count |
|---|---|
| Head-arrival transitions affected | 2,067 / 3,220 = **64.2%** |
| `abstract_delta` = "−" on affected steps | 2,067 / 2,067 (deterministic) |
| gap bucket = ">90d" on affected steps | 2,067 / 2,067 (deterministic) |
| `author_delta` real (0/+/− mix) | 3,220 / 3,220 |

A deterministic artifact component on 64% of transitions is absorbed trivially
by the marginal baseline, confounding V1's conditional-vs-marginal comparison.
`author_delta` was real everywhere, which is why V1's numbers were not pure
noise — but no V1 Stage-2 number was trustworthy.

## 2. Repair (code + data, committed before any re-run)

Commit `cdde9cc` on branch `sd20-revival-head-metrics` (tests: 12 SD20 + 41
SD10/sources green, billy-old):

1. **Data**: adapter `--fetch-heads` mode plans exactly head v_k per parent —
   one more lawful arXiv pass: **104 batched id_list requests**, 5.0 s spacing,
   descriptive UA with contact, **2,067/2,067 heads fetched,
   `missing_versions: []`, `error_log: []`** (receipt:
   `research/experiments/results/issue50/sd20/arxiv_head_receipt.json`).
2. **Analysis**: missing required metrics are now **CENSORED and counted, never
   defaulted** (`transitions_censored_missing_metric`, per-metric
   `censor_detail`, hard gate `no_missing_metric_silent_defaults`). Negative
   gaps are censored. Same-observation_id rows from two passes **supersede by
   strictly richer metric set** (counted in `merge_stats`) instead of
   duplicating.
3. **Variants**: `--alphabet {default 27-cell, coarse9, fine81}` ×
   `--context {default first/later|category}`. Fixed-lesson/F0 arms are
   SKIPPED-RECORDED (`SKIPPED_ALPHABET_VARIANT`) on variant alphabets (their
   encodings assume the default cells), never re-encoded.

Negative controls: NC4 (thin head steps → censored+counted, corpus with nothing
labelable → exit 3), NC5 (variant runs byte-deterministic, skips recorded).

## 3. Repaired corpus

| Quantity | Value |
|---|---|
| trajectories (SD10 arXiv parents) | 5,000 |
| multiversion trajectories | 2,067 |
| transitions labeled | **3,220 (100%)** |
| censored missing-metric | **0** |
| head rows superseded (thin→rich) | 2,067 (`arxiv_atom_metadata -> arxiv_atom_version_history`) |
| determinism | default run re-executed → byte-identical receipt |

All frozen hard gates green, including `no_missing_metric_silent_defaults`.
Parents (bibliometric / causal / network / F2-full) remain `CANNOT_CHECK_ON_SLICE`.

## 4. V2 results (heldout transition prediction, Δ = mean logscore − marginal baseline; negative = worse than marginal)

| Variant (cells / context) | Δ vs baseline | bootstrap CI95 | CI excl. 0 | TV stability (mean) |
|---|---|---|---|---|
| **default (27, first/later)** | **−0.0747** | [−0.0982, −0.0510] | yes | 0.0816 |
| coarse9 (9, first/later) | −0.0146 | [−0.0282, −0.0002] | yes | 0.0550 |
| fine81 (81, first/later) | −0.2262 | [−0.2573, −0.1953] | yes | 0.0860 |
| catctx (27, category) | −0.0507 | [−0.0714, −0.0290] | yes | 0.0745 |
| coarse9 + catctx (9, category) | −0.0073 | [−0.0206, +0.0062] | **no** | 0.0504 |

Default-variant arms: marginal baseline logscore −2.1774; conditional
−2.2520; F0 federation **−0.5918**; fixed lessons abstract_grows −0.9842 /
authors_nondecreasing −0.7955 / gaps_lengthen −1.0522 (all CI excl. 0).
**LOO beats baseline: 0/18 categories, in every variant.** No variant, lesson,
federation, or category produces a positive point estimate anywhere.

## 5. V1 → V2 comparison (V1 numbers superseded, shown only to document the correction)

| Quantity | V1 (defective labels) | V2 (repaired) |
|---|---|---|
| transitions labeled honestly | 1,153/3,220 (36%) | 3,220/3,220 (100%) |
| conditional Δ (default) | −0.0821 [−0.1021, −0.0623] | −0.0747 [−0.0982, −0.0510] |
| F0 federation Δ | −0.2690 | −0.5918 |
| fixed lessons Δ range | −1.40 … −2.66 | −0.79 … −1.05 |
| LOO beats baseline | 0/18 | 0/18 (all 5 variants) |
| classification | BOUNDED_PILOT_INTERIM | BOUNDED_PILOT_INTERIM (all 5 variants) |

Absolute logscores are NOT comparable across V1/V2 (the label distribution
itself changed once artifact determinism was removed); each run's internal
Δ-vs-baseline is the comparable quantity — and it keeps its sign and
significance in every powered variant.

## 6. Reading: the deficit is an estimation-variance floor, not a missed signal

The penalty is **monotone in alphabet fineness**: ~−0.01 at 9 cells, ~−0.07 at
27, ~−0.23 at 81, and statistically vanishes at the coarsest partition
(coarse9+catctx CI includes 0). This is the signature of estimating K-cell
multinomials per context from thin counts: the unregularized plug-in bound
(K−1)/(2·n̄_context) with n̄_context ≈ 3,220/36 ≈ 89 gives ≈ 0.045 (K=9),
≈ 0.15 (K=27), ≈ 0.45 (K=81) — each observed deficit sits below its bound
(smoothing shrinks the penalty) and scales with K as the bound does. **Any true
per-cell signal is below the detection floor of this corpus; there is no
evidence any granularity carries exploitable predictive information the
marginal lacks.**

## 7. Verdict + remaining levers (priced)

- **Negative CONFIRMED after repair** — and upgraded from "confounded" to
  "explained": variance-limited at n=3,220 transitions. No terminal claim.
- **Scale-up is the one live lever**: current default CI95 half-width ≈ 0.024
  nats/transition → minimum detectable effect ≈ 0.05. Detecting a true
  δ=0.01 nats needs ≈ 9× transitions (~29k, ≈ 18k multiversion parents vs
  today's 2,067). Mechanism: SD10 window expansion (adapter is
  window-parameterized; population-scale is a re-run, not new code).
- **Cross-source**: stays `CANNOT_CHECK` (no other lawful source exposes
  within-artifact version ladders).
- **Ladder**: SD30 matched-contrast remains structurally hard on this corpus
  (22 retraction-witnessed failures, 0 validated successes); SD40 heldout
  field/epoch transfer inherits this same variance floor — budget accordingly.

## 8. Reproduce

```bash
PYTHONPATH=src python3 scripts/sd20_operator_discovery.py \
  --observations out/sd10/arxiv_obs.jsonl \
  --observations out/sd20/arxiv_version_obs.jsonl \
  --observations out/sd20/arxiv_head_obs.jsonl \
  --output out/sd20/sd20_v2_default.json            # + --alphabet/--context variants
```

Head-repair fetch: adapter `--fetch-heads` (receipt:
`arxiv_head_receipt.json`; 104 requests, 2,067/2,067, zero missing).
Artifacts tarball `sd20_artifacts_20260829_v2.tar.gz` (raw observations +
all receipts; sha256 in the PR comment) mirrored on billy-old and LUNARC.
