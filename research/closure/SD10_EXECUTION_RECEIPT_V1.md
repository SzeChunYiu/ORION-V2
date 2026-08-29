# SD10 execution receipt V1 — bounded-window population corpus + bias audit (2026-08-29)

Owner issue #50 (science owner #49). Executes the SD10 stage of
`research/experiments/SCIENTIFIC_DEVELOPMENT_RECURSIVE_META_GENERALIZATION_PROTOCOL_V1.json`
on a bounded, fully-reproducible slice: **window 2024-01-01..2024-12-31, four lawful
source modes, ~5,000 records per mode** (arXiv 5,000 / Crossref 5,000 / OpenAlex 4,982 /
PubMed 5,000 = 19,982). Fetch host: `billy-old` (`~/sd10run/ORION-V2`, main at `8e879a3`).
This is a **bounded-window execution, not a population-scale claim**: scale-up is a
parameterized re-run of the same adapters (no new code), and no SD20+ inference is
authorized by this receipt.

## Stage 1 — lawful acquisition (4 adapter runs)

| Mode | Records | Observations | VALIDATED_FAILURE bindings | Requests | Errors | Window echo |
|---|---|---|---|---|---|---|
| `arxiv_atom_metadata` | 5000 | 5000 | 0 (by design: version progression ≠ outcome) | 30 | 0 | 2024-01-01..2024-12-31 |
| `crossref_rest_works` | 5000 | 5000 | 5 | 50 | 0 | 2024-01-01..2024-12-31 |
| `openalex_works` | 4982 | 4982 | 13 | 50 | 0 | 2024-01-01..2024-12-31 |
| `pubmed_eutils_metadata` | 5000 | 5000 | 5 | 102 | 0 | 2024-01-01..2024-12-31 (ESearch count 1,739,765, per-page echo recorded) |

Every adapter wrote a receipt with per-file sha256, lineage, rate etiquette
(arXiv ≥3 s; Crossref polite pool; OpenAlex documented budget; PubMed ≤3 req/s no-key,
contact `52784502+SzeChunYiu@users.noreply.github.com`), censoring statement and
`authority: {grants_causal_law: false, grants_scientific_truth: false}`.
The arXiv run survived an HTTP-429 interruption and resumed via the persisted cursor
(ledger merge semantics; no records lost, `error_log` empty at completion).

## Stage 2 — bias audit (5 frozen metrics)

`scripts/sd10_bias_audit.py` (this PR) over all four observation/binding sets:
**OVERALL EXECUTED, exit 0.**

- Coverage: 19,982 trajectories / 19,982 observations / 814 domains; per-mode table above.
- Missingness: institution ids empty for 100% of arXiv/Crossref obs vs 3.3% (OpenAlex)
  and 0.7% (PubMed); `team_id` empty everywhere (author lists are not stable team
  identities — CANNOT_CHECK, never invented); validation ids empty everywhere.
- Identity linkage: duplicate observation ids = 0; id schemes disjoint across modes;
  cross-mode linkable share 0.0000 = **absent linkage evidence, not zero linkage error**.
- Survivorship: 22/19,982 trajectories carry any validated binding (23 VALIDATED_FAILURE
  records); **19,960 stay UNKNOWN** — absence of a retraction marker never encodes success.
- Outcome proxy disagreement: `CANNOT_CHECK_FROM_EMITTED_FIELDS` — only Crossref emits
  `doi:` trajectory ids; remediation recorded (emit doi: aliases in source_ids when the
  source record carries a DOI, then re-run).

### Negative controls (audit script validation, 2026-08-29)

Both controls were run as in-place mutations of a real input, executed, then restored
(byte-verified):

1. 3-mode input (drop PubMed) → exit 3, `source modes [...] below frozen minimum 4`.
2. Doctored duplicate observation id (`openalex-obs:W3118608800` twice) → exit 3,
   `duplicate observation_id: ['openalex-obs:W3118608800']`.

