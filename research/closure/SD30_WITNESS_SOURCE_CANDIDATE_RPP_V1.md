# SD30 Witness Source Candidate V1 — REGISTERED_REPLICATION_VERDICT (RP:Psychology) (2026-08-29)

Schema: `orion.v2.sd30-witness-source-candidate.v1` · Classification:
**`WITNESS_SOURCE_CANDIDATE__C2_PRICED__NOT_INGESTED`**

This prices the C2 lever named in `SD30_STRUCTURAL_PILOT_RECEIPT_V1.md` §3
("a lawful, non-fame, prospectively-defined success witness source —
unpriced"). It is reconnaissance with real counts, NOT an ingestion: no
binding pass, no outcome-policy change, no new corpus.

## 1. Source and provenance (lawful, public)

| Item | Value |
|---|---|
| Project | Reproducibility Project: Psychology — OSF node `ezcuj` (Open Science Collaboration, *Science* 349:aac4716, 2015; paper component `ezum7`) |
| Data | component `ytpuq` (Analysis) → `rpp_data.csv` (259,220 B, 168 rows × 136 cols) + `rpp_data_codebook.csv` (130 variables) |
| Access | OSF public API v2 (`api.osf.io`), no auth; 5 API GETs + 2 file downloads (2026-08-29) |
| Integrity | sha256 of both files recorded in `research/experiments/results/issue50/sd30/rpp_witness_inventory.json` |
| Lawful-source class | public registry/project metadata + published supplementary dataset (same class as the Crossref/OpenAlex/PubMed/arXiv adapters) |

## 2. Proposed witness class: REGISTERED_REPLICATION_VERDICT

An **independent, prospectively-planned replication attempt** of a specific
published original, with **a priori success criteria**, judged by the
replicating team. Verbatim codebook definition of the verdict field
(`Replicate (R)`): *"Whether or not the replication reproduced the original's
results, judged by the replicator, according to a priori criteria: yes or no."*

This satisfies every constraint the frozen outcome policy imposes:
- **not** absence-of-retraction (`absence_of_retraction_is_never_success` untouched);
- **not** a citation/fame metric (`citation_or_prize_metric_is_truth_label=false` untouched);
- prospective (criteria fixed before outcome known), non-fame (no prestige
  signal), witnessed by an independent third party (the replicating team).

**Strict composite criterion** (conservative): replicator verdict AND
meta-analytic significance must agree.

## 3. Counts (verified 2026-08-29, reproduce in §6)

| Quantity | Value |
|---|---|
| rows with a-priori verdict AND original title | 100 / 168 (the canonical RP:P 100) |
| distinct original titles | 98 |
| replicator verdict yes / no | 39 / 61 |
| meta-analysis significant (of rows with both) | 51 yes / 24 no |
| subjective↔meta-analytic agreement | 48/75 = 64% (divergence is real; hence the strict composite) |
| **STRICT_SUCCESS** (yes ∧ MA significant) | **26** |
| **STRICT_FAILURE** (no ∧ MA not significant) | **22** |
| MIXED (indices disagree) | 52 |

Derived inventory: `research/experiments/results/issue50/sd30/rpp_witness_inventory.json`
(all 100 witnessed rows: title, journal, verdict, MA flag, CI-containment
flag, OSF project URL, composite class).

## 4. Price of full ingestion (what C2 would actually cost)

1. **Binding pass**: originals carry NO DOI column — identifier fields are
   Title/Journal/Volume/Issue/Pages → ~98 Crossref title-resolution queries
   (lawful, existing crossref source class) to obtain `doi:` trajectory ids;
   116 rows also carry the replication's OSF project URL.
2. **Outcome-policy amendment**: admit REGISTERED_REPLICATION_VERDICT as a
   VALIDATED_SUCCESS / VALIDATED_FAILURE witness class (strict composite).
   This is exactly the successes-AND-failures ingestion the protocol
   amendment already demands.
3. **Adapter mode**: one bounded OSF/crossref mode; **no new framework**.

## 5. Honest consequences for the SD30 counts

| Count | Effect |
|---|---|
| C1 (empty operator set) | unchanged — SD20 scale-up still in flight |
| **C2 (zero validated successes)** | **PRICED and executable**: 26 strict success + 22 strict failure witnesses on 98 originals |
| C3 (witness domain ≠ operator domain) | **NOT unblocked** — originals are 2008 psychology journal articles; they have no arXiv version ladders, so SD20 transition operators remain unevaluable on these trajectories |
| C4 (cross-mode identity linkage) | **NOT unblocked** — binding yields `doi:` ids; the ladder domain is `arxiv:` |

Net: the matched contrast (SD30 rule) stays closed until a witness class binds
to **ladder-bearing** trajectories; but the outcome ontology gains its first
lawful success-witness mechanism and a **second independent failure
mechanism** (failed registered replication, 22) alongside retraction (23) —
failure witnessing no longer rests on retraction alone.

Same-class sources, named but unpriced: Reproducibility Project: Cancer
Biology (eLife/OSF), Many Labs 1–5, Registered Replication Reports — the
witness class generalizes beyond this one project.

## 6. Reproduce

```bash
curl -sL -o rpp_data.csv     "https://osf.io/download/fgjvw/"   # ezcuj/ytpuq
curl -sL -o rpp_codebook.csv "https://osf.io/download/bhcsf/"
# verdict/MA cross-tab + strict composite: see rpp_witness_inventory.json
# generation script (issue50/sd30/rpp_witness_inventory.json §source carries
# sha256 of both files for verification)
```
