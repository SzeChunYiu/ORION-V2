# SD10 bias audit (V1)

Overall: **EXECUTED**. Window: `2024-01-01..2024-12-31`. Source modes: 4 (arxiv_atom_metadata, crossref_rest_works, openalex_works, pubmed_eutils_metadata).

| Mode | Trajectories | Observations | Domains | Epochs |
|---|---|---|---|---|
| `arxiv_atom_metadata` | 5000 | 5000 | 146 | year:2024 |
| `crossref_rest_works` | 5000 | 5000 | 1 | year:2024 |
| `openalex_works` | 4982 | 4982 | 26 | year:2024 |
| `pubmed_eutils_metadata` | 5000 | 5000 | 641 | year:2024, year:2026 |

- Missingness (share of observations): `arxiv_atom_metadata`: inst=1.000, team=1.000, val=1.000, proxy=0.000; `crossref_rest_works`: inst=1.000, team=1.000, val=1.000, proxy=0.000; `openalex_works`: inst=0.033, team=1.000, val=1.000, proxy=0.000; `pubmed_eutils_metadata`: inst=0.007, team=1.000, val=1.000, proxy=0.000
- Identity linkage: duplicate observation ids = 0; schemes disjoint = True; cross-mode linkable share = 0.0000 (absent evidence, not zero error).
- Survivorship: 22 of 19982 trajectories carry any outcome binding ({'VALIDATED_FAILURE': 23}); 19960 stay UNKNOWN.
- Outcome proxy disagreement: CANNOT_CHECK_FROM_EMITTED_FIELDS — fewer than two modes emit doi: trajectory ids (doi modes: ['crossref_rest_works']; non-doi: ['arxiv_atom_metadata', 'openalex_works', 'pubmed_eutils_metadata']); OpenAlex observations carry openalex:<W-id> only, so Crossref/OpenAlex retraction-channel disagreement is not computable from the normalized JSONL
- Censoring: unpublished failures are absent-by-censoring, not absent-by-fact; absence of a retraction marker never encodes success.