Exit 0 is reserved for EXECUTED (CANNOT_CHECK marks are honest outcomes); exit 3 is
internal-consistency failure. A same-input re-run after restore reproduced the committed
receipt byte-for-byte.

## Stage 3 — episodes and corpus

- `scripts/assemble_scientific_development_episodes.py` → 19,982 episodes
  (23 with a validated outcome class, 19,960 UNKNOWN), receipt records
  `acquisition_performed: false`, `citation_or_fame_infers_outcome: false`.
- `scripts/build_scientific_development_corpus.py` → `corpus.json` +
  `corpus_receipt.json`: 4 source modes, 814 domains, epochs `{year:2024, year:2026}`.
  The 34 `year:2026` episodes are all PubMed and are the documented `[dp]` multi-valued
  date semantics (a record matches the pdat window via one date form while the
  ArticleDate-first epoch channel resolves the other) — recorded, not "corrected".

## What SD10 does NOT establish

- No population-level regularity, operator, or meta-principle (SD20+ not run).
- No outcome for 99.9% of trajectories; the corpus is outcome-censored, and every
  downstream consumer must carry the censoring statement.
- Cross-mode identity linkage and retraction-channel disagreement remain CANNOT_CHECK
  until doi: aliases are emitted.
- PubMed carries no citation counts; none were invented. Proxy metrics never map to
  outcome classes anywhere in the pipeline.

## Artifacts

Committed (small): per-adapter receipts, bind files, 4-mode bias audit JSON+MD,
episodes/corpus receipts — under `research/experiments/results/issue50/sd10/`.
Hash-pinned data artifacts (not committed; 64 MB raw / 3.8 MB gzipped) live in
`sd10_artifacts_20260829.tar.gz` (sha256 `5a191c04c6694485a87d0d871814b5e45978fecac00dcafa0cfce3c53326f689`)
on `billy-old:~/sd10_artifacts_20260829.tar.gz` and
`lunarc:/projects/hep/fs9/users/scyiu/sd10_artifacts_20260829.tar.gz`.

| Artifact | sha256 |
|---|---|
| `arxiv_obs.jsonl` | `af5f52efe9191e630169e506d76dd929c2c30e808dc559f936013738d6386b0f` |
| `cr_obs.jsonl` | `c980bb680a9e824f9c35970efda76e2cbb75997f794abdbea0417a36102155d8` |
| `oa_obs.jsonl` | `1060bb8630fe9a5897f1e10b9d2569ab009f81c350cb5f64528af5526aec00b0` |
| `pm_obs.jsonl` | `c2f26b694314f2abc08460c6f2e35f7840fa1981dd3b767bd9683a8d5708180d` |
| `episodes.jsonl` | `57185cebef23dca53b7fdb47d1771b908164db9f0e36ed7e23434bd203213ec8` |
| `corpus.json` | `d41fd55bbd0990448b41e27f511091b8bf75a5190f9f8f46df3541a43da25b1d` |
| `bias_audit_4mode.json` | `2433a9c074ba536d814b8cb82c4dad893dce0453fac63c268a6c106225caef78` |

## Reproduction

```bash
PYTHONPATH=src python3 scripts/sd10_sources/<mode>_adapter.py ...   # per-adapter receipts
PYTHONPATH=src python3 scripts/assemble_scientific_development_episodes.py \
  --observation out/sd10/<mode>_obs.jsonl ... --output out/sd10/episodes.jsonl --receipt ...
python3 scripts/build_scientific_development_corpus.py --input out/sd10/episodes.jsonl \
  --output out/sd10/corpus.json --receipt out/sd10/corpus_receipt.json
python3 scripts/sd10_bias_audit.py --observation ... --outcome-binding ... --adapter-receipt ... \
  --output out/sd10/bias_audit_4mode.json --summary out/sd10/bias_audit_4mode.md \
  --min-source-modes 4 --run-window 2024-01-01..2024-12-31
```
