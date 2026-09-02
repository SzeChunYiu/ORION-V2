# H-EXT-1N Feasibility Receipt — Candidate Naturalistic Corpora

**Date:** 2026-09-02. **Host for reconnaissance:** billy-old (internet; LUNARC unreachable).
**Requirement (design brief):** a real, lawful, public source in which dependence among
supports is independently annotated or derivable from metadata the arms never see; ≥ 150
evidence sets with balanced dependent/independent oracle labels; oracle held out of every
arm-visible field with a programmatic canary.

## Feasibility table

| Candidate | Dependence annotation (oracle) | Size reachable | Annotation quality | Licence / access | Decision semantics match to PD-S1 | Verdict |
|---|---|---|---|---|---|---|
| **(a) PubMed records sharing a ClinicalTrials.gov registration** | `DataBankList` NCT accession per record (structured metadata, never in arm-visible fields after redaction) | Reconnaissance 2026-09-02, 10 MeSH topics, RCT[pt], 2016–2024: **9 462 records fetched, 1 126 NCTs with ≥ 2 eligible publications (3 565 records)**; 240 sets need 660 such NCTs | High: same NCT = same registered trial population by construction; residual noise from separately registered extensions (documented limit) | NLM E-utilities: public, documented, ≤ 3 req/s without key; metadata + abstracts retrievable programmatically; abstracts not redistributed (PMIDs + hashes committed) | Exact: "records reporting the same trial = one support family; ACCEPT_H iff ≥ 3 independent families" is PD-S1's registered rule with a naturalistic family definition | **CHOSEN** |
| (b) Replication projects (RP:P, Many Labs 1–5) | original–replication pairs share materials/protocol (OSF, CC0/CC-BY) | ~100 RP:P pairs + ~30–50 Many Labs effects × sites; ≥ 150 sets only by pooling projects with different structures | High as pairs, but the dependence *kind* differs: direct replications share instruments yet sample new populations; P-D's family rule (same latent source) is ambiguous for them — a replication is usually counted as independent corroboration | Open | Weak: the oracle label "dependent" is contestable, so a negative could not be attributed to the gate | rejected (semantics) |
| (c) Retraction Watch / Crossref retraction links → downstream citing works | citing works that share a retracted upstream reference (OpenAlex `referenced_works`) | Large (Retraction Watch via Crossref Labs, CC0; OpenAlex open) | Medium: shared citation ≠ shared evidence source; most citers cite tangentially | Open | Matches PD-S3 (revocation/uptake), not PD-S1 dependent corroboration; reference lists would have to be hidden, removing the one field that carries the dependence | rejected (wrong study family) |

## Reconnaissance numbers (a)

`H_EXT1N_RECON_PUBMED_NCT_20260902.json` (query as frozen in the design; fetched on billy-old):

| Topic | esearch count | NCTs | NCTs ≥ 2 pubs | records in those |
|---|---|---|---|---|
| hypertension | 846 | 569 | 87 | 307 |
| diabetes mellitus, type 2 | 1846 | 1189 | 206 | 688 |
| heart failure | 1039 | 539 | 146 | 579 |
| depressive disorder | 707 | 474 | 84 | 228 |
| asthma | 420 | 296 | 30 | 87 |
| breast neoplasms | 1247 | 877 | 172 | 460 |
| stroke | 1141 | 709 | 146 | 526 |
| obesity | 1226 | 864 | 138 | 377 |
| COPD | 519 | 342 | 47 | 129 |
| rheumatoid arthritis | 471 | 303 | 70 | 184 |
| **total** | 9462 | 6162 | **1126** | 3565 |

Budget: one cycle (NS1A+NS1B+NS1C+NS1D) consumes 11 NCTs; 60 cycles = 660 NCTs ≤ 1 126
available before the near-duplicate filter (which removes only same-title re-publications).
The design's adequacy floor (≥ 150 sets, ≥ 30 per stratum) is reachable with a wide margin;
the build receipt reports the realised counts.

Per-record efetch XML verified live (2026-09-02, PMIDs 34959951/34941131/34913976): NCT ids
sit in `DataBankList` AND in a `TRIAL REGISTRATION` abstract section — hence the redaction
rule drops registration-labelled sections and replaces every registry-shaped token.

## Corpus, model and host bindings

- Corpus build: billy-old, `/home/billy/hext1n/` (raw cache + full record texts stay there;
  `H_EXT1N_CORPUS_FREEZE.json` with per-record sha256 and PMIDs is committed).
- Model arms: gpt-5.5 via codex-cli 0.129.0-alpha.15 (`/home/billy/.npm-global/bin/codex`)
  on billy-old, as in the H-EXT-1 prospective cell (`/home/billy/hext1-prospective`).
- `CORPUS_ANNOTATION_INSUFFICIENT` is not reached at feasibility level; it remains the
  pre-registered terminal if the frozen build falls below the adequacy floor.

```text
H_EXT1N_FEASIBILITY = PRIMARY_CORPUS_SELECTED (PubMed-NCT)
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_REAL_CORPUS_DEPENDENCE_DETECTION = false
```
