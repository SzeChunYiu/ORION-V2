# H-EXT-1N Design V1 — Naturalistic Replication of the Evidence-Structure Gate

**Status:** `FROZEN_PROSPECTIVE_DESIGN_NO_GATED_RESULTS` (frozen 2026-09-02 before any corpus
dispatch or gated evaluation). Machine-readable twin: `H_EXT1N_DESIGN_V1.json` (its sha256 is
recorded in `H_EXT1N_CORPUS_FREEZE.json` and `H_EXT1N_GATE_FREEZE.json`). Parent:
`research/experiments/h-ext1/H_EXT1_OUTCOME_RECEIPT.md`, whose honest limit 3 names this
design: *"the witnesses that separate these strata need not exist or separate anything in
real corpora."* Feasibility: `H_EXT1N_FEASIBILITY_RECEIPT.md`. Builder:
`scripts/h_ext1n_corpus_builder.py`; runner: `scripts/h_ext1n_gate_study.py` (imports the
H-EXT-1 gate logic, nulls and accuracy aggregation from `scripts/h_ext1_gate_study.py`).

## 1. Claim under test

H-EXT-1 found, on the P-D generated suite, that a cheap input-computable gate over evidence
structure (`G_B_PLUS_XREF`: duplicate identifier ∨ shared lineage root ∨ text naming another
record's root) routes the dependence machinery to exactly the tasks where it helps. Those
witnesses were planted. H-EXT-1N asks whether the same six witness types, re-instantiated on
the fields a real evidence record actually carries, still identify the activation regime when
dependence is **naturalistic**: records that report the same registered clinical trial.

## 2. Corpus (one primary source, frozen)

| Item | Frozen choice |
|---|---|
| Source | PubMed E-utilities metadata (`esearch`/`efetch`, `db=pubmed`), public and documented; ≤ 3 req/s |
| Oracle | `DataBankList/DataBank[ClinicalTrials.gov]/AccessionNumber` (NCT id). Records sharing an NCT id report one trial population = one support family |
| Topics | 10 MeSH major topics (hypertension; type 2 diabetes; heart failure; depressive disorder; asthma; breast neoplasms; stroke; obesity; COPD; rheumatoid arthritis) |
| Query | `clinicaltrials.gov[si] AND {topic}[majr] AND randomized controlled trial[pt] AND 2016:2024[dp] AND hasabstract AND english[la]` |
| Eligibility | exactly one NCT id, no other registry, English, no review/meta-analysis/editorial/letter/comment/erratum/retraction/case-report/protocol type, abstract ≥ 500 chars after removing registration sections |
| Record pool | only NCTs with ≥ 2 eligible, non-near-duplicate (title Jaccard < 0.8) publications; independent records are single publications of distinct such NCTs, so record type is matched and only co-membership differs |
| Strata (oracle only) | NS1A: 3 records, one shared NCT → 2 families → `INCONCLUSIVE…`; NS1B: 3 distinct → `ACCEPT_H`; NS1C: 4 records, two shared pairs → 2 families → `INCONCLUSIVE…`; NS1D: 4 distinct → `ACCEPT_H` |
| Size | 60 sets per stratum = 240 sets (120 dependent / 120 independent), each NCT and PMID used once |
| Arm-visible fields | `record_id, title, abstract, authors, journal, year, publication_types, grant_ids, mesh_major` |
| Held out | PMID, DOI, every registry accession, affiliations, registration-labelled abstract sections, stratum, split, answer |
| Redaction | every registry-id-shaped token, PMID and DOI string in title/abstract → the single marker `[REGISTRY-ID]` |
| Canary | build-time: no forbidden key, none of the set's NCT/PMID/DOI strings in the serialized task, no registry-shaped token survives; extract-time: H-EXT-1 injected-oracle-key canary on every candidate gate |
| Custody | raw pages cached with per-page sha256; per-record and per-corpus sha256 committed in `H_EXT1N_CORPUS_FREEZE.json`; record texts stay on the build host (`billy-old`), PMIDs committed |

**Adequacy (checked before anything is dispatched):** ≥ 150 sets, ≥ 30 per stratum,
dependent/independent imbalance ≤ 10 %, ≥ 5 topics populated. Failure →
`CORPUS_ANNOTATION_INSUFFICIENT` (CANNOT_CHECK), nothing dispatched.

Registered decision rule shipped in every task (verbatim in the JSON twin): a support family
is the set of records reporting the same underlying study population (primary results,
secondary/post-hoc analyses, sub-studies, extensions, follow-ups); `ACCEPT_H` iff ≥ 3
independent families and no surviving defeater (none registered); otherwise
`INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT`; also return
`independent_support_family_count`. Scoring is exact match on both keys.

## 3. Arms, model, host

| Role | Arm | Notes |
|---|---|---|
| `M` (always-on) | `P_D_FULL` | `scripts/orion_pd_arms.py`, unchanged |
| `OFF` (always-off) | `P_D_MINUS_DEPENDENCE` | same module |
| `PARENT` | `STRONGEST_ASSURANCE_FEDERATION` | same module |
| `GATED_M` | `M(x)` if `gate(x)` else `OFF(x)` | routed arm's archived row/response |

Model: **gpt-5.5** via `codex exec --ephemeral` (codex-cli 0.129.0-alpha.15,
`ORION_CODEX_BIN=/home/billy/.npm-global/bin/codex`), read-only sandbox, one call per
instance per arm, resource parity — identical to the H-EXT-1 prospective cell. Host for
corpus fetch, build and all model arms: **billy-old** (LUNARC unreachable at design time).
Dispatch/evaluate: `run_formal_discovery_generated_suite.py` `dispatch()`/`evaluate()` reused
unchanged (oracle deleted for the whole child dispatch, hash-committed, restored, re-hashed).

## 4. Splits and sequencing

`N1-DEV` = 35 % of sets, stratified by (topic, stratum), seeded, membership frozen in the
corpus freeze. Sequence: build + freeze corpus → dispatch `N1-DEV` → select gate on DEV →
commit `H_EXT1N_GATE_FREEZE.json` → dispatch `N1-EVAL` → score. The EVAL responses do not
exist when the gate is frozen.

## 5. Witnesses and gate family (same six types as H-EXT-1)

| H-EXT-1 witness | Naturalistic instantiation |
|---|---|
| `w_dup_hash` (duplicate identifier) | two records share a visible grant id |
| `w_shared_root` (shared lineage root) | two records share the normalized last (senior) author |
| `w_declared_overlap` | title/abstract matches the frozen declared-relation regex (secondary / post-hoc / pre-specified / exploratory / ancillary / extension / sub-study / follow-up / pooled / subgroup + analysis / study / report / results) |
| `w_xref_root` (text names another record's root) | an uppercase token `[A-Z][A-Z0-9-]{3,}` from one record's **title** occurs in another record's title or abstract |
| `w_shared_token` | an uppercase token (identical regex) occurs in ≥ 2 records' title+abstract |
| `n_records`, `n_roots`, `root_ratio` | records; author-link connected components; ratio |

Candidate family, selection rule (`dev_advantage = acc(GATED_M) − max(acc(M), acc(OFF))`
on DEV, argmax, ties → lower activation rate → family order, abort with
`NO_CANDIDATE_GATE_ON_DEV` if none > 0), and reference gates (`ALWAYS_ON`, `ALWAYS_OFF`,
`ORACLE_STRATUM` ceiling) are exactly H-EXT-1's. `topic` and `n_records` are arm-visible
metadata, excluded from the family; they define the within-metadata null and the G4 unit.

## 6. Nulls and gates

`NULL_POOLED`: 2000 random gates with the selected gate's activation count (seed 20260902).
`NULL_WITHIN`: 2000 random gates matching the activation count inside each arm-visible
topic × size-class cell (seed 20260903) — a gate that only knows the visible metadata cannot
beat it. The oracle stratum is never used to build a null.

| Gate | Pass condition |
|---|---|
| G0 | DEV/EVAL disjoint; EVAL built from the frozen corpus and the gate frozen on it; canary passes; all arms present on every EVAL task |
| G1 | `acc(GATED_M) ≥ acc(M)`, `calls(GATED_M) ≤ calls(M)`, `mean_wall(GATED_M) ≤ 1.05·mean_wall(M)` |
| G2 | `acc(GATED_M) > acc(OFF)` and `acc(GATED_M) ≥ acc(PARENT)` |
| G3 | advantage > q95 of `NULL_POOLED` |
| G3S | advantage > q95 of `NULL_WITHIN` |
| G4 | in each size class (3, 4 records) `acc(GATED_M) ≥ max(acc(M), acc(OFF))` |

## 7. Pre-registered routing (precedence top-down)

| Condition | Terminal |
|---|---|
| corpus adequacy or build canary fails | `CORPUS_ANNOTATION_INSUFFICIENT` (CANNOT_CHECK) |
| DEV or EVAL run has missing/failed responses | `CANNOT_CHECK_RUN_INVALID` |
| no candidate gate with `dev_advantage > 0` | `NO_CANDIDATE_GATE_ON_DEV` (EVAL never dispatched) |
| G0 fails | `DESIGN_VIOLATION_RUN_VOID` |
| G1 fails | `GATING_DOES_NOT_DOMINATE_ALWAYS_ON` |
| G2 fails vs OFF | `GATING_DOES_NOT_DOMINATE_ALWAYS_OFF` |
| G2 fails vs PARENT | `STRONGEST_PARENT_SUFFICIENT_UNDER_GATING` |
| G3 fails | `ACTIVATION_POLICY_NOT_IDENTIFIABLE_IN_NATURALISTIC_RECORDS` |
| G4 fails | `ACTIVATION_ADVANTAGE_NOT_SIGN_CONSISTENT` |
| G3 passes, G3S fails | `ACTIVATION_POLICY_IDENTIFIABLE_ONLY_AT_METADATA_GRANULARITY` |
| all pass | `CONDITIONAL_ACTIVATION_IDENTIFIABLE_IN_NATURALISTIC_RECORDS` |

Secondary, reported never routed: per-oracle-stratum table, activation precision/recall
against NS1A/NS1C, M-vs-OFF paired discordance with exact McNemar p (the naturalistic
replication of the P-D dependence contrast itself), per-topic accuracies.

## 8. No-rescue clause

After the gate freeze: no re-selection, threshold or regex change, set/topic exclusion, null
redefinition, corpus rebuild or arm substitution. A failed gate is recorded under its routed
terminal. Any repair is V2 with its own freeze.

## 9. Honest limits (frozen before results)

- Oracle noise: distinct NCT ids can still share a population (separately registered
  extensions); such sets are labelled independent, so M errors on NS1B/NS1D partly measure
  annotation noise, not only over-triggering.
- The multi-publication pool favours larger, often named trials; the acronym witness is
  easier here than in a random literature sample.
- One model family (gpt-5.5); abstracts and metadata only; no full text.
- The six witnesses are H-EXT-1's family re-instantiated, not the best naturalistic gate. A
  negative says these witnesses do not identify the regime in these records.

```text
H_EXT1N_DESIGN = FROZEN_PROSPECTIVE_NO_GATED_RESULTS
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_FIELD_STATUS = false
GRANTS_REAL_CORPUS_DEPENDENCE_DETECTION = false
GRANTS_MANUSCRIPT_CHANGE = false
```

skills-applied: none (design receipt, no manuscript content)
