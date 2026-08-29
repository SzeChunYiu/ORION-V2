# SD10 Source Adapters Design Receipt V1

- **Status**: ADAPTERS_IMPLEMENTED__NOT_EXECUTED. This PR ships lawful acquisition
  code, fixture tests and this receipt. No fetch run has been performed; SD10 stays
  unexecuted until the real population fetch, corpus assembly and bias audit run
  under their own receipts.
- **Scope**: `scripts/sd10_sources/{common,arxiv_adapter,crossref_adapter,openalex_adapter}.py`,
  fixture tests `tests/unit/test_sd10_source_adapters_wave6.py` (network-free,
  injectable transport), fixtures under `tests/fixtures/sd10/`.
- **Authority**: none granted. No artifact in this lane claims scientific truth,
  causal law, or outcome validity beyond what a source itself carries as a record.

## 1. Lawfulness notes (source by source)

All three adapters use ONLY each source's public, documented metadata API. No
scraping, no fulltext, no authentication bypass, no ToS-grey endpoints.

| Source | Endpoint | Documented terms the adapter complies with | Enforced compliance |
|---|---|---|---|
| arXiv | `https://export.arxiv.org/api/query` (Atom metadata API) | arXiv API terms of use ask for at most one request per 3 seconds, one connection at a time, and a descriptive User-Agent with contact information (https://info.arxiv.org/help/api/tou.html) | `--rate-seconds` default 3.0 and CLI-rejected below 3.0; descriptive UA `ORION-V2-SD10-research-metadata-harvester (mailto:...)`; contact email REQUIRED for non-dry runs; page size <= 100 |
| Crossref | `https://api.crossref.org/works` (REST, documented swagger) | Crossref etiquette: identify yourself with a mailto to join the polite pool (https://www.crossref.org/documentation/retrieve-metadata/rest-api/); metadata reusable with attribution | mailto in UA AND `?mailto=` param; contact email REQUIRED for non-dry runs; conservative 1.0 s min interval; documented cursor deep paging (no offset hammering) |
| OpenAlex | `https://api.openalex.org/works` (REST) | OpenAlex documents a daily request limit (100,000 calls/day) and asks for a mailto UA for the polite pool; metadata is CC0 (https://docs.openalex.org) | mailto UA/param; hard daily request budget tracked in cursor state, run STOPS before exceeding the documented limit; conservative 1.0 s min interval |

Common mechanics (`common.py`): injectable transport + sleep (tests never touch
the network); timeout + capped exponential backoff; retry ONLY on 429/5xx and
transport errors; every other HTTP 4xx raises `HardFailClosed` (exit code 2, a
failed-closed receipt is still written); `--dry-run` performs zero requests and
prints the URL plan; `--max-records` caps every run; `--since/--until` are
ISO-date windows validated at parse time; cursor state is persisted atomically
after every page so an interrupted run resumes rather than silently skipping.

## 2. Outcome-policy conservatism (the scientific-honesty core)

1. **Citation/fame metrics are proxy metrics only.** `is-referenced-by-count`,
   `cited_by_count`, reference counts and author counts land in `proxy_metrics`
   and no code path can map them to `outcome_class`.
2. **arXiv version progression is NOT an outcome.** v2/v3 deposits become
   `VERSION_OR_REVISION` observations; the arXiv adapter emits ZERO outcome
   bindings, ever (its metadata carries no validated outcome).
3. **Outcome bindings only where the source itself carries a validated record:**
   - Crossref relation kind `is-retraction-of` -> the RETRACTED trajectory gets
     `VALIDATED_FAILURE` with the retraction notice DOI as witness id.
   - Crossref `is-retracted: true` -> that trajectory gets `VALIDATED_FAILURE`
     with the record itself as witness.
   - OpenAlex `is_retracted: true` -> `VALIDATED_FAILURE`, witness = the work record.
4. **Absence is never success.** No flag/relation -> no binding -> trajectory
   stays `UNKNOWN` downstream. The corpus receipt already states
   `unpublished_failure_absence_may_be_interpreted_as_no_failure: false`.
5. Every run receipt repeats the censoring statement: unpublished failures are
   absent-by-censoring, not absent-by-fact.

## 3. Field mapping tables (source record -> DevelopmentObservation)

Identity scheme: one trajectory = one work line (arXiv id without version /
DOI / OpenAlex W id); each emitted record is one observation on that trajectory.

| Observation field | arXiv Atom entry | Crossref /works item | OpenAlex /works item |
|---|---|---|---|
| `observation_id` | `arxiv-obs:<id>v<version>` | `crossref-obs:<doi>` | `openalex-obs:<W-id>` |
| `trajectory_id` | `arxiv:<id>` (version stripped) | `doi:<doi>` | `openalex:<W-id>` |
| `domain_id` | `arxiv-cat:<primary_category>` | `crossref-subject:<first subject or uncategorized>` | `openalex-field:<field id>` else `openalex-source:<source id>` else uncategorized |
| `epoch_id` | `year:<published year>` | `year:<issued year>` | `year:<publication_year>` |
| `source_mode_id` | `arxiv_atom_metadata` | `crossref_rest_works` | `openalex_works` |
| `ordinal` | version - 1 | page order index | page order index |
| `kind` | `VERSION_OR_REVISION` if version>1 else `OTHER` | `RETRACTION` for retraction evidence, `DATA_OR_INSTRUMENT` for dataset type, else `OTHER` | `DATA_OR_INSTRUMENT` for dataset type, else `OTHER` |
| `action_feature_ids` | `arxiv:deposit_version`, `arxiv:primary_category:<cat>` | `crossref:publish_work`, `crossref:type:<type>` | `openalex:publish_work`, `openalex:type:<type>` |
| `failure_feature_ids` | (never: metadata carries none) | `crossref:is_retracted` / `crossref:retraction_notice` | `openalex:is_retracted` |
| `source_ids` | entry id URL | `doi:<doi>` | `openalex:<W-id>` |
| `validation_ids` | empty (no validation witness in metadata) | empty (witnesses live in bindings) | empty |
| `institution_ids` | empty (CANNOT_CHECK: Atom exposes no affiliations) | `crossref-inst:<institution.name>` when present | `openalex-inst:<institution id>` for each authorship institution |
| `team_id` | empty (CANNOT_CHECK) | empty (CANNOT_CHECK) | empty (CANNOT_CHECK) |
| `proxy_metrics` | `arxiv:author_count` | `crossref:is_referenced_by_count`, `crossref:reference_count`, `crossref:author_count` | `openalex:cited_by_count`, `openalex:referenced_works_count`, `openalex:author_count` |
| `bias_flag_ids` | publication, survivorship, language/geography | publication, survivorship, citation-window, language/geography | publication, survivorship, citation-window, language/geography |
| `resource_cost` | 0.0 per record (acquisition cost is accounted at run level in the receipt: request count, pages, fetched window) | same | same |

Window filters: arXiv `submittedDate:[YYYYMMDD0000 TO YYYYMMDD2359]`;
Crossref `from-pub-date/until-pub-date`; OpenAlex `from/until_publication_date`.

## 4. Bias ledger (structural biases each source induces)

- `BIAS_PUBLICATION_ONLY_CORPUS` (all three): only publicly deposited records
  exist; the file-drawer and abandoned lines without artifacts are invisible.
- `BIAS_SURVIVORSHIP_OF_INDEXED_RECORDS` (all three): indexing itself selects
  for venues/publishers that participate in the source.
- `BIAS_CITATION_WINDOW_TRUNCATION` (Crossref, OpenAlex): citation counts are
  truncated at fetch date, mechanically deflating recent work — this is why
  they can never be an outcome signal, only a biased proxy.
- `BIAS_LANGUAGE_GEOGRAPHY_SKEW` (all three): arXiv is English-predominant;
  Crossref coverage tracks publisher participation; OpenAlex documents
  incomplete regional/non-English venue coverage.
- arXiv-specific: version progression visibility is NOT success (revision
  activity is censoring-prone too — many abandoned lines stop at v1 silently).

## 5. CANNOT_CHECK / known limits

- arXiv Atom metadata carries no affiliations, citations, or team identities;
  withdrawal states are not reliably machine-readable in Atom -> institution/
  team fields stay empty and NO arXiv outcome binding is ever emitted.
- Crossref `is-retracted` coverage is incomplete (not all publishers flag);
  withdrawal-without-flag is undetectable here.
- OpenAlex `is_retracted` similarly tracks Crossref's flag upstream.
- Author lists are not stable team identities; `team_id` is left empty across
  all sources rather than guessed.
- Cursor state is per-output-path; operators must not share one state file
  across different windows/sources (receipts record lineage to make mixing
  detectable).
- Daily/interval compliance is enforced client-side in good faith; a hostile
  clock or shared IP could still exceed source expectations — the receipt
  records request counts so audits can verify.
- No fulltext, abstracts-only metadata: no content-level scientific claims are
  made anywhere in this lane.

## 6. Interface contract guarantee

Emitted observation JSONL is validated by constructing the real
`DevelopmentObservation` (and `OutcomeBinding`) dataclasses at emit time
(`common.observation_to_json` / `common.binding_to_json`), so adapter output is
byte-compatible with `scripts/assemble_scientific_development_episodes.py`
(`proxy_metrics` serialized as a JSON object keyed by metric name). The fixture
tests additionally round-trip adapter output through `assemble_all` to prove
unbound trajectories come out `UNKNOWN` and retraction-bound trajectories come
out `VALIDATED_FAILURE` with the notice DOI as witness.

