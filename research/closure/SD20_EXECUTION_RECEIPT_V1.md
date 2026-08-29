> ## ⚠️ CORRECTION (2026-08-29 revival pass) — Stage-2 numbers below are superseded
>
> The revival pass (`SD20_REVIVAL_RECEIPT_V1.md`, same repo) found that Stage 2
> labeled outcomes with silent `.get(metric, 0.0)` defaults. SD10 head
> snapshots carry ONLY `arxiv:author_count`, so every head-arrival transition —
> **2,067/3,220 = 64% of the corpus** — received a deterministic artifact
> label: `abstract_delta` = "−" in 2,067/2,067 and gap bucket ">90d" in
> 2,067/2,067, both fabricated from missing data read as 0.0 (the head's
> abstract chars and per-version update date were simply never recorded by the
> SD10 head fetch). A deterministic component is absorbed trivially by the
> marginal baseline, which confounds the V1 conditional-vs-marginal comparison
> in the tables below.
>
> **Stage 1 (acquisition) is unaffected** — the version-history data files are
> correct; the defect was in the analysis script, and the repair re-fetched
> the missing head metadata lawfully (104 additional batched requests). The
> Stage-2 tables below are preserved as the honest record of the defective run
> and MUST NOT be cited; the corrected result of record is
> `research/closure/SD20_REVIVAL_RECEIPT_V1.md`.

# SD20 execution receipt V1 — bounded-pilot arXiv version-transition operator discovery (2026-08-29)

Owner issue #50 (science owner #49). Executes the SD20 stage
(`DEVELOPMENT_OPERATOR_DISCOVERY`) of
`research/experiments/SCIENTIFIC_DEVELOPMENT_RECURSIVE_META_GENERALIZATION_PROTOCOL_V1.json`
on the SD10 bounded corpus slice. SD10's arXiv observations are head-version
snapshots (one per trajectory), so this stage first ACQUIRED the missing
within-trajectory history (v1..v(k-1) of every head ≥ v2), then ran operator
discovery on the assembled multi-step trajectories. Fetch host: `billy-old`
(`~/sd10run/ORION-V2`, main at `0ce87a3`).

**Classification: `BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM`.** No terminal
option (`POPULATION_REGULARITY_ONLY` / `PARENT_SUFFICIENT` / `CANNOT_CHECK`)
is claimed from this slice; see "What SD20 does NOT establish".

## Stage 1 — version-history acquisition (`scripts/sd20_sources/arxiv_version_history_adapter.py`)

New lawful adapter, same public arXiv Atom API and etiquette contract as SD10
(≥3 s interval, contact UA, batched versioned `id_list` — one request per 20
versions, i.e. request count stays far BELOW the per-record floor):

| Quantity | Value |
|---|---|
| Parent trajectories (SD10 arXiv heads ≥ v2) | 2,067 (2,933 single-version = censored, no history exists) |
| Version targets planned | 3,220 (always the full v1..v(k-1) set — stable plan across runs) |
| Batches (20 ids / request) | 161 |
| HTTP requests total | 161 (84 run 1 + 77 resume run; 0 by the aborted run 2) |
| Observations in output | 3,220 — `missing_versions: []` |
| Errors / unplanned entries | 0 / 0 |
| Domain anchored to parent head | 3 events (mid-trajectory primary-category change; per-version category kept as action feature) |
| Epoch anchored to parent head | 0 events (`<published>` is the paper-level v1 date) |
| Outcome bindings emitted | 0 (version progression is an observation stream, never an outcome) |

Per-version `<updated>` dates are recorded as real temporal proxy metrics
(`arxiv:updated_epoch_days`, `arxiv:days_since_first_deposit`); `<published>`
is identical across versions and anchors `epoch_id` to the parent head.

### Incident: HTTP-429 interruption mid-run (fixed, zero data loss)

Run 1 died at batch 85 with `retries exhausted ... retryable HTTP 429`
(sustained arXiv throttle window; default budget 5 retries / 120 s cap was too
small). Two defects were found and fixed before the relaunch:

1. **Cursor non-advance** — the loop advanced `{"batch": start_batch + 1}`
   (a pre-loop constant) instead of the current batch index, so the persisted
   cursor never moved past 1 while `pages_fetched` told the truth (84).
2. **Shrinking-plan resume** — the plan excluded already-on-disk targets, so
   on resume the batch list shrank from 161 to 77 while the cursor indexed the
   original 161 → `batches[84:]` was empty → instant no-op "completion" with
   0 requests. The plan is now always the full stable target list; resume
   SKIPS batches whose targets are all durable (ledger membership) without a
   request, and the key-dedupe ledger absorbs any torn re-fetch.

