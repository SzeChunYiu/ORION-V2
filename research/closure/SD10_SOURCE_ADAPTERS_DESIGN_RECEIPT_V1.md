# SD10 Source Adapters Design Receipt V1

- **Status**: ADAPTERS_IMPLEMENTED__NOT_EXECUTED. The adapter PRs ship lawful
  acquisition code, fixture tests and this receipt only — NO fetch run has been
  performed (including the PubMed adapter PR); SD10 stays unexecuted until the
  real population fetch, corpus assembly and bias audit run under their own
  receipts.
- **Scope**: `scripts/sd10_sources/{common,arxiv_adapter,crossref_adapter,openalex_adapter,pubmed_adapter}.py`,
  fixture tests `tests/unit/test_sd10_source_adapters_wave6.py` (network-free,
  injectable transport), fixtures under `tests/fixtures/sd10/`.
- **Authority**: none granted. No artifact in this lane claims scientific truth,
  causal law, or outcome validity beyond what a source itself carries as a record.

## 1. Lawfulness notes (source by source)

All four adapters use ONLY each source's public, documented metadata API. No
scraping, no fulltext, no authentication bypass, no ToS-grey endpoints.

| Source | Endpoint | Documented terms the adapter complies with | Enforced compliance |
|---|---|---|---|
| arXiv | `https://export.arxiv.org/api/query` (Atom metadata API) | arXiv API terms of use ask for at most one request per 3 seconds, one connection at a time, and a descriptive User-Agent with contact information (https://info.arxiv.org/help/api/tou.html) | `--rate-seconds` default 3.0 and CLI-rejected below 3.0; descriptive UA `ORION-V2-SD10-research-metadata-harvester (mailto:...)`; contact email REQUIRED for non-dry runs; page size <= 100 |
| Crossref | `https://api.crossref.org/works` (REST, documented swagger) | Crossref etiquette: identify yourself with a mailto to join the polite pool (https://www.crossref.org/documentation/retrieve-metadata/rest-api/); metadata reusable with attribution | mailto in UA AND `?mailto=` param; contact email REQUIRED for non-dry runs; conservative 1.0 s min interval; documented cursor deep paging (no offset hammering) |
| OpenAlex | `https://api.openalex.org/works` (REST) | OpenAlex documents a daily request limit (100,000 calls/day) and asks for a mailto UA for the polite pool; metadata is CC0 (https://docs.openalex.org) | mailto UA/param; hard daily request budget tracked in cursor state, run STOPS before exceeding the documented limit; conservative 1.0 s min interval |
| PubMed | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{esearch,efetch}.fcgi?db=pubmed` (NCBI E-utilities, https://www.ncbi.nlm.nih.gov/books/NBK25499/) | E-utilities document max 3 requests/second WITHOUT an API key (none is used) and ask for a descriptive UA identifying the caller | `--rate-seconds` default 0.5 and CLI-rejected below 0.334 (the 1/3 s floor of the documented 3 req/s ceiling); descriptive UA `ORION-V2-SD10-research-metadata-harvester (mailto:...)`; contact email REQUIRED for non-dry runs; two documented requests per page (esearch JSON page -> one efetch XML for exactly that page's PMIDs) |

Common mechanics (`common.py`): injectable transport + sleep (tests never touch
the network); timeout + capped exponential backoff; retry ONLY on 429/5xx and
transport errors; every other HTTP 4xx raises `HardFailClosed` (exit code 2, a
failed-closed receipt is still written); `--dry-run` performs zero requests and
prints the URL plan; `--max-records` caps every run; `--since/--until` are
ISO-date windows validated at parse time; cursor state is persisted atomically
after every page so an interrupted run resumes rather than silently skipping.

Durable resume (`common.OutputLedger`): fetched records are APPENDED to the
output JSONL after every page and BEFORE the cursor state advances, then the
file is atomically rewritten (deduped by observation id / by
trajectory+witnesses for bindings) at run end. A crash between an append and
the cursor advance therefore only re-fetches rows already safely on disk, and
the load-time dedupe removes such duplicates — an interrupted run never loses
already-fetched records. A crash DURING an append can tear the final write
(truncated JSON or a split UTF-8 sequence); the loader applies the
append-only commit rule that a row counts only once its trailing newline is
on disk, drops the unterminated tail (those rows were never durably written
and are re-fetched), and the end-of-run atomic rewrite heals the file. Any
newline-terminated line that fails to decode or parse is treated as real
corruption and raises rather than being silently skipped. Receipts
distinguish `observations_emitted` (new this run) from
`observations_in_output` (total merged corpus slice).

Cursor paging follows each source's documented protocol exactly: Crossref
sends `cursor=*` on the first request and repeats `message.next-cursor`
afterwards (`offset` is never sent — the API documents that `rows` may be
combined with `cursor` but `offset` may not); OpenAlex sends `cursor=*` first
and repeats `meta.next_cursor` afterwards. The OpenAlex daily budget is keyed
by UTC date in the state file, so a new UTC day RESETS the counter instead of
resuming a spent budget forever. PubMed pages STATELESSLY with
`retstart`/`retmax` + `sort=pub_date` (esearch `datetype=pdat` window):
`usehistory`/WebEnv server-side history is deliberately NOT used because it
expires server-side and cannot satisfy the resumable-cursor contract above;
the persisted cursor is simply the next `retstart`, and the receipt records
this choice.

PubMed truncation cannot be silent (all live-verified 2026-08-29):

- ESearch stateless paging has a HARD ceiling: `retstart > 9998` returns
  HTTP 200 with a top-level `esearchresult.ERROR` string ("... ESearch can
  only retrieve the first 9,999 records matching the query ..."). The adapter
  FAILS CLOSED on that ERROR key (it is distinct from `errorlist`), so a
  window larger than 9,999 records aborts with exit 2 and a failed-closed
  receipt instead of silently writing a truncated corpus. Operators fetch
  larger windows by splitting the date range.
- A page returning fewer PMIDs than requested while the esearch `count`
  still shows unconsumed records (ceiling hit mid-page, or index drift)
  also fails closed — end-of-results is only ever `count == consumed`.
- Every page's `count` and the server's `querytranslation` echo are recorded
  in the run receipt (`esearch_window.counts_by_page` /
  `querytranslations`), and the echo is VERIFIED to contain the full
  `mindate:maxdate[Date - Publication]` range: a capture where the window
  collapsed to a single date (matching 242,229 records instead of the
  1,739,765-record 2024 window) proved this wrong-corpus failure class is
  real, so a collapsed echo fails closed rather than fetching the wrong
  PMID set. A drifted overlap that still pages normally is a fidelity limit,
  not a silent skip: the output ledger keys by observation id so overlap is
  deduped, never duplicated.

## 2. Outcome-policy conservatism (the scientific-honesty core)

1. **Citation/fame metrics are proxy metrics only.** `is-referenced-by-count`,
   `cited_by_count`, reference counts and author counts land in `proxy_metrics`
   and no code path can map them to `outcome_class`.
2. **arXiv version progression is NOT an outcome.** v2/v3 deposits become
   `VERSION_OR_REVISION` observations; the arXiv adapter emits ZERO outcome
   bindings, ever (its metadata carries no validated outcome).
3. **Outcome bindings only where the source itself carries a validated record:**
   - Crossref: a retraction NOTICE record whose `update-to` array carries an
     entry with `type: "retraction"` -> the RETRACTED trajectory gets
     `VALIDATED_FAILURE` with the retraction notice DOI as witness id. Verified
     against live `api.crossref.org` responses on 2026-08-29 (e.g. notice
     `10.1016/s0140-6736(10)60175-4` carries `update-to:
     [{DOI: "10.1016/s0140-6736(97)11096-0", type: "retraction", ...},
     {type: "correction", ...}]`): `update-to` is the only source-carried
     retraction channel in the current API — there is no `is-retracted` field,
     the relation-type enum contains no retraction kind (`is-retraction-of` is
     rejected as invalid), and the retracted target record itself typically
     carries no marker at all. Corrections and other update types do NOT bind.
   - OpenAlex `is_retracted: true` (a documented Work boolean) ->
     `VALIDATED_FAILURE`, witness = the work record.
   - PubMed PublicationType (verified against live efetch XML on 2026-08-29;
     fixtures under `tests/fixtures/sd10/pubmed_*` are trimmed live responses
     from that date): `"Retracted Publication"` (live UI `D016441`, e.g. PMID
     33522354, "RETRACTED: Effects of Methyl Donors on L-Tryptophan
     Fermentation") marks the RETRACTED ARTICLE ITSELF -> that trajectory
     binds `VALIDATED_FAILURE` with the pubmed record as its OWN witness —
     unlike Crossref, where only the notice knows and the witness must be the
     notice DOI. `"Retraction Notice"` (live UI `D016440`, e.g. PMID 36017998,
     the notice for 33522354) marks the retraction NOTICE -> an observation of
     kind `RETRACTION` with NO binding (a notice documents a failure, it is
     not the failed work). The legacy notice vocabulary `"Retraction of
     Publication"` is matched defensively too but no longer resolves as a
     live `[ptyp]` search term (`retraction notice[ptyp]` is the current
     term, 33,177 records live on 2026-08-29). Corrections/errata
     (`"Published Erratum"`, UI `D016425`, e.g. PMID 42462751) do NOT bind.
     The notice-to-target PMID link
     (`CommentsCorrectionsList/CommentsCorrections[@RefType='RetractionOf']`)
     is intentionally NOT a binding channel: the retracted record already
     carries its own PT witness, and keying on the PT (text, never the UI —
     the live UI assignment differs from the legacy one) keeps the witness
     first-party.
4. **Absence is never success.** No flag/update entry -> no binding -> trajectory
   stays `UNKNOWN` downstream. The corpus receipt already states
   `unpublished_failure_absence_may_be_interpreted_as_no_failure: false`.
5. Every run receipt repeats the censoring statement: unpublished failures are
   absent-by-censoring, not absent-by-fact.

## 3. Field mapping tables (source record -> DevelopmentObservation)

Identity scheme: one trajectory = one work line (arXiv id without version /
DOI / OpenAlex W id); each emitted record is one observation on that trajectory.

| Observation field | arXiv Atom entry | Crossref /works item | OpenAlex /works item | PubMed efetch `PubmedArticle` |
|---|---|---|---|---|
| `observation_id` | `arxiv-obs:<id>v<version>` | `crossref-obs:<doi>` | `openalex-obs:<W-id>` | `pubmed-obs:<PMID>` |
| `trajectory_id` | `arxiv:<id>` (version stripped) | `doi:<doi>` | `openalex:<W-id>` | `pubmed:<PMID>` |
| `domain_id` | `arxiv-cat:<primary_category>` | `crossref-subject:<first subject or uncategorized>` | `openalex-field:<field id>` else `openalex-source:<source id>` else uncategorized | `pubmed-mesh:<first DescriptorName UI>` (MeshHeadingList) else `pubmed-journal:<NlmUniqueID>` (MedlineJournalInfo) else uncategorized |
| `epoch_id` | `year:<published year>` | `year:<issued year>` | `year:<publication_year>` | `year:<first-public-appearance year>` (Article/ArticleDate Year — the electronic-publication channel, a direct child of Article in live XML; else Journal/JournalIssue/PubDate Year, else leading year of MedlineDate, else unknown. PubMed `[dp]` is MULTI-VALUED — live-verified: PMIDs 33522354 and 42493777 each match both their electronic and print years via `<uid>[UID] AND <year>[dp]` — so the epoch pins the earliest observable publication channel; ahead-of-print records carry the window-matching pdat in ArticleDate while the Journal PubDate still holds the future print year) |
| `source_mode_id` | `arxiv_atom_metadata` | `crossref_rest_works` | `openalex_works` | `pubmed_eutils_metadata` |
| `ordinal` | version - 1 | cumulative index (already-emitted + in-run order), stable across resumes | cumulative index (stable across resumes) | cumulative index (stable across resumes) |
| `kind` | `VERSION_OR_REVISION` if version>1 else `OTHER` | `RETRACTION` for records carrying a type=retraction `update-to` entry, `DATA_OR_INSTRUMENT` for dataset type, else `OTHER` | `DATA_OR_INSTRUMENT` for dataset type, else `OTHER` | `RETRACTION` for PT `Retracted Publication` OR PT `Retraction Notice`, `CORRECTION` for PT `Published Erratum`, else `OTHER` |
| `action_feature_ids` | `arxiv:deposit_version`, `arxiv:primary_category:<cat>` | `crossref:publish_work`, `crossref:type:<type>` | `openalex:publish_work`, `openalex:type:<type>` | `pubmed:publish_work`, `pubmed:pubtype:<first PublicationType text>` |
| `failure_feature_ids` | (never: metadata carries none) | `crossref:retraction_notice` (on the notice record only; the unmarked retracted target gets none) | `openalex:is_retracted` | `pubmed:retracted_publication` (on the retracted article itself) / `pubmed:retraction_notice` (on the notice record only); none for errata or plain records |
| `source_ids` | entry id URL | `doi:<doi>` | `openalex:<W-id>` | `pubmed:<PMID>` |
| `validation_ids` | empty (no validation witness in metadata) | empty (witnesses live in bindings) | empty | empty |
| `institution_ids` | empty (CANNOT_CHECK: Atom exposes no affiliations) | `crossref-inst:<institution.name>` when present | `openalex-inst:<institution id>` for each authorship institution | `pubmed-inst:<AffiliationInfo/Affiliation text>` for each distinct author affiliation (verbatim free text; not a canonical institution id) |
| `team_id` | empty (CANNOT_CHECK) | empty (CANNOT_CHECK) | empty (CANNOT_CHECK) | empty (CANNOT_CHECK) |
| `proxy_metrics` | `arxiv:author_count` | `crossref:is_referenced_by_count`, `crossref:reference_count`, `crossref:author_count` | `openalex:cited_by_count`, `openalex:referenced_works_count`, `openalex:author_count` | `pubmed:author_count`, `pubmed:mesh_heading_count` (PubMed XML carries NO citation counts; none are invented) |
| `bias_flag_ids` | publication, survivorship, language/geography | publication, survivorship, citation-window, language/geography | publication, survivorship, citation-window, language/geography | publication, survivorship, language/geography (NO citation-window flag: the source exposes no citation counts to truncate) |
| `resource_cost` | 0.0 per record (acquisition cost is accounted at run level in the receipt: request count, pages, fetched window) | same | same | same |

Window filters: arXiv `submittedDate:[YYYYMMDD0000 TO YYYYMMDD2359]`;
Crossref `from-pub-date/until-pub-date`; OpenAlex `from_publication_date` /
`to_publication_date` (the end-date filter is `to_publication_date`;
`until_publication_date` does not exist); PubMed esearch `datetype=pdat`
with `mindate/maxdate` (live-verified 2026-08-29 with the adapter's exact
URL shape: the server echoes and applies the full range —
`querytranslation` returns `2024/01/01:2024/12/31[Date - Publication]`,
count 1,739,765, vs 242,229 for the single-date query; the adapter sends
`YYYY/MM/DD` directly and verifies the echo, see the truncation rules
above).

## 4. Bias ledger (structural biases each source induces)

- `BIAS_PUBLICATION_ONLY_CORPUS` (all four): only publicly deposited records
  exist; the file-drawer and abandoned lines without artifacts are invisible.
- `BIAS_SURVIVORSHIP_OF_INDEXED_RECORDS` (all four): indexing itself selects
  for venues/publishers that participate in the source.
- `BIAS_CITATION_WINDOW_TRUNCATION` (Crossref, OpenAlex): citation counts are
  truncated at fetch date, mechanically deflating recent work — this is why
  they can never be an outcome signal, only a biased proxy. (Not flagged for
  arXiv/PubMed, which expose no citation counts at all.)
- `BIAS_LANGUAGE_GEOGRAPHY_SKEW` (all four): arXiv is English-predominant;
  Crossref coverage tracks publisher participation; OpenAlex documents
  incomplete regional/non-English venue coverage; MEDLINE indexing policy
  skews toward journals selected for MEDLINE (non-indexed venues appear only
  as PubMed-not-MEDLINE/In-Process records without MeSH).
- arXiv-specific: version progression visibility is NOT success (revision
  activity is censoring-prone too — many abandoned lines stop at v1 silently).
- PubMed-specific: MeSH-based domain identity exists ONLY for indexed records
  (In-Process/PubMed-not-MEDLINE fall back to journal identity), so domain
  coverage is biased by indexing lag and policy; affiliation strings are
  free text and over- or under-count institutions (consortium papers list
  hundreds, letters list none).

## 5. CANNOT_CHECK / known limits

- arXiv Atom metadata carries no affiliations, citations, or team identities;
  withdrawal states are not reliably machine-readable in Atom -> institution/
  team fields stay empty and NO arXiv outcome binding is ever emitted.
- Crossref: retraction evidence exists only where a notice record carries a
  type=retraction `update-to` entry (verified live 2026-08-29). Notices
  deposited without such an entry, and withdrawals with no notice at all, are
  undetectable here; the retracted target record itself usually carries no
  marker, which is why the binding witness is always the notice DOI.
- OpenAlex `is_retracted` tracks Crossref-derived retraction evidence
  upstream; works retracted without a Crossref-recorded notice can stay
  unflagged.
- PubMed: retraction evidence is the record's OWN PublicationType, so a
  retraction not yet flagged by NLM curation (or expressed only in the
  article title "RETRACTED:" text without the PT) is undetectable here;
  PubMed XML carries no citation counts, so no citation-window proxy exists
  (nothing invented); the CommentsCorrections RefType channel is recorded but
  deliberately not a binding channel; affiliations are free-text strings, not
  canonical institution identifiers; stateless retstart paging cannot exceed
  the first 9,999 records of a window (ESearch ceiling, live-verified
  2026-08-29) — larger windows must be split into smaller date ranges by the
  operator (the adapter fails closed rather than truncating silently).
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
out `VALIDATED_FAILURE` — with the notice DOI as witness for Crossref and with
the record's own `pubmed:<PMID>` as witness for PubMed (whose retracted
articles carry the PT marker themselves).

Fixture provenance: every `tests/fixtures/sd10/pubmed_*` file is a TRIMMED
live NCBI E-utilities response captured on 2026-08-29. The window fixtures
(`pubmed_esearch_page1/2.json`, `pubmed_efetch_page1/2.xml`) were captured
with the adapter's EXACT URL shape (datetype=pdat + mindate/maxdate +
sort=pub_date + retstart/retmax=3 for the 2024 window): their `count`
(1,739,765) and `querytranslation` (`2024/01/01:2024/12/31[Date -
Publication]`) are the live window echo the adapter verifies and records.
The retraction-set fixtures come from a 4-UID OR-term esearch plus its efetch
(live verbatim). The ceiling `ERROR` body reproduced in
`test_pubmed_esearch_error_field_fails_closed` is a verbatim live response
(retstart=20000). Trimming removed only element blocks the adapter never
reads (`Abstract`, `OtherAbstract`, `KeywordList`, `InvestigatorList`,
`PubmedData/ReferenceList`) to keep the fixtures small, with the trim
invariant verified by running the adapter's own parser over raw and trimmed
bodies and asserting identical records; every element path the adapter
parses is present verbatim in a live-response fixture.