The resume point was reconstructed from durable evidence only (1,680 ledger
rows ÷ 20 per batch = 84 == persisted `pages_fetched`, asserted) and the run
relaunched with `--rate-seconds 5.0 --retries 10 --backoff-cap 300`. Final
state: batch 161/161, 3,220/3,220 rows, `error_log` empty, `missing_versions`
empty. Full traceback of the aborted run is preserved in the artifacts tarball
(`run.log`).

## Stage 2 — operator discovery (`scripts/sd20_operator_discovery.py`)

Population: **2,067 multi-version trajectories (2,933 single-version censored),
3,220 transitions** (train 2,210 / test 1,010, trajectory-level disjoint
split). Outcome representation: 27-cell delta alphabet
(author_delta {0,+,−} × abstract_chars_delta {0,+,−} × gap bucket {≤7d, 8–90d,
>90d}); context = first/later step × arXiv top-level category (18 cells);
Laplace-smoothed categorical P(delta | context), `MIN_CONTEXT_TRANSITIONS=20`
fallback to marginal (recorded, never silent).

### Primary metric 1 — `heldout_transition_prediction` (mean log-score, test)

| Arm | mean log-score | Δ vs baseline | bootstrap 95% CI | CI excludes 0 |
|---|---|---|---|---|
| SIMPLE_FREQUENCY_BASELINE (marginal) | −1.5714 | 0 | — | — |
| TEMPORAL_SEQUENCE_MODEL_PARENT (context-conditional) | −1.6535 | **−0.0821** | [−0.1021, −0.0623] | True |
| FIXED_META_LESSON_INJECTION (abstract_grows) | −4.2303 | −2.6589 | [−2.7949, −2.5222] | True |
| FIXED_META_LESSON_INJECTION (authors_nondecreasing) | −2.9729 | −1.4014 | [−1.4869, −1.3107] | True |
| FIXED_META_LESSON_INJECTION (gaps_lengthen) | −3.1408 | −1.5694 | [−1.6542, −1.4775] | True |
| F0_META_PARENT_FEDERATION (log-linear pool) | −1.8404 | −0.2690 | [−0.3382, −0.2028] | True |

**Honest negative:** the context-conditional operator UNDERPERFORMS the
marginal frequency baseline on heldout transitions, and every science-of-science
parent arm loses. The three a-priori "breakthrough lessons" are not merely
insufficient — they are strongly anti-predictive (Δ −1.40 to −2.66). All
discoverable transition regularity on this slice lives in the POPULATION-level
marginal delta distribution.

### Primary metric 2 — `operator_stability`

Bootstrap TV distance (B=200): mean 0.0690, max 0.5668 (thin contexts). The
estimated marginal operator is stable, so the negative above is not noise.

### Primary metric 3 — `cross_domain_support`

Leave-one-category-out vs baseline: **0 / 18 evaluated categories beat the
baseline** (2 more TOO_FEW: n_test < 10). No arXiv domain shows beyond-marginal
transition regularity.

### Primary metric 4 — `failed_trajectory_explanation`

**CANNOT_CHECK** — the corpus is outcome-censored (SD10: 99.9% UNKNOWN); no
failed-trajectory labels exist and none are invented.

### CANNOT_CHECK_ON_SLICE arms (recorded, never silently passed)

- `BIBLIOMETRIC_SCIENCE_OF_SCIENCE_PARENT` — Atom metadata carries no citation/fame fields.
- `NETWORK_SCIENCE_PARENT` — no disambiguated author network in the inputs (SD10 CANNOT_CHECK).
- `CAUSAL_OR_QUASI_EXPERIMENTAL_PARENT_WHEN_IDENTIFIABLE` — no interventions or quasi-experimental variation in version deposits.
- `F2_RECURSIVE_SCIENTIFIC_DEVELOPMENT_FULL` — recursive promotion requires SD50 machinery; the pilot has one level.

### Hard gates (all enforced, exit 3 on violation)

Fame-field scan over proxy metric names (citation/cite/fame/impact/prize/award/
download/view); trajectory-level disjoint train/test split; version-local
features only (no post-outcome leakage); no L2+ claim; frozen protocol gates
all-false; `authority` all-false.

### Negative controls (script validation, now repo tests)

`tests/unit/test_sd20_operator_negctl.py` — NC1 injected fame field → exit 3
hard-gate; NC2 head-only (single-step) input → exit 3 "no transitions found";
NC3 identical inputs → byte-identical receipts (seeded: split/bootstrap/
stability all `random.Random(20260829)`). Adapter fixture suite
(`tests/unit/test_sd20_version_history_adapter.py`) covers parse, parent-head
domain/epoch anchoring + counters, Atom error fail-closed, missing-version
honesty, end-to-end `run()` with injected transport, and stable-plan resume
idempotence (0 requests, 0 new rows). Both suites ran green on the fetch host;
no test opens a socket.

## What SD20 does NOT establish

- **No terminal option is claimed.** The evidence pattern on this slice
  (stable marginal regularity + no conditional/parent gain) is CONSISTENT with
  `POPULATION_REGULARITY_ONLY` and REFUTES `PARENT_SUFFICIENT` here, but the
  pilot is bounded: 27-cell alphabet, metadata-only features, one source
  (arXiv), one deposit year (2024 window). The terminal mark stays open.
- No operator is validated for SD30 promotion; nothing here feeds SD40+.
- 2,933 single-version trajectories are censored, not "no-development".
- Version progression remains an observation stream; it is never an outcome,
  and no proxy metric maps to an outcome class anywhere in the pipeline.

### Revival levers (diagnose-revive-before-discard, next iteration)

1. **Alphabet sensitivity** — coarser (9-cell) / finer (include title_chars and
   author-count jointly) delta alphabets; the current 27-cell outcome space may
   be too sparse for conditional structure to pay for its parameters.
2. **Per-category marginal operators** — conditioning hurt in the JOINT
   context cell, but category-specific marginals (no first/later-step split)
   are untested.
3. **Scale-up** — the adapters are parameterized; a wider window (multi-year)
   is a re-run, not new code, and multiplies transitions per context cell.
4. **Cross-source transitions** — Crossref/OpenAlex/PubMed version-like
   records remain CANNOT_CHECK on this slice.

## Artifacts

Committed (small): adapter receipt + operator receipt JSON/MD under
`research/experiments/results/issue50/sd20/`. Hash-pinned data artifacts
(not committed; 2.6 MB raw / 103 KB gzipped) in
`sd20_artifacts_20260829.tar.gz` (sha256
`6c2ec6deec90af5603b811274ff229f1a7398ce21dc4be3d5d05e87876f20114`) on
`billy-old:~/sd20_artifacts_20260829.tar.gz` and
`lunarc:/projects/hep/fs9/users/scyiu/sd20_artifacts_20260829.tar.gz`
(hash verified on both hosts).

| Artifact | sha256 |
|---|---|
| `arxiv_version_obs.jsonl` | `ecf4f4a8f2c7e06e44eceeea43295aa54f9a167d2f9385b7e75050a88d3a6bc5` |
| `arxiv_version_receipt.json` | `0997cfd998e5b42f2408fbcf2104205129e5df5b683f6d43918b8bbf5bb83f6e` |
| `sd20_operator_receipt.json` | `777030a7630d2e71c1ccc00adc7f16f92b0a12ea401a227cc01dec5482bd428f` |
| `sd20_operator_receipt.md` | `47190b1f264c38422121c41c15701b5f0b3075829a96909e9d06f50e24360340` |

Parent lineage: SD10 `arxiv_obs.jsonl`
`af5f52efe9191e630169e506d76dd929c2c30e808dc559f936013738d6386b0f`
(recorded in the adapter receipt lineage field).

## Reproduction

```bash
# stage 1: version-history acquisition (resumable, rate-gated)
PYTHONPATH=src python3 scripts/sd20_sources/arxiv_version_history_adapter.py \
  --parent-observations out/sd10/arxiv_obs.jsonl \
  --output-observations out/sd20/arxiv_version_obs.jsonl \
  --output-bindings out/sd20/arxiv_version_bindings.jsonl \
  --receipt out/sd20/arxiv_version_receipt.json --state out/sd20/arxiv_version_state.json \
  --since 2024-01-01 --until 2024-12-31 --batch-size 20 \
  --contact-email "$SD10_CONTACT_EMAIL" --rate-seconds 5.0 --retries 10 --backoff-cap 300

# stage 2: operator discovery (seeded, offline)
PYTHONPATH=src python3 scripts/sd20_operator_discovery.py \
  --observations out/sd10/arxiv_obs.jsonl \
  --observations out/sd20/arxiv_version_obs.jsonl \
  --output out/sd20/sd20_operator_receipt.json
```
